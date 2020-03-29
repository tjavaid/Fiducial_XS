from ROOT import *

# Load some libraries                                 
#gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
#gSystem.Load("$CMSSW_BASE/lib/slc6_amd64_gcc491/libHiggsAnalysisCombinedLimit.so")
#gSystem.AddIncludePath("-I$ROOFITSYS/include")
#gSystem.AddIncludePath("-Iinclude/")

f = TFile("SM_125_all_13TeV_xs_pT4l_bin_v3_result.root","READ")
w = f.Get("w")

var = w.var("SigmaBin0")

w.loadSnapshot("clean")
print var.getVal()

w.loadSnapshot("MultiDimFit")
print var.getVal()

