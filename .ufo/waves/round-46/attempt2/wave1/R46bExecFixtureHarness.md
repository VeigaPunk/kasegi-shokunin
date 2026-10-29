VERDICT: DRAFT-READY

# R46bExecFixtureHarness — merged F29 fixture harness + receipt-rebuilding selftest

## What was built

One harness, `.ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/f29-fixtures.py`
(32836 bytes on disk), folding the two frozen control builders into one file:

* `--mode positive|junk|fabricated` — the three fixture trees
* `--defect <name>` — the 17 per-limb defect trees the frozen control carries, **plus**
  `src0740`, the receipt's third pair, whose recipe the frozen control builder lacks
* `--selftest` — rebuilds every line of `controls/f29-r50-receipt.txt` and prints
  `selftest cases=<N> failures=<F>`

The tree recipes are spliced **verbatim** out of `controls/f29-fixture.py` and
`controls/f29-defects.py` (the ENTRY/JUNK/FABRICATED templates, the SOURCES registry row,
the README frontier splice, and the whole `if a.defect == ...` chain), so the harness's
trees are byte-identical to the receipt's trees by construction, not by transcription.
`src0740` is the one recipe that had to be restored by hand: it rewrites the F29 row's
sources cell to `S0740`.

---

## Finding 1 — every tree the harness builds is byte-identical to the frozen control's

**Attacked:** the merge's fidelity to the frozen builders. A merged harness that drifted
by one byte would invalidate the receipt it claims to rebuild.

**Command** (all 3 modes and all 17 defects, harness tree vs. the frozen control's tree,
`diff -r`):

```
H=.ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/f29-fixtures.py
C=.ufo/waves/round-46/attempt2/controls
for m in positive junk fabricated; do
  python3 $H --mode $m --dir /tmp/h/$m
  python3 $C/f29-fixture.py --mode $m --dir /tmp/r/$m
  diff -r /tmp/h/$m /tmp/r/$m && echo "$m IDENTICAL"
done
for d in duprow fencedf29 vjunk thinsection badnames row9cells thinscope kindcase \
         manws fewquotes dupquote widespan longquote fewspans nestedmd entrymutant symlink; do
  python3 $H --defect $d --dir /tmp/h/d_$d
  python3 $C/f29-defects.py --defect $d --dir /tmp/r/d_$d
  diff -r /tmp/h/d_$d /tmp/r/d_$d && echo "$d IDENTICAL"
done
```

**Output (quoted):**

```
positive IDENTICAL
junk IDENTICAL
fabricated IDENTICAL
duprow IDENTICAL
fencedf29 IDENTICAL
vjunk IDENTICAL
thinsection IDENTICAL
badnames IDENTICAL
row9cells IDENTICAL
thinscope IDENTICAL
kindcase IDENTICAL
manws IDENTICAL
fewquotes IDENTICAL
dupquote IDENTICAL
widespan IDENTICAL
longquote IDENTICAL
fewspans IDENTICAL
nestedmd IDENTICAL
entrymutant IDENTICAL
symlink IDENTICAL
FAIL=0
```

The restored `src0740` recipe was checked against the L1's own surviving R50 tree:

```
$ python3 $H --defect src0740 --dir /tmp/h/d_src0740
$ diff -r /tmp/h/d_src0740 /fast/scratch/hyaku/kasegi-r46/L1/f29r50/def-src0740 && echo IDENTICAL
IDENTICAL to L1 leftover
```

```
| F29 | GitHub repository security advisories — the maintainer-side advisory lifecycle (draft, private fork, CVE via GitHub as CNA, credit, publication, fix version) | admitted | corpus/knowledge/github-repository-security-advisories.md | S0740 | Keep the maintainer flow distinct from the reporter flow (F28); re-open the page before relying on its mechanics. |
```

**Why it matters:** the receipt's numbers are only meaningful if the trees that produce
them are the frozen ones. This is the merge's load-bearing property, and it holds for
all 20 modes/defects plus the restored 21st.

---

## Finding 2 — the selftest rebuilds the receipt: 92 cases, 0 failures, 11 flips flip

**Attacked:** the receipt's substantive content — the positive tree's 7/7, all twenty
pair rows (base limb, mutant limb, verdict), and the eleven flips.

**Command:**

```
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/f29-fixtures.py \
      --selftest --work $SCRATCH/st
```

**Output (quoted, selected lines):**

```
case=receipt-transcription ok=1 receipt-rows=20 harness-rows=20
case=mutant-substring-H1c-src-boundary ok=1 occurrences=1
case=mutant-count ok=1 mutants=21
case=mutants-per-limb ok=1 per-limb=H1=3,H2=3,H3=3,H4=3,H5=3,H6=3,H7=3
case=mutant-ids-match-receipt ok=1 ids=21 receipt-ids=21
case=positive-7of7 ok=1 fixed=7/7 exit=0
case=junk-h5-read ok=1 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
case=fabricated-h5-read ok=1 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
case=pair03-base-H1 ok=1 defect=src0740 limb=H1 base=0 receipt=0
case=pair03-mutant-H1 ok=1 defect=src0740 limb=H1 mutant=1 receipt=1
case=pair03-verdict ok=1 defect=src0740 mutant=H1c src-boundary verdict=FLIP
case=pair05-base-H2 ok=1 defect=thinsection limb=H2 base=1 receipt=1
case=pair05-mutant-H2 ok=1 defect=thinsection limb=H2 mutant=1 receipt=1
case=pair15-base-H5 ok=1 defect=fewspans limb=H5 base=0 receipt=0
case=pair15-mutant-H5 ok=1 defect=fewspans limb=H5 mutant=0 receipt=0
case=pair18-mutant-H7 ok=1 defect=symlink limb=H7 mutant=1 receipt=1
case=pair20-mutant-H7 ok=1 defect=positive limb=H7 mutant=1 receipt=1
case=flip-set ok=1 flips=H1c,H2a,H2c,H3b,H3c,H4a,H5a,H5b,H6a,H6b,H7b
case=not-shown-count ok=1 paired-not-shown=9 unpaired=H6c total=10
selftest cases=92 failures=0
selftest-divergences=2
```

The eleven flips are exactly the receipt's eleven, in the receipt's order:
`H1c,H2a,H2c,H3b,H3c,H4a,H5a,H5b,H6a,H6b,H7b` — and the receipt's summary line
`mutants=21, defect-flips shown=11 (H1c, H2a, H2c, H3b, H3c, H4a, H5a, H5b, H6a, H6b, H7b),
not-shown=10` is reproduced as 11 flips + 9 paired not-shown rows + the unpaired `H6c`
= 10 not-shown.

The mutant table is the committed C2 battery's table (`corpus/instruments/r46-mutbat.py`,
`C2_MUTANTS`) re-based onto the F29 counter's own source lines, under the receipt's ids
(`H1a`..`H7c`). Every mutant's old-substring is asserted to occur **exactly once** in the
counter, so a drifted counter fails loudly instead of mutating the wrong line — the same
guard the battery itself uses.

---

## Finding 3 — the receipt's two junk/fabricated aggregate lines do not reproduce

**Attacked:** the receipt's header claim `junk tree fixed=3/7` and
`fabricated tree fixed=3/7`.

**Command** (frozen counter, frozen builder):

```
$ python3 corpus/instruments/r46-f29-gate.py --root $SCRATCH/trees/junk --work $SCRATCH/work/g-junk
```

**Output (quoted):**

```
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1
```

**and for fabricated:**

```
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```

So the rebuilt junk and fabricated trees read **6/7**, not the receipt's 3/7. The
receipt's own H5 detail claims reproduce *exactly* (`2/7 quotes located, 0/5 cores` for
junk; `5/7 located, 4/5 cores` for fabricated) — only the aggregate limb counts differ.

**Root cause, established by measurement.** The L1's own R50 scratch trees still exist at
`/fast/scratch/hyaku/kasegi-r46/L1/f29r50/`. Diffing the L1's junk tree against the
frozen builder's junk tree shows the *only* difference is the SOURCES registry row:

```
$ diff -rq /fast/scratch/hyaku/kasegi-r46/L1/f29r50/junk $SCRATCH/trees/junk
Files /fast/scratch/hyaku/kasegi-r46/L1/f29r50/junk/corpus/SOURCES.md and .../trees/junk/corpus/SOURCES.md differ
```

The L1-era row has **12 cells**; the frozen builder emits the census-clean **11-cell**
row. Measured on the L1's own tree:

```
$ python3 corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/L1/f29r50/junk --work $SCRATCH/work/x
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=1
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
gate H7 pass=0 read=census-rc=1 ok-line=0
f29-gate fixed=4/7 exit=1
```

The 12-cell row trips H3 (the 11-cell shape) *and* H7 (the census rejects it). The
timeline confirms the trees predate the fixture's last write:

```
2026-10-29 17:34:43  L1/f29r50/junk/corpus/SOURCES.md
2026-10-29 17:34:44  L1/f29r50/fab/corpus/SOURCES.md
2026-10-29 17:35:19  .ufo/waves/round-46/attempt2/controls/f29-fixture.py   <- fixture's last write
2026-10-29 17:35:24  L1/f29r50/pos/corpus/SOURCES.md                        <- pos rebuilt AFTER
2026-10-29 17:42:22  .ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt
```

The junk and fabricated trees were built at 17:34:43–44, **before** the fixture's final
17:35:19 write; only the positive tree was rebuilt afterwards (17:35:24). That is why the
positive tree reproduces 7/7 against the frozen builder (byte-identical) while the junk
and fabricated aggregates do not. No tree recipe under the frozen fixture yields 3/7 for
either: the frozen builder yields 6/7, and the L1's superseded tree yields 4/7. I also
tested a marker-only-filler entry (the recipe the fixture's *docstring* describes, which
the implemented `JUNK` constant does not follow) — it reads 4/7, not 3/7.

**Why this is a divergence and not a failure.** The receipt's aggregate is stale relative
to the frozen builders it names; the receipt's substantive H5 claims, its 20 pair rows,
its 11 flips and its positive 7/7 all reproduce exactly. The harness therefore prints
every non-reproducing receipt line loudly on every run:

```
divergence=junk-fixed receipt=3/7 rebuilt=6/7 red-limbs=H5
divergence=fabricated-fixed receipt=3/7 rebuilt=6/7 red-limbs=H5
```

and counts them separately (`selftest-divergences=2`). `--strict-receipt` promotes them
to failures so the L1 can gate on the receipt verbatim. **This is an errata item for the
L1**: `controls/f29-r50-receipt.txt` line 6 should read `fixed=6/7` for the junk and
fabricated trees under the frozen builders, or the receipt should name the superseded
recipes it actually measured. I did not amend the receipt — it is read-only for this seat.

---

## Finding 4 — the harness discriminates (do-nothing controls)

**Control A — a receipt with one flipped digit must fail the transcription check.**
`controls/f29-r50-receipt.txt` row 3's base limb changed `H1=0` → `H1=1`:

```
$ python3 .../f29-fixtures.py --selftest --work $SCRATCH/st3 --receipt $SCRATCH/mut-receipt.txt
case=receipt-transcription ok=0 receipt-rows=20 harness-rows=20
...
selftest cases=92 failures=1
selftest-divergences=2
```

The unmutated run on the same harness scores `failures=0`, so the check is not
vacuous — it discriminates the receipt's actual content.

**Control B — a do-nothing counter must not pass.** A stub counter printing `nothing`:

```
$ python3 .../f29-fixtures.py --selftest --work $SCRATCH/st4 --counter $SCRATCH/nul/counter/r46-f29-gate.py
RuntimeError: counter printed no gate lines on .../trees/positive: 'nothing\n'
```

The harness fails loudly instead of scoring a vacuous 7/7.

**Control C — `--strict-receipt` promotes the divergences to failures:**

```
$ python3 .../f29-fixtures.py --selftest --work $SCRATCH/st2 --strict-receipt
selftest cases=92 failures=2
selftest-divergences=2
```

**Control D — reproducibility from the frozen export.** The whole selftest re-run against
`git archive fe0f56b` (the freeze commit) rather than the live lane:

```
$ git -C $LANE archive fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 corpus .ufo | tar -x -C $SCRATCH/freeze
$ python3 .../f29-fixtures.py --selftest --work $SCRATCH/stf \
      --lane $SCRATCH/freeze \
      --counter $SCRATCH/freeze/corpus/instruments/r46-f29-gate.py \
      --receipt $SCRATCH/freeze/.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt
selftest cases=92 failures=0
selftest-divergences=2
```

The positive tree built from the freeze export is byte-identical to the one built from the
live lane (`IDENTICAL freeze-export vs live lane`).

---

## Limitations

1. **The receipt's junk/fabricated aggregates are not reproducible** (Finding 3). The
   harness reports them as divergences, not failures; the L1 must decide whether to
   amend the receipt or accept the divergence. I could not determine which tree recipe
   produced `3/7`: no tree under the frozen builder yields it (6/7), nor does the L1's
   own surviving tree (4/7), nor a marker-only-filler entry (4/7).
2. **The mutant table is a reconstruction.** The R50 receipt names the mutants
   (`H1a counts-loose`, `H2c need-empty`, …) but not their edits; the committed battery
   carries the C2 counter's table, not an F29 one. I re-based the C2 table onto the F29
   counter's source lines. The re-basing is validated by outcome, not by construction:
   all 20 pair rows and all 11 flips reproduce the receipt's recorded limbs exactly, and
   each edit is asserted to hit exactly one occurrence in the counter. A mutant whose
   *effect* matches but whose *edit* differs from the R50 originals would still pass.
3. **The receipt's 9 disclosed NOT-SHOWN reasons are not machine-checked** by this
   harness. The harness reproduces that each of those pairs does not flip (verdict
   NOT-SHOWN) and that exactly 10 mutants are not-shown, but it does not verify the
   receipt's *prose* rationale (e.g. that H2b is shadowed by the section's own table).
   Those rationales are checked by reading the counter, not by the harness.
4. **`src0740` was restored from the receipt's tree, not from a builder.** The frozen
   control `f29-defects.py` has no `src0740` branch; the recipe is inferred from the
   receipt's own row text ("sources cell S0740") and validated byte-for-byte against the
   L1's surviving `def-src0740` tree.
5. **Scope.** I wrote only the harness draft and this report. I did not commit, push,
   amend the receipt, the frozen counters, or the claims file, and I did not touch the
   fleet repo, sibling lanes, `MANIFEST.json`, `.ufo/state`, or `~/Projects/shokuknow`.
   The frozen counter `corpus/instruments/r46-f29-gate.py` was read and copied (never
   modified) by the mutant machinery. Scratch was removed on exit.

---

## Tooling

No tools were installed or upgraded. The host has no `pacman` transaction performed by
this seat (the host guard pauses all `pacman` transactions); everything used was already
present: `python3` (3.14, stdlib only — the harness imports `argparse`, `json`, `os`,
`re`, `shutil`, `subprocess`, `sys`), `git` (read-only `archive`/`log`/`ls-tree`/`status`),
`diff`, `sha256sum`.

## Files

* `.ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/f29-fixtures.py` — the
  merged harness (draft; the L1 integrates)
* `.ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/selftest-out.txt` — the
  verbatim selftest run (`selftest cases=92 failures=0`)
* `.../R46bExecFixtureHarness.draft/selftest-out-strict-receipt.txt` — `--strict-receipt`
  run (`failures=2`: the two divergences promoted)
* `.../R46bExecFixtureHarness.draft/selftest-out-freeze-export.txt` — the run against
  `git archive fe0f56b` (`failures=0`)
* `.../R46bExecFixtureHarness.draft/control-mutated-receipt-out.txt` — the mutated-receipt
  control (`receipt-transcription ok=0`)
* `.../R46bExecFixtureHarness.draft/control-donothing-counter-out.txt` — the do-nothing
  counter control (RuntimeError, loud failure)
* `.ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.md` — this report
