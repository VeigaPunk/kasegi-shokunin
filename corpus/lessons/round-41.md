# Round 41 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `5b29ea1439450b712581edf5f0f0bf98dfb262ab`; claims-freeze commit
`fbba3d96cdf8d37c1ea41304a1ba35691329684b` (`.ufo/waves/round-41/claims.json`). Judged head J = the lane
commit carrying every round-41 change except the receipt; verification ref Y = J + the receipt
`.ufo/waves/round-41/final-gates/all-gates.txt` only. Lane files never name J by hash (a commit cannot
contain its own hash); the report names J and Y. Counting commands run over the suite run at Y; negative
controls run at base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` and round-40 judged head
`c7aea5ef97902f38289cbdc1cf267068876a62dd`. Shape: two v1 waves, 60-seat build + 33-seat falsify = 93
seats (within 64–128); no residual call.

Attack share: wave 1 `kasegi-r41-build` 20/60 = 33.3% (reviewer 9 + critic 6 + mutation-tester 5),
counted from `wave1-dispatch.json`; wave 2 `kasegi-r41-falsify` 32/33 = 97.0% (reviewer 7 + critic 13 +
mutation-tester 12; one scout), total 52/93 = 55.9%. Wave 2 had 0 connector seats (conformance item);
wave 1 had 2. Dead seats: 0 (all 93 settled).

## Frozen claims

Before → after, as frozen in `.ufo/waves/round-41/claims.json` (2026-10-27T09:05:00Z, KasegiR41).

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | suite absent — base export exits 127 and nothing prints `closed=12/12` (`c1-controls/do-nothing.txt`); routed defects D1-D6 | `r41-closure.sh` landed export-only. At the integrated probe ref, I1's evidence-not-named and I3's mangled-value-token defeats survive and selftest fails; final Y run/receipt is recorded below. C1 is not verified on the frozen kill rule, so no score move is claimed. |
| C2 | coverage (8, held) | frontier 23 (F24 absent); registry 62 (S063 absent); entries citing S063 0; knowledge 59; queued 0; admitted 23; harness 26/26; binding 54/54; audit lines 59 expected 59; census exit 0 (W04 S028/S029 only) — `c2-controls/before.txt` | F24 row and S063 evidence landed; measured frontier 24, registry 63 (S063 mined), entry 1, knowledge 60, harness 27/27, binding 55/55, audit expected 60, census exit 0, measure 44/44. However, wave-2 CritProvinceBoundary found substantive shared RFC 9116 ground with kake; C2 coverage credit is not verified and no score move is claimed. |

## Mistakes

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M41-1 | evidence-provenance/calibration | round-40 graded C1 **verified** while its frozen kill rule fired on committed wave-2 fixtures | `corpus/lessons/round-40-verifier-spotcheck.md` §5 D1 (the SCORECARD/LOG/report C1 lines against the firing clauses) plus `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` (T2/T4/T7/T13/T14 pass with the defect present), `CritKillRule.md` (eight escape states F1-F8) and `MutH6H10.md` D2 | R37 criterion + new R38 calibration criterion | `Correction (round 41)` lines in `SCORECARD.md`, `LOG.md` and `SHONEN.md` grade round-40 C1 not verified on the frozen counter and name the firing evidence; the r41 suite's I1 enforces the line set | I1 is red at the claims freeze: `git grep -c '^Correction (round 41)' fbba3d96` returns 0 matches (exit 1), so a suite that cannot red I1 there is not closed |

## Census

Before (`census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0. After (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`): `W04 S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes`; `W04 S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes`; `ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, exit 0.
The registry now has 63 rows (S063 added after S062; no existing row cells changed). F24 is
recorded in the appended README coverage amendment and the PROVINCE end-of-file amendment;
SOURCES.md received an appended search-log item and the S063 registry row.

## Gate

### Admitted — F24 / S063 (RFC 9116 security.txt)
- **Row.** S063, kind spec, tier A, status mined, opened 2026-10-27, recheck on-release, used-by
  `corpus/knowledge/rfc-9116-security-txt.md`; row deliverable `wave1/ExecC2Rows.registry-row.txt`
  (byte-identical).
- **Source / capture.** `https://www.rfc-editor.org/rfc/rfc9116.txt`; access 2026-10-27 (fetched
  2026-10-27T08:19:23Z, HTTP 200, 45129 raw bytes). Capture
  `corpus/source-snapshots/round-41/S063.txt` is the full normalized text (CRLF->LF, no HTML):
  842 lines, 39301 B, sha256 `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa`.
- **Quotes (≤25 words, located in the capture).** §3 (18 words, L335): `"If a
  "security.txt" file is present in both locations, the one in the "/.well-known/" path MUST be
  used."` — the requirement that resolves a legacy top-level copy against the well-known path.
  §2.5.5 (20 words, L270): `"It is RECOMMENDED that the value of this field be less
  than a year into the future to avoid staleness."` §5.3 (15 words, L536): `"Not having
  a "security.txt" file may be preferable to having stale information in this file."`
- **Entry.** `corpus/knowledge/rfc-9116-security-txt.md` (`source: S063`, `verified-at: 2026-10-27`,
  `ground: F24`, executable `recheck:`). Its limbs anchor to §3 (the `/.well-known/` location and the
  legacy top-level redirect), §2.5.3 and §2.5.5 (Contact and Expires are the only fields that must
  always be present, and Expires must not appear more than once), §2.5.4 (the field carries a key
  URI, never a key) and §2.5.7 (the Policy link); the entry separates the machine-readable discovery
  channel from the policy text it points at (F10).
- **Frontier admission.** F24 row + coverage-map row + `PROVINCE.md` `[r41 Frontier amendment]`
  appended (deliverables `wave1/ExecC2Rows.readme-row.txt`,
  `wave1/ExecC2Rows.province-amendment.txt`) puts the frontier at 23 -> 24 rows, F24/24 admitted.
- **Limit.** RFC 9116 is Informational, not Standards Track (Status of This Memo: the document is
  not an Internet Standards Track specification), so the row's tier A rests on the document's own
  BCP 14 keyword discipline (§1.2) rather than on IETF Standard status; and the one-year Expires
  window is RECOMMENDED, not required, so a publisher may lawfully set a later date and the capture
  cannot by itself prove a file stale. The capture is the rfc-editor plain text only — the HTML/XML
  renditions and any errata are not in it — and every section number above is the RFC's own
  numbering.

## Wave-2 falsification

The falsify wave settled 33/33 seats: reviewers 7, critics 13, mutation-testers 12, scout 1; dead 0.
The round has 0 connector seats in wave 2 (conformance item); wave 1 carried two connectors.

**C1 — not verified.** At the integrated probe ref, committed I1 and I3 defeat fixtures survived:
removing evidence from one correction kept I1's cross-record evidence union at 3/3, and the
`closed=10/100` mangled tally left I3 green. `CritC1KillRule.md` and `RevC1Counters.md` preserve the
transcripts. The integrated probe also had a missing final receipt and scratch-root strays, so its
I2/I6 positives are not final-Y verdicts; the post-wave receipt run is recorded at the later Y
measurement. The frozen C1 claim cannot be repaired in this round.

**C2 — source checks pass; coverage not verified.** After correcting the round-41 manifest to S063
only, source-recheck Q1-Q3 passed at anchors 330/270/235, frontier harness was 27/27, capture binding
55/55, audit 60/60, and the source census exited 0. Wave-2 found the capture-binding checker accepts
missing-path and URL-variant mutations and the frontier count drops a status-flipped F24 to 26/26
without a nonzero exit; the frozen after-state remains distinguishable by the required F24 line
and exact 27/27 tally. More importantly for admission, the `CritProvinceBoundary` finding in
`.ufo/waves/round-41/kasegi-r41-falsify-results.json` documents shared RFC 9116 ground with kake's
existing `security-txt-publishing.md` on fields, host scope, expiry and non-authorization;
publisher-versus-researcher labels do not by themselves prove disjoint coverage.
No coverage-score increase is claimed pending the boundary judgment.

Other falsification results remain bounded to their probes: `MutSkillTablePipes.md` found bare
internal pipes and leading first-cell whitespace survive I7; `CritDeclarationCoverage.md` found
I5/I12 do not require every changed path to be declared (its probe did not show a green suite);
`MutScratchTiming.md` found an outside-configured-root stray is not seen by I6, outside the committed
fixture clause as tested. `CritI12Necessity.md` confirms the H9/T7 out-of-export symlink escape
routes through I5. The full seat outputs are in `.ufo/waves/round-41/wave2/` and
`kasegi-r41-falsify-results.json`.

## considerthese (round 41)

Proposal 7, “Keep a proposal-status ledger,” was the one still-unimplemented item mined from
`considerthese/2026-10-26.md` (read 2026-10-27): appended its missing `## Round-40 dispositions`
section to `corpus/knowledge/considerthese-proposals-ledger.md`, covering all seven proposals.
Proposal 2's remaining checker was not mined because the only exemplar is PARKED with authorization,
prior-submission and reviewer-distinctness gates failing by construction; proposals 4 and 6 remain
operator-owned.

## Final Y measurement (post-Y closure)

The final receipt at Y `0f64b8c5b3522d4db2160db087002e3a5f321880`,
`.ufo/waves/round-41/final-gates/all-gates.txt`, is the 31-line transcript of the run at its named
J ref, sha256 `0915f51d774e5f4bd744912b6b2a87b7387f5437730bef166457766ca10b9e94`; its header records
`time-basis=ref-commit` and `run-utc=2026-10-27T12:16:34Z`. Replaying the suite at Y yielded
`closed=10/12 exit=1`; the graded selftest yielded `selftest cases=12 failures=6` and exit 1.
I1's per-correction evidence mutant and I3's `closed=10/100` mutant remain accepted; I2 receipt
comparison and I6 scratch scan also red in the Y replay. Thus the transcript is recorded as an
honest failed closure, not as a verified C1 result. The plain run refuses exit 2; the base and
round-40-head controls remain red.
