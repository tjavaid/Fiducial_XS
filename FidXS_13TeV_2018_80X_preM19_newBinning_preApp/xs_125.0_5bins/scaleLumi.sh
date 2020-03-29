#sed -i "s~1.032~1.026~g" *.txt

#sed -i "s~4.74896~5.1283~g" *4e*.txt
#sed -i "s~12.8097~12.2527~g" *4mu*.txt
#sed -i "s~17.0467~18.411~g" *2e2mu*.txt

#sed -i "s~0.632/1.376~1.152/0.868~g" *2e2mu*.txt
#sed -i "s~0.595/1.427~1.316/0.727~g" *4e*.txt
#sed -i "s~0.639/1.362~1.080/0.925~g" *4mu*.txt

#for card in hzz4l_4muS_13TeV_xs_bin0.txt hzz4l_4muS_13TeV_xs_bin1.txt hzz4l_4muS_13TeV_xs_bin2.txt hzz4l_4muS_13TeV_xs_bin3.txt hzz4l_4muS_13TeV_xs_bin4.txt
#do
#echo "CMS_zjets_bkgdcompo lnN - - - - - - - - - 1.35" >> $card
#done

#for card in hzz4l_2e2muS_13TeV_xs_bin0.txt hzz4l_2e2muS_13TeV_xs_bin1.txt hzz4l_2e2muS_13TeV_xs_bin2.txt hzz4l_2e2muS_13TeV_xs_bin3.txt hzz4l_2e2muS_13TeV_xs_bin4.txt
#do
#echo "CMS_zjets_bkgdcompo lnN - - - - - - - - - 1.34" >> $card
#done

#for card in hzz4l_4eS_13TeV_xs_bin0.txt hzz4l_4eS_13TeV_xs_bin1.txt hzz4l_4eS_13TeV_xs_bin2.txt hzz4l_4eS_13TeV_xs_bin3.txt hzz4l_4eS_13TeV_xs_bin4.txt
#do
#echo "CMS_zjets_bkgdcompo lnN - - - - - - - - - 1.32" >> $card
#done

#sed -i "s~- 1.08 -~- 1.039/0.961~g" *.txt
sed -i "s~- 1.039/0.961~- 1.039/0.961 -~g" *.txt
#sed -i "s~1.0285~1.0325/0.958~g" *.txt
#sed -i "s~1.031~1.032/0.968~g" *.txt
#sed -i "s~1.0342~1.031/0.966~g" *.txt
