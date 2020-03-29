# inclusive obs="mass4l"
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4mu" >& effs_mass4l_4mu.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4e" >& effs_mass4l_4e.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "2e2mu" >& effs_mass4l_2e2mu.log &

# pT4l observable
#nohup python -u efficiencyFactors.py -l -q -b --dir="root://cmsio5.rc.ufl.edu//store/user/t2/users/klo/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Feb19_fixGENjet_bestCandLegacy/" --obsName="pT4l" --obsBins="|0|15|30|45|80|120|200|13000|"  >& effs_pT4l_2102.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|" -c "4mu" >& effs_pT4l_4mu.log &  # new binning suggested from Combination group
nohup python -u efficiencyFactors.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|" -c "4e" >& effs_pT4l_4e.log &  # new binning suggested from Combination group
nohup python -u efficiencyFactors.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|" -c "2e2mu" >& effs_pT4l_2e2mu.log &  # new binning suggested from Combination group

# rapdity of Higgs
nohup python -u efficiencyFactors.py -l -q -b --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.6|0.9|1.2|2.5|"  -c "4mu" >& log_rapidity4l_4mu.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.6|0.9|1.2|2.5|"  -c "4e" >& log_rapidity4l_4e.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.6|0.9|1.2|2.5|"  -c "2e2mu" >& log_rapidity4l_2e2mu.log &

# no. of jets (eta 2p5)
nohup python -u efficiencyFactors.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" -c "4mu" >& effs_njets_pt30_eta2p5_4mu.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" -c "4e" >& effs_njets_pt30_eta2p5_4e.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" -c "2e2mu" >& effs_njets_pt30_eta2p5_2e2mu.log &

# pT of leading jet (eta 2p5)
nohup python -u efficiencyFactors.py -l -q -b --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|120.0|13000|" -c "4mu" >& effs_pt_leadingjet_pt30_eta2p5_4mu.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|120.0|13000|" -c "4e" >& effs_pt_leadingjet_pt30_eta2p5_4e.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|120.0|13000|" -c "2e2mu" >& effs_pt_leadingjet_pt30_eta2p5_2e2mu.log &


