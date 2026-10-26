# RevReportPreflight — round-39 wave2 (report contract preflight)

Seat: `RevReportPreflight` (reviewer, leaf, no subagent dispatch). Round: kasegi-shokunin 39, wave 2
(falsify), judged on depth:verifiability. Item: review the round report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kasegi.md` for contract completeness; if absent,
evaluate the readiness of its inputs. Receipt only. Attack posture: I did not author any deliverable
under review; every number below is a command I ran at read time.

Lane read at HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37` (`round-39: receipt Y (all-gates v3)`),
tracked tree clean (`git status --porcelain --untracked-files=no` → empty). All times UTC 2026-10-26.
Scratch `/fast/scratch/hyaku/kasegi-r39/RevReportPreflight/` (TMPDIR + every `--work` bound there),
removed before this receipt was finalized. No tool installed or upgraded (nothing needed: bash, git,
python3 present); no pacman run; no git/jj mutation anywhere (status/show/log/diff/rev-parse/
merge-base/archive reads only); no fleet-root, state, sibling or source-tree write.

## 0. Verdict

**The report does not exist yet** (checked twice, ~22:05Z and ~22:2xZ: `REPORT_ABSENT` /
`REPORT_STILL_ABSENT`; the round-39 report dir holds 11 sibling-lane reports, no `kasegi.md`). Its
inputs are **mostly ready and measured green** — every C2 after-number reproduces at HEAD, the C1
reds fire, all report-section inputs exist — **but the landed C1 evidence receipt
`.ufo/waves/round-39/final-gates/all-gates.txt` contains a line its own pinned instrument cannot
print (F1), and the frozen C1 verification commands are window-bound: they fail in the live lane
during wave 2 and become unreachable once wave-2 artifacts are committed (F2).** The report must not
be filed citing `closed=8/8 exit=0` at Y as an unconditional live fact without resolving F1–F3.

## 1. Report existence

```
$ [ -f /home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kasegi.md ] && echo EXISTS || echo ABSENT
REPORT_ABSENT            (first check)
REPORT_STILL_ABSENT      (re-check before filing this receipt)
$ ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-39/
chousa.md kaidoku.md kake.md kama.md kengaku.md kotodama.md kumitate.md mado.md mori.md tameshi.md tsukuroi.md
```

Per the item: readiness evaluation follows. Template precedent (round-38 report, read in full):
sections in order `## Work performed`, `## Landed changes`, `## Before → after measurements`,
`## Sources & frontier`, `## Trend verdicts`, `## SHONEN`, plus `## Stale-lane` and `## Tooling`;
the r38 report also models the honest treatment this round will need (it reported C1 "killed on its
frozen counting command" and let the operator rule).

## 2. Inputs that ARE ready (measured at HEAD 5006097)

**Git/commit skeleton — all green:**

```
git rev-parse --verify 46c66c268502abd1b2c342fc71bf88ccf721845b^{commit}  → OK (J resolves)
git merge-base --is-ancestor 46c66c2… HEAD  → yes (J ancestor of tip Y=5006097)
git merge-base --is-ancestor 480b1a50… HEAD → yes (base)
git merge-base --is-ancestor dcd31701… HEAD → yes (claims freeze)
git diff --name-only 46c66c2… HEAD          → .ufo/waves/round-39/final-gates/all-gates.txt  (exactly 1 path)
git rev-list --count 480b1a50…..HEAD        → 8
git status --porcelain --untracked-files=no | wc -l → 0 (tracked clean)
```

Judged-head naming rule holds: `git grep 46c66c2… 46c66c2` → no hits (no file at J names J);
at HEAD exactly one hit (the receipt itself); `git grep 5006097…` at HEAD → no hits.

**C2 after-state — all nine frozen counting commands green at HEAD** (cross-checked against
claims.json + erratum E1 and the wave-1 receipts; no fabricated numbers found on the C2 side):

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                              → 22
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md    → 59   (E1: 59, not 58)
grep -rlE '^source: S057' corpus/knowledge | wc -l                      → 1
python3 corpus/instruments/frontier-recheck-count.py                    → entries=25 pass=25 exit=0
        (incl. `PASS F22 knowledge/cisa-when-to-issue-vex.md ids=S057`)
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057
                                                                        → exit 0
python3 corpus/instruments/capture-binding-check.py                     → records=46 bound=46 unbound=0
python3 corpus/instruments/recheck-audit.py --quiet                     → expected=51 missing=0 unexpected=0 exit=0
ls corpus/knowledge/*.md | wc -l                                        → 51
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
                                                                        → exit 0, only W04 S028/S029
```

Junk twin committed and red: `c2-controls/junk-f22-recheck.txt` → `S057:J1..J4 MISMATCH
reason=quote-not-found`, `exit=1`, with positive and isolation controls green in the same transcript.
E5.9 content bindings spot-checked: F22 row names `knowledge/cisa-when-to-issue-vex.md` + `S057`
(corpus/README.md:506); S057 row NF=13, `status mined`, exact URL (SOURCES.md:62); S056/S058/S059
rows `status rejected` with `flip:` tokens (SOURCES.md:63–65); entry 144 lines with the provenance
trio plus substantive body.

**C1 reds — all three fire (my runs, TMPDIR+`--work` under my scratch):**

```
bash corpus/instruments/r39-closure.sh --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a → closed=1/8 exit=1
bash corpus/instruments/r39-closure.sh --export-ref 66703acaaff50529a35be49aa8759d04140720ad → closed=1/8 exit=1  (E2 40-char hash)
bash corpus/instruments/r39-closure.sh                                                       → plain-exit=2
```

Matches the in-flight `final-gates/reds.txt` (base 1/8, r38-head 1/8) byte-for-byte on the closed
lines. J-run measured: `--export-ref 46c66c2…` → `closed=5/8 exit=1`, G2 all-zero (`receipt=0`) —
E4's "7/8" was the clean-window value; post-receipt a J-run additionally reds G8 (E9 head-match:
live HEAD is Y, not J) and G6.

**Report-section inputs — all present:** SCORECARD `## Round 39 result` (L1563) with the
judged-head-by-reference phrase, saturation line and distance block; SHONEN round-39 lines (6, incl.
the R2 correction at L190 and the judged-head phrase at L202); LOG `## Round 39` (L1707);
`corpus/lessons/round-39.md` (84 lines, `grep -c '⟨pending'` → 0); G7 ledger section (`rows=7`,
proposals 1+3, correction — green in my suite run); R4 criteria (`grep -cE 'M38-5|M38-7'
corpus/QUALITY.md` → 1). Suite self-digest `2856a210…` = executing bytes = deliverable bytes
(`ExecSuiteBuild.r39-closure.sh` diff → IDENTICAL), and the suite was committed once (1a139e0) with
an empty diff to Y — no byte drift.

## 3. Findings (attack results, by severity)

### F1 — CRITICAL: the landed all-gates v3 G6 line is not producible by the instrument it pins

Landed line (`final-gates/all-gates.txt`):

```
G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=/fast/scratch/hyaku/kasegi-r39/gates-work,read=ok closed=1
```

`check_g6`'s return (read in full, lines 866–927 of the pinned bytes) has **no tolerated carve-out**:

```bash
[ "$read" = ok ] && [ "$r37" = absent ] && [ "$r38" = absent ] || return 1
if [ "$r39" = absent ] || [ "$r39" = empty ]; then return 0; fi
return 1
```

`r39=present` (any scanned top-level entry under `kasegi-r39` that is not the run's `--work` and not
a clean-chain ancestor of it) forces `return 1` → the runner prints `closed=0`. Empirical
reproduction of the exact landed scenario (dedicated work dir + foreign entries under a scratch
root, `--export-ref Y`, all under my scratch):

```
$ TMPDIR=$S bash corpus/instruments/r39-closure.sh --export-ref 5006097a… \
    --scratch-root $S/fakescratch --work $S/fakescratch/kasegi-r39/gates-work
G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=…/fakescratch/kasegi-r39/gates-work,read=ok closed=0
closed=6/8 exit=1
```

Identical payload shape, **closed=0**. The landed pair (`r39=present` + `closed=1`) therefore also
contradicts the receipt's own summary line `closed=8/8 exit=0` (8/8 requires G6 rc=0, which requires
`r39 ∈ {absent, empty}`).

Provenance, from the overlay diff (`diff wave1/ExecSuiteBuild.overlay/all-gates.txt
final-gates/all-gates.txt`): the landed receipt was assembled from the seat's fixture-run receipt
(`export-ref=f918ec4f…`, run-utc 21:10:00Z, raw `== run ==` header) with **five payload lines
rewritten** — G1 `corrections-outside=1→0`, G3 `added-quotes=1,covered=1→0,0`, G5 `correction=1→2`,
G6 `r39=absent,work=outside,tolerated=none→r39=present,work=inside,tolerated=…/gates-work`,
G7 `rows=4→7` — while keeping the fixture's `closed=1` values. The G1/G3/G5/G7 rewrites are
legitimate re-measurements (they match my real-lane Y-run byte-for-byte); the G6 rewrite kept a
`closed=1` the rewritten payload forbids. ExecSuiteBuild §2.7's claim that the landed receipt would
be "byte-identical to the live run — verified by diff" is false for the landed bytes.

### F2 — HIGH: the frozen C1 verification commands are window-bound and fail in the live lane

E4 asserts unconditionally: `--export-ref Y` → `closed=8/8 exit=0`; `--selftest --export-ref Y` →
`cases=8 failures=0`. Measured during wave 2 (two runs: defaults, and with `--scratch-root`/`--work`
variants):

```
$ TMPDIR=$S bash corpus/instruments/r39-closure.sh --export-ref 5006097a… --work $S/work-y
G8 payload=…,r37-closed=0,r37-exit=1 closed=0
closed=7/8 exit=1
$ TMPDIR=$S bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097a… --work $S/work-selftest
selftest detail=G8 positive=fail rc=1 payload=…,r37-closed=0,r37-exit=1
selftest case=G8 positive=fail mutants=3/3 verdict=fail
selftest cases=8 failures=2          (G6 positive also red — my own work placement, see F6)
```

Mechanism (code read, pinned r37 suite `check_e9`, lines 559–611): E9's limbs are **live** — it runs
`git --no-optional-locks -C "$LANE" status --porcelain` and requires **zero** entries, and requires
live `HEAD == $want` (= the export ref). Direct pinned-r37 run at Y:

```
E9 payload=status-read=ok,status-dirty=6,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
```

The 6 = the untracked wave-2 entries (`final-gates/reds.txt`, `kasegi-r39-falsify.ready{,.dispatched}`,
`wave2-dispatch.json`, `wave2-run.err`, `wave2/`). Consequences:

- **During wave 2** every honest suite run at Y prints `closed=7/8` (G8 red) — the frozen C1.1/C1.2
  commands miss, and a literal reader hits the kill clause "the judged-head export prints
  closed != 8/8".
- **After wave-2 artifacts are committed** (HEAD = Z > Y) the 8/8 becomes unreachable at *every*
  ref: at Y, E9 `head-match=0` (live HEAD is Z); at Z, G2 `diff-clean=0` (`git diff --name-only
  46c66c2 Z` ⊇ the wave-2 files). The suite's own G2 mutant `post-receipt-diff-extra` pins exactly
  this red.
- The green state exists only while `HEAD == Y` **and** the tree has zero porcelain entries — a
  24-second window (Y committed 20:12:12Z; first wave-2 dispatch file 20:12:36Z) or a clean `--lane`
  clone. Wave-1 knew this: ExecPinnedG8Fixture §9 ("A fresh `closed=14/14` needs a clean lane whose
  HEAD is the exported ref") and ExecSuiteBuild §4 (the "green window" table, called "the round's
  R1/M39-1 hazard"). But neither claims.json, E4, the landed receipt nor the SCORECARD section
  states the precondition.

Corroboration: wave-2 sibling `CritBaseControl.md` measured the same signature independently (its
Y-run: `E9 payload=…,status-dirty=6,…,head-match=1,… closed=0`; verdict table: G8 red
"**environment**, see §3 — also red at Y").

### F3 — HIGH: the receipt's run-utc post-dates its own commit and the environment is undisclosed

`all-gates.txt` was committed exactly once, at Y = 20:12:12Z (`git log --format='%cI' -1 5006097` →
`2026-10-26T17:12:12-03:00`), yet records `run-utc=2026-10-26T21:35:00Z` — 83 minutes after its own
commit, by which time the lane carried ≥5 untracked entries (dispatch files 20:12:36–20:18:01Z). A
real-lane run at that moment cannot print the landed G8 green (F2), and no environment prints the
landed G6 pair (F1). Unlike the round-38 receipt (which carried `run-ref=7dd2fcd6…` and a prefixed
raw run header after its own receipt-fix lesson), the landed v3 records neither the CLI ref nor the
deviation lines — the assembly dropped the raw `== run ==` header the overlay receipt carried. The
report therefore cannot bind the 8/8 to a disclosed run environment from the receipt alone.

### F4 — MEDIUM: E5.7's R2-correction counting command misses on LOG.md

```
$ grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:1   LOG.md:0   SCORECARD.md:2   SHONEN.md:1
```

E5.7 requires ≥1 per file at the judged head. LOG.md's correction exists but bulleted
(`- **Correction (round 39):** …` at LOG.md:1704), so the frozen anchored command reads 0. Substance
present, frozen command unsatisfied — the report cannot cite E5.7 as passing without noting this.

### F5 — MEDIUM (readiness): evidence files the report needs are still untracked

`final-gates/reds.txt` (the base/r38-head red transcript; matches my independent runs) and
`wave2-dispatch.json` are untracked. E5.6/G3 bind quoted runs to committed transcripts under
`final-gates/`; G4 requires every tracked `*-dispatch.json` to have a paired results file. Both must
be committed (with a wave-2 results file) before the report's evidence pointers resolve.

### F6 — LOW (spec×suite interaction, recorded for wave-2 suite-run seats)

The seat spec mandates `--work under $S` (seat scratch). `check_g6` tolerates a work dir under
`kasegi-r39` only when the chain from the scanned top-level entry to WORK holds nothing else
(`g6_chain_ok`, lines 543–563) — a seat scratch containing the seat's own files breaks the chain, so
suite runs with spec-compliant work placement print `G6 … tolerated=none … closed=0` (my defaults
run; also ExecSuiteBuild §2.5). The G6-green pattern is a dedicated work dir directly under
`kasegi-r39/` (the L1's `gates-work`) or outside the scratch root. This is noise, not a claim
defect — but wave-2 seats running the suite should not read their own G6 red as a kill.

## 4. What the report must contain to pass contract review (when it lands)

1. Sections in order: Work performed / Landed changes / Before → after measurements / Sources &
   frontier / Trend verdicts / SHONEN (r38 template adds Stale-lane, Tooling).
2. J and Y named with hashes, both ancestors of the lane tip at filing; `git diff --name-only J Y` =
   the receipt only (verified now: holds at 5006097).
3. **The F1–F3 resolution**: either a re-run receipt (v4) produced in a disclosed clean-tree
   HEAD==Y environment with the raw run header/deviation lines kept, or an erratum stating that the
   landed v3's G6/G8 lines came from the fixture/clone environment (ExecSuiteBuild §2.7) and that
   live re-runs during/after wave 2 print 7/8 for the two documented live-state reasons. Absent
   this, the r38-precedent honest framing applies: C1's frozen counting command misses at filing
   time and the operator rules.
4. Numbers cross-checked against the C2 recheck receipts — verified consistent now (§2); registry
   cited as **59** per E1 everywhere (claims.json's 58 is superseded).
5. Evidence pointers resolving: `final-gates/reds.txt` + wave-2 dispatch/results committed (F5).
6. No placeholder text (lesson pending-markers 0; wave-1 placeholder scan receipt on file).
7. E5.7's LOG.md gap either fixed (anchored correction line in the round-39 LOG entry) or disclosed.

## 5. Wave-2 completion state (the dominant readiness gap)

Wave 2 = 37 seats (`wave2-spec.json`); 32 receipts on disk at my final read; dispatch + receipts
still untracked. The report cannot be written until the falsify wave closes and its evidence is
committed. My findings F1–F3 are inputs the L1 needs **before** drafting, since they determine how
the C1 headline is stated.

Report: .ufo/waves/round-39/wave2/RevReportPreflight.md
