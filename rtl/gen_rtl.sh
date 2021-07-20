#!/bin/bash
if [ -f ../inputs/design.v ]; then
  echo "Using RTL from parent graph"
  mkdir -p outputs
  (cd outputs; ln -s ../../inputs/design.v)
else
  mkdir -p outputs
  cp design.v outputs/design.v
fi
