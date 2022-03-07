import optparse
import os
import sys
from array import array
from decimal import *
from math import *
import yaml


# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from sample_shortnames import *
from Utils import *

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
    parser.add_option('',   '--inYAMLFile', dest='inYAMLFile', type='string', default="Inputs/observables_list.yml", help='Input YAML file having observable names and bin information')
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

# Don't move the root import before `sys.argv = grootargs`. Reference: https://root-forum.cern.ch/t/python-options-and-root-options/4641/3
from ROOT import *
from tdrStyle import *
setTDRStyle()

if (not os.path.exists("plots")):
    os.system("mkdir plots")

ROOT.gStyle.SetPaintTextFormat("1.2f")
#ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetNumberContours(99)

obsName = opt.OBSNAME

# Get label name from YAML file.
with open(opt.inYAMLFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    if ( ("Observables" not in cfg) or ("1D_Observables" not in cfg['Observables']) ) :
        print('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                 Please check your YAML file format!!!'''.format(InputYAMLFile))

    label = cfg['Observables']['1D_Observables'][obsName]['label']
    border_msg("Label name: {}".format(label))

obs_bins = opt.OBSBINS.split("|")
if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')):
    print('BINS OPTION MUST START AND END WITH A |')
obs_bins.pop()
obs_bins.pop(0)
if float(obs_bins[len(obs_bins)-1])>199:
    obs_bins[len(obs_bins)-1]='250'
if (opt.OBSNAME=="nJets" or opt.OBSNAME.startswith("njets")):
    obs_bins[len(obs_bins)-1]='4'

sys.path.append('./'+datacardInputs)

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
print("a_bins : ",a_bins)

c=TCanvas("c","c",1000,800)

for model in modelNames:
    for fState in fStates:
        eff2d = TH2D("eff2d", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        # FIXME: ensure if we don't need folding2D and eff2D4l histograms
        # folding2d = TH2D("folding2d", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        # eff2d4l = TH2D("eff2d4l", label, len(obs_bins)-1, a_bins, len(obs_bins)-1, a_bins)
        for x in range(0,len(obs_bins)-1):
            for y in range(0,len(obs_bins)-1):
                # eff2d.GetXaxis().SetBinLabel(x+1,str(x))
                # eff2d.GetYaxis().SetBinLabel(y+1,str(y))
                bin = eff2d.GetBin(x+1,y+1)
                if eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]>0:
                    eff2d.SetBinContent(bin,eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]), eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                else: eff2d.SetBinContent(bin,0), eff2d.SetBinError(bin,0)
                # if (not model.startswith('SM') and eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]!=0):
                # eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                # elif (not model.startswith('SM') and eff[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]==0):
                # eff2d.SetBinError(bin,0)
                # else: eff2d.SetBinError(bin,deff['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                # folding2d.GetXaxis().SetBinLabel(x+1,str(x))
                # folding2d.GetYaxis().SetBinLabel(y+1,str(y))
                # folding2d.SetBinContent(bin,folding[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                # if (not model.startswith('SM')): folding2d.SetBinError(bin,dfolding[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                # eff2d4l.GetXaxis().SetBinLabel(x+1,str(x))
                # eff2d4l.GetYaxis().SetBinLabel(y+1,str(y))
                # eff2d4l.SetBinContent(bin,effanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*folding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])
                # deff2d4l = sqrt((effanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*dfolding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])**2+(folding[model+'_4l_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)]*deffanyreco[model+'_'+fState+'_'+obsName+'_genbin'+str(x)+'_recobin'+str(y)])**2)
                # eff2d4l.SetBinError(bin,deff2d4l)
        # c.cd()
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

        if not os.path.isdir(SigEfficiencyPlots.format(obsName = obsName)): os.makedirs(SigEfficiencyPlots.format(obsName = obsName))
        c.SaveAs(SigEfficiencyPlots.format(obsName = obsName)+"/eff2d_"+model+"_"+obsName+"_"+fState+".png")
        c.SaveAs(SigEfficiencyPlots.format(obsName = obsName)+"/eff2d_"+model+"_"+obsName+"_"+fState+".pdf")
        c.Clear()
        # c=TCanvas("c","c",1000,800)
        # c.cd()
        # c.SetTopMargin(0.10)
        # c.SetRightMargin(0.20)
        # folding2d.GetXaxis().SetTitle(label+' (gen.)')
        # folding2d.GetYaxis().SetTitle(label+' (reco.)')
        # folding2d.GetZaxis().SetTitle('P^{ij} ('+fState.replace('mu','#mu')+')')
        # folding2d.GetZaxis().SetRangeUser(0.0,1.0)
        # folding2d.Draw("colzTEXT0E")
        # latex2 = TLatex()
        # latex2.SetNDC()
        # latex2.SetTextSize(0.5*c.GetTopMargin())
        # latex2.SetTextFont(42)
        # latex2.SetTextAlign(31) # align right
        # latex2.SetTextSize(0.5*c.GetTopMargin())
        # latex2.SetTextFont(62)
        # latex2.SetTextAlign(11) # align right
        # latex2.DrawLatex(0.18, 0.92, "CMS")
        # latex2.SetTextSize(0.4*c.GetTopMargin())
        # latex2.SetTextFont(52)
        # latex2.SetTextAlign(11)
        # latex2.DrawLatex(0.27, 0.92, "Preliminary")
        # latex2.SetTextFont(42)
        # latex2.DrawLatex(0.43, 0.92, model.replace("_"," ")+" GeV (#sqrt{s} = 8 TeV)")
        # c.SaveAs("plots/folding2d_"+model+"_"+obsName+"_"+fState+".png")
        # c.SaveAs("plots/folding2d_"+model+"_"+obsName+"_"+fState+".pdf")
        # del c
        # c=TCanvas("c","c",1000,800)
        # c.cd()
        # c.SetTopMargin(0.10)
        # c.SetRightMargin(0.20)
        # eff2d4l.GetXaxis().SetTitle(label+' (gen.)')
        # eff2d4l.GetYaxis().SetTitle(label+' (reco.)')
        # eff2d4l.GetZaxis().SetTitle('P^{ij}(4l)#epsilon^{i} ('+fState.replace('mu','#mu')+')')
        # eff2d4l.GetZaxis().SetRangeUser(0.0,1.0)
        # eff2d4l.Draw("colzTEXT0E")
        # latex2 = TLatex()
        # latex2.SetNDC()
        # latex2.SetTextSize(0.5*c.GetTopMargin())
        # latex2.SetTextFont(42)
        # latex2.SetTextAlign(31) # align right
        # latex2.SetTextSize(0.5*c.GetTopMargin())
        # latex2.SetTextFont(62)
        # latex2.SetTextAlign(11) # align right
        # latex2.DrawLatex(0.18, 0.92, "CMS")
        # latex2.SetTextSize(0.4*c.GetTopMargin())
        # latex2.SetTextFont(52)
        # latex2.SetTextAlign(11)
        # latex2.DrawLatex(0.27, 0.92, "Preliminary")
        # latex2.SetTextFont(42)
        # latex2.DrawLatex(0.43, 0.92, model.replace("_"," ")+" GeV (#sqrt{s} = 8 TeV)")
        # c.SaveAs("plots/eff2d4l_"+model+"_"+obsName+"_"+fState+".png")
        # c.SaveAs("plots/eff2d4l_"+model+"_"+obsName+"_"+fState+".pdf")
        # del c
        del eff2d
        # del folding2d
        # del eff2d4l

