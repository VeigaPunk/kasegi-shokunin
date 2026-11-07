# MutC2Counter — round 89 C2 counter mutation test

**Object under test:** `.ufo/waves/round-89/c2/capability-check.py`, sha256
`176effca85337a67093462b6239d7e6486566d72eeaf300958b298b00785abcf` (the pin in
`claims.json`). It was **not modified**: mutated copies live only in scratch, and the lane file
re-hashes to the same value after every run (receipt §restoration).
Judged at base `090a46f8`, C1 `eb5f0df8`, C2 landing `c61c5586`; the landing instrument and
allowlist are byte-equal to the frozen candidates (`95f24a54…`, `76245bba…`), re-read with
`git show c61c5586:corpus/instruments/…`.

**Verdict:** nothing here re-scores C2 — five mutants are killed by the frozen positive control
itself, nine by a frozen negative, and no mutant reaches a verdict that changes a C2 predicate. But
**20 of 35 counter mutants survive the frozen control suite**: eleven delete a conjunct the limb's
own docstring states, five delete a K7 value-derivation property the docstring promises and the
suite's `literal` control structurally cannot see, and four are equivalent/stricter/harmless on the
frozen inputs. One further finding (S1) is about the controls
script, not the counter: two of its controls are no longer reproducible after the landing.

## Method

- Scratch `/fast/scratch/hyaku/kasegi-r89/MutC2Counter` only, `TMPDIR` inside it; the only writes
  outside it are this report and its receipts under `w1/`. No git/jj write in the lane or the fleet
  repo: every clone and fixture repository was created inside the scratch root with `--shared` and
  its `rev-parse --show-toplevel` asserted before any commit.
- All fourteen control builds plus the do-nothing control were reproduced in scratch from the
  frozen script's own `build`/`count` lines (`controls/c2-controls-r89.sh`), one control at a time
  (`wrongsha` reuses the positive tree).
  My rebuild reproduces `controls/c2-controls-r89.txt` limb-for-limb, including the K1 detail
  hashes, so the baselines below are the same experiment, not a look-alike
  (receipt §baselines).
- Each mutant = one behavioural edit of the counter at the line numbers below, applied to a scratch
  copy; the positive control (pinned candidate tree, `--seed 8989`) and the negative control most
  likely to notice it were then run against it.
- **Noticed** = the positive stops passing (rc≠0 or any limb not `pass`), **or** the negative's rc
  changes, **or** any `LIMB` status in the negative changes. Detail-string-only changes are recorded
  separately: they do not change any limb verdict, and the frozen script only echoes output.
- Two runs per mutant (three where a second negative was strictly stronger); 3 s per counter run.

## Baselines (pristine counter, scratch rebuild)

`pos` pass; `pos`@seed1 pass; `wrongsha` K1 FAIL; `noallow` K3 FAIL; `r88` K3,K4,K7,K8 FAIL;
`cfoff` K1,K3,K4,K7,K8; `cfnokpi` K1,K3,K4,K7,K8; `cfdash` K1,K4,K8; `cfcase` K1,K7;
`cffloor` K1,K4,K8; `nojsonsep` K1,K4,K7,K8; `nolb` K1,K4,K7,K8; `literal` K7 only;
`alwaysclean` K2,K4,K7; `norow` K5; do-nothing (base as landing, pinned) K1,K4,K5,K7,K8 —
all `rc=1` except the two positives.

## Mutants

`line` = line of `c2/capability-check.py`. Positive is always `pos`, pinned, seed 8989.
"FLIP" names the limb whose verdict changed in the negative.

| id | line | mutation | positive | negative | noticed |
|---|---|---|---|---|---|
| m01 | 340 | K7 stops comparing the generated hit set (`ok = rcg == 1`) | pass | literal | FLIP K7 FAIL→pass, rc 0 |
| m02 | 214 | K7 CloudFront signature is a fixed constant, not `random.Random(seed)` | pass | literal | **no** |
| m02b | 214 | K7 CloudFront signature = the K4 fixture constant | pass | literal | **no** |
| m03 | 337 | K7 calls `generated(8989)` instead of `generated(seed)` | pass | literal | **no** |
| m04 | 245 | `--seed` parsed but the effective seed is the constant 8989 | pass | literal | **no** |
| m05 | 340 | K7 accepts extra hits (`gexpect <= ghits`) | pass | cfcase | FLIP K7 FAIL→pass |
| m06 | 340 | K7 stops requiring exit 1 | pass | alwaysclean | FLIP K7 FAIL→pass |
| m07 | 216 | K7 Azure signature = the K4 fixture constant | pass | nolb | **no** |
| m08 | 349 | K8 drops the hit-polarity half of the clause test | pass | cffloor | FLIP K8 FAIL→pass |
| m09 | 350 | K8 tolerates one failing clause | pass | cffloor | FLIP K8 FAIL→pass |
| m10 | 315 | K4 accepts extra hits (`PLANT_EXPECT <= hits`) | pass | cfnokpi | FLIP K4 FAIL→pass |
| m11 | 314 | `--files` stops requiring the CloudFront hit in the practice report | pass | r88, cfoff | **no** (detail only) |
| m12 | 313 | `--files` no longer passes the documentation-placeholder file | pass | literal | **no** |
| m13 | 315 | the forged-STS allowlist run may exit 0 or 2 | pass | alwaysclean | **no** |
| m14 | 78 | `BASE_REV` moved to the C2 landing | **FAIL (K6)** | r88 (K6 flips) | positive |
| m15 | 330 | K6 drops "base hits are only PLANT_EXPECT members" | pass | r88 | **no** |
| m16 | 361 | K5 drops the `gcs-signed-url-signature` needle | pass | norow | **no** |
| m17 | 362 | K5 drops the `last cell == 87` conjunct | pass | norow | **no** |
| m18 | 286 | K2 drops the `oracle == HISTORY_EXPECTED` cross-check | pass | do-nothing | **no** |
| m19 | 285 | K2 counts any hit shape as the STS oracle | pass | do-nothing | **no** (stricter, see N3) |
| m20 | 278 | K1 stops checking `--gate-sha256` | pass | wrongsha (no flip), wronggate (K1 FLIP) | frozen suite: no; seat probe: yes |
| m21 | 276 | K1 accepts selftest exit 0 with any result line | pass | cfoff | **no** |
| m22 | 155 | the allowlist digest binds a different byte span | **FAIL (K4,K6)** | — | positive |
| m23 | 154 | K4's expectation set loses the pre-round-89 plants | **FAIL (K4,K6)** | — | positive |
| m24 | 253 | instrument read from `HEAD` instead of `REV` | pass | do-nothing | FLIPs K1,K3,K4,K7,K8 |
| m25 | 315 | K4 accepts any non-zero exit as the hit run | pass | alwaysclean | **no** |
| m26 | 293 | K3 stops rejecting an unused allowlist row | pass | noallow (no flip), r88 (K3 FLIP) | r88 |
| m27 | 293 | K3 stops requiring `allowed >= 1` | pass | noallow, r88 | **no** |
| m28 | 218 | K7's host stops varying with the seed | pass | literal | **no** (N2) |
| m29 | 224,229 | K7 drops the Azure positive plant and its expectation | pass | nolb | FLIP K7 FAIL→pass |
| m30 | 349 | K8 drops the "clause's plant exists in PLANTS" guard | pass | cffloor | **no** |
| m31 | 114,148 | K4 drops the S128-order positive from plant set and expectations | **FAIL (K8)** | — | positive |
| m32 | 362 | K5 accepts `len(rows) >= 1` instead of exactly one | pass | norow | **no** |
| m33 | 77 | `ORACLE_RE` narrowed to `{60,}` | pass | do-nothing | **no** (N1) |
| m34 | 73 | `HISTORY_EXPECTED` pins a path the history cannot return | **FAIL (K2)** | — | positive |

Totals: 35 mutants; 14 noticed by the frozen suite (5 by the positive alone: m14, m22, m23, m31,
m34; 9 by a negative: m01, m05, m06, m08, m09, m10, m24, m26, m29), 1 more by the seat-supplied
`wronggate` negative (m20, see N4), 20 survive.
`m26` is the case where my first negative (`noallow`) was too weak and `r88` was the right one: the
`unused_allow` conjunct is actually controlled. The reverse is true for the survivors below — for
each I also ran the second-strongest candidate negative where one exists (`m11` vs `cfoff`), and the
negative still cannot see the change.

## Routed defects (surviving mutants that remove a stated guarantee)

Each defect: the docstring sentence it falsifies, the counter line, the edit, and the evidence that
the property is really gone. `S` = a scratch dir; all commands are the frozen script's own
`build`/`count` lines with that one edit (run one control at a time, as the script's header says).

**D1 — K7 does not pin the CloudFront signature to the seed** (`line 214`, m02/m02b).
Docstring K7: "signature, key-pair-id and SAS values are drawn at run time from
`random.Random(seed)` … a detector keyed on the fixture literals of K4 fails here." Replacing the
`cfsig` draw with a fixed constant keeps the positive passing and keeps the `literal` control
failing, because that control also requires the fixture *key-pair-id* — it therefore cannot see
that the signature stopped being seed-derived. Evidence (receipt §probe, judged on `LIMB K7` only):
a detector whose `_CF_SIG` alternative is the single fixed value finds **nothing** under the
pristine counter at seed 1 (`K7 FAIL, missing g1|CF, g2|CF`) and **both** generated positives under
`m02`/`m02b` (`K7 pass`). Fix: key the generated values on the seed *and* add a control instrument
whose CloudFront branch is a single-value literal with a generic `Key-Pair-Id` context, run at two
seeds.

**D2 — `--seed` no longer describes the generated sample** (`lines 337, 245`, m03/m04).
The counter prints `seed=N` on its first line and K7's detail repeats it, which is the only
reproduction handle a reader has. With `generated(8989)` hard-wired (or the default seed pinned),
a `--seed 1` run prints `seed=1` and generates the 8989 fixtures. Evidence: a detector keyed to the
value `generated(8989)` places in `g/x-receipts/live-g1.txt` fails under the pristine counter at
seed 1 (`K7 FAIL, missing g1|CF, g2|CF`) and passes under both mutants (`K7 pass`, and m04 prints
`seed=8989` while still being run with `--seed 1`). No frozen control compares two seeds' *values*,
so none can notice. This is the r88 D4 failure mode reappearing in a subtler form: the sample is
reproducible only if the printed seed is the seed actually used.

**D3 — K7 does not pin the Azure signature to the seed** (`line 216`, m07). Same mechanism as D1 on
the `asig` draw; the `nolb` control keeps failing for its own reason. Evidence: `_SIG`-literal
detector, pristine `K7 FAIL (missing g3|AZ)`, `m07` `K7 pass`.

**D4 — K4's `--files` limb no longer requires the CloudFront hit** (`line 314`, m11). Docstring:
"exits 1 with exactly the two expected hits." `fhits == {(f1,AZ),(f3,CF)}` → `{(f1,AZ)} <= fhits`
leaves an instrument that misses the practice-report CloudFront URL with `files_ok=True`. `r88` and
`cfoff` both miss that hit and both keep `K4 FAIL` for other reasons, so no control's rc or limb set
changes (detail only: `files_ok=True`).

**D5 — K4's forged-allowlist clause accepts a clean exit** (`line 315`, m13). Docstring: "an
allowlist holding an `aws-sts-session-token` row makes the instrument exit 2." `rc2 == 2` →
`rc2 in (0, 2)`. `alwaysclean` reaches `sts_allow_rc=2` (its edit leaves the exit-2 path intact), so
no control exercises the difference.

**D6 — K6 no longer checks that the base instrument stays inside `PLANT_EXPECT`** (`line 330`, m15).
Docstring: "and only PLANT_EXPECT members." Dropping `bhits <= set(PLANT_EXPECT)` is invisible
because the base instrument's 11 hits are all expected members; no control perturbs the base
expectation set.

**D7 — K5's three conjuncts are individually unpinned** (`lines 361, 362`, m16/m17/m32). Docstring:
"its last cell is `87` and the row names `cloudfront-signed-url-signature`,
`gcs-signed-url-signature`, `azure-sas-signature` and `corpus/practice/*/evidence/`", and "exactly
one row". Each conjunct can be deleted with the positive passing and `norow` still failing K5 (it
fails on row content, not on the deleted conjunct). Worse for verifiability: K5's detail line is
`rows=%d` only, so even a human reading the control log cannot tell *which* conjunct failed.

**D8 — K2's oracle pin is not load-bearing** (`line 286`, m18). Docstring: the oracle "must itself
equal HISTORY_EXPECTED". Deleting the cross-check changes nothing, because the oracle and the pinned
set are computed from the same committed history; no control varies either side.

**D9 — K1's selftest result string is not exercised** (`line 276`, m21). Docstring: "`--selftest` exits
0 **and prints** `SELFTEST-RESULT pass`." The only negative that fails selftest (`cfoff`) exits 1, so
`rc == 0` already decides it; the string conjunct has no discriminating control.

**D10 — K4 accepts exit 2 as "the hit run"** (`line 315`, m25). `rc == 1` → `rc != 0` lets a usage
error on the planted repository satisfy the limb. No control produces exit 2 there.

**D11 — K3's `allowed >= 1` floor is unexercised** (`line 293`, m27). Deleting it changes nothing:
`noallow` keeps `allowed=18`, `r88` fails on `unused_allow`.

**D12 — K8's existence guard is unexercised** (`line 349`, m30). With the `p not in PLANTS` half
removed, a clause pointed at a plant that no longer exists still passes when its polarity is
negative (`(p,s) in hits` is False and `want` is False), i.e. a typo'd negative clause becomes
silent. No control edits `CLAUSES`, so nothing notices. (m31 shows the *polarity* half is
load-bearing: dropping the S128 plant fails the positive through K8.)

### Non-defects (recorded so the L1 does not re-derive them)

- **N1 (m33)** narrowing `ORACLE_RE` to `{60,}` is equivalent on the frozen history (both STS tokens
  are longer); it is not a loss of the predicate today, but the oracle's breadth is unpinned.
- **N2 (m28)** the generated host is not part of any detection shape, so its constancy has no
  contract effect.
- **N3 (m19)** mapping K2's oracle to "any shape" makes K2 *stricter* (it fails if any non-STS hit
  exists), so it cannot mask a miss.
- **N5 (m12)** dropping the placeholder file from `--files` removes a redundant negative: S006/S010
  still cover documentation placeholders inside the planted repository.
- **N4 (m20)** the `--gate-sha256` check is sound today (a wrong gate pin fails K1); the frozen suite
  simply never passes one, so only a seat-supplied wrong-gate run notices the deletion. The gap is
  one missing negative in the control set, not a counter defect.

## S1 — the frozen controls script is not commit-bound for two of its controls

`controls/c2-controls-r89.sh` builds its `r88` and `noallow` trees from **lane worktree** files:

```
build r88 "" yes "$L/corpus/instruments/capture-secret-scan.py"
build noallow "" yes "" "$L/corpus/instruments/capture-secret-allow.tsv"
```

After the C2 landing those two paths hold the landed candidate bytes (`95f24a54…`, `76245bba…`), so
both trees are now byte-identical to the positive control: the rebuilt `drift-r88` hashes
instrument `95f24a54…`/allowlist `76245bba…` (the recorded control hashed the base instrument
`d7349536…`), and the frozen counter over both drift trees prints
`CAPABILITY-CHECK-RESULT pass rc=0` — the exact opposite of the script's own "(expected fail …)"
annotations for those controls. The recorded `c2-controls-r89.txt` is sound because it ran before
the landing; the script is not re-runnable, and a future re-run would silently lose two negative
controls and report a false "controls re-run OK".
Fix (r90): materialise both files from `$B` (`git show $B:corpus/instruments/…`), as the other
builds already do — they read the frozen `c2/candidate/*` files, which do not move. Evidence that this restores the recorded behaviour: the commit-bound
rebuilds give `r88` `K3,K4,K7,K8 FAIL` and `noallow` `K3 FAIL` (receipt).

This is the same class as r88's routed defect 2 ("counter binding"); it recurs one round later on the
control *inputs* rather than on the counter.

## Restoration and hygiene

- The lane counter was never edited: sha256 `176effca…` before (the `claims.json` pin, read at the
  start) and after (measured when the receipt was rendered, after every mutant run) — receipt
  §restoration. Every mutant, detector instrument and fixture repository existed only under the scratch
  root, which is deleted (`trap 'rm -rf -- "$S"' EXIT`); nothing was left in `/tmp`.
- No credential-shaped value is written here or in the receipts: receipts carry sha256 digests,
  `LIMB`/`CAPABILITY-CHECK-RESULT` lines, paths and shape names only — the scanner's own HIT/summary
  lines, never fixture bytes. The counter, the scanner and no `S<digits>.txt` snapshot were copied
  into this directory.
- The lane tree, the fleet repo and the frozen `c1/ c2/ controls/ l1/` bytes were read only.
- Not done: no re-scoring of C2, no live target, no full `resolve.py` census, and the controls
  script was never run end-to-end (single controls only, as the seat bounds require).
