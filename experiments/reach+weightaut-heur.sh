#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "reach+weightaut-heur" -r "-s BestFS --ltl-por reach --ltl-heur weight-aut" verifypn-linux64 mcc2020
cd experiments
