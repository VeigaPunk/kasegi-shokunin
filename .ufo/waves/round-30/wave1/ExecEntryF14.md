# ExecEntryF14 — round 30 wave 1 (kasegi)

Seat: `ExecEntryF14` (executor, leaf). Assignment: sole writer of `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (Frontier F14). No subagents spawned; no tool installed (none needed; operator tooling rule recorded/na).

## Deliverable

- File: `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`
- Bytes: **7,096 B**, **38 lines**, sha256 **f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32**
- Header: `source: S046 — <URL> — <anchor>`, `source: S047 — <URL> — <anchor>`, `source: S041 — <URL> — <anchor>` (anchors from the actual round-30 captures, lines cited per source), `verified-at: 2026-10-25`, `ground: F14`, one executable `recheck:` chain with a trailing `#` human note (Q10).

## Captures measured (round-30 snapshot dir, sha256)

| artifact | sha256 | note |
|---|---|---|
| `S046.txt` (IPA JVN iPedia activity report, 2021 Q4) | `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3` | CVSSv2/v3 band legends at lines 555–570; applied labels at 111–113 |
| `S047.txt` (IPA JVN iPedia registration report, 2026 Q3) | `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4` | 2-2 distribution at lines 215–240; CWE ranking at 200–214 |
| `S041.txt` (JPCERT/CC 2026 guideline) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` | identical to round-28 pin; 付録4 at lines 1455–1501 |
| `manifest.json` | `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6` | final measured state; see note below |

## Recheck

- Line as landed parses under `bash -n` → exit 0 (Q10: cwd-independent `cd <lane-root> &&`, single chain, `#` note after command).
- Full chain executed from the lane root: `source-recheck.py --source S046 && … S047 && … S041` → exit **0**:
  - S046: sha256 OK; Q1–Q4 all `occurrences=1` (Q3/Q4 normalized=markup-whitespace).
  - S047: sha256 OK; Q1 `occurrences=3 anchor=123-ok`, Q3 `occurrences=2 anchor=130-ok`, Q2/Q4/Q5 `occurrences=1`.
  - S041: sha256 OK; Q1–Q3 `occurrences=1`.
- Source-set equality (harness rule A): header `source:` ids {S046, S047, S041} = recheck `--source` ids {S046, S047, S041}; manifest lists all three; entry body cites all three ids (15 id mentions total).

**Manifest stability observation:** the manifest first observed at 15:51 lacked anchors for S047 Q1/Q3 and failed `occurrence-not-unique` (exit 1). The manifest owner added anchors (123/130) before this report; the digest above is the fixed, measured state with exit 0.

## Q/R mapping (per QUALITY.md)

- **Q1**: opens under H1 with three `source:` lines (S### + URL + exact anchor from capture), `verified-at: 2026-10-25`, executable `recheck:`; present.
- **Q2**: load-bearing claims rest on tier-A rows — S046/S047 (first registered this round, opened 2026-10-25) and S041 (tier A, already registered); no tier-C support.
- **Q3**: every load-bearing claim carries a verbatim quote with exact capture location; percentages copied from S047.txt: `13.6% / 44.2% / 39.6% / 2.5%` (v3, 図2-3) and `44.1% / 44.3% / 11.6%` (v2, 図2-2). All quoted fragments verified uniquely present in captures (raw=1/norm=1) except where the manifest pins them.
- **Q4**: all statements attributed to IPA's own JVN reports (S046/S047) and the IPA/JPCERT/CC partnership guideline (S041); no generalization into a universal rule.
- **Q5**: three falsifiable checks (band-label pairs, quarterly percentages, 付録4 matrix/closure rule) and three rejected over-generalizations with reasons (緊急≠remediation mandate; Q3 shares not a stable distribution; high score alone does not decide handling).
- **Q6**: documentation-only; no probing/scanning/login/submission instruction; no credential, session, or private-URL material.
- **Q7/Q10**: recheck is one command, `bash -n`-parseable, self-prefixed with `cd`, human note after `#`, executes exit 0.
- **Q8**: normalization receipt printed by the instrument (S046 Q3/Q4 normalize=markup-whitespace; all occurrences counted).
- **Q9**: manifest assertions all `occurrences=1` or anchor-verified (S047 123/130); capture stems == ids (S046.txt/S047.txt/S041.txt).
- **R12**: recheck `--source` ids equal the entry's header `source:` ids and are cited in the body; manifest lists them.

## Scope

Only the assigned entry file and this report were written (both inside the lane repo). `SOURCES.md`, `README.md`, manifests, and the frontier F14 row are other seats' scope and were not edited. No writes to fleet root, sibling lanes, shokuknow, or lane git state. No live target contacted; no network fetch performed by this seat.
