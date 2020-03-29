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
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time, copy
#from math import *
#from decimal import *

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
    parser.add_option('-c',   '--central_line',dest='CENTRAL_LINE',type='string',default='theory_hres', help='Add central line of the graph. Add comma separated list of graph names w/o spaces.')
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

#sqrts = [7,8,13,13.5,14]
sqrts = [6,7,8,9,10,11,12,13,14]

#1.106 + 0.433 - 0.360

graphs_list = {
    'measured':{

        #'central' : [0.555, 1.106],
        #'uncerUp' : [0.701, 0.433],
        #'uncerDn' : [0.446,0.360],
        #'x_values': sqrts[1:3],
        'x_values': [7,8,13],

        'central' : [0.555, 1.106, 2.479],
        'uncerUp' : [0.701, 0.433, 1.482],
        'uncerDn' : [0.446,0.360, 1.141],

        'setup' : {'color': kBlack, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "PZ" },
        #'legend' : {'text': "Asimov Data (stat.#oplussys. unc.)", 'draw_opt' : 'EP'}
        'legend' : {'text': "Data (stat. #oplus sys. unc.)", 'draw_opt' : 'EP'}

            },

    'measured_sys':{
        #'central' : [0.555, 1.106],
        #'uncerUp' : [0.212,0.1392444],
        #'uncerDn' : [0.061,0.0958697],
        'central' : [0.555, 1.106, 2.479],
        'uncerUp' : [0.212,0.1392444, 0.282],
        'uncerDn' : [0.061,0.0958697, 0.178],


        #'x_values': sqrts[1:3],
        'x_values': [7,8,13],

        'setup' : {'color': kRed, 'linestyle': kSolid ,'linewidth': 4, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2,
                   'draw_opt' : "PZ"
                    #'draw_opt' : "P"
                       },
        'legend' : {'text': "Systematic uncertainty", 'draw_opt' : 'L'}
            },

    'model_dependancy':{
        #'central' : [0.555, 1.106],
        #'uncerUp' : [0.016, 0.079],  #FIXME
        #'uncerDn' : [0.019, 0.023],   #FIXME
        'central' : [0.555, 1.106, 2.479],
        'uncerUp' : [0.016, 0.079, 0.009 ],  #FIXME
        'uncerDn' : [0.019, 0.023, 0.041 ],   #FIXME




        #'x_values': sqrts[1:3],
        'x_values': [7,8,13],
        'setup' : {'color': kGray, 'linestyle': kSolid ,'linewidth': 0, 'fillstyle' : 1001, 'draw_opt' : "E2"},
        'legend' : {'text': "Model dependence", 'draw_opt' : 'f'}
            },

    #'measured':{
        #'central' : [0.945, 1.106],
        #'uncerUp' : [0.799, 0.433],
        #'uncerDn' : [0.593,0.360],
        #'x_values': sqrts[:2],
        #'setup' : {'color': kBlack, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "EP" },
        #'legend' : {'text': "Asimov Data (stat.#oplussys. unc.)", 'draw_opt' : 'EP'}
            #},

    #'measured_sys':{
        #'central' : [0.945, 1.106],
        #'uncerUp' : [0.799*0.26, 1.1060.26],  #FIXME
        #'uncerDn' : [0.593*0.30, 0.360*0.30],  #FIXME
        #'x_values': sqrts[:2],
        #'setup' : {'color': kRed, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "EP" },
        #'legend' : {'text': "systematic uncertainty", 'draw_opt' : 'L'}
            #},

    #'model_dependancy':{
        #'central' : [0.945, 1.106],
        #'uncerUp' : [0.041, 0.08],  #FIXME
        #'uncerDn' : [0.034, 0.02],   #FIXME

        #'x_values': sqrts[:2],
        #'setup' : {'color': kGray, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 1001, 'draw_opt' : "E2" },
        #'legend' : {'text': "model dep. uncertainty", 'draw_opt' : 'f'}
            #},

    'theory_powheg_nlo':{
        'central' : [0.9344896537,1.1558231007,1.3213441338,1.5227727109,1.7468640848,2.0134473995,2.3201324158,2.6850344998],
        'uncerUp' : [0.2087455195,0.2511676183,0.2800160931,0.3171503996,0.3558498901,0.4056180449,0.4609648732,0.5263551199],
        'uncerDn' : [0.1652791729,0.1993755464,0.222997893,0.2529829028,0.285252785,0.3256909875,0.3713465352,0.4256995284],

        'x_values': sqrts,
        'setup' : {'color': kAzure, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        'legend' : {'text': "gg#rightarrowH (powheg+JHUgen) + XH", 'draw_opt' : 'f'}
            },


    'theory_powheg_nlo_old_qcd_unc':{
        #'central' : [0.9344896537,0.9344896537,1.16128033,1.3213441338,1.5227727109,1.7468640848,2.0134473995,2.3201324158,2.6850344998],
        #'uncerUp' : [0.0993947982,0.0993947982,0.115716668,0.1397039116,0.16147756,0.1861647573,0.2159319844,0.2506933504,0.2925030563],
        #'uncerDn' : [0.0993947982,0.0993947982,0.115886197,0.1397039116,0.16147756,0.1861647573,0.2159319844,0.2506933504,0.2925030563],
                #log in x-axis
        #'central' : [0.9447893915,1.1612803275,1.3684735774,1.6132105053,1.8621253927,2.1281471253,2.4030857826,2.6963625775],
        #'uncerUp' : [0.0818997193,0.10835918,  0.1345550593,0.1762970074,0.226366083, 0.2888757426,0.3635459369,0.4547397944],
        #'uncerDn' : [0.0818997193,0.10835918,  0.1345550593,0.1762970074,0.226366083, 0.2888757426,0.3635459369,0.4547397944],

        'central' : [0.9447893915,1.1612803275,1.312383667, 1.515431886, 1.7431139667,2.0134934464,2.3255842596,2.6963625775],
        'uncerUp' : [0.0907807792,0.1104055521,0.1224402149,0.1414611866,0.1631194054,0.1892284674,0.2196964762,0.2613076797],
        'uncerDn' : [0.0907807792,0.1104055521,0.1224402149,0.1414611866,0.1631194054,0.1892284674,0.2196964762,0.2613076797],



        'x_values': sqrts[1:],
        'setup' : {'color': kAzure, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        #'setup' : {'color': kAzure, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 1001, 'draw_opt' : "E2" },
        #'legend' : {'text': "gg#rightarrowH (powheg+JHUgen) + XH", 'draw_opt' : 'f'}
        'legend' : {'text': "SM (m_{H} = 125 GeV, Powheg)", 'draw_opt' : 'f'}
            },

    'theory_hres':{

        #'central' : [0.9352035054,1.1601508402,1.3302514357,1.5286232837,1.7639903684,2.0366757836,2.3542149114,2.7231965295],
        #'uncerUp' : [0.09211705,  0.107493769, 0.1244555083,0.1427287282,0.1651692988,0.1826472419,0.2066911799,0.2460709227],
        #'uncerDn' : [0.09211705,  0.107493769, 0.1244555083,0.1427287282,0.1651692988,0.1826472419,0.2066911799,0.2460709227],


        #'central' : [0.9352035054,1.1601508402,1.3432989182,1.5456754477,1.7816922019,2.0538136011,2.3761890294,2.7504788633],
        #THE LAST UPDATE FROM TONGGUANG
        #'uncerUp' : [0.0980976005,0.1071872027,0.1355551574,0.1549888128,0.2147715326,0.2003548362,0.2774644179,0.2537638391],
        #'uncerDn' : [0.0959925587,0.1195079681,0.1314165397,0.1478237204,0.1480508619,0.1976827207,0.201648317, 0.2894143224],
        #THE SMOTHING OF THE LAST UPDATE FROM TONGGUANG (KEEPNG 7, 8 TeV POINT AS BEFORE)
        #'uncerUp' : [0.0980976005,0.1071872027,0.133320911,0.1594546194,0.1855883277,0.2117220361,0.2378557445,0.2639894528],
        #'uncerDn' : [0.0959925587,0.1195079681,0.1305643428,0.153941483,0.1773186232,0.2006957634,0.2240729035,0.2474500437],

        #July 3, 2015 from Tonggunag
        #'central' : [0.9296131077,1.1542772766,1.3710401057,1.6200831565,1.8659023766,2.1347070082,2.4143400983,2.6941877636],
        #'uncerUp' : [0.1033459198,0.1234731454,0.1633794322,0.1772845006,0.2036694062,0.2341355431,0.2507078436,0.3229102836],
        #'uncerDn' : [0.1119774028,0.125866129, 0.1398730584,0.1751084984,0.1909252988,0.2246974334,0.2477874013,0.2962510343],

        # correct for the subleading modes at 13 and 14
        'central' : [0.9296131077,1.1542772766,1.3710401057,1.6200831565,1.8659023766,2.1347070082,2.394,2.6718],
        'uncerUp' : [0.1033459198,0.1234731454,0.1633794322,0.1772845006,0.2036694062,0.2341355431,0.24806,0.32022],
        'uncerDn' : [0.1119774028,0.125866129, 0.1398730584,0.1751084984,0.1909252988,0.2246974334,0.24573,0.29379],

        #acceptances from June17 from Tonggunag
        #'central' : [0.9352035054,1.1601508402,1.3432989182,1.5456754477,1.7816922019,2.0538136011,2.3761890294,2.7504788633],
        #'uncerUp' : [0.1044552015,0.1259204483,0.1587770543,0.1707925537,0.193268329, 0.2240531773,0.2461480528,0.3304461905],
        #'uncerDn' : [0.1133572856,0.1282951993,0.1362158755,0.165920269, 0.1812180245,0.2150766775,0.2434398404,0.3034843112],




        #'uncerUp' : [0.0976304532,0.1070259149,0.1351283009,0.1549911778,0.2142866819,0.2005005817,0.278653994, 0.2537441794],
        #'uncerDn' : [0.0976304532,0.1070259149,0.1351283009,0.1549911778,0.2142866819,0.2005005817,0.278653994, 0.2537441794],


        'x_values': sqrts[1:],
        #'setup' : {'color': kMagenta, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 3005, 'draw_opt' : "E2" },
        'setup' : {'color': kAzure, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        #'setup' : {'color': kAzure, 'linestyle': kDashed ,'linewidth': 2, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        #'legend' : {'text': "gg#rightarrowH (powheg+JHUgen) + XH", 'draw_opt' : 'f'}
        'legend' : {'text': "Standard model (m_{H} = 125 GeV)", 'draw_opt' : 'fl'}
            },


    'theory_powheg':{
        'central' : [0.9447893914654486, 1.1612803274719998, 2.6525153442,2.8189481492,2.988291875],

        'uncerUp' : [0.10840894797*0.9447893914654486,0.107745069493*1.1612803274719998,0.2915595831,0.3118857531,0.3325473456],
        'uncerDn' : [0.10840894797*0.9447893914654486,0.107912001186*1.1612803274719998,0.2915595831,0.3118857531,0.3325473456],
        'x_values': sqrts,
        'setup' : {'color': kAzure, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 3004, 'draw_opt' : "E2" },
        'legend' : {'text': "gg#rightarrowH (powheg+JHUgen) + XH", 'draw_opt' : 'f'}
            },

    'theory_minlo' : {
        'central' : [0.9244994058503646, 1.142925191307387, 2.6105898253,2.7743920021,2.9410590898],
        'uncerUp' : [0.10840894797*0.9447893914654486,0.107745069493*1.142925191307387,0.2869512076,0.3069561032,0.3272911197],
        'uncerDn' : [0.10840894797*0.9447893914654486,0.107912001186*1.142925191307387,0.2869512076,0.3069561032,0.3272911197
],
        'x_values': sqrts,
        'setup' : {'color': kOrange, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : 3005, 'draw_opt' : "E2" },

        'legend' : {'text': "gg#rightarrowH (minlo HJJ) + XH", 'draw_opt' : 'f'}
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
c = TCanvas("c","xs_vs_sqrts", 1000, 800)
if (opt.SETLOG): c.SetLogy(1)
else: c.SetLogy(0)
c.SetBottomMargin(0.15)
c.SetRightMargin(0.06)
c.SetLeftMargin(0.2)

    #setup axis
#plot the canvas and interconect the points
move_left = -0.05
move_down = 0.52
move_down = 0.50
#legend = TLegend(.52-move_left,.68-move_down ,.9-move_left,0.95-move_down )
#legend = TLegend(.57-move_left,.68-move_down ,.9-move_left,0.95-move_down )
#legend = TLegend(.42-move_left,.68-move_down ,.9-move_left,0.95-move_down )
#upper left
move_left = -0.02
#move_down = 0.52
move_down = 0.03
move_down = 0.06#for adding "CMS Preliminary" tag
#move_down = 0.09#for adding "CMS Preliminary" tag v1


legend = TLegend(.22-move_left,.65-move_down,.6-move_left,0.9-move_down )

legend.SetTextSize(0.03)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
plots_order = [
    #'theory_powheg_nlo',
    'theory_hres',
    #'theory_powheg_nlo_old_qcd_unc',

    #'theory_powheg',
    #'theory_minlo',
    'model_dependancy',
    'measured',
    'measured_sys'
    ]

if opt.CENTRAL_LINE:
    for plot_name in opt.CENTRAL_LINE.split(','):
        v_x_values = TVectorD(len(graphs_list[plot_name]['x_values']), array('d',[graphs_list[plot_name]['x_values'][i] for i in range(len(graphs_list[plot_name]['x_values']))]))
        v_central = TVectorD(len(graphs_list[plot_name]['central']), array('d',[graphs_list[plot_name]['central'][i] for i in range(len(graphs_list[plot_name]['central']))]))
        tmp_graph = TGraph(v_x_values,v_central)
        tmp_graph.SetLineColor(graphs_list[plot_name]['setup']['color'])
        tmp_graph.SetLineStyle(kDashed)
        tmp_graph.SetLineWidth(3)
        tmp_graph.Draw('l same')

#for i_plot in range(len(plots_order)):

for i_plot, plot_name in enumerate(plots_order):
    the_plot = graphs_list[plot_name]

    the_plot['graph'].GetYaxis().SetTitleOffset(1.0)
    the_plot['graph'].GetXaxis().SetTitle("#sqrt{s} (TeV) ")
    #the_plot['graph'].GetXaxis().SetTitle("sssss")
    the_plot['graph'].GetYaxis().SetTitle("#sigma_{fid} [fb]")
    #the_plot['graph'].GetYaxis().SetTitle("#sigma_{fid.}^{pp #rightarrow H(4l) + anything} [fb]")


    the_plot['graph'].GetXaxis().SetRangeUser(0,15)

    if opt.SETLOG:
        #the_plot['graph'].GetYaxis().SetRangeUser(0.2,5)
        the_plot['graph'].GetYaxis().SetRangeUser(0.1,5)
    else:
        #the_plot['graph'].GetYaxis().SetRangeUser(0,3.2)
        the_plot['graph'].GetYaxis().SetRangeUser(0,3.49)
        #the_plot['graph'].GetYaxis().SetRangeUser(-0.05,3.99)
        the_plot['graph'].GetYaxis().SetRangeUser(-0.1,6.0)

    if plot_name=='model_dependancy':
        g = the_plot['graph']
        print(g)
        #print ('Before change:',g.GetFillStyle(), g.GetLineColor(), g.GetLineStyle())
        the_plot['graph'].SetLineColor(kBlack)
        the_plot['graph'].SetLineStyle(the_plot['setup']['linestyle'])
        the_plot['graph'].SetLineWidth(the_plot['setup']['linewidth'])
        #print ('Before change:',g.GetFillStyle(), g.GetLineColor(), g.GetLineStyle())
        tmp_graph.Draw('l same')




    draw_opt = the_plot['setup']['draw_opt']

    if i_plot==0:
        the_plot['graph'].Draw('A'+draw_opt)
        if plot_name.startswith('theory'):
            DrawErrorBand(the_plot['graph'])
        #the_plot['graph'].Draw('E2same')
        #tmp_graph.Draw('l same')
    else:
        #the_plot['graph'].Draw('E2same')
        if plot_name.startswith('theory'):
            DrawErrorBand(the_plot['graph'])
        else:
            the_plot['graph'].Draw(draw_opt+'same')


    #legend.AddEntry(the_plot['graph'], the_plot['legend']['text'], the_plot['legend']['draw_opt'])
    # change in ditionary....




graphs_list['theory_hres']['graph'].SetLineStyle(kDashed)
graphs_list['theory_hres']['graph'].SetLineWidth(3)
#legend.AddEntry(graphs_list['theory_hres']['graph'], graphs_list['theory_hres']['legend']['text'], graphs_list['theory_hres']['legend']['draw_opt'])

legend.AddEntry(graphs_list['measured']['graph'], graphs_list['measured']['legend']['text'], graphs_list['measured']['legend']['draw_opt'])
legend.AddEntry(graphs_list['measured_sys']['graph'], graphs_list['measured_sys']['legend']['text'], graphs_list['measured_sys']['legend']['draw_opt'])
legend.AddEntry(graphs_list['model_dependancy']['graph'], graphs_list['model_dependancy']['legend']['text'], graphs_list['model_dependancy']['legend']['draw_opt'])
#legend.AddEntry(graphs_list['theory_powheg_nlo']['graph'], graphs_list['theory_powheg_nlo']['legend']['text'], graphs_list['theory_powheg_nlo']['legend']['draw_opt'])
#legend.AddEntry(graphs_list['theory_powheg']['graph'], graphs_list['theory_powheg']['legend']['text'], graphs_list['theory_powheg']['legend']['draw_opt'])
#legend.AddEntry(graphs_list['theory_minlo']['graph'], graphs_list['theory_minlo']['legend']['text'], graphs_list['theory_minlo']['legend']['draw_opt'])
#legend.AddEntry(graphs_list['theory_powheg_nlo_old_qcd_unc']['graph'], graphs_list['theory_powheg_nlo_old_qcd_unc']['legend']['text'], graphs_list['theory_powheg_nlo_old_qcd_unc']['legend']['draw_opt'])
#graphs_list['theory_hres']['graph'].SetLineStyle(kDashed)
#graphs_list['theory_hres']['graph'].SetLineWidth(3)
legend.AddEntry(graphs_list['theory_hres']['graph'], graphs_list['theory_hres']['legend']['text'], graphs_list['theory_hres']['legend']['draw_opt'])
#legend.AddEntry(0, "XH = VBF (powheg) + VH + ttH (pythia)", "")

#legend.SetHeader("pp #rightarrow (H #rightarrow 4l) + anything")

legend.SetShadowColor(0);
legend.SetFillColor(0);
legend.SetLineColor(0);
legend.Draw()



latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right
#latex2.DrawLatex(0.87, 0.95,"19.7 fb^{-1} at #sqrt{s} = 8 TeV")
#latex2.DrawLatex(0.87, 0.95,"L=5.1 fb^{-1} at #sqrt{s} = 7 TeV, 19.7 fb^{-1} at #sqrt{s} = 8 TeV")
#latex2.DrawLatex(0.94, 0.94,"L = 5.1 fb^{-1} at #sqrt{s} = 7 TeV, 19.7 fb^{-1} at #sqrt{s} = 8 TeV")
#latex2.DrawLatex(0.94, 0.94,"5.1 fb^{-1} (7 TeV), 19.7 fb^{-1} (8 TeV)")
latex2.DrawLatex(0.94, 0.94,"5.1 fb^{-1} (7 TeV), 19.7 fb^{-1} (8 TeV), 2.8 fb^{-1} (13 TeV) ")
latex2.SetTextSize(0.9*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right
#latex2.DrawLatex(0.27, 0.85, "CMS")
#latex2.DrawLatex(c.GetLeftMargin(), 0.94, "CMS")  #paper version
#latex2.DrawLatex(c.GetLeftMargin()+0.02, 0.94, "CMS")  #preliminary version
#latex2.DrawLatex(c.GetLeftMargin()+0.03, 0.85, "CMS")  #preliminary version
latex2.DrawLatex(c.GetLeftMargin()+0.05, 0.85, "CMS")  #preliminary version


latex2.SetTextSize(0.7*c.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
#latex2.DrawLatex(c.GetLeftMargin()+0.02, 0.87, "Preliminary")
latex2.DrawLatex(c.GetLeftMargin()+0.165, 0.85, "Preliminary")
#latex2.DrawLatex(c.GetLeftMargin()+0.165, 0.85, "Simulation")



latex2.SetTextSize(0.7*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11)
#latex2.DrawLatex(0.27, 0.8, "pp #rightarrow (H #rightarrow 4l) + anything")
#latex2.DrawLatex(c.GetLeftMargin()+0.05, 0.85, "pp #rightarrow (H #rightarrow 4l) + anything")
#latex2.DrawLatex(c.GetLeftMargin()+0.27, 0.25, "pp #rightarrow (H #rightarrow 4l) + anything")
latex2.DrawLatex(c.GetLeftMargin()+0.39, 0.25, "pp #rightarrow (H #rightarrow 4l) + X")


if (opt.SETLOG): set_log = '_logscale'
else: set_log = ''
if (opt.NAME_APPEND): name_append = '_'+opt.NAME_APPEND
else: name_append = ''
for ext in ['.pdf','.png','.root','.C']:
    c.SaveAs('plots/xs_vs_sqrts'+set_log+name_append+ext)

