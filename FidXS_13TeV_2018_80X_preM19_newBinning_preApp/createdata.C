#include <TFile.h>
#include <TTree.h>
#include <iostream>

void createdata(bool useRefit=false) {

   TFile *oldfile = new TFile("Data_Mar14_bestCandLegacy_NoDuplicates.root","READ");

   TTree *oldtree = (TTree*)oldfile->Get("passedEvents");

   ULong64_t Run;
   oldtree->SetBranchAddress("Run",&Run);
   ULong64_t LumiSect;
   oldtree->SetBranchAddress("LumiSect",&LumiSect);
   ULong64_t Event;
   oldtree->SetBranchAddress("Event",&Event);

   Bool_t passedFullSelection;
   oldtree->SetBranchAddress("passedFullSelection",&passedFullSelection);

   Float_t mass4l;
   oldtree->SetBranchAddress("mass4l",&mass4l);
   Float_t mass4lErr;
   oldtree->SetBranchAddress("mass4lErr",&mass4lErr);
   Float_t mass4lREFIT;
   oldtree->SetBranchAddress("mass4lREFIT",&mass4lREFIT);
   Float_t mass4lErrREFIT;
   oldtree->SetBranchAddress("mass4lErrREFIT",&mass4lErrREFIT);
   Float_t mass4e;
   oldtree->SetBranchAddress("mass4e",&mass4e);
   Float_t mass4mu;
   oldtree->SetBranchAddress("mass4mu",&mass4mu);
   Float_t mass2e2mu;
   oldtree->SetBranchAddress("mass2e2mu",&mass2e2mu);

   Float_t pT4l;
   oldtree->SetBranchAddress("pT4l",&pT4l);
   Float_t rapidity4l;
   oldtree->SetBranchAddress("rapidity4l",&rapidity4l);
   /*
   Float_t massZ1;
   oldtree->SetBranchAddress("massZ1",&massZ1);
   Float_t massZ2;
   oldtree->SetBranchAddress("massZ2",&massZ2);
   Float_t rapidity4l;
   oldtree->SetBranchAddress("rapidity4l",&rapidity4l);
   Float_t cosThetaStar;
   oldtree->SetBranchAddress("cosThetaStar",&cosThetaStar);
   Float_t cosTheta1;
   oldtree->SetBranchAddress("cosTheta1",&cosTheta1);
   Float_t cosTheta2;
   oldtree->SetBranchAddress("cosTheta2",&cosTheta2);
   Float_t Phi;
   oldtree->SetBranchAddress("Phi",&Phi);
   Float_t Phi1;
   oldtree->SetBranchAddress("Phi1",&Phi1);
   */
   Int_t njets_pt30_eta4p7;
   oldtree->SetBranchAddress("njets_pt30_eta4p7",&njets_pt30_eta4p7);
   Int_t njets_pt30_eta2p5;
   oldtree->SetBranchAddress("njets_pt30_eta2p5",&njets_pt30_eta2p5);
   Float_t pt_leadingjet_pt30_eta4p7;
   oldtree->SetBranchAddress("pt_leadingjet_pt30_eta4p7",&pt_leadingjet_pt30_eta4p7);
   Float_t pt_leadingjet_pt30_eta2p5;
   oldtree->SetBranchAddress("pt_leadingjet_pt30_eta2p5",&pt_leadingjet_pt30_eta2p5);

   Int_t finalState;
   oldtree->SetBranchAddress("finalState",&finalState);

   Float_t D_bkg_kin;
   oldtree->SetBranchAddress("D_bkg_kin",&D_bkg_kin);
  
   std::vector<ULong64_t> runVec, lumiVec, eventVec;

   TFile *newfile = new TFile("data_13TeV_2018_Mar14.root","recreate");
   TTree *newtree = new TTree("passedEvents","passedEvents");
   
   Float_t CMS_zz4l_mass;
   Float_t CMS_zz4l_massErr;
   Float_t melaLD;
   newtree->Branch("CMS_zz4l_mass",&CMS_zz4l_mass);
   newtree->Branch("CMS_zz4l_massErr",&CMS_zz4l_massErr);
   newtree->Branch("melaLD",&melaLD);
   newtree->Branch("mass4e",&mass4e);
   newtree->Branch("mass4mu",&mass4mu);
   newtree->Branch("mass2e2mu",&mass2e2mu);
   newtree->Branch("pT4l",&pT4l);
   newtree->Branch("rapidity4l",&rapidity4l);
   /**
   newtree->Branch("massZ1",&massZ1);
   newtree->Branch("massZ2",&massZ2);
   newtree->Branch("rapidity4l",&rapidity4l);
   newtree->Branch("cosThetaStar",&cosThetaStar);
   newtree->Branch("cosTheta1",&cosTheta1);
   newtree->Branch("cosTheta2",&cosTheta2);
   newtree->Branch("Phi",&Phi);
   newtree->Branch("Phi1",&Phi1);
   */
   newtree->Branch("njets_pt30_eta4p7",&njets_pt30_eta4p7);
   newtree->Branch("njets_pt30_eta2p5",&njets_pt30_eta2p5);
   newtree->Branch("pt_leadingjet_pt30_eta4p7",&pt_leadingjet_pt30_eta4p7);
   newtree->Branch("pt_leadingjet_pt30_eta2p5",&pt_leadingjet_pt30_eta2p5);
   newtree->Branch("finalState",&finalState);

   int n4e = 0;
   int n2e2mu = 0;
   int n4mu = 0;

   int nEntries = oldtree->GetEntries();

   std::cout<<"using refit? "<<useRefit<<std::endl;

   for(int i = 0; i < oldtree->GetEntries(); i++) {

       oldtree->GetEntry(i);

       if (i%1000==0) std::cout<<i<<"/"<<nEntries<<std::endl;

       if (!passedFullSelection) continue;

       if (useRefit) {
           CMS_zz4l_mass = mass4lREFIT;
           CMS_zz4l_massErr = mass4lErrREFIT;           
           if (mass4e>0.0) mass4e = mass4lREFIT;
           if (mass4mu>0.0) mass4mu = mass4lREFIT;
           if (mass2e2mu>0.0) mass2e2mu = mass4lREFIT;
       }
       else {
           CMS_zz4l_mass = mass4l;
           CMS_zz4l_massErr = mass4lErr;
       }

       melaLD = D_bkg_kin;

       if (mass4e>105.0 && mass4e<140.0) n4e++;
       if (mass4mu>105.0 && mass4mu<140.0) n4mu++;
       if (mass2e2mu>105.0 && mass2e2mu<140.0) n2e2mu++;
      
       newtree->Fill();

   }

   std::cout<<"105.0-140.0: "<<n4e<<" 4e, "<<n4mu<<" 4mu, "<<n2e2mu<<" 2e2mu."<<std::endl;

   newfile->Write();

}
