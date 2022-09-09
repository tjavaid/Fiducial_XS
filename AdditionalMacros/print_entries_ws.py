from ROOT import *

Year = '2018'
Channel = '2e2mu'
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


print("="*50)
# Get the RooRealVar CMS_zz4l_mass from data and plot it
# Define the RooRealVar
# CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass", "CMS_zz4l_mass", 105, 160)

# Get the RooRealVar from WS
CMS_zz4l_mass = w.var("CMS_zz4l_mass")

# Get RooDataSet from WS
ds_LLR = w_LLR.data("data_obs")
obs_LLR = ds_LLR.get()
h4lMass_LLR = obs_LLR.find("CMS_zz4l_mass")
# Reset range
h4lMass_LLR.setRange(105,160)
# Reset bins
h4lMass_LLR.setBins(100)

ds_xBF = w_xBF.data("data_obs")
obs_xBF = ds_xBF.get()
h4lMass_xBF = obs_xBF.find("CMS_zz4l_mass")
# Reset range
h4lMass_xBF.setRange(105,160)
# Reset bins
h4lMass_xBF.setBins(100)

print("entries: ",ds_xBF.numEntries())
# for x in xrange(0, ds_xBF.numEntries()):
#   ds_xBF.get(x)
#   print x,h4lMass_xBF.getValV()

# print("entries: ",ds_LLR.numEntries())
# for x in xrange(0, ds_LLR.numEntries()):
#   ds_LLR.get(x)
#   print x,h4lMass_LLR.getValV()

print("entries: ",ds_LLR.numEntries())
for x in xrange(0, ds_LLR.numEntries()):
  ds_LLR.get(x)
  ds_xBF.get(x)
#   print x,h4lMass_LLR.getValV(),h4lMass_xBF.getValV()
  print("{}\t{}".format(h4lMass_LLR.getValV(),h4lMass_xBF.getValV()))

# c2 = TCanvas("c2","")
# frame_xBF = h4lMass_xBF.frame(RooFit.Title("H_{4l} invariant mass"))
# ds_xBF.plotOn(frame_xBF,RooFit.LineColor(2),RooFit.MarkerColor(2),RooFit.LineWidth(2), RooFit.Name("LLR"))
# frame_xBF.Draw()
# legend.AddEntry("xBF","xBF", "P");
# legend.Draw()

# frame_LLR = h4lMass_LLR.frame(RooFit.Title("H_{4l} invariant mass"))
# ds_LLR.plotOn(frame_LLR,RooFit.LineColor(2),RooFit.MarkerColor(2),RooFit.LineWidth(2), RooFit.Name("LLR"))
# frame_LLR.Draw("same")
# legend.AddEntry("LLR","LLR", "P");
# legend.Draw()

# raw_input() # don't close the pop up-ed canvas
