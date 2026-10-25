# CritGlobal — round-28 whole-claim falsification pass (wave 1)

seat: CritGlobal (UFO-FSD critic, leaf; no production edits)
lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
lane base (claims freeze): c9f8b115a098c65356e4b3b6048af45a37ab8395
claims: .ufo/waves/round-28/claims.json (frozen; C1/C2)
measured: 2026-10-25 UTC (after-state at 17:22–17:35Z; landed instrument digest 95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514, stable during my batch)

Method: re-ran both claims' frozen counters on (i) base bytes (`git archive c9f8b115a098c65356e4b3b6048af45a37ab8395` of anchorcheck.py + committed r27 fixtures) and (ii) landed working-tree bytes; swept all 43 corpus + lessons + SKILL.md files old-vs-new verdict vectors; read every wave receipt under `.ufo/waves/round-28/receipts/` and `wave1/`; read the L1 erratum `claims-erratum-1.md`; read the staged assimilation package (read-only). Reported 2026-10-25; all counters below exit-observed, none fabricated.

---

## 1. Before-values: HONEST (re-run from base, all match)

From `git archive c9f8b115…` (pre-change anchorcheck.py sha256 c2a9e6c6…, byte-identical to claims.json before.instrument_sha256; the four round-27 fixtures are committed at `c2ab51d`, an ancestor):

| frozen before | claimed | re-measured from base bytes |
|---|---|---|
| bad_fixture_exit | 0 | 0 (BASE-ABSENT md:2 printed, exit 0) |
| bounties_fixture_BOUNTIES_lines | 0 | 0 (CITE has no bounties arm; cite invisible) |
| selftest_receipt_lines | 0 (crash exit 1) | 0, FileNotFoundError '--selftest', exit 1 |
| skill_md_exit / bad / LOST-RECORDED | 0 / 0 / 306 | 0 / 0 / 306 |
| instrument_sha256 | c2a9e6c6… | c2a9e6c6… |

R4 (resolvable work commit) holds for the before side: base is an ancestor of HEAD (`git merge-base --is-ancestor` exit 0). No before-value is inflated.

## 2. After-values on the landed digest: C1(a)(b)(d) and C2 counters all reach their after values

Measured at digest 95333e29 (stable before==after across my runs and across the ExecGateLog/ExecReceiptCanonC1 batches):

- C1(a) bad-fixture exit 1, BASE-ABSENT printed. C1(b) BOUNTIES-ABSENT lines = 1. C1(d) SKILL.md exit 0, LOST-RECORDED=306, BASE-ABSENT=0, PIN-BROKEN=0, OUTSIDE-BASE=0 (byte-identical summary to skill-before.txt). `--selftest` prints `selftest cases=9 failures=0`, exit 0; each of the six FAIL_CLASSES has exactly one failing fixture (cases 1–6: MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT) plus three controls; each fixture's env isolates the limb (KASEGI_LANE_ROOT/MIRROR/ORIGIN_ROOT/BOUNTIES overridden; subprocess per case). I could not find a non-isolating fixture.
- C2: frontier_admitted 12 (F12 row), entries citing S042 = 1, S042 registry row present, census exit 0 / 42 rows, harness entries=15 pass=15 exit=0, source-recheck exit 0 on S041 and S042 (6+6 quotes, all occurrences=1), entry recheck line cwd-independent (verified from /), S041 used-by gained the entry (old→new logged in SOURCES.md), S042 used-by exactly the entry. Manifest path stem == id, sha256 pins bind the committed captures (S041 re-capture byte-identical to round 26, e18acbf9…; S042 b432ec16…). Gate draft records ≥1 admit (F12 entry + S042) and ≥1 reject (Chinese thresholds re-confirmed; vendor-third-party new refusal) with inline quotes ≤25 words. R14 landed as QUALITY.md criterion and is practised in-round (no corpus-sized fixture trees committed; largest scratch is 7.4 MB fetched body, below the tarball threshold or to be excluded from commit).

## 3. Falsification findings — what is FALSE or UNPROVABLE-as-stated right now

### F1. C1 `corpus_disclosure` cell (claims.json) is FALSE as worded — erratum already filed
The frozen sentence: 4 corpus marked bounties citations (claim-gates.md, intake-and-finalize.md, mission-control.md, source-tree-loss-2026-09-28.md) "newly classify LOST-RECORDED after the arm". Measured: those four named lines are `source: [lost-tree] ~/Projects/bounties/…` **provenance headers written without backticks** — `TOK` is backtick-only, so they are not tokens before OR after; the four files' LOST-RECORDED counts with the new instrument are 0/0/0/15, unchanged from the pre-change instrument. The only backticked anchored bounties citations in the whole lane are in anchorcheck.py's own selftest strings. The erratum `claims-erratum-1.md` corrects this ("zero backticked anchored bounties citations exist… no verdict-class movement anywhere") and the correction is TRUE — my old-vs-new sweep of all 43+ files shows zero per-file verdict-class deltas (LOST-RECORDED totals 374 → 374). So: the disclosure cell is false; the stronger no-harm statement is true. The claim as frozen, before erratum, is not reproduced.

### F2. C1(c) "committed in the round receipt index" — index ABSENT at measure time
`.ufo/waves/round-28/c1-receipt-index.txt` does not exist. ExecReceiptCanonC1 explicitly created no canonical file; `assemble-receipts.py` is an L1-close step. So the frozen counter (c) limb (`grep -cE 'selftest cases=' …c1-receipt-index.txt` → 1) is NOT reachable yet. The selftest itself runs and prints the required line; the committed-index half is PENDING. After-value (c) is unprovable until the L1 lands the index at the committed digest.

### F3. C2 close-out gate RED: recheck-audit expected list not regenerated
`corpus/instruments/knowledge-expected.txt` still holds 41 lines / 39 entries; the F12 entry is the 40th. `recheck-audit.py` at the final bytes prints `lines=40 total=40 pass=40 … expect=present expected=39 missing=0 unexpected=1 exit=1`. README's own round-28 reconciliation says the list must become 40 entries / 42 lines in the same round the entry lands. ExecExpectedList (read-only) did not regenerate it; the refresh is an L1-run step. As of measure, the lane's expected-list gate is red — the C2 after-state is reached only if the L1 regenerates (or the round publishes the red explicitly).

### F4. R3/R4: every after-value is measured on uncommitted (working-tree) bytes
The wave is mid-flight: the round-28 lesson file is ABSENT (ScribeLessonGate is a draft-only seat; `corpus/lessons/round-28.md` does not exist), source-snapshots/round-28 is untracked, and no production change is committed. Receipts pin digests (good — post-commit re-verification is possible), but per R4 a round counts only with a resolvable work commit; as of 17:35Z the claims' after-cells are "measured, not committed". Not a defect if the L1 commits atomically and re-runs the gate block at the commit.

### F5. Frozen counter (d) limb 2 is vacuous on BOTH byte sets
`sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'` matches the summary grammar "N bad; K distinct anchors" — the regex expects "bad; N bad". Output: 0 lines pre-change AND post-change, including on a file with bad=1 (corpus/QUALITY.md). So the kill-rule limb "bad count moves" cannot be detected by the frozen command; the no-movement fact was verified only by field extraction (bad=0 identical before/after) in the canonical batch, not by the frozen command. This is a defect in the claim's own counter (same class the round-25 mutation seat fixed for the three-limb predicate), not a kill — but the frozen command as written would not catch a bad-count move.

### F6. "No axis harmed" outside SKILL.md: corpus surfaces now exit 1 — disclosed, but outside the claim's (d) scope
The new fail-closed exit flips anchorcheck exit 0 → 1 on 18 corpus/lessons files carrying pre-existing unverifiable verdicts (BASE-ABSENT/PAST-EOF), including `corpus/QUALITY.md` (bad=1, exit 1) and `corpus/knowledge/citation-bases.md` whose own recheck line runs anchorcheck unguarded and now exits 1. Count unchanged (18 before, 18 after) — the exit flip, not a verdict change. The C1(d) no-harm promise names only SKILL.md; the corpus red is intended per predicate (a) and is disclosed (ExecImplC1 O3; Gate draft), but "no axis harmed" in the claim's literal text applies to SKILL.md only, not to the corpus gate surfaces the same round now marks red (plus the F3 expected-list red).

## 4. Strongest honest counter-case (for the L1 to answer)
1. The frozen `corpus_disclosure` sentence is false as worded (F1); the erratum supersedes it — confirm the erratum is appended to the round lesson once ScribeLesson lands.
2. C1(c) committed-index limb and the C2 recheck-audit expected-list gate are both unlanded at measure (F2/F3) — both are L1 close-out steps; the claims cannot be certified until they land and are re-run at the commit.
3. All after-values are uncommitted (F4) — R4 requires the commit; re-run the gate block at the final commit, not at 17:29Z bytes.
4. The frozen (d) sed counter is vacuous (F5) — replace it in the post-round instrument (it cannot detect a bad-count move).
5. The corpus exit-flip (F6) is a behavior change to 18 recorded corpus surfaces; it is disclosed but not covered by the claim's no-harm text — say explicitly in the lesson that corpus surfaces now fail closed and that is the intended feature, not a regression.

## 5. What passes
Before-values honest; C1(a)(b)(d) and the selftest run itself pass on the landed digest; C2's frozen counters (frontier, entry, row, census, harness, rechecks, manifest Q9) all reach their after values; the Gate rejects/(admits carry ≤25-word inline quotes; the disclosure erratum's stronger no-harm (zero verdict-class movement anywhere) is verified; R14 landed and is practised.

## 6. Re-run commands for the L1 (post-commit)
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt
grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo bad_fixture_exit=$?
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py --selftest; echo selftest_exit=$?
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo skill_exit=$?
python3 corpus/instruments/recheck-audit.py | tail -2   # must be expected=40 unexpected=0 exit=0 after ExecExpectedList regeneration
python3 corpus/instruments/frontier-recheck-count.py | tail -1
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
```
