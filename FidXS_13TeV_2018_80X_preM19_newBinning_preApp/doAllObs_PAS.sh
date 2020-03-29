# blinded

nohup python -u runHZZFiducialXS.py --obsName="pT4l" --obsBins="|0|15|30|45|80|120|200|13000|"  --calcSys >& log_pT4l_Run2Fid.txt & 
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys  >& log_mass4l_Run2Fid.txt & 
nohup python -u runHZZFiducialXS.py --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|"  --calcSys  >& log_njets_pt30_eta2p5_Run2Fid.txt &
nohup python -u runHZZFiducialXS.py --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|200.0|13000.0|"  --calcSys >& log_pt_leadingjet_pt30_eta2p5_Run2Fid.txt &
nohup python -u runHZZFiducialXS.py --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.6|0.9|1.2|2.5|"  --calcSys >& log_rapidity4l_Run2Fid.txt &

