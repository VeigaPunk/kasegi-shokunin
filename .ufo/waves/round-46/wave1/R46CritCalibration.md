VERDICT: BROKEN

Headline counts in the self-assessment match the repo (gated 24/64, 23 `test -d ~/Projects` lines, 64 knowledge entries, 72 SOURCES rows, 27 frontier rows; frozen controls and freeze-check reproduce). Five mismatches the round must repair (F1-F5), and both frozen counters accept degenerate or semantically wrong input that their claim text forbids (F6-F10). Every number below is a re-run by this seat.

## Scope and method

- Lane HEAD `323d1f5` (read-only `git status`/`show`/`archive`); freeze `9f23aab`; base `914ca0b`.
- Scratch trees: `base` = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure`; `freeze` = `git archive 9f23aab corpus SKILL.md PROVINCE.md SCORECARD.md SHONEN.md LOG.md .ufo/waves/round-46/controls`, plus `claims.json` and `freeze.txt` via `git show`.
- Counters were run from the frozen bytes (`corpus/instruments/r46-c1-gate.py` sha256 `b0c730c8…`, `r46-c2-gate.py` sha256 `0ee95857…`) with `--root` set to a scratch tree. Live-lane checks ran against the lane.
- Drafts (C1 re-grounds, F28 entry) and mutants were built and graded in scratch. Scratch is removed on exit; the draft texts are reproduced in Appendices A and B.

## 1. Calibration table

Columns: assertion (path:line) | observed | match? | command.

| # | assertion (path:line) | observed | match? | command |
|---|---|---|---|---|
| 1 | claims.json C1.before: `executes=40 gated=24 broken=0` | `executes=40 gated=24 broken=0` (live); `strict pass=64/64 cdroot_fail=0 instrument_fail=0 own_fail=0` | yes | `python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet` |
| 2 | claims.json C1.before: `gap: 24 of 64 rechecks still gated` | `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` | yes | `python3 corpus/instruments/score-gap.py \| grep '^gap:'` |
| 3 | claims.json C1.plain: 23 entries open with `test -d ~/Projects` | `23` | yes | `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md \| wc -l` |
| 4 | claims.json C1.before: 64 `recheck:` lines | 64 (one per entry); recheck-audit `lines=64 total=64` | yes | `grep -c '^recheck:' corpus/knowledge/*.md \| awk -F: '{s+=$2} END{print s}'` |
| 5 | claims.json C2.before: 64 knowledge entries | `64` | yes | `ls corpus/knowledge/*.md \| wc -l` |
| 6 | claims.json C2.before, C2.plain: 72 SOURCES rows | `72`; ids S001..S072 contiguous, no duplicates (only S073 absent) | yes | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` |
| 7 | claims.json C2.before: 27 frontier rows F01-F27 | `27` | yes | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` |
| 8 | SCORECARD.md:1756 (round-45 row): `27, 72, 64` after | `27`, `72`, `64` | yes | `grep -cE '^\| F[0-9]+ \|' corpus/README.md; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; ls corpus/knowledge/*.md \| wc -l` |
| 9 | corpus/README.md:653 (r45 amendment): `27/27 admitted` | matches row count 27 | yes | `sed -n '653p' corpus/README.md` |
| 10 | PROVINCE.md frontier lines vs README rows (27) | ids F01-F27 all covered: F01-F10 at :38 and :57, F01-F15 at :69, F01-F08 at :118 and :131; one amendment line per F16..F27 at :74, :75, :77, :78, :80, :156, :158, :161, :163, :165, :167, :169 (12 lines = F16..F27) | yes | `grep -nE '^\[r[0-9]+ Frontier amendment' PROVINCE.md; grep -noE 'F0[0-9][–-]F[0-9]{2}\|F01-F[0-9]+' PROVINCE.md` |
| 11 | SHONEN.md:3 "the round-35 paragraphs appended at the end of this file are the boxes' current evidence" | round-35 block sits at SHONEN.md:89-170; file is 303 lines; last `##` heading is `## Round 42 evidence` (:232); round-43/44 paragraphs at :234-303 are unheaded; no round-35 text at the end | NO (F1) | `grep -n 'round-35' SHONEN.md; grep -n '^## ' SHONEN.md; wc -l SHONEN.md` |
| 12 | SHONEN.md boxes: all four remain `[~]`; SCORECARD depth:verifiability stays 4 | every box line is `[~]`; no `[x]`; SCORECARD `4 held` at :1747 | yes | `grep -nE '\[[ xX]\]\|☐\|☑\|✓\|✗\|- \[' SHONEN.md \| grep -v '\[~\]'` (empty, rc=1); `grep -n 'depth:verifiability' SCORECARD.md \| tail -2` |
| 13 | SCORECARD.md:1771-1774 depth gate: "state each claim's before-value per start tree (base and freeze tree)" | claims carry `before` and `freeze_tree_reading`; reproduced: C1 base `fixed=1/7`, freeze `fixed=1/7`; C2 base `fixed=1/7`, freeze `fixed=2/7` | yes | `python3 corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>`; `python3 corpus/instruments/r46-c2-gate.py --root <tree>` (tree = base, freeze) |
| 14 | SCORECARD.md:1771-1774 depth gate: "run capture-binding-check.py --root ... before dispatching a wave" | freeze tree: `FAIL rule=no-row record=S073 dir=round-46` / `records=60 bound=59 unbound=1`, exit 1; live tip: identical, exit 1; base: `records=59 bound=59 unbound=0`, exit 0; no pre-dispatch receipt in `.ufo/waves/round-46` | NO (F2) | `python3 corpus/instruments/capture-binding-check.py --root <tree>; echo rc=$?` |
| 15 | SCORECARD.md:1771-1774 depth gate: "census before dispatching a wave" | `controls/sources-census-before.txt` shows `census-exit=0`; live `sources-census.sh validate` rc=0 | yes | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md; echo rc=$?` |
| 16 | SCORECARD.md:1774 coverage gate: "non-author admit/reject spot-check of S071/S072 before any coverage statement beyond +1 row" | C2 claims exactly +1 SOURCES row and +1 frontier row, so the gate is not triggered on its own words; the gate is not in claims.json; no committed non-author record exists (only an uncommitted scribe note, `wave1/R46ScribeRowsA.md:53`) | partial (F4) | `grep -rniE 'spot-check\|admit/reject' .ufo/waves/round-46 -l`; `grep -c 'spot' .ufo/waves/round-46/claims.json` (0) |
| 17 | SCORECARD.md:1774 coverage gate: "keep rejected-row captures outside corpus/source-snapshots/" | S072 capture not under `corpus/source-snapshots/` (round-45 dir holds `S071.txt` and `manifest.json` only); SOURCES.md:78 anchors S072 at `.ufo/waves/round-45/source-recon/S072.txt` | yes | `ls corpus/source-snapshots/round-45; sed -n '78p' corpus/SOURCES.md \| cut -c150-400` |
| 18 | claims.json C2.frontier_step: "S072/S070 supersede pair recorded in the registry notes" | `## Registry changes` (SOURCES.md:115-) has 0 bullets naming S071 or S072 (and 0 for S060, S064); last count-bearing bullet is the round-44 one at :156; S070 row is `rejected` (:76), S072 row is `rejected` (:78) | NO (F3) | `sed -n '115,$p' corpus/SOURCES.md \| grep -c 'S072'; sed -n '115,$p' corpus/SOURCES.md \| grep -c 'S071'` (both 0) |
| 19 | SOURCES.md prose row count | last count prose `Registry 55 rows pre-append → 59 post-append` at :149; table is 72 rows; no count bullet for rounds 40-45 | NO (stale; F3) | `grep -n 'rows pre-append' corpus/SOURCES.md \| tail -1` |
| 20 | claims.json C1.after: "every BASE line kept (append-only)" | counter L5 (`r46-c1-gate.py:198-199`) compares only non-recheck BASE lines (`if not RECHECK_RE.match(x)`); the claim text does not exempt the recheck line | NO (wording, F5) | `sed -n '198,199p' corpus/instruments/r46-c1-gate.py` |
| 21 | freeze-controls.txt: `controls total=9 red=9 green=0` and frozen gate readings | re-run from the frozen generator in scratch: output byte-identical to committed `controls/freeze-controls.txt` (diff empty); final line `controls total=9 red=9 green=0` | yes | `python3 .ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6… --work <scratch>`, then `diff` against the committed file |
| 22 | freeze.txt: `freeze-check claims=2 base_ok=2`; claims/gate/S073/manifest sha256 | `freeze-check claims=2 base_ok=2 exit=0`; sha256 match: claims `e56ebf87…`, c1 `b0c730c8…`, c2 `0ee95857…`, S073 `66c96a61…`, manifest `01f02572…` | yes | `python3 corpus/instruments/freeze-check.py --claims <freeze>/.ufo/waves/round-46/claims.json --tool-root <freeze> --base <base>`; `sha256sum` on the four files |
| 23 | claims.json C2.after: "eight located manifest quotes" | `recheck-rc=0 quotes-ok=8 frozen-cores-missing=0` | yes | `python3 corpus/instruments/r46-c2-gate.py --root <freeze>` (G4) |
| 24 | claims.json C2 `census exit 0` | `census-rc=0 ok-line=1` (freeze and live) | yes | same counter, G7 |
| 25 | r46-c2-gate.py:54 `CENSUS` depends on a fleet-root script outside the lane; freeze.txt pins no census hash | file exists (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, mtime 2026-10-19); not in the lane tree or freeze.txt | NO (F9) | `ls -la /home/vgpnk/Projects/shokunin/scripts/sources-census.sh; grep -n census .ufo/waves/round-46/freeze.txt` (no match, rc=1) |
| 26 | tip measurement script | `controls/final-measure.sh` is untracked (`?? .ufo/waves/round-46/controls/final-measure.sh`) and runs `capture-binding-check.py`; not in freeze.txt | NO (F10) | `git -C <lane> status --short` |
| 27 | instruments/README.md:489 "gap: 24 of 44 rechecks" | dated block "Digests after the C1 edits" (:468, 2026-10-26); denominator 44 is historical; current is 64 | n/a (dated) | `sed -n '468,492p' corpus/instruments/README.md` |

## 2. Findings the round must repair

F1 (row 11). SHONEN.md:3 names the round-35 paragraphs "at the end of this file" as the boxes' current evidence. They are not at the end: they sit at :89-170, and the end (:234-303) holds round-43/44 evidence with no heading. Repair: point the header at the real current block, or add a heading at :234.

F2 (row 14). The planned depth gate (SCORECARD.md:1773) says run `capture-binding-check.py --root` before dispatch. At the freeze tree and at the live tip it exits 1 with `FAIL rule=no-row record=S073 dir=round-46` (the S073 capture is committed; its SOURCES row lands later). The base exits 0. Dispatch proceeded (`wave1.ready.dispatched` exists) with no recorded red reading. Repair: record the red reading and make the S073 row a stated precondition of the C2 landing, or re-run and record after landing.

F3 (rows 18-19). claims.json C2.frontier_step says the S072/S070 supersede pair is "recorded in the registry notes". At freeze and tip, `## Registry changes` has no S071 or S072 bullet. The last count prose is the round-36 `55 → 59`. The S072 row says `rejected` but does not name S070 as superseded. Repair: append registry bullets for S071/S072 (and S060/S064, which also lack bullets), or drop the claim; refresh the count prose or state that it is no longer maintained.

F4 (row 16). The planned coverage gate (SCORECARD.md:1774) is not frozen in claims.json, and no committed non-author admit/reject record of S071/S072 exists. The gate is not triggered by C2's +1 row, but the round should say so in the claim, not leave it implied by a planning line.

F5 (row 20). claims.json C1.after promises "every BASE line kept (append-only)". The counter (r46-c1-gate.py:198-199) exempts recheck lines from the append-only check. The exemption is necessary (the first recheck line must change for the entry to stop being gated), so the counter is right and the claim wording is wrong. Repair the wording: "every non-recheck BASE line kept".

F6 (C1 counter, recheck-line holes). The claim requires a recheck line that "runs `r46-c1-gate.py --entry` on itself with no ~/ or $HOME path". The counter enforces neither:
- `CD_RE` (r46-c1-gate.py:61) strips any leading `cd <path> &&` before the no-`~/` test (line 187). A `~/` path inside that prefix is never tested. Mutant m1 (`recheck: cd ~/Projects/shokunin/kasegi-shokunin && python3 …`) grades 7/7.
- L3 (line 187) checks substrings, not that the gate command executes. Mutant m2b (`recheck: true # r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`) grades 7/7; running that line executes nothing (`bash -c "true # …"` exits 0). The frozen control only covers a bare `true`, which L3 does catch.
Repair: strip only the lane's own `cd` prefix, reject `~` anywhere in the line, require the gate to be the executed command (not in a comment or behind `true`), and add both mutants to freeze-controls.py.

F7 (C1 and C2 semantics). A green counter is not a semantic check. C1 mutant m3 (rows whose claims say nothing, all anchored to the shebang `#!/usr/bin/env python3`) grades 7/7. C2 graded 7/7 on a first F28 draft that said the Linux process keeps AI-assisted finds off public lists, the opposite of `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:23` ("you must treat it as public"); the sentence was uncited, so G5 never looked at it. The claim's kill rule relies on a non-author reading for exactly this reason; the SCORECARD and round receipts should not present a 7/7 as evidence of support.

F8 (C2 counter holes). Verified on mutants of the F28 draft:
- G5 has no span-width limit (r46-c2-gate.py:267 uses whatever `N-M` the author writes). Citing a real quote as `(`S073.txt:1-589`)` locates it anywhere in the capture; mutant c2m1 grades `fixed=7/7`. The narrow wrong-line control c2m2 (`S073.txt:560` for a quote at :577) grades `6/7`, so the limb works for narrow citations. Repair: cap span width (C1 uses 40 lines).
- G2 checks that the four section headings exist, not that they have bodies. Mutant c2m4 (empty `## Limits`) grades `fixed=7/7`. Repair: require non-empty section bodies.
- G2 checks the entry's `recheck:` line by substring. Mutant c2m3 (`recheck: true # source-recheck.py … --source S073`) passes G2. G4 re-runs the real tool, so the counter total is unaffected, but the entry's own recheck is not verified.

F9 (row 25). r46-c2-gate.py:54 reads the census from `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane and not hashed in freeze.txt. G7 can change with a file the lane does not control. Repair: pin the census sha in freeze.txt, or vendor the check into the lane.

F10 (row 26). `controls/final-measure.sh` is untracked and names `capture-binding-check.py`, the planned gate from F2. It is not in the freeze record. Repair: commit it with its sha in freeze.txt, or drop it.

## 3. Falsification and re-runs

Frozen readings (re-run at the stated trees):

```
C1 base   : gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64 … c1-gate fixed=1/7 exit=1
C1 freeze : gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64 … c1-gate fixed=1/7 exit=1
C2 base   : gate G1 pass=0 read=rows=27 admitted=27 dup=0 … c2-gate fixed=1/7 exit=1
C2 freeze : gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0 … c2-gate fixed=2/7 exit=1
freeze-check claims=2 base_ok=2 exit=0
controls total=9 red=9 green=0   (rerun byte-identical to controls/freeze-controls.txt)
```

Negative controls (frozen, rerun): C1 marker-only `fixed=3/7`, gutted-entry `fixed=6/7`; C2 junk-row `4/7`, fabricated-quote `4/7`, uncited-filler `5/7`. All red, as the controls file records.

C1 mutants (built from the honest C1 draft, Appendix B):

```
m1  (cd ~/Projects/… prefix)            : gate L3 pass=1 read=recheck-lines-clean=2 … c1-gate fixed=7/7 exit=0
m2  (cd /home/… && true # … /home/…)    : gate L3 pass=0 read=bad=claim-gates.md … c1-gate fixed=6/7 exit=1
m2b (recheck: true # r46-c1-gate.py …)  : gate L3 pass=1 read=recheck-lines-clean=2 … c1-gate fixed=7/7 exit=0
m3  (six shebang-token rows, unrelated) : gate L6 pass=1 read=mutants=12 survivors=none … c1-gate fixed=7/7 exit=0
```

C2 mutants (built from the honest F28 draft, Appendix A):

```
c2m1 (S073.txt:1-589 citation)           : gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5 … c2-gate fixed=7/7 exit=0
c2m2 (S073.txt:560 for a :577 quote)     : gate G5 pass=0 read=spans=5 located=4 failed=1 uncited=0 cores=4/5 … c2-gate fixed=6/7 exit=1
c2m3 (recheck: true # source-recheck.py) : gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=7 xrefs=2/2 … c2-gate fixed=7/7 exit=0
c2m4 (empty ## Limits)                   : gate G2 pass=1 read=… sections=4/4 … c2-gate fixed=7/7 exit=0
```

Drafts graded green in scratch:

```
C1 draft (7 re-grounded rows in each of claim-package-contract.md and claim-gates.md)
  gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
  gate L3..L6 pass=1 (L6 mutants=14 survivors=none)
  gate L7 pass=1 read=still-gated=22 changed=none
  c1-gate fixed=7/7 exit=0

F28 draft (Appendix A)
  gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
  gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=7 xrefs=2/2
  gate G3 pass=1 read=row-S073=ok
  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
  gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5
  gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
  gate G7 pass=1 read=census-rc=0 ok-line=1
  c2-gate fixed=7/7 exit=0
```

Drafting finding: my first C1 claim-gates draft put all seven rows in one anchor file and graded `reground entry=claim-gates.md rows=7 ok=7 files=1 exit=1`. The two-anchor-files limb did its job; moving one row to the fixture manifest fixed it.

These drafts are not committed and change no score. The F28 draft also needs the README F28 row and the SOURCES S073 row (Appendix A), which the counter checks structurally.

## 4. Limitations

- Read-only seat: no commit, no lane edits. Drafts and mutants exist only in scratch (removed on exit); the drafts are reproduced in the appendices.
- Semantics of the F28 draft and the C1 rows were checked only by direct reading of S073.txt:553-579 and the Linux row at :23. A non-author reading is still needed (the kill rule says so).
- Base C2 `fixed=1/7` is from a fresh run at the base tree and from the frozen-controls rerun; freeze C2 `2/7` is from a fresh run at the freeze tree.
- The live-tip `capture-binding-check.py` reading is a single run at `323d1f5`; a later tip may differ.
- I did not run freeze-check or the controls at the current tip; both were run at the freeze tree and the base export.
- `score-gap.py` was run with `--root <scratch>` once; its output matched the live line, but I did not verify that the script honors `--root`, so no freeze-tree count rests on it.
- Host-dependent: r46-c2-gate.py's G7 reads a fleet-root script (F9); a rerun on another host may differ.
- Untracked lane files in `git status` (`wave1/*.draft/`, `wave1.ready*`, `controls/final-measure.sh`) were observed, not changed.

## Appendix A — F28 draft (graded 7/7 in scratch; not committed)

README row (insert after the F27 row, `corpus/README.md:651`):

```
| F28 | GitHub private vulnerability reporting (the reporter flow of a repository's built-in advisory form) | admitted | knowledge/github-private-vulnerability-reporting.md | S073 | Read enablement first: the form exists only where the repository switched it on, is separate from SECURITY.md, and gives the reporter no merge path; disclose AI assistance when used. |
```

SOURCES row (insert in the Registry before `## Paths`):

```
| S073 | GitHub Docs: Privately reporting a security vulnerability — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately | docs | A | reporter-side flow of the repository advisory form | sha256 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 | enablement per repository, default required fields, optional AI-assistance field, automatic collaborator credit, maintainer-only merge from the private fork | mined | 2026-10-28 | 180d | corpus/knowledge/github-private-vulnerability-reporting.md |
```

Entry `corpus/knowledge/github-private-vulnerability-reporting.md`:

```
source: S073 — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — GitHub Docs, Privately reporting a security vulnerability (capture 2026-10-28)
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073  # re-derives the S073 capture digest and the eight quote checks

# GitHub private vulnerability reporting: the reporter flow

Frontier F28. A public repository's built-in advisory form is a reporter-side channel that is separate from the repository's SECURITY.md file and works only where the maintainers have switched it on. This entry states the reporter's decision rule for that form and nothing about the maintainer's triage after submission.

## Scope and decision rule

The feature belongs to public repositories whose owners or administrators have enabled it. The decision rule below is the order in which a reporter must decide, using only the pinned capture `corpus/source-snapshots/round-46/S073.txt`.

| Step | Decide | Source |
|---|---|---|
| 1 | Is the feature enabled on the repository? If not, the form is not an option; follow the route the security policy names or ask the maintainers for a preferred contact. | S073 lines 564-566 |
| 2 | Do you hold admin or security permission on the repository? Then file no report and create a draft security advisory directly. | S073 line 563 |
| 3 | Is there a SECURITY.md policy? It is displayed above the form; read it before filling in anything. | S073 line 564 |
| 4 | Fill the form. By default the four fields are summary, details, proof of concept and impact statement; maintainers may require more. | S073 line 573 |
| 5 | Optionally tick the AI-assistance box. The page presents the box as optional. | S073 line 574 |
| 6 | After submission the reporter is added as a collaborator and a credited user without further action. | S073 line 577 |
| 7 | Optionally start a temporary private fork; only the repository maintainer can merge from it. | S073 line 578 |

The five load-bearing statements of the page are quoted here exactly as the capture holds them. Each quote is followed by its line citation in the pinned capture.

Enablement is per repository: “You can only report vulnerabilities privately for repositories where this feature is enabled.” (`S073.txt:564`)

The required content is a floor set by the default form: “By default, you must provide a summary, details, proof of concept, and impact statement.” (`S073.txt:573`)

The AI-assistance field is optional: “Optionally, select I used AI assistance to find or write up this report.” (`S073.txt:574`)

Credit and access follow from submission alone: “GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.” (`S073.txt:577`)

The fork gives the reporter no merge path: “Note that only the repository maintainer can merge changes from that private fork into the parent repository.” (`S073.txt:578`)

## Overlap and novelty

The entry does not restate SECURITY.md guidance; the page itself says the two are separate (S073 line 564). The closest neighbours in the corpus are the Linux kernel's e-mail channel and the AI-assisted validation entry. The Linux process says an AI-assisted find must be treated as public (`corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:23`). GitHub's form does not refuse AI-assisted reports; its AI-assistance checkbox is optional (S073 line 574). The validation rule of F04 still applies before submission: an AI-originated finding is a candidate until it is reproduced (`corpus/knowledge/ai-assisted-finding-validation.md:7`). Neither neighbour grants a route into GitHub's form, and the form grants no validation by itself.

## Limits

The capture was taken on 2026-10-28 from one page. The page does not state how long a private report is retained, how fast a maintainer must respond, or whether the AI-assistance box changes triage. The page states that maintainers can customize the form and require more fields, so the default floor is a floor and not the form a given repository shows. The entry reads no repository, no advisory and no live form; it grades the reporter's own steps against the page. Nothing here is a claim about how often the feature is enabled.

## Falsifiable package rule

A reporter's package is ready for this channel only when all of the following hold, each checkable against the capture:

1. The repository shows private vulnerability reporting as enabled; otherwise the package goes to the route the security policy names.
2. The package holds a summary, details, a proof of concept and an impact statement, or a recorded reason that the repository's customized form asks for something else.
3. The AI-assistance box is set exactly when AI assistance was used to find or write up the report.
4. The reporter expects, and accepts, automatic collaborator access and credit on the proposed advisory.
5. Fix work in a private fork gives the reporter no merge path: the reporter does not expect to merge it, because only the maintainer can.

The rule is falsified by a package that is filed where the feature is off, that omits a default field while claiming the form was complete, or that assumes the reporter can merge from the fork. The rule is not falsified by a maintainer who later customizes the form; that case is the customization clause of the Limits section.
```

## Appendix B — C1 re-ground rows (graded 7/7 in scratch; not committed)

Recheck line in each of the two entries (replaces the BASE `test -d ~/Projects/bounties` line in place; no `~` path, no `$HOME`):

```
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>.md
```

`claim-package-contract.md` — appended `## Re-ground (round 46)` section:

```
| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | The six contract files are required as regular, non-symlink, non-empty files | `corpus/instruments/claim-package-check.py:51` | `six contract files present` |
| G2 | The manifest schema_version is exactly evidence-manifest/v1 | `corpus/instruments/claim-package-check.py:305` | `evidence-manifest/v1` |
| G3 | decision.scope_signal must be exactly NO_SCOPE_OBJECTION | `corpus/instruments/claim-package-check.py:460` | `NO_SCOPE_OBJECTION` |
| G4 | the policy digest field is policy_sha256 | `corpus/instruments/claim-package-check.py:524` | `policy_sha256` |
| G5 | the claim review carries a hard_gates object | `corpus/instruments/claim-package-check.py:591` | `hard_gates` |
| G6 | claimable=true requires every hard gate to PASS | `corpus/instruments/claim-package-check.py:616` | `claimable=true,gates-not-pass` |
| G7 | the exemplar manifest carries schema_version evidence-manifest/v1 | `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | `evidence-manifest/v1` |
```

`claim-gates.md` — appended `## Re-ground (round 46)` section:

```
| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | file-presence gate: the six package files are checked as present regular files | `corpus/instruments/claim-package-check.py:51` | `six contract files present` |
| G2 | manifest gate: schema_version must read evidence-manifest/v1 | `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | `evidence-manifest/v1` |
| G3 | scope gate: the decision scope_signal must be NO_SCOPE_OBJECTION | `corpus/instruments/claim-package-check.py:460` | `NO_SCOPE_OBJECTION` |
| G4 | provenance and policy gate: the policy digest is read from policy_sha256 | `corpus/instruments/claim-package-check.py:524` | `policy_sha256` |
| G5 | status gate: the claim review must hold hard_gates | `corpus/instruments/claim-package-check.py:591` | `hard_gates` |
| G6 | status gate: claimable=true with a non-PASS hard gate is refused | `corpus/instruments/claim-package-check.py:616` | `claimable=true,gates-not-pass` |
| G7 | the gate rule order is fixed as a tuple in the committed gate | `corpus/instruments/claim-package-check.py:90` | `_GATE_RULE_ORDER` |
```

Both entries pass the aggregate's per-entry limb (`L4 pass=1 read=entry-mode-green=2`) and the aggregate reads `c1-gate fixed=7/7 exit=0`. I did not run `--entry` standalone on each entry and print its own line; the per-entry result is the L4 reading. The rows show the tokens are present; they do not prove the entries' prose claims are true. A non-author reading is still required.
