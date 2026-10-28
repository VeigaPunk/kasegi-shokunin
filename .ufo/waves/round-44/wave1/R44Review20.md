# R44Review20 — Independent C1/C2 claim-admission assessment

## Axis and scope
Assessment axis: **depth:verifiability** for C1 and **coverage** for C2. Findings are read-only observations. HEAD at the round-44 freeze was `66314015122b9aa32dc40f2f1815df56624c26d1` (parent/base recorded in `.ufo/waves/round-44/controls/do-nothing.txt`: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`). The worktree was actively changing during review; distinguish frozen-HEAD results from transient worktree results below.

## Findings — actionable replayability defects

### High — C1’s counter labels string-presence predicates as gate visibility / defect closure

The frozen list is reproducibly eight headings: at HEAD,
`git show HEAD:corpus/lessons/round-43-verifier-spotcheck.md | grep -Ec '^6\\. Routed defects|^[0-9]+\\. \\*\\*'` → `8` (also the control command in `controls/do-nothing.txt`). That command counts headings, not whether any of the eight is resolved; it does not test the control’s adjacent assertion that none has a correction.

The current worktree counter `corpus/instruments/r44-routed-defects.py` (observed SHA-256 prefix `9566b225484ee154`, untracked at the time) grades eight hand-coded conditions at lines 28–52. Several are not faithful checks of the frozen defect:

- **RD43-2, line 46:** label is “K17 can see defect 1,” but predicate is only that `closed=13/19` and `superseded` occur in the erratum. The defect’s required property is that a check can see/grade the bad token. K17 does not: `corpus/instruments/r43-limbs/k17-claims-before.sh:105` token regex is `closed|failures|cases`, and its grading block at lines 326 onward skips `field == "after"` before its supersede logic. The `13/19` token is in the round-43 C1 `after` cell; `exit 127` is not in K17’s token regex. Reproduction: run K17 on an archive of HEAD with `--tree <export> --work <scratch>`; payload was `claims=22,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1`. Adding `.ufo/waves/round-43/claims-erratum-6.md` to that scratch export left the payload byte-for-byte unchanged. A scratch-only fabricated erratum containing `closed=13/19 superseded` made the counter’s RD43-2 resolve while K17 still returned the same payload. This is false admission of the claimed visibility, not merely an absent test.
- **RD43-4, line 48:** frozen defect #4 requires the round report to carry planner=L1 and the L2-floor/residual-call line. The counter checks `corpus/lessons/round-44.md`, not the report; a lesson can make this limb green while the report omits the required content.
- **RD43-7, line 51:** frozen defect #7 names the SHONEN pointer and `corpus/instruments/README.md`; the counter checks two already-present `SKILL.md` instrument names and a phrase in `corpus/lessons/round-44.md`. Neither the defective pointer nor the README rows are checked. At frozen HEAD, `git grep -c 'instruments/README' HEAD -- SHONEN.md` returned no match (exit 1), so the alleged before-state is itself not reproduced by the named artifact.
- **RD43-8, line 52:** string tests over erratum/receipt, not a transcript or execution. A scratch-only fabricated receipt with just `exit=127` plus an erratum containing the expected strings made this limb resolve. Thus it does not establish that the cited missing-suite command was actually run. The worktree receipt `.ufo/waves/round-44/controls/missing-suite-base.txt` used the placeholder command `cd <git archive base> ...` and recorded no raw output; K17 cannot grade `exit 127` in any case.
- **RD43-1, line 45:** earlier observed counter revision used `correction_after()` on the first SCORECARD occurrence and a mere token presence in errata. In that revision, a scratch erratum with only `closed=13/19` (no “superseded”) made RD43-1 resolve. The current revision must be assessed at its pinned bytes; this demonstrates the predicate drift during review and that its positive test is not a frozen contract. Do not treat that earlier run as a result for the current script.

The counter’s own optional selftest (current file lines 75–111) mutates each predicate’s fixture strings, including deleting `closed=13/19` for RD43-2; it does not test K17 visibility or report-vs-lesson binding. At frozen HEAD, I ran the counter against a `git archive HEAD` export as both `--root` and `--baseline`: `fixed=0 unresolved=8 exit=1`. This is a useful overall red-before control, but it does not validate each limb’s semantic target. During the later live-worktree observation, the then-current script returned `fixed=5 unresolved=3`; that is transient and not committed evidence.

### High — C2 frontier counter cannot replay its own stated baseline

The C2 `counter` in `claims.json` uses `grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md`. At frozen HEAD it returned `0`, while the control’s wider pattern `grep -cE '^\\| F[0-9]+ \\| .* \\| admitted \\|'` returned `25`. The table header at `corpus/README.md:200` is `id | topic | status | entry | sources | next`; e.g. F01 at line 202 has topic in the second cell and `admitted` in the third. The claims.json regex therefore expects the topic cell to be `admitted`, and cannot count the baseline 25 or target 26. On the active worktree the same bad regex remained 0 while the control pattern was 26. The exact third-column pattern `grep -cE '^\\| F[0-9]+ \\| [^|]+ \\| admitted \\|' corpus/README.md` returned 26. This is a direct counter/claim mismatch.

### Medium — other C2 quantities are replayable only as weak proxies or non-delta guards

- **SOURCES row cardinality:** the declared row regex reproduces 68 at frozen HEAD. It does not test newness, tier, status, or citation. On the active worktree it counted 70 rows, including S070 (tier C, rejected); therefore a row-count increase alone can pass without the required new tier-A sourced knowledge entry. In the observed worktree the actual stronger condition did hold: S069 was tier A/mined, `used-by` named `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`, and that entry’s `source:` line named S069. The count is not proof of that condition.
- **Knowledge cardinality:** `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` reproduced 62 at HEAD and 63 in the observed worktree; there were no nested markdown files in the checked tree. The worktree also updated `corpus/instruments/knowledge-expected.txt` to 63 entries. That expected-list agreement is a separate necessary predicate: `recheck-audit.py` documents that an extra knowledge entry prints `unexpected=<name>` and fails (lines 44–51, 252–253), but the C2 counter does not check it.
- **Recorded reject:** already true at HEAD (13 rejected rows in the 68-row registry); it is not a round-44 delta predicate as phrased. The worktree’s S070 adds another rejected row, but “a recorded reject” alone cannot establish new coverage.
- **SOURCES census:** the prescribed fleet-root invocation returned exit 0 at both the frozen control and this review’s active-worktree run, with W04 warnings for S028/S029. It is replayable as a guard, but already green at baseline and does not measure the claimed movement. It is not included in the claims.json counter string.
- **Non-author admit/reject spot-check:** not countable by any listed command; it requires a committed receipt and independent decision evidence.

## Residual risk / verification gaps

The round-44 worktree was changing while these checks ran. At the last tracking check, `corpus/instruments/r44-routed-defects.py`, `claims-erratum-6.md`, and the relevant round-44 control files were untracked; the counter’s hash changed during review. The current counter and its inputs therefore were not yet committed evidence, and results from successive versions must not be conflated. The exact claims.json C1 CLI was later aligned with the counter’s `--root/--baseline` interface, but the counter still needs semantic discrimination checks for the defects above. The round-44 report and lesson had not landed when inspected; report-dependent acceptance cannot yet be confirmed.

The frozen do-nothing control’s C1 grep proves the defect-list size only, not the unresolved count. For a canonical replay, pin both `--root` and `--baseline` to explicit committed exports, run the same counter against the frozen base and final export, and ensure each limb checks the actual artifact/condition named by its frozen defect. For C2, correct the frontier regex and keep row-count, tier-A/status/newness, source-to-entry binding, expected-list equality, census exit, reject record, and non-author review as distinct predicates.

## Commands and outputs exercised

- `git show HEAD:corpus/lessons/round-43-verifier-spotcheck.md | grep -Ec '^6\\. Routed defects|^[0-9]+\\. \\*\\*'` → `8`.
- `git show HEAD:corpus/README.md | grep -cE '^\\| F[0-9]+ \\| admitted \\|'` → `0`; `git show HEAD:corpus/README.md | grep -cE '^\\| F[0-9]+ \\| .* \\| admitted \\|'` → `25`.
- Frozen HEAD export: current counter `--root <HEAD-export> --baseline <HEAD-export>` → `frozen_defects=8 fixed=0 unresolved=8 exit=1`.
- K17 HEAD export, then same export plus erratum-6: both → `K17 payload=claims=22,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1`.
- `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → W04 S028, W04 S029, `kasegi ok .../corpus/SOURCES.md`, exit 0.

No production/shared files were edited. Only this assigned report is written.
