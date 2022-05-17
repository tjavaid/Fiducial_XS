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

################################
# Name of output directories
datacardInputs = "{year}/datacardInputs"

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
