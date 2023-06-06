#!/bin/sh

# Директория для хранения csv_file
output=$"/Users/molchanov/dev/baz_auto/csv"

docker run --rm -v $output:/output baz_auto --output /output
