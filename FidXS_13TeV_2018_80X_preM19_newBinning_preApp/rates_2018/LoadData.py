from ROOT import *
from array import array
import os

dirData_94 ='/eos/user/v/vmilosev/Skim_2018_HZZ/WoW/'

print "data  directory: ", dirData_94

dirMC_94 = '/eos/user/v/vmilosev/Skim_2018_HZZ/WoW//'    #  


print "samples directory: ", dirMC_94


SamplesMC_94 = [
'GluGluToContinToZZTo2e2mu_M125_2018_slimmed.root',
'GluGluToContinToZZTo4mu_M125_2018_slimmed.root',
'GluGluToContinToZZTo4e_M125_2018_slimmed.root',
'ZZTo4L_powheg_ext1_slimmed.root'
]

SamplesData_94 = [
'2018_noDuplicates.root',
]
###################################################### 
RootFile = {} 
Tree = {} 
nEvents = {} 
sumw = {}


# 80X MC
for i in range(0,len(SamplesMC_94)):

    sample = SamplesMC_94[i].rstrip('.root')

    RootFile[sample] = TFile(dirMC_94+'/'+sample+'.root',"READ")
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

#    Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")
    Tree[sample]  = RootFile[sample].Get("passedEvents")

#    h_nevents = RootFile[sample].Get("Ana/nEvents")
    #h_nevents = RootFile[sample].Get("nEvents")
    h_nevents = RootFile[sample].Get("nEvents")
#    h_sumw = RootFile[sample].Get("Ana/sumWeights")
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
    
