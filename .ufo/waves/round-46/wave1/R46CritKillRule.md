VERDICT: BROKEN

Scope: kill rules of C1 and C2 in .ufo/waves/round-46/claims.json (frozen; freeze.txt pins claims-sha256 e56ebf87…), the frozen counters corpus/instruments/r46-c1-gate.py (sha256 b0c730c8…) and r46-c2-gate.py (sha256 0ee95785…), the controls file, and every `plain` command. Nothing in the lane was edited; no git mutation; scratch removed on exit.

Method: freeze tree = `git -C <lane> archive 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 corpus SKILL.md PROVINCE.md SCORECARD.md SHONEN.md LOG.md .ufo/waves/round-46` (exported to scratch). Base tree = `git archive 914ca0b6…` (`diff -rq` against /fast/scratch/hyaku/kasegi-r46/L1/pure/corpus: no output, identical). Plain commands were run on the freeze export and on the base copy, not on the lane tip. Fixtures were built in scratch from the freeze export as single mutations; each is named below.

## 1. Frozen readings and controls reproduce

- `python3 corpus/instruments/r46-c1-gate.py --root freeze --baseline base` printed `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64` ... `gate L7 pass=1 read=still-gated=24 changed=none` / `c1-gate fixed=1/7 exit=1`. Matches claims.json `freeze_tree_reading`.
- C2 at freeze: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`, `gate G7 pass=1 read=census-rc=0 ok-line=1`, `c2-gate fixed=2/7 exit=1`. Matches claims.json `freeze_tree_reading`.
- Do-nothing base: C1 `c1-gate fixed=1/7 exit=1`; C2 `c2-gate fixed=1/7 exit=1`.
- `python3 .ufo/waves/round-46/controls/freeze-controls.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --base 914ca0b6… --work <scratch>` (lane counters, sha matches freeze.txt) output diffed against controls/freeze-controls.txt: `IDENTICAL`, 91 lines, `controls total=9 red=9 green=0`, rc 0.
- Plain commands at freeze (base numbers, unchanged at freeze for C1 and C2 except as noted):
  - C1-1 `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` → `23`
  - C1-2 `recheck-audit.py --root . --quiet | grep '^executes='` → `executes=40 gated=24 broken=0 ...`
  - C1-3 `score-gap.py | grep '^gap:'` → `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`
  - C2-1 `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `27`
  - C2-2 `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `72`
  - C2-3 `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `64`
  - C2-4 `source-recheck.py --manifest … --source S073` → `S073:sha256 OK`, `S073:Q1 OK … S073:Q8 OK`, rc 0 (already true at freeze, so this line does not discriminate freeze from base)
  - C2-5 `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → no output, rc 1 (base state)
  - Same numbers on the base copy (C1-1 `23`, C1-2 `executes=40 gated=24`, C2-1 `27`, C2-2 `72`, C2-3 `64`).

## 2. C1 (depth:verifiability): states the kill rule does not name

C1-a. Leading `cd ~/…` is exempt from the no-`~/` test (counter green, defect present).
- Fixture: both re-grounded entries (claim-gates.md, claim-package-contract.md) with valid rows and recheck `cd ~/Projects/bounties && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md`.
- Output: `gate L3 pass=1 read=recheck-lines-clean=2` … `c1-gate fixed=7/7 exit=0`.
- Mechanism: r46-c1-gate.py:61 `CD_RE` strips `cd … &&`, :187 tests HOME_RE on the stripped line, :163 runs the stripped line in TREE. recheck-audit.py:97 runs the full line. `bash -c 'cd ~/Projects/bounties && true'` → `bash: line 1: cd: /home/vgpnk/Projects/bounties: No such file or directory`, rc 1: the line is gated on the lost base, which is what the instrument of record sees.
- Minimal wording (add to C1 kill_rule): "or if any re-grounded recheck line differs from `^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate\.py --entry corpus/knowledge/[A-Za-z0-9._-]+\.md$` (a `grep -cE` of that pattern per re-grounded file must be 1)". Checked: that pattern gives 1 per file on the valid control and 0 on C1-a, C1-b, C1-c.

C1-b. A no-op recheck that merely contains the gate's name passes L3 (counter green, gate never runs).
- Fixture: recheck `true  # python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md`, valid rows.
- Output: `c1-gate fixed=7/7 exit=0`. `recheck-audit.py --root <fixture> --quiet | grep '^executes='` → `executes=42 gated=22 broken=0`, so plain C1-2's target (`gated<=22 broken=0`) is also green.
- Mechanism: r46-c1-gate.py:187 is a substring test (`"r46-c1-gate.py" not in ln`), not an execution test; classify (:160-168) only sees the exit code.
- Minimal wording: the exact-form pattern of C1-a (rejects this line).

C1-c. Spelling `--entry ./corpus/knowledge/…` is red with the claim true.
- Fixture: recheck `cd /home/vgpnk/… && python3 corpus/instruments/r46-c1-gate.py --entry ./corpus/knowledge/<e>.md`, valid rows.
- Output: `gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md` … `c1-gate fixed=6/7 exit=1`.
- Mechanism: :187 literal `--entry corpus/knowledge/<e>` substring.
- Minimal wording: the exact-form pattern in C1-a (it names the spelling; the claim does not).

C1-d. The after-clause "every BASE line kept (append-only)" cannot be satisfied with the BASE recheck line kept.
- Fixture: BASE recheck line left in place, new recheck line appended after the section.
- Output: `gate L1 pass=0 read=gated=24 broken=0 …` … `c1-gate fixed=1/7 exit=1`.
- Mechanism: `recheck_line()` returns the first `recheck:` match (r46-c1-gate.py:78-83), so the old gated line is read; L5 (:198-200) exempts recheck lines, so the counter itself expects replacement in place. Controls replace in place (freeze-controls.py `set_recheck`).
- Minimal wording: "every BASE line except its `recheck:` line kept in order; the BASE recheck line is replaced in place by the new one."

C1-e. The "current claim" column is never read (empty claim cells).
- Fixture: all rows `| G1 |  | `<anchor>` | `<token>` |` with the valid anchors and tokens.
- Output: `gate L6 pass=1 read=mutants=12 survivors=none` … `c1-gate fixed=7/7 exit=0`.
- Mechanism: check_row (r46-c1-gate.py:101-122) reads cells 2 and 3 and never the claim text.
- Minimal wording: "each row's `current claim` cell is a non-empty sentence of the entry; `grep -cE '^\| G[0-9]+ \| *\|'` over the section must be 0."

C1-f. Trivial token and self-anchoring pass every limb (the one-command limb cannot judge support).
- Fixture: six rows per entry, three anchored to `corpus/instruments/r46-c1-gate.py:44-83` and three to `corpus/instruments/claim-package-check.py:81-120`, token `import`, claim text `row`.
- Output: `gate L6 pass=1 read=mutants=12 survivors=none` … `c1-gate fixed=7/7 exit=0`.
- Mechanism: :110 excludes only the entry as anchor, so the counter may anchor to itself; :115 accepts any token of ≥6 characters inside a 40-line range. L6 cannot discriminate here: any row whose token is located turns the entry check red when blanked, so "load-bearing" adds nothing beyond "located".
- Minimal wording: "no anchor is `corpus/instruments/r46-c1-gate.py`; each anchored range is at most 3 lines (`:N-M` with M−N ≤2); no token is a bare language keyword (`import`, `def`, `return`, `class`)." The keyword and self-anchor parts are one-command greps; the range part is `grep -oE '`[^`]+:[0-9]+-[0-9]+`'`.

C1-g. Plain C1-1 is a proxy that a rename satisfies while the gate stays closed.
- Fixture: `sed` changes `test -d ~/Projects/` to `test -d $HOME/Projects/` in the two entries, nothing else.
- Output: `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` → `21` (target ≤21 reads green); `recheck-audit.py` → `executes=40 gated=24 broken=0`; counter → `gate L7 pass=0 read=still-gated=24 changed=claim-gates.md,claim-package-contract.md` … `c1-gate fixed=0/7 exit=1`.
- Minimal wording: replace C1-1 with `grep -lE 'test -d (~/|\$HOME|/home/)' corpus/knowledge/*.md | wc -l` (prints `23` on base and `23` on the rename fixture, so target ≤21 is red on a rename).

C1-h. Exit-code-only reading of plain C1-2.
- `python3 corpus/instruments/recheck-audit.py --root <freeze> --quiet | grep '^executes='; echo pipeline_rc=$?` printed `executes=40 gated=24 broken=0 …` then `pipeline_rc=0`. recheck-audit's own exit is 1 at base (`echo ${PIPESTATUS[0]}` → 1).
- Minimal wording: "read the printed number; never judge plain C1-2 by the pipeline exit."

C1-i. recheck-audit on an export copy measures the live lane wherever a recheck carries `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` (artifact of the form the counter's docstring prescribes, r46-c1-gate.py:15).
- Fixture V0 (valid rows, no other change): `recheck-audit.py --root <V0> --quiet` → `executes=40 gated=24`, same as base, while the counter reads 7/7. The two re-grounded lines run `cd <live lane>`, fail there, and are gated.
- Minimal wording: "plain C1-2 is run at the lane root only, never on a copy."

C1-j. [INFERENCE, not tested] Recheck lines execute the TREE's own copy of r46-c1-gate.py, so the scored tree's counter bytes are not pinned by the kill rule. L4 uses the frozen SELF, so fabricated rows still turn the aggregate red; the recheck-audit reading would follow the tree copy. Minimal wording: "or if corpus/instruments/r46-c1-gate.py at the scored tree is not sha256 b0c730c8…".

Controls: the four C1 controls (do-nothing, marker-only, fabricated, single-file, gutted) do not cover C1-a through C1-g; the states above are not in controls/freeze-controls.txt.

## 3. C2 (coverage): states the kill rule does not name

C2-a. Restatement with no decision rule scores 7/7.
- Fixture A: F28 row (name `GitHub private vulnerability reporting`), S073 row, 65 entries, entry with the four headings, the provenance trio, five curly quotes each cited `(`S073.txt:<line>`)` to lines 564/573/574/577/578, a six-row situation table, two xrefs, paraphrase padding (7495 bytes).
- Output: `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`, `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5`, `c2-gate fixed=7/7 exit=0`.
- `grep -cE '^(If|When) ' <entry>` → `0`.
- Mechanism: G2 counts headings and 3-cell table lines (r46-c2-gate.py:194-195); nothing reads whether a decision is stated.
- Minimal wording (add to C2 kill_rule): "or if fewer than two sentences in `## Scope and decision rule` begin `If ` or `When ` and name a reporter action (`grep -cE '^(If|When) ' <entry>` < 2)."

C2-b. Unbounded citation range scores 7/7.
- Fixture B: same entry, every quote cited `(`S073.txt:1-589`)`.
- Output: `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5`, `c2-gate fixed=7/7 exit=0`.
- Mechanism: window = snapshot lines a..b with no size bound (r46-c2-gate.py:262-269).
- Minimal wording: "or if any citation spans more than 3 lines (`grep -oE 'S073\.txt:[0-9]+-[0-9]+'` with end−start > 2)."

C2-c. F28's name cell is not read.
- Fixture C: README row `| F28 | Misc notes | admitted | knowledge/github-private-vulnerability-reporting.md | S073 | next |`, otherwise fixture A.
- Output: `gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md`, `c2-gate fixed=7/7 exit=0`.
- Mechanism: G1 reads id, status and entry cell only (r46-c2-gate.py:165-179).
- Minimal wording: "or if the F28 name cell is not `GitHub private vulnerability reporting` (`grep -cE '^\| F28 \| GitHub private vulnerability reporting \| admitted \|' corpus/README.md` ≠ 1)."

C2-d. The env override voids the base-knowledge pin.
- Fixture D: fixture A plus a one-line backlink appended to corpus/knowledge/ai-assisted-finding-validation.md.
- Without env: `gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1`, `c2-gate fixed=6/7 exit=1`.
- With `R46_PINS_OVERRIDE=<file containing {"base-knowledge-content": null}>`: `gate G6 pass=1 …`, `c2-gate fixed=7/7 exit=0`. (The variable takes a file path, r46-c2-gate.py:66-67; the docstring calls it selftest-only.)
- Minimal wording: "C2 is graded only with R46_PINS_OVERRIDE unset (`env -u R46_PINS_OVERRIDE`); any run with it set is void."

C2-e. Counter red with the claim true: any edit to a base knowledge entry.
- Fixture D without env (above) is red on G6 only. The claim is silent on base entries; the counter pins all 64 of them (r46-c2-gate.py:279-291). A legitimate backlink reds C2.
- Minimal wording: either "the 64 base knowledge entries are byte-identical to base; any edit to one is a kill" (so the scorer knows) or drop the pin (counter change, requires re-freeze).

C2-f. The stated contrast with F27 and F04 is not read by any limb.
- Fixture A has no F27 or F04 text (`grep -cE 'F27|F04' <entry>` → `0`) and scores 7/7.
- Minimal wording: "or if the entry does not name F27 and F04 (`grep -cE 'F27|F04' <entry>` < 2)."

C2-g. [Not tested] G7 runs the fleet-root script /home/vgpnk/Projects/shokunin/scripts/sources-census.sh (r46-c2-gate.py:54, :294-297) with no pin; a change there moves G7 with no lane change. Minimal wording: "pin sha256 of scripts/sources-census.sh (or name its version) in the kill rule."

C2-h. Plain C2-4 (`source-recheck.py … S073`) already passes at freeze, so it is a tip-state check that does not distinguish freeze from base. Minimal wording: say it is a freeze-state check, or drop it from the discriminating set.

## 4. Consolidated minimal wording (to be applied before re-freeze; the claims are frozen)

C1 kill_rule, append: "; or if any re-grounded recheck line differs from the exact form `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>.md`; or if any row's current-claim cell is empty, any anchor is r46-c1-gate.py itself, or any anchored range exceeds 3 lines; or if recheck-audit.py at the lane root (never a copy) disagrees with the counter's L1 gated count; or if corpus/instruments/r46-c1-gate.py at the scored tree is not sha256 b0c730c8…; or if the printed `c1-gate fixed=` line is not read (exit code alone never scores)."
C1 after-clause: replace "every BASE line kept (append-only)" with "every BASE line except its `recheck:` line kept in order; the BASE recheck line is replaced in place."
C1 plain 1: replace with `grep -lE 'test -d (~/|\$HOME|/home/)' corpus/knowledge/*.md | wc -l`, target ≤21.

C2 kill_rule, append: "; or if fewer than two `If `/`When ` decision sentences exist in `## Scope and decision rule`; or if any citation spans more than 3 lines; or if the F28 name cell is not `GitHub private vulnerability reporting`; or if the entry does not name F27 and F04 (<2 mentions); or if any base knowledge entry differs from base; or if R46_PINS_OVERRIDE is set in the grading environment; or if scripts/sources-census.sh is not pinned to the freeze-time sha256."

## 5. Limitations
- Fixtures were built in scratch from the freeze export as single mutations and removed on exit. They are not the lane's eventual drafts; no re-ground or F28 draft was built by this seat (not in this seat's item).
- The lane tip has no re-grounds or F28 row yet, so the counters were not run at the lane tip; all green/red readings above are on constructed trees.
- Semantic clauses (rows support the entry's claims; the decision rule is actionable; "separate from SECURITY.md") cannot be settled by one command. I give one-command proxies only where they discriminate the fixtures; the rest stays with the non-author reading.
- C1-j and C2-g are not tested; they are read from the source.
- No counter, control, gate or claims file was edited; no git or jj mutation; no file in the fleet repo or sibling lane touched.
