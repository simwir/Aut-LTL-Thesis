#!/bin/bash

set +x

BIN="$1"
F=mcc2020
SCRIPTS="$2"

if [[ ! -f "parallel-bin/$BIN" ]] ; then
	echo "$BIN is not a file"
	exit 1
fi

mkdir -p "output/${BIN}-TIMED/"
COUNT=$(ls $F | wc -l)
for t in LTL{Cardinality,Fireability} ; do
    if [[ -z $3 ]] ; then
        parallel -P 25% ./run_benchkit.sh $SCRIPTS $BIN $t {} :::: <(seq 1 $COUNT)
    else
        sbatch --array=1-$COUNT -n 1 -c 4 --output="slurm-dump/job-%j" --job-name=$BIN ./run_benchkit.sh $SCRIPTS $BIN $t
    fi
done
