# RevK18 — reviewer, K18 (RD42-5) attack pass

Seat: `RevK18` (reviewer, r43 wave 1, leaf). Lane `kasegi-shokunin`; base
`ab98fac9dce87130bc4f66de89e30650d63943dc`; claims read from
`.ufo/waves/round-43/claims.json` (never edited). Target: `ExecK18Transcript`
(executor seat), deliverables under `.ufo/waves/round-43/w1/`. This seat is
receipt-only; no landable bytes, no lane edits beyond this receipt, no mutation
of any git object.

Claim under test, frozen: "K18 every `closed=`/`selftest cases=` value quoted
in round-42/43 lane records appears in a committed transcript under the round's
`final-gates/` or `c1-controls/`, or its line carries `report-only`, or it is
named superseded by a `Correction (round 43)`/claims-erratum line."

## 0. Bytes under test (the limb moved twice while this seat probed)

The executor revised `ExecK18Transcript.sh` three times. Every number below was
re-executed from scratch on the bytes named:

| sha256 | lines | when | note |
|---|---|---|---|
| `8b797e42…0cfd029` | 260 | first landed read | header coupling still present |
| `243b562d…977801` | 270 | executor message "limb is landed"; receipt/transcript cite this | r43 `w1/` receipts could bind |
| **`3551a0fc…495a89e`** | **278** | **current, mtime 2026-10-28 13:59:49 -0300** | all results below unless marked otherwise |

All fixtures were minimal `git archive`-style trees under
`/fast/scratch/hyaku/kasegi-r43/RevK18/fx/`, sourced with
`. ExecK18Transcript.sh` and run as `check_k18 <tree>`; the limb reads only
files under the export root it is handed. Nothing was written to the lane.

Snapshot warning, 2026-10-28T17:01Z: the limb is `3551a0fc` (278 lines) while
the executor's own receipt (`.ufo/waves/round-43/w1/ExecK18Transcript.md`,
13:58) and transcript (`.…transcript.txt`, 13:57) still cite `243b562d`
(270 lines). If they land as-is, the executor receipt's hash table is stale
against the bytes it describes. The executor was still regenerating them when
this seat stopped; the L1 should confirm the final hash table before landing.

## 1. Verdict

Four of the five assigned attack vectors behave correctly in `3551a0fc`;
**one does not**: the anti-example exemption can swallow a summary-shaped
`closed=` claim when the same token appears earlier on the same line
(D1, false green). Two further claim-vs-implementation divergences are
material: the binding-evidence surface is wider than the frozen location
(D2; under the frozen four directories K18 cannot close at Y), and the tee
deliverable is the suite's two-mode `--receipt-out` receipt, not a plain
stdout tee (D3). The frozen predicate also does not authorize the two extra
exemptions the limb applies (D4).

| attack | file | expected | observed (`3551a0fc`) | verdict |
|---|---|---|---|---|
| 1 trailing punctuation | `fx/f1`, `fx/f1b` | extract, no escape | green; transcript-side punctuation red | pass (safe direction) |
| 2 fenced transcript in a lesson | `fx/f2a`, `fx/f2b` | record's own fence red | red; non-record copy was green on `243b562d`, red now | pass now; was a defect |
| 3 different denominator | `fx/f3`, `fx/f3b`, `y_exec_denom` | unbound | red (`unbound=1/1/2`) | pass |
| 4 report-only blanket / no-value line | `fx/f4a`,`f4b`,`f4c` | line-scoped only | `r=0` on no-value line; blanket line red; own line green | pass |
| 5 round-42 verifier file | real base, `t_noverif` | in scope (glob) | 22 vs 4 quotes; verifier is a lane record | pass |
| extra: repeated-token anti-example | `fx/f7`,`f7b`,`f7c` | unbound state claim red | **quotes=0 closed=1** | **FAIL (D1)** |

## 2. Attack 1 — a value with trailing punctuation

Two directions matter: punctuation after the *quoted* token must not defeat
extraction, and punctuation on the *transcript* summary line. Fixtures:
`f1` = a record line ``the run prints `closed=13/13.` at Y`` plus a real
`closed=13/13 exit=0` transcript; `f1b` = a record quoting `closed=16/19`
with the only transcript line `closed=16/19.` (period, no `exit=`).

```
$ . ExecK18Transcript.sh; check_k18 fx/f1
K18 payload=quotes=1,bound=1,report-only=0,superseded=0,unbound=0 closed=1
rc=0
$ check_k18 fx/f1b
K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
rc=1
```

The extraction regex is `(?<![0-9/])closed=(\d+)/(\d+)(?![0-9/])`
(`ExecK18Transcript.sh:69`): a trailing `.` is neither digit nor slash, so
the token is extracted whole and the punctuated quote is graded. The
executor's own probe agrees: `closed=11/12,` / `selftest cases=7 failures=1.`
are extracted, and with no transcript they are `unbound=2 closed=0`
(`ExecK18Transcript.transcript.txt` §5). A period *inside* the transcript
summary line cannot bind, because binding requires the anchored line
`^closed=<n>/<m> exit=<k>$` (`:71`); that is a false-red direction only and
matches the frozen "whole token" reading, so this attack does not escape.
No finding.

## 3. Attack 2 — a value inside a fenced transcript quoted in a lesson

`f2a`: the lesson record itself contains a fenced block with
`closed=17/19 exit=0`, no transcript anywhere.

```
$ check_k18 fx/f2a
K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
rc=1
```

Correct: the record is in `record_set` and is never read as a transcript, so a
lesson cannot certify its own fenced copy. The executor's §6 probe is the same
shape and red.

`f2b` is the sharper version of the RD42-5 class: the *lesson* quotes
`closed=17/19 exit=0` in prose, and the only "transcript" is a fenced copy in
`.ufo/waves/round-43/w1/copy.md` — a seat receipt, not a gate transcript.
On the `243b562d` bytes this bound the quote:

```
$ check_k18 fx/f2b            # 243b562d
K18 payload=quotes=1,bound=1,report-only=0,superseded=0,unbound=0 closed=1
rc=0
```

On the current `3551a0fc` bytes the evidence surface excludes this round's
`w1/` receipts (`EVIDENCE_DIRS`, `ExecK18Transcript.sh:126-129`), and the
fixture now reds:

```
$ check_k18 fx/f2b            # 3551a0fc
K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
rc=1
```

So this specific escape was fixed between revisions. The frozen-location
residue that remains is D2.

## 4. Attack 3 — a transcript that contains the token with a different denominator

`f3`: quote `closed=10/13`, transcript line `closed=10/14 exit=1`.
`f3b`: quote `closed=16/19`, transcript line `closed=16/190 exit=1`
(the substring hazard behind M42-2). `y_exec_denom`: the real Y tree with the
landed tee edited from `closed=10/13` to `closed=10/14`.

```
$ check_k18 fx/f3
K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
$ check_k18 fx/f3b
K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
$ check_k18 y_exec_denom 1
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:177
K18 scope records=2 transcripts=162
K18 payload=quotes=22,bound=20,report-only=0,superseded=0,unbound=2 closed=0
```

All red. Binding is a set of full summary-line tokens
(`SUM_CLOSED_LINE`, `:71`; `SUM_TEST_LINE`, `:72`), never a prefix or
substring. Pass. The executor's `10/100` / `failures=30` probe is the same
result.

## 5. Attack 4 — `report-only` as a blanket escape on a line with no value

`f4a`: a record line carrying `report-only` and **no** token.
`f4b`: a file-level sentence "All tallies in this file are report-only." on
line 1, an unbacked `closed=7/19` on line 2.
`f4c`: the unbacked `closed=7/19` and `report-only` on the *same* line.

```
$ check_k18 fx/f4a
K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=1
$ check_k18 fx/f4b
K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
$ check_k18 fx/f4c
K18 payload=quotes=1,bound=0,report-only=1,superseded=0,unbound=0 closed=1
```

Correct in all three: the exemption is tested per token on the quoting line
(`elif "report-only" in line`, `:238`), a value-less line adds nothing to
`report-only=`, and no file-level blanket applies. Pass.

## 6. Attack 5 — a value in the round-42 verifier file (is that a lane record?)

Yes. `corpus/lessons/round-42-verifier-spotcheck.md` is a committed lane record
under `corpus/lessons/`, authored by the round-42 verifier spot-check, and it
matches the frozen scope glob `corpus/lessons/round-42*.md` literally
(`SURFACE_PREFIXES`, `ExecK18Transcript.sh:77`; `fnmatch`, `:108`).

What the limb does: it grades that file. At base it contributes 18 of the
22 graded quotes (the file has 31 raw token occurrences: 13 distinct values
plus repeats); deleting only that file drops the run from 22 quotes to 4 and
to green.

```
$ check_k18 base 1
K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=selftest cases=13 failures=3 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:177
K18 scope records=2 transcripts=160
rc=1
$ check_k18 base-without-verifier-file
K18 payload=quotes=4,bound=4,report-only=0,superseded=0,unbound=0 closed=1
rc=0
```

Consequence for the executor's required base transcript: `round-42.md` at base
quotes only eight raw tokens — `closed=13/13` ×2, `closed=8/12`,
`selftest cases=12 failures=8`, `selftest cases=13 failures=0`,
`closed=10/100` ×2 — and **no `closed=10/13`**. The base red that names
`closed=10/13` exists only in the verifier file. A limb that scanned only
`round-42.md` could not produce the executor's own required transcript line;
this limb correctly reads the glob and names `round-42-verifier-spotcheck.md:65`
and `:177`. The executor transcript's wording ("names `closed=10/13`", with the
path quoted) is accurate; it does not falsely say `round-42.md`. Pass, with the
record established: the verifier file is in scope.

## 7. Defect D1 (high) — the anti-example exemption swallows a repeated summary-shaped claim

Claim in the executor receipt: "Summary-shaped values are graded even on those
lines" and "it cannot hide a summary-shaped claim." That is false for a line
that mentions the same token earlier in a `mangled`/`substring` cell:
`summary_shaped()` and `cell_of()` both locate `line.find(tok)`, the **first**
occurrence (`ExecK18Transcript.sh:186`, `:198`), and the grade loop calls them
without the current match offset (`:231-234`). Every occurrence whose token
also appears earlier is therefore classified from the first occurrence.

`fx/f7` — one prose line, no transcript:

```
The mangled probe showed `closed=7/19` and the final state was `closed=7/19 exit=0`.
```

`fx/f7c` — the same shape as a markdown table row (the verifier's own format;
first cell `M99` is not an attack id, so no attack-row exemption):

```
| id | event | after |
|---|---|---|
| M99 | the mangled probe printed `closed=7/19` | the state claim is `closed=7/19 exit=0` |
```

```
$ check_k18 fx/f7 1
K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=1
rc=0
$ check_k18 fx/f7c 1
K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=1
rc=0
```

Expected: `quotes=1, unbound=1, closed=0` — the second, summary-shaped
occurrence is a state claim and has no transcript. The limb reports zero quotes
and green: the whole line is skipped because the first occurrence sits in the
"mangled" cell. `fx/f7b` ("substring … `closed=9/19`; the final state was
`closed=9/19 exit=1`") is identical: `quotes=0 … closed=1`.

Impact: any round-42/43 record line that pairs a mangled/substring mention with
a state-shaped claim of the same value is invisible. This is the exact class the
check exists to grade (a quoted tally with no committed transcript), and it is
a false green, not a false red. The frozen predicate has no such exemption at
all (D4), but even under the executor's own declared rule the summary-shaped
value should be graded. Fix: pass the `re.Match.start()` of each occurrence into
`summary_shaped`/`cell_of` (or iterate matches with `finditer` and test the
offset) instead of `line.find(tok)`.

## 8. Defect D2 (high) — evidence surface is wider than the frozen location

Frozen: a value must appear in a committed transcript "under the round's
`final-gates/` or `c1-controls/`" (seat prompt names four: r42/r43
`final-gates/` and `c1-controls/`). The limb's evidence stores are
`EVIDENCE_DIRS` (`ExecK18Transcript.sh:126-129`): **all** of
`.ufo/waves/round-42/` plus r43 `final-gates/` and `c1-controls/`. Round-42
`wave1/`, `wave2/`, result JSONs and seat receipts are therefore evidence.

This is not cosmetic: it is what makes the check close. Replacing
`EVIDENCE_DIRS` with the frozen four directories (a scratch copy of the
deliverable; no lane byte changed) gives:

```
$ check_k18 base                  # frozen dirs only
K18 payload=quotes=22,bound=14,report-only=0,superseded=0,unbound=8 closed=0
$ check_k18 y_exec 1              # frozen dirs only, landed tee present
K18 unbound token=closed=5/13 at corpus/lessons/round-42-verifier-spotcheck.md:52
K18 unbound token=closed=4/13 at corpus/lessons/round-42-verifier-spotcheck.md:53
K18 unbound token=closed=5/13 at corpus/lessons/round-42-verifier-spotcheck.md:227
K18 unbound token=closed=4/13 at corpus/lessons/round-42-verifier-spotcheck.md:228
K18 unbound token=closed=10/12 at corpus/lessons/round-42-verifier-spotcheck.md:298
K18 scope records=2 transcripts=6
K18 payload=quotes=22,bound=17,report-only=0,superseded=0,unbound=5 closed=0
```

So under the frozen location the after-state is unreachable: base is 8 unbound
and Y still has 5 (`closed=5/13` ×2, `closed=4/13` ×2, `closed=10/12`), none of
which the planned de09313 tee binds. The limb's base/Y numbers (`22/19/3` and
`22/22/0`) depend on non-gate round-42 files:

- `closed=5/13` and `closed=4/13`: only `.ufo/waves/round-42/wave1/ExecSuiteCore.transcripts.txt`.
- `closed=10/12`: `.ufo/waves/round-42/wave1/RevC1Counters.md` and `wave1/RevengerReceipt.md`.

The executor half-discloses this in receipt §"What the L1 must land" item 2
("w1 files bind but are not themselves quote sources") but does not state that
the frozen four-directory reading reds the after-state. Required action: either
(a) amend/erratum the frozen sentence to name the whole round-42 archive as the
evidence store (the round-42 bytes are frozen and cannot be re-authored this
round, which is a defensible reason), or (b) land those three values as
transcripts under a frozen gate directory (or name them in a `Correction
(round 43)`). Without one of these, K18's `closed=1` at Y is a claim the frozen
text does not license.

Note the separate, now-fixed, r43 half of D2: on `243b562d`, an r43 `w1/`
receipt was evidence and a fenced copy in `w1/copy.md` bound a lesson's quote
(`f2b`, `bound=1 closed=1`); `3551a0fc` excludes r43 `w1/` and reds it. That fix
is correct and should stay.

## 9. Defect D3 (medium) — the tee is a two-mode receipt, not one stdout tee; and a plain tee cannot close K18

Deliverable: `ExecK18Transcript.de09313-tee.txt`, 33 lines, sha256
`44a53379…d9b3`, landed at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`.
It is the suite's `--receipt-out` file: `all-gates v2` header + `export-ref=` +
`suite-sha256=` + `time-basis=` + `run-utc=`, J1-J13 run lines,
`closed=10/13 exit=1:` (line 19), the thirteen graded selftest lines and
`selftest cases=13 failures=3` (line 33). The executor's §10 provenance shows
`cat tee-run.txt tee-st.txt > tee.txt` and `cmp` identical to the suite's own
receipt for that ref. That is a composite of two modes, not
"tee stdout+stderr UNEDITED (no header, no edit)" as the seat prompt specifies.

This matters because the check needs **both** summary shapes, and neither
single-mode stdout carries both:

```
$ check_k18 y_plain        # plain-run tee only: closed=10/13 exit=1, no selftest summary
K18 payload=quotes=22,bound=21,report-only=0,superseded=0,unbound=1 closed=0
$ check_k18 y_self         # selftest tee only: selftest cases=13 failures=3, no closed summary
K18 payload=quotes=22,bound=20,report-only=0,superseded=0,unbound=2 closed=0
$ check_k18 y_both         # plain + selftest summaries (the delivered composite)
K18 payload=quotes=22,bound=22,report-only=0,superseded=0,unbound=0 closed=1
$ check_k18 y_exec         # same tree with the executor's actual tee
K18 payload=quotes=22,bound=22,report-only=0,superseded=0,unbound=0 closed=1
```

(`y_plain` here is my independent plain run of the ref's own bytes —
`closed=10/13 exit=1`, 144 s; `y_self` is my `--selftest` run of the same
bytes — `selftest cases=13 failures=3`, 179 s.)

Also confirmed independently: running the **current** repaired instrument at
`de09313` prints `closed=12/13 exit=1` (J8 red), not 10/13, so the ref's own
bytes are the only correct runner; the executor's receipt §RD42-5 says this
correctly. Required action: the L1 should land the composite as the round's
receipt (it is byte-identical to what the instrument writes with
`--receipt-out`, which is stronger than a stdout tee), and record that the
deliverable is a receipt, not a raw tee. If the literal single-plain-run tee is
required instead, K18 cannot close at Y (the `selftest cases=13 failures=3`
quote at `round-42-verifier-spotcheck.md:65` stays unbound).

## 10. Defect D4 (medium) — extra exemptions not in the frozen predicate

The frozen K18 allows exactly three dispositions per quoted value: bound,
`report-only` on its line, or named superseded. The limb adds two more
(`ExecK18Transcript.sh:70-75`, `:229-234`):

- **attack row**: a round-42 markdown row whose first cell is `aN`/`bN` is
  skipped entirely — 13 raw occurrences at base (`closed=12/13` ×4,
  `closed=11/13` ×7, `selftest cases=13 failures=0` ×1,
  `selftest cases=13 failures=2` ×1). The values are the verifier's mutant
  observations; no transcript can exist for a mutated scratch tree, so the
  exemption is substantively reasonable — but the freeze does not name it, and
  the exemption is line-wide: it also drops the *real* `selftest cases=13
  failures=0` quoted on row `a2` (`:110`), which happens to be bound elsewhere.
- **anti-example**: a non-summary-shaped value whose cell contains `mangled` or
  `substring` is skipped — 4 raw occurrences at base (2× `closed=10/100`,
  2× `closed=13/13`). This exemption is also the vehicle for D1.

Required action: an erratum that names both exemptions (and states that they
only apply to non-summary-shaped values / round-42 attack rows), or an
`exempt=<n>` field in the payload and a line in the frozen predicate. As
written, the limb's `closed` verdict is not the frozen predicate's verdict; the
receipt discloses the exemption set, which is honest, but disclosure does not
authorize it. (D1 must be fixed regardless: the anti-example exemption claims
not to hide summary-shaped claims and does.)

## 11. Scope note — the report and the append-only records

The limb scans `corpus/lessons/round-42*.md`, `corpus/lessons/round-43*.md`,
and top-level `.ufo/waves/round-43/*.md` only; `SCORECARD.md`, `LOG.md`,
`SHONEN.md` are not quote sources (declared, K14's domain) and the lane report
is graded only if it lands under one of those paths.

Measured:

```
$ check_k18 y_rootreport        # y_exec + lane-root REPORT.md quoting `closed=99/99 exit=0`
K18 payload=quotes=22,bound=22,report-only=0,superseded=0,unbound=0 closed=1
$ check_k18 y_report 1          # y_exec + ScribeReportSkeleton.report.md as .ufo/waves/round-43/report.md
K18 unbound token=closed=19/19 at .ufo/waves/round-43/report.md:27
K18 unbound token=selftest cases=19 failures=0 at .ufo/waves/round-43/report.md:29
K18 unbound token=selftest cases=10 failures=0 at .ufo/waves/round-43/report.md:45
K18 unbound token=closed=19/19 at .ufo/waves/round-43/report.md:309
K18 unbound token=selftest cases=19 failures=0 at .ufo/waves/round-43/report.md:310
K18 unbound token=closed=0/19 at .ufo/waves/round-43/report.md:313
K18 unbound token=selftest cases=10 failures=0 at .ufo/waves/round-43/report.md:329
K18 unbound token=selftest cases=10 failures=0 at .ufo/waves/round-43/report.md:414
K18 unbound token=closed=19/19 at .ufo/waves/round-43/report.md:440
K18 unbound token=selftest cases=19 failures=0 at .ufo/waves/round-43/report.md:440
K18 payload=quotes=39,bound=29,report-only=0,superseded=0,unbound=10 closed=0
```

Two consequences for the L1. (a) A lane-root `REPORT.md` is invisible: RD42-5's
own original locus (the report's "Work performed" section) would be ungraded if
the report lands there. (b) If the report lands as a scanned record (the
skeleton copied to `.ufo/waves/round-43/report.md`), it adds 10 unbound
occurrences at the pre-wave snapshot. At Y the `19/19` and
`cases=19 failures=0` lines bind from the r43 receipt, and `cases=10
failures=0` can bind from the C2 gate's committed transcript (the limb's
header explicitly allows no-`export-ref` evidence for the C2 gate); `closed=0/19`
(a negative-control row) still needs a transcript or `report-only`. This is a
landing-path coupling, not a limb bug — but it must be resolved or the report
will red K18 at Y.

## 12. Residual risk / verification gaps

- `3551a0fc` is not a frozen artifact yet: the executor was still regenerating
  its transcript and receipt when this seat stopped. The L1 must re-run the
  base/Y checks on the final bytes and confirm the executor receipt's hash table
  matches; at 17:01Z it did not (`243b562d` cited, `3551a0fc` measured).
- D1's fixture uses the word `mangled`/`substring` before a repeated token; the
  same skip occurs on any line where the first occurrence sits in such a cell
  (`cell_of` is also first-occurrence). No test in the executor's transcript or
  in `MutK18K19` exercises the repeated-token case.
- The wide round-42 evidence surface (D2) is an intentional design choice with
  a stated rationale (frozen archive); it is not an accident. The finding is
  that the frozen claim does not name it and the after-state depends on it.
- K18 cannot judge authenticity of a committed summary line (the receipt says
  so; K8's job). This seat did not test forged committed summary lines beyond
  the executor's own summary-only fixture (which reds because it lacks the
  token).
- The suite integration (K1-K19 payload/selftest wiring, the receipt) is not in
  this seat's scope; `MutK18K19` covers one-limb mutants and
  `ExecSelftest19`/`ExecSuiteSkeleton` cover the harness.

## Appendix A — consolidated commands (all from the scratch tree)

```
$ S=/fast/scratch/hyaku/kasegi-r43/RevK18; . /…/w1/ExecK18Transcript.sh
$ sha256sum /…/w1/ExecK18Transcript.sh
3551a0fc5a18d9e94e4f3f11a07520f6fd8082842cafad00d1b98f862495a89e
$ check_k18 "$S/base" 1
K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=selftest cases=13 failures=3 at corpus/lessons/round-42-verifier-spotcheck.md:65
K18 unbound token=closed=10/13 at corpus/lessons/round-42-verifier-spotcheck.md:177
K18 scope records=2 transcripts=160
$ check_k18 "$S/t_noverif"
K18 payload=quotes=4,bound=4,report-only=0,superseded=0,unbound=0 closed=1
$ for t in f0 f1 f1b f2a f2b f3 f3b f4a f4b f4c f5 f7 f7b; do check_k18 "$S/fx/$t"; done
f0      quotes=1,bound=1,unbound=0 closed=1
f1      quotes=1,bound=1,unbound=0 closed=1
f1b     quotes=1,bound=0,unbound=1 closed=0
f2a     quotes=1,bound=0,unbound=1 closed=0
f2b     quotes=1,bound=0,unbound=1 closed=0
f3      quotes=1,bound=0,unbound=1 closed=0
f3b     quotes=1,bound=0,unbound=1 closed=0
f4a     quotes=0,bound=0,report-only=0,unbound=0 closed=1
f4b     quotes=1,bound=0,unbound=1 closed=0
f4c     quotes=1,bound=0,report-only=1,unbound=0 closed=1
f5      quotes=1,bound=1,unbound=0 closed=1
f7      quotes=0,bound=0,unbound=0 closed=1     # D1
f7b     quotes=0,bound=0,unbound=0 closed=1     # D1
f7c     quotes=0,bound=0,unbound=0 closed=1     # D1, table-row form
$ check_k18 "$S/y_plain" | head -1
K18 payload=quotes=22,bound=21,report-only=0,superseded=0,unbound=1 closed=0
$ check_k18 "$S/y_self" | head -1
K18 payload=quotes=22,bound=20,report-only=0,superseded=0,unbound=2 closed=0
$ check_k18 "$S/y_both" | head -1
K18 payload=quotes=22,bound=22,report-only=0,superseded=0,unbound=0 closed=1
$ check_k18 "$S/y_exec" | head -1
K18 payload=quotes=22,bound=22,report-only=0,superseded=0,unbound=0 closed=1
$ . "$S/k18-narrow2.sh"; check_k18 "$S/base" | head -1
K18 payload=quotes=22,bound=14,report-only=0,superseded=0,unbound=8 closed=0
$ check_k18 "$S/y_exec" 1 | grep -E 'payload|unbound token'
K18 unbound token=closed=5/13 at corpus/lessons/round-42-verifier-spotcheck.md:52
K18 unbound token=closed=4/13 at corpus/lessons/round-42-verifier-spotcheck.md:53
K18 unbound token=closed=5/13 at corpus/lessons/round-42-verifier-spotcheck.md:227
K18 unbound token=closed=4/13 at corpus/lessons/round-42-verifier-spotcheck.md:228
K18 unbound token=closed=10/12 at corpus/lessons/round-42-verifier-spotcheck.md:298
K18 scope records=2 transcripts=6
K18 payload=quotes=22,bound=17,report-only=0,superseded=0,unbound=5 closed=0
$ check_k18 "$S/y_rootreport" | head -1
K18 payload=quotes=22,bound=22,report-only=0,superseded=0,unbound=0 closed=1
```

Independent instrument runs (not the limb), same scratch tree:

```
$ bash r42-at-de09313.sh --export-ref de09313… --lane … --work "$S/dew2" …   # ref's own bytes, plain
closed=10/13 exit=1                                         # exit 1, 144 s
$ bash r42-at-de09313.sh --selftest --export-ref de09313… …  # ref's own bytes, selftest
selftest cases=13 failures=3                                # exit 1, 179 s
$ bash corpus/instruments/r42-closure.sh --export-ref de09313… …  # current repaired instrument
closed=12/13 exit=1                                         # exit 1, 227 s
```

Environment: no tools installed/upgraded; bash + python3 stdlib only; no
pacman, no PATH writes, no config edits. Scratch
`/fast/scratch/hyaku/kasegi-r43/RevK18/` removed before yield. Only lane write:
this receipt. No git mutation; only `git show`, `git archive`, `git log`,
`git rev-parse`.
