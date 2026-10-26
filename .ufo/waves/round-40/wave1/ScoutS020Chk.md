# ScoutS020Chk — round 40, cross-check of ScoutS020's capture for row S020

Seat: reviewer cross-check (leaf, no subagents). Item: re-fetch/re-open the captured bytes for
S020 (DOJ CCIPS, "A Framework for a Vulnerability Disclosure Program for Online Systems",
https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline=), verify
sha256/status/size and quote occurrence, and assess `mined` vs `rejected` per QUALITY.md Q1-Q6
and CORPUS.md. Attack-on-build posture: my agreement is independent evidence.

## Verdict (delivered in ScoutS020Chk.txt)

**mined** — every check below passed on bytes I produced independently, and the
covered/superseded reading has no support in the corpus.

## Independent verification (commands + observed output)

1. **Independent re-fetch #1 (curl, per seat spec).** From my scratch:
   `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o s020-fetch.bin -w '...' '<url>'`
   → `HTTP_STATUS=200 SIZE=140909 URL=https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline= CONTENT_TYPE=application/pdf`,
   `FETCH_UTC=2026-10-26T21:17:10Z`,
   `sha256 s020-fetch.bin` → `d0cfa766a29328e120be7187435d09e5aef374c80bcbf0b1bd7a167c16e51ee7`,
   `file` → `PDF document, version 1.5`. Matches ScoutS020's reported fetch (status 200,
   140909 bytes, raw sha256 `d0cfa766…51ee7`, fetched_utc 2026-10-26T21:16:10Z) byte-for-byte
   on the raw artifact.

2. **Independent re-fetch #2 (the lane's own instrument, deterministic pipeline).**
   `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S020 --url '<url>' --out ./S020-refetch.txt --kind pdf`
   → `S020 status=200 fetched_bytes=140909 snapshot_bytes=16693 sha256=8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c utc=2026-10-26T21:17:43Z`.
   Two fetches ~90 s apart (ScoutS020's 21:16:10Z, mine 21:17:43Z) produce the identical
   snapshot digest — the capture is a faithful, deterministic conversion of the served PDF,
   not a one-off.

3. **Delivered capture byte-identity.** `sha256sum wave1/ScoutS020.capture.txt` →
   `8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c`; `wc -l -c` →
   `319 16693`; `cmp wave1/ScoutS020.capture.txt S020-refetch.txt` → silent,
   `BYTE_IDENTICAL_TO_MY_REFETCH`. Status/size fields in the record (status 200,
   fetched_bytes 140909, size_bytes/snapshot_bytes 16693, lines 319) all match observed.

4. **Manifest record.** `ScoutS020.manifest-record.json` sha256
   `06fe885da1dcaa063b14dcbfc328d0be5355b391b76a4a587c4634750d750b6b` (matches the scout's
   claim). Required fields present: `fetched_utc` 2026-10-26T21:16:10Z, `sha256`, `lines` 319,
   `files` ["S020.txt"], `url` (the registry row's URL), `status` 200, `size_bytes` 16693;
   plus the round-39-shape extras (raw_sha256/raw_bytes, snapshot_sha256, normalized, http
   block, quotes[Q1 anchor 142]). `path` stem `S020` == `id` (Q9/B1 binding).

5. **Quote occurrence (the spec's grep -c >= 1, done honestly).** The located quote is 22
   words and wraps capture L142-L145, so a single-pattern `grep -cF` of the full quote prints
   **0** on the line-collapsed capture — I verified occurrence three ways instead of
   accepting a naive miss or a forged single-line match:
   - per-line fragments: `grep -cF 'Absent an agreement with the'` → 1;
     `grep -cF 'cloud service provider, the organization implementing the vulnerability disclosure'` → 1;
     `grep -cF 'program may lack the authority to authorize others to access the provider'` → 1;
   - whitespace-joined whole-capture count (the Q8 declared normalization,
     `normalized=markup-whitespace`): **1** — exactly-once (Q9).
   - Word count of the quote: 22 ≤ 25 (Q3).

6. **source-recheck re-run by me, on the delivered bytes + delivered record** (record wrapped
   into `{"schema_version":1,"sources":[<record>]}` in my scratch, capture copied as
   `S020.txt` beside it):
   `python3 corpus/instruments/source-recheck.py --manifest ./chk-manifest.json --source S020`
   →
   ```
   S020:sha256 OK
   S020:Q1 OK normalized=markup-whitespace occurrences=1 anchor=142-ok
   recheck_exit=0
   ```
   Independently reproduces ScoutS020's claimed recheck result. The mined path's
   "capture passes source-recheck and is manifest-bound" requirement is satisfiable with
   these bytes.

7. **Coverage sweep (new-ground test, my own commands).** From `corpus/`:
   `grep -rilE 'department of justice|criminal-ccips|\bCFAA\b|computer fraud and abuse' knowledge README.md`
   → **no hits**; `grep -rl '983996' knowledge README.md SOURCES.md` → only `SOURCES.md`
   (the queued S020 row itself). Closest held ground, read directly:
   - `knowledge/authorization-safe-harbor-and-scope.md:39` (F03, S006/S007/S008): "These
     sources do not resolve third-party asset ownership, external legal protection, or
     whether an unlisted activity is authorized in a particular jurisdiction." — the lane's
     own admitted entry **names this gap**; S020's Step 1.C fills it from the org-design side.
   - `knowledge/statutory-authorization-and-unauthorized-access.md:46` (F09, Japan statute):
     "Where the asset is operated by a third party (a customer, a supplier, a hosting
     tenant), the platform's text cannot supply that third party's consent…" — researcher-side
     consent consequence only; it does not hold the DOJ framework's org-side rule that the
     organization itself "may lack the authority to authorize others to access the provider's
     servers" absent an agreement (capture L142-L145), nor the contract/counsel mechanism
     (L146-L151).
   No supersession candidate exists: no other registry row is a version of this document
   (unlike S022→S030/S031 CNA rules and S024→S029 CRA, where rejection is version supersession).

8. **Anchor content spot-reads in the delivered capture** (all present, verbatim):
   - L6-L8 title + "Version 1.0 (July 2017)" — matches the row's anchor cell.
   - L35-L36: "This guidance is intended as assistance, not authority. Nothing in it is
     intended to create any substantive or procedural rights…" — the Q4 attribution guard is
     quotable from the capture itself (DOJ's position, guidance not authority).
   - L133-L137 Step 1 marker C + third-party-interests paragraph; L138-L145 cloud-storage
     example; L146-L151 service-level-contract/counsel point.
   - L229-L232 Step 3 heading + item A: "Describe authorized and unauthorized conduct in
     plain, easily understood terms." (occurs exactly once; single line).
   - L73-L79 CFAA footnote (18 U.S.C. § 1030(e)(2)/(e)(8), "without authorization or in
     excess of authorization", "not limited to purely domestic conduct").
   - L282-L296 Step 3.D commitments (no civil action/law-enforcement complaint for good-faith
     violations; policy-consistent activity "authorized" under the CFAA; org will make
     compliance known to public/court).

## Q1-Q6 assessment (can an entry citing this capture satisfy the bar?)

| criterion | support in quote+capture |
|---|---|
| Q1 | Row S020 gives source id + URL; anchor "Steps 1(C) and 3(A); Version 1.0, July 2017" verified at L133-L137/L229-L232, L8; recheck command proven above (exit 0 on delivered bytes). |
| Q2 | docs, tier A (official DOJ guidance) — primary for its scope; opened this round. |
| Q3 | Located quote 22 words, verbatim, exactly-once under declared normalization, anchor 142 verified by the instrument. |
| Q4 | Attribution guard in the document itself (L35-L36 "assistance, not authority"); entry must state DOJ's position, not a universal rule — supportable. |
| Q5 | Falsifiable rule available ("a VDP may authorize testing of supplier-hosted assets without the provider's agreement" — rejected by L142-L145); over-generalization to reject is natural ("a VDP authorizes everything in cloud scope"). |
| Q6 | Capture is public PDF text; no credential/session/private URL; no probing instruction. |

## Why not `rejected`

The rejected pattern in this round (S022 superseded by S030; S024 by S029) is version
supersession or already-held ground. S020 has neither: no other row carries this document,
and the ground it teaches (org-side supplier-hosted authorization limit; plain
allowed/disallowed-conduct drafting; US CFAA framing) is absent from `corpus/knowledge` and
explicitly named unresolved by F03's own Limits line. Caveat that belongs in the eventual
entry's Limits, not a rejection ground: 2017 guidance using "may"; no case law and no current
DOJ charging policy in these bytes; the 18F/NTIA/ISO 29147 pointers (L145-L166) are unread
links, not content.

## Tools

No installs. `pdftotext` (poppler 26.08.0, /usr/bin) pre-existing on the host; the lane's
`capture-source.py` and `source-recheck.py` run read-only against scratch. Disk guard green
before the fetch (/fast/scratch/hyaku 26% used, 600.3G free). No tool/version/channel to
record beyond that.

## Deliverable

`ScoutS020Chk.txt` — 1 line, 2223 bytes, sha256
`a57c6c0a56e9ef3507c287dd97d4e4087b00939937edebb8abecc0d18fe9caf7`.

## Scratch

All work copies bound under `/fast/scratch/hyaku/kasegi-r40/ScoutS020Chk/` (fetch bin, two
capture copies, chk-manifest.json); removed before yield.
