# Aut-LTL-Thesis
Reproducebility package for the Automata-driven LTL extension of the verifypn model checker for TAPAAL.
This package includes the answers and the data analysis used for creating the master thesis of Nikolaj Jensen Ulrik and Simon Mejlby Virenfeldt.

## Usage
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
#### Using our results

The results from our thesis is available in the two files `output.tar.gz` and `BENCHKIT.tar.gz`. Extract these files to perform data analysis on our results.
