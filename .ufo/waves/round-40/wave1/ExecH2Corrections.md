# ExecH2Corrections — round 40, wave 1 (executor)

Item: four `Correction (round 40)` append blocks (SCORECARD.md, LOG.md, SHONEN.md,
`corpus/lessons/round-39.md`) naming the final round-39 receipt values and the G2/G6
non-independence reason. Axes: **depth:verifiability** (H2 of the C1 suite), **coverage** untouched.

Scratch `S=/fast/scratch/hyaku/kasegi-r40/ExecH2Corrections` (removed before yield). Disk guard read
before work: `/tmp 3%`, `/var/tmp 35%`, `/fast/scratch/hyaku 26%` — green. Tooling: none installed,
nothing upgraded (no pacman, no uv/npx, no network). No mutating git/jj command run anywhere.

## Inputs read (lane repo, read-only)

| Path | sha256 |
|---|---|
| `.ufo/waves/round-40/claims.json` | `33a4602d3669aab178907082421fc72c3f2e938a06d902696ff4cb86cba2953f` |
| `SCORECARD.md` (1584 lines) | `0a7843f200495bba1354115d21b06833f5804f53259479f0d5f06fa2c906825d` |
| `LOG.md` (1719 lines) | `d2fe1ad94fa5340f70ed7b9b77d9216acd13be470f4cb33a485fc431a9061815` |
| `SHONEN.md` (203 lines) | `b1864cfffe23518d95ff61c745581c72b92b6fc0c07d94a627bb3b7de544bf39` |
| `corpus/lessons/round-39.md` (94 lines) | `dc530f1a1689ffd0bb4bf901c6624737588dcfff1a91be6cced6608cfb17004a` |
| `corpus/lessons/round-39-verifier-spotcheck.md` | `c71321c8606f1074b52bdf5da048e2346566af62a4375679924871fc226e289b` |
| `.ufo/waves/round-39/wave2/CritG2Exploit.md`, `CritC1Kill.md` | read; quoted findings below |

## The exact sentence R2 asked for

`corpus/lessons/round-39-verifier-spotcheck.md:173` (raw `cat -A`, `$` = EOL):

```
  `Correction (round 40)` lines naming the final receipt values in each record.$
```

Preceded at `:172` by "…do not name the final 7/8 / `failures=1` in SCORECARD and SHONEN. Append".
Each of the four blocks quotes the sentence verbatim, prefixed `Verifier R2's ask, quoted: "…"`.

## Measured facts the blocks assert

Final receipt at Y = `8371e7ac9f32cae5ed72f8c28205634603f836fa`:

```
$ git -C <lane> show 8371e7a:.ufo/waves/round-39/final-gates/all-gates.txt | sha256sum
8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471  -
$ … | head -4
all-gates v5
export-ref=ee5ae5e1739527f4cdb50babe2d694005607b44e
suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
run-utc=2026-10-26T20:54:44Z
$ … | sed -n '10p'      # G2, the single red
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=0,diff-read=ok,digest-match=1,export-suite=1,run-lines=8,closed-lines=0,distinct-ids=8,closed-line=1,graded-cases=8,ungraded-cases=0,selftest-summary=1,scorecard-ref=1,shonen-ref=1,final-lane-commit=0 closed=0
$ … | sed -n '14p'      # G6, green with a tolerated work dir under the seat root
G6 payload=r37=absent,r38=absent,r39=empty,work=inside,tolerated=/fast/scratch/hyaku/kasegi-r39/gates-work,read=ok closed=1
$ … | sed -n '17,18p;39p;79p;87p'
closed=7/8 exit=1
run-exit=1
selftest case=G2 positive=fail mutants=8/8 verdict=fail
selftest cases=8 failures=1
selftest-exit=1
```

All committed revisions of that receipt (`git log --all -- .ufo/waves/round-39/final-gates/all-gates.txt`):

| rev | header | `run-utc` | tally | commit `%cI` |
|---|---|---|---|---|
| `8371e7ac` (Y) | all-gates v5 | `2026-10-26T20:54:44Z` | `closed=7/8 exit=1`, `selftest cases=8 failures=1` | `2026-10-26T17:55:17-03:00` |
| `b810df6c` | all-gates v5 | `2026-10-26T20:54:44Z` | same | `2026-10-26T17:55:17-03:00` |
| `5006097a` (attempt-1 Y) | all-gates v3 | `2026-10-26T21:35:00Z` | `closed=8/8 exit=0`, `selftest cases=8 failures=0` | `2026-10-26T17:12:12-03:00` (= 20:12:12Z) |
| `de203895` | all-gates v3 | `2026-10-26T21:35:00Z` | same | `2026-10-26T17:12:12-03:00` |

So the only 8/8 tally is the attempt-1 v3 receipt whose `run-utc` (21:35:00Z) post-dates its containing
commit (20:12:12Z) — the R1 discard. `grep -c 'closed=8/8'` over the four revisions → `0 0 1 1`.

Ancestry, for the "earlier head" wording: `git merge-base --is-ancestor 3fa81ef5… ee5ae5e1…` exit 0
(3fa81ef5 = `2026-10-26T17:48:26-03:00`), and `… ee5ae5e1… 8371e7ac…` exit 0 (J ancestor of Y).

Non-independence of the two limbs the pass would rest on:

- **G2**: `wave2/CritG2Exploit.md` F2 — `g2_graded` reads only `positive=pass`/`verdict=pass`, never
  `mutants=`; `g2_run_shapes` accepts an empty payload. Probes f (no `mutants=`), g (`mutants=0/0`),
  h (empty payload), j (`mutants=0/1`), k (indented ninth case line) all grade `rc=0` with payloads
  byte-identical to the green control. A hand-written receipt is indistinguishable from a run by this limb.
- **G6**: `wave2/CritC1Kill.md` §row 3 — with seats live the same limb prints
  `G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=none,read=ok closed=0`; it greens only
  on a quiet `/fast/scratch/hyaku/kasegi-r39/`, the root the seat spec mandates for seat scratch. The Y
  receipt greens it with `deviation=non-default --lane` recorded (`:8`).

## Deliverable

Path: `.ufo/waves/round-40/wave1/ExecH2Corrections.txt` — **16 lines, 5493 bytes**,
sha256 `7529e20c777edc312ed2033d2ef285c8f6ebbebd8b046fe81b8491607b8ef087`.

Four blocks, each preceded only by its marker line (which the L1 strips):

| Marker (line) | Target record | Block body |
|---|---|---|
| `## BLOCK SCORECARD.md` (1) | `SCORECARD.md` EOF | blank line + 2 `^Correction (round 40)` lines |
| `## BLOCK LOG.md` (5) | `LOG.md` EOF | blank line + 2 lines |
| `## BLOCK SHONEN.md` (9) | `SHONEN.md` EOF | blank line + 2 lines |
| `## BLOCK corpus/lessons/round-39.md` (13) | `corpus/lessons/round-39.md` EOF | blank line + 2 lines |

Each block names the overstated lines it corrects, not the file line numbers (which stay stable anyway):
SCORECARD `## Round 39 result` depth:verifiability row (quoted `closed=8/8 exit=0` at Y, graded
`selftest cases=8 failures=0`) + the claims row's report-only `3fa81ef5…`; LOG `## Round 39` C1 bullet +
the round-39 correction below it; SHONEN round-39 box 3 evidence line (quoted "suite `--selftest` graded
cases=8 failures=0 at the verification ref"); lesson Frozen claims C1 after-cell + the
`## Final measurement at integration head J1` paragraph.

Validation (splice into scratch copies; lane files untouched). Output verbatim:

```
deliverable bytes=5493 lines=16 sha256=7529e20c777edc312ed2033d2ef285c8f6ebbebd8b046fe81b8491607b8ef087

== SCORECARD.md: block lines=3 orig_lines=1584
  added_lines=3 (orig 1584 -> 1587)
  ^Correction (round 40) count=2
  baseline count=0
  orig trailing newline=True

== LOG.md: block lines=3 orig_lines=1719
  added_lines=3 (orig 1719 -> 1722)
  ^Correction (round 40) count=2
  baseline count=0

== SHONEN.md: block lines=3 orig_lines=203
  added_lines=3 (orig 203 -> 206)
  ^Correction (round 40) count=2
  baseline count=0

== corpus/lessons/round-39.md: block lines=3 orig_lines=94
  added_lines=3 (orig 94 -> 97)
  ^Correction (round 40) count=2
  baseline count=0

FAILS: none
```

The script asserts, per block: body ≤ 6 lines; first non-blank line matches `Correction (round 40):`;
body contains `closed=7/8 exit=1`, `selftest failures=1`, the Y hash and the R2 sentence verbatim; no
fence or tilde marker; the original file bytes are an exact prefix of the spliced file (pure append,
zero deletions) and added lines = block lines. Deliverable hygiene: 4 markers, 8 anchored corrections,
0 trailing-space lines, 0 CR bytes.

## Write scope / no-harm

Wrote exactly two files, both under `.ufo/waves/round-40/wave1/`: this receipt and
`ExecH2Corrections.txt`. No lane record was edited (target file shas above are pre-land values for the L1
to diff), no fleet-root or `/home/vgpnk/Projects/shokuknow` write, no PATH write, no `corpus/instruments`
touch, no `SKILL.md`/`PROVINCE.md`/`SOURCES.md` touch. Scratch removed on exit; no `kasegi-r39*` or
`kasegi-r40` sibling left by this seat beyond the shared `/fast/scratch/hyaku/kasegi-r40/` parent.

## Risks / notes for the L1

- The blocks must be appended at EOF (not inserted) so G1's whole-tail declaration sees added lines only;
  the leading blank line in each block is part of the added bytes.
- SHONEN's box numbering: the round-39 evidence line at `:194` is **box 3** ("Instructions executable by
  an agent without oral context"), matching the round-39 correction's own "box 3" wording at `:190`/`:203`;
  the round-39 verifier's §5 R2 calls it "box 1" — the block uses the file's own numbering and quotes the
  line's text, so it resolves either way.
- H2 itself is the L1's to execute; this seat measured the blocks by splicing, not by landing them.
