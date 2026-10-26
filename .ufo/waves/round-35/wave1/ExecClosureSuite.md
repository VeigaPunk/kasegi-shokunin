# ExecClosureSuite — D1–D7 closure suite (`corpus/instruments/r35-defect-closure.sh`)

Seat: ExecClosureSuite (leaf). Lane: `kasegi-shokunin`, round 35. Lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
Scope: C1's counter only — the committed suite that measures the seven round-34 verifier-routed defects
D1–D7 (`corpus/lessons/round-34-verifier-spotcheck.md` §6). I landed no fixed content: the SCORECARD
corrections (D1/D2), the SKILL registry rows (D3), the results provenance note (D4), the D5 erratum, the
L1Integration correction (D6), the QUALITY supersession rows (D7) and the whole `r35-fixtures/` tree are
other seats' bytes. No `git`/`jj` mutation was run.

## Report

### 1. Deliverable and digests

| path | sha256 | lines | mode |
|---|---|---|---|
| `corpus/instruments/r35-defect-closure.sh` | `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` | 834 | `-rwxr-xr-x` |

Read-only inputs consumed (not mine): `corpus/instruments/r35-fixtures/fixtures.json`
`b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113`, `…/README.md`
`c7261c745e60812824a430574b42766a1e3f2193fea30c29e9e866e6e3547e55` (the fixture seat revised its
README after my first read; the fixture trees themselves are unchanged — §10).

Provenance of the digest: `d7ad8438…` (773 lines) was measured by two reviewers with no blocking defect;
the next revision added the D5 `erratum-file` mutant that `RevSelftestFixtures` showed was missing,
honoured `--root` inside `--selftest` (so the green-path run needs no patched copy — `RevClosureSuite`
observation 2) and recorded the prose-placeholder limit in the header (`RevClosureSuite` observation 1),
giving `a4f80067…` (834 lines). That one carried a false statement in a comment — it said "sixteen
mutants in all" where the clause table has seventeen — caught by my own recount and corrected here
(`0ae4b48…`, same 834 lines). No check semantics changed in either revision. Counts measured on the
green tree, not asserted: `D1 3/3 D2 3/3 D3 2/2 D4 2/2 D5 3/3 D6 2/2 D7 2/2` = **17/17**.

No tool was installed or upgraded this seat (`pacman`, `uv`, `npm` untouched).

### 2. The seven checks (one function each; `check_d1` … `check_d7`)

Every check body opens by `cd`-ing into the root it measures —
`( cd "$root" || { printf 'root-unreadable'; exit 2; } …` — where `$root` defaults to the absolute
`LANE_ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin` declared at `r35-defect-closure.sh:88`, so
lane-relative reads happen only after `cd` to the lane root (or to an explicit `--root`). Each check
prints a compact `key=value` payload and exits 0 = closed, 1 = open, 2 = harness error (unreadable root).

| defect | clauses (payload keys) | closed means |
|---|---|---|
| D1 | `placeholders`, `lane-hash-markers`, `correction-c1c6a5f` | `placeholders=0`, `lane-hash-markers=0`, `correction-c1c6a5f>=1` |
| D2 | `erratum-row`, `erratum-mean`, `row-bytes` | each `>=1` |
| D3 | `registry-r-defect-closure`, `registry-kill-rule` | each `>=1` in `SKILL.md` |
| D4 | `tracked`, `provenance` | `tracked=1` (`git ls-files … \| wc -l`), `provenance=1` |
| D5 | `erratum-file`, `discriminating-invocation`, `per-id-occurrences` | `present`, `>=1`, `>=1` |
| D6 | `dead-seat-sentence`, `correction-round-35` | `=0`, `>=1` |
| D7 | `supersedes-R22`, `supersedes-R23` | each `>=1` |

**Seventeen clause mutants, one per clause.** Isolation is per clause: a mutant is credited only when the
check rejects it *and* every other clause of that check still reads closed — so the rejection is
attributable to the reopened clause. The single exception is D5's `-erratum-file` (the file removed,
which necessarily takes both statement clauses with it): it is a `cascade` mutant, credited on the
rejection naming `erratum-file=absent`, and its detail line carries `cascade=1`. That mutant exists
because `RevSelftestFixtures` correctly noted the clause was otherwise evidenced only by the base-tree
run; the gap is now inside `--selftest`.

Two literal notes the frozen claim forces:

- **D1 has a third clause** for the C1 kill rule's other marker spelling, `<LANE_HASH>`
  (`claims.json` → C1 `kill_rule`: "`<LANE_HASH>` still present in SCORECARD.md"). It reads 0 on base,
  live and every fixture, and has its own mutant. **L1 note:** it is a literal count, so any later edit
  that quotes the token in SCORECARD prose turns the gate red exactly as the kill rule says.
- **D2's "the stale row's own bytes untouched (diff shows 0 deletions)"** is byte survival of the row's
  opening — `grep -cE '^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 path-citation
  instances'` — not a `git diff --numstat` deletion count, which cannot run in a `git archive` export or
  in a fixture tree, i.e. in neither of the two places the claim requires the suite to run. A fix that
  rewrites the row in place drops the literal and fails; the append-only fix keeps it. Measured:
  `row-bytes=1` live, and the round-33 row (`mean 191.5, 24 blocks, 689 path-citation instances`) does
  not match, so the count is unique to the round-34 row.
- **Documented limit (header, `r35-defect-closure.sh` §"Documented limit").** D1 matches the two
  placeholder spellings the spot-check and this round's kill rule name literally. The other round-34
  placeholder was prose ("the L1 fills this line in the closing commit"); a literal matcher cannot cover
  prose placeholders without also matching legitimate prose that quotes them, so that spelling is
  measured (0 at base, 0 at tip) rather than asserted. This is the spelling-brittleness residue
  `RevClosureSuite` flagged; it is recorded in the instrument's header, not hidden.

### 3. Plain run — live lane (the gate as the L1 will run it)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && bash -n corpus/instruments/r35-defect-closure.sh
bash_n_exit=0
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
plain_exit=1
```

The three open limbs are not mine to close; each measured at its named location at this read:

```
$ grep -c -F 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md   -> 1
$ grep -c -F 'Correction (round 35)'             .ufo/waves/round-34/wave1/L1Integration.md   -> 0
$ grep -c -F 'supersedes R22' corpus/QUALITY.md ; grep -c -F 'supersedes R23' corpus/QUALITY.md -> 0 ; 0
$ git ls-files -- .ufo/waves/round-34/wave1-results.json | wc -l                             -> 0
```

- **D4** is a commit-order fact by construction: `git ls-files` reads the index and the provenance note
  already exists (`provenance=1`), so D4 closes on the L1's commit — which is the frozen counting
  command (`claims.json` → C1 `counting_commands[4]`).
- **D6** still carries the stale sentence at `L1Integration.md:30` and no `Correction (round 35)`.
- **D7** still carries 0 `supersedes R22` / `supersedes R23` rows.

### 4. Base tree — the failure direction

```
$ git archive 3266c9937b03062d9bbc2f436e20820115ed179c | tar -x -C /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite/base
$ bash corpus/instruments/r35-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite/base
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1
base_exit=1
```

`closed=0/7 exit=1` on the tree that still carries every defect — no check is vacuously green. Base
clause counts measured directly on the base blobs (`git show 3266c99:<path> | grep -c`): SCORECARD
`filled by the L1` 1, `c1c6a5f` 0, `round-34 depth:density row` 0, `201.2` 0, stale-row prefix 1;
SKILL `r-defect-closure` 0, `kill-rule-check` 0; QUALITY `supersedes R22` 0, `supersedes R23` 0;
L1Integration dead-seat 1, `Correction (round 35)` 0; `wave1-results.json` absent from the base tree.

### 5. All-fixed tree — the passing direction (`closed=7/7 exit=0`)

`r35-fixtures/clean/` carries the closed form of all seven limbs; materialized as its own worktree
(`cp -a clean/. $S/clean/ && ( cd $S/clean && git init -q && git add -A )`):

```
$ bash corpus/instruments/r35-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite/clean
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
clean_exit=0
```

`tracked=1` there is a real index read (no `.gitignore`, `git add -A` indexes the results file), which is
what `clean/` exists to prove; the D4 fixture does the opposite with a `.gitignore` naming that path.

### 6. `--selftest`, live lane (red for exactly D4/D6/D7)

```
$ KASEGI_SCRATCH=/fast/scratch/hyaku/kasegi-r35/ExecClosureSuite \
  bash corpus/instruments/r35-defect-closure.sh --selftest
selftest detail=D1 fixture reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0
selftest detail=D1 mutant=placeholders reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=3
selftest detail=D1 mutant=lane-hash-markers reason=placeholders=0,lane-hash-markers=1,correction-c1c6a5f=3
selftest detail=D1 mutant=correction-c1c6a5f reason=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=0
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D2 fixture reason=erratum-row=0,erratum-mean=0,row-bytes=1
selftest detail=D2 mutant=erratum-row reason=erratum-row=0,erratum-mean=1,row-bytes=1
selftest detail=D2 mutant=erratum-mean reason=erratum-row=1,erratum-mean=0,row-bytes=1
selftest detail=D2 mutant=row-bytes reason=erratum-row=1,erratum-mean=2,row-bytes=0
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D3 fixture reason=registry-r-defect-closure=0,registry-kill-rule=0
selftest detail=D3 mutant=registry-r-defect-closure reason=registry-r-defect-closure=0,registry-kill-rule=1
selftest detail=D3 mutant=registry-kill-rule reason=registry-r-defect-closure=1,registry-kill-rule=0
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D4 fixture reason=tracked=0,provenance=0
selftest detail=D4 mutant=tracked reason=tracked=0,provenance=1
selftest detail=D4 mutant=provenance reason=tracked=1,provenance=0
selftest case=D4 live=fail fixture=rejected mutants=2/2 others=6/6 verdict=fail
selftest detail=D4 live-reason=tracked=0,provenance=1
selftest detail=D5 fixture reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0
selftest detail=D5 mutant=erratum-file reason=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 cascade=1
selftest detail=D5 mutant=discriminating-invocation reason=erratum-file=present,discriminating-invocation=0,per-id-occurrences=5
selftest detail=D5 mutant=per-id-occurrences reason=erratum-file=present,discriminating-invocation=5,per-id-occurrences=0
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D6 fixture reason=dead-seat-sentence=1,correction-round-35=0
selftest detail=D6 mutant=dead-seat-sentence reason=dead-seat-sentence=2,correction-round-35=0 verdict=unexpected rc=1
selftest detail=D6 mutant=correction-round-35 reason=dead-seat-sentence=1,correction-round-35=0 verdict=unexpected rc=1
selftest case=D6 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest detail=D6 live-reason=dead-seat-sentence=1,correction-round-35=0
selftest detail=D7 fixture reason=supersedes-R22=0,supersedes-R23=0
selftest detail=D7 mutant=supersedes-R22 reason=supersedes-R22=0,supersedes-R23=0 verdict=unexpected rc=1
selftest detail=D7 mutant=supersedes-R23 reason=supersedes-R22=0,supersedes-R23=0 verdict=unexpected rc=1
selftest case=D7 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest detail=D7 live-reason=supersedes-R22=0,supersedes-R23=0
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest problem=self-report status=1
selftest_exit=1
```

Read this precisely. The policy is correct and the report is honest: D6 and D7's clause mutants read
`verdict=unexpected` only because the *other* clause of the same check is still open on the live bytes —
`isolate_ok` refuses to credit a rejection it cannot attribute to the reopened clause. On the all-fixed
tree (§7) the same mutants isolate. The three `verdict=fail` cases are exactly the three limbs other
seats and the L1 still own (§3). Both controls pass on live: `clean` 7/7, `two-defect/D1D2` failing
exactly D1+D2. `others=6/6` on every case is the cross-limb check (each `D<i>` fixture breaks one limb,
so the other six checks must pass on that same materialized tree).

### 7. `--selftest` on the all-fixed tree (`cases=7 failures=0`, exit 0) — no patched copy

```
$ KASEGI_SCRATCH=/fast/scratch/hyaku/kasegi-r35/ExecClosureSuite \
  bash corpus/instruments/r35-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite/clean --selftest
selftest detail=D1 fixture reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0
selftest detail=D1 mutant=placeholders reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=1
selftest detail=D1 mutant=lane-hash-markers reason=placeholders=0,lane-hash-markers=1,correction-c1c6a5f=1
selftest detail=D1 mutant=correction-c1c6a5f reason=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=0
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D2 fixture reason=erratum-row=0,erratum-mean=0,row-bytes=1
selftest detail=D2 mutant=erratum-row reason=erratum-row=0,erratum-mean=1,row-bytes=1
selftest detail=D2 mutant=erratum-mean reason=erratum-row=1,erratum-mean=0,row-bytes=1
selftest detail=D2 mutant=row-bytes reason=erratum-row=1,erratum-mean=1,row-bytes=0
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D3 fixture reason=registry-r-defect-closure=0,registry-kill-rule=0
selftest detail=D3 mutant=registry-r-defect-closure reason=registry-r-defect-closure=0,registry-kill-rule=1
selftest detail=D3 mutant=registry-kill-rule reason=registry-r-defect-closure=1,registry-kill-rule=0
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D4 fixture reason=tracked=0,provenance=0
selftest detail=D4 mutant=tracked reason=tracked=0,provenance=1
selftest detail=D4 mutant=provenance reason=tracked=1,provenance=0
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D5 fixture reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0
selftest detail=D5 mutant=erratum-file reason=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 cascade=1
selftest detail=D5 mutant=discriminating-invocation reason=erratum-file=present,discriminating-invocation=0,per-id-occurrences=1
selftest detail=D5 mutant=per-id-occurrences reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D6 fixture reason=dead-seat-sentence=1,correction-round-35=0
selftest detail=D6 mutant=dead-seat-sentence reason=dead-seat-sentence=1,correction-round-35=1
selftest detail=D6 mutant=correction-round-35 reason=dead-seat-sentence=0,correction-round-35=0
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D7 fixture reason=supersedes-R22=0,supersedes-R23=0
selftest detail=D7 mutant=supersedes-R22 reason=supersedes-R22=0,supersedes-R23=1
selftest detail=D7 mutant=supersedes-R23 reason=supersedes-R22=1,supersedes-R23=0
selftest case=D7 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
green_exit=0
```

All **17 clause mutants** are credited (16 isolated + the one `cascade`), all seven fixture rejections
name their own limb, both controls agree, and the judge accepts the report. `cases=7 failures=0` is
reachable on these bytes through the frozen CLI; it is withheld on the live tree only because three limbs
are not yet landed.

### 8. The do-nothing control is rejected (the discriminator)

```
$ bash .ufo/waves/round-35/c1-controls/fake-suite.sh
closed=7/7 exit=0
fake_plain_exit=0
$ bash .ufo/waves/round-35/c1-controls/fake-suite.sh --selftest
cases=7 failures=0
fake_selftest_exit=0
```

The fake prints exactly the two summary strings the claim asks for. It is rejected by the suite's own
judgement, not by a differently-shaped summary:

- `report_ok` requires **seven distinct** `selftest case=D1..D7` lines of the exact form
  `selftest case=D<i> live=pass fixture=rejected mutants=n/n others=6/6 verdict=pass`; for each id a
  `selftest detail=D<i> fixture reason=…` whose payload contains that limb's defect clause in its open
  form (`placeholders=[1-9]`, `erratum-row=0`, `registry-r-defect-closure=0`, `provenance=0`,
  `per-id-occurrences=0`, `dead-seat-sentence=[1-9]`, `supersedes-R22=0`); at least one mutant detail
  line per id; and the case line's `mutants=n/n` equal to that id's mutant detail-line count.
- `plain_report_ok` requires seven named `D<i> check=… open=[01]` lines and a summary agreeing with
  their open counts.
- `--selftest` re-proves the judgement on two machine-generated forgeries and on the control suite
  itself: `judge=forged-summary`, `judge=forged-caselines` (shape-complete except that its case lines
  claim `mutants=0/0` while detail lines exist — rejected by the count cross-check),
  `judge=short-report`, `judge=fake-suite`, `judge=fake-plain` all `rejected=1`;
  `judge=complete-report accepted=1`.
- Observed twice in §6: `selftest problem=self-report status=1` is that same guard refusing to bless an
  incomplete report. A `--selftest` body replaced by `printf 'selftest cases=7 failures=0'` exits 1 with
  `selftest problem=self-report cases=0 expected=7`; the plain equivalent exits 1 with
  `suite problem=self-report plain-lines=0 expected=7`. Independently confirmed by `RevClosureSuite`'s
  vacuous-echo battery (7/7 caught) and by `MutClosureSuite`'s baseline.

### 9. Read-only proof

```
$ B=$(git status --porcelain | sha256sum | cut -d' ' -f1)
$ bash corpus/instruments/r35-defect-closure.sh >/dev/null 2>&1; KASEGI_SCRATCH=$S bash corpus/instruments/r35-defect-closure.sh --selftest >/dev/null 2>&1
$ A=$(git status --porcelain | sha256sum | cut -d' ' -f1)
before=6f05e46ef2e66d5829888630a8407e738068e332647b45a8fe70d47a71c4371b
after=6f05e46ef2e66d5829888630a8407e738068e332647b45a8fe70d47a71c4371b
worktree_unchanged=1
```

The plain run writes nothing. Its only git invocation is `git ls-files` (index read; D4 cannot be counted
otherwise and that is the frozen counting command). `--selftest` writes only under
`${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}`, removes that tree on return (`trap 'rm -rf -- "$scratch"' RETURN`),
and runs `git init`/`git add` only inside it.

### 10. Fixtures consumed (owned by ExecSelftestFixtures)

Tree digest = `find <dir> -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum`:

| tree | sha256 |
|---|---|
| `r35-fixtures/D1` | `3ce10ceeaeff23b8321311326332d4ade731b13dfb10cb379f775a128acd8c19` |
| `r35-fixtures/D2` | `0dab48c03e0ec67c1b133a9ebeba5ab04f243882c3c72f5efa26ccd6be124207` |
| `r35-fixtures/D3` | `bfbe12cf708406b9e4f1c26c52e48cb39a7fd49830a8c265f0d97d96439d975c` |
| `r35-fixtures/D4` | `23de214a8e32195ad15ca3a01224c021c58d9bc9e2616f3dc290d18668c6a5db` |
| `r35-fixtures/D5` | `c0c3241d4d45adfdf3957bacf9e7768b72c3c8fda9ba514b416b40709a530cfd` |
| `r35-fixtures/D6` | `4b30fe352199a1675bc52f731c74667e8ab2c6f444e8df8266fb13fc7e27b7e6` |
| `r35-fixtures/D7` | `9947e5761e0959456e238666efd5562c77fa9004c37511a43a03a287e3e1e162` |
| `r35-fixtures/clean` | `35c233b11db004c1997d26f5850f871339d7f5224caf74b06ce6a04cd111f4b0` |
| `r35-fixtures/two-defect/D1D2` | `3621d0acb2eabbcc0af50149bfc89828bea66727616224320abb0aa3fe7d47f8` |

Cross-reference for the fixture seat (owner of that README): its Limits section still says "The
`erratum-file=absent` clause has no fixture and no mutant", which is stale on the mutant half — `D5` in
`mutant_specs` now carries `'-erratum-file' 'erratum-file' 'cascade'`, and §7 shows the credit line
(`mutant=erratum-file … cascade=1`, case `mutants=3/3`). The "no fixture" half remains true: no committed
fixture breaks that limb, and the absence direction is exercised by the base-tree run (§4) and now by the
cascading mutant. Reported to `RevClosureSuite` and to the README owner rather than edited here.

Protocol mismatches were resolved in writing rather than by widening a check: I sent the fixture seat the
exact grep and expected payload for each limb, and every check reads a path its own limb names
(`SCORECARD.md`, `SKILL.md`, `.ufo/waves/round-34/wave1-results.json` + `.provenance.md`,
`.ufo/waves/round-35/claims-erratum-d5.md`, `.ufo/waves/round-34/wave1/L1Integration.md`,
`corpus/QUALITY.md`). No check reads outside its limb, which is what makes `others=6/6` meaningful.

### 11. Findings for the L1

1. **The counter is final; three limbs of C1 are not.** On the bytes above, the plain run prints
   `closed=4/7 exit=1` and `--selftest` prints `selftest cases=7 failures=3`, naming D4, D6, D7. C1's
   predicate (`closed=7/7`, `cases=7 failures=0`) becomes measurable the moment (a) the D6 correction is
   appended to `.ufo/waves/round-34/wave1/L1Integration.md`, (b) the D7 supersession rows are appended to
   `corpus/QUALITY.md`, and (c) the L1 commits `.ufo/waves/round-34/wave1-results.json`. No byte of the
   suite needs to change for that: §5/§7 print `closed=7/7 exit=0` and `cases=7 failures=0` on a tree
   where those limbs are fixed.
2. **D4 red until the commit is correct-by-design, not a check bug.** `git ls-files` reads the index, so
   staging the results file is sufficient; run the gate after the `git add` if you want it green before
   the commit lands.
3. **The D1 kill-rule clause is a measured literal.** `grep -c '<LANE_HASH>' SCORECARD.md` is 0 at base
   and at tip. The D1 correction prose must not quote that token, or C1's own kill rule fires.
4. **D2's no-deletion limb is a byte-survival test, deliberately** (§2). If a judge insists on a literal
   `git diff --numstat` deletion count, that check cannot run in a git-free export or in a fixture and
   the selftest coverage of D2 drops to two of its three clauses.
5. **Two defects inside the counter were caught by reviewers after my first freeze and are fixed in these
   bytes.** (i) `report_ok`'s fixture-detail match was anchored at `reason=`, so D4's (`tracked=0,…`) and
   D5's (`erratum-file=present,…`) payloads failed it and the honest report was rejected once the tree
   went green — found by `ExecSelftestFixtures`, fixed to `reason=.*<clause>`. (ii) D5's `erratum-file`
   clause had no mutant — found by `RevSelftestFixtures`, fixed with the cascading mutant in §2. Both are
   reported here rather than silently absorbed: the first would have made C1 unmeasurable, the second
   made one clause's evidence live-run-only.
6. **`--selftest` now honours `--root`** (`RevClosureSuite` observation 2): the green-path run is the
   frozen CLI, not a `sed`-patched copy. The prose-placeholder residue (`RevClosureSuite` observation 1)
   is documented in the instrument header; it is a lesson/R1-class note, not a live blind spot
   (`filled by the L1` 0, `<LANE_HASH>` 0, "the L1 fills this line" 0 at tip).
7. **No tool installed; no external state touched.** All work under
   `/fast/scratch/hyaku/kasegi-r35/ExecClosureSuite/`, removed before this receipt (§12).

### 12. Scratch cleanup

Scratch root `/fast/scratch/hyaku/kasegi-r35/ExecClosureSuite/` held the base export (`base/`, 6930
files), the materialized `clean/` trees and the captured run logs. Ordering, stated precisely because
`CritBoundary-3` caught an earlier version of this paragraph claiming `scratch-absent` while a later
`--root clean --selftest` had re-created the tree (D4 ordering class, my mistake): the last
scratch-creating invocation was that green-path `--selftest`; cleanup and the `ls -d` below ran *after*
it; no scratch-creating mode (`--selftest`) has run since, and the two non-creating commands that
followed were the plain run (`closed=4/7 exit=1`, writes nothing — §9) and this receipt's own edit:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite; echo "rm_exit=$?"
rm_exit=0
$ ls -d /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite 2>/dev/null || echo scratch-absent
scratch-absent
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T06:47:16Z
```

The durable check is re-runnable and must print `scratch-absent`:
`ls -d /fast/scratch/hyaku/kasegi-r35/ExecClosureSuite 2>/dev/null || echo scratch-absent`.
No work tree of mine is left on disk.
