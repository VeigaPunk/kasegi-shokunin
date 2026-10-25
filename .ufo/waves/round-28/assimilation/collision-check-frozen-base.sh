#!/usr/bin/env bash
# collision-check-frozen-base.sh — round-28 wave-1: the id-collision check against the FROZEN
# lane base (rev c9f8b115a098c65356e4b3b6048af45a37ab8395, the claims-freeze commit), so the
# collision count is pinned to the state the claims were frozen against, independently of any
# concurrent in-wave registry append.
#
# Reads the base revision with `git show` (read-only) into scratch; never touches the worktree.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
A=$LANE/.ufo/waves/round-28/assimilation
BASE=c9f8b115a098c65356e4b3b6048af45a37ab8395
PAT='^ {0,3}\|[[:space:]]*S[0-9]{3,}'

run() { printf '$ %s\n' "$*"; bash -c "$*"; rc=$?; printf '[exit %s]\n\n' "$rc"; }

cd "$LANE" || exit 1
mkdir -p "$A/base"

echo "== round-28 wave-1 collision check against the FROZEN lane base =="
echo "base revision: $BASE"
run "git rev-parse --verify $BASE^{commit}"
run "git show $BASE:corpus/SOURCES.md > $A/base/SOURCES.md"
run "wc -l < $A/base/SOURCES.md | sed 's/^/base SOURCES.md lines: /'"
echo
run "grep -oE '$PAT' $A/base/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/base/reg-ids"
run "grep -oE '$PAT' $PKG/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > $A/base/staged-ids"
run "comm -12 $A/base/reg-ids $A/base/staged-ids > $A/base/collisions"
run "printf 'base reg-ids    lines='; wc -l < $A/base/reg-ids"
run "printf 'base staged-ids lines='; wc -l < $A/base/staged-ids"
run "printf 'base collisions  lines='; wc -l < $A/base/collisions"
run "cat $A/base/collisions"
echo
echo "-- do the 11 colliding ids carry the SAME DOCUMENT in lane and staged? (all must differ) --"
run "python3 - <<'PY'
import re
base=open('.ufo/waves/round-28/assimilation/base/SOURCES.md',encoding='utf-8').read().split('\n')
pkg=open('/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md',encoding='utf-8').read().split('\n')
def rows(lines):
    d={}
    for l in lines:
        m=re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|(.*)$',l)
        if m:
            u=re.search(r'https?://[^ |]+', m.group(2))
            d[m.group(1)]=(u.group(0) if u else '', m.group(2)[:70])
    return d
b=rows(base); p=rows(pkg)
same=0; diff=0
for i in sorted(set(b)&set(p)):
    if b[i][0]==p[i][0]:
        same+=1; print(f'{i}  SAME URL  {b[i][0]}')
    else:
        diff+=1; print(f'{i}  DIFFER    lane={b[i][0][:58]}')
        print(f'{\"\":6}staged={p[i][0][:58]}')
print(f'--- collisions={len(set(b)&set(p))} same-document={same} different-document={diff}')
PY"
