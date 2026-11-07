# ExecC2Probe — round-93 w1, independent end-to-end probe of the landed capture-secret-scan

Seat: ExecC2Probe (leaf, wave w1 of 13). Target: the scanner as landed at 9225954a6e3f177af46bdb9d811c062a4353a552 (lane HEAD during the probe, `git rev-parse` = 9225954a…). Method: independent probe only — no counter import; fresh fixture repo built in seat scratch; all fixture values below are synthetic (invented for this probe, not credentials).

## Verdict

rev_hits=4 files_hits=4 selftest=pass cases=90 intake=refused

- The landed scanner's `gitlab-pat` shape and the escape-terminator left boundary behave exactly as the frozen C2 statement says on every limb I probed; AGREE on the probed surface (I re-derived each result from the committed bytes, not from the counter).
- Pins: corpus/instruments/capture-secret-scan.py sha256 7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5 = the frozen candidate sha256; corpus/instruments/claim-package-check.py (the gate the scanner imports SECRET_PATTERNS from) sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 = the frozen gate sha256; corpus/source-snapshots/round-93/S139.txt sha256 154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188 = the frozen S139 sha256. Observed in pins.txt.

## Fixture and method

- Fixture repo: git init in scratch (`/fast/scratch/hyaku/kasegi-r93/ExecC2Probe/fixture`), `git rev-parse --show-toplevel` asserted equal to the fixture dir before the commit (toplevel-ok line in each build run); fixture HEAD 38a6023346c68326129f9ab299f79e4c952b8577, five files under `corpus/source-snapshots/round-93-probe/` (capture-class path so `--rev` scans them). Byte manifest: receipts/fixture-manifest.txt.
- Positives (one per file, 20-char tails over `A-Za-z0-9_-`, all six values distinct):
  - prose.md:1 — `glpat-REDACTED-r93` in prose;
  - data.json:1 — `glpat-REDACTED-r93` as a JSON value;
  - escapes-tab.log:1 — `glpat-REDACTED-r93` preceded by a literal two-byte `\t` escape inside a JSON-ish log line;
  - escapes-pct.log:1 — `glpat-REDACTED-r93` preceded by `%20` in a URL query.
- Negatives (negatives.txt, six lines, none matching the key-name shapes of the gate patterns either): 19-char tail, 21-char tail, `glrt-`+20, bare prefix (the S139 sentence), letter-prefixed `xglpat-`+20, post-escape (`\t`) with trailing `_`.

## Findings

1. `--rev HEAD` over the fixture (receipts/fixture-rev.txt, rc=1):
   ```
   HIT shape=gitlab-pat path=corpus/source-snapshots/round-93-probe/data.json line=1
   HIT shape=gitlab-pat path=corpus/source-snapshots/round-93-probe/escapes-pct.log line=1
   HIT shape=gitlab-pat path=corpus/source-snapshots/round-93-probe/escapes-tab.log line=1
   HIT shape=gitlab-pat path=corpus/source-snapshots/round-93-probe/prose.md line=1
   CAPTURE-SECRET-SCAN mode=rev:HEAD scanned=5 hits=4 files=4 allowed=0 unused_allow=23 rc=1
   ```
   All four positives hit; no other shape fired; negatives clean.
2. `--files` over the same five paths (receipts/fixture-files.txt, rc=1): identical four HIT lines and identical summary except the mode label (`mode=files`). rev_hits = files_hits = 4.
3. All six negatives produced no line in either mode: 19 chars, 21 chars, `glrt-`, bare prefix, letter-prefixed, post-escape with trailing `_` — matches the frozen statement's negative list (uppercase `GLPAT-` is additionally covered by the selftest's `gl-pat-upper-prefix`, and the 36-char `-` tail by the github-token negative set).
4. S139 allowlist binding (each run `--files corpus/source-snapshots/round-93/S139.txt` from the lane root):
   - committed allowlist (receipts/s139-committed-allow.txt): `CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 files=0 allowed=4 unused_allow=19 rc=0` — all four S139 rows consumed, zero unused S139 rows, rc 0.
   - S139 rows removed (scratch copy, 19 rows left; receipts/s139-allow-rows-removed.txt): `HIT shape=bearer … line=124`, `HIT shape=credential … line=116`, `… hits=2 … allowed=0 … rc=1`.
   - Exact binding, one perturbed sha per run (scratch copies; each changes exactly one S139 row, diff checked =1 row): bearer-row perturbed → HIT bearer line=124, allowed=3; api_key-row perturbed → HIT credential line=116, allowed=1 (the 126/139 rows are never reached because reporting stops at the first non-allowed match per shape); api-token-row perturbed → HIT credential line=126, allowed=2; prose-row perturbed → HIT credential line=139, allowed=3. Each row therefore binds exactly its own matched value at its own line (116/124/126/139, agreeing with the reasons' line annotations), and a one-hex-digit change unbinds it.
5. `--selftest` (receipts/selftest.txt): `SELFTEST-RESULT pass cases=90`, rc=0, zero FAIL lines. The round-93 additions are present and ok: 11 `gh-escape-*` cases (tab, cr, u0020, pct20, pct3a, pct2f, u0026, pct26, html entity, right underscore negative, word-before) and 11 `gl-pat-*` cases (prose, json, after-pct20, after-u0026 positives; 19/21-char, right-underscore, upper-prefix, bare-prefix, letter-before, runner `glrt-` negatives).
6. Intake gate (receipts/intake-probe.txt; local HTTP server in scratch, capture-source.py with the committed allowlist, out paths in scratch): planted body → `INTAKE-REFUSED S000PROBE shape=gitlab-pat line=1 … written=no`, rc=3; the pre-existing out file kept byte-for-byte (`b'previous\n'`). Clean-body control → rc=0, snapshot written, so the refusal is caused by the planted `glpat-` value. intake=refused.
7. Fixture-construction incident (kept as evidence, not a scanner defect): my first escapes.log positive was written with a 21-character tail by construction error, and the scanner correctly refused it (receipts/fixture-rev-v1-21char-tail-rejected.txt shows only 3 hits; receipts/fixture-v1-debug.txt shows the byte-level diagnosis: tail `5f6G7h8I9jK1L2m3N4o5P` is 21 chars, so the `{20}`+lookahead rejects it — same behavior as selftest `gl-pat-21-chars`). Fixture v2 (receipts/fixture-rev-v2-tab-hit-first-per-shape.txt) also documents that one file carrying two positives yields one HIT line (first match per shape per file), which motivated splitting the escape positives into two files in fixture v3.

No unexpected scanner behavior observed. Named limits (glrt-, encoded prefix separator, fine-grained github_pat_) were not re-tested beyond the selftest's own negative cases; nothing in this probe contradicts them.

## Receipts

All under `.ufo/waves/round-93/w1/ExecC2Probe-receipts/`:

- pins.txt — lane HEAD, sha256 of capture-secret-scan.py, capture-source.py, claim-package-check.py, capture-secret-allow.tsv, S139.txt; frozen-pin MATCH lines observed in the run output.
- fixture-manifest.txt — fixture v3 per-file sha256 at HEAD 38a602334.
- fixture-rev.txt — `capture-secret-scan.py --lane <fixture> --rev HEAD`, rc=1, 4 HIT lines + summary above.
- fixture-files.txt — `--files <same five paths>`, rc=1, identical HIT set/summary.
- fixture-rev-v1-21char-tail-rejected.txt, fixture-files-v1-21char-tail-rejected.txt — v1 runs (rc=1, 3 hits; 21-char tail correctly rejected).
- fixture-v1-debug.txt — byte-level regex diagnosis of the v1 tail length (probe output).
- fixture-rev-v2-tab-hit-first-per-shape.txt — v2 run (rc=1, escapes-tab line 1 first-per-shape).
- s139-committed-allow.txt — S139 with committed allowlist, rc=0, allowed=4 unused=19.
- s139-allow-rows-removed.txt — S139 rows removed, rc=1, HIT bearer 124 + credential 116.
- s139-allow-perturb-bearer.txt / -apikey / -apitoken / -prose — one perturbed row each, rc=1, HIT lines 124/116/126/139 respectively.
- selftest.txt — `--selftest`, rc=0, `SELFTEST-RESULT pass cases=90`.
- intake-probe.txt — capture-source.py planted → INTAKE-REFUSED rc=3 written=no; clean control rc=0.

No repo files were modified by this seat (report and receipts only); no tools were installed or upgraded; scratch (`/fast/scratch/hyaku/kasegi-r93/ExecC2Probe`) is removed at seat end.
