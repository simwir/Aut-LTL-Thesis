#!/bin/bash

# This is the initialization script for the participation of TAPAAL
# untimed sequntial engine verifypn in the Petri net competition 2016.

# BK_EXAMINATION: it is a string that identifies your "examination"
# BK_TOOL: it is the name of the TAPAAL tool variant to be invoked
# export PATH="$PATH:/home/mcc/BenchKit/bin/"

echo $BK_TOOL

case "$BK_TOOL" in
    tapaal)
        echo "---> " $BK_TOOL " --- TAPAAL"
        $PREFIX/tapaal.sh
                ;;
    *)
        echo "---> Error: Unrecognized BK_TOOL name !!!"  
        exit 0
        ;;
esac
