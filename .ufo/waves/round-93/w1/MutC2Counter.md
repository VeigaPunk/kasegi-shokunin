# MutC2Counter — round-93 C2 mutation probe

Seat: mutation-tester, one v1 wave, 13 seats. Lane workdir
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch
`/fast/scratch/hyaku/kasegi-r93/MutC2Counter` (removed at seat exit; nothing of
this seat lives outside it and the receipt/report paths below).

Frozen identity re-read and re-hashed at measurement time, not trusted from the spec:

| item | frozen value | observed |
|---|---|---|
| base | e15996bfd2f6eca4af39507a7c5973afbeca8347 | — (not needed: K2/K6 read their own revs) |
| freeze | 5bad9e55d3d9319446e3d9b63bc2dece633cdb68 | — |
| C2 landing | 9225954a6e3f177af46bdb9d811c062a4353a552 | `git rev-parse HEAD` of the clone = same |
| counter | 8a4ad5081cb21d9afb80e83f490b51df2e3a7fb6211a4e9e91a69c456d751bb6 | equal |
| candidate / landed scanner | 7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5 | equal (both `.ufo/.../candidate-…` and `corpus/instruments/capture-secret-scan.py`) |
| gate | 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 | equal |
| P3 path set of the landing | `corpus/instruments/capture-secret-scan.py`, `SCORECARD.md` | `git diff-tree --no-commit-id --name-only -r 9225954a` = exactly those two |

## Method

Every probe is run by the frozen counter itself, unmodified, invoked with
`--lane <clone>` against a **fresh clone** of the lane at the landing
(`git clone -q --shared`, `rev-parse --show-toplevel` == the clone before the first
fixture commit; every mutant clone differs from HEAD in exactly one path,
`corpus/instruments/capture-secret-scan.py`). Each forged instrument is built from
the pristine landed bytes by a generator whose every textual patch asserts the
anchor occurs exactly once (`forge-gen.py`), and each forged instrument passes its
own `--selftest` (rc 0, except F6, which is the point of F6). "pinned" = the frozen
predicate's own command (`--instrument-sha256 7d9d… --gate-sha256 8b6f…`),
"unpinned" = the same counter with the two pin flags removed — the only way a
forged instrument can reach the behavioural limbs K2–K8 rather than being stopped
by K1's hash.

### Baseline (pristine candidate, before any mutant)

| run | rc | verdict |
|---|---|---|
| pinned, seed 1 | 0 | `CAPABILITY-CHECK-RESULT pass` |
| unpinned, seed 1 | 0 | pass |
| pinned, seed 9191 | 0 | pass |
| unpinned, seed 9191 | 0 | pass |
| pinned, no `--seed` (printed run-time seed 2602165834, nonce 29a6a37e) | 0 | pass, K1–K8 pass |

A baseline failure would have made the whole wave inconclusive; it did not occur.

## Forgeries (7 of my own) and what killed them

All shas are of the forged `capture-secret-scan.py` actually placed in the clone.

| # | forgery (defect) | sha256 | own selftest | unpinned seed 1 | unpinned seed 9191 | rejecting limb(s) |
|---|---|---|---|---|---|---|
| F1 | exact-path table over the fixed K4 plant paths (round-92-style fixed paths; real `gitlab-pat` and escape-left-boundary detection removed) | 2da1f6e2…5013c1f1 | pass (68 cases) | fail | fail | **K4** (9 missing: S035–S039, live-k/l/m, E6 — all nonce-renamed), **K7** (3 missing), **K8** (9 clauses) |
| F2 | detector gated on the harness's own tempdir name (`plant-`/`gen-`/`c2check-`): full detection inside the harness, blind outside | 358f1821…7622cf | pass (68) | **pass** | **pass** | none unpinned → **SURVIVOR**; pinned: K1 only |
| F3 | `glpat-` + any ≥3 characters | 87c684cf…1bed9400 | pass (68) | fail | fail | **K4** (extra S040 19-char, S041 21-char), **K7** (extra live-n12/n13), **K8** (2 clauses) |
| F4 | escape-terminator kept, `gh[pousr]_` tail widened to 3–36 | 0b23b9b8…110e8c04f | pass (88) | fail | fail | **K3** (4 spurious hits on the lane), **K4** (extra S027 bare prefix, S028 35-char, S051 `-` in tail), **K7** (extra live-n8), **K8** (3 clauses) |
| F5 | new-class patterns replaced by the K4 plant literals read out of the counter's own committed source (`.ufo/waves/round-93/c2/capability-check.py`) | 0e091586…caa7cf | pass (68) | fail | fail | **K4** (missing S025, S050), **K7** (missing live-g7/8/9/10/11/12), **K8** (2 clauses) |
| F6 | candidate detection untouched, instrument's own `--selftest` gutted (`SELFTEST-RESULT pass cases=0`) | 6778331a…c70379e | pass (cases=0, fake) | **pass** | **pass** | none unpinned → **SURVIVOR**; pinned: K1 only |
| F7 | nonce-stable **suffix** table over the plant paths (reroot inserts a directory, it does not rename anything else); real new-class detection removed | c241f91e…aad8e1 | pass (68) | **pass** | **pass** | none unpinned → **SURVIVOR**; pinned: K1 only |

8 (F1) and 7 (F7) were checked against the lane tree first: no capture path in the
landing ends with any of the tabled suffixes (`…/round-1/S0{35..50}.txt`,
`…/t-receipts/live-{k,l,m}.json`, `…/evidence/E6.txt`, `…/x-receipts/live-g1{0,1,2}.*`),
so K3 stays clean for them by construction, not by luck of this run.

## Verdict

**forged=7 rejected=4 survivors=3.**

- Rejected unpinned at both seeds: F1, F3, F4, F5 (F1/F3/F5 by K4+K7+K8, F4 also by K3).
- Survivors unpinned at both seeds: **F2** (harness-name gating), **F6** (gutted selftest),
  **F7** (suffix-keyed). All three are rejected only by **K1**, and only because the
  pin flag is supplied: with the pins removed the counter prints
  `CAPABILITY-CHECK-RESULT pass rc=0` for each.

This is a coverage finding about the counter's adversarial breadth, not a re-score of
C2. The frozen C2 predicate is measured, not inferred: P1 passes at seeds 1 and 9191
and at a printed run-time seed with both sha pins; P2 holds (candidate = landed =
frozen sha); P3 holds (exactly two landed paths). C2's claim therefore STANDS on its
own predicate; the three survivors are routed qualifiers (D1–D3 below) for the
counter's next round. C1 was not probed by this seat.

## Routed defects / qualifiers (not verdict changes)

**D1 — K1 is the only defence against harness-name gating (F2).** The counter runs the
candidate instrument exactly twice per run: on the lane (K3, which contains no
gitlab/escape secret) and inside throwaway repos whose tempdir names are the
fixed prefixes `plant-` and `gen-` (`tempfile.mkdtemp(prefix=…)` via `make_repo`).
A scanner that enables its real new-class patterns only when
`os.path.basename(toplevel)` starts with those names passes K1–K8 unpinned. Nothing
in K2–K8 ever exercises the candidate on a non-harness repository that contains a
`glpat-` value or an escape-terminated GitHub token.

**D2 — K1's selftest leg is self-attested (F6).** `run_instr(inst, "--selftest")`
trusts the instrument to run its own cases; a `selftest()` that prints
`SELFTEST-RESULT pass cases=0` satisfies it. Only `--instrument-sha256` separates
F6 from the candidate. The pin is an out-of-band value from the claim author, so
this is a property of every unpinned run, including the `do_nothing` and forgery
controls in `c2-controls-r93.txt`.

**D3 — the nonce covers directories only (F7).** `reroot()` inserts
`r<n>/`, `p<n>/`, `n<n>/`, `w/n<n>/` and leaves every basename and every later
segment byte-identical; the K4 plant paths are fixed literals in the counter source,
which is committed in the same repository the instrument is read from. A detector
keyed on the suffix `…/round-1/S035.txt` (or on the whole suffix list) passes K4,
K7 and K8 without detecting either new class. The K7 plant paths are not rerooted
at all — `g/x-receipts/live-g{10,11,12}.*` are the same literal paths at every seed
and every nonce.

**D4 — K4's literals are readable by the instrument under test (F5).** The counter,
its `PLANTS` dict and the fixed `GLP`/`GHT` fixture values are committed at
`.ufo/waves/round-93/c2/capability-check.py`, i.e. readable from inside the clone the
instrument runs in. F5 extracts them at import and keys only on those literals; it is
killed by K4's U5 control (S050, a 20+20 tail that is not the fixture literal) and by
K7's run-time-drawn values. So the counter's defence here is the *value* randomness in
K7 plus the U5 control, not the secrecy of K4's values.

**Observation, not defect.** F4's widening also trips K3 on the real lane corpus
(4 spurious `github-token` hits), and F3's widened length trips both K4 boundaries —
the boundary and scope plants do carry discriminating power once the detector is
actually too broad; the survivors are the ones that are correctly narrow and merely
keyed on where they run.

## Counter nondeterminism probes

From `nondeterminism-probe.txt` (imports the frozen counter read-only; no plants written):

- P1: 76 K4 plants; reroot renames 76 of 76; paths without the nonce: none.
- P2: basenames changed by reroot: 0 (reroot is shown to be directory-only).
- P3: `w/t-receipts/live-k.json` → `w/ndeadbeef/t-receipts/live-k.json` (sample).
- P4: 27 K7 plants; 0 contain any nonce; 27/27 paths identical across seeds 1 and 9191.
- P5: K7 plant *values* differ per seed (plants_equal=False), expected sets equal.
- P6/P7: own work dir `c2check-…`; fixed children `inst`, `base-inst`,
  `plant-allow.tsv`, `plant-allow-sts.tsv`; fixture repos `plant-…` (K4), `gen-…` (K7).
- P8: `nonce = os.urandom(4).hex()` (32-bit, per run).
- P9/P10: seed = `--seed` else `int.from_bytes(os.urandom(4), "big")`; printed twice
  (header `seed=… nonce=…`, and `LIMB K7 … seed=…`). Confirmed in every receipt:
  the header line carries the printed seed, and the four baseline runs carry four
  distinct nonces (`e13e4318`, `43fd15da`, `61010964`, `d780d633`).
- Run-output grep: in F1's failing run every one of the 9 missing plant paths found by
  the counter carries that run's nonce (`nonce-grep.txt`); the pass runs print the
  nonce in `LIMB K4` with `missing=none`, so the nonce reaches all plants the counter
  checks, and reaches none of the K7 plants (P4).

## Receipts

All under `.ufo/waves/round-93/w1/MutC2Counter-receipts/`; seed/nonce lines below are
copied from those files.

1. `git clone -q --shared <lane> /fast/scratch/…/lane && git -C lane rev-parse HEAD --show-toplevel`
   → rc 0, `9225954a6e3f177af46bdb9d811c062a4353a552`, toplevel = clone; `git status --porcelain` empty.
2. `sha256sum .ufo/…/c2/capability-check.py corpus/instruments/capture-secret-scan.py corpus/instruments/claim-package-check.py`
   → rc 0, `8a4ad508…1bb6`, `7d9d7309…83c5`, `8b6f8493…c8e6`.
3. `sh run-matrix.sh <clone> BASELINE-candidate` → 4/4 rc 0:
   `BASELINE-candidate pinned seed=1 rc=0`, `unpinned seed=1 rc=0`,
   `pinned seed=9191 rc=0`, `unpinned seed=9191 rc=0`, each
   `CAPABILITY-CHECK-RESULT pass rc=0`; 8 limbs each, none failing.
4. `capability-check.py --lane <clone> --rev 9225954a… --work … --instrument-sha256 7d9d… --gate-sha256 8b6f…` (no `--seed`)
   → rc 0, `CAPABILITY-CHECK … seed=2602165834 nonce=29a6a37e`, `LIMB K7 pass seed=2602165834 rc=1`, `CAPABILITY-CHECK-RESULT pass rc=0`.
5. `python3 -B forge-gen.py` → rc 0, 7 mutants, one-path diffs, own selftest rc 0
   (F6 `SELFTEST-RESULT pass cases=0`; F4 88 cases; others 68).
6. `sh run-matrix.sh <mutant> <name>` × 7 → 28 runs; `matrix-summary.txt` lists
   per-file verdict and failing limbs (F1 pinned K1,K4,K7,K8 / unpinned K4,K7,K8;
   F2 pinned K1 / unpinned pass; F3 same shape as F1; F4 pinned K1,K3,K4,K7,K8 /
   unpinned K3,K4,K7,K8; F5 pinned K1,K4,K7,K8 / unpinned K4,K7,K8;
   F6 pinned K1 / unpinned pass; F7 pinned K1 / unpinned pass).
7. `python3 -B nondet-probe.py` → rc 0, P1–P13 as above.
8. `grep -H -oE "…seed=… nonce=…" receipts/*-seed*.txt` → 32 header lines, every run
   prints its seed and a fresh nonce; `grep -c <nonce> F1-pathkey-unpinned-seed1.txt`
   → 9 nonce-bearing missing plant paths (nonce-grep.txt).
9. `grep -E "^LIMB|^CAPABILITY" F2/F5/F7-unpinned-seed1.txt` and
   `grep -h "^LIMB K1" F2/F6/F7-pinned-seed1.txt` → survivor limbs (survivors-and-limb-detail.txt);
   pinned K1 lines show `instrument_sha256=358f…/6778…/c241…` against pin `7d9d…`.
10. `git diff-tree --no-commit-id --name-only -r 9225954a` → `SCORECARD.md`,
    `corpus/instruments/capture-secret-scan.py`; `git status --porcelain` on the lane
    → 18 concurrent-seat lines (none written by this seat; the receipts dir is the
    untracked `w1/` path this seat was given); `sha256sum` of the candidate and the
    landed scanner both `7d9d…83c5` after all probes
    (restoration-and-freeze-evidence.txt).

11. Preserved with the receipts: `forge-gen.py` (mutant generator; every anchor patch
    asserts a single occurrence), `run-matrix.sh` (the pinned/unpinned × two-seed
    driver), `nondet-probe.py`. Re-running the generator from a fresh clone at the
    landing reproduces all seven mutant sha256 **exactly** (7/7 MATCH;
    mutant-rebuild-repro.txt, mutant-rebuild-check.txt), and re-running the probe
    reproduces nondeterminism-probe.txt byte-identically.
12. Teardown: `files_before_rm=140412`, `rm -rf -- /fast/scratch/hyaku/kasegi-r93/MutC2Counter`,
    `scratch_after_rm_exists=no`; receipts dir = 44 files.

Restoration: no lane or sibling file was edited; the only writes are this report and
the receipts directory. The instrument under test was never modified in place — every
mutant is a separate clone in scratch. Scratch teardown:
`rm -rf -- /fast/scratch/hyaku/kasegi-r93/MutC2Counter` at seat exit.
