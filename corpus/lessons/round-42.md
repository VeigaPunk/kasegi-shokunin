# Round 42 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `5053a7f46de35784cff4b56756906e9014a38276`; claims-freeze commit
`0566bd66e93d429b2df8b6751cf10cbdc391e79b` (`.ufo/waves/round-42/claims.json`). Judged head J = the lane
commit carrying every round-42 change except the receipt (the lane never names it); verification ref Y = J + the
receipt `.ufo/waves/round-42/final-gates/all-gates.txt` only. Lane files never name J by hash
(a commit cannot contain its own hash); the report names J and Y. Counting commands run over the suite run
at Y; negative controls run at base `5053a7f46de35784cff4b56756906e9014a38276` and round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`. Shape: two v1 waves; wave 1 `kasegi-r42-build` dispatched 64
seats (32–64 band), and wave 2 and the round total are counted from the wave-2 dispatch when it lands,
never estimated: wave 2 dispatched 36 seats; the round total is 100. Every wave carries connector seats this round (the D-r41-5 routed item):
wave 1 carries 2 (`ConnCrossClaims`, `ConnWave2Seed`); wave 2 carries 2.

Attack share: wave 1 `kasegi-r42-build` 21/64 = 32.8% (reviewer 8 + critic 8 + mutation-tester 5, counted
from the `wave1-dispatch.json` registry members, `counts.spawn` 64); wave 2 and the round total are counted
from the wave-2 dispatch when it lands: 36 seats, 32 attack roles.

## Frozen claims

Before → after, as frozen in `.ufo/waves/round-42/claims.json` (2026-10-28T12:05:00Z, KasegiR42).

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | suite absent — base export exits 127 and nothing prints `closed=13/13` (`c1-controls/do-nothing.txt`); the r41 suite at base prints `selftest cases=12 failures=8`, `closed=8/12 exit=1`, with I1's per-block evidence union and I3's mangled-token acceptance alive; routed queue open: I1 per-correction evidence, I3 token boundary, I7 bare-pipe/leading-whitespace, I5/I12 declaration completeness, I6 outside-configured-root stray, capture-binding missing-path/URL variants, frontier-counter status-flip blind spot (`corpus/lessons/round-41-verifier-spotcheck.md` §5 item 6); D-r41-1 duplicated `Correction (round 41)` blocks, D-r41-3 SKILL registry split table + duplicate `r40-closure.sh` row | `r42-closure.sh` landed export-mode only (plain run exits 2); `closed=13/13 exit=0` at Y; graded `selftest cases=13 failures=0` with both transcripts teed in the receipt; base and round-41-head exports each red (`closed<13/13 exit=1`); J1–J13 close the routed families, and every repaired check carries a replay limb that re-executes its committed defeat artifact against the current suite bytes and requires rejection |
| C2 | coverage (8, held) | frontier 24 (F25 absent); registry 63 (S064+ absent); entries citing S064+ 0; knowledge 60; harness `entries=27 pass=27`; binding `records=55 bound=55`; audit `expected=60`; census exit 0 (`W04 S028`/`W04 S029` only) — `c2-controls/before.txt` | frontier 25 (F25 admitted); registry 64+R (S064 mined, ≥1 screened reject S065+ with reason + flip); entry citing S064 1; knowledge 61; harness `entries=28 pass=28` incl `PASS F25`; binding 56/56; audit `expected=61`; census exit 0; measure 45/45 = 1.000 |

## Mistakes

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M42-1 | evidence-union (per-correction evidence not enforced) | the round-41 suite's I1 collected correction evidence as a cross-record union, so its own selftest fixture that removes one correction's named evidence still reported `evidence=3/3` and the check accepted it | `.ufo/waves/round-41/wave2/CritC1KillRule.md` and `RevC1Counters.md`: `selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0`; the r41 instrument collects evidence across records (lines 902–906); routed at `corpus/lessons/round-41-verifier-spotcheck.md` §5 item 6 | new round-42 QUALITY criterion (per-record verdicts: evidence claims are per-correction, never union aggregates; id Q-M42-1) | J1 (F-EVID): every record block's own `Correction (round N)` line set must name its evidence, with no cross-block union; J1's replay limb re-executes the committed `evidence-not-named` defeat and requires rejection | `selftest case=J1` must print `mutants=1/1 positive=pass ... verdict=pass`, and `check_j1` over the `evidence-not-named` fixture must print `closed=0`; the r41 I1 printed `rejected=0` with `evidence=3/3` on that same input |
| M42-2 | token-boundary (counted value matched as a substring, not a whole token) | the round-41 suite's I3 accepted a mangled tally: replacing a correction value with `closed=10/100` still satisfied the value-presence tally, so the check reported every record valid | `.ufo/waves/round-41/wave2/RevC1Counters.md` item 1 and `CritC1KillRule.md`: `selftest detail=I3 mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0` (mutant written at r41 instrument lines 1757–1759; value limb 438–459) | J2 (F-TOKEN) | J2 extracts every `closed=<n>/<m>`, `failures=<k>` and `cases=<k>` value as a whole token bounded by non-digit non-slash characters (word boundaries are not sufficient), and its replay limb re-executes the `mangled-value-token` defeat requiring rejection | `selftest case=J2` must print `mutants=1/1 ... verdict=pass`, and `check_j2` over `closed=10/100` must print `closed=0`; the r41 I3 printed `tally=3/3` on that input |
| M42-3 | replay-substrate (a replay limb mutated a line its check does not grade) | r42's J1 replay and J1 selftest mutant selected the first correction line whose evidence changed under stripping, across all rounds; `check_j1` grades only `Correction (round 42)` lines, so the strip landed on a round-39 line and the check accepted the mutated tree — C1 stayed red at the integration head with `replay=RevC1Counters.md=accepted` and `selftest case=J1 mutants=0/1` | `.ufo/waves/round-42/final-gates/all-gates.pre-repair.txt` (J1 line), `.ufo/waves/round-42/claims-erratum-4.md` E-R1 | the J1 selftest mutant limb itself: `mutants=0/1` on an otherwise-green check is a red, and the integration read of the selftest line must block the receipt until the mutant rejects | `graded_lines()` selects only the round-42 claim-bearing correction lines and requires the stripped line to lose every evidence id; replay and selftest mutant now share that one substrate | yes — the repaired limb prints `replay=RevC1Counters.md=rejected` and `mutants=1/1`, and the stripped fixture shows `evidence=1/2,missing=1,union=1` |
| M42-4 | self-reference (a check graded a payload computed after it, so its own baseline could never match) | J8's canonical transcript and J10's graded-line count were built from the live selftest lines, so their `payload-match` was structurally 0 in both modes and the frozen `selftest cases=13 failures=0` was unreachable | `.ufo/waves/round-42/final-gates/all-gates.pre-repair.txt` (J8/J10 selftest lines, `failures=4`), `.ufo/waves/round-42/claims-erratum-4.md` E-R4/E-R5 | a frozen after-state must be reachable by its own instrument: an all-green fixture has to print thirteen `verdict=pass` lines | `run_selftest` iterates to a fixed point planting J10/J8 payloads before grading; `line_ok` means a graded case line was emitted; J8 canonical mode grades a synthetic all-pass block while a committed receipt is still graded from its own bytes | yes — pre-repair `failures=3` with `payload-match=0` on J8/J10; post-repair `cases=13 failures=0`, and a receipt whose selftest block carries `verdict=fail` still reds J8 |
| M42-5 | wrong-absence (a declared dynamic artifact's absence counted as an escaping declaration) | `.ufo/waves/round-42/declared-blocks.txt` declares the receipt `dyn unpinned`; at J the receipt is legitimately absent, so J4 reported `valid=468,escape=1` and C1 could not close at J | `.ufo/waves/round-42/claims-erratum-4.md` E-R3; `.ufo/waves/round-42/final-gates/all-gates.pre-repair.txt` (J4 line) | J4's own declaration grammar: the `dyn` kind cell already means the run materialises the path | `check_j4` treats a `dyn` declaration as valid while still rejecting absolute paths, `..`, and paths resolving outside the export root | yes — J4 now prints `declared=469,valid=469,escape=0` at J and at Y, while an absolute or `..` entry still increments `escape` |

## Census

Before (`census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0. After
(`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`): `W04 S028`, `W04 S029`, `ok`, exit 0.
Registry 63 → 64+R rows: the appended block adds S064 (status mined, opened this round) and at least one
screened reject S065+ (status rejected, reason + flip); no existing row cell changes; `PROVINCE.md`,
`SKILL.md`, `SOURCES.md`, `corpus/README.md` and the search log receive appended blocks only.

## Gate

Landed by the round-42 C2 gate seat as `wave1/ScribeC2Gate.gate-block.txt`: the admitted
F25 / S064 block (registry row, source with URL and access date, capture and manifest, ≤25-word located
quotes, knowledge entry, frontier admission, limit) plus the recorded screened reject (S065+, reason +
flip, URL, access date, ≤25-word located quote — closes D-r41-2).

## Wave-2 falsification

Appended when the round-42 falsify wave reports: per-claim verdicts, attack tallies counted
from the wave-2 dispatch (never estimated), each routed family named with the J-check that reds it, and
each committed defeat artifact re-executed by its replay limb.

## Gate

### Admitted — F25 / S064 (CVE Record Format)

- **Lead screen (2026-10-28, three candidates).** Machine-readable vulnerability-data standards the lane
  does not hold were screened before any fetch: the OSV schema, the CVE Record Format bundled JSON
  Schema, and the NVD Vulnerability Data API 2.2.4 schema. Lane ground first — `grep -liE
  'osv|cve.?record.?format|cve.schema|CVE_Record|nvd'` over `corpus/SOURCES.md`, `corpus/README.md` and
  `corpus/knowledge/*.md` finds no row and no entry that captures any of the three documents; the only
  near hit is the S031 CNA Rules capture, which names "the CVE Record Format" as an approved format in
  seven places across §4.5.5 and §5.1-§5.2 (`corpus/source-snapshots/round-23/S031.txt:L102-L116`)
  without the format document itself. Sibling ground over
  every `/home/vgpnk/Projects/shokunin/*-shokunin` corpus: no hit for `cve-schema` or
  `CVE_Record_Format`; kaidoku's S015 holds one OSV *record instance*
  (`api.osv.dev/v1/vulns/CVE-2025-55305`, dataset), adjacent to the OSV schema but not the schema
  document. Pick = CVE Record Format: it is the canonical record standard (the NVD schema is one
  consumer's NVD-enriched projection of it, and the OSV schema is a different record format whose family
  kaidoku has begun reading), it is primary first-party (`CVEProject/cve-schema`), and its normative
  artifact is the bundled JSON Schema itself.
- **Row.** S064, kind spec, tier A, status mined, opened 2026-10-28, recheck on-release, used-by
  `corpus/knowledge/cve-json-record-format.md`; row deliverable
  `wave1/ExecC2Rows.registry-rows.txt`.
- **Source / capture.** `https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json`;
  access 2026-10-28 (fetched 2026-10-28T11:06:45Z, HTTP 200, 133616 raw bytes, raw sha256
  `44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f`). Capture
  `corpus/source-snapshots/round-42/S064.txt` is the complete document, no slice — capture line k is
  document line k — normalized by `corpus/instruments/capture-source.py --kind text` (CRLF/CR to LF,
  space/tab/NBSP runs collapsed, lines trimmed, blank lines dropped, UTF-8, final newline): 3545 lines,
  84520 B, sha256 `b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa`.
- **Quotes (≤25 words, located in the capture).** L5 (18 words): "cve-schema specifies the CVE JSON
  record format. This is the blueprint for a rich set of JSON data" — the bundled schema's own
  top-level description: the CVE Record is the unit CNAs and ADPs submit. L3466 (15 words): "When a CNA
  populates the data associated with a CVE ID as a CVE Record" — the `Published` branch of the
  top-level `oneOf` (title at L3465), whose object requires `dataType`, `dataVersion`, `cveMetadata`
  and `containers` (L3500-L3505) and whose `containers` requires `cna` while `adp` stays optional
  (L3478-L3498). L3510 (18 words): "A Rejected CVE Record remains on the CVE List so that users can
  know when it is invalid." — the `Rejected` branch (title at L3509): rejection is a state of the same
  record, not its deletion, which is what makes invalidation observable to a consumer.
- **Entry.** `corpus/knowledge/cve-json-record-format.md` (`source: S064`,
  `verified-at: 2026-10-28`, `ground: F25`, executable `recheck:`), its limbs anchored to L5, L3466 and
  L3510 above plus the container rule (`cna` required, `adp` optional) and the two-state root; it
  separates record shape (this format) from assignment policy (F07 / the S031 CNA Rules, which governs
  who may assign an ID) and from the consumption-side formats the lane already holds (S055 CSAF v2.0,
  S060 CycloneDX analysis subtree).
- **Frontier admission.** F25 row + coverage-map row + `PROVINCE.md` `[r42 Frontier amendment]` appended
  (deliverables `wave1/ExecC2Rows.readme-row.txt`, `wave1/ExecC2Rows.province-amendment.txt`) puts the
  frontier at 24 -> 25 rows, F25/25 admitted.
- **Limit.** The capture is the schema artifact, not the CVE Program's prose specification: `required`
  arrays and the two-branch `oneOf` constrain the shape of an instance, but no line in it states who may
  assign an ID or when a record should be rejected. Its normative force is JSON Schema draft-07
  (`$schema`, L2) over a moving raw `main` ref pinned only by the raw sha256 above; the `$id` (L3)
  names the rendered `cveproject.github.io` copy, which can drift from the captured bytes, and a new
  bundled version would change the document without changing the URL, so the on-release recheck must
  compare hashes rather than fetch success. The row's "5.x" label rests on the schema's own
  `dataVersion` pattern (`^5\.(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))?$`, L482) and its `default` `5.2.0`
  (L483), not on a published version of record in the capture; errata and version history sit outside
  it.

### Rejected — the screened floor (closes D-r41-2)

- **S065 (OSV schema — Open Source Vulnerability format, v1.9.2)** —
  `https://ossf.github.io/osv-schema/`; access 2026-10-28 (fetched 2026-10-28T11:06:45Z, HTTP 200,
  228890 bytes, sha256 `8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8`). Located
  quote (14 words; "Purpose", opening sentence, L9-L10 of the page normalized by
  `capture-source.py --kind text`): "This document defines a standard interchange format for describing
  vulnerabilities in open source packages." REJECTED: primary and normative, but the OSV document family
  is already named in the sibling ground (kaidoku S015 holds an OSV record instance, so that lane has
  begun reading the format), and its canonical artifact is an HTML page describing a schema published
  elsewhere, whereas the picked document's normative artifact is the bundle itself; for one frontier
  slot the disjoint, directly verifiable document wins. Flip: re-open if S064's row or the F25 entry is
  withdrawn, or if a frontier needs OSV-specific range semantics (`affected[].ranges[].events`,
  `database_specific.extracted_events`) that the CVE format cannot express.
- **S066 (NVD Vulnerability Data API 2.2.4 schema)** —
  `https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema`; access 2026-10-28 (fetched
  2026-10-28T11:08:16Z, HTTP 200, 10394 bytes, sha256
  `2b9c4e8ab7e6e42aa17ea787f58167beff47c119c6f291405f86ac19c6149e01`). Located quote (9 words; served
  L96, the `metrics.description` field): "Metric scores for a vulnerability as found on NVD." REJECTED:
  this schema specifies one downstream consumer's API response shape — its own title reads "JSON Schema
  for NVD Vulnerability Data API version 2.2.4" — and carries NVD-only keys (`evaluatorComment`,
  `evaluatorSolution`, `evaluatorImpact`, `cisa*`), so it is a derived, NVD-enriched projection of the
  CVE record, not the canonical record standard; the same document family's canonical artifact is the
  picked S064 bundle. Flip: re-open if a frontier targets NVD-specific enrichment (`vulnStatus`,
  `evaluator*`, `cisa*`, NVD-side metrics or weaknesses) or the API interface contract
  (`resultsPerPage`/`startIndex` pagination) that the CVE format does not carry.
- Screened and dropped without a row: the GHSA unauthenticated advisory API doc (sibling mori S012
  already holds a GitHub Security Advisory page, so the family is adjacent in sibling ground and weaker
  on disjointness than both fetched finalists) and FIRST VIN (no standalone normative document found;
  not fetched).

The round-41 Gate recorded no reject, so the outside spot-check had nothing to sample (D-r41-2). This
block records two, each with URL, 2026-10-28 access date, a located ≤25-word quote, an honest reason on
a named criterion, and a flip condition.
