# ExecC2Probe — independent probe of the landed capture-secret-scan at 9964608

Seat: ExecC2Probe-2 (round-94 w1). Probed rev: 996460861d4130ddb2da6b7554e905d3e47504a3 (C2 landing).
Method: independent — copied `corpus/instruments/capture-secret-scan.py`, `claim-package-check.py`, `capture-secret-allow.tsv` and `corpus/source-snapshots/round-94/S140.txt` out of the rev with `git show` into private scratch; built my own fixture files from scratch-derived 20-char fake tails; derived expected matches by hand from the landed regex source before running, then measured with the landed CLI. The wave counter (`capability-check.py`) was not imported and its fixtures were not reused. Fixture tails are fabricated, not credentials.

## Verdict

**AGREE, scoped to this probe**: the landed scanner's three GitLab shapes behave exactly as the frozen C2 statement defines them, re-derived independently and confirmed by measurement. 7/7 seat-spec positives hit with the correct shape attribution; 6/6 core spec negatives are clean; `--selftest` passes. One seat-spec "negative" (21-character custom prefix) measures as a HIT — see D1; it does not contradict the frozen statement, which never promises a miss for that input.

Per-item results (all single-line fixtures, hit line=1):

| fixture | content shape | derived | measured |
|---|---|---|---|
| p01 | `acme-` + `glpat-` + 20 tail | gitlab-pat | HIT gitlab-pat |
| p02 | `glpat-` + 20 tail | gitlab-pat | HIT gitlab-pat |
| p03 | `glrt-` + 20 tail | gitlab-runner-auth-token | HIT gitlab-runner-auth-token |
| p04 | `glrtr-t1_` + 20 tail | gitlab-runner-auth-token | HIT gitlab-runner-auth-token |
| p05 | `gldt-` + 20 tail | gitlab-deploy-token | HIT gitlab-deploy-token |
| p06 | `acme-` + `glrt-` + 20 tail | gitlab-runner-auth-token | HIT gitlab-runner-auth-token |
| p07 | `acme-` + `gldt-` + 20 tail | gitlab-deploy-token | HIT gitlab-deploy-token |
| n01 | `xglpat-` + 20 tail (letter before prefix, no hyphen) | none | clean |
| n02 | `gldt-` + 19 tail | none | clean |
| n03 | `gldt-` + 21 tail | none | clean |
| n04 | `glrt-` + 21 tail | none | clean |
| n05 | `glrtr-t4_` + 20 tail (t4_ not in t[1-3]) | none | clean |
| n06 | `GLD T-` + 20 tail (case + space) | none | clean |
| n07 | 21 alnum + `-` + `glpat-` + 20 tail | **gitlab-pat (inner unprefixed token)** | HIT gitlab-pat |

Primary run: `CAPTURE-SECRET-SCAN mode=files scanned=14 hits=8 files=8 allowed=0 unused_allow=23 rc=1`.

Selftest: `SELFTEST-RESULT pass cases=101`, rc=0, zero per-case FAIL lines (probe-02).

S140 capture scan: the committed redacted snapshot scans **clean — hits=0** both with the landed allowlist bound (`allowed=0 unused_allow=23 rc=0`) and with an empty allowlist (`unused_allow=0 rc=0`), so the clean result is genuine, not allow-masked. This matches the redaction design: example/negativeExample values are replaced by a fixed marker and the three quoted regex lines (anchors 4, 114, 255) carry regex character classes (`[0-9a-zA-Z_\-]{20}`), not literal 20-char tails.

Boundary extras (supplementary, beyond the spec'd 14): a prefix of exactly 20 alnum + `-` + `glpat-` + tail HITS (the 1-20 prefix bound is inclusive and measured at the boundary); the same 21-char prefix run with no hyphen before `glpat-` is clean (left boundary rejects the alnum-preceded token).

Shape-source cross-check (probe-07): the landed regexes equal the vendor's own rules at S140 lines 4/114/255 — `(?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20}`, `glrtr?-(?:t[1-3]_)?[0-9a-zA-Z_\-]{20}`, `gldt-[0-9a-zA-Z_\-]{20}` — with the lane's left boundary (`(?<![A-Za-z0-9_])` plus escape-terminator alternatives) equivalent to the vendor's `\b` for every measured case, and the lane's right lookahead `(?![A-Za-z0-9_-])` equivalent to the vendor's `(?:[^0-9a-zA-Z_\-]|$)`. The escape-terminator left-boundary alternatives are the lane's documented round-93 extension, not a vendor shape.

Routed qualifier (not a verdict change):

- **D1 — seat-spec negative n07 is not a negative.** A 21-character custom instance prefix followed by `-glpat-` + 20 tail measures as `gitlab-pat`: the optional prefix group cannot span the 21-char run, but the match restarts at the inner `glpat-`, whose preceding `-` satisfies the left boundary (vendor `\b` behaves the same). The frozen C2 statement pins 1-20 prefix acceptance and the letter-before-no-hyphen negative; it is silent on >20 prefixes, so the claim is unaffected. If any wave label or fixture elsewhere assumed a 21-char prefix instance is missed, that assumption is wrong for both the landed scanner and the vendor rule; route to the wave authors as an expectation fix, not a scanner defect.
- **D2 — S140 sha bookkeeping.** claims.json's frontier line pins the *raw* snapshot sha 04fc5cfa…; the committed capture (blob identical from freeze 96b5033 through C2 landing to HEAD) hashes f3fd09e4… because example/negativeExample values were redacted before commit (redaction-r94.txt records both values and the 82 redacted lines; line count 563 preserved). Consistent pair, but the claims.json line names only the never-committed sha — worth a wording fix in the round-95 lesson.

Pins re-verified at the probed rev: instrument sha256 22ba32d145f90f7759caf16d3ee524eb1779153d3f2a33611675a93a4667beaf (matches frozen), gate sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 (matches frozen). This probe did not run `capability-check.py` and does not re-score the C2 predicate; K1-K9 remain the counter's to prove.

## Receipts

All commands run with cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin` or the stated scratch; outputs preserved under `.ufo/waves/round-94/w1/ExecC2Probe-receipts/`.

- probe-00-extract.txt — `git show 9964608…:{scanner,gate,S140}` into scratch; `sha256sum` all three: instrument 22ba32d1… ✓ pin, gate 8b6f8493… ✓ pin, S140 f3fd09e4… (see D2); wc: 491/802/563 lines. rc=0.
- probe-01-s140-revs.txt — `git log`/`rev-parse` for the capture path: absent at base dff5a0a, blob 076cdc9 identical at freeze, C2 landing, HEAD and working tree. rc=0.
- probe-07-regex-derivation.txt — landed `GITLAB_PATTERNS` printed from the scratch copy; per-fixture `scan_bytes()` derivation (expectation table above, derived before the CLI runs); fixture sha256 manifest (16 files); S140 lines 4/114/255 quoted. rc=0.
- probe-02-selftest.txt — `python3 -B capture-secret-scan.py --selftest`: 102 lines, 0 FAIL lines, `SELFTEST-RESULT pass cases=101`, rc=0.
- probe-03-files-spec14.txt — `--files` on the 14 seat-spec fixtures: 8 HIT lines (table above), `scanned=14 hits=8 files=8 allowed=0 unused_allow=23`, rc=1 (hits are the expected nonzero exit).
- probe-04-files-extras.txt — `--files` on the two boundary extras: 1 HIT (x02, 20-char prefix), x01 clean, `scanned=2 hits=1 files=1`, rc=1.
- probe-05-s140-allow.txt — `--files corpus/source-snapshots/round-94/S140.txt` from lane root with the landed allowlist (23 data rows, printed count appended): `hits=0 allowed=0 unused_allow=23`, rc=0.
- probe-06-s140-noallow.txt — same file, empty allowlist: `hits=0 unused_allow=0`, rc=0.

Notes: scratch `/fast/scratch/hyaku/kasegi-r94/ExecC2Probe` removed and verified gone at seat end (cleanup by explicit `rm -rf` after the runs; the persistent shell would have fired an EXIT trap mid-seat). No tools installed or upgraded (none needed; pacman paused per orchestrator ruling). No git/jj mutation anywhere; the only lane writes are this report and the receipts directory. No credential values appear anywhere: every fixture tail is fabricated by this seat.
