#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "reach+dist-heur" -r "-s BestFS --ltl-heur dist --ltl-por reach" verifypn-linux64 mcc2020
cd experiments
