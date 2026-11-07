#!/usr/bin/env bash
# Round-85 C1 pre-freeze controls: do-nothing, pad, delete-GONE, wrong-target,
# partial, positive. Run from the lane root; SCRATCH via $1.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$L/.ufo/waves/round-85
S=${1:?scratch}; mkdir -p "$S"
BASE_REV=bc722e540c93b48ff159454b65a0f9f4630db1ed
git -C "$L" show $BASE_REV:SKILL.md > "$S/base.md"
MAP=$W/c1/repair-map.json
MSHA=$(sha256sum "$MAP" | cut -d' ' -f1)
M="python3 -B $W/c1/skill-meter.py --lane $L --work $S/w"
echo "base_rev=$BASE_REV map_sha256=$MSHA skill_base_sha256=$(sha256sum "$S/base.md" | cut -d' ' -f1)"
$M --measure "$S/base.md"
python3 -B $W/c1/apply-map.py "$MAP" "$S/base.md" "$S/positive.md"
T=$($M --measure "$S/positive.md" | sed -E 's/.*rate=([0-9]+\/[0-9]+).*/\1/')
echo "positive-derived target=$T"
run() { echo "== control $1 (expected: $2)"; $M --base "$S/base.md" --after "$3" --map "$MAP" --target "$T" --map-sha256 "$MSHA"; echo "rc=$?"; }
run donothing fail "$S/base.md"
cp "$S/base.md" "$S/pad.md"; printf '\nPad: `corpus/knowledge/cisa-kev-catalog.md` `corpus/knowledge/claim-gates.md` `corpus/knowledge/claim-package-contract.md` `corpus/knowledge/cvss-v4-severity-and-vector.md` `corpus/knowledge/vdp-disclosure-packages.md` `corpus/instruments/density.py` `corpus/instruments/anchorcheck.py` `corpus/instruments/recheck-audit.py` `corpus/instruments/figure-audit.py` `corpus/instruments/wave-registry.py` `corpus/instruments/freeze-check.py` `corpus/instruments/gate-quote-audit.py` `corpus/instruments/census-freshness-check.py` `corpus/instruments/derive-head-census.py` `corpus/instruments/citation-ground-check.py` `corpus/instruments/mirror-containment-check.py` `corpus/instruments/recheck-cwd-census.py` `corpus/instruments/source-recheck.py`\n' >> "$S/pad.md"
run pad-resolving-cites fail "$S/pad.md"
python3 - "$S/base.md" "$S/delgone.md" "$L" <<'P'
import sys,os
sys.path.insert(0,os.path.join(sys.argv[3],'corpus','instruments'))
import resolve as R
t=open(sys.argv[1],encoding='utf-8').read(); n=0
mirror=os.path.expanduser(R.MIRROR_ROOT)
for line in t.split('\n'):
    for m in R.TOKEN.finditer(line):
        tok=m.group(1).strip().rstrip('.,;:')
        if n<18 and tok.startswith('~/Projects/bounties/') and R.is_pathlike(tok) and R.classify(tok,sys.argv[3],mirror)[0]=='GONE' and t.count('`%s`'%m.group(1))==1:
            t=t.replace('`%s`'%m.group(1), m.group(1).replace('/', ' / ')); n+=1
open(sys.argv[2],'w',encoding='utf-8').write(t); print('delete-gone de-cited', n)
P
run delete-gone-cites fail "$S/delgone.md"
python3 -B $W/c1/apply-map.py "$MAP" "$S/base.md" "$S/wrong.md" --swap resolve.py=corpus/instruments/density.py
run wrong-target fail "$S/wrong.md"
python3 -B $W/c1/apply-map.py "$MAP" "$S/base.md" "$S/partial.md" --only 9
run partial-9-of-18 fail "$S/partial.md"
run positive pass "$S/positive.md"
