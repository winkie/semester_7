#!/bin/bash

declare signal=15

function print_help()
{
   echo -e "\nGo away!"
}

function my_kill_all()
{
   if [ $# -ne 1 ]; then
      return
   fi
   
   echo "Killing $1"  
   pids=$(pgrep $1)
   
   for pid in $pids
   do
      kill -$signal $pid
   done
}

function main()
{
   if [ $# -eq 0 ]; then
      echo "No arguments"
      print_help
      return 
   fi
   
   #first char of the first parameter
   local start=1
   if [ ${1:0:1} == "-" ]; then
      signal=${1:1}
      start=2
   fi
   
   if [ $signal -le 0 -o $signal -ge 31 ]; then
      echo "Wrong signal number!"
      return
   fi
   
   for i in $(seq $start $#)
   do
      my_kill_all ${@:$i:1}
   done
}

main $@
