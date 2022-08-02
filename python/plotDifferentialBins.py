import optparse
import os
import sys
from array import array
from decimal import *
from math import *
import yaml

# INFO: Following items are imported from either python directory or Inputs
from sample_shortnames import *
from Input_Info import *
from read_bins import read_bins
from Utils import logger, border_msg, GetDirectory

grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)

### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',    dest='SOURCEDIR',  type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--inYAMLFile', dest='inYAMLFile', type='string', default="Inputs/observables_list.yml", help='Input YAML file having observable names and bin information')
    parser.add_option('',   '--asimovModel',dest='ASIMOV',type='string',default='ggH_powheg15_JHUgen_125', help='Name of the asimov data mode')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.38', help='Asimov MAss')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observable, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    parser.add_option('-y', '--year', dest="ERA", type = 'string', default = '2018', help='Era to analyze, e.g. 2016, 2017, 2018 or Full')
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)

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


asimovDataModel = opt.ASIMOV
asimovPhysicalModel = 'v2'
obsName = opt.OBSNAME
# observableBins = opt.OBSBINS.split('|')
# observableBins.pop()
# observableBins.pop(0)
# print float(observableBins[len(observableBins)-1])
# if float(observableBins[len(observableBins)-1])>200.0:
#     observableBins[len(observableBins)-1]='200.0'

if (opt.ERA == '2016'): years = ['2016']
if (opt.ERA == '2017'): years = ['2017']
if (opt.ERA == '2018'): years = ['2018']
if (opt.ERA == 'allYear'): years = ['2016','2017','2018']

ListObsName = (''.join(obsName.split())).split('vs')

observableBins = read_bins(opt.OBSBINS)
logger.info("Parsed bins: {}".format(observableBins))
logger.info("Bin size = "+str(len(observableBins)))

nBins = len(observableBins) -1
if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
    nBins = len(observableBins)
logger.debug("nBins: = "+str(nBins))


# if len(ListObsName) == 1:    # INFO: for 2D this list size == 1
    # print("{}".format(float(observableBins[nBins])))
    # if float(observableBins[nBins])>200.0:
        # observableBins[nBins]='200.0'


def plotDifferentialBins(asimovDataModel, asimovPhysicalModel, obsName, fstate, observableBins, years):

    global nBins

    # FIXME: we could relate channel and fstate???
    # FIXME: Channels and fstates are given at many places.
    # FIXME: Is it possible to define them at one place and grab it where its necessary?
    channel = {"4mu":"1", "4e":"2", "2e2mu":"3", "4l":"2"} # 4l is dummy, won't be used

    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

    # FIXME: Improve the directory naming/pointer of hardcoded directory
    inFile = combineOutputs+"/"+asimovDataModel+'_all_'+obsName.replace(' ','_')+'_13TeV_Asimov_'+asimovPhysicalModel+unblindString+'.root'
    f_asimov = TFile(inFile, 'READ')
    logger.debug("Asimov file is :  {}".format(inFile))

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
    n_trueH_otherfid_asimov = {}
    n_zjets_asimov = {}
    n_ggzz_asimov = {}
    n_fakeH_asimov = {}
    n_out_trueH_asimov = {}
    n_qqzz_asimov = {}
    n_zz_asimov = {}
    logger.debug("Years: {}".format(years))
    for year in years:
        for recobin in range(nBins):
            n_trueH_asimov["4lrecobin"+str(recobin)+year] = 0.0
            n_trueH_otherfid_asimov["4lrecobin"+str(recobin)+year] = 0.0
            n_zjets_asimov["4lrecobin"+str(recobin)+year] = 0.0
            n_ggzz_asimov["4lrecobin"+str(recobin)+year] = 0.0
            n_fakeH_asimov["4lrecobin"+str(recobin)+year] = 0.0
            n_out_trueH_asimov["4lrecobin"+str(recobin)+year] = 0.0
            n_qqzz_asimov["4lrecobin"+str(recobin)+year] = 0.0
	    n_zz_asimov["4lrecobin"+str(recobin)+year] = 0.0
    fStates = ['4mu','4e','2e2mu']
    for year in years:
        for fState in fStates:
            for recobin in range(nBins):
                if (len(years) > 1): AdditionalAllYearText = obsName.replace(' ','_')+"_4e4mu2e2mu_"+year+"_"
                else: AdditionalAllYearText = ""
                TaggerFromWS = "n_exp_final_bin"+AdditionalAllYearText+obsName.replace(' ','_')+"_"+fState+"S_"+year+"_"+obsName.replace(' ','_')+"_"+fState+"S_"+str(recobin)+"_"+year
                for bin in range(nBins):
                    trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)+year] = w_asimov.function(TaggerFromWS+"_proc_trueH"+fState+"Bin"+str(bin))
                zjets_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function(TaggerFromWS+"_proc_bkg_zjets")
                ggzz_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function(TaggerFromWS+"_proc_bkg_ggzz")
                fakeH_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function(TaggerFromWS+"_proc_fakeH")
                out_trueH_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function(TaggerFromWS+"_proc_out_trueH")
                qqzz_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function(TaggerFromWS+"_proc_bkg_qqzz")
                n_trueH_otherfid_asimov[fState+"recobin"+str(recobin)+year] = 0.0
                for bin in range(nBins):
                    if (bin==recobin):
                        n_trueH_asimov[fState+"recobin"+str(recobin)+year] = trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)+year].getVal()
                    else:
                        n_trueH_otherfid_asimov[fState+"recobin"+str(recobin)+year] += trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)+year].getVal()
                n_zjets_asimov[fState+"recobin"+str(recobin)+year] = zjets_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_ggzz_asimov[fState+"recobin"+str(recobin)+year] = ggzz_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_fakeH_asimov[fState+"recobin"+str(recobin)+year] = fakeH_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_out_trueH_asimov[fState+"recobin"+str(recobin)+year] = out_trueH_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_qqzz_asimov[fState+"recobin"+str(recobin)+year] = qqzz_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_zz_asimov[fState+"recobin"+str(recobin)+year] = n_ggzz_asimov[fState+"recobin"+str(recobin)+year]+n_qqzz_asimov[fState+"recobin"+str(recobin)+year]
                n_trueH_asimov["4lrecobin"+str(recobin)+year] += n_trueH_asimov[fState+"recobin"+str(recobin)+year]
                n_trueH_otherfid_asimov["4lrecobin"+str(recobin)+year] += n_trueH_otherfid_asimov[fState+"recobin"+str(recobin)+year]
                n_zjets_asimov["4lrecobin"+str(recobin)+year] += zjets_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_ggzz_asimov["4lrecobin"+str(recobin)+year] += ggzz_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_fakeH_asimov["4lrecobin"+str(recobin)+year] += fakeH_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_out_trueH_asimov["4lrecobin"+str(recobin)+year] += out_trueH_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_qqzz_asimov["4lrecobin"+str(recobin)+year] += qqzz_asimov[fState+"recobin"+str(recobin)+year].getVal()
                n_zz_asimov["4lrecobin"+str(recobin)+year] += n_ggzz_asimov[fState+"recobin"+str(recobin)+year]+n_qqzz_asimov[fState+"recobin"+str(recobin)+year]


    CMS_channel = w.cat("CMS_channel")
    mass = w.var("CMS_zz4l_mass").frame(RooFit.Bins(1))
    logger.debug(type(mass))

    databin = {}
    logger.debug("databin: {}".format(databin))
    if (fstate=="4l"):
        for year in years:
            for recobin in range(nBins):
                datacut = ''
                for fState in fStates:
                    if (len(years) > 1): AdditionalAllYearText = obsName.replace(' ','_')+"_4e4mu2e2mu_"+year+"_"
                    else: AdditionalAllYearText = ""
                    sbin = AdditionalAllYearText+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+"_"+fstate+"S_"+str(recobin)+"_"+year
                    datacut += "CMS_channel==CMS_channel::"+sbin+" || "
                datacut = datacut.rstrip(" || ")
                logger.debug("datacut is :    {}".format(datacut))
                databin[str(recobin)+year] = data.reduce(RooFit.Cut(datacut))
        logger.debug("databin: {}".format(databin))
    else:
        for year in years:
            for recobin in range(nBins):
                if (len(years) > 1): AdditionalAllYearText = obsName.replace(' ','_')+"_4e4mu2e2mu_"+year+"_"
                else: AdditionalAllYearText = ""
                sbin = AdditionalAllYearText+obsName.replace(' ','_')+"_"+fstate+"S_"+year+"_"+obsName.replace(' ','_')+"_"+fstate+"S_"+str(recobin)+"_"+year
                databin[str(recobin)+year] = data.reduce(RooFit.Cut("CMS_channel==CMS_channel::"+sbin))
                logger.debug("databin: {}".format(databin))
        logger.debug("databin: {}".format(databin))

    if (obsName.startswith('njets')):
        h_data = TH1D("h_data","h_data",nBins,0,nBins)
        h_sig = TH1D("h_sig","h_xig",nBins,0,nBins)
        h_zz = TH1D("h_zz","h_zz",nBins,0,nBins)
        h_zx = TH1D("h_zx","h_zx",nBins,0,nBins)
    else:
        CustomBinInfo = [float(observableBins[i]) for i in range(nBins+1)]
        # CustomBinInfo[0] = 0.0
        if str(CustomBinInfo[-1]) == "inf": # if the value is "inf" set it to large number
            CustomBinInfo[-1] = 10000
        logger.debug("nBins: {}, CustomBinInfo: {}".format(nBins, CustomBinInfo))
        h_data = TH1D("h_data","h_data",nBins,array('d',CustomBinInfo))
        h_sig = TH1D("h_sig","h_xig",nBins,array('d',CustomBinInfo))
        h_zz = TH1D("h_zz","h_zz",nBins,array('d',CustomBinInfo))
        h_zx = TH1D("h_zx","h_zx",nBins,array('d',CustomBinInfo))
        logger.debug("CustomBinInfo: {}".format(CustomBinInfo))

    nH={};
    nZZ={};
    nZX={};
    nData={}
    for recobin in range(nBins):
        nH[fstate+"recobin"+str(recobin)] = 0.0
        nZZ[fstate+"recobin"+str(recobin)] = 0.0
        nZX[fstate+"recobin"+str(recobin)] = 0.0
        nData[fstate+"recobin"+str(recobin)] = 0.0


    for recobin in range(nBins):
        for year in years:
            logger.debug(fstate+"recobin"+str(recobin)+ "year"+ str(year))
            nH[fstate+"recobin"+str(recobin)]+=n_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_trueH_otherfid_asimov[fstate+"recobin"+str(recobin)+year]+n_out_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_fakeH_asimov[fstate+"recobin"+str(recobin)+year]
            logger.debug('H:'+str(n_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_trueH_otherfid_asimov[fstate+"recobin"+str(recobin)+year]+n_out_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_fakeH_asimov[fstate+"recobin"+str(recobin)+year]))

            nZZ[fstate+"recobin"+str(recobin)]+=n_zz_asimov[fstate+"recobin"+str(recobin)+year]
            logger.debug('ZZ:'+str(n_zz_asimov[fstate+"recobin"+str(recobin)+year]))

            nZX[fstate+"recobin"+str(recobin)]+=n_zjets_asimov[fstate+"recobin"+str(recobin)+year]
            logger.debug('Z+X:'+str(n_zjets_asimov[fstate+"recobin"+str(recobin)+year]))

            nData[fstate+"recobin"+str(recobin)]+=databin[str(recobin)+year].sumEntries()
            logger.debug('Data:'+str(databin[str(recobin)+year].sumEntries()))

        logger.debug("nH[fstate+recobin+str(recobin)]: {}".format(nH[fstate+"recobin"+str(recobin)]))
        h_sig.SetBinContent(recobin+1,nH[fstate+"recobin"+str(recobin)])
        h_zz.SetBinContent(recobin+1,nZZ[fstate+"recobin"+str(recobin)])
        h_zx.SetBinContent(recobin+1,nZX[fstate+"recobin"+str(recobin)])
        h_data.SetBinContent(recobin+1,nData[fstate+"recobin"+str(recobin)])

    h_sig.SetLineColor(kRed)
    h_sig.SetLineWidth(2)

    h_zz.SetLineColor(kBlue)
    h_zz.SetFillColor(kAzure+6)
    h_zz.SetLineWidth(2)

    h_zx.SetLineColor(kGreen+4)
    h_zx.SetFillColor(kGreen-5)
    h_zx.SetLineWidth(2)

    h_data.SetBinErrorOption(ROOT.TH1.kPoisson)
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.2)

    h_stack = THStack()
    h_stack.Add(h_zx)
    h_stack.Add(h_zz)
    h_stack.Add(h_sig)

    gStyle.SetOptStat(0)

    c = TCanvas("c","c",1000,800)
    c.cd()

    # Get label name & Unit from YAML file.
    with open(opt.inYAMLFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        if ( ("Observables" not in cfg) or ("1D_Observables" not in cfg['Observables']) ) :
            print('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                    Please check your YAML file format!!!'''.format(opt.inYAMLFile))

        label = cfg['Observables']['1D_Observables'][obsName]['label']
        unit = cfg['Observables']['1D_Observables'][obsName]['unit']
        # border_msg("Label name: {}, Unit: {}".format(label, unit))


    if str(observableBins[nBins]) == "inf":
        observableBins[nBins] = 10000
    logger.debug("boundary and bins: nBins: {}, bin start val: {}, last bin val: {}".format(nBins, float(observableBins[0]),float(observableBins[nBins])))
    if (obsName.startswith("njets")):
        dummy = TH1D("","",nBins,0,nBins)
    else:
        dummy = TH1D("","",nBins,float(observableBins[0]),float(observableBins[nBins]))
    dummy.SetBinContent(1,1)
    dummy.SetFillColor(0)
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.SetMarkerColor(0)
    dummy.GetYaxis().SetTitle("Events")
    if (obsName.startswith('njets')):
        dummy.GetXaxis().SetTitle(label)
        dummy.GetXaxis().SetBinLabel(1,'0')
        dummy.GetXaxis().SetBinLabel(2,'1')
        dummy.GetXaxis().SetBinLabel(3,'2')
        dummy.GetXaxis().SetBinLabel(4,'#geq 3')
    elif (unit == ""):
        dummy.GetXaxis().SetTitle(label)
    else:
        dummy.GetXaxis().SetTitle(label+" ["+unit+"]")
    dummy.SetMaximum(2.0*h_data.GetMaximum())
    if (obsName=="massZ1"): dummy.SetMaximum(2.5*h_data.GetMaximum())
    dummy.SetMinimum(0.0)
    dummy.Draw()

    h_stack.Draw("histsame")
    h_data.Draw("ex0same")
    ROOT.gPad.RedrawAxis()

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    if (not opt.LUMISCALE=="1.0"):
        if (opt.ERA=='2016') : lumi = round(Lumi_2016*float(opt.LUMISCALE),1)
        elif (opt.ERA=='2017') : lumi = round(Lumi_2017*float(opt.LUMISCALE),1)
        else  : lumi = round(58.5*float(opt.LUMISCALE),1)
        latex2.DrawLatex(0.94, 0.94,str(lumi)+" fb^{-1} (13 TeV)")
    else:
        if (opt.ERA=='2016') : latex2.DrawLatex(0.94, 0.94, str(Lumi_2016) + " fb^{-1} (13 TeV)")
        elif (opt.ERA=='2017') : latex2.DrawLatex(0.94, 0.94, str(Lumi_2017) + " fb^{-1} (13 TeV)")
        elif (opt.ERA=='2018') : latex2.DrawLatex(0.94, 0.94, str(Lumi_2018) + " fb^{-1} (13 TeV)")
        else : latex2.DrawLatex(0.94, 0.94, str(Lumi_Run2) + " fb^{-1} (13 TeV)")

    latex2.SetTextSize(0.9*c.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.25, 0.85, "CMS")
    latex2.SetTextSize(0.7*c.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.23, 0.8, "Preliminary")
    latex2.SetTextFont(42)
    latex2.SetTextSize(0.45*c.GetTopMargin())
    latex2.DrawLatex(0.19,0.75,str(INPUT_m4l_low)+" GeV < m("+fstate.replace('mu','#mu')+") < "+str(INPUT_m4l_high)+" GeV")
    legend = TLegend(.6,.70,.9,.90)
    if (not opt.UNBLIND):
        legend.AddEntry(h_data,"Asimov Data (SM)","ep")
    else:
        legend.AddEntry(h_data,"Data","ep")
    legend.AddEntry(h_sig,"m(H) = "+opt.ASIMOVMASS+" GeV","f")
    legend.AddEntry(h_zz,"ZZ background","f")
    legend.AddEntry(h_zx,"Z+X background","f")
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw()

    # Create output directory if it does not exits
    OutputPath = DifferentialBins.format(year = year, obsName = obsName.replace(' ','_'))
    logger.debug("OutputPath: {}".format(OutputPath))
    logger.debug("asimovDataModel: {}".format(asimovDataModel))
    logger.debug("asimovPhysicalModel: {}".format(asimovPhysicalModel))
    logger.debug(OutputPath+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+".pdf")
    GetDirectory(OutputPath)
    if (not opt.UNBLIND):
        c.SaveAs(OutputPath+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+".pdf")
        c.SaveAs(OutputPath+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+".png")
    else:
        c.SaveAs(OutputPath+"/data_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+".pdf")
        c.SaveAs(OutputPath+"/data_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName.replace(' ','_')+'_'+fstate+".png")


# fStates = ["4e","4mu","2e2mu","4l"]
fStates = ["4e","4mu","2e2mu"]
logger.debug("years are: {}".format(years))
for fState in fStates:
    plotDifferentialBins(asimovDataModel, asimovPhysicalModel, obsName, fState, observableBins, years)
