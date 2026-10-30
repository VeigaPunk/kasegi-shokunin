## Round 47 evidence

All four boxes stay `[~]`; `[x]` is operator-owned, and this wave-1 draft neither self-attests promotion nor reports an integrated-tree pass.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence (round 47): the F30 draft supplies a ten-row policy-branch/located-words/package-consequence decision table and a falsifiable rule preserving the unstated 120-day start event (`.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md:5-22,32-34`), while the frozen `corpus/instruments/r47-routed-defects.py` and `corpus/instruments/r47-f30-gate.py` supply the 11-limb and seven-limb decision artifacts with explicit red/green readings (`.ufo/waves/round-47/claims.json:12-18,36-42`), not evidence of a new SKILL.md edit or independent admission.
- [~] At least one end-to-end domain task executed and logged in LOG.md — evidence (round 47): the frozen claims define an end-to-end measurement chain from base controls through source-backed defect repair/F30 admission to explicit counter targets and semantic kill rules (`.ufo/waves/round-47/claims.json:12-18,36-42`), but this is documentation measurement rather than an executed target-domain task or submission, and the observed `grep -c '^## Round 47' LOG.md` printed `0`.
- [~] Instructions executable by an agent without oral context — evidence (round 47): the committed counter commands and selftest interface are replayable (`.ufo/waves/round-47/claims.json:15,39`; `corpus/instruments/r47-counters-selftest.py:484-490`), their do-nothing base receipts are red at `routed-defects total=11 fixed=0 unresolved=11 exit=1` and `f30-gate fixed=1/7 exit=1` (`.ufo/waves/round-47/controls/c1-base.txt:12-13`, `c2-base.txt:8-9`), and the inherited selftest receipt records `selftest cases=43 failures=0 exit=0` (`.ufo/waves/round-47/controls/selftest-receipt.txt:44-45`), without erasing the disclosed C1 16/35 and C2 18/21 uncaught mutants (`.ufo/waves/round-47/controls/mutbat-receipt.txt:36,58`) or claiming a rerun/integrated closure by this seat.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — evidence (round 47): `git diff --numstat fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 308a2cb2dc7bdce233461cc1ac49dd88e51c6193 -- PROVINCE.md` printed nothing, F30's attributed broker acquisition-disclosure policy fits the existing submission/disclosure-packaging province (`PROVINCE.md:29-30`), and the draft preserves F02/F15 rather than absorbing them or importing advisory records, reward rules or researcher submission rules (`.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md:24-30`; `PROVINCE.md:45`), with novelty still subject to independent review (`.ufo/waves/round-47/claims.json:41`).

---

## Scoped findings and integration boundary

The section above is the append-only SHONEN.md candidate; append only that section after existing history, not this findings appendix. SHONEN.md itself was not edited. All paths are relative to the kasegi lane root unless explicitly absolute. The F30 pointer deliberately resolves to the available wave-1 draft, not an unlanded production entry; this paragraph makes no claim that F30 is already the 30th admitted row or the 67th entry.

### Behavior and gates

- Axes: depth:verifiability; coverage. Four `[~]` boxes are retained with explicit supporting artifacts and limits.
- Provenance: frozen base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`; `.ufo/waves/round-47/freeze.txt:4-6` pins both counters and the selftest. The source manifest pins S075 to `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1` and body lines 20–27; the entry's decision table is a draft, not execution evidence.
- Do-nothing discrimination is inherited evidence, not a new probe: `controls/freeze-controls.txt:1-3` identifies `c1-base.txt`/`c2-base.txt`; `controls/freeze-check.txt:1-4` records both expected base readings and `freeze-check claims=2 base_ok=2 exit=0`.
- Targets remain targets: C1 11/11 and C2 7/7. Frozen-tree readings are C1 0/11 and C2 2/7 (`claims.json:29,50`); the 43-case selftest's two synthetic green fixtures do not establish an integrated candidate pass.
- No counter, selftest, full mutation battery, build, lint, census or live network recapture was run by this seat. Existing receipts were read, not recreated.
- Known conflicts/limits, verbatim: `mutbat counter=c1 mutants=35 caught=19 equivalent=0 uncaught=16 baseline_failures=0 exit=1`; `mutbat counter=c2 mutants=21 caught=3 equivalent=0 uncaught=18 baseline_failures=0 exit=1`. Neither survivor set is closed or equivalent. F02 overlap remains disputed prior art; a numbered F30 row alone does not settle novelty.

### Commands actually observed

Read-only observations below were run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless stated otherwise; these are observations of a changing wave-1 tree, not final-head verification.

| Exact command | Printed outcome |
|---|---|
| `git log -1 --format='HEAD=%h %s'` | `HEAD=82a8bd7 round-47: hand off 64-seat build and falsification wave` |
| `git diff --numstat fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 308a2cb2dc7bdce233461cc1ac49dd88e51c6193 -- PROVINCE.md` | Empty; establishes base-to-freeze equality only, not all future integrated bytes. |
| `grep -c '^## Round 47' LOG.md` | `0`; absence of that heading alone is not proof that no differently named domain task exists, so the draft also relies on its documentation-only scope. |
| `wc -l PROVINCE.md` | `174 PROVINCE.md` |
| `sha256sum PROVINCE.md` | `a9a9f62fa45cbc5f71511a645350053e13a8d66f56d06affb676ea7ab8bdbc25  PROVINCE.md` |
| `git ls-tree 308a2cb2dc7bdce233461cc1ac49dd88e51c6193 corpus/knowledge/ \| grep -c '\.md$'` | `66`; freeze count, not target 67. |
| `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | Printed `/fast/scratch/hyaku 54% 375.1G`, `/tmp 25% 96.7G`, `/var/tmp 41% 532.8G`; the command subsequently timed out after 30 seconds while at `top consumers /tmp`, so a successful complete guard exit is not claimed. |

### Touched surfaces and out of scope

- Deliverable: `.ufo/waves/round-47/w1/R47SrShonen.md` only; seat draft directory `.ufo/waves/round-47/w1/R47SrShonen.draft/` reserved, with no alternate product draft needed.
- Scratch: `/fast/scratch/hyaku/kasegi-r47/R47SrShonen/` was created empty and removed before handoff; no clone, fixture or counter work tree was made.
- No product files, PROVINCE.md, fleet files, sibling repositories, index or git/jj history were modified; no commit, push, publish, deployment, tool installation or service restart was performed.
- L1 owns integration and any subsequent checks; wave 2 owns attack of integrated bytes. This scribe report is neither claim judgment nor operator promotion.

### Self-evaluation

Accuracy 4/5 (inherited receipts and draft-byte evidence, not integrated verification); completeness 5/5 (all four required boxes, control, limits and append boundary supplied); clarity 4/5 (long box sentences preserve the requested one-sentence form); actionability 4/5 (append candidate is ready, but F30 remains a draft pointer); conciseness 4/5 (audit appendix retained separately from the candidate). Overall 4.2/5. Highest-impact improvement is later binding the same evidence to integrated bytes, which is L1/wave-2 work rather than an unrun pass here. The assessment does not confer claim or promotion credit.

Report: .ufo/waves/round-47/w1/R47SrShonen.md
