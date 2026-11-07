# MutC2Scanner — C2 `github-token` mutation probe (round 92, attempt 1)

Frozen subject: C2 counter `.ufo/waves/round-92/c2/capability-check.py`, landing
`58c0c115342877ee556cae19928d69839b0b29f0`. Instrument under test:
`corpus/instruments/capture-secret-scan.py` at that rev, sha256
`04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e` (matches the frozen
pin); gate `claim-package-check.py` sha256
`8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` (matches). Base
`0628fd247914555838a42c02ba5d4ac08b7e095d`.

All counter runs were **unpinned** (no `--instrument-sha256`), against a commit of the
variant in a `git clone --shared` scratch clone. Each commit mirrors `variant()` of
`.ufo/waves/round-92/controls/c2-controls-r92.sh`: `checkout --detach BASE`, replace
`corpus/instruments/capture-secret-scan.py`, patch the single
`| capture-secret-scan |` SCORECARD row with `c2/candidate/scorecard-row.txt`, commit.
Seeds: **9191** plus one `SystemRandom` seed per variant. 16 mutants, each a single
forced replacement inside `_GH_LB` / `_JWT_SEG` / `GITHUB_PATTERNS` bytes. Regenerated
the 10 pre-freeze forgeries (`controls/c2-forgeries.py`) in scratch and compared blob
sha256s: **0 overlap** (`sha-set-compare.txt`), so all 16 are beyond the forgery set.

## Controls

- Pristine landed instrument (sha `04666f67…`), seeds 9191 / 622733741: `rc=0`, K1–K8
  pass both runs (`baseline-candidate.txt`). A kill below is therefore behavioural, not
  a broken baseline.
- Clone toplevel asserted equal to the clone dir before use; read-only git only in the
  lane.
- Restoration: base instrument blob at BASE =
  `89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7`; after all 34
  runs the clone was checked out at BASE and the working-tree instrument hashed to the
  same value, `restored_equal=True` (`restore.txt`). The scratch clone was then removed
  with the scratch root.

## Verdicts (34 runs: 2 pristine + 16 × 2 seeds)

| mutant | single edit | 9191 | random seed | killing limb(s) | own selftest |
|---|---|---|---|---|---|
| M01-classic-len-35-36 | classic `{36}` → `{35,36}` | fail | fail | K1,K4,K7,K8 | FAIL (`gh-35-chars`) |
| M02-right-boundary-drops-underscore | right lookahead `[A-Za-z0-9_]` → `[A-Za-z0-9]` | pass | pass | — | pass |
| M03-prefix-adds-x | `[pousr]` → `[pousrx]` | fail | fail | K1,K4,K8 | FAIL (`gh-unknown-prefix`) |
| M04-appid-empty | app-id digits `{1,20}` → `{0,20}` | pass | pass | — | pass |
| M05-json-any-backslash | JSON lookbehind `(?<=\\n)` → `(?<=\\)` | fail | fail | K1,K4,K8 | FAIL (`gh-installation-json-joined`) |
| M06-jwt-any-separator | JWT separator `rb"\\."` → `rb"."` | pass | pass | — | pass |
| M07-jwt-two-segments | three JWT segments → two | pass | pass | — | pass |
| M08-classic-prefix-ghs-only | classic prefix set → stateless prefix only | fail | fail | K1,K4,K7,K8 | FAIL (4 positives) |
| M09-left-boundary-drops-underscore | left lookbehind `[A-Za-z0-9_]` → `[A-Za-z0-9]` | pass | pass | — | pass |
| M10-classic-tail-allows-dash | classic tail `[A-Za-z0-9]{36}` → `[A-Za-z0-9-]{36}` | pass | pass | — | pass |
| M11-appid-letters | app-id `[0-9]` → `[0-9A-Za-z]` | pass | pass | — | pass |
| M12-appid-cap-15 | app-id digits `{1,20}` → `{1,15}` | pass | pass | — | pass |
| M13-left-boundary-drops-digit | left lookbehind `[A-Za-z0-9_]` → `[A-Za-z]` | pass | pass | — | pass |
| M14-json-tab-escape | JSON lookbehind `(?<=\\n)` → `(?<=\\t)` | fail | fail | K1,K4,K8 | FAIL (`gh-installation-json-joined`) |
| M15-jwt-seg-cap-40 | `_JWT_SEG` `{10,}` → `{10,40}` | **pass** | fail (888485536) | K7 only | pass |
| M16-jwt-seg-floor-9 | `_JWT_SEG` `{10,}` → `{9,}` | pass | pass | — | pass |

Random seeds per variant are in `runs.tsv`; full LIMB/RESULT output for all runs is in
`limbs.txt`. Exact old/new strings and mutant blob sha256 are in
`reproductions.tsv` / `mutants.tsv`.

### Kills

Five mutants are killed deterministically, each by K1 (selftest) **and** the planted
limbs; the kill details identify the fixture that fires:

- M01: K4 `extra=…/S028.txt|github-token` (35-character negative now hits); K7
  `extra=g/x-receipts/live-n8.txt`; K8 clause "35 characters after the prefix is not a
  hit".
- M03: K4 `extra=…/S031.txt` (undocumented prefix now hits); K8 ghx clause.
- M05: K4 `missing=w/s-receipts/live-j.json` (JSON `\n`-joined plant missed); K8
  JSON-`\n` clause. K7 has no non-`\n` escape fixture, so it passes.
- M08: K4 misses S023/S024/E5/live-i; K7 misses g7/g8; K8 fails four positive clauses.
- M14: K4 misses `live-j.json`; K8 JSON-`\n` clause.
- M15 (seed-dependent): at 9191 every generated JWT segment was ≤ 40 chars, so K7
  passed; at seed 888485536 K7 failed with
  `missing=g/x-receipts/live-g9.txt|github-token`. K1/K4/K8 and the instrument's own
  selftest never see the upper bound.

### Survivors (10) — pass K1–K8 at both seeds, own `--selftest` rc=0

| mutant | contract clause broken | untested axis |
|---|---|---|
| M02 | right boundary must exclude `_` | no fixture has `_` after the 36-char tail |
| M04 | stateless app id is 1–20 digits | no zero-digit app-id fixture |
| M06 | segments are dot-separated | no non-dot separator fixture, positive or negative |
| M07 | exactly three segments | no two-10+-segment negative |
| M09 | left boundary must exclude `_` | no `_`-preceded prefix; K7's letter-prefixed negative draws its prefix from 63 choices, so it kills this only with ~1/63 probability per run (both seeds missed) |
| M10 | classic tail is exactly 36 base62 chars | no `-` inside the tail |
| M11 | stateless app id is digits | no letter app id followed by a 10+ segment |
| M12 | app id may be 16–20 digits | K4/K7/selftest use ≤ 8 digits — false negative |
| M13 | left boundary must exclude digits | no digit-preceded fixture; K7's negative never draws a digit |
| M16 | segments are 10+ | no 9-character-segment negative |

No surviving mutant is killed by the instrument's own `--selftest` (all 16 were also run
standalone: 5 fail, 11 pass — `selftest.tsv`; K1 passes in every surviving run).

## Coverage reading

The frozen negative corpus exercises length 35/36/37, prefix case, undocumented prefix,
letter-before, documentation placeholders, fine-grained `github_pat_` (known limit) and
3-character segments. It does not exercise either boundary's `_`/digit exclusions, the
classic tail charset, the stateless app-id cardinality and charset, separator identity
and count, the 9-character segment floor edge, or the segment upper bound. Two
survivors are false-negative defects (M12 rejects 16–20-digit app ids; M15 rejects
segments > 40), and M15's only kill is a K7 random draw — a fixed seed can pass it. The
other eight are over-accept mutants that no limb sees at any seed. This is a routed
coverage finding, not a re-scoring of the claim.

## Reproduce

```
S=/fast/scratch/hyaku/kasegi-r92/<new>; C=$S/c2clone
git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$C"
git -C "$C" checkout -q --detach 0628fd247914555838a42c02ba5d4ac08b7e095d
# replace corpus/instruments/capture-secret-scan.py bytes per reproductions.tsv,
# verify sha256 against mutants.tsv, patch the capture-secret-scan SCORECARD row with
# .ufo/waves/round-92/c2/candidate/scorecard-row.txt, commit
python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/c2/capability-check.py \
  --lane "$C" --rev "$(git -C "$C" rev-parse HEAD)" --work "$S/w" --seed 9191
```

Unpinned is deliberate: the pin would reject every mutant at K1 on hash alone. A
pristine run is required in the same clone to establish the baseline.

## Hygiene

No credential-shaped value was written to the wave dir: receipts carry only LIMB/RESULT
lines, sha256 digests, seeds, revs, and regex replacement strings; no fixture bytes, no
scanner copy, no counter copy. The landed scanner run over every receipt file in this
directory reported `hits=0` before this report was written. Scratch root
`/fast/scratch/hyaku/kasegi-r92/MutC2Scanner/` was deleted before yielding (mutants,
fixtures and the clone lived only there).
