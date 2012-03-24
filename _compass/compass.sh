#!/bin/bash
# compass.sh - run the "Compass" program

BASE=$(dirname $(readlink -f $(which "$0")))
cd $BASE
export GEM_HOME=$BASE/Gem
export RUBYLIB=$BASE/Gem/lib
$BASE/Gem/bin/compass "$@"
