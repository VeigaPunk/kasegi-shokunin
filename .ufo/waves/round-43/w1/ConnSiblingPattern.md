# ConnSiblingPattern — sibling instrument/contract pattern scan (kasegi round 43)

Seat: `ConnSiblingPattern`, leaf (no subagent dispatch, no swarm).
Base: `ab98fac9dce87130bc4f66de89e30650d63943dc` (lane tip at seat start `4cb6d4a`).
Axes served: `depth:verifiability` (primary), `coverage`.
Read first: `.ufo/waves/round-43/claims.json` (frozen; not edited), then
`c1-controls/do-nothing.txt`, `c2-controls/before.txt`, `w1-spec.json`, `w1-dispatch.json`,
`corpus/knowledge/claim-package-contract.md`, and the r42 in-lane instruments that the round-43
deliverables extend.

## Deliverable

| path | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ConnSiblingPattern.txt` | 445 | `c251ec4db2104504a025374ba03c9453e6e9a1972bd362380f091e58a33db26f` |

Landable text only: no validation table, no notes, no non-landed heading. Sections 1-6 are the six
requested pattern families; section 7 is the contradiction set; section 8 is the reject list.

Counts inside the deliverable (verified by `grep -cE '^P[0-9]+\.[0-9]+ (ADOPT|HOLD|CONTRADICTS)'`):
34 entries — 27 `ADOPT`, 7 `HOLD` (P1.4, P2.5, P3.8, P3.10, P4.5, P5.4, P5.5) — plus 5 `X<n>`
contradictions and 3 reject-list items. Every entry cites `path:line` and names the kasegi
deliverable it should inform (`r43-closure.sh` K1-K19 / `claim-package-check.py` /
`corpus/knowledge/claim-package-gate.md` / the round-43 receipt / `declared-blocks.txt`).

## Scope actually read

17 sibling lane repos sit beside the lane. Nine carry a non-empty `tools/` tree; those nine were
read and all nine are cited. The other eight carry no instrument tree to borrow from.

```
### A. lane inventory (17 siblings, 9 with an instrument tree)
145	souji-shokunin
91	kama-shokunin
81	tsukuroi-shokunin
43	mori-shokunin
33	tameshi-shokunin
28	kotodama-shokunin
22	kaidoku-shokunin
17	mado-shokunin
14	chousa-shokunin
0	tabi-shokunin
0	revenger-shokunin
0	lore-shokunin
0	kumitate-shokunin
0	kotoba-shokunin
0	kengaku-shokunin
0	kake-shokunin
0	kagi-shokunin
```

Command:
`cd /home/vgpnk/Projects/shokunin && for d in */; do if [ -d "$d/.ufo" ] && [ "$d" != "kasegi-shokunin/" ]; then printf '%s\t%s\n' "$(ls "$d"tools 2>/dev/null | wc -l)" "${d%/}"; fi; done | sort -rn`

Files read in full or in cited ranges: `chousa/tools/research-gate.sh` (8812 lines: header 1-30,
token matchers 1860-2010, drift reporter 4213-4260, selftest 4377-6000, fail-closed arms 2214-2226
and 6303-6316), `chousa/tools/{inference-ground,quarantine-check}.py`,
`kaidoku/tools/round-44/c2-counter.py`, `kaidoku/tools/round-34/replay-gate.py`,
`kaidoku/tools/round-42/fetch-carrier.py`, `kama/tools/{kama-ollama-evidence,digest-ledger,
report-landing-audit,round42-digest-audit,round41-pinwatch-audit,round60-c2-counter}.py`,
`kotodama/tools/gates/handoff-packet-check.py`, `kotodama/tools/harness/{receipt_guard,
round_runner_conformance}.py`, `mado/tools/mado-geometry.py`,
`mori/tools/{mori-census.sh,mori-routed-r24.py,mori-blind-check.sh}`,
`mori/corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`,
`souji/tools/cand-c2-clusterc-selftest.sh`, `tameshi/tools/receipt-measure.py`,
`tsukuroi/tools/{check-report-receipts,check-kernel-taint,check-package-anatomy-r41}.py`.

## Citation audit

Every `path:line` in the deliverable was resolved against the file on disk and checked for range.

```
distinct path:line citations = 41
lanes cited = 9  (chousa-shokunin, kaidoku-shokunin, kama-shokunin, kotodama-shokunin, mado-shokunin, mori-shokunin, souji-shokunin, tameshi-shokunin, tsukuroi-shokunin)
out-of-range or missing = 0
per-lane citation counts: chousa-shokunin=12, kaidoku-shokunin=6, kama-shokunin=6, kotodama-shokunin=7, mado-shokunin=2, mori-shokunin=3, souji-shokunin=1, tameshi-shokunin=1, tsukuroi-shokunin=4
```

A second audit resolved the 15 in-lane citations (`r42-closure.sh:<n>`, `r41-closure.sh:<n>`):
15 distinct, 15 in range, 0 problems.

Citations were repaired against the bytes during the pass; the deliverable carries only the
corrected values. The substantive repairs: the `+`/`-` token entry (P3.7) was rewritten after
reading `research-gate.sh:4213-4234` — those prefixes are the *reporter's* diff vocabulary
(`gate_drift_field_report` emits `-<key>` for a vanished field), not argument operators in
`tdrift`; the first draft had them as argument syntax and was wrong. Also corrected:
`r42-closure.sh:18` for `suite-sha256` (was 19), `r42-closure.sh:26-27` for the exit table (was
25-27), `c2-counter.py:23-24` (was 20-24), `handoff-packet-check.py:724-830` and `:741-747` /
`:795-806` (were 743-830 and 791-797 / 800-806), `digest-ledger.py:39-53` (was 43-50), and the
`fence_scan` / `fence_open_at_eof` lines (306 / 337-342, were drafted as 1544-1552).

## The one measured divergence (deliverable P5.1)

Both token matchers were re-executed from their source bytes: `r42-closure.sh:348-370`
(`TOKEN_BAD` / `token_at` / `value_present`) and `research-gate.sh:1867-1906`
(`TOK_WS` / `TOK_PUNCT` / `tok_word_char` / `tok_right_ok`).

```
hay                      needle         kasegi  chousa  want   verdict
closed=19/19 exit=0      closed=19/19   True    True    True   agree
closed=19/19-rc1         closed=19/19   True    False   False  kasegi-mismatch
closed=19/19:61          closed=19/19   True    True    False  kasegi-mismatch
closed=19/19,            closed=19/19   True    True    True   agree
(closed=19/19)           closed=19/19   True    True    True   agree
closed=19/190            closed=19/19   False   False   False  agree
```

Reading: kasegi's `TOKEN_BAD` (digits, `/`, `.`, `=`, `_`, ASCII alnum) omits `-` and `:`, so a
hyphen- or colon-continued `closed=19/19` reads as a whole token there. chousa's joiner rule closes
the hyphen class and leaves the colon class open (`:` is in `TOK_PUNCT`). Neither lane closes the
colon class; the deliverable states that as a named limit rather than implying a fix. This matters
because K15 grades quoted `closed=` values against committed transcripts.

## Regression corpus, measured not asserted (deliverable X5)

```
### D. SIGPIPE regression corpus
r41-closure.sh grep -q sites: 12
r42-closure.sh grep -q sites: 0
r42 scratch/signal handling: SIGTERM=0 atexit=0 trap=0
### E. lessons mentioning the sigpipe class
0
```

Commands: `grep -c 'grep -q' corpus/instruments/r41-closure.sh`, the same for `r42-closure.sh`,
`grep -c SIGTERM|atexit|trap` on `r42-closure.sh`, and `grep -rl -i 'sigpipe' corpus/lessons | wc -l`.
The twelve r41 sites are `r41-closure.sh:904, 973, 1029, 1030, 1031, 1186, 1570, 1571, 1572, 1642,
1935, 1936`; the class is documented at
`mori-shokunin/corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md:4-30` and fixed at
`mori-shokunin/tools/mori-census.sh:3301-3324`. Two consequences the deliverable records: r43 must
not reintroduce the shape, and the r42 export is left on disk after a run because the driver has no
cleanup and no signal handler (compare `kama-shokunin/tools/round41-pinwatch-audit.py:210-215`).

## Contradictions flagged (L1 decides; no sibling was edited)

1. **X1** — chousa's "absence/malformation is exit 2 so cannot-compare cannot masquerade as clean"
   (`research-gate.sh:5968-5970`) must not be folded onto an unresolvable ref. The frozen C1
   contract requires `ref-not-found` at **exit 1**, and the kill rule makes its absence a defeat.
   Different objects: absent input baseline = cannot-compare; absent ref = red. Highest-risk import
   in the scan.
2. **X2** — kaidoku's exit `3` for UNEVALUABLE (`replay-gate.py` SELFTEST_CASES) must not enter the
   r43 exit table, which is 0/1/2 (`r42-closure.sh:26-27`).
3. **X3** — mado's conditional summary-line shape (`mado-geometry.py:65-70`) is not available:
   kasegi payloads may grow fields, summary lines may not, because K8/K10 and the C2 summary are
   parsed.
4. **X4** — kotodama's triple agreement (committed `.expected` + in-code table + emitted set,
   `handoff-packet-check.py:697-701`) is adoptable, but its single-fixture economy is not: C2 needs
   nine separate defect fixtures.
5. **X5** — the r41 SIGPIPE class is closed in r42 and must stay closed; kasegi has no lesson file
   recording it.

## Not done (scope discipline)

- No sibling lane, fleet-root file, or `shokuknow` file was written, moved or deleted. All writes
  are the deliverable plus this receipt, both under `.ufo/waves/round-43/w1/`.
- No mutating git/jj command anywhere: no add/commit/push/checkout/reset/stash/branch/tag/worktree.
  Only `git log`, `git ls-files`, `git rev-parse` were used, all read-only.
- No network fetch was made, so no HTTP status/byte/UTC triple applies.
- No subagent, no swarm, no second judge.
- No instrument was run against the claim-package contract; this seat produces findings, not the
  C1/C2 instruments.

## Tooling

No tool was installed, upgraded or removed. No `pacman`, `uv`, `npx` or PATH-directory write.
Existing `python3` and `coreutils` were sufficient.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r43/ConnSiblingPattern`, created with `mkdir -p`; all probe scripts,
work copies and captured evidence were bound there (`TMPDIR` not relied on). Disk guard checked at
start (`scripts/hyaku/disk-guard.sh status`: `/fast/scratch/hyaku/kasegi-r43` at 26.8G, no
pressure warning). The directory is removed before yield; no scratch artifact is left behind.

## Handoff — what the L1 should read first

For C1: **P3.1 + P3.2** (implementation mutants with the anchor-missing guard) and **P3.7** (the
diff vocabulary that makes a superseded literal's absence assertable). For C2: **P3.3** (dual
witness), **P3.4** (exact rule set), **P3.5** (single-replacement fixtures), **P3.6** (tautology
control). For the driver: **P1.2** (export cleanup + SIGTERM) and **P1.1** (tar containment). For
the header: **P4.4** (frozen predicate sentence quoted with its claims path). Then **X1** before
anyone imports chousa's exit-2-for-absence rule.
