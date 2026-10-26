# ConnC1C2 — receipt (round 39, wave 2, attack seat)

Seat: ConnC1C2. Item: cross-claim integration audit of C1 (depth:verifiability) × C2
(coverage) on the landed tree. Deliverable: `ConnC1C2.conn.md` (this directory).

## What was done

Read the frozen claims (`.ufo/waves/round-39/claims.json`) and `claims-erratum-1.md`
first. Built a scratch clone of the lane at HEAD Y (`5006097a84305267c9a3e8c1e1d560e60fe41d37`;
toplevel asserted equal to the clone dir before any fixture commit; fixture-local git
identity only; no mutating git against the real lane; no lane/fleet writes). Ran every
counter in export mode with `--lane <clone>` and scratch bound to the seat dir.

## Commands and actual outputs (abridged; full detail in ConnC1C2.conn.md)

Baseline, clean clone at Y:
- `r39-closure.sh --export-ref 5006097a8…41d37` → `closed=8/8 exit=0` (suite-sha256 `2856a210…4222b`).
- `r39-closure.sh --selftest --export-ref 5006097a8…41d37` → `selftest cases=8 failures=0` exit 0; judge `own-report accepted=1`, six forged reports rejected. (First attempt red on G6-positive until the scratch root was quiesced to a single work dir — G6 fail-closed, confirmed.)
- plain run → exit 2; base `480b1a50…` → `closed=2/8 exit=1`; r38 head `66703acaaff…` → `closed=2/8 exit=1`.
- C2: frontier 22; registry 59 (E1); S057 cites 1; knowledge 51; harness `entries=25 pass=25`; binding `records=46 bound=46 unbound=0`; recheck-audit `expected=51 missing=0 unexpected=0`; census exit 0 (only W04 ×2); source-recheck S057 exit 0; junk-manifest (capture beside it, sha `11c8d6d6…4f2f`) → 4 × `MISMATCH reason=quote-not-found`, exit 1.

EXP-1 (clone commit 9668a28; r39-closure.sh, final-gates/, declared-blocks.txt, wave1-dispatch.json, wave1/, c1-controls/ all removed): every C2 counter identical to baseline (22 / 59 / 1 / 51 / 25-25 / 46-46 / expected=51 unexpected=0 / census 0). recheck-audit exit 1 is the strict `cdroot` mirror artifact, identical with C1 artifacts present. → C2 ⊥ C1 held.

EXP-2a (clone A=143d685c, B=19bf6914; S057 snapshot+manifest, knowledge entry, S056–S059 registry rows removed; README kept; receipt regenerated over A): suite at B → `closed=8/8 exit=0`. → C1 does not depend on S057/F22 registry/knowledge/snapshot artifacts.

EXP-2b (clone A=051ac98, B=4edbff4; only the declared 28-line README amendment removed; receipt regenerated over A): suite at B → `closed=7/8 exit=1`, G1 red (`front-doors=0`), G2–G8 green. → single C1↔C2 byte contact is G1's sha-bound declared whole-tail of corpus/README.md (the F22 amendment); fails closed, by design.

EXP-3a (own C2 entry removed): knowledge 50, cites 0, harness `FAIL F22 missing-entry`, `entries=25 pass=24 exit=1`. EXP-3b (receipt payload value forged `declared=9`): suite still `closed=8/8 exit=0` — G2 payload-value comparison is a documented non-limb.

Receipt order: Y is tip, parent J, `git diff --name-only J Y` = the receipt only; receipt `export-ref=J`, `suite-sha256=` sha256 of `corpus/instruments/r39-closure.sh` at J (verified via `git show J:… | sha256sum`); all content commits precede. Receipt-last held.

Live-state couplings confirmed: G8 red on the live lane right now (`status-dirty=6` from untracked wave-2 files; `closed=7/8 exit=1` at Y on the dirty tree, `closed=8/8 exit=0` in the clean clone); E4 J-run reproduces G2 `receipt=0` red.

## Findings handed to the L1 (detail + options in the deliverable §7)

1. LOG.md round-39 correction is a bullet (`- **Correction (round 39):**`), so the literal erratum-E5-item-7 grep `^Correction (round 39)` counts 0 for LOG.md (lesson 1, SCORECARD 2, SHONEN 1). No frozen kill rule fires; recommend erratum 2 (count first non-list-marker text) rather than a tree change that would regenerate J/Y.
2. wave2-dispatch.json (untracked, wave `kasegi-r39-falsify`, 37 tasks) must get a paired `kasegi-r39-falsify-results.json` (same wave, 37 distinct identities) before filing, or G4 reds on every post-wave-2 export. Frozen C1 ref Y is unaffected.
3. Keep a clean-tree window at Y (or verify in a clean checkout) for the C1 counting command to print 8/8 at filing; if wave-2 receipts are committed atop Y, keep J pinned via the receipt per the judged-head rule.
4. G2 payload-value forgery window is real but a documented suite non-limb; suggest noting it in the round-39 lesson. No predicate change.
5. receipt `run-utc=21:35:00Z` is nominal and postdates Y's committer date (scripted commits); no limb checks it.

## Verdict

C1 and C2 are causally separable on the landed tree; receipt-last holds; both claims'
controls behave as frozen. One minor erratum-level discrepancy (LOG.md correction
prefix) and two filing-hygiene items for the L1. Neither claim is falsified; no lane
or fleet file was modified.

## Housekeeping

- Tooling: no installs/upgrades needed (bash, git, python3, gawk already present).
- No network fetches.
- Scratch dir `/fast/scratch/hyaku/kasegi-r39/ConnC1C2/` (clone, fixtures, logs)
  removed after filing this receipt and the deliverable.
- Writes: only `.ufo/waves/round-39/wave2/ConnC1C2.md` (this receipt) and
  `.ufo/waves/round-39/wave2/ConnC1C2.conn.md` (deliverable) in the lane tree.

Deliverable digest: ConnC1C2.conn.md = 230 lines, sha256
`ebf6b6e794768379ae04625eaeffc62748f4c5e7a0f9a8ca978b9f6984e47044`; receipt
ConnC1C2.md = this file, sha256 `40d58f0a224ffef06b5b8317561ea13788d9d980535f6ade2b50d8e50f12e81e`
(measured before this digest line was appended; re-measure to confirm).
