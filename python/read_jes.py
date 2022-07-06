import yaml
import io
import argparse
import os
from Input_Info import *
import importlib

parser = argparse.ArgumentParser(description='Main input options')
parser.add_argument( '-c', dest='channel', default="4l", help='Final state channle chosen for the template')
parser.add_argument( '-b', dest='nbins', default=1, help='nBins for the chosen variable')
parser.add_argument( '-v', dest='variable_name', default="mass4lj", help='Observatble name')
parser.add_argument( '-y', dest='year', default='2018', help='Data taking period')
args = parser.parse_args()

channel = args.channel
variable_name = args.variable_name
nbins = int(args.nbins)
year = args.year


os.system('touch __init__.py')
os.system('cp __init__.py Inputs/__init__.py')
os.system('cp __init__.py Inputs/JES/__init__.py')
os.system('cp __init__.py Inputs/JES/{}/__init__.py'.format(year))
os.system('cp __init__.py Inputs/JES/{}/{}/__init__.py'.format(year, variable_name))
JES = importlib.import_module("Inputs.JES.{}.{}.inputs_JESnuis_{}".format(year, variable_name, variable_name))

jes_sources = [
    "Abs", 
    "Abs_year", 
    "BBEC1", 
    "BBEC1_year", 
    "EC2", 
    "EC2_year", 
    "FlavQCD", 
    "HF", 
    "HF_year", 
    "RelBal", 
    "RelSample_year", ]
#    "Total"]
# We don't use Total for now
processes = [

]

jes_sources = [x.replace('year', year) for x in jes_sources]

datacardInputs = {}

for b in range(nbins):
    lines = [] 
    for jes_source in jes_sources:
       line = "CMS_scale_j_"+ jes_source + " lnN " + "{} ".format(JES.yield_nom['Hproc_125_'+ variable_name +'_'+ channel +'_recobin' +str(b)]) * (nbins + 2) + \
              str(JES.yield_nom['bkg_qqzz_125_'+ variable_name +'_'+ channel +'_recobin' + str(b)]) + " "  + \
              str(JES.yield_nom['bkg_ggzz_125_'+ variable_name +'_'+ channel +'_recobin' + str(b)]) + " "  + \
              str(JES.yield_nom['bkg_zjets_125_'+ variable_name +'_'+ channel +'_recobin' + str(b)])
      # print(line)
       lines.append(line)

    datacardInputs[variable_name + "_" + str(b)] = lines   

#print(datacardInputs)


f = open("Inputs/JES/{}/{}/datacardLines_JESnuis_{}_{}.txt".format(year, variable_name, variable_name, channel),"w")
f.write( str(datacardInputs) )
f.close()

