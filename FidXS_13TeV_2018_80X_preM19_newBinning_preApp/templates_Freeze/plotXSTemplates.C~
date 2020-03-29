//-----------------------------------
// last update: 2014.10.02
//-----------------------------------

// ROOT include
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TH1D.h>
#include "TH2.h"
#include "TChain.h"
#include <TStyle.h>
#include <TMath.h>
#include <TROOT.h>
#include "TRandom.h"

// C include
#include <iostream>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <stdio.h>
#include "TLatex.h"

using namespace std;

const TString sPlotsStore = "plotsXS/";

//_______________________________________________________________________________________________________________________________________________
void cmsPreliminary(TCanvas* &c){
    c->cd();

    TLatex *CMSPrelim = new TLatex();
    CMSPrelim->SetNDC(kTRUE);

    CMSPrelim->SetTextSize(0.5*c->GetTopMargin());
    CMSPrelim->SetTextFont(42);
    CMSPrelim->SetTextAlign(31); // align right
    CMSPrelim->DrawLatex(0.93, 0.96,"7.65 fb^{-1} at #sqrt{s} = 13 TeV");

    CMSPrelim->SetTextSize(0.9*c->GetTopMargin());
    CMSPrelim->SetTextFont(62);
    CMSPrelim->SetTextAlign(11); // align right
    CMSPrelim->DrawLatex(0.27, 0.85, "CMS");

    CMSPrelim->SetTextSize(0.7*c->GetTopMargin());
    CMSPrelim->SetTextFont(52);
    CMSPrelim->SetTextAlign(11);
    CMSPrelim->DrawLatex(0.25, 0.8, "Preliminary");
}

//_______________________________________________________________________________________________________________________________________________
void analysisInit() {
    gErrorIgnoreLevel = kWarning;
    gErrorIgnoreLevel = kError;
}

//_______________________________________________________________________________________________________________________________________________
void setCavasAndStyles(TString canvasName, TCanvas* &c, TString stat = "", double leftMaring = 0.15, double rightMaring = 0.05, double bottomMaring = 0.15, double topMaring = 0.05){
    // setup environment
    gROOT->ProcessLine(".L setTDRStyle.C"); setTDRStyle();
    // setup canvas
    c = new TCanvas(canvasName,"myPlots",0,0,800,800);
    c->cd(1); c->SetLogy(0);
    gStyle->SetOptStat(stat);
    gStyle->SetPalette(1);

    c->GetPad(0)->SetRightMargin(rightMaring);
    c->GetPad(0)->SetLeftMargin(leftMaring);
    c->GetPad(0)->SetTopMargin(topMaring);
    c->GetPad(0)->SetBottomMargin(bottomMaring);
}

//_______________________________________________________________________________________________________________________________________________
int normaliseHist(TH1D* &h1D, double norm = 1.){
    if (h1D->Integral()==0) return -1;
    h1D->Scale(norm/h1D->Integral());

    return 0;
}

//_______________________________________________________________________________________________________________________________________________
int setHistProperties(TH1D* &hist, Width_t lineWidth, Style_t lineStyle, Color_t lineColor, Style_t fillStyle=0, Color_t fillColor=0, TString xAxisTitle = "skip", TString yAxisTitle = "skip"){
    if (!hist) return -1;
    // line
    hist->SetLineWidth(lineWidth);
    hist->SetLineStyle(lineStyle);
    hist->SetLineColor(lineColor);
    // fill
    hist->SetFillStyle(fillStyle);
    hist->SetFillColor(fillColor);
    // divisions, offsets, sizes
    hist->GetXaxis()->SetNdivisions(510);
    hist->GetYaxis()->SetNdivisions(510);
    hist->GetXaxis()->SetLabelSize(0.05);
    hist->GetYaxis()->SetLabelSize(0.05);
    hist->GetXaxis()->SetTitleOffset(1.2);
    hist->GetYaxis()->SetTitleOffset(1.2);
    // titles
    if (xAxisTitle!="skip") hist->GetXaxis()->SetTitle(xAxisTitle);
    if (yAxisTitle!="skip") hist->GetYaxis()->SetTitle(yAxisTitle);
    // return
    return 0;
}

//_______________________________________________________________________________________________________________________________________________
int setHistProperties2D(TH2D* &hist, TString xAxisTitle = "skip", TString yAxisTitle = "skip"){
    if (!hist) return -1;
    // divisions, offsets, sizes
    hist->GetXaxis()->SetNdivisions(510);
    hist->GetYaxis()->SetNdivisions(510);
    hist->GetXaxis()->SetLabelSize(0.05);
    hist->GetYaxis()->SetLabelSize(0.05);
    hist->GetXaxis()->SetTitleOffset(1.2);
    hist->GetYaxis()->SetTitleOffset(1.2);
    // titles
    if (xAxisTitle!="skip") hist->GetXaxis()->SetTitle(xAxisTitle);
    if (yAxisTitle!="skip") hist->GetYaxis()->SetTitle(yAxisTitle);
    // return
    return 0;
}

//_______________________________________________________________________________________________________________________________________________
int setLegendProperties(TLegend* &leg, TString sHeader = "skip", Style_t fillStyle=0, Color_t fillColor=0){
    // sanity-check
    if (!leg) return -1;
    // titles
    if (sHeader!="skip") leg->SetHeader(sHeader);;
    leg->SetFillColor(0);
    leg->SetFillStyle(0);
    leg->SetBorderSize(0);
    leg->SetTextFont(42);
    // return
    return 0;
}

//_______________________________________________________________________________________________________________________________________________
void smoothAndNormaliseTemplate2D(TH2D* &h2D, bool silent = 1){

    int nXbins=h2D->GetNbinsX();
    int nYbins=h2D->GetNbinsY();
    // smooth
    TString smthAlg = "k5b";
    if (!silent) cout << "   Pre-Smooth:  " << h2D->Integral() << endl;
    h2D->Smooth(1, smthAlg);
    if (!silent) cout << "   Post-Smooth: " << h2D->Integral() << endl;
    // norm + floor + norm
    normaliseHist2D(h2D);
    if (!silent) cout << "   Normalised:  " << h2D->Integral() << endl;
    double floor = .001/(nXbins*nYbins);
    fillEmptyBinsHist2D(h2D,floor);
    if (!silent) cout << "   Post-Floor:  " << h2D->Integral() << endl;
    normaliseHist2D(h2D);
    if (!silent) cout << "   Final:       " << h2D->Integral() << endl;
}

//_______________________________________________________________________________________________________________________________________________
void smoothAndNormaliseTemplate1D(TH1D* &h1D, double norm = 1.){
    // smooth
    h1D->Smooth();
    // norm + floor + norm
    normaliseHist(h1D, norm);
    fillEmptyBinsHist1D(h1D,.001/(h1D->GetNbinsX()));
    normaliseHist(h1D, norm);
}

//_______________________________________________________________________________________________________________________________________________
int normaliseHist2D(TH2D* &h2D, double norm = 1.){
    if (h2D->Integral()==0) return -1;
    h2D->Scale(norm/h2D->Integral());

    return 0;
}

//_______________________________________________________________________________________________________________________________________________
int fillEmptyBinsHist2D(TH2D* &h2D, double floor) {
    int nXbins=h2D->GetNbinsX();
    int nYbins=h2D->GetNbinsY();
    for(int i=1; i<=nXbins; i++){
        for(int j=1; j<=nYbins; j++){
            h2D->SetBinContent(i,j,h2D->GetBinContent(i,j)+floor);
        }
    }

    return 0;
}

//_______________________________________________________________________________________________________________________________________________
int normaliseHist1D(TH1D* &h1D, double norm = 1.){
    if (h1D->Integral()==0) return -1;
    h1D->Scale(norm/h1D->Integral());

    return 0;
}

//_______________________________________________________________________________________________________________________________________________
int fillEmptyBinsHist1D(TH1D* &h1D, double floor) {
    int nXbins=h1D->GetNbinsX();
    for(int i=1; i<=nXbins; i++){
        h1D->SetBinContent(i,h1D->GetBinContent(i)+floor);
    }

    return 0;
}

//_______________________________________________________________________________________________________________________________________________
void plotXSTemplates() {

    analysisInit();

    // setup environment & canvas
    TCanvas *c1;
    setCavasAndStyles("c1",c1,"");

    /*
    TString obsTag = "pT4l";
    const TString sTemplateDirName = "templatesXS/DTreeXS_"+obsTag+"/13TeV/";
    const int N_BINS = 4;
    TString binRange[N_BINS]     = {"0.0_15.0",      "15.0_30.0",      "30.0_60.0",      "60.0_200.0"};
    TString binRangeLow[N_BINS]  = {"0",      "15",      "30",      "60"};
    TString binRangeHigh[N_BINS] = {"15",      "30",      "60",      "1000"};
    TString binRangeLeg[N_BINS]  = {"0 < p_{T} < 15 GeV",      "15 < p_{T} < 30 GeV",      "30 < p_{T} < 60 GeV",      "60 < p_{T} < 200 GeV"};
    */

//    TString obsTag = "massZ2";
//    const TString sTemplateDirName = "templatesXS/DTreeXS_"+obsTag+"/13TeV/";
//    const int N_BINS = 4;
//    TString binRange[N_BINS]   = {"12_20",      "20_28",      "28_35",      "35_120"};
//    TString binRangeLow[N_BINS]  = {"12",      "20",      "28",      "35"};
//    TString binRangeHigh[N_BINS] = {"20",      "28",      "35",      "120"};
//    TString binRangeLeg[N_BINS]   = {"12 < m_{Z2} < 20 GeV",      "20 < m_{Z2} < 28 GeV",      "28 < m_{Z2} < 35 GeV",      "35 < m_{Z2} < 120 GeV"};

    TString obsTag = "njets_pt30_eta4p7";
    const TString sTemplateDirName = "templatesXS/DTreeXS_"+obsTag+"/13TeV/";
    const int N_BINS = 4;
    TString binRange[N_BINS]   = {"0.0_1.0",      "1.0_2.0",      "2.0_3.0",      "3.0_10.0"};
    TString binRangeLow[N_BINS]  = {"0",      "1",      "2",      "3"};
    TString binRangeHigh[N_BINS] = {"1",      "2",      "3",      "10"};
    TString binRangeLeg[N_BINS]   = {"N_{jets} = 0",      "N_{jets} = 1",      "N_{jets} = 2",      "N_{jets} >= 3"};

//    TString obsTag = "rapidity4l";
//    const TString sTemplateDirName = "templatesXS/DTreeXS_"+obsTag+"/13TeV/";
//    const int N_BINS = 4;
//    TString binRange[N_BINS]     = {"0_0.4",      "0.4_0.8",      "0.8_1.2",      "1.2_2.4"};
//    TString binRangeLow[N_BINS]  = {"0",      "0.4",      "0.8",      "1.2"};
//    TString binRangeHigh[N_BINS] = {"0.4",    "0.8",      "1.2",      "2.4"};
//    TString binRangeLeg[N_BINS]  = {"0 < |Y| < 0.4",      "0.4 < |Y| < 0.8",      "0.8 < |Y| < 1.2",      "1.2 < |Y| < 2.4"};

//    TString obsTag = "cosThetaStar";
//    const TString sTemplateDirName = "templatesXS/DTreeXS_"+obsTag+"/13TeV/";
//    const int N_BINS = 4;
//    TString binRange[N_BINS]     = {"0.0_0.25",      "0.25_0.5",      "0.5_0.75",      "0.75_1.0"};
//    TString binRangeLow[N_BINS]  = {"0",      "0.25",      "0.5",      "0.75"};
//    TString binRangeHigh[N_BINS] = {"0.25",    "0.5",      "0.75",      "1.0"};
//    TString binRangeLeg[N_BINS]  = {"0 < |cos#theta*| < 0.25",      "0.25 < |cos#theta*| < 0.5",      "0.5 < |cos#theta*| < 0.75",      "0.75 < |cos#theta*| < 1.0"};


    const int N_BKGS = 3;
    TString bkgName[N_BKGS]   = {"qqZZ",      "ggZZ",      "ZJetsCR"};

    TFile* fTemplateFile_2e2mu[N_BKGS][N_BINS];
    TFile* fTemplateFile_4mu[N_BKGS][N_BINS];
    TFile* fTemplateFile_4e[N_BKGS][N_BINS];
    TH1D* h1D_2e2mu[N_BKGS][N_BINS];
    TH1D* h1D_4mu[N_BKGS][N_BINS];
    TH1D* h1D_4e[N_BKGS][N_BINS];

    cout << "obsTag: " << obsTag << endl;
    for (int iBin = 0; iBin<N_BINS; iBin++ ) {
        for (int iBkg = 0; iBkg<N_BKGS; iBkg++ ) {
            if (bkgName[iBkg]!="ZJetsCR"){
                int nSmooth = 2;

                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_2e2mu_"+obsTag+"_"+binRange[iBin]+".root";
                fTemplateFile_2e2mu[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
                h1D_2e2mu[iBkg][iBin] = (TH1D*) fTemplateFile_2e2mu[iBkg][iBin]->Get("m4l_"+obsTag+"_"+binRange[iBin]);
                cout << "sTemplateDirName/sTemplateFileName: " << sTemplateDirName+"/"+sTemplateFileName << endl;
                cout << "h1D_2e2mu["<<bkgName[iBkg]<<"]["<<binRange[iBin]<<"]->GetEntries(): " << h1D_2e2mu[iBkg][iBin]->GetEntries() << endl;
                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_2e2mu[iBkg][iBin]);

                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_4mu_"+obsTag+"_"+binRange[iBin]+".root";
                fTemplateFile_4mu[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
                h1D_4mu[iBkg][iBin] = (TH1D*) fTemplateFile_4mu[iBkg][iBin]->Get("m4l_"+obsTag+"_"+binRange[iBin]);
                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_4mu[iBkg][iBin]);

                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_4e_"+obsTag+"_"+binRange[iBin]+".root";
                fTemplateFile_4e[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
                h1D_4e[iBkg][iBin] = (TH1D*) fTemplateFile_4e[iBkg][iBin]->Get("m4l_"+obsTag+"_"+binRange[iBin]);
                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_4e[iBkg][iBin]);
            } else {
                int nSmooth = 1;

                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans_"+obsTag+"_"+binRange[iBin]+".root";
                fTemplateFile_2e2mu[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
                h1D_2e2mu[iBkg][iBin] = (TH1D*) fTemplateFile_2e2mu[iBkg][iBin]->Get("m4l_"+obsTag+"_"+binRange[iBin]);
                cout << "sTemplateDirName/sTemplateFileName: " << sTemplateDirName+"/"+sTemplateFileName << endl;
                cout << "h1D_2e2mu["<<bkgName[iBkg]<<"]["<<binRange[iBin]<<"]->GetEntries(): " << h1D_2e2mu[iBkg][iBin]->GetEntries() << endl;
                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_2e2mu[iBkg][iBin]);

                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans_"+obsTag+"_"+binRange[iBin]+".root";
                fTemplateFile_4mu[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
                h1D_4mu[iBkg][iBin] = (TH1D*) fTemplateFile_4mu[iBkg][iBin]->Get("m4l_"+obsTag+"_"+binRange[iBin]);
                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_4mu[iBkg][iBin]);

                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans_"+obsTag+"_"+binRange[iBin]+".root";
                fTemplateFile_4e[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
                h1D_4e[iBkg][iBin] = (TH1D*) fTemplateFile_4e[iBkg][iBin]->Get("m4l_"+obsTag+"_"+binRange[iBin]);
                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_4e[iBkg][iBin]);

//                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans.root";
//                fTemplateFile_2e2mu[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//                h1D_2e2mu[iBkg][iBin] = new TH1D("m4l_"+obsTag+"_"+binRange[iBin], "m4l_"+obsTag+"_"+binRange[iBin], 20, 105.6, 140.6);
//                TTree* tempTree = (TTree*) fTemplateFile_2e2mu[iBkg][iBin]->Get("selectedEvents");
//                TString treeCut = "(("+binRangeLow[iBin]+" < "+obsTag+") && ("+obsTag+" < "+binRangeHigh[iBin]+"))";
//                tempTree->Draw("mass4l>>m4l_"+obsTag+"_"+binRange[iBin], treeCut, "goff");
//                cout << "sTemplateDirName/sTemplateFileName: " << sTemplateDirName+"/"+sTemplateFileName << endl;
//                cout << "h1D_2e2mu["<<bkgName[iBkg]<<"]["<<binRange[iBin]<<"]->GetEntries(): " << h1D_2e2mu[iBkg][iBin]->GetEntries() << endl;
//                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_2e2mu[iBkg][iBin]);
//
//                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans.root";
//                fTemplateFile_4mu[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//                h1D_4mu[iBkg][iBin] = new TH1D("m4l_"+obsTag+"_"+binRange[iBin], "m4l_"+obsTag+"_"+binRange[iBin], 20, 105.6, 140.6);
//                TTree* tempTree = (TTree*) fTemplateFile_4mu[iBkg][iBin]->Get("selectedEvents");
//                TString treeCut = "(("+binRangeLow[iBin]+" < "+obsTag+") && ("+obsTag+" < "+binRangeHigh[iBin]+"))";
//                tempTree->Draw("mass4l>>m4l_"+obsTag+"_"+binRange[iBin], treeCut, "goff");
//                cout << "sTemplateDirName/sTemplateFileName: " << sTemplateDirName+"/"+sTemplateFileName << endl;
//                cout << "h1D_4mu["<<bkgName[iBkg]<<"]["<<binRange[iBin]<<"]->GetEntries(): " << h1D_4mu[iBkg][iBin]->GetEntries() << endl;
//                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_4mu[iBkg][iBin]);
//
//                TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans.root";
//                fTemplateFile_4e[iBkg][iBin] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//                h1D_4e[iBkg][iBin] = new TH1D("m4l_"+obsTag+"_"+binRange[iBin], "m4l_"+obsTag+"_"+binRange[iBin], 20, 105.6, 140.6);
//                TTree* tempTree = (TTree*) fTemplateFile_4e[iBkg][iBin]->Get("selectedEvents");
//                TString treeCut = "(("+binRangeLow[iBin]+" < "+obsTag+") && ("+obsTag+" < "+binRangeHigh[iBin]+"))";
//                tempTree->Draw("mass4l>>m4l_"+obsTag+"_"+binRange[iBin], treeCut, "goff");
//                cout << "sTemplateDirName/sTemplateFileName: " << sTemplateDirName+"/"+sTemplateFileName << endl;
//                cout << "h1D_4e["<<bkgName[iBkg]<<"]["<<binRange[iBin]<<"]->GetEntries(): " << h1D_4e[iBkg][iBin]->GetEntries() << endl;
//                for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate1D(h1D_4e[iBkg][iBin]);

            } // if ZJetsCR
        } // iBkg<N_BKGS
    } // iBin<N_BINS

    // prepare dummy
    double var_plotHigh = 140.6, var_plotLow = 105.6;
    int var_nBins = 20;
    TString varAxLabel = "m_{4l} (GeV)";
    double binWidth = ((int) (100*(var_plotHigh - var_plotLow)/var_nBins))/100.;
    TString sUnit = (varAxLabel.Contains(" (GeV)"))?"(GeV)":" ";
    TString sBinWidth = TString::Format("%.1f",binWidth) + sUnit;
    TH1D* h1D_dummy = new TH1D("dummy", "dummy", var_nBins, var_plotLow, var_plotHigh);
    setHistProperties(h1D_dummy,1,1,kBlue-7,0,0,varAxLabel,"Events/"+sBinWidth);

    // common proeprties
    Width_t lineWidth = 2;
    double leg_xl = 0.60, leg_xr = 1.00, leg_yb = 0.65, leg_yt = 0.90;

    // plot hists
    int kBkg_qqZZ = 0, kBkg_ggZZ = 1, kBkg_ZJets = 2;
    c1->cd();
    for (int iBin = 0; iBin<N_BINS; iBin++ ) {
        /////// 2e2mu /////
        // qqZZZ + ggZZ //
        h1D_dummy->SetMaximum(2.0*h1D_2e2mu[kBkg_qqZZ][iBin]->GetMaximum());
        h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,binRangeLeg[iBin]+", 2e2#mu");
        setHistProperties(h1D_2e2mu[kBkg_qqZZ][iBin],lineWidth,1,kBlack); h1D_2e2mu[kBkg_qqZZ][iBin]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_qqZZ][iBin], "q#bar{q} #rightarrow ZZ","L");
        setHistProperties(h1D_2e2mu[kBkg_ggZZ][iBin],lineWidth,1,kBlue-7); h1D_2e2mu[kBkg_ggZZ][iBin]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_ggZZ][iBin], "gg #rightarrow ZZ","L");
        leg->Draw(); 
        c1->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+".pdf");
        c1->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+".png");
        // qqZZZ + Z+X //
        h1D_dummy->SetMaximum(2.0*h1D_2e2mu[kBkg_qqZZ][iBin]->GetMaximum());
        h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,binRangeLeg[iBin]+", 2e2#mu");
        setHistProperties(h1D_2e2mu[kBkg_qqZZ][iBin],lineWidth,1,kBlack); h1D_2e2mu[kBkg_qqZZ][iBin]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_qqZZ][iBin], "q#bar{q} #rightarrow ZZ","L");
        setHistProperties(h1D_2e2mu[kBkg_ZJets][iBin],lineWidth,1,kRed-7); h1D_2e2mu[kBkg_ZJets][iBin]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_ZJets][iBin], "Z + X","L");
        leg->Draw(); 
        c1->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ZJets]+".pdf");
        c1->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ZJets]+".png");

        /////// 4mu /////
        // qqZZZ + ggZZ //
        h1D_dummy->SetMaximum(2.0*h1D_4mu[kBkg_qqZZ][iBin]->GetMaximum());
        h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,binRangeLeg[iBin]+", 4#mu");
        setHistProperties(h1D_4mu[kBkg_qqZZ][iBin],lineWidth,1,kBlack); h1D_4mu[kBkg_qqZZ][iBin]->Draw("same"); leg->AddEntry(h1D_4mu[kBkg_qqZZ][iBin], "q#bar{q} #rightarrow ZZ","L");
        setHistProperties(h1D_4mu[kBkg_ggZZ][iBin],lineWidth,1,kBlue-7); h1D_4mu[kBkg_ggZZ][iBin]->Draw("same"); leg->AddEntry(h1D_4mu[kBkg_ggZZ][iBin], "gg #rightarrow ZZ","L");
        leg->Draw(); 
        c1->SaveAs(sPlotsStore+"/XSTemplates_4mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+".pdf");
        c1->SaveAs(sPlotsStore+"/XSTemplates_4mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+".png");

        // qqZZZ + Z+X //
        h1D_dummy->SetMaximum(2.0*h1D_4mu[kBkg_qqZZ][iBin]->GetMaximum());
        h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,binRangeLeg[iBin]+", 4#mu");
        setHistProperties(h1D_4mu[kBkg_qqZZ][iBin],lineWidth,1,kBlack); h1D_4mu[kBkg_qqZZ][iBin]->Draw("same"); leg->AddEntry(h1D_4mu[kBkg_qqZZ][iBin], "q#bar{q} #rightarrow ZZ","L");
        setHistProperties(h1D_4mu[kBkg_ZJets][iBin],lineWidth,1,kRed-7); h1D_4mu[kBkg_ZJets][iBin]->Draw("same"); leg->AddEntry(h1D_4mu[kBkg_ZJets][iBin], "Z + X","L");
        leg->Draw(); 
        c1->SaveAs(sPlotsStore+"/XSTemplates_4mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ZJets]+".pdf");
        c1->SaveAs(sPlotsStore+"/XSTemplates_4mu_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ZJets]+".png");

        /////// 4e /////
        // qqZZZ + ggZZ //
        h1D_dummy->SetMaximum(2.0*h1D_4e[kBkg_qqZZ][iBin]->GetMaximum());
        h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,binRangeLeg[iBin]+", 4e");
        setHistProperties(h1D_4e[kBkg_qqZZ][iBin],lineWidth,1,kBlack); h1D_4e[kBkg_qqZZ][iBin]->Draw("same"); leg->AddEntry(h1D_4e[kBkg_qqZZ][iBin], "q#bar{q} #rightarrow ZZ","L");
        setHistProperties(h1D_4e[kBkg_ggZZ][iBin],lineWidth,1,kBlue-7); h1D_4e[kBkg_ggZZ][iBin]->Draw("same"); leg->AddEntry(h1D_4e[kBkg_ggZZ][iBin], "gg #rightarrow ZZ","L");
        leg->Draw(); 
        c1->SaveAs(sPlotsStore+"/XSTemplates_4e_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+".pdf");
        c1->SaveAs(sPlotsStore+"/XSTemplates_4e_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ggZZ]+".png");

        // qqZZZ + Z+X //
        h1D_dummy->SetMaximum(2.0*h1D_4e[kBkg_qqZZ][iBin]->GetMaximum());
        h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,binRangeLeg[iBin]+", 4e");
        setHistProperties(h1D_4e[kBkg_qqZZ][iBin],lineWidth,1,kBlack); h1D_4e[kBkg_qqZZ][iBin]->Draw("same"); leg->AddEntry(h1D_4e[kBkg_qqZZ][iBin], "q#bar{q} #rightarrow ZZ","L");
        setHistProperties(h1D_4e[kBkg_ZJets][iBin],lineWidth,1,kRed-7); h1D_4e[kBkg_ZJets][iBin]->Draw("same"); leg->AddEntry(h1D_4e[kBkg_ZJets][iBin], "Z + X","L");
        leg->Draw(); 
        c1->SaveAs(sPlotsStore+"/XSTemplates_4e_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ZJets]+".pdf");
        c1->SaveAs(sPlotsStore+"/XSTemplates_4e_"+obsTag+"_"+binRange[iBin]+"_"+bkgName[kBkg_qqZZ]+"_"+bkgName[kBkg_ZJets]+".png");

    } // iBin<N_BINS

    // Z+X for all the bins
    h1D_dummy->SetMaximum(2.0*h1D_2e2mu[kBkg_ZJets][0]->GetMaximum());
    h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"all final states");
    setHistProperties(h1D_2e2mu[kBkg_ZJets][0],lineWidth,1,kRed-7); h1D_2e2mu[kBkg_ZJets][0]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_ZJets][0], "Z + X, 0","L");
    setHistProperties(h1D_2e2mu[kBkg_ZJets][1],lineWidth,2,kRed-7); h1D_2e2mu[kBkg_ZJets][1]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_ZJets][1], "Z + X, 1","L");
    setHistProperties(h1D_2e2mu[kBkg_ZJets][2],lineWidth,3,kRed-7); h1D_2e2mu[kBkg_ZJets][2]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_ZJets][2], "Z + X, 2","L");
    setHistProperties(h1D_2e2mu[kBkg_ZJets][3],lineWidth,4,kRed-7); h1D_2e2mu[kBkg_ZJets][3]->Draw("same"); leg->AddEntry(h1D_2e2mu[kBkg_ZJets][3], "Z + X, 3","L");
    TH1D* hSum = (TH1D*) h1D_2e2mu[kBkg_ZJets][0]->Clone(); hSum->Add(h1D_2e2mu[kBkg_ZJets][1]); hSum->Add(h1D_2e2mu[kBkg_ZJets][2]); hSum->Add(h1D_2e2mu[kBkg_ZJets][3]);
    normaliseHist1D(hSum);
    setHistProperties(hSum,lineWidth,1,kBlack); hSum->Draw("same"); leg->AddEntry(hSum, "Z + X, all","L");
    leg->Draw(); 
    c1->SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_ZJets]+"_allBins.pdf");
    c1->SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_ZJets]+"_allBins.png");

    // qqZZ for all the bins
    h1D_dummy->SetMaximum(2.0*h1D_2e2mu[kBkg_qqZZ][0]->GetMaximum());
    h1D_dummy->Draw(); cmsPreliminary(c1); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"q#bar{q} #rightarrow ZZ");
    TH1D* hSum_2e2mu = (TH1D*) h1D_2e2mu[kBkg_qqZZ][0]->Clone(); hSum->Add(h1D_2e2mu[kBkg_qqZZ][1]); hSum->Add(h1D_2e2mu[kBkg_qqZZ][2]); hSum->Add(h1D_2e2mu[kBkg_qqZZ][3]);
    TH1D* hSum_4mu = (TH1D*) h1D_4mu[kBkg_qqZZ][0]->Clone(); hSum->Add(h1D_4mu[kBkg_qqZZ][1]); hSum->Add(h1D_4mu[kBkg_qqZZ][2]); hSum->Add(h1D_4mu[kBkg_qqZZ][3]);
    TH1D* hSum_4e = (TH1D*) h1D_4e[kBkg_qqZZ][0]->Clone(); hSum->Add(h1D_4e[kBkg_qqZZ][1]); hSum->Add(h1D_4e[kBkg_qqZZ][2]); hSum->Add(h1D_4e[kBkg_qqZZ][3]);
    setHistProperties(hSum_2e2mu,lineWidth,1,kRed-7); hSum_2e2mu->Draw("same"); leg->AddEntry(hSum_2e2mu, "2e2#mu, all bins","L");normaliseHist1D(hSum_2e2mu);
    setHistProperties(hSum_4mu,lineWidth,2,kGreen-7); hSum_4mu->Draw("same"); leg->AddEntry(hSum_4mu, "4#mu, all bins","L");normaliseHist1D(hSum_4mu);
    setHistProperties(hSum_4e,lineWidth,3,kBlue-7); hSum_4e->Draw("same"); leg->AddEntry(hSum_4e, "4e, all bins","L");normaliseHist1D(hSum_4e);
    leg->Draw(); 
    c1->SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_qqZZ]+"_allBins.pdf");
    c1->SaveAs(sPlotsStore+"/XSTemplates_AllChans_"+obsTag+"_"+bkgName[kBkg_qqZZ]+"_allBins.png");

    // 2D plots
//    TCanvas *c2;
//    setCavasAndStyles("c2",c2,"",0.15,0.15,0.15,0.05);
//
//    TFile* fTemplFile_2e2mu[N_BKGS];
//    TFile* fTemplFile_4mu[N_BKGS];
//    TFile* fTemplFile_4e[N_BKGS];
//    TH2D* h2D_2e2mu[N_BKGS];
//    TH2D* h2D_4mu[N_BKGS];
//    TH2D* h2D_4e[N_BKGS];
//
//    for (int iBkg = 0; iBkg<N_BKGS; iBkg++ ) {
//        if (bkgName[iBkg]!="ZJetsCR"){
//            int nSmooth = 1;
//
//            TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_2e2mu.root";
//            fTemplFile_2e2mu[iBkg] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//            h2D_2e2mu[iBkg] = (TH2D*) fTemplFile_2e2mu[iBkg]->Get("h2D_m4l_"+obsTag);
//            for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate2D(h2D_2e2mu[iBkg]);
//
//            TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_4mu.root";
//            fTemplFile_4mu[iBkg] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//            h2D_4mu[iBkg] = (TH2D*) fTemplFile_4mu[iBkg]->Get("h2D_m4l_"+obsTag);
//            for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate2D(h2D_4mu[iBkg]);
//
//            TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_4e.root";
//            fTemplFile_4e[iBkg] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//            h2D_4e[iBkg] = (TH2D*) fTemplFile_4e[iBkg]->Get("h2D_m4l_"+obsTag);
//            for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate2D(h2D_4e[iBkg]);
//        } else {
//            int nSmooth = 1;
//
//            TString sTemplateFileName = "XSBackground_"+bkgName[iBkg]+"_AllChans.root";
//            fTemplFile_2e2mu[iBkg] = new TFile(sTemplateDirName+"/"+sTemplateFileName, "READ");
//            h2D_2e2mu[iBkg] = (TH2D*) fTemplFile_2e2mu[iBkg]->Get("h2D_m4l_"+obsTag);
//            for (int k = 0; k < nSmooth; k++) smoothAndNormaliseTemplate2D(h2D_2e2mu[iBkg]);
//
//        } // if ZJetsCR
//    } // iBkg<N_BKGS
//
//    double leg_xl = 0.50, leg_xr = 0.90, leg_yb = 0.65, leg_yt = 0.90;
//
////    TH2D* h2D_dummy = new TH2D("dummy2D", "dummy2D", var_nBins, var_plotLow, var_plotHigh, var_nBins, 0, 120);
////    setHistProperties2D(h2D_dummy,varAxLabel,"p_{T}^{H} (GeV)");
//    TH2D* h2D_dummy = new TH2D("dummy2D", "dummy2D", var_nBins, var_plotLow, var_plotHigh, var_nBins, 12, 120);
//    setHistProperties2D(h2D_dummy,varAxLabel,"m_{Z2} (GeV)");
//
//    c2->cd(0);
//    // Z+X //
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"Z + X, all chan.");
//    setHistProperties2D(h2D_2e2mu[kBkg_ZJets]); h2D_2e2mu[kBkg_ZJets]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_m4l_vs_"+obsTag+"_"+bkgName[kBkg_ZJets]+".pdf");
//    // qqZZ //
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"q#bar{q} #rightarrow ZZ, 2e2#mu");
//    setHistProperties2D(h2D_2e2mu[kBkg_qqZZ]); h2D_2e2mu[kBkg_qqZZ]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_m4l_vs_"+obsTag+"_"+bkgName[kBkg_qqZZ]+".pdf");
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"q#bar{q} #rightarrow ZZ, 4#mu");
//    setHistProperties2D(h2D_4mu[kBkg_qqZZ]); h2D_4mu[kBkg_qqZZ]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_4mu_m4l_vs_"+obsTag+"_"+bkgName[kBkg_qqZZ]+".pdf");
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"q#bar{q} #rightarrow ZZ, 4e");
//    setHistProperties2D(h2D_4e[kBkg_qqZZ]); h2D_4e[kBkg_qqZZ]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_4e_m4l_vs_"+obsTag+"_"+bkgName[kBkg_qqZZ]+".pdf");
//    // ggZZ //
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"gg #rightarrow ZZ, 2e2#mu");
//    setHistProperties2D(h2D_2e2mu[kBkg_ggZZ]); h2D_2e2mu[kBkg_ggZZ]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_2e2mu_m4l_vs_"+obsTag+"_"+bkgName[kBkg_ggZZ]+".pdf");
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"gg #rightarrow ZZ, 4#mu");
//    setHistProperties2D(h2D_4mu[kBkg_ggZZ]); h2D_4mu[kBkg_ggZZ]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_4mu_m4l_vs_"+obsTag+"_"+bkgName[kBkg_ggZZ]+".pdf");
//    h2D_dummy->Draw(); cmsPreliminary(c2); TLegend* leg = new TLegend(leg_xl,leg_yb,leg_xr,leg_yt); setLegendProperties(leg,"gg #rightarrow ZZ, 4e");
//    setHistProperties2D(h2D_4e[kBkg_ggZZ]); h2D_4e[kBkg_ggZZ]->Draw("colz same");
//    leg->Draw(); c2->SaveAs(sPlotsStore+"/XSTemplates_4e_m4l_vs_"+obsTag+"_"+bkgName[kBkg_ggZZ]+".pdf");

}

