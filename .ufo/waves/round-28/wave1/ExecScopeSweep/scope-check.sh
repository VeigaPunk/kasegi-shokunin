#!/usr/bin/env bash
# Round-28 write-scope checker (seat ExecScopeSweep, round 28 wave 1).
#
# Limbs:
#   1  fleet root: untracked files whose content names kasegi/round-28 (MISROOT)
#   2  lane repo: every working-status path classified against the round-28
#      ownership map (production file -> exactly one writer seat)
#   2b lane repo: gitignored paths touched since wave start (informational)
#   3  shokuknow: no kasegi-scoped write since wave start (read-only substrate)
#
# Read-only: runs only git read commands and find/grep. Writes nothing.
# Exit 0 = no scope violation detected at run time; 1 = violation(s).
#
# Usage (from anywhere):
#   bash .../wave1/ExecScopeSweep/scope-check.sh            # full sweep
#   bash .../wave1/ExecScopeSweep/scope-check.sh --selftest # limb-2 classifier proof
set -u

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
KNOW=/home/vgpnk/Projects/shokuknow
BASE=c9f8b115a098c65356e4b3b6048af45a37ab8395
# Wave start = the C1/C2 freeze commit instant (authority for "before the wave").
WAVE_START=$(date -u -d "$(git -C "$LANE" log -1 --format=%cI "$BASE")" +%Y-%m-%dT%H:%M:%SZ)

# Ownership map — production files have exactly ONE writer (wave brief).
OWNERS=$(
  printf '%s\t%s\n' \
    corpus/instruments/anchorcheck.py                         ExecImplC1 \
    corpus/instruments/README.md                              ExecInstrReadme \
    SKILL.md                                                  ScribeSkillGate \
    corpus/source-snapshots/round-28/S042.txt                 ExecCaptureS042 \
    corpus/source-snapshots/round-28/S041.txt                 ExecCaptureS041 \
    corpus/source-snapshots/round-28/manifest.json            ExecManifest \
    corpus/knowledge/japanese-domestic-disclosure-workflow.md ScribeEntryC2 \
    corpus/SOURCES.md                                         ScribeRegistryC2 \
    corpus/README.md                                          ScribeReadmeC2 \
    corpus/QUALITY.md                                         ScribeR14 \
    corpus/lessons/round-28.md                                ScribeLesson \
    LOG.md                                                    ScribeLog \
    SCORECARD.md                                              ScribeScorecard
)

# classify_path <path> -> "<CLASS>\t<owner-or-dash>\t<path>"; returns 1 on VIOLATION
classify_path() {
  local path=$1 owner
  owner=$(printf '%s\n' "$OWNERS" | awk -F'\t' -v p="$path" '$1==p{print $2; exit}')
  if [ -n "$owner" ]; then
    printf 'PROD\t%s\t%s\n' "$owner" "$path"; return 0
  fi
  case "$path" in
    .ufo/waves/round-28|.ufo/waves/round-28/*) printf 'WAVE\t-\t%s\n' "$path"; return 0 ;;
  esac
  printf 'VIOLATION\t-\t%s\n' "$path"; return 1
}

if [ "${1:-}" = "--selftest" ]; then
  cases=0; failures=0
  check() { # check <status-line> <expected>
    local line=$1 want=$2 path got
    path=${line:3}
    case "$path" in *' -> '*) path=${path##* -> } ;; esac
    got=$(classify_path "$path")
    cases=$((cases+1))
    if [ "$(printf '%s' "$got" | cut -f1,2 | tr '\t' ' ')" != "$want" ]; then
      printf 'FAIL case=%s want="%s" got="%s"\n' "$line" "$want" "$(printf '%s' "$got" | tr '\t' ' ')"
      failures=$((failures+1))
    fi
  }
  check ' M corpus/QUALITY.md'                                    'PROD ScribeR14'
  check ' M LOG.md'                                               'PROD ScribeLog'
  check ' M SCORECARD.md'                                         'PROD ScribeScorecard'
  check '?? corpus/source-snapshots/round-28/S041.txt'            'PROD ExecCaptureS041'
  check '?? corpus/source-snapshots/round-28/manifest.json'       'PROD ExecManifest'
  check 'R  old/SOURCES.md -> corpus/SOURCES.md'                  'PROD ScribeRegistryC2'
  check '?? .ufo/waves/round-28/receipts/SomeSeat.txt'            'WAVE -'
  check '?? .ufo/waves/round-28/wave1/SeatX/scratch.txt'          'WAVE -'
  check '?? corpus/knowledge/rogue-r28.md'                        'VIOLATION -'
  check ' M corpus/lessons/round-27.md'                           'VIOLATION -'
  check ' M templates/foo.md'                                     'VIOLATION -'
  check '?? .ufo/state/kasegi.r28.json'                           'VIOLATION -'
  check ' M corpus/instruments/resolve.py'                        'VIOLATION -'
  printf 'selftest cases=%s failures=%s\n' "$cases" "$failures"
  [ "$failures" -eq 0 ]
  exit $?
fi

rc=0
echo "== ExecScopeSweep scope-check =="
echo "run_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "lane=$LANE"
echo "lane_head=$(git -C "$LANE" rev-parse HEAD)"
if git -C "$LANE" merge-base --is-ancestor "$BASE" HEAD 2>/dev/null; then
  echo "base_ancestor=$BASE yes"
else
  echo "base_ancestor=$BASE NO"; rc=1
fi

echo
echo "-- limb 2: lane working status vs ownership map --"
nprod=0; nwave=0; nviol=0
while IFS= read -r line; do
  [ -n "$line" ] || continue
  st=${line:0:2}
  path=${line:3}
  case "$path" in *' -> '*) path=${path##* -> } ;; esac   # rename: judge the new path
  out=$(classify_path "$path") || {
    printf 'VIOLATION %s  %s\n' "$st" "$path"; nviol=$((nviol+1)); continue
  }
  cls=$(printf '%s' "$out" | cut -f1)
  own=$(printf '%s' "$out" | cut -f2)
  if [ "$cls" = PROD ]; then
    printf 'PROD   %s  %-16s %s\n' "$st" "$own" "$path"; nprod=$((nprod+1))
  else
    printf 'WAVE   %s  %s\n' "$st" "$path"; nwave=$((nwave+1))
  fi
done < <(git -C "$LANE" status --porcelain -uall)
echo "lane_prod_paths=$nprod lane_wave_paths=$nwave lane_violations=$nviol"
[ "$nviol" -eq 0 ] || rc=1

echo
echo "-- limb 2b (informational): gitignored paths touched since wave start --"
ign=$(find "$LANE" -path "$LANE/.git" -prune -o -path "$LANE/.jj" -prune -o \
      -path '*/__pycache__' -prune -o -type f -newermt "$WAVE_START" -print 2>/dev/null |
      while IFS= read -r f; do
        rel=${f#"$LANE"/}
        git -C "$LANE" check-ignore -q "$rel" && printf '%s\n' "$rel"
      done)
if [ -n "$ign" ]; then printf '%s\n' "$ign"; else echo "(none)"; fi

echo
echo "-- limb 1: fleet root untracked files naming kasegi/round-28 --"
fleet_untracked=0; misroot=0
while IFS= read -r line; do
  [ -n "$line" ] || continue
  st=${line:0:2}
  [ "$st" = "??" ] || continue
  path=${line:3}
  case "$path" in *-shokunin/*) continue ;; esac   # sibling/lane repos are their own scopes
  fleet_untracked=$((fleet_untracked+1))
  if grep -qIE 'kasegi|round-28' "$FLEET/$path" 2>/dev/null; then
    printf 'MISROOT %s\n' "$path"; misroot=$((misroot+1))
  fi
done < <(git -C "$FLEET" status --porcelain -uall)
echo "fleet_untracked_scanned=$fleet_untracked fleet_misroot=$misroot"
[ "$misroot" -eq 0 ] || rc=1

echo
echo "-- limb 1b (informational): fleet root modified tracked paths --"
git -C "$FLEET" status --porcelain -uall | awk '$1!="??"{print "MODIFIED "$0}'

echo
echo "-- limb 1c: fleet root gitignored surface newer than wave start --"
ign_dirs=$(git -C "$FLEET" status --porcelain -uall --ignored=matching |
  awk '$1=="!!"{print $2}' |
  grep -vE '^(\.jj/|\.git/|\.ufo/state/|\.scratch/|.*-shokunin/|r80-baseline-frozen-worktree/|templates/|scripts/)' |
  sort -u)
ign_files=0; ign_misroot=0
while IFS= read -r p; do
  [ -n "$p" ] || continue
  [ -e "$FLEET/$p" ] || continue
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    ign_files=$((ign_files+1))
    rel=${f#"$FLEET"/}
    if grep -qIE 'kasegi|round-28' "$f" 2>/dev/null; then
      printf 'MISROOT(ignored) %s\n' "$rel"; ign_misroot=$((ign_misroot+1))
    fi
  done < <(find "$FLEET/$p" -type f -newermt "$WAVE_START" -print 2>/dev/null)
done <<< "$ign_dirs"
echo "fleet_ignored_roots=$(printf '%s' "$ign_dirs" | grep -c . ) fleet_ignored_files_scanned=$ign_files fleet_ignored_misroot=$ign_misroot"
[ "$ign_misroot" -eq 0 ] || rc=1

echo
echo "-- limb 3: shokuknow read-only tree --"
know_status=$(git -C "$KNOW" status --porcelain -uall | wc -l)
know_pkg=$(git -C "$KNOW" status --porcelain -uall -- merge/kasegi | wc -l)
know_new=$(find "$KNOW/merge/kasegi" -type f -newermt "$WAVE_START" 2>/dev/null | wc -l)
know_new_named=$(find "$KNOW" -path "$KNOW/.git" -prune -o -type f -newermt "$WAVE_START" \
                   -print0 2>/dev/null | xargs -0 -r grep -lI 'kasegi' 2>/dev/null | wc -l)
know_max=$(find "$KNOW/merge/kasegi" -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS\n' 2>/dev/null | sort -r | head -1)
know_recent_total=$(find "$KNOW" -path "$KNOW/.git" -prune -o -type f -newermt "$WAVE_START" -print 2>/dev/null | wc -l)
know_status_touched=$(git -C "$KNOW" status --porcelain -uall |
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    p=${line:3}
    case "$p" in *' -> '*) p=${p##* -> } ;; esac
    [ -f "$KNOW/$p" ] && [ -n "$(find "$KNOW/$p" -newermt "$WAVE_START" -print 2>/dev/null)" ] && printf 'x\n'
  done | wc -l)
# Only kasegi-owned subtrees are in this wave's scope; other lanes stage their
# own work in the same repo (concurrent waves), which is not our violation.
know_scoped_new=$(find "$KNOW/merge/kasegi" "$KNOW/lanes/kasegi" -type f -newermt "$WAVE_START" 2>/dev/null | wc -l)
echo "shokuknow_head=$(git -C "$KNOW" rev-parse HEAD)"
echo "shokuknow_status_paths=$know_status   (repo-wide: pre-existing staging dirt, all lanes)"
echo "shokuknow_merge_kasegi_status_paths=$know_pkg"
echo "shokuknow_merge_kasegi_files_newer_than_wave=$know_new (max_mtime=$know_max)"
echo "shokuknow_files_newer_than_wave_naming_kasegi=$know_new_named"
echo "shokuknow_files_newer_than_wave_total=$know_recent_total"
find "$KNOW" -path "$KNOW/.git" -prune -o -type f -newermt "$WAVE_START" -print 2>/dev/null |
  while IFS= read -r f; do printf 'recent %s\n' "${f#"$KNOW"/}"; done
echo "shokuknow_status_paths_touched_since_wave_start=$know_status_touched"
echo "shokuknow_kasegi_scoped_files_newer_than_wave=$know_scoped_new"
[ "$know_scoped_new" -eq 0 ] || rc=1
[ "$know_new" -eq 0 ] || rc=1

echo
echo "scope_check_exit=$rc"
exit "$rc"
