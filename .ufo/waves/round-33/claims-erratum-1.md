# C1 erratum 1 — Rule B binding semantics (L1 ruling, before any measurement)

Filed 2026-10-26 by the L1 (KasegiR33) after ScoutManifestAudit surfaced a Rule B hazard at
base. This erratum clarifies the frozen C1 interface contract; it does not change the frozen
claim's predicate sentence, counters, kill rule or targets. No seat had scored when it was filed.

## Finding (ScoutManifestAudit §4)

- URL `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` is carried by TWO registry rows:
  S024 (queued) and S029 (mined, supersedes S024). Record S029 exists in the round-23 manifest.
- URL `https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq` is carried by
  TWO registry rows: S006 (mined) and S028 (rejected duplicate-row proposal). Record S006 exists
  in the round-24 manifest.
- URL for S048 occurs once as a registry-row source cell (row S048) and once as raw text inside
  a Search-log bullet (line 72) — not a row cell.

Under a global "URL appears in exactly one registry row" reading, records S029 and S006 could never
bind (2 row matches), so `unbound=0` would be unattainable without touching immutable registry rows
(R8), which no seat may do this round.

## Ruling (binding for ExecCaptureBinding, ExecManifestUpgrade, RevC1Instrument, CritC1Kill)

Rule B binds each record to its OWN registry row:

1. For a record with id `Sxxx`, locate the registry row `| Sxxx | ... |` in
   `corpus/SOURCES.md` (source cell). If NO row carries that id -> failure `no-row` (fabrication).
2. The record's `url` must equal the row's URL byte-for-byte (the URL = the `https://` token in
   the row's source cell). Mismatch -> failure `url-mismatch`.
3. If TWO rows carry the same id (never observed), -> failure `dup-id`.
4. A URL that also appears in other rows (S024/S029, S006/S028) or in prose (search log) is NOT a
   failure: the checker prints an informational count `multi_row_url=N` (records whose URL text
   appears in more than one row) and the receipts disclose it. The registry's pre-existing W04
   duplicate-URL warnings are census facts outside this claim.
5. `bound` = records satisfying 1+2 (and rule C). `unbound` = records failing 1, 2, 3 or rule C.

Predicate sentence, kill rule, counters and the 40/40/0 target are unchanged.
