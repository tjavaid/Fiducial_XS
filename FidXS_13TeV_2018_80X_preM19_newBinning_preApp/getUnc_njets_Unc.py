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
    parser.add_option('-d', '--dir',    dest='SOURCEDIR',  type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--modelName',dest='MODELNAME',type='string',default='SM', help='Name of the Higgs production or spin-parity model, default is "SM", supported: "SM", "ggH", "VBF", "WH", "ZH", "ttH", "exotic","all"')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "mass4l", "pT4l", "massZ2", "rapidity4l", "cosThetaStar", "nets_reco_pt30_eta4p7"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('-f', '--doFit', action="store_true", dest='DOFIT', default=False, help='doFit, default false')
    parser.add_option('-p', '--doPlots', action="store_true", dest='DOPLOTS', default=False, help='doPlots, default false')
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

doFit = opt.DOFIT
doPlots = opt.DOPLOTS

if (not os.path.exists("plots") and doPlots):
    os.system("mkdir plots")

from ROOT import *
from LoadData import *

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)    

if (opt.DOPLOTS and os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()

Histos = {}
acceptance = {}
qcdUncert = {}
pdfUncert = {}

def getunc(channel, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, genbin):    

    obs_gen_low = obs_bins[genbin]
    obs_gen_high = obs_bins[genbin+1]

    obs_gen_lowest = obs_bins[0]
    obs_gen_highest = obs_bins[len(obs_bins)-1]
    
    if (obs_reco.startswith("mass4l")):
        m4l_low = float(obs_gen_low)
        m4l_high = float(obs_gen_high)
        m4l_bins = int((m4l_high-m4l_low)/2)

    i_sample = -1

    print List

    for Sample in List:
        if (not Sample in Tree): continue
        if (not Tree[Sample]): continue

        cutobs_gen = "("+obs_gen+">="+str(obs_gen_low)+")"
        cutm4l_gen     = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
        
        if (channel == "4l"):
            cutchan_gen      = "((abs(GENlep_id[GENlep_Hindex[0]])==11 || abs(GENlep_id[GENlep_Hindex[0]])==13) && (abs(GENlep_id[GENlep_Hindex[2]])==11 || abs(GENlep_id[GENlep_Hindex[2]])==13) )"
            cutchan_gen_out  = "((GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13))"
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
        if (channel == "4e"):
            cutchan_gen      = "(abs(GENlep_id[GENlep_Hindex[0]])==11 && abs(GENlep_id[GENlep_Hindex[2]])==11)"
            cutchan_gen_out  = "(abs(GENZ_DaughtersId[0])==11 && abs(GENZ_DaughtersId[1])==11)"
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
        if (channel == "4mu"):
            cutchan_gen      = "(abs(GENlep_id[GENlep_Hindex[0]])==13 && abs(GENlep_id[GENlep_Hindex[2]])==13)"
            cutchan_gen_out  = "(GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[1]==13)"
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
        if (channel == "2e2mu"):
            cutchan_gen      = "(((abs(GENlep_id[GENlep_Hindex[0]])==11 && abs(GENlep_id[GENlep_Hindex[2]])==13) ||(abs(GENlep_id[GENlep_Hindex[0]])==13 && abs(GENlep_id[GENlep_Hindex[2]])==11)))"
            cutchan_gen_out  = "(((GENZ_DaughtersId[0]==11 && GENZ_DaughtersId[1]==13) || (GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[1]==11)))"   
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
        
        cuth4l_gen  = "(GENlep_MomMomId[GENlep_Hindex[0]]==25 && GENlep_MomMomId[GENlep_Hindex[1]]==25 && GENlep_MomMomId[GENlep_Hindex[2]]==25 && GENlep_MomMomId[GENlep_Hindex[3]]==25)"
        cuth4l_gen  = "1==1"
        cutnoth4l_gen  = "(!"+cuth4l_gen+")"

        if Sample.startswith("ZH"):
            if (channel == "4l"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && GENZ_MomId[1]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13)) || (GENZ_MomId[0]==25 && GENZ_MomId[2]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[2]==13) && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13)) || (GENZ_MomId[1]==25 && GENZ_MomId[2]==25 && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13) && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13)))"
            if (channel == "4e"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && GENZ_MomId[1]==25 && GENZ_DaughtersId[0]==11 && GENZ_DaughtersId[1]==11) || (GENZ_MomId[0]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[0]==11 && GENZ_DaughtersId[2]==11) || (GENZ_MomId[1]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[1]==11 && GENZ_DaughtersId[2]==11))"
            if (channel == "4mu"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && GENZ_MomId[1]==25 && GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[1]==13) || (GENZ_MomId[0]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[2]==13) || (GENZ_MomId[1]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[1]==13 && GENZ_DaughtersId[2]==13))"
            if (channel == "2e2mu"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && GENZ_MomId[1]==25 && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13) && GENZ_DaughtersId[0]!=GENZ_DaughtersId[1]) || (GENZ_MomId[0]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && GENZ_MomId[2]==25 && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13) && GENZ_DaughtersId[0]!=GENZ_DaughtersId[2]) || (GENZ_MomId[1]==25 && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13) && GENZ_MomId[2]==25 && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13) && GENZ_DaughtersId[1]!=GENZ_DaughtersId[2]))"
 
        shortname = sample_shortnames[Sample]
        processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)

        # GEN level        
        Histos[processBin+"fs"] = TH1D(processBin+"fs", processBin+"fs", 100, -1, 10000)
        Histos[processBin+"fs"].Sumw2()
        if ("NNLOPS" in processBin):
            Tree[Sample].Draw("GENmass4l >> "+processBin+"fs","(nnloWeights[0])*("+cutchan_gen_out+")","goff")
        else:
            Tree[Sample].Draw("GENmass4l >> "+processBin+"fs","(qcdWeights[0])*("+cutchan_gen_out+")","goff")
        
        if ("NNLOPS" in processBin):
            for i in range(0,27):
                if (i==5 or i==7 or i==11 or i==14 or i==15 or i==16 or i==17 or i==19 or i==21 or i==22 or i==23 or i==25): continue 

                Histos[processBin+"fid"+str(i)] = TH1D(processBin+"fid"+str(i), processBin+"fid"+str(i), m4l_bins, m4l_low, m4l_high)  
                Histos[processBin+"fid"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fid"+str(i),"(nnloWeights["+str(i)+"])*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
                Histos[processBin+"fid"+str(i)].Scale(1.0/Histos[processBin+"fs"].Integral())

        else:
            for i in [0,1,2,3,4,6,8]:

                Histos[processBin+"fid"+str(i)] = TH1D(processBin+"fid"+str(i), processBin+"fid"+str(i), m4l_bins, m4l_low, m4l_high)  
                Histos[processBin+"fid"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fid"+str(i),"(qcdWeights["+str(i)+"])*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
                Histos[processBin+"fid"+str(i)].Scale(1.0/Histos[processBin+"fs"].Integral())

        Histos[processBin+"fidPDF"] = TH1D(processBin+"fidPDF", processBin+"fidPDF", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"fidPDF"].Sumw2()
        if ("NNLOPS" in processBin):
#            Tree[Sample].Draw("GENmass4l >> "+processBin+"fidPDF","(nnloWeights[0]*pdfENVup)*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
            Tree[Sample].Draw("GENmass4l >> "+processBin+"fidPDF","(nnloWeights[0]*pdfENVup/abs(qcdWeights[0]))*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
        else:
#            Tree[Sample].Draw("GENmass4l >> "+processBin+"fidPDF","(qcdWeights[0]*pdfENVup)*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
            Tree[Sample].Draw("GENmass4l >> "+processBin+"fidPDF","(qcdWeights[0]*pdfENVup/abs(qcdWeights[0]))*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
        Histos[processBin+"fidPDF"].Scale(1.0/Histos[processBin+"fs"].Integral())

        Histos[processBin+"fs"].Scale(1.0/Histos[processBin+"fs"].Integral())

        # GEN level 
        if (Histos[processBin+"fs"].Integral()>0):
            if ("NNLOPS" in processBin):
                print Histos[processBin+"fs"].Integral(),Histos[processBin+"fid0"].Integral()
                acceptance[processBin] = Histos[processBin+"fid0"].Integral()/Histos[processBin+"fs"].Integral()
                qcderrup=0.0; qcderrdn=0.0; 
                for i in range(0,27):
                    if (i==5 or i==7 or i==11 or i==14 or i==15 or i==16 or i==17 or i==19 or i==21 or i==22 or i==23 or i==25): continue 
                    ratio = Histos[processBin+"fid"+str(i)].Integral()-Histos[processBin+"fid0"].Integral()
                    #print i,'ratio',ratio
                    if (ratio>qcderrup): qcderrup = Histos[processBin+"fid"+str(i)].Integral()-Histos[processBin+"fid0"].Integral()
                    if (ratio<qcderrdn): qcderrdn = Histos[processBin+"fid"+str(i)].Integral()-Histos[processBin+"fid0"].Integral()

            else:
                print Histos[processBin+"fs"].Integral(),Histos[processBin+"fid0"].Integral()
                acceptance[processBin] = Histos[processBin+"fid0"].Integral()/Histos[processBin+"fs"].Integral()
                qcderrup=0.0; qcderrdn=0.0; 
                for i in [1,2,3,4,6,8]:
                    ratio = Histos[processBin+"fid"+str(i)].Integral()-Histos[processBin+"fid0"].Integral()
                    #print i,'ratio',ratio
                    if (ratio>qcderrup): qcderrup = Histos[processBin+"fid"+str(i)].Integral()-Histos[processBin+"fid0"].Integral()
                    if (ratio<qcderrdn): qcderrdn = Histos[processBin+"fid"+str(i)].Integral()-Histos[processBin+"fid0"].Integral()


            qcdUncert[processBin] = {"uncerDn":abs(qcderrdn),"uncerUp":abs(qcderrup)}
            if ("NNLOPS" in processBin):
                pdferr = Histos[processBin+"fidPDF"].Integral()/Histos[processBin+"fid0"].Integral()
            else:
                pdferr = Histos[processBin+"fidPDF"].Integral()/Histos[processBin+"fid0"].Integral()
            pdfUncert[processBin] = {"uncerDn":abs(pdferr-1.0),"uncerUp":abs(pdferr-1.0)}


            #print processBin,acceptance[processBin],qcderrup,qcderrdn,pdferr
            
m4l_bins = 35
m4l_low = 105.0
m4l_high = 140.0

# Default to inclusive cross section
obs_reco = 'mass4l'
obs_gen = 'GENmass4l'
obs_reco_low = 105.0
obs_reco_high = 140.0
obs_gen_low = 105.0
obs_gen_high = 140.0

if (opt.OBSNAME == "massZ1"):
    obs_reco = "massZ1"
    obs_gen = "GENmZ1"
if (opt.OBSNAME == "massZ2"):
    obs_reco = "massZ2"
    obs_gen = "GENmZ2"
if (opt.OBSNAME == "pT4l"):
    obs_reco = "pT4l"
    obs_gen = "GENpT4l"
if (opt.OBSNAME == "eta4l"):
    obs_reco = "eta4l"
    obs_gen = "GENeta4l"
if (opt.OBSNAME == "njets_pt30_eta4p7"):
    obs_reco = "njets_pt30_eta4p7"
    obs_gen = "GENnjets_pt30_eta4p7"
if (opt.OBSNAME == "njets_pt30_eta2p5"):
    obs_reco = "njets_pt30_eta2p5"
    obs_gen = "GENnjets_pt30_eta2p5"
if (opt.OBSNAME == "pt_leadingjet_pt30_eta4p7"):
    obs_reco = "pt_leadingjet_pt30_eta4p7"
    obs_gen = "GENpt_leadingjet_pt30_eta4p7"
if (opt.OBSNAME == "pt_leadingjet_pt30_eta2p5"):
    obs_reco = "pt_leadingjet_pt30_eta2p5"
    obs_gen = "GENpt_leadingjet_pt30_eta2p5"
if (opt.OBSNAME == "rapidity4l"):
    obs_reco = "abs(rapidity4l)"
    obs_gen = "abs(GENrapidity4l)"
if (opt.OBSNAME == "cosThetaStar"):
    obs_reco = "abs(cosThetaStar)"
    obs_gen = "abs(GENcosThetaStar)"
if (opt.OBSNAME == "cosTheta1"):
    obs_reco = "abs(cosTheta1)"
    obs_gen = "abs(GENcosTheta1)"
if (opt.OBSNAME == "cosTheta2"):
    obs_reco = "abs(cosTheta2)"
    obs_gen = "abs(GENcosTheta2)"
if (opt.OBSNAME == "Phi"):
    obs_reco = "abs(Phi)"
    obs_gen = "abs(GENPhi)"    
if (opt.OBSNAME == "Phi1"):
    obs_reco = "abs(Phi1)"
    obs_gen = "abs(GENPhi1)"
    
#obs_bins = {0:(opt.OBSBINS.split("|")[1:((len(opt.OBSBINS)-1)/2)]),1:['0','inf']}[opt.OBSNAME=='inclusive'] 
obs_bins = opt.OBSBINS.split("|") 
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins.pop()
obs_bins.pop(0) 

List = []
for long, short in sample_shortnames.iteritems():
    if (not "ggH" in short): continue
    #if ("NNLOPS" in short): continue
    List.append(long)

if (obs_reco=="mass4l"):
    chans = ['4e','4mu','2e2mu','4l']
else:
    chans = ['4e','4mu','2e2mu']
#    chans = ['2e2mu']

for chan in chans:
    for genbin in range(len(obs_bins)-1):
        getunc(chan,List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, genbin)  

if (obs_reco.startswith("njets")):
    for chan in chans:
        for genbin in range(len(obs_bins)-1):
            for Sample in List:
                shortname = sample_shortnames[Sample]
                processBin = shortname+'_'+chan+'_'+obs_reco+'_genbin'+str(genbin)
                processBinPlus1 = shortname+'_'+chan+'_'+obs_reco+'_genbin'+str(genbin+1)
                
                if (genbin==len(obs_bins)-2):
                    qcdUncert[processBin]['uncerUp'] = sqrt(qcdUncert[processBin]['uncerUp']*qcdUncert[processBin]['uncerUp'])/acceptance[processBin]
                    qcdUncert[processBin]['uncerDn'] = sqrt(qcdUncert[processBin]['uncerDn']*qcdUncert[processBin]['uncerDn'])/acceptance[processBin]
                else:
                    acceptance[processBin] = acceptance[processBin]-acceptance[processBinPlus1]
                    qcdUncert[processBin]['uncerUp'] = sqrt(qcdUncert[processBin]['uncerUp']*qcdUncert[processBin]['uncerUp']+qcdUncert[processBinPlus1]['uncerUp']*qcdUncert[processBinPlus1]['uncerUp'])/acceptance[processBin]
                    qcdUncert[processBin]['uncerDn'] = sqrt(qcdUncert[processBin]['uncerDn']*qcdUncert[processBin]['uncerDn']+qcdUncert[processBinPlus1]['uncerDn']*qcdUncert[processBinPlus1]['uncerDn'])/acceptance[processBin]
                
                #print Sample,processBin,qcdUncert[processBin]['uncerUp'],qcdUncert[processBin]['uncerDn']
                    
os.system('cp accUnc_'+opt.OBSNAME+'.py accUnc_'+opt.OBSNAME+'_ORIG.py')
with open('accUnc_'+opt.OBSNAME+'.py', 'w') as f:
    f.write('acc = '+str(acceptance)+' \n')
    f.write('qcdUncert = '+str(qcdUncert)+' \n')
    f.write('pdfUncert = '+str(pdfUncert)+' \n')
