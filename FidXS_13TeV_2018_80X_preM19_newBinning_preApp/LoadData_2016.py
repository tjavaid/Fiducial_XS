from ROOT import *
from array import array
import os
from datapaths_full import *

# 80X samples
#dirMC_80 = 'root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC80X_M17_4l_Feb21/'

dirMC_80_PAS = 'root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC80X_M17_4l_Feb21_fixGenPtJet/' #PAS 
#dirMC_80 = '/store/user/t2/users/ferrico/chenguan/2016/MC/' # filippo from Chengguang
#dirMC_80 = 'samples_newSF/' #/store/user/t2/users/ferrico/chenguan/2016/MC/' # filippo from Chengguang
#dirMC_80 = 'root://cmsio5.rc.ufl.edu//cmsuf/data/store/user/qguo/raid/fiducial/ntuple_2016/' # Qianying
#dirMC_80 = 'root://cmsio5.rc.ufl.edu//store/user/qguo/raid/fiducial/ntuple_2016/' # Qianying
#dirMC_80 = '../samples_2016/'
#dirMC_80 = '/publicfs/cms/data/hzz/jtahir/legacy2016/samples_2016/'
#dirMC_80 = '/eos/cms/store/group/phys_muon/TagAndProbe/HZZ4L/legacy_2016/'


#dirMC_80 = 'root://eoscms.cern.ch//eos/cms/store/group/phys_muon/TagAndProbe/HZZ4L/legacy_2016/slimmed/'
dirMC_80 = datapaths["2016"]["MC"] 
print "the sample directory is : ", dirMC_80
#dirMC_80 = "$CMSSW_BASE/src/ntup/"

dirMC_80_1 = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/'

#dirMC_80_temp = '/raid/raid9/ahmad/temp_WH/'
#dirData_80 = 'root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/Data_80XM17_FebCombined/'
#dirData_80 = '/publicfs/cms/data/hzz/jtahir/legacy2016/'
dirData_80 = '/eos/cms/store/group/phys_muon/TagAndProbe/HZZ4L/legacy_2016/'
SamplesMC_80 = [
'GluGluHToZZTo4L_M124_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'GluGluHToZZTo4L_M125_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'GluGluHToZZTo4L_M126_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'GluGluHToZZTo4L_M130_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'VBF_HToZZTo4L_M125_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
'WH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUGenV709_pythia8_slimmed.root',
'ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUGenV709_pythia8_slimmed.root',
'ttH_HToZZ_4LFilter_M125_13TeV_powheg2_JHUGenV709_pythia8_slimmed.root',
#'testGGH_nnlops_GENonly_slimmed.root',
#'ggH_amcatnloFXFX_2018_slimmed.root'
#'2016GGH_125.root',

#'GluGluHToZZTo4L_M125_13TeV_powheg2_minloHJ_NNLOPS_JHUgenV702_pythia8.root',

#'2016VBF_125.root',
#'2016WH_125.root',
#'2016ZH_125.root',
#'2016ttH_125.root'
]

SamplesData_80 = [
'data_legacy2016_17Jul2018_noDuplicates.root'
#'Data_Run2016-03Feb2017_noDuplicates.root'
]


###################################################### 
RootFile = {} 
Tree = {} 
nEvents = {} 
sumw = {}


# 80X MC
for i in range(0,len(SamplesMC_80)):

    #sample = SamplesMC_80[i].rstrip('.root')
    sample = SamplesMC_80[i].replace('.root','')
 #   if (SamplesMC_80[i].startswith('WH')):
#        RootFile[sample] = TFile.Open(dirMC_80_temp+'/'+sample+'.root',"READ")
#    else:
#        RootFile[sample] = TFile.Open(dirMC_80+'/'+sample+'.root',"READ")
    print "sample is", sample
    #if sample=="GluGluHToZZTo4L_M125_13TeV_powheg2_minloHJ_NNLOPS_JHUgenV702_pythia8":
    if ("nnlops" in sample or "amcatnloFXFX" in sample):
        RootFile[sample] = TFile.Open(dirMC_80_1+'/'+sample+'.root',"READ")
    else:
        RootFile[sample] = TFile.Open(dirMC_80+'/'+sample+'.root',"READ")
        #RootFile[sample] = TFile.Open('root://cmsio5.rc.ufl.edu/'+dirMC_80+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
    if (not Tree[sample]): Tree[sample] = RootFile[sample].Get("passedEvents")

#    h_nevents = RootFile[sample].Get("Ana/nEvents")
#    h_sumw = RootFile[sample].Get("Ana/sumWeights")
#
#
#    if (h_nevents): nEvents[sample] = h_nevents.Integral()
#    else: nEvents[sample] = 0.
    h_nevents = RootFile[sample].Get("Ana/passedEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")

    #if (h_nevents): nEvents[sample] = h_nevents.Integral()
    if (h_nevents): nEvents[sample] = h_nevents.GetEntries() #Integral()

    if (h_sumw): sumw[sample] = h_sumw.Integral()
    else: sumw[sample] = 0.

    if (not Tree[sample]): print sample+' has no passedEvents tree'
    else:
        print sample,"nevents",nEvents[sample],"sumw",sumw[sample]



for i in range(0,len(SamplesData_80)):

    sample = SamplesData_80[i].rstrip('.root')

    RootFile[sample] = TFile.Open(dirData_80+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("passedEvents")

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
    
