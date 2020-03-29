#new binning
python -u getUnc_Unc.py --obsName="mass4l" --obsBins="|105.0|140.0|" >& unc_mass4l.log & 
#pT(H) (7 bins)
python -u getUnc_Unc.py -l -q -b --obsName="pT4l" --obsBins="|0|15|30|45|80|120|200|13000|" >& unc_pT4l.log &
# jet multiplicity (increased 1 bin, total 5 bins now)
python -u getUnc_njets_Unc.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" >& unc_njets_pt30_eta2p5.log &
python -u getUnc_Unc.py -l -q -b --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|200.0|13000.0|" >& unc_pt_leadingjet_pt30_eta2p5.log &
python -u getUnc_Unc.py -l -q -b --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.6|0.9|1.2|2.5|" >& unc_rapidity4l.log &



