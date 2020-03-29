from math import *

# pT4l
allobs = ["pT4l","njets_pt30_eta2p5","pt_leadingjet_pt30_eta2p5"]

for obs in allobs:
  
  resultsXS = __import__('resultsXS_LHScan_'+obs+'_v3', globals(), locals(), ['resultsXS'], -1)

  if obs=="pT4l": nbins = 5
  if obs=="njets_pt30_eta2p5": nbins = 4
  if obs=="pt_leadingjet_pt30_eta2p5": nbins = 4

  print obs

  for i in range(nbins):
    line = str(round(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)]['central'],3))

    line += " +"+str(round(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)+'_statOnly']['uncerUp'],3))
    line += ","+str(round(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)+'_statOnly']['uncerDn'],3))

    line += " (DSYS=+"+str(round(sqrt(float(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)]['uncerUp'])**2-float(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)+'_statOnly']['uncerUp'])**2),3))
    line += ",-"+str(round(sqrt(float(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)]['uncerDn'])**2-float(resultsXS.resultsXS['SM_125_'+obs+'_genbin'+str(i)+'_statOnly']['uncerDn'])**2),3))
    line += ");"
    print line
