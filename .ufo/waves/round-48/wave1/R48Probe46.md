# R48Probe46 — bounded canonical-form probe (box 4 Unicode lookalike)

Seat: R48Probe46 (leaf member, no subagent dispatch). Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Scratch: /fast/scratch/hyaku/kasegi-r48/R48Probe46/ (removed on exit after this report saved). No production file, fleet file, sibling, claim, git/jj state, or PATH entry was touched. No install was performed.

Read before work: /home/vgpnk/.omp/agent/RULES.md; round-47 verifier spot-check (`corpus/lessons/round-47-verifier-spotcheck.md`, routes R1/R2 as relevant); frozen snapshot `.ufo/waves/round-48/controls/protocol-source.txt` (read to line 300 of 544).

## Frozen inputs (observed)

- Canonical `SHONEN.md` sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, 761 bytes. Before and after the probe the lane-root file still hashes to the same value (verified in the final batch).
- Frozen detector `corpus/instruments/shonen-form.py` sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`, Python 3.14.8 (already installed; no install performed).
- Detector grammar (read from source): each of four LABELS must match the box line by `re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label))`; an exact byte-level label match is required before the evidence line is read. Any mismatch returns `SF-BOX` immediately.
- `claims.json` at `.ufo/waves/round-48/claims.json` (1782 bytes): grep for `Probe` returns 0 matches and no `R48Probe*` seat row exists. The seat is therefore not a row in the frozen claim file; this is recorded as an observation, not repaired.

## Transformation

Scratch copy `SHONEN.md` (byte-identical to canonical, sha256 b1352168…). Only box 4's label was changed: the `o` in `No cross-domain bleed` was replaced by U+043E CYRILLIC SMALL LETTER O (UTF-8 `d0 be`). Byte delta +1 (761 → 762). Other boxes and evidence lines unchanged.

Diff (exact, `diff -u` of pristine copy vs mutant):

```
--- /fast/scratch/hyaku/kasegi-r48/R48Probe46/SHONEN.pristine.md
+++ /fast/scratch/hyaku/kasegi-r48/R48Probe46/SHONEN.md
@@ -8,5 +8,5 @@
       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
 - [~] Instructions executable by an agent without oral context
       Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
-- [~] No cross-domain bleed (PROVINCE.md still accurate)
+- [~] Nо cross-domain bleed (PROVINCE.md still accurate)
       Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
DIFFEXIT=1
```

Mutant sha256 `899a6ae58172f3bcf71dfab138932f7c35ec3ac655c4d19c7773e6a6b9b3a2ee`. Pristine copy sha256 `b1352168…` (kept at `SHONEN.pristine.md` in scratch).

## Commands and observed output

1. Positive control (unmodified pristine copy):

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe46/SHONEN.md   # pristine copy at this point
→ shonen-form canonical=1 finding=SF-CLEAN exit=0
→ EXIT=0
```

Expected: SF-CLEAN, exit 0. Observed: SF-CLEAN, exit 0. Match.

2. Mutant, first run:

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe46/SHONEN.md
→ shonen-form canonical=0 finding=SF-BOX exit=1
→ EXIT=1
```

3. Mutant, second run (stability):

```
(same command)
→ shonen-form canonical=0 finding=SF-BOX exit=1
→ EXIT=1
```

Expected for the probe: nonclean and a stable SF finding, exit 1. Observed: `SF-BOX`, exit 1, identical on both runs. Match.

Note: the `Ran in a temporary shell ...` trailer on some tool outputs is a shell-session artifact; it does not alter the detector output lines above.

## Semantic-permission check

The transformation is not semantically permitted by the frozen grammar. The detector compares labels by exact code-point regex and does not normalize. U+043E is visually identical to Latin `o`, but it is a different code point, so the label is not the canonical label. `SF-BOX` is the correct finding under the frozen form. This is a true form defect in the mutant, and the detector catches it; no detector defect is claimed. The probe shows the frozen checker is confusable-sensitive for label text (it does not reject visually identical lookalikes in *evidence* text, which was not probed here).

## Verdict per probe

- Positive control: PASS (expected SF-CLEAN/0, observed SF-CLEAN/0).
- Box-4 lookalike mutant: DETECTED (expected nonclean SF finding/1, observed SF-BOX/1, stable across two runs).
- Mutant-to-canonical byte integrity: canonical sha unchanged (b1352168…) at the end of the probe.

## Observations (not repaired; frozen bytes untouched)

- The current canonical `SHONEN.md` (761 bytes, 4 boxes, single seed shape) does not show the per-round assessment-block drift described in round-47 route R1 in the bytes read here.
- `claims.json` contains no `R48Probe46` (or any `Probe`) seat row; seat identity could not be cross-checked against the frozen claim file.

## Restoration / cleanup

- Canonical `SHONEN.md` hash re-verified after the probe: b1352168… (no change).
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe46/` (SHONEN.md mutant, SHONEN.pristine.md) removed after this report was written; receipts above are the record.
- No commit, push, mutating git/jj, background job, delegation, install, or PATH change.
