# HistoricalRows — r23 critic (leaf, read-only)

Scope: audit `.ufo/waves/round-23/claims.json`, `SCORECARD.md`, `corpus/QUALITY.md`,
r22 lessons; attack r22 placeholder status and the "rejected C1 corrected by
append-only erratum" strategy. Base `922a4dd`. Findings only; no edits.

## F1 (impact: depth:verifiability, falsifier for C1's "after")

The MIRROR-EQUIVALENT escape is real and wider than the two named cases.
`resolve.py:210-212` (bounty fallback) and `:230-233` (relative fallback) apply
`exists_any` but never `under_mirror()`; only the explicit-alias branch
(`:219-222`) confines. Reproduced against the committed code
(`KASEGI_MIRROR=/tmp/r23-check/mirror`, local scratch fixture):

- `~/Projects/bounties/../outside-target/secret.md` → `MIRROR-EQUIVALENT`
  (`mirror/../outside-target/secret.md`) — claims.json's own before-case confirmed.
- `escape-link/secret.md` (mirror symlink → outside) → `MIRROR-EQUIVALENT`.
- `../outside-target/secret.md` → `INTERNAL` (`lane/../outside-target/...`):
  the claim scopes this out ("explicit lane-relative paths keep prior
  semantics"), but a relative token that escapes the *lane repo* is credited
  INTERNAL — the same unsoundness class, second channel.
- Prefix-sibling note (already-reject, not a fix): `~/Projects/bounties-real/x.md`
  matches `BOUNTY_PREFIXES` via `startswith` (`:204`), is dom-tagged `bounty`,
  then rel = `-real/x.md` is sought *inside* the mirror. Falls GONE today;
  "reject sibling-root prefix confusion" is satisfied by boundary-matching the
  prefix (`base == root or base.startswith(root + "/")`), not by the join fix.

**Falsifier:** post-fix, any fixture token whose realpath lands outside the
selected mirror (or outside the lane repo for INTERNAL) that still classifies
MIRROR-EQUIVALENT/INTERNAL falsifies the claim. **Smallest correction:** the
fixture matrix must include symlink-escape AND brace/glob-escape variants
(`exists_any` methods `brace`/`glob` return paths that bypass a literal-only
join check), and the claim should either confine the INTERNAL lane-escape case
or record it as a deliberate documented residual, not silently leave it.

## F2 (impact: depth:verifiability + coverage credibility; erratum scope too narrow)

The r23 SCORECARD section's correction paragraph names the verdict but leaves
three live texts still asserting the rejected assessment. At worktree state
(uncommitted diff) the r22 row `SCORECARD.md:327` still reads "**Improved,
score held**", the Move log row (`SCORECARD.md:191`) "4 held (headers 25/25…)",
and `LOG.md` round-22 entry still says "Verdicts (pending non-author
verification). C1 improved, score held 4". A pointer-only erratum leaves the
primary cells contradicting it — exactly the R9 class the lane minted.

**Falsifier:** `grep -n "Improved" SCORECARD.md | grep -i verif` after the r23
commit must return the r22 row carrying an appended marker, not bare
"Improved". **Smallest correction:** same-line suffix markers (R6-safe, no line
shifts) on the r22 axis-row verdict cell and the Move-log row — e.g.
"[r23 erratum: C1 REJECTED-HONEST-STOP, provenance work not depth credit; see
corpus/lessons/round-22-verifier-spotcheck.md]" — plus one appended LOG.md
line resolving the "(pending non-author verification)" tag. C2's "Improved"
row is verifier-confirmed and needs no marker.

## F3 (impact: verifiability of r22 records; the "stale pointers/deletion tally" debt is itself wrong)

Re-opened the r22 lesson/LOG evidence against `git show c8b719d`:
`corpus/knowledge/` deletions are **32 lines / 14 deletion-containing hunks /
6 files** (numstat: submitted-registry 14, intake-and-finalize 6,
ops-invariants 6, operator-queue 3, triage-thresholds 2, citation-bases 1;
total commit 34 incl. SCORECARD+README each 1). `corpus/lessons/round-22.md:151`
says "22 deletions"; `LOG.md:1081` says "16 hunks". Both are wrong (verifier's
"22 vs 32" confirmed the tally, not the hunk count). The underlying
prefix-preservation conclusion holds (my re-run: 0 lost text; the one flagged
line was only a trailing-newline add).

**Falsifier:** `git show c8b719d -- corpus/knowledge/ | grep -c '^-[^-]'` = 32;
hunks containing `-` lines = 14. **Smallest correction:** append-only erratum
to the r22 lesson naming base c8b719d: "numstat deletions were 32 (14
deletion-containing hunks), not 22/16; prefix-preservation conclusion
unchanged" — per R9.

## F4 (impact: coverage gate ambiguity; C2 bar drift)

claims.json C2 requires "Q1–Q6 evidence" but the live bar at r23 includes Q7
(committed worktree `corpus/QUALITY.md` §Round-23 criteria). All five r22
entries' `recheck:` fields are prose beginning "On each"/"Annually" (verified
verbatim at `corpus/knowledge/*.md:4`) — the exact shape Q7 fails. If F06–F08
ship prose rechecks they fail the amended bar while matching the frozen claim.

**Falsifier:** an admitted F0x row whose recheck field is prose → claim met
literally, Q7 failed; judge inconsistency. **Smallest correction:** claims.json
amendment (or planner note) naming "all QUALITY criteria in force (Q1–Q7)" —
preregistration is frozen, so record the superseding bar in the r23 lesson and
make the executors' acceptance Q1–Q7, not Q1–Q6.

## F5 (impact: verifiability; self-inflicted stale pointer)

`corpus/QUALITY.md:48-51` grounds Q7/R7–R9 in "`corpus/lessons/round-23.md`
M1–M5" — a file that does not exist at base (confirmed absent). Same class as
the r22 stale pointers being corrected (M3/M4). M-id collision caveat: those
M-ids are the verifier's correction ids (`round-22-verifier-spotcheck.md:17`),
not the lane's r22 M-sequence (M1 there = 273 B marker).

**Smallest correction:** either `corpus/lessons/round-23.md` lands in the same
round commit carrying verifier-correction ids M1–M5 (disambiguated as verifier
ids), or the grounding column is re-pointed to
`corpus/lessons/round-22-verifier-spotcheck.md`.

## F6 (impact: minor; placeholder status already half-fixed in worktree)

Verifier correction "M1 placeholder row replaced" is in flight: the
uncommitted SCORECARD diff deletes "none enter through this rollout" — correct,
since at base `922a4dd` the `sources-registry` row coexisted with the
contradicting sentence. **Smallest correction:** log this closure in
round-23.md as verifier-M1 debt discharged, not a silent fold-in
(claims.json's "no independent axis credit" wording already covers the
no-credit part; it does not cover the *record* of the fix).

## Scope limits

- Read-only audit; no fixture matrix file exists yet — F1's symlink/glob cases
  are demonstrated against `classify()` directly, not against a persisted matrix.
- F2/F3 corrections assume append-only discipline (R6/R9); no historical text
  rewrite is proposed.
- Not re-verified: whether 922a4dd's `sources-registry` row predates the
  placeholder sentence's authorship order (irrelevant to the fix).
- No installs; tools used: python3 stdlib, git, stock coreutils.
