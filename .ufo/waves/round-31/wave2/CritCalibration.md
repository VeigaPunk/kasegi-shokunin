# CritCalibration — round 31, wave 2 (AXES calibration: self-assessment vs observed state)

Seat: CritCalibration (critic). Round 31, lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope). Base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`. HEAD at measurement: `eecad59` (wave-1 integration). Answering model: `opencode-go/deepseek-v4.1-flash` (harness route; this seat passed no model). Tools installed/upgraded: none (no pacman transaction; nothing added to `~/.local/bin`). No git/jj mutation; no subagent dispatch; no live fetch.

## Measurement state (bound 6: pre-state labelled, in-flight non-comparative)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && date -u +%Y-%m-%dT%H:%M:%SZ && git status --porcelain -- corpus/ SKILL.md SHONEN.md SCORECARD.md PROVINCE.md LOG.md
```

```text
2026-10-26T00:31:46Z
(no output — quiescent for every path below)
```

```text
d058f5664a660ab6…  SHONEN.md            (last commit touching it: 98261eb, round 25)
5fa41aef7c8e795e…  SCORECARD.md
d9865b2e126c6265…  corpus/README.md
e41eca75bb03bcaf…  corpus/instruments/README.md
817636048968caf9…  SKILL.md
5d4842da6103f17c…  corpus/instruments/recheck-audit.py
```

Four live-path writers are still in flight in wave 2 (`corpus/QUALITY.md` → ScribeQualityFix, `SCORECARD.md` → ScribeScorecard, `SHONEN.md` → ScribeShonen, `corpus/lessons/round-31.md` → ScribeLesson). Every value below is at the digests above; re-run on quiescent close-out bytes before citing.

## 1. Observed state on the landed bytes (the "observed" column's commands)

```sh
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md   # 15
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                            # 48
grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md                                  # 1
grep -lE '^source: S048 ' corpus/knowledge/*.md | wc -l                                         # 1
ls corpus/knowledge/*.md | wc -l                                                                # 44
python3 corpus/instruments/frontier-recheck-count.py                                            # entries=18 pass=18 exit=0
python3 corpus/instruments/recheck-audit.py --quiet                                             # strict pass=44/44 … exit=0
python3 corpus/instruments/density.py SKILL.md --label critcal                                  # mean 191.5, 24 blocks, 689 cites
python3 corpus/instruments/anchorcheck.py SKILL.md                                              # 7 in-range, 0 bad, LOST-RECORDED=306
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json  # 13/13/0, controls 3/3, exit 0
python3 corpus/instruments/source-recheck.py --selftest                                         # cases=10 failures=0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi  # exit 0 (W04 S028/S029 only)
```

Key outputs, verbatim (abridged to the lines the table cites):

```text
entries=18 pass=18 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0

strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0

# Density census — critcal (1071 lines, 24 blocks)
| | **mean dens** | | | | | | | | **191.5** |
Total path-citation instances: 689 across 24 blocks.

== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchor_exit=0

LIMB RA-parse live=0/y mutant=1/n verdict=killed
… 13 LIMB lines, every one killed …
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

Counter side-checks: stdout sha256 `9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838` (matches `corpus/instruments/README.md:487-488`), `--selftest` → `selftest cases=20 failures=0`, and the counter writes nothing into the lane (`find corpus -newer <10s-marker> -type f` → empty after a full run). Elapsed on this host: **14 515 ms** (single run, `date +%s%N` delta; two earlier runs 18.0 s / 23.9 s under concurrent load).

C1/C2 frozen-predicate check: all six C2 counters and both C1 summary lines match `claims.json` exactly; the C1 do-nothing-control base digests reproduce (`git show b374febbb:corpus/instruments/{recheck-audit,source-recheck,frontier-recheck-count}.py | sha256sum` → `3fc0d751…`, `33602a9d…`, `aa60b581…`).

## 2. Self-assessment vs observed — mismatch table

`stale-live` = the line reads as current state and is now wrong. `historical-ok` = dated/superseded statement whose value was correct in its stated frame (R6/R9 append-only), kept as history.

| # | path:line | statement | observed value (command) | classification |
|---|---|---|---|---|
| 1 | `SHONEN.md:6-8` | "density.py SKILL.md mean 154.0, 652 path-citation instances, 19 blocks" | mean **191.5**, **689** instances, **24** blocks (1071 lines) — `density.py SKILL.md --label critcal` | **stale-live** |
| 2 | `SHONEN.md:14` | "recheck-audit.py exits 0 with `executes=14 gated=23 broken=0`" | `strict pass=44/44 … executes=20 gated=24 broken=0 … exit=0` — `recheck-audit.py --quiet` | **stale-live** (also understates the audited set: 14 → 20 executes, 35 → 44 lines) |
| 3 | `SHONEN.md:15` | "`frontier-recheck-count.py` entries=12 pass=12 exit=0" | `entries=18 pass=18 exit=0` incl. `PASS F15 … ids=S048` — harness run above | **stale-live** |
| 4 | `SHONEN.md:17` | "PROVINCE.md frontier F01–F10" | frontier admitted **15** (`awk … admitted` over `corpus/README.md`); `PROVINCE.md:45-70` already carries the r31 amendment naming F12–F15 | **stale-live** (pointer range; the file's own amendment is correct) |
| 5 | `SHONEN.md:10` | "round report `.ufo/reports/round-25/kasegi.md`" | absent under the lane root: `ls .ufo/reports/` → `round-21` only; `git log --all --oneline -- .ufo/reports/` → one commit `2baaff8`. The file exists only at the **fleet** root (9 113 B): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-25/kasegi.md` | **stale-live** (broken as written; smallest fix: qualify `../../../.ufo/reports/…`, the idiom `corpus/README.md` already uses for `l0-questions.md`) |
| 6 | `SKILL.md:1069` | "counter `f926bf75…` (the merge receipt's FINAL was `cde7c2b6…`…)" | landed/committed counter digest is **`c660a95f…`** (`sha256sum`, and `git show eecad59:corpus/instruments/limb-mutation-check.py`); `git cat-file --batch-all-objects --batch-check` contains **no** object hashing to `f926bf75`; `corpus/instruments/README.md:445-446` documents the whole chain `9e729daf → eb9b87ff → b4223ed9 → cde7c2b6 → bd18c244 → c660a95f` and measures at `c660a95f` | **stale-live — unresolvable digest (false provenance)** |
| 7 | `SKILL.md:1069` | "Counter exit 0 in ~10 s from the lane root" | exit 0 — measured **14 515 ms** (two earlier runs 18.0 s / 23.9 s while siblings ran) | **stale-live (minor)**; environment-dependent, so recommend "≈10–24 s under load" rather than a new point value |
| 8 | `SCORECARD.md:839` | "the audit now prints `strict pass=43/43 …` and `expect=present expected=43…`" | live **`strict pass=44/44`**, `expected=44`, `executes=20`, on `recheck-audit.py` `5d4842da…` (base `3fc0d751…`) | **stale-live** (present tense; superseded by the 44th entry + instrument edit that landed at `eecad59`). The erratum's own conditional at `:858` ("If recheck-audit.py bytes change later this round … re-run and label any new value with its date") is **triggered**: bytes changed. The re-run exists only at `SKILL.md:1069` and `corpus/knowledge/considerthese-proposals-ledger.md:35`, never in `SCORECARD.md` |
| 9 | `corpus/instruments/README.md:16-18` | "`citation-survival.md` / `.tsv` are the **current census of record**, regenerated in round 18" | git: last change is `644ed37` — "round-20: … kasegi census regeneration" (and `SCORECARD.md:134` records an r19 regeneration), not round 18. The file still reports 1 480 distinct / SKILL 506 / `134/1480 = 9.05 %` / "50 files". Same instrument, same definition, re-run read-only in a `mktemp` copy of today's corpus (`resolve.py <copy>`, never the lane): **2 263** distinct, SKILL **547**, `47/547 = 8.59 %`, lane `260/2263 = 11.49 %`, 85 files | **stale-live** — "current census of record" is 11 rounds old and both rates have moved 6.32 % → 8.59 % and 9.05 % → 11.49 %. Caveat: scratch copy at a non-canonical path (the instrument writes, and this seat is read-only on the lane), so record it as a direction + magnitude, not a byte-identical lane-root value |
| 10 | `corpus/instruments/README.md:1-3` | "Three stdlib-only, deterministic scripts" | `ls corpus/instruments/*.py` → **12** (11 instruments + `test_resolve.py`), plus `limb-ledger.json`, `limb-fixtures/`, two fixture matrices and the two snapshot manifests | **stale-live** (header inventory of a file that now indexes the whole set; later sections are correct) |
| 11 | `corpus/README.md:74-76` | "only 1 of 21 `knowledge/*.md` entries … carries an explicit pin so far — pinning the other 20 is the r16 … move" | **44** knowledge entries; **44** carry `source:`; **30** match `pin|blob` (`grep -liE 'pin|blob' corpus/knowledge/*.md \| wc -l`); r16 is 15 rounds past | **stale-live** (Known-gaps bullet never re-based) |
| 12 | `corpus/README.md:35` | instrument row source basis "`instruments/{density.py,resolve.py,anchorcheck.py,mirror-containment-check.py,source-recheck.py,README.md}`" plus r23/r24 additions | 11 committed instruments, incl. `capture-source.py`, `recheck-audit.py`, `frontier-recheck-count.py`, `resolve-dispatch-check.py`, `score-gap.py`, `limb-mutation-check.py` + `limb-ledger.json` — the live coverage-map row enumerates neither r25–r31 additions nor an amendment that does | **stale-live** (incomplete enumeration) |

### Historical-ok rows that look wrong (deliberate discrimination)

| # | path:line | statement | why it is historical-ok |
|---|---|---|---|
| H1 | `SCORECARD.md:813-819` | "`expect=present expected=43 missing=0 unexpected=0 exit=1`" | Round-30 result paragraph; named and superseded by the appended r31 erratum at `:839`, which is exactly the M31-1 fix. Filed bytes stay (R6/R9). |
| H2 | `SCORECARD.md:843-856` | dated block "Measured 2026-10-25T23:33:27Z" → `strict pass=43/43`, `executes=19` | Carries its own UTC stamp **and** digest pin (`3fc0d751…`); it is a correctly labelled pre-integration receipt, not a live claim. It is pre-state for the wave-1 integration at `21:16:52-03:00` (= `00:16:52Z`). |
| H3 | `SCORECARD.md:858` | base export "prints `strict pass=1/43 cdroot_fail=42 …`" | Reproduced exactly, today: `git archive b374febbb \| tar -x -C $(mktemp -d)`, 43 knowledge files, instrument `3fc0d751…` → `strict pass=1/43 cdroot_fail=42 instrument_fail=0 own_fail=0 … exit=1`. |
| H4 | `SCORECARD.md:839` | ledger pin "sha256 `d91889e5…`" | `git show bc1a1e1:corpus/knowledge/considerthese-proposals-ledger.md \| sha256sum` → `d91889e5…` — the pin is true for the round-30 close bytes it names. Live is `c354ca02…` (round-31 append), and `:5` is byte-identical live, so the pin's substance holds; reader trap only. |
| H5 | `SCORECARD.md:825` | "(last capability entry round 25)" | Corrected in the same file by the appended capabilities errata (`source-capture-pdf`, round 26, `:580-584` — verified those lines are the round-26 capabilities table). |
| H6 | `corpus/README.md:217, :288` | "11/11 admitted at round 26"; "**14/14 admitted**" | Both round-scoped and explicitly restated as history by later amendments; the live statement at `:313` says "**15/15 admitted**" and matches the measured 15. |
| H7 | `PROVINCE.md:36-41` | "Frontier F01–F10 … 10/10 admitted" | The r31 amendment at `:45-70` names F12–F15 and declares the parenthetical history; its pointers `:64` → `corpus/README.md:213 / :264 / :284` resolve to the F12 / F13 / F14 rows (verified). |
| H8 | `corpus/README.md:36, :44` | Lessons rows "round-1.md … round-15.md"; "(25 files; gaps at 2, 16, 18, 19)" | `:44` explicitly corrects `:36`; both are round-labelled snapshots. (Live: **42** lesson files — see gap G2.) |
| H9 | `corpus/README.md:5` | entry-count chain "… r25 correction: the round-25 entry count is 37" | Every clause is round-scoped and true for its round (37 + 2 (r26) + 1 (r28) + 1 (r29) + 2 (r30) = 43 at base; 44 now). Chain simply stops — see gap G1. |
| H10 | `corpus/instruments/README.md:451-465, :487-488` | six landed digests; stdout sha256; `selftest cases=20` | All verified byte-for-byte on the landed bytes (`5d4842da…`, `fd2e01e8…`, `aa60b581…`, `c660a95f…`, `c042adf6…`, `855869bf…`; stdout `9b386485…`; `cases=20 failures=0`). |

Mismatch count: **12 stale-live**, **10 historical-ok** (out of 22 rows that carry a checkable number or pointer in the files named by this item).

## 3. Calibration gaps with no wrong number (L1 decides, no erratum target)

- **G1 — no live entry-count line.** `corpus/README.md:5` stops at 37 (r25); `knowledge-expected.txt` and the audit hold the basis at **44 entries / 46 lines**. Nothing states 44 in the index; the audit is the only live basis. Fix shape: one appended sentence, not a rewrite of `:5`.
- **G2 — no live lessons inventory.** Live **42** `corpus/lessons/*.md`; the map's newest row dates to r22 (25 files). Largest single stale coverage statement in the index, and it is coverage-map content, not a log.
- **G3 — counter verdict enum is a superset of the frozen interface.** `claims.json` C1 freezes `invalid:live-baseline|find-count|noop|nocompile`; the counter implements those **plus** `invalid:import`, `invalid:mutant-baseline`, `invalid:timeout` (`grep -oE 'invalid:[a-z-]+' limb-mutation-check.py`). `corpus/instruments/README.md:399-401` discloses the extension and says it "is routed to the L1 rather than silently widened" — so this is disclosed drift, not a hidden one. It still needs an interface amendment (or an explicit L1 acceptance) because the C1 kill rule cannot see the added verdicts: a limb whose repeated mutant runs disagree prints `invalid:mutant-baseline` where the frozen contract defines only `killed`/`survivor`, and an `invalid:import`/`invalid:timeout` row replaces what the contract would have scored. Nothing is hidden by the summary — `exit 0` requires every limb verdict to be `killed` (`limb-mutation-check.py:61-62`), so any invalid row fails the run — but the verdict vocabulary in the receipt is wider than the frozen interface.
- **G4 — `corpus/QUALITY.md:95-96` (R16/R17) ground in `corpus/lessons/round-31.md`, which is ABSENT** at measurement (`ls corpus/lessons/round-31.md` → missing; ScribeLesson in flight). If that seat lands, re-check; if it does not, two frozen criteria cite a non-existent record at close.
- **G5 — score-5 bar lives only inside a round-22 table row.** `score-gap.py` resolves it at `SCORECARD.md:331`, which is the round-22 evaluation row; the `Axes`/`Planned` sections never restate it. Reproducible today (`threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."`), but the axis definition depends on one English sentence inside a historical row — a later append that rewords it makes the reporter `exit 2` (its own selftest covers the reword, so the failure is loud, not silent).

## 4. Answers to the specific probes in this item

- **Counts that "should now say 48 / 15 / 18 / 44":** every live *counter* agrees — registry **48**, frontier **15**, harness **entries=18 pass=18**, entries **44**, S048 rows **1**, entries citing S048 **1**. The stale numbers live in prose pointers (`SHONEN.md`, `corpus/README.md:74-76`, `corpus/instruments/README.md:1-3/16-18`), not in the counters.
- **`strict pass=43/43` occurrences:** three, all in `SCORECARD.md` — `:839` (present tense → stale-live), `:841` (a pointer saying `round-30.md` "records … the final `strict pass=43/43`" — true of that lesson), `:852` (dated block, historical-ok). None of them is the live value.
- **`entries=17`, `14/14 admitted`, `43 entries`:** no live-claim occurrence survives. `entries=17` appears only in the round-30 section (`SCORECARD.md:794, :835`) and `LOG.md` round-30/31 appends; `14/14` only in the r30 amendment (`corpus/README.md:288`); "43 … entries" only in dated receipts/lessons. All historical-ok.
- **SHONEN evidence pointers:** `ScoutNoHarm.md` (11 229 B) resolves; `LOG.md` round-25 entry resolves; `.ufo/reports/round-25/kasegi.md` does **not** resolve from the lane (row 5); `PROVINCE.md frontier F01–F10` resolves but is superseded in-file (row 4).
- **SCORECARD axes vs cited counters:** no axis score contradicts its counter. depth:verifiability 4 vs the score-5 bar (gap line `24 of 44 rechecks still gated…`) is consistent; coverage 7 while frontier is 15/15 is the documented lost-denominator split; depth:density 9 with mean 191.5 > `BAR_R15 = 142.5` is disclosed as a metric move, not claimed as a score move (rounds 29/30 posture, unchanged).

## 5. Limits of this review (published, not hidden)

- The census re-measurement (row 9) ran on a `mktemp` copy at a non-canonical path because `resolve.py` writes its census; the lane stayed read-only. Direction and magnitude are safe; a lane-root number would need a writer seat.
- Timing (row 7) is host- and load-dependent; the counter's own digests match on every run, so only the wall-clock sentence is at issue.
- `SHONEN.md`, `SCORECARD.md`, `corpus/QUALITY.md` and `corpus/lessons/round-31.md` have named wave-2 writers. This seat wrote only this receipt; every fix above is routed to the L1 and to those seats.
- No file outside `/home/vgpnk/Projects/shokunin/kasegi-shokunin` was written; the `git archive` base export and the resolve scratch copy were deleted after use.
