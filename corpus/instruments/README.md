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
  4/8, always-GONE resolver 1/8, always-RESOLVES 0/8 (the artefact's own label,
  `.ufo/waves/round-24/wave1/LivenessMatrix.md:200-201`; earlier lane files called
  it `always-INTERNAL`, corrected round 25).
  **Known limit (R11):** no case has more than four brace alternatives, so a
  mutant that lowers `brace_expand`'s 64-combination bound to 8 flips real verdicts
  without moving the pass count. Measured: on the **baseline** bytes
  (`690153ad…`) that mutant scores 4/8 with an identical receipt and 24/24 on the
  round-23 containment matrix (`ResolverAttack.md:151`); on the **landed** bytes
  (`db5e0767…`) the same mutant (`88122e10…`, round 25) scores **8/8 and 24/24**,
  which is the blind spot demonstrated rather than inferred — receipt
  `.ufo/waves/round-25/d24-3/receipt.txt`. Reported, not hidden.
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
  with `--source`). Rule G (round 42): a frontier census runs over **every**
  `| F<n> |` row before the records — a `FRONTIER-CENSUS rows=N admitted=N
  closed=N problem-rows=N registry=N|absent` line, then `FRONTIER-PASS <id>` /
  `FRONTIER-FAIL <id> status=<status> ids=<ids> problems=<...>` per row; the
  three row-failure problems are `status-not-admitted`, `missing-pass-line` and
  `source-id-absent:<id>` (an id bound by the row's README `sources` cell or its
  entries with no `corpus/SOURCES.md` row). Prints one line per entry and
  `entries=K pass=P exit=0|1` (the summary line stays last; `entries` counts
  the raw row set plus records, so a status flip can never shrink it).
- `corpus/source-snapshots/round-24/manifest.json` — 19 captured records, 76
  assertions: S001–S015 (the five round-22 Frontier entries) and S032–S035 (the
  round-24 F09 admissions). Every assertion was measured exactly-once in its own
  capture; the checker now prints `occurrences=N` and verifies a declared `anchor`
  line for non-unique quotes (QUALITY Q9). Count it from the lane root:
  `python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"`
  → `76`, and the round-24 receipt's 95 `OK` lines are 19 `:sha256` plus these 76.
- `source-recheck.py` (round-24 changes) — rejects a quote shorter than 12
  normalized characters (`reason=quote-too-short-to-be-evidence`), prints the
  occurrence count on every pass, and verifies an optional `anchor` line number.
- `resolve.py` (round-24 changes) — brace alternatives: an empty alternative in a
  real alternative set is a literal expansion (`{,sub}`), a bare `{}` stays a
  placeholder; a surviving alternative that carries a `<...>` placeholder is
  globbed (`brace-glob`); the glob branch credits the first match that exists, not
  `matches[0]`. The CLI now refuses a non-directory root and refuses to overwrite
  the census when it collects no citations.

## Round-28 amendment — `anchorcheck.py` fails closed (C1)

Appended at file end; no line above moved (R6). Instrument bytes: ExecImplC1
(diff `corpus/instruments/ExecImplC1.diff`, receipt
`.ufo/waves/round-28/receipts/ExecImplC1.txt`). Landed digest measured here:
`95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514` (523 lines,
2026-10-25T17:30Z); the figure of record is the round-28 receipt index, not a
digest retyped from another document. Figures labelled *before* are runs against
the pre-change digest
`c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748` (the
do-nothing control); figures labelled *after* are runs at the landed digest. The
re-verify block is at the end of this section.

**Exit is a verdict, not a print.** `FAIL_CLASSES` is the exit driver:
`MISSING-FILE`, `PAST-EOF`, `OUTSIDE-BASE`, `PIN-BROKEN`, `BASE-ABSENT`,
`BOUNTIES-ABSENT` — exit 1 when any count is nonzero, else 0. Exit 0 means every
recognized anchor is `IN-RANGE*` or `LOST-RECORDED`. `LOST-RECORDED` keeps its
round-16 meaning: recorded-not-fail — counted, never checked, never able to flip
the exit code. `bad` stays the historical three-class count (MISSING-FILE +
PAST-EOF + OUTSIDE-BASE) for receipt continuity, so PIN-BROKEN, BASE-ABSENT and
BOUNTIES-ABSENT move the exit without moving `bad`: read the exit status, not
only the summary. *Before*, no class moved the exit code at all — `main()` fell
off the end, so `sys.exit(None)` was 0 even with a fail verdict printed
(`.ufo/waves/round-28/c1-controls/bad-fixture-before.txt` shows both halves, the
`BASE-ABSENT` line and `exit=0`). *After*: the r27 bad fixture exits 1, and a
sweep of `corpus/knowledge/*.md` + `corpus/*.md` + `SKILL.md` (44 files,
2026-10-25T17:30Z) moves no verdict class in any file while flipping exactly 5
exits 0→1 — all BASE-ABSENT-driven: `QUALITY.md`, `citation-bases.md`,
`cra-manufacturer-reporting-duties.md`,
`iso-29147-divergence-and-clause-crosswalk.md`, `root-loss-2026-10-12.md`.

**This file is flagged by its own rule.** At the landed digest a run of the
instrument over this file exits 1: three BASE-ABSENT cites carried since
rounds 17/24 (the `ResolverAttack` and mirror `ops/rank.mjs` examples at lines
114, 116 and 164) point into the mirror base absent since 2026-10-12. They are
pre-existing documentation examples, not anchors added by this section (0
added), and they are left as measured rather than relabelled to make the file
pass.

**`BOUNTIES-ABSENT` — the lost PROVINCE root gets its own class.** `CITE` gains a
`~/Projects/bounties/` arm, so a citation into the PROVINCE root is classified
instead of being invisible to the matcher. The root is derived like MIRROR and
ORIGIN, never hardcoded: `$KASEGI_BOUNTIES` wins, else the canonical
`~/Projects/bounties` — a single candidate, because that root was removed on
2026-09-28 and never relocated (`test -d ~/Projects/bounties` → exit 1,
2026-10-25; loss record `corpus/knowledge/source-tree-loss-2026-09-28.md`). A
citation into the absent root reports `BOUNTIES-ABSENT`, its own class: not
`BASE-ABSENT` (the mirror/origin bases) and not `MISSING-FILE` (a lane file that
is not there). The arm carries the same realpath confinement as the MIRROR arm —
a `../` segment or symlink resolving outside the derived root is `OUTSIDE-BASE`
against that root, not a hit; when the root is present but the cited file is not,
the verdict is `MISSING-FILE` (still a fail class, never a silent pass). The
class appears exactly once for the r27 bounties fixture, because the frozen
counter is `grep -c BOUNTIES-ABSENT` — it counts lines, not occurrences, which is
why the summary's bucket list deliberately gains no `BOUNTIES-ABSENT=` field.
*Before*, `CITE` had no such alternative, so that fixture produced no cite
instance in any class (0 `BOUNTIES-ABSENT` lines, every bucket 0):
`.ufo/waves/round-28/c1-controls/bounties-fixture-before.txt`. *After*: one
`BOUNTIES-ABSENT md:3 … (base tree absent: …)` line naming the derived root,
`grep -c` = 1, exit 1, summary buckets unchanged.

**`--selftest` — the limbs prove themselves.** Spelling:
`python3 corpus/instruments/anchorcheck.py --selftest`, from the lane root, with
no file argument (the pre-change bytes opened the flag as a path and died
`FileNotFoundError: '--selftest'`, exit 1 — a crash, not a verdict:
`.ufo/waves/round-28/c1-controls/selftest-before.txt`). Each case runs this file
as a subprocess in a fresh temp dir with `KASEGI_LANE_ROOT`, `KASEGI_MIRROR`,
`KASEGI_ORIGIN_ROOT` and `KASEGI_BOUNTIES` overridden, and asserts the complete
verdict-class vector plus the exit status — so a fixture that trips a second
limb, or a limb with no failing fixture, is itself a failure. The landed set is
9 cases: six fail limbs, one per `FAIL_CLASSES` entry — `missing-file` (every
base present, cited file absent), `past-eof` (real temp file, anchor past EOF),
`outside-base` (a bounties cite that walks out of the root with a `..` segment
while the root is present), `pin-broken` (temp `git init` repo, pin object
`deadbeef`), `base-absent` (unprefixed mirror name, mirror root absent),
`bounties-absent` (bounties root absent) — each expecting exactly its own class
at exit 1; and three controls at exit 0: `bounties-in-range` (the arm resolves
in a present root, so the arm is not merely an outage), `lost-recorded` (one
backticked marked token plus one bare `source:` trailer, asserting
`LOST-RECORDED=1` not 2 — the token model asserted as code), `clean` (in-range
lane cite). Success prints `selftest cases=N failures=0` and exits 0; a failing
case prints its name plus that case's stdout/stderr and exits 1. Measured at
the landed digest: `selftest cases=9 failures=0`, exit 0. Quote N from a live
run, never retype it.

**Corpus disclosure — declared four, measured zero.** C1's frozen disclosure says
the bounties arm reclassifies 4 marked bounties citations as `LOST-RECORDED`:
`corpus/knowledge/claim-gates.md` (line 123), `intake-and-finalize.md` (109),
`mission-control.md` (169) and `source-tree-loss-2026-09-28.md` (353). Measured
at the landed digest — and earlier at the pre-change digest and on a scratch copy
carrying only the `CITE` arm
(`.ufo/waves/round-28/wave1/ExecInstrReadme/anchorcheck-scratch.py`, not the live
file) — **0 of the 4 reclassify**: the landed 44-file sweep
(`corpus/knowledge/*.md` + `corpus/*.md` + `SKILL.md`) moves no verdict class in
any file, the four named ones included. The cause is structural: those four
citations are plain-text `source:` header lines, not
backticked tokens, so `TOK` never hands them to `CITE`; and a scan of
`corpus/**/*.md` + `SKILL.md` + `LOG.md` + `SCORECARD.md` at 2026-10-25T17:24Z
(before this section existed) found 70 backticked `~/Projects/bounties/…` tokens
with **0** carrying a `:NN` anchor, so none can match `CITE` with or without the
arm. `SKILL.md` is unchanged by construction (0 marked bounties cites,
`LOST-RECORDED=306`, 7 in-range, bad 0). The disclosure is therefore recorded as
DECLARED and NOT REPRODUCED — at the landed digest `95333e29…` as at
`c2a9e6c6…`. If a later change reaches 4, it matches outside the documented
backticked-token shape, and that broadening belongs here with its own
before/after. The L1 has since superseded the frozen cell by an appended
correction (`.ufo/waves/round-28/claims-erratum-1.md`) whose statement is
stronger and matches this measurement: zero backticked anchored
`~/Projects/bounties/` citations exist in the lane tree, so the arm is invisible
to every existing byte and no verdict-class count moves. Raw measurement:
`.ufo/waves/round-28/wave1/ExecInstrReadme/disclosure-measurement.txt`.

**Re-verify** (from the lane root; run after any instrument edit — every target
below was measured at the landed digest `95333e29…`):

    sha256sum corpus/instruments/anchorcheck.py
    python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_fixture_exit=$?"
    python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
    python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$?"
    python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '
    for f in corpus/knowledge/*.md corpus/*.md SKILL.md; do python3 corpus/instruments/anchorcheck.py "$f" 2>/dev/null | grep '^== '; done

Targets: `bad_fixture_exit=1`; bounties fixture `1`; `selftest cases=9 failures=0`
with exit 0; and the SKILL.md no-harm line `0 bad`, `LOST-RECORDED=306`,
`PIN-BROKEN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`, 7 in-range instances — the same
numbers the pre-change bytes print
(`.ufo/waves/round-28/c1-controls/skill-before.txt`), so the arm and the exit rule
change no verdict class there. A drop of the `BOUNTIES-ABSENT` count to 0 means
the arm or its print path regressed; a sweep that moves a class means a matcher
widened, which must be documented here with its before/after.

## Round-31 additions — one-limb mutation ledger + score-gap reporter

Appended at file end; no line above moved (R6). Four new paths, all stdlib-only and
read-only over the lane: `corpus/instruments/limb-mutation-check.py` (counter),
`corpus/instruments/limb-ledger.json` (13 limbs + 3 controls as data),
`corpus/instruments/limb-fixtures/` (isolating fixture roots the SR/FR kill commands
need), and `corpus/instruments/score-gap.py` (read-only distance-to-score-5 reporter,
considerthese 2026-10-25 proposal 2). Every number below was measured by this scribe
seat at the digests in the re-verify block; figures from earlier digests of the same
files are labelled superseded, never mixed in.

| path | what it measures | run |
|---|---|---|
| `corpus/instruments/limb-mutation-check.py` | one-limb mutation discrimination of the three recheck-family instruments. Per ledger row: copy the lane's `corpus/` into a fresh `tempfile.mkdtemp` scratch lane, run the row's kill on the **unmutated** scratch copy, confirm the same `(exit, signal)` a second time (a nondeterministic baseline is `invalid:live-baseline`), require `find` to occur exactly once, require the patch to change bytes, `py_compile` the mutant, exec the mutant's module level in a subprocess (must exit 0 **and** print a sentinel, else `invalid:import`), then run the kill on the mutated bytes. `killed` iff the mutant's exit differs from `live_exit` or the signal no longer matches. | `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` → `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`, exit 0; `--selftest` → `selftest cases=20 failures=0`, exit 0 |
| `corpus/instruments/limb-ledger.json` | the frozen 13 rows in contract order (RA x9: parse, cwd, paths, cdroot, instrument, own, completeness, expect-missing, expect-unexpected; SR x2: stem-mismatch, occurrence-not-unique; FR x2: missing-entry, duplicate-entry) plus 3 controls (`CTL-noop` ⇒ `invalid:noop`, `CTL-nocompile` ⇒ `invalid:nocompile`, `CTL-equivalent` ⇒ `survivor`), each control bound to a real limb's instrument/kill/signal/`live_exit`. | read by the counter; `python3 -c 'import json;json.load(open("corpus/instruments/limb-ledger.json"))'` → `version=1 limbs=13 controls=3` |
| `corpus/instruments/limb-fixtures/` | isolating fixture roots for the SR/FR kill commands: `sr/stem-mismatch` (record `SFIX-STEM`, capture `SFIX-STEM-capture.txt`, correct sha256 pin, unique quote — so only B1 fails), `sr/occurrence-not-unique` (stem-correct `SFIX-REPEAT.txt` == id, quote twice, no anchor — the M30-1 closure), `fr/fr-missing-entry` (one admitted row naming an absent entry), `fr/fr-duplicate-entry` (two admitted rows, one entry realpath, both rows PASS their own A–D contract). 10 files, 40K. | via the ledger's kill commands; individually `python3 corpus/instruments/frontier-recheck-count.py --root corpus/instruments/limb-fixtures/fr/fr-missing-entry` or `python3 corpus/instruments/source-recheck.py --manifest corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json --source SFIX-REPEAT` |
| `corpus/instruments/score-gap.py` | distance to the next `depth:verifiability` score: (1) `recheck-audit.py --quiet` lines/executes/gated/broken + exit, (2) `anchorcheck.py SKILL.md` verdict buckets + exit, (3) the committed citation-survival lane/SKILL rates with that file's own definition sentence, (4) the `SCORECARD.md` line number and quoted score-5 threshold sentence, (5) one computed `gap:` line. Prints the sha256 of every input. **Not a claim; asserts no score move.** | `python3 corpus/instruments/score-gap.py [--root <lane>]` (any cwd) → exit 0; `--selftest` → `selftest fields=7 failures=0`, exit 0; exit 2 only when an input is missing/unreadable |

### The counter's measured output (landed bytes, quiescent)

`python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json`
from the lane root, 2026-10-26T00:05Z, exit 0, stdout sha256
`9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838` on two runs:

```text
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
```

Two rows are killed by signal alone, not by exit: `FR-missing-entry` (the mutant still
exits 1, through an uncaught `FileNotFoundError` traceback) and every RA row (mutant
exit 1 plus the isolating case line stops matching). `live=1` on the SR/FR rows is
correct, not a failing baseline: those three limbs protect a fail-closed exit 1, and the
counter's rule compares the mutant **against** `live_exit`.

### Known limits (measured, not assumed)

- **The counter cannot tell whether a `find` patches the line its `id` names.** The
  frozen row schema has no code-location field, so isolation lives in each row's `note`,
  in the fixtures above, and in the per-limb cross-run matrices the executors published
  (`ExecRALimbs.md` §4, `ExecSRLimbs.md` §5, `ExecFRLimbs.md` §C2). An attack seat's
  degenerate ledger of 13 equivalent patches prints the target summary lines and exits 0
  (`CritC1Kill.md` §3.1); the claim's closure clause — hand-re-derive a row and require
  the instrument's own report to move — is what rejects it. That closure remains open at
  the claim level (attack A7), not closed by the counter.
- **`--root` scores any tree and the frozen stdout grammar names neither root nor
  digests** (attack A11, open). The published figure is pinned only because the claim's
  command runs from the lane root.
- **The 13-id set is not asserted** (attack A12, open and moot here: the landed ledger
  carries exactly the frozen ids).
- **`killed` means "the run differs", not "the named limb decided it".** A mutant that
  guts a whole module body still imports and reads `killed` (attack A6); only the
  one-limb `find`/`replace` pairs and the isolating fixtures make the 13 verdicts
  limb-attributable.
- **`invalid:timeout` and `invalid:import` extend the frozen verdict enum**
  (`invalid:live-baseline|find-count|noop|nocompile`); both are implemented and
  selftested, and the enum extension is routed to the L1 rather than silently widened.
- **Rows are coupled to print formats through their `signal` regexes.** The RA signals
  key on `selftest <case>` lines; the FR signals encode the harness' column padding
  (`\s+`, `[ \t]*`). A reformat turns the row `invalid:live-baseline` — loud, exit
  non-zero — never a silent pass, but the row must then be re-derived.
- **Two `find` texts are multi-line for uniqueness.** `RA-completeness` needs the
  following `expect_ok` line (the bare production line also matches the selftest oracle),
  and `FR-missing-entry` needs `return None` (the bare `if not os.path.isfile(full):`
  occurs three times).
- **`score-gap.py` reads the committed r18 census of record**, not a live re-resolve:
  re-running `resolve.py` rewrites `citation-survival.md`/`.tsv`, which is a write. Its
  `gated` field is `recheck-audit.py`'s own definition (the line runs and fails closed on
  an absent base), and its threshold field depends on one English sentence in
  `SCORECARD.md` — a reword makes it exit 2 rather than print a stale line number.
- **Fixture ids are synthetic.** `SFIX-STEM` / `SFIX-REPEAT` sit outside the `S0xx`
  registry namespace and under `corpus/instruments/limb-fixtures/`, not
  `corpus/source-snapshots/`; the census reads only `corpus/SOURCES.md`. The tree is
  invisible to both instruments that walk the corpus: `recheck-audit.py` globs
  `corpus/knowledge/*.md` only, and the fr tree contains no backtick token, so
  `resolve.py`'s collection is identical with and without it (measured in
  `ExecFRLimbs.md` §F: 2201 distinct citations / 4311 occurrences / 85 citing files,
  delta 0). The RA limbs need no fixture tree — their kill is `--selftest`, which builds
  its own temporary trees.
- **Not claimed: the two FR mutants no current oracle kills** (dropping
  `no-source-selection`; dropping the `not-a-recheck-invocation` branch). They are
  outside the frozen 13, so they are not ledger rows; the isolating fixtures that would
  catch them are described in `MutFRExisting.md` and were not landed.

### R13 / R11 relation

R13 asks that each limb of a counter be shown load-bearing by a fixture that fails
**that** limb and no other, and that a discrimination figure be a measurement on the
landed bytes. The 13 rows answer the first half directly: every RA row's `signal` keys on
one `selftest` case line, and the SR/FR rows key on a fixture whose only failing limb is
the patched one. Where a limb had no failing oracle, the fixture was **added**, not
relabelled: `RA-completeness` was a proven survivor on the pre-round-31 bytes (mutant
compiled, `find` once, exit 0, stdout byte-identical), and the fix is the two `main()`-level
selftest cases `complete-empty` and `complete-missing-line`; `source-recheck.py` gained
the adjacent `quote-absent` case after `MutSRExisting.md` measured a survivor on
`reason=quote-not-found`. Both strengthenings are selftest cases, not new ledger rows, so
the frozen 13 stay 13. `frontier-recheck-count.py` needed no edit at round 34:
its two limbs were load-bearing on unchanged bytes once a fixture-backed kill
exists.

[r42 counter amendment, appended 2026-10-28, end-of-file append per R6] Round 42
hardened the same counter with rule G (the frontier census above): it now fails
the run when a `| F<n> |` row's status cell is not `admitted`, when an admitted
row owns no PASS record, or when an id the row binds has no registry row.
Re-measured: 566 lines, sha256 `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6`;
selftest 6 cases unchanged in number and wording; `FRONTIER-*` lines precede the
per-entry records (byte-identical record lines).

R11 is why the digest discipline below matters. The counter changed at least six times
during the wave (`9e729daf` → `eb9b87ff` → `b4223ed9` → `cde7c2b6` → `bd18c244` →
`c660a95f`); every figure in this section was measured by this seat at `c660a95f`, and
the merge receipt's earlier-digest figures are superseded, not averaged. The open limits
listed above (A7, A11, A12, A6) are the R11 statement that this counter's discrimination
is published, not assumed.

### Digests after the C1 edits

Measured by this seat with `sha256sum` on quiescent bytes (2026-10-26T00:05Z, before and
after the counter run, identical), from the lane root:

| path | before round 31 | landed |
|---|---|---|
| `corpus/instruments/recheck-audit.py` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` | `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` |
| `corpus/instruments/source-recheck.py` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6` (round 42, rule G frontier census) |
| `corpus/instruments/limb-mutation-check.py` | absent | `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` |
| `corpus/instruments/limb-ledger.json` | absent | `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` |
| `corpus/instruments/score-gap.py` | absent | `855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb` |

The three "before" digests are the base bytes of the round-31 claims' do-nothing control.
`recheck-audit.py` gained two `main()`-level selftest cases; `source-recheck.py` gained
`quote-absent`; `frontier-recheck-count.py` is byte-identical to base, so its digest
change set is empty by construction. These are working-tree digests — the round's
integration commit was not available to this seat, so no commit-pinned claim is made here.

The score-gap reporter's own field lines on the same bytes (its full block, including the
sha256 of each input, is in `ExecScoreGap.md` §6): `recheck: lines=44 executes=20 gated=24
broken=0 exit=0`, `anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0
base-absent=0 exit=0`, `threshold: SCORECARD.md:331`, and `gap: 24 of 44 rechecks still
gated on a lost base; score 5 needs 0 gated unsupported claims`. The reporter is not a
claim and moves no score.

### Re-verify (from the lane root; run after any edit to these files)

    sha256sum corpus/instruments/recheck-audit.py corpus/instruments/source-recheck.py corpus/instruments/frontier-recheck-count.py corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json corpus/instruments/score-gap.py
    python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
    python3 corpus/instruments/limb-mutation-check.py --selftest; echo "counter_selftest_exit=$?"
    python3 corpus/instruments/score-gap.py; echo "score_gap_exit=$?"
    python3 corpus/instruments/score-gap.py --selftest; echo "score_gap_selftest_exit=$?"

Targets: the six digests above; `limbs=13 killed=13 survivors=0` with
`controls=3 rejected=3` and exit 0 (stdout sha256
`9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`); `selftest cases=20
failures=0`; and the reporter's `gap:` line — which is *supposed* to move when a recheck
base returns, so re-read it rather than diffing it. A LIMB line that stops showing
`live` != `mutant` in exit or signal, or any `verdict=` other than `killed`, means the
subject instrument's print format or its fixtures moved: re-derive that row, do not edit
the summary.

### Round-31 close-out erratum — digests after the wave-2 repairs (appended by the L1)

The table above is the wave-1 state and is kept as history (R6/R9). Two instruments moved afterwards:
`limb-mutation-check.py` was repaired by `ExecCounterFix` (three implicit guard fixtures run on every
`--ledger` invocation; the printed output gained one `guard cases=3 failures=0` line, so the stdout
sha256 above changed) and `score-gap.py` was repaired by the L1 (census `cmd:` pattern, stub-fixture JSON,
`import json`, missing-field guard in the selftest). Current working-tree digests, measured 2026-10-26:

| path | landed (final) |
|---|---|
| `corpus/instruments/limb-mutation-check.py` | `237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4` |
| `corpus/instruments/score-gap.py` | `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf` |

`limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` stdout sha256 is now
`d6aefddca50293347c348646479bbe406745ad3163422b27edefcea861264270` (second run byte-identical), exit 0, with
the same two summary lines `limbs=13 killed=13 survivors=0` and `controls=3 rejected=3`. The other four digests
in the table are unchanged.

## Round-33 additions — `capture-binding-check.py` (C1 capture-manifest binding)

Appended at file end; no line above moved (R6). One new committed, stdlib-only instrument:
`corpus/instruments/capture-binding-check.py`. It answers a question the instruments
above never asked — a capture directory can hold real bytes and still be unauditable,
because nothing in its `manifest.json` says which documented URL those bytes came from
or when they were fetched. It audits that binding over every
`corpus/source-snapshots/*/manifest.json` and closes routed defect D5
(`corpus/lessons/round-32-verifier-spotcheck.md`: S049/S050 were committed with no
`round-32/manifest.json`, so an auditor could not tell where the bytes came from).

| script | what it measures | run |
|---|---|---|
| `corpus/instruments/capture-binding-check.py` | **Capture-manifest binding**, three rules. **A** manifest presence: every directory under `corpus/source-snapshots/` that holds a `manifest.json` *or* any captured file must hold one (`FAIL rule=missing-manifest dir=<dir>`). **B** URL binding, id-scoped per `claims-erratum-1`: the record id must name a registry row else `FAIL rule=no-row`; two rows with that id are `FAIL rule=dup-id`; the record `url` must byte-equal the `https://` token of *its own* row's source cell else `FAIL rule=url-mismatch` (an absent `url` is the `detail=absent` form). **C** provenance: a non-empty `fetched_utc` or `"archival": true`, with the archival exemption closed for `round-32`+ directories and for unparsable directory names (`FAIL rule=provenance-missing`). Prints one `AUDIT` header, one `MANIFEST <dirname> records=N url_bound=M fetched=K archival=L` line per manifest directory, one `FAIL` line per failure, and one summary `records=<total> bound=<total> unbound=<total>`; `bound` counts records satisfying B **and** C. Exit 0 only when every rule passes, 1 on any failure, 2 on a usage/read error (`UNAVAILABLE …`). | `python3 corpus/instruments/capture-binding-check.py [--root <lane>]` → 9 `MANIFEST` lines, the `AUDIT` line, `records=40 bound=40 unbound=0`, exit 0. `--selftest` → `selftest cases=11 failures=0`, exit 0. |

### Measured on the landed bytes (quiescent, this seat)

Instrument digest measured here with `sha256sum` on quiescent bytes, twice, identical
(2026-10-26T04:26Z): `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`,
492 lines — the digest the executor receipt's header carries, with its digest-history
line naming `bcabe76a…` → `4bc7aed3…` → **`b4182665…`**
(`.ufo/waves/round-33/wave1/ExecCaptureBinding.md`). Read the history, not only the
header: the executor's §3–§7 runs were executed at `4bc7aed3…` and only its selftest was
re-run at `b4182665…`, where the change is docstring prose — the fixture count said
`ten` while `CASES` holds eleven (`corpus/instruments/capture-binding-check.py:80`).
This section's live figures were measured at `b4182665…`.

Live run, twice, byte-identical stdout (sha256 of the 12-line body — nine `MANIFEST`
lines, the `AUDIT` line, the summary and the `binding_exit` line —
`5cac3ea71553ea102cbfcf83760a5a798750694bdc2979d02cea057cefb201d9`), against
registry `corpus/SOURCES.md` sha256
`fe89b17a2e059ef0d6e934157fef7c72508f1421e87a82a4aafefad40bc68c3c` (50 `S0xx` rows,
S049/S050 appended by ExecRegistryAppend). The registry moved again after that run —
`b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b`, still 50 rows,
2026-10-26T04:29Z — and a re-run at those bytes (twice, byte-identical) printed the
same twelve lines and the same body sha256, so the Search-log and R8 lines appended
after the two rows do not move this verdict:

```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
binding_exit=0
```

`--selftest` at the same digest prints all eleven case lines `verdict=pass` and
`selftest cases=11 failures=0`, exit 0; fixture trees are built in `tempfile.mkdtemp`
under `--scratch`, else `$HYAKU_SCRATCH`, and are removed at exit (measured: the
scratch root was empty afterwards). Exit 2 was measured, not assumed:
`UNAVAILABLE reason=no-snapshot-tree <root>` for a root without
`corpus/source-snapshots/`, and `UNAVAILABLE reason=read-error … No such file or
directory: '…/corpus/SOURCES.md'` for a present snapshot tree with no registry —
both `exit=2`.

### Manifest-schema additions (the rule B/C data)

Every manifest record gained the fields the checker reads; the round-23 through
round-31 manifests keep `schema_version: 1`, `purpose` and their `quotes` arrays
byte-identical and only gain these keys:

| field | value | records |
|---|---|---|
| `url` | the registry row's `https://` token, byte-exact (`S018` → `https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1`) | 40 |
| `archival` + `archival_note` | `true`, note `pre-round-32 capture; fetch instant not recorded` (one distinct value across all 38) | 38 (rounds 23–31) |
| `fetched_utc` | `2026-10-25T23:14:00-03:00`, the capture commit `288ea9ac17a78dce644388af35b89aa96b7994da` author instant | 2 (round-32 S049/S050) |

The round-32 records carry no `archival` key at all — rule C's exemption is closed
there, so they must stay on `fetched_utc`. The 40 records are 9 snapshot directories
(4 + 19 + 5 + 1 + 2 + 3 + 3 + 1 + 2) and every one has a manifest
(`missing_manifest=0`), which is the D5 shape closed.

Manifest digests at the same quiescent state, for re-verification:

| manifest | sha256 |
|---|---|
| `round-23` | `1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70` |
| `round-24` | `77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3` |
| `round-25` | `251cb5b2c1bacb5ba47758fb60e41aaf1e367ae11df05ed19886361b35f7aea2` |
| `round-26` | `1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247` |
| `round-28` | `89f51e052eaefcb56a880d48e6778ee88b46e55cafde1275c69992304e7ef75e` |
| `round-29` | `b24a485ff3d2d03abe3ef2022e211c7092bcf7509f3913cfa44145216e2c8d15` |
| `round-30` | `8aacf77cf2f3d9c7912eea419a05e10604959b2faacb4ae3b0e097f8ab81f94b` |
| `round-31` | `5fa37fd7249d043af1e36f98a549ee4ac8d6181e29f5def78116d3c637cb50e8` |
| `round-32` | `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774` |

### Known limits (measured, not assumed)

- **Rule B binds by id, so the binding is only as good as the manifest's `id` field**
  (`corpus/instruments/capture-binding-check.py:67-68`). A record whose id names a row
  while its bytes came from another document passes rule B; only `source-recheck.py`
  (sha256 + quote pins) or a human reader catches that. `bound=40` means "40 records
  name their own row and carry provenance", not "40 captures are the right documents".
- **Duplicate URL values across different ids are not a failure.** Per
  `claims-erratum-1` §4 the record binds to its own row, and a URL that also sits in
  another row or in prose is reported as `multi_row_url=2` — measured on the two
  erratum-declared records, S029 (`round-23`) and S006 (`round-24`), whose URLs also
  appear in rows S024 and S028. A global "the URL appears in exactly one row" reading
  would have made `unbound=0` unattainable without editing immutable registry rows (R8).
  The registry's pre-existing W04 duplicate-URL warnings stay census facts outside this
  instrument.
- **A row that carries two URL tokens binds when the record's url is one of them**
  (`:71-73`). Measured: all 50 rows carry exactly one `https://` token today, so the
  lenient branch is untested by the live tree and is proven only by the contract text.
- **The registry is read as column 2 of every `| S0xx |` row, whatever its status**
  (`:74-75`) — a `rejected` or `queued` row's URL binds a record exactly like a `mined`
  row's. `bound=40` is not a statement about row status.
- **`fetched_utc` is the capture commit instant for the round-32 records, not a
  measured HTTP instant** (`.ufo/waves/round-33/wave1/ExecManifest32.md` §8: "it records
  when the captures were committed, not a measured HTTP instant"). No independent
  fetch log exists for that round; drift is bounded only from the 2026-10-26T04:16Z
  live re-fetch onward (`ScoutLiveDrift`), which is not a substitute for the pin.
- **Exit 2 is a separate verdict from a rule failure.** An absent root, absent
  `SOURCES.md`, unparsable manifest JSON or malformed manifest shape prints
  `UNAVAILABLE …` and exits 2; a missing manifest, unbound URL or missing provenance
  exits 1. Neither is exit 0, so a wrapper that only greps the summary line can still
  be fooled by a stale stdout — read the exit status.
- **The instrument writes nothing** (`:77-78`), and only `--selftest` creates a scratch
  directory. Measured: `git status --porcelain corpus/instruments corpus/source-snapshots
  corpus/SOURCES.md` is identical before and after the runs in this section.

### Re-verify (from the lane root; run after any edit to this instrument or to a manifest)

```
sha256sum corpus/instruments/capture-binding-check.py
python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"
python3 corpus/instruments/capture-binding-check.py --selftest; echo "selftest_exit=$?"
for f in corpus/source-snapshots/*/manifest.json; do python3 -c "import json,sys; d=json.load(open(sys.argv[1])); s=d.get('sources',[]); print(sys.argv[1], 'records=', len(s), 'url=', sum('url' in x for x in s), 'fetched=', sum('fetched_utc' in x for x in s), 'archival=', sum('archival' in x for x in s))" "$f"; done
```

Targets: digest `b4182665…`; `records=40 bound=40 unbound=0` with `binding_exit=0`;
`selftest cases=11 failures=0` with `selftest_exit=0`; and the per-manifest field
counts `url=` equal to `records=`, `archival=` 38 over the eight legacy manifests,
`fetched=` 2 on `round-32`. A summary that leaves `records=40` means a manifest was
added, moved or lost — re-measure, do not adjust the target. A drop of `url_bound`
below `records` on the legacy manifests means a row's URL text moved in
`corpus/SOURCES.md`; that is a registry defect, not a capture defect.

## Round-34 hardening — `capture-binding-check.py` rules A3–A5, B3–B4, C1, D (C1 R5/R6/R8)

Appended at file end; no line above moved (R6 convention). Instrument digest before
`b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` (492 lines) →
after `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (892 lines),
measured with `sha256sum` on the landed bytes. The round-33 section above is left
untouched, so its targets are now **superseded**: the digest, `selftest cases=11`, the
AUDIT line drawn without `orphans=`/`orphan=` tokens, and the two "known limits" that
read a two-token cell leniently and a `rejected` row as binding like a `mined` row.
Its historical numbers stay true of the round-33 bytes; do not re-measure them against
this file.

### What the four rules now say (failure names are the contract)

| rule | addition this round | a defect prints |
|---|---|---|
| A | **Per-file binding.** Every capture file directly inside a manifest directory must be named by some `sources[].path`, or declared in the manifest's top-level `orphans` list as `{"path": "<file name in that directory>", "reason": "<non-empty>"}`. An undeclared capture fails; a declared one still prints `orphan=<file>` on the AUDIT line and leaves the exit status at 0 — the listing is the record that the file is known and unbound. A declaration whose file is absent is a stale listing. | `FAIL rule=orphan-capture file=<f> dir=<d>`, `FAIL rule=orphan-declared-missing file=<f> dir=<d>` |
| A | **Nested snapshot directories.** The walk descends regardless of whether the parent is a snapshot directory; a nested directory is audited on its own and named by its path below `corpus/source-snapshots/`. A parent's per-file check reads only its own direct files. | `FAIL rule=missing-manifest dir=round-31/inner` |
| B | **Two-token rows fail.** A source cell carrying two or more `https://` tokens cannot say which document the row names, so the row fails and every record pointing at it is ambiguous. This replaces the round-33 lenient branch (`a row that carries two URL tokens binds when the record's url is one of them`), which was untested on the live tree precisely because all rows carry one token. | `FAIL rule=double-https-row row=<id> n=<n>`, `FAIL rule=url-ambiguous record=<id> row=<id> tokens=<n>` |
| B | **A `rejected` row cannot anchor a record.** Status is column 8 of the row (index 7 after the empty-first-cell split). This replaces the round-33 limit (`whatever its status … a rejected or queued row's URL binds a record exactly like a mined row's`); a capture claiming a refused source is now a failure, and `queued` still binds. | `FAIL rule=rejected-row-anchor record=<id> row=<id>` |
| C | **Strict UTC.** `fetched_utc` must be an ISO-8601 timestamp with a `Z` or `+00:00` suffix and real calendar fields. Placeholders, local or non-zero offsets and malformed values each fail with their own `detail`; an absent value keeps the round-33 `provenance-missing` line. A present-but-invalid value fails in every round, legacy rounds included — the field is an assertion whether or not the round requires it. | `FAIL rule=fetched-utc record=<id> dir=<d> detail=pending\|local-offset\|malformed` |
| D | **Manifest integrity.** Two records in one manifest carrying the same `id`, or naming the same capture `path`, fail: the record count otherwise overstates the captures documented. | `FAIL rule=dup-record field=id\|path value=<v> count=<n> dir=<d>` |

Orphans, duplicate records and rejected anchors never move `records=`/`bound=`/`unbound=`:
`records - bound = unbound` stays the printed invariant and the exit status stays the
verdict, so a summary-only grep is still not a reading.

### Selftest is now a report, not a summary (the F-5 shape)

`--selftest` runs one fixture tree per case plus two report-verifier cases and prints
exactly one `selftest case=<name> exit=<n> want=<n> verdict=<pass|fail>` line per case,
then `selftest cases=23 failures=0`. The report checker (`judge_selftest_report`) rejects
a report with no case lines (`summary-only-report`), a case line whose `exit` ≠ `want`, a
duplicated or missing case line, and a summary whose `cases`/`failures` disagree with the
lines — the round-33 F-5 shape, where a mutant that skipped every fixture printed
`selftest cases=N failures=0` and passed. `summary-only-selftest-rejected` feeds that
forged report to the checker and requires rejection; `complete-selftest-report-accepted`
feeds a well-formed one and requires acceptance, so the limb is proven discriminating
rather than always-reject.

Named cases (23): `clean-all-pass`, `missing-manifest-dir`, `record-without-url`,
`shared-url-between-two-records`, `duplicate-id-rows`, `url-mismatch`, `no-row`,
`shared-url-not-a-failure`, `round-32-record-without-fetched_utc`,
`pre-round-32-record-without-archival`, `round-32-record-with-fetched_utc-passes`,
`pre-round-32-archival-passes`, `fetched-utc-pending-rejected`,
`fetched-utc-local-offset-rejected`, `per-file-orphan-detected`,
`per-file-orphan-listed`, `nested-snapshot-dir`, `nested-snapshot-missing-manifest`,
`dup-record-in-manifest`, `double-https-row`, `rejected-row-anchor`,
`summary-only-selftest-rejected`, `complete-selftest-report-accepted`.

`url-matching-two-rows` is retired (R5): its fixture built a duplicate-id registry, not a
shared-URL one. The renamed `shared-url-between-two-records` builds two records sharing
one URL across distinct rows and asserts `multi_row_url=2` at exit 0; `duplicate-id-rows`
keeps the `rule=dup-id` coverage under a name that matches its fixture.

### Old bytes pass, new bytes reject — the discrimination matrix

Nine fixture shapes, run against the round-33 bytes and the landed bytes from the same
roots (each built once in a scratch tree, `--root` on each copy). `exit` is the
instrument's own verdict:

| fixture shape | round-33 bytes | landed bytes |
|---|---|---|
| `fetched_utc: "pending"` (round-32) | exit 0, `records=1 bound=1 unbound=0` | exit 1, `detail=pending` |
| `fetched_utc: "2026-10-25T23:14:00-03:00"` | exit 0, bound 1 | exit 1, `detail=local-offset` |
| undeclared capture file beside a full manifest | exit 0, bound 1 | exit 1, `rule=orphan-capture file=S009.txt dir=round-30` |
| declared orphan (same file, `orphans` list) | exit 0 (key ignored) | exit 0, `orphans=1 orphan=S009.txt` |
| nested dir with its own manifest | exit 0, `records=1` (inner unread) | exit 0, `records=2 snapshot_dirs=2` |
| nested dir with captures, no manifest | exit 0 | exit 1, `dir=round-31/inner` |
| duplicate `id` and duplicate `path` in one manifest | exit 0, `records=3 bound=3` | exit 1, two `rule=dup-record` lines |
| two-`https://` registry row | exit 0, bound 1 | exit 1, `double-https-row n=2` + `url-ambiguous` |
| record anchored to a `rejected` row | exit 0, bound 1 | exit 1, `rejected-row-anchor` |
| clean two-record control | exit 0, bound 2 | exit 0, bound 2 (unchanged) |

Also measured: a malformed `orphans` declaration (bare string element) is exit 2
`UNAVAILABLE reason=manifest-shape … orphans` on the landed bytes and exit 0 on the
round-33 bytes, because the key was invisible to them.

### Live tree at landing time (and the one open sibling)

```text
MANIFEST round-34 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S051 dir=round-34
records=41 bound=40 unbound=1
binding_exit=1
```

`orphans=1 orphan=S040-live.txt` is round-26's declaration
(`corpus/source-snapshots/round-26/manifest.json` sha256
`33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa`): the file is named
and unbound, no `orphan-capture` failure, `records=` untouched. The single FAIL line is
a **C2 sibling in flight**, not a capture defect — round-34 landed its `sources` record
for S051 before the registry row, so rule B1 has no row to bind to yet. Once
`corpus/SOURCES.md` carries `| S051 |`, the same bytes print
`records=41 bound=41 unbound=0`, `binding_exit=0`. Read the pair, not the literal 40 in
the round-33 section above: the invariant is `bound=records`, and the record total moves
whenever a round adds a capture.

Re-verify targets after this section: digest `3d9e5e0…`; `selftest cases=23 failures=0`
with `selftest_exit=0`; `grep -c 'detail=local-offset'` = 0; `orphans=1
orphan=S040-live.txt` with 0 `rule=orphan-capture` lines; `missing_manifest=0` over ten
snapshot directories. A run that prints `records=41 bound=40` is reading the in-flight
C2 tree; a run that prints fewer than 23 case lines is not the landed selftest.

### Addendum — the C2 row landed inside the same wave; live gate is green

The in-flight state quoted above closed while this wave was still running:
`corpus/SOURCES.md` gained `| S051 |` (registry rows 50 → 51), so rule B1 now has a row to
bind. Measured on the same instrument bytes `3d9e5e0…`:

```text
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
binding_exit=0
```

`bound=records` at `binding_exit=0`, with `orphans=1 orphan=S040-live.txt` still the only
orphan token and no `FAIL` line of any class. The ten `MANIFEST` lines are unchanged from
the block above except `round-34 url_bound=0 → 1`. Re-verify targets are therefore:
digest `3d9e5e0…`; `selftest cases=23 failures=0`; `records=41 bound=41 unbound=0` at
`binding_exit=0`; `grep -c 'detail=local-offset'` = 0; `orphans=1 orphan=S040-live.txt`
with zero `rule=orphan-capture` lines.

## Round-34 amendment — `frontier-recheck-count.py` rule A is bidirectional (C1, R9)

Appended at file end; no line above moved (R6). Round-34 seat ExecFrontierBidirectional.
Instrument bytes: `sha256 aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`
(228 lines, lane base `014ee2d7`) → `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249`
(433 lines, worktree). Receipt `.ufo/waves/round-34/wave1/ExecFrontierBidirectional.md`.

**The gap (R9, round-33 `MutEntryF16.md:179`).** Rule A ran one direction:
`header-sources-not-rechecked` fired on `declared ⊄ recheck_ids` (a declared id the
line does not re-verify), and the mirror — `recheck_ids ⊄ declared`, a `--source` the
entry never declares — had no check. The only filter on that side was
`selection-not-cited-by-entry`, and `cited` was *every* `S\d{3,}` in the whole file,
including the recheck line's own `--source` ids, so it was satisfied by construction:
vacuous. Measured on the base bytes: dropping `source: S050` from
`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` leaves
`PASS F16 … exit=0`, `entries=19 pass=19 exit=0` — the survivor, reproduced.

**The repair, two parts.**

1. **Rule A runs both ways** against the entry's *declared source set*:
   `header-sources-not-rechecked` (declared ⊄ recheck) and the new
   `selection-not-declared-by-entry` (recheck ⊄ declared). Different problem names,
   so a receipt names the limb that fired.
2. **`cited` no longer counts declaration lines.** It is now built from every line
   except a `source:` line and the `recheck:` line, so
   `selection-not-cited-by-entry` fires when a selection is mentioned nowhere else in
   the entry. Evidence-list items (`- S002, …`) still count — they are citations.

**What "declared" means, and why it is not header-only.** The corpus uses two
declaration shapes: one header `source:` line per source (F09, F10, F13, F14) and one
per-source evidence item, `- S002, "Assessment": "…"` (the round-24 F01–F05 entries,
whose single header line declares the primary source and whose evidence list declares
the rest, e.g. `corpus/knowledge/cvss-v4-severity-and-vector.md:2` S001 header plus
`:26-29` S002 items). The declared set is their union. Measured: a header-only rule
fails five admitted rows (F01 S002; F02 S004/S005; F03 S007/S008; F04 S010–S012;
F05 S014/S015) — `entries=19 pass=14 exit=1` — because those entries' rechecks
legitimately cover their evidence lists. The union rule keeps the tree green at
`entries=20 pass=20 exit=0`, F17 included (measured after F17 landed; `entries=19
pass=19 exit=0` on the tree before it).

**Residue, stated rather than hidden.** For the five evidence-list entries a header
`source:` line can still be dropped without rule A firing, because the id stays
declared by its evidence items; those entries lose only the header's URL/section
provenance, not the entry↔source binding. Closing that residue means giving F01–F05
one header line per declared source (the F09/F10/F13/F14 shape) and then requiring
header-only membership; that is an entry-content change, not an instrument change, and
is the L1's call. It is **not** closed by this amendment.

**Selftest (new).** `--selftest [--scratch DIR]` runs six fixture lanes and prints
`selftest case=<name> exit=N want=N verdict=<pass|fail>` plus
`selftest cases=6 failures=0`, exit 0. Each fixture carries a stub
`corpus/instruments/source-recheck.py` and a schema-1 manifest, so a case failure can
only come from the harness's own binding. Cases: `bidirectional-holds` (pass path),
`selection-not-declared` (reverse limb; extra `--source` mentioned in prose only),
`header-source-not-rechecked` (forward limb), `evidence-list-declares-selection`
(second declaration shape passes), `evidence-declared-not-rechecked` (forward limb
over the evidence shape), `selection-neither-declared-nor-mentioned` (both problems,
in that order).

**Measured demos (scratch copies of the lane; lane untouched).**

| # | mutation | base `aa60b581…` | landed (rule code == `1be79af6…`) |
|---|---|---|---|
| 1 | F16 `source: S050` header line deleted | `PASS F16 ids=S049 exit=0`, `entries=19 pass=19 exit=0` | `FAIL F16 ids=S049 exit=- problems=selection-not-declared-by-entry`, `entries=19 pass=18 exit=1` |
| 2 | F16 recheck `--source S050` clause deleted | `FAIL … problems=header-sources-not-rechecked`, exit 1 | identical (forward limb unchanged) |
| 3 | reverse check deleted from the instrument | — | `selection-not-declared` fixture flips `FAIL`→`PASS` (`entries=1 pass=1 exit=0`) |
| 4 | forward check deleted from the instrument | — | `header-source-not-rechecked` fixture flips `FAIL`→`PASS` |
| 5 | no-op patch | — | `noop_changes_bytes=False` |

`limb-ledger.json` rows `FR-missing-entry` / `FR-duplicate-entry` still apply: each
`find` occurs exactly once in the landed bytes, and the two fixture roots print
`problems=missing-entry` / `DUPLICATE-ENTRY F98,F97 … entries=2 pass=2 exit=1`.

**Pin note.** `SKILL.md:1069` cites `aa60b581…` inside a sentence dated "Measured at
append time (working tree, 2026-10-25)" — a dated measurement, not a live target. This
section is the current pin for the worktree bytes; the integration commit belongs to
the L1.

**Re-verify (from the lane root):**

```
sha256sum corpus/instruments/frontier-recheck-count.py
python3 corpus/instruments/frontier-recheck-count.py --selftest; echo "selftest_exit=$?"
python3 corpus/instruments/frontier-recheck-count.py; echo "exit=$?"
```

Targets: digest `1be79af6…`; `selftest cases=6 failures=0` with `selftest_exit=0`;
`entries=20 pass=20 exit=0` once F17 has landed (`entries=19 pass=19 exit=0` on the
tree this seat measured). A drop in `pass` means an entry's recheck line and its
declared set drifted apart — read the `problems=` token before editing either side.

## Round-34 additions — `kill-rule-check.py` (C1 survivor-mutant counter)

`corpus/instruments/kill-rule-check.py`. Round 33 measured its C1 mutant set under a
kill rule that accepted a `--selftest` span with no per-case evidence (a forged
`selftest cases=0 failures=0` exited 0 and was recorded as caught — verifier defect
R4, F-5) and under a plain-run rule that let a url-less manifest record bind. This
counter replays the three named mutants against a **copy** of the landed instrument
bytes and applies a tightened rule with two independent oracles:

- **Output shape.** A `--selftest` span is accepted only with one
  `selftest case=<name> … verdict=pass` line per case, a `selftest cases=N failures=0`
  summary where N equals the case-line count, the pristine bytes' case-name multiset,
  and (pristine side only) `N >= CASE_FLOOR=19`. A summary-only span is rejected as
  `summary-only`; a forged `cases=0` summary is rejected by the floor and by the
  case-set comparison.
- **External fixtures.** Eight fixture lanes, one per documented failure family:
  `record-without-url` (no `url` → exit 1, `detail=absent`, `unbound=1`),
  `per-file-orphan` (capture with no record → exit 1, `rule=orphan-capture`,
  `orphans=1 orphan=S009.txt`), `unnamed-record-id` (no `id` → `rule=no-row
  record=<unnamed>`, exit 1), `stale-orphan-declaration` (declared orphan absent →
  `rule=orphan-declared-missing`, exit 1), `malformed-fetched-utc` (impossible
  UTC-shaped stamp **and** unparsable string → `detail=malformed`, exit 1),
  `punctuated-url-cell` (registry cell URL ending in `.` still binds its clean
  record url → exit 0, `url_bound=1`), `malformed-orphan-declaration` (declared
  orphan without a `reason` → exit 2, `reason=manifest-shape`), `nested-legacy-round`
  (`round-31/inner` is legacy: an archival record passes → exit 0). These do not
  read the mutant's own selftest.
- **Named-row pins and gates.** `ROW_PINS` holds the literal `find` and
  `find\0replace` sha256 of each named row, so a substituted named patch is
  `invalid:anchor-mismatch`; the `named-rows` gate requires the pinned name set to
  equal `MUTANTS` with each name present once; a `killed` verdict with an empty
  `killed_by` is `invalid:inconsistent-kill`. An edit that rewrites the summary line
  itself is not defensible in-band — the header prints `counter_sha256`, so bind the
  counter bytes before trusting the zero.

Each row is an exactly-once `find`/`replace` (QUALITY R17): `find` must occur once,
the patch must change bytes, and the mutant must compile (`py_compile`) before any
probe. An unevaluable row is `invalid:<reason>` (exit 1); it is never relabelled
killed or counted as a survivor. `killed` means "a probe the pristine bytes pass is
failed by the mutant", not "the mutated limb is the sole cause".

```
sha256sum corpus/instruments/capture-binding-check.py corpus/instruments/kill-rule-check.py
python3 corpus/instruments/kill-rule-check.py; echo "exit=$?"
python3 corpus/instruments/kill-rule-check.py --selftest; echo "selftest_exit=$?"
```

Measured at instrument digest `3d9e5e0d…` (40556 B, 892 lines, `--selftest`
`cases=23`): three `mutant=<name> killed=1` lines (`skip-selftest-summary` by
`selftest-shape`; `accept-record-without-url` by `selftest-shape` + `record-without-url`;
`per-file-binding-removal` by `selftest-shape` + `per-file-orphan`),
`controls=4 rejected=4`, `gates=7 failed=0`, and the final `survivors=0`, exit 0.
Counter bytes of record: `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61`
(43138 B, 881 lines), which prints `counter_sha256=c279d952…` in its header.

The probe set grew under attack. `MutKillRuleMutants` reported three behaviour-bearing
survivors at earlier generations (`unnamed-id-guard-removal`, `url-token-normalization-removal`,
and the two `malformed` acceptance variants); `CritC1Kill` reported a false-zero path
(a substituted named row plus a forced `killed` verdict). Replayed at the current bytes
through `--row-file`, every reported survivor is killed by exactly the probe that pins
its limb and by no other probe (`selftest-shape` shows `mutant=pass` for each):
`unnamed-record-id`, `punctuated-url-cell`, `malformed-fetched-utc` (one record per
malformed path), `stale-orphan-declaration` — measured `mutants=9 killed=8
survivors=1 invalid=0` where the single survivor is the deliberately comment-only red
row. The critic's two-edit attack now fails three ways: `invalid:anchor-mismatch`
(pin), `invalid:inconsistent-kill` (guard, with the pin check removed), and
`GATE fail name=named-rows` (a renamed row), each at exit 1.

Controls, on every run: `CTL-noop` (`invalid:noop`, never a kill), `CTL-nocompile`
(`invalid:nocompile`, never a kill), `CTL-equivalent` (a comment-only patch no probe
can see: `survivor`, and the witness line `witness_survivors=1 witness_exit=1`), and
`CTL-fake-killrule` — the newest `.ufo/waves/round-*/c1-controls/fake-killrule.py`,
which prints `survivors=0` without replaying anything: its span carries no `mutant=`
line, no patch digest and no `mutants=` line (`verdict=opaque`) and still prints
`survivors=0` on the survivor witness, so `differs=1`. An attack seat adds rows with
`--row-file PATH` (`{"rows": [{"name","find","replace","note"}]}`), measured and
counted like the named rows: a deliberately surviving row prints `survivors=1` and
exits 1. `--selftest` checks only this counter's verdict arithmetic (green / one
survivor / one invalid), not the instrument.

**Known limits.** Patch anchors bind to the bytes measured at run time — different
instrument bytes produce `invalid:find-count` and exit 1 rather than a silent zero.
The fixture probes assert the documented contract lines, not every printed line, so a
mutant that leaves those lines intact survives. A selftest-only defect (mutant 1) has
no external probe by construction. The fake control binds to the newest round's
`c1-controls/fake-killrule.py`; if that path moves, the control reports `absent`
(`ok=0`, a failed gate) until `--fake PATH` is supplied — it is never skipped.

## Round-44 registry addition — the round-43 instruments and the round-44 counter (appended 2026-10-28)

The round-43 SHONEN bullet named `corpus/instruments/README.md` as the registry
for the two round-43 instruments; this file existed but carried no matching row
(routed defect 7 of `corpus/lessons/round-43-verifier-spotcheck.md` §6). The rows
are appended here. The gates' home registry remains the `SKILL.md` *Gates &
probes* section, which already carries the same rows; this section makes the
pointer in the round-43 bullet true as written.

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| r43-closure.sh | gate | `bash corpus/instruments/r43-closure.sh --export-ref <hash> [--receipt-out PATH] [--lane DIR] [--work DIR] [--scratch-root DIR]` (export-mode only; plain run refuses exit 2) | one `K<n> payload=… closed=0\|1` per K1-K19, then `closed=K/19 exit=0\|1`; exit 0 only for K=19 | `bash corpus/instruments/r43-closure.sh --selftest --export-ref <hash>` → nineteen graded cases and `selftest cases=19 failures=0` | `.ufo/waves/round-43/claims.json`, `.ufo/waves/round-43/final-gates/`, `corpus/instruments/r43-limbs/` | read-only (export and receipt-out in scratch only) | kasegi (round 43; 19 checks) |
| claim-package-check.py | gate | `python3 corpus/instruments/claim-package-check.py <package-dir>` | one `RULE <id> verdict=pass\|fail` per rule; `package=<path> rules=8 pass=<k> fail=<m> verdict=WELL-FORMED\|DEFECT exit=0\|1` | `python3 corpus/instruments/claim-package-check.py --selftest` → `selftest cases=10 failures=0` | `corpus/instruments/fixtures/claim-package/` (exemplar and nine named defect fixtures) | read-only over the supplied package | kasegi (round 43) |
| r44-routed-defects.py | counter | `python3 corpus/instruments/r44-routed-defects.py --root <tree> [--baseline <tree>]` | one `R44-D<n> status=fixed\|unresolved detail=…` line per limb (eight routed defects of `corpus/lessons/round-43-verifier-spotcheck.md` §6), then `routed-defects total=8 fixed=<k> unresolved=<n> exit=0\|1`; exit 0 only when unresolved=0 | `python3 corpus/instruments/r44-routed-defects.py --root <tree> --selftest --work <dir>` → one `selftest case=<id> verdict=pass\|fail` per case and `selftest cases=<n> failures=<k>`; every mutant keeps the prose marker and drops the artifact the limb binds to, and must be rejected | `.ufo/waves/round-43/claims-erratum-6.md`, `corpus/lessons/round-43.md`, `corpus/lessons/round-44.md`, `LOG.md`, `SHONEN.md`, `SCORECARD.md`, `corpus/instruments/README.md` | read-only over the graded tree; the selftest writes only under `--work` | kasegi (round 44) |
| wave-registry.py | emitter | `python3 corpus/instruments/wave-registry.py --results <wave>-results.json --out <registry> [--lane kasegi]` | writes `wave=`, `lane=`, `policy=`, `seats=`, `roles=`, `attack_seats=`, `names=`; refuses (exit 1) when the results file's `seats` count and its named seats disagree, so an empty `names=` field can never be emitted | the round-44 registry `.ufo/waves/round-44/wave-registry.txt` is its committed output and is graded by `r44-routed-defects.py` limb D5 | `.ufo/waves/round-44/wave1-results.json` | writes only the `--out` path | kasegi (round 44) |
