# ScribeLesson — round-28 lesson assembly (wave 1)

Seat: `ScribeLesson` (scribe, leaf). Round 28, wave 1, milestone `round-28`. Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Assembled 2026-10-25T17:30Z–17:37Z (UTC).
Receipt: `.ufo/waves/round-28/receipts/ScribeLesson.txt`.

## Behavior

Wrote `corpus/lessons/round-28.md` (517 lines, 46,988 B, sha256 `973b6362…948d3d`) from the wave's
seats, not from memory. Structure delivered:

- H1 + header naming **three** revisions the receipts mix up (lane tip at round start `261a665…`,
  claims-freeze commit `c9f8b11…`, dispatch `94f387c…`) and the 69-seat role split.
- **DRAFT banner** with the reason it is a draft (below), the six seats that had filed nothing, and
  the two close-out steps nobody has run.
- `## Frozen claims` — C1, C2 and the density guard with before, after and verdict-at-assembly; the
  timestamped counter-state table (six runs, three distinct digests) so a reader can tell PRE-STATE
  receipts from landed-digest runs; the appended claims erratum and its measured consequence.
- `## Gate` — `ScribeLessonGate`'s draft, pasted, minus its assembly note, plus a reconciliation
  line (entry 103 lines / `a22d2321…`, manifest `e62ddad1…` / 5038 B, census exit 0 / 42 rows,
  harness 15/15 — all re-measured here). Admit keeps its inline S042:Q1 quote; **both rejects now
  carry inline ≤25-word quotes with file:line** (the draft's rows had evidence but no quote, which
  the C2 predicate and round-26 routed defect 3 require). S041's `used-by` old→new cell is recorded
  in the lesson, as R8 and the C2 predicate demand.
- `## Mistakes` — 12 rows (M28-1..M28-12), each with class, evidence pointer, captured-by, fix.
- `## Compliance` — freeze discipline, nine-file ownership table with digests, census
  before/mid/after, scope and safety, tooling, close-out ledger.
- `## Carry-forward for round 29` — 8 items, each tied to a mistake row.

## Gates (what I ran vs what I cite)

Run by this seat, read-only: `sources-census.sh validate --root … kasegi` → **exit 0**, two
pre-existing W04 (S028/S029), `S042` row count **1**, registry rows **42**; sha256 of the nine
production files, the manifest and both captures; HEAD→worktree line counts; `git diff --numstat`
for `corpus/instruments/README.md`; and one discriminating check —
`source-recheck.py --source S041 --source S042` prints **6** quote lines, not 12 (M28-11).

Cited, not re-run: the four frozen C1 counters and the five frozen C2 counters, each to the seat and
digest that produced it (`ExecImplC1` 17:29:28Z at `95333e29…`; `RevCounters2` 17:26:24Z;
`ExecReceiptCanonC2` 17:27:13Z; `RevFixturesC1` 17:31:21Z). The two receipts my assignment names as
the verdict source (`ExecC2Counters.txt`, `ExecFixtureRun.txt`) are **PRE-STATE**. Hence:

**The lesson is DRAFT.** C1's limbs (a)–(d) are observed at the landed digest, but the canonical
`.ufo/waves/round-28/c1-receipt-index.txt` does not exist (verified absent three times), so frozen
counter (c)'s index greps have not run, and no re-run exists at the commit that will contain the
lesson. The L1 finalizes after close with the block in `## Compliance` → close-out ledger.

## Touched surfaces

One production file: `corpus/lessons/round-28.md` (did not exist before; no other seat owns it).
Two non-production paths: this report and the receipt. No scratch tree, no `/tmp` artifact, no VCS
write, no subagent, no background job, no tool install (`pacman` paused host-wide; nothing needed).

## Findings worth the L1's attention (full argument in the lesson)

1. **M28-2 / claims-erratum-1** — the frozen `corpus_disclosure` cell does not reproduce: the four
   named citations are unbackticked `source:` trails, `TOK` is backtick-only, and the lane has **0**
   backticked anchored bounties tokens. Measured reclassification 0 of 4. `ScribeScorecard`'s receipt
   had recorded the expectation "1 / 1 / 1 / 16" from the frozen cell; no receipt may do so.
2. **M28-3** — `claims.json` C1 counter 4's `bad=` sed is unsatisfiable (`bad; N bad` vs the summary's
   `N bad; K distinct anchors`); three seats measured it printing nothing on both byte sets.
3. **M28-6** — R6's letter and "append at the END of the registry table" are incompatible: SKILL.md
   1032 → 1035 shifts 51 lines, and `resolve-dispatch-fixtures.json:159,161` pins `SKILL.md:1000`
   (119 further `.ufo` copies cite it). Both `ExecSkillGateSupport` and `SentinelScope` flagged it;
   the shift landed and is disclosed. The L1 must decide the rule, not just this instance.
4. **M28-5** — rows landed before their entry: census went `E11 ×2` exit 1 and the frontier harness
   crashed with an uncaught `FileNotFoundError` (no `entries=` line). Cleared at 17:26Z; the harness
   crash is still an instrument defect (route: fail a named row).
5. **M28-8** — Q9's "path stem equals id" conjunct has no instrument: `source-recheck` exits 0 on a
   stem-mismatched record. C2's Q9 clause rests on hand-run receipts (`check_q9.py`,
   `RevManifestC2`, `ExecReceiptCanonC2` F-3) until that is promoted.
6. **M28-12** — digests drift behind receipts: README `e38ba567…` → landed `5f458a7a…` (243 → 245
   lines, F12 `next` cell rewritten); `instruments/README.md` went 289 → 327 lines across two
   receipt revisions; `ExecGateLog` §A reads `95333e29…` while §B calls `c3629229…` "LANDED".
   The L1 should re-hash immediately before the commit and record digests in LOG.md.
7. **Evidence tax** — seven PRE-STATE receipts exist for work that landed minutes later (M28-1).
   The labels worked; the wave shape did not. Counters belong in a second tranche.

## Out of scope / not done

- Did not run the frozen counters as a verdict, did not assemble the canonical index (defect 4), did
  not edit `claims.json`, `SCORECARD.md`, `LOG.md`, the entry, the registry, README, SKILL.md or any
  instrument. **`SCORECARD.md`'s C2 cell still cites the two-`--source` form** (M28-11) — its owner
  or the L1 must correct that wording.
- Did not obtain the non-author spot-check of a refusal that LEARNING.md requires; the lesson names
  it as an omission rather than asserting agreement.
- Six seats had filed no artifact at assembly; nothing is credited to them.

## Artifacts

- `corpus/lessons/round-28.md` — the lesson (DRAFT).
- `.ufo/waves/round-28/receipts/ScribeLesson.txt` — evidence receipt (states, digests, commands).
- `.ufo/waves/round-28/wave1/ScribeLesson.md` — this report.
