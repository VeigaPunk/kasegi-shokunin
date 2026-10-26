# Round-34 cl erratum 1 — C1 counting-literal scope (filed by the L1, pre-integration)

Filed: 2026-10-26, before any scoring seat's verdict was finalized (wave still in
flight; this is the L1's record, mirroring round-33's Rule-B erratum discipline).

## What the frozen claim says

`claims.json` C1's `counting_commands` list includes:
`python3 corpus/instruments/capture-binding-check.py -> records=40 bound=40 unbound=0 exit=0 (unchanged C1 instrument baseline)`.

## Why the literal no longer matches the tree

Round 34's own C2 capture adds a manifest record to the audit surface:
`corpus/source-snapshots/round-34/S051.txt` (Immunefi VSCS v2.2) with record id
S051. The capture-binding-check audit enumerates the whole snapshot set, so the
landed record count is 41 (the 40 round-33 records plus S051), not 40. The
binding invariant is unchanged: every record bound, `unbound=0`, exit 0.

## Ruling

The literal "40" in the counting command is a snapshot-of-round-33 scope note,
not the invariant. The C1 predicate sentence and kill rule are unchanged:

- predicate: committed `capture-binding-check.py` audit prints exit 0 with
  `bound=records` and `unbound=0` on the landed tree;
- measured after-state (once S051's registry row lands): `records=41 bound=41
  unbound=0 exit=0`;
- intermediate state (before the S051 row lands) is not a measurement state:
  it prints `unbound=1` with the named FAIL `rule=no-row record=S051`, exit 1 —
  which is itself the proof that rule B binds a record to its registry row.

This erratum is committed before any final C1/C2 after-state is measured or
reported, and it is disclosed on every surface that reads the C1 counter.
