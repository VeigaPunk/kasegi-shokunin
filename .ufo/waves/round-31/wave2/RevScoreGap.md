# RevScoreGap — round 31 wave 2 review receipt

- Seat: `RevScoreGap` (reviewer; leaf, one write scope: this file). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `b374feb`, claims freeze `738a779`).
- Subject: `corpus/instruments/score-gap.py`, reviewed against `considerthese/2026-10-25.md` proposal 2 ("Track distance to the next score, not just improved, held", lines "Proposal: I compute and report that gap daily from committed bytes…").
- Reviewed bytes: `score-gap.py` sha256 `855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb` (matches the README "landed" digest at `corpus/instruments/README.md:463`, so this is the wave-1 quiescent file, not a mid-edit read).
- Answering model: `opencode-go/deepseek-v4.1-flash` (as routed; never passed by me).
- Tools installed/upgraded: none (stdlib python3 only). No pacman, no network fetch.
- Write footprint: this receipt + `/tmp` scratch dirs, all deleted (`leftover_count=0` after cleanup, see §Cleanup).

## Verdict: `defect`

The five printed field groups and their numbers are correct on today's bytes and each is traceable to a real command, except one: the **census** block prints a `cmd:` that provably cannot produce the `census-lane` value it sits above. Second defect: the advertised `--selftest` `recheck-mode=stub` fallback cannot run — its fixture data is written in a non-JSON dialect that `json.load` rejects, so forcing the fallback crashes with `KeyError: 'recheck'` instead of reporting. Both are small, local fixes (one string, one `json.dumps`), but "every printed number comes from the stated command" and "the fallback works" are exactly what this instrument sells, so the honest verdict is `defect`, not `weak`.

Strengths verified: gap line computed from field 1 (not typed); no score-move claim in docstring or output; writes nothing (proved by running against a `chmod -R a-w` lane copy); cwd-invariant (lane root vs `cd /` byte-identical); exit-2 fail-closed on each missing/unyieldable input.

## 1. Q1 — does every printed number come from a stated command over committed bytes?

Mostly yes, one counterexample.

### 1a. Reproducing the four `cmd:` lines from the report

Report (from the lane):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=44 executes=20 gated=24 broken=0 exit=0
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- (lane total|SKILL\.md alone): ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
EXIT=0
```

Field 1 reproduced by the printed command (`exit` here was 0; see §6 for why a copy prints 1):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/recheck-audit.py --root "$PWD" --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
EXIT=0
```

Field 2 reproduced by the printed command (cwd = lane root):

```
$ python3 -B corpus/instruments/anchorcheck.py SKILL.md | grep '^=='
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

Field 4 reproduced, and the quoted sentence is verbatim (15 words, ≤ Q3's 25-word cap, location `SCORECARD.md:331`):

```
$ grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md | cut -c1-200
331:| depth:verifiability (C1, lowest axis) | 4 | **4** | **Improved, score held.** Legacy knowledge entries carrying `source:`/`verified-at:`/`recheck:` (appended end-of-file `## Provenance` block, s
$ grep -o 'Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims\.' SCORECARD.md
Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims.
$ grep -c 'Threshold for 5' SCORECARD.md
1
```

### 1b. The census `cmd:` is false — **FINDING D1**

`score-gap.py:183` prints `grep -nE '^Numerator = |^- (lane total|SKILL\.md alone): ' corpus/instruments/citation-survival.md`, but the value `census-lane: 134/1480 = 9.05%` is parsed by `CENSUS_LANE_RE` (`score-gap.py:71-73`), which requires the parenthetical: `^- lane total \(SKILL\.md \+ corpus\): \*\*(\d+)/(\d+) = ([\d.]+)%\*\*$`. The printed pattern demands a colon immediately after `lane total`, which the file does not have. Reproducing the printed command yields **two** lines and neither contains the printed rate:

```
$ grep -nE '^Numerator = |^- (lane total|SKILL\.md alone): ' corpus/instruments/citation-survival.md | cut -c1-90
29:Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citatio
31:- SKILL.md alone: **32/506 = 6.32%**
$ grep -nE '^Numerator = |^- (lane total \(SKILL\.md \+ corpus\)|SKILL\.md alone): ' corpus/instruments/citation-survival.md | cut -c1-90
29:Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citatio
31:- SKILL.md alone: **32/506 = 6.32%**
33:- lane total (SKILL.md + corpus): **134/1480 = 9.05%**
```

So `census-definition` and `census-skill` are reproducible from the printed command, `census-lane` is not. This contradicts the module docstring ("each with the command it came from", `score-gap.py:5-9`), the printed header, and `SKILL.md:1071` ("each with the command it came from"). Fix: print the pattern the code actually uses (`^- lane total \(SKILL\.md \+ corpus\): `). The *value* is right; only its stated provenance is wrong.

## 2. Q2 — can each field change? (selftest fixture)

Yes, all seven field labels move between fixtures a and b, and the selftest asserts it rather than printing a total:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py --selftest; echo "EXIT=$?"
selftest recheck-mode=real
selftest exit-a                       ok rc=0 want=0 err=''
selftest no-write-a                   ok tree digest unchanged=True
selftest exit-b                       ok rc=0 want=0 err=''
selftest no-write-b                   ok tree digest unchanged=True
selftest recheck.lines                ok a=2 b=3
selftest recheck.executes             ok a=1 b=2
selftest recheck.gated                ok a=1 b=0
selftest recheck.broken               ok a=0 b=1
selftest anchorcheck.in-range         ok a=1 b=2
selftest anchorcheck.bad              ok a=2 b=0
selftest anchorcheck.lost-recorded    ok a=1 b=3
selftest anchorcheck.origin           ok a=0 b=1
selftest anchorcheck.outside-base     ok a=1 b=0
selftest anchorcheck.base-absent      ok a=1 b=0
selftest anchorcheck.exit             ok a=1 b=0
selftest census-lane                  ok a='100/200 = 50.00%' b='3/4 = 75.00%'
selftest census-skill                 ok a='10/20 = 50.00%' b='3/8 = 37.50%'
selftest census-definition            ok a='Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denomin' b='Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denomin'
selftest threshold                    ok a='SCORECARD.md:5 "Threshold for 5: a non-author audit passing ' b='SCORECARD.md:10 "Threshold for 5: all source chains passing '
selftest gap                          ok a='1 of 2 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims' b='0 of 3 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims'
selftest gap-computed                 ok got='1 of 2 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims' want='1 of 2 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims'
selftest exit2-missing-census         ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: corpus/instruments/citation-survival.'
selftest exit2-missing-recheck        ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: corpus/instruments/recheck-audit.py ('
selftest exit2-missing-scorecard      ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: SCORECARD.md (/tmp/score-gap-selftest'
selftest exit2-no-threshold           ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE SCORECARD.md no longer names the score-5 threshold ('
selftest fields=7 failures=0
EXIT=0
```

Notes: the fixture pairs are genuinely different inputs (stub/real recheck summaries, two SKILL.md anchor sets, two census files, two SCORECARD files at different line numbers). `census-definition` moves only by its trailing wording, so that arm proves "printed, not constant" but not much more — acceptable, recorded under residual risk R4. The `threshold-matches: N` arm is not exercised by the selftest; I exercised it: appending a second threshold row to a scratch SCORECARD gives `threshold-matches: 2 (first line used)` and exit 0 (below, §5).

## 3. Q3 — is the `gap:` line computed, not typed?

Yes, on three independent pieces of evidence:

1. Code path: `gap_line(recheck)` (`score-gap.py:221-226`) formats `recheck["gated"]` and `recheck["lines"]`, and `report()` calls it with field 1's dict (`score-gap.py:279-281`); no literal numbers anywhere in the module (grep for the printed text finds only the format string).
2. `selftest gap-computed` recomputes the expectation from fixture a's own parsed `recheck` fields and compares — `ok`.
3. Both fixtures print different gaps derived from their own numbers: `1 of 2` (a: gated=1 lines=2) and `0 of 3` (b: gated=0 lines=3), and no limb strings beside them.

Live: `gap: 24 of 44 rechecks still gated on a lost base` = field 1's `gated=24`, `lines=44`. Note the proposal's example figure was "23/37 rechecks gated" (r25 bytes) — the reporter correctly reports today's 24/44, not the proposal's stale number. Semantic caveat under R1.

## 4. Q4 — does it claim no score move?

Yes, in both required places, and nowhere does it assert a move:

- Docstring, second paragraph (`score-gap.py:10-14`): "THIS IS NOT A CLAIM AND IT ASSERTS NO SCORE MOVE… no field here is evidence for or against a score change, and a green run does not mean a score is due."
- Output line 1: `score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)`.
- Argparse description repeats it: "…(NOT a claim; asserts no score move)".
- Output values: `root:`, four `source: … sha256=`, four `cmd:`, five field groups, one `gap:`. No before/after score column, no "improved"/"held" word.

## 5. Q5 — does it write nothing?

Yes. Three checks:

(a) Read-only lane copy (the assignment's strace-free check) — whole lane except `.ufo/.jj/.git` copied, then `chmod -R a-w`, run from `cd /`:

```
$ S=$(mktemp -d /tmp/scoregap-ro2.XXXXXX); for e in AGENTS.md LOG.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md considerthese corpus plans; do cp -a "$L/$e" "$S/"; done; chmod -R a-w "$S"
$ cd / && python3 "$S/corpus/instruments/score-gap.py" --root "$S" | sed -n '1,3p;6,8p'
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /tmp/scoregap-ro2.yL5OoB
source: corpus/instruments/recheck-audit.py sha256=5d4842da…          (identical to the lane run)
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /tmp/scoregap-ro2.yL5OoB --quiet
EXIT=0
```

It runs to completion (exit 0, all five field groups printed) on a tree where every write would fail — so the reporter and the two subprocess instruments write nothing. `--selftest` also passes on that read-only copy (`SELFTEST_EXIT=0`, `selftest fields=7 failures=0`).

(b) Fixture-level no-write assertion inside the selftest: `no-write-a ok`, `no-write-b ok` (tree digest over the whole fixture root before/after the report, §2).

(c) Lane-level: after a run, no non-`.ufo` file in the lane is newer than the run marker, and `git status --porcelain` shows only the 12 pre-existing untracked `.ufo` paths (round-29/30/31 receipts, sibling seats' files):

```
$ touch /tmp/scoregap-ref && sleep 1 && python3 corpus/instruments/score-gap.py >/dev/null 2>&1; echo "run_exit=$?"
run_exit=0
$ find . -newer /tmp/scoregap-ref -type f -not -path './.ufo/*' -not -path './.jj/*' -not -path './.git/*'
(no output)
```

Multi-threshold branch (untested by the selftest) writes nothing either — run inside a scratch copy:

```
$ printf '\n| depth:verifiability | 4 | 5 | Threshold for 5: a second bar line with 0 unsupported current claims. |\n' >> "$S/SCORECARD.md"
$ cd / && python3 "$S/corpus/instruments/score-gap.py" --root "$S" | sed -n '/\[4\]/,$p'
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
threshold-matches: 2 (first line used)
[5] gap
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
EXIT=0
```

## 6. Q6 — runs from the lane and from `cd /`

Byte-identical output and exit 0 from both, because `lane_root()` derives the root from `__file__` and every subprocess gets an absolute `--root`/`cwd`:

```
$ cd / && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py; echo "EXIT=$?"
<all 22 lines identical to §1a, including root: /home/vgpnk/Projects/shokunin/kasegi-shokunin>
EXIT=0
```

Caveat, not a defect (R2): the *propagated* field-1 `exit` is root-sensitive, because the audited `recheck:` lines hardcode the absolute lane path (`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/…`). On the read-only copy, `recheck-audit.py` reports `strict pass=1/44 cdroot_fail=43 … exit=1`, and the reporter faithfully prints `exit=1` while still exiting 0 itself (its documented contract).

## Findings (by severity)

### D1 — `defect`: the census block's `cmd:` cannot produce `census-lane`
`corpus/instruments/score-gap.py:183` prints a grep pattern that omits the parenthetical the parsed line carries (`score-gap.py:71-73` is the real reader). Evidence in §1b: the printed pattern yields 2 lines / no `134/1480`; the corrected pattern yields line 33. This breaks the instrument's central promise ("each with the command it came from", `score-gap.py:5-9`, `SKILL.md:1071`) for one of its five fields, on committed bytes, today. Fix = print `^- lane total \(SKILL\.md \+ corpus\): ` in the `cmd:` string (single-line change; the value needs no change).

### D2 — `defect` (latent): the advertised `recheck-mode=stub` fallback is broken; forcing it crashes
`STUB_RECHECK` (`score-gap.py:288-303`) does `json.load(...)` of `recheck.json` (line 297), but `_make_fixture` writes that file with `'%s: %d,\n' % (k, v)` (lines 408-409) — Python-ish text, not JSON:

```
$ python3 -c "import json;json.loads('lines: 2,\ntotal: 2,\n')" 2>&1 | tail -1
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

Forcing the branch (scratch copy whose `recheck-audit.py` prints nothing, so the §2 pre-flight fails and `mode` flips to `stub`):

```
$ cd / && python3 "$S/corpus/instruments/score-gap.py" --root "$S" --selftest 2>&1 | head -6
selftest recheck-mode=stub reason=corpus/instruments/recheck-audit.py --quiet printed no executes/gated/broken summary (exit 0)
selftest exit-a                       FAIL rc=2 want=0 err='score-gap: INPUT-UNREADABLE corpus/instruments/recheck-audit.py --quiet printed no executes/gated/broken summary (exit 1'
selftest no-write-a                   ok tree digest unchanged=True
selftest exit-b                       FAIL rc=2 want=0 …(same)
Traceback (most recent call last):
  …
  File "/tmp/scoregap-stub.vsoqRc/corpus/instruments/score-gap.py", line 485, in selftest
    ra, rb = _split_counts(a["recheck"]), _split_counts(b["recheck"])
KeyError: 'recheck'
SELFTEST_EXIT=1
```

Two independent faults compound: the fixture JSON is invalid, and `selftest()` indexes `a["recheck"]` without checking the report produced the field (line 485), so a red fixture surfaces as a raw traceback instead of a named `FAIL`. Neither is reachable today (`recheck-mode=real`), and the selftest has no arm that exercises stub mode — which is why wave 1 did not see it. Fix: `json.dump(spec["recheck"], …)` in `_make_fixture`, and make the field loops skip/declare a missing field instead of raising.

### W1 — `weak`: `anchorcheck.py` is an input with no digest, and the README says it prints one
The `source:` block digests four files (`score-gap.py:231`: `RECHECK_REL, SKILL_REL, CENSUS_REL, SCORECARD_REL`) but the `[2] anchors` numbers come from `corpus/instruments/anchorcheck.py`, which is never digested (`python3 … score-gap.py | grep -c 'sha256'` → `4`; `sha256sum corpus/instruments/anchorcheck.py` → `d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912`, absent from any report line). `corpus/instruments/README.md:347` states the reporter "Prints the sha256 of every input" — false for the one executable input most likely to drift. Same block: `field_anchorcheck` parses `anchors` and `pin_broken` (lines 156, 158) that no output line ever prints, and `field_recheck` parses `total` that is never printed — dead fields in a file whose value is auditability. Fix: add `ANCHOR_REL` to the digest loop; drop or print the unused parses.

### W2 — `weak` (cosmetic but provenance-relevant): printed `cmd:` ≠ invoked argv
`field_recheck`/`field_anchorcheck` run `[sys.executable, "-B", <abspath>, …]` (lines ~128-131, 155) but print `python3 <lane-relative path> …` (lines 137, 163). The `-B` difference is the flag that blocks bytecode writes, i.e. exactly the property the "read-only" claim rests on; it is inert today only because both instruments import stdlib exclusively (`recheck-audit.py:73-80`: argparse, glob, hashlib, json, os, re, subprocess, sys; `anchorcheck.py:112`: re, sys, os, subprocess, tempfile, shutil), so no `__pycache__` can appear. Low risk, one-line fix (print the `-B`), worth doing because a copied equivalence string should not silently drop the no-write flag.

### Residual risks (no fix demanded, but they bound the instrument's claim)

- **R1 — the `gap:` line covers one conjunct of the quoted threshold.** The quoted bar is "passing 25/25 source chains and 0 unsupported current claims" (§1a), but `gap_line` reports `gated of lines` (today 24 of 44 = fail-closed `recheck:` lines) and renders it as "0 gated unsupported claims". `gated` is `recheck-audit.py`'s own class (`recheck-audit.py:385`, printed definition at 447-450) and the docstring documents the computation (`score-gap.py:43-46`), so this is disclosed, not hidden — but the source-chain conjunct (25 chains) is not measured anywhere in the report, and "rechecks" ≠ "claims" ≠ "source chains". A reader comparing the gap line to `SCORECARD.md:331` gets a paraphrase, not the same predicate.
- **R2 — a `--root` copy reports a red `exit=`.** Because audited `recheck:` lines carry the absolute lane path, any copied-root run yields `strict pass=1/44 cdroot_fail=43`, `exit=1` (§6). Honest propagation, but the report has no "root ≠ the root the rechecks name" note, so a reader may read `exit=1` as a lane regression.
- **R3 — census figures are the r18 census of record, not live.** The block labels itself "(committed figures)" and quotes the definition verbatim, and `corpus/instruments/README.md:410` discloses "reads the committed r18 census of record"; but the report prints no revision or date of that census, so its staleness (registry is at 48 rows this round) is only discoverable by opening the census header (`# citation-survival census — kasegi lane`, "Instrument: … (r18 definition)").
- **R4 — one selftest arm is nearly vacuous.** `census-definition` moves between fixtures only by trailing wording, so it proves the value is read from the file but cannot distinguish a faithful read from a stale literal that happens to differ.
- **R5 — `threshold` parsing depends on one English sentence.** Disclosed at `README.md:412-414`; verified behaviour: removing it exits 2 rather than printing a stale line (`selftest exit2-no-threshold ok`), and two matches are flagged (`threshold-matches: 2 (first line used)`).

## Verification gaps

- No `lsp` device is mounted in this seat (only `ast_edit`/`debug`), so `references`/`definition`/`diagnostics` were unavailable; findings rest on the code text plus executed commands, not on server semantics. Recorded as unavailability, not as evidence of absence.
- I did not run the counter (`limb-mutation-check.py`) or the limb ledger — other seats own C1; nothing here is a judgement on those.
- I did not diff the reporter's numbers against a committed revision: `SCORECARD.md` is append-owned by `ScribeScorecard` during this wave, so the digests above are working-tree digests of quiescent files (tracked files were unmodified at review time; `git status --porcelain` showed only untracked `.ufo` paths).
- I did not test a lane missing `anchorcheck.py` at report time (only in the fixture path); by inspection `field_anchorcheck` raises `InputError` → exit 2, but I did not execute that arm.

## Cleanup

All scratch roots removed: `/tmp/scoregap-ro.RewUFO`, `/tmp/scoregap-stub.vsoqRc`, `/tmp/scoregap-full.Y2eKzM`, `/tmp/scoregap-ro2.yL5OoB`, `/tmp/scoregap-thr.*`, `/tmp/scoregap-ref`; `ls -d /tmp/scoregap-* /tmp/score-gap-selftest-*` → `leftover_count=0`. No lane mutation, no git/jj write, no pacman, no network fetch.
