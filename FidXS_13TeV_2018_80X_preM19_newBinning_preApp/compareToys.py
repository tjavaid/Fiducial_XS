from ROOT import *
from array import array
from math import *
from decimal import *

from tdrStyle import *
setTDRStyle()

def plotToy():

    # Load some libraries                                 
    ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
    ROOT.gSystem.Load("$CMSSW_BASE/lib/slc6_amd64_gcc491/libHiggsAnalysisCombinedLimit.so")
    ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
    ROOT.gSystem.AddIncludePath("-Iinclude/")
    
    f_pre = TFile("higgsCombinepT4lpre.MultiDimFit.mH125.123456.root",'READ')
    d_pre = f_pre.Get("toys/toy_asimov") 

    f_post = TFile("higgsCombinepT4lpost.MultiDimFit.mH125.123456.root",'READ')
    d_post = f_post.Get("toys/toy_asimov") 

    CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",105.0,140.0)
    mass = CMS_zz4l_mass.frame(RooFit.Bins(15))
    
    d_post.plotOn(mass,RooFit.LineColor(2),RooFit.MarkerColor(2),RooFit.LineWidth(4))
    d_pre.plotOn(mass,RooFit.LineColor(1),RooFit.MarkerColor(1),RooFit.LineWidth(1))

    c = TCanvas("c","c",800,800)
    c.cd()
    #if (var=="err"): 
    #  c.SetLogy()
        
    datahistpre = RooAbsData.createHistogram(d_pre,"datahistpre",CMS_zz4l_mass,RooFit.Binning(15,105,140))
    datahistpost = RooAbsData.createHistogram(d_post,"datahistpost",CMS_zz4l_mass,RooFit.Binning(15,105,140))

    datahistpre.SetLineColor(1)
    datahistpre.SetMarkerColor(1)
    datahistpre.SetMarkerSize(1.2)
    datahistpre.SetMarkerStyle(20)

    datahistpost.SetLineColor(1)
    datahistpost.SetMarkerColor(1)
    datahistpost.SetMarkerSize(1.2)
    datahistpost.SetMarkerStyle(20)
    
    dummy = TH1D("","",1,105.0,140.0)
    dummy.SetBinContent(1,2)
    dummy.SetFillColor(0)
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetMarkerSize(0)
    dummy.SetMarkerColor(0) 
    dummy.GetYaxis().SetTitle("Events")
    dummy.GetXaxis().SetTitle("m_{4l} (GeV)")
    dummy.SetMinimum(0.0)
    dummy.SetMaximum(1.5*datahistpre.GetMaximum())
    dummy.Draw()
    
    dummy_data = TH1D()
    dummy_data.SetMarkerColor(kBlack)
    dummy_data.SetMarkerStyle(20)

    mass.Draw("same")
    
    #legend = TLegend(.20,.41,.53,.89)
    #legend.SetTextSize(0.03)
    #legend.AddEntry(dummy_data,"Toy Number "+str(toy),"ep")
                                                                          
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right
    #latex2.DrawLatex(0.95, 0.95,"10.0 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.8*c.GetTopMargin())
    latex2.SetTextFont(62)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.19, 0.95, "CMS")
    latex2.SetTextSize(0.6*c.GetTopMargin())
    latex2.SetTextFont(52)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.30, 0.95, "Preliminary")
    latex2.SetTextFont(42)
    latex2.SetTextSize(0.45*c.GetTopMargin())
    
    c.SaveAs("compareasimov.pdf")

plotToy()
