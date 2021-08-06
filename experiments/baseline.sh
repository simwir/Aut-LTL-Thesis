#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "baseline" -r "-s DFS --ltl-por none" verifypn-linux64 mcc2020
cd experiments
