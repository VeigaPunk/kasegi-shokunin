# CritClaims — round-41 wave-1 receipt: frozen-claims attack (C1 + C2)

Seat: `CritClaims` (critic, leaf). Item: attack the FROZEN claims in
`.ufo/waves/round-41/claims.json` (read first; live file carries the L1's freeze
errata of 2026-10-27) before any round-41 data exists. No lane/fleet/source-tree
file was edited; no subagents; no tool installs; no network fetches. Read-only git
on the lane; two scratch clone fixtures under the seat scratch (removed at yield).
Axes touched: **depth:verifiability** (primary), **coverage**.

Corrections applied per L1 note `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md`:
base = 40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (the 38-char freeze
literal resolves to no git object — verified `git rev-parse --verify` rc=128);
I11 = the EIGHT committed CritKillRule states F1–F8 (verified: 8 `### F` headings
in `.ufo/waves/round-40/wave2/CritKillRule.md`; the file's intro prose saying
"7 distinct" is superseded).

---

## Q1 — Can the C1 predicate be satisfied by a suite that does not close the routed defects?

### Attack A (trivially-printing suite): YES at the counting-command level — built and run

Fixture: scratch clone of the lane (HEAD `96dbd5f`, pre-build tree) + a fake
`corpus/instruments/r41-closure.sh` that extracts the export (same harness
interface) and prints green iff the export contains
`.ufo/waves/round-41/final-gates/all-gates.txt`, with `payload=unchecked` on
every I-line — it implements NONE of the I1–I12 semantics (no token-boundary
matching, no fence awareness, no symlink canonicalization, no scratch scan, no
forgery detection, no numeric negative-control comparison, no append-only /
density / census limbs). Fixture J `6d5ee010` (fake suite + three Correction
lines), fixture Y `a603e43d` (J + receipt). All five frozen counting commands
pass:

```
$ bash corpus/instruments/r41-closure.sh --export-ref a603e43d54536bae84c8a0cd177874d304784a9b
I1 payload=unchecked closed=1
... I2..I12 identical ...
closed=12/12 exit=0            rc=0

$ bash corpus/instruments/r41-closure.sh --selftest --export-ref a603e43d54536bae84c8a0cd177874d304784a9b
selftest case=I1 positive=pass mutants=1/1 verdict=pass
... I2..I12 identical ...
selftest cases=12 failures=0   rc=0

$ bash corpus/instruments/r41-closure.sh --export-ref 5b29ea1439450b712581edf5f0f0bf98dfb262ab
closed=0/12 exit=1             rc=1
$ bash corpus/instruments/r41-closure.sh --export-ref c7aea5ef97902f38289cbdc1cf267068876a62dd
closed=0/12 exit=1             rc=1
$ bash corpus/instruments/r41-closure.sh
                               rc=2
```

Conclusion: the five frozen counting commands are jointly satisfiable without
closing a single routed defect. They observe stdout only.

### Attack B (selftest grades its own strings): YES — demonstrated

The fake's `--selftest` prints the twelve graded lines and `cases=12 failures=0`
even on the T2-defect tree `a4df4428` (below): `selftest case=I3 positive=pass
... verdict=pass` with the substring defect present. Nothing in the selftest
output contract distinguishes a run selftest from a printing selftest on a
green-looking tree.

### What actually enforces closure: the kill rule's committed-fixture clause — and it IS exhibitable

Kill rule: "a committed fixture shows a check passing while the defect it names
is present". Exhibit (judge-crafted fixture commit; no suite-side knobs needed
for tree-state defects): planted the round-40 T2 defeat values into the
SCORECARD Correction line and re-ran the fake:

```
$ sed 's/closed=10\/10 exit=0/closed=7\/80 and failures=10/' SCORECARD.md  # committed as a4df4428
$ bash corpus/instruments/r41-closure.sh --export-ref a4df442845d6c8458f4ac84d6824e6e4d00df10e
I3 payload=unchecked closed=1
...
closed=12/12 exit=0            rc=0
```

I3 passes while `closed=7/80` / `failures=10` are present → the kill clause
fires. So the frozen C1 claim is defended NOT by its counting commands but by
the kill rule, exercisable either through the per-case env knobs the build spec
requires the suite to expose (wave-2 exhibits) or through judge-crafted fixture
trees as above. The r40-committed defeat fixtures (T2/T4/T7/T13/T14,
CritKillRule F1–F8, MutH6H10, MutH1H5) pin the exhibits; a cheating suite cannot
author its own easy fixtures for those.

### Hole: D4/D5/D6 have no owning check — the claim "the twelve checks close D1–D6" is false for D4–D6

The frozen I1–I12 enumeration maps D1→I1, D2→I2, D3→{I3…I11}, nothing→D4/D5,
D6-adjacent→I7 (the **r41** row only). Verified open at base
(5b29ea1439450b712581edf5f0f0bf98dfb262ab): round-40 lesson L27 garbled census
line, duplicated `## Gate` (2 occurrences), and the SKILL.md blank-line table
break (separator L1120, blank L1121, r40 row L1122) all present in the base
export. A suite can print `closed=12/12 exit=0` at Y with all three unfixed and
no kill clause fires: no instrument reads lesson prose (census reads SOURCES.md
only), I12's SKILL.md limb is append-only, and I7 examines only the r41 row.
Closure of D4–D6 therefore rests on the L1 landing seat RevD4D5D6's erratum /
tally / table-repair bytes (build spec) plus judge inspection — not on any
frozen check. Seat MutDesign is tasked with exactly this orphan matrix.

- **predicate hole: no I-check limb names the D4 lesson erratum, the D5 tally
  fix, or the D6 r40-row repair. Smallest safe correction:** extend I1's
  required byte set (or add a thirteenth assertion) to grep the landed erratum /
  tally-fix / corrected-table-block appends; until a round can do that, the
  canonical judge must verify D4–D6 closure by direct tree inspection. The
  rest of the C1 enforcement core holds (below).

## Q2 — Is the C1 kill rule self-referential or unsatisfiable (the r38 M38-1 class)?

M38-1 definition (r38 spotcheck R1): a frozen counting command "is dry-run over
a stand-in head before freeze and must be satisfiable by a commit that cannot
name itself."

- **Not the M38-1 class.** No stand-in head exists: `r41-closure.sh` exists
  nowhere yet (verified absent at lane HEAD `96dbd5f`), the do-nothing control
  `c1-controls/do-nothing.txt` shows the counter red at base (exit 127, suite
  absent), and the literal command 3 was re-run on the real lane just now:
  `bash: .../r41-closure.sh: No such file or directory; rc=127`. The commands
  are forward-looking, and the before-control pins red-at-base.
- **Self-reference: I2's receipt clause is satisfiable under one forced
  reading.** The receipt at Y is produced by a run at J (it cannot be produced
  at Y before Y exists), so `run-utc` must be the committer instant of the
  receipt's recorded `export-ref` (J), not of the `--export-ref` argument (Y).
  The predicate text "run-utc equal to the ref's committer instant" is
  ambiguous between the two, and the stakes are real: fixture J %ct=1793089930
  vs fixture Y %ct=1793089943 (13 s apart) — a judge coding `run-utc ==
  committer(Y)` fails every honest build where a second boundary falls between
  the two commits. The J-reading is forced by `time-basis=ref-commit`, the r40
  v4 receipt contract this round inherits, and the production chicken-and-egg.
  **Ambiguity flagged; safe reading: the ref named by the receipt's own
  export-ref line.**
- **Freeze typo found and corrected (verified):** the original freeze wrote the
  base as a 38-char literal that resolves to no git object (rc=128, reproduced).
  The L1's errata commit `96dbd5f` corrected the live claims.json to the
  40-char hash (same commit, prefix 5b29ea14) and added the guard that a suite
  must report an unresolvable `--export-ref` as a distinct red (`ref-not-found`
  in payload), never a vacuous `closed<12/12 exit=1`. My fake printed exactly
  that vacuous red for the 38-char literal (`fatal: not a valid object name` →
  `closed=0/12 exit=1`), demonstrating the failure mode the errata punishes.

## Q3 — Can the C2 target be reached by a do-nothing or junk control?

### Do-nothing: NO — baseline reproduced exactly on the freeze tree

`frontier 23 / F24 rows 0 / registry 62 / S063 rows 0 / entries citing S063 0 /
knowledge 59 / harness entries=26 pass=26 / binding records=54 bound=54 /
audit lines=59 expected=59 / census exit 0 (W04 S028/S029 only)` — all nine
frozen counting commands re-run on a pristine clone of the freeze tree match
`c2-controls/before.txt` byte for byte.

### Junk twin (r40 O4 class): NO — flips the two row-level counters only, then dies

Appended a mined-marked S063 row with no capture, no manifest record, no entry
(clone fixture, committed):

```
cmd2 registry rows   62 -> 63     FLIPPED by junk alone
cmd3 mined S063       0 -> 1      FLIPPED by junk alone
cmd4 entries citing S063  0       (entry missing — holds)
cmd5 knowledge files     59       (holds)
cmd6 harness      entries=26 pass=26, no PASS F24   (holds)
cmd7 binding      records=54 bound=54 unbound=0     (holds; binding is record→row
                   direction only, so the junk row adds nothing to fail — it simply
                   never reaches the 55/55 after-state)
```

Defense-in-depth: the sources census also trips — the junk row appended after
the registry section prints `E12 S063 row outside Registry section` and the
census exits 1 (verified, `rc=1`); placed inside the registry with `used-by = —`
it would trip a **new W03** instead. Either way the kill clause "census exit!=0
or a new W/E code" fires.

### Carried fabrication class (r40 Variant C): structural counters reachable, provenance is the only differentiator

r40 wave-1 seat CritC2Junk proved Variant C — self-authored captures + fake
fetch metadata — reaches every structural numeric target (source-recheck 0,
binding 51/51, census 0) and was ruled "freeze defect/risk, not a legitimate
pass": the counters establish internal integrity, not provenance. Round 41's C2
predicate carries exactly the same instruments and the same limit; its kill
rule covers only the no-evidence junk twin. This is a carried, adjudicated
tradeoff, not a new hole: the L1's real fetch (ExecC2Capture records HTTP
status, bytes, sha256, UTC time) and the report ledger are the discernment
backstop. Correction carried from r40: require independently corroborated
URL/access-date/quote provenance for mined rows in the report; a digest and a
local recheck prove consistency, not provenance.

- **predicate holds** for C2 against do-nothing and junk controls (proven by
  execution above); the fabrication class is judge-discerned, unchanged from
  the r40 ruling.

## Q4 — Universal clauses the counting commands do not enumerate

C1 kill clauses with **no frozen counting command**:
1. `census exit!=0 or a new W/E code` (C2 has cmd9; C1 has none).
2. `the lane working tree not clean at filing` — host state, filing-time only.
3. `any kasegi-r41* scratch sibling at filing other than the passed --work dir`
   — host state, filing-time only.
4. `the receipt at Y not byte-identical to the teed transcript of the run that
   produced it` — commands 1/2 print a fresh transcript; nothing enumerates the
   `cmp` against the committed file.
5. `a committed fixture shows a check passing while the defect it names is
   present` — no command; it is the judge's exhibit construction (workable, Q1).

C2 kill clauses with **no frozen counting command**:
1. F24 `status cell not admitted` — cmd1 counts `^\| F[0-9]+ \|` rows
   regardless of status (demonstrated: a `queued` F24 row yields 24).
2. Entry provenance trio `source:/verified-at:/recheck:` — cmd4 greps only
   `^source: S063`; `verified-at:` is never enumerated (`recheck:` is partially
   covered corpus-wide by recheck-audit's count).
3. `any tracked deletion in corpus paths` — no command (would be a git
   name-status diff).
4. `the measure reading below 1.000` — the r22 measure (20+F_admitted)/
   (20+F_total) = 44/44 appears in the predicate and after-state but NO
   counting command computes it.

## Q5 — Ambiguous counting commands (same sentence, different code)

1. **C1 cmd3/4 `-> closed<12/12 exit=1`**: at base / r40J the suite file is
   absent → bash exit 127, no closed line (verified on the real lane). Literal
   exit==1 vs any-red are different code. The before-control documents 127 and
   the kill rule is phrased positively ("prints closed=12/12"), and r40 used
   identical phrasing and passed — the lenient reading is the precedent-safe
   one. Flag only.
2. **C1 cmd1/2 result strings**: substring vs full-line anchoring
   (`closed=12/12 exit=0` as the last line vs anywhere in an I-line payload).
   Prior-round receipts anchor exact lines. Safe fix: full-line, last-line.
3. **C1 I2 predicate `run-utc equal to the ref's committer instant`** — J-vs-Y
   ambiguity, demonstrated stakes (13 s between fixture J and Y commits);
   forced safe reading: the receipt's recorded export-ref (Q2).
4. **C2 cmd1 `grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 23 -> 24`**: counts
   F-shaped rows ANYWHERE (demonstrated: an appendix row counts). Satisfiable
   by a non-admitted or misplaced row; the kill rule carries the intent.
5. **C2 cmd5 `ls corpus/knowledge/*.md | wc -l -> 59 -> 60`**: any new top-level
   .md satisfies it (demonstrated: `junk-probe.md` → 60) — note also cmd4
   counts any file recursively (`grep -r`) while cmd5 counts only top-level
   `*.md`, so cmd4 and cmd5 can diverge on a forged non-.md or nested entry;
   the named-entry limb is enforced only by the kill rule.
6. **C2 cmd8 environment sensitivity**: recheck-audit's 59 recheck lines
   hardcode the real lane root as `cdroot`; on any scratch copy 58 lines print
   `cdroot_fail` and the summary reads `exit=1` even in the honest before-state
   (verified). The frozen `expected=60` command is only meaningful run at the
   real lane root — harmless, but the judge must run it there.
7. Property worth noting (not a defect): cmd6's harness counts only
   `admitted`-status rows as entries (verified: my queued F24 row left
   entries=26), so cmd1 (row count) and cmd6 (admitted entries) measure
   different sets; the kill rule and the harness agree on the status limb.

## Verdicts

- **C1 (depth:verifiability): predicate holds** for the I1–I12/I2 enforcement
  core — the printing-suite, fake-registry-row, and self-grading-selftest
  attacks all die on the kill rule's committed-fixture clause, which is
  exhibitable (Q1), the kill rule is satisfiable under the forced J-reading and
  is not the M38-1 class (Q2), and the base-hash freeze typo is corrected and
  verified. **Predicate hole: the D4–D6 closure limb is missing from the check
  enumeration** (exact limb + fix in Q1); plus two judge-facing ambiguances to
  code safely (run-utc ref identity; exit=1-vs-127 / substring-vs-line
  readings) and five unenumerated universal kill clauses (Q4) that need
  judge-side or report-side execution.
- **C2 (coverage): predicate holds** — do-nothing and junk controls provably
  cannot reach the after-state (transcripts above; census E12/new-W03 as
  backstop); the only structural reach is the carried r40 fabrication class,
  which the r40 canonical ruling already adjudicated as discernment, not a
  counting pass. Unenumerated kill clauses (F24 status cell, provenance trio,
  tracked deletions, the 1.000 measure) and the cmd1/cmd5 ambiguities need
  judge-side enforcement.

Impacted axes: depth:verifiability (primary), coverage. No axis harmed; no
file outside the seat receipt/scratch touched. Scratch dir removed at yield.
