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
  with `--source`). Prints one line per entry and `entries=K pass=P exit=0|1`.
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
the frozen 13 stay 13. `frontier-recheck-count.py` needed no edit: its two limbs are
load-bearing on unchanged bytes once a fixture-backed kill exists.

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
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` (unchanged) |
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
