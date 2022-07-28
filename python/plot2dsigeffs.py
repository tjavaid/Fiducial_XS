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
from read_bins import read_bins

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
    parser.add_option('', '--obs', dest='OneDOr2DObs', default=1, type=int, help="1 for 1D obs, 2 for 2D observable")
    parser.add_option('-y', '--year', dest="ERA", type = 'string', default = '2018', help='Specifies the data taking period')

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

ObsToStudy = "1D_Observables" if opt.OneDOr2DObs == 1 else "2D_Observables"
obsName = opt.OBSNAME
ListObsName = (''.join(obsName.split())).split('vs')

# Get label name from YAML file.
with open(opt.inYAMLFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
        print('''No section named 'observable' or sub-section name '1D-Observable' or '2D-Observable' found in file {}.
                 Please check your YAML file format!!!'''.format(InputYAMLFile))

    label = cfg['Observables'][ObsToStudy][obsName]['label']
    # border_msg("Label name: {}".format(label))


obs_bins = read_bins(opt.OBSBINS)
logger.info("Parsed bins: {}".format(obs_bins))
logger.info("Bin size = "+str(len(obs_bins)))

nBins = len(obs_bins) -1
if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
    nBins = len(obs_bins)
logger.debug("nBins: = "+str(nBins))

if float(obs_bins[nBins])>199:
    obs_bins[nBins]='250'
if (opt.OBSNAME=="nJets" or opt.OBSNAME.startswith("njets")): # FIXME: This won't work for 2D bins
    obs_bins[nBins]='4'

datacardInputs = datacardInputs.format(year = opt.ERA)
sys.path.append('./'+datacardInputs)

_temp = __import__('inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['eff','deff'], -1)
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
        eff2d = TH2D("eff2d", label, nBins, a_bins, nBins, a_bins)
        # FIXME: ensure if we don't need folding2D and eff2D4l histograms
        # folding2d = TH2D("folding2d", label, nBins, a_bins, nBins, a_bins)
        # eff2d4l = TH2D("eff2d4l", label, nBins, a_bins, nBins, a_bins)
        for x in range(0,nBins):
            for y in range(0,nBins):
                # eff2d.GetXaxis().SetBinLabel(x+1,str(x))
                # eff2d.GetYaxis().SetBinLabel(y+1,str(y))
                bin = eff2d.GetBin(x+1,y+1)
                if eff[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]>0:
                    eff2d.SetBinContent(bin,eff[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]), eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])
                else: eff2d.SetBinContent(bin,0), eff2d.SetBinError(bin,0)
                # if (not model.startswith('SM') and eff[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]!=0):
                # eff2d.SetBinError(bin,deff[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])
                # elif (not model.startswith('SM') and eff[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]==0):
                # eff2d.SetBinError(bin,0)
                # else: eff2d.SetBinError(bin,deff['ggH_powheg_JHUgen_125_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])
                # folding2d.GetXaxis().SetBinLabel(x+1,str(x))
                # folding2d.GetYaxis().SetBinLabel(y+1,str(y))
                # folding2d.SetBinContent(bin,folding[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])
                # if (not model.startswith('SM')): folding2d.SetBinError(bin,dfolding[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])
                # eff2d4l.GetXaxis().SetBinLabel(x+1,str(x))
                # eff2d4l.GetYaxis().SetBinLabel(y+1,str(y))
                # eff2d4l.SetBinContent(bin,effanyreco[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]*folding[model+'_4l_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])
                # deff2d4l = sqrt((effanyreco[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]*dfolding[model+'_4l_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])**2+(folding[model+'_4l_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)]*deffanyreco[model+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(x)+'_recobin'+str(y)])**2)
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

        SigEfficiencyPlots = SigEfficiencyPlots.format(year = opt.ERA, obsName = obsName.replace(' ','_'))
        GetDirectory(SigEfficiencyPlots)

        c.SaveAs(SigEfficiencyPlots + "/eff2d_"+model+"_"+obsName.replace(' ','_')+"_"+fState+".png")
        c.SaveAs(SigEfficiencyPlots + "/eff2d_"+model+"_"+obsName.replace(' ','_')+"_"+fState+".pdf")
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

