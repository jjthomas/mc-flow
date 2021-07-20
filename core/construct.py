#! /usr/bin/env python
#=========================================================================
# construct.py
#=========================================================================
# Author :
# Date   :
#

import os
import sys

from mflowgen.components import Graph, Step
from shutil import which

def construct():

  g = Graph()

  #-----------------------------------------------------------------------
  # Parameters
  #-----------------------------------------------------------------------

  adk_name = 'tsmc16'
  adk_view = 'view-standard'

  parameters = {
    'construct_path'    : __file__,
    'design_name'       : 'Core',
    'clock_period'      : 1.0,
    'adk'               : adk_name,
    'adk_view'          : adk_view,
    # Synthesis
    'flatten_effort'    : 3,
    # hold target slack
    'hold_target_slack' : 0.030,
    # design size
    'block_size'        : 2
  }

  #-----------------------------------------------------------------------
  # Create nodes
  #-----------------------------------------------------------------------

  this_dir = os.path.dirname(os.path.abspath(__file__))

  # ADK step

  g.set_adk(adk_name)
  adk = g.get_adk_step()

  # Custom steps

  rtl = Step(this_dir + '/../rtl')
  custom_init = Step(this_dir + '/custom-init')
  custom_power = Step(this_dir + '/../common/custom-power-leaf')
  constraints = Step(this_dir + '/../common/constraints')

  # Default steps

  info         = Step('info', default=True)
  synth        = Step('cadence-genus-synthesis', default=True)
  iflow        = Step('cadence-innovus-flowsetup', default=True)
  init         = Step('cadence-innovus-init', default=True)
  power        = Step('cadence-innovus-power', default=True)
  place        = Step('cadence-innovus-place', default=True)
  cts          = Step('cadence-innovus-cts', default=True)
  postcts_hold = Step('cadence-innovus-postcts_hold', default=True)
  route        = Step('cadence-innovus-route', default=True)
  postroute    = Step('cadence-innovus-postroute', default=True)
  postroute_hold = Step('cadence-innovus-postroute_hold', default=True)
  signoff      = Step('cadence-innovus-signoff', default=True)
  genlib       = Step('cadence-genus-genlib', default=True)
  drc          = Step( 'mentor-calibre-drc', default=True)
  lvs          = Step( 'mentor-calibre-lvs', default=True)

  init.extend_inputs(custom_init.all_outputs())
  power.extend_inputs(custom_power.all_outputs())

  #-----------------------------------------------------------------------
  # Graph -- Add nodes
  #-----------------------------------------------------------------------

  g.add_step(info)
  g.add_step(rtl)
  g.add_step(constraints)
  g.add_step(synth)
  g.add_step(iflow)
  g.add_step(init)
  g.add_step(custom_init)
  g.add_step(power)
  g.add_step(custom_power)
  g.add_step(place)
  g.add_step(cts)
  g.add_step(postcts_hold)
  g.add_step(route)
  g.add_step(postroute)
  g.add_step(postroute_hold)
  g.add_step(signoff)
  g.add_step(genlib)
  g.add_step(drc)
  g.add_step(lvs)

  #-----------------------------------------------------------------------
  # Graph -- Add edges
  #-----------------------------------------------------------------------

  # Connect by name

  g.connect_by_name(adk, synth)
  g.connect_by_name(adk, iflow)
  g.connect_by_name(adk, init)
  g.connect_by_name(adk, power)
  g.connect_by_name(adk, place)
  g.connect_by_name(adk, cts)
  g.connect_by_name(adk, postcts_hold)
  g.connect_by_name(adk, route)
  g.connect_by_name(adk, postroute)
  g.connect_by_name(adk, postroute_hold)
  g.connect_by_name(adk, signoff)
  g.connect_by_name(adk, drc)
  g.connect_by_name(adk, lvs)

  g.connect_by_name(rtl, synth)
  g.connect_by_name(constraints, synth)

  g.connect_by_name(synth, iflow)
  g.connect_by_name(synth, init)
  g.connect_by_name(synth, power)
  g.connect_by_name(synth, place)
  g.connect_by_name(synth, cts)

  g.connect_by_name(iflow, init)
  g.connect_by_name(iflow, power)
  g.connect_by_name(iflow, place)
  g.connect_by_name(iflow, cts)
  g.connect_by_name(iflow, postcts_hold)
  g.connect_by_name(iflow, route)
  g.connect_by_name(iflow, postroute)
  g.connect_by_name(iflow, postroute_hold)
  g.connect_by_name(iflow, signoff)

  g.connect_by_name(custom_init, init)
  g.connect_by_name(custom_power, power)
  g.connect_by_name(init, power)
  g.connect_by_name(power, place)
  g.connect_by_name(place, cts)
  g.connect_by_name(cts, postcts_hold)
  g.connect_by_name(postcts_hold, route)
  g.connect_by_name(route, postroute)
  g.connect_by_name(postroute, postroute_hold)
  g.connect_by_name(postroute_hold, signoff)

  g.connect_by_name(signoff, genlib)
  g.connect_by_name(adk, genlib)

  g.connect_by_name(signoff, drc)
  g.connect_by_name(signoff, lvs)
  g.connect(signoff.o('design-merged.gds'), drc.i('design_merged.gds'))
  g.connect(signoff.o('design-merged.gds'), lvs.i('design_merged.gds'))

  #-----------------------------------------------------------------------
  # Parameterize
  #-----------------------------------------------------------------------

  g.update_params(parameters)

  # Increase hold slack on postroute_hold step
  postroute_hold.update_params({'hold_target_slack': parameters['hold_target_slack']}, allow_new=True)

  return g


if __name__ == '__main__':
  g = construct()

