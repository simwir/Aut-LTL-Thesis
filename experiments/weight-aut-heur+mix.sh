#! bin/bash

cd ..
./run_job.sh -t 15 -m 16 -n "weight-aut-heur+mix" -r "-s BestFS --ltl-heur weight-aut --ltl-por mix" verifypn-linux64 mcc2020
cd experiments
