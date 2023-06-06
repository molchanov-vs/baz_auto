#!/bin/sh

# Директория для хранения csv_file
output=$"/Users/molchanov/dev/baz_auto/csv"

/usr/local/bin/docker run --rm -v $output:/output baz_auto --output /output
