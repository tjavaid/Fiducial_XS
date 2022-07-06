import yaml
import io
import argparse
import os
from Input_Info import *


parser = argparse.ArgumentParser(description='Main input options')
parser.add_argument( '-c', dest='channel', default="4l", help='Final state channle chosen for the template')
parser.add_argument( '-b', dest='nbins', default=1, help='nBins for the chosen variable')
parser.add_argument( '-o', dest='observation', default=2, help='Observation in the given bin')
parser.add_argument( '-p', dest='path', default="", help='Path to the folder in which to store the datacards')
parser.add_argument( '-y', dest='year', default='2018', help='Data taking period')
args = parser.parse_args()

channel = args.channel
observation = int(args.observation)
nbins = int(args.nbins)
year = args.year


def CollectFromConfig(config_location = 'test.yaml'):
    Process_names = []
    Process_rate = []
    Nuisances_name = []
    Nuisances_applied_to = []
    Nuisances_type = []
    Nuisances_value = []

    with open(config_location, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        for section in cfg:

            if section == "Processes":
                for item in cfg[section]:
                    Process_names.append(cfg[section][item]['Name'])
                    Process_rate.append(cfg[section][item]['Rate'])

            if section == "Nuissances":
                for item in cfg[section]:
                    Nuisances_name.append(cfg[section][item]['Name'])
                    Nuisances_applied_to.append(cfg[section][item]['Applied_To'])
                    Nuisances_type.append(cfg[section][item]['Type'])
                    Nuisances_value.append(cfg[section][item]['Value'])

    return [Process_names, Process_rate, Nuisances_name, Nuisances_applied_to, Nuisances_type, Nuisances_value]

def DataCardMaker(process_names, process_rate, nbins, current_bin, channel, observation, nuisances_name, nuisances_applied_to, nuisances_type, nuisances_value, path_dir):
        nprocesses = len(process_names)
        bin_name = "a4"
        if channel == "4mu":
            bin_name = "a1"
        if channel == "4e":
            bin_name = "a2"
        if channel == "2e2mu":
            bin_name = "a3"

        datacard_name = '/hzz4l_{}S_13TeV_xs_bin{}.txt'.format(channel, current_bin)
        if nbins == 1:
            datacard_name = '/hzz4l_{}S_13TeV_xs_inclusive_bin{}.txt'.format(channel, current_bin)
            
        with open( path_dir+datacard_name, 'w') as f:
        #print beginning of the datacard

            # f.write("imax "+str(nbins)+"\n") # For multibinned datacards
            f.write("imax 1\n")
	    f.write("jmax *"+"\n")
            f.write("kmax *"+"\n")


            f.write("------------"+"\n")

            f.write("shapes * * hzz4l_{}S_13TeV_xs.Databin{}.root w:$PROCESS".format(channel, current_bin)+"\n") 

            f.write("------------"+"\n")

            f.write("bin "+bin_name+"_recobin{}".format(current_bin)+"\n")
            f.write("observation {}".format(observation)+"\n")

            f.write("------------"+"\n")
            #f.write("## mass window [105.0,140.0]\n")
            f.write("## mass window [{},{}]".format(INPUT_m4l_low, INPUT_m4l_high)+"\n")
            f.write("bin " + (bin_name+"_recobin{} ").format(current_bin)*(nbins + nprocesses - 1) +"\n")

            tmp_line = "process "
            tmp_line2 = "process "
            tmp_line3 = "rate "

            for i in range(nbins):
                tmp_line = tmp_line + process_names[0]+str(i)+ " "
                tmp_line2 = tmp_line2 + "-" + str(i + 1) + " "
                tmp_line3 = tmp_line3 + str(process_rate[0]) + " "


            for i in range(1,nprocesses):
                tmp_line = tmp_line + process_names[i]+" "
                tmp_line2 = tmp_line2 + str(i) + " "
                tmp_line3 = tmp_line3 + str(process_rate[i]) + " "
                
            f.write(tmp_line+"\n")
            f.write(tmp_line2+"\n")
            f.write(tmp_line3+"\n")
            f.write("------------"+"\n")
            #print nuisance parameters and corresponding values 

            for i in range(len(nuisances_name)):

                line = nuisances_name[i] + ' '
                
                if 'param' in nuisances_type[i]:
                    line = line + nuisances_type[i] + " " + nuisances_value[i]
                    f.write (line+"\n")
                    continue
                
                if ("lnN" in nuisances_type[i]) or ("lnU" in nuisances_type[i]):
                    line = line + nuisances_type[i] + ' '

                if "All" in nuisances_applied_to[i][0]:
                    line = line + (nuisances_value[i] + " ")*nbins
                    
                    if "ButZX" in nuisances_applied_to[i][0]:
                        line = line + (nuisances_value[i] + " ")*(nprocesses - 2) + "-"
                    else:
                        line = line + (nuisances_value[i] + " ")*(nprocesses - 1)

                
                else:
                    if process_names[0] in nuisances_applied_to[i]:
                        line = line + (nuisances_value[i] + " ")*nbins
                        nuisances_applied_to[i].remove(process_names[0])
                    else:
                        line = line + ("- ")*nbins
                    
                    indices_list = []
                    values_list = []
                    for j in range(len(nuisances_applied_to[i])):
                        if nuisances_applied_to[i][j] in process_names:
                            indices_list.append(process_names.index(nuisances_applied_to[i][j]))
                            values_list.append(nuisances_value[i])
                    
                    mini_list = ["-" for m in range(nprocesses-1)]

                    for idx in range(len(indices_list)):
                        mini_list[indices_list[idx] - 1] = values_list[idx]

                    for idx in range(len(mini_list)):
                        line = line + mini_list[idx] + ' ' 

                f.write(line+"\n")
             
            f.write('zz_norm_0 rateParam {}_recobin{} bkg_*zz 1 [0,2]'.format(bin_name, current_bin))


Inputs = CollectFromConfig("Inputs/inputs_{}_{}.yml".format(channel, year))
process_names = Inputs[0]
process_rate = Inputs[1]
nuisances_name = Inputs[2]
nuisances_applied_to = Inputs[3]
nuisances_type = Inputs[4]
nuisances_value = Inputs[5]

path_dir = args.path

folder_name = 'xs_125.0_{}bins'.format(nbins)
if nbins == 1:
    folder_name = 'xs_125.0_{}bin'.format(nbins)

if not (path_dir == ''):
    path_dir = path_diri + "/" + folder_name
else:
    path_dir = folder_name

if not os.path.exists(path_dir):
    os.mkdir(path_dir)
    

for current_bin in range(nbins):
    DataCardMaker(process_names, process_rate, nbins, current_bin, channel, observation, nuisances_name, nuisances_applied_to, nuisances_type, nuisances_value, path_dir)
