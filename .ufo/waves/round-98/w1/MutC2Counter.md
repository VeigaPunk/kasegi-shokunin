# MutC2Counter — round-98 C2 mutation probe

Seat: MutC2Counter (leaf; no subagent dispatch). Read-only attacker on the lane repo.
Target: `corpus/instruments/capture-secret-scan.py` at the C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`,
sha256 `45f8d226b65e5bf16b9323bfc246c2748319713af5740a608838d6a6eb6f9f0e` (equals the claim's `instrument_sha256`).
Gate under test: `.ufo/waves/round-98/c2/capability-check.py`, sha256
`a0c4b952812269f2d01771fe6d4ff5ae577fa877ff48b5e21206ae5220b21c15` (equals the claim's `counter_sha256`).

Fixture: `git clone --shared` of the lane at `/fast/scratch/hyaku/kasegi-r98/MutC2Counter/lane`,
`git -C <clone> checkout e2caf4a...`, `git -C <clone> rev-parse --show-toplevel` printed the clone path before
the first commit; final `git -C <clone> status --porcelain` printed nothing and HEAD was back at `e2caf4a...`.

## Detectors

* **D1 `--selftest`** — `python3 -B <instrument> --selftest`; killed iff rc != 0 (the instrument prints
  `SELFTEST-RESULT pass|fail cases=170`).
* **D2 K3 plants** — the gate's own plant builder, imported from the landed gate:
  `importlib` load of `.ufo/waves/round-98/c2/capability-check.py`, `build_plants(work, seed)`, then
  `python3 -B <instrument> --files <plant paths>` and `(basename, shape)` set equality with the
  `PLANT_SPEC`-derived `expect` set (9 positives, 10 negatives). Killed iff the set differs.
  This is the gate's K3 limb verbatim: the gate's `run_instr`/`HIT` regex and `build_plants` are reused,
  not re-implemented.

Baseline on pristine bytes (both seeds, `results-20261107.json` / `results-424242.json`):

```
baseline A: pass 170 k3 hits 9 True
baseline B: pass 170 k3 hits 9 True
plant rev A 9bb678b824af63b029be4bbf45af5b2c64eee996   B 0909aee6f6134868c7ebcc9ef092725bcddd3f6e   files 19 19
pristine==final A True   B True
```

Gate cross-check on the same pristine bytes (`--rev e2caf4a... --seed 20261107`, both sha pins supplied):

```
LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=170
LIMB K2 ok rc=0 scanned=3280 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K7 ok base_widened_hits=0 landing_widened_hits=5 missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
```

The gate's K3 limb and D2 agree on pristine bytes (`hits=9 missing=none extra=none`), so D2 is the gate's detector.

## Mutants

17 single-point mutants, each a one-occurrence string replacement on the pristine file (the harness asserts
`text.count(old) == 1` before applying). M01–M13 are the seat's required list; M14–M17 are supplementary
coverage probes. Full table with per-mutant sha256, selftest failing cases and K3 missing/extra sets:
`MutC2Counter-receipts/mutants.tsv`; raw stdout per mutant: `MutC2Counter-receipts/raw/<id>.{selftest,k3}.txt`.

| id | mutation (landed point) | D1 selftest | D2 K3 | verdict | asymmetry |
|---|---|---|---|---|---|
| M01 | drop `gitlab-ci-build-token` (302-303) | rc1, `gl-ci-build->none` | missing p1 | killed | both |
| M02 | drop `gitlab-iam-refresh-token` (304-305) | rc1, `gl-iam-refresh->none` | missing p2 | killed | both |
| M03 | drop `gitlab-iam-authorization-code` (306-307) | rc1, `gl-iam-auth-code->none` | missing p3 | killed | both |
| M04 | drop `gitlab-session-cookie` (308-310) | rc1, 3 cookie positives lost | missing p4 | killed | both |
| M05 | registration `(?![A-Za-z0-9])`→`(?![A-Za-z0-9_-])` (311-312) | rc1, both right-boundary cases lost | missing p5 | killed | both |
| M06 | feed-token boundary narrowed (313-314) | rc1, `gl-feed-token-right-underscore->none` | missing p6 | killed | both |
| M07 | oauth-app boundary narrowed (315-316) | rc1, `gl-oauth-app-right-hyphen->none` | missing p7 | killed | both |
| M08 | feed-token-v2 boundary narrowed (317-318) | rc1, `gl-feed-token-v2-right-underscore->none` | missing p8 | killed | both |
| M09 | scim boundary narrowed (321-322) | rc1, `gl-scim-oauth-right-hyphen->none` | missing p9 | killed | both |
| M10 | drop `_gitlab_session` keyword (308-310) | rc1, 3 cookie positives lost | missing p4 | killed | both |
| M11 | `gliamrt-…{43}`→`{42}` (304-305) | rc1, `gl-iam-refresh->none`, `gl-iam-refresh-short->hit` | missing p2 **and extra n2** | killed | both |
| M12 | drop `_` in ci-build grammar (302-303) | rc1, 5 cases (incl. `gl-jwt-clcbt` now double-hits) | missing p1 | killed | both |
| M13 | session value `[0-9a-f]{64}`→`[0-9a-fA-F]{64}` (308-310) | rc1, `gl-session-cookie-upper->gitlab-session-cookie` | **ok, 9/9** | killed | **selftest-only** |
| M14* | ci-build boundary `(?![A-Za-z0-9])`→`(?![A-Za-z0-9_-])` (302-303) | **rc0, pass 170** | **ok, 9/9** | **SURVIVED** | **neither** |
| M15* | `gliamac-…{43}`→`{44}` (306-307) | rc1, `gl-iam-auth-code-44->hit` | missing p3 | killed | both |
| M16* | `_gitlab_session…` made optional (308-310) | **rc0, pass 170** | **ok, 9/9** | **SURVIVED** | **neither** |
| M17* | registration `{20}`→`{20,21}` (311-312) | **rc0, pass 170** | **extra n5** | killed | **K3-only** |

`*` = supplementary probe, not on the required list. Line numbers are the landed instrument's; the exact
mutated text is in `MutC2Counter-receipts/harness.py` (`MUTANTS`).

Seed stability: the full 17-mutant matrix was run twice, seed `20261107` and seed `424242`; every verdict and
asymmetry label is identical (`mutants.tsv` column `seed_agree=yes` for all 17). The survivors are
seed-independent by construction (see G1/G3 below), not seed luck.

Restoration: after every mutant the harness rewrote the pristine bytes and re-hashed; `restored==pristine`
is `yes` for all 17 rows, and `final_sha256` equals `45f8d226…` for both seeds (`hashes.txt`).

## What the required list shows

All 13 required mutants are killed. 12 are killed by both detectors; M13 is killed by the selftest only.
The four drop-shape mutants are caught twice each (positive case + missing plant), the five boundary
narrowings are caught twice each (the round-97 `_`/`-` cases + the p5–p9 plants), and the two grammar/length
mutants are caught twice each. M11 is caught by both a lost positive and a new negative hit (n2 becomes a
hit), which is the strongest form.

## Coverage findings (named)

### G1 — the new `gitlab-ci-build-token` right boundary is untested by both detectors (M14 survives the whole gate)

Landed point: `corpus/instruments/capture-secret-scan.py:302-303`

```python
    ("gitlab-ci-build-token", re.compile(
        _GL_LB + rb"glcbt-[A-Za-z0-9]{1,5}_[A-Za-z0-9_-]{20}(?![A-Za-z0-9])")),
```

Narrowing that boundary to `(?![A-Za-z0-9_-])` — the exact defect the claim fixes for the five round-97
shapes, and the change a future editor would most plausibly make to "match" them — leaves both detectors
green. Differential probe (`probe.py`, payload `glcbt-Ab3_` + 20×`k` + `_x`):

```
PRISTINE                       B-ci-build-then-underscore   rc=1 gitlab-ci-build-token
M14-narrow-ci-build-boundary   B-ci-build-then-underscore   rc=0 none
```

The mutant refuses a real ci-build token followed by `_` (a punct character S140's own boundary allows) and
neither detector notices. Cause: the selftest has no `glcbt-…`+`_`/`-` case (cases at
`capture-secret-scan.py:618-622` cover prefix length 6, missing `_`, short tail, right-alnum only), and K3's
p1 plant ends with ` end` (`capability-check.py:140-141`), so the right boundary is never exercised. At gate
level the mutant is not just a K3 miss — the **whole gate passes it**:

```
=== M14-narrow-ci-build-boundary rev=894f82fe6b61db630bb747cc84dd1bec8157a4b6
LIMB K1 ok selftest=pass cases=170
LIMB K2 ok rc=0 scanned=3280 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K7 ok base_widened_hits=0 landing_widened_hits=5 missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
```

That is the C2 gate certifying an instrument that reintroduces the round-97 boundary defect on one of the
four new shapes. The claim's K3 sentence "the ten boundary negatives produce no hit" is true but does not
cover this boundary: n1 is a prefix-length negative, not a right-boundary negative.

### G2 — session value case-class is selftest-only (M13)

`M13` (value class `[0-9a-f]`→`[0-9a-fA-F]`) is killed by the selftest (`gl-session-cookie-upper`) and
**not** by K3: K3 has no upper-case session plant and its only session negative is 63 lower-case hex (n4).
Gate-level the mutant is still stopped by K1:

```
LIMB K1 FAIL selftest=rc1 cases=none
LIMB K3 ok rc=1 hits=9 missing=none extra=none
CAPABILITY-CHECK-RESULT fail rc=1
```

So the gate is safe here, but the K3 limb alone would certify a scanner that fires on non-tokens. Differential
probe: `_gitlab_session=` + 64 upper-case hex → pristine rc=0, M13 rc=1 `gitlab-session-cookie`.

### G3 — the session-cookie *context requirement* is not tested by K3 (M16; K2 is the only kill)

`M16` makes the `_gitlab_session` keyword optional while keeping the separator class. Both listed detectors
stay green (`selftest pass 170`, `K3 ok 9/9`), and the differential probe shows the false positive the claim
says the context prevents. The literal drop (M10) is killed by both detectors, but only because it also stops
matching real cookies (missing p4, three positives lost) — not because either detector tests the context
requirement:

```
M16-optional-session-context   A-sep-hex-no-keyword       rc=1 gitlab-session-cookie
PRISTINE                       A-sep-hex-no-keyword       rc=0 none
```

K3's n10 negative is a bare 64-hex line with no separator, so it is blocked by `_GL_LB`/`[\s"'=:;]+`, not by
the keyword; the selftest's `gl-session-cookie-no-context` is `x=<hex>`, blocked by the left boundary for the
same reason. The gate only survives this mutant because **K2** scans the whole lane tree and finds 321 false
positives:

```
=== M16-optional-session-context
LIMB K1 ok selftest=pass cases=170
LIMB K2 FAIL rc=1 scanned=3280 hits=321 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential,gitlab-session-cookie
CAPABILITY-CHECK-RESULT fail rc=1
```

(321 hits, all `gitlab-session-cookie`, e.g. `.ufo/waves/round-25/c1-controls/live-lane.json:24`,
`.ufo/waves/round-81/w1/MutCounter-receipts/mutants.json:9` — sha256 digests preceded by a separator.)
The context requirement is load-bearing; the K3 plant set just does not test it. The gate's plant-set comment ("negatives: one
boundary defect per new shape") is not met for the session cookie: its negative is a length negative.

### G4 — registration length widening is K3-only (M17)

`{20}`→`{20,21}` passes the selftest (no 21-character negative exists; `gl-registration-short` is 19) and is
killed by K3 (n5 becomes a hit) and by K2 (one 21-character `GR1348941…` fixture value at
`.ufo/waves/round-97/w1/ExecC2Probe-receipts/fixture-bytes.txt:5`):

```
=== M17-registration-20-to-21
LIMB K1 ok selftest=pass cases=170
LIMB K2 FAIL rc=1 scanned=3280 hits=1 allowed=27 unused_allow=0
LIMB K3 FAIL rc=1 hits=10 missing=none extra=[('04cjvrpevejp-n5.txt', 'gitlab-runner-registration-token')]
LIMB K7 FAIL base_widened_hits=0 landing_widened_hits=6 missing=none
CAPABILITY-CHECK-RESULT fail rc=1
```

The gate is safe; the selftest alone would not be. This is the mirror of G2 and confirms the two detectors are
not redundant: each has a blind spot the other covers for a different shape.

## Bounds and tooling

* Wrote only `.ufo/waves/round-98/w1/MutC2Counter.md` and `MutC2Counter-receipts/` in the lane repo; no commits,
  pushes, resets or other mutating git commands in the lane repo. The fixture clone under scratch took the
  mutant commits and `git reset --hard` back to `e2caf4a...`; every git call named `-C <fixture>` and the
  toplevel was asserted before the first commit.
* No files under `/tmp`; no writes to `.ufo/state/`, `.ufo/watchdog.log`, `MANIFEST.json`, the fleet repo, or
  any sibling lane.
* No tool installs or upgrades were needed (stdlib Python + git only): `Python 3.14.8` (`/usr/bin/python3`),
  `git version 2.56.0`.
* Scratch removed after the receipts were copied: `rm -rf /fast/scratch/hyaku/kasegi-r98/MutC2Counter`.

## Receipts

`MutC2Counter-receipts/`: `mutants.tsv` (17 rows, both seeds), `hashes.txt` (pristine/final/clone state),
`results-20261107.json`, `results-424242.json` (full per-mutant records), `probe.txt` (differential probe),
`raw/` (36 files: per-mutant selftest + K3 stdout), `gate-raw/` (6 files: full gate runs for pristine, M01,
M13, M14, M16, M17), `harness.py`, `probe.py`, `gatecheck.sh` (the exact drivers).

VERDICT: required mutant set (M01–M13) — 13/13 killed; 12 by both detectors, M13 by the selftest only; no required mutant survives either detector.
VERDICT: supplementary M14 (ci-build right boundary narrowed) — SURVIVED both detectors and the full gate (CAPABILITY-CHECK-RESULT pass rc=0); real coverage gap G1.
VERDICT: supplementary M16 (session context made optional) — survived selftest and K3; killed by the gate's K2 (321 corpus hits); coverage gap G3 at the K3 level.
VERDICT: supplementary M17 (registration `{20,21}`) — selftest survives, K3 and K2 kill; coverage gap G4 at the selftest level.
VERDICT: detector asymmetry — selftest-only kill: M13 (G2); K3-only kill: M17 (G4); both-blind: M14 (G1) and M16 at the K3 level (G3).
VERDICT: restoration — 17/17 mutants restored to the pristine sha256 `45f8d226…`; clone clean at `e2caf4a…`; no mutant overturned a claim positive.
