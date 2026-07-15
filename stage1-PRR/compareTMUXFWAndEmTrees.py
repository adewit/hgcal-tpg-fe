import ROOT
import math
import json

def compare_dictionaries(dict_1, dict_2, dict_1_name, dict_2_name, path=""):
    """Compare two dictionaries recursively to find non matching elements

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns: string

    """
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1:
        path = old_path + "[%s]" % k
        if not k in dict_2:
            key_err += "Key %s%s not in %s\n" % (dict_1_name, path, dict_2_name)
        else:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k], dict):
                err += compare_dictionaries(dict_1[k],dict_2[k],dict_1_name,dict_2_name, path)
            else:
                if dict_1[k] != dict_2[k]:
                    value_err += "Value of %s%s (%s) not same as %s%s (%s)\n"\
                        % (dict_1_name, path, dict_1[k], dict_2_name, path, dict_2[k])

    for k in dict_2:
        path = old_path + "[%s]" % k
        if not k in dict_1:
            key_err += "Key %s%s not in %s\n" % (dict_2_name, path, dict_1_name)

    return key_err + value_err + err

detmux_dict = {}
for evt in range(0,128):
    detmux_dict[evt]={}
    for mod in range(0,300):
        detmux_dict[evt][mod]={}
        for col in range(0,10):
            detmux_dict[evt][mod][col]=[]

link_nr = 109
first_tc =0
first_tc_offset=0
first_tc_offset_bc=0
link_offset_board=2 #-2 for BC when running on S026, 0 otherwise
#link_offset_board=0
for evt in range(0,128):
    if (evt%18)==1 or (evt%18)==2:
        first_tc_offset=324
        if(link_offset_board==0):first_tc_offset_bc=324
        else: first_tc_offset_bc=0
    else:
        first_tc_offset=0
        first_tc_offset_bc=0
    for mod in range(0,300):
        link_offset=18*math.floor(mod/50)
        for col in range(0,10):
            if mod%5==0 and col<7:
                if(link_nr-link_offset_board)<94:
                    detmux_dict[evt][mod][col].append((link_nr-link_offset-link_offset_board+18,first_tc+first_tc_offset_bc+32*math.floor((mod%50)/5)+col))
                else:
                    detmux_dict[evt][mod][col].append((link_nr-link_offset-link_offset_board,first_tc+first_tc_offset_bc+32*math.floor((mod%50)/5)+col))
            if mod%5==1 and col<4:
                if(link_nr - link_offset_board)<94:
                    detmux_dict[evt][mod][col].append((link_nr-link_offset-link_offset_board+18,first_tc+first_tc_offset_bc+32*math.floor((mod%50)/5)+7+col))
                else:
                    detmux_dict[evt][mod][col].append((link_nr-link_offset-link_offset_board,first_tc+first_tc_offset_bc+32*math.floor((mod%50)/5)+7+col))
            if mod%5==2 and col<7:
                detmux_dict[evt][mod][col].append((link_nr-link_offset,first_tc+first_tc_offset+32*math.floor((mod%50)/5)+11+col))
            if mod%5==3 and col <3:
                if(mod%50==48):
                    detmux_dict[evt][mod][col].append((link_nr-link_offset,(first_tc+first_tc_offset-324)+32*math.floor((mod%50)/5)+18+col)) #In the FW, TCs corresponding to the last two TC proc in the last link pair sent to a given TMUX link actually corresponds to evt from 18BX later, hence this offset
                else:
                    detmux_dict[evt][mod][col].append((link_nr-link_offset,first_tc+first_tc_offset+32*math.floor((mod%50)/5)+18+col))
            if mod%5==4 and col <3:
                if(mod%50==49):
                    detmux_dict[evt][mod][col].append((link_nr-link_offset,(first_tc+first_tc_offset-324)+32*math.floor((mod%50)/5)+21+col)) #In the FW, TCs corresponding to the last two TC proc in the last link pair sent to a given TMUX link actually corresponds to evt from 18BX later, hence this offset

                else:
                    detmux_dict[evt][mod][col].append((link_nr-link_offset,first_tc+first_tc_offset+32*math.floor((mod%50)/5)+21+col))
    link_nr+=1
    if link_nr>111: 
        link_nr=94
        first_tc+=324

print(detmux_dict[3])


flipped_detmux_dict={}
for link_nr in range(0,112):
    flipped_detmux_dict[link_nr] = {}
    for tc_number in range(0,5000):
        flipped_detmux_dict[link_nr][tc_number] = []

for evt, modcolval in detmux_dict.items():
    for mod, colval in modcolval.items():
        for col, val in colval.items():
            if len(val)>0 and val[0][1]>-1:
                flipped_detmux_dict[val[0][0]][val[0][1]].append((evt, mod, col))


file_fw = ROOT.TFile.Open("out_tmux0907_S026_v4.root")
file_em = ROOT.TFile.Open("TCProcessor_EmulationResults_RandomData_AllBX.root")

tree_fw = file_fw.Get("outtree")
tree_em = file_em.Get("Events")

fw_dict = {}
em_dict = {}
for evt in range(0,128):
    fw_dict[evt]={}
    em_dict[evt]={}
    for mod in range(0,300):
        fw_dict[evt][mod]={}
        em_dict[evt][mod]={}
        for column in range(0,10):
            fw_dict[evt][mod][column]=[]
            em_dict[evt][mod][column]=[]
        
for entry in tree_fw:
    if(entry.link_number > -1):
       evtmodcoltuple = flipped_detmux_dict[entry.link_number][entry.tc_number]
       if len(evtmodcoltuple)>0:
           fw_dict[evtmodcoltuple[0][0]][evtmodcoltuple[0][1]][evtmodcoltuple[0][2]].append((entry.tc_energy,entry.tc_address))

for entry in tree_em:
    em_dict[entry.Event][entry.Module][entry.Column].append((entry.Energy,entry.Address))


#print("FW dict")
#print(json.dumps(fw_dict,indent=4))

#print("EM dict")
#print(json.dumps(em_dict,indent=4))
print("In the printout below, the first index is the module number, the second the column number")
for evt in range(0,128):
    print("Comparing event ",evt)
    a = compare_dictionaries(fw_dict[evt],em_dict[evt],'FW dict','EM dict')
    print(a)
    print("==========================================================================================")
