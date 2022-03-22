from ROOT import *
from array import array
import os
from Utils import *

dirMC_94 = '/raid/raid9/qguo/combine/2018_MC_Ntuple/'
dirMC_94 = '/publicfs/cms/user/qyguo/ufl_machine/tools/combine/2018_MC_Ntuple/'
#dirMC_94 = 'root://eosuser.cern.ch//eos/cms/store/group/phys_muon/TagAndProbe/HZZ4L/2018/'
dirMC_94 = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/'
dirMC_94_1 = '/raid/raid7/tjavaid/sig_samples_mc/'    # after copying to the local from Lucien working directory
dirMC_94_Mad = '/raid/raid9/qguo/Run2/after/Run2_2/new/CMSSW_10_2_18/src/'
dirData_94 = 'root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC80X_M17_4l_Feb21/'  # /cms/data/store/user/t2/users/archived/dsperka/Run2/Zprime/2017/rootfiles_Data_Apr16/  #to be added

border_msg("samples directory: "+dirMC_94)


SamplesMC_94 = [
#File missing or needs to be redirected (Vukasin)'GluGluHToZZTo4L_M125_13TeV_powheg2_minloHJ_NNLOPS_JHUgenV702_pythia8.root',   # path needs to be redirected
###
'GluGluHToZZTo4L_M124_2018_slimmed.root',
'GluGluHToZZTo4L_M125_2018_slimmed.root',
'GluGluHToZZTo4L_M126_2018_slimmed.root',
'VBF_HToZZTo4L_M125_2018_slimmed.root',
'WH_HToZZTo4L_M125_2018_slimmed.root',
'ZH_HToZZ_4LFilter_M125_2018_slimmed.root',
'ttH_HToZZ_4LFilter_M125_2018_slimmed.root',
'ggH_amcatnloFXFX_2018_slimmed.root',
'testGGH_nnlops_GENonly_slimmed.root',
#'ggH_amcatnloFXFX__newMuonSF_2018_all.root'
#'ttH_p.root'
]

SamplesData_94 = [
'DoubleEG_Run2017B-17Nov2017-v1.root','DoubleEG_Run2017C-17Nov2017-v1.root','DoubleEG_Run2017D-17Nov2017-v1.root','DoubleEG_Run2017E-17Nov2017-v1.root','DoubleEG_Run2017F-17Nov2017-v1.root',
'DoubleMuon_Run2017-17Nov2017-v1.root','DoubleMuon_Run2017B-17Nov2017-v1.root','DoubleMuon_Run2017C-17Nov2017-v1.root'
]


RootFile = {}
Tree = {}
nEvents = {}
sumw = {}

for i in range(0,len(SamplesMC_94)):

    sample = SamplesMC_94[i].rstrip('.root')


    if ("NNLOPS" in sample):
        RootFile[sample] = TFile(dirMC_94_1+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    elif ("ggH_amcatnloFXFX" in sample):
        RootFile[sample] = TFile(dirMC_94+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    else:
        RootFile[sample] = TFile.Open(dirMC_94+'/'+sample+'.root',"READ")
        Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    h_nevents = RootFile[sample].Get("Ana/nEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")

    if (h_nevents): nEvents[sample] = h_nevents.Integral()
    else: nEvents[sample] = 0.

    if (h_sumw): sumw[sample] = h_sumw.Integral()
    else: sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print('{sample:37}\t nevents: {nevents:11}\t sumw: {sumw}'.format(
            sample = sample, nevents = nEvents[sample], sumw = sumw[sample]))

for i in range(0,len(SamplesData_94)):
    break
    sample = SamplesData_94[i].rstrip('.root')

    RootFile[sample] = TFile(dirData_94+'/'+sample+'.root',"READ")

    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

    h_nevents = RootFile[sample].Get("nEvents")
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

