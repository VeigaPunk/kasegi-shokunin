# ScribeConsiderthese — round 29, wave 1 (proposal mine)

- Seat: `ScribeConsiderthese` (scribe; leaf — no subagent dispatch).
- Lane: `kasegi-shokunin`; round 29, wave 1 (build+attack, single v2 wave, 64 seats).
- Date: 2026-10-25. Lane base `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims-freeze commit `f28ff5d26b29270f93163117e7255e24f0b1d947`.
- Answering model: route-table-selected from environment (inception/mercury-3); the seat does not pass a model (bound 8).
- Scope: mine `considerthese/2026-10-25.md`; choose exactly one still-unimplemented proposal (**proposal 5**: open-defects ledger with runnable closure checks); ground it in the round's routed defects M28-1/3/5/6/8/12 and the open-debt list; propose QUALITY.md criterion **R15**; record a proposals-status ledger; hand R15 to ScribeQuality.

## 1. Proposals-status ledger (considerthese/2026-10-25.md proposals 1–6)

| # | Proposal (verbatim summary) | Status | Where / evidence |
|---|---|---|---|
| 1 | Cap wave-evidence bloat (receipts/digests in git; tarball or regenerate) | **MINED** | Landed as `corpus/QUALITY.md` **R14** (Round-28 additions), round 28; grounded in `considerthese/2026-10-25.md` proposal 1; practice exercised in-round (`.ufo/waves/round-28/c1-controls/` at 44 KiB) — `corpus/lessons/round-28.md:219-228` |
| 2 | Track "distance to the next score", not just "improved, held" | **OPEN** | No lesson/scorecard reference found (grep `distance to the next score|distance` over lessons, SCORECARD.md, round-29 wave dir → 0). Verifiability still held 4 with 23/37-type gated rechecks |
| 3 | Point a round at bounty craft + SHONEN box 2; F11 on platform severity tables | **PARTIALLY LANDED** | Severity-tables plank substantively covered by round-29 **C2** F13 admission (S043 HackerOne standard program policy set, S044 Bugcrowd VRT README, S045 Bugcrowd CWE crosswalk) — though `claims.json` C2 cites the merge/kasegi/ theme, not the proposal. SHONEN box 2 end-to-end hunt-to-claim pipeline + rebuilt minimal `claim-check` gate remain OPEN |
| 4 | Give my own proposals a status ledger | **BEING MINED (this report)** | First ledger note is this seat's §1; the permanent home (a table at the top of each `considerthese/` file) is still OPEN/not implemented |
| 5 | Keep an open-defects ledger with runnable closure checks | **MINED HERE** | This seat grounds it (§2) and proposes criterion text **R15** (§3); text handed to ScribeQuality |
| 6 | Event-driven reflections (push listener on `master`; weekly idle note) | **OPEN** | No reference found in lessons/scorecard/round-29 wave dir |

Prior-window proposals (2026-10-24.md): proposal 1 mined as Q9 (round 24), proposal 2 mined round 25 (`round-25.md:213-217`) — both recorded in lessons.

## 2. Grounded reflection — proposal 5, opened against the tree

Proposal 5 wants: a ledger of routed+open defects where each entry carries a **runnable closure check**, run daily read-only, with flips reported. Grounding = opening what it points at: the round-29-routed defects (round-28 verifier spotcheck §Routed defects) and the open-debt list (round-28 lesson close-out ledger + carry-forward; SCORECARD.md carried debt). Measured tree state at 2026-10-25 (read-only):

### 2a. Routed defects M28-1/3/5/6/8/12 — current state

| Defect | What it is | State verified in the current tree |
|---|---|---|
| M28-1 | Seven PRE-STATE receipts ran before their subject landed; "label PRE-STATE, name the re-run, never compare to an after column" | **OPEN as standing process rule**, mitigated by construction in r29: round-29 C1/C2 counter commands run on committed bytes and instrument selftests (`anchorcheck.py --selftest`; greps over committed files), so no counter depends on a seat's landing order. Mid-wave verification not possible (wave landing); carry-forward 1 stands |
| M28-3 | Frozen counter command (d)'s `bad=` sed limb cannot emit: `sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'` vs summary grammar `… N bad; …` → prints nothing | **Avoided in r29, historical defect recorded**: round-29 C1 counter_commands use `grep -E 'selftest cases=|limbs='`; the dead limb is not carried forward. Round-28's frozen command remains honestly reported (round-28 lesson M28-3, close-out addendum) without an erratum for the counter itself |
| M28-5 | `frontier-recheck-count.py` crashes on an absent entry (uncaught `FileNotFoundError`) instead of failing a named row | **VERIFIED STILL OPEN**: `entry_contract()` does an unbounded `open(full)` (`frontier-recheck-count.py:65`); an admitted frontier row whose entry file is absent still raises rather than printing `pass=14 of 15` |
| M28-6 | R6 table-row carve-out undecided; `resolve-dispatch-fixtures.json:159,161` stale pointer to `SKILL.md:1000` | **VERIFIED STALE POINTER**: `SKILL.md` is 1035 lines; the four-alternative brace set now sits at line **1008** (`SKILL.md:1008`), while the fixture still pins "SKILL.md:1000 verbatim alternative set" — line 1000 currently holds `~/Projects/bounties/evidence/<program>/` (per-program audit store). Carve-out decision still open |
| M28-8 | Q9's stem==id conjunct has no instrument behind it; C2's Q9 clause rests on hand-run receipts | **VERIFIED STILL OPEN**: no `corpus/instruments/check_q9.py` exists; `source-recheck.py` never compares path stem to record id; `frontier-recheck-count.py`'s `PASS` row doesn't test it either |
| M28-12 | Receipt digests/labels drifted behind the bytes they describe (ScribeReadmeC2 243 vs landed 245 lines) | **Partially mended by process**: round-28 `c1-receipt-index.txt` exists and pins the landed instrument digest `23818c1204…` (file present, digest matches the verifier's recomputed hash); the "re-hash production files immediately before commit" rule is stated in carry-forward 7-adjacent text but nothing enforces it — process open |

### 2b. Open-debt list (named debt with unblock)

Round-28 carry-forward (round-28.md:567-588) + SCORECARD.md carried debt:

1. Dispatch counters after their subject lands / hand them the landed digest (M28-1) — open rule; r29 design complies.
2. Frozen disclosure names the lexical form the matcher reads, fixture runs before freeze (M28-2/M28-14) — addressed in r28 via appended erratum 1 (measured 0/4 reclassification); stands as a house rule.
3. Every frozen counter executes once against frozen before bytes before `claims.json` commits (M28-3) — open rule; M28-3 is the case.
4. Decide R6 for table rows (carve-out or end-of-file table) (M28-6) — open; the round ships a disclosed +1/+8 shift and the stale `SKILL.md:1000` fixture pointer.
5. Promote Q9's stem check into an instrument and register `check_q9.py` beside `source-recheck.py` (M28-8) — open; no such instrument exists.
6. Fix `frontier-recheck-count.py`'s crash on an absent entry (M28-5) and re-point `resolve-dispatch-fixtures.json` at the current SKILL.md line — open.
7. Re-base the same-byte density guard at each round's base (M28-9) — done for r28 (150.3/20/652 base vs 160.2 after append, disclosed); standing rule.
8. Carried debt, unchanged: 23 of 40 recheck lines stay gated on lost bases (2026-09-28 / 2026-10-12 losses); `anchorcheck.py` fail-closed makes five corpus files exit 1 by design — standing, disclosed; unblock = operator restoration.
9. SCORECARD.md carried debt: `RECEIPT-STORE-LOST`, `MIRROR-SOURCE-LOST`, `ORIGIN-REPO-LOST` — standing, operator-owned.

Proposal-5-era debt (from the proposal's own list), cross-checked today:
- D24-4 (L4 label) — closed (corrected in round-25 lesson M25-3).
- D24-5 (recheck form: cwd prefix/parse) — closed (Q10 + R13).
- R25-1 (`claims.json` edited after freeze) — closed by freeze discipline (round-28 compliance: committed before dispatch, never in-place, erratum appended).
- R25-2 (selftest tally missing from receipts) — closed (anchorcheck `--selftest` tally now required and receipted; C1/round-29 counts it).
- R25-3 (`recheck-audit.py` not registered in SKILL) — closed (`grep -c recheck-audit SKILL.md` → 1).
- R25-4 (fix-control wording) — closed per round-26 scorecard C1 row.
- R25-5 (S040 URL 301s/403s a browser UA) — documented in SOURCES.md recheck-cell notes (cadence-only cell restored); recorded, not code-fixed.
- Carried: entry deletion shrinks audited set while passing — **closed** (`recheck-audit.py` exits 1 naming the missing entry; round-26 scorecard row).
- Carried: `source-recheck.py --source` single-valued — **still open** (M28-11); workaround is chained invocations; the round-28 SCORECARD cell wording still cites the two-flag form.

### 2c. Why the criterion is needed

The individual debts are real and individually recorded, but they are scattered across lessons, scorecard rows, and carry-forward lists; none carries a single runnable closure command that a reader can re-run, and several (M28-5, M28-6, M28-8, M28-12) are verifiably still open in the current tree because nothing re-checks them daily. Proposal 5 is the least-implemented and highest-leverage item: a ledger whose rows each name a closure command (exit-code verdict) would have caught M28-3 before freeze, M28-5's crash the day it landed, M28-6's stale pointer when SKILL.md moved, and M28-12's drift at commit time. It is a record criterion (R-space), not an entry criterion (Q-space), so it belongs in QUALITY.md's Record section as **R15**.

## 3. Proposed QUALITY.md criterion text — R15

Add a new section after the Round-28 additions (appended at file end, per R6 — never inserted mid-file), carrying the row:

> ## Round-29 additions — open-defects ledger
>
> | id | criterion | grounded in |
> |---|---|---|
> | R15 | Every open or routed defect is carried in a ledger entry that states its exact closure command (an exit-code verdict a reader can re-run) or a dated disposition (fixed in \<round\>, declined, superseded); the ledger is re-run read-only, with flips reported. A defect whose closure command cannot emit its value (a frozen counter that parses nothing) or whose named instrument is absent stays OPEN — never silently dropped. | considerthese/2026-10-25.md proposal 5 (2026-10-25); round-28 routed defects `corpus/lessons/round-28.md` M28-1/3/5/6/8/12 and `round-28-verifier-spotcheck.md` §Routed defects — M28-3's frozen `bad=` sed limb printed nothing for a whole round, M28-5's harness crashes on an absent entry instead of naming the row, M28-8 has no instrument behind Q9's stem conjunct, M28-6 ships a stale `SKILL.md:1000` fixture pointer, M28-12 receipts drifted behind the bytes. |

Handoff: the full R15 text (section heading + row) is delivered to `ScribeQuality` for integration into `corpus/QUALITY.md` (their write scope; appended at end per R6).

## 4. Notes

- Read-only grounding; no lane file modified by this seat; no git state touched.
- No tool installed; no pacman transaction (bound 5). Answering model recorded above (bound 8).
- ScribeLesson-2 will be pinged once this file is written (requested).
