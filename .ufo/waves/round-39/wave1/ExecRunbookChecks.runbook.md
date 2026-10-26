# Round 39 integration runbook (L1 KasegiR39) — landing order, commit boundaries, validation matrix

Land the round-39 wave-1 deliverables into `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, commit the
judged-head state, take the C1 receipt over the receipt-bearing head, then run the frozen validations.
Every expected value below is cross-checked against `.ufo/waves/round-39/claims.json` as corrected by
`.ufo/waves/round-39/claims-erratum-1.md` (commit `7beae60`); values this seat re-measured read-only on
2026-10-26 are marked `[measured]`.

## 0. Variables and invariants

```bash
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
W=$LANE/.ufo/waves/round-39/wave1
JJ=/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh
BASE=480b1a505a2dfc14a4f718d16d63808247214d0a
R38=66703acaaff50529a35be49aa8759d04140720ad
WORK=/fast/scratch/hyaku/kasegi-r39-gate
FG=$LANE/.ufo/waves/round-39/final-gates
cd "$LANE"
```

- `jj-lane.sh commit` is pathspec-limited and prints `landed <hash>`; that line is the only citable output.
  Identity is the lane id: `--as kasegi`.
- Fleet root and shokuknow stay read-only; no pacman; no mutating git/jj outside `jj-lane.sh`.
- The suite is export-mode only: every run needs `--export-ref` and a `--work` outside the lane and outside
  `/fast/scratch/hyaku/kasegi-r3[678]` (G6 and the pinned r37 suite's E9 read live scratch state).
- `git status --porcelain` must be empty at filing. Untracked wave-1 artefacts are committed at boundary B8,
  never left behind.

## 1. Pre-flight — stop on any MISSING line

```bash
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status      # must be green
git rev-parse HEAD          # expect 7beae60… (claims erratum 1) or later; record it
git status --porcelain      # untracked wave-1 files only, before B8
for f in \
  ExecFrontierCapture.S057.txt ExecFrontierCapture.manifest.json \
  ScribeRowS057.row.md ScribeRowsRejected.S056.row.md ScribeRowsRejected.S058.row.md \
  ScribeRowsRejected.S059.row.md ScribeSearchLog.searchlog.append.md ScribeEntryF22.entry.md \
  ExecSuiteBuild.r39-closure.sh \
  ExecCorrectionsR2.round38-lesson.append.md ExecCorrectionsR2.log.append.md \
  ExecCorrectionsR2.scorecard.append.md ExecCorrectionsR2.shonen.append.md \
  ExecQualityCriteria.quality.append.md ExecMistakesDraft.mistakes.md ScribeLessonGate.gate.md \
  ExecConsidertheseLedger.ledger.append.md ExecConsiderthese.scorecard.append.md \
  ScribeProvinceF22.province.append.md ScribeFrontierF22.readme.append.md ScribeShonen.shonen.append.md \
  ExecJunkRecheck.manifest.json ExecJunkRecheck.junk-recheck.txt \
  ; do test -s "$W/$f" || echo "MISSING $f"; done
```

Before landing, also require: the wave is settled and the results document exists at
`.ufo/waves/round-39/kasegi-r39-build-results.json` (preferred) or `.ufo/waves/round-39/wave1-results.json`,
parseable, with exactly 49 entries whose `name` values are distinct (G4 identity field is `name`;
`agent` is the role and repeats).

## 2. Destination map

| Wave-1 file (in `$W`) | Lane path | Boundary |
|---|---|---|
| `ExecFrontierCapture.S057.txt` | `corpus/source-snapshots/round-39/S057.txt` | B1 |
| `ExecFrontierCapture.manifest.json` | `corpus/source-snapshots/round-39/manifest.json` | B1 |
| `ScribeRowS057.row.md`, `ScribeRowsRejected.S0{56,58,59}.row.md` | four rows in `corpus/SOURCES.md` `## Registry`, after the `S055` row | B2 |
| `ScribeSearchLog.searchlog.append.md` | last bullet of `corpus/SOURCES.md` `## Search log` | B2 |
| `ScribeEntryF22.entry.md` | `corpus/knowledge/cisa-when-to-issue-vex.md` | B2 |
| (compose) | one sorted line `corpus/knowledge/cisa-when-to-issue-vex.md` in `corpus/instruments/knowledge-expected.txt` | B2 |
| `ExecSuiteBuild.r39-closure.sh` | `corpus/instruments/r39-closure.sh` | B3 |
| `ExecCorrectionsR2.round38-lesson.append.md` | EOF append `corpus/lessons/round-38.md` | B5 |
| `ExecMistakesDraft.mistakes.md` + `ScribeLessonGate.gate.md` | new `corpus/lessons/round-39.md` (`## Mistakes`, `## Gate`) | B5 |
| `ExecCorrectionsR2.log.append.md` | `LOG.md`, new `## Round 39` entry | B5 |
| `ExecCorrectionsR2.scorecard.append.md` | EOF append `SCORECARD.md` | B5 |
| `ExecCorrectionsR2.shonen.append.md`, `ScribeShonen.shonen.append.md` | EOF append `SHONEN.md` box lines | B5 |
| `ExecQualityCriteria.quality.append.md` | EOF append `corpus/QUALITY.md` | B5 |
| `ExecConsidertheseLedger.ledger.append.md` | EOF append `corpus/knowledge/considerthese-proposals-ledger.md` | B6 |
| `ExecConsiderthese.scorecard.append.md` | `SCORECARD.md`, before the closing `## Round 39 result` section | B6 |
| `ScribeProvinceF22.province.append.md` | EOF append `PROVINCE.md` (one line: 156 → 157) | B7 |
| `ScribeFrontierF22.readme.append.md` | EOF append `corpus/README.md` (28 lines: 486 → 514) | B7 |
| (compose) | `| r39-closure.sh | gate | …` row appended after the `r38-closure.sh` row at `SKILL.md` EOF | B7 |
| (generate) | `.ufo/waves/round-39/declared-blocks.txt` | B7 |
| all receipts/deliverables/fixtures in `$W`, results document, `swarm-registry.json`, `$FG/reds.txt`, remaining orchestrator artefacts under `.ufo/waves/round-39/` | as-is | B8 = J |

## 3. Landing sequence

### B1 — capture

```bash
install -D -m 0644 "$W/ExecFrontierCapture.S057.txt"      corpus/source-snapshots/round-39/S057.txt
install -D -m 0644 "$W/ExecFrontierCapture.manifest.json" corpus/source-snapshots/round-39/manifest.json
cmp "$W/ExecFrontierCapture.S057.txt" corpus/source-snapshots/round-39/S057.txt
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-39/manifest.json --source S057
```

Expected (exit 0) `[measured]`:

```
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
```

```bash
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: C2 capture — S057 CISA When-to-Issue VEX (PDF text + manifest Q1-Q4)" \
  -- corpus/source-snapshots/round-39
```

### B2 — rows, entry, expected-list line

Insert the four row files as one block after the `| S055 |` registry row and before `## Paths`; append the
search-log bullet as the last bullet of `## Search log`; write the entry; insert the expected-list line in
sorted position (`chinese-…` < `cisa-when-to-issue-vex.md` < `citation-bases.md`).

```bash
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # 59 (erratum E1; freeze text said 58)
awk -F'|' '/^\| S05[6-9] /{print $2, NF}' corpus/SOURCES.md           # four rows, each NF=13
ls corpus/knowledge/*.md | wc -l                                       # 51
diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | sort) \
     <(ls corpus/knowledge/*.md | sort) && echo expected-list-in-sync
grep -rlE '^source: S057' corpus/knowledge | wc -l                     # 1
```

```bash
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: C2 rows/entry — S057 mined + S056/S058/S059 rejected, F22 entry, expected-list line" \
  -- corpus/SOURCES.md corpus/knowledge/cisa-when-to-issue-vex.md corpus/instruments/knowledge-expected.txt
```

### B3 — instrument

```bash
cp "$W/ExecSuiteBuild.r39-closure.sh" corpus/instruments/r39-closure.sh
cmp "$W/ExecSuiteBuild.r39-closure.sh" corpus/instruments/r39-closure.sh
bash -n corpus/instruments/r39-closure.sh
sha256sum corpus/instruments/r39-closure.sh            # record; this is the receipt's suite-sha256
bash corpus/instruments/r39-closure.sh; echo $?        # 2 — plain run refused
stat -c '%a %n' corpus/instruments/r39-closure.sh      # 644 — the r37/r38 suites are 644; no executable bit
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: C1 instrument — r39-closure.sh (G1-G8, export-mode only, graded selftest)" \
  -- corpus/instruments/r39-closure.sh
```

### B4 — required reds (no commit yet)

```bash
mkdir -p "$FG" "$WORK"
{
  printf '# round-39 C1 required reds — run %s by the L1; --work outside the lane and outside kasegi-r3[678]\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '$ bash corpus/instruments/r39-closure.sh --export-ref %s\n' "$BASE"
  bash corpus/instruments/r39-closure.sh --export-ref "$BASE" --lane "$LANE" --work "$WORK/red-base" 2>&1
  printf 'exit=%s\n' "$?"
  printf '$ bash corpus/instruments/r39-closure.sh --export-ref %s\n' "$R38"
  bash corpus/instruments/r39-closure.sh --export-ref "$R38" --lane "$LANE" --work "$WORK/red-r38" 2>&1
  printf 'exit=%s\n' "$?"
} > "$FG/reds.txt"
grep -c '^closed=[0-7]/8 exit=1$' "$FG/reds.txt"    # 2
```

Both reds must end `closed=<8/8` and exit 1. `$FG/reds.txt` is committed at B8 so G3 finds a transcript for
every hashed red quoted in `SCORECARD.md`, `SHONEN.md`, `LOG.md` or `corpus/lessons/round-38.md`.

### B5 — corrections and records

```bash
cat "$W/ExecCorrectionsR2.round38-lesson.append.md" >> corpus/lessons/round-38.md
cat "$W/ExecCorrectionsR2.scorecard.append.md"      >> SCORECARD.md
cat "$W/ExecCorrectionsR2.shonen.append.md"         >> SHONEN.md
test -s "$W/ScribeShonen.shonen.append.md" && cat "$W/ScribeShonen.shonen.append.md" >> SHONEN.md
cat "$W/ExecQualityCriteria.quality.append.md"      >> corpus/QUALITY.md
# compose corpus/lessons/round-39.md: heading, claims/erratum pointers, then the Gate block
# (ScribeLessonGate.gate.md) and the Mistakes table (ExecMistakesDraft.mistakes.md);
# compose the LOG.md "## Round 39 — 2026-10-26 — …" entry and merge the correction bullet.
```

`SHONEN.md` must carry the exact reference phrase (G2/G5): `judged head: export-ref of
.ufo/waves/round-39/final-gates/all-gates.txt`. No line that names a head/commit may carry a hex run of 7+
characters.

```bash
grep -c '^Correction (round 39)' SCORECARD.md corpus/lessons/round-38.md corpus/knowledge/considerthese-proposals-ledger.md
grep -cF 'judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt' SHONEN.md   # >=1
grep -cF $'\u27e8pending' corpus/lessons/round-39.md    # 0 (kill rule)
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: corrections — R2 overstate sweep, QUALITY R34-R36, lesson + Mistakes/Gate, LOG/SHONEN" \
  -- corpus/lessons/round-38.md corpus/lessons/round-39.md LOG.md SCORECARD.md SHONEN.md corpus/QUALITY.md
```

### B6 — ledger and saturation criteria

```bash
cat "$W/ExecConsidertheseLedger.ledger.append.md" >> corpus/knowledge/considerthese-proposals-ledger.md
cat "$W/ExecConsiderthese.scorecard.append.md"    >> SCORECARD.md
# then append the closing "## Round 39 result" section LAST, containing the reference phrase,
# the counter deltas, and no head hash:
cat >> SCORECARD.md <<'EOF'

## Round 39 result

Frontier 21 → 22 (F22 CISA When to Issue VEX Information, source S057); registry 55 → 59; knowledge
50 → 51; harness 24/24 → 25/25; binding 45/45 → 46/46; audit expected 50 → 51; census exit 0 (W04 S028/S029
only). C1 depth:verifiability 4 held; C2 coverage 7 held. Judged head: export-ref of
.ufo/waves/round-39/final-gates/all-gates.txt (receipt in that directory; the lane tip adds only the receipt).
EOF
grep -cF 'judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt' SCORECARD.md   # >=1
awk '/^## Round 39/{f=1} f&&/^## /&&!/^## Round 39/{f=0} f' SCORECARD.md | grep -c 'Final lane commit:'   # 0
grep -nE '^## Round-39 dispositions \(appended 2026-10-26\)' corpus/knowledge/considerthese-proposals-ledger.md
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: ledger — Round-39 dispositions (7 rows) and distance-to-next-score criteria in SCORECARD" \
  -- corpus/knowledge/considerthese-proposals-ledger.md SCORECARD.md
```

### B7 — declarations and declared blocks

```bash
cat "$W/ScribeProvinceF22.province.append.md" >> PROVINCE.md
cat "$W/ScribeFrontierF22.readme.append.md"   >> corpus/README.md
# append the r39-closure.sh row after the r38-closure.sh row at SKILL.md EOF (same eight columns)
wc -l PROVINCE.md corpus/README.md            # 157 and 514

mk_decl() { p=$1; set -- $(git diff --numstat "$BASE" -- "$p"); a=$1; d=$2
  [ "$d" = 0 ] || { echo "STOP $p deleted=$d"; return 1; }
  printf '%s %s %s\n' "$p" "$a" "$(tail -n "$a" "$p" | sha256sum | cut -d' ' -f1)"; }
{ mk_decl corpus/README.md; mk_decl PROVINCE.md; } > .ufo/waves/round-39/declared-blocks.txt
while read -r p n s; do
  [ "$(tail -n "$n" "$p" | sha256sum | cut -d' ' -f1)" = "$s" ] || echo "BAD $p"
done < .ufo/waves/round-39/declared-blocks.txt
git diff --numstat "$BASE" -- corpus/README.md PROVINCE.md    # added counts equal the declared counts
```

The declared block covers the WHOLE appended tail and is generated last, after every front-door edit.

```bash
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: declarations — F22 frontier/coverage rows, PROVINCE line, SKILL registry, declared-blocks" \
  -- PROVINCE.md corpus/README.md SKILL.md .ufo/waves/round-39/declared-blocks.txt
```

### B8 — evidence, then J

```bash
# verification-run receipts for every instrument in section 4 (capture them under $WORK; commit
# $FG/reds.txt only), then commit every remaining wave artefact so the tree is clean:
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: wave evidence — 49-seat wave receipts, results, required reds (judged-head state)" \
  -- .ufo/waves/round-39
git status --porcelain          # empty
J=$(git rev-parse HEAD); echo "J=$J"
git log -1 --format='%H %s'
```

`J` is the judged head: every round-39 change except `.ufo/waves/round-39/final-gates/all-gates.txt`.

## 4. Receipt cycle — J, bootstrap receipt, genuine receipt (Y)

G2 reads the receipt from the exported tree and requires `git diff --name-only <export-ref> REF` to list only
that receipt. The receipt therefore cannot be in the commit it names: it is committed on top of `J` and names
`J`. Consequence, by construction: an export of `J` itself prints 7/8 (G2 red — no receipt), and the 8/8 run
is taken over the receipt-bearing head. Never quote the `J`-only 7/8 as the judged run.

```bash
# 4.1 line set over J (for the receipt's non-G2 lines), then compose the receipt:
bash corpus/instruments/r39-closure.sh --export-ref "$J" --lane "$LANE" --work "$WORK/j-run" | tee "$WORK/j-run.txt"
bash corpus/instruments/r39-closure.sh --selftest --export-ref "$J" --lane "$LANE" --work "$WORK/j-selftest" | tee "$WORK/j-selftest.txt"
# 4.2 write $FG/all-gates.txt in this order (no other top-level G<n>/closed lines):
#     all-gates v3
#     export-ref=$J
#     suite-sha256=<sha256sum of corpus/instruments/r39-closure.sh at J>
#     run-ref=<R1, filled in below>
#     a '#' comment naming the run head, work dir, UTC time, lane HEAD and clean tree
#     the 8 G<n> payload=… closed=1 lines and the single closed=8/8 exit=0 line from the receipt-bearing run
#     the 8 graded selftest case=G<n> … positive=pass … verdict=pass lines and selftest cases=8 failures=0
#     (an optional export-ref-run: prefixed 7/8 block is admissible only if G2 still prints run-lines=1,
#      closed-line=1, selftest-lines=1 — verify on the R1 run before relying on it)
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: C1 bootstrap all-gates receipt (export-ref = judged head J)" \
  -- .ufo/waves/round-39/final-gates/all-gates.txt
R1=$(git rev-parse HEAD)
bash corpus/instruments/r39-closure.sh --export-ref "$R1" --lane "$LANE" --work "$WORK/r1-run" | tee "$WORK/r1-run.txt"
bash corpus/instruments/r39-closure.sh --selftest --export-ref "$R1" --lane "$LANE" --work "$WORK/r1-selftest" | tee "$WORK/r1-selftest.txt"
#    expect: closed=8/8 exit=0 ; G2 payload receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,
#    digest-match=1,run-lines=1,closed-line=1,selftest-lines=1,selftest-summary=1 ; selftest cases=8 failures=0
# 4.3 rewrite all-gates.txt with run-ref=$R1 and the EXACT R1 run/selftest lines (replacing, not appending),
#     then commit and re-run:
bash "$JJ" commit "$LANE" --as kasegi \
  -m "round-39: C1 genuine all-gates receipt (run + graded selftest over the receipt-bearing head)" \
  -- .ufo/waves/round-39/final-gates/all-gates.txt
Y=$(git rev-parse HEAD); echo "Y=$Y"
git diff --name-only "$J" "$Y"     # exactly .ufo/waves/round-39/final-gates/all-gates.txt
bash corpus/instruments/r39-closure.sh --export-ref "$Y" --lane "$LANE" --work "$WORK/y-run" | tee "$WORK/y-run.txt"
bash corpus/instruments/r39-closure.sh --selftest --export-ref "$Y" --lane "$LANE" --work "$WORK/y-selftest" | tee "$WORK/y-selftest.txt"
```

Precondition for every run at `R1`/`Y`: `git rev-parse HEAD` equals the exported commit and `git status
--porcelain` is empty. G8 executes the pinned r37 suite, whose E9 limb reads live state (`head-match`,
`status-dirty`) — a dirty tree or a moved tip reds G8 and drops the run to 7/8.

Post-run checks (no further commits; the lane tip stays `Y`):

```bash
git status --porcelain                                  # empty
git rev-parse HEAD                                      # Y
grep -cE '^export-ref=[0-9a-f]{40}$'                    "$FG/all-gates.txt"   # 1
grep -cE '^suite-sha256=[0-9a-f]{64}$'                  "$FG/all-gates.txt"   # 1
grep -cE '^G[1-8] payload=.* closed=1$'                 "$FG/all-gates.txt"   # 8
grep -c '^closed=8/8 exit=0$'                           "$FG/all-gates.txt"   # 1
grep -cE '^selftest case=G[1-8] .*positive=pass.*verdict=pass' "$FG/all-gates.txt"   # 8
grep -c '^selftest cases=8 failures=0$'                 "$FG/all-gates.txt"   # 1
test -z "$(find /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38 \
  /fast/scratch/hyaku/kasegi-r39 -mindepth 1 -maxdepth 1 -type d 2>/dev/null)" && echo scratch-clean
```

## 5. Commit boundary summary

| # | message | pathspec | output |
|---|---|---|---|
| B1 | round-39: C2 capture — S057 CISA When-to-Issue VEX (PDF text + manifest Q1-Q4) | `corpus/source-snapshots/round-39` | `landed <hash>` |
| B2 | round-39: C2 rows/entry — S057 mined + S056/S058/S059 rejected, F22 entry, expected-list line | `corpus/SOURCES.md corpus/knowledge/cisa-when-to-issue-vex.md corpus/instruments/knowledge-expected.txt` | `landed <hash>` |
| B3 | round-39: C1 instrument — r39-closure.sh (G1-G8, export-mode only, graded selftest) | `corpus/instruments/r39-closure.sh` | `landed <hash>` |
| B5 | round-39: corrections — R2 overstate sweep, QUALITY R34-R36, lesson + Mistakes/Gate, LOG/SHONEN | `corpus/lessons/round-38.md corpus/lessons/round-39.md LOG.md SCORECARD.md SHONEN.md corpus/QUALITY.md` | `landed <hash>` |
| B6 | round-39: ledger — Round-39 dispositions (7 rows) and distance-to-next-score criteria in SCORECARD | `corpus/knowledge/considerthese-proposals-ledger.md SCORECARD.md` | `landed <hash>` |
| B7 | round-39: declarations — F22 frontier/coverage rows, PROVINCE line, SKILL registry, declared-blocks | `PROVINCE.md corpus/README.md SKILL.md .ufo/waves/round-39/declared-blocks.txt` | `landed <hash>` |
| B8 | round-39: wave evidence — 49-seat wave receipts, results, required reds (judged-head state) | `.ufo/waves/round-39` | `landed <hash>` = **J** |
| R1 | round-39: C1 bootstrap all-gates receipt (export-ref = judged head J) | `.ufo/waves/round-39/final-gates/all-gates.txt` | `landed <hash>` |
| Y | round-39: C1 genuine all-gates receipt (run + graded selftest over the receipt-bearing head) | `.ufo/waves/round-39/final-gates/all-gates.txt` | `landed <hash>` = **Y** |

## 6. Validation matrix (after landing)

| Check | Command (from `$LANE`) | Expected | Source |
|---|---|---|---|
| frontier rows | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `22` (was 21) | C2 |
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `59` (was 55) | C2 + erratum E1 |
| knowledge entries | `ls corpus/knowledge/*.md \| wc -l` | `51` (was 50) | C2 |
| entries cite S057 | `grep -rlE '^source: S057' corpus/knowledge \| wc -l` | `1` | C2 |
| harness | `python3 corpus/instruments/frontier-recheck-count.py` | `PASS     F22  knowledge/cisa-when-to-issue-vex.md ids=S057 exit=0` then `entries=25 pass=25 exit=0` (was 24/24) | C2 |
| recheck S057 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` | 5 lines `S057:sha256 OK` + `S057:Q[1-4] OK … occurrences=1 …`, exit 0 | C2 `[measured]` |
| binding | `python3 corpus/instruments/capture-binding-check.py` | final line `records=46 bound=46 unbound=0` (was 45/45) | C2 |
| audit | `python3 corpus/instruments/recheck-audit.py --quiet` | `expect=present expected=51 missing=0 unexpected=0 exit=0` (was expected=50) | C2 |
| census | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi W04 S028 …`, `kasegi W04 S029 …`, `kasegi ok …/corpus/SOURCES.md`, exit 0 | C2 `[measured]` |
| suite, plain | `bash corpus/instruments/r39-closure.sh` | exit 2, refusal line | C1 `[measured on r38 model]` |
| suite at base | `bash corpus/instruments/r39-closure.sh --export-ref $BASE --lane $LANE --work $WORK/red-base` | `closed=<8/8 exit=1` | C1 |
| suite at r38 head | `bash corpus/instruments/r39-closure.sh --export-ref $R38 --lane $LANE --work $WORK/red-r38` | `closed=<8/8 exit=1` | C1 (hash per erratum E2) |
| suite at J | `bash corpus/instruments/r39-closure.sh --export-ref $J --lane $LANE --work $WORK/j-run` | `G2 payload=receipt=0,… closed=0` then `closed=7/8 exit=1` | structural, receipt absent |
| suite at Y | `bash corpus/instruments/r39-closure.sh --export-ref $Y --lane $LANE --work $WORK/y-run` | 8 × `G<n> payload=… closed=1` then `closed=8/8 exit=0` | C1 |
| selftest at Y | `bash corpus/instruments/r39-closure.sh --selftest --export-ref $Y --lane $LANE --work $WORK/y-selftest` | 8 × `selftest case=G<n> … positive=pass … verdict=pass`, `selftest cases=8 failures=0`, exit 0 | C1 |
| junk twin | `python3 corpus/instruments/source-recheck.py --manifest "$W/ExecJunkRecheck.manifest.json" --source S057` | 4 × `S057:J<n> MISMATCH reason=quote-not-found`, exit 1 | C2 |
| receipt diff | `git diff --name-only "$J" "$Y"` | exactly `.ufo/waves/round-39/final-gates/all-gates.txt` | C1 G2 |
| tree clean | `git status --porcelain` | empty | C1 kill rule |
| scratch | `ls -d /fast/scratch/hyaku/kasegi-r3[789]/*/ 2>/dev/null` | no output | C1 G6 |

## 7. Registry and rule notes that decide reds

- G1 declared blocks: two lines, README then PROVINCE; count = added lines of `git diff --numstat $BASE J`
  for the path, sha256 = `tail -n <count> | sha256sum`; both fence families (backtick and tilde) must walk
  closed; a `Correction (round 39)` inside an open fence does not count; every declared path must exist in
  the export. Recompute and recommit B7 if any front-door byte changes afterwards.
- G2 receipt: `all-gates v3` first line, one `export-ref=`, one `suite-sha256=` equal to the executing bytes,
  eight G lines, one `closed=8/8 exit=0`, eight graded selftest case lines, one `selftest cases=8 failures=0`;
  the payload keys/order are whichever the landed suite prints — copy them verbatim, never hand-write limbs.
- G3: any `--export-ref <hash> -> closed=K/K` or `closed=K/K exit=0` quoted in `SCORECARD.md`, `SHONEN.md`,
  `LOG.md` or `corpus/lessons/round-38.md` needs that hash inside a `$FG` file committed at J, or the sentence
  must contain `report-only`. Safest: quote the judged run by reference only; quote the base/r38 reds with the
  hashes already present in `$FG/reds.txt`.
- G4: every tracked `.ufo/waves/round-39/*-dispatch.json` needs a parseable sibling results document with
  exactly 49 entries and 49 distinct `name` values; identity is `name` (`agent` is the role and repeats).
- G5: the `## Round 39` SCORECARD section has zero `Final lane commit:` lines and no hex run beside a
  head/commit phrase; `SCORECARD.md` carries a line beginning `Correction (round 39)` naming the round-38
  overstate (`f06148c6` report-quoted-only).
- G6: at run time `kasegi-r37`/`kasegi-r38` absent or empty and `kasegi-r39` free of seat dirs; the suite's
  `--work` is outside the lane and outside `kasegi-r3[678]`.
- G7: `## Round-39 dispositions (appended 2026-10-26)` in the ledger after the round-38 sections, a line
  beginning `Correction (round 39)`, and at least three proposal rows including 1 and 3.
- G8: pinned r37 suite (sha256 `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` from
  `git show 2387dcf6:corpus/instruments/r37-closure.sh`) must end `closed=14/14 exit=0` over `Y`; the export's
  own r37 copy must hash to the pinned digest.

## 8. Measured constraints and discrepancies (do not lose these)

1. Registry after-count is 59, not the frozen 58 (erratum E1, commit `7beae60`, already filed). Four rows
   are appended (S057 mined + S056/S058/S059 rejected).
2. The r38 judged head is `66703acaaff50529a35be49aa8759d04140720ad`; the frozen text truncated it to 38
   characters (erratum E2). Use the 40-char form for every control run.
3. C1's "8/8 on J" is only satisfiable over the receipt-bearing head: the exported commit must contain the
   receipt, and the receipt names its parent J. Expected pair: J → `closed=7/8 exit=1`; Y → `closed=8/8
   exit=0`. Record both; quote only Y as the judged run.
4. G8 is live-state-bound: the pinned r37 suite's E9 requires the live lane clean and `HEAD` equal to the
   exported ref, so a replay of the r39 suite at a later tip prints 7/8 with `G8 … closed=0`. Take the judged
   run at Y with a clean tree and an empty `kasegi-r37`, and say so in the receipt comment.
5. `corpus/instruments/knowledge-expected.txt` must gain the F22 entry line or the audit prints
   `unexpected=corpus/knowledge/cisa-when-to-issue-vex.md` and exits 1 (expected=51 is unreachable without it).
6. QUALITY.md lives at `corpus/QUALITY.md`; it is 292 lines / 46,569 bytes at base, not 288 lines — measure
   before appending.
7. The suite deliverable was still in flight when this runbook was written; treat section 1's loop as the
   gate, and take G payload keys from the landed suite's own output.

## 9. Stop conditions

Stop and re-derive J (a new B8) if: any front-door byte changes after B7; `git diff --numstat $BASE J --
corpus/README.md PROVINCE.md` shows a deletion; a G line in the receipt does not match the landed suite's
output; `git diff --name-only J Y` lists anything besides the receipt; the tree is dirty at filing; or any
`kasegi-r3[789]` seat dir survives. Do not commit after Y except another receipt-only commit (same pathspec),
followed by a fresh run at the new head.
