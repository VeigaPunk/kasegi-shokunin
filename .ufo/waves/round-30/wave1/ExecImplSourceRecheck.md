# ExecImplSourceRecheck — round-30 wave-1 (C1 limbs B1+B2)

Seat: ExecImplSourceRecheck (L2 executor leaf). Lane: kasegi-shokunin.
Assignment: implement C1 limbs B1+B2 in `corpus/instruments/source-recheck.py`
(single owner). No tool was installed (tooling rule read from
`~/.omp/agent/RULES.md`; nothing needed beyond stdlib).

## Files changed (only write scope)

- `corpus/instruments/source-recheck.py` — the only production file touched
  (module docstring, `anchor_verdict`, `check_source`, `selftest`, `--selftest`
  help text).
- Evidence artifacts written under `.ufo/waves/round-30/wave1/`:
  `ExecImplSourceRecheck.pre.py` (pre-edit bytes), `ExecImplSourceRecheck.diff`
  (unified diff), `ExecImplSourceRecheck-b2/{manifest-clean-b2.json,
  manifest-clean-b2-anchored.json,S0B2.txt}` (clean B2 demonstration fixtures).
- No commit/push; no git/jj mutation; no write to fleet root, siblings, or
  read-only package trees.

## Implementation

**B1 (stem binding, Q9).** In `check_source`, immediately after path-form
validation: `if Path(path).stem != source_id:` → emit
`<id>:manifest MISMATCH reason=stem-mismatch` and return 1. Returns 2 still
only for config errors (invalid path/sha256/quotes), preserving the exit
convention (1 = mismatch, 2 = unavailable).

**B2 (occurrence/anchor gate, Q9).** `anchor_verdict` now returns `(note,
verdict)` with verdict ∈ `unique|ok|missing|out-of-range|broken`. In the
assertion loop, a quote whose normalized occurrence count > 1 passes only when
verdict == `ok`; otherwise it emits a MISMATCH with the reason and sets
status=1:

- missing anchor → `reason=occurrence-not-unique` (exactly the frozen predicate wording)
- out-of-range anchor → `reason=anchor-out-of-range`
- broken anchor → `reason=anchor-broken`

Unique quotes keep prior behavior untouched (their B-broken anchor note stays
visible but non-fatal; `occurrences=N` and `normalized=markup-whitespace` lines
unchanged).

**Selftest.** Added 5 cases (9 total): `stem-mismatch` (exit 1,
`reason=stem-mismatch`), `double-occurrence` (exit 1,
`reason=occurrence-not-unique`), `double-occurrence-anchored` (exit 0,
`anchor=6-ok`), `double-occurrence-out-of-range` (exit 1,
`reason=anchor-out-of-range`), `double-occurrence-broken` (exit 1,
`reason=anchor-broken`). Each case asserts exit code, the complete emitted-id
list, empty stderr, and the expected reason substring. Added the required
summary line `selftest cases=N failures=0`.

## Measured evidence (all runs at the landed bytes)

| Check | Command | Result |
|---|---|---|
| Selftest | `python3 corpus/instruments/source-recheck.py --selftest` | 9/9 PASS, `selftest cases=9 failures=0`, exit 0 |
| C1 B1 counter | `… --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043` | `S043:manifest MISMATCH reason=stem-mismatch`, `b1_exit=1` |
| C1 B2 counter | `… --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b2.json --source S045` | `S045:manifest MISMATCH reason=stem-mismatch`, `b2_exit=1` (see Risk 1) |
| Clean B2 (missing anchor) | `… --manifest …/ExecImplSourceRecheck-b2/manifest-clean-b2.json --source S0B2` | `S0B2:Q1 MISMATCH reason=occurrence-not-unique`, exit 1 |
| Clean B2 (anchored) | `… --manifest …/manifest-clean-b2-anchored.json --source S0B2` | `S0B2:Q1 OK occurrences=2 anchor=1-ok`, exit 0 |
| Real manifests | `… --manifest corpus/source-snapshots/round-{23,24,25,26,28,29}/manifest.json` | all exit 0; every assertion OK; non-unique real quotes (S029 art14-2a-early-warning anchor=10, S036 Q9 anchor=15, S041 Q2a anchor=1874) verify `anchor=N-ok` |
| Frontier harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=17 pass=16 exit=1`, FAIL F14 `problems=missing-entry` (see Risk 2) |

## Diff + digest

- Before (working tree == base, matches claims do-nothing control):
  `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96`
- After: `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`
- Unified diff: `.ufo/waves/round-30/wave1/ExecImplSourceRecheck.diff` (217 lines).

## Risks / blockers

1. **Frozen B2 fixture trips B1 first.** `manifest-b2.json` declares `id=S045`
   with `path=B2.txt`, so the new B1 stem check fires before the occurrence
   gate; the frozen counter b2 therefore exits 1 with
   `reason=stem-mismatch`. That satisfies the kill rule (exit 1 + a failure
   reason) but does not exercise the B2 limb, and a B2-dropping mutant would
   not flip under this fixture. The B2 limb is instead demonstrated exactly by
   the selftest `double-occurrence*` cases and by the clean S0B2 fixtures
   above. Recommended: append a corrected B2 fixture (path stem == id, e.g.
   record `S0B2` → `B2.txt`) as a separate appended control so the occurrence
   gate is individually isolable.
2. **Frontier harness mid-wave state.** F14 is already admitted in
   `corpus/README.md` but its knowledge entry is not yet on disk (another seat
   owns it), so the harness reports `FAIL F14 problems=missing-entry` —
   `entries=17 pass=16 exit=1`. This is wave-in-progress state, not a
   regression from this change (source-recheck.py is untouched by the harness
   path; before receipt measured entries=16 pass=16 with no F14 row). Re-run
   the harness after the F14 entry lands.
3. Real-manifest regression check passed for every committed manifest
   (rounds 23–29), so the C1/C2 "every real manifest recheck that passed at
   base must still pass" conjunct holds at the current bytes.
