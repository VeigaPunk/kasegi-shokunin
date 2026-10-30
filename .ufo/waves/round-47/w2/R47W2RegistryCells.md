# R47W2RegistryCells — integrated immutable-cell review

Axes: **depth:verifiability; coverage**.

Reviewed committed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193` is context, not the comparison baseline. Working HEAD differed, so results below use explicit committed Git objects, not working files.

## Findings by severity

**No actionable immutable-registry-cell defect found in this bounded scope.** All original S001–S074 IDs occur exactly once in both committed registries, each with 11 cells (`corpus/SOURCES.md:5-80`). Compared all **814 original cells**, including cell whitespace without normalization. **813 protected cells are unchanged**; the sole difference is the authorized S074 used-by cell at `corpus/SOURCES.md:80`:

- Base: `corpus/knowledge/github-repository-security-advisories.md`
- Integrated: `corpus/lessons/round-46.md`

S001–S073 whole row strings are also identical, not merely equivalent after cell trimming. S074's other ten cells are identical, including status **mined**, recheck **90d**, and its historical source/scope/anchor/teaches values. No unauthorized mutation was observed. The permitted transition is accurately logged at `corpus/SOURCES.md:176` and `corpus/lessons/round-47.md:67`.

## Residual risk and claim boundaries

- **C1 remains not fully met**, not repaired by rerolling its frozen target. The integrated lesson explicitly retains S074 mined rather than performing the harmful frozen mined→rejected transition (`corpus/lessons/round-47.md:59,69`). This report establishes the retained status directly from committed cells; B3 failure execution belongs to the historical W1 evidence, not this seat.
- **C2 remains unmet**: F02 enrichment is not a new F30 coverage admission (`corpus/lessons/round-47.md:60,65`; `corpus/SOURCES.md:175`). Registry preservation does not establish coverage progress or saturation.
- Historical S074's anchor still calls capture chrome prose by design; its historical nature and the superseding correction are explicitly disclosed (`corpus/SOURCES.md:177`). This authorized preservation is not a reason to rewrite immutable cells.
- S075/S076 are new rows, outside the original-cell comparison. Their semantic admission, capture reproducibility, and broader runtime/resume contracts are outside this seat's bounded item. No global acceptance recommendation follows from this local result.

## Evidence and execution limits

Executed **static data analysis only**: read-only `git diff BASE REV -- corpus/SOURCES.md`, explicit `git show COMMIT:path`, and in-memory Python comparison/hash calculation. No product runtime, counters, mutants, selftests, source fetches, domain-target actions, Git mutations, or service restarts were run. No scratch/export was necessary; none remains. No tools were installed or updated.

`xd://lsp` is unavailable (device returned “No such tool”); no language-server status/references/definition/diagnostics could run. Literal committed Markdown row comparison is the fallback here, not semantic caller proof.

Receipt: `.ufo/waves/round-47/w2/R47W2RegistryCells.receipt.json` records both source-file SHA-256 digests, every original row's line and hash, exact changed-cell bytes, uniqueness, and the empty unauthorized-change list. The committed round-47 lesson decisions were read directly; W1 `R47SrRegistry.md` and `R47SentNoHarm.md` were read as historical context only, not alternative instructions or acceptance rules.

Self-evaluation: accuracy 4/5 (exact committed comparison; no runtime proof); completeness 5/5 for all 74 original rows and the sole allowed cell; clarity 4/5 (historical versus executed evidence separated); actionability 4/5 (per-row receipt available; broader claims intentionally unassessed); conciseness 4/5 (claim-boundary caveats retained). Overall 4.2/5. Improvement: broader admission/runtime assurance requires the assigned owners, not widening this leaf review. Would the user agree: the requested immutable-cell item is fully covered without claiming C1/C2 success.

Report: .ufo/waves/round-47/w2/R47W2RegistryCells.md
