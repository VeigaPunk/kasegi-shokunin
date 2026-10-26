# ScoutS021Chk receipt — round 40, cross-check of ScoutS021's S021 capture (CISA BOD 20-01)

Seat: ScoutS021Chk (leaf, no subagents). Item: re-fetch/re-open ScoutS021's captured bytes for row S021, verify sha256/status/size, verify the located quote occurs in the capture (grep -c >= 1), and assess `mined` vs `rejected` per QUALITY.md Q1-Q6 and CORPUS.md. Attack-on-build: independent agreement with the scout's `mine` recommendation.

## Result

**Agree: mined.** Every byte-level check passed; the new-ground case is confirmed independently.

## 1. Capture byte verification (all match the manifest-record)

Against `.ufo/waves/round-40/wave1/ScoutS021.capture.txt` and `ScoutS021.manifest-record.json`:

- `sha256sum ScoutS021.capture.txt` → `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329` — equals record `sha256`.
- `wc -c` → 58004 — equals record `size_bytes`/`snapshot_bytes` (58004).
- `wc -l` → 432 — equals record `lines` (432).
- `file` → UTF-8 text, consistent with the record's `normalized` note.
- Record self-consistency: `status` 200; `fetched_utc` 2026-10-26T21:15:57Z matches `http.date` "Mon, 26 Oct 2026 21:15:57 GMT" and is in the past (not future-dated); `fetched_bytes` 127832 = raw HTML.
- `ScoutS021.manifest-record.json`: 38 lines, sha256 `439d2fb63956fc21fe43b3b5989b1157ab9bedb5dec38216294391e0baa790f9` — matches the scout receipt's claim.

## 2. Independent re-fetch (not just re-open)

`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -D headers.txt -o raw.html -w ...` on the S021 URL, from my scratch dir, 2026-10-26T21:18:41Z:

- Observed: `HTTP=200 CT=text/html; charset=utf-8 SIZE=127832 URL=https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy REDIR=0`.
- `sha256sum raw.html` → `fc7267288c8de400d433d911c3336fc573f65ea50d74d1b1a56f82a0cc998a5d` — **byte-identical to the record's `raw_sha256`** (fetched ~3 min after the scout's 21:15:57Z fetch; upstream stable).
- Reproduced the snapshot transform myself: imported `corpus/instruments/capture-source.py` `html_to_text()` over my re-fetched raw bytes → sha256 `72dbba57…329`, 58004 bytes, 432 lines, `byte_identical = True` against the delivered capture. The record's `normalized` description matches the instrument's actual behavior.

## 3. Quote verification

Quote (record Q1): "restrict the reporter’s ability to disclose discovered vulnerabilities to others, except for a request for a reasonably time-limited response period."

- `grep -c` of the exact string (curly apostrophe U+2019, as recorded) in the capture → **1** (unique). ASCII-apostrophe variant → 0, i.e. the quote is the capture's own byte form, not a retyped normalization.
- L133 reads: `Attempt to restrict the reporter’s ability to disclose discovered vulnerabilities to others, except for a request for a reasonably time-limited response period.` — the record's location note ("quote starts after the leading 'Attempt to'") is accurate; 20 words ≤ 25 (Q3).
- Context verified: L130 `The policy, or implementation of policy, must not:`; the quote is the third item of that list under Required Actions, as the record states.
- Lane instrument, run by me on a scratch wrapper manifest (`{"schema_version":1, ..., "sources":[record]}` with the capture copied as `S021.txt` beside it): `python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json --source S021` → `S021:sha256 OK` / `S021:Q1 OK occurrences=1 anchor=133-ok`, **exit 0**. (B1 stem check and B2 anchor check both pass.)

## 4. Verdict assessment (QUALITY.md Q1-Q6, CORPUS.md)

New-ground check, run independently (not trusting the scout's grep):

- `grep -rn "BOD 20-01|bod-20-01|20-01" corpus/knowledge/` → exactly one hit: `authorization-safe-harbor-and-scope.md:38` — "S008 is a CISA template written to help agencies create a VDP aligned with BOD 20-01". The lane holds the **template** (S008), not the directive's own requirements.
- Per-term counts in corpus/knowledge for the directive's distinctive requirements — `vetted`, `U.S. citizens`, `Equities`, `reasonably time-limited`, `anonymously`, `180 calendar` — **all 0**.
- Frontier rows F01-F22 (corpus/README.md): no federal-VDP row. F03 is authorization/safe-harbor via S006-S008; F18 is KEV under BOD 26-04 (a different, later directive); F22 is VEX issuance. Uncovered ground in the capture, all located: mandatory VDP elements (L119-129, incl. anonymous-submission statement L125, no-legal-action commitment L126, acknowledgement expectations L127, issuance date), the must-not list (L130-134: no PII required, no vetted/citizenship limit, no disclosure restriction beyond a time-limited response request, no VEP submission), 30/180/270-calendar-day + 2-year clocks (L112, L117, L139-140 — spot-checked L112/L117 verbatim), handling timelines (L141-155, footnotes 3 business days / 7 days / 90 days), CyberScope reporting metrics (L161-171 — spot-checked).
- No prior rejection of the directive: round-22 lesson opened S021 `queued` (different quote, L98-equivalent); round-35's kake rejection was of the BOD 20-01 **template**, not the directive. CORPUS.md `rejected` semantics (covered/superseded ground) do not apply.
- Q1-Q6 fit of the planned entry: Q3 quote verbatim + anchored ✓; Q4 — capture L92-95 confirms the directive binds federal executive-branch agencies only ("compulsory direction to federal, executive branch, departments and agencies"; "do not apply to statutorily defined 'national security systems'…"), so the entry must attribute to the directive and keep the FCEB-only scope, never generalize to vendors/bounty programs (the scout receipt already flags this; the row's `teaches` phrasing is the lane's inference, and the directive itself calls a VDP "similar to, but distinct from" a bug bounty at L107); Q6 — documentation-only, no operational instruction ✓. Q1/Q2/Q5 are entry-writing obligations owned by ScribeEntriesG2; the capture supplies what they need (provenance trio, tier-A row, falsifiable must-not list).

## 5. Notes

- Minor shape observation (not a defect): the record carries the seat-requested `files`/`status`/`size_bytes` plus `normalized` and `http{}` but no `snapshot_sha256` alias (S016's record had one); `sha256` is the capture digest either way, and the L1 wraps the record into the manifest envelope per the scout receipt.
- No tools installed (nothing to record). One network fetch (the re-fetch above): HTTP 200, 127832 bytes, 2026-10-26T21:18:41Z, UA `kasegi-shokunin/1.0`.
- Scratch `/fast/scratch/hyaku/kasegi-r40/ScoutS021Chk` removed before yield.

## Deliverable

- `ScoutS021Chk.txt` — 1 line, 1005 bytes, sha256 `818b45e68d7fbc605f35c92d4a9d90f839d5daf9c199a54995c43c1bc3a4c326`.
