void mass4l_unfoldwith_SM_125_logscale_asimov()
{
//=========Macro generated from canvas: c/mass4l
//=========  (Fri Sep 17 19:37:52 2021) by ROOT version6.02/05
   TCanvas *c = new TCanvas("c", "mass4l",0,0,1400,1400);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c->SetHighLightColor(2);
   c->Range(-0.923077,-1.952947,4.205128,2.49443);
   c->SetFillColor(0);
   c->SetBorderMode(0);
   c->SetBorderSize(2);
   c->SetLogy();
   c->SetTickx(1);
   c->SetTicky(1);
   c->SetLeftMargin(0.18);
   c->SetRightMargin(0.04);
   c->SetTopMargin(0.07);
   c->SetBottomMargin(0.13);
   c->SetFrameFillStyle(0);
   c->SetFrameBorderMode(0);
   c->SetFrameFillStyle(0);
   c->SetFrameBorderMode(0);
   
   TH1D *dummy1 = new TH1D("dummy1","dummy",4,0,4);
   dummy1->SetBinContent(1,6.929326);
   dummy1->SetBinContent(2,6.929326);
   dummy1->SetBinContent(3,6.929326);
   dummy1->SetBinContent(4,6.929326);
   dummy1->SetMinimum(0.0421902);
   dummy1->SetMaximum(152.4452);
   dummy1->SetEntries(4);
   dummy1->SetLineColor(0);
   dummy1->SetLineStyle(0);
   dummy1->SetLineWidth(0);
   dummy1->SetMarkerColor(0);
   dummy1->SetMarkerSize(0);
   dummy1->GetXaxis()->SetBinLabel(1,"4l");
   dummy1->GetXaxis()->SetBinLabel(2,"2e2#mu");
   dummy1->GetXaxis()->SetBinLabel(3,"4#mu");
   dummy1->GetXaxis()->SetBinLabel(4,"4e");
   dummy1->GetXaxis()->SetLabelFont(42);
   dummy1->GetXaxis()->SetLabelOffset(0.007);
   dummy1->GetXaxis()->SetLabelSize(0.08);
   dummy1->GetXaxis()->SetTitleSize(0);
   dummy1->GetXaxis()->SetTitleOffset(0.9);
   dummy1->GetXaxis()->SetTitleFont(42);
   dummy1->GetYaxis()->SetTitle("#sigma_{fid} (fb)");
   dummy1->GetYaxis()->SetLabelFont(42);
   dummy1->GetYaxis()->SetLabelOffset(0.007);
   dummy1->GetYaxis()->SetTitleSize(0.06);
   dummy1->GetYaxis()->SetTitleOffset(1.4);
   dummy1->GetYaxis()->SetTitleFont(42);
   dummy1->GetZaxis()->SetLabelFont(42);
   dummy1->GetZaxis()->SetLabelOffset(0.007);
   dummy1->GetZaxis()->SetLabelSize(0.05);
   dummy1->GetZaxis()->SetTitleSize(0.06);
   dummy1->GetZaxis()->SetTitleFont(42);
   dummy1->Draw("hist");
   
   TLegend *leg = new TLegend(0.28,0.65,0.85,0.9,NULL,"brNDC");
   leg->SetBorderSize(1);
   leg->SetTextSize(0.025);
   leg->SetLineColor(0);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(1001);
   TLegendEntry *entry=leg->AddEntry("","Toy Data (stat. #oplus sys. unc.)","ep");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1.4);
   entry->SetTextFont(42);
   entry=leg->AddEntry("","Systematic uncertainty","l");

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#ff0000");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(5);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("","gg#rightarrowH (NNLOPS) + XH","lf");

   ci = TColor::GetColor("#cc6600");
   entry->SetFillColor(ci);
   entry->SetFillStyle(3245);

   ci = TColor::GetColor("#cc6600");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("","gg#rightarrowH (POWHEG) + XH","lf");

   ci = TColor::GetColor("#0066cc");
   entry->SetFillColor(ci);
   entry->SetFillStyle(3254);

   ci = TColor::GetColor("#0066cc");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("h_XH","XH = VBF + VH + ttH (POWHEG)","f");

   ci = TColor::GetColor("#99cc99");
   entry->SetFillColor(ci);
   entry->SetFillStyle(3344);
   entry->SetLineColor(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("dummy","(LHC HXSWG YR4, m_{H}=125.09 GeV)","");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   leg->Draw();
   
   TH1D *h_ggH_powheg2 = new TH1D("h_ggH_powheg2","h_ggH_powheg",4,0,4);
   h_ggH_powheg2->SetBinContent(1,2.77173);
   h_ggH_powheg2->SetBinContent(2,1.295587);
   h_ggH_powheg2->SetBinContent(3,0.7748361);
   h_ggH_powheg2->SetBinContent(4,0.7013121);
   h_ggH_powheg2->SetEntries(4);

   ci = TColor::GetColor("#0066cc");
   h_ggH_powheg2->SetLineColor(ci);
   h_ggH_powheg2->SetLineStyle(0);
   h_ggH_powheg2->SetLineWidth(2);
   h_ggH_powheg2->GetXaxis()->SetLabelFont(42);
   h_ggH_powheg2->GetXaxis()->SetLabelOffset(0.007);
   h_ggH_powheg2->GetXaxis()->SetLabelSize(0.05);
   h_ggH_powheg2->GetXaxis()->SetTitleSize(0.06);
   h_ggH_powheg2->GetXaxis()->SetTitleOffset(0.9);
   h_ggH_powheg2->GetXaxis()->SetTitleFont(42);
   h_ggH_powheg2->GetYaxis()->SetLabelFont(42);
   h_ggH_powheg2->GetYaxis()->SetLabelOffset(0.007);
   h_ggH_powheg2->GetYaxis()->SetLabelSize(0.05);
   h_ggH_powheg2->GetYaxis()->SetTitleSize(0.06);
   h_ggH_powheg2->GetYaxis()->SetTitleOffset(1.25);
   h_ggH_powheg2->GetYaxis()->SetTitleFont(42);
   h_ggH_powheg2->GetZaxis()->SetLabelFont(42);
   h_ggH_powheg2->GetZaxis()->SetLabelOffset(0.007);
   h_ggH_powheg2->GetZaxis()->SetLabelSize(0.05);
   h_ggH_powheg2->GetZaxis()->SetTitleSize(0.06);
   h_ggH_powheg2->GetZaxis()->SetTitleFont(42);
   h_ggH_powheg2->Draw("histsame");
   
   TH1D *h_ggH_minloHJ3 = new TH1D("h_ggH_minloHJ3","h_ggH_minloHJ",4,0,4);
   h_ggH_minloHJ3->SetBinContent(1,2.762851);
   h_ggH_minloHJ3->SetBinContent(2,1.302437);
   h_ggH_minloHJ3->SetBinContent(3,0.7619546);
   h_ggH_minloHJ3->SetBinContent(4,0.6984598);
   h_ggH_minloHJ3->SetEntries(4);

   ci = TColor::GetColor("#cc6600");
   h_ggH_minloHJ3->SetLineColor(ci);
   h_ggH_minloHJ3->SetLineStyle(0);
   h_ggH_minloHJ3->SetLineWidth(2);
   h_ggH_minloHJ3->GetXaxis()->SetLabelFont(42);
   h_ggH_minloHJ3->GetXaxis()->SetLabelOffset(0.007);
   h_ggH_minloHJ3->GetXaxis()->SetLabelSize(0.05);
   h_ggH_minloHJ3->GetXaxis()->SetTitleSize(0.06);
   h_ggH_minloHJ3->GetXaxis()->SetTitleOffset(0.9);
   h_ggH_minloHJ3->GetXaxis()->SetTitleFont(42);
   h_ggH_minloHJ3->GetYaxis()->SetLabelFont(42);
   h_ggH_minloHJ3->GetYaxis()->SetLabelOffset(0.007);
   h_ggH_minloHJ3->GetYaxis()->SetLabelSize(0.05);
   h_ggH_minloHJ3->GetYaxis()->SetTitleSize(0.06);
   h_ggH_minloHJ3->GetYaxis()->SetTitleOffset(1.25);
   h_ggH_minloHJ3->GetYaxis()->SetTitleFont(42);
   h_ggH_minloHJ3->GetZaxis()->SetLabelFont(42);
   h_ggH_minloHJ3->GetZaxis()->SetLabelOffset(0.007);
   h_ggH_minloHJ3->GetZaxis()->SetLabelSize(0.05);
   h_ggH_minloHJ3->GetZaxis()->SetTitleSize(0.06);
   h_ggH_minloHJ3->GetZaxis()->SetTitleFont(42);
   h_ggH_minloHJ3->Draw("histsame");
   
   Double_t _fx3001[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3001[4] = {
   2.77173,
   1.295587,
   0.7748361,
   0.7013121};
   Double_t _felx3001[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fely3001[4] = {
   0.145604,
   0.06806403,
   0.04070787,
   0.03683206};
   Double_t _fehx3001[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fehy3001[4] = {
   0.145604,
   0.06806403,
   0.04070787,
   0.03683206};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(4,_fx3001,_fy3001,_felx3001,_fehx3001,_fely3001,_fehy3001);
   grae->SetName("");
   grae->SetTitle("");

   ci = TColor::GetColor("#0066cc");
   grae->SetFillColor(ci);
   grae->SetFillStyle(3254);

   ci = TColor::GetColor("#0066cc");
   grae->SetLineColor(ci);
   grae->SetLineWidth(2);

   ci = TColor::GetColor("#0066cc");
   grae->SetMarkerColor(ci);
   
   TH1F *Graph_Graph3001 = new TH1F("Graph_Graph3001","",100,0,4.4);
   Graph_Graph3001->SetMinimum(0.4391946);
   Graph_Graph3001->SetMaximum(3.14262);
   Graph_Graph3001->SetDirectory(0);
   Graph_Graph3001->SetStats(0);
   Graph_Graph3001->SetLineStyle(0);
   Graph_Graph3001->GetXaxis()->SetLabelFont(42);
   Graph_Graph3001->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3001->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3001->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3001->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3001->GetXaxis()->SetTitleFont(42);
   Graph_Graph3001->GetYaxis()->SetLabelFont(42);
   Graph_Graph3001->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3001->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3001->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3001->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3001->GetYaxis()->SetTitleFont(42);
   Graph_Graph3001->GetZaxis()->SetLabelFont(42);
   Graph_Graph3001->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3001->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3001->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3001);
   
   grae->Draw("5");
   
   Double_t _fx3002[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3002[4] = {
   2.77173,
   1.295587,
   0.7748361,
   0.7013121};
   Double_t _felx3002[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fely3002[4] = {
   0.145604,
   0.06806403,
   0.04070787,
   0.03683206};
   Double_t _fehx3002[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fehy3002[4] = {
   0.145604,
   0.06806403,
   0.04070787,
   0.03683206};
   grae = new TGraphAsymmErrors(4,_fx3002,_fy3002,_felx3002,_fehx3002,_fely3002,_fehy3002);
   grae->SetName("");
   grae->SetTitle("");

   ci = TColor::GetColor("#0066cc");
   grae->SetFillColor(ci);
   grae->SetFillStyle(0);

   ci = TColor::GetColor("#0066cc");
   grae->SetLineColor(ci);

   ci = TColor::GetColor("#0066cc");
   grae->SetMarkerColor(ci);
   
   TH1F *Graph_Graph3002 = new TH1F("Graph_Graph3002","",100,0,4.4);
   Graph_Graph3002->SetMinimum(0.4391946);
   Graph_Graph3002->SetMaximum(3.14262);
   Graph_Graph3002->SetDirectory(0);
   Graph_Graph3002->SetStats(0);
   Graph_Graph3002->SetLineStyle(0);
   Graph_Graph3002->GetXaxis()->SetLabelFont(42);
   Graph_Graph3002->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3002->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3002->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3002->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3002->GetXaxis()->SetTitleFont(42);
   Graph_Graph3002->GetYaxis()->SetLabelFont(42);
   Graph_Graph3002->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3002->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3002->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3002->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3002->GetYaxis()->SetTitleFont(42);
   Graph_Graph3002->GetZaxis()->SetLabelFont(42);
   Graph_Graph3002->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3002->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3002->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3002->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3002);
   
   grae->Draw("5");
   
   Double_t _fx3003[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3003[4] = {
   2.762851,
   1.302437,
   0.7619546,
   0.6984598};
   Double_t _felx3003[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fely3003[4] = {
   0.1450916,
   0.06845904,
   0.03996502,
   0.03666757};
   Double_t _fehx3003[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fehy3003[4] = {
   0.1450916,
   0.06845904,
   0.03996502,
   0.03666757};
   grae = new TGraphAsymmErrors(4,_fx3003,_fy3003,_felx3003,_fehx3003,_fely3003,_fehy3003);
   grae->SetName("");
   grae->SetTitle("");

   ci = TColor::GetColor("#cc6600");
   grae->SetFillColor(ci);
   grae->SetFillStyle(3245);

   ci = TColor::GetColor("#cc6600");
   grae->SetLineColor(ci);
   grae->SetLineWidth(2);

   ci = TColor::GetColor("#cc6600");
   grae->SetMarkerColor(ci);
   
   TH1F *Graph_Graph3003 = new TH1F("Graph_Graph3003","",100,0,4.4);
   Graph_Graph3003->SetMinimum(0.4371772);
   Graph_Graph3003->SetMaximum(3.132558);
   Graph_Graph3003->SetDirectory(0);
   Graph_Graph3003->SetStats(0);
   Graph_Graph3003->SetLineStyle(0);
   Graph_Graph3003->GetXaxis()->SetLabelFont(42);
   Graph_Graph3003->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3003->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3003->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3003->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3003->GetXaxis()->SetTitleFont(42);
   Graph_Graph3003->GetYaxis()->SetLabelFont(42);
   Graph_Graph3003->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3003->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3003->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3003->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3003->GetYaxis()->SetTitleFont(42);
   Graph_Graph3003->GetZaxis()->SetLabelFont(42);
   Graph_Graph3003->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3003->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3003->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3003->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3003);
   
   grae->Draw("5");
   
   Double_t _fx3004[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3004[4] = {
   2.762851,
   1.302437,
   0.7619546,
   0.6984598};
   Double_t _felx3004[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fely3004[4] = {
   0.1450916,
   0.06845904,
   0.03996502,
   0.03666757};
   Double_t _fehx3004[4] = {
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t _fehy3004[4] = {
   0.1450916,
   0.06845904,
   0.03996502,
   0.03666757};
   grae = new TGraphAsymmErrors(4,_fx3004,_fy3004,_felx3004,_fehx3004,_fely3004,_fehy3004);
   grae->SetName("");
   grae->SetTitle("");

   ci = TColor::GetColor("#cc6600");
   grae->SetFillColor(ci);
   grae->SetFillStyle(0);

   ci = TColor::GetColor("#cc6600");
   grae->SetLineColor(ci);

   ci = TColor::GetColor("#cc6600");
   grae->SetMarkerColor(ci);
   
   TH1F *Graph_Graph3004 = new TH1F("Graph_Graph3004","",100,0,4.4);
   Graph_Graph3004->SetMinimum(0.4371772);
   Graph_Graph3004->SetMaximum(3.132558);
   Graph_Graph3004->SetDirectory(0);
   Graph_Graph3004->SetStats(0);
   Graph_Graph3004->SetLineStyle(0);
   Graph_Graph3004->GetXaxis()->SetLabelFont(42);
   Graph_Graph3004->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3004->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3004->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3004->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3004->GetXaxis()->SetTitleFont(42);
   Graph_Graph3004->GetYaxis()->SetLabelFont(42);
   Graph_Graph3004->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3004->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3004->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3004->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3004->GetYaxis()->SetTitleFont(42);
   Graph_Graph3004->GetZaxis()->SetLabelFont(42);
   Graph_Graph3004->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3004->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3004->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3004->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3004);
   
   grae->Draw("5");
   
   TH1D *h_XH4 = new TH1D("h_XH4","h_XH",4,0,4);
   h_XH4->SetBinContent(1,0.3233113);
   h_XH4->SetBinContent(2,0.1510891);
   h_XH4->SetBinContent(3,0.09020494);
   h_XH4->SetBinContent(4,0.0820173);
   h_XH4->SetEntries(4);

   ci = TColor::GetColor("#99cc99");
   h_XH4->SetFillColor(ci);
   h_XH4->SetFillStyle(3344);
   h_XH4->SetLineStyle(0);
   h_XH4->GetXaxis()->SetLabelFont(42);
   h_XH4->GetXaxis()->SetLabelOffset(0.007);
   h_XH4->GetXaxis()->SetLabelSize(0.05);
   h_XH4->GetXaxis()->SetTitleSize(0.06);
   h_XH4->GetXaxis()->SetTitleOffset(0.9);
   h_XH4->GetXaxis()->SetTitleFont(42);
   h_XH4->GetYaxis()->SetLabelFont(42);
   h_XH4->GetYaxis()->SetLabelOffset(0.007);
   h_XH4->GetYaxis()->SetLabelSize(0.05);
   h_XH4->GetYaxis()->SetTitleSize(0.06);
   h_XH4->GetYaxis()->SetTitleOffset(1.25);
   h_XH4->GetYaxis()->SetTitleFont(42);
   h_XH4->GetZaxis()->SetLabelFont(42);
   h_XH4->GetZaxis()->SetLabelOffset(0.007);
   h_XH4->GetZaxis()->SetLabelSize(0.05);
   h_XH4->GetZaxis()->SetTitleSize(0.06);
   h_XH4->GetZaxis()->SetTitleFont(42);
   h_XH4->Draw("histsame");
   
   Double_t _fx3005[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3005[4] = {
   2.769,
   1.296,
   0.775,
   0.702};
   Double_t _felx3005[4] = {
   0,
   0,
   0,
   0};
   Double_t _fely3005[4] = {
   0.389,
   0.243,
   0.15,
   0.201};
   Double_t _fehx3005[4] = {
   0,
   0,
   0,
   0};
   Double_t _fehy3005[4] = {
   0.429,
   0.269,
   0.169,
   0.241};
   grae = new TGraphAsymmErrors(4,_fx3005,_fy3005,_felx3005,_fehx3005,_fely3005,_fehy3005);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);
   grae->SetLineWidth(2);
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(1.4);
   
   TH1F *Graph_Graph3005 = new TH1F("Graph_Graph3005","",100,0.2,3.8);
   Graph_Graph3005->SetMinimum(0.2313);
   Graph_Graph3005->SetMaximum(3.4677);
   Graph_Graph3005->SetDirectory(0);
   Graph_Graph3005->SetStats(0);
   Graph_Graph3005->SetLineStyle(0);
   Graph_Graph3005->GetXaxis()->SetLabelFont(42);
   Graph_Graph3005->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3005->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3005->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3005->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3005->GetXaxis()->SetTitleFont(42);
   Graph_Graph3005->GetYaxis()->SetLabelFont(42);
   Graph_Graph3005->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3005->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3005->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3005->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3005->GetYaxis()->SetTitleFont(42);
   Graph_Graph3005->GetZaxis()->SetLabelFont(42);
   Graph_Graph3005->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3005->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3005->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3005->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3005);
   
   grae->Draw("pz0");
   
   Double_t _fx3006[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3006[4] = {
   2.769,
   1.296,
   0.775,
   0.702};
   Double_t _felx3006[4] = {
   0,
   0,
   0,
   0};
   Double_t _fely3006[4] = {
   0.2091339,
   0.09860527,
   0.05657738,
   0.07619055};
   Double_t _fehx3006[4] = {
   0,
   0,
   0,
   0};
   Double_t _fehy3006[4] = {
   0.2480746,
   0.1172305,
   0.06734983,
   0.1105939};
   grae = new TGraphAsymmErrors(4,_fx3006,_fy3006,_felx3006,_fehx3006,_fely3006,_fehy3006);
   grae->SetName("");
   grae->SetTitle("");

   ci = TColor::GetColor("#ff0000");
   grae->SetFillColor(ci);

   ci = TColor::GetColor("#ff0000");
   grae->SetLineColor(ci);
   grae->SetLineWidth(5);

   ci = TColor::GetColor("#ff0000");
   grae->SetMarkerColor(ci);
   
   TH1F *Graph_Graph3006 = new TH1F("Graph_Graph3006","",100,0.2,3.8);
   Graph_Graph3006->SetMinimum(0.3866829);
   Graph_Graph3006->SetMaximum(3.256201);
   Graph_Graph3006->SetDirectory(0);
   Graph_Graph3006->SetStats(0);
   Graph_Graph3006->SetLineStyle(0);
   Graph_Graph3006->GetXaxis()->SetLabelFont(42);
   Graph_Graph3006->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3006->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3006->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3006->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3006->GetXaxis()->SetTitleFont(42);
   Graph_Graph3006->GetYaxis()->SetLabelFont(42);
   Graph_Graph3006->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3006->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3006->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3006->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3006->GetYaxis()->SetTitleFont(42);
   Graph_Graph3006->GetZaxis()->SetLabelFont(42);
   Graph_Graph3006->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3006->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3006->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3006->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3006);
   
   grae->Draw("pz0");
   
   Double_t _fx3007[4] = {
   0.5,
   1.5,
   2.5,
   3.5};
   Double_t _fy3007[4] = {
   2.769,
   1.296,
   0.775,
   0.702};
   Double_t _felx3007[4] = {
   0,
   0,
   0,
   0};
   Double_t _fely3007[4] = {
   0,
   0,
   0,
   0};
   Double_t _fehx3007[4] = {
   0,
   0,
   0,
   0};
   Double_t _fehy3007[4] = {
   0,
   0,
   0,
   0};
   grae = new TGraphAsymmErrors(4,_fx3007,_fy3007,_felx3007,_fehx3007,_fely3007,_fehy3007);
   grae->SetName("");
   grae->SetTitle("");
   grae->SetFillColor(1);
   grae->SetLineWidth(2);
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(1.4);
   
   TH1F *Graph_Graph3007 = new TH1F("Graph_Graph3007","",100,0.2,3.8);
   Graph_Graph3007->SetMinimum(0.4953);
   Graph_Graph3007->SetMaximum(2.9757);
   Graph_Graph3007->SetDirectory(0);
   Graph_Graph3007->SetStats(0);
   Graph_Graph3007->SetLineStyle(0);
   Graph_Graph3007->GetXaxis()->SetLabelFont(42);
   Graph_Graph3007->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph3007->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph3007->GetXaxis()->SetTitleSize(0.06);
   Graph_Graph3007->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph3007->GetXaxis()->SetTitleFont(42);
   Graph_Graph3007->GetYaxis()->SetLabelFont(42);
   Graph_Graph3007->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph3007->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph3007->GetYaxis()->SetTitleSize(0.06);
   Graph_Graph3007->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph3007->GetYaxis()->SetTitleFont(42);
   Graph_Graph3007->GetZaxis()->SetLabelFont(42);
   Graph_Graph3007->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph3007->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph3007->GetZaxis()->SetTitleSize(0.06);
   Graph_Graph3007->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph3007);
   
   grae->Draw("p");
   TLatex *   tex = new TLatex(0.94,0.94,"58.8 fb^{-1} (13 TeV)");
tex->SetNDC();
   tex->SetTextAlign(31);
   tex->SetTextFont(42);
   tex->SetTextSize(0.035);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.19,0.94,"CMS");
tex->SetNDC();
   tex->SetTextSize(0.049);
   tex->SetLineWidth(2);
   tex->Draw();
   
   TH1D *dummy5 = new TH1D("dummy5","dummy",4,0,4);
   dummy5->SetBinContent(1,6.929326);
   dummy5->SetBinContent(2,6.929326);
   dummy5->SetBinContent(3,6.929326);
   dummy5->SetBinContent(4,6.929326);
   dummy5->SetMinimum(0.0421902);
   dummy5->SetMaximum(152.4452);
   dummy5->SetEntries(4);
   dummy5->SetLineColor(0);
   dummy5->SetLineStyle(0);
   dummy5->SetLineWidth(0);
   dummy5->SetMarkerColor(0);
   dummy5->SetMarkerSize(0);
   dummy5->GetXaxis()->SetBinLabel(1,"4l");
   dummy5->GetXaxis()->SetBinLabel(2,"2e2#mu");
   dummy5->GetXaxis()->SetBinLabel(3,"4#mu");
   dummy5->GetXaxis()->SetBinLabel(4,"4e");
   dummy5->GetXaxis()->SetLabelFont(42);
   dummy5->GetXaxis()->SetLabelOffset(0.007);
   dummy5->GetXaxis()->SetLabelSize(0.08);
   dummy5->GetXaxis()->SetTitleSize(0);
   dummy5->GetXaxis()->SetTitleOffset(0.9);
   dummy5->GetXaxis()->SetTitleFont(42);
   dummy5->GetYaxis()->SetTitle("#sigma_{fid} (fb)");
   dummy5->GetYaxis()->SetLabelFont(42);
   dummy5->GetYaxis()->SetLabelOffset(0.007);
   dummy5->GetYaxis()->SetTitleSize(0.06);
   dummy5->GetYaxis()->SetTitleOffset(1.4);
   dummy5->GetYaxis()->SetTitleFont(42);
   dummy5->GetZaxis()->SetLabelFont(42);
   dummy5->GetZaxis()->SetLabelOffset(0.007);
   dummy5->GetZaxis()->SetLabelSize(0.05);
   dummy5->GetZaxis()->SetTitleSize(0.06);
   dummy5->GetZaxis()->SetTitleFont(42);
   dummy5->Draw("axissame");
   c->Modified();
   c->cd();
   c->SetSelected(c);
}
