#!/usr/bin/python3

import os
import sys
import argparse
import csv

NUM_QUERIES = 2032 * 16

def calc_correct(input_list, oracle):
    return len(list(filter(lambda x: x[0] in oracle and x[1] == oracle[x[0]], input_list)))

def compare_results(input_list, oracle):
    good = []
    bad = []
    for f in input_list:
        if f[0] not in oracle:
            continue
        if f[1] == oracle[f[0]]:
            good.append(f)
        else:
            bad.append(f)
    return good, bad

def calc_answers_not_in_oracle(input_list, oracle):
    return len(list(filter(lambda x: x[0] not in oracle, input_list)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser("This utility creates statistics about a run_sc run.")
    parser.add_argument("-o", "--oracle", help="File containing the oracle answers. Defaults to single-oracle", default="single-oracle")
    parser.add_argument("-i", "--input", help="The input file. If omitted stdin is used.")
    parser.add_argument("-m", "--print-mismatch", help="Print list of queries with answers inconsistent with oracle", type=argparse.FileType('w'))
    parser.add_argument("-u", "--upper", help="Consider only answers obtained within specified duration (in minutes)", type=float)
    parser.add_argument("--no-query", help="Exclude answers obtained directly from query simplification", action='store_true')

    args = parser.parse_args()


    try:
        oracle = {}
        with open(args.oracle, 'r') as oracle_file:
            oracle_reader = csv.reader(oracle_file)
            for row in oracle_reader:
                oracle[row[0]] = row[1].strip()
    except IOError:
        print(f"Unable to open the file {args.oracle}", file=sys.stderr)
        raise

    if args.input is not None:
        input_file = open(args.input, 'r')
    else:
        input_file = sys.stdin

    exclude = set()
    if args.no_query:
        with open("simplified") as f:
            exclude = set(q.strip() for q in f.readlines())
        with open("immediate-solve") as f:
            exclude = exclude.union(set(q.strip() for q in f.readlines()))


    n_skipped = 0
    n_skipped_qred = 0
    input_reader = csv.reader(input_file)
    def use_row(row):
        global n_skipped
        global n_skipped_qred
        if row[0].strip() in exclude:
            n_skipped += 1
            n_skipped_qred += 1
            return False
        if args.upper is None or args.upper >= float(row[2]) / 60:
            return True
        n_skipped += 1
        return False

    input_list = list(filter(use_row, input_reader))

    good, bad = compare_results(input_list, oracle)
    num_correct = len(good)
    num_answered = len(input_list)
    num_not_in_oracle = calc_answers_not_in_oracle(input_list, oracle)

    if args.print_mismatch is not None:
        writer = csv.writer(args.print_mismatch)
        for row in bad:
            writer.writerow(row)

    print(f"Number of queries: {NUM_QUERIES}")
    print(f"Number of answers not in oracle: {num_not_in_oracle}")
    print(f"Number of answered queries of all queries: {num_answered}/{NUM_QUERIES}")
    print(f"Percentage answered: {(num_answered/(NUM_QUERIES))*100}%")

    print(f"Number of correct of answered: {num_correct}/{num_answered-num_not_in_oracle}")
    print(f"Percentage correct of answered: {(num_correct/(num_answered-num_not_in_oracle))*100}%")
    if n_skipped > 0:
        print(f"Number of answers from query simplification: {n_skipped_qred}")
        print(f"Total queries answered: {num_answered + n_skipped}")
