VERDICT: DRAFT-READY

Seat `R46bScribeLesson` (round 46 attempt 2, kasegi lane) — draft only; no commits, no pushes, no
mutating git/jj call, no writes outside this seat's draft directory and this Report file.

## What was built

Three draft files in
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeLesson.draft/`
(the L1 integrates them into `corpus/lessons/round-46.md` and into the landing commits):

1. `attempt2-lesson-section.md` — the append-only `## Attempt 2 (2026-10-29, L1 KasegiR46)` section
   skeleton: C1/C2 one-liners, the frozen-counter lineage table, the frozen before-readings, and the
   `## Mistakes` starter table with M46-4 (mutation coverage shipped unmeasured) and M46-5 (the ten
   f29-gate mutants the gate level cannot isolate).
2. `gate-block.md` — the `## Gate` block for S074: URL, access date 2026-10-29, the nine located quotes
   (one per frozen core, each ≤ 25 words, each verified on its anchor line), the F29 frontier row and
   the S074 SOURCES row, and three reject/flip candidates with reason + flip condition.
3. `status-recheck-usedby.md` — the `## Status, recheck and used-by changes (old → new)` section with
   the registry/README diffs (additive only), the per-cell statement, the census coupling and the
   capture-binding before/after.
4. `evidence.md` — the verbatim command/output transcript behind every claim above.

## Findings (each: what was attacked or built, the command, the printed output)

### F1 — the nine quotes land on their anchor lines (built: the Gate quote block)

`sed -n '<anchor>p' corpus/source-snapshots/round-46-a2/S074.txt` and a substring check of the
manifest's quote records against those lines:

```
Q1 anchor=10 substring=True words=19 <=25=True
Q2 anchor=13 substring=True words=11 <=25=True
Q3 anchor=17 substring=True words=12 <=25=True
Q4 anchor=24 substring=True words=15 <=25=True
Q5 anchor=25 substring=True words=8 <=25=True
Q6 anchor=25 substring=True words=11 <=25=True
Q7 anchor=26 substring=True words=14 <=25=True
Q8 anchor=31 substring=True words=22 <=25=True
Q9 anchor=38 substring=True words=15 <=25=True
```

`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074`
prints `S074:sha256 OK` and nine `S074:Qn OK occurrences=1 anchor=N-ok` lines, `RC=0`. All five frozen
cores are inside the quoted text (`Q1@10`, `Q2@13`, `Q4@24`, `Q5@25`, `Q9@38`); 9 quotes, 9 distinct
texts, 8 distinct anchors. Capture digest `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`,
42 lines, 7087 bytes — matches `freeze.txt`.

### F2 — the frozen-counter lineage: v1.2 counters UNCHANGED this round

`git diff --stat 04af9bc9 fe0f56b7 -- <the six instrument paths>` prints only

```
 corpus/instruments/r46-f29-gate.py | 367 +++++++++++++++++++++++++++++++++++++
 corpus/instruments/r46-mutbat.py   | 184 +++++++++++++++++++
 2 files changed, 551 insertions(+)
```

and the per-path digests are identical base→freeze for `r46-c1-gate.py` (`95f2eb79…`),
`r46-c2-gate.py` (`647bd5b7…`), `r46-counters-selftest-c1.py` (`8b17164a…`),
`r46-counters-selftest-c2.py` (`ff7104cf…`); `r46-mutbat.py` (`e3b0c442…` = absent at base →
`f7a7cdfa…`) and `r46-f29-gate.py` (`e3b0c442…` → `a1091e24…`) are new at the freeze. Both new digests
match `freeze.txt`. The counters' docstring line 2 reads "v1.2 (hardened after the wave-1 and wave-2
falsification; errata E1 and E2, see .ufo/waves/round-46/counter-errata.md)". The attempt-1 errata file
is `.ufo/waves/round-46/counter-errata.md`. The **attempt-2 errata file exists** at
`.ufo/waves/round-46/attempt2/counter-errata.md` (written during this wave, frozen at `fe0f56b7`, same
claims sha256 `ca73279f…`): it classifies the round's changes as an erratum, not a changed rule, and
logs **E1** the battery `v1 → v1.1` extension (`F29_MUTANTS` + `--counter f29`; the c1/c2 predicate is
untouched so the before-value stays reproducible under v1 bytes), **E2** the two selftest extensions
(baselines stay `failures=0`; each new dedicated case must fail under its targeted mutant), and
**E3 — CONDITIONAL** a `r46-c2-gate.py` `v1.2 → v1.3` ledger exemption that lands only if the wave's
own verification succeeds, otherwise E3 is struck and the `considerthese` ledger append is deferred
again. Consequence for the lesson text: "v1.2 counters UNCHANGED this round" holds for the wave's seats
and for the freeze, but the L1's landed lineage table must record the c2 counter as v1.3 **if** E3 lands,
with the erratum pointer — never as a silent change.

### F3 — M46-4 mined from the frozen battery receipt

`controls/mutbat-before.txt` (sha256 `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`)
ends with

```
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
BATEXIT=1
```

with `verdict=uncaught` lines for M06/M07/M13/M14/M18/M19/M20 (c1) and G1c/G2a/G2b/G2c/G3a/G4b/G5c/
G6a/G6b/G6c/G7a/G7b/G7c (c2). Against `controls/selftest-baselines.txt`
(`selftest cases=76 failures=0`, `selftest cases=137 failures=0`) this is the mined mistake: the
case-count baseline never exercised those clauses. M46-5 is mined from
`controls/f29-r50-receipt.txt` (21 mutants, `defect-flips shown=11`, `not-shown=10`, disclosures (a)-(f)).

### F4 — the draft admit rows move the gate limbs they are supposed to move (built)

On a scratch export of the freeze commit (`git archive fe0f56b7 corpus | tar -x -C <scratch>`) with the
two draft rows inserted and a stub entry file:

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=4/7 exit=1
```

Do-nothing controls on the same export: without the rows `f29-gate fixed=2/7 exit=1`
(`H1 pass=0 read=rows=28 admitted=28 dup=0`, `H3 pass=0 read=row-S074=absent-… hits=0`); with the S074
row but no entry file `H3 pass=0 read=bad=used-by` and `H7 pass=0 read=census-rc=1 ok-line=0`.
The base export `04af9bc9` reads `f29-gate fixed=1/7 exit=1`, reproducing
`controls/f29-gate-at-base.txt`. The three red limbs (H2/H5/H6) are the real entry's work, not the rows'.

### F5 — the census couples the row and the entry (new finding for the landing)

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <tree>/corpus/SOURCES.md`
on the tree carrying the S074 row but not the entry file prints

```
file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
   (exit 1)
```

and exits 0 once the entry file is present (same three `W04` warnings as
`controls/sources-census-before.txt`). So a row-only landing makes the C2 counter's H7 limb red: the row
and the entry must land in the same commit.

### F6 — capture binding flips with the row

`python3 corpus/instruments/capture-binding-check.py --root .` at the tip prints
`FAIL rule=no-row record=S074 dir=round-46-a2` and `records=61 bound=60 unbound=1`; on the scratch tree
with the draft row and entry it prints `records=61 bound=61 unbound=0` — the attempt-1 S073 precedent.

### F7 — the registry/README diffs are additive only

`diff <(git show 04af9bc9:corpus/SOURCES.md) <scratch copy with the draft row>` prints `79a80` with one
added line and zero removed lines; the same diff on `corpus/README.md` prints `668a669,674` (the appended
section, header, separator and the F29 row), again with zero removed lines.

### F8 — base counts for the after-table

On the freeze export (equal to the base for these files): frontier rows 28, SOURCES registry rows 73,
knowledge entries 65, absence sweep 2 files (`corpus/knowledge/github-private-vulnerability-reporting.md`,
`corpus/SOURCES.md`). These are the "before" side of the after-table in the draft.

### F9 — the claims file has no candidates list (deviation, stated)

`grep -n -i 'candidat' .ufo/waves/round-46/attempt2/claims.json` prints nothing; the file's top-level keys
are `schema, lane, round, attempt, author, base, note, claims, sourced_claim, frontier_step`. The reject/
flip candidates in `gate-block.md` are therefore reconstructed from the lane's own corpus evidence
(README rows F07 and F28, SOURCES rows S068 and S073) and attempt 1's `## Gate` section, and the draft
says so explicitly rather than attributing them to the claims file.

### F10 — the attempt-2 errata file appeared during the wave and pins the lineage

`.ufo/waves/round-46/attempt2/counter-errata.md` (untracked at the time of reading, written by another
seat of this wave) states: "`claims.json` is byte-identical at the tip … No claim sentence, before-value,
after-value, target or kill rule was edited", classifies the round's changes as "Erratum, not a changed
rule", and logs E1 (battery `v1 → v1.1`: `F29_MUTANTS` + `--counter f29`), E2 (the selftest extensions)
and E3 (a CONDITIONAL `r46-c2-gate.py` `v1.2 → v1.3` ledger exemption). The draft's lineage section
points at that file by name and states the conditional.

## Limitations

- Draft only. Nothing here is committed; the L1 owns the committed bytes, the row wording and the entry.
- The entry file `corpus/knowledge/github-repository-security-advisories.md` does not exist at draft time,
  so gate limbs H2, H5 and H6 could only be read red (the stub entry used in the scratch tree exercises
  H3's `used-by` check but is not a real entry). No claim is made about the final `fixed=7/7`.
- The mutation battery was not re-run by this seat: `r46-mutbat.py` needs the wave's extended selftests,
  which do not exist yet. The before-value was read from the frozen receipt and its digest re-verified
  (`sha256sum` = `13c21fcd…`), not re-derived by a run.
- The live page was not re-fetched (live-target testing is refused; this corpus is documentation only).
  The quotes are verified against the frozen capture `S074.txt` and its manifest, whose sha256 matches the
  freeze record.
- The "expected after" column of the after-table is an expectation, not a measurement.
- Base counts were taken from the freeze export rather than from a separate base export; the two files are
  byte-identical for `corpus/README.md`, `corpus/SOURCES.md` and `corpus/knowledge/` (the freeze adds only
  the two new instrument files and the `round-46-a2` snapshot directory).
- Tooling: no package was installed or upgraded for this seat — the task needed only `git`, `sed`, `python3`
  and `bash`, all present. No `pacman`, `uv tool`, `cargo` or `npm` transaction was run.
- Moving target: wave artefacts changed while this seat worked (the attempt-2 `counter-errata.md`
  appeared, `attempt2/wave1/` and `attempt2/wave2/` are being written). The lineage text is written
  against the freeze `fe0f56b7` and against the errata file as read; the L1 re-reads both at integration.
- Scratch: `/fast/scratch/hyaku/kasegi-r46/R46bScribeLesson/` was removed after the receipts were copied
  into `evidence.md`.
