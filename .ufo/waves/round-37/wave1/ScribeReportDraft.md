# kasegi — round 37 report — DRAFT skeleton (ScribeReportDraft receipt)

Lane: `kasegi-shokunin` (bounty & security research). Axes owned: depth:verifiability (4),
coverage (7), depth:density (9, no-harm). Lane base `b56a41680cefd391868c1c370dc063c69d827e7d`;
claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c` (`claims.json` sha256 `570c1d2c…`, 81 lines,
frozen 2026-10-26T16:30Z, attempt 1), plus appended `claims-erratum-1.md` (`b362068`, S054 capture URL
correction, filed before any seat scored).

Draft status: **skeleton**. Every value below is one of (a) copied from the frozen claims, (b) measured
read-only at the named commits by this seat (command printed), or (c) taken from a wave-1 receipt that
had landed while this draft was written (13 receipts were present at measurement time; this seat's own
receipt is the 14th, listed below). Anything that exists only at
the round-37 final lane head is marked `[MEASURE: …]` for the L1 to replace after measurement. Copy from
"## Work performed" onward into `.ufo/reports/round-37/kasegi.md`, supply the title, and commit the
report **after** the final lane commit (landing order: report last). This is L1-owned Shokunin evidence,
not a canonical Rust verdict or Pareto claim.

- Seats whose receipts back filled values: `ExecC1BaseFail`, `ExecC1JudgedHeadFail`, `ExecC1ExportMode`,
  `ExecC2Capture`, `ExecC2JunkControl`, `ExecC2QuoteOnce`, `ExecCensusReplay`, `ExecExpectedListSync`,
  `ExecManifestChecks`, `ExecQuiescenceProbe`, `ExecRegressionBase`, `ExecAncestry`, `ScribeRowS054`.
- In flight at this draft, so their numbers stay `[MEASURE]`: `ExecC1SuiteBuild`, `ExecC1Fixtures`,
  `ExecC2Harness`, the `Rev*` / `Crit*` / `Mut*` receipts, `Scout*`, `Conn*`, `Sent*`, `Simpl*`,
  `ScribeEntryF20`, `ScribeGateLesson`, `ScribeMistakes`, `ScribeScorecard`, `ScribeShonen`, `ScribeLOG`,
  `ScribeQualityRows`, `ScribeAssimilationGate`, `ScribeConsiderthese`, `ScribeFrontierAmendments`,
  `ScribeReportDraft`, and `wave1-results.json`.
- Round-37 carriers that did **not** exist when this draft was written and are placeholders by
  construction: `corpus/instruments/r37-closure.sh`, `.ufo/waves/round-37/final-gates/all-gates.txt`,
  `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`,
  `corpus/source-snapshots/round-37/{S054.txt,manifest.json}`, the `## Round 37` sections of
  `SCORECARD.md` / `LOG.md`, `corpus/lessons/round-37.md`, `corpus/considerthese-ledger.md`.

## Work performed

The round declares **two claims**, frozen before dispatch in `.ufo/waves/round-37/claims.json` (attempt 1;
base `b56a4168…`, claims-freeze `224df74d…`, before-controls `c1-controls/before.txt` `63670cf5…`
(30 lines), `c2-controls/before.txt` `fd849486…` (22 lines), `census-before.txt` `ada01b8e…` (8 lines) —
all measured at `224df74d` with `git show`), with one appended erratum (`claims-erratum-1.md`, in
`b362068`). Saturation line is 9/10 per owned axis, window N = 3; the lowest non-retired axis is
depth:verifiability (4). This round works the two lowest axes and restates density as no-harm.

- **C1 — depth:verifiability (score 4, held).** The committed instrument `corpus/instruments/r37-closure.sh`
  runs fourteen checks E1–E14 over a `git archive` export of a named lane head (`--export-ref <hash>`) and
  prints `closed=14/14 exit=0` on the round-37 final lane head and `cases=14 failures=0` under `--selftest`.
  E1–E9 carry the round-36 semantics forward; E10–E14 are the new discriminators closing the round-36
  verifier spot-check's routed defects D1, D2, D4, D5, D6 (`corpus/lessons/round-36-verifier-spotcheck.md`
  §5). **Mapping gap to state, not to paper over:** §5 routes six defects D1–D6, but the frozen claim's
  parenthetical maps only five (D1→E10, D2→E11, D4→E12, D5→E13, D6→E14). **D3** (the closure-order
  recurrence: `c20300df` + erratum `1c43fd8f` landed *after* `complete kasegi round=36`) has no named
  E-check in the frozen mapping; the report must either point at the E-check whose payload actually reads
  the order class or record D3 as an open routed defect carried to round 38 — this draft asserts neither
  `[MEASURE: whether any E<n> payload names D3; ScribeGateLesson / RevC1Suite ruling]`:

  | check | semantics (frozen claim) | defect closed |
  |---|---|---|
  | E1 | structural placeholder/hash binding (`filled by the L1` = 0, `<LANE_HASH>` = 0; the lane-commit line's hash exists and is an ancestor of the exported ref) | carried over |
  | E2 | round-34 depth:density erratum present | carried over |
  | E3 | `SKILL.md` Gates & probes registry rows for the **exact** basenames `r35-defect-closure.sh` **and** `r36-closure.sh` | carried over |
  | E4 | round-35 `wave1-results.json` tracked **with** its provenance note | carried over |
  | E5 | `claims-erratum-d5.md` present | carried over |
  | E6 | path-pinned `L1Integration.md` carries `Correction (round 35)` | carried over |
  | E7 | `QUALITY.md` supersedes-R22/R23 **rows** | carried over |
  | E8 | the false-evidence-line correction recorded in the round-36 lesson | carried over |
  | E9 | quiescence: `git status --porcelain` empty, no leftover `/fast/scratch/hyaku/kasegi-r37` seat dirs — **fail-closed**: a failed git-status read is red, never clean | carried over (rewritten) |
  | E10 | export's `.ufo/waves/round-37/final-gates/all-gates.txt` carries `suite-sha256=<sha>` (sha == digest of the suite bytes), fourteen `E<n> payload=` lines, `closed=14/14 exit=0`, fourteen `selftest case=` lines, `cases=14 failures=0` | **D1** |
  | E11 | `LOG.md` round-37 entry contains a named correction of the round-36 C1 bullet's false `corpus/instruments/r36-fixtures/` path | **D2** |
  | E12 | round-37 lesson **and** round-37 `SCORECARD` section label r36 lane head `c20300df…` as `anchor ancestor`; stale `Final lane commit: e666d902` appears nowhere inside the round-37 SCORECARD section | **D4** |
  | E13 | `SKILL.md` registry row `r36-closure.sh` has a single-choice type cell (not the literal `gate\|probe`) and its verdict map includes exit `2` → `could-not-evaluate` | **D5** |
  | E14 | the suite's own quiescence code is fail-closed **by shape**: `grep -cF 'porcelain:-0' r37-closure.sh` → 0, no status-read `2>/dev/null` swallow | **D6** |

  Required reds (frozen): r36 base export `cc692008…` → `closed<14/14 exit=1`; r36 judged-head export
  `a23dc478…` → `closed<14/14 exit=1` (E10–E14 open there). Both are structurally guaranteed by the
  measured limb matrix below (E10 absent, E11 defect present, E12 stale label present, E13 literal type
  cell, E14 `porcelain:-0` present at both refs) `[MEASURE: the two actual suite runs]`.

- **C2 — coverage (score 7, held).** Frontier **F20 — SSVC (Stakeholder-Specific Vulnerability
  Categorization, CERT/CC / Carnegie Mellon)** admitted 19 → 20; registry row S054 added (tier A, kind
  `docs`, status `mined`, opened 2026-10-26, anchored in the round-37 capture); knowledge entry
  `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` cites `source: S054`;
  harness `entries=23 pass=23 exit=0` incl. `PASS F20 ids=S054`; `source-recheck.py --source S054` exit 0;
  census exit 0 (W04 S028/S029 only); `corpus/knowledge/*.md` 48 → 49; capture
  `corpus/source-snapshots/round-37/{S054.txt,manifest.json}` committed and bound; `knowledge-expected.txt`
  synced (audit `expected=49 unexpected=0`); junk twin `c2-controls/junk-f20.md` rejected by the counter it
  was built to fool. The capture URL is the **erratum-1** value
  `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`, not the frozen `https://certcc.github.io/SSVC/`;
  the frozen claim's URL literal is superseded by the appended erratum (reported verbatim for the canonical
  judge, never silently rewritten). Measured capture (this draft, `ExecC2Capture`): `S054.txt` 32,623 B /
  518 lines / sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`
  `[MEASURE: landed manifest sha256]`.

**Work items by area** (receipts under `.ufo/waves/round-37/wave1/`):

- **C1 build** — `ExecC1SuiteBuild` (`r37-closure.sh`, E1–E14), `ExecC1Fixtures` (per-check red/green
  fixtures generated per selftest case; no committed fixture tree — the D2 correction says so explicitly),
  `ExecC1ExportMode` (export-mode discipline), `ExecC1BaseFail` (r36-base red), `ExecC1JudgedHeadFail`
  (r36 judged-head red), `ExecQuiescenceProbe` (E9 fail-closed red/green), `ExecAncestry` (E12
  existence/ancestry table), `ExecGateReviewPrep` (post-integration gate script).
- **C1 attack/review** — `RevC1Suite`, `RevC1Fixtures`, `RevC1Selftest`, `MutC1Suite`, `MutC1Fixtures`,
  `CritC1Kill`, `CritC1Export`, `ExecRegressionBase` (before-controls replay), `ExecDatawalk` (spot-check
  §5 open/closed matrix), `SimplC1`.
- **C2 build** — `ExecC2Capture` (S054 capture + round-37 manifest), `ScribeEntryF20` (entry),
  `ScribeRowS054` (row + search-log bullet + Paths line), `ExecC2Harness` (`knowledge-expected.txt` 49 +
  harness sync), `ExecCensusReplay`, `ExecManifestChecks`, `ExecC2QuoteOnce`, `ExecC2JunkControl` (junk
  twin + discriminating invocation), `ExecExpectedListSync`.
- **C2 attack/review** — `RevEntryF20`, `RevRowS054`, `RevSourceRecheck`, `RevHarnessSync`, `MutC2Entry`,
  `MutC2Row`, `MutJunkTwin`, `CritC2Kill`, `CritC2Claim`, `ScoutF20Open`, `ScoutCaptureAvailability`,
  `ScoutF20Sibling`, `ExecSiblingSweep`, `ConnSibling`, `ConnC1C2`, `ConnPatterns`, `RevNoHarm`,
  `RevSpotCheckReadiness`, `RevClaimsFreeze`, `CritMotivation`, `CritBoundary`.
- **Non-claim frontier items** — assimilation: `ScoutQuarantine`, `ScoutIdCollisions`,
  `ScoutStandingRefusals`, `ScribeAssimilationGate`; considerthese: `ScribeConsiderthese`; mistakes:
  `ScribeMistakes`; QUALITY rows: `ScribeQualityRows`; scope/credentials: `SentScope`, `SentSecrets`;
  simplification: `SimplReport`.
- **Round record** — `ScribeGateLesson` (`corpus/lessons/round-37.md`), `ScribeScorecard`,
  `ScribeShonen`, `ScribeLOG`, `ScribeFrontierAmendments` (PROVINCE F20 + README F20),
  `ScribeReportDraft`.

## Landed changes

Every change below is tied to the round-37 `LOG.md` entry (heading `## Round 37`, appended in
`[MEASURE: commit]`; draft at `.ufo/waves/round-37/wave1/ScribeLOG.md`) and to the commits named. The
report commit follows the final lane commit (landing order: report last).

| Change | Commit |
|---|---|
| Claims freeze: `claims.json` (`570c1d2c…`, 81 lines), `census-before.txt` (`ada01b8e…`), `c1-controls/before.txt` (`63670cf5…`), `c2-controls/before.txt` (`fd849486…`) | `224df74d` |
| Claims erratum 1: S054 capture URL → `…/SSVC/tutorials/ssvc_overview/` (appended file, frozen claims untouched) | `b362068` |
| Wave evidence: `wave1-spec.json`, `wave1-dispatch.json`, `wave1.ready` + `.partial`, plan/run logs, `assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}` | `f324655` |
| C1 counter `corpus/instruments/r37-closure.sh` (E1–E14, export-mode only) `[MEASURE: sha256, line count]` | `[MEASURE: commit]` |
| D1: `.ufo/waves/round-37/final-gates/all-gates.txt` — `suite-sha256=<sha>` header, 14 `E<n> payload=` lines, `closed=14/14 exit=0`, 14 `selftest case=` lines, `cases=14 failures=0` | `[MEASURE: commit / path sha]` |
| D2: `LOG.md` round-37 entry named correction paragraph (the round-36 C1 bullet said `corpus/instruments/r36-fixtures/` landed; `git ls-tree` shows it absent — the r36 suite bytes are the instrument, the fixture tree was never committed) | `[MEASURE: LOG line]` |
| D4: `corpus/lessons/round-37.md` + the round-37 `SCORECARD.md` section label r36 lane head `c20300df…` as `anchor ancestor`; the round-37 SCORECARD section carries no `Final lane commit: e666d902` | `[MEASURE: line refs]` |
| D5: `SKILL.md` Gates & probes registry — `r36-closure.sh` row's type cell becomes a single choice and its verdict map gains exit `2` → `could-not-evaluate` (end-of-file append or in-row edit; the append-only rule decides) | `[MEASURE: SKILL.md line, sha256, line count]` |
| E1/E3/E4/E5/E7 held closed: round-37 SCORECARD section placeholder-free; exact-basename rows for `r35-defect-closure.sh` **and** `r36-closure.sh`; `.ufo/waves/round-35/wave1-results.json.provenance.md`; `.ufo/waves/round-35/claims-erratum-d5.md`; QUALITY supersedes-R22/R23 rows | `[MEASURE: commit; E1/E3/E4 payloads]` |
| C2: `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` `[MEASURE: sha256, lines]`; `corpus/SOURCES.md` S054 row + round-37 search-log bullet; `corpus/README.md` F20 row + admission paragraph; `corpus/source-snapshots/round-37/{S054.txt,manifest.json}`; `corpus/instruments/knowledge-expected.txt` 48 → 49 | `[MEASURE: commit]` |
| PROVINCE frontier amendment F20 (end-of-file append per R6) | `[MEASURE: commit, PROVINCE.md line]` |
| QUALITY rows R30 (fail-closed failure path; no `${x:-0}`/`2>/dev/null` swallow) and R31 (considerthese disposition recorded + ledger) — end-of-file append | `[MEASURE: commit, lines]` |
| `corpus/considerthese-ledger.md` (proposal tracking ledger, proposal 7 mined) | `[MEASURE: commit]` |
| Round close: SCORECARD round-37 section, SHONEN append, `corpus/lessons/round-37.md` (Gate/Assimilation/considerthese/Census/Mistakes M37-1…M37-5), `LOG.md` `## Round 37`, wave receipts, `[MEASURE: wave1-results.json]` | `[MEASURE: final lane commit]` |

No existing line of `SKILL.md`, `PROVINCE.md`, `corpus/SOURCES.md`, `corpus/README.md`,
`corpus/QUALITY.md`, `SCORECARD.md`, `SHONEN.md` or `LOG.md` is rewritten: landings are appends, except
the D5 registry cell, where the frozen claim requires the row's type cell to change (the round must state
which form it took and why) `[MEASURE: RevNoHarm verdict on the export diff; D5 edit form]`.

## Before → after measurements

Measured commits: **before** — base `b56a4168…` and the claims freeze `224df74d…`; controls over the
named exports `cc692008b0cfd58d18275aa6c4aed79620120799` (r36 base) and
`a23dc4788aa7c98831eed6db953434034ce5ae8d` (r36 judged head); **after** — `[MEASURE: final lane commit]`.

Measurement state on the freeze bytes (this seat, `git show <ref>:<path> | sha256sum` and `wc -l` at
`b56a4168`): `corpus/SOURCES.md` `2ff7818a…` (117 lines, 53 rows), `corpus/README.md` `55c41374…`
(398 lines, 19 F-rows), `corpus/QUALITY.md` `cfd0187a…` (264 lines), `SKILL.md` `2ddb1bc7…` (1111 lines),
`PROVINCE.md` `b0e91a61…` (78 lines), `SCORECARD.md` 1494 lines (no `## Round 37` section yet —
`grep -c '^## Round 37' SCORECARD.md` = 0). Instrument corpus: 17 committed scripts (14 `.py`, 3 `.sh`);
`r37-closure.sh` present = 0 (`ls corpus/instruments/r37-closure.sh` → exit 2).

### C1 — depth:verifiability (fourteen closure checks over a named export)

Frozen before-controls (`c1-controls/before.txt`, at `224df74d`): `suite_missing=1`,
`placeholder_filled=0`, `placeholder_angle=0`, `D1 open` (no `final-gates/all-gates.txt`), `D2 open`
(LOG cites `r36-fixtures`, `git ls-tree | grep -c r36-fixtures` = 0), `D4 open`
(`grep -c 'Final lane commit: e666d902' SCORECARD.md` = 1), `D5 open` (row type cell literal
`gate\|probe`, no exit-2 verdict), `D6 open` (`porcelain:-0` present), `worktree_clean=0`,
`scratch_leftovers=0`.

| Counter (frozen command) | Before | After |
|---|---|---|
| `bash corpus/instruments/r37-closure.sh --export-ref <r37-final-lane-hash>` | suite absent (`ls` exit 2, `suite_missing=1`) | `closed=14/14 exit=0` `[MEASURE: output]` |
| same, `--export-ref cc692008b0cfd58d18275aa6c4aed79620120799` | suite absent | **`closed<14/14 exit=1`** — structurally forced: E10 absent, E11 defect present, E12 stale label present, E13 literal type cell, E14 `porcelain:-0` present `[MEASURE: closed=K/14 line]` |
| same, `--export-ref a23dc4788aa7c98831eed6db953434034ce5ae8d` | suite absent | **`closed<14/14 exit=1`** — same five limbs red `[MEASURE: closed=K/14 line]` |
| `bash corpus/instruments/r37-closure.sh --selftest --export-ref <r37-final-lane-hash>` | suite absent | `cases=14 failures=0 exit=0` `[MEASURE: landed revision]` |
| `grep -c 'filled by the L1' SCORECARD.md` | 0 | 0 `[MEASURE]` |
| `grep -c '<LANE_HASH>' SCORECARD.md` | 0 | 0 `[MEASURE]` |
| `grep -c 'Final lane commit: e666d902' SCORECARD.md` (whole file) / restricted to the round-37 section | 1 / n/a (no round-37 section) | `[MEASURE: whole-file may stay 1 from the round-36 block; the E12 literal is section-scoped and must read 0]` |
| `grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh` (E14) | 0 — the suite is absent (`grep` exit 1); the literal lives in the **r36** suite at `r36-closure.sh:466` | 0 `[MEASURE]` |
| E9 `status-dirty` / `scratch-seat-dirs` / `head-match` | 0 / 0 / n/a at freeze; **6 / 23** while this wave runs (this seat: `git status --porcelain \| wc -l` = 6 untracked round-37 wave entries; `find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 -maxdepth 1 -type d \| wc -l` = 23) | 0 / 0 / 1 at filing `[MEASURE]` |

D-limb matrix over the three named trees (literals re-measured by this seat with `git show <ref>:<path>`
and `git ls-tree`, 2026-10-26; suite verdicts are `[MEASURE]` because the r37 suite does not exist at
draft time):

| limb | r36 base `cc692008` | r36 judged head `a23dc478` | r37 base `b56a416` | r37 final head |
|---|---|---|---|---|
| E10 `r37 final-gates/all-gates.txt` tracked | 0 → **open** | 0 → **open** | 0 → open | `[MEASURE: 1, header + 14 E lines + 14 case lines]` |
| E11 `r36-fixtures` cited in `LOG.md` | 0 | 1 (r36 bullet, `LOG.md:1665`) → **open** | 1 → open | `[MEASURE: correction present, defect named]` |
| E12 stale `Final lane commit: e666d902` | 0 | 1 (`SCORECARD.md:1492`; also `corpus/lessons/round-36.md:3`) → **open** | 1 → open | `[MEASURE: 0 inside the round-37 section]` |
| E12 `anchor ancestor` / `c20300df` occurrences | 0 / 0 | 0 / 0 | 0 / 0 | `[MEASURE: ≥1 / ≥1 in lesson + section]` |
| E13 `r36-closure.sh` row type cell = literal `gate\|probe` | 0 (row absent) | 1 (`SKILL.md:1111`) → **open** | 1 → open | `[MEASURE: 0 / single-choice cell]` |
| E13 row verdict map `2` → `could-not-evaluate` | 0 | 0 (`could-not-evaluate` file-wide 1, at `:981` on the `recheck-audit.py` row) → **open** | 0 | `[MEASURE: 1 in the r36 row]` |
| E14 `porcelain:-0` in the r36 suite | 0 (suite absent) | 1 (`r36-closure.sh:466`, with `2>/dev/null` at `:465`) → **open** | 1 | `[MEASURE: 0 in the r37 suite]` |
| E1–E9 carried-over limbs | E2/E5/E6/E7 closed, E1/E3/E4/E8/E9 open (round-36 receipt set) | E2/E5/E6/E7 closed, E9 open | E2/E5/E6/E7 closed; E4 note present (`.ufo/waves/round-35/wave1-results.json.provenance.md` = 1); E5 present (`claims-erratum-d5.md` = 1) | `[MEASURE: all closed]` |
| suite verdict over this ref (r37 suite) | `[MEASURE: closed=K/14 exit=1]` | `[MEASURE: closed=K/14 exit=1]` | not the measured target | `[MEASURE: closed=14/14]` |

Context reds already measured with the **r36** suite (not the r37 counters; `ExecC1BaseFail`,
`ExecC1JudgedHeadFail`): `r36-closure.sh` sha256 `4db1ae70…`, 894 lines — over `cc692008…`
`closed=4/9 exit=1` (open E1, E3, E4, E8, E9; closed E2, E5, E6, E7) and over `a23dc478…`
`closed=8/9 exit=1` with only the live E9 limb open (`status-dirty=6,scratch-seat-dirs=0,head-match=0`).
That pair shows the r36 base's four extra reds are the round-36 landing delta, and that E9 is live by
definition on historical exports. It does **not** substitute for the two required r37-suite reds.

Export-mode contract (`ExecC1ExportMode`, measured on a scratch `git archive` copy of the r36 suite whose
sha256 `4db1ae70…` equals the lane file's): a plain run is refused with exit 2, so the suite needs no
worktree-reading mode; and the two guards E10/E14 exist to force are named there — **G1** derive
`suite-sha256` from the *ref's blob* rather than the worktree copy, **G2** rc-check the status read and
print a distinct red on failure `[MEASURE: both guards present in the landed r37 suite]`.

`Runtime`/design limits to state in the report, not as passes: E1 tokenisation is `SCORECARD`-scoped;
E9 is a live reading (worktree, scratch root, HEAD) and can only mean "not quiescent **now**" on an
historical export; E12 is literal- and section-scoped, so a stale label elsewhere (the round-36 lesson,
`SCORECARD.md:1492` outside the round-37 section) is not tested by it; E13 tests the row's cells, not the
row's truth; E14 is a shape test on the suite's own bytes, not a proof that every read fails closed
`[MEASURE: CritC1Kill / CritC1Export / RevC1Suite residue]`.

### C2 — coverage (F20 / S054)

Frozen before-controls (`c2-controls/before.txt`, at `224df74d`): `frontier=19`, `registry_rows=53`,
`s054_rows=0`, `entries_citing=0`, `knowledge_entries=48`, `harness=entries=22 pass=22 exit=0`,
`capture-binding records=43 bound=43 unbound=0`, `recheck-audit strict pass=48/48 expected=48`,
`round-37 capture dir 0`, `junk-f20 absent`.

| Counter (frozen command) | Before | After |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | **19** (F01–F19; measured this seat on `b56a4168`) | **20** (F20 row `[MEASURE: line]`) |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **53** (S001–S053; measured) | **54** `[MEASURE: line; malformed=0]` |
| `grep -cE '^\|[[:space:]]*S054[[:space:]]*\|' corpus/SOURCES.md` | 0 | 1 |
| `grep -rlE '^source: S054 ' corpus/knowledge \| wc -l` | 0 | 1 |
| `python3 corpus/instruments/frontier-recheck-count.py` | `entries=22 pass=22 exit=0` | **`entries=23 pass=23 exit=0`** incl. `PASS F20 … ids=S054` `[MEASURE: output]` |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` | manifest absent → exit 2 (`manifest UNAVAILABLE … missing`, fail-closed) | exit 0, `S054:sha256 OK`, quotes `occurrences=1` `[MEASURE: landed run]` |
| `python3 corpus/instruments/capture-binding-check.py` | `records=43 bound=43 unbound=0 exit=0` (measured; no round-37 record) | **`records=44 bound=44 unbound=0 exit=0`** `[MEASURE: landed]` |
| `python3 corpus/instruments/recheck-audit.py --quiet` | `strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0`, `expect=present expected=48 missing=0 unexpected=0 exit=0` (measured) | `strict pass=49/49`, `expected=49 unexpected=0 exit=0` `[MEASURE]` |
| `ls corpus/knowledge/*.md \| wc -l` | **48** (measured) | **49** |
| `wc -l < corpus/instruments/knowledge-expected.txt` | 50 (measured at `b56a4168`; the file carries header lines, so the audit's entry count is 48) | `[MEASURE: 51 physical lines, 49 entries]` `ExecExpectedListSync` mirror: `lines=48 total=48 pass=48` → `lines=49 total=49 pass=49`, and the same mirror **without** the sync reads exit 1 |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit **0**, exactly `W04 S028` + `W04 S029`, no E-codes (measured via `census-before.txt`; `ExecCensusReplay` reproduced it and also ran a mirror carrying the planned S054 row + entry → exit 0, E-codes 0, registry rows 53 at that state) | exit 0, same two W04 rows `[MEASURE]` |
| junk twin `c2-controls/junk-f20.md` | absent (`ls` = 0) | **rejected**: quote-not-found / mismatch under the removed-or-fabricated-sentence limb `[MEASURE: exact J-code + exit from ExecC2JunkControl / MutJunkTwin]` |

Capture: `corpus/source-snapshots/round-37/S054.txt` — normalized **32,623 B / 518 lines / sha256
`ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`** (`ExecC2Capture`), URL
`https://certcc.github.io/SSVC/tutorials/ssvc_overview/` (erratum-1 value; the docs home page was
measured to carry only the acronym expansion, one methodology sentence and a navigation list, with no
decision-point/outcome prose), `fetched_utc` strict UTC `[MEASURE: timestamp]`, manifest
`corpus/source-snapshots/round-37/manifest.json` sha256 `[MEASURE: sha256]`, one record keyed `sources`.
Live re-open (`ScoutF20Open`) and UA independence (`ScoutCaptureAvailability`): `[MEASURE: HTTP status,
raw-body sha256 vs capture]`.

Entry and row review posture: `RevEntryF20` verdict `[MEASURE: verdict verbatim]`; `RevRowS054` verdict
`[MEASURE: verdict verbatim, NF=13]`. Counter separability must be stated as a limit, not as proof
(`CritC2Claim`): the harness's `PASS F20 ids=S054` line is a citation test, not a capture test, and the
registry row cannot move without its `used-by` entry (census E11) while an EOF-appended row can fire
census E12 — the frozen C2 predicate survives only because it also requires the source-recheck and
capture-binding limbs `[MEASURE: CritC2Claim residual table]`.

## Sources & frontier

`corpus/SOURCES.md` before → after: **53 → 54 rows** (measured at `b56a4168`: 53 rows, 117 lines,
`2ff7818a…`). Rows added by tier: **1 × A** — S054 (source
`SSVC: Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/`
per erratum 1, kind `docs`, tier A scoped to CERT/CC's own SSVC documentation, anchor into
`corpus/source-snapshots/round-37/S054.txt`, status `mined`, opened 2026-10-26, used-by
`corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`) `[MEASURE: applied line,
NF=13]`. Tier histogram before: **A 50 / B 1 / C 2**; after: **A 51 / B 1 / C 2**. Status histogram
before: **mined 41 / queued 9 / rejected 3**; after: **mined 42 / queued 9 / rejected 3**; malformed rows
0, duplicate ids none (before measured this seat with `awk -F'|'` over the row set plus
`grep -oE '^\|[[:space:]]*S[0-9]{3,}' | sort | uniq -d | wc -l` = 0; after `[MEASURE]`).

Rows touched old→new: **none** — no status, recheck or used-by cell of S001–S053 changes
`[MEASURE: RevNoHarm / MutC2Row]`. Kind histogram before (measured): docs 40 / spec 8 / dataset 3 /
community 1 / paper 1 = 53.

Frontier rows advanced: **F19 → F20** (`corpus/README.md`, F19 at `:389` at base, 398 lines,
`55c41374…`; F20 at `[MEASURE: line]`). F20 teaches the SSVC statement this lane can act on: SSVC is a
modular decision-point system for prioritizing vulnerability-management actions for a named stakeholder,
distinct from CVSS severity, KEV catalog status and EPSS likelihood; read each decision point's outcomes
rather than collapsing them into a severity score. `PROVINCE.md` gets the end-of-file F20 amendment per R6
(`ScribeFrontierAmendments`) `[MEASURE: line, prefix-identical rehearsal]`; base `PROVINCE.md` is 78 lines
`b0e91a61…` and the appended list stops at F19.

Search log: round-37 bullet at `[MEASURE: corpus/SOURCES.md line]` with the counts and the negative sweep
(strict anchors `SSVC`, `Stakeholder-Specific Vulnerability Categorization`, decision-point vocabulary).
Adjacency: `ScoutF20Sibling` + `ExecSiblingSweep` over 20 sibling lanes plus shokuknow `[MEASURE: ruling
text — contested / uncontested and the hit list]`; note the round-36 sweep already recorded a shokuknow
CSS2024 programme abstract naming SSVC alongside KEV and EPSS, which is a naming hit, not SSVC method
ground — the ruling must say which it is. `ConnSibling` consolidates: `[MEASURE: final ruling]`. Nothing
is absorbed; the lane reports the item.

Non-claim frontier items (frozen): **assimilation — none adopted.** Id-collision rerun: registry **53** ×
staged **94** ids → **23** standing collisions (round 36 read 22); quarantine slice re-derives to **7**
rows, all refused this round — `payload-absent` 2 (S037, S054), `unreachable prose-class` 5, adopted 0
`[MEASURE: collision list + slice digests in the lesson / Scout receipts]`. **considerthese 2026-10-26:**
proposal 7 (a proposal-status ledger) mined → QUALITY **R31** + `corpus/considerthese-ledger.md`;
proposals 1–6 dispositions recorded old→new in the lesson (proposal 1's §Saturation thresholds plank stays
open; proposal 4 cap/externalise wave evidence stays an operator/LFS decision)
`[MEASURE: lesson disposition lines]`. **mistakes:** M37-1…M37-5 minted in `corpus/lessons/round-37.md`
(the D1–D6 routed-defect rows plus the r36 scratch-sweep incident) `[MEASURE: rows]`.

## Trend verdicts

- **expansion: improved.** One admitted knowledge entry on ground the coverage map did not hold — SSVC's
  stakeholder-tailored decision-point prioritization, distinct from the severity ground
  (S001/S002/S046/S047), the platform ladders (S043/S044/S049/S050/S051), the KEV exploitation-status
  ground (S052) and the EPSS likelihood ground (S053); frontier 19 → 20; registry 53 → 54 at tier A;
  entry cites mined `source: S054`; harness 22/22 → 23/23; census exit 0. No new capability row: a
  closure suite plus one admission is not a new thing the lane can do to the domain, so the capability
  window does not restart (last entry round 33) `[MEASURE: ScribeScorecard capability check]`.
- **quality: improved.** Five of the six round-36 routed defects (D1, D2, D4, D5, D6) land as runnable,
  discriminating checks (D3 has no named E-check — the gap stated in §Work performed). E10–E14 are new,
  and the two required reds are structurally forced at both r36 refs — measured limb matrix above, base
  `cc692008` → judged head `a23dc478`: E10 absent 0 → 0; E11 r36-fixtures cited 0 → 1; E12 stale label
  0 → 1 with `c20300df` unlabelled 0 → 0 and `anchor ancestor` 0 → 0; E13 literal type cell 0 → 1 and the
  row's exit-2 verdict 0 → 0; E14 `porcelain:-0` 0 (r36 suite absent at the base) → 1 — against the frozen
  target `closed=14/14 exit=0` + `cases=14 failures=0`
  `[MEASURE: post-landing outputs]`. The false lines are corrected by named correction (D2 in `LOG.md`,
  D4 in lesson + SCORECARD, D5 in the registry row) rather than rewritten; the quiescence limb is
  rewritten fail-closed and the suite's own shape is tested (E14), closing the `porcelain:-0` default
  (`r36-closure.sh:465-466`, measured). Held-closed re-verifications must not be sold as new moves:
  E2/E5/E6/E7 are round-34/35 landings (E4's note and E5's erratum are present at `b56a4168`). Strength
  limits: `closed=14/14` attests to the invocation that produced it (export-mode forgery surface recorded
  by `CritC1Export` in round 36 and re-attacked this round `[MEASURE: residue]`), E9 is live by
  definition, E12 is section-scoped, and a green selftest on fixture-authored bytes is not admittance
  `[MEASURE: RevC1Suite verdict on the landed suite]`.
- **discernment: improved.** The gate refused and recorded rather than absorbed: the junk twin is
  rejected by the counter it was built to fool (`[MEASURE: J-code, exit]`); assimilation **adopted 0**
  with the id-collision screen and the 7-row quarantine slice re-derived and all refused; the D5 error
  was found by an outside (round-36 verifier) read and closed with a named correction, which is the
  outside-spot-check limb doing its job `[MEASURE: RevSpotCheckReadiness verdict]`; considerthese
  dispositions are recorded with an owning criterion (R31) instead of prose. C2 attack residue reported,
  not proof `[MEASURE: CritC2Kill survivors]`; C1 attack residue `[MEASURE: CritC1Kill]`.
- **Score position.** Both claims **held** (C1 4, C2 7); no promotion, no saturation signal, no aggregate
  verified-round inference. Distance to the next verifiability score recomputed on the landed bytes:
  `python3 corpus/instruments/score-gap.py` `[MEASURE: output]`; the threshold text is `SCORECARD.md:331`
  ("non-author audit passing 25/25 source chains and 0 unsupported current claims") `[MEASURE: line ref
  unchanged]`.

## SHONEN

- [~] **SKILL.md contains real decision tables, error patterns, checklists, cited sources** — the
  round's SKILL.md delta is the Gates & probes registry: the D5 repair sets the `r36-closure.sh` row's
  type cell to a single choice and adds the exit-2 verdict, and the round registers its own suite
  `[MEASURE: whether the r37 suite gets a row this round — the frozen claims require only the two
  exact basenames stated above]`. Bytes: base 1111 lines `2ddb1bc7…`; after `[MEASURE: sha256, lines,
  density.py SKILL.md mean/blocks/cites, anchorcheck.py SKILL.md exit]`. Box stays `[~]`: no named
  non-author verifier has checked it; a wave seat cannot check its own box.
- [~] **At least one end-to-end domain task executed and logged in LOG.md** — **no new end-to-end domain
  task ran this round**; the `## Round 37` entry logs instruments, one admission and corrections, not a
  hunt-to-claim task `[MEASURE: LOG.md line]`. The closest executed measurement is the S054 capture +
  `source-recheck` + the E1–E14 closure suite, which is instrument work. Box stays open; considerthese
  proposal 2 records the missing round as not this round.
- [~] **Instructions executable by an agent without oral context** — `recheck-audit.py` `strict
  pass=49/49 expected=49 exit=0` `[MEASURE]`; `r37-closure.sh --selftest cases=14 failures=0` `[MEASURE]`;
  every knowledge recheck line `bash -n`-clean and `cd`-prefixed; the manifest/entry/row chain is
  three-way bound (header `source: S054` = recheck `--source S054` = manifest record id) `[MEASURE]`.
  Open: the suite's own bytes must be pinned by a digest inside the round's own receipt (D1's
  `suite-sha256=` header is that pin for the export, but the report must state where the pinned value
  lives), and only a non-author run closes the box.
- [~] **No cross-domain bleed (PROVINCE.md still accurate)** — F20 sits inside the province (program
  rules, claim packages; the F13/F16/F17/F18/F19 precedent) and lands as an end-of-file append;
  `ScoutF20Sibling` + `ExecSiblingSweep` rule `[MEASURE: contested/uncontested]` across 20 sibling lanes
  plus shokuknow, so nothing is absorbed and no report-to-lane item arises `[MEASURE: ConnSibling final
  ruling; PROVINCE append line]`. Box stays open on non-author verification.

## Round shape

- **One v2 wave**, `kasegi-r37-build`, dispatched through the inline spawn handoff (`wave1.ready`,
  L1 `KasegiR37`, hyaku run 9, attempt 1): counts `spawn 64 / resume 0 / total 64`; policy
  `waveMinLanes 64 / waveMaxLanes 128 / declaredMaxLanes 128 / hardCeiling 256`, `rampBatchSize 5`,
  `rampIntervalMs 700`, `globalRunnerCeiling 1056`; `compaction.applied = false`.
- **Role mix (registry, `.ufo/waves/round-37/wave1/swarm-registry.json`, 64 members, `agentId` null for
  all 64 because the inline handoff binds them):** executor 18, scribe 12, reviewer 10, critic 6,
  mutation-tester 5, scout 6, connector 3, sentinel 2, simplifier 2 → attack share
  (reviewers + critics + mutation-testers) **21/64 = 32.8 %**. Axis binding: 17 seats C1-only, 30
  coverage-only, 14 both claims, 3 calibration (`ScribeShonen`, `ScribeConsiderthese`, `SimplReport`).
  The planner seat is the L1 (orchestrator ruling 2026-10-19) and is not a wave member.
- **Dead seats:** at this draft `14/64` receipts are present in `.ufo/waves/round-37/wave1/`
  (`ls .ufo/waves/round-37/wave1/*.md \| wc -l` = 14 including this seat's) and 50 registry members have
  no receipt yet — that is in-flight, not dead `[MEASURE: receipts n/64 at wrap; wave1-results.json
  settled count; dead = member with no output after the wave settles]`.
- **Round total:** one wave / 64 seats / two claims (C1, C2) / one appended claims erratum / one
  admission (F20 = 20th frontier row) / `[MEASURE: wave1-results.json path, entry count, seats with final
  output]`.
- **Residual calls** (the L1 decides; none blocks this draft): (i) whether `r37-closure.sh` also gets a
  SKILL.md registry row this round, or whether the two exact basenames in the frozen claim are the whole
  obligation; (ii) the D5 repair form — append-only end-of-file correction versus an edit of
  `SKILL.md:1111`'s row (the row's type cell must change, which the append-only rule does not cleanly
  cover); (iii) whether the stale `Final lane commit: e666d902` outside the round-37 section
  (`SCORECARD.md:1492` at base, `corpus/lessons/round-36.md:3`) is corrected or left as round-36 history;
  (iv) considerthese proposal 4 (cap/externalise wave evidence) is an operator/LFS decision, and proposal
  1's thresholds plank stays open; (v) the round-32 L0 question (below).

**Stale-lane:** respawn-per-round driver; `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` reads
`2026-10-26T13:52:56-03:00 launch kasegi round=37 pgid=1603012 driver=hyaku-inline attempt=1`, preceded by
`2026-10-26T13:02:47-03:00 complete kasegi round=36; hyaku-inline attempt=1`; no other kasegi mission is
open `[MEASURE: state at filing; no complete line for round 37 while the report is written]`.

**Tooling installs:** none by this seat and none recorded in any seat receipt at this draft; no pacman
transaction was run (pacman is paused host-wide) `[MEASURE: confirm across all 64 receipts — scan for a
tool/version/channel line]`.

**Open L0 questions:** the kasegi **round-32** question remains open as last recorded
(`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:175`): `wave1.ready` (37 seats, validated) was
cap-deferred by the dispatcher and no seat ran, so the L1 landed the round with L1-only verifiable work;
the ruling wanted is re-dispatch with a swarm versus admitting the L1-only landing. Also still listed for
this lane: round-12 (bounties interactive-rebase stall), round-15 (PROVINCE re-point against the lost
`~/Projects/bounties` root), round-16 (second in-round source loss) and round-17 (round-namespace
reconciliation) — five kasegi rows in total (`grep -c '^kasegi' …/l0-questions.md` = 5). None blocks this
round `[MEASURE: confirm no new kasegi L0 row is filed this round]`.
