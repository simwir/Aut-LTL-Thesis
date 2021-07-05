#!/usr/bin/env python3

from collections import namedtuple as _namedtuple
from typing import List, Dict, IO, Iterable, Tuple, Any
import itertools as _itertools
import csv as _csv
import os as _os
import sys as _sys
import argparse as _argparse

########### Input ################

args: Any = None

Row = _namedtuple("Row", ["query", "answer", "time", "memory", "states"])

def import_csv(file):
    reader = _csv.reader(file)
    rows = {}
    for row in reader:
        if len(row) < 5:
            row.append(-1)
        query = row[0].strip()
        rows[query] = Row(
            query=query,
            answer=row[1].strip(),
            time=float(row[2]),
            memory=float(row[3]),
            states=int(row[4]) if len(row) > 4 else -1,
        )
    return rows


def get_argument_parser() -> _argparse.ArgumentParser:
    parser = _argparse.ArgumentParser(
        description="Script for turning .csv answer files into nice LaTeX tables"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=_argparse.FileType("r"),
        help="Input file. If omitted stdin is used.",
        nargs="+",
    )
    parser.add_argument(
        "-n",
        "--names",
        type=str,
        help="Names of each configuration. Used as table heading.",
        nargs="+",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="File to output table to.",
    )
    parser.add_argument(
        "-t",
        "--min-time",
        type=int,
        help="Minimum amount of time outside of number of answers tables (in s).",
        default=5
    )
    parser.add_argument(
        "-q",
        "--query-simplification",
        action='store_true',
        help="Include answers obtained by query simplifications in the final result."
    )

    return parser


def parse_program_arguments(parser=None):
    if parser is None:
        parser = get_argument_parser()
    _args = parser.parse_args()

    if _args.output is None:
        print("Error: Missing output file.")
        _sys.exit(1)

    if not len(_args.input) == len(_args.names):
        print("Error: Mismatching number of inputs and names")
        _sys.exit(1)

    global args
    args = _args
    return args



########### Output ################

outdir = _os.getcwd()
outfile = None
def sout(*args):
    global outfile
    print(*args, end="", file=outfile)


def soutln(*args):
    sout(*args)
    sout("\n")


def set_outdir(odir):
    global outdir
    outdir = odir


def open_file(fname, mode):
    global outfile
    outfile = open(fname, mode)
    return outfile


def _print_value(val):
    if type(val) == int or type(val) == float:
        sout(f"\\num{{{val}}}")
    else:
        sout(val)


def table_row(row_contents, spacing=None):
    for i in range(len(row_contents) - 1):
        _print_value(row_contents[i])
        sout(" & ")
    _print_value(row_contents[-1])
    soutln(r" \\" + (f"[{spacing}]" if spacing is not None else ""))


def table_head_row(headers):
    def __print_centered(val):
        if val.strip() != "":
            if "multicolumn" in val:
                sout(val)
            else:
                sout(r"\multicolumn{1}{c}{" + val + "}")
    # TODO center header fields rather than defer call
    for i in range(len(headers) - 1):
        __print_centered(headers[i])
        sout(" & ")
    __print_centered(headers[-1])
    soutln(r"\\")
    #soutln(f"\\centering {headers[-1]}\\\\")


def table_header(colfmt: str):
    # TODO can make tabularx with textwidth
    soutln(r"\begin{tabular}{@{}" + colfmt + "@{}}")
    soutln(r"\toprule")


def table_midrule():
    soutln(r"\midrule")


def table_footer():
    soutln(
        r"""\bottomrule
\end{tabular}"""
    )


########### Computations ################
exclude = None

def _query_filter(row):
    global exclude
    global immediately_solved
    if args.query_simplification:
        return True
    if exclude is None:
        with open("exclude") as f:
            exclude = set(q.strip() for q in f.readlines())
    return row.query not in exclude


def get_ltlc_positive(data: Dict[str, Row], use_filter=True):
    return filter(lambda r: r[1].query.endswith('LTLC')
                  and r[1].answer == "TRUE"
                  and (_query_filter(r[1]) if use_filter else True), data.items())

def get_ltlc_negative(data: Dict[str, Row], use_filter=True):
    return filter(lambda r: r[1].query.endswith('LTLC')
                  and r[1].answer == "FALSE"
                  and (_query_filter(r[1]) if use_filter else True), data.items())

def get_ltlf_positive(data: Dict[str, Row], use_filter=True):
    return filter(lambda r: r[1].query.endswith('LTLF')
                  and r[1].answer == "TRUE"
                  and (_query_filter(r[1]) if use_filter else True), data.items())

def get_ltlf_negative(data: Dict[str, Row], use_filter=True):
    return filter(lambda r: r[1].query.endswith('LTLF')
                  and r[1].answer == "FALSE"
                  and (_query_filter(r[1]) if use_filter else True), data.items())

def calculate_score(base, other, pred: str = None):
    ntime = 0
    nmemory = 0
    nstates = 0
    nexclusive = 0
    factor = args.point_threshold / 100.0
    for query, row in dict(other).items():
        if pred and not query.endswith(pred):
            continue
        if query not in base.keys():
            ntime += 1
            nmemory += 1
            nstates += 1
            nexclusive += 1
        else:
            base_answer = base[query]
            if args.min_time and min(row.time, base_answer.time) <= args.min_time:
                continue
            if row.time < base_answer.time * factor:
                ntime += 1
            if row.memory < base_answer.memory * factor:
                nmemory += 1
            if row.states > 0 and row.states < base_answer.states * factor:
                nstates += 1
    return ntime, nmemory, nstates, nexclusive



def exclusive_answers(left, right):
    keys = set(left.keys()).difference(right)
    return {key: row for key, row in left if key in keys}

########### Table ##############

N_QUERIES = 1016 * 2 * 16

def num_answers_table(dataset, args, fname="num-answered.tex"):
    # TODO exclusive answers?
    with open_file(fname, "w") as f:
        table_header("lrrrrrr")
        table_head_row(["", "LTLC$+$", "LTLC$-$", "LTLF$+$", "LTLF$-$", r"\multicolumn{2}{c}{Total}"])
        table_midrule()

        for name, data in dataset.items():
            ltlc_pos = list(get_ltlc_positive(data))
            ltlc_neg = list(get_ltlc_negative(data))
            ltlf_pos = list(get_ltlf_positive(data))
            ltlf_neg = list(get_ltlf_negative(data))
            ntotal = len(ltlc_pos) + len(ltlc_neg) + len(ltlf_pos) + len(ltlf_neg)
            table_row([
                name,
                len(ltlc_pos),
                len(ltlc_neg),
                len(ltlf_pos),
                len(ltlf_neg),
                ntotal,
                f"\\SI{{{ntotal / (N_QUERIES - len(exclude)):.1%}}}{{\percent}}".replace("%", ""),
            ])

        table_footer()


def percentage_comparison(dataset, args, fname="percentage-diff.tex"):
    def _percent_diff(a, b):
        return f"\\SI{{{(a - b) / b:.1%}}}{{\\percent}}".replace("%", "")

    with open_file(fname, "w") as f:
        table_header("lrrrrr")
        table_head_row(["", "LTLC$+$", "LTLC$-$", "LTLF$+$", "LTLF$-$", "Total"])
        table_midrule()

        baseline = dataset["Baseline"]
        base_ltlc_pos = len(list(get_ltlc_positive(baseline)))
        base_ltlc_neg = len(list(get_ltlc_negative(baseline)))
        base_ltlf_pos = len(list(get_ltlf_positive(baseline)))
        base_ltlf_neg = len(list(get_ltlf_negative(baseline)))
        base_total = base_ltlc_pos + base_ltlc_neg + base_ltlf_pos + base_ltlf_neg
        del dataset["Baseline"]
        for name, data in dataset.items():
            ltlc_pos = len(list(get_ltlc_positive(data)))
            ltlc_neg = len(list(get_ltlc_negative(data)))
            ltlf_pos = len(list(get_ltlf_positive(data)))
            ltlf_neg = len(list(get_ltlf_negative(data)))
            ntotal = ltlc_pos + ltlc_neg + ltlf_pos + ltlf_neg

            table_row([name,
                       _percent_diff(ltlc_pos, base_ltlc_pos),
                       _percent_diff(ltlc_neg, base_ltlc_neg),
                       _percent_diff(ltlf_pos, base_ltlf_pos),
                       _percent_diff(ltlf_neg, base_ltlf_neg),
                       _percent_diff(ntotal, base_total)])
        table_footer()

