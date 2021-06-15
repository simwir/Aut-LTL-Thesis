#!/bin/bash

set +x

cd experiments
for f in $(ls); do
    ./$f
done
cd ..
