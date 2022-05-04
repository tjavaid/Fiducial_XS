# this script is called once for each reco bin (obsBin)
# in each reco bin there are (nBins) signals (one for each gen bin)

# FIXME: Commented RooFit.Silence() and RooFit.RecycleConflictNodes()
# RooFit.RecycleConflictNodes(): https://root.cern.ch/doc/master/classRooWorkspace.html
#           If any of the function objects to be imported already exist in the name space,
#           connect the imported expression to the already existing nodes.
#           Attention:
#           Use with care! If function definitions do not match,
#           this alters the definition of your function upon import

# For Silence issue we should shift to ROOT 6.18
#       Reference: https://root-forum.cern.ch/t/rooworkspace-import-roofit-silence-does-not-work-when-importing-datasets/32591/2

import sys
import os

from ROOT import *

# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from Utils import  logger
import logging

logger.setLevel(logging.DEBUG)

sys.path.append('./'+datacardInputs)

def createXSworkspace(obsName, channel, nBins, obsBin, observableBins, usecfactor, addfakeH, modelName, physicalModel, year):
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
    global combineOutputs
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
        logger.debug("SuffixOfRootFile: {}".format(SuffixOfRootFile))
    else:
        logger.info("This is recognised as 1D observable...")
        # obsNameOrig = obsName
        obsBin_low = observableBins[obsBin]
        obsBin_high = observableBins[obsBin+1]

        obs_bin_lowest = observableBins[0]
        obs_bin_highest = observableBins[len(observableBins)-1]

        recobin = "recobin"+str(obsBin)
        logger.debug("""
                (obsBin_low,  obsBin_high ) = ({},{});
                (obs_bin_lowest,  obs_bin_highest ) = ({}, {})""".format(
                    obsBin_low, obsBin_high, obs_bin_lowest, obs_bin_highest
                    ))
        SuffixOfRootFile = obsNameOrig[0]+"_"+obsBin_low+"_"+obsBin_high
        logger.info("SuffixOfRootFile: {}".format(SuffixOfRootFile))

    doJES = 1

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

    # Load the legacy f
    # FIXME: We should move this to inputs directory. With better name "Workspace_Template_From8TeV_Analysis.root"
    f_in = TFile("125.0/hzz4l_"+channel+"S_8TeV.input.root","READ")
    w = f_in.Get("w")
    # w.Print()

    # import h4l xs br
    _temp = __import__('higgs_xsbr_13TeV', globals(), locals(), ['higgs_xs','higgs4l_br'], -1)
    higgs_xs = _temp.higgs_xs
    higgs4l_br = _temp.higgs4l_br

    # 4 lepton mass observable to perform the fit
    m = w.var("CMS_zz4l_mass")
    # m = RooRealVar("CMS_zz4l_mass", "CMS_zz4l_mass", 105.0, 140.0)
    #logger.info("m.numBins()",m.numBins())
    m.setMin(105.0)
    m.setMax(140.0)
    #m.setBins(45)
    #m.Print("v")

    mass4e = RooRealVar("mass4e", "mass4e", 105.0, 140.0)
    mass4mu = RooRealVar("mass4mu", "mass4mu", 105.0, 140.0)
    mass2e2mu = RooRealVar("mass2e2mu", "mass2e2mu",105.0, 140.0)
    if (not obsName=="mass4l"):
        # if (obsName=="rapidity4l" or obsName=="cosThetaStar" or obsName=="cosTheta1" or obsName=="cosTheta2" or obsName=="Phi" or obsName=="Phi1"):
            # observable = RooRealVar(obsName,obsName,-1.0*float(obs_bin_highest),float(obs_bin_highest))
        observable   = RooRealVar(obsName,obsName,float(obs_bin_lowest),float(obs_bin_highest))
        observable.Print()
        if is2DObs:
            observable2 = RooRealVar(obsNameOrig[1],obsNameOrig[1],float(obs_bin_lowest2),float(obs_bin_highest2))
            observable2.Print()
    # luminosity
    lumi = RooRealVar("lumi_13","lumi_13", 59.7) # FIXME: Lumi value is hardcoded

    # SM values of signal expectations (inclusive, reco level)
    ggH_norm = w.function("ggH_norm")
    qqH_norm = w.function("qqH_norm")
    WH_norm = w.function("WH_norm")
    ZH_norm = w.function("ZH_norm")
    ttH_norm = w.function("ttH_norm")
    # logger.debug("""
    #     Norm values:
    #         ggH_norm = {}
    #         qqH_norm = {}
    #         WH_norm = {}
    #         ZH_norm = {}
    #         ttH_norm = {}
    #         Total: n_allH = {}
    # """.format(
    #     ggH_norm.getVal(),
    #     qqH_norm.getVal(),
    #     WH_norm.getVal(),
    #     ZH_norm.getVal(),
    #     ttH_norm.getVal(),
    #     ggH_norm.getVal() + qqH_norm.getVal() + WH_norm.getVal() + ZH_norm.getVal() + ttH_norm.getVal()
    # ))
    # logger.error("=="*51)
    # ggH_norm = RooRealVar("ggH_norm","ggH_norm", 6.94202296623) # FIXME: got these values from 8TeV Rootfiles
    # qqH_norm = RooRealVar("qqH_norm","qqH_norm", 0.633580595429) # FIXME: got these values from 8TeV Rootfiles
    # WH_norm = RooRealVar("WH_norm","WH_norm", 0.209508946773) # FIXME: got these values from 8TeV Rootfiles
    # ZH_norm = RooRealVar("ZH_norm","ZH_norm", 0.157008222773) # FIXME: got these values from 8TeV Rootfiles
    # ttH_norm = RooRealVar("ttH_norm","ttH_norm", 0.03604907196) # FIXME: got these values from 8TeV Rootfiles
    n_allH = (ggH_norm.getVal()+qqH_norm.getVal()+WH_norm.getVal()+ZH_norm.getVal()+ttH_norm.getVal())
    logger.info("allH norm: {}".format(n_allH))

    # true signal shape
    trueH = w.pdf("ggH")

    # update to 13 TeV parameterization
    MH = w.var("MH")
    CMS_zz4l_mean_m_sig = w.var("CMS_zz4l_mean_m_sig")
    CMS_zz4l_mean_e_sig = w.var("CMS_zz4l_mean_e_sig")
    CMS_zz4l_mean_m_err_1_8 = w.var("CMS_zz4l_mean_m_err_1_8")
    CMS_zz4l_mean_m_err_3_8 = w.var("CMS_zz4l_mean_m_err_3_8")
    CMS_zz4l_mean_e_err_2_8 = w.var("CMS_zz4l_mean_e_err_2_8")
    CMS_zz4l_mean_e_err_3_8 = w.var("CMS_zz4l_mean_e_err_3_8")
    CMS_zz4l_sigma_m_sig = w.var("CMS_zz4l_sigma_m_sig")
    CMS_zz4l_sigma_e_sig = w.var("CMS_zz4l_sigma_e_sig")
    CMS_zz4l_n_sig_1_8 = w.var("CMS_zz4l_n_sig_1_8")
    CMS_zz4l_n_sig_2_8 = w.var("CMS_zz4l_n_sig_2_8")
    CMS_zz4l_n_sig_3_8 = w.var("CMS_zz4l_n_sig_3_8")


    if (obsName!="mass4lREFIT"):
        if (channel=='2e2mu'):

            CMS_zz4l_mean_sig_3_8_centralValue = RooFormulaVar("CMS_zz4l_mean_sig_3_8_centralValue","CMS_zz4l_mean_sig_3_8_centralValue", \
                                                                   "(124.260469656+(0.995095874123)*(@0-125)) + (@0*@1*@3 + @0*@2*@4)/2", \
                                                                   RooArgList(MH,CMS_zz4l_mean_m_sig,CMS_zz4l_mean_e_sig,CMS_zz4l_mean_m_err_3_8,CMS_zz4l_mean_e_err_3_8))

            CMS_zz4l_mean_sig_NoConv_3_8 = RooFormulaVar("CMS_zz4l_mean_sig_NoConv_3_8","CMS_zz4l_mean_sig_NoConv_3_8","@0",RooArgList(CMS_zz4l_mean_sig_3_8_centralValue))

            CMS_zz4l_sigma_sig_3_8_centralValue = RooFormulaVar("CMS_zz4l_sigma_sig_3_8_centralValue","CMS_zz4l_sigma_sig_3_8_centralValue",\
                                                                    "(1.55330758963+(0.00797274642218)*(@0-125))*(TMath::Sqrt((1+@1)*(1+@2)))",RooArgList(MH,CMS_zz4l_sigma_m_sig,CMS_zz4l_sigma_e_sig))
            CMS_zz4l_alpha_3_centralValue = RooFormulaVar("CMS_zz4l_alpha_3_centralValue","CMS_zz4l_alpha_3_centralValue","(0.947414158515+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_3_8_centralValue = RooFormulaVar("CMS_zz4l_n_3_8_centralValue","CMS_zz4l_n_3_8_centralValue","(3.33147279858+(-0.0438375854704)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_3_8))
            CMS_zz4l_alpha2_3_centralValue = RooFormulaVar("CMS_zz4l_alpha2_3_centralValue","CMS_zz4l_alpha2_3_centralValue","(1.52497361611+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_3_8_centralValue = RooFormulaVar("CMS_zz4l_n2_3_8_centralValue","CMS_zz4l_n2_3_8_centralValue","(5.20522265056+(0)*(@0-125))",RooArgList(MH))

        if (channel=='4e'):

            CMS_zz4l_mean_sig_2_8_centralValue = RooFormulaVar("CMS_zz4l_mean_sig_2_8_centralValue","CMS_zz4l_mean_sig_2_8_centralValue", \
                                                                   "(123.5844824+(0.985478630993)*(@0-125)) + @0*@1*@2", \
                                                                   RooArgList(MH,CMS_zz4l_mean_e_sig,CMS_zz4l_mean_e_err_2_8))

            CMS_zz4l_mean_sig_NoConv_2_8 = RooFormulaVar("CMS_zz4l_mean_sig_NoConv_2_8","CMS_zz4l_mean_sig_NoConv_2_8","@0",RooArgList(CMS_zz4l_mean_sig_2_8_centralValue))
            CMS_zz4l_sigma_sig_2_8_centralValue = RooFormulaVar("CMS_zz4l_sigma_sig_2_8_centralValue","CMS_zz4l_sigma_sig_2_8_centralValue", \
                                                                    "(2.06515102908+(0.0170917403402)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_e_sig))

            CMS_zz4l_alpha_2_centralValue = RooFormulaVar("CMS_zz4l_alpha_2_centralValue","CMS_zz4l_alpha_2_centralValue","(0.948100247167+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_2_8_centralValue = RooFormulaVar("CMS_zz4l_n_2_8_centralValue","CMS_zz4l_n_2_8_centralValue","(4.50639853892+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_2_8))
            CMS_zz4l_alpha2_2_centralValue = RooFormulaVar("CMS_zz4l_alpha2_2_centralValue","CMS_zz4l_alpha2_2_centralValue","(1.50095152675+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_2_8_centralValue = RooFormulaVar("CMS_zz4l_n2_2_8_centralValue","CMS_zz4l_n2_2_8_centralValue","(8.41693578742+(0.219719825966)*(@0-125))",RooArgList(MH))

        if (channel=='4mu'):

            CMS_zz4l_mean_sig_1_8_centralValue = RooFormulaVar("CMS_zz4l_mean_sig_1_8_centralValue","CMS_zz4l_mean_sig_1_8_centralValue", \
                                                                   "(124.820536957+(0.999619883119)*(@0-125)) + @0*@1*@2",RooArgList(MH,CMS_zz4l_mean_m_sig,CMS_zz4l_mean_m_err_1_8))

            CMS_zz4l_mean_sig_NoConv_1_8 = RooFormulaVar("CMS_zz4l_mean_sig_NoConv_1_8","CMS_zz4l_mean_sig_NoConv_1_8","@0",RooArgList(CMS_zz4l_mean_sig_1_8_centralValue))
            CMS_zz4l_sigma_sig_1_8_centralValue = RooFormulaVar("CMS_zz4l_sigma_sig_1_8_centralValue","CMS_zz4l_sigma_sig_1_8_centralValue", \
                                                                    "(1.09001384743+(0.00899911411679)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_sigma_m_sig))

            CMS_zz4l_alpha_1_centralValue = RooFormulaVar("CMS_zz4l_alpha_1_centralValue","CMS_zz4l_alpha_1_centralValue","(1.23329827124+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n_1_8_centralValue = RooFormulaVar("CMS_zz4l_n_1_8_centralValue","CMS_zz4l_n_1_8_centralValue","(2.04575884495+(0)*(@0-125))*(1+@1)",RooArgList(MH,CMS_zz4l_n_sig_1_8))
            CMS_zz4l_alpha2_1_centralValue = RooFormulaVar("CMS_zz4l_alpha2_1_centralValue","CMS_zz4l_alpha2_1_centralValue","(1.84386824883+(0)*(@0-125))",RooArgList(MH))
            CMS_zz4l_n2_1_8_centralValue = RooFormulaVar("CMS_zz4l_n2_1_8_centralValue","CMS_zz4l_n2_1_8_centralValue","(2.98483993137+(0)*(@0-125))",RooArgList(MH))


    # Wrong signal combination events
    if (channel=='4mu'):
        #p1_1_8 = RooRealVar("CMS_fakeH_p1_1_8","p1_1_8", 150.0, 135.0, 185.)
        #p2_1_8 = RooRealVar("CMS_fakeH_p2_1_8","p2_1_8", 20.0, 10.0, 40.0)
        p1_1_8 = RooRealVar("CMS_fakeH_p1_1_8","p1_1_8",165.0, 145.0, 185.0)
        p3_1_8 = RooRealVar("CMS_fakeH_p3_1_8","p3_1_8",89.0, 84.0,94.0)
        p2_1_8 = RooFormulaVar("CMS_fakeH_p2_1_8","p2_1_8","0.72*@0-@1",RooArgList(p1_1_8,p3_1_8))
        fakeH = RooLandau("fakeH", "landau", m, p1_1_8, p2_1_8)
    if (channel=='4e'):
        #p1_2_8 = RooRealVar("CMS_fakeH_p1_2_8","p1_2_8", 150.0, 135.0, 185.)
        #p2_2_8 = RooRealVar("CMS_fakeH_p2_2_8","p2_2_8", 20.0, 10.0, 40.0)
        p1_2_8 = RooRealVar("CMS_fakeH_p1_2_8","p1_2_8",165.0, 145.0, 185.0)
        p3_2_8 = RooRealVar("CMS_fakeH_p3_2_8","p3_2_8",89.0, 84.0,94.0)
        p2_2_8 = RooFormulaVar("CMS_fakeH_p2_2_8","p2_2_8","0.72*@0-@1",RooArgList(p1_2_8,p3_2_8))
        fakeH = RooLandau("fakeH", "landau", m, p1_2_8, p2_2_8)
    if (channel=='2e2mu'):
        #p1_3_8 = RooRealVar("CMS_fakeH_p1_3_8","p1_3_8", 150.0, 135.0, 185.)
        #p2_3_8 = RooRealVar("CMS_fakeH_p2_3_8","p2_3_8", 20.0, 10.0, 40.0)
        p1_3_8 = RooRealVar("CMS_fakeH_p1_3_8","p1_3_8",165.0, 145.0, 185.0)
        p3_3_8 = RooRealVar("CMS_fakeH_p3_3_8","p3_3_8",89.0, 84.0,94.0)
        p2_3_8 = RooFormulaVar("CMS_fakeH_p2_3_8","p2_3_8","0.72*@0-@1",RooArgList(p1_3_8,p3_3_8))
        fakeH = RooLandau("fakeH", "landau", m, p1_3_8, p2_3_8)
    if (addfakeH):
        inc_wrongfrac_ggH=inc_wrongfrac["ggH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        #inc_wrongfrac_ggH=inc_wrongfrac["ggH_HRes_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_qqH=inc_wrongfrac["VBF_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_WH=inc_wrongfrac["WH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_ZH=inc_wrongfrac["ZH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
        inc_wrongfrac_ttH=inc_wrongfrac["ttH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    else:
        inc_wrongfrac_ggH=0.0
        inc_wrongfrac_qqH=0.0
        inc_wrongfrac_WH=0.0
        inc_wrongfrac_ZH=0.0
        inc_wrongfrac_ttH=0.0

    binfrac_wrongfrac_ggH=binfrac_wrongfrac["ggH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    #binfrac_wrongfrac_ggH=binfrac_wrongfrac["ggH_HRes_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_qqH=binfrac_wrongfrac["VBF_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_WH=binfrac_wrongfrac["WH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_ZH=binfrac_wrongfrac["ZH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    binfrac_wrongfrac_ttH=binfrac_wrongfrac["ttH_powheg_JHUgen_125_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]

    if (channel=='4e'):
        # FIXME: Check these values
        n_fakeH = (0.24*inc_wrongfrac_WH*binfrac_wrongfrac_WH+0.20*inc_wrongfrac_ZH*binfrac_wrongfrac_ZH+0.10*inc_wrongfrac_ttH*binfrac_wrongfrac_ttH)
    if (channel=='4mu'):
        n_fakeH = (0.45*inc_wrongfrac_WH*binfrac_wrongfrac_WH+0.38*inc_wrongfrac_ZH*binfrac_wrongfrac_ZH+0.20*inc_wrongfrac_ttH*binfrac_wrongfrac_ttH)
    if (channel=='2e2mu'):
        n_fakeH = (0.57*inc_wrongfrac_WH*binfrac_wrongfrac_WH+0.51*inc_wrongfrac_ZH*binfrac_wrongfrac_ZH+0.25*inc_wrongfrac_ttH*binfrac_wrongfrac_ttH)

    n_fakeH_var = RooRealVar("n_fakeH_var_"+recobin+"_"+channel,"n_fakeH_var_"+recobin+"_"+channel,n_fakeH);

    fakeH_norm = RooFormulaVar("fakeH_norm","@0",RooArgList(n_fakeH_var))

    # Out of acceptance events
    # (same shape as in acceptance shape)
    out_trueH = trueH.Clone()

    # true signal shape/norm
    trueH = w.pdf("ggH")

    # signal shape in different recobin
    trueH_shape = {}
    fideff = {}
    fideff_var = {}
    trueH_norm = {}

    # nuisance describes the jet energy scale uncertainty
    JES = RooRealVar("JES","JES", 0, -5.0, 5.0)
    if (obsName == "nJets"  or ("jet" in obsName)):
        lambda_JES_sig = lambdajesup[modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+""+"_"+recobin]
        lambda_JES_sig_var = RooRealVar("lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+""+"_"+recobin, "lambda_sig_"+modelName+"_"+channel+"_"+obsName+"_genbin"+str(obsBin)+""+"_"+recobin, lambda_JES_sig)
        JES_sig_rfv = RooFormulaVar("JES_rfv_sig_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_sig_var) )

    for genbin in range(nBins):
        trueH_shape[genbin] = trueH.Clone();
        trueH_shape[genbin].SetName("trueH"+channel+"Bin"+str(genbin))
        if (usecfactor): fideff[genbin] = cfactor[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(genbin)+"_"+recobin]
        else: fideff[genbin] = eff[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(genbin)+"_"+recobin]
        logger.info("fideff[genbin]: {}".format(fideff[genbin]))
        logger.info("model name is   {}".format(modelName))
        fideff_var[genbin] = RooRealVar("effBin"+str(genbin)+"_"+recobin+"_"+channel,"effBin"+str(genbin)+"_"+recobin+"_"+channel, fideff[genbin]);

        if( not (obsName=='nJets' or ("jet" in obsName)) or (not doJES)) :
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

    for genbin in range(nBins):
        if (physicalModel=="v3"):
            fidxs = {}
            for fState in ['4e','4mu', '2e2mu']:
                fidxs[fState] = 0
                fidxs[fState] += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                #fidxs[fState] += acc['ggH_HRes_125_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_JHUgen_125_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
                fidxs[fState] += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsNameDictKey+'_genbin'+str(genbin)+'_recobin'+str(genbin)]
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
            if (obsName == "nJets" or ("jet" in obsName)):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2" ,RooArgList(SigmaHBin[channel+str(genbin)],fideff_var[genbin],lumi))
        elif (physicalModel=="v1"):
            fracBin['4mu'+str(genbin)] = RooRealVar("frac4muBin"+str(genbin),"frac4muBin"+str(genbin), 0.25, 0.0, 0.5) # frac 4mu
            fracBin['4e'+str(genbin)] = RooRealVar("frac4eBin"+str(genbin),"frac4eBin"+str(genbin), 0.25, 0.0, 0.5) # frac 4e
            fracBin['2e2mu'+str(genbin)] = RooFormulaVar("frac2e2muBin"+str(genbin),"1-@0-@1", RooArgList(fracBin['4e'+str(genbin)],fracBin['4mu'+str(genbin)])) # frac 2e2mu
            fracBin['4mu'+str(genbin)].setConstant(True)
            fracBin['4e'+str(genbin)].setConstant(True)
            rBin[str(genbin)] = RooRealVar("rBin"+str(genbin),"rBin"+str(genbin), 1.0, 0.0, 10.0)
            rBin[str(genbin)].setConstant(True)
            #trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_final_norm","@0*@1*@2", RooArgList(rBin[str(genbin)], fracBin[channel+str(genbin)], trueH_norm[genbin]) );
            if (obsName == "nJets" or ("jet" in obsName)):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*@3*(1-@4)" ,RooArgList(rBin[str(genbin)],fracBin[channel+str(genbin)],fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*@3" ,RooArgList(rBin[str(genbin)],fracBin[channel+str(genbin)],fideff_var[genbin],lumi))
        else:
            rBin_channel[str(genbin)] = RooRealVar("r"+channel+"Bin"+str(genbin),"r"+channel+"Bin"+str(genbin), 1.0, 0.0, 10.0)
            rBin_channel[str(genbin)].setConstant(True)
            #trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+"_final_norm","@0*@1", RooArgList(rBin_channel[str(genbin)], trueH_norm[genbin]) );
            if (obsName == "nJets" or ("jet" in obsName)):
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2*(1-@3)", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi,JES_sig_rfv))
            else:
                trueH_norm_final[genbin] = RooFormulaVar("trueH"+channel+"Bin"+str(genbin)+recobin+"_final","@0*@1*@2", RooArgList(rBin_channel[str(genbin)], fideff_var[genbin],lumi))

    outin = outinratio[modelName+"_"+channel+"_"+obsNameDictKey+"_genbin"+str(obsBin)+"_"+recobin]
    logger.info("outin: obsBin: {:3}\t outin: {}".format(obsBin,outin))
    outin_var = RooRealVar("outfracBin_"+recobin+"_"+channel,"outfracBin_"+recobin+"_"+channel, outin);
    outin_var.setConstant(True)
    out_trueH_norm_args = RooArgList(outin_var)
    out_trueH_norm_func = "@0*("
    for i in range(nBins):
        out_trueH_norm_args.add(trueH_norm_final[i])
        out_trueH_norm_func = out_trueH_norm_func+"@"+str(i+1)+"+"
    out_trueH_norm_func = out_trueH_norm_func.replace(str(nBins)+"+",str(nBins)+")")
    out_trueH_norm = RooFormulaVar("out_trueH_norm",out_trueH_norm_func,out_trueH_norm_args)

    # Backgrounds
    #ggZZ = w.pdf("bkg_ggzz")
    #qqZZ = w.pdf("bkg_qqzz")
    #zjets = w.pdf("bkg_zjetsB")

    # fraction for bkgs and for signal in each gen bin
    bkg_sample_tags = { 'qqzz':{'2e2mu':'ZZTo2e2mu_powheg', '4e':'ZZTo4e_powheg', '4mu':'ZZTo4mu_powheg'},
                        'ggzz':{'2e2mu':'ggZZ_2e2mu_MCFM67', '4e':'ggZZ_4e_MCFM67', '4mu':'ggZZ_4mu_MCFM67'},
                        'zjets':{'2e2mu':'ZX4l_CR', '4e':'ZX4l_CR', '4mu':'ZX4l_CR'}}
    frac_qqzz = fractionsBackground[bkg_sample_tags['qqzz'][channel]+'_'+channel+'_'+obsNameDictKey+'_'+recobin]
    frac_qqzz_var  = RooRealVar("frac_qqzz_"+recobin+"_"+channel,"frac_qqzz_"+recobin+"_"+channel, frac_qqzz);

    frac_ggzz = fractionsBackground[bkg_sample_tags['ggzz'][channel]+'_'+channel+'_'+obsNameDictKey+'_'+recobin]
    frac_ggzz_var = RooRealVar("frac_ggzz_"+recobin+"_"+channel,"frac_ggzz_"+recobin+"_"+channel, frac_ggzz);

    logger.info ("fractionsBackground:\n\t{}".format(fractionsBackground))
    frac_zjets = fractionsBackground[bkg_sample_tags['zjets'][channel]+"_AllChans_"+obsNameDictKey+'_'+recobin]
    frac_zjets_var = RooRealVar("frac_zjet_"+recobin+"_"+channel,"frac_zjet_"+recobin+"_"+channel, frac_zjets);

    logger.info ("obsBin: {obsBin:2}, frac_qqzz: {frac_qqzz:9}, frac_ggzz: {frac_ggzz:9}, frac_zjets: {frac_zjets:9}".format(
        obsBin = obsBin, frac_qqzz = frac_qqzz, frac_ggzz = frac_ggzz, frac_zjets = frac_zjets
    ))

    if (obsName=="nJets" or ("jet" in obsName)):
        #######
        lambda_JES_qqzz = 0.0 #lambda_qqzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_qqzz_var = RooRealVar("lambda_qqzz_"+recobin+"_"+channel,"lambda_"+recobin+"_"+channel, lambda_JES_qqzz)
        JES_qqzz_rfv = RooFormulaVar("JES_rfv_qqzz_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_qqzz_var) )

        ####
        lambda_JES_ggzz = 0.0 #lambda_ggzz_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_ggzz_var = RooRealVar("lambda_ggzz_"+recobin+"_"+channel,"lambda_"+recobin+"_"+channel, lambda_JES_ggzz)
        JES_ggzz_rfv = RooFormulaVar("JES_rfv_ggzz_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_ggzz_var) )

        ####
        lambda_JES_zjets = 0.0 #lambda_zjets_jes[modelName+"_"+channel+"_nJets_"+recobin]
        lambda_JES_zjets_var = RooRealVar("lambda_zjets_"+recobin+"_"+channel,"lambda_zjets_"+recobin+"_"+channel, lambda_JES_zjets)
        JES_zjets_rfv = RooFormulaVar("JES_rfv_zjets_"+recobin+"_"+channel,"@0*@1", RooArgList(JES, lambda_JES_zjets_var) )


    ## background shapes in each reco bin
#    ggzzTemplatePdf = w.pdf("bkg_ggzz")
#    qqzzTemplatePdf = w.pdf("bkg_qqzz")
#    zjetsTemplatePdf = ggzzTemplatePdf.Clone();
#    zjetsTemplatePdf.SetName("bkg_zjets");

    #template path : ./templates/templatesXS/DTreeXS_{obsName}/8TeV/
    #template name : XSBackground_{bkgTag}_{finalStateString}_{obsName}_recobin{binNum}.root

    logger.debug("SuffixOfRootFile: "+SuffixOfRootFile)
    template_qqzzName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_qqZZ_"+channel+"_"+SuffixOfRootFile+".root"
    template_ggzzName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_ggZZ_"+channel+"_"+SuffixOfRootFile+".root"
    if (not obsName=="mass4l"):
        template_zjetsName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_ZJetsCR_AllChans_"+SuffixOfRootFile+".root"
    else:
        template_zjetsName = "./templates/templatesXS_"+str(year)+"/DTreeXS_"+obsNameDictKey+"/13TeV/XSBackground_ZJetsCR_"+channel+"_"+SuffixOfRootFile+".root"
    qqzzTempFile = TFile(template_qqzzName,"READ")
    qqzzTemplate = qqzzTempFile.Get("m4l_"+SuffixOfRootFile)
    logger.info('qqZZ bins : {}, {}, {}'.format(qqzzTemplate.GetNbinsX(),qqzzTemplate.GetBinLowEdge(1),qqzzTemplate.GetBinLowEdge(qqzzTemplate.GetNbinsX()+1)))

    ggzzTempFile = TFile(template_ggzzName,"READ")
    ggzzTemplate = ggzzTempFile.Get("m4l_"+SuffixOfRootFile)
    logger.info('ggZZ bins : {}, {}, {}'.format(ggzzTemplate.GetNbinsX(),ggzzTemplate.GetBinLowEdge(1),ggzzTemplate.GetBinLowEdge(ggzzTemplate.GetNbinsX()+1)))

    zjetsTempFile = TFile(template_zjetsName,"READ")
    zjetsTemplate = zjetsTempFile.Get("m4l_"+SuffixOfRootFile)
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

    qqzzTemplateName = "qqzz_"+channel+recobin
    ggzzTemplateName = "ggzz_"+channel+recobin
    zjetsTemplateName = "zjets_"+channel+recobin

    #qqzzTempDataHist = RooDataHist(qqzzTemplateName,qqzzTemplateName,RooArgList(m),qqzzTemplate)
    #ggzzTempDataHist = RooDataHist(ggzzTemplateName,ggzzTemplateName,RooArgList(m),ggzzTemplate)
    #zjetsTempDataHist = RooDataHist(zjetsTemplateName,zjetsTemplateName,RooArgList(m),zjetsTemplate)
    qqzzTempDataHist = RooDataHist(qqzzTemplateName,qqzzTemplateName,RooArgList(m),qqzzTemplateNew)
    ggzzTempDataHist = RooDataHist(ggzzTemplateName,ggzzTemplateName,RooArgList(m),ggzzTemplateNew)
    zjetsTempDataHist = RooDataHist(zjetsTemplateName,zjetsTemplateName,RooArgList(m),zjetsTemplateNew)

    qqzzTemplatePdf = RooHistPdf("qqzz","qqzz",RooArgSet(m),qqzzTempDataHist)
    ggzzTemplatePdf = RooHistPdf("ggzz","ggzz",RooArgSet(m),ggzzTempDataHist)
    zjetsTemplatePdf = RooHistPdf("zjets","zjets",RooArgSet(m),zjetsTempDataHist)

    # bkg fractions in reco bin; implemented in terms of fractions

    if( not (obsName=='nJets' or ("jet" in obsName) ) or (not doJES)) :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0", RooArgList(frac_qqzz_var) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0", RooArgList(frac_ggzz_var) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0", RooArgList(frac_zjets_var) )
    else :
       qqzz_norm = RooFormulaVar("bkg_qqzz_norm", "@0*(1-@1)", RooArgList(frac_qqzz_var, JES_qqzz_rfv) )
       ggzz_norm = RooFormulaVar("bkg_ggzz_norm", "@0*(1-@1)", RooArgList(frac_ggzz_var, JES_ggzz_rfv) )
       zjets_norm = RooFormulaVar("bkg_zjets_norm", "@0*(1-@1)", RooArgList(frac_zjets_var, JES_zjets_rfv) )


    #legacy_data = w.data("data_obs").reduce(RooArgSet(m))
    #for event in range(legacy_data.numEntries()):
    #     row = legacy_data.get(event)
    #     row.Print("v")
    #legacy_data.Print("v")

    if (obsName=="mass4lREFIT"):  data_obs_file = TFile('Inputs/data_13TeV_refit.root')
    else:  data_obs_file = TFile('Inputs/data_13TeV.root') #FIXME: Want to keep this in Input directory or at the same place where all ntuples are stored
    data_obs_tree = data_obs_file.Get('passedEvents')

    logger.info ("Obs name: {:11}  Bin (low, high) edge: ({}, {})".format(obsName,obsBin_low,obsBin_high))
    if (obsName == "nJets"): obsName = "njets_reco_pt30_eta4p7"
    if (channel=='4mu'):
        if (obsName.startswith("mass4l")): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu),"(mass4mu>105.0 && mass4mu<140.0)")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),"(mass4mu>105.0 && mass4mu<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        elif is2DObs: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable,observable2),"(mass4mu>105.0 && mass4mu<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+" && abs("+obsNameOrig[1]+")>="+obsBin_low2+" && abs("+obsName+")<"+obsBin_high2+")")
        else:                  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4mu,observable),                    "(mass4mu>105.0 && mass4mu<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+")")
    if (channel=='4e'):
        if (obsName.startswith("mass4l")): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e),"(mass4e>105.0 && mass4e<140.0)")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>105.0 && mass4e<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        elif is2DObs: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable,observable2),"(mass4e>105.0 && mass4e<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+" && abs("+obsNameOrig[1]+")>="+obsBin_low2+" && abs("+obsName+")<"+obsBin_high2+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass4e,observable),"(mass4e>105.0 && mass4e<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+")")
    if (channel=='2e2mu'):
        if (obsName.startswith("mass4l")): data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu),"(mass2e2mu>105.0 && mass2e2mu<140.0)")
        elif (obsName.startswith("abs")):  data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>105.0 && mass2e2mu<140.0 && "+obsName+">="+obsBin_low+" && "+obsName+"<"+obsBin_high+")")
        elif is2DObs: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable,observable2),"(mass2e2mu>105.0 && mass2e2mu<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+" && abs("+obsNameOrig[1]+")>="+obsBin_low2+" && abs("+obsName+")<"+obsBin_high2+")")
        else: data_obs = RooDataSet("data_obs","data_obs",data_obs_tree,RooArgSet(m,mass2e2mu,observable),"(mass2e2mu>105.0 && mass2e2mu<140.0 && abs("+obsName+")>="+obsBin_low+" && abs("+obsName+")<"+obsBin_high+")")
    #for event in range(data_obs.numEntries()):
    #    row = data_obs.get(event)
    #    row.Print("v")
    #data_obs.Print("v")

    # scale systematics
    CMS_zz4l_mean_m_err_1_8 = RooRealVar("CMS_zz4l_mean_m_err_1_8","CMS_zz4l_mean_m_err_1_8",0.0004,0.0004,0.0004)
    CMS_zz4l_mean_e_err_2_8 = RooRealVar("CMS_zz4l_mean_e_err_2_8","CMS_zz4l_mean_e_err_2_8",0.003,0.003,0.003)
    CMS_zz4l_mean_m_err_3_8 = RooRealVar("CMS_zz4l_mean_m_err_3_8","CMS_zz4l_mean_m_err_3_8",0.0004,0.0004,0.0004)
    CMS_zz4l_mean_e_err_3_8 = RooRealVar("CMS_zz4l_mean_e_err_3_8","CMS_zz4l_mean_e_err_3_8",0.003,0.003,0.003)

    wout = RooWorkspace("w","w")

    if (channel=='2e2mu'):
        getattr(wout,'import')(CMS_zz4l_mean_sig_3_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_sig_NoConv_3_8,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_sigma_sig_3_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_alpha_3_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_n_3_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_alpha2_3_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_n2_3_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_m_err_3_8,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_e_err_3_8,RooFit.RecycleConflictNodes())
    if (channel=='4e'):
        getattr(wout,'import')(CMS_zz4l_mean_sig_2_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_sig_NoConv_2_8,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_sigma_sig_2_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_alpha_2_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_n_2_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_alpha2_2_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_n2_2_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_e_err_2_8,RooFit.RecycleConflictNodes())
    if (channel=='4mu'):
        getattr(wout,'import')(CMS_zz4l_mean_sig_1_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_sig_NoConv_1_8,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_sigma_sig_1_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_alpha_1_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_n_1_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_alpha2_1_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_n2_1_8_centralValue,RooFit.RecycleConflictNodes())
        getattr(wout,'import')(CMS_zz4l_mean_m_err_1_8,RooFit.RecycleConflictNodes())

    for genbin in range(nBins):
        # For Silence issue we should shift to ROOT 6.18
        # Reference: https://root-forum.cern.ch/t/rooworkspace-import-roofit-silence-does-not-work-when-importing-datasets/32591/2
        getattr(wout,'import')(trueH_shape[genbin],RooFit.RecycleConflictNodes()) # RooFit.Silence()
        getattr(wout,'import')(trueH_norm[genbin],RooFit.RecycleConflictNodes()) # RooFit.Silence()

    if (not usecfactor):
        out_trueH.SetName("out_trueH")
        getattr(wout,'import')(out_trueH,RooFit.RecycleConflictNodes()) # RooFit.Silence()
        getattr(wout,'import')(out_trueH_norm,RooFit.RecycleConflictNodes()) # RooFit.Silence()

    getattr(wout,'import')(fakeH) # RooFit.Silence()
    getattr(wout,'import')(fakeH_norm) # RooFit.Silence()

    #logger.info("trueH norm: ",n_trueH,"fakeH norm:",n_fakeH)
    qqzzTemplatePdf.SetName("bkg_qqzz")
    qqzzTemplatePdf.Print("v")
    getattr(wout,'import')(qqzzTemplatePdf,RooFit.RecycleConflictNodes()) # RooFit.Silence()
    getattr(wout,'import')(qqzz_norm) # RooFit.Silence()

    ggzzTemplatePdf.SetName("bkg_ggzz")
    ggzzTemplatePdf.Print("v")
    getattr(wout,'import')(ggzzTemplatePdf,RooFit.RecycleConflictNodes())
    getattr(wout,'import')(ggzz_norm) # RooFit.Silence()

    zjetsTemplatePdf.SetName("bkg_zjets")
    zjetsTemplatePdf.Print("v")
    getattr(wout,'import')(zjetsTemplatePdf, RooFit.RecycleConflictNodes()) # RooFit.Silence()
    getattr(wout,'import')(zjets_norm) # RooFit.Silence()

    ## data
    getattr(wout,'import')(data_obs.reduce(RooArgSet(m))) # RooFit.Silence()

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
#createXSworkspace("mass4l", "2e2mu", 2, 0, ["105.0","140.0"], False, True, "ggH_powheg_JHUgen_125", "v2")
