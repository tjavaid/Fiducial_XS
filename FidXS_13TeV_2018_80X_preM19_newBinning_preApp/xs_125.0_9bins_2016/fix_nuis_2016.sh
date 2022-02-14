# inclusive
#line=$(grep "lumi" hzz4l_4muS_13TeV_xs_inclusive_bin0.txt)
# differential
line=$(grep "lumi" hzz4l_4muS_13TeV_xs_bin0.txt)
sed -i -e $'17 a\\\n'"$line" hzz4l_*.txt
#sed -i -e $'17 a\\\n'"$line" hzz4l_*.txt

sed -i '17s~lumi_13TeV_2016~lumi_13TeV_2016_uncorrelated~g' hzz4l_*.txt 
sed -i '17s~1.026~1.01~g' hzz4l_*.txt 
sed -i '18s~lumi_13TeV_2016~lumi_13TeV_correlated_16_17_18~g' hzz4l_*.txt 
sed -i '18s~1.026~1.006~g' hzz4l_*.txt 
#sed -i '19s~lumi_13TeV_2016~lumi_13TeV_correlated_17_18~g' hzz4l_*.txt 
#sed -i '19s~1.026~1.002~g' hzz4l_*.txt 
#####
sed -i "s~1.152/0.868~0.65673/1.35484~g" *2e2mu*.txt
sed -i "s~1.316/0.727~0.60745/1.42863~g" *4e*.txt
sed -i "s~1.080/0.925~0.69481/1.30542~g" *4mu*.txt

# removing correlated part
sed -i "s~CMS_zjets_bkgdcompo~#CMS_zjets_bkgdcompo~g" *.txt

