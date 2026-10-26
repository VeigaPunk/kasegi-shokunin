# SCORECARD.md — round-35 fixture payload (not the lane scorecard)

Committed test fixture for `corpus/instruments/r35-defect-closure.sh --selftest`
(`corpus/instruments/r35-fixtures/README.md`). It reproduces only the lines the C1 closure checks
read, in the lane file's own shapes and spellings. The live file is `SCORECARD.md` at the lane root;
these bytes are pinned here and are never re-copied from the live file.

## Round 34 — depth:density row (verbatim from the round-34 scorecard)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| depth:density | 9 | mean **201.7**, 25 blocks, 710 path-citation instances (`SKILL.md` `b11b6085…`, 1090 lines — the round-33 final bytes) | mean **201.7**, 25 blocks, 710 cites, 1090 lines; `SKILL.md` and `PROVINCE.md` absent from `git diff --numstat 014ee2d7` (0 lines changed, both sides the same bytes); `anchorcheck.py SKILL.md` → `12 in-range cite instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 (`RevNoHarm` §A–§C, the independent reviewer; no `ExecNoHarmFinal` receipt had landed at this seat's read) | **Unchanged (held 9), no harm, no move claimed.** The round adds instruments, manifests, lessons and registry rows and no `SKILL.md`/`PROVINCE.md` byte, so the density census reproduces round 33 exactly on the same committed instrument; every failure class in `anchorcheck.py` is at its recorded value, and the one authorised deletion set (2 lane-hash marker lines + in-place instrument/manifest replacements) is mapped to frozen-claim text line by line in `RevNoHarm` §A | r15 (held r34) |


<!-- limb D2 fixed: the appended erratum below names the stale row and the corrected mean -->
**Erratum (round 35) — round-34 depth:density row.** The row above is stale on two counts: at the
round-34 tip `SKILL.md` and `PROVINCE.md` each carry +1 appended line (0 changed lines is wrong), and
the corrected `density.py` mean is **201.2**, not 201.7. The row's filed bytes are left untouched;
this paragraph supersedes only those two numbers.

<!-- limb D1 broken: the round-34 placeholder prose is still here and no tip hash is named -->
**Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section
was measured at the wave-1 integration state.
