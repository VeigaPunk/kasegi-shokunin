VERDICT: INFO

Seat R46bRevC1Lineage — attack on C1's evidence chain at the current tip (freeze ee03806, base 04af9bc92229232ea5cce8b32bfe59dd969eb26d). All runs re-performed by me 2026-10-29; scratch was /fast/scratch/hyaku/kasegi-r46/R46bRevC1Lineage (removed after the receipts were copied to R46bRevC1Lineage.draft/receipts/). No git/jj mutation, no lane file touched.

## F1 — DRIFT: the recorded c1-gate pair (1/7 before, 7/7 after) is NOT reproducible against the declared attempt-2 base 04af9bc9; both roots read 2/7

Thing attacked: the recorded c1-gate fixed values that my seat spec replays against a base export of 04af9bc9.

Commands and printed output (base export = my `git archive 04af9bc9` at $S/base):

```
$ python3 -B corpus/instruments/r46-c1-gate.py --root $S/base --baseline $S/base --work $S/work-gate/g1
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=65
gate L2 pass=0 read=base-gated=22 regrounded=0
gate L3 pass=0 read=recheck-lines-exact=0
gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
gate L5 pass=0 read=append-only-restoration-kept=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=2/7 exit=1
```

(verbatim log: g1-base-base.log.)

```
$ python3 -B corpus/instruments/r46-c1-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --baseline $S/base --work $S/work-gate/g2
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=65
gate L2 pass=0 read=base-gated=22 regrounded=0
...
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=2/7 exit=1
```

(verbatim log: g2-live-base.log.)

Seat-spec expectation was `fixed=1/7` for base-vs-base and `fixed=7/7` for live-vs-base. Observed: 2/7 in BOTH. Exact numbers of the drift: before-value 1/7 → 2/7 (+1 limb, L1); after-value 7/7 → 2/7 (−5 limbs, L2–L6).

Root cause (lineage), with reproduction:

1. Attempt-1 landed the re-grounding of the two C1 entries BEFORE the attempt-2 base was cut. Evidence: `git log --oneline` shows round-46 attempt-1 commits 510a2d5 and 7eb7786 below base 04af9bc9 ("hyaku run12"); both entries already carry `## Re-ground (round 46)` and the exact `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md` line in my 04af9bc9 export.
2. Therefore gated(04af9bc9)=22 = TARGET_GATED (r46-c1-gate.py:24), so L1 passes at the do-nothing base itself, and the regrounded set R = gated(BASE)−gated(TREE) is ∅ for every descendant tree → L2–L6 fail at base and at the live tip alike.
3. The recorded 1/7↔7/7 pair belongs to the attempt-1 era base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba. Attempt-1's own receipt `.ufo/waves/round-46/controls/final-measure.txt:8-19` (measured-at-rev eb874bc, base 914ca0b) prints `gate L1 pass=0 read=gated=24 ... c1-gate fixed=1/7 exit=1` at base and `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md ... c1-gate fixed=7/7 exit=0` at tip. The errata file (`.ufo/waves/round-46/counter-errata.md`, C1-E6 note) records `gated=24 broken=0 at the base under v1.1`.
4. I reproduced the recorded values exactly on the era-correct baseline. pure2 is the corpus-only export of 914ca0b (`/fast/scratch/hyaku/kasegi-r46/L1/pure2`; it lacks the r46 instruments and has 64 knowledge files vs 65 at 04af9bc9):

```
$ python3 -B corpus/instruments/r46-c1-gate.py --root /fast/scratch/hyaku/kasegi-r46/L1/pure2 --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/work-gate/g3
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
gate L3 pass=0 read=recheck-lines-exact=0
gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
gate L5 pass=0 read=append-only-restoration-kept=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
```

(g3-pure2-pure2.log — matches the recorded before-value `c1-gate fixed=1/7 exit=1` with the exact limb readings.)

```
$ python3 -B corpus/instruments/r46-c1-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/work-gate/g4
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=46 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

(g4-live-pure2.log — matches the recorded after-value `c1-gate fixed=7/7 exit=0` line-for-line, including L6 `mutants=46 survivors=none`.)

Impact assessment: this is a calibration/spec defect, not a C1 kill. The attempt-2 C1 claim's counter command is the battery (r46-mutbat.py) and its kill rule's do-nothing control concerns the battery and selftests at the base export — neither involves c1-gate moving this round; the attempt-2 freeze pins no c1-gate value (freeze.txt lines 8–11 record f29-gate, mutbat, selftest baselines only). But two consequences must be named: (a) the wave-1 seat-spec expectations for c1-gate against 04af9bc9 encode the attempt-1-era baseline and will produce false regression flags for anyone replaying them; (b) as a contrast instrument c1-gate is now saturated at this base — final-measure.sh's no-harm replay `--root tip --baseline base` will print 2/7 for the wave's integrated tip, which a human could misread as a regression unless this note is at hand.

## F2 — HOLDS: selftest baselines reproduce exactly (76/0 and 137/0)

Commands (recorded invocations from `.ufo/waves/round-46/attempt2/controls/final-measure.sh`, PURE=/fast/scratch/hyaku/kasegi-r46/L1/pure2):

```
$ python3 -B corpus/instruments/r46-counters-selftest-c1.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/work-s1 --jobs 8
...
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
```

(s1-selftest-c1.log — matches controls/selftest-baselines.txt line 3 `selftest cases=76 failures=0`, including the same single disclosed residual false green.)

```
$ python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
...
selftest cases=137 failures=0
```

(s2-selftest-c2.log — matches controls/selftest-baselines.txt line 5 `selftest cases=137 failures=0`; case list begins `ok null null-pure-base-unmodified fixed=1/7` and ends with the three ACCEPTED probes, identical in shape to the L1-scratch baseline receipt.)

Supporting byte-checks: r46-c1-gate.py sha256 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7 is identical at base 04af9bc9 (git archive) and the live lane; `git diff --stat 04af9bc9..HEAD` shows corpus/ gains only r46-f29-gate.py, r46-mutbat.py and the S074 snapshot — no knowledge entry, instrument or fixture is modified, which is exactly why the two gate roots in F1 agree.

## F3 — HOLDS: the two re-grounded entries' rows are load-bearing (2/46 spot-blanked, entries go red; do-nothing copies stay green)

Thing attacked: load-bearingness of the `## Re-ground (round 46)` rows in corpus/knowledge/claim-gates.md (25 rows) and corpus/knowledge/claim-package-contract.md (21 rows), per the L6 limb and attempt-1's `mutants=46 survivors=none` receipt.

Method: scratch copies of the live corpus; do-nothing control copy unmutated; one token blanked in its anchored lines per mutated copy, exactly the gate's own L6 blanking (`#`-fill of the token string at the anchored line).

Do-nothing controls (green, exit 0):

```
$ python3 -B corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md --root $S/spot/control-gates
reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0

$ python3 -B corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md --root $S/spot/control-contract
reground entry=claim-package-contract.md rows=21 ok=21 files=4 distinct=1 exit=0
```

Mutated copies (red, exit 1, exactly the targeted row — discrimination against the do-nothing control):

```
# claim-gates.md row G1: anchor corpus/instruments/claim-package-check.py:101-108, token 'custodian-receipts.json', (found literally at line 105)
$ python3 -B corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md --root $S/spot/mut-gates
row G1 ok=0 read=token-not-in-lines
reground entry=claim-gates.md rows=25 ok=24 files=3 distinct=1 exit=1
# full-output re-grep for "ok=0": exactly one line (row G1); all other 24 rows ok=1

# claim-package-contract.md row G17: anchor corpus/instruments/claim-package-check.py:636-637, token 'if NO_SUBMISSION not in text:' (found literally at line 636)
$ python3 -B corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md --root $S/spot/mut-contract
row G17 ok=0 read=token-not-in-lines
reground entry=claim-package-contract.md rows=21 ok=20 files=4 distinct=1 exit=1
# full-output re-grep for "ok=0": exactly one line (row G17); all other 20 rows ok=1
```

The full 46-row sweep was additionally re-executed by the gate itself in the F1 era-correct run (L6 `mutants=46 survivors=none`, g4-live-pure2.log), covering all rows of both entries with the same procedure; my two probes sample that set and confirm the mechanism still bites at the current tip. The anchored files are byte-identical between pure2 (914ca0b) and the live lane (sha256 compared: claim-package-check.py and all five anchored fixture files SAME), so the rows anchor content that has been stable across both eras.

## F4 — minor: the claims.json `plain` case-count grep does not describe the committed selftests

`grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py` prints `0` and `0` — neither script defines `case_` functions; cases are a `CASES` list (selftest-c1, line 457) and an incremental counter over case classes (selftest-c2, lines 287/570). The recorded tallies in F2 are the authoritative `selftest cases=N failures=F` lines and they reproduce; the plain grep in claims.json `plain` is stale boilerplate only.

## Limitations

- Spot-blank sampled 2 of 46 rows (per seat spec); the other 44 rows' load-bearingness was verified only through the gate's own L6 sweep inside the g4 run (mutants=46 survivors=none), not by 44 independent manual probes.
- F1's classification of the drift as era-dependence rests on pure2 being the 914ca0b corpus export; I verified that by content (64 knowledge files, no r46 instruments, QUALITY/README/SOURCES differ from the 04af9bc9 export) and by exact reproduction of the recorded limb readings, not by a git tag.
- The battery before/after (mutbat) re-run is outside this seat's item; my verdict on C1's overall state is limited to the gate, the two selftest baselines, and row load-bearingness.
- All gate aggregate runs executed tree-supplied recheck lines read-only with cwd set to the graded tree, under the grader's minimal environment, as the instrument itself does; no host state was written.
