# CritFreezeAudit — round-39 freeze falsification (spec level, before the suite lands)

Seat `CritFreezeAudit` (critic, leaf). Axis: depth:verifiability. Item: falsify the frozen claims — can a
do-nothing round satisfy the frozen counting commands? This is a spec review: `corpus/instruments/r39-closure.sh`
does not exist yet (`.ufo/waves/round-39/c1-controls/before.txt`: `No such file or directory`), so every finding
below is against the frozen text, not an implementation.

Inputs (read-only): `.ufo/waves/round-39/claims.json` sha256
`e427ab6a6ecec4b1f49ed5eed95860c468e0982af331a3a1ba135649d27e051c` (freeze commit `dcd3170`); base
`480b1a505a2dfc14a4f718d16d63808247214d0a`; before-controls `c1-controls/before.txt`, `c2-controls/before.txt`,
`census-before.txt`; `corpus/lessons/round-38-verifier-spotcheck.md` §5 R1–R5; `corpus/lessons/round-38.md`;
`.ufo/waves/round-38/final-gates/all-gates.txt` at the r38 tip `f06148c6`. No lane gate was executed (critic
scope). Deliverable: none — receipt only. Writes: this receipt plus scratch
`/fast/scratch/hyaku/kasegi-r39/CritFreezeAudit/` (removed before yield).

## Verdict summary

| Area | Verdict | Core reason |
|---|---|---|
| A. R1 class — self-referential after-commands | **breach** | `--export-ref <J>` cannot contain the receipt that G2 demands in the export; the only way to green it violates the head rule |
| B. Base / prior-head red | base **satisfied** (weakly); r38 head **breach** | base lacks the receipt and ledger section, so it must be red; the r38 head named in the freeze is a 37-char unresolvable hash, so the prior-head red is never exercised |
| C. C2 counters | **breach** | registry expectation is off by one (58 vs 59); the counters are format-only, so junk and sourceless rows pass |
| D. Graded lines | summary-only **satisfied**; "graded" **breach** | a summary line cannot satisfy a case, but `mutants=0/0` and `payload=` pass; R2/R4 are not covered by any check |

**Bottom line:** a do-nothing round (no real fix) can print `closed=8/8 exit=0` against these predicates. The
discriminating content is G2 (a hand-writable receipt) and G7 (a hand-writable empty section); G1, G3, G4, G5
and the C2 counters are vacuous at zero, and G8 is a pinned carry-over. Section D5 gives the concrete path.

## A. R1 class — does an after-command require a commit that cannot contain its own evidence?

### A1 — BREACH: `--export-ref <J>` cannot print `closed=8/8`

Exact frozen text:

- counting command 1: `bash corpus/instruments/r39-closure.sh --export-ref <J> -> closed=8/8 exit=0`
- after: ``closed=8/8 exit=0 at J; selftest cases=8 failures=0 graded``
- head rule: ``J is the lane commit that carries every round-39 change except that receipt; the lane tip Y adds only the receipt file (`git diff --name-only J Y` = `.ufo/waves/round-39/final-gates/all-gates.txt`)``
- G2: ``.ufo/waves/round-39/final-gates/all-gates.txt` in the export starts with `all-gates v3`, carries exactly one `export-ref=<40 hex>` whose commit exists and is ancestor-or-equal of REF``

The head rule says J does **not** carry the receipt. G2 requires the receipt **in the export**. An export of J
therefore has no receipt, G2 is `closed=0`, and the run ends `closed=7/8 exit=1` — the frozen command's expected
output is unsatisfiable by construction. This is exactly the defect the round-38 verifier killed C1 over:

> R1 — frozen self-referential predicate not mined. C1's G2 required the receipt inside the export while the
> judged-head rule made J the receipt's own `export-ref` … J cannot contain the receipt that names it.
> (`corpus/lessons/round-38-verifier-spotcheck.md:155-160`)

The r38 committed receipt records the same failure mode on its own bytes:

```
export-ref-run: G2 payload=receipt=0,sentinel=0,export-ref=0,... closed=0
export-ref-run: closed=7/8 exit=1
```

Fixture proof (throwaway git repo under scratch; `git rev-parse --show-toplevel` asserted equal to the fixture):

```
J=ef30cad2b7709a95d43828495ef8eb7e637e054f
Y=b9ebbf0223f3654d8a0226a08d61bcd74d948624
diff J..Y: .ufo/waves/round-39/final-gates/all-gates.txt
=== frozen counting command, literal --export-ref J
G2 closed=0 receipt-absent-from-export
exit=1
=== genuine run over the tip Y
G2 head=[all-gates v3] export-ref=ef30cad2… ancestor=1 diff=[.ufo/waves/round-39/final-gates/all-gates.txt] diff-only-receipt=1
G2 closed=1
exit=0
```

So the genuinely green run is over **Y**, which counting command 1 does not name. Either the command is wrong
(it should be `--export-ref <Y>` with the receipt recording `export-ref=J`) or the head rule is wrong (J must
carry the receipt). The freeze states both and they cannot both hold. `--selftest --export-ref <J>` inherits the
same ambiguity: it is green at J only if the selftest's positive G2 case is a synthetic fixture, in which case
the selftest no longer proves the closure run's G2.

### A2 — BREACH: the only way to satisfy counting command 1 violates the head rule

If J is made to carry a receipt, the receipt must name a commit A with `git diff --name-only A J` = receipt only.
A cannot be J (a commit cannot contain its own hash), so the receipt in the judged head's export names A ≠ J, and
the `closed=8/8 exit=0` line in it was written before any run over J (a pre-printed claim). Fixture:

```
B=108eb24d60e97ed8273cac4f88acf34b7919a012
Jb=cd09da7a5d1292c20d18afafc0fb93cf4e658ac9
diff B..Jb = .ufo/waves/round-39/final-gates/all-gates.txt
=== frozen counting command literals against Jb
G2 export-ref=108eb24d… ancestor=1 diff=[.ufo/waves/round-39/final-gates/all-gates.txt] diff-only-receipt=1 receipt-closed-line=[closed=8/8 exit=0]
G2 closed=1
exit=0
--- head-rule statement check: does Jb carry the receipt?
Jb tree: .ufo/waves/round-39/final-gates/all-gates.txt
```

The command is green at Jb, but Jb carries the receipt, contradicting "J … carries every round-39 change except
that receipt", and the receipt in Jb's export names B, not Jb. The 8/8 is a bootstrap claim, not a run over the
judged head. The kill rule does not forbid a bootstrap receipt; only "any committed fixture shows a check passing
while its defect is present" could catch it, and a bootstrap is not a fixture.

### A3 — BREACH: the head rule's hash sentence contradicts G2

Head rule: ``Lane files never name J by hash (a commit cannot contain its own hash)``. G2 requires a **lane file**
(`.ufo/waves/round-39/final-gates/all-gates.txt`) to carry ``export-ref=<40 hex>`` = J. The receipt is a lane file
that must name J by hash. The sentence is only true if restricted to "no lane file at or before J", which is not
what it says. A strict implementation enforcing the head rule must fail G2; an implementation ignoring it lets
the receipt name J. The freeze requires both.

### A4 — BREACH: G3 is globally scoped and red before the round starts; the escape hatch preserves R3

Exact frozen text: ``every `--export-ref <hash> -> closed=K/K` or selftest result quoted in the lane files
SCORECARD.md, SHONEN.md, LOG.md or corpus/lessons/round-38.md has a committed transcript in
`.ufo/waves/round-39/final-gates/` or is explicitly labeled report-only``.

The lane already contains literal matches with no round-39 transcript:

```
SCORECARD.md:1434:    bash corpus/instruments/r36-closure.sh --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c -> closed=0/9 exit=1
SCORECARD.md:1435:    bash corpus/instruments/r36-closure.sh --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988 -> closed<9/9 exit=1
round-39 final-gates: absent
```

Those are round-36 runs. As written, G3 is red at the judged head unless the round commits round-39 transcripts
for runs it did not make, or retro-labels historical text report-only (touching append-only history). At the same
time, the clause "or is explicitly labeled report-only" is the same escape the r38 verifier rejected as R3, and
G3's file list excludes the round report (`.ufo/reports/round-39/kasegi.md`), so the report can quote any
uncommitted run. The check is simultaneously over-broad (historical lines) and under-broad (the report).

## B. Base and prior-head red

### B1 — SATISFIED (base): 480b1a5 must be red

Exact frozen text: ``base 480b1a505a2dfc14a4f718d16d63808247214d0a or r38 judged head … export prints
closed=8/8`` (kill), and ``--export-ref 480b1a50… -> closed<8/8 exit=1`` (counting command 3).

Measured at base:

```
480b1a505a2dfc14a4f718d16d63808247214d0a resolves; git archive | tar -t -> 8207 entries
base tree .ufo/waves/: round-34 … round-38 only (no round-39)
base ledger: grep -c 'Round-39' -> 0
base: r39 all-gates.txt absent (git cat-file -e -> absent)
```

G2 (receipt "in the export") and G7 (`## Round-39 dispositions` section) cannot pass at base, so base < 8/8
regardless — provided absence is fail-closed, which G2's "starts with `all-gates v3`" implies for the receipt and
G7's "carries a … section" implies for the ledger.

Weakness: only G2 and G7 are structurally guaranteed to fail at base. G1 (zero declarations), G3 (no round-39
quotes), G4 (zero tracked round-39 dispatch files: `git ls-tree -r --name-only 480b1a5 | grep -c
'round-39.*-dispatch.json'` -> `0`), G5 (no `## Round 39` section to contain a `Final lane commit:` line), G6
(hygiene) and G8 (pinned carry-over) can all pass at base. Base red therefore proves the round added two files,
not that any check checks anything.

### B2 — BREACH: the r38 judged head named in the freeze does not exist

Exact frozen text (counting command 4): ``--export-ref 66703aca50529a35be49aa8759d04140720ad -> closed<8/8 exit=1``;
kill rule: ``r38 judged head 66703aca50529a35be49aa8759d04140720ad export prints closed=8/8``.

Measurement:

```
66703aca50529a35be49aa8759d04140720ad len=37 -> git rev-parse --verify -q -> UNRESOLVED
git archive 66703aca50529a35be49aa8759d04140720ad | tar -t | wc -l -> 0      (exit 128)
66703acaaff50529a35be49aa8759d04140720ad len=40 -> resolves (the real r38 head)
occurrences of the 37-char string in claims.json: 2 (command 4 + kill rule)
occurrences of the 40-char string in claims.json: 0
```

The command dies at export (exit 128, no `closed=K/K` line), so the expected `closed<8/8 exit=1` is never
produced and the prior-head red is not exercised at all. A do-nothing round cannot fail this control because the
control cannot run. The real r38 judged head is `66703acaaff50529a35be49aa8759d04140720ad` (it contains `aff`
after `66703aca`; the frozen string dropped those three characters).

## C. C2 counters — can a junk or sourceless row pass the counts?

### C1 — BREACH: the registry expectation is off by one

Exact frozen text:

- counting command: ``grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58``
- predicate: ``registry row S057 added …; three rejected rows S056 (CISA Minimum Requirements for VEX), S058 (OpenVEX v0.2.0), S059 (CycloneDX v1.7 analysis) appended with reason and flip``
- kill rule: ``S056/S058/S059 rows absent as rejected rows``

Measured with the frozen regex: base = **55** (also 55 at the freeze commit `dcd3170`); base rows S056–S059 =
none (only S055). Four new registry rows (S057 mined + S056/S058/S059 rejected; the precedent rejected rows
S026/S027/S028 sit in the same `| S0xx |` table and are counted) give **59**, not 58. Simulation on a copy of the
base file:

```
base rows: 55
after +4 rows: 59
```

`58 = 54 + 4`: the freeze reused the round-38 **before** count (54 at `a173b0c2`), not the round-39 base (55).
Consequence: a compliant round yields 59 and misses the frozen counter by one; a round that omits one of the four
declared rows yields 58 and passes the counter while violating the kill rule. The frozen counter rewards the
non-compliant tree.

### C2 — BREACH: the counters are format-only, so junk and sourceless rows pass

Exact frozen texts and what they actually bind:

| Frozen counter | What it binds | Junk/sourceless pass |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 22` | a first cell `F<digits>` | any fabricated row; no URL/status/mined check |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58` | a first cell `S<3+ digits>` | any row, mined or rejected, with or without a URL |
| `grep -rlE '^source: S057' corpus/knowledge \| wc -l -> 1` | one line anywhere | a file containing only `source: S057` |
| `ls corpus/knowledge/*.md \| wc -l -> 51` | file count | empty files |

Demonstrated:

```
junk frontier row appended: | F99 | totally fabricated junk | https://example.invalid/x | n/a | junk |
base frontier: 21
after junk row: 22
knowledge file containing only `source: S057`: files matching -> 1
```

The remaining C2 commands are lane-owned and self-consistent, not provenance checks:

- `frontier-recheck-count.py` re-executes each entry's **own** `recheck:` line (its docstring: "point every entry
  at one captured source, or write `recheck: true`, and the loop reports 8/8 with no capture work done").
- `source-recheck.py` reads **checked-in** snapshots: "Manifest paths are relative to the manifest directory. This
  instrument reads [checked-in source snapshots]" and compares the capture's sha256 to the manifest's `sha256`
  field. No network fetch. A self-consistent fabricated capture + manifest passes; the junk twin only shows that
  a twin mismatching S057's capture is rejected, which is internal consistency, not provenance.
- `sources-census.sh validate` checks row shape and enums only (header lines 24–33: E01 NF, E02 id, E03/E04
  duplicates, E05–E09 enums/dates, W01–W04 warnings). No DNS/HTTP check, so a fabricated
  `https://example.invalid/…` row passes.

So a sourceless registry row passes every C2 counting command. The kill-rule items that would catch it — "S057 row
absent or NF != 13", "S056/S058/S059 rows absent as rejected rows", "junk-f22 accepted", "harness … incl. PASS F22
ids=S057" — are **not** in the counting-command list; they are manual checks, and the frozen commands alone do not
carry them.

## D. Graded-line requirements

### D1 — SATISFIED: a summary-only line cannot satisfy a case

Exact frozen texts: ``one graded `selftest case=G<n> ... positive=pass ... verdict=pass` line per check`` and
``no summary-only line satisfies a case``. Test against the literal shape
`^selftest case=G[1-8] .*positive=pass.*verdict=pass$`:

```
selftest cases=8 failures=0            -> 0 graded-pattern hits
```

The plural `cases=` cannot match `case=G<n>`, so a summary-only receipt is excluded by construction. This part of
the freeze holds.

### D2 — BREACH: "graded" is only a line shape; zero-mutant and zero-payload cases pass

The same test set:

```
selftest case=G1 positive=pass mutants=0/0 verdict=pass   -> matches (graded)
selftest case=G2 positive=pass verdict=pass               -> matches (graded; no mutants field)
G1 payload= closed=1                                      -> matches (^G[1-8] payload=.* closed=1$)
```

The predicate's prose says "whose mutants are all rejected"; at `mutants=0/0` that is vacuously true. The kill
rule counts only "fewer than 8 graded case lines or any failure", so eight `mutants=0/0 … verdict=pass` lines and
eight empty payloads satisfy the frozen text. The r38 suite itself emits `mutants=0/0 … verdict=pass` lines in its
own forge cases (`corpus/instruments/r38-closure.sh:1403`), so the shape is producible without testing anything.

### D3 — BREACH: the eight checks do not close R1–R4 by enumeration

Exact frozen text: ``Its eight checks close the routed defects of the round-38 verifier spot-check (… §5: R1, R2,
R3, R4) plus the round-38 instrument attack findings``.

| Routed defect | Check claimed to close it | Actual coverage |
|---|---|---|
| R1 self-referential predicate | G2 | re-encodes it (A1/A2) |
| R2 records overstate C1 at J | (none named) | G3's literal pattern does not match the overstatements |
| R3 positive run not committed | G3 | escape hatch "or is explicitly labeled report-only"; report outside scope |
| R4 M38-5/M38-7 lack criteria | (none named) | no check reads `QUALITY.md` or `captured-by` |

Measured details:

- R2 text survives: `corpus/lessons/round-38.md:21` says "`closed=8/8 exit=0` … over the judged head are the
  receipt" and `:94` says "`--export-ref J` → `closed=8/8 exit=0`"; `SHONEN.md:185` says "run + selftest over the
  judged head". G3's pattern (`--export-ref <40hex> -> closed=`) matches **0** of lines 21/94 (they use `J` and
  `→`), and 0 in SCORECARD/SHONEN/LOG round-38 text. G1 only checks declared blocks if they are declared; G5 only
  forbids `Final lane commit:` lines. No check requires the `Correction (round 39)` lines.
- R4: `QUALITY.md` cites M38-1 (R32) and M38-2/M38-4 (R33) only; no row cites M38-5 or M38-7 (`grep -nE 'M38-[0-9]'
  corpus/QUALITY.md` -> lines 291–292 only). None of G1–G8 reads QUALITY or `captured-by`.
- R1 provenance: the r38 receipt cites "round-38 lesson, M38-8", but no M38-8 row exists at `6c0ae18`, `f06148c6`
  or `480b1a5` (`grep -cE '^\| M38-8'` -> 0 at each). The r38 lesson has M38-1…M38-7 only, consistent with the
  verifier's "R1 … not mined".

### D4 — BREACH: G1, G4, G5 and G7 are vacuous at zero; G6 is hygiene; G8 is a carry-over

- **G1** (exact: ``every declared appended block … matches … the declared line count equals the added-line count
  of `git diff <base> J -- <path>` … corrections count only outside fences … every declared path exists``): an
  empty `declared-blocks.txt` satisfies every clause (zero declarations, zero corrections). It does not require
  every changed path to be declared. Model on a fixture where README gained 5 lines with zero declarations:

  ```
  G1 model: declared-blocks=0 declared-ok=0/0 -> closed=1 (vacuous)
  actual added lines in README: 5 (undeclared, never checked)
  ```

  So R2's corrections can simply not be made and G1 still closes.
- **G4** (exact: ``for every tracked `.ufo/waves/round-39/*-dispatch.json` in the export the sibling
  `-results.json` parses as JSON, lists exactly `len(taskCall.tasks)` seats with distinct agent ids (a zero-task
  dispatch is RED)``): zero tracked dispatch files is vacuously true. Base has 0; a round that never commits the
  dispatch passes. "Zero-task" is not "zero files".
- **G5** (exact: ``the SCORECARD.md `## Round 39` section and SHONEN round-39 lines contain zero `Final lane
  commit:` lines and name the judged head only by reference``): with no `## Round 39` section there is nothing to
  contain a label, so the zero-label clause is vacuously true; the "name the judged head" clause is
  implementation-dependent (presence is not stated).
- **G7** (exact: ``carries a `## Round-39 dispositions` section at/after the round-38 section with one row per
  proposal mined this round and a `Correction (round 39)` line``): "one row per proposal mined" is vacuous at
  zero proposals; an empty section plus one Correction line passes. The anchor is also undefined: the ledger has no
  section named `Round-38` —

  ```
  18:## Limits
  22:## Round-31 status flips (appended 2026-10-25)
  37:## Round-37 dispositions (appended 2026-10-26, R31 home)
  41:## Re-pin note (appended 2026-10-26)
  45:## Round-37 dispositions — filled (round 38)
  ```

  The round-38 work filled the `Round-37` section; "the round-38 section" cannot be located by heading name.
- **G6** (exact: ``under the scratch root `kasegi-r37` and `kasegi-r38` are absent or hold zero entries, and
  `kasegi-r39` holds nothing but this run's own `--work` dir``): hygiene only; it does not measure work.
- **G8** (exact: ``the round-37 suite bytes pinned at … `2387dcf6…` … end `closed=14/14 exit=0`; the export's own
  copy of r37-closure.sh must hash to the pinned digest``): a carry-over. Pinned digest measured
  `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`, identical at base `480b1a5`; it re-proves
  round-37, not round-39.

### D5 — BREACH: the do-nothing path to 8/8

No real fix is needed. The minimal green round:

1. `declared-blocks.txt` empty (G1 closes; no corrections, no appends).
2. A hand-written `all-gates.txt` at the tip Y naming J, with the eight `G<n> payload=` lines, the eight
   `selftest case=G<n> … mutants=0/0 … verdict=pass` lines, `closed=8/8 exit=0`, `selftest cases=8 failures=0`, and
   `suite-sha256` equal to a script that prints exactly this shape. G2 checks shape, ancestry and diff, not that
   the run happened.
3. Two transcript copies for the pre-existing SCORECARD:1434/1435 quotes (G3), or retro-labels; the r38
   overstatements stay.
4. `wave1-dispatch.json` + `-results.json` with distinct ids (G4; the round dispatches seats anyway).
5. `## Round 39` text in SCORECARD/SHONEN with a by-reference head line and no `Final lane commit:` (G5).
6. Clean scratch at filing (G6).
7. `## Round-39 dispositions` with zero rows + one `Correction (round 39)` line (G7).
8. The pinned r37 suite, unchanged (G8).

Base stays red only because the receipt and ledger section are absent; the r38 red control is dead (B2). The C2
counters are met with three S-rows (58), a junk F-row, and a one-line knowledge file. Nothing in the frozen
commands would detect that no routed defect was closed.

## Smallest safe corrections (spec edits, before the suite lands)

1. **Name Y for the positive run.** Change counting commands 1–2 to `--export-ref <Y>` and keep the receipt's
   `export-ref=J` (G2 already checks `git diff J Y` = receipt only). If the frozen text must keep J, then G2 must
   be graded from the tip, not "in the export". Also change the head-rule sentence to "no lane file at or before J
   names J by hash; the receipt at Y records it" (A3).
2. **Fix the r38 head literal.** Replace both occurrences of `66703aca50529a35be49aa8759d04140720ad` with
   `66703acaaff50529a35be49aa8759d04140720ad` (B2).
3. **Fix the registry expectation.** Set it to **59** (55 + S057 + S056 + S058 + S059), or restate the predicate
   to add three rows so 58 is correct (C1).
4. **Bind the counters to content.** Require the F22 row's URL
   `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`, the S057 row `NF=13` and
   `status mined`, the S056/S058/S059 rows `status rejected` with a `flip:` token, and at least one substantive
   line in the S057-citing entry (or gate the entry on QUALITY Q1–Q6 in a counting command) (C2).
5. **Grade "graded".** Require `mutants=n/n` with n ≥ 1 in every `selftest case=G<n>` line (and the kill rule),
   and require named payload fields rather than `payload=` (D2).
6. **Add the missing checks.** One counting command for the R2 corrections (`grep -c '^Correction (round 39)'` in
   each of SCORECARD/LOG/SHONEN/round-38.md), one for R4 (a QUALITY row citing M38-5 and M38-7, or the missing
   record), and a G7 minimum row count ≥ 1 (D3/D4).
7. **Scope G3.** Restrict it to round-39 text (or explicitly exempt the historical SCORECARD lines as
   pre-existing); drop the "report-only" escape for the judged-head run; include the report file if report quotes
   are to be graded (A4).
8. **Fail-closed minimums.** G1: require the declared set to cover every changed path (or at least one
   declaration); G4: require at least one tracked dispatch; G5: require the `## Round 39` section to exist; G7:
   anchor on the existing `## Round-37 dispositions — filled (round 38)` heading or require a real
   `## Round-38 dispositions` heading (D4).

## Impacted axes

- **depth:verifiability (4, held)** — C1 cannot verify as frozen: commands 1–2 are unsatisfiable at J (A1), the
  bootstrap path falsifies provenance (A2), the r38 red control cannot run (B2), and R2/R4 are not covered (D3).
  The freeze must be corrected before the suite lands, or the judge will have to kill C1 exactly as in round 38.
- **coverage (7, held)** — C2's registry counter is off by one (C1) and every counter is format-only (C2); a
  compliant tree scores 59 against a frozen 58, and a non-compliant tree can hit 58. Not verifiable as frozen.

## Tooling / scratch

No installs, no upgrades, no pacman. Scratch `/fast/scratch/hyaku/kasegi-r39/CritFreezeAudit/` created with
`mkdir -p`, all fixtures under it, removed before yield. Disk guard green at start (`/fast/scratch/hyaku` 25% use,
609.5G free). No git mutation in the lane or fleet; all fixture commits were inside
`$S/fix`, `$S/fix2`, `$S/g1` with `git rev-parse --show-toplevel` asserted equal to the fixture dir and a local
throwaway identity.
