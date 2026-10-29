VERDICT: DRAFT-READY

Scope: LOG.md scribe (seat R46bScribeLog). Deliverable: `.ufo/waves/round-46/attempt2/wave1/R46bScribeLog.draft/log.md` — the `## Round 46 (attempt 2) — L1 \`KasegiR46\`` entry, in the shape of the attempt-1 entry at `LOG.md:2012-2020`. It is a **draft**: the L1 fills the `AT-FREEZE` / `AT-TIP` / `AT-W1-*` / `AT-COUNTERS` / `AT-W2-*` / `AT-MEASURE` slots and the wave-1 findings. Nothing was committed, pushed, or mutated in git; no shared production file was touched; the draft is the only file this seat wrote outside its own scratch.

Two findings below change what the L1's final measurement can claim. Both are re-run evidence, and the second is a **do-nothing control that inverts**.

## Findings

### F1. The attempt-1 counters are do-nothing controls on this round's tree — a *correct* attempt-2 landing turns them RED

**Attacked:** `corpus/instruments/r46-c1-gate.py` and `corpus/instruments/r46-c2-gate.py` (attempt-1's claim counters, which the attempt-2 `final-measure.sh` runs as the "prior-attempt instruments on the same exports (no-harm)" section).

Command (base export of `04af9bc9…` at `$S`, freeze export at `$S/freeze`):

```
python3 -B corpus/instruments/r46-c2-gate.py --root "$S"
```
Output:
```
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1 symlinks=0
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```
**`r46-c2-gate.py` reads `fixed=7/7 exit=0` (fully GREEN) on an untouched attempt-2 base tree.** It cannot be evidence of attempt-2's C2: attempt-1's F28 entry and `S073` row already landed in the attempt-2 base.

```
python3 -B corpus/instruments/r46-c1-gate.py --root "$S" --baseline "$S" --work "$S/w-dn1"
```
Output:
```
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=65
gate L2 pass=0 read=base-gated=22 regrounded=0 
gate L3 pass=0 read=recheck-lines-exact=0
gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
gate L5 pass=0 read=append-only-restoration-kept=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=2/7 exit=1
```
The attempt-1 c1-gate is red at the attempt-2 base for a structural reason: L2 wants the *re-grounded* set `gated(BASE) - gated(TREE)` to be non-empty, and attempt-1's re-grounds are already in the attempt-2 base, so the set is empty (`regrounded=0`). The same counter reads `fixed=7/7 exit=0` only against the **attempt-1** base `914ca0b…` — verified: `python3 -B corpus/instruments/r46-c1-gate.py --root "$S/a1tip" --baseline "$S/a1base"` → `c1-gate fixed=7/7 exit=0`.

Now the **projection** of this round's landing (I built it in scratch: the freeze export + the frozen fixture's F29 README row + the frozen fixture's `ENTRY` body + the F29 entry file → 29 frontier rows, 66 knowledge files):

```
python3 -B corpus/instruments/r46-c2-gate.py --root "$S/proj-tip"
```
Output:
```
gate G1 pass=0 read=rows=29 admitted=29 dup=0
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=5/7 exit=1
```
and `python3 -B corpus/instruments/r46-c1-gate.py --root "$S/proj-tip" --baseline "$S"` → `c1-gate fixed=2/7 exit=1`.

**Discrimination:** the attempt-1 counters hard-code attempt-1's targets — `r46-c2-gate.py:178` `if len(rows) != 28 or adm != 28` and `:347` `len(names) == 65 and len(everything) == 65 and nested == 65`, and G3 pins `S073` (`:158` `f27 = [r for r in rows if r[0] == "F28"]`). A correct attempt-2 landing (29 rows, 66 entries) therefore reads `c2-gate fixed=5/7 exit=1` on the tip. Consequences the L1 must record in the final measurement: a green `c2-gate` on the tip is **not** evidence of the F29 admission (it is green before the round starts), and a red `c1-gate`/`c2-gate` on the tip is **not** evidence of a regression (it is the expected reading of a correct landing). Only the new `r46-f29-gate.py` and the battery discriminate this round's two claims. This is the attempt-1 M46-1 ("vacuous counters") class reappearing one level up: the no-harm section of `attempt2/controls/final-measure.sh` currently reads as if the attempt-1 counters were a pass/fail signal for attempt 2.

### F2. The frozen R50 receipt's own numbers disagree with each other, and its junk-control readings do not reproduce

**Attacked:** `.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt` (committed at the freeze `fe0f56b…`, cited by the C2 claim's after-sentence).

Command (parse the receipt):
```
python3 - <<'EOF'   # count the receipt's pairing rows and verdicts
rows=[l for l in open('f29-r50-receipt.txt') if re.match(r'^\| \d+ \|', l)]
EOF
```
Output:
```
table rows: 20
FLIP rows: 11
NOT-SHOWN rows: 9
header says: ## Mutants defined: 21 (3 per limb H1-H7)
result says: Result: mutants=21, defect-flips shown=11 (H1c, H2a, H2c, H3b, H3c, H4a, H5a, H5b, H6a, H6b, H7b),
```
Three different counts for one mutant set: the header says 21, the `Result:` line says `mutants=21 … not-shown=10`, and the table itself carries **20** rows (11 FLIP + 9 NOT-SHOWN) with **20** distinct mutant ids. Per-limb: H1/H2/H3/H4/H5/H7 carry three mutants each, **H6 carries only two** (`H6a`, `H6b`) — `H6c` has no row and no id anywhere in the receipt. The "3 per limb H1-H7" claim and the "21" total are both wrong for the table as committed.

The junk controls do not reproduce either. The receipt states `junk tree fixed=3/7` and `fabricated tree fixed=3/7`. I rebuilt both from the **frozen** fixture (`.ufo/waves/round-46/attempt2/controls/f29-fixture.py`) and ran the **frozen** gate:

```
python3 -B .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive   --dir "$S/fix-positive"
python3 -B .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode junk        --dir "$S/fix-junk"
python3 -B .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode fabricated --dir "$S/fix-fabricated"
python3 -B corpus/instruments/r46-f29-gate.py --root "$S/fix-$M"
```
Output:
```
=== f29-gate on positive tree ===
f29-gate fixed=7/7 exit=0
=== f29-gate on junk tree ===
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1
=== f29-gate on fabricated tree ===
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```
The positive tree reproduces `7/7`; both junk controls read **`6/7`**, not `3/7`. I also rebuilt the junk and fabricated trees with `--lane "$S/freeze"` (the freeze export as the source lane) and got the same `6/7`. The receipt's per-limb read strings (`2/7 quotes located, 0/5 cores` and `5/7 located, 4/5 cores`) match my run exactly, so the receipt's *defect* observations are right and its *totals* are not. The receipt describes a different gate revision than the one frozen at `fe0f56b…`.

**Discrimination:** the receipt is a committed frozen artifact and the C2 claim's after-sentence leans on it ("the R50 pre-freeze mutant receipt controls/f29-r50-receipt.txt (21 mutants, 11 defect-tree flips, 9 disclosed)"). The committed file says 20 mutants / 11 flips / 9 not-shown with `H6c` missing, and its junk readings are stale. The L1 must reconcile it as errata before the C2 verdict rests on it; the wave-1 `r46-selftest-f29.py` must grade the mutants that actually exist in the frozen gate, not a 21-mutant set that does not.

### F3. The claim's named control file is missing from the freeze

`claims.json` lines 26 and 47 both name `"control": ".ufo/waves/round-46/attempt2/controls/freeze-controls.txt"`. That file does not exist:

```
$ ls .ufo/waves/round-46/attempt2/controls/freeze-controls.txt
ls: cannot access '...': No such file or directory
$ git ls-tree --name-only fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 .ufo/waves/round-46/attempt2/controls/
.ufo/waves/round-46/attempt2/controls/f29-defects.py
.ufo/waves/round-46/attempt2/controls/f29-fixture.py
.ufo/waves/round-46/attempt2/controls/f29-gate-at-base.txt
.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt
.ufo/waves/round-46/attempt2/controls/mutbat-before.txt
.ufo/waves/round-46/attempt2/controls/selftest-baselines.txt
.ufo/waves/round-46/attempt2/controls/sources-census-before.txt
```
Attempt 1's freeze did commit a control set (`git ls-tree --name-only 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 .ufo/waves/round-46/controls/` → `freeze-check.txt`, `freeze-controls.py`, `freeze-controls.txt`, `sources-census-before.txt`). The attempt-2 freeze ships seven control files and none is the one the claims name. `freeze.txt` line 10 also names a `run-controls.sh` ("freeze-check replay: run-controls.sh (wave 1) …") which is likewise absent. Both are omissions for the L1 to close or record as errata.

### F4. The wave-2 spec's "tree under attack" placeholder points at the freeze, not the wave-1 integration

**Attacked:** `.ufo/waves/round-46/attempt2/build-wave2-spec.py:8` and the generated `wave2-spec.json`.

Command:
```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff .ufo/waves/round-46/attempt2/build-wave2-spec.py
```
Output:
```
-INTEG = "AT-INTEGRATION"       # patched by the L1 before validation
-FREEZE = "AT-FREEZE"
+INTEG = "fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4"       # patched by the L1 before validation
+FREEZE = "fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4"
```
The committed copy at `ee03806` still reads `AT-INTEGRATION`; the L1's working-tree edit points `INTEG` at `fe0f56b…`, which is the **freeze** commit — the same value as `FREEZE`. The wave-2 context string therefore reads "the tree under attack is lane commit fe0f56b… (integration of wave 1)", i.e. wave 2 would attack the freeze tree, which does not contain the wave-1 work. The placeholder has to be repointed at the wave-1 integration commit once that commit exists. (This is the L1's own working-tree edit, observed read-only; the draft entry states the requirement and the current value without touching the file.)

### F5. Facts the draft entry states, each re-derived
- **Base / freeze.** `claims.json` `"base": "04af9bc92229232ea5cce8b32bfe59dd969eb26d"`; `git rev-parse fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4^` → `04af9bc92229232ea5cce8b32bfe59dd969eb26d`. Freeze record `freeze.txt` line 2 agrees.
- **Pin integrity.** `sha256sum` of `claims.json` → `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0` (= `freeze.txt` line 3); `r46-mutbat.py` → `f7a7cdfa…29e7fa8` (= line 4); `r46-f29-gate.py` → `a1091e24…6fb8cd` (= line 5); `round-46-a2/S074.txt` → `1296528d…78c039` (= line 6); `round-46-a2/manifest.json` → `46e8077a…81569f` (= line 7); `source-recheck.py` → `fd2e01e8…9c003` (= line 8); `controls/mutbat-before.txt` → `13c21fcd…59efb1fd` (= the claims' own `expect_before` receipt pin). All match.
- **Attempt-1 counters untouched.** `git diff 04af9bc92229232ea5cce8b32bfe59dd969eb26d fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py` → **empty**. Also `diff -q` of the base export's and the freeze export's `r46-counters-selftest-c1.py` → identical.
- **C2 before-value (re-run).** Frozen gate on the base export → `f29-gate fixed=1/7 exit=1` (H1,H2,H3,H4,H5,H6 red, H7 green); on the freeze export → `f29-gate fixed=2/7 exit=1` (H4 capture green + H7 census green). Matches `controls/f29-gate-at-base.txt` byte-for-byte in its 8 lines, and the claims' `freeze_tree_reading` ("2/7 at the freeze tree").
- **C2 capture binding (re-run).** `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` → `S074:sha256 OK` then `S074:Q1 OK occurrences=1 anchor=10-ok` … `S074:Q9 OK occurrences=1 anchor=38-ok`, exit 0. S074 capture is 42 lines, 7 087 bytes; manifest quotes 9.
- **Plain counts (re-run at both trees).** Base export: frontier rows 28, SOURCES rows 73, knowledge 65, absence sweep 2 files. Freeze export: 28 / 73 / 65 / 2 (identical — the freeze adds instruments and the S074 capture, not corpus knowledge). The two absence-sweep files are `corpus/knowledge/github-private-vulnerability-reporting.md` (F28's scope-out note) and `corpus/SOURCES.md` (the `S068` GitHub-Advisory-Database row), matching the claim's `before` sentence.
- **c2 selftest baseline (re-run).** `python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure "$S/pure"` → last line `selftest cases=137 failures=0`, matching `controls/selftest-baselines.txt` ("c2 137/0").
- **c1 selftest baseline (re-derived statically, not by run).** The c1 selftest's own count line is `out("selftest cases=%d failures=%d" % (len(results), failures))` (`r46-counters-selftest-c1.py:670`), so the count is the number of `results` entries. Parsing the frozen file: 59 literal `CASES` entries + 12 from the `ROWLEVEL` expansion (each of its 12 members becomes 2 cases, `:541-544`) + 1 `_stub_only` + 4 fixed results (`TIP-7of7`, `CONTROL-do-nothing`, and two `home_case` entries, `:621-625`) = **76**, matching `controls/selftest-baselines.txt` ("c1 76/0"). The *failures* half of that receipt line is not re-derived by this seat (see Limitations).
- **C1 battery receipt consistency (re-derived by parsing).** The receipt's 41 mutant ids equal the frozen battery's `C1_MUTANTS` (20) + `C2_MUTANTS` (21) id-for-id, in order; its 20 `verdict=uncaught` ids are exactly the 7 + 13 the claim names (`M06-L3-home-dropped, M07-L3-home-no-abs, M13-L6-control-dropped, M14-L6-exit-ignored, M18-anchor-dirs-wide, M19-L2-eq-relaxed, M20-syntax-ignored` and `G1c-src-boundary, G2a-verified-prefix, G2b-wordfloor-low, G2c-need-empty, G3a-cells-loose, G4b-quotes-low, G5c-pass-low, G6a-guards-dead, G6b-integrity-loose, G6c-size-low, G7a-verdict-or, G7b-symlink-dead, G7c-okline-loose`). The receipt is faithful to the instrument; only the f29 R50 receipt (F2) is not faithful to its gate.
- **Wave shapes (re-derived).** I ran both committed builders in scratch (patched to write into my scratch, so the committed specs were not overwritten): wave 1 → `{"connector": 1, "critic": 5, "executor": 11, "mutation-tester": 7, "revenger": 1, "reviewer": 12, "scout": 9, "scribe": 15, "sentinel": 2, "simplifier": 1}` / `seats=64 attack=27 (42.2%)`; wave 2 → `{"connector": 1, "critic": 7, "executor": 3, "mutation-tester": 10, "revenger": 1, "reviewer": 6, "scout": 2, "sentinel": 1, "simplifier": 1}` / `seats=32 attack=23 (71.9%)`. These match the committed `wave1-spec.json` / `wave2-spec.json` (64 and 32 items). The attempt-2 `wave-registry.txt` does **not exist yet**; the draft says so and counts from the specs. The attempt-1 entry's own convention (`LOG.md:2015`, "attack 21/64") is reviewer+critic+mutation-tester, so the draft uses that for comparability and states the builders' own numbers beside it.
- **Assimilation (re-derived).** Lane registry 73 ids vs the read-only merge package's 94 staged ids → **43** id collisions (`S031`–`S073`). The package's own `MERGE-REPORT.md` still claims "lane registry currently holds 30 rows", and `grep -rliE 'repository securit. advisor|GHSA'` over the package returns **no files** — the package holds no advisory ground, so nothing competes with F29.

### F6. Attempt-1 entry shape the draft follows

`LOG.md:2012-2020` has seven bullets: base/freeze, planner mapping + wave shapes, wave findings, landed commits + final measurement, mined mistakes, scores + assimilation + open-for-the-closure, tooling + stale lane. The draft has the same seven, same order, same headings (`## Round 46 (attempt 2) — L1 \`KasegiR46\``), same closers (`Tools`/`Stale lane`, `Assimilation`, `Open for the closure`, `Mined mistakes`). Attempt-1's stale-lane line reads "respawn-per-round driver; no other kasegi mission open" — I re-derived that the fleet's `.ufo/state/kasegi.mission` (`2685101`) is **not running** and `.ufo/state/kasegi.round` still reads `17`, and the lane's only fleet report is `.ufo/reports/round-46/kasegi.md` (the attempt-1 honest stop). No other kasegi mission is open.

## Limitations

- **The battery replay at the base export did not complete inside this seat's window.** I launched `python3 -B corpus/instruments/r46-mutbat.py --root "$S" --pure "$S/pure" --work "$S/w-base" --counter both --jobs 8` against the base export and it was still running after ~30 minutes with only the first mutant line emitted. The host was under extreme contention from sibling seats (load average 277, 17 concurrent `r46-mutbat` processes). **C1's before-value in the draft is therefore the committed receipt `controls/mutbat-before.txt` (sha256-pinned by `freeze.txt` and by the claim), cross-checked id-for-id against the frozen battery's mutant tables — not a completed re-run of the battery itself.** The L1's final measurement must re-derive it.
- **The c1 selftest baseline re-run also did not complete** (only 4 of 76 case scratch dirs after ~30 minutes, same contention). `controls/selftest-baselines.txt` says "c1 76/0"; I verified the **case count** of 76 structurally by parsing the frozen file (F5) and the **c2 half** by run (`cases=137 failures=0`), but the c1 `failures=0` half is cited from the receipt, not re-derived.
- **The wave-1 findings and the `AT-*` slots are placeholders**, because wave 1 was still running when this seat wrote (45 of 64 seat reports present at write time, no `wave1-results.json`, no `attempt2/wave-registry.txt`, no `attempt2/wave2-dispatch.json`). The wave-1 and wave-2 role mixes come from the committed specs, not from a registry file that does not yet exist. The wave-2 spec's `INTEG` placeholder (F4) must be repointed at the wave-1 integration commit before wave 2 is validated; it currently names the freeze commit.
- **The L1 is editing the same working tree this seat read.** `build-wave2-spec.py` and `wave2-spec.json` are modified in the working tree (the L1's `INTEG`/`FREEZE` patch, F4) and `attempt2/wave1/`, `attempt2/wave2/`, `attempt2/controls/final-measure.sh`, `attempt2/counter-errata.md`, `attempt2/digest-wave.py` are untracked. This seat read them read-only and wrote only inside `.ufo/waves/round-46/attempt2/wave1/R46bScribeLog.draft/` and its own report file; the two tracked modifications are the L1's, not mine (`git diff` shows only the `INTEG`/`FREEZE` lines).
- **The `AT-TIP` projection (F1) is a projection, not the landing tree.** It is the frozen fixture's positive tree with the F29 README row and the frozen `ENTRY` body, built in scratch. It shows what the attempt-1 counters will read on a correct landing; the L1's real tip may differ.
- **I did not read all 45 wave-1 seat reports.** The wave-1 findings bullet in the draft therefore carries the L1's own fill-in rather than a seat-by-seat synthesis; a scribe seat reading the settled wave would add the falsification results.
- **No tool was installed or upgraded** and no pacman transaction was attempted (the host-wide pacman pause stands); the operator tooling directive at `/home/vgpnk/.omp/agent/RULES.md` was read.
- **Scratch removed** on exit: `/fast/scratch/hyaku/kasegi-r46/R46bScribeLog` (receipts were copied into the evidence quoted above before removal).
