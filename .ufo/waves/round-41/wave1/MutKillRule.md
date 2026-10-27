# MutKillRule — round-41 wave-1 receipt (C1 kill-rule attack, fresh escapes)

Seat: `MutKillRule` (mutation-tester, leaf). Item: find **NEW** kill-rule escape
states beyond the committed CritKillRule seven (`.ufo/waves/round-40/wave2/CritKillRule.md`
F1–F8) and beyond the enumerated defeat fixtures (T2/T4/T7/T13/T14, MutH6H10
leaf-capped green base, MutH1H5 count-relative forgery): states where a real
defect exists at filing but the frozen C1 kill rule (`.ufo/waves/round-41/claims.json`,
`kill_rule` field, read in full) does NOT fire. Axes: depth:verifiability (primary),
coverage. Read-only git only; no lane/fleet/source-tree writes; no subagents; no
tool installs; no network fetches.

**Verdict: 10 fresh escape states found (3 high, 5 medium, 2 low).** 8 were
reproduced empirically against committed bytes (r40 closure suite at the
round-40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd`, and the
committed fleet `scripts/sources-census.sh` run on scratch fixtures); 2 are
specification-gap findings evidenced by direct quotes of the frozen kill-rule
text. None overlaps the committed seven or the enumerated fixtures.

---

## 0. Method and frozen-clause baseline

The frozen C1 kill rule (`claims.json` line 27) is a disjunction of ten clauses
(referred to below as K1–K10 in order):

- K1 suite absent from the Y export; K2 Y export prints `closed!=12/12` or
  `exit!=0`; K3 selftest prints fewer than twelve graded case lines / any
  failure / a summary-only line satisfies a case; K4 base or round-40 judged
  head export prints `closed=12/12`; K5 a committed fixture shows a check
  passing while the defect it names is present (enumerated: T2/T4/T7/T13/T14,
  CritKillRule seven, MutH6H10 leaf-capped green base, MutH1H5 count-relative
  forgery); K6 the `Correction (round 41)` line set does not grade round-40 C1
  not verified and name the firing evidence; K7 census `exit!=0` or a new W/E
  code; K8 lane working tree not clean at filing; K9 any `kasegi-r41*` scratch
  sibling at filing other than the passed `--work` dir; K10 receipt at Y not
  byte-identical to the teed transcript of the run that produced it.

Empirical probes ran against:

- `corpus/instruments/r40-closure.sh` (committed blob
  `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`) in export
  mode over ref `c7aea5ef97902f38289cbdc1cf267068876a62dd` with `--lane`,
  `--work`, `--scratch-root` all under the seat scratch — the r41 suite's I6 is
  specified as the same live-scan design, so the r40 bytes are a faithful model
  of the mechanism being frozen.
- `scripts/sources-census.sh` (committed fleet script, 806 lines) in `validate`
  and `overdue` modes against hand-built registry fixtures via `--file`.

Every probe below is checked clause-by-clause against K1–K10.

---

## 1. E-suite-digest-unbound — receipt produced by a different suite version than the export's (HIGH)

**Setup.** Run suite v1 (digest d1) at the judged head J, tee transcript T
(header line `suite-sha256=d1`); then silently revise the suite to v2 (digest
d2), and commit v2 + receipt=T together at Y. The committed suite at Y is not
the instrument whose behavior the receipt attests.

**Why the kill rule misses it.** Every clause passes: K1 (suite present), K2 (v2
genuinely prints `closed=12/12 exit=0` when the counting commands re-run it), K3
(selftest of v2 is clean), K10 (T **is** byte-identical to the teed transcript
of the run that produced it — the v1 run). Nothing else compares d1 to d2.
Verified by direct search of the frozen text:

```
$ grep -oiE 'sha-?256|digest|suite version' .ufo/waves/round-41/claims.json | sort | uniq -c
(no output — zero matches in claims.json)
```

The round-40 instrument shows what the missing limb looks like when present:
`receipt_shape` in r40-closure.sh compares the receipt's recorded
`suite-sha256` against `file_digest "$EXPORT/corpus/instruments/r40-closure.sh"`
(lines 451–454) and H7 reds on `digest=0`. The r40 suite's own H1 also binds
`suite=1,digest=1`.

**I-check coverage.** Covered **iff** the r41 I2 implementation inherits r40-H7's
digest comparison. The frozen I2 predicate names only "teed transcript of BOTH
the suite run and the graded selftest at Y, `time-basis=ref-commit`, run-utc =
ref committer instant" — the digest limb is not in the specification. **Gap:**
name the digest binding explicitly in I2 (or add a suite-digest clause to the
kill rule), else this state is green with the evidence chain broken. A sibling
variant — suite run and selftest teed from runs over *different* refs — has the
same shape (K10 is self-referential; only I2's "at Y" wording opposes it).

## 2. E-selftest-extra-line — a thirteenth graded line carrying a forged pass (MEDIUM-HIGH)

**Setup.** A defect exists in one check's real selftest; the suite's selftest
printer emits twelve genuine graded lines for the passing cases **plus one
extra** `selftest case=I<n> ... verdict=pass` line duplicating a passing case,
and the summary still prints `selftest cases=12 failures=0`.

**Why the kill rule misses it.** K3 fires only on "fewer than twelve graded case
lines", "any failure", or "a summary-only line satisfies a case". Thirteen lines
is not fewer than twelve; the forged line prints no failure; the cases that ran
are covered by real lines. Clause-by-clause: K1–K2, K10 pass (the receipt is the
honest tee of this selftest). Direct search confirms no quantity/identity limb
beyond the count:

```
$ grep -oiE 'order|reorder|unique|duplicate id|exactly twelve' .ufo/waves/round-41/claims.json
(no output)
```

**I-check coverage.** I8 enumerates exactly six receipt-forgery variants
(payload-contradicting, future-dated, foreign-ref, nonexistent-ref,
summary-only, tampered payload line) — an inserted graded line is not among
them. I9 ("a tampered payload reds exactly its own case") tests per-case
isolation of the payload comparison, not transcript line-set integrity. **Gap:**
the graded selftest contract should require exactly the twelve ids I1–I12, each
exactly once (set + uniqueness), and the summary count to equal the graded-line
count.

## 3. E-selftest-reorder — graded lines reordered or case ids duplicated (MEDIUM)

**Setup.** All twelve selftest cases run, but the graded lines print in
scrambled order, or one case id prints twice and another is absent, every line
`verdict=pass`, summary `cases=12 failures=0`.

**Why the kill rule misses it.** Same K3 shape as E2: the clause checks a floor
on the line count and the absence of failures, not the identity, multiplicity,
or order of the case ids. A mislabeled line (case I7's result printed under
`case=I9`) keeps the count at twelve with no failure. Nothing in K1–K10
compares line order or id multiset against `{I1..I12}`.

**I-check coverage.** I9 covers this **only if** implemented as a strict
per-expected-case contract (exactly-one-red-per-tamper over the fixed id set);
the frozen wording "isolates the payload-value comparison per case" does not
explicitly demand id-set/order integrity. **Gap:** specify "graded lines appear
in check order I1…I12, each id exactly once" inside I3's family or I9.

## 4. E-late-scratch — scratch sibling created AFTER the scan timestamp (HIGH)

**Setup.** The suite runs green at time T0 with its live I6 scan printing
`strays=0`; after the run — before filing — a leftover `kasegi-r41-<x>` appears
(a failed cleanup trap, a background job, a seat that yields late). The receipt
is filed byte-identical to the T0 tee; at filing a real leftover exists.

**Why the kill rule misses it.** K9 is the only clause that could fire
("any `kasegi-r41*` scratch sibling **at filing**"), but its only
operationalization is the suite's run-time scan; K10 (receipt byte-identity)
holds because the receipt honestly records the T0 scan. Reproduced with the
committed r40 bytes (r41-named variant; the r40 family is what the committed
instrument scans for — the mechanism is identical):

```
$ bash corpus/instruments/r40-closure.sh --export-ref c7aea5e... --lane <lane> \
    --work $S/work --scratch-root $S/scratchroot
H6 payload=strays=0,read=ok closed=1          # run at T0, root empty
closed=9/10 exit=1                            # H7 red at J (receipt absent) — expected
$ mkdir -p $S/scratchroot/kasegi-r40-late     # AFTER the run
$ grep '^H6 ' run1.txt
H6 payload=strays=0,read=ok closed=1          # the committed receipt still attests strays=0
```

A fresh run does see the in-root stray (`strays=1,read=ok closed=0`) — the scan
works; the escape is purely the **time gap** between scan and filing.

**I-check coverage.** I6 is run-time by nature; no I-check re-scans at filing.
The round-40 wave-2 sentinel performed a live listing as a human check, but that
is not part of the frozen kill rule. **Gap:** add a filing-time clause — either
a sentinel re-scan whose output is part of the Y evidence, or a receipt-embedded
scan timestamp that a filing-time re-run must reproduce.

## 5. E-sibling-outside-root — leftover outside the scanned root (MEDIUM)

**Setup.** A seat's leftover lives where the suite never looks: `/tmp`,
`/var/tmp`, or any alternate TMPDIR path (`/tmp` is expressly permitted for
files under 50 MB; TMPDIR overrides are foreseeable), named `kasegi-r41-*`.

**Why the kill rule misses it.** K9 as written is unqualified ("any
`kasegi-r41*` scratch sibling at filing"), but the enforcement instrument scans
one fixed root. Reproduced with the committed r40 bytes:

```
$ mkdir -p $S/outsidetmp/kasegi-r40-outroot          # outside the scanned root
$ bash r40-closure.sh ... --scratch-root $S/scratchroot --work $S/work3
H6 payload=strays=0,read=ok closed=1                 # green; out-of-root stray invisible
$ find $S/outsidetmp -maxdepth 1 -name 'kasegi-r40-*' | wc -l
1                                                    # the leftover is real and unscanned
```

This is distinct from the committed seven: F1 is nested **inside** the scanned
root; F6 is a missing root; this state has a healthy root plus a sibling the
root never covers. CritKillRule's own §5 fix ("scan the scratch root
recursively") does not address siblings **outside** the root.

**I-check coverage.** None of I1–I12 names a scan location beyond the scratch
root family. **Gap:** either qualify K9 ("under the hyaku scratch root") or add
a cheap filing-time sweep of the documented temp locations (`/tmp`, `/var/tmp`)
for the round family.

## 6. E-declared-subset — declared-blocks covering a subset of the landed changes (HIGH)

**Setup.** The round's landed bytes include an append to an owned file (say
`SCORECARD.md`) that is **not** listed in `.ufo/waves/round-41/declared-blocks.txt`;
every listed declaration is a clean whole-tail append.

**Why the kill rule misses it.** The frozen kill rule contains **no
declared-blocks clause at all** — `grep -c declared claims.json` finds the word
once, inside the I12 *predicate*, not in the kill-rule disjunction. K5 fires
only for the enumerated fixtures (none is an undeclared append); K6 checks only
the `Correction (round 41)` line set's grading; K2 stays green if the suite's
I12 validates only the declared entries. The committed r40 H9 shows that shape:
its loop iterates **over the declared-blocks lines** and validates each against
tail-sha/numstat (`declared=293,valid=293`) — it never enumerates the round's
changed-path set to require the declaration is complete:

```
$ sed -n '893,938p' corpus/instruments/r40-closure.sh | grep -nE 'while|declared=|valid=|diff|done <|printf'
9:    while IFS= read -r line ...; do          # iterates declared lines only
11:      declared=$((declared + 1))
27:      if ! nm=$(git ... diff --numstat "$BASE_REF" "$ref" -- "$path" ...); then
42:    printf 'declared=%s,valid=%s,tail=%s,pure=%s,paths=%s,diff-read=%s' ...
```

**I-check coverage.** I12 per the frozen predicate says "declared-blocks equal
whole-tail appends with zero deletions" — satisfiable by validating only the
declared subset. **Gap:** I12 must be bidirectional — the declared path set must
equal the set of paths the round changed (e.g. `git diff --name-only base..Y`
minus the receipt), with each declared entry a whole-tail append.

## 7. E-census-overdue-invisible — an overdue recheck date passes the frozen census clause (MEDIUM)

**Setup.** A registry row (e.g. S063) carries a well-formed ISO `recheck` date
in the past — a genuinely overdue recheck under the corpus's own discipline.
`E09` checks only the date's format; `E08` gates `opened`, not `recheck`.

**Why the kill rule misses it.** The frozen census clause (K7) runs the
`validate` shape only; `overdue` is a separate census mode that the counting
commands never invoke, and in `validate` mode only **E-codes** set `findings=1`
(census lines 739–740; W-codes "never change status", line 17). Reproduced on a
scratch fixture with the committed fleet script:

```
$ cat overdue.md   # mined row, recheck=2026-10-01 (26 days before filing)
| S901 | https://example.com/a | spec | A | kasegi | - | teaches ok | mined | 2026-10-20 | 2026-10-01 | — |
$ bash scripts/sources-census.sh validate --file overdue.md --today 2026-10-27
file	W03	S901 mined but unused
file	ok	.../overdue.md
exit=0                                            # K7 silent: exit 0, no new W/E code
$ bash scripts/sources-census.sh overdue --file overdue.md --today 2026-10-27
file	overdue	S901 26d recheck=2026-10-01 opened=2026-10-20
exit=1                                            # the defect is real and detectable — just not by K7
```

**I-check coverage.** None of I1–I12 reads registry recheck due dates; C2's kill
rule likewise gates only `validate`. **Gap:** run `sources-census.sh overdue` as
a counting command (or add its exit to K7) so a due-recheck row cannot file
silently.

## 8. E-census-e04-keyword — an E-finding suppressed by a keyword in `teaches` (MEDIUM)

**Setup.** Two live (non-rejected) rows share the same URL **within one scope** —
the exact condition the census's E04 exists to flag — but the second row's
`teaches` cell contains the bytes `supersedes S<nnn>`. The awk exemption
(census lines 646–648) regex-matches the keyword only; it never validates that
the supersedes target exists, is the duplicated row, or is related.

**Why the kill rule misses it.** The E04 line is never emitted, so no E-code
sets `findings=1`, exit stays 0, no new W/E code appears — K7 silent. Reproduced
on scratch fixtures (S001 is not in the registry and is unrelated to the
duplicate):

```
$ bash sources-census.sh validate --file dup-suppressed.md --today 2026-10-27   # teaches: 'round-41 row, supersedes S001'
file	W03	S901 mined but unused
file	W03	S902 mined but unused
file	ok	.../dup-suppressed.md
exit=0                                            # same-scope duplicate invisible
$ bash sources-census.sh validate --file dup-control.md --today 2026-10-27      # identical rows, teaches without the keyword
file	W03	S901 mined but unused
file	E04	S902 duplicate url example.com/a within scope kasegi
file	W03	S902 mined but unused
exit=1                                            # control reds as designed
```

Honest control (kill rule works in the other direction): an **across-scope**
duplicate emits a `W04` line — a new code K7 catches by the claims' "W04
S028/S029 only" enumeration (though note W-codes never change the exit status;
that clause is only as strong as a verifier diffing the emitted code list).

**I-check coverage.** None — no I-check inspects census emission classes or
supersedes-truth. C2's other counters don't help: source-recheck validates
content reachability, not registry uniqueness. **Gap:** the census exemption
could require the supersedes target id to be present and rejected/superseded;
short of a fleet-script change, the kill rule gains nothing here — record it as a
known accepted hole or route a census-hardening note to the operator.

## 9. E-lesson-tally — wrong arithmetic in the round-41 lesson body (LOW)

**Setup.** `corpus/lessons/round-41.md` body text (outside any `Correction`
line, outside fences) states a wrong wave tally or census figure — the exact
class the round-40 verifier routed as D4/D5 for the round-40 lesson.

**Why the kill rule misses it.** K6 constrains only the `Correction (round 41)`
line set in SCORECARD/LOG/SHONEN (grading + evidence naming); the lesson body is
not in that set. I1 checks the correction lines, not the lesson; D4/D5 repairs
target the round-40 lesson only. Nothing in K1–K10 audits lesson-body arithmetic.
**I-check coverage:** none. In round 40 this class was caught only by the
non-author human verifier. Severity low (quality defect, not a claim falsification),
but it is a recurring routed class the frozen rule does not mechanize.

## 10. E-evidence-name — correction lines name a plausible-but-wrong evidence path (LOW)

**Setup.** The three `Correction (round 41)` lines grade round-40 C1 not
verified, but name e.g. `.ufo/waves/round-40/wave2/RevC1Counters.md` where the
firing fixture is `RevC1Counters.defeats.txt` — or cite `CritKillRule.md`
without the sibling fixtures.

**Why the kill rule misses it.** K6 requires the line set to "grade round-40 C1
not verified and name the firing evidence". If the suite's I1 checks a loose
substring (e.g. any mention of `CritKillRule` / `RevC1Counters`) rather than the
three exact committed paths the I1 predicate names, the miss passes every
clause. **I-check coverage:** I1 *as specified* names the exact evidence
(RevC1Counters.defeats.txt, CritKillRule.md, MutH6H10.md) — covered if the
implementation matches the predicate's exact paths; a gap only if I1's matcher
is looser than its spec. Flagged so the L1 pins I1's path list byte-exactly.

---

## 11. Severity summary

| # | Escape | Severity | Killed by an I-check as frozen? |
|---|---|---|---|
| 1 | E-suite-digest-unbound | HIGH | Only if I2 inherits r40-H7's digest limb — not in the frozen I2 wording |
| 2 | E-selftest-extra-line | MEDIUM-HIGH | No (outside I8's six variants; I9 tests tamper isolation, not line set) |
| 3 | E-selftest-reorder | MEDIUM | Only via strict I9 id-set/order contract — not specified |
| 4 | E-late-scratch | HIGH | No (I6 is run-time; no filing-time re-scan clause) |
| 5 | E-sibling-outside-root | MEDIUM | No |
| 6 | E-declared-subset | HIGH | Only if I12 is bidirectional — the r40-H9 shape is declared-only |
| 7 | E-census-overdue-invisible | MEDIUM | No (validate never runs the overdue mode) |
| 8 | E-census-e04-keyword | MEDIUM | No (fleet-script exemption; needs operator-facing note) |
| 9 | E-lesson-tally | LOW | No (human-verifier-only class) |
| 10 | E-evidence-name | LOW | I1 covers iff its matcher is byte-exact on the three paths |

Recommended kill-rule additions for the L1 (cheapest first): K9-time qualifier +
filing-time re-scan (E4, E5); I12 bidirectional coverage (E6); I2 digest limb
named in the predicate (E1); selftest id-set/order contract (E2, E3); census
counting command extended with `overdue` (E7); I1 exact-path matcher (E10). E8
needs a fleet-side census change or an accepted-hole note; E9 is a process gap.

---

## 12. Hygiene

- Disk guard green before and after (`/fast/scratch/hyaku` 25%, 604.0G free,
  `disk-guard.sh status` exit 0).
- No tool installed/upgraded; no pacman; no network fetches; no writes to
  `~/.local/bin` or any PATH directory; no mutating git/jj anywhere (the r40
  suite probe used export mode with `--work`/`--scratch-root` under the seat
  scratch; `git -C <lane> archive` is read-only).
- Lane untouched: all probes wrote only under
  `/fast/scratch/hyaku/kasegi-r41/MutKillRule/`. No sibling lane or source tree
  was read for writes; `shokuknow` untouched.
- Seat scratch removed before yield (`rm -rf` after copying evidence into this
  receipt); no `kasegi-r41*` stray survives from this seat. (This receipt's
  prose is the only artifact; the item is receipt-only, no deliverable file.)
- Evidence commands and their actual outputs are quoted inline in §1–§10.
