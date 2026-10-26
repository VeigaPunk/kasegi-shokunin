# ScoutS023Chk — round 40, cross-check of ScoutS023's S023 capture (CISA CVD Program page)

Verdict recommendation delivered in `ScoutS023Chk.txt` (1 line, sha256 `534285e46d5444c37bbfedb3ca6ea9bee06b139ddeaa75dce53e0d9e34b64222`): **mined**. This receipt holds the verification evidence; nothing here is part of the landed bytes.

## What was cross-checked

ScoutS023.capture.txt (213 lines, 14,357 bytes) + ScoutS023.manifest-record.json in `.ufo/waves/round-40/wave1/`, against an independent re-fetch and an instrument re-derivation run by this seat.

## Verification commands and actual output

1. Independent re-fetch (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, 2026-10-26T21:18:22Z):
   `http_code=200`, `75587 S023-refetch.html`, sha256 `383792fd393700210e2a6b8ac38f12c8bc249b85eb60bbbe1976667bab5ca6da`.
   → Identical to ScoutS023's two fetches (21:15:55Z, 21:16:16Z per its receipt) and to the manifest record's `raw_sha256`/`raw_bytes` (75587). Raw bytes deterministic across 3 fetches ~3 min apart.
2. Re-derivation with the lane's own instrument (`python3 corpus/instruments/capture-source.py --id S023 --url <S023 url> --out <scratch>/S023-rederive.txt --kind html`, 21:18:58Z):
   `S023 status=200 fetched_bytes=75587 snapshot_bytes=14357 sha256=52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087 utc=2026-10-26T21:18:58Z`, exit=0; re-derived file sha256 `52a6671f…6087`.
   → Byte-identical to ScoutS023.capture.txt; matches manifest `sha256`/`size_bytes`(14357)/`lines`(213)/`status`(200).
3. Manifest record: `sha256sum` = `e413ac5748d1a4b39420a3587c2cf2efaa7dd54c0f376f206fb75141181a26e5` (matches ScoutS023's receipt claim); parses as JSON; required fields `fetched_utc, sha256, lines, files, url, status, size_bytes` all present with the values above; shape carries the round-39 manifest's extra keys (`capture_url`, `snapshot_*`, `raw_*`, `tool`, `normalized`, `http`, `quotes`).
4. Quotes in capture (grep -c, both = 1):
   - Q1, L151 (19 words, ≤25): "CISA may disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made" — full line is the 'Vendor Responsiveness.' bullet and continues ", regardless of the availability of a patch or update." as the manifest note says.
   - Q2, L154 (9 words): "The Vulnerability Disclosure Process (VDP) is separate from CVD." — under section 'CISA Vulnerability Disclosure Process (VDP)'.
5. Capture is the right page: L1 = "The Coordinated Vulnerability Disclosure (CVD) Program | CISA"; body L104-156 read in full this seat: Overview with CISA Top-Level-Root / CNA-of-Last-Resort (L112), Authorities with 6 U.S.C. 659(c)(12)/650(25)/659(n) (L114), CVD Process steps 1-7 (L115-146, step 7 = KEV evaluation; step 6 publishes CSAF), Disclosure Timeline four factors (L147-152), VEP carve-out per VEP Charter 5.4 (L153), CVD-vs-VDP separation (L154-156). Substantive, not chrome.

## New-ground assessment (independent greps, this seat)

Over `corpus/knowledge/`: `VINCE` hits only as a substring of "PROVINCE" (source-tree-loss, considerthese ledgers); `last resort` 0; `Top Level Root`/`top-level root` 0 (only unrelated "top-level dirs" filesystem text); word-boundary `VEP` 0; `equities` 0; `separate from CVD|VDP is about` 0. `45 days` in `coordinated-disclosure-timelines.md` only at L22 as CERT/CC's S004 policy — CISA's own program-page floor is unheld. Whole-corpus check: `CNA of Last Resort|Top Level Root` appears only in `corpus/source-snapshots/round-24/S013.txt:118,121` (MITRE's roles on the CVE Program page) — no knowledge entry holds CISA's operationalization of those roles, so the L112 claim is attribution-distinct new ground (Q4 discipline applies).

Unheld claims the capture supports: (1) CISA's own 45-day earliest-disclosure floor for an unresponsive vendor regardless of patch (L151); (2) four disclosure-timeline factors (L148-152); (3) CVD-reported vulnerabilities not subject to VEP adjudication per VEP Charter 5.4 (L153); (4) CVD ≠ VDP (L154-155); (5) the 7-stage intake→triage→coordination→CVE-determination→advisory→disclosure→KEV process (L115-146) — the registry row's stated lesson.

QUALITY.md fit: Q3 quotes located and ≤25 words; Q4 the rules are CISA's own program statements (attribute, don't generalize — CERT/CC's 45-day trigger differs, F02 L12 per S041 note); Q5 the 45-day floor is a falsifiable rule; Q6 documentation-only. CORPUS.md: `mined` = cited by ≥1 path in `used-by`; tier A / kind docs fits.

## Attack findings (none fatal)

- c2-controls/junk-decisions.md line 18 fabricates `S023 | rejected | no time | none` — that file is the declared do-nothing control ("must be rejected by the frozen counter"), not a decision; the real C2 plan names only S022/S024 as rejections, so S023 mined is consistent with the claim.
- Source typos an entry author must respect: "no subject to VEP adjudication" and "Lean more about VEP" (L153) — quote exactly or avoid; ScoutS023 flagged both.
- Manifest `http.user_agent` says `kasegi-shokunin/1.0` while the instrument's UA constant appends a contact suffix; server does not vary on UA (raw bytes identical across both UAs), so no impact.
- No defect found in the capture, the manifest record, or the located quotes; agreement is independent (separate fetches, separate greps, instrument re-run).

## Housekeeping

- Tools installed: none. No mutating git/jj command run; reads only outside wave1.
- Scratch `/fast/scratch/hyaku/kasegi-r40/ScoutS023Chk/` (S023-refetch.html, S023-rederive.txt) removed before yield.
- Deliverable: `.ufo/waves/round-40/wave1/ScoutS023Chk.txt` — 1 line, 2484 bytes, sha256 `534285e46d5444c37bbfedb3ca6ea9bee06b139ddeaa75dce53e0d9e34b64222`.
