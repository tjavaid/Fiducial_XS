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
    from Utils import logging, logger, border_msg
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
parser.add_argument( '-s', dest='step', default=1, choices=[1, 2, 3, 4, 5, 6, 7], type=int, help='Which step to run')
parser.add_argument( '-c', dest='channels', nargs="+",  default=["4mu", "4e", "2e2mu", "4l"], help='list of channels')
parser.add_argument( '-model', dest='modelNames', default="SM_125",
                        help='Names of models for unfolding, separated by , (comma) . Default is "SM_125"')
parser.add_argument( '-p', dest='NtupleDir', default="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/", help='Path of ntuples')
parser.add_argument( '-m', dest='HiggsMass', default=125.0, type=float, help='Higgs mass')
parser.add_argument( '-y', dest='year', default=2018, type=int, help='dataset year')
parser.add_argument( '-r', dest='RunCommand', default=0, type=int, choices=[0, 1], help="if 1 then it will run the commands else it will just print the commands")
parser.add_argument( '-obs', dest='OneDOr2DObs', default=1, type=int, choices=[1, 2], help="1 for 1D obs, 2 for 2D observable")
parser.add_argument('-n', dest="nohup", action='store_true', help='if want to run using nohup')
parser.add_argument(
     "--log-level",
     default=logging.DEBUG,
     type=lambda x: getattr(logging, x),
     help="Configure the logging level."
     )
args = parser.parse_args()

# Setup logger level
logger.setLevel(args.log_level)

# create a directory named "log" to save nohup outputs.
if not os.path.isdir('log'): os.mkdir('log')

InputYAMLFile = args.inYAMLFile
ObsToStudy = "1D_Observables" if args.OneDOr2DObs == 1 else "2D_Observables"

with open(InputYAMLFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

    if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
        logger.error('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                 Please check your YAML file format!!!'''.format(InputYAMLFile))


    if ObsToStudy in cfg['Observables']:
        for obsName, obsBin in cfg['Observables'][ObsToStudy].items():
            logger.info("="*51)
            logger.info("Observable: {:11} Bins: {}".format(obsName, obsBin['bins']))
            if (args.step == 1):
                border_msg("Running efficiencies step: "+ obsName)
                for channel in args.channels:
                    logger.info("==> channel: {}".format(channel))
                    command = 'nohup python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}" -y "{year}" >& log/effs_{obsName_log}_{channel}.log &'.format(
                    # command = 'python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}"'.format(
                        obsName = obsName, obsBins = obsBin['bins'], channel = channel, year = args.year, obsName_log = obsName.replace(" ","_")
                    )
                    logger.info("Command: {}".format(command))
                    if (args.RunCommand): os.system(command)
                # os.system('ps -t')

            if (args.step == 2):
                border_msg("Running collect inputs: "+ obsName)
                collect(obsName)
                logger.info("="*51)

                # FIXME: Currently the plotter is only working for 1D vars.
                if ((not obsName.startswith("mass4l") ) and (ObsToStudy != "2D_Observables")):
                    border_msg("Running plotter to plot 2D signal efficiencies")
                    command = 'python python/plot2dsigeffs.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" --inYAMLFile="{inYAMLFile}" --obs={obsToStudy}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], inYAMLFile = args.inYAMLFile, obsToStudy = args.OneDOr2DObs
                    )
                    logger.info("Command: {}".format(command))
                    if (args.RunCommand): os.system(command)
                else:
                    logger.info("Not running `plot2dsigeffs.py` as either the choosen option is `mass4l` or `2D observables`.")
            if (args.step == 3 and (ObsToStudy != "2D_Observables")):  #  Don't run this step for 2D obs for now
                border_msg("Running Interpolation to get acceptance for MH = 125. 38 GeV and obs " + obsName)
                command = 'python python/interpolate_differential_full.py --obsName="{obsName}" --obsBins="{obsBins}" --year={year}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], year = args.year
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 4):
                border_msg("Running getUnc")
                # command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" >& log/unc_{obsName}.log &'.format(
                command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -y "{year}"'.format(
                        obsName = obsName, obsBins = obsBin['bins'], year = args.year
                )
                logger.info("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 5 and (ObsToStudy != "2D_Observables")): #  Don't run this step for 2D obs for now
                border_msg("Grab NNLOPS acc & unc for MH = 125.38 GeV using the powheg sample")
                command = 'python python/interpolate_differential_pred.py --obsName="{obsName}" --obsBins="{obsBins}" --year={year}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], year = args.year
                )
                print("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 6):
                border_msg("Running Background template maker: " + obsName)
                # FIXME: Check if we need modelNames in step-4 or not
                command = ''
                if args.nohup: command = 'nohup '
                command += 'python -u runHZZFiducialXS.py --dir="{NtupleDir}" --obsName="{obsName}" --obsBins="{obsBins}" --modelNames {modelNames} --redoTemplates --templatesOnly '.format(
                        obsName = obsName, obsBins = obsBin['bins'], NtupleDir = args.NtupleDir, modelNames= args.modelNames
                )
                if args.nohup: command += ' >& log/step_6_nohup.log &'
                logger.info("Command: {}".format(command))
                if (args.RunCommand): os.system(command)

            if (args.step == 7):
                border_msg("Running final measurement and plotters: " + obsName)
                # Copy model from model directory to combine path
                CMSSW_BASE = os.getenv('CMSSW_BASE')
                copyCommand = 'cp models/HZZ4L*.py {CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python/'.format(CMSSW_BASE=CMSSW_BASE)
                os.system(copyCommand)

                command = ''
                if args.nohup: command = 'nohup '
                command += 'python -u runHZZFiducialXS.py --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass} --modelNames {modelNames}'.format(
                        obsName = obsName, obsBins = obsBin['bins'], HiggsMass = args.HiggsMass, modelNames= args.modelNames
                )
                if args.nohup: command += ' >& log/step_7_nohup.log &'
                logger.info("Command: {}".format(command))
                if (args.RunCommand): os.system(command)
