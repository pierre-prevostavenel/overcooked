#!/bin/bash

FOLDER="./results"
find "$FOLDER" -maxdepth 1 -type f -exec rm -f {} \;
