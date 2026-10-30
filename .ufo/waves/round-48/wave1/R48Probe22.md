# R48Probe22 — Bounded grammar probe: box-2 duplication

- Seat: R48Probe22 (leaf member, lane `kasegi-shokunin`, round 48 wave 1; no subagent dispatch)
- Axis: depth:verifiability
- Frozen claim probed: C1 (`claims.json`), predicate = "SHONEN.md conforms to the canonical
  four-box author-assessment grammar" — form validation only, not promotion or evidence truth.
- Frozen claim provenance: `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` resolves as a git commit
  (`git cat-file -t` → `commit`). On-disk `.ufo/waves/round-48/claims.json` sha256 =
  `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matching the
  `claims-sha256` line in `.ufo/waves/round-48/freeze.txt`.
- Lane HEAD at probe time: `3d7e042ecbb1f17662f5042e8d3da3290722c031`.
- Frozen counter: `corpus/instruments/shonen-form.py`, sha256
  `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (read and executed, not modified).
- Round-47 route context: R1 (SHONEN.md canonical-form drift) is the repair route this probe
  exercises the counter against; R2 was not used.
- No production edits. No git/jj mutation. No tool installs. No target testing. No pacman activity.

## Probe design

Transformation: on a scratch copy of canonical `SHONEN.md`, box 2 only, duplicate the box's
two lines (checklist line `- [ ] At least one end-to-end domain task executed and logged in
LOG.md` plus its `      Evidence: LOG.md — ...` line) immediately after the original. Boxes 1, 3
and 4 unchanged.

Semantic permission check: the transformation is **not** semantically permitted under the
canonical grammar. The frozen checker requires exactly four boxes in a fixed label order
(`LABELS` tuple, `shonen-form.py`); a duplicated box makes box 3's expected label
("Instructions executable…") meet the second copy of box 2's label, which is a box-sequence
violation. No defect is fabricated: the nonclean finding is the checker's designed response.

Scratch fixtures (all under `/fast/scratch/hyaku/kasegi-r48/R48Probe22/`):

```
SHA256 b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.pristine.md (identical to production SHONEN.md)
SHA256 cac8fe5852d1f745d2eeeb244276666819eb3da4ac9b0ba4110472b77f863f3a  SHONEN.mutant.md (box-2 duplicated)
```

Diff (exact, from the scratch pair):

```
$ diff SHONEN.pristine.md SHONEN.mutant.md
8a9,10
> - [ ] At least one end-to-end domain task executed and logged in LOG.md
>       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
DIFF_EXIT=1
```

## Observed results

Commands (exactly as executed; `--root` is the lane root, `--file` is the scratch fixture):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe22/SHONEN.pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
POSITIVE_EXIT=0

$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe22/SHONEN.mutant.md
shonen-form canonical=0 finding=SF-BOX exit=1
MUTANT_EXIT=1
```

Stability: the mutant was run three times across the session (two runs before a restore/re-apply
cycle, one after the diff capture); each printed `shonen-form canonical=0 finding=SF-BOX exit=1`.
The pristine positive was run twice; each printed `shonen-form canonical=1 finding=SF-CLEAN exit=0`.

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Unmodified positive (pristine copy) | canonical=1 SF-CLEAN exit=0 | canonical=1 SF-CLEAN exit=0 | yes |
| Mutant (box 2 duplicated) | nonclean, stable SF finding | canonical=0 SF-BOX exit=1, stable across runs | yes |

Mechanism of the observed finding: the checker consumes box 1 correctly, consumes box 2's first
copy and its evidence line, then reads the duplicated `- [ ] At least one…` line where box 3's
frozen label is required; `re.fullmatch` fails → `SF-BOX`, exit 1.

## Hygiene

- Production `SHONEN.md` sha256 unchanged: `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`.
- Frozen counter `corpus/instruments/shonen-form.py` sha256 unchanged: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`.
- Scratch mutant restored to pristine bytes before scratch removal; scratch dir removed after this
  report was written.
- No repair was produced: the seat spec is a bounded probe with no production edits, and the
  counter predicate is frozen. The duplicated-box mutant is reported as a killed mutant, not as a
  checker defect.
- Tooling: none installed. Python from the host (`/usr/bin/python3`) was used; nothing installed or upgraded.
