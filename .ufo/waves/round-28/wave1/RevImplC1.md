# RevImplC1 — round-28 C1 review

**Verdict: CHANGES-REQUIRED** (reviewed frozen implementation bytes `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`, 523 lines; base `c9f8b115a098c65356e4b3b6048af45a37ab8395`). No `.diff` existed initially; the live file changed during review. ExecImplC1 confirmed this digest frozen and pointed to `.ufo/waves/round-28/wave1/ExecImplC1.diff`.

## Findings

1. **Frozen corpus-disclosure assertion is not reproduced.** The C1 claims freeze says four marked citations in `claim-gates.md`, `intake-and-finalize.md`, `mission-control.md`, and `source-tree-loss-2026-09-28.md` newly classify `LOST-RECORDED` after the CITE arm. Their cited provenance trailers are plain, unbackticked text: e.g. `claim-gates.md:123` is `source: [lost-tree] ~/Projects/bounties/ops/claim-check.mjs:1-233`; corresponding lines are `intake-and-finalize.md:109`, `mission-control.md:169`, and `source-tree-loss-2026-09-28.md:353`. The implementation still extracts tokens only via `TOK = re.compile(r"`([^`\n]+)`")` at `anchorcheck.py:152`, so these four trailers are never presented to CITE/LOST. I ran the instrument on all four: **0** `LOST-RECORDED` verdict lines for each (only their unrelated summary is emitted). This is not fixed by the new regex arm at `anchorcheck.py:159-166`; it only applies after token extraction. Do not silently widen the token model in this review; the frozen disclosure needs an appended correction or an explicitly scoped implementation decision before claiming C1 complete.

## Predicate review

- **(1) Exit contract:** `FAIL_CLASSES` at `anchorcheck.py:169-170` exactly lists MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT; `LOST-RECORDED` is absent. All six have a `kinds[...]` classification path (`:469-496`, plus BASE-ABSENT `:473-476`, BOUNTIES-ABSENT `:477-480`) and `main` returns 1 iff any listed count is nonzero (`:518-519`). IN-RANGE classes are not in the tuple. Verified: bad-fixture exits 1; bounties fixture prints one BOUNTIES-ABSENT line; a combined MISSING-FILE/PAST-EOF/PIN-BROKEN/OUTSIDE-BASE probe prints all four and exits 1; an IN-RANGE(PIN) control exits 0; a LOST-RECORDED-only control exits 0. SKILL.md exits 0 with `7 in-range cite instances, 0 bad`, LOST-RECORDED=306, PIN-BROKEN=0, OUTSIDE-BASE=0, BASE-ABSENT=0. The frozen bad-extraction sed emitted no result against the current summary syntax; the summary itself confirms `0 bad`.
- **(2) CITE arm and confinement:** `CITE` gains the explicit `~/Projects/bounties/` alternative at `anchorcheck.py:159-166`, with the existing province extension set. Root derives from `KASEGI_BOUNTIES` plus canonical `~/Projects/bounties` via `_derive_root` (`:147-149`, candidate declaration at `:128-130`). The new arm is confined exactly like MIRROR (names substituted):

  ```python
  # MIRROR, anchorcheck.py:394-405
  mirror_root = os.path.realpath(MIRROR)
  path = os.path.realpath(os.path.join(mirror_root, rel[len(MIRROR_CITE_PREFIX):]))
  try:
      within_mirror = os.path.commonpath((mirror_root, path)) == mirror_root
  except ValueError:
      within_mirror = False
  if not within_mirror:
      outside_root = mirror_root; verdict = 'OUTSIDE-BASE'
  elif MIRROR_ABSENT:
      verdict = 'BASE-ABSENT'
  elif not os.path.isfile(path):
      verdict = 'MISSING-FILE'
  else:
      kind = 'MIRROR'
  ```

  ```python
  # BOUNTIES, anchorcheck.py:408-424
  bounties_root = os.path.realpath(BOUNTIES_ROOT)
  path = os.path.realpath(os.path.join(bounties_root, rel[len(BOUNTIES_CITE_PREFIX):]))
  try:
      within_bounties = os.path.commonpath((bounties_root, path)) == bounties_root
  except ValueError:
      within_bounties = False
  if not within_bounties:
      outside_root = bounties_root; verdict = 'OUTSIDE-BASE'
  elif BOUNTIES_ABSENT:
      verdict = 'BOUNTIES-ABSENT'
  elif not os.path.isfile(path):
      verdict = 'MISSING-FILE'
  else:
      kind = 'BOUNTIES'
  ```

  This is the same realpath/commonpath confinement, including ValueError handling and ordering. The escaping-bounties fixture in selftest and my traversal probe both reached OUTSIDE-BASE.
- **(3) Selftest isolation:** `--selftest` builds nine independent temp-root subprocess cases and compares the complete fail-class/LOST/IN-RANGE vector plus exit code (`anchorcheck.py:185-300`). Six fixtures each target one FAIL_CLASSES member; three controls cover bounties in-range, marked loss, and clean lane in-range. Per-case environment overrides all four roots, and the pin case initializes its own temp git repo. The assertions are isolating by construction. Run result: `selftest cases=9 failures=0`, exit 0.
- **(4) LOST-RECORDED:** the token-level `if lost` classification remains before normal verdict classification at `anchorcheck.py:355-357,465-468`; it is not added to FAIL_CLASSES. The selftest's marked-loss case exits 0 and the live SKILL.md count remains 306. No change to this behavior found.
- **(5) Scope / drive-by:** the diff is confined to `anchorcheck.py`. Apart from C1 docs/comments, changes are the bounties root/CITE arm, FAIL_CLASSES and exit, and selftest/argument dispatch. The CITE refactor preserves the pre-existing alternatives and extension sets; `_PRINT_FIRST` preserves prior ordering while adding BOUNTIES-ABSENT. No unrelated behavior change found. Empty-argv usage handling is local to the new argument dispatch.

## Verification evidence and gap

At frozen digest `95333e29…`: bad-fixture exit 1; bounties-fixture `grep -c BOUNTIES-ABSENT` = 1; selftest `cases=9 failures=0` exit 0; SKILL.md exit 0 / 0 bad / LOST-RECORDED=306 / BASE-ABSENT=0 / PIN-BROKEN=0 / OUTSIDE-BASE=0. The live four-citation disclosure check returned 0 LOST-RECORDED lines for each of the four paths above. `.ufo/waves/round-28/c1-receipt-index.txt` was not present during this review, so the frozen receipt-index-at-digest predicate is not verified here (L1 must populate and check it against this sha256).
