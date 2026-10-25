# MutC1A2 — C1 mutant-A2 (duplicate detection removed), round-30 wave-1

Seat: `MutC1A2` (L2 mutation-tester leaf, kasegi lane). Assignment: after the
round-30 instrument update lands, create mutant-a2 (A2 duplicate detection
removed) from `corpus/instruments/frontier-recheck-count.py`, run the A2
fixture against it, show it exits 0 with pass=2 — the flip — and record
sha256 + outputs. Report trailer: `.ufo/waves/round-30/wave1/MutC1A2.md`.

## Instrument-update poll

The post-update digest was already on disk at first read (no sleep-poll
needed): `CritC1Kill-attack/digests-before.txt` and `ExecImplFrontierHarness.md`
record the landed harness digest `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`.
Live bytes measured at probe start confirm it: `sha256sum corpus/instruments/frontier-recheck-count.py`
→ `aa60b581…` (matches; the do-nothing-control base digest `c8a62888…` is no
longer live).

## Mutant-a2 (scratch-only; live instrument never touched)

Method: copied the live instrument byte-for-byte into an isolated scratch copy
`.ufo/waves/round-30/wave1/MutC1A2-scratch/frontier-recheck-count.py` (scratch
hash at copy = `aa60b581…`, identical to live). Mutated only the scratch copy,
removing exactly the round-30 A2 limb (the smallest behavior-bearing point):

- deleted the `seen_realpath` duplicate scan + `DUPLICATE-ENTRY` print
  (was lines 202–213);
- `fail_closed = duplicate is not None or not records or passed != len(records)`
  → `fail_closed = not records or passed != len(records)`;
- deleted the JSON receipt key `"duplicate_entry": duplicate[2] if duplicate else None`.

A1 missing-entry limb, per-row prints, summary line shape, exit semantics for
all other outcomes, and the `--root`/`--json` CLI are untouched.

Mutant sha256 (before restore): `9232ca169a9202f045251d8dd0a511b0ffc5c70a9a84ffe128b289c35191f8ae`.

## Detector (C1 counter-A, same command as claims.json)

`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 <instrument> --root .ufo/waves/round-30/c1-controls/harness-root-a2; echo "a2_exit=$?"`
plus the isolation probe on `harness-root-a1`.

## Outputs (all measured, exit codes captured)

### Pristine (live instrument, `aa60b581…`)
```
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
```
`a2_exit=1` — names both duplicate rows and the entry (claim-faithful).
JSON receipt: `entries=2 pass=2 duplicate_entry='knowledge/dup-entry.md'`.

### Mutant-a2 (scratch, `9232ca169a…`)
```
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
entries=2 pass=2 exit=0
```
`a2_exit=0` — **the flip**: no `DUPLICATE-ENTRY` line, pass=2 retained, exit 0.
JSON receipt: `entries=2 pass=2 duplicate_entry=None`.

### Isolation probe (mutant on A1 fixture)
```
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
```
`mutant_a1_exit=1` — the A1 missing-entry limb still fails closed; only the A2
limb was removed.

## Verdict

**KILLED (flip observed).** Removing the A2 limb flips the C1-A2 fixture from
exit 1 (naming the duplicate) back to exit 0 / pass=2 — exactly the mutant
behavior C1's `mutants` clause stipulates. The fixture therefore exercises the
duplicate-detection limb: the limb is load-bearing and the C1-A2 predicate is
verifiable, not dead code. Asserted claim C1-A2 stands (pristine exit 1 names
the duplicate); the mutant is a coverage/verifiability positive, not a claim
failure.

## Restoration evidence

- Live instrument sha256 unchanged across the whole probe: `aa60b581…`
  before, during, and after (measured at each stage).
- Scratch restored by re-copying live bytes: restored scratch sha256 =
  `aa60b581…` (identical). Re-run of the A2 detector on the restored scratch:
  `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`, `entries=2 pass=2 exit=1`,
  `restored_a2_exit=1` — byte-exact return to pristine behavior.
- Fixture bytes measured (read-only, never modified): `harness-root-a2/corpus/knowledge/dup-entry.md`
  `ff725848…`, `corpus/README.md` `fac44baa…`, `source-snapshots/round-24/manifest.json`
  `b32443bb…`, `S003.txt` `1054e187…`.
- Scratch artifacts kept under `MutC1A2-scratch/` (pristine/mutant receipts).
  No file outside the lane repo and outside the seat's wave-1 dir was written;
  working-tree only, no git/jj mutation, no live target contacted, no tools
  installed (none needed), no pacman transaction.
