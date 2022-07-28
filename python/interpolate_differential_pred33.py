import optparse
import os
import sys

from scipy import interpolate

from Utils import *
from Input_Info import datacardInputs

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

def interpolate_pred(x, nbins, obsName, DEBUG):
    """Module to get the interpolation from powheg and apply that SF to the NNLOPS sample

    Args:
        x (float): Mass value for which we need the eff, acc, etc.
        nbins (int): Number of bins
        obsName (str): Name of observable
        DEBUG (bool): True/False depending if you want many printouts or least
    """
    if (DEBUG): border_msg("Start of module `interpolate_pred`")
    sys.path.append(datacardInputs)

    acceptance={}
    # pdfunc={}
    pdf_uncerUp={}
    pdf_uncerDn={}
    qcd_uncerUp={}
    qcd_uncerDn={}
    # qcdunc={}

    _temp = __import__('accUnc_'+obsName, globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
    acc_all = _temp.acc
    pdfunc_all = _temp.pdfUncert
    qcdunc_all = _temp.qcdUncert
    logger.debug("[INFO]#L{:3}:  acc_all: {}".format(get_linenumber(), acc_all))

    x_points = [124, 125, 126]
    # x_points = [120,124, 125, 126,130]
    modes= ['ggH_powheg_JHUgen_']
    #modes=['ggH_powheg_JHUgen_','ggH_NNLOPS_JHUgen_','ggH_amcatnloFXFX_'] # use when several mass points are available for all three
    channels=['4mu','2e2mu','4e']
    if obsName=='mass4l':
        channels=['4mu','2e2mu','4e','4l']
    for mode in modes:
        for channel in channels:
            for obsBin in range(0, nbins-1):
                if (DEBUG): border_msg("obsName: {:12} Channel: {:5} obsBin: {:3}".format(obsName, channel, obsBin))

                key_powheg_M125='ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                #key_powheg_MX='ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                key_powheg_MX= mode+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                logger.debug("[INFO]#L{:3}: key_powheg_MX: {}".format(get_linenumber(), key_powheg_MX))

                # FIXME: Later we can generalise this so that we can apply this SF to other samples
                # NNLOPs
                key_NNLOPS_M125='ggH_NNLOPS_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                key_NNLOPS_MX='ggH_NNLOPS_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                # amcatnlo
                key_amcatnloFXFX_M125='ggH_amcatnloFXFX_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                key_amcatnloFXFX_MX='ggH_amcatnloFXFX_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)

                acc_points = []; pdf_points_uncerUp =[]; pdf_points_uncerDn =[]; qcd_points_uncerUp = []; qcd_points_uncerDn = [];
                for point in x_points:
                    key = mode+str(point)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
                    acc_points.append(acc_all[key]);
                    pdf_points_uncerUp.append(pdfunc_all[key]['uncerUp']);pdf_points_uncerDn.append(pdfunc_all[key]['uncerDn']);
                    qcd_points_uncerUp.append(qcdunc_all[key]['uncerUp']);qcd_points_uncerDn.append(qcdunc_all[key]['uncerDn']);


                logger.debug("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "acc_points", acc_points))
                logger.debug("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "pdf_points_uncerUp", pdf_points_uncerUp))
                logger.debug("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "pdf_points_uncerDn", pdf_points_uncerDn))
                logger.debug("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "qcd_points_uncerUp", qcd_points_uncerUp))
                logger.debug("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "qcd_points_uncerDn", qcd_points_uncerDn))

                spl_acc_points                = interpolate.splrep(x_points, acc_points, k=2)
                spl_pdf_points_uncerUp = interpolate.splrep(x_points, pdf_points_uncerUp, k=2)
                spl_pdf_points_uncerDn = interpolate.splrep(x_points, pdf_points_uncerDn, k=2)
                spl_qcd_points_uncerUp = interpolate.splrep(x_points, qcd_points_uncerUp, k=2)
                spl_qcd_points_uncerDn = interpolate.splrep(x_points, qcd_points_uncerDn, k=2)

                acceptance[key_powheg_MX]    = float(interpolate.splev(x, spl_acc_points))
                pdf_uncerUp[key_powheg_MX] = float(interpolate.splev(x, spl_pdf_points_uncerUp))
                pdf_uncerDn[key_powheg_MX] = float(interpolate.splev(x, spl_pdf_points_uncerDn))
                qcd_uncerUp[key_powheg_MX] = float(interpolate.splev(x, spl_qcd_points_uncerUp))
                qcd_uncerDn[key_powheg_MX] = float(interpolate.splev(x, spl_qcd_points_uncerDn))
                #qcdunc[key_powheg_MX]=float(interpolate.splev(x, tck3))
                logger.debug("[INFO]#L{:3}: key_powheg_MX                       : {}".format(get_linenumber(), key_powheg_MX ))
                logger.debug("[INFO]#L{:3}: acceptance[key_powheg_MX]   : {}".format(get_linenumber(), acceptance[key_powheg_MX] ))
                logger.debug("[INFO]#L{:3}: pdf_uncerUp[key_powheg_MX] : {}".format(get_linenumber(), pdf_uncerUp[key_powheg_MX] ))
                logger.debug("[INFO]#L{:3}: pdf_uncerDn[key_powheg_MX] : {}".format(get_linenumber(), pdf_uncerDn[key_powheg_MX] ))
                logger.debug("[INFO]#L{:3}: qcd_uncerUp[key_powheg_MX] : {}".format(get_linenumber(), qcd_uncerUp[key_powheg_MX] ))
                logger.debug("[INFO]#L{:3}: qcd_uncerDn[key_powheg_MX] : {}".format(get_linenumber(), qcd_uncerDn[key_powheg_MX]))

                # Compute the acc, pdf and qcd unc for NNLOPS and amcatnloFXFX
        # applying powheg SFs to NNLOPS and amcatnloFXFX because several mass points are not available for these)
                acc_all[str(key_powheg_MX)] = {}
                acc_all[str(key_powheg_MX)] = acceptance[key_powheg_MX]

                acc_all[str(key_NNLOPS_MX)] = {}
                acc_all[str(key_NNLOPS_MX)] = acc_all[key_NNLOPS_M125]*(acc_all[str(key_powheg_MX)]/acc_all[str(key_powheg_M125)] )
                logger.debug("[INFO]#L{:3}: acc_all[str(key_NNLOPS_MX)]: {}".format(get_linenumber(), acc_all[str(key_NNLOPS_MX)]))

                acc_all[str(key_amcatnloFXFX_MX)] = {}
                acc_all[str(key_amcatnloFXFX_MX)] = acc_all[key_amcatnloFXFX_M125]*(acc_all[str(key_powheg_MX)]/acc_all[str(key_powheg_M125)] )
                logger.debug("[INFO]#L{:3}: acc_all[str(key_amcatnloFXFX_MX)]: {}".format(get_linenumber(), acc_all[str(key_amcatnloFXFX_MX)]))

                pdfunc_all[str(key_powheg_MX)]={}
                pdfunc_all[str(key_powheg_MX)]['uncerUp'] = pdf_uncerUp[key_powheg_MX]
                pdfunc_all[str(key_powheg_MX)]['uncerDn']=pdf_uncerDn[key_powheg_MX]

                pdfunc_all[str(key_NNLOPS_MX)]={}
                pdfunc_all[str(key_NNLOPS_MX)]['uncerUp']=pdfunc_all[key_NNLOPS_M125]['uncerUp']*(pdfunc_all[str(key_powheg_MX)]['uncerUp']/pdfunc_all[str(key_powheg_M125)]['uncerUp'])
                pdfunc_all[str(key_NNLOPS_MX)]['uncerDn']=pdfunc_all[key_NNLOPS_M125]['uncerDn']*pdfunc_all[str(key_powheg_MX)]['uncerDn']/pdfunc_all[str(key_powheg_M125)]['uncerDn']  #acceptance[key_powheg_MX]


                pdfunc_all[str(key_amcatnloFXFX_MX)]={}
                pdfunc_all[str(key_amcatnloFXFX_MX)]['uncerUp']=pdfunc_all[key_amcatnloFXFX_M125]['uncerUp']*(pdfunc_all[str(key_powheg_MX)]['uncerUp']/pdfunc_all[str(key_powheg_M125)]['uncerUp'])
                pdfunc_all[str(key_amcatnloFXFX_MX)]['uncerDn']=pdfunc_all[key_amcatnloFXFX_M125]['uncerDn']*pdfunc_all[str(key_powheg_MX)]['uncerDn']/pdfunc_all[str(key_powheg_M125)]['uncerDn']  #acceptance[key_powheg_MX]

                qcdunc_all[str(key_powheg_MX)]={}
                qcdunc_all[str(key_powheg_MX)]['uncerUp']=qcd_uncerUp[key_powheg_MX]
                qcdunc_all[str(key_powheg_MX)]['uncerDn']=qcd_uncerDn[key_powheg_MX]

                qcdunc_all[str(key_NNLOPS_MX)]={}
                qcdunc_all[str(key_NNLOPS_MX)]['uncerUp']=qcdunc_all[key_NNLOPS_M125]['uncerUp']*qcdunc_all[str(key_powheg_MX)]['uncerUp']/qcdunc_all[str(key_powheg_M125)]['uncerUp']  #acceptance[key_powheg_MX]
                qcdunc_all[str(key_NNLOPS_MX)]['uncerDn']=qcdunc_all[key_NNLOPS_M125]['uncerDn']*qcdunc_all[str(key_powheg_MX)]['uncerDn']/qcdunc_all[str(key_powheg_M125)]['uncerDn']  #acceptance[key_powheg_MX]

                qcdunc_all[str(key_amcatnloFXFX_MX)]={}
                qcdunc_all[str(key_amcatnloFXFX_MX)]['uncerUp']=qcdunc_all[key_amcatnloFXFX_M125]['uncerUp']*qcdunc_all[str(key_powheg_MX)]['uncerUp']/qcdunc_all[str(key_powheg_M125)]['uncerUp']  #acceptance[key_powheg_MX]
                qcdunc_all[str(key_amcatnloFXFX_MX)]['uncerDn']=qcdunc_all[key_amcatnloFXFX_M125]['uncerDn']*qcdunc_all[str(key_powheg_MX)]['uncerDn']/qcdunc_all[str(key_powheg_M125)]['uncerDn']  #acceptance[key_powheg_MX]


    OutputDictFileName = 'accUnc_'+obsName+'.py'
    os.system('cp ' + datacardInputs + '/' + OutputDictFileName + " " +datacardInputs+'/'+ OutputDictFileName.replace('.py','_beforeInterpolation.py'))


    with open(datacardInputs + '/' + OutputDictFileName, 'w') as f:
        print("going write interpolated values in file:   " + OutputDictFileName)
        f.write('acc = '+str(acc_all)+' \n')
        f.write('qcdUncert = '+str(qcdunc_all)+' \n')
        f.write('pdfUncert = '+str(pdfunc_all)+' \n')


if __name__ == "__main__":

    global opt, args
    parseOptions()
    year=opt.YEAR
    datacardInputs = './'+datacardInputs.format(year = year)

    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    nbins = len(observableBins)

    print("\n==> Obs Name: {:15}  nBins: {:2}  bins: {}".format(opt.OBSNAME, nbins, observableBins))

    interpolate_pred(125.38, nbins, opt.OBSNAME,  opt.DEBUG);

    print("Interpolation completed... :) ")
    print("----------\n")
