#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "weight-aut-heur" -r "-s BestFS --ltl-heur weight-aut --ltl-por none" verifypn-linux64 mcc2020
cd experiments
