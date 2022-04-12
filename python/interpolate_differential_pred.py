import optparse
import optparse
import os

from scipy import interpolate

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

def interpolate_pred(x, nbins, obsName, DEBUG):
    """Module to get the interpolation from powheg and apply that SF to the NNLOPS sample

    Args:
        x (float): Mass value for which we need the eff, acc, etc.
        nbins (int): Number of bins
        obsName (str): Name of observable
        DEBUG (bool): True/False depending if you want many printouts or least
    """
    if (DEBUG): border_msg("Start of module `interpolate_pred`")
    acceptance={}
    # pdfunc={}
    pdf_uncerUp={}
    pdf_uncerDn={}
    qcd_uncerUp={}
    qcd_uncerDn={}
    # qcdunc={}

    _temp = __import__('accUnc_'+obsName, globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
    acc_ggH_powheg = _temp.acc
    pdfunc_ggH_powheg = _temp.pdfUncert
    qcdunc_ggH_powheg = _temp.qcdUncert
    if (DEBUG): print("[INFO]#L{:3}:  acc_ggH_powheg: {}".format(get_linenumber(), acc_ggH_powheg))

    x_points = [124, 125, 126]
    channels=['4mu','2e2mu','4e']
    if obsName=='mass4l':
        channels=['4mu','2e2mu','4e','4l']

    for channel in channels:
        for obsBin in range(0, nbins-1):
            if (DEBUG): border_msg("obsName: {:12} Channel: {:5} obsBin: {:3}".format(obsName, channel, obsBin))

            key_powheg_M125='ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            key_powheg_MX='ggH_powheg_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            if (DEBUG): print("[INFO]#L{:3}: key_powheg_MX: {}".format(get_linenumber(), key_powheg_MX))

            # FIXME: Later we can generalise this so that we can apply this SF to other samples
            key_NNLOPS_M125='ggH_NNLOPS_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)
            key_NNLOPS_MX='ggH_NNLOPS_JHUgen_'+str(x)+'_'+channel+'_'+obsName+'_genbin'+str(obsBin)

            # acceptance[key_powheg_MX]=0.0
            # pdf_uncerUp[key_powheg_MX]=0.0
            # pdf_uncerDn[key_powheg_MX]=0.0
            # qcd_uncerUp[key_powheg_MX]=0.0
            # qcd_uncerDn[key_powheg_MX]=0.0

            acc_points = [acc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)],acc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]]   #  [12,14,22,39,58,77]
            pdf_points_uncerUp = [pdfunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp']]   #  [12,14,22,39,58,77]
            pdf_points_uncerDn = [pdfunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],pdfunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn']]
            qcd_points_uncerUp = [qcdunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerUp']]   #  [12,14,22,39,58,77]
            qcd_points_uncerDn = [qcdunc_ggH_powheg['ggH_powheg_JHUgen_124_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_125_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn'],qcdunc_ggH_powheg['ggH_powheg_JHUgen_126_'+channel+'_'+obsName+'_genbin'+str(obsBin)]['uncerDn']]   #  [12,14,22,39,58,77]

            if (DEBUG): print("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "acc_points", acc_points))
            if (DEBUG): print("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "pdf_points_uncerUp", pdf_points_uncerUp))
            if (DEBUG): print("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "pdf_points_uncerDn", pdf_points_uncerDn))
            if (DEBUG): print("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "qcd_points_uncerUp", qcd_points_uncerUp))
            if (DEBUG): print("[INFO]#L{:3}: {:21} {}".format(get_linenumber(), "qcd_points_uncerDn", qcd_points_uncerDn))

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
            if (DEBUG): print("[INFO]#L{:3}: key_powheg_MX                       : {}".format(get_linenumber(), key_powheg_MX ))
            if (DEBUG): print("[INFO]#L{:3}: acceptance[key_powheg_MX]   : {}".format(get_linenumber(), acceptance[key_powheg_MX] ))
            if (DEBUG): print("[INFO]#L{:3}: pdf_uncerUp[key_powheg_MX] : {}".format(get_linenumber(), pdf_uncerUp[key_powheg_MX] ))
            if (DEBUG): print("[INFO]#L{:3}: pdf_uncerDn[key_powheg_MX] : {}".format(get_linenumber(), pdf_uncerDn[key_powheg_MX] ))
            if (DEBUG): print("[INFO]#L{:3}: qcd_uncerUp[key_powheg_MX] : {}".format(get_linenumber(), qcd_uncerUp[key_powheg_MX] ))
            if (DEBUG): print("[INFO]#L{:3}: qcd_uncerDn[key_powheg_MX] : {}".format(get_linenumber(), qcd_uncerDn[key_powheg_MX]))

            # Compute the acc, pdf and qcd unc for NNLOPS
            acc_ggH_powheg[str(key_powheg_MX)] = {}
            acc_ggH_powheg[str(key_powheg_MX)] = acceptance[key_powheg_MX]

            acc_ggH_powheg[str(key_NNLOPS_MX)] = {}
            acc_ggH_powheg[str(key_NNLOPS_MX)] = acc_ggH_powheg[key_NNLOPS_M125]*(acc_ggH_powheg[str(key_powheg_MX)]/acc_ggH_powheg[str(key_powheg_M125)] )
            if (DEBUG): print("[INFO]#L{:3}: acc_ggH_powheg[str(key_NNLOPS_MX)]: {}".format(get_linenumber(), acc_ggH_powheg[str(key_NNLOPS_MX)]))

            pdfunc_ggH_powheg[str(key_powheg_MX)]={}
            pdfunc_ggH_powheg[str(key_powheg_MX)]['uncerUp'] = pdf_uncerUp[key_powheg_MX]
            pdfunc_ggH_powheg[str(key_powheg_MX)]['uncerDn']=pdf_uncerDn[key_powheg_MX]

            pdfunc_ggH_powheg[str(key_NNLOPS_MX)]={}
            pdfunc_ggH_powheg[str(key_NNLOPS_MX)]['uncerUp']=pdfunc_ggH_powheg[key_NNLOPS_M125]['uncerUp']*(pdfunc_ggH_powheg[str(key_powheg_MX)]['uncerUp']/pdfunc_ggH_powheg[str(key_powheg_M125)]['uncerUp'])
            pdfunc_ggH_powheg[str(key_NNLOPS_MX)]['uncerDn']=pdfunc_ggH_powheg[key_NNLOPS_M125]['uncerDn']*pdfunc_ggH_powheg[str(key_powheg_MX)]['uncerDn']/pdfunc_ggH_powheg[str(key_powheg_M125)]['uncerDn']  #acceptance[key_powheg_MX]

            qcdunc_ggH_powheg[str(key_powheg_MX)]={}
            qcdunc_ggH_powheg[str(key_powheg_MX)]['uncerUp']=qcd_uncerUp[key_powheg_MX]
            qcdunc_ggH_powheg[str(key_powheg_MX)]['uncerDn']=qcd_uncerDn[key_powheg_MX]

            qcdunc_ggH_powheg[str(key_NNLOPS_MX)]={}
            qcdunc_ggH_powheg[str(key_NNLOPS_MX)]['uncerUp']=qcdunc_ggH_powheg[key_NNLOPS_M125]['uncerUp']*qcdunc_ggH_powheg[str(key_powheg_MX)]['uncerUp']/qcdunc_ggH_powheg[str(key_powheg_M125)]['uncerUp']  #acceptance[key_powheg_MX]
            qcdunc_ggH_powheg[str(key_NNLOPS_MX)]['uncerDn']=qcdunc_ggH_powheg[key_NNLOPS_M125]['uncerDn']*qcdunc_ggH_powheg[str(key_powheg_MX)]['uncerDn']/qcdunc_ggH_powheg[str(key_powheg_M125)]['uncerDn']  #acceptance[key_powheg_MX]

    # FIXME: Hardcoded path
    DirForUncFiles = "python"
    OutputDictFileName = 'accUnc_'+obsName+'.py'
    os.system('cp ' + DirForUncFiles + '/' + OutputDictFileName + " " +DirForUncFiles+'/'+ OutputDictFileName.replace('.py','_beforeInterpolation.py'))

    with open(DirForUncFiles + '/' + OutputDictFileName, 'w') as f:
        print("going write interpolated values in file:   " + OutputDictFileName)
        f.write('acc = '+str(acc_ggH_powheg)+' \n')
        f.write('qcdUncert = '+str(qcdunc_ggH_powheg)+' \n')
        f.write('pdfUncert = '+str(pdfunc_ggH_powheg)+' \n')

if __name__ == "__main__":

    global opt, args
    parseOptions()

    observableBins = {0:(opt.OBSBINS.split("|")[1:(len(opt.OBSBINS.split("|"))-1)]),1:['0','inf']}[opt.OBSBINS=='inclusive']
    nbins = len(observableBins)

    print("\n==> Obs Name: {:15}  nBins: {:2}  bins: {}".format(opt.OBSNAME, nbins, observableBins))

    interpolate_pred(125.38, nbins, opt.OBSNAME,  opt.DEBUG);

    print("Interpolation completed... :) ")
    print("----------\n")
