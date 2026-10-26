# ScoutS016 — S016 decision evidence (Anthropic CVD for Claude-discovered vulnerabilities)

## Verdict
**MINE-ELIGIBLE (reachable, substantive, teaches uncovered ground).** Recommend decide S016 -> mined (not rejected). Confidence high on reachability/content; the "not already held" finding rests on grep of corpus/knowledge + README F01-F22 (observed below).

## (a) Reachable and substantive
- `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://www.anthropic.com/coordinated-vulnerability-disclosure`
- HTTP 200, text/html; charset=utf-8, 164126 raw bytes, final URL unchanged (0 redirects), fetched 2026-10-26T21:15:52Z.
- raw sha256 fa4e70bc2217b566be7dec67fe0bacc2fe32fd81d6308c177410852220eac56d. A second fetch (2026-10-26T21:16:24Z, HTTP 200) gave the identical raw sha256.
- Text extracted with the lane's own `corpus/instruments/capture-source.py html_to_text()`: 32 lines, 4481 bytes, snapshot sha256 91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b. Running `capture-source.py --id S016 --url ... --kind html --out re.txt` independently (utc 2026-10-26T21:16:25Z) printed `S016 status=200 fetched_bytes=164126 snapshot_bytes=4481 sha256=91cc99...957a3b` and `sha256sum re.txt S016.txt` matched, so the capture is reproducible.
- Body text is L5-L17 (title "Coordinated vulnerability disclosure for Claude-discovered vulnerabilities", "Last updated Mar 6, 2026" at L6; matches the registry row's "last updated 2026-03-06"); L1-L4 and L18-L32 are site chrome. First-party Anthropic policy, ~3.2 KB of policy prose.

## (b) Teaches ground not held
Registry row S016 (SOURCES.md:22) is `queued`; no corpus/knowledge file or README F-row cites S016 (`grep -rn S016` over knowledge/ and README.md: no S016 hits; "anthropic" hits in knowledge/ are only the lane's own Anthropic VDP filings/queue notes — intake-surface.md, submitted-registry.md, vdp-disclosure-packages.md — not this policy).
Existing adjacent coverage: F02 (S003 / S004 CERT/CC 45-day / S005 90+14 extension; coordinated-disclosure-timelines.md), F04 (ai-assisted-finding-validation.md, S009-S012: validation of AI findings, no outbound-disclosure policy), F10 (vendor-side policies as corpus objects, S036-S040), F15 (vendor third-party finding coordination, S048). grep for `pacing|provenance|human-reviewed|7-day|45 days` in coordinated-disclosure-timelines.md, ai-assisted-finding-validation.md, vendor-disclosure-policies-as-corpus-objects.md, vendor-disclosure-policy-commitments-crosswalk.md, multiparty-vulnerability-coordination.md returned only the F02 timeline lines (L7/L14/L22/L25 re the 14-day grace extension in S005) — none of the S016 content.
Ground S016 adds (all in the capture): an AI-discoverer's outbound policy — 90-day default or patch-released-first (L10); 14-day extension on request (L11); 7-day target for actively exploited critical vulns plus a further 7-day extension (L12); defer to maintainer severity except credible active exploitation, 30-day non-response escalation to an external coordinator (L14); 45-day wait after patch before full technical details (L16); human-reviewed reports, AI-origin labelling, candidate patches labelled by provenance, no large-volume submission without agreeing a pace, actively exploited exempt from pacing (L17). It fits as an F02/F04 extension (a fourth clock vocabulary: discoverer-side post-patch buffer + AI provenance labelling) or a new F-row on AI-era discoverer disclosure policy; it is not covered by F01-F22.

## (c) Located quotes (<=25 words; each verified `quote in capture_line` by script)
- Q1 (10 words), L17, "Vulnerability Disclosure Reporting and Coordination": "Reports originating from AI-powered discovery are clearly labeled as such."
- Q2 (16 words), L16, "Patch Details": "Once a patch is available, we would generally wait 45 days before publishing full technical details."
- Q3 (15 words), L12: "For actively exploited critical vulnerabilities, we target a 7-day timeline for a patch or mitigation."

## Deliverables (written beside this receipt)
- `ScoutS016.capture.txt` — 32 lines, sha256 91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b (the snapshot text; to be committed as corpus/source-snapshots/round-40/S016.txt).
- `ScoutS016.manifest-record.json` — 48 lines, sha256 64d69742d7497e410eaf2ee47b8a6080e9446681cb365a2d63f7bdc3f41923c3; one `sources[]` entry in the round-39 manifest shape (id, path, url, fetched_utc, status, size_bytes, lines, files, sha256, snapshot_sha256, raw_sha256, raw_bytes, tool, http, quotes[Q1-Q3 with anchor+location]). Note: `path` is `S016.txt`; adjust if the L1 names the snapshot differently. Note the `http.date` field carries the second fetch's Date header (first fetch used no -D).

## Caveats
- Page is a Next.js page with `s-maxage=300`; content can change after this fetch — the pinned sha256 binds this instant.
- SOURCES row not written (ScribeRows owns it). No tools installed; no lane/fleet files modified.

## Cleanup
Scratch /fast/scratch/hyaku/kasegi-r40/ScoutS016 removed on exit (see final check).
