# ScribeShonen — SHONEN.md round-31 evidence update (round 31, wave 2)

Seat: `ScribeShonen` (UFO-FSD scribe). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`; wave-1 landing HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`). Single write target: `SHONEN.md`; this receipt is the
second write. Lane read-only everywhere else; fleet root and `/home/vgpnk/Projects/shokuknow` not
touched. No git/jj mutation (read-only `git status`, `git diff`, `git log`, `git rev-parse` only), no
delegation, no background job, no network fetch, no tool install/upgrade (nothing needed; pacman not
invoked). Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (harness route; no model
passed).

## 1. What changed

`SHONEN.md` keeps its header and its four-box shape (`grep -c '^\- \[' SHONEN.md` -> `4`); only the
`— evidence:` block under each box was replaced, round-25 text -> round-31 observable state. Every box
stays `[~]` (no box is ticked: no non-author verifier is on record).

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git status --porcelain -- SHONEN.md
 M SHONEN.md
$ git diff --numstat -- SHONEN.md
34	11	SHONEN.md
$ grep -n '^\- \[' SHONEN.md
5:- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
15:- [~] At least one end-to-end domain task executed and logged in LOG.md
24:- [~] Instructions executable by an agent without oral context
36:- [~] No cross-domain bleed (PROVINCE.md still accurate)
```

## 2. Poll for the wave-2 receipts (cap 45 min, not reached)

Seat start listing of `.ufo/waves/round-31/wave2/`: `ExecNoHarmDensity.md`, `ExecCensusFinal.md`,
`ExecCounterFix.md`, `ExecRegressionC1.md` all absent. Polled with
`until [ -s <file> ]; do sleep 15; done` in bounded batches; landed and read:

```
ExecCensusFinal.md    20870 B  21:34
ExecNoHarmDensity.md  21416 B  21:34
ExecCounterFix.md     15878 B  21:44
ExecRegressionC1.md   18481 B  21:47
```

All four are post-fix receipts on quiescent bytes; this seat did not re-run any instrument (no
PRE-STATE reading is cited, bound 6 / M30-3).

```
$ sha256sum SHONEN.md .ufo/waves/round-31/wave2/ExecNoHarmDensity.md \
    .ufo/waves/round-31/wave2/ExecCensusFinal.md \
    .ufo/waves/round-31/wave2/ExecCounterFix.md \
    .ufo/waves/round-31/wave2/ExecRegressionC1.md
2d4468a2dd3e91b3638bb1c40d02fb6b7fa66b82f634c6048810292490d01436  SHONEN.md
c7d7ddd2bcfa167f53736a5398de922ff84365722212b6f75e4719f9ec54416c  .ufo/waves/round-31/wave2/ExecNoHarmDensity.md
54fa97fb9a12a964ea1d28ff3723b551aa750f546279cb87311651eac5ca0ddb  .ufo/waves/round-31/wave2/ExecCensusFinal.md
77a29b65ea7302af53a490087710a7b5f622e0f63a49420703fa746bed37d455  .ufo/waves/round-31/wave2/ExecCounterFix.md
07238cc6d7d9e2a5c5ace7394dfb81d10252b740c27277804c2f386f62b64e3d  .ufo/waves/round-31/wave2/ExecRegressionC1.md
```

`SHONEN.md` sha256 above is post-edit; the pre-edit blob is `git show HEAD:SHONEN.md` (index
`f5a20cb`, see the diff in §4).

## 3. Evidence read per box (command -> observed output -> pointer written into SHONEN.md)

### Box 1 — SKILL.md content (`ExecNoHarmDensity.md`)

```
# receipt §0 and §1b/§2b
$ python3 corpus/instruments/density.py SKILL.md --label r31-final
# Density census — r31-final (1071 lines, 24 blocks)
| | mean dens | ... | 191.5 |
Total path-citation instances: 689 across 24 blocks.
density_exit=0
$ python3 corpus/instruments/anchorcheck.py SKILL.md; echo "anchor_exit=$?"
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 ...
anchor_exit=0
# r30 replay column, receipt §1a: mean dens 171.1, 23 blocks, 662 cites, 0 bad
```
Form-gaming audit, quoted from receipt §1d: block 24 resolves 11/27 = 40.74% under the instrument's
own conjunctive rule, "so this block would not qualify" — the receipt claims no quality gain, and the
SHONEN evidence line says so. `SKILL.md` sha256 `8176360…` was confirmed clean
(`git status --porcelain -- SKILL.md` empty; `git diff --numstat b374febb -- SKILL.md` = `14 0`,
the round-31 Gates & probes append).

### Box 2 — LOG.md (`LOG.md`, `ScribeLogR30.md`, C1/C2 receipts)

```
$ grep -n '^## ' LOG.md | tail -3
1469:## Round 30 — 2026-10-25 — instrument conformance ... (one v2 wave, 64 seats)
$ grep -n 'round-31\|Round 31' LOG.md | head -3
1471:**Late append, made in round 31.** Round 30 closed with no entry here ...
```
No round-31 `LOG.md` entry exists at HEAD. The round-30 entry is present and was appended in round 31
by seat `ScribeLogR30` (`.ufo/waves/round-31/wave1/ScribeLogR30.md`, cited in `LOG.md:1478`).
Round-31's own measured end-to-end commands are the C1 counter and the C2 census/harness:
`ExecRegressionC1.md` §2 prints `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`, `$?` `0`;
`ExecCensusFinal.md` §C-census prints `census_exit=0` and `entries=18 pass=18 exit=0`. The box
therefore stays `[~]` with those pointers, and the line states the missing round-31 LOG entry.

### Box 3 — executable instructions (`ExecRegressionC1.md`, `ExecCensusFinal.md`)

```
$ python3 corpus/instruments/recheck-audit.py --quiet; echo $?
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
0
$ cd / && python3 $L/corpus/instruments/recheck-audit.py --quiet --root $L   # same four lines, 0
$ python3 corpus/instruments/frontier-recheck-count.py; echo $?
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
S048:sha256 OK
S048:Q1 OK occurrences=1   ...   S048:Q8 OK occurrences=1
recheck_exit=0
```
Sources: `ExecRegressionC1.md` §3 and §4 (lane root and foreign cwd `/`), `ExecCensusFinal.md` §3
(S048 recheck) and its census block (`census_exit=0`, findings `W04 S028`, `W04 S029`). The 44 figure
is the committed `corpus/instruments/knowledge-expected.txt` count and the audit's own `lines=44
total=44`; the entry set itself was not retyped.

### Box 4 — PROVINCE accuracy / no bleed (`ConnSibling.md`, `PROVINCE.md`)

```
$ git diff --numstat b374febb -- PROVINCE.md
20	0	PROVINCE.md
# ConnSibling.md §1.5: "Zero overlap. No sibling lane holds ground on Microsoft MSRC/MSVR, ..."
# ConnSibling.md §1.4: grep -rin "vendor research" / "vulnerability coordination" -> NO MATCH (exit 1)
# ConnSibling.md §2.2: F15 inside province; kake-shokunin/corpus/README.md:457-460 disclaims intake
# ConnSibling.md §1 scan list: chousa, kengaku, kake, kagi, kumitate, kotoba (six sibling corpora)
```
The PROVINCE diff is the round-31 end-of-file amendment only (F12–F15 appended; no existing line
moved), consistent with the box text "PROVINCE.md still accurate".

## 4. `git diff` of SHONEN.md (verbatim)

```diff
diff --git i/SHONEN.md w/SHONEN.md
index f5a20cb..cefcfde 100644
--- i/SHONEN.md
+++ w/SHONEN.md
@@ -3,17 +3,40 @@
 Promotion to shokunin requires all of:
 
 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
-      — evidence: `corpus/instruments/density.py SKILL.md` mean 154.0, 652 path-citation
-      instances, 19 blocks; `anchorcheck.py SKILL.md` bad=0 (round-25 receipts in
-      `.ufo/waves/round-25/wave1/ScoutNoHarm.md`). `SKILL.md` bytes untouched by round 25.
+      — evidence (round 31, HEAD `eecad59`; `SKILL.md` sha256
+      `817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7`, clean in
+      `git status --porcelain -- SKILL.md`): `density.py SKILL.md` prints mean dens 191.5 over
+      24 blocks and 689 path-citation instances, `density_exit=0`; `anchorcheck.py SKILL.md` prints
+      `7 in-range cite instances, 0 bad`, `anchor_exit=0` — compared against an r30 replay (mean 171.1,
+      23 blocks, 662 cites, `0 bad`) in `.ufo/waves/round-31/wave2/ExecNoHarmDensity.md` §1b/§2b. The
+      mean move comes only from the round-31 appended block 24, whose resolvable share is 11/27 =
+      40.74%, so the receipt claims no quality gain for it (§1d).
+
 - [~] At least one end-to-end domain task executed and logged in LOG.md
-      — evidence: LOG.md round-25 entry; round report `.ufo/reports/round-25/kasegi.md`;
-      both claims land with measured before→after receipts.
+      — evidence (round 31): `LOG.md:1469` carries the round-30 entry, appended in round 31 by seat
+      `ScribeLogR30` (`.ufo/waves/round-31/wave1/ScribeLogR30.md`), and round-31's own end-to-end
+      commands land with receipts: the C1 counter prints `limbs=13 killed=13 survivors=0` and
+      `controls=3 rejected=3`, exit 0 (`.ufo/waves/round-31/wave2/ExecRegressionC1.md` §2), and C2's
+      census exits 0 with the harness at `entries=18 pass=18 exit=0`
+      (`.ufo/waves/round-31/wave2/ExecCensusFinal.md`). No round-31 `LOG.md` entry exists yet at HEAD
+      `eecad59`; the box stays `[~]`.
+
 - [~] Instructions executable by an agent without oral context
-      — evidence: every `corpus/knowledge/*.md` `recheck:` line is one cwd-independent command;
-      `recheck-audit.py` exits 0 with `executes=14 gated=23 broken=0` (`c1-receipt-index.txt`);
-      `frontier-recheck-count.py` entries=12 pass=12 exit=0.
+      — evidence (round 31, HEAD `eecad59` plus the wave-2 counter fix, `limb-mutation-check.py` sha256
+      `237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4`): every one of the 44
+      `corpus/knowledge/*.md` entries carries one `recheck:` command;
+      `recheck-audit.py --quiet` prints `strict pass=44/44` and
+      `expect=present expected=44 missing=0 unexpected=0`, exit 0 from the lane root and from `/` with `--root`
+      (`.ufo/waves/round-31/wave2/ExecRegressionC1.md` §3); `frontier-recheck-count.py` prints
+      `PASS F15 knowledge/vendor-third-party-finding-coordination.md ids=S048` and
+      `entries=18 pass=18 exit=0` (§4 and `.ufo/waves/round-31/wave2/ExecCensusFinal.md`); and
+      `source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048`
+      exits 0 with 8 assertion `OK` lines (ExecCensusFinal.md §3).
+
 - [~] No cross-domain bleed (PROVINCE.md still accurate)
-      — evidence: PROVINCE.md frontier F01–F10; connector seat found no sibling lane holds the
-      F10 ground (chousa cedes bounty-program scope; kake refuses disclosure timing), adjacency
-      reported, nothing absorbed.
+      — evidence (round 31): `PROVINCE.md` gained only an end-of-file amendment (`git diff --numstat
+      b374febb -- PROVINCE.md` = `20	0`), naming F12–F15 and keeping the older F01–F10 paragraph as
+      history; the sibling sweep in `.ufo/waves/round-31/wave1/ConnSibling.md` §1.5/§2.2 found zero
+      MSVR and zero "vendor research" hits across the six sibling corpora, placed F15 inside this
+      province, and recorded `kake-shokunin/corpus/README.md:457-460` as an explicit refusal of
+      vulnerability intake; adjacency reported, nothing absorbed.
```

## 5. Findings and limits

1. **No box ticked and no new verdict claim.** All four boxes remain `[~]`; the file asserts no score move.
   Box 2 is the weakest: the round-31 end-to-end task is measured in receipts but its own `LOG.md`
   entry does not exist yet at HEAD `eecad59`, and the evidence line says exactly that.
2. **Density mean move is not a quality claim.** The 171.1 -> 191.5 move is the appended block 24,
   and that block's own resolvable share is 11/27 = 40.74% (receipt §1d, "volume/rule effect of the
   path-like definition"). The SHONEN line carries the caveat rather than quoting the mean as progress.
3. **Counter output now has 4 extra `guard ` lines** on every `--ledger` run (`ExecRegressionC1.md`
   §2: `guard cases=3 failures=0`, one line per guard fixture). The frozen contract's exact summary
   lines, the 13 `LIMB ` lines and `controls=3 rejected=3` are unchanged or exceeded, so no contract
   violation is observed here; the grammar delta is recorded for the canonical judge, not fixed by
   this seat.
4. **Wave-2 counter bytes are uncommitted** at receipt time: `git status --porcelain --
   corpus/instruments/limb-mutation-check.py` -> ` M` (sha256 `237fd07c…`); the L1 commits through the
   lane helper. `SHONEN.md` cites that digest, so its box 3 pointer names measured bytes, not HEAD.
5. **Out of scope / not done:** no instrument re-run (all values are read from the four receipts named
   in §2), no edit to `LOG.md`, `SKILL.md`, `PROVINCE.md`, the ledger or the counter, no scratch lane
   created (nothing was executed), no receipt other than this one and `SHONEN.md`.

Report: .ufo/waves/round-31/wave2/ScribeShonen.md
