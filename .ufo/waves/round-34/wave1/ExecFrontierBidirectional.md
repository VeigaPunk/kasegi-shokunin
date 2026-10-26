# ExecFrontierBidirectional — round 34, wave 1 (C1, R9)

Scope: `corpus/instruments/frontier-recheck-count.py` rule A made bidirectional, plus its
documentation append in `corpus/instruments/README.md`. No entry, registry, manifest or
scorecard file touched. No tool installed (nothing needed; stdlib only).

## Report

### 1. Files changed

| path | before (lane base `014ee2d7`) | after (worktree) | lines |
|---|---|---|---|
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` (228) | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` (433) | +220 / −15 |
| `corpus/instruments/README.md` | — (base 656 lines) | `42d3a584be119410fd57fd67c1c62c02827af94b7e784bf5d32adcc3e4f0b2ca` (930 lines at measurement; this seat's append is §783–872, 90 lines) | appended §783–872 only |

```
$ sha256sum corpus/instruments/frontier-recheck-count.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
$ git diff --numstat -- corpus/instruments/frontier-recheck-count.py
220	15	corpus/instruments/frontier-recheck-count.py
```

The README append begins at `corpus/instruments/README.md:783`
(`## Round-34 amendment — frontier-recheck-count.py rule A is bidirectional (C1, R9)`);
no line above it moved (R6). Two corrections were made inside my own append as the bytes
settled (F17 landed: `entries=19 pass=19` → the measured `entries=20 pass=20`; and the
digest references now name the final instrument bytes `1be79af6…`). The README is a shared
append-only file: this seat's section is `:783-872` (90 lines), other seats' round-34
sections sit above and below it (`:658` capture-binding, `:874` kill-rule-check), so the
930-line file digest above is a point-in-time value for the whole file, not a pin of my
section.

### 2. The gap being closed (R9, quoted)

Round-33 `wave1/MutEntryF16.md:179`:

> Cause, read from `corpus/instruments/frontier-recheck-count.py` (read-only): rule A is
> implemented one-directionally — `header-sources-not-rechecked` fires only when
> `declared ⊄ recheck_ids`; there is no `recheck_ids ⊆ declared` check. The reverse
> direction is filtered through `selection-not-cited-by-entry`, but `cited` is every
> `S\d{3,}` occurrence in the whole file — always satisfied by the recheck line's own
> `--source S050`.

Confirmed by reading the base bytes: `cited` was built from `re.findall(r"S\d{3,}", body)`
over the whole file, and the recheck line is inside that body, so
`selection-not-cited-by-entry` could never fire — dead by construction.

### 3. What the landed rule does

Rule A now runs both ways against the entry's **declared source set**:

* forward — `header-sources-not-rechecked`: a declared id missing from the recheck's
  `--source` selections (unchanged behaviour, unchanged name);
* reverse — **new** `selection-not-declared-by-entry`: a `--source` id the entry never
  declares.

Declared set = header `source:` lines ∪ per-source evidence items (`^(?:[-*]|\d+[.)])\s+S\d{3,}\b`,
e.g. `- S002, "Assessment": "…"`). Both shapes are live in the corpus: F09/F10/F13/F14 use
one header line per source, F01–F05 declare the primary source on the header line and the
rest in their evidence list. A capture-path mention in prose or a blockquote attribution
(`S050.txt:70`) is a *reference*, not a declaration.

`cited` is now built from every line **except** a `source:` line and `recheck:` line, so
`selection-not-cited-by-entry` is no longer vacuous. `--json` records the new
`evidence_declared_ids` field alongside `declared_ids`.

A header-only reverse rule was measured first and rejected on this corpus, not assumed:
it fails five admitted rows — F01 S002, F02 S004/S005, F03 S007/S008, F04 S010–S012,
F05 S014/S015 — `entries=19 pass=14 exit=1`, because those rechecks legitimately cover
their evidence lists (`corpus/knowledge/cvss-v4-severity-and-vector.md:2` header S001,
`:26-29` evidence S002, `:4` recheck S001+S002).

### 4. Selftest (new): six fixture lanes, `cases=6 failures=0`

```
$ python3 corpus/instruments/frontier-recheck-count.py --selftest --scratch /fast/scratch/hyaku/kasegi-r34/ExecFrontierBidirectional
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0
selftest_exit=0
```

Each fixture lane carries a stub `corpus/instruments/source-recheck.py` and a schema-1
manifest, so a case can only fail on the harness's own binding. The reverse-direction case
named in the assignment is `selection-not-declared`: the fixture entry declares S001/S002
on header lines, its recheck line adds `--source S003`, and S003 is mentioned in prose
only — the landed tool prints
`FAIL F98 knowledge/fixture.md ids=S001,S002 exit=- problems=selection-not-declared-by-entry`,
`entries=1 pass=0 exit=1`. Scratch is removed in a `finally:` `shutil.rmtree`.

### 5. Live harness on the lane (before → after)

Before, base bytes `aa60b581…` (re-derived from `git show 014ee2d7:…`, run with
`--root $PWD` against the current tree, F17 present):

```
$ python3 .../before.py --root "$PWD" | tail -3; echo "before_live_exit=${PIPESTATUS[0]}"
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
before_live_exit=0
```

The same base bytes printed `entries=19 pass=19 exit=0` on the pre-F17 tree (this seat's
first run, before any edit).

After, landed bytes `1be79af6…`, F17 present:

```
$ python3 corpus/instruments/frontier-recheck-count.py; echo "live_exit=$?"
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
live_exit=0
```

`entries=20 pass=20 exit=0` including `PASS F17 … ids=S051` is measured on the landed
bytes, not inferred. Independently reproduced by ExecHarnessAfter at `87b14892…` (same
code, one docstring clause shorter) and its receipt `.ufo/waves/round-34/wave1/ExecHarnessAfter.md` §7b.

### 6. Demonstrations (scratch copies at the final bytes; lane read-only during them)

Script `/fast/scratch/hyaku/kasegi-r34/ExecFrontierBidirectional/demo.sh` (deleted at
cleanup; 60-line output quoted below, `demo_exit=0`). Each real-entry demo copies
`corpus/README.md`, `corpus/knowledge/` and `corpus/source-snapshots/` into scratch, so
the only delta from the green run is the mutated line.

```
== 0. before bytes from lane base 014ee2d7..., after bytes from the worktree
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  .../before.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  .../corpus/instruments/frontier-recheck-count.py
  228 .../before.py
  433 .../corpus/instruments/frontier-recheck-count.py

== 1. real-entry reverse demo: F16 header 'source: S050' line dropped
header source: lines left = 1
-- before bytes (base 014ee2d7...):
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049           exit=0
entries=20 pass=20 exit=0
before_exit=0
-- after bytes (worktree):
FAIL     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049           exit=-    problems=selection-not-declared-by-entry
entries=20 pass=19 exit=1
after_exit=1

== 2. real-entry forward demo: '--source S050' dropped from the F16 recheck line
-- before bytes (base 014ee2d7...):
FAIL     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=-    problems=header-sources-not-rechecked
entries=20 pass=19 exit=1
before_exit=1
-- after bytes (worktree):
FAIL     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=-    problems=header-sources-not-rechecked
entries=20 pass=19 exit=1
after_exit=1

== 3. limb mutants on the after bytes, against the instrument's own fixtures
-- mutant reverse-removed (one direction deleted):
   landed exit=1 FAIL F98 knowledge/fixture.md ids=S001,S002 exit=- problems=selection-not-declared-by-entry
          entries=1 pass=0 exit=1
   mutant exit=0 PASS F98 knowledge/fixture.md ids=S001,S002 exit=0
          entries=1 pass=1 exit=0
-- mutant forward-removed (one direction deleted):
   landed exit=1 FAIL F98 knowledge/fixture.md ids=S001,S002 exit=- problems=header-sources-not-rechecked
          entries=1 pass=0 exit=1
   mutant exit=0 PASS F98 knowledge/fixture.md ids=S001,S002 exit=0
          entries=1 pass=1 exit=0

== 4. no-op control: a replacement identical to the original changes no bytes
noop_changes_bytes=False

== 5. FR ledger fixtures (limb-ledger.json rows FR-missing-entry / FR-duplicate-entry)
-- fr-missing-entry
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
exit=1
-- fr-duplicate-entry
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
exit=1

== 6. ledger find-strings still occur exactly once in the worktree bytes
FR-missing-entry       find_count=1
FR-duplicate-entry     find_count=1
demo_exit=0
```

Reading of each row:

* **1 — the R9 mutant, now killed.** With the F16 entry's `source: S050` line deleted
  (one header `source:` line left) and base instrument bytes, the harness prints
  `PASS F16 … exit=0`, `entries=20 pass=20 exit=0` — `MutEntryF16.md`'s survivor,
  reproduced at the current row count. With the landed bytes the same tree prints
  `problems=selection-not-declared-by-entry`, `entries=20 pass=19 exit=1`.
* **2 — the forward limb is unchanged.** Deleting `--source S050` from the F16 recheck
  line fails on both generations with the same name, `header-sources-not-rechecked`.
  This is the "dropping a `--source` now fails" demonstration on the named entry; the
  reverse direction is row 1.
* **3 — both limbs are load-bearing.** Deleting the reverse check from the landed bytes
  flips the reverse fixture `FAIL`→`PASS`; deleting the forward check flips the forward
  fixture the same way. Each mutant makes exactly one substitution (`find` count asserted
  = 1), so no other limb can explain the flip.
* **4 — no-op control.** A replacement identical to the original changes no bytes and
  therefore cannot be banked as a mutation.
* **5/6 — the frozen FR ledger rows still bind.** Both fixture roots print the same
  verdicts as before, and each row's `find` string still occurs exactly once in the landed
  bytes, so `limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` is not
  staled by this edit. I did not run the ledger gate (parent-owned); the find-count check
  is the applicable pre-condition.

### 7. Residue — stated, not hidden

1. **Evidence-list header drops are not caught.** For F01–F05, a source is declared twice
   (header line + evidence items), so deleting the header line still leaves it declared and
   rule A does not fire; the entry loses only the header's URL/section provenance. Closing
   that needs the five legacy entries rewritten to the F09/F10/F13/F14 shape (one header
   line per declared source) and then a header-only rule — an entry-content change outside
   this seat's assigned file, and the L1's decision. The instrument docstring and
   `corpus/instruments/README.md:823-829` state this residue verbatim.
2. **`selection-not-cited-by-entry` remains the weaker limb.** It now excludes declaration
   lines, so it fires on an id mentioned nowhere except the recheck line, but a prose
   mention anywhere satisfies it (`S050.txt:70` style). The load-bearing side of rule A is
   the declared-set equality, not citation.
3. **Pin drift.** `SKILL.md:1069` cites `aa60b581…` inside a dated "Measured at append time
   (working tree, 2026-10-25)" sentence — a dated measurement, not a live target; this
   receipt and README §783 carry the current worktree digest. Any other doc that pins
   `aa60b581…` as a live digest needs the L1's refresh decision.

### 8. Scratch

All fixtures and demo trees lived under
`/fast/scratch/hyaku/kasegi-r34/ExecFrontierBidirectional/` and were deleted before this
receipt was finalised (`demo.sh`, `demo.out`, `before.py`, `demo/`, selftest temp dirs).
The lane did see one transient artefact from my `python3 -m py_compile` sanity call,
`corpus/instruments/__pycache__/frontier-recheck-count.cpython-314.pyc`; it is gitignored,
was not committed, and I deleted it (`git status --porcelain corpus/instruments` shows only
`M corpus/instruments/frontier-recheck-count.py`, `M corpus/instruments/README.md` from this
seat, plus the other seats' `M capture-binding-check.py`, `?? kill-rule-check.py`,
`?? r-defect-closure.sh`).

### 9. Hand-off checks for the parent

* `python3 corpus/instruments/frontier-recheck-count.py` → `entries=20 pass=20 exit=0`
  (measured, this receipt §5); `--selftest` → `selftest cases=6 failures=0`, exit 0.
* `limb-mutation-check.py --ledger …` → expected `limbs=13 killed=13 survivors=0`
  (find-counts verified unchanged here, counter not run by this seat).
* `ExecHarnessAfter`/`ExecRegressionC1`/`ExecRegressionC2`: the tree is green at
  `entries=20 pass=20 exit=0` on `1be79af6…`. The red readings those seats reported came
  from the superseded `2cff234e…` draft, whose reverse limb was header-only (rejected in
  §3, `entries=19 pass=14 exit=1`). Two later digests carried the landed rule with docstring
  corrections only: `87b14892…` and `8a79010d…`. MutFrontierRuleA pinned `8a79010d…` and
  was told it was final before the last docstring fix moved the bytes to `1be79af6…`; that
  ping-pong is this seat's error and is disclosed here rather than smoothed over. Rule code
  is byte-identical from `87b14892…` onward.
