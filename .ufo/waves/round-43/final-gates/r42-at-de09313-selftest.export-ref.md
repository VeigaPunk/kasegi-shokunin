# r42-at-de09313-selftest.txt — export-ref annotation (appended round 44)

This sidecar annotates the committed receipt
`.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt`, which named no
`export-ref` (routed defect 5 of
`corpus/lessons/round-43-verifier-spotcheck.md` §6). The receipt bytes are not
edited — a receipt is evidence, and rewriting one would destroy it. The fact it
omitted is recorded here instead.

- receipt: `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt`
- export-ref=ab98fac9dce87130bc4f66de89e30650d63943dc
- round: 42 (the receipt is the round-42 selftest replayed at the round-43 base)
- derivation: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse ab98fac9^{commit}`
  → `ab98fac9dce87130bc4f66de89e30650d63943dc`; the export is reproducible with
  `git archive ab98fac9 | tar -x -C "$EXPORT"`.
- replay receipt for the same export: `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt`
- round-44 cross-check: `.ufo/waves/round-44/controls/r42-at-de09313-selftest-replay.txt`
  and `.ufo/waves/round-44/controls/r42-at-de09313-selftest-runner.log` (the
  round-44 replay of the same export, with its runner log).

`corpus/instruments/r44-routed-defects.py` limb D5 grades the presence of this
sidecar and the `export-ref=` token it carries; the receipt itself stays
byte-identical.
