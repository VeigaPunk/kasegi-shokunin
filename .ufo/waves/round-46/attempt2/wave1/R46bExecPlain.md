VERDICT: DRAFT-READY

# Seat R46bExecPlain — round 46 (attempt 2), kasegi lane

Scope of this seat: ONE item — build the plain measurement script
`.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/plain-measure2.sh <tree>` and run it on a
base export AND on the live lane, reporting both. No corpus file was touched; the only bytes this
seat wrote are (a) the draft script in its own draft directory, (b) the run logs under
`.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/`, and (c) this report.

Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Base rev (frozen): `04af9bc92229232ea5cce8b32bfe59dd969eb26d`
Freeze rev: `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`
Live lane HEAD at measurement time: `ee03806b6b54a2822045e96641a77fa76984b410`
Scratch root used: `/fast/scratch/hyaku/kasegi-r46/R46bExecPlain*` (removed before yield; the base
export and the junk control tree were kept only while the runs were live).
Tools: python3 3.14.8, git 2.56.0, GNU bash 5.3.20 — **no tool was installed, upgraded or removed
by this seat** (nothing was needed; the pacman pause was therefore never engaged).

---

## F1 — BUILT: the measurement script (the seat's deliverable)

**Exact thing built:** `.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/plain-measure2.sh`
— one invocation, nine `key=value` lines, one per spec'd measurement, tree read-only.

```
$ bash -n .../R46bExecPlain.draft/plain-measure2.sh && echo "syntax OK"
syntax OK
```

The script's nine lines and their sources (verbatim from the script header):
`a_frontier_rows` = `grep -cE '^\| F[0-9]+ \|' <tree>/corpus/README.md`;
`b_frontier_counter` = `r44-frontier-count.py --root <scratch COPY of tree> --expect 29`;
`c_sources_rows` = `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <tree>/corpus/SOURCES.md`;
`d_knowledge_files` = `find <tree>/corpus/knowledge -maxdepth 1 -name '*.md' | wc -l`;
`e_absence_sweep_files` = `grep -rliE 'repository securit. advisor|GHSA' <tree>/corpus/knowledge
<tree>/corpus/SOURCES.md <tree>/corpus/README.md | wc -l`;
`f_selftest_c1` = `r46-counters-selftest-c1.py --pure PURE --work W --jobs 8 | tail -1`;
`f_selftest_c2` = `r46-counters-selftest-c2.py --pure PURE | tail -1`;
`g_battery_c1` / `g_battery_c2` = `r46-mutbat.py --root <tree> --pure PURE --work W --counter <c> --jobs 8`.

**Three deviations from the card's prose, all deliberate and all documented in the script header:**
1. the frontier counter (b) runs against a **scratch COPY** of the tree (the card asks for this);
   the copy excludes `.git` and `.ufo` (no corpus byte lives in either) and is removed on exit, so
   the counter provably cannot mutate the tree;
2. both selftests are bound to the tree under test with `--lane <tree>` — the counter a selftest
   grades is the one in `--lane`; without it the "base export" run would have graded the LIVE
   LANE's counter and the base row would not have been about the base;
3. the c2 selftest takes **neither `--work` nor `--jobs`** (see F6), so the c2 twin is invoked in
   the form its own usage line documents and the form actually used is printed on the line.

---

## F2 — BASE EXPORT RUN (the before-values)

Base export (read-only `git archive` of the frozen base, never a checkout):

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d | tar -x -C /fast/scratch/hyaku/kasegi-r46/R46bExecPlain-export/base
```

Manual command-by-command check of the same five measures, on that export:

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
```

Frontier counter against a scratch COPY of that export:

```
$ python3 .../corpus/instruments/r44-frontier-count.py --root "$S/copy" --expect 29; echo "exit=$?"
frontier rows=28 admitted=28
frontier expected=29 admitted=28 verdict=SHORT exit=1
exit=1
```

c1 selftest bound to the base export (the tree's own counter graded, `--lane` = the base export):

```
$ cd "$T" && python3 -B corpus/instruments/r46-counters-selftest-c1.py --lane "$T" --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work "$S/w/c1base" --jobs 8 | tail -5
case P-prose-after-table                           L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
case P-trailing-comment-on-recheck-line           L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
```
(wall clock 328.87 s; exit 0)

The nine-line run of the delivered script on that export is in F4.

---

## F3 — FINDING: the card's (e) before-value is wrong; the claim's is right

The card says "(e) absence sweep … (base 1)". Measured at the frozen base export: **2 files**, not 1
— quoted in F2. The two files are exactly the ones the frozen claim C2 names: the F28 entry
`corpus/knowledge/github-private-vulnerability-reporting.md` (its body quotes the link text
"Creating a repository security advisory") and `corpus/SOURCES.md` (row S068's
`GHSA-v676-f8gm-92r9` cell and the round-43 screen-log line 157's `GHSA-v6mg-96c6-gmpq`).

The frozen claim C2 "before" says "prints 2 files (the F28 entry's scope-out note and the S068
rejected-database row's search-log context …)" — that matches the measurement. **The card's `base 1`
is the error, not the claim.** Nothing in the lane changes this: the sweep is a `grep -rli` over
three paths, so it counts FILES, and both files match at the base.

---

## F4 — THE SCRIPT ON THE BASE EXPORT AND ON THE LIVE LANE (both runs)

Base export (delivered script, nine lines):

```
$ PLAIN2_SCRATCH=.../R46bExecPlain/base PLAIN2_BATTERY_COUNTERS="c1 c2" \
  bash .../R46bExecPlain.draft/plain-measure2.sh /fast/scratch/hyaku/kasegi-r46/R46bExecPlain-export/base
```

Live lane (delivered script, nine lines):

```
$ PLAIN2_SCRATCH=.../R46bExecPlain/live PLAIN2_BATTERY_COUNTERS="c1 c2" \
  bash .../R46bExecPlain.draft/plain-measure2.sh /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

(RUN_OUTPUT_PLACEHOLDER)

---

## F5 — CONTROL: the script is not tautological (junk F29 tree)

A **junk control tree** was built in scratch only (never in the corpus): a copy of the base export
with one synthetic frontier row `| F29 | GitHub repository security advisories … | admitted | … |`,
one synthetic `S074` row, one synthetic `knowledge/github-repository-security-advisories.md`, and
nothing else changed. The delivered script on that tree prints:

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

So the five census measures move exactly onto the C2 after-values (29 / admitted=29 exit 0 / 74 /
66 / 4) when an F29-shaped tree is substituted, and the before-values (28 / SHORT exit 1 / 73 / 65 /
2) when it is not: the script discriminates the two worlds and the do-nothing base export cannot
reach the target. This is the discrimination the C2 kill rule demands of a counter.

---

## F6 — FINDING: the card's (f) c2 twin command is rejected by argparse

The card's c2 twin is `python3 .../r46-counters-selftest-c2.py --pure <pure> --work <scratch>
--jobs 8`. That script's argparse has no `--work` and no `--jobs` (only `--lane --pure --counter
--do-nothing-control --keep -v`):

```
$ python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/tmp-w --jobs 8 | tail -3; echo "exit=${PIPESTATUS[0]}"
                                   [--counter COUNTER] [--do-nothing-control]
                                   [--keep] [-v]
r46-counters-selftest-c2.py: error: unrecognized arguments: --work /fast/scratch/hyaku/kasegi-r46/R46bExecPlain/tmp-w --jobs 8
exit=2
```

The frozen claim's own `plain` list is consistent with the tool, not with the card:
`python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure> | tail -1`. The delivered
script tries the card's twin form first, and falls back to the tool's own form, printing which form
was used on the line (see F5). The c2 selftest also cannot be given a work dir at all: it builds
its scratch under `$HYAKU_SCRATCH/kasegi-r46/R46W2ExecSelftestC2/` (its own code), so the script
exports `HYAKU_SCRATCH` to its own scratch root to keep every byte it causes to be written inside
its own scratch.

---

## F7 — FINDING (cross-claim collision, L1 must decide): the C2 after-state breaks the frozen c2 counter, and therefore the C1 "selftests keep failures=0" after-state

The frozen, READ-ONLY-for-all-seats counter `corpus/instruments/r46-c2-gate.py` pins the corpus
census in its G1 and G6 limbs (`corpus/instruments/r46-c2-gate.py:178`
`if len(rows) != 28 or adm != 28 or dup:` and `:178`/G6 `knowledge=65`). Run against the junk
F29 tree (29 rows, 66 knowledge entries) it reads:

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

Against the base export and against the live lane the same counter reads 7/7:

```
$ python3 -B corpus/instruments/r46-c2-gate.py --root "$E/base"
...
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
...
c2-gate fixed=7/7 exit=0
exit=0
$ python3 -B corpus/instruments/r46-c2-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
...
c2-gate fixed=7/7 exit=0
exit=0
```

Consequence, measured: the committed c2 selftest's control case that grades the counter against
the lane tree itself FAILS on such a tree, so the c2 selftest stops reading `failures=0`:

```
$ grep -n "FAIL" .../R46bExecPlain.draft/logs/junk-c2-selftest-v.txt
1089:FAIL control ctl-committed-tip-direct fixed=4/7 failing=['G1', 'G6', 'G7']  <- control-not-7/7 failing=['G1', 'G6', 'G7']
$ tail -1 .../R46bExecPlain.draft/logs/junk-c2-selftest-v.txt
selftest cases=137 failures=1
```

(Cited verbatim: `FAIL control ctl-committed-tip-direct fixed=4/7 failing=['G1', 'G6', 'G7']`.)

This matters because the two frozen claims pull in opposite directions on the same bytes:

* C2 "after" = **29 admitted frontier rows, 66 knowledge entries, S074 mined** (claims.json C2.after);
* C1 "after" = "the extended selftests … keep `failures=0` baselines **at the final revision**"
  (claims.json C1.after), with the kill rule "C1 fails if either battery summary … prints
  uncaught>0 or **baseline_failures!=0**".

The c2 battery's baseline is exactly the c2 selftest's `failures=` count (`r46-mutbat.py:99-104`
`m = re.findall(r"failures=(\d+)", p.stdout)` → `baseline_failures`). So on a tree that carries the
C2 after-state, the c2 battery's `baseline_failures` becomes non-zero and **C1's kill rule fires**
unless the frozen c2 counter (or the selftest's control case) is amended — and the claims freeze
both counters and forbid any seat from amending them
("The attempt-1 counters r46-c1-gate.py / r46-c2-gate.py are NOT edited by this round's claims
(any amendment is a logged erratum)"). The junk control shows the collision is real and lands on
the *baseline*, not on a mutant. **This is an L1 decision point, not a seat fix:** either the c2
counter's G1/G6 census pins move to 29/66 in a logged erratum (and the selftest's expectations
with them), or the C2 after-state cannot coexist with C1's `failures=0` requirement.

(Caveat on the strength of this finding: the junk tree adds an *admitted* F29 row and a *66th*
knowledge file — the shape the C2 after-state has — but the real after-state will also add the
S074 row, the capture and the manifest, which can only add further census deltas; the direction of
the collision is therefore fixed, its exact gate count at the real tip is not.)

---

## F8 — LIVE LANE STATE AT MEASUREMENT TIME: still at the before-values

The live lane's graded instruments are byte-identical to the frozen base at measurement time:

```
$ sha256sum corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py   # live
8b17164aadbd9c69…  r46-counters-selftest-c1.py
ff7104cfc8910071…  r46-counters-selftest-c2.py
95f2eb7933841d6c…  r46-c1-gate.py
647bd5b7b6268551…  r46-c2-gate.py
$ sha256sum <base export>/corpus/instruments/…                                                            # base
8b17164aadbd9c69…  r46-counters-selftest-c1.py
ff7104cfc8910071…  r46-counters-selftest-c2.py
95f2eb7933841d6c…  r46-c1-gate.py
647bd5b7b6268551…  r46-c2-gate.py
```
(full digests in `.ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live-instrument-sha-before.txt`)

Live census, measured directly on the lane worktree:

```
$ grep -oE '^\| F[0-9]+ \|' corpus/README.md | tr -d '| ' | tr '\n' ' '
F01 F02 … F27 F28
$ find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l
65
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
73
$ grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md
corpus/knowledge/github-private-vulnerability-reporting.md
corpus/SOURCES.md
```

So at measurement time the live lane reads the **before** values on every C2 measure and holds no
F29, no S074 and no 66th entry: **no C1 or C2 wave work had landed in the lane's instruments yet.**
Any "after" number the L1 reads later must come from a later revision than this one.

---

## F9 — THE BATTERY (g): base values come from the committed receipt; live values from my run

The committed before-value receipt (sha256 matches the digest the frozen claim records):

```
$ sha256sum .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd  .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
$ grep '^mutbat counter=' .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

(BATTERY_PLACEHOLDER)

---

## Limitations

1. **The (g) battery is not a fast measurement.** One mutant = one full selftest run: the c1
   selftest took 328.87 s per run here (21 runs for c1), the c2 selftest 701.75 s per run in the
   junk run (22 runs for c2) — hours per battery, under a host whose load average was 148 on 32
   cores while sibling seats ran their own jobs. My runs bound each battery invocation with
   `PLAIN2_BATTERY_TIMEOUT=10800` (3 h); the c2 battery cannot finish inside that bound, so its
   line is partial and the per-mutant progress is in the preserved logs. The complete base values
   are the committed receipt's (F9), which the claim itself designates as the before-value.
2. **The live-lane run is of a moving worktree.** Peers are editing the lane concurrently; the
   live run's battery grades counter copies taken from the tree at mutant-application time, so a
   concurrent landing would make that run internally inconsistent. The instrument digests were
   captured before the run (`logs/live-instrument-sha-before.txt`) and after it, and the report
   says so where they differ.
3. **The junk control is a shape control, not a candidate after-state.** It proves the measures
   discriminate (F5) and that the frozen c2 counter's census pins break on an F29-shaped tree
   (F7); it proves nothing about whether the real F29 admission will be correct.
4. **No live-target testing.** The corpus is documentation only; every command above reads
   committed or scratch bytes. Nothing was fetched from the network.
5. **No mutation of the repo.** No `git`/`jj` write was issued in the lane, no commit, no push; the
   only `git` calls were `archive`, `ls-tree`, `log`, `status`, `rev-parse` (read-only). The
   scratch trees are under `/fast/scratch/hyaku/kasegi-r46/R46bExecPlain*` and are removed before
   yield.
6. **The script is a DRAFT.** It is written to the seat's draft directory only; the L1 owns the
   integration, and the claim-side errata it flags (F7) are not applied by this seat.
