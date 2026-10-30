# R48Review23 — x-mark rejection vs canonical checker claim

Seat: R48Review23 (critic, leaf — no subagent dispatch)
Axis: depth:verifiability
Question assigned: **Evaluate rejecting x marks: does restricted author-side scope contradict canonical checker claim? Quote predicate and normative source.**

## Frozen inputs (read-only, hashed at review time)

- Claim file `.ufo/waves/round-48/claims.json` — sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matching `freeze.txt` (`claims-sha256: b8022cdf…`); frozen commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`; base `903d47e13058982460f0d90c1c2b9c7c02680646`.
- Protocol source snapshot `.ufo/waves/round-48/controls/protocol-source.txt` (S077: normative protocol File contract and Promotion gates).
- Checker under test: `corpus/instruments/shonen-form.py` (frozen counter), selftest `shonen-form-selftest.py` (context only).
- Round-47 verifier routes: R1 = SHONEN.md canonical-form drift (`corpus/lessons/round-47-verifier-spotcheck.md` §6) — the routed defect C1 closes; R2 = plain-target phrasing — read for context, not exercised by this question.

## Quoted predicate and normative source

Frozen claim C1, `predicate`:

> "SHONEN.md conforms to the canonical four-box author-assessment grammar with existing local evidence pointers; this is form validation, not promotion or evidence truth."

Frozen claim C1, `mechanical_limits` (the scope under review):

> "Specific author-side grammar: x marks are rejected (independence cannot be established mechanically). Evidence pointer existence is checked, not semantic truth. Scores held; no source restoration or end-to-end bounty task claimed."

Frozen claim C1, `kill_rule` (relevant clause):

> "Semantic evidence and promotion stay independently judged."

Normative source, Promotion gates (`.ufo/waves/round-48/controls/protocol-source.txt:66-68`):

> "The lane's own assessment is `[~]` asserted (with its evidence pointer); only a non-author `<id>` may write `[x]`, and any `[x]` carrying no named non-author verifier is author attestation counting as `[~]` for the gate."

Normative source, File contract SHONEN.md row (`protocol-source.txt:446`):

> "Verification is mechanical: the seed block … must diff byte-identical modulo `<name>` …, and marks are confined to the box character plus one indented evidence line per box — `[x] <verifier-id>` or `[~]` with a resolvable pointer; no other prose, added boxes, or removed boxes."

Normative source, canonical template marks note (`protocol-source.txt:464-465`):

> "Marks: `[~]` asserted by the lane itself (evidence pointer required), `[x]` only with a named non-author verifier per **Promotion gates**."

Checker x-rejection branch (`corpus/instruments/shonen-form.py:46-47`):

```python
if mark == 'x':
    return 'SF-VERIFIER'  # This author-side checker cannot attest independence.
```

## Bounded probes (scratch fixtures only; production untouched)

Scratch root `/fast/scratch/hyaku/kasegi-r48/R48Review23/` (removed after this report landed). Exact commands and observed output:

1. **Live tree (expect_after of the frozen claim).**
   Command: `python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin`
   Expected: `shonen-form canonical=1 finding=SF-CLEAN exit=0`. Observed: `shonen-form canonical=1 finding=SF-CLEAN exit=0` (exit 0). Match.

2. **Mutant A — box 1 `[~]`→`[x]`, evidence line byte-identical (valid pointer `SKILL.md`).**
   Expected: `canonical=0 finding=SF-VERIFIER exit=1`. Observed: `shonen-form canonical=0 finding=SF-VERIFIER exit=1` (exit 1). Match — the checker's disclosed x rejection.

3. **Mutant B — box 1 `[x]` with its evidence line removed.**
   Expected: `canonical=0 finding=SF-EVIDENCE exit=1` (the `elif mark != ' '` branch precedes any mark-level verdict). Observed: `shonen-form canonical=0 finding=SF-EVIDENCE exit=1`. Match — and it documents precedence: x-without-evidence is an evidence defect first.

4. **Mutant C — box 1 `[x]`, evidence line names the verifier id as the pointer token (`Evidence: verifier-42 — SKILL.md reviewed; …`).**
   Expected: `canonical=0 finding=SF-POINTER exit=1` (pointer validation runs before the mark check). Observed: `shonen-form canonical=0 finding=SF-POINTER exit=1`. Match — a verifier-id-first line cannot reach SF-VERIFIER.

Probe breadth note: the committed selftest (`shonen-form-selftest.py:13-19`) exercises SF-CLEAN, SF-PREAMBLE, SF-NEWLINE, SF-TRAILING, SF-BOX, SF-EVIDENCE but contains no SF-VERIFIER or SF-POINTER case (grep-confirmed). The scratch mutants above supply the missing live evidence for the x path; no checker source was amended — the frozen counter is reported as observed, byte-for-byte.

## Strongest counterexample and why it fails

Counterexample tested: the File contract's mechanical grammar lists "`[x] <verifier-id>` or `[~]`" as confined marks, so a file whose box a genuine non-author verifier marked `[x]`, with a resolvable pointer, satisfies the protocol's canonical-file grammar — yet the frozen checker returns `canonical=0` (mutant A). If the frozen claim asserted "the checker passes every file the protocol calls canonical," this would be a direct contradiction.

It does not assert that, on four independent grounds:

1. **The claim's own scope text discloses the rejection verbatim.** `mechanical_limits` states "x marks are rejected (independence cannot be established mechanically)." The frozen predicate is bounded to the "author-assessment grammar"; the checker's behavior is the frozen, disclosed realization of that bound. A claim and its counter behaving exactly as the claim's limits describe is conformity, not contradiction.
2. **The normative Promotion gates assign x-semantics to non-author reviewers, not to tools.** Line 66-68 makes the lane's own assessment `[~]` and decrees that an `[x]` whose non-author verifier cannot be named "is author attestation counting as `[~]` for the gate." Independence is a provenance judgment the protocol itself forbids a lane-side mechanism to make ("a subagent the lane dispatched is still the lane"). A mechanical author-side checker that attested x would arrogate the reviewer's gate; rejecting x defers to it. This is fail-closed in the direction the protocol points.
3. **No duplicate authority is created.** The checker declining x does not block or grade promotion; it reports that the author-side form is not the author's own `[~]` assessment. Promotion authority stays with the non-author reviewer per the Promotion gates, and the kill rule keeps "semantic evidence and promotion … independently judged."
4. **The claim's measurable surface is unaffected.** C1's `after` state is `shonen-form canonical=1 finding=SF-CLEAN exit=0` on the measured SHONEN.md, whose four boxes carry only `[~]`/`[ ]` (live probe 1: green). No kill-rule clause involves x marks.

## Verdict

**No contradiction.** The restricted author-side scope is consistent with the frozen canonical checker claim: the x rejection is disclosed in the claim's own mechanical limits, grounded in the normative Promotion gates (author assessment = `[~]`; x belongs to non-author reviewers; unverifiable x degrades to `[~]`), and fail-closed rather than authority-duplicating. The residual tradeoff — the lane checker is strictly narrower than the protocol's mechanical file contract and rejects even genuinely verifier-marked x boxes, and its committed selftest does not exercise the SF-VERIFIER path (covered here by live scratch mutants) — is a scope boundary, not a defect the frozen claim must reject. No counter bytes or predicate were amended; defeats, where observed, are reported as observed (none — all four probes matched expectation).

## Receipts

- Report (this file): `.ufo/waves/round-48/wave1/R48Review23.md`.
- Fixtures: `/fast/scratch/hyaku/kasegi-r48/R48Review23/{fixture,fixtureB,fixtureC}/` — created for the probes above, removed on exit.
- No production edits. No git/jj mutation. No fleet/sibling/domain-tree writes. No delegation, no background jobs.
- Tooling: no installs or upgrades for this seat (host `python3` 3.14.x sufficed; pacman untouched).
- Bounded verification only: the assigned probes above; no build/lint blanket run.
