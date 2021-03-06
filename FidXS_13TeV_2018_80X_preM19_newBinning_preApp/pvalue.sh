#!/bin/sh

combine -n BestFit_mass4l_v2 -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit"   --saveWorkspace -m 125.09 --setPhysicsModelParameterRanges MH=125.09,125.09 --setPhysicsModelParameters r2e2muBin0=1.28091360465,r4muBin0=0.765091865929,r4eBin0=0.691450720086,MH=125.09 -P r2e2muBin0 -P r4muBin0 -P r4eBin0 --saveNLL

combine -n SMFit_mass4l_v2 -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit"   --saveWorkspace -m 125.09 --setPhysicsModelParameterRanges MH=125.09,125.09 --setPhysicsModelParameters r2e2muBin0=1.28091360465,r4muBin0=0.765091865929,r4eBin0=0.691450720086,MH=125.09 -P r2e2muBin0 -P r4muBin0 -P r4eBin0 --freezeNuisances r2e2muBin0,r4muBin0,r4eBin0 --saveNLL

