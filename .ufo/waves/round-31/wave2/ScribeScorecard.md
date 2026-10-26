# ScribeScorecard — round 31 wave 2 receipt (SCORECARD append)

Seat: `ScribeScorecard` (scribe, leaf). Round kasegi-shokunin 31, wave 2 (falsify wave; wave 1
quiescent). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base
`b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`;
lane HEAD at every measurement `eecad59db166e0626ca2472e96ea48bc28a35153`.

- Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (harness project context /
  config route table; no model passed by this seat anywhere).
- Tooling installed or upgraded: **none** (no pacman transaction — host pause respected; no
  uv/npx/binary download; `sha256sum`, `wc`, `grep`, `sed`, `git` read-only, `python3` stdlib only).
- Writes by this seat: `SCORECARD.md` (one append) and this receipt. Nothing else in the lane; no
  scratch trees needed; no git/jj mutation (read-only `git rev-parse`, `git status`, `git diff`,
  `git log`); no delegation, no subagent, no background job of my own (the shell tool
  auto-backgrounded three of my poll loops — disclosed in §2, not described as foreground runs);
  no network fetch; no credential material.

## 1. Frozen claims read (verbatim source of every target)

```sh
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -c "import json;d=json.load(open('.ufo/waves/round-31/claims.json'));print(len(d['claims']),[c['id'],c['axis'],c['score_before'],c['score_after']] for c in d['claims'])"
```
(read in full; C1 depth:verifiability 4 → "held 4", C2 coverage 7 → "held 7".)

Before columns, quoted from the frozen controls:

```sh
$ cat .ufo/waves/round-31/c1-controls/before.txt   # counter absent
ls_exit=2 / counter_exit=2; selftest cases=9 failures=0 (source-recheck); ra_selftest_exit=0;
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0 … ra_exit=0
$ cat .ufo/waves/round-31/c2-controls/before.txt
frontier_admitted=14 / entries_citing_S048=0 / rows_S048=0 / registry_rows=47 /
census_exit=0 / entries=17 pass=17 exit=0 / manifest UNAVAILABLE reason=missing / recheck_exit=2
```

## 2. Poll log (item gate: `ExecRegressionC1.md`, `ExecCensusFinal.md`, ≥10 wave-2 receipts)

| time (UTC) | observation |
|---|---|
| 00:16–00:31 | 22–23 wave-2 receipts present at first listings; `ExecRegressionC1.md`, `ExecCensusFinal.md`, `ExecNoHarmDensity.md`, `ExecCounterFix.md` absent |
| 00:31:28Z | `ExecCensusFinal.md` present (quiescence proof inside: ten surfaces digested twice, 107 s apart, identical) |
| 00:35:58Z | `ExecNoHarmDensity.md`, `MutCtrTimeoutKilled.md`, `RevScoreGap.md` present; counter digest had moved `c660a95f…` → `76039cf9…` (owner `ExecCounterFix` still editing → not measured) |
| 00:39–00:42Z | counter stable at `237fd07c…`; `ExecCounterFix.md` absent |
| 00:42:59Z | `ExecCounterFix.md` present (15878 B; counter `237fd07c…`, ledger unchanged) |
| 00:47:04Z | `ExecRegressionC1.md` still absent; peer `ExecRegressionC1` sent its measured numbers over IRC at this point |
| 00:47:32Z | `ExecRegressionC1.md` present (18405 B); values verified against the receipt before any citation, and re-verified at receipt close after the seat's final edit — every cited line unchanged (`grep` §3) |

Disclosure: three poll loops (`timeout 230/210/180 bash -c 'until [ -s … ]; do sleep …; done'`) were
auto-backgrounded by the shell tool (`bg_20741`, `bg_21214`, `bg_21610`) instead of staying in the
foreground; one further 115 s loop was "backgrounded early to handle an incoming message". No
busy-loop was spun by hand; each loop capped well under the 30-minute/45-minute item caps.
`BLOCKED:` lines: none — every gated file appeared inside the cap.

## 3. Numbers cited in the append, and where each comes from

```sh
$ cd .ufo/waves/round-31/wave2 && sed -n '60,110p' ExecRegressionC1.md
guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
guard cases=3 failures=0
LIMB RA-parse live=0/y mutant=1/n verdict=killed
… (13 LIMB lines, every row live ≠ mutant) …
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
$ echo $? → 0 ; grep -c '^LIMB ' → 13 ; grep -c '^CONTROL ' → 3
$ cmp counter1.out counter2.out → IDENTICAL ; sha256 d6aefddca50293347c348646479bbe406745ad3163422b27edefcea861264270 (both)
$ --selftest → selftest cases=20 failures=0 (exit 0, lane root and /)
$ recheck-audit --quiet → strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0 ;
    expect=present expected=44 missing=0 unexpected=0 exit=0
$ source-recheck --selftest → cases=10 failures=0 ; anchorcheck --selftest → cases=12 failures=0,
    limbs=9 covered=9 ; frontier-recheck-count → entries=18 pass=18 exit=0 incl. PASS F15 … ids=S048
$ 38 registered source ids / 8 manifests → 38/38 exit 0 (both cwds)
```

```sh
$ cd .ufo/waves/round-31/wave2 && sed -n '30,60p' ExecCensusFinal.md
15 / 1 / 1 / 48 ; census_exit=0 with W04 S028, W04 S029, ok ; entries=18 pass=18 exit=0 ;
recheck_exit=0 with S048:sha256 OK + Q1..Q8 OK occurrences=1
```

```sh
$ cd .ufo/waves/round-31/wave2 && grep -nE "mean dens|Total path-citation" ExecNoHarmDensity.md
45:| | **mean dens** | … **171.1** |       84:| | **mean dens** | … **191.5** |
47:Total path-citation instances: 662 across 23 blocks.
86:Total path-citation instances: 689 across 24 blocks.
```

Counter-mutant receipts (per-seat verdicts, quoted in the append): `MutCtrNonUniqueFind.md`
§Verdict SURVIVOR (`9b386485…`, exit 0), `MutCtrNoLiveBaseline.md` §Verdict SURVIVOR
(byte-identical, 9.8 s vs 20.8 s), `MutCtrTimeoutKilled.md` §Verdict SURVIVOR,
`MutCtrAlwaysKilled.md` (`controls=3 rejected=2`), `MutCtrNoCompileCheck.md` (`rejected=2`),
`MutCtrSignalIgnored.md` (`limbs=13 killed=12 survivors=1`). Repair: `ExecCounterFix.md` §1, §3,
§4, §5 (three implicit guard fixtures on every `--ledger` run; no limb, no control added; ledger
byte-identical; all six mutants exit 1 on `237fd07c…`).

Limb re-derivations: `ExecLimb*.md` §Verdict — 10 `holds`, 3 `weak` (`RA-cdroot`, `RA-paths`,
`FR-missing-entry`); no row is a survivor; each receipt reproduces the counter's line by hand.

## 4. The append (single write) and additions-only proof

Appended `## Round 31 — frozen claims C1/C2 (2026-10-25)` … `### Round-31 move-log rows` after the
existing round-30 erratum paragraph, plus `## Round-31 capabilities`, with `edit` (content-addressed,
old_string = the erratum's last sentence, which is left byte-identical).

```sh
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && echo "deleted_lines=$(git diff -U0 SCORECARD.md | grep -c '^-[^-]')"
deleted_lines=0
$ git diff --numstat SCORECARD.md
87	0	SCORECARD.md
$ git diff -U0 SCORECARD.md | grep -E '^@@' | head -1
@@ -860,0 +861,87 @@ …
$ wc -l < SCORECARD.md
947
$ sha256sum SCORECARD.md
4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da  SCORECARD.md
```

87 added lines, 0 deleted, one hunk at the end of the file: the wave-1 erratum text, the round-30
section and every earlier line are untouched.

## 5. Judgement recorded in the append (and its evidence)

- **C1 = verified, score held 4**, on the repaired final revision (`237fd07c…` / `c042adf6…`):
  frozen kill-rule clauses all met by `ExecRegressionC1.md`; 13 hand re-derivations agree.
  Disclosed, not counted as a clause met: `claims.json` C1 `mutants_of_the_counter` was falsified at
  the wave-1 landing (2 of 4 frozen mutants survived byte-identically) and repaired post-freeze by
  `ExecCounterFix` — the round-25 "post-freeze counter repair" form.
- **C2 = NOT VERIFIED, honest stop, no credit claimed (score stays 7).** All seven frozen counter
  cells met on quiescent bytes (`ExecCensusFinal.md`), but the kill-rule clause "the entry fails any
  QUALITY.md Q1-Q10 under the non-author reviewer" trips: `RevEntryQ.md` §5 files `REFUSE — on Q3
  only` against `corpus/knowledge/vendor-third-party-finding-coordination.md:84-87`, refuted by
  `vendor-disclosure-policy-commitments-crosswalk.md:49`, `:66`. Nothing in the received receipts
  rebuts that finding on its own terms.
- **Conflict reported verbatim, ruling left to the canonical judge** (append §"C2 reviewer
  conflict"): `RevEntryQ` `REFUSE` vs `RevQuoteRoles` `0 HIGH, 2 MEDIUM, 12 LOW` /
  `none is a claim without a locatable quote` vs `CritExpansion` `partial` /
  `C2 is not failed by this review` vs `RevRowS048` `all six rules CONFORMANT at row level` vs
  `RevQuoteRoutes` `all 8 manifest assertions AGREE`. Divergence from the round's own lesson noted
  in place: `corpus/lessons/round-31.md:14` reads these as `Non-author reviews agree on admission`,
  which does not carry the filed Q3 REFUSE.
- **depth:density = unchanged (held 9), no harm**, numbers from `ExecNoHarmDensity.md` (171.1 → 191.5,
  23 → 24 blocks, 662 → 689 cites, anchor classes unmoved), with the seat's own mechanism
  disclosure (`11/27 = 40.74%` resolve fraction, fails the ≥60% conjunctive bar) recorded rather
  than the bare mean.
- **Capabilities: one row** (`limb-mutation-ledger`, first-working round 31) because
  `ExecRegressionC1.md` shows the counter running with the exit-0 output. Appended as
  `## Round-31 capabilities` (the round-24/25/26 pattern) because this seat is append-only; the
  master `## Capabilities` table is untouched, and the append says so.

## 6. Out-of-scope observations (routed, not fixed, not claimed)

1. `RevScoreGap.md` returns `defect` on `corpus/instruments/score-gap.py` (census `cmd:` line cannot
   produce the `census-lane` value it sits above; `--selftest` `recheck-mode=stub` fallback crashes
   with `KeyError: 'recheck'`). Non-claim frontier item; no SCORECARD change made.
2. `RevGateSpot.md` re-derived the four Gate items (`AGREE` on (a)–(c), `AGREE on the digits,
   DISAGREE on the word "guard proof"` on (d)) — recorded here because its item-a evidence bears on
   the S048 row my C2 cell cites.
3. `ExecNoHarmDensity.md` §6 route 1: the committed citation-survival census is round-20 stale
   (9.05% quoted in round-31 SKILL block vs 17.15% measured on final bytes). Not my file; not fixed.
4. The shell tool auto-backgrounded poll loops for several seats this wave (`ScribeLesson`,
   `RevGateSpot`, this seat); every such receipt discloses it rather than presenting it as a
   foreground run.

## 7. State of the lane at receipt time

```sh
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ git status --porcelain -- corpus SKILL.md SCORECARD.md
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/instruments/limb-mutation-check.py
?? corpus/lessons/round-31.md
$ sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json SCORECARD.md SKILL.md corpus/knowledge/vendor-third-party-finding-coordination.md
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da  SCORECARD.md
817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7  SKILL.md
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
```
`corpus/QUALITY.md` is `ScribeQualityFix`'s write, `corpus/lessons/round-31.md` is
`ScribeLesson`'s, the counter is `ExecCounterFix`'s; none was touched by this seat. The L1 commits
through the lane helper.

Report: .ufo/waves/round-31/wave2/ScribeScorecard.md
