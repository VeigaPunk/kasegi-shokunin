# MutDeletionControls — C1 deletion-mutant controls (pre-fix receipts)

- Seat: `L1Kasegi26.MutDeletionControls` (mutation tester, leaf)
- Round/wave: kasegi-shokunin round 26, wave 1 (build)
- Date (UTC): 2026-10-25; run window 12:35:12Z–12:35:24Z
- Milestone: C1 deletion-mutant controls (do-nothing pre-fix receipts)

## Instrument under test

`corpus/instruments/recheck-audit.py` — **current pre-fix bytes** at measurement time:

```
sha256sum: c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f
```

(Matches the expected prefix `c3c19adc...` and the `.ufo/waves/round-26/c1-live.json` record.)
The sha was verified immediately **before and after** the full six-run batch and was stable
across it. The production instrument file changed to `503de028d64d7209947ed8c09c9fd507b165c846695468a0313b0abe2fccfd8c`
**after** the batch completed (concurrent peer fix work); every receipt below is therefore on
`c3c19adc` bytes.

## Method

- Fixture trees: snapshot copies of the lane's corpus at 2026-10-25T12:34Z, laid out as
  `<fixture>/corpus/...`, under
  `.ufo/waves/round-26/c1-controls/fixtures/{base,m1a,m1b,m1c,m1c2,m1d}`.
  Base has 37 knowledge files, each with a `recheck:` line.
- Detector run for every mutant:
  ```
  python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-audit.py \
      --root <fixture> --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin
  ```
- Raw outputs: `.ufo/waves/round-26/c1-controls/m1-*.txt`; machine summary:
  `.ufo/waves/round-26/c1-controls/m1-summary.json`.

## Results

| Mutant | Mutation | Exit | lines/total | strict pass | Verdict |
|---|---|---|---|---|---|
| A | delete whole knowledge entry `multiparty-vulnerability-coordination.md` | **0** | 36/36 | 36/36 | **survived** |
| B | delete the recheck line from one entry (file kept) | 1 | 36/37 | 36/37 | killed |
| C | rename own-file-naming entry `intake-surface.md` → `intake-surface-slug-changed.md` | 1 | 37/37 | 36/37 | killed |
| C2 | rename source-recheck-owned entry `multiparty-vulnerability-coordination.md` → `...-slug-changed.md` | **0** | 37/37 | 37/37 | **survived** (extra finding) |
| D | add stray extra knowledge file without recheck line | 1 | 37/38 | 37/38 | killed |
| E | base copy, no changes (do-nothing control) | 0 | 37/37 | 37/37 | baseline-ok |

## Verbatim detector output (summary lines)

- **A** (`m1-a.txt`): `lines=36 total=36 pass=36 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` — no line names the deleted entry.
- **B** (`m1-b.txt`): `lines=36 total=37 pass=36 ... exit=1` (completeness: `strict pass=36/37`).
- **C** (`m1-c.txt`): `intake-surface-slug-changed.md frozen=110 strict=110110 lane=1 foreign=1 gated FAIL`; `lines=37 total=37 pass=36 ... paths_fail=1 exit=1` (strict `own_fail=1`).
- **C2** (`m1-c2.txt`): `multiparty-vulnerability-coordination-slug-changed.md frozen=111 strict=111111 lane=0 foreign=0 executes PASS`; `lines=37 total=37 pass=37 ... exit=0`.
- **D** (`m1-d.txt`): `lines=37 total=38 pass=37 ... exit=1` (completeness: `strict pass=37/38`).
- **E** (`m1-e.txt`): `lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; `executes=14 gated=23 broken=0`. Base audit **passes** — no failing lines to quote.

## Findings

1. **Mutant A survives (exit 0)** — the C1 soundness gap is reproduced on current bytes:
   deleting a whole knowledge entry leaves `lines == total` (both shrink together), so the
   completeness check cannot see the loss and nothing names the missing entry. This matches the
   claim's before value `deletion_fixture_exit=0` and is the target of the fix (after: exit 1
   naming the deleted entry).
2. **Mutants B and D are killed (exit 1)** — the existing completeness check already catches a
   missing recheck line and an extra un-audited file.
3. **Mutant C is killed (exit 1)** — a slug rename of an entry whose recheck line names its own
   file fails the frozen `paths` limb (old path missing) and strict `own`.
4. **Mutant C2 survives (exit 0)** — extra coverage finding: renaming a *source-recheck-owned*
   entry is invisible to the audit. The `own` limb is satisfied via the `--source` +
   `corpus/source-snapshots/` pair, not the entry's own file, and the file/line counts stay
   equal. The C1 fix should be checked against this class too (or its scope explicitly recorded).
5. **Mutant E passes (exit 0)** — do-nothing control green on 37/37 frozen and strict; 14
   lines execute today, 23 are gated (fail-closed on absent bases). No baseline failures.

## Restoration evidence

- This seat made **no production edits**. The audit and its entry commands are read-only over
  the fixtures (entry commands `cd` into the live lane root, which they only read).
- Instrument sha bracketed the batch: `c3c19adc...` → `c3c19adc...`.
- Mutation state re-verified after all runs: A's entry absent; B's recheck-line count 0; C/C2
  renames present with originals absent; D's stray file present with 0 recheck lines.
- Fixture knowledge-tree digests after runs recorded in `m1-summary.json`. Fixtures are scratch
  receipt trees and are left in place for verifier re-audit; no restore-to-production step
  applies.

## Notes

- The item's example file `cnvd-canonical-advisory-cross-references-2026-10-23.md` does not
  exist in the current corpus; an existing entry (`multiparty-vulnerability-coordination.md`)
  was used for mutants A/B.
- Concurrency caveat: entry commands resolve support instruments (`source-recheck.py`,
  `anchorcheck.py`) via the live lane root (by design of `--cdroot`), so those runs saw the
  production support scripts at run time. The audited instrument itself was the frozen
  `c3c19adc` bytes for all six runs.

Report: `.ufo/waves/round-26/wave1/MutDeletionControls.md`
