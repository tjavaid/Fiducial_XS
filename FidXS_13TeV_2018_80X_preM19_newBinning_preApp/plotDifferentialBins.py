import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *

from datetime import datetime
now = datetime.now() # current date and time
##date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
date = now.strftime("%d%m%Y")
from sample_shortnames import *
#from sample_shortnames_2016 import *
#from sample_shortnames_2017 import *
#from sample_shortnames_2018 import *
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
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.38', help='Asimov MAss')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observable, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    parser.add_option('',   '--era',  dest='ERA',  type='string',default='2018',   help='Era to analyze, e.g. 2016, 2017, 2018 or Full ')
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

era=opt.ERA
#if (not os.path.exists("plots")):
#    os.system("mkdir plots")
#if (not os.path.exists("plots_"+date)):
if (not os.path.exists("plots_"+era+"/"+opt.OBSNAME)):
    os.system("mkdir -p plots_"+era+"/"+opt.OBSNAME)
            
from ROOT import *
from tdrStyle import *
setTDRStyle()

            
asimovDataModel = opt.ASIMOV
asimovPhysicalModel = 'v2'
obsName = opt.OBSNAME
observableBins = opt.OBSBINS.split('|')
observableBins.pop()
observableBins.pop(0)
print float(observableBins[len(observableBins)-1])
if float(observableBins[len(observableBins)-1])>200.0:
    observableBins[len(observableBins)-1]='200.0'

if (opt.ERA == '2016'): years = ['2016']
if (opt.ERA == '2017'): years = ['2017']
if (opt.ERA == '2018'): years = ['2018']
if (opt.ERA == 'Full'): years = ['2016','2017','2018']

    
#def plotDifferentialBins(asimovDataModel, asimovPhysicalModel, obsName, fstate, observableBins):
def plotDifferentialBins(asimovDataModel, asimovPhysicalModel, obsName, fstate, observableBins, years):


    nBins = len(observableBins)-1
    channel = {"4mu":"1", "4e":"2", "2e2mu":"3", "4l":"2"} # 4l is dummy, won't be used

    # Load some libraries                                 
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")
    
    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
    
    f_asimov = TFile(asimovDataModel+'_all_'+obsName+'_13TeV_Asimov_'+asimovPhysicalModel+'.root','READ')
    print "Asimov file is :  ", f_asimov

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
    '''
    n_trueH_asimov = {}
    for recobin in range(nBins):    
        n_trueH_asimov["4lrecobin"+str(recobin)] = 0.0
    n_trueH_otherfid_asimov = {}
    for recobin in range(nBins):
        n_trueH_otherfid_asimov["4lrecobin"+str(recobin)] = 0.0
    n_zjets_asimov = {}
    for recobin in range(nBins):
        n_zjets_asimov["4lrecobin"+str(recobin)] = 0.0
    n_ggzz_asimov = {}
    for recobin in range(nBins):
        n_ggzz_asimov["4lrecobin"+str(recobin)] = 0.0
    n_fakeH_asimov = {}
    for recobin in range(nBins):    
        n_fakeH_asimov["4lrecobin"+str(recobin)] = 0.0
    n_out_trueH_asimov = {}
    for recobin in range(nBins):    
        n_out_trueH_asimov["4lrecobin"+str(recobin)] = 0.0
    n_qqzz_asimov = {}
    for recobin in range(nBins):    
        n_qqzz_asimov["4lrecobin"+str(recobin)] = 0.0
    n_zz_asimov = {}
    for recobin in range(nBins):    
        n_zz_asimov["4lrecobin"+str(recobin)] = 0.0
    '''    
    n_trueH_asimov = {}
    n_trueH_otherfid_asimov = {}
    n_zjets_asimov = {}
    n_ggzz_asimov = {}
    n_fakeH_asimov = {}
    n_out_trueH_asimov = {}
    n_qqzz_asimov = {}
    n_zz_asimov = {}
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
                for bin in range(nBins):
                    #trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+"_proc_trueH"+fState+"Bin"+str(bin))            
		   # print "bin, recobin, value ", bin, recobin, w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin+1)+"_"+year+"_proc_trueH"+fState+"Bin"+str(bin)).getVal()
                    trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)+year] = w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+"_proc_trueH"+fState+"Bin"+str(bin))            
                #zjets_asimov[fState+"recobin"+str(recobin)] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+"_proc_bkg_zjets")
										#n_exp_final_bin   pT4l    _   4mu    _bin         5        _   2018 _proc_bkg_zjets
#		print "trueH_asimov list:  ", trueH_asimov
                zjets_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+"_proc_bkg_zjets")
                #ggzz_asimov[fState+"recobin"+str(recobin)] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+"_proc_bkg_ggzz")
                ggzz_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+"_proc_bkg_ggzz")
                #fakeH_asimov[fState+"recobin"+str(recobin)] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+"_proc_fakeH")
                fakeH_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+"_proc_fakeH")
                #out_trueH_asimov[fState+"recobin"+str(recobin)] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+"_proc_out_trueH")
                out_trueH_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+"_proc_out_trueH")
                #qqzz_asimov[fState+"recobin"+str(recobin)] = w_asimov.function("n_exp_final_binch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+"_proc_bkg_qqzz")
                qqzz_asimov[fState+"recobin"+str(recobin)+year] = w_asimov.function("n_exp_final_bin"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+"_proc_bkg_qqzz")
                n_trueH_otherfid_asimov[fState+"recobin"+str(recobin)+year] = 0.0
                for bin in range(nBins):
    		    print "bin is==", bin
	    	    print "recobin===", recobin	
                    if (bin==recobin): 
			n_trueH_asimov[fState+"recobin"+str(recobin)+year] = trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)+year].getVal()
#		        print "trueH_asimov value is(if condition) ==", trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)].getVal()	
                    else: 
			#print "year is :  ", year
			#print "else:  bin, recoin, value:   ", bin, recobin,fState+"Bin"+str(bin)+"recobin"+str(recobin)
			#print "else:  bin, recoin, value:   ", bin, recobin,trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)].getVal()
			n_trueH_otherfid_asimov[fState+"recobin"+str(recobin)+year] += trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)+year].getVal()
 		#        print "trueH_asimov value is (else condition) ==", trueH_asimov[fState+"Bin"+str(bin)+"recobin"+str(recobin)].getVal()	
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

    databin = {}
    if (fstate=="4l"):
        for year in years:
            for recobin in range(nBins):
                datacut = ''
                for fState in fStates:
#                    datacut += "CMS_channel==CMS_channel::ch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+" || "
		    datacut += "CMS_channel==CMS_channel::"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+" || "
                datacut = datacut.rstrip(" || ")
	        print "datacut is :    ", datacut
            #databin[str(recobin)] = data.reduce(RooFit.Cut(datacut))
                databin[str(recobin)+year] = data.reduce(RooFit.Cut(datacut))
            #databin[str(recobin)].Print("v")
    else:
        for year in years:
            for recobin in range(nBins):
            #sbin = "ch"+channel[fstate]+"_ch"+str(recobin+1)
#                sbin = "ch"+channel[fstate]+"_ch"+str(recobin+1)+"_"+year
                sbin = obsName+"_"+fstate+"_bin"+str(recobin)+"_"+year
                databin[str(recobin)+year] = data.reduce(RooFit.Cut("CMS_channel==CMS_channel::"+sbin))

#TJ
    '''
    else:
        for recobin in range(nBins):
            datacut = ''
	    print "fStates are:  ", fStates
            for year in years:
                for fState in fStates:
#                    datacut += "CMS_channel==CMS_channel::ch"+channel[fState]+"_ch"+str(recobin+1)+"_"+year+" || "
                    datacut += "CMS_channel==CMS_channel::"+obsName+"_"+fState+"_bin"+str(recobin)+"_"+year+" || "
            datacut = datacut.rstrip(" || ")
            print "datacut is :    ", datacut
            databin[str(recobin)] = data.reduce(RooFit.Cut(datacut))
            #databin[str(recobin)].Print("v")
    '''


    if (obsName.startswith('njets')):
        h_data = TH1D("h_data","h_data",nBins,0,nBins)
        h_sig = TH1D("h_sig","h_xig",nBins,0,nBins)
        h_zz = TH1D("h_zz","h_zz",nBins,0,nBins)
        h_zx = TH1D("h_zx","h_zx",nBins,0,nBins)
    else:
        h_data = TH1D("h_data","h_data",nBins,array('d',[float(observableBins[i]) for i in range(nBins+1)]))
        h_sig = TH1D("h_sig","h_xig",nBins,array('d',[float(observableBins[i]) for i in range(nBins+1)]))
        h_zz = TH1D("h_zz","h_zz",nBins,array('d',[float(observableBins[i]) for i in range(nBins+1)]))
        h_zx = TH1D("h_zx","h_zx",nBins,array('d',[float(observableBins[i]) for i in range(nBins+1)]))


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
            print fstate,"recobin",recobin, "year", year
            nH[fstate+"recobin"+str(recobin)]+=n_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_trueH_otherfid_asimov[fstate+"recobin"+str(recobin)+year]+n_out_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_fakeH_asimov[fstate+"recobin"+str(recobin)+year]
            print 'H:',n_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_trueH_otherfid_asimov[fstate+"recobin"+str(recobin)+year]+n_out_trueH_asimov[fstate+"recobin"+str(recobin)+year]+n_fakeH_asimov[fstate+"recobin"+str(recobin)+year] 

	    nZZ[fstate+"recobin"+str(recobin)]+=n_zz_asimov[fstate+"recobin"+str(recobin)+year]
            print 'ZZ:',n_zz_asimov[fstate+"recobin"+str(recobin)+year]

	    nZX[fstate+"recobin"+str(recobin)]+=n_zjets_asimov[fstate+"recobin"+str(recobin)+year]
            print 'Z+X:',n_zjets_asimov[fstate+"recobin"+str(recobin)+year]

	    nData[fstate+"recobin"+str(recobin)]+=databin[str(recobin)+year].sumEntries()
            print 'Data:',databin[str(recobin)+year].sumEntries()
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


    if (obsName=="pT4l"):
        label="p_{T}^{H}"
        unit="GeV"
    elif (obsName=="massZ2"):
        label = "m(Z_{2})"
        unit = "GeV"
    elif (obsName=="massZ1"):
        label = "m(Z_{1})"
        unit = "GeV"
    elif (obsName=="nJets" or obsName=="njets_pt30_eta4p7"):
        label = "N(jets) |#eta|<4.7"
        unit = ""
    elif (obsName=="njets_pt30_eta2p5"):
        label = "N(jets) |#eta|<2.5"
        unit = ""
    elif (obsName=="pt_leadingjet_pt30_eta4p7"):
        label = "p_{T}(jet)"
        unit = "GeV"
    elif (obsName=="pt_leadingjet_pt30_eta2p5"):
        label = "p_{T}(jet) |#eta|<2.5"
        unit = "GeV"
    elif (obsName=="absrapidity_leadingjet_pt30_eta4p7"):
        label = "|y(jet)|"
        unit = ""
    elif (obsName=="absrapidity_leadingjet_pt30_eta2p5"):
        label = "|y(jet)| |#eta|<2.5"
        unit = ""
    elif (obsName=="absdeltarapidity_hleadingjet_pt30_eta4p7"):
        label = "|y(H)-y(jet)|"
        unit = ""
    elif (obsName=="absdeltarapidity_hleadingjet_pt30_eta2p5"):
        label = "|y(H)-y(jet)| |#eta|<2.5"
        unit = ""
    elif (obsName=="rapidity4l"):
        label = "|y^{H}|"
        unit = ""
    elif (obsName=="cosThetaStar"):
        label = "cos#theta*"
        unit = ""
    elif (obsName=="cosTheta1"):
        label = "cos#theta_{1}"
        unit = ""
    elif (obsName=="cosTheta2"):
        label = "cos#theta_{2}"
        unit = ""
    elif (obsName=="Phi"):
        label = "#Phi"
        unit = ""
    elif (obsName=="Phi1"):
        label = "#Phi_{1}"
        unit = ""
                                                                                                        

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
#    latex2.DrawLatex(0.87, 0.95, "10.0 fb^{-1} at #sqrt{s} = 13 TeV")
   # latex2.DrawLatex(0.87, 0.95, "41.4 fb^{-1} at #sqrt{s} = 13 TeV")
#    latex2.DrawLatex(0.87, 0.95, "58.8 fb^{-1} at #sqrt{s} = 13 TeV")
    print opt.LUMISCALE
    if (not opt.LUMISCALE=="1.0"):
        if (opt.ERA=='2016') : lumi = round(35.9*float(opt.LUMISCALE),1)
        elif (opt.ERA=='2017') : lumi = round(41.7*float(opt.LUMISCALE),1)
        else  : lumi = round(58.5*float(opt.LUMISCALE),1)
        latex2.DrawLatex(0.94, 0.94,str(lumi)+" fb^{-1} (13 TeV)")
    else:
        if (opt.ERA=='2016') : latex2.DrawLatex(0.94, 0.94,"35.9 fb^{-1} (13 TeV)")
        elif (opt.ERA=='2017') : latex2.DrawLatex(0.94, 0.94,"41.7 fb^{-1} (13 TeV)")
        elif (opt.ERA=='2018') : latex2.DrawLatex(0.94, 0.94,"58.8 fb^{-1} (13 TeV)")
        else : latex2.DrawLatex(0.94, 0.94,"137 fb^{-1} (13 TeV)")

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
    latex2.DrawLatex(0.19,0.75,"105 GeV < m("+fstate.replace('mu','#mu')+") < 140 GeV")
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
                                                                                                            
    if (not opt.UNBLIND):
        #c.SaveAs("plots/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName+'_'+fstate+".pdf")
        c.SaveAs("plots_"+era+"/"+opt.OBSNAME+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName+'_'+fstate+".pdf")
        c.SaveAs("plots_"+era+"/"+opt.OBSNAME+"/asimovdata_"+asimovDataModel+"_"+asimovPhysicalModel+"_"+obsName+'_'+fstate+".png")
    else:
        c.SaveAs("plots_"+era+"/"+opt.OBSNAME+"/data_"+obsName+'_'+fstate+".pdf")
        c.SaveAs("plots_"+era+"/"+opt.OBSNAME+"/data_"+obsName+'_'+fstate+".png")


fStates = ["4e","4mu","2e2mu","4l"]
print "years are: ", years
for fState in fStates:
    #plotDifferentialBins(asimovDataModel, asimovPhysicalModel, obsName, fState, observableBins)
    plotDifferentialBins(asimovDataModel, asimovPhysicalModel, obsName, fState, observableBins, years)
