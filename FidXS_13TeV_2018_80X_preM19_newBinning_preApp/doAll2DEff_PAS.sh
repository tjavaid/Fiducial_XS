#new binings
# inclusive obs="mass4l"
#
python -u plot2dsigeffs.py -l -q -b --obsName="pT4l" --obsBins="|0|15|30|45|80|120|200|13000|" >& sigeffs_pT4l.log & # PAS
#python -u plot2dsigeffs.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|" >& sigeffs_pT4l.log & # paper
# jet multiplicity (increased 1 bin, total 5 bins now)
python -u plot2dsigeffs.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" >& sigeffs_njets.log &

#pT leading jet (5 bins, 2 bins increassed)
python -u plot2dsigeffs.py -l -q -b --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|120.0|13000|" >& sigeffs_ptjet.log &
#eta(H) (new obs as compared to HIG-16-041, same binning as combination and Run1)
python -u plot2dsigeffs.py -l -q -b --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.6|0.9|1.2|2.5|" >& sigeffs_rapidity4l.log &



