# CritBaselineEscape — base-red attack on C1 K14-K19

Seat: critic (leaf, receipt-only). Round 43, lane `kasegi-shokunin`.
Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; freeze commit `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`;
round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13`. Host clock at first command:
`date -u` = `2026-10-28T16:41:59Z`.

Axes owned: `depth:verifiability` (C1). Attack share: 23/73.

## Verdict

**The base-red requirement survives every degenerate path I could build: no limb and no seam state
I tested makes base `ab98fac9` print better than `closed=13/19 exit=1` with exactly K14-K19 open.**
The draft suite (stubs) measured exactly that, and each of the six landed limbs is red at the base
export for its intended defect — with one exception in *kind*: **K19's base red is an absence-red,
not a defect-red** (F3).

Four false-green paths exist outside base, and one seam can award `verdict=pass` with zero mutants:

| id | where | counterexample result | class |
|----|-------|----------------------|-------|
| F1 | K18 | `quotes=0 … closed=1 rc=0` on an empty tree **and at the round-41 negative control** | glob/read-failure defaults to pass (R30 violation) |
| F2 | K14 | records byte-identical to base, only the exported r42 engine doctored → `closed=1` while the true ledger is 34 | limb trusts the graded tree's own yardstick |
| F3 | K19 | a record future-dated 65 min after its own commit → `closed=1`; at base it reds only because `.ufo/waves/round-43` is absent | cannot see the RD42-6 mechanism |
| F4 | seam | `selftest case=K18 positive=pass mutants=0/0 verdict=pass` | zero-mutant selftest line passes |
| F5 | K16 | `check_k16` with no argument reads `"."`; from a corrected cwd tree it prints `closed=1` | latent working-tree read |
| F6 | K8 | base `source=canonical`, `payload-match=18/18`, `closed=1` | 1 of the 13 base-closed checks is self-synthesized |

## Evidence inputs (read-only)

Exports built with `git -C <lane> archive <ref> | tar -x -C <scratch>` (152 MB each), outside the lane.
Draft instrument `r43-closure.sh` sha256 `d601d7e8d01c61d63792a2aff4958989cc04275d2d5c63290c8b62c245009a81`
(self-contained: engine inlined at lines 139-2330), `engine.py` sha256
`a5ef2d0d2afefe46a2471feaaffa84c8e12a80ef5e39f27a31da622045634355`.

Limb deliverables under grade (w1 digests at read time):

```
4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c  ExecK14Corrections.sh
14a195b1eb7ec61550bf4938f62ae7856dbae0c1a49dc7aba078f7b97304e93a  ExecK15WaveNarrative.sh
d7c33c9efdcfb5ab0feeac494da6a12d83d95d9b0d2d20b2bd121ba7af5a74cb  ExecK16Placeholder.sh
37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348  ExecK17ClaimsBefore.sh
8b797e424d5d3f35da0897fb36e7b3c294f3aa7f445e9313163e4170f0cfd029  ExecK18Transcript.sh
8e6b124feb975469e0837de4a3998ccf6a940543a19bfae93b9ec73d5165d7f2  ExecK19Freeze.sh
```

## Base figure, measured

Draft suite at base, `bash r43-closure.sh --export-ref ab98fac9… --work <scratch>/w-base`:

```
suite-sha256=none
run-utc=2026-10-28T16:27:52Z
K1 payload=records=1,blocks=3,graded=1,evidence=3,missing=0,wrong-grade=0,per-record=SCORECARD.md=3/3;LOG.md=0;SHONEN.md=0,union=0,replay=RevC1Counters.md=rejected closed=1
K2 … closed=1   K3 … closed=1   K4 … closed=1   K5 … closed=1   K6 … closed=1   K7 … closed=1
K8 payload=receipt=(canonical),source=canonical,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=18/18,forged=6/6 closed=1
K9 … closed=1   K10 … closed=1   K11 payload=corrections=34,groups=4,… closed=1   K12 … closed=1   K13 … closed=1
K14 payload=stub closed=0
K15 payload=stub closed=0
K16 payload=stub closed=0
K17 payload=stub closed=0
K18 payload=stub closed=0
K19 payload=stub closed=0
closed=13/19 exit=1
```

Plain run: exit 2 (`r43-closure: a plain run is refused (export mode only)`). Unresolvable ref:
`ERROR ref-not-found ref=deadbeef… closed=0 exit=1`, exit 1. Both match the frozen claim.

Note that the 13/19 was produced **with the six stubs**. Substituting the landed limbs must be
re-measured; the per-limb runs below predict it stays 13/19, because every limb is open at base.

## Per-limb matrix (payload line + real exit status)

```
K14 base  rc=1  K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
K15 base  rc=1  K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
K16 base  rc=1  payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
K17 base  rc=1  K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
K18 base  rc=1  K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
K19 base  rc=1  K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
```

Every limb is open at base. The four degenerate mechanics named in the seat spec, tested limb by limb:

| probe | K14 | K15 | K16 | K17 | K18 | K19 |
|-------|-----|-----|-----|-----|-----|-----|
| empty tree / absent target treated as pass | red (`engine-unreadable`) | red (`sentences=0`) | red (`sections=0`) | red (`claims=0,parse=1`) | **GREEN (F1)** | red (`freeze=absent`) |
| glob matches nothing | n/a (no glob; missing records → red) | red (`receipt_count` 0 → absent) | red (`promises=0` guard) | red (`claims=0`) | **GREEN (F1)** | n/a |
| parse failure defaults to closed=1 | red (compile/exec failure → `engine-unreadable`) | red (`json` error → `corrupt` → mismatch) | red (`promises=0`) | red (`parse=1`) | **GREEN (F1)** — an unreadable record is simply skipped | red (record `None` → `order=bad`) |
| reads the working tree instead of the export | no (cwd=lane, tree=base → same red) | no | **latent (F5)**: defaults to `"."` | no | no | no |

K14's defect line names the exact base literal: `K14 stale=SCORECARD.md:1634 corrections=33 live=34`.
K17's names the exact RD42-8 binding: `K17 detail round=round-42 claim=C1 field=before
token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12
result=unbacked`.

## F1 — K18 awards `closed=1` when it read nothing (R30 violation)

`ExecK18Transcript.sh:228`:

```python
closed = 1 if ucount == 0 else 0
```

There is no `quotes > 0` term. Every sibling has the positive-population guard (K15 `sentences_total==0`
→ closed=0; K16 `sections>0 and promises>0`; K17 `claims>0, tokens>0`; K19 absent → red). K18 is the
outlier, so a failed or empty read is a pass.

Counterexample 1 — empty tree:

```
$ check_k18 /fast/scratch/hyaku/kasegi-r43/CritBaselineEscape/empty
K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=1
rc=0
```

Counterexample 2 — a root with no round-42/43 records at all (only `SCORECARD.md`):

```
$ check_k18 /fast/scratch/hyaku/kasegi-r43/CritBaselineEscape/min
K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=1
rc=0
```

Counterexample 3 — **the mandatory round-41 negative control** (pre-dates round 42, so its record
population is empty):

```
$ check_k18 <export of 1f7464612ac4c44e39886b82e812610d3c039b13>
K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=1
rc=0
```

The r41 head export has `.ufo/waves/{round-38,round-39,round-40,round-41}` and zero round-42/43
lessons, so K18 closes there vacuously. The overall r41 control still prints closed<19/19 (K14, K16,
K19 are red there), so the kill rule is not broken — but K18 must not be cited as part of that red,
and a recordless export is exactly the shape a future mutant/fixture will have.

At base the same formula is red only because the base carries 22 quotes
(`quotes=22,bound=19,unbound=3`), so base-red itself is intact.

Impacted axes: `depth:verifiability`.

Smallest safe correction: `closed = 1 if (quotes > 0 and ucount == 0) else 0`, plus a selftest mutant
that empties the record population and must be rejected. One condition, no grammar change.

## F2 — K14 derives its "live" ledger from the graded tree's own r42 engine

`ExecK14Corrections.sh:142` (`payload, ok = ns["check_j11"](TREE)`) executes the engine embedded in
`<export>/corpus/instruments/r42-closure.sh`; `ok` is bound once and never used, and the `live=` value
is whatever that embedded function returns. The records are scanned by K14 itself, but the yardstick
they are compared to is supplied by the tree under grade.

Counterexample: copy the base export, change **only** the exported r42 engine (early return
`corrections=33,groups=4` in `check_j11`), leave `SCORECARD.md`, `LOG.md`, `SHONEN.md` byte-identical:

```
$ check_k14 <tamper>            # records identical to base (diff -q clean)
K14 payload=literals=2,stale=0,superseded=0,live=corrections=33,groups=4 closed=1
rc=0

original engine on tamper tree: corrections=34,groups=4,…
tampered engine on tamper tree: corrections=33,groups=4,…
records identical between base and tamper? records-identical
```

So a tree can report RD42-1 repaired (no `Correction (round 43)` appended, ledger still 34) by editing
the instrument it ships. That is the round's own design lesson inverted: the counter is supplied by the
record. Nothing else in the suite hashes or cross-checks `corpus/instruments/r42-closure.sh`; K11 in
the same run derives `corrections=34` from raw records, so the run would carry a visible contradiction
(`K11 payload=corrections=34` next to `K14 … live=corrections=33`).

Impacted axes: `depth:verifiability`.

Smallest safe correction: cross-check. After parsing `live`, require it to equal the K11 count the same
run derived (pass the engine's `check_k11` payload into the K14 slot; the r43 engine already contains
that code and K11's own selftest grades it), and require the embedded call's `ok` to be true. Two
conditions, no change to the literal grammar.

## F3 — K19's base red is an absence-red; the RD42-6 mechanism is not graded

`ExecK19Freeze.sh` reads only `.ufo/waves/round-43/{claims.json,freeze.txt}` and the two control
receipts those name. Its relations are (a) freeze label == claims label, (b) label ≥ latest control
`measured-at=`, (c) record states the real max and the claims base, (d) sha256 of the claims bytes.
It never compares the label with the instant of the commit that carries it.

Counterexample: a round-43-shaped record whose `frozen_at_utc` is the r42 defect value `12:05:00Z`
(the commit that carried that value, `0566bd6`, is `2026-10-28T11:00:01Z` — 65 minutes **earlier**),
with a matching freeze record and controls measured at 10:50/11:00:

```
$ check_k19 <base + that record>
K19 payload=freeze=present,order=ok,sha=match closed=1
rc=0
reference: 0566bd6 2026-10-28T08:00:01-03:00  (= 11:00:01Z)
```

K19 accepts it. Two consequences:

1. **At base, K19 is red for absence, not for its defect.** Every other new limb sees its own committed
   defect in bytes that exist at base (K14 `stale=…:1634`, K15 `unbacked=3`, K16 `unresolved=1`,
   K17 `unbacked=1`, K18 `unbound=3`). K19 sees nothing; `.ufo/waves/round-43` does not exist at base.
   The frozen predicate's own parenthetical — "at base every one of K14-K19 is open (each new check
   must see its own committed defect at base)" — is therefore not met by K19 in the only sense that
   matters: the defect it names is the r42 future-dated label, and K19 does not read the r42 record.
2. **A future-dated round-43 record would pass at Y**, so the repair cannot distinguish an honest
   freeze from a fabricated one — the specific RD42-6 class.

This is a claim-scope gap rather than a limb-versus-text bug: the frozen K19 sentence defines exactly
the narrower relation the limb implements. Two honest resolutions, both cheap:

- Strengthen: the suite already resolves the export ref and has the lane; supply the commit instant
  (read-only `git show -s --format=%ct`, and for prior rounds
  `git log --diff-filter=A -1 --format=%ct -- .ufo/waves/round-NN/claims.json`), require
  `frozen_at_utc <= instant`, and grade every committed `claims.json` whose freeze record or receipt is
  present. At base the r42 record (12:05Z vs 11:00:01Z) then reds K19 for its defect.
- Or record the narrowing in `claims-erratum-1.md` and drop the "sees its own defect" claim for K19.

Do not leave both the parenthetical and the narrow limb unremarked: that is the internal contradiction
a later verifier will grade.

Impacted axes: `depth:verifiability`.

## F4 — the selftest seam awards `verdict=pass` with zero mutants

`engine.py:2063`:

```python
verdict = "pass" if (res["positive"] and pm == 1
                     and (total == 0 or good == total)) else "fail"
```

and `engine.py:1693`: `limb_mutants(...)` returns `(0, 0)` for every limb slot. Executed against the
draft engine's own `selftest_line`:

```
zero mutants built (the seam's current limb_mutants):
  selftest case=K18 positive=pass mutants=0/0 verdict=pass
one mutant built and ACCEPTED (the defect this must catch):
  selftest case=K18 positive=pass mutants=0/1 verdict=fail
one mutant built and rejected:
  selftest case=K18 positive=pass mutants=1/1 verdict=pass
```

So once a limb returns open-at-base and closed-at-Y, its selftest line reads `verdict=pass` with
`mutants=0/0` — nineteen graded lines, six of them with no mutation evidence. The frozen kill rule
only names a "summary-only line", so 0/0 can pass unnoticed. This matters especially for F1: K18's
mutant battery must contain the empty-scope mutant, and the seam must refuse zero cases.

Impacted axes: `depth:verifiability`.

Smallest safe correction: for `check_id in LIMB_SLOTS`, require `total >= 1` in the verdict expression
(e.g. `(total >= 1 and good == total)`); implement `limb_mutants` for K14-K19 as part of the same
substitution that replaces each stub. Without the floor the substitution can land vacuously.

## F5 — K16 defaults its root to `"."` (latent working-tree read)

`ExecK16Placeholder.sh:51`: `local root="${1:-.}"`. Every other limb refuses or reds when called with
no argument (K14/K17/K18/K19 no-arg → `closed=0`, K15 no-arg → rc 2). K16 scans the caller's cwd:

```
$ check_k16                                  # cwd = corrected tree
payload=sections=491,promises=1,fenced=0,unresolved=0 closed=1
rc=0
$ check_k16 <base export>
payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
```

With the correction appended in cwd, a no-argument call greens; with the base export it reds. This is
live only if the assembled suite mis-wires the slot (the draft stub passes `EXPORT`, so it is not live
today), but it is exactly the "reads the working tree instead of the export" class the claim forbids,
and the suite is normally invoked from the lane root.

Impacted axes: `depth:verifiability`.

Smallest safe correction: `local root="${1:-}"` plus the existing `root-not-found` red, matching K19's
argument discipline.

## F6 — observation on the base 13/19 (not a defect claim)

Base `K8` is closed through `source=canonical` (`engine.py:1491ff`): with no `.ufo/waves/round-43`
receipt in the export, the check synthesizes a receipt from the run's own payload lines and grades that
(`payload-match=18/18`, `forged=6/6`, `derived == closed`). It cannot fail for its own defect at base
by construction. This is what makes the frozen base figure `closed=13/19` reachable while the r42
stand-in printed `12/13` (its receipt existed and was stale). It is acceptable for the base-red
purpose — K1-K13 are carried checks and the claim requires them closed at base — but "13/19 at base"
should not be read as thirteen independently evidenced checks: one of them is a self-referential
probe, and the substantive base-red evidence is K14-K19.

`run-utc` is the ref's commit instant (`utc = ref_utc(REF)`), not wall clock, so the base transcript
is reproducible and K8's `utc` fact passes. That is consistent with the claim's `time-basis=ref-commit`.

## What the round gets right (for balance)

- K15 masks inline-code for the `dispatched` predicate but parses wave names from raw text, so a
  backticked wave name still counts; it reds at base on `LOG.md:1804` and `round-42.md:11,:16`, and a
  lesson-only correction leaves the LOG claim unbacked (`unbacked=1` on my corrected tree), so
  supersession is per-file rather than blanket.
- K16 requires `sections>0 and promises>0`, so erasing the promise cannot close it; it reds on the base
  `## Wave-2 falsification` stanza and greens only when a `Correction (round 43)` names the heading after it.
- K17 defines a population over every round's `claims.json`, so its base red is a real binding failure
  (`closed=10/12` quoted against a control that prints `closed=8/12`), not an absence.
- K19 rejects absent, corrupt, truncated, wrong-digest and out-of-order records (11/11 probes red in my
  battery), and reads only under its export root (`inside()` containment); cwd poisoning had no effect.

## Scratch and tooling

Scratch `S=/fast/scratch/hyaku/kasegi-r43/CritBaselineEscape` (exports, tamper tree, probes) was
removed before yield. No tool installs, no network fetches, no pacman, no mutating git, no writes
outside this receipt and `$S`. Disk guard read before the heavy pass: `/fast/scratch/hyaku 25% use,
605.8G free`.
