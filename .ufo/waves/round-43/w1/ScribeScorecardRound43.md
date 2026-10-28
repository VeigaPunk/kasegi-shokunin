# ScribeScorecardRound43 — receipt

Seat: `ScribeScorecardRound43` (scribe, leaf). Round 43, wave 1 (`kasegi-r43-hyaku`, 73 seats).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Claims-freeze head at the time of work: `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`.
Frozen claims read first: `.ufo/waves/round-43/claims.json` (sha256 `a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`, per `.ufo/waves/round-43/freeze.txt`). Never edited.

## Deliverable

| Artifact | Lines | sha256 |
|---|---:|---|
| `.ufo/waves/round-43/w1/ScribeScorecardRound43.append.md` | 27 | `07fa41948d1d7bb81b716612ca7c6209872dc25bd63fd15fb378fe9a9792b9b8` |

The block is byte-exact, append-only, and starts with `## Round 43 result`. It carries, in order:
(a) the `## Round 43 result` table — three rows: `depth:verifiability`, `coverage`, `depth:density` (non-target guard);
the frozen-control "Measured before" paragraph; (c) `## Round-43 capabilities` with the single
`claim-package-gate` row whose evidence pointer is `<pending: demo>`; the saturation line;
(b) `### Round-43 move-log rows` — three rows (`43 | depth:verifiability`, `43 | coverage`,
`43 | depth:density`); (d) one `Correction (round 43)` line at EOF.

Append mechanics: `SCORECARD.md` ends with `\n\n` (verified: `tail -c 120 SCORECARD.md | od -c` ends
`... G a t e b l o c k | \n \n`), so the block appends without an added leading blank line and without
touching any existing byte.

## Verdict wording rule applied

No row says the round is verified. The after cells read `4 (held; not verified by this append — the
round-43 kill rule is not re-derived here)` and `8 (held; no score increase claimed)`; every after-state
figure in the evidence column is labelled the frozen predicate's, and the move-log after cells say
`**expected** (...) — **the Y measurement is the receipt's, not this append's**`. The capability row is
`<pending: demo>` and states that the L1 confirms the demo from the seat receipts.

## Commands run (verbatim, with real output)

### 1. Claims and controls

```
$ python3 -c "import json; d=json.load(open('.ufo/waves/round-43/claims.json')); ..."
claims: C1 depth:verifiability (score_before 4, "held 4"); C2 coverage (score_before 8, "held 8 (capability row enters)")
axes_owned: depth:density, depth:verifiability, coverage
base=ab98fac9dce87130bc4f66de89e30650d63943dc  frozen_at_utc=2026-10-28T16:37:07Z
```

```
$ cat .ufo/waves/round-43/freeze.txt
frozen-at=2026-10-28T16:37:07Z
measured-at-max=2026-10-28T16:34:15Z
claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
base=ab98fac9dce87130bc4f66de89e30650d63943dc
```

```
$ cat .ufo/waves/round-43/c1-controls/do-nothing.txt
--- A. r43 suite absent at base
ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory
--- B. r42 suite (the do-nothing stand-in) run over the base export
export-ref=ab98fac9dce87130bc4f66de89e30650d63943dc
...
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,...,run-lines=1,selftest-lines=1,...,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=0
J11 payload=corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
closed=12/13 exit=1
--- C. the six routed r42 defects present at base (the r42 suite cannot see them)
RD42-1 corrections=33 literal at SCORECARD.md:1634:   corrections=33
RD42-2 LOG.md wave-2-dispatched sentence:             (absent evidence file)
RD42-3 lesson sentence:                                wave 2 dispatched 36 seats; the round total is 100
RD42-4 placeholder:                                    ## Wave-2 falsification
RD42-5 quoted value vs committed transcript:           all-gates.pre-repair.txt / all-gates.txt / verify-Y0.txt
RD42-8 claims.json before literal vs control:          closed=8/12 exit=1
RD42-6 freeze label:                                   2026-10-28T12:05:00Z / 2026-10-28T08:00:01-03:00
```

```
$ cat .ufo/waves/round-43/c2-controls/before.txt
--- A. claim-package gate absent at base
ls: cannot access 'corpus/instruments/claim-package-check.py': No such file or directory
ls: cannot access 'corpus/instruments/fixtures/claim-package': No such file or directory
instrument-basenames-matching-claim: 0
--- B. registry rows
66
S067 onwards: 0
--- C. knowledge files
61
entries citing S067: 0
--- D. capture binding
records=56 bound=56 unbound=0   (AUDIT ... orphan=S040-live.txt)
--- E. recheck audit
expect=present expected=61 missing=0 unexpected=0 exit=0
--- F. frontier harness
entries=28 pass=28 exit=0
--- G. census
kasegi	W04	S028 duplicate url ...; kasegi	W04	S029 duplicate url ...; kasegi	ok	.../corpus/SOURCES.md
census-exit=0
```

```
$ cat .ufo/waves/round-43/census-before.txt
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census exit=0
```

### 2. Correction-ledger state (the K14 / Rd42-1 inputs)

```
$ for f in SCORECARD.md LOG.md SHONEN.md; do grep -c '^Correction (round ' $f; done
SCORECARD.md corr-lines=19
LOG.md corr-lines=7
SHONEN.md corr-lines=8
```

```
$ grep -n 'corrections=[0-9]' SCORECARD.md LOG.md SHONEN.md
SCORECARD.md:1634:Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33,groups=4,dups=4,...
```

```
$ sed -n '1600,1612p' SCORECARD.md   # duplicate pair confirmed
1602 Correction (round 41): round-40 C1 is not verified on the frozen counter ...
1603 Correction (round 41): the `## Round 40 result` depth:verifiability row's "4 (held; verifi ...
1604 Correction (round 41): the row's `graded --selftest cases=10 failures=0` carries no committ ...
1605 Correction (round 41): the round-41 receipt at its Y tees the transcripts of BOTH the suit ...
1607 Correction (round 41): round-40 C1 is not verified on the frozen counter ...
1608 Correction (round 41): the `## Round 40 result` depth:verifiability row's "4 (held; verifi ...
1609 Correction (round 41): the row's `graded --selftest cases=10 failures=0` carries no committ ...
1610 Correction (round 41): the round-41 receipt at its Y tees the transcripts of BOTH the suit ...
```

`SCORECARD.md:1634` carries `corrections=33`; the same export's K11 (J11) line prints `corrections=34`
(c1-controls above) — this is RD42-1 exactly as the verifier spot-check routed it
(`corpus/lessons/round-42-verifier-spotcheck.md:173`: required action "appended `Correction (round 43)`
naming the superseded cell; do not rewrite 1634").

Ledger semantics I reused by reading (not forking) `corpus/instruments/r42-closure.sh:1078-1130`
(`check_j11`): `total` counts every `Correction (round <n>)` line in the three records; duplicates are
grouped by normalized body; `unexcused == 0` is required for green. Consequence for the block: a new
`Correction (round 43)` line raises `total`, and a body duplicated verbatim would open a new unexcused
group — the block therefore carries exactly one correction line with unique wording.

### 3. Non-target guard (density)

```
$ git cat-file blob ab98fac9dce87130bc4f66de89e30650d63943dc:corpus/instruments/density.py | sha256sum
ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  -
$ git show ab98fac9:corpus/instruments/density.py | wc -l
208
```

This sha256 is the value written into the two `depth:density` cells; it is the guard target that K12
must hold at J and Y. It was re-derived by me at base, read-only.

### 4. Append mechanics

```
$ tail -c 120 SCORECARD.md | od -c | tail -3
0000140   -   4   2   -   *   .   m   d   `       G   a   t   e       b
0000160   l   o   c   k       |  \n  \n
```

### 5. Deliverable audit

```
$ wc -l ScribeScorecardRound43.append.md      -> 27
$ sha256sum ScribeScorecardRound43.append.md  -> 07fa41948d1d7bb81b716612ca7c6209872dc25bd63fd15fb378fe9a9792b9b8
$ grep -n 'corrections=[0-9]' ScribeScorecardRound43.append.md   -> (no match; exit 1)
$ grep -c 'Correction (round 43)' ScribeScorecardRound43.append.md -> 1
$ grep -o 'closed=[0-9]*/[0-9]*' ... | sort | uniq -c
      1 closed=12/13
      1 closed=13/13
      2 closed=13/19
      2 closed=19/19
$ grep -o 'selftest cases=[0-9]* failures=[0-9]*' ... | sort | uniq -c
      2 selftest cases=19 failures=0
$ python3 (unescaped-pipe cell split per table block)
result table rows: 5 cells each (3 rows + header + separator)
capabilities table rows: 4 cells each
move-log rows: 5 cells each
```

### 6. Lane state at read time

```
$ git rev-parse HEAD
4cb6d4ae768481e1a14afbedc2d865a060ebacfd
$ ls corpus/instruments/r43-closure.sh corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/
ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory
ls: cannot access 'corpus/instruments/claim-package-check.py': No such file or directory
ls: cannot access 'corpus/instruments/fixtures/claim-package/': No such file or directory
$ git status --porcelain
?? .ufo/waves/round-43/INTEGRATION-PLAN.md
?? .ufo/waves/round-43/w1-REGISTRY.txt
?? .ufo/waves/round-43/w1.ready
?? .ufo/waves/round-43/w1.ready.partial
?? .ufo/waves/round-43/w1/
$ ls .ufo/waves/round-43/w1/
ExecGateManifest.rules.py  ExecK19Freeze.sh  ExecK19Freeze.transcript.txt
ExecSourceCapture.S067.txt  ExecSourceCapture.manifest.json  ExecSourceCapture.provenance.txt  swarm-registry.json
```

No tracked lane file is modified; the worktree delta is untracked wave material only. I ran no mutating
git/jj command anywhere (reads only: `rev-parse`, `log`, `cat-file`, `show`, `status`).

## Findings

1. **RD42-1 is exactly as routed.** `SCORECARD.md:1634` carries `corrections=33`; the same export's K11
   prints `corrections=34`. There is exactly one `corrections=<digits>` literal across
   `SCORECARD.md`/`LOG.md`/`SHONEN.md` at `4cb6d4a`; its line also carries `groups=4`.
2. **D-r41-1 duplicate state is intact and byte-identical.** The two four-line `Correction (round 41)`
   blocks sit at 1602-1605 and 1607-1610; nothing in my block edits, deletes or reorders them.
3. **The block deliberately does not restate the stale numeric literal.** K14's supersession is
   "the line carrying the literal must be followed by a `Correction (round 43)` line that names that
   literal verbatim as superseded"; the designated naming line is `ScribeCorrections.scorecard.txt`
   (RD42-1). Repeating `corrections=33` in a second correction line would create a second graded
   occurrence whose supersession depends on the K14 limb's treatment of declaration lines — a risk with
   no upside. My line names the cell by `SCORECARD.md:1634` and states it is superseded, so the closure
   reads correctly while the verbatim naming stays with the block tasked for it.
4. **Base figure is frozen, not observed here.** The frozen assignment requires base `ab98fac9` to print
   `closed=13/19 exit=1` with exactly K14-K19 open; the committed do-nothing control can only measure the
   r42 stand-in (`closed=12/13 exit=1`). The block writes the frozen predicate's figure and points at the
   receipt. If the r43 suite at base instead prints `closed=12/19` (the carried K8 limb seeing the
   post-receipt base commits, as J8 does in the control), the claim's base limb and that cell are wrong
   together; that is a C1 finding, not a scribe edit.
5. **Quoted `closed=`/`selftest` tokens are transcript-bound by K18.** The block quotes
   `closed=19/19`, `closed=13/19`, `closed=12/13`, `closed=13/13` and `selftest cases=19 failures=0`.
   `closed=12/13` is already in `.ufo/waves/round-43/c1-controls/do-nothing.txt`; `closed=13/13` is in the
   round-42 final-gates transcripts; the other three must appear in `.ufo/waves/round-43/final-gates/`
   or they will be unbound quotes. The fix, if any, is the Y receipt (it must tee the run, the base
   control and the selftest), not the block text.
6. **Append is clean.** `SCORECARD.md` EOF is `|\n\n`, so the block appends without a stray join.

## Known limits

- The r43 instruments are absent at HEAD; I observed none of the after-state values. Every after figure
  in the block is the frozen predicate's, and the verdict cells say so. Nothing here is a run I performed.
- I did not run `r43-closure.sh`, `claim-package-check.py`, or any gate/negative control: the tools are
  unlanded, my seat is a scribe, and the round contract puts the single counting pass at Y.
- The K14 limb's implementation was unlanded at read time, so its exact literal-exclusion behaviour for
  a declaration line's own literal is unknown (finding 3 is the consequence).
- The `claim-package-gate` row carries `<pending: demo>` exactly as assigned; I did not convert it.

## Write scope

Writes: this receipt, `.ufo/waves/round-43/w1/ScribeScorecardRound43.append.md`, and scratch under
`/fast/scratch/hyaku/kasegi-r43/ScribeScorecardRound43`. No other lane byte, no fleet-root byte, no
`shokuknow` byte, no PATH directory, no `~/.omp/agent` file. Scratch removed before yield.

## Tooling

No installs or upgrades. No network fetch. `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
was read before work (top consumer at read time: `/fast/scratch/hyaku/kasegi-r43` 3.6G, idle=0); no heavy
pass was run.
