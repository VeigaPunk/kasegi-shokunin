# r42-at-de09313-selftest.txt — export-ref annotation (appended round 44)

This sidecar annotates the committed receipt
`.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt`, which named no
`export-ref` (routed defect 5 of
`corpus/lessons/round-43-verifier-spotcheck.md` §6). The receipt bytes are not
edited — a receipt is evidence, and rewriting one would destroy it. The fact it
omitted is recorded here instead.

- receipt: `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt`
- export-ref=de09313e8edb98280b19767d0094bb2dd8031d73
- round: 42 (the receipt is the round-42 selftest replayed at the round-42 base)
- derivation: the paired run receipt
  `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt:2` carries
  `export-ref=de09313e8edb98280b19767d0094bb2dd8031d73` and the receipt's own
  name carries the same export; `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin
  rev-parse de09313e8edb98280b19767d0094bb2dd8031d73^{commit}` resolves it. The
  export is reproducible with
  `git archive de09313e8edb98280b19767d0094bb2dd8031d73 | tar -x -C "$EXPORT"`.
- replay receipt for the same export: `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt`
- round-44 cross-check: `.ufo/waves/round-44/controls/r42-at-de09313-selftest-replay.txt`
  and `.ufo/waves/round-44/controls/r42-at-de09313-selftest-runner.log` (the
  round-44 replay of the same export, with its runner log).

Correction (round 44; falsify wave): the first version of this sidecar carried
`export-ref=ab98fac9dce87130bc4f66de89e30650d63943dc`, which is the ROUND-43
base this round measured against — not the export the r42 receipt was produced
at. R44W2Rev09 caught the contradiction with the paired run receipt; the value
above is corrected to the run receipt's own `export-ref`, and
`corpus/instruments/r44-routed-defects.py` limb D5 now requires the sidecar's
export-ref to EQUAL the paired run receipt's export-ref, so this class of error
is graded rather than merely documented. The round-44 measurement receipt
`.ufo/waves/round-44/controls/missing-suite-base.txt` keeps `ab98fac9` — that
is the export the round-43 missing-suite replay was taken at, a different
measurement with a different export.

`corpus/instruments/r44-routed-defects.py` limb D5 grades the presence of this
sidecar, the equality of its `export-ref` with the paired run receipt's, and the
pinned digest of the sidecar bytes; the annotated receipt itself stays
byte-identical.
