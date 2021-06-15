#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "dist-heur" -r "-s BestFS --ltl-heur dist" verifypn-linux64 mcc2020
cd experiments
