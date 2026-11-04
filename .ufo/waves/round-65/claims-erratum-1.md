# Round-65 claims erratum 1 — driver base reference and base-trial pin scope

Appended after the freeze (`57cb8dec1cd3a688b0f8a23f5b6b434656592577`) and before any final measured run.
It corrects the driver, not the claim: the predicate, metric, kill rule, target values and axes are
unchanged.

## What the frozen record says

`claims.json` pins `driver_sha256 = 533a6d4f536431d3a043e48c29b250ea4690432a3994f4216c6a04bd6051eb5b`
and C1's predicate names that hash.

## Defect (found by the first final-mode run, not by a seat score)

The frozen driver resolved the "base gate" from `--revision`. At the base revision that is correct; at a
later measured revision it read the landed implementation as if it were the base, so:

- `probes-base` expected the base gate's two signal false-greens and read the fail-closed gate instead;
- `mutbat-base-limb-absent` expected `killed=0/4 limb=absent` and read the limb-bearing gate.

Receipt: `controls/final-verification-pre-erratum-r65.txt` — `VERIFY measurements=8 failures=2` at
`1c36d724c91cdd8585219798ea7cf60bb4f24b5b` with driver `533a6d4f…`.

Separately, a base trial (no `--candidate`, no `--final`) counted the gate pin against the base tree,
adding a spurious fourth failure to the before-state.

## Amendment (counter only)

1. The base gate is read at `--base-rev`, defaulting to `claims.json`'s `base`, else `--revision`.
2. In a base trial the gate pin is not counted (`input-hashes … gate-pin=base-tree`); the other four
   pins still apply. With `--candidate` or `--final` all five pins apply.

Amended driver: `.ufo/waves/round-65/verify-r65.py`, sha256
`5aa842abdceac676ff8c0a1b90f641bbad93a9505161f192dde85b1a1d06aaaf`. The `driver_sha256` field in
`claims.json` is superseded by this erratum in the direction of this byte string; the frozen file is not
rewritten.

## Unchanged

Predicate after-state `VERIFY measurements=8 failures=0`, before-state `failures=3` at
`a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`, metric `driver failures`, kill rule, both axes, both score
cells and the C2 predicate.

Receipts after the amendment: `controls/driver-base-donothing-finaldrv-r65.txt` (8/3, exit 1, driver
`5aa842ab…`), `controls/driver-construction-finaldrv-r65.txt` (8/0), and the final run
`controls/final-verification-r65.txt` at the measured revision.
