#ifndef __TMUXConfig_h__
#define __TMUXConfig_h__

#include <vector>
#include <cstdint>  // uint32_t
#include <unordered_map>
#include <cmath>

namespace l1thgcfirmware {
  class TMUXConfig{ 
  public:
    TMUXConfig() {}

    void configureTMUXMap() {
     unsigned link_nr_ = 109;
     unsigned tc_slot_ = 0; 
     for (unsigned iBX=0; iBX<128;iBX++) {
	for (unsigned iModGroup = 0; iModGroup < 60; iModGroup++) {
            unsigned link_offset_=18*std::floor(iModGroup/10);
	    for(unsigned j=0;j<7;j++){//BC High
                ol_and_slot_per_bx_mod_and_col_[iBX][iModGroup * 5][j].push_back(std::make_pair(link_nr_-link_offset_,tc_slot_+32*iModGroup+j));
	    }
	    for(unsigned j=0; j<4;j++) {//BC Low
                ol_and_slot_per_bx_mod_and_col_[iBX][1 + iModGroup * 5][j].push_back(std::make_pair(link_nr_-link_offset_,tc_slot_+32*iModGroup+7+j));
	     }
	    for(unsigned j=0; j<7;j++) {//STC 4
                ol_and_slot_per_bx_mod_and_col_[iBX][2 + iModGroup * 5][j].push_back(std::make_pair(link_nr_-link_offset_,tc_slot_+32*iModGroup+11+j));
	     }
	    for(unsigned j=0; j<3;j++) {//STC 16 
                ol_and_slot_per_bx_mod_and_col_[iBX][3 + iModGroup * 5][j].push_back(std::make_pair(link_nr_-link_offset_,tc_slot_+32*iModGroup+18+j));
                ol_and_slot_per_bx_mod_and_col_[iBX][4 + iModGroup * 5][j].push_back(std::make_pair(link_nr_-link_offset_,tc_slot_+32*iModGroup+21+j));
	     }
	   }
          link_nr_+=1;
	  if(link_nr_>111){
	     link_nr_=94;
	     tc_slot_+=324;
	}
        //
     }
     //This should create something that identifies which input link pairs are sent to which TMUX
     //ie: input link pairs 1-10 go to "TMUX 1", etc etc. 
     //Needs to identify which TC to place first (by column number, and by module type)
     //And position within the TMUX link output (based on ibx)
    }

    std::vector<std::pair<unsigned, unsigned>> getTMUXOLAndSlot(unsigned bx, unsigned moduleId, int columnId) const { return ol_and_slot_per_bx_mod_and_col_.at(bx).at(moduleId).at(columnId); }

  private:
    std::unordered_map<unsigned, std::unordered_map<unsigned, std::unordered_map<int, std::vector<std::pair<unsigned, unsigned>>>>> ol_and_slot_per_bx_mod_and_col_;
  };
}
#endif
