# ExecK18Transcript — K18 (RD42-5) receipt

Seat `ExecK18Transcript` (executor, r43 wave 1). Lane `kasegi-shokunin`, base
`ab98fac9dce87130bc4f66de89e30650d63943dc`. Claims read from
`.ufo/waves/round-43/claims.json` (not edited). Scope: the RD42-5 narrative-evidence limb only — no suite
integration, no gate, no commits, no second judge.

## Deliverables (under `.ufo/waves/round-43/w1/`)

| file | lines | sha256 |
|---|---|---|
| `ExecK18Transcript.sh` (sourceable `check_k18`) | 278 | `3551a0fc5a18d9e94e4f3f11a07520f6fd8082842cafad00d1b98f862495a89e` |
| `ExecK18Transcript.transcript.txt` | 132 | `a0223f6232e64a4197b62fe8d02b414f67c8724d4591b7c1c785f82606eb2efb` |
| `ExecK18Transcript.de09313-tee.txt` → land at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt` | 33 | `44a53379bf3151d8f1667aa8f6c3417dc77b5a4e0149afac3288e04ea42d9db6` |

`bash -n ExecK18Transcript.sh` → clean (rc 0, no output).

## Interface

```
. ExecK18Transcript.sh
check_k18 <export-root>              # optional 2nd arg 1 = verbose (stderr only)
bash ExecK18Transcript.sh <export-root> [--verbose]     # standalone
```
stdout is exactly one line:
`K18 payload=quotes=<n>,bound=<b>,report-only=<r>,superseded=<s>,unbound=<u> closed=0|1`;
return 0 when `closed=1`, 1 when `closed=0`. Diagnostics
`K18 unbound token=<tok> at <file>:<line>` and a `K18 scope records=.. transcripts=..` line go to stderr only.
Pure function of the export tree (no lane git, no writes), so the suite's selftest can plant a mutant export
and re-call it.

## Declared scope

Quote surface (committed prose records):
- `corpus/lessons/round-42*.md` — glob, so `round-42-verifier-spotcheck.md` is in scope
- `corpus/lessons/round-43*.md`
- `.ufo/waves/round-43/*.md`, top level only (not `w1/`, `final-gates/`, `c1-controls/`)

`SCORECARD.md`, `LOG.md`, `SHONEN.md` are not quote sources: their `corrections=` ledger is K14's, and their
older-round `closed=` history predates r42. They are read only for `Correction (round 43)` supersede lines.

Token, whole (R41 boundary): `(?<![0-9/])closed=(\d+)/(\d+)(?![0-9/])` and
`(?<![0-9])selftest cases=(\d+) failures=(\d+)(?![0-9])`. `closed=10/100` never satisfies `closed=10/13`;
`failures=30` never satisfies `failures=3`; trailing punctuation does not hide a token.

Evidence store — two places only:
1. the **frozen round-42 archive** (every committed file under `.ufo/waves/round-42/`), which cannot be
   re-authored to bind a new value; and
2. this round's **attestation directories** `.ufo/waves/round-43/final-gates/` and `.../c1-controls/`.

This round's seat receipts (`.ufo/waves/round-43/w1/`) are claims awaiting verification, **not** evidence.
That exclusion is deliberate: without it a seat receipt could certify a value by quoting it, and this seat's
own receipt (which quotes `closed=10/13 exit=1` in its evidence blocks) would have bound the very value it
reports. A record never binds its own tokens either, so a fenced transcript pasted into a lesson does not
certify that lesson.

A token is bound only by a **summary-shaped** line in an evidence file —
`^closed=<n>/<m> exit=<k>$` or `^selftest cases=<n> failures=<k>$` — so a value inside a fixture's `printf`,
a payload cell, or a quoted defeat does not bind.

Exemptions, per occurrence: `report-only` on the quoting line; superseded by a `Correction (round 43)` line
quoting it, or by the blank-line-separated entry of a `claims-erratum*.md` (round-42/43 wave dirs) that carries
`superseded`; a **round-42** markdown table row whose first cell is an attack id (`aN`/`bN`) (observations from
mutated scratch trees; round-43 records get no such exemption and must carry `report-only`); a
**non-summary-shaped** value whose table cell names it a mangled exemplar (`mangled`/`substring`).
Summary-shaped values are always graded, even on those lines.

Base accounting is exact: 39 raw tokens in the two round-42 lesson files → 13 attack-row occurrences and 4
non-summary anti-example mentions dropped → `quotes=22`.

## Evidence (commands and real output)

Full transcript `ExecK18Transcript.transcript.txt` (sections 0-11). Key rows, all from isolated `git archive`
exports under `/fast/scratch/hyaku/kasegi-r43/ExecK18Transcript/fix/`:

| # | command | observed |
|---|---|---|
| 0 | `check_k18 <live lane worktree> --verbose` (17:09Z snapshot) | `quotes=28,bound=27,…,unbound=1 closed=0` — only `selftest cases=13 failures=3` at spotcheck:65 is open, because `final-gates/r42-at-de09313-run.txt` (19 lines, landed by the L1) already binds `closed=10/13` |
| 1 | base export `ab98fac9` → `check_k18` | `quotes=22,bound=19,unbound=3 closed=0` rc=1, naming `closed=10/13` at `round-42-verifier-spotcheck.md:65` and `:177`, `selftest cases=13 failures=3` at `:65` |
| 2 | base export **+ the 33-line tee** at `final-gates/r42-at-de09313.txt` | `quotes=22,bound=22,unbound=0 closed=1` rc=0 |
| 3 | base export + forged summary-only transcript (header + `closed=19/19 exit=0` + `selftest cases=19 failures=0`, no payloads, no 10/13) | `unbound=3 closed=0` rc=1 — still red |
| 4 | base export + transcript carrying `closed=10/100 exit=1` / `selftest cases=13 failures=30` | `unbound=3 closed=0` rc=1 — wrong denominator does not bind |
| 5 | tee export + record line `` `closed=11/12,` `` / `` `selftest cases=7 failures=1.` `` | `quotes=24,unbound=2 closed=0` rc=1 — trailing punctuation still extracted |
| 6 | base export + `corpus/lessons/round-43-probe.md` containing a fenced transcript with `closed=10/13 exit=1` | `quotes=24,unbound=5 closed=0` rc=1 — a record cannot self-certify |
| 7 | tee export + a `report-only` line carrying `closed=6/13 exit=1` and `selftest cases=5 failures=2`, plus a `report-only` line with no value | `quotes=24,bound=22,report-only=2,unbound=0 closed=1` — the no-value line adds nothing |
| 8 | base export + `.ufo/waves/round-43/claims-erratum-1.md` entry carrying `superseded` and quoting both tokens | `quotes=24,bound=19,superseded=5,unbound=0 closed=1` |
| 11 | HEAD tree + round-43 records + the 33-line tee | `quotes=28,bound=28,unbound=0 closed=1` rc=0 |
| 11b | same tree with only the run-only transcript `r42-at-de09313-run.txt` | `quotes=28,bound=27,unbound=1 closed=0` rc=1 (`selftest cases=13 failures=3`) |

### RD42-5 itself: the quoted values are the ref's own bytes

```
$ sha256sum <lane>/corpus/instruments/r42-closure.sh
fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b   (2185 lines, repaired)
$ bash <lane>/corpus/instruments/r42-closure.sh --export-ref de09313… --work <scratch>/w-cur --scratch-root <scratch>
closed=12/13 exit=1

$ git -C <lane> show de09313:corpus/instruments/r42-closure.sh > r42-de09313.sh      # 2142 lines
$ sha256sum r42-de09313.sh
d92c0de1e3b4d01ca330994c781fda6aeb0cfd874f00f6d17641c3f6bc73f464
$ bash r42-de09313.sh --export-ref de09313… --work <scratch>/w --scratch-root <scratch> --receipt-out receipt.txt
closed=10/13 exit=1
$ grep '^selftest cases=' receipt.txt
selftest cases=13 failures=3
```

So the frozen sentence at `corpus/lessons/round-42-verifier-spotcheck.md:65` is true of the instrument **at
that ref**, and the repair transcript must be produced by those bytes. Running the lane's current
`corpus/instruments/r42-closure.sh` against the same export prints `closed=12/13` and would leave the quote
unbound. (`suite-sha256=` inside a run transcript is `sha256` of the *exported* suite — `suite_sha()` hashes
`in_tree(SUITE_REL)` — so it does not identify the runner; the runner is the file whose own sha256 is shown.)

Deliverable provenance: stdout of the ref-bytes run (19 lines: header + J1-J13 + `closed=10/13 exit=1`),
then stdout of the ref-bytes `--selftest` (14 lines: 13 graded selftest lines +
`selftest cases=13 failures=3`), concatenated unedited with no header. That 33-line file is **byte-identical**
to the suite's own `--receipt-out` receipt for the same ref (`cmp` → identical), which is the format the
instrument defines. Key lines: `19:closed=10/13 exit=1`, `33:selftest cases=13 failures=3`.

## What the L1 must land

1. Land the 33-line tee at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`
   (sha `44a53379bf3151d8f1667aa8f6c3417dc77b5a4e0149afac3288e04ea42d9db6`).
   Its run half is already committed as `final-gates/r42-at-de09313-run.txt` — my first 19 lines are
   byte-identical to that file (`cmp` clean) — so the additive repair is the **selftest block**: either land
   the whole 33-line file (replacing/alongside the run-only file) or land its last 14 lines as
   `final-gates/r42-at-de09313-selftest.txt`. Without those 14 lines K18 stays red on
   `selftest cases=13 failures=3` (section 11b).
2. Nothing else is open at the 17:09Z snapshot: the only unbound quote in the whole surface is
   `selftest cases=13 failures=3`, which item 1 closes. The current round-43 records quote
   `closed=10/13` (`INTEGRATION-PLAN.md:22`, the RD42-5 landing line itself), `closed=12/13`
   (`INTEGRATION-PLAN.md:52`, bound by `c1-controls/do-nothing.txt`) and `closed=10/12`
   (`claims-erratum-1.md:5`, bound by the round-42 archive and named superseded by its own E1 entry). Any
   further `closed=`/`selftest cases=` value added to a round-43 record needs a summary line in
   `final-gates/`/`c1-controls/` or `report-only` on that line — the Y receipt at `final-gates/all-gates.txt`
   will bind `closed=19/19` and `selftest cases=19 failures=0` if the round records state them.
3. Re-run at the judged head: `bash ExecK18Transcript.sh <Y export> --verbose` must print `unbound=0 closed=1`;
   base `ab98fac9` stays `unbound=3 closed=0`; the round-41 head `1f74646` is red on other checks and K18's
   behaviour there is unaffected.

## Limits and risks (named, not silent)

- Binding is presence of a summary-shaped line, not authenticity: a committed forged summary line binds.
  Receipt forgery for the round is K8/J8's job; K18 does not re-derive a foreign instrument's run.
- Round-43 seat receipts never bind (deliberate, see scope). A receipt that misquotes a value is graded by the
  wave's report, not by K18 — otherwise 73 receipts would make the check unactionable and self-binding.
- Round-42 attack rows are out of scope by construction; the same shape in a round-43 record is graded, which
  is the actionable half of the class.
- The anti-example rule keys on `mangled`/`substring` in the token's cell and applies only to
  non-summary-shaped values; it drops 4 raw tokens today (2× `closed=10/100`, 2× a bound `closed=13/13`).
- Section 0 of the transcript is a live-worktree snapshot and its counts move as peers land files; sections
  1-8 and 11 run against isolated `git archive` exports and are stable.

## Environment / tooling

No tool installed, upgraded or removed (bash + python3 stdlib sufficed). No pacman, no PATH writes, no config
edits, no service restarts. Disk guard checked at start (`/fast/scratch/hyaku` 25% used, 606G free). All work
bound to `/fast/scratch/hyaku/kasegi-r43/ExecK18Transcript/` with `TMPDIR` set explicitly; the scratch
directory is removed after the deliverables are copied. Read-only git only (`archive`, `show`, `log`,
`rev-parse`, `status`); no add/commit/checkout/reset/stash/branch/tag/worktree. Lane writes: the three
deliverables and this receipt, nothing else.
