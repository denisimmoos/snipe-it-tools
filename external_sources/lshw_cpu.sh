#!/bin/bash -
#===============================================================================
#
#          FILE: lshw_cpu.sh
#
#         USAGE: ./lshw_cpu.sh
#
#   DESCRIPTION: 
#
#        AUTHOR: Denis Immoos <denisimmoos@gmail.com> (DevOps Engineer)
#  ORGANIZATION: 
#       CREATED: 26.07.2021 14:35:12
#      REVISION:  ---
#===============================================================================

set -o nounset                                  # Treat unset variables as an error
sudo lshw -class cpu -quiet | grep "\: " | sed s/^\ *//g
