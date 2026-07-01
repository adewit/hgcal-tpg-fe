import ROOT
import argparse


all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-i", "--input_file", type=str, required=True, default="out_fixeden_vallp_uniquetc_bx50.root",
help="Root file with links, tc numbers, energies and addresses")
    
args = all_args.parse_args()

#infile = ROOT.TFile.Open(args.input_file)
#rtree = infile.Get("outtree")

thedataframe = ROOT.RDataFrame("outtree",args.input_file)

injected_energies_stc16 = [lp*2+1 for lp in range (2,62)]
print(injected_energies_stc16)

injected_energies_nonstc16_begin=[lp*2+1 for lp in range (2,8)]
injected_energies_nonstc16_end = [(lp-4)*4+2 for lp in range (8,62)]
injected_energies_nonstc16 = injected_energies_nonstc16_begin+injected_energies_nonstc16_end
print(injected_energies_nonstc16)

bc_highocc_addresses = [11,12,13,14,15,16,19,20,21]
bc_lowocc_addresses = [3,4,5,6]
stc4a_addresses= [1,9,17,25,33,41,45]
stc16_addresses = [2,18,34]

energies_full=[]
energies_notfull=[]
addresses_bchi_cutstr = []
for address in bc_highocc_addresses:
    addresses_bchi_cutstr.append('tc_address==%i'%address)
addresses_bchi = '('+"||".join(addresses_bchi_cutstr)+')'

print('---Checking BC high occupancy---')
for energy in injected_energies_nonstc16:
    full_cut = addresses_bchi+'&&tc_energy==%i'%energy
    #print(full_cut)
    entries_addresscut = thedataframe.Filter(full_cut)
    #print(" energy ",energy," nentries ",entries_addresscut.Count().GetValue()) 
    if(entries_addresscut.Count().GetValue()==7):
        energies_full.append(energy)
        print('Found 7 entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
    else:
        energies_notfull.append(energy)
        #print('Did not find 7 entries for energy ', energy, ', found ',entries_addresscut.Count().GetValue())
        print('Found ',entries_addresscut.Count().GetValue(),' entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
        #display = entries_addresscut.Display({"tc_energy","tc_address","link_number","tc_number"},20)
        #display.Print()
print('Energies for which all expected output was found:')
print(energies_full)
print('Energies for which not all expected output was found:')
print(energies_notfull)
       
energies_full=[]
energies_notfull=[]
addresses_bclo_cutstr = []
for address in bc_lowocc_addresses:
    addresses_bclo_cutstr.append('tc_address==%i'%address)
addresses_bclo= '('+"||".join(addresses_bclo_cutstr)+')'
print('---Checking BC low occupancy---')
for energy in injected_energies_nonstc16:
    full_cut = addresses_bclo+'&&tc_energy==%i'%energy
    #print(full_cut)
    entries_addresscut = thedataframe.Filter(full_cut)
    #print(" energy ",energy," nentries ",entries_addresscut.Count().GetValue()) 
    if(entries_addresscut.Count().GetValue()==4):
        energies_full.append(energy)
        print('Found 4 entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
    else:
        energies_notfull.append(energy)
        #print('Did not find 4 entries for energy ', energy)
        print('Found ',entries_addresscut.Count().GetValue(),' entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
        #display = entries_addresscut.Display({"tc_energy","tc_address","link_number","tc_number"},20)
        #display.Print()
print('Energies for which all expected output was found:')
print(energies_full)
print('Energies for which not all expected output was found:')
print(energies_notfull)
    
energies_full=[]
energies_notfull=[]
addresses_stc4a_cutstr = []
for address in stc4a_addresses:
    addresses_stc4a_cutstr.append('tc_address==%i'%address)
addresses_stc4a= '('+"||".join(addresses_stc4a_cutstr)+')'
print('---Checking STC4A---')
for energy in injected_energies_nonstc16:
    full_cut = addresses_stc4a+'&&tc_energy==%i'%energy
    #print(full_cut)
    entries_addresscut = thedataframe.Filter(full_cut)
    #print(" energy ",energy," nentries ",entries_addresscut.Count().GetValue()) 
    if(entries_addresscut.Count().GetValue()==7):
        energies_full.append(energy)
        print('Found 7 entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
    else:
        energies_notfull.append(energy)
        #print('Did not find 4 entries for energy ', energy)
        print('Found ',entries_addresscut.Count().GetValue(),' entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
        #display = entries_addresscut.Display({"tc_energy","tc_address","link_number","tc_number"},20)
        #display.Print()
print('Energies for which all expected output was found:')
print(energies_full)
print('Energies for which not all expected output was found:')
print(energies_notfull)

energies_full=[]
energies_notfull=[]
addresses_stc16_cutstr = []
for address in stc16_addresses:
    addresses_stc16_cutstr.append('tc_address==%i'%address)
addresses_stc16= '('+"||".join(addresses_stc16_cutstr)+')'
print('---Checking STC16---')
for energy in injected_energies_stc16:
    full_cut = addresses_stc16+'&&tc_energy==%i'%energy
    #print(full_cut)
    entries_addresscut = thedataframe.Filter(full_cut)
    #print(" energy ",energy," nentries ",entries_addresscut.Count().GetValue()) 
    if(entries_addresscut.Count().GetValue()==6):
        energies_full.append(energy)
        print('Found 6 entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
    else:
        energies_notfull.append(energy)
        print('Found ',entries_addresscut.Count().GetValue(),' entries for energy ', energy, ', minimum link ',entries_addresscut.Min('link_number').GetValue(),' maximum link ',entries_addresscut.Max('link_number').GetValue(),' mean  link number ',entries_addresscut.Mean('link_number').GetValue())
        #display = entries_addresscut.Display({"tc_energy","tc_address","link_number","tc_number"},20)
        #display.Print()
print('Energies for which all expected output was found:')
print(energies_full)
print('Energies for which not all expected output was found:')
print(energies_notfull)
