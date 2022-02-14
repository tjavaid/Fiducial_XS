# this script is called once for each reco bin (obsBin)
# in each reco bin there are (nBins) signals (one for each gen bin)

from ROOT import *
from datapaths_full import *
from sample_shortnames import *
import os,sys
def createXSworkspace(obsName, channel, nBins, obsBin, observableBins, usecfactor, addfakeH, modelName, physicalModel,year):
    #import os,sys

    tmpSrcDir=datapaths[year]["data"]
    sys.path.append('./datacardInputs_'+year+'/')


    print "workspace: working path is:      ",os.getcwd()
    obsBin_low = observableBins[obsBin]
    obsBin_high = observableBins[obsBin+1]

    obs_bin_lowest = observableBins[0]
    obs_bin_highest = observableBins[len(observableBins)-1]
    
    recobin = "recobin"+str(obsBin)

    doJES = 1
    
    # Load some libraries
    gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    gSystem.Load("$CMSSW_BASE/lib//$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
    gSystem.AddIncludePath("-I$ROOFITSYS/include")
    gSystem.AddIncludePath("-Iinclude/")

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING) 

    #from inputs_sig import eff,inc_wrongfrac,binfrac_wrongfrac,inc_outfrac,binfrac_outfrac
    if (usecfactor):
        _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['cfactor','inc_wrongfrac','binfrac_wrongfrac','inc_outfrac','binfrac_outfrac','lambdajesup','lambdajesdn'], -1)
        cfactor = _temp.cfactor
        inc_outfrac = _temp.inc_outfrac
        binfrac_outfrac = _temp.binfrac_wrongfrac
    else:
        _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc','eff','inc_wrongfrac','binfrac_wrongfrac','outinratio','lambdajesup','lambdajesdn'], -1)
        acc = _temp.acc
        eff = _temp.eff
        outinratio = _temp.outinratio        

    lambdajesup = _temp.lambdajesup
    lambdajesdn = _temp.lambdajesdn        
    inc_wrongfrac = _temp.inc_wrongfrac
    binfrac_wrongfrac = _temp.binfrac_wrongfrac

    #from inputs_bkg_{obsName} import fractionsBackground
    _temp = __import__('inputs_bkg_'+obsName, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # Load the legacy f
    #workspace_in = TFile("125.0/hzz4l_"+channel+"S_8TeV.input.root","READ")
    f_in = TFile("125.0/hzz4l_"+channel+"S_8TeV.input.root","READ")
    w = f_in.Get("w")
    #w.Print()

    # import h4l xs br
    _temp = __import__('higgs_xsbr_13TeV', globals(), locals(), ['higgs_xs','higgs4l_br'], -1)
    higgs_xs = _temp.higgs_xs
    higgs4l_br = _temp.higgs4l_br

    # 4 lepton mass observable to perform the fit
    m = w.var("CMS_zz4l_mass")
    #print "m.numBins()",m.numBins()
    m.setMin(105.0)
    m.setMax(140.0)
    #m.setBins(45)
    #m.Print("v")

    mass4e = RooRealVar("mass4e", "mass4e", 105.0, 140.0)
    mass4mu = RooRealVar("mass4mu", "mass4mu", 105.0, 140.0)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",105.0, 140.0)
    if (not obsName=="mass4l"):
        #if (obsName=="rapidity4l" or obsName=="cosThetaStar" or obsName=="cosTheta1" or obsName=="cosTheta2" or obsName=="Phi" or obsName=="Phi1"):
        if (obsName=="rapidity4l"): #TJ, absolute ?
            observable = RooRealVar(obsName,obsName,-1.0*float(obs_bin_highest),float(obs_bin_highest))
        else:
            observable = RooRealVar(obsName,obsName,float(obs_bin_lowest),float(obs_bin_highest))        
        observable.Print()

    # luminosity
    if (year=="2018"): lumi = RooRealVar("lumi_13"+year,"lumi_13"+year, 59.7)
    elif (year=="2017"): lumi = RooRealVar("lumi_13"+year,"lumi_13"+year, 41.5)
    else: lumi = RooRealVar("lumi_13"+year,"lumi_13"+year, 35.9)
    #lumi = RooRealVar("lumi_13"+year,"lumi_13"+year, 58.8)
    
    # update to 13 TeV parameterization
    MH = w.var("MH")

    
    if (year=='2018'):
        CMS_zz4l_mean_m_sig_2018 = RooRealVar("CMS_zz4l_mean_m_sig_"+year,"CMS_zz4l_mean_m_sig_"+year,0.0)
        CMS_zz4l_mean_e_sig_2018 = RooRealVar("CMS_zz4l_mean_e_sig_"+year,"CMS_zz4l_mean_e_sig_"+year,0.0)
        CMS_zz4l_sigma_m_sig_2018 = RooRealVar("CMS_zz4l_sigma_m_sig_"+year,"CMS_zz4l_sigma_m_sig_"+year,0.0)
        CMS_zz4l_sigma_e_sig_2018 = RooRealVar("CMS_zz4l_sigma_e_sig_"+year,"CMS_zz4l_sigma_e_sig_"+year,0.0)
        CMS_zz4l_n_sig_1_2018 = RooRealVar("CMS_zz4l_n_sig_1_"+year,"CMS_zz4l_n_sig_1_"+year,0.0)
        CMS_zz4l_n_sig_2_2018 = RooRealVar("CMS_zz4l_n_sig_2_"+year,"CMS_zz4l_n_sig_2_"+year,0.0)
        CMS_zz4l_n_sig_3_2018 = RooRealVar("CMS_zz4l_n_sig_3_"+year,"CMS_zz4l_n_sig_3_"+year,0.0)

        # scale systematics
        CMS_zz4l_mean_m_err_1_2018 = RooRealVar("CMS_zz4l_mean_m_err_1_"+year,"CMS_zz4l_mean_m_err_1_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_2_2018 = RooRealVar("CMS_zz4l_mean_e_err_2_"+year,"CMS_zz4l_mean_e_err_2_"+year,0.003,0.003,0.003)
        CMS_zz4l_mean_m_err_3_2018 = RooRealVar("CMS_zz4l_mean_m_err_3_"+year,"CMS_zz4l_mean_m_err_3_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_3_2018 = RooRealVar("CMS_zz4l_mean_e_err_3_"+year,"CMS_zz4l_mean_e_err_3_"+year,0.003,0.003,0.003)

    elif (year=='2017'):
        CMS_zz4l_mean_m_sig_2017 = RooRealVar("CMS_zz4l_mean_m_sig_"+year,"CMS_zz4l_mean_m_sig_"+year,0.0)
        CMS_zz4l_mean_e_sig_2017 = RooRealVar("CMS_zz4l_mean_e_sig_"+year,"CMS_zz4l_mean_e_sig_"+year,0.0)
        CMS_zz4l_sigma_m_sig_2017 = RooRealVar("CMS_zz4l_sigma_m_sig_"+year,"CMS_zz4l_sigma_m_sig_"+year,0.0)
        CMS_zz4l_sigma_e_sig_2017 = RooRealVar("CMS_zz4l_sigma_e_sig_"+year,"CMS_zz4l_sigma_e_sig_"+year,0.0)
        CMS_zz4l_n_sig_1_2017 = RooRealVar("CMS_zz4l_n_sig_1_"+year,"CMS_zz4l_n_sig_1_"+year,0.0)
        CMS_zz4l_n_sig_2_2017 = RooRealVar("CMS_zz4l_n_sig_2_"+year,"CMS_zz4l_n_sig_2_"+year,0.0)
        CMS_zz4l_n_sig_3_2017 = RooRealVar("CMS_zz4l_n_sig_3_"+year,"CMS_zz4l_n_sig_3_"+year,0.0)

        # scale systematics
        CMS_zz4l_mean_m_err_1_2017 = RooRealVar("CMS_zz4l_mean_m_err_1_"+year,"CMS_zz4l_mean_m_err_1_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_2_2017 = RooRealVar("CMS_zz4l_mean_e_err_2_"+year,"CMS_zz4l_mean_e_err_2_"+year,0.003,0.003,0.003)
        CMS_zz4l_mean_m_err_3_2017 = RooRealVar("CMS_zz4l_mean_m_err_3_"+year,"CMS_zz4l_mean_m_err_3_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_3_2017 = RooRealVar("CMS_zz4l_mean_e_err_3_"+year,"CMS_zz4l_mean_e_err_3_"+year,0.003,0.003,0.003)

    else:
        CMS_zz4l_mean_m_sig_2016 = RooRealVar("CMS_zz4l_mean_m_sig_"+year,"CMS_zz4l_mean_m_sig_"+year,0.0)
        CMS_zz4l_mean_e_sig_2016 = RooRealVar("CMS_zz4l_mean_e_sig_"+year,"CMS_zz4l_mean_e_sig_"+year,0.0)
        CMS_zz4l_sigma_m_sig_2016 = RooRealVar("CMS_zz4l_sigma_m_sig_"+year,"CMS_zz4l_sigma_m_sig_"+year,0.0)
        CMS_zz4l_sigma_e_sig_2016 = RooRealVar("CMS_zz4l_sigma_e_sig_"+year,"CMS_zz4l_sigma_e_sig_"+year,0.0)
        CMS_zz4l_n_sig_1_2016 = RooRealVar("CMS_zz4l_n_sig_1_"+year,"CMS_zz4l_n_sig_1_"+year,0.0)
        CMS_zz4l_n_sig_2_2016 = RooRealVar("CMS_zz4l_n_sig_2_"+year,"CMS_zz4l_n_sig_2_"+year,0.0)
        CMS_zz4l_n_sig_3_2016 = RooRealVar("CMS_zz4l_n_sig_3_"+year,"CMS_zz4l_n_sig_3_"+year,0.0)

        # scale systematics
        CMS_zz4l_mean_m_err_1_2016 = RooRealVar("CMS_zz4l_mean_m_err_1_"+year,"CMS_zz4l_mean_m_err_1_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_2_2016 = RooRealVar("CMS_zz4l_mean_e_err_2_"+year,"CMS_zz4l_mean_e_err_2_"+year,0.003,0.003,0.003)
        CMS_zz4l_mean_m_err_3_2016 = RooRealVar("CMS_zz4l_mean_m_err_3_"+year,"CMS_zz4l_mean_m_err_3_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_3_2016 = RooRealVar("CMS_zz4l_mean_e_err_3_"+year,"CMS_zz4l_mean_e_err_3_"+year,0.003,0.003,0.003)





    if (channel=='2e2mu'):
	if (year=='2018'):
            CMS_zz4l_mean_sig_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year, \
                                                             "(124.260469656+(0.995095874123)*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                               RooArgList(MH,CMS_zz4l_mean_m_sig_2018,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_err_3_2018,CMS_zz4l_mean_e_err_3_2018))
        
            CMS_zz4l_sigma_sig_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year, \
                                                                "(1.55330758963+(0.00797274642218)*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_sigma_e_sig_2018))   
        
            CMS_zz4l_alpha_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"(0.947414158515+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"(3.33147279858+(-0.0438375854704)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_2018))
        
        
            CMS_zz4l_alpha2_3_centralValue_2018=RooFormulaVar("CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"(1.52497361611+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_centralValue_2018=RooFormulaVar("CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"(5.20522265056+(0)*(@0-125))",RooArgList(MH))

        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_3_centralValue_2018,CMS_zz4l_sigma_sig_3_centralValue_2018,CMS_zz4l_alpha_3_centralValue_2018,CMS_zz4l_n_3_centralValue_2018,CMS_zz4l_alpha2_3_centralValue_2018,CMS_zz4l_n2_3_centralValue_2018)
	elif (year=='2017'):
	    CMS_zz4l_mean_sig_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year, \
                                                               "(124.524+(0.00248708+1)*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                               RooArgList(MH,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_m_err_3_2017,CMS_zz4l_mean_e_err_3_2017))

            CMS_zz4l_sigma_sig_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,\
                                                                "(1.77228+(0.00526163)*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_e_sig_2017))

            CMS_zz4l_alpha_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"(0.967963+(-0.0047248)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"(3.69774+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_2017))
            CMS_zz4l_alpha2_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"(1.51606+(-0.000272186)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"(6.01048+(0)*(@0-125))",RooArgList(MH))

        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_3_centralValue_2017,CMS_zz4l_sigma_sig_3_centralValue_2017,CMS_zz4l_alpha_3_centralValue_2017,CMS_zz4l_n_3_centralValue_2017,CMS_zz4l_alpha2_3_centralValue_2017,CMS_zz4l_n2_3_centralValue_2017)
	else:
	    CMS_zz4l_mean_sig_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year, \
                                                               "(124.539+(-0.00679774+1)*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                               RooArgList(MH,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_m_err_3_2016,CMS_zz4l_mean_e_err_3_2016))
    
            CMS_zz4l_sigma_sig_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,\
                                                                "(1.64632+(0.016435)*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_e_sig_2016))    
            CMS_zz4l_alpha_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"(0.905389+(0.0029819)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"(3.90164+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_2016))
            CMS_zz4l_alpha2_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"(1.5737+(0.00776476)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"(4.33416+(0)*(@0-125))",RooArgList(MH))

        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_3_centralValue_2016,CMS_zz4l_sigma_sig_3_centralValue_2016,CMS_zz4l_alpha_3_centralValue_2016,CMS_zz4l_n_3_centralValue_2016,CMS_zz4l_alpha2_3_centralValue_2016,CMS_zz4l_n2_3_centralValue_2016) 
        
    if (channel=='4e'):
	if (year=='2018'):


            CMS_zz4l_mean_sig_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year, \
                                                             "(123.5844824+(0.985478630993)*(@0-125)) + @0*@1*@2", \
                                                               RooArgList(MH,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_e_err_2_2018))
        
            CMS_zz4l_sigma_sig_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(2.06515102908+(0.0170917403402)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig_2018))
        
            CMS_zz4l_alpha_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"(0.948100247167+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"(4.50639853892+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_2018))
            CMS_zz4l_alpha2_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"(1.50095152675+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"(8.41693578742+(0.219719825966)*(@0-125))",RooArgList(MH))
        
        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_2_centralValue_2018,CMS_zz4l_sigma_sig_2_centralValue_2018,CMS_zz4l_alpha_2_centralValue_2018,CMS_zz4l_n_2_centralValue_2018,CMS_zz4l_alpha2_2_centralValue_2018,CMS_zz4l_n2_2_centralValue_2018)
	elif (year=='2017'):
	    CMS_zz4l_mean_sig_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year, \
                                                               "(124.1+(-0.00262293+1)*(@0-125)) + @0*@1*@2", \
                                                               RooArgList(MH,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_err_2_2017))
    
            CMS_zz4l_sigma_sig_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(2.38283+(0.0155)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig_2017))
    
            CMS_zz4l_alpha_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"(0.972669+(-0.00597402)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"(5.05142+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_2017))
            CMS_zz4l_alpha2_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"(1.62625+(0.0121146)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"(6.30057+(0)*(@0-125))",RooArgList(MH))

        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_2_centralValue_2017,CMS_zz4l_sigma_sig_2_centralValue_2017,CMS_zz4l_alpha_2_centralValue_2017,CMS_zz4l_n_2_centralValue_2017,CMS_zz4l_alpha2_2_centralValue_2017,CMS_zz4l_n2_2_centralValue_2017)
	else:
	    CMS_zz4l_mean_sig_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year, \
                                                               "(124.194+(-0.0123934+1)*(@0-125)) + @0*@1*@2", \
                                                               RooArgList(MH,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_err_2_2016))

            CMS_zz4l_sigma_sig_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(2.09076+(0.0153247)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig_2016))

            CMS_zz4l_alpha_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"(0.778691+(-0.00177387)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"(6.85936+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_2016))
            CMS_zz4l_alpha2_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"(1.47389+(0.00503384)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"(7.24158+(0)*(@0-125))",RooArgList(MH))

        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_2_centralValue_2016,CMS_zz4l_sigma_sig_2_centralValue_2016,CMS_zz4l_alpha_2_centralValue_2016,CMS_zz4l_n_2_centralValue_2016,CMS_zz4l_alpha2_2_centralValue_2016,CMS_zz4l_n2_2_centralValue_2016) 
        
    if (channel=='4mu'):
	if (year=='2018'):
            CMS_zz4l_mean_sig_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year, \
                                                               "(124.820536957+(0.999619883119)*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig_2018,CMS_zz4l_mean_m_err_1_2018))
        
            CMS_zz4l_sigma_sig_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(1.09001384743+(0.00899911411679)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig_2018))                                                          
            CMS_zz4l_alpha_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.23329827124+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"(2.04575884495+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_2018))
            CMS_zz4l_alpha2_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"(1.84386824883+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"(2.98483993137+(0)*(@0-125))",RooArgList(MH))
            
        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_1_centralValue_2018,CMS_zz4l_sigma_sig_1_centralValue_2018,CMS_zz4l_alpha_1_centralValue_2018,CMS_zz4l_n_1_centralValue_2018,CMS_zz4l_alpha2_1_centralValue_2018,CMS_zz4l_n2_1_centralValue_2018)
	elif (year=='2017'):
	    CMS_zz4l_mean_sig_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year, \
                                                               "(124.82+(-0.000560694+1)*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_err_1_2017))

            CMS_zz4l_sigma_sig_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(1.16647+(0.0124833)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig_2017))    
    
	    CMS_zz4l_alpha_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.23329827124+(0)*(@0-125))",RooArgList(MH))    
            #CMS_zz4l_alpha_1_centralValue = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.22997+(0.00256332)*(@0-125))",RooArgList(MH))        
	    CMS_zz4l_n_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"(2.07185+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_2017))
            CMS_zz4l_alpha2_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"(1.92338+(0.0109082)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"(2.90336+(0)*(@0-125))",RooArgList(MH))
    
        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_1_centralValue_2017,CMS_zz4l_sigma_sig_1_centralValue_2017,CMS_zz4l_alpha_1_centralValue_2017,CMS_zz4l_n_1_centralValue_2017,CMS_zz4l_alpha2_1_centralValue_2017,CMS_zz4l_n2_1_centralValue_2017)
	else:
	    CMS_zz4l_mean_sig_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year, \
                                                               "(124.801+(-0.00230642+1)*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_err_1_2016))
    
            CMS_zz4l_sigma_sig_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(1.20385+(0.00862539)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig_2016))    
    
            CMS_zz4l_alpha_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.29006+(-0.0040219)*(@0-125))",RooArgList(MH))        
	    CMS_zz4l_n_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"(2.1216+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_2016))
            CMS_zz4l_alpha2_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"(1.90093+(-0.0017352)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"(2.7194+(0)*(@0-125))",RooArgList(MH))
    
        # true signal shape 
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_1_centralValue_2016,CMS_zz4l_sigma_sig_1_centralValue_2016,CMS_zz4l_alpha_1_centralValue_2016,CMS_zz4l_n_1_centralValue_2016,CMS_zz4l_alpha2_1_centralValue_2016,CMS_zz4l_n2_1_centralValue_2016) 
 
       
    # Wrong signal combination events

    if (year=='2018'):
        if (channel=='4mu'):
            p1_12018 = RooRealVar("CMS_fakeH_p1_1"+year,"p1_1"+year,165.0, 145.0, 185.0)       
            p3_12018 = RooRealVar("CMS_fakeH_p3_1"+year,"p3_1"+year,89.0, 84.0,94.0) 
            p2_12018 = RooFormulaVar("CMS_fakeH_p2_1"+year,"p2_1"+year,"0.72*@0-@1",RooArgList(p1_12018,p3_12018))         
            fakeH = RooLandau("fakeH", "landau", m, p1_12018, p2_12018)
        if (channel=='4e'):
            p1_22018 = RooRealVar("CMS_fakeH_p1_2"+year,"p1_2"+year,165.0, 145.0, 185.0)       
            p3_22018 = RooRealVar("CMS_fakeH_p3_2"+year,"p3_2"+year,89.0, 84.0,94.0) 
            p2_22018 = RooFormulaVar("CMS_fakeH_p2_2"+year,"p2_2"+year,"0.72*@0-@1",RooArgList(p1_22018,p3_22018))         
            fakeH = RooLandau("fakeH", "landau", m, p1_22018, p2_22018) 
        if (channel=='2e2mu'):
            p1_32018 = RooRealVar("CMS_fakeH_p1_3"+year,"p1_3"+year,165.0, 145.0, 185.0)       
            p3_32018 = RooRealVar("CMS_fakeH_p3_3"+year,"p3_3"+year,89.0, 84.0,94.0) 
            p2_32018 = RooFormulaVar("CMS_fakeH_p2_3"+year,"p2_3"+year,"0.72*@0-@1",RooArgList(p1_32018,p3_32018))         
            fakeH = RooLandau("fakeH", "landau", m, p1_32018, p2_32018) 
    elif (year=='2017'):
        if (channel=='4mu'):
            p1_12017 = RooRealVar("CMS_fakeH_p1_1"+year,"p1_1"+year,165.0, 145.0, 185.0)       
            p3_12017 = RooRealVar("CMS_fakeH_p3_1"+year,"p3_1"+year,89.0, 84.0,94.0) 
            p2_12017 = RooFormulaVar("CMS_fakeH_p2_1"+year,"p2_1"+year,"0.72*@0-@1",RooArgList(p1_12017,p3_12017))         
            fakeH = RooLandau("fakeH", "landau", m, p1_12017, p2_12017)
        if (channel=='4e'):
            p1_22017 = RooRealVar("CMS_fakeH_p1_2"+year,"p1_2"+year,165.0, 145.0, 185.0)       
            p3_22017 = RooRealVar("CMS_fakeH_p3_2"+year,"p3_2"+year,89.0, 84.0,94.0) 
            p2_22017 = RooFormulaVar("CMS_fakeH_p2_2"+year,"p2_2"+year,"0.72*@0-@1",RooArgList(p1_22017,p3_22017))         
            fakeH = RooLandau("fakeH", "landau", m, p1_22017, p2_22017) 
        if (channel=='2e2mu'):
            p1_32017 = RooRealVar("CMS_fakeH_p1_3"+year,"p1_3"+year,165.0, 145.0, 185.0)       
            p3_32017 = RooRealVar("CMS_fakeH_p3_3"+year,"p3_3"+year,89.0, 84.0,94.0) 
            p2_32017 = RooFormulaVar("CMS_fakeH_p2_3"+year,"p2_3"+year,"0.72*@0-@1",RooArgList(p1_32017,p3_32017))         
            fakeH = RooLandau("fakeH", "landau", m, p1_32017, p2_32017) 
    else:
        if (channel=='4mu'):
            p1_12016 = RooRealVar("CMS_fakeH_p1_1"+year,"p1_1"+year,165.0, 145.0, 185.0)       
            p3_12016 = RooRealVar("CMS_fakeH_p3_1"+year,"p3_1"+year,89.0, 84.0,94.0) 
            p2_12016 = RooFormulaVar("CMS_fakeH_p2_1"+year,"p2_1"+year,"0.72*@0-@1",RooArgList(p1_12016,p3_12016))         
            fakeH = RooLandau("fakeH", "landau", m, p1_12016, p2_12016)
        if (channel=='4e'):
            p1_22016 = RooRealVar("CMS_fakeH_p1_2"+year,"p1_2"+year,165.0, 145.0, 185.0)       
            p3_22016 = RooRealVar("CMS_fakeH_p3_2"+year,"p3_2"+year,89.0, 84.0,94.0) 
            p2_22016 = RooFormulaVar("CMS_fakeH_p2_2"+year,"p2_2"+year,"0.72*@0-@1",RooArgList(p1_22016,p3_22016))         
            fakeH = RooLandau("fakeH", "landau", m, p1_22016, p2_22016) 
        if (channel=='2e2mu'):
            p1_32016 = RooRealVar("CMS_fakeH_p1_3"+year,"p1_3"+year,165.0, 145.0, 185.0)       
            p3_32016 = RooRealVar("CMS_fakeH_p3_3"+year,"p3_3"+year,89.0, 84.0,94.0) 
            p2_32016 = RooFormulaVar("CMS_fakeH_p2_3"+year,"p2_3"+year,"0.72*@0-@1",RooArgList(p1_32016,p3_32016))         
            fakeH = RooLandau("fakeH", "landau", m, p1_32016, p2_32016) 


    if (addfakeH):
        inc_wrongfrac_ggH=inc_wrongfrac["ggH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_qqH=inc_wrongfrac["VBF_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_WH=inc_wrongfrac["WH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_ZH=inc_wrongfrac["ZH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_ttH=inc_wrongfrac["ttH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    else:
        inc_wrongfrac_ggH=0.0
        inc_wrongfrac_qqH=0.0
        inc_wrongfrac_WH=0.0
        inc_wrongfrac_ZH=0.0
        inc_wrongfrac_ttH=0.0

    binfrac_wrongfrac_ggH=binfrac_wrongfrac["ggH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_qqH=binfrac_wrongfrac["VBF_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_WH=binfrac_wrongfrac["WH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_ZH=binfrac_wrongfrac["ZH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_ttH=binfrac_wrongfrac["ttH_powheg_JHUgen_125_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    
    if (channel=='4e'):
        n_fakeH = (0.24*inc_wrongfrac_WH*binfrac_wrongfrac_WH+0.20*inc_wrongfrac_ZH*binfrac_wrongfrac_ZH+0.10*inc_wrongfrac_ttH*binfrac_wrongfrac_ttH)
    if (channel=='4mu'):
        n_fakeH = (0.45*inc_wrongfrac_WH*binfrac_wrongfrac_WH+0.38*inc_wrongfrac_ZH*binfrac_wrongfrac_ZH+0.20*inc_wrongfrac_ttH*binfrac_wrongfrac_ttH)
    if (channel=='2e2mu'):
        n_fakeH = (0.57*inc_wrongfrac_WH*binfrac_wrongfrac_WH+0.51*inc_wrongfrac_ZH*binfrac_wrongfrac_ZH+0.25*inc_wrongfrac_ttH*binfrac_wrongfrac_ttH)

    n_fakeH_var = RooRealVar("n_fakeH_var_"+recobin+"_"+channel+year,"n_fakeH_var_"+recobin+"_"+channel+year,n_fakeH);
    
    fakeH_norm = RooFormulaVar("fakeH_norm","@0",RooArgList(n_fakeH_var))

    # Out of acceptance events
    # (same shape as in acceptance shape)
    out_trueH = trueH.Clone()
    
    # signal shape in different recobin
    trueH_shape = {}
    fideff = {}
    fideff_var = {}
    trueH_norm = {}

    # nuisance describes the jet energy scale uncertainty
    #JES = RooRealVar("JES_"+year,"JES_"+year, 0, -5.0, 5.0)
    JES = RooRealVar("JES","JES", 0, -5.0, 5.0)    # FIXME, update with new recommendations
    #if (obsName == "nJets"  or ("jet" in obsName)):
    if (("jet" in obsName) or ("Jet" in obsName) or ("j1" in obsName) or ("j2" in obsName) or ("4lj" in obsName) or (doJES) ):
        lambda_JES_sig = lambdajesup[modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+""+"_"+recobin]
        lambda_JES_sig_var = RooRealVar("lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+""+"_"+recobin+"_"+year, "lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+""+"_"+recobin+"_"+year, lambda_JES_sig)    
        JES_sig_rfv = RooFormulaVar("JES_rfv_sig_"+recobin+"_"+channel+"_"+year,"@0*@1", RooArgList(JES, lambda_JES_sig_var) )

    for genbin in range(nBins-1):
        trueH_shape[genbin] = trueH.Clone();
        trueH_shape[genbin].SetName("trueH"+channel+"Bin"+str(genbin))
        if (usecfactor): fideff[genbin] = cfactor[modelName+"_"+channel+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
        else: fideff[genbin] = eff[modelName+"_"+channel+"_"+obsName+"_genbin"+str(genbin)+"_"+recobin]
#                                  `SM_125_2e2mu_pT4l_genbin8_recobin0
        fideff_var[genbin] = RooRealVar("effBin"+str(genbin)+"_"+recobin+"_"+channel+"_"+year,"effBin"+str(genbin)+"_"+recobin+"_"+channel+"_"+year, fideff[genbin]);

#        if( not (obsName=='nJets' or ("jet" in obsName)) or (not doJES)) :
	if ((not "jet" in obsName) or (not "Jet" in obsName) or (not "j1" in obsName) or (not "j2" in obsName) or (not "4lj" in obsName) or (not doJES) ):
            trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_var[genbin], lumi) );
        else :
            trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_var[genbin], lumi, JES_sig_rfv) ); 
 

    trueH_norm_final = {}
    fracBin = {}
    rBin = {}
    rBin_channel = {}
    fracSM4eBin = {}
    fracSM4muBin = {}
    K1Bin = {}
    K2Bin = {}
    SigmaBin = {}
    SigmaHBin = {}

    for genbin in range(nBins-1):

        if (physicalModel=="v3"):

            fidxs = {}
            for fState in ['4e','4mu', '2e2mu']:
                fidxs[fState] = 0
                #fidxs[fState] += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin'+str(genbin)]  # 125.38   ?
                fidxs[fState] += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin'+str(genbin)]  # 
                fidxs[fState] += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(genbin)+'_recobin'+str(genbin)]        
            fidxs['4l'] = fidxs['4e'] + fidxs['4mu'] + fidxs['2e2mu']
            
            fracSM4eBin[str(genbin)] = RooRealVar('fracSM4eBin'+str(genbin), 'fracSM4eBin'+str(genbin), fidxs['4e']/fidxs['4l'])
            fracSM4eBin[str(genbin)].setConstant(True)
            fracSM4muBin[str(genbin)] = RooRealVar('fracSM4muBin'+str(genbin), 'fracSM4muBin'+str(genbin), fidxs['4mu']/fidxs['4l'])
            fracSM4muBin[str(genbin)].setConstant(True)
            K1Bin[str(genbin)] = RooRealVar('K1Bin'+str(genbin), 'K1Bin'+str(genbin), 1.0, 0.0,  1.0/fracSM4eBin[str(genbin)].getVal())
            K2Bin[str(genbin)] = RooRealVar('K2Bin'+str(genbin), 'K2Bin'+str(genbin), 1.0, 0.0, (1.0-fracSM4eBin[str(genbin)].getVal())/fracSM4muBin[str(genbin)].getVal())
            SigmaBin[str(genbin)] = RooRealVar('SigmaBin'+str(genbin), 'SigmaBin'+str(genbin), fidxs['4l'], 0.0, 10.0)
            SigmaHBin['4e'+str(genbin)] = RooFormulaVar("Sigma4eBin"+str(genbin),"(@0*@1*@2)", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)]))
            SigmaHBin['4mu'+str(genbin)] = RooFormulaVar("Sigma4muBin"+str(genbin),"(@0*(1.0-@1*@2)*@3*@4/(1.0-@1))", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)], K2Bin[str(genbin)], fracSM4muBin[str(genbin)]))
            SigmaHBin['2e2mu'+str(genbin)] = RooFormulaVar("Sigma2e2muBin"+str(genbin),"(@0*(1.0-@1*@2)*(1.0-@3*@4/(1.0-@1)))", RooArgList(SigmaBin[str(genbin)], fracSM4eBin[str(genbin)], K1Bin[str(genbin)], K2Bin[str(genbin)], fracSM4muBin[str(genbin)]))

#            if (obsName == "nJets" or ("jet" in obsName)):
	    if (("jet" in obsName) or ("Jet" in obsName) or ("j1" in obsName) or ("j2" in obsName) or ("4lj" in obsName) or (doJES) ):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi))

        elif (physicalModel=="v2"):

            rBin_channel[str(genbin)] = RooRealVar("r"+channel+"Bin"+str(genbin),"r"+channel+"Bin"+str(genbin), 1.0, 0.0, 10.0)                
            rBin_channel[str(genbin)].setConstant(True)

#            if (obsName == "nJets" or ("jet" in obsName)):
	    if (("jet" in obsName) or ("Jet" in obsName) or ("j1" in obsName) or ("j2" in obsName) or ("4lj" in obsName) or (doJES) ):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi))
                                                                                                                                                            

    outin = outinratio[modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+"_"+recobin]
    print "outin",obsBin,outin
    outin_var = RooRealVar("outfracBin_"+recobin+"_"+channel,"outfracBin_"+recobin+"_"+channel+"_"+year, outin);
    outin_var.setConstant(True)
    out_trueH_norm_args = RooArgList(outin_var)
    out_trueH_norm_func = "@0*(" 
    for i in range(nBins-1): 
        out_trueH_norm_args.add(trueH_norm_final[i]) 
        out_trueH_norm_func = out_trueH_norm_func+"@"+str(i+1)+"+" 
    out_trueH_norm_func = out_trueH_norm_func.replace(str(nBins-1)+"+",str(nBins-1)+")") 
    out_trueH_norm = RooFormulaVar("out_trueH_norm",out_trueH_norm_func,out_trueH_norm_args) 
                                                                                              
    # Backgrounds
    
    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = {'qqzz':{'2e2mu':'ZZTo2e2mu_powheg', '4e':'ZZTo4e_powheg', '4mu':'ZZTo4mu_powheg'},'ggzz':{'2e2mu':'ggZZ_2e2mu_MCFM67', '4e':'ggZZ_4e_MCFM67', '4mu':'ggZZ_4mu_MCFM67'},'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}} 
    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][channel]+'_'+channel+'_'+obsName+'_'+recobin]
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+recobin+"_"+channel+"_"+year,"frac_qqzz_"+recobin+"_"+channel+"_"+year, frac_qqzz);

    frac_ggzz = fractionsBackground[bkg_sample_tags['ggzz'][channel]+'_'+channel+'_'+obsName+'_'+recobin]
    frac_ggzz_var = RooRealVar("frac_ggzz_"+recobin+"_"+channel+"_"+year,"frac_ggzz_"+recobin+"_"+channel+"_"+year, frac_ggzz);

    print fractionsBackground
    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][channel]+"_AllChans_"+obsName+'_'+recobin]
    frac_zjets_var = RooRealVar("frac_zjet_"+recobin+"_"+channel+"_"+year,"frac_zjet_"+recobin+"_"+channel+"_"+year, frac_zjets);

    print obsBin,"frac_qqzz",frac_qqzz,"frac_ggzz",frac_ggzz,"frac_zjets",frac_zjets

#    if (obsName=="nJets" or ("jet" in obsName)):
    if (("jet" in obsName) or ("Jet" in obsName) or ("j1" in obsName) or ("j2" in obsName) or ("4lj" in obsName) or (doJES) ):
        ####
        lambda_JES_qqzz = 0.0 #lambda_qqzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_qqzz_var = RooRealVar("lambda_qqzz_"+recobin+"_"+channel+"_"+year,"lambda_"+recobin+"_"+channel+"_"+year, lambda_JES_qqzz)           
        JES_qqzz_rfv = RooFormulaVar("JES_rfv_qqzz_"+recobin+"_"+channel+"_"+year,"@0*@1", RooArgList(JES, lambda_JES_qqzz_var) )

        ####
        lambda_JES_ggzz = 0.0 #lambda_ggzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_ggzz_var = RooRealVar("lambda_ggzz_"+recobin+"_"+channel+"_"+year,"lambda_"+recobin+"_"+channel+"_"+year, lambda_JES_ggzz)
        JES_ggzz_rfv = RooFormulaVar("JES_rfv_ggzz_"+recobin+"_"+channel+"_"+year,"@0*@1", RooArgList(JES, lambda_JES_ggzz_var) )

        ####
        lambda_JES_zjets = 0.0 #lambda_zjets_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_zjets_var = RooRealVar("lambda_zjets_"+recobin+"_"+channel+"_"+year,"lambda_zjets_"+recobin+"_"+channel+"_"+year, lambda_JES_zjets)
        JES_zjets_rfv = RooFormulaVar("JES_rfv_zjets_"+recobin+"_"+channel+"_"+year,"@0*@1", RooArgList(JES, lambda_JES_zjets_var) )


    ## background shapes in each reco bin

    #template_qqzzName = "./templates/templatesXS/DTreeXS_"+obsName+"/13TeV/XSBackground_qqZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_qqzzName = "./templates_"+year+"/templatesXS/DTreeXS_"+obsName+"/13TeV/XSBackground_qqZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    template_ggzzName = "./templates_"+year+"/templatesXS/DTreeXS_"+obsName+"/13TeV/XSBackground_ggZZ_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    if (not obsName=="mass4l"):
        template_zjetsName = "./templates_"+year+"/templatesXS/DTreeXS_"+obsName+"/13TeV/XSBackground_ZJetsCR_AllChans_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"
    else:
        template_zjetsName = "./templates_"+year+"/templatesXS/DTreeXS_"+obsName+"/13TeV/XSBackground_ZJetsCR_"+channel+"_"+obsName+"_"+obsBin_low+"_"+obsBin_high+".root"

    qqzzTempFile = TFile(template_qqzzName,"READ")
    qqzzTemplate = qqzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    print 'year is ..', year
    print 'qqZZ bins',qqzzTemplate.GetNbinsX(),qqzzTemplate.GetBinLowEdge(1),qqzzTemplate.GetBinLowEdge(qqzzTemplate.GetNbinsX()+1)

    ggzzTempFile = TFile(template_ggzzName,"READ")
    ggzzTemplate = ggzzTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    print 'ggZZ bins',ggzzTemplate.GetNbinsX(),ggzzTemplate.GetBinLowEdge(1),ggzzTemplate.GetBinLowEdge(ggzzTemplate.GetNbinsX()+1)

    zjetsTempFile = TFile(template_zjetsName,"READ")
    zjetsTemplate = zjetsTempFile.Get("m4l_"+obsName+"_"+obsBin_low+"_"+obsBin_high)
    print 'zjets bins',zjetsTemplate.GetNbinsX(),zjetsTemplate.GetBinLowEdge(1),zjetsTemplate.GetBinLowEdge(zjetsTemplate.GetNbinsX()+1)

    binscale = 3
    qqzzTemplateNew = TH1F("qqzzTemplateNew","qqzzTemplateNew",binscale*qqzzTemplate.GetNbinsX(),qqzzTemplate.GetBinLowEdge(1),qqzzTemplate.GetBinLowEdge(qqzzTemplate.GetNbinsX()+1))
    for i in range(1,qqzzTemplate.GetNbinsX()+1):        
        for j in range(binscale):
            qqzzTemplateNew.SetBinContent((i-1)*binscale+j+1,qqzzTemplate.GetBinContent(i)/binscale)
    ggzzTemplateNew = TH1F("ggzzTemplateNew","ggzzTemplateNew",binscale*ggzzTemplate.GetNbinsX(),ggzzTemplate.GetBinLowEdge(1),ggzzTemplate.GetBinLowEdge(ggzzTemplate.GetNbinsX()+1))
    for i in range(1,ggzzTemplate.GetNbinsX()+1):        
        for j in range(binscale):
            ggzzTemplateNew.SetBinContent((i-1)*binscale+j+1,ggzzTemplate.GetBinContent(i)/binscale)
    zjetsTemplateNew = TH1F("zjetsTemplateNew","zjetsTemplateNew",binscale*zjetsTemplate.GetNbinsX(),zjetsTemplate.GetBinLowEdge(1),zjetsTemplate.GetBinLowEdge(zjetsTemplate.GetNbinsX()+1))
    for i in range(1,zjetsTemplate.GetNbinsX()+1):        
        for j in range(binscale):
            zjetsTemplateNew.SetBinContent((i-1)*binscale+j+1,zjetsTemplate.GetBinContent(i)/binscale)

    qqzzTemplateName = "qqzz_"+channel+recobin+year
    ggzzTemplateName = "ggzz_"+channel+recobin+year
    zjetsTemplateName = "zjets_"+channel+recobin+year

    qqzzTempDataHist = RooDataHist(qqzzTemplateName,qqzzTemplateName,RooArgList(m),qqzzTemplateNew)
    ggzzTempDataHist = RooDataHist(ggzzTemplateName,ggzzTemplateName,RooArgList(m),ggzzTemplateNew)
    zjetsTempDataHist = RooDataHist(zjetsTemplateName,zjetsTemplateName,RooArgList(m),zjetsTemplateNew)

    qqzzTemplatePdf = RooHistPdf("qqzz","qqzz",RooArgSet(m),qqzzTempDataHist)
    ggzzTemplatePdf = RooHistPdf("ggzz","ggzz",RooArgSet(m),ggzzTempDataHist)
    zjetsTemplatePdf = RooHistPdf("zjets","zjets",RooArgSet(m),zjetsTempDataHist)

    # bkg fractions in reco bin; implemented in terms of fractions
#    if( not (obsName=='nJets' or ("jet" in obsName) ) or (not doJES)) :
    if ((not "jet" in obsName) or (not "Jet" in obsName) or (not "j1" in obsName) or (not "j2" in obsName) or (not "4lj" in obsName) or (not doJES) ):
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0", RooArgList(frac_ggzz_var) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )
    else :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0*(1-@1)", RooArgList(frac_qqzz_var, JES_qqzz_rfv) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0*(1-@1)", RooArgList(frac_ggzz_var, JES_ggzz_rfv) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0*(1-@1)", RooArgList(frac_zjets_var, JES_zjets_rfv) )
     

#    data_obs_file = TFile('data_13TeV_2018.root')  # David PAS
    #if (year=="2018"): data_obs_file = TFile('data_13TeV_2018_Jun05.root')   #  
    if (year=="2018"): data_obs_file = TFile(tmpSrcDir+'/'+background_samples_2018['ZX4l_CR'])    
    elif (year=="2017"): data_obs_file = TFile(tmpSrcDir+'/'+background_samples_2017['ZX4l_CR'])    
    else: data_obs_file = TFile(tmpSrcDir+'/'+background_samples_2016['ZX4l_CR']) # 
    print "data file: ", data_obs_file
    data_obs_tree = data_obs_file.Get('passedEvents')
    
    print obsName,obsBin_low,obsBin_high
    if (obsName == "nJets"): obsName = "njets_reco_pt30_eta4p7"
    if (channel=='4mu'):
        if (obsName.startswith("mass4l")): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu),"(mass4mu>105.0 && mass4mu<140.0)")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>105.0 && mass4mu<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>105.0 && mass4mu<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+")")
    if (channel=='4e'):
        if (obsName.startswith("mass4l")): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e),"(mass4e>105.0 && mass4e<140.0)")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>105.0 && mass4e<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>105.0 && mass4e<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+")")
    if (channel=='2e2mu'):
        if (obsName.startswith("mass4l")): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu),"(mass2e2mu>105.0 && mass2e2mu<140.0)")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>105.0 && mass2e2mu<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>105.0 && mass2e2mu<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+")") 

    
    wout = RooWorkspace("w","w")


    if (year=="2018"):
        if (channel=='2e2mu'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_3_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_3_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_3_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_3_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_3_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_3_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_m_err_3_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_e_err_3_2018,RooFit.RecycleConflictNodes())
        if (channel=='4e'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_2_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_2_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_2_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_2_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_2_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_2_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_e_err_2_2018,RooFit.RecycleConflictNodes())
        if (channel=='4mu'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_1_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_1_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_1_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_1_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_1_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_1_centralValue_2018,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_m_err_1_2018,RooFit.RecycleConflictNodes())
    elif (year=="2017"):
        if (channel=='2e2mu'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_3_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_3_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_3_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_3_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_3_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_3_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_m_err_3_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_e_err_3_2017,RooFit.RecycleConflictNodes())
        if (channel=='4e'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_2_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_2_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_2_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_2_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_2_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_2_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_e_err_2_2017,RooFit.RecycleConflictNodes())
        if (channel=='4mu'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_1_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_1_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_1_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_1_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_1_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_1_centralValue_2017,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_m_err_1_2017,RooFit.RecycleConflictNodes())
    else:
        if (channel=='2e2mu'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_3_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_3_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_3_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_3_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_3_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_3_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_m_err_3_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_e_err_3_2016,RooFit.RecycleConflictNodes())
        if (channel=='4e'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_2_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_2_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_2_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_2_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_2_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_2_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_e_err_2_2016,RooFit.RecycleConflictNodes())
        if (channel=='4mu'):
            getattr(wout,'import')(CMS_zz4l_mean_sig_1_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_sigma_sig_1_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha_1_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n_1_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_alpha2_1_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_n2_1_centralValue_2016,RooFit.RecycleConflictNodes())
            getattr(wout,'import')(CMS_zz4l_mean_m_err_1_2016,RooFit.RecycleConflictNodes())
                



    for genbin in range(nBins-1):
        getattr(wout,'import')(trueH_shape[genbin],RooFit.RecycleConflictNodes(),RooFit.Silence())
        getattr(wout,'import')(trueH_norm[genbin],RooFit.RecycleConflictNodes(),RooFit.Silence())

    if (not usecfactor):
        out_trueH.SetName("out_trueH")  
        getattr(wout,'import')(out_trueH,RooFit.RecycleConflictNodes(),RooFit.Silence()) 
        getattr(wout,'import')(out_trueH_norm,RooFit.RecycleConflictNodes(),RooFit.Silence()) 
    
    getattr(wout,'import')(fakeH,RooFit.Silence()) 
    getattr(wout,'import')(fakeH_norm,RooFit.Silence())
    
    qqzzTemplatePdf.SetName("bkg_qqzz")
    qqzzTemplatePdf.Print("v")    
    getattr(wout,'import')(qqzzTemplatePdf,RooFit.RecycleConflictNodes(), RooFit.Silence())
    getattr(wout,'import')(qqzz_norm,RooFit.Silence())

    ggzzTemplatePdf.SetName("bkg_ggzz")
    ggzzTemplatePdf.Print("v")
    getattr(wout,'import')(ggzzTemplatePdf,RooFit.RecycleConflictNodes())
    getattr(wout,'import')(ggzz_norm,RooFit.Silence())

    zjetsTemplatePdf.SetName("bkg_zjets")
    zjetsTemplatePdf.Print("v")
    getattr(wout,'import')(zjetsTemplatePdf, RooFit.RecycleConflictNodes(), RooFit.Silence())
    getattr(wout,'import')(zjets_norm,RooFit.Silence())

    ## data
    getattr(wout,'import')(data_obs.reduce(RooArgSet(m)),RooFit.Silence())

    if (addfakeH):
        if (usecfactor):
            #fout = TFile("xs_125.0/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.root","RECREATE")
            fout = TFile("xs_125.0_"+year+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.root","RECREATE")
        else:
            fout = TFile("xs_125.0_"+year+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".root","RECREATE")
    else:
        if (usecfactor):
            fout = TFile("xs_125.0_"+year+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.NoFakeH.root","RECREATE")
        else:
            fout = TFile("xs_125.0_"+year+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+".NoFakeH.root","RECREATE")

    print "write ws to fout"
    fout.WriteTObject(wout) 
    fout.Close()

    return data_obs.numEntries()

#createXSworkspace("pT4l", "2e2mu", 4, 0, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 1, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 2, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 3, False, True)
#createXSworkspace("mass4l", "2e2mu", 2, 0, ["105.0","140.0"], False, True, "ggH_powheg_JHUgen_125", "v2","2018")
