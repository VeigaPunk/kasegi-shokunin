# kasegi — round 36 report — DRAFT skeleton (ScribeReportDraft receipt)

Lane: `kasegi-shokunin` (bounty & security research). Axes owned: depth:verifiability (4),
coverage (7), depth:density (9). Lane base `cc692008b0cfd58d18275aa6c4aed79620120799`;
claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (`claims.json` sha256 `a6405e71…`,
frozen 2026-10-26T15:33:19Z, attempt 1).

Draft status: **skeleton**. Values are filled from the frozen claims, from read-only measurements at
the claims-freeze tree and the named exports (`cc69200…`, `3266c99…`, `0aee0ef…`), and from the
wave-1 receipts that had landed when this draft was written (`.ufo/waves/round-36/wave1/*.md`). Every
value that exists only at the round-36 final lane head is marked `[MEASURE: …]` for the L1 to replace
after measurement. Copy from "## Work performed" onward into `.ufo/reports/round-36/kasegi.md`,
supply the title, and commit the report **after** the final lane commit (M36-4: the report lands
last). This is L1-owned Shokunin evidence, not a canonical Rust verdict.

- Seats whose receipts back the filled values: `ExecC1SuiteBuild`, `ExecC1BaseFail`, `ExecC1Fixtures`,
  `ExecC2Capture`, `ExecC2QuoteOnce`, `ExecC2JunkControl`, `MutJunkTwin`, `ExecManifestChecks`,
  `ExecCensusReplay`, `ExecRegressionBase`, `ExecInstrumentsSynopsis`, `ExecAncestry`, `ExecDatawalk`,
  `ExecQuiescenceProbe`, `ExecScoreGap`, `ExecGateReviewPrep`, `ScoutF19Open`,
  `ScoutCaptureAvailability`, `ScoutF19Sibling`, `ExecSiblingSweep`, `ScoutIdCollisions`,
  `ScoutQuarantine`, `ScoutStandingRefusals`, `CritMotivation`, `CritC1Export`, `CritC2Kill`,
  `CritC2Claim`, `RevC1Suite`, `RevClaimsFreeze`, `RevSourceRecheck`, `RevEntryF19`, `RevRowS053`,
  `RevSpotCheckReadiness`, `ConnSibling`, `ScribeEntryF19`, `ScribeRowS053`, `ScribeScorecard`,
  `ScribeShonen`, `ScribeMistakes`, `ScribeQualityRows`, `ScribeSOURCSCorrection`,
  `ScribeConsiderthese`, `ScribeAssimilationGate`, `ScribeLOG`, `SimplC1`.
- Still in flight at this draft, so their deltas stay `[MEASURE]`: `ExecC1ExportMode`, the remaining
  `RevC1*`/`MutC1*`/`MutC2*`/`CritC1Kill` receipts, `SimplReport`, `ScribeGateLesson`, `RevNoHarm`,
  `RevHarnessSync`, `Sent*`, and the final `wave1-results.json`.
- Heading check: `grep -c '^## SHONEN'` = 1 (this is the only heading that names it).

## Work performed

The round declares **two claims**, frozen before dispatch in `.ufo/waves/round-36/claims.json`
(attempt 1; base `cc69200…`, claims-freeze commit `b47f2cdf…`, with frozen before-controls
`c1-controls/before.txt` `14213f1a…`, `c2-controls/before.txt` `802091d7…` and `census-before.txt`
`920e6fd4…`). The saturation line is 9/10 per owned axis, window N = 3; the lowest non-retired axis
is depth:verifiability (4). This round works the two lowest axes and restates density as no-harm.

- **C1 — depth:verifiability (score 4, held).** The committed instrument
  `corpus/instruments/r36-closure.sh` runs nine checks E1–E9 over a `git archive` export of a named
  lane head (`--export-ref <hash>`, export mode only; a plain run is refused with exit 2) and prints
  `closed=9/9 exit=0` on the round-36 final lane head and `cases=9 failures=0` under `--selftest`.
  Its discriminators, measured with the drafted suite (`ExecC1BaseFail`): the round-35 base export
  `3266c9937b03062d9bbc2f436e20820115ed179c` reads `closed=0/9 exit=1` (all nine open) and the
  round-35 judged head `0aee0ef105395a2f1d6ace7eaeef13871bb26988` reads `closed=4/9 exit=1`
  (E1/E3/E4/E8/E9 open). The checks close the round-35 verifier spot-check's routed defects
  (`§5.1`–`§5.6`, `corpus/lessons/round-35-verifier-spotcheck.md`) and the standing closure-order
  defects: **E1** structural placeholder/hash binding (no `filled by the L1` / `<LANE_HASH>` tokens;
  the Final lane commit line's hash exists and is an ancestor of the exported ref); **E2** round-34
  depth:density erratum present; **E3** `SKILL.md` Gates & probes registry rows for the exact
  basenames `r35-defect-closure.sh` **and** `r36-closure.sh` (the near-name `r-defect-closure.sh` row
  does not satisfy it); **E4** round-35 `wave1-results.json` tracked with its provenance note (both
  limbs: the ref and the index; the note limb `.ufo/waves/round-35/wave1-results.json.provenance.md`
  reads 0 at the freeze and is **owed as an L1 landing** — no wave seat owns it); **E5** `claims-erratum-d5.md` present; **E6** `L1Integration.md` carries
  `Correction (round 35)` (path derived from the export, fixture copies excluded); **E7** `QUALITY.md`
  supersedes-R22/R23 rows present; **E8** the false-evidence-line correction recorded in the
  round-36 lesson; **E9** quiescence (lane `git status --porcelain` empty; no leftover
  `$HYAKU_SCRATCH/kasegi-r36` seat dirs; HEAD equals the exported ref).
- **C2 — coverage (score 7, held).** Frontier F19 (FIRST EPSS — exploitation-likelihood scoring
  distinct from CVSS severity and from KEV catalog status) admitted 18 → 19; registry row S053 added
  (kind `docs`, tier A scoped to FIRST's own EPSS statements, status `mined`, opened 2026-10-26,
  recheck `90d`); knowledge entry `corpus/knowledge/epss-exploit-prediction-scoring.md` cites
  `source: S053`; harness `entries=22 pass=22 exit=0` incl. `PASS F19 ids=S053`; `source-recheck.py
  --source S053` exit 0; census exit 0 (W04 S028/S029 only); `corpus/knowledge/*.md` 47 → 48; the
  junk twin `c2-controls/junk-f19.md` is rejected by the counter it was built to fool (measured:
  fabricated sentence absent, `quote-not-found`, exit 1).

**Wave.** One v2 wave `kasegi-r36-build`, 64 seats (`spawn 64 / resume 0`), dispatched through the
inline spawn handoff (`wave1.ready`, L1 `KasegiR36`, hyaku-inline attempt 1): executor 18, scribe 12,
reviewer 10, scout 6, mutation-tester 5, critic 6, connector 3, sentinel 2, simplifier 2 — attack
share 21/64 = 32.8 % (reviewers + critics + mutation-testers). The planner seat is the L1
(orchestrator ruling 2026-10-19), so it is not a wave member. Receipts land under
`.ufo/waves/round-36/wave1/`; `wave1-results.json` is the dispatcher's and finalizes after the wave
settles `[MEASURE: results path, entry count, seats with final output]`. `[MEASURE: dead seats at
wrap]`.

**Work items by area** (receipts under `.ufo/waves/round-36/wave1/`):

- **C1 build** — `ExecC1SuiteBuild` (`r36-closure.sh`), `ExecC1Fixtures` (per-check red/green
  fixtures generated per selftest case under `--work`; **no committed fixture corpus** —
  `ExecC1SuiteBuild` deviation 3), `ExecC1ExportMode` (export-mode discipline), `ExecC1BaseFail`
  (base/judged-head failure), `ExecQuiescenceProbe` (E9 red/green), `ExecAncestry` (E1
  existence/ancestry table over the SCORECARD hashes).
- **C1 attack/review** — `RevC1Suite`, `RevC1Fixtures`, `RevC1Selftest` (summary-only forgery
  rejected), `MutC1Suite`, `MutC1Fixtures`, `CritC1Kill`, `CritC1Export`, `ExecRegressionBase`
  (before-controls replay: c1 7/7 MATCH with two derived keys, c2 6/7 MATCH with `junk_present` the
  one DIFF), `ExecDatawalk` (spot-check §5.1–§5.6 open/closed matrix),
  `ExecInstrumentsSynopsis` (26 instrument runs, all exit 0 — no-harm baseline), `CritMotivation`
  (do-nothing base control), `SimplC1`, `ExecGateReviewPrep` (`r36-post-integration-gate.sh`).
- **C2 build** — `ExecC2Capture` (S053 capture + round-36 manifest), `ScribeEntryF19` (entry),
  `ScribeRowS053` (row + search-log bullet + Paths line), `ScribeSOURCSCorrection` (R9 correction for
  the round-35 S052 search-log bullet), `ExecC2Harness` (`knowledge-expected.txt` 48 + harness sync),
  `ExecCensusReplay`, `ExecManifestChecks`, `ExecC2QuoteOnce`, `ExecC2JunkControl` (junk twin +
  discriminating invocation), `ExecScoreGap`.
- **C2 attack/review** — `RevEntryF19` (Q1–Q10), `RevRowS053`, `RevSourceRecheck`, `RevHarnessSync`,
  `MutC2Entry`, `MutC2Row`, `MutJunkTwin`, `CritC2Kill`, `CritC2Claim`, `ScoutF19Open` (live re-open),
  `ScoutCaptureAvailability`, `ScoutF19Sibling`, `ExecSiblingSweep`, `ConnSibling`, `ConnC1C2`,
  `ConnPatterns`.
- **Non-claim frontier items** — assimilation: `ScoutQuarantine`, `ScoutIdCollisions`,
  `ScoutStandingRefusals`, `ScribeAssimilationGate`; considerthese: `ScribeConsiderthese`; mistakes:
  `ScribeMistakes`; QUALITY rows: `ScribeQualityRows`; scope/credential: `SentScope`, `SentSecrets`,
  `CritBoundary`, `SimplReport`.
- **Round record** — `ScribeGateLesson`, `ScribeScorecard`, `ScribeShonen`, `ScribeLOG`, `ScribeLOG`'s
  entry draft (15 lines / 9,541 B, appended at `LOG.md` EOF after `## Round 35` at `:1651`),
  `ScribeReportDraft`.

## Landed changes

Every change below is tied to the round-36 `LOG.md` entry (heading `## Round 36`, appended in
`[MEASURE: commit]`; draft text at `.ufo/waves/round-36/wave1/ScribeLOG.md` §7) and to the commits
named. The report commit follows the final lane commit (M36-4 fix: one landing order, report last).

| Change | Commit |
|---|---|
| Claims freeze: `claims.json`, `census-before.txt`, `c1-controls/before.txt`, `c2-controls/before.txt` | `b47f2cdf` |
| Wave spec/dispatch: `build-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`, `wave1.ready` | `[MEASURE: commit carrying the wave spec/dispatch]` |
| C1 counter `corpus/instruments/r36-closure.sh` (draft `ff616adc…`, 737 lines / 28,980 B); per-check fixtures are **generated per selftest case under `--work`**, not a committed corpus (`ExecC1SuiteBuild` deviation 3) | `[MEASURE: commit]` |
| E1/E3: SCORECARD round-36 section with no placeholder tokens and **no self-referential lane-commit line** (`ScribeScorecard` F2 — E1's binding is carried by the two existing round-33/34 `Final lane commit:` blocks, both hashes exist and are ancestors); `SKILL.md` Gates & probes registry rows for the exact basenames `r35-defect-closure.sh` and `r36-closure.sh` | `[MEASURE: commit]` |
| E4: `.ufo/waves/round-35/wave1-results.json.provenance.md` beside the tracked results file (mirror of the round-34 note, 5,639 B), closing the note limb that reads 0 at the freeze — **owed L1 landing, no wave seat owns it** | `[MEASURE: commit/path/sha]` |
| E2/E5/E6/E7 (held closed, re-verified): round-34 depth:density erratum; `claims-erratum-d5.md`; `L1Integration.md` `Correction (round 35)`; `QUALITY.md` supersedes-R22/R23 rows | `[MEASURE: commit]` |
| E8/E9: `corpus/lessons/round-36.md` (E8 false-evidence-line correction + `## Mistakes` M36-1…M36-4, drafted at `wave1/ScribeMistakes.md`) and the quiescence gate (drafted at `wave1/ExecQuiescenceProbe.md`, reusable script `wave1/ExecGateReviewPrep.md`) | `[MEASURE: commit]` |
| QUALITY R28/R29 rows (quiescence/head-closure; exact-basename registration), end-of-file append | `[MEASURE: commit]` |
| C2: `corpus/knowledge/epss-exploit-prediction-scoring.md`; `corpus/SOURCES.md` S053 row + round-36 search-log bullet + appended R9 S052-search-log correction; `corpus/README.md` F19 row; `corpus/source-snapshots/round-36/{S053.txt,manifest.json}`; `corpus/instruments/knowledge-expected.txt` 47 → 48 | `[MEASURE: commit]` |
| PROVINCE frontier amendments: F18 (owed from round 35) and F19, end-of-file append per R6 | `[MEASURE: commit]` |
| Round close: SCORECARD round-36 section, SHONEN append, `corpus/lessons/round-36.md`, `LOG.md` `## Round 36`, wave receipts, `[MEASURE: wave1-results.json]` | `[MEASURE: final lane commit]` |

No existing line of `SKILL.md`, `PROVINCE.md`, `corpus/SOURCES.md`, `corpus/README.md`,
`corpus/QUALITY.md`, `SCORECARD.md`, `SHONEN.md` or `LOG.md` is rewritten; landings are appends and
the placeholder substitutions E1 requires `[MEASURE: RevNoHarm verdict on the export diff]`.

## Before → after measurements

Measured commits: **before** — claims freeze `b47f2cd…` (and the exports `cc69200…`, `3266c99…`,
`0aee0ef…` for the controls); **after** — `[MEASURE: final lane commit]`.

### C1 — depth:verifiability (nine closure checks over a named export)

Frozen before-controls (`c1-controls/before.txt`, at `b47f2cd`): `suite_missing=1`,
`placeholder_filled=0`, `placeholder_angle=0`, `r36_registry=0`, `r35_registry=0`,
`scratch_leftovers=0`, `worktree_clean=0`. `ExecRegressionBase` replayed the controls on the base
export and reports **c1 7/7 MATCH** (two of them labelled *derived*: `worktree_clean`,
`scratch_leftovers`) and **c2 6/7 MATCH, 1 DIFF** (`junk_present=1` is not reproducible from committed
base bytes), with the scope caveats the suite must honour: `<LANE_HASH>` is 0 only under the
`SCORECARD.md` scope (repo-wide it is 502 lines/89 files), `r-defect-closure` is 4 lines (one registry
row + three prose), and `worktree_clean` / `scratch_leftovers` are live readings, not properties of a
past commit. `RevClaimsFreeze` re-ran every literal in the predicates and kill rules against the base
tree: **24/24 satisfiable**, zero constants contradict the base tree, and the freeze discriminates (a
do-nothing lane fails C1 on the missing suite and C2 on at least five independent arms) — verdict
**freeze OK**; E8, E9 and every `closed=…` run are filing-time targets over a head that does not exist
at freeze.

| Counter (frozen command) | Before | After |
|---|---|---|
| `bash corpus/instruments/r36-closure.sh --export-ref <final-lane-hash>` | suite absent (`ls_exit=2`) | `closed=9/9 exit=0` `[MEASURE: output]` |
| same, `--export-ref 3266c9937b03062d9bbc2f436e20820115ed179c` | suite absent | **`closed=0/9 exit=1`, all nine open** (drafted suite, `ExecC1BaseFail` Case 1) |
| same, `--export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988` | suite absent | **`closed=4/9 exit=1`**, open E1/E3/E4/E8/E9 (drafted suite, Case 2) |
| `bash corpus/instruments/r36-closure.sh --selftest` | suite absent | draft measured **`selftest cases=9 failures=0`** (`ExecC1Fixtures`, on the fixture green tree: controls E9b/E4b each reopen one limb, three forged reports rejected); an earlier suite-build revision read `failures=4`. The landing must keep `cases=9 failures=0` **and** land the review's HIGH repairs `[MEASURE: landed revision]` |
| `grep -c 'filled by the L1' SCORECARD.md` | 0 (freeze) / 1 (r35 base `:1240`) / 1 (r35 judged `:1271`) | 0 `[MEASURE]` |
| `grep -c '<LANE_HASH>' SCORECARD.md` | 0 | 0 `[MEASURE]` |
| Final-lane-commit binding (hash exists + ancestor of exported ref) | no round-36 line; the two older label blocks name 4 hashes, all ancestors | no new line (`ScribeScorecard` F2 — a section cannot cite its own commit); the two existing blocks stay bound, 8/8 exist and are ancestors, placeholders 0 → E1 closes `[MEASURE: suite E1 payload]` |
| E2 limbs (`erratum-row`, `erratum-mean`) | 0 / 0 (r35 base); 1 / 3 (r35 judged); 1 / 6 (freeze) | present `[MEASURE]` |
| `grep -cF 'r35-defect-closure.sh' SKILL.md` (E3) | 0 | 1 exact-basename row `[MEASURE]` |
| `grep -cF 'r36-closure.sh' SKILL.md` (E3) | 0 | 1 `[MEASURE]` |
| E4 `tracked-ref` / `tracked-index` / `provenance-note` | 0 / 1 / 0 (r35 base); 0 / 1 / 0 (r35 judged); 1 / 1 / 0 (freeze) | 1 / 1 / 1 `[MEASURE]` |
| `.ufo/waves/round-35/claims-erratum-d5.md` (E5) | 0 (r35 base); 1 (r35 judged / freeze) | 1 `[MEASURE]` |
| `Correction (round 35)` in the path-pinned `L1Integration.md` (E6) | 0 (r35 base); 1 (r35 judged / freeze) | 1 `[MEASURE]` |
| `supersedes R22` / `supersedes R23` in `corpus/QUALITY.md` (E7) | 0 / 0 (r35 base); 1 / 1 (r35 judged / freeze) | 1 / 1 `[MEASURE]` |
| E8 `m36-rows` / `stale-line` | 0 / 0 (r35 base); 0 / 1 (r35 judged); 0 / 0 (freeze — the line was deleted, not corrected) | ≥1 / 0 `[MEASURE]` |
| E9 `status-dirty` / `scratch-seat-dirs` / `head-match` | 9 / 0 / 0 (r35 base run); 9 / 40–48 / 0 while this wave ran | 0 / 0 / 1 at filing `[MEASURE]` |

E-limb matrix over the three named trees (literals re-measured by this seat with `git show
<ref>:<path>`; suite verdicts from the drafted suite, `ExecC1BaseFail`):

| limb | r35 base `3266c99` | r35 judged head `0aee0ef` | freeze `b47f2cd` | final head |
|---|---|---|---|---|
| E1 placeholders / lane-hash markers / bound commits | 1 / 0 / 2 → open | 1 / 0 / 3 → open | 0 / 0 / 2 | `[MEASURE: 0 / 0 / n, all ancestors]` |
| E2 erratum-row / mean | 0 / 0 → open | 1 / 3 → closed | 1 / 6 | `[MEASURE: closed]` |
| E3 `r35-defect-closure.sh` / `r36-closure.sh` | 0 / 0 → open | 0 / 0 → open | 0 / 0 | `[MEASURE: 1 / 1]` |
| E4 tracked-ref / tracked-index / provenance | 0 / 1 / 0 → open | 0 / 1 / 0 → open | 1 / 1 / 0 | `[MEASURE: 1 / 1 / 1]` |
| E5 `claims-erratum-d5.md` | 0 → open | 1 → closed | 1 | `[MEASURE: 1]` |
| E6 path-pinned `Correction (round 35)` | 0 → open | 1 → closed | 1 | `[MEASURE: 1]` |
| E7 `supersedes R22` / `R23` | 0 / 0 → open | 1 / 1 → closed | 1 / 1 | `[MEASURE]` |
| E8 m36-rows / stale-line | 0 / 0 → open | 0 / 1 → open | 0 / 0 → open | `[MEASURE: ≥1 / 0]` |
| E9 status-dirty / scratch dirs / head-match | 9 / 0 / 0 → open | 9 / 40–48 / 0 → open | dirty (wave artifacts) | `[MEASURE: 0 / 0 / 1]` |
| suite verdict | **closed=0/9 exit=1** (measured) | **closed=4/9 exit=1** (measured) | not run (suite lands this round) | `[MEASURE: closed=9/9]` |

Why the checks are structural rather than file-wide literal greps (`ExecRegressionBase` F1–F6): E1
must be `SCORECARD.md`- and label-scoped and match the sibling spelling `the L1 fills this line`; E2
alone is vacuous (`201.2` already counts 6 at base) and binds the erratum heading plus the
`201.7`→`201.2` pair; the Final-lane-commit hash is the first 40-hex run at/after the label (older
label blocks carry other hashes inline); E6 is path-pinned because `Correction (round 35)` appears in
9 `L1Integration.md` files at base (the real one plus 8 under `corpus/instruments/r35-fixtures/`); E4
is a single-limb gain (tracked 1, note 0); E9's keys are filing-time reads. Do-nothing control
(`CritMotivation`): at BASE E1 and E2 already pass while E3 and E4 fail, so neither claim's
after-state is reachable by a do-nothing round.

Recorded limits, not filed as passes. (0) **Suite review posture, verbatim for the canonical judge.**
`RevC1Suite` verdict on the 737-line draft (`bash -n` exit 0): **"REFUSE (repair-then-admit)"** — two
HIGH defects sit on the routed defect this round exists to close: `check_e3` greps `SKILL.md`
file-wide for both basenames instead of testing the registry rows, and `check_e7` greps
`corpus/QUALITY.md` file-wide for `supersedes R22`/`R23` where the frozen claim says rows, so a prose
quote or mention can satisfy either; one MED defect has `check_e4` read the live lane index
(`git ls-files`) inside an export-only suite; a further defect has E9 pass vacuously when the scratch
root is missing. The suite is therefore **not admitted yet**; the repairs plus a re-review are
`[MEASURE: landed suite sha256, re-review verdict]`. (1) `SCORECARD.md:613` cites the round-28 dispatch commit with a
dropped hex digit (`94f387cbe…` has no such object), so the claim's literal whole-file tokenisation
yields 9 non-existent tokens; scoped to the final-lane-commit paragraphs the set is 8/8 exists and
8/8 ancestors (`ExecAncestry` §6 F1) — `[MEASURE: whether the L1 corrects line 613 or declares it
exempt]`. (2) E8, as drafted, binds `m36-rows>=1` plus `stale-line==0`; that is a presence test on
the mistakes block, not a test that the correction sentence is truthful `[MEASURE: CritC1Kill
residue]`. (3) `c2-controls/before.txt`'s `junk_present=1` is not a base property (`ExecRegressionBase`
F6): the round-36 twin is absent at base, so the value is either lineage-scoped or was read from an
uncommitted tree; pin the definition when the control is scored. (4) E9's gate was implemented and
proved able to fail before the suite bound it (`ExecQuiescenceProbe`): `shellcheck -S warning` clean,
its own `selftest cases=11 failures=0 exit=0`, red on a fake dirty tree and on a fake leftover seat
dir, green on a clean state, and **exit 2 rather than a green `0/0`** when it cannot bind HEAD to the
export or the scratch root to the frozen absolute path. (5) Export-mode attack surface
(`CritC1Export`), recorded as limits on the provenance of a passing run: supplying `--lane` and
`--scratch-root` lets a forged repo print `closed=9/9` and the header shows only `export-ref=`, not
`lane=`, so the pasted output is indistinguishable from an honest run; `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_ALTERNATE_OBJECT_DIRECTORIES`/`GIT_INDEX_FILE` forge the git limbs (only E9's `head-match` catches
the env vector); `export-ignore` in `.git/info/attributes` can drop a measured file and flip E8's
absence limb to closed on an unchanged ref; and a committed symlink at a measured path is followed
outside the export. A green `closed=9/9` therefore attests to the invocation that produced it, and the
report does not present it as a proof against a hostile runner `[MEASURE: whether the smallest safe
corrections land]`.

### C2 — coverage (F19 / S053)

Frozen before-controls (`c2-controls/before.txt`, at `b47f2cd`): `frontier=18`, `registry_rows=52`,
`s053_rows=0`, `entries_citing=0`, `knowledge_entries=47`, `harness=entries=21 pass=21 exit=0`,
`junk_present=1`.

| Counter (frozen command) | Before | After |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 18 (F01–F18) | **19** (F19 row `[MEASURE: line]`) |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 52 (S001–S052) | **53** `[MEASURE: line; malformed=0]` |
| `grep -cE '^\|[[:space:]]*S053[[:space:]]*\|' corpus/SOURCES.md` | 0 | **1** |
| `grep -rlE '^source: S053 ' corpus/knowledge \| wc -l` | 0 | **1** |
| `python3 corpus/instruments/frontier-recheck-count.py` | `entries=21 pass=21 exit=0` | **`entries=22 pass=22 exit=0`** incl. `PASS F19 knowledge/epss-exploit-prediction-scoring.md ids=S053` `[MEASURE: output]` |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` | manifest absent → exit 2 (`manifest UNAVAILABLE reason=missing`, fail-closed) | `S053:sha256 OK`; `Q1..Q4 OK occurrences=1 anchor=N-ok`; exit 0 (measured against the scratch manifest at `ExecC2QuoteOnce`; `MutJunkTwin` reproduced it twice) `[MEASURE: landed run]` |
| `python3 corpus/instruments/capture-binding-check.py` | `records=42 bound=42 unbound=0 exit=0` (no round-36 record) | the round-36 record binds: expected **lane-root** run `records=43 bound=43 unbound=0 exit=0` (42 before + the round-36 record; a fixture root carrying only that manifest reads `records=1 bound=1`) `[MEASURE: landed]` |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, exactly two `W04` lines S028 + S029 (two runs byte-identical, `ExecCensusReplay`) | exit 0, same two W04 rows `[MEASURE]` |
| `ls corpus/knowledge/*.md \| wc -l` | 47 | **48** |
| `python3 corpus/instruments/recheck-audit.py` | `strict pass=47/47`, `expected=47 missing=0 unexpected=0 exit=0` | `strict pass=48/48`, `expected=48 missing=0 unexpected=0 exit=0` `[MEASURE]` |
| junk twin `c2-controls/junk-f19.md` | control not admitted; fabricated sentence `grep -cF` = 0 in `S053.txt` (`grep` exit 1), `normalized_occurrences=0` | **rejected, measured**: `S053:J1 MISMATCH reason=quote-not-found`, exit 1; the wrong-source variant (`--source S052` against the real quote) also `quote-not-found` exit 1; the real entry is the only construction that passes (exit 0, reproduced twice) (`ExecC2JunkControl`, `MutJunkTwin`) |

Capture: `corpus/source-snapshots/round-36/S053.txt` — `https://www.first.org/epss/` (the slashless
form 301s; the registry row and manifest URL carry the trailing slash), HTTP 200, `text/html;
charset=UTF-8`, no redirect, served body 26,804 B, `last-modified` 2026-07-30, `fetched_utc`
2026-10-26T15:35:10Z; normalized snapshot **8,448 B / 244 lines / sha256
`4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`**. Manifest
`corpus/source-snapshots/round-36/manifest.json` sha256
`f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3`, one record keyed `sources` (a
`records` key exits 2 as `manifest-shape`); on a fixture root carrying only that record and the
bare-URL row it reads `records=1 bound=1 unbound=0`, while the frozen lane-root command is the
42 → 43-record run expected after integration.
Live re-open `ScoutF19Open` (2026-10-26T15:36:36Z): HTTP 200, raw body sha256
`66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868` — byte-identical to the capture's
raw body (`cmp` equal); content differences 0 (the 173 diff-lines against `S053.txt` are line
segmentation only; whitespace-stripped texts are byte-identical). UA independence confirmed by
`ScoutCaptureAvailability` (plain curl, urllib default, instrument UA and short UA: all 200, all the
same 26,804 B / same sha256). Quote anchoring (`ExecC2QuoteOnce`): four pins, each `grep -cF` = 1 and
true occurrences = 1, anchors 216 / 217 / 217 / 235, all ≤25 words and single-line; the junk sentence
and the second fabricated sentence = 0. Entry drafting note: the spec-suggested Q1 wording (without
`The Exploit Prediction Scoring System (EPSS)`) is not on the page; the pinned Q1 is the 25-word span
beginning at the `(EPSS)` parenthetical (`ScoutF19Open` §40).

Entry and row review posture. `RevEntryF19` verdict: **ADMIT — no Q1–Q10 criterion fails** on the
corrected 262-line / 17,266 B text (11 blockquotes + 9 inline spans all `occ=1`, ≤25 words and
on-anchor; 8 rejected over-generalizations; three-way manifest/header/recheck binding), after it found
and fixed the draft's digest typo (`4ec61c59b0a9aedf…` → `…b0e9…`, the same defect `MutJunkTwin` §3
raised) during review; two one-line repairs should land with it — FC-2's span list adds the L217
"It offsets subjective judgments…" blockquote (12 spans, not 11) and a one-word miscount in the
Honest-limit line — plus one L1 note (F5). `RevRowS053` verdict: **matches — no fixes required** (11
cells / NF=13, zero inner pipes, tier A, `mined`, opened 2026-10-26, anchor carries the full sha256,
URL equals the manifest URL; only its §8 narration timestamp is noted). Land the corrected entry bytes
`[MEASURE: final entry sha256, FC-2 spans=12]`. Counter
separability is bounded, and the report states it (`CritC2Claim`): the do-nothing control is sound,
but the counters are not causally separable as measurements — the harness prints `PASS F19 ids=S053`
on an export containing **zero S053 capture bytes** (so it is not a capture test), the registry row
cannot move without its `used-by` entry (`census E11`), and an EOF-appended row placement fires
`census E12`; the frozen C2 predicate survives because it also requires the source-recheck and
capture-binding limbs `[MEASURE: CritC2Claim residual table]`.

## Sources & frontier

`corpus/SOURCES.md` before → after: **52 → 53 rows**. Rows added by tier: **1 × A** — S053 (`source`
`FIRST EPSS documentation page — https://www.first.org/epss/`, kind `docs`, tier A scoped to FIRST's
own EPSS statements, anchor into `corpus/source-snapshots/round-36/S053.txt` with the full sha256,
status `mined`, opened 2026-10-26, recheck `90d`, used-by
`corpus/knowledge/epss-exploit-prediction-scoring.md`) `[MEASURE: applied line number]`. Tier histogram
before: **A 49 / B 1 / C 2**; after: **A 50 / B 1 / C 2**. Status histogram before: **mined 40 /
queued 9 / rejected 3**; after: **mined 41 / queued 9 / rejected 3**; malformed rows 0, duplicate ids
none (before/after measured on scratch copies of the registry by `RevSpotCheckReadiness` §3;
`[MEASURE: landed counts]`).

Rows touched old→new: **none** — no status, recheck or used-by cell changed on any pre-existing row
(S001–S052 untouched) `[MEASURE: RevNoHarm / MutC2Row]`. The one change to pre-existing text is an
appended R9 correction for the round-35 S052 search-log bullet (`corpus/SOURCES.md:79`): the printed
suffix `d69349e8…77e8826` is invalid (the capture hashes to `d69349e86c5cce17146ccb4a…779e8826`), and
the bullet's "7 SOURCES rows" counted two `## Search log` bullets — the base row-restricted CISA
count is 6. The correction is a new paragraph; `:79` stays byte-intact `[MEASURE: appended line]`.

Frontier rows advanced: **F18 → F19** (`corpus/README.md`; F18 at `:388` at base, F19 at
`[MEASURE: line]`). `PROVINCE.md` carries end-of-file frontier amendments for **F18** (owed from round
35; round-35 box 4 recorded it unapplied) and **F19** `[MEASURE: line numbers, prefix-identical
rehearsal]`.

Search log: round-36 bullet at `[MEASURE: corpus/SOURCES.md line]` with the counts and the negative
sweep. Sweep nuance: `EPSS` → 0 files and `exploit prediction` → 0 files, but the broad token
`exploitation likelihood` → 1 pre-existing Immunefi line that is not EPSS ground, so the
uncovered-ground assertion must use the strict anchors (`ScoutF19Open` §49). Adjacency: `ScoutF19Sibling`
rules **UNCONTESTED** (0 strict hits across 20 sibling lanes); `ExecSiblingSweep` rules **RATIFIED /
uncontested** after widening to hidden files and shokuknow — 127 EPSS-family files fleet-wide, all
non-ground (97 are the `epssweep` Godot-boundary-test identifier in `game-dev-2d-shokunin`, the rest
ASCII substring noise), and shokuknow holds a CSS2024 programme abstract naming EPSS as one of three
prioritisation inputs (SSVC, KEV, EPSS) with no method, threshold or data. Nothing is absorbed; the
lane reports it. Method note carried to the entry: a `\bEPSS\b` anchor fails on 「EPSSなど」 (Unicode
word boundary), so Japanese-language cites need the boundary-free form. `ConnSibling` consolidates the
two labels into the round's ruling: **uncontested by every sibling; doctrine-assigned at the domain
level only** — "UNCONTESTED" says no sibling holds EPSS ground, "RATIFIED" adds the doctrine-host and
in-lane-occupancy axes, and the host table itself carries no `first.org` row, so the lane reports F19
the way it reported F18 and absorbs nothing `[MEASURE: final ruling text in the lesson]`.

## Trend verdicts

- **expansion: improved.** One admitted knowledge entry on ground the coverage map did not hold
  (EPSS exploitation-likelihood scoring, distinct from the severity ground S001/S002/S046/S047, the
  platform ladders S043/S044/S049/S050/S051 and the KEV exploitation-status ground S052); frontier
  18 → 19; registry 52 → 53 at tier A; entry cites mined `source: S053`; harness 22/22; strict-sweep
  hits 0. No new capability row (the capability window is not restarted; last entry round 33).
- **quality: improved.** The round-35 spot-check's routed defects land as runnable, discriminating
  checks, and the first two discriminators are now measured with the drafted suite: r35 base export
  `closed=0/9 exit=1` (all nine open) and r35 judged head `closed=4/9 exit=1` (E1/E3/E4/E8/E9 open),
  against the frozen target `closed=9/9 exit=0` + `cases=9 failures=0` `[MEASURE: post-landing
  outputs]`; the before/after limbs are bound to named bytes (matrix above); the false-evidence lines
  are corrected in the lesson (E8) instead of rewritten; the lane files quiescent (E9); `recheck-audit`
  strict 48/48 with `expected=48`; `anchorcheck.py SKILL.md` 0 bad `[MEASURE: post-landing]`; census
  exit 0; the 26-instrument no-harm baseline is green on the base bytes (`ExecInstrumentsSynopsis`).
  Strength limit, stated: E2/E5/E6/E7 are held-closed re-verifications of round-34/35 landings, not new
  moves; the new work is E1/E3/E4/E8/E9 plus the suite and fixtures. The suite's own fixture matrix is
  green (`ExecC1Fixtures`: green fixture `closed=9/9`, `selftest cases=9 failures=0`, nine per-check red
  fixtures each opening only its own limb, 14 clause mutants, controls E9b/E4b, three forged reports
  rejected), but a green selftest on fixture-authored bytes is not admittance: `RevC1Suite` returns
  **REFUSE (repair-then-admit)** on the draft (two HIGH file-wide-literal limbs on E3/E7, one MED
  live-index read on E4), and `CritC1Export` records a forged-run surface (`--lane`/`--scratch-root`
  and `GIT_DIR`-style env vectors can print `closed=9/9`; `export-ignore` can flip E8's absence limb on
  an unchanged ref; a committed symlink at a measured path is followed). Three E-limbs also carry
  design limits (E1 tokenisation/F1, E8 presence-only, E4's single-limb gain). `closed=9/9` is
  therefore a landing requirement with the repairs plus a re-review, not a measured state `[MEASURE:
  landed revision, re-review verdict]`. On the C2 side, `RevSourceRecheck` passes all five Q10 criteria
  on the drafted recheck line and reproduces the fail-closed exit 2 three ways, and `RevClaimsFreeze`'s
  freeze verdict is OK at 24/24.
- **discernment: improved.** The gate refused and recorded rather than absorbed: the junk twin is
  rejected by the counter it was built to fool (fabricated quote absent, `quote-not-found`, exit 1;
  wrong-source twin exit 1 or fail-closed exit 2; the real entry exit 0 twice); assimilation
  **adopted 0** — id-collision screen 52 registry ids vs 94 staged ids = **22** collisions at HEAD
  (23 on a synthetic S053 copy), guard proven load-bearing (an indented collision is caught only by
  the 0-3-space pattern) and failing closed (exit 2) on a missing registry; the quarantine slice
  re-derives to 7 rows, byte-identical to the committed round-35 slice, all 7 refused this round —
  present-and-located 1 (S068, duplicate of S040), absent 2 (S037, S054), unreachable 4 (S048, S065,
  S069, S070), prose-class-unverifiable 0, adopted 0; the seven standing refusals stand `[MEASURE:
  ScoutStandingRefusals digests]`; `RevEntryF19`/`RevRowS053` verdicts are recorded verbatim
  `[MEASURE]`; considerthese 2026-10-26: proposal 1 partially landed (gap computed; the
  thresholds-in-§Saturation plank **not** landed), 2 not this round, 3 adopted-in-scope (R28 + E9)
  landing pending, 4 not this round (operator/LFS decision; `.ufo/` is 6905/7175 tracked files and
  109.4/115.0 MB of blobs), 5 adopted-in-scope (F18 + F19), 6 recorded as reflection no change, 7
  recorded not started — with that receipt's own F-1 warning that adopted-in-scope is not landed. The
  C2 attack matrix is reported as residue, not as proof: a fabricated entry-body quote survives when
  the manifest asserts a different (real) sentence (A2c: harness `entries=22 pass=22`, source-recheck
  OK), a twin reusing the real selection and seeded as F20 with a prose citation is admitted (A4c:
  `entries=23 pass=23`), a passing entry with no README row is invisible to every counter (A5a), and
  a manifest URL mismatch is caught **only** by `capture-binding-check` (A3a/A3b/A3d)
  `[MEASURE: CritC2Kill §survivors line refs]`; the C1 attack residue is `[MEASURE:
  CritC1Kill/CritC1Export]`.
- **Score position.** Both claims are **held** (C1 4, C2 7); no promotion, no saturation signal, no
  aggregate verified-round inference. Distance to the next verifiability score, recomputed on the
  landed bytes with `python3 corpus/instruments/score-gap.py` `[MEASURE: output]`; at base it reads
  `recheck: lines=47 executes=23 gated=24 broken=0 exit=0` and `gap: 24 of 47 rechecks still gated on
  a lost base; score 5 needs 0 gated unsupported claims` (threshold text `SCORECARD.md:331`:
  "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims").

## SHONEN

- [~] **SKILL.md contains real decision tables, error patterns, checklists, cited sources** — the
  round's SKILL.md delta is the Gates & probes registry end-of-file append registering both closure
  instruments by exact basename (`r35-defect-closure.sh` and `r36-closure.sh`); both literals are 0 on
  the pre-append blob (`daeff71b…`, 1104 lines; the near-name `r-defect-closure.sh` row is 4 lines
  and does not satisfy them), so the rows are this round's delta, and the criterion now travels with
  the literal (M36-3, QUALITY R29) `[MEASURE: post-append sha256/lines, density.py mean/blocks/cites,
  anchorcheck exit]`. Box stays `[~]`: no named non-author verifier has checked it; a wave seat cannot
  check its own box.
- [~] **At least one end-to-end domain task executed and logged in LOG.md** — **no new end-to-end
  domain task ran this round**; `LOG.md` gets a `## Round 36` heading logging instruments and an
  admission, not a hunt-to-claim task `[MEASURE: LOG.md line]`. The closest executed measurement is
  the S053 capture + `source-recheck` + the E1–E9 closure suite, which is instrument work. Box stays
  open, and considerthese proposal 2 records it as not this round.
- [~] **Instructions executable by an agent without oral context** — `recheck-audit.py` strict 48/48
  / `expected=48` `[MEASURE]`; `r36-closure.sh --selftest cases=9 failures=0` `[MEASURE]`; every
  knowledge recheck line is `bash -n`-clean and `cd`-prefixed; the manifest/entry/row chain is
  three-way bound (header `source: S053` = recheck `--source S053` = manifest record id); the
  post-integration gate script `wave1/ExecGateReviewPrep.md` is `bash -n`-clean and writes nothing to
  the lane. Open: the suite's own bytes are not pinned by a digest (the round-35 spot-check's F-1),
  and only a non-author run closes the box.
- [~] **No cross-domain bleed (PROVINCE.md still accurate)** — F18/F19 sit inside the province
  (program rules, claim packages; the F13/F16/F17 precedent) and land as appends; `ScoutF19Sibling`
  rules UNCONTESTED and `ExecSiblingSweep` RATIFIED/uncontested across 20 sibling lanes plus
  shokuknow, so nothing is absorbed and no report-to-lane item arises `[MEASURE: ConnSibling final
  ruling; PROVINCE append lines]`. Box stays open on non-author verification.

**Stale-lane:** respawn-per-round driver; `.ufo/watchdog.log` reads
`2026-10-26T12:31:14-03:00 launch kasegi round=36 pgid=14809 driver=hyaku-inline attempt=1`; no other
mission of this lane is open `[MEASURE: state at filing; no `complete` line while the report is
written]`.

**Tooling installs:** none this round by this seat; no pacman transactions (host-wide pause)
`[MEASURE: confirm across seat receipts — none records a tool/version/channel]`.

**Open L0 questions:** kasegi round-15 (PROVINCE re-point against the lost `~/Projects/bounties`
root), round-16 (second in-round source loss) and round-32 (re-dispatch vs L1-only landing ruling)
remain open as last recorded; round-12 (bounties interactive-rebase stall) and round-17
(round-namespace reconciliation) are also still listed in the fleet L0 registry; none blocks this
round. Proposal 4 (cap/externalise wave evidence) is an operator/LFS decision recorded in the
considerthese disposition, not filed as an L0 row `[MEASURE: confirm no new kasegi L0 row]`.
