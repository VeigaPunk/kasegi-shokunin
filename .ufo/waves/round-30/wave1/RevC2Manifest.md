# RevC2Manifest — round-30 source-snapshot manifest assertion re-run

Seat: RevC2Manifest-2 (kasegi round 30, wave 1). Date: 2026-10-25. Scope: re-run
`corpus/instruments/source-recheck.py` against `corpus/source-snapshots/round-30/manifest.json`
for S046, S047, S041; verify sha256 pins, stems==ids, anchors in range, and selftest.
No files were written outside this report. No tools installed. No network contact with any
bounty target; all checks are local-bytes only.

## Measured bytes (sha256, independently computed via `sha256sum`)

| File | sha256 | Matches manifest pin |
|---|---|---|
| corpus/source-snapshots/round-30/manifest.json | `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6` (3523 bytes, mtime 2026-10-25 15:52:11.204 -0300) | n/a (is the pin file) |
| corpus/source-snapshots/round-30/S046.txt (575 lines) | `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3` | YES |
| corpus/source-snapshots/round-30/S047.txt (1402 lines) | `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4` | YES |
| corpus/source-snapshots/round-30/S041.txt (2354 lines) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` | YES |

## Measurement timeline (material — the manifest was mutated mid-verification)

1. **Pass 1** (before 15:52:11 -0300): S046 FAIL (Q1 `quote-not-found`, Q2 `occurrence-not-unique`),
   S047 FAIL (Q1/Q3 `occurrence-not-unique`), S041 FAIL (Q2 `quote-not-found`); all three sha256 OK.
   These results were measured against **pre-edit manifest bytes that I did not hash** (behavior only).
2. The manifest was modified on disk at **15:52:11.204787 -0300** by a concurrent wave writer while I
   was reading it (wave1 contains `ExecImplSourceRecheck.{md,diff,pre.py}` — the B1/B2 enforcement
   work; the manifest edit adding anchors/correcting quotes is consistent with that seat's round).
3. **Pass 2** (after edit, ~15:53) and **Pass 3** (Pass 2 + 30 s stability re-poll): identical
   results, all three sources exit 0; manifest hash `dfc88357…` identical across both passes.
   All Pass 2/3 results below are against `dfc88357…` bytes only.

## Final assertion results (manifest `dfc88357…`, two consecutive green passes)

- **S046** exit 0: sha256 OK; Q1 OK occurrences=1; Q2 OK occurrences=1; Q3 OK
  `normalized=markup-whitespace occurrences=1`; Q4 OK `normalized=markup-whitespace occurrences=1`.
- **S047** exit 0: sha256 OK; Q1 OK occurrences=3 **anchor=123-ok**; Q2 OK occurrences=1;
  Q3 OK occurrences=2 **anchor=130-ok**; Q4 OK occurrences=1; Q5 OK occurrences=1.
- **S041** exit 0: sha256 OK; Q1 OK occurrences=1; Q2 OK occurrences=1; Q3 OK occurrences=1.
- **B1 stems==ids**: S046.txt→S046, S047.txt→S047, S041.txt→S041; no `stem-mismatch` emitted.
- **Anchors in range**: only S047 declares anchors (Q1=123, Q3=130), both int, ≤ 1402 capture
  lines, both verify `anchor=N-ok` under the B2 rule. S046/S041 declare none and are unique.
- **Selftest**: `python3 corpus/instruments/source-recheck.py --selftest` → 9 cases, 0 failures,
  exit 0 (clean / corrupt / missing-source / missing-manifest / stem-mismatch / double-occurrence /
  -anchored / -out-of-range / -broken all PASS). Run against the working-tree instrument.

## Verdict

**PASS — for the exact bytes hashed above.** Every assertion passes under the instrument's
Round-30 Q9 contract (B1 stem equality; B2 non-unique quotes anchored and anchor-verified);
all three capture sha256 pins bind the checked-in bytes; selftest is green. Reasons: (a) pins
independently re-hashed and matching; (b) B1 holds on all three records; (c) the only non-unique
assertions (S047 Q1/Q3) carry in-range anchors that verify; (d) selftest 9/9 including the B2
anchor limbs; (e) stable across two consecutive passes 30 s apart.

The PASS is **not certifiable as frozen**: see findings 1–2.

## Findings by severity

1. **MEDIUM — mid-verification manifest mutation.** The manifest changed at 15:52:11.204 -0300
   between my Pass 1 and Pass 2 (anchors added to S047 Q1/Q3; quote strings for S046 Q1/Q2 and
   S041 Q2 altered — Pass 1 `quote-not-found`/`occurrence-not-unique` became found/unique without
   any capture change, and capture hashes were identical in both passes). Any receipt citing
   Pass-1-style FAILs, or citing an earlier manifest hash, is stale. Pre-edit manifest bytes were
   not hashed by me; only their behavior was observed.
2. **MEDIUM — measured state is entirely uncommitted.** `git status --porcelain` shows
   `?? corpus/source-snapshots/round-30/` (whole directory untracked) and
   ` M corpus/instruments/source-recheck.py` (+126/−14: the Round-30 Q9 B1/B2 enforcement, turning
   previously non-fatal `anchor=BROKEN` notes into exit-1 failures). The claims-freeze commit
   3c557354 pins none of these bytes; the green state exists only in the working tree and a reset
   would silently revert both the anchors and the fatal-anchor semantics.
3. **INFO — ticket phrasing vs gate semantics.** "All assertions occurrences=1 raw and normalized"
   does not hold literally under manifest `dfc88357…`: S047 Q1 occurs 3× and Q3 2× (legitimate
   under B2 with verified anchors), and S046 Q3/Q4 have **no raw-substring match** — they pass only
   via the declared `markup-whitespace` normalization (reader `<u>` markup). This conforms to the
   instrument's documented contract, but any downstream check expecting literal occurrences=1-raw
   should cite the instrument output, not the phrasing.

## Residual risk and verification gaps

- Pre-edit manifest bytes unobserved (no hash captured before 15:52:11 edit) — cannot prove the
  edit was limited to anchors + the five quote strings named above.
- I verified captured bytes against manifest pins only; per the instrument's own docstring this
  says nothing about upstream availability/freshness of S041/S046/S047 sources (and upstream
  contact is prohibited for this seat).
- No `lsp` device is available in this session; the instrument was reviewed by direct file read
  (403 lines), and behavior confirmed by execution + selftest, not by semantic index.
- Concurrent wave writers are still active in this directory; anyone re-running must re-hash the
  manifest first and treat any hash ≠ `dfc88357…` as a different measurement.
