# RevC1Freeze — pre-freeze satisfiability (R22/R25) of frozen claim C1

Seat `RevC1Freeze` (reviewer, leaf). Round 43, kasegi-shokunin.
Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; claims-freeze commit
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. Axes: depth:verifiability, coverage.
Receipt-only item: no landable deliverable is produced by this seat.

Question asked of this seat: **can the instrument still to be built print the after-state that
`claims.json` C1 declares?** Not "is the plan good" — every literal and regex in C1's
`predicate`, `kill_rule`, `counting_commands`, `before` and `after` was checked against (a) base
bytes and (b) the declared after-adds: `corpus/instruments/r43-closure.sh` (a fork of
`corpus/instruments/r42-closure.sh`), the K14-K19 limbs, the correction/erratum blocks, and the
Y receipt. The standing implementation is the r42 engine, so every claim below that needs
execution was executed: three constant-level ports of the r42 suite were run against the base
export, plus the suite exactly as committed.

**Headline: C1 cannot be frozen as written.** Three blockers (B1, B2, B3) and two high-severity
literal defects (H1, H2) make the declared after-state unreachable as the claim states it. B3 is
not in the frozen text but in the instrument the round has already committed: its K8 cannot print
`closed=19/19 exit=0` at Y (§16). Each finding is a one- or two-line fix; none requires redesign.
Details and the measured port matrix follow.

---

## 0. Verdict table

| # | Check / literal in C1 | Status at base | Status the claim declares at Y | Verdict |
|---|---|---|---|---|
| B1 | `after`: base export prints `closed=13/19 exit=1` | measured 12/19 (ports A, B) or 10/19 (port D); 13/19 only in port C (§2) | `closed=13/19` | **UNSATISFIABLE as a natural fork**; reachable only by a port that makes K8 vacuous at base |
| B2 | K17 over `claims.json` `before`/`after` cells | red (correct) | must be green | **UNSATISFIABLE at Y**: 33 of 49 tokens unsatisfied, and the round's own `after` cell cannot be satisfied without falsifying the claim (§3) |
| B3 | `closed=19/19 exit=0` at Y (K8, committed instrument) | 12/19 (K8 absent branch) | 19/19 | **UNSATISFIABLE as implemented**: K8 requires the receipt's `export-ref` to equal the graded ref Y, which no receipt can declare about the commit that contains it (§16) |
| H1 | K14 `corrections=<n>` literals | red via the *row's* rule → **green**, i.e. a kill | green | **Kill-rule violation** under the dispatched row: its `payload=` exemption excludes the only base literal (§4) |
| H2 | K18 quoted `closed=`/`selftest cases=` values | red | must be green | **UNSATISFIABLE**: 191 unsatisfied tally occurrences in the row's own scan set; the broad reading is vacuous (§5) |
| M1 | K15 wave-dispatch narrative | red | must be green | 17 unbacked sentences, not the one the after-adds name (§6) |
| M2 | K16 placeholder promise | red | must be green | row-level scan over-collects 18 sections and its phrase list misses the defect sentence (§7) |
| M3 | `selftest cases=19` vs per-check (a)+(b)+(c) limbs | n/a | `cases=19 failures=0` | ambiguous counting; row wording yields 25-31 cases (§8) |
| L1 | predicate "the exact base figure is measured during integration … never pre-declared" vs `after` cell `closed=13/19` | n/a | n/a | internal contradiction; the same literal is graded by K17 and K18 (§9) |
| L2 | CLI: predicate authorises only `--export-ref` | n/a | n/a | the claim's own counting commands pass `--work/--scratch-root`; `--receipt-out/--lane/--leaf` likewise unmentioned (§10) |
| OK | K19 freeze ordering | red (round-43 dir absent) — correct | green | **satisfiable**; inputs verified (§11) |
| OK | K1-K13 payload grammar + replay limbs | byte-identical across ports | unchanged | **satisfiable**; measured (§2) |
| OK | `ref-not-found`, plain-run exit 2, 19-line shape, `--selftest` grammar | satisfied by the r42 engine | same | satisfiable (§12) |

"OK" rows are listed so the L1 does not churn them.

---

## 1. Method

Literal inventory was taken mechanically from `claims.json` (not from the seat prompt's summary:
the summary is truncated mid-sentence in the dispatch, so only the file is authoritative):

```
$ python3 -   # inventory: every closed=/failures=/cases=/corrections= token per claim and cell
--- round 43
C1 before  ['closed=10/12', 'closed=10/13', 'closed=12/13', 'closed=8/12']
C1 after   ['closed=13/19', 'closed=19/19', 'failures=0']
C1 predicate ['closed=0', 'closed=19/19', 'failures=0']
C1 kill_rule ['closed=19/19']
C2 after ['failures=0']  C2 predicate ['failures=0']  C2 kill_rule ['failures=0']
```

The regex used for the token extraction is
`(?<![0-9A-Za-z/])(?:closed=\d+/\d+|failures=\d+|cases=\d+)(?![0-9A-Za-z/])` — the R41 whole-token
form, so `closed=10/100` never satisfies `closed=10/10`. Every count in this receipt uses it.

Freshness of the reading: `claims.json` sha256 equals the hash in the freeze record —

```
$ sha256sum .ufo/waves/round-43/claims.json
a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630  .ufo/waves/round-43/claims.json
$ grep claims-sha256 .ufo/waves/round-43/freeze.txt
claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
```

All four ports ran the **committed** r42 engine (2185 lines) with the scratch/work roots and
`TMPDIR` inside `/fast/scratch/hyaku/kasegi-r43/RevC1Freeze`, never inside the lane, and each
port differs from the committed file only in the named constants (`diff` of the copies is
documented per run). No lane file was written before this receipt.

---

## 2. B1 — the declared base figure `closed=13/19` is not what a fork of the r42 suite prints

C1's `after` cell: "base export `closed=13/19 exit=1` with exactly K14-K19 open". That is 13
closed carried checks plus six open new ones. The r42 suite prints **12/13** at base — the
do-nothing control says so, and I re-measured it:

```
$ bash corpus/instruments/r42-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
      --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work $S/wA --scratch-root $S/sA
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,
ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=0,run-lines=1,selftest-lines=1,verdicts=1,summary=1,
closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=0
closed=12/13 exit=1
   (RUN A, exit=1, 230 s)
```

`diff=0` is the only red fact: the committed r42 receipt declares `export-ref=4c40ef21…`, and the
base export is three commits later. So whatever the r43 suite does with K8 decides whether base
is 12/19 or 13/19. K8's target is `RECEIPT_REL`, and `locate_receipt()` has a second door:

```
136:RECEIPT_REL = ".ufo/waves/round-42/final-gates/all-gates.txt"
1494:def locate_receipt(tree):
1495:    p = in_tree(RECEIPT_REL, tree)
1496:    if os.path.isfile(p):
1497:        return RECEIPT_REL, read_text(p)
1498:    root = in_tree(".ufo/waves/round-42", tree)      # <- hardcoded round, not ROUND
1499:    if os.path.isdir(root):
1500:        for dirpath, _dn, filenames in os.walk(root):
1501:            for fn in sorted(filenames):
1502:                if fn == "all-gates.txt":
1503:                    q = os.path.join(dirpath, fn)
1504:                    return os.path.relpath(q, tree), read_text(q)
1505:    return None, ""
```

and when both doors miss, `check_j8` synthesises a *canonical* receipt from the payloads it just
computed (lines 1588-1596) and grades that. Both branches were exercised:

### 2.1 Port B — `RECEIPT_REL` moved to round-43, fallback untouched

```
$ bash $S/probe-receipt43.sh --export-ref ab98fac9… --work $S/wB --scratch-root $S/sB
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,
ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=0,run-lines=1,selftest-lines=1,verdicts=1,summary=1,
closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=0
closed=12/13 exit=1
   (RUN B, exit=1)
```

The round-42 receipt is found **through the fallback**, so re-pointing `RECEIPT_REL` alone changes
nothing: base is still 12/19.

### 2.2 Port C — `RECEIPT_REL` **and** the hardcoded fallback moved to round-43

```
$ bash $S/probe-receipt43-nofallback.sh --export-ref ab98fac9… --work $S/wC --scratch-root $S/sC
J8 payload=receipt=(canonical),source=canonical,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,
ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,
payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=1
closed=13/13 exit=0
   (RUN C, exit=0)
```

Base is then 13/19 — **but only because the receipt is absent and K8 grades a receipt it
synthesised itself.** K8's whole subject (a committed receipt whose payload matches the tree)
is not examined at base in this branch. That is not an accident of my probe: it is the same
branch that minted the committed r42 receipt (`receipt=(canonical),source=canonical … closed=1`,
`.ufo/waves/round-42/final-gates/all-gates.txt:13`), i.e. the Y receipt records K8 as closed
against a receipt that did not exist yet.

### 2.3 Port D — the naive single-constant fork (`ROUND=43`)

```
$ bash $S/probe-round43.sh --export-ref ab98fac9… --work $S/wD --scratch-root $S/sD
J1 payload=records=0,blocks=0,graded=0,evidence=0,missing=0,wrong-grade=0,
  per-record=SCORECARD.md=0;LOG.md=0;SHONEN.md=0,union=0,replay=RevC1Counters.md=no-substrate closed=0
J2 payload=boundary=10/10,truth-tokens=3,stated=0,mangled=0,truth-stated=0,token=whole,
  replay=RevC1Counters.defeats.txt=rejected closed=0
J8 payload=receipt=(canonical),source=canonical,…,closed-line=0,… closed=0
J11 payload=corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,
  marker-appended=1,eof-closed=3/3,fenced=0 closed=1
closed=10/13 exit=1
   (RUN D, exit=1)
```

Two carried checks die under `ROUND=43`:
`check_j1` opens with `correction_lines(text, ROUND)` and closes on `contributing >= 1`;
`check_j2` closes on `stated > 0` over the same filter. At base there are **zero**
`^Correction (round 43)` lines:

```
$ grep -c '^Correction (round 43)' SCORECARD.md LOG.md SHONEN.md
SCORECARD.md:0
LOG.md:0
SHONEN.md:0
$ grep -h -o '^Correction (round [0-9]*)' SCORECARD.md LOG.md SHONEN.md | sort | uniq -c
      1 Correction (round 34)
      1 Correction (round 35)
      1 Correction (round 38)
      7 Correction (round 39)
      7 Correction (round 40)
     14 Correction (round 41)
      3 Correction (round 42)      # total 34 = J11's corrections=34
```

So the port is forced: **K1-K13 must keep a round-42 filter** (a separate `CARRY_ROUND = 42`
next to `ROUND = 43`, or `ROUND` left at 42 and a `MARK_ROUND = 43` for the new limbs). Under
that split the carried payloads are provably the r42 ones — RUN A vs RUN C differ in exactly one
line:

```
$ diff <(grep -E '^J[0-9]+ payload=' outA.txt) <(grep -E '^J[0-9]+ payload=' outC.txt)
8c8
< J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,…,diff=0,… closed=0
---
> J8 payload=receipt=(canonical),source=canonical,…,diff=1,… closed=1
```

with `J1 … replay=RevC1Counters.md=rejected`, `J2 … replay=RevC1Counters.defeats.txt=rejected`,
and J3-J7's replay limbs unchanged. In RUN D the J1 replay limb degrades to
`replay=RevC1Counters.md=no-substrate` — the exact "skips its defeat" the kill rule forbids.

### 2.4 Port matrix

| port | ROUND | K8 receipt target | K8 fallback | base tally | matches `after` cell? |
|---|---|---|---|---|---|
| A (committed engine) | 42 | round-42 | round-42 | `closed=12/13 exit=1` | no |
| B | 42 | round-43 | round-42 (hardcoded) | `closed=12/13 exit=1` | no |
| C | 42 | round-43 | round-43 | `closed=13/13 exit=0` | **yes** |
| D | 43 | round-43 | round-43 | `closed=10/13 exit=1` | no |

### 2.5 What the L1 must do for B1

Either

- **(i)** freeze the split (K1-K13 at `CARRY_ROUND=42`) **and** port the fallback to round-43,
  and state in the claim/report that K8 is green at base through the canonical branch, so the
  K8 base-red evidence quoted in C1's `before` cell ("J8 red only because the base carries
  commits after the r42 receipt") applies to the r42 suite, not to K8 in the r43 suite; or
- **(ii)** keep K8's r42 target (A/B) and change the `after` literal to the measured
  `closed=12/19 exit=1`.

Silently forking with `RECEIPT_REL` moved but the fallback left hardcoded (B) produces a suite
whose base figure is 12/19 while the claim says 13/19 — and `closed=13/19` is also graded by K17
and K18 (see B2, H2), so the disagreement surfaces twice.

**Status when this receipt was written:** the suite the round actually committed takes neither
option. It drops J8 entirely and its K8 reds on an absent receipt (base 12/19), and its K8 adds a
stricter `export-ref` equality that prevents K8 from closing at Y at all — see §16 (B3). Option
(ii) is therefore the live one: correct the claim's base figure, and restore the r42
ancestor+diff allowance in K8.

---

## 3. B2 — K17 cannot be green at Y: the `after` cells have no receipt to cite

C1's K17, verbatim:

> every `closed=`/`failures=` literal in a claims.json `before`/`after` cell appears in the
> control receipt that cell cites, or is named superseded by a committed claims erratum

A `before` cell cites `controls.c1`/`controls.c2`; an `after` cell cites **nothing** — by
construction it states the target state. The dispatched row resolves the ambiguity in the
unhelpful direction ("require each token to appear in the control receipt the claim cites
(`controls.c1`/`controls.c2`, or a path named in the string)"), i.e. `after` tokens are read
against a *pre-state* control. Measured over every claims file in the base export (the row says
"for every `.ufo/waves/round-<NN>/claims.json` in the export"), with controls = that round's
`c1-controls/` + `c2-controls/` and errata = that round's `claims-erratum*.md` carrying
`superseded`:

```
claims-files=21 tokens=49 unsatisfied=33
rounds with unsatisfied tokens: {'round-27': 1, 'round-35': 4, 'round-36': 4, 'round-37': 4,
 'round-38': 3, 'round-39': 3, 'round-40': 3, 'round-41': 2, 'round-42': 2, 'round-43': 7}
round-43 detail: [('C1','before','closed=10/13'), ('C1','after','closed=19/19'),
 ('C1','after','cases=19'), ('C1','after','failures=0'), ('C1','after','closed=13/19'),
 ('C2','after','cases=10'), ('C2','after','failures=0')]
round-42 detail: [('C1','after','cases=13'), ('C1','after','failures=0')]
round-41 detail: [('C1','after','cases=12'), ('C1','after','failures=0')]
```

Notes on the numbers, so the L1 can trust them:

- round-42's `closed=10/12` is *already* excused by `.ufo/waves/round-42/claims-erratum-5.md`
  ("Round-42 C1's `before` cell quote `closed=10/12` is superseded"), which is why that token is
  not in the list. The after-add `ScribeClaimsErratum` (round-43 erratum) is therefore
  *additional*, not the first time this is fixed.
- round-43 already carries `.ufo/waves/round-43/claims-erratum-1.md`, which covers `closed=10/12`
  and `closed=8/12` in C1's `before` cell; it does **not** cover `closed=10/13`.
- `closed=10/13` is quoted *inside* C1's `before` cell (it is part of the description of
  RD42-5), so K17 grades the claim's own description of the defect. That literal exists in four
  committed round-42 records (`corpus/lessons/round-42-verifier-spotcheck.md:65`,
  `.ufo/waves/round-42/claims-erratum-4.md:9`, `.ufo/waves/round-42/wave1/MutPredicates.md:17,29,30`,
  `.ufo/waves/round-42/wave1/CritKillRule.md:72`) and in no committed transcript before
  `ExecK18Transcript` lands `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`.

The seven round-43 `after` tokens are the claim's own target state. The only escape the frozen
text offers is "named superseded by a committed claims erratum" — an erratum that declares
`closed=19/19` superseded *falsifies the claim it is filing*. So K17 is not merely unplanned; it
is unsatisfiable at Y on any reading that keeps the `after` cells.

**Fix (before data).** Amend K17 to:

> … every `closed=`/`failures=`/`cases=` literal in a claims.json `before` cell appears in the
> control receipt the claim cites, and every such literal in an `after` cell appears in the
> round's `.ufo/waves/round-<NN>/final-gates/all-gates.txt` (or the control receipt the cell
> cites), or is named superseded by a committed claims erratum.

and scope the scan to the rounds the claim is about (round-42 and round-43 for RD42-8), not to
all 21 historical claims files — otherwise rounds 27, 35-41 need errata the round does not plan.
With that amendment: base is red for `closed=10/13` and for every round-43 after token (no
round-43 receipt exists at base), Y is green for the after tokens (the Y receipt prints
`closed=19/19`, `selftest cases=19 failures=0`) and needs one erratum for `closed=10/13`.
That is satisfiable with the after-adds actually dispatched.

---

## 4. H1 — K14's exemption hides the only base literal, so K14 passes at base (a kill)

The frozen K14 rule has no exemption. The dispatched row adds one:

> Exclude literals that occur only inside quoted defect evidence: a literal on a line whose own
> text also carries `payload=` or `mutant=` or `quarantined` is evidence, never a result (R41).

and, two sentences later, its own base expectation:

> At base ab98fac9: SCORECARD.md:1634 carries `corrections=33` while the live count is 34 ->
> stale=1 closed=0.

Base bytes, one literal, and it sits on a line that carries `payload=`:

```
$ ls SHENON.md SHONEN.md 2>&1; grep -rn 'corrections=' SCORECARD.md LOG.md SHONEN.md
ls: cannot access 'SHENON.md': No such file or directory
SHONEN.md
SCORECARD.md:1634:Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite
  at Y prints `J11 payload=corrections=33,groups=4,dups=4,excused=4,unexcused=0,marker=1,
  marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1` …
$ grep -o 'corrections=[0-9]*' LOG.md SHONEN.md SCORECARD.md | wc -l
1
```

So the exemption (`payload=` on the line) removes `SCORECARD.md:1634`, `literals=0`, `stale=0`,
and K14 closes **at base** — the kill rule's "a K14-K19 check passes at base" fires. The row's
base expectation and its exemption are mutually exclusive.

There is a second, structural reason the exemption was written: a superseding line that *quotes*
the superseded literal ("…the stale `corrections=33`…") would itself be graded, giving
`33 ≠ live` forever. The two requirements are reconcilable, but only with a directional rule,
e.g.:

> A literal is graded unless the line carrying it is a `Correction (round 43)` line that names
> that literal and the words `superseded`/`supersedes`. Lines inside fenced code blocks and
> lines carrying `mutant=`/`quarantined` are quoted evidence and are not graded.

With that: base has one graded literal (`corrections=33` on a `Correction (round 42)` line) and
the live count is 34 (measured: 34 anchored `Correction (round …)` lines, `J11 … corrections=34`)
→ red at base, as the frozen claim states; at Y the appended `Correction (round 43)` line names
it, and any *live* count it states must equal the post-append count (each appended
`Correction (round 43)` line raises the count by one — 34 + k — so the number written must be
computed after the append, which the claim already requires: "the value the suite re-derives at
the same export").

Third defect in the same sentence: **`SHENON.md` does not exist.** The frozen predicate, the row
spec and the dispatch summary all spell the record `SHENON.md`; the lane's record is `SHONEN.md`
(and both the r42 engine's `RECORDS` and J1/J11 use `SHONEN.md`). A limb built to the literal
reads a missing file, `read_text` returns `""`, and every `corrections=` literal in `SHONEN.md`
is silently ungraded — while K1/K11 grade that same file. Fix the literal to `SHONEN.md` in the
row spec and record the correction in the round's erratum (claims.json is frozen and must not be
edited).

---

## 5. H2 — K18's scan set is undefined; its narrow reading is unsatisfiable and its broad reading is vacuous

Frozen K18: "every `closed=`/`selftest cases=` value quoted in round-42/43 lane records appears
in a committed transcript under the round's final-gates/ or c1-controls/…". Three separations
are missing: which files are "lane records", which token shape is a "value", and what counts as
a "quoted value" rather than quoted *evidence*. Each was measured.

**(a) Token shape.** `closed=` occurs in two forms in these records:

```
$ grep -roE 'closed=[0-9]+' .ufo/waves/round-42 .ufo/waves/round-43 | grep -vE 'closed=[0-9]+/' | wc -l
3073                                  # per-check flag form, e.g. "… closed=1"
$ grep -roE 'closed=0\|1' .ufo/waves/round-42 .ufo/waves/round-43 | wc -l
86                                    # the grammar token in the K-line shape itself
```

Read as `closed=\d+`, K18 grades 3073 occurrences, and the ordinary flag value `closed=1` is
satisfied by the first transcript that prints one closed check — the check approaches vacuity
while grading almost nothing that matters. Read as `closed=<n>/<m>` (the tally form the RD42-5
defect is about) it is hard. Only the second reading is worth minting.

**(b) Scan set.** With tallies only, transcripts = each round's `final-gates/` + `c1-controls/`:

```
round 42 record-value occurrences=662  unsatisfied=404  files=63
  64 .ufo/waves/round-42/kasegi-r42-build-results.json
  36 .ufo/waves/round-42/wave1/RevSuitePlan.md
  25 .ufo/waves/round-42/wave1/ExecJ3Registry.skill-fix.txt
  17 .ufo/waves/round-42/wave1/ConnWave2Seed.txt
  …
round 43 record-value occurrences=381  unsatisfied=206  files=32
```

and on the row's own narrower set ("`corpus/lessons/round-42*.md` and round-43 lane records"):

```
corpus/lessons/round-42*.md: occurrences=39 unsatisfied=17
round-43 lane records (all): occurrences=410 unsatisfied=212
round-43 lane records (excl claims/spec/dispatch): occurrences=352 unsatisfied=174
```

The 17 in the lesson are legitimate observations from ad-hoc runs, all of them values the round
is *not* planning to transcribe (`closed=5/13`, `closed=4/13`, `closed=11/13` ×5,
`selftest cases=13 failures=2`, `closed=10/100` — the last is a deliberately mangled token quoted
as the F-TOKEN example at `corpus/lessons/round-42.md:32`). `ExecK18Transcript` backs exactly one
of them (`closed=10/13` at `--export-ref de09313e…`); the rest have no transcript and no planned
correction.

**(c) Quoted evidence.** Round-43's own seat records quote probe tables — e.g.
`.ufo/waves/round-43/w1/ConnSiblingPattern.md:100-109` lists `closed=19/19`,
`closed=19/19-rc1`, `closed=19/190` as *inputs* of a boundary test. Under K18 each is a quoted
value with no transcript. K14's row already recognises this class ("a literal on a line whose
own text also carries `payload=` or `mutant=` … is evidence, never a result"); K18 — the check
whose *subject* is quotation — does not. Also excluded by construction: the seats' teed
transcripts (`.ufo/waves/round-43/w1/*.transcript.txt`), which are the only transcripts that
exist before the Y receipt.

**Fix (before data).** Name the file set exactly (as K14 does), accept every
`*.transcript.txt` / `final-gates/` / `c1-controls/` file committed under the round as a
transcript, grade only `closed=<n>/<m>` and `selftest cases=<n> failures=<k>` (the RD42-5
shapes), add the quoted-evidence exemption, and — critically — exclude
`claims.json` from the scan, because the frozen claim quotes `closed=13/19` for a state that a
base-side transcript cannot print (B1).

---

## 6. M1 — K15's unbacked set is 17 sentences, not the one the after-adds name

Frozen K15: every sentence in `LOG.md` or `corpus/lessons` asserting a named `kasegi-rNN-*` wave
was dispatched must have `.ufo/waves/round-NN/<wave>-results.json` or a `Correction (round 43)`
line. Enumerated over `LOG.md` + every `corpus/lessons/*.md`, taking each `kasegi-rNN-X` that
appears on a line about dispatch/spawn/seats, and testing both name derivations
(`kasegi-rNN-X-results.json` and `wave1/wave2-results.json` for build/falsify):

```
mentions=59 unbacked=17
   LOG.md:1147 kasegi-r23-build          LOG.md:1148 kasegi-r23-falsify
   LOG.md:1240 kasegi-r24-build          LOG.md:1242 kasegi-r24-falsify
   LOG.md:1293 kasegi-r25-build          LOG.md:1295 kasegi-r25-falsify
   LOG.md:1804 kasegi-r42-falsify
   corpus/lessons/round-23.md:219 kasegi-r23-build
   corpus/lessons/round-23.md:221 kasegi-r23-falsify
   corpus/lessons/round-23.md:238 kasegi-r23-falsify
   corpus/lessons/round-24-verifier-spotcheck.md:168 kasegi-r24-falsify
   corpus/lessons/round-24.md:5  kasegi-r24-build
   corpus/lessons/round-24.md:6  kasegi-r24-falsify
   corpus/lessons/round-24.md:202 kasegi-r24-build
   corpus/lessons/round-24.md:206 kasegi-r24-falsify
   corpus/lessons/round-42-verifier-spotcheck.md:34  kasegi-r42-falsify
   corpus/lessons/round-42-verifier-spotcheck.md:174 kasegi-r42-falsify
```

Rounds 23, 24 and 25 have no `*-results.json` of any name at all
(`ls .ufo/waves/round-*/[a-z0-9]*results*.json` starts at round-28); rounds 28-42 are backed
under one derivation or the other. The planned corrections (RD42-2/3) name `LOG.md:1804` and the
lesson's repetition; `round-42-verifier-spotcheck.md:174` *quotes* the LOG sentence as RD42-2's
evidence, and `:34` summarises the wave shape — under a rule with no quoted-evidence exemption
each of those is itself an assertion needing its own correction.

**Fix.** Scope K15 to the round-42 sentences (that is the defect class the round mined), or plan
14 more corrections; and fix two derivations in the text: (a) `<wave>` in a sentence is
`kasegi-r42-falsify` while the file the before cell names is `wave2-results.json` — state the
mapping; (b) a sentence that quotes another sentence's claim is evidence, not an assertion.

---

## 7. M2 — K16's frozen form is fine; the row's generalization is not

Frozen K16 names exactly one object: "the round-42 lesson's `## Wave-2 falsification` promise is
named unfulfilled by a `Correction (round 43)` line". That is satisfiable: base red, Y green once
one correction names `corpus/lessons/round-42.md`'s `## Wave-2 falsification`.

The dispatched row widens it to "a `## ` section whose body … promises content `when the ...
reports`, `to be filled`, `TBD`, `placeholder`, or `pending the ... wave`" scanned over
`corpus/lessons/*.md, LOG.md, SCORECARD.md, SHONEN.md`. Measured: 18 section bodies match that
phrase list —

```
LOG.md | 2026-10-16 — protocol conformance …            | placeholder
LOG.md | Round 35 …  Round 36 … Round 37 …             | placeholder
SCORECARD.md | Capabilities                            | placeholder
corpus/lessons/round-22-verifier-spotcheck.md | Adjudication | placeholder
corpus/lessons/round-23.md | Mistakes                  | placeholder
… 18 total
```

— and every one of them is prose *about* a placeholder defect, not a promise. Conversely a
literal regex for `when the \w+ (reports|lands|returns)` **misses** the actual defect sentence,
"Appended when the round-42 falsify wave reports: …" (`corpus/lessons/round-42.md:52-56`),
because its subject is four words. A limb built to the row therefore needs 18 corrections and
still may not see its own defect.

**Fix.** Keep the frozen K16 (one named section). If the row is generalized, restrict the scan to
`corpus/lessons/round-42*.md`, require the section body to consist of the promise (no result
content), and match `Appended when`/`to be filled` rather than bare `placeholder`.

---

## 8. M3 — `selftest cases=19` versus the row's three limbs per new check

Frozen: "`--selftest --export-ref Y` prints nineteen graded lines … and `selftest cases=19
failures=0`". Row `ExecSelftest19`: "K14-K19 each need at minimum (a) a positive case …, (b) a
mutant …, and (c) one degenerate control that must be rejected". If (a)/(b)/(c) are counted as
cases, the summary becomes 13+3·6 = 31 (or 19+6 = 25 if the degenerate control is per-check), and
the frozen `cases=19` is unreachable. The r42 engine's shape is one graded line per check with
internal mutants — `selftest case=J9 mutants=3/3 positive=pass payload-match=1 verdict=pass`,
`selftest cases=13 failures=0` (`.ufo/waves/round-42/final-gates/all-gates.txt:28-33`) — so the
intent is clear, but the row must say so: **all three limbs live inside the single graded line of
their own check; nineteen lines, nineteen cases.**

---

## 9. L1 — the predicate forbids what the `after` cell does

C1's predicate: "the exact base figure is measured during integration and quoted in the report,
never pre-declared." C1's `after` cell: "base export `closed=13/19 exit=1` with exactly K14-K19
open" — a pre-declared base figure. Beyond the internal contradiction, this literal is graded by
K17 (§3) and by K18's claims-file scan (§5c), and it is printable only under port C (§2). Pick
one: drop the number from `after` (leave "base red with exactly K14-K19 open"), or delete the
"never pre-declared" sentence. Do not do both halves of the contradiction.

---

## 10. L2 — CLI literals the predicate does not authorise

The predicate authorises `--export-ref` (and an unnamed work dir "outside the lane"). The
trusted counting commands and the required tee use `--work`, `--scratch-root`, and the receipt
step needs `--receipt-out`; K9 needs `--lane`/`--leaf`; `--selftest` is named but its combination
with `--export-ref` is only implied. An instrument built to the predicate's letter exits 2 on
its own counting commands (the r42 driver rejects unknown arguments:
`*) printf 'r42-closure: unexpected argument %s\n' … ; exit 2`). Name the full option set in the
predicate, or state that the r42 CLI is carried verbatim.

---

## 11. K19 — satisfiable as frozen (do not churn)

Frozen K19 checks only ordering and presence: the round-43 freeze record's `frozen_at_utc` is not
earlier than the latest `measured-at=` in the two committed control receipts, and both receipts
carry that line. All inputs verified:

```
$ for f in .ufo/waves/round-43/c1-controls/do-nothing.txt .ufo/waves/round-43/c2-controls/before.txt; \
      do printf "%s " "$f"; grep -c '^measured-at=' "$f"; done
.ufo/waves/round-43/c1-controls/do-nothing.txt 1
.ufo/waves/round-43/c2-controls/before.txt 1
$ cat .ufo/waves/round-43/c2-controls/before.txt | head -30
=== do-nothing / before control: kasegi round 43 C2 (measured 2026-10-28T16:34:15Z) at base ab98fac9…
measured-at=2026-10-28T16:34:15Z
…
$ sed -n '38,60p' .ufo/waves/round-43/c1-controls/do-nothing.txt
…                                    # lines 38-39 are the tail of the RD42-5 listing
RD42-8 claims.json before literal vs control:
see .ufo/waves/round-42/c1-controls/do-nothing.txt — the frozen counter run against the base tree:
r42 suite absent (exit 127, cannot print closed=13/13); the r41 suite at base prints closed=10/12 …
closed=8/12 exit=1
RD42-6 freeze label:
2026-10-28T12:05:00Z
2026-10-28T08:00:01-03:00
   (long lines elided by me at the "…"; the file's own text continues)
   (c1's own first two lines, read with the read tool:
    === do-nothing control: kasegi round 43 (measured 2026-10-28T16:32:23Z) at base ab98fac9…
    measured-at=2026-10-28T16:32:23Z )
$ cat .ufo/waves/round-43/freeze.txt
frozen-at=2026-10-28T16:37:07Z
measured-at-max=2026-10-28T16:34:15Z
claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
base=ab98fac9dce87130bc4f66de89e30650d63943dc
                                       # 16:37:07Z >= max(16:32:23Z, 16:34:15Z); claims frozen_at_utc same
```

and the row's extra limbs also hold (one `measured-at=` per receipt; `freeze.txt`
`frozen-at=2026-10-28T16:37:07Z` equals the claims value; `claims-sha256` matches, §1). Base is
red because `.ufo/waves/round-43/` is absent from the base export. **No action needed** — the
only new check that needs none.

---

## 12. Literals confirmed satisfiable (measured, not inferred)

- Plain run refuses exit 2 and an unresolvable ref prints a distinct red: the r42 driver's
  `--export-ref` guard (`a plain run is refused (export mode only)` → `exit 2`) and its
  `ERROR ref-not-found ref=%s closed=0 exit=1` path are carried code, and the committed round-42
  spotcheck records the run at `deadbeef…`: "`ERROR ref-not-found ref=deadbeef… closed=0 exit=1`
  — exit 1 (distinct red)" (`corpus/lessons/round-42-verifier-spotcheck.md`, §2 row 6).
  I did not re-run that probe this pass; the statement rests on a byte-read of the driver and on
  that committed record.
- The K-line shape (`K<n> payload=… closed=0|1`), the 19-line order, `closed=19/19 exit=0` only
  at 19/19, and the selftest line grammar (`selftest case=<id> … positive=pass … verdict=pass`,
  `selftest cases=N failures=0`) all exist in the r42 engine and need only the `J→K` rename
  (`CHECK_IDS`, `NCHECKS=19`, receipt line count `5 + N + 1 + N + 1` = 45).
- "Each committed r41/r42 defeat artifact is re-executed and rejected": `DEFEAT_ARTIFACTS`
  binds seven artifacts by sha256 and `J1-J7` re-execute them; RUN C shows
  `replay=…=rejected` intact for all seven and payloads byte-identical to the committed engine
  (RUN A), i.e. carrying K1-K13 is safe **provided the round constant is not moved** (§2.3).
- The round-41 judged-head export requirement (`closed<19/19 exit=1`) is not at risk: the r42
  suite already prints a red tally at `1f746461…` and K9 re-derives it in a nested run (the
  engine's `neg_accept` requires `rc!=0`, `0≤tally<NCHECKS` and ≥2 dependent reds).

---

## 13. Residual risk and what I did not do

- `corpus/instruments/r43-closure.sh` does not exist yet; **no K14-K19 limb was executed**. Every
  statement above about K14-K19 is either a byte measurement of the objects they grade (counts,
  file sets, tokens, timestamps) or a code-read of the r42 functions they must reuse, and is
  labelled as such. The four executed ports measure the *carried* checks, which is where the base
  figure is decided.
- The K14-K19 findings are stated against the dispatched row text
  (`build-w1-spec.py:45-…`) as well as against the frozen predicate, because the two disagree;
  where they disagree I named both and which one the L1 must change.
- Attack share, seat counts and the C2 instrument are out of this seat's scope; C2 was touched
  only where a C1 literal grades a C2 cell (K17's `cases=10 failures=0`).
- Scratch (`/fast/scratch/hyaku/kasegi-r43/RevC1Freeze`, including the four run trees and the
  three probe copies) was removed before this receipt was yielded; the numbers above are the only
  copy of those runs.
- Tooling: none installed or upgraded this pass; no network fetch; no pacman. No git write of any
  kind was performed — the ports read the lane with `git archive` and `git rev-parse`/`git diff`
  only, and no fixture repository was created (none was needed).

---

## 14. MUST-FIX list for the L1, before any data is counted

1. **B3 (do this first)** — restore the r42 ancestor+diff allowance in the committed `check_k8`
   (accept a receipt whose `export-ref` is an ancestor of `FULL`, with `git diff --name-only`
   limited to the receipt path); without it K8 can never close at Y and `closed=19/19 exit=0` is
   unreachable however the six new limbs perform. Also decide and state whether K8 is "J8
   re-pointed" (frozen predicate's wording) or a new check with the grammar the suite implements.
2. **B1** — correct the base figure. The committed suite (and ports A/B) print **12/19** at base;
   `after` must say `closed=12/19 exit=1`, or the claim must be amended to require only that
   K14-K19 are open at base. If the round instead keeps the r42 `RECEIPT_REL`/fallback, base is
   still 12/19; `closed=13/19` is reachable only through the canonical branch that K8's own
   committed form does not use.
3. **B2** — amend K17: `before` cells against the cited control, `after` cells against the
   round's `final-gates/all-gates.txt`; scope to the claims files the claim is about.
4. **H1** — replace K14's `payload=` exclusion with a directional supersede rule; if the
   exemption is kept as written, K14 passes at base and the round's own kill rule fires.
5. **H1b** — `SHENON.md` → `SHONEN.md` (predicate, row, erratum).
6. **H2** — define K18's scan set and token shape, accept seat transcripts, exempt quoted
   evidence, exclude `claims.json`.
7. **M1** — scope K15 to round-42, or plan corrections for 14 more sentences; state the
   `wave → results file` mapping and the quoted-sentence rule.
8. **M2** — keep K16's frozen single-section form; do not let the limb scan by bare `placeholder`.
9. **M3** — state that the three selftest limbs live inside the nineteen graded lines.
10. **L1/L2** — resolve the "never pre-declared" versus `closed=13/19` contradiction; name the
    full CLI in the predicate.

Everything else in C1 is satisfiable on committed bytes; the three blockers are small code or
text edits, not redesigns, and all must land before the first K-line is graded or the round will
spend its data budget on an instrument that cannot print its own claim.

---

## 15. Commands run (verbatim, with exit status)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status        # /fast 26% used, 601G free
$ git -C .../kasegi-shokunin rev-parse HEAD                                    # 4cb6d4ae768481e1a14afbedc2d865a060ebacfd
$ sha256sum .ufo/waves/round-43/claims.json                                    # a4c03e1e…  == freeze.txt
$ for f in .ufo/waves/round-43/c1-controls/do-nothing.txt .ufo/waves/round-43/c2-controls/before.txt; \
      do printf "%s " "$f"; grep -c '^measured-at=' "$f"; done                     # 1, 1
$ bash corpus/instruments/r42-closure.sh --export-ref ab98fac9… --lane … --work $S/wA --scratch-root $S/sA
  -> closed=12/13 exit=1                                                       # RUN A, 230 s
$ bash $S/probe-receipt43.sh            --export-ref ab98fac9… …              # RUN B -> closed=12/13 exit=1
$ bash $S/probe-receipt43-nofallback.sh --export-ref ab98fac9… …              # RUN C -> closed=13/13 exit=0
$ bash $S/probe-round43.sh              --export-ref ab98fac9… …              # RUN D -> closed=10/13 exit=1
$ diff <(grep -E '^J[0-9]+ payload=' outA.txt) <(grep -E '^J[0-9]+ payload=' outC.txt)   # only J8 differs
$ grep -c '^Correction (round 43)' SCORECARD.md LOG.md SHONEN.md               # 0, 0, 0
$ grep -h -o '^Correction (round [0-9]*)' … | sort | uniq -c                   # 34 total == J11 corrections=34
$ python3 <claims-token + control/erratum join>                                # 21 files, 49 tokens, 33 unsatisfied
$ python3 <K18 scan over round-42/43 records>                                  # 404/63, 206/32, 17, 174
$ python3 <K15 dispatch-sentence scan>                                         # 59 mentions, 17 unbacked
$ python3 <K16 section-body scan>                                              # 18 promise-shaped bodies
$ git rev-parse --verify --quiet 1f7464612ac4c44e39886b82e812610d3c039b13^{commit}   # resolves
$ git rev-parse --verify --quiet ab98fac9dce87130bc4f66de89e30650d63943dc^{commit}   # resolves
$ git rev-parse --verify --quiet de09313e8edb98280b19767d0094bb2dd8031d73^{commit}   # resolves
$ grep -roE 'closed=[0-9]+' .ufo/waves/round-42 .ufo/waves/round-43 | grep -vE 'closed=[0-9]+/' | wc -l
                                                                               # 3073
$ grep -roE 'closed=0\|1' .ufo/waves/round-42 .ufo/waves/round-43 | wc -l       # 86
```

Plot: C1's evidence chain is sound where it is measurable (K19, the carried checks, the CLI
behaviours, the 19-line shape) and unsound exactly where this round's new value lives — in the
six narrative-evidence checks, whose escape clauses, scan sets and case arithmetic are
underspecified in four independent ways. Fix the text, not the ambition: the round can still
print `closed=19/19 exit=0` at Y with every one of the six checks red at base, but only after
B1-B2 and H1-H2 are resolved on paper.

---

## 16. B3 — the committed K8 cannot print `closed=19/19 exit=0` at Y, and J8's grammar is not carried

By the time this receipt was written the suite was no longer hypothetical: it is committed at the
lane HEAD that had advanced to `ffe197d` (473 lines; worktree copy `sha256 6f585a48…` on top of
blob `d31fbbf0…`). I read the committed bytes — not to grade a sibling's work, but because the
frozen claim's after-state depends on what that code does. Its own header states the
composition:

```
$ sed -n '10,26p' corpus/instruments/r43-closure.sh
# grades an exported tree, never a working tree.  The export is produced with
#     git -C <lane> archive <hash> | tar -x -C <work>/export
# A ref that does not resolve prints `ref-not-found` and exits 1: an
# unresolvable ref is a red, never a vacuous pass.
#
# Composition.  K1-K7 and K9-K13 carry the round-42 suite's J1-J7 and J9-J13
# checks verbatim by invoking its committed bytes inside the export and
# re-emitting each `J<n> payload=...` line as `K<n> payload=...`; the round-42
# J8 is NOT carried because its receipt path is the round-42 receipt, which the
# round-43 tree legitimately invalidates.  K8 is the round-43 receipt check with
# the same payload grammar (receipt/ref/digest/time-basis/utc/one-run/
# payload-match/forged/selftest-lines/summary/closed-line).  K14-K19 are the
# round-43 narrative-evidence checks, sourced from corpus/instruments/r43-limbs/.
```

Three consequences, each a byte-level reading of the committed file:

**(a) Base cannot be 13/19.** With no round-43 receipt in the export, K8 takes the absent branch:

```
146:        printf 'K8 payload=receipt=%s,source=absent,header=0,ref=0,digest=0,time-basis=0,utc=0,one-run=0,payload-match=0/0,forged=0/0,selftest-lines=0,summary=0,closed-line=0 closed=0\n' "$RECEIPT_REL"
147:        return 1
```

so K1-K7 and K9-K13 close (12) and K8 is red → base is **12/19**, exactly what ports A and B
measured on the r42 engine. Because the carried payloads are re-emitted from the exported r42
suite itself (the wrapper invokes it with `--export-ref "$FULL"`), K1-K13 keep their round-42
filter by construction — RUN A's twelve closed payloads are what K1-K7/K9-K13 reproduce, and the
one difference is that RUN A's single red (J8) is dropped instead of re-pointed. The frozen
`after` literal `closed=13/19 exit=1` is therefore wrong against the instrument the round is
actually landing, not merely against my fork of it.

**(b) Y cannot be 19/19.** `ok_ref` requires the receipt's declared `export-ref` to *equal* the
ref being graded:

```
157:    closed=$(grep -cE '^closed=(18/19 exit=1|19/19 exit=0)$' "$r")
160:    [ "$ref_line" = "$FULL" ] && ok_ref=1
229:    [ "$ok_hdr$ok_ref$ok_dig$ok_tb$ok_utc$ok_one" = "111111" ] || return 1
```

and `FULL` is the resolved `--export-ref` (`84:FULL="$(git -C "$LANE" rev-parse --verify
"${EXPORT_REF}^{commit}")"`). A receipt that lives inside the tree it certifies cannot declare
that tree's own commit: the receipt is produced by a run at J (the tree without it), so it records
`export-ref=J`; at Y the comparison is J ≠ Y, K8 reds, and the run prints `18/19 exit=1`.
Iterating does not converge — every rewritten receipt declares the *previous* commit, so it is
always one commit stale. The r42 engine solved precisely this with an ancestor test plus a
one-file diff allowance (`check_j8`: `git merge-base --is-ancestor ref REF`, and
`git diff --name-only ref REF` limited to `{RECEIPT_REL, rel}`), which is why the committed
round-42 receipt closes while declaring `export-ref=4c40ef21…` inside commit `b2c49ea`. The
committed round-43 K8 dropped that allowance, so K8 can never close at Y and
`closed=19/19 exit=0` is unreachable **as implemented**, independently of the frozen text.

**(c) The carried grammar is contradicted as well.** The frozen predicate says "K1-K13 keep the
r42 J1-J13 payload grammar"; the committed suite says J8 is not carried and K8 has a different
grammar (`header/ref/digest/time-basis/utc/one-run/…` against J8's
`sentinel/lines/ref/digest/time-basis/utc/ancestor/diff/run-lines/…`). One of the two must
change — either K8 is J8 re-pointed at the round-43 receipt with the ancestor+diff rule preserved
(and the claim's base figure becomes 12/19), or the predicate must say K8 is new and carry the
grammar the suite implements.

**Fix.** Restore the r42 ancestor+diff allowance in `check_k8` (accept a receipt whose
`export-ref` is an ancestor of `FULL` with `git diff --name-only` limited to the receipt path),
and change the frozen `after` figure to the measured base value. Anything else leaves the round
unable to print its own target, however well the six new limbs are built.

I make no claim in this section about the limbs: K14-K19 are sourced from
`corpus/instruments/r43-limbs/`, which is not yet committed, and §3-§8 stand on the frozen and
dispatched text alone.
