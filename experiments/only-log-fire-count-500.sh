#! /bin/bash

cd ..
./run_job.sh -t 15 -m 16 -p dhabi -n "only-log-fire-count-500" -r "--ltl-por none -s BestFS --ltl-heur log-fire-count --log-fire-count-threshold 500" verifypn-linux64 mcc2020
cd experiments
