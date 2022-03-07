#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.10.16
#-----------------------------------------------
import json
import math
import optparse
import os
import sys
from decimal import *
from inspect import currentframe
from subprocess import *

from ROOT import *

# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from createXSworkspace import createXSworkspace
from higgs_xsbr_13TeV import *
from sample_shortnames import *


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

# NOTE: append the directory `datacardInputs`, as .py files inside is going to load using import.
#       load XS-specific modules
sys.path.append('./'+datacardInputs)


### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',      dest='SOURCEDIR',type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--asimovModelName',dest='ASIMOVMODEL',type='string',default='SM_125', help='Name of the Asimov Model')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.09', help='Asimov Mass')
    parser.add_option('',   '--modelNames',dest='MODELNAMES',type='string',default="SM_125,SMup_125,SMdn_125",help='Names of models for unfolding, separated by , (comma) . Default is "SM_125"')
    parser.add_option('',   '--fixMass',  dest='FIXMASS',  type='string',default='125.09',   help='Fix mass, default is a string "125.09" or can be changed to another string, e.g."125.6" or "False"')
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--fixFrac', action='store_true', dest='FIXFRAC', default=False, help='fix the fractions of 4e and 4mu when extracting the results, default is False')
    # action options - "redo"
    parser.add_option('',   '--redoEff',       action='store_true', dest='redoEff',      default=False, help='Redo the eff. factors, default is False')
    parser.add_option('',   '--redoTemplates', action='store_true', dest='redoTemplates',default=False, help='Redo the bkg shapes and fractions, default is False')
    # action options - "only"
    parser.add_option('',   '--effOnly',       action='store_true', dest='effOnly',       default=False, help='Extract the eff. factors only, default is False')
    parser.add_option('',   '--templatesOnly', action='store_true', dest='templatesOnly', default=False, help='Prepare the bkg shapes and fractions only, default is False')
    parser.add_option('',   '--uncertOnly',    action='store_true', dest='uncertOnly',    default=False, help='Extract the uncertanties only, default is False')
    parser.add_option('',   '--resultsOnly',   action='store_true', dest='resultsOnly',   default=False, help='Run the measurement only, default is False')
    parser.add_option('',   '--finalplotsOnly',action='store_true', dest='finalplotsOnly',default=False, help='Make the final plots only, default is False')
    # action options - do Z4l measurement
    parser.add_option('',   '--doZ4l',         action='store_true', dest='doZ4l',         default=False, help='Perform the Z->4l measurement instead of H->4l, default is False')
    parser.add_option('',   '--doRatio',       action='store_true', dest='doRatio',       default=False, help='Do H4l/Z4l ratio, default is False')
    # Unblind option
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    # Calculate Systematic Uncertainties
    parser.add_option('',   '--calcSys', action='store_true', dest='SYS', default=False, help='Calculate Systematic Uncertainties (in addition to stat+sys)')
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    parser.add_option('',   '--inYAMLFile', dest='inYAMLFile', type='string', default="Inputs/observables_list.yml", help='Input YAML file having observable names and bin information')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

    # prepare the global flag if all the step should be run
    runAllSteps = not(opt.effOnly or opt.templatesOnly or opt.uncertOnly or opt.resultsOnly or opt.finalplotsOnly)

    if (opt.OBSBINS=='' and opt.OBSNAME!='inclusive'):
        parser.error('Bin boundaries not specified for differential measurement. Exiting...')
        sys.exit()

    # FIXME: Check why we need these directories
    #        The directory `combineOutputs` is used to keep the generated workspaces
    if not os.path.isdir(combineOutputs): os.mkdir(combineOutputs)
    #dirToExist = ['templates','datacardInputs','125.6','xs_125.6']
    dirToExist = ['templates', datacardInputs, '125.0', combineOutputs]
    for dir in dirToExist:
        if not os.path.isdir(os.getcwd()+'/'+dir+'/'):
            parser.error(os.getcwd()+'/'+dir+'/ is not a directory. Exiting...')
            sys.exit()

### Define function for processing of os command
def processCmd(cmd, lineNumber, quiet = 0):
    """This function is defined for processing of os command

    Args:
        cmd (str): The command to be run on the terminal
        lineNumber (int): The line number from where this function was invoked
        quiet (int, optional): Want to run the command in quite mode (Don't print anything) or print everything. Defaults to 0.

    Raises:
        RuntimeError: If the command failed then exit the program with exit code

    Returns:
        str: The full output of the command
    """
    output = '\n'
    print("="*51)
    print("[INFO]: Current working directory: {0}".format(os.getcwd()))
    print("[INFO]: {}#{} command:\n\t{}".format(os.path.basename(__file__), lineNumber, cmd))
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        # FIXME: We don't need print statement here
        #        If quite mode is set to 1 then it won't
        #        print anything, if not then it will enter
        #        the condition `if (not quite)` below and print outputs
        # print (line, end=' ') # works with python3
        # print line,
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))

    if (not quiet):
        print ('Output:\n   [{}] \n'.format(output))
    return output

### Extract the all efficiency factors (inclusive/differential, all bins, all final states)
def extractFiducialEfficiencies(obsName, observableBins, modelName):
    """Extract efficiencies and plot the 2D signal efficiency

    Args:
        obsName (str): name of the observable
        observableBins (array): Array containing the bin boundaries
        modelName (str): Name of model. For example SM_125, SMup_125, etc.
    """

    #from inputs_bkg_{obsName} import fractionsBackground and observableBins
    if (not opt.redoEff):
        print ('[Skipping eff. and out.factors for '+str(obsName)+']')
        return

    print ('[Extracting eff. and out.factors]')
    #cmd = 'python efficiencyFactors.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b'
    cmd = 'python efficiencyFactors.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b --doPlots --doFit'
    output = processCmd(cmd, get_linenumber())
    print (output)
    if (not opt.OBSNAME.startswith("mass4l")):
        cmd = 'python plot2dsigeffs.py -l -q -b --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'"'
        output = processCmd(cmd, get_linenumber())

### Extract the templates for given obs, for all bins and final states (differential)
def extractBackgroundTemplatesAndFractions(obsName, observableBins):
    global opt

    print("[INFO] Obs Name: {:15}\tBins: {}".format(obsName, observableBins))

    fractionBkg = {}; lambdajesdnBkg={}; lambdajesupBkg={}
    #if exists, from inputs_bkg_{obsName} import observableBins, fractionsBackground, jesLambdaBkgUp, jesLambdaBkgDn
    if os.path.isfile(datacardInputs+'/inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName+'.py'):
        _temp = __import__('inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName, globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1)
        if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
            print ('[Fractions already exist for the given binning. Skipping templates/shapes... ]')
            return
        if (hasattr(_temp,'fractionsBackground') and hasattr(_temp,'lambdajesupBkg') and hasattr(_temp,'lambdajesdnBkg')):
            fractionBkg = _temp.fractionsBackground
            lambdajesupBkg = _temp.lambdajesupBkg
            lambdajesdnBkg = _temp.lambdajesdnBkg

    print('[INFO] Preparing bkg shapes and fractions, for bins with boundaries {}'.format(observableBins))
    # save/create/prepare directories and compile templates script
    # FIXME: directory name hardcoded
    currentDir = os.getcwd(); os.chdir('./templates/')

    print("==> Compile the package main_fiducialXSTemplates...")
    cmd = 'make'; processCmd(cmd, get_linenumber())
    DirectoryToCreate = 'templatesXS/DTreeXS_'+opt.OBSNAME+'/13TeV/'
    print('[INFO] Create directory: {}'.format(DirectoryToCreate))
    print('[INFO] compile the script inside the template directory')
    cmd = 'mkdir -p '+DirectoryToCreate; processCmd(cmd, get_linenumber(),1)

    # extract bkg templates and bin fractions
    sZZname2e2mu = 'ZZTo2e2mu_powheg'
    sZZname4mu = 'ZZTo4mu_powheg'
    sZZname4e = 'ZZTo4e_powheg'

    if (opt.doZ4l):
        """If Z->4l analysis is set true
        """
        sZZname2e2mu = 'ZZTo2e2mu_powheg_tchan'
        sZZname4mu = 'ZZTo4mu_powheg_tchan'
        sZZname4e = 'ZZTo4e_powheg_tchan'

    # FIXME: Explain each name for documentation
    bkg_sample_tags = ['ZX4l_CR', 'ZX4l_CR_4e', 'ZX4l_CR_4mu', 'ZX4l_CR_2e2mu', sZZname2e2mu, sZZname4e, sZZname4mu,'ggZZ_2e2mu_MCFM67', 'ggZZ_4e_MCFM67', 'ggZZ_4mu_MCFM67']
    bkg_samples_shorttags = {sZZname2e2mu:'qqZZ', sZZname4e:'qqZZ', sZZname4mu:'qqZZ', 'ggZZ_2e2mu_MCFM67':'ggZZ', 'ggZZ_4e_MCFM67':'ggZZ', 'ggZZ_4mu_MCFM67':'ggZZ', 'ZX4l_CR':'ZJetsCR', 'ZX4l_CR_4e':'ZJetsCR', "ZX4l_CR_4mu":'ZJetsCR', 'ZX4l_CR_2e2mu':'ZJetsCR'}
    bkg_samples_fStates = {sZZname2e2mu:'2e2mu', sZZname4e:'4e', sZZname4mu:'4mu', 'ggZZ_2e2mu_MCFM67':'2e2mu', 'ggZZ_4e_MCFM67':'4e', 'ggZZ_4mu_MCFM67':'4mu', 'ZX4l_CR':'AllChans', 'ZX4l_CR_4e':'4e', 'ZX4l_CR_4mu':'4mu', 'ZX4l_CR_2e2mu':'2e2mu'}

    print('[INFO] Loop over each background sample tags: \n\t{}\n'.format(bkg_sample_tags))
    for sample_tag in bkg_sample_tags:
        tmpObsName = obsName
        tmpSrcDir = opt.SOURCEDIR
        if (sample_tag=='ZX4l_CR'):
            # tmpSrcDir = '/eos/user/v/vmilosev/Skim_2018_HZZ/WoW'
            tmpSrcDir = opt.SOURCEDIR # FIXME: if the paths for ZX CR is different then we need to update this
        # FIXME: Try to understand this syntax
        fitTypeZ4l = [['none','doRatio'],['doZ4l','doZ4l']][opt.doZ4l][opt.doRatio]
        cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 13TeV templatesXS DTreeXS ' + fitTypeZ4l+ ' 0'
        output = processCmd(cmd, get_linenumber())
        print('###\n[INFO] output: \n\t{}\n###'.format(output))

        tmp_fracs = output.split("[Bin fraction: ")
        print('[INFO] tmp_fracs: {}'.format(tmp_fracs))
        print('[INFO] Length of observables bins: {}'.format(len(observableBins)))

        for obsBin in range(0,len(observableBins)-1):
            fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
            tmpFrac = float(tmp_fracs[obsBin+1].split("][end fraction]")[0])
            if not math.isnan(tmpFrac):
                fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac
            if (('jet' in obsName) and tmpFrac!=0 and not math.isnan(tmpFrac)):
                tmpFrac_up =float(tmp_fracs[obsBin+1].split("Bin fraction (JESup): ")[1].split("]")[0])
                tmpFrac_dn =float(tmp_fracs[obsBin+1].split("Bin fraction (JESdn): ")[1].split("]")[0])
                if not math.isnan(tmpFrac_up):
                    lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_up/tmpFrac - 1
                if not math.isnan(tmpFrac_dn):
                    lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_dn/tmpFrac - 1

    os.chdir(currentDir)
    with open(datacardInputs+'/inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName+'.py', 'w') as f:
        f.write('observableBins = '     +json.dumps(observableBins)+';\n')
        f.write('fractionsBackground = '+json.dumps(fractionBkg)   +';\n')
        f.write('lambdajesupBkg = '     +json.dumps(lambdajesupBkg)+';\n')
        f.write('lambdajesdnBkg = '     +json.dumps(lambdajesdnBkg)+';\n')


### Extract the XS-specific uncertainties for given obs and bin, for all final states (differential)
def extractUncertainties(obsName, observableBinDn, observableBinUp):
    """This function should compute the uncertanities
       THis is now computed using a separate script named `getUnc_Unc.py`
       I am keeping this, thinking that later we will keep only this and remove the
       script `RunEverything.py`
       # FIXME
    """
    print ('[Extracting uncertainties  -  range ('+observableBinDn+', '+observableBinUp+')]')
    cmd = 'some command...with some parameters...'
    #processCmd(cmd, get_linenumber())

### Produce datacards for given obs and bin, for all final states
def produceDatacards(obsName, observableBins, modelName, physicalModel):
    """Produce workspace/datacards for the given observable and bins

    Args:
        obsName (str): Name of observable
        observableBins (array): Array having bin boundaries
        modelName (str): Name of model. For example: SM_125
        physicalModel (str): version of model, for example: v2
    """

    print ('[INFO] Producing workspace/datacards for obsName - '+obsName+', bins - '+str(observableBins)+']')
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    for fState in fStates:
        # print ("INFO::: VM Creating datacards for nBins = {}".format(nBins))
        print('[INFO] VM Creating datacards for:\n\tobsName: {obsName}\n\tfState: {fState}\n\tnBins: {nBins}\n\tobservableBins: {observableBins}\n\tmodelName: {modelName}\n\tphysicalModel: {physicalModel}'.format(
                obsName = obsName , fState = fState , nBins = nBins , observableBins = observableBins , modelName = modelName , physicalModel = physicalModel
                ))
        if (not obsName.startswith("mass4l")):
            os.system("python python/datacard_maker.py -c {} -b {}".format(fState, nBins - 1))
            for obsBin in range(nBins-1):
                # first bool = cfactor second bool = add fake H               #
                ndata = createXSworkspace(obsName,fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel)
                os.system("cp xs_125.0_"+str(nBins - 1)+"bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                os.system("sed -i 's~_xs.Databin"+str(obsBin)+"~_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+"~g' "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                if ("jet" in obsName):
                    os.system("sed -i 's~\#JES param~JES param~g' "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")

                os.system("sed -i 's~0.0 0.2~0.0 0.2 [-1,1]~g' "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")


        else:
            os.system("python python/datacard_maker.py -c {} -b {}".format(fState, 1))
            ndata = createXSworkspace(obsName,fState, nBins, 0, observableBins, False, True, modelName, physicalModel)
            if obsName=='mass4l': os.system("cp xs_125.0_1bin/hzz4l_"+fState+"S_13TeV_xs_inclusive_bin0.txt "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
            if obsName=='mass4lREFIT': os.system("cp xs_125.0_1bin/hzz4l_"+fState+"S_13TeV_xs_inclusiveREFIT_bin0.txt "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
            os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
            os.system("sed -i 's~_xs.Databin0~_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin0~g' "+combineOutputs+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")

### Create the asimov dataset and return fit results
def createAsimov(obsName, observableBins, modelName, resultsXS, physicalModel):
    """Create the Asimov dataset and return the fit results.

    Args:
        obsName (str): Name of observable
        observableBins (array): Array having bin boundaries
        modelName (str): Name of model
        resultsXS (_type_): _description_
        physicalModel (_type_): _description_
    """
    print ('[Producing/merging workspaces and datacards for obsName '+obsName+' using '+modelName+']')

    # Run combineCards and text2workspace
    currentDir = os.getcwd(); os.chdir('./'+combineOutputs+'/') # FIXME: Hardcoded directory
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    print('[INFO] nBins: {}'.format(nBins))
    for fState in fStates:
        if (nBins>1):
            cmd = 'combineCards.py '
            for obsBin in range(nBins-1):
                cmd = cmd + 'hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '
            cmd = cmd + '> hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
            processCmd(cmd, get_linenumber(),1)
        else:
            # FIXME: Did not get why this line is here?
            #        If we need this then why we are not running this command?
            cmd = 'cp hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin0_'+physicalModel+'.txt hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'

    # combine 3 final state cards
    cmd = 'combineCards.py hzz4l_4muS_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_4eS_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_2e2muS_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt > hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
    processCmd(cmd, get_linenumber(),1)
    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')

    # FIXME: put this mkdir command at appropriate place
    # workspacesDir = "workspaces"
    # if not os.path.isdir(workspacesDir): os.mkdir(workspacesDir)
    # text-to-workspace
    if (physicalModel=="v2"):
        #if (opt.FIXMASS=="False"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        #else:
        #cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange='+opt.ASIMOVMASS+','+opt.ASIMOVMASS+' --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber())

    # FIXME: don't copy file to the one back directory; and try to make combine command work by fixing paths
    cmd = 'mv hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
    processCmd(cmd, get_linenumber())

    os.chdir(currentDir)

    # import acc factors
    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc

    # Run the Combine
    if (physicalModel=="v2"):
        #if (opt.FIXMASS=="False"):
        cmd =  'combine -n '+obsName+' -M MultiDimFit  '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root -m '+opt.ASIMOVMASS+' --setParameters '
        print("="*51)
        print("[INFO]: {}#{} command:\n\t{}".format(os.path.basename(__file__),get_linenumber(),cmd))
        #else:
        #cmd =  'combine -n '+obsName+' -M MultiDimFit  '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root -m '+opt.ASIMOVMASS+' --PO higgsMassRange='+opt.ASIMOVMASS+','+opt.ASIMOVMASS+' --setParameters '
        for fState in fStates:
            nBins = len(observableBins)
            for obsBin in range(nBins-1):
                fidxs = 0
                fidxs += higgs_xs['ggH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                #fidxs += acc['ggH_HRes_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['VBF_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['VBF_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['WH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['ZH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['ttH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                cmd = cmd + 'r'+fState+'Bin'+str(obsBin)+'='+str(fidxs)+','
        cmd =  cmd+ 'MH='+opt.ASIMOVMASS
        print("="*51)
        print("[INFO]: {}#{} command:\n\t{}".format(os.path.basename(__file__),get_linenumber(),cmd))
        for fState in fStates:
            nBins = len(observableBins)
            for obsBin in range(nBins-1):
                cmd = cmd + ' -P r'+fState+'Bin'+str(obsBin)
        if (opt.FIXMASS=="False"):
            cmd = cmd + ' -P MH '
        else:
            cmd = cmd + ' --floatOtherPOIs=0'
        print("="*51)
        print("[INFO]: {}#{} command:\n\t{}".format(os.path.basename(__file__),get_linenumber(),cmd))
        cmd = cmd +' -t -1 --saveWorkspace --saveToys'
        if not os.path.isdir(combineOutputs): os.mkdir(combineOutputs)
        # cmd = cmd + ' --out ' + combineOutputs # FIXME: redirect log files from combine script to `combineOutputs` directory
        #cmd += ' --X-rtd TMCSO_PseudoAsimov=1000000'
        #cmd += ' --freezeNuisanceGroups r4muBin0,r4eBin0,r2e2muBin0'
        output = processCmd(cmd, get_linenumber())
        processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs+'/'+modelName+'_all_'+obsName+'_13TeV_Asimov_'+physicalModel+'.root', get_linenumber(), 1)
        #cmd = cmd.replace(' --freezeNuisanceGroups r4muBin0,r4eBin0,r2e2muBin0','')
        #cmd = cmd.replace(' --X-rtd TMCSO_PseudoAsimov=1000000','')
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        output = processCmd(cmd, get_linenumber())
        lsCMD = "ls *.root"
        processCmd(lsCMD, get_linenumber())
        processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs+'/', get_linenumber())

    # parse the results for all the bins and the given final state
    tmp_resultsXS = {}
    for fState in fStates:
        for obsBin in range(len(observableBins)-1):
            binTag = str(obsBin)
            tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag] = parseXSResults(output,'r'+fState+'Bin'+str(obsBin)+' :')


    # merge the results for 3 final states, for the given bins
    for obsBin in range(len(observableBins)-1):
        binTag = str(obsBin)
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
        for fState in fStates:
            resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
        tmp_central = 0.0
        tmp_uncerDn = 0.0
        tmp_uncerUp = 0.0
        for fState in fStates:
            tmp_central += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['central']
            tmp_uncerDn += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerDn']**2
            tmp_uncerUp += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerUp']**2
            resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag]['central'] = float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['central']))
            resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag]['uncerDn'] = -float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerDn']))
            resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag]['uncerUp'] = +float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerUp']))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['central'] = float("{0:.5f}".format(tmp_central))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['uncerDn'] = -float("{0:.5f}".format(tmp_uncerDn**0.5))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['uncerUp'] = +float("{0:.5f}".format(tmp_uncerUp**0.5))

    # run combine with no systematics for stat only uncertainty
    if (opt.SYS):
#Test VM:        cmd = cmd + ' --freezeNuisanceGroups CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 --freezeParameters allConstrainedNuisances'
        cmd = cmd + ' --freezeParameters allConstrainedNuisances'
        output = processCmd(cmd, get_linenumber())

        # FIXME: The current combine command and the previous
        #        combine command generates output with exactly same name (obvious).
        #        But, we are not renaming them so its updated with current command.
        #        check if this is fine?
        print("="*51)
        lsCMD = 'echo "ls *.root";ls *.root'
        processCmd(lsCMD, get_linenumber())
        processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs+'/', get_linenumber())


        for fState in fStates:
            for obsBin in range(len(observableBins)-1):
                binTag = str(obsBin)
                tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly'] = parseXSResults(output,'r'+fState+'Bin'+str(obsBin)+' :')

        # merge the results for 3 final states, for the given bins
        for obsBin in range(len(observableBins)-1):
            binTag = str(obsBin)
            resultsXS['AsimovData_'+obsName+'_genbin'+binTag+'_statOnly'] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
            for fState in fStates:
                resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag+'_statOnly'] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
            tmp_central = 0.0
            tmp_uncerDn = 0.0
            tmp_uncerUp = 0.0
            for fState in fStates:
                tmp_central += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly']['central']
                tmp_uncerDn += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly']['uncerDn']**2
                tmp_uncerUp += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly']['uncerUp']**2
                resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag+'_statOnly']['central'] = float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly']['central']))
                resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag+'_statOnly']['uncerDn'] = -float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly']['uncerDn']))
                resultsXS['AsimovData_'+obsName+'_'+fState+'_genbin'+binTag+'_statOnly']['uncerUp'] = +float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly']['uncerUp']))
            resultsXS['AsimovData_'+obsName+'_genbin'+binTag+'_statOnly']['central'] = float("{0:.5f}".format(tmp_central))
            resultsXS['AsimovData_'+obsName+'_genbin'+binTag+'_statOnly']['uncerDn'] = -float("{0:.5f}".format(tmp_uncerDn**0.5))
            resultsXS['AsimovData_'+obsName+'_genbin'+binTag+'_statOnly']['uncerUp'] = +float("{0:.5f}".format(tmp_uncerUp**0.5))

    return resultsXS

# parse the fit results from the MultiDim fit output "resultLog", for the bin and final state designated by "rTag"
def parseXSResults(resultLog, rTag):
    try:
        fXS_c = float(resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" ")[0])
        fXS_d = float('-'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[0])
        fXS_u = float('+'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[1])
        fXS = {'central':fXS_c, 'uncerDn':fXS_d, 'uncerUp':fXS_u}
        return fXS
    except IndexError:
        print ("Parsing Failed!!! Inserting dummy values!!! check log!!!")
        fXS = {'central':-1.0, 'uncerDn':0.0, 'uncerUp':0.0}
        return fXS

### Extract the results and do plotting
def extractResults(obsName, observableBins, modelName, physicalModel, asimovModelName, asimovPhysicalModel, resultsXS):
    # Run combineCards and text2workspace
    print ('[Producing/merging workspaces and datacards for obsName '+obsName+']')

    currentDir = os.getcwd(); os.chdir(combineOutputs)
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    for fState in fStates:
        cmd = 'combineCards.py '
        for bin in range(nBins-1):
            cmd = cmd+'hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin'+str(bin)+'_'+physicalModel+'.txt '
        cmd = cmd + '> hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
        processCmd(cmd, get_linenumber(),1)

    cmd = 'combineCards.py hzz4l_4muS_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_4eS_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt hzz4l_2e2muS_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt > hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
    processCmd(cmd, get_linenumber(),1)

    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')

    if (physicalModel=="v2"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber())
    if (physicalModel=="v3"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducialV3 --PO higgsMassRange=115,135 --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber())

    cmd = 'mv hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
    processCmd(cmd, get_linenumber(),1)

    os.chdir(currentDir)

    cmd = 'root -l -b -q "src/addToyDataset.C(\\"'+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root\\",\\"'+combineOutputs+'/'+asimovModelName+'_all_'+obsName+'_13TeV_Asimov_'+asimovPhysicalModel+'.root\\",\\"toy_asimov\\",\\"'+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root\\")"'
    processCmd(cmd, get_linenumber())

    # Run the Combine
    if (physicalModel=="v3"):
        if (not opt.FIXFRAC):
            if (opt.FIXMASS=="False"):
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m 125.0 -D toy_asimov '
            else:
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m '+opt.FIXMASS+' -D toy_asimov --setParameters MH='+opt.FIXMASS
            # you can add fractions to the POIs if you want the uncertainties on frac4e, frac4mu
            for bin in range(nBins-1):
                cmd = cmd + ' -P SigmaBin'+str(bin)
                #cmd = cmd + ' -P SigmaBin'+str(bin)+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)
            if (opt.FIXMASS=="False"):
                cmd = cmd + ' -P MH'
            cmd = cmd + ' --floatOtherPOIs=1 --saveWorkspace'
            if (not opt.FIXMASS=="False"):
                cmd = cmd + ' --setParameterRanges MH='+opt.FIXMASS+','+opt.FIXMASS#+'001'
                #cmd = cmd + ' --freezeNuisanceGroups MH '
            if (opt.UNBLIND):
                #cmd = cmd.replace('_exp','')
                cmd = cmd.replace('-D toy_asimov',' ')
            output=processCmd(cmd, get_linenumber())
            if (opt.FIXMASS=="False"):
                processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH125.root '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root', get_linenumber(), 1)
            else:
                processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.FIXMASS.replace('.0.root','.root')+'.root '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root', get_linenumber(), 1)
            cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
            output=processCmd(cmd, get_linenumber())

        else:
            # import acc factors
            _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc'], -1)
            acc = _temp.acc

            tmp_xs = {}
            tmp_xs_sm = {}
            nBins = len(observableBins)
            for fState in fStates:
                for obsBin in range(nBins-1):
                    fidxs_sm = 0
                    fidxs_sm += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    #fidxs_sm += acc['ggH_HRes_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs = 0
                    if (not opt.FIXMASS=="False"):
                        fidxs += higgs_xs['ggH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        #fidxs += acc['ggH_HRes_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['VBF_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['WH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['ZH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['ttH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    else: fidxs = fidxs_sm

                    tmp_xs_sm[fState+'_genbin'+str(obsBin)] = fidxs_sm

                    if (opt.FIXMASS=="False"):
                        tmp_xs[fState+'_genbin'+str(obsBin)] = fidxs_sm
                    else:
                        tmp_xs[fState+'_genbin'+str(obsBin)] = fidxs

            if (opt.FIXMASS=="False"):
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m 125.0 -D toy_asimov  --setParameters '
            else:
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m '+opt.FIXMASS+' -D toy_asimov --setParameters MH='+opt.FIXMASS+','
            for obsBin in range(nBins-1):
                fidxs4e = tmp_xs['4e_genbin'+str(obsBin)]
                fidxs4mu = tmp_xs['4mu_genbin'+str(obsBin)]
                fidxs2e2mu = tmp_xs['2e2mu_genbin'+str(obsBin)]
                frac4e = fidxs4e/(fidxs4e+fidxs4mu+fidxs2e2mu)
                frac4mu = fidxs4mu/(fidxs4e+fidxs4mu+fidxs2e2mu)
                fidxs4e_sm = tmp_xs_sm['4e_genbin'+str(obsBin)]
                fidxs4mu_sm = tmp_xs_sm['4mu_genbin'+str(obsBin)]
                fidxs2e2mu_sm = tmp_xs_sm['2e2mu_genbin'+str(obsBin)]
                frac4e_sm = fidxs4e_sm/(fidxs4e_sm+fidxs4mu_sm+fidxs2e2mu_sm)
                frac4mu_sm = fidxs4mu_sm/(fidxs4e_sm+fidxs4mu_sm+fidxs2e2mu_sm)
                K1 = frac4e/frac4e_sm
                K2 = frac4mu/frac4mu_sm * (1.0-frac4e_sm)/(1.0-frac4e)
                cmd = cmd + 'K1Bin'+str(obsBin)+'='+str(K1)+',K2Bin'+str(obsBin)+'='+str(K2)+','
            cmd = cmd.rstrip(',')
            for bin in range(nBins-1):
                #cmd = cmd + ' -P SigmaBin'+str(bin)+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)
                cmd = cmd + ' -P SigmaBin'+str(bin)#+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)

            if (opt.FIXMASS=="False"):
                cmd = cmd+' -P MH --floatOtherPOIs=1'
            else:
                cmd = cmd+' --floatOtherPOIs=1'

            cmd = cmd + ' --saveWorkspace --setParameterRanges '
            for obsBin in range(nBins-1):
                fidxs4e = tmp_xs['4e_genbin'+str(obsBin)]
                fidxs4mu = tmp_xs['4mu_genbin'+str(obsBin)]
                fidxs2e2mu = tmp_xs['2e2mu_genbin'+str(obsBin)]
                frac4e = fidxs4e/(fidxs4e+fidxs4mu+fidxs2e2mu)
                frac4mu = fidxs4mu/(fidxs4e+fidxs4mu+fidxs2e2mu)
                fidxs4e_sm = tmp_xs_sm['4e_genbin'+str(obsBin)]
                fidxs4mu_sm = tmp_xs_sm['4mu_genbin'+str(obsBin)]
                fidxs2e2mu_sm = tmp_xs_sm['2e2mu_genbin'+str(obsBin)]
                frac4e_sm = fidxs4e_sm/(fidxs4e_sm+fidxs4mu_sm+fidxs2e2mu_sm)
                frac4mu_sm = fidxs4mu_sm/(fidxs4e_sm+fidxs4mu_sm+fidxs2e2mu_sm)
                K1 = frac4e/frac4e_sm
                K2 = frac4mu/frac4mu_sm * (1.0-frac4e_sm)/(1.0-frac4e)
                cmd = cmd + 'K1Bin'+str(obsBin)+'='+str(K1)+','+str(K1)+':K2Bin'+str(obsBin)+'='+str(K2)+','+str(K2)+':'
            if (opt.FIXMASS!="False"):
                cmd = cmd + 'MH='+opt.FIXMASS+','+opt.FIXMASS+':'

            cmd = cmd.rstrip(':')

            if (opt.UNBLIND):
                #cmd = cmd.replace('_exp','')
                cmd = cmd.replace('-D toy_asimov',' ')
            output=processCmd(cmd, get_linenumber())

            if (opt.FIXMASS=="False"):
                processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH125.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
            else:
                processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.FIXMASS.rstrip('.0')+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
            cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
            output=processCmd(cmd, get_linenumber())

    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName+' -M MultiDimFit '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -D toy_asimov --saveWorkspace'
        if (not opt.FIXMASS=="False"):
            cmd = cmd + ' -m '+opt.FIXMASS+' --setParameterRanges MH='+opt.FIXMASS+','+opt.FIXMASS#+'001'
        else:
            cmd = cmd + ' -m 125.0'
        if (opt.UNBLIND):
            #cmd = cmd.replace('_exp','')
            cmd = cmd.replace('-D toy_asimov',' ')
        output=processCmd(cmd, get_linenumber())
        if (opt.FIXMASS=="False"):
            processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH125.root '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root', get_linenumber(), 1)
        else:
            # FIXME: seems like `opt.FIXMASS.rstrip('.0')` this part may do something wrong later.
            processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.FIXMASS.rstrip('.0')+'.root '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root', get_linenumber(), 1)
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        output=processCmd(cmd, get_linenumber())

    # parse the results for all the bins
    for obsBin in range(len(observableBins)-1):
        if (physicalModel=="v3"):
            resultsXS[modelName+'_'+obsName+'_genbin'+str(obsBin)] = parseXSResults(output,'SigmaBin'+str(obsBin)+' :')
        elif (physicalModel=="v2"):
            for fState in fStates:
                resultsXS[modelName+'_'+obsName+'_'+fState+'_genbin'+str(obsBin)] = parseXSResults(output, 'r'+fState+'Bin'+str(obsBin)+' :')

    # load best fit snapshot and run combine with no systematics for stat only uncertainty
    if (opt.SYS):
        cmd = cmd.replace(combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root','-d '+combineOutputs+'/'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root -w w --snapshotName "MultiDimFit"')
       #VM Test:  cmd = cmd + ' --freezeNuisanceGroups CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 --freezeParameters allConstrainedNuisances'
        cmd = cmd + ' --freezeParameters allConstrainedNuisances'

        output = processCmd(cmd, get_linenumber())
        # parse the results
        for obsBin in range(len(observableBins)-1):
            if (physicalModel=="v3"):
                resultsXS[modelName+'_'+obsName+'_genbin'+str(obsBin)+'_statOnly'] = parseXSResults(output,'SigmaBin'+str(obsBin)+' :')
            elif (physicalModel=="v2"):
                for fState in fStates:
                    resultsXS[modelName+'_'+obsName+'_'+fState+'_genbin'+str(obsBin)+'_statOnly'] = parseXSResults(output, 'r'+fState+'Bin'+str(obsBin)+' :')

    return resultsXS

### Extract model dependance uncertnaities from the fit results
def addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName, physicalModel):

    if (opt.UNBLIND): DataModel = 'SM_125_'
    else: DataModel = 'AsimovData_'

    modelIndependenceUncert = {}
    if (physicalModel=="v2"):
        for obsBin in range(len(observableBins)-1):
            for fState in ['4e','4mu','2e2mu']:
                modelIndependenceUncert[DataModel + obsName +'_'+fState+ '_genbin'+str(obsBin)] = {'uncerDn':0.0, 'uncerUp':0.0}

        print (modelIndependenceUncert)
        for key, value in resultsXS.iteritems():
            if (opt.UNBLIND and key.startswith('Asimov')): continue
            for obsBin in range(len(observableBins)-1):
                for fState in ['4e','4mu','2e2mu']:
                    binTag = str(obsBin)
                    if (obsName+'_'+fState+'_genbin'+binTag) in key:
                        asimCent = resultsXS[DataModel + obsName + '_' + fState+'_genbin'+binTag]['central']
                        keyCent = resultsXS[key]['central']
                        diff = keyCent - asimCent
                        if (diff<0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName + '_'+fState+'_genbin'+binTag]['uncerDn'])):
                            modelIndependenceUncert[DataModel + obsName + '_'+fState+'_genbin'+binTag]['uncerDn'] = float("{0:.4f}".format(diff))
                        if (diff>0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName + '_'+fState+'_genbin'+binTag]['uncerUp'])):
                            modelIndependenceUncert[DataModel + obsName +'_'+fState+ '_genbin'+binTag]['uncerUp'] = float("{0:.4f}".format(diff))

    if (physicalModel=="v3"):
        for obsBin in range(len(observableBins)-1):
            modelIndependenceUncert[DataModel + obsName +'_genbin'+str(obsBin)] = {'uncerDn':0.0, 'uncerUp':0.0}

        for key, value in resultsXS.iteritems():
            if (opt.UNBLIND and key.startswith('Asimov')): continue
            for obsBin in range(len(observableBins)-1):
                binTag = str(obsBin)
                if (obsName+'_genbin'+binTag) in key:
                    asimCent = resultsXS[DataModel + obsName + '_genbin'+binTag]['central']
                    keyCent = resultsXS[key]['central']
                    diff = keyCent - asimCent
                    if (diff<0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName + '_genbin'+binTag]['uncerDn'])):
                        modelIndependenceUncert[DataModel + obsName + '_genbin'+binTag]['uncerDn'] = float("{0:.4f}".format(diff))
                    if (diff>0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName + '_genbin'+binTag]['uncerUp'])):
                        modelIndependenceUncert[DataModel + obsName + '_genbin'+binTag]['uncerUp'] = float("{0:.4f}".format(diff))

    return modelIndependenceUncert

### run all the steps towards the fiducial XS measurement
def runFiducialXS():

    # parse the arguments and options
    global opt, args, runAllSteps
    parseOptions()

    # save working dir
    jcpDir = os.getcwd()

    # prepare the set of bin boundaries to run over, only 1 bin in case of the inclusive measurement
    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']

    ### Run for the given observable
    obsName = opt.OBSNAME
    print('\n[INFO] Running fiducial XS computation for - {} - bin boundaries: {}'.format(obsName, observableBins))

    # FIXME: Now we are extracing efficiencies separately. So, don't need below part.
    #        confirm and delete this
    ## Extract the efficiency factors for all reco/gen bins and final states
    #if (runAllSteps or opt.effOnly):
    #    extractFiducialEfficiencies(obsName, observableBins, 'SM')

    # FIXME: Now we are extracing efficiencies separately. Keeping this so that later we can do everything from this script only
    ## Prepare templates and uncertaincies for each reco bin and final states
    #for obsBin in range(0,len(observableBins)-1):
    #    # extract the uncertainties
    #    if (runAllSteps or opt.uncertOnly):
    #        extractUncertainties(obsName, observableBins[obsBin], observableBins[obsBin+1])

    ## Prepare templates for all reco bins and final states
    print("Options:\n\trunAllSteps: {}\n\topt.templatesOnly {}\n".format(runAllSteps,opt.templatesOnly))

    # FIXME: Understand why in step 4; runAllSteps is False, while in step 5 its True
    if (runAllSteps or opt.templatesOnly):
        extractBackgroundTemplatesAndFractions(obsName, observableBins)

    print("\n[INFO] runAllSteps: {runAllSteps}".format(runAllSteps=runAllSteps))
    ## Create the asimov dataset
    if (runAllSteps):
        print('='*51)
        print('[INFO] Create asimov dataset...')
        resultsXS = {}
        #asimovDataModelName = "ggH_powheg_JHUgen_125"
        cmd = 'python python/addConstrainedModel.py -l -q -b --obsName="'+opt.OBSNAME+'" --obsBins="'+opt.OBSBINS+'"'
        output = processCmd(cmd, get_linenumber())
        asimovDataModelName = "SM_125" # FIXME: Is it fine if the model name is hardcoded here. Since model (ASIMOVMODEL) is also an input argument
        asimovPhysicalModel = "v2" # FIXME: Same above message.

        print("{}\n[DEBUG]: {}#{} command:\n".format("="*51,os.path.basename(__file__),get_linenumber())) # Just print filename and line number; Added for debug
        produceDatacards(obsName, observableBins, asimovDataModelName, asimovPhysicalModel)
        print("{}\n[DEBUG]: {}#{} command:\n".format("="*51,os.path.basename(__file__),get_linenumber())) # Just print filename and line number; Added for debug
        resultsXS = createAsimov(obsName, observableBins, asimovDataModelName, resultsXS, asimovPhysicalModel)
        print("resultsXS: \n", resultsXS)

        # plot the asimov predictions for data, signal, and backround in differential bins
        if (not obsName.startswith("mass4l")):
            cmd = 'python python/plotDifferentialBins.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --inYAMLFile="'+opt.inYAMLFile+'"'
            if (opt.UNBLIND): cmd = cmd + ' --unblind'
            output = processCmd(cmd, get_linenumber())
            sys.exit()
            print(output)

    ## Extract the results
    # use constrained SM
    modelNames = opt.MODELNAMES
    modelNames = modelNames.split(',')
    print("[DEBUG]#{} model name: {}".format(get_linenumber(),modelNames))

    # FIXME: Why for mass4l we are using two versions while for others only v3.
    if (obsName.startswith("mass4l")): physicalModels = ["v2","v3"]
    else: physicalModels = ["v3"]

    if (runAllSteps or opt.resultsOnly):
        for physicalModel in physicalModels:
            for modelName in modelNames:
                produceDatacards(obsName, observableBins, modelName, physicalModel)
                resultsXS = extractResults(obsName, observableBins, modelName, physicalModel, asimovDataModelName, asimovPhysicalModel, resultsXS)
                print("resultsXS: \n{}".format(resultsXS))
                # plot the fit results
                if (not obsName.startswith("mass4l")):
                    cmd = 'python python/plotAsimov_simultaneous.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'"'# +' --lumiscale=str(opt.LUMISCALE)'
                    if (opt.UNBLIND): cmd = cmd + ' --unblind'
                    output = processCmd(cmd, get_linenumber())
                    print (output)
                elif (physicalModel=="v2"):
                    cmd = 'python python/plotAsimov_inclusive.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'"' #+' --lumiscale=str(opt.LUMISCALE)'
                    if (opt.UNBLIND): cmd = cmd + ' --unblind'
                    output = processCmd(cmd, get_linenumber())
                    print (output)

            ## Calculate model dependance uncertainties
            modelIndependenceUncert = addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName,physicalModel)
            print("modelIndependenceUncert: \n{}".format(modelIndependenceUncert))
            if (opt.FIXFRAC): floatfix = '_fixfrac'
            else: floatfix = ''
            with open('python/resultsXS_'+obsName+'_'+physicalModel+floatfix+'.py', 'w') as f:
                f.write('modelNames = '+json.dumps(modelNames)+';\n')
                f.write('asimovDataModelName = '+json.dumps(asimovDataModelName)+';\n')
                f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
                f.write('modelIndUncert = '+json.dumps(modelIndependenceUncert))

    # Make final differential plots
    if (runAllSteps or opt.finalplotsOnly):
        DatasetForObservedLimit = "toy_asimov"
        if (opt.UNBLIND):
            DatasetForObservedLimit = "data_obs"

        if (obsName=="mass4l"):

            # These commands for observed data
            # with systematics
            # FIXME: Check if --points=500 improves results/not? If not, keep it to default value which is 50
            # FIXME: hardcoded higgs mass value
            cmd = 'combine -n mass4l_SigmaBin0 -M MultiDimFit '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v3_exp.root -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=500'
            output = processCmd(cmd, get_linenumber())

            # no systematics
            cmd = 'combine -n mass4l_SigmaBin0_NoSys -M MultiDimFit -d '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v3_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:SigmaBin0=0.0,5.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=500  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber())

            #### These commands for observed data
            # 4e
            # with systematics
            cmd = 'combine -n mass4l_r4eBin0 -M MultiDimFit '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P r4eBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:r4eBin0=0.0,5.0 --redefineSignalPOI r4eBin0 --algo=grid --points=500'
            output = processCmd(cmd, get_linenumber())

            # no systematics
            cmd = 'combine -n mass4l_r4eBin0_NoSys -M MultiDimFit -d '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P r4eBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:r4eBin0=0.0,5.0 --redefineSignalPOI r4eBin0 --algo=grid --points=500  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber())

            # 4mu
            # with systematics
            cmd = 'combine -n mass4l_r4muBin0 -M MultiDimFit '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P r4muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:r4muBin0=0.0,5.0 --redefineSignalPOI r4muBin0 --algo=grid --points=500'
            output = processCmd(cmd, get_linenumber())

            # no systematics
            cmd = 'combine -n mass4l_r4muBin0_NoSys -M MultiDimFit -d '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P r4muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:r4muBin0=0.0,5.0 --redefineSignalPOI r4muBin0 --algo=grid --points=500  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber())

            # 2e2mu
            # with systematics
            cmd = 'combine -n mass4l_r2e2muBin0 -M MultiDimFit '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v2_exp.root -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P r2e2muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:r2e2muBin0=0.0,5.0 --redefineSignalPOI r2e2muBin0 --algo=grid --points=500'
            output = processCmd(cmd, get_linenumber())

            # no systematics
            cmd = 'combine -n mass4l_r2e2muBin0_NoSys -M MultiDimFit -d '+combineOutputs+'/SM_125_all_13TeV_xs_mass4l_bin_v2_result.root -w w --snapshotName "MultiDimFit" -m 125.09 -D '+DatasetForObservedLimit+' --setParameters MH=125.09 -P r2e2muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:r2e2muBin0=0.0,5.0 --redefineSignalPOI r2e2muBin0 --algo=grid --points=500  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber())

        else:
            for obsBin in range(0,len(observableBins)-1):
                cmd = "combine -n "+obsName+"_SigmaBin"+str(obsBin)+" -M MultiDimFit -d "+combineOutputs+"/SM_125_all_13TeV_xs_"+obsName+"_bin_"+physicalModel+"_exp.root -m 125.09 -D toy_asimov --setParameters MH=125.09 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:SigmaBin"+str(obsBin)+"=0.0,3.0 --redefineSignalPOIs SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4 "
                if (opt.UNBLIND): cmd = cmd.replace("-D toy_asimov","-D data_obs") # FIXME: Amend this in previous line using variable `DatasetForObservedLimit`
                print("combine command: ",cmd)

                # FIXME: Along with observables in the YAML file we can also add this custom sigmaBin range???
                # if (obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='1'): cmd = cmd.replace('0.0,3.0','0.0,1.5')
                # if (obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='2'): cmd = cmd.replace('0.0,3.0','0.0,0.7')
                if (obsName=='mass4l' and str(obsBin)=='0'): cmd = cmd.replace('0.0,3.0','0.0,5.0')
                if (obsName=='pT4l' and str(obsBin)=='7'): cmd = cmd.replace('0.0,3.0','0.0,2.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='0'): cmd = cmd.replace('0.0,3.0','0.0,4.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='2'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='3'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='4'): cmd = cmd.replace('0.0,3.0','0.0,1.0')

                output = processCmd(cmd, get_linenumber())

                cmd = "combine -n "+obsName+"_SigmaBin"+str(obsBin)+"_NoSys -M MultiDimFit -d "+combineOutputs+"/SM_125_all_13TeV_xs_"+obsName+"_bin_"+physicalModel+"_result.root -w w --snapshotName \"MultiDimFit\" -m 125.09 -D toy_asimov --setParameters MH=125.09 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.09,125.09:SigmaBin"+str(obsBin)+"=0.0,3.0 --redefineSignalPOI SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4 --freezeParameters allConstrainedNuisances "
                output = processCmd(cmd, get_linenumber())

        cmd = 'python python/plotLHScans.py -l -q -b --obsName='+obsName
        output = processCmd(cmd, get_linenumber())
        for modelName in modelNames:
            if (not opt.FIXMASS=="False"):
                cmd = 'python python/producePlots.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --theoryMass="'+opt.FIXMASS+'"'
            else:
                cmd = 'python python/producePlots.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --theoryMass="125.0"'
                ### FIXME: VUKASIN: Just until Higgs mass is properly implemented
            cmd = 'python python/producePlots.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --theoryMass="125.0"'


            if (opt.FIXFRAC): cmd = cmd + ' --fixFrac'
            if (opt.UNBLIND): cmd = cmd + ' --unblind'
            output = processCmd(cmd, get_linenumber())
            print (output)
            cmd = cmd + ' --setLog'
            output = processCmd(cmd, get_linenumber())
            print (output)

if __name__ == "__main__":
    runFiducialXS()

print ("all modules successfully compiled")
