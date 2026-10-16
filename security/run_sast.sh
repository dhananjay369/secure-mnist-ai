#!/bin/sh
set -eu
mkdir -p results/sast
bandit -r security/sast_before.py -f txt > results/sast/before.txt || true
bandit -r security/sast_fixed.py -f txt > results/sast/after.txt || true
echo 'SAST reports written to results/sast/'
