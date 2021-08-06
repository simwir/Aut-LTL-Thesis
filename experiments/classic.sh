#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "classic" -r "-s DFS --ltl-por classic" verifypn-linux64 mcc2020
cd experiments
