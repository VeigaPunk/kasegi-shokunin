# R48Review07 — Pre-freeze fixture receipt, independent verification

Seat: R48Review07 (reviewer, leaf; no subagent dispatch)
Scope: independently verify the pre-freeze fixture receipt (`controls/pre-freeze-fixtures.txt`, 17 cases) against the frozen source at commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` (claim C1, axis `depth:verifiability`).
Skill: godspeed. Report-only; no production, fleet, sibling, or git/jj state mutated.

## Verdict

**Pre-freeze fixture receipt VERIFIED.** All 17/17 cases independently reproduce against the frozen checker source: observed exit and finding match the frozen receipt on every line, and match the per-fixture `exit` field frozen in `controls/fixtures.json`. 0 mismatches.

This verifies the receipt as a measurement of the frozen instrument. Per claim C1's own mechanical limits, this is author-side form validation only — not promotion, not evidence truth.

## Frozen-anchor integrity (all hashes independently recomputed)

| Artifact | Frozen commit `3546f70` | Worktree disk | Match |
|---|---|---|---|
| `controls/fixtures.json` | `10d2aa79…c0cbb288` | `10d2aa79…c0cbb288` | yes |
| `controls/pre-freeze-fixtures.txt` | `3a41198f…f18e57` | `3a41198f…f18e57` | yes |
| `controls/shonen-before.txt` | `596122c0…17e9c05` | `596122c0…17e9c05` | yes |
| `controls/canonical-candidate.txt` | `b476c7aa…a4de4b8c` | `b476c7aa…a4de4b8c` | yes |
| `controls/do-nothing.txt` | `34fd5e88…b7724f5c` | `34fd5e88…b7724f5c` | yes |
| `controls/pre-freeze-mutants.txt` | `fe93dd8e…bde549475` | `fe93dd8e…bde549475` | yes |
| `controls/census-before.txt` | `584e3103…12033e804` | `584e3103…12033e804` | yes |
| `controls/protocol-source.txt` | `622b29a0…b1739fd0` | `622b29a0…b1739fd0` | yes |
| `corpus/instruments/shonen-form.py` | `0ab32a2c…77b313dd` | `0ab32a2c…77b313dd` | yes |

`git merge-base --is-ancestor 3546f70 HEAD` → true (frozen commit is an ancestor of the integrated HEAD `3d7e042`); `git fsck --no-dangling` clean. The worktree checker is byte-identical to the frozen checker, so no "checker source amendment after seat scoring" condition exists as of this measurement.

Cross-anchors inside the frozen controls (independently recomputed, not just trusted):
- `actual-r47-drift` fixture text sha256 = `596122c0…17e9c05` = `shonen-before.txt` = `git show 903d47e:SHONEN.md`. The drift fixture genuinely is the round-47 base bytes; the archive control retains the exact pre-restore historical bytes, satisfying the kill rule's restoration clause.
- `canonical` fixture text sha256 = `b476c7aa…a4de4b8c` = `canonical-candidate.txt`.
- `shonen-before.txt` carries exactly 52 `- [~]` author marks, matching claims.json `before` ("52 author marks and accumulated assessment blocks").

## Method (independent re-run)

Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Review07/` (created, driver + fixture trees + receipts kept there; removed on exit after this report landed).

Driver: `verify_fixtures.py` (scratch-owned) — for each of the 17 fixtures in the frozen `fixtures.json`, writes the fixture text to an isolated tree `runs/<case>/SHONEN.md` with a stub `LOG.md` (required so the checker's evidence-pointer limb resolves), runs the frozen checker, and compares observed `(exit, finding)` against both the frozen receipt line and the fixture's own `exit` field.

Exact command:

```
python3 /fast/scratch/hyaku/kasegi-r48/R48Review07/verify_fixtures.py
```

## Per-case results: expected vs observed

Frozen checker: `python3 shonen-form.frozen.py --root runs/<case>` (source `0ab32a2c…77b313dd`). All observed values are this seat's fresh measurements, not quoted outputs.

| case | receipt expected | fixtures.json exit | observed | result |
|---|---|---|---|---|
| canonical | 0 SF-CLEAN | 0 | 0 SF-CLEAN | PASS |
| actual-r47-drift | 1 SF-PREAMBLE | 1 | 1 SF-PREAMBLE | PASS |
| missing-file | 1 SF-NEWLINE | 1 | 1 SF-NEWLINE | PASS |
| fenced | 1 SF-PREAMBLE | 1 | 1 SF-PREAMBLE | PASS |
| commented | 1 SF-PREAMBLE | 1 | 1 SF-PREAMBLE | PASS |
| duplicate | 1 SF-TRAILING | 1 | 1 SF-TRAILING | PASS |
| extra-prose | 1 SF-TRAILING | 1 | 1 SF-TRAILING | PASS |
| crlf | 1 SF-NEWLINE | 1 | 1 SF-NEWLINE | PASS |
| no-newline | 1 SF-NEWLINE | 1 | 1 SF-NEWLINE | PASS |
| wrong-label-0 | 1 SF-BOX | 1 | 1 SF-BOX | PASS |
| missing-evidence-0 | 1 SF-EVIDENCE | 1 | 1 SF-EVIDENCE | PASS |
| wrong-label-1 | 1 SF-BOX | 1 | 1 SF-BOX | PASS |
| missing-evidence-1 | 1 SF-EVIDENCE | 1 | 1 SF-EVIDENCE | PASS |
| wrong-label-2 | 1 SF-BOX | 1 | 1 SF-BOX | PASS |
| wrong-label-3 | 1 SF-BOX | 1 | 1 SF-BOX | PASS |
| missing-evidence-3 | 1 SF-EVIDENCE | 1 | 1 SF-EVIDENCE | PASS |
| missing-evidence-2 | 1 SF-EVIDENCE | 1 | 1 SF-EVIDENCE | PASS |

Driver summary line: `SUMMARY cases=17 mismatches=0`, driver exit 0.

The 17 cases exercise each rejection class of the frozen grammar exactly once per limb: newline hygiene (CRLF, missing final newline, empty file), preamble exactness (fenced, commented — the "hidden/commented checklist" kill-rule shapes), trailing bytes (duplicate seed, extra prose), box label/mount integrity (4× wrong-label → SF-BOX, 4× missing evidence → SF-EVIDENCE), the positive canonical case, and the true round-47 drift.

## Corroborating bounded probes (same frozen checker, fresh runs)

1. **Do-nothing / expect_before.** Command: `python3 shonen-form.frozen.py --root probes/base` where `probes/base/SHONEN.md = git show 903d47e:SHONEN.md`. Observed: `shonen-form canonical=0 finding=SF-PREAMBLE exit=1`, probe exit 1 — byte-identical to the frozen `controls/do-nothing.txt` content and to claims.json `expect_before`.
2. **expect_after at the integrated HEAD.** Command: `python3 shonen-form.frozen.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (worktree = HEAD `3d7e042` for SHONEN.md; `git status` shows SHONEN.md unmodified). Observed: `shonen-form canonical=1 finding=SF-CLEAN exit=0`, exit 0 — matches claims.json `expect_after` and the `after` cell. The kill rule's "canonical=0 at final measured revision" limb does not fire.
3. **`[x]` rejection (mechanical limit "x marks are rejected").** Variant of the canonical fixture with `[~]→[x]`. Command: `python3 shonen-form.frozen.py --root probes/xmark`. Observed: `canonical=0 finding=SF-VERIFIER exit=1`. Independence is not mechanically attestable — consistent with the protocol's Promotion gates and the claim's mechanical limits.
4. **Evidence-pointer existence check.** Canonical fixture with `Evidence: LOG.md` → `Evidence: NOPE.md` (nonexistent). Command: `python3 shonen-form.frozen.py --root probes/badptr`. Observed: `canonical=0 finding=SF-POINTER exit=1`. The checker verifies pointer existence under the declared root, not semantic truth — as the predicate states.
5. **Ancestry/landedness.** `git merge-base --is-ancestor 3546f70 HEAD` → true; the frozen controls tree is byte-stable on disk at this seat's measurement.

## Observations (neutral — no kill-rule limb fires)

- **Landed SHONEN.md ≠ frozen canonical candidate, but is grammar-conformant.** HEAD `SHONEN.md` sha256 `b1352168…a46d0` vs canonical-candidate `b476c7aa…a4de4b8c`. Differences: box 2 mark `[ ]` (unchecked) instead of `[~]`; evidence pointers `SKILL.md` / `corpus/lessons/round-47-verifier-spotcheck.md` / `PROVINCE.md` instead of all-`LOG.md`. The checker's grammar (`- \[([ ~x])\]` + optional 6-space-indented `Evidence:` line with a root-relative pointer) accepts both shapes, so C1's after-state (`canonical=1 SF-CLEAN exit=0`) holds at the final measured revision. The deviation is a content choice inside the canonical grammar, not a form defect; noted for the integrator's awareness, not routed.
- The checker's positive grammar also accepts a fully `[ ]`-unchecked file, and accepts any root-relative existing file as the evidence pointer. Both are per the frozen predicate ("author-assessment grammar with existing local evidence pointers … form validation, not … evidence truth"), not escape hatches: the `[x]`→SF-VERIFIER limb and pointer-existence limb are exactly what keeps promotion semantics out of the author-side checker.

## Residual risk and verification gaps

- **Mutants receipt not re-executed.** `pre-freeze-mutants.txt` (6 checker-source mutants, all `caught=1`, divergent_cases 3+2+3+4+4+1=17) is hash-verified frozen and internally consistent with the 17-case count, but the mutant checker bodies are not frozen in `controls/`, so this seat could not re-run them without fabricating mutant sources. Gap named, not worked around.
- **Round-47 R2 (plain-target phrasing)** is explicitly out of C1's scope (C1 closes R1 only); R2's frozen targets remain unrepaired by design of this round and were not probed here beyond confirming the round-47 spot-check lesson (`corpus/lessons/round-47-verifier-spotcheck.md:86`) is the route of record.
- The receipt verifies form only. Semantic evidence and promotion remain independently judged per the claim; this seat expresses no opinion on them.
- Worktree SKILL.md shows an unrelated in-flight modification (`git status`: `M SKILL.md`) owned by another seat; not touched, not probed, not part of this receipt's surfaces (the checker reads only `SHONEN.md` and the evidence pointers it names).

## Receipt commands (for re-derivation)

```
# frozen extraction (all under scratch, read-only on the repo)
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 3546f70:corpus/instruments/shonen-form.py
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 3546f70:.ufo/waves/round-48/controls/{fixtures.json,pre-freeze-fixtures.txt,shonen-before.txt,canonical-candidate.txt,do-nothing.txt}
# independent 17-case re-run
python3 /fast/scratch/hyaku/kasegi-r48/R48Review07/verify_fixtures.py   # -> SUMMARY cases=17 mismatches=0
```

## Trend verdicts

Not applicable to a bounded review seat (no lane axis measurement claimed). No score moves.
