# CritKillRule.pending-variants.md — round-40 wave-2 attack fixture

Attacker: `CritKillRule` (critic seat, C1 kill rule).
Target: the frozen kill-rule clause
```text
`grep -c '⟨pending' corpus/lessons/round-40.md` != 0
```
(claims.json, C1 `kill_rule`). The clause fires only on the exact byte
sequence U+27E8 `⟨` + `pending`. Any respelled pending marker leaves `grep -c`
= 0, so the round can close while genuine unfinished work is still marked.

Current state at Y (J5 3074c76):
```text
$ grep -c '⟨pending' corpus/lessons/round-40.md
0
```

The variants below each carry the *same* pending intent. Each is written on its
own line in this fixture; `grep -c '⟨pending'` over them returns 0.

| # | marker byte sequence | intent | detected by literal grep? |
|---|---|---|---|
| 1 | `⟨ pending` (space after U+27E8) | pending | no |
| 2 | `〈pending` (U+2329 left-pointing angle bracket) | pending | no |
| 3 | `<pending` (ASCII) | pending | no |
| 4 | `⟨Pending` / `⟨PENDING` (case) | pending | no |
| 5 | `⟨pending` (the literal the rule catches) | pending | **yes (control)** |

Verification transcript:

```text
$ grep -c '⟨pending' CritKillRule.pending-variants.md
0
$ printf '⟨ pending\n〈pending\n<pending\n⟨Pending\n⟨PENDING\n' | grep -c '⟨pending'
0
$ printf '⟨pending\n' | grep -c '⟨pending'
1
```

Consequence: the kill-rule clause enforces a single byte spelling, not the
semantic state ("no unfinished markers in the round lesson"). A pending item
written in any other spelling is a real defect (unfinished work in the round
lesson) that the kill rule does not fire on. Hardening suggestion: normalize
the marker lexicon (grep for a class: `⟨[[:space:]]*[Pp]ending`, plus ASCII
`<pending`, plus `〈pending`) and/or require the lesson's own "## Pending-marker
resolutions" table (round-39 precedent) to list the resolved markers by name.

Counterexample status: **escape reproduced** (the kill rule does not fire on a
respelled pending marker).
