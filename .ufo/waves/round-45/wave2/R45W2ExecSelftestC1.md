VERDICT: DRAFT-READY

Seat R45W2ExecSelftestC1 — selftest for counter v1.1 (C1, `corpus/instruments/r45-routed-defects.py`).
Draft: `.ufo/waves/round-45/wave2/R45W2ExecSelftestC1.draft/r45-counters-selftest-c1.py` (stdlib, 80 mutants + 5 controls, `--lane` default = the lane, `--base`, `--counter`, `--only`, `--jobs`, `--keep`). Counter not edited.
Attacked: export of `6662a4276b6f7bd61e23e12058414e09dd71b9e4` (`git archive … | tar -x`), baseline = `/fast/scratch/hyaku/kasegi-r45/L1/pure`.

## Command and printed result
`TMPDIR=<scratch>/tmp python3 …/r45-counters-selftest-c1.py --lane <export>` — wall 40 s, exit 1. Last stdout line:

    selftest cases=85 failures=7

(85 = 5 controls + 80 mutants; 71 `verdict=rejected`, 7 FALSE-GREEN failures, 2 `info-accepted` not counted.) Full case lines are quoted below.

## Design (how v1.1 pins are satisfied)
- GOOD tree = base export + synthetic artifacts (own freeze-check.py with an 8-case real selftest, r44-frontier-count.py patched with an 8-case real selftest, S072 row inside `## Registry`, a correction that quotes a located S072 span, R47-R49 rows >=300 chars with in-range `round-44.md:<n>` refs, SKILL registry table, README row; S071/S072/manifest/claims.json/refiled receipt copied from `--lane`).
- Pins computed from those artifacts, written to a grader-side JSON and passed as `R45_PINS_OVERRIDE`. Printed: `synthetic pins (R45_PINS_OVERRIDE): S072.txt=364166c4a23e claims.json=bbe40503281c freeze-check.py=8b7f54184a75 r44-frontier-count.py=48a916fcb719 r44-routed-defects.py=d5438c67befa refiled-body=03fe3af53006`. GOOD counter output: `limb R1..R5 fixed=1 … routed-defects total=5 fixed=5 unresolved=0 exit=0`.
- Pin-limb mutants keep the GOOD pins; behaviour mutants (7/8-case selftest counts, selftest failure, replay-short claims) re-pin only the mutated artifact, so token/replay limbs are tested in isolation.
- A mutant is `rejected` only if: target limb fixed=0, its `read=` token matches the intended reason regex (`WRONG-REASON` otherwise), total drops by exactly 1 (+declared coupled), no collateral limb, counter rc=1, and the tree really differs from GOOD (inode+bytes walk).

## Controls (do-nothing discrimination)
    case control-good-tree verdict=ok total_fixed=5 rc=0 … R1=1 R2=1 R3=1 R4=1 R5=1
    case control-do-nothing-base verdict=ok total_fixed=0 rc=1 expect fixed=0 (pins override active)
    case control-null-mutant verdict=ok total_fixed=5 unchanged clone must stay fixed=5 …
    case control-marker-only verdict=ok total_fixed=0 prose markers only, no artifacts: expect fixed=0
    case control-good-tree-under-real-pins verdict=ok … R3=0(r44-frontier-count-not-the-pinned-bytes) R4=0(freeze-check-not-the-pinned-bytes) R1=1 R2=1 R5=1(real receipt)
The last control shows the real pins genuinely bind the code: the synthetic code is rejected without the override.

## FALSE-GREENS the v1.1 counter fails to reject (the findings)
Verbatim from the run (`FALSE-GREEN …` lines):
FALSE-GREEN mutant=r1-flip-vacuous-tbd limb=R1 recipe: S072 flip clause reduced to the vacuous `flip: tbd` (wave-1 probe; predicate: a checkable flip clause) | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r1-flip-vacuous-colon-dot limb=R1 recipe: S072 flip clause reduced to `flip: .` | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r2-row-in-code-fence limb=R2 recipe: R49 row wrapped in ``` fences inside the Round-45 block (a fenced line is not a criterion row) | counter read: limb R2 fixed=1 read=criteria=3 total=5
FALSE-GREEN mutant=r2-row-in-html-comment limb=R2 recipe: R49 row wrapped in an HTML comment inside the Round-45 block | counter read: limb R2 fixed=1 read=criteria=3 total=5
INFO-ACCEPTED (not counted) mutant=r2-padded-filler-criterion limb=R2 recipe: INFO: R48 criterion padded with 400 chars of filler to pass the length floor (class word + any file + a ref) | counter read: limb R2 fixed=1 read=criteria=3
INFO-ACCEPTED (not counted) mutant=r2-enforced-by-unrelated-file limb=R2 recipe: INFO: R47 enforced-by names LOG.md (an existing file that enforces nothing); predicate as written asks only that the path exists | counter read: limb R2 fixed=1 read=criteria=3
FALSE-GREEN mutant=r3-registry-row-in-code-fence limb=R3 recipe: wave-registry.py registry row wrapped in ``` fences inside the section (a fenced line is not a table row) | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5
FALSE-GREEN mutant=r3-registry-row-in-html-comment limb=R3 recipe: wave-registry.py registry row wrapped in an HTML comment inside the section | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5
FALSE-GREEN mutant=r3-readme-row-in-code-fence limb=R3 recipe: instruments README row for r44-frontier-count.py wrapped in ``` fences | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5

Interpretation / location in the counter (`r45-routed-defects.py` @6662a42):
1. **Vacuous flip (R1)** — `flip: tbd` and `flip: .` accepted. `:158 if not re.search(r"flip:\s*\S", teaches)` tests only that one non-space char follows `flip:`; the claimed "checkable flip clause" is not checked. Two mutants, both fixed=1 with rc 0 (R1 `read=S072=supersedes recheck-quotes=2 corrections=1`). Wave-1 reported this for v1; v1.1 did not change the regex.
2. **R2 rows in a code fence / HTML comment** — `:213 lines = [ln for ln in tail.splitlines() if re.match(r"^\|\s*R4x\s*\|", ln)]` runs on raw text; R49 row wrapped in ``` or `<!-- -->` still counts (`criteria=3`). R1 gained `registry_lines()` fence/comment stripping; R2 did not.
3. **R3 SKILL.md registry row inside a fence / comment** — `:259-263` match rows on `m.group(0)` without stripping fences/comments: `registry-row` wave-registry.py wrapped in ``` or `<!-- -->` still counts (R3 stays fixed=1, `selftest-cases=8`).
4. **R3 README row inside a fence** — `:267 re.search(r"^\|\s*`?r44-frontier-count\.py`?\s*\|", rd_, re.M)` matches a fenced row (fixed=1).
Not counted (INFO, beyond the literal predicate — the predicate only asks that the path exist / criterion name its class): a 400-char filler R48 criterion naming `enforced-by: LOG.md` passes (`r2-padded-filler-criterion`), and `enforced-by: LOG.md` on R47 passes (`r2-enforced-by-unrelated-file`): the >=300 length floor and path-exists test do not bind content.

## What v1.1 limbs DO reject (71 mutants, each with the intended reason)
Code byte flipped (behaviour-identical, pin kept): `r3-code-byte-flipped`, `r3-code-trailing-newline`, `r4-code-byte-flipped`, `r5-r44-counter-edited` -> `…-not-the-pinned-bytes`; stubs printing the tokens (`r3-stub-selftest`, `r4-stub-freeze-check`) -> pin; self-consistent forged snapshot with manifest/row re-pinned (`r1-forged-snapshot-self-consistent`, source-recheck passes) -> `snapshot-not-the-pinned-capture-or-not-in-anchor`; claims weakened/changed/newline/absent -> `claims-not-the-frozen-bytes`; claims changed + re-pinned -> `replay-rc=1`; S072 row in a fence, HTML comment, under `## Paths`, 4-space indented, 10 cells -> `row-S072=absent`; criterion too short, line ref :9999 / :0 / absent -> `R47-criterion-too-short`, `R48-line-refs-absent-or-out-of-range`; receipt body edited / line deleted / extra line / hand-typed / cases=19 -> `receipt-body-not-the-pinned-run-output`; correction without located quote, wrong size, content-free, indented -> `lesson-correction-absent-or-quotes-no-located-S072-span`; behaviour selftests 7 cases / failures=1 / 5 cases (re-pinned) -> `selftest-rc=…-tokens=(7, 0)|(8, 1)|(5, 0)`. Wave-1 mutants kept (all 5 limbs); none dropped as moot except the wave-1 "row in fence at end of SOURCES.md", subsumed by the stricter in-place fence + under-`## Paths` mutants (both rejected). Wave-1 `r3-stub-selftest`/`r4-stub-freeze-check`/`r4-claims-weakened`/`r5-fabricated-receipt` were false-green probes under v1; under v1.1 they are rejected by pin (shown above), so they stay as regression cases.

## Full case lines
```
synthetic pins (R45_PINS_OVERRIDE): S072.txt=364166c4a23e claims.json=bbe40503281c freeze-check.py=8b7f54184a75 r44-frontier-count.py=48a916fcb719 r44-routed-defects.py=d5438c67befa refiled-body=03fe3af53006
GOOD counter output:
  limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
  limb R2 fixed=1 read=criteria=3
  limb R3 fixed=1 read=selftest-cases=8
  limb R4 fixed=1 read=selftest-cases=8 replay=base_ok=2
  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
  routed-defects total=5 fixed=5 unresolved=0 exit=0
case control-good-tree verdict=ok total_fixed=5 rc=0 expect fixed=5 R1=1 R2=1 R3=1 R4=1 R5=1
case control-do-nothing-base verdict=ok total_fixed=0 rc=1 expect fixed=0 (pins override active)
case control-null-mutant verdict=ok total_fixed=5 unchanged clone must stay fixed=5 (harness does not flag everything)
case control-marker-only verdict=ok total_fixed=0 prose markers only, no artifacts: expect fixed=0
case control-good-tree-under-real-pins verdict=ok no override: the synthetic code must NOT satisfy the real pins; R1=1(S072=supersedes recheck-quotes=2 corrections=1) R2=1(criteria=3) R3=0(r44-frontier-count-not-the-pinned-bytes) R4=0(freeze-check-not-the-pinned-bytes) R5=1(refiled=pinned-run-output
case r1-snapshot-byte-flipped limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/source-snapshots/round-45/S072.txt read=recheck-rc=1-quotes=0
case r1-manifest-quote-dropped limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/source-snapshots/round-45/manifest.json read=recheck-rc=0-quotes=1
case r1-forged-snapshot-self-consistent limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md,corpus/source-snapshots/round-45/S072.txt,corpus/source-snapshots/round-45/manifest.json read=snapshot-not-the-pinned-capture-or-not-in-anchor
case r1-anchor-sha-wrong limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=snapshot-not-the-pinned-capture-or-not-in-anchor
case r1-s070-row-edited limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=S070-row-changed-or-baseline-absent
case r1-s070-row-duplicated limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=S070-row-changed-or-baseline-absent
case r1-teaches-not-supersedes limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=teaches-not-supersedes
case r1-status-admitted limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=status=admitted
case r1-flip-clause-removed limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=flip-absent
case r1-flip-vacuous-tbd limb=R1 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=corpus/SOURCES.md read=S072=supersedes recheck-quotes=2 corrections=1
case r1-flip-vacuous-colon-dot limb=R1 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=corpus/SOURCES.md read=S072=supersedes recheck-quotes=2 corrections=1
case r1-size-token-absent limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=size-token-absent
case r1-row-in-code-fence limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=row-S072=absent
case r1-row-in-html-comment limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=row-S072=absent
case r1-row-after-registry limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=row-S072=absent
case r1-row-indented-code-block limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=row-S072=absent
case r1-row-10-cells limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/SOURCES.md read=row-S072=absent
case r1-correction-wrong-size limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/lessons/round-44.md read=lesson-correction-absent-or-quotes-no-located-S072-span
case r1-correction-content-free limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/lessons/round-44.md read=lesson-correction-absent-or-quotes-no-located-S072-span
case r1-correction-quote-unlocated limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/lessons/round-44.md read=lesson-correction-absent-or-quotes-no-located-S072-span
case r1-correction-quote-absent limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/lessons/round-44.md read=lesson-correction-absent-or-quotes-no-located-S072-span
case r1-correction-indented limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/lessons/round-44.md read=lesson-correction-absent-or-quotes-no-located-S072-span
case r1-lesson-not-append-only limb=R1 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/lessons/round-44.md read=round-44-lesson-not-append-only
case r2-enforced-by-missing limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R48-enforced-by-not-a-file-corpus/instruments/does-not-exist.py
case r2-enforced-by-directory limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R47-enforced-by-not-a-file-corpus
case r2-enforced-by-absent limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R49-enforced-by-absent
case r2-quality-prefix-edited limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=quality-not-append-only-or-unchanged
case r2-r49-ungrounded limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R49-ungrounded
case r2-duplicate-heading limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=round-45-heading!=1
case r2-r47-lacks-before-data limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R47-missing-before data
case r2-r48-lacks-presence-only limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R48-missing-presence-only
case r2-row-duplicated limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R48-rows=2
case r2-criterion-too-short limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R47-criterion-too-short
case r2-line-ref-out-of-range limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R48-line-refs-absent-or-out-of-range
case r2-line-ref-zero limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R48-line-refs-absent-or-out-of-range
case r2-line-ref-absent limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R49-line-refs-absent-or-out-of-range
case r2-vacuous-criterion limb=R2 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/QUALITY.md read=R48-criterion-too-short
case r2-row-in-code-fence limb=R2 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=corpus/QUALITY.md read=criteria=3
case r2-row-in-html-comment limb=R2 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=corpus/QUALITY.md read=criteria=3
case r2-padded-filler-criterion limb=R2 target_fixed=1 total_fixed=5 rc=0 verdict=info-accepted changed=corpus/QUALITY.md read=criteria=3
case r2-enforced-by-unrelated-file limb=R2 target_fixed=1 total_fixed=5 rc=0 verdict=info-accepted changed=corpus/QUALITY.md read=criteria=3
case r3-code-byte-flipped limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-frontier-count.py read=r44-frontier-count-not-the-pinned-bytes
case r3-code-trailing-newline limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-frontier-count.py read=r44-frontier-count-not-the-pinned-bytes
case r3-frontier-absent limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-frontier-count.py read=r44-frontier-count-not-the-pinned-bytes
case r3-stub-selftest limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-frontier-count.py read=r44-frontier-count-not-the-pinned-bytes
case r3-selftest-7-cases limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-frontier-count.py read=selftest-rc=0-tokens=(7, 0)
case r3-selftest-failure limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-frontier-count.py read=selftest-rc=1-tokens=(8, 1)
case r3-registry-row-7-cells limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=SKILL.md read=registry-row-wave-registry.py=1
case r3-registry-row-duplicated limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=SKILL.md read=registry-row-r44-routed-defects.py=2
case r3-registry-row-prose-only limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=SKILL.md read=registry-row-wave-registry.py=0
case r3-registry-row-in-code-fence limb=R3 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=SKILL.md read=selftest-cases=8
case r3-registry-row-in-html-comment limb=R3 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=SKILL.md read=selftest-cases=8
case r3-registry-section-renamed limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=SKILL.md read=registry-section-absent
case r3-readme-row-bullet limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/README.md read=readme-row-absent
case r3-readme-row-in-code-fence limb=R3 target_fixed=1 total_fixed=5 rc=0 verdict=FALSE-GREEN changed=corpus/instruments/README.md read=selftest-cases=8
case r3-skill-not-append-only limb=R3 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=SKILL.md read=SKILL-not-append-only
case r4-code-byte-flipped limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/freeze-check.py read=freeze-check-not-the-pinned-bytes
case r4-stub-freeze-check limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/freeze-check.py read=freeze-check-not-the-pinned-bytes
case r4-freeze-selftest-5-cases limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/freeze-check.py read=selftest-rc=0-tokens=(5, 0)
case r4-freeze-selftest-failure limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/freeze-check.py read=selftest-rc=1-tokens=(8, 1)
case r4-freeze-absent limb=R4 target_fixed=0 total_fixed=3 rc=1 verdict=rejected changed=corpus/instruments/freeze-check.py read=freeze-check-absent
case r4-claims-weakened limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-45/claims.json read=claims-not-the-frozen-bytes
case r4-claims-expect-changed limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-45/claims.json read=claims-not-the-frozen-bytes
case r4-claims-trailing-newline limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-45/claims.json read=claims-not-the-frozen-bytes
case r4-claims-absent limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-45/claims.json read=claims-not-the-frozen-bytes
case r4-claims-replay-short limb=R4 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-45/claims.json read=replay-rc=1
case r5-usage-line limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=usage-or-error-line-present
case r5-error-line-only limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=usage-or-error-line-present
case r5-original-changed limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3.txt read=original-receipt-changed
case r5-invocation-absent limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=invocation-lines=0
case r5-invocation-twice limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=invocation-lines=2
case r5-exit-nonzero limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=exit0-line-absent
case r5-cases-19 limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=receipt-body-not-the-pinned-run-output
case r5-receipt-body-edited limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=receipt-body-not-the-pinned-run-output
case r5-receipt-body-line-deleted limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=receipt-body-not-the-pinned-run-output
case r5-receipt-body-extra-line limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=receipt-body-not-the-pinned-run-output
case r5-fabricated-receipt limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=receipt-body-not-the-pinned-run-output
case r5-fabricated-comment-invocation limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=invocation-lines=0
case r5-r44-counter-edited limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=corpus/instruments/r44-routed-defects.py read=r44-counter-not-the-pinned-bytes
case r5-refiled-absent limb=R5 target_fixed=0 total_fixed=4 rc=1 verdict=rejected changed=.ufo/waves/round-44/controls/final-attempt3-refiled.txt read=refiled-absent
FALSE-GREEN mutant=r1-flip-vacuous-tbd limb=R1 recipe: S072 flip clause reduced to the vacuous `flip: tbd` (wave-1 probe; predicate: a checkable flip clause) | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r1-flip-vacuous-colon-dot limb=R1 recipe: S072 flip clause reduced to `flip: .` | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r2-row-in-code-fence limb=R2 recipe: R49 row wrapped in ``` fences inside the Round-45 block (a fenced line is not a criterion row) | counter read: limb R2 fixed=1 read=criteria=3 total=5
FALSE-GREEN mutant=r2-row-in-html-comment limb=R2 recipe: R49 row wrapped in an HTML comment inside the Round-45 block | counter read: limb R2 fixed=1 read=criteria=3 total=5
INFO-ACCEPTED (not counted) mutant=r2-padded-filler-criterion limb=R2 recipe: INFO: R48 criterion padded with 400 chars of filler to pass the length floor (class word + any file + a ref) | counter read: limb R2 fixed=1 read=criteria=3
INFO-ACCEPTED (not counted) mutant=r2-enforced-by-unrelated-file limb=R2 recipe: INFO: R47 enforced-by names LOG.md (an existing file that enforces nothing); predicate as written asks only that the path exists | counter read: limb R2 fixed=1 read=criteria=3
FALSE-GREEN mutant=r3-registry-row-in-code-fence limb=R3 recipe: wave-registry.py registry row wrapped in ``` fences inside the section (a fenced line is not a table row) | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5
FALSE-GREEN mutant=r3-registry-row-in-html-comment limb=R3 recipe: wave-registry.py registry row wrapped in an HTML comment inside the section | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5
FALSE-GREEN mutant=r3-readme-row-in-code-fence limb=R3 recipe: instruments README row for r44-frontier-count.py wrapped in ``` fences | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5
selftest cases=85 failures=7
```

## Other runs
- `--only r1-status-admitted,r5-refiled-absent,r4-claims-replay-short` -> `selftest cases=8 failures=0`, exit 0 (exit 0 iff F==0).
- `env -u TMPDIR … --only r5-refiled-absent` -> `selftest cases=6 failures=0` (fallback TMPDIR inside the scratch works).
- Scratch `$HYAKU_SCRATCH/kasegi-r45/selftest-c1/run-*` is removed by the script on exit; the seat scratch dir removed before yield.

## Limitations
- The default `--lane` is the moving lane working tree; the report run used an export (`--lane <export>`). `--lane` supplies counter, snapshots, claims.json and the refiled receipt, so the real receipt body is used for R5 (its pin = real pin; only R3/R4 differ under real pins).
- The synthetic freeze-check.py/r44-frontier-count.py are mine, not the lane's; behaviour mutants therefore test the counter's token/pin limbs, not the lane's code.
- Replay (R4) shells out to `r45-c2-gate.py` and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (read-only) from the export.
- `info` mutants never count as failures; the 7 failures are all counted because each violates the limb's stated content-binding.
- Cases run with `--jobs 4` threads; a mutant tree is hardlink-cloned from GOOD and every write unlinks first, so the base export and the lane were not modified (`git status --short` shows only wave2/ untracked).
