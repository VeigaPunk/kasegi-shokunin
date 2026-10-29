VERDICT: DRAFT-READY

# Seat R46bScribeSkillRegistry — round-46 (attempt 2) registry appends

Lane: kasegi, round 46 attempt 2, wave 1. Scope: the two registry appends only. Draft only — no
tracked file was edited, nothing was committed, no git/jj mutating command was run anywhere, the
fleet root, sibling lanes, `MANIFEST.json` and `.ufo/state` were not touched.

## What I built

Two files under
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/`:

- `SKILL-append.md` — the `## Round-46 (attempt 2) Gates & probes registry addition (appended 2026-10-29)`
  block for the END of `SKILL.md`, in the shape of the round-46 attempt-1 block at `SKILL.md:1157-1166`
  (heading, blank line, the same 8-column header `name | type | entry command | verdict map | self-test |
  pinned-value path | write scope | owner`, three data rows). One row each for
  `corpus/instruments/r46-mutbat.py`, `corpus/instruments/r46-f29-gate.py` and the planned
  `corpus/instruments/r46-selftest-f29.py`.
- `README-append.md` — the matching rows for `corpus/instruments/README.md`, following that file's
  round-44 addition section pattern (`README.md:979-1003`): a `## Round-46 (attempt 2) registry
  addition — …` heading, a short prose paragraph explaining that the gates' home registry stays
  `SKILL.md`'s *Gates & probes* section, then the same 8-column table with the same three rows.

Every row carries the four fields the card names: entry command, verdict map with exit 0/1
semantics, self-test command, pinned-value path.

## Findings

### F1 — the byte-check passes on a scratch copy (required `>= 2`)

Command (my own re-run, in scratch; the copy is `SKILL.md` with my block appended):

```
$ cp <lane>/SKILL.md $S/apply/SKILL.md && printf '\n' >> $S/apply/SKILL.md \
    && cat <draft>/SKILL-append.md >> $S/apply/SKILL.md
$ grep -c 'r46-mutbat' $S/apply/SKILL.md
2
```

`2` — the `r46-mutbat.py` row plus the `r46-f29-gate.py` row, whose self-test cell names the
battery extension `corpus/instruments/r46-mutbat.py --counter f29`. The same count on the README
copy is also `2`.

### F2 — table shape matches the attempt-1 block exactly (8 cells, no escaped pipes)

The attempt-1 round-46 rows in `SKILL.md:1161-1166` each split into exactly 8 cells on `|` with
zero escaped pipes (measured: `pipes: 9 escpipes: 0 cells_split: 8` per row). My rows are
identical in that respect — I first drafted with `\|` escapes and then removed them, because the
escapes inflate a naive `split("|")` cell count to 10-12 and the round-46 attempt-1 rows carry
none. Measured on the applied copies:

```
## SKILL.md | last table header at line 1170
   line 1170 cells: 8 esc: 0 | name
   line 1172 cells: 8 esc: 0 | r46-mutbat.py
   line 1173 cells: 8 esc: 0 | r46-f29-gate.py
   line 1174 cells: 8 esc: 0 | r46-selftest-f29.py
## README.md | last table header at line 1016
   line 1016 cells: 8 esc: 0 | name
   line 1018 cells: 8 esc: 0 | r46-mutbat.py
   line 1019 cells: 8 esc: 0 | r46-f29-gate.py
   line 1020 cells: 8 esc: 0 | r46-selftest-f29.py
```

This matters because `corpus/instruments/r45-routed-defects.py:293` grades a registry row by
`len(rows[0].strip().strip("|").split("|")) != 8`.

### F3 — do-nothing control: the append changes no existing gate verdict

Control = `git archive HEAD` export; treatment = the same export with my two blocks appended.
Baseline for the counter = the round-45 base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`
(exported to scratch).

`corpus/instruments/r45-routed-defects.py` (the gate that owns the SKILL.md registry's R3 limb):

```
=== CONTROL: r45-routed-defects, root=noappend, baseline=r45base ===
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=1 read=selftest-cases=61
limb R4 fixed=1 read=selftest-cases=27 replay=base_ok=2
limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
routed-defects total=5 fixed=5 unresolved=0 exit=0
=== TREATMENT: r45-routed-defects, root=appended, baseline=r45base ===
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=1 read=selftest-cases=61
limb R4 fixed=1 read=selftest-cases=27 replay=base_ok=2
limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
routed-defects total=5 fixed=5 unresolved=0 exit=0
```

Byte-identical verdicts. `corpus/instruments/anchorcheck.py` (control vs treatment, cwd = the tree
under test, so the base is the tree itself):

```
noappend   SKILL.md                         == SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
noappend   corpus/instruments/README.md     == corpus/instruments/README.md: 5 in-range cite instances, 0 bad; 5 distinct anchors; LOST-RECORDED=2 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=4
appended   SKILL.md                         == SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
appended   corpus/instruments/README.md     == corpus/instruments/README.md: 5 in-range cite instances, 0 bad; 5 distinct anchors; LOST-RECORDED=2 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=4
```

`0 bad` in both arms. `corpus/instruments/recheck-audit.py --root --quiet` is likewise identical:

```
control:    lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
treatment:  lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
```

And the R3 pinned-row bytes are untouched (I re-derived the counter's own `PINS` and hashed the
rows): `SKILL rows pinned: {'r44-frontier-count.py': True, 'r44-routed-defects.py': True,
'wave-registry.py': True} | README row pinned: True` in both arms.

`corpus/instruments/density.py SKILL.md` moves as expected for an appended block: 33 → 34 blocks,
839 → 865 path-citation instances, mean density 258.7 → 274.2. No density threshold exists in the
tool (`density.py` has no fail path; it only prints).

### F4 — every verdict-map clause in the rows is a re-run I performed

`corpus/instruments/r46-mutbat.py` (committed v1, sha256 `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`,
matching `.ufo/waves/round-46/attempt2/freeze.txt`):

- `--list` prints 41 mutant lines, 20 for c1 and 21 for c2, exit 0:
  `c1 M01-L1-target-24 | TARGET_GATED = 22 => TARGET_GATED = 24` … (measured).
- `--counter zzz` → `r46-mutbat.py: error: argument --counter: invalid choice: 'zzz' (choose from 'c1', 'c2', 'both')`, exit 2.
- `--counter f29` → `invalid choice: 'f29' (choose from 'c1', 'c2', 'both')`, exit 2. This is why my
  f29-gate row calls `--counter f29` **planned**, not present.
- `--selftest` → `error: unrecognized arguments: --selftest`, exit 2 — the instrument has no
  `--selftest` flag, so the row's self-test cell names the two counter selftests it drives instead.
- Missing `--root/--pure/--work` → `error: the following arguments are required: --root, --pure, --work`, exit 2.
- The drift guard is real: `apply_mutant` raises `SystemExit` when the old-substring does not occur
  exactly once (`corpus/instruments/r46-mutbat.py:116`), and `SystemExit` with a string message exits 1
  (measured on a stand-alone reproduction of the same call).
- The equivalent predicate is `mid in eq and os.path.isfile(eq[mid])`
  (`corpus/instruments/r46-mutbat.py:169`): the id must be a key of the `--equivalent` JSON map and the
  named proof path must exist. `os.path.isfile` on an empty file is `True`, so an empty proof file
  still satisfies the predicate — the row states the predicate as the code implements it and does not
  claim the proof is read.

`corpus/instruments/r46-f29-gate.py` (committed v1, sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`):

- At the base export `04af9bc9`: `f29-gate fixed=1/7 exit=1`, limb reads
  `H1 pass=0 read=rows=28 admitted=28 dup=0` … `H7 pass=1 read=census-rc=0 ok-line=1` — byte-identical to
  the committed receipt `.ufo/waves/round-46/attempt2/controls/f29-gate-at-base.txt`.
- At the live freeze tree: `f29-gate fixed=2/7 exit=1` (H4 and H7 green) — matching the claim's
  `freeze_tree_reading`.
- On a missing `--root`: `f29-gate fixed=0/7 exit=1 (root-missing)`, exit 1.
- `--selftest` → `error: unrecognized arguments: --selftest`, exit 2.
- The gate writes nothing: `grep -nE "open\([^)]*['\"][wa]|\.write\(|makedirs|mkdtemp|shutil\."` over
  the file returns no match, and `a.work` is never referenced — so `--work` is accepted and ignored.
  The row says exactly that.

The wave-1 selftest (draft, not committed at this writing):
`.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`,
sha256 `23b528a40e1d982820d360aea3cd12166a8b6ac07226e7567fd5abaa16f4435d`, 906 lines.

- Plain run: `selftest cases=30 failures=0`, exit 0, with
  `note provenance f29-defects.py sha256=2e95d4d4… matches` and
  `note provenance f29-fixture.py sha256=52ea9693… matches`.
- `--do-nothing-control`: 29 `FAIL` lines over 30 case lines, still `selftest cases=30 failures=0`,
  exit 0 — i.e. every red-expecting case is reported FAIL against the stub counter that reads green
  everywhere (`ctl junk`, `ctl fabricated`, all 17 defect cases and all 8 clause cases), and the
  `ctl positive` case stays `ok`. That is the do-nothing discrimination the row advertises.

Fixture discrimination for the gate (control trees built by the committed
`.ufo/waves/round-46/attempt2/controls/f29-fixture.py`):

```
positive    -> f29-gate fixed=7/7 exit=0
junk        -> f29-gate fixed=6/7 exit=1   (H5 red: spans=7 located=2 failed=5 cores=0/5)
fabricated  -> f29-gate fixed=6/7 exit=1   (H5 red: spans=7 located=5 failed=2 cores=4/5)
```

Each of the 17 defect trees the committed builder carries was run and each reads red on the limb
the receipt names (measured; e.g. `duprow` → `red=[H1] fixed=6/7`, `manws` → `red=[H4] fixed=6/7`,
`symlink` → `red=[H6,H7] fixed=5/7`).

### F5 — two defects in the committed round-46 control material, found by re-running it

These are **not** mine to fix (the controls are frozen at the freeze commit), and they do not
block my two appends, but the L1 and the canonical judge need them verbatim.

**(a) The R50 receipt's junk/fabricated readings do not reproduce against the committed bytes.**
`.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt:6-7` states:

> Positive tree reads `f29-gate fixed=7/7 exit=0`; junk tree `fixed=3/7` (H2/H5 red: 2/7 quotes
> located, 0/5 cores); fabricated tree `fixed=3/7` (5/7 located, 4/5 cores).

My re-run of the committed `f29-fixture.py` against the committed `r46-f29-gate.py` reads
`fixed=6/7` for both junk and fabricated, with **H5** red and **H2 green** — not `3/7` with H2 red:

```
=== junk ===
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1
```

The reason is visible in the committed fixture: its docstring says junk is "the positive tree with
the entry replaced by marker-only filler (no located quotes) — must NOT read 7/7 (H2/H5 red)", but the
committed `JUNK` constant (`f29-fixture.py:79-83`) is a set of *phrase substitutions* inside the real
entry, so the four sections, the table and the xrefs all survive and H2 stays green. The
`f29-fixture.py` docstring and its own `JUNK` constant disagree. The quote-locating numbers in the
receipt (2/7 located, 0/5 cores) do reproduce; only the H2 leg and the `3/7` total do not.

**(b) The committed defect builder is missing the receipt's `src0740` defect.** The receipt's
pairing table names 18 distinct defect names, but `f29-defects.py` carries 17 —
`grep -c 'src0740' f29-defects.py` → `0`, and
`python3 f29-defects.py --defect src0740 …` → `unknown defect src0740`, exit 2. The wave-1 selftest
compensates by building that case itself (`r46-selftest-f29.py:224-227` says so explicitly), but the
committed control builder alone cannot reproduce receipt pair 3. My `r46-selftest-f29.py` row records
this fact in its pinned-value cell rather than silently claiming 17 defect trees cover 18 receipt rows.

### F6 — the R50 receipt's per-defect base-limb column disagrees with the committed trees

The receipt's pairing table gives each defect a "base limb" and a "mutant limb". I ran the gate on
every defect tree the builder carries and compared. The receipt's limb attribution is not what the
committed bytes produce: e.g. receipt pair 5 `thinsection` says base limb `H2=1`, but the committed
`thinsection` tree reads `red=[H6] fixed=6/7` (`gate H6 pass=0 read=knowledge=66 entries=66
nested-md=66 base-intact=1 entry-bytes-ok=0 symlinks=0`); receipt pair 15 `fewspans` says base limb
`H5=0`, but the committed tree reads `red=[H2,H5] fixed=5/7`; receipt pair 18 `symlink` says base limb
`H7=0` while the committed tree reads `red=[H6,H7]`. Only some rows agree (e.g. `duprow` → `H1`,
`vjunk` → `H2`, `manws` → `H4`, `widespan` → `H5`). My rows do not restate the receipt's limb
attributions — they state only the gate's own output contract, which is what a registry row is for —
but the C2 kill rule's "no control grades 7/7" is still satisfied: every junk, fabricated and defect
tree I ran reads `< 7/7`.

## Limitations

- **Draft only, by design.** Nothing is applied to `SKILL.md` or `corpus/instruments/README.md`; the
  L1 appends the two blocks at integration. I did not commit, push, or run any mutating git/jj
  command.
- **The `r46-selftest-f29.py` row names a planned, not-yet-committed path.** The file exists only as
  the wave-1 executor draft
  `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`. My row names the
  planned committed path `corpus/instruments/r46-selftest-f29.py` and cites the draft path beside it;
  the selftest's own numbers (30 cases, failures=0) are labelled "measured on the wave-1 draft" so
  they are not mistaken for a committed-instrument measurement.
- **`--counter f29` does not exist yet.** The committed `r46-mutbat.py` rejects it with an argparse
  exit 2. My f29-gate row says the extension is **planned** and cites the measured rejection, so the
  row cannot be read as claiming a live capability. If wave 2 lands a different shape, the L1 must
  amend that cell.
- **The battery's full before-value replay did not finish in my time budget.** One mutant of
  `r46-mutbat.py --counter both` takes ≈25 minutes against the live tree (the c1 selftest baseline
  alone exceeds 15 minutes); the run reached `mutant=M01-L1-target-24 baseline_failures=0
  mutant_failures=26 verdict=caught` and I stopped it at the 25-minute mark. The before-values in my
  rows are therefore quoted from the **committed frozen receipt**
  `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (sha256
  `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`, `BATEXIT=1`), which is the
  pinned value the row is required to cite — not a re-run I completed. I did independently confirm the
  receipt's shape by running `--list` and by the single mutant above, whose printed line matches the
  receipt's first line exactly.
- **`r46-c1-gate.py` and `r46-c2-gate.py` were both re-run on the control and the treatment tree**
  (the two attempt-1 counters, which grade this round's claims):
  ```
  === r46-c1-gate (control) ===      gate L6 pass=1 read=mutants=46 survivors=none
                                      gate L7 pass=1 read=still-gated=22 changed=none
                                      c1-gate fixed=7/7 exit=0
  === r46-c1-gate (treatment) ===    gate L6 pass=1 read=mutants=46 survivors=none
                                      gate L7 pass=1 read=still-gated=22 changed=none
                                      c1-gate fixed=7/7 exit=0
  === r46-c2-gate (control) ===      gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
                                      gate G7 pass=1 read=census-rc=0 ok-line=1
                                      c2-gate fixed=7/7 exit=0
  === r46-c2-gate (treatment) ===    gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
                                      gate G7 pass=1 read=census-rc=0 ok-line=1
                                      c2-gate fixed=7/7 exit=0
  ```
  Byte-identical in both arms. Independently, `grep -c 'SKILL.md\|instruments/README.md'` is `0` in
  both counter sources and their input roots are `corpus/knowledge/*`, `corpus/source-snapshots/*`
  and `corpus/SOURCES.md` — neither reads the two files I append to.
  `corpus/instruments/r46-f29-gate.py` on the appended tree reads `f29-gate fixed=2/7 exit=1`, the
  same as on the live lane (the F29 entry has not landed), so the append is inert for it too.
- **Fixture-based numbers depend on the lane's current `corpus/knowledge/` contents.** The
  `f29-fixture.py` builder copies the real 65 base knowledge entries plus a synthetic entry; if a
  sibling seat's entry lands before integration, the fixture trees change and the `6/7` readings must
  be re-taken. The registry rows do not pin those readings — they pin the gate's *output contract*,
  which is stable.
- **`src0740` and the `3/7` junk/fabricated readings** (F5) are conflicts in frozen control material
  I cannot amend. They need an L1 erratum; my report carries them verbatim for the canonical judge.
- No tool was installed or upgraded for this seat, so there is no tooling line to record.

## Suggested L1 integration

1. Append `SKILL-append.md` to the END of `SKILL.md` (after `SKILL.md:1166`), preceded by one blank
   line. Append `README-append.md` to the END of `corpus/instruments/README.md` (after
   `corpus/instruments/README.md:1003`), preceded by one blank line.
2. Re-take the two fixture readings (`junk`, `fabricated`) after the wave-2 entry lands, and amend
   F5(a)/(b) as a logged erratum against `.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt`.
3. If wave 2 lands `r46-mutbat.py --counter f29` with a different flag shape than the wave-1 card
   states, amend the `r46-f29-gate.py` row's self-test cell and the `r46-mutbat.py` row's entry
   command; both cells currently describe the committed v1 and mark the extension as planned.
4. After landing, re-run `grep -c 'r46-mutbat' SKILL.md` (expect `>= 2`),
   `python3 corpus/instruments/r45-routed-defects.py --root <tip> --baseline <round-45 base>`
   (expect `fixed=5 unresolved=0 exit=0`) and `python3 corpus/instruments/anchorcheck.py SKILL.md`
   (expect `0 bad`).

## Artifacts

- Draft: `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/SKILL-append.md`
- Draft: `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/README-append.md`
- This report: `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.md`
- Receipts (copied out of scratch before it was removed):
  - `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/bytecheck-and-cells.txt`
    — the `grep -c 'r46-mutbat'` byte-check and the per-row cell counts.
  - `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/gate-control-vs-treatment.txt`
    — every gate's control-vs-treatment output.
  - `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/r50-receipt-vs-committed-bytes.txt`
    — the R50 receipt text verbatim beside my re-run of the committed control bytes (F5).
  - `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/f29-selftest-draft-run.txt`
    — the wave-1 selftest draft's plain run (`selftest cases=30 failures=0`).
  - `.ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/f29-selftest-draft-donothing-control.txt`
    — the same selftest under `--do-nothing-control` (29 FAIL lines over 30 cases).
- Scratch (removed on exit): `/fast/scratch/hyaku/kasegi-r46/R46bScribeSkillRegistry/`
