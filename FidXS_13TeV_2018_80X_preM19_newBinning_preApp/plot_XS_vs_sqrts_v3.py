from ROOT import *
import ROOT
from array import array
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time, copy

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

from tdrStyle import *
setTDRStyle()
ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetEndErrorSize(0)

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

# MOriond 2017
#data [2.896, 1.199, 0.84, 0.857]
#data_hi [0.54, 0.338, 0.216, 0.347]
#data_lo [0.482, 0.296, 0.191, 0.279]
#modedlep_hi [0.004, 0.001, 0.0, 0.002]
#modeldep_lo [0.013, 0.004, 0.003, 0.007]
#systematics_hi [0.2654223050159878, 0.1192140931266099, 0.05837807807730571, 0.1493452376207557]
#systematics_lo [0.20616498247762635, 0.11007724560507487, 0.05137119815616531, 0.09058145505565697]

graphs_list = {
    'measured':{
        'x_values': [7,8,13],
        'central' : [0.555, 1.106, 2.896],
        'uncerUp' : [0.701, 0.433, 0.54],
        'uncerDn' : [0.446,0.360, 0.482],
        'setup' : {'color': kBlack, 'linestyle': kSolid ,'linewidth': 2, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "PZ" },
        'legend' : {'text': "Data (stat. #oplus sys. unc.)", 'draw_opt' : 'EP'}
            },

    'measured_sys':{
        'x_values': [7,8,13],
        'central' : [0.555, 1.106, 2.896],
        'uncerUp' : [0.212,0.1392444, 0.27],
        'uncerDn' : [0.061,0.0958697, 0.21],
        'setup' : {'color': kRed, 'linestyle': kSolid ,'linewidth': 4, 'fillstyle' : kSolid, 'markerstyle' : 20, 'markersize': 1.2, 'draw_opt' : "PZ" },
        'legend' : {'text': "Systematic uncertainty", 'draw_opt' : 'L'}
            },

    'model_dependancy':{
        'x_values': [7,8,13],
        'central' : [0.555, 1.106, 2.896],
        'uncerUp' : [0.00, 0.00, 0.004 ],
        'uncerDn' : [0.00, 0.00, 0.013 ],
        'setup' : {'color': kGray, 'linestyle': kSolid ,'linewidth': 0, 'fillstyle' : 1001, 'draw_opt' : "E2"},
        'legend' : {'text': "Model dependence", 'draw_opt' : 'f'}
            },

    'theory_hres1':{
        'x_values': [6,7,8,9],
        'central' : [1.0227,1.2699,1.501,1.750],
        'uncerUp' : [0.0537,0.0667,0.0789,0.0920],
        'uncerDn' : [0.0537,0.0667,0.0789,0.0920],
        'setup' : {'color': kAzure, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "A3" },
        'legend' : {'text': "Standard model (m_{H} = 125 GeV, N^{3}LO gg#rightarrow H)", 'draw_opt' : 'fl'}
            },

    'theory_hres2':{
        'x_values': [12,13,14],
        'central' : [2.431,2.719,3.034],
        'uncerUp' : [0.125,0.14,0.156],
        'uncerDn' : [0.125,0.14,0.156],
        'setup' : {'color': kAzure, 'linestyle': kDashed ,'linewidth': 3, 'fillstyle' : 3004, 'draw_opt' : "A3" },
        'legend' : {'text': "Standard model (m_{H} = 125 GeV, N^{3}LO gg#rightarrow H)", 'draw_opt' : 'fl'}
            },



}


for gr_key, gr_setup in graphs_list.iteritems():

    v_x_values = TVectorD(len(gr_setup['x_values']), array('d',[gr_setup['x_values'][i] for i in range(len(gr_setup['x_values']))]))

    if gr_key.startswith('model_dependancy'):
        v_x_valuesUp = v_x_valuesDn = TVectorD(len(gr_setup['x_values']), array('d',[0.1 for i in range(len(gr_setup['x_values']))]))
    #elif gr_key.startswith('theory_hres'):
    #    v_x_valuesUp = v_x_valuesDn = TVectorD(len(gr_setup['x_values']), array('d',[0.2 for i in range(len(gr_setup['x_values']))]))
    else:
        v_x_valuesUp = v_x_valuesDn = TVectorD(len(gr_setup['x_values']), array('d',[0.0 for i in range(len(gr_setup['x_values']))]))

    v_central = TVectorD(len(gr_setup['central']), array('d',[gr_setup['central'][i] for i in range(len(gr_setup['central']))]))
    v_uncerUp = TVectorD(len(gr_setup['uncerUp']), array('d',[gr_setup['uncerUp'][i] for i in range(len(gr_setup['uncerUp']))]))
    v_uncerDn = TVectorD(len(gr_setup['uncerDn']), array('d',[gr_setup['uncerDn'][i] for i in range(len(gr_setup['uncerDn']))]))

    v_zeros = TVectorD(len(gr_setup['uncerUp']), array('d',[0.0 for i in range(len(gr_setup['x_values']))]))

    gr_setup['graph'] = TGraphAsymmErrors(v_x_values,v_central,v_x_valuesDn,v_x_valuesUp, v_uncerDn,v_uncerUp)
    gr_setup['graphborder'] = TGraphAsymmErrors(v_x_values,v_central,v_x_valuesDn,v_x_valuesUp, v_uncerDn,v_uncerUp)
    gr_setup['graphey0'] = TGraphAsymmErrors(v_x_values,v_central,v_x_valuesDn,v_x_valuesUp, v_zeros,v_zeros)

    if not gr_key.startswith("measured"):
        gr_setup['graph'].SetFillStyle(gr_setup['setup']['fillstyle']);
        gr_setup['graph'].SetFillColor(gr_setup['setup']['color'])
        gr_setup['graph'].SetLineColor(gr_setup['setup']['color'])
        gr_setup['graph'].SetLineStyle(gr_setup['setup']['linestyle'])
        gr_setup['graph'].SetLineWidth(gr_setup['setup']['linewidth'])

        gr_setup['graphey0'].SetFillStyle(gr_setup['setup']['fillstyle']);
        gr_setup['graphey0'].SetFillColor(gr_setup['setup']['color'])
        gr_setup['graphey0'].SetLineColor(gr_setup['setup']['color'])
        gr_setup['graphey0'].SetLineStyle(kDashed)
        gr_setup['graphey0'].SetLineWidth(gr_setup['setup']['linewidth'])

        gr_setup['graphborder'].SetFillStyle(0)
        gr_setup['graphborder'].SetFillColor(gr_setup['setup']['color'])
        gr_setup['graphborder'].SetLineColor(gr_setup['setup']['color'])
        gr_setup['graphborder'].SetLineStyle(kDashed)
        gr_setup['graphborder'].SetLineWidth(2)

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

legend = TLegend(.20-move_left,.65-move_down,.58-move_left,0.9-move_down )

legend.SetTextSize(0.03)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
plots_order = [
    'theory_hres1',
    'theory_hres2',
    'model_dependancy',
    'measured',
    'measured_sys'
    ]

for i_plot, plot_name in enumerate(plots_order):
    the_plot = graphs_list[plot_name]

    the_plot['graph'].GetYaxis().SetTitleOffset(1.0)
    the_plot['graph'].GetXaxis().SetTitle("#sqrt{s} (TeV) ")
    the_plot['graph'].GetYaxis().SetTitle("#sigma_{fid} [fb]")

    the_plot['graph'].GetXaxis().SetRangeUser(0,15)

    if opt.SETLOG:
        the_plot['graph'].GetYaxis().SetRangeUser(0.1,6.0)
    else:
        the_plot['graph'].GetYaxis().SetRangeUser(-0.3,6.0)

    if plot_name=='model_dependancy':
        g = the_plot['graph']
        the_plot['graph'].SetLineColor(kBlack)
        the_plot['graph'].SetLineStyle(the_plot['setup']['linestyle'])
        the_plot['graph'].SetLineWidth(the_plot['setup']['linewidth'])
        #tmp_graph.Draw('l same')


    draw_opt = the_plot['setup']['draw_opt']

    if i_plot==0:
        the_plot['graph'].Draw(draw_opt)
    else:
        the_plot['graph'].Draw(draw_opt+'same')

    #if (plot_name.startswith('theory')):
    #    the_plot['graphey0'].Draw('psame')
    #    the_plot['graphborder'].Draw('2same')


#graphs_list['theory_hres']['graph'].SetLineStyle(kDashed)
#graphs_list['theory_hres']['graph'].SetLineWidth(3)

legend.AddEntry(graphs_list['measured']['graph'], graphs_list['measured']['legend']['text'], graphs_list['measured']['legend']['draw_opt'])
legend.AddEntry(graphs_list['measured_sys']['graph'], graphs_list['measured_sys']['legend']['text'], graphs_list['measured_sys']['legend']['draw_opt'])
legend.AddEntry(graphs_list['model_dependancy']['graph'], graphs_list['model_dependancy']['legend']['text'], graphs_list['model_dependancy']['legend']['draw_opt'])
legend.AddEntry(graphs_list['theory_hres1']['graph'], graphs_list['theory_hres1']['legend']['text'], graphs_list['theory_hres1']['legend']['draw_opt'])

legend.SetShadowColor(0);
legend.SetFillColor(0);
legend.SetLineColor(0);
legend.Draw()

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.45*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right
latex2.DrawLatex(0.94, 0.94,"5.1 fb^{-1} (7 TeV), 19.7 fb^{-1} (8 TeV), 35.9 fb^{-1} (13 TeV) ")
latex2.SetTextSize(0.8*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right
latex2.DrawLatex(c.GetLeftMargin()+0.05, 0.85, "CMS")  #preliminary version


latex2.SetTextSize(0.7*c.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(c.GetLeftMargin()+0.175, 0.85, "Preliminary")

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
    c.SaveAs('plots/xs_vs_sqrts'+set_log+name_append+ext)

