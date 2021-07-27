#!/bin/bash
mflowgen run --design $MC_FLOW_HOME/group/

make cadence-genus-genlib
make mentor-calibre-lvs

mkdir -p outputs
cp -L *cadence-genus-genlib/outputs/design.lib outputs/group_tt.lib
cp -L *cadence-innovus-signoff/outputs/design.lef outputs/group.lef
cp -L *cadence-innovus-signoff/outputs/design-merged.gds outputs/group.gds
cp -L *-lvs/outputs/design_merged.lvs.v outputs/group.lvs.v

