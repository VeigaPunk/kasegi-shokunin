# Round-65 verifier spot-check — kasegi

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi r65 · base `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b` · final lane hash
`a33573291dd1867eed2c283516fc1ce38b7dae69` · report `.ufo/reports/round-65/kasegi.md`
(fleet commits `7a19fa3d1dc2b1594f291bf60804136365bd2967` then
`bf01cca52e7d568f438ec0ce0f786819a0d73135`, both by `kasegi-shokunin <kasegi@shokunin.local>`) ·
prompt `.ufo/prompts/kasegi-round-65.md` (814 lines, fleet commit
`e6e4bc602fb7e937abcc4232fce70dac21910818`, 16:19:35, before the 16:19:36 launch).

## Conformance (step 1)

- Report attribution: `git log --format='%an %H' -- .ufo/reports/round-65/kasegi.md` → `kasegi-shokunin
  <kasegi@shokunin.local>` on both commits; the report landed at 16:56:41, after the lane's final commit
  (16:56:33), and cites the final lane hash.
- `grep -c '^## SHONEN'` = 1; four box lines (`[~]`, `[ ]`, `[~]`, `[~]`), one per `SHONEN.md` box.
- Ancestry: all 13 cited lane commits (plus the measured revision `03a23921`) exist and
  `git merge-base --is-ancestor <hash> master` = yes for each: `462ed24a`, `57cb8dec`, `1c36d724`,
  `a333d8ef`, `2f6017fa`, `155737d0`, `55b26e7a`, `5195147`, `2cf5039`, `308e5728`, `90e8f94d`,
  `a3357329`, `03a23921`.
- Lane state (`scripts/hyaku/jj-lane.sh state`): `branch=master local=a3357329 remote=a3357329 ahead=0
  behind=0`; `git status --porcelain` empty — no uncommitted round work.
- Prompt fidelity: §1 mission/AXES binding, §2 1–3 falsifiable claims with the lowest-non-retired-axis
  rule, §3 L2 floor (≥8, matching `MISSION.md` §L2 concurrency), §5 commit-then-push + push scope + L0,
  and all five child-lane items are present (report path §4; "The report lands last and cites the
  pushed lane hash" line 516; `grep -c '^## SHONEN'` requirement line 521; commit-hash citation rule
  line 472; write scope line 448). The run-15 route addendum names the host route table, not a pin.
- Round shape: one v1 wave, 12 seats (`w1-spec.json` items=12; `w1-dispatch.json` counts total=12),
  5 attack seats (2 reviewer, 1 critic, 1 mutation-tester, 1 sentinel) = 42 %, 1 connector; 12/12 seat
  report files committed. `w1-results.json` retains null outputs with one shared kernel-restart note —
  disclosed by the report; verdicts are read from the seat files.
- Marker check: substantive report — claims, per-item pointers, 15-commit round, checkable hashes.
  Status `ok`.

## Claim re-checks

### C1 — depth:verifiability (evidence-verified; the lane gate was not executed)

Receipts (committed, read as bytes):

```
controls/final-verification-tip-r65.txt
  driver_sha256=7f27c4d2fe43db875453478983faa39d44d7aa8ae82b455fb3ff8f039e9f6172
  GUARD driver-self-pin PASS (x2)
  RESULT selftest PASS cases=63 failures=0 exit=0
  RESULT mutbat-candidate PASS SUMMARY killed=4/4 survivors=0 equivalents_held=2 controls_held=1 invalid_rejected=1
  RESULT real-ledger PASS exit=0
  VERIFY measurements=8 failures=0 revision=03a239212633411cf2dbc96beedc672b9c3d0790 ; exit=0
controls/driver-base-donothing-r65.txt
  same driver_sha256=7f27c4d2…, GUARD PASS, VERIFY measurements=8 failures=3 revision=a283189b… (exit not recorded)
controls/driver-construction-r65.txt  8/0 exit=0
```

- `sha256sum .ufo/waves/round-65/verify-r65.py` = `7f27c4d2…` = `driver.sha256`; the driver is
  self-pinned, so the receipt's counter identity is checkable.
- Candidate identity: `sha256sum corpus/instruments/figure-audit.py` =
  `sha256sum .ufo/waves/round-65/figure-audit-candidate-r65.py` = `86becbde…` (adopted byte-identically).
- Implementation: `git diff <base> <tip> -- corpus/instruments/figure-audit.py` adds
  `if status < 0: return status != -signal.SIGPIPE` to `upstream_stale`, maps a negative final status to
  `derive-signal-N` and a negative upstream status to `derive-upstream-signal-N`, pins `EXPECTED_CASES`
  59→63 and adds four selftest cases (middle SIGTERM, SIGKILL with surviving output, final-signal,
  SIGPIPE-non-final benign) plus the flipped `upstream-python-signal-ignored`. Ledger:
  `corpus/instruments/figure-audit-ledger.json` `figures` = 35.
- The claim's frozen driver hash was superseded on the record: `claims-erratum-2.md` (`a5fb3b04…`) and
  `claims-erratum-3.md` (`7f27c4d2…`) each state the supersession and re-measure 8/3 → 8/0; erratum 3
  also records the missing self-pin defect.
- Revision measured is `03a23921`; `git diff 03a23921 a3357329` touches only three receipt files
  (`final-verification-tip`, `census-after`, `fresh-clone`), so the verdict holds at the lane tip.
- Verdict: **improved** — the base false-greens are falsified by the same counter (base 8/3 vs after
  8/0); score held at 4, nominal per QUALITY R58, as the lane states.

### C2 — coverage (re-measured over committed bytes)

```
git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   97 -> 98
git show <rev>:corpus/README.md | grep -cE '^\|[[:space:]]*F[0-9]+[[:space:]]*\|'             43 -> 44
admitted F-rows (status cell)                                                              43 -> 44
git ls-tree -r <rev> corpus/knowledge | grep -c '\.md$'                                      81 -> 82
git show <rev>:corpus/instruments/knowledge-expected.txt | wc -l                             83 -> 84
manifest source records across corpus/source-snapshots/**/manifest.json                      78 -> 79
snapshot directories (manifest count)                                                        38 -> 39
```

- Snapshot: `corpus/source-snapshots/round-65/S098.txt` sha256
  `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2` = manifest `sha256`, 1573 lines,
  170137 bytes; 18/18 manifest quotes ≤25 words and present at their anchors; `body_lines [216,1536]`.
- Registry row: `awk -F'|'` on S098 → NF=13 (11 columns), kind docs, tier A, status mined, opened
  2026-11-04, recheck 180d, `used-by corpus/knowledge/first-psirt-services-framework.md` resolves.
- Frontier: `| F44 | … | admitted | knowledge/first-psirt-services-framework.md | S098 | … |`.
- Instrument-derived terms evidence-verified from committed receipts: `entries=46 pass=46`
  (`controls/base-counters-r65.txt`) and `rows=44 admitted=44 closed=44 problem-rows=0 registry=98` +
  `FRONTIER-PASS F44 ids=S098` (`controls/fresh-clone-r65.txt`); `source-recheck.py … --source S098` →
  18 OK, exit 0 (same receipt).
- Census: `scripts/sources-census.sh validate --root … kasegi` → six pre-existing W04 warnings
  (S028/S029/S072/S076/S080/S085), `kasegi ok …/corpus/SOURCES.md`, exit 0 — same as
  `controls/census-before-r65.txt` and `controls/census-after-r65.txt`.
- Verdict: **improved** — frontier advanced 43→44 with a new, sourced entry on ground F43/F06/F11 do not
  hold; the coverage denominator stays operator-owned (score 8 held, stated).

### Held axis

- depth:density 9 held, not targeted or re-measured; no density credit asserted.
- `git diff <base> <tip> -- SCORECARD.md` is additions-only; no earlier score decreased. QUALITY.md is
  append-only (R84–R91 appended after byte 110820); no existing criterion rewritten.

## Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S098 whole row (FIRST PSIRT Services Framework v1.1) | admit | live `https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1` + snapshot `corpus/source-snapshots/round-65/S098.txt` L1, L219, L229, L853, L918 | agree | Live page title/version, "possible services" purpose and the Service Areas/Services/Functions structure match; snapshot anchors carry qualification gates (L853), isolated reproduction (L918) and disclosure (L1231). |
| "Established finders skip the whole process" at L875 | reject | snapshot L875 | agree | L875 bypasses *qualification and triage* only, routing the report to root-cause analysis and remediation development; intake, reproduction and disclosure remain. |
| "The framework is a compliance standard" | reject | snapshot L219 + live Purpose section | agree | L219 says "possible services"; no normative "shall" or certification claim is made. |
| S098 row quote grounds `teaches` (L853) | ≤25-word check | snapshot L853 | agree | "sometimes called Quality gate and/or bug bars, are used to establish minimum acceptable levels of security quality" = 17 words, verbatim, and grounds the row's CVSS/bug-bar teaches cell. |

Lesson Gate also records URL, access date 2026-11-04 and the full anchored quote list; the rejected
attributions stay as rejections, not silent rows.

## Trend verdicts

- **Expansion — improved.** New sourced knowledge entry on uncovered ground (`coverage` +1 rows, registry
  97→98, knowledge 81→82; F44's distinguishment against F43/F06/F11 recorded in `corpus/README.md`).
- **Quality — unchanged.** No admitted entry superseded or found false and left unmarked; QUALITY.md gains
  only appended criteria R84–R91; the knowledge audit's pre-existing gaps are carried unchanged
  (81→82 lines, fail-closed 22, `cwd_fail=9`; `controls/base-counters-r65.txt`, `w1/ReviewC2Base/NOTES.md`).
- **Discernment — improved.** The wave disagreed in writing and the lane changed course before the final
  measurement: the probe seat's base receipt refuted the spec's P3 sentence (M65-1), the final-mode run
  exposed the driver's base reference (erratum 1, M65-2/M65-3), the critic's H1 and D2 and the sentinel's
  S-02/S-03/S-08 produced errata 2–3 (M65-7/M65-8), and the reviewer independently reproduced the base
  premise (`w1/ReviewC1Base.md` PREMISE HOLDS).

## Routed defects (status-neutral; lane to fix next round)

1. **Report's commit→LOG ties cite non-existent labels.** The Landed-changes table says "LOG bolts 1–12";
   `LOG.md` Round 65 has 10 bullets and the word "bolt" appears nowhere in it. Cite bullet indices (e.g.
   "§ Round 65 bullet 4") or tie each commit to its LOG evidence line.
2. **Two round commits missing from the Landed-changes table.** `git rev-list --count base..tip` = 15
   commits; the table rows name 13. Unlisted: `1929a47` (widen S098 body range, M65-9) and `6824522`
   (re-record the final-tip receipt).
3. **"Exact final driver" label is wrong for the cited before receipt.** The report's before block cites the
   `base-finaldrv2` workdir, whose receipt (`controls/driver-base-donothing-finaldrv-r65.txt`) records the
   erratum-1 driver `5aa842ab…`. A same-result base receipt from the final driver exists —
   `controls/driver-base-donothing-r65.txt` (`7f27c4d2…`, 8/3, self-pin PASS); cite that one.
4. **"Final tip" is not the lane tip.** The tip receipt names revision `03a23921`, while the lane tip is
   `a3357329` (two receipt-only commits later). Name the revision as measured and state the delta, or
   re-run at the tip; the verdict itself is unaffected.
5. **Base receipts record no exit code.** `driver-base-donothing*.txt` end at `VERIFY … failures=3` with no
   `exit=` line, while the report claims "exit 1". Capture the exit status in every receipt.
6. **Sentinel helper-count phrasing.** `w1/SentinelScope/07-parser-sort-compress-exec.txt` shows
   `marker lines=121900 (two gate runs; ~60950 program invocations per run)`; the report's "executed a
   helper 121900 times" would read as one run. State per-run counts when re-citing.

## SHONEN note for the operator

Box 2 (end-to-end domain task) remains `[ ]`: source roots absent and live-target testing refused, as in
rounds 59–64. Boxes 1, 3 and 4 are checkable by a non-author if a promotion review is dispatched; promotion
remains operator-owned and no box was marked here.
