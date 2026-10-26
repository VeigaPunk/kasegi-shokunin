# RevH3Criterion — round-40 falsify wave 2 receipt

Seat: reviewer (leaf; no subagent dispatch, no background job). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` only; fleet root and `/home/vgpnk/Projects/shokuknow`
read-only, untouched. Base `a7af2ce63bce153757d39bf66b366a96caf30c13`; claims-freeze
`5e985b74075dd3813a63d7750966bf8abf693465`; frozen claims read at `.ufo/waves/round-40/claims.json`
(not edited). Refs measured this run: judged head J = lane tip `3074c7679d6f527ec3930d7748ccce1dbae4a58a`
(`git log`: 5e985b7 freeze → 4766b9d integrate wave1 → bfca9ae J2 → 8717b8b J3 → 94abbff J4 → 3074c76 J5);
the receipt `.ufo/waves/round-40/final-gates/all-gates.txt` (1062 bytes, untracked) is the only pending
Y delta, so at today's tip `corpus/QUALITY.md` at Y is byte-identical to `corpus/QUALITY.md` at J.
Simulated Y = scratch clone head `198e68a6bb905e46396d3b06e17d8804f9f00f24` (lane clone + the receipt
committed on top of J, nothing else; `git diff --name-only 3074c76… 198e68a…` →
`.ufo/waves/round-40/final-gates/all-gates.txt` only). Disk guard before work: green
(`/fast/scratch/hyaku` 24% use, 615.0G free; `/tmp` 3%; `/var/tmp` 35%). Scratch
`S=/fast/scratch/hyaku/kasegi-r40/RevH3Criterion` removed before yield. Tooling installed: none (nothing
needed; pacman paused and not touched).

## Attack item (H3)

What is attacked: (a) wave-1's H3 deliverable — the R37 criterion row appended to `corpus/QUALITY.md`
(`wave1/ExecH3Criterion.{txt,md}`, landed in 4766b9d, untouched by J2–J5); (b) the H3 gate
`check_h3` in `corpus/instruments/r40-closure.sh:626-639`; (c) the frozen claims' H3 promises — C1
predicate "corpus/QUALITY.md carries a table criterion row citing M39-2", counting commands 1–2 at Y,
and the R36 flag shape ("a criterion that names the class without citing M39-2", QUALITY.md:309).

## Re-runs — all reproduced

| # | command (at committed bytes) | result | call |
|---|---|---|---|
| 1 | `git archive 3074c76… \| tar -x` then `grep -cE 'M39-2' corpus/QUALITY.md` | `1` (≥1) | reproduced |
| 2 | same grep at claims-freeze `5e985b7…` | `0` | reproduced (criterion is new this round; R5's "→ 0" premise confirmed) |
| 3 | `r40-closure.sh --export-ref 3074c76… --receipt-out <S>/my-receipt.txt` | `closed=10/10 exit=0`; `H3 payload=mentions=1,rows=1 closed=1`; teed receipt **byte-identical** (`cmp`) to the lane's `all-gates.txt` | reproduced |
| 4 | `r40-closure.sh --export-ref 3074c76…` (plain, no `--receipt-out`) | `closed=9/10 exit=1`, `H7 payload=receipt=0,…` | mechanics, not a defect: at J the receipt is not yet in the exported tree, and H7 validates the teed file via `--receipt-out`; at Y the receipt is committed and the plain command goes green (row 6) |
| 5 | `r40-closure.sh --selftest --export-ref 3074c76…` | `selftest case=H3 positive=pass mutants=2/2 verdict=pass`; `cases=10 failures=1` — the one failure is `case=H7 positive=fail` (`payload=receipt=0`), same receipt-not-in-export mechanics; all 6 H7 mutants still `rejected` | reproduced for H3 |
| 6 | simulated Y `198e68a…`: `--export-ref 198e68a…` | `closed=10/10 exit=0`, `H3 mentions=1,rows=1 closed=1`, transcript **byte-identical** to the lane receipt | reproduced — claims counting command 1 verified at Y exactly |
| 7 | simulated Y: `--selftest --export-ref 198e68a…` | `selftest cases=10 failures=0 exit=0`; `case=H3 positive=pass mutants=2/2 verdict=pass`; `case=H7 positive=pass mutants=6/6 verdict=pass` | reproduced — claims counting command 2 verified at Y exactly |

Determinism note: the receipt's `run-utc=2026-10-26T21:56:22Z` equals the committer instant of
`3074c76…` (`2026-10-26T18:56:22-03:00`) — `time-basis=ref-commit` honored, run-utc printed by the run
itself and not future-dated, exactly the R37 rule. Two independent re-runs (rows 3 and 6) produced
byte-identical transcripts.

## Grounding audit of the R37 row (`corpus/QUALITY.md:323`, 2985 bytes)

- **Cites the lesson row**: `M39-2 (`corpus/lessons/round-39.md:77`, § Mistakes)` — pointer verified:
  M39-2 is `round-39.md:77` at Y (class `evidence-record`; five r38 records state the C1 run/selftest
  over the judged head where the receipt contradicts them).
- **Cites the routed defect**: R5 at `round-39-verifier-spotcheck.md:181-182` — quoted text matches the
  committed bytes verbatim ("M39-2 has `captured-by: none` and no criterion … Add the criterion or state
  in the lesson why not").
- **Cites the provenance-limb source**: R1 (`:158-167`) — every value checked against committed bytes:
  `5006097a:.ufo/waves/round-39/final-gates/all-gates.txt` line 4 records
  `run-utc=2026-10-26T21:35:00Z`; commit `5006097a` committer instant `2026-10-26T17:12:12-03:00` =
  `20:12:12Z` (run-utc post-dates its commit); v3 tally `closed=8/8` vs the L1's own run
  `closed=6/8 exit=1`, `selftest cases=8 failures=2`; `make-receipt.sh` printed no `run-utc` line.
  All match the row's text.
- **Also cites** M39-3 (`round-39.md:78`) — pointer verified (quote-without-transcript class, same
  family from the other direction).
- **States the receipt-transcript rule verbatim**: "a receipt is only the unedited tee of one observed
  run: its bytes are that invocation's stdout+stderr as written, with no hand-written header, no edited
  tally and no value the run did not print, and its `run-utc` is printed by the run itself at execution
  and never post-dates the commit that contains it" — present in the criterion cell.
- **Append-only premises verified at `5e985b7…`**: 53420 bytes / 309 lines / `head -c 53420 | sha256sum`
  → `b379ed92eba012d8d4910526745abfe98ac76c9c538841b83df6799ebdd16fd5` — all three match the row's
  R6-form figures; `grep -c 'R37'` → 0 and `grep -c 'M39-2'` → 0 at pre-append (next-free-id and
  new-criterion premises true); `git diff --numstat 5e985b7… Y` on QUALITY.md = `14 0` (pure append).
- **Wave-1 landing fidelity**: the landed file's last 3807 bytes equal
  `wave1/ExecH3Criterion.txt` (sha256 `84ad5eda9b9ab19cc378d25d966e02eaa3f4f0b2646f4e025f80e4ce307d83f6`,
  matching `kasegi-r40-build-results.json`) byte-for-byte (`cmp` clean); landed bytes 1–53420 equal the
  pre-append file byte-for-byte. The landed file is 57226 bytes = pre + 3806: the txt's leading `\n`
  coincides with the pre file's existing trailing newline, so a literal `cat >>` (57227 bytes, heading
  at :312) was not what landed — one boundary newline is shared instead. Every substantive promise holds
  (lines 1–309 byte-identical, row content byte-exact, the row's own "appended after line 309" figure
  true); recorded as observation O4, not a defect.

## R36 flag check and mutation tests

The only `corpus/QUALITY.md` criterion naming the receipt class is R37, and it cites M39-2 → **no flag
warranted on the landed tree**. The flag condition was then mutation-tested with the original suite
against scratch fixture repos (each fixture commit preceded by a `git rev-parse --show-toplevel`
assertion; `--lane` pointed at the fixture; only the H3 line read):

| mutant | tree | H3 result | reading |
|---|---|---|---|
| A1 — criterion names the class, `M39-2` token removed everywhere (`s/M39-2/M39-9/g`) | fixture head `2cc31d2` | `mentions=0,rows=0 closed=0` (RED) | gate catches the R36 shape when no token exists ✓ (matches selftest mutant `row-absent-at-all`, limb `mentions=0`) |
| A2 — bypass: same token removal + stray table row `\| R38 \| unrelated filler row \| M39-2 stray citation \|` appended | fixture head `3a1a95b` | `mentions=1,rows=1 closed=1` (GREEN) | **gate fooled while the criterion does not cite M39-2** — defect F1 |

In A2 every other red is fixture-repo mechanics (H7 `receipt=0`, H8 refs absent, H9/H10 `diff-read=fail`
— the fixture lacks the lane's base refs), so no other gate binds the citation to the criterion row
either; in a real lane (refs present, declared-blocks regenerated as the lane does each round) the
bypass sails through at `closed=10/10`. The built-in selftest covers `row-absent-at-all` and
`mention-without-criterion-row` (both rejected) but not this shape.

## Findings

- **F1 — minor, gate strength (H3).** `check_h3`'s rows counter (`grep -E '^\|' corpus/QUALITY.md |
  grep -cF -- 'M39-2'`) accepts any pipe-initial line, so a non-criterion stray row satisfies the gate
  while the criterion row itself names the class without citing M39-2 — the exact shape R36
  (QUALITY.md:309) says "does not close it". The instrument header's stated intent ("carries a table
  criterion row citing M39-2", r40-closure.sh:18) is not enforced; only token presence in some table row
  is. The frozen claim's letter (`grep -cE 'M39-2' corpus/QUALITY.md >= 1`) is intact and the landed
  tree satisfies the intent, so this is a hardening gap, not a claim contradiction. Evidence: fixture
  head `3a1a95b` (Y export + the two-step mutation), suite output `H3 payload=mentions=1,rows=1
  closed=1`. Byte-exact fixture shipped: `RevH3Criterion.h3-bypass.txt` (57280 bytes, sha256
  `69549d19fe6147521f7820fe7d8e6566e4bb7c80038132dcadb7c429da54258e`) = the exact `corpus/QUALITY.md`
  bytes the gate consumed. Hardening suggestion: bind the rows count to the criterion row itself (e.g.
  require M39-2 in the same row that carries the receipt-rule keywords, or require the row's id cell to
  be the criterion id the lesson's captured-by names).
- No other defect found in the H3 target.

## Observations (not defects)

- **O1** — `selftest cases=10 failures=0` is Y-conditioned: at J it prints `failures=1` (H7 positive has
  no receipt in the export; mechanism verified, all mutants still rejected). Flips green at Y — verified
  in the simulated-Y clone (row 7). Anyone re-running claims counting command 2 at today's tip sees
  `failures=1`; that is the receipt-commit boundary, not a regression.
- **O2** — M39-2's captured-by cell (`round-39.md:77`) still reads "none — corrections sweep this round
  (R2)" although the criterion now exists (R37); M39-4's cell was updated to "none — R36 criterion
  added". R36 is satisfied by the criterion's existence, so no rule breaks; the stale cell is cosmetic.
- **O3** — R37's grounded-in cell does not name M40-1 (the round-40 lesson row mined from R1); M40-1's
  fix cell names R37, and R37 cites R1 (`:158-167`), so the chain is complete without the reverse
  pointer; no rule requires it.
- **O4** — wave-1's receipt documents the landing as `cat …txt >> corpus/QUALITY.md`; the landed bytes
  correspond to that append with the boundary newline shared (57226 vs 57227 bytes, heading at :311 vs
  :312). All substantive promises verified true (see grounding audit); documentation nuance only.

## Verdict

**H3 target VERIFIED at Y.** The counting grep reproduces (`1 ≥ 1`) on committed bytes and is new this
round (`0` at the claims-freeze pre-append head). The criterion row is grounded: it cites M39-2 with an
accurate `corpus/lessons/round-39.md:77` § Mistakes pointer, cites routed defects R5/R1 with every value
matching committed bytes, and states the receipt-transcript rule verbatim. No R36 violation exists in the
landed tree, and the gate correctly reds the uncited-class mutant (A1). Both claims' H3-related counting
commands reproduce at Y exactly (byte-identical transcript; `selftest cases=10 failures=0`). One minor
gate-strength defect found (F1, stray-row bypass) and delivered with a byte-exact fixture.

## Hygiene

Scratch `S` removed before yield. Writes limited to this receipt and
`RevH3Criterion.h3-bypass.txt` in `.ufo/waves/round-40/wave2/`. No lane, fleet-root, or shokuknow file
edited; no git/jj mutation outside scratch fixture repos (toplevel asserted before every fixture
commit); no tool installed; no host service touched.
