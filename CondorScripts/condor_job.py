import argparse
import os

import yaml
from Utils import bcolors as style
from Input_Info import datacardInputs


import makeTarFile

parser = argparse.ArgumentParser(description="""
    Script to submit the condor jobs:


    Example command:
    ---------------------
    # For 1D observables
    python CondorScripts/condor_job.py  -obs 1 -c longlunch -f OneDJobs --OutputPath <EOSOutPutPath> --log log_OneDJobs --tar

    # For 2D observables
    python CondorScripts/condor_job.py  -obs 2 -c tomorrow -f TwoDJobs --OutputPath <EOSOutPutPath> --log log_TwoDJobs --tar
    """, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument( '-i', dest='inYAMLFile', default="Inputs/observables_list.yml", type=str, help='Input YAML file having observable names and bin information')
parser.add_argument( '-obs', dest='OneDOr2DObs', default=1, type=int, choices=[1, 2], help="1 for 1D obs, 2 for 2D observable")
parser.add_argument('-f', dest='CondorFileName', type=str,
                    default='test',
                    help='String to be added in the output file name')
parser.add_argument('-c', dest='condorQueue', type=str,
                    default="longlunch",
                    help='The condor queue to use',
                    # Reference: https://twiki.cern.ch/twiki/bin/view/ABPComputing/LxbatchHTCondor#Queue_Flavours
                    choices=['espresso',  # 20min
                             'microcentury',  # 1h
                             'longlunch',  # 2h
                             'workday',  # 8h
                             'tomorrow',  # 1d
                             'testmatch',  # 3d
                             'nextweek'  # 1w
                             ])
parser.add_argument('--OutputPath', type=str,
                    default='/eos/user/r/rasharma/post_doc_ihep/H4LStudies/FiducialXS/test',
                    help='output path, where the CMSSW tar file and the datacard dict will be stored')
parser.add_argument('--log', type=str,
                    default='condor_logs',
                    help='output path, where the CMSSW tar file and the datacard dict will be stored')
parser.add_argument('--tar', dest="ifTar", action='store_true', help='if want to run using nohup')
parser.add_argument( '-y', dest='year', default=2018, type=int, help='dataset year')
parser.add_argument( '-j', dest='jobType', default="eff", choices=['eff','unc'], help='dataset year')
args = parser.parse_args()

datacardInputs = datacardInputs.format(year = args.year)

def CreateCMSSWTarFile(OutputPath_):
    """Create tarball of present working CMSSW base directory
    and send it to the EOS.

    This tarball will be called by the main condor job for the processing.
    """
    # create tarball of present working CMSSW base directory
    os.system('rm -f CMSSW*.tgz')

    # Get CMSSW directory path and name
    cmsswDirPath = os.environ['CMSSW_BASE']
    CMSSWRel = cmsswDirPath.split("/")[-1]
    makeTarFile.make_tarfile(cmsswDirPath, CMSSWRel + ".tgz")
    print "copying the " + CMSSWRel + ".tgz  file to eos path: " + OutputPath_ + "\n"
    os.system('mv ' + CMSSWRel + ".tgz" + ' ' + OutputPath_ + '/' + CMSSWRel + ".tgz")

def GetArgumentTextFile(InputYAMLFile = "", OneDOr2DObs = "", fileName = "test", year = "2018"):
    ObsToStudy = "1D_Observables" if OneDOr2DObs == 1 else "2D_Observables"

    with open(InputYAMLFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

        if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
            print('''No section named 'observable' or sub-section name '1D-Observable' found in file {}.
                    Please check your YAML file format!!!'''.format(InputYAMLFile))

        if ObsToStudy in cfg['Observables']:
            arguments = []
            for obsName, obsBin in cfg['Observables'][ObsToStudy].items():
                print("Observable: {:11} Bins: {}".format(obsName, obsBin['bins']))
                for channel in ["4mu", "4e", "2e2mu", "4l"]:
                    """For 2D observables there is space in between the observable name. And condor argument unable to take it
                    as one argument. So, replacing spaces with "==". And we need to undo this before running the efficiency module"
                    """
                    arguments.append('{} {} {} {}'.format(obsName.replace(' ','=='), channel.replace(' ','=='), obsBin["bins"].replace(' ','=='), year))

            with open(fileName+".txt", "w") as args:
                args.write("\n".join(arguments))

def condorJDLFile(fileName = "test",
                            logFilePath = "condor_logs",
                            logFileName = "output",
                            JobFlavour = "espresso"):
    if not os.path.isdir(logFilePath): os.mkdir(logFilePath)

    outJdl = open(fileName+'.jdl','w')
    outJdl.write('executable = '+fileName+'.sh')
    outJdl.write('\n'+'should_transfer_files = YES')
    outJdl.write('\n'+'transfer_input_files = '+fileName+'.sh, '+fileName+'.txt')
    outJdl.write('\n'+'when_to_transfer_output = ON_EXIT')
    # outJdl.write('\n'+'x509userproxy = $ENV(X509_USER_PROXY)')
    outJdl.write('\n'+'+JobFlavour = "'+JobFlavour+'"')
    outJdl.write('\n'+'+AccountingGroup        = "group_u_CMS.CAF.ALCA"')
    # if request_memory != 0: outJdl.write('\n'+'request_memory = '+str(request_memory))
    # if request_cpus != 0: outJdl.write('\n'+'request_cpus = '+ str(request_cpus))
    outJdl.write('\n'+'output = '+logFilePath+os.sep+logFileName+'_$(ClusterId)_$(ProcId).stdout')
    outJdl.write('\n'+'error  = '+logFilePath+os.sep+logFileName+'_$(ClusterId)_$(ProcId).stdout')
    outJdl.write('\n'+'log  = '+logFilePath+os.sep+logFileName+'_$(ClusterId)_$(ProcId).log')
    outJdl.write('\n'+'queue arguments from '+fileName+'.txt')
    outJdl.close()

def condorSHFile(fileName = "test",
                        EOSPath = "/eos/",
                        CMSSW = "CMSSW_10_2_13"):
    outSHFile = open(fileName+".sh","w");
    outSHFile.write('#!/bin/sh -e')
    outSHFile.write('\n'+'obsName=$1')
    outSHFile.write('\n'+'channel=$2')
    outSHFile.write('\n'+'obsBins=$3')
    outSHFile.write('\n'+'year=$4')
    outSHFile.write('\n'+'echo "Input arguments: "')
    outSHFile.write('\n'+'echo "obsName: ${obsName}"')
    outSHFile.write('\n'+'echo "channel: ${channel}"')
    outSHFile.write('\n'+'echo "obsBins: ${obsBins}"')
    outSHFile.write('\n'+'echo "year: ${year}"')
    outSHFile.write('\n'+'')
    outSHFile.write('\n'+'obsName=$(echo ${obsName} | sed "s/==/ /g")')
    outSHFile.write('\n'+'channel=$(echo ${channel} | sed "s/==/ /g")')
    outSHFile.write('\n'+'obsBins=$(echo ${obsBins} | sed "s/==/ /g")')
    outSHFile.write('\n'+'year=$(echo ${year} | sed "s/==/ /g")')
    outSHFile.write('\n'+'')
    outSHFile.write('\n'+'echo "Input arguments: "')
    outSHFile.write('\n'+'echo "obsName: ${obsName}"')
    outSHFile.write('\n'+'echo "channel: ${channel}"')
    outSHFile.write('\n'+'echo "obsBins: ${obsBins}"')
    outSHFile.write('\n'+'echo "year: ${year}"')
    outSHFile.write('\n'+'')
    outSHFile.write('\n'+'cp '+EOSPath+'/'+CMSSW+'.tgz .')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'ls')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'tar -xf CMSSW_10_2_13.tgz')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'ls')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'rm CMSSW_10_2_13.tgz')
    outSHFile.write('\n'+'cd CMSSW_10_2_13/src/')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'ls')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'scramv1 b ProjectRename')
    outSHFile.write('\n'+'eval `scram runtime -sh`')
    outSHFile.write('\n'+'cd Fiducial_XS')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'ls')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'eval `scramv1 runtime -sh`')
    outSHFile.write('\n'+'# load necessary modules in the python PATH')
    outSHFile.write('\n'+'export PYTHON27PATH=$PYTHON27PATH:$(pwd)/python')
    outSHFile.write('\n'+'export PYTHON27PATH=$PYTHON27PATH:$(pwd)/Inputs')
    outSHFile.write('\n'+'')
    outSHFile.write('\n'+'export PYTHONPATH=$PYTHONPATH:$(pwd)/python')
    outSHFile.write('\n'+'export PYTHONPATH=$PYTHONPATH:$(pwd)/Inputs')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'rm -rf %s'%(datacardInputs))
    outSHFile.write('\n'+'ls')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'echo "Start of efficiency script"')
    outSHFile.write('\n'+'date')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'python -u efficiencyFactors.py -l -q -b --obsName="${obsName}" --obsBins="${obsBins}" -c "${channel}" -y "${year}"')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'date')
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'echo "content of datacard directory: "')
    outSHFile.write('\n'+'ls {}'.format(datacardInputs))
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'echo "Copy datacardInputs directory to eos"')
    outSHFile.write('\n'+'cp -r {datacardInputs}/*  {EOSPath}/{datacardInputs}/'.format(datacardInputs = datacardInputs, EOSPath = EOSPath))
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'echo "content of eos datacard directory: "')
    outSHFile.write('\n'+'ls  {EOSPath}/{datacardInputs}'.format(datacardInputs = datacardInputs, EOSPath = EOSPath))
    outSHFile.write('\n'+'echo "==============="')
    outSHFile.write('\n'+'echo -e "DONE"')
    outSHFile.close()
    os.system("chmod 777 " + fileName + ".sh")


if __name__ == "__main__":

    # Create necessary directory that we need
    if not os.path.isdir(args.log): os.mkdir(args.log)
    if not os.path.isdir(args.OutputPath): os.mkdir(args.OutputPath)
    if not os.path.isdir(args.OutputPath + "/{}".format(datacardInputs)): os.makedirs(args.OutputPath + "/{}".format(datacardInputs))

    if args.jobType = "unc":
        # Step-1: Check if the efficiency dict exists?
        # Step-2: Check if the collect input run or not?
        pass
    if args.ifTar or  args.jobType = "unc":
        CreateCMSSWTarFile(args.OutputPath)
    GetArgumentTextFile(InputYAMLFile = args.inYAMLFile,
                                fileName = args.CondorFileName,
                                OneDOr2DObs = args.OneDOr2DObs,
                                year = args.year)
    condorJDLFile(fileName = args.CondorFileName,
                            JobFlavour = args.condorQueue,
                            logFilePath=args.log)
    condorSHFile(fileName = args.CondorFileName, EOSPath = args.OutputPath)

    print "===> Set Proxy Using:";
    print "\tvoms-proxy-init --voms cms --valid 168:00";
    print "\"condor_submit "+args.CondorFileName+".jdl\" to submit";
