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

def interpolate_full(x, nbins, obsName, year, DEBUG = 0):
    global datacardInputs

    border_msg("Start of module `interpolate_full`")

    datacardInputs = datacardInputs.format(year = year)
    sys.path.append(datacardInputs)

    x_points = [124, 125, 126]
    channels=['4mu','2e2mu','4e']

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
    # acc_4l = {}
    # dacc_4l = {}
    binfrac_wrongfrac = {}
    cfactor = {}
    lambdajesup = {}
    lambdajesdn = {}
    if (DEBUG): print("===>Line#{}:  acceptance: {}".format(get_linenumber(), acceptance))

    _temp = __import__('inputs_sig_'+obsName, globals(), locals(), ['acc','dacc','eff','deff','inc_outfrac','binfrac_outfrac','outinratio','doutinratio','inc_wrongfrac', 'inc_outfrac','binfrac_wrongfrac','cfactor','lambdajesup','lambdajesdn'], -1)
    acc_ggH_powheg = _temp.acc
    dacc_ggH_powheg = _temp.dacc
    eff_ggH_powheg = _temp.eff
    deff_ggH_powheg = _temp.deff
    inc_wrongfrac_ggH_powheg = _temp.inc_wrongfrac
    binfrac_outfrac_ggH_powheg = _temp.binfrac_outfrac
    outinratio_ggH_powheg = _temp.outinratio
    doutinratio_ggH_powheg = _temp.doutinratio
    # acc_4l_ggH_powheg = _temp.acc_4l
    # dacc_4l_ggH_powheg = _temp.dacc_4l
    inc_outfrac_ggH_powheg = _temp.inc_outfrac
    binfrac_wrongfrac_ggH_powheg = _temp.binfrac_wrongfrac
    cfactor_ggH_powheg = _temp.cfactor
    lambdajesup_ggH_powheg = _temp.lambdajesup
    lambdajesdn_ggH_powheg = _temp.lambdajesdn
    if (DEBUG): print("===>Line#{}:  acc_ggH_powheg: {}".format(get_linenumber(), acc_ggH_powheg))

    for channel in channels:
        for obsBin in range(0, nbins-1):
            for recoBin in range(0, nbins-1):
                border_msg("obsName: {:11} Channel: {:5} obsBin: {:3}  recoBin: {}".format(obsName, channel, obsBin, recoBin))

                key_powheg_MX = 'ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)
                print("=== ===>{:15} : {}".format("dict key", key_powheg_MX))

                # INFO: Step: 1: Grab info from inputs_sig_*.py and get an array for three different mass points [124, 125, 126] using corresponding acc, eff, etc.
                acc_points = [acc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                dacc_points = [dacc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                eff_points = [eff_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],eff_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],eff_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                deff_points = [deff_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],deff_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],deff_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                inc_wrongfrac_points = [inc_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                binfrac_outfrac_points = [binfrac_outfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_outfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_outfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                outinratio_points = [outinratio_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],outinratio_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],outinratio_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                doutinratio_points = [doutinratio_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],doutinratio_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],doutinratio_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                # acc_4l_points = [acc_4l_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_4l_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],acc_4l_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                # dacc_4l_points = [dacc_4l_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_4l_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],dacc_4l_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                inc_outfrac_points = [inc_outfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_outfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],inc_outfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                binfrac_wrongfrac_points = [binfrac_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],binfrac_wrongfrac_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                cfactor_points = [cfactor_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],cfactor_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],cfactor_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                lambdajesup_points = [lambdajesup_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesup_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesup_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]
                lambdajesdn_points = [lambdajesdn_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesdn_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)],lambdajesdn_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)+'_recobin'+str(recoBin)]]

                print("=== ===>{:15} : {}".format("acc_points", acc_points))
                print("=== ===>{:15} : {}".format("eff_points", eff_points))

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
                # spl_acc_4l_points = interpolate.splrep(x_points, acc_4l_points, k=2)
                # spl_dacc_4l_points = interpolate.splrep(x_points, dacc_4l_points, k=2)
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
                # acc_4l[key_powheg_MX]=float(interpolate.splev(x, spl_acc_4l_points))
                # dacc_4l[key_powheg_MX]=float(interpolate.splev(x, spl_dacc_4l_points))
                inc_outfrac[key_powheg_MX]= float(interpolate.splev(x, spl_inc_outfrac_points))
                binfrac_wrongfrac[key_powheg_MX]= float(interpolate.splev(x, spl_binfrac_wrongfrac_points))
                cfactor[key_powheg_MX]= float(interpolate.splev(x, spl_cfactor_points))
                lambdajesup[key_powheg_MX]= float(interpolate.splev(x, spl_lambdajesup_points))
                lambdajesdn[key_powheg_MX]= float(interpolate.splev(x, spl_lambdajesdn_points))

                print("=== ===>{:15} : {}".format("acceptance", acceptance))

                #################################################################
                # INFO: Step - 4: Update the original dict
                acc_ggH_powheg.update(acceptance)
                dacc_ggH_powheg.update(dacceptance)
                eff_ggH_powheg.update(efficiency)
                deff_ggH_powheg.update(defficiency)
                inc_wrongfrac_ggH_powheg.update(inc_wrongfrac)
                binfrac_outfrac_ggH_powheg.update(binfrac_outfrac)
                outinratio_ggH_powheg.update(outinratio)
                doutinratio_ggH_powheg.update(doutinratio)
                # acc_4l_ggH_powheg.update(acc_4l)
                # dacc_4l_ggH_powheg.update(dacc_4l)
                inc_outfrac_ggH_powheg.update(inc_outfrac)
                binfrac_wrongfrac_ggH_powheg.update(binfrac_wrongfrac)
                cfactor_ggH_powheg.update(cfactor)
                lambdajesup_ggH_powheg.update(lambdajesup)
                lambdajesdn_ggH_powheg.update(lambdajesdn)
                if (DEBUG): print("=== ===>{:15} : {}".format("acc_ggH_powheg", acc_ggH_powheg))

    OutputDictFileName = datacardInputs+'/inputs_sig_'+obsName+'.py'
    os.system('cp ' + OutputDictFileName + " " + OutputDictFileName.replace('.py','_beforeInterpolation.py'))

    with open( OutputDictFileName, 'w') as f:
        print("going write interpolated values  in  "+OutputDictFileName)
        f.write('acc = '+str(acc_ggH_powheg)+' \n')
        f.write('dacc = '+str(dacc_ggH_powheg)+' \n')
        f.write('eff = '+str(eff_ggH_powheg)+' \n')
        f.write('deff = '+str(deff_ggH_powheg)+' \n')
        f.write('inc_wrongfrac = '+str(inc_wrongfrac_ggH_powheg)+' \n')
        f.write('binfrac_outfrac = '+str(binfrac_outfrac_ggH_powheg)+' \n')
        f.write('outinratio = '+str(outinratio_ggH_powheg)+' \n')
        f.write('doutinratio = '+str(doutinratio_ggH_powheg)+' \n')
        # f.write('acc_4l = '+str(acc_4l_ggH_powheg)+' \n')
        # f.write('dacc_4l = '+str(dacc_4l_ggH_powheg)+' \n')
        f.write('inc_outfrac = '+str(inc_outfrac_ggH_powheg)+' \n')
        f.write('binfrac_wrongfrac = '+str(binfrac_wrongfrac_ggH_powheg)+' \n')
        f.write('cfactor = '+str(cfactor_ggH_powheg)+' \n')
        f.write('lambdajesup = '+str(lambdajesup_ggH_powheg)+' \n')
        f.write('lambdajesdn = '+str(lambdajesdn_ggH_powheg)+' \n')


if __name__ == "__main__":
    global opt, args
    parseOptions()
    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    nbins = len(observableBins)

    print("Obs Name: {:15}  nBins: {:2}  bins: {}".format(opt.OBSNAME, nbins, observableBins))

    interpolate_full(125.38, nbins, opt.OBSNAME, opt.YEAR, opt.DEBUG)
    print("Interpolation completed... :) ")
