# ConnR25Continuity — round-25 frozen metric spans (revenger/no-harm baseline)

Seat: `L1Kasegi26.ConnR25Continuity` (round 26, wave 1). Read-only reconstruction;
no production edit was made. All strings below are quoted byte-exact from the lane
at the named revisions. Access dates: 2026-10-25 (UTC).

## Revision pins

| label | commit |
|---|---|
| round-25 base (claims `base_revision`) | `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` |
| round-25 tip (spotcheck scope end) | `41a77b83f3a338053fa69629d753546b8d592617` |
| round-25 claims.json first/only commit on tip lineage | `98261ebaf06b6415badaec362c69623d0e1db880` (`round-25: repair rechecks and assimilate vendor policies`, parent `b49948f`, ancestor of `41a77b8`; confirmed `git merge-base --is-ancestor 98261eb 41a77b8` = 0) |
| round-26 freeze (current HEAD) | `1b076fa7f2fb5e7dd9d87449514eba526043421b` |

Two sibling commits (`60bad6c`, `e8de75a`) share the identical tree
`ab953de03dbcf88104825eddb9f00a9b3bb552ab`, parent `b49948f`, and the same
message/timestamp as `98261eb`; only `98261eb` is on the tip lineage (the other
two never appear in `git log 41a77b8 -- .ufo/waves/round-25/claims.json`).

## 1. C1 claim counters: before `lines=35 pass=6 fail-closed=23 exit=1`, after `lines=37`

The round-25 `claims.json` (commit `98261eb`) carries the predicate and before/target
prose; the exact counter strings live in the receipts/index. Quoted from
`.ufo/waves/round-25/claims.json` at `98261eb`:

- C1 predicate: `"Every `recheck:` line in corpus/knowledge/*.md is a single shell command that (a) parses under `bash -n`, (b) produces the same exit status AND the same combined stdout+stderr digest when run from the lane root and from a foreign cwd (/), and (c) names at least one lane-relative corpus/ path or a ~/Projects/ base test, with every named corpus/ path existing under the lane root. The audit prints one verdict per line and lines=35 pass=N exit=0|1."`
- C1 `target`: `"lines=35 pass=35 exit=0"`; C1 `before`: `"pass=6 (23 lines are prose+command hybrids that fail `bash -n`; 6 are cwd-dependent: lane-root exit 0, foreign-cwd exit 2)"`
- `counter_notes.counter_repair`: `"strict limbs and completeness rule added after mutation seats proved the frozen counter reachable by degenerate controls; receipts before/after on final instrument digest c3c19adc…"`
- `counter_notes.surface_interaction`: `"C2 adds two files; final tree is 37 lines, so report frozen-surface (35) and final-tree (37) separately."`

Before (committed bytes, exit 1) — `.ufo/waves/round-25/c1-before.json` at `41a77b8`:
`lines = 35`, `pass = 6`, `fail_closed = 23`, `failing_limbs = {'parse': 23, 'cwd': 6, 'paths': 0}`.
`c1-before-strict.json`: `instrument_sha256 = c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`,
`lines = 35`, `pass = 6`, `pass_strict = 6`, `broken = 23`, `complete = True`, exit 1.
Index line 5 (before): `lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`.

After — frozen surface (35 files, F10 entries removed) — `c1-after-35.json`:
`lines = 35`, `pass = 35`, `pass_strict = 35`, `fail_closed = 23`, exit 0.
Index line 9: `lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`.

After — final tree (37 entries, with F10) — `c1-after.json`:
`lines = 37`, `pass = 37`, `pass_strict = 37`, `fail_closed = 23`, `gated = 23`, `broken = 0`,
exit 0. Index line 13: `lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`.

## 2. Instrument digest and the receipt-index line-4 cross-reference

`.ufo/waves/round-25/c1-instrument-digest.txt` at `41a77b8`, verbatim (line 1):
```
instrument=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f
```
Cross-checks: `sha256sum corpus/instruments/recheck-audit.py` (current worktree) =
`c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`, and
`git show 41a77b8:corpus/instruments/recheck-audit.py | sha256sum` = the same value
(the instrument is tracked at tip, blob `146d349480419ec5c920cbdc739e0820a432cfd7` —
this contradicts the wave-2 residual-risk note claiming it untracked; the bytes are
committed and digest-pinned). Every strict receipt pins the same `instrument_sha256`.
The index contains no selftest line (`grep -c selftest` over `c1-receipt-index.txt` = 0).

Actual line 4 of `.ufo/waves/round-25/c1-receipt-index.txt` (verbatim, `41a77b8`):
```
executes=12 gated=0 broken=23  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
```
wave-2 cross-reference, `.ufo/waves/round-25/wave2/C1InstrumentDigest.md` at `41a77b8`:
- line 53: `### 3. Selftest at the pinned digest (index line 4 claims `cases=14 failures=0 exit=0`)`
- line 65: `Matches `c1-receipt-index.txt:4` exactly.`

Verdict: the cross-reference is a misreference (routed defect R25-2, confirmed). Line 4
is the `executes=12 gated=0 broken=23` summary, not a selftest tally; the index has no
selftest line at any position. The selftest tally `cases=14 failures=0 exit=0` is
evidenced only in wave-2 prose, exactly as R25-2 states.

## 3. d24-3 receipts exist

`.ufo/waves/round-25/d24-3/` at `41a77b8` contains: `dispatch-mut8.json`,
`contain-mut8.json`, `receipt.txt`, `digests.txt`, `mut-bound8.py`.

`receipt.txt` summary lines (verbatim):
```
cases=8 pass=8 exit=0
sha256 resolver=88122e10e94cb74eefcd39841061ca128317bb7d0a81733f1cdb7d51c2234285 matrix=fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c checker=acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1
exit=0
...
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=88122e10e94cb74eefcd39841061ca128317bb7d0a81733f1cdb7d51c2234285 matrix_sha256=d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809
exit=0
```
JSON receipts agree: `dispatch-mut8.json` totals `cases=8 pass=8 exit=0` (liveness 4,
controls 4, resolver sha256 `88122e10…`); `contain-mut8.json` totals
`cases=24 pass=24 fail=0` (escape 12, controls 12). This is the landed-byte mutant
measurement cited by lesson M25-3 and R11/QUALITY.md (`88122e10…`: dispatch 8/8,
containment 24/24).

## 4. Fix-control #3 text and the retained historical line at `corpus/lessons/round-24.md:77`

Round-25 lesson, `corpus/lessons/round-25.md` lines 193–197 (verbatim):
```
3. **One measured number per artefact (M25-3).** Control: run the counting command against a
   scratch copy with one quote removed — it must print 75; and
   `grep -rn '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md
   corpus/lessons/round-24.md` returns 0 hits after this round's corrections (the round-24
   lesson keeps its historical sentence and carries an appended erratum, R9).
```
Retained historical line `corpus/lessons/round-24.md:77` — identical at base `b49948f`
and tip `41a77b8` (verbatim):
```
it was written; `source-recheck.py` exits 0 over 19 records / 77 assertions.
```
(The pattern hit is the `77 assertions` spelling; the `62 assertions` stale figure named
in M25-3 is absent from all three files at base — pre-round-24 corrected state.)

Measured grep behavior:
- Old (un-restated) pattern at tip, exact lesson spelling
  `git grep -n '62 assertions\|77 assertions' 41a77b8 -- corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md`:
  exactly **1** hit — `41a77b8:corpus/lessons/round-24.md:77:it was written; `source-recheck.py` exits 0 over 19 records / 77 assertions.`
  Same on the current worktree: `corpus/lessons/round-24.md:77:… / 77 assertions.` (1 hit).
- Restated (round-26 C1 counter: `… | grep -v 'round-24.md:77' | wc -l`): **0**.
- `corpus/instruments/README.md` and `SCORECARD.md` have 0 hits for either spelling at
  tip (corrections landed); at base, `SCORECARD.md:510` also carried
  `(19 records, 77 assertions, exit 0)` — i.e. the pre-fix pattern would have hit 2
  files, and the round-25 fix left exactly the retained historical sentence.

## Summary of the baseline (for revenger/no-harm)

| metric | before | after (frozen 35) | after (final 37) |
|---|---|---|---|
| C1 `lines=`/`pass=` | 35 / 6 | 35 / 35 | 37 / 37 |
| `fail-closed=23` | 23 (parse 23, cwd 6) | 23 (parse 0, cwd 0) | 23 (parse 0, cwd 0) |
| exit | 1 | 0 | 0 |
| instrument digest | — | `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` | same |
| index line 4 | `executes=12 gated=0 broken=23` (no selftest line in index) | — | — |
| d24-3 receipts | exist at tip: dispatch `8/8`, containment `24/24`, resolver `88122e10…` | — | — |
| fix-control #3 | pre-fix: hit at `round-24.md:77` (+ `SCORECARD.md:510` at base) | un-restated still 1 hit (retained `:77`); restated 0 | — |

Blocker: none. All items reconstructed from read-only git history (`git log/show/ls-tree/
grep/merge-base`) and read-only filesystem reads; no writes outside the two report files.
