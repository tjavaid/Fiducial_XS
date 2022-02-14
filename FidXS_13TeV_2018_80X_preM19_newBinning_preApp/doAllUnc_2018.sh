nohup python -u getUnc_Unc.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --year="2018" >& unc_mass4l_2018.unc & 

nohup python -u getUnc_Unc.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|60|80|120|200|13000|" --year="2018" >& unc_pT4l_2018.unc & 
nohup python -u getUnc_Unc.py -l -q -b --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.45|0.6|0.75|0.9|1.2|1.6|2.5|" --year="2018" >& unc_rapidity4l_2018.unc & 
nohup python -u getUnc_Unc.py -l -q -b --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|200.0|13000.0|" --year="2018" >& unc_pt_leadingjet_pt30_eta2p5_2018.unc & 
#nohup python -u getUnc_Unc.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" --year="2018" >& unc_njets_pt30_eta2p5_2018.unc &
nohup python -u getUnc_njets_Unc.py -l -q -b --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" --year="2018" >& unc_njets_pt30_eta2p5_2018.unc &
nohup python -u getUnc_Unc.py -l -q -b --obsName="massZ2" --obsBins="|12.0|22.0|25.0|28.0|30.0|32.0|35.0|40.0|50.0|65.0|" --year="2018" >& unc_massZ2_2018.unc & 
nohup python -u getUnc_Unc.py -l -q -b --obsName="massZ1" --obsBins="|40.0|65.0|73.0|80.0|85.0|90.0|120.0|" --year="2018" >& unc_massZ1_2018.unc &
nohup python -u getUnc_Unc.py -l -q -b --obsName="cosTheta1" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|" --year="2018" >& unc_cosTheta1_2018.unc &
nohup python -u getUnc_Unc.py -l -q -b --obsName="cosTheta2" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|" --year="2018" >& unc_cosTheta2_2018.unc &
nohup python -u getUnc_Unc.py -l -q -b --obsName="Phi" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|" --year="2018" >& unc_Phi_2018.unc &
nohup python -u getUnc_Unc.py -l -q -b --obsName="Phi1" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|" --year="2018" >& unc_Phi1_2018.unc &
nohup python -u getUnc_Unc.py -l -q -b --obsName="cosThetaStar" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|" --year="2018" >& unc_cosThetaStar_2018.log &

