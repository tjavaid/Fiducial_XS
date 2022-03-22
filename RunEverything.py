import sys
import os
import argparse
import yaml


# INFO: Following items are imported from either python directory or Inputs
# FIXME: Seems like try-except not implemented correctly
try:
    from collectInputs import collect
except ImportError as e:
    print(e)
    raise ImportError("Check if you run `source setup.sh`. If not please run it.\n")

try:
    from Utils import *
except Exception as e:
    print (e)
    raise ImportError("Check if you run `source setup.sh`. If not please run it.\n")


# Kept for record of models (copied from runHZZFiducialXS.py)
# modelNames = "SM_125,SMup_125,SMdn_125" #,'VBF_powheg_JHUgen_125']
# # do all models
# #if (not 'jet' in obsName):
# #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125', 'ttH_powheg_JHUgen_125']
# #else:
# #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125']

parser = argparse.ArgumentParser(description='Input arguments')
parser.add_argument( '-i', dest='inYAMLFile', default="Inputs/observables_list.yml", type=str, help='Input YAML file having observable names and bin information')
parser.add_argument( '-s', dest='step', default=1, choices=[1, 2, 3, 4, 5], type=int, help='Which step to run')
parser.add_argument( '-c', dest='channels', nargs="+",  default=["4mu", "4e", "2e2mu", "4l"], help='list of channels')
parser.add_argument( '-model', dest='modelNames', default="SM_125,SMup_125,SMdn_125",
                        help='Names of models for unfolding, separated by , (comma) . Default is "SM_125"')
parser.add_argument( '-p', dest='NtupleDir', default="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/", help='Path of ntuples')
parser.add_argument( '-m', dest='HiggsMass', default=125.0, type=float, help='Higgs mass')
parser.add_argument( '-y', dest='year', default=2018, type=int, help='dataset year')
parser.add_argument( '-r', dest='RunCommand', default=0, type=int, choices=[0, 1], help="if 1 then it will run the commands else it will just print the commands")

args = parser.parse_args()

if not os.path.isdir('log'): os.mkdir('log')


InputYAMLFile = args.inYAMLFile

with open(InputYAMLFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

    if ( ("Observables" not in cfg) or ("1D_Observables" not in cfg['Observables']) ) :
        print('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                 Please check your YAML file format!!!'''.format(InputYAMLFile))

    if "1D_Observables" in cfg['Observables']:
        for obsName, obsBin in cfg['Observables']['1D_Observables'].items():
            print("="*51)
            print("Observable: {:11} Bins: {}".format(obsName, obsBin['bins']))
            if (args.step == 1):
                border_msg("Running the efficiencies step")
                for channel in args.channels:
                    print("==> channel: {}".format(channel))
                    command = 'nohup python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}" >& log/effs_{obsName}_{channel}.log &'.format(
                    # command = 'python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}"'.format(
                        obsName = obsName, obsBins = obsBin['bins'], channel = channel
                    )
                    print("Command: {}".format(command))
                    if (args.RunCommand): os.system(command)
                # os.system('ps -t')

            if (args.step == 2):
                border_msg("Running collect inputs")
                collect(obsName)
                print("="*51)

                if (not obsName.startswith("mass4l")):
                    border_msg("Running plotter to plot 2D signal efficiencies")
                    command = 'python python/plot2dsigeffs.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" --inYAMLFile="{inYAMLFile}"'.format(
                        obsName = obsName, obsBins = obsBin['bins'], inYAMLFile = args.inYAMLFile
                    )
                    print("Command: {}".format(command))
                    if (args.RunCommand): os.system(command)

            if (args.step == 3):
                border_msg("Running Interpolation to get acceptance for MH = 125. 38 GeV")
                command = 'python python/interpolate_differential_full.py --obsName="{obsName}" --obsBins="{obsBins}" --year={year}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], year = args.year
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 4):
                border_msg("Running getUnc")
                # command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" >& log/unc_{obsName}.log &'.format(
                command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}"'.format(
                        obsName = obsName, obsBins = obsBin['bins']
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 5):
                border_msg("Grab NNLOPS acc & unc for MH = 125.38 GeV using the powheg sample")
                command = 'python python/interpolate_differential_pred.py --obsName="{obsName}" --obsBins="{obsBins}" --year={year}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], year = args.year
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 6):
                border_msg("Running Background template maker")
                # FIXME: Check if we need modelNames in step-4 or not
                command = 'python -u runHZZFiducialXS.py --dir="{NtupleDir}" --obsName="{obsName}" --obsBins="{obsBins}" --modelNames {modelNames} --redoTemplates --templatesOnly '.format(
                        obsName = obsName, obsBins = obsBin['bins'], NtupleDir = args.NtupleDir, modelNames= args.modelNames
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 7):
                border_msg("Running final measurement and plotters")
                # Copy model from model directory to combine path
                CMSSW_BASE = os.getenv('CMSSW_BASE')
                copyCommand = 'cp models/HZZ4L*.py {CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python/'.format(CMSSW_BASE=CMSSW_BASE)
                os.system(copyCommand)

                # command = 'nohup python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass}  >& log/log_{obsName}_Run2Fid.txt &'.format(
                command = 'python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass} --modelNames {modelNames}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], HiggsMass = args.HiggsMass, modelNames= args.modelNames
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)
