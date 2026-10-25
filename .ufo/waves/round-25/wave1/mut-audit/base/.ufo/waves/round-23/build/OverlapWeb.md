# OverlapWeb — local source-recheck vs security corpus

Seat: read-only overlap scan. Axes: `depth:verifiability`, `coverage` (F06–F08).
Base: `922a4dde90b60b465e2b8b241d1fe363f1f27e98` (`claims.json`).
No packages installed. No production edit. No admission.

## Boundary

Kasegi owns the security-corpus recheck. The instrument is local captured text plus sha256 plus quote presence. Kake owns publisher web properties and its live freshness gate. Chousa owns any further official-source capture. Those are three routes, not one shared `S0xx` namespace.

| Surface | Owner | What a clean result means |
|---|---|---|
| `kasegi-shokunin/corpus/instruments/source-recheck.py` | kasegi | Pinned local excerpt bytes and a substring quote. Docstring: captured bytes, not upstream freshness. No HTTP client in the file (full read this scan). |
| `kasegi-shokunin/corpus/source-snapshots/round-23/{S018,S029,S030}.txt` | kasegi | Normalized public-doc excerpts for F06/F08/F07. Round cache `opened-source-snapshots.json` field `kind`: "normalized public-doc reader excerpt; not raw HTTP bytes". |
| `kasegi-shokunin/corpus/SOURCES.md` rows S018, S022, S024, and uncommitted S029/S030 | kasegi | Security-practice registry. S022 stays CNA Rules **v4.1.0**. S024 stays the CRA row whose anchor says Article 14 was not reached. |
| `kake-shokunin/corpus/SOURCES.md` rows S018, S022, S024 | kake | Different documents: DebugBear web vitals (S018, rejected), Google canonicalization troubleshooting (S022), WHATWG `base` element (S024). |
| `kake-shokunin/scripts/freshness-sweep.mjs` | kake | Live host probes. `fetchBody` at line 680 calls `fetch` for `https://veigapunk.github.io/charter-ufo-fsd/`, `https://charter-ufo-fsd.kimi.page/`, and `https://ds4cc.com/sitemap.xml` (pins at lines 72–85). Exit 0 clean / 1 drift / 2 unreadable / 64 usage. |
| Fuller FIRST/CNA/CRA capture, if the pinned excerpt lacks a sentence the registry asserts | chousa, then a new kasegi pin | Source hierarchy and external-target approval. Not a kake crawl. |

`PROVINCE.md` (kasegi) refuses live-target testing and names kake as adjacent web properties. `PROVINCE.md` (kake) owns ds4cc.com, kimi.page/pro mirrors, and Pages deploys. `resolve.py:122` and `density.py:79` already drop `http(s)` tokens. Source-recheck belongs in that local-instrument family.

Site-relative media inside S018.txt line 19 (`/global/sigs/vulnerability-coordination/multiparty/media/figure-1.jpg`) is FIRST document content. It is not a kake property and not a recheck fetch.

## Evidence

Working tree at scan time was dirty on top of the frozen base (sibling writes). Untracked: `corpus/instruments/source-recheck.py`, `corpus/source-snapshots/`, three F06–F08 knowledge files, `corpus/lessons/round-23.md`. Modified: `corpus/SOURCES.md`, `corpus/QUALITY.md`, `SCORECARD.md`. Committed `corpus/README.md` frontier was not in that diff.

Pinned bytes (sha256 matches `opened-source-snapshots.json`):

| File | sha256 | bytes |
|---|---|---|
| `corpus/source-snapshots/round-23/S018.txt` | `d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4` | 8372 |
| `corpus/source-snapshots/round-23/S029.txt` | `82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c` | 19900 |
| `corpus/source-snapshots/round-23/S030.txt` | `673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019` | 26660 |

Instrument observed this scan: `corpus/instruments/source-recheck.py` sha256 `f743942d9643c930453c415414fd4468486140049541e3f7babc935581ae888d`. Stable ids are bare (`S900:sha256`, `S900:Q1` in `--selftest`). `location` is accepted on a quote object and never read (`check_source` uses `quote in source_text` only, lines 127–133). Path confinement is the manifest directory, not the kasegi root and not a lane id.

Named recheck commands, all three knowledge headers line 4:

- F06 `corpus/knowledge/multiparty-vulnerability-coordination.md` → `--source S018`
- F07 `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` → `--source S030`
- F08 `corpus/knowledge/cra-manufacturer-reporting-duties.md` → `--source S029`

Each names `corpus/source-snapshots/round-23/manifest.json`. That path was absent. Command result:

```
manifest UNAVAILABLE reason=missing
exit 2
```

`--selftest` exited 0. Controls: clean 0, corrupt 1, missing source 2, missing manifest 2.

Quote probe against copies of the pinned excerpts (`/tmp/kasegi-r23-overlapweb`, manifest schema_version 1):

| id | quote | stdout | exit |
|---|---|---|---|
| S018 | `Spring 2020` | `S018:version MISMATCH reason=quote-not-found` | 1 |
| S018 | `Guiding Concepts and Best Current Practices` | `S018:heading OK` (file line 21) | (same run) |
| S029 | `within 24 hours` with location text `Article 14(1)(a) only` | `S029:clock OK` | 0 |

`within 24 hours` occurs on both Article 14 tracks (S029.txt lines 10 and 20). Exit 0 did not use the location string. `11 December 2027` is present (line 122). Lesson quote `no later than 14 days after a corrective or mitigating measure is available` is present (line 14). S030.txt line 211 is `4.2.11 CNAs SHOULD assign different CVE IDs to different, Independently Fixable Vulnerabilities.` That lesson quote is in the excerpt. `4.1.9` on line 165 is the excerpt's "Independently Fixable" determination rule. No pinned v4.1.0 file is in `corpus/source-snapshots/round-23/`, so the knowledge sentence that the same guidance "moved from 4.1.10 in 4.1.0" has no local counterpart file.

Homonym probe: a one-line snapshot `INP support in Firefox 114` (kake S018's anchor phrase) with manifest id `S018` exited 0 as `S018:sha256 OK` / `S018:Q1 OK`. Same stable-id shape as the FIRST excerpt.

Registry URL split, committed kasegi rows vs kake rows vs opened snapshot URLs:

- F06: kasegi S018 and the S018 snapshot share `https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1`. Kake S018 is `https://www.debugbear.com/blog/firefox-safari-web-vitals`.
- F07: committed frontier source is kasegi S022 `CNA_Rules_v4.1.0.pdf`. Opened bytes and the uncommitted knowledge `source:` line are S030 `CNA_Rules_v4.2.0.pdf` (header lines 12–16: version 4.2.0, approved 2026-August-20, effective 2026-August-25). Kake S022 is Google Search Central canonicalization troubleshooting.
- F08: committed frontier source is kasegi S024, same EUR-Lex URL, anchor text says Article 14 was not reached. Opened S029.txt begins at `Article 14`. Kake S024 is the WHATWG `base` element.

`corpus/README.md` lines 200–202 still read `queued` for F06, F07, F08, with sources S018, S022, S024. The frozen count command in `SCORECARD.md` (`grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md`) therefore still sees 0. Uncommitted `SCORECARD.md` and `corpus/lessons/round-23.md` line 6 already say C2 `0/3 → 3/3`. Uncommitted lesson lines 41–42 say the FIRST body "explicitly says version 1.1 and Spring 2020". `S018.txt` has zero matches for `1.1` and for `Spring 2020`.

`source-recheck.py` is not present under `kake-shokunin`.

## Falsifiable finding

A bare `S018` clean exit does not identify the security corpus, and the F06 version sentence is not in the pinned excerpt.

1. Re-running the three knowledge `recheck:` commands against the still-missing manifest exits 2 with `manifest UNAVAILABLE reason=missing`. A README frontier status of `admitted` while that command exits 2 has no executable local recheck behind it (C2, Q7).
2. A manifest quote `Spring 2020` or `version 1.1` on `S018.txt` (`d366bf40…`) exits 1 `quote-not-found`. The coordination-role quotes that are in the file can still match. Lesson lines 41–42 are not that oracle.
3. A manifest that reuses id `S018` for the kake DebugBear sentence exits 0 with stable id `S018:…`. Joining that line to F06 is a cross-lane false clean. The same bare-id join maps kake S022/S024 onto F07/F08.
4. `within 24 hours` exits 0 even when `location` claims only Article 14(1)(a), because both tracks contain the phrase and `location` is ignored.

## Contradiction (not a single score)

- Committed frontier: F06–F08 `queued`, sources S018 / S022 / S024, admitted count 0.
- Uncommitted lesson and scorecard: C2 after-state `3/3`.
- Uncommitted knowledge `recheck:` commands: exit 2 until `manifest.json` exists.
- Uncommitted lesson: S018 body contains Spring 2020 and version 1.1. Pinned S018.txt: those strings are absent (probe exit 1).
- C2 forbids substituting secondary authority when official text is absent. The round cache itself labels these files as normalized excerpts, not raw HTTP bytes. Excerpt sha256 OK is support for quotes inside the excerpt. It is not a live first.org / cve.org / eur-lex re-fetch, and it is not kake freshness exit 0.

## Proposed move

One join rule for L1, no kake edit:

Count an F06–F08 local recheck toward coverage only as the tuple `(repo=kasegi-shokunin, manifest under corpus/source-snapshots/, snapshot sha256, quote string observed in that file)`. Stamp the recorded result `lane=kasegi oracle=pinned-excerpt not-network=1`.

- F06 quotes come from `S018.txt` `d366bf40…`. Keep `Guiding Concepts and Best Current Practices` (line 21) and in-file sentences such as line 36. Hold `version 1.1` and `Spring 2020` out of the passing quote set until a later pin contains them.
- F07 bytes are S030 `673526db…`, not committed S022 and not kake S022.
- F08 bytes are S029 `82514478…`, not the S024 "Article 14 not reached" anchor and not kake S024.
- Refuse a join whose only key is bare `S018` / `S022` / `S024`, or whose command is `kake-shokunin/scripts/freshness-sweep.mjs`.

Affected axes: `depth:verifiability` (the clean line says which oracle ran) and `coverage` (F06–F08 numerator cannot be fed by a homonymous kake row, a superseded source id, or a version sentence the excerpt does not contain). Kake's live-host gate stays kake's. Chousa remains the route if someone needs a capture that actually contains the FIRST version sentence.

## Risks

- Requiring `lane=kasegi` inside `source-recheck.py` stdout would change the stable ids `--selftest` already pins (`S900:sha256`, `S900:Q1`). The join rule above can prefix at admission time without that edit. A later instrument edit that rewrites ids has to move the selftest expectation in the same change.
- `manifest.json` may appear after this scan. Exit 2 is then stale; findings 2–4 are not. They depend on the excerpt bytes and on bare ids, not on the manifest's absence.
- Hash OK on a normalized excerpt can be narrated as "official text re-verified". Q7 requires the successful output to name a pinned comparison. Current stdout is `OK` with no oracle token. The join stamp covers that until stdout grows one.
- The v4.1.0 section-move sentence has no pinned v4.1.0 snapshot here. Do not treat it as recheck-proved.
- S028 mined-versus-rejected is outside this scan.

## Verification

From `kasegi-shokunin`, after the manifest exists, a passing F06 command must print a sha256 OK for `d366bf40…` and must exit 1 if the quote list includes `Spring 2020`. A fixture manifest with id `S018` and quote `Firefox 114` must not be recorded as F06. `grep -c 'Spring 2020' corpus/source-snapshots/round-23/S018.txt` is 0 on the hashed bytes above. Re-read kake `corpus/SOURCES.md` lines 26, 30, and 32 before any bare-id join.

## Scope limits

Read-only seat. Did not edit the instrument, registries, frontier table, or kake. Did not run network, freshness-sweep, or a live fetch. Did not audit C1 mirror confinement. Did not admit or reject C2. In-flight sibling files were evidence of wiring, not a landed tree. Probe leftovers: `/tmp/kasegi-r23-overlapweb`.
