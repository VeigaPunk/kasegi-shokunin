# Provenance — `.ufo/waves/round-34/wave1-results.json` (fixture payload)

Committed test fixture for the C1 closure check D4: the round-34 results file is tracked and carries
a provenance note beside it. The live pair is `.ufo/waves/round-34/wave1-results.json` +
`.ufo/waves/round-34/wave1-results.json.provenance.md` at the lane root; this fixture copy only has
to exist beside its results file. Tracking is counted with
`git ls-files .ufo/waves/round-34/wave1-results.json | wc -l` -> 1, measured in the scratch repo the
fixture loader builds (`corpus/instruments/r35-fixtures/README.md` § D4).
