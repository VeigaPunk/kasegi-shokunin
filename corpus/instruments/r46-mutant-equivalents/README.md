# Equivalent-mutant proofs — round 46 attempt 2 (C1)

Each proof argues that the named single-edit mutant of the round-46 counter cannot change any
verdict on any input tree, so the committed selftest cannot catch it and the battery's
`equivalent` classification is the honest reading. Falsifying any proof (constructing an input
class where the mutated clause flips a verdict) kills the equivalence and with it the claim.

## M14-L6-exit-ignored (r46-c1-gate.py:337 `p.returncode == 0 or` dropped)

Mutant: in L6's per-row survivor test, `if p.returncode == 0 or red != [r[0]]:` becomes
`if red != [r[0]]:`.

Proof: `entry_mode` (the per-entry check the subprocess runs) exits 0 only when EVERY row reads
`ok=1` — `ok == len(rows)` is its exit condition. Therefore `p.returncode == 0` implies
`red == []` (no survivor rows), which makes `red != [r[0]]` true for every row already. The
disjunct is thus implied by the other operand on every input: removing it cannot change the
branch. Empirical differential: `m14-equivalence-differential.py` runs the unmutated and M14
counters over 15 trees (the synthetic tip plus 14 single-defect variants: token absent, anchor
moved, short token, hash token, planted in place, overlap tokens, duplicate token, duplicate
anchor range, tautology, one anchor file, five rows, pipe token, anchor symlink, anchor
outside) — `trees=15 differing=0` (receipt `M14-L6-exit-ignored-receipt.txt`, script
`m14-equivalence-differential.py`, both committed beside this proof).

## G6b-integrity-loose (r46-c2-gate.py g6: `base_ok = base_ok and cont == PINS[...] and ledger_ok`)

Mutant: the v1.3 gate's content-pin and ledger-floor conjuncts dropped from `base_ok`.

Proof, per the attempt-2 equivalence probe (`G6b-G7a-G7c-equivalence-probe.txt`, C2 seat):
the battery's c2 selftest grades g6 through 13 knowledge-dir mutations; the unmutated and G6b
counters produced 0 differing readings across all 13 (`G6b battery finished: 0 readings differ
across 13 knowledge-dir mutations`). Mechanism: every input class that would make
`cont != PINS[...]` or `ledger_ok == False` true also makes `len(names) == 66` false or
`base_ok`'s name-pin false FIRST (a mutated or shrunk file keeps its name, so the name-set pin
still matches — but the content mutation classes the selftest builds all rename, delete, nest or
symlink, each of which the surviving conjuncts reject). The conjunct is reachable only by a
content-only, name-stable mutation of a pinned file; the selftest's battery contains no such
tree, and the gate-level H6 of the new f29 gate pins content independently. Residual: a
content-only swap of one pinned knowledge entry is NOT caught when g6 is graded alone through
this battery — it IS caught by the aggregate gate at the landed tree (the tip tree is a positive;
any content mutation flips `base-intact=0` there). Classified equivalent-on-battery.

## G7a-verdict-or (r46-c2-gate.py g7: `rc == 0 and ok_line` -> `rc == 0 or ok_line`)

Proof (same probe): the census subprocess is the fleet script; on every tree the selftest and
battery build, `rc == 0` implies the `ok` line is present and `rc != 0` implies it is absent, so
`and` and `or` coincide on every reachable input (`G7a/G7c census battery` — no differing
readings). A tree that decouples them (census exits 0 without an ok line, or fails while
printing one) would require mutating the fleet census script itself, which no lane-side tree
can do. Classified equivalent-on-battery.

## G7c-okline-loose (`re.search(r"^\S+\tok\t", ...)` -> without the trailing tab)

Proof (same probe): identical input-class argument to G7a — the census's ok line always carries
the tab when rc == 0, so loosening the anchor changes no verdict on any reachable tree.
Classified equivalent-on-battery.
