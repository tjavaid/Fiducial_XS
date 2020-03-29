#!/bin/bash


#combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09:SigmaBin0=2.5,3.5 --doInitialFit --robustFit 1
#combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09:SigmaBin0=2.5,3.5 --robustFit 1 --setCrossingTolerance 0.001 --autoRange 2 --doFits --parallel 4 
#combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09:SigmaBin0=2.5,3.5 -o impacts.json
#plotImpacts.py -i impacts.json -o impacts --POI SigmaBin0


combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09 --robustFit 1 --doFits
for channel in r2e2muBin0 r4muBin0 r4eBin0; do
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09 -o impacts_v2_${channel}.json
plotImpacts.py -i impacts_v2_${channel}.json -o impacts_v2_${channel} --POI ${channel}
done
