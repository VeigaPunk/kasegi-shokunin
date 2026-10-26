# SimplifierCleanup — round 35 wave 1 — YAGNI sweep of the new instruments

Seat: SimplifierCleanup (simplifier leaf, round 35 wave 1). Item: a YAGNI sweep of the four
round-35 surfaces — (1) `corpus/instruments/r35-defect-closure.sh`, (2) `corpus/instruments/
r35-fixtures/`, (3) the F18 knowledge entry `corpus/knowledge/cisa-kev-catalog.md`, (4) the
wave's receipts. Deletions are proposed only where behaviour is provably preserved, with the
counter before and after the proposal pasted below. No lane file was edited by this seat; the
one code deletion is delivered as a patch in §1.3 for the L1 (the suite has a live owner seat
and moved twice while this receipt was being written — see §0.3).

## Report

Posture `/skill:godspeed`: axes named were depth:verifiability (the sweep's whole product is
"can this instrument be deleted from or narrowed without losing a check?") and coverage (do the
four surfaces carry anything that is not load-bearing?). Iteration was cheap and parallel:
hash/consumer scans, then a scratch before/after proof, then a discrimination matrix.

No tool installs. No `pacman`. Shell-side tools used: `shellcheck 0.11.0` (already present,
`/usr/bin/shellcheck`), `patch`, `git` (index reads and scratch-only `git init`).

### 0. Pins, scope, and what moved under me

0.1 Read scope (all under `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless absolute):
`corpus/instruments/r35-defect-closure.sh`, `corpus/instruments/r35-fixtures/**`,
`corpus/knowledge/cisa-kev-catalog.md`, `corpus/lessons/round-34-verifier-spotcheck.md` §6,
`.ufo/waves/round-35/{claims.json,wave1/**}`, `corpus/instruments/r-defect-closure.sh` (read
only, for the cross-suite comparison). Writes: this receipt only.

0.2 Measurement pins (sha256 at the moment of measurement; window 2026-10-26T06:40Z–06:52Z):

```
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  corpus/instruments/r35-defect-closure.sh
b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113  corpus/instruments/r35-fixtures/fixtures.json
e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730  corpus/knowledge/cisa-kev-catalog.md
6a50764e5b069351062e892d69b4eeaf094b02b98b9f119e48aa161ca006ad72  deadcode.patch (§1.3, scratch)
b4c17aea45c7d6600f96aa11cc5ea765a8d030468b8476a560c28b1cc53ff168  matrix.out (§1.2)
1e1f2af4866e9c34481caf39166c5251ec61675f3c95c6183e28579706c7ba18  green-path selftest stdout (§1.3)
```

0.3 The suite is live. Two digests were observed during this seat: `a4f80067183e…` at
03:43 local (773 → 834 lines) and `0ae4b4848b10…` at 03:49. The delta was prose plus one real
addition (a 17th mutant, D5 `-erratum-file`, with a `cascade` field) — i.e. a sibling seat was
landing the same "one mutant per clause" gap this sweep would otherwise have reported. A prose
count that read "sixteen mutants in all" in `a4f8006` now reads "seventeen" at `0ae4b48`
(`r35-defect-closure.sh:35`), which matches the measured `mutants=` sum (17/17). Every number in
this receipt is pinned to `0ae4b48`; the patch in §1.3 applies to those bytes.

### 1. `corpus/instruments/r35-defect-closure.sh`

#### 1.1 Every check loads a distinct defect, and no two checks test the same fact

Static reading first: 7 checks, 17 clauses (`clause_specs`), 17 clause mutants (`mutant_specs`),
17 `build_mutant` branches. One clause → one mutant → one branch, per defect:

```
D1: clauses=3 mutants=3 build_branches=3
D2: clauses=3 mutants=3 build_branches=3
D3: clauses=2 mutants=2 build_branches=2
D4: clauses=2 mutants=2 build_branches=2
D5: clauses=3 mutants=3 build_branches=3
D6: clauses=2 mutants=2 build_branches=2
D7: clauses=2 mutants=2 build_branches=2
```

The branch-name set and the spec-name set are equal (no dead branch, no spec without a branch):

```
$ awk '/^build_mutant\(\)/,/^}/' r35-defect-closure.sh | grep -oE '^    D[1-7]:[^)]*\)' | ... | sort
D1:+lane-hash-markers  D1:+placeholders  D1:-c1c6a5f  D2:-erratum-mean  D2:-erratum-row
D2:-row-bytes  D3:-registry-kill-rule  D3:-registry-r-defect-closure  D4:-provenance
D4:-tracked  D5:-discriminating-invocation  D5:-erratum-file  D5:-per-id-occurrences
D6:+dead-seat-sentence  D6:-correction-round-35  D7:-supersedes-R22  D7:-supersedes-R23
$ awk '/^mutant_specs\(\)/,/^}/' r35-defect-closure.sh | grep -oE "'[-+][^']+'" | tr -d "'" | sort
(same 17 names, same order)
```

Static identity is not evidence that two checks do not sample the same fact, so the fact-level
question was measured instead: **run all seven checks against every tree in the set and print the
set of failing checks.** A tree that breaks one limb must produce exactly one failing check; two
failing checks would mean two checks load the same fact. Driver: scratch `matrix.sh`, which
`sources` the suite's own function region (`funcs.sh`, extracted verbatim up to the trailing
plain-run driver, so the clause mutations and the checks are the committed ones and not a
re-implementation), then calls `materialize`/`build_mutant`/`check_d<i>` directly.

```
$ bash matrix.sh /fast/scratch/hyaku/kasegi-r35/SimplifierCleanup/cleanroot      # exit 0
## fixtures (materialized as their own git worktree)
fixture=D1     fails=[D1] expected=[D1]
fixture=D2     fails=[D2] expected=[D2]
fixture=D3     fails=[D3] expected=[D3]
fixture=D4     fails=[D4] expected=[D4]
fixture=D5     fails=[D5] expected=[D5]
fixture=D6     fails=[D6] expected=[D6]
fixture=D7     fails=[D7] expected=[D7]
control=clean            fails=[]
control=two-defect/D1D2  fails=[D1 D2]
## clause mutants (complete clean root + exactly one reopened clause)
mutant=D1   +placeholders              fails=[D1] expected=[D1]
mutant=D1   +lane-hash-markers         fails=[D1] expected=[D1]
mutant=D1   -c1c6a5f                   fails=[D1] expected=[D1]
mutant=D2   -erratum-row               fails=[D2] expected=[D2]
mutant=D2   -erratum-mean              fails=[D2] expected=[D2]
mutant=D2   -row-bytes                 fails=[D2] expected=[D2]
mutant=D3   -registry-r-defect-closure fails=[D3] expected=[D3]
mutant=D3   -registry-kill-rule        fails=[D3] expected=[D3]
mutant=D4   -tracked                   fails=[D4] expected=[D4]
mutant=D4   -provenance                fails=[D4] expected=[D4]
mutant=D5   -erratum-file              fails=[D5] expected=[D5]
mutant=D5   -discriminating-invocation fails=[D5] expected=[D5]
mutant=D5   -per-id-occurrences        fails=[D5] expected=[D5]
mutant=D6   +dead-seat-sentence        fails=[D6] expected=[D6]
mutant=D6   -correction-round-35       fails=[D6] expected=[D6]
mutant=D7   -supersedes-R22            fails=[D7] expected=[D7]
mutant=D7   -supersedes-R23            fails=[D7] expected=[D7]
```

26 trees, 26 exact singletons: no clause of any check leaks into another check, and the two
controls read exactly `[]` and `[D1 D2]`. Driver note: each mutant tree is rebuilt as a
*complete* root (the clean root plus the one reopened clause, own git index) — `build_mutant`
alone emits only the mutated limb's files, and every mutant tree needs an index or `check_d4`
would fail there for a reason unrelated to the mutation; the two deletion mutants
(`-provenance`, `-erratum-file`) keep their layout file absent by construction.

Verdict: **no dead or duplicate check, no unreachable branch, nothing to delete from the
check set.** The 17 clauses are 17 distinct facts.

#### 1.2 Dead code — found, proven inert, proposed for deletion

`shellcheck` reports three SC2034 dead assignments (`open`, `oout`, `cout`); independent grep
confirms none of the three is ever read:

```
$ shellcheck -s bash corpus/instruments/r35-defect-closure.sh
  ^-- SC2034 (warning): open appears unused. Verify use (or export if used externally).   (line 507, run_plain)
  ^-- SC2034 (warning): oout appears unused. Verify use (or export if used externally).   (line 692, run_selftest others-loop)
  ^-- SC2034 (warning): cout appears unused. Verify use (or export if used externally).   (line 790, control loops x2)
  (also: 8x SC2329 "never invoked" on check_d1..check_d7 — false positives, they are called through
   CHECK_FNS; 1x SC2016 on the intentional single-quoted fixture literal)
$ grep -nE '\$\{?(open|oout|cout)\b' corpus/instruments/r35-defect-closure.sh
NO-READS
```

`open` is assigned in both branches of `run_plain` and never read (the printed text is the
literal `open=0`/`open=1`); `oout`/`cout` capture output that the following `[ "$rc" ... ]` never
uses — only the exit status matters.

#### 1.3 The proposal, and the counters before/after

The patch removes 8 lines and adds 6 (six hunks), leaving every command, every message,
every exit code and every clause untouched:

```diff
--- a/corpus/instruments/r35-defect-closure.sh
+++ b/corpus/instruments/r35-defect-closure.sh
@@ -492,19 +492,17 @@
 run_plain() {
-  local i id rc closed=0 open
+  local i id rc closed=0
   for i in "${!CHECK_IDS[@]}"; do
     id=${CHECK_IDS[$i]}
     run_check "$RD_ROOT" "${CHECK_FNS[$i]}"
     rc=$?
     if [ "$rc" -eq 0 ]; then
-      open=0
       closed=$((closed + 1))
       printf '%s check=%s open=0\n' "$id" "${PAYLOAD:-undescribed}"
     elif [ "$rc" -eq 2 ]; then
       printf '%s check=%s harness-error=1 open=1\n' "$id" "${PAYLOAD:-undescribed}"
     else
-      open=1
       printf '%s check=%s open=1\n' "$id" "${PAYLOAD:-undescribed}"
     fi
   done
@@ -646,7 +644,7 @@
   local i id fn live_out live_rc fix_out fix_rc case_ok live_state fix_state
-  local name label cascade dest mout mrc mtotal mok j oout orc oth oth_failed
+  local name label cascade dest mout mrc mtotal mok j orc oth oth_failed
@@ -689,7 +687,7 @@
-        oout=$("${CHECK_FNS[$j]}" "$fixroot")
+        "${CHECK_FNS[$j]}" "$fixroot" >/dev/null
         orc=$?
@@ -753,7 +751,7 @@
-  local controls_ok=1 croot cid cfn cout crc cclosed cfailed
+  local controls_ok=1 croot cid cfn crc cclosed cfailed
@@ -761,7 +759,7 @@
-      cout=$("$cfn" "$croot")
+      "$cfn" "$croot" >/dev/null
       crc=$?
@@ -787,7 +785,7 @@
-      cout=$("$cfn" "$croot")
+      "$cfn" "$croot" >/dev/null
       crc=$?
```

Construction: scratch tree `b3` = the lane's `0ae4b48` bytes copied verbatim beside the
committed fixture set; `a3` = the same bytes with the patch applied (`patch -p1`, exit 0).
`shellcheck` on `a3` reports 0 SC2034.

Counters, all four paths, before and after (driver `proof.sh`, which rebuilds `b3`/`a3` from the
lane and applies the patch itself, so the patch is the only difference):

```
## digests
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  .../b3/corpus/instruments/r35-defect-closure.sh
2abccc817cf68b5819f0f0af83b31c83ae8f7a46e65f830d08014a9118cef35b  .../a3/corpus/instruments/r35-defect-closure.sh
## counters
before-green           rc=0 lines=40 sha256=1e1f2af4866e9c34481caf39166c5251ec61675f3c95c6183e28579706c7ba18
after-green            rc=0 lines=40 sha256=1e1f2af4866e9c34481caf39166c5251ec61675f3c95c6183e28579706c7ba18
before-base            rc=1 lines=8 sha256=c6e02c25f8e97311c8b9c0ba18a8c1f77637795ce4732baff986ae3a31f64365
after-base             rc=1 lines=8 sha256=c6e02c25f8e97311c8b9c0ba18a8c1f77637795ce4732baff986ae3a31f64365
before-plain           rc=1 lines=8 sha256=4f77e948ff50ad9d2a94891a5ae45bf4ae74377c50bac43a9df2d14fa9d5a53b
after-plain            rc=1 lines=8 sha256=4f77e948ff50ad9d2a94891a5ae45bf4ae74377c50bac43a9df2d14fa9d5a53b
before-prune           rc=1 lines=8 sha256=1eb25c2e62e34e0bab1c08ae34b6a8a2684a1846fd348f850afe0cd2beebe408
after-prune            rc=1 lines=8 sha256=1eb25c2e62e34e0bab1c08ae34b6a8a2684a1846fd348f850afe0cd2beebe408
## comparisons
green stdout identical      green stderr identical
base stdout identical       base stderr identical
plain stdout identical      plain stderr identical
prune stdout identical      prune stderr identical
```

The four paths are the full contract: `--root <all-fixed tree> --selftest` (green, 7/7 + the
five judge lines), `--root <lane base 3266c993>` (all seven open, `closed=0/7 exit=1`), the live
lane root (mixed, `closed=4/7 exit=1` at measurement — D4/D6/D7 still open, the L1's pending
landings), and `--root <fixture two-defect/D1D2>` (`closed=5/7`, the partial-summary branch).

Green-path stdout, before (= after, byte for byte; `--root cleanroot --selftest`):

```
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
```

Preserved contract (unchanged by the patch): the three CLI shapes (`(none)`, `--root DIR`,
`--selftest`), the `D<i> check=<payload> open=0|1` + `closed=K/7 exit=0|1` line grammar, the
`selftest case=`/`detail=`/`control=`/`judge=` grammar that `report_ok`/`plain_report_ok` judge,
the 17 clauses / 17 mutants / 2 controls, and exit codes 0 / 1 / 2.

I did **not** apply the patch to the lane: the file has a live owner seat (its digest changed
twice during this sweep) and the L1 is the only committer. It is a 6-hunk, zero-behaviour change
for whoever lands it next; if it lands after `0ae4b48`, `patch` may need a fuzz retry on the
`run_plain` hunk only.

#### 1.4 Cross-suite weight — observed, not proposed

The round-34 suite and this one share 7 function names (`usage`, `filter_out`, `report_ok`,
`plain_report_ok`, `judge_selftest_report`, `run_plain`, `run_selftest`) and 59 identical
non-comment lines out of 642 (`r-defect-closure.sh`) / 637 (`r35-defect-closure.sh`) code lines.
A shared library would remove those 59 lines and add a second convention to two fail-closed
gates whose *report shapes differ* (`case=R# live=… control=…` vs `case=D# live=… fixture=…
mutants=… others=…`), and would put one file's bug in both gates at once. Candidate: **rejected**
— the duplication is cheaper than the coupling, and `r-defect-closure.sh` is a frozen round-33
provenance instrument (`closed=9/9 exit=0` still measures today: `R1..R9`, run below).

One cross-suite duplicate *fact* exists and is worth recording: `D1`'s `lane-hash-markers` clause
counts `<LANE_HASH>` tokens in `SCORECARD.md`; `r-defect-closure.sh` `check_r1` counts the same
tokens in the same file. Neither subsumes the other (`R1` also requires the appended
`Correction (round 34)` block naming `7963976e`/`014ee2d`; `D1` also requires
`placeholders=0` and `c1c6a5f >= 1`), so both stay. Recorded, not deleted.

```
$ bash corpus/instruments/r-defect-closure.sh          # exit 0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
```

### 2. `corpus/instruments/r35-fixtures/`

#### 2.1 Weight

```
$ find . -type f -printf '%s\n' | awk '{s+=$1; n++} END{print "files="n, "bytes="s}'
files=65 bytes=77361
$ (sha256 per file, group by content)
redundant_instances=48 redundant_bytes=50814 distinct_blobs=17
```

17 distinct contents across 65 files: 66% of the bytes are copies of six fixed layout files
(`SCORECARD.md` fixed blob ×6, `SKILL.md` ×8, `corpus/QUALITY.md` ×7, `L1Integration.md` ×7,
`wave1-results.json` ×9, `…provenance.md` ×8, `claims-erratum-d5.md` ×7, plus the D4
`.gitignore`). No *file* inside any single tree is unused: each tree carries exactly the seven
layout files the six other checks need for `others=6/6`, plus D4's `.gitignore`.

#### 2.2 Every tree is load-bearing (measured)

Removing any one of the nine trees from a scratch copy of the set and running the green path:

```
$ for id in D1..D7 clean two-defect; do rm -rf <copy>/r35-fixtures/$id; \
    bash <copy>/r35-defect-closure.sh --root cleanroot --selftest; done      # exit 1 every time
removed=D1           rc=1  selftest problem=fixture-missing id=D1 … selftest cases=7 failures=1 control-failures=0
removed=D2           rc=1  selftest problem=fixture-missing id=D2 … selftest cases=7 failures=1 control-failures=0
removed=D3           rc=1  selftest problem=fixture-missing id=D3 … selftest cases=7 failures=1 control-failures=0
removed=D4           rc=1  selftest problem=fixture-missing id=D4 … selftest cases=7 failures=1 control-failures=0
removed=D5           rc=1  selftest problem=fixture-missing id=D5 … selftest cases=7 failures=1 control-failures=0
removed=D6           rc=1  selftest problem=fixture-missing id=D6 … selftest cases=7 failures=1 control-failures=0
removed=D7           rc=1  selftest problem=fixture-missing id=D7 … selftest cases=7 failures=1 control-failures=0
removed=clean        rc=1  selftest problem=control-missing path=…/clean  selftest cases=7 failures=0 control-failures=1
removed=two-defect   rc=1  selftest problem=control-missing path=…/two-defect/D1D2  selftest cases=7 failures=0 control-failures=1
```

So no fixture *tree* is redundant: the seven `D<i>` trees are the seven distinct defects, `clean`
is the only always-pass control, and `two-defect/D1D2` is the only conjunctive control (the
single-limb trees cannot show that two simultaneous faults are both reported; §1.1 measures
`fails=[D1 D2]` for it and `fails=[D1]`/`fails=[D2]` for the singles).

#### 2.3 `fixtures.json` — zero code readers, but pinned by five receipts: held

`fixtures.json` (3,236 B, `b9a07afa…`) restates the same case set as `r35-fixtures/README.md` in
JSON. Nothing reads it: the suite resolves only `$FIXTURES/<case>` directories (no glob over the
set root, and `materialize` copies a case dir, never the set root), and the only instruments in
the repo that read a `*-fixtures.json` read their own files
(`mirror-containment-check.py`, `resolve-dispatch-check.py`).

Deleting it in a scratch copy leaves the green path byte-identical:

```
$ rm <copy>/corpus/instruments/r35-fixtures/fixtures.json
$ bash <copy>/corpus/instruments/r35-defect-closure.sh --root cleanroot --selftest   # exit 0
no-fixtures.json rc=0
1e1f2af4866e9c34481caf39166c5251ec61675f3c95c6183e28579706c7ba18  b3-self.out
1e1f2af4866e9c34481caf39166c5251ec61675f3c95c6183e28579706c7ba18  b6-self.out
IDENTICAL-WITHOUT-FIXTURES-JSON
```

Behaviourally it is dead weight; evidentially it is not. Seven round-35 receipts pin its digest
(`ExecClosureSuite.md:19` lists it as a consumed read-only input; `ExecSelftestFixtures.md:19`,
`RevClosureSuite.md:29,346,510`, `MutFixturesLimbs.md:672`, `CritC1Kill.md:313`, `SentCred.md:193`,
`SentCred/artifacts.sha256:150` all quote `b9a07afa…`). Deleting it now makes seven delivered
records cite a path that does not exist. **Held for the L1**: retire it at a round boundary with
the digests re-issued, or keep it as the machine-readable case table. Not deleted by this seat.

#### 2.4 Base + overlay de-duplication — rejected

A base tree plus per-case overlays would cut the 48 duplicate copies (50,814 B). Rejected:
self-containment is the set's stated contract ("each tree is a complete minimal root",
`r35-fixtures/README.md` — "Contract"), the suite's `materialize` copies a whole tree with no
composer, and an overlay composer would be a *new* convention for 50 KB. The copy weight is not
the weight that costs anything here; the wrong bytes with the right file name would be.

### 3. The F18 entry — `corpus/knowledge/cisa-kev-catalog.md`

Measured at `e3f233c0…` (118 lines, 17,643 B). The entry grew from 88 to 118 lines while this
seat read it (a sibling scribe landed Claim 4b / FC-12 / FC-13), so these are counts at the pin.

3.1 **No filler, no duplicated sentence.** Zero duplicated sentences over 40 characters (60
sentences checked after stripping inline code). Every section carries a distinct fact: the
`Attribution` section states the one thing the capture cannot supply (no definitional sentence),
`Honest limit` states four limits, `Rejected over-generalizations` six rejections, `Scope and
limits` the pin/provenance limits — overlapping *subjects* with the claims, not restating them.

3.2 **No redundant claim.** Seven claims → thirteen checks, every claim naming at least one check:

```
Claim 1  quotes=2 checks=FC-1,FC-2
Claim 2  quotes=2 checks=FC-3,FC-4
Claim 3  quotes=0 checks=FC-5        (cites the quote carried in Claim 2)
Claim 4  quotes=2 checks=FC-6,FC-7,FC-9,FC-10
Claim 4b quotes=4 checks=FC-12       (plus FC-13 later in the entry)
Claim 5  quotes=0 checks=FC-8
Claim 6  quotes=0 checks=FC-11,FC-8
```

`FC-8` is the one check supporting two claims: it counts severity vocabulary and reward
vocabulary in one `grep` loop, and Claim 5 (no severity ladder, the F18-vs-CVSS distinction) and
Claim 6 (no reward ladder, the F18-vs-F13/F17 distinction) each take a different half as their
falsifier. That is one command, two facts — not a duplicated claim. No claim restates another:
Claim 5 and Claim 6 are the two *distinct* frontier distinctions that justify F18's admission,
which is exactly what the claim was for.

3.3 **One risk flagged (not a deletion).** Claim 4b's evidence is a live-page read of
`cisa.gov/…/bod-26-04…`, explicitly *not* registered as a source row and *not* inside
`corpus/source-snapshots/round-35/`, so it is the only claim in the entry that the `recheck:`
command cannot re-derive. The entry says so in-line ("not a pinned-source claim"), so it is
honest rather than hidden; whether an unpinned claim belongs inside a `source: S052` entry is the
reviewer's call, not a YAGNI deletion.

### 4. The wave's receipts — no duplicate artifacts

```
$ find .ufo/waves/round-35/wave1 -type f | wc -l          # 68 at measurement, growing
$ find .ufo/waves/round-35 -type f -size +0c -exec sha256sum {} + | sort | <adjacent-hash scan>
(no output: zero byte-identical artifacts anywhere in the round-35 wave directory)
$ find .ufo/waves/round-35 -type f -size 0c
./wave1-plan.err
./wave1-run.err
```

- Zero duplicate artifacts. Same-basename hits are only `c1-controls/before.txt` vs
  `c2-controls/before.txt` (two different controls' frozen baselines) and `RevD3D4/`'s four raw
  logs, which are not verbatim copies of their receipt (≤3 shared long lines out of 53/3/9/12 —
  they are the raw evidence, the receipt cites line ranges).
- The two 0-byte dispatch logs are the only zero-content files. Not deletable this round:
  `wave1/SentCred/artifacts.sha256:26,28` pin both at `e3b0c442…` (the empty-string digest), so
  removing them falsifies a delivered manifest. Candidate: **held**, same rule as §2.3.
- `wave1-spec.json` / `wave1-plan.out` / `wave1-dispatch.json` are not duplicates: `plan.out` is
  the planner's stdout embedding the spec, `dispatch.json` is spec + per-seat spawn records, and
  `wave1-spec.json` is the round's own artifact path cited by the round-28/31/33/34 lessons.

### 5. Deletion ledger

| # | surface | candidate | proof | verdict |
|---|---|---|---|---|
| 1 | `r35-defect-closure.sh` | `open`/`oout`/`cout` dead assignments (8 lines removed, 6 added) | 4 paths byte-identical before/after; shellcheck 3×SC2034 → 0 | **proposed**, patch in §1.3 |
| 2 | `r35-defect-closure.sh` | any of the 17 clauses / 17 mutants / 7 checks | 26-tree discrimination matrix, all singletons | **no candidate** (all load-bearing) |
| 3 | `r35-defect-closure.sh` + `r-defect-closure.sh` | shared report/judge functions (59 lines) | shared-line count; report shapes differ | **rejected** (couples two gates, second convention) |
| 4 | `r35-fixtures/` | any of the 9 trees | 9 removal runs, each exit 1 with a named missing tree | **no candidate** |
| 5 | `r35-fixtures/fixtures.json` | the file (3,236 B, zero code readers) | green path identical without it; 8 receipt digests cite it | **held** for the L1 |
| 6 | `r35-fixtures/` | base+overlay de-duplication (48 copies, 50,814 B) | weight measured | **rejected** (breaks complete-root contract, new composer) |
| 7 | F18 entry | any claim / section / check | claim→FC map, 0 duplicated sentences | **no candidate** |
| 8 | wave receipts | `wave1-plan.err`, `wave1-run.err` (0 B) | empty-string digests pinned in `SentCred/artifacts.sha256` | **held** (falsifies a manifest) |

Stop rule reached: the next deletion on any of the four surfaces would remove a distinction
either the suite's own matrix or a delivered receipt depends on.

### 6. Commands and exit codes

| command | exit | note |
|---|---|---|
| `shellcheck -s bash corpus/instruments/r35-defect-closure.sh` | 1 | 3×SC2034 (real dead code) + 8×SC2329 false positives + 1×SC2016 intentional |
| `grep -nE '\$\{?(open\|oout\|cout)\b' …` | 1 | `NO-READS` (no match) |
| `bash proof.sh` (scratch driver, 8 counter runs) | 0 | all 8 outputs identical in the four before/after pairs |
| `bash matrix.sh cleanroot` (26 trees × 7 checks) | 0 | 26 exact singletons |
| `bash corpus/instruments/r-defect-closure.sh` | 0 | `closed=9/9 exit=0` |
| `bash corpus/instruments/r35-defect-closure.sh` (live lane) | 1 | `closed=4/7 exit=1` — D4/D6/D7 open, the L1's pending landings |
| `bash <copy>/r35-defect-closure.sh --root cleanroot --selftest` | 0 | `cases=7 failures=0`, 5 judge lines, `complete-report accepted=1` |
| `bash <copy>/r35-defect-closure.sh --root <lane base 3266c993>` | 1 | `closed=0/7 exit=1` |
| 9× fixture-removal selftests | 1 each | every removal names the missing tree |
| `sha256sum` / `cmp` on all pairs | 0 | quoted above |

### 7. Scratch

All work trees lived under `/fast/scratch/hyaku/kasegi-r35/SimplifierCleanup/`
(`b3`, `a3`, `b5-*`, `b6`, `cleanroot`, `base`, `pruned`, `matrix-work`, drivers). The scratch
directory is removed before this seat yields (verified: the path is gone). Nothing was written
outside the lane's `.ufo/waves/round-35/wave1/` (this receipt) — no lane file, no git/jj
mutation, no other lane, no `shokuknow`.
