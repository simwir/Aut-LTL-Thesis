#!/usr/bin/env python3

import argparse
import os
import sys
import itertools
#from typing import IO, List, Dict
from common import *


if __name__ == "__main__":
    args = parse_program_arguments()

    dataset = {}
    for input, name in zip(args.input, args.names):
        dataset[name] = import_csv(input)

    num_answers_table(dataset, args, args.output)
