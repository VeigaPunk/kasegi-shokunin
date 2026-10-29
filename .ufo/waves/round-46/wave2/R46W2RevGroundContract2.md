VERDICT: HOLDS

Scope: side-by-side check of re-ground rows G8-G14 of `corpus/knowledge/claim-package-contract.md`, section `## Re-ground (round 46)`, against committed anchor bytes. No overreach and no circular row was found, so the BROKEN rule does not fire. Three rows need a named edit before landing (G8, G11 re-anchor or disclose; G13 cell reword). Nothing was edited, committed or mutated in the lane.

Tree checked: lane commit 5437afeaf9b642c267bba3c31f00ae701e49da68. `cmp` against `git show 5437afe:<path>` was identical for `corpus/knowledge/claim-package-contract.md`, `corpus/instruments/claim-package-check.py`, `corpus/instruments/r46-c1-gate.py`, `corpus/instruments/fixtures/claim-package/exemplar/provenance.json` and `.../custodian-receipts.json`. HEAD is now 0d121a2 (wave-2 spec commit). `git diff --stat 5437afe HEAD -- <those paths>` is empty. `git diff --stat 914ca0b 5437afe -- corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` is empty, so the anchor code predates round 46 (the R43 gate).

## Row table

Entry lines (`sed -n '14,15p' corpus/knowledge/claim-package-contract.md`):
- l.14 (custodian-receipts): `Every action: nonempty \`matched_grant_id\` AND \`scope_signal\` exactly \`"NO_SCOPE_OBJECTION"\`. \`head_sha256\` == final decision digest == \`manifest.expected_head_sha256\`.`
- l.15 (provenance): `Agents + requested/resolved models per transition, commands + exit codes, pin (remote + commit), \`policy_sha256\`, \`external_effects_performed: []\`, secrets attestation.`

Anchor lines (`sed -n 'a,bp' corpus/instruments/claim-package-check.py`, numbers added by awk):

| row | entry line | anchor lines | class | evidence |
| --- | --- | --- | --- | --- |
| G8 | l.14 | 457-458 | narrow, undisclosed | 457 `grant = decision.get('matched_grant_id')`; 458 `if not isinstance(grant, str) or not grant.strip():`. The verdict is `if grant_miss: raise` at 475-476, outside the anchor. Probe N8 below: with 475-476 removed, all 21 rows stay green and the gate accepts a grant-less action. |
| G9 | l.14 | 467 | faithful | 467 `or head.lower() != final_digest.lower()):` is the condition of 465-468; 468 `raise _GateFail('chain=%d,head=mismatch' ...)`. `final_digest` is chain[-1] (463). |
| G10 | l.14 | 471 | faithful; verifiability note | 471 `if head.lower() != head_expected.lower():`; 472 raises `head-manifest=mismatch`. `head_expected` is `manifest.get('expected_head_sha256')` at 435, uncited. Probe N10: 435 repointed to another key, row stays green. |
| G11 | l.15 | 497 | narrow, undisclosed | 497 `for key in ('transition', 'requested_model', 'resolved_model'):` is the loop header only. The value test is 498-501 and the verdict is 539-540 (`if agent_bad: raise`), both outside the anchor. Probe N11 below: value test disabled, all 21 rows green, gate accepts an empty `requested_model`. |
| G12 | l.15 | 515-516 | narrow, disclosed (OK) | 515 `pin = document.get('pin')`; 516 `if not isinstance(pin, dict):`. The claim cell says "presence only" and points at 518-523, which is what the probes below confirm. |
| G13 | l.15 | 524-525 | faithful; claim-cell reword | 524 `policy = document.get('policy_sha256')`; 525 `if not isinstance(policy, str) or not HEX64.match(policy):`; 526 raises. The 64-hex requirement is in the gate, but l.15 names only `policy_sha256` and never says 64-hex. The cell attributes a gate rule to the entry. |
| G14 | l.15 | 527-528 | faithful | 527 `effects = document.get('external_effects_performed')`; 528 `if not isinstance(effects, list) or effects:`; 529 raises. Matches `[]` plus "any entry fails". |

Cross-cutting: the section header text (line 73) lists the provenance block, the round-13 boundary note (lines 18-27), the status census and the validation command as historical. It does not name the table at lines 7-16, which holds l.14 and l.15. The G8-G14 cells still quote those lines as "Entry l.N" current claims. Each cell is a sentence about the committed gate, so each should read "committed gate enforces: ...". Also, the boundary note at line 23 still says the provenance fields are "not machine gates", which contradicts G12-G14. Line 73 covers that text as historical but does not name the conflict.

## Findings

F1 (G8, narrow, undisclosed). Row cites 457-458 only; the enforcement is 475-476. Commands run, with outputs quoted:

```
per-entry counter, lane tree: row G8 ok=1 read=token-located ... reground entry=claim-package-contract.md rows=21 ok=21 files=4 distinct=1 exit=0
mutant N8 (475-476 replaced by pass; anchor 457-458 untouched):
  row G8 ok=1 read=token-located ... reground ... rows=21 ok=21 ... exit=0
  N8 gate on grant-absent package: 0 ['RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound']
control: committed gate on same grant-absent package
  RULE R-CUSTODIAN verdict=fail detail=chain=3,grant-miss=1   (exit 1)
```

Required edit: re-anchor G8 to 475-476 (token `if grant_miss:`, 14 chars, meets MIN_TOKEN 8), or state in the cell that 457-458 witnesses only the per-action test and the verdict is 475-476.

F2 (G11, narrow, undisclosed). Row cites the loop header only. Commands run:

```
mutant N11 (line 499 `if not isinstance(value, str) or not value.strip():` -> `if False:`; anchor 497 untouched):
  row G11 ok=1 read=token-located ... rows=21 ok=21 ... exit=0
  N11 gate on empty requested_model: 0 ['RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok']
control, committed gate on same package:
  RULE R-PROVENANCE verdict=fail detail=agents=2,agents-bad=1   (exit 1)
```

Required edit: re-anchor G11 to 497-501 plus 539-540, or disclose that 497 is the key list and the value test is uncited.

F3 (G10, faithful, verifiability note). Row token 471 compares against `head_expected`, sourced from 435 (uncited). Commands run:

```
mutant N10 (435 -> manifest.get('expected_head_sha256_renamed'); anchor 471 untouched):
  row G10 ok=1 read=token-located ... rows=21 ok=21 ... exit=0
  N10 gate on exemplar: 1 ['RULE R-CUSTODIAN verdict=fail detail=chain=3,manifest-head=bad']
```

The gate then rejects every package, so this is over-rejection, not silent acceptance. The row is blind to it. Optional: anchor 435-471 (span 36, within the 39-line cap).

F4 (G13, claim-cell reword). l.15 (quoted above) names `policy_sha256` with no format. The 64-hex rule is gate behaviour. Probes: `policy_sha256 = "abc"` gives `RULE R-PROVENANCE verdict=fail detail=policy_sha256=bad` (exit 1); a 64-hex uppercase digest gives `verdict=pass` (exit 0). Required edit: `Committed gate reads policy_sha256 as 64-hex (line 525); entry l.15 names the field only.`

F5 (G12, OK). Probes confirm the disclosed narrowing:
- pin absent: `RULE R-PROVENANCE verdict=fail detail=pin=absent` (exit 1)
- pin `{}`: `verdict=fail detail=pin=remote` (exit 1). Presence check 515-516 passes an empty dict, and 518-523 catch it.
- commit 6 hex `abc123`: `verdict=fail detail=pin=commit` (exit 1)
- commit 7 hex `abcdef1`: `verdict=pass` (exit 0)
The "7-64-hex" wording in the cell matches `HEX_ANY` (line 117).

F6 (G9, G14, faithful). Probes: final decision digest changed gives `RULE R-CUSTODIAN verdict=fail detail=chain=3,head=mismatch` (exit 1). `external_effects_performed = ["git push origin main"]` gives `external_effects_performed=not-empty` (exit 1). Cosmetic: an absent field also reports `not-empty` (`G14b`), which is misleading text but correctly fails.

F7 (circularity). No row is circular. No anchor reads the entry, and no row uses the exemplar fixture as its evidence (the exemplar is used only as a control here). The rows do show that the lane's own R43 gate implements the sentence. They do not show the lost `~/Projects/bounties` contract requires it. That is a claim-cell wording issue (cross-cutting note above), not a circularity.

## Controls (do-nothing and discriminating)

- Unmutated exemplar: `RULE R-CUSTODIAN verdict=pass ... head=bound`, `RULE R-PROVENANCE verdict=pass ... pin=ok,effects=none,secrets=ok`, `package=... rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`.
- Blanked tokens (lines 457 and 471 emptied in a scratch copy): `row G8 ok=0 read=token-not-in-lines`, `row G10 ok=0 read=token-not-in-lines`, `reground ... ok=19 ... exit=1`. The per-entry counter is not vacuous, but it only tests token presence.
- Base export 914ca0b (`/fast/scratch/hyaku/kasegi-r46/L1/pure`): `grep -c "## Re-ground (round 46)"` printed `0`; counter printed `reground entry=claim-package-contract.md rows=0 ok=0 exit=1 read=section-count=0`.

## Required edits (named, not made)

1. G8: re-anchor to 475-476 (or disclose the 457-458 scope). Cell as-is is narrow and silent.
2. G11: re-anchor to 497-501 + 539-540 (or disclose). Cell as-is is narrow and silent.
3. G13: reword the cell so the 64-hex rule is attributed to the committed gate, not to l.15.
4. G8-G14: reword "Entry l.N:" to "committed gate enforces:" (or add a disclosure line), because l.14-15 are lost-tree lines and line 73 does not name the table as current or historical.
5. Optional: G10 anchor 435-471.

## Limitations

- Lost-tree truth not checked: `~/Projects/bounties` is absent per the entry text, and I did not re-run any check against it. My verdict is on the committed bytes only.
- Scope is G8-G14 only. G1-G7 and G15-G21 were not reviewed.
- Aggregate `--baseline` run (L1-L7) and `claim-package-check.py --selftest` not run. Only the per-entry counter and the gate on constructed packages.
- Probes ran on copies of the R43 exemplar, which the lane authored, so C0 passing is consistency, not independent evidence.
- Counter v1.1 is a token-presence grader. The N8/N10/N11 results show it cannot see enforcement outside an anchor; that is why F1-F3 are semantic findings.
- Scratch `$HYAKU_SCRATCH/kasegi-r46/R46W2RevGroundContract2/` removed on exit. No git mutation, no commit, no push. Reads only.
