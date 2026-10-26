
# Round 39 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `480b1a505a2dfc14a4f718d16d63808247214d0a`; claims-freeze commit
`dcd31701720a6a4929a32471a62011ed87103421` (erratum `claims-erratum-1.md` E1/E2/E4/E5); judged head J = the
`export-ref=` of `.ufo/waves/round-39/final-gates/all-gates.txt`; verification ref Y = J + the receipt only.
Shape: two v1 waves — `kasegi-r39-build` 49 seats (executor 27, scribe 11, reviewer 6, critic 2, connector 1,
scout 2) + `kasegi-r39-falsify` 37 seats (reviewer 12, critic 8, mutation-tester 7, scout 4, sentinel 2,
connector 2, simplifier 1, scribe 1) = 86 total (64-128 band). Attack share: wave 2 27/37 = 73%.

## Frozen claims — before → after

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | suite absent; R1-R4 open; 25 surviving r38 mutants (c1-controls/before.txt) | suite landed; `closed=8/8 exit=0` at Y; graded `selftest cases=8 failures=0`; base/r38-head reds; receipt at Y |
| C2 | coverage (7, held) | frontier 21; registry 55; S057 0; knowledge 50; harness 24/24; binding 45/45; audit expected=50 | frontier 22; registry 59; S057 mined + S056/S058/S059 rejected; knowledge 51; harness 25/25; binding 46/46; audit expected=51; junk twin rejected |

## Gate

### Admitted — F22 / S057 (CISA, When to Issue VEX Information)
- **Row.** S057: kind docs, tier A, status mined, opened 2026-10-26, recheck 180d, used-by
  `corpus/knowledge/cisa-when-to-issue-vex.md`; NF=13; one `https://` token = manifest url. Row deliverable
  `wave1/ScribeRowS057.row.md` (byte-identical).
- **Quotes (each ≤25 words, located in the capture):** Q1 `S057.txt:12-14` "Whether, and when, to issue VEX
  information is a business decision for most suppliers…"; Q2 `:79-81` "The decisions and timing around providing
  VEX information are primarily business decisions and are not determined by a strict protocol."; Q3 `:136-138`
  timestamp-reaffirmation sentence; Q4 `:183-186` inheritance caution. Access date 2026-10-26; capture
  `corpus/source-snapshots/round-39/S057.txt` (275 lines, 17,971 B, sha256 11c8d6d6…); manifest `sha256`
  matches; live re-open byte-identical (ScoutReopenS057).
- **Entry.** `corpus/knowledge/cisa-when-to-issue-vex.md` (`source: S057`, `verified-at: 2026-10-26`,
  `ground: F22`, executable `recheck:`); recheck exit 0 (Q1-Q4 occurrences=1).
- **Frontier row** F22 + PROVINCE amendment + count-line (22/22 admitted).
- **Tier reasoning:** CISA's own guidance document (publication page + 508c PDF), tier A for its own statements;
  guidance, not a standard — scoped as such.

### Rejected
- S056 (CISA Minimum Requirements for VEX) — REJECTED: vocabulary already mirrored by S055; flip: a round that
  needs the consumer-side minimum-elements phrasing or tool-neutral metadata rules.
- S058 (OpenVEX v0.2.0) — REJECTED: same labels; community spec at mutable `main`, no release date; flip: pinned
  commit + release date + a ground needing its label-over-free-text recommendation.
- S059 (CycloneDX v1.7 analysis) — REJECTED: different vocabulary is a separate frontier; 6.4MB reference needs a
  scoped capture; flip: a CycloneDX-vs-CSAF entry with scoped analysis-subtree capture.

### Candidates considered and not taken
- CSAF v2.1 (Committee Specification Draft 04) — flip monitor: an OASIS Standard v2.1 exists (fired when `os/`
  appears).
- CISA VEX Status Justifications (June 2022) — moved to `## Leads (unopened)` (opened, origin of the five labels).
- The staged package's 7 refusals carry unchanged (byte-identical package, SOURCES.append.md sha256 4fe049cb…).

### Assimilation
Id-collision rerun (0-3-space extractor): reg-ids 55 (S001-S055), staged-ids 94 (S031-S124), `comm -12` = 25
collisions (S031-S055); guard proof reproduction on indented S002 fixture. Quarantine slice (7 rows): 2
quote-defective (S037, S054), 4 unreachable (S048, S068, S069, S070), 1 unverifiable (S065); 0 adopted. Standing
refusals carried; **Assimilation: none**.

### Considerthese
Proposal 1 (make distance-to-next-score explicit) mined into SCORECARD §Saturation: measured gap
depth:verifiability `gated=24` of `lines=50` (5 needs 0); coverage `41/50 = 0.820` strict, `41/41` frontier-only
(non-discriminating). Ledger round-39 dispositions section filled (rows 1-7); proposal 3 status carried; proposal 5
resolved-landed (F18 amendment at PROVINCE.md:77).

### Spot-check readiness
See `wave1/ScribeSpotCheckList.checklist.md` (items 1-9): capture identity, quote pins, row/registry 59, frontier
22, harness 25/25, binding 46/46, audit expected=51, census exit 0, junk red, C1 receipts at Y, quiescence.

## Census

Before (`census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0. After: `W04 S028`, `W04 S029`, `ok`,
exit 0. Registry 55 → 59 rows; tier A +1 (S057), rejected +3. Rows touched old→new: none besides additions
(registry-changes bullets). Search-log bullet appended.

## Mistakes

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M39-1 | stale-premise / claim hygiene | r38 C1 frozen unsatisfiable: predicate required 8/8 at J while G2 required the receipt inside the export and J was the receipt's own export-ref | r38 claims.json + all-gates.txt (`export-ref-run: closed=7/8 exit=1`); verifier R1 | none at freeze — R34 criterion added this round (pre-freeze dry-run over a stand-in head) | r39 E4: verification ref Y = J + receipt; run at J documented 7/8 | `--export-ref J` on the final head prints 7/8 with G2 receipt=0; `--export-ref Y` prints 8/8 |
| M39-2 | evidence-record | five r38 lane records state the C1 run/selftest are over the judged head; the receipt contradicts them | lesson :21, :94; SHONEN :185; LOG C1 bullet; SCORECARD row | none — corrections sweep this round (R2) | `Correction (round 39)` blocks appended to all five records | `grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md` >= 1 each |
| M39-3 | evidence-record | r38 report quotes tip run f06148c6 (8/8) with no committed transcript | report :37-38; commit grep 0 hits | none — R35 criterion added (committed transcript or report-only label) | r39 G3 scans round-39-added lines; receipt + reds committed at Y | a quoted run without transcript and without report-only label reds G3 |
| M39-4 | evidence-record | M38-5/M38-7 have `captured-by: none` and no QUALITY row cites them | QUALITY.md greps (0 hits); verifier R4 | none — R36 criterion added | R36 row cites M38-5 and M38-7 | `grep -cE 'M38-5|M38-7' corpus/QUALITY.md` >= 1 |

## Instrument attack findings (wave 2)

The 37-seat falsification wave re-opened the committed instrument and C2 artifacts. Findings and full receipts are in `.ufo/waves/round-39/wave2/`; they are not omitted from the round verdict:
- G2 accepts fabricated payload values because it validates the shape/digest of the receipt but does not compare recorded `G<n> payload=` values with a captured invocation. CritG2Exploit.md documents passing mutations; the receipt is not proof of its own payload.
- G6 is live-state dependent: its green result requires a quiescent `/fast/scratch/hyaku/kasegi-r39/` apart from the one tolerated work directory. Wave seats necessarily populate that path. CritC1Kill.md records default-root reds and isolated clean-clone success; the frozen bare command is therefore not an unconditional reproducible counter.
- The committed receipt's `run-utc=2026-10-26T21:35:00Z` post-dates its containing commit (`2026-10-26T20:12:12Z`), so its timestamp is false provenance. The final report uses only a run timestamp observed at execution.
- LOG.md's correction bullet failed the frozen `^Correction (round 39)` count (0); a standalone append was added without rewriting the earlier entry.
- The claimed SKILL.md r39 registry row was absent; the row is now appended. CritOverclaimScan.md records the before-state.

No predicate or kill rule was changed after scoring. C1's suite/selftests and C2's package checks have behavioral evidence, but the G2 receipt-value blind spot and G6 environment coupling prevent admitting C1 on the frozen counter alone. The round reports that uncertainty rather than treating the composed receipt as independent proof.
### Final measurement at integration head J1
Commit `3fa81ef5e7b558030903db71c3bb66cb0ea976a2` contains the round changes and wave-2 evidence. With only the single `gates-work` directory under the required scratch root, `bash corpus/instruments/r39-closure.sh --export-ref 3fa81ef5e7b558030903db71c3bb66cb0ea976a2 --work /fast/scratch/hyaku/kasegi-r39/gates-work` printed `G2 ... diff-clean=0 ... closed=0`, `G6 ... r39=empty ... closed=1`, and `closed=7/8 exit=1`. The same command with `--selftest` printed `G2 positive=fail`, the other seven cases positive=pass, and `selftest cases=8 failures=1`, exit 1. This is the observed J1 result, not an admitted C1 pass; the prior receipt's claimed Y pass is not promoted past the wave-2 attacks.

C2 on J1: frontier-row count → 22; registry-row count → 59; S057 citation count → 1; `python3 corpus/instruments/frontier-recheck-count.py` → `entries=25 pass=25 exit=0`; source-recheck S057 exit 0; capture binding `records=46 bound=46 unbound=0`; recheck audit `expected=51 missing=0 unexpected=0 exit=0`; knowledge count 51; source census exit 0 (W04 S028/S029 warnings only). Before values are frozen in `c2-controls/before.txt` and `census-before.txt`.
