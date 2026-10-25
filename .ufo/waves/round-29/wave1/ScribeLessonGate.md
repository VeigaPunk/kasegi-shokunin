# Round-29 Gate — draft for the lesson (seat: ScribeLessonGate)

Drafted by `ScribeLessonGate` for `ScribeLesson` to assemble into
`corpus/lessons/round-29.md` (the L1 finalizes after close). All measurements
below were made by this seat on 2026-10-25 (~18:16–18:22Z) from committed or
live bytes; nothing is projected. Where a value depends on a seat that had not
landed at draft time, it is labelled UNVERIFIED with the named re-run.

Answering model: N/A — this item is read-only measurement and report drafting;
no model-route decision was involved.

## 1. Assimilation set

**Package (read-only):** `/home/vgpnk/Projects/shokuknow/merge/kasegi/`.
Bytes read this round: `MERGE-REPORT.md`; `SOURCES.append.md` (all 94 staged
rows, S031–S124); staged entries
`knowledge/corpus/knowledge/program-severity-ladders-and-reward-scales.md`,
`program-scope-rules-and-asset-boundaries.md`,
`claim-packaging-and-report-quality.md`. Register read (read-only):
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.

**Staged rows inspected:** 94 numeric ids (S031–S124). By-URL join of staged
vs lane registry (98 distinct staged URLs vs 43 lane URLs) found 14 staged
rows whose URL already exists in the lane: S055→S036, S056→S037, S031→S043,
S039→S033, S123→S032, S057→S038, S032→S044, S033→S045, S068→S040,
S060→S039, S042→S042, S043/S064/S076→S041, S041→S035, S040→S034. Only
S031/S032/S033 are adopted this round.

**By-document id map (adopted):**

| Staged id | Staged URL | Lane id | Why |
|---|---|---|---|
| S031 | `https://hackerone.com/security/policy_versions` | **S043** | URL absent from lane pre-append (`grep -cF` → 0); S043 free (`grep -cE '^ {0,3}\| *S043 *\|'` → 0 pre-append) |
| S032 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | **S044** | same, both checks → 0 |
| S033 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | **S045** | same, both checks → 0 |

Adopted ids continue the lane registry from S042 (registry 42 rows pre-append
→ 45 post-append, measured at ScribeSourcesGate's append).

**Collision list:** 12 numeric collisions, S031–S042 (staged S031–S042 vs
lane S031–S042) — `assimilation/collisions` (12 lines) and re-derived by this
seat with the 0–3-space-tolerant pattern. **Guard proof** (scratch fixture in
`/tmp/r29gate`): a registry fixture with an indented `  | S002 |` row
collides with staged S002 under the tolerant pattern (1 hit), while the naive
`^\|` pattern misses it (0 hits) — no colliding row can be appended silently.

**Quarantine slice — 7 rows, hand-checked this round** (fetch at
2026-10-25, instrument UA `kasegi-shokunin/1.0`; normalization Q8:
tags stripped, whitespace collapsed; PDFs via `pdftotext -enc UTF-8`).
Verdicts vs the round-28 measured verdicts; **flips: none**:

| Staged row | Register class | Fresh fetch | Measured verdict (2026-10-25) | Reason | Flip condition |
|---|---|---|---|---|---|
| S037 | `payload-absent` | 200 / 24,189 B | **fetched no-quote** | register quote `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01` → 0×; `发布日期` 1×, `GB/T 30279-2020` 2× | cell-anchored fragment quotes after a capture |
| S054 | `payload-absent` | 200 / 513,648 B PDF | **fetched no-quote** | pdftotext text 8,785 B: register quote `脆弱性の悪用が確認されたもの又は疑われるもの` → 0×; `府連第7号` 0× (glyph-spaced header); `独立行政法人情報処理推進機構` 1× | longer fragment or spacing-normalized capture |
| S048 | `the cited source could not be fetched, so no quote was checked` | **404 / 748 B** | **unfetchable** | `gbDetailed?id=3B865A…` still 404 | R8 `supersedes` row naming a live id |
| S065 | `the cited source could not be fetched, so no quote was checked` | 200 / 7,465,472 B PDF | **fetched quote-located** | `现行有效法律目录` 1×, `刑法（7 件）` 1× | not adopted: no admitted entry cites it |
| S068 | `the cited source could not be fetched, so no quote was checked` | 301→tools.cisco.com→302→sec.cloudapps.cisco.com, final 200 / 94,027 B | **already-mined-by-document** | URL byte-equal to lane S040; `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018` 1× | none (document already registered) |
| S069 | `the cited source could not be fetched, so no quote was checked` | 302 → kass.sacinfo.org.cn, exit 60 (TLS) | **unfetchable** | curl `(60)` certificate failure | certificate-verifying fetch or reachable mirror |
| S070 | `the cited source could not be fetched, so no quote was checked` | 302 → kass.sacinfo.org.cn, exit 60 (TLS) | **unfetchable** | same | same |

None adopted. Reachability is reported, not upgraded into adoption.

**Admits.** Three new registry rows and the F13 entry:

| Row | URL | Access date | Tier/status | Inline located quote (≤25 words) |
|---|---|---|---|---|
| S043 | `https://hackerone.com/security/policy_versions` | 2026-10-25 | A / mined / 90d | "Issues affecting assets under HackerOne's control are in scope." (12 words; record 3787452, new_policy, Program Scope and Assets/In Scope; occurs 12× across the 153-record array — see §Unverified). Record metadata verified: `id` 3787452 1×, `timestamp` `2026-10-16T15:34:59.854Z` (staged anchor claim) |
| S044 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | 2026-10-25 | A / mined / 90d | "P1 (Critical) to P5 (Informational)" (5 words, README Data within an Entry/Priority) and "application complexity, bounty brief restrictions or unusual impact could result in a different rating." (14 words; each occurs 1× in the capture) |
| S045 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | 2026-10-25 | A / mined / 90d | JSON fragment `"id": "idor", "cwe": ["CWE-932"]` (path `$.content[4].children[2]`, occurs 1×); dataset facts: 36 top-level entries, `metadata.default` null |

Captures (sha256): S043.txt `02ecb500…dfc6` (1,220,741 B, single-line JSON,
153 records, byte-identical to live probe); S044.txt `8adfca61…26bf`
(8,187 B); S045.txt `f583a396…0f86` (14,575 B, JSON-equivalent to the live
28,482 B pretty-printed `cwe.json`).

**F13 entry status at final re-open (not an unconditional admission).** The target `corpus/knowledge/program-severity-ladders-and-reward-scales.md` is now present as a substantive 7,583-byte entry (after the earlier 631-byte stub). It cites S043/S044/S045, includes bounded HackerOne/Bugcrowd claims, falsifiable checks and rejected over-generalizations, and uses the lane F13 ground. However, the frozen C2 kill rule requires every manifest assertion to be `occurrences=1`; current `source-recheck.py` reports S043 Q1/Q2/Q4 each `occurrences=12` (with `anchor=1-ok`) while S044/S045 quotes are each exactly once. Therefore **the entry cannot be counted as a passed C2 admission under the frozen claim**, even though its Q9 anchors are accepted by the instrument. The source rows exist; the C2 claim remains not verified until S043 quotes are made exactly-once (or the frozen requirement is otherwise met without editing claims.json) and the entry is reviewed on the final bytes.

The staged package entry is not adopted as written: its CNVD 众测 and BILISRC/360SRC claims rely on staged S034/S035/S036, not the three C2 documents. The landed entry narrows to HackerOne S043, VRT README S044, and CWE map S045; its own `## Limits` records that exclusion. This addresses CritC2Kill's C5 concern that source headers must bind the body rather than remap IDs while carrying unrelated prose.

**Rejects (with flip conditions).** Each refusal below was re-opened this
round with measured evidence:

| Candidate (package path) | Failing gate | Reason (measured) | Flip condition |
|---|---|---|---|
| `knowledge/corpus/knowledge/program-scope-rules-and-asset-boundaries.md` | Q2, Q3, Q7/Q10, ground | adopted S043 (HackerOne) is registered, but the entry's platform-branch claims cite staged S034 (CNVD 众测) and S035 (360SRC) — neither a lane row (lane = S001–S045; `grep -cE '^\| *S04[4-6] *\|'` → 2 = S044/S045 only, S046 absent); no located quote for those claims; `recheck:` is the package's prose form; ground `F09`/`F03` is the package F-space, not a lane frontier topic | register S034+S035 as lane rows with captures + exactly-once quotes; add a named lane frontier row |
| `knowledge/corpus/knowledge/claim-packaging-and-report-quality.md` | Q2, Q3, Q7/Q10, ground | sources S034/S035/S036 all staged, none registered; ground `F11` is package F-space (lane F11 = ISO 29147/30111 division-of-labour). Measured opening: S034 200/56,674 B, S035 200/427,391 B, S036 (BILISRC PDF) 200/439,149 B — all reachable; `pdftotext` shows `三、安全漏洞评分标准` 1×, `1.7` 1×, 严重 16× / 中危 5× / 低危 6× / 忽略 13× — so the block is refusal-by-registration, not unavailability | register S034–S036 with captures + located quotes; re-ground claims |
| `knowledge/corpus/knowledge/chinese-criminal-thresholds-and-authorisation.md` (standing, re-confirmed) | Q2, Q3, Q4, Q5, Q7/Q10, ground | staged S044/S045/S046 are not lane rows (URL join: S044/S045/S046 URLs absent from lane); Q4 generalizes three instruments into a jurisdiction-wide rule; no located quote; prose recheck | register S044/S045/S046 with captures; attribute per instrument |
| `knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` (standing, re-confirmed) | ground, Q2, Q3, Q7/Q10 | `ground: F20` names no lane frontier row (`grep -cE '\| F20 ' corpus/README.md` → 0); sole source staged S080 not a lane row; quote restated with no location; prose recheck | register MSRC page; capture; locate an exactly-once quote; add a lane frontier row |

No Q/R bar was relaxed. None of the refused files exists in the lane
(`test -e corpus/knowledge/<name>` → absent for all four).

## 2. Registry changes old→new (every touched cell)

- **S043 row added** (SOURCES.md): tier A, status `mined`, `opened
  2026-10-23 → 2026-10-25`, `recheck 90d` (new), `anchor` rewritten from the
  round-29 capture (policy_versions API array, 153 records; record id 3787452,
  timestamp 2026-10-16T15:34:59.854Z; Program Scope and Assets and DoS Reward
  sections located in new_policy; manifest quotes Q1–Q4) — staged prose anchor
  not carried; `used-by` = `corpus/knowledge/program-severity-ladders-and-reward-scales.md`.
- **S044 row added**: tier A, `mined`, `opened 2026-10-23 → 2026-10-25`,
  `recheck 90d`, `anchor` from capture (Description, Data within an Entry,
  Priority), `used-by` = the F13 entry.
- **S045 row added**: tier A, `mined`, `opened 2026-10-23 → 2026-10-25`,
  `recheck 90d`, `anchor` from capture (metadata.default; broken_access_control;
  idor; CWE-932), `used-by` = the F13 entry.
- **S041/S042**: no cell old→new this round (both untouched). No row
  superseded, retired, or re-titled. The `## Registry changes` log in
  SOURCES.md carries the three additions verbatim.

## 3. New rows — URL, access date, located quote

As tabulated above; each new row was opened 2026-10-25; quotes are verbatim
from the captures with normalization `markup-whitespace`.

## What I could not verify (named)

- **Historical capture-state note (18:16–18:22Z):** the first draft recorded the F13 entry as a 631-byte stub and the F13 row as not yet visible. Those observations were true at that time and are superseded by the current state below.
- **Current manifest limitation:** the landed round-29 manifest has three S043 assertions (`Q1`, `Q2`, `Q4`) at `occurrences=12`, each with `anchor=1-ok`; `Q3` occurs once. The anchors satisfy source-recheck's anchored-alternative behavior, but the frozen C2 kill rule explicitly requires `occurrences=1` for every assertion. Thus the C2 predicate fails even though each `source-recheck.py` invocation exits 0. Flip: replace repeated S043 assertions with unique exact quotes and/or captured record-specific evidence that yields exact-once assertions, then rerun the frozen C2 command set; do not edit `claims.json`.
- **Final F13 row/entry arrived after the original draft:** current frontier admitted count is 13; the entry is 7,583 B and the harness/census now pass (measurements below).
- **Reviewer timing matters:** `RevC2Entry` reviewed the earlier stub, not the present 7,583-byte body. Its disagreement is valid for that reviewed snapshot only; no final-byte reviewer verdict is available here.
- **Reject-review gap:** `RevStagedIntent` is a revenger, not a reviewer-role seat. Its source re-open supports rejecting the specific automatic-integration inference, but the available receipts do not provide a reviewer-role re-open of a refused candidate. This remains an unfulfilled spot-check requirement; the assembler must report it as a gap unless a later reviewer receipt lands.
## Final-state correction and spot-check (2026-10-25)

The previous paragraphs contain measurements captured during wave assembly; this section supersedes any earlier claim that F13 was already admitted or that its C2 predicate passed.

| Surface | Final observation at this re-open |
|---|---|
| Frozen C2 target | `corpus/knowledge/program-severity-ladders-and-reward-scales.md` now exists (7,583 B); source headers S043/S044/S045, F13 ground, executable chained `source-recheck.py` line. |
| Frontier / rows | `corpus/README.md` admitted count **13**; new lane rows **3** (S043–S045); exactly one entry matches `^source: S04[3-5]`. |
| Manifest | Round-29 `source-recheck.py` exit 0 for S043/S044/S045; S043 Q1/Q2/Q4 each `occurrences=12 anchor=1-ok`, Q3 once; S044/S045 assertions once. Exit 0 does not satisfy frozen C2's stricter `occurrences=1` kill-rule limb. |
| Independent entry review | Reviewer `RevC2Entry` re-opened the earlier 631-byte stub at its review timestamp and explicitly **disagreed with admission** (Q1–Q5/Q7–Q10 failed or unverifiable; body was `body stub S043 S044 S045`). The current substantive 7,583-byte entry landed after that review; the reviewer verdict is not upgraded to a pass for the later bytes. A fresh final-byte review remains required. |
| Independent reject review | `RevStagedIntent` (role `revenger`, not reviewer) re-opened the staged F13 claims against S044/S045 captures: agreed the VRT's P1–P5 is Bugcrowd's suggested baseline and the CWE JSON proves a mapping, but found that the dataset does not establish automatic program integration (`RevStagedIntent.md` §§15–25). This supports rejecting the staged over-generalization “a program maps its own priority ladder onto CWE automatically”; flip by limiting the statement to Bugcrowd's published taxonomy-to-CWE crosswalk. This does **not** satisfy the requested reviewer-role re-open of a rejected candidate; no such receipt is present in the available artifacts. |

**Spot-check row for the lesson assembler:** ADMIT candidate — non-author reviewer `RevC2Entry` disagreed with the stub it inspected; current substantive bytes landed afterward and still require fresh reviewer review. REJECT subclaim — independent `RevStagedIntent` re-opened staged S033's CWE evidence and disagreed with the “automatic program integration” inference; agree with rejecting that inference. The latter seat's role is `revenger`, not `reviewer`, so no reviewer-role check of a refused package candidate is evidenced; do not report this criterion as fully satisfied.

### Current verdict and exact rerun

**C2 F13: NOT VERIFIED at this observation.** The three registry rows and F13 frontier row exist, and the entry body now exists, but S043's three repeated manifest assertions violate the frozen exact-once counter requirement, and the available RevC2Entry review predates the current entry bytes. Do not report an unconditional admit or a passing C2 predicate.

Rerun after S043 manifest assertions are corrected and a reviewer reopens the final entry:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S044
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S045
python3 corpus/instruments/frontier-recheck-count.py
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```
Acceptance must include S043 assertions `occurrences=1`, a reviewer-role final-entry verdict, `entries=16 pass=16 exit=0`, and census exit 0; a mere `source-recheck` exit 0 is insufficient.
