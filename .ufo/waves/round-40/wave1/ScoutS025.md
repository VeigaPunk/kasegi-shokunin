# ScoutS025 — S025 (CVE-Bench, arXiv:2503.17332) decision evidence

## Verdict
(a) Reachable and substantive: **yes**. (b) New ground vs lane holdings: **yes** (see below). (c) Located quote: Q1/Q2 below, both pass `source-recheck.py` (exit 0).
Recommendation to L1: **mine** (not reject). No SOURCES row written (ScribeRows owns it).

## Fetch record (curl -sS -L --max-time 90 -A kasegi-shokunin/1.0)
| item | url | HTTP | bytes | sha256 | UTC |
|---|---|---|---|---|---|
| landing | https://arxiv.org/abs/2503.17332 | 200 text/html | 44575 | 28675fd2808412c1255561965bfc8d409d979f05cea2877db5acc0606146d627 | 2026-10-26T21:16:02Z |
| raw PDF | https://arxiv.org/pdf/2503.17332 | 200 application/pdf | 602933 | 334417c3bbc4fbaa1777df3a98b5c518e9187cac3b21714879116a0260f26cb1 | 2026-10-26T21:16:02Z |
| pinned v4 PDF | https://arxiv.org/pdf/2503.17332v4 | 200 | 602933 | identical to above | 2026-10-26 (shortly after) |

Landing page states: "Submitted on 21 Mar 2025 (v1), last revised 24 Jun 2025 (this version, v4)"; PDF header "arXiv:2503.17332v4 [cs.CR] 24 Jun 2025". Authors Yuxuan Zhu … Daniel Kang (UIUC). PDF Last-Modified Wed, 25 Jun 2025 00:25:34 GMT.

Capture = `corpus/instruments/capture-source.py` `pdf_to_text()` (pdftotext -enc UTF-8 + collapse) of the raw PDF, as for S057: **1490 lines, 71851 bytes, sha256 faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b**. Landing page is metadata only (the abs page carries the abstract but the PDF is the substantive text).

## (a) Substantive
Full 30+ page paper text: sandbox design (§3), 40 critical-CVSS-v3 NVD CVEs published 2024-05-01..2024-06-14, eight "standard attacks" grader, zero-day vs one-day settings, agents Cy-Agent/T-Agent/AutoGPT, results (§4), failure modes and Limitation (§5), Impact Statement.

## (b) Ground not already held
Lane check: `grep -rn S025 corpus/knowledge corpus/README.md` → no hits; the only S025 mentions are SOURCES.md (row S025 queued; chain at L71) and corpus/lessons/round-22.md L101 (a pinned abstract quote, no knowledge entry). `corpus/knowledge/ai-assisted-finding-validation.md` (F04, S009-S012) states only a generic "a benchmark is bounded to its task design" (L34-39, citing S010) — it has no CVE-Bench task design, success-rate numbers, or zero-day/one-day semantics. F01-F22 (CVSS, CVD timelines, safe harbor, CNA rules, CRA, JP/CN regimes, KEV/EPSS/SSVC, CSAF/VEX, Immunefi, MSVR) do not cover agent-exploit benchmarks. Teachable new ground:
- Scope of the benchmark number: 40 web-app CVEs, one date window, only 8 pre-defined attack types graded (paper's own Limitation: "cannot evaluate attacks other than the pre-defined eight standard attacks, potentially leading to false negatives") — exploit-success on a closed set, not finding/triage accuracy.
- Zero-day vs one-day definitions (one-day = NVD-style high-level description supplied); results: up to 10% zero-day, 12.5% one-day (§4 L508-510); Abstract/Conclusion round to 13%; Cy-Agent 2.5% one-day success@5 (L121-123).
- Ethics framing: agents prompted as white-hat hackers "with permissions granted by application owners" (L500-502) — a prompt-asserted authorization, tying to F03.
- Reproducing one exploit took 5-24 person-hours (L105-106 region) — cost of ground-truth validation.
Fits the existing chain S006→…→S012→S025 (SOURCES.md L71).

## Discrepancy to flag for ScribeRows
The registry row/round-22 lesson L101 quote "Our evaluation shows that the state-of-the-art agent framework can resolve up to 13% of vulnerabilities." is **not present** in the v4 text (grep "resolve up to" → none). v4 Abstract says "Our experiments show that the state-of-the-art agent framework can exploit up to 13% of the vulnerabilities." (L31-34). Wording is likely a v1/v2 abstract or a paraphrase [INFERENCE]. Entries must cite v4 wording; the abs page itself is v4 (checked). Also internal inconsistency: Abstract/Conclusion 13% vs §4 12.5% one-day (13% is the rounded 12.5%).

## (c) Located quotes (both source-recheck OK, occurrences=1)
- Q1 anchor L32 (L31-34; Abstract, heading L7), 16 words: "Our experiments show that the state-of-the-art agent framework can exploit up to 13% of the vulnerabilities."
- Q2 anchor L507 (L506-510; §4 "Success Rate." paragraph), 20 words: "LLM agents can exploit up to 10% web application vulnerabilities under the zero-day setting, and 12.5% under the one-day setting."
Source-recheck run (manifest + S025.txt copied to scratch):
```
S025:sha256 OK
S025:Q1 OK normalized=markup-whitespace occurrences=1 anchor=32-ok
S025:Q2 OK normalized=markup-whitespace occurrences=1 anchor=507-ok
exit=0
```
(An earlier draft with Q2 anchor=508 was BROKEN because the quote starts at end of L507; corrected to 507.)

## Deliverables (beside this receipt)
- `ScoutS025.capture.txt` — 1490 lines, 71851 bytes, sha256 faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b (land as corpus/source-snapshots/round-40/S025.txt; sha256 identical to manifest `sha256`/`snapshot_sha256`).
- `ScoutS025.manifest-record.json` — schema_version 1, sources[0] with id S025, path S025.txt, files [S025.txt], url, capture_url, status 200, fetched_utc 2026-10-26T21:16:02Z, fetched_bytes/size_bytes 602933, snapshot_bytes 71851, lines 1490, sha256, snapshot_sha256, raw_sha256, tool/normalized, http, landing_page, quotes Q1-Q2 (shape as source-snapshots/round-39/manifest.json). `purpose` text is a candidate; L1 may merge into the round-40 manifest.

## Other
Cross-check seat ScoutS025Chk asked for the record via IRC; answered with the same facts. Tools installed: none. Disk guard green (/fast/scratch 27%). Scratch /fast/scratch/hyaku/kasegi-r40/ScoutS025 removed after this receipt.
