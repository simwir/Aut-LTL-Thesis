#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "vis-reach-stub" -r "-s DFS --ltl-por mix" verifypn-linux64 mcc2020
cd experiments
