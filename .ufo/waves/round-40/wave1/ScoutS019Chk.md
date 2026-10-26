# ScoutS019Chk — cross-check of ScoutS019's S019 capture (round 40)

Seat: ScoutS019Chk (reviewer, leaf — no subagents). Item: cross-check scout seat ScoutS019's capture for row S019 (NIST SP 800-216, https://csrc.nist.gov/pubs/sp/800/216/final): re-fetch/re-open the captured bytes, verify sha256/status/size, verify the located quote occurs in the capture (grep -c >= 1), assess mined-vs-rejected per QUALITY.md Q1-Q6 and CORPUS.md (corpus/README.md). Verdict: **MINE** (recommendation; the L1 decides).

## Deliverable
- `ScoutS019Chk.txt` — 1 line (plus final newline), 1461 bytes, sha256 `db3796b4368705a117dc095c1ca9ad358722239b53265b967e15d0e49b7be396`.

## Independent verification (all commands run by this seat, 2026-10-26)

1. **Re-fetch of the registry URL** (curl -sS -L --max-time 90 -A kasegi-shokunin/1.0, 2026-10-26T21:17:49Z): `HTTP=200 bytes=44658`. Raw page HTML is NOT byte-stable: three fetches (ScoutS019 21:15:58Z, ScoutS019 21:16:56Z, mine 21:17:49Z) give three distinct raw sha256s (5ad9a3d5…, c0c894bd…, 35e43f5922e6a9fb5a539a6c8e18e776a1722a278b7fdc240785e2e84a4ea639) at equal/near size — per-request tokens. The converted text IS stable (check 2).
2. **Text-sha stability, strongest check**: ran the lane instrument's own `html_to_text()` on MY raw fetch → sha256 `514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6`, 132 lines — byte-identical to the landed `ScoutS019.capture.txt` (4901 B) and to the manifest record's `sha256` pin. A re-fetch + reconvert reproduces the pin, so source-recheck passes on re-runs.
3. **Fresh instrument run** (`capture-source.py --id S019 --url … --kind html --out <scratch>/instr/S019.txt`, 2026-10-26T21:19:49Z) printed exactly: `S019 status=200 fetched_bytes=45019 snapshot_bytes=4901 sha256=514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6` — every manifest-record field (status, fetched_bytes, snapshot_bytes, sha256) reproduces independently; fetched_bytes 45019 (instrument UA `kasegi-shokunin/1.0 (documentation capture; …)`, capture-source.py:32) vs 44658 (curl UA) is UA-dependent raw variance, same text.
4. **Quote check on the landed capture**: `grep -c 'The framework allows for local resolution support while providing federal oversight' ScoutS019.capture.txt` → **2** (>= 1 required); occurrences at L80 and L83 (abstract + "See full abstract" repeat), so the declared anchor 80 disambiguates. Quote is exactly 25 words (`wc -w`). Q1 fragment at L80: `sed -n 80p | grep -c 'recommends guidance for establishing a federal vulnerability disclosure framework'` → 1. Q3 anchor: L97 is exactly `05/24/23: SP 800-216 (Final)`.
5. **Lane gate instrument**: wrapped the landed `ScoutS019.manifest-record.json` as `{"schema_version":1,"sources":[<record>]}` beside a copy of the landed capture and ran `corpus/instruments/source-recheck.py --manifest …` → exit **0**:
   ```
   S019:sha256 OK
   S019:Q1 OK occurrences=2 anchor=80-ok
   S019:Q2 OK occurrences=2 anchor=80-ok
   S019:Q3 OK occurrences=1 anchor=97-ok
   ```
   This is the exact gate C2 requires mined captures to pass ("captures pass source-recheck and bind").
6. **Manifest record completeness**: all seven required fields present (fetched_utc, sha256, lines, files, url, status, size_bytes) plus house-shape extras (id/path/fetched_bytes/snapshot_bytes/normalized/http/quotes) matching the round-39 manifest shape (S057 record). File sha256 `9ef2101816875910b12a4a2e2812b41d33be5745e6ba9d5568d38a5c1a921368`, 43 lines — matches ScoutS019's receipt claim.
7. **PDF probe re-verification**: re-fetched https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216.pdf → HTTP 200, 1510851 bytes, sha256 `363183f02e9366e63a0913080c6576cb4f10f1b635e0a3f12ad7367d8980b67f` — byte-identical to ScoutS019's probe (raw PDF is byte-stable, unlike the page). pdftotext of it: Federal Coordination Body ×6, VDPO ×12, findings report ×4, source vulnerability report ×42; the quoted sentence is in the PDF abstract too (line-wrapped at L108-109 of the default extraction).

## Mined-vs-rejected assessment (QUALITY.md Q1-Q6; CORPUS.md = corpus/README.md)

- **New ground (mined side)**: `grep -rni '800-216|VDPO|Federal Coordination' corpus/knowledge` → zero hits (only BOD 20-01 via S008 and BOD 22-01/26-04 via the KEV entry). The only prior SP 800-216 touch in corpus is the queued S019 row itself and `lessons/round-22.md:95` (the old recheck line quoting the abstract). No frontier row F01-F22 covers a government-run federal coordination framework: F02 = coordinator timelines (CISA/CERT/CC/PZ), F03 = authorization/safe-harbor incl. S008 (CISA's per-agency BOD 20-01 VDP **template**), F06 = FIRST multi-party, F07 = CNA rules, F08 = CRA, F10 = vendor policies. SP 800-216's object is different: the federal operating framework (Federal Coordination Body, per-system VDPOs, source vulnerability reports, findings reports, tracking) — matches the row's own `teaches` cell ("Formalize intake, assessment, tracking and communications…").
- **Rejected side does not hold**: no supersession applies to S019 (unlike S022→S030 CNA rules, S024→S029 CRA clocks), and no held entry/row covers its ground.
- **Q1-Q6 support**: Q1 anchor exists (L80; verified). Q2: S019 is tier A. Q3: verbatim ≤25-word quote with location — verified (occ=2, anchor 80-ok; plus Q1 21-word and Q3 4-word alternates). Q4: attribution is inherent — the abstract is NIST's own statement; an entry must state it as NIST's recommendation, not a universal rule. Q5: falsifiable rule available — "allows for local resolution support while providing federal oversight" is checkable against any federal VDP. Q6: documentation-only public NIST page; no probing/credentials.
- **Caveat (agreed with ScoutS019's own receipt)**: the committed capture is abstract-level (page record: abstract, keywords naming FCB/VDPO/findings report/source vulnerability report, document history). An entry mined from it must keep load-bearing claims to what L80-L97 support; FCB/VDPO process detail requires capturing the PDF text (probe sha byte-stable, verified above) — a later capture, not a blocker for the mined verdict.

## Result
Cross-check **agrees** with ScoutS019: verdict recommendation **mined**. Capture verified (sha256/status/size/quote/anchors), record complete and recheck-clean, ground new. Evidence delivered in `ScoutS019Chk.txt`.

## Tools / environment
- No tool installs. Used preinstalled pdftotext (poppler 26.08.0) and python3 stdlib only. Disk guard green at start (592G free on /fast). No pacman. No git mutations.
- Scratch /fast/scratch/hyaku/kasegi-r40/ScoutS019Chk removed at yield (deliverable + receipt copied to the wave dir first).
