# ScoutS023 — round 40, source row S023 (CISA CVD Program page)

## Decision input: MINE-worthy (reachable, substantive, new ground)

**Fetch** (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, run twice):
- URL https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program
- HTTP status 200, no redirect (effective URL = requested), `text/html; charset=utf-8`
- Fetch 1 at 2026-10-26T21:15:55Z: 75,587 bytes, raw sha256 `383792fd393700210e2a6b8ac38f12c8bc249b85eb60bbbe1976667bab5ca6da`
- Fetch 2 at 2026-10-26T21:16:16Z: raw sha256 identical (served bytes deterministic across the two fetches)
- Capture via `corpus/instruments/capture-source.py --id S023 --url <above> --kind html` (instrument output: `S023 status=200 fetched_bytes=75587 snapshot_bytes=14357 sha256=52a6671f…6087 utc=2026-10-26T21:16:01Z`). Capture-time UTC 2026-10-26T21:16:01Z.
- Capture: 213 lines, 14,357 bytes, sha256 `52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087` (wave file ScoutS023.capture.txt, byte-identical to instrument output; `wc -l`=213, `wc -c`=14357).
- Manifest record sha256 `e413ac5748d1a4b39420a3587c2cf2efaa7dd54c0f376f206fb75141181a26e5` (ScoutS023.manifest-record.json; fields fetched_utc, sha256, lines, files, url, status, size_bytes plus the round-39 manifest's extra keys: capture_url, fetched_bytes, snapshot_bytes, snapshot_sha256, raw_sha256, raw_bytes, tool, normalized, http, quotes; `json.tool` parses it).

**(a) Reachable and substantive?** Yes. Body text is lines ~72-182 of the capture (L1-L71 and L183-L213 are site navigation/footer chrome, which the capture keeps because html_to_text does not strip it). Substantive sections: Submit a Vulnerability (L88-89, VINCE-NT), About CVD overview (L104-112), Program Impact (L113), Authorities (L114, 6 U.S.C. 659(c)(12), 650(25), 659(n)), The CVD Process steps 1-7 (L115-146), Public Disclosure and Disclosure Timeline (L147-152), CVD vs the Vulnerability Equities Process (L153), CISA VDP vs CVD (L154-156), Resources (L157-173). The page carries no visible publication date (matches the registry row "no visible publication date"). The registry row's "steps 1-7" claim holds: L116 step 1 Report Submission; L117 step 2 Intake and Triage; L128 step 3 Coordination; L134 step 4 CVE Record Determination; L136 step 5 Advisory Development; L141 step 6 Public Disclosure; L146 step 7 KEV Evaluation and Publication.

**(b) New ground?** Yes, checked against corpus/knowledge and corpus/SOURCES.md:
- `knowledge/coordinated-disclosure-timelines.md` (F02) cites S003 (CISA supplier guide), S004 (CERT/CC 45 days after initial report), S005 (Project Zero). It holds no statement of CISA's OWN program-page rule. Grep for `VINCE|Last Resort|Top.Level Root|VEP|Equities` across corpus/knowledge returns no hit for VINCE, CNA of Last Resort, Top Level Root or Vulnerability Equities Process (only unrelated filenames/other strings); `45 days` appears in the timelines entry only as CERT/CC's S004 policy (L22 there).
- `knowledge/cna-assignment-and-vulnerability-rules.md` (F07, S031) holds CNA assignment rules, not CISA's Top-Level-Root/CNA-of-Last-Resort role (L112) or its step 4 "determines ... which CNA is responsible" (L134).
- `knowledge/multiparty-vulnerability-coordination.md` (F06, S018) holds FIRST roles, not CISA's Mediation-between-reporter-and-vendor stage (L132).
- `knowledge/cisa-kev-catalog.md` (S052) holds the KEV feed; S023 adds that KEV evaluation is step 7 of the CVD process (L146) and that disclosure publishes CSAF (L144). Not duplicated.
- `knowledge/vdp-disclosure-packages.md` and vendor-policy entries: none state the CVD-vs-VDP separation (L154-155).
- Frontier rows F01-F22 (README) cover the listed regimes; none maps to a CISA-as-coordinator program page. S023 would fall under F02/F06/F07 (timelines, multi-party, CNA) as a source for a new entry, or could pair with S030 for a CISA-coordinator entry. Distinct unheld claims the page makes: (1) 45-day earliest disclosure for an unresponsive vendor regardless of patch (L151); (2) disclosure timeline depends on four factors (L148-152); (3) vulnerabilities reported via CVD are not subject to VEP adjudication per VEP Charter 5.4 (L153); (4) CVD != VDP (L154-155); (5) seven-stage separation of intake, triage, coordination, CVE determination, advisory prep, disclosure, KEV (L115-146) — the registry row's stated lesson.
- Caveats for the entry author: the page says "no subject to VEP" (L153, source typo) and "Lean more about VEP" (typo); quote exactly or avoid those words. The page has `Opens in a new window` and nav chrome lines; quote only from L72-182. L151 quote ends before ", regardless of the availability of a patch or update." — do not drop that tail when stating the rule.

**(c) Located quotes** (both verified as substrings of the stated capture line by script):
- Q1, L151, 19 words, under bullet "Vendor Responsiveness." in Disclosure Timeline: "CISA may disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made"
- Q2, L154, 9 words, section "CISA Vulnerability Disclosure Process (VDP)": "The Vulnerability Disclosure Process (VDP) is separate from CVD."

**Verdict for the L1:** S023 is reachable (200), substantive, and teaches unheld ground; mine it (no reject-with-flip needed). Capture would pass source-recheck by construction (same instrument, deterministic raw bytes across two fetches); manifest record ready for binding under round-40.
Scope-wise: ScribeRows owns the SOURCES row; I did not touch it. Tools installed: none. Scratch /fast/scratch/hyaku/kasegi-r40/ScoutS023 removed before yield.

## Deliverables
- ScoutS023.capture.txt: 213 lines, 14,357 bytes, sha256 52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087
- ScoutS023.manifest-record.json: sha256 e413ac5748d1a4b39420a3587c2cf2efaa7dd54c0f376f206fb75141181a26e5
