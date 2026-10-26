# MutCtrNoLiveBaseline — counter mutant probe: never-run-live-baseline

Round 31 wave 2, seat MutCtrNoLiveBaseline. 2026-10-25.
Answering model: zai/glm-5.3-flash (config route; no model passed to any call).
Tooling: none installed, no pacman transaction (host-paused), python3 stdlib only.
Scratch lane: `/tmp/mutctr-nolivebaseline-r31.CPYaZ8` (made with `mktemp -d`; the lane tree was never written — see Lane integrity).

## Verdict

**SURVIVOR — a hole in the frozen counter-kill detector.**

The mutant counter's `--ledger` output is byte-identical to the real counter's and exits 0, so no
clause of the frozen C1 kill rule and none of the 3 controls catches it on the landed bytes. The
frozen design line — claims.json C1 key `mutants_of_the_counter`: "Attack seats must show each of
these counter mutants fails the 3 controls or the LIMB-line clause: … never-run-live-baseline …" —
is falsified for this mutant.

## The mutant

One behavior-bearing point: `evaluate_row` in a scratch copy of
`corpus/instruments/limb-mutation-check.py` no longer runs the unmutated instrument at all. It
trusts the declared `live_exit`, assumes the declared signal holds, and `invalid:live-baseline`
(the live-side guards, including live-side timeout/unstable) becomes unreachable. The killed test
is unchanged — the real counter already compares the mutant side against the declared
`row["live_exit"]`, so "compare mutant only to the declared live_exit" needs no second edit.

```diff
--- /tmp/mutctr-nolivebaseline-r31.CPYaZ8/counter-real.py   (byte-identical copy of corpus/instruments/limb-mutation-check.py, sha256 c660a95f…)
+++ /tmp/mutctr-nolivebaseline-r31.CPYaZ8/counter-mutant.py
@@ -416,14 +416,7 @@
             raise LedgerError("scratch copy is missing the instrument: %s" % rel)
         write_bytes(instrument_path, original)
         drop_bytecode_cache(instrument_path)
-        live = measure_runs(row, scratch, instrument_path, timeout)
-        live_exit = live["display"]
-        if live["token"] == "timeout":
-            return verdict_row(live_exit, "n", "-", "-", "invalid:timeout")
-        if live["token"] == "unstable":
-            return verdict_row(live_exit, yes_no(live["signal"]), "-", "-", "invalid:live-baseline")
-        if live["exit"] != row["live_exit"] or not live["signal"]:
-            return verdict_row(live_exit, yes_no(live["signal"]), "-", "-", "invalid:live-baseline")
+        live_exit = str(row["live_exit"])  # MUTANT never-run-live-baseline: trust the declaration
         text = original.decode("utf-8")
         if text.count(row["find"]) != 1:
             return verdict_row(live_exit, "y", "-", "-", "invalid:find-count")
```

Full diff on disk: `$SCR/mutant.diff`, sha256
`8294c81ce457be054503c3f900b6157cb84188d15826310479414d2a05d46e65`.

## Setup (commands + output)

```
$ mktemp -d /tmp/mutctr-nolivebaseline-r31.XXXXXX
/tmp/mutctr-nolivebaseline-r31.CPYaZ8
$ ls -d /tmp/limb-mutation-* 2>/dev/null | wc -l
3
```

```
$ cp -a $LANE/corpus $SCR/corpus \
  && find $SCR -name __pycache__ -type d -prune -exec rm -rf {} + \
  && cp $LANE/corpus/instruments/limb-ledger.json  $SCR/limb-ledger.json \
  && cp $LANE/corpus/instruments/limb-mutation-check.py $SCR/counter-real.py \
  && cp $LANE/corpus/instruments/limb-mutation-check.py $SCR/counter-mutant.py \
  && sha256sum <5 lane files + 6 scratch files>
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  $LANE/corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  $LANE/corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  $LANE/corpus/instruments/frontier-recheck-count.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  $LANE/corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  $LANE/corpus/instruments/limb-mutation-check.py
5d4842da… / fd2e01e8… / aa60b581… / c042adf6… / c660a95f…  (all six scratch copies: identical hashes, not repeated)
```

## Baseline: REAL counter run twice on the same scratch lane bytes

```
$ cd /tmp && time env PYTHONDONTWRITEBYTECODE=1 python3 $SCR/counter-real.py \
    --ledger $SCR/limb-ledger.json --root $SCR > $SCR/outA.txt 2> $SCR/errA.txt
real 0m20.800s   ; exit 0 (exA=0)  ; errA.txt = 0 bytes
$ … second identical invocation …
real 0m20.547s   ; exit 0 (exB=0)  ; errB.txt = 0 bytes
$ cmp $SCR/outA.txt $SCR/outB.txt && echo "realA==realB BYTE-IDENTICAL"
realA==realB BYTE-IDENTICAL
$ sha256sum $SCR/outA.txt $SCR/outB.txt
9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838  $SCR/outA.txt
9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838  $SCR/outB.txt
```

Baseline passes: exit 0, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3` (full text
below, shared with the mutant). Per the role rules this baseline success is what makes the
comparison below conclusive rather than inconclusive.

Lane crosscheck (canonical C1 counter command on the lane itself; the counter writes only its own
mkdtemp scratch, so this is read-only on the lane):

```
$ cd $LANE && env PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/limb-mutation-check.py \
    --ledger corpus/instruments/limb-ledger.json > $SCR/outLane.txt 2>&1
lane_exit=0
$ cmp $SCR/outA.txt $SCR/outLane.txt && echo "scratch==lane-root BYTE-IDENTICAL"
scratch==lane-root BYTE-IDENTICAL
```

The scratch corpus snapshot is therefore faithful to the landed bytes and the bytes were quiescent
across all runs (no PRE-STATE ambiguity).

## Mutant run (full output + exit code)

```
$ cd /tmp && time env PYTHONDONTWRITEBYTECODE=1 python3 $SCR/counter-mutant.py \
    --ledger $SCR/limb-ledger.json --root $SCR > $SCR/outM.txt 2> $SCR/errM.txt
real 0m9.780s    ; exit 0 (exM=0)  ; errM.txt = 0 bytes
```

stdout `$SCR/outM.txt` in full (sha256
`9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`):

```
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
```

The mutant only runs half the kill invocations (9.8s vs 20.8s wall) — unobservable in the printed
bytes. `grep -c '^LIMB '` = 13, `grep -c '^CONTROL '` = 3.

## Why SURVIVOR — frozen kill-rule clause by clause

Clauses quoted from claims.json C1 `kill_rule` (short fragments, exact location = that JSON key):

1. "counter is absent or exits non-zero" — mutant exits 0. Not caught.
2. output "lacks the exact lines" `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` — both printed verbatim. Not caught.
3. "fewer than 13 lines beginning `LIMB `" or any row "shows live-result == mutant-result" — 13 LIMB lines; every live column (`0/y` or `1/y`) equals the declared value, which on landed bytes equals the measured value; every mutant column differs from its live pair (FR-missing-entry differs by signal: `1/y` vs `1/n`). Not caught.
4. "find text does not occur exactly once" — the find-count gate still runs and every ledger find is exactly-once. Not caught.
5. "the real corpus regresses" — orthogonal: a counter mutant cannot move the corpus gates. Not caught.
6. closure "re-derives any one ledger patch by hand … differs" — the patches still behave exactly as the mutant counter reports. Not caught.

Controls: skipping the live run sits ABOVE the noop/compile gates and above the mutant-side run, so
`CTL-noop` → `invalid:noop`, `CTL-nocompile` → `invalid:nocompile`, `CTL-equivalent` → `survivor`
— all three still rejected. The mutation is observable only when some live baseline FAILS its
declaration (exit mismatch, signal miss, unstable, live timeout); the frozen target output itself
asserts every live baseline passes (`live=…/y` on all 16 rows), so on landed bytes the hole is
unobservable.

Supplementary evidence (NOT part of the frozen detector — the C1 `counter_commands` never pass
`--selftest`): the counter's internal selftest does flag the mutant:

```
$ python3 $SCR/counter-mutant.py --selftest; echo exit=$?
…
selftest invalid-live-baseline    verdict=killed                  want=invalid:live-baseline FAIL
selftest invalid-nondeterministic verdict=invalid:mutant-baseline want=invalid:live-baseline FAIL
selftest invalid-mutant-baseline  verdict=survivor                want=invalid:mutant-baseline FAIL
selftest cases=20 failures=3
exit=1
```

So the instrument's own fixtures know about live-baseline; the frozen ledger-run detector never
exercises that knowledge. Full selftest output: `$SCR/mutant-selftest.txt`.

## Smallest fix that kills this mutant (proposed; ExecCounterFix owns the file)

One whitelisted expect value + one ledger control row. Zero changes to verdict logic.

(a) `corpus/instruments/limb-mutation-check.py` line 88:
`CONTROL_EXPECTS = ("invalid:noop", "invalid:nocompile", "survivor", "invalid:live-baseline")`
(required — `validate_row` rejects any control `expect` outside this tuple, lines 139-141).
Optionally also bind `"CTL-livebaseline": "invalid:live-baseline"` in `CONTROL_ID_EXPECTS`
(lines 89-93) for id-swap symmetry.

(b) `corpus/instruments/limb-ledger.json`, append to `controls`:

```json
{
  "id": "CTL-livebaseline",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "def digest(data):",
  "replace": "def digest(data):",
  "kill": "python3 {inst} --selftest",
  "live_exit": 1,
  "signal": "(?m)^selftest parseonly\\.md .*\\bok$",
  "expect": "invalid:live-baseline",
  "note": "control, bound to the RA-parse limb's instrument/kill/signal with a deliberately WRONG declared live_exit: the unmutated selftest exits 0, so the honest counter must stop at invalid:live-baseline before compiling or running any mutant; a counter that never runs the live baseline trusts the declaration, falls through to invalid:noop, prints rejected=3 of 4 and exits 1."
}
```

Expected behavior split (derived from the code paths above, both sides verified structurally):

- REAL counter: live run exits 0 ≠ declared 1 → `CONTROL CTL-livebaseline verdict=invalid:live-baseline expected=invalid:live-baseline ok=y` → summary `controls=4 rejected=4`, exit 0.
- THIS mutant: skips the live run → find-count ok (`def digest(data):` occurs exactly once — same anchor as CTL-noop) → mutated == original → `verdict=invalid:noop … ok=n` → `controls=4 rejected=3`, exit 1 → caught by the controls clause AND the exit-nonzero clause.
- Side benefit: an always-killed counter (skip the mutant run, report killed) also reports this row `killed ≠ expect` and is caught by the same row.

Claims-freeze note (L1 decision — I have no write access to either file): adopting the row moves
the frozen target line `controls=3 rejected=3` to `controls=4 rejected=4` in the C1
`predicate_sentence`; frozen claims are append-only, so this needs an erratum/re-freeze alongside
the fix. If ExecCounterFix lands the fix, the counter runs on the new ledger must be re-quoted on
quiescent bytes (bound 6).

## Lane integrity / restoration evidence

- The lane tree was never written by this seat; every byte changed lives under
  `/tmp/mutctr-nolivebaseline-r31.CPYaZ8`. Nothing to restore.
- sha256 of the five lane files AFTER all runs — identical to the before column:
  `5d4842da…` recheck-audit.py, `fd2e01e8…` source-recheck.py, `aa60b581…` frontier-recheck-count.py,
  `c042adf6…` limb-ledger.json, `c660a95f…` limb-mutation-check.py.
- `git -C $LANE status --porcelain -- corpus/instruments` → empty, exit 0.
- Scratch hygiene: the counter mkdtemp's and finally-rmtree's every scratch; my three counter runs
  all exited 0, so their cleanup paths ran. Residual `/tmp/limb-mutation-*` dirs at check time: 2
  (mtimes 2026-10-25T21:29:34 and 21:31:06) — both created after my run batch had completed;
  concurrent seats are running the same counter, so these are consistent with peers' in-flight
  runs and none is attributable to a completed run of mine.

## Bounds

- No git/jj mutations in the lane (read-only `git status` only, scoped to corpus/instruments).
- No pacman, no tool installs, no network fetches, no live bounty target contacted.
- Quote discipline: quoted fragments ≤ 25 words with exact location (JSON key path or file:line); numbers copied from recorded outputs above, none from memory.
- Wave-2 bounds respected: single-writer receipt only; instruments/ledger/entries untouched (defect reported to ExecCounterFix instead).

## Addendum — disposition (2026-10-25, post-probe coordination)

ExecCounterFix (owner of limb-mutation-check.py, fixes only) confirmed the survivor from this
receipt and declined the proposed 4th control row: the frozen C1 line must stay
`controls=3 rejected=3`, so a 4th row is out of their scope. Their alternative, quoted from their
message (IRC, ExecCounterFix r31w2): the three guard fixtures "run inside run_ledger() on every
`--ledger` invocation" on "a throwaway probe lane with a 1 s cap", folding "into the exit status".
Their replay of an equivalent mutant against the patched counter prints the guard line
`guard invalid-live-baseline verdict=killed want=invalid:live-baseline FAIL` with
`guard cases=3 failures=1`, exit 1, while the LIMB lines and both frozen summary lines still print
unchanged — i.e. the mutant is caught by the kill rule's exit-nonzero clause without moving the
frozen target lines. Pristine patched counter: `guard cases=3 failures=0`, target lines intact,
`--selftest cases=20 failures=0`.

Byte attribution per their heads-up: at the time of this addendum the lane counter is STILL
sha256 `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` (re-checked; scoped
`git status --porcelain -- corpus/instruments` clean) — their guard fix has not landed on lane
bytes yet, so the subject of every run recorded above remains the current lane subject. Their
replay evidence is from their own scratch; main-agent verification should re-run both the frozen
counter command and a replay of this seat's exact mutant
(`/tmp/mutctr-nolivebaseline-r31.CPYaZ8/counter-mutant.py`, diff in `mutant.diff` there) against
the patched bytes once they land. This seat's verdict is unchanged and scoped: **SURVIVOR against
bytes c660a95f…** under the frozen detector as it stood at probe time.
