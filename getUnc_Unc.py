import optparse
import os
import sys
from decimal import *
from math import *

# INFO: Following items are imported from either python directory or Inputs
from LoadData import *
from sample_shortnames import *
from Utils import *
from read_bins import *

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

# Don't move the root import before `sys.argv = grootargs`. Reference: https://root-forum.cern.ch/t/python-options-and-root-options/4641/3
from ROOT import *

doFit = opt.DOFIT
doPlots = opt.DOPLOTS

if (not os.path.exists("plots") and doPlots):
    os.system("mkdir plots")

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

if (opt.DOPLOTS and os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()

Histos = {}
acceptance = {}
qcdUncert = {}
pdfUncert = {}

def getunc(channel, List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, genbin, obs_reco_2 = '', obse_gen2 = ''):


    if (obs_reco2 == ''):
        border_msg("The option of performing a 1D differential measurement has been selected.")

        obs_gen_low = obs_bins[genbin]
        obs_gen_high = obs_bins[genbin+1]

        obs_gen_lowest = obs_bins[0]
        obs_gen_highest = obs_bins[len(obs_bins)-1]

        print("General information about the variable:")
        print ("Chosen Gen Bin is: {}, Low geb bin value is: {}, High gen bin value is: {}, Lowest value is: {}, Highest value is: {}".format(genbin, obs_gen_low, obs_gen_high, obs_gen_lowest, obs_gen_highest))
        
    else:
        border_msg("The option of performing a double differential measurement has been selected.")


        obs_gen_low = obs_bins[genbin][0][0]
        obs_gen_high = obs_bins[genbin][0][1]

        obs1_boundaries = [boundary for bin in obs_bins for boundary in bin[0]]
        obs1_boundaries_float = [float(i) for i in obs1_boundaries]

        obs_gen_lowest = str(min(obs1_boundaries_float))
        obs_gen_highest = str(max(obs1_boundaries_float))

        obs_gen2_low = obs_bins[genbin][1][0]
        obs_gen2_high = obs_bins[genbin][1][1]

        obs2_boundaries = [boundary for bin in obs_bins for boundary in bin[1]]
        obs2_boundaries_float = [float(i) for i in obs2_boundaries]

        obs_gen2_lowest = str(min(obs2_boundaries_float))
        obs_gen2_highest = str(max(obs2_boundaries_float))
        
        print("General information about the variable 1:")
        print ("Chosen Gen Bin is: {}, Low geb bin value is: {}, High gen bin value is: {}, Lowest value is: {}, Highest value is: {}".format(genbin, obs_gen_low, obs_gen_high, obs_gen_lowest, obs_gen_highest))

        print("General information about the variable 2:")
        print ("Chosen Gen Bin is: {}, Low geb bin value is: {}, High gen bin value is: {}, Lowest value is: {}, Highest value is: {}".format(genbin, obs_gen2_low, obs_gen2_high, obs_gen2_lowest, obs_gen2_highest))


    if (obs_reco.startswith("mass4l")):
        m4l_low = float(obs_gen_low)
        m4l_high = float(obs_gen_high)
        m4l_bins = int((m4l_high-m4l_low)/2)

    i_sample = -1

    print(List)

    for Sample in List:
        if (not Sample in Tree): continue
        if (not Tree[Sample]): continue

        if (obs_reco.startswith("njets")) or (obs_gen_high == "inf"):
            cutobs_gen = "("+obs_gen+">="+str(obs_gen_low)+")"

            if (obs_reco2.startswith("njets")) or (obs_gen2_high == "inf"):
                cutobs_gen  += "&& ("+obs_gen2+">="+str(obs_gen2_low)+")"
            else:
                cutobs_gen += "&& ("+obs_gen2+">="+str(obs_gen2_low)+" && "+obs_gen2+"<"+str(obs_gen2_high)+")"
        else:
            cutobs_gen = "("+obs_gen+">="+str(obs_gen_low)+" && "+obs_gen+"<"+str(obs_gen_high)+")"

            if not (obs_reco2 == ''):
                if obs_gen2_high == "inf":
                    cutobs_gen += "&& ("+obs_gen2+">="+str(obs_gen2_low)+")"
                else:
                    cutobs_gen += "&& ("+obs_gen2+">="+str(obs_gen2_low)+" && "+obs_gen2+"<"+str(obs_gen2_high)+")"

        cutm4l_gen     = "(GENmass4l>"+str(m4l_low)+" && GENmass4l<"+str(m4l_high)+")"

        print(bcolors.HEADER+"cutobs_gen :"+bcolors.ENDC)
        print(cutobs_gen)
        print(bcolors.HEADER+"cutm4l_gen :"+bcolors.ENDC)
        print(cutm4l_gen)

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

        if not (obs_reco2 == ''):
            processBin = shortname+'_'+channel+'_'+opt.OBSNAME.replace(" ","_")+'_genbin'+str(genbin)

        #if ("NNNLOPS" in processBin):
        #    cutchan_gen = "("+cutchan_gen+" && Sum$(abs(nnloWeights[]/qcdWeights[0])>100.0)==0 )"
        #    cutchan_gen_out = "("+cutchan_gen_out+" && Sum$(abs(nnloWeights[]/qcdWeights[0])>100.0)==0 )"

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
                Histos[processBin+"fs"+str(i)] = TH1D(processBin+"fs"+str(i), processBin+"fs"+str(i), 100, -1, 10000)
                Histos[processBin+"fs"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fs"+str(i),"(nnloWeights["+str(i)+"])*("+cutchan_gen_out+")","goff")

                Histos[processBin+"fid"+str(i)] = TH1D(processBin+"fid"+str(i), processBin+"fid"+str(i), m4l_bins, m4l_low, m4l_high)
                Histos[processBin+"fid"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fid"+str(i),"(nnloWeights["+str(i)+"])*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
                Histos[processBin+"fid"+str(i)].Scale(1.0/Histos[processBin+"fs"].Integral())

                Histos[processBin+"fidraw"+str(i)] = TH1D(processBin+"fidraw"+str(i), processBin+"fidraw"+str(i), m4l_bins, m4l_low, m4l_high)
                Histos[processBin+"fidraw"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fidraw"+str(i),"(nnloWeights["+str(i)+"])*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
                Histos[processBin+"fidraw"+str(i)].Scale(1.0/Histos[processBin+"fs"+str(i)].Integral())
                Histos[processBin+"fs"+str(i)].Scale(1.0/Histos[processBin+"fs"+str(i)].Integral())


        else:
            for i in [0,1,2,3,4,6,8]:
                Histos[processBin+"fs"+str(i)] = TH1D(processBin+"fs"+str(i), processBin+"fs"+str(i), 100, -1, 10000)
                Histos[processBin+"fs"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fs"+str(i),"(qcdWeights["+str(i)+"])*("+cutchan_gen_out+")","goff")

                Histos[processBin+"fid"+str(i)] = TH1D(processBin+"fid"+str(i), processBin+"fid"+str(i), m4l_bins, m4l_low, m4l_high)
                Histos[processBin+"fid"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fid"+str(i),"(qcdWeights["+str(i)+"])*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
                Histos[processBin+"fid"+str(i)].Scale(1.0/Histos[processBin+"fs"].Integral())

                Histos[processBin+"fidraw"+str(i)] = TH1D(processBin+"fidraw"+str(i), processBin+"fidraw"+str(i), m4l_bins, m4l_low, m4l_high)
                Histos[processBin+"fidraw"+str(i)].Sumw2()
                Tree[Sample].Draw("GENmass4l >> "+processBin+"fidraw"+str(i),"(qcdWeights["+str(i)+"])*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
                Histos[processBin+"fidraw"+str(i)].Scale(1.0/Histos[processBin+"fs"+str(i)].Integral())
                Histos[processBin+"fs"+str(i)].Scale(1.0/Histos[processBin+"fs"+str(i)].Integral())

        Histos[processBin+"fidPDF"] = TH1D(processBin+"fidPDF", processBin+"fidPDF", m4l_bins, m4l_low, m4l_high)
        Histos[processBin+"fidPDF"].Sumw2()
        if ("NNLOPS" in processBin):
            Tree[Sample].Draw("GENmass4l >> "+processBin+"fidPDF","(nnloWeights[0]*pdfENVup/abs(qcdWeights[0]))*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
        else:
            Tree[Sample].Draw("GENmass4l >> "+processBin+"fidPDF","(qcdWeights[0]*pdfENVup/abs(qcdWeights[0]))*(passedFiducialSelection==1 && "+cutm4l_gen+" && "+cutobs_gen+" && "+cutchan_gen+"  && "+cuth4l_gen+")","goff")
        Histos[processBin+"fidPDF"].Scale(1.0/Histos[processBin+"fs"].Integral())

        fsintegral = Histos[processBin+"fs"].Integral()
        Histos[processBin+"fs"].Scale(1.0/Histos[processBin+"fs"].Integral())

        # GEN level
        accerrstat=0.0
        if (Histos[processBin+"fs"].Integral()>0):
            if ("NNLOPS" in processBin):
                print("\n{}\t{}".format(Histos[processBin+"fs"].Integral(),Histos[processBin+"fid0"].Integral()))
                acceptance[processBin] = Histos[processBin+"fid0"].Integral()/Histos[processBin+"fs"].Integral()
                accerrstat = sqrt(acceptance[processBin]*(1-acceptance[processBin])/fsintegral)
                qcderrup=1.0; qcderrdn=1.0;
                accerrup=1.0; accerrdn=1.0;
                for i in range(0,27): # FIXME: What is this number 27?
                    if (i==5 or i==7 or i==11 or i==14 or i==15 or i==16 or i==17 or i==19 or i==21 or i==22 or i==23 or i==25): continue
                    ratio = Histos[processBin+"fid"+str(i)].Integral()/Histos[processBin+"fid0"].Integral()
                    print("{:2}\tratio\t{}".format(i,ratio))
                    if (ratio>qcderrup): qcderrup = Histos[processBin+"fid"+str(i)].Integral()/Histos[processBin+"fid0"].Integral()
                    if (ratio<qcderrdn): qcderrdn = Histos[processBin+"fid"+str(i)].Integral()/Histos[processBin+"fid0"].Integral()

                    acci = Histos[processBin+"fidraw"+str(i)].Integral()/Histos[processBin+"fs"+str(i)].Integral()
                    print("{:2}\tacc  \t{}".format(i,acci))
                    print("{}\t{}".format(Histos[processBin+"fidraw"+str(i)].Integral(),Histos[processBin+"fs"+str(i)].Integral()))
                    if (acci/acceptance[processBin]>accerrup): accerrup=acci/acceptance[processBin]
                    if (acci/acceptance[processBin]<accerrdn): accerrdn=acci/acceptance[processBin]
            else:
                print("\n{}\t{}".format(Histos[processBin+"fs"].Integral(),Histos[processBin+"fid0"].Integral()))
                acceptance[processBin] = Histos[processBin+"fid0"].Integral()/Histos[processBin+"fs"].Integral()
                accerrstat = sqrt(acceptance[processBin]*(1-acceptance[processBin])/fsintegral)
                qcderrup=1.0; qcderrdn=1.0;
                accerrup=1.0; accerrdn=1.0;
                for i in [1,2,3,4,6,8]:
                    ratio = Histos[processBin+"fid"+str(i)].Integral()/Histos[processBin+"fid0"].Integral()
                    print("{:2}\tratio\t{}".format(i,ratio))
                    if (ratio>qcderrup): qcderrup = Histos[processBin+"fid"+str(i)].Integral()/Histos[processBin+"fid0"].Integral()
                    if (ratio<qcderrdn): qcderrdn = Histos[processBin+"fid"+str(i)].Integral()/Histos[processBin+"fid0"].Integral()

                    acci = Histos[processBin+"fidraw"+str(i)].Integral()/Histos[processBin+"fs"+str(i)].Integral()
                    print("{:2}\tacc  \t{}".format(i,acci))
                    if (acci/acceptance[processBin]>accerrup): accerrup=acci/acceptance[processBin]
                    if (acci/acceptance[processBin]<accerrdn): accerrdn=acci/acceptance[processBin]

            qcdUncert[processBin] = {"uncerDn":abs(qcderrdn-1.0),"uncerUp":abs(qcderrup-1.0)}
            if ("NNLOPS" in processBin):
                pdferr = Histos[processBin+"fidPDF"].Integral()/Histos[processBin+"fid0"].Integral()
            else:
                pdferr = Histos[processBin+"fidPDF"].Integral()/Histos[processBin+"fid0"].Integral()
            pdfUncert[processBin] = {"uncerDn":abs(pdferr-1.0),"uncerUp":abs(pdferr-1.0)}


            print(processBin,acceptance[processBin],accerrstat,qcderrup,qcderrdn,pdferr)
            print("accerrup",accerrup,"accerrdn",accerrdn)

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

obs_reco2 = ''
obs_gen2 = ''
obs_reco2_low = -1
obs_reco2_high = -1
obs_gen2_low = -1
obs_gen2_high = -1

if 'vs' in opt.OBSNAME:
    obs_reco = opt.OBSNAME.split(" vs ")[0]
    obs_gen = "GEN" + obs_reco

    obs_reco2 = opt.OBSNAME.split(" vs ")[1]
    obs_gen2 = "GEN" + obs_reco2

else:
    obs_reco = opt.OBSNAME
    obs_gen = "GEN"+opt.OBSNAME

    obs_reco2 = ''
    obs_gen2 = ''

# variables measured in absolute values
if (obs_reco == "rapidity4l"):
    obs_reco = "abs(rapidity4l)"
    obs_gen = "abs(GENrapidity4l)"

if (obs_reco2 == "rapidity4l"):
    obs_reco2 = "abs(rapidity4l)"
    obs_gen2 = "abs(GENrapidity4l)"


print("[INFO] obs_reco is : {}".format(obs_reco))
print("[INFO] obs_gen is  : {}".format(obs_gen))

#obs_bins = {0:(opt.OBSBINS.split("|")[1:((len(opt.OBSBINS)-1)/2)]),1:['0','inf']}[opt.OBSNAME=='inclusive']
obs_bins = read_bins(opt.OBSBINS)

List = []
for long, short in sample_shortnames.iteritems():
    if (not "ggH" in short): continue
    List.append(long)

if (obs_reco=="mass4l"):
    chans = ['4e','4mu','2e2mu','4l']
else:
    chans = ['4e','4mu','2e2mu']
    #chans = ['4l','4e','4mu','2e2mu']

Nbins = len(obs_bins)

if obs_reco2 == '':
    Nbins = Nbins - 1 #  For the double diff measurement the len(obs_bins) is the actual number of bins, while for the 1 observable we parse bin edges so it needs to be len -1

for chan in chans:
    for genbin in range(Nbins):
        getunc(chan,List, m4l_bins, m4l_low, m4l_high, obs_reco, obs_gen, obs_bins, genbin, obs_reco2, obs_gen2)

if (obs_reco.startswith("njets")):
    for chan in chans:
        for genbin in range(len(obs_bins)-2): # last bin is >=3
            for Sample in List:
                shortname = sample_shortnames[Sample]
                processBin = shortname+'_'+chan+'_'+obs_reco+'_genbin'+str(genbin)
                processBinPlus1 = shortname+'_'+chan+'_'+obs_reco+'_genbin'+str(genbin+1)
                acceptance[processBin] = acceptance[processBin]-acceptance[processBinPlus1]
                qcdUncert[processBin]['uncerUp'] = sqrt(qcdUncert[processBin]['uncerUp']*qcdUncert[processBin]['uncerUp']+qcdUncert[processBinPlus1]['uncerUp']*qcdUncert[processBinPlus1]['uncerUp'])
                qcdUncert[processBin]['uncerDn'] = sqrt(qcdUncert[processBin]['uncerDn']*qcdUncert[processBin]['uncerDn']+qcdUncert[processBinPlus1]['uncerDn']*qcdUncert[processBinPlus1]['uncerDn'])

DirForUncFiles = "python"
if not os.path.isdir(DirForUncFiles): os.mkdir(DirForUncFiles)
with open(DirForUncFiles+'/accUnc_'+opt.OBSNAME.replace(" ","_")+'.py', 'w') as f:
    f.write('acc = '+str(acceptance)+' \n')
    f.write('qcdUncert = '+str(qcdUncert)+' \n')
    f.write('pdfUncert = '+str(pdfUncert)+' \n')
