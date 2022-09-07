"""
This file is created to keep all the general parameters
necessary in this framework.

For example: Directory name, etc.
"""

channels_central = ['2e2mu','4mu','4e']

################################
# Mass 4l boundary
INPUT_m4l_bins = 55
INPUT_m4l_low = 105.0
INPUT_m4l_high = 160.0

# Lumi for each year
# Reference: https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#SummaryTable
Lumi_2016 = 36.31
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
