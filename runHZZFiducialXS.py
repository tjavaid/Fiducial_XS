#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.10.16
#-----------------------------------------------
import ast
import json
import math
import optparse
import os
import sys

from cgi import test
from decimal import *

import yaml

# INFO: Following items are imported from either python directory or Inputs
from createXSworkspace import createXSworkspace
from higgs_xsbr_13TeV import filtereff, higgs4l_br, higgs_xs, higgsZZ_br
from Input_Info import combineOutputs, datacardInputs, channels_central
from read_bins import read_bins
from ROOT import *
from sample_shortnames import background_samples, sample_shortnames
from Utils import (GetDirectory, get_linenumber, logger, logging,
                   mergeDictionary_average, processCmd)

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

### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps, unblindString

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',      dest='SOURCEDIR',type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--asimovModelName',dest='ASIMOVMODEL',type='string',default='SM_125', help='Name of the Asimov Model')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.38', help='Asimov Mass')
    parser.add_option('',   '--modelNames',dest='MODELNAMES',type='string',default="SM_125",help='Names of models for unfolding, separated by , (comma) like "SM_125,SMup_125,SMdn_125". Default is "SM_125"')
    # FIXME: `FIXMASS` option should be bool. As per its name. No?
    parser.add_option('',   '--fixMass',  dest='FIXMASS',  type='string',default='125.38',   help='Fix mass, default is a string "125.38" or can be changed to another string, e.g."125.6" or "False"')
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
    parser.add_option('-i',   '--inYAMLFile', dest='inYAMLFile', type='string', default="Inputs/observables_list.yml", help='Input YAML file having observable names and bin information')
    parser.add_option("-l", "--logLevel", dest="logLevel",  type = 'string', default = '2', help="Change log verbosity(WARNING: 0, INFO: 1, DEBUG: 2, ERROR: 3)")
    parser.add_option('-y', '--year', dest="ERA", type = 'string', default = '2018', help='Specifies the data taking period')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

    # NOTE: append the directory `datacardInputs`, as .py files inside is going to load using import.
    #       load XS-specific modules
    GetDirectory(datacardInputs.format(year = opt.ERA))
    sys.path.append('./'+datacardInputs.format(year = opt.ERA))

    log_level = logging.DEBUG # default initialization
    if opt.logLevel == "0":
        log_level = logging.WARNING
    elif opt.logLevel == "1":
        log_level = logging.INFO
    elif opt.logLevel == "2":
        log_level = logging.DEBUG
    elif opt.logLevel == "3":
        log_level = logging.ERROR
    logger.setLevel( log_level)

    unblindString = ""
    if (opt.UNBLIND): unblindString = "_unblind"

    # prepare the global flag if all the step should be run
    runAllSteps = not(opt.effOnly or opt.templatesOnly or opt.uncertOnly or opt.resultsOnly or opt.finalplotsOnly)
    # runAllSteps = not(opt.templatesOnly or opt.uncertOnly or opt.resultsOnly or opt.finalplotsOnly)

    if (opt.OBSBINS=='' and opt.OBSNAME!='inclusive'):
        parser.error('Bin boundaries not specified for differential measurement. Exiting...')
        sys.exit()

    # FIXME: Check why we need these directories
    #        The directory `combineOutputs` is used to keep the generated workspaces
    GetDirectory(combineOutputs.format(year = opt.ERA))

    dirToExist = ['templates', datacardInputs.format(year = opt.ERA), combineOutputs.format(year = opt.ERA)]
    for dir in dirToExist:
        if not os.path.isdir(os.getcwd()+'/'+dir+'/'):
            parser.error(os.getcwd()+'/'+dir+'/ is not a directory. Exiting...')
            sys.exit()

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
    output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
    print (output)
    # if (not opt.OBSNAME.startswith("mass4l")):
    if (not (opt.OBSNAME=="mass4l")):
        cmd = 'python plot2dsigeffs.py -l -q -b --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'"'
        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

### Extract the templates for given obs, for all bins and final states (differential)
def extractBackgroundTemplatesAndFractions(obsName, observableBins, year, obs_ifJES, obs_ifJES2):
    global opt

    logger.debug("[INFO] Obs Name: {:15}\tBins: {}".format(obsName, observableBins))

    fractionBkg = {}; lambdajesdnBkg={}; lambdajesupBkg={}

    if os.path.isfile(datacardInputs.format(year = year)+'/inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName.replace(" ","_")+'.py'):
        _temp = __import__('inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName.replace(" ","_"), globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1)
        if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
            logger.info ('[Fractions already exist for the given binning. Skipping templates/shapes... ]')
            return
        if (hasattr(_temp,'fractionsBackground') and hasattr(_temp,'lambdajesupBkg') and hasattr(_temp,'lambdajesdnBkg')):
            fractionBkg = _temp.fractionsBackground
            lambdajesupBkg = _temp.lambdajesupBkg
            lambdajesdnBkg = _temp.lambdajesdnBkg

    logger.debug('Preparing bkg shapes and fractions, for bins with boundaries {}'.format(observableBins))
    # save/create/prepare directories and compile templates script
    # FIXME: directory name hardcoded
    currentDir = os.getcwd(); os.chdir('./templates/')

    # Here, rm command is mandatory, just to ensure that make works. If make command files
    #   then this can pick older executable. So, to avoid this we first delete the executable
    # logger.info("==> Remove the executable and Compile the package main_fiducialXSTemplates...")
    # cmd = 'rm main_fiducialXSTemplates; make';
    # processCmd(cmd, get_linenumber(), os.path.basename(__file__))
    # moved the compilation part in the "setup.sh"
    # FIXME: this directory name is hardcoded in fiducialXSTemplates.C
    # FIXME: Try to link the two automatically.
    # FIXME: Also, this name is passed as one of arguments of `main_fiducialXSTemplates()`
    DirectoryToCreate = 'templatesXS_'+str(year)+'/DTreeXS_' + obsName.replace(" ","_") + '/13TeV/'
    logger.debug('Create directory: {}'.format(DirectoryToCreate))
    logger.debug('compile the script inside the template directory')
    cmd = 'mkdir -p '+DirectoryToCreate; processCmd(cmd, get_linenumber(), os.path.basename(__file__), 1)

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

    logger.info('Loop over each background sample tags: \n\t{}\n'.format(bkg_sample_tags))
    for sample_tag in bkg_sample_tags:
        tmpSrcDir = opt.SOURCEDIR
        if (sample_tag=='ZX4l_CR'):
            # tmpSrcDir = '/eos/user/v/vmilosev/Skim_2018_HZZ/WoW'
            tmpSrcDir = opt.SOURCEDIR # FIXME: if the paths for ZX CR is different then we need to update this
        # FIXME: Try to understand this syntax
        fitTypeZ4l = [['none','doRatio'],['doZ4l','doZ4l']][opt.doZ4l][opt.doRatio]
        logger.info("observableBins: "+str(observableBins))

        if (" vs " not in obsName ):
            #cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[year][sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+obsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 13TeV templatesXS_'+str(year)+' DTreeXS ' + fitTypeZ4l+ ' 0' +' "' +str(obs_ifJES).lower() +'" '
            cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[year][sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+obsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 13TeV templatesXS'+' DTreeXS ' + fitTypeZ4l+ ' 0 ' +str(int(obs_ifJES)) + ' "'+ str(year)+'"'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            # FIXME: URGENT: Here previous command copies all the cout info in variable `output`
            #               then from the string it is going to extract useful information about bin fraction
            tmp_fracs = output.split("[Bin fraction: ")
            print('[INFO] tmp_fracs: {}'.format(tmp_fracs))
            logger.debug('Length of observables bins: {}'.format(observableBins))
            logger.debug('Length of observables bins: {}'.format(len(observableBins)))
            # for lines_ in tmp_fracs:
            if (" does not exists" in tmp_fracs[0]):
                """INFO: Sometime template maker
                """
                logger.error("Seems like template maker did not finish as expected. Please check!!!")
                sys.exit(0)
            for obsBin in range(0,len(observableBins)-1):
                fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
                lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
                lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = 0
                tmpFrac = float(tmp_fracs[obsBin+1].split("][end fraction]")[0])
                if not math.isnan(tmpFrac):
                    fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac
                #if (('jet' in obsName) and tmpFrac!=0 and not math.isnan(tmpFrac)):
                if ((obs_ifJES) and tmpFrac!=0 and not math.isnan(tmpFrac)):
                    tmpFrac_up =float(tmp_fracs[obsBin+1].split("Bin fraction (JESup): ")[1].split("]")[0])
                    tmpFrac_dn =float(tmp_fracs[obsBin+1].split("Bin fraction (JESdn): ")[1].split("]")[0])
                    if not math.isnan(tmpFrac_up):
                        lambdajesupBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_up/tmpFrac - 1
                    if not math.isnan(tmpFrac_dn):
                        lambdajesdnBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = tmpFrac_dn/tmpFrac - 1
        else:
            for nBins_ in range(len(observableBins)):
                # First observable boundary:  observableBins[nBins_][0]
                # 2nd  observable boundary:  observableBins[nBins_][1]
                bin0_ = '|' + observableBins[nBins_][0][0] + '|' +  observableBins[nBins_][0][1] + '|'  # FIXME: Discuss with Vukasin
                bin1_ = '|' + observableBins[nBins_][1][0] + '|' +  observableBins[nBins_][1][1] + '|'

                ListObsName = (''.join(obsName.split())).split('vs')
                logger.info(ListObsName[0]+ ' : ' + str(bin0_)+"\t"+ListObsName[1] + ' : '+str(bin1_))

                cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[year][sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+ListObsName[0]+' "'+bin0_+'" "'+bin0_ +'" 13TeV templatesXS'+' DTreeXS ' + fitTypeZ4l+ ' 0 ' + str(int(obs_ifJES)) + ' "'+ str(year)+'"' + ' ' + ListObsName[1]+' "'+bin1_+'" "'+bin1_ +'" '+str(int(obs_ifJES2))
                output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
                tmp_fracs = output.split("[Bin fraction: ")
                logger.debug('tmp_fracs: {}'.format(tmp_fracs))
                logger.debug('Length of observables bins: {}'.format(len(observableBins)))

                tag_ = sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName.replace(' ','_')+'_recobin'+str(nBins_)
                logger.debug('tag_ : {}'.format(tag_))

                fractionBkg[tag_] = 0
                lambdajesupBkg[tag_] = 0
                lambdajesdnBkg[tag_] = 0

                logger.debug('tmp_fracs: {}'.format(tmp_fracs))
                logger.debug('tmp_fracs[1]: {}'.format(tmp_fracs[1]))
                logger.debug('tmp_fracs[1].split("][end fraction]"): {}'.format(tmp_fracs[1].split("][end fraction]")))

                # The current for loop depends on how many times "[Bin fraction: " appears, when we run the `main_fiducialXSTemplates`
                tmpFrac = float(tmp_fracs[1].split("][end fraction]")[0])
                if not math.isnan(tmpFrac):
                    fractionBkg[tag_] = tmpFrac
                else:
                    logger.error('total entries in the current bin is isnan. Please check...')
                    #FIXME: should we exit program here or not???

                #if (('jet' in ListObsName[0] or 'jet' in ListObsName[1]) and tmpFrac!=0 and not math.isnan(tmpFrac)): # FIXME: this part will have issue when we have double differential obs.
                if ((obs_ifJES or obs_ifJES2) and tmpFrac!=0 and not math.isnan(tmpFrac)): # FIXME: this part will have issue when we have double differential obs.
                    # FIXME: Check jets information, if its passing correctly or not.
                    # FIXME: Again we are grabbing things from the log of `main_fiducialXSTemplates`. The next result depends on the couts of `main_fiducialXSTemplates`
                    logger.debug('tmp_fracs[1].split("Bin fraction (JESup): "): {}'.format(tmp_fracs[1].split("Bin fraction (JESup): ")))
                    logger.debug('tmp_fracs[1].split("Bin fraction (JESup): ")[1]: {}'.format(tmp_fracs[1].split("Bin fraction (JESup): ")[1]))
                    logger.debug('tmp_fracs[1].split("Bin fraction (JESup): ")[1].split("]"): {}'.format(tmp_fracs[1].split("Bin fraction (JESup): ")[1].split("]")))

                    tmpFrac_up =float(tmp_fracs[1].split("Bin fraction (JESup): ")[1].split("]")[0])
                    tmpFrac_dn =float(tmp_fracs[1].split("Bin fraction (JESdn): ")[1].split("]")[0])
                    if not math.isnan(tmpFrac_up):
                        lambdajesupBkg[tag_] = tmpFrac_up/tmpFrac - 1
                    if not math.isnan(tmpFrac_dn):
                        lambdajesdnBkg[tag_] = tmpFrac_dn/tmpFrac - 1

    os.chdir(currentDir)
    logger.debug('observableBins: {}'.format(observableBins))
    logger.debug('fractionBkg: {}'.format(fractionBkg))
    logger.debug('lambdajesupBkg: {}'.format(lambdajesupBkg))
    logger.debug('lambdajesdnBkg: {}'.format(lambdajesdnBkg))

    OutputFileName = 'inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName.replace(' ','_')+'.py'
    logger.debug('File Name: '+OutputFileName)
    with open(datacardInputs.format(year = year) + '/' + OutputFileName, 'w') as f:
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
    #processCmd(cmd, get_linenumber(), os.path.basename(__file__))

### Produce datacards for given obs and bin, for all final states
#def produceDatacards(obsName, observableBins, modelName, physicalModel, obs_ifJES, obs_ifJES2, year):
def produceDatacards(obsName, observableBins, modelName, physicalModel, obs_ifJES, obs_ifJES2, obs_ifAbs, obs_ifAbs2, year):
    """Produce workspace/datacards for the given observable and bins

    Args:
        obsName (str): Name of observable
        observableBins (array): Array having bin boundaries
        modelName (str): Name of model. For example: SM_125
        physicalModel (str): version of model, for example: v2
    """

    logger.info ('Producing workspace/datacards for obsName - '+obsName+', bins - '+str(observableBins)+']')
    logger.debug('obsName: {}'.format(obsName))
    logger.debug('observableBins: {}'.format(observableBins))

    ListObsName = (''.join(obsName.split())).split('vs')
    logger.debug('ListObsName: {}'.format(ListObsName))

    fStates = channels_central

    # INFO: in case of 2D obs nbins is n else its n-1
    logger.debug("len(observableBins): = "+str(len(observableBins)))
    nBins = len(observableBins) -1
    if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
        nBins = len(observableBins)

    for fState in fStates:
        logger.info('''VM Creating datacards for:
        \tobsName: {obsName}
        \tfState: {fState}
        \tnBins: {nBins}
        \tobservableBins: {observableBins}
        \tmodelName: {modelName}
        \tphysicalModel: {physicalModel}'''.format(
                obsName = ListObsName , fState = fState , nBins = nBins ,
                observableBins = observableBins , modelName = modelName ,
                physicalModel = physicalModel
                ))
        if (obs_ifJES):
            # Call read_jes module
            command_read_jes = 'python python/read_jes.py -c {channel} -b {nbins} -v {variable} -y {year}'.format(channel = fState, nbins = nBins, variable = obsName.replace(' ','_'), year = year)
            processCmd(command_read_jes, get_linenumber(), os.path.basename(__file__))
        if (not (obsName=="mass4l")):
            logger.debug("Running the datacard_maker.py...")
            processCmd("python python/datacard_maker.py -c {} -b {} -y {}".format(fState, nBins, year),get_linenumber(), os.path.basename(__file__))
            logger.debug("Completed the datacard_maker.py...")
            for obsBin in range(nBins):
                logger.debug("=="*51)
                logger.debug("""
                    \ttmpObsName = {},
                    \tfState = {},
                    \tnBins = {}, obsBin = {},
                    \tobservableBins = {},
                    \tFalse = {}, True = {},
                    \tmodelName = {}, physicalModel = {},
                    \tobs_ifJES = {}, obs_ifJES2 = {}
                    """.format(ListObsName, fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel, obs_ifJES, obs_ifJES2))
                #ndata = createXSworkspace(ListObsName, fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel, year, obs_ifJES, obs_ifJES2)
                ndata = createXSworkspace(ListObsName, fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel, year, obs_ifJES, obs_ifJES2, obs_ifAbs, obs_ifAbs2)
                CopyDataCardToOutputDir = "cp xs_125.0_"+str(nBins)+"bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName.replace(' ','_')+"_bin"+str(obsBin)+"_"+physicalModel+".txt"
                processCmd(CopyDataCardToOutputDir, get_linenumber(), os.path.basename(__file__))
                UpdateObservationValue = "sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName.replace(' ','_')+"_bin"+str(obsBin)+"_"+physicalModel+".txt"
                processCmd(UpdateObservationValue, get_linenumber(), os.path.basename(__file__))
                UpdateDatabin = "sed -i 's~_xs.Databin"+str(obsBin)+"~_xs_"+modelName+"_"+obsName.replace(' ','_')+"_"+physicalModel+".Databin"+str(obsBin)+"~g' "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName.replace(' ','_')+"_bin"+str(obsBin)+"_"+physicalModel+".txt"
                os.system(UpdateDatabin)

                if (obs_ifJES):
                    # INFO: This "command_append" here just to ensures appending new line from next one. Below, "command_append" is just added a blank in card
                    command_append = "echo '" "' >> " +combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName.replace(' ','_')+"_bin"+str(obsBin)+"_"+physicalModel+".txt"
                    os.system(command_append)
                    with open("Inputs/JES/{year}/{obsName}/datacardLines_JESnuis_{obsName}_{channel}.txt".format(year = year, obsName = obsName.replace(' ','_'), channel= fState)) as f:
                        data = f.read()

                    d = ast.literal_eval(data)
                    for keys, values in d.items():
                        if (keys == obsName.replace(' ','_') + '_' + str(obsBin)):
                            for value in values:
                                command_append = "echo '"+str(value)+" ' >> " +combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName.replace(' ','_')+"_bin"+str(obsBin)+"_"+physicalModel+".txt"
                                os.system(command_append)

        else:
            logger.debug("Running the datacard_maker.py...")
            dataCardMakerCommand = "python python/datacard_maker.py -c {} -b {} -y {}".format(fState, 1, year)
            processCmd(dataCardMakerCommand, get_linenumber(), os.path.basename(__file__))
            logger.debug("Completed the datacard_maker.py...")
            #ndata = createXSworkspace(ListObsName,fState, nBins, 0, observableBins, False, True, modelName, physicalModel, year, obs_ifJES, obs_ifJES2)
            ndata = createXSworkspace(ListObsName,fState, nBins, 0, observableBins, False, True, modelName, physicalModel, year, obs_ifJES, obs_ifJES2, obs_ifAbs, obs_ifAbs2)
            if obsName=='mass4l':
                CopyDataCardToOutputDir = "cp xs_125.0_1bin/hzz4l_"+fState+"S_13TeV_xs_inclusive_bin0.txt "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt"
                processCmd(CopyDataCardToOutputDir, get_linenumber(), os.path.basename(__file__))
            if obsName=='mass4lREFIT':
                os.system("cp xs_125.0_1bin/hzz4l_"+fState+"S_13TeV_xs_inclusiveREFIT_bin0.txt "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
            UpdateObservationValue = "sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt"
            processCmd(UpdateObservationValue, get_linenumber(), os.path.basename(__file__))
            UpdateDatabin = "sed -i 's~_xs.Databin0~_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin0~g' "+combineOutputs.format(year = year)+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt"
            processCmd(UpdateDatabin, get_linenumber(), os.path.basename(__file__))


def createAsimov_161718(obsName, observableBins, modelName, resultsXS, physicalModel, years = ['2016', '2017', '2018'], obs_ifJES = False):
    logger.info('[Combined datacard for all 3 years for obsName "'+obsName.replace(' ','_')+'" using '+modelName+']')

    logger.debug('obsName: {}'.format(obsName))
    logger.debug('observableBins: {}'.format(observableBins))
    logger.debug("resultsXS: {}".format(resultsXS))

    ListObsName = (''.join(obsName.split())).split('vs')
    logger.debug('ListObsName: {}'.format(ListObsName))

    # INFO: in case of 2D obs nbins is n else its n-1
    nBins = len(observableBins) -1
    if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
        nBins = len(observableBins)
    logger.debug("nBins: = "+str(nBins))

    GetDirectory(combineOutputs.format(year = 'allYear'))

    fStates = channels_central
    AllChannelCombinedDataCards = 'hzz4l_all_13TeV_xs_{obsName}_bin_{physicalModel}.txt '
    cmd = 'combineCards.py '
    for year in years:
        pathOfCard = combineOutputs.format(year = year)
        logger.info("path of datacard for year - {}: {}".format(year, pathOfCard))
        # cmd +=  pathOfCard + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)
        cmd += obsName+'_4e4mu2e2mu_'+year + '=' + pathOfCard + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)
    # FIXME: Hardcoded dir string year
    cmd += ' > ' + combineOutputs.format(year = 'allYear') + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)
    processCmd(cmd, get_linenumber(), os.path.basename(__file__))


    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> '+ combineOutputs.format(year = 'allYear') + '/' +'hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> '+combineOutputs.format(year = 'allYear') + '/' +'hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> '+combineOutputs.format(year = 'allYear') + '/' +'hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')

    # text-to-workspace
    if (physicalModel=="v2"):
        cmd = 'text2workspace.py ' + combineOutputs.format(year = 'allYear') + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel) + ' -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins)+' -o ' + combineOutputs.format(year = 'allYear') + '/' +(AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)).replace('.txt', '.root')
        processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    # FIXME: Can we improve this?
    cmd = 'mv ' + combineOutputs.format(year = 'allYear') + '/' +(AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)).replace('.txt', '.root') + ' ' + combineOutputs.format(year = 'allYear') + '/' +modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
    processCmd(cmd, get_linenumber(), os.path.basename(__file__))


    # Run the Combine
    logger.info("Going to run the combine commands...")
    cmd = ''
    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str("allYear")+unblindString+' -M MultiDimFit  '+combineOutputs.format(year = "allYear")+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root -m '+opt.ASIMOVMASS+' --setParameters '
        logger.debug("command:\n\t{}".format(cmd))
        for fState in fStates:
            for obsBin in range(nBins):
                fidxs = 0
                for year in years:
                    # import acc factors
                    logger.debug("Import module: {}".format((datacardInputs.format(year = year)).replace('/','.') + '.' + 'inputs_sig_'+obsName.replace(' ','_')))
                    _temp = __import__((datacardInputs.format(year = year)).replace('/','.') + '.' + 'inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['acc'], -1)
                    acc = _temp.acc
                    fidxs += higgs_xs['ggH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    #fidxs += acc['ggH_HRes_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs += higgs_xs['VBF_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['VBF_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs += higgs_xs['WH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['WH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs += higgs_xs['ZH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ZH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs += higgs_xs['ttH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ttH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                cmd = cmd + 'r'+fState+'Bin'+str(obsBin)+'='+str(fidxs/3.0)+',' # FIXME: Check division by 3.0

        cmd =  cmd+ 'MH='+opt.ASIMOVMASS
        logger.debug("command+:\n\t{}".format(cmd))
        for fState in fStates:
            for obsBin in range(nBins):
                cmd = cmd + ' -P r'+fState+'Bin'+str(obsBin)
        if (opt.FIXMASS=="False"):
            cmd = cmd + ' -P MH '
        else:
            cmd = cmd + ' --floatOtherPOIs=0'
        cmd = cmd +' -t -1 --saveWorkspace --saveToys  --saveFitResult '
        logger.debug("command+:\n\t{}".format(cmd))

        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        # INFO: Move combine output to combineOutputs.format(year = opt.ERA) directory
        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str("allYear")+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs.format(year = "allYear")+'/'+modelName+'_all_'+obsName.replace(' ','_')+'_13TeV_Asimov_'+physicalModel+unblindString+'.root', get_linenumber(), os.path.basename(__file__), 1)

        #cmd = cmd.replace(' --freezeNuisanceGroups r4muBin0,r4eBin0,r2e2muBin0','')
        #cmd = cmd.replace(' --X-rtd TMCSO_PseudoAsimov=1000000','')
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str("allYear")+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs.format(year = "allYear")+'/', get_linenumber(), os.path.basename(__file__))

    # parse the results for all the bins and the given final state
    tmp_resultsXS = {}
    for fState in fStates:
        for obsBin in range(nBins):
            binTag = str(obsBin)
            tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag] = parseXSResults(output,'r'+fState+'Bin'+str(obsBin)+' :')


    # merge the results for 3 final states, for the given bins
    for obsBin in range(nBins):
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
        cmd = cmd + ' --freezeParameters allConstrainedNuisances'
        # cmd = cmd + ' --freezeParameters '
        # cmd = cmd + 'CMS_fakeH_p1_1'+year+',CMS_fakeH_p1_2'+year+',CMS_fakeH_p1_3'+year+',CMS_fakeH_p3_1'+year+',CMS_fakeH_p3_2'+year+',CMS_fakeH_p3_3'+year+','
        # cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year)+',CMS_hzz4e_Zjets_'+str(year)+',CMS_hzz4mu_Zjets_'+str(year)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year)+',CMS_zz4l_sigma_m_sig_'+str(year)+',CMS_zz4l_n_sig_1_'+str(year)+',CMS_zz4l_n_sig_2_'+str(year)+',CMS_zz4l_n_sig_3_'+str(year)+',CMS_zz4l_mean_e_sig_'+str(year)+',CMS_zz4l_mean_m_sig_'+str(year)+',CMS_zz4l_sigma_e_sig_'+str(year)+','
        # if (obs_ifJES):
        #     jes_sources_year_updated = [x.replace('year', year) for x in jes_sources]
        #     for jes_source in jes_sources:
        #         cmd += ",CMS_scale_j_"+ jes_sources_year_updated[jes_sources.index(jes_source)]
        #     cmd = cmd + ',lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'

        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        #for year in years:
        #    cmd = cmd + 'CMS_fakeH_p1_1'+year+',CMS_fakeH_p1_2'+year+',CMS_fakeH_p1_3'+year+',CMS_fakeH_p3_1'+year+',CMS_fakeH_p3_2'+year+',CMS_fakeH_p3_3'+year+','
        #    cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year)+',CMS_hzz4e_Zjets_'+str(year)+',CMS_hzz4mu_Zjets_'+str(year)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year)+',CMS_zz4l_sigma_m_sig_'+str(year)+',CMS_zz4l_n_sig_1_'+str(year)+',CMS_zz4l_n_sig_2_'+str(year)+',CMS_zz4l_n_sig_3_'+str(year)+',CMS_zz4l_mean_e_sig_'+str(year)+',CMS_zz4l_mean_m_sig_'+str(year)+',CMS_zz4l_sigma_e_sig_'+str(year)+','
	#    if len(years)>1:
	#        cmd = cmd + 'lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'
        #if (obs_ifJES):
        #    jes_sources_year_updated = [x.replace('year', year) for x in jes_sources]
        #    for jes_source in jes_sources:
        #        cmd += ",CMS_scale_j_"+ jes_sources_year_updated[jes_sources.index(jes_source)]

        #logger.error(cmd)
        #sys.exit()
        # processCmd(cmd, get_linenumber(), os.path.basename(__file__))


        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str("allYear")+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs.format(year = "allYear")+'/', get_linenumber(), os.path.basename(__file__))

        for fState in fStates:
            for obsBin in range(nBins):
                binTag = str(obsBin)
                tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag+'_statOnly'] = parseXSResults(output,'r'+fState+'Bin'+str(obsBin)+' :')

        # merge the results for 3 final states, for the given bins
        for obsBin in range(nBins):
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

### Create the asimov dataset and return fit results
#def createAsimov(obsName, observableBins, modelName, resultsXS, physicalModel, year = 2018, obs_ifJES = False):
def createAsimov(obsName, observableBins, modelName, resultsXS, physicalModel, year = 2018, obs_ifJES = False, obs_ifAbs = False):
    """Create the Asimov dataset and return the fit results.

    Args:
        obsName (str): Name of observable
        observableBins (array): Array having bin boundaries
        modelName (str): Name of model
        resultsXS (_type_): _description_
        physicalModel (_type_): _description_
    """
    logger.info('[Producing/merging workspaces and datacards for obsName "'+obsName.replace(' ','_')+'" using '+modelName+']')

    logger.debug('obsName: {}'.format(obsName))
    logger.debug('observableBins: {}'.format(observableBins))

    ListObsName = (''.join(obsName.split())).split('vs')
    logger.debug('ListObsName: {}'.format(ListObsName))

    # INFO: in case of 2D obs nbins is n else its n-1
    nBins = len(observableBins) -1
    if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
        nBins = len(observableBins)
    logger.debug("nBins: = "+str(nBins))

    # Run combineCards and text2workspace
    currentDir = os.getcwd(); os.chdir('./'+combineOutputs.format(year = year)+'/') # FIXME: Hardcoded directory
    fStates = channels_central
    for fState in fStates:
        """Combine cards for all bins corresponding to each final state.
        """
        # if (nBins>1):
        cmd = 'combineCards.py '
        for obsBin in range(nBins):
            cmd +=   obsName + '_' + fState + 'S_'+str(obsBin)+'_'+year + '=' +'hzz4l_'+fState+'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '
        cmd += ' > hzz4l_'+fState+'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt' # Output combine card name
        processCmd(cmd, get_linenumber(),  os.path.basename(__file__), 1)

    # combine 3 final state cards
    cmd = 'combineCards.py '
    for channels_ in fStates:
        cmd += obsName + '_' + channels_ + 'S_' + year + '=hzz4l_' + channels_ + 'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt  '
    cmd += ' >  hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt'
    processCmd(cmd, get_linenumber(), os.path.basename(__file__), 1)

    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt')

    # text-to-workspace
    if (physicalModel=="v2"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins)+' -o hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber(), os.path.basename(__file__))
    if (physicalModel=="v3"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducialV3 --PO higgsMassRange=115,135 --PO nBin='+str(nBins)+' -o hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    # FIXME: Can we improve this?
    cmd = 'mv hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root '+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
    processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    os.chdir(currentDir)

    # import acc factors
    _temp = __import__('inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['acc'], -1)
    acc = _temp.acc

    # Run the Combine
    logger.info("Going to run the combine commands...")
    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str(year)+unblindString+' -M MultiDimFit  '+combineOutputs.format(year = year)+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root -m '+opt.ASIMOVMASS+' --setParameters '
        for fState in fStates:
            for obsBin in range(nBins):
                fidxs = 0
                fidxs += higgs_xs['ggH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                #fidxs += acc['ggH_HRes_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['VBF_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['VBF_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['WH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['WH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['ZH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ZH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['ttH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ttH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                cmd = cmd + 'r'+fState+'Bin'+str(obsBin)+'='+str(fidxs)+','
        cmd =  cmd+ 'MH='+opt.ASIMOVMASS
        for fState in fStates:
            for obsBin in range(nBins):
                cmd = cmd + ' -P r'+fState+'Bin'+str(obsBin)
        if (opt.FIXMASS=="False"):
            cmd = cmd + ' -P MH '
        else:
            cmd = cmd + ' --floatOtherPOIs=0'
        cmd = cmd +' -t -1 --saveWorkspace --saveToys'
        logger.debug("command+:\n\t{}".format(cmd))

        GetDirectory(combineOutputs.format(year = year))

        #cmd += ' --freezeNuisanceGroups r4muBin0,r4eBin0,r2e2muBin0'
        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        # INFO: Move combine output to combineOutputs.format(year = opt.ERA) directory
        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs.format(year = year)+'/'+modelName+'_all_'+obsName.replace(' ','_')+'_13TeV_Asimov_'+physicalModel+unblindString+'.root', get_linenumber(), os.path.basename(__file__), 1)

        #cmd = cmd.replace(' --freezeNuisanceGroups r4muBin0,r4eBin0,r2e2muBin0','')
        #cmd = cmd.replace(' --X-rtd TMCSO_PseudoAsimov=1000000','')
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        # lsCMD = "ls *.root"
        # processCmd(lsCMD, get_linenumber(), os.path.basename(__file__))
        # INFO: Move combine output to combineOutputs.format(year = opt.ERA) directory
        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs.format(year = year)+'/', get_linenumber(), os.path.basename(__file__))

    # parse the results for all the bins and the given final state
    tmp_resultsXS = {}
    for fState in fStates:
        for obsBin in range(nBins):
            binTag = str(obsBin)
            tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag] = parseXSResults(output,'r'+fState+'Bin'+str(obsBin)+' :')


    # merge the results for 3 final states, for the given bins
    for obsBin in range(nBins):
        binTag = str(obsBin)
        resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
        for fState in fStates:
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
        tmp_central = 0.0
        tmp_uncerDn = 0.0
        tmp_uncerUp = 0.0
        for fState in fStates:
            tmp_central += tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag]['central']
            tmp_uncerDn += tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag]['uncerDn']**2
            tmp_uncerUp += tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag]['uncerUp']**2
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag]['central'] = float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag]['central']))
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag]['uncerDn'] = -float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag]['uncerDn']))
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag]['uncerUp'] = +float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag]['uncerUp']))
        resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag]['central'] = float("{0:.5f}".format(tmp_central))
        resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag]['uncerDn'] = -float("{0:.5f}".format(tmp_uncerDn**0.5))
        resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag]['uncerUp'] = +float("{0:.5f}".format(tmp_uncerUp**0.5))

    # run combine with no systematics for stat only uncertainty
    if (opt.SYS):
        # Test VM:        cmd = cmd + ' --freezeNuisanceGroups CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 --freezeParameters allConstrainedNuisances'
        cmd = cmd + ' --freezeParameters allConstrainedNuisances'

        # cmd = cmd + ' --freezeParameters '
        # cmd = cmd + 'CMS_fakeH_p1_1'+year+',CMS_fakeH_p1_2'+year+',CMS_fakeH_p1_3'+year+',CMS_fakeH_p3_1'+year+',CMS_fakeH_p3_2'+year+',CMS_fakeH_p3_3'+year+','
        # cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year)+',CMS_hzz4e_Zjets_'+str(year)+',CMS_hzz4mu_Zjets_'+str(year)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year)+',CMS_zz4l_sigma_m_sig_'+str(year)+',CMS_zz4l_n_sig_1_'+str(year)+',CMS_zz4l_n_sig_2_'+str(year)+',CMS_zz4l_n_sig_3_'+str(year)+',CMS_zz4l_mean_e_sig_'+str(year)+',CMS_zz4l_mean_m_sig_'+str(year)+',CMS_zz4l_sigma_e_sig_'+str(year)+','
        # if (obs_ifJES):
        #     jes_sources_year_updated = [x.replace('year', year) for x in jes_sources]
        #     for jes_source in jes_sources:
        #         cmd += ",CMS_scale_j_"+ jes_sources_year_updated[jes_sources.index(jes_source)]
	    #     cmd = cmd + 'lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'

        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        # FIXME: The current combine command and the previous
        #        combine command generates output with exactly same name (obvious).
        #        But, we are not renaming them so its updated with current command.
        #        check if this is fine?
        # print("="*51)
        # lsCMD = 'echo "ls *.root";ls *.root'
        # processCmd(lsCMD, get_linenumber(), os.path.basename(__file__))
        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+combineOutputs.format(year = year)+'/', get_linenumber(), os.path.basename(__file__))


        for fState in fStates:
            for obsBin in range(nBins):
                binTag = str(obsBin)
                tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly'] = parseXSResults(output,'r'+fState+'Bin'+str(obsBin)+' :')

        # merge the results for 3 final states, for the given bins
        for obsBin in range(nBins):
            binTag = str(obsBin)
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly'] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
            for fState in fStates:
                resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag+'_statOnly'] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
            tmp_central = 0.0
            tmp_uncerDn = 0.0
            tmp_uncerUp = 0.0
            for fState in fStates:
                tmp_central += tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['central']
                tmp_uncerDn += tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['uncerDn']**2
                tmp_uncerUp += tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['uncerUp']**2
                resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag+'_statOnly']['central'] = float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['central']))
                resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag+'_statOnly']['uncerDn'] = -float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['uncerDn']))
                resultsXS['AsimovData_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag+'_statOnly']['uncerUp'] = +float("{0:.5f}".format(tmp_resultsXS[modelName+'_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['uncerUp']))
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['central'] = float("{0:.5f}".format(tmp_central))
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['uncerDn'] = -float("{0:.5f}".format(tmp_uncerDn**0.5))
            resultsXS['AsimovData_'+obsName.replace(' ','_')+'_genbin'+binTag+'_statOnly']['uncerUp'] = +float("{0:.5f}".format(tmp_uncerUp**0.5))

    return resultsXS

# parse the fit results from the MultiDim fit output "resultLog", for the bin and final state designated by "rTag"
def parseXSResults(resultLog, rTag):
    """parse the fit results from the MultiDim fit output "resultLog", for the bin and final state designated by "rTag"

    Args:
        resultLog (str): This contains full log output of the combine log from MultiDim filt
        rTag (str): This contains the bin and final state inforamation, that will help to get useful information

    Returns:
        dict: dict having central, up and down values.
    """
    try:
        fXS_c = float(resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" ")[0])
        fXS_d = float('-'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[0])
        fXS_u = float('+'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[1])
        fXS = {'central':fXS_c, 'uncerDn':fXS_d, 'uncerUp':fXS_u}
        return fXS
    except IndexError:
        logger.error("Parsing Failed!!! Inserting dummy values!!! check log!!!")
        fXS = {'central':-1.0, 'uncerDn':0.0, 'uncerUp':0.0}
        return fXS

### Extract the results and do plotting
def extractResults(obsName, observableBins, modelName, physicalModel, asimovModelName, asimovPhysicalModel, resultsXS, year = 2018):
    # Run combineCards and text2workspace
    logger.info('[Extract the results and do plotting obsName "'+obsName.replace(' ','_')+'" using '+modelName+']')
    logger.debug("physicalModel: {}".format(physicalModel))
    logger.debug("resultsXS: {}".format(resultsXS))

    logger.debug('obsName: {}'.format(obsName))
    logger.debug('observableBins: {}'.format(observableBins))

    ListObsName = (''.join(obsName.split())).split('vs')
    logger.debug('ListObsName: {}'.format(ListObsName))

    # INFO: in case of 2D obs nbins is n else its n-1
    logger.debug("len(observableBins): = "+str(len(observableBins)))
    nBins = len(observableBins) -1
    if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
        nBins = len(observableBins)
    logger.debug("nBins: = "+str(nBins))

    currentDir = os.getcwd(); os.chdir(combineOutputs.format(year = year))
    fStates = channels_central
    AllChannelCombinedDataCards = 'hzz4l_all_13TeV_xs_{obsName}_bin_{physicalModel}.txt '

    for fState in fStates:
        """Combine cards for all bins corresponding to each final state.
        """
        if year == "allYear":
            cmd = 'combineCards.py '
            for year_ in ['2016', '2017', '2018']:
                pathOfCard = '../'+combineOutputs.format(year = year_)
                # pathOfCard = "" # since each card already had the path attached with the root file so no need to attach the path
                logger.info("path of datacard for year_ - {}: {}".format(year_, pathOfCard))
                # cmd +=  pathOfCard + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)
                cmd += obsName+'_4e4mu2e2mu_'+year_ + '=' + pathOfCard + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)
            # FIXME: Hardcoded dir string year_
            pathOfCard = '../'+combineOutputs.format(year = year)
            cmd += ' > ' + pathOfCard + '/' + AllChannelCombinedDataCards.format(obsName = obsName.replace(' ','_'), physicalModel = physicalModel)
            processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        if year == "allYear": break
        # if (nBins>1):
        cmd = 'combineCards.py '
        # pathOfCard = combineOutputs.format(year = year)
        pathOfCard = "."
        for obsBin in range(nBins):
            cmd +=   obsName + '_' + fState + 'S_'+str(obsBin)+'_'+year + '=' +pathOfCard+'/hzz4l_'+fState+'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '
        cmd += ' > '+pathOfCard+'/'+'hzz4l_'+fState+'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt' # Output combine card name
        processCmd(cmd, get_linenumber(),  os.path.basename(__file__), 1)

    # pathOfCard = combineOutputs.format(year = year)
    pathOfCard = "."
    logger.info("obsName: "+obsName)
    # combine 3 final state cards
    if year != "allYear":
        cmd = 'combineCards.py '
        for channels_ in fStates:
            cmd += obsName + '_' + channels_ + 'S_' + year + '='+ pathOfCard + '/hzz4l_' + channels_ + 'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt  '
        cmd += ' >  ' + pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt'
        processCmd(cmd, get_linenumber(), os.path.basename(__file__), 1)

    # cmd = 'combineCards.py '
    # for year_ in ['2016', '2017', '2018']:
    #   for fState in fStates:
    #     for obsBin in range(nBins):
    #       cmd += obsName.replace(' ','_')+'_'+fState+'_bin'+str(obsBin)+'_'+year_+'='+combineOutputs.format(year = year_)+'/hzz4l_'+fState+'S_13TeV_xs_'+obsName.replace(' ','_')+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '
    # cmd += ' > ' + combineOutputs.format(year = year_) + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt'
    # processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> ' + pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> ' + pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> ' + pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt')

    if (physicalModel=="v2"):
        cmd = 'text2workspace.py '+ pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins)+' -o  ' + pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber(), os.path.basename(__file__))
    if (physicalModel=="v3"):
        cmd = 'text2workspace.py '+ pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducialV3 --PO higgsMassRange=115,135 --PO nBin='+str(nBins)+' -o  ' + pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
        processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    cmd = 'mv ' +pathOfCard + '/hzz4l_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root ' + pathOfCard + '/' + modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root'
    processCmd(cmd, get_linenumber(), os.path.basename(__file__), 1)

    os.chdir(currentDir)

    pathOfCard = combineOutputs.format(year = year)
    toyFileName = "toy_asimov"
    # if (opt.UNBLIND):
        # toyFileName = "data_obs"
    cmd = 'root -l -b -q "src/addToyDataset.C(\\"'+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+'.root\\",\\"'+pathOfCard+'/'+asimovModelName+'_all_'+obsName.replace(' ','_')+'_13TeV_Asimov_'+asimovPhysicalModel+unblindString+'.root\\",\\"'+toyFileName+'\\",\\"'+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root\\")"'
    processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    # Run the Combine
    if (physicalModel=="v3"):
        if (not opt.FIXFRAC):
            if (opt.FIXMASS=="False"):
                cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str(year)+unblindString+' -M MultiDimFit '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root -m 125.0 -D toy_asimov '
            else:
                cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str(year)+unblindString+' -M MultiDimFit '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root -m '+opt.FIXMASS+' -D toy_asimov --setParameters MH='+opt.FIXMASS
            # you can add fractions to the POIs if you want the uncertainties on frac4e, frac4mu
            for bin in range(nBins):
                cmd = cmd + ' -P SigmaBin'+str(bin)
                #cmd = cmd + ' -P SigmaBin'+str(bin)+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)
            if (opt.FIXMASS=="False"):
                cmd = cmd + ' -P MH'
            cmd = cmd + ' --floatOtherPOIs=1 --saveWorkspace'
            if (not opt.FIXMASS=="False"):
                cmd = cmd + ' --setParameterRanges MH='+opt.FIXMASS+','+opt.FIXMASS#+'001'
                #cmd = cmd + ' --freezeNuisanceGroups MH '
            if (opt.UNBLIND):
                cmd = cmd.replace('-D toy_asimov',' ')
            output=processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            if (opt.FIXMASS=="False"):
                processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH125.root '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root', get_linenumber(), os.path.basename(__file__), 1)
            else:
                processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.FIXMASS.replace('.0.root','.root')+'.root '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root', get_linenumber(), os.path.basename(__file__), 1)
            cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
            output=processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        else:
            # import acc factors
            _temp = __import__('inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['acc'], -1)
            acc = _temp.acc

            tmp_xs = {}
            tmp_xs_sm = {}
            # nBins = len(observableBins)
            for fState in fStates:
                for obsBin in range(nBins):
                    fidxs_sm = 0
                    fidxs_sm += higgs_xs['ggH_125.38']*higgs4l_br['125.38_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    #fidxs_sm += acc['ggH_HRes_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['VBF_125.38']*higgs4l_br['125.38_'+fState]*acc['VBF_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['WH_125.38']*higgs4l_br['125.38_'+fState]*acc['WH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['ZH_125.38']*higgs4l_br['125.38_'+fState]*acc['ZH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['ttH_125.38']*higgs4l_br['125.38_'+fState]*acc['ttH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs = 0
                    if (not opt.FIXMASS=="False"):
                        fidxs += higgs_xs['ggH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        #fidxs += acc['ggH_HRes_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['VBF_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['VBF_powheg_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['WH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['WH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['ZH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ZH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                        fidxs += higgs_xs['ttH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ttH_powheg_JHUgen_125.38_'+fState+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    else: fidxs = fidxs_sm

                    tmp_xs_sm[fState+'_genbin'+str(obsBin)] = fidxs_sm

                    if (opt.FIXMASS=="False"):
                        tmp_xs[fState+'_genbin'+str(obsBin)] = fidxs_sm
                    else:
                        tmp_xs[fState+'_genbin'+str(obsBin)] = fidxs

            if (opt.FIXMASS=="False"):
                cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str(year)+unblindString+' -M MultiDimFit '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root -m 125.0 -D toy_asimov  --setParameters '
            else:
                cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str(year)+unblindString+' -M MultiDimFit '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root -m '+opt.FIXMASS+' -D toy_asimov --setParameters MH='+opt.FIXMASS+','
            for obsBin in range(nBins):
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
            for bin in range(nBins):
                #cmd = cmd + ' -P SigmaBin'+str(bin)+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)
                cmd = cmd + ' -P SigmaBin'+str(bin)#+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)

            if (opt.FIXMASS=="False"):
                cmd = cmd+' -P MH --floatOtherPOIs=1'
            else:
                cmd = cmd+' --floatOtherPOIs=1'

            cmd = cmd + ' --saveWorkspace --setParameterRanges '
            for obsBin in range(nBins):
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
                cmd = cmd.replace('-D toy_asimov',' ')
            output=processCmd(cmd, get_linenumber(), os.path.basename(__file__))

            if (opt.FIXMASS=="False"):
                processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH125.root '+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root', os.path.basename(__file__), 1)
            else:
                processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.FIXMASS.rstrip('.0')+'.root '+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root', os.path.basename(__file__), 1)
            cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
            output=processCmd(cmd, get_linenumber(), os.path.basename(__file__))

    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName.replace(' ','_')+'_'+str(year)+unblindString+' -M MultiDimFit '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root -D toy_asimov --saveWorkspace'
        if (not opt.FIXMASS=="False"):
            cmd = cmd + ' -m '+opt.FIXMASS+' --setParameterRanges MH='+opt.FIXMASS+','+opt.FIXMASS#+'001'
        else:
            cmd = cmd + ' -m 125.0'
        if (opt.UNBLIND):
            cmd = cmd.replace('-D toy_asimov',' ')
        output=processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        if (opt.FIXMASS=="False"):
            processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH125.root '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root', get_linenumber(), os.path.basename(__file__), 1)
        else:
            # FIXME: seems like `opt.FIXMASS.rstrip('.0')` this part may do something wrong later.
            processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.FIXMASS.rstrip('.0')+'.root '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root', get_linenumber(), os.path.basename(__file__), 1)
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        output=processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.root '+pathOfCard+'/', get_linenumber(), os.path.basename(__file__))
        # sys.exit()
    # parse the results for all the bins
    logger.debug("resultsXS: {}".format(resultsXS))
    for obsBin in range(nBins):
        if (physicalModel=="v3"):
            resultsXS[modelName+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)] = parseXSResults(output,'SigmaBin'+str(obsBin)+' :')
            logger.debug("""
                nBins = {:2}, obsBins = {:2}, physicalModel = {},
                key = {},
                resultsXS = {}
            """.format(
                nBins, obsBin, physicalModel, modelName+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin), resultsXS[modelName+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)]
            ))
        elif (physicalModel=="v2"):
            for fState in fStates:
                resultsXS[modelName+'_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+str(obsBin)] = parseXSResults(output, 'r'+fState+'Bin'+str(obsBin)+' :')
                logger.debug("""
                    nBins = {:2}, obsBins = {:2}, final State: {:4}, physicalModel = {},
                    key = {},
                    resultsXS = {}
                """.format(
                    nBins, obsBin, fState, physicalModel, modelName+'_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+str(obsBin), resultsXS[modelName+'_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+str(obsBin)]
                ))
    logger.debug("resultsXS: {}".format(resultsXS))
    # load best fit snapshot and run combine with no systematics for stat only uncertainty
    if (opt.SYS):
        cmd = cmd.replace(pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_exp.root','-d '+pathOfCard+'/'+modelName+'_all_13TeV_xs_'+obsName.replace(' ','_')+'_bin_'+physicalModel+unblindString+'_result.root -w w --snapshotName "MultiDimFit"')
       #VM Test:  cmd = cmd + ' --freezeNuisanceGroups CMS_fakeH_p1_1_8,CMS_fakeH_p1_2_8,CMS_fakeH_p1_3_8,CMS_fakeH_p3_1_8,CMS_fakeH_p3_2_8,CMS_fakeH_p3_3_8 --freezeParameters allConstrainedNuisances'
        cmd = cmd + ' --freezeParameters allConstrainedNuisances'

        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        processCmd('mv higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+unblindString+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.root '+pathOfCard+'/higgsCombine'+obsName.replace(' ','_')+'_'+str(year)+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+unblindString+'_FreezAllConstrainedNuisances.root ', get_linenumber(), os.path.basename(__file__))
        # parse the results
        for obsBin in range(nBins):
            if (physicalModel=="v3"):
                resultsXS[modelName+'_'+obsName.replace(' ','_')+'_genbin'+str(obsBin)+'_statOnly'] = parseXSResults(output,'SigmaBin'+str(obsBin)+' :')
            elif (physicalModel=="v2"):
                for fState in fStates:
                    resultsXS[modelName+'_'+obsName.replace(' ','_')+'_'+fState+'_genbin'+str(obsBin)+'_statOnly'] = parseXSResults(output, 'r'+fState+'Bin'+str(obsBin)+' :')

    return resultsXS

### Extract model dependance uncertnaities from the fit results
def addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName, physicalModel):

    logger.debug('[Extract model dependance uncertnaities from the fit results for obsName "'+obsName.replace(' ','_')+'" using '+']')

    logger.warning('resultsXS: {}'.format(resultsXS))

    logger.debug('obsName: {}'.format(obsName))
    logger.debug('observableBins: {}'.format(observableBins)) # AsimovData_mass4l_4e_genbin0

    ListObsName = (''.join(obsName.split())).split('vs')
    logger.debug('ListObsName: {}'.format(ListObsName))

    # INFO: in case of 2D obs nbins is n else its n-1
    nBins = len(observableBins) -1
    if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
        nBins = len(observableBins)
    logger.debug("nBins: = "+str(nBins))

    if (opt.UNBLIND): DataModel = 'SM_125_'
    else: DataModel = 'AsimovData_'

    modelIndependenceUncert = {}
    if (physicalModel=="v2"):
        for obsBin in range(nBins):
            for fState in channels_central:
                modelIndependenceUncert[DataModel + obsName.replace(' ','_') +'_'+fState+ '_genbin'+str(obsBin)] = {'uncerDn':0.0, 'uncerUp':0.0}

        logger.debug ("modelIndependenceUncert: {}".format(modelIndependenceUncert))
        for key, value in resultsXS.iteritems():
            if (opt.UNBLIND and key.startswith('Asimov')): continue
            for obsBin in range(nBins):
                for fState in channels_central:
                    binTag = str(obsBin)
                    if (obsName.replace(' ','_')+'_'+fState+'_genbin'+binTag) in key:
                        asimCent = resultsXS[DataModel + obsName.replace(' ','_') + '_' + fState+'_genbin'+binTag]['central']
                        keyCent = resultsXS[key]['central']
                        diff = keyCent - asimCent
                        if (diff<0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_'+fState+'_genbin'+binTag]['uncerDn'])):
                            modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_'+fState+'_genbin'+binTag]['uncerDn'] = float("{0:.4f}".format(diff))
                        if (diff>0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_'+fState+'_genbin'+binTag]['uncerUp'])):
                            modelIndependenceUncert[DataModel + obsName.replace(' ','_') +'_'+fState+ '_genbin'+binTag]['uncerUp'] = float("{0:.4f}".format(diff))

    if (physicalModel=="v3"):
        for obsBin in range(nBins):
            modelIndependenceUncert[DataModel + obsName.replace(' ','_') +'_genbin'+str(obsBin)] = {'uncerDn':0.0, 'uncerUp':0.0}

        for key, value in resultsXS.iteritems():
            if (opt.UNBLIND and key.startswith('Asimov')): continue
            for obsBin in range(nBins):
                binTag = str(obsBin)
                if (obsName.replace(' ','_')+'_genbin'+binTag) in key:
                    asimCent = resultsXS[DataModel + obsName.replace(' ','_') + '_genbin'+binTag]['central']
                    keyCent = resultsXS[key]['central']
                    diff = keyCent - asimCent
                    if (diff<0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_genbin'+binTag]['uncerDn'])):
                        modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_genbin'+binTag]['uncerDn'] = float("{0:.4f}".format(diff))
                    if (diff>0) and (abs(diff) > abs(modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_genbin'+binTag]['uncerUp'])):
                        modelIndependenceUncert[DataModel + obsName.replace(' ','_') + '_genbin'+binTag]['uncerUp'] = float("{0:.4f}".format(diff))

    return modelIndependenceUncert

### run all the steps towards the fiducial XS measurement
def runFiducialXS():

    # parse the arguments and options
    global opt, args, runAllSteps
    parseOptions()

    # save working dir
    jcpDir = os.getcwd()

    year = opt.ERA

    # prepare the set of bin boundaries to run over, only 1 bin in case of the inclusive measurement
    # observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    # FIXME & DISCUSS: When we need the above mentioned feature? Get back this feature.???

    ### Run for the given observable
    obsName = opt.OBSNAME
    ListObsName = (''.join(obsName.split())).split('vs')

    logger.info('Running fiducial XS computation for - {} - bin boundaries: {}'.format(obsName, opt.OBSBINS))

    # INFO: Call read bins to parse the input bins information
    observableBins = read_bins(opt.OBSBINS)
    logger.info("Parsed bins: {}".format(observableBins))
    logger.debug("Bin size = "+str(len(observableBins)))
    nBins = len(observableBins) -1
    if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
        nBins = len(observableBins)
    logger.debug("nBins: = "+str(nBins))

    obs_ifJES = ''
    obs_ifJES2 = ''

    obs_ifAbs = ''
    obs_ifAbs2 = ''

    ObsToStudy = "1D_Observables" if (len(ListObsName) == 1) else "2D_Observables"
    with open(opt.inYAMLFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        if ( ("Observables" not in cfg) or (ObsToStudy not in cfg['Observables']) ) :
            logger.error('''No section named 'observable' or sub-section name '1D-Observable' or '2D-Observable' found in file {}.
                     Please check your YAML file format!!!'''.format(opt.inYAMLFile))

        ifJES = cfg['Observables'][ObsToStudy][opt.OBSNAME]['ifJES']
        ifAbs = cfg['Observables'][ObsToStudy][opt.OBSNAME]['ifAbs'] # FIXME for 2D

    if 'vs' in opt.OBSNAME:
        obs_ifJES = eval(ifJES.split(" vs ")[0])
        obs_ifJES2 = eval(ifJES.split(" vs ")[1])

        obs_ifAbs = eval(ifAbs.split(" vs ")[0])
        obs_ifAbs2 = eval(ifAbs.split(" vs ")[1])

    else:
        obs_ifJES = eval(str(ifJES))
        obs_ifJES2 = ''

        obs_ifAbs = eval(str(ifAbs))
        obs_ifAbs2 = ''


    logger.debug("obs_ifJES: {}, obs2_ifJES2: {}".format(obs_ifJES, obs_ifJES2))

    ## Prepare templates for all reco bins and final states
    logger.debug("Options:\n\trunAllSteps: {}\n\topt.templatesOnly {}\n\topt.resultsOnly\n".format(runAllSteps, opt.templatesOnly, opt.resultsOnly))

    resultsXS = {}
    asimovDataModelName = "SM_125" # FIXME: Is it fine if the model name is hardcoded here. Since model (ASIMOVMODEL) is also an input argument
    asimovPhysicalModel = "v2" # FIXME: Same above message.

    # FIXME: Why for mass4l we are using two versions while for others only v3.
    if (obsName == "mass4l"): physicalModels = ["v2","v3"]
    else: physicalModels = ["v3"]

    # FIXME: Understand why in step 4; runAllSteps is False, while in step 5 its True
    logger.debug("(runAllSteps or opt.templatesOnly) and year.isdigit() = {}".format((runAllSteps or opt.templatesOnly) and year.isdigit()))
    if ((runAllSteps or opt.templatesOnly) and year.isdigit()): # Don't run this for all year. "year.isdigit()" is added to skip when "allYear" option is provided
        extractBackgroundTemplatesAndFractions(obsName, observableBins, year, obs_ifJES, obs_ifJES2)

    logger.debug("resultsXS: {}".format(resultsXS))
    if year == "allYear":
        logger.info("Option opt: Combination of all years.")
        resultsXS = createAsimov_161718(obsName, observableBins, asimovDataModelName, resultsXS, asimovPhysicalModel,  ['2016', '2017', '2018'], obs_ifJES)
        logger.debug("resultsXS: {}".format(resultsXS))
        # plot the asimov predictions for data, signal, and backround in differential bins
        if ( (not (obsName=="mass4l")) and ("vs" not in obsName)):
            cmd = 'python python/plotDifferentialBins.py -l -q -b --obsName="'+obsName.replace(' ','_')+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --inYAMLFile="'+opt.inYAMLFile+'" --year="'+year+'"'
            if (opt.UNBLIND): cmd = cmd + ' --unblind'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            logger.debug(output)

    ## Create the asimov dataset
    if (runAllSteps and year != "allYear"):
        logger.info('Run addConstrainedModel')
        cmd = 'python python/addConstrainedModel.py -l -q -b --obsName="'+opt.OBSNAME+'" --obsBins="'+opt.OBSBINS+'" --year="'+year+'"'
        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        logger.debug("""
            obsName = {},
            observableBins = {}
            asimovDataModelName = {}
            asimovPhysicalModel = {}""".format(obsName, observableBins, asimovDataModelName, asimovPhysicalModel))
        logger.info("Going to produce datacards...")
        # INFO: Pass the updated bins information here
        #produceDatacards(obsName, observableBins, asimovDataModelName, asimovPhysicalModel, obs_ifJES, obs_ifJES2, year)
        produceDatacards(obsName, observableBins, asimovDataModelName, asimovPhysicalModel, obs_ifJES, obs_ifJES2, obs_ifAbs, obs_ifAbs2, year)
        logger.info("Create the Asimov dataset...")
        resultsXS = createAsimov(obsName, observableBins, asimovDataModelName, resultsXS, asimovPhysicalModel, year, obs_ifJES)
        logger.debug("resultsXS: {}".format(resultsXS))
        # plot the asimov predictions for data, signal, and backround in differential bins
        if ( (not (obsName=="mass4l")) and ("vs" not in obsName)):
            cmd = 'python python/plotDifferentialBins.py -l -q -b --obsName="'+obsName.replace(' ','_')+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --inYAMLFile="'+opt.inYAMLFile+'" --year="'+year+'"'
            if (opt.UNBLIND): cmd = cmd + ' --unblind'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            logger.debug(output)

    ## Extract the results
    # use constrained SM
    modelNames = opt.MODELNAMES
    modelNames = modelNames.split(',')
    logger.info("model name: {}".format(modelNames))

    if (runAllSteps or opt.resultsOnly):
        for physicalModel in physicalModels:
            for modelName in modelNames:
                logger.debug("Produce datacard for physicsModel - {}, and modelName - {}".format(physicalModel, modelName))
                logger.debug("""
                    obsName = {},
                    observableBins = {}
                    asimovDataModelName = {}
                    asimovPhysicalModel = {}""".format(obsName, observableBins, modelName, physicalModel))
                #if (year != "allYear"): produceDatacards(obsName, observableBins, modelName, physicalModel, obs_ifJES, obs_ifJES2, year)
                if (year != "allYear"): produceDatacards(obsName, observableBins, modelName, physicalModel, obs_ifJES, obs_ifJES2, obs_ifAbs, obs_ifAbs2, year)
                logger.debug("Extract results for physicsModel - {}, and modelName - {}".format(physicalModel, modelName))
                resultsXS = extractResults(obsName, observableBins, modelName, physicalModel, asimovDataModelName, asimovPhysicalModel, resultsXS, year)
                # plot the fit results
                if ( (not (obsName == "mass4l")) and year != "allYear"):
                    # identify 1D or 2D obs using `ListObsName` length
                    cmd = 'python python/plotAsimov_simultaneous.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'" --obs='+str(len(ListObsName)) + ' --year="'+year+'"'# +' --lumiscale=str(opt.LUMISCALE)'
                    if (opt.UNBLIND): cmd = cmd + ' --unblind'
                    output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
                    print (output)
                elif (physicalModel=="v2" and year != "allYear"):
                    cmd = 'python python/plotAsimov_inclusive.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'"' + ' --year="'+year+'"' #+' --lumiscale=str(opt.LUMISCALE)'
                    if (opt.UNBLIND): cmd = cmd + ' --unblind'
                    output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
                    print (output)

            ## Calculate model dependance uncertainties
            logger.debug("Calculate model dependence uncertainties for physicsModel - {}, and modelName - {}".format(physicalModel, asimovDataModelName))
            modelIndependenceUncert = addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName,physicalModel)
            logger.debug("modelIndependenceUncert: \n{}".format(modelIndependenceUncert))
            if (opt.FIXFRAC): floatfix = '_fixfrac'
            else: floatfix = ''
            with open(datacardInputs.format(year = year)+'/resultsXS_'+obsName.replace(' ','_')+'_'+physicalModel+floatfix+'.py', 'w') as f:
                f.write('modelNames = '+json.dumps(modelNames)+';\n')
                f.write('asimovDataModelName = '+json.dumps(asimovDataModelName)+';\n')
                f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
                f.write('modelIndUncert = '+json.dumps(modelIndependenceUncert))

    logger.debug("Options:\n\trunAllSteps: {}\n\topt.finalplotsOnly {}\n".format(runAllSteps,opt.finalplotsOnly))

    # Merge all year resultsXS
    if (year == "allYear"):
        _temp = __import__((datacardInputs.format(year = '2016')).replace('/','.') + '.' + 'inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['acc'], -1)
        inputs_sig_2016 = _temp.acc
        _temp = __import__((datacardInputs.format(year = '2017')).replace('/','.') + '.' + 'inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['acc'], -1)
        inputs_sig_2017 =  _temp.acc
        _temp = __import__((datacardInputs.format(year = '2018')).replace('/','.') + '.' + 'inputs_sig_'+obsName.replace(' ','_'), globals(), locals(), ['acc'], -1)
        inputs_sig_2018 =  _temp.acc

        _temp = __import__((datacardInputs.format(year = '2016')).replace('/','.') + '.' + 'accUnc_'+obsName.replace(' ','_'), globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
        acc_ggH_powheg_2016 = _temp.acc
        pdfunc_ggH_powheg_2016 = _temp.pdfUncert
        qcdunc_ggH_powheg_2016 = _temp.qcdUncert

        _temp = __import__((datacardInputs.format(year = '2017')).replace('/','.') + '.' + 'accUnc_'+obsName.replace(' ','_'), globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
        acc_ggH_powheg_2017 = _temp.acc
        pdfunc_ggH_powheg_2017 = _temp.pdfUncert
        qcdunc_ggH_powheg_2017 = _temp.qcdUncert

        _temp = __import__((datacardInputs.format(year = '2018')).replace('/','.') + '.' + 'accUnc_'+obsName.replace(' ','_'), globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
        acc_ggH_powheg_2018 = _temp.acc
        pdfunc_ggH_powheg_2018 = _temp.pdfUncert
        qcdunc_ggH_powheg_2018 = _temp.qcdUncert

        inputs_sig_allYear = mergeDictionary_average(inputs_sig_2016, inputs_sig_2017, inputs_sig_2018)

        with open(datacardInputs.format(year = year)+'/inputs_sig_'+obsName.replace(' ','_')+'.py', 'w') as f:
            f.write('acc = '+json.dumps(inputs_sig_allYear)+';\n')

        accUnc_acc_allYear      = mergeDictionary_average(acc_ggH_powheg_2016, acc_ggH_powheg_2017, acc_ggH_powheg_2018)
        accUnc_pdfunc_allYear      = mergeDictionary_average(pdfunc_ggH_powheg_2016, pdfunc_ggH_powheg_2017, pdfunc_ggH_powheg_2018)
        accUnc_qcdunc_allYear      = mergeDictionary_average(qcdunc_ggH_powheg_2016, qcdunc_ggH_powheg_2017, qcdunc_ggH_powheg_2018)

        with open(datacardInputs.format(year = year)+'/accUnc_'+obsName.replace(' ','_')+'.py', 'w') as f:
            f.write('acc = '+json.dumps(accUnc_acc_allYear)+';\n')
            f.write('pdfUncert = '+json.dumps(accUnc_pdfunc_allYear)+';\n')
            f.write('qcdUncert = '+json.dumps(accUnc_qcdunc_allYear)+';\n')

    # Make final differential plots
    if (runAllSteps or opt.finalplotsOnly):
        logger.debug("Running combine...")
        DatasetForObservedLimit = "toy_asimov"
        if (opt.UNBLIND):
            DatasetForObservedLimit = "data_obs"

        if (obsName=="mass4l"):

            # These commands for observed data
            # with systematics
            # FIXME: Check the result of --points=50  and --points=500 improves results/not? In earlier version it was set to 500.
            # FIXME: hardcoded higgs mass value to 125.38
            cmd = 'combine -n mass4l_SigmaBin0'+'_'+str(year)+unblindString+' -M MultiDimFit '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v3'+unblindString+'_exp.root -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin0=0.0,5.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=300'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_SigmaBin0"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            # no systematics
            cmd = 'combine -n mass4l_SigmaBin0_NoSys'+'_'+str(year)+unblindString+' -M MultiDimFit -d '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v3'+unblindString+'_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P SigmaBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin0=0.0,5.0 --redefineSignalPOI SigmaBin0 --algo=grid --points=300  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_SigmaBin0_NoSys"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            #### These commands for observed data
            # 4e
            # with systematics
            cmd = 'combine -n mass4l_r4eBin0'+'_'+str(year)+unblindString+' -M MultiDimFit '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v2'+unblindString+'_exp.root -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P r4eBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:r4eBin0=0.0,5.0 --redefineSignalPOI r4eBin0 --algo=grid --points=300'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_r4eBin0"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            # no systematics
            cmd = 'combine -n mass4l_r4eBin0_NoSys'+'_'+str(year)+unblindString+' -M MultiDimFit -d '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v2'+unblindString+'_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P r4eBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:r4eBin0=0.0,5.0 --redefineSignalPOI r4eBin0 --algo=grid --points=300  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_r4eBin0_NoSys"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            # 4mu
            # with systematics
            cmd = 'combine -n mass4l_r4muBin0'+'_'+str(year)+unblindString+' -M MultiDimFit '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v2'+unblindString+'_exp.root -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P r4muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:r4muBin0=0.0,5.0 --redefineSignalPOI r4muBin0 --algo=grid --points=300'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_r4muBin0"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            # no systematics
            cmd = 'combine -n mass4l_r4muBin0_NoSys'+'_'+str(year)+unblindString+' -M MultiDimFit -d '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v2'+unblindString+'_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P r4muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:r4muBin0=0.0,5.0 --redefineSignalPOI r4muBin0 --algo=grid --points=300  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_r4muBin0_NoSys"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            # 2e2mu
            # with systematics
            cmd = 'combine -n mass4l_r2e2muBin0'+'_'+str(year)+unblindString+' -M MultiDimFit '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v2'+unblindString+'_exp.root -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P r2e2muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:r2e2muBin0=0.0,5.0 --redefineSignalPOI r2e2muBin0 --algo=grid --points=300'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_r2e2muBin0"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

            # no systematics
            cmd = 'combine -n mass4l_r2e2muBin0_NoSys'+'_'+str(year)+unblindString+' -M MultiDimFit -d '+combineOutputs.format(year = year)+'/SM_125_all_13TeV_xs_mass4l_bin_v2'+unblindString+'_result.root -w w --snapshotName "MultiDimFit" -m 125.38 -D '+DatasetForObservedLimit+' --setParameters MH=125.38 -P r2e2muBin0 --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:r2e2muBin0=0.0,5.0 --redefineSignalPOI r2e2muBin0 --algo=grid --points=300  --freezeParameters allConstrainedNuisances'
            output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
            processCmd("mv higgsCombinemass4l_r2e2muBin0_NoSys"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

        else:
            for obsBin in range(0,nBins):
                cmd = "combine -n "+obsName.replace(' ','_')+"_SigmaBin"+str(obsBin)+'_'+str(year)+unblindString+" -M MultiDimFit -d "+combineOutputs.format(year = year)+"/SM_125_all_13TeV_xs_"+obsName.replace(' ','_')+"_bin_"+physicalModel+unblindString+"_exp.root -m 125.38 -D "+DatasetForObservedLimit+" --setParameters MH=125.38 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin"+str(obsBin)+"=0.0,3.0 --redefineSignalPOIs SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4 "
                logger.debug("combine command: {}".format(cmd))

                # FIXME: Along with observables in the YAML file we can also add this custom sigmaBin range???
                # if (obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='1'): cmd = cmd.replace('0.0,3.0','0.0,1.5')
                # if (obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='2'): cmd = cmd.replace('0.0,3.0','0.0,0.7')
                if (obsName=='mass4l' and str(obsBin)=='0'): cmd = cmd.replace('0.0,3.0','0.0,5.0')
                #if (obsName=='pT4l' and str(obsBin)=='7'): cmd = cmd.replace('0.0,3.0','0.0,2.0')
                if (obsName=='pT4l'): cmd = cmd.replace('0.0,3.0','0.0,2.0') # TJ
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='0'): cmd = cmd.replace('0.0,3.0','0.0,4.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='2'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='3'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and str(obsBin)=='4'): cmd = cmd.replace('0.0,3.0','0.0,1.0')

                output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
                processCmd("mv higgsCombine"+obsName.replace(' ','_')+"_SigmaBin"+str(obsBin)+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

                #cmd = "combine -n "+obsName.replace(' ','_')+"_SigmaBin"+str(obsBin)+"_NoSys"+'_'+str(year)+unblindString+" -M MultiDimFit -d "+combineOutputs.format(year = year)+"/SM_125_all_13TeV_xs_"+obsName.replace(' ','_')+"_bin_"+physicalModel+unblindString+"_result.root -w w --snapshotName \"MultiDimFit\" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin"+str(obsBin)+"=0.0,3.0 --redefineSignalPOI SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4 "
                cmd = "combine -n "+obsName.replace(' ','_')+"_SigmaBin"+str(obsBin)+"_NoSys"+'_'+str(year)+unblindString+" -M MultiDimFit -d "+combineOutputs.format(year = year)+"/SM_125_all_13TeV_xs_"+obsName.replace(' ','_')+"_bin_"+physicalModel+unblindString+"_result.root -w w --snapshotName \"MultiDimFit\" -m 125.38 -D "+DatasetForObservedLimit+" --setParameters MH=125.38 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin"+str(obsBin)+"=0.0,2.0 --redefineSignalPOI SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4 " # TJ
                cmd += " --freezeParameters allConstrainedNuisances "
                # cmd = cmd + ' --freezeParameters '
                # loopYear = []
                # if year == "allYear": loopYear = ['2016', '2017','2018']
                # else: loopYear = [str(year)]
                # for year_ in loopYear:
                #     cmd = cmd + 'CMS_fakeH_p1_1'+year_+',CMS_fakeH_p1_2'+year_+',CMS_fakeH_p1_3'+year_+',CMS_fakeH_p3_1'+year_+',CMS_fakeH_p3_2'+year_+',CMS_fakeH_p3_3'+year_+','
                #     cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year_)+',CMS_hzz4e_Zjets_'+str(year_)+',CMS_hzz4mu_Zjets_'+str(year_)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year_)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year_)+',CMS_zz4l_sigma_m_sig_'+str(year_)+',CMS_zz4l_n_sig_1_'+str(year_)+',CMS_zz4l_n_sig_2_'+str(year_)+',CMS_zz4l_n_sig_3_'+str(year_)+',CMS_zz4l_mean_e_sig_'+str(year_)+',CMS_zz4l_mean_m_sig_'+str(year_)+',CMS_zz4l_sigma_e_sig_'+str(year_)+','
                #     if (obs_ifJES):
                #         jes_sources_year_updated = [x.replace('year', year_) for x in jes_sources]
                #         for jes_source in jes_sources:
                #             cmd += "CMS_scale_j_"+ jes_sources_year_updated[jes_sources.index(jes_source)]+','
                # cmd = cmd + 'lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'

                output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
                processCmd("mv higgsCombine"+obsName.replace(' ','_')+"_SigmaBin"+str(obsBin)+"_NoSys"+'_'+str(year)+unblindString+".MultiDimFit.mH125.38.root "+ combineOutputs.format(year = year) + '/', get_linenumber(), os.path.basename(__file__))

        cmd = 'python python/plotLHScans.py -l -q -b --obsName="{}" --obsBins="{}" --year="{}"'.format(
            obsName.replace(' ','_'),  opt.OBSBINS, year
        )
        if (opt.UNBLIND): cmd = cmd + ' --unblind'
        output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))

        # For now, this part was moved to "RunEverything.py" as step-8
        # for modelName in modelNames:
        #     if (not opt.FIXMASS=="False"):
        #         cmd = 'python python/producePlots.py -l -q -b --obsName="'+obsName.replace(' ','_')+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --theoryMass="'+opt.FIXMASS+'"'+ ' --year="'+ year + '"'
        #     else:
        #         cmd = 'python python/producePlots.py -l -q -b --obsName="'+obsName.replace(' ','_')+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --theoryMass="125.0"'+ ' --year="'+ year + '"'

        #     if (opt.FIXFRAC): cmd = cmd + ' --fixFrac'
        #     if (opt.UNBLIND): cmd = cmd + ' --unblind'
        #     output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        #     print (output)
        #     cmd = cmd + ' --setLog'
        #     output = processCmd(cmd, get_linenumber(), os.path.basename(__file__))
        #     print (output)

if __name__ == "__main__":
    runFiducialXS()

print ("all modules successfully compiled")
