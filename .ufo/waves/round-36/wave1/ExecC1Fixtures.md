# ExecC1Fixtures — per-check red/green fixture set for the r36-closure suite (C1)

Seat: ExecC1Fixtures (leaf executor, hyaku run 9, round 36). Item: build a fixture
set proving each of E1–E9 can fail (red) and pass (green); record the fixture
inventory, each red/green exit, and a check→red_exit→green_exit matrix; prove the
matrix is not vacuous. Judged axis: depth:verifiability.

Lane writes: this receipt only. Everything else ran in
`/fast/scratch/hyaku/kasegi-r36/ExecC1Fixtures/` (removed at yield). No lane file
was edited, no git mutation touched the lane, no tool was installed (bash, git,
python3 were already present; pacman untouched).

## 1. What was tested

Two scripts, both drafts, both outside the lane:

| role | path | sha256 | lines |
|---|---|---|---|
| checker under test (mine) | scratch `r36-closure.sh` | `4283a9d3eae810e03ddc6181e4c7a11de491e0fdd4f8f554ce7c1fbc947c03e5` | 308 |
| fixture generator | scratch `r36-fixture-gen.py` | `474a27eef6d8e310bb8cfbdfc750d8538351d1c78d2b0c466860c76f1b0e973c` | 367 |
| per-check driver | scratch `matrix.py` | `2e640fcf6dff84fc52e07d90dc68e31c41614e0279c29256053ec572ad53267c` | — |
| clause driver | scratch `clause.py` | `4cb8ac3fbfeacbce1d29d727337fafaa8ecadfb0b991445c207b8b2a91cea249` | — |
| suite-mutant driver | scratch `suitemut.py` | `2def666d6f0179ce6fde92ebb980e9fd571f6e619b763012f829d37b4208644d` | — |
| cross driver | scratch `cross.py` | `f72a677b1f8683fa032ac9f5f5aed0a33fd1d665cf127d51a5126728a80b0574` | — |

ExecC1SuiteBuild's instrument was not in the lane when this seat started, so the
draft above implements the frozen E1–E9 reading and every fixture was **also**
run through ExecC1SuiteBuild's evolving draft (`--lane <fixture> --export-ref
HEAD --work <outside> --scratch-root <empty>`). The draft moved three times
while this seat ran: `53d9e324…`, `9fbdee690bb5540704b29079a63f854272c757ddba7d70db02b7bab420d49e16`,
`76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323`, and
`4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (their
final, extracted from their receipt and sha-verified). §6 reports the per-check
table as it held at each digest it was measured on. The cross run is the part that speaks to the instrument that will
be committed.

My draft's modes: `--export-ref <hash>` (git archive + checks over the export;
E1 ancestry and E9 quiescence read the lane repo, as they must), `--root DIR
--gitroot DIR` (fixture mode, HEAD of the fixture repo is the exported ref),
`--selftest`. Quiescence scan root is `KASEGI_R36_SCRATCH` so a fixture can own
its own empty scratch root.

## 2. Fixture inventory

Source tree `src/` = pruned `git -C <lane> archive b47f2cd -- SCORECARD.md
SKILL.md {AGENTS,PROVINCE,README,SHONEN,LOG}.md corpus/QUALITY.md
corpus/lessons/* .ufo/waves/round-34/wave1/L1Integration.md
.ufo/waves/round-35/wave1-results.json .ufo/waves/round-35/claims-erratum-d5.md`
(1.6 MB; the full export is 120 MB and ten copies were not affordable).

Every fixture is its **own git repository**, because three limbs cannot be
measured on a bare tree: E1's ancestry (`cat-file`/`merge-base --is-ancestor`),
E4's index limb (`git ls-files`) and E9's worktree limb (`git status`). Fixture
repo is `git init` + two commits with fixed `GIT_AUTHOR_DATE`/
`GIT_COMMITTER_DATE`, so the base sha is a deterministic function of `src`:

- **C0** — `src` normalised to the round-36 closure state, final-lane line reads
  `PENDING_HASH`.
- **C1** — `PENDING_HASH` replaced by C0's sha and every 40-hex token on a
  `Final lane commit` block re-bound to C0 (historic lane hashes do not exist in
  a fixture repo; without the rebind the fixture reads E1 red for the wrong
  reason — measured: ExecC1SuiteBuild's E1 printed `final-lane-commits=4,bound=0`
  on the pre-rebind green). HEAD = C1.

Two green builds of the same `src` agree: `HEAD=0ef3a50a5759243208fa5d818112bb19db4eb5bd
BASE=d540b7cfd38c6c52b2745854e6b888cc16764c3a`.

| fixture | construction | expected |
|---|---|---|
| `fx/green` | C0 + C1 | `closed=9/9 exit=0` |
| `fx/red-E1` | green + every bound hash replaced by `filled by the L1 in the closing commit` | E1 open only |
| `fx/red-E2` | green + `round-34 depth:density row` → `round-34 depth density row` (mean `201.2` still ×6) | E2 open only |
| `fx/red-E3` | green + the `\| r35-defect-closure.sh \| …` row deleted (r36 row intact) | E3 open only |
| `fx/red-E4` | green + `wave1-results.json.provenance.md` deleted | E4 open only |
| `fx/red-E5` | green + `claims-erratum-d5.md` deleted | E5 open only |
| `fx/red-E6` | green + `Correction (round 35)` → `Correction (round 34)` | E6 open only |
| `fx/red-E7` | green + first `supersedes R22` → `R22 citation unchanged` | E7 open only |
| `fx/red-E8` | green + `corpus/lessons/round-36.md` deleted | E8 open only |
| `fx/red-E9` | green + untracked `.ufo/waves/round-36/wave1/stray.md`, left **uncommitted** (dirtiness *is* the defect) | E9 open only |
| `fx/red-E4b` | green + `wave1-results.json` dropped from the index with `.git/info/exclude` keeping status clean | E4 open only (second E4 limb) |
| `fx/red-E9b` | clean green repo, `<scratch>/stray-seat/` present under the scan root | E9 open only (second E9 limb) |
| `fx/mut-E1a…E8d` | 14 clause mutants (§4) | own check open only |
| `fx/flip-E1` | `red-E1` with the placeholder replaced by the bound hash and committed | `8/9 → 9/9` |

The green fixture is a **fixture**, not a claim about the lane: its registry
rows, round-36 lesson, provenance note and erratum text are fixture-authored so
each limb has bytes to read. What it proves is that the checks discriminate, not
that round 36 has landed those bytes.

## 3. Per-check matrix

Driver: `python3 matrix.py` (builds every fixture from `src`, runs the draft,
parses `E<i> … open=0|1` and `closed=K/9`). `green_exit` is the green fixture's
exit; `others_open` is the number of checks other than the target that read
`open=1` on that same red tree.

| check | red_exit | green_exit | red closed | own_open | others_open | verdict |
|---|---|---|---|---|---|---|
| E1 | 1 | 0 | 8/9 | 1 | none | pass |
| E2 | 1 | 0 | 8/9 | 1 | none | pass |
| E3 | 1 | 0 | 8/9 | 1 | none | pass |
| E4 | 1 | 0 | 8/9 | 1 | none | pass |
| E5 | 1 | 0 | 8/9 | 1 | none | pass |
| E6 | 1 | 0 | 8/9 | 1 | none | pass |
| E7 | 1 | 0 | 8/9 | 1 | none | pass |
| E8 | 1 | 0 | 8/9 | 1 | none | pass |
| E9 | 1 | 0 | 8/9 | 1 | none | pass |
| E4b | 1 | 0 | 8/9 | 1 (E4) | none | pass |
| E9b | 1 | 0 | 8/9 | 1 (E9) | none | pass |

`green closed=9/9 exit=0 opens=none`; `matrix rows=9 failures=0`.
Export-mode controls on the same draft (full `git archive`, lane repo argv):

| ref | meaning | result |
|---|---|---|
| `3266c9937b03062d9bbc2f436e20820115ed179c` | r35 base | `closed=0/9 exit=1` (frozen counting command) |
| `0aee0ef105395a2f1d6ace7eaeef13871bb26988` | r35 judged head | `closed=4/9 exit=1` (<9/9; frozen) |
| `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` | r36 claims-freeze head | `closed=5/9 exit=1` |

failing checks at the r35 judged head: E1 (placeholders=1 — the round-35 section
re-published the D1 prose), E3 (neither exact basename registered), E4
(provenance note absent), E8 (no round-36 lesson), E9 (`dirty_paths=9`: the live
worktree during this wave). The E9 reading in export mode is by design — the
frozen clause is "git status --porcelain empty" *now*, so it can only close at
filing.

Draft `--selftest` from the full tip export
(`--export-ref b47f2cd --selftest`, 15 s):

```
selftest control=green closed=9/9 expected=closed=9/9
selftest case=E1 live=pass fixture=rejected own_open=1 others_closed=8/8 verdict=pass
… (E2…E9 identical shape) …
selftest control=E9b-stray own_open=1 others_open=0
selftest control=E4b-untracked own_open=1 others_open=0
selftest control=fake-summary rejected=1
selftest cases=9 failures=0
```

## 4. Clause matrix — every clause is load-bearing

`python3 clause.py`: each mutant is a fresh green fixture with **one clause**
reopened and committed; the target check must open and the other eight stay
closed (14/14 pass, `clause cases=14 failures=0`).

| mutant | clause reopened | target | exit | closed |
|---|---|---|---|---|
| E1a | placeholder prose appended, hash binding intact | E1 | 1 | 8/9 |
| E1b | `<LANE_HASH>` token appended | E1 | 1 | 8/9 |
| E1c | bound hash → 40×`f` (object absent) | E1 | 1 | 8/9 |
| E1d | bound hash → `git commit-tree` orphan (object present, not an ancestor) | E1 | 1 | 8/9 |
| E2b | erratum row present, `201.2` removed (→`twelve`) | E2 | 1 | 8/9 |
| E3b | r36 row absent, r35 row present | E3 | 1 | 8/9 |
| E3c | **both rows absent, both basenames left in prose** (mention control) | E3 | 1 | 8/9 |
| E5b | `discriminating invocation` removed | E5 | 1 | 8/9 |
| E5c | `per-id occurrences` removed | E5 | 1 | 8/9 |
| E6b | correction kept, stale `did not file a receipt (dead seat` restored | E6 | 1 | 8/9 |
| E7b | `supersedes R23` removed, R22 kept | E7 | 1 | 8/9 |
| E8b | `false evidence` marker removed from the lesson | E8 | 1 | 8/9 |
| E8c | corrected line (`source-recheck exit 0 on committed bytes`) no longer named | E8 | 1 | 8/9 |
| E8d | measured pair `+10/0` removed | E8 | 1 | 8/9 |

## 5. Killing the checker (non-vacuity beyond the fixtures)

`python3 suitemut.py` mutates the *draft suite* and requires the draft's own
selftest to notice (`suitemut cases=4 failures=0`):

| suite mutant | expected | observed |
|---|---|---|
| M1 `c_e3` replaced by `return 0` (always closed) | red-E3 case accepted | exit 1, `case=E3 … own_open=0 … verdict=fail`, `cases=9 failures=1` |
| M2 E9 leftover clause (`left=0`) | stray-scratch control passes wrongly | exit 1, `control=E9b-stray own_open=0`, `cases=9 failures=1` |
| M3 `c_e7` always open | green control cannot read 9/9 | exit 2, `suite problem=green-not-closed closed=8/9` |
| flip | red-E1 with the defect removed | `flip E1 red=8/9 exit=1 -> green=9/9 exit=0` |
| forged summary | `closed=9/9 exit=0` alone must not pass | `control=fake-summary rejected=1` |

So vacuity is detected at three grains: per-check (`own_open` + `others_open`),
per-clause (§4), and per-suite (§5). A suite that cannot fail fails its own
selftest.

## 6. Cross run against ExecC1SuiteBuild's draft (the instrument that lands)

`python3 cross.py` — fixtures driven as lanes (`--lane fx/… --export-ref HEAD
--work <scratch>/sw/<tag> --scratch-root <empty>`), suite sha `9fbdee69…` and
`76273416…` (both give the same table):

| check | red_exit | green_exit | red closed | own_closed | others_open |
|---|---|---|---|---|---|
| E1…E9 (each) | 1 | 0 | 8/9 | 0 | none |

`cross green closed=9/9 exit=0 open=none`, `cross rows=9 failures=0`; second
limbs `cross E4b own_closed=0`, `cross E9b own_closed=0`, others closed. Every
one of my nine red fixtures discriminates against **their** checks, independently
of my draft.

Clause mutants through their suite (`crossclause cases=14`): caught 9/14.
Not caught, with the reading I sent them mid-wave:

| mutant | their reading | assessment |
|---|---|---|
| E3c | closed (was: prose mention satisfied both counts) | **fixed during the wave** — E3 rows are now scoped to a Gates & probes registry section and anchored to the first table column (not just `^\| *basename *\|`), and the section-scoped form still finds my fixture's registry block (green 9/9 at `76273416…`), so re-running catches E3c at both later digests |
| E8c | closed (was: E8 bound on `M36` rows + absence in round-35.md) | **fixed during the wave** — E8 now also requires `source-recheck` named in the round-36 lesson plus a present round-35 lesson, and catches E8c |
| E8b | closed | **survivor at `76273416…`** (measured after ExecC1SuiteBuild reported it fixed): `names-corrected-line=1` because the mutant leaves the word `source-recheck` in place, `closed=9/9 exit=0`. E8 binds "a correction is named", not "what was corrected" — either add `false[- ]evidence` and `+10/0` limbs on the round-36 lesson, or list it as a documented survivor |
| E8d | closed | **survivor at `76273416…`**, same root cause (`names-corrected-line=1`, suite 9/9) |
| E5b, E5c | closed | beyond frozen wording: C1 says "claims-erratum-d5.md present", so presence-only is conformant; my E5 keeps round-35's D5 statement clauses |
| E6b | closed | beyond frozen wording: C1 says "has 'Correction (round 35)'"; my E6 also requires the stale dead-seat sentence gone (round-35 D6) |

No fixture of mine proves a *frozen* clause that their suite misses other than
the two it fixed mid-wave; the residuals are either beyond the frozen text or
survivors of the E8 wording (E8b, E8d — reported to them with payloads after
they reported those fixed; the claim did not hold at `76273416…`).

One harness defect found while cross-running, reported and low severity: a
**relative `--lane`** silently makes E1 read `final-lane-commits=1,bound=0`.
E1 evaluates `git -C "$LANE" cat-file -e` inside a `( cd "$tree" … )` subshell,
so a relative lane path resolves against the export tree and the hash looks
unresolvable — a false red on a tree that is fine with an absolute `--lane`.
Fix is one line in `prepare_export` (`LANE=$(cd "$LANE" && pwd -P)`).

**Final digest, cross-run done.** ExecC1SuiteBuild's last revision,
`4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 lines,
39,022 B), was extracted from their receipt
(`awk '/^## Draft text \(verbatim, sha256/{f=1;next} f&&/^```bash$/{g=1;next}
g&&/^```$/{exit} g' .ufo/waves/round-36/wave1/ExecC1SuiteBuild.md`), sha256
verified, `bash -n` clean, and driven with this seat's fixtures. Results:

- green `closed=9/9 exit=0`, `open=none`;
- E1, E3, E4, E5, E6, E7, E8, E9: red_exit=1, closed=8/9, own check closed=0,
  **others closed** — unchanged from `76273416…`;
- E4b and E9b second limbs: own check closed=0, others closed;
- clause mutants caught 10/14; survivors E5b, E5c, E6b, E8b, E8d — exactly the
  set their receipt records in its documented-limits block, all outside the
  frozen limbs (E5 presence, E6 marker, E8 "what was corrected");
- **one adapter note, not a defect**: my per-check red-E2 fixture (deletes the
  `round-34 depth:density row` anchor) no longer corresponds to their E2, which
  now binds `Erratum (round 35)` + a `| depth:density | 9 | mean **201.2**` row
  + `201.2`. Re-expressed against those three clauses the check still
  discriminates each of them alone, with the other eight closed:

  | E2 variant | E2 payload | exit |
  |---|---|---|
  | marker `Erratum (round 35)` → `(round 34)` | `erratum-marker=0,erratum-row=1,erratum-mean=6` | 1 |
  | row value `mean **201.2**` → `mean 201.7` | `erratum-marker=1,erratum-row=0,erratum-mean=6` | 1 |
  | all `201.2` → `twelve` (clause mutant E2b) | `erratum-marker=1,erratum-row=0,erratum-mean=0` | 1 |

  So no frozen-limb survivor remains at the final digest; the residual 5/14
  clause mutants are the dimensions their documented limits name.

**The appendix generator is executable, not just documentary.** After this
seat's scratch was deleted, `r36-fixture-gen.py` was restored by extracting the
fenced block from this receipt; its sha256 came back
`474a27eef6d8e310bb8cfbdfc750d8538351d1c78d2b0c466860c76f1b0e973c` and a fresh
`green` build reproduced `HEAD=0ef3a50a5759243208fa5d818112bb19db4eb5bd
BASE=d540b7cfd38c6c52b2745854e6b888cc16764c3a` exactly, so the fixtures can be
regenerated from the receipt alone.

## 7. Risks and limits

- **E9 in export mode reads live state.** Worktree cleanliness, scratch
  leftovers and (in their suite) `HEAD == export ref` cannot be evaluated from
  export bytes; during a wave they read open by construction. My fixtures prove
  the clause discriminates, not that the lane is quiescent — that is a filing-
  time reading.
- **Green fixtures are normalised, not real.** Registry rows, round-36 lesson,
  provenance note and erratum text are fixture-authored. They prove the checks
  can go red/green; they say nothing about the round-36 lane bytes.
- **My E5/E6/E8 are stricter than the frozen claim.** E5/E6 add round-35's
  statement/stale-sentence clauses; E8 requires the corrected false line to be
  named plus the measured pair. Where the committed instrument keeps the frozen
  wording, my mutants for those clauses are *not* evidence against it (§6).
- **Rebinding.** Historic 40-hex names on `Final lane commit` blocks are rebound
  to the fixture base commit; without it a fixture repo cannot satisfy E1's
  ancestry limb. A fixture that skipped the rebind read E1 red for the wrong
  reason (observed, §2), which is itself a reminder that E1 is only as good as
  the export's object database.
- **Determinism** holds for the same `src` bytes, git version and fixed dates;
  a different git release changes the shas even though the fixture content is
  identical.
- **Scratch is not durable.** The fixture trees are removed at yield. The
  generator below rebuilds them; the driver contracts are in §8. If the round
  wants the trees as evidence, they belong under
  `corpus/instruments/r36-fixtures/` with the generator beside the instrument
  (the r35 pattern), committed by the instrument owner — not by this seat.

## 8. Reproduce

```
S=/fast/scratch/hyaku/kasegi-r36/ExecC1Fixtures        # mkdir -p
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
git -C $L archive b47f2cd -- SCORECARD.md SKILL.md AGENTS.md PROVINCE.md \
  README.md SHONEN.md LOG.md corpus/QUALITY.md 'corpus/lessons/*' \
  .ufo/waves/round-34/wave1/L1Integration.md \
  .ufo/waves/round-35/wave1-results.json \
  .ufo/waves/round-35/claims-erratum-d5.md | tar -x -C $S/src
python3 $S/r36-fixture-gen.py green $S/src $S/fx/green     # HEAD=0ef3a50… BASE=d540b7c…
python3 $S/r36-fixture-gen.py red   $S/src $S/fx/red-E3 E3
KASEGI_R36_SCRATCH=$S/scratch-empty bash $S/r36-closure.sh --root $S/fx/red-E3 --gitroot $S/fx/red-E3
# -> E3 … open=1, the other eight open=0, closed=8/9, exit 1
# clause mutant: green, take BASE from its stdout, then
python3 $S/r36-fixture-gen.py mutate $S/fx/mut-E3c E3c <BASE>   # exit 0 only if the checker names the limb
# through ExecC1SuiteBuild's instrument:
bash <their>/r36-closure.sh --lane $S/fx/green --export-ref HEAD \
  --work $S/sw/g --scratch-root $S/scratch-empty           # closed=9/9 exit=0
```

Driver contracts (rewritten in minutes if the scratch is gone): `matrix.py`
builds green + 9 reds + 2 second limbs, parses `open=` and prints the §3 table;
`clause.py` iterates the 14 mutants in §4; `suitemut.py` patches `c_e3`/`c_e9`/
`c_e7` textually and runs `--selftest`, then flips `red-E1`; `cross.py` drives a
foreign suite with `--lane/--export-ref/--work/--scratch-root`.

## Appendix — r36-fixture-gen.py (verbatim, sha256 `474a27ee…`)

```python
#!/usr/bin/env python3
"""r36-fixture-gen.py — fixture git repos for r36-closure.sh (draft, ExecC1Fixtures).

Every fixture is its own git repository inside the caller's scratch directory:
E1 needs an ancestry limb and E4/E9 need a real index. `green` normalises the
tree under test to the round-36 closure state (all nine checks closed); `red`
injects exactly one check's defect and commits it, so the other eight stay
closed and E9 stays clean. Only `red E9` leaves its defect uncommitted —
dirtiness is that defect.

usage:
  r36-fixture-gen.py green  SRC DEST            -> HEAD=<sha> BASE=<sha>
  r36-fixture-gen.py red    SRC DEST E<i>       -> HEAD=<sha> (committed defect)
  r36-fixture-gen.py untrack DEST PATH          -> index-only drop, committed
  r36-fixture-gen.py mutate DEST NAME BASE      -> clause mutant, committed
"""
import os
import re
import shutil
import subprocess
import sys

PLACEHOLDER = "filled by the L1"
# Deterministic commits: the fixture's base hash is then a stable function of the
# source bytes, so a receipt can cite reproducible shas.
FIXED_DATE = "2026-10-26T00:00:00 +0000"
os.environ["GIT_AUTHOR_DATE"] = FIXED_DATE
os.environ["GIT_COMMITTER_DATE"] = FIXED_DATE
LESSON = """# kasegi round 36

## Gate

- **Correction (round 35 verifier spot-check, routed defect 5 — false evidence
  lines).** The round-35 lesson `## Gate` line "source-recheck exit 0 on committed
  bytes" is a false evidence line: at the judged revision `0aee0ef` the S052
  capture was uncommitted, so no committed-bytes recheck could have exited 0.
  The same spot-check measured the `## No-harm` pair at `0aee0ef` as `SKILL.md`
  +10/0 (not +13/0) and `LOG.md` 0/0 (not "0 changed"); the corrected pair
  `+10/0` is recorded here and in the QUALITY row for this round.

## Mistakes

| id | mistake |
|---|---|
| M36-1 | A wave seat committed closure bytes after the driver's `complete` line. |
| M36-2 | A registry row was registered by prose mention, not by a table row. |
| M36-3 | A closure line named a hash the export could not resolve. |
| M36-4 | A do-nothing control was cited as evidence of a live run. |
"""

REGISTRY = """
## Round-36 Gates & probes registry addition (appended 2026-10-26)

| instrument | class | invocation | report | receipt |
|---|---|---|---|---|
| r35-defect-closure.sh | gate\\|probe | `bash corpus/instruments/r35-defect-closure.sh [--root DIR] [--selftest]` | one `D<i> check=... open=0\\|1` line per defect D1-D7, then `closed=K/7 exit=0\\|1`; `--selftest` prints `cases=7 failures=0` | `.ufo/waves/round-35/wave1/ExecClosureSuite.md` |
| r36-closure.sh | gate\\|probe | `bash corpus/instruments/r36-closure.sh --export-ref <hash>` | one `E<i> check=... open=0\\|1` line per check E1-E9, then `closed=K/9 exit=0\\|1`; `--selftest` prints `cases=9 failures=0` | `.ufo/waves/round-36/wave1/ExecC1SuiteBuild.md` |
"""

ERRATUM_D5 = """# round-35 claims erratum — D5

The D5 closure is the discriminating invocation: the base-export run must read
`closed=0/7` while the after-state run reads the per-id occurrences of the two
statement clauses. The per-id occurrences are recorded beside each check line.
"""

PROVENANCE = """# provenance — round-35 wave1-results.json

Generated by the round-35 wave-1 runner from the frozen dispatch
(`.ufo/waves/round-35/wave1-dispatch.json`); committed under the lane identity so
the claims' counters can be re-read from committed bytes.
"""


def sh(*args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("fixture-gen: %s failed (%s): %s" % (args, p.returncode, p.stderr.strip()))
    return p.stdout.strip()


def rd(path):
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as fh:
        return fh.read()


def wr(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
        fh.write(text)


def append_if_missing(path, marker, text):
    cur = rd(path) if os.path.exists(path) else ""
    if marker in cur:
        return
    wr(path, cur + ("\n" if cur and not cur.endswith("\n") else "") + text)


def copy_tree(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".git"), symlinks=True)


def gitinit(dest):
    sh("git", "-c", "init.defaultBranch=main", "init", "-q", dest)
    for k, v in (("user.name", "r36-fixture"), ("user.email", "fixture@r36.invalid"),
                 ("commit.gpgsign", "false")):
        sh("git", "-C", dest, "config", k, v)


def commit(dest, msg):
    sh("git", "-C", dest, "add", "-A")
    sh("git", "-C", dest, "-c", "commit.gpgsign=false", "commit", "-q", "-m", msg)
    return sh("git", "-C", dest, "rev-parse", "HEAD")


def normalise(dest):
    """Bring any tree under test to the round-36 closure state."""
    sc = os.path.join(dest, "SCORECARD.md")
    txt = rd(sc) if os.path.exists(sc) else ""
    txt = txt.replace(PLACEHOLDER, "recorded in the closing commit")
    txt = txt.replace("<LANE_HASH>", "the final lane hash")
    if "round-34 depth:density row" not in txt:
        txt += ("\n## Round-34 depth:density erratum (appended in round 35)\n\n"
                "| round-34 depth:density row | 201.2 | corrected: the stale row read the "
                "pre-correction mean; the corrected mean is 201.2 |\n")
    if "201.2" not in txt:
        txt += "\nDepth:density no-harm guard mean 201.2 (corrected value).\n"
    txt += ("\n## Round 36 — fixture closure section\n\nFrozen claims in "
            "`.ufo/waves/round-36/claims.json`. **Final lane commit:\n`PENDING_HASH`** "
            "(recorded in the closing commit).\n")
    wr(sc, txt)

    sk = os.path.join(dest, "SKILL.md")
    append_if_missing(sk, "| r36-closure.sh |", REGISTRY)
    q = os.path.join(dest, "corpus/QUALITY.md")
    append_if_missing(q, "supersedes R22", "\n| R36 | fixture row | supersedes R22 — corrected citation. |\n")
    append_if_missing(q, "supersedes R23", "\n| R37 | fixture row | supersedes R23 — corrected citation. |\n")
    li = os.path.join(dest, ".ufo/waves/round-34/wave1/L1Integration.md")
    if os.path.exists(li):
        t = rd(li).replace("did not file a receipt (dead seat", "receipt present (dead seat")
        wr(li, t)
        append_if_missing(li, "Correction (round 35)",
                          "\n- Correction (round 35): the dead-seat bullet above was corrected "
                          "in place; the seat filed late, see the round-35 receipts.\n")
    append_if_missing(os.path.join(dest, ".ufo/waves/round-35/claims-erratum-d5.md"),
                      "discriminating invocation", ERRATUM_D5)
    append_if_missing(os.path.join(dest, ".ufo/waves/round-35/wave1-results.json.provenance.md"),
                      "provenance", PROVENANCE)
    lesson = os.path.join(dest, "corpus/lessons/round-36.md")
    if not os.path.exists(lesson):
        wr(lesson, LESSON)
    # The round-35 lesson's false evidence line is corrected at the source in
    # round 36 (the correction quotes it in the round-36 lesson instead), so the
    # stale sentence must no longer read as current evidence there.
    r35 = os.path.join(dest, "corpus/lessons/round-35.md")
    if os.path.exists(r35):
        t = rd(r35).replace("source-recheck exit 0 on committed bytes",
                            "source-recheck recheck (corrected in round 36: false at 0aee0ef)")
        wr(r35, t)


def bind_blocks(path, base):
    """Re-bind every 40-hex token on a `Final lane commit` block to `base`.

    Historical hashes name commits that do not exist in a fixture repository, so
    a fixture would read E1 red for a reason that is not its defect. Rebinding
    makes the fixture's ancestry limb satisfiable by its own base commit while
    keeping the structural shape (one resolvable ancestor name per block).
    """
    lines = rd(path).splitlines(True)
    hex40 = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
    for i, ln in enumerate(lines):
        if "Final lane commit" in ln:
            for j in range(i, min(i + 5, len(lines))):
                lines[j] = hex40.sub(base, lines[j])
    wr(path, "".join(lines))


def green(src, dest):
    copy_tree(src, dest)
    normalise(dest)
    gitinit(dest)
    base = commit(dest, "fixture base C0")
    sc = os.path.join(dest, "SCORECARD.md")
    wr(sc, rd(sc).replace("PENDING_HASH", base))
    bind_blocks(sc, base)
    head = commit(dest, "fixture closure C1 (final lane commit binding)")
    return head, base


def red(src, dest, defect):
    head, base = green(src, dest)
    sc = os.path.join(dest, "SCORECARD.md")
    sk = os.path.join(dest, "SKILL.md")
    q = os.path.join(dest, "corpus/QUALITY.md")
    li = os.path.join(dest, ".ufo/waves/round-34/wave1/L1Integration.md")
    lesson = os.path.join(dest, "corpus/lessons/round-36.md")
    prov = os.path.join(dest, ".ufo/waves/round-35/wave1-results.json.provenance.md")
    d5 = os.path.join(dest, ".ufo/waves/round-35/claims-erratum-d5.md")
    if defect == "E1":
        wr(sc, rd(sc).replace(base, PLACEHOLDER + " in the closing commit"))
    elif defect == "E2":
        wr(sc, rd(sc).replace("round-34 depth:density row", "round-34 depth density row", 1))
    elif defect == "E3":
        lines = [ln for ln in rd(sk).splitlines(True)
                 if not ln.startswith("| r35-defect-closure.sh")]
        wr(sk, "".join(lines))
    elif defect == "E4":
        os.remove(prov)
    elif defect == "E5":
        os.remove(d5)
    elif defect == "E6":
        wr(li, rd(li).replace("Correction (round 35)", "Correction (round 34)"))
    elif defect == "E7":
        wr(q, rd(q).replace("supersedes R22", "R22 citation unchanged", 1))
    elif defect == "E8":
        os.remove(lesson)
    elif defect == "E9":
        wr(os.path.join(dest, ".ufo/waves/round-36/wave1/stray.md"),
           "untracked seat residue left in the worktree (E9 dirty-tree limb)\n")
        return sh("git", "-C", dest, "rev-parse", "HEAD"), base
    else:
        raise SystemExit("fixture-gen: unknown defect %r" % defect)
    head = commit(dest, "fixture defect %s" % defect)
    return head, base


MUTANTS = {}


def mutant(name):
    def deco(fn):
        MUTANTS[name] = fn
        return fn
    return deco


@mutant("E1a")  # placeholder prose added, hash binding intact
def _e1a(d, base):
    sc = os.path.join(d, "SCORECARD.md")
    wr(sc, rd(sc) + "\nThe closing line is filled by the L1 in the closing commit.\n")


@mutant("E1b")  # angle-bracket lane-hash token only
def _e1b(d, base):
    sc = os.path.join(d, "SCORECARD.md")
    wr(sc, rd(sc) + "\nLane hash marker: <LANE_HASH>\n")


@mutant("E1c")  # hash token that does not exist
def _e1c(d, base):
    sc = os.path.join(d, "SCORECARD.md")
    wr(sc, rd(sc).replace(base, "f" * 40))


@mutant("E1d")  # hash exists in the object db but is not an ancestor
def _e1d(d, base):
    sc = os.path.join(d, "SCORECARD.md")
    tree = sh("git", "-C", d, "rev-parse", "HEAD^{tree}")
    orphan = sh("git", "-C", d, "commit-tree", tree, "-m", "orphan fixture commit")
    wr(sc, rd(sc).replace(base, orphan))


@mutant("E2b")  # erratum row present, corrected mean gone
def _e2b(d, base):
    sc = os.path.join(d, "SCORECARD.md")
    wr(sc, rd(sc).replace("201.2", "twelve"))


@mutant("E3b")  # r36 row absent, r35 row present
def _e3b(d, base):
    sk = os.path.join(d, "SKILL.md")
    wr(sk, "".join(ln for ln in rd(sk).splitlines(True) if not ln.startswith("| r36-closure.sh")))


@mutant("E3c")  # both rows absent, both basenames mentioned in prose
def _e3c(d, base):
    sk = os.path.join(d, "SKILL.md")
    keep = [ln for ln in rd(sk).splitlines(True)
            if not ln.startswith("| r35-defect-closure.sh") and not ln.startswith("| r36-closure.sh")]
    wr(sk, "".join(keep) + "\nThe gate later reads r36-closure.sh and r35-defect-closure.sh.\n")


@mutant("E5b")
def _e5b(d, base):
    f = os.path.join(d, ".ufo/waves/round-35/claims-erratum-d5.md")
    wr(f, rd(f).replace("discriminating invocation", "discriminating run"))


@mutant("E5c")
def _e5c(d, base):
    f = os.path.join(d, ".ufo/waves/round-35/claims-erratum-d5.md")
    wr(f, rd(f).replace("per-id occurrences", "per-cell counts"))


@mutant("E6b")  # correction present, stale dead-seat sentence restored
def _e6b(d, base):
    f = os.path.join(d, ".ufo/waves/round-34/wave1/L1Integration.md")
    wr(f, rd(f) + "\n- The seat did not file a receipt (dead seat).\n")


@mutant("E7b")
def _e7b(d, base):
    f = os.path.join(d, "corpus/QUALITY.md")
    wr(f, rd(f).replace("supersedes R23", "R23 citation unchanged"))


@mutant("E8b")
def _e8b(d, base):
    f = os.path.join(d, "corpus/lessons/round-36.md")
    wr(f, rd(f).replace("false evidence", "unverified").replace("false\nevidence", "unverified"))


@mutant("E8c")
def _e8c(d, base):
    f = os.path.join(d, "corpus/lessons/round-36.md")
    wr(f, rd(f).replace("source-recheck exit 0 on committed\n  bytes", "the recheck line")
          .replace("source-recheck exit 0 on committed bytes", "the recheck line"))


@mutant("E8d")
def _e8d(d, base):
    f = os.path.join(d, "corpus/lessons/round-36.md")
    wr(f, rd(f).replace("+10/0", "the corrected byte pair"))


def mutate_tree(dest, name, base):
    if name not in MUTANTS:
        raise SystemExit("fixture-gen: unknown mutant %r" % name)
    MUTANTS[name](dest, base)
    return commit(dest, "clause mutant %s" % name)


def untrack(dest, path):
    # Keep the worktree byte-identical and the repo clean: exclude the path so
    # the only open check is E4's tracking limb.
    excl = os.path.join(dest, ".git/info/exclude")
    with open(excl, "a") as fh:
        fh.write("\n/" + path + "\n")
    sh("git", "-C", dest, "rm", "--cached", "-q", "--", path)
    sh("git", "-C", dest, "-c", "commit.gpgsign=false", "commit", "-q",
       "-m", "fixture index drop %s" % path)
    return sh("git", "-C", dest, "rev-parse", "HEAD")


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    mode = argv[0]
    if mode == "green":
        head, base = green(argv[1], argv[2])
        print("HEAD=%s BASE=%s" % (head, base))
    elif mode == "red":
        head, base = red(argv[1], argv[2], argv[3])
        print("HEAD=%s BASE=%s" % (head, base))
    elif mode == "mutate":
        print("HEAD=%s" % mutate_tree(argv[1], argv[2], argv[3]))
    elif mode == "untrack":
        print("HEAD=%s" % untrack(argv[1], argv[2]))
    else:
        raise SystemExit("fixture-gen: unknown mode %r" % mode)


if __name__ == "__main__":
    main(sys.argv[1:])
```

## What the round should carry

1. The instrument owner should adopt a fixture set of this shape in the suite's
   own `--selftest` (mine synthesises the trees; the r35 pattern commits them
   under `corpus/instruments/r36-fixtures/`). The two clauses I found mid-wave
   (E3 mention-satisfiable, E8 not naming the corrected line) are already fixed
   in their draft; E8 still does not require the false-evidence marker or the
   measured pair — their call, and their documented-limits block should say so
   if they keep it.
2. Per-check isolation must be reported as `own_open` **and** `others_open`: a
   red fixture that also opens the other eight is not evidence about the target.
   My matrix reports both; none of the eleven red trees opens a sibling check.
3. The green control, the clause matrix and the three suite mutants are what
   stop a `closed=9/9 exit=0` summary from being taken on faith. A suite that
   prints the summary without the case lines is rejected by all three.

## Appendix B — draft checker contract (sha256 `4283a9d3…`, 308 lines, scratch only)

The draft itself is not durable (scratch is removed at yield) and it is not the
instrument that lands. This is its exact contract, so the §3–§5 numbers can be
re-derived without the file; `$R` is the export/fixture root, `$G` the git root,
`$REF` the exported ref.

| check | payload fields (in order) | closed iff |
|---|---|---|
| E1 | `placeholders`, `lane_hash_tokens`, `hash`, `hash_exists`, `ancestor` | `grep -c -F 'filled by the L1' $R/SCORECARD.md` = 0 **and** `grep -c -F '<LANE_HASH>'` = 0 **and** the first `[0-9a-f]{7,40}` token on the last case-insensitive `final lane commit` line or the line after it resolves via `git -C $G cat-file -e <h>^{commit}` **and** `git -C $G merge-base --is-ancestor <h> $REF` |
| E2 | `erratum_rows`, `corrected_mean` | `grep -c -F 'round-34 depth:density row' $R/SCORECARD.md` ≥ 1 and `grep -c -F '201.2'` ≥ 1 |
| E3 | `row_r35_defect_closure`, `row_r36_closure` | `grep -cE '^\|[[:space:]]*r35-defect-closure\.sh[[:space:]]*\|' $R/SKILL.md` ≥ 1 and the same for `r36-closure\.sh` (row-anchored, so a mention cannot satisfy it) |
| E4 | `tracked`, `provenance_note` | `git -C $G ls-files -- .ufo/waves/round-35/wave1-results.json \| wc -l` = 1 and `-s $R/.ufo/waves/round-35/wave1-results.json.provenance.md` |
| E5 | `present`, `discriminating_invocation`, `per_id_occurrences` | `-s $R/.ufo/waves/round-35/claims-erratum-d5.md` and both statement greps ≥ 1 inside it |
| E6 | `correction_round_35`, `stale_dead_seat` | `grep -c -F 'Correction (round 35)' $R/.ufo/waves/round-34/wave1/L1Integration.md` ≥ 1 and `grep -c -F 'did not file a receipt (dead seat'` = 0 |
| E7 | `supersedes_R22`, `supersedes_R23` | both ≥ 1 in `$R/corpus/QUALITY.md` |
| E8 | `lesson`, `false_evidence_marker`, `names_false_line`, `measured_pair` | first `$R/corpus/lessons/round-36*.md` exists and, on its newline-flattened text, `grep -ciE 'false[- ]evidence'` ≥ 1, `grep -c -F 'source-recheck exit 0 on committed bytes'` ≥ 1, `grep -c -F '+10/0'` ≥ 1 |
| E9 | `dirty_paths`, `leftover_seat_dirs` | `git -C $G status --porcelain \| wc -l` = 0 and `find ${KASEGI_R36_SCRATCH:-/fast/scratch/hyaku/kasegi-r36} -mindepth 1 -maxdepth 1 -type d \| wc -l` = 0 |

Plain runner: `E<i> check=<payload> open=0|1` × 9, then `closed=K/9 exit=0|1`;
the report is re-parsed (`plain_ok`: exactly nine distinct `E<i> check=` lines
ending `open=0|1`, summary equals the open-line count) so a bare summary line
cannot pass. `--selftest` builds `green`, `red-E<i>` for each i, the E9b stray
control, the E4b untracked control and the forged-summary control from the tree
under test (via the appendix-A generator), requires `live=pass
fixture=rejected own_open=1 others_closed=8/8` per case, and prints
`selftest cases=9 failures=N`; exit 2 if the green control cannot read 9/9.
`--export-ref` archives into `mktemp -d ${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}` and
removes it on exit; the only git writes are `init/add/commit` inside fixture
directories whose paths are under that scratch base.
