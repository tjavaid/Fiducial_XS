#!/usr/bin/python
import sys, os, pwd, commands
from subprocess import *
import optparse, shlex, re
import math
import time
from decimal import *


#obsNames = ['rapidity4l','cosThetaStar','massZ2']
#obsNames = ['massZ2']
#obsNames = ['rapidity4l','cosThetaStar']
obsNames = ['mass4l']
#obsNames = ['pT4l']
#obsNames = ['njets_reco_pt30_eta4p7']
#obsNames = ['njets_reco_pt30_eta2p5']
#obsNames = ['njets_reco_pt30_eta2p5','njets_reco_pt30_eta4p7']
#obsNames = ['massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7', 'cosThetaStar']
#obsNames = ['pT4l', 'massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7']
#obsNames = ['pT4l', 'massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7', 'njets_reco_pt30_eta2p5','cosThetaStar']
#obsNames = ['massZ1']
#obsNames = ['cosTheta1']
#obsNames = ['massZ1', 'cosTheta1', 'cosTheta2', 'Phi', 'Phi1']
#obsNames = ['pT4l', 'massZ2', 'rapidity4l', 'njets_reco_pt30_eta4p7', 'njets_reco_pt30_eta2p5','cosThetaStar','massZ1', 'cosTheta1', 'cosTheta2', 'Phi', 'Phi1']
#obsNames = ['pT4l', 'massZ2', 'rapidity4l', 'cosThetaStar','cosTheta1', 'cosTheta2', 'Phi', 'Phi1']

tag="_tchanCorr"

finalplotsOnly=False
resultsOnly=True
useAsimov= True
redoEff = True
effOnly = False
redoTemplates = True
templatesOnly = False
floatPOIs = True
fixMZ = True
inputDir = "/scratch/osghpc/dsperka/Analyzer/SubmitArea_8TeV/Trees_HZZFiducialSamples_Nov22/"
modelName = 'SMZ4l'
obsBinsDict = {'mass4l' : '"|50|105|"', 'pT4l' : '"|0|15|30|60|200|"', 'massZ2' : '"|12|20|28|35|60|"', 'rapidity4l' : '"|0|0.4|0.8|1.2|2.4|"', 'njets_reco_pt30_eta4p7' : '"|0|1|2|3|10|"',  'njets_reco_pt30_eta2p5' : '"|0|1|2|3|10|"', 'cosThetaStar' : '"|0.0|0.25|0.5|0.75|1.0|"', 'massZ1':'"|40.0|75.0|87.2|92.0|120.0|"', 'cosTheta1' : '"|0.0|0.25|0.5|0.75|1.0|"','cosTheta2' : '"|0.0|0.25|0.5|0.75|1.0|"', 'Phi' : '"|0.0|0.785398163|1.570796327|2.35619449|3.141592654|"', 'Phi1' : '"|0.0|0.785398163|1.570796327|2.35619449|3.141592654|"'} 


### Define function for processing of os command
def processCmd(cmd, quiet = 0):
    #print cmd
    #status, output = commands.getstatusoutput(cmd)
    #output = subprocess.check_output(cmd, shell=True)

    output = '\n'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT,bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
        print line,
    p.stdout.close()
    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))

    #if (status !=0 and not quiet):
    #    print 'Error in processing command:\n   ['+cmd+']'
    #    print 'Output:\n   ['+output+'] \n'
    if (not quiet):
        print 'Output:\n   ['+output+'] \n'
    return output

for obsName in obsNames:
    obsBins = obsBinsDict[ obsName ]
    cmd = 'python runHZZFiducialXS.py --dir='+inputDir+' --modelName='+modelName+' --obsName='+obsName+' --obsBins='+obsBins+' '
    if (resultsOnly):
        cmd = cmd + ' --resultsOnly'
    if (finalplotsOnly):
        cmd = cmd + ' --finalplotsOnly'
    if (redoEff):
        cmd = cmd + ' --redoEff '
    if (effOnly):
        cmd = cmd + ' --effOnly '
    if (redoTemplates): 
        cmd = cmd + ' --redoTemplates '
    if (useAsimov):
        cmd = cmd + ' --useAsimov '
    if (templatesOnly):
        cmd = cmd + ' --templatesOnly '
    if (floatPOIs):
        cmd = cmd + ' --floatPOIs '
    if (fixMZ):
        cmd = cmd + ' --fixMZ '


    cmd = cmd + ' &> testz4l_'+modelName+'_'+obsName
    if (resultsOnly):
        cmd = cmd + '_resultsOnly'
    if (finalplotsOnly):
        cmd = cmd + '_finalplotsOnly'
    if (useAsimov):
        cmd = cmd + '_useAsimov'
    if (redoEff):
        cmd = cmd + '_redoEff'
    if (effOnly):
        cmd = cmd + '_effOnly'
    if (redoTemplates):
        cmd = cmd + '_redoTemplates'
    if (templatesOnly):
        cmd = cmd + '_templatesOnly'
    if (floatPOIs):
        cmd = cmd + '_floatPOIs'
    if (fixMZ):
        cmd = cmd + '_fixMZ'
    cmd = cmd + tag + '.log &'
    print cmd
    #output=processCmd(cmd)
    #print output






