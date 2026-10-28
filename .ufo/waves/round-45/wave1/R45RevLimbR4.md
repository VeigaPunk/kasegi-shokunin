VERDICT: BROKEN

Scope: C1 limb attack on R4 of `corpus/instruments/r45-routed-defects.py` (`def limb_r4`, lines 210-222). Read-only seat; nothing committed, no git mutation, scratch removed on exit.

## Finding 1 — a 70-byte stub makes limb R4 read fixed=1

What limb R4 does (`r45-routed-defects.py:210-222`): it checks only that `corpus/instruments/freeze-check.py` exists under the graded root, runs it with `--selftest` and parses `^selftest cases=(\d+) failures=(\d+)` (needs rc 0, failures 0, cases >= 6), then runs it again with `--claims <root>/.ufo/waves/round-45/claims.json --tool-root <root> --base <base>` and matches `^freeze-check claims=2 base_ok=2\b`. It never reads the claims, never runs a `counter_cmd`, and never looks at the base beyond passing it through. Its stdout is the entire evidence.

Recipe (cheapest tree): one file, `corpus/instruments/freeze-check.py`, the only content in the root:

```
print("selftest cases=6 failures=0\nfreeze-check claims=2 base_ok=2")
```
(`wc -c` = 70 bytes.)

Command and printed output:
```
python3 $S/tree/corpus/instruments/r45-routed-defects.py --root $S/c1 --baseline $S/base
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=1 unresolved=4 exit=1
```
The defect R4 stands for (spot-check `corpus/lessons/round-44-verifier-spotcheck.md` §6 item 4: "A frozen counter string must be run on the base before freeze") is still present: no replay code exists in the tree; the limb has been satisfied by a print.

## Finding 2 — the stub's inputs are ignored (the limb does not measure a replay)

Commands and output, same stub `$S/c1/corpus/instruments/freeze-check.py`:
```
python3 freeze-check.py --claims /nonexistent --tool-root /nonexistent --base /nonexistent
selftest cases=6 failures=0
freeze-check claims=2 base_ok=2
rc=0
```
Counter with an EMPTY baseline directory (`$S/emptybase`), root = stub only:
```
limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
```
Frozen claims altered so that the replay must fail (C1/C2 `counter_cmd` pointing at a nonexistent `corpus/instruments/does-not-exist.py`, `expect_before` set to `routed-defects total=5 fixed=9 unresolved=9 exit=1`), root = stub + those claims:
```
limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
```
A stub that never consults its base or claims passes whichever base and claims it is handed.

## Finding 3 — the constructions tried, and the discriminators

Seven constructions (each root contains only what is listed; counter = frozen `r45-routed-defects.py`, base = pure base copy unless noted):

| construction | limb R4 printed | result |
|---|---|---|
| c1: one-line stub printing both tokens (70 B) | `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2` | FOOLED |
| c2: parses the real `claims.json` and prints `base_ok=len(claims)`, never runs any counter | `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2` | FOOLED |
| c7: symlink `freeze-check.py` -> stub stored outside the tree | `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2` | FOOLED |
| c3: tokens only inside a docstring (inert) | `limb R4 fixed=0 read=selftest-rc=0-tokens=None` | rejected |
| c4: prints both tokens then `sys.exit(1)` | `limb R4 fixed=0 read=selftest-rc=1-tokens=(6, 0)` | rejected |
| c5: zero-byte `freeze-check.py` | `limb R4 fixed=0 read=selftest-rc=0-tokens=None` | rejected |
| c6: dangling symlink `freeze-check.py` | `limb R4 fixed=0 read=freeze-check-absent` | rejected |

The limb rejects crude failures (absent, rc != 0, no token, dangling link) and accepts any file that prints the two tokens. The `--selftest` gate (`tk[0] >= 6`) is met by a literal.

Controls (discriminating the fixed=1 result from a do-nothing):
```
python3 r45-routed-defects.py --root $S/base --baseline $S/base
limb R4 fixed=0 read=freeze-check-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1

python3 r45-routed-defects.py --root $S/tree --baseline $S/base   # frozen claims + counters, no freeze-check.py
limb R4 fixed=0 read=freeze-check-absent
```

## Finding 4 — the honest replay happens to agree; the limb cannot tell

I ran the frozen counters at base directly (the replay the limb claims to represent):
```
python3 r45-routed-defects.py --root $S/base --baseline $S/base   -> routed-defects total=5 fixed=0 unresolved=5 exit=1
python3 r45-c2-gate.py --root $S/base                              -> c2-gate fixed=1/7 exit=1
```
Both match `expect_before` in the frozen claims, so `base_ok=2` is true for the frozen claims. The stub's answer is correct by coincidence: nothing in the tree derives it, and Finding 2 shows it stays `base_ok=2` when the claims are false. The limb's outcome on the frozen data is accurate; its evidence is not.

## Finding 5 — the frozen controls cannot catch this

`.ufo/waves/round-45/controls/freeze-controls.py` builds five trees (do-nothing base, `c1-marker-only`, `c2-junk-row`, `c2-fabricated-quote`, plus the base). The `c1-marker-only` builder (lines 53-71) writes prose markers and appends to `QUALITY.md`, `SKILL.md`, `README.md`, `round-44.md` and the refiled receipt; it never creates `corpus/instruments/freeze-check.py`. `freeze-controls.txt` therefore contains no control in which a `freeze-check.py` exists, and none exercises limb R4's stub path. The C1 kill rule ("any control grades fixed=5") is not triggered by a stub alone (it yields fixed=1), so the kill rule does not catch R4 being satisfied by a fabrication.

## Finding 6 — repo state (read-only evidence)

`git -C <repo> cat-file -e dc5bb8c…:corpus/instruments/freeze-check.py` -> `fatal: path 'corpus/instruments/freeze-check.py' does not exist in 'dc5bb8c…'`, `base-exists-rc=128`.
`git -C <repo> log --oneline --all -- corpus/instruments/freeze-check.py | wc -l` -> `0`.
The working tree and HEAD 5242db6 have no `corpus/instruments/freeze-check.py`. The limb's only gate is that file existing in the graded root, so any seat's `freeze-check.py` (including the R45ExecFreezeA/B drafts, which I did not read) would be graded by the same stdout-only test.

## Suggested repair (not applied; the counter is frozen)

- The limb must not trust a tool's stdout. Replay in the limb: run each claim's `counter_cmd` at the base itself and require `expect_before` as a whole line, or have the limb recompute the base result from the frozen counters.
- Add to `freeze-controls.py` a tree containing only the 70-byte stub, expecting R4 `fixed=0`. This is a predicate-level change; per the kill rule it would be logged as an erratum only if the predicate sentence is unchanged.

## Limitations

- Attacked R4 only. I did not attack limbs R1, R2, R3, R5, and did not check the total C1 fixed=5 claim beyond R4.
- Built the trees from the pure base copy (`/fast/scratch/hyaku/kasegi-r45/L1/pure`, copied, never edited) plus the frozen `claims.json` and `r45-routed-defects.py` and `r45-c2-gate.py` read with `git show 8cf62c8…` (claims sha256 `bbe40503…c206` matches `freeze.txt` `claims-sha256`). Source snapshots were copied in `tree` only; the stub constructions do not use them.
- A first run of c2 failed because I had not copied `claims.json` into its root; that was my construction error. I fixed it and report only the rerun. The honest C1 and C2 replays were run from the frozen counter copies, not from HEAD.
- I did not read or run the builder drafts, so I make no claim about whether a real `freeze-check.py` passes this limb.
- Commands are re-runs performed in this seat; the outputs above are copied from those runs.

## Installs / side effects

None. No tools installed or upgraded. Read-only git (`show`, `cat-file`, `log`, `ls-files`, `status`) only; no writes to the repo except this Report file. Scratch `$HYAKU_SCRATCH/kasegi-r45/R45RevLimbR4/` removed on exit.
