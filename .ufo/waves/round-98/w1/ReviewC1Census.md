# ReviewC1Census — C1 revision-pinned citation census (round 98, attempt 1, w1)

Seat: `ReviewC1Census` (leaf reviewer; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Chain: base `2133f5b` → freeze `12bb2f9` → C2 landing `e2caf4a1` → C1 landing `e2d3de7`.
Reviewed: `corpus/instruments/census-at-rev.py` at `e2d3de7` (sha256 `66383371…`, matches the
claim pin), the census of record `corpus/instruments/citation-survival.md` (sha256
`86ca5da7…`), and the frozen C1 claim/harness in `.ufo/waves/round-98/`.
Receipts: `.ufo/waves/round-98/w1/ReviewC1Census-receipts/receipts.txt` plus the scripts,
fixtures and generated bodies in that directory. No tool installs or upgrades were needed.

## Environment note (affects how to read the runs)

The host has 1,663,194 files / 64 GB under `/home/vgpnk/Projects`; `resolve.py` resolves the
citation `` `~/Projects/**` `` (`corpus/lessons/round-15.md:87`) with
`glob.glob('/home/vgpnk/Projects/**', recursive=True)`. Unshimmed, that glob did not finish in
30 s, and three unshimmed `resolve.py` runs were terminated by signal 15 at 178–190 s
(`rc=143`; the instrument reported `CENSUS-WRITE error reason=resolve-rc-15 rc=2`). For the
verification runs I put a one-pattern shim on `PYTHONPATH` that returns
`['/home/vgpnk/Projects/']` for exactly that pathname — the first sorted match the real glob
returns and the value the round-19 TSV records (`~/Projects/**` → `/home/vgpnk/Projects/`).
Every other path is unmodified. All verdicts below are from the shimmed runs; the shim changes
no classification, only the runtime of that one pattern. Receipts: §"unshimmed runs" and
§"same command with the one-pattern shim".

## Numbers I got

Independent script: `independent-census-fast.py` (in the receipts), written from resolve.py's
documented path-like rule and resolution policy, importing nothing from the lane. It counts
distinct backticked path-like citations per scope and classifies relative tokens by existence
under the extract (literal / brace / glob); absolute tokens are counted in the denominators but
not existence-tested (they are the host-owned part, not the pinned numerator).

| item | census header (e2caf4a1) | my script (e2caf4a1) | `--check` (e2caf4a1) | my script (12bb2f9) |
|---|---|---|---|---|
| distinct citations | 7961 | 7961 | — | 7958 |
| contributing files | 334 | 334 | — | 333 |
| SKILL pinned (INTERNAL) | 162/732 | 162/732 | 162/732 | 162/732 |
| corpus pinned (INTERNAL) | 2551/7559 | 2551/7559 | 2551/7559 | 2550/7556 |
| lane pinned (INTERNAL) | 2589/7961 | 2589/7961 | 2589/7961 | 2588/7958 |
| host-inclusive SKILL | 166/732 | resolve.py: 166/732 | — | 166/732 |
| host-owned | 78 | 78 | 78 | 78 |

The census header is **correct for its `measured-at` revision**. The assignment text's
`corpus 2550/7556` and `lane 2588/7958` are the **freeze `12bb2f9`** measurement, not the
`e2caf4a1` measurement: the same script on a `git archive 12bb2f9` extract returns exactly
those numbers, and `--check` on a `12bb2f9` census with the `12bb2f9` pinned line passes
(`CENSUS-CHECK pass rev=12bb2f9… corpus=2550/7556 lane=2588/7958`). The C2 landing added
3 distinct citations, 1 of them INTERNAL: the set difference between the two fresh TSVs is
exactly `CI/CD Job tokenglcbt-`, `cell-<N>-`, `corpus/source-snapshots/round-96/S144.txt:356`,
all from the C2 knowledge entry `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`
(0 removed). The assignment's numbers are stale, not the census's.

## What reproduces

- **P1** — `python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work <fresh>` prints
  `CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78`, rc 0.
  It passes with a fresh work dir (no pre-existing cache) and with a cache hit.
- **P2** — the frozen harness re-run prints all 8 `CONTROL … PASS`, `ATTRIBUTION pass fixtures=8`,
  `C1-CONTROLS-RESULT pass controls=8 rc=0` (13.9 s shimmed). The `stale-rev` control measures
  `b06af5e` (round-97 base) and gets `pinned-mismatch` as declared.
- **P3** — `e2caf4a1` is an ancestor of `e2d3de7` (`git merge-base --is-ancestor` yes);
  `grep -c 'tree-e2caf4a1561b'` = 0 and `grep -c '/fast/scratch'` = 0 in the census;
  `Lane root: … (measured from the git-archive extract of e2caf4a1…)` is present.
- **Body is resolve.py's output** — a fresh `resolve.py` run in the same extract, with the
  instrument's documented rewrite (extract path → lane path, Lane-root line → named revision),
  matches the committed body except two host-dependent cells: the `.ufo/watchdog.log` line
  counts (3233 now vs 3230 when the census was generated). `--write` at `e2caf4a1` likewise
  reproduces the committed census except those two cells.
- **Host-owned line** — the instrument computes
  `sum(1 for c,_ in rows if c in ("RESOLVES","MIRROR-EQUIVALENT"))` (`census-at-rev.py:125`);
  the fresh TSV has 78 RESOLVES + 0 MIRROR-EQUIVALENT = 78, matching the header. All 78 are
  domain `other` (absolute, outside the lane), so the header's "absolute-path citations"
  wording is accurate **at this revision**.
- **Cache cross-revision isolation** — the cache key is the full 40-hex revision
  (`census-at-rev.py:86`). With the `e2caf4a1` cache present, a file whose `measured-at` is
  `12bb2f9` is measured fresh (`… corpus=2550/7556 lane=2588/7958`) and an `e2caf4a1` pinned
  line in that file fails `pinned-mismatch`. A cache entry for one revision is not reusable for
  another. This is the specific property the assignment asked about, and it holds.

## Findings

### F1 (high — claim wording / reproducibility): the pinned rate is not "revision-stable" for `../` citations

`extract()` puts the tree at `<work>/tree-<rev12>` (`census-at-rev.py:58-81`) and runs the
extract's own `resolve.py` with that directory as the lane root (`:94`). resolve.py's domain REL
policy deliberately keeps `../` walk-outs INTERNAL (`resolve.py` docstring, "domain REL"; the
`exists_any(os.path.join(lane_root, base))` call). The extract's parent is therefore the scratch
work directory, not the lane's parent.

Two citations in scope walk out:

- `corpus/knowledge/source-tree-loss-2026-09-28.md:315` cites `` `../MISSION.md:49-56` ``;
- `corpus/lessons/round-20-recensus.md:4` cites
  `` `../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kasegi*.md` ``.

In the live lane both targets exist (`/home/vgpnk/Projects/shokunin/MISSION.md`,
`/home/vgpnk/Projects/shokunin/.ufo/waves/…/KasegiGateRepair.md`), and the round-19 live-lane
TSV classifies both INTERNAL. In the extract the fresh TSV classifies both **GONE**, because
`<work>/MISSION.md` and `<work>/.ufo/...` do not exist. Concretely, a work dir whose parent
contains those two targets makes the same revision measure **corpus 2553/7559, lane 2591/7961**
and `--check` on the committed census fails `pinned-mismatch`; a clean work dir gives
2589/7961 and passes. The `--write` under the contaminated work dir also emits a body row
`| ../MISSION.md:49-56 | INTERNAL | …/kasegi-shokunin/../MISSION.md | 49-56 | 0 | OUT OF RANGE |`
— a path outside the lane, which the P3 `tree-e2caf4a1561b` grep does not catch.

So the census's "revision-stable" label and the instrument docstring's "the measurement is
deterministic for a revision" (`census-at-rev.py:23-25`) are overstated: the pinned numerator
is a function of the revision **and the scratch work directory's parent contents**. The frozen
definition ("lane-relative citations that exist in the extract") makes 2589 well-defined given
the extract location, and P1 passes with a clean scratch, but a checker whose scratch parent
happens to contain `MISSION.md`/`.ufo` gets a false failure. The two citations are exactly the
2-count gap between the extract measurement and a lane-located measurement (2589 vs 2591).
Fix options: run the extract at a path whose parent mirrors the lane's parent (or bind/symlink
the lane path), or confine `../` in the pinned definition, or document the scratch-parent
requirement in the header.

### F2 (high — verifiability): `--check` verifies only the pinned line; the body and host lines are unchecked

`check()` compares exactly one line (`census-at-rev.py:203-232`, comparison at `:222-228`). It
does not read the body, the `host-inclusive rate` line, or the `host-owned inputs` line. I
replaced the body with `GARBAGE BODY, NOT resolve.py OUTPUT` and kept the pinned line:
`CENSUS-CHECK pass … rc=0`. I replaced the host-inclusive and host-owned lines with
`0/0`/`9999` values and kept the pinned line: `CENSUS-CHECK pass … rc=0`. The control harness
has a `tampered-pinned` control but no body/host-line tamper control.

The claim's statement says "The body below the header is resolve.py's own generated output for
that revision" and specifies the host-inclusive and host-owned lines; P1's command enforces
none of that. The body claim is true **at generation** (I verified it with a fresh resolve.py
run), but the census of record can be edited after the fact and the one-command check still
passes. If the body is part of the claim, the check needs a body/host-line comparison (or a
sha256 of the body, or a full-file regeneration diff).

### F3 (medium — cache trust): same-revision cache is trusted without validation

The cache is read with no validation (`census-at-rev.py:86-90`) and written non-atomically
(`:152-154`, `json.dump` directly to the final path). Consequences I demonstrated:

- **Poisoned same-rev cache flips the verdict.** With the `e2caf4a1` cache rates changed to
  `999/732, 9999/9999, 9999/9999`, `--check` on the correct census fails `pinned-mismatch`;
  a census whose pinned line matches the poisoned cache passes
  (`CENSUS-CHECK pass … skill=999/732 corpus=9999/9999 lane=9999/9999`).
- **Truncated cache JSON crashes the instrument.** A killed write leaves a partial JSON; the
  next `--check` raises an uncaught `json.decoder.JSONDecodeError` and exits rc 1 (a traceback,
  not the documented rc 2 "could-not-evaluate").
- **The cache key omits the instrument version and the lane.** A cache produced by the
  pre-fix instrument (`435128a2…`, the body-rewrite erratum) in the same work dir would be
  reused by the current instrument (`66383371…`), returning the old body; a cache produced
  under one `--lane` names that lane in the body if reused under another.
- **The extract directory is reused without a completion marker** (`:58-61`: if
  `tree-<rev12>/corpus/instruments/resolve.py` exists, it is trusted). A run killed during
  `tar.extractall` can leave a partial tree that a later run measures and caches.
- The default work dir is `/tmp/census-at-rev` (`:244-245`), world-writable, combined with
  cache trust; the frozen command uses an explicit scratch, so this is a hardening note.

The cross-revision property the assignment named **does hold**; the broader "cache cannot mask
a wrong measurement" does not, for same-rev poisoning/staleness and partial extracts.

### F4 (medium — provenance): the frozen `harness_sha256` matches no committed harness

`claims.json` pins `harness_sha256 = d39a1fc8cc5ad189b5077dc03c1c3373bca59d77a120493163ccca63eb4f05e0`.
The committed harness is `0488d796…` at the freeze `12bb2f9` and `d9713268…` at the landing
`e2d3de7` (working tree = `d9713268…`); `git cat-file -t d39a1fc8…` says "Not a valid object
name". The instrument pin is correct (`66383371…` matches the committed instrument). The
harness behavior reproduces 8/8, so this is a provenance-pin defect, not a control failure: the
erratum (2) changed the harness after the freeze (fixture clone checks out `--base`) but the
pin was not updated at the landing. Anyone verifying the claim's provenance from the pin will
fail to find the artifact.

### F5 (medium — consistency): the committed TSV was not regenerated and contradicts the census

`git show e2d3de7:corpus/instruments/citation-survival.tsv | wc -l` = **5153** (5152 citations,
the round-19 table); the census MD has **7961** distinct citations. `git diff --stat e2caf4a1
e2d3de7 -- corpus/instruments/citation-survival.tsv` is empty — the landing changed the MD but
not the TSV. The census body's self-verification says
`diff <(pipeline to file) <(cut -f1 citation-survival.tsv | tail -n +2 | sort -u)` is empty
("sets identical"); against the committed tree that is false. The instrument regenerates the
TSV only inside the scratch extract and `--write` writes only the MD, so the landing leaves the
machine-readable companion stale. Either commit the regenerated TSV or drop the TSV-equality
claim from the body.

### F6 (medium — reproducibility): the body is resolve.py's output at generation, but not a pure function of the revision

The line-anchor table's "file lines" column is computed with `file_lines(r["path"])` on the
resolved path; for absolute citations that is a **host** file. The committed census records
`.ufo/watchdog.log` at 3230 lines; a fresh run now records 3233 (the log grew). The body is
therefore not reproducible from the revision alone, and the committed body already differs
from a fresh run. The claim's "body … for that revision" is true of the generation run, but a
reader re-running the instrument gets a different body. The pinned line is unaffected; the
host-inclusive line is documented as not revision-stable. This should be stated for the body
too (or the line-count column should be marked host-dependent).

### F7 (low — body content): the printed self-verification pipeline does not match the stated scope

The body prints `grep -ohP … SKILL.md corpus/README.md corpus/*/*.md` — depth 2 only — while
the scope is `corpus/**/*.md`. The extract has 371 `.md` files under corpus (82 at depth ≥3);
the printed pipeline yields **7930** on the fresh extract (it also includes the census itself,
which resolve.py excludes), and a corrected scope (`SKILL.md` + `corpus/**/*.md` minus the
census) yields **7946**, not 7961. The body's "both yield 7961" and "sets identical" are not
reproducible as printed. This text is inherited from resolve.py's static output (round 19), not
new in this landing, but it is part of the census of record.

### F8 (low — wording): "absolute-path citations" is broader than the code's definition

`host_owned` counts RESOLVES + MIRROR-EQUIVALENT (`:125`), and MIRROR-EQUIVALENT can be a
**relative** citation (domain `rel`) when the mirror exists. At this revision the mirror is
absent (`MIRROR-EQUIVALENT 0`), all 78 RESOLVES are domain `other` absolute paths, and the
header's wording is accurate. If the mirror is ever present, a rel-domain MIRROR-EQUIVALENT
would be counted on the "absolute-path" line. The assignment's definition
(RESOLVES+MIRROR-EQUIVALENT) matches the code; only the header wording is conditional.

### F9 (low — operational): the measurement inherits resolve.py's unbounded `~/Projects/**` glob

The one `~/Projects/**` citation triggers a recursive glob over 1,663,194 files / 64 GB. On
this loaded host the unshimmed runs were SIGTERM'd at 178–190 s; the instrument reports
`resolve-rc-15` rc 2. `--check` is therefore not reliably runnable under memory pressure, and
the claim's "controls reproduce when re-run after the landing" is at risk on a loaded host (my
shimmed re-run reproduces 8/8). The C1 landing's own receipt shows the controls passed when
generated. This is inherited from resolve.py, but the instrument's `--check` is the exposed
surface.

### F10 (low — hardening): the bare `--rev` path does not validate the revision

`--write` validates the rev (`:250-253`) and `--check` extracts 40 lowercase hex from the file
(`:209`), but the bare `--rev` measure path (`:255-263`) passes the raw string to the cache path
(`work/cache/<rev>.json`) and to `git archive`. A local tool, low risk; the frozen command does
not use this path. The default work dir `/tmp/census-at-rev` is world-writable (F3).

### F11 (info): extract dir reuse by `rev[:12]` and no completion marker

`extract()` keys the tree directory by the first 12 hex chars (`:59`). Two revisions sharing a
12-hex prefix would reuse the wrong tree; the probability is negligible. More practically, a
partial extraction after a kill is trusted if `resolve.py` is present (F3). A
`tree-<rev>.complete` marker written after `extractall` would close both.

### F12 (info): `Scope: … (334 files)` counts contributing files, not scanned files

resolve.py computes the parenthetical as the number of files that contributed at least one
citation. The scanned set is 371 files (SKILL.md + 370 corpus `.md`, the census excluded); 334
contributed. The old census's "224 files" had the same meaning. Minor ambiguity for a reader
comparing the scope to `find`.

## Residual risk and verification gaps

- The only deviation from a stock run is the one-pattern glob shim (documented above). The
  unshimmed `--check`/controls could not be completed on this host (SIGTERM/OOM); the shimmed
  runs are the evidence. The shim's result for `~/Projects/**` matches the round-19 TSV's
  resolved path and the real glob's first sorted match.
- The control harness's `stale-rev` control uses `b06af5e` (round-97 base); I did not record
  that revision's measurement, only that the control passed with `pinned-mismatch` as declared.
- C2 is out of scope for this seat. I used its landing only as the census's `measured-at` and
  confirmed the 3-citation delta (all from the C2 knowledge entry, 0 removed).
- The census file itself has no sha256 in `claims.json`; the claim pins only the instrument and
  harness. The body/host lines are therefore not provenance-pinned (F2/F5).
- I did not modify the lane, the fleet repo, `.ufo/state/`, or any sibling lane; the fixture
  clone and all extracts live in `/fast/scratch/hyaku/kasegi-r98/ReviewC1Census` and were
  removed after the receipts were copied.

## Verdicts

VERDICT: C1 pinned numbers at `measured-at e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` (SKILL 162/732, corpus 2551/7559, lane 2589/7961, host-owned 78, host-inclusive SKILL 166/732) — VERIFIED by independent re-derivation; the assignment's 2550/7556 and 2588/7958 are the freeze `12bb2f9` numbers, not the census's.
VERDICT: C1 P1 (`--check` pass, rc 0) — VERIFIED (fresh work dir; shimmed run).
VERDICT: C1 P2 (8/8 controls + `ATTRIBUTION pass fixtures=8`) — VERIFIED (shimmed re-run).
VERDICT: C1 P3 (measured-at ancestor, no scratch path, Lane-root line names the revision) — VERIFIED.
VERDICT: Cache cross-revision isolation (an entry for one revision is not reusable for another) — VERIFIED (full-40-hex key; demonstrated).
VERDICT: Body is resolve.py's own output — VERIFIED (fresh run matches except two host-dependent `watchdog.log` line-count cells).
VERDICT: Host-owned line is RESOLVES+MIRROR-EQUIVALENT distinct citations — VERIFIED (78; all absolute at this revision).
VERDICT: "Revision-stable" pinned rate — NOT VERIFIED / OVERSTATED (scratch-parent dependence via `../`; 2589 → 2591 and `--check` fails under a contaminated work dir).
VERDICT: `--check` verifies the body and host lines — NOT VERIFIED (garbage body and garbage host lines pass).
VERDICT: Harness `sha256` pin — NOT VERIFIED (`d39a1fc8…` matches no committed harness; freeze `0488d796…`, landing `d9713268…`).
VERDICT: Committed TSV consistency with the census — NOT VERIFIED (5152 vs 7961 citations; TSV unchanged at the landing).
VERDICT: Cache robustness (same-rev trust, corrupt JSON, version/lane scoping) — NOT VERIFIED.
