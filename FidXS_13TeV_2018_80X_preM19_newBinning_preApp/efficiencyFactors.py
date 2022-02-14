import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames import *
#from sample_shortnames_2016 import *
#from sample_shortnames_2017 import *
#from sample_shortnames_2018 import *
from datetime import datetime
now = datetime.now() # current date and time
#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
date = now.strftime("%d%m%Y")
print "date is..................", date

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
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='mass4l',   help='Name of the observalbe, supported: "mass4l", "pT4l", "massZ2", "rapidity4l", "cosThetaStar", "nets_reco_pt30_eta4p7"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('-f', '--doFit', action="store_true", dest='DOFIT', default=False, help='doFit, default false')
    parser.add_option('-p', '--doPlots', action="store_true", dest='DOPLOTS', default=False, help='doPlots, default false')
    parser.add_option('-c', '--channel', dest="CHAN", type='string', default='', help='only do one channel')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
    parser.add_option('',   '--year',  dest='YEAR',  type='string',default='2018',   help='Year to analyze, e.g. 2016, 2017 or 2018 ')                       
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs

year = opt.YEAR
print "year being processed: ",year

doFit = opt.DOFIT
doPlots = opt.DOPLOTS

#if (not os.path.exists("plots_"+year+"_"+date)):
#    os.system("mkdir plots_"+year+"_"+date)
#if (not os.path.exists("Eff_plots_"+year+"/"+opt.OBSNAME)):
#    os.system("mkdir -p Eff_plots_"+year+"/"+opt.OBSNAME)

#if (not os.path.exists("plots") and doPlots):
#    os.system("mkdir plots")

from ROOT import *
#from LoadData import *
#LoadData(opt.SOURCEDIR)
save = ""

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)    

if (opt.DOPLOTS and os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()
    
    if (not os.path.exists("Eff_plots_"+year+"/"+opt.OBSNAME)):
        os.system("mkdir -p Eff_plots_"+year+"/"+opt.OBSNAME)

Histos = {}
wrongfrac = {}
dwrongfrac = {}
binfrac_wrongfrac = {}
dbinfrac_wrongfrac = {}
outfrac = {}
doutfrac = {}
binfrac_outfrac = {}
dbinfrac_outfrac = {}
outinratio = {}
doutinratio = {}
CB_mean_post = {}
CB_sigma_post = {}
CB_dmean_post = {}
CB_dsigma_post = {}
Landau_mean_post = {}
Landau_sigma_post = {}
effrecotofid = {}
deffrecotofid = {}
acceptance = {}
dacceptance = {}
acceptance_4l = {}
dacceptance_4l = {}
cfactor = {}
dcfactor = {}
lambdajesup = {}
lambdajesdn = {}
eff_fit = {}
deff_fit = {}
effanyreco = {}
deffanyreco = {}
folding = {}
dfolding = {}

def geteffs(channel, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin):    
    gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    gSystem.Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
    gSystem.AddIncludePath("-I$ROOFITSYS/include")

    #recoweight = "genWeight*pileupWeight*dataMCWeight"
    
    if ("NNLOPS" in sample or "nnlops" in sample):
        print ("Will skip: "+ sample)
    #    recoweight = "genWeight*pileupWeight*dataMCWeight"
    #else:
    #    recoweight = "genWeight*pileupWeight*dataMCWeight"
    recoweight = "genWeight*pileupWeight*dataMCWeight"
    #recoweight = "genWeight"
    #recoweight = "totalWeight"
    #recoweight = "1.0"
    
    obs_reco_low = obs_bins[recobin]
    obs_reco_high = obs_bins[recobin+1]

    obs_gen_low = obs_bins[genbin]
    obs_gen_high = obs_bins[genbin+1]

    obs_gen_lowest = obs_bins[0]
    obs_gen_highest = obs_bins[len(obs_bins)-1]
    
    if (obs_reco.startswith("mass4l")):
        m4l_low = float(obs_reco_low)
        m4l_high = float(obs_reco_high)
        m4l_bins = int((m4l_high-m4l_low)/2)

    i_sample = -1

    print List

    for Sample in List:
	
        if ("NNLOPS" in Sample or "nnlops" in Sample):
            print ("Skipping: "+ sample)
            recoweight = "genWeight*pileupWeight*dataMCWeight"
            continue
        else:
            recoweight = "genWeight*pileupWeight*dataMCWeight"
	
        if (not Sample in Tree): continue
        if (not Tree[Sample]): continue
        i_sample = i_sample+1
	#if (Sample.startswith("VBF")):
	#    recoweight = "(1.0)*pileupWeight*dataMCWeight"

#        shortname = sample_shortnames[Sample]
	if year =="2018": shortname = sample_shortnames_2018[Sample]
        elif year =="2017": shortname = sample_shortnames_2017[Sample]
        else: shortname = sample_shortnames_2016[Sample]
        print "short name is: ",shortname

        processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin)+'_recobin'+str(recobin)

#        if ((not "jet" in opt.OBSNAME) and abs(genbin-recobin)>1):
	if (((not "jet" in opt.OBSNAME) or (not "Jet" in opt.OBSNAME) or (not "j1" in opt.OBSNAME) or (not "j2" in opt.OBSNAME) or (not "4lj" in opt.OBSNAME)) and abs(genbin-recobin)>1):
            acceptance[processBin] = 0.0
            dacceptance[processBin] = 0.0
            acceptance_4l[processBin] = 0.0
            dacceptance_4l[processBin] = 0.0
            wrongfrac[processBin] = 0.0
            dwrongfrac[processBin] = 0.0
            binfrac_wrongfrac[processBin] = 0.0
            dbinfrac_wrongfrac[processBin] = 0.0
            outfrac[processBin] =  0.0
            doutfrac[processBin] = 0.0
            binfrac_outfrac[processBin] =  0.0
            dbinfrac_outfrac[processBin] = 0.0                                                                       
            effrecotofid[processBin] = 0.000001
            deffrecotofid[processBin] = 0.00001
            cfactor[processBin] = 0.0
            folding[processBin] = 0.0
            dfolding[processBin] = 0.0
            outinratio[processBin] = 0.0
            doutinratio[processBin] = 0.0
            lambdajesup[processBin] = 0.0
            lambdajesdn[processBin] = 0.0
            continue


        cutobs_reco = "("+obs_reco+">="+str(obs_reco_low)+" && "+obs_reco+"<"+str(obs_reco_high)+")"
        cutobs_gen = "("+obs_gen+">="+str(obs_gen_low)+" && "+obs_gen+"<"+str(obs_gen_high)+")"
        print "cutobs_gen : ", cutobs_gen
#        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
	if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME) or ("j1" in opt.OBSNAME)  or ("j2" in opt.OBSNAME) or ("4lj" in opt.OBSNAME)): 
           cutobs_reco_jesup = "("+obs_reco+"_jesup"+">="+str(obs_reco_low)+" && "+obs_reco+"_jesup"+"<"+str(obs_reco_high)+")"
           cutobs_reco_jesdn = "("+obs_reco+"_jesdn"+">="+str(obs_reco_low)+" && "+obs_reco+"_jesdn"+"<"+str(obs_reco_high)+")"
            
        cutobs_gen_otherfid = "(("+obs_gen+"<"+str(obs_gen_low)+" && "+obs_gen+">="+str(obs_gen_lowest)+") || ("+obs_gen+">="+str(obs_gen_high)+" && "+obs_gen+"<="+str(obs_gen_highest)+"))"
        cutm4l_gen     = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
        cutm4l_reco    = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+")" 
        
        if (channel == "4l"):
            cutchan_gen      = "((abs(GENlep_id[GENlep_Hindex[0]])==11 || abs(GENlep_id[GENlep_Hindex[0]])==13) && (abs(GENlep_id[GENlep_Hindex[2]])==11 || abs(GENlep_id[GENlep_Hindex[2]])==13))"
            cutchan_gen_out  = "((GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13))"
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4l>"+str(m4l_low)+" && mass4l<"+str(m4l_high)+")"                        
        if (channel == "4e"):
            cutchan_gen      = "(abs(GENlep_id[GENlep_Hindex[0]])==11 && abs(GENlep_id[GENlep_Hindex[2]])==11)"
            cutchan_gen_out  = "(abs(GENZ_DaughtersId[0])==11 && abs(GENZ_DaughtersId[1])==11)"
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4e>"+str(m4l_low)+" && mass4e<"+str(m4l_high)+")"                        
        if (channel == "4mu"):
            cutchan_gen      = "(abs(GENlep_id[GENlep_Hindex[0]])==13 && abs(GENlep_id[GENlep_Hindex[2]])==13)"
            cutchan_gen_out  = "(GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[1]==13)"
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass4mu>"+str(m4l_low)+" && mass4mu<"+str(m4l_high)+")"                        
        if (channel == "2e2mu"):
            cutchan_gen      = "((abs(GENlep_id[GENlep_Hindex[0]])==11 && abs(GENlep_id[GENlep_Hindex[2]])==13) ||(abs(GENlep_id[GENlep_Hindex[0]])==13 && abs(GENlep_id[GENlep_Hindex[2]])==11))"
            cutchan_gen_out  = "((GENZ_DaughtersId[0]==11 && GENZ_DaughtersId[1]==13) || (GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[1]==11))"   
            cutm4l_gen       = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"
            cutm4l_reco      = "(mass2e2mu>"+str(m4l_low)+" && mass2e2mu<"+str(m4l_high)+")"
        
        cuth4l_gen  = "(GENlep_MomMomId[GENlep_Hindex[0]]==25 && GENlep_MomMomId[GENlep_Hindex[1]]==25 && GENlep_MomMomId[GENlep_Hindex[2]]==25 && GENlep_MomMomId[GENlep_Hindex[3]]==25)"
        cuth4l_reco = "((lep_genindex[passedFullSelection*lep_Hindex[0]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[0]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[0]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[0]])]==23 && (lep_genindex[passedFullSelection*lep_Hindex[1]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[1]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[1]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[1]])]==23 && (lep_genindex[passedFullSelection*lep_Hindex[2]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[2]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[2]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[2]])]==23 && (lep_genindex[passedFullSelection*lep_Hindex[3]]>-0.5)*GENlep_MomMomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[3]])]==25 && (lep_genindex[passedFullSelection*lep_Hindex[3]]>-0.5)*GENlep_MomId[max(0,lep_genindex[passedFullSelection*lep_Hindex[3]])]==23)"

        cutnoth4l_gen  = "(!"+cuth4l_gen+")"
        cutnoth4l_reco = "(!"+cuth4l_reco+")"

        if Sample.startswith("ZH"):
            if (channel == "4l"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && GENZ_MomId[1]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13)) || (GENZ_MomId[0]==25 && GENZ_MomId[2]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[2]==13) && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13)) || (GENZ_MomId[1]==25 && GENZ_MomId[2]==25 && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13) && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13)))"
            if (channel == "4e"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && GENZ_MomId[1]==25 && GENZ_DaughtersId[0]==11 && GENZ_DaughtersId[1]==11) || (GENZ_MomId[0]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[0]==11 && GENZ_DaughtersId[2]==11) || (GENZ_MomId[1]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[1]==11 && GENZ_DaughtersId[2]==11))"
            if (channel == "4mu"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && GENZ_MomId[1]==25 && GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[1]==13) || (GENZ_MomId[0]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[0]==13 && GENZ_DaughtersId[2]==13) || (GENZ_MomId[1]==25 && GENZ_MomId[2]==25 && GENZ_DaughtersId[1]==13 && GENZ_DaughtersId[2]==13))"
            if (channel == "2e2mu"):
                cutchan_gen_out  = "((GENZ_MomId[0]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && GENZ_MomId[1]==25 && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13) && GENZ_DaughtersId[0]!=GENZ_DaughtersId[1]) || (GENZ_MomId[0]==25 && (GENZ_DaughtersId[0]==11 || GENZ_DaughtersId[0]==13) && GENZ_MomId[2]==25 && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13) && GENZ_DaughtersId[0]!=GENZ_DaughtersId[2]) || (GENZ_MomId[1]==25 && (GENZ_DaughtersId[1]==11 || GENZ_DaughtersId[1]==13) && GENZ_MomId[2]==25 && (GENZ_DaughtersId[2]==11 || GENZ_DaughtersId[2]==13) && GENZ_DaughtersId[1]!=GENZ_DaughtersId[2]))"
 
        if (recoweight=="totalWeight"): genweight = "10000.0*genWeight/"+str(sumw[Sample])
        else:  genweight = "genWeight"

        # RECO level
        Histos[processBin+"reco_inc"] = TH1D(processBin+"reco_inc", processBin+"reco_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reco_inc"].Sumw2()        
        Histos[processBin+"recoh4l"] = TH1D(processBin+"recoh4l", processBin+"recoh4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4l"].Sumw2()
        Histos[processBin+"recoh4l_inc"] = TH1D(processBin+"recoh4l_inc", processBin+"recoh4l_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4l_inc"].Sumw2() 
        Histos[processBin+"reconoth4l"] = TH1D(processBin+"reconoth4l", processBin+"reconoth4l", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reconoth4l"].Sumw2() 
        Histos[processBin+"reconoth4l_inc"] = TH1D(processBin+"reconoth4l_inc", processBin+"reconoth4l_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"reconoth4l_inc"].Sumw2()                 
        #if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
	if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME) or ("j1" in opt.OBSNAME)  or ("j2" in opt.OBSNAME) or ("4lj" in opt.OBSNAME)): 
            Histos[processBin+"recoh4l_jesup"] = TH1D(processBin+"recoh4l_jesup", processBin+"recoh4l_jesup", m4l_bins, m4l_low, m4l_high)
            Histos[processBin+"recoh4l_jesup"].Sumw2()
            Histos[processBin+"recoh4l_jesdn"] = TH1D(processBin+"recoh4l_jesdn", processBin+"recoh4l_jesdn", m4l_bins, m4l_low, m4l_high)
            Histos[processBin+"recoh4l_jesdn"].Sumw2()
                                    
        # GEN level
        Histos[processBin+"fid"] = TH1D(processBin+"fid", processBin+"fid", m4l_bins, m4l_low, m4l_high)  
        Histos[processBin+"fid"].Sumw2()
        Histos[processBin+"fs"] = TH1D(processBin+"fs", processBin+"fs", 100, -1, 10000)
        Histos[processBin+"fs"].Sumw2()
        
        # RECO and GEN level ( e.g. f(in) and f(out) )
        Histos[processBin+"recoh4lfid"] = TH1D(processBin+"recoh4lfid", processBin+"recoh4lfid", m4l_bins, m4l_low, m4l_high)        
        Histos[processBin+"recoh4lfid"].Sumw2()
        Histos[processBin+"anyrecoh4lfid"] = TH1D(processBin+"anyrecoh4lfid", processBin+"anyrecoh4lfid", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"anyrecoh4lfid"].Sumw2()                
        Histos[processBin+"recoh4lnotfid"] = TH1D(processBin+"recoh4lnotfid", processBin+"recoh4lnotfid", m4l_bins, m4l_low, m4l_high)        
        Histos[processBin+"recoh4lnotfid"].Sumw2() 
        Histos[processBin+"recoh4lnotfid_inc"] = TH1D(processBin+"recoh4lnotfid_inc", processBin+"recoh4lnotfid_inc", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4lnotfid_inc"].Sumw2() 
        Histos[processBin+"recoh4lotherfid"] = TH1D(processBin+"recoh4lotherfid", processBin+"recoh4lotherfid", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"recoh4lotherfid"].Sumw2()
        
        # GEN level 
        Tree[Sample].Draw("GENmass4l >> "+processBin+"fid","("+genweight+")*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
	print "cutm4l_gen is....", cutm4l_gen
	print "cutobs_gen is....", cutobs_gen
	print "cutchan_gen is....", cutchan_gen
        Tree[Sample].Draw("GENmass4l >> "+processBin+"fs","("+genweight+")*("+cutchan_gen_out+")","goff")
        # RECO level 
        Tree[Sample].Draw("mass4l >> "+processBin+"reco","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1)","goff") 
        Tree[Sample].Draw("mass4l >> "+processBin+"reco_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1)","goff")
        Tree[Sample].Draw("mass4l >> "+processBin+"recoh4l","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+")","goff") 
#        if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME)):
	if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME) or ("j1" in opt.OBSNAME) or ("j2" in opt.OBSNAME) or ("4lj" in opt.OBSNAME)):
            Tree[Sample].Draw("mass4l >> "+processBin+"recoh4l_jesup","("+recoweight+"*passedFullSelection)*(passedFullSelection==1 && "+cutm4l_reco+" && "+cutobs_reco_jesup+" && "+cuth4l_reco+")","goff")
            Tree[Sample].Draw("mass4l >> "+processBin+"recoh4l_jesdn","("+recoweight+"*passedFullSelection)*( passedFullSelection==1 && "+cutm4l_reco+" && "+cutobs_reco_jesdn+" && "+cuth4l_reco+")","goff")
        Tree[Sample].Draw("mass4l >> "+processBin+"reconoth4l_inc","("+recoweight+")*(passedFullSelection==1 && "+cutm4l_reco+" &&  "+cutnoth4l_reco+")","goff") 
        Tree[Sample].Draw("mass4l >> "+processBin+"recoh4l_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cuth4l_reco+")","goff") 
        Tree[Sample].Draw("mass4l >> "+processBin+"reconoth4l","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cutnoth4l_reco+")","goff")  
        Tree[Sample].Draw("mass4l >> "+processBin+"reconoth4l_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cutnoth4l_reco+")","goff") 
        # RECO and GEN level ( i.e. f(in) and f(out) ) 
        Tree[Sample].Draw("mass4l >> "+processBin+"recoh4lnotfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && "+cutchan_gen_out+" && (passedFiducialSelection==0 || !("+cuth4l_gen+") || !("+cutm4l_gen+")) )","goff") 
        Tree[Sample].Draw("mass4l >> "+processBin+"recoh4lnotfid_inc","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && "+cutchan_gen_out+" && (passedFiducialSelection==0 || !("+cuth4l_gen+") || !("+cutm4l_gen+")) )","goff") 
        Tree[Sample].Draw("mass4l >> "+processBin+"recoh4lfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && passedFiducialSelection==1 && "+cuth4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen+")","goff")  
        Tree[Sample].Draw("mass4l >> "+processBin+"recoh4lotherfid","("+recoweight+")*("+cutm4l_reco+" && "+cutobs_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && passedFiducialSelection==1 && "+cuth4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen_otherfid+")","goff") 
        #Tree[Sample].Draw("mass4l >> "+processBin+"anyrecoh4lfid","("+recoweight+")*("+cutm4l_reco+" && passedFullSelection==1 && "+cuth4l_reco+" && passedFiducialSelection==1 && "+cuth4l_gen+" && "+cutm4l_gen+" && "+cutchan_gen+" && "+cutobs_gen+")","goff")

        if (Histos[processBin+"fs"].Integral()>0):
            
            acceptance[processBin] = Histos[processBin+"fid"].Integral()/Histos[processBin+"fs"].Integral()
	    print "acceptance    numerator========", Histos[processBin+"fid"].Integral()
            print "acceptance     denominator========", Histos[processBin+"fs"].Integral()
            dacceptance[processBin] = sqrt(acceptance[processBin]*(1.0-acceptance[processBin])/Histos[processBin+"fs"].Integral())
            acceptance_4l[processBin] = Histos[processBin+"fid"].Integral()/nEvents[Sample]
            dacceptance_4l[processBin] = sqrt(acceptance_4l[processBin]*(1.0-acceptance_4l[processBin])/nEvents[Sample])                        
        else:
            acceptance[processBin] = -1.0
            dacceptance[processBin] = -1.0
            acceptance_4l[processBin] = -1.0
            dacceptance_4l[processBin] = -1.0
            
        if (Histos[processBin+"reco_inc"].Integral()>0):
            wrongfrac[processBin] = Histos[processBin+"reconoth4l_inc"].Integral()/Histos[processBin+"reco_inc"].Integral()
            dwrongfrac[processBin] = sqrt(wrongfrac[processBin]*(1-wrongfrac[processBin])/Histos[processBin+"reco_inc"].Integral())
        else:
            wrongfrac[processBin] = -1.0
            dwrongfrac[processBin] = -1.0
            
        if (Histos[processBin+"reconoth4l_inc"].Integral()>0):
            print "error checking processBin: ", processBin
            print "error checking histos processBin_reconoth4l integral: ", Histos[processBin+"reconoth4l"].Integral()
            binfrac_wrongfrac[processBin] = Histos[processBin+"reconoth4l"].Integral()/Histos[processBin+"reconoth4l_inc"].Integral()
            print "error checking binfrac_wrongfrac: ", binfrac_wrongfrac[processBin]
	   # dbinfrac_wrongfrac[processBin] = sqrt(binfrac_wrongfrac[processBin]*(1-binfrac_wrongfrac[processBin])/Histos[processBin+"reconoth4l_inc"].Integral())
            if (binfrac_wrongfrac[processBin]<0):    
                binfrac_wrongfrac[processBin] = -1
                dbinfrac_wrongfrac[processBin] = -1
            else:
                dbinfrac_wrongfrac[processBin] = sqrt(binfrac_wrongfrac[processBin]*(1-binfrac_wrongfrac[processBin])/Histos[processBin+"reconoth4l_inc"].Integral())
        else:
            binfrac_wrongfrac[processBin] = -1.0
            dbinfrac_wrongfrac[processBin] = -1.0
            
        if (Histos[processBin+"recoh4l_inc"].Integral()>0):
            outfrac[processBin] = Histos[processBin+"recoh4lnotfid_inc"].Integral()/Histos[processBin+"recoh4l_inc"].Integral()
            doutfrac[processBin] = sqrt(outfrac[processBin]*(1-outfrac[processBin])/Histos[processBin+"recoh4l_inc"].Integral())
        else:
            outfrac[processBin] =  -1.0
            doutfrac[processBin] = -1.0

        if (Histos[processBin+"recoh4lnotfid_inc"].Integral()>0):
            binfrac_outfrac[processBin] = Histos[processBin+"recoh4lnotfid"].Integral()/Histos[processBin+"recoh4lnotfid_inc"].Integral()
            dbinfrac_outfrac[processBin] = sqrt(binfrac_outfrac[processBin]*(1-binfrac_outfrac[processBin])/Histos[processBin+"recoh4lnotfid_inc"].Integral())
        else:
            binfrac_outfrac[processBin] =  -1.0
            dbinfrac_outfrac[processBin] = -1.0                                                                       

        if (Histos[processBin+"fid"].Integral()>=10.0):
#	    print "effrecotofid     numerator========", Histos[processBin+"recoh4lfid"].Integral()
#            print "effrecotofid     denominator========", Histos[processBin+"fid"].Integral()
            effrecotofid[processBin] = Histos[processBin+"recoh4lfid"].Integral()/Histos[processBin+"fid"].Integral()
	    print "inside sqrt deff num", effrecotofid[processBin]*(1-effrecotofid[processBin]), "inside sqrt deff den", Histos[processBin+"fid"].Integral() 
	    if (effrecotofid[processBin]*(1-effrecotofid[processBin])/Histos[processBin+"fid"].Integral()>0):
	    #if (effrecotofid[processBin]*(1-effrecotofid[processBin])/Histos[processBin+"fid"].Integral()>=0):
                deffrecotofid[processBin] = sqrt(effrecotofid[processBin]*(1-effrecotofid[processBin])/Histos[processBin+"fid"].Integral())
#	    print "effrecotofid     numerator========", Histos[processBin+"recoh4lfid"].Integral() 
#	    print "effrecotofid     denominator========", Histos[processBin+"fid"].Integral()
            cfactor[processBin] = Histos[processBin+"recoh4l"].Integral()/Histos[processBin+"fid"].Integral()
	
        else:
            print "the fid integral is====", Histos[processBin+"fid"].Integral()
            effrecotofid[processBin] = -1.0
            deffrecotofid[processBin] = -1.0
            cfactor[processBin] = Histos[processBin+"recoh4l"].Integral()/1.0 # if N(fid) for a gen bin is 0.0, change it to 1.0

        if (Histos[processBin+"anyrecoh4lfid"].Integral()>0.0):
            folding[processBin] = Histos[processBin+"recoh4lfid"].Integral()/Histos[processBin+"anyrecoh4lfid"].Integral()
            dfolding[processBin] = sqrt(folding[processBin]*(1-folding[processBin])/Histos[processBin+"anyrecoh4lfid"].Integral())
        else:
            folding[processBin] = -1.0
            dfolding[processBin] = -1.0

        if ((Histos[processBin+"recoh4lfid"].Integral()+Histos[processBin+"recoh4lotherfid"].Integral())>0.0):
            outinratio[processBin] = Histos[processBin+"recoh4lnotfid"].Integral()/(Histos[processBin+"recoh4lfid"].Integral()+Histos[processBin+"recoh4lotherfid"].Integral())
            if (Histos[processBin+"recoh4lnotfid"].Integral()>0):
                doutinratio[processBin] = outinratio[processBin]*sqrt(1.0/(Histos[processBin+"recoh4lnotfid"].Integral())+1.0/(Histos[processBin+"recoh4lfid"].Integral()+Histos[processBin+"recoh4lotherfid"].Integral()))
            else: doutinratio[processBin] = 0.0
        else:
            outinratio[processBin] = -1.0
            doutinratio[processBin] = -1.0
            
#        if (opt.OBSNAME == "nJets" or opt.OBSNAME.startswith("njets") or ("jet" in opt.OBSNAME)):
	if (("jet" in opt.OBSNAME) or ("Jet" in opt.OBSNAME) or ("j1" in opt.OBSNAME) or ("j2" in opt.OBSNAME) or ("4lj" in opt.OBSNAME)):
            if (Histos[processBin+"recoh4l"].Integral()>0):                
                lambdajesup[processBin] = (Histos[processBin+"recoh4l_jesup"].Integral()-Histos[processBin+"recoh4l"].Integral())/Histos[processBin+"recoh4l"].Integral()
                lambdajesdn[processBin] = (Histos[processBin+"recoh4l_jesdn"].Integral()-Histos[processBin+"recoh4l"].Integral())/Histos[processBin+"recoh4l"].Integral()
            else:
                lambdajesup[processBin] = 0.0
                lambdajesdn[processBin] = 0.0
        else:
            lambdajesup[processBin] = 0.0
            lambdajesdn[processBin] = 0.0

        if (doPlots or doFit):
            n_wrongsig = Histos[processBin+"reconoth4l"].Integral()
            n_outsig = Histos[processBin+"recoh4lnotfid"].Integral()
            n_truesig = Histos[processBin+"recoh4lfid"].Integral()                
            n_otherfid = Histos[processBin+"recoh4lotherfid"].Integral()


        #print Sample,'nEvents total:',nEvents[Sample],channel,'pass Gen:',Histos[processBin+"fid"].Integral(),'pass Reco:',Histos[processBin+'recoh4lfid'].Integral()
        print processBin,"acc",round(acceptance[processBin],3),"eff",round(effrecotofid[processBin],3),"fout",round(outinratio[processBin],3),"wrongfrac",round(wrongfrac[processBin],3)
        
        if (doFit): 
        
            mass4l              = RooRealVar("mass4l", "mass4l", m4l_low, m4l_high)
            mass4e              = RooRealVar("mass4e", "mass4e", m4l_low, m4l_high)
            mass4mu             = RooRealVar("mass4mu", "mass4mu", m4l_low, m4l_high)
            mass2e2mu           = RooRealVar("mass2e2mu", "mass2e2mu", m4l_low, m4l_high)

            passedFullSelection = RooRealVar("passedFullSelection", "passedFullSelection", 0, 2)
            eventMCWeight       = RooRealVar("eventMCWeight", "eventMCWeight", 0.0, 10.0)
            totalWeight         = RooRealVar("totalWeight", "totalWeight", 0.0, 10.0)

            if (obs_reco.startswith('abs(')):
                obs_reco_noabs = obs_reco.replace('abs(','')
                obs_reco_noabs = obs_reco_noabs.replace(')','')
                observable = RooRealVar(obs_reco_noabs, obs_reco_noabs, -1.0*max(float(obs_reco_high), float(obs_gen_high)), max(float(obs_reco_high), float(obs_gen_high)))
            else:
                observable = RooRealVar(obs_reco, obs_reco, max(float(obs_reco_low), float(obs_gen_low)), max(float(obs_reco_high), float(obs_gen_high)))
                
            a1 = RooRealVar("a1","a1",165.0, 135.0, 215.0) # Landau
            a2 = RooRealVar("a2","a2",30.0, 2.0, 500.0) # Landau
            #a3 = RooRealVar("a3","a3",89.0,84.0,94.0)
            #a2 = RooFormulaVar("a2","a2","0.72*@0-@1",RooArgList(a1,a3))
            
            if (channel == "4l"): poly = RooLandau("poly", "PDF", mass4l, a1, a2)
            if (channel == "4e"): poly = RooLandau("poly", "PDF", mass4e, a1, a2)
            if (channel == "4mu"): poly = RooLandau("poly", "PDF", mass4mu, a1, a2)
            if (channel == "2e2mu"): poly = RooLandau("poly", "PDF", mass2e2mu, a1, a2)
            
            nbkg = RooRealVar("N_{wrong}^{fit}","N_{wrong}^{fit}", n_wrongsig, 0.5*n_wrongsig, 1.5*n_wrongsig)
            epoly = RooExtendPdf("epoly","extended bg",poly,nbkg);
            
            mh = shortname.split("_")
            mass = ""
            for i in range(len(mh)):
                if mh[i].startswith("1"): mass = mh[i]
            if (mass=="125p6"): mass="125.6"            

            massHiggs = ast.literal_eval(mass)
            
            MH = RooRealVar("MH", "MH", massHiggs)
            CMS_zz4l_sigma_sig = RooRealVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig",0.0,-0.2,0.2);
            CMS_zz4l_mean_sig  = RooRealVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig",0.0,-0.02,0.02);

            #if (channel=='2e2mu'):
            if (channel=='2e2mu' or channel=='4l'):   # FIXME, temporary fix for 4l  (for mass4l obs. only)
                if (year=='2018'): 
                    #CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.771931539+(0.998407660986)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.260469656+(0.995095874123)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.42180192725+(0.0100469936221)*(@0-125))",RooArgList(MH))                                                          
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.55330758963+(0.00797274642218)*(@0-125))",RooArgList(MH))                                                          
                    #CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.927601791812)+(0*@0)",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.947414158515+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(3.18098806656+(-0.0188855891779)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(3.33147279858+(-0.0438375854704)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.56743054428)+(0*@0)",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.52497361611+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(3.98349053402+(0.0517139624607)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(5.20522265056+(0)*(@0-125))",RooArgList(MH))
                elif(year=='2017'):
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.524+(0.00248708+1)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.77228+(0.00526163)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.967963+(-0.0047248)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(3.69774+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.51606+(-0.000272186)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(6.01048+(0)*(@0-125))",RooArgList(MH))                
                else:  # 2016
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.539+(-0.00679774+1)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.64632+(0.016435)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.905389+(0.0029819)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(3.90164+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.5737+(0.00776476)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(4.33416+(0)*(@0-125))",RooArgList(MH))


            if (channel=='4e'):
                if (year=='2018'):
                    #CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.711610542+(0.994980862782)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(123.5844824+(0.985478630993)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.69738413126+(0.0100692479936)*(@0-125))",RooArgList(MH))                                                          
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(2.06515102908+(0.0170917403402)*(@0-125))",RooArgList(MH))                                                          
                    #CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.744232722334)+(0*@0)",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.948100247167+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(5.54037295934+(-0.0686672890921)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(4.50639853892+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.39075508491)+(0*@0)",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.50095152675+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(5.52294539756+(0.194030101663)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(8.41693578742+(0.219719825966)*(@0-125))",RooArgList(MH))
                elif (year=='2017'):
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.1+(-0.00262293+1)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(2.38283+(0.0155)*(@0-125))",RooArgList(MH))    
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.972669+(-0.00597402)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(5.05142+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.62625+(0.0121146)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(6.30057+(0)*(@0-125))",RooArgList(MH))
                else:   # 2016
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.194+(-0.0123934+1)",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(2.09076+(0.0153247)*(@0-125))",RooArgList(MH))    
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(0.778691+(-0.00177387)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(6.85936+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.47389+(0.00503384)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(7.24158+(0)*(@0-125))",RooArgList(MH))


            if (channel=='4mu'):
                if (year=='2018'):
                    #CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.79931766+(0.997772599479)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.820536957+(0.999619883119)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.12879491843+(0.00905588096292)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.09001384743+(0.00899911411679)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(1.25651736389)+(0*@0)",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(1.23329827124+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(2.03705433186+(-0.00786186895228)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(2.04575884495+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.94273283715)+(0*@0)",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.84386824883+(0)*(@0-125))",RooArgList(MH))
                    #CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(2.57493609201+(0.00406135415709)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(2.98483993137+(0)*(@0-125))",RooArgList(MH))
                elif (year=='2017'):
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.82+(-0.000560694+1)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.16647+(0.0124833)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(1.23329827124+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(2.07185+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.92338+(0.0109082)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(2.90336+(0)*(@0-125))",RooArgList(MH))        
                else:  # 2016
                    CMS_zz4l_mean = RooFormulaVar("CMS_zz4l_mean_sig","CMS_zz4l_mean_sig","(124.801+(-0.00230642+1)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_sigma = RooFormulaVar("CMS_zz4l_sigma_sig","CMS_zz4l_sigma_sig","(1.20385+(0.00862539)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha = RooFormulaVar("CMS_zz4l_alpha","CMS_zz4l_alpha","(1.29006+(-0.0040219)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n = RooFormulaVar("CMS_zz4l_n","CMS_zz4l_n","(2.1216+(0)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_alpha2 = RooFormulaVar("CMS_zz4l_alpha2","CMS_zz4l_alpha2","(1.90093+(-0.0017352)*(@0-125))",RooArgList(MH))
                    CMS_zz4l_n2 = RooFormulaVar("CMS_zz4l_n2","CMS_zz4l_n2","(2.7194+(0)*(@0-125))",RooArgList(MH))



            if (channel == "4l"): signal  = RooDoubleCB("signal","signal", mass4l, CMS_zz4l_mean, CMS_zz4l_sigma, CMS_zz4l_alpha, CMS_zz4l_n, CMS_zz4l_alpha2, CMS_zz4l_n2)  # FIXME, parameter assignment issue, 
            if (channel == "4e"): signal  = RooDoubleCB("signal","signal", mass4e, CMS_zz4l_mean, CMS_zz4l_sigma, CMS_zz4l_alpha, CMS_zz4l_n, CMS_zz4l_alpha2, CMS_zz4l_n2)
            if (channel == "4mu"): signal  = RooDoubleCB("signal","signal", mass4mu, CMS_zz4l_mean, CMS_zz4l_sigma, CMS_zz4l_alpha, CMS_zz4l_n, CMS_zz4l_alpha2, CMS_zz4l_n2)
            if (channel == "2e2mu"): signal  = RooDoubleCB("signal","signal", mass2e2mu, CMS_zz4l_mean, CMS_zz4l_sigma, CMS_zz4l_alpha, CMS_zz4l_n, CMS_zz4l_alpha2, CMS_zz4l_n2)
            
            nsig    = RooRealVar("N_{right}^{fit}","N_{right}^{fit}", 1.0*n_truesig, 1.0*n_truesig)
            esignal = RooExtendPdf("esignal","esig", signal, nsig)

            #if (channel == "4l"): outsignal  = RooDoubleCB("outsignal","outsignal", mass4l, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            #if (channel == "4e"): outsignal  = RooDoubleCB("outsignal","outsignal", mass4e, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            #if (channel == "4mu"): outsignal  = RooDoubleCB("outsignal","outsignal", mass4mu, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
            #if (channel == "2e2mu"): outsignal  = RooDoubleCB("outsignal","outsignal", mass2e2mu, rfv_mean_CB, rfv_sigma_CB, rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)

            outsignal  = signal.Clone("outsignal")
            noutsig    = RooRealVar("N_{out}^{fit}","N_{out}^{fit}", 1.0*n_outsig, 1.0*n_outsig) 
            eoutsignal = RooExtendPdf("eoutsignal","eoutsig", outsignal, noutsig)            
 

            otherfid   = signal.Clone("otherfid")
            notherfid  = RooRealVar("N_{other fid}^{fit}","N_{other fid}^{fit}", 1.0*n_otherfid, 1.0*n_otherfid)
            eotherfid  = RooExtendPdf("eotherfid","eotherfid", otherfid, notherfid)
                                    
            ## sum sig and bkg pdf weighted by corresponding yield
            sum = RooAddPdf("sum","sig+otherfid+outsig+poly",RooArgList(esignal,eotherfid,eoutsignal,epoly))
            
            ## fitting
            r = RooFitResult()

            #print 'Defining RooDataSet:',Sample
            #print "TreesPassed Events slim Entries: ",Tree[Sample].GetEntriesFast()
            

            #print "TreesPassed Events slim Entries: ",Tree[Sample].GetEntriesFast()                                                                                                                                                                                                                                                               

            if (channel == "4l"):
                dataset_sig  = RooDataSet("dataset_sig","dataset_sig", Tree[Sample], RooArgSet(mass4l,observable,passedFullSelection), cutobs_reco.replace("abs(","fabs(")+" && passedFullSelection>0.5")
            elif (channel == "4e"):
                dataset_sig  = RooDataSet("dataset_sig","dataset_sig", Tree[Sample], RooArgSet(mass4e,observable,passedFullSelection), cutobs_reco.replace("abs(","fabs(")+" && passedFullSelection>0.5")
            elif (channel == "4mu"):
                dataset_sig  = RooDataSet("dataset_sig","dataset_sig", Tree[Sample], RooArgSet(mass4mu,observable,passedFullSelection), cutobs_reco.replace("abs(","fabs(")+" && passedFullSelection>0.5")
            elif (channel == "2e2mu"):
                dataset_sig  = RooDataSet("dataset_sig","dataset_sig", Tree[Sample], RooArgSet(mass2e2mu,observable,passedFullSelection), cutobs_reco.replace("abs(","fabs(")+" && passedFullSelection>0.5")


            #print "RooDataSet sumEntries = ",dataset_sig.sumEntries()
            #print ' '
            #print 'Fitting....'
            
            r = sum.fitTo(dataset_sig, RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.Verbose(kFALSE),RooFit.PrintLevel(-1),RooFit.Warnings(kFALSE))
            #r.Print()            
            #sum.Print()

            #print Sample,channel,"post fit CB mean:",rfv_mean_CB.getVal()," sigma: ",rfv_sigma_CB.getVal()
            CB_mean_post[processBin] = CMS_zz4l_mean.getVal()
            #CB_dmean_post[processBin] = rfv_mean_CB.getError()
            CB_sigma_post[processBin] = CMS_zz4l_sigma.getVal()
            #CB_dsigma_post[processBin] = rfv_sigma_CB.getVal()

            print Sample,channel,"post fit Landau mean:",a1.getVal()," sigma: ",a2.getVal()
            Landau_mean_post[processBin] = a1.getVal()
            Landau_sigma_post[processBin] = a2.getVal()
        
        if (doPlots):
            ################################
            ######### Plotting #############
            ################################
        
            hs = THStack("hs","mass spectrum");
            Histos[processBin+"reconoth4l"].SetFillColor(0)
            Histos[processBin+"reconoth4l"].SetLineColor(kOrange)
            hs.Add(Histos[processBin+"reconoth4l"])
            Histos[processBin+"recoh4lotherfid"].SetFillColor(0)
            Histos[processBin+"recoh4lotherfid"].SetLineColor(kBlue)
            hs.Add(Histos[processBin+"recoh4lotherfid"])
            Histos[processBin+"recoh4lnotfid"].SetFillColor(0)
            Histos[processBin+"recoh4lnotfid"].SetLineColor(kBlack)
            hs.Add(Histos[processBin+"recoh4lnotfid"])                                    
            Histos[processBin+"recoh4lfid"].SetFillColor(0)
            Histos[processBin+"recoh4lfid"].SetLineColor(kRed)
            hs.Add(Histos[processBin+"recoh4lfid"])

            leg = TLegend(0.54,0.57,0.91,0.72);
            leg.SetShadowColor(0)
            leg.SetFillColor(0)
            leg.SetLineColor(0)
            leg.AddEntry(Histos[processBin+"recoh4lfid"],"N_{sig}^{MC} = "+str(int(n_truesig)), "F")
            leg.AddEntry(Histos[processBin+"reconoth4l"],"N_{wrong}^{MC} = "+str(int(n_wrongsig)), "F")
            leg.AddEntry(Histos[processBin+"recoh4lnotfid"],"N_{out}^{MC} = "+str(int(n_outsig)), "F")
            if (doFit):
                # Plot updated with fitting
                frame = RooPlot()
                if (channel == "4l"): frame = mass4l.frame(RooFit.Title("m4l"),RooFit.Bins(m4l_bins))
                if (channel == "4e"): frame = mass4e.frame(RooFit.Title("m4e"),RooFit.Bins(m4l_bins))
                if (channel == "4mu"): frame = mass4mu.frame(RooFit.Title("m4mu"),RooFit.Bins(m4l_bins))
                if (channel == "2e2mu"): frame = mass2e2mu.frame(RooFit.Title("m2e2mu"),RooFit.Bins(m4l_bins))
                
                dataset_sig.plotOn(frame, RooFit.LineColor(kRed), RooFit.MarkerSize(0))
                sum.plotOn(frame, RooFit.Components('poly,otherfid,outsignal'), RooFit.LineColor(kBlack))                
                sum.plotOn(frame, RooFit.Components('poly,otherfid'),RooFit.LineColor(kBlue))
                sum.plotOn(frame, RooFit.Components('poly'), RooFit.LineColor(kOrange))
                sum.plotOn(frame, RooFit.LineColor(kRed) )
                
                # Uncorrelated
                if (Histos[processBin+"fid"].Integral()>0):
                    eff_fit[processBin]  = nsig.getVal()/Histos[processBin+"fid"].Integral()
                else:
                    eff_fit[processBin] = -1.0
                    
                if (eff_fit[processBin]<1.0 and eff_fit[processBin]>-0.1):
                    deff_fit[processBin] = sqrt(eff_fit[processBin]*(1-eff_fit[processBin])/Histos[processBin+"fid"].Integral()) 
                else:
                    deff_fit[processBin] = eff_fit[processBin]
                
                #print " "
                #print " "            
                #print "Passed Reco. Selection and true H->ZZ->4l (from fit) : ",nsig.getVal()
                #print "Passed Gen.  Selection and true H->ZZ->4l (from gen.): ",Histos[processBin+"fid"].Integral()
                #print "correction factor from fit: %.3f +/- %.3f "  % (cfactor[processBin], dcfactor[processBin])                
                #print " "
                #print " "   
                
            #c = TCanvas("c","c",750,750)
            c = TCanvas("c","c",750,800)
            SetOwnership(c,False)
            c.cd()
            #c.SetLogy()
 
            #hs.SetMaximum(1.15*hs.GetMaximum())
            hs.SetMaximum(2.2*hs.GetMaximum())
            hs.SetMinimum(0.1)
            hs.Draw("ehist")
            if (channel == "4l"): hs.GetXaxis().SetTitle("m_{4l} (GeV)")
            if (channel == "4e"): hs.GetXaxis().SetTitle("m_{4e} (GeV)")
            if (channel == "4mu"): hs.GetXaxis().SetTitle("m_{4#mu} (GeV)")
            if (channel == "2e2mu"): hs.GetXaxis().SetTitle("m_{2e2#mu} (GeV)")
            if (doFit): frame.Draw("same")
       
            xval = 0.20
            #xval = 0.50

            latex2 = TLatex()
            latex2.SetNDC()
            latex2.SetTextSize(0.75*c.GetTopMargin())
            latex2.SetTextFont(62)
            latex2.SetTextAlign(11) # align right
            latex2.DrawLatex(xval+0.02, 0.85, "CMS")
            latex2.SetTextSize(0.6*c.GetTopMargin())
            latex2.SetTextFont(52)
            latex2.SetTextAlign(11)
            latex2.DrawLatex(xval, 0.8, "Simulation")
            latex2.SetTextSize(0.4*c.GetTopMargin())
            latex2.SetTextFont(42)
            latex2.SetTextAlign(11)
            latex2.DrawLatex(xval, 0.73, shortname.replace('_',' ')+' GeV');
            latex2.SetTextSize(0.35*c.GetTopMargin())
            latex2.SetTextFont(42)
            latex2.DrawLatex(xval, 0.68, str(obs_reco_low)+" < "+obs_reco+" < "+str(obs_reco_high) )
            
            print opt.LUMISCALE
            if (not opt.LUMISCALE=="1.0"):
                if (year=='2016') : lumi = round(35.9*float(opt.LUMISCALE),1)
                elif (year=='2017') : lumi = round(41.7*float(opt.LUMISCALE),1)
                else  : lumi = round(58.5*float(opt.LUMISCALE),1)
                latex2.DrawLatex(0.80, 0.94,str(lumi)+" fb^{-1} (13 TeV)")
            else:
                if (year=='2016') : latex2.DrawLatex(0.80, 0.94,"35.9 fb^{-1} (13 TeV)")
                elif (year=='2017') : latex2.DrawLatex(0.80, 0.94,"41.7 fb^{-1} (13 TeV)")
                elif (year=='2018') : latex2.DrawLatex(0.80, 0.94,"58.8 fb^{-1} (13 TeV)")
                else : latex2.DrawLatex(0.80, 0.94,"137 fb^{-1} (13 TeV)")


            if (doFit):
                latex2.DrawLatex(xval, 0.64, "eff. = %.3f #pm %.3f" % (effrecotofid[processBin],deffrecotofid[processBin]))
                latex2.DrawLatex(xval, 0.60, "acc. = %.3f #pm %.3f" % (acceptance[processBin],dacceptance[processBin]))
                latex2.DrawLatex(xval, 0.56, "mean = %.3f " % (CMS_zz4l_mean.getVal())+" GeV")
                latex2.DrawLatex(xval, 0.52, "#sigma = %.3f " % (CMS_zz4l_sigma.getVal())+" GeV")
                latex2.DrawLatex(xval, 0.48, "#alpha = %.3f " % (CMS_zz4l_alpha.getVal()))
                latex2.DrawLatex(xval, 0.44, "n = %.3f " % (CMS_zz4l_n.getVal()))
                latex2.DrawLatex(xval, 0.40, "#alpha2 = %.3f " % (CMS_zz4l_alpha2.getVal()))
                latex2.DrawLatex(xval, 0.36, "n2 = %.3f " % (CMS_zz4l_n2.getVal()))
                latex2.DrawLatex(xval, 0.32, "#mu_{land.} = %.3f " % (a1.getVal()))
                latex2.DrawLatex(xval, 0.28, "#sigma_{land.} = %.3f " % (a2.getVal()))
                latex2.DrawLatex(xval, 0.24, "#chi^{2}/dof = %.3f" % frame.chiSquare(r.floatParsFinal().getSize()))
            else:
                latex2.DrawLatex(xval, 0.64, "N_{fid.}^{MC} = "+str(int(n_truesig)) )
                latex2.DrawLatex(xval, 0.60, "N_{other fid.}^{MC} = "+str(int(n_otherfid)) )
                latex2.DrawLatex(xval, 0.56, "N_{not fid.}^{MC} = "+str(int(n_outsig)) )
                latex2.DrawLatex(xval, 0.52, "N_{wrong comb.}^{MC} = "+str(int(n_wrongsig)) )
                latex2.DrawLatex(xval, 0.44, "eff^{MC} = %.3f #pm %.3f" % (effrecotofid[processBin],deffrecotofid[processBin]))
            
#            c.SaveAs("plots/"+processBin+"_effs_"+recoweight+".png")
            #c.SaveAs("plots_"+date+"/"+processBin+"_effs_"+recoweight+".png")
            c.SaveAs("Eff_plots_"+year+"/"+opt.OBSNAME+"/"+processBin+"_effs_"+recoweight+".png")
            c.SaveAs("Eff_plots_"+year+"/"+opt.OBSNAME+"/"+processBin+"_effs_"+recoweight+".pdf")


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

#test 
obs_reco = opt.OBSNAME 
obs_gen = "GEN"+opt.OBSNAME 

if (obs_reco.startswith("Tau")):
    obs_gen = "GEN_"+opt.OBSNAME
# variables measured in absolute values

if (opt.OBSNAME == "rapidity4l"):
    obs_reco = "abs(rapidity4l)"
    obs_gen = "abs(GENrapidity4l)"


if (opt.OBSNAME == "dEtaj1j2"):
    obs_reco = "abs(dEtaj1j2)"
    obs_gen = "abs(GENdEtaj1j2)"

print "obs_reco is :  ", obs_reco
print "obs_gen is :  ", obs_gen

'''
if (opt.OBSNAME == "massZ1"):
    obs_reco = "massZ1"
#    obs_gen = "GENmZ1"
    obs_gen = "GENmassZ1"
if (opt.OBSNAME == "massZ2"):
    obs_reco = "massZ2"
#    obs_gen = "GENmZ2"
    obs_gen = "GENmassZ2"
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
# new obs.
if (opt.OBSNAME == "pT4lj"):
    obs_reco = "pT4lj"
    obs_gen = "GENpT4lj"
if (opt.OBSNAME == "pTj2"):
    obs_reco = "pTj2"
    obs_gen = "GENpTj2"
if (opt.OBSNAME == "mass4lj"):
    obs_reco = "mass4lj"
    obs_gen = "GENmass4lj"
if (opt.OBSNAME == "mj1j2"):
    obs_reco = "mj1j2"
    obs_gen = "GENmj1j2"
'''
    
#obs_bins = {0:(opt.OBSBINS.split("|")[1:((len(opt.OBSBINS)-1)/2)]),1:['0','inf']}[opt.OBSNAME=='inclusive'] 
obs_bins = opt.OBSBINS.split("|") 
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins.pop()
obs_bins.pop(0) 

List = []
if year=="2018": from LoadData_2018 import *;
elif year=="2017": from LoadData_2017 import *;
else : from LoadData_2016 import *;

if year=="2018": temp_list = sample_shortnames_2018.iteritems()
elif year=="2017": temp_list = sample_shortnames_2017.iteritems()
else : temp_list = sample_shortnames_2016.iteritems()
print "temp_list is  ", temp_list

#for long, short in sample_shortnames.iteritems():
for long, short in temp_list:
    #if (not ("WH" in short) or ("ttH" in short) or ("ZH" in short)): continue
    #if (not ("ggH" in short)): continue
    #if (not "VBF" in short): continue
    List.append(long)

if (obs_reco=="mass4l"):
    chans = ['4e','4mu','2e2mu','4l']
else:
    chans = ['4e','4mu','2e2mu']

if (not opt.CHAN==''):
    chans = [opt.CHAN]

for chan in chans:
    for recobin in range(len(obs_bins)-1):
        for genbin in range(len(obs_bins)-1):
            geteffs(chan,List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, recobin, genbin)  

ext=''
if (not opt.CHAN==''):
    ext='_'+opt.CHAN

#with open('datacardInputs/inputs_sig_'+opt.OBSNAME+ext+'.py', 'w') as f:
#with open('datacardInputs_'+year+'/inputs_sig_'+opt.OBSNAME+ext+'.py', 'w') as f:
with open('datacardInputs_'+year+'/inputs_sig_'+opt.OBSNAME+ext+'.py', 'w') as f:
    f.write('acc = '+str(acceptance)+' \n')
    f.write('dacc = '+str(dacceptance)+' \n')
    f.write('acc_4l = '+str(acceptance_4l)+' \n')
    f.write('dacc_4l = '+str(dacceptance_4l)+' \n')
    f.write('eff = '+str(effrecotofid)+' \n')
    f.write('deff = '+str(deffrecotofid)+' \n')
    f.write('inc_outfrac = '+str(outfrac)+' \n') 
    f.write('binfrac_outfrac = '+str(binfrac_outfrac)+' \n') 
    f.write('outinratio = '+str(outinratio)+' \n')
    f.write('doutinratio = '+str(doutinratio)+' \n')
    f.write('inc_wrongfrac = '+str(wrongfrac)+' \n') 
    f.write('binfrac_wrongfrac = '+str(binfrac_wrongfrac)+' \n') 
    f.write('cfactor = '+str(cfactor)+' \n')
    f.write('lambdajesup = '+str(lambdajesup)+' \n')
    f.write('lambdajesdn = '+str(lambdajesdn)+' \n')

#with open('datacardInputs/moreinputs_sig_'+opt.OBSNAME+ext+'.py', 'w') as f:
#with open('datacardInputs_'+year+'/moreinputs_sig_'+opt.OBSNAME+ext+'.py', 'w') as f:
with open('datacardInputs_'+year+'/moreinputs_sig_'+opt.OBSNAME+ext+'.py', 'w') as f:
    f.write('CB_mean = '+str(CB_mean_post)+' \n')
    #f.write('CB_dmean = '+str(CB_dmean_post)+' \n')
    f.write('CB_sigma = '+str(CB_sigma_post)+' \n')
    #f.write('CB_dsigma = '+str(CB_dsigma_post)+' \n')
    f.write('folding = '+str(folding)+' \n')
    f.write('dfolding = '+str(dfolding)+' \n')
    #f.write('effanyreco = '+str(effanyreco)+' \n')
    #f.write('deffanyreco = '+str(deffanyreco)+' \n')
print "All samples in all process bins compiled!"
    

