# R48Probe16 — Box 1 label Unicode-lookalike grammar probe (kasegi round 48, wave 1)

- Seat: `R48Probe16`, mutation-tester, leaf member (no subagent dispatch). Date: 2026-10-30.
- Scope: one bounded probe on a scratch copy of canonical `SHONEN.md`, box 1 label only; author-side form only, never promotion or semantic truth. No production edits, no commit/push, no target testing, no tool installs (none needed).
- Report path: `.ufo/waves/round-48/wave1/R48Probe16.md` (relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, as written here).
- Read `/home/vgpnk/.omp/agent/RULES.md` first: tooling directive noted; no installs performed, no pacman transactions initiated.

## Frozen references

- Freeze commit cited by tasking: `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` — confirmed a commit in the lane repo: `git cat-file -t` → `commit`; `git log --oneline -1` → `3546f70 round-48: freeze canonical checklist restoration and controls` (read-only invocations).
- `.ufo/waves/round-48/freeze.txt`: `frozen-at: 2026-10-30T14:30:48.968093Z`, `claims-sha256: b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` — matches observed `sha256sum` of `.ufo/waves/round-48/claims.json` (`b8022cdf…`). (The tasking id is the freeze commit, not a file hash; `git hash-object` of the current `claims.json` is `f52264e7ca651cc99b064bb72b407c767c35d4c7`.)
- Counter bytes (frozen): `corpus/instruments/shonen-form.py`, sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`. Docstring: "Validate the canonical four-box checklist, never promotion or semantic truth. 0 clean; 1 noncanonical; 2 unreadable input. Read-only; no network."
- Canonical target: `SHONEN.md`, sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`.
- Interpreter: Python 3.14.8 (main, Oct  2 2026) [GCC 16.2.1 20260810], host `python3`.

## Mutant

Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Probe16/` (explicitly created; copies made with `cp -p` from the canonical file).

- `pristine.md` sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` (byte-identical to canonical).
- `mutant.md`: one substitution in the box 1 label (line 5, the only differing line): `U+0061 LATIN SMALL LETTER A` → `U+0430 CYRILLIC SMALL LETTER A` (the only `a` in `contains`). Visually identical; different bytes (line 88 B → 89 B). Mark `[~]`, box 1's Evidence line, and all other boxes byte-identical.
- Mutant sha256 `f54330649746041c3100ad8a89bb55a6491a20e45b5de5ae375d41ad54b5f2c8` — unchanged before and after all detector runs (counter is read-only, confirmed).

Mutation driver (saved as scratch fixture `mutate_box1.py`, source reproduced here verbatim):

```python
#!/usr/bin/env python3
"""R48Probe16 fixture driver.

Substitute ONE Unicode lookalike in the box 1 label of a scratch copy of the
canonical SHONEN.md; every other byte, including the other three boxes and
box 1's own Evidence line, stays identical to pristine.
"""
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
LATIN_LINE = '- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources'
# Latin small letter a (U+0061) -> Cyrillic small letter a (U+0430): visually identical.
MUTANT_LINE = '- [~] SKILL.md cont\u0430ins real decision tables, error patterns, checklists, cited sources'

pristine = (SCRATCH / 'pristine.md').read_bytes()
lines = pristine.decode('utf-8').splitlines(keepends=True)
hits = [i for i, l in enumerate(lines) if l.rstrip('\n') == LATIN_LINE]
assert len(hits) == 1, f'expected exactly one box-1 label line, found {hits}'
i = hits[0]
before = lines[i]
lines[i] = MUTANT_LINE + '\n'
(SCRATCH / 'mutant.md').write_bytes(''.join(lines).encode('utf-8'))

after_bytes = (SCRATCH / 'mutant.md').read_bytes()
print(f'mutated line: index {i} 0-based (line {i + 1} 1-based)')
print(f'before: {before!r}')
print(f'after : {lines[i]!r}')
print('substitution: U+0061 LATIN SMALL LETTER A -> U+0430 CYRILLIC SMALL LETTER A '
      "(the only 'a' in 'contains', box 1 label)")
print(f'line bytes: pristine {len(before.encode("utf-8"))} -> mutant {len(lines[i].encode("utf-8"))}')
pl = pristine.decode('utf-8').splitlines()
ml = after_bytes.decode('utf-8').splitlines()
diff = [j + 1 for j, (a, b) in enumerate(zip(pl, ml)) if a != b]
print(f'lines differing vs pristine (1-based): {diff}')
print(f'total lines pristine/mutant: {len(pl)}/{len(ml)}')
```

Driver output (command: `python3 /fast/scratch/hyaku/kasegi-r48/R48Probe16/mutate_box1.py`):

```
mutated line: index 4 0-based (line 5 1-based)
before: '- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources\n'
after : '- [~] SKILL.md contаins real decision tables, error patterns, checklists, cited sources\n'
substitution: U+0061 LATIN SMALL LETTER A -> U+0430 CYRILLIC SMALL LETTER A (the only 'a' in 'contains', box 1 label)
line bytes: pristine 88 -> mutant 89
lines differing vs pristine (1-based): [5]
total lines pristine/mutant: 12/12
```

## Detector runs (frozen counter, expected vs observed)

Positive control — unmodified copy, expected `canonical=1 finding=SF-CLEAN exit=0`:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py \
    --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --file /fast/scratch/hyaku/kasegi-r48/R48Probe16/pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

Observed = expected. The positive control passes, so the mutant verdict below is attributable to the mutation, not a broken baseline.

Mutant — expected `canonical=0` with a stable `SF-*` finding and exit 1:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py \
    --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --file /fast/scratch/hyaku/kasegi-r48/R48Probe16/mutant.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

Determinism re-run (identical invocation): `shonen-form canonical=0 finding=SF-BOX exit=1` — stable across two runs.

## Verdict

- **KILLED.** A single-codepoint homoglyph in the box 1 label defeats canonical form and the frozen counter catches it deterministically (`SF-BOX`, exit 1, twice). Baseline failure: none (positive control clean), so the result is conclusive, not inconclusive.
- Coverage observation (not a contract change): the predicate matches each label with `re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label), …)`, so any byte drift in any label collapses to the same coarse `SF-BOX` finding with no box index or codepoint detail. Sensitivity is total (byte-exact); diagnostic precision is per-class only.
- Semantically-permitted check (seat requirement): the substitution is **not** a permitted variant of the author-side form. The canonical template fixes the label bytes; `re.escape` matching admits exactly those bytes. The checklist's *meaning* is unchanged, but the counter's own docstring disclaims semantic truth — it validates the canonical form, so this is a genuine form defect (the classic paste-through homoglyph class), caught as designed. No defect fabrication was needed and none was made; the counter bytes were not touched.

## Restoration evidence

Production lane files unchanged (hashes identical before and after all runs):

| File | sha256 before | sha256 after |
|---|---|---|
| `SHONEN.md` | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` | same |
| `corpus/instruments/shonen-form.py` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | same |
| `.ufo/waves/round-48/claims.json` | `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` | same |

Scratch removal (receipts embedded above first, then removal per seat spec):

```
$ rm -rf /fast/scratch/hyaku/kasegi-r48/R48Probe16
$ ls -la /fast/scratch/hyaku/kasegi-r48/
total 4
drwxr-xr-x  6 vgpnk vgpnk   78 Oct 30 11:41 .
drwxr-xr-x 15 vgpnk vgpnk 4096 Oct 30 11:37 ..
drwxr-xr-x  2 vgpnk vgpnk   86 Oct 30 11:38 R48Probe11
drwxr-xr-x  2 vgpnk vgpnk   69 Oct 30 11:38 R48Probe14
drwxr-xr-x  2 vgpnk vgpnk    6 Oct 30 11:41 R48Probe15
drwxr-xr-x  2 vgpnk vgpnk   48 Oct 30 11:28 l1-novelty
probe16-scratch-exists=no
```

Only my own `R48Probe16` directory was removed; sibling scratch dirs were left untouched. No git/jj index or state was read mutatively or written; no files outside this report and the (now removed) scratch dir were created, modified, or deleted.

## Notes

- Round-47 verifier routes R1/R2 were not consulted: this probe's oracle is fully defined by the seat spec plus the frozen counter; no verifier-route input was needed.
- No build/lint blanket verification was run; only the assigned bounded probe executed.
