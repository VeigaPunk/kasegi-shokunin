# ConnC1C2 — cross-claim integration audit (C1 depth:verifiability × C2 coverage)

Seat: ConnC1C2 (attack, leaf). Round 39 wave 2. Verified against the landed tree at
HEAD Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37`, judged head
J = `46c66c268502abd1b2c342fc71bf88ccf721845b` (receipt `export-ref=`).

Axes examined: depth:verifiability (C1), coverage (C2).
Question: do the C1 and C2 counter sets remain causally separable on the landed
bytes, is the final-gates receipt generated last, and what integration steps remain
for the L1.

Method: every experiment was run against a scratch clone of the lane
(`git clone` into the seat scratch dir, toplevel asserted equal to the clone dir
before any fixture commit; fixture-local identity only). Mirrors were mutated only
inside the clone. The suite was always run in export mode with `--lane <clone>`,
`--work`/`--scratch-root` under the seat's own scratch root. No lane/fleet file was
written; no mutating git command was run against the real lane.

## 1. Artifact inventory (as landed)

C1-owned artifacts: `corpus/instruments/r39-closure.sh`,
`.ufo/waves/round-39/declared-blocks.txt`, `.ufo/waves/round-39/final-gates/all-gates.txt`,
`.ufo/waves/round-39/wave1-dispatch.json` (+ its paired results file
`.ufo/waves/round-39/kasegi-r39-build-results.json`, matched by the dispatch's
`wave=kasegi-r39-build`), `.ufo/waves/round-39/c1-controls/`, `.ufo/waves/round-39/wave1/`,
and the C1 limbs of `SCORECARD.md` / `SHONEN.md` / `LOG.md` /
`corpus/lessons/round-38.md` / `corpus/knowledge/considerthese-proposals-ledger.md`.

C2-owned artifacts: the round-39 amendment of `corpus/README.md` (28-line appended
tail containing the F22 frontier row and the `knowledge/cisa-when-to-issue-vex.md`
coverage row), registry rows S056–S059 in `corpus/SOURCES.md`,
`corpus/knowledge/cisa-when-to-issue-vex.md`,
`corpus/source-snapshots/round-39/` (`S057.txt` + `manifest.json`), and the counters
`frontier-recheck-count.py`, `source-recheck.py`, `capture-binding-check.py`,
`recheck-audit.py`, `scripts/sources-census.sh`.

Static read of the instruments agrees with the split: the four C2 instruments and the
census script read only `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/`,
`corpus/source-snapshots/`; none of them opens `r39-closure.sh`, the receipt,
`declared-blocks.txt`, or any `.ufo/waves/round-39/` dispatch/results JSON. The C1
suite reads only `.ufo/waves/round-39/` files, the four lesson/ledger files, the two
front doors — and, through G1's declared whole-tail, the 28 appended lines of
`corpus/README.md` (the only C2-owned bytes it touches).

## 2. Baseline reproduction (clean clone at Y, commit 5006097)

- `bash corpus/instruments/r39-closure.sh --export-ref 5006097a8…41d37 --lane <clone>` →
  `closed=8/8 exit=0` (all eight G lines `closed=1`; suite-sha256 `2856a210…4222b`).
- `bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097a8…41d37` →
  `selftest cases=8 failures=0`, exit 0; all eight graded case lines
  `positive=pass mutants=n/n verdict=pass` (n = 4,8,2,6,4,4,3,3 — all ≥ 1, E5-1
  satisfied); `selftest judge=own-report accepted=1` and the six forged reports
  (`forged-summary`, `forged-caselines`, `forged-failed-cases`, `forged-detail-free`,
  `forged-7-cases`, `forged-no-verdict`) all rejected. (First selftest attempt red on
  G6-positive only because the scratch root held a sibling work dir from an earlier
  probe; with a quiesced scratch root it is green — G6 doing its job, see §6.)
- Plain run → exit 2 (refused). Base `480b1a50…` → `closed=2/8 exit=1`.
  r38 judged head `66703acaaff50529a35be49aa8759d04140720ad` → `closed=2/8 exit=1`.
- C2 counters: frontier 22; registry 59 (E1); `^source: S057` citations 1; knowledge
  files 51; harness `entries=25 pass=25 exit=0`; binding `records=46 bound=46 unbound=0`;
  `recheck-audit --quiet` → `expected=51 missing=0 unexpected=0`; census validate exit 0
  with exactly two `W04` codes (S028/S029) and no new W/E code; `source-recheck.py
  --manifest corpus/source-snapshots/round-39/manifest.json --source S057` → exit 0
  (sha256 OK + Q1–Q4 OK).

## 3. EXP-1 — C2 counters with every C1 artifact ABSENT (clone commit 9668a28)

Removed in the clone: `corpus/instruments/r39-closure.sh`,
`.ufo/waves/round-39/final-gates/`, `.ufo/waves/round-39/declared-blocks.txt`,
`.ufo/waves/round-39/wave1-dispatch.json`, `.ufo/waves/round-39/wave1/` (incl. the
`ExecSuiteBuild.overlay/wave1-results.json`), `.ufo/waves/round-39/c1-controls/`.
Committed; tree clean.

Measured against this mirror (frozen values in parentheses):
frontier 22 (22); registry 59 (59, E1); S057 citations 1 (1); knowledge 51 (51);
source-recheck S057 exit 0 (0); harness `entries=25 pass=25 exit=0` (25/25);
binding `records=46 bound=46 unbound=0` (46/46); recheck-audit frozen limbs
`expected=51 missing=0 unexpected=0` (51/0/0); census exit 0 (0).

Result: every C2 counter is byte-for-byte on its frozen value with the entire C1
artifact set gone. The only deviation is `recheck-audit`'s exit code 1, which is
identical in the clone baseline WITH the C1 artifacts present: it comes from the
strict `cdroot` limb (recheck lines name the canonical lane path; the audited root is
the clone), a documented strict add-on that "never replaces" the frozen limbs. It is
therefore a mirror artifact, not a dependence on C1.
**Separability direction C2 ⊥ C1: HELD.**

## 4. EXP-2 — C1 suite with C2 artifacts ABSENT

G2's structural limb requires `git diff --name-only <export-ref> REF` to list only the
receipt, so each variant was built as a two-commit chain in the clone: content commit
A (C2 bytes removed; receipt deleted), then a receipt commit B = A + a regenerated
`all-gates.txt` naming `export-ref=A` (G-lines and graded selftest lines carried from
Y's receipt; `suite-sha256` unchanged because `r39-closure.sh` was untouched). The
suite was then run at B.

### 4a. All C2 artifacts removed EXCEPT the README amendment (A=143d685c, B=19bf6914)

Removed: `corpus/source-snapshots/round-39/`, `corpus/knowledge/cisa-when-to-issue-vex.md`,
the four registry rows S056–S059 in `corpus/SOURCES.md`. README untouched.

Suite at B: `closed=8/8 exit=0` — G1 green (`declared=2,valid=2,front-match=2,
pure-append=1`), G2 green (`diff-clean=1,digest-match=1,graded-cases=8`), G3–G8 green.
**The C1 suite does not read or depend on the S057/F22 registry rows, the knowledge
entry, or the capture snapshot.** HELD.

### 4b. ONLY the README round-39 amendment removed (A=051ac98, B=4edbff4)

Removed exactly the declared 28-line tail of `corpus/README.md` (the F22 frontier row
+ coverage-map amendment); all C2 artifacts otherwise intact.

Suite at B: `closed=7/8 exit=1` — G1 red (`declared=2,valid=1,front-doors=0,
tail-match=1`: the README declaration no longer binds), G2–G8 all green.

This isolates the single coupling point between the two claims: G1's declared
whole-tail of `corpus/README.md` embeds the F22 amendment bytes C2 landed. The
coupling is declared line-by-line and sha256-bound in `declared-blocks.txt`
(`corpus/README.md 28 a59d42cc…c8f`), it fails closed, and it is the stated purpose of
G1 (whole-tail declarations of the round-39 append). It is a designed, hashed
verification coupling, not a hidden dependence: remove any other C2 artifact and C1
stays green (§4a).

## 5. Own-artifact controls (do-nothing direction)

- EXP-3a (clone commit on top of Y): removed only `corpus/knowledge/cisa-when-to-issue-vex.md`.
  C2 counters moved off every frozen value: knowledge 50, S057 citations 0, harness
  `FAIL F22 problems=missing-entry`, `entries=25 pass=24 exit=1`. The C2 counters
  stand on their own artifacts and fall when those fall.
- EXP-3b (clone commit on top of Y): forged one payload value inside the receipt
  (`G1 payload=declared=9,valid=2,…`). Suite at the forged commit still prints
  `closed=8/8 exit=0`; G2 green. G2 verifies receipt structure, linkage, digest and
  graded-line shapes — not payload values. This is a real forgery window, and it is an
  explicitly documented non-limb of the suite ("The cross-run payload VALUE comparison
  is not a limb"), so the frozen predicate is met as written; flagged as residual
  risk in §7.
- Junk twin: `source-recheck.py --manifest <scratch>/junk-manifest.json` with the
  captured `S057.txt` beside it (fixture layout as recorded in
  `c2-controls/junk-f22-recheck.txt`; capture sha256 `11c8d6d6…4f2f` matches) →
  `S057:sha256 OK` + four × `MISMATCH reason=quote-not-found`, exit 1 — byte-identical
  to the committed control. The junk F22 twin is rejected.

## 6. Receipt generation order and live-state couplings

Receipt-last: **HELD.** Y (`5006097`) is the lane tip, its parent is J (`46c66c2`),
and `git diff --name-only J Y` prints exactly `.ufo/waves/round-39/final-gates/all-gates.txt`.
The receipt carries `export-ref=J` (40 hex, ancestor-or-equal), `suite-sha256=
2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`, which equals the
sha256 of `corpus/instruments/r39-closure.sh` at J (verified with `git show J:… |
sha256sum`), all eight `G<n> … closed=1` run lines, one `closed=8/8 exit=0`, eight
graded selftest case lines and `selftest cases=8 failures=0`. All content commits
 precede the receipt commit. Wave-1 evidence `.ufo/waves/round-39/wave1/ExecSuiteBuild.md`
§2.3 records the generation flow (an earlier iteration named `export-ref=f918ec4f…` at
`run-utc=21:10:00Z`, superseded by the final receipt naming J at `run-utc=21:35:00Z`).

Live-state couplings of the C1 instrument (by design, documented in the suite header;
verified live during this audit):

- G8 executes the pinned r37 suite, whose E9 requires the lane checkout to equal the
  export ref and `git status --porcelain` to be empty. The live lane currently holds
  untracked wave-2 orchestration files (`wave2-dispatch.json`, `kasegi-r39-falsify.ready*`,
  `wave2-run.err`, `wave2/`), so a fresh `bash corpus/instruments/r39-closure.sh
  --export-ref Y` on the live tree prints `closed=7/8 exit=1` with G8 `status-dirty=6`.
  In the clean clone the same command prints `closed=8/8 exit=0`. The committed receipt
  is the transcript of a clean-tree window, which is exactly the E4 resolution
  (verification ref Y, receipt as the committed run).
- G6 scans the live scratch root and failed this seat's first selftest run until the
  scratch root was quiesced to a single work dir — fail-closed behavior confirmed.
- The E4 "J-run prints 7/8 with G2 receipt=0" was reproduced on the mirror (G2
  `receipt=0` red at export-ref J); with HEAD≠J, G8 additionally reds on `head-match`,
  giving 6/8 — the documented "checkout must equal the export ref" limit.

## 7. Findings and risks

1. (Discrepancy, minor — content present, form mismatches) Erratum E5 item 7 states
   the R2 counting command `grep -c '^Correction (round 39)' corpus/lessons/round-38.md
   LOG.md SCORECARD.md SHONEN.md` yields "at least 1 per file at the judged head".
   Measured at HEAD: lesson 1, SCORECARD 2, SHONEN 1, **LOG.md 0**. LOG.md's
   correction exists at line 1704 but as a list item (`- **Correction (round 39):**`),
   so the literal `^Correction` count is 0. No frozen kill rule fires (G5 checks only
   SCORECARD/SHONEN; the claims.json kill list does not include this grep), but a
   wave-2 seat running the E5 command literally records a miss. Cheapest closure:
   erratum 2 noting the command counts the first non-list-marker text (consistent with
   the E1/E2 precedent); the alternative (landing a line-start correction in LOG.md)
   mutates the judged tree and forces J/Y regeneration.
2. (Integration step) `.ufo/waves/round-39/wave2-dispatch.json` (untracked at HEAD,
   `wave=kasegi-r39-falsify`, 37 tasks) will be counted by G4's `find … -maxdepth 1
   -name '*-dispatch.json'` in any export that tracks it. G4 at Y pairs
   `wave1-dispatch.json` with `kasegi-r39-build-results.json` via the matching `wave`
   field. Before filing, land a results file `.ufo/waves/round-39/kasegi-r39-falsify-results.json`
   with `"wave": "kasegi-r39-falsify"` and 37 distinct seat identities, or every
   post-wave-2 suite run reds on G4 (`pairs != dispatches`). The frozen C1
   verification ref Y predates the wave-2 dispatch file, so the frozen C1 commands at
   Y are unaffected; this protects post-wave-2 re-runs and any wave-3 export checks.
3. (Integration step) C1 counting-command reproducibility at filing: the lane must
   present a clean-tree window at Y (or the verifier must run in a clean checkout of
   Y, e.g. a scratch clone/worktree) for `bash corpus/instruments/r39-closure.sh
   --export-ref Y` to print `closed=8/8 exit=0`; with wave-2 receipts untracked in the
   lane, G8 reds by construction. If wave-2 receipts are committed atop Y, keep the
   judged-head rule pinned to J via the receipt and re-state the verification ref.
4. (Residual risk, documented) G2 does not compare payload values across receipts
   (§5, EXP-3b). A self-consistent forged receipt with altered payload values passes
   G2. Mitigations in place: suite-bytes digest, ref ancestry + post-ref diff,
   graded-line shape, G3 transcript coverage for lane-file quotes, and the r37
   analogue (G8) which does compare pinned bytes. Recommend carrying the note into
   `corpus/lessons/round-39.md` documented limits; no predicate change needed.
5. (Cosmetic) The receipt's `run-utc=2026-10-26T21:35:00Z` is nominal and postdates
   Y's committer date (`2026-10-26T20:12:12Z`): scripted committer dates. No frozen
   limb checks run-utc ordering; a strict reader may ask. Optional note for the
   round-39 lesson.

## 8. Verdict

- C2 counters with the C1 artifact set absent: all nine frozen values reproduce →
  **C2 is causally independent of C1.**
- C1 suite with the S057/F22 registry, knowledge and snapshot artifacts absent:
  `closed=8/8 exit=0` → **C1 does not depend on C2's S057/F22 artifacts.** The only
  C1↔C2 byte contact is G1's declared, sha-bound whole-tail of `corpus/README.md`
  (fails closed when the F22 amendment is removed), which is the designed behavior of
  the whole-tail declaration check.
- Receipt generation order: content commits → receipt commit last; digest, ancestry
  and diff-clean limbs all verified → **receipt-last: HELD.**
- Own-artifact absence and forgery controls behave as frozen (C2 counters red without
  their entry; junk twin rejected; suite reds without its receipt; payload-value
  forgery remains a documented non-limb).
- Both claims remain separable on the landed tree; the two discrepancies found are a
  literal-form mismatch in LOG.md against erratum E5 item 7 (minor, erratum-fixable)
  and wave-2 filing hygiene (results pairing + clean-tree window) for the L1.

No files in the lane or fleet were modified by this audit; all mutations were inside
the seat scratch clone, which is removed after this deliverable and receipt are filed.
