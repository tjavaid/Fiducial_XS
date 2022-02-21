
#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.10.16
#-----------------------------------------------
import sys, os, pwd, commands
from subprocess import *
import optparse, shlex, re
import math
import time
from decimal import *
import json
from ROOT import *

from createXSworkspace import createXSworkspace
from sample_shortnames import *
from datapaths_full import *
from datetime import datetime
now = datetime.now() # current date and time
#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
date = now.strftime("%d%m%Y")
print "date is..................", date


# load XS-specific modules
#sys.path.append('./datacardInputs')
from higgs_xsbr_13TeV import *

### Define function for parsing options
def parseOptions():
    
    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-d', '--dir',      dest='SOURCEDIR',type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--asimovModelName',dest='ASIMOVMODEL',type='string',default='SM_125', help='Name of the Asimov Model')
    parser.add_option('',   '--asimovMass',dest='ASIMOVMASS',type='string',default='125.38', help='Asimov Mass')
    parser.add_option('',   '--modelNames',dest='MODELNAMES',type='string',default='SM_125',help='Names of models for unfolding, separated by | . Default is "SM_125"')
    parser.add_option('',   '--fixMass',  dest='FIXMASS',  type='string',default='125.38',   help='Fix mass, default is a string "125.38" or can be changed to another string, e.g."125.6" or "False"')
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"') 
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string') 
    parser.add_option('',   '--era',  dest='ERA',  type='string',default='',   help='Era to analyze, e.g. 2016, 2017, 2018 or Full ') 
    parser.add_option('',   '--fixFrac', action='store_true', dest='FIXFRAC', default=False, help='fix the fractions of 4e and 4mu when extracting the results, default is False')
    # Unblind option
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    # Calculate Systematic Uncertainties
    parser.add_option('',   '--calcSys', action='store_true', dest='SYS', default=False, help='Calculate Systematic Uncertainties (in addition to stat+sys)')
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    parser.add_option('',   '--hack', action='store_true', dest='HACK', default=False, help='Do hacks you normally would not do')
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

        
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    runAllSteps = not(opt.effOnly or opt.templatesOnly or opt.uncertOnly or opt.resultsOnly or opt.finalplotsOnly)
    if (opt.OBSBINS=='' and opt.OBSNAME!='inclusive'):
        parser.error('Bin boundaries not specified for differential measurement. Exiting...')
        sys.exit()

#    dirToExist = ['xs_125.0_2016','xs_125.0_2017','xs_125.0_2018']
    dirToExist = ['xs_125.0_2016','xs_125.0_2017','xs_125.0_2018','datacardInputs_2016','datacardInputs_2017','datacardInputs_2018']
    for dir in dirToExist:
        if not os.path.isdir(os.getcwd()+'/'+dir+'/'):
            cmd = 'mkdir '+dir; processCmd(cmd,1)
#            parser.error(os.getcwd()+'/'+dir+'/ is not a directory. Exiting...')
#            sys.exit()

### Define function for processing of os command
def processCmd(cmd, quiet = 0):
    output = '\n'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        print line, 
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))
    
    if (not quiet):
        print 'Output:\n   ['+output+'] \n'
    return output

def extractBackgroundTemplatesAndFractions(obsName, observableBins, years):
    global opt 
    for year in years:
        fractionBkg = {}; lambdajesdnBkg={}; lambdajesupBkg={}
        '''	
        if os.path.isfile('datacardInputs_'+year+'/inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName+'.py'):
            _temp = __import__('inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName, globals(), locals(), ['observableBins','fractionsBackground','lambdajesupBkg','lambdajesdnBkg'], -1) 
            if (hasattr(_temp,'observableBins') and _temp.observableBins == observableBins and not opt.redoTemplates):
                print '[Fractions already exist for the given binning. Skipping templates/shapes... ]'
                return
            if (hasattr(_temp,'fractionsBackground') and hasattr(_temp,'lambdajesupBkg') and hasattr(_temp,'lambdajesdnBkg')):
                fractionBkg = _temp.fractionsBackground
                lambdajesupBkg = _temp.lambdajesupBkg
                lambdajesdnBkg = _temp.lambdajesdnBkg
	'''
        print '[Preparing bkg shapes and fractions, for bins with boundaries ', observableBins
    # save/create/prepare directories and compile templates script
        currentDir = os.getcwd(); os.chdir('./templates_'+year+'/')
        print "current directory is:  ",os.getcwd()
        #cmd = 'rm main_fiducialXSTemplates; make'; processCmd(cmd)
        cmd = 'mkdir -p templatesXS/DTreeXS_'+opt.OBSNAME+'/13TeV/'; processCmd(cmd,1)

    # extract bkg templates and bin fractions
        sZZname2e2mu = 'ZZTo2e2mu_powheg'; sZZname4mu = 'ZZTo4mu_powheg'; sZZname4e = 'ZZTo4e_powheg'
        if (opt.doZ4l):
            sZZname2e2mu = 'ZZTo2e2mu_powheg_tchan'; sZZname4mu = 'ZZTo4mu_powheg_tchan'; sZZname4e = 'ZZTo4e_powheg_tchan'
	bkg_sample_tags = ['ggZZ_2e2mu_MCFM67', 'ggZZ_4e_MCFM67', 'ggZZ_4mu_MCFM67','ZX4l_CR', 'ZX4l_CR_4e', 'ZX4l_CR_4mu', 'ZX4l_CR_2e2mu', sZZname2e2mu, sZZname4e, sZZname4mu]
        bkg_samples_shorttags = {sZZname2e2mu:'qqZZ', sZZname4e:'qqZZ', sZZname4mu:'qqZZ', 'ggZZ_2e2mu_MCFM67':'ggZZ', 'ggZZ_4e_MCFM67':'ggZZ', 'ggZZ_4mu_MCFM67':'ggZZ', 'ZX4l_CR':'ZJetsCR', 'ZX4l_CR_4e':'ZJetsCR', "ZX4l_CR_4mu":'ZJetsCR', 'ZX4l_CR_2e2mu':'ZJetsCR'}
        bkg_samples_fStates = {sZZname2e2mu:'2e2mu', sZZname4e:'4e', sZZname4mu:'4mu', 'ggZZ_2e2mu_MCFM67':'2e2mu', 'ggZZ_4e_MCFM67':'4e', 'ggZZ_4mu_MCFM67':'4mu', 'ZX4l_CR':'AllChans', 'ZX4l_CR_4e':'4e', 'ZX4l_CR_4mu':'4mu', 'ZX4l_CR_2e2mu':'2e2mu'}
        for sample_tag in bkg_sample_tags:
            tmpObsName = obsName
            #tmpSrcDir = opt.SOURCEDIR
	    tmpSrcDir=datapaths[year]["MC"]
            #if (sample_tag=='ZX4l_CR'):
            if (sample_tag.startswith('ZX4l')):
		tmpSrcDir=datapaths[year]["data"]
	    print "year is: ",year
            print "sample short_tag is:  ", sample_tag
            print "sample directory tmpSrcDir is:  ",tmpSrcDir
            fitTypeZ4l = [['none','doRatio'],['doZ4l','doZ4l']][opt.doZ4l][opt.doRatio]
	    # currently different for eras, will generalize once UL ingredients are in place	    
            if year=="2018": cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples_2018[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 13TeV templatesXS DTreeXS ' + fitTypeZ4l+ ' 0' 
            elif year=="2017": cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples_2017[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 13TeV templatesXS DTreeXS ' + fitTypeZ4l+ ' 0' 
            else : cmd = './main_fiducialXSTemplates '+bkg_samples_shorttags[sample_tag]+' "'+tmpSrcDir+'/'+background_samples_2016[sample_tag]+'" '+bkg_samples_fStates[sample_tag]+' '+tmpObsName+' "'+opt.OBSBINS+'" "'+opt.OBSBINS+'" 13TeV templatesXS DTreeXS ' + fitTypeZ4l+ ' 0'

            print cmd 
            output = processCmd(cmd)
            print output
            tmp_fracs = output.split("[Bin fraction: ")
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
        with open('datacardInputs_'+year+'/inputs_bkg_'+{0:'',1:'z4l_'}[int(opt.doZ4l)]+obsName+'.py', 'w') as f:
            f.write('observableBins = '     +json.dumps(observableBins)+';\n')
            f.write('fractionsBackground = '+json.dumps(fractionBkg)   +';\n')
            f.write('lambdajesupBkg = '     +json.dumps(lambdajesupBkg)+';\n')
            f.write('lambdajesdnBkg = '     +json.dumps(lambdajesdnBkg)+';\n')


### Produce datacards for given obs and bin, for all final states
def produceDatacards(obsName, observableBins, modelName, physicalModel,years):

    print '[Producing workspace/datacards for obsName '+obsName+', bins '+str(observableBins)+']'

    fStates = ['2e2mu','4mu','4e']
    nBins = len(observableBins)
    actBins = nBins-1
    for year in years:
        sys.path.append('./datacardInputs_'+year+'/') # 
        for fState in fStates:


            if (not obsName.startswith("mass4l")):
                for obsBin in range(nBins-1):
                # first bool = cfactor second bool = add fake H               #
                    ndata = createXSworkspace(obsName,fState, nBins, obsBin, observableBins, False, True, modelName, physicalModel, year)
	#	    int actBins=nBins-1;
		    print "actual no. of bins! ", actBins
                    os.system("cp xs_125.0_"+str(actBins)+"bins_"+year+"/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
#                    if ((nBins-1)==8):
#                        print "8 Bins!"
#                        os.system("cp xs_125.0_8bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt xs_125.0/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
#                    if ((nBins-1)==7):
#                        print "7 Bins!"
#                        os.system("cp xs_125.0_7bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt xs_125.0/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
#                    if ((nBins-1)==6):
#                        print "6 Bins!"
#                        os.system("cp xs_125.0_6bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt xs_125.0/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
#
#                    if ((nBins-1)==5):
#                        print "5 Bins!"
#                        os.system("cp xs_125.0_5bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt xs_125.0/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
#
#                    if ((nBins-1)==4):
#                        print "4 Bins!"
#                        os.system("cp xs_125.0_4bins/hzz4l_"+fState+"S_13TeV_xs_bin"+str(obsBin)+".txt xs_125.0/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                    os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                    os.system("sed -i 's~_xs.Databin"+str(obsBin)+"~_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin"+str(obsBin)+"~g' xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")
                    if ("jet" in obsName):
                        os.system("sed -i 's~\#JES param~JES param~g' xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")

                    os.system("sed -i 's~0.0 0.2~0.0 0.2 [-1,1]~g' xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin"+str(obsBin)+"_"+physicalModel+".txt")


            else:
                ndata = createXSworkspace(obsName,fState, nBins, 0, observableBins, False, True, modelName, physicalModel, year)
                #if obsName=='mass4l': os.system("cp xs_125.0_1bin/hzz4l_"+fState+"S_13TeV_xs_inclusive_bin0.txt xs_125.0/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
                if obsName=='mass4l': os.system("cp xs_125.0_1bin_"+year+"/hzz4l_"+fState+"S_13TeV_xs_inclusive_bin0.txt xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
                if obsName=='mass4lREFIT': os.system("cp xs_125.0_1bin_"+year+"/hzz4l_"+fState+"S_13TeV_xs_inclusiveREFIT_bin0.txt xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
                os.system("sed -i 's~observation [0-9]*~observation "+str(ndata)+"~g' xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")
                os.system("sed -i 's~_xs.Databin0~_xs_"+modelName+"_"+obsName+"_"+physicalModel+".Databin0~g' xs_125.0_"+year+"/hzz4l_"+fState+"S_13TeV_xs_"+obsName+"_bin0_"+physicalModel+".txt")



### Create the asimov dataset and return fit results
#def createAsimov(obsName, observableBins, modelName, resultsXS, physicalModel):
def createAsimov(obsName, observableBins, modelName, resultsXS, physicalModel, years):
    print '[Producing/merging workspaces and datacards for obsName '+obsName+' using '+modelName+']'

    # Run combineCards and text2workspace
    nBins = len(observableBins)
    fStates = ['4e','4mu','2e2mu']

    cmd = 'combineCards.py '
    for year in years:
      for fState in fStates:  
        for obsBin in range(nBins-1):
          cmd += obsName+'_'+fState+'_bin'+str(obsBin)+'_'+year+'=xs_125.0_'+year+'/hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '  # ORIG, working
    cmd += ' > hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
    print cmd, '\n'
    
    #print cmd 
    processCmd(cmd,1)

    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')

    # text-to-workspace
    if (physicalModel=="v2"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root '
        print cmd
        processCmd(cmd)

    cmd = 'cp hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
    print cmd 
    processCmd(cmd,1)
       
    print "importing acc. factors from:    ",os.getcwd()   # 
    # import acc factors
    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc'], -1)
    acc = _temp.acc
    #print "acceptance dictionary is:   ", acc 
    # Run the Combine
    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName+' -M MultiDimFit  '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root -m '+opt.ASIMOVMASS+' --setParameters '
        for fState in fStates:
            nBins = len(observableBins)
            for obsBin in range(nBins-1):
                fidxs = 0
                fidxs += higgs_xs['ggH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)] # FIXME
                #fidxs += higgs_xs['ggH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['VBF_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['VBF_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['WH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['ZH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                fidxs += higgs_xs['ttH_'+opt.ASIMOVMASS]*higgs4l_br[opt.ASIMOVMASS+'_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                cmd = cmd + 'r'+fState+'Bin'+str(obsBin)+'='+str(fidxs)+','
        cmd =  cmd+ 'MH='+opt.ASIMOVMASS
        for fState in fStates:
            nBins = len(observableBins)
            for obsBin in range(nBins-1):
                cmd = cmd + ' -P r'+fState+'Bin'+str(obsBin)
        if (opt.FIXMASS=="False"):
            cmd = cmd + ' -P MH '
        else:
            cmd = cmd + ' --floatOtherPOIs=0'
        cmd = cmd +' -t -1 --saveWorkspace --saveToys --saveFitResult'
        #cmd += ' --X-rtd TMCSO_PseudoAsimov=1000000'
        #cmd += ' --freezeParameters r4muBin0,r4eBin0,r2e2muBin0'
        print cmd
        output = processCmd(cmd)
        processCmd('mv higgsCombine'+obsName+'.MultiDimFit.mH'+opt.ASIMOVMASS.rstrip('.0')+'.123456.root '+modelName+'_all_'+obsName+'_13TeV_Asimov_'+physicalModel+'.root',1)
        #cmd = cmd.replace(' --freezeParameters r4muBin0,r4eBin0,r2e2muBin0','')
        #cmd = cmd.replace(' --X-rtd TMCSO_PseudoAsimov=1000000','')
        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        print cmd
        output = processCmd(cmd)

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
        cmd = cmd + ' --freezeParameters '

        for year in years:
            cmd = cmd + 'CMS_fakeH_p1_1'+year+',CMS_fakeH_p1_2'+year+',CMS_fakeH_p1_3'+year+',CMS_fakeH_p3_1'+year+',CMS_fakeH_p3_2'+year+',CMS_fakeH_p3_3'+year+','
            cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year)+',CMS_hzz4e_Zjets_'+str(year)+',CMS_hzz4mu_Zjets_'+str(year)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year)+',CMS_zz4l_sigma_m_sig_'+str(year)+',CMS_zz4l_n_sig_1_'+str(year)+',CMS_zz4l_n_sig_2_'+str(year)+',CMS_zz4l_n_sig_3_'+str(year)+',CMS_zz4l_mean_e_sig_'+str(year)+',CMS_zz4l_mean_m_sig_'+str(year)+',CMS_zz4l_sigma_e_sig_'+str(year)+','
	if len(years)>1:
	    cmd = cmd + 'lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'		

        print cmd
        output = processCmd(cmd)
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
        print "Parsing Failed!!! Inserting dummy values!!! check log!!!"
        fXS = {'central':-1.0, 'uncerDn':0.0, 'uncerUp':0.0}
        return fXS

### Extract the results and do plotting
#def extractResults(obsName, observableBins, modelName, physicalModel, asimovModelName, asimovPhysicalModel, resultsXS):
def extractResults(obsName, observableBins, modelName, physicalModel, asimovModelName, asimovPhysicalModel, resultsXS, years):
    # Run combineCards and text2workspace
    print '[Producing/merging workspaces and datacards for obsName '+obsName+']'

    # Run combineCards and text2workspace
    nBins = len(observableBins)
    fStates = ['4e','4mu','2e2mu']

    cmd = 'combineCards.py '
    for year in years:
      for fState in fStates:  
        for obsBin in range(nBins-1):
          cmd += obsName+'_'+fState+'_bin'+str(obsBin)+'_'+year+'=xs_125.0_'+year+'/hzz4l_'+fState+'S_13TeV_xs_'+obsName+'_bin'+str(obsBin)+'_'+physicalModel+'.txt '
    cmd += ' > hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt'
#    processCmd(cmd,1)
    print cmd 
    processCmd(cmd,1)

    if (not opt.LUMISCALE=="1.0"):
        os.system('echo "    " >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "lumiscale rateParam * * '+opt.LUMISCALE+'" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')
        os.system('echo "nuisance edit freeze lumiscale" >> hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt')

    if (physicalModel=="v2"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial_v2:differentialFiducialV2 --PO higgsMassRange=115,135 --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        print cmd
        processCmd(cmd)
    if (physicalModel=="v3"):
        cmd = 'text2workspace.py hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.txt -P HiggsAnalysis.CombinedLimit.HZZ4L_Fiducial:differentialFiducialV3 --PO higgsMassRange=115,135 --PO nBin='+str(nBins-1)+' -o hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
        print cmd
        processCmd(cmd)
                       
    cmd = 'cp hzz4l_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root'
    print cmd
    processCmd(cmd,1)

    cmd = 'root -l -b -q "addToyDataset.C(\\"'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'.root\\",\\"'+asimovModelName+'_all_'+obsName+'_13TeV_Asimov_'+asimovPhysicalModel+'.root\\",\\"toy_asimov\\",\\"'+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root\\")"'
    print cmd
    processCmd(cmd)

    # Run the Combine
    if (physicalModel=="v3"):
        if (not opt.FIXFRAC):
            if (opt.FIXMASS=="False"):
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m 125.0 -D toy_asimov '
            else:
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m '+opt.FIXMASS+' -D toy_asimov --setParameters MH='+opt.FIXMASS  
            # you can add fractions to the POIs if you want the uncertainties on frac4e, frac4mu
            for bin in range(nBins-1):
                cmd = cmd + ' -P SigmaBin'+str(bin)
                #cmd = cmd + ' -P SigmaBin'+str(bin)+' -P K1Bin'+str(bin)+' -P K2Bin'+str(bin)
            if (opt.FIXMASS=="False"):
                cmd = cmd + ' -P MH'
            cmd = cmd + ' --floatOtherPOIs=1 --saveWorkspace --saveFitResult '
            if (not opt.FIXMASS=="False"):
                cmd = cmd + ' --setParameterRanges MH='+opt.FIXMASS+','+opt.FIXMASS#+'001'            
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5'): cmd = cmd +':SigmaBin0=0.0,4.0:SigmaBin2=0.0,3.0:SigmaBin3=0.0,1.0:SigmaBin4=0.0,2.0'               #+'001'          tahir  
                if (obsName=='rapidity4l'): cmd = cmd +':SigmaBin0=0.0,5.0:SigmaBin1=0.0,5.0:SigmaBin2=0.0,5.0:SigmaBin3=0.0,5.0:SigmaBin4=0.0,5.0:SigmaBin5=0.0,5.0'               #+'001'          tahir  
                if (obsName=='pT4l' or obsName=='massZ2'): cmd = cmd +':SigmaBin6=0.0,2.0:SigmaBin7=0.0,2.0:SigmaBin8=0.0,2.0' #cmd = cmd.replace('0.0,3.0','0.0,2.0')
                if (obsName=='cosThetaStar'): cmd = cmd +':SigmaBin1=0.0,4.0' #cmd = cmd.replace('0.0,3.0','0.0,2.0')
                if (obsName=='massZ1'): cmd = cmd +':SigmaBin0=0.0,2.0:SigmaBin1=0.0,3.0' #cmd = cmd.replace('0.0,3.0	','0.0,2.0')
                if (obsName=='Phi'): cmd = cmd +':SigmaBin1=0.0,4.0:SigmaBin2=0.0,4.0:SigmaBin3=0.0,3.0:SigmaBin4=0.0,4.0:SigmaBin7=0.0,4.0'               #+'001'          tahir  
                #cmd = cmd + ' --freezeParameters MH '
            if (opt.UNBLIND):
                #cmd = cmd.replace('_exp','')
                cmd = cmd.replace('-D toy_asimov',' ')
            print cmd 
            output=processCmd(cmd)
            if (opt.FIXMASS=="False"):
                processCmd('cp higgsCombine'+obsName+'.MultiDimFit.mH125.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
            else:
                processCmd('cp higgsCombine'+obsName+'.MultiDimFit.mH'+opt.FIXMASS.replace('.0.root','.root')+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
#	    if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5'): cmd = cmd +':SigmaBin2=0.0,1.0:SigmaBin4=0.0,1.0'  # tahir
            cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
            print cmd
            output=processCmd(cmd)

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
                    fidxs_sm += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)] # FIXME
                    #fidxs_sm += higgs_xs['ggH_125.0']*higgs4l_br['125.0_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    #fidxs_sm += acc['ggH_HRes_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['VBF_125.0']*higgs4l_br['125.0_'+fState]*acc['VBF_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['WH_125.0']*higgs4l_br['125.0_'+fState]*acc['WH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['ZH_125.0']*higgs4l_br['125.0_'+fState]*acc['ZH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs_sm += higgs_xs['ttH_125.0']*higgs4l_br['125.0_'+fState]*acc['ttH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
                    fidxs = 0
                    if (not opt.FIXMASS=="False"):
                        fidxs += higgs_xs['ggH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125.38_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)] # FIXME
                        #fidxs += higgs_xs['ggH_'+opt.FIXMASS]*higgs4l_br[opt.FIXMASS+'_'+fState]*acc['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(obsBin)]
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
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m 125.0 -D toy_asimov  --setParameters '
            else:
                cmd =  'combine -n '+obsName+' -M MultiDimFit '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -m '+opt.FIXMASS+' -D toy_asimov --setParameters MH='+opt.FIXMASS+','
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

            cmd = cmd + ' --saveWorkspace --saveFitResult --setParameterRanges '
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
            print cmd
            output=processCmd(cmd)

            if (opt.FIXMASS=="False"):
                processCmd('cp higgsCombine'+obsName+'.MultiDimFit.mH125.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
            else:
                processCmd('cp higgsCombine'+obsName+'.MultiDimFit.mH'+opt.FIXMASS.rstrip('.0')+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
            cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
            print cmd
            output=processCmd(cmd)


    if (physicalModel=="v2"):
        cmd =  'combine -n '+obsName+' -M MultiDimFit '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root -D toy_asimov --saveWorkspace'
        if (not opt.FIXMASS=="False"):
            cmd = cmd + ' -m '+opt.FIXMASS+' --setParameterRanges MH='+opt.FIXMASS+','+opt.FIXMASS#+'001'
	    #if (obsName=='mass4l'): cmd=cmd + ':r4eBin0=0.0,5.0'   # tahir 
	   # if (obsName=='mass4l'): cmd=cmd + ':r4eBin0=0.0,3.0'   # tahir 
	    if (obsName=='mass4l'): cmd=cmd + ':r4eBin0=0.0,3.0:r2e2muBin0=0.0,3.0'   # tahir 
        else:
            cmd = cmd + ' -m 125.0'
        if (opt.UNBLIND): 
            #cmd = cmd.replace('_exp','')
            cmd = cmd.replace('-D toy_asimov',' ')
        print cmd
        output=processCmd(cmd)
        if (opt.FIXMASS=="False"):
            processCmd('cp higgsCombine'+obsName+'.MultiDimFit.mH125.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
        else:
            processCmd('cp higgsCombine'+obsName+'.MultiDimFit.mH'+opt.FIXMASS.rstrip('.0')+'.root '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root',1)
	#if (obsName=='njets_pt30_eta2p5'): cmd = cmd + ':SigmaBin2=0.0,1.0:SigmaBin3=0.0,1.0:SigmaBin4=0.0,1.0'    # tahir
	



        cmd = cmd + ' --algo=singles --cl=0.68 --robustFit=1'
        print cmd
        output=processCmd(cmd)
                                                                                            
    # parse the results for all the bins
    for obsBin in range(len(observableBins)-1):
        if (physicalModel=="v3"):
            resultsXS[modelName+'_'+obsName+'_genbin'+str(obsBin)] = parseXSResults(output,'SigmaBin'+str(obsBin)+' :')
        elif (physicalModel=="v2"):
            for fState in fStates:
                resultsXS[modelName+'_'+obsName+'_'+fState+'_genbin'+str(obsBin)] = parseXSResults(output, 'r'+fState+'Bin'+str(obsBin)+' :')

    # load best fit snapshot and run combine with no systematics for stat only uncertainty
    if (opt.SYS):
        cmd = cmd.replace(modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_exp.root','-d '+modelName+'_all_13TeV_xs_'+obsName+'_bin_'+physicalModel+'_result.root -w w --snapshotName "MultiDimFit"')

        cmd = cmd + ' --freezeParameters '
        for year in years:
            cmd = cmd + 'CMS_fakeH_p1_1'+year+',CMS_fakeH_p1_2'+year+',CMS_fakeH_p1_3'+year+',CMS_fakeH_p3_1'+year+',CMS_fakeH_p3_2'+year+',CMS_fakeH_p3_3'+year+','
            cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year)+',CMS_hzz4e_Zjets_'+str(year)+',CMS_hzz4mu_Zjets_'+str(year)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year)+',CMS_zz4l_sigma_m_sig_'+str(year)+',CMS_zz4l_n_sig_1_'+str(year)+',CMS_zz4l_n_sig_2_'+str(year)+',CMS_zz4l_n_sig_3_'+str(year)+',CMS_zz4l_mean_e_sig_'+str(year)+',CMS_zz4l_mean_m_sig_'+str(year)+',CMS_zz4l_sigma_e_sig_'+str(year)+','

        if len(years)>1:
            cmd = cmd + 'lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'


        print cmd
        output = processCmd(cmd)
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

        print modelIndependenceUncert
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
   
    if (opt.ERA == '2016'): years = ['2016']
    if (opt.ERA == '2017'): years = ['2017']
    if (opt.ERA == '2018'): years = ['2018']
    if (opt.ERA == 'Full'): years = ['2016','2017','2018']

    # save working dir
    jcpDir = os.getcwd()
    
    # prepare the set of bin boundaries to run over, only 1 bin in case of the inclusive measurement
    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']

    ### Run for the given observable
    obsName = opt.OBSNAME

    print '[Running fiducial XS computation - '+obsName+' - bin boundaries: ', observableBins, ']'
    
    #runAllSteps=True
    ## Prepare templates for all reco bins and final states
    #if (runAllSteps or opt.templatesOnly):
    if ( opt.templatesOnly):
        #extractBackgroundTemplatesAndFractions(obsName, observableBins)
        extractBackgroundTemplatesAndFractions(obsName, observableBins, years)

    ## Create the asimov dataset
    if (runAllSteps):
        resultsXS = {}
	for year in years:
	    cmd = 'python addConstrainedModel.py -l -q -b --obsName="'+opt.OBSNAME+'" --obsBins="'+opt.OBSBINS+'" --year="'+year+'"'
            print "for year:    ", year
            print cmd
            output = processCmd(cmd)
            print output

        asimovDataModelName = "SM_125"    
        asimovPhysicalModel = "v2"
	produceDatacards(obsName, observableBins, asimovDataModelName, asimovPhysicalModel,years)

        #resultsXS = createAsimov(obsName, observableBins, asimovDataModelName, resultsXS, asimovPhysicalModel)
        resultsXS = createAsimov(obsName, observableBins, asimovDataModelName, resultsXS, asimovPhysicalModel, years)
        print "resultsXS: \n", resultsXS
        
        # plot the asimov predictions for data, signal, and backround in differential bins
        if (not obsName.startswith("mass4l")):
            cmd = 'python plotDifferentialBins.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --era="'+opt.ERA+'"'
            print cmd
            if (opt.UNBLIND): cmd = cmd + ' --unblind'
            output = processCmd(cmd)
            print output
    
    ## Extract the results
    # use constrained SM 
    modelNames = ['SM_125']#,'SMup_125','SMdn_125']#,'VBF_powheg_JHUgen_125']    
    # do all models
    #if (not 'jet' in obsName):
    #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125', 'ttH_powheg_JHUgen_125']
    #else:
    #    modelNames = ['SM_125','ggH_powheg_JHUgen_125', 'VBF_powheg_JHUgen_125', 'WH_powheg_JHUgen_125', 'ZH_powheg_JHUgen_125']

    # just ggH
    #modelNames = ['ggH_powheg_JHUgen_125']

    # Testing
    #print opt.MODELNAMES
    #modelNames = opt.MODELNAMES
    #modelNames = modelNames.split('|')
    print "modelNames",modelNames
    
#    if (obsName.startswith("mass4l")): physicalModels = ["v2","v3"]
    if (obsName=="mass4l"): physicalModels = ["v2","v3"]
    else: physicalModels = ["v3"]

    if (runAllSteps or opt.resultsOnly):
        for physicalModel in physicalModels:
	    print "physicalModel is:      ",physicalModel
            for modelName in modelNames:
	#	for year in years:
            #produceDatacards(obsName, observableBins, asimovDataModelName, asimovPhysicalModel,"2018")
		produceDatacards(obsName, observableBins, modelName, physicalModel,years)
                resultsXS = extractResults(obsName, observableBins, modelName, physicalModel, asimovDataModelName, asimovPhysicalModel, resultsXS, years)
                print "resultsXS: \n", resultsXS
                # plot the fit results
                if (not obsName.startswith("mass4l")):
                    cmd = 'python plotAsimov_simultaneous.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'"'# +' --lumiscale=str(opt.LUMISCALE)'
                    if (opt.UNBLIND): cmd = cmd + ' --unblind'
                    print cmd
                    output = processCmd(cmd)
#                    print output                                                
                elif (physicalModel=="v2"):
                    #cmd = 'python plotAsimov_inclusive.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'"' #+' --lumiscale=str(opt.LUMISCALE)'            
                    cmd = 'python plotAsimov_simultaneous.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --asimovModel="'+asimovDataModelName+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'"' #+' --lumiscale=str(opt.LUMISCALE)'            
                    if (opt.UNBLIND): cmd = cmd + ' --unblind'
                    print cmd
                    output = processCmd(cmd)
                    print output
        
            ## Calculate model dependance uncertainties
            modelIndependenceUncert = addModelIndependenceUncert(obsName, observableBins, resultsXS, asimovDataModelName,physicalModel)
            print "modelIndependenceUncert: \n", modelIndependenceUncert
            if (opt.FIXFRAC): floatfix = '_fixfrac'
            else: floatfix = ''
            with open('resultsXS_'+obsName+'_'+physicalModel+floatfix+'.py', 'w') as f:
                f.write('modelNames = '+json.dumps(modelNames)+';\n')
                f.write('asimovDataModelName = '+json.dumps(asimovDataModelName)+';\n')
                f.write('resultsXS = '+json.dumps(resultsXS)+';\n')
                f.write('modelIndUncert = '+json.dumps(modelIndependenceUncert))
        
    # Make final differential plots
    if (runAllSteps or opt.finalplotsOnly):

        if (opt.UNBLIND):
            cmd = "sed -i 's~-D toy_asimov~-D data_obs~g' doLScan*.sh"
            output = processCmd(cmd)
        else:
            cmd = "sed -i 's~-D data_obs~-D toy_asimov~g' doLScan*.sh"
            output = processCmd(cmd)

        if (obsName=="mass4l"):
            #cmd = './doLScan_mass4l.sh'
            cmd = './doLScan_mass4l.sh '+opt.ERA
            output = processCmd(cmd)
        else:
            for obsBin in range(0,len(observableBins)-1):
                cmd = "combine -n "+obsName+"_SigmaBin"+str(obsBin)+" -M MultiDimFit -d SM_125_all_13TeV_xs_"+obsName+"_bin_"+physicalModel+"_exp.root -m 125.38 -D toy_asimov --setParameters MH=125.38 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin"+str(obsBin)+"=0.0,3.0 --redefineSignalPOIs SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4 "
                if (opt.UNBLIND): cmd = cmd.replace("-D toy_asimov","-D data_obs")
#tahir
                if ((obsName=='pT4l' or obsName=='massZ2') and (str(obsBin)=='6' or str(obsBin)=='7' or str(obsBin)=='8')): cmd = cmd.replace('0.0,3.0','0.0,2.0')
                if (obsName=='Phi' and (str(obsBin)=='1' or str(obsBin)=='2' or str(obsBin)=='3' or str(obsBin)=='4' or str(obsBin)=='7')): cmd = cmd.replace('0.0,3.0','0.0,4.0')
                if (obsName=='Phi1' and str(obsBin)=='3'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and (str(obsBin)=='0') or str(obsBin)=='2' or str(obsBin)=='3' or str(obsBin)=='4'): cmd = cmd.replace('0.0,3.0','0.0,4.0')
                if (obsName=='rapidity4l' and (str(obsBin)=='0' or str(obsBin)=='1' or str(obsBin)=='2' or str(obsBin)=='3' or str(obsBin)=='4' or str(obsBin)=='5')): cmd = cmd.replace('0.0,3.0','0.0,5.0')
                if (obsName=='cosThetaStar' and str(obsBin)=='1'): cmd = cmd.replace('0.0,3.0','0.0,4.0')



                print cmd
                output = processCmd(cmd)

                cmd = "combine -n "+obsName+"_SigmaBin"+str(obsBin)+"_NoSys -M MultiDimFit -d SM_125_all_13TeV_xs_"+obsName+"_bin_"+physicalModel+"_result.root -w w --snapshotName \"MultiDimFit\" -m 125.38 -D toy_asimov --setParameters MH=125.38 -P SigmaBin"+str(obsBin)+" --floatOtherPOIs=1 --saveWorkspace --setParameterRanges MH=125.38,125.38:SigmaBin"+str(obsBin)+"=0.0,3.0 --redefineSignalPOI SigmaBin"+str(obsBin)+" --algo=grid --points=50 --autoRange 4" # --freezeParameters CMS_fakeH_p1_12016,CMS_fakeH_p1_22016,CMS_fakeH_p1_32016,CMS_fakeH_p3_12016,CMS_fakeH_p3_22016,CMS_fakeH_p3_32016,CMS_fakeH_p1_12017,CMS_fakeH_p1_22017,CMS_fakeH_p1_32017,CMS_fakeH_p3_12017,CMS_fakeH_p3_22017,CMS_fakeH_p3_32017,CMS_fakeH_p1_12018,CMS_fakeH_p1_22018,CMS_fakeH_p1_32018,CMS_fakeH_p3_12018,CMS_fakeH_p3_22018,CMS_fakeH_p3_32018 "

	        cmd = cmd + ' --freezeParameters '
                for year in years:
                    cmd = cmd + 'CMS_fakeH_p1_1'+year+',CMS_fakeH_p1_2'+year+',CMS_fakeH_p1_3'+year+',CMS_fakeH_p3_1'+year+',CMS_fakeH_p3_2'+year+',CMS_fakeH_p3_3'+year+','

	            cmd += 'CMS_eff_e,CMS_eff_m,CMS_hzz2e2mu_Zjets_'+str(year)+',CMS_hzz4e_Zjets_'+str(year)+',CMS_hzz4mu_Zjets_'+str(year)+',QCDscale_VV,QCDscale_ggVV,kfactor_ggzz,lumi_13TeV_'+str(year)+'_uncorrelated,norm_fakeH,pdf_gg,pdf_qqbar,CMS_zz4l_sigma_e_sig_'+str(year)+',CMS_zz4l_sigma_m_sig_'+str(year)+',CMS_zz4l_n_sig_1_'+str(year)+',CMS_zz4l_n_sig_2_'+str(year)+',CMS_zz4l_n_sig_3_'+str(year)+',CMS_zz4l_mean_e_sig_'+str(year)+',CMS_zz4l_mean_m_sig_'+str(year)+',CMS_zz4l_sigma_e_sig_'+str(year)+','
        	if len(years)>1:
	            cmd = cmd + 'lumi_13TeV_correlated_16_17_18,lumi_13TeV_correlated_17_18'


                if (opt.UNBLIND): cmd = cmd.replace("-D toy_asimov","-D data_obs")
#tahir
                if (obsName=='mass4l' and str(obsBin)=='0'): cmd = cmd.replace('0.0,3.0','0.0,5.0')
                if (obsName=='Phi' and str(obsBin)=='3'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='massZ1' and str(obsBin)=='1'): cmd = cmd.replace('0.0,3.0','0.0,2.0')

                if ((obsName=='pT4l' or obsName=='massZ2') and (str(obsBin)=='6' or str(obsBin)=='7' or str(obsBin)=='8')): cmd = cmd.replace('0.0,3.0','0.0,2.0')
                if (obsName=='Phi' and (str(obsBin)=='1' or str(obsBin)=='2' or str(obsBin)=='3' or str(obsBin)=='4' or str(obsBin)=='7')): cmd = cmd.replace('0.0,3.0','0.0,4.0')
                if (obsName=='Phi1' and str(obsBin)=='3'): cmd = cmd.replace('0.0,3.0','0.0,1.0')
                if (obsName=='njets_pt30_eta2p5' or obsName=='pt_leadingjet_pt30_eta2p5' and (str(obsBin)=='0') or str(obsBin)=='2' or str(obsBin)=='3' or str(obsBin)=='4'): cmd = cmd.replace('0.0,3.0','0.0,4.0')
                if (obsName=='rapidity4l' and (str(obsBin)=='0' or str(obsBin)=='1' or str(obsBin)=='2' or str(obsBin)=='3' or str(obsBin)=='4' or str(obsBin)=='5')): cmd = cmd.replace('0.0,3.0','0.0,5.0')
                if (obsName=='cosThetaStar' and str(obsBin)=='1'): cmd = cmd.replace('0.0,3.0','0.0,4.0')

                print cmd
                output = processCmd(cmd)


        #if (obsName=="pT4l"):
        #    cmd = './doLScan_pT4l.sh'
        #if (obsName=="njets_pt30_eta4p7"):
        #    cmd = './doLScan_njets.sh'
        #if (obsName=="njets_pt30_eta2p5"):
        #    cmd = './doLScan_njets2p5.sh'
        #if (obsName=="pt_leadingjet_pt30_eta4p7"):
        #    cmd = './doLScan_ptjet1.sh'
        #if (obsName=="pt_leadingjet_pt30_eta2p5"):
        #    cmd = './doLScan_ptjet12p5.sh'
        #if (obsName=="rapidity4l"):
        #    cmd = './doLScan_rapidity4l.sh' 
        #output = processCmd(cmd)
        
        cmd = 'python plotLHScans.py -l -q -b --era="'+opt.ERA+'" --obsName='+obsName
	print cmd
        output = processCmd(cmd)
	ext1=''
        for modelName in modelNames:
            if (not opt.FIXMASS=="False"):
                if (not opt.LUMISCALE=="1.0"):
                    cmd = 'python producePlots'+ext1+'.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'" --theoryMass="'+opt.FIXMASS+'"'+' --lumiscale=str(opt.LUMISCALE)'
                    
                else:
                    cmd = 'python producePlots'+ext1+'.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'" --theoryMass="'+opt.FIXMASS+'"'
            else:
                if (not opt.LUMISCALE=="1.0"):
                    cmd = 'python producePlots'+ext1+'.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'" --theoryMass="125.0"'+' --lumiscale=str(opt.LUMISCALE)'
                else:
                    cmd = 'python producePlots'+ext1+'.py -l -q -b --obsName="'+obsName+'" --obsBins="'+opt.OBSBINS+'" --unfoldModel="'+modelName+'" --era="'+opt.ERA+'" --theoryMass="125.0"'


            if (opt.FIXFRAC): cmd = cmd + ' --fixFrac'
            if (opt.UNBLIND): cmd = cmd + ' --unblind'
            print cmd   
            output = processCmd(cmd)  
            print output  
            cmd = cmd + ' --setLog'
            print cmd   
            output = processCmd(cmd)  
            print output  

        
if __name__ == "__main__":   
    runFiducialXS()  
print "all modules successfully compiled"
