# Round 26 — kasegi

Lane: kasegi-shokunin. Round base (claims freeze commit) `1b076fa7f2fb5e7dd9d87449514eba526043421b`. Two frozen claims (`.ufo/waves/round-26/claims.json`, frozen 2026-10-25T12:27:41Z before any measurement or dispatch): C1 depth:verifiability (the lane's lowest non-retired axis, score 4, held) and C2 coverage (score 7, held). The claims file is committed at the freeze commit; its bytes are unchanged from that commit (`git show 1b076fa7:.ufo/waves/round-26/claims.json | sha256sum` = `343e568e7113f0d63ea63f7c9b8d7c18f44e310a67717d490a35ae1adec6741f` = the working-tree file), so no in-place edit happened after freeze — R25-1's rule, complied with this round.

## Overview — claims and counters

| Claim | Axis | Counter (frozen, exact) | Before | After |
|---|---|---|---|---|
| C1 | depth:verifiability (4, lowest non-retired) | (a) `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` | 0 | **1** |
| C1 | — | (b) `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` | 0 | **1** |
| C1 | — | (c) `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md \| grep -v 'round-24.md:77' \| wc -l` | 1 | **0** |
| C1 | — | (d) `python3 corpus/instruments/recheck-audit.py --root <scratch-tree-with-one-knowledge-entry-deleted> --cdroot <lane-root>` | exit 0 (36/36 lines) | **exit 1 naming the deleted entry** |
| C2 | coverage (7) | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | 10 | **11** |
| C2 | — | `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md \| wc -l` | 0 | **3** |
| C2 | — | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0 (rows 40) | exit 1 at compose — see §Gate kill-rule status and §Fixes item 5 |

C1 kill rule: any counter misses its after value, or the do-nothing control hits any after value. C2 kill rule: a source row is appended without an admitted entry citing it; or census exit ≠ 0 at round end. Status at compose is recorded in §Gate.

### Which bytes each number reads

- `recheck-audit.py` pre-change bytes (round-25 pinned digest) = `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`; the working tree was byte-identical to round-25 tip `41a77b8` before e1's change (revenger `r1-digest-lineage.md`: `cmp` identical, sha equal). The lane's own change is forward-only and is the only instrument edit this round.
- The C1 receipts (selftest, live audit, controls) are produced by the one instrument; the round's committed receipt index is `.ufo/waves/round-26/c1-receipt-index.txt`.
- The C2 admissions are the F11 row in `corpus/README.md`, the S041 row in `corpus/SOURCES.md`, and the two new knowledge entries.

## Gate — the assimilation set

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi` (read-only; no campaign tool run there). Round shape: ONE theme — ISO/IEC 29147/30111 division-of-labour (JPCERT/CC 2026 P-guideline) — with two entries, plus the quarantine slice hand-check and the two standing rejects.

### Collision / adoption ids

Id-collision check ran at freeze in scratch: registry `reg=40`, staged `staged=94`, collisions=10 (S031–S040); adopted ids continue the lane registry from **S041**. The staged rows S076 (division-of-labour anchor) and S064 (付録6 §4 + 参考1 anchor) are renumbered **by document** into one adopted lane row, S041 = JPCERT/CC 2026 partnership guideline capture; citations re-point by URL/anchor — evidence is the document, never arithmetic. Staged S068 (Cisco page, used by the staged crosswalk) is NOT newly adopted: the same document is already lane **S040** (round 25), confirmed by the quarantine hand-check below.

### Admitted

| Row | Admitted as | Document / capture | Opened | Evidence | Entry |
|---|---|---|---|---|---|
| S041 | A, `mined` | 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC), `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | 2026-10-25 | `corpus/source-snapshots/round-26/S041.txt` (pdf capture via `capture-source.py --kind pdf`, status 200, fetched 1,338,665 B → 147,267 B, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`, utc 2026-10-25T12:34:17Z, 2,354 lines); manifest `corpus/source-snapshots/round-26/manifest.json` binds 7 quote assertions (`source-recheck.py --source S041` exit 0, all `occurrences=1` or anchor-verified) | both F11 entries |

Staged adoption ids: staged **S076** → adopted S041 (§2/図1 division paragraph, `S041.txt:1667-1678`); staged **S064** → adopted S041 (§4 + 参考1, `S041.txt:1691-2079`); staged S068 (Cisco) → already lane S040 (round 25), not re-numbered.

Entries (both created this round, Q1–Q9 conformant, `source:` = S041, `recheck:` = the pinned `source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041` command with `cd <lane-root> &&` prefix):

| Entry | Lines | What it holds | Ground |
|---|---|---|---|
| `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` | 54 | 29147 = outward-facing handling (receipt + advisory distribution), 30111 = in-house verification/mitigation process, 図1 correspondence; supported by Hitachi's step mapping (S039) and Cisco's 2018 edition claim (S040). Rejected over-generalizations ("29147 is only about receiving reports"; "vendors follow 29147:2014") with evidenced falsification. | F11 — adopts staged `iso-29147-and-30111-division-of-labour-2026-10-23.md` re-grounded |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | 67 | The P-guideline's own divergence sentence (policy not required by the guideline, required by 29147:2014), the 7-day receipt guidance, the 6.2/6.3 republication, and the 参考1 clause table (clauses 6/8 have no guideline counterpart); falsifiable rules and rejected over-generalizations. | F11 — adopts staged `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` re-grounded |

Both F11 rows' claims were quote-located independently in the ORIGINAL PDF (scout s5): division paragraph FULL 2009-2010 (printed p.45), 図1 caption FULL 2020 (printed p.46), divergence sentence FULL 2238 (printed p.50), 7-day FULL 2291 (printed p.51), 6.2/6.3 markers FULL 2180/2225, 参考1 header FULL 2382-2383 (printed p.54-55). The staged anchors had page drift (図1 caption is on printed p.46, not 45; §4 divergences on p.49-50, not 46-47; 参考1 on p.54-55, not 53-54), which is why the entries cite capture lines, not the staged page numbers.

### Refused (rejects carry flip conditions)

| Candidate | Failing gate | Reason (evidence) | Flip condition |
|---|---|---|---|
| `vendor-cvd-policy-crosswalk-2026-10-23.md` | Q7, Q3, ground | (1) Q7 — its `recheck:` is prose with a command inside backticks plus a `(ran …)` tail; `bash -n` fails (s3 strict-limb check: parse/cwd/paths/instrument/own fail, 4/6 strict limbs) — same shape the round-25 verifier recorded for the staged text; (2) its `ground: F20` names no lane frontier row (`grep -cE '\| F20 ' corpus/README.md` → 0); (3) Q3 — the staged entry asserts "the two conditions under which it will go faster" while its own bytes of record list FOUR disclosure-trigger conditions (`S040.txt` L301, L302–L304, L305–L308, L309) — the round-25 verifier re-opened the live page and both agree. | Restate the count with line anchors, cite the lane id S040 (already registered round 25), and ground on an indexed lane row — which is what the admitted F10 entries already do under a different name, so the refusal is of the staged text, not of the theme. |
| `chinese-criminal-thresholds-and-authorisation.md` | Q2 + Q4, and Q1/Q7 | Refused round 24; reason retained: its own cited 第二百八十五条 text (S045) carries no 情节严重 element for the first paragraph while the entry asserts "criminal risk attaches to scale and effect, not to the mere act"; "purely quantitative" is falsified by 第一条(五) 其他情节严重的情形 (S044); its `recheck:` is prose and its `curl -sSL` exits 0 on a 404; `ground: F12` names no lane frontier item (round-24 lesson §Refused; s3 re-confirmed the same strict-limb failures this round). | Restate 285(1) as a conduct offence, quote 第一条 in full including (五), make the recheck fail closed, add `### Rejected`, register the rows under lane ids. |

No Q/R bar was relaxed for either reject.

### Quarantine slice — seven rows hand-checked (scout s4, 2026-10-25)

The absent-defect-register slice (`assimilation/quarantine-slice`) holds seven kasegi rows: S037, S054 (`payload-absent`); S048, S065, S068, S069, S070 (`could-not-be-fetched`). s4 re-fetched each source today with the lane instrument UA and attempted quote location (`wave1/quarantine-verdicts.txt`):

| Staged row | Register class | Verdict (2026-10-25, instrument UA) | Meaning for adoption |
|---|---|---|---|
| S037 | payload-absent | `fetched no-quote` — GB/T 30279-2020 catalogue page 200/24,189 B; the staged quote is a composite that concatenates separate table cells; never occurs contiguously | reachable + authentic metadata, quote-form defect: not appendable as staged (cell-anchored fragments would be needed) |
| S054 | payload-absent | `fetched no-quote` — IPA request PDF 200/513,648 B; the quote spans a line break with an interpolated legal-citation parenthetical | source real, quote is a shortened re-construction: not appendable as staged (corrected longer fragment needed) |
| S048 | could-not-be-fetched | `unfetchable` — `gbDetailed?id=3B865A…` returns **404**/748 B (Tomcat `未找到`); dead as cited | refuse until an R8 `supersedes` row names a live id |
| S065 | could-not-be-fetched | `fetched quote-located` — npc.gov.cn PDF 200/7,465,472 B; staged fragments (现行有效法律目录, 刑法（7 件）, 2009 年修正） present verbatim, full clause wraps only at a PDF line break | reachable + quote located; row not adopted this round (not cited by the admitted entries) |
| S068 | could-not-be-fetched | `already-mined-legacy` — Cisco policy 200/94,027 B at the final URL; quoted sentence `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018` located verbatim | already mined as lane S040 (round 25); no new row needed |
| S069 | could-not-be-fetched | `unfetchable` — `gbPlan/download?path=…` 302/0 B; redirect target fails TLS (curl 60) | unverifiable from these endpoints |
| S070 | could-not-be-fetched | `unfetchable` — same 302/0 B + TLS-failing redirect | unverifiable from these endpoints |

`payload-absent` and `could-not-be-fetched` remain the register's unchecked families; reachability today does not certify a quote, and for S037/S054 the staged quote is not verbatim anywhere, so neither is appendable as staged.

### Kill-rule status (as composed, 2026-10-25)

- **C1:** (a) 1 ✓, (b) 1 ✓ (with the caveat in §Fixes item 2), (c) 0 ✓, (d) exit 1 naming the deleted entry ✓ (verified in scratch on the landed instrument). Do-nothing control (pre-change bytes, m1 mutant E) stays 37/37 exit 0 and cannot reach any after value. C1 kill rule: satisfied at compose for (a)/(c)/(d); (b) requires the receipt-index regeneration below before commit.
- **C2:** F11 admitted (awk 11) ✓; entries citing S04x = 3 (S040 round-25 entry + both new S041 entries) ✓; sources census exits **1** at compose (E09 on the S040/S041 recheck cells — §Fixes item 5), so the C2 kill-rule limb "census exit ≠ 0 at round end" is **not yet satisfied** and must be cleared before round close by the cadence-only cell correction. The kill rule's other limb (a source row appended without an admitted entry citing it) is satisfied: S041 is cited by both admitted entries.

## Mistakes

**M26-1 · the receipt index was written before the instrument change landed (R25-2's own trap).** Class: pinned-value path written against pre-change bytes. Evidence: `c1-receipt-index.txt` pins `instrument_sha256=c3c19adc…` and `selftest cases=14 failures=0` while the landed instrument is `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` with `selftest cases=15 failures=0` (e1's change landed after the index was written; the revenger and critic both flagged the same). Captured-by: R13's "one frozen instrument" rule applied to the *receipt line*, not the *receipt time*; the index must be regenerated at the final digest before commit (the fix is listed in §Fixes item 2).

**M26-2 · a mid-wave instrument revision that did not parse.** Class: landed-draft breakage. Evidence: during e1's iteration the working-tree `recheck-audit.py` briefly contained a duplicated `def load_expected` and a dangling `if record:` (IndentationError at lines 173-174, `py_compile` exit 1; a later iteration failed at line 253-254). The final bytes parse and pass `--selftest` (15 cases). Captured-by: none at write time — a tracked file can be broken between edits; the selftest and compile are the controls (§Fixes item 1/4). This is recorded as a transient state, not a round claim.

**M26-3 · frontier row admitted before its entries existed, and under the staged filenames.** Class: admission-before-entry ordering + name mismatch. Evidence: `corpus/README.md` F11 row (added by w4) cites `knowledge/iso-29147-…-2026-10-23.md` (staged-package names), while the scribes created `knowledge/iso-29147-and-30111-division-of-labour.md` and `knowledge/iso-29147-divergence-and-clause-crosswalk.md` (no suffix). `frontier-recheck-count.py` therefore raises `FileNotFoundError` (exit 1, no summary) on the live map — measured by e8 and the C2 critic both before and after the entries landed. Captured-by: e8's simulation (row-before-entries crash) and k2/k3. Fix: align the F11 row's entry cell with the actual entry names (or name the entries as the row does) before round close; the awk frontier counter itself is unaffected (11).

**M26-4 · the C2 frozen counter cannot isolate "first registered this round" and counts empty shells.** Class: counter overmatch / vacuity. Evidence: `grep -lE '^source: S04[0-9] '` matches S040 (round-25 F10 entry `vendor-disclosure-policy-commitments-crosswalk.md:2`), so the before value is 1, not 0 — the do-nothing control hits the after value (`>=1`) with zero round-26 work (e7 do-nothing receipt; k2; m3). Empty-shell entries satisfy every frozen C2 counter (awk 11, grep ≥1, census used-by edges, frontier harness pass). Captured-by: m3 gameability probes + k2 vacuity attack. The substantive counter this round therefore is the **content** of the two entries (Q1–Q9, body quotes pinned to the manifest), which the frozen counters do not see; this is recorded, not re-worded (claims are frozen).

**M26-5 · the R25-5 recheck-cell note breaks the sources-census grammar.** Class: record-correctness vs contract format. Evidence: the S040/S041 `recheck:` cells carry `180d — <prose>`; the census accepts only ISO date / NNd / symbolic cadence, so both rows raise E09 and the census exits 1 — the C2 kill-rule blocker (k2/k3 measured; §Fixes item 5 has the smallest safe correction). The R25-5 record itself (final URL, two-hop redirect chain, instrument-UA requirement) is correct and receipted (s2 probe).

**M26-6 · the fix-control #3 restatement's bare pattern is vacuous under GNU ERE.** Class: counter string vs semantics. Evidence: with `-E`, `\|` is a literal pipe, so the frozen pattern `'62 assertions\|77 assertions'` matches nothing by itself; the 0 is real only because content ground truth shows the single remaining occurrence of either spelling in the three files is the retained historical `corpus/lessons/round-24.md:77` line, which the `grep -v` exclusion drops (s1 datawalk caveat; verified here). Recorded so the control is not misread as proving the numbers are absent everywhere.

**M26-7 · a rename of a source-recheck-owned entry was invisible pre-fix (extra mutant finding).** Class: mutant coverage beyond the claim's letter. Evidence: m1 mutant C2 (renamed `multiparty-vulnerability-coordination.md` → slug-changed) exited 0 on the pre-fix bytes — the `own` limb is satisfied via the `--source` + snapshot pair, not the entry's own file. The landed expected-list equality closes this class as well (unexpected + missing both fire; verified on the landed bytes by the same scratch method).

### Routed defect fixes R25-1..R25-5 and compliance

| Defect | Disposition this round |
|---|---|
| R25-1 · frozen claims file edited after freeze | **Complied**: `claims.json` committed at freeze commit `1b076fa7` before any measurement or dispatch; bytes match the freeze commit (sha `343e568e…`); corrections land as separate appended files, never in-place edits. No correction was needed. |
| R25-2 · selftest tally not in the committed receipt (cross-reference claimed `c1-receipt-index.txt:4`) | **Fixed and measured**: `c1-receipt-index.txt` now carries a `selftest cases=… failures=0` line and an explicit cross-reference correction note (the round-25 index line 4 is `executes=12 gated=0 broken=23`, not a selftest tally). Caveat: the index was written at the pre-change digest (`cases=14`); regeneration at the landed digest (`cases=15`) is required before commit (M26-1). |
| R25-3 · new gate without a registry row | **Fixed and measured**: `SKILL.md` gained `## Gates & probes registry` with one `gate\|probe` row for `recheck-audit.py`: entry command, verdict map (`0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate`), self-test spelling `--selftest`, pinned-value path `.ufo/waves/round-26/c1-receipt-index.txt`, write scope `corpus/` read-only + own receipt dir, owner `kasegi`; plus the expected-list sentence (deletion = red audit). Counter (a) = 1. m2 shows the counter only discriminates the missing `|probe` marker; the other row properties are content-verified, not counter-verified. |
| R25-4 · fix-control fails on its own bytes | **Fixed and measured**: fix-control #3 restated to exclude the retained historical `round-24.md:77` line; `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md \| grep -v 'round-24.md:77' \| wc -l` → **0** (recorded; the only real hit anywhere is the retained line). |
| R25-5 · S040 recheck URL drift | **Fixed and measured**: s2 probe records the live chain — browser UA 403/0 redirects; instrument UA 301 → `tools.cisco.com` → 302 → `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` → 200 (2 hops). Final-page capture is byte-identical to the round-25 snapshot (sha `b7f7b55f…`), so the round-25 capture stays valid; the S040 recheck cell now names the final URL/UA requirement. Note: the note must live OUTSIDE the cadence cell for the census (M26-5). |
| Lane-declared: entry-file deletion shrinks the audited set while passing | **Fixed and measured**: `--expect` expected-list equality (committed `corpus/instruments/knowledge-expected.txt`, 37 entries) makes deleting a whole entry exit 1 naming it (verified: `missing_entries=['corpus/knowledge/multiparty-vulnerability-coordination.md']`, exit 1; extra file → `unexpected` exit 1; absent `--expect` → prior behavior, `expect=absent`). |

## Fixes that can fail

1. **Expected-list gate in `recheck-audit.py` (C1(d); M26-7, lane-declared debt).** Controls: (a) the deletion-mutant control — delete one knowledge entry in a scratch copy and run `python3 corpus/instruments/recheck-audit.py --root <scratch> --cdroot <lane-root>`; it must exit 1 and print/record `missing=<name>` (verified on the landed bytes: `missing_entries=['corpus/knowledge/multiparty-vulnerability-coordination.md']`, exit 1); (b) the extra-file mutant — add an unlisted entry; exit 1 with `unexpected=<name>`; (c) the do-nothing base — unchanged tree exits 0 (37/37); (d) the rename mutant C2 — renaming a source-recheck-owned entry must now exit 1 (missing + unexpected).
2. **Selftest receipt in `c1-receipt-index.txt` (C1(b); R25-2, M26-1).** Control: `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` → 1, AND the index's `instrument_sha256` must equal `sha256sum corpus/instruments/recheck-audit.py` at commit (`3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`; `selftest cases=15 failures=0`) — currently the index pins the pre-change digest/cases=14, so **regenerate the index at the landed digest before commit** (the round's one open C1 item).
3. **Restated fix-control #3 (C1(c); R25-4, M26-6).** Control (run, output recorded): `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l` → **0**. The exclusion is load-bearing: with it removed the same command returns 1 (round-24.md:77, the retained historical sentence). Re-introduction of a 62/77 figure anywhere else in the three files flips this control to ≥1 (verify with proper ERE alternation `'62 assertions|77 assertions'` for the content check); the frozen command's `\|` under `-E` is a literal pipe, so the exclusion pipeline is what makes it meaningful.
4. **Registry row in SKILL.md (C1(a); R25-3).** Control: `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → ≥1; and the row keeps the verdict map, `--selftest` spelling, pinned-value path, write scope and owner (m2: the counter alone only detects a missing `|probe` marker — content review is the rest).
5. **S040/S041 recheck cells vs census (C2 kill rule; R25-5, M26-5).** Control: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 (only pre-existing W04 S028/S029). At compose the census exits 1 with E09 on both cells; smallest safe correction: keep the recheck cells cadence-only (`180d`) and move the final-URL/UA prose into the `## Registry changes` note (the R25-5 record stays in the lane either way).
6. **F11 row entry-cell names vs actual entries (C2 integration; M26-3).** Control: `python3 corpus/instruments/frontier-recheck-count.py` on the live tree → exit 0, `entries=14 pass=14` (F11 contributes 2). At compose it crashes (`FileNotFoundError`) because the row cites staged suffixed names; correct the row's entry cell to the actual filenames (or align the entries to the row) and re-run.
7. **C2 "first registered this round" counter (M26-4).** Control note: the frozen grep is S040-overmatching and shell-tolerant; the round's substantive check is the two entries' Q1–Q9 conformance and their body quotes pinned to the S041 manifest (passing `source-recheck.py --source S041`), plus census exit 0. Do not mistake the awk/grep counts for a quality gate.

## Appendix — counters, confirmation and access-date evidence

Exact frozen counter commands (run from the lane root; all confirmed 2026-10-25 UTC):

```
# C1(a) registry row
grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md                      # 0 -> 1
# C1(b) selftest receipt line
grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt  # 0 -> 1 (regenerate at landed digest)
# C1(c) fix-control #3 (restated, excludes retained historical line)
grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l   # 1 -> 0 (observed 0)
# C1(d) deletion soundness
python3 corpus/instruments/recheck-audit.py --root <scratch-tree-with-one-knowledge-entry-deleted> --cdroot <lane-root>
#   -> exit 1, missing_entries names the deleted entry (before: exit 0, 36/36)
# C2 frontier
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md   # 10 -> 11 (observed 11)
# C2 entries citing a row first registered this round
grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l        # 0 -> >=1 (observed 3: S040 F10 entry + two S041 entries; overmatch caveat M26-4)
# C2 sources census
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi   # exit 0 at round end (currently 1: E09 S040/S041; fix per §Fixes 5)
```

Confirmation rules (house): a round counts only with a resolvable work commit and a before→after measurement (R4); every instrument verdict names its matcher and definition (R3); a number is published with its counting command (R2); corrections land as separate appended files, never in-place edits (R9, R25-1). Kill rules: C1 — any counter misses its after value, or the do-nothing control hits any after value; C2 — a source row appended without an admitted entry citing it, or census exit ≠ 0 at round end.

Access dates: every fetch, probe, receipt and counter run in this round was executed on 2026-10-25 (UTC). S041 capture utc `2026-10-25T12:34:17Z`; S040 live probe `12:34:25Z–12:34:27Z`; C2 do-nothing receipt `12:34:41Z`; m1 mutation batch `12:35:12Z–12:35:24Z`; n1 scope sweep snapshot `12:40Z`; both F11 entries landed between `12:39Z` and `12:43Z` (kit timeline). Claims freeze: `2026-10-25T12:27:41Z` at commit `1b076fa7`.

## Routed debt (named, not hidden)

- The C1(b) receipt index must be regenerated at the landed instrument digest before the round commits (§Fixes 2).
- The sources census must exit 0 at round end: S040/S041 recheck cells → cadence-only, R25-5 prose to the `## Registry changes` note (§Fixes 5).
- The F11 row entry cell must match the actual entry filenames so `frontier-recheck-count.py` stops crashing (§Fixes 6).
- Carried from round 25 (unchanged): `anchorcheck.py` exits 0 for every verdict class and `CITE` lacks the `~/Projects/bounties/` arm; `capture-source.py` `TAG_RE` lossy with no `render`/`raw_sha256` fields; `source-recheck.py --source` single-valued. These are named, not hidden, and remain the r27 planned work.
## Integration closure (2026-10-25)

The four wave-1 open items (recorded in §Fixes 2/5/6 and §Routed debt) were resolved by the L1 integration and are closed below. Earlier blocks are unchanged.

| # | Wave-1 open item | Resolution (measured at integration, 2026-10-25 UTC) |
|---|---|---|
| 1 | C1(b): `c1-receipt-index.txt` pinned pre-change bytes (`instrument_sha256=c3c19adc…`, `selftest cases=14`) | Regenerated at the landed instrument digest `3fc0d751…` (`.ufo/waves/round-26/c1-receipt-index.txt:2-4,13-14`): `instrument_sha256=3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`, `selftest cases=15 failures=0 exit=0`. C1(b) closed. |
| 2 | C2 kill rule: sources census exit 1 on E09 (S040/S041 recheck cells carrying `180d — <prose>`) | S040/S041 recheck cells restored to cadence-only `180d`; the final-URL/UA/fetch-procedure prose moved to `## Registry changes` (SOURCES.md, per census rule E09). Census exits 0 at round close; E09/E11 cleared. C2 kill rule satisfied. |
| 3 | C2 integration: README F11 row cited staged suffixed filenames → `frontier-recheck-count.py` `FileNotFoundError` | F11 entry cell (README.md § Frontier) and the SCORECARD round-26 result row aligned to the actual unsuffixed filenames `knowledge/iso-29147-and-30111-division-of-labour.md`, `knowledge/iso-29147-divergence-and-clause-crosswalk.md`; `frontier-recheck-count.py` exits 0, 14/14 (F11 contributes 2). |
| 4 | Lane-declared/C1(d): `knowledge-expected.txt` stale at 37 entries | Regenerated from the working tree: 39 entries, both new F11 entries included; live audit `expect=present expected=39 missing=0 unexpected=0 exit=0` (`.ufo/waves/round-26/c1-live.json`). |

Final measured counters (integration time, 2026-10-25 UTC):

| Counter | Command / fixture | Value |
|---|---|---|
| C1a | `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` | 1 |
| C1b | `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` | 1 |
| C1c | fix-control #3 restated (BRE alternation, excludes retained `round-24.md:77` line) | 0 |
| C1d | deletion fixture (`--root` scratch tree minus one knowledge entry, `--cdroot` lane root) | exit 1, `missing=<name>` |
| C2 | `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | 11 |
| precise S041-citing | entries whose `source:` row is S041 (`grep -lE '^source: S041 ' corpus/knowledge/*.md \| wc -l`; the frozen S04x grep reads 3 via S040 overmatch, M26-4) | 2 |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0 |
| frontier | `python3 corpus/instruments/frontier-recheck-count.py` (live tree) | 14/14 exit 0 |
| 5 | F11-1 entry re-quoted two F10-B quotes verbatim (hitachi-step1-29147; cisco-iso-29147-2018) — duplication defect vs the round-25 standard (wave 2 AttackC3) | Converted both rows to cross-references to `vendor-disclosure-policy-commitments-crosswalk.md` (the already-admitted verbatim owner); `## Revisions` note appended to the entry; claims/locations unchanged and still checkable. |

Wave-2 falsification (36 attack seats) closed all kill-rule limbs and surfaced the counter blind spots recorded in §Mistakes (C1b presence-only grep; C1c frozen `\|` vacuity under `-E`; C2 S04x overmatch; no reverse-E11). See `.ufo/waves/round-26/wave2/` for per-seat verdicts.
