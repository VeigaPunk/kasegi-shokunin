# R44Review3 — C1 routed defect 3

## Finding

**Count confirmed; correction remains unresolved in the visible tree.** Frozen defect 3 is the wrong “29-character prefix” claim at `corpus/lessons/round-43.md:90` and `:101`, requiring an append-only correction and a counting command (spot-check §6 at `corpus/lessons/round-43-verifier-spotcheck.md:103`). The prefix is 26 characters: `printf '%s' c6ae07c6a541e0e96d0040afb6 | wc -c` → `26`. The full hash is 40 characters: `printf '%s' c6ae07c6a541e0e96d0040afb62b45dd37711300 | wc -c` → `40`. Counting command must omit the line feed; `printf '%s\n' ... | wc -c` instead returns 27 and 41. The exact 26-character token also appears in the captured curl quote at `corpus/lessons/round-43.md:90`; full 40-character hash is stated in the frozen spot-check at `round-43-verifier-spotcheck.md:103`.

I find no append-only correction in the current lesson. Its disputed wording remains at both cited lines, so defect 3 is still unresolved; C1's “all eight fixed” predicate is not established. The frozen do-nothing control at `.ufo/waves/round-44/controls/do-nothing.txt:4-7` records eight defects unresolved at the frozen base. Current observation of the unchanged lesson plus no correction evidence means this item still discriminates do-nothing from a landed correction; I do not claim the whole C1 is falsified beyond this one outstanding item.

## Verification and limits

Read-only inspection and literal count only. Exact count outputs: prefix with newline `27`, full hash with newline `41`, prefix without newline `26`; the corresponding full hash without newline is `40`. Lane HEAD observed as `66314015122b9aa32dc40f2f1815df56624c26d1`. No tools installed (RULES.md read first; Pacman not invoked). `HYAKU_SCRATCH` was unset; no scratch was created. No source edits. Report path relative to lane root: `.ufo/waves/round-44/wave1/R44Review3.md`.
