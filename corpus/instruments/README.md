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

## `resolve.py` explicit-mirror citation alias (round-17 continuation)

`resolve.py` derives its mirror root — `$KASEGI_MIRROR` wins, else the first
existing of `MIRROR_CANDIDATES` (`~/Projects/the-bounty-hunter`,
`~/Projects/origin-work/the-bounty-hunter`), else the canonical absent path
(`_derive_mirror`). The round-17 change makes citations written with an
explicit canonical mirror prefix honor that derived root, as relative and
bounty-relative citations already did in `classify`:

- **Exact-prefix, slash-delimited matching.** The alias applies only to the
  two `MIRROR_CANDIDATES` prefixes in tilde form (`~/…`) or expanded-`$HOME`
  absolute form (`/home/vgpnk/…`) — the root itself or a descendant below a
  `/`. Prefix-sibling paths (`~/Projects/the-bounty-hunter-extra/x.md`) are
  not mirror cites and keep the plain absolute-path check.
- **Selected root, no stale fallback.** When `$KASEGI_MIRROR` is set, the
  suffix after the matched prefix resolves only under the selected
  `mirror_root`; the canonical written path is never consulted as a source
  of stale bytes. A missing suffix classifies `GONE` truthfully.
- **Unchanged schema, actual path.** A hit stays `RESOLVES`, domain `other`,
  and the census reports the actual resolved path under `mirror_root`; a
  miss is `GONE`. Bounty, relative and other-root classification is
  untouched; the four classes remain `RESOLVES` / `MIRROR-EQUIVALENT` /
  `INTERNAL` / `GONE`.
- **Realpath confinement.** Newly mapped explicit hits must stay under the
  realpath of `mirror_root`: `../` segments or symlinks below that root
  cannot credit unrelated files. The selected root itself may be a symlink.

Pre-fix baseline (resolver SHA-256
`97012403e89a94d2478249de4fa198f873520328df14e4432b1040c564e03294`),
reproduced by L1 with `KASEGI_MIRROR` pointing at a populated relocated
root: explicit `~/Projects/the-bounty-hunter/ops/rank.mjs:1` and expanded
`$HOME/Projects/the-bounty-hunter/.omp/config.yml:1` both classified `GONE`
(0/2) while relative `ops/rank.mjs:1` was `MIRROR-EQUIVALENT`. The
regression fixture proves relocation, precedence and confinement from the
consumer side (subprocess of the real CLI, temporary dirs, isolated
`HOME`/`KASEGI_MIRROR`, census writes stay inside the fixture, exit code =
verdict): `python3 corpus/instruments/test_resolve.py`. To replay the
pre-fix bytes instead, set `KASEGI_RESOLVER_UNDER_TEST=<path>` to an
alternate resolver copy; the default is same-directory `resolve.py`.

**What the alias does NOT mean.** It adds no ORIGIN-WORK override:
`~/Projects/origin-work/open-bug-bounties/` keeps the ordinary literal
other-root check, and `anchorcheck.py` retains its separate ORIGIN-WORK
base rules. No receipt or provenance authentication is added.
No sources were restored: both roots remain absent on this host
(`corpus/knowledge/root-loss-2026-10-12.md`), and a fixture `RESOLVES` is
proof of the mapping, not of a recovered bounty tree. Fixture numbers are
not census numbers: keep synthetic TSVs inside their temporary fixtures;
never publish them as `citation-survival.*`. The live resolvability score
moves only on measurements of the actual lane corpus and domain roots.


## Round-23 instruments

- `mirror-containment-check.py` + `mirror-containment-fixtures.json` — replays the
  frozen C1 matrix (24 cases: 12 escape, 12 control) on real copied `resolve.py`
  bytes, one isolated `HOME`/`KASEGI_MIRROR`/lane tree per case; asserts the CLI's
  `class`, `resolved_path`, `method` and `domain`; writes a JSON receipt with
  resolver, matrix and checker digests. `--resolver PATH` replays alternate bytes
  (the do-nothing control). Fixture names are confined to the case root.
- `source-recheck.py` + `corpus/source-snapshots/round-23/manifest.json` — checks
  pinned captures against declared SHA-256 and exact quotes, applying a declared
  normalization (`normalized=markup-whitespace`); exits 0 only when every assertion
  holds, 1 on a mismatch, 2 when a base is missing.

## Round-24 instruments

- `resolve-dispatch-check.py` + `resolve-dispatch-fixtures.json` — the C1 counter-B
  matrix: 8 cases (4 liveness, 4 control) replayed on real copied `resolve.py`
  bytes in isolated case trees, asserting `class` **and** `resolved_path`
  (existence plus containment to the root that class implies). `--resolver PATH`
  scores alternate bytes; `--json` writes a receipt with resolver, matrix, checker
  and runner digests. Measured discrimination: fixed bytes 8/8, round-23 bytes
  4/8, always-GONE resolver 1/8, always-INTERNAL 0/8.
  **Known limit (R11):** no case has more than four brace alternatives, so a
  mutant that lowers `brace_expand`'s 64-combination bound to 8 scores 8/8 here and
  24/24 on the round-23 matrix while flipping real verdicts. Reported, not hidden.
- `capture-source.py` — fetches one public document, converts it to UTF-8 text
  (HTML tags stripped and entities decoded; PDF text via `pdftotext -enc UTF-8`;
  plain text as served), collapses per-line whitespace, writes the snapshot and
  prints its sha256 plus fetch byte count and UTC stamp. `--selftest` proves the
  conversion is deterministic. **Known limit:** it is a network-capable producer;
  the scheme allowlist lives in `allow_url()`, redirects stay on http(s), but it
  cannot certify that a host will serve the same bytes again.
- `frontier-recheck-count.py` — the C1 counter-A harness: reads the Frontier table
  in `corpus/README.md`, and for each admitted entry binds the entry to its own
  `recheck:` line before running it (header `source:` ids must be covered by the
  `--source` selections, the selections must be cited in the entry, the named
  manifest must list them, and the line must be a `source-recheck.py` invocation
  with `--source`). Prints one line per entry and `entries=K pass=P exit=0|1`.
- `corpus/source-snapshots/round-24/manifest.json` — 19 captured records, 62
  assertions: S001–S015 (the five round-22 Frontier entries) and S032–S035 (the
  round-24 F09 admissions). Every assertion was measured exactly-once in its own
  capture; the checker now prints `occurrences=N` and verifies a declared `anchor`
  line for non-unique quotes (QUALITY Q9).
- `source-recheck.py` (round-24 changes) — rejects a quote shorter than 12
  normalized characters (`reason=quote-too-short-to-be-evidence`), prints the
  occurrence count on every pass, and verifies an optional `anchor` line number.
- `resolve.py` (round-24 changes) — brace alternatives: an empty alternative in a
  real alternative set is a literal expansion (`{,sub}`), a bare `{}` stays a
  placeholder; a surviving alternative that carries a `<...>` placeholder is
  globbed (`brace-glob`); the glob branch credits the first match that exists, not
  `matches[0]`. The CLI now refuses a non-directory root and refuses to overwrite
  the census when it collects no citations.
