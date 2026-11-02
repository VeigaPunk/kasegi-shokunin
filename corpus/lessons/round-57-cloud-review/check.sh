#!/bin/bash
set -uo pipefail
root=$(cd "$(dirname "$0")" && pwd)
cd "$root/export"
export PYTHONDONTWRITEBYTECODE=1 GIT_DIR=/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi/.git GIT_WORK_TREE="$PWD"
echo "review-run-utc=$(date -u +%FT%TZ) candidate=9b1028c00656d2693f4accc513e14c4c180a2f27"
for cmd in 'python3 corpus/instruments/osv-semantic-check.py' 'python3 corpus/instruments/osv-semantic-check.py --selftest' 'python3 .ufo/waves/round-57/mutations.py' 'python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089' 'python3 corpus/instruments/capture-binding-check.py' 'python3 corpus/instruments/figure-audit.py' 'python3 corpus/instruments/frontier-recheck-count.py'; do
 echo "COMMAND $cmd"; bash -c "$cmd"; echo "EXIT=$?"
done
