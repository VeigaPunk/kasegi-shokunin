# CritDesignReview — round-39 C1 design falsification (leaf)

Seat `CritDesignReview` (critic, leaf; no subagents). Item: falsify the frozen r39 C1 suite spec check by check —
for each of G1–G8 give a minimal state that should be RED but a naive limb accepts, a state that should be GREEN
but a naive/strict limb rejects, and the discriminating requirements the implementation MUST carry; feed
`ExecSuiteBuild`'s verification and the wave-2 attack. Axis: depth:verifiability. The suite does not exist yet
(`c1-controls/before.txt`: absent), so this is a spec/design review plus executable fixtures of the *limbs*, not a
run of `r39-closure.sh`.

Deliverable: `.ufo/waves/round-39/wave1/CritDesignReview.design.md` — 350 lines, sha256
`763271fba2561a1086e100229052747ce4dbe6151ab48a3e5301e58261a18805` (measured after the final edit).
Receipt only for everything below.

## Inputs (read-only)

- `.ufo/waves/round-39/claims.json` sha256 `e427ab6a6ecec4b1f49ed5eed95860c468e0982af331a3a1ba135649d27e051c`
  (freeze `dcd3170`), full C1 predicate (G1–G8) read via `python3 -c json`.
- `corpus/lessons/round-38-verifier-spotcheck.md` §5 (R1–R5), `corpus/lessons/round-38.md` §Instrument attack
  findings, `corpus/instruments/r38-closure.sh` (1473 lines) and `r37-closure.sh` (1558 lines) in full for the
  limbs being tightened; `.ufo/waves/round-38/final-gates/all-gates.txt` at the r38 tip `f06148c6`.
- `.ufo/waves/round-39/claims-erratum-1.md` (E1 registry 59; E2 r38 head full hash), `c1-controls/before.txt`,
  `.ufo/waves/round-39/wave1` sibling deliverables (front-door appends, R2 corrections, ledger append).
- Peer `CritFreezeAudit.md` (spec-level A1–A4). My P0.1 confirms A1 with the committed r38 receipt bytes; the
  per-G table is the new material and is what ExecSuiteBuild/wave-2 should consume. `M39-1` (mistakes draft)
  already records the r38 unsatisfiable predicate; P0.1 records that the *r39* rule repeats it verbatim.
- Tooling: none installed; `pacman` never run. Network fetches: none (0 requests). Scratch:
  `/fast/scratch/hyaku/kasegi-r39/CritDesignReview/` (removed before yield; only wave receipt/design remain).
  Fixtures were built under scratch with `git init` and asserted `rev-parse --show-toplevel == fixture`; the lane
  was never mutated (read-only `git diff/log/show/cat-file/rev-parse/merge-base` only).

## P0 — claim-level findings (evidence)

### P0.1 The frozen green command is unsatisfiable at J (R1 recurrence)

Commands:

```
git -C <lane> cat-file -e 66703acaaff50529a35be49aa8759d04140720ad:.ufo/waves/round-38/final-gates/all-gates.txt
  -> fatal: path ... exists on disk, but not in '66703...'; exit=128
git -C <lane> cat-file -e 7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e:.ufo/waves/round-38/final-gates/all-gates.txt
  -> exit=0
grep -nE '^export-ref-run: (G2|closed=)' .ufo/waves/round-38/final-gates/all-gates.txt
  8:export-ref-run: G2 payload=receipt=0,...,closed=0
  15:export-ref-run: closed=7/8 exit=1
```

The r38 receipt itself proves that an export of the head it names (`export-ref=`) prints 7/8 with G2 red,
because that commit cannot contain the receipt. The r39 head rule is identical to r38's after substituting the
round number (python comparison of the two `judged_head_rule` strings: `equal: True`). The r39 counting command
`--export-ref <J> -> closed=8/8 exit=0` therefore cannot pass; nor can `--selftest --export-ref <J>` print
`failures=0`, because its G2 (and G8, HEAD≠REF) positives are red at J. Correct green ref: the receipt-carrying
tip Y with HEAD==Y; the receipt inside Y names J. This is a wording/erratum decision for the L1 (P0.1 in the
deliverable); it is not fixable in the suite without making G2 read the receipt from outside the export (the
exact false green R1 rejected).

### P0.2 G8 is coupled to the live lane HEAD

`r37-closure.sh:563` `local want=${5:-$ref}`; the E9 payload prints `head-match=...` and E9 returns non-zero
unless `HEAD == want` (the exported ref). So the pinned r37 suite is green only when the r39 run ref equals the
lane HEAD — i.e. the green run is on the tip. A run over J while HEAD=Y is red for G8 independently of the
bytes. `--scratch-root` must not be passed to hide this; the pinned suite's default prefix
(`/fast/scratch/hyaku/kasegi-r37`) must be empty (it is absent today, measured).

### P0.3 Commit-graph shape

r38's `reds.txt` was added at J (`git log --diff-filter=A -- .../reds.txt` → `66703ac ...`), and
`git diff --name-only 66703ac` against each of `7dd2fcd`, `6c0ae18`, `f06148c` lists only
`.ufo/waves/round-38/final-gates/all-gates.txt`. That is why its G2 diff-clean stayed green while a red
transcript existed. For r39: declared-blocks, wave dispatch+results, red transcripts, and every lane append go
in J; Y1=J+field-complete receipt; run over Y1; Y2=Y1+genuine receipt embedding the Y1 run and a `run-ref=<Y1>`
line; `git diff --name-only J Y2` = the receipt only; the scorer re-runs over Y2. A single receipt commit cannot
embed its own run.

### P0.4 Erratum dependencies

```
66703aca50529a35be49aa8759d04140720ad len=37 UNRESOLVABLE
66703acaaff50529a35be49aa8759d04140720ad len=40 resolvable
```

The build item's "Prove it" block still carries the 37-char string; a run with it dies in `git archive` (exit
128), not with the frozen `closed<8/8 exit=1`. E2's 40-hex value is the only one to use.

### P0.5 Landing dependency: the exact judged-head phrase

G2/G5 require `judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt` in the SCORECARD
`## Round 39…` section and in SHONEN's round-39 lines. The SHONEN seat's spec says only "an evidence pointer";
there is no ScribeScorecard seat this round, so the L1 authors the SCORECARD section. Both must be landed with
the exact phrase and zero `Final lane commit` lines, or the green ref reds on G2/G5. `md_section` over the
current SCORECARD for `^## Round 39` is empty (measured), which is exactly the vacuous-green state G5 must
refuse.

## Per-check falsification (measured limb demos)

Method: each demo is a minimal file/fixture plus the naive limb from the r38 suite and the strict limb the r39
spec requires; outputs are the actual run. The 100-line fixture repo for G1 was `git init`-ed under scratch with
identity passed per-command inside the fixture only.

### G1 — whole-tail declarations

```
numstat (base..round): 10 0 PROVINCE.md
naive (tail-2 digest only): GREEN (partial tail of 2 accepted)
strict (declared 2 != added 10): RED
```

Fence states (whole-file walk; naive = r38 exact-3 backtick walk; strict = both types, closer length >= opener):

```
tilde_inside:              naive_walk=closed strict_walk=closed  naive_corr=1 strict_corr=0
backtick_inside:           naive_walk=closed strict_walk=closed  naive_corr=1 strict_corr=0
tilde_unclosed:            naive_walk=closed strict_walk=open
long_open_4_closed_3:      naive_walk=closed strict_walk=open
long_closed_4_4:           naive_walk=open   strict_walk=closed
tilde_door_with_odd_ticks: naive_walk=open   strict_walk=closed
```

Two RED-should-pass holes (unclosed `~~~`; four-tick opener closed by three) and two GREEN-may-fail holes (a
legitimate four-tick fence; a tilde door containing a stray ``` line) fall out of the same walk. The correction
limb is the r38 `g1_correction` hole: it counts a fenced `Correction (round 39)` (1) where the strict count is 0.

Path confinement:

```
declared ../outside.md 1 <sha>: naive [ -f $export/../outside.md ] TRUE (resolves outside the root)
strict realpath prefix: RED
```

Landed append sizes to derive (not hardcode): `PROVINCE.md` 156 lines + 1-line deliverable; `corpus/README.md`
486 lines + 28-line deliverable.

### G2 — graded receipt

```
line [selftest case=G1 positive=pass verdict=pass]            item-rule=accept strict=reject
line [selftest case=G1 positive=pass mutants=0/0 verdict=pass] item-rule=accept strict=reject
line [selftest case=G1 positive=pass mutants=1/2 verdict=pass] item-rule=accept strict=reject
line [selftest case=G1 positive=pass mutants=3/3 verdict=pass] item-rule=accept strict=accept
line [selftest case=G1 mutants=3/3 positive=pass verdict=pass] item-rule=accept strict=accept
```

The item's grading rule (fields present; both pass) accepts a detail-less line and `0/0`; the claim's "graded …
whose mutants are all rejected" requires `mutants=K/N`, N>=2, K=N. The r38 receipt already emits K/N (8 case
lines: 3/3, 6/6, 2/2, 2/2, 4/4, 5/5, 2/2, 2/2; 26 `rejected=1` detail lines; 0 `rejected=0`), so the stronger
rule costs nothing.

```
G1 payload= closed=1            r38 regex ACCEPT; strict reject
G1 payload=province-correction=1 closed=1  both ACCEPT
```

Anchored vs substring on the committed r38 receipt:

```
substring export-ref= lines: 7     anchored ^export-ref=[0-9a-f]{40}$: 1
substring closed= lines:    20     anchored ^closed=8/8 exit=0$:          1
anchored G closed=1: 8 / anchored G any closed: 8 / anchored closed= lines: 1
```

The prefixed red-run lines (`export-ref-run: … closed=0`, `… closed=7/8 exit=1`) must stay prefixed: unprefixed
they create a ninth anchored G line and a second anchored `closed=`.

Digest binding:

```
committed r38 suite sha256 85d33ea9… ; receipt suite-sha256 85d33ea9…
same bytes + appended comment 3b73cab5…  -> only the digest differs
```

The r39 suite must bind executing bytes == receipt digest == export copy bytes (three-way), otherwise a worktree
edit can produce a receipt digest no commit carries. Equality `export-ref == REF` must be RED (strict ancestor);
"ancestor-or-equal" permits the self-name shape R1 rejects and no honest fixed point produces.

### G3 — committed-run truth

```
SCORECARD.md            closed= quotes 17  export-ref pairs 3  added lines vs base 0
SHONEN.md               closed= quotes  6  export-ref pairs 1  added lines vs base 0
LOG.md                  closed= quotes  5  export-ref pairs 0  added lines vs base 0
corpus/lessons/round-38.md closed= quotes 2  export-ref pairs 0  added lines vs base 0
```

Thirty pre-existing quotes (four with pairs) sit in the frozen file list. A whole-file rule reds at the base and
at every honest head; the added-lines scope is required. The R2 correction deliverables quote the r38 receipt's
`closed=7/8` and `closed=8/8` across wrapped lines with two refs; a same-line parser mispairs them, and a
round-39-only transcript dir rejects the only honest witness (the r38 receipt). Allow a paragraph that names a
committed transcript whose bytes contain the pair (the corrections name
`.ufo/waves/round-38/final-gates/all-gates.txt`), and allow any `round-*/final-gates/` block for the quoted
round.

Report-only escape:

```
file-wide report-only on another line: GREEN
same-line/same-paragraph report-only:  RED (the quote has no witness)
```

### G4 — seat identity

```
r38: tasks 73  results 73  top-level seats 73
distinct task names 73 ; distinct task agents 9 (connector, critic, executor, mutation-tester, reviewer, ...)
distinct result names 73 ; distinct result agents 9 ; name sets equal: True
synthetic X/Y/Z vs A/B/C: count-only True, set-equality False
zero-task: count-only True (r38 code's `rtasks >= 0` accepts 0)
```

`agent` is the role, not an identity; the item's "accept `id` or `agent` when unique" would red on the real
file. Use `name` (73/73 unique, set-equal); accept `agent` only if unique and set-equal. Require `results` the
list, not the top-level `seats` int. The r39 wave-1 dispatch has 49 tasks (`wave1-dispatch.json`), so identity
distinctness is cheap to check.

### G5 — label drift

```
md_section(SCORECARD, '^## Round 39') -> EMPTY
naive Final-lane-commit count in that section -> 0 -> GREEN (vacuous)
whole-file 'Final lane commit:' lines in SCORECARD: 5
line-grep correction in a fenced fixture: 1 ; strict outside-fence: 0
```

The section must exist exactly once and be non-empty; the final-label scan must be case-insensitive and scoped to
the section + SHONEN round-39 lines (whole-file reds on 5 historical lines); hex tokens on lines carrying
final/judged/head labels are banned, while `--export-ref <red-run-hash>` quotes are legitimate. A fenced
correction satisfies a line grep and must be rejected by the shared fence walk.

### G6 — scratch quiescence

```
chmod 000 on $root/kasegi-r38:
  naive: find ... 2>/dev/null | wc -l = 0
  strict: find FAILED ('Permission denied') -> unreadable -> RED
kasegi-r37 as symlink + plain file:
  naive -type d count = 0 ; any-entry count = 2
live kasegi-r39 entries at measurement: 6 seat dirs (all must be gone or be the run's own work chain at gate time)
```

The r38 `g6_root_state` already counts every entry and labels a failed scan `unreadable`; do not regress it. The
tolerance is the realpath chain to `--work` (a sibling beside it is residual). `kasegi-r39-l1` at the scratch
root is not one of the three prefixes and must be ignored, not counted.

### G7 — ledger fill

```
naive first-cell prefix + ">=3 rows, 1 and 3": 2 rows match -> GREEN
strict numeric distinct set vs the 2026-10-26 source (7 proposals):
  valid pill: ids [1..7] distinct exact{1..7} closed_vocab True
  mutated 1x/3y: ids [2,4,5,6,7] exact{1..7} False
```

The landed rows are `| 1. Make … | **mined round 39** (criteria; …) | … |`; require `^[0-9]+\.` and a
word-bounded vocabulary word in the status cell, not an exact-cell match. The ledger carries two numberings
(6 from 2026-10-25, 7 from 2026-10-26); the round-39 section rows the seven 2026-10-26 proposals. A heading-only
section (M38-5) must be RED and the correction must be inside the section and outside a fence.

### G8 — pinned carry-over

```
git show 2387dcf6:corpus/instruments/r37-closure.sh | sha256sum
  0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d
export copy (HEAD) sha256: 0da98e37… (identical today)
stub export copy printing "closed=14/14 exit=0": last line [closed=14/14 exit=0]
  pinned 0da98e37… vs stub d4c7dfbc… -> digest gate RED
one-byte mutant of the pinned suite: a23ed9fd… (it still executes; on the base export the scratch run reads
  13/14 vs 12/14, so its own self-check reacts as well — the pinned-digest gate is still required)
```

The r38 G8 executed the export's own copy; the r39 spec must execute the pinned extraction and compare *both*
the pinned copy and the export copy to the hardcoded sha256 constant (not a git blob sha1, not the export's own
digest). The stub proves a last-line-only check is not a gate.

## Cross-cutting checks confirmed against the r38 bytes

- Anchored receipt counts (r38): `all-gates v2` ×1, `export-ref` ×1, `suite-sha256` ×1, G lines ×8 (all
  closed=1), anchored `closed=` ×1, case lines ×8, summary ×1, `rejected=1` details ×26, `rejected=0` ×0. The
  r39 v3 parser should keep all of these anchored and add the mutants-fraction, empty-payload, strict-ancestor,
  three-way-digest and detail-line limbs.
- `bash -n`, plain-run exit 2, and the `--work`-inside-lane refusal are r38 guards to carry forward unchanged;
  the r39 selftest must not weaken the judge (own report accepted, forged reports rejected).

## Deliverable

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39/wave1/CritDesignReview.design.md`

```
wc -l   -> 350
sha256  -> 763271fba2561a1086e100229052747ce4dbe6151ab48a3e5301e58261a18805
```

Contents: P0.1–P0.5 (claim-level blockers/corrections), a per-G table with the RED-should-pass and
GREEN-may-fail states, the MUST limbs (with the exact predicates/bindings), the selftest mutant list per check,
the cross-cutting output/receipt contract, the L1 verification sequence, and the fixture map.

## No-harm / scope

- Writes: this receipt, the design deliverable, and scratch only. No lane/tree edits, no fleet-root writes, no
  PATH writes, no mutating git/jj anywhere; the lane's git was read-only. Fixtures lived under scratch
  (`git rev-parse --show-toplevel` asserted) and were removed with the scratch dir.
- The two `demo*.sh` drivers and their outputs were under `/fast/scratch/hyaku/kasegi-r39/CritDesignReview/` and
  are removed before yield; the outputs quoted above are the ones they produced.
- No score move is claimed. The deliverable is a checklist for ExecSuiteBuild/verification and the wave-2
  attack; it does not judge C1 or edit the frozen claim.

## Open decisions for the L1 (blocking C1 closure)

1. P0.1: state the green ref as the receipt-carrying tip Y (erratum or report wording); keep the J red embedded.
   Without this the frozen counting command is unsatisfiable.
2. P0.3: land every non-receipt artifact in J; Y adds only `all-gates.txt`; use the Y1→Y2 genuine-receipt flow.
3. P0.5: land the exact judged-head phrase in the SCORECARD `## Round 39…` section and SHONEN round-39 lines.
4. E2: use the 40-hex r38 head in every control run; the 37-char string is an invalid object name.
