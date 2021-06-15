#!/bin/bash

set -x

mkdir -p mcc2020
git clone https://github.com/yanntm/pnmcc-models-2020.git pnmcc
cd pnmcc
./install_inputs.sh

cd website/INPUTS
for f in $(ls | grep "PT"); do
    tar -xzf $f -C ../../../mcc2020
done

cd ../../../
rm -rf pnmcc
