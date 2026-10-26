# LabExportClean — round 40, falsify wave 2 (isolation probe of `r40-closure.sh`, H6 + work-dir)

Seat: `LabExportClean` (lab, leaf). Attacks: claim C1's suite `corpus/instruments/r40-closure.sh`,
limb **H6** (scratch-sibling scan) and the `--work` export isolation, via a dirty `--scratch-root`
and a pre-populated `--work`. No lane/fleet file was edited; only read-only git on the lane.

Verification ref. The true Y (J + receipt) is not yet committed in the lane (J = HEAD
`3074c7679d6f527ec3930d7748ccce1dbae4a58a`; the receipt `final-gates/all-gates.txt` is untracked). I built a
**fixture clone** (`git clone` of the lane into scratch, then one commit adding that exact receipt file, in
the clone after asserting its toplevel): Y' with `git diff --name-only J Y'` = the receipt only, tree
identical to Y. The suite bytes run were `bdbd18a3…7f1e` (equals the committed
`corpus/instruments/r40-closure.sh` at J and the receipt's `suite-sha256`). Y' hash differs from the true Y
only by the commit instant; the transcript names J and is independent of Y's hash.

Deliverables (beside this receipt):
- `LabExportClean.transcripts.txt` — 799 lines, sha256 `7c1a96eb…bbd`, verbatim stdout/stderr/rc of 23 scenario runs + the 8 H6 mutant selftests + live-behaviour of the surviving mutants .
- `LabExportClean.isolation-replay.sh` — byte-exact replay of the core scenarios (A,B,C,D,F,H,I + dirty selftest); I re-ran it end-to-end: same H6/closed lines as the transcripts, `A==C` byte-identical.

## 1. H6 semantics as implemented (read from the committed bytes, lines 760-797)

Scans only top-level entries of `--scratch-root` by **name** `kasegi-r39*|kasegi-r40*` (no dot-prefix, `find -mindepth 1 -maxdepth 1`); an entry whose realpath is `--work`'s realpath or an ancestor of it
is skipped (the whole family dir holding `--work` is "the caller's own space"); every other match counts
as a stray (empty included); `cd` into an entry failing, or root-unreadable, is `read=fail` (red).

## 2. Isolation matrix (Y', `--lane <clone> --export-ref Y'`, sandbox root + separate work)

| id | scratch-root state | --work state | H6 line | tally | expectation | result |
|---|---|---|---|---|---|---|
| A | clean (`kasegi-r41-ignored/`, `gates-work/` present) | clean, outside root | `strays=0,read=ok` | 10/10 exit 0 | green | reproduced |
| B | `kasegi-r40-stray/` | clean, outside | `strays=1,read=ok` | **7/10** exit 1 | red (H6) | red, **but 3 lines red, not 1** (§3.1) |
| C | clean | pre-populated: `export/` (forged suite+SCORECARD, symlink to lane), `mut/`, `neg-base/`, `neg-r39/`, `h5/`, stale `payloads.tsv pay.tsv h5-source.txt h7-source.txt h7row.tsv selftest-report.txt` | `strays=0` | 10/10 exit 0 | green | reproduced; **stdout byte-identical to A** (`cmp`) |
| D | `kasegi-r40-stray/` | pre-populated as C | `strays=1` | 7/10 exit 1 | red | same as B (stale work did not change anything) |
| E | `kasegi-r40-seat/work` (work inside family) | that | `strays=0` | 10/10 | green | reproduced, stdout == A |
| F | E + `kasegi-r40-seat/other-seat/leftover.txt` | inside family | `strays=0` | **10/10** exit 0 | NOT green by kill rule | **DEFECT D1** |
| G | E + sibling `kasegi-r40-stray/` | inside family | `strays=1` | 7/10 | red | reproduced |
| H | `.kasegi-r40-seat/f` (dot-dir) | outside | `strays=0` | **10/10** | red per wave-1 ref limb | **DEFECT D2** |
| I | `kasegi-r40-file` (regular file) | outside | `strays=0,read=fail` | 7/10 | red | red (payload says read=fail, not a stray count) |
| J | `kasegi-r40-seat` → symlink to foreign dir | outside | `strays=1` | 7/10 | red | reproduced |
| K | `kasegi-r39-link` → symlink to the work dir | outside | `strays=0` | 10/10 | green (tolerated by realpath) | reproduced |
| L | `kasegi-r40-dangling` → dangling symlink | outside | `strays=0,read=fail` | 7/10 | red | reproduced |

Selftest (`--selftest --export-ref Y'`): ST1 clean root → `selftest cases=10 failures=0`, all ten graded lines
pass (reproduced); ST3 pre-populated work (incl. forged `selftest-report.txt`, `forge-9-cases.txt`) →
`cases=10 failures=0` (stale work does not leak, reproduced); ST4 work inside a family dir with a sibling →
`failures=0`; **ST2 dirty root (stray dir) → `selftest cases=10 failures=2`** with `case=H5 positive=fail`, `case=H7 positive=fail`, **`case=H6 positive=pass mutants=4/4`**.

Default (live) root `/fast/scratch/hyaku`: D1 work under `kasegi-r40/` → 10/10 exit 0 (22 live peer seat
dirs sat inside `kasegi-r40/` at that moment); D2 work in `/var/tmp` → `strays=1` 7/10 exit 1 (the live
`kasegi-r40/` family dir counts); D3 `--selftest` → `cases=10 failures=0`.
Counting/negative controls re-run (clean sandbox root): `D4` plain run exit 2 with refusal text;
`D5` base a7af2ce → `closed=3/10 exit=1`; `D6` r39 head 8371e7a → `closed=2/10 exit=1`;
`D7` at J (no receipt) → `closed=9/10 exit=1` (H7 red — the documented green window is Y only).
All as the frozen counting commands require (**green re-run, reproduced**).

## 3. Interpretation against H6 semantics, and defects

**Verdict on the assignment as stated.** The suite stays green with a stray in the *wrong* place and a
pre-populated `export/` in `--work` (C, E, K; ST3), and reds when the stray is in the scanned root (B, D, G,
J; dirty selftest ST2). "The stray in scope must not count" holds for strays that are inside the one
family dir holding `--work` (F) — that is the implemented H6, but it is weaker than the frozen kill rule
(see D1). No red was produced by `--work` contents, ever.

**3.1 DEFECT D3 (attribution/cascade, low):** one stray dir turns **three** check lines red (H5, H6, H7),
tally 7/10, not the 9/10 the H6 limb implies. Cause: H5 recomputes `control=n/8` by comparing the eight
recorded payloads (incl. H6, H8) with the live ones, H7 `payload-match=6` (of 9), and H8's nested leaf run
inherits the dirty root (`base=2/10,r39=1/10` instead of `3/10,2/10`), so the H8 payload also drifts from the
receipt. Observed in B/D/G/I/J/L and selftest ST2 (`H5 positive=fail`, `H7 positive=fail`, while
`H6 positive=pass`). Effect: a scratch-hygiene fault is reported as "forgery rejection" (H5) and "receipt
transcript" (H7) failures; and the selftest H6 case never exercises the live root (its positive limb is the
internal `own-work-dir` control), so a dirty live root is invisible to H6's own graded line and shows up as
H5/H7 FAIL. Documented as "H6 is LIVE", but the tally and attribution are not.

**3.2 DEFECT D1 (kill-rule gap, medium):** scenario F (and the live D1): when `--work` sits under a family
directory, every sibling/nested entry in that directory is exempt (the suite's own header: "entries nested
inside the one family directory that contains --work are the caller's own space and are not audited").
The frozen kill rule names "any leftover kasegi-r39*/r40 scratch entry at filing other than the passed
--work dir". At the live default root `kasegi-r40/` holds every seat's scratch; a counting run with
`--work` under it is `closed=10/10` with 22 foreign dirs present, whereas a run with `--work` outside is
red (D2). The wave-1 reference limb (`ExecH6ScratchFixtures`, `work-chain-contaminated expect=red`) required
a clean chain and was not adopted. Fix direction: tolerate only entries on the work-chain whose every level
contains exactly the next component.

**3.3 DEFECT D2 (name-family, low):** `.kasegi-r40-seat/` (dot-prefixed family dir) is not scanned (H); the
reference limb strips one leading dot. A dotted leftover is silently ignored.

**3.4 Note (not a defect):** regular-file and dangling-symlink strays red as `read=fail` with `strays=0`
(I, L); correct verdict, misleading payload.

## 4. Mutation test of the H6 limb (8 mutants, selftest run on a mutated copy; baseline failures=3 from H1/H7 digest drift of the copy)

| mutant | change | selftest `case=H6` | killed? |
|---|---|---|---|
| M1 | exact names `kasegi-r39|kasegi-r40` | mutants=2/4 verdict=fail | killed |
| M3 | stray counter removed | 1/4 fail | killed |
| M4 | empty family entries exempt | 2/4 fail | killed |
| M8 | work-anywhere-inside-root tolerated | 1/4 fail | killed |
| M2 | unreadable entry (`cd` fail) ignored | 4/4 pass | **survived** |
| M5 | `find -type d` only | 4/4 pass | **survived** |
| M9 | `read=fail` no longer reds | 4/4 pass | **survived** |
| M10 | `find` failure ignored | 4/4 pass | **survived** |

Survivors are real behaviour changes, proven on plain runs (transcript tail): M5 on fixture I (file stray) →
`H6 strays=0,read=ok closed=1` (original red); M2 on I → closed=1; M9 on I → `read=fail closed=1`;
M10 on a root with mode 0311 (searchable, not listable) → `read=ok closed=1` vs original `read=fail closed=0`.
**DEFECT D4 (selftest coverage, medium):** the committed H6 mutants are four directory/empty-root fixtures
(empty family dir, `kasegi-r39-stray`, `kasegi-r40-stray`, root mode 000); no fixture covers a non-directory
entry, a dangling symlink, an unreadable entry, a listable-failure root (0311) or the dot-prefixed name.

## 5. What reproduced / what contradicted

- Reproduced: all five counting commands at J/Y'-equivalent (10/10 at Y' with clean root; 3/10 base; 2/10
  r39 head; plain run exit 2; selftest cases=10 failures=0 with graded lines); stale `--work` content never
  changes the transcript; own `--work`/symlink-to-work never reds; stray in scanned root reds.
- Contradicted/defects: D1 kill-rule gap (F, D1), D2 dot-dir, D3 cascade 7/10 + H5/H7 attribution,
  D4 survivors M2/M5/M9/M10.

## 6. Tooling / hygiene
No tool installed; no network; no pacman. Read-only git only on the lane (`clone`, `rev-parse`, `diff --name-only`); the
only commit made was inside the scratch clone after asserting its toplevel. All runs used `--scratch-root` sandboxes
under my scratch dir except D1-D3 (default live root, read-only scan; strays I created lived only inside my own
scratch dir, never at the host root). `/var/tmp/LabExportClean-dw` was removed. Scratch
`/fast/scratch/hyaku/kasegi-r40/LabExportClean` (and the replay scratch) removed at yield; disk-guard green at start
(`/fast/scratch/hyaku` 24%, 616.7G free).

## 7. Files
- `.ufo/waves/round-40/wave2/LabExportClean.md` (this)
- `.ufo/waves/round-40/wave2/LabExportClean.transcripts.txt`
- `.ufo/waves/round-40/wave2/LabExportClean.isolation-replay.sh` (sha256 `67127f2c…41b0`)
