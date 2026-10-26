# MutCtrSelftestSkip — counter-mutant probe: skip-selftest

- Seat: MutCtrSelftestSkip, kasegi-shokunin round 33 wave 1 (leaf; no subagents, no background jobs).
- Subject: `corpus/instruments/capture-binding-check.py`. The lane file was NEVER written by this seat; the mutation exists only in scratch copies under `/fast/scratch/hyaku/kasegi-r33/MutCtrSelftestSkip/`.
- Detector: `python3 <copy> --selftest --scratch <scratch>`; judged by the assigned kill rule: "requires failures=0 lines printed from real cases and exit 0".
- Tooling: none installed (stdlib python3 + coreutils suffice). No pacman transactions. No git/jj mutations in the lane (read-only `rev-parse`, `log`, `status` only).
- Answering model (bound 10): zai/glm-5.3-flash; no model in the probe loop — purely behavioral.

## Mutant (one behavior-bearing point)

In `main()`, the selftest dispatch (lane file lines 481-482 in the v2 anchor):

```
old:     if args.selftest:
             return selftest(args.scratch)
new:     if args.selftest:
             print("selftest cases=0 failures=0")
             return 0
```

`--selftest` returns 0 without running any fixture case, printing a forged summary.

## Anchors (concurrent-edit handling, bound 6)

The owning seat ExecCaptureBinding edited the instrument mid-probe. Two hash-frozen anchors were probed:

- v1: `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79`
- v2: `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`

v1→v2 diff (captured at probe time): docstring-only — the summary placeholder
`records=<total> bound=<total> unbound=<bound-failures>` was reworded to
`unbound=<U>` with an explanatory sentence, and "ten fixture lane trees" became
"eleven". The mutation point `if args.selftest: return selftest(args.scratch)` is byte-identical in both.

At probe end the live lane file hashed `b4182665…` (same as v2) with `git status --porcelain` = `?? corpus/instruments/capture-binding-check.py` (file new/uncommitted at probe time), so the v2 verdict attaches to the exact bytes currently in the lane.

## Detector on pristine bytes (v1 = 4bc7aed3…)

```
$ python3 "$S/pristine/capture-binding-check.py" --selftest --scratch "$S/fixture-scratch"
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=url-matching-two-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0
pristine_exit=0
real_case_lines=11        # grep -c '^selftest case=' pristine.out
```

Baseline passes: 11 real cases, each with a case-backed verdict line, exit 0. (Contract asks >=6 cases incl. the six named shapes; observed 11, all pass.)

## Detector on mutated bytes (v1 and v2 anchors agree)

```
$ python3 "$S/mutated/capture-binding-check.py" --selftest --scratch "$S/fixture-scratch"   # v1 (4bc7aed3…)
selftest cases=0 failures=0
mutant_exit=0
real_case_lines=0        # grep -c '^selftest case=' mutant.out

$ python3 "$S/mutated-v2/capture-binding-check.py" --selftest --scratch "$S/fixture-scratch"  # v2 (b4182665…)
selftest cases=0 failures=0
mutant_v2_exit=0
real_case_lines=0
```

No fixture case ran (zero `selftest case=` verdict lines; the fixture scratch gained no run tree); the only output is the forged `selftest cases=0 failures=0`; exit 0.

## Kill-rule evaluation

- Clause A "failures=0 lines printed from real cases": UNMET by the mutant — its only `failures=0` line reports `cases=0`; no real case executed, so no case-backed failures=0 evidence exists (0 real-case verdict lines vs 11 in the pristine run).
- Clause B "exit 0": met by the mutant, but trivially — the mutation's whole point is exiting 0.

The kill rule requires A **and** B. The mutant cannot satisfy A by construction (skipping cases destroys the case-backed evidence it would need), and its output is trivially distinguishable from the genuine baseline (0 case lines + `cases=0` vs 11 case lines + `cases=11`).

## Verdict

**KILLED.** Catching clause: **"failures=0 lines printed from real cases"** — the forged `cases=0 failures=0` summary is self-incriminating (it reports zero cases) and is unaccompanied by any `selftest case=... verdict=` line from a real fixture run. The "exit 0" clause alone does NOT catch it (the skip exits 0 by design). This supplies the demonstration C1 `mutants_of_the_counter` requires for the `skip-selftest` counter mutant ("exit 0 without running selftest").

Coverage finding (for the L1, not a verdict change): claims.json C1 `predicate_sentence` wording — "`--selftest` prints failures=0 and exits 0" (claims.json, C1 predicate_sentence) — is satisfiable by the forged line; a harness that greps only the `failures=0` token plus the exit code would accept this skip. The assigned kill rule's "from real cases" qualifier is what closes it; C1's blunter clause "`--selftest` prints any failure or exits non-zero" does not catch this mutant on its own. Recommend any C1 verifier bind the pass to the 11 `selftest case=` verdict lines (or `cases=11`), not to the bare token.

## Restoration evidence (both anchors)

```
$ cp "$S/pristine/capture-binding-check.py" "$S/mutated/capture-binding-check.py"
$ sha256sum "$S/pristine/capture-binding-check.py" "$S/mutated/capture-binding-check.py"
4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79  pristine/capture-binding-check.py
4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79  mutated/capture-binding-check.py
$ python3 "$S/mutated/capture-binding-check.py" --selftest --scratch "$S/fixture-scratch"
selftest cases=11 failures=0
restored_exit=0
restored_diff_pristine=identical    # diff pristine.out restored.out -> empty

# v2:
$ sha256sum "$S/pristine-v2/capture-binding-check.py" "$S/mutated-v2/capture-binding-check.py"
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  pristine-v2/capture-binding-check.py
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  mutated-v2/capture-binding-check.py
restored_v2_exit=0
restored_v2_diff_pristine=identical
```

## End-state attestation

- Lane file sha256 before probe: `4bc7aed3…`; at probe end: `b4182665…` (owner's concurrent edit; this seat wrote it zero times). `git status --porcelain -- corpus/instruments/capture-binding-check.py` = `??` throughout (uncommitted owner work-in-progress; not mine).
- Writes by this seat: this receipt + `/fast/scratch/hyaku/kasegi-r33/MutCtrSelftestSkip/` only. No sibling path touched, no fleet-root or shokuknow writes, no campaign tools run there.

## Cleanup

Scratch dir removed before yield (receipt retained in the wave dir). Executed evidence:

```
$ rm -rf -- "$S" && test ! -e "$S" && echo scratch_removed=yes
scratch_removed=yes        # /fast/scratch/hyaku/kasegi-r33/MutCtrSelftestSkip absent; sibling seat dirs untouched
```

Report: .ufo/waves/round-33/wave1/MutCtrSelftestSkip.md
