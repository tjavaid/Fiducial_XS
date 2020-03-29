nohup python -u runHZZFiducialXS.py  --dir="root://cmsio5.rc.ufl.edu//store/user/t2/users/rosedj1/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Mar12_4l_2018Jets_JER_bestCandLegacy" --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly >& templates_mass4l.log &

#nohup python -u runHZZFiducialXS.py  --dir="root://cmsio5.rc.ufl.edu//store/user/t2/users/rosedj1/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Mar12_4l_2018Jets_JER_bestCandLegacy" --obsName="pT4l" --obsBins="|0|15|30|45|80|120|200|13000|" --redoTemplates --templatesOnly >& templates_pT4l_1303.log &
nohup python -u runHZZFiducialXS.py  --dir="root://cmsio5.rc.ufl.edu//store/user/t2/users/rosedj1/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Mar12_4l_2018Jets_JER_bestCandLegacy" --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|" --redoTemplates --templatesOnly >& templates_pT4l.log &


nohup python -u runHZZFiducialXS.py  --dir="root://cmsio5.rc.ufl.edu//store/user/t2/users/rosedj1/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Mar12_4l_2018Jets_JER_bestCandLegacy" --obsName="njets_pt30_eta2p5" --obsBins="|0.0|1.0|2.0|3.0|4.0|10.0|" --redoTemplates --templatesOnly >& templates_njets_pt30_eta2p5.log &


nohup python -u runHZZFiducialXS.py  --dir="root://cmsio5.rc.ufl.edu//store/user/t2/users/rosedj1/Higgs/HZZ4l/NTuple/Run2/MC2018_M19_Mar12_4l_2018Jets_JER_bestCandLegacy" --obsName="pt_leadingjet_pt30_eta2p5" --obsBins="|-2.0|30.0|55.0|95.0|200.0|13000.0|" --redoTemplates --templatesOnly >& templates_pt_leadingjet_pt30_eta2p5.log &





