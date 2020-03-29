from ROOT import *
gSystem.Load("$CMSSW_BASE/lib/${SCRAM_ARCH}/libHiggsAnalysisCombinedLimit.so")                                                                                                                                                               

fin = TFile("higgsCombinepT4l.MultiDimFit.mH125.123456.root")

ws = fin.Get("w")
var = ws.var("CMS_zz4l_mass")
var.Print("v")

data = fin.Get("toys/toy_asimov")
data.Print("V")

#var.setBins(40,"mybins")
##bins = var.getBinningNames()
#bins = var.binBoundaries(var,var.getMin(),var.getMax())
#print bins
