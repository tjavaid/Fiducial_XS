#!/bin/bash

combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 --robustFit 1 --doFits --parallel 4
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 -o impacts_v3.json
plotImpacts.py -i impacts_v3.json -o impacts_v3 --POI SigmaBin0

#combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09 --doInitialFit --robustFit 1
#combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09 --robustFit 1 --doFits
#combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D data_obs --setParameters MH=125.09 --setParameterRanges MH=125.09,125.09 -o impacts_v2_2e2mu.json
#plotImpacts.py -i impacts_v2_2e2mu.json -o impacts_v2_2e2mu --POI r2e2muBin0