# ConnCrossClaims — round-43 cross-claim ordering receipt

Seat: ConnCrossClaims (connector). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin (only repo written).
Read first: `.ufo/waves/round-43/claims.json` (sha256 a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630, = freeze.txt `claims-sha256`; never edited).
Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; lane head at spawn `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`; work window 2026-10-28T16:44Z–16:57Z.
Network: none (no curl). Tooling: none installed or upgraded. Scratch: `/fast/scratch/hyaku/kasegi-r43/ConnCrossClaims/` (4.1G of export trees), removed before yield.

Deliverable: `.ufo/waves/round-43/w1/ConnCrossClaims.txt` — 123 lines, sha256 `853b26513da1e0aa117084ab8bd81ba17c3fda906d3cbf1caa5a2ad6731156d8`.

## What was measured, with commands and real output

### 1. The r42 suite at base (the do-nothing stand-in), to establish the carried state
```
cd $S && bash <lane>/corpus/instruments/r42-closure.sh \
  --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc --work $S/w-base --scratch-root $S
```
J1 closed=1, J2 closed=1, J3 closed=1 (`tables=18,rows=73,r42-rows=1,r40-rows=1`), J4 closed=1
(`declared=469,valid=469,missing=0,escape=0,coverage=11/11,file=present`), J5/J6/J7 closed=1
(J7 `rows=25,admitted=25`), J8 closed=0 (`…ancestor=1,diff=0,…payload-match=12/12,forged=6/6`),
J9/J10/J11/J12/J13 closed=1 (`J11 payload=corrections=34,groups=4,dups=4,excused=4,unexcused=0…`),
`closed=12/13 exit=1`; wall 227.85 s.

### 2. Why base cannot be 13/19: the two carried checks that are red at base for round-43 paths
```
git -C <lane> cat-file -e ab98fac9:.ufo/waves/round-43/declared-blocks.txt
fatal: path '.ufo/waves/round-43/declared-blocks.txt' does not exist in 'ab98fac9…'   # exit 128
git -C <lane> cat-file -e ab98fac9:.ufo/waves/round-42/declared-blocks.txt ; echo $?   # 0
git -C <lane> cat-file -e ab98fac9:.ufo/waves/round-43/claims.json                     # exit 128
```
K4 semantics applied to the round-43 declaration path (r42 engine, `DECLARED_REL` retargeted, probe tree):
`declared=0,valid=0,missing=11,escape=0,coverage=0/11,file=absent` closed=0.
K8 at base: no round-43 receipt; `locate_receipt` falls back to `.ufo/waves/round-42/final-gates/all-gates.txt`
(a 13-check receipt, 33 lines), so `lines` (expects 45) and `closed-line` (expects (19,19,0)) fail; the base
r42 run above shows the same defect shape (`J8 … diff=0 … closed=0`). Derived base: 11/19 exit=1
(K4, K8, K14–K19 open). claims.json's `after` cell says 13/19 — measured contradiction 6.1 of the deliverable.

### 3. K4 declaration semantics (probe tree: `git archive HEAD` + landed deliverables)
```
absent                     -> declared=0,valid=0,missing=11,escape=0,coverage=0/11,file=absent   closed=0
declares an absent path    -> declared=14,valid=13,missing=0,escape=1,coverage=11/11,file=present closed=0
all declared paths present -> declared=24,valid=24,missing=0,escape=0,coverage=11/11,file=present closed=1
```

### 4. Landed-tree probe (all cited w1 deliverables applied at their landing paths)
`.ufo/waves/round-43/w1/` bytes used: ScribeCorrections.{scorecard,log,lesson42}.txt,
ScribeScorecardRound43.append.md, ScribeLogEntry.log-entry.md, ScribeShonenLines.append.md,
ScribeLessonDraft.round-43-lesson.md, ScribeClaimsErratum.claims-erratum-1.md,
ExecSourceCapture.{S067.txt,manifest.json}, ExecRegistryRows.rows.txt, ScribeKnowledgeGate.entry.md,
ExecCoverageMapNote.append.md, ExecGateCore.claim-package-check.py, ExecGateFixtures.defect-{1..9}-*,
ExecExemplarPackage.* (6 files), ExecGateSelftest.transcript.txt.
```
K1  records=1,blocks=3,graded=1,evidence=3,missing=0,wrong-grade=0,per-record=SCORECARD.md=3/3;LOG.md=0;SHONEN.md=0,union=0 closed=1
K3  tables=18,rows=73,r42-rows=1,r40-rows=1,r40-split=0,bare=0,lead=0 closed=1
K6  instrument=present,base=1,missing-path=1,url-mutated=1,digest-mutated=1,rule=reject closed=1
K7  instrument=present,base=1,status-flip=1,no-pass=1,rows=25,admitted=25 closed=1
K11 corrections=37,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
K12 deleted=0,density=1,density-sha=ee803726a322,diff-read=ok,base=5053a7f4 closed=1
K14 payload=literals=3,stale=0,superseded=2,live=corrections=37,groups=4 closed=1
   (stderr: superseded=SCORECARD.md:1634 corrections=33 live=37 ; superseded=SCORECARD.md:1662 corrections=33 live=37)
K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1   (with a round-42 erratum copy)
C2  capture-binding records=57 bound=57 unbound=0 ; frontier entries=28 pass=28 exit=0 ;
    census exit=0 with 68 SOURCES rows ; knowledge 62 ; 9 defect fixture dirs
```
Correction ledger arithmetic: 34 at base + 2 SCORECARD `Correction (round 43)` lines + 1 LOG line = 37.
The `corpus/lessons/round-42.md` correction line is not a RECORDS file and does not count.

### 5. K17 erratum placement (three states, same tree otherwise)
```
erratum absent (HEAD only)                    -> K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0
  detail: round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
erratum at .ufo/waves/round-43/claims-erratum-1.md (the spec path) -> identical payload, closed=0
same bytes copied to .ufo/waves/round-42/claims-erratum-5.md        -> superseded=1,unbacked=0 closed=1
```
Cause: `superseded_by(round_dir, token)` lists errata in `os.path.dirname(<claims.json>)` only
(ExecK17ClaimsBefore.sh:224-232). The spec's landing path alone cannot close K17.

### 6. K18 across the three states (quote sources = corpus/lessons/round-42*, round-43*, .ufo/waves/round-43/*.md;
evidence store = every non-record file under .ufo/waves/round-42/ and round-43/)
```
pre-receipt, as landed                                       -> quotes=51,bound=38,report-only=2,superseded=8,unbound=3 closed=0
  unbound: corpus/lessons/round-43.md:26 closed=19/19 (x2) and selftest cases=19 failures=0
same line marked `report-only`                               -> quotes=51,bound=38,report-only=7,superseded=6,unbound=0 closed=1
Y state (receipt with `closed=19/19 exit=0` + `selftest cases=19 failures=0`) -> bound=41,unbound=0 closed=1
```
Earlier state probes that establish two couplings:
```
erratum only in round-42, gate transcript absent -> quotes=43,bound=34,report-only=2,superseded=3,unbound=4
  unbound: round-42-verifier-spotcheck.md:65 `selftest cases=13 failures=3`; round-43.md:26 `closed=13/19`;
           round-43.md:27 and :140 `selftest cases=10 failures=0`
+ .ufo/waves/round-43/w1/ExecGateSelftest.transcript.txt -> unbound 2 (C2 transcript binds cases=10)
+ a wave-dir supersede line quoting closed=13/19 and cases=13 failures=3 -> unbound=0 closed=1
```
At 16:57:12Z that transcript (sha256 b4e8b2d4f70e57270ba4cbcef94a54db808462bfdbc91b68bbdf181d085363f9)
prints `selftest cases=10 failures=0` at line 60 but ends `selftest cases=10 failures=9` / `exit=1`:
K18 binds the token, not the verdict — a C1-green path that consumes a C2-red transcript.

### 7. C2 registry landing (census, read-only script)
```
lane current registry                        -> W04 x2, `ok`, census exit=0
rows appended at EOF of corpus/SOURCES.md    -> E12 S067 row outside Registry section
                                                E12 S068 row outside Registry section, exit=1
rows inserted after the last `| S` row       -> E11 S067 missing used-by corpus/knowledge/claim-package-gate.md, exit=1
same, with the entry file present            -> `ok`, exit=0, rows 66 -> 68
```
Lane baselines at 16:52Z: recheck-audit `expected=61 … exit=0`; frontier `entries=28 pass=28 exit=0`;
capture-binding `records=56 bound=56 unbound=0`.

### 8. Frozen-claim literals (K17 population check by hand)
```
C1 before tokens: closed=12/13 (printed by do-nothing), closed=10/12 (printed), closed=8/12 (printed), closed=10/13 (quoted from a record; limb counts it quoted=)
C1 after tokens : closed=19/19, selftest cases=19, failures=0, closed=13/19 — after cells are targets, not measurements (limb header)
C2 after tokens : selftest cases=10, failures=0 — C2's own counters, outside K17
```

## Findings that change the landing plan (deliverable sections 2, 4, 6)
1. Erratum must also exist under `.ufo/waves/round-42/` for K17 (measured closed=0 -> closed=1).
2. The base figure is 11/19, not 13/19; claims.json cannot be edited (K19 checks its sha256) — the report must quote the measured figure and the erratum supersedes the literal.
3. Any lane record quoting `closed=19/19` before Y must carry `report-only`, or the J run cannot print 19/19 (measured unbound=3 -> 0).
4. SOURCES rows must go inside `## Registry`; the knowledge entry must exist first (census E12/E11, both measured as exit=1).
5. `declared-blocks` must be generated last: a declared-but-absent path reds K4 as `escape`, not `missing`.
6. The claims text writes `SHENON.md`; the lane file and r42 RECORDS are `SHONEN.md`.

## State at yield (in-flight siblings, not judged here)
`ExecSuiteSkeleton.r43-closure.sh` and `ExecCarryChecks.declared-blocks.txt` were absent at 16:57:12Z, so
`corpus/instruments/r43-closure.sh` is undeclared/absent in every probe; the r43 suite must be final before the
receipt is generated (K8 suite-sha256). Scribe deliverables were read at the sha256 values cited above and may
have changed after the probe.

## Lane writes
`.ufo/waves/round-43/w1/ConnCrossClaims.txt` (deliverable) and this receipt. Nothing else in the lane, the fleet
root, shokuknow, or any PATH directory was written. No git/jj mutation was run anywhere; all git use was
read-only (`log`, `rev-parse`, `archive`, `cat-file`, `diff`, `ls-tree`).
