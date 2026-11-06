# CriticClaims — round 80 attempt 1 (kasegi)

Attack seat. Read-only on the lane outside the wave dir; no git/jj writes anywhere; every
measurement below is on the frozen bytes (commit `4ab5458`, `git archive` export into
`/fast/scratch/hyaku/kasegi-r80/CriticClaims/`) or on the committed controls. Scratch is
deleted at hand-off; receipts are copied into `CriticClaims-receipts/`.

**Verdicts (one line each).**
- **C1: NOT FALSIFIED on the frozen bytes** — every predicate that can be executed here is green
  on the byte-pinned candidate and its 28 kills are case-named; but the frozen counter cannot
  distinguish an assertion kill from a self-integrity/location kill, so `killed=28/28` is carried
  by P2 (the sha pin), not by P3 (the tally).
- **C2: NOT FALSIFIED on the drafted entry** — capture fidelity, counts, frontier row and
  distinctness all measure as claimed; but B0–B7 contain no entry-prose limb, so a claims-free
  six-quote dump satisfies them (a r79 carry-in, still open).

---

## (a) Forgery: can a do-nothing or cheap forgery reach killed=28? **Yes — three of four.**

Base is the committed print-stub control `.ufo/waves/round-80/controls/c1-forgery-stub.py`
(sha `7b0c488a…`, scored `killed=0 survived=28` in `controls/c1-forgery-r80.txt`). Each forgery
below is that stub plus a guard; **no assertion from the real selftest is executed for any
mutant**, and every table anchor is left byte-intact so every row derives.

| forgery | added lines | mechanism | frozen counter result |
|---|---|---|---|
| F1 `forgery-F1-location-guard.py` | 6 | FAIL when `__file__`'s parent dir is not `instruments` (the counter copies every mutant into a temp dir) | `baseline=ok rows=28 killed=28 survived=0 dirty=0 notderived=0` rc0 |
| F2 `forgery-F2-selfhash-guard.py` | 7 | FAIL when the body after a sentinel differs from an embedded sha256 (r79's `F-selfhash-forgery` class) | same, `target_sha256=10aeb27e…` rc0 |
| F3 `forgery-F3-sibling-guard.py` | 7 | FAIL when a sibling marker file is absent (mutants are copied alone into a bare dir) | same, `target_sha256=c3bff2b6…` rc0 |
| F4 `forgery-F4-baseline-limb.py` | 6 | prints a FAIL line **and** `selftest cases=15 failures=0`, returns 0 at the landing path | same, `target_sha256=aa9d847c…` rc0 |

Receipts: `CriticClaims-receipts/mutbat-F{1,2,3,4}.txt`. Invocation (identical to P3's, target
only substituted):

```
python3 -B .ufo/waves/round-80/c1/mutbat.py --target <forgery> \
  --table .ufo/waves/round-80/c1/mutant-table.json --expect-cases 15 --work $S
```

**Does the predicate set exclude them?** Only P2 does.
- P1 (`cases=15 failures=0` rc0) — F1 passes (measured at `<land>/corpus/instruments/`, receipt
  `forgery-limbs.txt`); P4 (TMPDIR rc2, no Traceback) — passes; P5 (census `entries=94 … conformant`)
  — passes (the census code is untouched by all four forgeries); P7 (1/1/0) — passes; P8 is the
  counter's own selftest — passes (`mutbat selftest ok … rc0`). P6 is docs-only and independent.
- P3's tally is *identical* for the forgeries, and its printed `target_sha256` differs, so P3 fails
  only on the digest string it shares with P2. **P2 and P3 are therefore not independent limbs**:
  the only thing that keeps the kill number honest is that the frozen bytes were read.

**Why this is a routed defect, not a verdict change.** (i) P2 pins the candidate byte-for-byte, so
no forgery can land; (ii) the frozen candidate's kills *are* causal — the `--keep` run shows
case-named FAIL details, e.g. `gate-regs FAIL registered=[]` (K-M1), `gate-predicates FAIL rows=28
expect=28 bad=[13]` (N26), `gate-negpolarity FAIL neg_ok=False neg_ret_ok=True` (T2),
`gate-wiring FAIL findings=['F4:gate-consume:526']` (T1) (`frozen-candidate-limbs.txt`).

**What is new vs carried in.** The self-hash class was already demonstrated by the r79 critic
(`.ufo/waves/round-79/w1/CriticClaims.md` § (a), `killed=19` with no assertion executed) and r79
routed it; r80 changed the *classifier* (R129) but not this property, and its `do_nothing` cell still
enumerates only base / r79-candidate / print-stub. F1 and F3 are **cheaper than the r79 class**
(no hash to maintain: a path predicate or a sibling existence check), and **F4 is a new limb
defect**: the baseline check is a substring test, so a target that is red on its own pristine bytes
(`selftest case=integrity FAIL …` followed by `selftest cases=15 failures=0`, rc 0) is scored
`baseline=ok`.

**Smallest safe corrections (r81, frozen bytes untouched).**
1. Counter: require each row's FAIL case id to equal the row's declared `expect` case (the table
   already carries an `expect` string per row), or require the per-row FAIL case-id sets to be
   pairwise distinct and to include the mutated case; a single `case=integrity`/`case=location` line
   then cannot score 28 rows.
2. Counter: baseline limb additionally requires *no* `FAIL_RE` match in the baseline output.
3. `do_nothing`: add a guard-forgery control (F1's 6 lines are enough) or reword the cell to
   "no committed control reaches the target".

## (b) Is the axis named by the surface it changes? **Yes — with one drafting gap.**

§9 (`corpus/lessons/round-31.md` §9): name the axis by the surface, not the number; re-scoring a
held rule on new inputs is quality, never depth. C1 does not re-score: the candidate changes the
detector's own enforcement surface (15 cases vs 6 base names; nine r79-routed gaps now have checks;
the counter's classifier rule is new and R129-frozen), which is the r31-admitted sense
("detector soundness under R7/R11/R13", `.ufo/waves/round-31/wave1/RevClaimsFreeze.md:229-233`).
The claim also self-labels **nominal**, which is the honest reading given that the scored
`resolve.py` census (`SCORECARD.md:33`) does not read this instrument.

Gap (low): R58's remedy is "labelled nominal **and** the non-moving metric named". The claim says
"nominal per QUALITY R58" and names what moved, but never names the metric that did not
(`corpus/instruments/citation-survival.md` / `resolve.py`). Prior rounds say it in the scorecard row
(`SCORECARD.md:2908`, "(held; … the scored `resolve.py` census is not read by this gate)"); the claim
cell should carry the same clause.

## (c) P6: before-values honest, satisfiability not.

- At base `58905f2` both patterns print **0** (`grep -c` rc1), matching the claim's "(base: cases=6
  in both)" — the intended pin rows are `SKILL.md:982` (`… --selftest -> \`selftest cases=6
  failures=0\`, exit 0`) and `corpus/instruments/README.md:354` (`--selftest` → `selftest cases=6
  failures=0`). No third registry row pins the count in the base tree (checked over `*.md`, `*.json`,
  `*.txt`).
- **A junk edit satisfies both**: appending one comment line per file containing the exact phrases
  yields `1` and `1` while both pin rows still read `cases=6` (`p6-decoy.txt`). `grep -c` counts
  lines matching a phrase anywhere, not the registry row — the exact shape QUALITY **R55** forbids
  ("A plain expression used as a frozen row target anchors the table-row shape and whole identifier
  cells, not a phrase also found in prose"), and R113's own check (`grep -rn 'selftest cases='` ==
  the gate's output) would still be red under the decoy.
- Smallest safe correction: anchor the two rows (`^\|\s*recheck-cwd-census\.py\s*\|` and
  `^\|\s*\`corpus/instruments/recheck-cwd-census\.py\`\s*\|`) and assert the `cases=15` string inside
  that matched row. No verdict impact if the L1 edits the rows as intended; the claim's measured
  after-value is then genuine.

## (d) C2: does a junk entry pass B0–B7 as written? **Yes.**

Built in a scratch lane from `git archive 4ab5458` (`c2-junk-run.txt` contains the entry): six pinned
quotes pasted verbatim, the three header lines, the exact B0 recheck command, the S114 row moved
`queued→mined` with `used-by`, the F56 row, and `knowledge-expected.txt` +1 — **no claim, no
falsifiable rule, no rejected over-generalization (QUALITY Q3/Q5 unmet)**:

```
B0  S114:sha256 OK + six "OK occurrences=1 anchor=<n>-ok"           rc0
B1  SOURCES.md rows 114; exactly the S114 row changed
B2  knowledge 93 -> 94 ; knowledge-expected 95 -> 96
B3  FRONTIER-CENSUS rows=56 admitted=56 closed=56 problem-rows=0 registry=114 ; FRONTIER-PASS F56 ids=S114
B4  records=94 bound=94 unbound=0
B5  recheck line exits 0 from a foreign cwd
B6  literal containment 0/6 over the 93 admitted entries
B7  entry-independent (fleet-root validate); it cannot be affected by entry prose
```

Nothing in B0–B7 reads the entry's claims: B0 is manifest-only, B3's A–D limbs bind the recheck
line and the manifest, B1/B2/B4/B7 are bookkeeping. This is the **r79 carry-in** already routed at
`.ufo/waves/round-79/w1/CriticClaims.md:149` ("B0–B7 verify capture fidelity and admission
bookkeeping, not the entry's clause prose") — r80 did not close it, and r80's own draft is the
reason it is not verdict-changing today: the drafted entry states six falsifiable rules, six
rejected over-generalizations, a Gate table and a Limits block, so Q1–Q6 are met by reading, not by
predicate.

Smallest safe correction: add **B8**, an entry-content limb of the `r45-c2-gate.py` G5 shape (every
quoted span ≤25 words and located on its declared snapshot line; ≥1 "Falsifiable rule" and ≥1
"Rejected over-generalization" per claimed clause) — `r45-c2-gate.py` itself is pinned to F27/S071
constants and cannot be reused unchanged.

## (e) Is any claimed clause a restatement of admitted ground? **No.**

- Literal: 0/6 hits over the 93 admitted entries for every pinned quote (measured at the freeze
  archive), matching B6.
- Term-level, over the admitted corpus excluding the new entry: `grep -rli ubuntu` → none;
  `binary package` → none; `Ubuntu:` → none; `binary_names` → none; `empty object` → none;
  `1000 per` → none. The only other `source package` sentence is
  `corpus/knowledge/osv-affected-range-events.md:30`, quoting S080's "open source packages" — an
  OSV-format phrase, not an indexing rule.
- Rule-shape: Q02/Q03 (indexing key, scanner use), Q04 (ecosystem forms), Q05 (the binary_names
  bounds) and Q07 (empty object) have no admitted counterpart; the two candidate overlaps the claim
  declares as *held* (the experimental-status paragraph, and the ordering clause of `:58` matching
  F54) are in fact held and not claimed. `Q05`'s "1000 per request" is a distinct quantity from
  F54's batch limits, and the draft says so explicitly.
- Residual (low): B6's second half ("the scout paraphrase sweep … records each clause novel") is a
  record, not a runnable limb; the discriminating half is the literal scan, which a paraphrase-level
  restatement would pass. Mitigated in fact by the word-level sweeps above.

## (f) Other predicate/wording defects (low, none verdict-changing)

1. **P3 is not literally satisfiable as written**: it expects the line to contain
   `target_sha256=420151fd...5698` with an ellipsis, while the counter prints the full 64-hex digest
   (observed: `target_sha256=420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698`).
   Either pin the full digest (P2 has it) or write "prefix `420151fd`…`5698`".
2. **B7 depends on unfrozen sibling bytes**: `sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kasegi` walks every lane under the fleet root, so its exit status is
   not a function of kasegi's landing commit and cannot be replayed from a scratch export. Inherited
   from earlier rounds; worth stating as such in the landing report.
3. **Observation, not a defect**: K-T1's kill is a caught crash (`FAIL ret=-99
   stdout="exception=FileNotFoundError(…)"`), so the anchored R129 classifier scores it KILLED
   (assertion) exactly as the table's `expect` declares. Within R129's letter; no action.

## What I verified green on the frozen candidate (receipt `frozen-candidate-limbs.txt`)

P1 `selftest cases=15 failures=0` rc0 · P2/P3 sha `420151fd…5698`, `baseline=ok rows=28 killed=28
survived=0 dirty=0 notderived=0` rc0 · P4 rc2, `recheck-cwd: TMPDIR … is not a directory`, no
Traceback · P5 `RECHECK-CWD entries=94 noprefix=0 exit2_foreign=0 exit0_foreign=72 exit1_foreign=22
exit_other=0 norecheck=0 restoration_only=0` + `RECHECK-CWD-RESULT conformant` rc0, with
`ls corpus/knowledge/*.md | wc -l` = 94 (the working tree is dirty: the uncommitted C2 entry and
the C1 candidate are already present — P5/P6 are landing-commit measurements and must be re-run
after the L1 lands) · P7 1/1/0 · P8 `mutbat selftest ok … rc0` · nine r79 ids present in the frozen
table (N10 N11 N21 N25 N26 N27 N30 T1 T2) · C2 B0 six `OK occurrences=1 anchor=<n>-ok` at anchors
25,35,35,38,39,58.

## Receipts (`CriticClaims-receipts/`)

`mutbat-F1.txt` · `mutbat-F2.txt` · `mutbat-F3.txt` · `mutbat-F4.txt` · `mutbat-real.txt` ·
`forgery-F1-location-guard.py` · `forgery-F2-selfhash-guard.py` · `forgery-F3-sibling-guard.py` ·
`forgery-F4-baseline-limb.py` · `forgery-limbs.txt` · `p6-decoy.txt` · `c2-junk-run.txt` ·
`frozen-candidate-limbs.txt`

Tool changes: none. Nothing was written outside `.ufo/waves/round-80/w1/CriticClaims.md`,
`.ufo/waves/round-80/w1/CriticClaims-receipts/` and the scratch root (deleted).
