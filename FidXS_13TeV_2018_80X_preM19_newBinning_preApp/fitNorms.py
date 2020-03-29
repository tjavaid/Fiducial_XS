import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from ROOT import *
from tdrStyle import *
setTDRStyle()


plotPath = 'plots_signalnorms'
sys.path.append("./"+plotPath) 

m4lvar = 'mass4l'
lumi=2701

g_res_untag = {}; g_res_tag = {}
g_nonres_untag = {}; g_nonres_tag = {}

_xsbr = __import__('higgs_xsnlo_br', globals(), locals())
_xs = _xsbr.sigma_nlo
_br4l = _xsbr.br_h4l
_br_hzz2lX = _xsbr.br_hzz2lX

ggH_norm = {}
VBF_norm = {}
WplusH_norm = {}
WminusH_norm = {}
ZH_norm = {}

for fs in ['4e','4mu','2e2mu']:
#for fs in ['2e2mu']:

  _sig = __import__('signorms_mass4l_'+fs+'_test', globals(), locals())
  _norms = _sig.N_sig

#  for proc in ['GluGluHToZZTo4L','VBF_HToZZTo4L','WminusH_HToZZTo4L','WplusH_HToZZTo4L']:
#  for proc in ['GluGluHToZZTo4L','VBF_HToZZTo4L','WminusH_HToZZTo4L','WplusH_HToZZTo4L','ZH_HToZZ_4LFilter']:
#  for proc in ['ZH_HToZZ_4LFilter']:
  for proc in ['ttH_HToZZ_4LFilter']:

    masses = array('d',[]);
    res_tag = array('d',[]);
    res_untag = array('d',[]);
    nonres_tag = array('d',[]);
    nonres_untag = array('d',[]);
    dres_tag = array('d',[]);
    dres_untag = array('d',[]);
    dnonres_tag = array('d',[]);
    dnonres_untag = array('d',[]);
    zeros = array('d',[])

#    for key in _norms:
    for key in _br4l:

#      if (not proc in key): continue

#      mass = key.split('_'+fs)[0].split('_M')[1].split('_')[0]
      mass = key

      if mass=='155': continue

      if (float(mass)>=160): continue
#      if (float(mass) in masses): continue
      
      if (proc.startswith('GluGlu')): xsbr = _xs['ggH_'+mass]*_br4l[mass]*(44.14/_xs['ggH_125'])
      if (proc.startswith('VBF')): xsbr = _xs['VBF_'+mass]*_br4l[mass]*(3.782/_xs['VBF_125'])
      if (proc.startswith('Wplus')): xsbr = _xs['WplusH_'+mass]*_br4l[mass]*(1.38/(_xs['WplusH_125']+_xs['WminusH_125']))
      if (proc.startswith('Wminus')): xsbr = _xs['WminusH_'+mass]*_br4l[mass]*(1.38/(_xs['WplusH_125']+_xs['WminusH_125']))
      if (proc.startswith('ZH')): xsbr = _xs['ZH_'+mass]*_br_hzz2lX[mass]*0.15038*(0.8696/_xs['ZH_125'])
      if (proc.startswith('ttH')): xsbr = _xs['ttH_'+mass]*_br_hzz2lX[mass]*0.1544*(0.5027/_xs['ttH_125'])
 
      print proc,mass,xsbr

      continue

      masses.append(float(mass))

      res_tag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_res_tag']*xsbr*lumi)
      res_untag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_res_untag']*xsbr*lumi)
      nonres_tag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_nonres_tag']*xsbr*lumi)
      nonres_untag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_nonres_untag']*xsbr*lumi)

      dres_tag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_res_tag_err']*xsbr*lumi)
      dres_untag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_res_untag_err']*xsbr*lumi)
      dnonres_tag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_nonres_tag_err']*xsbr*lumi)
      dnonres_untag.append(_norms[proc+'_M'+mass+'_'+fs+'_'+m4lvar+'_nonres_untag_err']*xsbr*lumi)

      zeros.append(0.0)

    v_mass = TVectorD(len(masses),masses)

    v_res_tag = TVectorD(len(res_tag),res_tag)
    v_res_untag = TVectorD(len(res_untag),res_untag)
    v_nonres_tag = TVectorD(len(nonres_tag),nonres_tag)
    v_nonres_untag = TVectorD(len(nonres_untag),nonres_untag)

    v_dres_tag = TVectorD(len(dres_tag),dres_tag)
    v_dres_untag = TVectorD(len(dres_untag),dres_untag)
    v_dnonres_tag = TVectorD(len(dnonres_tag),dnonres_tag)
    v_dnonres_untag = TVectorD(len(dnonres_untag),dnonres_untag)

    v_zeros = TVectorD(len(zeros),zeros)

    c1 = TCanvas("c1","c1",800,800)
    c1.SetRightMargin(0.1)
    c1.cd()
    dummy = TH1D("dummy","dummy",1,110,140)
    dummy.GetXaxis().SetTitle("m(H) [GeV]")
    dummy.GetYaxis().SetTitle("Resonant Signal Yield: Untagged")
    dummy.SetMinimum(0.5*min(res_untag))
    dummy.SetMaximum(1.5*max(res_untag))
    dummy.SetBinContent(1,0.0)
    dummy.Draw()    
    g_res_untag[proc+'_'+fs] = TGraphErrors(v_mass,v_res_untag,v_zeros,v_dres_untag)
    g_res_untag[proc+'_'+fs].SetMarkerStyle(20)
    g_res_untag[proc+'_'+fs].SetMarkerSize(1.1)
    g_res_untag[proc+'_'+fs].SetMarkerColor(kGreen)
    g_res_untag[proc+'_'+fs].SetLineColor(kGreen)
    g_res_untag[proc+'_'+fs].Draw("Psame")
    f1 = TF1("f1","pol2",110,140)
    g_res_untag[proc+'_'+fs].Fit('f1','R')
    if proc.startswith('GluGlu'): 
      print g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ggH_norm['p0_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ggH_norm['p1_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ggH_norm['p2_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('VBF'): 
      VBF_norm['p0_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      VBF_norm['p1_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      VBF_norm['p2_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wplus'): 
      WplusH_norm['p0_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WplusH_norm['p1_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WplusH_norm['p2_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wminus'): 
      WminusH_norm['p0_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WminusH_norm['p1_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WminusH_norm['p2_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('ZH'): 
      ZH_norm['p0_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ZH_norm['p1_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ZH_norm['p2_'+fs+'_res_0'] = g_res_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_res_untag.pdf")
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_res_untag.png")
    
    del c1                                                

    c1 = TCanvas("c1","c1",800,800)
    c1.SetRightMargin(0.1)
    c1.cd()
    dummy = TH1D("dummy","dummy",1,110,140)
    dummy.GetXaxis().SetTitle("m(H) [GeV]")
    dummy.GetYaxis().SetTitle("Resonant Signal Yield: Tagged")
    dummy.SetMinimum(0.5*min(res_tag))
    dummy.SetMaximum(1.5*max(res_tag))
    dummy.SetBinContent(1,0.0)
    dummy.Draw()    
    g_res_tag[proc+'_'+fs] = TGraphErrors(v_mass,v_res_tag,v_zeros,v_dres_tag)
    g_res_tag[proc+'_'+fs].SetMarkerStyle(20)
    g_res_tag[proc+'_'+fs].SetMarkerSize(1.1)
    g_res_tag[proc+'_'+fs].SetMarkerColor(kGreen)
    g_res_tag[proc+'_'+fs].SetLineColor(kGreen)
    g_res_tag[proc+'_'+fs].Draw("Psame")
    f1 = TF1("f1","pol2",110,140)
    g_res_tag[proc+'_'+fs].Fit('f1','R')
    if proc.startswith('GluGlu'): 
      ggH_norm['p0_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ggH_norm['p1_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ggH_norm['p2_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('VBF'): 
      VBF_norm['p0_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      VBF_norm['p1_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      VBF_norm['p2_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wplus'): 
      WplusH_norm['p0_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WplusH_norm['p1_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WplusH_norm['p2_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wminus'): 
      WminusH_norm['p0_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WminusH_norm['p1_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WminusH_norm['p2_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('ZH'): 
      ZH_norm['p0_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ZH_norm['p1_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ZH_norm['p2_'+fs+'_res_1'] = g_res_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_res_tag.pdf")
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_res_tag.png")
    
    del c1

    c1 = TCanvas("c1","c1",800,800)
    c1.SetRightMargin(0.1)
    c1.cd()
    dummy = TH1D("dummy","dummy",1,110,140)
    dummy.GetXaxis().SetTitle("m(H) [GeV]")
    dummy.GetYaxis().SetTitle("Nonresonant Signal Yield: Untagged")
    dummy.SetMinimum(0.5*min(nonres_untag))
    dummy.SetMaximum(1.5*max(nonres_untag))
    dummy.SetBinContent(1,0.0)
    dummy.Draw()    
    g_nonres_untag[proc+'_'+fs] = TGraphErrors(v_mass,v_nonres_untag,v_zeros,v_dnonres_untag)
    g_nonres_untag[proc+'_'+fs].SetMarkerStyle(20)
    g_nonres_untag[proc+'_'+fs].SetMarkerSize(1.1)
    g_nonres_untag[proc+'_'+fs].SetMarkerColor(kGreen)
    g_nonres_untag[proc+'_'+fs].SetLineColor(kGreen)
    g_nonres_untag[proc+'_'+fs].Draw("Psame")
    f1 = TF1("f1","pol2",110,140)
    g_nonres_untag[proc+'_'+fs].Fit('f1','R')
    if proc.startswith('GluGlu'): 
      ggH_norm['p0_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ggH_norm['p1_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ggH_norm['p2_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('VBF'): 
      VBF_norm['p0_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      VBF_norm['p1_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      VBF_norm['p2_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wplus'): 
      WplusH_norm['p0_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WplusH_norm['p1_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WplusH_norm['p2_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wminus'): 
      WminusH_norm['p0_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WminusH_norm['p1_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WminusH_norm['p2_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('ZH'): 
      ZH_norm['p0_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ZH_norm['p1_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ZH_norm['p2_'+fs+'_nonres_0'] = g_nonres_untag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_nonres_untag.pdf")
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_nonres_untag.png")
    
    del c1                                                

    c1 = TCanvas("c1","c1",800,800)
    c1.SetRightMargin(0.1)
    c1.cd()
    dummy = TH1D("dummy","dummy",1,110,140)
    dummy.GetXaxis().SetTitle("m(H) [GeV]")
    dummy.GetYaxis().SetTitle("Nonresonant Signal Yield: Tagged")
    dummy.SetMinimum(0.5*min(nonres_tag))
    dummy.SetMaximum(1.5*max(nonres_tag))
    dummy.SetBinContent(1,0.0)
    dummy.Draw()    
    g_nonres_tag[proc+'_'+fs] = TGraphErrors(v_mass,v_nonres_tag,v_zeros,v_dnonres_tag)
    g_nonres_tag[proc+'_'+fs].SetMarkerStyle(20)
    g_nonres_tag[proc+'_'+fs].SetMarkerSize(1.1)
    g_nonres_tag[proc+'_'+fs].SetMarkerColor(kGreen)
    g_nonres_tag[proc+'_'+fs].SetLineColor(kGreen)
    g_nonres_tag[proc+'_'+fs].Draw("Psame")
    f1 = TF1("f1","pol2",110,140)
    g_nonres_tag[proc+'_'+fs].Fit('f1','R')
    if proc.startswith('GluGlu'): 
      ggH_norm['p0_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ggH_norm['p1_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ggH_norm['p2_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('VBF'): 
      VBF_norm['p0_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      VBF_norm['p1_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      VBF_norm['p2_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wplus'): 
      WplusH_norm['p0_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WplusH_norm['p1_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WplusH_norm['p2_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('Wminus'): 
      WminusH_norm['p0_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      WminusH_norm['p1_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      WminusH_norm['p2_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    if proc.startswith('ZH'): 
      ZH_norm['p0_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(0)
      ZH_norm['p1_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(1)
      ZH_norm['p2_'+fs+'_nonres_1'] = g_nonres_tag[proc+'_'+fs].GetFunction('f1').GetParameter(2)
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_nonres_tag.pdf")
    c1.SaveAs(plotPath + "/norm_"+proc+"_"+fs+"_nonres_tag.png")    

    del c1


with open(plotPath+'/ggH_norm.py', 'w') as f:
    f.write('ggH_norm = '+str(ggH_norm))
f.close()
with open(plotPath+'/VBF_norm.py', 'w') as f:
    f.write('VBF_norm = '+str(VBF_norm))
f.close()
with open(plotPath+'/WplusH_norm.py', 'w') as f:
    f.write('WplusH_norm = '+str(WplusH_norm))
f.close()
with open(plotPath+'/WminusH_norm.py', 'w') as f:
    f.write('WminusH_norm = '+str(WminusH_norm))
f.close()
with open(plotPath+'/ZH_norm.py', 'w') as f:
    f.write('ZH_norm = '+str(ZH_norm))
f.close()
