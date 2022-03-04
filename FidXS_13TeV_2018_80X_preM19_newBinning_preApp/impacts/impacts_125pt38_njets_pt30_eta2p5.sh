#!/bin/bash


combineTool.py -M Impacts -d SM_125_all_13TeV_xs_njets_pt30_eta2p5_bin_v3_exp.root -m 125.38 -D toy_asimov --expectSignal 1 --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=0.01,1 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_njets_pt30_eta2p5_bin_v3_exp.root -m 125.38 -D toy_asimov --expectSignal 1 --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=0.01,1 --robustFit 1 --setCrossingTolerance 0.001 --autoRange 2 --doFits --parallel 4 
combineTool.py -M Impacts -d SM_125_all_13TeV_xs_njets_pt30_eta2p5_bin_v3_exp.root -m 125.38 -D toy_asimov --expectSignal 1 --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=0.01,1 -o impacts_njets_pt30_eta2p5.json
#plotImpacts.py -i impacts_njets_pt30_eta2p5.json -o impacts_njets_pt30_eta2p5 --POI SigmaBin0 SigmaBin1 SigmaBin2 SigmaBin3 SigmaBin4 SigmaBin5 SigmaBin6 SigmaBin7
i=0
echo "producing impact plots..... "
while (( $i <= 8 ))
do
   echo "$i"
   plotImpacts.py -i impacts_njets_pt30_eta2p5.json -o impacts_njets_pt30_eta2p5_SigmaBin$i --POI SigmaBin$i
  (( i=$i+1 ))
done

#plotImpacts.py -i impacts_njets_pt30_eta2p5.json -o impacts_njets_pt30_eta2p5_SigmaBin7 --POI SigmaBin7
#plotImpacts.py -i impacts_njets_pt30_eta2p5.json -o impacts_njets_pt30_eta2p5 --POI SigmaBin0 SigmaBin1 SigmaBin2 SigmaBin3 SigmaBin4 SigmaBin5 SigmaBin6 SigmaBin7
