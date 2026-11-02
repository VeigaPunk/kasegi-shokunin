#!/usr/bin/env bash
set -u
set -o pipefail
lane=$(git rev-parse --show-toplevel) || exit 2
ref=$(git rev-parse HEAD) || exit 2
scratch=$(mktemp -d /workspace/scratch/e2fdad13233f/kasegi-r59-export.XXXXXX) || exit 2
trap 'rm -rf "$scratch"' EXIT
printf 'run-utc=%s\nmeasured-ref=%s\n' "$(date -u +%FT%TZ)" "$ref"
git archive "$ref" | tar -x -C "$scratch" || exit 2
export GIT_DIR="$lane/.git" GIT_WORK_TREE="$scratch" PYTHONDONTWRITEBYTECODE=1
bad=0
run() { local want=$1; shift; printf '\nCOMMAND '; printf '%q ' "$@"; printf '\n'; "$@"; local rc=$?; printf 'exit=%s expected=%s\n' "$rc" "$want"; [ "$rc" = "$want" ] || bad=$((bad+1)); }
cd "$scratch" || exit 2
run 0 python3 corpus/instruments/kernel-report-check.py
run 0 python3 corpus/instruments/kernel-report-check.py --selftest
run 0 python3 .ufo/waves/round-58/mutations.py
run 0 python3 corpus/instruments/kernel-report-assess.py .ufo/waves/round-58/example.json
run 0 python3 corpus/instruments/osv-semantic-check.py
run 0 python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S090
run 0 python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-58/reject/manifest.json --source S091
run 0 python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092
run 0 python3 corpus/instruments/source-recheck.py --selftest
run 0 python3 corpus/instruments/figure-audit.py
run 0 python3 corpus/instruments/capture-binding-check.py
run 1 python3 corpus/instruments/frontier-recheck-count.py
run 1 python3 corpus/instruments/recheck-audit.py
run 0 env PATH="/workspace/scratch/e2fdad13233f/shokunin-training/tooling/bin:$PATH" bash /workspace/scratch/e2fdad13233f/shokunin-training/shokunin/scripts/sources-census.sh validate --file "$scratch/corpus/SOURCES.md"
run 0 python3 corpus/instruments/score-gap.py
run 0 python3 - <<'PY'
import pathlib,subprocess,json,hashlib
base='f17171eac43ce5df67870ef038dbe92273a3a5f3';freeze='106a1c6'
for p in ['LOG.md','SCORECARD.md','SKILL.md','PROVINCE.md','corpus/README.md','corpus/QUALITY.md']:
 old=subprocess.check_output(['git','show',base+':'+p]);assert pathlib.Path(p).read_bytes().startswith(old);print('PREFIX '+p+' preserved=true')
for p in ['.ufo/waves/round-59/CONTRACT.md','.ufo/waves/round-59/freeze.json']:
 assert pathlib.Path(p).read_bytes()==subprocess.check_output(['git','show',freeze+':'+p]);print('FREEZE '+p+' unchanged=true')
old=subprocess.check_output(['git','show',base+':corpus/SOURCES.md']).decode().splitlines();new=pathlib.Path('corpus/SOURCES.md').read_text().splitlines();it=iter(new);assert all(any(x==y for y in it) for x in old);print('SOURCES existing-lines-preserved=true')
print('source-rows-before='+str(sum(x.startswith('| S') and x[3:6].isdigit() for x in old))+' after='+str(sum(x.startswith('| S') and x[3:6].isdigit() for x in new)))
pathlib.Path('base-skill.md').write_bytes(subprocess.check_output(['git','show',base+':SKILL.md']))
print('located-quote-words='+str(sum(len(q['quote'].split()) for q in json.loads(pathlib.Path('corpus/source-snapshots/round-59/manifest.json').read_text())['sources'][0]['quotes'])))
PY
run 0 python3 corpus/instruments/density.py base-skill.md --label before
run 0 python3 corpus/instruments/density.py SKILL.md --label after
printf 'export-size='; du -sh "$scratch"
unset GIT_DIR GIT_WORK_TREE
cd "$lane" || exit 2
run 0 python3 corpus/instruments/resolve.py .
run 0 python3 corpus/instruments/census-freshness-check.py .
printf 'FINAL unexpected-results=%s\n' "$bad"
[ "$bad" -eq 0 ]
