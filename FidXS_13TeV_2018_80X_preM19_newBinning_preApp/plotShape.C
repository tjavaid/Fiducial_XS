
void plotShape() {
    TFile *sig = TFile::Open("");
    RooWorkspace *w = (RooWorkspace*)sig-&gt;Get("w");  // necessary to Get the workspace in ROOT6 to avoid reloading
                                           
   
    w->var("MH")->setVal(125.7);
    RooAbsPdf *ggH = w->pdf("shapeSig_trueH2e2muBin0_ch3");
    
// prepare the canvas
    RooPlot *plot =  w->var("CMS_hgg_mass")->frame();
    
// plot nominal pdf
    ggH->plotOn(plot, RooFit::LineColor(kBlack));
    
// plot minus 3 sigma pdf
    w->var("CMS_zz4l_mean_m_sig")->setVal(-3*0.004717);
    ggH->plotOn(plot, RooFit::LineColor(kBlue));
    
// plot plus 3 sigma pdf
    w->var("CMS_zz4l_mean_m_sig")->setVal(+3*0.004717);
    ggH->plotOn(plot, RooFit::LineColor(kRed));
    plot->Draw();
    
