# CriticClaimsC2 — round 97, C2 (capture-secret-scan, ten GitLab families)

Seat: leaf critic. Claim C2, landing `a9a53608dce6aea07d298bb9d5133532078eb1dd`, base
`b06af5e07efbd961a8449f7de6b57eeea62c6bd3`, freeze `daf7fc6a627d615178c27594110e956e592e4cd9`.
Frozen predicate: K1–K6 in `.ufo/waves/round-97/claims.json`. Nothing below edits the claim, the
counter, the instrument or the axes; findings are routed qualifiers only.

## Verdict

**C2 STANDS on K1–K6 at `a9a5360`.** Every limb re-derived by this seat: the gate at three seeds of
my own (7001, 7002, 7003) plus an independent 88-case boundary audit of the ten shape regexes
against byte-exact Python translations of S140 lines 101/160/174/190/213/229/278/341/392/412, plus a
base-vs-new differential scan at two revisions. No routed defect re-scores a limb.

| Limb | Verdict | My numbers (re-derived, not copied) |
|---|---|---|
| K1 instrument | **STANDS** | `inst_sha=pin-ok` (`59909fc4…`), `gate_sha=pin-ok` (`8b6f8493…`), `selftest=pass cases=148` rc=0; base instrument at `7ef1d365` prints `cases=128` rc=0 |
| K2 clean | **STANDS** | landing: `rc=0 scanned=3018 hits=0 allowed=27 unused_allow=0` at all three seeds |
| K3 planted | **STANDS** | `rc=1 hits=10 missing=none extra=none` at all three seeds; nonce-derived paths, ten positives, ten boundary negatives |
| K4 discrim | **STANDS** | `base_new_shape_hits=0 old_shapes_missing=none`; static: base 25 shape ids, new 35, added = exactly the ten, removed = none; base and new both carry all 19 earlier ids |
| K5 table | **STANDS** | exactly one `capture-secret-scan` row in `## Capabilities` (line 307), 4-column header, last cell `87`, all ten round-97 ids named with S140 line refs |
| K6 history | **STANDS** | `252df0c9`: `rc=1`, `aws-sts-session-token` present; base and new produce an identical 6-hit / 2-file set at that revision |

Pins recomputed by this seat: counter `1d87da672ffe…` = `counter_sha256`; instrument at the landing
`59909fc4d708…` = `instrument_sha256`; gate `8b6f84934915…` = `gate_sha256`. The landing commit
touches exactly `SCORECARD.md` and `corpus/instruments/capture-secret-scan.py` (+78/−6).

## Independent shape audit — 88 cases, 7 divergences, 0 cross-fires

Each instrument regex was compared against a byte-exact Python translation of the S140 rule
(`[[:punct:]]` = ASCII punctuation, `[[:space:]]`/`[[:blank:]]` = whitespace). 81 of 88 cases agree.
The seven divergences are all boundary-class, none of them a false hit on a well-formed token:

1. **`_` terminator, the five `[[:punct:]]` families** (registration, `feed_token=`, `gloas-`,
   `glft-`, `glsoat-`): S140 accepts, the instrument refuses. The instrument enforces "exactly N
   characters from the token alphabet" — the claim's own wording — while POSIX `[[:punct:]]`
   includes `_`. Narrowing, and the stricter reading is the correct one.
2. **`-` terminator, registration**: same class (S140's `[[:punct:]]` includes `-`). Narrowing.
3. **non-ASCII byte after a registration token**: S140 refuses, the instrument matches a 20-char
   prefix of a 21-byte token. The only divergence in the permissive direction; it can fire only on
   a malformed token. Note only.
4. **`gitlab+deploy-token-` preceded by a word character**: S140 matches (the rule has no left
   boundary), the instrument refuses (`_GL_LB` added). Narrowing; a URL is delimited by `/`, `"`,
   `?` or a `%XX` escape in practice, and all of those pass.

Exact-length checks all bind: 19/20/21 for the fixed-length families; 19/20/25/26 for `glimt-`;
49/50/51 for `glagent-`. `glimt-` refuses upper-case and mixed-case tails and accepts digits
(S140 `[0-9a-z]`). The deploy-token URL form refuses a missing `@`, a 19- or 21-character token and
a digit-less instance id. The `glagent-` right boundary is exactly S140's
`[^0-9a-zA-Z_\-.]|\.[^0-9a-z]|\.$|$`: `.`+lower/digit refused, `.`+upper/`_`/end-of-input accepted,
`-`/`_`/letter refused.

**No shape swallows a plain token of the same family.** The three versioned-`glagent-` fixtures fire
only `gitlab-agent-token-versioned`; the new plain-50 shape never fires on a versioned token,
including a versioned token whose first segment is exactly 50 characters (the `\.[0-9a-z]` clause
does its job). No case in the 88 fires two shapes.

## Counterexample attempts

**A. New shape on the lane's own evidence at an earlier revision.** At `7ef1d365` and at the base
`b06af5e`, the new instrument fires `gitlab-deploy-token-in-url` on
`.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:76` (43-byte match); the
base instrument fires nothing there. The round-97 redaction `b3c2aff` removed that literal (its
receipt carries the row `…/08-unlisted-classes.txt … gitlab-deploy-token-in-url=1`), so at the
landing the same file has 0 matches. Not a live defect at the landing — it shows the redaction was
load-bearing for the new shape.

**B. K6 breadth.** The frozen limb checks one shape on one revision. I ran base and new over
`252df0c9`: identical HIT sets (6 hits, 2 files, `allowed=16 unused_allow=10 rc=1`), and over the
whole id set new ⊇ base (35 vs 25, removed = none). No earlier shape lost.

**C. K4's static half.** `OLD_SHAPES` is a hardcoded 19; the base instrument has 25 ids — the other
six are gate shapes (`authorization`, `bearer`, `credential`, `op-ref`, `private-key`,
`session-cookie`) that the limb does not name. They are not at risk: the direct name-set diff shows
new ⊇ base, so nothing is dropped.

## Routed qualifiers — none re-scores a limb

- **Q1 (stale docstring, cosmetic).** `.ufo/waves/round-97/c2/capability-check.py` line 18 (K1
  docstring) says "cases >= 128" while line 212 enforces `>= 148`. A reader could take the floor for
  128.
- **Q2 (provenance of the receipt repair).** The 152-literal / 19-file round-96 receipt redaction is
  carried by `b3c2aff` (round-97 redaction, an ancestor), not by the C2 landing `a9a5360`, which
  touches only two files. The state at the landing is repaired — I counted 152
  `[<shape>-fixture-redacted-r97]` markers and 0 residual shape matches across those 19 files — so
  the state-based statement holds; the commit-attribution reading does not.
- **Q3 (surface attribution).** "the ten … the round-96 known-limits list named": the round-96
  docstring known-limits block names nine (six prefixes plus the registration token, `feed_token=`
  and the deploy-token URL); the plain `glagent-` 50 form was CriticHarm **D1**'s routed defect
  ("the known-limits list drops `glagent-` entirely"), which the surface's own parenthetical already
  says. Wording only; the set of ten is right.
- **Q4 (S140 boundary fidelity).** The four divergence classes above. The `_`/`-` strictness is the
  claim's "exactly N"; only the non-ASCII widening departs in the permissive direction and it
  requires a malformed token.

## Impacted axes

- **coverage (8, held):** no change. The ten families bind to S140's published lengths, alphabets and
  terminators; no earlier shape was lost; no new shape double-fires.
- **depth:verifiability:** not touched by this seat.

## Smallest safe correction

None required for the verdict. If the lane wants the counter self-consistent, change the K1
docstring's `>= 128` to `>= 148` (one line, no behaviour change). Leave the `_`/`-` strictness
alone — it implements "exactly N", and S140's punctuation terminator is the looser reading.

## Receipts

All outputs under `.ufo/waves/round-97/w1/CriticClaimsC2-receipts/`; scripts included there so every
number is re-runnable. No credential value is printed anywhere (line numbers and match lengths only).
Scratch `S=/fast/scratch/hyaku/kasegi-r97/CriticClaimsC2`, removed at seat exit.

| # | Command | Observed |
|---|---|---|
| 1 | `git clone -q --no-hardlinks . "$S/lane"` then `git -C "$S/lane" rev-parse --show-toplevel` | prints `$S/lane`; `cat-file -t a9a5360` = `commit` |
| 2 | `python3 -B .ufo/waves/round-97/c2/capability-check.py --lane "$S/lane" --rev a9a5360… --work "$S/work-<seed>" --instrument-sha256 59909fc4… --gate-sha256 8b6f8493… --seed <7001\|7002\|7003>` | rc=0 each; K1–K6 all `ok`; `CAPABILITY-CHECK-RESULT pass rc=0` (9 lines each; `gate-seed-700{1,2,3}.txt`) |
| 3 | `sha256sum .ufo/waves/round-97/c2/capability-check.py .ufo/waves/round-97/c2/candidate-scanner.py`; `git show a9a5360:corpus/instruments/{capture-secret-scan,claim-package-check}.py \| sha256sum` | counter `1d87da672ffe…`, instrument `59909fc4…`, gate `8b6f8493…` — all equal the pins |
| 4 | `python3 -B "$S/work-7001/inst-{rev,base}/…/capture-secret-scan.py" --selftest` | new `SELFTEST-RESULT pass cases=148` rc=0; base `cases=128` rc=0 (`selftest-{new,base}.txt`, 149/129 lines) |
| 5 | `python3 -B "$S/independent-shapes.py"` | `INDEPENDENT-SHAPES cases=88 divergences=7 cross-fire=3`; `OLD-SHAPES present=19/19 lost=none`; `SHAPES-ADDED` = the ten; rc=1 from the divergence count (`independent-shapes.txt`, 93 lines) |
| 6 | `python3 -B "$S/extra-checks.py"` | `SHAPES base=25 new=35 added=<ten> removed=none`; `OLD-SHAPES base=19/19 new=19/19`; K5 `rows_in_file=1 last_cell='87' named_all=True`; `REDACTION round96_files=19 base_shape_matches=152 landing_markers=152 landing_residual=0`; `DEPLOY-URL-FIXTURE` 1 match at `7ef1d365`/`b06af5e`, 0 at `a9a5360` (13 lines, `extra-checks.txt`) |
| 7 | `python3 -B <inst> --lane "$S/lane" --rev 252df0c9… --allow <landing allow>` for base and new | both rc=1, 6 HIT lines / 2 files, `allowed=16 unused_allow=10`; `diff` of the shape sets identical (`diff-{new,base}-252df0c9….txt`, 7 lines each) |
| 8 | same for `--rev 7ef1d365…` | new rc=1 with one `gitlab-deploy-token-in-url` HIT (round-94 SentinelShapes receipt line 76); base rc=0, 0 HIT lines (`diff-new-7ef1d365….txt` 2 lines, `diff-base-7ef1d365….txt` 1 line) |
| 9 | `git show a9a5360:SCORECARD.md \| grep -n capture-secret-scan`; `git show --stat a9a5360` | row at line 307 only; landing stat = 2 files, +78/−6 |
| 10 | `git show --name-only b3c2aff \| grep -c round-94`; `git show a9a5360:<receipt> \| grep -o '\[[a-z0-9-]*-fixture-redacted-r97\]' \| sort \| uniq -c` | 1; `5 aws-access-key-id`, `2 credential`, `1 private-key` markers in the sampled receipt |

No tool was installed or upgraded for this seat (python3, git, grep, sed only). No git/jj mutation
was run: the only repository writes are the report and the receipts directory named by the seat.
