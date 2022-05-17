from ROOT import *
from array import array
import os
from Utils import *

dirMC = {}

#dirMC['2018'] = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/'
#dirMC['2017'] = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/' # 2018 for now until we sort out the locations
#dirMC['2016'] = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/' # 2018 for now until we sort out the locations
dirMC['2018'] = '/eos/user/q/qguo/newNTuple_UL/2018/Slimmed_2p5/'
dirMC['2017'] = '/eos/user/q/qguo/newNTuple_UL/2017/Slimmed_2p5/'
dirMC['2016'] = '/eos/cms/store/group/phys_muon/TagAndProbe/HZZ4L/2016/UL/MC/postVFP/'

dirData_94 = '/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/'  

border_msg("samples directory: "+dirMC['2018'])

SamplesMC = {}
SamplesMC['2018'] = [
#File missing or needs to be redirected (Vukasin)'GluGluHToZZTo4L_M125_13TeV_powheg2_minloHJ_NNLOPS_JHUgenV702_pythia8.root',   # path needs to be redirected
###
'GluGluHToZZTo4L_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluToZH_HToZZTo4L_M125_TuneCP5_13TeV-jhugenv723-pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M120_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M124_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M126_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M130_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M120_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M124_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M125_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M126_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M130_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'tqH_HToZZTo4L_M125_TuneCP5_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
#old#'GluGluHToZZTo4L_M124_2018_slimmed.root',
#old#'GluGluHToZZTo4L_M125_2018_slimmed.root',
#old#'GluGluHToZZTo4L_M126_2018_slimmed.root',
#old#'VBF_HToZZTo4L_M125_2018_slimmed.root',
#old#'WH_HToZZTo4L_M125_2018_slimmed.root',
#old#'ZH_HToZZ_4LFilter_M125_2018_slimmed.root',
#old#'ttH_HToZZ_4LFilter_M125_2018_slimmed.root',
#old#'ggH_amcatnloFXFX_2018_slimmed.root',
#old#'testGGH_nnlops_GENonly_slimmed.root',
#'ggH_amcatnloFXFX__newMuonSF_2018_all.root'
#'ttH_p.root'
]

SamplesMC['2017'] = [
'GluGluHToZZTo4L_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluToZH_HToZZTo4L_M125_TuneCP5_13TeV-jhugenv723-pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M120_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M124_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M126_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M130_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M120_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M124_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M125_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M126_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M130_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'tqH_HToZZTo4L_M125_TuneCP5_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
]

SamplesMC['2016'] = [
'GluGluHToZZTo4L_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'GluGluHToZZTo4L_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'VBF_HToZZTo4L_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WminusH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M120_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M124_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M126_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'WplusH_HToZZTo4L_M130_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M120_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M124_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M126_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ZH_HToZZ_4LFilter_M130_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M120_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M124_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M125_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M126_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'bbH_HToZZTo4L_M130_TuneCP2_13TeV-jhugenv7011-pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M120_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M124_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M126_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
'ttH_HToZZ_4LFilter_M130_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_slimmed_newMuSF_add2p5',
]

SamplesData = {}

SamplesData['2017'] = [
'DoubleEG_Run2017B-17Nov2017-v1.root','DoubleEG_Run2017C-17Nov2017-v1.root','DoubleEG_Run2017D-17Nov2017-v1.root','DoubleEG_Run2017E-17Nov2017-v1.root','DoubleEG_Run2017F-17Nov2017-v1.root',
'DoubleMuon_Run2017-17Nov2017-v1.root','DoubleMuon_Run2017B-17Nov2017-v1.root','DoubleMuon_Run2017C-17Nov2017-v1.root'
]




def GrabMCTrees(era = '2018'):
    RootFile = {}
    Tree = {}
    nEvents = {}
    sumw = {}

    for i in range(0,len(SamplesMC[era])):

        sample = SamplesMC[era][i].rstrip('.root')


        if ("NNLOPS" in sample):
            RootFile[sample] = TFile(dirMC[era]+'/'+sample+'.root',"READ")
            Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

        elif ("ggH_amcatnloFXFX" in sample):
            RootFile[sample] = TFile(dirMC[era]+'/'+sample+'.root',"READ")
            Tree[sample]  = RootFile[sample].Get("Ana/passedEvents")

        else:
            RootFile[sample] = TFile.Open(dirMC[era]+'/'+sample+'.root',"READ")
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

    return RootFile, Tree, nEvents, sumw
