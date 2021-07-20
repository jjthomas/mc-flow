#!/bin/bash
mflowgen run --design $MC_FLOW_HOME/core/

make cadence-genus-genlib
make mentor-calibre-lvs

mkdir -p outputs
cp -L *cadence-genus-genlib/outputs/design.lib outputs/core_tt.lib
cp -L *cadence-innovus-signoff/outputs/design.lef outputs/core.lef
cp -L *cadence-innovus-signoff/outputs/design-merged.gds outputs/core.gds
cp -L *-lvs/outputs/design_merged.lvs.v outputs/core.lvs.v

