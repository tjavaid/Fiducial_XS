# mass4l 
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly >& templates_mass4l.log &
#pT4l
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="pT4l" --obsBins="|0|10|20|30|45|60|80|120|200|13000|" --redoTemplates --templatesOnly >& templates_pT4l.log &
# rapidity4l
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="rapidity4l" --obsBins="|0.0|0.15|0.3|0.45|0.6|0.75|0.9|1.2|1.6|2.5|" --redoTemplates --templatesOnly >& templates_rapidity4l.log &
# pt_leadingjet_pt30_eta2p5
nohup python -u runHZZFiducialXS.py  --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|200.0|13000.0|" --redoTemplates --templatesOnly >& templates_pt_leadingjet_pt30_eta2p5.log &
# njets_pt30_eta2p5
nohup python -u runHZZFiducialXS.py  --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" --redoTemplates --templatesOnly >& templates_njets_pt30_eta2p5.log &
# cosThetaStar
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="cosThetaStar" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|"  --redoTemplates --templatesOnly >& templates_cosThetaStar.log &
# cosTheta1
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="cosTheta1" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|" --redoTemplates --templatesOnly >& templates_cosTheta1.log &
# cosTheta2
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="cosTheta2" --obsBins="|-1.0|-0.75|-0.5|-0.25|0.0|0.25|0.5|0.75|1.0|" --redoTemplates --templatesOnly >& templates_cosTheta2.log &
# massZ1
nohup python -u runHZZFiducialXS.py  --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="massZ1" --obsBins="|40.0|65.0|73.0|80.0|85.0|90.0|120.0|" --redoTemplates --templatesOnly  >& templates_massZ1.log &
# massZ2
nohup python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="massZ2" --obsBins="|12.0|22.0|25.0|28.0|30.0|32.0|35.0|40.0|50.0|65.0|" --redoTemplates --templatesOnly  >& templates_massZ2.log &
# Phi
nohup python -u runHZZFiducialXS.py  --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="Phi" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|" --redoTemplates --templatesOnly   >& templates_Phi.log &
# Phi1
nohup python -u runHZZFiducialXS.py  --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="Phi1" --obsBins="|-3.14159|-2.35619|-1.570795|-0.7853975|0.0|0.7853975|1.570795|2.35619|3.14159|" --redoTemplates --templatesOnly   >& templates_Phi1.log &
