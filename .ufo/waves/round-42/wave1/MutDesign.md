# MutDesign — claim->check map mutation test (J1–J13)

Seat: `MutDesign`, kasegi round 42, build wave 1 (fresh-start). Item: for each check
J1–J13 of the frozen C1 predicate, propose the concrete mutant a *weak* check would
pass, and mark which committed round-40/round-41 artifact already demonstrates it.
Axes: depth:verifiability (primary), coverage. Receipt-only item: this file is the
receipt; no other deliverable.

Frozen source read first: `.ufo/waves/round-42/claims.json` (not edited). Routed
queue: `corpus/lessons/round-41-verifier-spotcheck.md` §5. Disk guard green before
the read pass (`/fast/scratch/hyaku` 27% used, 592.6G free). Scratch:
`/fast/scratch/hyaku/kasegi-r42/MutDesign/` (removed before yield). No tools
installed; no git/jj mutation; lane reads only.

For every check the table gives: the weak-check shape, the smallest mutant input
that escapes it, and the committed artifact (with its observed output) that already
demonstrates that exact escape. **Status** is one of:

- **DEMONSTRATED** — a committed r40/r41 artifact shows the mutant accepted (green)
  or the artifact is the live defective state itself.
- **BOUNDED** — the artifact demonstrates the repair boundary (mutant killed once),
  so the weak form is defined by contrast.
- **GAP** — no committed artifact demonstrates this mutant; the replay limb must
  construct it fresh (flagged for the suite builders).

## Map

| J | Family | Weak-check shape | Concrete mutant it passes | Demonstrating artifact | Status |
|---|--------|------------------|---------------------------|------------------------|--------|
| J1 | F-EVID | evidence identifiers collected as a cross-record **union** | one correction's line-set names no evidence id; another record covers it — aggregate `evidence=N/N` still green | `r41/wave2/RevC1Counters.md` finding 2: `selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0`; `r41/wave2/CritC1KillRule.md` (same detail lines); union site r41 suite `check_i1` ~L902–906 | DEMONSTRATED |
| J2 | F-TOKEN | substring/prefix presence test (`closed=10/10` inside `closed=10/100`), or one-sided boundary | `closed=10/100` (prefix `closed=10/10` inside a longer digit run); also `closed=7/80`, `failures=10` as quoted-but-wrong values | `r41/wave2/RevC1Counters.md` finding 1: `mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,...,tally=3/3,mangled=0` (mutant planted by r41 suite ~L1757–1759); r40 `wave2/RevC1Counters.defeats.txt` T2: `closed=7/80`+`failures=10` → `rc=0` green | DEMONSTRATED |
| J3 | F-TABLE | (a) row found by basename mention, cell count unchecked; (b) first cell compared after trim; (c) only the new r42 row checked, table integrity ignored | (a) bare `|` inside a command cell → `cells=11`; (b) `|  r41-closure.sh |` leading-whitespace cell; (c) the CURRENT HEAD table: split r40 block + duplicated `r40-closure.sh` row | `r41/wave2/MutSkillTablePipes.findings.md`: bare pipe `rows=1,cells=11,broken=0,ok=1` and leading whitespace `ok=1` **survived**; blank-line/EOF-dislocation killed (`broken=1,ok=0`). Live HEAD defect = D-r41-3 (verifier §5 item 3; ExecJ3 spec confirms HEAD still carries it) | DEMONSTRATED |
| J4 | F-DECL | (a) validates only listed declarations (subset, not completeness); (b) whole-tail hash without canonicalization/containment | (a) changed path omitted from `declared-blocks.txt` is never visited; (b) declared path = symlink to bytes outside the export (`pwn`) | (a) `r41/wave2/CritDeclarationCoverage.md`: `declared_blocks_check` (r41 suite L1054–1115) iterates declaration records only — coverage weakness documented; probe printed `declared=132,valid=130 closed=0` (aggregate caught it, focused gap open); (b) r40 `wave2/RevC1Counters.defeats.txt` T7: `numstat: 1 0 pwn` → `rc=0 payload=declared=1,valid=1,tail=1,pure=1,paths=1` GREEN; confirmed load-bearing by `r41/wave2/CritI12Necessity.md` | DEMONSTRATED (b); documented gap (a) |
| J5 | F-SCAN | (a) literal single-prefix scan (`kasegi-r40*` only); (b) top-level-only enumeration; (c) fail-open on missing/non-dir root; (d) scans only the configured root's children, never its parent | (a) `Kasegi-R40-stray`, `kasegi_r40-stray`, `kasegi-r39-*` sibling; (b) nested stray under a container; (c) `--scratch-root` = plain file or nonexistent dir; (d) stray in the parent family container the root lives in | (a) `RevC1Counters.defeats.txt` D4: `Kasegi-R40-stray` and `kasegi_r40-stray` → `rc=0 strays=0`; (b) `r40/wave2/RevC1Sandbox.scratch-nested-blindspot-green.txt` ends `closed=10/10 exit=0` (+ `CritKillRule.md` F1); (c) `RevC1Sandbox.scratch-file-root-green.txt` `closed=10/10 exit=0` (+ F6); (d) `r41/wave2/MutScratchTiming.md`: `/tmp/kasegi_r41_outside_probe` live, `I6 strays=0` unchanged — survived | DEMONSTRATED |
| J6 | F-BIND | binding = record↔row URL match + capture-file orphan logic only; no path existence, sha equality, or url-cell byte equality | (a) record `path` names an absent capture; (b) `url` case-mutated (`rfc9116`→`RFC/rfc9116`); (c) `url` + trailing slash; (d) mined registry row with no capture/manifest record at all | `r41/wave2/MutBindingExistence.md`: all three record mutations → `records=63 bound=63 unbound=0` exit 0 (**survived**; the missing-path red at source-recheck was a `stem-mismatch` artifact, not an existence check); `r41/wave2/MutAuditUnexpected.md`: unreferenced `S999` mined row → `records=63 bound=63 unbound=0` silent | DEMONSTRATED |
| J7 | F-FLIP | evaluates/counts only `admitted` rows — a flipped row exits the denominator silently; or accepts `entries=N pass=N` without per-row `PASS F<n>` | F24 status `admitted`→`explored`: `entries=26 pass=26 exit=0`; also `queued`/any non-admitted status, or an admitted row missing its PASS line | `r41/wave2/MutC2Chain.md` mutation A **SURVIVED** (`26/26 exit 0`, F24 vanished); killed bound: `r41/wave2/MutFrontierParser.md` decoy `| F999 | ... admitted |` → `FAIL F999 ... problems=missing-entry` exit 1 | DEMONSTRATED (survivor + bound) |
| J8 | F-RCPT | (a) field-wise receipt grading without byte `cmp`; (b) recorded payload values trusted, not re-derived; (c) no ancestry/diff-clean tree binding; (d) accepts a header+tally receipt with no per-check lines; (e) no run-utc = ref-committer check | (a) payload lines reordered, every field green; (b) `J<n> payload=` rewritten to false values; (c) receipt of a foreign/nonexistent ref with coherent fields; (d) summary-only receipt; (e) `run-utc` future-dated | (a) `r40/wave2/MutH6H10.md` D1 **SURVIVOR**: reorder fixture `MutH6H10.h7-reorder-receipt.txt` → mutant `rc=0` vs pristine `rc=1`, `cmp` the sole guard; (b–e) `r40/wave2/CritReceiptForge.md` variants a/c1/c2/d/h7line all REJECTED (payload-match, ancestor/diff-clean, run-lines, not-future); `r41/wave2/CritDigestSelftest.md` — `recorded-payload-contradicts` and `selftest-lines-reordered` rejected, but digest-after-run and duplicate-case limbs untested | DEMONSTRATED (a survivor + b–e bounds); GAP for digest/duplicate-case |
| J9 | negative controls | (a) `exit!=0` or `closed<13/13` accepted for any bad ref — no distinct `ref-not-found`; (b) acceptance predicate `tally<13 && exit==1` with no per-limb redness; (c) plain-run refusal untested | (a) unresolvable ref printed as an ordinary vacuous `closed=0/13 exit=1` (class conflation); (b) negative ref whose nested run is a leaf-capped green window (`closed=12/13 exit=1` with tree-dependent limbs green); (c) suite that exits 2 but still executes | (a) `r41/wave2/MutAncestorGuard.md`: nonexistent ref → `I2 payload=ref-not-found,ref=0000...0001 closed=0`, `closed=0/12 exit=1` (distinct path vs `ancestor=0` for a valid non-ancestor); (b) `r40/wave2/MutH6H10.md` D2 **SURVIVOR**: pristine H8 accepted `base=7/10` on a green-window ref; r41 `neg_accept` (L1339–1347) now requires `i1=i2=i7=0` — plus `R41_NEG_WEAK` env flip `MutSuite.findings.txt` probe 3 | DEMONSTRATED (a design, b survivor); GAP for (c) |
| J10 | selftest isolation | counts `cases=N,isolated=N` from a payload-match walk over a synthetic receipt (r41 `check_i9` L1308–1324 proves `isolated=` measures nothing about private copies) | cases share one fixture dir — a later case reads an earlier case's mutated copy; a case leaks files outside its private dir; `isolated=13` still prints | nearest class evidence only: `r40/wave2/MutH6H10.md` M-inert (one comment byte cascades H1→H5→H7 positives — shared-state coupling); `r41/wave2/MutSuite.findings.txt` (I6 positive depends on host scratch layout — environment bleed); `r40/wave2/SentinelFinal.selftest-scratch-root-intree.txt` (green selftest with `--scratch-root .` in-tree) | GAP — no committed isolation-escape artifact; limb is new |
| J11 | F-CORR | presence/count only (`grep -c 'Correction (round' >= 1` per file); or naive global uniqueness that would also red the honest dedup-erratum repair | the CURRENT HEAD state: four `Correction (round 41)` lines duplicated verbatim | live at HEAD — verified this pass: `SCORECARD.md` L1602–1605 byte-identical to L1607–1610 (awk equality: 4× `IDENTICAL`); D-r41-1 (verifier §5 item 1); `r41/wave2/RevCorrectionsFinal.md` counted SCORECARD `grep -c`=8 (4 unique ×2) with a `>=1` predicate blind to the dup | DEMONSTRATED (live committed state) |
| J12 | no-deletions + density | `diff --name-status` counting only `D` rows (misses `R`/delete+add pairs); density.py compared by line count or worktree file instead of export blob vs base sha | deleted corpus file recommitted (history hides it from a worktree check); rename `R###` row; density.py modified with identical `wc -l` | guards proven load-bearing: `r40/wave2/MutH6H10.md` M-H10a (`deleted` guard dropped → `tracked-path-deleted` fixture `rejected=0`); `r41/wave2/CritI12Necessity.md` r40-head run `deleted=2` fires on real deletions; r41 I12 `density=1` confirms sha limb vs base `ee803726…f54710` | BOUNDED (guard evidence); GAP for `R`-status and wc-l escapes |
| J13 | quiescence | (a) scans a root other than the suite's own `--scratch-root` (host-global `$HYAKU_SCRATCH`, lane worktree); (b) `git status` on the lane only, not on the exported-ref clone in scratch; (c) quiescence checked mid-run, not at receipt time | (a) leftover `kasegi-r4x` inside the suite's own root while the checked root is clean (and converse: truth dirty, audited root clean); (b) uncommitted change inside the scratch clone with a clean lane; (c) stray arriving between scan and receipt | (a) `RevC1Counters.defeats.txt` T11: `strays=0` audited at an empty root while the dirty root held `kasegi-r40-stray` — produced green re-run, unfalsifiable post-hoc; (b) `r40/wave2/CritKillRule.md` F8 (skip-worktree status blindness) + F5 ancestor-prefix tolerance; (c) `r40/wave2/LabDeterminismY.two-strays.txt` `strays=2 → closed=7/10`, `LabDeterminismY.work-outside-scratch.txt` `closed=7/10` | DEMONSTRATED |

## Cross-cutting mutant on the repair itself

Every J1–J7 check carries a committed REPLAY limb (`replay_defeat`). The weak form
of *that*: a replay that verifies the artifact file exists (greps the wave2 path)
instead of re-executing the reconstructed defeat state — every replay "passes" while
the check stays weak. The frozen kill rule names this directly ("the committed
replay limb of any J1-J7 check is absent or skipped — a defeat that is not replayed
is not repaired"). No committed artifact demonstrates it (the mechanism is new);
catalog: ExecReplayHarness spec defeat list = `r41/wave2/{CritC1KillRule,RevC1Counters,
MutSkillTablePipes,CritDeclarationCoverage,MutScratchTiming,CritI12Necessity,
CritDigestSelftest,CritReceiptBootstrap,MutSuite.findings}` + `r40/wave2/
{RevC1Counters.defeats.txt,CritKillRule.md,CritKillRule.h6-escapes.sh,MutH6H10.md}`.

## Two repair-shape warnings (weak at the boundary, not the center)

- **J11:** strict "each body once, ever" would red the honest r42 repair — the
  dedup erratum keeps history append-only (ExecJ11Corr spec: count==1 per distinct
  normalized body *plus* an appended `Correction-dedup (round 42)` marker naming the
  dup). The mutant to reject is a verbatim duplicate *without* the marker; a checker
  that reds the marked-dedup state is a false-positive generator.
- **J5:** the outside-root limb per ExecJ5Scan spec materializes a fixture parent
  under `--work`; a check that reads the real host parent (`/fast/scratch/hyaku`)
  is host-global state and fails J13's own boundary — the scan must evaluate the
  materialized tree only.

## Evidence commands run this pass

- `bash scripts/hyaku/disk-guard.sh status` → green: `/fast/scratch/hyaku` 27%,
  592.6G free (full output retained during session).
- `read .ufo/waves/round-42/claims.json` (lines 27–28, 48–49 raw for full
  predicate/kill text).
- `grep -n 'Correction (round 41)' SCORECARD.md` → hits at L1602–1605 and
  L1607–1610; `awk` equality pass → all four line pairs `IDENTICAL` (live J11
  mutant at HEAD).
- `grep -n 'ref-not-found\|NEG_WEAK' corpus/instruments/r41-closure.sh` →
  `print_ref_not_found` L376–402, `neg_accept` L1339–1347, `R41_NEG_WEAK` env
  backdoor L1339/1880–1883.
- `sed -n '1308,1326p' corpus/instruments/r41-closure.sh` → `check_i9` derives
  `isolated=` from `payload_match_ids` only (J10 weak-shape reference).
- Read in full: r41 wave2 `RevC1Counters.md`, `CritC1KillRule.md`,
  `MutSkillTablePipes.findings.md`, `MutScratchTiming.md`,
  `CritDeclarationCoverage.md`, `MutBindingExistence.md`, `MutC2Chain.md`,
  `MutFrontierParser.md`, `MutSuite.findings.txt`, `CritReceiptBootstrap.md`,
  `CritDigestSelftest.md`, `MutExportRefReemit.md`, `MutAncestorGuard.md`,
  `MutAuditUnexpected.md`, `RevCorrectionsFinal.md`, `CritI12Necessity.md`;
  r40 wave2 `RevC1Counters.defeats.txt`, `CritReceiptForge.md`, `MutH6H10.md`,
  `SentinelFinal.selftest-scratch-root-intree.txt`, `LabDeterminismY.two-strays.txt`,
  `RevC1Sandbox.scratch-{nested-blindspot,file-root}-green.txt`,
  `LabDeterminismY.work-outside-scratch.txt`, `LabScratchClean.md`;
  `corpus/lessons/round-41-verifier-spotcheck.md` §5; `wave1-spec.json` item texts
  for the J-check contracts.

## Restoration / conduct

No suite, lane, fleet, or source-tree bytes written; no mutating git/jj command.
All quoted outputs are verbatim from the cited committed artifacts. Scratch
`/fast/scratch/hyaku/kasegi-r42/MutDesign/` removed before yield. Tools installed:
none. Network: none.

Report: .ufo/waves/round-42/wave1/MutDesign.md
