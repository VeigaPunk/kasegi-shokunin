# MutFrontierRuleA — round-34 wave1 seat receipt

Seat: MutFrontierRuleA (mutation-tester, leaf of the L2 wave, hyaku run 8).
Assignment: mutation-test the bidirectional rule A of `corpus/instruments/frontier-recheck-count.py` —
(1) remove the reverse direction → a fixture entry with an extra `--source` in its recheck line
(cited but not declared) that fails on the landed tool must PASS; (2) remove the forward direction →
a fixture entry whose header cites a source its recheck line omits must PASS; (3) controls: a no-op
patch must leave both defective fixtures rejected. Scratch copies only; this receipt quotes actual
commands, outputs and exit codes.

## Report

### 1. Target bytes and mid-wave drift (recorded, not hidden)

- Digest of record: `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` (433 lines).
  Confirmed FINAL by the author seat ExecFrontierBidirectional (peer message: "1be79af6… is FINAL and
  quiescent … I will not touch that file again") and independently by this seat's watcher: hash
  stable across 6 consecutive 10 s polls (≥60 s), every poll `1be79af6…`.
- The file moved four times while this seat worked: `87b14892dfc4…a7c29` (first read, 427 lines) →
  `cbd3879ea25…04da46` (430 lines) → `8a79010d55…57499c` (431 lines; peer declared it final, it was
  not) → `1be79af60c…cd48249` (433 lines). Diffs of my pinned copies against each successive landed
  state show every move was docstring-only (round-31 naming clause; six-case selftest description;
  the `cited`-set definition sentence). The rule-A code is byte-identical across all four digests —
  forward limb `if declared_set and recheck_ids and not declared_set.issubset(set(recheck_ids)):
  problems.append("header-sources-not-rechecked")` and reverse limb
  `if declared_set and recheck_ids and not set(recheck_ids).issubset(declared_set):
  problems.append("selection-not-declared-by-entry")` (final bytes: lines 211–212 and 213–214).
  The premature "final" call and the extra write are the author seat's to record; their words:
  "I should have frozen at 8a79010d and told you before touching it — my error, recorded in my
  receipt" (`.ufo/waves/round-34/wave1/ExecFrontierBidirectional.md`). This seat re-pinned and
  re-ran the entire matrix at `1be79af6…`; the interim runs at `8a79010d…` produced identical
  verdicts (noted in §5/§6).
- The lane instrument was never opened for write by this seat. Every mutant is a scratch copy under
  `/fast/scratch/hyaku/kasegi-r34/MutFrontierRuleA/variants/` (`pristine.py` = byte copy of landed,
  `working.py` = mutated in place and restored between steps).

### 2. Method and classification (declared before the runs)

- Detector D1 (the assignment's bounded behavioral detector): `timeout 60 /usr/bin/python3
  <variant>.py --root <lane>` per fixture lane; exit code + stdout recorded per run.
- Detector D2 (corroboration): `timeout 120 /usr/bin/python3 <variant>.py --selftest --scratch
  <seat scratch>` — the tool's own 6 fixture cases, two per direction of rule A.
- Classification: **KILLED** = the assigned fixture's verdict flips `FAIL`→`PASS` (rc 1→0) under the
  mutant while the other two lanes keep pristine verdicts; **SURVIVED** = all lane verdicts identical
  to pristine; control = never a kill; a pristine-baseline failure would make every probe
  **INCONCLUSIVE** (baseline held — §4 — so none is).
- Exact-once assertion before mutating: at the record digest, `grep -c` = 1 for each of the two limb
  `if` lines; at `8a79010d…` all four find-strings (both `if` lines + both `problems.append(...)`
  lines) measured `grep -c` = 1. The code is byte-identical across the drift, so the assertion
  carries over.

### 3. Fixtures (scratch lanes)

Three single-entry lanes under `$S/lanes/{pass,extra,missing}` (`$S` =
`/fast/scratch/hyaku/kasegi-r34/MutFrontierRuleA`). Each lane: a Frontier table with one `admitted`
row `F98 → knowledge/fixture.md`, a schema-1 manifest listing every mentioned id, and a stub
`corpus/instruments/source-recheck.py` (`import sys; sys.exit(0)`) — so a verdict can only come from
the harness's own binding, never from a capture. Entry files, complete:

`pass` (baseline; must pass on every variant) — sha256 `c76d0d2a63b7abecb22e7848221950827da5f550dfab050a4a397d93a8501274`:
```
# fixture entry

source: S050 — fixture header declaration

Body mentions S050 in prose only; no evidence bullets.

recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/fixture/manifest.json --source S050
```
`extra` (reverse defect: the recheck line selects S051, which the body cites in prose but no
declaration line declares) — sha256 `b8b27148605cf99d9791d5f097c013120355326102306ef86734a387bb7d0753`:
```
# fixture entry

source: S050 — fixture header declaration

Body mentions S050, S051 in prose only; no evidence bullets.

recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/fixture/manifest.json --source S050 --source S051
```
`missing` (forward defect: the header declares S051, the recheck line omits it) — sha256
`9ceefa913aab7b525b96aa493566fbd6e9589ece404edb232e7fa880182005ca`:
```
# fixture entry

source: S050 — fixture header declaration
source: S051 — fixture header declaration

Body mentions S050 in prose only; no evidence bullets.

recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/fixture/manifest.json --source S050
```
Shared lane bytes: README `d71dd9caa98d7a740ba63fdbd5e55120605c6cc151157084550cd0bfd2111505`
(pass/extra) and `65d6a874d910cea7951a22ad28056c7e3005fc47a3f51bbfcbb5effdbbf43ff8` (missing);
manifest `8dc62791475ff88d46c19c3e02de967218b31db9d6726bf3e3831bee3fde6579` (extra/missing, lists
S050+S051), `4eb1bf63289a2c9ef83663e940aa88173f484123a3cc4854fa1b73f962344c0f` (pass, S050);
stub `8529a9702678392668eb3a7b3635716d59bf26e5d0cfb37e3faea7c45a238fac` (all three).

The defect fixtures are limb-isolating by construction: in `extra` the only rule-A limb that can
fire is the reverse one (declared {S050} ⊆ selected {S050,S051}); in `missing` only the forward one
(selected {S050} ⊆ declared {S050,S051}); S050 is prose-cited in both, so
`selection-not-cited-by-entry` cannot mask a kill, and the manifest lists every selected id, so
rule B (`manifest-missing-ids`) cannot either.

### 4. Baseline — pristine `1be79af6…` (all runs below at this digest)

```
$ python3 $S/variants/pristine.py --root $S/lanes/pass    → rc=0
PASS     F98  knowledge/fixture.md    ids=S050      exit=0
entries=1 pass=1 exit=0
$ python3 $S/variants/pristine.py --root $S/lanes/extra   → rc=1
FAIL     F98  knowledge/fixture.md    ids=S050      exit=-    problems=selection-not-declared-by-entry
entries=1 pass=0 exit=1
$ python3 $S/variants/pristine.py --root $S/lanes/missing → rc=1
FAIL     F98  knowledge/fixture.md    ids=S050,S051 exit=-    problems=header-sources-not-rechecked
entries=1 pass=0 exit=1
$ python3 $S/variants/pristine.py --selftest --scratch $S/selftest/base → rc=0
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0
```
Baseline holds: the pass lane passes; each defect lane fails with exactly its own problem name —
the bidirectional rule fires in both directions on the landed bytes. No probe is
inconclusive-by-baseline.

### 5. M-REV — reverse direction removed → **KILLED**

One exact-once deletion of the two reverse-limb lines (diff against pristine; mutant sha256
`0704534056d92a6f8fab097d92589186b093e1002933abb6b149094a9efc53c8`):
```diff
@@ -210,8 +210,6 @@
         problems.append("no-manifest")
     if declared_set and recheck_ids and not declared_set.issubset(set(recheck_ids)):
         problems.append("header-sources-not-rechecked")
-    if declared_set and recheck_ids and not set(recheck_ids).issubset(declared_set):
-        problems.append("selection-not-declared-by-entry")
     if recheck_ids and not set(recheck_ids).issubset(set(cited)):
         problems.append("selection-not-cited-by-entry")
```
```
D1 lane=pass    → rc=0   PASS ... entries=1 pass=1 exit=0     (unchanged)
D1 lane=extra   → rc=0   PASS ... entries=1 pass=1 exit=0     ← FLIPPED (pristine: rc=1 FAIL)
D1 lane=missing → rc=1   FAIL ... problems=header-sources-not-rechecked / entries=1 pass=0 exit=1 (unchanged)
D2 selftest     → rc=1   selftest cases=6 failures=2
   selftest case=selection-not-declared exit=0 want=1 verdict=fail   (problem: exit=0 want=1)
   selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=fail
     (problem: missing='problems=selection-not-declared-by-entry,selection-not-cited-by-entry'
      — the fixture now reports only problems=selection-not-cited-by-entry)
```
The extra `--source S051` — rejected by the landed tool — **passes** once the reverse limb is gone:
the assignment's mutant (1) is killed by exactly its fixture, and the kill is corroborated by the
tool's own two reverse-direction selftest cases. The forward limb still catches the `missing`
fixture, so the mutant is surgical. (Interim run at `8a79010d…`: identical verdicts.)

### 6. M-FWD — forward direction removed → **KILLED**

Mirror-image deletion of the two forward-limb lines (mutant sha256
`3aada0aa6379b7205b39e813c45ccbc737b27b8c3dedf66165d023010092f03e`):
```diff
@@ -208,8 +208,6 @@
         problems.append("no-source-selection")
     if not manifest:
         problems.append("no-manifest")
-    if declared_set and recheck_ids and not declared_set.issubset(set(recheck_ids)):
-        problems.append("header-sources-not-rechecked")
     if declared_set and recheck_ids and not set(recheck_ids).issubset(declared_set):
         problems.append("selection-not-declared-by-entry")
```
```
D1 lane=pass    → rc=0   PASS ... entries=1 pass=1 exit=0     (unchanged)
D1 lane=extra   → rc=1   FAIL ... problems=selection-not-declared-by-entry / entries=1 pass=0 exit=1 (unchanged)
D1 lane=missing → rc=0   PASS ... ids=S050,S051 exit=0 / entries=1 pass=1 exit=0   ← FLIPPED (pristine: rc=1 FAIL)
D2 selftest     → rc=1   selftest cases=6 failures=2
   selftest case=header-source-not-rechecked exit=0 want=1 verdict=fail
   selftest case=evidence-declared-not-rechecked exit=0 want=1 verdict=fail
```
The header-declared source dropped from the recheck line — rejected by the landed tool — **passes**
once the forward limb is gone: assignment mutant (2) is killed by exactly its fixture, corroborated
by the tool's two forward-direction selftest cases, with the reverse limb still catching `extra`.
(Interim run at `8a79010d…`: identical verdicts.)

### 7. C-NOOP — comment-only patch adjacent to rule A → control holds; defective fixtures still rejected

One inserted comment line after the `declared_set` assignment (mutant sha256
`3f7020a92e5aa5699008cea199f303f2e17cdbf418ece6804e7a2157babc7e5a`):
```diff
@@ -197,6 +197,7 @@
         full = os.path.join(root, "corpus", entry_path)
     realpath = os.path.realpath(full)
     declared_set = set(declared) | set(evidence)
+    # control C-NOOP: comment-only edit, behavior unchanged (MutFrontierRuleA)
     problems = []
```
```
D1 lane=pass    → rc=0;  stdout byte-identical to pristine run (`diff` empty)
D1 lane=extra   → rc=1;  stdout byte-identical: FAIL problems=selection-not-declared-by-entry / exit=1
D1 lane=missing → rc=1;  stdout byte-identical: FAIL problems=header-sources-not-rechecked / exit=1
D2 selftest     → rc=0, selftest cases=6 failures=0
```
Control verdict: **not a kill** — the no-op moves no verdict anywhere; per the assignment's control
phrasing, both defective fixtures remain **rejected** under the no-op patch. The two kills in §5/§6
are therefore attributable to the deleted limbs, not to patching the file per se.

### 8. Restoration evidence

After each mutation step the working copy was restored with `cp <landed file> working.py` and
re-hashed. Final state, one command (`sha256sum` over landed + both scratch copies):
```
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  <lane>/corpus/instruments/frontier-recheck-count.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  $S/variants/pristine.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  $S/variants/working.py
```
The landed instrument is byte-identical before and after this seat's entire matrix.

### 9. Findings

- **F1 — both directions of rule A are load-bearing on the landed bytes.** M-REV killed by the
  extra-`--source` fixture; M-FWD killed by the omitted-source fixture; each kill flips exactly its
  own D1 fixture (rc 1→0) plus the tool's own two selftest cases for that direction, and leaves the
  other direction's fixture failing. C1's "frontier-recheck-count.py rule A enforces both directions
  (R9)" is corroborated at mutation depth, on digest `1be79af6…`.
- **F2 — the harness does not reward non-behavioral edits.** C-NOOP produced byte-identical outputs
  on all three lanes and 6/6 selftest.
- **F3 — cross-seat process note (for the L1, not a claims defect).** The instrument bytes were
  declared final twice (`8a79010d…`, then `1be79af6…`) while mutation seats were running. Both moves
  were docstring-only and moved no verdict (this seat ran the matrix at both digests), but a
  mutation receipt needs a pinned digest — done here, drift documented in §1.
- **F4 — scratch disposal.** `rm -rf /fast/scratch/hyaku/kasegi-r34/MutFrontierRuleA` executed after
  this receipt was written into the wave dir; removal verified in the seat's closing report.

No tools were installed or upgraded for this seat (stdlib `python3` + coreutils only), so the
tooling-authorization reporting clause has nothing to record.
