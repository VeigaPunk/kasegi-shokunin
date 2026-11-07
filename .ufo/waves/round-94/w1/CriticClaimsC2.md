# CriticClaimsC2 — round 94, C2 (capture-secret-scan: GitLab custom instance prefix, runner auth token, deploy token)

Seat: leaf critic, no dispatch. Lane: kasegi. Landing under attack:
`996460861d4130ddb2da6b7554e905d3e47504a3` (parent `d51220ae…` = C1 landing; freeze `96b5033f…`;
base `dff5a0a0…`). Every command ran in `/home/vgpnk/Projects/shokunin/kasegi-shokunin` or in a fresh
`git clone --shared` of the lane at `/fast/scratch/hyaku/kasegi-r94/CriticClaimsC2/fx.3krj/lane`
(`git rev-parse --show-toplevel` asserted equal to the clone dir before any commit; scratch removed at exit).

Axes under test: `coverage` (8 held) — capability extension of `capture-secret-scan`, sourced S140.

## Verdict

**DOES-NOT-STAND — the frozen predicate (P1 ∧ P2 ∧ P3 ∧ P4) is not satisfied: P4 fails as written.
P1, P2 and P3 STAND, re-derived independently.**

P1 is re-derived at the landing in a fresh shared clone at the printed run-time seed (2323026125) and at
seeds 1 and 9191, rc=0 with all nine limbs pass each time. P2 is re-derived: the landed
`capture-secret-scan.py` is `22ba32d1…67beaf` and the landed `claim-package-check.py` is `8b6f8493…1cc8e6`,
both equal to the frozen pins. P3 is re-derived: the landing diff against its parent names exactly
`SCORECARD.md` and `corpus/instruments/capture-secret-scan.py` (two `M` records, no mode change), and the
landed `| capture-secret-scan |` row is byte-identical to `candidate-row.txt`
(sha256 `4f10e273…4beed8`, 3397 bytes, last cell `87`, one row).

P4 does not stand as written. It names a tenth control — "the S140-allowlist-removed control" — that is
absent from the frozen receipt, absent from the frozen driver, and vacuous on the frozen artifact set; the
receipt's tenth control is `tampered-instrument`, a sha-pin control. See "P4 — counterexample" below. This is
an evidential/predicate defect, not a capability regression: every limb the claim asserts is green at three
seeds, and all four forgeries this seat was told to build are rejected by behavioural limbs.

## P1 — counter at the landing, three seeds (re-derived)

Fresh `git clone --shared` of the lane, checked out at the landing (`git rev-parse HEAD` =
`996460861d…`). Counter run with the frozen pins
`--instrument-sha256 22ba32d1…67beaf --gate-sha256 8b6f8493…1cc8e6`:

| run | seed | nonce | rc | limbs |
|---|---|---|---|---|
| `02-run-seed-auto.txt` (no `--seed`) | 2323026125 (printed) | `6c289b8c` | 0 | K1–K9 pass |
| `03-run-seed-1.txt` | 1 | `d42a16ca` | 0 | K1–K9 pass |
| `04-run-seed-9191.txt` | 9191 | `8b84535f` | 0 | K1–K9 pass |

Stable limb detail across all three: K1 `selftest_rc=0 instrument_sha256=22ba32d1…67beaf
gate_sha256=8b6f8493…1cc8e6`; K2 `rc=1 sts_files=2 oracle=2 oracle_matches_expected=True`;
K3 `rc=0 scanned=2224,hits=0,files=0,allowed=24,unused_allow=0`; K4 `rc=1 missing=none extra=none
sts_allow_rc=2 files_rc=1 files_hits=2 files_ok=True` with a different nonce per run; K6 `base_rc=1
base_hits=22 new_caught_by_base=none outside_plants=none`; K9 `prev_rc=1 prev_hits=39 lost=none
prev_caught_new=none`; K7 `rc=1 missing=none extra=none` at each seed; K8 `clauses=61 failing=none`;
K5 `rows=1`. Verdict line `CAPABILITY-CHECK-RESULT pass rc=0` in all three.

## P2 — pins (re-derived from the clone's rev, not the working tree)

`sha256sum` inside the clone at the landing:
`22ba32d145f90f7759caf16d3ee524eb1779153d3f2a33611675a93a4667beaf  corpus/instruments/capture-secret-scan.py`
= frozen `candidate_sha256`; `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6
corpus/instruments/claim-package-check.py` = frozen `gate_sha256`. Both match `claims.json` verbatim.

## P3 — path set and row bytes (re-derived)

`git diff --name-status` (and `--raw`) `d51220ae…` → `99646086…`: exactly two paths, both `M`:

```
:100644 100644 20a406f bd46aad M	SCORECARD.md
:100755 100755 396b233 0f4653e M	corpus/instruments/capture-secret-scan.py
```

`git rev-list --parents -n1 99646086…` prints `99646086… d51220ae…`, so the C2 landing sits directly on the
C1 landing. The landed `| capture-secret-scan |` capability row: one occurrence, 3397 bytes,
sha256 `4f10e273f3c27e5b43cec77b280071d13284c3c475e976ac160bb674ca4beed8` — equal to
`candidate-row.txt` byte for byte (`byte_equal=True`), last cell `87`. The pre-landing row is a different,
shorter row (2730 bytes, sha256 `6d18d579…`), so the row genuinely moved.

Statement-level details re-checked against the landed bytes: the three regexes are
`_GL_LB + _GL_PREFIX + "glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"`,
`…"glrtr?-(?:t[1-3]_)?[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"` and
`…"gldt-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"` with `_GL_PREFIX = "(?:[A-Za-z0-9]{1,20}-)?"`; S140 lines
4/114/255 quote the vendor's own three regexes and are unredacted (the capture is 563 lines, ending
`pipeline = true`); and the round-93 known limit ("GitLab runner (`glrt-`) and other GitLab token prefixes")
is gone from the landed docstring, replaced by routable/versioned, JWT-form and remaining-prefix limits
(receipt 07).

## P4 — counterexample: the named tenth control does not exist

P4 requires the receipt to print `C2-CONTROLS-RESULT pass controls=10` with, in its own words,
"candidate rc 0 pinned; do-nothing, the six forgeries F1-F6, the round-93 row and the S140-allowlist-removed
control each rc 1". The frozen receipt (`controls/c2-controls-r94.txt`, 122 lines) prints:

```
candidate rc=0 want=0 · do-nothing rc=1 · F1-path-shape-keyed rc=1 · F2-harness-gated rc=1 ·
F3-drop-github rc=1 · F4-loose-runner rc=1 · F5-literal-keyed rc=1 · F6-always-clean rc=1 ·
row-round93 rc=1 · tampered-instrument rc=1
C2-CONTROLS-RESULT pass controls=10
```

There is no `S140-allowlist-removed` / `s140-allow-rows-removed` control anywhere: `grep -rn
'allow-rows|allowlist-removed|allow-removed' .ufo/waves/round-94/controls/` = 0 hits; `grep -c S140
c2-controls-r94.py` = 0 (the receipt's five `S140` occurrences are K8 clause names inside FAIL detail
lines, not a control); and the frozen `claims.json` C2 `controls` field is the only place the name appears.
The tenth executed control is the pin control at driver line 130 — a clone, an appended `# tamper` line, a
commit, and `--instrument-sha256 <isha>`, i.e. K1 rejects it on the sha, which is a different wall.

The named control is also *vacuous on this artifact set*: `capture-secret-allow.tsv` has 23 data rows and
**zero** rows naming `round-94` or `S140`, so "remove the S140 allow rows" is a no-op that leaves the
candidate command byte-identical — it would exit 0, not the `rc 1` P4 requires. So P4's enumeration cannot be
satisfied by executing it either: it was either unexecuted (as recorded) or self-defeating (if executed
literally). The predicate's machine-checkable conjunct therefore fails, and no post-landing edit may repair
it (`claims.json` is frozen).

Note this is exactly the class the critic role exists to catch — an evidence identity substituted without
the predicate changing — and it is *not* a capability finding: P1's K1–K9 at three seeds and the four
forgery classes rejected below are independent of it.

For fairness to the claim text: the round-94 C2 kill rule lists only "any limb FAIL at the landing at any of
the three seeds, or P3 naming another path set", so a reader can argue the P4 parenthetical was meant
descriptively and the substitution of the tenth control was harmless. But P4 is a conjunct of the frozen
predicate, it is machine-checkable, and a check for the control it names fails on the frozen bytes; nobody
may edit `claims.json` after the freeze to reconcile the two. The verdict below is on that conjunct. If the
L1 reads the parenthetical as non-substantive, P1–P3 fully support the capability and the only remaining
action is qualifier 1's wording fix.

## Attacks on the counter's own guards (this seat's assigned battery)

Each forgery is a fresh `git clone --shared` of the landing, checked out at the landing, instrument patched,
committed, and run with `--gate-sha256 8b6f8493…1cc8e6 --seed 4242` and **no** `--instrument-sha256`, so the
forgery reaches the behavioural limbs instead of dying on the pin (the frozen controls' own protocol). A
second run per forgery keeps the instrument's `--selftest` green so that K1 cannot be the wall.

| forged instrument | sha256 | K1 | rejecting limbs | observed detail |
|---|---|---|---|---|
| A path-keyed on `round-1/` + `S\d{3}.txt` (+ preserved `live-`, `*-receipts/`) | `70399bd4…` | FAIL `selftest_rc=1` | K1, K4, K9, K8 | K4 `missing=29 extra=0`; K9 `lost=25`; K8 23 clauses; K2 **pass** |
| A2 same, selftest kept green | `bb82709b…` | pass | **K4, K9, K8** | K4 `missing=29 extra=0` (15/44 pairs still reached, all `w/…-receipts/live-*`); K9 `lost=25`; K8 23 clauses |
| B harness-gated on `/<c2check|plant|gen>-…` in `--lane` | `140c0f94…` | pass | **K4, K7, K9, K8** | K4 `rc=0 missing=44`; K7 `rc=0 missing=17`; K9 `lost=39`; K8 35 clauses; K2/K3 pass |
| C `gldt-` tail `{20}` → `{3,}` | `ed66b71e…` | FAIL | K1, K4, K7, K8 | K4 `extra=2`; K7 `extra=1` (`live-n17.txt`); K8 2 clauses (19-char, 21-char deploy tails) |
| C2 same, selftest kept green | `64b56aa4…` | pass | **K4, K7, K8** | K4 `extra=2`; K7 `extra=1`; K8 2 clauses |
| D drop `GITHUB_PATTERNS` from `patterns()` | `f8860ae8…` | FAIL | K1, K4, K9, K7, K8 | K4 `missing=11`; K9 `lost=11`; K7 `missing=4`; K8 16 clauses |
| D2 same, selftest kept green | `ddfe8b73…` | pass | **K4, K9, K7, K8** | K4 `missing=11`; K9 `lost=11`; K7 `missing=4`; K8 16 clauses |

No SURVIVOR. Each named forgery is rejected, and with K1 neutralised the walls are K4's exact
`(path, shape)` set equality (both directions), K7's run-time-drawn values, K8's clause map and K9's
"previous landing loses nothing" limb — four independent limbs, not one.

## Qualifiers (routed; none of these re-scores P1–P3)

1. **The statement's "a path-shape-keyed detector finds nothing" is stronger than the relocation delivers.**
   `relocate()` keeps the path class: `corpus/source-snapshots/r<nonce>/…`, `corpus/practice/p<nonce>/…`,
   `w/n<nonce>/<hash>-receipts/…`, and it keeps the `live-` basename prefix. A path key on those classes
   admits 15 of the 44 planted pairs — the 13 `w/…-receipts/*` plants (including one whose basename carries
   no `live-`) and the two `w/*/live-*.html` plants; receipt 09 lists them, verified by set difference
   against `PLANT_EXPECT` with the run nonce `3d63872e`. It cannot *name* the shape from the path, which is
   why K4/K8 still reject it — but "finds nothing" should read "cannot pass", and the next round's M93-4
   lesson should not over-claim.
2. **K1's selftest is the first wall for a careless forger, not the load-bearing one.** For A, C and D the
   instrument's own `--selftest` flips to `rc=1` (the selftest fixtures carry no plant-path shape; the
   deploy 19/21-char negatives; the GitHub positives). That is a weak rejection — a forger edits the
   selftest too — so the A2/C2/D2 variants were run with the selftest filtered, and K4/K7/K8/K9 still
   rejected all three. The counter's rejection does not depend on the instrument policing itself.
3. **The receipt's `candidate=1ab01c98…` is a fixture clone HEAD, not a lane revision.** P4's "candidate rc 0
   pinned" is carried by the instrument sha256 in the same line, not by that SHA; nobody should read
   `1ab01c98…` as evidence about the lane.
4. **K3's `allowed=24` vs 23 data rows** is not a contradiction, measured not assumed: 23 rows, all 23 used
   (`unused_allow=0`), 24 allowlisted matches, three `(path, shape)` pairs carrying more than one allowed
   value (receipt 08). Recorded so a later reader does not read `24` as a stale-row defect.

## Impacted axes

- `coverage` (8 held): **unchanged**. The capability is re-derived at the landing — three new shapes with the
  frozen alphabets/boundaries, the retired `glrt-` limit, relocated plants, K9 — and no attack this seat
  built survives. Nothing here justifies a coverage downgrade.
- Claim-package verifiability: **blocked at P4 as written**. The frozen predicate names a control the frozen
  evidence does not contain, so no re-run can make P4 true; the axis score cannot be booked against P4 until
  the enumeration is corrected. This is the freeze's defect, not the landing's.

## Smallest safe correction

Replace P4's parenthetical item "the S140-allowlist-removed control" with "the tampered-instrument pin
control" — that is the control that was executed and that the receipt evidences (with the note that the C2
allowlist holds no S140 rows, so no allowlist-removal control is meaningful here). Do it at the next
freeze-capable point together with the `claims.json` `controls` field, which carries the same misnomer
(`s140-allow-rows-removed`). If instead a genuine allowlist-removal control is wanted, it must first create
an S140 row to remove, and it then belongs to a new freeze, not to this predicate. Everything else in P1–P3
and the claim statement can stand as landed; no counter, scanner or row change is needed.

## Receipts

All under `.ufo/waves/round-94/w1/CriticClaimsC2-receipts/`; every line below is observed output.

| receipt | command (cwd = lane root unless noted) | rc | lines |
|---|---|---|---|
| `01-rederive-p2-p3.txt` | `git -C <clone> rev-parse --show-toplevel` / `HEAD` / `log -1 --format='%H %P %s' 99646086…`; `sha256sum` both instruments; `git diff --name-status` and `--raw` and `--stat d51220ae… 99646086…`; python row-vs-`candidate-row.txt` byte compare | 0 | 26 |
| `02-run-seed-auto.txt` | `python3 -B .ufo/waves/round-94/c2/capability-check.py --lane <clone> --rev 99646086… --work <scratch> --instrument-sha256 22ba32d1… --gate-sha256 8b6f8493…` | 0 | 11 |
| `03-run-seed-1.txt` | same with `--seed 1` | 0 | 11 |
| `04-run-seed-9191.txt` | same with `--seed 9191` | 0 | 11 |
| `05-forgery-A…` / `A2…` | `CriticClaimsC2-forges.py` (A) and `CriticClaimsC2-forges-selftest-green.py` (A2): clone at landing, patch, commit (toplevel asserted), counter `--rev HEAD --gate-sha256 8b6f8493… --seed 4242`, no instrument pin | 1 (counter) | 17 each |
| `05-forgery-B…` | same driver, harness-gated patch | 1 | 17 |
| `05-forgery-C…` / `C2…` | same drivers, `gldt-` `{20}`→`{3,}` | 1 | 17 each |
| `05-forgery-D…` / `D2…` | same drivers, `GITHUB_PATTERNS` dropped from `patterns()` | 1 | 17 each |
| `06-controls-receipt-audit.txt` | `grep -n '^C2-CONTROLS\|^CONTROL ' c2-controls-r94.txt`; `grep -n 'record("' c2-controls-r94.py`; python extract of P4 + `controls` field; `grep -rn allow-rows\|allowlist-removed` (0); `grep -c S140` driver (0) / receipt (5); `grep -vc '^#' capture-secret-allow.tsv` (23); `grep -c 'round-94\|S140'` allowlist (0); `sed -n 119,131p` driver (ctl-tamper) | 0 | 47 |
| `07-s140-anchors-and-known-limits.txt` | `wc -l S140.txt` (563); `sed -n 4p/114p/255p`; `git show 99646086…:…capture-secret-scan.py` GITLAB_PATTERNS; base vs landing `Known limits:` paragraphs; frozen `source-recheck-r94.txt` | 0 | 54 |
| `08-allowlist-and-capture-shape.txt` | landed instrument imported in-process: `load_allow` + `tree_blobs` + `scan_bytes` over the landing rev → rows/used/matches; `wc -l S140.txt`, `tail -1`, last byte | 0 | 9 |
| `09-path-key-reach.txt` | counter module imported; `PLANT_EXPECT` relocated with the A2 nonce `3d63872e`; set difference against A2's K4 `missing=` list → 15 found pairs listed | 0 | 17 |
| `CriticClaimsC2-forges.py`, `CriticClaimsC2-forges-selftest-green.py` | the two attack drivers as run (kept here because the scratch is deleted at seat exit) | — | 2 files |

Clone provenance (receipt 01): `git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin
<scratch>/fx.3krj/lane`, `rev-parse --show-toplevel` = `<scratch>/fx.3krj/lane`, `rev-parse HEAD` =
`996460861d4130ddb2da6b7554e905d3e47504a3`. No git/jj mutation ran in the lane; the only commits were made
inside scratch clones after their toplevel was asserted. No tool was installed or upgraded for this seat.
