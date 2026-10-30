# R46bExecControls — round-46 (attempt 2) freeze controls runner

VERDICT: DRAFT-READY

Seat: `R46bExecControls` (executor), lane `kasegi-shokunin`, round 46 attempt 2.
Deliverables (draft only, not committed):

- the controls runner `.ufo/waves/round-46/attempt2/wave1/R46bExecControls.draft/run-controls.sh`
- the receipt it produced
  `.ufo/waves/round-46/attempt2/wave1/R46bExecControls.draft/freeze-controls.txt`
  — `checks: 13  failed: 0`, ending
  `VERDICT: HOLDS — every declared before-value re-derived from committed bytes (13 checks, 0 failed).`

The runner is the artifact `freeze.txt` names as the freeze-check replay
("run-controls.sh (wave 1) re-derives every declared before-value at the base export before any
seat result is integrated"). Its default output path is the canonical control file the claims
name (`.ufo/waves/round-46/attempt2/controls/freeze-controls.txt`); this seat's own run wrote
the receipt into its draft directory instead, because a builder seat may write only its own
draft dir and its Report file. Running it with no argument lands the canonical receipt.

## What the runner does

It re-derives, from committed bytes only, the four before-values the round-46 (attempt 2)
freeze declares, and grades each one:

1. `corpus/instruments/r46-f29-gate.py` (frozen v1, sha256
   `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`, extracted from the
   freeze tree by `git archive`) replayed on four trees: the base export of
   `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, the freeze tree
   `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`, and the junk / fabricated / positive trees the
   committed `.ufo/waves/round-46/attempt2/controls/f29-fixture.py` builds from the freeze tree.
2. `corpus/instruments/r46-mutbat.py` (frozen v1, sha256
   `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`) replayed at the base
   export, `--counter c1` and `--counter c2` concurrently; every `mutant=` line and both
   `mutbat counter=...` summary lines are diffed against the same two line classes in
   `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`.
3. The stub-selftest control: the lane tree is copied to scratch, its
   `corpus/instruments/r46-counters-selftest-c1.py` is replaced by a stub whose cases all pass
   (`selftest cases=1 failures=0` printed unconditionally), and the battery is rerun — every
   mutant must read `verdict=uncaught` and the battery must exit 1. A battery that graded
   markers instead of the selftest's own verdict would still report caught mutants; that is the
   defect this control catches.
4. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kasegi` — expect exit 0 and exactly three `W04` warnings, run
   before the receipt closes.

Read-only on the lane: git is used only as `git archive` / `git show`; the lane's `corpus/` and
`.ufo/` trees are never written. Scratch lives under
`$HYAKU_SCRATCH/kasegi-r46/R46bExecControls.$$/` (pid-suffixed so two concurrent runs cannot
share it; `HYAKU_SCRATCH` defaults to `/fast/scratch/hyaku`) and is removed by an `EXIT` trap;
`TMPDIR` is set explicitly to a scratch subdir, and `HYAKU_SCRATCH` is re-pointed at the seat's
own scratch so the c2 selftest's fixed scratch name cannot collide with another seat's. The
pure export `/fast/scratch/hyaku/kasegi-r46/L1/pure2` is copied, never edited. The receipt file
is truncated at run start and carries a `# receipt-end` marker line, so an interrupted run can
never be mistaken for a complete one.

## Findings (each re-run by this seat; the run completed 2026-10-29T22:34:58Z-23:49 local)

### F1. The frozen f29-gate reads 1/7 at the base export — only H7 green

```
$ python3 <frozen r46-f29-gate.py> --root <base export of 04af9bc...> --work <scratch>
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1
```

This reproduces the committed `controls/f29-gate-at-base.txt` limb for limb. Receipt check:
`CHECK 1a base export reads fixed=1/7: PASS (expected=1/7 H7 actual=1/7 H7)`.

### F2. The frozen f29-gate reads 2/7 at the freeze tree — H4 and H7 green

```
$ python3 <frozen r46-f29-gate.py> --root <freeze tree fe0f56b...> --work <scratch>
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=2/7 exit=1
```

Receipt check: `CHECK 1b freeze tree reads fixed=2/7: PASS (expected=2/7 H4,H7 actual=2/7
H4,H7)`. H4 is green because the freeze commit carries the S074 capture and the round-46-a2
manifest; H7 because the census accepts the freeze tree's `SOURCES.md`. This matches the
claim's declared `freeze_tree_reading` (H4 capture + H7 census green at the freeze tree).

### F3. The junk and fabricated fixture trees grade below 7/7 — only H5 red

Built by the committed `f29-fixture.py` from the freeze tree. Junk tree (verbatim):

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=6/7 exit=1
```

Fabricated tree (verbatim):

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=6/7 exit=1
```

Both are `<7/7` and the red limb is H5 in both — the located-quote/cores limb the junk and
fabricated defects are built to trip. Receipt checks: `CHECK 1c junk fixture tree grades <7/7:
PASS`, `CHECK 1c fabricated fixture tree grades <7/7: PASS`.

Discriminator against a do-nothing gate: the **positive** fixture tree built by the same
committed script reads 7/7, so the gate is not vacuously red on this fixture family (verbatim:
`gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5 ... f29-gate fixed=7/7
exit=0`); receipt check `CHECK 1c positive fixture tree reads 7/7 (the gate is not vacuously
red): PASS`.

### F4. The frozen R50 receipt's junk/fabricated numbers do not reproduce; the committed fixture gives 6/7

The frozen `controls/f29-r50-receipt.txt` states (lines 6-7, quoted verbatim):

```
Positive tree reads `f29-gate fixed=7/7 exit=0`; junk tree `fixed=3/7` (H2/H5 red:
2/7 quotes located, 0/5 cores); fabricated tree `fixed=3/7` (5/7 located, 4/5 cores).
```

Re-deriving with the **committed** `f29-fixture.py` gives junk `6/7` and fabricated `6/7`
(F3), not `3/7`. The H5 limb reads match the receipt exactly (`located=2 ... cores=0/5` for
junk; `located=5 ... cores=4/5` for fabricated), so the limb-level story is the same; only the
totals differ. The cause is visible in the stale R50 scratch trees, which the runner re-grades
as section 1d. Their `SOURCES.md` S074 row has **12 cells**, not the 11 the contract requires,
so the census rejects them and H3/H7 go red for that reason rather than for the defect the tree
was built to carry. Re-grading the stale R50 trees with the frozen gate (verbatim):

```
$ python3 <frozen r46-f29-gate.py> --root /fast/scratch/hyaku/kasegi-r46/L1/f29r50/junk --work <scratch>
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=1
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=0 read=census-rc=1 ok-line=0
f29-gate fixed=4/7 exit=1
```

and the stale fabricated tree reads `fixed=4/7` the same way (H3, H5, H7 red). The census on
the stale junk tree's `SOURCES.md`, directly:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r46/L1/f29r50/junk/corpus/SOURCES.md
file	E01	S074 fields=12
exit=1
```

So the receipt's `3/7` is reproducible from no tree I can reach (committed fixture: 6/7; stale
trees: 4/7), and its own parenthetical ("H2/H5 red" = 2 red limbs) is inconsistent with its own
total (3/7 = 4 red limbs). The C2 kill rule only requires the junk and fabricated trees to
grade `<7` — every reading satisfies that — but the L1 should know the receipt's quoted `3/7`
is stale before resting a verdict on it.

### F5. The frozen battery reproduces the committed before-value receipt, line for line

```
$ python3 <frozen r46-mutbat.py> --root <base export> --pure <copy of pure2> --work <scratch>/mut-c1 --counter c1 --jobs 8
$ python3 <frozen r46-mutbat.py> --root <base export> --pure <copy of pure2> --work <scratch>/mut-c2 --counter c2 --jobs 8
```

Summaries produced (verbatim):

```
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

The runner's comparison (verbatim from the receipt):

```
before-value comparison
  mine   (c1 run + c2 run): 43 kept lines
  receipt (controls/mutbat-before.txt): 43 kept lines
  RESULT: IDENTICAL — every mutant line and both summary lines match the frozen receipt
comparison exit=0 (0 = the replay reproduces the frozen before-value lines)
CHECK 2 mutbat replay reproduces the frozen before-value lines: PASS (expected=0 actual=0)
CHECK 2a mutbat --counter c1 exit status (uncaught>0 => 1): PASS (expected=1 actual=1)
CHECK 2b mutbat --counter c2 exit status (uncaught>0 => 1): PASS (expected=1 actual=1)
```

This is the C1 kill rule's "the before-value must stay reproducible at the base export" leg:
the battery is not marker-grading, and its per-mutant `mutant_failures` counts (e.g.
`mutant=M01-L1-target-24 ... mutant_failures=26`, `mutant=G3c-kind-dead ... 94`) reproduce
exactly. The receipt file itself hashes identically in the working tree and at the freeze rev
(`13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`).

### F6. The stub-selftest control: the battery grades the selftest, not markers

The runner copies the lane tree to scratch, replaces
`corpus/instruments/r46-counters-selftest-c1.py` with a stub whose cases all pass (it prints
`selftest cases=1 failures=0` unconditionally), and reruns the battery. Output (verbatim):

```
mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M04-L2-one-reground baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M05-L3-shape-loose baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M07-L3-home-no-abs baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M08-L4-bytes-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M09-L4-planted-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M10-L4-symlink-ok baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M11-L5-prefix-flip baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M12-L5-restore-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M13-L6-control-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M14-L6-exit-ignored baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M15-L7-always-true baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M16-min-rows-5 baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M17-min-token-1 baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M18-anchor-dirs-wide baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M19-L2-eq-relaxed baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=0 verdict=uncaught
mutbat counter=c1 mutants=20 caught=0 equivalent=0 uncaught=20 baseline_failures=0
```

Receipt checks (all PASS):

```
CHECK 3 stub selftest: the battery exits 1: PASS (expected=1 actual=1)
CHECK 3 stub selftest: every mutant line reads verdict=uncaught: PASS (expected=20 actual=20)
CHECK 3 stub selftest: the summary reads uncaught=20 caught=0: PASS (expected=20 0 actual=20 0)
```

Discriminator: at the same tree with the *real* selftest the same battery reports
`caught=13` for c1 (F5), so the caught/uncaught verdict demonstrably comes from the selftest's
own failure count and not from a marker the battery grades instead. The receipt also prints the
counter sha256 of the stubbed tree (lane HEAD
`95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7`) and of the base export's
counter (same digest) so the reader can see the stub control graded the same counter bytes that
F5 graded.

### F7. The census validation is clean with exactly three W04 warnings

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
W04 warning lines: 3
CHECK 4 census validate exits 0: PASS (expected=0 actual=0)
CHECK 4 census validate prints three W04 warnings: PASS (expected=3 actual=3)
```

The three W04s are the same three the frozen `controls/sources-census-before.txt` already
carries.

### F8. The claims' named control file does not exist at the freeze commit

Both claims name the same control file
(`.ufo/waves/round-46/attempt2/controls/freeze-controls.txt`), and `freeze.txt` line 10 names
the `run-controls.sh` that was to produce it — neither exists in the freeze commit
`fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`, which ships seven control files (`f29-defects.py`,
`f29-fixture.py`, `f29-gate-at-base.txt`, `f29-r50-receipt.txt`, `mutbat-before.txt`,
`selftest-baselines.txt`, `sources-census-before.txt`). This seat's runner is that missing
`run-controls.sh`; the L1 lands it (and the receipt it writes) at integration.

## Limitations

- **The mutbat replay is slow under a loaded host.** The battery runs 20 c1 mutants and 21 c2
  mutants, each mutant re-running the whole selftest suite; this run took ~75 minutes
  (19:35-20:49 local) on a host whose load average sat between 70 and 290 on 32 cores, with
  ~30 sibling seats running their own batteries. The runner therefore leaves the two counters
  concurrent, keeps per-mutant output in scratch as it goes, and stamps the receipt with a
  `# receipt-end` marker plus the run's start time so a truncated receipt is detectable.
- **The c2 selftest reads the LIVE lane.** `r46-counters-selftest-c2.py` defaults `--lane` to
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin` and copies the lane's C1 knowledge entries
  into every synthetic tree, so the c2 before-value is a function of the live lane's bytes at
  run time, not only of the base export. The runner records the live lane's HEAD, its
  `corpus/SOURCES.md` sha256, its knowledge-entry count, its README F-row count and its
  dirty-`corpus/` count in the receipt header. At this run: HEAD
  `ee03806b6b54a2822045e96641a77fa76984b410`, 65 knowledge entries, 28 F rows, 0 dirty
  `corpus/` paths — i.e. the same corpus bytes the freeze declared. The c1 selftest reads only
  the pure export and the counter under test. If the L1 lands wave-1 corpus work before
  re-running this control, the c2 half of the comparison must be re-checked.
- **The pure export is taken as given.** The runner copies
  `/fast/scratch/hyaku/kasegi-r46/L1/pure2` and never edits it; it is the round-15 base export
  the task card designates, but nothing here re-verifies its provenance.
- **The stale R50 scratch trees live outside the lane.** F4 re-grades trees under
  `/fast/scratch/hyaku/kasegi-r46/L1/f29r50/`, which another seat owns and may delete; that
  section degrades gracefully (skipped when the trees are absent) and the authoritative reading
  is the one the committed fixture builds.
- **Tooling.** Nothing was installed or updated; pacman was not invoked (the host-wide pacman
  pause stands). The run used only `git` (read-only `archive`/`show`), `bash`, `python3`
  3.14.8 and coreutils already present.
- **No commits, pushes, or mutating git/jj command anywhere; no fleet-repo, sibling-lane,
  `MANIFEST.json`, `.ufo/state` or `~/Projects/shokuknow` writes.** The lane working tree is
  untouched; this seat wrote only its draft directory and this Report.
