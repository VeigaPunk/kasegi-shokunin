# Round-30 wave-1 spot-check findings

Axes: `depth:verifiability`, `coverage`.

## Behavior and evidence boundary

Collected non-author reviews available in the round-30 lane worktree and peer messages. This is a consolidation of their findings, not an independent rerun. Reports are cited by their exact available paths; where a requested current-round reviewer report was not produced, that is marked rather than substituted with an earlier-round result.

## Spot-check result

| item | gate decision | re-opened by | agree/disagree | reason |
|---|---|---|---|---|
| C1 instruments A1/A2/B1/B2 | Instrument conformance target (C1) | `RevC1Instrument-2` (`.ufo/waves/round-30/wave1/RevC1Instrument.md`) | **Conditional agree; C1 receipt blocked on B2 isolation** | A1/A2/B1 pass, and reviewer reports lane harness 17/17 plus all 37/37 real manifest rechecks pass at bound digests. B2 does not isolate: frozen fixture triggers `stem-mismatch` before occurrence logic; mutant-B2 still exits 1, so the `occurrence-not-unique` limb is not shown load-bearing. Reviewer recommends an appended claims correction, isolating fixture, and rerun. Instruments remain uncommitted; final digest binding is still owed. |
| C1 overall assessment | Instrument conformance target (C1) | `RevClaimsOverall` (`.ufo/waves/round-30/wave1/RevClaimsOverall.md`) and `RevC1Instrument-2` | **Disagreement in evidence state; latest reviewer evidence narrows prior gap** | RevClaimsOverall had not observed B2 or no-regression evidence at its snapshot and classified strict C1 as unproven. RevC1Instrument later reports the real-manifest regression sweep green, but independently confirms B2 mutant isolation fails. Preserve the blocking B2 finding and integration-time digest caveat. |
| F14 admission and C2 | Admit F14 with S046/S047/S041 | `RevClaimsOverall` (`.ufo/waves/round-30/wave1/RevClaimsOverall.md`); F14 entry reviewer report absent | **Disagree with C2 target achieved on measured bytes** | `RevClaimsOverall` measured zero S046/S047-citing entries, census exit 1 (E11 missing used-by paths), harness `entries=17 pass=16 exit=1` (missing F14 entry), and S047 source-recheck exit 1 (`occurrence-not-unique`). The report explicitly says its snapshot is a current working tree, not final integrated bytes. `RevC2Entry` did not have a round-30 assignment/report; its peer message summarized its round-29 F13 review only, so it is not evidence about F14. |
| S046/S047 registry additions and Registry changes log | Add two rows, no existing-row edits, complete R8 log | `RevC2Registry` (peer message; only prior report is `.ufo/waves/round-29/wave1/RevC2Registry.md`) | **Agree, for the registry evidence described** | Re-derivation reported 45 total rows at the prior registry snapshot, two new rows, no duplicate/malformed/enum violations, tier A, used-by paths, and complete old→new logging; frozen census exit 0 with disclosed W04 warnings. Round-30 `ExecRegistryAppend.md` reports 47 rows and census exit 0 after F14 entry landing. `RevClaimsOverall` measured census exit 1 earlier while that entry was absent; these are different snapshots. |
| S037 quarantine row (`payload-absent`) | Retain checked-ABSENT classification | `RevQuarantineInd` (`.ufo/waves/round-30/wave1/RevQuarantineInd.md`) | **Disagree** | Local capture `fetch/s037.html:431-446,461-474,517-527` contains the title, status and dates matching the cited quote. Reviewer cautions that capture digest/status was not measured; finding counters the absent classification for available captured evidence, not the historical original fetch. |
| S054 quarantine row (`payload-absent`) | Retain checked-ABSENT classification | `RevQuarantineInd` | **Disagree, qualified** | Fetched local PDF `fetch/s054.pdf:15` contains the exact Japanese quotation. Historical register status concerns an earlier payload not independently inspected; current capture makes the quote verifiable, so refresh/clear current quarantine status rather than infer fabrication. |
| S048 quarantine row (`NEVER CHECKED`) | Keep unreachable/unverified, not fabrication | `RevQuarantineInd` | **Agree** | `fetch/s048.html` is an HTTP 404 page, not the cited standard payload; it cannot verify a quote. |
| `program-scope-rules-and-asset-boundaries.md` staged candidate | Reject | `RevC2Entry` peer message, referring to its round-29 review | **Agree with refusal** | The reviewer found “Three different mechanisms, one invariant…” universalizes platform-specific policies without support, a Q4 attribution/generalization failure. This is supporting evidence about the staged candidate only, not a round-30 F14 entry review. |

## Boundaries and artifact paths

- Reviewed inputs: frozen round-30 `claims.json`, C1/C2 before receipts and census receipt; lane corpus/readme/quality/scorecard and prior lessons; read-only merge package and absent-defect register.
- Relevant round-30 evidence: `.ufo/waves/round-30/wave1/RevClaimsOverall.md`, `ExecImplFrontierHarness.md`, `ExecPostCommitRecheck.md`, `ExecRegistryAppend.md`, `RevQuarantineInd.md`, `ScoutQuarantineSlice.md`, `ScribeLessonGate.md`.
- Scope limit: no `RevC2Entry.md` or `RevC2Registry.md` round-30 report was available; the correspondingly named peer seats reported only round-29 ownership. C2 and entry-bar conclusions therefore remain tied to the stated report snapshots, not final integration.
- No product code or judge edited; no checks rerun; no tool installed; no network/live target contacted by this scribe. No writes outside the lane repo.
- Report path: `.ufo/waves/round-30/wave1/ScribeSpot.md`.
