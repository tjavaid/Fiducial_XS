
#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.10.02
#-----------------------------------------------
import sys, os, pwd, commands
import optparse, shlex, re
import math
import time
from decimal import *
import json
from ROOT import *

# load XS-specific modules
sys.path.append('./datacardInputs')

from sample_shortnames_bkg import *
from createXSworkspace import createXSworkspace
from higgs_xsbr import *

### Define function for parsing options
def parseOptions():
    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',      dest='SOURCEDIR',type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--modelName',dest='MODELNAME',type='string',default='SM', help='Name of the Higgs production or spin-parity model, default is "SM", supported: "SM", "ggH", "VBF", "WH", "ZH", "ttH", "exotic","all"')
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    # action options - "redo"
    parser.add_option('',   '--redoEff',       action='store_true', dest='redoEff',      default=False, help='Redo the eff. factors, default is False')
    parser.add_option('',   '--redoTemplates', action='store_true', dest='redoTemplates',default=False, help='Redo the bkg shapes and fractions, default is False')
    # action options - "only"
    parser.add_option('',   '--effOnly',       action='store_true', dest='effOnly',      default=False, help='Extract the eff. factors only, default is False')
    parser.add_option('',   '--templatesOnly', action='store_true', dest='templatesOnly',default=False, help='Prepare the bkg shapes and fractions only, default is False')
    parser.add_option('',   '--uncertOnly',    action='store_true', dest='uncertOnly',   default=False, help='Extract the uncertanties only, default is False')
    parser.add_option('',   '--resultsOnly',   action='store_true', dest='resultsOnly',  default=False, help='Run the measurement only, default is False')


    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

    # prepare the global flag if all the step should be run
    runAllSteps = not(opt.effOnly or opt.templatesOnly or opt.uncertOnly or opt.resultsOnly)

    if (opt.OBSBINS=='' and opt.OBSNAME!='inclusive'):
        parser.error('Bin boundaries not specified for differential measurement. Exiting...')
        sys.exit()

    dirToExist = ['templates','datacardInputs','125.6','xs_125.6']
    for dir in dirToExist:
        if not os.path.isdir(os.getcwd()+'/'+dir+'/'):
            parser.error(os.getcwd()+'/'+dir+'/ is not a directory. Exiting...')
            sys.exit()

### Define function for processing of os command
def processCmd(cmd, quiet = 0):
    #print cmd
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quiet):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    if (not quiet):
        print 'Output:\n   ['+output+'] \n'                
    return output


### Extract the all efficiency factors (inclusive/differential, all bins, all final states)
def extractFiducialEfficiencies(obsName, observableBins, modelName):

    #from inputs_bkg_{obsName} import fractionsBackground and observableBins
    if (not opt.redoEff):
        print '[Skipping eff. and out.factors for '+str(obsName)+']'
        return

    print '[Extracting eff. and out.factors]'
    # determine the ntuples/scipts to use from the path to ntuples [must contain only "sperka" or only "tchen"]
    # need a better way to handle this...
    if ((opt.SOURCEDIR.find("dsperka")!=-1) and (opt.SOURCEDIR.find("tcheng")==-1)):
        cmd = 'python efficiencyFactors_dsperka.py --dir='+opt.SOURCEDIR+' --obsName='+opt.OBSNAME+' --obsBins="'+opt.OBSBINS+'" -l -q -b --modelName='+modelName
#        print cmd
        output = processCmd(cmd)
    elif ((opt.SOURCEDIR.find("dsperka")==-1) and (opt.SOURCEDIR.find("tcheng")!=-1)):
        cmd = 'root -l -q -b "efficiencyFactors_tcheng.C"' # need to pass parameters on opt.SOURCEDIR, obsName, observableBins, modelName...
        #processCmd(cmd)
    else:
        print 'Ambigious type of ntuples/scipts to use ["dsperka" or "tcheng"]. Exiting...'
        sys.exit()

### Extract the templates for given obs and bin, for all final states (differential)
def extractBackgroundTemplatesAndFractions(obsName, obsBin, observableBins):
    global opt

    fractionBkg = {}
    #if exists, from inputs_bkg_{obsName} import fractionsBackground and observableBins
    if os.path.isfile('datacardInputs/inputs_bkg_'+obsName+'.py'):
        _temp = __import__('inputs_bkg_'+obsName, globals(), locals(), ['observableBins','fractionsBackground'], -1)
        if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
            print '[Fractions already exist for the given binning. Skipping templates/shapes - bin '+str(obsBin)+']'
            return
        fractionBkg = _temp.fractionsBackground

    print '[Preparing bkg shapes and fractions - bin '+str(obsBin)+' - range ('+observableBins[obsBin]+', '+observableBins[obsBin+1]+')]'
#    fractionBkg = _temp.fractionsBackground
    # save/create/prepare directories and compile templates script
    currentDir = os.getcwd(); os.chdir('./templates/')
    cmd = 'rm main_fiducialXSTemplates; make'; processCmd(cmd,1)
    cmd = 'mkdir -p templatesXS/DTreeXS_'+opt.OBSNAME+'/8TeV/'; processCmd(cmd,1)

    # extract bkg templates and bin fractions
    bkg_sample_tags = ['ZZTo2e2mu_powheg', 'ZZTo4e_powheg', 'ZZTo4mu_powheg','ggZZ_2e2mu_MCFM67', 'ggZZ_4e_MCFM67', 'ggZZ_4mu_MCFM67', 'ZX4l_CR']
    bkg_samples_shorttags = {'ZZTo2e2mu_powheg':'qqZZ', 'ZZTo4e_powheg':'qqZZ', 'ZZTo4mu_powheg':'qqZZ', 'ggZZ_2e2mu_MCFM67':'ggZZ', 'ggZZ_4e_MCFM67':'ggZZ', 'ggZZ_4mu_MCFM67':'ggZZ', 'ZX4l_CR':'ZJetsCR'}
    bkg_samples_fStates = {'ZZTo2e2mu_powheg':'2e2mu', 'ZZTo4e_powheg':'4e', 'ZZTo4mu_powheg':'4mu','ggZZ_2e2mu_MCFM67':'2e2mu', 'ggZZ_4e_MCFM67':'4e', 'ggZZ_4mu_MCFM67':'4mu', 'ZX4l_CR':'AllChans'}
    for sample_tag in bkg_sample_tags:
        if (sample_tag=='ZX4l_CR'):
            tmpSrcDir = '/scratch/osghpc/predragm/Histogramming_8TeV/rootFiles_dsperka_XS/'
        else:
            tmpSrcDir = opt.SOURCEDIR
        if (opt.OBSNAME=='njets_reco_pt30_eta4p7'):
            tmpObsName = 'nJets'
        else:
            tmpObsName = obsName
        cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' '+observableBins[obsBin]+' '+observableBins[obsBin+1]+' 8TeV templatesXS DTreeXS'
        print cmd
        output = processCmd(cmd,1)
        fractionBkg[sample_tag+'_'+bkg_samples_fStates[sample_tag]+'_'+obsName+'_recobin'+str(obsBin)] = float(output.split("[Bin fraction: ")[1].split("]")[0])
    os.chdir(currentDir)
    with open('datacardInputs/inputs_bkg_'+obsName+'.py', 'w') as f:
        f.write('fractionsBackground = '+json.dumps(fractionBkg)+';\n')
        f.write('observableBins = '+json.dumps(observableBins))

### Extract the XS-specific uncertainties for given obs and bin, for all final states (differential)
def extractUncertainties(obsName, observableBinDn, observableBinUp):
    print '[Extracting uncertainties  -  range ('+observableBinDn+', '+observableBinUp+')]'
    cmd = 'some command...with some parameters...'
    #processCmd(cmd)

### Import eff-factors and produce datacards for given obs and bin, for all final states
def produceDatacards(obsName, observableBins, modelName):
 
    print '[Producing workspace/datacards for obsName '+obsName+', bins '+str(observableBins)+']'
    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    for fState in fStates:
        for obsBin in range(nBins-1):
#            ndata = createXSworkspace(obsName,fState, nBins, obsBin, observableBins[obsBin], observableBins[obsBin+1], True, True, modelName)
            ndata = createXSworkspace(obsName,fState, nBins, obsBin, observableBins, True, True, modelName)
            os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' xs_125.6/hzz4l_"+fState+"S_8TeV_xs_bin"+str(obsBin)+".txt")

### Create the asimov dataset and return fit results
def createAsimov(obsName, observableBins, modelName, resultsXS):
    print '[Producing/merging workspaces and datacards for obsName '+obsName+' using '+modelName+']'

    # Run combineCards and text2workspace
    currentDir = os.getcwd(); os.chdir('./xs_125.6/')
    fStates = ['2e2mu','4mu','4e']
    for fState in fStates:
        cmd = 'combineCards.py hzz4l_'+fState+'S_8TeV_xs_bin0.txt hzz4l_'+fState+'S_8TeV_xs_bin1.txt hzz4l_'+fState+'S_8TeV_xs_bin2.txt hzz4l_'+fState+'S_8TeV_xs_bin3.txt > hzz4l_'+fState+'S_8TeV_xs_bin.txt'
        print cmd
        processCmd(cmd,1)
    # combine 3 final states
    cmd = 'combineCards.py hzz4l_4muS_8TeV_xs_bin.txt hzz4l_4eS_8TeV_xs_bin.txt hzz4l_2e2muS_8TeV_xs_bin.txt > hzz4l_all_8TeV_xs_bin.txt'
    print cmd
    processCmd(cmd,1)

    # text-to-workspace
    cmd = 'text2workspace.py hzz4l_all_8TeV_xs_bin.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 -o hzz4l_all_8TeV_xs_bin.root'
    print cmd
    processCmd(cmd)

    cmd = 'cp hzz4l_all_8TeV_xs_bin.root ../'+modelName+'_all_8TeV_xs_bin.root'
    print cmd
    processCmd(cmd,1)

    os.chdir(currentDir)

    # import acc factors
    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc

    # Run the Combine
    cmd =  'combine -M MultiDimFit  '+modelName+'_all_8TeV_xs_bin.root -m 125.6 --setPhysicsModelParameters '
    for fState in fStates:
        nBins = len(observableBins)
        for obsBin in range(nBins-1):
            fidxs = 0
            fidxs += higgs_xs['ggH_125.6']*higgs4l_br['125.6_'+fState]*acc['ggH_powheg15_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
            fidxs += higgs_xs['VBF_125.6']*higgs4l_br['125.6_'+fState]*acc['VBF_powheg_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
            fidxs += higgs_xs['WH_125.6']*higgs4l_br['125.6_'+fState]*acc['WH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
            fidxs += higgs_xs['ZH_125.6']*higgs4l_br['125.6_'+fState]*acc['ZH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
            fidxs += higgs_xs['ttH_125.6']*higgs4l_br['125.6_'+fState]*acc['ttH_pythia_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin0']
            cmd = cmd + 'r'+fState+'Bin'+str(obsBin)+'='+str(fidxs)+','
    cmd = cmd+'MH=125.6 -t -1 --algo=singles --cl=0.68 --robustFit=1 --saveWorkspace --saveToys'
    print cmd
    output=processCmd(cmd)

#    # parse the results for all the bins and the given final state
#    for obsBin in range(len(observableBins)-1):
#        resultsXS['AsimovData_'+obsName+'_genbin'+str(obsBin)] = parseXSResults(output,'rBin'+str(obsBin))

    # parse the results for all the bins and the given final state
    tmp_resultsXS = {}
    for fState in fStates:
        rTags = {'0':'r'+fState+'Bin0 :','1':'r'+fState+'Bin1 :','2':'r'+fState+'Bin2 :','3':'r'+fState+'Bin3 :'}
        for obsBin in range(len(observableBins)-1):
            binTag = str(obsBin)
            tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag] = parseXSResults(output,rTags[binTag])

    cmd = 'cp higgsCombineTest.MultiDimFit.mH125.6.123456.root '+modelName+'_all_8TeV_Asimov.root'
    processCmd(cmd,1)

    # merge the results for 3 final states, for the given bins
    for obsBin in range(len(observableBins)-1):
        binTag = str(obsBin)
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag] = {'central':0.0, 'uncerDn':0.0, 'uncerUp':0.0}
        tmp_central = 0.0
        tmp_uncerDn = 0.0
        tmp_uncerUp = 0.0
        for fState in fStates:
            tmp_central += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['central']
            tmp_uncerDn += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerDn']**2
            tmp_uncerUp += tmp_resultsXS[modelName+'_'+fState+'_'+obsName+'_genbin'+binTag]['uncerUp']**2
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['central'] = float("{0:.5f}".format(tmp_central))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['uncerDn'] = -float("{0:.5f}".format(tmp_uncerDn**0.5))
        resultsXS['AsimovData_'+obsName+'_genbin'+binTag]['uncerUp'] = +float("{0:.5f}".format(tmp_uncerUp**0.5))

    return resultsXS

# parse the fit results from the MultiDim fit output "resultLog", for the bin and final state designated by "rTag"
def parseXSResults(resultLog, rTag):
    fXS_c = float(resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" ")[0])
    fXS_d = float('-'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[0])
    fXS_u = float('+'+resultLog.split(rTag)[1].split(' (68%)')[0].strip().split(" -")[1].split("/+")[1])
    fXS = {'central':fXS_c, 'uncerDn':fXS_d, 'uncerUp':fXS_u}
    return fXS

### Extract the results and do plotting
def extractResults(obsName, observableBins, modelName, resultsXS):
    # Run combineCards and text2workspace
    print '[Producing/merging workspaces and datacards for obsName '+obsName+']'

    currentDir = os.getcwd(); os.chdir('./xs_125.6/')
    fStates = ['2e2mu','4mu','4e']

    for fState in fStates:
        cmd = 'combineCards.py hzz4l_'+fState+'S_8TeV_xs_bin0.txt hzz4l_'+fState+'S_8TeV_xs_bin1.txt hzz4l_'+fState+'S_8TeV_xs_bin2.txt hzz4l_'+fState+'S_8TeV_xs_bin3.txt > hzz4l_'+fState+'S_8TeV_xs_bin.txt'
        print cmd
        processCmd(cmd,1)

    cmd = 'combineCards.py hzz4l_4muS_8TeV_xs_bin.txt hzz4l_4eS_8TeV_xs_bin.txt hzz4l_2e2muS_8TeV_xs_bin.txt > hzz4l_all_8TeV_xs_bin.txt'
    print cmd
    processCmd(cmd,1)

    cmd = 'text2workspace.py hzz4l_all_8TeV_xs_bin.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducial --PO higgsMassRange=115,135 -o hzz4l_all_8TeV_xs_bin.root'
    print cmd
    processCmd(cmd)

    cmd = 'cp hzz4l_all_8TeV_xs_bin.root ../'+modelName+'_all_8TeV_xs_bin.root'
    print cmd
    processCmd(cmd,1)

    os.chdir(currentDir)

    cmd = 'root -l -b -q "addToyDataset.C(\\"'+modelName+'_all_8TeV_xs_bin.root\\",\\"ggH_powheg15_JHUgen_125_all_8TeV_Asimov.root\\",\\"toy_asimov\\",\\"'+modelName+'_all_8TeV_xs_bin_exp.root\\")"'
    print cmd
    processCmd(cmd)

    # Run the Combine
    cmd =  'combine -M MultiDimFit '+modelName+'_all_8TeV_xs_bin_exp.root -m 125.6 -D toy_asimov --algo=singles --cl=0.68 --robustFit=1'
    print cmd
    output=processCmd(cmd)

    # parse the results for all the bins
    for obsBin in range(len(observableBins)-1):
        resultsXS[modelName+'_'+obsName+'_genbin'+str(obsBin)] = parseXSResults(output,'rBin'+str(obsBin)+' :')

    # Prepare plots
    cmd = 'root -l -q -b "producePlotsXS.C(...some parameters...)"'
    #processCmd(cmd)

    return resultsXS

### Extract model dependance uncertnaities from the fit results
def addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName):
    modelIndependenceUncert = {'AsimovData_' + obsName + '_genbin0':{'uncerDn':0.0, 'uncerUp':0.0}, 'AsimovData_' + obsName + '_genbin1':{'uncerDn':0.0, 'uncerUp':0.0}, 'AsimovData_' + obsName + '_genbin2':{'uncerDn':0.0, 'uncerUp':0.0}, 'AsimovData_' + obsName + '_genbin3':{'uncerDn':0.0, 'uncerUp':0.0}}
    for key, value in resultsXS.iteritems():
        for obsBin in range(len(observableBins)-1):
            binTag = str(obsBin)
            if ('genbin'+binTag) in key:
                asimCent = resultsXS['AsimovData_' + obsName + '_genbin'+binTag]['central']
                keyCent = resultsXS[key]['central']
                diff = keyCent - asimCent
                if (diff<0) and (abs(diff) > abs(modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerDn'])):
                    modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerDn'] = float("{0:.4f}".format(diff))
                if (diff>0) and (abs(diff) > abs(modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerUp'])):
                    modelIndependenceUncert['AsimovData_' + obsName + '_genbin'+binTag]['uncerUp'] = float("{0:.4f}".format(diff))
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
    print '[Running fiducial XS computation - '+obsName+' - bin boundaries: ', observableBins, ']'
    ## Extract the efficiency factors for all reco/gen bins and final states
    if (runAllSteps or opt.effOnly):
        extractFiducialEfficiencies(obsName, observableBins, opt.MODELNAME)

    ## Prepare templates and uncertaincies for each reco bin and final states
    for obsBin in range(0,len(observableBins)-1):
        # produce the background templates
        if (runAllSteps or opt.templatesOnly):
            extractBackgroundTemplatesAndFractions(obsName, obsBin, observableBins)
        # extract the uncertainties
        if (runAllSteps or opt.uncertOnly):
            extractUncertainties(obsName, observableBins[obsBin], observableBins[obsBin+1])

    resultsXS = {}
    asimovDataModelName = "ggH_powheg15_JHUgen_125"
    produceDatacards(obsName, observableBins, asimovDataModelName)
    resultsXS = createAsimov(obsName, observableBins, asimovDataModelName, resultsXS)
    print "resultsXS: \n", resultsXS

    ## Extract the results
    modelNames = ['ggH_powheg15_JHUgen_125', 'VBF_powheg_125', 'WH_pythia_125', 'ZH_pythia_125', 'ttH_pythia_125']
#    modelNames = ['ttH_pythia_125']
    for modelName in modelNames:
      produceDatacards(obsName, observableBins, modelName)
      if (runAllSteps or opt.resultsOnly):
          resultsXS = extractResults(obsName, observableBins, modelName, resultsXS)
    print "resultsXS: \n", resultsXS
    # add model dependance uncertnaties
    modelIndependenceUncert = addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName)
    print "modelIndependenceUncert: \n", modelIndependenceUncert
    with open('resultsXS_'+obsName+'.py', 'w') as f:
        f.write('modelNames = '+json.dumps(modelNames)+';\n')
        f.write('asimovDataModelName = '+json.dumps(asimovDataModelName)+';\n')
        f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
        f.write('modelIndUncert = '+json.dumps(modelIndependenceUncert))

if __name__ == "__main__":
    runFiducialXS()
