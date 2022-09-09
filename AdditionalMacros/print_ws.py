from ROOT import *

Year = '2018'
Channel = '4mu'
Name = Year + ": "+Channel
legend =  TLegend(0.7,0.7,0.98,0.9);
legend.SetHeader(Name,"C");

# File 1 to compare
f_xBF = TFile('/eos/user/r/rasharma/www/h4l/HIG_21_009/Sept6_2022/xs_125.0_'+Year+'/hzz4l_'+Channel+'S_13TeV_xs_SM_125_mass4l_v3.Databin0.root','READ')
w_xBF = f_xBF.Get("w")
# w_xBF.Print()

# File 2 to compare
f_LLR = TFile('../LLR_'+Year+'_hzz4l_'+Channel+'S_13TeV_xs_SM_125_mass4l_v3.Databin0.root','READ')
w_LLR = f_LLR.Get("w")
# w_LLR.Print()


"""
# Compare file1  and file2 RooRealVars
print("|{0:30} | {1:15} | {2:15} | ".format("RooRealVar", "xBF", "LLR"))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("CMS_zz4l_mass: ",w_xBF.var("CMS_zz4l_mass").getVal(), w_LLR.var("CMS_zz4l_mass").getVal(), abs(w_LLR.var("CMS_zz4l_mass").getVal() - w_xBF.var("CMS_zz4l_mass").getVal())/w_LLR.var("CMS_zz4l_mass").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("CMS_zz4l_mean_m_err_1_2017:",w_xBF.var("CMS_zz4l_mean_m_err_1_2017").getVal(), w_LLR.var("CMS_zz4l_mean_m_err").getVal(), abs(w_LLR.var("CMS_zz4l_mean_m_err").getVal() - w_xBF.var("CMS_zz4l_mean_m_err_1_2017").getVal())/w_LLR.var("CMS_zz4l_mean_m_err").getVal()))
# print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("CMS_zz4l_mean_m_sig: ",w_xBF.var("CMS_zz4l_mean_m_sig").getVal(), w_LLR.var("CMS_zz4l_mean_m_sig").getVal(), abs(w_LLR.var("CMS_zz4l_mean_m_sig").getVal() - w_xBF.var("CMS_zz4l_mean_m_sig").getVal())/w_LLR.var("CMS_zz4l_mean_m_sig").getVal()))
# print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("CMS_zz4l_n_sig_1_2017: ",w_xBF.var("CMS_zz4l_n_sig_1_2017").getVal(), w_LLR.var("CMS_zz4l_n_sig_1_2017").getVal(), abs(w_LLR.var("CMS_zz4l_n_sig_1_2017").getVal() - w_xBF.var("CMS_zz4l_n_sig_1_2017").getVal())/w_LLR.var("CMS_zz4l_n_sig_1_2017").getVal()))
# print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("CMS_zz4l_sigma_m_sig:",w_xBF.var("CMS_zz4l_sigma_m_sig").getVal(), w_LLR.var("CMS_zz4l_sigma_m_sig").getVal(), abs(w_LLR.var("CMS_zz4l_sigma_m_sig").getVal() - w_xBF.var("CMS_zz4l_sigma_m_sig").getVal())/w_LLR.var("CMS_zz4l_sigma_m_sig").getVal()))
# print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("K1Bin0:",w_xBF.var("K1Bin0").getVal(), w_LLR.var("K1Bin0").getVal(), abs(w_LLR.var("K1Bin0").getVal() - w_xBF.var("K1Bin0").getVal())/w_LLR.var("K1Bin0").getVal()))
# print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("K2Bin0:",w_xBF.var("K2Bin0").getVal(), w_LLR.var("K2Bin0").getVal(), abs(w_LLR.var("K2Bin0").getVal() - w_xBF.var("K2Bin0").getVal())/w_LLR.var("K2Bin0").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("MH:",w_xBF.var("MH").getVal(), w_LLR.var("MH").getVal(), abs(w_LLR.var("MH").getVal() - w_xBF.var("MH").getVal())/w_LLR.var("MH").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("effBin0_recobin0_4mu_2017: ",w_xBF.var("effBin0_recobin0_4mu_2017").getVal(), w_LLR.var("eff_hzz_smH_mass4l_13TeV_105p0_160p0_hzz_mass4l_105p0_160p0_cat4mu").getVal(), abs(w_LLR.var("eff_hzz_smH_mass4l_13TeV_105p0_160p0_hzz_mass4l_105p0_160p0_cat4mu").getVal() - w_xBF.var("effBin0_recobin0_4mu_2017").getVal())/w_LLR.var("eff_hzz_smH_mass4l_13TeV_105p0_160p0_hzz_mass4l_105p0_160p0_cat4mu").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("fracSM4eBin0:",w_xBF.var("fracSM4eBin0").getVal(), w_LLR.var("fracSM4eBin0").getVal(), abs(w_LLR.var("fracSM4eBin0").getVal() - w_xBF.var("fracSM4eBin0").getVal())/w_LLR.var("fracSM4eBin0").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("fracSM4muBin0: ",w_xBF.var("fracSM4muBin0").getVal(), w_LLR.var("fracSM4muBin0").getVal(), abs(w_LLR.var("fracSM4muBin0").getVal() - w_xBF.var("fracSM4muBin0").getVal())/w_LLR.var("fracSM4muBin0").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("frac_ggzz_recobin0_4mu_2017: ",w_xBF.var("frac_ggzz_recobin0_4mu_2017").getVal(), w_LLR.var("frac_ggzz_recobin0_4mu_2017").getVal(), abs(w_LLR.var("frac_ggzz_recobin0_4mu_2017").getVal() - w_xBF.var("frac_ggzz_recobin0_4mu_2017").getVal())/w_LLR.var("frac_ggzz_recobin0_4mu_2017").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("frac_qqzz_recobin0_4mu_2017: ",w_xBF.var("frac_qqzz_recobin0_4mu_2017").getVal(), w_LLR.var("frac_qqzz_recobin0_4mu_2017").getVal(), abs(w_LLR.var("frac_qqzz_recobin0_4mu_2017").getVal() - w_xBF.var("frac_qqzz_recobin0_4mu_2017").getVal())/w_LLR.var("frac_qqzz_recobin0_4mu_2017").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("frac_zjet_recobin0_4mu_2017: ",w_xBF.var("frac_zjet_recobin0_4mu_2017").getVal(), w_LLR.var("frac_zjet_recobin0_4mu_2017").getVal(), abs(w_LLR.var("frac_zjet_recobin0_4mu_2017").getVal() - w_xBF.var("frac_zjet_recobin0_4mu_2017").getVal())/w_LLR.var("frac_zjet_recobin0_4mu_2017").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("lumi_132017: ",w_xBF.var("lumi_132017").getVal(), w_LLR.var("lumi_132017").getVal(), abs(w_LLR.var("lumi_132017").getVal() - w_xBF.var("lumi_132017").getVal())/w_LLR.var("lumi_132017").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("n_fakeH_var_recobin0_4mu2017:",w_xBF.var("n_fakeH_var_recobin0_4mu2017").getVal(), w_LLR.var("n_nonResH_var_recobin0_4mu_2017").getVal(), abs(w_LLR.var("n_nonResH_var_recobin0_4mu_2017").getVal() - w_xBF.var("n_fakeH_var_recobin0_4mu2017").getVal())/w_LLR.var("n_nonResH_var_recobin0_4mu_2017").getVal()))
print("|{0:30} | {1:15} | {2:15} | 3:15 | ".format("outfracBin_recobin0_4mu: ",w_xBF.var("outfracBin_recobin0_4mu").getVal(), w_LLR.var("outfracBin_recobin0_4mu2017").getVal(), abs(w_LLR.var("outfracBin_recobin0_4mu2017").getVal() - w_xBF.var("outfracBin_recobin0_4mu").getVal())/w_LLR.var("outfracBin_recobin0_4mu2017").getVal()))
"""

# Print Entries
entries = int(w_xBF.data("data_obs").sumEntries())
print(entries)

# Print summary of RooDataSet
print(w_xBF.data("data_obs").Print("V"))
print(w_LLR.data("data_obs").Print("V"))

# Print one entry of RooDataset
# print(w_xBF.data("data_obs").get(0).printValue())
# print(w_xBF.data("data_obs").get(0).Print("V"))
# print(w_LLR.data("data_obs").get(0).Print("V"))


# for i in range(entries):
#     print("===: Entry: ",i)
#     print(w_xBF.data("data_obs").get(i).Print("V"))
#     print(w_LLR.data("data_obs").get(i).Print("V"))


print("="*50)
# Get the RooRealVar CMS_zz4l_mass from data and plot it
# CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass", "CMS_zz4l_mass", 105, 160)

# Get the RooRealVar from WS
CMS_zz4l_mass = w.var("CMS_zz4l_mass")

# Get RooDataSet from WS
ds_LLR = w_LLR.data("data_obs")
ds_xBF = w_xBF.data("data_obs")

c = TCanvas()


frame = CMS_zz4l_mass.frame()
ds_LLR.plotOn(frame,RooFit.LineColor(1),RooFit.MarkerColor(1),RooFit.LineWidth(1), RooFit.Name("LLR"))
frame.Draw()
legend.AddEntry("LLR","LLR", "P");

frame2 = CMS_zz4l_mass.frame()
ds_xBF.plotOn(frame2,RooFit.LineColor(2),RooFit.MarkerColor(2),RooFit.LineWidth(2), RooFit.Name("xBF"))
frame2.Draw("same")
legend.AddEntry("xBF","xBF","P");

legend.Draw()
c.SaveAs(Name.replace(':','_').replace(' ','_')+".png")
# raw_input() # don't close the pop up-ed canvas
