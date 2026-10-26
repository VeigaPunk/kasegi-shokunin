# ConnCrossPattern — cross-claim / cross-source pattern scan over landed round 31 (wave 2)

- **Seat:** `ConnCrossPattern` (connector, leaf — no subagent dispatch, no background jobs)
- **Round/milestone:** kasegi-shokunin round 31, hyaku run 7, wave 2 (falsify)
- **Answering model:** `inception/mercury-3` (session config route table; no model passed by this seat)
- **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope; this receipt is the only write)
- **Lane base:** `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`; HEAD at measurement `eecad59db166e0626ca2472e96ea48bc28a35153`
- **Scope:** read wave1 + wave2 receipts as they land; report (1) shared patterns worth a QUALITY criterion or a SKILL.md line with file:line evidence, (2) silent C1↔C2 dependencies (recheck-audit strict pass N vs knowledge-expected.txt vs the F15 entry's recheck line), (3) sibling-lane mutation/limb-harness precedents to align with.
- **Tooling:** no install/upgrade, no pacman transaction, no network fetch, no git/jj mutation (read-only `rev-parse`/`status` only).

## 0. Bytes measured and receipts read

Wave-2 receipts read (all landed before this receipt was written): `MutCtrAlwaysKilled.md`, `MutCtrSignalIgnored.md`, `MutCtrNoCompileCheck.md`, `MutCtrNonUniqueFind.md`, `CritCalibration.md`, `CritExpansion.md`, `RevEntryQ.md`, `RevRowS048.md`, `RevQuoteRoutes.md`, `RevQuoteRoles.md`, `ScoutLiveDrift.md`, `ExecLimbRAparse.md`, `ExecLimbRAcwd.md`, `ExecLimbRApaths.md`, `ExecLimbRAcdroot.md`, `ExecLimbRAinstrument.md`, `ExecLimbRAown.md`, `ExecLimbRAcompleteness.md`, `ExecLimbRAexpectmissing.md`, `ExecLimbRAexpectunexpected.md`, `ExecLimbSRstemmismatch.md`, `ExecLimbSRoccurrencenotunique.md`, `ExecLimbFRmissingentry.md`, `ExecLimbFRduplicateentry.md`; wave1 `ExecCounter.md`, `ExecLedgerMerge.md`, `CritC1Kill.md`, `ConnOwnership.md`, `ConnClaims.md`, `ConnSibling.md`, `ExecEntryF15.md`, `ExecExpectedList.md`, `ExecHarnessC2.md`.

Quiescent digests at 2026-10-26T00:31–00:33Z (sha256sum, listed once here; repeated at the bottom of this receipt for the runs it covers):

```
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
d6f25227b6025bb070740cd38c03783092dbcb51340e5c99689c9c1737b8f156  corpus/instruments/knowledge-expected.txt
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be  corpus/source-snapshots/round-31/manifest.json
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
```

One combined quiescent read of both claims' counters (this seat's run, lane root):

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print "frontier_admitted=" n+0}' corpus/README.md
frontier_admitted=15
$ grep -lE '^source: S048 ' corpus/knowledge/*.md | wc -l        → 1
$ grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md  → 1
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 48
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
$ python3 corpus/instruments/recheck-audit.py --quiet | head -5
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048 | tail -1
S048:Q8 OK occurrences=1        # recheck_exit=0
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed   … 13 lines, all killed …
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

Both claims hold on one byte-set; every number above is a measured output, and the C1 summary matches the byte-identical stdout sha256 `9b386485…` already in `SKILL.md:1069`-adjacent receipts (`ExecLedgerMerge.md` §2, `CritCalibration.md` §1).

## 1. Shared patterns worth a QUALITY criterion or a SKILL.md line

### P1 — "exactly-once in a frozen byte-set" is one constraint, two spellings (QUALITY Q9 and R17)
- `corpus/QUALITY.md:64` (Q9): the quote is "exactly-once in the capture (or carries an `anchor`…)", and the check "prints the occurrence count it observed"; the failure name is `reason=occurrence-not-unique` (`source-recheck.py:194`).
- `corpus/QUALITY.md:96` (R17): the mutant is "an exact-once `find`/`replace` over the instrument's own bytes"; the failure name is `invalid:find-count` (`limb-mutation-check.py:428-430`).
- Both are the same discipline: a byte string asserted to occur once in a frozen input; both are enforced by counting, not by first-match; both fail closed on multiplicity. Evidence this round: `ExecEntryF15.md` §6 measured 13 entry quotes at `occurrences=1`; `ExecLedgerMerge.md` §1 re-counted all 16 ledger `find` texts as exactly-once; `MutCtrNonUniqueFind.md` §"Ground fact" re-measured all 16 at 1.
- Worth **one SKILL.md line**: in the round-31 gate row area (`SKILL.md:1064-1067`), state that Q9's `occurrences=1` and R17's `invalid:find-count` are the same singleton-occurrence gate over different frozen inputs (capture vs instrument), and that a patch/mutant whose find text is ambiguous is refused before being run. No new QUALITY criterion needed; a cross-reference line prevents the two spellings drifting apart.

### P2 — "frozen input" = digest pin + exactly-once assertions, in both claims
- C2 pins a capture: manifest `sha256` + 8 `occurrences=1` assertions (`corpus/source-snapshots/round-31/manifest.json`; `source-recheck.py:171-174,188-213`).
- C1 pins instrument bytes: the do-nothing control cites base instrument hashes (`claims.json:26`), and every counter/merged receipt names the subject digests (`ExecLedgerMerge.md` §1; `ExecCounter.md` §1).
- Same idea, one object is a web capture, the other a source file. The wave-2 live-drift probes (`ScoutLiveDrift.md`, `RevQuoteRoutes.md` §2, `RevRowS048.md` §1.1) show the capture pin is line-2-Trace-Id-fragile for whole-file hashes but stable for exactly-once assertions — i.e. the assertion layer, not the whole-file digest, is the load-bearing pin. Worth a SKILL.md registry column already exists (`pinned-value path`); propose a one-line gloss in the round-31 gate row that the *assertion set* is the pin; whole-file digest equality is not re-fetch reproducible.

### P3 — double-run determinism before any live-vs-mutant or before-vs-after comparison
- `limb-mutation-check.py:371-381` (`measure_runs`) runs each side twice and requires the same `(exit, signal)`; the mutant side is a separate fresh scratch (`invalid:mutant-baseline`). This is the counter-side embodiment of M30-3 (bound 6: in-flight outputs are non-comparative) and of `ExecHarnessC2.md` §0 (two identical digest sets 125 s apart).
- Proposal: one QUALITY line (or a SKILL.md line next to the gate row) — "a counter compares only quiescent bytes, and each side of a mutation run must reproduce itself; a number measured on moving bytes is PRE-STATE and compares to nothing."

### P4 — a kill rule's gates must be exercised by committed data, else they are dead clauses (the strongest shared finding)
- `MutCtrNonUniqueFind.md` shows the frozen counter mutant `find-text-not-unique accepted` **survives**: every committed `find` occurs exactly once, so the `invalid:find-count` gate is extensionally identical to the mutant's `== 0` predicate; the mutant prints the exact C1 summary lines at exit 0. The hole is only closed by a fourth control (`CTL-find-count`, proposed, not landed — landing changes `controls=3 rejected=3` and requires an L1 claims amendment).
- The same shape appears on the C2 side: the entry's `recheck:` note says "8 assertions, every quote exactly-once", but the entry carries 10–16 S048 quote spans while the manifest asserts 8 (`RevEntryQ.md` F2; `RevQuoteRoutes.md` §6 F1; `RevQuoteRoles.md` L-7). A future edit to any unasserted span passes `source-recheck --source S048` unchanged — the note overstates what the instrument binds.
- These are two instances of one rule: **what a claim says its instrument checks must equal the instrument's real assertion set, and every gate the kill rule names must be exercised by at least one committed control/fixture.** This extends R11 (`QUALITY.md:65`, "A counter's instrument is part of the claim… its discrimination against degenerate and mutated instruments") from pass-count discrimination to *gate coverage*: a gate no committed row exercises is dead. Proposal: an R18 (or a SKILL.md line at `SKILL.md:1069` after the measured-at-append paragraph): "a kill rule names only gates that at least one committed control or fixture exercises; a required-verdict path no row reaches is a dead clause."

### P5 — receipts are commands + output, and a "green" number without a byte-set is stale-live
- `CritCalibration.md` found 12 stale-live statements whose numbers are wrong against live counters but whose counters are fine; H2/H5/H9 show the dated, digest-pinned receipts are correctly historical. The concrete discipline: every number in a receipt names the digest or UTC it was measured on (`ExecExpectedList.md` §3; `ExecHarnessC2.md` §0). This is already R2/R6/R9 text; the new, worth-echoing detail is that C1's own counter summary is pinned by stdout sha256 (`9b386485…`), so a re-run that prints different bytes is a different result even with the same exit code.

## 2. Silent dependencies between C1 and C2

### D1 — the C1 regression guard literally reads C2's landing: `strict pass=N/N` where N = committed expected-entry count
- `recheck-audit.py:44-56` (docstring): when `corpus/instruments/knowledge-expected.txt` exists, the audit requires set equality between the committed list and the tree; an extra entry prints `unexpected=<name>` and reds.
- `claims.json:25` (C1 kill rule, verbatim): "recheck-audit.py --quiet must still print `strict pass=N/N` with N equal to the committed expected-entry count and exit 0". The N is deliberately dynamic.
- `ConnOwnership.md` §5 measured the transient: the moment `ExecEntryF15` lands the entry before `ExecExpectedList` appends it, the audit prints `expect=present expected=43 missing=0 unexpected=1 exit=1` — a false C1 regression. `ExecExpectedList.md` §2/§3 closed it: 43→44 entries, `strict pass=44/44`, exit 0.
- So C1's "real corpus regresses" clause is a *function of C2's completion*: a C2 landing without its expected-list pair fails C1. That is not a defect — it is the intended lockstep — but it is a silent dependence that must stay sequenced (entry → expected-list → quiescent audit). Worth a SKILL.md line naming `ExecExpectedList` as the atomic pair of any new knowledge entry.

### D2 — C1's regression clause and C2's counters run the same instruments
- C1 kill-rule half-clauses (`claims.json:25`): "source-recheck.py --selftest failures=0; frontier harness pass == entries, exit 0".
- C2 counter commands 6 and 7 (`claims.json:44-45`): `frontier-recheck-count.py` and `source-recheck.py --manifest …/round-31/manifest.json --source S048`.
- Same two instruments; C1 checks them at selftest/fixture level, C2 at live-data level. Either instrument regression breaks both claims' counters. The C1 ledger's 13 limbs are exactly the load-bearing guarantees of these two instruments plus `recheck-audit.py` — i.e. **C1 is the mechanism-level warranty behind C2's numbers** (D3).

### D3 — the SR limbs directly guard the gate C2's S048 recheck passes through
- C2's `source-recheck … --source S048` passes `occurrences=1` on all 8 quotes and the B1 stem check; the two gates are `source-recheck.py:123-126` (B1: `Path(path).stem != source_id` → `reason=stem-mismatch`) and `source-recheck.py:188-199` (B2: `occurrences > 1` without a verified anchor → `reason=occurrence-not-unique`).
- C1's `SR-stem-mismatch` and `SR-occurrence-not-unique` limbs mutate exactly those two gates and prove them load-bearing (`limb-ledger.json:95-113`; `ExecLimbSRstemmismatch.md` §1/§2; `ExecLimbSRoccurrencenotunique.md`). If either limb were a survivor, C2's S048 recheck exit 0 would be an ungrounded number.
- Same for the RA family: `RA-expect-missing`/`RA-expect-unexpected` guarantee the expected-list behavior that D1's audit line depends on (`limb-ledger.json:75-93`), and `FR-missing-entry`/`FR-duplicate-entry` guarantee the harness's fail-closed shape that `entries=18 pass=18` relies on (`limb-ledger.json:115-133`).
- Conclusion: the two claims are not parallel surfaces; C1's ledger is a *precondition warranty* for C2. Any future C2 admission that touches a recheck instrument must re-run the affected limbs first — a sequencing rule worth one SKILL.md sentence.

### D4 — the F15 entry's recheck note overstates instrument coverage (intra-C2, but it is the C2-side face of P4)
- Entry L4 says "8 assertions, every quote exactly-once"; measured real bound = 8 of 10–16 spans (`RevEntryQ.md` F2; `RevQuoteRoutes.md` F1; `RevQuoteRoles.md` L-7). Not a C2 predicate failure (the kill rule only requires asserted quotes to be exactly-once-or-anchored), but it is a self-description that will silently lie after any edit to an unasserted span. Same class as the `MutCtrNonUniqueFind` dead-gate finding; both are routed to the L1 (manifest extension or note narrowing; a fourth control plus claims amendment).

### D5 — score-gap.py parses the same audit bytes
- `SKILL.md:1071` and `ConnOwnership.md` §5 show `score-gap.py` runs `recheck-audit.py --quiet` and parses `executes/gated/broken`; its numbers are therefore only meaningful on quiescent bytes, and F15's landing moved `executes` 19→20 while holding `gated=24`. Proposal 2 and both claims share one quiescence barrier.

## 3. Sibling-lane precedent (mutation/limb harnesses)

Fleet scan: only kasegi has `corpus/instruments/` (`find /home/vgpnk/Projects/shokunin -maxdepth 4 -type d -name instruments -path '*corpus*'` → kasegi only). Sibling mutation/limb harnesses live elsewhere; the closest precedents:

1. **kama-shokunin/tests/report-audit/isolation-mutants.py:5-9** — "Each mutant removes or weakens exactly one element (one literal source replacement that must match exactly once). A mutant is killed only when the grid's current arm reports a violation (exit 1)"; `:21-25` fail-fast: a non-exactly-once replacement is `could-not-evaluate` for the whole run and kills nothing; `:41-44` exit contract 0 = pristine passed and every mutant ran, 2 = could not evaluate; survivors are reported "without a necessity claim" (`:9-10`); retired ids are never reused (`:14-20`). This is R13's isolating-fixture + honest-survivor discipline already in fleet shape.
2. **kotoba-shokunin/verifiers/check_sweep_mutants.py:41-46** — the frozen mutant table is embedded as a literal with a sha256 over `json.dumps(TABLE, sort_keys=True)`, and the target is pinned to a base rev (`git_show` at `:213-223`); `:286-313` `synthetic_full_kill()` builds a fixture where every mutant dies and every equivalent stays green; equivalents are counted separately from mutants (`:277-283`). This is the same "full-kill fixture + equivalents-not-inflated" idea as kasegi's `CTL-equivalent → survivor`.
3. **kumitate-shokunin/scripts/gate-mutants.mjs:35** (`MIN_CONTROL_CASES`), `:596-603` (`countOccurrences`/`applyLiteral`), `:525-529` (`confirmKill`: the second run must also kill with the same sorted FAIL names), `:553` (`gateExitCode`). Controls with minimum case counts and a two-run kill confirmation mirror C1's double-run determinism (P3).

Alignment recommendations (for one SKILL.md or QUALITY line, not new code): (a) adopt the sibling vocabulary "killed only when the observable moves; a survivor is never a necessity claim" — kasegi already has it in R17, keep it explicit against sibling naming; (b) keep the kama rule "a replacement that does not match exactly once is cannot-evaluate for the whole run (exit 2)" — kasegi's `invalid:find-count` per-row verdict is a compatible, more granular form; (c) kasegi's ledger adds what siblings lack: a per-row `signal` regex and an isolating-fixture note, which is what makes a kill attributable to one gate (this round's SR/RA receipts prove it) — worth stating as the lane's differentiator so it is not flattened in a fleet-wide convention.

## 4. Risks / routing (not fixes; this seat writes only this receipt)

- `MutCtrNonUniqueFind`'s fourth control is not landed and **cannot** land silently: the frozen summary line is `controls=3 rejected=3`, so the change requires an L1 claims amendment (appended erratum), not a ledger bump.
- R16/R17 (`QUALITY.md:95-96`) ground in `corpus/lessons/round-31.md`, which was absent at measurement (`CritCalibration.md` G4; ScribeLesson in flight) — a reference-drift risk if that seat does not land.
- The counter's verdict enum is a superset of the frozen interface (`invalid:import`, `invalid:mutant-baseline`, `invalid:timeout`), disclosed in `corpus/instruments/README.md:400-403` but needing an L1 acceptance (`CritCalibration.md` G3).
- All numbers in this receipt are pinned to the digests in §0; if the L1 commit changes any subject byte, the before/after columns here are stale and must be re-run (M30-3).

Verification: the commands above are this seat's own runs on the quiescent bytes; no further check was run and no byte of the lane was modified other than this receipt.
