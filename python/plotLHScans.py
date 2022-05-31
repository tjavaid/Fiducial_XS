import optparse
import os
import sys
from array import array
from decimal import *
from math import *

from sample_shortnames import *
from Input_Info import *
from Utils import logger, GetDirectory
from read_bins import read_bins

grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)

### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "mass4l", "pT4l", "massZ2", "rapidity4l", "cosThetaStar", "nets_reco_pt30_eta4p7"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--lumiscale', type='string', dest='LUMISCALE', default='1.0', help='Scale yields')
    parser.add_option('-y', '--year', dest="ERA", type = 'string', default = '2018', help='Specifies the data taking period')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)

    # store options and arguments as global variables
    global opt, args, datacardInputs, combineOutputs
    (opt, args) = parser.parse_args()

    datacardInputs = datacardInputs.format(year = opt.ERA)
    combineOutputs = combineOutputs.format(year = opt.ERA)

# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs

# Don't move the root import before `sys.argv = grootargs`. Reference: https://root-forum.cern.ch/t/python-options-and-root-options/4641/3
from ROOT import *
from tdrStyle import *
setTDRStyle()

observables = [opt.OBSNAME]
ListObsName = (''.join((opt.OBSNAME).split())).split('vs')

observableBins = read_bins(opt.OBSBINS)
logger.info("Parsed bins: {}".format(observableBins))
logger.info("Bin size = "+str(len(observableBins)))

nBins = len(observableBins) -1
if len(ListObsName) == 2:    # INFO: for 2D this list size == 2
    nBins = len(observableBins)
logger.debug("nBins: = "+str(nBins))


resultsXS ={}

for obsName in observables:

    if obsName=="mass4l":
        obsbins = ['SigmaBin0','r2e2muBin0','r4muBin0','r4eBin0']
    else:
        obsbins = ["SigmaBin"+str(bins_) for bins_ in range(0, nBins)]

    logger.debug("obsName: {:12}, obsBins: {}".format(obsName, obsbins))

    for obsbin in obsbins:

        # FIXME: Why continue for `cosTheta1`
        if (obsName=="cosTheta1" and obsbin=="0"): continue

        inFile = combineOutputs + "/higgsCombine"+obsName.replace(' ','_')+"_"+obsbin+"_"+opt.ERA+".MultiDimFit.mH125.38.root"
        logger.info("File to read: {}".format(inFile))
        f = TFile(inFile,"READ")
        if (f==0): continue

        limit = f.Get("limit")
        npoints = limit.GetEntries()

        sigma = []
        deltanll = []
        bestfit = 9999.0

        for point in range(0, npoints):
            limit.GetEntry(point)
            if (point == 0): bestfit=getattr(limit, obsbin)
            if (point > 0):
                if (limit.deltaNLL<2.5):
                    sigma.append(getattr(limit, obsbin))
                    deltanll.append(2.0*limit.deltaNLL)

            if point>0 and len(deltanll)>0:
                if deltanll[len(deltanll)-1]>5.0 and sigma[len(sigma)-1]>bestfit: break

        fstat = TFile(combineOutputs + "/higgsCombine"+obsName.replace(' ','_')+"_"+obsbin+"_NoSys"+"_"+opt.ERA+".MultiDimFit.mH125.38.root","READ")
        if (fstat==0): continue

        limitstat = fstat.Get("limit")
        npointsstat = limitstat.GetEntries()

        sigmastat = []
        deltanllstat = []
        bestfitstat = 9999.0

        for point in range(0,npointsstat):
            limitstat.GetEntry(point)
            if (point == 0): bestfit=getattr(limitstat, obsbin)
            if (point > 0):
                if (limitstat.deltaNLL<2.5):
                    sigmastat.append(getattr(limitstat, obsbin))
                    deltanllstat.append(2.0*limitstat.deltaNLL)

            if point>0 and len(deltanllstat)>0:
                if deltanllstat[len(deltanllstat)-1]>5.0 and sigmastat[len(sigmastat)-1]>bestfit: break


        print("obsName: {}, obsbin: {}".format(obsName,obsbin))
        scan = TGraph(len(sigma),array('d',sigma),array('d',deltanll))
        scanstat = TGraph(len(sigmastat),array('d',sigmastat),array('d',deltanllstat))


        c = TCanvas("c","c",1000,800)

        dummy = TH1D("dummy","dummy",1,0.0,sigmastat[len(sigmastat)-1])
        dummy.SetMinimum(0.0)
        dummy.SetMaximum(5.0)
        dummy.SetLineColor(0)
        dummy.SetMarkerColor(0)
        dummy.SetLineWidth(0)
        dummy.SetMarkerSize(0)
        dummy.GetYaxis().SetTitle("-2 #Delta lnL")
        dummy.GetXaxis().SetTitle("#sigma_{fid.} [fb]")
        dummy.Draw()

        scan.SetLineWidth(2)
        scan.SetLineColor(1)
        scan.Draw("Lsame")

        scanstat.SetLineWidth(2)
        scanstat.SetLineStyle(2)
        scanstat.SetLineColor(1)
        scanstat.Draw("Lsame")


        gStyle.SetOptFit(0)

        f1 = TF1("f1","pol8",0.0,5.0)
        f1.SetLineColor(1)
        f1.SetLineWidth(2)
        scan.Fit("f1","N")
        #f1.Draw("same")

        f1stat = TF1("f1stat","pol8",0.0,5.0)
        f1stat.SetLineColor(1)
        f1stat.SetLineWidth(2)
        f1stat.SetLineStyle(2)
        scanstat.Fit("f1stat","N")
        #f1stat.Draw("same")

        cl68 = TF1("cl68","1.0",0.0,5.0)
        cl68.SetLineStyle(2)
        cl68.SetLineColor(1)
        cl68.Draw("same")

        cl95 = TF1("cl95","3.84",0.0,5.0)
        cl95.SetLineStyle(2)
        cl95.SetLineColor(1)
        cl95.Draw("same")

        cl68up = 0.0
        cl68dn = 0.0
        cl95up = 0.0
        cl95dn = 0.0

        cl68upstat = 0.0
        cl68dnstat = 0.0
        cl95upstat = 0.0
        cl95dnstat = 0.0

        for i in range(0,100000): # FIXME: What is this doing?
            x = 0.+i/20000.
            #scanval = f1.Eval(x)
            scanval = scan.Eval(x)
            #if abs(scanval-3.84)<.001: print x,scanval
            if abs(scanval-1.0)<.003 and x<bestfit:
                cl68dn = round((bestfit-x),6)
            if abs(scanval-1.0)<.003 and x>bestfit:
                cl68up = round((x-bestfit),6)
            if abs(scanval-3.84)<.003 and x<bestfit:
                cl95dn = round((bestfit-x),6)
            if abs(scanval-3.84)<.003 and x>bestfit:
                cl95up = round((x-bestfit),6)

        if (cl68dn==0.0): cl68dn=round(bestfit,6)
        if (cl95dn==0.0): cl95dn=round(bestfit,6)

        print(obsName,obsbin,round(bestfit,6),"+",cl68up,"-",cl68dn,"(68%)","+",cl95up,"-",cl95dn,"(95%)")

        for i in range(0,100000):
            x = 0.+i/20000.
            #scanval = f1stat.Eval(x)
            scanval = scanstat.Eval(x)
            #if abs(scanval-3.84)<.001: print x,scanval
            if abs(scanval-1.0)<.003 and x<bestfit:
                cl68dnstat = round((bestfit-x),6)
            if abs(scanval-1.0)<.003 and x>bestfit:
                cl68upstat = round((x-bestfit),6)
            if abs(scanval-3.84)<.003 and x<bestfit:
                cl95dnstat = round((bestfit-x),6)
            if abs(scanval-3.84)<.003 and x>bestfit:
                cl95upstat = round((x-bestfit),6)

        if (cl68dnstat==0.0): cl68dnstat=round(bestfit,6)
        if (cl95dnstat==0.0): cl95dnstat=round(bestfit,6)


        print(obsName,obsbin,round(bestfit,6),"+",cl68upstat,"-",cl68dnstat,"(68%)","+",cl95upstat,"-",cl95dnstat,"(95%)")

        sysup = round(sqrt(max(0.0,cl68up**2-cl68upstat**2)),6)
        sysdn = round(sqrt(max(0.0,cl68dn**2-cl68dnstat**2)),6)
        print(obsName,obsbin,round(bestfit,6),"+",cl68upstat,"-",cl68dnstat,"(stat.)","+",sysup,"-",sysdn,"(sys.)")

        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right
        print(opt.LUMISCALE)
        if (not opt.LUMISCALE=="1.0"):
            lumi = round(59.7*float(opt.LUMISCALE),1)
            latex2.DrawLatex(0.87, 0.94,str(lumi)+" fb^{-1} (13 TeV)")
        else:
            latex2.DrawLatex(0.87, 0.95,"59.7 fb^{-1} (13 TeV)")
        latex2.SetTextSize(0.8*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right
        latex2.DrawLatex(0.19, 0.95, "CMS")
        latex2.SetTextSize(0.6*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.30, 0.95, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.45*c.GetTopMargin())
        #latex2.DrawLatex(0.30,0.85, obsName+" Bin"+obsbin)
        #latex2.DrawLatex(0.30,0.78, "#sigma_{fid.} = "+str(round(bestfit,3))+" ^{+"+str(cl68up)+"}_{-"+str(cl68dn)+"} (68%) ^{+"+str(cl95up)+"}_{-"+str(cl95dn)+"} (95%)")
        latex2.DrawLatex(0.37,0.78, "#sigma_{fid.} = "+str(round(bestfit,3))+" ^{+"+str(cl68upstat)+"}_{-"+str(cl68dnstat)+"} (stat.) ^{+"+str(sysup)+"}_{-"+str(sysdn)+"} (sys.)")


        if (obsName=="mass4l"):
            if (obsbin=="SigmaBin0"):
                resultsXS['SM_125_mass4l_genbin0'] = {"uncerDn": -1.0*cl68dn, "uncerUp": cl68up, "central": bestfit}
                resultsXS['SM_125_mass4l_genbin0_statOnly'] = {"uncerDn": -1.0*cl68dnstat, "uncerUp": cl68upstat, "central": bestfit}
            else:
                resultsXS['SM_125_mass4l_'+obsbin.replace('r','').replace('Bin0','')+'_genbin0'] = {"uncerDn": -1.0*cl68dn, "uncerUp": cl68up, "central": bestfit}
                resultsXS['SM_125_mass4l_'+obsbin.replace('r','').replace('Bin0','')+'_genbin0_statOnly'] = {"uncerDn": -1.0*cl68dnstat, "uncerUp": cl68upstat, "central": bestfit}
        else:
            resultsXS['SM_125_'+obsName.replace(' ','_')+'_genbin'+obsbin.replace('SigmaBin','')]                       = {"uncerDn": -1.0*cl68dn, "uncerUp": cl68up, "central": bestfit}
            resultsXS['SM_125_'+obsName.replace(' ','_')+'_genbin'+obsbin.replace('SigmaBin','')+'_statOnly']   = {"uncerDn": -1.0*cl68dnstat, "uncerUp": cl68upstat, "central": bestfit}

        # Create output directory if it does not exits
        OutputPath = LHScanPlots.format(year = opt.ERA, obsName = obsName.replace(' ','_'))
        GetDirectory(OutputPath)

        c.SaveAs(OutputPath+"/lhscan_"+obsName.replace(' ','_')+"_"+obsbin+".pdf")
        c.SaveAs(OutputPath+"/lhscan_"+obsName.replace(' ','_')+"_"+obsbin+".png")

        # FIXME: currently its sending the modules to the python directory.
        #        we should fix this. Instead of sending this to python send
        #        to some other temp directory then import at appropriate place
        if (obsName=="mass4l"):
            if (obsbin=="SigmaBin0"):
                with open(datacardInputs+'/resultsXS_LHScan_mass4l_v3.py', 'w') as f:
                    f.write('resultsXS = '+str(resultsXS)+' \n')
            else:
                with open(datacardInputs+'/resultsXS_LHScan_mass4l_v2.py', 'w') as f:
                    f.write('resultsXS = '+str(resultsXS)+' \n')
        else:
            with open(datacardInputs+'/resultsXS_LHScan_'+obsName.replace(' ','_')+'_v3.py', 'w') as f:
                f.write('resultsXS = '+str(resultsXS)+' \n')
