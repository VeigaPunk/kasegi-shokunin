# ScoutS019 — S019 NIST SP 800-216 decision evidence (round 40)

Verdict: **MINE** (reachable, substantive, new ground). Not unreachable; no reject-with-flip needed.

## Fetch
- `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://csrc.nist.gov/pubs/sp/800/216/final` at 2026-10-26T21:15:58Z: HTTP 200, text/html; charset=utf-8, 44658 raw bytes, no redirect, raw sha256 5ad9a3d5a99daf1c54ccaa441a9200163946ef6b61d3e786c9b414b29ad9aa10.
- Second curl at 2026-10-26T21:16:56Z (with -D): HTTP/2 200, 44658 bytes, raw sha256 c0c894bd… (raw HTML differs per fetch — page carries per-request tokens), but the converted text sha256 is identical on both curl fetches and on the instrument capture (`514cc379…`): text is stable.
- Committed capture made with the lane instrument `corpus/instruments/capture-source.py --id S019 --url … --kind html` at 2026-10-26T21:16:11Z (its own UA `kasegi-shokunin/1.0 (documentation capture; …)`): `S019 status=200 fetched_bytes=45019 snapshot_bytes=4901 sha256=514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6`. 132 lines. fetched_bytes 45019 (instrument UA) vs 44658 (curl UA) differ in raw bytes only; same text.
- No lane-root `source-snapshots/`; the shape followed is `corpus/source-snapshots/round-36/manifest.json` (S053 record) — fields id/path/url/fetched_utc/fetched_bytes/snapshot_bytes/lines/sha256/normalized/http/quotes, plus the requested aliases `status`, `size_bytes` (=snapshot_bytes 4901) and `files`.

## (a) Reachable and substantive?
Reachable: yes. Substantive: the **committed capture is the CSRC landing/record page only** — title, authors (Schaffer, Mell, Trinh, Van Wyk), the full abstract (L80), keywords (L86: Federal Coordination Body; Vulnerability Disclosure Program Office; findings report; source vulnerability report…), document history (L96 draft 06/07/21, L97 final 05/24/23), topic/law tag Internet of Things Cybersecurity Improvement Act (L102). It carries no timelines or procedure text. The page links the full document (L91 DOI https://doi.org/10.6028/NIST.SP.800-216; PDF https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216.pdf). Probe only (not delivered): PDF fetched 2026-10-26T21:16:22Z, HTTP 200, application/pdf, 1510851 bytes, sha256 363183f02e9366e63a0913080c6576cb4f10f1b635e0a3f12ad7367d8980b67f; pdftotext → 1630 raw lines; instrument-normalized text 81717 B / 1330 lines, sha256 aa7129b324ad9f9c843a9d633e6eecb67f11baebfbcee1b3f97ae03c7e1513bc. It defines the Federal Coordination Body (FCB) and Vulnerability Disclosure Program Offices (VDPOs) (raw lines 314-317, 389-445), lists "Disclosure plans (specifically, embargo and publication timelines)" (487), says to leverage CVSS with environmental factors (680, 877), and states no fixed day counts (grep for "N days" found none). If L1 wants depth beyond the abstract, a second capture of the PDF as a separate row/capture is possible; the landing page alone supports only abstract-level claims (what it recommends, scope, dates, authors).

## (b) Ground not already held?
Checked corpus/README.md F01–F22 rows and `grep -rli "800-216|VDPO|Federal Coordination Body|20-01" corpus`:
- Only prior hits for SP 800-216 are the S019 SOURCES queued row and `lessons/round-22.md:95` (the old S019 recheck line citing the abstract); no `knowledge/` file cites it. No VDPO/FCB occurrence anywhere in corpus/knowledge.
- Nearest held ground: BOD 20-01 agency VDP template (S008; `knowledge/authorization-safe-harbor-and-scope.md:38`, S003 note L106). That is the per-agency *policy* template (F03). SP 800-216 is the federal *operating framework* — a coordinating body, per-system lowest-level program offices, source-vulnerability-report intake, findings reports, advisories — which F02/F06 (coordinator timelines, FIRST multi-party CVD), F03, F07, F08 do not cover. No frontier F-row covers a government-run coordination architecture.
- Fits the "formalize intake, assess, track, communicate" teaching already in the S019 SOURCES row, and is tag-adjacent to F06 (multi-party roles) — enough to be a new frontier/knowledge theme or an appended cross-reference, not a duplicate.
Caution for the entry: the capture supports abstract-level facts only; FCB/VDPO detail needs the PDF capture.

## (c) Located quotes (all ≤25 words; source-recheck.py on the record: rc=0)
```
S019:sha256 OK
S019:Q1 OK occurrences=2 anchor=80-ok
S019:Q2 OK occurrences=2 anchor=80-ok
S019:Q3 OK occurrences=1 anchor=97-ok
```
- Q1 (21 words, L80, recurs L83 so anchor 80): "recommends guidance for establishing a federal vulnerability disclosure framework, properly handling vulnerability reports, and communicating the mitigation and/or remediation of vulnerabilities."
- Q2 (25 words, L80/L83): "The framework allows for local resolution support while providing federal oversight and should be applied to all software, hardware, and digital services under federal control."
- Q3 (4 words, L97, unique): "05/24/23: SP 800-216 (Final)"

## Deliverables (beside this receipt)
- `ScoutS019.capture.txt` — 132 lines, 4901 B, sha256 514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6 (byte-equal to instrument output; lands as corpus/source-snapshots/round-40/S019.txt).
- `ScoutS019.manifest-record.json` — 43 lines, sha256 9ef2101816875910b12a4a2e2812b41d33be5745e6ba9d5568d38a5c1a921368; one record object (id S019, path S019.txt); drop it into a `sources[]` array of the round-40 manifest.json.

## Tools / scratch
No installs. pdftotext already present. Scratch /fast/scratch/hyaku/kasegi-r40/ScoutS019 removed at yield. Disk guard green at start. SOURCES row not written (ScribeRows owns it).
