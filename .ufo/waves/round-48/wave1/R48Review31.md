# R48Review31 — Frozen kill-rule archival review + integrated-candidate shape-test review

Seat: R48Review31 (reviewer, leaf — no dispatch). Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Frozen claim: `.ufo/waves/round-48/claims.json` sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2c345` (matches `freeze.txt` `claims-sha256` — verified). Base `903d47e13058982460f0d90c1c2b9c7c02680646`; final measured revision `3d7e042`.
Scope: the C1 kill rule's three archival/entrapment prongs, and whether the one-wave shape battery tested the integrated candidate or a hypothetical draft. Round-47 routes R1 (checklist canonical-form drift, 52 marks) and R2 (prose-sensitive count) read via `corpus/lessons/round-48.md` and round-47 controls. No production file, fleet, sibling, domain tree, or git/jj state touched. No installs. No delegation. No commit.

## Verdict

**Claim C1 survives its frozen kill rule on all three prongs (re-produced below). One non-killing coverage finding: the frozen shape battery's positive control is the pre-freeze draft bytes, not the integrated candidate bytes; the integrated shape that actually shipped (blank `[ ]` box with an evidence line) is covered by zero fixtures. Mitigated by a direct counter run on the integrated bytes and by `measure.py` measuring the actual integrated revision — the claim's expected-after holds.**

## Kill-rule prong 1 — canonical=0 at final measured revision

Expected-after (claims.json): `shonen-form canonical=1 finding=SF-CLEAN exit=0`.

Observed (re-run, exact commands):

```
$ python3 .ufo/waves/round-48/measure.py --root . --base 903d47e13058982460f0d90c1c2b9c7c02680646 --after 3d7e042 --work /fast/scratch/hyaku/kasegi-r48/R48Review31
before: shonen-form canonical=0 finding=SF-PREAMBLE exit=1 process_exit=1
before-plain: {"checklist_lines": 356, "boxes": 52, "checklist_sha256": "596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05"}
after: shonen-form canonical=1 finding=SF-CLEAN exit=0 process_exit=0
after-plain: {"checklist_lines": 12, "boxes": 4, "checklist_sha256": "b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0"}
frozen-counter-sha256: 0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd
```

- Before-state matches `expect_before` and the do-nothing control byte-for-byte in verdict (`controls/do-nothing.txt` = `SF-PREAMBLE exit=1`).
- After-state matches `expect_after`. Working-tree `SHONEN.md` sha256 `b1352168…` == `git show HEAD:SHONEN.md` == the `after-plain` digest — nothing uncommitted on this surface.
- Frozen counter integrity: `shonen-form.py` sha256 `0ab32a2c…` identical across the freeze commit (`git show 3546f70:corpus/instruments/shonen-form.py`), `HEAD`, and the working tree. No post-freeze checker amendment; kill-rule clause "a checker source amendment after seat scoring cannot validate this frozen claim" not implicated.
- **Prong status: PASS.**

## Kill-rule prong 2 — tested hidden/commented/duplicate checklist passes the frozen checker

Re-ran all 17 fixtures from `controls/fixtures.json` through the frozen counter (`--file /dev/stdin`). Recorded exit == actual exit for 17/17. The entrapment shapes the kill rule names:

| fixture | recorded | observed | finding |
|---|---|---|---|
| `fenced` | 1 | 1 | SF-PREAMBLE |
| `commented` | 1 | 1 | SF-PREAMBLE |
| `duplicate` | 1 | 1 | SF-TRAILING |
| `extra-prose` | 1 | 1 | SF-TRAILING |

No tested hidden/commented/duplicate checklist passes. `controls/pre-freeze-fixtures.txt` (frozen in commit `3546f70`) records the same 17 expectations, so the committed record matches live counter behavior. The integrated tree file itself is 12 lines with no comments, fences, or duplicate checklists. Six checker-source mutants (`pre-freeze-mutants.txt`: preamble/trailing/newline/box/evidence/label-count, all `caught=1`) are tallied but their mutant inputs are not retained — not independently re-runnable (see Gaps).
- **Prong status: PASS.**

## Kill-rule prong 3 — restoration loses historical bytes (archive SHA256 596122c0…)

Required archive digest `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05`.

- `sha256sum .ufo/waves/round-48/controls/shonen-before.txt` → `596122c0…` (frozen in commit `3546f70`). The 356-line drift (52 marks) is retained byte-for-byte.
- `git show 903d47e:SHONEN.md | sha256sum` → `596122c0…` — git history independently retains the identical bytes; the archive does not depend on a single control file.
- LOG.md round-48 entry names the retention pointer; `corpus/lessons/round-48.md` M48-1 cites it.
- **Prong status: PASS.**

## Finding 1 (medium, non-killing): one-wave shape battery tested the hypothetical draft, not the integrated candidate

The claim's milestone language is "integrated candidate and 64 distinct bounded probes/reviews", and this seat was asked to check whether the one-wave shape tests exercised the integrated candidate.

Observed byte identities:

| surface | sha256 |
|---|---|
| integrated `SHONEN.md` (working tree == `HEAD` == measure `after`) | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` |
| `controls/canonical-candidate.txt` (pre-freeze draft) | `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c` |
| fixtures.json positive control `canonical` | `b476c7aa…` — byte-identical to the draft |
| fixtures.json `actual-r47-drift` | `596122c0…` — byte-identical to the frozen archive |

- The battery's only positive fixture is the pre-freeze **draft**; **no fixture equals the integrated candidate bytes** (`fixtures equal to integrated tree bytes: NONE`, computed over all 17).
- The integration commit `3d7e042` ("restore canonical checklist") did not ship the draft verbatim. Concrete draft→integrated deltas: box 2 mark `[~]`→`[ ]` with evidence line retained; box 1 evidence pointer `LOG.md`→`SKILL.md`; box 3 pointer `LOG.md`→`corpus/lessons/round-47-verifier-spotcheck.md`; box 4 pointer `LOG.md`→`PROVINCE.md`. All four pointers resolve at `HEAD` (and in the measure sandbox's 5-path export set — `measure.py` exports exactly the surfaces the integrated file cites).
- Consequence: had the integration edit introduced a form defect the draft lacks, the frozen battery would not have caught it; the committed battery's `canonical` positive control certifies bytes that are not what shipped.

Mitigation (why this does not kill C1):
- The frozen counter run directly on the integrated bytes: `shonen-form canonical=1 finding=SF-CLEAN exit=0` (re-run this seat, stdin-fed).
- `measure.py`'s `after` leg measures the actual integrated revision (`3d7e042`), not the draft — the claim's scored after-state is about the tree, and it holds.
- The kill rule's three prongs are all tree/history-facing, and all pass.

Recommendation (for the integrator, not executed by this seat): add a fixture equal to the integrated `b1352168…` bytes as the positive control, or record in the round notes that the frozen battery's positive control is the draft and that integrated-byte coverage is supplied by the measure harness `after` leg.

## Finding 2 (low): integrated candidate uses a mark shape with zero fixture coverage

The integrated box 2 is `- [ ] At least one end-to-end domain task…` followed by an evidence line. The frozen checker accepts mark class ` ` (evidence optional; if present, pointer must resolve). None of the 17 fixtures contains a `- [ ]` mark in any position — every positive/mutation baseline uses `[~]`. So the shipped file's most distinctive grammatical feature (unchecked box carrying an author-note evidence line) is untested by the battery. The frozen counter accepts it (verified on integrated bytes and on the live tree); the protocol template shows `- [ ]` only as the bare seed state, so the checker's grammar is the binding authority for this form-only claim and it is not violated. Not a kill; a coverage note.

## Minor observations (no action)

- `missing-file` fixture name vs behavior: it actually triggers `SF-NEWLINE` (its text ends without `\n`); recorded exit 1 agrees with the counter, so the expectation is sound — only the name is misleading.
- Working tree carries an in-flight sibling edit ` M SKILL.md` (not this seat's; untouched). Box 1's evidence pointer resolves both at `HEAD` and in the working tree, and all frozen measurements are per-commit (`git show`), so verdicts are unaffected.
- `census-before.txt` exit 0; LOG round-48 entry's "seventeen tree probes and six source mutants" matches the frozen counts (17 fixtures, 6 mutants).
- Do-nothing control re-verified: `do-nothing.txt` = `SF-PREAMBLE exit=1` == measure `before` verdict.

## Residual risk and verification gaps

1. **Mutant tally not re-runnable.** `pre-freeze-mutants.txt` commits only `caught=1` summaries; the six checker-source mutant bodies are not retained under `controls/`, so a non-author cannot re-execute the mutation-testing claim. The 17-fixture battery is fully re-runnable and agrees.
2. **Draft-vs-integrated divergence relied on integrator discipline.** Because the battery's positive control is the draft, correctness of the integrated bytes rests on the measure harness and ad-hoc runs (both green here), not on the frozen fixture set. Any future edit to `SHONEN.md` that keeps 4 boxes but drifts in a fixture-uncovered dimension (e.g., blank-mark evidence handling) would pass the battery's positive control unchanged.
3. **Form-only scope honored.** This review validates author-side grammar, pointer existence, and byte archival only — not semantic evidence truth, promotion, or independent-verifier identity, which the claim itself excludes (`mechanical_limits`).

## Evidence index (all commands run this seat, 2026-10-30)

- `sha256sum .ufo/waves/round-48/claims.json` → `b8022cdf…` (== `freeze.txt`).
- `python3 .ufo/waves/round-48/measure.py --root . --base 903d47e13058982460f0d90c1c2b9c7c02680646 --after 3d7e042 --work <scratch>` → before `SF-PREAMBLE exit=1`, after `SF-CLEAN exit=0` (full output quoted in prong 1).
- 17-fixture battery re-run via `python3 corpus/instruments/shonen-form.py --root . --file /dev/stdin` (table above; 0 mismatches).
- Integrated-vs-draft byte identities and fixture-membership check via `python3` + `hashlib` (tables above); `diff SHONEN.md controls/canonical-candidate.txt` (four box-level deltas listed).
- `git show 903d47e:SHONEN.md | sha256sum` → `596122c0…`; `git diff 3546f70 3d7e042 --stat` for the integration delta; `git show 3546f70:corpus/instruments/shonen-form.py | sha256sum` → `0ab32a2c…` (counter frozen).

Scratch receipts were written under `/fast/scratch/hyaku/kasegi-r48/R48Review31/` and the directory was removed on exit per seat spec; receipt contents are quoted verbatim in this report.
