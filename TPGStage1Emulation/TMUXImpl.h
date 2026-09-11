#ifndef __TMUXImpl_h__
#define __TMUXImpl_h__

#include "HGCalTriggerCell_SA.h"
#include "TMUXConfig.h"

#include <vector>
#include <cstdint>        // uint32_t, unsigned
#include <unordered_map>  // std::unordered_map

namespace l1thgcfirmware {
  class TMUXImpl {
  public:
    TMUXImpl();
    ~TMUXImpl() {};
    
    void runAlgorithm() const;

    unsigned run(const l1thgcfirmware::HGCalTriggerCellSACollection& tcs_in,
		 const l1thgcfirmware::TMUXConfig& theConf,
		 unsigned eventnr,
		 l1thgcfirmware::HGCalTriggerCellSACollection& tcs_out) const; //This also needs to take tower sums as input


  };
}
#endif

