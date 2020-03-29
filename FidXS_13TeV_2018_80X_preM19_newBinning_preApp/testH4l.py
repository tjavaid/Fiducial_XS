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
finalplotsOnly=True
resultsOnly=False
#useAsimov= True
redoEff = False
effOnly = False
redoTemplates = False
templatesOnly = False
floatPOIs = False
fixMH = False
modelName = 'SM'
inputDir = "/scratch/osg/dsperka/Run2/HZZ4l/SubmitArea_13TeV/rootfiles_MC_20151002/"
obsBinsDict = {'mass4l' : '"|105.0|140.0|"', 'pT4l' : '"|0|15|30|60|200|"', 'massZ2' : '"|12|20|28|35|60|"', 'rapidity4l' : '"|0|0.4|0.8|1.2|2.4|"', 'njets_reco_pt30_eta4p7' : '"|0|1|2|3|10|"',  'njets_reco_pt30_eta2p5' : '"|0|1|2|3|10|"', 'cosThetaStar' : '"|0.0|0.25|0.5|0.75|1.0|"', 'massZ1':'"|40.0|75.0|87.2|92.0|120.0|"', 'cosTheta1' : '"|0.0|0.25|0.5|0.75|1.0|"','cosTheta2' : '"|0.0|0.25|0.5|0.75|1.0|"', 'Phi' : '"|0.0|0.785398163|1.570796327|2.35619449|3.141592654|"', 'Phi1' : '"|0.0|0.785398163|1.570796327|2.35619449|3.141592654|"'} 


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

for obsName in obsNames:
    obsBins = obsBinsDict[ obsName ]
    cmd = 'python runHZZFiducialXS.py --dir='+inputDir+' --obsName='+obsName+' --obsBins='+obsBins+' --modelName='+modelName+ ' '
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
 #   if (useAsimov):
 #       cmd = cmd + ' --useAsimov '
    if (templatesOnly):
        cmd = cmd + ' --templatesOnly '
    if (floatPOIs):
        cmd = cmd + ' --floatPOIs '
    if (fixMH):
        cmd = cmd + ' --fixMH '


    cmd = cmd + ' &> testH4l_'+obsName
    if (resultsOnly):
        cmd = cmd + '_resultsOnly'
    if (finalplotsOnly):
        cmd = cmd + '_finalplotsOnly'
 #   if (useAsimov):
 #       cmd = cmd + '_useAsimov'
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
    if (fixMH):
        cmd = cmd + '_fixMH'
    cmd = cmd + '.log &'
    print cmd
    output=processCmd(cmd)
    print output

