# SimplifierCleanup — YAGNI sweep of the round-34 instruments and the F17 landing (round 34, wave 1)

Seat: simplifier (`SimplifierCleanup`), leaf of the round-34 L2 wave, lane `kasegi-shokunin`.
Write scope used: **this receipt only**. No lane file was created, edited or deleted by this seat; no
git/jj mutation, no subagent, no `agent://all`, no tool installed or upgraded (bash 5.3.20,
python3 3.14.8 and `/usr/bin/shellcheck` were already present and are the only tools run).
Every fixture, patched copy, mirror root and captured output lived under
`/fast/scratch/hyaku/kasegi-r34/SimplifierCleanup/` and was removed after this receipt was written
(§7). Scratch copies only are mutated below; the lane instruments were read, never patched in place.

## Report

### 0. The bytes every number below was measured on

Measured with `sha256sum` on quiescent lane bytes, 2026-10-26T05:57Z, re-confirmed byte-identical at
06:08Z:

| path | sha256 | size |
|---|---|---|
| `corpus/instruments/r-defect-closure.sh` | `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d` | 35971 B, 832 lines |
| `corpus/instruments/kill-rule-check.py` | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` | 43138 B, 881 lines |
| `corpus/instruments/capture-binding-check.py` | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` | 40556 B, 892 lines |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` | read-only here; not edited by this seat |

**Drift, disclosed rather than smoothed.** During this seat the closure script moved
`93e2285a… → 0beafed2… → 357a7e49… → 2a635bf5… → 809aaf90…` and the counter moved `e33a300f… →
7a20e724… → c279d952…` (peers hardening in flight; the probe set grew 3 → 9 and the suite grew a
self-report judge while I measured). Every before/after pair in §1–§3 was **re-measured at the
digests above** — the closure pair a second time when the file reached `809aaf90…` — so nothing
below is quoted from an intermediate generation. `capture-binding-check.py` was `3d9e5e0d…`
throughout the seat.

Landed-run baseline, run from the lane root at those bytes (`python3`/`bash`, exit codes are the
instrument's own verdict):

```
$ bash corpus/instruments/r-defect-closure.sh
…R1..R9 check=… open=0 (nine lines)…
closed=9/9 exit=0                               # exit 0

$ bash corpus/instruments/r-defect-closure.sh --selftest --scratch <scratch>
selftest case=R8 live=pass fixture=rejected control=pass verdict=pass
selftest case=R9 live=pass fixture=rejected control=absent verdict=pass
selftest cases=9 failures=0
selftest judge=forged-summary rejected=1
selftest judge=short-report rejected=1
selftest judge=complete-report accepted=1       # exit 0

$ python3 corpus/instruments/capture-binding-check.py
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0                   # exit 0   (stdout body sha256 390e96037832d1e679446dc7d7ee96f236d4b5fa2c82bc37c103dcfa200b7cf0)

$ python3 corpus/instruments/capture-binding-check.py --selftest
selftest cases=23 failures=0                    # exit 0

$ python3 corpus/instruments/kill-rule-check.py
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0                                     # exit 0
```

Full captured outputs are digested in §8. These reproduce the frozen C1 targets
(`closed=9/9`, `cases=9 failures=0`, `records=41 bound=41 unbound=0`, `cases=23 failures=0`,
`survivors=0`), so the sweep below is over instruments that are green when measured.

---

### 1. `r-defect-closure.sh` — nine checks, nine distinct facts, no duplicate authority

Function line numbers in `809aaf90…`: `check_r1` 143, `check_r2` 160, `check_r3` 185, `check_r4`
205, `check_r5` 269, `check_r6` 286, `check_r7` 330, `check_r8` 377, `check_r9` 439.

| check | the one fact only it loads | where |
|---|---|---|
| R1 | `SCORECARD.md` carries **0** literal lane-hash markers **and** an appended `Correction (round 34)` block naming `7963976e` and `014ee2d` | grep-count + block anchor |
| R2 | the round-33 SCORECARD section carries `Erratum 2` with the per-id restatement (`0 or 2+`, `multi_row_url`, `dup-id`) **and** `QUALITY.md` carries the R22 pre-freeze row | SCORECARD + QUALITY |
| R3 | `QUALITY.md` carries the appended `Note (round 34)` **below** the R20 row, quoting `exactly one` and saying the per-id reading supersedes it | QUALITY only |
| R4 | the tightened kill rule is on the `QUALITY` R24 row (`kill rule` + `selftest case=` + `per case`) **and** `corpus/lessons/round-33.md` carries the appended R4 3-of-4 erratum after its filed tail | QUALITY + lesson |
| R5 | the retired case name `url-matching-two-rows` is **absent** while the case table still holds ≥11 tuples | capture-binding bytes |
| R6 | `round-26/manifest.json` binds `S040-live.txt` (record path or `orphans` list) **and** its `purpose` no longer says the file was skipped | round-26 manifest |
| R7 | `round-33.md` carries the appended R7 erratum (`19→31`, `23→22`, `S050.txt:70`) | lesson only |
| R8 | every `round-32` `fetched_utc` is a **real** strict-UTC instant (shape floor + calendar parse, zero offset) | round-32 manifest |
| R9 | capture-binding carries the nine added case names **and** frontier rule A is **bidirectional** (behavioural: mirror fixture exit 0, reverse fixture exit 1) **and** the `c2-controls` junk twin exists | two instruments + twin |

**Verdict: no two checks test the same fact.** The three pairs that could have collided were
checked one by one:

- R2 / R3 / R4 read three different record surfaces (`SCORECARD` round-33 erratum; a `QUALITY`
  note; the `QUALITY` R24 row plus the lesson erratum). Each check has its own isolating broken
  fixture in `--selftest` and each is rejected there (nine `fixture=rejected` lines), while the
  live tree passes all nine — every check therefore has both a passing and a failing witness that
  the other eight do not supply.
- R5 counts case tuples (`grep -cE '^[[:space:]]*\("[a-z0-9-]+",'` → `cases=21`) while R9 checks
  nine **names**. Neither implies the other: a restored retired name keeps the count at 21, and a
  name check alone does not bound the table. R5's summary line at the landed bytes prints
  `R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0`.
- R8's shape floor and capture-binding rule C are deliberately the same **accept set** (the
  closure file says so at its header, lines 77-83), which is parity, not duplication: R8 is the
  closure check for the round-32 manifest and must not be looser than the instrument it mirrors.

Dead paths found (measured, not inferred):

- **D1 — R6 accepts two manifest shapes nobody writes.** `r-defect-closure.sh:306-309`:
  `orphans = data.get("orphan", data.get("orphans", []))` / `if isinstance(orphans, str): orphans =
  [orphans]`. An audit of every manifest in the lane shows the only declared-orphan shape in use is
  a list of objects under `orphans`:

  ```
  corpus/source-snapshots/round-26/manifest.json ['orphans'] {"orphans": [{"path": "S040-live.txt", "reason": "Live probe capture of the S040 page, …"}]}
  --- round-26 full keys --- ['schema_version', 'purpose', 'orphans', 'sources']
  ```
  and `capture-binding-check.py:308` (`orphan_paths`) treats anything but a list of `{path, reason}` objects
  as `UNAVAILABLE … orphans` (exit 2). The singular key and the string coercion are a second
  authority that diverges from the instrument; no tree exercises them (the R6 broken fixture pops
  **both** keys, so the fixture cannot see them either).
- **D2 — R4 carries a SCORECARD-paragraph fallback no tree exercises.**
  `r-defect-closure.sh:221-224` (`if [ "$ok" -ne 0 ] && [ -f "$s" ] && para_grep "$s" 'kill rule'
  'selftest case=' 'per case'; then ok=0; fi`) plus its helper `para_grep` (131-139) and the R4
  fixture's `SCORECARD.md` copy (`:632`, `:634`). The live tree satisfies the **row** limb
  (`| R24 |` exists and carries all three tokens), and the broken fixture deletes `selftest case=`
  from both files, so the fallback is deciding in no passing run and no failing fixture. It is also
  a second record surface for a requirement the round recorded on the R24 row.
- **T1 (tolerated, kept).** R9 probes two junk-twin spellings
  (`c2-controls/junk-f17.md` then `.ufo/waves/round-34/c2-controls/junk-f17.md`); the first is dead
  in this tree. Kept deliberately: it is a relocation tolerance, not a duplicate authority, and the
  claim text spells the path as `c2-controls/`. Removing it would fail closed if the L1 moves the
  twin up one level. Not proposed for deletion.

Static checks at `809aaf90…`: `shellcheck -S info` reports 11 × SC2329 and 1 × SC2016 and nothing
else. SC2329 is a call-graph false positive: the nine `check_r*` functions are invoked through the
`CHECK_FNS` array, and `block_from`/`para_grep` are called only from those functions, so shellcheck
cannot see any of the eleven. SC2016 is the literal backticks in the R9 fixture's markdown
`printf`. A local-declaration scan over all 22 functions found **no** unused `local`
(`UNUSED-LOCAL` count 0); every shell helper except `para_grep` (D2) has a caller.

**Before/after for D1+D2 (proposal P3).** The closure script derives its lane root from its own
location and builds fixtures from that root, so a patched copy is exercised through a symlinked
mirror root in scratch whose checked inputs are symlinks to the live lane bytes:
`<mirror>/SCORECARD.md → lane/SCORECARD.md`, `<mirror>/corpus/{QUALITY,README,SOURCES}.md`,
`<mirror>/corpus/lessons`, `<mirror>/corpus/source-snapshots`, the two instrument files and the junk
twin. Script bytes: pristine = `809aaf90…` (copy verified byte-identical), lean = same file with
D1, D2, `para_grep`, the `s=SCORECARD.md` local, one comment and the R4 fixture's SCORECARD copy
deleted (35971 B → 35149 B; `bash -n` exit 0; `shellcheck -S warning` exit 0). The pair below was
first measured at `2a635bf5…` and re-measured unchanged at `809aaf90…`:

```
$ bash <mirror>/corpus/instruments/rd-pristine.sh          # pristine bytes
…R1..R9 … open=0…
closed=9/9 exit=0                                          # exit 0
$ bash <mirror>/corpus/instruments/rd-lean.sh              # P3 applied
…R1..R9 … open=0…                                          # identical bytes to the run above
closed=9/9 exit=0                                          # exit 0
$ diff pristine.out lean.out                               # → PLAIN_IDENTICAL (no output)

$ bash <mirror>/corpus/instruments/rd-pristine.sh --selftest --scratch <s1>
…nine `selftest case=R# live=pass fixture=rejected … verdict=pass` lines…
selftest cases=9 failures=0
selftest judge=forged-summary rejected=1
selftest judge=short-report rejected=1
selftest judge=complete-report accepted=1                  # exit 0
$ bash <mirror>/corpus/instruments/rd-lean.sh --selftest --scratch <s2>
…byte-identical to the run above…                          # exit 0
$ diff pristine-selftest.out lean-selftest.out             # → SELFTEST_IDENTICAL (no output)
```

Base-tree control (`git archive 014ee2d7… | tar -x`, read-only git): both copies print
`closed=0/9 exit=1` with all nine `open=1`; the **only** differing line is R4's failure wording,
because the removed fallback's name is removed from the message:

```
-R4 check=tightened kill-rule requirement not recorded (QUALITY R24 row or a SCORECARD paragraph: kill rule + one 'selftest case=' line per case) open=1
+R4 check=tightened kill-rule requirement not recorded (QUALITY R24 row: kill rule + one 'selftest case=' line per case) open=1
```

Verdict and signal are unchanged (9/9 closed on the landed tree, 0/9 on base); only the sentence
that described the removed fallback changes. That is the intended, honest message change, not a
verdict change.

---

### 2. `kill-rule-check.py` — the mutant set is minimal and every added probe is load-bearing

**Named mutant set (3 rows) — minimal, each load-bearing.** At `c279d952…` each row is an
exactly-once patch (`find_count=1 status=ok`) and each is killed by a probe the pristine bytes pass:

```
mutant=skip-selftest-summary killed=1            killed by  selftest-shape (reasons=summary-only;case-set-mismatch)
mutant=accept-record-without-url killed=1        killed by  selftest-shape + record-without-url (reasons=exit=0 want=1;missing='detail=absent'…)
mutant=per-file-binding-removal killed=1         killed by  selftest-shape + per-file-orphan (reasons=missing='rule=orphan-capture'…)
mutants=3 killed=3 survivors=0 invalid=0
controls=4 rejected=4
gates=7 failed=0
```

They cover three different limbs (round-33 F-5 report shape; rule B5 absent-url; rule A1 per-file
orphan), so dropping any one loses a limb rather than weight. No fourth row is claimed by the
frozen claim, and none is needed for the counter to reach `survivors=0`.

**Probe set (9) — no dead fixture.** Six probes were added during the wave
(`unnamed-record-id`, `stale-orphan-declaration`, `malformed-fetched-utc`, `punctuated-url-cell`,
`malformed-orphan-declaration`, `nested-legacy-round`). An oracle probe that no row can fail is
unproven weight, so I added six attack rows through the sanctioned `--row-file` path
(`{"rows":[{name,find,replace,note}]}`) and measured each probe against the limb it exists for
(the block below condenses each row's `mutant-probe … mutant=fail` line and its `mutant=… killed=1`
line into one row; the run printed both):

```
$ python3 corpus/instruments/kill-rule-check.py --root <lane> --row-file rows3.json --json …
mutant=drop-malformed-orphans-guard killed=1             probe=malformed-orphan-declaration  reasons=exit=0 want=2;missing='reason=manifest-shape'
mutant=drop-stale-orphan-detection killed=1              probe=stale-orphan-declaration      reasons=exit=0 want=1;missing='rule=orphan-declared-missing file=S077.txt'
mutant=url-token-rstrip-removal killed=1                 probe=punctuated-url-cell           reasons=exit=1 want=0;missing='records=1 bound=1 unbound=0'
mutant=nested-round-first-component-removal killed=1     probe=nested-legacy-round           reasons=exit=1 want=0;missing='records=1 bound=1 unbound=0'
mutant=accept-unnamed-record killed=1                    probe=unnamed-record-id             reasons=exit=0 want=1;missing='rule=no-row record=<unnamed>';missing='unbound=1'
mutant=accept-unparsable-fetched killed=1                probe=malformed-fetched-utc         reasons=missing='record=S002 dir=round-32 detail=malformed'
mutants=9 killed=9 survivors=0 invalid=0
controls=4 rejected=4
gates=7 failed=0
survivors=0                                              # exit 0
```

Each added probe is failed by exactly one row and by no other — six probes, six distinct killers.
**Verdict: no dead probe, and the probe additions are not weight.** (The same run is the positive
control for the counter's own `--row-file` path: extra rows are measured, counted and can make the
aggregate red, exactly as documented.)

Dead code found:

- **D3 — duplicate assignment of the survivor witness.** `kill-rule-check.py:804-805`
  (`if result["verdict"] == "survivor": witness_survivors = summarise(["survivor"])[1]`) is always
  overwritten three lines later by the `CTL-equivalent` block. `CTL-equivalent` is the only control
  whose verdict is `survivor`, so the first assignment can never survive to the `fake_control` call.
- **D4 — a no-op display branch.** `kill-rule-check.py:709-710`
  (`if not instrument_path.startswith(root + os.sep): instrument_ref = instrument_path`). For a
  relative `--instrument`, `instrument_path = os.path.join(root, ref)` always starts with
  `root + os.sep`; for an absolute one, `instrument_path is instrument_ref`, so the assignment
  rewrites a variable with itself. Measured on all three argument shapes — default relative,
  absolute inside the root (`KILL-RULE instrument=…` line identical modulo the self-digest, both
  copies exit 0), and absolute outside the root (full stdout identical) — stdout identical to the
  byte.

**Before/after for D3+D4 (proposal P5).** Same counter bytes (`c279d952…`) with the two segments
deleted (43138 B → 42932 B, `py_compile` OK), both copies run with `--root <lane>` and the default
(absolute) fake control:

```
$ python3 kr-pristine.py --root <lane> --scratch <s1>     # exit 0
$ python3 kr-lean.py     --root <lane> --scratch <s2>     # exit 0
$ diff <(pristine | sed 's/counter_sha256=[0-9a-f]*/counter_sha256=<self>/') \
       <(lean     | sed 's/counter_sha256=[0-9a-f]*/counter_sha256=<self>/')
COUNTER_IDENTICAL                                          # no output
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
$ python3 kr-pristine.py --selftest ; python3 kr-lean.py --selftest
selftest cases=3 failures=0                                # both, exit 0
```

`--json` output is unaffected (the payload carries no `witness_survivors` field). The only
byte that must differ between the copies is the self-digest `counter_sha256=`, which is why it is
normalised in the diff; every verdict line is identical.

---

### 3. `capture-binding-check.py` — no dead case, no unreachable branch, two dead constants

**Dead cases: none.** 23 case names, each asserting a distinct contract line — 21 fixture trees plus
the 2 report-verifier cases that prove `judge_selftest_report` is not an always-reject limb. The one
near-pair that reads as duplication is not:

```
selftest case=shared-url-between-two-records exit=0 want=0 verdict=pass   # two records share one URL -> multi_row_url=2
selftest case=shared-url-not-a-failure       exit=0 want=0 verdict=pass   # one record, two rows share that URL -> multi_row_url=1
```

The second case is the only fixture that fixes the **unit** of `multi_row_url` (records, not rows):
with two records the count could be explained either way, with one record it cannot. Likewise the
provenance quartet is four facts, not one: `round-32`+archival fails (the exemption is closed for
modern rounds), legacy without archival fails (an absent value fails everywhere), and two pass-path
controls prove the branches are not always-fail. Every case line in the landed run prints
`verdict=pass` (§0), and `judge_run` fails any case whose observed `exit` differs from its `want`.

**Unreachable branches: none at the instrument level, and the three that were unproven at counter
gen 3 are now probed.** `malformed` (both paths: impossible calendar and unparsable string),
`orphan-declared-missing`, and `record=<unnamed>` were reachable but had no proving fixture in the
gen-3 counter; the landed counter's `malformed-fetched-utc`, `stale-orphan-declaration` and
`unnamed-record-id` probes cover them, and §2 measures each of those probes as load-bearing.
`orphan_paths`' rejection of a non-list/non-object declaration is proven by
`malformed-orphan-declaration` (pristine `exit=2`, mutant missing `reason=manifest-shape`).

**Dead constants: two, with different fates.** An AST scan (Loaded-name count 0) finds
`SCHEMA_VERSION` and `GAMMA` are never read:

- **`GAMMA` (`capture-binding-check.py:531`)** — dead fixture colour, no consumer anywhere
  (`grep -c GAMMA` = 1). Deleting it cannot change behaviour, and measurement agrees:
  - plan output vs pristine: `identical_stdout=True`, exit 0, 12 lines, stdout sha256 prefix
    `390e96037832d1e6` (identical to the landed run);
  - `--selftest`: `selftest cases=23 failures=0`, exit 0;
  - counter against the lean bytes: `controls=4 rejected=4`, `gates=7 failed=0`,
    `mutants=3 killed=3 survivors=0`, exit 0.
- **`SCHEMA_VERSION` (`capture-binding-check.py:158`)** — dead as a **value** (the instrument never
  validates `schema_version`; `write_manifest` writes the literal `1`) but **load-bearing as an
  anchor**: it is `CTL-noop`'s exactly-once `find` in the counter (`control_rows()`). Measured:

```
# SCHEMA_VERSION deleted, counter untouched:
control=CTL-noop verdict=invalid:find-count expect=invalid:noop ok=0
controls=4 rejected=3
GATE fail name=controls
survivors=0                                              # exit 1  (a dead constant is a live anchor)

# SCHEMA_VERSION deleted AND CTL-noop re-anchored to `def row_tokens(cell):` (exactly once in both byte sets):
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
controls=4 rejected=4
gates=7 failed=0
survivors=0                                              # exit 0, on the lean instrument and on the pristine instrument
```

So `SCHEMA_VERSION` is not weight to delete alone; it is a coupled pair. Nothing else in the file
is dead: every helper (`double_https_rows`, `url_row_count`, `snapshot_dirs`, `classify_fetched`,
`provenance_ok`, `bind_record`, `orphan_paths`, `capture_files`, `duplicate_records`,
`judge_run`, `judge_selftest_report`, `forged_*`, `scratch_base`) has a caller, and no function has
an unused parameter.

---

### 4. The F17 entry (`immunefi-vscs-v2-2-smart-contract-severity.md`) — no filler, no redundant claim

Mechanical check: **18 of 18** manifest assertions are quoted in the entry, and each is hosted by
the claim it supports — so no assertion is carried for a claim the entry does not make, and no claim
rests on an unquoted assertion:

```
manifest quotes: 18 | absent from entry: []
Q1,Q2  -> Claim 1 (five levels / per asset class)          Q3,Q4  -> Claim 2 (impact decides)
Q5,Q6  -> Claim 3 (consequence + downgrade-or-reject)      Q7,Q10,Q11 -> Claim 4 (Critical list)
Q8     -> Claim 6 (one asset class per impact)             Q12    -> Claim 5 (funds boundary)
Q13,Q14,Q15,Q16,Q17 -> Claim 7 (Medium/Low/None)           Q9 -> Claim 4 + FC-5 + limits;  Q17 -> Claim 7 + FC-7;  Q18 -> Claim 6 + FC-6
```

All seven claims are non-overlapping facts (level count/numbering; impact-over-likelihood; the
carve-out; the Critical enumeration; the funds boundary; asset-class membership; the Medium/Low
shape), and the four prose sections are each a distinct obligation of the entry bar (Q5 requires a
rejected over-generalization and a falsifiable rule; Q4 requires attribution; Q1/Q7 require the
limits). The closest thing to redundancy is by design, and I record it rather than deleting it:

- Rejected #3 ("A downgrade is a rejection") and #4 ("Any loss of funds is Critical") restate the
  evidence of Claims 3 and 5. Their role is to **name the misreading**, which is what Q5 asks for;
  deleting them would remove the named misreading, not duplicate prose.
- The CVSS negative and the payout negative each appear on three/four surfaces (attribution,
  honest limit, rejected item, FC-3/FC-4). If the L1 wants a shorter entry, the removable instance
  is the attribution parenthesis — FC-3 and FC-4 keep the evidence — but that is a content call on
  a claim surface, not a YAGNI deletion, so I propose nothing here.

**Verdict: no deletion proposed inside the F17 entry.**

---

### 5. Wave receipts — no duplicate artifact

Census over the wave directory (recursive, `2026-10-26T05:58Z`):

```
files 77  distinct digests 77  duplicate-digest groups 0
subdirs: ['ScribeSkillGate', 'SentCred']
```

So no receipt, transcript or JSON payload is a byte copy of another. The three artefacts that look
like duplicates and are not deletions:

- **The `before.txt` triple is already filed; I confirm it and do not re-file it.**
  `census-before.txt`, `c1-controls/before.txt` and `c2-controls/before.txt` are byte-identical
  (`sha256 d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0`, 1552 B each) — already
  reported as finding **F1** in `.ufo/waves/round-34/wave1/ExecBeforeReceipts.md:285` ("the three
  'before' receipts are one file copied three times") and noted at `ScoutDatawalk.md:13`. Two of the
  three are referenced by name in receipts (`RevC1BeforeAfter.md:5`, `RevC2BeforeAfter.md:40`), so
  deleting them here would break evidence paths; consolidation is the L1's call.
- **`ScribeQualityDraft-block.txt` is not an orphan copy.** Its 3971 bytes (3957 characters) are an exact substring of
  `ScribeQualityDraft.md`, and it is named by three receipts (`ExecQualityAppends.md`,
  `ScribeQualityDraft.md`, `CritOverclaim.md`): a staging artefact with callers. Keep. (It is also
  *not* the landed `QUALITY.md` block — `block in QUALITY.md` is `False` — so it is a draft, and the
  landed append is the executor's.)
- **`SCORECARD.md` has two writers, sequentially.** `ExecScorecardMarkers.md` ("Assigned path:
  `SCORECARD.md` only", marker substitution at `:988`/`:1087`) and `ScribeScorecard.md` ("Wrote
  exactly two files: `SCORECARD.md` (one append at EOF, 124 lines)"). Both landings are present in
  the final bytes — R1 reads `lane-hash-markers=0` and R2 finds the round-34 block — so this is a
  coordination observation, not a lost write: two seats wrote one file in one wave with no shared
  lock, and R1/R2 are the checks that would have caught an overwrite.

---

### 6. Proposals for the L1 (each measured; none applied)

| id | change | evidence (before → after) | risk / land condition |
|---|---|---|---|
| **P1** | delete `capture-binding-check.py:531` `GAMMA = "https://example.invalid/gamma"` | plain run byte-identical (12 lines, sha `390e9603…`), `--selftest 23/0`, counter `survivors=0 gates=7 failed=0 exit=0` | none measured. Changing these bytes moves the C1 instrument digest pinned in `corpus/instruments/README.md`, the receipts and every `pristine_sha256=3d9e5e0d…` line → land **after** the wave's digest pins close, and re-pin in one commit |
| **P2** | delete `capture-binding-check.py:158` `SCHEMA_VERSION = 1` **and** re-anchor `CTL-noop` to an exactly-once literal (measured with `def row_tokens(cell):`) | alone: `CTL-noop invalid:find-count`, `controls=4 rejected=3`, `exit 1`. Paired: `controls=4 rejected=4 gates=7 failed=0 exit=0` on both instruments | must be a pair; a lone deletion makes the counter red. Same digest-repin condition as P1 |
| **P3** | delete `r-defect-closure.sh:306-309` (the `orphan` singular key + string coercion) | mirror plain run `closed=9/9 exit=0` identical; `--selftest cases=9 failures=0` identical | the check becomes strict about an undocumented shape (a `"orphans": "file"` scalar would now fail R6). Aligns R6 with `capture-binding.orphan_paths`, the shape authority. `0beafed2…`-era to `809aaf90…` receipt pins move only at the next integration |
| **P4** | delete the R4 SCORECARD fallback (`:221-224`), `para_grep` (`:131-139`), the `s=SCORECARD.md` local and the R4 fixture's SCORECARD copy/filter (`:632`,`:634`); message loses "or a SCORECARD paragraph" | mirror plain `closed=9/9`, selftest `cases=9 failures=0`, base tree `closed=0/9 exit=1` — all identical except the R4 failure sentence quoted in §1 | removes a second record surface for a requirement the round recorded on the `QUALITY` R24 row. If the L1 prefers the SCORECARD paragraph as an allowed surface, keep it instead — but then R4 must be *documented* as an OR, which today only the docstring says |
| **P5** | delete `kill-rule-check.py:804-805` and `:709-710` | counter stdout identical modulo the self-digest, `survivors=0`, `gates=7 failed=0`, `--selftest 3/0`, exit 0 | none measured; `--json` payload unaffected. Same digest-repin condition |

Not proposed: R9's junk-twin path tolerance (T1, §1) and the `before.txt` consolidation (§5, evidence
paths).

**Why nothing is applied here.** All three instruments are frozen evidence for C1: their digests are
pinned in `corpus/instruments/README.md` and in the other round-34 receipts (`grep -rl` finds
`0beafed2…` in 9 wave files and `3d9e5e0d…` in 15), and `kill-rule-check.py`'s patch anchors bind to
`capture-binding-check.py`'s current bytes. A mid-wave simplification would create a second
generation of pinned bytes, which is exactly the duplicate authority this seat exists to remove.
The proposals are staged behind one integration commit that re-pins them.

---

### 7. Scratch and cleanliness

- **A leak of mine, found and removed.** Six stale fixture trees
  `/tmp/r-defect-closure-selftest.{MekMRi,xxXB6n,PyeVzg,0nlRfQ,bRo1iJ,3EtP6H}` (9 dirs each, `R1`–`R9`)
  survived my early `--selftest` runs, mtimes `2026-10-26T05:35:27Z`–`05:37:09Z`. Cause: those runs
  were killed by the harness (no `rm -rf` on `SIGKILL` — an EXIT trap cannot fire), not a script
  defect: a normal run leaves nothing (`new leftovers: []` measured with the same command at the
  landed bytes). Before deleting I checked no consumer: `pgrep -af r-defect-closure` → none,
  `pgrep -af 'kill-rule-check|capture-binding-check'` → none, ages 22.7–24.4 min. Removed all six;
  post-removal glob is empty.
- **My parse tree is gone.** `/fast/scratch/hyaku/kasegi-r34/SimplifierCleanup/` (mirror root,
  base export, patched copies, attack row files, captured outputs) was removed after this receipt
  was written and before the seat yielded; `/fast/scratch/hyaku/kasegi-r34/` then holds only the
  other seats' roots.
- **Lane untouched by this seat.** `git status --porcelain` in the lane shows only the peers'
  round-34 work (modified `SCORECARD.md`/`QUALITY.md`/`README.md`/`SOURCES.md`/manifests/lessons and
  the new instrument/knowledge/snapshot files); no path carries this seat's name and no experiment
  artefact was written into the lane.

### 8. Reproduction digests

| artefact | sha256 | size |
|---|---|---|
| `final-closure-plain.txt` (landed `r-defect-closure.sh` stdout) | `0823a08c544444788672a11009254951ac985fb66702594ad96f0e80555dfa15` | 1002 B |
| `final-closure-selftest.txt` | `9955ce658978a51bf307af52c595aae50f3cf4d6a4fea33cac5adc3fa2905026` | 796 B |
| `final-capture-plain.txt` | `390e96037832d1e679446dc7d7ee96f236d4b5fa2c82bc37c103dcfa200b7cf0` | 808 B |
| `final-capture-selftest.txt` | `ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51` | 1552 B |
| `final-kill-plain.txt` (landed `kill-rule-check.py` stdout) | `85d80cb2c8c6cbf237bba0941617b7ad9904db6fbaabac0d5e7066b9f3bb9027` | 5401 B |
| `final-kill-selftest.txt` | `eb83937c44aef715cbe84a28f9fbe72425451107afb38f48e6a4a25688a20ec1` | 250 B |
| pristine closure copy used for P3/P4 (`rd-pristine4.sh`) | `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d` | byte-identical to the lane |
| pristine counter copy used for P5 (`kr-pristine2.py`) | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` | byte-identical to the lane |

(The six stdout captures live in the deleted scratch tree; their digests are recorded here so the
receipt's numbers can be re-derived by re-running the six commands in §0, whose verdict lines are
quoted verbatim above.)

Re-run contract, from the lane root:

```
sha256sum corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py corpus/instruments/capture-binding-check.py
bash corpus/instruments/r-defect-closure.sh; echo "closure_exit=$?"
bash corpus/instruments/r-defect-closure.sh --selftest; echo "closure_selftest_exit=$?"
python3 corpus/instruments/kill-rule-check.py; echo "kill_exit=$?"
python3 corpus/instruments/capture-binding-check.py; echo "capture_exit=$?"
python3 corpus/instruments/capture-binding-check.py --selftest; echo "capture_selftest_exit=$?"
```

Targets at the digests in §0: `closed=9/9 exit=0`; `selftest cases=9 failures=0`;
`mutants=3 killed=3 survivors=0 invalid=0` + `survivors=0`; `records=41 bound=41 unbound=0`;
`selftest cases=23 failures=0`. A different instrument digest means the bytes moved — re-measure,
do not adjust the target.
