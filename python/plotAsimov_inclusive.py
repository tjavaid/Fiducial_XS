import optparse
import os
import sys
from decimal import *
from math import *


# INFO: Following items are imported from either python directory or Inputs
from sample_shortnames import *
from Input_Info import *


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
    parser.add_option('',   '--asimovModel',dest='ASIMOV',type='string',default='ggH_powheg15_JHUgen_125', help='Name of the asimov data mode')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.0', help='Asimov Mass')
    parser.add_option('',   '--unfoldModel',dest='UNFOLD',type='string',default='ggH_powheg15_JHUgen_125', help='Name of the unfolding model')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--fixFrac', action='store_true', dest='FIXFRAC', default=False, help='Use results from fixed fraction fit, default is False')
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs

# Don't move the root import before `sys.argv = grootargs`. Reference: https://root-forum.cern.ch/t/python-options-and-root-options/4641/3
from ROOT import *
from tdrStyle import *
setTDRStyle()

if (not os.path.exists("plots")):
    os.system("mkdir plots")

modelName = opt.UNFOLD
physicalModel = 'v2'
asimovDataModel = opt.ASIMOV
asimovPhysicalModel = 'v2'
obsName = opt.OBSNAME
observableBins = opt.OBSBINS.split('|')
observableBins.pop()
observableBins.pop(0)

def plotAsimov(asimovDataModel, asimovPhysicalModel, modelName, physicalModel, obsName, fstate, recobin):

    channel = {"4mu":"1", "4e":"2", "2e2mu":"3", "4l":"2"}

    # Load some libraries
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc6_amd64_gcc491/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

    print('[INFO] Filename: {}'.format(asimovDataModel+'_all_'+obsName+'_13TeV_Asimov_'+asimovPhysicalModel+'.root','READ'))
    f_asimov = TFile(combineOutputs+'/'+asimovDataModel+'_all_'+obsName+'_13TeV_Asimov_'+asimovPhysicalModel+'.root','READ')
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


    fStates = ['4mu','4e','2e2mu']
    for fState in fStates:
        trueH_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_trueH"+fState+"Bin0")
        zjets_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_zjets")
        ggzz_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_ggzz")
        fakeH_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_fakeH")
        out_trueH_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_out_trueH")
        qqzz_asimov[fState] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_qqzz")
        n_trueH_asimov[fState] = trueH_asimov[fState].getVal()
        n_zjets_asimov[fState] = zjets_asimov[fState].getVal()
        n_ggzz_asimov[fState] = ggzz_asimov[fState].getVal()
        n_fakeH_asimov[fState] = fakeH_asimov[fState].getVal()
        n_out_trueH_asimov[fState] = out_trueH_asimov[fState].getVal()
        n_qqzz_asimov[fState] = qqzz_asimov[fState].getVal()
        n_zz_asimov[fState] = n_ggzz_asimov[fState]+n_qqzz_asimov[fState]
        n_trueH_asimov["4l"] += trueH_asimov[fState].getVal()
        n_zjets_asimov["4l"] += zjets_asimov[fState].getVal()
        n_ggzz_asimov["4l"] += ggzz_asimov[fState].getVal()
        n_fakeH_asimov["4l"] += fakeH_asimov[fState].getVal()
        n_out_trueH_asimov["4l"] += out_trueH_asimov[fState].getVal()
        n_qqzz_asimov["4l"] += qqzz_asimov[fState].getVal()
        n_zz_asimov["4l"] += n_ggzz_asimov[fState]+n_qqzz_asimov[fState]

    f_modelfit = TFile(combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root','READ')
    w_modelfit = f_modelfit.Get("w")
    sim = w_modelfit.pdf("model_s")
    #sim.Print("v")
    if (fstate=="4l"): pdfi = sim.getPdf("ch2")
    else: pdfi = sim.getPdf("ch"+channel[fstate])
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
        trueH_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_trueH"+fState+"Bin0")
        zjets_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_zjets")
        ggzz_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_ggzz")
        fakeH_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_fakeH")
        out_trueH_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_out_trueH")
        qqzz_modelfit[fState] = w_modelfit.function("n_exp_final_binch"+channel[fState]+"_proc_bkg_qqzz")
        n_trueH_modelfit[fState] = trueH_modelfit[fState].getVal()
        n_zjets_modelfit[fState] = zjets_modelfit[fState].getVal()
        n_ggzz_modelfit[fState] = ggzz_modelfit[fState].getVal()
        n_fakeH_modelfit[fState] = fakeH_modelfit[fState].getVal()
        n_out_trueH_modelfit[fState] = out_trueH_modelfit[fState].getVal()
        n_qqzz_modelfit[fState] = qqzz_modelfit[fState].getVal()
        n_zz_modelfit[fState] = n_ggzz_modelfit[fState]+n_qqzz_modelfit[fState]
        n_trueH_modelfit["4l"] += trueH_modelfit[fState].getVal()
        n_zjets_modelfit["4l"] += zjets_modelfit[fState].getVal()
        n_ggzz_modelfit["4l"] += ggzz_modelfit[fState].getVal()
        n_fakeH_modelfit["4l"] += fakeH_modelfit[fState].getVal()
        n_out_trueH_modelfit["4l"] += out_trueH_modelfit[fState].getVal()
        n_qqzz_modelfit["4l"] += qqzz_modelfit[fState].getVal()
        n_zz_modelfit["4l"] += n_ggzz_modelfit[fState]+n_qqzz_modelfit[fState]

    CMS_channel = w.cat("CMS_channel")
    mass = w.var("CMS_zz4l_mass").frame(RooFit.Bins(15))
    #mass = w.var("CMS_zz4l_mass").frame(RooFit.Bins(45))

    if (fstate=="4l"):
        data.plotOn(mass,RooFit.LineColor(0),RooFit.MarkerColor(0),RooFit.LineWidth(0))
        sim.plotOn(mass,RooFit.LineColor(kRed), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kBlack), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3,shapeBkg_out_trueH_ch1,shapeBkg_out_trueH_ch2,shapeBkg_out_trueH_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kOrange), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3,shapeBkg_fakeH_ch1,shapeBkg_fakeH_ch2,shapeBkg_fakeH_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kAzure-3), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3,shapeBkg_bkg_ggzz_ch1,shapeBkg_bkg_ggzz_ch2,shapeBkg_bkg_ggzz_ch3,shapeBkg_bkg_qqzz_ch1,shapeBkg_bkg_qqzz_ch2,shapeBkg_bkg_qqzz_ch3"), RooFit.ProjWData(data,True))
        sim.plotOn(mass, RooFit.LineColor(kGreen+3), RooFit.Components("shapeBkg_bkg_zjets_ch1,shapeBkg_bkg_zjets_ch2,shapeBkg_bkg_zjets_ch3"), RooFit.ProjWData(data,True))
        datahist = RooAbsData.createHistogram(data,"datahist",CMS_zz4l_mass,RooFit.Binning(15,105,140))
    else:
        sbin = "ch"+channel[fstate]
        data = data.reduce(RooFit.Cut("CMS_channel==CMS_channel::"+sbin))
        data.plotOn(mass,RooFit.LineColor(0),RooFit.MarkerColor(0),RooFit.LineWidth(0))
        pdfi.plotOn(mass, RooFit.Components("pdf_binch"+channel[fstate]+"_nuis"),RooFit.LineColor(kRed), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kBlack), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin+",shapeBkg_out_trueH_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kOrange), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin+",shapeBkg_fakeH_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kAzure-3), RooFit.Components("shapeBkg_bkg_zjets_"+sbin+",shapeBkg_bkg_ggzz_"+sbin+",shapeBkg_bkg_qqzz_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        pdfi.plotOn(mass, RooFit.LineColor(kGreen+3), RooFit.Components("shapeBkg_bkg_zjets_"+sbin), RooFit.Slice(CMS_channel,sbin),RooFit.ProjWData(RooArgSet(CMS_channel),data,True))
        datahist = RooAbsData.createHistogram(data,"datahist",CMS_zz4l_mass,RooFit.Binning(15,105,140))

    gStyle.SetOptStat(0)

    c = TCanvas("c","c",1000,800)
    c.cd()

    #dummy = TH1D("","",1,105.6,140.6)
    dummy = TH1D("","",1,105.0,140.0)
    dummy.SetBinContent(1,2)
    dummy.SetFillColor(0)
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.SetMarkerColor(0)
    dummy.GetYaxis().SetTitle("Events / (2.33 GeV)")
    #dummy.GetYaxis().SetTitle("Events / (1 GeV)")
    dummy.GetXaxis().SetTitle("m_{"+fstate.replace("mu","#mu")+"} (GeV)")
    if (not opt.UNBLIND):
        dummy.SetMaximum(1.15*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate]))
    else:
        if (fstate=="4mu"):
            dummy.SetMaximum(2.7*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate],3.0))
        elif (fstate=="4e"):
            dummy.SetMaximum(2.7*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate],2.0))
        elif (fstate=="2e2mu"):
            dummy.SetMaximum(2.7*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate],3.0))
        else:
            dummy.SetMaximum(1.5*max(n_trueH_asimov[fstate],n_trueH_modelfit[fstate],7.0))
    dummy.SetMinimum(0.0)
    dummy.Draw()

    dummy_data = TH1D()
    dummy_data.SetMarkerColor(kBlack)
    dummy_data.SetMarkerStyle(20)
    dummy_fid = TH1D()
    dummy_fid.SetLineColor(kRed)
    dummy_fid.SetLineWidth(2)
    dummy_out = TH1D()
    dummy_out.SetLineColor(kBlack)
    dummy_out.SetLineWidth(2)
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
    legend.AddEntry(dummy_data,"Asimov Data (SM m(H) = 125.0 GeV)","ep")
    legend.AddEntry(dummy_fid,"N_{fid.}^{fit} = %.2f (exp. = %.2f)"%(n_trueH_modelfit[fstate],n_trueH_asimov[fstate]), "l")
    legend.AddEntry(dummy_out, "N_{out}^{fit} = %.2f (exp. = %.2f)"%(n_out_trueH_modelfit[fstate],n_out_trueH_asimov[fstate]), "l")
    legend.AddEntry(dummy_fake, "N_{wrong}^{fit} = %.2f (exp. = %.2f)"%(n_fakeH_modelfit[fstate],n_fakeH_asimov[fstate]), "l")
    legend.AddEntry(dummy_zz, "N_{ZZ}^{fit} = %.2f (exp. = %.2f)"%(n_zz_modelfit[fstate],n_zz_asimov[fstate]), "l")
    legend.AddEntry(dummy_zx, "N_{Z+X}^{fit} = %.2f (exp. = %.2f)"%(n_zjets_modelfit[fstate],n_zjets_asimov[fstate]), "l")
    legend.SetTextSize(0.03)
    #if (not opt.UNBLIND):
    #    legend.AddEntry(dummy_data,"Asimov Data (SM m(H) = "+opt.ASIMOVMASS+" GeV)","ep")
    #else:
    #    legend.AddEntry(dummy_data,"Data","ep")
    #legend.AddEntry(dummy_fid,"Fiducial Signal", "l")
    #legend.AddEntry(dummy_out, "Non-fiducial Signal", "l")
    #legend.AddEntry(dummy_fake, "Combinatorial XH", "l")
    #legend.AddEntry(dummy_zz, "ZZ", "l")
    #legend.AddEntry(dummy_zx, "Z+X", "l")
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw()

    '''
    legend = TLegend(.20,.7,.9,.90)
    legend.SetTextSize(0.04)
    legend.SetNColumns(2)
    if (not opt.UNBLIND):
    #    legend.AddEntry(dummy_data,"Asimov Data (SM m(H) = "+opt.ASIMOVMASS+" GeV)","ep")
        legend.AddEntry(dummy_data,"Asimov Data","ep")
    else:
        legend.AddEntry(dummy_data,"Data","ep")
    legend.AddEntry(dummy_fake, "Combinatorial XH", "l")
    legend.AddEntry(dummy_fid,"Fiducial Signal", "l")
    legend.AddEntry(dummy_zz, "ZZ", "l")
    legend.AddEntry(dummy_out, "Non-fiducial Signal", "l")
    legend.AddEntry(dummy_zx, "Z+X", "l")
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw()
    '''

    mass.Draw("same")
    datagraph = TGraphAsymmErrors(datahist)
    datagraph.SetMarkerSize(1.2)
    datagraph.SetMarkerStyle(20)
    datagraph.SetLineWidth(1)
    alpha = 1.0 - 0.6827
    for i in range(0,datagraph.GetN()):
        N = datagraph.GetY()[i];
        if (N==0): L = 0.0
        else: L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
        U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
        datagraph.SetPointEYlow(i, N-L);
        datagraph.SetPointEYhigh(i, U-N);
    datagraph.Draw("psame")

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    if (not opt.LUMISCALE=="1.0"):
        lumi = round(59.7*float(opt.LUMISCALE),1)
        latex2.DrawLatex(0.87, 0.95,str(lumi)+"fb^{-1} at #sqrt{s} = 13 TeV")
    else:
        latex2.DrawLatex(0.87, 0.95,"59.7 fb^{-1} at #sqrt{s} = 13 TeV")
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
    #latex2.DrawLatex(0.20,0.85,"Unfolding model: "+modelName.replace("_"," ")+" GeV")


    if (not opt.UNBLIND):
        c.SaveAs("plots/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName+'_'+fstate+"_recobin"+str(recobin)+".pdf")
        c.SaveAs("plots/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName+'_'+fstate+"_recobin"+str(recobin)+".png")
    else:
        c.SaveAs("plots/data_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName+'_'+fstate+"_recobin"+str(recobin)+".pdf")
        c.SaveAs("plots/data_unfoldwith_"+modelName+"_"+physicalModel+"_"+obsName+'_'+fstate+"_recobin"+str(recobin)+".png")


modelName = opt.UNFOLD
physicalModel = 'v2'
asimovDataModel = opt.ASIMOV
asimovPhysicalModel = 'v2'
obsName = opt.OBSNAME
observableBins = opt.OBSBINS.split('|')
observableBins.pop()
observableBins.pop(0)

#asimovModelName = 'ggH_powheg15_JHUgen_125'
#asimovPhysicalModel = 'v2'
#modelName = 'ggH_powheg15_JHUgen_125'
#physicalModel = 'v2'
#recobin = 0

for fState in ["4e","4mu","2e2mu","4l"]:
    for recobin in range(len(observableBins)-1):
        plotAsimov(asimovDataModel, asimovPhysicalModel, modelName, physicalModel, 'mass4l', fState, recobin)
