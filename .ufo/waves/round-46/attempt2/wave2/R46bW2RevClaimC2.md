# R46bW2RevClaimC2 — round 46 (attempt 2) wave 2 — C2 verdict attack

VERDICT: HOLDS

Seat: `R46bW2RevClaimC2` (reviewer, leaf lane — no delegation). Attacked the C2 verdict on its five
named points. All five verify at the landed tree; the do-nothing controls discriminate; the claim
was not narrowed post-freeze. Findings F1–F5 below are defects in supporting artifacts discovered
while attacking (F1 is in the C2 support chain and must be fixed before the round's battery items
can run); none falsifies a C2 after-value.

Trees (exported read-only via `git archive` to `$HYAKU_SCRATCH/kasegi-r46/R46bW2RevClaimC2/`):

- freeze `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` → `freeze/`
- live lane tip / wave-1 integration `96379ae26ef9443097b860ddb33ef924b2cd5b5a` → `live/`
- base `04af9bc92229232ea5cce8b32bfe59dd969eb26d` → `base/`
- pure2 attempt-1 pure export `/fast/scratch/hyaku/kasegi-r46/L1/pure2` (used as `--pure`, 27 rows/64 entries, pre-round)

## 1. The five named attacks

### 1.1 Frontier row admits F29 with status third-cell — HOLDS

Command: `grep -nE '^\| F29 \|' live/corpus/README.md` (live tip export)

Output (line 691): `| F29 | GitHub repository security advisories, maintainer-side lifecycle: … | admitted |
`corpus/knowledge/github-repository-security-advisories.md` | S074 | …`

Cell-exact parse (`row.split('|')`): 6 cells; cell 3 (status) = `admitted`; cell 5 (sources) = `S074`
only — no double-counted source. Counts: `grep -cE '^\| F[0-9]+ \|' live/corpus/README.md` → `29`.

### 1.2 Entry cites five frozen cores inside located live spans — HOLDS (each re-located by this seat)

The gate's frozen cores (`corpus/instruments/r46-f29-gate.py` CORES): privately discuss-and-fix /
temporary private fork / authorized-to-assign-CVE / reviews-within-72-hours / fix-version-before-publishing.

(a) In the snapshot, my own grep (`grep -in -e <core> … S074.txt`):
- line 10 `Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.`
- line 13 `Privately collaborate to fix the vulnerability in a temporary private fork.`
- line 24 `GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.`
- line 25 `GitHub usually reviews the request within 72 hours.`
- line 38 `Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory.`

Each matches the entry's own citation (`S074.txt:10/13/24/25/38`, verified in the entry text at
lines 14/19/21/21/20 and in the G-table).

(b) On the live page, re-fetched by this seat 2026-10-29:
`curl -sS -L 'https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories'`
→ `HTTP 200 final=…repository-security-advisories bytes=582877` (manifest records bytes 582877).
Whitespace/markup-flattened text search: all five cores OK, all nine manifest quotes (Q1–Q9) OK,
and all 42 snapshot lines verify verbatim in the live text (0 missing under the flattened
comparison). The capture is faithful to today's page.

### 1.3 Census exits 0 — HOLDS

Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file live/corpus/SOURCES.md`
Output: three `W04` lines (S028, S029, S072 duplicate-url warnings) then
`file ok …/live/corpus/SOURCES.md`; exit code `0`. Identical shape to the frozen before-receipt
`controls/sources-census-before.txt` (three W04s + ok line). Gate H7 reads `census-rc=0 ok-line=1`.

### 1.4 After-values hold — HOLDS

| after-value | command | result |
|---|---|---|
| gate 7/7 | `python3 live/corpus/instruments/r46-f29-gate.py --root live` | `f29-gate fixed=7/7 exit=0`, H1–H7 all pass=1 (H5: spans=45 located=45 failed=0 cores=5/5) |
| frontier rows 29 | `python3 corpus/instruments/r44-frontier-count.py --root live --expect 29` | `frontier rows=29 admitted=29`, rc=0 |
| knowledge 66 | `find corpus/knowledge -maxdepth 1 -name '*.md' \| wc -l` | `66` |
| SOURCES ≥74 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `74` (S074 row present, tier A, mined, sha256 1296528d…) |
| absence sweep 2→4 | `grep -rliE 'repository securit. advisor\|GHSA' …` | 4 files: F28 entry, new F29 entry, README.md, SOURCES.md |
| snapshot pinned | `sha256sum S074.txt` / `wc -l` | `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, `42` lines — both match the claim |
| manifest pinned | `sha256sum manifest.json` | `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f` — matches freeze.txt |
| 9 quotes OK | `python3 corpus/instruments/source-recheck.py --manifest … --source S074` | `sha256 OK` + `Q1..Q9 OK` each `occurrences=1 anchor=…-ok`, rc=0 (independently re-confirmed by my own line scan: each quote on its declared anchor line) |
| capture binding | `python3 corpus/instruments/capture-binding-check.py --root live` | `records=61 bound=61 unbound=0`, rc=0 |

Before-values reproduce at the base export: gate `f29-gate fixed=1/7 exit=1` (matches
`controls/f29-gate-at-base.txt`); 28 rows / 65 entries / 73 SOURCES rows; absence sweep 2 files
(F28 entry + SOURCES.md S068 context). At the freeze tree the gate reads `fixed=2/7 exit=1`
(H4+H7 green), matching `freeze_tree_reading`.

### 1.5 Target not narrowed post-freeze — HOLDS

`git diff fe0f56b 96379ae -- .ufo/waves/round-46/attempt2/claims.json` → empty; blob identical at
both revs (`1cf17e21…`); `git show 96379ae:…claims.json | sha256sum` →
`ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0`, equal to the sha declared in
freeze.txt. No claim sentence, target, or kill rule edited after the freeze.

## 2. Do-nothing / defect controls (discrimination)

- base export: `fixed=1/7 exit=1` (H7 only) — not 7/7.
- freeze tree: `fixed=2/7 exit=1` — not 7/7.
- junk-entry tree (live corpus with the entry replaced by marker filler):
  `fixed=4/7 exit=1` (H2 sections=0/4, H5 cores=0/5, H6 entry-bytes red) — not 7/7.
- fabricated-quote tree (entry quotes rewritten to text the snapshot does not hold; citations kept):
  `fixed=6/7 exit=1` (H5 spans=45 located=40 failed=5 cores=4/5) — not 7/7.
- census before/after both exit 0 with the same three W04s (no new rows break it).

No control grades 7/7; a tree that broke the quotes or the entry structure reads red.

## 3. Findings (artifacts attacked; exact commands and outputs)

### F1 — HIGH — `corpus/instruments/r46-selftest-f29.py` fails at baseline on the landed tree

The C2 after-text names this selftest as the carrier of the R50 receipt ("the R50 pre-freeze mutant
receipt … carried into the f29 selftest the wave builds"), and the R50 receipt's frozen duty makes
the selftest + `r46-mutbat.py --counter f29` the graders of the 9 disclosed mutants.

Command: `python3 corpus/instruments/r46-selftest-f29.py` (live lane worktree, HEAD 96379ae; same on the tip export)
Output: `note provenance f29-fixture.py sha256=52ea… matches` then
`selftest: lane README carries 29 frontier rows, expected 28`, exit 1.
Root cause: the tree builder asserts `len(frows) == 28` against the lane README
(`r46-selftest-f29.py:187-188`); the wave-1 integration commit added the F29 README row (29 rows)
in the same commit that shipped the selftest, so the shipped selftest can never pass on the tree it
ships in.
Consequence: `python3 corpus/instruments/r46-mutbat.py --root . --pure … --counter f29 --jobs 8`
prints `mutbat counter=f29 BASELINE-DIRTY baseline_failures=-1` (rc=1) — the f29 battery mode
cannot grade any of the 21 R50 mutants at the landed tree.
Control: with `--lane <freeze export>` (28 rows) the same selftest runs
`selftest cases=30 failures=0` rc=0 — the cases are sound; only the hard-coded row count is stale.
Not a C2 after-value falsification (the gate itself reads 7/7 and all content measures hold), but a
broken instrument in the claim's named support chain; blocks the wave-2 battery items that must
reconcile the 21 mutants against the R50 receipt. Fix is a one-line re-derivation (expect 29, or
build the synthetic README from the base export).

### F2 — HIGH (C1 chain, corroborating) — `corpus/instruments/r46-counters-selftest-c2.py` crashes at import

Command: `python3 corpus/instruments/r46-counters-selftest-c2.py --pure .` (any args; module-level fault)
Output: `File "…/r46-counters-selftest-c2.py", line 68, in <module>  EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}` /
`NameError: name 'C1_ENTRIES' is not defined`, exit 1.
Root cause: line 68 uses `C1_ENTRIES`; line 69 defines it. Order-of-definition bug landed in the
wave-1 extension. Consequence: the extended c2 baseline (147 cases, failures=0) that the C1 after
claims is ungradeable, and `r46-mutbat.py --counter c2` prints
`mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1` (reproduced with the correct pure2 export).
This is the C1 seat's primary territory; reported here because the round directive requires
re-running the selftests and battery rather than trusting them. (The c1 twin is clean: with
`--pure /fast/scratch/hyaku/kasegi-r46/L1/pure2`, `r46-counters-selftest-c1.py` prints
`selftest cases=83 failures=0`, rc=0.)

### F3 — MEDIUM — `controls/final-battery.txt` (untracked, worktree) is internally inconsistent and truncated

The file records the c2 NameError traceback and then `exit=0` on the next line — impossible for a
direct `cmd; echo "exit=$?"` capture after a python crash — and ends mid-file at `== battery c1:`.
It sits in the controls directory where receipts live, but it is not committed, not named by the
claims, and not trustworthy as a measurement. Quote:
```
== selftest c2 (extended+ledger):
                     ^^^^^^^^^^
NameError: name 'C1_ENTRIES' is not defined
exit=0
== battery c1:
```
(ends there). The committed `controls/final-measure.sh` does not produce this format, so the file's
provenance is unclear. Request the L1 remove or replace it with a complete honest receipt.

### F4 — LOW (pre-disclosed) — the claims' `control` pointer dangles

`claims.json` (both claims) names `.ufo/waves/round-46/attempt2/controls/freeze-controls.txt`;
that path does not exist in the tree or the worktree. Wave-1 reviewers already flagged it
(`wave1/R46bCritFreeze.md` finding 6, `wave1/R46bScribeLog.md`); the actual freeze-controls receipt
landed at `wave1/R46bExecControls.draft/freeze-controls.txt` (`checks: 13 failed: 0`). This seat
re-derived every control value independently (§1.4, §2), so the substance stands; the pointer
itself is still unlogged in `counter-errata.md` (E1–E4 cover instruments only).

### F5 — LOW — the freeze-era `controls/f29-fixture.py` cannot build trees from the live lane

`python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive --dir … --lane <live>`
fails `AssertionError: 29` at `assert len(frows) == 28` — same 28-row assumption as F1, one layer
down. The R50 pre-freeze fixtures were correct at freeze time; wave-2 fixture/selftest variants
need the 29-row form. (My junk/fabricated controls in §2 were therefore derived from the live
corpus directly.)

## 4. Limitations

- The c1 mutation battery at the tip (`--root . --pure pure2 --counter c1 --jobs 8`) did not print
  a summary within 20 minutes of wall time on this host (load ~165 at last check); interrupted at
  my 1200 s window with `error: interrupted`. It is C1-chain evidence, outside this seat's five
  points; the c1 selftest baseline itself passes 83/0 (§F2). A longer re-run was left outstanding
  at report time.
- Live-page check used one fresh curl fetch (HTTP 200, 582877 bytes — byte count equal to the
  manifest's raw size); quote/line verification was whitespace/markup-normalized. CDN caching
  could in principle serve stale content, but the snapshot lines match the fetched page exactly.
- The junk/fabricated controls were built by mutating the live corpus in scratch (the committed
  fixture is frozen at 28 rows, see F5); both grade < 7/7 as the kill rule requires.
- No git/jj/index mutation performed; the lane worktree was only read (`git archive`, `git show`,
  `git diff`). Scratch removed on exit.
