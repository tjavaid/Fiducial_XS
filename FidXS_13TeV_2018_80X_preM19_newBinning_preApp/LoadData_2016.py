from ROOT import *
from array import array
import os


# 80X samples
dirMC_80 = 'root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC80X_M17_4l_Feb21/'
dirMC_80_temp = '/raid/raid9/ahmad/temp_WH/'
dirData_80 = 'root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/Data_80XM17_FebCombined/'
SamplesMC_80 = [
'GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8.root',
'GluGluHToZZTo4L_M125_13TeV_powheg2_minloHJ_NNLOPS_JHUgenV702_pythia8.root',
'VBF_HToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8.root',
'WH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8.root',
'ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8.root',
'ttH_HToZZ_4LFilter_M125_13TeV_powheg2_JHUgenV6_pythia8.root'
]

SamplesData_80 = [
'Data_Run2016-03Feb2017_noDuplicates.root'
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
    if (SamplesMC_80[i].startswith('WH')):
        RootFile[sample] = TFile.Open(dirMC_80_temp+'/'+sample+'.root',"READ")
    else:
        RootFile[sample] = TFile.Open(dirMC_80+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
    if (not Tree[sample]): Tree[sample] = RootFile[sample].Get("passedEvents")

    h_nevents = RootFile[sample].Get("Ana/nEvents")
    h_sumw = RootFile[sample].Get("Ana/sumWeights")


    if (h_nevents): nEvents[sample] = h_nevents.Integral()
    else: nEvents[sample] = 0.

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
    
