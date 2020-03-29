import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames_ordered import *
from sample_latexnames_ordered import *

if (not os.path.exists("tables")):
    os.system("mkdir tables")
if (not os.path.exists("plots")):
    os.system("mkdir plots")

from ROOT import *
from tdrStyle import setTDRStyle
setTDRStyle()
lum_16=35.9
lum_17=41.4
#lum_18=58.8
lum_18=59.7
lumin=[35.9,41.4,58.8]
years=[2016,2017,2018]
year='2018'
#sys.path.append('./datacardInputs/')
#path='raid/raid7/tjavaid/fiducial_XS/CMSSW_7_4_7/src/FidXS_13TeV_2018_80X_preM19_newBinning_preApp/datacardInputs'
#sys.path.append('./datacardInputs/')
sys.path.append('./table/')
#sys.path.append('./datacardInputs_Run2Fid/')
obsName = 'mass4l'
_temp16 = __import__('inputs_sig_mass4l_'+'2016', globals(), locals(), ['acc','dacc','eff','deff','outinratio','doutinratio','inc_wrongfrac'], -1)
acc16 = _temp16.acc
dacc16 = _temp16.dacc
eff16 = _temp16.eff
deff16 = _temp16.deff
outinratio16 = _temp16.outinratio
doutinratio16 = _temp16.doutinratio
inc_wrongfrac16 = _temp16.inc_wrongfrac

_temp17 = __import__('inputs_sig_mass4l_'+'2017', globals(), locals(), ['acc','dacc','eff','deff','outinratio','doutinratio','inc_wrongfrac'], -1)
acc17 = _temp17.acc
dacc17 = _temp17.dacc
eff17 = _temp17.eff
deff17 = _temp17.deff
outinratio17 = _temp17.outinratio
doutinratio17 = _temp17.doutinratio
inc_wrongfrac17 = _temp17.inc_wrongfrac

_temp18 = __import__('inputs_sig_mass4l_'+'2018', globals(), locals(), ['acc','dacc','eff','deff','outinratio','doutinratio','inc_wrongfrac'], -1)
acc18 = _temp18.acc
dacc18 = _temp18.dacc
eff18 = _temp18.eff
deff18 = _temp18.deff
outinratio18 = _temp18.outinratio
doutinratio18 = _temp18.doutinratio
inc_wrongfrac18 = _temp18.inc_wrongfrac







#_temp = __import__('inputs_sig_njets_pt30_eta4p7', globals(), locals(), ['lambdajesup'], -1)
#lambdajesup = _temp.lambdajesup


fStates = ['4e','4mu','2e2mu','4l']
endcolumn = {'4e':' & ', '4mu':' & ', '2e2mu':' & ', '4l':' \\\\ \n'}
nmodels = 0

# summary
for tabletype in ['SM','Exo']:


    print '\\documentclass{article}'
    print '\\begin{document}'
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Summary of different Standard Model signal models.'
        print '\label{tab:summarySM}'
    else:
        print 'Summmary for different models used to check model dependence.'
        print '\label{tab:summaryExo}'
    print '}'
    print '\\begin{tabular}{|l|c|c|c|c|} \\hline \\hline '
    print '\\textbf{Signal process} & $\\mathcal{A}_{\\rm fid}$ & $\\epsilon$ & $f_{\\rm nonfid}$  & $(1+f_{\\rm nonfid})\\epsilon$ \\\\ \\hline \\hline '
    print '\\multicolumn{5}{|c|}{Individual Higgs boson production modes} \\\\ \\hline '
    table = ''
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
#        prod_acc=acc[short+'_4l_'+obsName+'_genbin0_recobin0']
        acc=((acc16[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_16)+(acc17[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_17)+(acc18[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_18))/(lum_16+lum_17+lum_18)
#	print "eff 2016 is  ",eff16[short+'_4l_'+obsName+'_genbin0_recobin0']
#	print "eff 2017 is   ", eff17[short+'_4l_'+obsName+'_genbin0_recobin0']
#	print "eff 2018 is   ", eff18[short+'_4l_'+obsName+'_genbin0_recobin0']
        eff=((eff16[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_16)+(eff17[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_17)+(eff18[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_18))/(lum_16+lum_17+lum_18)
        outinratio=((outinratio16[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_16)+(outinratio17[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_17)+(outinratio18[short+'_4l_'+obsName+'_genbin0_recobin0']*lum_18))/(lum_16+lum_17+lum_18)
###############################combining the uncertainties
	dacc=sqrt((dacc16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2+(dacc17[short+'_4l_'+obsName+'_genbin0_recobin0'])**2+(dacc18[short+'_4l_'+obsName+'_genbin0_recobin0'])**2)
	deff=sqrt((deff16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2+(deff17[short+'_4l_'+obsName+'_genbin0_recobin0'])**2+(deff18[short+'_4l_'+obsName+'_genbin0_recobin0'])**2)
        doutinratio=sqrt((doutinratio16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2+(doutinratio17[short+'_4l_'+obsName+'_genbin0_recobin0'])**2+(doutinratio18[short+'_4l_'+obsName+'_genbin0_recobin0'])**2)
#last col. unc.        
        deff1pfout16 = sqrt( ((1+outinratio16[short+'_4l_'+obsName+'_genbin0_recobin0'])*deff16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 + (eff16[short+'_4l_'+obsName+'_genbin0_recobin0']*doutinratio16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 )
        deff1pfout17 = sqrt( ((1+outinratio17[short+'_4l_'+obsName+'_genbin0_recobin0'])*deff17[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 + (eff17[short+'_4l_'+obsName+'_genbin0_recobin0']*doutinratio17[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 )
        deff1pfout18 = sqrt( ((1+outinratio18[short+'_4l_'+obsName+'_genbin0_recobin0'])*deff18[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 + (eff18[short+'_4l_'+obsName+'_genbin0_recobin0']*doutinratio18[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 )
	deff1pfout=sqrt((deff1pfout16)**2+(deff1pfout17)**2+(deff1pfout18)**2)


#        print "average acceptance is====",acc
#        print "test print for acceptance is ===", acc16[short+'_4l_'+obsName+'_genbin0_recobin0']
        line = sample_latexnames[long].replace('_','\_')+' & '
#        line = line + '%.3f'%acc16[short+'_4l_'+obsName+'_genbin0_recobin0']+' $\pm$ %.3f'%dacc16[short+'_4l_'+obsName+'_genbin0_recobin0']+' & '
        line = line + '%.3f'%acc+' $\pm$ %.3f'%dacc+' & '
        #line = line + '%.3f'%eff16[short+'_4l_'+obsName+'_genbin0_recobin0']+' $\pm$ %.3f'%deff16[short+'_4l_'+obsName+'_genbin0_recobin0']+' & '
        line = line + '%.3f'%eff+' $\pm$ %.3f'%deff+' & '
        #line = line + '%.3f'%outinratio16[short+'_4l_'+obsName+'_genbin0_recobin0']+' $\pm$ %.3f'%doutinratio16[short+'_4l_'+obsName+'_genbin0_recobin0']+' & '
        line = line + '%.3f'%outinratio+' $\pm$ %.3f'%doutinratio+' & '
#        deff1pfout = sqrt( ((1+outinratio16[short+'_4l_'+obsName+'_genbin0_recobin0'])*deff16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 + (eff16[short+'_4l_'+obsName+'_genbin0_recobin0']*doutinratio16[short+'_4l_'+obsName+'_genbin0_recobin0'])**2 )
#        line = line + '%.3f'%(eff16[short+'_4l_'+obsName+'_genbin0_recobin0']*(1+outinratio16[short+'_4l_'+obsName+'_genbin0_recobin0']))+' $\pm$ %.3f'%deff1pfout+' \\\\ \n '
        line = line + '%.3f'%(eff*(1+outinratio))+' $\pm$ %.3f'%deff1pfout+' \\\\ \n '
        table += line
    print table
    print '\\hline \\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print '\end{document}'
    print ' '
    print ' '
    print ' '
    


'''
### Acceptance
for tabletype in ['SM','Exo']:
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Standard Model signal Model Carlo Samples.'
        print '\label{tab:samplesSM}'
    else:
        print 'Signal Model Carlo Samples used to test model dependence.'
        print '\label{tab:samplesExo}'
    print '}'
    print '\\begin{tabular}{|l|c|} \\hline '
    table = 'Sample & Description \\\\ \hline \n'
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
        if (tabletype=='SM' and '125p6' in short): continue
        if (tabletype=='Exo' and not '125p6' in short): continue
        line = long.replace('_','\_')+' & '+sample_latexnames[long].replace('_','\_')+' \\\\ \n '
        table += line
    print table
    print '\\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print ' '
    print ' '
    print ' '


### Acceptance
for tabletype in ['SM','Exo']:
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Fiducial volume acceptance per final state for different Standard Model signal models.'
        print '\label{tab:acceptanceSM}'
    else:
        print 'Fiducial volume acceptance per final state for different signal models used to check model dependence.'
        print '\label{tab:acceptanceExo}'
    print '}'
    print '\\begin{tabular}{|l|c|c|c|c|} \\hline '
    table = 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline \n'
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
        if (tabletype=='SM' and '125p6' in short): continue
        if (tabletype=='Exo' and not '125p6' in short): continue
        line = sample_latexnames[long].replace('_','\_')+' & '
        for fState in fStates:
            line = line + ('%.3f'%acc[short+'_'+fState+'_'+obsName+'_genbin0_recobin0'])+(' $\pm$ %.3f'%dacc[short+'_'+fState+'_'+obsName+'_genbin0_recobin0'])+endcolumn[fState]
            #if (short.startswith('ggH')): line = line + '%.3f'%acc[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+endcolumn[fState]
            #if (short.startswith('ggH')): line = line + '%.3f'%acc['ggH_HRes_125_'+fState+'_'+obsName+'_genbin0_recobin0']+endcolumn[fState]
            #else: line = line + '%.3f'%acc[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+endcolumn[fState]

        table += line
    print table
    print '\\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print ' '
    print ' '
    print ' '

### Efficiency
for tabletype in ['SM','Exo']:
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Reconstruction efficiency ($\epsilon$) for fiducial events per final state for different Standard Model signal models.'
        print '\label{tab:efficiencySM}'
    else:
        print 'Reconstruction efficiency ($\epsilon$) for fiducial events per final state for different models used to check model dependence.'
        print '\label{tab:efficiencyExo}'
    print '}'
    print '\\begin{tabular}{|l|c|c|c|c|} \\hline '
    table = 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline \n'
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
        if (tabletype=='SM' and '125p6' in short): continue
        if (tabletype=='Exo' and not '125p6' in short): continue
        if (not (short.startswith('WH_JHUgen') or short.startswith('ZH_JHUgen')) ): nmodels +=1
        line = sample_latexnames[long].replace('_','\_')+' & '
        for fState in fStates:
            line = line + '%.3f'%eff[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+' $\pm$ %.3f'%deff[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+endcolumn[fState]
        table += line
    print table
    print '\\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print ' '
    print ' '
    print ' '
            
# f(out)
for tabletype in ['SM','Exo']:
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Ratio of reconstructed events which are from outside the fiducial volume and reconstructed events which are from within the fiducial volume ($f_{out}$) per final state for different Standard Model signal models.'
        print '\label{tab:foutSM}'
    else:
        print 'Ratio of reconstructed events which are from outside the fiducial volume and reconstructed events which are from within the fiducial volume ($f_{out}$) per final state for different models used to check model dependence.'
        print '\label{tab:foutExo}'
    print '}'
    print '\\begin{tabular}{|l|c|c|c|c|} \\hline '
    table = 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline \n'
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
        if (tabletype=='SM' and '125p6' in short): continue
        if (tabletype=='Exo' and not '125p6' in short): continue
        line = sample_latexnames[long].replace('_','\_')+' & '
        for fState in fStates:
            line = line + '%.3f'%outinratio[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+' $\pm$ %.3f'%doutinratio[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+endcolumn[fState]
        table += line
    print table
    print '\\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print ' '
    print ' '
    print ' '

# wrong frac
for tabletype in ['SM','Exo']:
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Fraction of signal events in the mass range 105.6--140.6 $\GeV$ where at least one lepton selected is not from the Higgs boson decay'
        print '\label{tab:wrongracSM}' 
    else:
        print 'Fraction of signal events in the mass range 105.6--140.6 $\GeV$ where at least one lepton selected is not from the Higgs boson decay'
        print '\label{tab:wrongfracExo}'
    print '}'
    print '\\begin{tabular}{|l|c|c|c|c|} \\hline '
    table = 'Sample & $4e$ & $4\mu$ & $2e2\mu$ & $4\ell$ \\\\ \hline \n'
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
        if (tabletype=='SM' and '125p6' in short): continue
        if (tabletype=='Exo' and not '125p6' in short): continue
        line = sample_latexnames[long].replace('_','\_')+' & '
        for fState in fStates:
            line = line + '%.3f'%inc_wrongfrac[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']+endcolumn[fState]
        table += line
    print table
    print '\\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print ' '
    print ' '
    print ' '


# JES
for tabletype in ['SM','Exo']:
    print '\\begin{table}[!h!tb]'
    print '\\begin{center}'
    print '\small'
    print '\caption{'
    if (tabletype == 'SM'):
        print 'Percent change in events when increasing the jet energy scale by 1$\sigma$ for various signal model (all final states combined).'
        print '\label{tab:jesSM}'
    else:
        print 'Percent change in events when increasing the jet energy scale by 1$\sigma$ for various signal model (all final states combined).'
        print '\label{tab:jesExo}'
    print '}'
    print '\\begin{tabular}{|l|c|c|c|c|} \\hline '
    table = 'Sample & N(jets)=0 & N(jets)=1 & N(jets)=2 & N(jets)$\geq$3 \\\\ \hline \n'
    for long in sample_shortnames.keys():
        short = sample_shortnames[long]
        if (tabletype=='SM' and '125p6' in short): continue
        if (tabletype=='Exo' and not '125p6' in short): continue
        #if (not short+'_2e2mu_njets_reco_pt30_eta4p7_genbin0_recobin0' in lambdajesup): continue
        line = sample_latexnames[long].replace('_','\_')+' & '
        for recobin in range(0,4):
            line = line + '%.3f'%lambdajesup[short+'_2e2mu_njets_pt30_eta4p7_genbin0_recobin'+str(recobin)]+' & '
        line = line.rstrip(' & ')+' \\\\ \n'
        table += line
    print table
    print '\\hline'
    print '\end{tabular}'
    print '\\normalsize'
    print '\end{center}'
    print '\end{table}'
    print ' '
    print ' '
    print ' '
'''            
## Plot ratio of efficiency and fout vs. model together
#effmodeldep = {}
#finmodeldep = {}
#for fState in fStates:
    #effmodeldep[fState] = TH1D('effmodeldep'+fState,'effmodeldep'+fState,nmodels,0,nmodels)
    #finmodeldep[fState] = TH1D('finmodeldep'+fState,'finmodeldep'+fState,nmodels,0,nmodels)
    #bin=1
    #for long in sample_shortnames.keys():
        #short = sample_shortnames[long]
        ##if (tabletype=='SM' and '125p6' in short): continue
        ##if (tabletype=='Exo' and not '125p6' in short): continue
        
        #if (short.startswith('WH_JHUgen')): continue
        #if (short.startswith('ZH_JHUgen')): continue

        #effmodeldep[fState].GetXaxis().SetBinLabel(bin,short.replace('_',' '))
        #finmodeldep[fState].GetXaxis().SetBinLabel(bin,short.replace('_',' '))
        
        #model_eff = eff[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']
        #model_deff = deff[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']
        #model_fout = outinratio[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']
        #model_dfout = doutinratio[short+'_'+fState+'_'+obsName+'_genbin0_recobin0']
        #model_fin = 1.0-model_fout
        #model_dfin = model_fin*(model_dfout/model_fout)
        #model_efffout = model_eff*(1+model_fout)
        
        #ggH_eff = eff['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #ggH_deff = deff['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0'] 
        #ggH_fout = outinratio['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #ggH_dfout = doutinratio['ggH_powheg_JHUgen_125_'+fState+'_'+obsName+'_genbin0_recobin0']
        #ggH_fin = 1.0-ggH_fout
        #ggH_dfin = ggH_fin*(ggH_dfout/ggH_fout)
        #ggH_efffout = ggH_eff*(1+ggH_fout)
        
        #effratio = model_eff/ggH_eff
        #deffratio = effratio*sqrt((model_deff/model_eff)**2+(ggH_deff/ggH_eff)**2)
        #finratio = model_fin/ggH_fin
        #dfinratio = finratio*sqrt((model_dfin/model_fin)**2+(ggH_dfin/ggH_fin)**2)
        #efffoutratio = model_efffout/ggH_efffout
        
        #print short,str(effratio),str(finratio)
        #effmodeldep[fState].SetBinContent(bin,effratio)
        #effmodeldep[fState].SetBinContent(bin,efffoutratio)
        #effmodeldep[fState].SetBinError(bin,deffratio)
        #finmodeldep[fState].SetBinContent(bin,finratio)
        #finmodeldep[fState].SetBinError(bin,dfinratio)
        
        #bin+=1
            
#c = TCanvas("c","c",1000,800)
#c.SetRightMargin(0.1)
#c.SetLeftMargin(0.05)
#effmodeldep['4e'].GetYaxis().SetLabelSize(0.04)    
#effmodeldep['4e'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['4e'].GetYaxis().SetTitleOffset(0.4)        
#effmodeldep['4e'].GetYaxis().SetTitleSize(0.09)        
#effmodeldep['4mu'].GetYaxis().SetLabelSize(0.04)    
#effmodeldep['4mu'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['4mu'].GetYaxis().SetTitleOffset(0.4)        
#effmodeldep['4mu'].GetYaxis().SetTitleSize(0.09)        
#effmodeldep['2e2mu'].GetYaxis().SetLabelSize(0.04)    
#effmodeldep['2e2mu'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['2e2mu'].GetYaxis().SetTitleOffset(0.4)        
#effmodeldep['2e2mu'].GetYaxis().SetTitleSize(0.09)        
#effmodeldep['4l'].GetYaxis().SetLabelSize(0.04)    
#effmodeldep['4l'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['4l'].GetYaxis().SetTitleOffset(0.6)        
#effmodeldep['4l'].GetYaxis().SetTitleSize(0.057)        

#c.cd()
#c.SetTopMargin(0.06)
#latex2 = TLatex()
#latex2.SetNDC()
#latex2.SetTextSize(0.5*c.GetTopMargin())
#latex2.SetTextFont(42)
#latex2.SetTextAlign(31) # align right                                                                                                                 
#latex2.DrawLatex(0.87, 0.9,"#sqrt{s} = 13 TeV")
#latex2.SetTextSize(0.9*c.GetTopMargin())
#latex2.SetTextFont(62)
#latex2.SetTextAlign(11) # align right                                                                                                                 
#latex2.DrawLatex(0.17, 0.9, "CMS")
#latex2.SetTextSize(0.7*c.GetTopMargin())
#latex2.SetTextFont(52)
#latex2.SetTextAlign(11)
#latex2.DrawLatex(0.27, 0.9, "Preliminary")
#pad1 = TPad("pad1", "pad1", 0.0, 0.7, 1.0, 0.9)
#pad1.SetFillColor(0)
#pad1.SetFillStyle(0)
#pad1.SetLeftMargin(0.1)
#pad1.SetBottomMargin(0.0)
#pad1.Draw()    
#pad1.cd()
#effmodeldep['4e'].SetLineColor(6)
#effmodeldep['4e'].SetMarkerColor(6)
#effmodeldep['4e'].SetMaximum(1.19)
#effmodeldep['4e'].SetMinimum(0.81)
#effmodeldep['4e'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['4e'].GetYaxis().SetLabelSize(0.06)    
#effmodeldep['4e'].Draw("LP")
#finmodeldep['4e'].SetLineColor(8)
#finmodeldep['4e'].SetMarkerColor(8)
##finmodeldep['4e'].Draw("LPsame")
#latex2.SetTextFont(42)
#latex2.SetTextSize(2.0*c.GetTopMargin())
#latex2.DrawLatex(0.15,0.7, "4e")
#legend = TLegend(.8,.65,.95,.85)
#legend.AddEntry(effmodeldep['4e'],"#epsilon(1+f_{out})", "l")
##legend.AddEntry(finmodeldep['4e'],"f_{out}","l")
#legend.SetShadowColor(0);
#legend.SetFillColor(0);
#legend.SetLineColor(0);
#legend.Draw("same")
#c.cd()
#pad2 = TPad("pad2", "pad2", 0.0, 0.5, 1.0, 0.7)
#pad2.SetFillColor(0)
#pad2.SetFillStyle(0)
#pad2.SetLeftMargin(0.1)
#pad2.SetBottomMargin(0.0)
#pad2.SetTopMargin(0.0)
#pad2.Draw()
#pad2.cd()
#effmodeldep['4mu'].SetLineColor(6)
#effmodeldep['4mu'].SetMarkerColor(6)
#effmodeldep['4mu'].SetMaximum(1.19)
#effmodeldep['4mu'].SetMinimum(0.81)
#effmodeldep['4mu'].GetYaxis().SetLabelSize(0.06)    
#effmodeldep['4mu'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['4mu'].Draw("LP")
#finmodeldep['4mu'].SetLineColor(8)
#finmodeldep['4mu'].SetMarkerColor(8)
##finmodeldep['4mu'].Draw("LPsame")
#latex2.SetTextFont(42)
#latex2.SetTextSize(2.0*c.GetTopMargin())
#latex2.DrawLatex(0.15,0.7, "4#mu")
#legend.Draw("same")
#c.cd()
#pad3 = TPad("pad3", "pad3", 0.0, 0.3, 1.0, 0.5)
#pad3.SetFillColor(0)
#pad3.SetFillStyle(0)
#pad3.SetLeftMargin(0.1)
#pad3.SetBottomMargin(0.0)
#pad3.SetTopMargin(0.0)
#pad3.Draw()
#pad3.cd()
#effmodeldep['2e2mu'].SetLineColor(6)
#effmodeldep['2e2mu'].SetMarkerColor(6)
#effmodeldep['2e2mu'].SetMaximum(1.19)
#effmodeldep['2e2mu'].SetMinimum(0.81)
#effmodeldep['2e2mu'].GetYaxis().SetLabelSize(0.06)    
#effmodeldep['2e2mu'].GetYaxis().SetTitle("model/gg#rightarrowH(125 GeV)")    
#effmodeldep['2e2mu'].Draw("LP")
#finmodeldep['2e2mu'].SetLineColor(8)
#finmodeldep['2e2mu'].SetMarkerColor(8)
##finmodeldep['2e2mu'].Draw("LPsame")
#latex2.SetTextFont(42)
#latex2.SetTextSize(2.0*c.GetTopMargin())
#latex2.DrawLatex(0.15,0.7, "2e2#mu")
#legend.Draw("same")
#c.cd()
#pad4 = TPad("pad4", "pad4", 0.0, 0.0, 1.0, 0.3)
#pad4.SetFillColor(0)
#pad4.SetFillStyle(0)
#pad4.SetLeftMargin(0.1)
#pad4.SetBottomMargin(0.25)
#pad4.SetTopMargin(0.0)
#pad4.Draw()
#pad4.cd()
#effmodeldep['4l'].SetLineColor(6)
#effmodeldep['4l'].SetMarkerColor(6)
#effmodeldep['4l'].SetMaximum(1.19)
#effmodeldep['4l'].SetMinimum(0.81)
#effmodeldep['4l'].Draw("LP")
#finmodeldep['4l'].SetLineColor(8)
#finmodeldep['4l'].SetMarkerColor(8)
##finmodeldep['4l'].Draw("LPsame")
#latex2.SetTextFont(42)
#latex2.SetTextSize(1.2*c.GetTopMargin())
#latex2.DrawLatex(0.15,0.85, "4l")
##legend.Draw("same")

#c.SaveAs('plots/modeldep_inclusive.pdf')
