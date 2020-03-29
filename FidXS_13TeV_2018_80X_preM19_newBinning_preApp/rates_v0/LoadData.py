from ROOT import *
from array import array
import os


# 80X samples
#dirMC_80 = '/cms/data/store/user/t2/users/dsperka/rootfiles_MC80X_20160712/'
#dirMC_80 = '/cms/data/store/user/t2/users/dsperka/dsperka/rootfiles_MC80X_20160725/'
#dirMC_80 = '/raid/raid5/dsperka/Run2/HZZ4l/CMSSW_8_0_25/src/'
#dirMC_80 = '/cms/data/store/user/t2/users/dsperka/Run2/HZZ4l/SubmitArea_13TeV/rootfiles_MC80X_4lskim_M17_Feb21/'
#dirMC_80 = '/raid/raid7/lucien/Higgs/DarkZ-NTuple/20180702/Tree_BkgMC/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUGenV7011_pythia8'    
#dirMC_94 = '/MC_files'    # copied MC samples from Lucien to local
#dirMC_94 = '/home/tjavaid/fiducial_XS/CMSSW_7_4_7/src/FidXS_13TeV_2016_80X_postM17/MC_files'    # copied MC samples from Lucien to local
#dirMC_94 = '/cms/data/store/user/t2/users/klo/Higgs/DarkZ/NTuples/BkgMC_Run2017/'    # copied MC samples from Lucien to local
#dirMC_94 = '/store/user/t2/users/klo/Higgs/DarkZ/NTuples/BkgMC_Run2017/'    # copied MC samples from Lucien to local
#dirMC_94 = '/cms/data/store/user/t2/users/klo/Higgs/DarkZ/NTuples/BkgMC_Run2017/'    # copied MC samples from Lucien to local
##dirMC_94 = '/store/user/t2/users/klo/Higgs/DarkZ/NTuples/BkgMC_Run2017/'    # copied MC samples from Lucien to local
##dirMC_94 = '/raid/raid7/tjavaid/sig_samples_mc/'    # after copying to the local from Lucien working directory
#dirData_80 = '/cms/data/store/user/t2/users/dsperka/rootfiles_Data80X_20160712_4lSkim/'
#dirData_80 = 'root://cmsio5.rc.ufl.edu/store/user/t2/users/archived/dsperka/Run2/Zprime/2017/rootfiles_Data_Apr6/'  # /cms/data/store/user/t2/users/archived/dsperka/Run2/Zprime/2017/rootfiles_Data_Apr16/  #to be added
dirData_94 = '/raid/raid7/tjavaid/data_root_files_2017'  # /cms/data/store/user/t2/users/archived/dsperka/Run2/Zprime/2017/rootfiles_Data_Apr16/  #to be added

##dirMC_94 = '/raid/raid7/tjavaid/sig_samples_mc/'    # for data MC
##dirMC_94='/raid/raid7/tjavaid/bkg_samples'   # background
#dirMC_94='/store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Feb1_noCorrections_bestCandLegacy/'
#dirMC_94='/store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Feb19_fixGENjet_bestCandLegacy/'
dirMC_94='/store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Feb28_NewSF_2017Jets_bestCandLegacy/'



#SamplesMC_80 = [
##'GluGluHToZZTo4L_M120_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
##'GluGluHToZZTo4L_M124_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'GluGluHToZZTo4L_M125_13TeV_powheg2_minloHJ_NNLOPS_JHUgenV702_pythia8_RunIISummer16MiniAODv2.root',
##'GluGluHToZZTo4L_M126_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
##'GluGluHToZZTo4L_M130_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'VBF_HToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'WminusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'WplusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'WH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'ttH_HToZZ_4LFilter_M125_13TeV_powheg2_JHUgenV6_pythia8_RunIISummer16MiniAODv2.root',
#'testGGH_nnlops_noIso.root',
#'testGGH_nnlops.root',
#'testGGH_nnlops_tightIso.root',
#'testTTH_noIso.root',
#'testTTH.root',
#'testTTH_tightIso.root',
#'testGGH_nnlops_GENonly.root',
#]

#SamplesData_80 = [
#'Data_2016_4lskim.root'
#]

SamplesMC_94 = [
'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8.root',
'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8.root',
'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8.root',
##'ZZTo4L_13TeV_powheg_pythia8.root',
'ZZTo4L_TuneCP5_13TeV_powheg_pythia8.root',
#'ZZTo4L_ext1_13TeV_powheg_pythia8.root',
]

SamplesData_94 = [
#'DoubleEG_Run2017B-17Nov2017-v1.root','DoubleEG_Run2017C-17Nov2017-v1.root','DoubleEG_Run2017D-17Nov2017-v1.root','DoubleEG_Run2017E-17Nov2017-v1.root','DoubleEG_Run2017F-17Nov2017-v1.root',
#'DoubleMuon_Run2017-17Nov2017-v1.root','DoubleMuon_Run2017B-17Nov2017-v1.root','DoubleMuon_Run2017C-17Nov2017-v1.root', 
'data_13TeV_2017_duplicated_removed.root'
]
###################################################### 
RootFile = {} 
Tree = {} 
nEvents = {} 
sumw = {}


# 80X MC
for i in range(0,len(SamplesMC_94)):

#    sample = SamplesMC_80[i].rstrip('.root')
    sample = SamplesMC_94[i].rstrip('.root')
#    sample = SamplesMC_94[i].replace('.root','')

#    RootFile[sample] = TFile(dirMC_94+'/'+sample+'.root',"READ")
    RootFile[sample] = TFile.Open('root://cmsio5.rc.ufl.edu/'+dirMC_94+'/'+sample+'.root',"READ")
#ROOT.TFile.Open("root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/DarkZ/NTuples/BkgMC_Run2017/blah.root")
#    RootFile[sample] = TFile.Open('root://cmsio5.rc.ufl.edu/'+dirMC_94+'/'+sample+'.root',"READ")
##    RootFile[sample] = TFile.Open('root://cms-xrd-global.cern.ch//store/test/xrootd/T2_US_Florida/'+dirMC_94+'/'+sample+'.root',"READ")
##    RootFile[sample] = TFile('root://cms-xrd-global.cern.ch//store/test/xrootd/T2_US_Florida/'+dirMC_94+'/'+sample+'.root',"READ")
#    RootFile[sample] = TFile.Open('gsiftp://cmsio.rc.ufl.edu/cms/data/'+dirMC_94+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    h_nevents = RootFile[sample].Get("Ana/nEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")

    if (h_nevents): nEvents[sample] = h_nevents.Integral()
    else: nEvents[sample] = 0.

    if (h_sumw): sumw[sample] = h_sumw.Integral()
    else: sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]

for i in range(0,len(SamplesData_94)):

    sample = SamplesData_94[i].rstrip('.root')

    RootFile[sample] = TFile.Open(dirData_94+'/'+sample+'.root',"READ")

##    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
    Tree[sample]  = RootFile[sample].Get("passedEvents")

##    h_nevents = RootFile[sample].Get("Ana/nEvents")
    h_nevents = RootFile[sample].Get("nEvents")
##    h_sumw = RootFile[sample].Get("Ana/sumWeights")
    h_sumw = RootFile[sample].Get("sumWeights")

    if (h_nevents):
        nEvents[sample] = h_nevents.Integral()
        sumw[sample] = h_sumw.Integral()
    else:
        nEvents[sample] = 0.
        sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]
    
