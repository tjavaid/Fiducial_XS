import sys
import os
import argparse

# INFO: Following items are imported from either python directory or Inputs
from Input_Info import *
from Utils import *

def collect(obsName, year):
	global datacardInputs

	datacardInputs = datacardInputs.format(year = year)
	sys.path.append('./' + datacardInputs)

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
		border_msg("module to import: "+'inputs_sig_'+obsName.replace(' ','_')+'_'+ch+".py")
		_tmp = __import__('inputs_sig_'+obsName.replace(' ','_')+'_'+ch, globals(), locals(), -1)

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

	with open( datacardInputs + '/inputs_sig_'+obsName.replace(" ","_")+'.py', 'w') as f:
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

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Input arguments')
	parser.add_argument( '-obs', dest='OBSNAME', default="", type=str, help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
	parser.add_argument( '-y', dest='YEAR', default="2018", type=str, help='Name of the observable, supported: "inclusive", "pT4l", "eta4l", "massZ2", "nJets"')
	args = parser.parse_args()

	print("Start of program: 'collectInputs'")
	collect(args.OBSNAME, args.YEAR)
	print("successfully completed...")
