# kasegi depth instruments (committed round 15)

Three stdlib-only, deterministic scripts. They are the measurement base for the
`depth` axis in `SCORECARD.md`; before round 15 they lived only in `/tmp/kasegi-r1*`
and would have been lost to a tmp sweep. All three are read-only over the lane
repo and every domain surface.

| script | what it measures | run |
|---|---|---|
| `density.py` | per-block evidence density of a markdown file: `ev = path-cites + concrete-table-rows + unique-numerics + unique-ALL-CAPS-signatures`, `dens = ev*100/nb` (nb = non-blank lines). Blocks segment at `^#{2,3}`. Full exclusion rules in its docstring. | `python3 corpus/instruments/density.py SKILL.md --label X` → stdout table + mean |
| `resolve.py` | **live citation-resolvability**: every distinct backticked path-like citation in `SKILL.md` + `corpus/**/*.md`, excluding its generated `citation-survival.md`; preserves leading-dot paths and classifies `RESOLVES` / `MIRROR-EQUIVALENT` / `INTERNAL` / `GONE`; numerator = the first three. | `python3 corpus/instruments/resolve.py <lane-repo-root>` → writes `citation-survival.md` + `citation-survival.tsv` **next to the script** |
| `anchorcheck.py` | anchor gate: each supported `path:NN[-MM]` citation is range-checked against the lane, frozen mirror, pinned Git blob, or declared ORIGIN-WORK root; prints the cited source lines. Round 18 added lane-prefixed paths (`corpus/`, `claims/`, `evidence/`, `.ufo/`, etc.), `csv`/`jsonl`/`rst`/`txt`/`py`/`ts`, and explicit mirror paths. ORIGIN-WORK checks current bytes only and do not establish tracking or a durable pin. | `python3 corpus/instruments/anchorcheck.py <file.md>` |

ORIGIN-WORK citations must use the explicit `~/Projects/origin-work/open-bug-bounties/` prefix; explicit mirror citations use `~/Projects/the-bounty-hunter/`. Both roots are realpath-confined (`OUTSIDE-BASE`) and read-only. Relative lane paths are checked lane-root-relative; bare names also search the four declared lane directories and then fixed mirror subdirectories. Round 18 changed leading/trailing cleanup from `strip` to `rstrip`: a leading dot is path data, so `.ufo/` and `.omp/` must never be silently rewritten before matching. Summary output keeps `ORIGIN` and `OUTSIDE-BASE` separate.

`citation-survival.md` / `.tsv` are the **current census of record**, regenerated
in round 18. The historical round-15 census and its double-run md5
`ab25833e897822af3e87b371a3d4eeff` remain recoverable from git history.

## Known limits (measured, not assumed)

- **`density.py` is form-sensitive.** Identical content measured 93.3 as
  ~76-col prose vs 150.0 as a single-line-row table (r15 labrat, same script);
  the lane's own r14 record is 86.0 vs 973.3. Hold rendering form constant
  across a before/after pair, and never reflow prose into a table to move the
  number.
- **`density.py` does not validate existence.** A fabricated `path:line` scores
  exactly like a real one, and duplicate citation instances each count. That is
  why `anchorcheck.py` exists and why round 15 runs both: density is a proxy for
  evidence, `anchorcheck` + `resolve` are the checks that the evidence points at
  something. Mutation testing (r15, `/tmp/kasegi-r15/mutation-report.md`) killed
  8 of 12 mutations and recorded 4 blind spots: fabricated cites rewarded,
  duplicate cites inflate, coordinated numeric edits can leave unique-`num`
  unchanged, and deleting prose raises density.
- **`resolve.py` counts name survival, not content survival.** A citation whose
  relative path exists in the mirror is `MIRROR-EQUIVALENT` even when the line
  number is past the mirror's EOF or the content differs (r15 found 2 such
  corpus cites: `[lost-tree] ops/claim-check.mjs:174-199` vs an 83-line file,
  `[lost-base] ops/shared.mjs:55` vs 41 lines). `anchorcheck.py` is the instrument that
  catches those; run it after any re-anchor.
- **`anchorcheck.py` checks only supported anchored token shapes.** `bad=0`
  means every recognized anchor is either in range or explicitly
  `LOST-RECORDED`; it does not make historical lost-tree content openable and
  does not validate unanchored template paths. Round 18 broadened the matcher,
  exposed 82 bad anchors in the pre-edit `SKILL.md` (versus 46 under the r17
  matcher), and then triaged all 82 rather than preserving the blind spot.
- **The rate is definition-sensitive.** Three independent r15 implementations
  agreed on direction and disagreed on absolutes: `resolve.py` (instrument of
  record, definition above) SKILL 222/486 = 45.68 %, lane 410/1437 = 28.53 %; a
  strict-live variant that
  refuses mirror equivalence and counts only citations resolving at their
  written path: 6.9 % distinct / 7.1 % instances; a third that excludes
  glob/pattern tokens first: 202/419 = 48.2 % concrete-shaped tokens existing
  on disk. Always publish the definition with the number.
- **Round-18 rate moved honestly, not monotonically.** Exact ORIGIN-WORK
  re-anchors raised the corrected SKILL numerator 228 → 232, while expanding
  ambiguous shorthand and previously invisible lost-tree anchors raised its
  denominator 488 → 503; therefore the fraction moved 46.72 % → 46.12 %.
  Lane total still improved 427/1461 = 29.23 % → 432/1469 = 29.41 %. The
  score stays 4. The auditability move is reported separately by
  `anchorcheck.py`: broadened-matcher bad anchors 82 → 0, ORIGIN 1 → 5, and
  explicit LOST-RECORDED 5 → 104.
  The corrected resolver excludes its own generated Markdown and preserves
  leading-dot paths; two consecutive final runs produced byte-identical stdout,
  Markdown, and TSV.

## Bar rule for repairs (round-15 amendment)

`BAR_R15 = 142.5` — **frozen declared constant**, equal to the pre-edit file
mean measured at the start of round 15 (`density.py` on `SKILL.md` before any
edit). It is NOT re-derived from the post-edit mean (self-inflating, circular)
and NOT re-derived each round from the current file mean (a compounding
survivorship ratchet: 96.5 pristine → 102.5 at r14 → 142.5 at r15 → ~167.5
projected for r16, which adds the most demand to exactly the blocks a previous
round left thin). Round 15's four repaired blocks did **not** clear it in
prose form (131.4 / 111.5 / 117.4 / 93.0) and the lane records that rather than
reformatting to pass.

From round 16 the density bar is **conjunctive** with a resolvability gate:
a repaired block counts as repaired only if `dens ≥ BAR` **and** ≥ 60 % of its
path citations resolve (`RESOLVES` + `MIRROR-EQUIVALENT` + `INTERNAL` +
blob-pinned), because density alone rewards citing files that no longer exist.
