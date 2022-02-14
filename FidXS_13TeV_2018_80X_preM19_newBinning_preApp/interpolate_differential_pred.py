import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
import numpy as np
#import matplotlib.pyplot as plt
from scipy import interpolate
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--year',  dest='YEAR',  type='string',default='2018',   help='Era to analyze, e.g. 2016, 2017, 2018 or Full ')
    global opt, args
    (opt, args) = parser.parse_args()

#
#def f(x):
def f(x,n,obsName):
#def f(mass, channel):
    #obsName='mass4l'
   # channel='2e2mu'
    acceptance={}
#    pdfunc={}
    pdf_uncerUp={}
    pdf_uncerDn={}
    qcd_uncerUp={}
    qcd_uncerDn={}
    qcdunc={}
    #_temp = __import__('accUnc_'+obsName, globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
    #_temp = __import__('accUnc_'+obsName'_2018', globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
    _temp = __import__('accUnc_'+obsName+'_'+opt.YEAR, globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
    acc_ggH_powheg = _temp.acc
    print "acc_ggH_powheg", acc_ggH_powheg
    pdfunc_ggH_powheg = _temp.pdfUncert
    qcdunc_ggH_powheg = _temp.qcdUncert
# ggH_powheg_JHUgen_126_2e2mu_'+obsName+'_genbin0
#from scipy import interpolate
#
#def f(x):
    #x_points = [ 0, 1, 2, 3, 4, 5]
    x_points = [124, 125, 126]
    #x_points = [124, 125, 126,130]
    channels=['4mu','2e2mu','4e']

    if obsName=='mass4l': channels=['4mu','2e2mu','4e','4l']
    #y_points = [12,14,22,39,58,77]
    #y_points = [acc_ggH_powheg['ggH_powheg_JHUgen_124_2e2mu_'+obsName+'_genbin0'],acc_ggH_powheg['ggH_powheg_JHUgen_125_2e2mu_'+obsName+'_genbin0'],acc_ggH_powheg['ggH_powheg_JHUgen_126_2e2mu_'+obsName+'_genbin0']]   #  [12,14,22,39,58,77]
    for channel in channels:
	for obsBin in range(0,n-1):
        #thread='ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin0'
            thread0p='ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            thread='ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            thread2='ggH_NNLOPS_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            thread0n='ggH_NNLOPS_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            print "thread is       ", thread
            acceptance[thread]=0.0
            pdf_uncerUp[thread]=0.0
            pdf_uncerDn[thread]=0.0
            qcd_uncerUp[thread]=0.0
            qcd_uncerDn[thread]=0.0
            #acc_points = [acc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_130_'+channel+'_'+obsName+'_genbin'+str(obsBin)]]   #  [12,14,22,39,58,77]
            acc_points = [acc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]]   #  [12,14,22,39,58,77]
	    #pdf_points_uncerUp = [pdfunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_130_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp']]   #  [12,14,22,39,58,77]
	    pdf_points_uncerUp = [pdfunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp']]   #  [12,14,22,39,58,77]
	    #pdf_points_uncerDn = [pdfunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_130_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn']] 
	    pdf_points_uncerDn = [pdfunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn']] 
            #qcd_points_uncerUp = [qcdunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_130_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp']]   #  [12,14,22,39,58,77]
            qcd_points_uncerUp = [qcdunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp']]   #  [12,14,22,39,58,77]
            #qcd_points_uncerDn = [qcdunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_130_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn']]   #  [12,14,22,39,58,77]
            qcd_points_uncerDn = [qcdunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn']]   #  [12,14,22,39,58,77]
            print "obsName is  ..  ", obsName
            print "channel is ..  ", channel
            print "acc_points are,,,,,,,,,,,,,,," ,  acc_points
            print "pdf_points_uncerUp are,,,,,,,,,,,,,,," ,  pdf_points_uncerUp
            print "pdf_points_uncerDn are,,,,,,,,,,,,,,," ,  pdf_points_uncerDn
            print "qcd_points_uncerUp are,,,,,,,,,,,,,,," ,  qcd_points_uncerUp
            print "qcd_points_uncerDn are,,,,,,,,,,,,,,," ,  qcd_points_uncerDn


    #tck = interpolate.splrep(x_points, y_points)
            tck1 = interpolate.splrep(x_points, acc_points, k=2)
            tck2 = interpolate.splrep(x_points, pdf_points_uncerUp, k=2)
            tck3 = interpolate.splrep(x_points, pdf_points_uncerDn, k=2)
            tck4 = interpolate.splrep(x_points, qcd_points_uncerUp, k=2)
            tck5 = interpolate.splrep(x_points, qcd_points_uncerDn, k=2)
        #thread='ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
        #print 'the thread is .. ', thread
    #with open('accUnc_mass4l.py', 'w') as f:
        #acceptance[thread]=interpolate.splev(x, tck)
            acceptance[thread]=float(interpolate.splev(x, tck1))
            pdf_uncerUp[thread]=float(interpolate.splev(x, tck2))
            pdf_uncerDn[thread]=float(interpolate.splev(x, tck3))
            qcd_uncerUp[thread]=float(interpolate.splev(x, tck4))
            qcd_uncerDn[thread]=float(interpolate.splev(x, tck5))
        #qcdunc[thread]=float(interpolate.splev(x, tck3))
        #print "the acceptance is  ....................", acceptance[thread] #acc_ggH_powheg
        #print "Bla Bla ....................", acc_ggH_powheg
	    acc_ggH_powheg[str(thread)]={}
	    acc_ggH_powheg[str(thread2)]={}
	    acc_ggH_powheg[str(thread)]=acceptance[thread]
	    acc_ggH_powheg[str(thread2)]=acc_ggH_powheg[thread0n]*acc_ggH_powheg[str(thread)]/acc_ggH_powheg[str(thread0p)]  #acceptance[thread]
#            acc_ggH_powheg.update(acceptance)
        #print "interpol.           acceptance is  ....................", acc_ggH_powheg[str(thread)]#acc_ggH_powheg
        #print "pdfunc_ggH_powheg                           ",pdfunc_ggH_powheg
            print "the thread is ...........", thread
            print "acceptance is.             ", acceptance[thread] #=float(interpolate.splev(x, tck2))
            print "pdf uncUp is.             ", pdf_uncerUp[thread] #=float(interpolate.splev(x, tck2))
            print "pdf uncDn is.             ", pdf_uncerDn[thread] #=float(interpolate.splev(x, tck2))
            print "qcd uncUp is.             ", qcd_uncerUp[thread] #=float(interpolate.splev(x, tck2))
            print "qcd uncDn is.             ", qcd_uncerDn[thread]
#pdfunc_ggH_powheg.update(pdfunc)
        #pdfunc_ggH_powheg.update(pdf_uncerUp)
        #pdfunc_ggH_powheg[thread]['uncerUp'].update(pdf_uncerUp)
        #pdfunc_ggH_powheg[thread]['uncerUp'].update(pdf_uncerUp)
#       pdfunc_ggH_powheg['uncerUp'].update(pdf_uncerUp)  # error#FIXME
#        print "bla bal is .  ", pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_4mu_'+obsName+'_genbin0']['uncerUp']
            pdfunc_ggH_powheg[str(thread)]={}
            pdfunc_ggH_powheg[str(thread2)]={}
            pdfunc_ggH_powheg[str(thread)]['uncerUp']=pdf_uncerUp[thread]
	    pdfunc_ggH_powheg[str(thread2)]['uncerUp']=pdfunc_ggH_powheg[thread0n]['uncerUp']*pdfunc_ggH_powheg[str(thread)]['uncerUp']/pdfunc_ggH_powheg[str(thread0p)]['uncerUp']  #acceptance[thread]
#            pdfunc_ggH_powheg[str(thread2)]['uncerUp']=pdf_uncerUp[thread]
            pdfunc_ggH_powheg[str(thread)]['uncerDn']=pdf_uncerDn[thread]
	    pdfunc_ggH_powheg[str(thread2)]['uncerDn']=pdfunc_ggH_powheg[thread0n]['uncerDn']*pdfunc_ggH_powheg[str(thread)]['uncerDn']/pdfunc_ggH_powheg[str(thread0p)]['uncerDn']  #acceptance[thread]
#            pdfunc_ggH_powheg[str(thread2)]['uncerDn']=pdf_uncerDn[thread]

            qcdunc_ggH_powheg[str(thread)]={}
            qcdunc_ggH_powheg[str(thread2)]={}
            qcdunc_ggH_powheg[str(thread)]['uncerUp']=qcd_uncerUp[thread]
	    qcdunc_ggH_powheg[str(thread2)]['uncerUp']=qcdunc_ggH_powheg[thread0n]['uncerUp']*qcdunc_ggH_powheg[str(thread)]['uncerUp']/qcdunc_ggH_powheg[str(thread0p)]['uncerUp']  #acceptance[thread]
           # qcdunc_ggH_powheg[str(thread2)]['uncerUp']=qcd_uncerUp[thread]
            qcdunc_ggH_powheg[str(thread)]['uncerDn']=qcd_uncerDn[thread]
	    qcdunc_ggH_powheg[str(thread2)]['uncerDn']=qcdunc_ggH_powheg[thread0n]['uncerDn']*qcdunc_ggH_powheg[str(thread)]['uncerDn']/qcdunc_ggH_powheg[str(thread0p)]['uncerDn']  #acceptance[thread]
	    print thread, thread0p, thread2, thread0n
	    print "qcdunc_ggH_powheg[thread0n]['uncerDn']", qcdunc_ggH_powheg[thread0n]['uncerDn']
	    print "qcdunc_ggH_powheg[thread]['uncerDn']",qcdunc_ggH_powheg[str(thread)]['uncerDn'] # qcdunc_ggH_powheg[thread0n]['uncerDn']
	    print "qcdunc_ggH_powheg[thread0p]['uncerDn']",qcdunc_ggH_powheg[str(thread0p)]['uncerDn'] # qcdunc_ggH_powheg[thread0n]['uncerDn']
            print "qcdunc_ggH_powheg[str(thread2)]['uncerDn']", qcdunc_ggH_powheg[str(thread2)]['uncerDn']
#            qcdunc_ggH_powheg[str(thread2)]['uncerDn']=qcd_uncerDn[thread]
            #os.system('cp accUnc_'+opt.OBSNAME+'.py accUnc_'+opt.OBSNAME+'_ORIG.py')
            #os.system('cp accUnc_'+opt.OBSNAME+'_2018.py accUnc_'+opt.OBSNAME+'_2018_ORIG.py')
            os.system('cp accUnc_'+opt.OBSNAME+'_'+opt.YEAR+'.py accUnc_'+opt.OBSNAME+'_'+opt.YEAR+'_ORIG.py')
#            os.system('cp accUnc_mass4l_ORIG.py accUnc_mass4l.py')
#            with open('accUnc_mass4l.py', 'w') as f:
	    #with open('accUnc_'+obsName+'.py', 'w') as f:
	    #with open('accUnc_'+obsName+'_2018.py', 'w') as f:
	    with open('accUnc_'+obsName+'_'+opt.YEAR+'.py', 'w') as f:
                print "going write interpolated values   "
                f.write('acc = '+str(acc_ggH_powheg)+' \n')
                f.write('qcdUncert = '+str(qcdunc_ggH_powheg)+' \n')
                f.write('pdfUncert = '+str(pdfunc_ggH_powheg)+' \n')

    return interpolate.splev(x, tck1)

global opt, args
parseOptions()
observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
nbins = len(observableBins)
obsName = opt.OBSNAME

#value= f(125.38);
value= f(125.38,nbins,obsName);
#value= f(125)
print ("the value is ", value)
