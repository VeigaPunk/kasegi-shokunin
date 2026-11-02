#!/usr/bin/env bash
set -u
set -o pipefail
lane=$(git rev-parse --show-toplevel) || exit 2
ref=$(git rev-parse HEAD) || exit 2
scratch=$(mktemp -d /workspace/scratch/e2fdad13233f/kasegi-r62-export.XXXXXX) || exit 2
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
run 0 python3 corpus/instruments/osv-semantic-check.py
run 0 python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-62/manifest.json --source S108
run 0 python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-62/reject/manifest.json --source S109
run 0 python3 corpus/instruments/source-recheck.py --selftest
run 0 python3 corpus/instruments/figure-audit.py
run 0 python3 corpus/instruments/capture-binding-check.py
run 1 python3 corpus/instruments/frontier-recheck-count.py
run 1 python3 corpus/instruments/recheck-audit.py --quiet
run 0 env PATH="/workspace/scratch/e2fdad13233f/shokunin-training/tooling/bin:$PATH" bash /workspace/scratch/e2fdad13233f/shokunin-training/shokunin/scripts/sources-census.sh validate --file "$scratch/corpus/SOURCES.md"
run 0 python3 - <<'PY'
import pathlib,subprocess,json,hashlib,re,collections
base='f282e44e17c20d4587977412398a8a5136ae1524'
for p in ['LOG.md','SCORECARD.md','SKILL.md','PROVINCE.md','corpus/README.md','corpus/QUALITY.md']:
 old=subprocess.check_output(['git','show',base+':'+p]);assert pathlib.Path(p).read_bytes().startswith(old);print('PREFIX',p,'preserved=true')
old=subprocess.check_output(['git','show',base+':corpus/SOURCES.md']).decode().splitlines();new=pathlib.Path('corpus/SOURCES.md').read_text().splitlines();it=iter(new);assert all(any(x==y for y in it) for x in old);print('SOURCES existing-lines-preserved=true')
for label,lines in [('before',old),('after',new)]:
 rows=[x.split('|') for x in lines if re.match(r'^\| S\d+ \|',x)];print('CENSUS',label,'rows='+str(len(rows)),'tiers='+str(dict(collections.Counter(x[4].strip() for x in rows))),'status='+str(dict(collections.Counter(x[8].strip() for x in rows))))
for p in ['.ufo/waves/round-62/CONTRACT.md','.ufo/waves/round-62/freeze.json','.ufo/waves/round-62/negative-controls.json']:
 assert pathlib.Path(p).read_bytes()==subprocess.check_output(['git','show','7131fef:'+p]);print('FREEZE',p,'preserved=true')
for p,sha in json.loads(pathlib.Path('.ufo/waves/round-62/freeze.json').read_text())['inputs'].items():
 assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==sha;print('INPUT',p,'preserved=true')
for p in ['first-answers.json','first-negative-answers.json','challenge.md']:
 rel='.ufo/waves/round-62/'+p;assert pathlib.Path(rel).read_bytes()==subprocess.check_output(['git','show','201473ba:'+rel]);print('FIRST',p,'preserved=true')
expected={x.strip() for x in pathlib.Path('corpus/instruments/knowledge-expected.txt').read_text().splitlines() if x.strip() and not x.startswith('#')};actual={str(x) for x in pathlib.Path('corpus/knowledge').glob('*.md')};assert expected==actual,(expected-actual,actual-expected);print('KNOWLEDGE-INVENTORY missing=0 unexpected=0')
for q in ['including non-anticipated states of the product.','OpenVEX Specification v0.2.0']:
 n=subprocess.check_output(['wc','-w'],input=q.encode()).decode().strip();print('GATE-QUOTE',repr(q),'words='+n);assert int(n)<=25
pathlib.Path('base-skill.md').write_bytes(subprocess.check_output(['git','show',base+':SKILL.md']))
PY
run 0 python3 corpus/instruments/density.py base-skill.md --label before
run 0 python3 corpus/instruments/density.py SKILL.md --label after
unset GIT_DIR GIT_WORK_TREE
cd "$lane" || exit 2
run 0 python3 .ufo/waves/round-62/operability-replay.py
run 0 python3 .ufo/waves/round-62/retained-failures.py
run 0 python3 corpus/instruments/score-gap.py
run 0 python3 corpus/instruments/census-freshness-check.py .
printf 'FINAL unexpected-results=%s\n' "$bad"
[ "$bad" -eq 0 ]
