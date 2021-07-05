#!/usr/bin/python3
import os
import argparse
import re
import sys

regex = r".*FORMULA ([\S]*) ([\S]*) TECHNIQUES .*@@@([^,]*),([^@]*)@@@"
stats_regex = r".*FORMULA [\S]* STATS EXPLORED (\d+)"
query_red_str = "COLLATERAL_PROCESSING STRUCTURAL_REDUCTION QUERY_REDUCTION"

if __name__ == "__main__":
    parser = argparse.ArgumentParser("This utility translates the output of a run_sc output folder into a csv containing the data.")
    parser.add_argument("folder", help="Path to the folder containing the output files.")
    parser.add_argument("--non_match", help="A file to dump the contents of the non matching files to. Can be used to determine inputs that error.")
    parser.add_argument("--count_queries", help="A file to dump the total number of queries to.")
    parser.add_argument("--filter", help="Include only query files containing given string.")
    parser.add_argument("--progress", help="Print progress to stderr", action='store_true')
    
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"{args.folder} is not a directory", file=sys.stderr)
        exit(1)

    if args.non_match is not None:
        non_match = open(args.non_match, 'w')
    else:
        non_match = None

    if args.count_queries is not None:
        with open(args.count_queries, "w") as file:
            print(len(os.listdir(args.folder)), file=file)


    num_files=len(os.listdir(args.folder))
    for i, output_file in enumerate(os.listdir(args.folder)):
        if args.progress and (i % 1000) == 0:
            print(f"{i}/{num_files}", file=sys.stderr)
        if not (output_file.endswith("LTLCardinality") or output_file.endswith("LTLFireability")):
                continue
        try:
            with open(os.path.join(args.folder, output_file), 'r') as file:
                try:
                    file_contents = file.read()
                except UnicodeDecodeError:
                    print(f"error reading file {output_file}")
                    raise
                if file_contents == "":
                    continue
                match = re.match(regex, file_contents, re.DOTALL)
                stats = re.match(stats_regex, file_contents, re.DOTALL)
                if args.filter and args.filter not in file_contents:
                    continue
                if match:
                    groups = list(match.groups())
                    if stats:
                        groups.append(stats.group(1))
                    else:
                        groups.append("-1")
                    print(','.join([f"{groups[0]}-{output_file[output_file.rfind('LTL'):][:4]}"] + groups[1:])) 
                elif non_match is not None:
                    print(output_file, file=non_match)
                    print(file_contents, file=non_match)

        except IOError:
            print(f"Unable to open {output_file}.", file=sys.stderr)
