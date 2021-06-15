#!/bin/bash

TO=15
ALGORITHM=tarjan
MEMORY=16
while getopts ":t:n:hp:a:r:m:" opt; do
    case $opt in
        t)
            TO=$OPTARG
            #echo "$OPTARG"
            ;;
        n)
            NAME=$OPTARG
            ;;
	p)
	    PARTITION=$OPTARG
	    ;;
	a)
	    ALGORITHM=$OPTARG
	    ;;
	r)
	    ARGUMENTS=$OPTARG
	    ;;
	m)
	    MEMORY=$OPTARG
	    ;;
        h)
            echo "$0 [-t timeout] [-n test_name] [-p partition] [-a algorithm] [-h] [-r program arguments] [-m memory] binary test-folder"
            exit 0
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [[ -z "$2" ]] ; then
	echo "Missing test-folder"
	exit
fi

if [[ -z "$1" ]] ; then
	echo "Missing binary"
	exit
fi


BIN="$1";
N=1
F=$(basename ${2})

if [[ ! -f "sequential-bin/$BIN" ]] ; then
	echo "$BIN is not a file"
	exit
fi

if [[ ! -d "$F" ]] ; then
	echo "$F is not a folder"
	exit
fi


ODIR="output/$F/$NAME"
mkdir -p $ODIR
COUNT=$(ls $F | wc -l)
for t in LTL{Cardinality,Fireability} ; do 
    let "M=$MEMORY+1" ; 
    CMD="sequential-bin/$BIN -n -x QUERY_PLACEHOLDER ./$F/MODEL_PLACEHOLDER/model.pnml ./$F/MODEL_PLACEHOLDER/${t}.xml -ltl $ALGORITHM $ARGUMENTS" 
    OUT="$ODIR/MODEL_PLACEHOLDER.QUERY_PLACEHOLDER.${t}"
    if [[ -z $PARTITION ]] ; then
        parallel ./run_job_array.sh "\"$CMD\"" "\"$OUT\"" $MEMORY $TO $F {} :::: <(seq 1 $COUNT)
    else
        sbatch --array=1-$COUNT -n 1 -c $N --mem="${M}G" --partition=$PARTITION --output="slurm-dump/job-%j" --job-name=$BIN ./run_job_array.sh "$CMD" "$OUT" $MEMORY $TO $F
    fi
done
