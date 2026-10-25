# ScribeSkillGate — round 28, wave 1

**Seat:** scribe (leaf, no dispatch). **Axis:** depth:verifiability. **Milestone:** round-28.
**Lane root:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
**Receipt:** `.ufo/waves/round-28/receipts/ScribeSkillGate.txt`.
**Write scope used:** `SKILL.md`, that receipt, this report, `.ufo/waves/round-28/wave1/ScribeSkillGate/`
(scratch). No other production file touched; no tool installed; no VCS write.

## Delivered

Two appends to `SKILL.md`, nothing else changed (1032 → 1035 lines):

1. **One registry row at line 982**, at the end of the `## Gates & probes registry` table (prior last
   row: 981, `recheck-audit.py`), for `anchorcheck.py`:
   entry command, `gate|probe` type, fail-closed verdict map (`exit 1` on
   MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BASE-ABSENT/BOUNTIES-ABSENT; LOST-RECORDED recorded,
   not fail), bounties base = `$KASEGI_BOUNTIES` override else canonical `~/Projects/bounties`,
   `--selftest` printing `selftest cases=N failures=0` (one isolating fixture per limb), pinned-value
   path `.ufo/waves/round-28/c1-receipt-index.txt`, write scope "all inputs read-only + its own receipt
   dir", owner `kasegi`. `gate|probe` rows 1 → 2.
2. **One-sentence round-28 note at end of file (line 1035)**, recording the erratum, not the frozen cell:
   zero backticked anchored `~/Projects/bounties/` citations exist lane-wide, so the new
   `BOUNTIES-ABSENT` arm is invisible to all existing bytes — no verdict-class movement on any file.

## Gates

| Gate | Command (lane root) | Observed |
|---|---|---|
| R6 before/after, pre-change instrument `c2a9e6c6…` | `python3 corpus/instruments/anchorcheck.py SKILL.md` | both exit 0; both summaries `7 in-range, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` |
| same, normalized | `md:NN` collapsed, diff | **identical**; both sha256 `dd63c163a56b8db4…` |
| same, raw | diff of the two 315-line reports | one line only: `md:998` → `md:999` for `[lost-base] check-freshness.mjs:61` |
| C1(a) on landed bytes `c3629229…` | bad fixture, `echo $?` | `1` (frozen after; pre was `0`) |
| C1(b) on landed bytes | bounties fixture, `grep -c BOUNTIES-ABSENT` | `1`; `BOUNTIES-ABSENT md:3 ~/Projects/bounties/ops/claim-check.mjs:96 (base tree absent: …)`; exit 1 |
| C1(c) on landed bytes | `--selftest` | `selftest cases=9 failures=0`, exit 0 |
| `$KASEGI_BOUNTIES` root load-bearing | same fixture with a present temp root | `PAST-EOF … (file has 1 lines)`, 1 bad — no BOUNTIES-ABSENT |
| C1(d) on landed bytes | `SKILL.md` worktree vs pre-edit HEAD bytes | both exit 0, identical summary (306 LOST, 0 bad, BASE-ABSENT 0, PIN-BROKEN 0, OUTSIDE-BASE 0); normalized diff **identical**, sha256 `e53e8b5be7c5da3c…` |
| erratum non-reproduction | `grep -rno '\`\[lost-\(base\|tree\)\] ~/Projects/bounties/[^\`]*:[0-9][0-9]*\`' corpus/ SKILL.md \| wc -l` | `0` |
| note creates no new citation | summary counts above | unchanged (7 in-range, 306 LOST) |

Instrument digest was stable at block start and end of the verify block
(`c36292292ec0d85eef348b0c1ef723c6501fb136cab939e0e87c93137edb6a2a`). Earlier landed reads were
mid-write (`NameError: name '_selftest' is not defined`, bad fixture still exit 0); those are recorded in
the receipt as transient, not as results. After this report was written the instrument moved once more to
`95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`; every counter was re-run there
(17:29:16Z, digest stable across the block) and reproduced every value: `selftest cases=9 failures=0`
exit 0, bad fixture exit 1, 1 `BOUNTIES-ABSENT` line, `SKILL.md` exit 0 with the same class counts
(receipt §8).

## Findings / conflicts

1. **The frozen C1 `corpus_disclosure` cell does not reproduce** — confirmed independently, not just
   accepted: the four named citations are plain `source:` prose (e.g. `corpus/knowledge/claim-gates.md:123`)
   with no backticks, and `anchorcheck` only scans backticked spans. Zero backticked anchored bounties
   citations exist lane-wide. The note therefore records `.ufo/waves/round-28/claims-erratum-1.md`, per the
   L1's mid-run correction; had it kept the brief's wording, `SKILL.md` would assert a movement that
   cannot happen.
2. **R6 is satisfied in substance, not in the letter.** Appending a row at the end of a mid-file table
   moves 51 following lines by +1. Proven harmless: normalized report identity at both instrument
   digests; the single moved report position (`SKILL.md:998` occurrence) is cited by nothing. A shift-free
   append is impossible here — the only compensating deletions would move either the section heading at
   977 (cited by `corpus/lessons/round-26-verifier-spotcheck.md:32`, whose range 977-985 still holds) or
   the paragraph at 984.
3. **Pre-existing stale pointer, not caused by this seat:**
   `corpus/instruments/resolve-dispatch-fixtures.json:159,161` say `SKILL.md:1000` for "the verbatim
   four-alternative set". Line 1000 is `~/Projects/bounties/ops/shared.mjs`; the set is at 1007 before
   this edit and 1008 after. Round-26 created the drift (9 lines inserted at 976). Not my file — flagged
   for the L1.
4. `SKILL.md` row's write-scope claim ("all inputs read-only") verified against the landed module: only
   read opens, one `git … show` subprocess, `--selftest` writes only under `tempfile`, and its docstring
   states "No fixture reads or writes the live tree".

## Not done / out of scope

- Did not create `.ufo/waves/round-28/c1-receipt-index.txt` (ExecReceiptCanonC1 / KasegiR28); the row's
  pinned-value path is asserted as the round's canonical index, not as an existing file.
- Did not run the C1 counters as a final gate (L1's job); the same commands were run and their observed
  values are in the receipt §3 and §7, with a paste-ready re-run block.
- Did not touch `corpus/instruments/README.md`, `corpus/lessons/round-28.md`, `LOG.md`, `SCORECARD.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, or any source snapshot.
- The instrument changed five times during this seat's measurement window; any later ExecImplC1 edit
  invalidates §3 numbers and requires the §7 re-run.

## Artifacts

- `.ufo/waves/round-28/receipts/ScribeSkillGate.txt` (scoped receipt, geometry, both summaries, limits)
- `.ufo/waves/round-28/wave1/ScribeSkillGate/` — before/after reports, normalized pairs
  (`n-before.txt` ≡ `n-after.txt`), `SKILL-head.md` (pre-edit bytes), `landed-head.txt`,
  `landed-worktree.txt`, `lh.n` ≡ `lw.n`, `verify-block.txt`, `final-block.txt`
