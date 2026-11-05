# ScribeLesson — round-71 lesson draft

**Seat:** ScribeLesson (scribe, leaf member — no subagent dispatch).
**Product file written:** `corpus/lessons/round-71.md` — **199 lines** (cap: under 200). No other lane
file was written by this seat. No commit, push, or mutating git/jj command was run by this seat.

**Scratch:** `/fast/scratch/hyaku/kasegi-r71/ScribeLesson/` (clones `clone`, `clone-base`, `clone-tip`,
mutant trees `mut/`, `mut3/`, work dirs `work-*`), removed at the end of this seat.

## Sections written (in the order the item specifies)

| section | content |
|---|---|
| title | names C1 (per-script python-head census) and C2 (F49/S106, TrendAI ZDI disclosure process) |
| `## C1 - measured result` | the three control VERIFY lines with their committed receipt paths; the four VERIFY lines this seat re-ran; the direction-by-direction limb table; the one-limb mutation audit |
| `## C2 - measured result` | the counter table, before column from `controls/c2-base-counters-r71.txt`, after column re-measured at the landed tip; the 15 quote anchors with `wc -w` |
| `## Gate` | two-row table: S106 admitted (access date + 15-word located quote at `S106.txt:70`) and the explicit "no source was rejected this round" statement with its R102 arithmetic |
| `## Mistakes` | one mined mistake M71-1 (the global deny list applied where the flags are per-script), its captured-by criteria R103/R110 and the fix |
| `## Routed defects` | V71-1, V71-2, V71-3 |
| `## Residuals` | the named open classes, each with a measured gate probe |

## Numbers copied, with source paths

Every number in the lesson is either a number this seat measured or a number copied from a committed
receipt named here.

### Copied from committed receipts (path → value)

- `.ufo/waves/round-71/controls/c1-donothing-r71.txt` (sha256 `eb24dd87…`, pin line 3 of
  `controls/pins-r71.txt`) → `VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb… mode=donothing`;
  the N8/N9/N12 FAIL rows; the R1–R8 `admitted=0` rows; `selftest cases=96`; `no-write-side-effect FAIL
  marker_runs=1`.
- `.ufo/waves/round-71/controls/c1-base-r71.txt` (sha256 `f553ddb4…`) → `VERIFY measurements=25 failures=14
  gate_sha256=c09b0fb1… mode=base`; the twelve N rows with `refused=0`; the R1–R8 `admitted=1` rows;
  `selftest cases=86`; `no-write-side-effect FAIL marker_runs=5`.
- `.ufo/waves/round-71/controls/c1-candidate-trial-r71.txt` (landed at `4e33119`) → `VERIFY
  measurements=25 failures=0 gate_sha256=182f4ef7… mode=candidate`; the twelve N rows `ok`; the R1–R8
  rows `ok`; `selftest cases=106 failures=0`; `mutbat killed=5/5 survivors=0`; `real-ledger figures=35
  ok=35 stale=0`; `no-write-side-effect ok marker_runs=0`.
- `.ufo/waves/round-71/controls/c2-base-counters-r71.txt` (sha256 `4adae3b6…`) → the entire "before"
  column: `rows=48 admitted=48 registry=105`; `entries=51 pass=51 exit=0`; `records=84 bound=84
  unbound=0`; knowledge-expected 88 lines / 86 entries; `sort_exit=0`; 86 knowledge files; 48 frontier
  rows; 105 registry rows.
- `.ufo/waves/round-71/controls/pins-r71.txt` → its five pin lines (the counter `80020705…`, the base
  receipt `f553ddb4…`, the do-nothing receipt `eb24dd87…`, the C2 base counters `4adae3b6…`, and
  `claims.json` `c530ec65…`), all re-hashed against the committed blobs at `4e33119` and matching. Note
  the candidate trial receipt `c1-candidate-trial-r71.txt` is **not** in the pins file; its sha256 is
  `2231c8c814549ec9ffd4e0a6f35ffb3431f4079d79c6764134b21f12879de4dc`.
- `.ufo/waves/round-70/w1/CriticC1.md` (committed) → the round-70 over-refusal rows (ten paired rows,
  `--root` on six instruments, `--json` stdout-only at `claim-package-check.py:791`, the no-option
  `frontier-recheck-count.py` exec class), quoted in the Mistakes section.
- `corpus/lessons/round-70.md` (committed) → the r70 verdicts, the `measurements=12 failures=0`
  control-set artefact, the V70-5/V70-6 routing, and the `M1-out` equivalent-mutant finding.
- `corpus/source-snapshots/round-71/manifest.json` at `4e33119` → 15 quotes, their ids, anchors and
  quote text (sha256 `815566ac…`; not pinned in `pins-r71.txt`).
- `corpus/source-snapshots/round-71/S106.txt` at `4e33119` → sha256 `291f36c2…cf59db`, 148 lines,
  15004 bytes; the fetched date and HTTP status from the manifest (`2026-11-05T01:27:03Z`, 200).

### Measured by this seat (commands and observed output)

- Gate hash at the measured revision:
  `git show 4e33119:corpus/instruments/figure-audit.py | sha256sum` → `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603`.
- Control re-runs on `git clone --shared` of the lane at `4e33119`, counter
  `.ufo/waves/round-71/controls/c1-probe-run-r71.py`, `--work` under the seat scratch:
  `candidate exit=0 : VERIFY measurements=25 failures=0 gate_sha256=182f4ef7… mode=candidate`;
  `donothing exit=1 : … failures=13 gate_sha256=7a8d52eb… mode=donothing`;
  `base exit=1 : … failures=14 gate_sha256=c09b0fb1… mode=base`;
  `forgery exit=1 : … failures=12 gate_sha256=126de75d… mode=forgery` (the last against the committed
  round-70 forgery gate `.ufo/waves/round-70/controls/forgery-blanket-refusal-gate-r70.py`; its receipt
  shows `read-only-controls-admitted FAIL controls=8 failed=8` and `selftest FAIL selftest cases=86
  failures=47`).
- One-limb mutants of the committed gate bytes, each run with
  `python3 corpus/instruments/figure-audit.py --selftest` in its own tree: nine killed
  (`selftest cases=106 failures=1` each, named case in the lesson), one equivalent (`--out` removed →
  `cases=106 failures=0`), eight per-script entries with `cases=106 failures=0` while the gate's verdict
  changes from `rc=2 refused=1` to `rc=1 refused=0`.
- Two of those eight also pass the frozen counter: `VERIFY measurements=25 failures=0` on the
  `limb-mutation-check.py --root` mutant gate and on the `citation-ground-check.py --json` mutant gate.
- `PY_SCRIPT_CENSUS` = 44 names, `PY_SELFTEST_FIXTURE_HEADS` = 8, `EXPECTED_CASES` = 106,
  `corpus/instruments/*.py` = 44 files (read from the committed module).
- C2 after-values re-measured on clones of the tips `453275f` and `34faab9` (identical values at
  both): `FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106`; `entries=52 pass=52
  exit=0`; `records=85 bound=85 unbound=0` (capture exit 0); knowledge-expected 89 lines / 87 entries,
  `LC_ALL=C sort -c` exit 0; 87 knowledge files; 49 frontier rows; 106 registry rows;
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 with six inherited W04
  warnings.
- C2 before-values re-measured on a clone of `39cde8a`: `rows=48 admitted=48 registry=105`; `entries=51
  pass=51`; `records=84 bound=84 unbound=0` (capture exit 0); 88/86; 86 files; 48 frontier rows; 105
  registry rows.
- `capture-binding-check.py` at the capture commit `4e33119` alone: `FAIL rule=no-row record=S106
  dir=round-71`, `records=85 bound=84 unbound=1`, exit 1.
- The 15 manifest quotes: every quote is an exact substring of the line its anchor names; `wc -w` on each
  quoted text gives 7/13/19/5/15/15/25/19/12/19/19/16/19/18/13.
- The Gate quote: "Vendors are given a standard coordination window of 120 days under TrendAI™ ZDI's
  disclosure policy." at `S106.txt:70`, 15 words by `wc -w`.
- Residual probes against the candidate gate (all `rc=2 refused=1` unless stated): positional
  `claim-package-check.py <exemplar>` admitted (`rc=1 refused=0`); `resolve.py .` admitted (probe timed
  out at 90 s, no refusal); `--results`, `--manifest`, `--fleet-root` admitted; `ok.py -- --root` admitted;
  `capture-source.py -- --out x` admitted while `capture-source.py --out x --` refused;
  `corpus/instruments/../instruments/capture-binding-check.py` admitted; `python3 ../ok.py` and
  `python3 /tmp/x/ok.py` refused; `--url=file:///dev/null`, `'--url' file:///dev/null` and `-ox.txt`
  refused; `corpus/instruments/zzz.py` refused.

## Findings for the L1 (not applied by this seat)

1. **R110 is satisfied only by the round's own artifacts being committed.** `git -C
   /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain` printed one line,
   ` M corpus/SOURCES.md` (the round-71 `## Registry changes` bullet) at tip `453275f`; that bullet was
   committed at `34faab9`, and at that tip the only untracked entries are this seat's two output files.
   `bash corpus/instruments/r35-defect-closure.sh` printed no `filled by the L1` line. The lesson states
   this.
2. **The lane tip moved twice during this seat**: `4e33119` → `453275f` ("preserve in-flight work at hyaku
   run-15 wrap-up (L1 died on provider failure; not a landed round)") → `34faab9` ("late seat output
   (ScribeRegistry registry-changes bullet + report) after wrap-up; not a landed round"). The lesson's C2
   "after" column is measured at both later tips (identical values), and the C1 sections are measured at
   the frozen implementation commit `4e33119`. The L1 must re-measure the C1 candidate against whatever
   tip it lands.
3. **The committed candidate trial receipt `c1-candidate-trial-r71.txt` differs from a fresh re-run in
   two R rows** (`R1-capture-binding-root direct_rc=0 gate_rc=0` vs my re-run `direct_rc=1 gate_rc=1`, and
   the same for R8): the committed receipt was taken against a lane whose `capture-binding-check.py`
   exited 0, while at `4e33119` that instrument exits 1 (`FAIL rule=no-row record=S106 dir=round-71`)
   because the S106 registry row had not landed yet. Both runs are `ok` and both score
   `measurements=25 failures=0`; the difference is the instrument's exit status, not the gate's verdict.
4. **R103 gap (V71-1):** eight per-script denial entries are load-bearing but unpinned, two of them
   invisible to the frozen counter as well.
5. **V71-3:** the `frontier-recheck-count.py --json` entry is inert under `PY_HEAD_REFUSED`.
6. Tooling: no tool was installed or upgraded this round (nothing needed); the pacman guard was not
   invoked. Host tools used as-is: python3 3.14.8, GNU sort 9.12, git 2.56.0 (the `HOST` line of every
   counter receipt).

## Not done / out of scope

- No QUALITY.md criterion row was added for M71-1 (R36 wants one in the same round); the lesson names the
  criteria that carry the class (R103, R110). QUALITY.md is not a file this seat may write.
- No commit, push, tag or any other mutating git/jj command was run by this seat.
