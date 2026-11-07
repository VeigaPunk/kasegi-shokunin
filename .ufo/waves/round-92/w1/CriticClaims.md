# CriticClaims — round 92, attempt 1 (leaf attack: C1 tranche 7, C2 github-token)

Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scope: falsify the two frozen claims on their
frozen predicates only, at their landing commits. No lane file, instrument, frozen byte or sibling
lane was edited; every fixture lived in `/fast/scratch/hyaku/kasegi-r92/CriticClaims` (deleted on exit).

## Verdicts

- **C1 (depth:verifiability, tranche 7) — STANDS** on P1/P2/P3 at `cb1ef2b9856df79c530f3ff1374fa9691ff56233`.
- **C2 (coverage, `github-token`) — STANDS** on P1/P2/P3 at `58c0c115342877ee556cae19928d69839b0b29f0`.

Routed defects and qualifiers below; none re-scores a claim. The strongest attack found is on the
**C2 counter's plant coverage** (D-1), not on the landed bytes.

## 1. Frozen commands re-run (evidence: `CriticClaims-receipts/c1-frozen-run.txt`, `CriticClaims-receipts/c2-frozen-run.txt`)

C1, exactly the frozen command with `--lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`, `--work $S`:

```
KNOWLEDGE-METER base=947/1947 after=960/1944 base_target=947/1947 target=960/1944 sites=25 labels=30 ... pinned=archive
LIMB M0 pass; M1 pass; M3 pass (bad_lines=0 old_not_once=0 dup_rows=0); M4 pass; M5 pass; M9 pass rows=25 unbound=none
LIMB M10 pass labelled=30 want=25 mapped=25 kinds=dash-cell=2,drop-token=2,excluded=2,named=2,named-cell=2,no-edit=3,qualify=7,range=10
LIMB M6 pass sha256=6d87cafa...
KNOWLEDGE-METER-RESULT pass rc=0
```

The M10 kind tally is exactly the claim's own decomposition (10 range repoints, 7 CORRECT
qualifications, 2 dash cells 369/370, 2 token drops 58/144, 2 named repoints 150/152, 2 whole-cell
repairs 155/249, 3 no-edit, 2 EXCLUDED). Independent cross-check via the meter's other code path
(`--measure-rev`): base `947/1947`, landing `960/1944`, same host line (`abs_tokens=127`).

C2, exactly the frozen command, at seeds 9191, 1 (the two pinned seeds) plus fresh 271828 and 314159,
with the frozen `--instrument-sha256` and `--gate-sha256`: `CAPABILITY-CHECK-RESULT pass rc=0` at
all four seeds, `K1–K8 pass`, `K3 scanned=1882 hits=0 files=0 allowed=20 unused_allow=0`,
`K6 base_hits=22 new_caught_by_base=none`. The landing receipt's run-time seed run is not
reproducible by nature; the four seeded runs cover the two pinned ones.

## 2. P2 and P3 (`CriticClaims-receipts/p2-p3.txt`)

| pin | claims.json | freeze tree | landing / worktree |
|---|---|---|---|
| C1 counter sha256 | `631ad3dc…a2399` | `631ad3dc…a2399` | `631ad3dc…a2399` |
| C1 map sha256 | `6d87cafa…b772` | `6d87cafa…b772` | `6d87cafa…b772` |
| C2 candidate sha256 | `04666f67…a9e` | `04666f67…a9e` | landing instrument `04666f67…a9e` |
| C2 counter sha256 | `3feed3b0…a847` | `3feed3b0…a847` | `3feed3b0…a847` |
| C2 gate sha256 | `8b6f8493…8e6` | — | printed by K1, equal |
| scorecard row sha256 | `9bd66c5c…e832` | `9bd66c5c…e832` | SCORECARD.md:307 at landing `9bd66c5c…e832` |

P3, `git diff-tree --no-commit-id --name-only -r`:
- C1 landing: `corpus/knowledge/root-loss-2026-10-12.md`, `corpus/knowledge/triage-thresholds.md` — exactly 2.
- C2 landing: `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py` — exactly 2; SCORECARD diff is
  1 insertion + 1 deletion (the capability row only; no axis score line).
- Receipts commit `ee830069…`: the two `l1/` receipts only.

No path outside each landing's allowed set was touched, so P3 holds for both.

## 3. Freeze ordering (`CriticClaims-receipts/freeze-order.txt`)

`9e4f0d68` 06:09:08 → C1 `cb1ef2b9` 06:09:15 → C2 `58c0c115` 06:09:23 → receipts `ee830069` 06:10:47;
`merge-base --is-ancestor` rc=0 for base→freeze, freeze→C1, freeze→C2. All eight control receipts are
blobs in the freeze commit; the labels commit `d0bd4758` (05:51) is an ancestor of the base
(05:57). The freeze commit touches **no** `corpus/knowledge/` path, so base→landing isolates the 25
edits, and it contains the counters/map/candidate byte-identical to the pins above (hashes verified
both from the freeze tree and the worktree).

The pre-freeze controls are not just present but *coherent with the frozen bytes*: the candidate
control reproduces `947/1947 → 960/1944` with the same map sha; no-work reads `after=947/1947`
(M1, M3 FAIL); partial-24 reads `959/1944`; excluded-437 reads `961/1944` with M9/M10 FAIL;
drop-token-58-as-dash reads `960/1944` with M4 FAIL. A meter without the EXCLUDED set could not
produce the excluded-437 M10 line (`unlabelled=437`) — so the exclusion existed when the controls
ran, not after the landing.

## 4. C1 attacks (`CriticClaims-receipts/c1-forgery.txt`, `CriticClaims-receipts/c1-labels-and-excluded.txt`)

**Is there a cheap forgery?** No, inside the measured scope. The map is fully determined: M6 pins its
bytes, M9 derives each `(old,new)` from the label row at `d0bd4758`, M10 pins the
mapped pair set to exactly `want`, and M3 requires every other line of every `corpus/knowledge/*.md`
file to be byte-identical and every mapped line to be base-line-with-one-replacement. (M9 compares
`exp[1:]` only, so a `range` label that repeats the key's own range and a `qualify` label collapse to
the same `(old,new)`; the kind distinction is nominal for enforcement and is used only by M10's
`want` set. This is not exploitable: both derive the same edit.) Four variants
built in a scratch `--shared` clone at the base:

| variant | result |
|---|---|
| A: frozen map + one rate-neutral edit (trailing space) on an **unlabelled scope** line | `960/1944`, M1/M6/M9/M10 pass, **M3 FAIL bad_lines=1** → caught |
| B: frozen map + one edit **outside** `corpus/knowledge` (`SKILL.md` line 1) | **meter PASS, all limbs** → P1 is scope-bound by design; only P3 sees it, and P3 passes on the landing |
| C: frozen map + an unlabelled in-scope GONE repoint, no map row | `960/1945`, **M1 FAIL and M3 FAIL** → caught twice |
| D: map + EXCLUDED 437, `--map-sha256` omitted | `961/1944`, **M1/M9/M10 FAIL** → the exclusion is enforced, not merely permitted |

Variant B is the honest statement of the division of labour: **P1 alone cannot detect an
out-of-scope edit**; the frozen predicate's P3 is load-bearing for that class. P3 is verified here
(exactly 2 paths), so the claim is not forgeable at this landing — but a future round must not treat
the meter run as sufficient.

**Do-nothing.** With no edits applied the same map reads `947/1947` and fails M1 and M3 (control
receipt); the meter's M3 cannot pass without all 25 site lines actually changed.

**EXCLUDED as post-hoc narrowing?** Frozen, not post-hoc: the set is in the meter bytes at `9e4f0d68`
(lines 86–89, comment "frozen before any edit was scored"), it is disclosed in the claim statement by
number, M10 forces the two pairs to exist among the labels (`set(EXCLUDED) <= kinds`), and the
excluded-437 control shows application is rejected. It is also **numerically conservative, not
self-serving**: applying 437 at this base raises the rate to `961/1944`, i.e. *above* the claim's
`960/1944`; applying both excluded pairs reads `961/1943` (`CriticClaims-receipts/c1-excluded-additivity.txt`), so
438 contributes 0 to the numerator (its target token is the one the 155 repair already creates) and −1
to the denominator (it is the last site of the bare `mission-control.md:37-38` token). The 27-label
application at this base is therefore +14/−4; the claim's +13/−3 differs by exactly those two pairs. No
hidden gain.
Residue, worth recording on this exact axis: both excluded cells' quotes are absent at their cited
ranges already (`reward.min present on 48` occurs nowhere in `intake-surface.md`; `openai-oauth`
occurs only at `mission-control.md:57`, not at `:37-38`). The exclusion defers a *quote-level* repair,
not a pointer-level one; the claim does not hide this, but it also does not repair it.

**Labels provenance.** `round92-labels.tsv` at `d0bd4758`: 30 data rows, 5 columns; 26 cite
`triage-thresholds.md`, 1 `root-loss-2026-10-12.md:68`, 2 `citation-bases.md:14` (no-edit),
1 `japanese-domestic-disclosure-workflow.md:7` (no-edit); written by the round-91 reviewer seat
`ReviewC1Labels` (non-author; `swarm-registry.json` role `reviewer`). The seat's `map_eligible=26` counts
target-bearing rows (10 canonical range + 6 non-dash content repairs + 10 CORRECT); it is not an
exclusion count. Edit-bearing rows are 30 − 3 no-edit = 27 = the claim's 25 + 2 EXCLUDED, consistent.

**Counter gap (low, not instantiated).** M3 walks only `corpus/knowledge/*.md`, while M9/M10 accept any
label pair. A label naming a site outside that directory would be counted in `want`/`mapped` and its
map row accepted without any check that the after tree contains the edit. All 30 labels here cite
`corpus/knowledge`, so it is not exercised this round; it is a one-line future hardening.

## 5. C2 attacks (`CriticClaims-receipts/c2-boundary-probe.txt`, `CriticClaims-receipts/c2-mutants.txt`)

**Do-nothing.** Controls: the base instrument misses all 6 round-92 plants (K4) and the 3 generated
GitHub positives (K7); K8 fails 6 clauses. At the landing, K6 confirms the base instrument catches
none of `NEW_EXPECT` (`base_hits=22`, `new_caught_by_base=none`), and `base_hits ⊆ PLANT_EXPECT`, so the
landed scanner also drops no earlier shape.

**Control forgeries.** F1–F10 all fail a behavioural limb besides K1; F8 (literal-keyed on the K4
fixtures) is the interesting one — it passes K4 and K8 and is caught only by K7's seeded values, which
is exactly why the seeded repo exists. These are good controls.

**Predicate-coverage counterexample (D-1, medium).** K4/K7/K8 do not bind the statement's boundary
classes for `_` (and only probabilistically for digits). Single-token mutants of the landed scanner,
run through the frozen counter unpinned (`K1` prints the mutant sha), at the two pinned seeds:

| mutant (one token changed) | 9191 | 1 |
|---|---|---|
| right boundary `(?![A-Za-z0-9])` — allows `_` after the 36-char tail | **pass** | **pass** |
| left boundary `(?<![A-Za-z0-9])` — allows `_` before the prefix | **pass** | **pass** |
| left boundary `(?<![A-Za-z_])` — allows a digit before the prefix | pass | **fail** (K7 n11 draws a digit) |

The right-underscore mutant passes at **every** seed: K4's only right-boundary plant is a letter
(`S029` appends `Z`), and K7's `live-n9` appends `r.choice(b62)` — letters and digits only, never `_`.
The left-underscore mutant is caught only when the fresh run-time seed happens to draw `_` before the
prefix (1/63); the two pinned seeds draw `V` and `6`. The frozen statement says "not preceded by a
letter, digit or _ … and not followed by a letter, digit or _", so these are statement-violating bytes
that the behavioural limbs cannot distinguish from the candidate; only P2/K1's sha identity does.
K8 is not a defence here because `CLAUSES` is the counter's own restatement and names only the
letter-before and 37th-letter cases.

**The landed instrument itself is correct.** A 15-fixture synthetic probe against the landed bytes:
left digit `9` **no hit**, left `_` **no hit**, right digit **no hit**, right `_` **no hit**, right `.` hit,
right space hit, line-start hit, JSON `\n` escape hit, letter-before no hit, 20-digit APPID hit,
21-digit APPID no hit, two-segment stateless no hit, bare prefix no hit, non-capture path unscanned.
Two statement-silent cases hit (a 4-segment JWT; a 36-tail followed by a Unicode `é`) — the boundary
class is ASCII by design, matching the shape's ASCII base62 alphabet, so neither is a stated negative.

**Sources.** S136 `:158` prefix rule, `:160` stateless note + 40-character installation-token length,
`:162`–`:167` the five prefixes + `github_pat_`; S137 `:156` three-letter prefixes, `:157`–`:161` ghp/gho/
ghu/ghs/ghr, `:167` 6-digit Base62 checksum, `:173` 30-char random portion (36-char base62 tail). Every
K8 clause citation matches those lines exactly. S138 is
rejected by the claim and is not cited by any clause. No false provenance found.

**Scorecard.** The landed row is byte-identical to the frozen `scorecard-row.txt` and the SCORECARD
diff is that one row; no axis line moved, consistent with "coverage 8 held".

## 6. Cross-claim residue for integration (routed, not a falsification)

The C2 landing grows `corpus/instruments/capture-secret-scan.py` from 378 to 417 lines (+39), which shifts line anchors
that four knowledge entries cite. At HEAD those entries are stale (`capture-intake-gate.md`,
`cloud-signed-cookies-and-user-bound-sas.md`, `cloud-signed-url-credentials-in-captured-evidence.md`,
`presigned-url-credentials-in-captured-evidence.md`, e.g. `:184-185 → :206-207`, `:192 → :214`,
`:146-161 → :168-183`, plus the shape count "eleven → thirteen"). The working tree already carries an
uncommitted re-anchor (sibling work in flight). I sampled five new anchors against the landed file and
each resolves to the content claimed (`:109-110`, `:168-183`, `:206-207`, `:214`, `:220`); the repair is
substantively right but **must be committed with the wave** — the C2 P3 path set cannot cover it, and
round 91's M91-3 class is exactly this failure. This is the C2 landing's cost on C1's axis.
(The L1 already has untracked `l1/reanchor-r92.txt` + `l1/reanchor-scanner-cites.py` in flight for
this; its `:184-185 → :206-207`, `:192 → :214`, `:146-161 → :168-183`, `:94-95 → :109-110` rows agree
with the five anchors I sampled independently. I did not rely on those files for the verdict.)

Working-tree state observed at 2026-11-07T09:35Z (not edited by this seat): the four files above are
`M`, and an untracked candidate entry `corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md`
appeared while this review ran (siblings writing the wave's entry in the live tree); no other
`corpus/knowledge` path is dirty. All counters read `git archive REV`, so no reading in this report was
affected by those modifications (both `--measure-rev` values reproduce at their commits).

## 7. Impacted axes

| axis | impact |
|---|---|
| depth:verifiability (C1's axis) | (a) C2's line-shift leaves four entries mis-anchored in HEAD until the uncommitted repair lands; (b) the 2 EXCLUDED cells keep quotes that occur nowhere at their cited ranges. Neither is claimed away by C1; both are residue on the axis the round is repairing. |
| coverage (C2's axis) | D-1: the statement's `_`/digit boundary clauses are unbound by K4/K7/K8. The landed bytes honour them (probe), so coverage 8 holds; a future instrument violating them could be frozen with a passing predicate. |

## 8. Smallest safe corrections

1. **C2 counter (round 93):** add two deterministic K4 plants — `ghp_<36>_` (right `_`) and `_ghp_<36>`
   / `9ghp_<36>` (left `_` and digit) — and make K7's `live-n9`/`live-n11` boundary draws explicit
   (`_` and a digit, not `r.choice`), then name them in `CLAUSES`. No instrument change.
2. **C1 counter (round 93):** have M3 refuse (or verify) a map row whose file is not in the measured
   scope; M9/M10 currently accept such a pair without an application check.
3. **Integration (this wave):** commit the four-entry re-anchor that is already in the working tree;
   record 437/438 as quote-level repairs (drop the stale quote, not the pointer) for a later tranche.

## 9. Re-runnable commands

```
# C1 frozen predicate (13 s)
python3 -B .ufo/waves/round-92/c1/knowledge-meter.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --base-rev 0628fd247914555838a42c02ba5d4ac08b7e095d --after-rev cb1ef2b9856df79c530f3ff1374fa9691ff56233 \
  --map .ufo/waves/round-92/c1/repair-map.tsv --labels-rev d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d \
  --base-target 947/1947 --target 960/1944 --map-sha256 6d87cafaec99961a15c00967d30c2bb164ed480d8b3fbaeadccd55b048d9b772 --work $S

# C2 frozen predicate at a seed (15 s each)
python3 -B .ufo/waves/round-92/c2/capability-check.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --rev 58c0c115342877ee556cae19928d69839b0b29f0 --work $S \
  --instrument-sha256 04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e \
  --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 --seed 9191

# D-1: rebuild the right-underscore mutant in a scratch clone at the landing rev, change exactly
#   gh[pousr]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])  ->  ...{36}(?![A-Za-z0-9])
# commit it in the clone, then run the counter above with --lane <clone> --rev HEAD and no
# --instrument-sha256. Result: K1-K8 pass at seeds 9191 and 1 (CriticClaims-receipts/c2-mutants.txt).
```

## 10. Bounds

No lane writes outside `.ufo/waves/round-92/w1/CriticClaims*`; no counter, instrument, snapshot or
frozen byte copied into the wave dir; no credential-shaped value written (fixtures and mutants lived
in scratch; receipts carry sha256 digests, LIMB lines and paths only). Every wave file written by this
seat was scanned with the landed instrument before yield: `CAPTURE-SECRET-SCAN mode=files scanned=11
hits=0 files=0 rc=0`. No git/jj mutation in the lane; fixture repos were `--shared` clones in scratch
with asserted `rev-parse --show-toplevel`. Scratch `/fast/scratch/hyaku/kasegi-r92/CriticClaims`
deleted before yield. No tool installed or upgraded.

## Files written

- `.ufo/waves/round-92/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c1-frozen-run.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c1-forgery.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c1-excluded-additivity.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c1-labels-and-excluded.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c2-frozen-run.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c2-boundary-probe.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c2-mutants.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/c2-source-anchors.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/freeze-order.txt`
- `.ufo/waves/round-92/w1/CriticClaims-receipts/p2-p3.txt`

