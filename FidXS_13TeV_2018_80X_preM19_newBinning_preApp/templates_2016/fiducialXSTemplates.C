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
#include "TGraphErrors.h"
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
const TString fakeRatesEl = "newData_FakeRates_OS_2016.root";  // new for HIG-19-001 paper
//const TString h1Name_FRel_EB = "h1D_FRel_EB";
const TString g1Name_FRel_EB = "FR_OS_electron_EB";
//const TString h1Name_FRel_EE = "h1D_FRel_EE";
const TString g1Name_FRel_EE = "FR_OS_electron_EE";
//const TString fakeRatesMu = "fakeRates_mu.root";
const TString fakeRatesMu = "newData_FakeRates_OS_2016.root";  // new for HIG-19-001 paper
//const TString h1Name_FRmu_EB = "h1D_FRmu_EB";
const TString g1Name_FRmu_EB = "FR_OS_muon_EB";
//const TString h1Name_FRmu_EE = "h1D_FRmu_EE";
const TString g1Name_FRmu_EE = "FR_OS_muon_EE";
//TH1D *h1DFRelEB, *h1DFRelEE, *h1DFRmuEB, *h1DFRmuEE;

TGraph *g1DFRelEB, *g1DFRelEE, *g1DFRmuEB, *g1DFRmuEE;  // 


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
    cout << "templatesDir :" << templatesDir << endl;
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
// new obs.
    float pT4lj; float pT4ljj;
    float mass4lj; float mass4ljj;
    float pTj1; float mj1; float yj1; float etaj1; float phij1;
    float pTj2; float yj2; float mj2; float etaj2; float phij2;
    float pTj1_2p5; float mj1_2p5; float yj1_2p5; float etaj1_2p5; float phij1_2p5;
    float pTj2_2p5; float yj2_2p5; float mj2_2p5; float etaj2_2p5; float phij2_2p5;
    float mj1j2; float dEtaj1j2;
    float dPhiHj1; float dyHj1;
    float dPhij1j2; float dPhiHj1j2;
    float dPhij1j2_VBF ;
    
    float dPhiHj1_2p5; float dyHj1_2p5;
    float mj1j2_2p5; float dEtaj1j2_2p5;
    float dPhij1j2_2p5; float dPhiHj1j2_2p5;
    float pTj1_VBF; float dPhiHj1j2_VBF;
//new obs. JES dn. reco
    float pTj1_jesdn; float mj1_jesdn; float yj1_jesdn; float etaj1_jesdn; float phij1_jesdn;
    float pTj2_jesdn; float yj2_jesdn; float mj2_jesdn; float etaj2_jesdn; float phij2_jesdn;

    float pTj1_2p5_jesdn; float mj1_2p5_jesdn; float yj1_2p5_jesdn; float etaj1_2p5_jesdn; float phij1_2p5_jesdn;
    float pTj2_2p5_jesdn; float yj2_2p5_jesdn; float mj2_2p5_jesdn; float etaj2_2p5_jesdn; float phij2_2p5_jesdn;

    float mj1j2_jesdn; float dEtaj1j2_jesdn;

    float dPhiHj1_jesdn; float dyHj1_jesdn;
    float dPhij1j2_jesdn; float dPhiHj1j2_jesdn;

    float dPhiHj1_2p5_jesdn; float dyHj1_2p5_jesdn;
    float mj1j2_2p5_jesdn; float dEtaj1j2_2p5_jesdn;
    float dPhij1j2_2p5_jesdn; float dPhiHj1j2_2p5_jesdn;
    float pTj1_VBF_jesdn; float dPhij1j2_VBF_jesdn; float dPhiHj1j2_VBF_jesdn;
    float mass4lj_jesdn; float mass4ljj_jesdn; float pT4lj_jesdn; float pT4ljj_jesdn;
    // JES up reco
    float pTj1_jesup; float mj1_jesup; float yj1_jesup; float etaj1_jesup; float phij1_jesup;
    float pTj2_jesup; float yj2_jesup; float mj2_jesup; float etaj2_jesup; float phij2_jesup;

    float pTj1_2p5_jesup; float mj1_2p5_jesup; float yj1_2p5_jesup; float etaj1_2p5_jesup; float phij1_2p5_jesup;
    float pTj2_2p5_jesup; float yj2_2p5_jesup; float mj2_2p5_jesup; float etaj2_2p5_jesup; float phij2_2p5_jesup;


    float mj1j2_jesup; float dEtaj1j2_jesup;

    float dPhiHj1_jesup; float dyHj1_jesup;
    float dPhij1j2_jesup; float dPhiHj1j2_jesup;

    float dPhiHj1_2p5_jesup; float dyHj1_2p5_jesup;
    float mj1j2_2p5_jesup; float dEtaj1j2_2p5_jesup;
    float dPhij1j2_2p5_jesup; float dPhiHj1j2_2p5_jesup;
    float pTj1_VBF_jesup; float dPhij1j2_VBF_jesup; float dPhiHj1j2_VBF_jesup;
    float mass4lj_jesup; float mass4ljj_jesup;
    float pT4lj_jesup; float pT4ljj_jesup;

// KD based new observables
    float D_bkg_kin, D_bkg, D_g4, D_g1g4, D_0m, D_CP, D_0hp, D_int, D_L1, D_L1_int, D_L1Zg, D_L1Zgint;
// Tau variables
    float TauC_Inc_0j_EnergyWgt, TauB_Inc_0j_EnergyWgt;


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
    if (tree->GetBranch("pTj1")) {tree->SetBranchAddress("pTj1",&pt_leadingjet_pt30_eta4p7);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta4p7_jesup")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta4p7_jesup",&pt_leadingjet_pt30_eta4p7_jesup);}
    if (tree->GetBranch("pTj1_jesup")) {tree->SetBranchAddress("pTj1_jesup",&pt_leadingjet_pt30_eta4p7_jesup);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta4p7_jesdn")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta4p7_jesdn",&pt_leadingjet_pt30_eta4p7_jesdn);}
    if (tree->GetBranch("pTj1_jesdn")) {tree->SetBranchAddress("pTj1_jesdn",&pt_leadingjet_pt30_eta4p7_jesdn);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta2p5")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta2p5",&pt_leadingjet_pt30_eta2p5);}
    if (tree->GetBranch("pTj1_2p5")) {tree->SetBranchAddress("pTj1_2p5",&pt_leadingjet_pt30_eta2p5);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta2p5_jesup")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta2p5_jesup",&pt_leadingjet_pt30_eta2p5_jesup);}
    if (tree->GetBranch("pTj1_2p5_jesup")) {tree->SetBranchAddress("pTj1_2p5_jesup",&pt_leadingjet_pt30_eta2p5_jesup);}
    if (tree->GetBranch("pt_leadingjet_pt30_eta2p5_jesdn")) {tree->SetBranchAddress("pt_leadingjet_pt30_eta2p5_jesdn",&pt_leadingjet_pt30_eta2p5_jesdn);}
    if (tree->GetBranch("pTj1_2p5_jesdn")) {tree->SetBranchAddress("pTj1_2p5_jesdn",&pt_leadingjet_pt30_eta2p5_jesdn);}
// new obs.
    if (tree->GetBranch("mass4lj")){tree->SetBranchAddress("mass4lj",&mass4lj);}
    if (tree->GetBranch("mass4lj_jesdn")){tree->SetBranchAddress("mass4lj_jesdn",&mass4lj_jesdn);}
    if (tree->GetBranch("mass4lj_jesup")){tree->SetBranchAddress("mass4lj_jesup",&mass4lj_jesup);}
    if (tree->GetBranch("pTj2")){tree->SetBranchAddress("pTj2",&pTj2);}
    if (tree->GetBranch("pTj2_jesdn")){tree->SetBranchAddress("pTj2_jesdn",&pTj2_jesdn);}
    if (tree->GetBranch("pTj2_jesup")){tree->SetBranchAddress("pTj2_jesup",&pTj2_jesup);}
    if (tree->GetBranch("mj1j2")){tree->SetBranchAddress("mj1j2",&mj1j2);}
    if (tree->GetBranch("mj1j2_jesdn")){tree->SetBranchAddress("mj1j2_jesdn",&mj1j2_jesdn);}
    if (tree->GetBranch("mj1j2_jesup")){tree->SetBranchAddress("mj1j2_jesup",&mj1j2_jesup);}

//   leading jet (eta 4p7) 
    if (tree->GetBranch("pTj1")) {tree->SetBranchAddress("pTj1",&pTj1);}
    if (tree->GetBranch("yj1")) {tree->SetBranchAddress("yj1",&yj1);}
    if (tree->GetBranch("etaj1")) {tree->SetBranchAddress("etaj1",&etaj1);}
    if (tree->GetBranch("phij1")) {tree->SetBranchAddress("phij1",&phij1);}
    if (tree->GetBranch("mj1")) {tree->SetBranchAddress("mj1",&mj1);}
//   leading jet JES dn (eta 4p7) 
    if (tree->GetBranch("pTj1_jesdn")) {tree->SetBranchAddress("pTj1_jesdn",&pTj1_jesdn);}
    if (tree->GetBranch("yj1_jesdn")) {tree->SetBranchAddress("yj1_jesdn",&yj1_jesdn);}
    if (tree->GetBranch("etaj1_jesdn")) {tree->SetBranchAddress("etaj1_jesdn",&etaj1_jesdn);}
    if (tree->GetBranch("phij1_jesdn")) {tree->SetBranchAddress("phij1_jesdn",&phij1_jesdn);}
    if (tree->GetBranch("mj1_jesdn")) {tree->SetBranchAddress("mj1_jesdn",&mj1_jesdn);}
//   leading jet JES up(eta 4p7) 
    if (tree->GetBranch("pTj1_jesup")) {tree->SetBranchAddress("pTj1_jesup",&pTj1_jesup);}
    if (tree->GetBranch("yj1_jesup")) {tree->SetBranchAddress("yj1_jesup",&yj1_jesup);}
    if (tree->GetBranch("etaj1_jesup")) {tree->SetBranchAddress("etaj1_jesup",&etaj1_jesup);}
    if (tree->GetBranch("phij1_jesup")) {tree->SetBranchAddress("phij1_jesup",&phij1_jesup);}
    if (tree->GetBranch("mj1_jesup")) {tree->SetBranchAddress("mj1_jesup",&mj1_jesup);}
/////////////////////////////////////////////////////////////////////////////////////////////
//   sub-leading jet (eta 4p7) 
    if (tree->GetBranch("pTj2")) {tree->SetBranchAddress("pTj2",&pTj2);}
    if (tree->GetBranch("yj2")) {tree->SetBranchAddress("yj2",&yj2);}
    if (tree->GetBranch("etaj2")) {tree->SetBranchAddress("etaj2",&etaj2);}
    if (tree->GetBranch("phij2")) {tree->SetBranchAddress("phij2",&phij2);}
    if (tree->GetBranch("mj2")) {tree->SetBranchAddress("mj2",&mj2);}
//   sub-leading jet JES dn (eta 4p7) 
    if (tree->GetBranch("pTj2_jesdn")) {tree->SetBranchAddress("pTj2_jesdn",&pTj2_jesdn);}
    if (tree->GetBranch("yj2_jesdn")) {tree->SetBranchAddress("yj2_jesdn",&yj2_jesdn);}
    if (tree->GetBranch("etaj2_jesdn")) {tree->SetBranchAddress("etaj2_jesdn",&etaj2_jesdn);}
    if (tree->GetBranch("phij2_jesdn")) {tree->SetBranchAddress("phij2_jesdn",&phij2_jesdn);}
    if (tree->GetBranch("mj2_jesdn")) {tree->SetBranchAddress("mj2_jesdn",&mj2_jesdn);}
//   sub-leading jet JES up (eta 4p7) 
    if (tree->GetBranch("pTj2_jesup")) {tree->SetBranchAddress("pTj2_jesup",&pTj2_jesup);}
    if (tree->GetBranch("yj2_jesup")) {tree->SetBranchAddress("yj2_jesup",&yj2_jesup);}
    if (tree->GetBranch("etaj2_jesup")) {tree->SetBranchAddress("etaj2_jesup",&etaj2_jesup);}
    if (tree->GetBranch("phij2_jesup")) {tree->SetBranchAddress("phij2_jesup",&phij2_jesup);}
    if (tree->GetBranch("mj2_jesup")) {tree->SetBranchAddress("mj2_jesup",&mj2_jesup);}
//////////////////////////////////////////////////////////////////////////////////////////////    	
//   leading jet (eta 2p5) 
    if (tree->GetBranch("pTj1_2p5")) {tree->SetBranchAddress("pTj1_2p5",&pTj1_2p5);}
    if (tree->GetBranch("yj1_2p5")) {tree->SetBranchAddress("yj1_2p5",&yj1_2p5);}
    if (tree->GetBranch("etaj1_2p5")) {tree->SetBranchAddress("etaj1_2p5",&etaj1_2p5);}
    if (tree->GetBranch("phij1_2p5")) {tree->SetBranchAddress("phij1_2p5",&phij1_2p5);}
    if (tree->GetBranch("mj1_2p5")) {tree->SetBranchAddress("mj1_2p5",&mj1_2p5);}
//   leading jet JES dn (eta 2p5) 
    if (tree->GetBranch("pTj1_2p5_jesdn")) {tree->SetBranchAddress("pTj1_2p5_jesdn",&pTj1_2p5_jesdn);}
    if (tree->GetBranch("yj1_2p5_jesdn")) {tree->SetBranchAddress("yj1_2p5_jesdn",&yj1_2p5_jesdn);}
    if (tree->GetBranch("etaj1_2p5_jesdn")) {tree->SetBranchAddress("etaj1_2p5_jesdn",&etaj1_2p5_jesdn);}
    if (tree->GetBranch("phij1_2p5_jesdn")) {tree->SetBranchAddress("phij1_2p5_jesdn",&phij1_2p5_jesdn);}
    if (tree->GetBranch("mj1_2p5_jesdn")) {tree->SetBranchAddress("mj1_2p5_jesdn",&mj1_2p5_jesdn);}
//   leading jet JES up (eta 2p5) 
    if (tree->GetBranch("pTj1_2p5_jesup")) {tree->SetBranchAddress("pTj1_2p5_jesup",&pTj1_2p5_jesup);}
    if (tree->GetBranch("yj1_2p5_jesup")) {tree->SetBranchAddress("yj1_2p5_jesup",&yj1_2p5_jesup);}
    if (tree->GetBranch("etaj1_2p5_jesup")) {tree->SetBranchAddress("etaj1_2p5_jesup",&etaj1_2p5_jesup);}
    if (tree->GetBranch("phij1_2p5_jesup")) {tree->SetBranchAddress("phij1_2p5_jesup",&phij1_2p5_jesup);}
    if (tree->GetBranch("mj1_2p5_jesup")) {tree->SetBranchAddress("mj1_2p5_jesup",&mj1_2p5_jesup);}
///////////////////////////////////////////////////////////////////////////////////////////////////////
//   sub-leading jet (eta 2p5) 
    if (tree->GetBranch("pTj2_2p5")) {tree->SetBranchAddress("pTj2_2p5",&pTj2_2p5);}
    if (tree->GetBranch("yj2_2p5")) {tree->SetBranchAddress("yj2_2p5",&yj2_2p5);}
    if (tree->GetBranch("etaj2_2p5")) {tree->SetBranchAddress("etaj2_2p5",&etaj2_2p5);}
    if (tree->GetBranch("phij2_2p5")) {tree->SetBranchAddress("phij2_2p5",&phij2_2p5);}
    if (tree->GetBranch("mj2_2p5")) {tree->SetBranchAddress("mj2_2p5",&mj2_2p5);}
//   sub-leading jet JES dn (eta 2p5) 
    if (tree->GetBranch("pTj2_2p5_jesdn")) {tree->SetBranchAddress("pTj2_2p5_jesdn",&pTj2_2p5_jesdn);}
    if (tree->GetBranch("yj2_2p5_jesdn")) {tree->SetBranchAddress("yj2_2p5_jesdn",&yj2_2p5_jesdn);}
    if (tree->GetBranch("etaj2_2p5_jesdn")) {tree->SetBranchAddress("etaj2_2p5_jesdn",&etaj2_2p5_jesdn);}
    if (tree->GetBranch("phij2_2p5_jesdn")) {tree->SetBranchAddress("phij2_2p5_jesdn",&phij2_2p5_jesdn);}
    if (tree->GetBranch("mj2_2p5_jesdn")) {tree->SetBranchAddress("mj2_2p5_jesdn",&mj2_2p5_jesdn);}
//   sub-leading jet JES up (eta 2p5) 
    if (tree->GetBranch("pTj2_2p5_jesup")) {tree->SetBranchAddress("pTj2_2p5_jesup",&pTj2_2p5_jesup);}
    if (tree->GetBranch("yj2_2p5_jesup")) {tree->SetBranchAddress("yj2_2p5_jesup",&yj2_2p5_jesup);}
    if (tree->GetBranch("etaj2_2p5_jesup")) {tree->SetBranchAddress("etaj2_2p5_jesup",&etaj2_2p5_jesup);}
    if (tree->GetBranch("phij2_2p5_jesup")) {tree->SetBranchAddress("phij2_2p5_jesup",&phij2_2p5_jesup);}
    if (tree->GetBranch("mj2_2p5_jesup")) {tree->SetBranchAddress("mj2_2p5_jesup",&mj2_2p5_jesup);}
/////////////////////////////////////////////////////////////////////////////////////////////////////
// other Higgs plus jet system variables
/////////////////////////////////////////////////////////////////////////////////////////////////////
    if (tree->GetBranch("mass4lj")){tree->SetBranchAddress("mass4lj",&mass4lj);}
    if (tree->GetBranch("mass4ljj")){tree->SetBranchAddress("mass4ljj",&mass4ljj);}
    if (tree->GetBranch("pT4lj")){tree->SetBranchAddress("pT4lj",&pT4lj);}
    if (tree->GetBranch("pT4ljj")){tree->SetBranchAddress("pT4ljj",&pT4ljj);}
    if (tree->GetBranch("dPhiHj1")){tree->SetBranchAddress("dPhiHj1",&dPhiHj1);}
    if (tree->GetBranch("dyHj1")){tree->SetBranchAddress("dyHj1",&dyHj1);}
    if (tree->GetBranch("mj1j2")){tree->SetBranchAddress("mj1j2",&mj1j2);}
    if (tree->GetBranch("dEtaj1j2")){tree->SetBranchAddress("dEtaj1j2",&dEtaj1j2);}
    if (tree->GetBranch("dPhij1j2")){tree->SetBranchAddress("dPhij1j2",&dPhij1j2);}
    if (tree->GetBranch("dPhiHj1j2")){tree->SetBranchAddress("dPhiHj1j2",&dPhiHj1j2);}
    if (tree->GetBranch("dPhij1j2_VBF")){tree->SetBranchAddress("dPhij1j2_VBF",&dPhij1j2_VBF);}
    if (tree->GetBranch("dPhiHj1j2_VBF")){tree->SetBranchAddress("dPhiHj1j2_VBF",&dPhiHj1j2_VBF);}

// other Higgs plus jet system variables    JES dn
    if (tree->GetBranch("mass4lj_jesdn")){tree->SetBranchAddress("mass4lj_jesdn",&mass4lj_jesdn);}
    if (tree->GetBranch("mass4ljj_jesdn")){tree->SetBranchAddress("mass4ljj_jesdn",&mass4ljj_jesdn);}
    if (tree->GetBranch("pT4lj_jesdn")){tree->SetBranchAddress("pT4lj_jesdn",&pT4lj_jesdn);}
    if (tree->GetBranch("pT4ljj_jesdn")){tree->SetBranchAddress("pT4ljj_jesdn",&pT4ljj_jesdn);}
    if (tree->GetBranch("dPhiHj1_jesdn")){tree->SetBranchAddress("dPhiHj1_jesdn",&dPhiHj1_jesdn);}
    if (tree->GetBranch("dyHj1_jesdn")){tree->SetBranchAddress("dyHj1_jesdn",&dyHj1_jesdn);}
    if (tree->GetBranch("mj1j2_jesdn")){tree->SetBranchAddress("mj1j2_jesdn",&mj1j2_jesdn);}
    if (tree->GetBranch("dEtaj1j2_jesdn")){tree->SetBranchAddress("dEtaj1j2_jesdn",&dEtaj1j2_jesdn);}
    if (tree->GetBranch("dPhij1j2_jesdn")){tree->SetBranchAddress("dPhij1j2_jesdn",&dPhij1j2_jesdn);}
    if (tree->GetBranch("dPhiHj1j2_jesdn")){tree->SetBranchAddress("dPhiHj1j2_jesdn",&dPhiHj1j2_jesdn);}
    if (tree->GetBranch("dPhij1j2_VBF_jesdn")){tree->SetBranchAddress("dPhij1j2_VBF_jesdn",&dPhij1j2_VBF_jesdn);}
    if (tree->GetBranch("dPhiHj1j2_VBF_jesdn")){tree->SetBranchAddress("dPhiHj1j2_VBF_jesdn",&dPhiHj1j2_VBF_jesdn);}
// other Higgs plus jet system variables    JES up
    if (tree->GetBranch("mass4lj_jesup")){tree->SetBranchAddress("mass4lj_jesup",&mass4lj_jesup);}
    if (tree->GetBranch("mass4ljj_jesup")){tree->SetBranchAddress("mass4ljj_jesup",&mass4ljj_jesup);}
    if (tree->GetBranch("pT4lj_jesup")){tree->SetBranchAddress("pT4lj_jesup",&pT4lj_jesup);}
    if (tree->GetBranch("pT4ljj_jesup")){tree->SetBranchAddress("pT4ljj_jesup",&pT4ljj_jesup);}
    if (tree->GetBranch("dPhiHj1_jesup")){tree->SetBranchAddress("dPhiHj1_jesup",&dPhiHj1_jesup);}
    if (tree->GetBranch("dyHj1_jesup")){tree->SetBranchAddress("dyHj1_jesup",&dyHj1_jesup);}
    if (tree->GetBranch("mj1j2_jesup")){tree->SetBranchAddress("mj1j2_jesup",&mj1j2_jesup);}
    if (tree->GetBranch("dEtaj1j2_jesup")){tree->SetBranchAddress("dEtaj1j2_jesup",&dEtaj1j2_jesup);}
    if (tree->GetBranch("dPhij1j2_jesup")){tree->SetBranchAddress("dPhij1j2_jesup",&dPhij1j2_jesup);}
    if (tree->GetBranch("dPhiHj1j2_jesup")){tree->SetBranchAddress("dPhiHj1j2_jesup",&dPhiHj1j2_jesup);}
    if (tree->GetBranch("dPhij1j2_VBF_jesup")){tree->SetBranchAddress("dPhij1j2_VBF_jesup",&dPhij1j2_VBF_jesup);}
    if (tree->GetBranch("dPhiHj1j2_VBF_jesup")){tree->SetBranchAddress("dPhiHj1j2_VBF_jesup",&dPhiHj1j2_VBF_jesup);}

/////////////////////////////////////////////////////////////////////////////////////////////////////
// other Higgs plus jet system variables (eta 2p5)
/////////////////////////////////////////////////////////////////////////////////////////////////////
    if (tree->GetBranch("dPhiHj1_2p5")){tree->SetBranchAddress("dPhiHj1_2p5",&dPhiHj1_2p5);}
    if (tree->GetBranch("dyHj1_2p5")){tree->SetBranchAddress("dyHj1_2p5",&dyHj1_2p5);}
    if (tree->GetBranch("mj1j2_2p5")){tree->SetBranchAddress("mj1j2_2p5",&mj1j2_2p5);}
    if (tree->GetBranch("dEtaj1j2_2p5")){tree->SetBranchAddress("dEtaj1j2_2p5",&dEtaj1j2_2p5);}
    if (tree->GetBranch("dPhij1j2_2p5")){tree->SetBranchAddress("dPhij1j2_2p5",&dPhij1j2_2p5);}
    if (tree->GetBranch("dPhiHj1j2_2p5")){tree->SetBranchAddress("dPhiHj1j2_2p5",&dPhiHj1j2_2p5);}
// other Higgs plus jet system variables JES dn  (eta 2p5)
/////////////////////////////////////////////////////////////////////////////////////////////////////
    if (tree->GetBranch("dPhiHj1_2p5_jesdn")){tree->SetBranchAddress("dPhiHj1_2p5_jesdn",&dPhiHj1_2p5_jesdn);}
    if (tree->GetBranch("dyHj1_2p5_jesdn")){tree->SetBranchAddress("dyHj1_2p5_jesdn",&dyHj1_2p5_jesdn);}
    if (tree->GetBranch("mj1j2_2p5_jesdn")){tree->SetBranchAddress("mj1j2_2p5_jesdn",&mj1j2_2p5_jesdn);}
    if (tree->GetBranch("dEtaj1j2_2p5_jesdn")){tree->SetBranchAddress("dEtaj1j2_2p5_jesdn",&dEtaj1j2_2p5_jesdn);}
    if (tree->GetBranch("dPhij1j2_2p5_jesdn")){tree->SetBranchAddress("dPhij1j2_2p5_jesdn",&dPhij1j2_2p5_jesdn);}
    if (tree->GetBranch("dPhiHj1j2_2p5_jesdn")){tree->SetBranchAddress("dPhiHj1j2_2p5_jesdn",&dPhiHj1j2_2p5_jesdn);}
// other Higgs plus jet system variables JES up (eta 2p5)
/////////////////////////////////////////////////////////////////////////////////////////////////////
    if (tree->GetBranch("dPhiHj1_2p5_jesup")){tree->SetBranchAddress("dPhiHj1_2p5_jesup",&dPhiHj1_2p5_jesup);}
    if (tree->GetBranch("dyHj1_2p5_jesup")){tree->SetBranchAddress("dyHj1_2p5_jesup",&dyHj1_2p5_jesup);}
    if (tree->GetBranch("mj1j2_2p5_jesup")){tree->SetBranchAddress("mj1j2_2p5_jesup",&mj1j2_2p5_jesup);}
    if (tree->GetBranch("dEtaj1j2_2p5_jesup")){tree->SetBranchAddress("dEtaj1j2_2p5_jesup",&dEtaj1j2_2p5_jesup);}
    if (tree->GetBranch("dPhij1j2_2p5_jesup")){tree->SetBranchAddress("dPhij1j2_2p5_jesup",&dPhij1j2_2p5_jesup);}
    if (tree->GetBranch("dPhiHj1j2_2p5_jesup")){tree->SetBranchAddress("dPhiHj1j2_2p5_jesup",&dPhiHj1j2_2p5_jesup);}

// KD based obs.
    if (tree->GetBranch("D_bkg")){tree->SetBranchAddress("D_bkg",&D_bkg);}
    if (tree->GetBranch("D_bkg_kin")){tree->SetBranchAddress("D_bkg_kin",&D_bkg_kin);}
    if (tree->GetBranch("D_g4")){tree->SetBranchAddress("D_g4",&D_g4);}
    if (tree->GetBranch("D_g1g4")){tree->SetBranchAddress("D_g1g4",&D_g1g4);}
    if (tree->GetBranch("D_0m")){tree->SetBranchAddress("D_0m",&D_0m);}
    if (tree->GetBranch("D_CP")){tree->SetBranchAddress("D_CP",&D_CP);}
    if (tree->GetBranch("D_0hp")){tree->SetBranchAddress("D_0hp",&D_0hp);}
    if (tree->GetBranch("D_int")){tree->SetBranchAddress("D_int",&D_int);}
    if (tree->GetBranch("D_L1")){tree->SetBranchAddress("D_L1",&D_L1);}
    if (tree->GetBranch("D_L1_int")){tree->SetBranchAddress("D_L1_int",&D_L1_int);}
    if (tree->GetBranch("D_L1Zg")){tree->SetBranchAddress("D_L1Zg",&D_L1Zg);}
    if (tree->GetBranch("D_L1Zgint")){tree->SetBranchAddress("D_L1Zgint",&D_L1Zgint);}

// Tau variables
    if (tree->GetBranch("TauB_Inc_0j_EnergyWgt")){tree->SetBranchAddress("TauB_Inc_0j_EnergyWgt",&TauB_Inc_0j_EnergyWgt);}
    if (tree->GetBranch("TauC_Inc_0j_EnergyWgt")){tree->SetBranchAddress("TauC_Inc_0j_EnergyWgt",&TauC_Inc_0j_EnergyWgt);}
        
    

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
// new obs.
    // Jet obs. reco, nominal
    TT->Branch("pTj1",&pTj1,"pTj1/F");
    TT->Branch("phij1",&phij1,"phij1/F");
    TT->Branch("pTj1_VBF",&pTj1_VBF,"pTj1_VBF/F");
    TT->Branch("etaj1",&etaj1,"etaj1/F");
    TT->Branch("yj1",&yj1,"yj1/F");
    TT->Branch("mj1",&mj1,"mj1/F");

    TT->Branch("pTj2",&pTj2,"pTj2/F");
    TT->Branch("etaj2",&etaj2,"etaj2/F");
    TT->Branch("yj2",&yj2,"yj2/F");
    TT->Branch("mj2",&mj2,"mj2/F");
    TT->Branch("phij2",&phij2,"phij2/F");

    TT->Branch("dPhiHj1",&dPhiHj1,"dPhiHj1/F");
    TT->Branch("dyHj1",&dyHj1,"dyHj1/F");
    TT->Branch("mj1j2",&mj1j2,"mj1j2/F");
    TT->Branch("dEtaj1j2",&dEtaj1j2,"dEtaj1j2/F");
    TT->Branch("dPhij1j2",&dPhij1j2,"dPhij1j2/F");
    TT->Branch("dPhiHj1j2",&dPhiHj1j2,"dPhiHj1j2/F");
    TT->Branch("dPhij1j2_VBF",&dPhij1j2_VBF,"dPhij1j2_VBF/F");
    TT->Branch("dPhiHj1j2_VBF",&dPhiHj1j2_VBF,"dPhiHj1j2_VBF/F");
    TT->Branch("pT4lj",&pT4lj,"pT4lj/F");
    TT->Branch("pT4ljj",&pT4ljj,"pT4ljj/F");
    TT->Branch("mass4lj",&mass4lj,"mass4lj/F");
    TT->Branch("mass4ljj",&mass4ljj,"mass4ljj/F");

    TT->Branch("pTj1_2p5",&pTj1_2p5,"pTj1_2p5/F");
    TT->Branch("yj1_2p5",&yj1_2p5,"yj1_2p5/F");
    TT->Branch("mj1_2p5",&mj1_2p5,"mj1_2p5/F");
    TT->Branch("phij1_2p5",&phij1_2p5,"phij1_2p5/F");
    TT->Branch("etaj1_2p5",&etaj1_2p5,"etaj1_2p5/F");

    TT->Branch("pTj2_2p5",&pTj2_2p5,"pTj2_2p5/F");
    TT->Branch("yj2_2p5",&yj2_2p5,"yj2_2p5/F");
    TT->Branch("mj2_2p5",&mj2_2p5,"mj2_2p5/F");
    TT->Branch("etaj2_2p5",&etaj2_2p5,"etaj2_2p5/F");
    TT->Branch("phij2_2p5",&phij2_2p5,"phij2_2p5/F");

    TT->Branch("dPhiHj1_2p5",&dPhiHj1_2p5,"dPhiHj1_2p5/F");
    TT->Branch("dyHj1_2p5",&dyHj1_2p5,"dyHj1_2p5/F");
    TT->Branch("mj1j2_2p5",&mj1j2_2p5,"mj1j2_2p5/F");
    TT->Branch("dEtaj1j2_2p5",&dEtaj1j2_2p5,"dEtaj1j2_2p5/F");
    TT->Branch("dPhij1j2_2p5",&dPhij1j2_2p5,"dPhij1j2_2p5/F");
    TT->Branch("dPhiHj1j2_2p5",&dPhiHj1j2_2p5,"dPhiHj1j2_2p5/F");

    // JES down reco    
    TT->Branch("pTj1_jesdn",&pTj1_jesdn,"pTj1_jesdn/F");
    TT->Branch("pTj1_VBF_jesdn",&pTj1_VBF_jesdn,"pTj1_VBF_jesdn/F");
    TT->Branch("etaj1_jesdn",&etaj1_jesdn,"etaj1_jesdn/F");
    TT->Branch("yj1_jesdn",&yj1_jesdn,"yj1_jesdn/F");
    TT->Branch("mj1_jesdn",&mj1_jesdn,"mj1_jesdn/F");
    TT->Branch("phij1_jesdn",&phij1_jesdn,"phij1_jesdn/F");

    TT->Branch("pTj2_jesdn",&pTj2_jesdn,"pTj2_jesdn/F");
    TT->Branch("etaj2_jesdn",&etaj2_jesdn,"etaj2_jesdn/F");
    TT->Branch("yj2_jesdn",&yj2_jesdn,"yj2_jesdn/F");
    TT->Branch("mj2_jesdn",&mj2_jesdn,"mj2_jesdn/F");
    TT->Branch("phij2_jesdn",&phij2_jesdn,"phij2_jesdn/F");
    
    TT->Branch("dPhiHj1_jesdn",&dPhiHj1_jesdn,"dPhiHj1_jesdn/F");
    TT->Branch("dyHj1_jesdn",&dyHj1_jesdn,"dyHj1_jesdn/F");
    TT->Branch("mj1j2_jesdn",&mj1j2_jesdn,"mj1j2_jesdn/F");
    TT->Branch("dEtaj1j2_jesdn",&dEtaj1j2_jesdn,"dEtaj1j2_jesdn/F");
    TT->Branch("dPhij1j2_jesdn",&dPhij1j2_jesdn,"dPhij1j2_jesdn/F");
    TT->Branch("dPhiHj1j2_jesdn",&dPhiHj1j2_jesdn,"dPhiHj1j2_jesdn/F");
    TT->Branch("dPhij1j2_VBF_jesdn",&dPhij1j2_VBF_jesdn,"dPhij1j2_VBF_jesdn/F");
    TT->Branch("dPhiHj1j2_VBF_jesdn",&dPhiHj1j2_VBF_jesdn,"dPhiHj1j2_VBF_jesdn/F");
    
    TT->Branch("pTj1_2p5_jesdn",&pTj1_2p5_jesdn,"pTj1_2p5_jesdn/F");
    TT->Branch("yj1_2p5_jesdn",&yj1_2p5_jesdn,"yj1_2p5_jesdn/F");
    TT->Branch("mj1_2p5_jesdn",&mj1_2p5_jesdn,"mj1_2p5_jesdn/F");
    TT->Branch("etaj1_2p5_jesdn",&etaj1_2p5_jesdn,"etaj1_2p5_jesdn/F");
    TT->Branch("phij1_2p5_jesdn",&phij1_2p5_jesdn,"phij1_2p5_jesdn/F");

    TT->Branch("pTj2_2p5_jesdn",&pTj2_2p5_jesdn,"pTj2_2p5_jesdn/F");
    TT->Branch("yj2_2p5_jesdn",&yj2_2p5_jesdn,"yj2_2p5_jesdn/F");
    TT->Branch("mj2_2p5_jesdn",&mj2_2p5_jesdn,"mj2_2p5_jesdn/F");
    TT->Branch("etaj2_2p5_jesdn",&etaj2_2p5_jesdn,"etaj2_2p5_jesdn/F");
    TT->Branch("phij2_2p5_jesdn",&phij2_2p5_jesdn,"phij2_2p5_jesdn/F");
    
    TT->Branch("dPhiHj1_2p5_jesdn",&dPhiHj1_2p5_jesdn,"dPhiHj1_2p5_jesdn/F");
    TT->Branch("dyHj1_2p5_jesdn",&dyHj1_2p5_jesdn,"dyHj1_2p5_jesdn/F");
    TT->Branch("mj1j2_2p5_jesdn",&mj1j2_2p5_jesdn,"mj1j2_2p5_jesdn/F");
    TT->Branch("dEtaj1j2_2p5_jesdn",&dEtaj1j2_2p5_jesdn,"dEtaj1j2_2p5_jesdn/F");
    TT->Branch("dPhij1j2_2p5_jesdn",&dPhij1j2_2p5_jesdn,"dPhij1j2_2p5_jesdn/F");
    TT->Branch("dPhiHj1j2_2p5_jesdn",&dPhiHj1j2_2p5_jesdn,"dPhiHj1j2_2p5_jesdn/F");
    TT->Branch("mass4lj_jesdn",&mass4lj_jesdn,"mass4lj_jesdn/F");
    TT->Branch("mass4ljj_jesdn",&mass4ljj_jesdn,"mass4ljj_jesdn/F");
    TT->Branch("pT4lj_jesdn",&pT4lj_jesdn,"pT4lj_jesdn/F");
    TT->Branch("pT4ljj_jesdn",&pT4ljj_jesdn,"pT4ljj_jesdn/F");

    // JES up reco
    TT->Branch("pTj1_jesup",&pTj1_jesup,"pTj1_jesup/F");
    TT->Branch("pTj1_VBF_jesup",&pTj1_VBF_jesup,"pTj1_VBF_jesup/F");
    TT->Branch("etaj1_jesup",&etaj1_jesup,"etaj1_jesup/F");
    TT->Branch("yj1_jesup",&yj1_jesup,"yj1_jesup/F");
    TT->Branch("mj1_jesup",&mj1_jesup,"mj1_jesup/F");
    TT->Branch("phij1_jesup",&phij1_jesup,"phij1_jesup/F");

    TT->Branch("pTj2_jesup",&pTj2_jesup,"pTj2_jesup/F");
    TT->Branch("etaj2_jesup",&etaj2_jesup,"etaj2_jesup/F");
    TT->Branch("yj2_jesup",&yj2_jesup,"yj2_jesup/F");
    TT->Branch("mj2_jesup",&mj2_jesup,"mj2_jesup/F");
    TT->Branch("phij2_jesup",&phij2_jesup,"phij2_jesup/F");

    TT->Branch("dPhiHj1_jesup",&dPhiHj1_jesup,"dPhiHj1_jesup/F");
    TT->Branch("dyHj1_jesup",&dyHj1_jesup,"dyHj1_jesup/F");
    TT->Branch("mj1j2_jesup",&mj1j2_jesup,"mj1j2_jesup/F");
    TT->Branch("dEtaj1j2_jesup",&dEtaj1j2_jesup,"dEtaj1j2_jesup/F");
    TT->Branch("dPhij1j2_jesup",&dPhij1j2_jesup,"dPhij1j2_jesup/F");
    TT->Branch("dPhiHj1j2_jesup",&dPhiHj1j2_jesup,"dPhiHj1j2_jesup/F");
    TT->Branch("dPhij1j2_VBF_jesup",&dPhij1j2_VBF_jesup,"dPhij1j2_VBF_jesup/F");
    TT->Branch("dPhiHj1j2_VBF_jesup",&dPhiHj1j2_VBF_jesup,"dPhiHj1j2_VBF_jesup/F");

    TT->Branch("pTj1_2p5_jesup",&pTj1_2p5_jesup,"pTj1_2p5_jesup/F");
    TT->Branch("yj1_2p5_jesup",&yj1_2p5_jesup,"yj1_2p5_jesup/F");
    TT->Branch("mj1_2p5_jesup",&mj1_2p5_jesup,"mj1_2p5_jesup/F");
    TT->Branch("etaj1_2p5_jesup",&etaj1_2p5_jesup,"etaj1_2p5_jesup/F");
    TT->Branch("phij1_2p5_jesup",&phij1_2p5_jesup,"phij1_2p5_jesup/F");

    TT->Branch("pTj2_2p5_jesup",&pTj2_2p5_jesup,"pTj2_2p5_jesup/F");
    TT->Branch("yj2_2p5_jesup",&yj2_2p5_jesup,"yj2_2p5_jesup/F");
    TT->Branch("mj2_2p5_jesup",&mj2_2p5_jesup,"mj2_2p5_jesup/F");
    TT->Branch("etaj2_2p5_jesup",&etaj2_2p5_jesup,"etaj2_2p5_jesup/F");
    TT->Branch("phij2_2p5_jesup",&phij2_2p5_jesup,"phij2_2p5_jesup/F");

    TT->Branch("dPhiHj1_2p5_jesup",&dPhiHj1_2p5_jesup,"dPhiHj1_2p5_jesup/F");
    TT->Branch("dyHj1_2p5_jesup",&dyHj1_2p5_jesup,"dyHj1_2p5_jesup/F");
    TT->Branch("mj1j2_2p5_jesup",&mj1j2_2p5_jesup,"mj1j2_2p5_jesup/F");
    TT->Branch("dEtaj1j2_2p5_jesup",&dEtaj1j2_2p5_jesup,"dEtaj1j2_2p5_jesup/F");
    TT->Branch("dPhij1j2_2p5_jesup",&dPhij1j2_2p5_jesup,"dPhij1j2_2p5_jesup/F");
    TT->Branch("dPhiHj1j2_2p5_jesup",&dPhiHj1j2_2p5_jesup,"dPhiHj1j2_2p5_jesup/F");
    TT->Branch("mass4lj_jesup",&mass4lj_jesup,"mass4lj_jesup/F");
    TT->Branch("mass4ljj_jesup",&mass4ljj_jesup,"mass4ljj_jesup/F");
    TT->Branch("pT4lj_jesup",&pT4lj_jesup,"pT4lj_jesup/F");
    TT->Branch("pT4ljj_jesup",&pT4ljj_jesup,"pT4ljj_jesup/F");

//  KD based observables
    TT->Branch("D_bkg", &D_bkg, "D_bkg/F");
    TT->Branch("D_bkg_kin", &D_bkg_kin, "D_bkg_kin/F");
    TT->Branch("D_0hp", &D_0hp, "D_0hp/F");
    TT->Branch("D_0m", &D_0m, "D_0m/F");
    TT->Branch("D_CP", &D_CP, "D_CP/F");
    TT->Branch("D_int",&D_int,"D_int/F");
    TT->Branch("D_L1",&D_L1,"D_L1/F");
    TT->Branch("D_L1_int",&D_L1_int,"D_L1_int/F");
    TT->Branch("D_L1Zg",&D_L1Zg,"D_L1Zg/F");
    TT->Branch("D_L1Zgint",&D_L1Zgint,"D_L1Zgint/F");

// Tau variables
    TT->Branch("TauB_Inc_0j_EnergyWgt",&TauB_Inc_0j_EnergyWgt,"TauB_Inc_0j_EnergyWgt/F");
    TT->Branch("TauC_Inc_0j_EnergyWgt",&TauC_Inc_0j_EnergyWgt,"TauC_Inc_0j_EnergyWgt/F");
 

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
        sigTree = new TChain("passedEvents");
        loadFakeRateHists();
    } else {
        sigTree = new TChain("Ana/passedEvents");
    }
    sigTree->Add(processFileName);

    // tree for a set of variables, for selected events
    TString fOption = "RECREATE";
    //TString fOption = "recreate";
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
//        selectionObsName = "abs(cosThetaStar)";
        selectionObsName = "cosThetaStar";
    }else if (obsName=="cosThetaStar"){
//        selectionObsName = "abs(cosThetaStar)";
        selectionObsName = "cosThetaStar";
    }else if (obsName=="cosTheta1"){
//        selectionObsName = "abs(cosTheta1)";
        selectionObsName = "cosTheta1";
    }else if (obsName=="costheta1"){
//        selectionObsName = "abs(cosTheta1)";
        selectionObsName = "cosTheta1";
    }else if (obsName=="costheta2"){
//        selectionObsName = "abs(cosTheta2)";
        selectionObsName = "cosTheta2";
    }else if (obsName=="cosTheta2"){
//        selectionObsName = "abs(cosTheta2)";
        selectionObsName = "cosTheta2";
    }else if (obsName=="Phi"){
//        selectionObsName = "abs(Phi)";
        selectionObsName = "Phi";
    }else if (obsName=="phi"){
//        selectionObsName = "abs(Phi)";
        selectionObsName = "Phi";
    }else if (obsName=="Phi1"){
//        selectionObsName = "abs(Phi1)";
        selectionObsName = "Phi1";
    }else if (obsName=="phi1"){
//        selectionObsName = "abs(Phi1)";
        selectionObsName = "Phi1";
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
    //if (obsName.Contains("jet")){ // assumes obserbale name in form "njets_pt{pt}_eta{eta}"
    //if (obsName.Contains("jet") || obsName.Contains("j1j2") || obsName.Contains("pT4lj") || obsName.Contains("mass4lj")){ // assumes obserbale name in form "njets_pt{pt}_eta{eta}"
    if (obsName.Contains("jet") || obsName.Contains("j1") || obsName.Contains("j2") || obsName.Contains("j1j2") || obsName.Contains("pT4lj") || obsName.Contains("mass4lj")){ // assumes obserbale name in form "njets_pt{pt}_eta{eta}"
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
//    h1DFRelEB    = (TH1D*) frel->Get(h1Name_FRel_EB);
//    h1DFRelEB    = (TGraphErrors*) frel->Get(FR_OS_electron_EB);
    //g1DFRelEB    = frel->Get(h1Name_FRel_EB);
    g1DFRelEB    = (TGraph*) frel->Get(g1Name_FRel_EB);
//    h1DFRelEE    = (TH1D*) frel->Get(h1Name_FRel_EE);
//    h1DFRelEE    = (TGraphErrors*) frel->Get(FR_OS_electron_EE);
    //g1DFRelEE    = frel->Get(h1Name_FRel_EE);
    g1DFRelEE    = (TGraph*) frel->Get(g1Name_FRel_EE);
//    h1DFRmuEB    = (TH1D*) frmu->Get(h1Name_FRmu_EB);
    //h1DFRmuEB    = (TGraphErrors*) frmu->Get(FR_OS_muon_EB);
    //g1DFRmuEB    = frmu->Get(h1Name_FRmu_EB);
    g1DFRmuEB    = (TGraph*) frmu->Get(g1Name_FRmu_EB);
//    h1DFRmuEE    = (TH1D*) frmu->Get(h1Name_FRmu_EE);
    //h1DFRmuEE    = (TGraphErrors*) frmu->Get(FR_OS_muon_EB);
    //g1DFRmuEE    = frmu->Get(h1Name_FRmu_EE);
    g1DFRmuEE    = (TGraph*) frmu->Get(g1Name_FRmu_EE);
}

//_______________________________________________________________________________________________________________________________________________
double getFakeRateWeight(TString lepMode, TString etaRegion, double pT) {
    // get the fake rate for given pT and eta (fake rate files must be loaded)
    double fr, frWeight;
    if (pT>=80){pT==80;}
    int bin = 0;
    if ( pT > 5 && pT <= 7 ) bin = 0;
    else if ( pT >  7 && pT <= 10 ) bin = 1;
    else if ( pT > 10 && pT <= 20 ) bin = 2;
    else if ( pT > 20 && pT <= 30 ) bin = 3;
    else if ( pT > 30 && pT <= 40 ) bin = 4;
    else if ( pT > 40 && pT <= 50 ) bin = 5;
    else if ( pT > 50 && pT <= 80 ) bin = 6;
    if (lepMode == "el") bin=bin-1; // there is no [5, 7] bin in the electron fake rate


    if (lepMode == "el" && etaRegion == "EB") {
        //fr = h1DFRelEB->GetBinContent(h1DFRelEB->FindBin(pT));
        //fr = h1DFRelEB->Eval(pT);
        fr = g1DFRelEB->GetY()[bin]; 
    } else if (lepMode == "el" && etaRegion == "EE") {
        //fr = h1DFRelEE->GetBinContent(h1DFRelEE->FindBin(pT));
        //fr = h1DFRelEE->Eval(pT);
        fr = g1DFRelEE->GetY()[bin]; 
    } else if (lepMode == "mu" && etaRegion == "EB") {
        //fr = h1DFRmuEB->GetBinContent(h1DFRmuEB->FindBin(pT));
        //fr = h1DFRmuEB->Eval(pT);
        fr = g1DFRmuEB->GetY()[bin];
    } else if (lepMode == "mu" && etaRegion == "EE") {
        //fr = h1DFRmuEE->GetBinContent(h1DFRmuEE->FindBin(pT));
        //fr = h1DFRmuEE->Eval(pT);
        fr = g1DFRmuEE->GetY()[bin];
    } else {
        fr = 0.;
    }
    // compute the fake rate factor and return it
    frWeight = (fr / (1 - fr));
//    cout<<"lepton mode and eta region are....."<<lepMode<<"and  "<<etaRegion<<endl; 
//    cout<<"pT, bin, FR and FRweight are  ......."<<pT<<", "<<bin<<", "<<fr<<"   and  "<<frWeight<<endl; 
    return frWeight;
    //cout<<"pt, FR and FRweight are  ......."<<pt<<", "<<fr<<"and  "<<frWeight<<endl; 
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

