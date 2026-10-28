VERDICT: BROKEN

Seat R45W2MutC1R3R4 — mutation test of the v1.1 C1 counter `corpus/instruments/r45-routed-defects.py`, limbs R3 and R4 only. Target: lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4, exported with `git archive` to scratch. Counter bytes in the export verified unchanged (sha256 680c881af4a5f9a660c203c7a9e7e44e5ba4a860870e0d655121709e34f2fb67 before and after). Every mutant was applied to a fresh copy of the export and the counter was run as the grader runs it:
`python3 <tool>/corpus/instruments/r45-routed-defects.py --root <tree> --baseline <base>`, with `<base>` = export of dc5bb8c6e31efc4a6650819df85e79b72fd64bcd. Verdict `rejected=1` iff the counter exits nonzero.

## Controls (run by me)

    control=C0-tip-export (pristine tip as root) rc=0
      limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
      limb R2 fixed=1 read=criteria=3
      limb R3 fixed=1 read=selftest-cases=43
      limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2
      limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
      routed-defects total=5 fixed=5 unresolved=0 exit=0
    control=C-base-do-nothing (baseline export as root) rc=1
      limb R3 fixed=0 read=r44-frontier-count-not-the-pinned-bytes
      limb R4 fixed=0 read=freeze-check-absent
      routed-defects total=5 fixed=0 unresolved=5 exit=1

## Survivors (counter still green while the defect is present), listed first

S1-S3 are the important ones: the sha pins (`r44-frontier-count.py`, `freeze-check.py`, `claims.json`) do not cover them, and they reproduce the wave-1 defect classes "a stub selftest/freeze-check that prints the tokens" and "replay trusts graded-tree code".

**S1 — R3 selftest tokens forged by a shadow module (M01).** Single edit: add the new file `corpus/instruments/argparse.py` to the tree. It is transparent to every import except one: when `argv[0]` is `r44-frontier-count.py` and `--selftest` is given it prints `selftest cases=8 failures=0` and exits 0; otherwise it loads the real stdlib argparse by path into `sys.modules` and re-exports it.
Counter output (verbatim):

    limb R3 fixed=1 read=selftest-cases=8
    limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2
    routed-defects total=5 fixed=5 unresolved=0 exit=0
    mutant=M01-R3-shadow-argparse-stub rejected=0  (counter rc=0)

Cause: the limb runs `[sys.executable, s, "--selftest"]` with `s` = `<tree>/corpus/instruments/r44-frontier-count.py` (r45-routed-defects.py:247, 251). CPython puts the script's own directory (`<tree>/corpus/instruments`) first on `sys.path`, so any module the tree places there shadows the stdlib. The sha pin (line 249) covers the script bytes only, not the modules it imports.
Verified mitigation (on copies only): `python3 -P` drops the script-directory path entry. With the shadow present, `python3 -P corpus/instruments/r44-frontier-count.py --selftest` printed `selftest cases=43 failures=0`. With the counter copy patched to pass `-P` in the three `run(...)` calls (lines 251, 278, 286), the counter printed `limb R3 fixed=1 read=selftest-cases=43`.

**S2 — R4 freeze-check selftest and replay forged by a shadow module (M06).** Single edit: add `corpus/instruments/shlex.py` (transparent stdlib loader, except: `freeze-check.py --selftest` prints `selftest cases=6 failures=0`; `freeze-check.py --claims …` prints `freeze-check claims=2 base_ok=2 exit=0`; both exit 0). `freeze-check.py` imports `shlex` at line 37.
Counter output (verbatim):

    limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
    routed-defects total=5 fixed=5 unresolved=0 exit=0
    mutant=M06-R4-shadow-shlex-stub rejected=0  (counter rc=0)

Cause: `fc` is `<tree>/corpus/instruments/freeze-check.py` (r45-routed-defects.py:273), run at lines 278 and 286 with the tree's directory on `sys.path`, so the shadow is imported before freeze-check's own code. Mitigation check: with `-P` on the three calls, the same shadowed tree printed `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2` (the real counts).

**S3 — R4 replay verdict decided by an unpinned tree-side counter when TOOL_ROOT is the tree (M07).** Single edit: insert after line 46 of `corpus/instruments/r45-c2-gate.py` (after `from __future__ import annotations`):

    print("c2-gate fixed=1/7 exit=1")
    raise SystemExit(1)

Run the counter from inside the tree (`cd <tree> && python3 corpus/instruments/r45-routed-defects.py --root . --baseline <base>`, the usage string in the docstring), so `TOOL_ROOT` = `<tree>`. Line 66 derives TOOL_ROOT from `__file__` and never checks it against `--root`.
Counter output (verbatim):

    limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2
    routed-defects total=5 fixed=5 unresolved=0 exit=0
    mutant=M07-R4-treeside-c2-counter-prints-expect(TOOL_ROOT=tree) rejected=0

The replay's C2 claim (`{tool}/corpus/instruments/r45-c2-gate.py`, from the pinned claims.json) executes the tree's copy because freeze-check receives `--tool-root TOOL_ROOT` (line 286). The pinned claims bytes and the pinned freeze-check bytes do not help: the executed counter is unpinned.
Discrimination (same tree, only the tree-side line changed):
- silent variant (`raise SystemExit(0)` only), TOOL_ROOT = tree: `limb R4 fixed=0 read=replay-rc=1`, `routed-defects total=5 fixed=4 unresolved=1 exit=1` (M07c, rejected=1);
- same silent variant, TOOL_ROOT = pristine export: `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2`, exit 0.
So the R4 verdict follows whichever r45-c2-gate.py the tool root supplies. Reachable only if the grader invokes the counter from inside the graded tree; the code does not refuse that.

**S4 — R3 registry row with eight EMPTY cells (M02).** Edit: in SKILL.md, the round-45 `r44-frontier-count.py` row (line 1150) becomes `| r44-frontier-count.py | | | | | | | |`.
Output: `limb R3 fixed=1 read=selftest-cases=43` … `routed-defects total=5 fixed=5 unresolved=0 exit=0`; `mutant=M02-R3-registry-row-empty-cells rejected=0`.
Cause: the check counts cells only (r45-routed-defects.py:264, `len(rows[0].strip().strip("|").split("|")) != 8`) and never requires a non-empty cell.

**S5 — R3 registry row with placeholder cells (M10).** Edit: same row becomes `| r44-frontier-count.py | tbd | tbd | tbd | tbd | tbd | tbd | tbd |`.
Output: `limb R3 fixed=1 read=selftest-cases=43` … `exit=0`; `mutant=M10-R3-registry-row-placeholder-cells rejected=0`.
Same cause as S4 (r45-routed-defects.py:262-265).

**S6 — R3 registry table fenced inside SKILL.md (M03).** Edit: insert a line `` ``` `` before the round-45 table header row (`| name | type |…`) and another after its last row (SKILL.md ~1148 and ~1157, inside `## Round-45 Gates & probes registry addition`).
Output: `limb R3 fixed=1 read=selftest-cases=43` … `exit=0`; `mutant=M03-R3-registry-table-in-fence rejected=0`.
Cause: the section regex (line 259) and row regex (line 263) run on raw text with no fence or HTML-comment stripping. `registry_lines()` (lines 96-100) strips fences and comments for SOURCES.md (R1, the wave-1 "row inside a code fence" fix), but that handling was not applied to R3's SKILL.md and README.md reads.

**S7 — R3 README row inside an HTML comment (M04).** Edit: wrap the README row (corpus/instruments/README.md line 994, `| r44-frontier-count.py | counter | …`) with an `<!--` line before and a `-->` line after.
Output: `limb R3 fixed=1 read=selftest-cases=43` … `exit=0`; `mutant=M04-R3-readme-row-in-html-comment rejected=0`.
Cause: r45-routed-defects.py:266-267 runs `re.search` over the whole README with `re.M`; no comment or fence handling and no table-bounded check.

## Controls that do discriminate (the gate can fail)

- M05 (R3, delete the SKILL round-45 r44 row): `limb R3 fixed=0 read=registry-row-r44-frontier-count.py=0`, `routed-defects total=5 fixed=4 unresolved=1 exit=1`, `mutant=M05-R3-registry-row-deleted(control) rejected=1`.
- M08 (R4, claims.json C1 `expect_after` weakened): `limb R4 fixed=0 read=claims-not-the-frozen-bytes`, exit 1, rejected=1.
- M09 (R4, freeze-check replay check disabled by changing line 165 `if matched is None and not timed_out:` to `if False:`): `limb R4 fixed=0 read=freeze-check-not-the-pinned-bytes`, exit 1, rejected=1.
- M07c (R4, silent tree-side C2 counter, TOOL_ROOT = tree): see S3, rejected=1.

## Doc/code mismatch (finding D1)

r45-routed-defects.py lines 45-47 (v1.1 header) say: "source-recheck.py and freeze-check.py run from THIS script's own lane (the grader's tool root), never from the graded tree." Code: freeze-check is executed from the graded tree at line 273 (`fc = os.path.join(root, "corpus/instruments/freeze-check.py")`) and run at lines 278 and 286. Only the cwd is TOOL_ROOT; the executed file and its sys.path are the graded tree's. Lines 44-45 also say "rows are read only from the real registry table (not fences/comments)". That holds for SOURCES.md (R1, `registry_lines`) but not for the R3 SKILL.md and README.md checks (S6, S7).

## Recipe results (verbatim summary)

    mutant=M01-R3-shadow-argparse-stub rejected=0
    mutant=M02-R3-registry-row-empty-cells rejected=0
    mutant=M03-R3-registry-table-in-fence rejected=0
    mutant=M04-R3-readme-row-in-html-comment rejected=0
    mutant=M05-R3-registry-row-deleted(control) rejected=1
    mutant=M06-R4-shadow-shlex-stub rejected=0
    mutant=M07-R4-treeside-c2-counter-prints-expect(TOOL_ROOT=tree) rejected=0
    mutant=M07c-R4-treeside-c2-counter-silent(control) rejected=1
    mutant=M08-R4-claims-json-weakened(control) rejected=1
    mutant=M09-R4-freeze-check-replay-weakened(control) rejected=1
    mutant=M10-R3-registry-row-placeholder-cells rejected=0

Ten distinct mutants (M01-M10) were specified; M05, M08 and M09 are discriminating controls inside that set and M07c is a control for M07. Seven of the ten mutants survive (M01, M02, M03, M04, M06, M07, M10).

## Limitations

- Only CPython 3.14.8 was tested. Shadowing depends on sys.path[0] behaviour; the `-P` mitigation was verified on the same interpreter only.
- Mutants were applied to copies. The lane export and the lane working tree were not modified; the export counter sha is unchanged.
- The `-P` mitigation was verified on copies of the counter, not landed. I did not touch the lane.
- R1, R2 and R5 were not exercised (outside the assignment).
- freeze-check selftest case 2 reads the real base README from `/fast/scratch/hyaku/kasegi-r45/L1/pure` (freeze-check.py `PURE_DEFAULT`), an external L1 scratch path the grader may not have. Not mutated; noted only.
- Judgement: S4, S5, S6 and S7 survive under the stated R3 predicate ("eight-cell rows", "has a row"). The defect is that the predicate accepts a registry that is empty, placeholder, fenced or commented. If R3 is read as name-presence only, S4 and S5 are by design and only S1, S2, S3, S6 and S7 stand.
- Scratch removed on exit (`/fast/scratch/hyaku/kasegi-r45/R45W2MutC1R3R4`). No commit, push, or mutating git was run.
