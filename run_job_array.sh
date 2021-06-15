#!/bin/bash
#SBATCH --time=17:00:00
#SBATCH --mail-type=FAIL,END

if [[ -z $SLURM_ARRAY_TASK_ID ]] ; then
    SLURM_ARRAY_TASK_ID=$6
fi

let "m=$3*1024*1024"
ulimit -v $m
MODEL=$(ls "$5" | sed -n "${SLURM_ARRAY_TASK_ID}p")
echo "SLURM_ARRAY_TASK_ID: $SLURM_ARRAY_TASK_ID"
echo "MODEL: $MODEL"
for i in $(seq 1 16) ; do
    CMD=$(echo $1 | sed -e "s/QUERY_PLACEHOLDER/$i/g" | sed -e "s/MODEL_PLACEHOLDER/$MODEL/g")
    OUT=$(echo $2 | sed -e "s/QUERY_PLACEHOLDER/$i/g" | sed -e "s/MODEL_PLACEHOLDER/$MODEL/g")


    echo "$CMD &> $OUT" 
    timeout ${4}m /usr/bin/time -f "@@@%e,%M@@@" $CMD &> $OUT
done
exit 0
