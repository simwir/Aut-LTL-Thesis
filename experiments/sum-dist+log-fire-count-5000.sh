#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "sum-dist+log-fire-count-5000" -r "--ltl-por none --ltl-heur sum-composed-count --log-fire-count-threshold 5000" verifypn-linux64 mcc2020
cd experiments
