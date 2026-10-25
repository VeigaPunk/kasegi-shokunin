# ScribeCloseOut — kasegi round 30, wave 1 (hyaku run 7 inline spawn)

Lane: `kasegi-shokunin`. Seat: ScribeCloseOut (UFO-FSD scribe, leaf).
Measured on 2026-10-25 at the lane working tree; C2 subject landed during this seat's session
(entry + round-30 manifest present at final measurement). All runs below are the exact frozen
counter commands from `claims.json` (sha256 `68d77757c71f1779be89ac97efe3f1299a5858187c7f95e06d9da4e52cae523b`, frozen).

## 1. Bytes measured (sha256, worktree at measurement)

| path | sha256 |
|---|---|
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` |
| `corpus/instruments/source-recheck.py` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` |
| `corpus/source-snapshots/round-30/manifest.json` | `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6` |
| `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (F14 entry) | `f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32` |
| `corpus/source-snapshots/round-30/S046.txt` | `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3` |
| `corpus/source-snapshots/round-30/S047.txt` | `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4` |
| `corpus/source-snapshots/round-30/S041.txt` | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` (byte-identical to the round-28 capture; no new S041 fetch needed) |

Baseline instrument digests at the freeze commit match the committed before receipt
(`c1-controls/before.txt`): frontier-recheck-count.py `c8a62888…`, source-recheck.py `9fe6a4a0…`.
Freeze copies preserved at `c1-controls/mutants/freeze-*.py` (byte-identical to baseline); the
do-nothing control runs recorded there reproduce `before.txt` exactly.

## 2. Behavior — C1 counter runs (four fixtures, current bytes)

| fixture | output (verbatim) | exit | predicate verdict |
|---|---|---|---|
| A1 | `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry` / `entries=1 pass=0 exit=1` | 1 | OK — names row F98, no traceback |
| A2 | `PASS F98 … exit=0` + `PASS F97 … exit=0` + `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md` / `entries=2 pass=2 exit=1` | 1 | OK — names the duplicate |
| B1 | `S043:manifest MISMATCH reason=stem-mismatch` | 1 | OK — `reason=stem-mismatch` |
| B2 | `S045:manifest MISMATCH reason=stem-mismatch` | 1 | Kill-rule letter OK (exit 1 + a failure reason); see Finding 1 |

`source-recheck.py --selftest`: 9/9 PASS, exit 0 (limbs exercised: clean, corrupt,
missing-source, missing-manifest, stem-mismatch, double-occurrence unanchored/anchored/
out-of-range/broken). Real-corpus regression clause: harness on the lane (below) passes every
admitted row incl. F14; per-id round-30 rechecks all pass.

## 3. Behavior — C2 counter runs (seven counters, current bytes)

| # | counter | measured | required | |
|---|---|---|---|---|
| 1 | frontier admitted (`awk … corpus/README.md`) | **14** | 14 | F14 row present |
| 2 | entries citing `^source: S04[6-7] ` | **1** | 1 | the F14 entry |
| 3 | registry rows `S04[6-7]` | **2** | 2 | S046 + S047 |
| — | registry rows total (`S[0-9]{3,}`) | **47** | 47 | |
| 4 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit **0**, W04 S028/S029 only | 0 | E11 cleared after entry landed |
| 5 | `frontier-recheck-count.py` (real corpus) | `entries=17 pass=17 exit=0`, `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0` | 17/17/0 | |
| 6 | per-id `source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json` | S046 exit 0 (Q1–Q4 occurrences=1); S047 exit 0 (Q1–Q5, Q1 occurrences=3 anchor=123-ok, Q3 occurrences=2 anchor=130-ok); S041 exit 0 (Q1–Q3 occurrences=1) | all 0, exactly-once/anchored, stems==ids | |

All stems == ids (S046.txt/S047.txt/S041.txt). Kill rules for C1 and C2 are satisfied at the
measured working-tree bytes. C2 staged row adoption followed the claims map (S049→S046,
S050→S047; staged S043 → lane S041); registry changes appended per R8.

## 4. Gates

- S090 (0/18 lost-domain) unchanged; frontier is a separate denominator; F14 row recorded as an
  appended amendment, no map line renumbered (R6).
- QUALITY Q1–Q10 / R1–R15: F14 entry carries `source:`/`verified-at:`/`recheck:` header; manifest
  assertions exactly-once or anchor-verified (Q9). Q8 normalization declared (`normalized=markup-whitespace`).
- No gate relaxed; no refused package re-admitted; quarantine slice (7 rows) untouched by this seat.

## 5. Touched surfaces (production files measured; this seat wrote none of them)

`corpus/instruments/frontier-recheck-count.py`, `corpus/instruments/source-recheck.py`,
`corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`,
`corpus/source-snapshots/round-30/{manifest.json,S046.txt,S047.txt,S041.txt}`,
`corpus/README.md` (F14 row), `corpus/SOURCES.md` (S046/S047 rows + R8 change cells).
Wave reports/drafts also on disk: `wave1/{ScoutDatawalk,ScoutAssimPackage,ScoutQuarantineSlice,
ScoutInstrumentBaseline,ScoutMapExpected,ScoutAdjacency,ExecReadmeF14}.md`,
`wave1/ExecImplSourceRecheck.pre.py` (pre-edit snapshot of source-recheck.py),
`c1-controls/{before.txt,before-run-2.txt,a1.out,a1.err}`, `c1-controls/mutants/` (freeze copies
+ control runs), `assimilation/quarantine-slice`, `c2-controls/before.txt`, `census-before.txt`.

## 6. Findings

1. **B2 fixture does not isolate the occurrence limb (R13).** The committed fixture
   `manifest-b2.json` uses path `B2.txt` (stem `B2` ≠ id `S045`), so the new instrument reports
   `reason=stem-mismatch` before the occurrence check runs. The kill-rule letter is satisfied
   (exit 1 + failure reason), but the predicate's named reason `occurrence-not-unique` is not the
   exercised limb. An isolated probe with a stem-matching capture containing the quote twice prints
   exactly `S045:Q1 MISMATCH reason=occurrence-not-unique`, exit 1 — the limb is implemented and
   works; only the committed fixture fails to exercise it in isolation. Suggest appending a
   stem-matching double-occurrence fixture (or an R9 note in the lesson).
2. **Instrument bytes moved mid-wave.** `digest-poll.log` records the baseline digests at
   18:50:10Z and new digests at 18:50:40Z; `source-recheck.py` changed again between this seat's
   first run (`0b841d5d…`) and the final measurement (`33602a9d…`). Final bytes are settled above;
   the post-commit recheck must pin these digests (see ledger).
3. **C2 subject landed during the wave** (entry and manifest timestamps 15:52, after several seat
   measurements); all measurements in this report are post-landing and labelled with the bytes in
   §1. This is the M29-1 sequencing hazard class again; the dispatch-side fix (gate canon/review
   seats on subject receipts) remains a standing item.
4. Do-nothing control reproduced: freeze copies digest-match baseline and their runs match
   `before.txt` line-for-line (A1 traceback, A2 pass=2 exit 0, B1 OK, B2 OK anchor=MISSING).

## 7. Close-out ledger — what the L1 / main agent still owes after the wave (each item carries its closing command)

1. **Post-commit recheck at the final commit** (`ExecPostCommitRecheck`): re-run the four C1
   counters and the seven C2 counters at the integration commit; `git show <commit>:corpus/instruments/frontier-recheck-count.py | sha256sum`
   must equal `aa60b581…` and `git show <commit>:corpus/instruments/source-recheck.py | sha256sum`
   must equal `33602a9d…`; write `wave1/post-commit-recheck.txt`. **Command:** the four+counter
   runs of §2/§3 at `git rev-parse master`.
2. **Misroot sweep** (`ExecScopeSweep`, final post-integration): confirm no write outside the lane
   (fleet root, sibling lanes, `/home/vgpnk/Projects/shokuknow`, lane git/jj state,
   `.ufo/state`, `MANIFEST.json`) and refresh the wave1 receipt index. **Command:**
   `git status --porcelain` shows only lane-owned files; sweep for `/home/vgpnk/Projects/shokunin/*`
   strays.
3. **Report landing via fleet-commit** (hyaku driver/L1): commit `.ufo/reports/round-30/kasegi.md`
   in the fleet repo by the lane identity (outside this lane's write scope).
4. **Proof of census exit 0 at round end:**
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
   → exit 0 at the final commit (measured 0 at worktree).
5. **Final harness re-run:**
   `python3 corpus/instruments/frontier-recheck-count.py` → `entries=17 pass=17 exit=0` at the
   final commit (measured 0 at worktree).
6. **Mutant evidence receipts** for the four isolating C1 mutants (each dropping exactly one new
   limb) land from `ExecMutantsC1` in `wave1/`; the freeze-control runs are already on disk in
   `c1-controls/mutants/control-*`.
7. **Optional:** B2 fixture isolation correction (Finding 1) — append a stem-matching
   double-occurrence fixture or record the R13 caveat in the round-30 lesson.

## 8. Scope / out-of-scope

No write outside the lane working tree (this report is the only artifact this seat wrote). No
`git`/`jj` mutation; no `pacman` transaction; no tool installed/upgraded (none needed). No live
network contact, no bounty target probed; corpus entries remain documentation-only (Q6). No
subagent dispatch (leaf). Answering model: `inception/mercury-3` (operator route; no model passed).
