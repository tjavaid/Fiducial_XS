'''
void plotXSTemplates(const string & _year_="2018", const string & _obsTag_="pT4l", const string & _obsTagLeg_="p_{T}",const string & _obsBins_="|0|10|20|30|45|60|80|120|200|13000|", const int & _nBins_=9)
'''
#########################
# original plotter:
#  https://github.com/vukasinmilosevic/Fiducial_XS/blob/master/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/templates_Freeze/plotXSTemplates.C
########################

import ROOT
import sys, os, pwd
from subprocess import *
import optparse, shlex, re
import math
import time
from decimal import *
import json
from collections import OrderedDict as od
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Utils import processCmd

from tdrStyle import *
from read_bins import *
import yaml

def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('',   '--theoryMass',dest='THEORYMASS',    type='string',default='125.38',   help='Mass value for theory prediction')
    #parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='pT4l',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='mass4l',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    #parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='|0|10|20|30|45|60|80|120|200|13000|',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    parser.add_option('',   '--inYAMLFile', dest='inYAMLFile', type='string', default="Inputs/observables_list.yml", help='Input YAML file having observable names and bin information')
    parser.add_option('',   '--year',  dest='YEAR',  type='string',default='2018',   help='Era to analyze, e.g. 2016, 2017 or 2018')
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
parseOptions()

if 'vs' in opt.OBSNAME:
    obsName_tmp = opt.OBSNAME.split(' vs ')
    obsName = obsName_tmp[0]+'_vs_'+obsName_tmp[1]
    OneDOr2DObs=2
    obs_reco2 = obsName_tmp[1]
else:
    obsName = opt.OBSNAME
    obs_reco2 = ''
    OneDOr2DObs=1
print "OneDOr2DObs:  ", OneDOr2DObs


ObsToStudy = "1D_Observables" if OneDOr2DObs == 1 else "2D_Observables"
print "ObsToStudy:  ", ObsToStudy
with open(opt.inYAMLFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    act_bins_yml_yml = cfg['Observables'][ObsToStudy][opt.OBSNAME]['bins'] 
    obs_label = cfg['Observables'][ObsToStudy][opt.OBSNAME]['label'] 

act_bins_yml = read_bins(act_bins_yml_yml)
print "act_bins_yml_yml  ", act_bins_yml_yml
print " pairs bins act_bins_yml_yml  ", act_bins_yml

nBins = len(act_bins_yml)
year=opt.YEAR

#lumi = {"2016":36330.0,"2017":41480.0,"2018":59830.0}  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis
lumi = {"2016":36.3,"2017":41.5,"2018":59.8}  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis

if obs_reco2 == '':
        nBins = nBins - 1 

print "obsName: ", obsName
print "obs_label: ", obs_label
print "obsBins yml actual: ", act_bins_yml

print "nBins:  ", nBins

def setHistProperties(hist, lineWidth, lineStyle, lineColor, fillStyle=0, fillColor=0, xAxisTitle = "skip", yAxisTitle = "skip"):
    if not hist: return
    hist.SetLineWidth(lineWidth)
    hist.SetLineStyle(lineStyle)
    hist.SetLineColor(lineColor)
    hist.SetFillStyle(fillStyle)
    hist.SetFillColor(fillColor)
    hist.GetXaxis().SetNdivisions(510)
    hist.GetYaxis().SetNdivisions(510)
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleOffset(1.1)
    hist.GetYaxis().SetTitleOffset(1.24)
    if (xAxisTitle!="skip"): hist.GetXaxis().SetTitle(xAxisTitle)
    if (yAxisTitle!="skip"): hist.GetYaxis().SetTitle(yAxisTitle)

def cmsPreliminary(c):
    c.cd();

    CMSPrelim = ROOT.TLatex();
    CMSPrelim.SetNDC(ROOT.kTRUE);

    CMSPrelim.SetTextSize(0.5*c.GetTopMargin());
    CMSPrelim.SetTextFont(42);
    CMSPrelim.SetTextAlign(31); #// align right
 #   //CMSPrelim.DrawLatex(0.93, 0.96,"36.8 fb^{-1} at #sqrt{s} = 13 TeV");
    #CMSPrelim.DrawLatex(0.93, 0.96,"58.9 fb^{-1} at #sqrt{s} = 13 TeV");
    CMSPrelim.DrawLatex(0.93, 0.96,str(lumi[opt.YEAR])+ " fb^{-1} at #sqrt{s} = 13 TeV");

    CMSPrelim.SetTextSize(0.9*c.GetTopMargin());
    CMSPrelim.SetTextFont(62);
    CMSPrelim.SetTextAlign(11); #// align right
    CMSPrelim.DrawLatex(0.27, 0.85, "CMS");

    CMSPrelim.SetTextSize(0.7*c.GetTopMargin());
    CMSPrelim.SetTextFont(52);
    CMSPrelim.SetTextAlign(11);
    CMSPrelim.DrawLatex(0.25, 0.8, "Preliminary");


def setLegendProperties(leg, sHeader = "skip", fillStyle=0, fillColor=0):
    if not leg: return
    if (sHeader!="skip"): leg.SetHeader(sHeader)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(43)


def normaliseHist(h1D, norm = 1.):
    if (h1D.Integral()==0): return -1; 
    h1D.Scale(norm/h1D.Integral());
    return 0;


def fillEmptyBinsHist1D(h1D, floor):
    nXbins=h1D.GetNbinsX();
    #for(int i=1, i<=nXbins, i++):
#    for(int i=1, i<=nXbins, i++):
    for i in range(nXbins):
        #h1D.SetBinContent(i,h1D.GetBinContent(i)+floor);
        h1D.SetBinContent(i+1,h1D.GetBinContent(i+1)+floor);
    return 0;



def smoothAndNormaliseTemplate1D(h1D, norm = 1.):
    # smooth
    h1D.Smooth();
    #h1D.Smooth(10000);
    #norm + floor + norm
    normaliseHist(h1D, norm);
    fillEmptyBinsHist1D(h1D,.001/(h1D.GetNbinsX()));
    normaliseHist(h1D, norm);
 
def normaliseHist1D(h1D, norm = 1.):
    if (h1D.Integral()==0):
	 return -1; 
    h1D.Scale(norm/h1D.Integral());

    return 0;


#act_bins_yml, doubleDiff = binning(opt.OBSNAME)

obsTag = opt.OBSNAME

if OneDOr2DObs==2:
    binRange = [str(act_bins_yml[i][0])+'_'+str(act_bins_yml[i][1])+'_'+str(act_bins_yml[i][2])+'_'+str(act_bins_yml[i][3]) for i in range(nBins)]
    obsTag = obsTag.split(' vs ')[0]+'_'+obsTag.split(' vs ')[1]
    binRangeLeg = [str(act_bins_yml[i][0])+'<'+obsTag+'<'+str(act_bins_yml[i][1])+'/'+str(act_bins_yml[i][2])+'<'+obsTag+'<'+str(act_bins_yml[i][3]) for i in range(nBins)]
else:
    binRange = [str(act_bins_yml[i])+'_'+str(act_bins_yml[i+1]) for i in range(nBins)]
    binRangeLeg = [str(act_bins_yml[i])+'<'+obsTag+'<'+str(act_bins_yml[i+1]) for i in range(nBins)]

print(binRange)
print(binRangeLeg)


setTDRStyle()
c1 = ROOT.TCanvas('c1',"",0,0,800,800)
c1.cd(1)
c1.SetLogy(0)
gStyle.SetOptStat('')
gStyle.SetPalette(1)
c1.GetPad(0).SetRightMargin(0.05)
c1.GetPad(0).SetLeftMargin(0.15)
c1.GetPad(0).SetTopMargin(0.05)
c1.GetPad(0).SetBottomMargin(0.15)

bkgName=['qqZZ','ggZZ','ZJetsCR']
sTemplateDirName = os.getcwd()+"/templates/templatesXS_"+str(year)+"/DTreeXS_"+obsTag+"/13TeV/";
sPlotsStore = os.getcwd()+"/templates/plotsXS_"+str(year)+"/"+obsTag+"/";
fTemplateFile_2e2mu = {}
fTemplateFile_4mu = {}
fTemplateFile_4e = {}
h1D_2e2mu = {}
h1D_4mu = {}
h1D_4e = {}

for iBin in range(nBins):
    for iBkg in range(len(bkgName)):

	if iBkg=='ZJetsCR': 
	    nSmooth = 2;
	else:
	    nSmooth = 1;
        sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_2e2mu_"+obsTag+"_"+binRange[iBin]+".root"
        fTemplateFile_2e2mu[iBkg,iBin] = ROOT.TFile(sTemplateDirName+"/"+sTemplateFileName, "READ")
        h1D_2e2mu[iBkg,iBin] = ROOT.TH1D()
        h1D_2e2mu[iBkg,iBin] = fTemplateFile_2e2mu[iBkg,iBin].Get("m4l_"+obsTag+"_"+binRange[iBin])
	for k in range(nSmooth): #(int k = 0; k < nSmooth; k++):
	    smoothAndNormaliseTemplate1D(h1D_2e2mu[iBkg,iBin]);

        sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_4mu_"+obsTag+"_"+binRange[iBin]+".root"
        fTemplateFile_4mu[iBkg,iBin] = ROOT.TFile(sTemplateDirName+"/"+sTemplateFileName, "READ")
        h1D_4mu[iBkg,iBin] = ROOT.TH1D()
        h1D_4mu[iBkg,iBin] = fTemplateFile_4mu[iBkg,iBin].Get("m4l_"+obsTag+"_"+binRange[iBin])
	for k in range(nSmooth): #(int k = 0; k < nSmooth; k++):
	    smoothAndNormaliseTemplate1D(h1D_4mu[iBkg,iBin]);

        sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_4e_"+obsTag+"_"+binRange[iBin]+".root"
        fTemplateFile_4e[iBkg,iBin] = ROOT.TFile(sTemplateDirName+"/"+sTemplateFileName, "READ")
        h1D_4e[iBkg,iBin] = ROOT.TH1D()
        h1D_4e[iBkg,iBin] = fTemplateFile_4e[iBkg,iBin].Get("m4l_"+obsTag+"_"+binRange[iBin])

	for k in range(nSmooth): #(int k = 0; k < nSmooth; k++):
	    smoothAndNormaliseTemplate1D(h1D_4e[iBkg,iBin]);

        print(sTemplateFileName)
        print("m4l_"+obsTag+"_"+binRange[iBin])

var_plotHigh = 160.0; var_plotLow = 105.0;
var_nBins = 20
varAxLabel = 'm_{4l} (GeV)'
binWidth = (int(100*(var_plotHigh - var_plotLow)/var_nBins))/100.
h1D_dummy = ROOT.TH1D("dummy", "dummy", var_nBins, var_plotLow, var_plotHigh)
setHistProperties(h1D_dummy,1,1,ROOT.kBlue-7,0,0,varAxLabel,"Events/"+str(binWidth)+'(GeV)')

lineWidth = 2
leg_xl = 0.52
leg_xr = 0.90
leg_yb = 0.72
leg_yt = 0.90

kBkg_qqZZ = 0
kBkg_ggZZ = 1
kBkg_ZJets = 2
c1.cd()
for iBin in range(nBins):

    ########## 2e2mu ##########
    #### qqZZZ + ggZZ +ZX ####
    h1D_dummy.SetMaximum(2.0*h1D_2e2mu[kBkg_qqZZ,iBin].GetMaximum())
    h1D_dummy.Draw()
    cmsPreliminary(c1); #, binRangeLeg[iBin]+"      2e2#mu      "+year)
    leg1 = ROOT.TLegend(leg_xl,leg_yb,leg_xr,leg_yt)
    setLegendProperties(leg1,binRangeLeg[iBin]+", 2e2#mu")
    setHistProperties(h1D_2e2mu[kBkg_qqZZ,iBin],lineWidth,1,ROOT.kBlack)
    h1D_2e2mu[kBkg_qqZZ,iBin].Draw("histsame")
    leg1.AddEntry(h1D_2e2mu[kBkg_qqZZ,iBin], "q#bar{q} #rightarrow ZZ","L")
    setHistProperties(h1D_2e2mu[kBkg_ggZZ,iBin],lineWidth,1,ROOT.kBlue-7)
    h1D_2e2mu[kBkg_ggZZ,iBin].Draw("histsame")
    leg1.AddEntry(h1D_2e2mu[kBkg_ggZZ,iBin], "gg #rightarrow ZZ","L");
    setHistProperties(h1D_2e2mu[kBkg_ZJets,iBin],lineWidth,1,ROOT.kRed-7)
    h1D_2e2mu[kBkg_ZJets,iBin].Draw("histsame")
    leg1.AddEntry(h1D_2e2mu[kBkg_ZJets,iBin], "Z + X","L")
    leg1.Draw()
    c1.SaveAs(sPlotsStore+"/XSTemplates_2e2mu_"+obsTag+"_"+year+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+"_"+bkgName[kBkg_ZJets]+".pdf")
    c1.SaveAs(sPlotsStore+"/XSTemplates_2e2mu_"+obsTag+"_"+year+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+"_"+bkgName[kBkg_ZJets]+".png")

    ########## 4mu ##########
    #### qqZZZ + ggZZ +ZX ####
    h1D_dummy.SetMaximum(2.0*h1D_4mu[kBkg_qqZZ,iBin].GetMaximum())
    h1D_dummy.Draw()
    cmsPreliminary(c1) #, binRangeLeg[iBin]+"      4#mu      "+year)
    leg2 = ROOT.TLegend(leg_xl,leg_yb,leg_xr,leg_yt)
    setLegendProperties(leg2,binRangeLeg[iBin]+", 4#mu")
    setHistProperties(h1D_4mu[kBkg_qqZZ,iBin],lineWidth,1,ROOT.kBlack)
    h1D_4mu[kBkg_qqZZ,iBin].Draw("histsame")
    leg2.AddEntry(h1D_4mu[kBkg_qqZZ,iBin], "q#bar{q} #rightarrow ZZ","L")
    setHistProperties(h1D_4mu[kBkg_ggZZ,iBin],lineWidth,1,ROOT.kBlue-7)
    h1D_4mu[kBkg_ggZZ,iBin].Draw("histsame")
    leg2.AddEntry(h1D_4mu[kBkg_ggZZ,iBin], "gg #rightarrow ZZ","L");
    setHistProperties(h1D_4mu[kBkg_ZJets,iBin],lineWidth,1,ROOT.kRed-7)
    h1D_4mu[kBkg_ZJets,iBin].Draw("histsame")
    leg2.AddEntry(h1D_4mu[kBkg_ZJets,iBin], "Z + X","L")
    leg2.Draw()
    c1.SaveAs(sPlotsStore+"/XSTemplates_4mu_"+obsTag+"_"+year+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+"_"+bkgName[kBkg_ZJets]+".pdf")
    c1.SaveAs(sPlotsStore+"/XSTemplates_4mu_"+obsTag+"_"+year+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+"_"+bkgName[kBkg_ZJets]+".png")

    ########## 4e ##########
    #### qqZZZ + ggZZ +ZX ####
    h1D_dummy.SetMaximum(2.0*h1D_4e[kBkg_qqZZ,iBin].GetMaximum())
    h1D_dummy.Draw()
    cmsPreliminary(c1) #, binRangeLeg[iBin]+"      4e      "+year)
    leg3 = ROOT.TLegend(leg_xl,leg_yb,leg_xr,leg_yt)
    setLegendProperties(leg3,binRangeLeg[iBin]+", 4e")
    setHistProperties(h1D_4e[kBkg_qqZZ,iBin],lineWidth,1,ROOT.kBlack)
    h1D_4e[kBkg_qqZZ,iBin].Draw("histsame")
    leg3.AddEntry(h1D_4e[kBkg_qqZZ,iBin], "q#bar{q} #rightarrow ZZ","L")
    setHistProperties(h1D_4e[kBkg_ggZZ,iBin],lineWidth,1,ROOT.kBlue-7)
    h1D_4e[kBkg_ggZZ,iBin].Draw("histsame")
    leg3.AddEntry(h1D_4e[kBkg_ggZZ,iBin], "gg #rightarrow ZZ","L");
    setHistProperties(h1D_4e[kBkg_ZJets,iBin],lineWidth,1,ROOT.kRed-7)
    h1D_4e[kBkg_ZJets,iBin].Draw("histsame")
    leg3.AddEntry(h1D_4e[kBkg_ZJets,iBin], "Z + X","L")
    leg3.Draw()
    c1.SaveAs(sPlotsStore+"/XSTemplates_4e_"+obsTag+"_"+year+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+"_"+bkgName[kBkg_ZJets]+".pdf")
    c1.SaveAs(sPlotsStore+"/XSTemplates_4e_"+obsTag+"_"+year+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+"_"+bkgName[kBkg_ZJets]+".png")


# qqZZ for all the bins
h1D_dummy.SetMaximum(2.0*h1D_2e2mu[kBkg_qqZZ,0].GetMaximum());
h1D_dummy.Draw(); cmsPreliminary(c1); leg4 = ROOT.TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg4,"q#bar{q} #rightarrow ZZ");
hSum_2e2mu = h1D_2e2mu[kBkg_qqZZ,0].Clone(); 
hSum_4mu = h1D_4mu[kBkg_qqZZ,0].Clone(); 
hSum_4e = h1D_4e[kBkg_qqZZ,0].Clone(); 
for iBin in range(nBins-1):
#for iBin in range(nBins):
#    hSum.Add(h1D_2e2mu[kBkg_qqZZ,iBin]); hSum.Add(h1D_4mu[kBkg_qqZZ,iBin]); hSum.Add(h1D_4e[kBkg_qqZZ,iBin]);
    hSum_2e2mu.Add(h1D_2e2mu[kBkg_qqZZ,iBin+1]);
    hSum_4mu.Add(h1D_4mu[kBkg_qqZZ,iBin+1]);
    hSum_4e.Add(h1D_4e[kBkg_qqZZ,iBin+1]);

hSum = hSum_2e2mu.Clone();hSum.Add(hSum_4mu);hSum.Add(hSum_4e);

setHistProperties(hSum,lineWidth,1,ROOT.kGreen-7); hSum.Draw("histsame"); leg4.AddEntry(hSum, "4l, all bins","L");normaliseHist1D(hSum);
setHistProperties(hSum_2e2mu,lineWidth,1,ROOT.kRed-7); hSum_2e2mu.Draw("histsame"); leg4.AddEntry(hSum_2e2mu, "2e2#mu, all bins","L");normaliseHist1D(hSum_2e2mu);
setHistProperties(hSum_4mu,lineWidth,2,ROOT.kRed-7); hSum_4mu.Draw("histsame"); leg4.AddEntry(hSum_4mu, "4#mu, all bins","L");normaliseHist1D(hSum_4mu);
setHistProperties(hSum_4e,lineWidth,3,ROOT.kBlue-7); hSum_4e.Draw("histsame"); leg4.AddEntry(hSum_4e, "4e, all bins","L");normaliseHist1D(hSum_4e);
leg4.Draw(); 
c1.SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_qqZZ]+"_allBins.pdf");
c1.SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_qqZZ]+"_allBins.png");


# ggZZ for all the bins
h1D_dummy.SetMaximum(2.0*h1D_2e2mu[kBkg_ggZZ,0].GetMaximum());
h1D_dummy.Draw(); cmsPreliminary(c1); leg5 = ROOT.TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg5,"gg #rightarrow ZZ");
hSum_2e2mu = h1D_2e2mu[kBkg_ggZZ,0].Clone(); 
hSum_4mu = h1D_4mu[kBkg_ggZZ,0].Clone(); 
hSum_4e = h1D_4e[kBkg_ggZZ,0].Clone(); 
for iBin in range(nBins-1):
#for iBin in range(nBins):
#    hSum.Add(h1D_2e2mu[kBkg_ggZZ,iBin]); hSum.Add(h1D_4mu[kBkg_ggZZ,iBin]); hSum.Add(h1D_4e[kBkg_ggZZ,iBin]);
    hSum_2e2mu.Add(h1D_2e2mu[kBkg_ggZZ,iBin+1]);
    hSum_4mu.Add(h1D_4mu[kBkg_ggZZ,iBin+1]);
    hSum_4e.Add(h1D_4e[kBkg_ggZZ,iBin+1]);

hSum = hSum_2e2mu.Clone();hSum.Add(hSum_4mu);hSum.Add(hSum_4e);

setHistProperties(hSum,lineWidth,1,ROOT.kGreen-7); hSum.Draw("histsame"); leg5.AddEntry(hSum, "4l, all bins","L");normaliseHist1D(hSum);
setHistProperties(hSum_2e2mu,lineWidth,1,ROOT.kRed-7); hSum_2e2mu.Draw("histsame"); leg5.AddEntry(hSum_2e2mu, "2e2#mu, all bins","L");normaliseHist1D(hSum_2e2mu);
setHistProperties(hSum_4mu,lineWidth,2,ROOT.kRed-7); hSum_4mu.Draw("histsame"); leg5.AddEntry(hSum_4mu, "4#mu, all bins","L");normaliseHist1D(hSum_4mu);
setHistProperties(hSum_4e,lineWidth,3,ROOT.kBlue-7); hSum_4e.Draw("histsame"); leg5.AddEntry(hSum_4e, "4e, all bins","L");normaliseHist1D(hSum_4e);
leg5.Draw(); 
c1.SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_ggZZ]+"_allBins.pdf");
c1.SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_ggZZ]+"_allBins.png");



# ZJetsCR for all the bins
h1D_dummy.SetMaximum(2.0*h1D_2e2mu[kBkg_ZJets,0].GetMaximum());
h1D_dummy.Draw(); cmsPreliminary(c1); leg6 = ROOT.TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg6,"Z + X #rightarrow ZZ");
hSum_2e2mu = h1D_2e2mu[kBkg_ZJets,0].Clone(); 
hSum_4mu = h1D_4mu[kBkg_ZJets,0].Clone(); 
hSum_4e = h1D_4e[kBkg_ZJets,0].Clone(); 
for iBin in range(nBins-1):
#for iBin in range(nBins):
#    hSum.Add(h1D_2e2mu[kBkg_ZJets,iBin]); hSum.Add(h1D_4mu[kBkg_ZJets,iBin]); hSum.Add(h1D_4e[kBkg_ZJets,iBin]);
    hSum_2e2mu.Add(h1D_2e2mu[kBkg_ZJets,iBin+1]);
    hSum_4mu.Add(h1D_4mu[kBkg_ZJets,iBin+1]);
    hSum_4e.Add(h1D_4e[kBkg_ZJets,iBin+1]);

hSum = hSum_2e2mu.Clone();hSum.Add(hSum_4mu);hSum.Add(hSum_4e);

setHistProperties(hSum,lineWidth,1,ROOT.kGreen-7); hSum.Draw("histsame"); leg6.AddEntry(hSum, "4l, all bins","L");normaliseHist1D(hSum);
setHistProperties(hSum_2e2mu,lineWidth,1,ROOT.kRed-7); hSum_2e2mu.Draw("histsame"); leg6.AddEntry(hSum_2e2mu, "2e2#mu, all bins","L");normaliseHist1D(hSum_2e2mu);
setHistProperties(hSum_4mu,lineWidth,2,ROOT.kRed-7); hSum_4mu.Draw("histsame"); leg6.AddEntry(hSum_4mu, "4#mu, all bins","L");normaliseHist1D(hSum_4mu);
setHistProperties(hSum_4e,lineWidth,3,ROOT.kBlue-7); hSum_4e.Draw("histsame"); leg6.AddEntry(hSum_4e, "4e, all bins","L");normaliseHist1D(hSum_4e);
leg6.Draw(); 
c1.SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_ZJets]+"_allBins.pdf");
c1.SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_ZJets]+"_allBins.png");


del c1;



'''
pairs bins act_bins_yml_yml   ['0', '10', '20', '30', '45', '60', '80', '120', '200', '13000']
obsName:  pT4l
obs_label:  p_{T}(H)
obsBins yml actual:  ['0', '10', '20', '30', '45', '60', '80', '120', '200', '13000']
nBins:   9
'''


#void plotXSTemplates(const string & _year_="2018", const string & _obsTag_="pT4l", const string & _obsTagLeg_="p_{T}",const string & _obsBins_="|0|10|20|30|45|60|80|120|200|13000|", const int & _nBins_=9)


#cmd = "root -l -b -q "+os.getcwd()+"/templates/plotXSTemplates.C\(2018,\"pT4l\",\"p_{T}\",\"['0', '10', '20', '30', '45', '60', '80', '120', '200', '13000']\",9\)"
#print cmd 
#os.system(cmd)

