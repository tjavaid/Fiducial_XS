# These commands for observed data

# with systematics
combine -n pT4l_SigmaBin0 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin0=0.0,3.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=150

# no systematics
combine -n pT4l_SigmaBin0_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin0=0.0,3.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=300 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0


# with systematics
combine -n pT4l_SigmaBin1 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin1 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin1=0.0,3.0 --redefineSignalPOI SigmaBin1 --algo=grid --points=150

# no systematics
combine -n pT4l_SigmaBin1_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin1 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin1=0.0,3.0 --redefineSignalPOI SigmaBin1 --algo=grid --points=300 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0


# with systematics
combine -n pT4l_SigmaBin2 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin2 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin2=0.0,3.0 --redefineSignalPOI SigmaBin2 --algo=grid --points=150

# no systematics
combine -n pT4l_SigmaBin2_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin2 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin2=0.0,3.0 --redefineSignalPOI SigmaBin2 --algo=grid --points=300 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0

# with systematics
combine -n pT4l_SigmaBin3 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin3 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin3=0.0,3.0 --redefineSignalPOI SigmaBin3 --algo=grid --points=150

# no systematics
combine -n pT4l_SigmaBin3_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin3 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin3=0.0,3.0 --redefineSignalPOI SigmaBin3 --algo=grid --points=300 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0


# with systematics
combine -n pT4l_SigmaBin4 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin4 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin4=0.0,3.0 --redefineSignalPOI SigmaBin4 --algo=grid --points=300

# no systematics
combine -n pT4l_SigmaBin4_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin4 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin4=0.0,3.0 --redefineSignalPOI SigmaBin4 --algo=grid --points=600 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0

# with systematics
combine -n pT4l_SigmaBin5 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin5 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin5=0.0,0.3 --redefineSignalPOI SigmaBin5 --algo=grid --points=300
# no systematics
combine -n pT4l_SigmaBin5_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin5 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin5=0.0,3.0 --redefineSignalPOI SigmaBin5 --algo=grid --points=600 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0
# with systematics
combine -n pT4l_SigmaBin6 -M MultiDimFit SM_125_all_13TeV_xs_pT4l_bin_v3_exp.root -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin6 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin6=0.0,0.3 --redefineSignalPOI SigmaBin6 --algo=grid --points=300
# no systematics
combine -n pT4l_SigmaBin6_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_pT4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D toy_asimov --setPhysicsModelParameters MH=125.09 -P SigmaBin6 --floatOtherPOIs=1 --saveWorkspace --setPhysicsModelParameterRanges MH=125.09,125.09:SigmaBin6=0.0,3.0 --redefineSignalPOI SigmaBin6 --algo=grid --points=600 --freezeNuisances CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 -S 0
