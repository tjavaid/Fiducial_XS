# producePlots.py

python python/producePlots.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --unfoldModel="SM_125" --theoryMass="125.0" --setLog

python python/producePlots.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|60|80|120|200|13000|" --unfoldModel="SM_125" --theoryMass="125.0" --setLog

python python/producePlots.py -l -q -b --obsName="massZ1_vs_massZ2" --obsBins="|50|80| vs |10|30| / |50|80| vs |30|60| / |80|110| vs |10|25| / |80|110| vs |25|30|" --unfoldModel="SM_125" --theoryMass="125.0"


# plotDifferentialBins.py

python python/plotDifferentialBins.py -l -q -b --obsName="massZ1_vs_massZ2" --obsBins="|50|80| vs |10|30| / |50|80| vs |30|60| / |80|110| vs |10|25| / |80|110| vs |25|30|" --asimovModel="SM_125" --inYAMLFile="Inputs/observables_list.yml"

# plotLHScans.py

python python/plotLHScans.py -l -q -b --obsName=mass4l


# plotAsimov*.py

python python/plotAsimov_inclusive.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --asimovModel="SM_125" --unfoldModel="SM_125"

python python/plotAsimov_simultaneous.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|60|80|120|200|13000|" --asimovModel="SM_125" --unfoldModel="SM_125" --obs=1

python python/plotAsimov_simultaneous.py -l -q -b --obsName="massZ1 vs massZ2" --obsBins="|50|80| vs |10|30| / |50|80| vs |30|60| / |80|110| vs |10|25| / |80|110| vs |25|30|" --asimovModel="SM_125" --unfoldModel="SM_125" --obs=2
