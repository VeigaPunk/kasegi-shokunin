# RevCorrectionsFinal — round 41 correction review

**Verdict: PASS for the assigned correction checks.** Textual checks were run on the integrated lane files; this does not claim final Y verification.

- Exact `grep -c '^Correction (round 41)'` counts: `SCORECARD.md` **8**, `LOG.md` **3**, `SHONEN.md` **3** (each meets >=1).
- The three records' correction blocks collectively name `RevC1Counters.defeats.txt`, `CritKillRule.md`, and `MutH6H10.md`, and state that round-40 C1 is **not verified** on the frozen counter.
- `SCORECARD.md` and `LOG.md` enumerate the `closed=10/10 exit=0` receipt truth at Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5`; `SHONEN.md` repeats that receipt truth. All three disclose the D2 transcript gap: the round-40 Y receipt lacks a selftest transcript and the graded tally is scratch Y′/report-only.
- Token-boundary check: `closed=7/80` and `failures=10` occur in three correction lines, solely as quoted T2 defect/false-green evidence from `RevC1Counters.defeats.txt`; they are **not presented as correction result values**. Actual receipt results named by the corrections are `closed=10/10 exit=0` and the transcript gap is expressly called out.
- Semantic LSP status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool.” The required literal grep/count and targeted record reads were used; no grep is represented as semantic proof.

No final Y verification is claimed.