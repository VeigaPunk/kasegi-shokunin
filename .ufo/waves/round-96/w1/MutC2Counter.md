# MutC2Counter — round-96 C2 mutation campaign (seat report)

Seat: mutation-tester (leaf). Target: the round-96 `capture-secret-scan` shapes and
the frozen gate `.ufo/waves/round-96/c2/capability-check.py`.
Base: `7ef1d365eb523a83b2567342a6c0f585ab028ab0` (C2 landing). Lane read-only;
all mutation work in a scratch clone at `/fast/scratch/hyaku/kasegi-r96/MutC2Counter/lane`.

## Verdict

C2 STANDS at `7ef1d36`: I re-derived the frozen command myself (both pins) and got
`CAPABILITY-CHECK-RESULT pass rc=0` (K1 `inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=128`;
K2 `scanned=2744 hits=0 allowed=27 unused_allow=0`; K3 `hits=7 missing=none extra=none`;
K4 `base_new_shape_hits=0 old_shapes_missing=none`; K5 `rows=1 last=87 named=True`;
K6 `rc=1` with `aws-sts-session-token`). The mutation campaign does not overturn that
predicate — it shows the predicate is carried by the digest pin, not by the gate's
behavioural limbs: **8 of 14 single-point mutants are killed behaviourally, 6 survive, and
both gate forgeries pass with `--instrument-sha256` omitted; all 16 are refused only by K1's
sha pin.** Routed qualifier (coverage, not a verdict change): K1's selftest and K3's plants
do not pin the versioned/routable right boundary, the routable tail's first-group lower
bound, the versioned head floor, the versioned left boundary, or the custom-prefix span;
K2 has no scanned-count floor, so a scope-narrowed scanner passes.

## Method

- `git clone --no-hardlinks` of the lane into scratch at `7ef1d36`; `rev-parse --show-toplevel`
  asserted equal to the clone before every mutating command.
- Each mutant is a commit object built with plumbing only — `hash-object -w`, `read-tree` /
  `update-index` / `write-tree` under a private `GIT_INDEX_FILE`, `commit-tree`. No ref,
  index or working tree of the clone was changed; no `git add/commit/checkout/reset/stash`
  was run anywhere, and no jj command.
- Each mutant is exactly one replacement in `corpus/instruments/capture-secret-scan.py`
  (occurrence count asserted `== 1` before the edit; the committed blob is read back and
  compared byte-for-byte).
- Each run: the frozen gate with the mutant commit as `--rev`, once **with** the frozen
  instrument pin (`--instrument-sha256 71876619…`) and once **without** it, fixed seed.
- Baseline: pristine `7ef1d36` with both frozen pins (instrument + `claim-package-check.py`).

## Baseline (pristine 7ef1d36, both pins)

```
LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=128
LIMB K2 ok rc=0 scanned=2744 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=7 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
```

The round-95 instrument at `d8a2bb0` still passes its own selftest at `cases=115`, so K4's
"0 of the seven shapes" is a capability gap, not a broken base.

## Mutants (14, one edit each)

`nopin` = gate without `--instrument-sha256`; `pin` = gate with the frozen pin.
Every `pin` run is `rc=1` with `LIMB K1 FAIL inst_sha=<mutant digest>` — the digest guard
fires for all 14 (and for both forgeries below).

| # | edit (single point) | sha256 (16) | nopin | limb that caught it | verdict |
|---|---|---|---|---|---|
| M1 | `_GJ_ROUTABLE` head floor `{27,300}` → `{26,300}` | `869a742dadb90f77` | rc=1 | K1 selftest rc1 (case `glpat-routable-short-head`) **and** K3 extra `n1.txt gitlab-pat-routable` | killed |
| M2 | `_GJ_ROUTABLE` tail `\.[0-9a-z]{2}[0-9a-z]{7}` → `\.[0-9a-z]{1}[0-9a-z]{7}` | `e749efbe164c4a1e` | rc=1 | K1 selftest rc1 **and** K3 missing `p2.txt gitlab-pat-routable` | killed |
| M2b | `_GJ_ROUTABLE` tail `\.[0-9a-z]{2}[0-9a-z]{7}` → `\.[0-9a-z]{1,2}[0-9a-z]{7}` (the actual widening) | `b55f73ace252eb2e` | rc=0 | none | **survived** |
| M3 | `_GJ_VER` tail `[0-9a-z]` → `[0-9A-Za-z]` | `5b7299dffd1b8c72` | rc=1 | K3 extra `n6.txt gitlab-agent-token-versioned` (K1 passed: the uppercase cases are on the routable form) | killed |
| M4 | `_GJ_VER` drop `(?![A-Za-z0-9_])` | `cefd4656343b032b` | rc=0 | none | **survived** |
| M5 | `glptt-` `(?:{20}\|{40})` → `{20,40}` | `fb4eab1f21be5dcc` | rc=1 | K1 selftest rc1 (`glptt-39`) **and** K3 extra `n4.txt gitlab-pipeline-trigger-token` | killed |
| M6 | `gitlab-deploy-token-versioned` drop `_GL_PREFIX` | `1e39fd2717cc7788` | rc=0 | none (hit/no-hit equivalent; matched span 53 B → 48 B) | **survived** |
| M7 | `_GJ_VER` middle `\.[0-9a-z]{2}\.` → `\.[0-9a-z]{1}\.` | `41a144d6b963d60c` | rc=1 | K1 selftest rc1 **and** K3 missing p1,p3,p4,p5,p6 + extra `n3.txt` | killed |
| M8 | `_GJ_ROUTABLE` also matches the versioned tail | `b1c61ab8d897f106` | rc=1 | K1 selftest rc1 **and** K3 extra `p1.txt gitlab-pat-routable` | killed |
| M9 | `_GJ_VER` head floor `{27,300}` → `{26,300}` | `21bed514d6b038ba` | rc=0 | none | **survived** |
| M10 | `gitlab-pat-versioned` drop `_GL_LB` | `979b75bca4d82464` | rc=0 | none | **survived** |
| M11 | `glptt-` drop `(?![A-Za-z0-9_-])` | `09a5cd4f06d81ca0` | rc=1 | K1 selftest rc1 **and** K3 extra `n4.txt` | killed |
| M12 | `_GJ_ROUTABLE` head floor `{27,300}` → `{1,300}` | `f0dad4d693b135f7` | rc=1 | K1 selftest rc1 **and** K3 extra `n1.txt` | killed |
| M13 | `_GJ_ROUTABLE` drop `(?![A-Za-z0-9_])` | `289381024f3f3b55` | rc=0 | none | **survived** |

Kill split: K1 selftest alone caught 0; K3 alone caught 1 (M3); K1+K3 caught 7; 6 survived.
The selftest is the stronger limb (it fails on 7 of the 8 killed mutants); K3 is load-bearing for
M3, whose defect sits on a shape the selftest does not exercise at that boundary.

### Survivor probes (the mutants are real, not equivalent)

Run with `--files` on one planted line; landed = `capture-secret-scan.py` at `7ef1d36`.

| probe | landed | mutant |
|---|---|---|
| `glpat-<28>.ab.cd1234567X` (trailing token char) | no hit | M4: `HIT gitlab-pat-versioned` |
| `glpat-<28>.abcd12345X` | no hit | M13: `HIT gitlab-pat-routable` |
| `glpat-<28>.xyz12345` (1+7 routable tail) | no hit | M2b: `HIT gitlab-pat-routable` |
| `glpat-<26>.ab.cd1234567` (26-char versioned head) | no hit | M9: `HIT gitlab-pat-versioned` |
| `xglpat-<28>.ab.cd1234567` (letter before) | no hit | M10: `HIT gitlab-pat-versioned` |
| `acme-gldt-<30>.ab.cd1234567` | hit | M6: hit (span only: 53 B vs 48 B — allowlist digest changes) |

M6 is equivalent on hit/no-hit (the `-` before `gldt-` satisfies `_GL_LB` either way); it is a
real difference only for allowlist addressability, because the allowlist keys on
`sha256(m.group(0))`. The other five are genuine false positives/negatives that every limb
misses.

## Forgeries of the gate

### F1 — fixture-literal detector (`6b1fd44f3e62e87f…`)

The seven new patterns replaced by `re.escape` of the seven plant byte strings, and the 13
round-96 selftest cases rewritten to those same literals. The detector has **no general
capability**: a fresh routable PAT (`glpat-<30>.zzpq12345`) gets `hits=0` from F1 and
`HIT shape=gitlab-pat-routable` from the landed scanner.

Gate result without the pin: `CAPABILITY-CHECK-RESULT pass rc=0` — K1 `cases=128`, K2
`scanned=2744 hits=0 allowed=27 unused_allow=0`, K3 `hits=7 missing=none extra=none`, K4, K5,
K6 all ok. With the pin: `LIMB K1 FAIL inst_sha=6b1fd44f…` → rc=1.

Root cause: `build_plants` nonce-randomises only the **paths**; the token bytes are fixed
(`p1.txt` is always `glpat-` + `A`*28 + `.ab.cd1234567`). K3 therefore cannot separate a
general regex from a detector overfitted to the plant literals, and K1 runs the instrument's
own selftest, which a forger also controls. The digest pin is the only external anchor.

### F2 — scope-narrowed scanner (`2b3ad84b2af2948b…`)

`is_capture_path` reduced to `corpus/source-snapshots/` + `*-receipts` (the `live-` basename
and `corpus/practice/*/evidence/` branches dropped; the two selftest path expectations
flipped to match). On a probe commit carrying a real routable PAT in both a `live-` path and
a `-receipts` path, the landed scanner reports 2 hits and F2 reports 1 — the `live-` token is
lost.

Gate result without the pin: `CAPABILITY-CHECK-RESULT pass rc=0` — K2 `scanned=2708` (36
files fewer than the pristine 2744) `hits=0 allowed=27 unused_allow=0`, K3 `hits=7`, K4, K5,
K6 all ok. With the pin: `LIMB K1 FAIL inst_sha=2b3ad84b…` → rc=1.

Root cause: K2 checks only `rc==0, hits==0, unused_allow==0, allowed>=1` — it never pins the
scanned count, so a scope loss is invisible unless it orphans an allowlist row. The 16
allowlist rows under `-receipts` and the 9 under `corpus/source-snapshots/` keep exactly the
two branches F2 kept, so `unused_allow` stays 0. K3's plants live outside the lane and are
passed via `--files`, so K3 never exercises `is_capture_path` at all. K6 only re-tests one
shape (`aws-sts-session-token`) on one rev under `corpus/source-snapshots/`.

## Is the digest pin the only guard?

For the 6 surviving mutants and both forgeries: **yes**. With `--instrument-sha256` supplied,
all 16 are refused at K1 (`inst_sha=<digest>`), and the gate exits 1. Without it, 8 mutants
are still killed behaviourally, 6 survive, and both forgeries pass every limb. So the pin is
not the only guard in general — but it is the only guard for every defect the behavioural
limbs miss, and it is the only thing that distinguishes a reviewed instrument from an
overfitted or scope-narrowed one.

## Coverage findings (routed, not verdict changes)

1. The right boundary `(?![A-Za-z0-9_])` of both new tails is unpinned: M4 and M13 survive and
   both turn `<token>X` into a hit. No selftest case and no plant puts a token character
   immediately after a versioned or routable token.
2. The routable tail's first group is unpinned at its lower bound: M2b (`{1,2}` + 7) survives
   and reports a 1+7 tail that the frozen statement excludes.
3. The versioned head floor is unpinned: M9 (26) survives; only the routable form has a
   short-head case (`glpat-routable-short-head`).
4. The versioned left boundary is unpinned: M10 survives; the only letter-before case
   (`gl-pat-letter-before`) is on the 20-character `gitlab-pat` form.
5. The custom-instance-prefix span is unpinned: M6 survives on hit/no-hit and changes the
   matched bytes, i.e. the allowlist digest, for every prefixed token.
6. K3's nonce covers paths only, not token bytes — F1 passes with a detector that has no
   general capability.
7. K2 has no scanned-count floor and K3 bypasses `is_capture_path` — F2 passes with the
   `live-` and practice-evidence scopes removed.

None of these changes the frozen predicate at the landing; they are the fixtures the next
round would need if the claim is to rest on behaviour rather than on the pin.

## Restoration evidence

- The lane was never written: `git -C <lane> status --porcelain` shows only a sibling's
  in-flight `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` edit and untracked
  wave dirs (the lane HEAD moved to `b7f59c6` during this seat; my reads and the clone are
  pinned at `7ef1d36`). `corpus/instruments/capture-secret-scan.py` in the lane is still
  `71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9`.
- The scratch clone is unchanged: `HEAD=7ef1d36`, `status --porcelain` empty, refs only
  `refs/heads/master` + `origin/*`, instrument sha still `71876619…`.
- Mutant and forgery commits exist only as unreferenced objects in the scratch clone; the
  sources are copied into `MutC2Counter-receipts/sources/` and the scratch tree is removed at
  seat exit.

## Receipts

All under `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless absolute; scratch
`S=/fast/scratch/hyaku/kasegi-r96/MutC2Counter`, receipts `R=.ufo/waves/round-96/w1/MutC2Counter-receipts`.

| # | command | rc | observed |
|---|---|---|---|
| 1 | `git clone -q --no-hardlinks <lane> $S/lane` | 0 | clone at `7ef1d36`; `rev-parse --show-toplevel` = `$S/lane`; `252df0c` and `d8a2bb0` present |
| 2 | `python3 -B .ufo/waves/round-96/c2/capability-check.py --lane $S/lane --rev 7ef1d36… --work $S/work-base --instrument-sha256 71876619… --gate-sha256 8b6f8493… --seed 9601` | 0 | `CAPABILITY-CHECK-RESULT pass rc=0`; K1 pin-ok/pin-ok cases=128; K2 scanned=2744 hits=0 allowed=27 unused=0; K3 hits=7; K4 0/none; K5 rows=1 last=87; K6 aws-sts present (34 s) |
| 3 | `python3 -B $S/build_mutants.py` | 0 | 12 mutant commits, each `old` count asserted 1; `$S/mutants.json`; receipt `01-build-mutants.txt` |
| 4 | `python3 -B $S/build_forgeries.py` | 0 | F1 `b6d41f78…`, F2 `9a30abb1…`, PROBE `3a6782bf…`; receipt `02-build-forgeries.txt` |
| 5 | `xargs -P 6 -n 4 $S/run_one.sh < $S/jobs.txt` | 0 | 24 gate runs (12 mutants × pin/nopin), 4 m 5 s; per-run outputs in `R/mutants/` |
| 6 | `xargs -P 4 -n 4 $S/run_one.sh < $S/jobs2.txt` | 0 | M2b and M13 × pin/nopin, 1 m 7 s |
| 7 | `xargs -P 4 -n 4 $S/run_one.sh < $S/jobs3.txt` | 0 | F1 nopin rc=0 / pin rc=1; F2 nopin rc=0 / pin rc=1 |
| 8 | `python3 -B $S/mutants/<M>.py --files $S/probe-*.txt` (6 probes) | 0/1 | landed vs mutant hit lines, `R/04-survivor-probes.txt` |
| 9 | `python3 -B $S/forgeries/F1-fixture-literal.py --files $S/probe-general.txt` | 0 | `hits=0` (no general capability); landed on the same file `hits=1` |
| 10 | `python3 -B $S/forgeries/F2-scope-narrowed.py --lane $S/lane --rev 3a6782bf…` | 1 | 1 hit (receipts) vs landed 2 hits (receipts + `live-probe.txt`) |
| 11 | `python3 -B $S/lane/corpus/instruments/capture-secret-scan.py --selftest` (F1, F2) | 0 | both `SELFTEST-RESULT pass cases=128` |
| 12 | `python3 -B $S/base-r95.py --selftest` | 0 | `SELFTEST-RESULT pass cases=115` (round-95 base is sound) |
| 13 | `git -C $S/lane rev-parse HEAD; status --porcelain; for-each-ref` | 0 | `7ef1d36`, empty status, only master/origin refs |
| 14 | `git -C <lane> rev-parse HEAD; status --porcelain; sha256sum corpus/instruments/capture-secret-scan.py` | 0 | `b7f59c6` (sibling moved it), 3 entries (sibling's), instrument `71876619…` |
| 15 | `sha256sum $R/sources/*.py` | 0 | 17 digests, `R/07-source-digests.txt` |

Receipt files: `00-baseline.txt`, `01-build-mutants.txt`, `02-build-forgeries.txt`,
`03-forgery-selftests-and-general-probe.txt`, `04-survivor-probes.txt`,
`05-summary-tables.txt`, `06-restoration-evidence.txt`, `07-source-digests.txt`,
`mutants/` (32 gate transcripts), `sources/` (16 mutant/forgery sources + the gate).

No tool was installed or upgraded for this seat.
