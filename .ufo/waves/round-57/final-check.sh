#!/usr/bin/env bash
# Read committed export and run OSV + retained guards; regenerate owned census pair last.
# Exit 0 expected results, 1 unexpected result, 2 export/setup error. Scratch removed on exit.
set -u
set -o pipefail
lane=$(git rev-parse --show-toplevel) || exit 2
ref=$(git rev-parse HEAD) || exit 2
scratch=$(mktemp -d /workspace/scratch/e2fdad13233f/kasegi-r57-export.XXXXXX) || exit 2
trap 'rm -rf "$scratch"' EXIT
printf 'run-utc=%s\nmeasured-ref=%s\n' "$(date -u +%FT%TZ)" "$ref"
git archive "$ref" | tar -x -C "$scratch" || exit 2
export GIT_DIR="$lane/.git" GIT_WORK_TREE="$scratch" PYTHONDONTWRITEBYTECODE=1
bad=0
run() { local want=$1; shift; printf '\nCOMMAND '; printf '%q ' "$@"; printf '\n'; "$@"; local rc=$?; printf 'exit=%s expected=%s\n' "$rc" "$want"; [ "$rc" = "$want" ] || bad=$((bad+1)); }
cd "$scratch" || exit 2
run 0 python3 corpus/instruments/osv-semantic-check.py
run 0 python3 corpus/instruments/osv-semantic-check.py --selftest
run 0 python3 .ufo/waves/round-57/mutations.py
run 0 python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089
run 0 python3 corpus/instruments/source-recheck.py --selftest
run 0 python3 corpus/instruments/figure-audit.py
run 0 python3 corpus/instruments/capture-binding-check.py
run 1 python3 corpus/instruments/frontier-recheck-count.py
run 0 env PATH="/workspace/scratch/e2fdad13233f/shokunin-training/tooling/bin:$PATH" bash /workspace/scratch/e2fdad13233f/shokunin-training/shokunin/scripts/sources-census.sh validate --file "$scratch/corpus/SOURCES.md"
run 0 python3 corpus/instruments/score-gap.py
run 0 python3 - <<'PY'
import hashlib,json,pathlib,subprocess
base='eae1d614542e8d30d77e9f4e8b9dea6a11aad138'
declarations=json.loads(pathlib.Path('.ufo/waves/round-57/append-declarations.json').read_text())
for p,d in declarations.items():
 data=pathlib.Path(p).read_bytes();old=subprocess.check_output(['git','show',base+':'+p])
 assert data[:len(old)]==old,p
 assert hashlib.sha256(old).hexdigest()==d['base_sha256'],p
 assert hashlib.sha256(data[len(old):]).hexdigest()==d['append_sha256'],p
 print('APPEND '+p+' old-bytes-preserved=true declared-suffix=true')
for p in ['LOG.md','SCORECARD.md','corpus/QUALITY.md','corpus/lessons/round-50.md']:
 old=subprocess.check_output(['git','show',base+':'+p]);assert pathlib.Path(p).read_bytes().startswith(old);print('PREFIX '+p+' preserved=true')
old=subprocess.check_output(['git','show',base+':corpus/SOURCES.md']).decode().splitlines();new=pathlib.Path('corpus/SOURCES.md').read_text().splitlines();it=iter(new);assert all(any(x==y for y in it) for x in old)
print('SOURCES existing-lines-preserved=true')
m=json.loads(pathlib.Path('corpus/source-snapshots/round-57/manifest.json').read_text());print('located-quote-words='+str(sum(len(q['quote'].split()) for q in m['sources'][0]['quotes'])))
pathlib.Path('base-skill.md').write_bytes(subprocess.check_output(['git','show',base+':SKILL.md']))
PY
run 0 python3 corpus/instruments/density.py base-skill.md --label base
run 0 python3 corpus/instruments/density.py SKILL.md --label after
run 0 bash -c "grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md; grep -cE '^\\| F[0-9]+ \\|' corpus/README.md"
printf 'export-size='; du -sh "$scratch"
# Source availability census is a distinct host-dependent metric; do not claim its increase.
unset GIT_DIR GIT_WORK_TREE
cd "$lane" || exit 2
run 0 python3 corpus/instruments/resolve.py .
run 0 python3 corpus/instruments/census-freshness-check.py .
printf 'FINAL unexpected-results=%s\n' "$bad"
[ "$bad" -eq 0 ]
