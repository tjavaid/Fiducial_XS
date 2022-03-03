from ROOT import *
import ROOT
from array import array
#import shutil
#import yaml
#import pprint
#from lib.util.RootAttributeTranslator import RootAttributeTranslator
#from lib.util.Logger import Logger
#from lib.util.UniversalConfigParser import UniversalConfigParser
#from lib.plotting.RootPlotters import PlotPolisher,SimplePlotter
#from lib.plotting.RootPlottersBase import RootPlottersBase
#from lib.plotting.FitResultReader import FitResultReader
#from lib.util.MiscTools import AreSame
#import yaml
#import os
#import optparse
from optparse import *
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time, copy
#from math import *
#from decimal import *
acc_ggH_powheg = {}
pdfunc_ggH_powheg = {}
qcdunc_ggH_powheg = {}
#_temp = __import__('accUnc_'+obsName, globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
_temp = __import__('accUnc_mass4l', globals(), locals(), ['acc','pdfUncert','qcdUncert'], -1)
acc_ggH_powheg = _temp.acc
pdfunc_ggH_powheg = _temp.pdfUncert
qcdunc_ggH_powheg = _temp.qcdUncert

grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)

### Define function for parsing options
def parseOptions():

    global opt, args

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('',   '--setLog', action='store_true', dest='SETLOG', default=False, help='set plot to log scale y, default is False')
    parser.add_option('',   '--unblind', action='store_true', dest='UNBLIND', default=False, help='Use real data')
    parser.add_option('-a',   '--name_append',dest='NAME_APPEND',type='string',default='', help='Add string to the output file name.')
    parser.add_option('-c',   '--central_line',dest='CENTRAL_LINE',type='string',default='theory_hres1,theory_hres2', help='Add central line of the graph. Add comma separated list of graph names w/o spaces.')
    #parser.add_option('-c',   '--central_line', action='store_true', dest='CENTRAL_LINE', default=False, help='Add central line of the graph.')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
global opt, args
parseOptions()
sys.argv = grootargs



def DrawErrorBand(graph):
    isErrorBand = graph.GetErrorYhigh(0) != -1 and graph.GetErrorYlow(0) != -1
    npoints     = graph.GetN()

    if not isErrorBand:
        graph.Draw("l same")
        return

    # Declare individual TGraph objects used in drawing error band
    central, min, max = ROOT.TGraph(), ROOT.TGraph(), ROOT.TGraph()
    shapes = []
    for i in range((npoints-1)*4):
        shapes.append(ROOT.TGraph())

    # Set ownership of TGraph objects
    ROOT.SetOwnership(central, False)
    ROOT.SetOwnership(    min, False)
    ROOT.SetOwnership(    max, False)
    for shape in shapes:
        ROOT.SetOwnership(shape, False)

    # Get data points from TGraphAsymmErrors
    x, y, ymin, ymax = [], [], [], []
    for i in range(npoints):
        tmpX, tmpY = ROOT.Double(0), ROOT.Double(0)
        graph.GetPoint(i, tmpX, tmpY)
        x.append(tmpX)
        y.append(tmpY)
        ymin.append(tmpY - graph.GetErrorYlow(i))
        ymax.append(tmpY + graph.GetErrorYhigh(i))

    # Fill central, min and max graphs
    for i in range(npoints):
        central.SetPoint(i, x[i], y[i])
        min.SetPoint(i, x[i], ymin[i])
        max.SetPoint(i, x[i], ymax[i])

    # Fill shapes which will be shaded to create the error band
    for i in range(npoints-1):
        for version in range(4):
            shapes[i+(npoints-1)*version].SetPoint((version+0)%4, x[i],   ymax[i])
            shapes[i+(npoints-1)*version].SetPoint((version+1)%4, x[i+1], ymax[i+1])
            shapes[i+(npoints-1)*version].SetPoint((version+2)%4, x[i+1], ymin[i+1])
            shapes[i+(npoints-1)*version].SetPoint((version+3)%4, x[i],   ymin[i])

    # Set attributes to those of input graph
    central.SetLineColor(graph.GetLineColor())
    central.SetLineStyle(graph.GetLineStyle())
    central.SetLineWidth(graph.GetLineWidth())
    min.SetLineColor(graph.GetLineColor())
    min.SetLineStyle(graph.GetLineStyle())
    max.SetLineColor(graph.GetLineColor())
    max.SetLineStyle(graph.GetLineStyle())
    for shape in shapes:
        shape.SetFillColor(graph.GetFillColor())
        shape.SetFillStyle(graph.GetFillStyle())

    # Draw
    for shape in shapes:
        shape.Draw("f same")
    min.Draw("l same")
    max.Draw("l same")
    #central.Draw("l same")
    #min.Draw("same")
    #max.Draw("same")
    #central.Draw("same")
    ROOT.gPad.RedrawAxis()


from tdrStyle import *
setTDRStyle()
ROOT.gROOT.SetBatch(1)
#ROOT.gROOT.ProcessLine(".L tdrstyle.cc")
#from ROOT import setTDRStyle
#ROOT.setTDRStyle(True)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)


    ##7 TeV results
#Info in <TCanvas::Print>: pdf file plots/mass4l_unfoldwith_SM_125_logscale.pdf has been created
#Info in <TCanvas::Print>: png file plots/mass4l_unfoldwith_SM_125_logscale.png has been created
#data [0.945, 0.443, 0.268, 0.236]
#data_hi [0.799, 0.597, 0.379, 0.522]
#data_lo [0.593, 0.384, 0.22, 0.236]
#ggH powheg15+JHUgen + XH [0.9447893914654486, 0.4410694071037717, 0.26703873710939235, 0.23668124725228468]
#ggH_minloHJJ [0.9244994058503646, 0.4341011248607527, 0.25969732537228013, 0.23070095561733178]
#theory precent. up 0.10840894797 theory precent. down 0.10840894797
#XH [0.11768110767556389, 0.055088206629393115, 0.03296967966907641, 0.029623221377094375]
#modedlep_hi [0.04, 0.02, 0.012, 0.021]
#modeldep_lo [0.032, 0.034, 0.008, 0.002]


##8Tev results
#Info in <TCanvas::Print>: pdf file plots/mass4l_unfoldwith_SM_125.pdf has been created
#Info in <TCanvas::Print>: png file plots/mass4l_unfoldwith_SM_125.png has been created
#data [1.106, 0.542, 0.327, 0.297]
#data_hi [0.433, 0.298, 0.188, 0.27]
#data_lo [0.360, 0.253, 0.151, 0.202]
#ggH powheg15+JHUgen + XH [1.1612803274719998, 0.5404514228356333, 0.32616097488589235, 0.2946679297504741]
#ggH_minloHJJ [1.142925191307387, 0.540319903662999, 0.3173987368242344, 0.28520655082015367]
#theory precent. up 0.107745069493 theory precent. down 0.107912001186
#XH [0.1459092765599878, 0.06854348513284285, 0.04050638580950803, 0.03685940561763695]
#modedlep_hi [0.048, 0.024, 0.015, 0.025]
#modeldep_lo [0.003, 0.025, 0.004, 0.004]

# 13 TEV
#data [2.4788379669189453, 1.2801358699798584, 0.7354721426963806, 0.4610423445701599]
#data_hi [1.482, 1.09, 0.821, 0.841]
#data_lo [1.141, 0.754, 0.556, 0.433]
#ggH powheg15+JHUgen + XH [2.3911110320407434, 1.1218182936724084, 0.6567058702120272, 0.6125868681563076]
#modedlep_hi [0.009, 0.005, 0.006, 0.001]
#modeldep_lo [0.041, 0.02, 0.01, 0.009]
#systematics_hi [0.2816007812489159, 0.1802082129094017, 0.12774975538136962, 0.11572380913191528]
#systematics_lo [0.17819090885900998, 0.0775628777186614, 0.09963433143249378, 0.05871967302361285]

# ICHEP 2016
#data [2.285, 1.202, 0.789, 0.297]
#data_hi [0.741, 0.545, 0.343, 0.388]
#data_lo [0.636, 0.447, 0.278, 0.265]
#modedlep_hi [0.011, 0.007, 0.004, 0.001]
#modeldep_lo [0.052, 0.029, 0.017, 0.008]
#systematics_hi [0.29899331096196785, 0.21218152605728904, 0.08221921916437787, 0.09173330910852397]
#systematics_lo [0.2298847537354316, 0.1502264956657115, 0.06199193495931558, 0.03249615361854386]

#Moriond 17
#data [2.904, 1.182, 0.845, 0.877]
#data_hi [0.548, 0.331, 0.217, 0.342]
#data_lo [0.489, 0.295, 0.189, 0.285]
#ggH_powheg [2.718512455038266, 1.2717211530490333, 0.7599694790398797, 0.6868218229493533]
#NNLO ggH_powheg_hi [0.14272007854771973, 0.06676932013730273, 0.03991408973407199, 0.03603666867634499]
#NNLO ggH_powheg_lo [0.14272007854771973, 0.06676932013730273, 0.03991408973407199, 0.03603666867634499]
#modedlep_hi [0.002, 0.001, 0.001, 0.002]
#modeldep_lo [0.014, 0.005, 0.003, 0.008]
#systematics_hi [0.27152900397563445, 0.11331372379372237, 0.05467174773134663, 0.14007141035914508]
#systematics_lo [0.21540659228538014, 0.09869650449737302, 0.03867815921162749, 0.09967948635501683]

# for mH=125.09
# 7 TeV: mass4l SigmaBin0 0.557155 + 0.667895 - 0.439505 (stat.) + 0.21121 - 0.059803 (sys.)
# 8 TeV: mass4l SigmaBin0 1.11151 + 0.40879 - 0.34806 (stat.) + 0.136224 - 0.090408 (sys.)
# 13 TeV: mass4l SigmaBin0 2.91531 + 0.47874 - 0.44156 (stat.) + 0.277277 - 0.242277 (sys.)


# Moriond 2019 (Feb 25th unblinding)
#data [2.851, 1.362, 0.809, 0.719]
#data_hi [0.279, 0.179, 0.11, 0.157]
#data_lo [0.266, 0.164, 0.102, 0.138]
#systematics_hi [0.14559189537882947, 0.06939740629158987, 0.03583294573433784, 0.06255397669213368]
#systematics_lo [0.13701094846763162, 0.0505964425626941, 0.03154362059117497, 0.04024922359499621]

# ucorrelate lepton sys
#data [2.836, 1.328, 0.783, 0.721]
#data_hi [0.306, 0.189, 0.116, 0.173]
#data_lo [0.286, 0.173, 0.104, 0.15]
#systematics_hi [0.19356394292326246, 0.09734988443752772, 0.057052607302383644, 0.09588013350011565]
#systematics_lo [0.17527121840165308, 0.08074651695274539, 0.04232020793899764, 0.07124605252222749]

# Mar 7 update, with real SF and new calibrations for 2018
#data [2.755, 1.296, 0.774, 0.683]
#data_hi [0.302, 0.186, 0.117, 0.166]
#data_lo [0.275, 0.169, 0.104, 0.143]
#systematics_hi [0.19453277358841103, 0.09814275317108238, 0.0590592922409336, 0.09226050075736637]
#systematics_lo [0.16365818036383029, 0.0778524244966077, 0.04449719092257397, 0.0676239602507868]

# Mar14 update, actually put in the scale factor? and fix 2018 lumi
#data [2.78, 1.308, 0.766, 0.701]
#data_hi [0.302, 0.187, 0.116, 0.17]
#data_lo [0.282, 0.17, 0.102, 0.147]
#systematics_hi [0.18968131167829896, 0.09679359482941007, 0.05878775382679627, 0.09346657156438343]
#systematics_lo [0.17261228229763947, 0.07809609465267778, 0.03959797974644664, 0.068622153857191]

# Actually update eff. sys.
#data [2.733, 1.295, 0.749, 0.692]
#data_hi [0.33, 0.19, 0.109, 0.188]
#data_lo [0.292, 0.176, 0.098, 0.16]
#stat_hi [0.231, 0.0, 0.0, 0.0]
#stat_lo [-0.22, 0.0, 0.0, 0.0]
#sys_hi [0.23566713814191406, 0.10552724766618335, 0.047717921161760574, 0.12547509713086497]
#sys_lo [0.19199999999999998, 0.09206519429187122, 0.03637306695894644, 0.09600000000000002]

# paper HIG-19-001
#data [2.837, 1.314, 0.778, 0.757]
#data_hi [0.345, 0.203, 0.104, 0.181]
#data_lo [0.307, 0.194, 0.097, 0.163]
#systematics_hi [0.25803875677889937, 0.12868566353716332, 0.028565713714171354, 0.11472140166507727]
#systematics_lo [0.21412379596859382, 0.12423767544509196, 0.02393741840717166, 0.09963934965664922]
#stat_hi [0.229]
#stat_lo [-0.22]



graphs_list = {

    'dummy':{
        'x_values': [6,14],
        'central' : [0.0,6.0],
        'uncerUp' : [0.0,0.0],
        'uncerDn' : [0.0,0.0],
        'setup' : {'color': kWhite, 'linestyle': kWhite ,'linewidth': 0, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 0.0, 'draw_opt' : "L" },
        'legend' : {'text': "Dummy", 'draw_opt' : 'EP'}
            },

    'measured':{
        'x_values': [7,8,13],
        #'central' : [0.557, 1.111, 2.733],
        #'central' : [0.557, 1.111, 2.837],
        'central' : [0.557, 1.111, 2.835],
        #'uncerUp' : [0.700, 0.431, 0.330],
        #'uncerUp' : [0.700, 0.431, 0.345],
        'uncerUp' : [0.700, 0.431, 0.344],
        #'uncerDn' : [0.444,0.360, 0.292],
        #'uncerDn' : [0.444,0.360, 0.307],
        'uncerDn' : [0.444,0.360, 0.307],
        'setup' : {'color': kBlack, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "PZ" },
        #'legend' : {'text': "Data (stat. #oplus sys. unc.)", 'draw_opt' : 'EP'}
        #'legend' : {'text': "Data (stat #oplus sys unc.)", 'draw_opt' : 'EP'}
        'legend' : {'text': "Data (stat #oplus syst)", 'draw_opt' : 'EP'}
            },

    'measured_sys':{
        'x_values': [7,8,13],
        #'central' : [0.557, 1.111, 2.733],
        #'central' : [0.557, 1.111, 2.837],
        'central' : [0.557, 1.111, 2.835],
        #'uncerUp' : [0.211,0.136224, 0.236],
        #'uncerUp' : [0.211,0.136224, 0.25803875677889937],
        'uncerUp' : [0.211,0.136224, 0.25670021425779915],
        #'uncerDn' : [0.059,0.090408, 0.192],
        #'uncerDn' : [0.059,0.090408, 0.21412379596859382],
        'uncerDn' : [0.059,0.090408, 0.21412379596859382],
        'setup' : {'color': kRed, 'linestyle': kSolid ,'linewidth': 4, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "PZ" },
        'legend' : {'text': "Systematic uncertainty", 'draw_opt' : 'L'}
            },

    'model_dependancy':{
        'x_values': [7,8,13],
        #'central' : [0.557, 1.111, 2.733],
        #'central' : [0.557, 1.111, 2.837],
        'central' : [0.557, 1.111, 2.835],
        #'uncerUp' : [0.00, 0.00, 0.002 ],
        'uncerUp' : [0.00, 0.00, 0.0 ],
        #'uncerDn' : [0.00, 0.00, 0.014 ],
        'uncerDn' : [0.00, 0.00, 0.00 ],
        'setup' : {'color': kGray, 'linestyle': kSolid ,'linewidth': 0, 'fillstyle' : 1001, 'draw_opt' : "E2"},
        'legend' : {'text': "Model dependence", 'draw_opt' : 'f'}
            },

    'theory_hres1':{
        'x_values': [6,7,8,9],
        'central' : [0.7743,1.0309,1.2769,1.512],
        'uncerUp' : [0.0407,0.0542,0.0672,0.0795],
        'uncerDn' : [0.0407,0.0542,0.0672,0.0795],
        #'setup' : {'color': kAzure+2, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        #'setup' : {'color': kMagenta+2, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        #'setup' : {'color': kCyan, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        'setup' : {'color': kGreen+1, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "E2" },


        #'legend' : {'text': "Standard model (m_{H} = 125.09 GeV, N^{3}LO gg#rightarrow H)", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model (6-9 TeV at m_{H} = 125.0 GeV)  ", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model (m_{H} = 125.0 GeV)  ", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model (m_{H} = 125.00 GeV)  ", 'draw_opt' : 'fl'}
        'legend' : {'text': "Standard model (m_{H} = 125.00 GeV, LHC Run 1)  ", 'draw_opt' : 'fl'}
            },
# acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']
    'theory_hres2':{
        'x_values': [12,13,14],
        #'central' : [2.471,2.761,3.084],
        #'central' : [2.471*(acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']/acc_ggH_powheg['ggH_powheg_JHUgen_125_4l_mass4l_genbin0'])*(48313.8/48520)*(0.0271116/0.02641),2.850896578564893,3.084*(acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']/acc_ggH_powheg['ggH_powheg_JHUgen_125_4l_mass4l_genbin0'])*(48313.8/48520)*(0.0271116/0.02641)],  # treatment for 125.38 GeV
        #'central' : [2.471*(acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']/acc_ggH_powheg['ggH_powheg_JHUgen_125_4l_mass4l_genbin0'])*(48313.8/48520)*(0.0271116/0.02641),2.841764080207176,3.084*(acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']/acc_ggH_powheg['ggH_powheg_JHUgen_125_4l_mass4l_genbin0'])*(48313.8/48520)*(0.0271116/0.02641)],  # treatment for 125.38 GeV
        'central' : [2.471*(acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']/acc_ggH_powheg['ggH_powheg_JHUgen_125_4l_mass4l_genbin0'])*(48313.8/48520)*(0.0271116/0.02641),2.841764080207176,3.084*(acc_ggH_powheg['ggH_powheg_JHUgen_125.38_4l_mass4l_genbin0']/acc_ggH_powheg['ggH_powheg_JHUgen_125_4l_mass4l_genbin0'])*(48313.8/48520)*(0.0271116/0.02641)],  # treatment for 125.38 GeV
        #'uncerUp' : [0.126,0.144,0.157],
        #'uncerUp' : [0.126,0.14932688761505214,0.157],  # 13 TeV corresponds to 125.38
        'uncerUp' : [0.126*(0.14932688761505214/0.144),0.14932688761505214,0.157*(0.14932688761505214/0.144)],  # 13 TeV corresponds to 125.38, rest scaled w.r.t NNLOPS
        #'uncerDn' : [0.126,0.144,0.157],
        'uncerDn' : [0.126*(0.14932688761505214/0.144),0.14932688761505214,0.157*(0.14932688761505214/0.144)], # # 13 TeV corresponds to 125.38, scaled w.r.t NNLOPS
        'setup' : {'color': kAzure+2, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        #'legend' : {'text': "Standard model (m_{H} = 125.09 GeV, N^{3}LO gg#rightarrow H)", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model (12-14 TeV at m_{H} = 125.38 GeV)  ", 'draw_opt' : 'fl'}
        #'legend' : {'text': "Standard model (m_{H} = 125.38 GeV)  ", 'draw_opt' : 'fl'}
        'legend' : {'text': "Standard model (m_{H} = 125.38 GeV, LHC Run 2)  ", 'draw_opt' : 'fl'}
            },


}


#create asymetric graphs from 'graphs'
#v_data_hi_allunc = TVectorD(len(data_hi_allunc), array('d',[data_hi_allunc[i] for i in range(len(data_hi_allunc))]))
#for gr in graphs_list.keys():
for gr_key, gr_setup in graphs_list.iteritems():
    #create arrays from lists
    v_x_values = TVectorD(len(gr_setup['x_values']), array('d',[gr_setup['x_values'][i] for i in range(len(gr_setup['x_values']))]))
    if gr_key.startswith('model_dependancy'):
        v_x_valuesUp = v_x_valuesDn = TVectorD(len(gr_setup['x_values']), array('d',[0.2 for i in range(len(gr_setup['x_values']))]))
    else:
        v_x_valuesUp = v_x_valuesDn = TVectorD(len(gr_setup['x_values']), array('d',[0.0 for i in range(len(gr_setup['x_values']))]))

    v_central = TVectorD(len(gr_setup['central']), array('d',[gr_setup['central'][i] for i in range(len(gr_setup['central']))]))
    v_uncerUp = TVectorD(len(gr_setup['uncerUp']), array('d',[gr_setup['uncerUp'][i] for i in range(len(gr_setup['uncerUp']))]))
    v_uncerDn = TVectorD(len(gr_setup['uncerDn']), array('d',[gr_setup['uncerDn'][i] for i in range(len(gr_setup['uncerDn']))]))
    gr_setup['graph'] = TGraphAsymmErrors(v_x_values,v_central,v_x_valuesDn,v_x_valuesUp, v_uncerDn,v_uncerUp)
    if not gr_key.startswith("measured"):
        gr_setup['graph'].SetFillStyle(gr_setup['setup']['fillstyle']);
        gr_setup['graph'].SetFillColor(gr_setup['setup']['color'])
        gr_setup['graph'].SetLineColor(gr_setup['setup']['color'])
        #gr_setup['graph'].SetLineColor(kBlack)
        gr_setup['graph'].SetLineStyle(gr_setup['setup']['linestyle'])
        gr_setup['graph'].SetLineWidth(gr_setup['setup']['linewidth'])
    else:
        gr_setup['graph'].SetMarkerColor(gr_setup['setup']['color'])
        gr_setup['graph'].SetLineColor(gr_setup['setup']['color'])
        gr_setup['graph'].SetLineWidth(gr_setup['setup']['linewidth'])
        gr_setup['graph'].SetMarkerStyle(gr_setup['setup']['markerstyle'])
        gr_setup['graph'].SetMarkerSize(gr_setup['setup']['markersize'])
        if gr_key.endswith("sys"):
            gr_setup['graph'].SetMarkerColor(graphs_list['measured']['setup']['color'])
            gr_setup['graph'].SetLineColor(gr_setup['setup']['color'])


#create Canvas
print v_central,v_uncerUp,v_uncerDn
c = TCanvas("c","xs_vs_sqrts", 1000, 1000)
if (opt.SETLOG): c.SetLogy(1)
else: c.SetLogy(0)
c.SetBottomMargin(0.15)
c.SetRightMargin(0.06)
c.SetLeftMargin(0.18)

move_left = -0.05
move_down = 0.52
move_down = 0.50
move_left = -0.02
move_down = 0.03
move_down = 0.06
#move_down = 0.606  # test

legend = TLegend(.20-move_left,.65-move_down,.58-move_left,0.9-move_down )
legend.SetTextSize(0.03)
legend.SetFillStyle(0)
legend.SetBorderSize(0)


v_x_values = TVectorD(len(graphs_list['theory_hres1']['x_values']), array('d',[graphs_list['theory_hres1']['x_values'][i] for i in range(len(graphs_list['theory_hres1']['x_values']))]))
v_central = TVectorD(len(graphs_list['theory_hres1']['central']), array('d',[graphs_list['theory_hres1']['central'][i] for i in range(len(graphs_list['theory_hres1']['central']))]))
tmp_graph = TGraph(v_x_values,v_central)
tmp_graph.SetLineColor(graphs_list['theory_hres1']['setup']['color'])
tmp_graph.SetLineStyle(kDashed)
tmp_graph.SetLineWidth(3)

v_x_values2 = TVectorD(len(graphs_list['theory_hres2']['x_values']), array('d',[graphs_list['theory_hres2']['x_values'][i] for i in range(len(graphs_list['theory_hres2']['x_values']))]))
v_central2 = TVectorD(len(graphs_list['theory_hres2']['central']), array('d',[graphs_list['theory_hres2']['central'][i] for i in range(len(graphs_list['theory_hres2']['central']))]))
tmp_graph2 = TGraph(v_x_values2,v_central2)
tmp_graph2.SetLineColor(graphs_list['theory_hres2']['setup']['color'])
tmp_graph2.SetLineStyle(kDashed)
tmp_graph2.SetLineWidth(3)


plots_order = [
    'dummy',
    'theory_hres1',
    'theory_hres2',
    #'model_dependancy',
    'measured',
    'measured_sys'
    ]

#for i_plot in range(len(plots_order)):

for i_plot, plot_name in enumerate(plots_order):
    the_plot = graphs_list[plot_name]

    the_plot['graph'].GetYaxis().SetTitleOffset(1.0)
    the_plot['graph'].GetXaxis().SetTitle("#sqrt{s} (TeV) ")
    the_plot['graph'].GetYaxis().SetTitle("#sigma_{fid} (fb)")

    the_plot['graph'].GetXaxis().SetRangeUser(0,15)

    if opt.SETLOG:
        the_plot['graph'].GetYaxis().SetRangeUser(0.1,5)
    else:
        the_plot['graph'].GetYaxis().SetRangeUser(-0.3,6.4)

    if plot_name=='model_dependancy':
        g = the_plot['graph']
        print(g)
        the_plot['graph'].SetLineColor(kBlack)
        the_plot['graph'].SetLineStyle(the_plot['setup']['linestyle'])
        the_plot['graph'].SetLineWidth(the_plot['setup']['linewidth'])
        #tmp_graph.Draw('l same')


    draw_opt = the_plot['setup']['draw_opt']

    if i_plot==0:
        the_plot['graph'].Draw('A'+draw_opt)
        if plot_name.startswith('theory'):
            DrawErrorBand(the_plot['graph'])
        tmp_graph.Draw('l same')
        tmp_graph2.Draw('l same')

    else:
        if plot_name.startswith('theory'):
            DrawErrorBand(the_plot['graph'])
        else:
            the_plot['graph'].Draw(draw_opt+'same')


graphs_list['theory_hres1']['graph'].SetLineStyle(kDashed)
graphs_list['theory_hres1']['graph'].SetLineWidth(3)

graphs_list['theory_hres2']['graph'].SetLineStyle(kDashed)
graphs_list['theory_hres2']['graph'].SetLineWidth(3)

legend.AddEntry(graphs_list['measured']['graph'], graphs_list['measured']['legend']['text'], graphs_list['measured']['legend']['draw_opt'])
legend.AddEntry(graphs_list['measured_sys']['graph'], graphs_list['measured_sys']['legend']['text'], graphs_list['measured_sys']['legend']['draw_opt'])
#legend.AddEntry(graphs_list['model_dependancy']['graph'], graphs_list['model_dependancy']['legend']['text'], graphs_list['model_dependancy']['legend']['draw_opt'])
legend.AddEntry(graphs_list['theory_hres1']['graph'], graphs_list['theory_hres1']['legend']['text'], graphs_list['theory_hres1']['legend']['draw_opt'])
legend.AddEntry(graphs_list['theory_hres2']['graph'], graphs_list['theory_hres2']['legend']['text'], graphs_list['theory_hres2']['legend']['draw_opt'])
#legend.AddEntry(graphs_list['dummy']['graph'], "LHC HXSWG YR4, m_{H}=125.09 GeV", "")
#legend.AddEntry(graphs_list['dummy']['graph'], "LHC HXSWG YR4, m_{H}=125.38 GeV", "")

legend.SetShadowColor(0);
legend.SetFillColor(0);
legend.SetLineColor(0);
legend.Draw()


latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.45*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right
#latex2.DrawLatex(0.94, 0.94,"5.1 fb^{-1} (7 TeV), 19.7 fb^{-1} (8 TeV), 137.1 fb^{-1} (13 TeV) ")
latex2.DrawLatex(0.94, 0.94,"5.1 fb^{-1} (7 TeV), 19.7 fb^{-1} (8 TeV), 137 fb^{-1} (13 TeV) ")
latex2.SetTextSize(0.8*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right
latex2.DrawLatex(c.GetLeftMargin()+0.05, 0.85, "CMS")  #preliminary version


latex2.SetTextSize(0.7*c.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
#latex2.DrawLatex(c.GetLeftMargin()+0.175, 0.85, "Preliminary")

latex2.SetTextSize(0.7*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11)
latex2.DrawLatex(c.GetLeftMargin()+0.3, 0.22, "pp #rightarrow (H #rightarrow 4l) + X")
latex2.SetTextSize(0.68*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11)


if (opt.SETLOG): set_log = '_logscale'
else: set_log = ''
if (opt.NAME_APPEND): name_append = '_'+opt.NAME_APPEND
else: name_append = ''
for ext in ['.pdf','.png','.root','.C']:
    #c.SaveAs('plots/xs_vs_sqrts'+set_log+name_append+ext)
    #c.SaveAs('plots_05082020/xs_vs_sqrts'+set_log+name_append+ext)
    #c.SaveAs('plots_16102020/xs_vs_sqrts'+set_log+name_append+ext)
    #c.SaveAs('plots_20102020/xs_vs_sqrts'+set_log+name_append+ext)
    c.SaveAs('plots_03122020/xs_vs_sqrts'+set_log+name_append+ext)

