for fs in 4e 4mu 2e2mu
do

  cp hzz4l_${fs}S_13TeV_xs_bin0_sc2.txt hzz4l_${fs}S_13TeV_xs_bin1_sc2.txt
  cp hzz4l_${fs}S_13TeV_xs_bin0_sc2.txt hzz4l_${fs}S_13TeV_xs_bin2_sc2.txt
  cp hzz4l_${fs}S_13TeV_xs_bin0_sc2.txt hzz4l_${fs}S_13TeV_xs_bin3_sc2.txt
  cp hzz4l_${fs}S_13TeV_xs_bin0_sc2.txt hzz4l_${fs}S_13TeV_xs_bin4_sc2.txt
  cp hzz4l_${fs}S_13TeV_xs_bin0_sc2.txt hzz4l_${fs}S_13TeV_xs_bin5_sc2.txt
done

sed -i 's~bin0~bin1~g' hzz4l*bin1_sc2.txt
sed -i 's~bin0~bin2~g' hzz4l*bin2_sc2.txt
sed -i 's~bin0~bin3~g' hzz4l*bin3_sc2.txt
sed -i 's~bin0~bin4~g' hzz4l*bin4_sc2.txt
sed -i 's~bin0~bin5~g' hzz4l*bin5_sc2.txt
