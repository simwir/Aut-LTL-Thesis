#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "weight-aut-heur+log-fire-count-5000+mix" -r "-s BestFS --ltl-heur sum-composed-weight --log-fire-count-threshold 5000 --ltl-por mix" verifypn-linux64 mcc2020
cd experiments
