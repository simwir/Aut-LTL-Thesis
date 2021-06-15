#!/bin/bash
#SBATCH --time=1:15:00
#SBATCH --mail-type=FAIL,END
#SBATCH --mem=16500

# Usage: tool verifypn_binary examination [partition]

if [[ -z $SLURM_ARRAY_TASK_ID ]] ; then
    SLURM_ARRAY_TASK_ID=$4
fi

export BK_TOOL=tapaal
export PREFIX="$(pwd)/scripts/$1"
export VERIFYPN="$(pwd)/parallel-bin/$2"

MODEL=$(ls "./mcc2020" | sed -n "${SLURM_ARRAY_TASK_ID}p")

export BK_EXAMINATION=$3
export BK_TIME_CONFINEMENT=3600
export TEMPDIR=$(mktemp -d)
export LD_LIBRARY_PATH="$(pwd)/parallel-bin"
export MODEL_PATH=$TEMPDIR


mkdir -p BENCHKIT/$1/$2/
mkdir -p $TEMPDIR

F="$(pwd)/BENCHKIT/$1/$2/${MODEL}.${3}"

cp ./mcc2020/$MODEL/* $TEMPDIR
cd $TEMPDIR

let "m=16*1024*1024"
#ulimit -v $m

echo "$PREFIX/BenchKit_head.sh &> $F"
if [ -s "$F" ]
then
	echo "No Redo!"
else
	$PREFIX/BenchKit_head.sh &> $F
fi

rm -r $TEMPDIR
