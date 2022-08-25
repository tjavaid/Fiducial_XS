import os
import argparse
import yaml
import datetime
import sys

# INFO: Following items are imported from either python directory or Inputs
# FIXME: Seems like try-except not implemented correctly
try:
    from collectInputs import collect
except ImportError as e:
    print(e)
    raise ImportError("Check if you run `source setup.sh`. If not please run it.\n")

try:
    from Utils import logging, logger, border_msg, GetDirectory, processCmd, get_linenumber
except Exception as e:
    print (e)
    raise ImportError("Check if you run `source setup.sh`. If not please run it.\n")

from LoadData import dirMC

# Kept for record of models (copied from runHZZFiducialXS.py)
# modelNames = "SM_125,SMup_125,SMdn_125" #,'VBF_powheg_JHUgen_125']
# # do all models
# #if (not 'jet' in obsName):
# #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125', 'ttH_powheg_JHUgen_125']
# #else:
# #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125']

parser = argparse.ArgumentParser(description='Input arguments')
parser.add_argument( '-i', dest='inYAMLFile', default="Inputs/observables_list.yml", type=str, help='Input YAML file having observable names and bin information')
parser.add_argument( '-s', dest='step', default=1, choices=[1, 2, 3, 4, 5, 6, 7,8,9], type=int, help='Which step to run')
parser.add_argument( '-c', dest='channels', nargs="+",  default=["4mu", "4e", "2e2mu", "4l"], help='list of channels')
parser.add_argument( '-model', dest='modelNames', default="SM_125",
                        help='Names of models for unfolding, separated by , (comma) . Default is "SM_125"')
parser.add_argument( '-m', dest='HiggsMass', default=125.38, type=float, help='Higgs mass')
parser.add_argument( '-y', dest='year', default='2018', type=str, choices=["2016", "2017", "2018", "allYear", "all"], help='dataset year: 2016, 2017, 2018, allYear (combination), all (for running all three years and combination)')
parser.add_argument( '-r', dest='RunCommand', default=0, type=int, choices=[0, 1], help="if 1 then it will run the commands else it will just print the commands")
parser.add_argument( '-obs', dest='OneDOr2DObs', default=1, type=int, choices=[1, 2], help="1 for 1D obs, 2 for 2D observable")
parser.add_argument( '--test', dest='TestVar', default="", type=str, help="Name of test variables to run over. For example: mass4l")
parser.add_argument('--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
parser.add_argument('--checkDuplicate', action='store_true', dest='checkDuplicate', default=False, help='Use real data')
parser.add_argument('-n', dest="nohup", action='store_true', help='if want to run using nohup')
parser.add_argument(
     "--log-level",
     default=logging.ERROR,
     type=lambda x: getattr(logging, x),
     help="Configure the logging level."
     )
args = parser.parse_args()

print(args)

# Setup logger level
logger.setLevel(args.log_level)

if args.log_level == 30: # ('==> logging.WARNING: ', 30) # WARNING: 0
    logLevel = 0
elif args.log_level == 20: # ('==> logging.INFO: ', 20) # INFO: 1
    logLevel = 1
elif args.log_level == 10: # ('==> logging.DEBUG: ', 10) # DEBUG: 2
    logLevel = 2
elif args.log_level == 40:  # ('==> logging.ERROR: ', 40) # ERROR: 3
    logLevel = 3

# create a directory named "log" to save nohup outputs.
GetDirectory("log")

InputYAMLFile = args.inYAMLFile
ObsToStudy = "1D_Observables" if args.OneDOr2DObs == 1 else "2D_Observables"

f = open("CommandsRun.txt", "a") # INFO: Save commands in external file for debug purpose only
ct = datetime.datetime.now()

years = []

if  args.year == "2016":  years = ["2016"]
elif  args.year == "2017":  years = ["2017"]
elif  args.year == "2018":  years = ["2018"]
elif  args.year == "allYear":  years = ["allYear"]
#elif  args.year == "all":  years = ["2016", "2017", "2018"]
elif  args.year == "all":  years = ["2016", "2017", "2018", "allYear"]
else:
    logger.error("Invalid year. Please check!!!")

logger.info("years to run on: {}".format(years))
for year in  years:
    with open(InputYAMLFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

        if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
            logger.error('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                    Please check your YAML file format!!!'''.format(InputYAMLFile))


        if ObsToStudy in cfg['Observables']:
            for obsName, obsBin in cfg['Observables'][ObsToStudy].items():
                if (args.TestVar != "" and args.TestVar != obsName):
                    """If the test variable is given, then only run over that variable"""
                    continue
                logger.info("="*51)
                logger.info("Time now: {}".format(ct))
                logger.info("Observable: {:11} Bins: {}".format(obsName, obsBin['bins']))
                # plots/LHScanPlots/2017/D_int/
                dirSearch = 'plots/LHScanPlots/{}/{}'.format(year, obsName)
                if (args.checkDuplicate):
                    if (os.path.exists(dirSearch)):
                        logger.info("Directory {} exists".format(dirSearch))
                        continue
                    else:
                        logger.error("Directory {} does not exists".format(dirSearch))

                # create a directory to save log files, if it does not exists
                GetDirectory("log_{year}".format(year = year))

                if (args.step == 1):
                    border_msg_output = border_msg("Running efficiencies step: "+ obsName + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    for channel in args.channels:
                        logger.info("==> channel: {}".format(channel))
                        command = 'nohup python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}" -y "{year}" >& log/effs_{obsName_log}_{channel}.log &'.format(
                        # command = 'python -u efficiencyFactors.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -c "{channel}"'.format(
                            obsName = obsName, obsBins = obsBin['bins'], channel = channel, year = year, obsName_log = obsName.replace(" ","_")
                        )
                        logger.info("Command: {}".format(command))
                        f.write("\n{}\n".format(command))
                        if (args.RunCommand): os.system(command)
                    # os.system('ps -t')

                if (args.step == 2):
                    border_msg_output = border_msg("Running collect inputs: "+ obsName + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    collect(obsName, str(year))
                    logger.info("="*51)

                    #### FIXME: Currently the plotter is only working for 1D vars.
                    ###if ((not obsName.startswith("mass4l") ) and (ObsToStudy != "2D_Observables")):
                    ###    border_msg("Running plotter to plot 2D signal efficiencies")
                    ###    command = 'python python/plot2dsigeffs.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" --inYAMLFile="{inYAMLFile}" --obs="{obsToStudy}" --year={year}'.format(
                    ###        obsName = obsName, obsBins = obsBin['bins'], inYAMLFile = args.inYAMLFile, obsToStudy = args.OneDOr2DObs, year = year
                    ###    )
                    ###    logger.info("Command: {}".format(command))
                    ###    f.write("\n{}\n".format(command))
                    ###    if (args.RunCommand): os.system(command)
                    ###else:
                    ###    logger.info("Not running `plot2dsigeffs.py` as either the choosen option is `mass4l` or `2D observables`.")
                if (args.step == 3 and (ObsToStudy != "2D_Observables")):  #  Don't run this step for 2D obs for now
                    border_msg_output = border_msg("Running Interpolation to get acceptance for MH = 125. 38 GeV and obs " + obsName + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    command = ''
                    if args.nohup: command = 'nohup '
                    command += 'python python/interpolate_differential_full3.py --obsName="{obsName}" --obsBins="{obsBins}" --year={year}'.format(
                            obsName = obsName, obsBins = obsBin['bins'], year = year
                    )
                    if args.nohup: command += ' >& log_{year}/step_3_{obsName}.log &'.format(obsName = obsName, year = year)
                    print("Command: {}".format(command))
                    f.write("\n{}\n".format(command))
                    if (args.RunCommand): os.system(command)

                if (args.step == 4):
                    border_msg_output = border_msg("Running getUnc" + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    # command = 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" >& log/unc_{obsName}.log &'.format(
                    command = ''
                    if args.nohup: command = 'nohup '
                    command += 'python -u getUnc_Unc.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" -y "{year}"'.format(
                            obsName = obsName, obsBins = obsBin['bins'], year = year
                    )
                    if args.nohup: command += ' >& log_{year}/step_4_{obsName}.log &'.format(obsName = obsName, year = year)
                    logger.info("Command: {}".format(command))
                    f.write("\n{}\n".format(command))
                    if (args.RunCommand): os.system(command)

                if (args.step == 5 and (ObsToStudy != "2D_Observables")): #  Don't run this step for 2D obs for now
                    border_msg_output = border_msg("Grab NNLOPS acc & unc for MH = 125.38 GeV using the powheg sample" + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    command = 'python python/interpolate_differential_pred33.py --obsName="{obsName}" --obsBins="{obsBins}" --year={year}'.format(
                            obsName = obsName, obsBins = obsBin['bins'], year = year
                    )
                    print("Command: {}".format(command))
                    f.write("\n{}\n".format(command))
                    if (args.RunCommand): os.system(command)

                if (args.step == 6):
                    border_msg_output = border_msg("Running Background template maker: " + obsName + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    # FIXME: Check if we need modelNames in step-4 or not
                    command = ''
                    if args.nohup: command = 'nohup '
                    command += 'python -u runHZZFiducialXS.py --dir="{NtupleDir}" --obsName="{obsName}" --obsBins="{obsBins}" --modelNames {modelNames} --year="{year}" --redoTemplates --templatesOnly  --logLevel {logLevel}'.format(
                            obsName = obsName, obsBins = obsBin['bins'], NtupleDir = dirMC[year], modelNames= args.modelNames, year = year, logLevel=logLevel
                    )
                    if args.nohup: command += ' >& log_{year}/step_6_{obsName}.log &'.format(obsName = obsName, year = year)
                    logger.info("Command: {}".format(command))
                    f.write("\n{}\n".format(command))
                    if (args.RunCommand): os.system(command)

                if (args.step == 7):
                    border_msg_output = border_msg("Running final measurement and plotters: " + obsName + "   YEAR: " + str( year))
                    f.write("\n{}\n".format(border_msg_output))
                    # Copy model from model directory to combine path
                    CMSSW_BASE = os.getenv('CMSSW_BASE')
                    copyCommand = 'cp models/HZZ4L*.py {CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/python/'.format(CMSSW_BASE=CMSSW_BASE)
                    os.system(copyCommand)

                    command = ''
                    # if args.nohup: command = 'nohup '
                    command += 'python -u runHZZFiducialXS.py  --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass} --modelNames {modelNames} --year="{year}"   --logLevel {logLevel} '.format(
                    # command += 'python -u runHZZFiducialXS.py  --obsName="{obsName}" --obsBins="{obsBins}"  --calcSys --asimovMass {HiggsMass} --modelNames {modelNames} --year="{year}"   --logLevel {logLevel} --finalplotsOnly'.format(
                            obsName = obsName, obsBins = obsBin['bins'], HiggsMass = args.HiggsMass, modelNames= args.modelNames, year = year, logLevel=logLevel
                    )
                    logString = ''
                    if args.UNBLIND:
                        command += ' --unblind '
                        logString = '_unblind'
                    if (not args.checkDuplicate): command += ' |& tee  log_{year}/step_7_{obsName}{logString}.log '.format(obsName = obsName, year = year, logString = logString)
                    if (args.checkDuplicate): command += ' >&   log_{year}/step_7_{obsName}{logString}.log  '.format(obsName = obsName, year = year, logString = logString)
                    logger.info("Command: {}".format(command))
                    f.write("\n{}\n".format(command))
                    if (args.RunCommand): os.system(command)

                if (args.step == 8):
                    border_msg_output = border_msg("Running plotters: " + obsName)
                    f.write("\n{}\n".format(border_msg_output))

                    command = ''
                    if args.nohup: command = 'nohup '
                    command += 'python python/producePlots.py -l -q -b --obsName="{obsName}" --obsBins="{obsBins}" --unfoldModel="{modelNames}" --theoryMass="125.38" --year="{year}" --setLog'.format(
                            obsName = obsName, obsBins = obsBin['bins'], modelNames= args.modelNames, year = year
                    )
                    logString = ''
                    if args.UNBLIND:
                        command += ' --unblind '
                        logString = '_unblind'
                    if (not args.checkDuplicate): command += ' |& log_{year}/step_8_{obsName}{logString}.log '.format(obsName = obsName, year = year, logString = logString)
                    if args.checkDuplicate: command += ' >& log_{year}/step_8_{obsName}{logString}.log '.format(obsName = obsName, year = year, logString = logString)
                    logger.info("Command: {}".format(command))
                    f.write("\n{}\n".format(command))
                    if (args.RunCommand): os.system(command)
                # if (args.step == 9):
                #     border_msg_output = border_msg("Running impact plots: " + obsName)
                #     cmd1 = 'combineTool.py -M Impacts -d xs_125.0_{year}/SM_125_all_13TeV_xs_{obs}_bin_v3_exp.root -m 125.38 -D {toy_or_data} --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=2.5,3.5 --doInitialFit --robustFit 1'
                #     processCmd(cmd1.format(year = year, obs = obsName, toy_or_data = "toy_asimov" ) , get_linenumber(), os.path.basename(__file__))

                #     cmd2 = 'combineTool.py -M Impacts -d xs_125.0_{year}/SM_125_all_13TeV_xs_{obs}_bin_v3_exp.root -m 125.38 -D {toy_or_data} --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=2.5,3.5  --robustFit 1 --setCrossingTolerance 0.001 --autoRange 2 --doFits --parallel 4'
                #     processCmd(cmd2.format(year = year, obs = obsName, toy_or_data = "toy_asimov" ) , get_linenumber(), os.path.basename(__file__))

                #     cmd3 = 'combineTool.py -M Impacts -d xs_125.0_{year}/SM_125_all_13TeV_xs_{obs}_bin_v3_exp.root -m 125.38 -D {toy_or_data} --setParameters MH=125.38 --setParameterRanges MH=125.38,125.38:SigmaBin0=2.5,3.5  -o impacts_{obs}_{year}_{toy_or_data}.json'
                #     processCmd(cmd3.format(year = year, obs = obsName, toy_or_data = "toy_asimov" ) , get_linenumber(), os.path.basename(__file__))

                #     cmd4 = 'plotImpacts.py -i impacts_{obs}_{year}_{toy_or_data}.json -o impacts_{obs}_{year}_{toy_or_data} --POI SigmaBin0'
                #     processCmd(cmd4.format(year = year, obs = obsName, toy_or_data = "toy_asimov" ) , get_linenumber(), os.path.basename(__file__))

f.close()
