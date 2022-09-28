# this script is called once for each reco bin (obsBin)
# in each reco bin there are (nBins) signals (one for each gen bin)

import os
import sys

from ROOT import *
import ROOT

# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from Utils import  logger
import logging

logger.setLevel(logging.DEBUG)

sys.path.append('./'+datacardInputs)
m4l_bins = INPUT_m4l_bins
m4l_low = INPUT_m4l_low
m4l_high = INPUT_m4l_high

# FIXME: This is temporary bool. If we are running with LLR template keep it True.
ifLLR = False

def createXSworkspace(obsName, channel, nBins, obsBin, observableBins, usecfactor, addfakeH, modelName, physicalModel, year, obs_ifJES, obs_ifJES2, obs_ifAbs, obs_ifAbs2, zzFloatType = ''):
    """Create workspace
    this script is called once for each reco bin (obsBin)
    in each reco bin there are (nBins) signals (one for each gen bin)

    Args:
        obsName (str): Name of observable
        channel (str): Name of channel. For example 4e, 4mu, 2e2mu
        nBins (int): Number of bins
        obsBin (int): _description_
        observableBins (array): Array having all bin boundaries
        usecfactor (bool): _description_
        addfakeH (bool): _description_
        modelName (str): Name of model. For example "SM_125"
        physicalModel (str): physical model. For example: "v2"
    """
    global combineOutputs, ifLLR
    logger.info("""Input arguments to createXSworkspace module:
        obsName: {obsName}
        obsType: {obsType}
        channel: {channel}
        nBins: {nBins}
        obsBin: {obsBin}
        observableBins: {observableBins}
        usecfactor: {usecfactor}
        addfakeH: {addfakeH}
        modelName: {modelName}
        physicalModel: {physicalModel}""".format(
            obsName = obsName,
            obsType = type(obsName),
            channel = channel,
            nBins = nBins,
            obsBin = obsBin,
            observableBins = observableBins,
            usecfactor = usecfactor,
            addfakeH = addfakeH,
            modelName = modelName,
            physicalModel = physicalModel
        ))
    is2DObs = False
    obsNameOrig = obsName   # Save original list into new variable
    obsName = obsName[0]    # get first observable to be used for both 1D or 2D
    obsNameDictKey = obsName    # This saves key for 1D, if 2D update the key to be searched from dict
    if len(obsNameOrig)>1:
        is2DObs = True
        logger.info("This is recognised as 2D observable...")
        obsNameDictKey = obsNameOrig[0]+'_vs_'+obsNameOrig[1]   # Update the dict key
        logger.debug("observable bin - {} - : {}".format(obsBin, observableBins[obsBin]))

        obsBin_low = observableBins[obsBin][0][0]
        obsBin_high = observableBins[obsBin][0][1]

        obs_bin_lowest   =  min(observableBins[obsBin][0])
        obs_bin_highest =  max(observableBins[obsBin][0])

        recobin = "recobin"+str(obsBin)
        logger.debug("""
                (obsBin_low,  obsBin_high ) = ({},{});
                (obs_bin_lowest,  obs_bin_highest ) = ({}, {})""".format(
                    obsBin_low, obsBin_high, obs_bin_lowest, obs_bin_highest
                    ))
        SuffixOfRootFile = obsNameOrig[0]+"_"+obsBin_low+"_"+obsBin_high
        if (ifLLR): SuffixOfRootFile = SuffixOfRootFile.replace("ZZ","zz").replace(".0","")
        logger.debug("SuffixOfRootFile: {}".format(SuffixOfRootFile))

        obsBin_low2 = observableBins[obsBin][1][0]
        obsBin_high2 = observableBins[obsBin][1][1]

        obs_bin_lowest2 = min(observableBins[obsBin][1])
        obs_bin_highest2 = max(observableBins[obsBin][1])
        logger.debug("""
                (obsBin_low2, obsBin_high2) = ({},{});
                (obs_bin_lowest2, obs_bin_highest2) = ({}, {})""".format(
                    obsBin_low2, obsBin_high2, obs_bin_lowest2, obs_bin_highest2
                    ))
        SuffixOfRootFile = SuffixOfRootFile + '_' + obsNameOrig[1] + "_" + obsBin_low2 + "_" + obsBin_high2
        if (ifLLR): SuffixOfRootFile = SuffixOfRootFile.replace("ZZ","zz").replace(".0","")
        logger.debug("SuffixOfRootFile: {}".format(SuffixOfRootFile))
    else:
        logger.info("This is recognised as 1D observable...")
        # obsNameOrig = obsName
        obsBin_low = observableBins[obsBin]
        obsBin_high = observableBins[obsBin+1]
        if obsBin_high == 'inf':
            obsBin_high_inf = 10000
        else:
            obsBin_high_inf = obsBin_high

        obs_bin_lowest = observableBins[0]
        obs_bin_highest = observableBins[len(observableBins)-1]

        recobin = "recobin"+str(obsBin)
        logger.debug("""
                (obsBin_low,  obsBin_high ) = ({},{});
                (obs_bin_lowest,  obs_bin_highest ) = ({}, {})""".format(
                    obsBin_low, obsBin_high, obs_bin_lowest, obs_bin_highest
                    ))
        SuffixOfRootFile = obsNameOrig[0]+"_"+obsBin_low+"_"+obsBin_high
        if (ifLLR): SuffixOfRootFile = SuffixOfRootFile.replace("ZZ","zz").replace(".0","")
        logger.info("SuffixOfRootFile: {}".format(SuffixOfRootFile))

    # print "workspace: working path is:      ",os.getcwd()
    # obsBin_low = observableBins[obsBin]
    # obsBin_high = observableBins[obsBin+1]

    # obs_bin_lowest = observableBins[0]
    # obs_bin_highest = observableBins[len(observableBins)-1]

    # recobin = "recobin"+str(obsBin)

    doJES = 0

    # Load some libraries
    gSystem.AddIncludePath("-I$CMSSW_BASE/src/")
    gSystem.Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
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
        ModuleToImport = 'inputs_sig_'+obsNameDictKey
        logger.debug("Module to import: "+ModuleToImport)
        _temp = __import__(ModuleToImport, globals(), locals(), ['acc','eff','inc_wrongfrac','binfrac_wrongfrac','outinratio','lambdajesup','lambdajesdn'], -1)

        acc = _temp.acc
        eff = _temp.eff
        outinratio = _temp.outinratio

    lambdajesup = _temp.lambdajesup
    lambdajesdn = _temp.lambdajesdn
    inc_wrongfrac = _temp.inc_wrongfrac
    binfrac_wrongfrac = _temp.binfrac_wrongfrac

    #from inputs_bkg_{obsName} import fractionsBackground
    ModuleToImport = 'inputs_bkg_'+obsNameDictKey
    logger.debug("Module to import: "+ModuleToImport)
    _temp = __import__(ModuleToImport, globals(), locals(), ['fractionsBackground'], -1)
    fractionsBackground = _temp.fractionsBackground

    # import h4l xs br
    _temp = __import__('higgs_xsbr_13TeV', globals(), locals(), ['higgs_xs','higgs4l_br'], -1)
    higgs_xs = _temp.higgs_xs
    higgs4l_br = _temp.higgs4l_br

    # 4 lepton mass observable to perform the fit
    m = RooRealVar("CMS_zz4l_mass", "CMS_zz4l_mass", m4l_low, m4l_high)
    logger.info("m.numBins(): {}".format(m.numBins()))

    mass4e = RooRealVar("mass4e", "mass4e", m4l_low, m4l_high)
    mass4mu = RooRealVar("mass4mu", "mass4mu", m4l_low, m4l_high)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",m4l_low, m4l_high)

    
    if (not obsName=="mass4l"):
	logger.debug("obs_ifAbs = {}".format(obs_ifAbs))
	if obs_ifAbs:
	    observable = RooRealVar(obsName,obsName,-1.0*float(obs_bin_highest),float(obs_bin_highest)) 
	else:
	    observable   = RooRealVar(obsName,obsName,float(obs_bin_lowest),float(obs_bin_highest))
        observable.Print()
        if is2DObs:
            observable2 = RooRealVar(obsNameOrig[1],obsNameOrig[1],float(obs_bin_lowest2),float(obs_bin_highest2))
            observable2.Print()

    # luminosity
    lumi = RooRealVar("lumi_13"+str(year),"lumi_13"+str(year), 0.0)
    if (str(year) == "2018"): lumi = RooRealVar("lumi_13"+str(year),"lumi_13"+str(year), Lumi_2018)
    if (str(year) == "2017"): lumi = RooRealVar("lumi_13"+str(year),"lumi_13"+str(year),  Lumi_2017)
    if (str(year) == "2016"): lumi = RooRealVar("lumi_13"+str(year),"lumi_13"+str(year), Lumi_2016)
    if (str(year) == "allYear"): lumi = RooRealVar("lumi_13"+str(year),"lumi_13"+str(year), Lumi_Run2)

    # update to 13 TeV parameterization
    MH = RooRealVar("MH","MH", 125.38,  m4l_low, m4l_high) # Hardcoded mass


    if (year=='2018'):
        # CMS_zz4l_mean_m_sig_2018 = RooRealVar("CMS_zz4l_mean_m_sig_"+year,"CMS_zz4l_mean_m_sig_"+year,0.0)
        # CMS_zz4l_mean_e_sig_2018 = RooRealVar("CMS_zz4l_mean_e_sig_"+year,"CMS_zz4l_mean_e_sig_"+year,0.0)
        # CMS_zz4l_sigma_m_sig_2018 = RooRealVar("CMS_zz4l_sigma_m_sig_"+year,"CMS_zz4l_sigma_m_sig_"+year,0.0)
        # CMS_zz4l_sigma_e_sig_2018 = RooRealVar("CMS_zz4l_sigma_e_sig_"+year,"CMS_zz4l_sigma_e_sig_"+year,0.0)

        CMS_zz4l_mean_m_sig_2018 = RooRealVar("CMS_zz4l_mean_m_sig","CMS_zz4l_mean_m_sig",0.0)
        CMS_zz4l_mean_e_sig_2018 = RooRealVar("CMS_zz4l_mean_e_sig","CMS_zz4l_mean_e_sig",0.0)
        CMS_zz4l_sigma_m_sig_2018 = RooRealVar("CMS_zz4l_sigma_m_sig","CMS_zz4l_sigma_m_sig",0.0)
        CMS_zz4l_sigma_e_sig_2018 = RooRealVar("CMS_zz4l_sigma_e_sig","CMS_zz4l_sigma_e_sig",0.0)
        CMS_zz4l_n_sig_1_2018 = RooRealVar("CMS_zz4l_n_sig_1_"+year,"CMS_zz4l_n_sig_1_"+year,0.0)
        CMS_zz4l_n_sig_2_2018 = RooRealVar("CMS_zz4l_n_sig_2_"+year,"CMS_zz4l_n_sig_2_"+year,0.0)
        CMS_zz4l_n_sig_3_2018 = RooRealVar("CMS_zz4l_n_sig_3_"+year,"CMS_zz4l_n_sig_3_"+year,0.0)

        # scale systematics
        CMS_zz4l_mean_m_err_1_2018 = RooRealVar("CMS_zz4l_mean_m_err_1_"+year,"CMS_zz4l_mean_m_err_1_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_2_2018 = RooRealVar("CMS_zz4l_mean_e_err_2_"+year,"CMS_zz4l_mean_e_err_2_"+year,0.003,0.003,0.003)
        CMS_zz4l_mean_m_err_3_2018 = RooRealVar("CMS_zz4l_mean_m_err_3_"+year,"CMS_zz4l_mean_m_err_3_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_3_2018 = RooRealVar("CMS_zz4l_mean_e_err_3_"+year,"CMS_zz4l_mean_e_err_3_"+year,0.003,0.003,0.003)

    elif (year=='2017'):
        # CMS_zz4l_mean_m_sig_2017 = RooRealVar("CMS_zz4l_mean_m_sig_"+year,"CMS_zz4l_mean_m_sig_"+year,0.0)
        # CMS_zz4l_mean_e_sig_2017 = RooRealVar("CMS_zz4l_mean_e_sig_"+year,"CMS_zz4l_mean_e_sig_"+year,0.0)
        # CMS_zz4l_sigma_m_sig_2017 = RooRealVar("CMS_zz4l_sigma_m_sig_"+year,"CMS_zz4l_sigma_m_sig_"+year,0.0)
        # CMS_zz4l_sigma_e_sig_2017 = RooRealVar("CMS_zz4l_sigma_e_sig_"+year,"CMS_zz4l_sigma_e_sig_"+year,0.0)

        CMS_zz4l_mean_m_sig_2017 = RooRealVar("CMS_zz4l_mean_m_sig","CMS_zz4l_mean_m_sig", -10, 10)
        CMS_zz4l_mean_e_sig_2017 = RooRealVar("CMS_zz4l_mean_e_sig","CMS_zz4l_mean_e_sig", -10, 10)
        CMS_zz4l_sigma_m_sig_2017 = RooRealVar("CMS_zz4l_sigma_m_sig","CMS_zz4l_sigma_m_sig", -10, 10)
        CMS_zz4l_sigma_e_sig_2017 = RooRealVar("CMS_zz4l_sigma_e_sig","CMS_zz4l_sigma_e_sig", -10, 10)
        CMS_zz4l_n_sig_1_2017 = RooRealVar("CMS_zz4l_n_sig_1_"+year,"CMS_zz4l_n_sig_1_"+year, -10, 10)
        CMS_zz4l_n_sig_2_2017 = RooRealVar("CMS_zz4l_n_sig_2_"+year,"CMS_zz4l_n_sig_2_"+year, -10, 10)
        CMS_zz4l_n_sig_3_2017 = RooRealVar("CMS_zz4l_n_sig_3_"+year,"CMS_zz4l_n_sig_3_"+year, -10, 10)

        # scale systematics
        CMS_zz4l_mean_m_err_1_2017 = RooRealVar("CMS_zz4l_mean_m_err_1_"+year,"CMS_zz4l_mean_m_err_1_"+year,0.0001,0.0001,0.0001)
        CMS_zz4l_mean_e_err_2_2017 = RooRealVar("CMS_zz4l_mean_e_err_2_"+year,"CMS_zz4l_mean_e_err_2_"+year,0.006,0.006,0.006)
        CMS_zz4l_mean_m_err_3_2017 = RooRealVar("CMS_zz4l_mean_m_err_3_"+year,"CMS_zz4l_mean_m_err_3_"+year,0.0004,0.0004,0.0004)
        CMS_zz4l_mean_e_err_3_2017 = RooRealVar("CMS_zz4l_mean_e_err_3_"+year,"CMS_zz4l_mean_e_err_3_"+year,0.003,0.003,0.003)

    else:
        # CMS_zz4l_mean_m_sig_2016 = RooRealVar("CMS_zz4l_mean_m_sig_"+year,"CMS_zz4l_mean_m_sig_"+year,0.0)
        # CMS_zz4l_mean_e_sig_2016 = RooRealVar("CMS_zz4l_mean_e_sig_"+year,"CMS_zz4l_mean_e_sig_"+year,0.0)
        # CMS_zz4l_sigma_m_sig_2016 = RooRealVar("CMS_zz4l_sigma_m_sig_"+year,"CMS_zz4l_sigma_m_sig_"+year,0.0)
        # CMS_zz4l_sigma_e_sig_2016 = RooRealVar("CMS_zz4l_sigma_e_sig_"+year,"CMS_zz4l_sigma_e_sig_"+year,0.0)
        CMS_zz4l_mean_m_sig_2016 = RooRealVar("CMS_zz4l_mean_m_sig","CMS_zz4l_mean_m_sig",0.0)
        CMS_zz4l_mean_e_sig_2016 = RooRealVar("CMS_zz4l_mean_e_sig","CMS_zz4l_mean_e_sig",0.0)
        CMS_zz4l_sigma_m_sig_2016 = RooRealVar("CMS_zz4l_sigma_m_sig","CMS_zz4l_sigma_m_sig",0.0)
        CMS_zz4l_sigma_e_sig_2016 = RooRealVar("CMS_zz4l_sigma_e_sig","CMS_zz4l_sigma_e_sig",0.0)
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
                                                        "(124.512392+0.99361*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                        RooArgList(MH,CMS_zz4l_mean_m_sig_2018,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_err_3_2018,CMS_zz4l_mean_e_err_3_2018))

            CMS_zz4l_sigma_sig_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year, \
                                                        "(1.705306+0.00948*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_sigma_e_sig_2018))

            CMS_zz4l_alpha_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"(1.000696+0.00411*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_centralValue_2018 = RooFormulaVar("CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"(3.284378+(-0.06518)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_2018))


            CMS_zz4l_alpha2_3_centralValue_2018=RooFormulaVar("CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"(1.782321+(-0.00321)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_centralValue_2018=RooFormulaVar("CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"(3.600091+0.01133*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_3_centralValue_2018,CMS_zz4l_sigma_sig_3_centralValue_2018,CMS_zz4l_alpha_3_centralValue_2018,CMS_zz4l_n_3_centralValue_2018,CMS_zz4l_alpha2_3_centralValue_2018,CMS_zz4l_n2_3_centralValue_2018)
        elif (year=='2017'):
            CMS_zz4l_mean_sig_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year, \
                                                                "(124.499189+0.99550*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                                RooArgList(MH,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_m_err_3_2017,CMS_zz4l_mean_e_err_3_2017))

            CMS_zz4l_sigma_sig_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,\
                                                                "(1.679486+0.00442*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_e_sig_2017))

            CMS_zz4l_alpha_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"(1.000032+(-0.00336)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"(3.086201+(-0.01446)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_2017))
            CMS_zz4l_alpha2_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"(1.771256+(-0.01493)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_centralValue_2017 = RooFormulaVar("CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"(3.639008+0.04508*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_3_centralValue_2017,CMS_zz4l_sigma_sig_3_centralValue_2017,CMS_zz4l_alpha_3_centralValue_2017,CMS_zz4l_n_3_centralValue_2017,CMS_zz4l_alpha2_3_centralValue_2017,CMS_zz4l_n2_3_centralValue_2017)
        else:
            CMS_zz4l_mean_sig_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_3_centralValue_"+channel+recobin+year, \
                                                                "(124.508178+1.00243*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                                RooArgList(MH,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_m_err_3_2016,CMS_zz4l_mean_e_err_3_2016))

            CMS_zz4l_sigma_sig_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_3_centralValue_"+channel+recobin+year,\
                                                                "(1.656564+0.00626*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_e_sig_2016))
            CMS_zz4l_alpha_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_3_centralValue_"+channel+recobin+year,"(1.000108+(-0.01268)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n_3_centralValue_"+channel+recobin+year,"(2.960266+0.05011*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_2016))
            CMS_zz4l_alpha2_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_3_centralValue_"+channel+recobin+year,"(1.732230+0.00577*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_centralValue_2016 = RooFormulaVar("CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_3_centralValue_"+channel+recobin+year,"(3.798668+(-0.02313)*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_3_centralValue_2016,CMS_zz4l_sigma_sig_3_centralValue_2016,CMS_zz4l_alpha_3_centralValue_2016,CMS_zz4l_n_3_centralValue_2016,CMS_zz4l_alpha2_3_centralValue_2016,CMS_zz4l_n2_3_centralValue_2016)

    if (channel=='4e'):
        if (year=='2018'):
            CMS_zz4l_mean_sig_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(124.122309+0.99150*(@0-125)) + @0*@1*@2", \
                                                                RooArgList(MH,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_e_err_2_2018))

            CMS_zz4l_sigma_sig_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(2.228662+0.01068*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig_2018))

            CMS_zz4l_alpha_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"(1.000000+0.00386*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"(3.791876+(-0.07482)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_2018))
            CMS_zz4l_alpha2_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"(1.907851+(-0.00946)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_centralValue_2018 = RooFormulaVar("CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"(3.717134+0.09005*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_2_centralValue_2018,CMS_zz4l_sigma_sig_2_centralValue_2018,CMS_zz4l_alpha_2_centralValue_2018,CMS_zz4l_n_2_centralValue_2018,CMS_zz4l_alpha2_2_centralValue_2018,CMS_zz4l_n2_2_centralValue_2018)
        elif (year=='2017'):
            CMS_zz4l_mean_sig_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(124.034512+0.99869*(@0-125)) + @0*@1*@2", \
                                                                RooArgList(MH,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_err_2_2017))

            CMS_zz4l_sigma_sig_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(2.236452+0.00453*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig_2017))

            CMS_zz4l_alpha_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"(1.000001+(-0.01453)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"(3.647217+0.09608*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_2017))
            CMS_zz4l_alpha2_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"(1.915742+(-0.01599)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_centralValue_2017 = RooFormulaVar("CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"(3.968863+0.10151*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_2_centralValue_2017,CMS_zz4l_sigma_sig_2_centralValue_2017,CMS_zz4l_alpha_2_centralValue_2017,CMS_zz4l_n_2_centralValue_2017,CMS_zz4l_alpha2_2_centralValue_2017,CMS_zz4l_n2_2_centralValue_2017)
        else:
            CMS_zz4l_mean_sig_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(123.991536+1.01065*(@0-125)) + @0*@1*@2", \
                                                                RooArgList(MH,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_err_2_2016))

            CMS_zz4l_sigma_sig_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_2_centralValue_"+channel+recobin+year, \
                                                                "(2.250599+(-0.00689)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig_2016))

            CMS_zz4l_alpha_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_2_centralValue_"+channel+recobin+year,"(1.000207+(-0.02621)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n_2_centralValue_"+channel+recobin+year,"(3.485910+0.17889*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_2016))
            CMS_zz4l_alpha2_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_2_centralValue_"+channel+recobin+year,"(1.911649+(-0.01900)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_centralValue_2016 = RooFormulaVar("CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_2_centralValue_"+channel+recobin+year,"(4.027399+0.03819*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_2_centralValue_2016,CMS_zz4l_sigma_sig_2_centralValue_2016,CMS_zz4l_alpha_2_centralValue_2016,CMS_zz4l_n_2_centralValue_2016,CMS_zz4l_alpha2_2_centralValue_2016,CMS_zz4l_n2_2_centralValue_2016)

    if (channel=='4mu'):
        if (year=='2018'):
            CMS_zz4l_mean_sig_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(124.843147+0.99986*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig_2018,CMS_zz4l_mean_m_err_1_2018))

            CMS_zz4l_sigma_sig_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(1.159393+0.00953*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig_2018))
            CMS_zz4l_alpha_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.263473+(-0.00215)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"(2.050764+0.00066*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_2018))
            CMS_zz4l_alpha2_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"(1.939331+(-0.00025)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_centralValue_2018 = RooFormulaVar("CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"(2.551306+0.01706*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_1_centralValue_2018,CMS_zz4l_sigma_sig_1_centralValue_2018,CMS_zz4l_alpha_1_centralValue_2018,CMS_zz4l_n_1_centralValue_2018,CMS_zz4l_alpha2_1_centralValue_2018,CMS_zz4l_n2_1_centralValue_2018)
        elif (year=='2017'):
            CMS_zz4l_mean_sig_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(124.849295+0.99435*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_err_1_2017))

            CMS_zz4l_sigma_sig_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(1.154259+0.00825*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig_2017))

            CMS_zz4l_alpha_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.257942+0.00418*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"(2.059605+-0.01752*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_2017))
            CMS_zz4l_alpha2_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"(1.962162+0.00080*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_centralValue_2017 = RooFormulaVar("CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"(2.463661+0.00254*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_1_centralValue_2017,CMS_zz4l_sigma_sig_1_centralValue_2017,CMS_zz4l_alpha_1_centralValue_2017,CMS_zz4l_n_1_centralValue_2017,CMS_zz4l_alpha2_1_centralValue_2017,CMS_zz4l_n2_1_centralValue_2017)
        else:
            CMS_zz4l_mean_sig_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_mean_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(124.847170+0.99417*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_err_1_2016))

            CMS_zz4l_sigma_sig_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year,"CMS_zz4l_sigma_sig_1_centralValue_"+channel+recobin+year, \
                                                                "(1.153763+0.01344*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig_2016))

            CMS_zz4l_alpha_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha_1_centralValue_"+channel+recobin+year,"(1.259665+0.00540*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n_1_centralValue_"+channel+recobin+year,"(2.051191+-0.01579*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_2016))
            CMS_zz4l_alpha2_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_alpha2_1_centralValue_"+channel+recobin+year,"(1.871168+0.00937*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_centralValue_2016 = RooFormulaVar("CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"CMS_zz4l_n2_1_centralValue_"+channel+recobin+year,"(2.676450+-0.01358*(@0-125))",RooArgList(MH))

            # true signal shape
            trueH = RooDoubleCB("trueH","trueH",m,CMS_zz4l_mean_sig_1_centralValue_2016,CMS_zz4l_sigma_sig_1_centralValue_2016,CMS_zz4l_alpha_1_centralValue_2016,CMS_zz4l_n_1_centralValue_2016,CMS_zz4l_alpha2_1_centralValue_2016,CMS_zz4l_n2_1_centralValue_2016)


    # Wrong signal combination events
    if (year=='2018'):
        if (channel=='4mu'):
            p1_12018 = RooFormulaVar("CMS_fakeH_p1_1"+year,"p1_1"+year,"137.63080525+0.20718*(@0-125)",ROOT.RooArgList(MH))
            p2_12018 = RooFormulaVar("CMS_fakeH_p2_1"+year,"p2_1"+year,"17.73939875+(-0.0113475)*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_12018, p2_12018)
        if (channel=='4e'):
            p1_22018 = RooFormulaVar("CMS_fakeH_p1_2"+year,"p1_2"+year,"136.9123585+-0.020945*(@0-125)",ROOT.RooArgList(MH))
            p2_22018 = RooFormulaVar("CMS_fakeH_p2_2"+year,"p2_2"+year,"16.10426275+0.080675*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_22018, p2_22018)
        if (channel=='2e2mu'):
            p1_32018 = RooFormulaVar("CMS_fakeH_p1_3"+year,"p1_3"+year,"139.11565075+0.2334875*(@0-125)",ROOT.RooArgList(MH))
            p2_32018 = RooFormulaVar("CMS_fakeH_p2_3"+year,"p2_3"+year,"17.39454325+0.27387*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_32018, p2_32018)
    elif (year=='2017'):
        if (channel=='4mu'):
            p1_12017 = RooFormulaVar("CMS_fakeH_p1_1"+year,"p1_1"+year,"137.5872+-0.0187475*(@0-125)",ROOT.RooArgList(MH))
            p2_12017 = RooFormulaVar("CMS_fakeH_p2_1"+year,"p2_1"+year,"18.05642225+-0.182495*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_12017, p2_12017)
        if (channel=='4e'):
            p1_22017 = RooFormulaVar("CMS_fakeH_p1_2"+year,"p1_2"+year,"133.98211375+0.790945*(@0-125)",ROOT.RooArgList(MH))
            p2_22017 = RooFormulaVar("CMS_fakeH_p2_2"+year,"p2_2"+year,"16.82234175+-0.2156775*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_22017, p2_22017)
        if (channel=='2e2mu'):
            p1_32017 = RooFormulaVar("CMS_fakeH_p1_3"+year,"p1_3"+year,"139.4166885+0.149575*(@0-125)",ROOT.RooArgList(MH))
            p2_32017 = RooFormulaVar("CMS_fakeH_p2_3"+year,"p2_3"+year,"17.0934935+0.2527325*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_32017, p2_32017)
    else:
        if (channel=='4mu'):
            p1_12016 = RooFormulaVar("CMS_fakeH_p1_1"+year,"p1_1"+year,"136.7719185+0.3965175*(@0-125)",ROOT.RooArgList(MH))
            p2_12016 = RooFormulaVar("CMS_fakeH_p2_1"+year,"p2_1"+year,"17.86584175+-0.0833375*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_12016, p2_12016)
        if (channel=='4e'):
            p1_22016 = RooFormulaVar("CMS_fakeH_p1_2"+year,"p1_2"+year,"135.6637315+1.07089*(@0-125)",ROOT.RooArgList(MH))
            p2_22016 = RooFormulaVar("CMS_fakeH_p2_2"+year,"p2_2"+year,"15.976523+0.3065*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_22016, p2_22016)
        if (channel=='2e2mu'):
            p1_32016 = RooFormulaVar("CMS_fakeH_p1_3"+year,"p1_3"+year,"139.007959+0.569655*(@0-125)",ROOT.RooArgList(MH))
            p2_32016 = RooFormulaVar("CMS_fakeH_p2_3"+year,"p2_3"+year,"18.213078+0.378485*(@0-125)",ROOT.RooArgList(MH))
            fakeH = RooLandau("fakeH", "landau", m, p1_32016, p2_32016)


    if (addfakeH):
        inc_wrongfrac_ggH=inc_wrongfrac["ggH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_qqH=inc_wrongfrac["VBF_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_WH=inc_wrongfrac["WH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_ZH=inc_wrongfrac["ZH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_ttH=inc_wrongfrac["ttH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    else:
        inc_wrongfrac_ggH=0.0
        inc_wrongfrac_qqH=0.0
        inc_wrongfrac_WH=0.0
        inc_wrongfrac_ZH=0.0
        inc_wrongfrac_ttH=0.0

    binfrac_wrongfrac_ggH=binfrac_wrongfrac["ggH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_qqH=binfrac_wrongfrac["VBF_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_WH=binfrac_wrongfrac["WH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_ZH=binfrac_wrongfrac["ZH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_ttH=binfrac_wrongfrac["ttH_powheg_JHUgen_125.38_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]

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
    JES = RooRealVar("JES","JES", 0, -5.0, 5.0)
    logger.debug("obs_ifJES = {}".format(obs_ifJES))
    if (obs_ifJES):
        lambda_JES_sig = lambdajesup[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+""+"_"+recobin]
        lambda_JES_sig_var = RooRealVar("lambda_sig_"+modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+""+"_"+recobin+"_"+year, "lambda_sig_"+modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+""+"_"+recobin+"_"+year, lambda_JES_sig)
        JES_sig_rfv = RooFormulaVar("JES_rfv_sig_"+recobin+"_"+channel+"_"+year,"@0*@1", RooArgList(JES, lambda_JES_sig_var) )

    for genbin in range(nBins):
        trueH_shape[genbin] = trueH.Clone();
        trueH_shape[genbin].SetName("trueH"+channel+"Bin"+str(genbin))
        if (usecfactor): fideff[genbin] = cfactor[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(genbin)+"_"+recobin]
        else: fideff[genbin] = eff[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(genbin)+"_"+recobin]
        fideff_var[genbin] = RooRealVar("effBin"+str(genbin)+"_"+recobin+"_"+channel+"_"+year,"effBin"+str(genbin)+"_"+recobin+"_"+channel+"_"+year, fideff[genbin]);

        logger.debug("obs_ifJES: {},  doJES: {}, condition: {}".format(obs_ifJES, doJES, (not (obs_ifJES) or (not doJES))))
        logger.info("fideff[genbin]: {}".format(fideff[genbin]))
        logger.info("model name is   {}".format(modelName))

        # if( not (obs_ifJES) or (not doJES)) :
        #     trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_var[genbin], lumi) );
        # else :
        #     trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_var[genbin], lumi, JES_sig_rfv) );


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

    for genbin in range(nBins):

        if (physicalModel=="v3"):

            fidxs = {}
            for fState in ['4e','4mu', '2e2mu']:
                fidxs[fState] = 0
                fidxs[fState] += higgs_xs['ggH_125.38']*higgs4l_br['125.38_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['VBF_125.38']*higgs4l_br['125.38_'+fState]*acc['VBF_powheg_JHUgen_125.38_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['WH_125.38']*higgs4l_br['125.38_'+fState]*acc['WH_powheg_JHUgen_125.38_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['ZH_125.38']*higgs4l_br['125.38_'+fState]*acc['ZH_powheg_JHUgen_125.38_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['ttH_125.38']*higgs4l_br['125.38_'+fState]*acc['ttH_powheg_JHUgen_125.38_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
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

            if( not (obs_ifJES) or (not doJES)) :
                trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_var[genbin], lumi) );
                #trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1*@2", RooArgList(SigmaHBin[channel+str(genbin)], fideff_var[genbin], lumi) );
            else :
                trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_var[genbin], lumi, JES_sig_rfv) )

            logger.debug("obs_ifJES: {},  doJES: {}, condition: {}".format(obs_ifJES, doJES, (not (obs_ifJES) or (not doJES))))
            if (obs_ifJES):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi))

        elif (physicalModel=="v2"):

            rBin_channel[str(genbin)] = RooRealVar("r"+channel+"Bin"+str(genbin),"r"+channel+"Bin"+str(genbin), 1.0, 0.0, 10.0)
            rBin_channel[str(genbin)].setConstant(True)

            if( not (obs_ifJES) or (not doJES)) :
                trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1", RooArgList(fideff_var[genbin], lumi) );
            else :
                trueH_norm[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_norm","@0*@1*(1-@2)", RooArgList(fideff_var[genbin], lumi, JES_sig_rfv) )

            if (obs_ifJES):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi))

    outin = outinratio[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    logger.info("outin: obsBin: {:3}\t outin: {}".format(obsBin,outin))
    outin_var = RooRealVar("outfracBin_"+recobin+"_"+channel,"outfracBin_"+recobin+"_"+channel+"_"+year, outin)
    outin_var.setConstant(True)
    out_trueH_norm_args = RooArgList(outin_var)
    out_trueH_norm_func = "@0*("
    for i in range(nBins):
        out_trueH_norm_args.add(trueH_norm_final[i])
        out_trueH_norm_func = out_trueH_norm_func+"@"+str(i+1)+"+"
    out_trueH_norm_func = out_trueH_norm_func.replace(str(nBins)+"+",str(nBins)+")")
    out_trueH_norm = RooFormulaVar("out_trueH_norm",out_trueH_norm_func,out_trueH_norm_args)
    # Backgrounds

    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = { 'qqzz':{'2e2mu':'ZZTo2e2mu_powheg', '4e':'ZZTo4e_powheg', '4mu':'ZZTo4mu_powheg'},
                         'ggzz':{'2e2mu':'ggZZ_2e2mu_MCFM67', '4e':'ggZZ_4e_MCFM67', '4mu':'ggZZ_4mu_MCFM67'},
                         'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}}
    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][channel]+'_'+channel+'_'+obsNameDictKey+'_'+recobin]
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+recobin+"_"+channel+"_"+year,"frac_qqzz_"+recobin+"_"+channel+"_"+year, frac_qqzz);

    frac_ggzz = fractionsBackground[bkg_sample_tags['ggzz'][channel]+'_'+channel+'_'+obsNameDictKey+'_'+recobin]
    frac_ggzz_var = RooRealVar("frac_ggzz_"+recobin+"_"+channel+"_"+year,"frac_ggzz_"+recobin+"_"+channel+"_"+year, frac_ggzz);

    logger.info ("fractionsBackground:\n\t{}".format(fractionsBackground))
    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][channel]+"_AllChans_"+obsNameDictKey+'_'+recobin]
    frac_zjets_var = RooRealVar("frac_zjet_"+recobin+"_"+channel+"_"+year,"frac_zjet_"+recobin+"_"+channel+"_"+year, frac_zjets);

    logger.info ("obsBin: {obsBin:2}, frac_qqzz: {frac_qqzz:9}, frac_ggzz: {frac_ggzz:9}, frac_zjets: {frac_zjets:9}".format(
         obsBin = obsBin, frac_qqzz = frac_qqzz, frac_ggzz = frac_ggzz, frac_zjets = frac_zjets
     ))

    if (obs_ifJES):
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
    logger.debug("SuffixOfRootFile: "+SuffixOfRootFile)
    template_qqzzName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_qqZZ_"+channel+"_"+SuffixOfRootFile+".root"
    template_ggzzName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_ggZZ_"+channel+"_"+SuffixOfRootFile+".root"
    if (not obsName=="mass4l"):
        template_zjetsName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_ZJetsCR_AllChans_"+SuffixOfRootFile+".root"
    else:
        template_zjetsName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_ZJetsCR_"+channel+"_"+SuffixOfRootFile+".root"
    if (ifLLR): template_qqzzName = template_qqzzName.replace("ZZ","zz")
    qqzzTempFile = TFile(template_qqzzName,"READ")
    if (not ifLLR): qqzzTemplate = qqzzTempFile.Get("m4l_"+SuffixOfRootFile)
    if (ifLLR): qqzzTemplate = qqzzTempFile.Get("m4l_"+SuffixOfRootFile.replace("ZZ","zz").replace(".0",""))
    logger.info('qqZZ bins : {}, {}, {}'.format(qqzzTemplate.GetNbinsX(),qqzzTemplate.GetBinLowEdge(1),qqzzTemplate.GetBinLowEdge(qqzzTemplate.GetNbinsX()+1)))

    if (ifLLR): template_ggzzName = template_ggzzName.replace("ZZ","zz")
    ggzzTempFile = TFile(template_ggzzName,"READ")
    if (not ifLLR): ggzzTemplate = ggzzTempFile.Get("m4l_"+SuffixOfRootFile)
    if (ifLLR): ggzzTemplate = ggzzTempFile.Get("m4l_"+SuffixOfRootFile.replace("ZZ","zz").replace(".0",""))
    logger.info('ggZZ bins : {}, {}, {}'.format(ggzzTemplate.GetNbinsX(),ggzzTemplate.GetBinLowEdge(1),ggzzTemplate.GetBinLowEdge(ggzzTemplate.GetNbinsX()+1)))

    if (ifLLR): template_zjetsName = template_zjetsName.replace("ZZ","zz")
    zjetsTempFile = TFile(template_zjetsName,"READ")
    if (not ifLLR): zjetsTemplate = zjetsTempFile.Get("m4l_"+SuffixOfRootFile)
    if (ifLLR): zjetsTemplate = zjetsTempFile.Get("m4l_"+SuffixOfRootFile.replace("ZZ","zz").replace(".0",""))
    logger.info('zjets bins: {}, {}, {}'.format(zjetsTemplate.GetNbinsX(),zjetsTemplate.GetBinLowEdge(1),zjetsTemplate.GetBinLowEdge(zjetsTemplate.GetNbinsX()+1)))

    binscale = 3 # FIXME: Why number 3 hardcoded?
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
    if( not (obs_ifJES ) or (not doJES)) :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0", RooArgList(frac_ggzz_var) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )
    else :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0*(1-@1)", RooArgList(frac_qqzz_var, JES_qqzz_rfv) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0*(1-@1)", RooArgList(frac_ggzz_var, JES_ggzz_rfv) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0*(1-@1)", RooArgList(frac_zjets_var, JES_zjets_rfv) )

    # There is some issue with the data root file. So, temporarily we are using Tahir varsion.
    # if (year == '2016'): data_obs_file = TFile('/eos/user/q/qguo/newNTuple_UL/2016/data_UL2016_all_noDuplicates_slimmed_newMuSF_add2p5_workspace.root')
    # elif (year == '2017'): data_obs_file = TFile('/eos/user/q/qguo/newNTuple_UL/2017/Slimmed_2p5/DataUL2017_all_noDuplicates_slimmed_newMuSF_add2p5_slimmed_newMuSF_add2p5_workspace.root')
    # elif (year == '2018'): data_obs_file = TFile('/eos/user/q/qguo/newNTuple_UL/2018/Slimmed_2p5/DataUL2018_all_noDuplicates_slimmed_newMuSF_add2p5_slimmed_newMuSF_add2p5_workspace.root')
    if (year == '2016'): data_obs_file = TFile('/afs/cern.ch/user/t/tjavaid/public/data_UL2016_noDuplicates_created.root')
    elif (year == '2017'): data_obs_file = TFile('/afs/cern.ch/user/t/tjavaid/public/data_UL2017_noDuplicates_created.root')
    elif (year == '2018'): data_obs_file = TFile('/afs/cern.ch/user/t/tjavaid/public/data_UL2018_noDuplicates_created.root')

    data_obs_tree = data_obs_file.Get('passedEvents')

    logger.info ("Obs name: {:11}  Bin (low, high) edge: ({}, {})".format(obsName,obsBin_low,obsBin_high))
    if (obsName == "nJets"): obsName = "njets_reco_pt30_eta4p7"
    if (channel=='4mu'):
        if (obsName == "mass4l" ): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu),"(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+")")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>"+str(m4l_low)+" && mass4mu<"+mass_high+" && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        elif is2DObs: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable,observable2),"(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+" && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+" && abs("+obsNameOrig[1]+")>="+obsBin_low2+" && abs("+obsNameOrig[1]+")<"+obsBin_high2+")")
        else:                  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),                    "(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+" && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+str(obsBin_high_inf)+")")
    if (channel=='4e'):
        if (obsName == "mass4l"): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e),"(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+")")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+" && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        elif is2DObs: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable,observable2),"(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+" && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+" && abs("+obsNameOrig[1]+")>="+obsBin_low2+" && abs("+obsNameOrig[1]+")<"+obsBin_high2+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+" && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+str(obsBin_high_inf)+")")
    if (channel=='2e2mu'):
        if (obsName == "mass4l" ): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu),"(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+")")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+" && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        elif is2DObs: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable,observable2),"(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+" && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+" && abs("+obsNameOrig[1]+")>="+obsBin_low2+" && abs("+obsNameOrig[1]+")<"+obsBin_high2+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+" && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+str(obsBin_high_inf)+")")

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

    for genbin in range(nBins):
        getattr(wout,'import')(trueH_shape[genbin],RooFit.RecycleConflictNodes())
        getattr(wout,'import')(trueH_norm[genbin],RooFit.RecycleConflictNodes())

    if (not usecfactor):
        out_trueH.SetName("out_trueH")
        getattr(wout,'import')(out_trueH, RooFit.RecycleConflictNodes())
        getattr(wout,'import')(out_trueH_norm, RooFit.RecycleConflictNodes())

    getattr(wout,'import')(fakeH)
    getattr(wout,'import')(fakeH_norm)

    qqzzTemplatePdf.SetName("bkg_qqzz")
    qqzzTemplatePdf.Print("v")
    getattr(wout,'import')(qqzzTemplatePdf,RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence())
    getattr(wout,'import')(qqzz_norm)

    ggzzTemplatePdf.SetName("bkg_ggzz")
    ggzzTemplatePdf.Print("v")
    getattr(wout,'import')(ggzzTemplatePdf,RooFit.RecycleConflictNodes())
    getattr(wout,'import')(ggzz_norm)

    zjetsTemplatePdf.SetName("bkg_zjets")
    zjetsTemplatePdf.Print("v")
    getattr(wout,'import')(zjetsTemplatePdf, RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence())
    getattr(wout,'import')(zjets_norm)

    ## data
    getattr(wout,'import')(data_obs.reduce(RooArgSet(m)))

    combineOutputs = combineOutputs.format(year = year)
    if (addfakeH):
        if (usecfactor):
            fout = TFile(combineOutputs+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsNameDictKey+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.root","RECREATE")
        else:
            fout = TFile(combineOutputs+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsNameDictKey+"_"+physicalModel+".Databin"+str(obsBin)+".root","RECREATE")
    else:
        if (usecfactor):
            fout = TFile(combineOutputs+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsNameDictKey+"_"+physicalModel+".Databin"+str(obsBin)+".Cfactor.NoFakeH.root","RECREATE")
        else:
            fout = TFile(combineOutputs+"/hzz4l_"+channel+"S_13TeV_xs_"+modelName+"_"+obsNameDictKey+"_"+physicalModel+".Databin"+str(obsBin)+".NoFakeH.root","RECREATE")

    logger.info("write workspace to output root file")
    logger.debug("Total entries in data_obs: "+str(data_obs.numEntries()))
    fout.WriteTObject(wout)
    fout.Close()

    return data_obs.numEntries()

#createXSworkspace("pT4l", "2e2mu", 4, 0, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 1, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 2, False, True)
#createXSworkspace("pT4l", "2e2mu", 4, 3, False, True)
#createXSworkspace("mass4l", "2e2mu", 2, 0, ["105.0","140.0"], False, True, "ggH_powheg_JHUgen_125", "v2","2018")
