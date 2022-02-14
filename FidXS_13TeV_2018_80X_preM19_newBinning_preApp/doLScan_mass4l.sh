#if [[ "$1" == "Full" ]]; then   years="2016 2017 2018"; #fi
#elif [[ "$1" == "2016" ]]; then   years="2016"; #fi
#elif [[ "$1" == "2017" ]]; then   years="2017"; #fi
#else years="2018"
#fi

#echo "years are:  ", $years
echo "will do scan for :" $1
for ch in SigmaBin0 r4eBin0 r4muBin0 r2e2muBin0; do
  if [[ "$ch" == "SigmaBin0" ]]; then   model="v3"; #fi 
  else model="v2"
  fi
# with systematics
    combine -n mass4l_$ch -M MultiDimFit SM_125_all_13TeV_xs_mass4l_bin_$model\_exp.root -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=0.0,5.0 --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4
# no systematics
    if [[ "$1" == "Full" ]]; then
#    echo "running stat. fit for full Run 2"
    combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=0.0,5.0 --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_fakeH_p1_12016,CMS_fakeH_p1_22016,CMS_fakeH_p1_32016,CMS_fakeH_p3_12016,CMS_fakeH_p3_22016,CMS_fakeH_p3_32016,CMS_fakeH_p1_12017,CMS_fakeH_p1_22017,CMS_fakeH_p1_32017,CMS_fakeH_p3_12017,CMS_fakeH_p3_22017,CMS_fakeH_p3_32017,CMS_fakeH_p1_12018,CMS_fakeH_p1_22018,CMS_fakeH_p1_32018,CMS_fakeH_p3_12018,CMS_fakeH_p3_22018,CMS_fakeH_p3_32018,CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_2016,CMS_hzz4e_Zjets_2016,CMS_hzz4mu_Zjets_2016,CMS_hzz2e2mu_Zjets_2017,CMS_hzz4e_Zjets_2017,CMS_hzz4mu_Zjets_2017,CMS_hzz2e2mu_Zjets_2018,CMS_hzz4e_Zjets_2018,CMS_hzz4mu_Zjets_2018,QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_2016_uncorrelated,lumi_13TeV_2017_uncorrelated,lumi_13TeV_2018_uncorrelated,lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_2016,CMS_zz4l_sigma_e_sig_2017,CMS_zz4l_sigma_e_sig_2018,CMS_zz4l_sigma_m_sig_2016,CMS_zz4l_sigma_m_sig_2017,CMS_zz4l_sigma_m_sig_2018,CMS_zz4l_n_sig_1_2016,CMS_zz4l_n_sig_1_2017,CMS_zz4l_n_sig_1_2018,CMS_zz4l_n_sig_2_2016,CMS_zz4l_n_sig_2_2017,CMS_zz4l_n_sig_2_2018,CMS_zz4l_n_sig_3_2016,CMS_zz4l_n_sig_3_2017,CMS_zz4l_n_sig_3_2018,CMS_zz4l_mean_e_sig_2016,CMS_zz4l_mean_e_sig_2017,CMS_zz4l_mean_e_sig_2018,CMS_zz4l_mean_m_sig_2016,CMS_zz4l_mean_m_sig_2017,CMS_zz4l_mean_m_sig_2018
    else
#    echo "running stat. fit for 1" $1
    combine -n mass4l_$ch\_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_mass4l_bin_$model\_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P $ch --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:$ch\=0.0,5.0 --redefineSignalPOI $ch --algo=grid --points=50 --autoRange 4 --freezeParameters CMS_fakeH_p1_1$1,CMS_fakeH_p1_2$1,CMS_fakeH_p1_3$1,CMS_fakeH_p3_1$1,CMS_fakeH_p3_2$1,CMS_fakeH_p3_3$1,CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_$1,CMS_hzz4e_Zjets_$1,CMS_hzz4mu_Zjets_$1,QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_$1\_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_$1,CMS_zz4l_sigma_m_sig_$1,CMS_zz4l_n_sig_1_$1,CMS_zz4l_n_sig_2_$1,CMS_zz4l_n_sig_3_$1,CMS_zz4l_mean_e_sig_$1,CMS_zz4l_mean_m_sig_$1   # FIXME
    fi;
done;
#
