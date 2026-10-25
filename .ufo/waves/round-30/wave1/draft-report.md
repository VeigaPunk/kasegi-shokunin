# kasegi — Round 30 report (draft for L1 finalization)

Round: 30 · wave 1 (one v2 wave, 64 seats; hyaku run 7 inline spawn)
Lane: `kasegi-shokunin` · base `a94871315cafa368f79c17d8c62d71fddd967986` · freeze `3c5573541300ba0fd3d89372dda3d841172eaa3f` · dispatch HEAD `002e92ce07ed398334ef7cd8ca08d3fd99631351`
Frozen claims: `.ufo/waves/round-30/claims.json` (C1 depth:verifiability, C2 coverage)
Before receipts: `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`
After measurements: canonical snapshot at 2026-10-25T18:53:21Z, worktree bytes (integration commit pending) — `.ufo/waves/round-30/wave1/ScribeReport-canonical.txt`

## Work performed

- **C1 (depth:verifiability, 4 held) — instrument conformance for the frontier recheck harness and captured-source quote checker.** Fixes the round-29 mistakes M29-4 (harness crashes with uncaught `FileNotFoundError` on a missing entry; can pass pointing at an unrelated existing entry) and M29-3 (Q9 occurrence/stem binding not enforced; a record whose stem != id and a double-occurrence quote both pass with exit 0). Evidence: `ScoutInstrumentBaseline.md` (baseline reproduction), `c1-controls/before-run-2.txt`, `c1-controls/mutants/control-a1*.` (freeze-byte controls), instrument diffs in the working tree.
  - A1 limb: harness now fails closed with `problems=missing-entry` naming the row id (F98) instead of a traceback.
  - A2 limb: two admitted rows resolving to the same entry realpath fail with `DUPLICATE-ENTRY`.
  - B1 limb: `source-recheck.py` rejects a record whose capture stem != id with `reason=stem-mismatch`.
  - B2 limb: a non-unique quote without a verified anchor fails with `reason=occurrence-not-unique` (and anchor out-of-range/broken fail as `reason=anchor-out-of-range`/`reason=anchor-broken`); selftest covers all four double-occurrence sub-cases.
- **C2 (coverage, 7 held) — Frontier F14 "Japanese severity vocabulary and the handling-priority model" assimilation** from the read-only merge package `/home/vgpnk/Projects/shokuknow/merge/kasegi/`. Admitted entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (F14) citing S046 + S047 (first registered this round) plus already-registered S041; captures pinned in `corpus/source-snapshots/round-30/manifest.json`. Evidence: `ScoutAssimPackage.md`, `ScoutQuarantineSlice.md`, `assimilation/collisions`, `assimilation/reg-ids`, `assimilation/staged-ids`.
- **Proposal 4 mined** (`considerthese/2026-10-25.md`): proposals status ledger landed as `corpus/knowledge/considerthese-proposals-ledger.md` (`ExecConsiderthese.md`).

## Landed changes

Each will tie to a LOG.md round-30 entry and the integration commit hash once the L1 commits (hash not knowable at draft time):

- `corpus/instruments/frontier-recheck-count.py` — A1 named-row missing-entry fail-closed + A2 duplicate-realpath detection (+63/−? lines; worktree sha256 `aa60b581…`)
- `corpus/instruments/source-recheck.py` — B1 stem check + B2 occurrence/anchor fail-closed + selftest 9 cases (worktree sha256 `33602a9d…`)
- `corpus/source-snapshots/round-30/` — captures `S046.txt`, `S047.txt`, `S041.txt` + `manifest.json` (sha256 `dfc88357…`; 3 records, 12 assertions)
- `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` — F14 entry (sha256 `f584f06c…`; source trio S046/S047/S041; recheck line `bash -n` clean, cwd-independent)
- `corpus/knowledge/considerthese-proposals-ledger.md` — proposal-4 ledger (sha256 `7574b776…`)
- `corpus/SOURCES.md` — rows S046, S047 appended (registry 45 → 47; no pre-existing row cell changed, R8)
- `corpus/README.md` — F14 frontier row + coverage-map appendix row appended (R6; frontier admitted 13 → 14)
- `SKILL.md` — append-only (+10 lines) per `git diff --stat`; [pending ScribeSkillGate confirmation]
- `corpus/instruments/knowledge-expected.txt` — regen owed for the two new knowledge files (recheck-audit currently `unexpected=2`; see close-out)

## Before → after measurements

Counting command per claim: the frozen `counter_commands` from `claims.json` (each run from the lane root; after-run at the 18:53:21Z snapshot).

### C1 — depth:verifiability

| probe | before (frozen receipt) | after (measured) |
|---|---|---|
| A1 missing-entry | exit 1, uncaught `FileNotFoundError` traceback, row id F98 absent | **exit 1**, `FAIL F98 … problems=missing-entry`, `entries=1 pass=0 exit=1` |
| A2 duplicate target | exit 0, `entries=2 pass=2 exit=0` on duplicate | **exit 1**, `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`, `entries=2 pass=2 exit=1` |
| B1 stem mismatch | exit 0, `S043:Q1 OK` (stem S045 passes) | **exit 1**, `S043:manifest MISMATCH reason=stem-mismatch` |
| B2 double occurrence | exit 0, `occurrences=2 anchor=MISSING` | **exit 1** (see finding F-1: the committed B2 fixture trips `reason=stem-mismatch`; the occurrence limb is exercised by the selftest double-occurrence case, which exits 1 with `reason=occurrence-not-unique`) |
| real corpus | harness `entries=16 pass=16 exit=0` | harness `entries=17 pass=17 exit=0` (F14 line present) |

Instrument digests: frontier harness `c8a62888…` → `aa60b581…`; source-recheck `9fe6a4a0…` → `33602a9d…`. `source-recheck.py --selftest` → `selftest cases=9 failures=0`, exit 0 (stem-mismatch, double-occurrence, double-occurrence-anchored, out-of-range, broken all PASS).

### C2 — coverage

| counter | before | after |
|---|---|---|
| frontier admitted (README awk) | 13 | **14** |
| entries citing `^source: S04[6-7] ` | 0 | **1** (F14 entry) |
| `S04[6-7]` registry rows | 0 | **2** (S046, S047) |
| registry rows (`grep -cE '^\|…S[0-9]{3,}…'`) | 45 | **47** |
| census (`sources-census.sh validate …`) | exit 0, 45 rows, W04 S028/S029 | **exit 0**, 47 rows, W04 S028/S029 only |
| frontier harness | entries=16 pass=16 exit=0 | **entries=17 pass=17 exit=0** incl `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047` |
| per-id source-recheck (round-30 manifest) | no round-30 manifest existed | S046/S047/S041 each **exit 0**; 12 assertions OK (S047 Q1/Q3 non-unique but anchored `anchor=123-ok` / `anchor=130-ok`) |

## Sources & frontier

- SOURCES rows 45 → **47**; rows added: **S046, S047** (both tier A, mined, opened 2026-10-25; recheck 180d/90d; used-by the F14 entry). Staged `SOURCES.append.md` S049/S050 landed with re-stamped opened date and anchors rewritten from the round-30 captures; staged prose anchors not carried.
- Rows touched old→new: **none** (S041–S045 untouched; only additions, marginal8).
- Census command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0; W04 S028/S029 (pre-existing) only.
- Frontier rows advanced: 13 → **14** (F14 admitted; denominator 14/14).
- Assimilation theme: "Japanese severity vocabulary and the handling-priority model"; staged rows adopted by document (S049→S046, S050→S047; S043→S041 already registered). Quarantine slice: 7 rows (S037, S054, S048, S065, S068, S069, S070) hand-checked this round — verdicts per row land in the lesson Gate.
- considerthese: proposal 4 (proposals status ledger) mined and landed this round (`considerthese-proposals-ledger.md`).

## Trend verdicts

- **expansion: improved** — new frontier row F14 (13→14) with one admitted knowledge entry on uncovered ground; registry 45→47; both `source:` rows registered this round.
- **quality: improved** — all 17 entries re-verified by the harness (pass=17, exit 0); per-id source-rechecks all pass; C1 instruments strengthened (A1/A2/B1/B2 fail-closed, selftest 9/9); census exit 0.
- **discernment: [pending]** — Gate admit/reject verdicts and the non-author spot-check re-opens land in the lesson (ScribeLesson / RevC2Entry); draft has no independent determination beyond the measured counters.

## SHONEN

- Box 1 (SKILL decision tables / patterns / checklists / cited sources): `[~]` — evidence `corpus/instruments/density.py SKILL.md` mean 154.0, 652 cites, 19 blocks; `anchorcheck.py SKILL.md` bad=0 (round-25 receipts).
- Box 2 (end-to-end domain task executed and logged in LOG.md): `[~]` — evidence LOG.md round-25 entry; round report `.ufo/reports/round-25/kasegi.md`; both claims land with measured before→after receipts.
- Box 3 (instructions executable without oral context): `[~]` — evidence every `corpus/knowledge/*.md` recheck line is one cwd-independent command; `recheck-audit.py` executes=18 gated=25 broken=0; `frontier-recheck-count.py` entries=17 pass=17 exit=0.
- Box 4 (no cross-domain bleed): `[~]` — evidence PROVINCE.md frontier F01–F14; `ScoutAdjacency.md` report (pending in wave) confirms no sibling lane holds F14 ground.

## Stale-lane

None: lane HEAD `002e92ce` is this round's dispatch commit; base and freeze commits are ancestors (`git merge-base --is-ancestor` exit 0 for both). Production edits are present in the working tree awaiting the integration commit.

## Tool installs

None by this seat (no tool installed/upgraded; no pacman transaction; lane bounds respected).

## Close-out owed (L1)

1. Integrate; record commit hash; append LOG.md round-30 entry (ScribeLog) and SCORECARD round-30 section (ScribeScorecard).
2. Regenerate `corpus/instruments/knowledge-expected.txt` for the two new knowledge files → `recheck-audit.py` `expected=43 missing=0 unexpected=0 exit=0` (currently `expected=41 unexpected=2 exit=1`).
3. Run post-commit recheck (`wave1/ExecPostCommitRecheck.md` / `post-commit-recheck.sh`) at the integration commit.
4. Lesson assembly with Gate verdicts, mistakes M30-*, quarantine verdicts, spot-check.
