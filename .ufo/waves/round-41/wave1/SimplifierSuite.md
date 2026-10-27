# SimplifierSuite — r41 suite design: duplication map

Seat: `SimplifierSuite` (simplifier, leaf — no subagents). Item: review the r41 suite design
(claims.json I1-I12 + ExecSuiteCore's deliverable if present), find limbs that duplicate without
discriminating, and propose the minimal 12-check structure with one defect class per check. Axes
touched: **depth:verifiability** (primary), **coverage** (read-only). Receipt-only: I land no bytes and
edit no file except this receipt.

Bytes reviewed (authoritative): `.ufo/waves/round-41/claims.json` as it stands in the lane working tree
at read time, sha256 `1071c20594dcac01856f0a6625f7f0c614eacf3384d337e4e76b4df941369925`
(`git status` → ` M`, `git diff --stat` → 36 lines, 25 insertions / 11 deletions: the L1's two
mid-wave errata — base literal 38→40 hex, I11 escapes 7→8 — plus a `\ No newline at end of file`
tail). I also read the freeze-state text (commit `fbba3d9`) through `git diff` so the errata delta is
visible. `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` is treated as authoritative for those two
items.

ExecSuiteCore's suite deliverable was **not present** at read time (`ls .ufo/waves/round-41/wave1/`
held 23 files — 22 seat outputs plus `swarm-registry.json` — none named `ExecSuiteCore*`; no
`corpus/instruments/r41-closure.sh` in the tree, no untracked copy). The review therefore runs over the frozen predicate/kill-rule text, the wave-1
executor briefs in `.ufo/waves/round-41/wave1-spec.json` (the design's operative form: the I-limb
briefs are what the suite core will implement), and the committed r40 suite the r41 suite inherits.
If ExecSuiteCore lands a contradictory structure, §3's ownership table still applies; the sentence
proposals in §4 are the L1's to freeze.

---

## 1. Method and evidence run

Read-only: `git rev-parse/cat-file/log/show/diff/status`, `grep`, `awk`, `sed`, `sha256sum`, `python3 -c`.
No mutating git anywhere. No lane/fleet/source-tree writes. No network. No tool installed (nothing
needed; pacman is paused host-wide and was not touched). Disk guard green before the pass
(`bash scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku` 25% used, 610.2G free).

The seat role asks for `lsp` references as semantic proof of a deletion candidate. **No `lsp` device is
mounted in this seat** (`read xd://lsp` → "No such tool"; the mounted device list carries `ast_edit`,
`debug` and the MCP families only), and no language server indexes `claims.json` prose in any case.
Every reference count below is therefore **literal grep, not semantic proof**, and is labelled so.

E1. Round-40 suite limb inventory and defect anchors (`corpus/instruments/r40-closure.sh`, 1734 lines):

```
555 check_h1  suite present + digest + registry row (SKILL.md or instruments README)
587 h2_scan   fence-aware pass over a record; line 594:
              if (index(s, "closed=7/8") > 0 && index(s, "failures=1") > 0) named++
607 check_h2  corrections named with final values  (=> the T2 substring defect)
625 check_h3  criterion rows: mentions=...,rows=... (mention-without-criterion-row fixture)
689 check_h4  Gate-block quality: url/date/location/quoted span (s056/s058/s059/oversize)
715 check_h5  receipt: control=payload_matches n/8, forged-payload, future-dated, summary-only
760 check_h6  scratch scan: line 771 find -mindepth 1 -maxdepth 1 ; line 769 if [ -d "$root" ]
              byte-literal `case $b in kasegi-r39*|kasegi-r40*)` ; raw prefix `"$r"|"$r"/*`
797 check_h7  receipt re-derivation + canonical rebuild + cmp
855 check_h8  negative controls: line 861 R40_LEAF=1 -> return 1 ; line 886 [ "$b" -lt 10 ]
890 check_h9  declared blocks: path_safe (line 348, components only, no symlink resolution),
              tail sha256, numstat add==lines && del==0
942 check_h10 numstat / name-status diff
```

E2. Helper sharing inside that suite (literal `grep -c`, occurrences of the name including its
definition and doc comment, **not** semantic references): `payload_matches` 5 (definition + `h7_inner`
line 546 + three calls in `check_h5` lines 728/732), `receipt_shape` 8 (definition, doc comment, and
calls in `check_h5`/`check_h7`), `kv_get` 28, `h2_scan` 3, `path_safe` 3, `h4_code` 3. The value matcher and the receipt reader are **shared
primitives** consumed by two limbs each — which is why a single mutant cascades (MutH1H5 observed
`closed=7/10 exit=1` with H5/H7 payload-match reds from one patch).

E3. Escape-state count in the committed attack receipt:
`grep -cE '^### F[0-9]' .ufo/waves/round-40/wave2/CritKillRule.md` = **8** (F1-F8), while line 9 of the
same file says "Verdict: 7 distinct escape states reproduced" and §4 groups F1/F2 (and F3/F4 for
remediation only). The L1's erratum now freezes **escapes=8, red=8, naming F1-F8** — the predicate
sentence still says "seven" (§2 S4).

E4. Attack tallies, derived from the committed dispatches (`wave1-dispatch.json` 54 members,
`wave2-dispatch.json` 35 members, roles counted from `registry.members`):
wave 1 = reviewer 12 + critic 3 + mutation-tester 2 = 17/54 = 31.5%; wave 2 = 12 + 7 + 6 = 25/35 =
71.4%; round = 42/89 = 47.2%. `corpus/lessons/round-40.md` line 9 says "wave 2 33/35 = 94%; round
total 50/89" (D5).

E5. `corpus/lessons/round-40.md` structure: line 29 and line 31 are both `## Gate` (D4); line 27
reads "tier A +3?mined S016/…flips)" — a `?` mojibake and an unbalanced `)` (D4).

E6. Live-vs-stale values, measured on the landed correction draft
`.ufo/waves/round-41/wave1/ScribeCorrections.full-blocks.txt` (10 `Correction (round 41)` lines in 3
blocks of 4/3/3):

```
substring 'closed=7/8'  : 2   (both are substrings of the quoted bait 'closed=7/80')
substring 'failures=1'  : 2   (both are substrings of the quoted bait 'failures=10')
substring 'closed=10/10': 4
token (field-equality) 'closed=7/8'   : 0
token 'failures=1'                    : 0
token 'closed=10/10'                  : 4
token 'exit=0'                        : 4
lines whose token set contains 'closed=7/8' : 0
per block: with_closed1010 = 1 / 1 / 2 of 4 / 3 / 3 lines
```

E7. Census clause present in **both** claims: C1 kill_rule `" census exit!=0 or a new W/E code"`,
C2 kill_rule `" census exit!=0 or a new W/E code"`; the census counting command exists only under C2
(`bash …/sources-census.sh validate --root … kasegi -> exit 0`).

E8. D3's own item list, from the C1 `before` array: "D3 (H1/H2/H3/H5/H6/H7/H8/H9 instrument survivors
+ 7 CritKillRule escape states)". D3 names r40 **H3** (criterion-row limb); no I-check's sentence
asserts criterion-row *existence* (I4 owns only the fence half, I7 only the SKILL registry row).

E9. Deliverables read for design intent: `ScribeCorrections.full-blocks.txt`, `ScribeLesson.lesson.md`
(the r41 lesson still carries `## Gate` source blocks with URL/access-date/quotes and a `Mistakes`
table with an `able to fail` column), `ScoutKillRuleSpec.txt` (seven = F1/F2 merged + F3-F8, i.e. it
**includes** F7), `CORRECTIONS-L1.md`, `CritReceiptUtc.md` (I2 time-basis limbs all hold).

---

## 2. Findings — limbs that duplicate without discriminating

**S1 (largest). `I12` is a six-clause grab bag with three duplicate authorities, so it discriminates
nothing on its own.** I12 currently asserts: (a) "the negative controls are red at base and round-40
judged head"; (b) "declared-blocks equal whole-tail appends with zero deletions"; (c) SKILL/PROVINCE
append-only; (d) density.py byte-identical; (e) no tracked deletion; (f) "the sources census exits 0".
(a) is asserted three times over — by I10's killability clause and by C1 counting commands 3 and 4
(`--export-ref <base>` and `--export-ref c7aea5ef…` → `closed<12/12 exit=1`). (f) is asserted in C2's
predicate, C2's kill_rule and C2's counting command (E7): the same instrument, one owner too many.
(b)/(e) are the two halves of r40 H9's tail/purity limb; (d)/(c) are diff-shape. My move: (a) → I10,
(f) → C2 only, and I12 becomes one class, **append-only repair with zero deletion**, which is also the
only free slot for the routed defects D4/D5 (S5 below).

**S2. `I3` and `I9` overlap at the payload-value primitive; the residue must be partitioned, not
merged.** I3 (whole-token value matching) and I9 (per-case payload isolation) share the matcher
(E2: one `payload_matches` helper, two consumers). They *are* separable if I9 owns **attribution**:
MutH1H5's committed cascade evidence (one patch reds H1 + H5 + H7 together) is exactly the defect
class "a tamper is not attributed to one case". A token-boundary matcher can still cascade; a
cascading harness can still be token-bounded. So: keep both, and freeze the partition in §5. If the L1
insists on one slot, the merged sentence is:
"I3/I9 the value limb: a payload value is compared as a whole token (`closed=7/80`, `failures=10`
reject) and a single tampered value reds exactly its own case, no sibling case" — but that drops the
cascade falsifier's ownership and I recommend against it.

**S3. `I8` and `I2` do not duplicate as checks; their *fixtures* do.** CritReceiptForge's six variants
are the committed evidence (§ table, `CritReceiptForge.md` lines 276-283): a (forged payload) and
h7line red H5 `control=7/8` + H7 `payload-match`; b (future utc) reds `utc=0`/`not-future=0`; c1
(foreign ref) and c2 (nonexistent ref) red H7 `diff-clean`/`ancestor` and leave H5 green; d
(summary-only) reds H5 `control=0/8` + H7 `run-lines=0`. Four of the six are **I2's clause
negatives** (ref binding, committer instant, transcript shape), two are **I3's value negatives**.
I8's only residue is **independence** (MutH1H5 M-H5 count-relative class). Freeze: the six variants
are I2's and I3's mutant sets; I8's own mutant is the count-relative detector, and I8 asserts per-flag
predicates. Otherwise the same fixture is counted twice and I9's cascade clause fires on I8's cases.

**S4. `I11`'s count literal contradicts the frozen erratum, and the build brief contradicts both.**
The predicate still says "each of the seven committed CritKillRule escape states"; the L1 erratum
freezes "eight committed states, `escapes=8 red=8`, naming F1-F8" (`CORRECTIONS-L1.md` §2, claims
`errata[1]`); the wave-1 executor brief `ExecI11KillRule` still enumerates seven and its seven
**omits F7 (pending-marker spelling)** while splitting F1 and F2 (E3, E9). Meanwhile the scout's
canonical table (E9) uses the file's own seven (F1/F2 merged, F7 included). Three counts, three sets.
Consequence: if I11 is built to the brief, F7 has no fixture and no owning limb, and the claim's
`red=8` is unsatisfiable; if built to the predicate, the count is seven and the erratum is violated.
One sentence must name the eight, and F7/F8 must be given owners (S6).

**S5. D4 and D5 have no owning limb, so the predicate's "The twelve checks close … D1-D6" is false
today.** D1 → I1; D2 → I2; D3 → the I3-I10 bundle; D6 → I7; **D4 (duplicate `## Gate`, garbled census
cell) and D5 (attack tally) → nothing** (E4, E5), even though `RevD4D5D6` is drafting the erratum that
lands those bytes. My move: D4/D5 become I12's content — the erratum is the *repair*, and append-only
zero-deletion is the *proof the repair did not rewrite the record*; one class, "round-40 record
repaired append-only".

**S6. F7 and F8 are escapes with no owned limb.** I6's sentence covers F1-F6 and omits **F5's clean
chain** ("tolerates only the single clean chain … down to `--work`"); nothing in I1-I12 asserts the
**pending-marker semantics** (F7) or the **skip-worktree/ignored-file masking** (F8) — the latter was
the r40 kill-rule's *filing* clause, enforced outside the instrument (`closure-prompt.md`), and the
r41 design has no replacement. Fix: I6 gains the clean-chain clause; F7/F8 become I11's repaired-state
clauses (they are escape states, and I11 is the escape-closure check).

**S7. I3's value set is stale against the bytes it must judge, and the bait self-satisfies the
substring matcher.** On the landed correction draft, `closed=7/8` and `failures=1` occur **only as
substrings of the quoted baits** (`closed=7/80`, `failures=10`): 2 lines each, 0 tokens; the live
values `closed=10/10` and `exit=0` occur as 4 tokens each (E6). So an I3 built to the r40 value list
is wrong in both directions: token mode reds the honest landed text; substring mode is **satisfied by
the bait line itself** — a new member of the T2 class that the r41 bytes create by quoting the bait.
I3's required values must be the live ones, with the r40 baits kept as fixtures only.

**S8. I1's precision is unstated: per-line or per-block?** The landed blocks carry `closed=10/10` on
1/4, 1/3 and 2/3 lines respectively (E6). "Each correction line carries the values" would red the
honest text; "each record block names the truth at least once" is what the drafts satisfy. The
predicate must say which.

**S9. I11's ledger must read the selftest's own mutant lines, not re-run the owner fixtures.** The
escape fixtures *are* I6's/I12's mutants. Re-running them inside I11 gives two owners per fixture and
guarantees the cascade I9 exists to kill. I11 should assert: the selftest's `mutant=` lines name
F1-F8 exactly once, each under a case that rejected it (`escapes=8 red=8`), plus the repaired tree
state (S6). Cheap, unique falsifier (drop one mutant line → I11 red, all cases green), no double run.

---

## 3. Minimal 12-check structure (one defect class per check)

Primitives vs state checks. Three checks are **reader primitives** (I3 value matcher, I4 fence line
set, I9 attribution) and exist to prove a shared helper discriminates; nine are tree/state checks.
The count stays **12**, so `closed=12/12`, the twelve graded selftest lines and all five counting
commands survive unchanged.

| # | defect class (one each) | body | closes |
|---|---|---|---|
| I1 | grading correction is written | `Correction (round 41)` lines in SCORECARD/LOG/SHONEN grade r40 C1 NOT verified, name the firing evidence, ≥1 line per block carries `closed=10/10` + `exit=0` as whole tokens, read through I4's line set | D1 |
| I2 | receipt is the artifact of both runs | tee of BOTH the suite run and the graded selftest at Y; `time-basis=ref-commit`; `run-utc` = ref committer instant; own `export-ref`/`suite-sha256` bind | D2 |
| I3 | value equality is whole-token | live values match only as tokens (`closed=10/100`, `exit=00`, `failures=01` do not); r40 baits `closed=7/8`/`failures=1` never satisfied by `closed=7/80`/`failures=10` | T2, F7 |
| I4 | line anchors are fence-aware | correction/criterion lines inside 3-/4-backtick, tilde, nested-marker fences do not satisfy; fence state at EOF CLOSED | T4, H3-fence |
| I5 | declared paths stay inside the export | readlink-canonicalize every declared-block path; must resolve under the export root | T7 |
| I6 | scratch scan is complete and fail-closed | family normal form (case, dot, Unicode separators), recursive to bounded depth, fail-closed on scan error/missing root, clean-chain-only tolerance | T14, F1-F6 |
| I7 | structured rows exist and are well-formed | SKILL.md registry row **and** the r41 criterion row are table rows with structured cells; mention-only fails | T13, D6, H3-row |
| I8 | forgery flags are independent | one predicate per variant, not a count; the count-relative detector mutant reds | MutH1H5 |
| I9 | a tamper is attributed to exactly one case | actual payload values per case; one-token tamper reds exactly its own case, no sibling cascade | H7 non-isolation, D3 |
| I10 | negative-control acceptance is real | nested leaf runs compared by real numerics (`closed<=K<12`, `exit=1`), unresolvable ref = distinct `ref-not-found` red, M-H8a killed | MutH6H10, S1(a) |
| I11 | escape closure | selftest mutant lines name F1-F8 exactly once, each rejected (`escapes=8 red=8`); repaired state holds (no marker in any spelling; no skip-worktree/ignored masking) | CritKillRule, F7, F8 |
| I12 | the repair is append-only, zero deletion | r40 erratum (single `## Gate`, balanced census cell, tallies 25/35 = 71.4% and 42/89 = 47.2%); whole-tail declared blocks; no tracked deletion; density.py byte-identical; SKILL/PROVINCE append-only | D4, D5, H9-tail, H10 |

Every routed item lands exactly once: D1→I1, D2→I2, D3→{I3,I4,I5,I6,I7,I8,I9,I10}, D4/D5→I12,
D6→I7; T2→I3, T4→I4, T7→I5, T13→I7, T14→I6; CritKillRule F1-F8→{I6×6, I11×2};
MutH1H5→{I8 count-relative, I9 H7 non-isolation}; MutH6H10→I10; census→C2 only.

---

## 4. Proposed predicate sentences (the L1 owns the freeze; these are exact replacements)

Fenced because they are proposals, not landable bytes.

```
I1  `Correction (round 41)` lines in SCORECARD.md, LOG.md and SHONEN.md grade round-40 C1 NOT
    verified on the frozen counter and name the kill-rule firing evidence (RevC1Counters.defeats.txt,
    CritKillRule.md, MutH6H10.md), at least one line per record block carrying the receipt truth
    `closed=10/10` and `exit=0` as whole tokens, read through the I4 fence-aware line set;

I3  token-boundary value matching on the live values — `closed=10/10`, `exit=0`, `cases=12` and
    `failures=0` match only as whitespace-delimited tokens (`closed=10/100`, `exit=00`,
    `failures=01` do not), and the round-40 baits `closed=7/8` and `failures=1` are never satisfied
    by the T2 strings `closed=7/80` and `failures=10`, even when a live correction line quotes the
    bait;

I6  the scratch scan matches the `kasegi-r41` name family case- and separator-insensitively (one
    leading dot and Unicode separators normalized), recursively to bounded depth, including
    dot-prefixed and nested entries, fails closed on a scan error or a missing/non-directory
    `--scratch-root`, and tolerates only the single clean chain from a family-named entry down to
    `--work`;

I7  the SKILL.md registry row for r41-closure.sh and the round-41 criterion row (M41-1) are
    well-formed Markdown table rows with structured cells, and a mention without a row does not
    satisfy the limb;

I8  each receipt-forgery variant (payload-contradicting, future-dated, foreign-ref, nonexistent-ref,
    summary-only, tampered payload line) is INDEPENDENTLY flagged by its own clause predicate — a
    count-relative detector (one flag for all six, the MutH1H5 M-H5 class) reds;

I9  the graded selftest attributes a payload tamper to exactly one case: each case compares its
    check's ACTUAL payload values (not the closed bit alone), a one-token tamper reds exactly its own
    case with `positive=fail`, and no sibling case reds through a shared payload-match counter (the
    r40 MutH1H5 H7 class);

I10 the negative-control acceptance predicate is killable: nested leaf-mode runs at base and
    round-40 judged head are accepted only when their own tallies read `closed<=K<12` with `exit=1`
    under a real numeric comparison, an unresolvable `--export-ref` reports a distinct
    `ref-not-found` red rather than a vacuous `closed<12/12`, a leaf-capped green base (the MutH6H10
    M-H8a class) is rejected by that comparison, and the mutation that would accept it is killed by
    the graded selftest;

I11 escape closure: the graded selftest's mutant lines name each of the eight committed CritKillRule
    escape states (F1-F8) exactly once, each under a case that rejected it (`escapes=8 red=8`), and
    the repaired state holds on the tree — no unfinished marker in any normalized spelling
    (`⟨`/`〈`/`<`, optional space, any case, plus `pending`) in the round lessons, and no
    skip-worktree/assume-unchanged entry or ignored-untracked file masking the filing state;

I12 the round-40 record is repaired append-only: `corpus/lessons/round-40.md` carries a single
    `## Gate` heading, a balanced census cell, and the dispatch-derived attack tallies (wave 2
    25/35 = 71.4%, round total 42/89 = 47.2%); every declared-block entry is a whole-tail append
    (`git diff --numstat` additions equal the declared line count, deletions 0); the round diff
    deletes no tracked path; `corpus/instruments/density.py` is byte-identical to base; and
    `SKILL.md`/`PROVINCE.md` are append-only.
```

Sentence-level deletions (the whole point of the seat):

- **delete from I12**: "the negative controls are red at base and round-40 judged head" (owner: I10 +
  counting commands 3-4) and "the sources census exits 0" (owner: C2). Also **delete** the same
  census clause from C1's `kill_rule` — one instrument, one claim.
- **delete from I1**: any claim on T4 (fenced pseudo-row). T4 is I4's alone; I1 consumes I4's line set.
- **delete from I3**: the implied r40 required-value list (`closed=7/8`, `failures=1`) as *values*;
  they survive as *fixtures*.
- **delete from I8**: ownership of the six variants. They are I2's and I3's mutant sets (§5).
- **delete from I11**: the re-run of each owner's fixture. I11 reads the selftest's mutant ledger plus
  the two repaired states.

`kill_rule` additions (five checks currently have no named falsifier — I1, I2, I9, I11, I12):

```
a correction block that grades round-40 C1 verified, or names the receipt without grading it, reds I1;
a receipt holding only the suite transcript (the round-40 D2 shape) reds I2;
a one-token payload tamper that reds two or more cases, or none, reds I9;
an escape state with no mutant line, or a mutant line under a case that accepted it, reds I11;
an in-place rewrite of a lesson line, a tracked deletion, or a skip-worktree/ignored-file change
reds I12.
```

---

## 5. Fixture partition (so no fixture has two owners)

| fixture | owner | evidence it reds only that case |
|---|---|---|
| r40 T2 baits `closed=7/80`, `failures=10`; live-value baits `closed=10/100`, `exit=00`, `failures=01` | I3 | token matcher reds I3; I1 reads the same matcher but the honest block still matches (E6) |
| fenced pseudo-row (T4), 4-backtick correction, EOF-open fence | I4 | I1/I7 stay green because they consume I4's line set |
| symlink declaration outside the export (T7) | I5 | I12 is green (the tail is still a whole-tail append) |
| name-family/depth/dot/fail-open/clean-chain escapes (F1-F6, T14) | I6 | scale of the scan only; I11 reads the *ledger*, not the fixtures |
| mention-only registry row (T13), blank-line-split table (D6), criterion mention without row | I7 | row-shape only |
| count-relative detector (MutH1H5 M-H5) | I8 | one flag for all six variants |
| one-token payload tamper (a, h7line) | I9 | exactly one case reds; I3's matcher green |
| future-dated (b), foreign-ref (c1), nonexistent-ref (c2), summary-only (d) | I2 | the receipt artifact's own clauses; I8 green (its detector still flags each) |
| leaf-capped green base (MutH6H10 M-H8a), unresolvable ref | I10 | nested-run acceptance only |
| drop one escape mutant line; pending marker in another spelling; skip-worktree edit | I11 | ledger/repaired state only |
| non-tail rewrite of a lesson line; tracked deletion; skipped density.py | I12 | diff shape only |

Rule to freeze with the suite: **a fixture reds exactly its owning case.** MutH1H5's committed
cascades (`closed=7/10` with H1/H5/H7 red from one patch) are the evidence that this rule is not
automatic; I9 is the check that polices it.

---

## 6. Pairs examined and deliberately NOT merged

- **I3 vs I9** — matcher vs attribution. Falsifiers are independent: a token matcher can cascade
  (MutH1H5 M-H2), a cascading harness can be token-bounded. Merging loses the cascade owner.
- **I8 vs I2** — detector property vs artifact property. Kept apart, fixtures partitioned (§5);
  merging would make one defect red two cases and trip I9.
- **I1 vs I4** — content vs parser. I4 owns T4; I1 consumes its line set.
- **I5 vs I12** — r40 H9's two halves: containment (T7) vs whole-tail purity/deletion. Distinct
  fixtures, distinct failure modes; keeping them apart is what lets r41 split the r40 limb cleanly
  rather than inherit its compound payload.
- **I10 vs I11** — acceptance predicate vs escape ledger. I10's falsifier is a forged nested run;
  I11's is a missing escape line.

---

## 7. Tradeoffs and open items the L1 should decide

1. **Census is claimed twice** (C1 kill_rule, C2 kill_rule/predicate/command; E7). I recommend C2 as
   the sole owner; leaving it in both is not fatal but it is a second authority over one instrument,
   and C1's I12 would red for a corpus-hygiene reason unrelated to the suite.
2. **The errata are not in the predicate text.** `errata[0]` assigns the "unresolvable `--export-ref`
   reports a distinct `ref-not-found` red" behaviour to **I12**, and `errata[1]` assigns `escapes=8`
   to I11, but the frozen predicate sentences still say neither. A verifier grading the predicate
   text will not find `ref-not-found` anywhere and will grade I11 as seven. My class analysis puts
   `ref-not-found` in **I10** (it is a negative-control read), not I12; either home works, but the
   sentence must carry it. This is the single highest-value one-line edit left in the freeze.
3. **D4/D5 ownership is the only way the "D1-D6" sentence becomes true** (S5). If the L1 prefers a
   pure 12 (I12 without the erratum content), then the predicate sentence must stop claiming D4/D5
   closure and the round-41 lesson must record them as repaired-but-unverified. I recommend I12.
4. **r40 H3 and H4 are silently retired.** D3's item list names H3 (E8) and H4 was MutH1H5's only
   survivor; the r41 I-set carries H3's fence half in I4 and no row-existence half and no Gate-block
   quality limb at all — yet the r41 lesson draft still carries `## Gate` source blocks with
   URL/date/quotes and a `Mistakes` row with an `able to fail` column (E9), so both classes are live
   on r41's own bytes. My §3 folds H3's row half into I7 (D3 already names H3, so this widens
   nothing). H4 has no free slot; if the L1 wants it, the cheapest home is I11's "repair" clause
   (Gate blocks are the record's provenance) — I flag it rather than propose it, because it is new
   scope.
5. **No newline at EOF in claims.json** after the L1's errata write (`git diff` shows
   `\ No newline at end of file`). Harmless JSON; noted because every other wave file ends with LF.
6. **The wave-1 briefs are stale against the errata** for two items (base literal, I11 count).
   `ExecI11KillRule`'s seven omits F7 (S4) — that executor's deliverable will not satisfy the frozen
   `red=8` unless re-briefed or its output is read against F1-F8.

**Stop rule.** The next deletions would harm an axis: dropping I11 leaves the eight escape fixtures
unledgered (a state could be assigned to a limb that does not red it, and `red=8` becomes
unverifiable); dropping I4 re-opens T4 on I1/I7; dropping I3's live-value clause re-opens T2 on the
r41 bytes — because the landed correction blocks quote the bait, a substring matcher would be
satisfied by the evidence line itself (E6). I stop there.

---

## 8. Limits

- No `lsp` device is mounted in this seat; every reference count is literal grep (labelled in §1).
  No claim in this receipt rests on a semantic-reference proof, and none is presented as one.
- ExecSuiteCore's suite was absent, so I reviewed the frozen text + briefs + the committed r40 suite.
  A suite that structurally contradicts §3 changes the shape of the argument, not the ownership
  findings (S1-S9 rest on the committed r40 bytes and the frozen claims).
- I did not run any counting command (no `r41-closure.sh` exists), did not run the census or the r41
  instruments, and did not verify any post-integration value. All measured numbers above are on base
  or wave-1 draft bytes at read time.
- The attack-tally arithmetic (25/35, 42/89) is derived from the committed dispatch registries, not
  from a prose source; recompute if the wave-2 dispatch changes the counts.

## 9. Hygiene

- Writes: this receipt only. No deliverable file (receipt-only item); no edits to claims.json,
  controls, spec/dispatch, docs, corpus, or any fleet/source tree. No mutating git; read-only git only.
- No network fetch (nothing to record: no HTTP status/bytes/UTC). No tool installed or upgraded;
  pacman untouched (paused host-wide).
- Scratch `S=/fast/scratch/hyaku/kasegi-r41/SimplifierSuite/` held the folded claim text used to read
  past the 768-char line truncation; removed before yield, verified with `ls`.
- Disk guard green at start (`/fast/scratch/hyaku` 25%, 610.2G free).
- This receipt is the item's only output: **397 lines**. A file cannot embed its own sha256; the
  digest is reported in this seat's terminal result and recorded by the L1 at commit time. The digest
  that matters for the review itself is the one it targets — claims.json
  `1071c20594dcac01856f0a6625f7f0c614eacf3384d337e4e76b4df941369925`.
