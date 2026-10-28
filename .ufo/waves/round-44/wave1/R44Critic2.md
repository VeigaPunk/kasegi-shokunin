# R44Critic2 — falsifying the C1 fix approach for the unbacked `closed=13/19` narrative

- seat: `R44Critic2`, critic (leaf, read-only)
- item: **Try to falsify C1 fix approach for the unbacked 13/19 narrative, using only committed evidence.**
- revisions read: lane HEAD `66314015122b9aa32dc40f2f1815df56624c26d1`; round-44 frozen base `5ab3a60`; the defect's own base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
- frozen inputs read first: `.ufo/waves/round-44/claims.json`, `.ufo/waves/round-44/controls/do-nothing.txt`, `corpus/lessons/round-43-verifier-spotcheck.md` §6.
- scope discipline: no git/jj/index mutation, no commit/push, no production or shared-file edit; the only write in the lane is this report. Scratch `/fast/scratch/hyaku/kasegi-r44/R44Critic2/` (removed on exit; see Limitations). No tool installed, so nothing to report under the tooling directive.

Method: committed bytes only (`git show`, `git grep`, `git ls-tree`, `sed`, `sha256sum`) plus three read-only executions against `git archive` exports in scratch: limb K17 and limb K18 at the frozen base, and one run of the committed suite `corpus/instruments/r43-closure.sh` at `ab98fac9`. The suite run writes only under my `--work`/`--scratch-root`.

## Verdict — the prescribed fix is falsified in two of its three components and inert in the third

The prescription under attack (spotcheck §6.1 + §6.2): *"Append a `Correction (round 43)` naming the literal superseded by the per-limb base result (six per-limb transcripts, all red), **or** commit a base run of the landed suite"*, and *"Close it by adding the missing erratum paragraph (K17's existing escape then covers it)"*.

1. **Base-run branch: falsified.** The landed suite at `ab98fac9` prints `closed=12/19 exit=1` with **K8 and K14–K19 open** — not `13/19` with "exactly K14-K19 open". A committed base run therefore *contradicts* the literal instead of backing it.
2. **K17-escape branch: falsified.** K17 grades `before` cells only; the literal lives in the `after` cell. K17 is green at the frozen base with the literal unbacked, and no erratum can change that.
3. **K18 escape: already spent, and not fail-closed.** At the frozen base `closed=13/19` is *already* in K18's superseded set, and its only marker is the defect's own prescription line. Adding the erratum paragraph flips no verdict — so it yields no red-before control and cannot distinguish a correction from a mention.

Net: defect 1 can be *closed by prose* under the frozen C1 after-state, and the record would still assert a superseding value (`13/19` minus six) that the landed instrument refutes (`12/19`). That is the false-provenance risk this item exists to find.

## F1 — the landed suite at the defect's base prints `12/19`, not `13/19`

Seat run (scratch, read-only w.r.t. the lane), suite digest pinned to the committed one:

```
$ bash corpus/instruments/r43-closure.sh \
    --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --work $S/base-run/work --scratch-root $S/base-run/scratch
K8 payload=receipt=.ufo/waves/round-43/final-gates/all-gates.txt,source=absent,header=0,ref=0,digest=0,time-basis=0,utc=0,one-run=0,payload-match=0/0,forged=0/0,selftest-lines=0,summary=0,closed-line=0 closed=0
K14 payload=limb=absent,file=k14-corrections.sh closed=0
K15 payload=limb=absent,file=k15-wave-narrative.sh closed=0
K16 payload=limb=absent,file=k16-placeholder.sh closed=0
K17 payload=limb=absent,file=k17-claims-before.sh closed=0
K18 payload=limb=absent,file=k18-transcript.sh closed=0
K19 payload=limb=absent,file=k19-freeze.sh closed=0
closed=12/19 exit=1          (rc=1, 157 s)
```

The instrument is byte-identical to the committed suite: `sha256sum` of `corpus/instruments/r43-closure.sh` at HEAD = `a832908e15f49de89066d8168a833d3ffa0f5fad432ba1c2b5a813ba45bef168`, the same digest the spotcheck binds to `all-gates.txt`/`all-gates.at-Y.txt`.

The same `12/19` is derivable from committed bytes alone, without my run:

| fact | committed evidence |
|---|---|
| K8 is open at base | `corpus/instruments/r43-closure.sh:50` `RECEIPT_REL=".ufo/waves/round-43/final-gates/all-gates.txt"`; `:145-147` absent branch prints `source=absent … closed=0`; the round-43 receipt does not exist at `ab98fac9` |
| K14–K19 are open at base | `r43-closure.sh:300` `f="$EXPORT/$LIMB_REL/${LIMB_FILE[$id]}"` — limbs are read from the **export**, and `corpus/instruments/r43-limbs/` does not exist at `ab98fac9` → `limb=absent closed=0` |
| K1–K7, K9–K13 are closed at base | carried r42 run over the base export: `.ufo/waves/round-43/c1-controls/do-nothing.txt` §B `closed=12/13 exit=1` with only `J8 … closed=0` |

So 12 closed + 7 open (`K8`, `K14`–`K19`). The frozen literal (`.ufo/waves/round-43/claims.json:41`, and `SCORECARD.md:1685`) says `closed=13/19 exit=1 with exactly K14-K19 open` — off by one closed check and by one open check.

Where `13/19` actually came from, in committed bytes: the **draft carry harness**, not the landed suite — `.ufo/waves/round-43/w1/ExecCarryChecks.transcript.txt:58,113` (`K8 payload=receipt=(canonical),source=canonical,…,closed=1` — K8 closed against a receipt it synthesised) and `:70` of `.ufo/waves/round-43/w1/CritBaselineEscape.md` ("the 13/19 was produced **with the six stubs**"). `ExecNegCtlReceipt.md:52` already states the landed reading: *"at base there is no r43 receipt, so K8 is open at base. With the six new checks also open, the base figure is 12/19, not the frozen 'exactly K14-K19 open'."*

## F2 — "K17's existing escape then covers it" is false: the literal is not in K17's population

`corpus/instruments/r43-limbs/k17-claims-before.sh:326` `if field == "after": continue` — after cells are skipped *before* the erratum lookup, and `superseded_by()` is reached only for `before` tokens that a cited receipt fails to print. The literal is in the `after` cell (`claims.json:41`). Empirical confirmation at the frozen base:

```
$ bash corpus/instruments/r43-limbs/k17-claims-before.sh --tree <export 5ab3a60> --work $S/k17b
K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1     (rc=0)
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 by=claims-erratum-5.md result=superseded
K17 detail round=round-43 claim=C1 field=before token=closed=10/13 record=.ufo/waves/round-42/claims-erratum-4.md result=quoted
K17 detail round=round-43 claim=C1 field=before token=closed=10/12 record=claims.json result=quoted
```

K17 is **green** while `closed=13/19` sits unbacked in the same claims file. An erratum paragraph naming `13/19` is never consulted for it, so §6.2's mechanism cannot produce the "red-before control" C1's after-state requires.

## F3 — the K18 escape is already satisfied by the defect description itself

```
$ python3 $S/k18-account.py <export 5ab3a60>      # replica of K18's marker/token rules, read-only
marker files=11
SUPERSEDED closed=13/19                 by corpus/lessons/round-43-verifier-spotcheck.md:101
...
corpus/lessons/round-43-verifier-spotcheck.md:47  token=closed=13/19 classification=superseded
corpus/lessons/round-43-verifier-spotcheck.md:94  token=closed=13/19 classification=superseded
corpus/lessons/round-43-verifier-spotcheck.md:101 token=closed=13/19 classification=superseded
```

`spotcheck.md:101` is the **defect entry** — `1. **closed=13/19 is unbacked (highest priority).** … Append a Correction (round 43) naming the literal superseded …`. It contains both `closed=13/19` and the literal string `Correction (round 43)`, so K18's line-level marker (`k18-transcript.sh`, `if "Correction (round 43)" not in line: continue`) admits it as a supersede source. K18's supersede set is global by token, so every `13/19` in its record surface counts as superseded today.

Consequence: no erratum paragraph can move K18, and K18 cannot tell a real correction from a sentence that merely prescribes one. The escape is not fail-closed — this is precisely the mutant shape a sibling seat is asked to design, and it already fires at the frozen base.

Bound-by-nothing check: no summary-shaped `^closed=13/19 exit=` line exists in any K18 evidence dir (`.ufo/waves/round-42`, `round-43/final-gates`, `round-43/c1-controls`); the six hits are all under `.ufo/waves/round-43/w1/`, which K18 excludes as "claims, not evidence". No committed `^closed=12/19` line exists either (`git grep -n '^closed=12/19' HEAD | wc -l` → `0`).

## F4 — the two authoritative loci of the literal are in no instrument's population, and the defect text mislocates one

| locus (HEAD) | graded by | observed |
|---|---|---|
| `.ufo/waves/round-43/claims.json:41` — C1 **`after`** | nothing: K17 skips `after` (`k17:326`), K18 does not read `claims.json` | K17 green (F2) |
| `SCORECARD.md:1685` — round-43 move-log row, `4 held — **expected** (… base ab98fac9 closed=13/19 exit=1 with exactly K14-K19 open …)` | nothing: K18 excludes `SCORECARD.md` as a quote source; K14 grades `corrections=` only (`r43-closure.sh` references SCORECARD only for the K14 case) | — |

And the defect text itself is wrong about the cell: `spotcheck.md:101` says *"`.ufo/waves/round-43/claims.json` C1 **`before`** state the base export prints `closed=13/19`"*, but the committed `before` cell reads `closed=12/13` (the r42 stand-in), and `13/19` is in `after`. A fix drafted from that sentence targets a cell that does not contain the token; a counter written to that sentence's wording (grading `before` cells) reproduces K17's blind spot.

## F5 — adjacent state defect, outside the frozen eight: K18 is red at the frozen base

```
$ bash corpus/instruments/r43-limbs/k18-transcript.sh <export 5ab3a60> --verbose
K18 payload=quotes=68,bound=52,report-only=1,superseded=14,unbound=1 closed=0      (rc=1)
K18 unbound token=selftest cases=10 failures=9 at corpus/lessons/round-43-verifier-spotcheck.md:61
```

`spotcheck.md:61` quotes the C2 red-before `selftest cases=10 failures=9` with no `report-only` and no binding summary line. This is not one of §6's eight, but it means the round-44 base is not gate-green: "the erratum closes it" cannot be demonstrated by a suite run at the head, and the r44 counter must carry the proof alone. Reported as state, not as a ninth routed defect.

## F6 — adjacent: C1's frozen counter and control paths do not exist at the frozen base

```
$ git cat-file -e HEAD:corpus/instruments/r44-routed-defects.py   → ABSENT
$ git ls-tree -r --name-only HEAD .ufo/waves/round-44/controls/   → .ufo/waves/round-44/controls/do-nothing.txt
```

`.ufo/waves/round-44/claims.json:14-15` cite `python3 corpus/instruments/r44-routed-defects.py --root <lane-export> --baseline <frozen-base>` and `.ufo/waves/round-44/controls/c1-do-nothing.txt`; both are absent at freeze. The C1 after-state's only grader is therefore **unspecified at freeze** — which is what lets a prose-only correction pass (F2/F3) and what makes "proven by one committed read-only counter" unfalsifiable until the counter lands.

## Impacted axes

- `depth:verifiability` (C1): harmed if the fix is landed as prescribed. No gate changes, so "at least one red-before control per changed gate" is vacuous; the after-state's "0 of those same 8 … proven by one committed read-only counter" reduces to "a correction paragraph exists", while the correction's own superseding value can be wrong (F1).
- `coverage` (C2): no impact found; nothing here touches frontier, registry, knowledge or the census.
- No other axis is touched by this item.

## Smallest safe correction

1. **Correction text:** name the measured value, not the arithmetic. `closed=13/19` is superseded by `closed=12/19 exit=1` with open set `K8, K14-K19` (K8's r43 receipt absent at base; the six limbs absent from the base tree), produced by `corpus/instruments/r43-closure.sh` (sha256 `a832908e…`) at `export-ref=ab98fac9…`. Withdraw "exactly K14-K19 open" explicitly — it is wrong by one open check.
2. **Counter predicate (defect 1):** require all three, not prose alone — (a) a correction block naming `closed=13/19` as superseded; (b) the asserted superseding token equal to the `^closed=` summary line of a committed base-run receipt; (c) that receipt's `suite-sha256` equal to the landed suite digest and its `export-ref` equal to the frozen base. A predicate that greps for `13/19` next to the word "superseded" is satisfied by the defect description today (F3).
3. **Base-run admissibility:** the suite accepts `--receipt` (`r43-closure.sh:68`, `RECEIPT_OVERRIDE`), `--only` and `--leaf`. A base run that reproduces `13/19` is reachable only by handing K8 a synthesised receipt (the port-C branch documented at `RevC1Freeze.md:118-146`) — that would be a fabricated backing. The receipt must record the flags, and the counter must reject `--receipt`/`--only`/`--leaf` runs.
4. **Do not claim K17's escape.** If a gate is to change, say which: K18's marker should be a *correction block*, not "any line containing `Correction (round 43)`" — but that is a widening and must be declared, with a mutant proving the prescription sentence no longer satisfies it.

## Do-nothing discrimination

- Do-nothing at `ab98fac9`/`5ab3a60`: no correction, no counter, and the landed suite prints `12/19` — so neither "defect 1 resolved" nor the frozen `13/19` after-state is reachable. C1's kill rule ("a do-nothing replay can report all 8 fixed") is not accidentally fired.
- But the frozen after-state is also not reachable by the *prescribed* fix alone: it is reachable by any paragraph that mentions the token. That asymmetry is the finding.

## Limitations

- The `ab98fac9` run is a **seat run, not committed** (157 s, rc=1). Its output lived only in scratch and is deleted on exit; the committed-byte derivation in F1's table yields the same `12/19` independently, so the finding does not rest on my run.
- I did not run the suite at HEAD, and the eventual `r44-routed-defects.py` does not exist to test; F6 is a statement about the frozen state, not a prediction about the implementation.
- The per-limb base transcripts (`ExecK14Corrections.transcript.txt` etc.) were read, not re-executed; they show K14–K19 red at base under their own drivers, which is consistent with — not identical to — the suite's `limb=absent` at base.
- No live HTTP re-open; no git/jj mutation; no tool installation; no subagent dispatch.
