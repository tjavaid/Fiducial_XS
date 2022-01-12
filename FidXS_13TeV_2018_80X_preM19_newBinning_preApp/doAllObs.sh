nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys --asimovMass 125.0  >& log_mass4l.txt & # single bin
nohup python -u runHZZFiducialXS.py --obsName="pT4l" --obsBins="|0|10|20|30|45|60|80|120|200|13000|"  --calcSys >& log_pT4l.txt &  # 9 bins
nohup python -u runHZZFiducialXS.py --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.45|0.6|0.75|0.9|1.2|1.6|2.5|" --calcSys >& log_rapidity4l.txt &  # 9 bins
nohup python -u runHZZFiducialXS.py --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|"  --calcSys >& log_njets_pt30_eta2p5.txt &  # 5 bins
nohup python -u runHZZFiducialXS.py --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|200.0|13000.0|" --calcSys >& log_pt_leadingjet_pt30_eta2p5.txt &  # 5 bins
nohup python -u runHZZFiducialXS.py --obsName="massZ1" --obsBins="|40.0|65.0|73.0|80.0|85.0|90.0|120.0|"  --calcSys >& log_massZ1.txt & # 6 bins
nohup python -u runHZZFiducialXS.py --obsName="massZ2" --obsBins="|12.0|22.0|25.0|28.0|30.0|32.0|35.0|40.0|50.0|65.0|"  --calcSys >& log_massZ2.txt & # 9 bins
nohup python -u runHZZFiducialXS.py --obsName="cosTheta1" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|"  --calcSys >& log_cosTheta1.txt & # 8 bins
nohup python -u runHZZFiducialXS.py --obsName="cosTheta2" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|"  --calcSys >& log_cosTheta2.txt & # 8 bins 
nohup python -u runHZZFiducialXS.py --obsName="cosThetaStar" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|"  --calcSys >& log_cosThetaStar.txt & # 8 bins
nohup python -u runHZZFiducialXS.py --obsName="Phi" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|"  --calcSys >& log_Phi.txt & # 8 bins 
nohup python -u runHZZFiducialXS.py --obsName="Phi1" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|"  --calcSys >& log_Phi1.txt & # 8 bins


