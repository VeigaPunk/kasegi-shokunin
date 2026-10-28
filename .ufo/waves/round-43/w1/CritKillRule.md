# CritKillRule — C1 kill-rule re-derivation and firing attempts (kasegi round 43)

Seat CritKillRule (leaf, receipt-only). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
at head `4cb6d4a` (base `ab98fac9`; round-41 judged head `1f746461`; round-42 Y `b2c49ea`).
Read first: `.ufo/waves/round-43/claims.json` (sha256 `a4c03e1e…`, 78 lines), and both controls
(`c1-controls/do-nothing.txt`, `c2-controls/before.txt`). No lane file was written except this
receipt; no git/jj mutation was run (only `git log/show/cat-file/archive/rev-parse/diff`);
no tool needed installing; scratch `S=/fast/scratch/hyaku/kasegi-r43/CritKillRule` was created,
used for every extraction and tree copy, and removed at the end (verified absent).

## 0. The object the clauses name does not exist yet in any committed ref

```
$ for r in ab98fac9 1f746461 b2c49ea 4cb6d4a; do printf '%s ' $r; git cat-file -e $r:corpus/instruments/r43-closure.sh 2>/dev/null && echo PRESENT || echo absent; done
ab98fac9 absent
1f746461 absent
b2c49ea absent
4cb6d4a absent
```

So each clause is fired against the nearest committed bytes it names, and against the in-flight
limb snapshots, and each row below says exactly which bytes were tested. The committed analogue is
`corpus/instruments/r42-closure.sh` (sha256 `fca5ae62379e0123…`), which C1 says K1-K13 carry with
"the r42 J1-J13 payload grammar and their replay limbs" unchanged.

In-flight snapshots tested (uncommitted; hash is the exact bytes reviewed, they may change):

| file | sha256 (prefix) |
|---|---|
| `.ufo/waves/round-43/w1/ExecK14Corrections.sh` | `9fb97b4ce93a9d61…` |
| `.ufo/waves/round-43/w1/ExecK16Placeholder.sh` | `d7c33c9efdcfb5ab…` |
| `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.sh` | `37a513ed7dfbc8dd…` |
| `.ufo/waves/round-43/w1/ExecK18Transcript.sh` | `8b797e424d5d3f35…` |
| `.ufo/waves/round-43/w1/ExecK19Freeze.sh` | `8e6b124feb975469…` |
| `.ufo/waves/round-43/w1/ScribeClaimsErratum.claims-erratum-1.md` | `fcb439506093241d…` |
| `.ufo/waves/round-43/w1/ExecTranscriptDe0931.txt` (33 lines) | `8c3f9dd553fe24e8…` |
| `.ufo/waves/round-43/INTEGRATION-PLAN.md` | `d26658957e28d8de…` |

`ExecK15WaveNarrative.sh` did not exist at review time — K15 is untestable.

## 1. The ground under clause (i): the base measurement

```
$ bash corpus/instruments/r42-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
      --work $S/base/w --scratch-root $S/base/scr
… (13 payload lines)
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,
   ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=0,run-lines=1,selftest-lines=1,verdicts=1,
   summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=0
closed=12/13 exit=1
real 3m8.7s   exit=1
```

This reproduces the committed do-nothing control byte-for-byte (`run-utc=2026-10-28T16:27:52Z`,
`suite-sha256=fca5ae62…`, `closed=12/13`): the r42 check that reds at base is **J8**, and only on
`diff=0` — the base carries three commits after the r42 receipt (`30e67f6`, `ad20c02`, `ab98fac9`).
Every other carried check closes while the six routed r42 narrative defects stand (e.g. J11 prints
`corrections=34 … closed=1` while `SCORECARD.md:1634` still says `corrections=33`).

## 2. Clause verdicts

| clause | verdict | where the evidence is |
|---|---|---|
| (i) a K14-K19 check green at base | **NOT FIRED** for K14, K16, K17, K18, K19 (all red at base). K15 **untestable** (no deliverable). | §3.1 |
| (ii) a mutant accepted | **FIRES** for the K14 limb: a fabricated literal on a `Correction (round 43)` line is counted `superseded` and the check closes. The brief's literal exclusion rule would also accept the real base defect. K15-K19 mutants untestable (no assembled instrument). | §3.2 |
| (iii) a carried replay limb skipped | **NOT FIRED as a skip** (removing the artifact, or the replay substrate, reds the check), but the claim's word "re-executed" is false: the artifact bytes are never read, and J6/J7's limbs re-run the clean check. | §3.3 |
| (iv) a forged receipt accepted | **FIRES.** An edited J8 self-line, a permuted line order, and a receipt planted off the canonical path are all accepted (`closed=1`). | §3.4 |
| (v) a plain run not exiting 2 | **UNTESTABLE for r43** (the script is absent; `bash` exits 127, not 2). The committed analogue exits 2, including `--selftest` without a ref. | §3.5 |
| (vi) a ref-not-found that still prints a closed line | **NOT FIRED**: no `^closed=<n>/<m> exit=<n>` line; distinct `ERROR ref-not-found`, exit 1. Brittleness: the error line carries the bare token `closed=0`. | §3.6 |
| (vii) a selftest summary-only line satisfying a case | **NOT FIRED**: a summary-only receipt is rejected (`selftest-lines=0`, `lines=0`); a case needs the full graded line grammar. | §3.7 |

## 3. Clause detail (command → observed output → verdict)

### 3.1 (i) a K14-K19 check green at base

The five implemented limbs against an export of base `ab98fac9` (`$S/base/w/export`,
extracted with `git archive ab98fac9 | tar -x`):

Each limb was copied byte-for-byte into `$S/k14.sh` / `$S/k17.sh` before running (so the reviewed
bytes cannot change under the test); `$S/ExecK16Placeholder.sh`, `$S/ExecK18Transcript.sh` and
`$S/ExecK19Freeze.sh` are the same-named copies.

```
$ bash $S/k14.sh $S/base/w/export
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
exit=1

$ bash -c '. $S/ExecK16Placeholder.sh; check_k16 $S/base/w/export'
payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
exit=1

$ TMPDIR=$S bash $S/k17.sh --tree $S/base/w/export --work $S/k17w-base
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
exit=1

$ bash $S/ExecK18Transcript.sh $S/base/w/export
K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
exit=1

$ bash -c '. $S/ExecK19Freeze.sh; check_k19 $S/base/w/export'
K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
exit=1
```

Verdict: the clause does not fire on the delivered limbs — every one of them is red at base, and
each red names its own committed defect (K14 `SCORECARD.md:1634`; K16 the round-42 `## Wave-2
falsification` promise; K17 the round-42 `closed=10/12` cell; K18 three quoted values; K19 the
round-43 freeze record absent from base). K19 was also run on a head-shaped tree
(`$S/y2/export` = base export + the round-43 directory): `K19 payload=freeze=present,order=ok,sha=match closed=1`
— it is gradeable and its base red is real, not structural. K15 has no bytes to test.

### 3.2 (ii) a mutant accepted

The clause names mutants built from the committed r42 defeat bytes; those mutants do not exist
because K14-K19 do not exist. What can be fired now is the acceptance surface of the delivered
limbs.

**K14 phantom supersession (fires).** On a tree whose real staleness is repaired, a
`Correction (round 43)` line that carries a literal which never existed is counted as superseded and
the limb closes:

```
$ bash $S/k14.sh $S/base/w/export                    # real defect present
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0   exit=1

# base export + one Correction (round 43) line naming corrections=33 superseded
$ bash $S/k14.sh $S/green/export
K14 superseded=SCORECARD.md:1634 corrections=33 live=35
K14 payload=literals=4,stale=0,superseded=3,live=corrections=35,groups=4 closed=1    exit=0

# same green tree + a marker line carrying "superseded corrections=999" (never existed)
$ bash $S/k14.sh $S/phant2/export
K14 superseded=LOG.md:1808 corrections=999 live=36
K14 payload=literals=5,stale=0,superseded=4,live=corrections=36,groups=4 closed=1     exit=0
```

The limb's own comment says a marker line is "a carrier of every literal it names" and exempts the
self-naming occurrence. Nothing checks that a named literal ever occurred, so a fabricated literal is
recorded as a supersession. The payload then asserts four supersessions where three exist.

**The brief's literal exclusion rule would accept the real defect.** K14's brief excludes "a literal
on a line whose own text also carries `payload=`". The only stale literal lives on such a line, so a
limb implemented to the letter closes at base:

```
$ python3 $S/k14probe.py     (rule A = brief as written; rule B = exclude only an anchored payload line)
 SCORECARD.md:1634 corrections=33  ruleA(exclude if 'payload=' in line)=True  ruleB=False stale=True
 ruleA graded=0 stale=0 closed=1
 ruleB graded=2 stale=1 closed=0
```

The delivered `ExecK14Corrections.sh` avoids this (its exclusion also requires a fence or one of
`defeat/rejected/rejects/attack` on the line), which is why §3.1 is red. That deviation from the
brief is **required**, not optional, and should be recorded so a later re-fork does not relapse.

### 3.3 (iii) a carried replay limb skipped

Static: the committed defeat artifacts are used in exactly one place — the digest check:

```
$ grep -n "DEFEAT_ARTIFACTS" corpus/instruments/r42-closure.sh
167:DEFEAT_ARTIFACTS = {
1214:    rel, digest = DEFEAT_ARTIFACTS[family]        # inside artifact_ok()
```

No `replay_*` function reads the artifact's bytes; each builds its mutation from the *live* records
(`replay_j1` strips evidence from the live correction lines, `replay_j3` edits the live `SKILL.md`
row, `replay_j5` builds its own fixture). J6 and J7 have no mutation at all:

```
1395:def replay_j6(tree):
1396:    _p, ok = check_j6(tree)
1397:    return (1 if ok else 0), ("rejected" if ok else "accepted")
1400:def replay_j7(tree):
1401:    _p, ok = check_j7(tree)
```

Dynamic: skipping is caught, on a clean copy of the base export (`$S/rp2/*`, hardlink copy with
unlink-before-write so the source tree is untouched):

```
control-clean  J1: (…,replay=RevC1Counters.md=rejected', True)
control-clean  J3: (tables=18,rows=73,r42-rows=1,…,replay=MutSkillTablePipes.md=3/3', True)
no-artifact    J1: (…,replay=artifact-missing:RevC1Counters.md', False)      # artifact deleted
no-substrate   J3: (tables=18,rows=72,r42-rows=0,…,replay=MutSkillTablePipes.md=no-substrate', False)
```

Verdict: the limb cannot be *skipped* silently (digest loss and substrate loss both red). But the
receipt's `replay=<artifact>=rejected` states that the *committed artifact* was rejected, and the
instrument never feeds the artifact to anything; for J6/J7 the limb cannot fail unless the check
itself is already red. A literal reading of "skips its defeat" fires on that wording. See D7.

### 3.4 (iv) a forged receipt accepted — fires

Harness: the committed r42 engine imported as a module (extracted verbatim from
`r42-closure.sh`), `EXPORT` set to an export of Y (`b2c49ea`), `REF=b2c49ea`, live payloads taken
from the committed receipt's 12 deterministic lines (the receipt's own `payload-match=12/12` at Y),
receipt mutated inside a hardlink copy of the tree. Baseline and mutations:

```
baseline             closed=1  …payload-match=12/12,forged=6/6
M1-j8-self-line      closed=1  …payload-match=12/12,forged=6/6     ← J8 line rewritten to "receipt=forged,source=forged,diff=0,payload-match=0/12,forged=0/6 closed=0"
M2-swap-J1-J2        closed=1  …payload-match=12/12,forged=6/6     ← J1 and J2 lines transposed
M3-summary-only      closed=0  lines=0,selftest-lines=0,verdicts=0,forged=5/6
M4-stray-line        closed=0  no-stray=0
M5-run-utc           closed=0  utc=0,forged=5/6
M6-two-headers       closed=0  lines=0,no-stray=0
M7-J1-payload        closed=0  payload-match=0,11/12
M8-tally-exit        closed=0  closed-line=0,forged=5/6
M9-reversed-cases    closed=1  …payload-match=12/12,forged=6/6     ← the 13 selftest case lines reversed
M10-j8-facts         closed=1  …payload-match=12/12,forged=6/6     ← J8's own diff=1→0, payload-match 12/12→11/12
```

Cause: `DETERMINISTIC` excludes J8 (line 130) because J8 is the grader, so the J8 payload line is
the one line never re-derived; and `parse_receipt` is order-agnostic (dicts keyed by check id), so
line order is never compared to the canonical sequence even though `receipt_lines()` already
reconstructs that sequence.

Compound with the locator: `locate_receipt` falls back to "the first `all-gates.txt` anywhere under
`.ufo/waves/round-42/`" (lines 1494-1506). Remove the canonical receipt, plant the M1-forged text at
`.ufo/waves/round-42/wave1/all-gates.txt`, and J8 still closes:

```
locate_receipt -> .ufo/waves/round-42/wave1/all-gates.txt
closed=1 receipt=.ufo/waves/round-42/wave1/all-gates.txt,source=committed,…payload-match=12/12,forged=6/6
```

Verdict: clause (iv) fires on the carried check. A receipt that is not the canonical one, carries an
edited J8 self-line, and has been reordered is admitted as a clean receipt — the exact opposite of
"one unedited tee of one run". See D6 for the smallest fix.

### 3.5 (v) a plain run not exiting 2

```
$ bash corpus/instruments/r43-closure.sh            # absent at head
bash: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

$ bash corpus/instruments/r42-closure.sh ; exit=2
r42-closure: a plain run is refused (export mode only)
r42-closure: usage: r42-closure.sh --export-ref <hash> [options]

$ bash corpus/instruments/r42-closure.sh --selftest ; exit=2     # same two lines
```

Verdict: cannot fire — the r43 instrument does not exist at any committed ref, so the counting
command exits 127, not 2. The committed analogue is correct. **Must be re-run at Y**; a green
`--export-ref` run is the only evidence that counts.

### 3.6 (vi) a ref-not-found that still prints a closed line

```
$ bash corpus/instruments/r42-closure.sh --export-ref deadbeef…deadbeef
ERROR ref-not-found ref=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef closed=0 exit=1
exit=1
$ … | grep -cE '^closed=[0-9]+/[0-9]+ exit=[0-9]+$'
0
$ … | grep -o 'closed=[0-9]*'
closed=0
```

Verdict: does not fire — no tally line, distinct red, exit 1. Note the brittleness: the error line
carries `closed=0`, so an unanchored consumer (`grep closed=`) can read it as a red tally. See D8.

### 3.7 (vii) a selftest summary-only line satisfying a case

M3 above (all 13 `selftest case=` lines removed, summary kept) is rejected: `lines=0` (the receipt
must be 33 lines: 5 header + 13 payload + 1 tally + 13 cases + 1 summary) and `selftest-lines=0`
(13 graded lines required), both facts 0. The selftest runner itself derives each case line from
`selftest_case()` (`r42-closure.sh:1916-2076`), and `selftest_pass` computes the summary from the
same list it prints (line 2095-2106), so a summary cannot stand in for a case.

Verdict: does not fire on the carried design. Note the related, weaker defect: the summary-only
mutation drops `forged` from 6/6 to 5/6 because forgery v5 no longer has a case line to flip — a
degraded fixture count, not an acceptance.

## 4. Defects with the bytes, impacted axes, smallest safe correction

### D1 (high — Y-blocker): the planned repairs do not green K18; the erratum draft reds it

`ExecK18Transcript.sh` at a head-shaped tree (base export + the round-43 directory incl. the erratum
draft and INTEGRATION-PLAN.md) is red with 12 unbound quotes; at base it is red with 3:

```
$ bash $S/ExecK18Transcript.sh $S/y2/export
K18 payload=quotes=36,bound=24,report-only=0,superseded=0,unbound=12 closed=0       exit=1
K18 unbound token=closed=19/19 at .ufo/waves/round-43/INTEGRATION-PLAN.md:31
K18 unbound token=selftest cases=19 failures=0 at .ufo/waves/round-43/INTEGRATION-PLAN.md:32
K18 unbound token=closed=13/19 at .ufo/waves/round-43/INTEGRATION-PLAN.md:41
K18 unbound token=closed=12/12 at .ufo/waves/round-43/claims-erratum-1.md:5
K18 unbound token=closed=19/19 at .ufo/waves/round-43/claims-erratum-1.md:9
K18 unbound token=closed=13/19 at .ufo/waves/round-43/claims-erratum-1.md:9
K18 unbound token=selftest cases=19 failures=0 at .ufo/waves/round-43/claims-erratum-1.md:9
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=selftest cases=13 failures=3 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:177
```

Two of those are the round's own repair documents, and the planned RD42-5 repair cannot bind the
others: the transcript deliverable at `de09313` prints **`closed=12/13 exit=1`** and
`selftest cases=13 failures=1`, not the quoted `closed=10/13` / `failures=3`:

```
$ grep -n '^closed=' .ufo/waves/round-43/w1/ExecTranscriptDe0931.txt
19:closed=12/13 exit=1
$ tail -1 .ufo/waves/round-43/w1/ExecTranscriptDe0931.txt
selftest cases=13 failures=1
```

Landing that transcript (tested at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`) changes
nothing: `K18 payload=quotes=36,bound=24,report-only=0,superseded=0,unbound=12 closed=0`.

Impacted axes: depth:verifiability, coverage (C1 dies at Y; C2's own gate transcript may add
`selftest cases=10 failures=0` unbound if it does not land under `final-gates/` or `c1-controls/`).

Smallest safe correction (append-only, no check change):
1. Append a `Correction (round 43)` block to `corpus/lessons/round-42-verifier-spotcheck.md` naming
   `closed=10/13` and `selftest cases=13 failures=3` superseded by the committed de09313 transcript's
   actual lines (`closed=12/13`, `selftest cases=13 failures=1`) and citing its path; the transcript
   must still land.
2. Mark the erratum's and the plan's forward-looking sentences `report-only` (the token K18 already
   understands), or stop quoting bare `closed=` targets there. As drafted, the erratum adds five of
   the twelve unbound quotes it was meant to reduce.
3. Do not commit `INTEGRATION-PLAN.md` with bare target tokens, or mark those lines `report-only`.

### D2 (high — Y-blocker under the K17 draft as shipped): the erratum lands in the wrong round dir

K17's `superseded_by()` reads `claims-erratum*.md` in the **same round dir** as the claims file
(`ExecK17ClaimsBefore.sh:219-229`). Round-42's `closed=10/12` therefore needs an erratum in
`.ufo/waves/round-42/`, but `ScribeClaimsErratum` lands at `.ufo/waves/round-43/claims-erratum-1.md`.
Measured:

```
# base: red on the genuine RD42-8 defect (correct)
K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
# head-shaped tree + the erratum draft in round-43 only (as planned)
K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0
# same tree + the same bytes at .ufo/waves/round-42/claims-erratum-5.md
K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1   exit=0
```

Impacted axes: depth:verifiability (Y cannot reach 19/19), coverage.

Smallest safe correction: land the erratum (or a copy of it) as
`.ufo/waves/round-42/claims-erratum-5.md` — append-only, no deletion, no check change. The
alternative (extend the search to `.ufo/waves/round-43/claims-erratum*.md`) is also sound because the
frozen claim says only "a committed claims erratum", without the same-dir restriction; either fix is
one line.

### D3 (medium): K14 counts a fabricated literal as superseded

Evidence in §3.2 (`corrections=999` → `superseded=1`, `closed=1`). A marker line can launder a value
that never existed, and the payload's `superseded=` then asserts a supersession that did not happen.

Impacted axes: depth:verifiability (the counter's own payload becomes a false record).

Smallest safe correction: treat a marker-line literal as superseded only when the same whole literal
also occurs on a non-marker line of the same file; otherwise emit `phantom=<n>` and set `closed=0`.
Four lines in the limb, no grammar change.

### D4 (medium): K16's stdout is outside the suite's line grammar

```
$ bash -c '. $S/ExecK16Placeholder.sh; check_k16 $S/base/w/export' | cat -A | head -1
payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0$
```

Every other limb prints its id (`K14 payload=…`, `K17 payload=…`, `K18 payload=…`, `K19 payload=…`),
and C1 requires one `K<n> payload=… closed=0|1` line per check. If the suite emits the limb's line
verbatim, the run transcript carries a line that the grammar (`^(K\d+) payload=(.*) closed=([01])$`)
cannot match.

Impacted axes: depth:verifiability (receipt grammar), coverage (assembly).

Smallest safe correction: print `K16 payload=…` (one token), or document that the suite composes the
id and make the composer test cover it.

### D5 (medium): C1's frozen `after` pre-declares the base figure its own predicate forbids

`claims.json` C1 `after` says: "base export closed=13/19 exit=1 with exactly K14-K19 open". The same
claim's predicate says: "the exact base figure is measured during integration and quoted in the
report, **never pre-declared**". The measured analogue cannot be 13/19: at base the carried K8 either
finds no round-43 receipt (source=canonical) while the export's `r43-closure.sh` digest is absent
(`sha256_file` on a missing file returns `""` → `suite-sha256=none` → `digest=0`), or, pointed at the
round-42 receipt, hits `diff=0` exactly as J8 does today (`closed=12/13 exit=1`, J8 `diff=0`). Both
paths leave K8 open, so the base tally is 12/19, not 13/19. [INFERENCE for the r43 tally itself —
the suite does not exist; the two mechanisms are read from the committed engine code and the
measured base run.]

Impacted axes: depth:verifiability (the claim text), depth:density (narrative honesty of the round
that exists to grade narrative honesty).

Smallest safe correction: the claims erratum already being drafted must name `closed=13/19`
superseded by the measured base token printed by the integration transcript, and the report must
quote the measured figure. Do not "fix" K8 to close on an absent receipt — that would be the vacuous
pass the kill rule exists to forbid.

### D6 (high): K8 inherits three receipt-integrity holes (clause iv)

Evidence in §3.4. Impacted axes: depth:verifiability (the primary evidence artifact), coverage
(K18's transcript bindings quote receipts).

Smallest safe correction, in order:
1. Pin the receipt: delete the `os.walk` fallback in `locate_receipt` (require `RECEIPT_REL`, or
   require exactly one `all-gates.txt` under the round dir and fail on ambiguity).
2. Restore the tee property: compare the raw line sequence to the canonical sequence already built by
   `receipt_lines(info)`; reject on any difference. This catches M2/M9 (order) and reinforces M4/M6.
3. Re-derive the self line: compare the recorded K8 payload's fact vector (from `sentinel=1` onward,
   excluding the `receipt=`/`source=` prefix) to the recomputed one; reject on any difference. This
   catches M1/M10.

### D7 (low — wording): the replay limbs do not re-execute the committed artifacts

Evidence in §3.3. If K1-K13 are carried unchanged, the receipt's `replay=<artifact>=rejected` is a
false provenance statement, and for J6/J7 the limb cannot fail except when the check is already red.
Impacted axes: depth:verifiability (claim wording). Smallest safe correction: either feed the
artifact's documented mutation into the limb and require rejection, or record
`replay=<artifact>=digest-verified` and amend the claim sentence by erratum. Do not leave the claim's
"re-executed and rejected" standing over limbs that only digest-check.

### D8 (low): the ref-not-found red carries the token `closed=0`

Evidence in §3.6. Impacted axes: depth:verifiability (parser robustness). Smallest safe correction:
emit `tally=none` (or nothing) instead of `closed=0` on the error path; keep exit 1.

### D9 (low — coordination, K15 before it is written)

K15 is unwritten and its brief scans `LOG.md` and all of `corpus/lessons/*.md` for sentences that
assert a named wave was dispatched. Measured at base:

```
corpus/lessons/round-42-verifier-spotcheck.md:174  | RD42-2 | never-true narrative | `LOG.md:1804` |
   "wave 2 `kasegi-r42-falsify` 36 seats dispatched against the repaired head; …"
corpus/lessons/round-42-verifier-spotcheck.md:34   … wave 2 `kasegi-r42-falsify` 36 seats
   rendered/validated … but **undispatched**
corpus/lessons/round-38-verifier-spotcheck.md:33   … results file (73 entries = 73 dispatched tasks)
   … `kasegi-r38-build-results.json` …
corpus/lessons/round-42.md:9-16                    … wave 1 `kasegi-r42-build` dispatched 64 …
```

Three traps: (a) :174 is a *quoted* defect row that the planned corrections do not touch (they append
to SCORECARD.md, LOG.md, round-42.md), so a limb that grades it reds at Y on a file the round did not
route; (b) the substring `dispatched` occurs inside `undispatched` — a word-boundary match is
required; (c) `kasegi-r38-build-results` is a *file* name that matches the wave pattern, so the
resolver must strip a trailing `-results` before requiring `.ufo/waves/round-NN/<wave>-results.json`
(otherwise `.ufo/waves/round-38/kasegi-r38-build-results-results.json` is demanded). Smallest safe
correction: adopt the same R41 quoted-evidence exclusion K14 uses (a sentence that names another
record's defect is evidence), use `\b`, and normalise the `-results` suffix.

## 5. Not tested, and why

- The Y run, 19/19 tally, `--selftest` 19-case output, plain-run exit 2 and ref-not-found of
  `r43-closure.sh`: the file is absent from every committed ref (§0); measuring the r42 analogue is
  the strongest available substitute and is reported above.
- K15's limbs and mutants: no deliverable.
- The assembled suite's `K1-K13` payload equality with r42's `J1-J13` (ExecCarryChecks' own gate):
  two suites cannot be compared until the new one exists; the base run in §1 is the reference the
  carry owner must match cell-for-cell.
- The C2 claim-package gate and its nine fixtures: not this seat's item; K17/K18 only touch it where
  its transcript tokens feed K18 (D1 note).

## 6. Hygiene

- Scratch `S=/fast/scratch/hyaku/kasegi-r43/CritKillRule` created after
  `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` (25% used, 603.9G free);
  all extraction, trees and harnesses under `$S`; removed and verified absent before yield.
- No git/jj mutation anywhere; the only `git` writes were `git archive | tar -x` into `$S`.
- No writes outside the lane except `$S`; no PATH directory touched; no host service restarted.
- No tool installed or upgraded (nothing was needed).
- One misdirected IRC notice about a `souji` registry row (S242 / `corpus/SOURCES.md:189`) arrived at
  this seat; it concerns a different lane and a file outside this seat's write scope, so it was not
  acted on.
