# C1AnchorcheckDefect — verify anchorcheck exit semantics + fail-closed "no citation check" count

Seat: `L1Kasegi25.C1AnchorcheckDefect` (leaf, read-only). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
No production edit, no VCS write, no spawn. Probes wrote only to `/tmp/acprobe2` and `/tmp/c1-live-w2.json`.
Tool install/update record: **none** (no pacman/uv/npx/cargo transaction; only `python3`, `bash`, `git`).

## Verdicts

| # | Reported claim (source) | Verdict |
|---|---|---|
| A | `anchorcheck.py` `main()` has no return; `sys.exit(main(...))` → **exit 0 for every verdict class**; non-zero only by crash — `RevRecheckSemantics.md:59-73` | **CONFIRMED** |
| B | `fail-closed=23` lines all exit non-zero today; exit code moved 2 → 1 (syntax error → real `test -d` gate) — `RevRecheckSemantics.md:45-47`, `FixRecheckLines.md:152-155` | **CONFIRMED** |
| C | "**19 of the 23 fail-closed entries produce no checked citation** even after restoration" (Tier-1 ZERO=10 + Tier-2 LOST=9) — `RevRecheckSemantics.md:176-199` | **CONFIRMED as written; under-counted as phrased — see defect below** |
| D | `~/Projects/bounties/…` citations are invisible to `CITE` (no arm), so `0 bad` ≠ health — `RevRecheckSemantics.md:75-90` | **CONFIRMED** |
| E | `root-loss-2026-10-12.md` is a *passing* inverted line (`test ! -e`×3, `test -e` ufo-fsd-alpha) — `RevRecheckSemantics.md:127,166-171` | **CONFIRMED** |
| F | Final tree `lines=37 pass=37 fail-closed=23 … exit=0` — `LogDraft.md:28`, `log-entry.md:11`, coordinator note | **CONFIRMED on live bytes** |

## Commands run, verbatim

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py --json /tmp/c1-live-w2.json --quiet
  -> audit_rc=0
  strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
  executes=14 gated=23 broken=0
  lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
```

Instrument digest inside that receipt: `instrument_sha256 = c3c19adcde92…`; `sha256sum` of the file
matches (`c3c19adcde927ac8…`) — the wave-2 "final instrument sha c3c19adc…" is the live file.

### A — exit semantics (four verdict classes probed live)

Source: `corpus/instruments/anchorcheck.py:130-283` — `main()` ends in a `print` loop, **no `return`**;
`:282-283` is `sys.exit(main(sys.argv[1:]))` ⇒ `sys.exit(None)` ⇒ 0. Measured:

| probe | verdict printed | exit |
|---|---|---|
| `anchorcheck.py corpus/knowledge/triage-thresholds.md` | `148 in-range, 0 bad, LOST-RECORDED=18` | **0** |
| `anchorcheck.py corpus/knowledge/citation-bases.md` | `10 in-range, 0 bad, LOST-RECORDED=1, BASE-ABSENT=1` | **0** |
| `/tmp/acprobe2/probe.md` citing `~/Projects/the-bounty-hunter/ops/rank.mjs:55-58`, `KASEGI_MIRROR=/tmp/acprobe/fakemirror` (present, empty) | `MISSING-FILE md:3 …`, `1 bad` | **0** |
| `/tmp/acprobe2/probe2.md` citing `corpus/instruments/README.md:99999`, `KASEGI_LANE_ROOT=<lane>` | `PAST-EOF md:3 … (file has 196 lines)`, `1 bad` | **0** |
| `anchorcheck.py` (no argv) | `IndexError` | **1** |
| `anchorcheck.py /nonexistent-file.md` | `FileNotFoundError` | **1** |

Every measured verdict class — `IN-RANGE`, `LOST-RECORDED`, `BASE-ABSENT`, `MISSING-FILE`, `PAST-EOF`
— exits **0**; only crash paths exit non-zero. Consequence the receipt draws is correct: for the 22
fail-closed lines carrying a `test` clause the **exit status is decided entirely by `test -d`**;
`anchorcheck` contributes printed evidence only. `citation-bases.md` (no `test`) is constant-0 and its
live output today contains `BASE-ABSENT md:31 ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` —
a recorded loss invisible to anyone trusting the exit code.

### B — fail-closed count and the 2 → 1 move

Committed receipts:
```
.ufo/waves/round-25/c1-before.json -> {('passing',0):12, ('fail-closed',2):23}
.ufo/waves/round-25/c1-after.json  -> {('executes',0):14,  ('gated',1):23}
```
Live: all 23 gated entries `lane_exit=1`. Bases measured: `~/Projects/bounties`,
`~/Projects/the-bounty-hunter`, `~/Projects/origin-work` all ABSENT; `~/Projects/ufo-fsd-alpha` PRESENT.
`fail-closed=23` and exit `1` CONFIRMED. (Class renamed `fail-closed`→`gated` in the final
instrument; count stable.)

### C — per-file census of the 23 gated lines (all run today)

| bucket | n | files | anchorcheck summary |
|---|---|---|---|
| parses **0 citations** (Tier-1) | **10** | `claim-gates`, `evidence-dir`, `intake-and-finalize`, `mission-control`, `ops-invariants`, `program-quirks`, `target-checkouts`, `terminal-classes`, `ufo-archive-2026`, `vdp-disclosure-packages` | all `0 in-range, 0 bad, LOST-RECORDED=0, rc=0` |
| every parsed cite `LOST-RECORDED` (Tier-2) | **9** | `claim-package-contract`(2), `ev-model`(5), `intake-surface`(1), `mission-ledger`(2), `operator-queue`(2), `policy-access-playbook`(8), `retirement-autopsies`(2), `submitted-registry`(1), `ufo-workspaces`(9) | `0 in-range`, LOST counts as listed, `rc=0` |
| checks in-range cites (Tier-3 survivors) | **3** | `claim-anatomy-sample`(4+1 LOST), `source-tree-loss-2026-09-28`(11+15 LOST), `triage-thresholds`(148+18 LOST) | all in-range cites are **intra-lane**; `rc=0` |
| no citation instrument at all (Tier-4) | **1** | `repo-git-state.md` | line is `test -d ~/Projects/bounties/.git && git -C ~/Projects/bounties rev-parse HEAD` (`repo-git-state.md:75`) — prints HEAD, compares nothing |

10 + 9 = **19** = the receipt's "produce no checked citation" figure, and the three in-range
checkers + repo-git-state = its "remaining 4". The reported number is internally consistent.

### D — bounties-token invisibility

```
CITE.match('~/Projects/bounties/ops/claim-check.mjs:22')      -> NO-MATCH
CITE.match('~/Projects/bounties/ops/claim-check.mjs:1-233')   -> NO-MATCH
CITE.match('ops/claim-check.mjs:174-199')                     -> MATCH
CITE.match('~/Projects/the-bounty-hunter/ops/rank.mjs:55-58') -> MATCH
```
(Regex at `anchorcheck.py:104` has no `~/Projects/bounties/` arm — confirmed in source and by probe.)
Every gated file's `~/Projects/bounties/…` citations are not merely unopenable: they are **never
counted**, so `0 bad` summaries there certify nothing about the lost base.

### E — inverted line

`root-loss-2026-10-12.md:76` executed verbatim today: exits **0** (all three bases absent,
`ufo-fsd-alpha` present) — a *passing* fail-closed-by-design line, matching the receipt.

## Defect found — smallest safe correction

**Defect (wording/count boundary, fixable):** under the assignment's own phrase — "fail-closed lines
with no citation check" — the count is **20, not 19**. `repo-git-state.md`'s recheck runs
`git rev-parse` and no citation instrument at all; the receipt itself files it under "Tier 4 — no
comparison at all" (`RevRecheckSemantics.md:193-194`) and then excludes it from its own "19".
Two framing slippages compound it:

1. §6 header claims all entries in Tiers 1–3 "cannot ever verify anything, even after restoration"
   (`:176-178`), but Tier-3 includes the three lane-checkers, which *do* verify lane line-stability.
   The set that "cannot ever verify anything" is Tiers 1+2+4 = **20**.
2. The "Net" line (:199-201) counts "no checked citation" = 19 and then folds the 20th
   (`repo-git-state`) into the "remaining 4 … check only lane stability or print-only facts",
   a bucket whose members are described as *checking* something it does not check.

Smallest safe correction (one phrase, no production edit): restate the tally as
**"20 of the 23 fail-closed lines perform no citation check (10 parse zero citations, 9 check only
LOST-RECORDED cites, 1 — `repo-git-state` — runs no citation instrument); the remaining 3 check only
intra-lane line stability."** If the intended unit is strictly *anchorcheck's* "checked citation",
19 stands, but the report should say so and keep `repo-git-state` out of both buckets.

Nothing else falsified: the constant-0 exit, the invisible-bounties arm, the 2→1 exit move, the
inverted `root-loss` line, and both denominators (frozen 35/35, final tree 37/37) all reproduce
on the live bytes exactly as reported.
