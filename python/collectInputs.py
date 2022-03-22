import sys
import os

# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from Utils import *

sys.path.append('./'+datacardInputs)

def collect(obsName):

	acc = {}
	dacc = {} 
	acc_4l = {} 
	dacc_4l = {}
	dacc_4l = {}
	eff = {}
	deff = {}
	inc_outfrac = {}
	binfrac_outfrac = {}
	outinratio = {} 
	doutinratio = {}
	inc_wrongfrac = {}
	binfrac_wrongfrac = {}
	cfactor = {}
	lambdajesup = {}
	lambdajesdn = {}

	channels = ['4mu','4e','2e2mu']
	if (obsName=='mass4l'): channels.append('4l')

	for ch in channels:
		border_msg("module to import: "+'inputs_sig_'+obsName+'_'+ch+".py")
		_tmp = __import__('inputs_sig_'+obsName+'_'+ch, globals(), locals(), -1)

		acc.update(_tmp.acc)
		dacc.update(_tmp.dacc)
		acc_4l.update(_tmp.acc_4l)
		dacc_4l.update(_tmp.dacc_4l)
		eff.update(_tmp.eff)
		deff.update(_tmp.deff)
		inc_outfrac.update(_tmp.inc_outfrac)
		binfrac_outfrac.update(_tmp.binfrac_outfrac)
		outinratio.update(_tmp.outinratio)
		doutinratio.update(_tmp.doutinratio)
		inc_wrongfrac.update(_tmp.inc_wrongfrac)
		binfrac_wrongfrac.update(_tmp.binfrac_wrongfrac)
		cfactor.update(_tmp.cfactor)
		lambdajesup.update(_tmp.lambdajesup)
		lambdajesdn.update(_tmp.lambdajesdn)

	with open(datacardInputs+'/inputs_sig_'+obsName+'.py', 'w') as f:
		f.write('acc = '+str(acc)+' \n')
		f.write('dacc = '+str(dacc)+' \n')
		f.write('acc_4l = '+str(acc_4l)+' \n')
		f.write('dacc_4l = '+str(dacc_4l)+' \n')
		f.write('eff = '+str(eff)+' \n')
		f.write('deff = '+str(deff)+' \n')
		f.write('inc_outfrac = '+str(inc_outfrac)+' \n')
		f.write('binfrac_outfrac = '+str(binfrac_outfrac)+' \n')
		f.write('outinratio = '+str(outinratio)+' \n')
		f.write('doutinratio = '+str(doutinratio)+' \n')
		f.write('inc_wrongfrac = '+str(inc_wrongfrac)+' \n')
		f.write('binfrac_wrongfrac = '+str(binfrac_wrongfrac)+' \n')
		f.write('cfactor = '+str(cfactor)+' \n')
		f.write('lambdajesup = '+str(lambdajesup)+' \n')
		f.write('lambdajesdn = '+str(lambdajesdn)+' \n')

# collect('mass4l')
# collect('rapidity4l')
# collect('pT4l')
# collect('njets_pt30_eta4p7')
# collect('njets_pt30_eta2p5')
# collect('pt_leadingjet_pt30_eta4p7')
# collect('pt_leadingjet_pt30_eta2p5')
# collect('massZ2')
# collect('cosThetaStar')
# collect('cosTheta1')
# collect('cosTheta2')
# collect('Phi')
# collect('Phi1')
