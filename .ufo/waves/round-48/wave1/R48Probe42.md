# R48Probe42 — bounded grammar probe (C1 shonen-form, box 4 duplication)

Seat: R48Probe42 (leaf member, no subagent dispatch, no background jobs, no production edits).
Claim: C1 `depth:verifiability` routed-defect-closure, frozen at `.ufo/waves/round-48/claims.json`.
Frozen checker: `corpus/instruments/shonen-form.py` (read-only, not modified).

## Axes named

1. Form conformance of `SHONEN.md` to the canonical four-box grammar (C1 predicate). Form only, not promotion or semantic truth.
2. Detector stability: same bytes give same finding across repeated runs.
3. Restoration fidelity: pristine bytes restored exactly after the mutation.

## Freeze verification

- `claims.json` sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matching `freeze.txt` `claims-sha256`.
- Base `SHONEN.md` at `903d47e13058982460f0d90c1c2b9c7c02680646` (read-only `git show`) sha256 `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05`, matching the kill-rule archive SHA.

## Scratch and inputs

- Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Probe42/` (created explicitly, removed on exit after receipts were saved here).
- Pristine: `.ufo/waves/round-48/controls/canonical-candidate.txt`, sha256 `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c`, copied to scratch as `SHONEN.md`.
- Mutation (single, box 4 only): appended a second copy of box 4 (its mark line and its evidence line) after the canonical four-box block. Boxes 1–3 untouched. Mutant sha256 `72cca46c4c9d8bf7ab1d8e9f864acac5be8be2ea5f6dfc19ecafd5e92c9191f3`.
- Diff, pristine to mutant (`diff -U0`):

```
@@ -12,0 +13,2 @@
+- [~] No cross-domain bleed (PROVINCE.md still accurate)
+      Evidence: LOG.md — Author assessment only; no promotion claimed.
```

## Commands and observed output

Positive control (unmodified canonical bytes), expected `SF-CLEAN exit=0`:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe42/SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
```

Mutant (duplicated box 4), expected nonclean with a stable SF finding, observed:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe42/SHONEN-mutant-dupbox4.md
shonen-form canonical=0 finding=SF-TRAILING exit=1
```

Stability, three further reruns of the same mutant bytes, observed:

```
shonen-form canonical=0 finding=SF-TRAILING exit=1
shonen-form canonical=0 finding=SF-TRAILING exit=1
shonen-form canonical=0 finding=SF-TRAILING exit=1
```

Restoration: scratch `SHONEN.md` rewritten from the pristine canonical bytes; sha256 back to `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c`. Re-run observed `shonen-form canonical=1 finding=SF-CLEAN exit=0`.

Production (read-only observation, no edit): the frozen checker against the production file `SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, default root) observed `shonen-form canonical=1 finding=SF-CLEAN exit=0`. The production file is not byte-identical to the canonical candidate control (`b476c7aa…`): its box 2 is `[ ]` and its evidence lines differ. Both pass the frozen checker.

## Verdict

- Mutant (box 4 duplicated): **killed by the frozen checker**. Expected nonclean, observed `SF-TRAILING exit=1`, stable across four runs.
- Positive control: **expected clean, observed clean** (`SF-CLEAN exit=0`) both on canonical candidate bytes and after restoration.
- Restoration: exact pristine bytes restored and re-verified.
- No defeat of the frozen counter found. No checker, predicate, or claim bytes were modified. No defect is claimed.

## Semantic note

Duplicating box 4 is not a semantically permitted transformation under the canonical four-box grammar: the grammar fixes exactly four labelled boxes in order, so a fifth box is nonconforming form. The nonclean finding is therefore the correct outcome, not a fabricated defect. This probe says nothing about whether the duplicated text would be true or promotable.

## Limits

- This seat ran one distinct mutation (box 4 duplication), with the positive control and restoration. It did not run the 64-probe milestone; that count belongs to the wave, not to this seat.
- The probe checks form only: evidence pointer existence, not semantic truth; no `x` marks were tested.
- No tool was installed or updated. No pacman transaction. No git/jj mutation (only read-only `git show`).

## Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe42/` removed on exit after receipts were recorded above.
