# MutC2Counter — round-97 C2 mutation probe

Seat `MutC2Counter` (leaf; no subagents). Lane `kasegi`; working dir
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `b06af5e0…`, freeze
`daf7fc6a…`, C2 landing `a9a53608…`. Scratch
`/fast/scratch/hyaku/kasegi-r97/MutC2Counter` (created and removed on exit).

## What was attacked

The frozen C2 counter `.ufo/waves/round-97/c2/capability-check.py`
(sha256 `1d87da67…`) run against the landed instrument
`corpus/instruments/capture-secret-scan.py` (sha256 `59909fc4…`, the frozen
pin) and fourteen variants of that instrument: the ten single-point boundary
mutants this seat names, plus four gate forgeries. Each variant is a commit in
a `git clone --shared` of the lane at `a9a5360`; blobs, trees and commits were
built with plumbing (`hash-object`, `read-tree`, `update-index`, `write-tree`,
`commit-tree`, `update-ref`) so the lane and the clone worktree were never
written. Every gate run used `--seed 4242` and its own `--work` directory.

## Guard: the sha pin

Every variant is refused by K1 on the instrument pin before behaviour is
considered — e.g. M01 `LIMB K1 FAIL inst_sha=6b65cb1a… gate_sha=pin-ok
selftest=pass cases=148`, F01 `inst_sha=bb293093…`. The behavioural reading
below is the same gate run with `--instrument-sha256` omitted; K1 then checks
only the selftest. K4 and K5 cannot catch an instrument mutant by construction
(K4 imports the *base* instrument; K5 reads `SCORECARD.md`), so the
discriminating limbs are K1(selftest), K2, K3 and K6.

## Mutant results

| variant | single point | pin | no-pin limbs | verdict | caught by |
|---|---|---|---|---|---|
| M01-glagent-right-boundary | drop `(?![A-Za-z0-9_-]\|\.[0-9a-z])` on `glagent-{50}` | K1 FAIL (sha) | all ok | **SURVIVED** | no fixture |
| M02-glagent-49-or-51 | `{49}\|{51}` on `glagent-` | K1 FAIL (sha) | K1 FAIL, K3 FAIL | **KILLED** | K1 selftest `gl-kubernetes-agent` + `-short`; K3 p10 missing / n10 extra |
| M03-glimt-upper | `glimt-[A-Za-z0-9]{20,25}` | K1 FAIL (sha) | K1 FAIL, K3 FAIL | **KILLED** | K1 selftest `gl-incoming-email-upper`; K3 n5 extra |
| M04-deploy-url-no-at | drop `@` on `gitlab+deploy-token-N:` form | K1 FAIL (sha) | K1 FAIL, K3 FAIL | **KILLED** | K1 selftest `gl-deploy-token-in-url-no-at`; K3 n7 extra |
| M05-glsoat-19-or-21 | `glsoat-{19,21}` | K1 FAIL (sha) | K1 FAIL, K3 FAIL | **KILLED** | K1 selftest `gl-scim-oauth-short`; K3 n6 extra |
| M06-gloas-63 | `gloas-{63,64}` | K1 FAIL (sha) | K1 FAIL, K3 FAIL | **KILLED** | K1 selftest `gl-oauth-app-short`; K3 n3 extra |
| M07-glft-21 | `glft-{20,21}` | K1 FAIL (sha) | K1 FAIL, K3 FAIL | **KILLED** | K1 selftest `gl-feed-token-v2-long`; K3 n4 extra |
| M08-glsoat-no-left-boundary | drop `_GL_LB` on `glsoat-` | K1 FAIL (sha) | all ok | **SURVIVED** | no fixture |
| M09-glsoat-custom-prefix | add `_GL_PREFIX` to `glsoat-` | K1 FAIL (sha) | all ok | **SURVIVED** | no fixture |
| M10-feed-token-case-insensitive | `(?i:feed_token=)` | K1 FAIL (sha) | all ok | **SURVIVED** | no fixture |
| F01-literal-locked | ten shapes match only the fixture literals | K1 FAIL (sha) | all ok → gate PASS | **FORGERY SURVIVED** | none |
| F02-rev-mode-blind | `--rev` drops the cloud patterns | K1 FAIL (sha) | K2 FAIL | **CAUGHT** | K2 `allowed=25 unused_allow=2` (two cloudfront allow rows unused) |
| F02b-rev-mode-blind-gitlab | `--rev` drops every GitLab shape | K1 FAIL (sha) | all ok → gate PASS | **FORGERY SURVIVED** | none |
| F03-blanket-files | `--files` reports all ten shapes for every file | K1 FAIL (sha) | K3 FAIL | **CAUGHT** | K3 200 (path,shape) pairs vs 10 expected, 190 extras |

Killed mutants, exact selftest failures (`07-killed-selftest-fails.txt`):

- M02: `gl-kubernetes-agent FAIL got=none` and `gl-kubernetes-agent-short FAIL got=gitlab-kubernetes-agent-token`; K3 `missing=[(…-p10.txt, gitlab-kubernetes-agent-token)] extra=[(…-n10.txt, …)]`.
- M03: `gl-incoming-email-upper FAIL got=gitlab-incoming-email-token`; K3 extra `…-n5.txt`.
- M04: `gl-deploy-token-in-url-no-at FAIL got=gitlab-deploy-token-in-url`; K3 extra `…-n7.txt`.
- M05: `gl-scim-oauth-short FAIL got=gitlab-scim-oauth-token`; K3 extra `…-n6.txt`.
- M06: `gl-oauth-app-short FAIL got=gitlab-oauth-app-secret`; K3 extra `…-n3.txt`.
- M07: `gl-feed-token-v2-long FAIL got=gitlab-feed-token-v2`; K3 extra `…-n4.txt`.

All six are caught twice: by the instrument's own selftest (K1) and by the
gate's independent planted corpus (K3). The plant negatives that fire are
exactly the one-character boundary negatives the claim's falsifiable rule
names (19/21 for the 20-length families, 63 for `gloas-`, 49/51 for the plain
`glagent-` form, upper-case for `glimt-`, no-`@` for the URL form).

## Survivors — coverage findings (routed defects, no re-score)

Each survivor was re-checked with a direct probe against the pristine
instrument and the mutant (`05-direct-probes.json`), so none is an equivalent
mutant:

1. **M01 (right boundary of `glagent-{50}`).** No fixture exercises the right
   side of this shape: the plant negative and the selftest negative are both
   49 characters (the left side). Probe `glagent-` + 51 `J`: pristine reports
   no hit, M01 reports `gitlab-kubernetes-agent-token`. The published rule
   (S140:213) refuses a 51st token character; the gate cannot see the
   difference.
2. **M08 (left boundary of `glsoat-`).** No round-97 fixture glues a shape to
   a preceding word character (unlike `gl-pat-letter-before` for `glpat-`).
   Probe `xglsoat-` + 20 `F`: pristine no hit, M08 hit.
3. **M09 (custom prefix on `glsoat-`).** Hit/no-hit is unchanged for
   unallowlisted text because `_GL_LB` already admits a hyphen before the bare
   prefix (both instruments hit `acme-glsoat-…`). The difference is the
   matched span: with an allowlist row keyed to the bare value, pristine
   reports `allowed=1` and no hit, M09 reports `hits=1 allowed=0`. No K limb
   exercises a prefixed `glsoat-` against an allowlist row.
4. **M10 (case-insensitive `feed_token=`).** No fixture tests case. Probe
   `FEED_TOKEN=` + 20 `B`: pristine no hit, M10 hit. The published rule
   (S140:160) is case-sensitive.

## Forgeries

1. **F01 — literal-locked shapes (survives).** The ten new patterns were
   replaced by regexes that match only the fixture literals (`GR1348941A{20}`,
   `feed_token=B{20}`, `gloas-C{64}`, `glft-D{20}`, `glimt-e{22}`,
   `glsoat-F{20}`, `gitlab+deploy-token-7:G{20}@`, `glffct-H{20}`,
   `glrct-I{20}`, `glagent-J{50}`). The gate prints
   `CAPABILITY-CHECK-RESULT pass rc=0` with K1-K6 ok. Cause: K1's selftest and
   K3's planted corpus use the *same* literals, so a scanner that cannot
   detect any real GitLab token satisfies both. This is the strongest gate
   finding: K3's plants are not independent of the selftest.
2. **F02 — `--rev` drops the cloud patterns (caught).** K2 reports
   `allowed=25 unused_allow=2`: the two cloudfront allowlist rows go unused,
   so the gate fails. Caught by allowlist bookkeeping, not by shape
   detection.
3. **F02b — `--rev` drops every GitLab shape (survives).** Keeping the gate,
   cloud, AWS and GitHub patterns in `--rev` mode keeps K2 at `allowed=27
   unused_allow=0` and K6 at `aws-sts-session-token`; K3 only exercises
   `--files`. The gate prints `CAPABILITY-CHECK-RESULT pass rc=0`. A scanner
   that is honest only in `--files` mode passes, although `--rev` is the mode
   used on real captures.
4. **F03 — blanket reporting in `--files` (caught).** Emitting all ten shapes
   for every file gives K3 `hits=200` against the expected 10 (190 extras), so
   the gate fails. K3's exact-set comparison has teeth against over-reporting.

## Pristine and restored bytes

- Pristine landing, pin run: `CAPABILITY-CHECK-RESULT pass rc=0`, K1
  `selftest=pass cases=148`, K2 `scanned=3018 hits=0 allowed=27
  unused_allow=0`, K3 `hits=10 missing=none extra=none`, K4
  `base_new_shape_hits=0 old_shapes_missing=none`, K5 `rows=1 last=87
  named=True`, K6 `rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential`.
- After all fourteen variants, the same pin run on the untouched landing
  commit prints the same pass; the lane instrument sha256 is still
  `59909fc4…`, the clone's `a9a5360:corpus/instruments/capture-secret-scan.py`
  blob sha256 is still `59909fc4…`, and the lane HEAD is still `a9a5360`.
- The lane's dirty state (sibling edits such as `M corpus/QUALITY.md`, `M
  corpus/SOURCES.md`, untracked wave files) is not this seat's; the only paths
  written are this report and the receipts directory.

## Verdict

C2 STANDS on its frozen predicate: I re-derived `CAPABILITY-CHECK-RESULT pass
rc=0` with K1-K6 ok at the landing `a9a5360` (pin run, seed 4242) and again on
the restored bytes after all fourteen variants. The sha pin refuses every
mutated instrument (K1 FAIL on `inst_sha`), as designed.

Mutation result: 6/10 required single-point mutants are KILLED (M02-M07, each
by K1's selftest and K3's planted corpus); 4/10 SURVIVE (M01, M08, M09, M10).
Two gate forgeries survive (F01 literal-locked, F02b rev-mode-blind); F02 is
caught by K2's allowlist bookkeeping and F03 by K3's exactness. The survivors
are coverage findings routed to the C2 owner — no shape removal, no boundary
widening, no re-score of the claim. C1 is outside this seat.

## Receipts

All outputs are under `.ufo/waves/round-97/w1/MutC2Counter-receipts/` (46
files; `09-receipt-index.txt` carries sha256 and line counts). Commands and
observed results:

| command | observed |
|---|---|
| `sha256sum corpus/instruments/capture-secret-scan.py .ufo/waves/round-97/c2/candidate-scanner.py .ufo/waves/round-97/c2/capability-check.py corpus/instruments/claim-package-check.py` | rc 0; instrument = candidate = `59909fc4…` (the pin), counter `1d87da67…`, gate `8b6f8493…` |
| `git clone --shared --no-checkout <lane> $S/lane` | rc 0; `rev-parse --show-toplevel` = `$S/lane`; HEAD `a9a5360` |
| `python3 mutants.py` | rc 0; 13 commits (10 mutants + F01/F02/F03) — `01-mutant-manifest.json` |
| `git -C $S/lane diff a9a5360 <variant> -- corpus/instruments/capture-secret-scan.py` | 13 sections, 221 lines — `02-mutant-diffs.txt` |
| `python3 run-gate.py` | rc 0; 28 gate runs (13 variants + pristine × pin/no-pin), 583 s — `03-gate-matrix.txt`, `03-gate-matrix.json` |
| `python3 f02b.py`; two gate runs on F02b | rc 0; no-pin `CAPABILITY-CHECK-RESULT pass rc=0`, pin `fail rc=1` — `04-f02b-manifest.json`, `gate-F02b-…-{pin,nopin}.txt` |
| `python3 probe.py` | rc 0; 10 probe records — `05-direct-probes.json` |
| per-mutant `--selftest` (M02-M07) | rc 1 each; exact FAIL lines — `07-killed-selftest-fails.txt` |
| restoration: `sha256sum`, `git rev-parse`, `git status --porcelain`, gate re-run | rc 0; `CAPABILITY-CHECK-RESULT pass rc=0`; instrument sha unchanged — `06-restoration-before.txt`, `06-restoration-gate.txt`, `06-restoration-after.txt` |
| `gate-<variant>-{pin,nopin}.txt` | 30 files (28 matrix runs + 2 F02b runs); each carries the six `LIMB` lines and `CAPABILITY-CHECK-RESULT` |
| `08-summary.tsv` | 14 rows + header; verdict and catching limb per variant |
| `python3 -B corpus/instruments/capture-secret-scan.py --files <receipts>/* MutC2Counter.md` | rc 0; `scanned=47 hits=0 files=0` — `10-selfscan-receipts.txt` |

No credential values are recorded: every probe and plant value is a repeated
letter fixture, and the receipts carry shape names, paths and line numbers
only. One M08 receipt filename accidentally matched the `glsoat-` + 20 shape;
it was renamed before the final scan, so the receipts and this report scan
clean.
