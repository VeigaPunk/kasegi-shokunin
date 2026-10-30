# R48Probe26 — Unicode lookalike in box 2 label

## Scope and axes
Axes: canonical-form defect detection (grammar sensitivity to homoglyphs), reproducibility/stability of the finding, isolation of the mutation to one box. Author-side form only — no promotion, no semantic-truth judgment, no target testing. Read: `/home/vgpnk/.omp/agent/RULES.md` and the frozen validator `corpus/instruments/shonen-form.py`. Source-read limit (declared): I read only lines 1–300 of the 544-line frozen protocol snapshot `.ufo/waves/round-48/controls/protocol-source.txt`, and I did NOT read the round-47 verifier routes R1/R2; the probe does not depend on either beyond the frozen validator's own grammar.

## Frozen-state provenance (read-only checks)
- Frozen claim commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` is an ancestor of lane HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031`.
- `claims.json` blob at that commit = `f52264e7ca651cc99b064bb72b407c767c35d4c7` = `git hash-object` of the working-tree file; file sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` matches `freeze.txt` `claims-sha256` (`frozen-at: 2026-10-30T14:30:48.968093Z`).

```sh
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin cat-file -t 3546f7089c224ac6c8adc68208b1e648bbf3e6a5
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree 3546f7089c224ac6c8adc68208b1e648bbf3e6a5 -- .ufo/waves/round-48/claims.json
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin merge-base --is-ancestor 3546f7089c224ac6c8adc68208b1e648bbf3e6a5 HEAD && echo ancestor=ok
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin hash-object /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/claims.json
sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/claims.json
```

Observed: `commit`; `100644 blob f52264e7ca651cc99b064bb72b407c767c35d4c7`; `ancestor=ok`; `f52264e7ca651cc99b064bb72b407c767c35d4c7`; `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`.

## Mutant and expected detector
Setup copied canonical `SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, 761 bytes) byte-for-byte into two scratch files, then applied exactly one substitution to the mutant copy: in the box 2 label (line 7), byte 306, the ASCII `a` of `task` (U+0061) was replaced by U+0430 CYRILLIC SMALL LETTER A — a visual lookalike:

```
- [ ] At least one end-to-end domain tаsk executed and logged in LOG.md
```

Boxes 1, 3, 4, the preamble, and every evidence line remained byte-identical (verified, see receipts). The frozen grammar in `grade()` matches each box with `re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label), line)` — byte-exact label matching — so any codepoint substitution inside a label must fail the box-2 match. Expected: mutant exit 1 with a stable box finding (`SF-BOX`); unmodified positive exit 0 `SF-CLEAN`; restored/pristine bytes exit 0 `SF-CLEAN`.

Is the transformation semantically permitted? No. The canonical form is byte-exact by construction (`re.escape` over four fixed labels); a homoglyph is a different codepoint and therefore noncanonical, not an alternate spelling the grammar tolerates. The predicate's rejection is a genuine kill, not a fabricated defect.

## Full detector commands and observed output
Exact command used for every detector run (the trailing `echo` captures the detector's own exit status):

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file <SCRATCH_FILE>; echo "exit=$?"
```

Unmodified positive (`--file /fast/scratch/hyaku/kasegi-r48/R48Probe26/positive-SHONEN.md`), run 1:
```text
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

Mutant (`--file /fast/scratch/hyaku/kasegi-r48/R48Probe26/mutant-SHONEN.md`), run 1:
```text
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

Mutant, run 2 without any byte change (stability):
```text
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

Expected vs observed: positive clean = expected `SF-CLEAN`/0, observed same; mutant nonclean stable finding = expected `SF-BOX`/1, observed same on both runs. No discrepancy; no counter/predicate bytes were altered.

## Hash and restoration receipts
Setup command:
```sh
mkdir -p /fast/scratch/hyaku/kasegi-r48/R48Probe26 && cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe26/positive-SHONEN.md && cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe26/mutant-SHONEN.md && sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe26/positive-SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe26/mutant-SHONEN.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py && wc -c /fast/scratch/hyaku/kasegi-r48/R48Probe26/positive-SHONEN.md
```
Output: both scratch copies and canonical at `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`; validator at `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`; positive copy 761 bytes.

Mutant isolation verification:
```sh
cmp positive-SHONEN.md mutant-SHONEN.md; wc -c positive-SHONEN.md mutant-SHONEN.md; sha256sum mutant-SHONEN.md
# plus a read-only codepoint diff of the two files' lines
```
Output:
```text
/fast/scratch/hyaku/kasegi-r48/R48Probe26/positive-SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe26/mutant-SHONEN.md differ: char 306, line 7
 761 positive-SHONEN.md
 762 mutant-SHONEN.md
d5953c000162a20fb555061cdb5372ca62ae72306493cd74067a4b5573420432  mutant-SHONEN.md
differing_line_indexes(0-based)= [6]
label_char_diffs(pos_cp,mut_cp)= [(38, '0x61', '0x430')]
nonascii_in_mut_label= ['0x430']
other_lines_identical= True
```
Exactly one line (line 7, box 2) differs, by exactly one codepoint (U+0061 → U+0430, +1 byte); the only non-ASCII character in the mutated label is the injected U+0430.

Post-run receipt (after all detector runs):
```sh
sha256sum $R/SHONEN.md $R/corpus/instruments/shonen-form.py $S/positive-SHONEN.md $S/mutant-SHONEN.md
```
Output:
```text
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /fast/scratch/hyaku/kasegi-r48/R48Probe26/positive-SHONEN.md
d5953c000162a20fb555061cdb5372ca62ae72306493cd74067a4b5573420432  /fast/scratch/hyaku/kasegi-r48/R48Probe26/mutant-SHONEN.md
```

Restoration evidence: the validator is read-only by design and never writes; production `SHONEN.md` and `shonen-form.py` hashes are identical before and after every run (above), so there was nothing to restore outside the disposable scratch. The tasking declares the scratch removable on exit after receipts are saved; the mutant bytes are fully reconstructible from the canonical hash plus the single-codepoint substitution documented here. Scratch directory `/fast/scratch/hyaku/kasegi-r48/R48Probe26/` was removed after this report was written.

## Verdict
**Killed.** The unmodified positive passes (`SF-CLEAN`, exit 0), the box-2 homoglyph mutant fails deterministically and stably (`SF-BOX`, exit 1, identical across two runs), and the mutation is provably isolated to one codepoint on line 7. Expected and observed agree on every run. No frozen-claim defeat: the frozen grammar's byte-exact `re.fullmatch` over `re.escape`d labels legitimately classifies the lookalike as noncanonical, and this probe reports no way to pass a label homoglyph through it. No production, fleet, sibling, or domain-tree edits; no git/jj mutation; no tool installs (none required); no builds or blanket verification beyond the authorized bounded probe; no delegation or background jobs.

Operational note: the first setup attempt failed before executing anything because the process cwd was pointed at the not-yet-created scratch directory (`Working directory does not exist`); retried with absolute paths from an existing cwd and succeeded.
