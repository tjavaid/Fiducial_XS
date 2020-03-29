# These commands for observed data
# with systematics
combine -n mass4l_SigmaBin0 -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=500
# no systematics
combine -n mass4l_SigmaBin0_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=500 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0

#### These commands for observed data
# 4e
# with systematics
combine -n mass4l_r4eBin0 -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P r4eBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:r4eBin0=0.0,5.0 --redefineSignalPOI r4eBin0 --algo=grid --points=500
# no systematics
combine -n mass4l_r4eBin0_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P r4eBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:r4eBin0=0.0,5.0 --redefineSignalPOI r4eBin0 --algo=grid --points=500 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0
# 4mu
# with systematics
combine -n mass4l_r4muBin0 -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P r4muBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:r4muBin0=0.0,5.0 --redefineSignalPOI r4muBin0 --algo=grid --points=500
# no systematics
combine -n mass4l_r4muBin0_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P r4muBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:r4muBin0=0.0,5.0 --redefineSignalPOI r4muBin0 --algo=grid --points=500 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0
# 2e2mu
# with systematics
combine -n mass4l_r2e2muBin0 -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P r2e2muBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:r2e2muBin0=0.0,5.0 --redefineSignalPOI r2e2muBin0 --algo=grid --points=500
# no systematics
combine -n mass4l_r2e2muBin0_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P r2e2muBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:r2e2muBin0=0.0,5.0 --redefineSignalPOI r2e2muBin0 --algo=grid --points=500 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0

