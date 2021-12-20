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
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
    
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    
# parse the arguments and options
global opt, args
parseOptions()
sys.argv = grootargs
    
if (not os.path.exists("plots")):
    os.system("mkdir plots")
        
from ROOT import *
from tdrStyle import *
setTDRStyle()

ROOT.gStyle.SetPaintTextFormat("1.2f")
#ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetNumberContours(99)

obsName = opt.OBSNAME
if (obsName=='pT4l'):
    label = 'p_{T}(H)'
if (obsName=='massZ2'):    
    label = 'm(Z_{2})'
if (obsName=='massZ1'):    
    label = 'm(Z_{1})'
if (obsName=='njets_pt30_eta4p7'):
    label = "N(jets)"
if (obsName=='pt_leadingjet_pt30_eta4p7'):
    label = "p_{T}(jet)"
if (obsName=='njets_pt30_eta2p5'):
    label = "N(jets) |#eta|<2.5"
if (obsName=='pt_leadingjet_pt30_eta2p5'):
    label = "p_{T}(jet) |#eta|<2.5"
if (obsName=='absdeltarapidity_hleadingjet_pt30_eta4p7'):
    label = "|y(H)-y(jet)|"
if (obsName=='absrapidity_leadingjet_pt30_eta4p7'):
    label = "|y(jet)|"
if (obsName=='rapidity4l'):
    label = "|y(H)|" 
if (obsName=='cosThetaStar'):
    label = "|cos(#theta*)|"
if (obsName=='cosTheta1'):
    label = "|cos(#theta_{1})|"
if (obsName=='cosTheta2'):
    label = "|cos(#theta_{2})|"
if (obsName=='Phi'):
    label = "|#Phi|"
if (obsName=='Phi1'):
    label = "|#Phi_{1}|"

obs_bins = opt.OBSBINS.split("|")
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')):
    print 'BINS OPTION MUST START AND END WITH A |'
obs_bins.pop()
obs_bins.pop(0)
if float(obs_bins[len(obs_bins)-1])>199:
    obs_bins[len(obs_bins)-1]='250'
if (opt.OBSNAME=="nJets" or opt.OBSNAME.startswith("njets")):
    obs_bins[len(obs_bins)-1]='4'
                        

sys.path.append('./datacardInputs')
_temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['eff','deff'], -1)
eff = _temp.eff
deff = _temp.deff
#_temp = __import__('moreinputs_sig_'+obsName, globals(), locals(), ['folding','dfolding','effanyreco','deffanyreco'], -1)
#_temp = __import__('moreinputs_sig_'+obsName, globals(), locals(), ['folding','dfolding'], -1)
#folding = _temp.folding
#dfolding = _temp.dfolding
#effanyreco = _temp.effanyreco
#deffanyreco = _temp.deffanyreco

#modelNames = ['ggH_powheg_JHUgen_125','ggH_minloHJJ_125','VBF_powheg_125','WH_pythia_125','ZH_pythia_125','ttH_pythia_125']#,'SM_125','SMup_125','SMdn_125']
#modelNames = ['ggH_amcatnloFXFX_125','ggH_NNLOPS_JHUgen_125','ggH_powheg_JHUgen_125','VBF_powheg_JHUgen_125','WH_powheg_JHUgen_125','ZH_powheg_JHUgen_125','ttH_powheg_JHUgen_125']#'SM_125','SMup_125','SMdn_125']
modelNames = ['ggH_amcatnloFXFX_125','ggH_powheg_JHUgen_125','VBF_powheg_JHUgen_125','WH_powheg_JHUgen_125','ZH_powheg_JHUgen_125','ttH_powheg_JHUgen_125']#'SM_125','SMup_125','SMdn_125']

#modelNames = ['VBF_powheg_JHUgen_125']

fStates = ['4e','4mu','2e2mu']

a_bins = array('d',[float(obs_bins[i]) for i in range(len(obs_bins))])
print a_bins        
for model in modelNames:
    for fState in fStates:
        eff2d = TH2D("eff2d", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        folding2d = TH2D("folding2d", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        eff2d4l = TH2D("eff2d4l", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        for x in range(0,len(obs_bins)-1):
            for y in range(0,len(obs_bins)-1):
                #eff2d.GetXaxis().SetBinLabel(x+1,str(x))
                #eff2d.GetYaxis().SetBinLabel(y+1,str(y))                
                bin = eff2d.GetBin(x+1,y+1)
		if eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]>0:
                    eff2d.SetBinContent(bin,eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]), eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
#		elif eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]<=0:
#		    eff2d.SetBinContent(bin,0), eff2d.SetBinError(bin,0)
		else: eff2d.SetBinContent(bin,0), eff2d.SetBinError(bin,0)
#                if (not model.startswith('SM') and eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]!=0):
#		    eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
#		elif (not model.startswith('SM') and eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]==0):
#		    eff2d.SetBinError(bin,0)
#                else: eff2d.SetBinError(bin,deff['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #folding2d.GetXaxis().SetBinLabel(x+1,str(x))
                #folding2d.GetYaxis().SetBinLabel(y+1,str(y))
                #folding2d.SetBinContent(bin,folding[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #if (not model.startswith('SM')): folding2d.SetBinError(bin,dfolding[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #eff2d4l.GetXaxis().SetBinLabel(x+1,str(x))
                #eff2d4l.GetYaxis().SetBinLabel(y+1,str(y))
                #eff2d4l.SetBinContent(bin,effanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*folding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                #deff2d4l = sqrt((effanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*dfolding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])**2+(folding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*deffanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])**2)
                #eff2d4l.SetBinError(bin,deff2d4l) 
        c=TCanvas("c","c",1000,800)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d.GetXaxis().SetTitle(label+'(gen.)')
        eff2d.GetYaxis().SetTitle(label+'(reco.)')
        eff2d.GetZaxis().SetTitle('#epsilon^{ij} ('+fState.replace('mu','#mu')+')')
        eff2d.GetZaxis().SetRangeUser(0.0,1.0) 
        eff2d.Draw("colzTEXTE0")
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.27, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.45, 0.92, model.replace("_"," ")+" GeV (#sqrt{s} = 13 TeV)")
        c.SaveAs("plots/eff2d_"+model+"_"+obsName+"_"+fState+".png")
        c.SaveAs("plots/eff2d_"+model+"_"+obsName+"_"+fState+".pdf")
        del c
        c=TCanvas("c","c",1000,800)                               
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        folding2d.GetXaxis().SetTitle(label+' (gen.)')
        folding2d.GetYaxis().SetTitle(label+' (reco.)')
        folding2d.GetZaxis().SetTitle('P^{ij} ('+fState.replace('mu','#mu')+')')
        folding2d.GetZaxis().SetRangeUser(0.0,1.0) 
        folding2d.Draw("colzTEXT0E") 
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.27, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.DrawLatex(0.43, 0.92, model.replace("_"," ")+" GeV (#sqrt{s} = 8 TeV)")                        
        #c.SaveAs("plots/folding2d_"+model+"_"+obsName+"_"+fState+".png")
        #c.SaveAs("plots/folding2d_"+model+"_"+obsName+"_"+fState+".pdf")
        del c 
        c=TCanvas("c","c",1000,800)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d4l.GetXaxis().SetTitle(label+' (gen.)')
        eff2d4l.GetYaxis().SetTitle(label+' (reco.)')
        eff2d4l.GetZaxis().SetTitle('P^{ij}(4l)#epsilon^{i} ('+fState.replace('mu','#mu')+')')
        eff2d4l.GetZaxis().SetRangeUser(0.0,1.0)
        eff2d4l.Draw("colzTEXT0E")
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.27, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.DrawLatex(0.43, 0.92, model.replace("_"," ")+" GeV (#sqrt{s} = 8 TeV)")                        
        #c.SaveAs("plots/eff2d4l_"+model+"_"+obsName+"_"+fState+".png")
        #c.SaveAs("plots/eff2d4l_"+model+"_"+obsName+"_"+fState+".pdf")
        del c
        del eff2d
        del folding2d
        del eff2d4l
        
