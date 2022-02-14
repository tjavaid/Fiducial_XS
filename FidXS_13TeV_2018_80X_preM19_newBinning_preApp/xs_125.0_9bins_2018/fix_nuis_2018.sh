# inclusive
#line=$(grep "lumi" hzz4l_4muS_13TeV_xs_inclusive_bin0.txt)
# differential
line=$(grep "lumi" hzz4l_4muS_13TeV_xs_bin0.txt)

sed -i -e $'17 a\\\n'"$line" hzz4l_*.txt
sed -i -e $'17 a\\\n'"$line" hzz4l_*.txt

sed -i '17s~lumi_13TeV_2018~lumi_13TeV_2018_uncorrelated~g' hzz4l_*.txt 
sed -i '17s~1.025~1.015~g' hzz4l_*.txt 
sed -i '18s~lumi_13TeV_2018~lumi_13TeV_correlated_16_17_18~g' hzz4l_*.txt 
sed -i '18s~1.025~1.02~g' hzz4l_*.txt 
sed -i '19s~lumi_13TeV_2018~lumi_13TeV_correlated_17_18~g' hzz4l_*.txt 
sed -i '19s~1.025~1.002~g' hzz4l_*.txt 
#####
sed -i "s~1.152/0.868~0.67618/1.32828~g" *2e2mu*.txt
sed -i "s~1.316/0.727~0.64540/1.36539~g" *4e*.txt
sed -i "s~1.080/0.925~0.69559/1.30459~g" *4mu*.txt

# removing correlated part
sed -i "s~CMS_zjets_bkgdcompo~#CMS_zjets_bkgdcompo~g" *.txt

