# Aut-LTL-Thesis
Reproducibility package for the Automata-driven LTL extension of the verifypn model checker for TAPAAL.
This package includes the answers and the data analysis used for creating the master thesis of Nikolaj Jensen Ulrik and Simon Mejlby Virenfeldt.

## Usage

The data processing scripts assume a Unix-like environment (e.g. Linux) with Python 3 (3.9.5 tested, however earlier versions may work), and the supplied binaries assume 64-bit Linux.

### Model checker
#### Install dataset
To run the model checker the first step is to install the models by running the `install_models.sh` script.
This script uses https://github.com/yanntm/pnmcc-models-2020 to download and extract the models from the competition and then it extracts them to the relevant location.
#### Single Configuration

1. Run the desired experiment from the `experiments` folder or run `all_experiments.sh`.
2. The answers are available in `output/mcc2020`.

#### MCC setup

1. Run `run_mcc.sh`.
2. The answers are now available in the `BENCHKIT` folder.

### Data analysis
Data analysis is done using various Python 3 scripts located in `analysis`. All scripts (excluding `common.py`) have usage strings via `-h` (e.g. `python analysis/to_csv.py -h`), which may contain more options than detailed here.

#### Using our results

The raw data from our thesis is available in the two files `output.tar.gz` and `BENCHKIT.tar.gz`. Extract these files to perform data analysis on our results (1.8 GiB when unpacked).
For data analysis on your own data, simply proceed to the next step.

``` sh
$ tar -xzf output.tar.gz && tar -xzf BENCHKIT.tar.gz
```

#### Preprocessing

Our data processing scripts assume a CSV representation obtainable via `to_csv.py`. 
If the raw results are located in `output/mcc2020/foo`, `python analysis/to_csv.py output/mcc2020/foo` will write the CSV representation to stdout, which we recommend redirecting to a file like so:

``` sh
$ python analysis/to_csv.py output/mcc2020/foo > csv/foo.csv
```

The plots and tables in the thesis exclude answers obtained trivially, either due to no valid initial state or due to query simplification. 
To compute these based on CSV files `csv/foo.csv` and `csv/bar.csv`:

``` sh
$ python analysis/trivial-answers.py csv/foo.csv csv/bar.csv > exclude
```

#### Basic Statistics

A rudimentary statistical overview can be obtained using `stats-generator.py`, for example (assuming `baseline.csv` is created from `output/mcc/baseline` from our results)

``` sh
$ python analysis/stats-generator.py -i csv/baseline.csv
Number of queries: 32512
Number of answers not in oracle: 9931
Number of answered queries of all queries: 29103/32512
Percentage answered: 89.5146407480315%
Number of correct of answered: 19172/19172
Percentage correct of answered: 100.0%
```

Alternately, the CSV input can be obtained directly from stdin, which allows for the following useful workflows:

``` sh
python analysis/to_csv.py output/mcc2020/foo | python analysis/stats-generator.py
python analysis/to_csv.py output/mcc2020/foo | tee csv/foo.csv | python analysis/stats-generator.py
```

The notion of "correct" used here depends on oracle files from https://github.com/yanntm/pnmcc-models-2020, which we gather into a single, sorted file (default `single-oracle`).
The oracle file for the 2020 dataset is provided; for other datasets, the single oracle can be obtained as follows (assuming oracles formatted as in the repo are located in `./oracle`).

``` sh
$ for file in $(find . -name "*LTLF.out"); do grep "\(TRUE\|FALSE\) TECHNIQUES" $file; done | sed -E "s/FORMULA (.*)-([[:digit:]]+) (TRUE|FALSE).*/\1-LTLF-\2, \3/" > ../tmp
$ for file in $(find . -name "*LTLC.out"); do grep "\(TRUE\|FALSE\) TECHNIQUES" $file; done | sed -E "s/FORMULA (.*)-([[:digit:]]+) (TRUE|FALSE).*/\1-LTLC-\2, \3/" >> ../tmp
$ sort tmp > single-oracle-new
$ rm tmp
```

Then the new oracle file can be selected using `stats-generator.py -o single-oracle-new`.

#### Filtering trivial instances

The plots and tables in the thesis exclude answers obtained trivially, either due to no valid initial state or due to query simplification. 
To compute these based on CSV files `csv/foo.csv` and `csv/bar.csv`:

``` sh
$ python analysis/trivial-answers.py csv/foo.csv csv/bar.csv > exclude
```

#### Tables

The tables are output to `.tex` files containing just a `tabular` environment. The tables depend on the `siunitx` package. To modify the style or contents of the tables (e.g. if you want to avoid the `siunitx` dependency), we refer to `analysis/common.py`.

A tables is generated from a list of inputs and a list of row names, which are paired up (both must have the same length!).
For example, a table with rows Foo and Bar can be generated from `foo.csv` and `bar.csv` with

``` sh
$ python analysis/make-table.py --inputs foo.csv bar.csv --names Foo Bar -o foo-bar-answered.tex
```

By default, the tables exclude trivially obtained answers listed in the file `exclude`. To include everything, use the `-q` option.

#### Plots

The cactus plots are generated using `analysis/cactus_plots.py` (depends on `matplotlib`, 3.4.1 used, and a usable `pdflatex` for TeX fonts).
Like `make-table.py`, the cactus plots are given a list of CSV files and a list of labels.
In the thesis, for each comparison there is a cactus plot with a minimum time of 1 second and a cactus plot showing the top 1500 indices, obtainable as follows:

``` sh
python analysis/cactus_plots.py --input $INPUTS --names $NAMES --virtual-best -o cactus-all --no-simplification -m 1
python analysis/cactus_plots.py --input $INPUTS --names $NAMES --virtual-best -o cactus-tail --no-simplification --tail 1500 --no-legend
```

By defauls the plots are output as .pdf files. This can be modified using the `-f/--format` option (see the documentation for `matplotlib.pyplot.savefig` for valid formats).

By default, the cactus plots exclude trivially obtained answers listed in the file `exclude`. To include everything, use the `-q` option.
