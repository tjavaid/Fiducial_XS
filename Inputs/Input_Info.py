"""
This file is created to keep all the general parameters
necessary in this framework.

For example: Directory name, etc.
"""
################################
# Mass 4l boundary
INPUT_m4l_bins = 55
INPUT_m4l_low = 105.0
INPUT_m4l_high = 160.0

# Lumi for each year
Lumi_2016 = 36.33
Lumi_2017 = 41.48
Lumi_2018 = 59.83
Lumi_Run2 = 138

################################
# Name of output directories
# datacardInputs = "{year}/datacardInputs"
datacardInputs = "datacardInputs/{year}"

combineOutputs = "xs_125.0_{year}"

#################################
# Path of plot directory
# Plots/TypeOfPlot/Year/plotName.png

SigEfficiencyPlots = "plots/SigEfficiency/{year}/{obsName}"

DifferentialBins = "plots/DifferentialBins/{year}/{obsName}"

AsimovPlots = "plots/plotAsimov/{year}/{obsName}"

LHScanPlots =  "plots/LHScanPlots/{year}/{obsName}"

ResultsPlot = "plots/results/{year}/"
################################
# Paths of ntuples
################################
