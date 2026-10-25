# C1CwdReplay — wave-2 falsification of claim C1 (depth:verifiability)

**Verdict: CONFIRMED.** The wave-1 result stands: every `recheck:` line in
`corpus/knowledge/*.md` (37/37 final tree) is a single `bash -n`-clean command whose
exit status AND sha256(stdout + \x00 + stderr) are identical when run from the lane
root and from `/`. No correction required.

## What was attacked

claims.json C1 (`claims.json:8-21`), limb (b) specifically: "same exit status AND the
same combined stdout+stderr digest when run from the lane root and from a foreign cwd
(/)" — plus the instrument-level claim that the audit prints `lines=37 pass=37 exit=0`.
Wave-1 receipts attacked: `.ufo/waves/round-25/c1-after-35.{txt,json}` (frozen 35) and
`.ufo/waves/round-25/c1-after.{txt,json}` (final tree 37).

## Commands run and outputs

### 1. Independent replay harness (does not import the instrument)

`/tmp/c1cwd/replay.py` reimplements the instrument's exact formula —
`bash -c <line>` with `cwd=lane-root` then `cwd=/`, digest =
`sha256(stdout + b"\x00" + stderr)` — plus a lane-root **repeat** run per line to catch
nondeterminism that a two-cwd check could mask, plus `bash -n` and `corpus/` path
existence checks.

```
$ python3 /tmp/c1cwd/replay.py
entries=37  cwd_fail=0  nondet=0  parse_fail=0  paths_fail=0
REPLAY_EXIT=0
```

Every one of the 37 lines: parses, exits identically from both cwds, byte-identical
combined output, deterministic across a repeated lane-root run, names at least one
`corpus/` path or `~/Projects/` base test, and every named `corpus/` path exists.
Raw data: `/tmp/c1cwd/replay.json`.

### 2. The instrument itself, run from both cwds

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/recheck-audit.py --json /tmp/c1cwd/inst-lane.json
LANE_EXIT=0
  ... strict pass=37/37 cdroot_fail=0 instrument_fail=0 own_fail=0
  lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0

$ cd / && python3 .../recheck-audit.py --root .../kasegi-shokunin --json /tmp/c1cwd/inst-foreign.json
FOREIGN_EXIT=0
  ... strict pass=37/37 ... lines=37 total=37 pass=37 ... exit=0

$ diff /tmp/c1cwd/inst-lane.txt /tmp/c1cwd/inst-foreign.txt
TEXT_IDENTICAL          # byte-identical stdout, all 40 lines

$ (summary compare)
SUMMARY_EQUAL           # JSON summaries identical including all 37 entry records
```

### 3. Live replay vs the committed wave-1 receipt

Compared every entry in `c1-after.json` against the fresh lane-root run for
`lane_exit`, `foreign_exit`, `lane_output_sha256`, `foreign_output_sha256`:

```
entry sets: receipt=37 inst=37
MISMATCHES: none — receipts match live replay byte-for-byte
receipt summary: lines=37 total=37 pass=37 pass_strict=37 fail_closed=23
                 foreign_cwd='/' instrument_sha256=c3c19adc…
```

The committed receipt is honest and nothing has drifted since capture: all 74 stored
exit codes and 74 stored digests equal live values exactly.

### 4. Supporting facts

- Instrument digest: `sha256sum corpus/instruments/recheck-audit.py` =
  `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` — matches
  `c1-instrument-digest.txt` and the receipt header. The audited instrument is the
  committed one.
- Selftest: `python3 corpus/instruments/recheck-audit.py --selftest` →
  `cases=14 failures=0`, exit 0 (matches `c1-receipt-index.txt:4`).
- Exactly one `recheck:` line per file: `grep -c '^recheck:'` over 37 files → all `1`.
  The only other `recheck:` occurrence is mid-line prose in
  `vendor-disclosure-policy-commitments-crosswalk.md:38`, which `^recheck:` cannot match.
- Frozen vs final surface: `c1-receipt-index.txt:11-19` records 35/35 (frozen, before
  the two C2 entries) and 37/37 (final). Current tree has 37 files; the wave-1 claim's
  dual reporting is accurate.
- `fail-closed=23` is genuine, not a pass-through: `~/Projects/bounties`,
  `~/Projects/the-bounty-hunter`, `~/Projects/origin-work` are absent (`ls` exit 2);
  `~/Projects/ufo-fsd-alpha` exists. The 23 gated lines exit 1 identically from both
  cwds — limb (b) is about equality, not success — and class `gated` is honestly
  reported.

## Residual gap (does not void the claim)

The cwd limb is proven only for `/` as foreign cwd under the same HOME. A foreign
cwd with a different HOME (e.g., another user) could change `~` expansion: the
`root-loss-2026-10-12.md` line asserts `test -e ~/Projects/ufo-fsd-alpha` and would
flip status for a user lacking that dir. The frozen predicate fixes foreign cwd at
`/` and says nothing about HOME, so this is out of claim scope — noted for honesty.

## Tooling directive

No installs or updates performed. Used only system python3/bash/diff/sha256sum.

## Verdict

**CONFIRMED.** Wave-1 C1 (both surfaces, 35/35 frozen and 37/37 final, exit 0)
reproduces exactly under independent re-derivation; receipts are byte-accurate.
Smallest correction needed: none.
