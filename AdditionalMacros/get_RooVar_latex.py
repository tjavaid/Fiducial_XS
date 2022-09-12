from ROOT import *

Year = '2018'
Channel = '2e2mu'
Name = Year + ": "+Channel

# File 1 to compare
f_xBF = TFile('/eos/user/r/rasharma/www/h4l/HIG_21_009/Sept6_2022/xs_125.0_'+Year+'/hzz4l_'+Channel+'S_13TeV_xs_SM_125_mass4l_v3.Databin0.root','READ')
w_xBF = f_xBF.Get("w")
# w_xBF.Print()

print(w_xBF.Get(bkg_ggzz))

print("="*51)
# print(w_xBF.allVars().Print())
params = w_xBF.allVars()
initParams = params.snapshot()

# print("="*51)
# params.printLatex()
# params.printLatex(RooFit.Columns(2))
# params.printLatex(RooFit.Sibling(initParams))
params.printLatex(RooFit.Columns(2), RooFit.Format("NEU", RooFit.FixedPrecision(5), RooFit.VerbatimName()), RooFit.OutputFile(Name.replace(':','_').replace(' ','_') + "_xBF.tex"))

# Print two parameter lists side by side (name values initvalues)
# params.printLatex(RooFit.Sibling(initParams),  RooFit.Format("NEU", RooFit.FixedPrecision(5)))
# params.printLatex(RooFit.Sibling(initParams), RooFit.OutputFile("rf407_latextables.tex"))

# print(w_xBF.allVars().Print())
# print(type(w_xBF.allVars()))
# print(type(w_xBF.allVars().Print()))
# print(w_xBF.allVars().Print())
print("="*51)

# File 2 to compare
f_LLR = TFile('../LLR_'+Year+'_hzz4l_'+Channel+'S_13TeV_xs_SM_125_mass4l_v3.Databin0.root','READ')
w_LLR = f_LLR.Get("w")
# w_LLR.Print()

params_LLR = w_LLR.allVars()
initParams_LLR = params_LLR.snapshot()
params.printLatex(RooFit.Columns(2), RooFit.Format("NEU", RooFit.FixedPrecision(5), RooFit.VerbatimName()), RooFit.OutputFile(Name.replace(':','_').replace(' ','_') + "_LLR.tex"))
