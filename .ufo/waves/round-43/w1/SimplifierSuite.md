# SimplifierSuite — round 43 YAGNI review of the K1-K19 suite

Seat: SimplifierSuite (simplifier, leaf; no subagents). Lane: kasegi-shokunin.
Base: `ab98fac9dce87130bc4f66de89e30650d63943dc`. Freeze commit at review time:
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. All work read-only over committed
bytes and two `git archive` exports; this seat wrote no lane file except this
receipt and deleted nothing.

Scope of this item: which checks overlap, which limbs are dead or unreachable,
which could be one check with two limbs, and which carried r42 checks the r43
tree makes redundant. Recommendations only; the L1 decides and this seat does
not edit the suite.

State of the tree when measured (2026-10-28, ~16:45-16:55Z): limbs K14, K15,
K16, K17, K18, K19 landed in `.ufo/waves/round-43/w1/`; `ExecSelftest19.sh`
landed; `ExecSuiteSkeleton` and `ExecCarryChecks` had **not** yet produced
`r43-closure.sh`. So the sixteen carried checks were reviewed as source
(`corpus/instruments/r42-closure.sh`) and the six new checks were reviewed **as
run**, at both exports.

## 1. What I ran (verbatim)

```
$ S=/fast/scratch/hyaku/kasegi-r43/SimplifierSuite
$ git -C …/kasegi-shokunin archive ab98fac9… | tar -x -C "$S/base"    # 152M
$ git -C …/kasegi-shokunin archive 4cb6d4a… | tar -x -C "$S/head"    # 153M

$ for ref in base head; do bash …/ExecK15WaveNarrative.sh "$S/$ref"; done
base: K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
      K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 stated-seats=36 unbacked=no-evidence
      K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
      K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
head: identical payload and the same three details

$ bash …/ExecK14Corrections.sh "$S/base" ; bash …/ExecK14Corrections.sh "$S/head"
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0   (base)
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0   (head)

$ bash -c '. …/ExecK16Placeholder.sh; check_k16 "$S/base"'
payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0                      (base and head)

$ bash …/ExecK17ClaimsBefore.sh --tree "$S/base"
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
$ bash …/ExecK17ClaimsBefore.sh --tree "$S/head"
… same unbacked line …
K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0

$ bash …/ExecK18Transcript.sh "$S/base" --verbose
K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=selftest cases=13 failures=3 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:177
K18 scope records=2 transcripts=160
head: identical.

$ bash -c '. …/ExecK19Freeze.sh; check_k19 "$S/base"'
K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
$ bash -c '. …/ExecK19Freeze.sh; check_k19 "$S/head"'
K19 payload=freeze=present,order=ok,sha=match closed=1

$ git log -1 --format='author=%ai%ncommitter=%ci' 4cb6d4a
author=2026-10-28 13:27:52 -0300        (16:27:52Z, inherited from ab98fac9)
committer=2026-10-28 13:37:11 -0300     (16:37:11Z)
# .ufo/waves/round-43/freeze.txt frozen-at=2026-10-28T16:37:07Z -> 4 s before the
# committer instant: the RD42-6 shape does not recur in the round-43 record.
```

Supporting censuses I wrote in scratch and ran over `git show` bytes (scripts
removed with the scratch dir): a claims-token census over 20/21
`claims.json`, a quoted-tally census over `corpus/lessons/**`, a named-wave
census over `LOG.md` + 65 lesson files, and a copy of the K18 limb narrowed to
the frozen predicate's evidence dirs.

## 2. Measured live surface per new check (base | head)

| check | what it grades | base | head |
|---|---|---|---|
| K14 | `corrections=`/`groups=` literals vs re-derived `check_j11` | literals=2 stale=1 closed=0 | same |
| K15 | dispatch sentences vs wave evidence | sentences=5 unbacked=3 | same |
| K16 | `## ` promise sections vs correction | sections=491 promises=1 fenced=0 unresolved=1 | same |
| K17 | claims `before` tallies vs cited control | claims=20 tokens=3 unbacked=1 | claims=21 tokens=5 unbacked=1 quoted=2 |
| K18 | quoted `closed=`/`cases=` vs transcripts | quotes=22 bound=19 unbound=3 | same |
| K19 | freeze record vs controls + digest | freeze=absent closed=0 | present/ok/match closed=1 |

Two facts follow that the r43 report should state. (a) K19 is **already closed
at the freeze commit** and cannot regress unless `claims.json` or `freeze.txt`
is edited; it is a guard on the freeze bundle, not a repair of the round's
narrative bytes. (b) K14/K15/K16/K18 are all still red at the freeze commit —
they are waiting on the Scribe corrections, which is the intended landing order.

## 3. The three overlaps named in the item

### 3.1 K14 vs K11 (correction ledger) — real duplication, mergeable

K11 (carried `check_j11`) already re-derives the ledger and prints
`corrections=<c>,groups=<g>`; K14 prints the **same** derivation as
`live=corrections=<c>,groups=<g>`. Measured: both report `34`/`4` at base and
head. K14's landed limb derives by `exec`-ing the r42 instrument's embedded
engine and calling its `check_j11`
(`ExecK14Corrections.sh:53,119,142`), while K11 will be a copy of that same
function body (`ExecCarryChecks` instruction). So the tree would hold two
authorities for one number and K14 trusts the older one.

K14's unique signal is only `literals`, `stale`, `superseded` — a comparison of
prose literals against that derivation. That is a second limb of one check, not
a second check.

- Delete: K14's separate K line.
- Coverage keeper: K11, whose payload gains `literals=…,stale=…,superseded=…`.
  Every byte K14 reads is already read by K11; the only new assertion is
  `stale==0`, carried verbatim.
- Verdict: **deferred** — the frozen C1 predicate requires a `K14` line and
  `selftest cases=19`. Land the merge at round 44 (19 → 18).

### 3.2 K18 vs the transcript rule — not the overlap it looks like; one shared helper, one stale constant

The transcript rule in the carried set is **K2** (`check_j2`:
`prior_truth` reads `PRIOR_RECEIPT_REL` at `r42-closure.sh:576`, and
`mangled_tallies` rejects a correction line that prefixes a true token). K1 is
the per-correction *evidence-id* rule and does not touch transcripts. So K18
does not duplicate K1, and it does not duplicate K2 either: K2 grades
correction lines of round 43 against the **round-41** receipt, K18 grades quoted
tallies in round-42/43 prose against round-42/43 transcripts. Different bytes,
different subjects.

What is duplicated is the *mechanism*: K2 has `token_at`/`value_present` with a
`TOKEN_BAD` allowlist; K18 defines its own lookarounds
(`ExecK18Transcript.sh:66-67`, `(?<![0-9/])closed=…(?![0-9/])`). Two whole-token
conventions in one suite is exactly the failure the lane keeps correcting.
Recommendation: K18 imports the carried boundary helper; no check deleted.

The stale constant, though, is a real carried-check defect:

```
$ git show HEAD:.ufo/waves/round-41/final-gates/all-gates.txt | grep -oE 'closed=…|failures=…|cases=…' | sort -u
cases=12  closed=10/12  failures=6
$ git show HEAD:.ufo/waves/round-42/final-gates/all-gates.txt | … 
cases=13  closed=13/13  closed=3/3  failures=0
```

If K2 is carried with `PRIOR_RECEIPT_REL` unchanged, the r43 suite grades the
round-43 corrections against **round-41** tokens: a mangled `closed=13/130` (the
r42 value) is not caught, because `closed=13/13` is not in the r41 truth set.
K2 must roll to `.ufo/waves/round-42/final-gates/all-gates.txt`. Measured
consequence for the carry contract: the payload shape is unchanged
(`truth-tokens` stays 3), so the cell-for-cell rule survives — this is the one
constant that must move without a payload difference.

### 3.3 K19 vs K17 (control reading) — same loader, different assertions

Both load `claims.json`, resolve `controls.c1|c2` relative to the export and
refuse escapes; K17 does it to bind tally tokens, K19 to bind `measured-at`
plus the freeze record and its digest. Neither assertion subsumes the other, but
the loader and the freeze-bundle context are one subject: the frozen claims and
the evidence they cite.

- Delete: K19's separate K line.
- Coverage keeper: K17 extended with two limbs — `freeze-order` (relations 1-4
  of `ExecK19Freeze.sh:15-40`) and `claims-sha256` (relation 5). All five
  relations keep their assertions; K17 already owns the path-resolution code
  K19 re-implements.
- Verdict: **deferred to r44** (same reason as 3.1).

## 4. Dead, unreachable, or non-discriminating limbs (measured)

1. **K13 `named=` is a tautology.** `suite_scratch_root()` builds the path as
   `SCRATCH/r42-${REF[:12]}` (`r42-closure.sh:1177-1178`) and `named` tests
   whether `REF[:12]` occurs in that basename (`:1191`). It is 1 for every ref.
   Delete the field; the check keeps `faithful/extra/missing/strays/markers`.
2. **K1 `union=` is a redundant conjunct.** `union` (`r42-closure.sh:547`) is
   `|{rec : r_ev < n}|`, so `union == 0` iff `missing == 0`, and `ok` already
   requires `missing == 0`. The term can never be the failing one, and the name
   ("a cross-record union would have counted evidence found in a different
   record") describes a computation the code does not perform. Delete the field
   and the conjunct; keep `missing`.
3. **K10 is ref-invariant.** Its payload is a function of the selftest harness,
   not the export: at base and head it is identical
   (`cases=13,isolated=13,canary=0,graded-lines=13,fixture=synthetic`), and every
   case result it reads comes from the run's own `run_selftest` pass
   (`r42-closure.sh:2159-2165`). Nothing in a committed tree can red it.
4. **K9's leaf payload has no reader.** The `--leaf` branch emits
   `depth=leaf,base=deferred,r41=deferred,deferred=1,accept=tree-red`
   (`r42-closure.sh:1695-1696`); K9's own consumer filters dependent reds to
   `("J1","J2","J3","J4","J8","J11")` and drops the leaf line. Keep the flag,
   drop the never-read payload text.
5. **K16's `fenced` limb has no committed data** (`fenced=0` at both refs). The
   exclusion is proven only by the selftest fixture. Acceptable, but do not
   count it as coverage of committed bytes.
6. **K19 cannot see the routed defect, and its base red is "absent".** RD42-6's
   defect is a freeze label later than the commit that contains it; a
   `git archive` export has no `.git`, so K19 structurally cannot test that
   relation. It tests the proxy (controls' `measured-at`, `freeze.txt` label,
   digest), which is green at the freeze commit and red at base only because
   `.ufo/waves/round-43/` does not exist there. The round is clean under the
   proxy and under the committer instant (16:37:07Z ≤ 16:37:11Z). Note the trap
   for whoever writes the lesson: the commit's **author** date is 16:27:52Z
   (inherited from `ab98fac9`) and would false-positive an author-date reading.
7. **K14's spec exclusion is dead as written; the landed rule is the live
   one.** The frozen text says a literal "on a line whose own text also carries
   `payload=` … is evidence, never a result". The only stale literal in the
   three records is `SCORECARD.md:1634`, and that line carries
   `J11 payload=corrections=33,…` while quoting no mutant and sitting in no
   fence — the sentence as written would hide the one defect K14 exists to
   grade. The landed limb's `evidence_mode`
   (`ExecK14Corrections.sh:92-102`) skips only a **fenced** line carrying
   `payload=`; a line carrying `mutant=`/`quarantined` is graded for its
   `live=` claims only; everything else is graded whole, which is why the limb
   reads `literals=2,stale=1`. Keep the limb; do not quote the predicate
   sentence as the rule in the round-43 lesson. (The limb bytes were edited at
   13:50:57Z during this review; the payloads above are from re-runs after that
   edit.)
8. **K15's spec path rule is wrong for rounds ≤39, and the limb is right.**
   Rounds 31/33/34/35 store `wave1-results.json`/`wave2-results.json`, not
   `<wave>-results.json`; a literal implementation reds five historical
   sentences for a filename convention. The landed limb's evidence chain
   (`wave<label>-results.json` → `<named-wave>-results.json` → seat-receipt
   corpus with the stated seat count) resolves them: measured
   `sentences=5,unbacked=3`, and the three reds are exactly RD42-2/3. Record the
   chain as the rule, or a reimplementation will red history.
9. **K17's "before/after" is wider than the limb, and the widening is
   unsatisfiable.** A census over all `claims.json` finds 4 unbacked `before`
   tokens and **37 unbacked `after` tokens across 9 rounds** (round-43's own
   `after` promises included: `closed=19/19`, `cases=19`, `closed=13/19`, C2
   `cases=10`). An `after` cell is a target, not a measurement; it cannot appear
   in a control receipt written before the round. The landed limb skips `after`
   (`ExecK17ClaimsBefore.sh:326`) and reports exactly one unbacked token at both
   refs — the RD42-8 defect. That reading is correct; the predicate wording
   should be quoted as "every `before` literal".

## 5. Merges: one check, two limbs

| # | delete | keeper (merged check) | limbs that survive | count |
|---|---|---|---|---|
| M1 | K14 | K11 | ledger derive + literal staleness | 19→18 |
| M2 | K16 | K15 | dispatch sentences + section promises, one `Correction (round 43)` resolution rule | 18→17 |
| M3 | K19 | K17 | claims before-token binding + freeze ordering + claims digest | 17→16 |
| M4 | K10's K line | runner assertion + K8 | selftest isolation/canary becomes an assert inside `run_selftest`; K8 keeps `selftest-lines/verdicts/summary` | 16→15 |

M2's evidence: K16's only committed promise is
`corpus/lessons/round-42.md ## Wave-2 falsification`, and K15's reds #2/#3 are
lines 11/16 of the same file about the same wave; both are retired by one
appended correction naming the wave or heading. The two scans already share the
file set and the retirement instrument, so they are two limbs of "a committed
record must not refer to a wave artifact that does not resolve".

M4 is a demotion, not a deletion of behavior: if the L1 will not spend the K
line on a ref-invariant property, the same assertions (isolated==cases,
canary==0, every graded line parses) must run as asserts in the selftest runner
so a leak still fails the suite. If that is unacceptable, keep K10 and accept
one non-discriminating line.

## 6. Carried r42 checks the r43 tree makes redundant

- **None wholesale.** Each of K1-K13 keeps a subject the others do not: K1
  evidence ids, K2 whole-token tallies, K3 registry integrity, K4 declared
  blocks (must be regenerated for the new paths), K5 scratch hygiene, K6
  binding existence, K7 frontier flip, K8 receipt integrity, K9 nested negative
  controls, K11 ledger uniqueness, K12 no-harm, K13 quiescence. Delete none of
  these on the strength of an r43 merge.
- **K10 is the only line whose content is redundant** with the selftest summary
  (`selftest cases=19 failures=0`) plus K8's `selftest-lines`/`verdicts`. See M4.
- **Two carried constants must move, and one conflicts with the carry
  instruction.** K2's `PRIOR_RECEIPT_REL` must be the round-42 receipt (§3.2).
  K12's `BASE_REF` must be `ab98fac9…` for a round-43 no-harm guard; K12 prints
  `base=<BASE_REF[:8]>` in its payload, so the `ExecCarryChecks` "match
  cell-for-cell" instruction cannot hold for that one cell if K12 is re-pointed.
  Resolve explicitly: allow `base=` to differ, pin the other eleven.
  `DENSITY_SHA` can stay (`density.py` is unchanged since `5053a7f4`; the base
  control prints `density-sha=ee803726a322` closed=1).
- **Weight note (cost, not defect).** A plain run executes the entire selftest
  to mint the receipt (`run_selftest` inside `main`, `r42-closure.sh:2159`), so
  the 19-check run pays for 19 mutation suites twice over (run + selftest). That
  is the price of the receipt grammar; nothing to cut without changing C1.

## 7. Divergences the L1 must adjudicate (frozen text vs landed limb)

1. **K17**: predicate says `before`/`after`; limb grades `before` only. The
   narrowing is necessary (§4.9). The report should quote the narrowing, or the
   claim is unsatisfiable at Y.
2. **K18**: predicate names evidence "under the round's `final-gates/` or
   `c1-controls/`"; the limb reads every non-record file under
   `.ufo/waves/round-42|43/` (`ExecK18Transcript.sh:76`). Measured with the
   limb's own engine narrowed to the four predicate dirs: `bound=14,unbound=8`
   instead of `bound=19,unbound=3`. The 5 occurrences gained are bound only by
   `.ufo/waves/round-42/wave1/RevC1Counters.md` (`closed=10/12`) and
   `.ufo/waves/round-42/wave1/ExecSuiteCore.transcripts.txt` (`closed=4/13`,
   `closed=5/13`). Both are committed, summary-shaped seat transcripts, so the
   spirit holds; the letter of the predicate does not. Decide: tighten the limb
   and land those transcripts under `final-gates/`, or state the broader
   definition of "transcript" in the report. Do not leave the two texts
   contradicting.
3. **K14**: predicate exclusion sentence is dead as written (§4.7); quote the
   landed rule instead.

## 8. Ranked recommendations

1. **Now (no claim change):** amend the round-43 lesson/report wording for K14,
   K15, K17, K18 to the landed rules (§4.7, §4.8, §4.9, §7.2). Nothing is
   deleted, and every measured behavior is already what the landings do; the
   risk is a critic grading the predicate prose instead of the instrument.
2. **Now:** K2's `PRIOR_RECEIPT_REL` → round-42 receipt; K12's `BASE_REF` →
   `ab98fac9…` with the `base=` cell exempted from the cell-for-cell rule.
3. **r44:** M1 (K14→K11) and M3 (K19→K17) — pure merges, coverage kept by the
   keeper, no behavior lost.
4. **r44:** M2 (K16→K15) — merge the two narrative-reference limbs.
5. **r44:** M4 — demote K10 to a runner assertion; never delete the assertions
   themselves.
6. **Do not delete:** K1-K9, K11-K13 as checks; only the dead fields in §4.1,
   §4.2 and the unread leaf payload in §4.4.

## 9. What this seat did not do

No lane file edited, no suite file touched, no deletion performed, no subagent
dispatched, no network fetch, no mutating git command (only `log`, `show`,
`ls-tree`, `rev-parse`, `archive`). No tool installed, so no tool record.
Scratch `/fast/scratch/hyaku/kasegi-r43/SimplifierSuite/` (exports, censuses,
the narrowed K18 copy) is removed before yield; the shared tree was never
written.

Deliverable: this receipt is the only artifact; no byte-exact landable text was
produced by this item.

Receipt: 324 lines. sha256 `b5527e7707a75c4aba0de27e3790f141b092ab662770a657a9cfc7a2ec6e884c` is the digest of the 322-line body above (this line and the blank line before it were appended after that digest); no other artifact was produced.
