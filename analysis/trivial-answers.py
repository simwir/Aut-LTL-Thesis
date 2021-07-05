#!/usr/bin/env python3

import argparse

from common import import_csv
from glob import glob


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs='+', help="Input range for computing trivial instances. Should include all experiments to ensure consistency.")

    args = parser.parse_args()

    bad = set()
    nstates = {}
    for fname in args.inputs:
        with open(fname) as f:
            rows = import_csv(f)
            for q, row in rows.items():
                if row.states == -1:
                    bad.add(q)
                elif q in nstates:
                    nstates[q] += row.states
                else:
                    nstates[q] = row.states

    bad |= set(q for q, n in nstates.items() if n == 0)

    for q in sorted(bad):
        print(q)
