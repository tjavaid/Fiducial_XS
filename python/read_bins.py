import os
import sys

def read_bins(obsBins):
    if not ('vs' in obsBins):

        print("1D measurement selected, reading the observable bins...")

        obs_bins = obsBins.split("|")

        if (not (obs_bins[0] == '' and obs_bins[len(obs_bins)-1]=='')):
            print('BINS OPTION MUST START AND END WITH A |')
            sys.exit()

    # INFO: obs_bins will be something like: ['', '105.0', '140.0', '']
    #       so, remove first and last element from the list
    #       pop(): removes last element, pop(0): removes first element
        obs_bins.pop()
        obs_bins.pop(0)

        print("[INFO] obs_bins is  : {}".format(obs_bins))
        return obs_bins


    else:
        print("Double differential measurement selectied, reading the observable bins...")
        if ( obsBins.count('vs') == 1 and obsBins.count('/') >= 1 ):
            obs_bins1 = obsBins.split(' vs ')[0]
            obs_bins2 = obsBins.split(' vs ')[1]

            obs_bins1 = obs_bins1.split("|")
            obs_bins1.pop(0)
            obs_bins1.pop()

            
            obs_bins2 = obs_bins2.split("/")

            for i in range(len(obs_bins2)):
                obs_bins2[i] = obs_bins2[i].split("|")
                obs_bins2[i].pop(0)
                obs_bins2[i].pop()
            
            obs_bins = []

            for i in range( len(obs_bins1) - 1 ):
                for j in range( len (obs_bins2[i]) - 1 ):
                    obs_bins.append([[obs_bins1[i], obs_bins1[i+1]] , [obs_bins2[i][j], obs_bins2[i][j+1]]])

            print ("First observable binning:")
            print (obs_bins1)
            print ("Second observable binning:")
            print (obs_bins2)

            print ("Final binning:")
            print (obs_bins)
            return obs_bins

        elif ( obsBins.count('vs') > 1 and obsBins.count('/') >= 1 ):
            tmp = obsBins.split(" / ")
            obs_bins = []
            print ("Input given: ")
            print (tmp)
            for i in range(len(tmp)):
                proto_bin = tmp[i].split(" vs ")
                #print(proto_bin)
                 
                proto_2d_bin = []
                for j in range(len(proto_bin)):
                    proto_bin_v2 = proto_bin[j].split("|")[1:len(proto_bin[j].split("|"))-1]
                    proto_2d_bin.append(proto_bin_v2)
                
                #print(proto_2d_bin)

                obs_bins.append(proto_2d_bin)
            print("Final binning: ")
            print(obs_bins)

            return obs_bins

        else:
            print("PLEASE CHECK YOUR BINNING FORMAT")
            sys.exit()

    

#a = read_bins("|0|1|10| vs |0|1| / |30|60|120|350|")
#a = read_bins("|50|80| vs |10|30| / |50|80| vs |30|60| / |80|110| vs |10|25| / |80|110| vs |25|30|")
#variable = "massZ1 vs massZ2"
