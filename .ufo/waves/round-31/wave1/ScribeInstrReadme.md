# ScribeInstrReadme — round 31, wave 1

Seat `ScribeInstrReadme` (scribe, leaf — no dispatch, no background work of my own).
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base
`b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`.
Answering model: `devin/deepseek-v4-1-flash` (runtime route table; no model passed by me).
Owned path written: `corpus/instruments/README.md` (append-only) + this receipt. Nothing else.
Tooling: none installed or upgraded; no pacman transaction; no network fetch.
Git: read-only only (`git diff`, `git status`). No git/jj mutation.

## 1. Deliverable

Appended one section at file end; no line above moved (R6):

```
$ wc -l corpus/instruments/README.md
493 corpus/instruments/README.md
$ sed -n '329,330p' corpus/instruments/README.md
## Round-31 additions — one-limb mutation ledger + score-gap reporter

$ git diff --numstat corpus/instruments/README.md
166	0	corpus/instruments/README.md
```

Section map (lines 329–493): the 4-row table (`limb-mutation-check.py`,
`limb-ledger.json`, `limb-fixtures/`, `score-gap.py` — what each measures + run command),
the counter's measured output block, "Known limits (measured, not assumed)", the
"R13 / R11 relation" paragraph, the before/after digest table, and a "Re-verify" command
block with targets.

Facts per row came from these receipts, read not rerun: `ExecLedgerMerge.md` (counter
pair runs, ledger shape, controls), `ExecScoreGap.md` (§2 contract map, §6 FINAL block,
§8 limits), `ExecRALimbs.md` (§4 per-limb verdicts, §5 the RA-completeness survivor and
its fix, §7 risks), `ExecSRLimbs.md` (§5 mutant cross-runs, §8 `quote-absent`
strengthening, §11 M30-1), `ExecFRLimbs.md` (§C2 cross-mutant matrix, §F resolve delta
0), `ExecCounter.md` (§3 selftest cases, §7 hardening), `MutRAExisting.md`,
`MutSRExisting.md` (M5 survivor), `MutFRExisting.md` (two un-killed FR mutants),
`CritC1Kill.md` (§2.1 attack disposition: A7/A11/A12/A6 open). Every number that appears
in the section is either quoted from one of those receipts with the receipt named in the
text, or measured by me in §3–§6 below.

## 2. Quiescence gate (bounds 6, 9)

My item named two receipts to wait for. Poll interval 20 s, `[ -s <file> ]`:

```
READY both final at 520s            # ExecLedgerMerge.md present AND ExecScoreGap.md has no PENDING/FINAL_BODY placeholder
```

`ExecLedgerMerge.md` (23,304 B, 20:49) and `ExecScoreGap.md` (15,383 B, 20:47, §6 FINAL
run present) both landed. The C1 subject bytes were **still moving** after that, so a
second gate ran on the counter itself:

```
QUIESCENT counter=c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f stable_checks=13 at 840s
-rw-r--r-- 1 vgpnk vgpnk 19098 21:04:53 .ufo/waves/round-31/wave1/ExecCounter.md
```

Counter digest drift observed while waiting (M30-2/M30-3 discipline): `cde7c2b6…` in
`ExecLedgerMerge.md` §1–§2 → `bd18c244…` in a later merge message → `c660a95f…` landed.
**Only `c660a95f…` is cited in the README**; the earlier figures are named as superseded
in the R11 paragraph. No PRE-STATE number of mine is compared to an after column.

## 3. Measured — the counter (quiescent bytes)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0

$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json 2>/dev/null | sha256sum
9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838  -
run2_exit=0

$ python3 corpus/instruments/limb-mutation-check.py --selftest 2>&1 | tail -4
selftest aggregate-green       ok
selftest aggregate-survivor    ok
selftest control-verdict-rule  ok
selftest cases=20 failures=0
```

Both runs exit 0; the stdout digest is byte-identical across them and equal to the
figure `ExecLedgerMerge.md` published, reproduced independently here. 13 `LIMB ` lines,
each `live` != `mutant` in exit or signal.

## 4. Measured — digests after the C1 edits (bounds: sha256sum on quiescent bytes)

```
$ sha256sum corpus/instruments/limb-ledger.json corpus/instruments/limb-mutation-check.py corpus/instruments/recheck-audit.py corpus/instruments/source-recheck.py corpus/instruments/frontier-recheck-count.py corpus/instruments/score-gap.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb  corpus/instruments/score-gap.py
```

Same six digests printed again after the counter pair and the selftest — identical
(quiescent: true). Base bytes for comparison, taken from
`.ufo/waves/round-31/c1-controls/base-instrument-digests.txt` / `claims.json` and matched
by my own read at seat start, before any executor edit landed: `3fc0d751…`
(recheck-audit), `33602a9d…` (source-recheck), `aa60b581…` (frontier — unchanged). Those
three are **PRE-STATE** figures; they appear in the README only in the "before round 31"
column and are never compared to an after column.

## 5. Measured — the score-gap reporter

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py; echo "sg_exit=$?"
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
sg_exit=0

$ cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py --selftest; echo "sg_selftest_exit=$?"
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
sg_selftest_exit=0
```

The README quotes fields 1, 2, 4 and 5 and the reporter's own run command; the full
block above (with the per-input sha256) is the audit trail. `ExecScoreGap.md` §5 is a
PRE-STATE block and is **not** used anywhere in the append.

## 6. No-write and no-harm evidence

```
$ git status --porcelain corpus/instruments > /tmp/sir-status-before.txt   # before the counter pair
$ git status --porcelain corpus/instruments > /tmp/sir-status-after.txt    # after pair + selftest
$ diff /tmp/sir-status-before.txt /tmp/sir-status-after.txt && echo "STATUS-UNCHANGED"
STATUS-UNCHANGED
$ cat /tmp/sir-status-after.txt
 M corpus/instruments/knowledge-expected.txt
 M corpus/instruments/recheck-audit.py
 M corpus/instruments/source-recheck.py
?? corpus/instruments/limb-fixtures/
?? corpus/instruments/limb-ledger.json
?? corpus/instruments/limb-mutation-check.py
?? corpus/instruments/score-gap.py
$ ls corpus/instruments/__pycache__ | grep -cE 'limb|score-gap'
0
```

The counter and the reporter added no lane file and no bytecode cache; every `M`/`??`
above belongs to another seat (`knowledge-expected.txt` = ExecExpectedList,
`recheck-audit.py` = ExecRALimbs, `source-recheck.py` = ExecSRLimbs, fixtures/ledger/
counter = ExecCounter/ExecSRLimbs/ExecFRLimbs/ExecLedgerMerge, `score-gap.py` =
ExecScoreGap). The only file I wrote is `corpus/instruments/README.md`.

Anchor gate on the appended file (read-only run; the three `BASE-ABSENT` cites are the
pre-existing ones the round-28 section already discloses at lines 114, 116, 164 — my
append starts at line 329 and adds none):

```
$ python3 corpus/instruments/anchorcheck.py corpus/instruments/README.md 2>&1 | grep -E '^== |BASE-ABSENT'
== corpus/instruments/README.md: 1 in-range cite instances, 0 bad; 1 distinct anchors; LOST-RECORDED=2 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=3
BASE-ABSENT md:114 ~/Projects/the-bounty-hunter/ops/rank.mjs:1 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs)
BASE-ABSENT md:116 ops/rank.mjs:1 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/ops/rank.mjs)
BASE-ABSENT md:164 ResolverAttack.md:151 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/ResolverAttack.md)
```

The one in-range cite instance my append adds is `SCORECARD.md:331`; verified as the
threshold line itself (single `Threshold for 5:` occurrence in the file):

```
$ grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md | cut -c1-200
331:| depth:verifiability (C1, lowest axis) | 4 | **4** | **Improved, score held.** Legacy knowledge entries carrying `source:`/`verified-at:`/`recheck:` (appended end-of-file `## Provenance` block, s
$ grep -cE 'Threshold for 5:' SCORECARD.md
1
```

Every other backticked path in the append was checked to exist (19 paths, all `OK`) —
no `GONE` citation was added to a file `resolve.py` collects from.

## 7. Limits of this seat's evidence

- The README records **working-tree** digests. The round's integration commit is not
  available to this seat, so the digest table is not a commit-pinned claim; the L1's
  commit + post-commit recheck is what would pin it.
- The README quotes the counter and reporter output as measured here at
  `c660a95f…` / `855869bf…`. `ExecLedgerMerge.md`'s counter figures were measured at
  `cde7c2b6…` and are named as superseded in the append, not merged into mine.
- The score-gap block prints the sha256 of `SKILL.md` and `SCORECARD.md`; both are
  append-only surfaces other seats still own this wave. If either changes, the reporter
  prints the new digest on the next run — the README says so rather than pretending the
  quoted block is permanent. `SCORECARD.md:331` is stable under an end-of-file append.
- I did **not** rerun the three subject instruments' selftests, the frontier harness, or
  the C1 no-harm counters; those are the executors' evidence
  (`ExecRALimbs.md` §6, `ExecSRLimbs.md` §8–§9, `ExecFRLimbs.md` §E, `ExecLedgerMerge.md`
  §5) and the C1 claim's closure commands. The README's known-limits text therefore
  quotes their receipts for anything I did not measure myself, and names the receipt.
- No claim about C1/C2 scores, and no score move, is made in the append or here.

## 8. Out of scope / untouched

`claims.json`, `corpus/lessons/`, `SHONEN.md`, the round report, `LOG.md`, `SCORECARD.md`,
`QUALITY.md`, `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`knowledge-expected.txt`, `considerthese-proposals-ledger.md`, the three subject
instruments, the ledger, the counter, the fixtures, `score-gap.py`, and everything under
`/home/vgpnk/Projects/shokuknow` (read-only, no campaign tool run) — all untouched by
this seat.

## 9. Checks the main agent should run (quiescent tree)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git diff --numstat corpus/instruments/README.md                      # expect 166 0 (additions only)
sha256sum corpus/instruments/{recheck-audit,source-recheck,frontier-recheck-count,limb-mutation-check,score-gap}.py corpus/instruments/limb-ledger.json
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"   # 13/13, controls 3/3, exit 0
python3 corpus/instruments/limb-mutation-check.py --selftest; echo "exit=$?"                                            # cases=20 failures=0
python3 corpus/instruments/score-gap.py; echo "exit=$?"                                                                  # exit 0, gap line present
python3 corpus/instruments/anchorcheck.py corpus/instruments/README.md | grep '^== '                                     # 1 in-range, 0 bad, BASE-ABSENT=3 (pre-existing)
```
