import optparse
import sys
from decimal import *
from math import *

import yaml


# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from read_bins import read_bins
from sample_shortnames import *
from Utils import GetDirectory, border_msg, logger

grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)

# Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',    dest='SOURCEDIR',  type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--inYAMLFile', dest='inYAMLFile', type='string', default="Inputs/observables_list.yml", help='Input YAML file having observable names and bin information')
    parser.add_option('',   '--asimovModel',dest='ASIMOV',type='string',default='ggH_powheg15_JHUgen_125', help='Name of the asimov data mode')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.38', help='Asimov Mass')
    parser.add_option('',   '--unfoldModel',dest='UNFOLD',type='string',default='ggH_powheg15_JHUgen_125', help='Name of the unfolding model')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--fixFrac', action='store_true', dest='FIXFRAC', default=False, help='Use results from fixed fraction fit, default is False')
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
    parser.add_option('', '--obs', dest='OneDOr2DObs', default=1, type=int, help="1 for 1D obs, 2 for 2D observable")
    parser.add_option('-y', '--year', dest='ERA',  type='string',default='2018',   help='year(s) of processing, e.g. 2016, 2017, 2018 or Full ')

    # store options and arguments as global variables
    global opt, args, combineOutputs, unblindString
    (opt, args) = parser.parse_args()

    combineOutputs = combineOutputs.format(year = opt.ERA)

    unblindString = ""
    if (opt.UNBLIND): unblindString = "_unblind"

# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs

# Don't move the root import before `sys.argv = grootargs`. Reference: https://root-forum.cern.ch/t/python-options-and-root-options/4641/3
from ROOT import *
from tdrStyle import *
setTDRStyle()

modelName = opt.UNFOLD
if opt.OBSNAME=="mass4l": physicalModel = 'v2'
else: physicalModel = 'v3'
asimovDataModel = opt.ASIMOV
asimovPhysicalModel = 'v2'
obsName = opt.OBSNAME
ListObsName = (''.join(obsName.split())).split('vs')

observableBins = read_bins(opt.OBSBINS)
logger.info("Parsed bins: {}".format(observableBins))
logger.info("Bin size = "+str(len(observableBins)))

nBins = len(observableBins) -1
if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
    nBins = len(observableBins)
logger.debug("nBins: = "+str(nBins))

ObsToStudy = "1D_Observables" if opt.OneDOr2DObs == 1 else "2D_Observables"

if (opt.ERA == '2016'): years = ['2016']
if (opt.ERA == '2017'): years = ['2017']
if (opt.ERA == '2018'): years = ['2018']
if (opt.ERA == 'Full'): years = ['2016','2017','2018']

def plotAsimov_sim(asimovDataModel, asimovPhysicalModel, modelName, physicalModel, obsName, fstate, observableBins, recobin, years):

    global nBins, ObsToStudy
    logger.debug("nBins: = "+str(nBins))
    channel = {"4mu":"1", "4e":"2", "2e2mu":"3", "4l":"2"} # 4l is dummy, won't be used

    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

    logger.debug (combineOutputs+"/"+asimovDataModel+'_all_'+obsName.replace(' ','_')+'_13TeV_Asimov_'+asimovPhysicalModel+unblindString+'.root')
    f_asimov = TFile(combineOutputs+'/'+asimovDataModel+'_all_'+obsName.replace(' ','_')+'_13TeV_Asimov_'+asimovPhysicalModel+unblindString+'.root','READ')

    if (not opt.UNBLIND):
        data = f_asimov.Get("toys/toy_asimov");
    #data.Print("v");
    w_asimov = f_asimov.Get("w")
    if (opt.UNBLIND):
        data = w.data("data_obs")
    w_asimov.loadSnapshot("clean")

    trueH_asimov = {}
    zjets_asimov = {}
    ggzz_asimov = {}
    fakeH_asimov = {}
    out_trueH_asimov = {}
    qqzz_asimov = {}
    n_trueH_asimov = {}
    n_trueH_asimov["4l"] = 0.0
    n_trueH_otherfid_asimov = {}
    n_trueH_otherfid_asimov["4l"] = 0.0
    n_zjets_asimov = {}
    n_zjets_asimov["4l"] = 0.0
    n_ggzz_asimov = {}
    n_ggzz_asimov["4l"] = 0.0
    n_fakeH_asimov = {}
    n_fakeH_asimov["4l"] = 0.0
    n_out_trueH_asimov = {}
    n_out_trueH_asimov["4l"] = 0.0
    n_qqzz_asimov = {}
    n_qqzz_asimov["4l"] = 0.0
    n_zz_asimov = {}
    n_zz_asimov["4l"] = 0.0

    if (fstate=='4l'): fStates = ['4mu','4e','2e2mu']
    else: fStates =  [fstate]

    for fState in fStates:
        trueH_asimov[fState] = 0.0
        zjets_asimov[fState] = 0.0
        ggzz_asimov[fState] = 0.0
        fakeH_asimov[fState] = 0.0
        out_trueH_asimov[fState] = 0.0
        qqzz_asimov[fState] = 0.0
        n_trueH_asimov[fState] = 0.0
        n_trueH_otherfid_asimov[fState] = 0.0
        n_zjets_asimov[fState] = 0.0
        n_ggzz_asimov[fState] = 0.0
        n_fakeH_asimov[fState] = 0.0
        n_out_trueH_asimov[fState] = 0.0
        n_qqzz_asimov[fState] = 0.0
        n_zz_asimov[fState] = 0.0

    logger.debug("Check-point")
    for year in years:
        for fState in fStates:
            WSTagger = "n_exp_final_bin"+obsName.replace(" ","_")+"_"+fState+"S_"+year+"_"+obsName.replace(" ","_")+"_"+fState+"S_"+str(recobin)+"_"+year
            logger.debug(WSTagger)
            for bin in range(nBins):
                trueH_asimov[fState+"Bin"+str(bin)] = w_asimov.function(WSTagger+"_proc_trueH"+fState+"Bin"+str(bin))
                logger.debug(WSTagger+"_proc_trueH"+fState+"Bin"+str(bin)+ " = " +str(trueH_asimov[fState+"Bin"+str(bin)].getVal()))
            zjets_asimov[fState] = w_asimov.function(WSTagger+"_proc_bkg_zjets")
            ggzz_asimov[fState] = w_asimov.function(WSTagger+"_proc_bkg_ggzz")
            fakeH_asimov[fState] = w_asimov.function(WSTagger+"_proc_fakeH")
            out_trueH_asimov[fState] = w_asimov.function(WSTagger+"_proc_out_trueH")
            qqzz_asimov[fState] = w_asimov.function(WSTagger+"_proc_bkg_qqzz")
            for bin in range(nBins):
                if (bin==recobin): n_trueH_asimov[fState] += trueH_asimov[fState+"Bin"+str(bin)].getVal()
                else: n_trueH_otherfid_asimov[fState] += trueH_asimov[fState+"Bin"+str(bin)].getVal()
            n_zjets_asimov[fState] += zjets_asimov[fState].getVal()
            n_ggzz_asimov[fState] += ggzz_asimov[fState].getVal()
            n_fakeH_asimov[fState] += fakeH_asimov[fState].getVal()
            n_out_trueH_asimov[fState] += out_trueH_asimov[fState].getVal()
            n_qqzz_asimov[fState] += qqzz_asimov[fState].getVal()
            n_zz_asimov[fState] += n_ggzz_asimov[fState]+n_qqzz_asimov[fState]

    for fState in fStates:
        n_trueH_asimov["4l"] += n_trueH_asimov[fState]
        n_trueH_otherfid_asimov["4l"] += n_trueH_otherfid_asimov[fState]
        n_zjets_asimov["4l"] += zjets_asimov[fState].getVal()
        n_ggzz_asimov["4l"] += ggzz_asimov[fState].getVal()
        n_fakeH_asimov["4l"] += fakeH_asimov[fState].getVal()
        n_out_trueH_asimov["4l"] += out_trueH_asimov[fState].getVal()
        n_qqzz_asimov["4l"] += qqzz_asimov[fState].getVal()
        n_zz_asimov["4l"] += n_ggzz_asimov[fState]+n_qqzz_asimov[fState]

    logger.debug(combineOutputs+"/"+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root')
    f_modelfit = TFile(combineOutputs+"/"+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root','READ')
    w_modelfit = f_modelfit.Get("w")
    sim = w_modelfit.pdf("model_s")
    #sim.Print("v")
    CMS_zz4l_mass = w_modelfit.var("CMS_zz4l_mass")
    w_modelfit.loadSnapshot("MultiDimFit")
    #pdfi.Print("v")

    trueH_modelfit = {}
    zjets_modelfit = {}
    ggzz_modelfit = {}
    fakeH_modelfit = {}
    out_trueH_modelfit = {}
    qqzz_modelfit = {}
    n_trueH_modelfit = {}
    n_trueH_modelfit["4l"] = 0.0
    n_trueH_otherfid_modelfit = {}
    n_trueH_otherfid_modelfit["4l"] = 0.0
    n_zjets_modelfit = {}
    n_zjets_modelfit["4l"] = 0.0
    n_ggzz_modelfit = {}
    n_ggzz_modelfit["4l"] = 0.0
    n_fakeH_modelfit = {}
    n_fakeH_modelfit["4l"] = 0.0
    n_out_trueH_modelfit = {}
    n_out_trueH_modelfit["4l"] = 0.0
    n_qqzz_modelfit = {}
    n_qqzz_modelfit["4l"] = 0.0
    n_zz_modelfit = {}
    n_zz_modelfit["4l"] = 0.0

    for fState in fStates:
        trueH_modelfit[fState] = 0.0
        zjets_modelfit[fState] = 0.0
        ggzz_modelfit[fState] = 0.0
        fakeH_modelfit[fState] = 0.0
        out_trueH_modelfit[fState] = 0.0
        qqzz_modelfit[fState] = 0.0
        n_trueH_modelfit[fState] = 0.0
        n_trueH_otherfid_modelfit[fState] = 0.0
        n_zjets_modelfit[fState] = 0.0
        n_ggzz_modelfit[fState] = 0.0
        n_fakeH_modelfit[fState] = 0.0
        n_out_trueH_modelfit[fState] = 0.0
        n_qqzz_modelfit[fState] = 0.0
        n_zz_modelfit[fState] = 0.0

    for year in years:
        for fState in fStates:
            WSTagger = "n_exp_final_bin"+obsName.replace(" ","_")+"_"+fState+"S_"+year+"_"+obsName.replace(" ","_")+"_"+fState+"S_"+str(recobin)+"_"+year
            for bin in range(nBins):
                trueH_modelfit[fState+"Bin"+str(bin)] = w_modelfit.function(WSTagger+"_proc_trueH"+fState+"Bin"+str(bin))
            zjets_modelfit[fState] = w_modelfit.function(WSTagger+"_proc_bkg_zjets")
            ggzz_modelfit[fState] = w_modelfit.function(WSTagger+"_proc_bkg_ggzz")
            fakeH_modelfit[fState] = w_modelfit.function(WSTagger+"_proc_fakeH")
            out_trueH_modelfit[fState] = w_modelfit.function(WSTagger+"_proc_out_trueH")
            qqzz_modelfit[fState] = w_modelfit.function(WSTagger+"_proc_bkg_qqzz")
            for bin in range(nBins):
                if (bin==recobin): n_trueH_modelfit[fState] += trueH_modelfit[fState+"Bin"+str(bin)].getVal()
                else: n_trueH_otherfid_modelfit[fState] += trueH_modelfit[fState+"Bin"+str(bin)].getVal()
            n_zjets_modelfit[fState] += zjets_modelfit[fState].getVal()
            n_ggzz_modelfit[fState] += ggzz_modelfit[fState].getVal()
            n_fakeH_modelfit[fState] += fakeH_modelfit[fState].getVal()
            n_out_trueH_modelfit[fState] += out_trueH_modelfit[fState].getVal()
            n_qqzz_modelfit[fState] += qqzz_modelfit[fState].getVal()
            n_zz_modelfit[fState] += n_ggzz_modelfit[fState]+n_qqzz_modelfit[fState]

    for fState in fStates:
        n_trueH_modelfit["4l"] += n_trueH_modelfit[fState]
        n_trueH_otherfid_modelfit["4l"] += n_trueH_otherfid_modelfit[fState]
        n_zjets_modelfit["4l"] += zjets_modelfit[fState].getVal()
        n_ggzz_modelfit["4l"] += ggzz_modelfit[fState].getVal()
        n_fakeH_modelfit["4l"] += fakeH_modelfit[fState].getVal()
        n_out_trueH_modelfit["4l"] += out_trueH_modelfit[fState].getVal()
        n_qqzz_modelfit["4l"] += qqzz_modelfit[fState].getVal()
        n_zz_modelfit["4l"] += n_ggzz_modelfit[fState]+n_qqzz_modelfit[fState]

    CMS_channel = w.cat("CMS_channel")
    if (obsName=="mass4l"):
        mass = w.var("CMS_zz4l_mass").frame(RooFit.Bins(15))
    else:
        mass = w.var("CMS_zz4l_mass").frame(RooFit.Bins(15))


    if (fstate=="4l"):

        datacut = ''
        for year in years:
            for fState in fStates:
                logger.debug(obsName+"_"+fState+"_bin"+str(recobin)+"_"+year)
                datacut += "CMS_channel==CMS_channel::"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+" || "
        datacut = datacut.rstrip(" || ")
        data = data.reduce(RooFit.Cut(datacut))
        data.plotOn(mass)
        sim.plotOn(mass,RooFit.LineColor(kRed), RooFit.ProjWData(data,True))

        comp_otherfid = ''
        for bin in range(nBins):
            if bin==recobin: continue
            for year in years:
                for fState in fStates:
                    comp_otherfid += "shapeSig_trueH"+fState+"Bin"+str(bin)+"_"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+","
        comp_otherfid = comp_otherfid.rstrip(',')

        comp_out = ''
        comp_fake = ''
        comp_zz = ''
        comp_zx = ''
        for year in years:
            for fState in fStates:
                comp_out += "shapeBkg_out_trueH_"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+","
                comp_fake += "shapeBkg_fakeH_"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+","
                comp_zz += "shapeBkg_bkg_ggzz_"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+",shapeBkg_bkg_qqzz_"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+","
                comp_zx += "shapeBkg_bkg_zjets_"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+","
        comp_out = comp_out.rstrip(',')
        comp_fake = comp_fake.rstrip(',')
        comp_zz = comp_zz.rstrip(',')
        comp_zx = comp_zx.rstrip(',')
        sim.plotOn(mass, RooFit.LineColor(kGray+2), RooFit.LineStyle(2), RooFit.Components(comp_zx+","+comp_zz+","+comp_fake+","+comp_otherfid+","+comp_out), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kRed), RooFit.LineStyle(2), RooFit.Components(comp_zx+","+comp_zz+","+comp_fake+","+comp_otherfid), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kOrange), RooFit.Components(comp_zx+","+comp_zz+","+comp_fake), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kAzure-3), RooFit.Components(comp_zx+","+comp_zz), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kGreen+3), RooFit.Components(comp_zx), RooFit.ProjWData(data,True))
        data.plotOn(mass)
    else:
        datacut = ''
        for year in years:
            sbin_ = obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+"_"+fstate+"S_"+str(recobin)+"_"+year
            logger.debug(sbin_)
            datacut += "CMS_channel==CMS_channel::" + sbin_ + " || "
        datacut = datacut.rstrip(" || ")
        data = data.reduce(RooFit.Cut(datacut))
        data.plotOn(mass)
        sim.plotOn(mass,RooFit.Components("*"+fstate+"*"),RooFit.LineColor(kRed), RooFit.ProjWData(data,True))

        comp_otherfid = ''
        for bin in range(nBins):
            if bin==recobin: continue
            for year in years:
                comp_otherfid += "shapeSig_trueH"+fstate+"Bin"+str(bin)+"_"+obsName+"_"+fstate+"_bin"+str(recobin)+"_"+year+","
        comp_otherfid = comp_otherfid.rstrip(',')

        comp_out = ''
        comp_fake = ''
        comp_zz = ''
        comp_zx = ''
        for year in years:
            comp_out += "shapeBkg_out_trueH_"+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+'_'+fstate+'S_'+str(recobin)+"_"+year+","
            comp_fake += "shapeBkg_fakeH_"+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+'_'+fstate+'S_'+str(recobin)+"_"+year+","
            comp_zz += "shapeBkg_bkg_ggzz_"+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+'_'+fstate+'S_'+str(recobin)+"_"+year+",shapeBkg_bkg_qqzz_"+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+'_'+fstate+'S_'+str(recobin)+"_"+year+","
            comp_zx += "shapeBkg_bkg_zjets_"+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+'_'+fstate+'S_'+str(recobin)+"_"+year+","
        comp_out = comp_out.rstrip(',')
        comp_fake = comp_fake.rstrip(',')
        comp_zz = comp_zz.rstrip(',')
        comp_zx = comp_zx.rstrip(',')
        sim.plotOn(mass, RooFit.LineColor(kGray+2), RooFit.LineStyle(2), RooFit.Components(comp_zx+","+comp_zz+","+comp_fake+","+comp_otherfid+","+comp_out), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kRed), RooFit.LineStyle(2), RooFit.Components(comp_zx+","+comp_zz+","+comp_fake+","+comp_otherfid), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kOrange), RooFit.Components(comp_zx+","+comp_zz+","+comp_fake), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kAzure-3), RooFit.Components(comp_zx+","+comp_zz), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kGreen+3), RooFit.Components(comp_zx), RooFit.ProjWData(data,True))
        data.plotOn(mass)

    gStyle.SetOptStat(0)

    c = TCanvas("c","c",1000,800)
    c.cd()

    dummy = TH1D("","",1,105.0,140.0)
    dummy.SetBinContent(1,2)
    dummy.SetFillColor(0)
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.SetMarkerColor(0)
    if (obsName=="mass4l"):
        dummy.GetYaxis().SetTitle("Events / (1 GeV)")
    else:
        dummy.GetYaxis().SetTitle("Events / (2.33 GeV)")

    dummy.GetXaxis().SetTitle("m_{"+fstate.replace("mu","#mu")+"} [GeV]")
    if (opt.UNBLIND):
        dummy.SetMaximum(max(3.0*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))
        if (obsName=="massZ2" and recobin==0): dummy.SetMaximum(max(6.0*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))
        if (obsName=="mass4l" and recobin==0):
            if (fstate=="4l"): dummy.SetMaximum(max(0.4*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))
            else: dummy.SetMaximum(max(0.5*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))
    else:
        if (fstate=="4l"):
            dummy.SetMaximum(max(0.5*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))
        else:
            dummy.SetMaximum(max(1.5*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))

        if (obsName=="massZ2" and recobin==0): dummy.SetMaximum(max(6.0*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]),3.5))

    dummy.SetMinimum(0.0)
    dummy.Draw()

    dummy_data = TH1D()
    dummy_data.SetMarkerColor(kBlack)
    dummy_data.SetMarkerStyle(20)
    dummy_fid = TH1D()
    dummy_fid.SetLineColor(kRed)
    dummy_fid.SetLineWidth(2)
    dummy_other = TH1D()
    dummy_other.SetLineColor(kRed)
    dummy_other.SetLineWidth(2)
    dummy_other.SetLineStyle(2)
    dummy_out = TH1D()
    dummy_out.SetLineColor(kGray+2)
    dummy_out.SetLineWidth(2)
    dummy_out.SetLineStyle(2)
    dummy_fake = TH1D()
    dummy_fake.SetLineColor(kOrange)
    dummy_fake.SetLineWidth(2)
    dummy_zz = TH1D()
    dummy_zz.SetLineColor(kAzure-3)
    dummy_zz.SetLineWidth(2)
    dummy_zx = TH1D()
    dummy_zx.SetLineColor(kGreen+3)
    dummy_zx.SetLineWidth(2)


    legend = TLegend(.20,.41,.53,.89)
    if (not opt.UNBLIND):
        legend.AddEntry(dummy_data,"Asimov Data (SM m(H) = "+opt.ASIMOVMASS+" GeV)","ep")
    else:
        legend.AddEntry(dummy_data,"Data","ep")
    legend.AddEntry(dummy_fid,"N_{fid.}^{fit} = %.2f (exp. = %.2f)"%(n_trueH_modelfit[fstate],n_trueH_asimov[fstate]), "l")
    legend.AddEntry(dummy_other,"N_{other fid.}^{fit} = %.2f (exp = %.2f)"%(n_trueH_otherfid_modelfit[fstate],n_trueH_otherfid_asimov[fstate]), "l")
    legend.AddEntry(dummy_out, "N_{out}^{fit} = %.2f (exp. = %.2f)"%(n_out_trueH_modelfit[fstate],n_out_trueH_asimov[fstate]), "l")
    legend.AddEntry(dummy_fake, "N_{wrong}^{fit} = %.2f (exp. = %.2f)"%(n_fakeH_modelfit[fstate],n_fakeH_asimov[fstate]), "l")
    legend.AddEntry(dummy_zz, "N_{ZZ}^{fit} = %.2f (exp. = %.2f)"%(n_zz_modelfit[fstate],n_zz_asimov[fstate]), "l")
    legend.AddEntry(dummy_zx, "N_{Z+X}^{fit} = %.2f (exp. = %.2f)"%(n_zjets_modelfit[fstate],n_zjets_asimov[fstate]), "l")

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw()

    mass.Draw("same")

    # Get label name & Unit from YAML file.
    with open(opt.inYAMLFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
            print('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                    Please check your YAML file format!!!'''.format(InputYAMLFile))

        label = cfg['Observables'][ObsToStudy][obsName]['label']
        unit = cfg['Observables'][ObsToStudy][obsName]['unit']
        # border_msg("Label name: {}, Unit: {}".format(label, unit))

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    if (not opt.LUMISCALE=="1.0"):
        if (opt.ERA=='2016') : lumi = round(35.9*float(opt.LUMISCALE),1)
        elif (opt.ERA=='2017') : lumi = round(41.7*float(opt.LUMISCALE),1)
        else  : lumi = round(58.5*float(opt.LUMISCALE),1)
        latex2.DrawLatex(0.94, 0.94,str(lumi)+" fb^{-1} (13 TeV)")
    else:
        if (opt.ERA=='2016') : latex2.DrawLatex(0.94, 0.94, str(Lumi_2016)+" fb^{-1} (13 TeV)")
        elif (opt.ERA=='2017') : latex2.DrawLatex(0.94, 0.94, str(Lumi_2017)+" fb^{-1} (13 TeV)")
        elif (opt.ERA=='2018') : latex2.DrawLatex(0.94, 0.94, str(Lumi_2018)+" fb^{-1} (13 TeV)")
        else : latex2.DrawLatex(0.94, 0.94, str(Lumi_Run2) + " fb^{-1} (13 TeV)")

    latex2.SetTextSize(0.8*c.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.19, 0.95, "CMS")
    latex2.SetTextSize(0.6*c.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.30, 0.95, "Preliminary")
    latex2.SetTextFont(42)
    latex2.SetTextSize(0.45*c.GetTopMargin())
    if (ObsToStudy == "1D_Observables"):
        latex2.DrawLatex(0.65,0.85, observableBins[recobin]+" "+unit+" < "+label+" < "+observableBins[recobin+1]+" "+unit)
    else:
        latex2.DrawLatex(0.65,0.85, observableBins[recobin][0][0]+" "+unit[0]+" < "+label[0]+" < "+observableBins[recobin][0][1]+" "+unit[0])
        latex2.DrawLatex(0.65,0.75, observableBins[recobin][1][0]+" "+unit[1]+" < "+label[1]+" < "+observableBins[recobin][1][1]+" "+unit[1])
    # Create output directory if it does not exits
    OutputPath = AsimovPlots.format(year = year, obsName = obsName.replace(' ','_'))
    GetDirectory(OutputPath)

    if (not opt.UNBLIND):
        c.SaveAs(OutputPath+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+"_recobin"+str(recobin)+".pdf")
        c.SaveAs(OutputPath+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+"_recobin"+str(recobin)+".png")
    else:
        c.SaveAs(OutputPath+"/data_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+"_recobin"+str(recobin)+".pdf")
        c.SaveAs(OutputPath+"/data_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+"_recobin"+str(recobin)+".png")


fStates = ["4e","4mu","2e2mu"]
for fState in fStates:
    for recobin in range(nBins):
        plotAsimov_sim(asimovDataModel, asimovPhysicalModel, modelName, physicalModel, obsName, fState, observableBins, recobin, years)
