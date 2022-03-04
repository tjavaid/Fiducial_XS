#!/bin/bash


combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.38 -D toy_asimov --expectSignal 1 --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=2.5,3.5 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.38 -D toy_asimov --expectSignal 1 --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=2.5,3.5 --robustFit 1 --setCrossingTolerance 0.0001 --autoRange 2 --doFits #--parallel 4 
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.38 -D toy_asimov --expectSignal 1 --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=2.5,3.5 -o impacts_mass4l_corr_v3.json
plotImpacts.py -i impacts_mass4l_corr_v3.json -o impacts_mass4l_corr_v3 --POI SigmaBin0
