import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames import *

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

if (not os.path.exists("plots_signalnorms")):
    os.system("mkdir plots_signalnorms")

from ROOT import *
from LoadData import *
#LoadData(opt.SOURCEDIR)
save = ""

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)    

if (os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()

Histos = {}
N_sig = {}

def getnorms(channel):
            
    m4lvar = 'mass4l'
    m4l_low  = 105.0
    m4l_high = 140.0

    if (channel=='4mu'): cut = '(passedFullSelection==1 && mass4mu>0.0 && '+m4lvar+' > '+str(m4l_low)+' && '+m4lvar+' < '+str(m4l_high)+')'
    if (channel=='4e'): cut = '(passedFullSelection==1 && mass4e>0.0 && '+m4lvar+' > '+str(m4l_low)+' && '+m4lvar+' < '+str(m4l_high)+')'
    if (channel=='2e2mu'): cut = '(passedFullSelection==1 && mass2e2mu>0.0 && '+m4lvar+' > '+str(m4l_low)+' && '+m4lvar+' < '+str(m4l_high)+')'

    cut_tag = cut+' && @jet_pt.size()>=2 && Djet_VAJHU>0.5'
    cut_untag = cut+' && !(@jet_pt.size()>=2 && Djet_VAJHU>0.5)'

    cuth4l = "((lep_genindex[passedFullSelection*lep_Hindex[0]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[0]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[0]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[0]])]==23 && (lep_genindex[passedFullSelection*lep_Hindex[1]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[1]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[1]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[1]])]==23 && (lep_genindex[passedFullSelection*lep_Hindex[2]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[2]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[2]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[2]])]==23 && (lep_genindex[passedFullSelection*lep_Hindex[3]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[3]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[3]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[3]])]==23)"
    cutnoth4l = "(!"+cuth4l+")"

    List = [
        'GluGluHToZZTo4L_M115_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M120_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M124_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv1-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M126_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M130_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M135_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M140_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M145_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M150_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M155_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'GluGluHToZZTo4L_M160_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'VBF_HToZZTo4L_M115_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'VBF_HToZZTo4L_M120_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'VBF_HToZZTo4L_M124_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'VBF_HToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'VBF_HToZZTo4L_M130_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'VBF_HToZZTo4L_M160_13TeV_powheg2_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M115_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M120_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M126_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M130_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M135_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WminusH_HToZZTo4L_M140_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WplusH_HToZZTo4L_M115_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WplusH_HToZZTo4L_M120_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WplusH_HToZZTo4L_M124_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv1-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2',
        'WplusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WplusH_HToZZTo4L_M126_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv1-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2',
        'WplusH_HToZZTo4L_M130_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WplusH_HToZZTo4L_M135_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'WplusH_HToZZTo4L_M140_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'ZH_HToZZ_4LFilter_M120_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'ZH_HToZZ_4LFilter_M124_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'ZH_HToZZ_4LFilter_M126_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1',
        'ZH_HToZZ_4LFilter_M140_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1'
        ]
        #print List

        
    for Sample in List:
        if (not Sample in Tree): 
            print Sample,'missing from LoadData'
            continue
        if (not Tree[Sample]): continue

        weight = '(genWeight/'+str(sumw[Sample])+')'

        shortname = Sample.split('_13TeV')[0]
        processBin = shortname+'_'+channel+'_'+m4lvar

        Histos[processBin+"res_tag"] = TH1D(processBin+"res_tag", processBin+"res_tag", 1, m4l_low, m4l_high)
        Histos[processBin+"res_tag"].Sumw2()

        Histos[processBin+"res_untag"] = TH1D(processBin+"res_untag", processBin+"res_untag", 1, m4l_low, m4l_high)
        Histos[processBin+"res_untag"].Sumw2()

        Histos[processBin+"nonres_tag"] = TH1D(processBin+"nonres_tag", processBin+"nonres_tag", 1, m4l_low, m4l_high)
        Histos[processBin+"nonres_tag"].Sumw2()

        Histos[processBin+"nonres_untag"] = TH1D(processBin+"nonres_untag", processBin+"nonres_untag", 1, m4l_low, m4l_high)
        Histos[processBin+"nonres_untag"].Sumw2()

        # RECO level 
        Tree[Sample].Draw(m4lvar+" >> "+processBin+"res_tag","("+weight+")*("+cuth4l+" && "+cut_tag+")","goff") 
        Tree[Sample].Draw(m4lvar+" >> "+processBin+"res_untag","("+weight+")*("+cuth4l+" && "+cut_untag+")","goff") 
        Tree[Sample].Draw(m4lvar+" >> "+processBin+"nonres_tag","("+weight+")*("+cutnoth4l+" && "+cut_tag+")","goff") 
        Tree[Sample].Draw(m4lvar+" >> "+processBin+"nonres_untag","("+weight+")*("+cutnoth4l+" && "+cut_untag+")","goff") 


        N_sig[processBin+'_res_tag'] = Histos[processBin+"res_tag"].GetBinContent(1)
        N_sig[processBin+'_res_untag'] = Histos[processBin+"res_untag"].GetBinContent(1)
        N_sig[processBin+'_nonres_tag'] = Histos[processBin+"nonres_tag"].GetBinContent(1)
        N_sig[processBin+'_nonres_untag'] = Histos[processBin+"nonres_untag"].GetBinContent(1)

        N_sig[processBin+'_res_tag_err'] = Histos[processBin+"res_tag"].GetBinError(1)
        N_sig[processBin+'_res_untag_err'] = Histos[processBin+"res_untag"].GetBinError(1)
        N_sig[processBin+'_nonres_tag_err'] = Histos[processBin+"nonres_tag"].GetBinError(1)
        N_sig[processBin+'_nonres_untag_err'] = Histos[processBin+"nonres_untag"].GetBinError(1)

        print processBin,"res_tag",round(N_sig[processBin+'_res_tag'],4),"res_untag",round(N_sig[processBin+'_res_untag'],4),"nonres_tag",round(N_sig[processBin+'_nonres_tag'],4),"nonres_untag",round(N_sig[processBin+'_nonres_untag'],4)

    os.system('cp plots_signalnorms/signorms_'+m4lvar+'_'+channel+'.py plots_signalnorms/signorm_'+m4lvar+'_'+channel+'_ORIG.py')
    with open('plots_signalnorms/signorms_'+m4lvar+'_'+channel+'_test.py', 'w') as f:
        f.write('N_sig = '+str(N_sig)+' \n')


chans = ['4e','4mu','2e2mu']
#chans = ['2e2mu']
for chan in chans:
    getnorms(chan)

