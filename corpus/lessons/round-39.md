
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

## Instrument attack findings (wave 2) — routed to round 40
Wave 2 attacked the landed suite and the C2 artifacts after scoring; findings and verdicts land in `wave2/` receipts
and are routed to round 40 as fixtures/limbs (per the frozen-rule discipline: a rule changed after scoring is not
the claim's rule).
