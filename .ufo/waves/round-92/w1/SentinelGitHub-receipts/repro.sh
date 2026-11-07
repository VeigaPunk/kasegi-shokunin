#!/usr/bin/env bash
# SentinelGitHub r92 — re-runnable reproduction of the routed C2 findings.
# Usage: S=$(mktemp -d -p /fast/scratch/... ) ; bash repro.sh LANE "$S"
# Writes only under $S. No credential-shaped literal appears in this file: the
# prefix is assembled from parts and the 36-char tail is generated at run time.
set -u
L=${1:?lane}; S=${2:?scratch}; REV=58c0c115342877ee556cae19928d69839b0b29f0
D=$(mktemp -d -p "$S") || exit 2
for f in capture-secret-scan.py claim-package-check.py capture-secret-allow.tsv; do
  git -C "$L" show "$REV:corpus/instruments/$f" > "$D/$f" || exit 2
done
P="gh""p""_"; O="gh""s""_"
T=$(python3 -c "import sys;sys.stdout.write('AbCdEfGhIjKlMnOpQrStUvWxYz0123456789')")
J=$(python3 -c "import sys;sys.stdout.write('eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJGQUtFIn0.FAKEsignatureFAKEsignature')")
B64=$(python3 -c "import base64,sys;sys.stdout.write(base64.b64encode(('x-access-token:'+'ghp_'+'AbCdEfGhIjKlMnOpQrStUvWxYz0123456789').encode()).decode())")
fx() { printf '%s' "$2" > "$D/$1"; }
fx c-control-header.txt   "Authorization: token $P$T
"
fx c-control-netrc.txt    "machine github.com
  password $P$T
"
fx b-pct-separator.json   "{\"t\":\"ghp%5F$T\"}
"
fx b-json-u005f.json      "{\"t\":\"ghp\\\\u005f$T\"}
"
fx b-html-entity.html     "<code>ghp&#95;$T</code>
"
fx b-json-tab.json        "{\"log\":\"a\\\\t$P$T\"}
"
fx b-json-u0020.json      "{\"log\":\"token\\\\u0020$P$T\"}
"
fx b-json-u0026.json      "{\"u\":\"https://h/p?a=1\\\\u0026$P$T\"}
"
fx b-pct-2f.json          "{\"u\":\"https://h/p%2F$P$T\"}
"
fx b-pct-3a.json          "{\"u\":\"https://x-access-token%3A$P$T@github.com/o/r\"}
"
fx b-basic-b64.txt        "Authorization: Basic $B64
"
fx b-softwrap-nokey.txt   "log: ghp_${T:0:18}
${T:18}
"
fx b-finegrained.txt      "github_pat_${T:0:22}_${T}${T}
"
fx fp-asset-id.txt        "https://cdn.example/assets/${O}9fK2mQ7xT4bR1vL8nC5wY3zA0eH6jD2sPuVx/app.js
"
fx fp-placeholder.txt     "Personal access tokens look like $P$(python3 -c "print('x'*36)")
"
fx fp-stateless4seg.txt   "v ${O}1_aaaaaaaaaa.bbbbbbbbbb.cccccccccc.dddddddddd
"
for f in "$D"/*.txt "$D"/*.json "$D"/*.html; do
  id=$(basename "$f")
  out=$(python3 -B "$D/capture-secret-scan.py" --files "$f")
  hit=$(printf '%s\n' "$out" | grep -c '^HIT ')
  shape=$(printf '%s\n' "$out" | sed -n 's/^HIT shape=\([^ ]*\).*/\1/p' | paste -sd, -)
  summ=$(printf '%s\n' "$out" | grep '^CAPTURE-SECRET-SCAN ')
  printf '%s\thits=%s\tshapes=%s\t%s\n' "$id" "$hit" "${shape:-none}" "$summ"
done
rm -rf -- "$D"
