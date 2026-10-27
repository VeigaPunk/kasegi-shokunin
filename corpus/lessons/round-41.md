# Round 41 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `5b29ea1439450b712581edf5f0f0bf98dfb262ab`; claims-freeze commit
`fbba3d96cdf8d37c1ea41304a1ba35691329684b` (`.ufo/waves/round-41/claims.json`). Judged head J = the lane
commit carrying every round-41 change except the receipt; verification ref Y = J + the receipt
`.ufo/waves/round-41/final-gates/all-gates.txt` only. Lane files never name J by hash (a commit cannot
contain its own hash); the report names J and Y. Counting commands run over the suite run at Y; negative
controls run at base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` and round-40 judged head
`c7aea5ef97902f38289cbdc1cf267068876a62dd`. Shape: `<<<WAVES>>>`.

Attack share: wave 1 `kasegi-r41-build` 20/60 = 33.3% (reviewer 9 + critic 6 + mutation-tester 5, counted
from the `wave1-dispatch.json` registry members, `counts.spawn` 60); wave 2 and the round total are counted
from the wave-2 dispatch when it lands, never estimated: `<<<WAVE2-TALLY>>>`.

## Frozen claims

Before → after, as frozen in `.ufo/waves/round-41/claims.json` (2026-10-27T09:05:00Z, KasegiR41).

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | suite absent — base export exits 127 and nothing prints `closed=12/12` (`c1-controls/do-nothing.txt`); open routed defects D1 (r40 C1 graded verified while its kill rule fires), D2 (Y-level selftest tally without a transcript), D3 (H1/H2/H3/H5/H6/H7/H8/H9 instrument survivors + 8 CritKillRule escape states), D4 (lesson duplicated Gate heading + garbled census line), D5 (lesson attack-tally error), D6 (SKILL.md registry table broken) | `r41-closure.sh` landed and export-mode only (plain run exits 2); `closed=12/12 exit=0` at Y; graded `selftest cases=12 failures=0` with BOTH transcripts teed in the receipt (`time-basis=ref-commit`, `run-utc` = ref committer instant); base and r40-head exports red; every routed defect closed by the check that names it (I1-I12) |
| C2 | coverage (8, held) | frontier 23 (F24 absent); registry 62 (S063 absent); entries citing S063 0; knowledge 59; queued 0; admitted 23; harness 26/26; binding 54/54; audit lines 59 expected 59; census exit 0 (W04 S028/S029 only) — `c2-controls/before.txt` | frontier 24 (F24 admitted); registry 63 (S063 mined); entry citing S063 1; knowledge 60; harness 27/27 incl `PASS F24 ids=S063`; binding 55/55; audit expected=60; census exit 0; measure 44/44 = 1.000 |

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

`<<<WAVE2>>>` — appended when the round-41 falsify wave reports: per-claim verdicts, attack tallies counted
from the wave-2 dispatch, and each routed defect named with the check that reds it.
