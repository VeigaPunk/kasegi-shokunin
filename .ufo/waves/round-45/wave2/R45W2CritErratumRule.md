VERDICT: BROKEN

Seat: R45W2CritErratumRule (process critic, leaf). Question: is v1 -> v1.1 of `corpus/instruments/r45-routed-defects.py` (C1 counter) a legitimate counter erratum, or a changed rule?

Decision: NOT a legitimate erratum as recorded. Most of v1.1 is a changed rule (new pass conditions the printed sentences do not state), one change is an unsanctioned widening (an environment override), one wave-1 attack is still open, and the v1.1 header's "predicate ... unchanged" label is true only for the prose sentences. A small subset (listed in Finding 2) qualifies as an erratum.

Artifacts (all re-derived by me):
- v1 = `git show 8cf62c879e6e6b031e67412f8fac1fba0bd378cf:corpus/instruments/r45-routed-defects.py`, sha256 `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee` (matches the digest the v1.1 header cites).
- v1.1 = same path at lane commit `6662a4276b6f7bd61e23e12058414e09dd71b9e4`, sha256 `680c881af4a5f9a660c203c7a9e7e44e5ba4a860870e0d655121709e34f2fb67` (from `git archive` export; my export matched).
- Frozen claims `.ufo/waves/round-45/claims.json`, sha256 `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206` (matches `freeze.txt` `claims-sha256`).
- Export roots used: base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`, integration `6662a42` (both via `git archive | tar -x`).

## Governing text (quoted)

1. Round prompt `.ufo/prompts/kasegi-round-45.md` lines 543-546 (the prompt has no literal "section 9"; this is §6 item 9, "Claim sizing"):
   "A rule changed after any seat has scored is not the claim's rule, whatever attacks it later passes (kumitate r42). Freeze one predicate that is the same sentence in the plan, the same condition in the counter's code and the same label in the receipt."
2. C1 `kill_rule` in the frozen claims: "...or if the counter's predicate sentence (five limbs R1-R5) is changed after a seat has scored (bug fixes that keep the predicate are logged as counter errata, not new rules)."

Two conditions follow. The sentence condition is satisfied (Finding 1). The "same condition in the counter's code" condition is not (Finding 2).

Timeline (verified): v1 frozen (`freeze.txt` `frozen-at: 2026-10-28T20:55:34Z`; commit committer time 17:55:40 -03:00); wave-1 results `wave1-results.json` mtime 18:29; v1.1 integrated in `6662a42` at 18:34:13 -03:00. Wave-1 seats scored v1 before v1.1 existed.

## Finding 1 — sentence level: unchanged (verified)

Command (python, extracted the WHAT IT MEASURES block of each docstring, removed the v1.1 VERSION block):
```
r45 WHAT-IT-MEASURES lines v1: 33  v1.1 (VERSION block removed): 33  identical: True
(no prose diff)
```
So the v1.1 header claim "predicate and limb names unchanged" is true for the prose sentences only.

## Finding 2 — code predicate: limb-by-limb diff of v1 against v1.1 (verified by `diff -u`)

Classes: BUG-FIX = a v1 pass that the printed sentence itself forbids; NEW CONDITION = a pass-set narrowing the sentence does not state; WIDENING = a new pass path; CONTESTED = arguable either way.

| Limb | v1 -> v1.1 change | Class |
|---|---|---|
| R1 | registry rows read only under `## Registry`, outside code fences and HTML comments (`registry_lines`) | BUG-FIX (sentence: "a NEW registry row") |
| R1 | `raw_row_line` must match exactly once (was: first match) | NEW CONDITION |
| R1 | recheck script run from the counter's own lane, not the graded tree (`TOOL_ROOT`) | CONTESTED (sentence names no script location) |
| R1 | snapshot sha must equal `PINS["S072.txt"]` (`counter:177`) | NEW CONDITION (sentence: "a sha-pinned snapshot") |
| R1 | lesson correction must carry a quoted span of >=30 chars, >=6 words, located in the S072 snapshot | NEW CONDITION (fixture D) |
| R1 | flip check `re.search(r"flip:\s*\S", teaches)` UNCHANGED (`counter:158`; v1 `:110`) | NOT FIXED (fixture A) |
| R2 | `enforced-by` path must be a regular file (was: exists) | CONTESTED |
| R2 | each criterion >=300 characters | NEW CONDITION |
| R2 | each criterion must cite `corpus/lessons/round-44.md:N` with N in range | NEW CONDITION |
| R3 | `r44-frontier-count.py` byte pin (`counter:249`) | NEW CONDITION (a stub printing the tokens satisfies the sentence literally) |
| R4 | `freeze-check.py` byte pin (`counter:276`) | NEW CONDITION (same as R3) |
| R4 | `claims.json` must equal the frozen bytes (`counter:284`) | NEW CONDITION (value grounded in `freeze.txt`) |
| R4 | replay now runs with `--tool-root TOOL_ROOT` from the counter's lane (was: tree root) | changed oracle |
| R5 | invocation must be the literal line `$ python3 ... --root <tip> --selftest --work <scratch>`, exactly once; `exit=0` exactly once after it (`counter:300`) | NEW CONDITION (fixture C) |
| R5 | refiled body must sha-match a pinned one-run output (`counter:316`); the header says this replaces a re-run | NEW CONDITION |
| R5 | `r44-routed-defects.py` byte pin (`counter:312`) | NEW CONDITION |
| all | `R45_PINS_OVERRIDE` env var replaces `PINS` from a JSON file (`counter:75-77`) | WIDENING, unsanctioned (fixture B) |
| dead | `CENSUS` constant removed (`grep -c CENSUS v1.py` printed `1`, i.e. unused) | neutral |

The counter's `main()` is identical in v1 and v1.1. Its only arguments are `--root` and `--baseline` (`grep -n add_argument v11.py` printed `326: ap.add_argument("--root", required=True)` and `327: ap.add_argument("--baseline", required=True)`). There is no selftest mode, so the header comment on the override ("selftests only: the grader's environment, never the graded tree's") describes behaviour the code does not have.

## Finding 3 — discrimination against the do-nothing control and the integration tree (re-run)

Commands: `python3 v1.py --root <X> --baseline <base>` and `python3 <int>/corpus/instruments/r45-routed-defects.py --root <X> --baseline <base>`.

- Do-nothing base, v1: `routed-defects total=5 fixed=0 unresolved=5 exit=1`.
- Do-nothing base, v1.1: `routed-defects total=5 fixed=0 unresolved=5 exit=1`.
- Integration `6662a42`, v1: `routed-defects total=5 fixed=5 unresolved=0 exit=0`.
- Integration `6662a42`, v1.1: `routed-defects total=5 fixed=5 unresolved=0 exit=0`.

The change is invisible at the verdict level on the claim's own measured tree. Only the R5 `read=` token differs (`refiled=ok original=unchanged` in v1, `refiled=pinned-run-output original=unchanged` in v1.1). So the erratum was not needed to hold the claim. It was needed to close attacks, which is the case §6 item 9 forbids.

## Finding 4 — attack fixtures (each a single change to a copy of the integration export; re-run)

A. Attack wave-1 `R45RevLimbR1.md:26` names: S072 `flip:` clause replaced by `flip: tbd`.
- v1: `routed-defects total=5 fixed=5 unresolved=0 exit=0`
- v1.1: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`, total `fixed=5`.
- Result: the vacuous-flip attack still passes v1.1. The v1.1 header (`counter:41`) lists "vacuous `flip: tbd`" as a wave-1 falsification, but the binding list (lines 42-46) does not include it, and the regex at `counter:158` is unchanged.

B. Tampered pinned `freeze-check.py` (one appended comment line), with the override JSON carrying the tampered digest.
- v1.1, no env: `limb R4 fixed=0 read=freeze-check-not-the-pinned-bytes`; `routed-defects total=5 fixed=4 unresolved=1 exit=1`
- v1.1 with `R45_PINS_OVERRIDE=<json>`: `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2`; `routed-defects total=5 fixed=5 unresolved=0 exit=0`
- Result: the pin is bypassed by an environment variable that no sentence declares. The override is a live pass path in the graded run, not a selftest path.

C. Receipt invocation rewritten to real paths (`--root <lane>/x/tip --selftest --work <lane>/x/work`). The printed sentence ("carries the selftest invocation without the failed bare call ... exit=0") is still satisfied.
- v1: `total=5 fixed=5`.
- v1.1: `limb R5 fixed=0 read=invocation-lines=0`; `total=5 fixed=4 unresolved=1 exit=1`.
- Result: a NEW CONDITION that rejects a receipt the sentence accepts.

D. Lesson correction line (`corpus/lessons/round-44.md:205`) with all quote marks removed. The sentence ("an appended `Correction (round 45` line ... that cites S072 and the size token") is still satisfied.
- v1: `total=5 fixed=5`.
- v1.1: `limb R1 fixed=0 read=lesson-correction-absent-or-quotes-no-located-S072-span`; `total=5 fixed=4 unresolved=1 exit=1`.
- Result: a NEW CONDITION (quote-location) that rejects a sentence-compliant correction.

## Finding 5 — the same pattern in the C2 counter (diffed; control receipts compared)

`diff` of `r45-c2-gate.py` v1 (`8cf62c8`, sha256 `5e07961…`) against v1.1 (`6662a42`, sha256 `639a038a…`): it adds PINS for `S071.txt`, `manifest.json` and `base-knowledge-names`; requires the knowledge dir to equal the base names plus F27 and the F27 entry to be >=3000 bytes; counts uncited curly quotes; and adds the same override hook (`c2-v11.py:63-64`, `if os.environ.get("R45_PINS_OVERRIDE")`). v1 read `SOURCES_CENSUS` from the environment; v1.1 replaces that with an env override of the pins. The env-var hole is moved, not closed.

The control receipts changed. Commands: `grep "C2\|c2" freeze-controls.txt freeze-controls-v1.1.txt`, output:
```
freeze-controls.txt:control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 expect=RED got=RED
freeze-controls.txt:control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED
freeze-controls-v1.1.txt:control c2-junk-row counter=C2 c2-gate fixed=2/7 exit=1 expect=RED got=RED
freeze-controls-v1.1.txt:control c2-fabricated-quote counter=C2 c2-gate fixed=3/7 exit=1 expect=RED got=RED
```
All stay RED. But `claims.json` still names `.ufo/waves/round-45/controls/freeze-controls.txt` (v1 values) as the control. The v1.1 control receipt is a separate file (added in commit `6662a42`, `freeze-controls-v1.1.txt | 6 ++++++`).

## Finding 6 — the r44 precedent does not settle legitimacy under r45's text

- r44 `corpus/lessons/round-44.md` "Attempt 2, wave 2" (lines 154-172) records the v1 counter falsified by wave-2 seats and the v2 changes in a table. It is a precedent for the same practice: in-place counter hardening after a falsify wave.
- r44 v2 (`4aba89c`) docstring records the v1 digest (`7e7c145f831a04d4b094ce6fda228587368c2aee04baadbb8345404a8baca950`, verified against `8063547` by `git show | sha256sum`), gives a per-seat VERSION 2 block mapping each falsification to its answer, and states: "The frozen predicate (eight routed defects, 0 unresolved) and the frozen target are unchanged; the frozen counter string in `.ufo/waves/round-44/claims.json` is untouched." That is better record-keeping than r45's header.
- r44's frozen kill rule says only: "The list and predicate are not widened after freeze." It forbids widening. It does not forbid changing the predicate sentence, and it does not state the errata clause that r45's kill rule states.
- Even r44's "unchanged" is looser than the sentence level: v2 removed the docstring sentence "Append-only is enforced where the protocol demands it: ..." (`grep -c "Append-only is enforced" r44-first.py r44-v2.py` printed `1` and `0`).

So r44 is a precedent for the practice, not for legitimacy under §6 item 9 and r45's kill rule.

## Finding 7 — what a closure reader must see on record (required; currently missing or wrong)

1. The v1 digest `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee` and its retrieval path `8cf62c8:corpus/instruments/r45-routed-defects.py`. The v1.1 digest `680c881af4a5f9a660c203c7a9e7e44e5ba4a860870e0d655121709e34f2fb67` at `6662a42`. A v1.1 file cannot carry its own digest, so it must be in the record.
2. The statement that the WHAT IT MEASURES sentences are unchanged (Finding 1), replacing "predicate and limb names unchanged", plus the table in Finding 2 that lists the changed code conditions.
3. A per-attack map: each wave-1 attack, its v1 verdict, its v1.1 verdict. Currently attack A (`flip: tbd`) reads `fixed=1` under v1.1.
4. The `R45_PINS_OVERRIDE` hook in both counters, either removed or recorded as an open widening.
5. The two control receipts (`freeze-controls.txt`, v1; `freeze-controls-v1.1.txt`, v1.1 with changed C2 rows) and the fact that `claims.json` names the v1 file.
6. The C1 result under the frozen rule: the integration tree scores 5/5 under v1 and under v1.1; the do-nothing base scores 0/5 under both. No kill-rule trigger fires on those numbers. But the frozen counter (v1) is falsified by attack A, and that falsification must stay on record as an open counter defect.

## Finding 8 — smallest safe correction (recommendation)

a. Remove `R45_PINS_OVERRIDE` from both counters, or declare it a new rule that is not scored in this round.
b. Judge C1 on v1, the frozen rule. Record wave-1 falsifications as open counter defects, attack A first. Do not credit C1 with v1.1.
c. If the L1 wants v1.1 judged, declare it a counter v2 that is a new rule, not scored this round. Split out the BUG-FIX subset (registry rows outside fences, and `isfile`) as E1 only if the L1 wants that subset kept.
d. Correct the v1.1 header: replace "predicate and limb names unchanged" with "sentences unchanged; code conditions changed (see record)", and add the v1.1 digest and the per-attack map.
e. Leave `flip: tbd` open (or reject it as a new rule), and say so in the record.

## Limitations

- I ran the base and integration trees and fixtures A-D only. I did not re-run every wave-1 attack tree; I relied on the cited seat reports for the others (e.g. `R45RevLimbR1.md:26,37-39,57`) and report only what I re-ran.
- I did not re-run the C2 counter myself. C2 findings are from `diff` and the existing control receipts.
- The "section 9" reference is §6 item 9 of the prompt (no literal section 9 exists).
- Freeze timestamps are consistent: author-date 17:47:59 -03:00 precedes committer-date 17:55:40 -03:00 and the `frozen-at` stamp 17:55:34 -03:00. Not a finding.
- No tools installed or upgraded. Only read-only git (`log`, `show`, `archive`) was used. No commits, pushes, index or working-tree changes. Scratch was removed on exit.
