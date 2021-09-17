//-----------------------------------
// contact: Predrag.Milenovic@cern.ch
// last update: 2014.05.02
//-----------------------------------

// ROOT include
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TH1D.h>
#include "TH2.h"
#include "TChain.h"
#include <TStyle.h>
#include <TString.h>
#include <TMath.h>
#include <TROOT.h>
#include "TRandom.h"
#include "TGraphAsymmErrors.h"
#include "TObjArray.h"

// C include
#include <iostream>
#include <iomanip>
#include <cmath>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <stdio.h>

using namespace std;

//--------------Global definitions---------------//
// default cuts
const double CUT_ELPT = 7.;
const double CUT_MUPT = 5.;
const double CUT_ELETA = 2.5;
const double CUT_MUETA = 2.4;
const double CUT_MZ1LOW = 40.;
const double CUT_MZ1HIGH = 120.;
const double CUT_MZ2LOW = 12.;
const double CUT_MZ2HIGH = 120.;
double CUT_M4LLOW = 105;
double CUT_M4LHIGH = 140;
const double CUT_M4LLOW_FULL = 0.;
const double CUT_M4LHIGH_FULL = 1000.;
// directory names
TString templatesDir = "templatesXS";
// print out settings
int printOutWidth = 12;
int printOutPrecision = 3;
const int SILENT = true;
const int NEVT_PRINTOUT = 100000;
const int SORT_EVENTS = false;
// fake rate files and hists
//const TString fakeRatesEl = "fakeRates_el.root";
const TString fakeRatesEl = "Hist_Data_ptl3_WZremoved.root";  //2018 Lucien
//const TString fakeRatesEl = "fakeRates_el.root";  //2016 
//const TString h1Name_FRel_EB = "h1D_FRel_EB";
const TString h1Name_FRel_EB = "Data_FRel_EB";
//const TString h1Name_FRel_EE = "h1D_FRel_EE";
const TString h1Name_FRel_EE = "Data_FRel_EE";
const TString fakeRatesMu = "Hist_Data_ptl3_WZremoved.root";
//const TString fakeRatesMu = "fakeRates_mu.root";
//const TString h1Name_FRmu_EB = "h1D_FRmu_EB";
const TString h1Name_FRmu_EB = "Data_FRmu_EB";
//const TString h1Name_FRmu_EE = "h1D_FRmu_EE";
const TString h1Name_FRmu_EE = "Data_FRmu_EE";
//TH1D *h1DFRelEB, *h1DFRelEE, *h1DFRmuEB, *h1DFRmuEE;
TH1D *h1DFRelEB, *h1DFRelEE, *h1DFRmuEB, *h1DFRmuEE;
// k-factor files and graphs
const TString kFactorFileName = "HZZ4l-KDFactorGraph.root";
const TString grName_kFactor= "KDScale_AllFlavors";
TGraphAsymmErrors  *gr_kFactor;
// others
TRandom *pRnd = new TRandom();
const unsigned int outNwidth = 16;
TString PROCESSING_TYPE = "XSTree";// "XSTreeZ4l"

void templatesXS(TString processNameTag, TString processFileName, TString sqrtsTag, TString sfinalState,
                 TString obsName, TString obsBinDn, TString obsBinUp, TString fitTypeZ4l, bool useRefit);

int getTemplateXS(TString processNameTag, TString processFileName, TString sqrtsTag, TString sfinalState,
                  TString obsName, TString obsBinDn, TString obsBinUp, TString fitTypeZ4l, bool useRefit,
                  double elpT = CUT_ELPT, double mupT = CUT_MUPT, double mZ2_low = CUT_MZ2LOW, 
                  double mZ1_low = CUT_MZ1LOW, double m4l_low = CUT_M4LLOW, double m4l_high = CUT_M4LHIGH);

double getFakeRateWeight(TString lepMode = "el", TString etaRegion = "EB", double pT = 10.);
//double kdWithPDFm4l(double KD, double pdfSigM4l, double pdfBkgM4l);
TString getTemplateNameTag(TString processNameTag);
void loadFakeRateHists();
TString strRandom(unsigned int rndmMax = 100000);
void smoothAndNormaliseTemplate(TH2D* &h2D, bool silent = true);
void smoothAndNormaliseTemplate1D(TH1D* &h1D, double norm = 1.);
void storeTreeAndTemplatesXS(TTree* TT, TString obsName, TString obsBinDn, TString obsBinUp, TString sfinalState, TString fLocation, TString templateNameTag, TString fOption, TString fitTypeZ4l, bool useRefit);
int normaliseHist(TH2D* &h2D, double norm = 1.);
int normaliseHist(TH1D* &h1D, double norm = 1.);
int fillEmptyBinsHist2D(TH2D* &h2D, double floor = .00001);
int fillEmptyBinsHist1D(TH1D* &h1D, double floor = .00001);
void loadKFactorGraphs();
double getGluGluZZKFactor(double m4l);
// proposed variable template binning
int nbinsX=35; const int nbinsY=35;

double nEvents = -1;

//==============================================================================================================================================



//_______________________________________________________________________________________________________________________________________________
void fiducialXSTemplates(TString processNameTag = "qqZZ", TString processFileName = "ZZTo2e2mu_mZZ95-160.root", TString sfinalState = "4l", TString obsName = "massZ2", TString obsBinDn = "0", TString obsBinUp = "120", TString sqrtsTag = "8TeV", TString baseDirXS = "templatesXS", TString sProcessingType = "DTreeXS", TString fitTypeZ4l = "none", bool useRefit = false){
    // prepare XS templates for given parameters
    PROCESSING_TYPE = sProcessingType;
    templatesDir = baseDirXS;
    if (fitTypeZ4l=="doZ4l") {
        CUT_M4LLOW = 50;
        CUT_M4LHIGH = 105;
    }
    else if (fitTypeZ4l=="doRatio") {
        CUT_M4LLOW = 50;
        CUT_M4LHIGH = 140;
        nbinsX=45;
    }
    else if (fitTypeZ4l=="doHighMass") {
        CUT_M4LLOW = 105;
        CUT_M4LHIGH = 885;
        nbinsX=390;
    }
    
    if (obsName!="mass4l") {
        nbinsX=15;
    }
    cout<<"Begin templatesXS"<<endl;
    templatesXS(processNameTag, processFileName, sqrtsTag, sfinalState, obsName, obsBinDn, obsBinUp, fitTypeZ4l, useRefit);
}

//_______________________________________________________________________________________________________________________________________________
void analysisInit() {
    gErrorIgnoreLevel = kWarning;
    gErrorIgnoreLevel = kError;
}

//_______________________________________________________________________________________________________________________________________________
void templatesXS(TString processNameTag, TString processFileName, TString sqrtsTag, TString sfinalState,
                 TString obsName, TString obsBinDn, TString obsBinUp, TString fitTypeZ4l, bool useRefit) {

    analysisInit();

    useRefit = false;

    // produce XS 2D templates (uniform binning)
    cout << "[preparing 2D XS templates, process: "+processNameTag+", sqrts: "+sqrtsTag+", fstate: "<<sfinalState<<"]" << "["<<PROCESSING_TYPE<<"]" << "["<<CUT_M4LLOW<<" < m4l < "<<CUT_M4LHIGH<<"]" << endl;
    cout<<"fitType: "<<fitTypeZ4l<<" templatesXS using refit? "<<useRefit<<endl;

    if (sfinalState == "4l") {
        getTemplateXS(processNameTag, processFileName, sqrtsTag, "2e2mu", obsName, obsBinDn, obsBinUp, fitTypeZ4l, useRefit);
        getTemplateXS(processNameTag, processFileName, sqrtsTag, "4e", obsName, obsBinDn, obsBinUp, fitTypeZ4l, useRefit);
        getTemplateXS(processNameTag, processFileName, sqrtsTag, "4mu", obsName, obsBinDn, obsBinUp, fitTypeZ4l, useRefit);
    } else {                            
        getTemplateXS(processNameTag, processFileName, sqrtsTag, sfinalState, obsName, obsBinDn, obsBinUp, fitTypeZ4l, useRefit);
    }
}

//_______________________________________________________________________________________________________________________________________________
int getHistTreesXS(TChain* tree, TString processNameTag, TString sqrtsTag, TTree* TT,
                   TH2D* &h2D_m4l_mZ2, TH2D* &h2D_m4l_pT4l, TH2D* &h2D_m4l_eta4l, TH2D* &h2D_m4l_nJets,
                   int iFinState, double ptElCut, double ptMuCut, double mZ2Cut, double mZ1Cut, double m4l_low, double m4l_high, bool useRefit=false, bool scale = false){
    // define vars
    int idL1, idL2, idL3, idL4;
    float pTL1, pTL2, pTL3, pTL4;
    float etaL1, etaL2, etaL3, etaL4;
    float mass4l, pT4l, eta4l, massZ1, massZ2;
    int njets_pt30_eta4p7=0, njets_pt30_eta4p7_jesdn=0, njets_pt30_eta4p7_jesup=0;
    int njets_pt30_eta2p5=0, njets_pt30_eta2p5_jesdn=0, njets_pt30_eta2p5_jesup=0;
    int finalState;
    float eventWeight, genWeight, crossSection, dataMCWeight;
    double etaElCut = CUT_ELETA;
    double etaMuCut = CUT_MUETA;
    long int Run, LumiSect, Event;
    bool passedFullSelection, passedZ4lSelection, passedZXCRSelection;
    int nZXCRFailedLeptons;
    float pTZ1, pTZ2;
    float rapidity4l=0.0;
    float cosThetaStar, cosTheta1, cosTheta2, Phi, Phi1;
    float k_qqZZ_qcd_M, k_qqZZ_ewk, k_ggZZ;
    float pt_leadingjet_pt30_eta4p7, pt_leadingjet_pt30_eta4p7_jesdn, pt_leadingjet_pt30_eta4p7_jesup;
    float pt_leadingjet_pt30_eta2p5, pt_leadingjet_pt30_eta2p5_jesdn, pt_leadingjet_pt30_eta2p5_jesup;

    // load ggZZ k-graphs
    loadKFactorGraphs();

    // get branches
    tree->SetBranchAddress("Run",&Run);
    tree->SetBranchAddress("LumiSect",&LumiSect);
    tree->SetBranchAddress("Event",&Event);
    tree->SetBranchAddress("eventWeight",&eventWeight);
    tree->SetBranchAddress("genWeight",&genWeight);
    tree->SetBranchAddress("k_qqZZ_qcd_M",&k_qqZZ_qcd_M);
    tree->SetBranchAddress("k_qqZZ_ewk",&k_qqZZ_ewk);
    tree->SetBranchAddress("k_ggZZ",&k_ggZZ);
    tree->SetBranchAddress("crossSection",&crossSection);
    if (tree->GetBranch("dataMCWeight")) {tree->SetBranchAddress("dataMCWeight",&dataMCWeight);}
    tree->SetBranchAddress("passedFullSelection",&passedFullSelection);
    tree->SetBranchAddress("passedZ4lSelection",&passedZ4lSelection);
    tree->SetBranchAddress("passedZXCRSelection",&passedZXCRSelection);
    tree->SetBranchAddress("nZXCRFailedLeptons",&nZXCRFailedLeptons);
    tree->SetBranchAddress("finalState",&finalState);
    tree->SetBranchAddress("idL1",&idL1);
    tree->SetBranchAddress("idL2",&idL2);
    tree->SetBranchAddress("idL3",&idL3);
    tree->SetBranchAddress("idL4",&idL4);
    tree->SetBranchAddress("pTL1",&pTL1);
    tree->SetBranchAddress("pTL2",&pTL2);
    tree->SetBranchAddress("pTL3",&pTL3);
    tree->SetBranchAddress("pTL4",&pTL4);
    tree->SetBranchAddress("etaL1",&etaL1);
    tree->SetBranchAddress("etaL2",&etaL2);
    tree->SetBranchAddress("etaL3",&etaL3);
    tree->SetBranchAddress("etaL4",&etaL4);
    if (useRefit) {tree->SetBranchAddress("mass4lREFIT",&mass4l);}
    else {tree->SetBranchAddress("mass4l",&mass4l);}
    tree->SetBranchAddress("pT4l",&pT4l);
    tree->SetBranchAddress("eta4l",&eta4l);
    if (tree->GetBranch("njets_pt30_eta4p7")) {tree->SetBranchAddress("njets_pt30_eta4p7",&njets_pt30_eta4p7);}
    if (tree->GetBranch("njets_pt30_eta4p7_jesdn")) {tree->SetBranchAddress("njets_pt30_eta4p7_jesdn",&njets_pt30_eta4p7_jesdn);}
    if (tree->GetBranch("njets_pt30_eta4p7_jesup")) {tree->SetBranchAddress("njets_pt30_eta4p7_jesup",&njets_pt30_eta4p7_jesup);}
    if (tree->GetBranch("njets_pt30_eta2p5")) {tree->SetBranchAddress("njets_pt30_eta2p5",&njets_pt30_eta2p5);}
    if (tree->GetBranch("njets_pt30_eta2p5_jesdn")) {tree->SetBranchAddress("njets_pt30_eta2p5_jesdn",&njets_pt30_eta2p5_jesdn);}
    if (tree->GetBranch("njets_pt30_eta2p5_jesup")) {tree->SetBranchAddress("njets_pt30_eta2p5_jesup",&njets_pt30_eta2p5_jesup);}
    if (tree->GetBranch("cosThetaStar")) {tree->SetBranchAddress("cosThetaStar",&cosThetaStar);}
    if (tree->GetBranch("cosTheta1")) {tree->SetBranchAddress("cosTheta1",&cosTheta1);}
    if (tree->GetBranch("cosTheta2")) {tree->SetBranchAddress("cosTheta2",&cosTheta2);}
    if (tree->GetBranch("Phi")) {tree->SetBranchAddress("Phi",&Phi);}
    if (tree->GetBranch("Phi1")) {tree->SetBranchAddress("Phi1",&Phi1);}
    if (tree->GetBranch("rapidity4l")) {tree->SetBranchAddress("rapidity4l",&rapidity4l);}
    if (tree->GetBranch("y4l")) {tree->SetBranchAddress("y4l",&rapidity4l);}
    tree->SetBranchAddress("massZ1",&massZ1);
    tree->SetBranchAddress("massZ2",&massZ2);
    tree->SetBranchAddress("pTZ1",&pTZ1);
    tree->SetBranchAddress("pTZ2",&pTZ2);
    if (tree->GetBranch("pt_leadingjet_pt30_eta4p7")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta4p7",&pt_leadingjet_pt30_eta4p7);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta4p7_jesup")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta4p7_jesup",&pt_leadingjet_pt30_eta4p7_jesup);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta4p7_jesdn")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta4p7_jesdn",&pt_leadingjet_pt30_eta4p7_jesdn);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta2p5")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta2p5",&pt_leadingjet_pt30_eta2p5);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta2p5_jesup")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta2p5_jesup",&pt_leadingjet_pt30_eta2p5_jesup);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta2p5_jesdn")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta2p5_jesdn",&pt_leadingjet_pt30_eta2p5_jesdn);}


    // prepare tree for a set of discriminants and variables (for templates)
    float selectedWeight; 
    float kfactor_ggZZ; //, Dbkg;
    float kfactor_qqZZ; 
    // info
    TT->Branch("Run",&Run,"Run/l");
    TT->Branch("LumiSect",&LumiSect,"LumiSect/l");
    TT->Branch("Event",&Event,"Event/l");
    TT->Branch("weight",&selectedWeight,"weight/F");
    if (useRefit) { TT->Branch("mass4lREFIT",&mass4l,"mass4lREFIT/F");}
    else { TT->Branch("mass4l",&mass4l,"mass4l/F");}
    TT->Branch("pT4l",&pT4l,"pT4l/F");
    TT->Branch("eta4l",&eta4l,"eta4l/F");
    TT->Branch("rapidity4l",&rapidity4l,"rapidity4l/F");
    TT->Branch("njets_pt30_eta4p7",&njets_pt30_eta4p7,"njets_pt30_eta4p7/I");
    TT->Branch("njets_pt30_eta4p7_jesup",&njets_pt30_eta4p7_jesup,"njets_pt30_eta4p7_jesup/I");
    TT->Branch("njets_pt30_eta4p7_jesdn",&njets_pt30_eta4p7_jesdn,"njets_pt30_eta4p7_jesdn/I");
    TT->Branch("njets_pt30_eta2p5",&njets_pt30_eta2p5,"njets_pt30_eta2p5/I");
    TT->Branch("njets_pt30_eta2p5_jesup",&njets_pt30_eta2p5_jesup,"njets_pt30_eta2p5_jesup/I");
    TT->Branch("njets_pt30_eta2p5_jesdn",&njets_pt30_eta2p5_jesdn,"njets_pt30_eta2p5_jesdn/I");
    TT->Branch("massZ1",&massZ1,"massZ1/F");
    TT->Branch("massZ2",&massZ2,"massZ2/F");
    TT->Branch("pTZ1",&pTZ1,"pTZ1/F");
    TT->Branch("pTZ2",&pTZ2,"pTZ2/F");
    TT->Branch("cosThetaStar",&cosThetaStar,"cosThetaStar/F");
    TT->Branch("cosTheta1",&cosTheta1,"cosTheta1/F");
    TT->Branch("cosTheta2",&cosTheta2,"cosTheta2/F");
    TT->Branch("Phi",&Phi,"Phi/F");
    TT->Branch("Phi1",&Phi1,"Phi1/F");
    TT->Branch("pt_leadingjet_pt30_eta4p7",&pt_leadingjet_pt30_eta4p7,"pt_leadingjet_pt30_eta4p7/F");
    TT->Branch("pt_leadingjet_pt30_eta4p7_jesup",&pt_leadingjet_pt30_eta4p7_jesup,"pt_leadingjet_pt30_eta4p7_jesup/F");
    TT->Branch("pt_leadingjet_pt30_eta4p7_jesdn",&pt_leadingjet_pt30_eta4p7_jesdn,"pt_leadingjet_pt30_eta4p7_jesdn/F");
    TT->Branch("pt_leadingjet_pt30_eta2p5",&pt_leadingjet_pt30_eta2p5,"pt_leadingjet_pt30_eta2p5/F");
    TT->Branch("pt_leadingjet_pt30_eta2p5_jesup",&pt_leadingjet_pt30_eta2p5_jesup,"pt_leadingjet_pt30_eta2p5_jesup/F");
    TT->Branch("pt_leadingjet_pt30_eta2p5_jesdn",&pt_leadingjet_pt30_eta2p5_jesdn,"pt_leadingjet_pt30_eta2p5_jesdn/F");
    TT->Branch("kfactor_ggZZ",&kfactor_ggZZ,"kfactor_ggZZ/F");
    TT->Branch("kfactor_qqZZ",&kfactor_qqZZ,"kfactor_qqZZ/F");

    // counters
    int nEvtMassWindow = 0;
    // fill histograms
    Long64_t nentries = tree->GetEntries();
//    nentries = 1000;
    if(!SILENT) {
        cout << setw(printOutWidth) << "nEntries: " << nentries << setw(printOutWidth) << "iFinState: " << iFinState << endl;
        cout << "Event" << ":" << "Run" << ":" << "LumiSect" << ":" << "mass4l" << ":" << "massZ1" << ":" << "massZ2" << ":" <<
            "weight" << ":" << "kd_ALT" << ":" << "superKD" << ":" << "pdfSigM4l" << ":" << "pdfBkgM4l" << endl;
    }
    // sort tree in "Event" number, ascending
	int *index = new int[nentries];
    if (SORT_EVENTS) {
        tree->Draw("Event","","goff");
        int nentries_int = static_cast<int>(nentries);
        TMath::Sort(nentries_int, tree->GetV1(), index, false);
    }
    for(int iEvt=0; iEvt < nentries; iEvt++){
        if (SORT_EVENTS)
            tree->GetEntry(index[iEvt]);	//index[iEvt]);}// take sorted entries
        else
            {tree->GetEntry(iEvt);}// take unsroted entries

        // print out
        if(iEvt%50000==0) cout << "   event: " << iEvt << "/" << nentries << endl;
//        if(iEvt%5000==0) cout << "   event: " << iEvt << "/" << nentries << endl;

        // weight
        if (dataMCWeight==0) dataMCWeight = 1;
        float weight = (scale)? genWeight*crossSection*dataMCWeight: 1.;
        if (processNameTag == "qqZZ") {
            weight *= k_qqZZ_qcd_M*k_qqZZ_ewk;
        }
        if (processNameTag == "ggZZ") {
            weight *= k_ggZZ;
        }

        // selection for irr. bkg.
        if (!passedZ4lSelection && (processNameTag != "ZJetsCR")) continue;
        // selection for red. bkg.
        if (!(passedZXCRSelection && nZXCRFailedLeptons==2) && (processNameTag == "ZJetsCR")) continue;

        if (finalState!=iFinState && !(finalState==4 && iFinState==3) && iFinState!=5) continue; // iFinState = 3 for final states 2e2mu and 2mu2e; iFinState = 5 for all final states together

        // for the predefined mass window only
        if ((PROCESSING_TYPE!="XSTreeZ4l")&&(CUT_M4LLOW > mass4l || mass4l > CUT_M4LHIGH)) continue;

        // in case of Z+X temaplte include fake rate factors
        double fr4, fr3;
        if (iFinState==5) {
            // fake rate factor for L4
            if ((abs(idL4) == 11) && (abs(etaL4) < 1.47)) fr4 = getFakeRateWeight("el", "EB", pTL4);
            if ((abs(idL4) == 11) && (abs(etaL4) > 1.47)) fr4 = getFakeRateWeight("el", "EE", pTL4);
            if ((abs(idL4) == 13) && (abs(etaL4) < 1.47)) fr4 = getFakeRateWeight("mu", "EB", pTL4);
            if ((abs(idL4) == 13) && (abs(etaL4) > 1.47)) fr4 = getFakeRateWeight("mu", "EE", pTL4);
            // fake rate factor for L3
            if ((abs(idL3) == 11) && (abs(etaL3) < 1.47)) fr3 = getFakeRateWeight("el", "EB", pTL3);
            if ((abs(idL3) == 11) && (abs(etaL3) > 1.47)) fr3 = getFakeRateWeight("el", "EE", pTL3);
            if ((abs(idL3) == 13) && (abs(etaL3) < 1.47)) fr3 = getFakeRateWeight("mu", "EB", pTL3);
            if ((abs(idL3) == 13) && (abs(etaL3) > 1.47)) fr3 = getFakeRateWeight("mu", "EE", pTL3);
            // include in weigth, if good values
            if (idL1 + idL2 + idL3 + idL4 != 0) continue;
            if (0. >= fr3 || fr3 >= 1.) continue;
            if (0. >= fr4 || fr4 >= 1.) continue;
            // test-only
            // weight = weight * fr3 * fr4;
        }

        nEvtMassWindow++;

        // fill 2D hists
        h2D_m4l_mZ2->Fill(mass4l, massZ2, weight);
        h2D_m4l_pT4l->Fill(mass4l, pT4l, weight);
        h2D_m4l_eta4l->Fill(mass4l, eta4l, weight);
        h2D_m4l_nJets->Fill(mass4l, njets_pt30_eta4p7, weight);

        // compute additional variables to store in the tree
        selectedWeight = weight;
        kfactor_ggZZ = k_ggZZ;
        kfactor_qqZZ = k_qqZZ_qcd_M*k_qqZZ_ewk;

        TT->Fill();

        if(!SILENT) {
            if (nEvtMassWindow<=NEVT_PRINTOUT || Run==46520) {
                string sfinalState;
                if (finalState==0) continue;
                if (finalState==1) sfinalState = "4mu";
                if (finalState==2) sfinalState = "4e";
                if (finalState==3) sfinalState = "2e2mu";
                if (finalState==4) sfinalState = "2mu2e";
                cout << fixed;
                cout.precision(printOutPrecision);
//                cout << Event << ":" << Run << ":" << LumiSect << ":" << mass4l << ":" << massZ1 << ":" << massZ2 << ":" << weight << ":" << kd_ALT << ":" << mekd_m4l << ":" << pdfSigM4l << ":" << pdfBkgM4l << endl;
            }
        }
    }
    if(!SILENT) {
        cout  << setw(printOutWidth) << "nEventsInMassWindow: " << nEvtMassWindow << endl;
    }

    // yield & eff. print-out
    if ((processNameTag != "Data")&&(processNameTag != "ZJetsCR")) {
        cout  << setw(printOutWidth) << "[" + processNameTag + ", " <<setw(6)<<iFinState << "][GEN: "<<setw(6)<<nEvents<< ", passed: "<<setw(6)<<nEvtMassWindow<<"]" << "[GEN-final-eff: " <<setw(6)<< ( (double) nEvtMassWindow/nEvents) << "]" << endl;
    }
    return 0;
}

//_______________________________________________________________________________________________________________________________________________
// using the fixed floor at the moment, to be changed
int getTemplateXS(TString processNameTag, TString processFileName, TString sqrtsTag, TString sfinalState,
                  TString obsName, TString obsBinDn, TString obsBinUp, TString fitTypeZ4l, bool useRefit,
                  double elpT, double mupT, double mZ2_low, double mZ1_low, double m4l_low, double m4l_high) {

    // prepare final state variables (for loop, later also plotting)
    unsigned int iFinState;
    if      (sfinalState == "4mu")   {iFinState = 1;}
    else if (sfinalState == "4e")    {iFinState = 2;}
    else if (sfinalState == "2e2mu") {iFinState = 3;}
    else if (sfinalState == "AllChans")   {iFinState = 5;}
    else return -1;

    // get chains
    TChain* sigTree;
    if (processNameTag == "Data") {
        sigTree = new TChain("Ana/passedEvents");
    } else if (processNameTag == "ZJetsCR") {
//        sigTree = new TChain("passedEvents");  //test 2016
        sigTree = new TChain("Ana/passedEvents"); // David 2018
        loadFakeRateHists();
    } else {
        sigTree = new TChain("Ana/passedEvents");
    }
//    cout<<"the sigTree is ===", sigTree 
    sigTree->Add(processFileName);

    // tree for a set of variables, for selected events
    TString fOption = "RECREATE";
    TString templateNameTag = getTemplateNameTag(processNameTag);
    TString fLocation = templatesDir+"/"+PROCESSING_TYPE+"_"+obsName+"/"+sqrtsTag+"/";
    TFile* fTemplateTree = new TFile(fLocation+"/"+templateNameTag+"_"+sfinalState+".root", fOption);
    TTree* TT = new TTree("selectedEvents","selectedEvents");



    //nEvents
    if ((processNameTag != "Data")&&(processNameTag != "ZJetsCR")) {
        TFile *f = TFile::Open(processFileName);
        TH1D* hNEvents = (TH1D*) f->Get("Ana/nEvents");
        nEvents = hNEvents->GetBinContent(1);
    }

    // define histograms with variable binning
    TH2D* h2D_m4l_mZ2   = new TH2D("m4l_massZ2","m4l_massZ2",nbinsX, m4l_low, m4l_high, nbinsY, 0, 60.0); h2D_m4l_mZ2->Sumw2();
    TH2D* h2D_m4l_pT4l  = new TH2D("m4l_pT4l",  "m4l_pT4l",  nbinsX, m4l_low, m4l_high, nbinsY, 0, 200.0); h2D_m4l_pT4l->Sumw2();
    TH2D* h2D_m4l_eta4l = new TH2D("m4l_eta4l", "m4l_eta4l", nbinsX, m4l_low, m4l_high, nbinsY, 0, 5.0); h2D_m4l_eta4l->Sumw2();
    TH2D* h2D_m4l_nJets = new TH2D("m4l_njets_pt30_eta4p7", "m4l_njets_pt30_eta4p7", nbinsX, m4l_low, m4l_high, 10, 0, 10); h2D_m4l_nJets->Sumw2();

    // loop over the tree and fill histograms
    getHistTreesXS(sigTree, processNameTag, sqrtsTag, TT, h2D_m4l_mZ2, h2D_m4l_pT4l, h2D_m4l_eta4l, h2D_m4l_nJets,
                   iFinState, elpT, mupT, mZ2_low, mZ1_low, m4l_low, m4l_high, useRefit, true);

    // smoothing, filling the empty bins, normalisation
    if (processNameTag != "Data") {
        smoothAndNormaliseTemplate(h2D_m4l_mZ2,   SILENT); // print-out info only if not silent
        smoothAndNormaliseTemplate(h2D_m4l_pT4l,  SILENT); // print-out info only if not silent
        smoothAndNormaliseTemplate(h2D_m4l_eta4l, SILENT); // print-out info only if not silent
        smoothAndNormaliseTemplate(h2D_m4l_nJets, SILENT); // print-out info only if not silent
    }

    // store & delete the tree, produce & store the templates
//    TString templateNameTag = getTemplateNameTag(processNameTag);
//    TString fLocation = templatesDir+"/"+PROCESSING_TYPE+"_"+obsName+"/"+sqrtsTag+"/";
//    TString fOption = "RECREATE";
    cout<<"obsBinDn "<<obsBinDn<<" obsBinUp "<<obsBinUp<<endl;
    if (obsBinDn==obsBinUp && obsBinDn.Contains("|")) { // if bin boundaries are passed - get the  boundaries in TObjArray and loop
        TObjArray* ta = (TObjArray*) obsBinDn.Tokenize("|");
        for (int kEntry = 0; kEntry < ta->GetEntries() - 1; kEntry++){
            TString obsBinDn = ((TObjString*) ta->At(kEntry))->GetString();
            TString obsBinUp = ((TObjString*) ta->At(kEntry+1))->GetString();
            cout<<"test1: "<<endl;
            storeTreeAndTemplatesXS(TT, obsName, obsBinDn, obsBinUp, sfinalState, fLocation, templateNameTag, fOption, fitTypeZ4l, useRefit);
        }
    } else { // if one set of up & down bin boundaries is passed - run for it
        cout<<"test1: "<<endl;
        storeTreeAndTemplatesXS(TT, obsName, obsBinDn, obsBinUp, sfinalState, fLocation, templateNameTag, fOption, fitTypeZ4l, useRefit);
    }

//    TFile* fTemplateTree = new TFile(fLocation+"/"+templateNameTag+"_"+sfinalState+".root", fOption);
    fTemplateTree->cd();
    TT->Write();
    h2D_m4l_mZ2->SetName("h2D_m4l_massZ2"); h2D_m4l_mZ2->Write();
    h2D_m4l_pT4l->SetName("h2D_m4l_pT4l"); h2D_m4l_pT4l->Write();
    h2D_m4l_eta4l->SetName("h2D_m4l_eta4l"); h2D_m4l_eta4l->Write();
    h2D_m4l_nJets->SetName("h2D_m4l_nJets"); h2D_m4l_nJets->Write();
    fTemplateTree->Close();
//    TT->Delete();

    return 0;
}

//_______________________________________________________________________________________________________________________________________________
void storeTreeAndTemplatesXS(TTree* TT, TString obsName, TString obsBinDn, TString obsBinUp, TString sfinalState, TString fLocation, TString templateNameTag, TString fOption, TString fitTypeZ4l, bool useRefit){

    TString obsTag = obsName+"_"+obsBinDn+"_"+obsBinUp;
    TH1D* h1D = new TH1D("m4l_"+obsTag, "m4l_"+obsTag, nbinsX, CUT_M4LLOW, CUT_M4LHIGH);

    // adjust obsName for the selection, e.g. where abs(x) is required
    TString selectionObsName = "1";
    if (obsName=="costhetastar"){
        selectionObsName = "abs(cosThetaStar)";
    }else if (obsName=="cosThetaStar"){
        selectionObsName = "abs(cosThetaStar)";
    }else if (obsName=="cosTheta1"){
        selectionObsName = "abs(cosTheta1)";
    }else if (obsName=="costheta1"){
        selectionObsName = "abs(cosTheta1)";
    }else if (obsName=="costheta2"){
        selectionObsName = "abs(cosTheta2)";
    }else if (obsName=="cosTheta2"){
        selectionObsName = "abs(cosTheta2)";
    }else if (obsName=="Phi"){
        selectionObsName = "abs(Phi)";
    }else if (obsName=="phi"){
        selectionObsName = "abs(Phi)";
    }else if (obsName=="Phi1"){
        selectionObsName = "abs(Phi1)";
    }else if (obsName=="phi1"){
        selectionObsName = "abs(Phi1)";
    }else if (obsName=="eta4l"){
        selectionObsName = "abs(eta4l)";
    }else if (obsName=="rapidity4l"){
        selectionObsName = "abs(rapidity4l)";
    }else if (obsName=="inclusive"){
        selectionObsName = "pT4l";
    }else {
        selectionObsName = obsName;
    }

    // prepare cuts and get hist from the tree->Draw()
    TString treeCut = "((" + obsBinDn + " <= "+selectionObsName+") && ("+selectionObsName+" < " + obsBinUp + "))";
    TString sM4l = "";
    if (useRefit) {sM4l = "mass4lREFIT>>m4l_";}
    else {sM4l = "mass4l>>m4l_";}
    TString treeReq; treeReq = sM4l+obsTag;
    double entriesTot = TT->GetEntries();
    double entriesBin = TT->GetEntries(treeCut);
    double fracBin = (double) entriesBin/entriesTot;
    cout << "[Observable tag: " << obsTag << "]" << endl;
    cout << "[Tree and templates saved in: " << fLocation << "]" << endl;
    cout << "[Bin fraction: " << fracBin << "][end fraction]" << endl;
    if (obsName.Contains("jet")){ // assumes obserbale name in form "njets_pt{pt}_eta{eta}"
        TString treeCut_jesdn = "((" + obsBinDn + " <= "+obsName+"_jesdn) && ("+obsName+"_jesdn < " + obsBinUp + "))";
        double entriesBin_jesdn = TT->GetEntries(treeCut_jesdn);
        double fracBin_jesdn = (double) entriesBin_jesdn/entriesTot;
        TString treeCut_jesup = "((" + obsBinDn + " <= "+obsName+"_jesup) && ("+obsName+"_jesup < " + obsBinUp + "))";
        double entriesBin_jesup = TT->GetEntries(treeCut_jesup);
        double fracBin_jesup = (double) entriesBin_jesup/entriesTot;
        cout << "[Bin fraction (JESdn): " << fracBin_jesdn << "]" << endl;
        cout << "[Bin fraction (JESup): " << fracBin_jesup << "]" << endl;
    }

    TString sWeight = "weight*";
    TString treeWeightedCut; treeWeightedCut = sWeight + treeCut;
    TT->Draw(treeReq.Data(), treeWeightedCut.Data(), "goff");

    TString templateLocation = fLocation+"/"+templateNameTag+"_"+sfinalState+"_"+obsTag+".root";
    TFile* fTemplate = new TFile(templateLocation, fOption);
    fTemplate->cd();
    h1D->GetXaxis()->SetTitle("CMS_zz4l_mass");

    if (fitTypeZ4l!="doHighMass") {
        //for (int k = 0; k < 5; k++)        
        smoothAndNormaliseTemplate1D(h1D); // 5-smoothing
        //if (templateNameTag == "XSBackground_ZJetsCR") {
        //    for (int k = 0; k < 5; k++) smoothAndNormaliseTemplate1D(h1D); // once again 5-smoothing
        // }
    }

    h1D->Write();
    fTemplate->Close();
    h1D->Delete();
}

//_______________________________________________________________________________________________________________________________________________
void smoothAndNormaliseTemplate(TH2D* &h2D, bool silent){
    cout.precision(2*printOutPrecision);
    int nXbins=h2D->GetNbinsX();
    int nYbins=h2D->GetNbinsY();
    // smooth
    TString smthAlg = "k5b";
    if (!silent) cout << "   Pre-Smooth:  " << h2D->Integral() << endl;
    h2D->Smooth(1, smthAlg);
    if (!silent) cout << "   Post-Smooth: " << h2D->Integral() << endl;
    // norm + floor + norm
    normaliseHist(h2D);
    if (!silent) cout << "   Normalised:  " << h2D->Integral() << endl;
    double floor = .001/(nXbins*nYbins);
    fillEmptyBinsHist2D(h2D,floor);
    if (!silent) cout << "   Post-Floor:  " << h2D->Integral() << endl;
    normaliseHist(h2D);
    if (!silent) cout << "   Final:       " << h2D->Integral() << endl;
}

//_______________________________________________________________________________________________________________________________________________
void smoothAndNormaliseTemplate1D(TH1D* &h1D, double norm){
    // smooth
    h1D->Smooth(10000);
    // norm + floor + norm
    normaliseHist(h1D, norm);
    fillEmptyBinsHist1D(h1D,.001/(h1D->GetNbinsX()));
    normaliseHist(h1D, norm);
}

//_______________________________________________________________________________________________________________________________________________
int normaliseHist(TH1D* &h1D, double norm){
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
int normaliseHist(TH2D* &h2D, double norm){
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
double kdWithPDFm4l(double KD, double pdfSigM4l, double pdfBkgM4l){
    double mekd_m4l = (pdfSigM4l * KD) / (pdfSigM4l * KD +  pdfBkgM4l * (1 - KD));  // superKD-like (computed directly from the KD)
    return mekd_m4l;
}

//_______________________________________________________________________________________________________________________________________________
TString strRandom(unsigned int rndmMax) {return (TString::Format("%d",(int)(pRnd->Rndm()*10000)));}

//_______________________________________________________________________________________________________________________________________________
TString getTemplateNameTag(TString processNameTag) {
    // init template file names
    TString DTreeNameTag = "";
    if      (processNameTag == "SM")    {DTreeNameTag = "XSSignal_gg0m+";}
    else if (processNameTag == "ALT")   {DTreeNameTag = "XSSignal_"+processNameTag;}
    else if (processNameTag == "qqZZ" ||
             processNameTag == "ggZZ" ||
             processNameTag == "ZJetsCR"){DTreeNameTag = "XSBackground_"+processNameTag;}
    else if (processNameTag == "Data")   {DTreeNameTag = "XSData";}

    if (PROCESSING_TYPE=="XSTreeZ4l" && processNameTag == "SM") {DTreeNameTag = "XSSignal_qqZZs";}

    return DTreeNameTag;
}

//_______________________________________________________________________________________________________________________________________________
void loadFakeRateHists(){
    // open files
    TFile *frel = TFile::Open(fakeRatesEl);
    TFile *frmu = TFile::Open(fakeRatesMu);
    // load fake rate histogram
    h1DFRelEB    = (TH1D*) frel->Get(h1Name_FRel_EB);
    h1DFRelEE    = (TH1D*) frel->Get(h1Name_FRel_EE);
    h1DFRmuEB    = (TH1D*) frmu->Get(h1Name_FRmu_EB);
    h1DFRmuEE    = (TH1D*) frmu->Get(h1Name_FRmu_EE);
}

//_______________________________________________________________________________________________________________________________________________
double getFakeRateWeight(TString lepMode, TString etaRegion, double pT) {
    // get the fake rate for given pT and eta (fake rate files must be loaded)
    double fr, frWeight;
    if (lepMode == "el" && etaRegion == "EB") {
        fr = h1DFRelEB->GetBinContent(h1DFRelEB->FindBin(pT));
    } else if (lepMode == "el" && etaRegion == "EE") {
        fr = h1DFRelEE->GetBinContent(h1DFRelEE->FindBin(pT));
    } else if (lepMode == "mu" && etaRegion == "EB") {
        fr = h1DFRmuEB->GetBinContent(h1DFRmuEB->FindBin(pT));
    } else if (lepMode == "mu" && etaRegion == "EE") {
        fr = h1DFRmuEE->GetBinContent(h1DFRmuEE->FindBin(pT));
    } else {
        fr = 0.;
    }
    // compute the fake rate factor and return it
    frWeight = (fr / (1 - fr));
    return frWeight;
}

//_______________________________________________________________________________________________________________________________________________
void loadKFactorGraphs(){
    // open file
    TFile *fKFactor = TFile::Open(kFactorFileName);
    // load k-factor graphs
    TGraphAsymmErrors* gr_kFactor_tmp = (TGraphAsymmErrors*) fKFactor->Get(grName_kFactor);
    gr_kFactor = (TGraphAsymmErrors*) gr_kFactor_tmp->Clone();
    fKFactor->Close();
    delete fKFactor;
}


//_______________________________________________________________________________________________________________________________________________
double getGluGluZZKFactor(double m4l) {
    // get the k-factor for ggZZ for given m4l (k-factor files must be loaded)
    //double kfactor = gr_kFactor->Eval(m4l);
    double kfactor = 1.7;
    return kfactor;
}

