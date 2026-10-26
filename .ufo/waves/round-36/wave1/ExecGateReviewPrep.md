# ExecGateReviewPrep — round-36 post-integration gate runner (draft)

**Item.** Prepare the post-integration gate run script (draft, in scratch): a bash script that
after integration will (1) run `bash {LANE}/corpus/instruments/r36-closure.sh --export-ref <hash>`
on the final lane hash, (2) run the three C2 counters, (3) census validate, (4)
`git -C {LANE} status --porcelain`; print a template receipt with placeholders. Also verify the
script itself is `bash -n` clean and does not write to the lane.

**Result.** Script written to scratch, then embedded verbatim in §3 (407 lines, sha256
`fad8bcd2b1c262285f5967b12c82a91e04d9811477fad0bb393fbba2dcf7bb89`). `bash -n` exit 0 (run twice),
`shellcheck -s bash` exit 0. Zero-write property measured two ways: a controlled fixture run
(tree fingerprint identical over 7,160 files) and a real-lane run whose only diffs are sibling
seats' own receipts (§4.5). Both directions of every check were exercised — the gate fails on the
frozen-before tree and passes the C2 checks once the after-values are present (§4.7).

No lane file was created, edited or deleted by this seat; the only write is this receipt.

---

## 1. Deliverable

| property | value |
|---|---|
| script | `r36-post-integration-gate.sh` (draft; not landed in the lane — see §7 R6) |
| scratch path (removed at yield) | `/fast/scratch/hyaku/kasegi-r36/ExecGateReviewPrep/r36-post-integration-gate.sh` |
| lines | 407 |
| sha256 | `fad8bcd2b1c262285f5967b12c82a91e04d9811477fad0bb393fbba2dcf7bb89` |
| md5 | `45daf2ebde8d872640abe6fd9da479c9` |
| `bash -n` | exit 0 (two independent runs) |
| `shellcheck -s bash` | exit 0, no findings (after the `A && B \|\| C` and `ls`/`grep\|wc` forms were replaced with `if/else`, `find -maxdepth 1`, `grep -vcE`) |
| writes | none to the lane; one optional `--out PATH`, refused (exit 2) when it resolves inside the lane |
| exit codes | `0` all checks PASS · `1` any check FAIL · `2` usage/environment error |

Invocations:

```
bash r36-post-integration-gate.sh [--lane DIR] [--ref REV] [--fleet-root DIR]
                                  [--census-script PATH] [--scratch-root DIR]
                                  [--out PATH] [--plan] [-h|--help]
```

`--ref` defaults to `git -C {LANE} rev-parse HEAD` and is normalised to a full commit id
(`--ref 2d9504` → current head full hash, measured). `--plan` prints the twelve commands that
would run and executes nothing.

---

## 2. What the gate measures

Fourteen checks, run in order, **never short-circuiting** — a missing C1 suite does not stop the
C2 counters from running or the receipt from printing, so one failure cannot hide the state of
the rest.

| # | check | command it runs | pass condition |
|---|---|---|---|
| 0.1 | `preflight.suite-present` | `[ -f {LANE}/corpus/instruments/r36-closure.sh ]` | present |
| 0.2 | `preflight.census-present` | `[ -f {FLEET}/scripts/sources-census.sh ]` | present |
| 1.1 | `c1.export-ref` | `bash {LANE}/corpus/instruments/r36-closure.sh --export-ref <ref>` | `closed=9/9` **and** exit 0 |
| 1.2 | `c1.selftest` | `bash {LANE}/corpus/instruments/r36-closure.sh --selftest` | `cases=9 failures=0` **and** exit 0 |
| 2.1 | `c2.frontier-rows` | `grep -cE '^\| F[0-9]+ \|' {LANE}/corpus/README.md` | 19 |
| 2.2 | `c2.registry-rows` | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' {LANE}/corpus/SOURCES.md` | 53 |
| 2.3 | `c2.entries-citing-S053` | `grep -rlE '^source: S053 ' {LANE}/corpus/knowledge \| wc -l` | 1 |
| 2s.1 | `c2s.knowledge-entries` | `find {LANE}/corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l` | 48 |
| 2s.2 | `c2s.harness` | `python3 {LANE}/corpus/instruments/frontier-recheck-count.py` (cwd = lane) | final line `entries=22 pass=22 exit=0` |
| 2s.3 | `c2s.recheck-S053` | `python3 {LANE}/corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` (cwd = lane) | exit 0 |
| 2s.4 | `c2s.capture-binding` | `python3 {LANE}/corpus/instruments/capture-binding-check.py` (cwd = lane) | exit 0 |
| 3.1 | `census.validate` | `bash {FLEET}/scripts/sources-census.sh validate --root {FLEET} kasegi` | exit 0 **and** every non-`ok` line is `W04 S028`/`W04 S029` |
| 4.1 | `quiescence.worktree` | `git -C {LANE} status --porcelain` | no lines |
| 4.2 | `quiescence.scratch-seats` | `find {SCRATCH}/kasegi-r36 -mindepth 1 -maxdepth 1 -type d` | no dirs |

Rows 1.1 and 2.1–2.3 are the item's letter; 1.2 and 2s.1–2s.4 are the rest of the frozen
predicates (`claims.json` C1 kill rule and C2 express/predicate) — a gate that ran only the
letter would pass a suite with broken fixtures and a harness at 21/21. 4.2 is E9's second limb,
added beside the item's `git status` limb because E9 names both.

**Counter definitions are the frozen ones, not re-derived.** The three C2 counters are copied
verbatim from `claims.json` C2 `counting_commands`; the after-values are frozen constants at the
top of the script (`EXP_*`), so a drifting expectation cannot silently follow a drifting tree.

---

## 3. Script (verbatim)

```bash
#!/usr/bin/env bash
# r36-post-integration-gate.sh — DRAFT post-integration gate runner for
# kasegi-shokunin round 36 (C1 depth:verifiability + C2 coverage).
#
# WHAT IT DOES (in order, never short-circuits: every phase runs and is
# recorded, so one failing phase cannot hide the state of the rest):
#   0.  preflight: lane is a git worktree; --ref resolves to a commit; the
#       counter subjects exist; the census script exists (fail closed).
#   1.  C1: `bash {LANE}/corpus/instruments/r36-closure.sh --export-ref <ref>`
#       must print `closed=9/9` and exit 0, and `--selftest` must print
#       `cases=9 failures=0` and exit 0.
#   2.  C2 counters (the three shell counters frozen in claims.json C2):
#       2.1 frontier rows            corpus/README.md      expect 19
#       2.2 registry rows            corpus/SOURCES.md     expect 53
#       2.3 entries citing S053      corpus/knowledge/*.md expect 1
#       §2s C2 supporting instruments (the rest of C2's predicate/kill rule):
#       knowledge entry count 48, harness entries=22 pass=22 exit=0,
#       source-recheck --source S053 exit 0, capture-binding-check exit 0.
#   3.  census validate: `sources-census.sh validate --root {FLEET} kasegi`
#       exit 0 with W04 S028/S029 as the only non-`ok` lines.
#   4.  quiescence (E9): `git -C {LANE} status --porcelain` empty, and no
#       leftover seat dirs under {SCRATCH}/kasegi-r36.
#   5.  prints a template receipt with `<...>` placeholders for the facts the
#       gate cannot measure (UTC stamp, L1 signoff, score).
#
# WRITE DISCIPLINE. The gate is a READER. Every phase pipes command output into
# shell variables; the script creates no file, no directory, no temp file, and
# passes no `--out`/`--scratch` to any instrument. The only `git` verbs it runs
# are `rev-parse` and `status --porcelain` (the latter may refresh git's own
# index stat-cache; it never changes worktree bytes). The single optional write
# is `--out PATH`, and it is refused (exit 2) when PATH resolves inside the lane
# — the assertion is realpath-based, not string-prefix-based.
#
# PLACEHOLDER DISCIPLINE. The receipt template this script prints is for the
# wave receipt, never for SCORECARD.md: C1 check E1 fails the suite on the
# literal `filled by the L1` placeholder line and on a bare `<LANE_HASH>`
# token, so no token emitted here may be pasted into SCORECARD.md. This script
# emits `<REF>`/`<UTC>`/`<L1_NAME>`-shaped tokens and deliberately never emits
# a `<...LANE_HASH>` token.
#
# Usage:
#   bash r36-post-integration-gate.sh [options]
#     --lane DIR            lane repo (default $KASEGI_LANE or
#                           /home/vgpnk/Projects/shokunin/kasegi-shokunin)
#     --ref REV             lane head to export (default: `git -C LANE rev-parse
#                           HEAD`); normalised to a full commit id
#     --fleet-root DIR      fleet root for the census (default
#                           $KASEGI_FLEET_ROOT or /home/vgpnk/Projects/shokunin)
#     --census-script PATH  census instrument (default
#                           {fleet-root}/scripts/sources-census.sh)
#     --scratch-root DIR    scratch root for the E9 leftover scan (default
#                           $KASEGI_SCRATCH_ROOT or /fast/scratch/hyaku)
#     --out PATH            also write the receipt template here; refused inside
#                           the lane
#     --plan                print the commands that would run, execute nothing
#     -h | --help           this text
#
# Exit: 0 all checks PASS · 1 any check FAIL · 2 usage/environment error.
#
# Unix tools only: bash, git, grep, sed, wc, find, realpath, python3 (called by
# the lane's own instruments).

set -uo pipefail

LANE=${KASEGI_LANE:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
FLEET_ROOT=${KASEGI_FLEET_ROOT:-/home/vgpnk/Projects/shokunin}
SCRATCH_ROOT=${KASEGI_SCRATCH_ROOT:-/fast/scratch/hyaku}
CENSUS_SCRIPT=""
REF_IN=""
OUT=""
PLAN=0

# Frozen expected values (claims.json round 36).
EXP_CLOSED="9/9"
EXP_CASES=9
EXP_FRONTIER=19
EXP_REGISTRY=53
EXP_CITING=1
EXP_KNOWLEDGE=48
EXP_HARNESS="entries=22 pass=22 exit=0"

usage() { sed -n '2,58p' "$0" | sed -e 's/^# \{0,1\}//'; }

die_usage() { printf '%s: %s\n' "${0##*/}" "$1" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --lane)          [ $# -ge 2 ] || die_usage "--lane needs a value"; LANE=$2; shift 2 ;;
    --ref)           [ $# -ge 2 ] || die_usage "--ref needs a value"; REF_IN=$2; shift 2 ;;
    --fleet-root)    [ $# -ge 2 ] || die_usage "--fleet-root needs a value"; FLEET_ROOT=$2; shift 2 ;;
    --census-script) [ $# -ge 2 ] || die_usage "--census-script needs a value"; CENSUS_SCRIPT=$2; shift 2 ;;
    --scratch-root)  [ $# -ge 2 ] || die_usage "--scratch-root needs a value"; SCRATCH_ROOT=$2; shift 2 ;;
    --out)           [ $# -ge 2 ] || die_usage "--out needs a value"; OUT=$2; shift 2 ;;
    --plan)          PLAN=1; shift ;;
    -h|--help)       usage; exit 0 ;;
    *)               die_usage "unknown argument: $1" ;;
  esac
done

[ -n "$CENSUS_SCRIPT" ] || CENSUS_SCRIPT="$FLEET_ROOT/scripts/sources-census.sh"

# ---------------------------------------------------------------- accounting
CHECKS=0
FAILED=0
declare -a ROWS=()

record() { # record NAME VALUE EXPECT VERDICT
  local name=$1 value=$2 expect=$3 verdict=$4
  CHECKS=$((CHECKS + 1))
  [ "$verdict" = PASS ] || FAILED=$((FAILED + 1))
  ROWS+=("$(printf '%s|%s|%s|%s' "$name" "$value" "$expect" "$verdict")")
  printf 'gate check=%-26s value=%-24s expect=%-24s verdict=%s\n' \
    "$name" "$value" "$expect" "$verdict"
}

note() { printf 'gate note=%s\n' "$*"; }

# count matching lines in a file; a missing file or zero matches reads as 0
count_lines() { # count_lines FILE ERE
  local f=$1 pat=$2 n=""
  if [ -f "$f" ]; then
    n=$(grep -cE -- "$pat" "$f" 2>/dev/null) || true
  fi
  printf '%s' "${n:-0}"
}

# number of non-blank lines in a string (used to count leftover findings)
count_text_lines() { # count_text_lines TEXT
  local t=$1 n=""
  if [ -n "$t" ]; then
    n=$(printf '%s\n' "$t" | grep -c '[^[:space:]]') || true
  fi
  printf '%s' "${n:-0}"
}

# ---------------------------------------------------------------- preflight
[ -d "$LANE" ] || die_usage "lane directory not found: $LANE"
top=$(git -C "$LANE" rev-parse --show-toplevel 2>/dev/null) || top=""
[ -n "$top" ] || die_usage "not a git worktree: $LANE"
LANE_REAL=$(realpath -e -- "$LANE") || die_usage "cannot realpath lane: $LANE"
top_real=$(realpath -e -- "$top") || die_usage "cannot realpath worktree top: $top"
[ "$top_real" = "$LANE_REAL" ] || die_usage "lane is not the worktree top ($LANE_REAL vs $top_real)"

if [ -n "$REF_IN" ]; then
  REF=$(git -C "$LANE" rev-parse --verify --quiet "$REF_IN^{commit}") \
    || die_usage "ref does not resolve to a commit: $REF_IN"
else
  REF=$(git -C "$LANE" rev-parse --verify --quiet 'HEAD^{commit}') \
    || die_usage "cannot resolve HEAD in $LANE"
fi

if [ -n "$OUT" ]; then
  OUT_REAL=$(realpath -m -- "$OUT") || die_usage "cannot realpath --out: $OUT"
  case "$OUT_REAL" in
    "$LANE_REAL"|"$LANE_REAL"/*) die_usage "--out resolves inside the lane (refused): $OUT_REAL" ;;
  esac
else
  OUT_REAL=""
fi

SUITE="$LANE/corpus/instruments/r36-closure.sh"
RECOUNT="$LANE/corpus/instruments/frontier-recheck-count.py"
RECHECK="$LANE/corpus/instruments/source-recheck.py"
BINDING="$LANE/corpus/instruments/capture-binding-check.py"
MANIFEST_REL="corpus/source-snapshots/round-36/manifest.json"

note "lane=$LANE_REAL"
note "ref=$REF"
note "census=$CENSUS_SCRIPT"
[ "$PLAN" -eq 1 ] && note "plan=1 (nothing executed)"

if [ "$PLAN" -eq 1 ]; then
  printf '%s\n' \
    "plan cmd: bash $SUITE --export-ref $REF" \
    "plan cmd: bash $SUITE --selftest" \
    "plan cmd: grep -cE '^\\| F[0-9]+ \\|' $LANE/corpus/README.md" \
    "plan cmd: grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' $LANE/corpus/SOURCES.md" \
    "plan cmd: grep -rlE '^source: S053 ' $LANE/corpus/knowledge | wc -l" \
    "plan cmd: ls $LANE/corpus/knowledge/*.md | wc -l" \
    "plan cmd: python3 $RECOUNT" \
    "plan cmd: python3 $RECHECK --manifest $LANE/$MANIFEST_REL --source S053" \
    "plan cmd: python3 $BINDING" \
    "plan cmd: bash $CENSUS_SCRIPT validate --root $FLEET_ROOT kasegi" \
    "plan cmd: git -C $LANE status --porcelain" \
    "plan cmd: find $SCRATCH_ROOT/kasegi-r36 -mindepth 1 -maxdepth 1 -type d"
  exit 0
fi

# ---------------------------------------------------------------- 0. preflight
if [ -f "$SUITE" ]; then
  record preflight.suite-present present present PASS
else
  record preflight.suite-present missing present FAIL
fi
for f in corpus/README.md corpus/SOURCES.md corpus/knowledge; do
  if [ -e "$LANE/$f" ]; then :; else record "preflight.subject-$f" missing present FAIL; fi
done
if [ -f "$CENSUS_SCRIPT" ]; then
  record preflight.census-present present present PASS
else
  record preflight.census-present missing present FAIL
fi

# ---------------------------------------------------------------- 1. C1 suite
printf '%s\n' "--- 1. C1: r36-closure.sh over the export of $REF"
suite_out=""
suite_rc=1
if [ -f "$SUITE" ]; then
  suite_out=$(bash "$SUITE" --export-ref "$REF" 2>&1)
  suite_rc=$?
fi
closed=$(printf '%s\n' "$suite_out" \
  | sed -n 's/.*closed=\([0-9][0-9]*\/[0-9][0-9]*\).*/\1/p' | tail -n 1)
closed=${closed:-none}
if [ "$closed" = "$EXP_CLOSED" ] && [ "$suite_rc" -eq 0 ]; then
  record c1.export-ref "closed=$closed exit=$suite_rc" "closed=$EXP_CLOSED exit=0" PASS
else
  record c1.export-ref "closed=$closed exit=$suite_rc" "closed=$EXP_CLOSED exit=0" FAIL
fi
printf '%s\n' "$suite_out" | tail -n 3 | sed 's/^/gate   suite: /'

selftest_out=""
selftest_rc=1
if [ -f "$SUITE" ]; then
  selftest_out=$(bash "$SUITE" --selftest 2>&1)
  selftest_rc=$?
fi
st_line=$(printf '%s\n' "$selftest_out" | grep -E 'selftest cases=[0-9]+ failures=[0-9]+' | tail -n 1)
st_cases=$(printf '%s\n' "$st_line" | sed -n 's/.*cases=\([0-9][0-9]*\).*/\1/p')
st_failures=$(printf '%s\n' "$st_line" | sed -n 's/.*failures=\([0-9][0-9]*\).*/\1/p')
st_cases=${st_cases:-none}
st_failures=${st_failures:-none}
if [ "$st_cases" = "$EXP_CASES" ] && [ "$st_failures" = 0 ] && [ "$selftest_rc" -eq 0 ]; then
  record c1.selftest "cases=$st_cases failures=$st_failures exit=$selftest_rc" \
    "cases=$EXP_CASES failures=0 exit=0" PASS
else
  record c1.selftest "cases=$st_cases failures=$st_failures exit=$selftest_rc" \
    "cases=$EXP_CASES failures=0 exit=0" FAIL
fi

# ---------------------------------------------------------------- 2. C2 counters
printf '%s\n' '--- 2. C2 counters (frozen shell counters)'
frontier=$(count_lines "$LANE/corpus/README.md" '^\| F[0-9]+ \|')
if [ "$frontier" = "$EXP_FRONTIER" ]; then
  record c2.frontier-rows "$frontier" "$EXP_FRONTIER" PASS
else
  record c2.frontier-rows "$frontier" "$EXP_FRONTIER" FAIL
fi

registry=$(count_lines "$LANE/corpus/SOURCES.md" '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|')
if [ "$registry" = "$EXP_REGISTRY" ]; then
  record c2.registry-rows "$registry" "$EXP_REGISTRY" PASS
else
  record c2.registry-rows "$registry" "$EXP_REGISTRY" FAIL
fi

citing=""
if [ -d "$LANE/corpus/knowledge" ]; then
  citing=$(grep -rlE '^source: S053 ' "$LANE/corpus/knowledge" 2>/dev/null | wc -l) || true
fi
citing=${citing:-0}
if [ "$citing" = "$EXP_CITING" ]; then
  record c2.entries-citing-S053 "$citing" "$EXP_CITING" PASS
else
  record c2.entries-citing-S053 "$citing" "$EXP_CITING" FAIL
fi

printf '%s\n' '--- 2s. C2 supporting instruments'
if [ -d "$LANE/corpus/knowledge" ]; then
  knowledge=$(find "$LANE/corpus/knowledge" -maxdepth 1 -type f -name '*.md' | wc -l) || true
fi
knowledge=${knowledge:-0}
if [ "$knowledge" = "$EXP_KNOWLEDGE" ]; then
  record c2s.knowledge-entries "$knowledge" "$EXP_KNOWLEDGE" PASS
else
  record c2s.knowledge-entries "$knowledge" "$EXP_KNOWLEDGE" FAIL
fi

harness_out=""
harness_rc=1
if [ -f "$RECOUNT" ]; then
  harness_out=$(cd "$LANE" && python3 "$RECOUNT" 2>&1)
  harness_rc=$?
fi
harness_line=$(printf '%s\n' "$harness_out" | grep -E '^entries=[0-9]+ pass=[0-9]+ exit=[0-9]+$' | tail -n 1)
harness_line=${harness_line:-none}
if [ "$harness_line" = "$EXP_HARNESS" ]; then
  record c2s.harness "$harness_line" "$EXP_HARNESS" PASS
else
  record c2s.harness "$harness_line rc=$harness_rc" "$EXP_HARNESS" FAIL
fi

recheck_out=""
recheck_rc=1
if [ -f "$RECHECK" ] && [ -f "$LANE/$MANIFEST_REL" ]; then
  recheck_out=$(cd "$LANE" && python3 "$RECHECK" --manifest "$MANIFEST_REL" --source S053 2>&1)
  recheck_rc=$?
fi
if [ "$recheck_rc" -eq 0 ]; then
  record c2s.recheck-S053 "exit=$recheck_rc" "exit=0" PASS
else
  record c2s.recheck-S053 "exit=$recheck_rc" "exit=0" FAIL
fi
printf '%s\n' "$recheck_out" | head -n 2 | sed 's/^/gate   recheck: /'

binding_out=""
binding_rc=1
if [ -f "$BINDING" ]; then
  binding_out=$(cd "$LANE" && python3 "$BINDING" 2>&1)
  binding_rc=$?
fi
binding_line=$(printf '%s\n' "$binding_out" | grep -E '^(records=|PASS |FAIL )' | tail -n 1)
binding_line=${binding_line:-none}
if [ "$binding_rc" -eq 0 ]; then
  record c2s.capture-binding "$binding_line exit=$binding_rc" "exit=0" PASS
else
  record c2s.capture-binding "$binding_line exit=$binding_rc" "exit=0" FAIL
fi

# ---------------------------------------------------------------- 3. census
printf '%s\n' '--- 3. sources census validate'
census_out=""
census_rc=1
if [ -f "$CENSUS_SCRIPT" ]; then
  census_out=$(bash "$CENSUS_SCRIPT" validate --root "$FLEET_ROOT" kasegi 2>&1)
  census_rc=$?
fi
unexpected=0
if [ "$census_rc" -eq 0 ] && [ -n "$census_out" ]; then
  unexpected=$(printf '%s\n' "$census_out" \
    | grep -vcE '^kasegi[[:space:]]+(W04[[:space:]]+S02[89][[:space:]]|ok[[:space:]])') || true
  unexpected=${unexpected:-1}
fi
if [ "$census_rc" -eq 0 ] && [ "$unexpected" = 0 ]; then
  record census.validate "exit=0 unexpected=$unexpected" "exit=0 unexpected=0" PASS
else
  record census.validate "exit=$census_rc unexpected=$unexpected" "exit=0 unexpected=0" FAIL
fi
printf '%s\n' "$census_out" | sed 's/^/gate   census: /'

# ---------------------------------------------------------------- 4. quiescence
printf '%s\n' '--- 4. quiescence (E9)'
status_out=$(git -C "$LANE" status --porcelain 2>&1) || true
status_lines=$(count_text_lines "$status_out")
if [ "$status_lines" = 0 ]; then
  record quiescence.worktree "dirty=$status_lines" "dirty=0" PASS
else
  record quiescence.worktree "dirty=$status_lines" "dirty=0" FAIL
  printf '%s\n' "$status_out" | head -n 10 | sed 's/^/gate   dirty: /'
fi

seat_dirs=""
if [ -d "$SCRATCH_ROOT/kasegi-r36" ]; then
  seat_dirs=$(find "$SCRATCH_ROOT/kasegi-r36" -mindepth 1 -maxdepth 1 -type d 2>/dev/null) || true
fi
seat_count=$(count_text_lines "$seat_dirs")
if [ "$seat_count" = 0 ]; then
  record quiescence.scratch-seats "leftover=$seat_count" "leftover=0" PASS
else
  record quiescence.scratch-seats "leftover=$seat_count" "leftover=0" FAIL
  printf '%s\n' "$seat_dirs" | sed 's/^/gate   leftover: /'
fi

# ---------------------------------------------------------------- verdict
if [ "$FAILED" -eq 0 ]; then VERDICT=PASS; EXIT=0; else VERDICT=FAIL; EXIT=1; fi
printf 'gate verdict=%s checks=%d failed=%d\n' "$VERDICT" "$CHECKS" "$FAILED"

# ---------------------------------------------------------------- 5. receipt
receipt=$(cat <<EOF
### Round-36 post-integration gate receipt (template)

| field | value |
|---|---|
| gate script | corpus/instruments/r36-post-integration-gate.sh (v1) |
| lane | $LANE_REAL |
| exported ref | $REF |
| run at (UTC) | <UTC> |
| C1 suite (\`--export-ref\`) | closed=$closed exit=$suite_rc |
| C1 suite (\`--selftest\`) | cases=$st_cases failures=$st_failures exit=$selftest_rc |
| C2 counter: frontier rows | $frontier (expect $EXP_FRONTIER) |
| C2 counter: registry rows | $registry (expect $EXP_REGISTRY) |
| C2 counter: entries citing S053 | $citing (expect $EXP_CITING) |
| C2 supporting: knowledge entries | $knowledge (expect $EXP_KNOWLEDGE) |
| C2 supporting: harness | $harness_line (expect $EXP_HARNESS) |
| C2 supporting: source-recheck S053 | exit=$recheck_rc |
| C2 supporting: capture-binding | exit=$binding_rc |
| census validate | exit=$census_rc unexpected=$unexpected |
| quiescence: worktree | dirty=$status_lines (expect 0) |
| quiescence: scratch seats | leftover=$seat_count (expect 0) |
| gate verdict | $VERDICT ($CHECKS checks, $FAILED failed) |
| score after | <SCORE_AFTER> |
| L1 signoff | <L1_NAME> <DATE> |

Per-check lines (machine form, in run order):

$(printf '%s\n' "${ROWS[@]}" | sed 's/^/- /')
EOF
)

printf '\n%s\n' "$receipt"

if [ -n "$OUT_REAL" ]; then
  printf '%s\n' "$receipt" > "$OUT_REAL" || die_usage "cannot write --out: $OUT_REAL"
  printf 'gate wrote receipt: %s\n' "$OUT_REAL" >&2
fi

exit "$EXIT"
```

---

## 4. Verification (all runs measured in this session)

### 4.1 Syntax and lint

```
$ bash --version | head -1     → GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
$ bash -n r36-post-integration-gate.sh   → exit 0
$ bash -n r36-post-integration-gate.sh   → exit 0   (second, independent run)
$ shellcheck -s bash r36-post-integration-gate.sh → exit 0 (no findings)
```

The first shellcheck pass reported 7 × SC2015 (`A && B || C`), 1 × SC2012 (`ls`), 1 × SC2126
(`grep|wc -l`); all nine were rewritten (`if/else`, `find -maxdepth 1`, `grep -vcE`) rather than
suppressed, and the re-run is silent. `shellcheck 0.11.0`.

### 4.2 `--plan` executes nothing and names every command

```
gate note=lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin
gate note=ref=b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
gate note=census=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
gate note=plan=1 (nothing executed)
plan cmd: bash /…/corpus/instruments/r36-closure.sh --export-ref b47f2cdf…
plan cmd: bash /…/corpus/instruments/r36-closure.sh --selftest
plan cmd: grep -cE '^\| F[0-9]+ \|' /…/corpus/README.md
plan cmd: grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /…/corpus/SOURCES.md
plan cmd: grep -rlE '^source: S053 ' /…/corpus/knowledge | wc -l
plan cmd: ls /…/corpus/knowledge/*.md | wc -l
plan cmd: python3 /…/corpus/instruments/frontier-recheck-count.py
plan cmd: python3 /…/corpus/instruments/source-recheck.py --manifest …/round-36/manifest.json --source S053
plan cmd: python3 /…/corpus/instruments/capture-binding-check.py
plan cmd: bash /…/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
plan cmd: git -C /…/kasegi-shokunin status --porcelain
plan cmd: find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d
plan_exit=0
```

### 4.3 Pre-integration run on the real lane — the gate is not always-green

Run at `2026-10-26` against the claims-freeze head `b47f2cdf…` (the C1 suite is not landed yet, so
the C1 checks and the C2 artifacts do not exist). Every C2 counter reads its frozen **before**
value and the gate exits 1:

```
gate check=preflight.suite-present    value=missing                  expect=present                  verdict=FAIL
gate check=preflight.census-present   value=present                  expect=present                  verdict=PASS
gate check=c1.export-ref              value=closed=none exit=1       expect=closed=9/9 exit=0        verdict=FAIL
gate check=c1.selftest                value=cases=none failures=none exit=1 expect=cases=9 failures=0 exit=0 verdict=FAIL
gate check=c2.frontier-rows           value=18                       expect=19                       verdict=FAIL
gate check=c2.registry-rows           value=52                       expect=53                       verdict=FAIL
gate check=c2.entries-citing-S053     value=0                        expect=1                        verdict=FAIL
gate check=c2s.knowledge-entries      value=47                       expect=48                       verdict=FAIL
gate check=c2s.harness                value=entries=21 pass=21 exit=0 rc=0 expect=entries=22 pass=22 exit=0 verdict=FAIL
gate check=c2s.recheck-S053           value=exit=1                   expect=exit=0                   verdict=FAIL
gate check=c2s.capture-binding        value=records=42 bound=42 unbound=0 exit=0 expect=exit=0   verdict=PASS
gate check=census.validate            value=exit=0 unexpected=0      expect=exit=0 unexpected=0      verdict=PASS
gate check=quiescence.worktree        value=dirty=9                  expect=dirty=0                  verdict=FAIL
gate check=quiescence.scratch-seats   value=leftover=47              expect=leftover=0               verdict=FAIL
gate verdict=FAIL checks=14 failed=11
gate_exit=1
```

`18 / 52 / 0 / 47 / entries=21 pass=21` reproduce `claims.json` round-36 `before` values exactly,
and `capture-binding records=42 bound=42 unbound=0` and `census exit=0 unexpected=0` (W04
S028/S029 only) confirm the two checks that must already be green at base. `dirty=9` is this
wave's untracked registry/plan files; `leftover=47` is the live seat population (all 47 are this
wave's in-flight seat dirs, mine included) — i.e. exactly the two things E9 requires to be 0 at
filing.

### 4.4 No-write proof, controlled (fixture built with `git archive`, so nothing in the lane is touched)

```
D=<scratch>/sandbox/lane ; mkdir -p ; git -C "$D" init -q
fixture_toplevel=/fast/scratch/hyaku/kasegi-r36/ExecGateReviewPrep/sandbox/lane
fixture_verified=1                      # realpath(toplevel) == realpath($D)
git -C <LANE> archive b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6 | tar -x -C "$D"
git -C "$D" add -A ; git -C "$D" commit -q -m "fixture: r36 frozen head tree"
fixture HEAD 2d9504edc9b438bdebc7f18ec5b1d304b2a1d272 ; status --porcelain → 0 lines
```

Full-tree fingerprint = `(relpath → size, mtime_ns, sha256)` over every non-`.git` file, taken
immediately before and immediately after `bash r36-post-integration-gate.sh --lane <fixture>`:

```
sandbox_before=7160 after=7160 added=0 removed=0 changed=0
sbx_index_unchanged=1                   # .git/index (mtime,size) identical too
git -C <fixture> status --porcelain → 0 lines
```

7160 files, byte- and mtime-identical: the gate created, modified and touched nothing, and did not
even refresh the fixture's git index. This run exercised every phase (14 checks, 9 FAIL, exit 1)
including the three python instruments and the fleet census, so the zero-diff covers the
instrument calls, not just the shell.

### 4.5 No-write proof, real lane (attributable despite concurrent sibling writes)

Same fingerprint over the real lane (9465 non-`.git` files), before and after
`bash r36-post-integration-gate.sh --lane <LANE>`:

```
lane_before=9465 after=9470 added=5 removed=0 changed=3
  ADDED .ufo/waves/round-36/wave1/ExecManifestChecks.md
  ADDED .ufo/waves/round-36/wave1/ExecScoreGap.md
  ADDED .ufo/waves/round-36/wave1/ScoutQuarantine.md
  ADDED .ufo/waves/round-36/wave1/ScribeMistakes.md
  ADDED .ufo/waves/round-36/wave1/ScribeRowS053.md
  CHANGED .ufo/waves/round-36/wave1/ExecAncestry.md
  CHANGED .ufo/waves/round-36/wave1/ScribeConsiderthese.md
  CHANGED .ufo/waves/round-36/wave1/ScribeShonen.md
lane_status_unchanged=1                 # git status --porcelain identical before/after (9 lines)
```

Every diff is a sibling seat's own receipt appearing or growing during the wall-clock window
(`ExecManifestChecks`, `ExecScoreGap`, `ScoutQuarantine`, `ScribeMistakes`, `ScribeRowS053`,
`ExecAncestry`, `ScribeConsiderthese`, `ScribeShonen` are live roster peers, none of them my id).
The gate has no code path that names, opens or writes those paths (`grep` of the script for write
redirects returns exactly one: `> "$OUT_REAL"`), and the controlled fixture run over the same code
path diffs to zero. Attribution is therefore by construction + controlled replication, not by
absence of concurrent activity — which is why §4.4 exists.

### 4.6 Static write audit and guard tests

Only mutation construct in the script (comments excluded):

```
$ grep -nE '>|>>|mkdir|touch|cp |mv |rm |tee|sed -i|mktemp|install -|truncate|find .*-delete' \
      r36-post-integration-gate.sh | grep -vE '2>&1|>&2|2>/dev/null|^\s*#'
403:  printf '%s\n' "$receipt" > "$OUT_REAL" || die_usage "cannot write --out: $OUT_REAL"
$ grep -oE '\bgit [a-z-]+' r36-post-integration-gate.sh | sort | uniq -c
      7 git -            (the `git -C …` invocations: rev-parse ×3, status ×1, + prose)
```

| test | invocation | measured |
|---|---|---|
| T1 `--out` inside the lane | `--lane <fixture> --out <fixture>/leak.md` | exit **2**, `--out resolves inside the lane (refused): …/sandbox/lane/leak.md`, `t1_leak=0` (no file created) |
| T2 `--out` outside the lane | `--lane <fixture> --scratch-root … --out <scratch>/t2-receipt.md` | exit 1 (checks fail pre-integration), receipt written outside: 1813 bytes, `t2_tree_unchanged=1` (fixture fingerprint byte-identical) |
| T3 unknown argument | `--nope` | exit **2**, `unknown argument: --nope` |
| T3b non-worktree lane | `--lane <scratch>/notarepo` | exit **2**, `not a git worktree: …` |
| T3c unresolvable ref | `--ref deadbeef` | exit **2**, `ref does not resolve to a commit: deadbeef` |
| `--help` | `--help` | exit 0, usage printed |

The `--out` refusal is realpath-based (`realpath -m` on the target, compared against
`realpath -e` of the lane and its descendants), so `../` and symlinked spellings cannot bypass it.
The guard is unconditional: it runs before any phase, so a mis-invocation cannot reach the census
or the suite.

### 4.7 Discrimination — both directions exercised per check

Fail direction: §4.3 (before-values → FAIL) and §4.4 (missing suite → FAIL; missing round-36
manifest → `c2s.recheck-S053 exit=1` FAIL, fail-closed rather than skipped-as-pass).

Pass direction (in the fixture only; no lane byte touched): append one `| F19 | … |` row to
`corpus/README.md`, one `| S053 | … |` row to `corpus/SOURCES.md`, and one
`corpus/knowledge/zz-gate-probe.md` carrying `source: S053 `:

```
gate check=c2.frontier-rows           value=19  expect=19  verdict=PASS
gate check=c2.registry-rows           value=53  expect=53  verdict=PASS
gate check=c2.entries-citing-S053     value=1   expect=1   verdict=PASS
gate check=c2s.knowledge-entries      value=48  expect=48  verdict=PASS
t5 added=0 removed=0 changed=0     # the gate itself wrote nothing during this run either
```

Scratch-seat check, both directions: with `--scratch-root` pointing at an empty root →
`leftover=0 PASS`; with one planted `kasegi-r36/ProbeSeat` dir → `leftover=1 FAIL`. Real scratch
root → `leftover=47 FAIL` (§4.3).

### 4.8 Parser unit tests (the C1 line shapes the gate must read)

Same `sed` expressions the script uses, on synthetic lines:

| input | parsed |
|---|---|
| `closed=9/9 exit=0` | `closed=9/9` |
| `r36-closure: all checks pass closed=9/9` | `closed=9/9` |
| `closed=0/9 exit=1` | `closed=0/9` |
| `closed=7/7` | `closed=7/7` |
| `no counters here` | `closed=none` → FAIL (fail-closed) |
| `selftest cases=9 failures=0` | `cases=9 failures=0` |
| `selftest cases=9 failures=2` | `cases=9 failures=2` → FAIL |

`--ref` normalisation: `--ref HEAD` → `2d9504edc9b438bdebc7f18ec5b1d304b2a1d272`; `--ref 2d9504`
→ the same full id.

---

## 5. Template receipt (exactly what the script prints; §4.3 values)

```markdown
### Round-36 post-integration gate receipt (template)

| field | value |
|---|---|
| gate script | corpus/instruments/r36-post-integration-gate.sh (v1) |
| lane | /home/vgpnk/Projects/shokunin/kasegi-shokunin |
| exported ref | b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6 |
| run at (UTC) | <UTC> |
| C1 suite (`--export-ref`) | closed=none exit=1 |
| C1 suite (`--selftest`) | cases=none failures=none exit=1 |
| C2 counter: frontier rows | 18 (expect 19) |
| C2 counter: registry rows | 52 (expect 53) |
| C2 counter: entries citing S053 | 0 (expect 1) |
| C2 supporting: knowledge entries | 47 (expect 48) |
| C2 supporting: harness | entries=21 pass=21 exit=0 (expect entries=22 pass=22 exit=0) |
| C2 supporting: source-recheck S053 | exit=1 |
| C2 supporting: capture-binding | exit=0 |
| census validate | exit=0 unexpected=0 |
| quiescence: worktree | dirty=9 (expect 0) |
| quiescence: scratch seats | leftover=47 (expect 0) |
| gate verdict | FAIL (14 checks, 11 failed) |
| score after | <SCORE_AFTER> |
| L1 signoff | <L1_NAME> <DATE> |

Per-check lines (machine form, in run order):

- preflight.suite-present|missing|present|FAIL
- preflight.census-present|present|present|PASS
- c1.export-ref|closed=none exit=1|closed=9/9 exit=0|FAIL
- c1.selftest|cases=none failures=none exit=1|cases=9 failures=0 exit=0|FAIL
- c2.frontier-rows|18|19|FAIL
- c2.registry-rows|52|53|FAIL
- c2.entries-citing-S053|0|1|FAIL
- c2s.knowledge-entries|47|48|FAIL
- c2s.harness|entries=21 pass=21 exit=0 rc=0|entries=22 pass=22 exit=0|FAIL
- c2s.recheck-S053|exit=1|exit=0|FAIL
- c2s.capture-binding|records=42 bound=42 unbound=0 exit=0|exit=0|PASS
- census.validate|exit=0 unexpected=0|exit=0 unexpected=0|PASS
- quiescence.worktree|dirty=9|dirty=0|FAIL
- quiescence.scratch-seats|leftover=47|leftover=0|FAIL
```

Placeholder tokens are `<UTC>`, `<SCORE_AFTER>`, `<L1_NAME>`, `<DATE>` — the four facts the gate
cannot measure. They are **receipt** tokens: the script never emits a `<...LANE_HASH>` token and
carries a header warning that none of its output may be pasted into `SCORECARD.md`, whose E1 limb
fails on the `filled by the L1` line and on a bare `<LANE_HASH>` token.

---

## 6. Exact post-integration invocation for the L1

```bash
# 1. confirm quiescence first: the gate counts leftover seat dirs under
#    /fast/scratch/hyaku/kasegi-r36, so run it after every seat (this one
#    included) has removed its scratch dir.
find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d   # expect: no output

# 2. run the gate against the FINAL lane commit
bash r36-post-integration-gate.sh \
     --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
     --ref  "$(git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD)" \
  | tee /tmp/r36-gate-run.txt        # stdout only; tee writes outside the lane

# 3. exit 0 == all 14 checks PASS. Anything non-zero: the FAIL lines name the
#    phase, the value and the expectation.
```

`--ref` is what C1's `--export-ref` receives; pass the same hash the SCORECARD's Final lane
commit line names, so the gate and E1 cannot disagree about which commit is being judged.

---

## 7. Risks and limits (measured or structural, not hedged)

- **R1 — the C1 parsers are untested against the real suite.** `r36-closure.sh` is not committed
  at this seat's write time (a sibling is building it), so `closed=N/M` and
  `selftest cases=N failures=N` are matched by the shapes frozen in `claims.json`, and §4.8
  exercises those shapes on synthetic lines only. If the landed suite prints `closed=9/9` inside
  a differently-worded line the `.*closed=….*` matcher still finds it; if it prints a malformed
  `closed=9/9/9` the matcher would read `9/9` and pass a malformed line. Residual risk, stated.
- **R2 — supporting-instrument expectations are frozen at the C2 after-values.** A legitimate
  change of those values (e.g. a knowledge entry added after the freeze) turns the gate red; that
  is intended (the gate is a freeze check, not a trend check), but the `EXP_*` block is the one
  place to update if the L1 re-freezes.
- **R3 — the census is fleet-rooted, not lane-rooted.** `sources-census.sh validate --root
  {FLEET} kasegi` validates the real lane even when `--lane` points at a fixture. That is what the
  frozen C2 predicate asks for; it means the gate's census line is evidence about the lane's
  registry, not about the `--lane` argument. Stated because §4.4's fixture run still printed the
  real lane's registry line.
- **R4 — `git status --porcelain` may refresh `.git/index`.** It writes no worktree bytes; in the
  fixture run the index `(mtime,size)` was identical after the run (`sbx_index_unchanged=1`), so
  the refresh is not even observable there. It remains the one `git` verb in the script that is
  not strictly read-only in principle.
- **R5 — the gate does not re-implement E1–E9.** It delegates closure to `r36-closure.sh` and adds
  independent witnesses only for what it can measure cheaply (both E9 limbs, the census, the C2
  counters). A suite that passed while its own fixtures were broken would still pass this gate;
  `--selftest` is the limb that catches that, and it is checked (row 1.2).
- **R6 — placement is the L1's decision, not taken here.** This seat's write scope is the receipt
  plus scratch, so the script is not landed anywhere. Two placements fit: wave-local
  (`.ufo/waves/round-36/gate/r36-post-integration-gate.sh`) — no SKILL.md registry row, no change
  to the instrument set the C1 suite or `capture-binding-check`/`resolve.py` walk; or
  `corpus/instruments/` — which then wants a `Gates & probes` registry row like its siblings.
  Wave-local is the lower-risk default for a post-integration runner whose output is a wave
  receipt, not an axis measurement. Either way the round-36 lesson should name it so the runner is
  not unowned next round.
- **R7 — the gate counts all children of `{scratch}/kasegi-r36`.** At gate time every seat dir must
  already be removed; a runner that creates its own scratch dir inside that tree before running the
  gate will see `leftover>=1`. §6 puts the quiescence probe before the run for this reason.

---

## 8. Tooling

No installs, no upgrades, no `pacman` (transactions are paused host-wide). Everything used was
already present:

| tool | version | used for |
|---|---|---|
| GNU bash | 5.3.20(1) | the script, `bash -n` |
| ShellCheck | 0.11.0 | lint (exit 0) |
| git | 2.56.0 | read-only `rev-parse`, `status`, `archive`, fixture `init`/`add`/`commit` inside the verified scratch fixture |
| Python | 3.14.8 | the lane's own instruments (invoked by the gate) + the sha256 fingerprint helper (scratch-only) |
| realpath | 0.8.0 | `--out` containment assertion |

The only `git` commands that mutate anything ran inside the `mktemp`-style scratch fixture whose
toplevel was verified equal to its own directory (`fixture_verified=1`), per the round's git rule.
No mutating git command ran in the lane, the fleet root, shokuknow, or any source tree.

---

## 9. Scratch

Everything lived under `/fast/scratch/hyaku/kasegi-r36/ExecGateReviewPrep/` (script, fixture repo,
eight fingerprint JSONs, run logs, `--out` probe receipt) and is removed with
`rm -rf /fast/scratch/hyaku/kasegi-r36/ExecGateReviewPrep` after this receipt was written. The
script survives in §3 verbatim (407 lines, sha256 `fad8bcd2…2dcf7bb89`), so the L1 can land it
without the scratch tree.
