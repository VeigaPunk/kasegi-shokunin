# VacuityDisclosure — round-23 C1 falsify (leaf, read-only)

Seat: `L1Kasegi23.VacuityDisclosure-2`. Attack surface: C1 guard clause
(`.ufo/waves/round-23/claims.json`), the no-harm receipts, and the filed lesson —
specifically sentences readable as source-availability / corpus-resolution claims,
and places where the host `mirror=0` vacuity is not disclosed next to a
changed-verdict count.

## Snapshot (the lane tree moved under this seat)

| object | HEAD `953c278` (committed) | live worktree, `2026-10-25T06:47Z` |
|---|---|---|
| `corpus/instruments/resolve.py` | `ed9a9dae1002…` | `8dd45bc8d9ae…` (mtime 03:42:37) |
| `corpus/instruments/mirror-containment-check.py` | `1bc2db10dfbc…` | `53742c8d9529…` (mtime 03:43:01) |
| `corpus/instruments/mirror-containment-fixtures.json` | `5e61a33ed5fa…`, 13 cases | `4e39f65c7c1b…`, 20 cases (mtime 03:43:01) |
| `.ufo/waves/round-23/c1-fixed.json` | resolver `ed9a9dae…`, matrix `5e61a33e…`, 13/13 pass | resolver `8dd45bc8…`, matrix `5c64e014…`, 17/17 pass, `checker_sha256 53742c8…` |
| `.ufo/waves/round-23/c1-baseline.json` | resolver `d6a3c3f1…`, matrix `5e61a33e…`, 7/13 pass (0/6 escape) | same resolver, matrix `5c64e014…`, 10/17 pass (0/7 escape) |

The worktree was being rewritten by other seats while this seat ran
(`c1-*.json`, `resolve.py`, checker, fixtures, knowledge entries and manifest all
have 03:40–03:43 mtimes). Nothing below was caused by this seat; every run used a
`/tmp/kasegi-r23-falsify-VacuityDisclosure` copy.

Reproduced, not assumed:
- HEAD-only evidence set (blobs of resolver+checker+fixtures at `HEAD`) →
  `cases=13 escape=6 controls=7 pass=13 fail=0`, exit 0, `matrix_sha256=5e61a33e…`.
  The committed set is self-consistent.
- Live triple (worktree bytes) → `cases=20 escape=9 controls=11 pass=20 fail=0`,
  exit 0, `matrix_sha256=4e39f65c…`.
- Frozen-corpus guard on the `922a4dd` export with both HEAD and live resolver:
  live bytes give the same line as HEAD at the same unpack path
  (`distinct=1589 resolves=11 mirror=0 internal=197 other=0 gone=1381
  skill=39/513 corpus=192/1262 all=208/1589`).

## Verdict on the assigned hypothesis

**Falsified as stated.** Every publication of a changed-verdict count does carry
the `mirror=0` vacuity in the same paragraph/row:

- `corpus/lessons/round-23.md:135-142` — numbers, then “**The guard is vacuous on
  this host**: `mirror=0` because neither mirror candidate exists … published as
  vacuity”.
- `SCORECARD.md:403` — “`changed=0 added=0 dropped=0`, `mirror=0` (published as
  vacuous)”, same cell.
- `LOG.md:1130-1133` — “`mirror=0` on this host makes that diff vacuous; published
  as vacuity”.

What survives is adjacent and worse in kind: the disclosure and disclaimer are
bolted to counts that no longer describe any live artifact, and the guard's other
half (density, anchorcheck) was never reported at all.

## Findings

### F1 — published C1 counts are one to two generations behind the evidence (depth:verifiability)

Counterexample: the lesson's counter table cannot be reproduced from *any* current
artifact.

- `corpus/lessons/round-23.md:118` — “**Before → after** (same 13-case matrix,
  `matrix_sha256=5e61a33e…b5e76a9`)”; `:122-124` — `0/6 → 6/6`, `7/7 → 7/7`,
  `7/13 → 13/13`; `:132` — “still scores 0/6 on the target”.
- `SCORECARD.md:412-415` — “Exercised this round (13/13 and 7/13 receipts…)”.
- `LOG.md:1125-1129` — `0/6`, `7/13`, `6/6`, `13/13`.
- Live receipts: 17 cases, `matrix 5c64e014…`, `0/7 → 7/7`, `10/17 → 17/17`
  (`python3 -c 'import json; …'` over `.ufo/waves/round-23/c1-{baseline,fixed}.json`).
- Live fixture file: **20 cases** (`4e39f65c…`) — already newer than the receipts
  that cite it (`5c64e014…`). My own run of the live triple: 20/20, exit 0.

So there are three generations: narrative (13) → receipts (17) → matrix (20). The
vacuity sentence at `:138-142` is attached to the 13-case numbers, so it discloses
vacuity for an evidence set that is no longer the one under test. Impacted axis:
depth:verifiability (C1's own evidence). Smallest safe correction: in the same
sentence, state the count as `<escapes>/<cases>` **and** the `matrix_sha256` of the
fixture file being counted, and regenerate `:118-132`, `SCORECARD:403/412-415` and
`LOG:1125-1129` from the final sha before landing; never carry a count without its
sha.

### F2 — the guard's density/anchorcheck half is unreported (claims.json C1 guard)

The guard clause reads: “Frozen pre-round SKILL, PROVINCE and corpus against each
detector; report all changed verdicts, **density and anchorcheck**.”

Evidence that it was not reported:
- `grep -n "density\|anchorcheck" corpus/lessons/round-23.md` → **no match**
  (exit 1). The same grep over the r23 `SCORECARD.md`/`LOG.md` entries finds only
  the prose claim “depth:density was not touched this round”
  (`SCORECARD.md:406`), not a value.
- The only r23 density/anchorcheck measurements are
  `.ufo/waves/round-23/before-instruments.json` → `results.density` and
  `results.anchors` (pre-round only; no after-run artifact exists). No filed
  document references it:
  `grep -rn "before-instruments" --include=*.md .` → only
  `.ufo/waves/round-23/build/*.md` (inherited seat reports), none in
  lesson/SCORECARD/LOG.

The delta is provably zero (`git show --stat 953c278 | grep -i SKILL` → no match;
`git diff 922a4dd 953c278 -- SKILL.md` → empty), but “zero by byte-identity” is not
what the guard asked for, and the filed text does not say it. Impacted axis:
depth:verifiability. Smallest safe correction: one sentence in the C1 guard
paragraph citing the `before-instruments.json` density/anchorcheck outputs and
stating SKILL.md is byte-identical between `922a4dd` and the landing, so both
deltas are 0 — or run both after the change.

### F3 — the frozen-corpus numerator depends on where the export is unpacked (depth:verifiability)

Same committed resolver bytes (`ed9a9dae`), same export content, two unpack paths:

| export path | published line | `../../../.ufo/l0-questions.md` |
|---|---|---|
| `/tmp/kasegi-r23-falsify-VacuityDisclosure/a` (as in `before-instruments.json`: `/tmp/kasegi-r23-xuj7ohl9/before`) | `internal=197 … all=208/1589` | `GONE` |
| `/tmp/kasegi-r23-falsify-VacuityDisclosure/cur/export` | `internal=198 … all=209/1589` | `INTERNAL`, path `…/cur/export/../../../.ufo/l0-questions.md` |

Root cause chain, all locally observable: `corpus/README.md:54` (in the `922a4dd`
export) cites `../../../.ufo/l0-questions.md`; the relative branch
`exists_any(join(lane_root, base)) → INTERNAL` is unconfined by design (the
carve-out the lesson discloses at `:143-145`); `/tmp/.ufo` is a symlink to
`/home/vgpnk/Projects/shokunin/.ufo` (`readlink -f`, link mtime Oct 24 04:44), and
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` exists. Three levels above
`…/cur/export` is `/tmp`, so the token resolves. A nested control at
`/tmp/…/deep/nest/export` (third ancestor `deep`, no `.ufo`) returns `197/208`
again, so it is the specific ancestor, not depth as such.

Consequence: “baseline and landed resolver bytes run against that identical
export … in both runs” (`lesson:135-138`) is only reproducible at the depth the
author happened to use; the lesson's counting command (`:105-113`) does not show
where the export is unpacked. Any re-runner who extracts to
`/tmp/<dir>/<name>/` gets a census that differs by one INTERNAL from the filed
number, and the diff then shows a `GONE → INTERNAL` verdict change that is an
artifact of the path, not of the resolver. Impacted axis: depth:verifiability.
Smallest safe correction: pin the unpack path in the published counting command
(e.g. `git archive 922a4dd | tar -x -C /tmp/kasegi-r23-guard/export` exactly once,
reused for both runs) and add one clause: “the `../../../`-style token classifies
INTERNAL iff an ancestor three levels above the export contains `.ufo`”.

### F4 — `distinct=1589` vs `distinct base=1588 fixed=1588` is unexplained (depth:verifiability, minor)

The lesson prints both numbers in one paragraph (`:137`, `:139`) without
reconciling them. Reproduced cause: the TSV carries one row per (citation,
scope-parent), and `evidence-manifest/v1` appears twice in both runs —
`[... 'GONE','', '1','','rel','1','+CORPUS']` and `[…,'SKILL']` — so 1589 records
collapse to 1588 unique `citation` keys:

```
$ python3 - <<'PY'  # over base/ and fix/ citation-survival.tsv (both from ed9a9dae / ed9a9dae-era runs)
records 1589 uniq 1588 dup keys: [('evidence-manifest/v1', 2)]
PY
```

A dict-keyed class diff therefore compares 1588 keys, not the 1589 the census
advertises; if those duplicate rows ever diverged in class the diff would be
last-wins and silently drop a changed verdict. Here both rows are `GONE` in both
runs, so `changed=0` survives — the defect is the undisclosed keying, not a missed
change. Smallest safe correction: print `rows=1589 unique_citation_keys=1588
(duplicate: evidence-manifest/v1, scopes SKILL/+CORPUS)` or key the diff on
`(citation, scopes)`.

### F5 — the C1 instrument of record is missing from both instrument indexes (depth:verifiability)

The lesson rests C1 on the matrix (“the matrix — not the frozen-corpus diff — is
C1's evidence”, `:141-142`), but the matrix is undiscoverable from the indexes:

- `corpus/README.md:35` — “Depth instruments (committed, re-runnable) |
  `instruments/{density.py,resolve.py,anchorcheck.py,README.md}` +
  `instruments/citation-survival.{md,tsv}`” — no `mirror-containment-check.py`,
  no fixtures file.
- `grep -rn "mirror-containment" corpus/README.md README.md
  corpus/instruments/README.md` → **no output**.
- Only `SCORECARD.md:412-417` names it (the capability entry).

Smallest safe correction: add the checker+matrix row to
`corpus/instruments/README.md` and extend `corpus/README.md:35`, so a reader who
follows the committed-instrument list can reach C1's evidence.

### F6 — observation on the live repair (not a finding against HEAD; overlaps the freeze-order seat)

The live checker now emits `path_check`/`resolved_path` and `checker_sha256`, and
the live fixtures carry `"path_tolerance": "carve-out"` on
`lane-relative-parent-internal-control` (`../outside.md` → `INTERNAL` for a path
outside the lane, with a `note` saying so). At 03:39–03:40, before the tolerance
landed, a mixed snapshot — resolver `9e0b5751`, path-checking checker, the frozen
13-case `5e61a33e` fixtures — produced **12/13**, failing exactly that case on
`path_check=path-outside-internal`. The HEAD checker (`1bc2db10`) has no path
assertion at all (HEAD receipts contain no `path_check` key), which is why HEAD
reproduces 13/13. I am not claiming this as a defect of the committed state; it
shows that the path assertion and the frozen matrix were momentarily
unsatisfiable together, and that the tolerance attribute is what reconciles them.
Routed to the freeze-order seat's scope, not scored here.

## Sentences that can be read as source-availability / corpus-resolution claims

Line numbers are for `corpus/lessons/round-23.md` at HEAD `953c278` (file
unmodified in the worktree), `SCORECARD.md`, `LOG.md`, `corpus/README.md`.

| # | location | sentence (excerpt) | reading risk | verdict |
|---|---|---|---|---|
| 1 | lesson:6-7 | “Neither claim restores a lost domain source. Score 4/7 remains held” | none — explicit disclaimer | safe, but 170 lines from the registry row at #11 |
| 2 | lesson:22-23 | “The prior source losses and 23/25 legacy recheck failures remain known historical limits, not recovered or converted to passing by local copies.” | none | safe |
| 3 | lesson:62 | “Source-row transition: S018 `status: queued → mined`, `used-by: — → …`” | reads as source availability gained (a `mined` flip is content acquisition, not restoration) | low: true but not adjacent to any “not restored” qualifier |
| 4 | lesson:118-124 | counts `0/6 → 6/6`, `7/7`, `7/13 → 13/13` | reads as a detector/resolution improvement with fresh evidence | **unsafe**: counts are stale (F1) |
| 5 | lesson:132 | “still scores 0/6 on the target” | same | **unsafe**: stale count (F1) |
| 6 | lesson:135-142 | guard numbers + “**The guard is vacuous on this host** … published as vacuity” | reads as reproducible no-harm evidence | **partially unsafe**: disclosure present, but the numbers are unpack-path dependent (F3) and the 1589/1588 pairing is unexplained (F4) |
| 7 | lesson:146-147 | “Score held at **4**: instrument correctness only; no restored source, no citation availability change.” | none | safe, adjacent to #6 |
| 8 | lesson:161-164 | “`S018` exit 0 … `S029` exit 0 … `S030` exit 0” | can be read as corpus recheck/resolution improvement (red→green) | scoped only 51 lines later by “C2 evidence ceiling … proves quote-in-capture, not current online law or freshness” (`:212-214`); acceptable but scope is non-adjacent |
| 9 | lesson:167-175 | “Admission rows: … F06→… F07→… F08→…” + “Frozen denominator `5/8 → 8/8`” | coverage, not availability; the adjacent `5/8 → 8/8` could be misread as a resolvability gain | safe as coverage; the sentence itself names no source availability |
| 10 | lesson:176-177 | “Score held at **7**: the r15 domain-root denominator is untouched by public-practice entries.” | none | safe, adjacent to #9 |
| 11 | lesson:233-236 | “SOURCES: registry rows 27 → 30 (tier A=28, C=2; status mined 18, queued 9, rejected 3; 18 rows carry `used-by`)” | reads as source inventory / availability growth | low: no adjacent qualifier; the nearest “not restored” statement is #1 ~170 lines earlier |
| 12 | `SCORECARD.md:403` | “**Improved, score held 4.** … `changed=0 added=0 dropped=0`, `mirror=0` (published as vacuous). Score held: instrument correctness, no source restoration or citation-availability change” | — | disclosure and disclaimer both adjacent: **correct in kind**; counts/sha stale (F1) |
| 13 | `SCORECARD.md:404` | “**Improved, score held 7.** … Score held: the r15 domain-root denominator is untouched by public-practice entries.” | “Improved” alone could be read as availability | safe: adjacent qualifier |
| 14 | `SCORECARD.md:406-409` | “**No axis harmed.** depth:density was not touched this round…” | asserts the guard outcome without the density/anchorcheck report | **unsafe as written** (F2): asserted, not reported |
| 15 | `SCORECARD.md:412-415` | “Exercised this round (13/13 and 7/13 receipts…)” | stale counter | **unsafe**: F1 |
| 16 | `LOG.md:1125-1133` | counts + “`mirror=0` on this host makes that diff vacuous; published as vacuity” | — | **correct in kind**; counts stale (F1) |
| 17 | `LOG.md:1134-1137` | “Counts: F06–F08 **0 → 3**, frontier **5/8 → 8/8**.” | coverage | safe as coverage |
| 18 | `corpus/README.md:195-202` | Frontier rows F06/F07/F08 “admitted” | corpus-state change | coverage claim; makes no availability claim |

No sentence in the filed artifacts claims that a *lost* source was restored, or
that corpus resolution improved as a result of C1. The only unqualified
“improved” words are `SCORECARD:403/404`, both followed in-cell by a
no-availability qualifier.

## Negative results (checked, not defects)

- The matrix is not vacuous: fixtures declare a disposable
  `HOME`/`KASEGI_MIRROR`/lane layout with `"mirror": "relocated/tbh"`, and the
  confined controls report `mirror=1` in both receipts, so the escape cases going
  `GONE` is not explained by mirror absence.
- The fixed receipt's `resolver_sha256` matches the committed resolver blob
  (`ed9a9dae` = `git cat-file blob HEAD:corpus/instruments/resolve.py`), and the
  baseline receipt's `d6a3c3f1` matches `.ufo/waves/round-23/c1-baseline-resolver.py`;
  both receipts share `matrix_sha256=5e61a33e` = HEAD fixture blob. Provenance of
  the HEAD receipts is sound.
- Class-keyed diff of the two frozen-corpus TSVs: `added=0 dropped=0
  changed-class=0` (the 198 “changed rows” my first tuple-diff reported are the
  resolved-path column only, which is expected when export roots differ).
- `before-instruments.json` `definition` says “git archive master export” while
  `revision` is `922a4dd`; at snapshot `master == 953c278` and `922a4dd` is an
  ancestor, and the recorded census reproduces exactly on the `922a4dd` export, so
  the wording is loose, not false. No count in it is relied on by F1–F5.

## Accidental writes and restoration (disclosed)

The resolver writes `citation-survival.{md,tsv}` next to its own file. My first
two runs (`python3 .ufo/waves/round-23/c1-baseline-resolver.py <export>` and
`python3 corpus/instruments/resolve.py <export>`) therefore wrote inside the repo:
`.ufo/waves/round-23/citation-survival.{tsv,md}` (created; deleted) and
`corpus/instruments/citation-survival.{tsv,md}` (tracked; restored with
`git checkout --` → now `793e0a4e…`/`795ba4f2…`, i.e. HEAD blobs). All later runs
used copies in `/tmp/kasegi-r23-falsify-VacuityDisclosure/{base,fix,cur,pinned,head3,deep}`.
Current `git status --porcelain` shows no path attributable to this seat; the
remaining modifications are the sibling seats' 03:40–03:43 edits. If the lane
intended a regenerated working-tree census before my run, that content was not
recoverable and the files now equal HEAD — the L1 should regenerate deliberately
if wanted.

## Scope limits

- Judged only C1 disclosure/count integrity and the availability-wording inventory.
  I did not evaluate the F06–F08 entry content, registry row fields, snapshot
  quote fidelity, or C2 denominators; those belong to the C2 seats.
- I did not judge, admit, score, edit production files, or run the wave registry.
  No claim of admission or score movement.
- Line numbers for the lesson are HEAD `953c278`; the live worktree is being
  rewritten concurrently, so re-derive after the final landing.
- The F1 counts and F3 numbers are timestamped (`2026-10-25T06:47Z`); re-running
  the reproduced commands after the live repair may legitimately differ.
