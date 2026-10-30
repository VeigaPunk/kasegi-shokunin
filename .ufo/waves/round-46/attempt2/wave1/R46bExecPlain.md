VERDICT: DRAFT-READY

# Seat R46bExecPlain — round 46 (attempt 2), kasegi lane

Scope of this seat: ONE item — build the plain measurement script
`.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/plain-measure2.sh <tree>` and run it on a
base export AND on the live lane, reporting both. No corpus byte was touched. The only bytes this
seat wrote are (a) the draft script in its own draft directory, (b) the run logs under
`.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/`, and (c) this report.

Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Base rev (frozen): `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; freeze rev `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`
Live lane HEAD at measurement time: `ee03806b6b54a2822045e96641a77fa76984b410` (the wave's work sits UNCOMMITTED on top of it)
Scratch used: `/fast/scratch/hyaku/kasegi-r46/R46bExecPlain*` — removed before yield (TMPDIR was
exported explicitly in every run; nothing was written under /tmp).
Tools: python3 3.14.8, git 2.56.0, GNU bash 5.3.20 — **no tool was installed, upgraded or removed**
(nothing was missing; the pacman pause was never engaged).

---

## F1 — BUILT: the measurement script (the seat's deliverable)

`​.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/plain-measure2.sh` — one invocation, nine
`key=value` lines, one per spec'd measurement, tree read-only.

```
$ bash -n .../R46bExecPlain.draft/plain-measure2.sh && echo "syntax OK"
syntax OK
```

Its nine lines: `a_frontier_rows` (`grep -cE '^\| F[0-9]+ \|' <tree>/corpus/README.md`),
`b_frontier_counter` (`r44-frontier-count.py --root <scratch COPY of tree> --expect 29`),
`c_sources_rows` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <tree>/corpus/SOURCES.md`),
`d_knowledge_files` (`find <tree>/corpus/knowledge -maxdepth 1 -name '*.md' | wc -l`),
`e_absence_sweep_files` (`grep -rliE 'repository securit. advisor|GHSA' <tree>/corpus/knowledge
<tree>/corpus/SOURCES.md <tree>/corpus/README.md | wc -l`), `f_selftest_c1`/`f_selftest_c2`
(`r46-counters-selftest-c{1,2}.py … | tail -1`), `g_battery_c1`/`g_battery_c2`
(`r46-mutbat.py --root <tree> --pure PURE --work W --counter <c> --jobs 8`, summary lines only).

Three deliberate, header-documented deviations from the card's prose:
1. (b) runs against a **scratch COPY** of the tree (the card asks for this); the copy excludes
   `.git`/`.ufo` (no corpus byte lives in either) and is removed on exit — the counter provably
   cannot mutate the tree.
2. both selftests are bound to the tree under test with `--lane <tree>`: the counter a selftest
   grades is the one in `--lane`; without it the "base export" row would have graded the LIVE
   LANE's counter and would not have been about the base export.
3. the c2 selftest accepts **neither `--work` nor `--jobs`** (F6), so the script tries the card's
   twin form, falls back to the form the tool's own usage documents, and prints which form ran.
   The battery is run as two parallel mutbat invocations (one per counter) — summary lines are
   byte-identical per counter, wall time is the slower counter instead of the sum.

---

## F2 — BASE EXPORT RUN: every before-value reproduced, including the battery

Base export (read-only `git archive` of the frozen base, never a checkout):

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d | tar -x -C /fast/scratch/hyaku/kasegi-r46/R46bExecPlain-export/base
```

Delivered script on that export (run 18:36→20:46, 7774 s wall; all times local −03:00):

```
BASE exit=0
a_frontier_rows=28
b_frontier_counter=frontier rows/admitted=[frontier rows=28 admitted=28;frontier expected=29 admitted=28 verdict=SHORT exit=1] exit=1
c_sources_rows=73
d_knowledge_files=65
e_absence_sweep_files=2
f_selftest_c1=selftest cases=76 failures=0 (rc=0)
f_selftest_c2=selftest cases=137 failures=0 (rc=0; form: --pure only (--work/--jobs rejected by argparse: r46-counters-selftest-c2.py: error: unrecognized arguments: --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/base/w/c2 --jobs 8))
g_battery_c1=mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
g_battery_c2=mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

This is the do-nothing control the C1 kill rule asks for ("the before-value must stay reproducible
at the base export"), and it holds at the battery level too: the two `g_battery_*` lines are
byte-identical to the committed receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`
(sha256 `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`, the digest the frozen
claim records):

```
$ grep '^mutbat counter=' .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

Manual cross-check of the same five census measures on that export (same numbers, independent
commands):

```
$ echo "a: $(grep -cE '^\| F[0-9]+ \|' "$T/corpus/README.md")"
a: 28
$ echo "c: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$T/corpus/SOURCES.md")"
c: 73
$ echo "d: $(find "$T/corpus/knowledge" -maxdepth 1 -name '*.md' | wc -l)"
d: 65
$ echo "e: $(grep -rliE 'repository securit. advisor|GHSA' "$T/corpus/knowledge" "$T/corpus/SOURCES.md" "$T/corpus/README.md" | wc -l)"
e: 2
$ grep -rliE 'repository securit. advisor|GHSA' "$T/corpus/knowledge" "$T/corpus/SOURCES.md" "$T/corpus/README.md"
/fast/scratch/hyaku/kasegi-r46/R46bExecPlain/base/corpus/knowledge/github-private-vulnerability-reporting.md
/fast/scratch/hyaku/kasegi-r46/R46bExecPlain/base/corpus/SOURCES.md
$ python3 .../corpus/instruments/r44-frontier-count.py --root <scratch copy> --expect 29; echo "exit=$?"
frontier rows=28 admitted=28
frontier expected=29 admitted=28 verdict=SHORT exit=1
exit=1
```

The c1 selftest bound to the base export (earlier manual run, 328.87 s): last lines
`residual-false-greens=1 (disclosed mechanical limits, not counted as failures:
R-claim-text-unrelated-to-anchor)` then `selftest cases=76 failures=0`, exit 0.

---

## F3 — LIVE LANE RUN: before-values on the census, and a c1 battery already moved by the wave

Delivered script on the live lane (run 18:33→20:47, 7887 s wall; instrument digests captured at
18:35:57, before the run — `logs/live-instrument-sha-before.txt`, all four = the base digests — and
again at 20:48:45, after it — `logs/live-instrument-sha-after.txt`, where the two selftests and the
c2 counter differ):

```
LIVE exit=0
a_frontier_rows=28
b_frontier_counter=frontier rows/admitted=[frontier rows=28 admitted=28;frontier expected=29 admitted=28 verdict=SHORT exit=1] exit=1
c_sources_rows=73
d_knowledge_files=65
e_absence_sweep_files=2
f_selftest_c1=selftest cases=76 failures=0 (rc=0)
f_selftest_c2=selftest cases=137 failures=0 (rc=0; form: --pure only (--work/--jobs rejected by argparse: r46-counters-selftest-c2.py: error: unrecognized arguments: --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/live/w/c2 --jobs 8))
g_battery_c1=mutbat counter=c1 mutants=20 caught=17 equivalent=0 uncaught=3 baseline_failures=0
g_battery_c2=mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

Reading of that run, with the drift made explicit:

* The five census lines (a–e) read the lane as it stood at ≈18:33 — the **before-values**, because
  the wave's C2 landing had not reached `corpus/` yet.
* The battery (g) graded the tree's selftest+counter COPIES taken per mutant, i.e. the lane as it
  evolved during ≈18:40–20:46. The c1 half read `caught=17 uncaught=3` against the base's
  `13/7`; the log (`logs/live/bat-c1.log`) shows exactly which four flipped from uncaught to
  caught — `M13-L6-control-dropped` (0→2), `M18-anchor-dirs-wide` (0→1), `M19-L2-eq-relaxed`
  (0→1), `M20-syntax-ignored` (0→1) — while `M06-L3-home-dropped`, `M07-L3-home-no-abs`,
  `M14-L6-exit-ignored` stayed uncaught. The four flips coincide with the c1 selftest being
  rewritten under the run (sha256 `8b17164a…` before → `03079421…` after, +123 lines; the file's
  last write, 20:28, fell inside the battery window): **the wave's C1 work was landing while the
  battery ran, and the run recorded it mid-flight.**
* The c2 half still read `caught=8 uncaught=13` — see F8 for why that number is only conditionally
  trustworthy.
* After the run (20:49), the live census reads the **C2 after-values**:
  `rows=29 sources=74 knowledge=66 absence=4` (commands as in F2, run against the lane worktree).

**A single live-lane run is therefore time-mixed by construction while the wave is in flight; the
L1's final measure should be taken on an exported revision (as `controls/final-measure.sh` does),
not on the moving worktree.**

---

## F4 — CONTROL: the script is not tautological (junk F29 tree)

A junk control tree was built in scratch only (never in the corpus): a copy of the base export
plus one synthetic `| F29 | … | admitted | … |` frontier row, one synthetic `S074` registry row and
one synthetic `knowledge/github-repository-security-advisories.md`, nothing else. The delivered
script on that tree printed:

```
JUNK exit=0
a_frontier_rows=29
b_frontier_counter=frontier rows/admitted=[frontier rows=29 admitted=29] exit=0
c_sources_rows=74
d_knowledge_files=66
e_absence_sweep_files=4
f_selftest_c1=selftest cases=76 failures=0 (rc=0)
f_selftest_c2=selftest cases=137 failures=1 (rc=1; form: --pure only (--work/--jobs rejected by argparse: r46-counters-selftest-c2.py: error: unrecognized arguments: --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/junk/w/c2 --jobs 8))
g_battery_c1=not-run
g_battery_c2=not-run
```

The five census measures move exactly onto the C2 after-values (29 / admitted=29 exit 0 / 74 / 66
/ 4) when an F29-shaped tree is substituted and sit on the before-values (28 / SHORT exit 1 / 73 /
65 / 2) when it is not: the script discriminates the two worlds, and the do-nothing base export
cannot reach the target. (The `f_selftest_c2` `failures=1` on the junk tree is F7's collision
showing up inside the selftest — see there.)

---

## F5 — FINDING: the card's (e) before-value is wrong; the frozen claim's is right

The card says "(e) absence sweep … (base 1)". Measured at the frozen base export: **2 files**, not
1 (F2, quoted). The two files are exactly the ones claim C2 names: the F28 entry
`corpus/knowledge/github-private-vulnerability-reporting.md` (its body quotes the link text
"Creating a repository security advisory") and `corpus/SOURCES.md` (row S068's
`GHSA-v676-f8gm-92r9` cell plus the round-43 screen-log line 157's `GHSA-v6mg-96c6-gmpq`). The
frozen claim's "before" says "prints 2 files (the F28 entry's scope-out note and the S068
rejected-database row's search-log context …)" — that matches the measurement. **The card's
`base 1` is the error, not the claim.** Nothing in the lane changes this: the sweep is a
`grep -rli` over three paths, so it counts files, and both files match at the base. The C2
after-value 4 (= README + SOURCES + the F28 entry + the new entry) is what the live lane reads
now, and what the junk control reproduced.

---

## F6 — FINDING: the card's (f) c2 twin command is rejected by argparse

The card's c2 twin is `python3 .../r46-counters-selftest-c2.py --pure <pure> --work <scratch>
--jobs 8`. That script's argparse has neither flag (only `--lane --pure --counter
--do-nothing-control --keep -v`):

```
$ python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/tmp-w --jobs 8 | tail -3; echo "exit=${PIPESTATUS[0]}"
                                   [--counter COUNTER] [--do-nothing-control]
                                   [--keep] [-v]
r46-counters-selftest-c2.py: error: unrecognized arguments: --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/tmp-w --jobs 8
exit=2
```

The frozen claim's own `plain` list agrees with the tool, not the card:
`python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure> | tail -1`. The delivered
script tries the card's form, falls back, and prints the form used (F2/F3/F4). The c2 selftest
also cannot be given a work dir at all: it builds its scratch under
`$HYAKU_SCRATCH/kasegi-r46/R46W2ExecSelftestC2/` from its own code, so the script exports
`HYAKU_SCRATCH` to its own scratch root to keep every byte it causes inside its own scratch.

---

## F7 — FINDING (cross-claim collision; an L1 decision, not a seat fix): the C2 after-state breaks the frozen c2 counter, and with it the C1 "selftests keep failures=0" after-state

The frozen, READ-ONLY-for-all-seats counter `corpus/instruments/r46-c2-gate.py` pins the corpus
census in G1/G6 (base bytes `:178`: `if len(rows) != 28 or adm != 28 or dup:` and the G6
`knowledge=65` limb). Run against the junk F29 tree it reads:

```
$ python3 -B corpus/instruments/r46-c2-gate.py --root "$E/junk"; echo "exit=$?"
gate G1 pass=0 read=rows=29 admitted=29 dup=0
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
gate G7 pass=0 read=census-rc=1 ok-line=0
c2-gate fixed=4/7 exit=1
exit=1
```

Against the base export the same counter reads `c2-gate fixed=7/7 exit=0` — pinned twice: by the
committed receipt's battery (its `baseline_failures=0` on every `mutant=` line of
`controls/mutbat-before.txt`) and by my base run's c2 battery (`logs/base/bat-c2.log`, likewise
`baseline_failures=0` throughout). Measured on the live lane AFTER the wave's C2 landing (20:47):

```
$ python3 -B corpus/instruments/r46-c2-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin; echo "exit=$?"
gate G1 pass=0 read=rows=29 admitted=29 dup=0
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
exit=1
```

— i.e. even the lane's own (already amended, still uncommitted) c2 counter reads 5/7 at the
current tip state (measured 20:47): the census pins have not been re-pinned to 29/66 yet.

Consequence, measured twice: the committed c2 selftest's control case that grades the counter
against the lane tree itself FAILS on such a tree, so the selftest stops reading `failures=0`:

```
$ grep -n "FAIL" .../R46bExecPlain.draft/logs/junk-c2-selftest-v.txt
1089:FAIL control ctl-committed-tip-direct fixed=4/7 failing=['G1', 'G6', 'G7']  <- control-not-7/7 failing=['G1', 'G6', 'G7']
$ tail -1 .../R46bExecPlain.draft/logs/junk-c2-selftest-v.txt
selftest cases=137 failures=1
```

This collides the two frozen claims on the same bytes:

* C2 "after" = **29 admitted frontier rows, 66 knowledge entries** (claims.json C2.after);
* C1 "after" = the extended selftests "keep `failures=0` baselines **at the final revision**", and
  its kill rule fires on "`baseline_failures!=0`" — which is exactly the c2 selftest's `failures=`
  count (`r46-mutbat.py`: `m = re.findall(r"failures=(\d+)", p.stdout)` → `baseline_failures`).

So on any tree carrying the C2 after-state, the c2 battery's baseline is dirty and C1's kill rule
fires — unless the frozen c2 counter's G1/G6 census pins (and the selftest's expectations with
them) move in a logged erratum, which the claims reserve to the L1 ("The attempt-1 counters … are
NOT edited by this round's claims (any amendment is a logged erratum)"). The junk control shows
the collision lands on the *baseline*, not on a mutant; the live lane shows it is not hypothetical.
Caveat: the junk tree is a shape control — the real tip adds the S074 row, capture and manifest on
top, which can only add census deltas, so the direction of the collision is fixed even where the
exact gate count at the real tip is not.

---

## F8 — FINDING (measurement validity): the c2 battery grades the LIVE LANE, not `--root`, so its verdicts move while the lane is edited

The c2 selftest's control case `ctl-committed-tip-direct` is defined as "the counter run on
`--lane` itself" (base bytes: case added at `:537`) and executes
`run_counter(counter, a.lane, env)` (base bytes: `:552`; `:721`/`:758` in the lane's rewritten,
uncommitted copy). `r46-mutbat.py` never passes `--lane` to the c2 selftest (its `run_selftest`
adds only `--pure` for c2), so `a.lane` stays the selftest's hard-coded default: the LIVE LANE.
Three runs of the same frozen bytes show what that does:

| run | `--root` | lane state during the c2 half | c2 summary |
|---|---|---|---|
| committed receipt (18:19) | freeze tree | quiet, 7/7 | `mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0` |
| my live-lane run (c2 half ≈18:40–19:25, log `logs/live/bat-c2.log`) | live lane | still green, 7/7 | `mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0` |
| my junk-tree run (20:18–20:36, log `logs/junk-mutbat-c2.txt`) | base export copy | mid-landing (corpus writes 20:33–20:34) | `mutants=21 caught=13 equivalent=0 uncaught=8 baseline_failures=0` |

The five mutants that flipped in the mid-landing window (`G6b-integrity-loose`, `G6c-size-low`,
`G7a-verdict-or`, `G7b-symlink-dead`, `G7c-okline-loose`) are exactly the tail of the battery's
mutant list — a time boundary, not a bytes difference: the lane stopped reading 7/7 part-way
through the sweep, and every mutant graded after that moment was scored "caught" by the failing
control case instead of by its own defect.

Positive control that the bytes themselves still reproduce the receipt's verdict (run 20:42, 51 s):
the G7a mutant (a copy of the base counter with the single G7a edit applied once) run by the c2
selftest with `--lane` pinned to the STABLE base export reads:

```
$ python3 -B .../g7a/corpus/instruments/r46-counters-selftest-c2.py --lane <base export> --counter .../g7a/corpus/instruments/r46-c2-gate.py --pure .../pure2
…
selftest cases=137 failures=0        (exit=0; no FAIL lines)
```

i.e. uncaught, exactly as the receipt says. So the flip was lane-state contamination, not byte
drift. **For the C1 claim this means the after-value `uncaught=0` for c2 is only trustworthy when
the lane is quiet or when `--lane` is pinned; the frozen mutbat v1 offers no way to pin it, so the
L1's final measure should either run on a quiet lane or add a `--lane` passthrough as a logged
erratum.** (The c1 selftest has the same exposure by a second route: its synthetic recheck lines
are `cd <LANE> && python3 corpus/instruments/r46-c1-gate.py …`, so its L1 limb executes the live
lane's gate file.)

---

## F9 — (g) BATTERY SUMMARY LINES (the card's item, answered)

Base, quoted from the committed receipt (the claim designates it as the before-value):

```
$ grep '^mutbat counter=' .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

Base, re-run by this seat on the frozen base export (F2): the same two lines, byte-identical.
Live lane (F3): `caught=17 uncaught=3` (c1 — the wave's new cases landing mid-run) and
`caught=8 uncaught=13` (c2). Per-mutant logs are preserved in
`R46bExecPlain.draft/logs/{base,live}/bat-c{1,2}.log`.

---

## Limitations

1. **The battery is hours, not seconds.** One mutant = one full selftest run; the c1 battery is 21
   runs, the c2 battery 22. Under this host's load (load average 148 on 32 cores while sibling
   seats ran their own jobs) the full nine-line script run took 2.1–2.2 h per tree. Both of my
   nine-line runs completed within the 3 h per-battery bound I set
   (`PLAIN2_BATTERY_TIMEOUT=10800`); a c2 sweep started on a busier evening would not.
2. **The live-lane run is time-mixed and its c1 half is mid-landing** (F3): the census lines and
   the battery read different moments of the same worktree, and the instrument digests changed
   under the run (`logs/live-instrument-sha-{before,after}.txt`). Treat F3's `caught=17` as a
   progress observation, not a verdict about any revision.
3. **The junk control is a shape control** (F4/F7): it proves the measures discriminate and that
   the frozen c2 counter's census pins break on an F29-shaped tree; it proves nothing about
   whether the real F29 admission is correct.
4. **No live-target testing**: the corpus is documentation only; every command above read
   committed or scratch bytes; nothing was fetched from the network.
5. **No repo mutation**: the only `git` invocations were `archive`, `ls-tree`, `log`, `status`,
   `diff --stat`, `rev-parse` (read-only). No commit, no push, no index or worktree write in the
   lane; no file outside the seat's draft directory, its logs, and its scratch was created or
   changed. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46bExecPlain*`) is removed before yield.
6. **The script is a DRAFT** in the seat's draft directory; the L1 owns integration, and the
   errata it flags (F7, F8) are not applied by this seat. Attribution of the four c1 mutant flips
   to specific new selftest cases was not chased (the modified c1 selftest does not name cases
   after mutant ids; that is the C1 seats' work, not this seat's).
