# MutBaseline — round 40, wave 1 (baseline mutation probe)

Seat: MutBaseline (mutation tester, leaf — no subagents dispatched). Item:
baseline-mutate the r39 closure suite at 8371e7ac9f32cae5ed72f8c28205634603f836fa
in scratch, reproduce the wave-2 finding that G2 accepts forged payload values
(CritG2Exploit F2) at full-suite level, and show a G6 prefix patch hides a stray
sibling. Deliverable: `MutBaseline.txt` (this dir). I authored none of the bytes
under attack: the suite is ExecSuiteBuild's round-39 deliverable, the receipt is
the round-39 L1's. Axes: depth:verifiability (primary), coverage (untouched).

## Environment and tooling

- No tools installed or upgraded (no pacman, no network, no uv/npx needed):
  bash, git, awk, sed, sha256sum only. Nothing to record under the 2026-10-19
  authorization.
- Disk guard green before the run: /fast/scratch/hyaku at 26% use, 601.6G free.
- Scratch S=/fast/scratch/hyaku/kasegi-r40/MutBaseline (removed before this
  receipt was finalized; contents persisted: deliverable + this receipt only).
- Lane repo /home/vgpnk/Projects/shokunin/kasegi-shokunin: READ-ONLY to this
  seat. All suite runs used `--lane <scratch clone>` and `--work` under S; no
  mutating git command touched any real repo. Read-only commands used against
  the lane: rev-parse, ls-tree, log, diff (no write flags), status, show,
  archive, clone (source untouched).

## Fixture provenance (all mutations inside scratch fixtures)

- `git clone <lane> S/lane-clone`; asserted
  `git rev-parse --show-toplevel` = the clone dir before any commit. Detached
  at 8371e7a, clean.
- Pristine suite extracted at 8371e7a into S/r39-export; sha256
  2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b — the same
  digest the r39 receipt names in `suite-sha256=`, so the bytes under test are
  exactly the committed instrument.
- Mutant copies built by find->replace (edit tool, per-patch auditable):
  - mut-g2: P1+P2+P3 (receipt-validation limbs), sha256
    21ef1eb211faa5d1ef8c7151f73955ca0ec33c6a90f384e978cc38b5684a293b;
    `bash -n` clean.
  - mut-g6: M4 only (G6 scan prefix kasegi-r39 -> kasegi-r90), sha256
    b95b913a1c75b19102522855c7f1f1fcc5d798d83b86ee8f1e1d6e073f8ee5c0;
    `bash -n` clean.
- FORGED1 = a00d1f78901cd52aa5b9bb9aa301b68b8721a23a (clone commit: suite bytes
  swapped to mut-g2 — required because G2's digest limb binds the receipt to
  the executing AND export copy; a forger must swap both, which is itself part
  of the demonstrated defect).
- FORGED2 = 97536d3747a4057ee762bd3a0a5ce8275be829f0 (clone commit on FORGED1:
  receipt only; `git diff --name-only FORGED1 FORGED2` =
  `.ufo/waves/round-39/final-gates/all-gates.txt`). Clone left detached at
  FORGED2, clean, so the pinned r37 suite's E9 head limb stays green.
- Honest receipt at 8371e7a: sha256
  8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471.
  Forged receipt (4 lying lines + 1 dropped line, all payload values honest):
  sha256 5e52e57a64612ef8ce44c49300de830cfa26be3b5a607055a93e0115fa976000.

## Runs (full transcripts hashed; evidence lines quoted in the deliverable)

| run | suite | export-ref | rc | suite tally | transcript sha256 (prefix) |
|---|---|---|---|---|---|
| R0 | pristine 2856a210 | 8371e7a (honest receipt) | 1 | closed=7/8 exit=1 | 89df5ccd |
| R1 | pristine 2856a210 | FORGED2 (tampered receipt) | 1 | closed=7/8 exit=1 | eaee2901 |
| R2 | mut-g2 21ef1eb2 | FORGED2 (same tampered receipt) | **0** | **closed=8/8 exit=0** | 6dafa56d |
| R3 | pristine 2856a210 | FORGED2, --scratch-root with stray kasegi-r39/SomeOtherSeat/work | 1 | closed=6/8 exit=1 (G6 r39=present closed=0) | a7d8af05 |
| R4 | mut-g6 b95b913a | FORGED2, same stray still present | 1 | closed=7/8 exit=1 (G6 r39=absent closed=1 — stray unnoticed) | fca4e66e |
| F2 | pristine, limb driver `check_g2` | tree/ref fixture, receipt with mutants=0/0 case lines + empty payloads | **0** | graded-cases=8 ungraded-cases=0 run-lines=8 all green | (driver output quoted in deliverable) |

G2 payload contrast (identical receipt bytes in R1/R2):

- R1 pristine: `digest-match=0,run-lines=7,closed-lines=1,closed-line=0,graded-cases=7,ungraded-cases=1 ... closed=0`
- R2 mut-g2:  `digest-match=1,run-lines=8,closed-lines=0,closed-line=1,graded-cases=8,ungraded-cases=0 ... closed=1`

R0 additionally proves the fixture environment is sound (G1,G3-G8 all green at
the honest head, including G8's pinned r37 run r37-closed=1,r37-exit=0), so the
R1->R2 flip is attributable to the three patches alone.

## Verdict per mutant (mutation-tester roles)

| mutant | expected | observed | verdict |
|---|---|---|---|
| P1 (g2_graded field-free grading) | tampered receipt accepted | R2 graded-cases=8/ungraded-cases=0 on a verdict=fail line; suite rc=0 | survived (baseline defect) |
| P2 (g2_run_shapes values unread) | accepted despite closed=0 run line | R2 run-lines=8/closed-lines=0; suite rc=0 | survived (baseline defect) |
| P3 (final-tally any-value) | accepted despite closed=7/8 exit=1 | R2 closed-line=1; suite rc=0 | survived (baseline defect) |
| M4 (G6 scan prefix) | stray sibling unnoticed | R4 r39=absent closed=1 with live stray; vs R3 r39=present closed=0 | survived (baseline defect) |

No baseline failures: every control behaved as documented (R0 honest red, R1
pristine rejection at 5 limbs, R3 stray detection). One non-target red in R4
(pristine G2 limbs correctly red the tampered receipt under mut-g6) — recorded,
not a defect of the probe; it shows M4 is independent of P1-P3.

## Incidental finding (pristine parser, reported to inform the r40 suite)

`sed -n 's/^export-ref=//p'` lifts every line-start `export-ref=`; the honest
receipt's transcript header starts with `export-ref=ee5ae5e... mode=export ...`,
so xref becomes two lines and `git cat-file -t` fails: R0 shows ancestor=0,
diff-clean=0 while `git merge-base --is-ancestor ee5ae5e 8371e7a` is rc=0
(verified). The honest v5 receipt can never pass G2's ancestry limb as written.
Recommendation carried in the deliverable: the r40 suite should anchor receipt
parsing to exact whole-line matches (claims H5/H7) and key transcripts off a
non-colliding marker.

## Restoration evidence

- Pristine suite bytes re-hashed after ALL runs:
  2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b (unchanged;
  mutants were separate copies).
- Lane repo: only reads + one clone (source untouched). Tracked-file state
  observed at yield: `corpus/SOURCES.md` modified — that is a C2 sibling seat's
  concurrent wave-1 work, not this seat's (this seat's only lane writes are the
  two files in `.ufo/waves/round-40/wave1/` named below); no other tracked file
  modified by anyone at observation time.
- Fixture clone and all transcripts lived under S and were removed with S
  before yield (`rm -rf` on S/g6root stray included — no kasegi-r37/38/39/90
  entries were ever created under the real /fast/scratch/hyaku root; the G6
  demonstration used `--scratch-root` inside S).

## Deliverable

- `.ufo/waves/round-40/wave1/MutBaseline.txt` — 162 lines, sha256
  49cd014775e93fee1fb1e12c8ce8a02f3b237c4d4c78f19ff0293492c701d8a5.
  Contents: patch list (P1/P2/P3/M4 with exact find->replace pairs and mutant
  hashes), forged-receipt spec, observed outputs R0-R4 + F2 with full G2/G6
  payload lines, incidental xref-poisoning finding, verdict.

## What the main agent can spot-check

1. `git -C <lane> cat-file -t a00d1f78901cd52aa5b9bb9aa301b68b8721a23a` fails
   outside my (removed) clone — the fixture commits existed only in scratch;
   the hashes above are reproducible only from the transcript hashes. The
   probe is re-runnable: the deliverable's patch list applied to the pristine
   suite bytes at 8371e7a reproduces every quoted output.
2. The r40 suite's H5/H6/H7 graded cases should each fail open against this
   baseline: forge a receipt per the deliverable's 4-line recipe, weaken the
   corresponding limbs P1/P2/P3-style, and require the H5 fixture to still red
   (it can only do so if H7's determinism binding or an exact-line parse is
   load-bearing, not a `grep -c` shape count).

Report: .ufo/waves/round-40/wave1/MutBaseline.md
