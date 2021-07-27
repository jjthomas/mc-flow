#=========================================================================
# floorplan.tcl
#=========================================================================
# This script is called from the Innovus init flow step.
#
# Author : Christopher Torng
# Date   : March 26, 2018

#-------------------------------------------------------------------------
# Floorplan variables
#-------------------------------------------------------------------------

set vert_pitch [dbGet top.fPlan.coreSite.size_y]
set horiz_pitch [dbGet top.fPlan.coreSite.size_x]

# Core bounding box margins

set core_margin_t $vert_pitch
set core_margin_b $vert_pitch 
set core_margin_r [expr 5 * $horiz_pitch]
set core_margin_l [expr 5 * $horiz_pitch]

# Margins between glb tiles and core edge
set tile_margin_t [expr 20 * $vert_pitch]
set tile_margin_b [expr 20 * $vert_pitch]
set tile_margin_l [expr 250 * $horiz_pitch]
set tile_margin_r [expr 250 * $horiz_pitch]

set inter_tile_margin_v [expr 40 * max($vert_pitch, $horiz_pitch)]
set inter_tile_margin_h [expr 40 * max($vert_pitch, $horiz_pitch)]

set tiles [get_cells -filter "@ref_name==Core"]
set tile_width [dbGet [dbGet -p2 top.insts.cell.name Core -i 0].cell.size_x]
set tile_height [dbGet [dbGet -p2 top.insts.cell.name Core -i 0].cell.size_y]
set num_tiles [sizeof_collection $tiles]
set tiles_per_row [expr round(sqrt($num_tiles))]
set num_rows [expr ($num_tiles + $tiles_per_row - 1) / $tiles_per_row]

#-------------------------------------------------------------------------
# Floorplan
#-------------------------------------------------------------------------

set core_width [expr ($tiles_per_row * $tile_width) + (($tiles_per_row - 1) * $inter_tile_margin_h) + $tile_margin_l + $tile_margin_r]
set core_height [expr ($num_rows * $tile_height) + (($num_rows - 1) * $inter_tile_margin_v) + $tile_margin_t + $tile_margin_b]

floorPlan -s $core_width $core_height \
             $core_margin_l $core_margin_b $core_margin_r $core_margin_t

setFlipping s

set tile_start_y [expr $core_margin_b + $tile_margin_b]
set tile_start_x [expr $core_margin_l + $tile_margin_l]

set y_loc $tile_start_y
set x_loc $tile_start_x
set tile_no 0
# TODO guarantee that this iteration is in order from tile0 ... n
foreach_in_collection tile $tiles {
  set tile_name [get_property $tile full_name]
  placeInstance $tile_name $x_loc $y_loc -fixed

  # Create M3 & M8 pg net blockage to prevent DRC from interaction
  # with tile stripes
  set llx [dbGet [dbGet -p top.insts.name $tile_name].box_llx]
  set lly [dbGet [dbGet -p top.insts.name $tile_name].box_lly]
  set urx [dbGet [dbGet -p top.insts.name $tile_name].box_urx]
  set ury [dbGet [dbGet -p top.insts.name $tile_name].box_ury]
  set tb_margin $vert_pitch
  set lr_margin [expr $horiz_pitch * 3]
  createRouteBlk \
    -inst $tile_name \
    -box [expr $llx - $lr_margin] [expr $lly - $tb_margin] [expr $urx + $lr_margin] [expr $ury + $tb_margin] \
    -layer {3 8} \
    -pgnetonly
  
  if {($tile_no + 1) % $tiles_per_row == 0} {
    set x_loc $tile_start_x
    set y_loc [expr $y_loc + $tile_height + $inter_tile_margin_v]
  } else {
    set x_loc [expr $x_loc + $tile_width + $inter_tile_margin_h]
  }
  incr tile_no
}

addHaloToBlock -allMacro [expr $horiz_pitch * 3] $vert_pitch [expr $horiz_pitch * 3] $vert_pitch

