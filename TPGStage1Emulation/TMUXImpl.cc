#include "TMUXImpl.h"
#include <cmath>
#include <algorithm>

using namespace l1thgcfirmware;

TMUXImpl::TMUXImpl() {}

unsigned TMUXImpl::run(const l1thgcfirmware::HGCalTriggerCellSACollection& tcs_in,
                       const l1thgcfirmware::TMUXConfig& theConf,
		       unsigned evtnr,
                       l1thgcfirmware::HGCalTriggerCellSACollection& tcs_out) const {

   for (const auto& tc: tcs_in) {
       std::vector<std::pair<unsigned, unsigned>> ol_and_slot= theConf.getTMUXOLAndSlot(evtnr,tc.moduleId(),tc.column());
       tcs_out.push_back(tc);
       unsigned tmux_out_link_ = ol_and_slot[0].first;
       unsigned tmux_out_slot_ = ol_and_slot[0].second;
       tcs_out.back().setTmuxOutputLink(tmux_out_link_);
       tcs_out.back().setTmuxOutputSlot(tmux_out_slot_);
   }
       
  return 0;   
}
