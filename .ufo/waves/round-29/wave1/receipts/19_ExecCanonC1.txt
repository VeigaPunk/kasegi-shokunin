# ExecCanonC1 — canonical C1 receipt index (round 29, wave 1)

Seat: `ExecCanonC1` (executor, leaf). Role: canonical C1 receipt index; runs
last for C1. UTC measurement window: 2026-10-25T18:16Z–18:17Z. Model run on:
`inception/mercury-3` (workstation route; no model passed by me). Tooling: no
tool installed/upgraded (nothing needed; pacman untouched).

## Sequencing (M28-1 compliant)

At wave start (18:16Z) the production file was still the base bytes — sha256
`23818c1204…7396`, identically the C1 do-nothing control digest
(`c1-controls/before.txt`): 9 selftest cases, no `limbs=` assertion, git-free
run crashes with `FileNotFoundError: 'git'`. I did **not** run the counters in
that state. I coordinated with the implementer peer `ExecImplC1-2`; it replied
that the fix had landed (digest `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`).
I re-hashed the production file, confirmed that digest, then ran all captures.
No PRE-STATE number is compared to an after column here.

## Captures (all at the landed digest `68e1bdc…`, 561 lines)

(a) `python3 corpus/instruments/anchorcheck.py --selftest`:

```
selftest cases=12 failures=0
limbs=9 covered=9
selftest_exit=0
```

(b) git-free PATH run (frozen counter 3, verbatim):

```
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
nogit_exit=0
```

Clean skip, no traceback, exit 0.

(c) `python3 corpus/instruments/anchorcheck.py SKILL.md`:

```
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
skill_exit=0
```

(d) instrument_sha256: `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`
(re-hashed with `sha256sum corpus/instruments/anchorcheck.py` immediately before
writing the receipt; the second hash taken right before the write is
byte-identical).

## Frozen C1 kill-rule check

| target | measured | result |
|---|---|---|
| selftest cases = 12 | 12 | PASS |
| failures = 0 | 0 | PASS |
| limbs = 9 | 9 | PASS |
| covered = 9 | 9 | PASS |
| nogit_exit = 0 | 0 | PASS |
| `c1-receipt-index.txt` has instrument_sha256 line matching committed digest | `68e1bdc…` | PASS |

No value differs from target. Full receipt: `.ufo/waves/round-29/wave1/c1-receipt-index.txt`.

## Notes / risks

- The receipt pins the **production working-tree digest**. The kill rule's
  "committed anchorcheck.py digest" is satisfied only if the landed file is
  committed unchanged (the L1/scribe commit step must not modify it; the digest
  should be re-checked at post-commit recheck by `ExecPostCommitRecheck`).
- `limbs=9 covered=9` is asserted by the instrument itself against the actual
  case set (12 cases: 9 fail limbs, each with an isolating failing fixture, plus
  3 controls), so the limb-coverage claim is self-checked by the selftest.
- Git-free hermeticity: `SKIP pin-broken (git not found)` — the pin case
  degrades to a skip, which is the declared clean behavior; the run still
  asserts its remaining limbs and exits 0.
- No other file was touched by this seat; only the two assigned outputs were
  written (`c1-receipt-index.txt`, this report).
