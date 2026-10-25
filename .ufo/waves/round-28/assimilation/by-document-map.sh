#!/usr/bin/env bash
# by-document-map.sh — round-28 wave-1: map the adopted staged rows onto lane ids BY DOCUMENT.
#
# Adopted this round (per frozen C2): staged S042 (IPA intake-process page) -> lane S042 (free);
# staged S043 (JPCERT/CC 2026 P-guideline) -> lane S041 (SAME document, already registered round 26).
# Reads only; writes only under .ufo/waves/round-28/assimilation/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
A=$LANE/.ufo/waves/round-28/assimilation

IPA_URL='https://www.ipa.go.jp/security/todokede/vuln/process.html'
PG_URL='https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf'

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

cd "$LANE" || exit 1

echo "== round-28 wave-1 by-document mapping =="
echo

echo "-- 1. staged S042 row (IPA intake-process page) --"
run "grep -nE '^ {0,3}\\| *S042 *\\|' $PKG/SOURCES.append.md | cut -c1-260"
echo

echo "-- 2. staged S043 row (JPCERT/CC 2026 P-guideline) --"
run "grep -nE '^ {0,3}\\| *S043 *\\|' $PKG/SOURCES.append.md | cut -c1-260"
echo

echo "-- 3. lane registry: is S042 free? --"
run "grep -cE '^ {0,3}\\| *S042 *\\|' corpus/SOURCES.md"
echo

echo "-- 4. lane registry: does ANY lane row carry the IPA intake-process URL? (must be 0) --"
run "grep -cF '$IPA_URL' corpus/SOURCES.md"
echo

echo "-- 5. lane registry: does ANY lane row carry the P-guideline URL? (must be >=1) --"
run "grep -cF '$PG_URL' corpus/SOURCES.md"
run "grep -nF '$PG_URL' corpus/SOURCES.md | cut -c1-120"
echo

echo "-- 6. lane S041 row in full (the row staged S043 maps onto) --"
run "grep -nE '^ {0,3}\\| *S041 *\\|' corpus/SOURCES.md"
echo

echo "-- 7. URL equality by document (not by number): staged S043 URL vs lane S041 URL --"
run "printf 'staged S043 url: '; grep -E '^ {0,3}\\| *S043 *\\|' $PKG/SOURCES.append.md | grep -oE 'https?://[^ |]+' | head -1"
run "printf 'lane   S041 url: '; grep -E '^ {0,3}\\| *S041 *\\|' corpus/SOURCES.md | grep -oE 'https?://[^ |]+' | head -1"
run "printf 'staged S042 url: '; grep -E '^ {0,3}\\| *S042 *\\|' $PKG/SOURCES.append.md | grep -oE 'https?://[^ |]+' | head -1"
echo

echo "-- 8. duplicate-document scan across the WHOLE lane registry (any URL appearing twice) --"
run "grep -oE 'https?://[^ |]+' corpus/SOURCES.md | sort | uniq -d"
echo "(empty above = no URL is registered twice in the lane registry)"
