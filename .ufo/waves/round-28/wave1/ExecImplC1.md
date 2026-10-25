# ExecImplC1 — round 28, wave 1: C1 anchorcheck.py gate soundness

Lane `kasegi-shokunin`, base `c9f8b115a098c65356e4b3b6048af45a37ab8395` (pre-change
instrument `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748`).
Landed instrument `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`,
523 lines. Generated 2026-10-25T17:29Z.

## Files changed

| path | role |
|---|---|
| `corpus/instruments/anchorcheck.py` | **only production file touched** (this seat's exclusive ownership) |
| `.ufo/waves/round-28/receipts/ExecImplC1.txt` | receipt, all outputs re-run live (170 lines) |
| `.ufo/waves/round-28/wave1/ExecImplC1.diff` | `git diff -- corpus/instruments/anchorcheck.py` + landed `sha256sum` (391 lines) |

No other production file, no fleet root, no sibling lane, no `shokuknow`, no VCS write, no
tool install (no pacman/uv/npx transaction; host pacman pause respected). Scratch mutant
copies live in `/tmp` only.

## Behaviour landed

1. `FAIL_CLASSES = (MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT,
   BOUNTIES-ABSENT)`; `main()` returns 1 iff any count in that tuple is nonzero, else 0.
   `LOST-RECORDED` remains recorded-not-fail: it is counted, never checked, and never
   enters the exit decision.
2. `CITE` gains the BOUNTIES-PROVINCE arm (`~/Projects/bounties/<path>:<line>`), built
   from one shared `_CITE_PATH` alternation, with the same realpath confinement as
   ORIGIN/MIRROR: an escape resolves outside the root and classifies `OUTSIDE-BASE`
   against it; an absent root classifies `BOUNTIES-ABSENT` (fail). Root derived like the
   others — `$KASEGI_BOUNTIES` override, else canonical `~/Projects/bounties`, with a
   `BOUNTIES_ABSENT` flag mirroring `MIRROR_ABSENT`/`ORIGIN_ABSENT`. `[\w./-]+` keeps
   admitting `..` so an escape is *reported*, not silently unmatched.
3. `--selftest`: 9 cases, each in a fresh temp dir with all four `KASEGI_*` roots
   overridden and each run as a subprocess of the instrument, asserting the complete
   verdict-class vector plus exit status. One isolating fixture per fail limb
   (`missing-file`, `past-eof`, `outside-base`, `pin-broken` in a temp `git init` repo,
   `base-absent`, `bounties-absent`) and three controls (`bounties-in-range`,
   `lost-recorded`, `clean`). Prints `selftest cases=9 failures=0`, exit 0; on mismatch it
   prints the failing case plus that case's stdout/stderr and exits 1.
4. Docstring updated: `BOUNTIES-ABSENT` class, fail-closed exit semantics, `--selftest`,
   base `(g) BOUNTIES-PROVINCE`, root derivation, and the explicit reason the summary line
   gains no `BOUNTIES-ABSENT=` bucket. Existing classes, spellings and the summary-line
   grammar are unchanged from r18, so the frozen counters still parse it.

## Retained evidence (all inside `receipts/ExecImplC1.txt`)

| claim limb | command | required | observed |
|---|---|---|---|
| (a) | `anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md` | exit 1, BASE-ABSENT printed | **exit 1**, `BASE-ABSENT md:2 …` |
| (b) | `… bounties-fixture.md 2>/dev/null \| grep -c BOUNTIES-ABSENT` | 1 | **1** (fixture exit 1) |
| (c) | `anchorcheck.py --selftest` | exit 0, `cases=N failures=0` | **exit 0**, `selftest cases=9 failures=0` |
| (d) | `anchorcheck.py SKILL.md` | exit 0, bad=0, classes unchanged | **exit 0**, `7 in-range, 0 bad; 7 anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` — byte-identical to `round-27/c1-controls/skill-before.txt` |
| do-nothing | pre-change bytes `c2a9e6c6…` on both fixtures + `--selftest` | unchanged bytes must reach **no** after value | fixture exits 0/0, `0` BOUNTIES lines, `--selftest` → `FileNotFoundError` exit 1 (the r27 before values) |
| discrimination (R11/R13) | mutant M1 (bounties CITE alternative removed) | arms' cases must fail | `failures=4` (outside-base, bounties-absent, bounties-in-range, lost-recorded), exit 1 |
| discrimination | mutant M2 (`BOUNTIES-ABSENT` dropped from `FAIL_CLASSES`) | that limb must fail | `failures=1` (bounties-absent), exit 1; landed bytes `failures=0` |

Corpus sweep, pre-change vs landed, `corpus/knowledge/*.md` + `corpus/*.md` + `SKILL.md`
(44 files, every verdict field + BOUNTIES-ABSENT line count): **verdict-class movement = 0**;
**exit-only movement = 5**, all BASE-ABSENT-driven and intended by predicate (a) —
`QUALITY.md`, `citation-bases.md`, `cra-manufacturer-reporting-duties.md`,
`iso-29147-divergence-and-clause-crosswalk.md`, `root-loss-2026-10-12.md`. `SKILL.md` is
not among them. Independently corroborated by `ExecRecheckAuditR28` for
`citation-bases.md` (17→16 executes, 23→24 gated, entry still PASS). No fleet or `scripts/`
caller invokes `anchorcheck.py`, so the fail-closed blast radius is direct invocations only.

## Disclosed: the frozen `corpus_disclosure` is NOT reproduced (0 of 4)

The frozen claims say the 4 marked bounties citations (`claim-gates.md`,
`intake-and-finalize.md`, `mission-control.md`, `source-tree-loss-2026-09-28.md`) "newly
classify LOST-RECORDED after the arm". **Measured: 0 of 4. LOST-RECORDED pre → post is
0→0, 0→0, 0→0, 15→15.** Cause, measured not assumed:

- the four citations are plain-text `source:` trailers at lines 123 / 109 / 169 / 353, each
  with **0 backticks on its line**;
- `TOK` is backtick-only, so `CITE` never sees them, arm or no arm;
- lane-wide, the number of backticked `~/Projects/bounties/<path>:<NN>` tokens is **0**
  (no such token exists in `corpus/knowledge/*.md`, `corpus/*.md` or `SKILL.md`).

`ExecInstrReadme` reached the same 0 independently on pre-change bytes and on a
CITE-arm-only scratch copy. The arm is nonetheless load-bearing for its own predicate
(counter (b) 0→1; mutant M1 kills 4 cases) — it simply cannot reach tokens that never
exist. **Claims-correction candidate for the L1** (append per R25-1, do not edit
`claims.json`): either record the disclosure as declared-but-not-reproduced, or dispatch a
separate instrument change authorising a marked-bare scan. Blast radius of that scan, if
ever authorised (measured, **not implemented here** — out of assigned scope): exactly those
4 lines in `corpus/knowledge/*.md`, 0 such lines in `SKILL.md`, so the 306/0 no-harm gate
would still hold.

## Risks / observations for the L1

- **O1** frozen counter (d) second command is vacuous on *both* byte sets:
  `sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'` expects the grammar `bad; N bad`, but
  the summary is `N bad; K distinct anchors` → 0 lines pre-change and 0 lines post-change.
  `bad=0` is still observable from the summary line (pasted with field extraction).
  Pre-existing, not caused by this change.
- **O2** `.ufo/waves/round-28/assemble-receipts.py` reads the SKILL.md no-harm line as
  `out.strip().split("\n")[-1]`; since r18 the summary prints *before* the verdict detail,
  so that line is a `LOST-RECORDED md:` verdict, not the summary. Not my file — flagged so
  the canonical index quotes `^== ` instead.
- **O3** `corpus/QUALITY.md` now exits 1 on pre-existing BASE-ABSENT cites (predicate (a)).
  Disclosed here so ScribeR14 / ScribeScorecard / the round lesson do not read it as drift.
- `--selftest` writes only under `tempfile.mkdtemp()` and removes it in a `finally`; it
  never reads or writes the live tree, and its fixtures live in `/tmp`, outside the lane.
- Untested-by-design: `BOUNTIES` in-range is exercised only by the selftest (the real root
  is absent on this host), so no live corpus citation can currently verify against it.
  Stated rather than implied.

## Blockers

None. Every reachable requirement is delivered; the one unmet frozen outcome
(`corpus_disclosure` 4 → LOST-RECORDED) is a claims-side defect with its cause measured,
its control run, and a scoped remedy named — it is not something this seat may fix by
silently widening the token model.
