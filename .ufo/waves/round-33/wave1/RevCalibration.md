# RevCalibration — round-33 calibration attack (AXES: self-assessment vs observed state)

- Seat: RevCalibration (reviewer, leaf; no delegation, no installs, no scratch left).
- Lane: kasegi-shokunin. HEAD at measurement start `a6a5023` (wave-1 spec/dispatch); claims-freeze `6e55c8d`; lane base `690b69da`.
- Answering model (rule 10): `zai/glm-5.3-flash`.
- Byte state: **wave-1 bytes were uncommitted working-tree edits landing while I measured** (M30-3). Every block below carries its UTC timestamp and the tree state it read. The canonical quiescent runs belong to ExecRegressionC1 / ExecHarnessC2 / ExecCensusAfter and the L1's post-commit re-run; re-run every counter in §4 on committed bytes before citing any number here as round-final.
- Lane writes: this receipt only.

## 1. Mismatch count and the two true standing defects (committed bytes)

Two mismatches exist on **committed** bytes today and have **no owner this round**; the rest of the count is in-flight landing state (§2) or verified-consistent history (§3).

### M1 — MEDIUM — SCORECARD's per-round ledger skips round 32 entirely (committed, no owner this round)

`SCORECARD.md` ends at `### Round-31 final addendum — residual call wave4` (`SCORECARD.md:978-980`, file end). Round 32 is committed history — LOG entry, frozen claims, honest stop, non-author verdict:

```sh
grep -n '^## Round' SCORECARD.md | tail -4
# 908:## Round 30 — frozen claims C1/C2 (2026-10-25)
# 862:## Round 31 — frozen claims C1/C2 (2026-10-25)   (last round section; final addendum ends the file)
grep -n '^## Round 32' LOG.md
# LOG.md:1593:## Round 32 — 2026-10-25 — honest stop: claims frozen, wave-1 spec validated, no seat ran (run-7 dispatcher cap 0) — re-dispatched as round 33
git log --oneline -1 690b69d
# 690b69d round-32 verifier spot-check (integrator, hyaku): non-author admit/reject
```

Precedent: the round-27 honest stop **does** have a SCORECARD section (`SCORECARD.md:590`, "Round 27 — … honest stop, NOT VERIFIED"). Round 32's verdict ("rejected-honest-stop", defects D1–D6 routed) lives only in `corpus/lessons/round-32-verifier-spotcheck.md` and `LOG.md:1593`. A reader of SCORECARD alone sees no round 32. Verified no seat covers it: `wave1-spec.json` prompts mentioning round-32 (ScoutDatawalk, ScoutLiveDrift, ConnClaims, ExecManifest*, ExecEntryF16, ExecRegistryAppend, ExecHarnessC2, ExecErratumCheck, ScribeLesson, reviewers) — none instructs a SCORECARD round-32 note; ScribeScorecard's item appends `## Round 33 — frozen claims C1/C2 (2026-10-26)` only. Fix: one appended note in the round-33 section naming the round-32 honest stop and its spot-check verdict (append-only; no history rewrite).

### M2 — MEDIUM — the depth:verifiability census of record contradicts observed state, and is routed-open with no owner this round (committed)

The SCORECARD proxy section names `corpus/instruments/citation-survival.md` the census of record for `resolve.py` (`SCORECARD.md:28-31`, "Census of record: `corpus/instruments/citation-survival.md`"), and the Axes table's depth:verifiability evidence pointer rides on it. The committed census is round-20-stale:

```sh
sed -n '33p' corpus/instruments/citation-survival.md
# - lane total (SKILL.md + corpus): **134/1480 = 9.05%**
grep -n '9.05' SKILL.md | head -1
# SKILL.md:1071: ... `census-lane: 134/1480 = 9.05%` and `census-skill: 32/506 = 6.32%` quoted from `corpus/instruments/citation-survival.md` ...
```

Round-31 wave-2 measured the same definition on final bytes at `388/2263 = 17.15%` (`corpus/lessons/round-31.md` open item 11; `.ufo/waves/round-31/wave2/ExecNoHarmDensity.md` §6 — receipt-recorded, not re-run by me). Both stale figures are attributed quotes, the direction of error understates the lane, and the debt is routed — but no round-33 seat owns `citation-survival.md` or the SKILL.md:1071 figure (FILE OWNERSHIP: instruments read-only except `capture-binding-check.py`; SKILL.md is ScribeSkillGate's, whose item covers only the capture-binding-check row). The census of record will still read 9.05% at round-33 close while the observed state is ~17%. Fix route: regenerate the census in a scratch tree and append an erratum line to the instrument README/lesson, or record it again as routed-open with the new round number.

### M3 — LOW — M31-3 anchor drift grew: `corpus/lessons/round-29.md:214` cites `corpus/SOURCES.md:83` (committed, no owner this round)

```sh
grep -n 'SOURCES.md:83' corpus/lessons/round-29.md | head -1
# 214:`corpus/SOURCES.md:83` (raw 153-record array → record-scoped capture; ...)
sed -n '83p;90p' corpus/SOURCES.md | cut -c1-40
# 83: ## Registry changes
# 90: Change cell old → new: the S043 anchor originally described ...
```

The S043 change cell sat at `:85` at base, `:87` when M31-3 was filed (off by +4), and is now `:90` (off by +7) after the round-33 S049/S050 appends. Recorded open by round-31 (M31-3, "correction belongs to `corpus/lessons/**`"); no seat owns `lessons/round-29.md` this round. Line-number cites into append-vulnerable files keep decaying each round — a recurring class worth one QUALITY row eventually.

## 2. Live-claim lines that read stale only against the landing wave (owner assigned, in-flight)

These are **not** defects of committed self-assessment — on committed bytes each line was true at its round. They are the expected mid-round skew, with owners in the spec; I verified each owner's fix had or had not landed at my timestamps.

### M4 — SHONEN.md box evidence (untouched at 04:30:09Z; ScribeShonen polling)

```sh
git status --porcelain -- SHONEN.md SCORECARD.md      # 04:30:09Z: empty (both untouched)
sed -n '28p' SHONEN.md   # `recheck-audit.py --quiet` prints `strict pass=44/44` and
sed -n '20,22p' SHONEN.md # census exits 0 with the harness at `entries=18 pass=18 exit=0` ... No round-31 LOG.md entry exists yet ...
```

- 04:21–04:27Z, landing bytes: knowledge entries 45 (`ls corpus/knowledge/*.md | wc -l`), `recheck-audit.py --quiet` → `strict pass=45/45 … exit=1`, `expect=present expected=44 missing=0 unexpected=1 exit=1` (the documented failure mode of `corpus/README.md` § Round-28 reconciliation). SHONEN.md:28 said "the 44 entries … `strict pass=44/44`".
- 04:30:09Z, after ExecExpectedList: `strict pass=45/45 … expected=45 missing=0 unexpected=0 exit=0`; `knowledge-expected.txt` 47 lines / 45 entries. SHONEN.md still says 44 — stale until ScribeShonen appends. Named re-run: `python3 corpus/instruments/recheck-audit.py --quiet` on committed bytes.
- SHONEN.md:20-22 additionally asserts "No round-31 `LOG.md` entry exists yet at HEAD `eecad59`; the box stays `[~]`" — false as a present-tense claim since `d24f700` landed `LOG.md:1584` ("## Round 31 — 2026-10-25 — one-limb mutation ledger …"). Calibration direction: the box understates — the round-31 LOG entry plus its receipts arguably satisfy box 2's requirement ("at least one end-to-end domain task executed and logged in LOG.md"), so the checklist may deserve `[x]`, not a refreshed `[~]`.

### M5 — the rest of the should-now-say set (all landed by 04:30:32Z; owners verified)

| should say | measured | landed at |
|---|---|---|
| registry 50, S049/S050 rows 1/1 | `grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md` → 50; S049=1, S050=1; rows at `SOURCES.md:55-56` | 04:28:58Z (ExecRegistryAppend) |
| frontier 16/16 | `awk -F'\|' '$2 ~ /^ \*F[0-9]+ / && $4 ~ /^ \*admitted \*$/ {n++} END{print n}' corpus/README.md` → 16; F16 row `corpus/README.md:335`; r33 amendment `:339` "16/16 admitted" | 04:28:58Z (ScribeReadmeF16) |
| harness entries=19 pass=19 | `python3 corpus/instruments/frontier-recheck-count.py` → `entries=19 pass=19 exit=0` incl. `PASS F16 … ids=S049,S050` | 04:28:58Z |
| source-recheck S049/S050 exit 0 | both → `exit=0` on `corpus/source-snapshots/round-32/manifest.json` | 04:28:58Z |
| census exit 0, W04 S028/S029 only | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → the two W04 lines + ok, `census_exit=0` | 04:28:58Z |
| PROVINCE names F16 | `PROVINCE.md:74` end-of-file append "F16 — Chinese crowdsourced-testing platform scope and reward rules … admitted round 33" | 04:28:13Z (ScribeProvince) |
| SKILL gate\|probe row | `SKILL.md:1077` capture-binding-check.py row + `:1079` provenance note | 04:28:13Z (ScribeSkillGate) |
| instruments README section | `corpus/instruments/README.md:513` "## Round-33 additions — `capture-binding-check.py`" | 04:28:13Z (ScribeInstrReadme) |
| QUALITY R20/R21 | `corpus/QUALITY.md:160` "## Round-33 additions" with R20 (manifest-in-same-commit) + R21 (url/fetched_utc provenance) | 04:28:13Z (ScribeQuality) |
| C1 counters | `python3 corpus/instruments/capture-binding-check.py` → `records=40 bound=40 unbound=0`, exit 0; `--selftest` → `cases=11 failures=0`, exit 0, all six contract-named cases present | 04:28:58Z |

### M6 — M30-3 timeline (why any single mid-round number lies)

The same counters printed three different states within ten minutes: 04:21Z knowledge=44-era audit green; ~04:27Z knowledge=45 with `unexpected=1` audit exit 1 and C1 exit 1 (`FAIL rule=no-row record=S049/S050`, `records=40 bound=38 unbound=2`, `multi_row_url=2`) because the registry rows lagged the entry; 04:28:58Z all C1/C2 counters green. Any seat scoring C1 or SHONEN box evidence between 04:2x–04:28Z on in-flight bytes would have filed a false failure. Rule holds: timestamp + quiescence statement with every digest, and cite only the settled state.

## 3. Verified-consistent (calibration passes; commands + outputs)

- **SKILL.md integrity**: sha256 `817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7` — byte-identical to SHONEN.md:5-7's claim; `git status --porcelain -- SKILL.md` → 0 (until the ScribeSkillGate append at 04:28:13Z, which is R6-licensed).
- **density/anchorcheck reproduce SHONEN.md:8-19 exactly** (04:2xZ): `density.py SKILL.md` → mean `191.5`, `24 blocks`, `689` cites, exit 0; `anchorcheck.py SKILL.md` → `7 in-range cite instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0. After the SKILL append (04:30:32Z): `12 in-range cite instances, 0 bad` — the five new SKILL.md:1077-1079 anchors all resolve (`capture-binding-check.py` is 492 lines; `SOURCES.md:55-56` are the S049/S050 rows).
- **Recorded instrument digests all current**: `limb-mutation-check.py` `237fd07c…`, `recheck-audit.py` `5d4842da…`, `source-recheck.py` `fd2e01e8…`, `frontier-recheck-count.py` `aa60b581…`, `knowledge-expected.txt` `d6f25227…` (pre-regen) — each equals the digest pinned in SCORECARD.md:949-954 / SHONEN.md:27.
- **SHONEN evidence pointers resolve with their quoted outputs**: `.ufo/waves/round-31/wave2/ExecRegressionC1.md:81-82` (`limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`); `ExecCensusFinal.md:83,110` (`entries=18 pass=18 exit=0`, `PASS F15`); `ExecNoHarmDensity.md:84,165` (`191.5`, `11/27 = 40.74%`); `LOG.md:1469` = the round-30 entry; the four `.ufo/waves/round-31/…` receipt files all exist.
- **Base controls reproduce**: harness `entries=18 pass=18 exit=0` and census W04 ×2 exit 0 at the round-33 base state — matching claims.json `do_nothing_control` and `c2-controls/before.txt` claims; round-32 spot-check's re-measurements (frontier 15, registry 48, knowledge 44 at `762bfe95`) consistent with everything I measured.
- **Axis scores vs receipts: no contradiction.** 9/4/7 consistent across the Axes table, every per-round before/after table, the Saturation declarations, and claims.json (`saturation: line 9/10 per owned axis, N=3; lowest depth:verifiability (4)`). Coverage 7 held in every receipt round 22–33frozen; verifiability 4 held; density 9 with the round-31 mean move honestly refused as credit (block-24 resolve fraction 40.74% < 60% bar).
- **No capability row without a demonstrated run**: round-22 `sources-registry` → `corpus/lessons/round-22.md` §Gate census block (grep `Census` → 1); round-24 `frontier-recheck-harness`/`source-capture` → `.ufo/waves/round-24/c1-counterA-{after,before}.json` exist; round-25 rows → `c1-receipt-index.txt` exists; round-26 `source-capture-pdf` → `capture-source.py`, round-26 manifest + `S041.txt` (147 KB) exist; round-31 `limb-mutation-ledger` → `ExecRegressionC1.md` quoted above. The pending round-33 `capture-binding-check` row's instrument runs green today (M5) and its receipt seats (ExecCaptureBinding/ExecRegressionC1) are in the spec.
- **Append-only protocol working as designed (not silent staleness)**: `corpus/QUALITY.md:77` (R13) still carries the stale `selftest cases=4` literal **by protocol**, with R19 (`QUALITY.md:103`) as the correction of record naming the literal and carrying the live measurement (18 case lines, exit 0, instrument `5d4842da…`) — the R19 form, satisfied.
- **Claims erratum consistency**: `claims-erratum-1.md` (Rule B per-record-id binding) is implemented by the checker — selftest cases `no-row`, `url-mismatch`, `shared-url-not-a-failure` all pass; informational `multi_row_url=2`; frozen predicate 40/40/0 unchanged.

## 4. Historical-by-design lines (separated, not counted as mismatches)

`corpus/README.md:217` "(11/11 admitted at round 26…)" + R9 amendment chain (:221 12/12, :288 14/14, :313 15/15); SKILL.md:1047 F13 note; SKILL.md:1069 "Measured at append time … `strict pass=44/44`, exit 0"; SCORECARD r15-era Axes table + every per-round "Last change" cell; SCORECARD:839 r31 erratum and :560-589 round-30-era numbers; PROVINCE r31 correction (`PROVINCE.md:67`). Each carries an in-place historical marker or an appended amendment; none is a live-claim line.

## 5. Instrument-output observation (informational, for RevC1Instrument)

`capture-binding-check.py` prints, between the contract's `MANIFEST <round> …` lines and the `records=… bound=… unbound=…` summary, one extra `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2` line (this carries the erratum's `multi_row_url=N` disclosure), plus `FAIL rule=…` lines naming record ids on failure. The interface contract names the MANIFEST and summary lines; the AUDIT/FAIL lines are additive and fail-direction-correct (exit 1 with `records=40 bound=38 unbound=2` when rule B failed at 04:27Z). Not a defect; reviewers should not read the extra line as a contract violation, and the summary-on-success matches the contract byte-shape (`records=40 bound=40 unbound=0`).

## 6. Residual risk and verification gaps

- Everything in §2/M5 was measured on **uncommitted working-tree bytes**; the L1's integration commit and the post-commit gate re-run can still change them. Re-run the §2 table's commands verbatim (they are the frozen counter set) on committed bytes before scoring.
- SHONEN.md and SCORECARD.md were still untouched at 04:30:09Z (ScribeShonen/ScribeScorecard poll on later receipts); M4's staleness is expected to close with their appends. If the final SCORECARD round-33 section does not also note the round-32 hole (M1), M1 stays open with no owner.
- I did not re-run `resolve.py` (scratch-tree run, ~minutes) — M2's 17.15% current figure is cited from the committed round-31 receipt, not re-measured here.
- M2/M3 are routed debt with no round-33 owner; if the L1 wants them closed this round they need an explicit seat, else they roll to round 34 with the drift in M3 growing by ~2 lines per admission round.

Report: .ufo/waves/round-33/wave1/RevCalibration.md
