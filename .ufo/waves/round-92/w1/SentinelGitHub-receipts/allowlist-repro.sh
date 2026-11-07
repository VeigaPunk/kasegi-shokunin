#!/usr/bin/env bash
# SentinelGitHub r92 — reproduction of D3 (allowlist row keyed on a path spelling)
# and of D4's remediation (one row per published example value).
# Usage: bash allowlist-repro.sh LANE "$S"   (writes only under $S)
set -u
L=${1:?lane}; S=${2:?scratch}; REV=58c0c115342877ee556cae19928d69839b0b29f0
D=$(mktemp -d -p "$S") || exit 2
for f in capture-secret-scan.py claim-package-check.py capture-secret-allow.tsv; do
  git -C "$L" show "$REV:corpus/instruments/$f" > "$D/$f" || exit 2
done
P="gh""p""_"
EX="${P}16C7e42F292c6912E7710c838347Ae178B4a"     # published example, 40 chars
OT="${P}AbCdEfGhIjKlMnOpQrStUvWxYz0123456789"     # a different value, same path shape
R1=$(mktemp -d -p "$S") || exit 2
git -C "$R1" init -q || exit 2
[ "$(git -C "$R1" rev-parse --show-toplevel)" = "$R1" ] || { echo "toplevel mismatch"; exit 2; }
mkdir -p "$R1/corpus/source-snapshots/round-92"
printf 'export GH_TOKEN=%s\n' "$EX" > "$R1/corpus/source-snapshots/round-92/S999.txt"
printf 'export GH_TOKEN=%s\n' "$OT" > "$R1/corpus/source-snapshots/round-92/S998.txt"
git -C "$R1" add -A && git -C "$R1" -c user.name=f -c user.email=f@invalid commit -q -m plant || exit 2
REV1=$(git -C "$R1" rev-parse HEAD)
DIG=$(python3 -c "import hashlib,sys;sys.stdout.write(hashlib.sha256(sys.argv[1].encode()).hexdigest())" "$EX")
AL="$D/allow-one.tsv"
printf 'corpus/source-snapshots/round-92/S999.txt\tgithub-token\t%s\tpublished documentation example value\n' "$DIG" > "$AL"
run() { python3 -B "$D/capture-secret-scan.py" "$@" | grep -E '^(HIT|CAPTURE-SECRET-SCAN)'; }
echo "== (a) rev mode, no allowlist";      run --lane "$R1" --rev "$REV1" --allow /dev/null
echo "== (b) rev mode, one row";           run --lane "$R1" --rev "$REV1" --allow "$AL"
echo "== (c) files mode, absolute path";   run --files "$R1/corpus/source-snapshots/round-92/S999.txt" --allow "$AL"
echo "== (d) files mode, repo-relative";   ( cd "$R1" && run --files corpus/source-snapshots/round-92/S999.txt --allow "$AL" )
rm -rf -- "$D" "$R1"
