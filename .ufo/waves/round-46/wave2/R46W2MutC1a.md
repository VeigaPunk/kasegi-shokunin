# R46W2MutC1a — C1 counter v1.1 mutation probe (limbs L1-L3)

VERDICT: BROKEN

Four of twelve single-edit mutants survive L1-L3 with the defect present (m09-m12 below). Eight are rejected. Both controls discriminate. The survivors are counter-definition gaps (one recheck line per entry; raw-text match with no Markdown awareness), and recheck-audit.py shares them.

## Setup (all re-run by this seat)

- Tree under test: export of committed tip `5437afeaf9b642c267bba3c31f00ae701e49da68` (`git archive ... | tar -x`), copies of its `corpus/` only (8.7 MB) per mutant.
- Base: export of `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba` (`corpus/` 8.5 MB).
- Counter: the lane's own instrument, run from the lane: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py --root <copy> --baseline <base export> --work <scratch>`. `cmp` of the lane file against the tip export's copy: identical.
- Lane HEAD at run time: `0d121a201fe7cc3d0604ceb7666d1a85a5bbc174` (wave-2 spec commit), a descendant of `5437afeaf9b642c267bba3c31f00ae701e49da68`. `git diff --name-only 5437afea HEAD -- corpus` prints nothing, so the corpus under test is identical to the assigned tip.
- Host state at run time: `test -d ~/Projects/bounties` → absent. Base gating (`gated=24`) depends on this; the counter discloses that dependence.
- Mutant edits were applied by a scratch recipe (deleted at exit). Each mutant is the exact edit listed below; the counter's own stdout is quoted.

## Survivors (rejected=0; defect present)

### m11-exact-line-in-html-comment — SURVIVES
- Edit: `corpus/knowledge/claim-gates.md`: a line `<!--` inserted before line 125 and a line `-->` inserted after the recheck line (mutant lines 125-127 read `<!--` / `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md` / `-->`). Nothing else changed.
- Counter output: `mutant=m11-exact-line-in-html-comment rejected=0 failing-limbs=none fixed=7/7`; `gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64`; `gate L3 pass=1 read=recheck-lines-exact=2`; all of L1-L7 pass; `c1-gate fixed=7/7 exit=0`.
- Defect: the only recheck line of a regrounded entry is inside an HTML comment, so a rendered reader sees no live recheck, yet the counter certifies the entry as regrounded and counted out of the gated set.
- Why it passes: `RECHECK_RE = re.compile(r"^recheck:[ \t]*(.*)$")` (r46-c1-gate.py:64) and `recheck_line()` (lines 108-112) match raw lines. `grep -n '<!--\|```\|fence\|comment'` over the counter returns nothing, so the counter has no Markdown structure check.
- Shared with the instrument of record: `recheck-audit.py` `audit_entry` also takes the first raw `^recheck:` match (lines 115-116). Its output on this tree: `executes=43 gated=22 broken=0` (same as tip).

### m12-exact-line-in-code-fence — SURVIVES
- Edit: `corpus/knowledge/claim-gates.md`: a line ```` ``` ```` inserted before line 125 and one after the recheck line (mutant lines 125-127 read ```` ``` ```` / `recheck: ...--entry corpus/knowledge/claim-gates.md` / ```` ``` ````).
- Counter output: `mutant=m12-exact-line-in-code-fence rejected=0 failing-limbs=none fixed=7/7`; `gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64`; `c1-gate fixed=7/7 exit=0`.
- Defect: the recheck is rendered as a code sample, not as the entry's live recheck. Same mechanism and same shared gap as m11 (recheck-audit `executes=43 gated=22 broken=0`).

### m09-hidden-second-gated-line — SURVIVES
- Edit: `corpus/knowledge/claim-package-gate.md`: one line inserted after line 5 (the existing recheck): `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/r46-probe-absent` (`grep -c '^recheck:'` on the mutant file → `2`). This entry was executing at tip and stays executing.
- Counter output: `mutant=m09-hidden-second-gated-line rejected=0 failing-limbs=none fixed=7/7`; `gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64`; `c1-gate fixed=7/7 exit=0`.
- Defect: a gated recheck line exists in the tree and is not counted in `gated=`.
- Why it passes: `classify()` takes `n = sum(...)` over all raw lines (r46-c1-gate.py:192) but classifies only `line = recheck_line(text)` = first match (line 193; `recheck_line` returns at line 112). L1's gated and broken counts therefore see one line per entry. The duplicate test (`ct[e]["n"] != 1`, line 230) applies only to the regrounded set. Shared: recheck-audit `audit_entry` breaks on the first match (lines 115-116); its `executes=43 gated=22 broken=0` is unchanged.

### m10-hidden-second-broken-line — SURVIVES
- Edit: `corpus/knowledge/claim-package-gate.md`: one line inserted after line 5: `recheck: test -s corpus/knowledge/claim-package-gate.md || true` (not allow-listed; would be `broken`).
- Counter output: `mutant=m10-hidden-second-broken-line rejected=0 failing-limbs=none fixed=7/7`; `gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64`; `c1-gate fixed=7/7 exit=0`.
- Defect: a non-allow-listed (broken) recheck line exists at TREE and L1's `broken=0` reads 0. Same mechanism as m09.

## Rejected (8/12)

- m01-gated-up-existing: `claim-package-gate.md` recheck replaced by `... && test -d ~/Projects/r46-probe-absent` → `rejected=1 failing-limbs=L1,L2 fixed=5/7`; `gate L1 pass=0 read=gated=23 broken=0`.
- m02-gated-up-new-entry: new `corpus/knowledge/r46-mut-probe.md` with a gated recheck → `rejected=1 failing-limbs=L1,L2 fixed=5/7`; `gate L1 pass=0 read=gated=23 broken=0 lines=66/base=64`.
- m03-parse-fail: `claim-package-gate.md` recheck ends with dangling `&&` → `rejected=1 failing-limbs=L1 fixed=6/7`; `gate L1 pass=0 read=gated=22 broken=1`.
- m04-allowlist-redirect: `claim-package-gate.md` recheck ends `&& echo probe > /fast/scratch/hyaku/kasegi-r46/R46W2MutC1a/allowlist-probe.txt` → `rejected=1 failing-limbs=L1 fixed=6/7`; `gate L1 pass=0 read=gated=22 broken=1`; `allowlist-probe-exists=0` (the redirect never ran).
- m05-regrounded-set-one: `claim-package-contract.md` exact recheck replaced by base's gated line → `rejected=1 failing-limbs=L1,L2,L7 fixed=4/7`; `gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md`.
- m06-section-renamed: `## Re-ground (round 46)` → `## Re-ground (round 45)` in `claim-package-contract.md` → `rejected=1 failing-limbs=L1,L2,L7 fixed=4/7`.
- m07-exact-line-names-other-entry: `claim-package-contract.md` recheck names `--entry corpus/knowledge/claim-gates.md` → `rejected=1 failing-limbs=L3 fixed=6/7`; `gate L3 pass=0 read=bad=claim-package-contract.md`.
- m08-restoration-promoted: `claim-gates.md` line 126 `restoration-recheck:` → `recheck:` → `rejected=1 failing-limbs=L3,L5 fixed=5/7`; `gate L3 pass=0 read=bad=claim-gates.md`.

## Controls

- control-tip-unmutated (committed tip export, corpus only): `control=control-tip-unmutated rejected=0 fixed=7/7`; `gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64`; `gate L6 pass=1 read=mutants=46 survivors=none`.
- control-base-do-nothing (base export as the tree): `control=control-base-do-nothing rejected=1 fixed=1/7`; `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64`; `gate L2 pass=0 read=base-gated=24 regrounded=0`.

## Limitations

- Twelve mutants, all single edits, all aimed at L1-L3 as assigned. L4-L7 were read only where the mutants touched them (m05, m06, m08); no L4-L7 mutant campaign was run.
- Allow-list: exercised only by m03 (parse) and m04 (redirect); both rejected. The bypass reading is not run: `CD_RE` strips the leading `cd <path> &&` before `allowed()`, and the executed command is the stripped string. I did not test a bypass beyond m04.
- Host dependence: every gate reading uses this host's HOME (`~/Projects/bounties` absent). Base gating depends on it. The counter says so; I did not vary HOME.
- recheck-audit was run only on the four survivor trees and the tip, for its per-line counts (`executes=43 gated=22 broken=0`, identical in all five). Its verdict is not cited: on an export root its `cdroot` limb fails for all 64 entries (`strict pass=1/65 cdroot_fail=64`), as expected for a root other than the lane.
- Semantic overreach of re-grounded rows (C1 kill-rule non-author reading) is out of scope for a mutation probe and was not tested.
- The four survivors are not failures of the frozen kill rule as written (`fixed<7/7`, controls, non-author reading). They are gaps against the L1 sentence ("gated lines at TREE") and the L3 sentence (recheck line shape) as worded. I report them as survivors and do not edit the counter or the lane.
- Nothing was committed, pushed or mutated in git. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46W2MutC1a/`) was removed at exit.
