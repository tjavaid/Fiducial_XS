import optparse
import os
import sys

from scipy import interpolate
import matplotlib.pyplot as plt

from Input_Info import datacardInputs
from Utils import *


def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('',   '--obsName',  dest='OBSNAME',  type='string',default='',   help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
    parser.add_option('',   '--obsBins',  dest='OBSBINS',  type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--year',  dest='YEAR',  type='string',default='2018',   help='Era to analyze, e.g. 2016, 2017, 2018 or Full ')
    parser.add_option('',   '--debug',  dest='DEBUG',  type='int',default=0,   help='0 if debug false, else debug True')
    global opt, args
    (opt, args) = parser.parse_args()

def interpolate_full(x, nbins, obsName, DEBUG = 0):
    border_msg("Start of module `interpolate_full`")
    sys.path.append(datacardInputs)

    channels=['4mu','2e2mu','4e']
    x_points = [124, 125, 126]
    #x_points = [120, 124, 125, 126, 130]
    #modes= ['ggH_powheg_JHUgen_']
    modes=['ggH_powheg_JHUgen_','VBF_powheg_JHUgen_','ZH_powheg_JHUgen_','WH_powheg_JHUgen_','ttH_powheg_JHUgen_']

    if obsName=='mass4l': channels=['4mu','2e2mu','4e','4l']

    acceptance={}
    dacceptance={}
    efficiency={}
    defficiency={}
    inc_wrongfrac = {}
    binfrac_outfrac = {}
    outinratio = {}
    doutinratio = {}
    inc_outfrac = {}
    acc_4l = {}
    dacc_4l = {}
    binfrac_wrongfrac = {}
    cfactor = {}
    lambdajesup = {}
    lambdajesdn = {}
    if (DEBUG): print("===>Line#{}:  acceptance: {}".format(get_linenumber(), acceptance))

    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc','dacc','eff','deff','inc_outfrac','binfrac_outfrac','outinratio','doutinratio','inc_wrongfrac', 'inc_outfrac','binfrac_wrongfrac','cfactor','lambdajesup','lambdajesdn'], -1)
    acc_all = _temp.acc
    dacc_all = _temp.dacc
    eff_all = _temp.eff
    deff_all = _temp.deff
    inc_wrongfrac_all = _temp.inc_wrongfrac
    binfrac_outfrac_all = _temp.binfrac_outfrac
    outinratio_all = _temp.outinratio
    doutinratio_all = _temp.doutinratio
    acc_4l_all = _temp.acc_4l
    dacc_4l_all = _temp.dacc_4l
    inc_outfrac_all = _temp.inc_outfrac
    binfrac_wrongfrac_all = _temp.binfrac_wrongfrac
    cfactor_all = _temp.cfactor
    lambdajesup_all = _temp.lambdajesup
    lambdajesdn_all = _temp.lambdajesdn
    if (DEBUG): print("===>Line#{}:  acc_all: {}".format(get_linenumber(), acc_all))
    for mode in modes:
        for channel in channels:
            for obsBin in range(0, nbins-1):
                for recoBin in range(0, nbins-1):
                    if (DEBUG): border_msg("obsName: {:11} Channel: {:5} obsBin: {:3}  recoBin: {}".format(obsName, channel, obsBin, recoBin))

                    #key_powheg_MX = 'ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)
                    key_powheg_MX = mode+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)
                    if (DEBUG): print("=== ===>{:15} : {}".format("dict key", key_powheg_MX))
            # introducing lists to store the values at different mass points
                    acc_points = []; dacc_points = []; acc_4l_points = []; dacc_4l_points = []; eff_points = []; deff_points = []; inc_wrongfrac_points = []; binfrac_outfrac_points = []; outinratio_points = []; doutinratio_points = []; inc_outfrac_points = []; binfrac_wrongfrac_points = []; cfactor_points = []; lambdajesup_points = []; lambdajesdn_points = [];

                    # INFO: Step: 1: Grab info from inputs_sig_*.py and get an array for three different mass points [124, 125, 126] using corresponding acc, eff, etc.
                    for point in x_points:
                        key = mode+str(point)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)
                        #print "key is : ", key
                        acc_points.append(acc_all[key]);  acc_4l_points.append(acc_4l_all[key]);
                        dacc_points.append(dacc_all[key]);  dacc_4l_points.append(dacc_4l_all[key]);
                        eff_points.append(eff_all[key]); deff_points.append(deff_all[key]); inc_wrongfrac_points.append(inc_wrongfrac_all[key]);
                        binfrac_outfrac_points.append(binfrac_outfrac_all[key]); outinratio_points.append(outinratio_all[key]);
                        doutinratio_points.append(doutinratio_all[key]);
                        inc_outfrac_points.append(inc_outfrac_all[key]); binfrac_wrongfrac_points.append(binfrac_wrongfrac_all[key]); cfactor_points.append(cfactor_all[key]);
                        lambdajesup_points.append(lambdajesup_all[key]); lambdajesdn_points.append(lambdajesdn_all[key]);

                    if (DEBUG): print("=== ===>{:15} : {}".format("acc_points", acc_points))
                    if (DEBUG): print("=== ===>{:15} : {}".format("eff_points", eff_points))

                    # INFO: Step - 2: Interpolate the line
                    # tck = interpolate.splrep(x_points, y_points)
                    spl_acc_points  = interpolate.splrep(x_points, acc_points, k=2)
                    spl_dacc_points = interpolate.splrep(x_points, dacc_points, k=2)
                    spl_eff_points = interpolate.splrep(x_points, eff_points, k=2)
                    spl_deff_points = interpolate.splrep(x_points, deff_points, k=2)
                    spl_inc_wrongfrac_points = interpolate.splrep(x_points, inc_wrongfrac_points, k=2)
                    spl_binfrac_outfrac_points = interpolate.splrep(x_points, binfrac_outfrac_points, k=2)
                    spl_outinratio_points = interpolate.splrep(x_points, outinratio_points, k=2)
                    spl_doutinratio_points = interpolate.splrep(x_points, doutinratio_points, k=2)
                    spl_acc_4l_points = interpolate.splrep(x_points, acc_4l_points, k=2)
                    spl_dacc_4l_points = interpolate.splrep(x_points, dacc_4l_points, k=2)
                    spl_inc_outfrac_points = interpolate.splrep(x_points, inc_outfrac_points, k=2)
                    spl_binfrac_wrongfrac_points = interpolate.splrep(x_points, binfrac_wrongfrac_points, k=2)
                    spl_cfactor_points = interpolate.splrep(x_points, cfactor_points, k=2)
                    spl_lambdajesup_points = interpolate.splrep(x_points, lambdajesup_points, k=2)
                    spl_lambdajesdn_points = interpolate.splrep(x_points, lambdajesdn_points, k=2)

                    # INFO: Step - 3: Get the value corresponding to "x" based on the interpolation line done above
                    acceptance[key_powheg_MX]=float(interpolate.splev(x, spl_acc_points))
                    dacceptance[key_powheg_MX]= float(interpolate.splev(x, spl_dacc_points))
                    efficiency[key_powheg_MX]=float(interpolate.splev(x, spl_eff_points))
                    defficiency[key_powheg_MX]=float(interpolate.splev(x, spl_deff_points))
                    inc_wrongfrac[key_powheg_MX]=float(interpolate.splev(x, spl_inc_wrongfrac_points))
                    binfrac_outfrac[key_powheg_MX]=float(interpolate.splev(x, spl_binfrac_outfrac_points))
                    outinratio[key_powheg_MX]=float(interpolate.splev(x, spl_outinratio_points))
                    doutinratio[key_powheg_MX]=float(interpolate.splev(x, spl_doutinratio_points))
                    acc_4l[key_powheg_MX]=float(interpolate.splev(x, spl_acc_4l_points))
                    dacc_4l[key_powheg_MX]=float(interpolate.splev(x, spl_dacc_4l_points))
                    inc_outfrac[key_powheg_MX]= float(interpolate.splev(x, spl_inc_outfrac_points))
                    binfrac_wrongfrac[key_powheg_MX]= float(interpolate.splev(x, spl_binfrac_wrongfrac_points))
                    cfactor[key_powheg_MX]= float(interpolate.splev(x, spl_cfactor_points))
                    lambdajesup[key_powheg_MX]= float(interpolate.splev(x, spl_lambdajesup_points))
                    lambdajesdn[key_powheg_MX]= float(interpolate.splev(x, spl_lambdajesdn_points))

                    if (DEBUG): print("=== ===>{:15} : {}".format("acceptance", acceptance))

                    #################################################################
                    # INFO: Step - 4: Update the original dict
                    acc_all.update(acceptance)
                    dacc_all.update(dacceptance)
                    eff_all.update(efficiency)
                    deff_all.update(defficiency)
                    inc_wrongfrac_all.update(inc_wrongfrac)
                    binfrac_outfrac_all.update(binfrac_outfrac)
                    outinratio_all.update(outinratio)
                    doutinratio_all.update(doutinratio)
                    acc_4l_all.update(acc_4l)
                    dacc_4l_all.update(dacc_4l)
                    inc_outfrac_all.update(inc_outfrac)
                    binfrac_wrongfrac_all.update(binfrac_wrongfrac)
                    cfactor_all.update(cfactor)
                    lambdajesup_all.update(lambdajesup)
                    lambdajesdn_all.update(lambdajesdn)
                    if (DEBUG): print("=== ===>{:15} : {}".format("acc_all", acc_all))

    OutputDictFileName = datacardInputs+'/inputs_sig_'+obsName+'.py'
    os.system('cp ' + OutputDictFileName + " " + OutputDictFileName.replace('.py','_beforeInterpolation.py'))

    with open( OutputDictFileName, 'w') as f:
        print("going write interpolated values  in  "+OutputDictFileName)
        f.write('acc = '+str(acc_all)+' \n')
        f.write('dacc = '+str(dacc_all)+' \n')
        f.write('eff = '+str(eff_all)+' \n')
        f.write('deff = '+str(deff_all)+' \n')
        f.write('inc_wrongfrac = '+str(inc_wrongfrac_all)+' \n')
        f.write('binfrac_outfrac = '+str(binfrac_outfrac_all)+' \n')
        f.write('outinratio = '+str(outinratio_all)+' \n')
        f.write('doutinratio = '+str(doutinratio_all)+' \n')
        f.write('acc_4l = '+str(acc_4l_all)+' \n')
        f.write('dacc_4l = '+str(dacc_4l_all)+' \n')
        f.write('inc_outfrac = '+str(inc_outfrac_all)+' \n')
        f.write('binfrac_wrongfrac = '+str(binfrac_wrongfrac_all)+' \n')
        f.write('cfactor = '+str(cfactor_all)+' \n')
        f.write('lambdajesup = '+str(lambdajesup_all)+' \n')
        f.write('lambdajesdn = '+str(lambdajesdn_all)+' \n')


if __name__ == "__main__":
    global opt, args
    parseOptions()
    year=opt.YEAR
    datacardInputs = './'+datacardInputs.format(year = year)

    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    nbins = len(observableBins)

    print("Obs Name: {:15}  nBins: {:2}  bins: {}".format(opt.OBSNAME, nbins, observableBins))

    interpolate_full(125.38, nbins, opt.OBSNAME, opt.DEBUG)
    print("Interpolation completed... :) ")
