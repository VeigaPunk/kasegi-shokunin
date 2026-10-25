# VacuityDisclosure — round-23 C1 falsify (leaf, read-only)

Seat: `L1Kasegi23.VacuityDisclosure-2`. Attack surface: the C1 guard clause in
`.ufo/waves/round-23/claims.json`, the no-harm outputs, and the filed lesson —
specifically (a) sentences readable as source-availability / corpus-resolution
claims and (b) places where the host `mirror=0` vacuity is not disclosed next to a
changed-verdict count.

## Revisions judged (the lane committed 8 revisions during this seat's run)

| revision | what it is | how judged |
|---|---|---|
| `953c278` | first landed C1 (13-case matrix) — the state this seat was assigned | judged in full; findings F1a, F6 recorded there |
| `2712c99` → `4d9231e` → `12edac4` → `8acb255` | post-wave repairs, 20-case then 23-case matrix, errata blocks | re-verified; F1a became resolved |
| `bf9ce02` | rescue: 24-case matrix, corrected census, forced docstring | **primary pinned evidence set — every reproduction below is from its blobs** |
| `f6966d4` → `5842ef7` | receipts carry per-case method/domain; wave reports amended | spot-checked: F2, F3, F4, F5 and F1b unchanged |

Pinned blobs at `bf9ce02` (also current at `f6966d4` except the checker, which is
`dddd5549…` there and is bound correctly in both the lesson and the receipts):
`corpus/instruments/resolve.py` = `690153adc3e3…`,
`mirror-containment-fixtures.json` = `d05b1e0cf627…` (24 cases: 12 escape,
12 control), `mirror-containment-check.py` = `53742c8d9529…` at `bf9ce02` /
`dddd55496b55…` from `f6966d4`; receipts `c1-baseline.json` 12/24 pass (12 fail,
0/12 escape GONE) and `c1-fixed.json` 24/24 pass, both `checker_sha256`-bound.

Reproduced by this seat from committed blobs (commands in “Reproduce” below):
- landed set → `cases=24 escape=12 controls=12 pass=24 fail=0`, exit 0,
  `matrix_sha256=d05b1e0c…`, `resolver_sha256=690153ad…`;
- do-nothing control (`.ufo/waves/round-23/c1-baseline-resolver.py`,
  `d6a3c3f1…`) → `pass=12 fail=12`, exit 1, same matrix sha;
- frozen-corpus census on the `922a4dd` export with the final resolver → the
  published guard line, one citation exception described in F3.

Earlier defect, for the record: at `953c278` the narrative counted a 13-case
matrix (`5e61a33e…`), the receipts had moved to 17 cases (`5c64e014…`), and the
fixture file to 20 (`4e39f65c…`) — three generations at once. That is fixed at
`bf9ce02`+ (F1a).

## Verdict on the assigned hypothesis

**Falsified as stated** — no publication of a changed-verdict count lacks the
vacuity disclosure:

- `corpus/lessons/round-23.md:135-142` — numbers, then “**The guard is vacuous on
  this host**: `mirror=0` because neither mirror candidate exists … published as
  vacuity”.
- `SCORECARD.md:403` — “`changed=0 added=0 dropped=0`, `mirror=0` (published as
  vacuous)”, same cell.
- `LOG.md:1130-1133` — “`mirror=0` on this host makes that diff vacuous; published
  as vacuity”.
- `SCORECARD.md:433-437` and `LOG.md:1187-1189` (final counts) rest on the matrix,
  which is **not** vacuous: the fixtures declare a disposable
  `HOME`/`KASEGI_MIRROR`/lane layout (`"mirror": "relocated/tbh"`) and the confined
  controls report `mirror=1` in the receipts, so GONE is not mirror absence.

What remains is adjacent: the guard's `mirror=0` disclosure is correct, but the
guard is not reproducible (F3), is not bound to a resolver sha (F1c), its
density/anchorcheck half is unreported (F2), its key universe is undisclosed (F4),
and one stale count pair still sits unlabeled in `SCORECARD.md` (F1b).

## Findings

### F1a — RESOLVED AT SEAL: counts were three generations apart at `953c278`

At `953c278` the lesson’s table said “same 13-case matrix, `5e61a33e…`”, while the
worktree receipts had already grown to 17 cases (`5c64e014…`) and the fixture file
to 20 (`4e39f65c…`); my replay of the live triple gave 20/20. Now the pattern is
right: lesson `:259-270` (“Corrected C1 measurement (supersedes the 13-case numbers
earlier in this lesson; they stay as history)”), `SCORECARD.md:430-431` (“Append-only
corrections to the result table above; the earlier cells stand as the first
landing’s assessment”) with its C1 bullet at `:433-440`, `LOG.md:1187-1189`, all naming `matrix_sha256=d05b1e0c…`
and `resolver_sha256=690153ad…`, and I reproduce both receipts exactly. No action.

### F1b — `SCORECARD.md:414` still asserts the 13/13 and 7/13 exercise, unlabelled

Current text: “Exercised this round (13/13 and 7/13 receipts, three failing recheck
controls).” The final receipts are **24/24** and **12/24** (`d05b1e0c…`), and the
document’s own errata (`:433-437`) supersedes only “the earlier ‘6/6, 13/13’
**cells**” of the result table — the capability entry below that table is not named,
so the stale pair stands in the same document without an adjacent pointer. Impacted
axis: depth:verifiability (count integrity). Smallest safe correction: append
“first landing’s matrix; final is 24/24 / 12/24, `d05b1e0c…`” to the capability
entry, or move it under the errata heading.

### F1c — the guard paragraph is not bound to the final resolver sha

`corpus/lessons/round-23.md:135-142` is the only statement of the guard in the
sealed corpus (the errata blocks report matrix counts only). It says “baseline and
landed resolver bytes” without naming either sha; the landed bytes at that point
were `ed9a9dae…`, the final landed resolver is `690153ad…`. I re-ran the guard with
`690153ad…` and the numbers coincide (`1589/11/0/197/0/1381`, same unpack depth), so
there is no numeric error today — but a re-runner cannot tell from the text which
bytes produced it, and F3 shows the number moves with the unpack path. Smallest safe
correction: one appended line — “final resolver `690153ad…` on `922a4dd` unpacked at
`<path>`: identical 1589/11/0/197/0/1381 …; matrix, not this diff, is the C1
evidence (mirror=0, vacuous)”.

### F2 — the guard’s density/anchorcheck half is unreported (claims.json C1 guard)

Guard clause: “Frozen pre-round SKILL, PROVINCE and corpus against each detector;
report all changed verdicts, **density and anchorcheck**.”

- `grep -c 'density\|anchorcheck' corpus/lessons/round-23.md` → **0** (also 0 at
  `f6966d4`/`5842ef7`).
- The r23 entries of `SCORECARD.md`/`LOG.md` report no value; `SCORECARD.md:406-409`
  asserts “depth:density was not touched this round” instead of reporting it.
- The only r23 density/anchorcheck measurements are
  `.ufo/waves/round-23/before-instruments.json` (`results.density`,
  `results.anchors`; pre-round only) and **no filed document cites it**:
  `grep -rn "before-instruments" --include=*.md .` returns only
  `.ufo/waves/round-23/build/*.md` (inherited seat reports).

The delta is provably zero — `git show --stat 953c278 | grep -i SKILL` → no match;
`git diff 922a4dd 953c278 -- SKILL.md` → empty — but the guard asked for the report,
and byte-identity is the argument the text never makes. Impacted axis:
depth:verifiability. Smallest safe correction: one sentence citing the
`before-instruments.json` density/anchorcheck outputs plus the SKILL.md byte-identity
(the deltas are 0 by construction), or run both instruments after the landing and
publish both numbers.

### F3 — the frozen-corpus numerator depends on where the export is unpacked

Same final resolver bytes (`690153ad…`), same export content, two unpack paths:

| export path | printed line | `../../../.ufo/l0-questions.md` |
|---|---|---|
| `/tmp/kasegi-r23-falsify-VacuityDisclosure/a` (matches `before-instruments.json`’s recorded path depth, `/tmp/kasegi-r23-xuj7ohl9/before`) | `internal=197 … all=208/1589` | `GONE` |
| `/tmp/kasegi-r23-falsify-VacuityDisclosure/cur/export` | `internal=198 … all=209/1589` | `INTERNAL`, path `…/cur/export/../../../.ufo/l0-questions.md` |

Chain, all locally observable: `corpus/README.md:54` (in the `922a4dd` export)
cites `../../../.ufo/l0-questions.md`; the relative branch
`exists_any(join(lane_root, base)) → INTERNAL` is unconfined by design (the
carve-out the lesson names at `:143-144`); `/tmp/.ufo` is a symlink to
`/home/vgpnk/Projects/shokunin/.ufo` (`readlink -f`; link mtime Oct 24 04:44) and
`…/shokunin/.ufo/l0-questions.md` exists. Three levels above `…/cur/export` is
`/tmp`, so the token resolves. A control at `/tmp/…/deep/nest/export` (third
ancestor without `.ufo`) returns `197/208` again — it is the specific ancestor, not
depth as such.

Consequence: “baseline and landed resolver bytes run against that identical export
… in both runs” (`:135-138`) reproduces only at the author’s unpack depth; the
counting command (`:105-113`) never states it. A re-runner who extracts to
`/tmp/<dir>/<name>/` sees a census one INTERNAL higher and a spurious
`GONE → INTERNAL` class change. Impacted axis: depth:verifiability. Smallest safe
correction: pin the unpack path in the published command and add one clause:
“the `../../../`-style token classifies INTERNAL iff an ancestor three levels above
the export contains `.ufo`”.

### F4 — `distinct=1589` vs `distinct base=1588 fixed=1588` is unexplained

`corpus/lessons/round-23.md:137` prints 1589; `:139` prints 1588 for the diff, in
the same paragraph, with no reconciliation. Cause reproduced on the final resolver:
the TSV has one row per (citation, scope-parent) and `evidence-manifest/v1` appears
twice — scopes `+CORPUS` and `SKILL` — so 1589 records carry 1588 unique `citation`
keys:

```
records 1589 uniq 1588
dups [('evidence-manifest/v1', 2)]
```

A dict-keyed class diff therefore compares 1588 keys, not the 1589 the census
advertises; if those two rows ever diverged in class the diff would be last-wins and
would silently drop a changed verdict. Today both rows are `GONE` in both runs, so
`changed=0` survives — the defect is the undisclosed keying. Smallest safe
correction: print `rows=1589 unique_citation_keys=1588 (duplicate:
evidence-manifest/v1, scopes SKILL/+CORPUS)` or key the diff on
`(citation, scopes)`.

### F5 — the C1 instrument of record is missing from both instrument indexes

C1’s evidence is the matrix, but the matrix is undiscoverable from the indexes a
reader is told to use:

- `corpus/README.md:35` — “Depth instruments (committed, re-runnable) |
  `instruments/{density.py,resolve.py,anchorcheck.py,README.md}` +
  `instruments/citation-survival.{md,tsv}`”; no `mirror-containment-check.py`, no
  fixture file.
- `grep -c mirror-containment corpus/README.md corpus/instruments/README.md` →
  **0 / 0** (also 0 at `f6966d4`).
- Only `SCORECARD.md:412-417` names it (capability entry) — the same entry that
  carries the stale counts (F1b).

Smallest safe correction: add the checker+matrix row to
`corpus/instruments/README.md` and extend `corpus/README.md:35`.

### F6 — historical note on the checker’s path assertion (no live defect)

At `953c278` the committed checker blob (`1bc2db10…`) had **no** `path_check` logic
(`grep -c path_check` on that blob → 0; its receipts carry no `path_check` key) and
reproduced 13/13. During the 03:39–03:40 repair window a path-checking checker was
paired with the still-13-case matrix, and
`lane-relative-parent-internal-control` failed `path_check=path-outside-internal`
(12/13) — the assertion and the frozen matrix were momentarily unsatisfiable
together. The landed repair reconciles them by declaring the escape instead of
suppressing it: the case now carries `"path_tolerance": "carve-out"` and the receipt
line reads `carve-out:path-outside-internal`
(`corpus/lessons/round-23.md:268`). At the pinned revisions this is consistent;
recorded only so the sequence is not mistaken for a regression.

## Sentences that can be read as source-availability / corpus-resolution claims

Line numbers: `corpus/lessons/round-23.md` at `5842ef7`; `SCORECARD.md`,
`LOG.md` at the same revision.

| # | location | sentence (excerpt) | reading risk | verdict |
|---|---|---|---|---|
| 1 | lesson:6-7 | “Neither claim restores a lost domain source. Score 4/7 remains held” | none — explicit disclaimer | safe, but ~170 lines from the registry census at #11 |
| 2 | lesson:22-23 | “The prior source losses and 23/25 legacy recheck failures remain known historical limits, not recovered or converted to passing by local copies.” | none | safe |
| 3 | lesson:62 | “Source-row transition: S018 `status: queued → mined`” | reads as source availability gained (`mined` = content acquired) | low: true, but no adjacent “not restored” qualifier |
| 4 | lesson:91 | “Landed in `corpus/instruments/resolve.py`:” | code landing | safe |
| 5 | lesson:105-113 | counting command | omits the export’s unpack path | **unsafe as a reproduction recipe** (F3) |
| 6 | lesson:118-124 | `0/6 → 6/6`, `7/7`, `7/13 → 13/13` under “same 13-case matrix, `5e61a33e…`” | reads as fresh detector evidence | superseded at `:259`; caption names the matrix, so acceptable under append-only, but the pointer is 135 lines away |
| 7 | lesson:132 | “still scores 0/6 on the target” | same | historical, same caveat as #6 |
| 8 | lesson:135-142 | guard numbers + “**The guard is vacuous on this host** … published as vacuity” | reads as reproducible no-harm evidence | **disclosure correct**; numbers path-dependent (F3), unbound to a resolver sha (F1c), 1589/1588 unreconciled (F4) |
| 9 | lesson:143-144 | “lane-relative `INTERNAL` branch remains unconfined by design (carve-out) … not generalized into ‘the detector is sound’” | none | safe, adjacent |
| 10 | lesson:146-147 | “Score held at **4**: instrument correctness only; no restored source, no citation availability change.” | none | safe, adjacent |
| 11 | lesson:161-164 | “`S018` exit 0 … `S029` exit 0 … `S030` exit 0” | reads as corpus recheck/resolution improvement (red→green) | scoped 51 lines later by “C2 evidence ceiling … proves quote-in-capture, not current online law or freshness” (`:212-214`); acceptable, scope non-adjacent |
| 12 | lesson:167-175 | “Admission rows: … F06→… F07→… F08→…” + “Frozen denominator `5/8 → 8/8`” | coverage claim; `5/8 → 8/8` could be misread as resolvability | safe as coverage (no source-availability wording) |
| 13 | lesson:176-177 | “Score held at **7**: the r15 domain-root denominator is untouched by public-practice entries.” | none | safe, adjacent |
| 14 | lesson:233-236 | “SOURCES: registry rows 27 → 30 (… status mined 18 …)” | reads as source inventory growth | low; superseded by the appended census correction (“31 rows … mined 19 … corrected here, not rewritten”), so corrected but non-adjacent |
| 15 | lesson:259-270 | “**Corrected C1 measurement** … Fixed: **24/24, exit 0**” | reads as detector/resolution improvement | safe: matrix-only, counts reproduced, sha-bound; no source-availability claim |
| 16 | `SCORECARD.md:403` | “**Improved, score held 4.** … `mirror=0` (published as vacuous). Score held: instrument correctness, no source restoration or citation-availability change” | — | disclosure + disclaimer adjacent: **correct in kind**; counts historical per #18 |
| 17 | `SCORECARD.md:404` | “**Improved, score held 7.** … the r15 domain-root denominator is untouched…” | “Improved” alone could read as availability | safe, adjacent qualifier |
| 18 | `SCORECARD.md:406-409` | “**No axis harmed.** depth:density was not touched this round…” | asserts the guard outcome without the density/anchorcheck report | **unsafe as written** (F2) |
| 19 | `SCORECARD.md:412-417` | “Exercised this round (13/13 and 7/13 receipts…)” | stale counter in the capability entry | **unsafe** (F1b) |
| 20 | `SCORECARD.md:433-440` | “**C1 measurement superseded** … 24 cases … 24/24, exit 0 … `resolver_sha256=690153ad…`” | — | safe: supersession + sha + no availability claim |
| 21 | `LOG.md:1125-1133` | counts + “`mirror=0` on this host makes that diff vacuous; published as vacuity” | — | **correct in kind** |
| 22 | `LOG.md:1134-1137` | “Counts: F06–F08 **0 → 3**, frontier **5/8 → 8/8**.” | coverage | safe |
| 23 | `LOG.md:1187-1189` | “Final matrix **24 cases** … fixed **24/24 exit 0** … do-nothing control **0/12 escape GONE**” | — | safe: sha-bound, reproduced |
| 24 | `corpus/README.md:195-202` | F06/F07/F08 status `admitted` | corpus-state change | coverage claim; no availability wording |

No filed sentence claims a *lost* source was restored or that corpus resolution
improved as a result of C1. The only unqualified “improved” tokens are
`SCORECARD.md:403/404`, each followed in-cell by a no-availability qualifier; the
guard’s own vacuity is disclosed everywhere it is counted.

## Negative results (checked, not defects)

- The matrix is non-vacuous (synthetic mirror present; controls report `mirror=1`),
  so `GONE` on escape cases is a real classification, not mirror absence.
- Receipt provenance: `resolver_sha256` matches the committed resolver blob at each
  revision (`bf9ce02`: `690153ad…` = blob; `f6966d4`: receipts and
  `lesson:262` both carry `dddd5549…`); `matrix_sha256` matches the committed
  fixture blob (`d05b1e0c…`); baseline resolver `d6a3c3f1…` matches
  `.ufo/waves/round-23/c1-baseline-resolver.py`.
- Both receipts reproduce exactly from committed blobs: 24/24 exit 0 and 12/24
  exit 1 (do-nothing control — the counter is not reachable without the fix).
- Class-only diff of the two frozen-corpus TSVs: `added=0 dropped=0 changed-class=0`
  (my first tuple diff reported 198 “changes” that are the `resolved_path` column
  only, expected when the export roots differ — a path column must not be diffed
  across differently-located exports).
- `before-instruments.json` `definition` says “git archive master export” while
  `revision` is `922a4dd`; `922a4dd` is an ancestor of every later HEAD and the
  recorded census reproduces exactly on that export, so the wording is loose, not
  false. Nothing in F1-F5 relies on it.

## Accidental writes and restoration (disclosed)

`resolve.py` writes `citation-survival.{md,tsv}` next to **its own file**. My first
two runs therefore wrote inside the repo: `.ufo/waves/round-23/citation-survival.{tsv,md}`
(created; deleted) and `corpus/instruments/citation-survival.{tsv,md}` (tracked;
restored with `git checkout --`, now the HEAD blobs). Every later run used copies
under `/tmp/kasegi-r23-falsify-VacuityDisclosure/{base,fix,cur,pinned,head3,head4,head5,head6}`.
At `5842ef7` `git status --porcelain corpus/instruments/` is clean, so nothing I
wrote survives in the lane. If the lane intended a regenerated working-tree census
before my run, that content was not recoverable; the files now equal HEAD.

## Reproduce

```sh
# pinned evidence set (bf9ce02 blobs)
h=/tmp/kasegi-r23-falsify-VacuityDisclosure/head6
for f in resolve.py mirror-containment-check.py mirror-containment-fixtures.json; do
  git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin cat-file blob bf9ce02:corpus/instruments/$f > $h/corpus/instruments/$f; done
cd $h && python3 corpus/instruments/mirror-containment-check.py --json receipt.json      # 24/24 exit 0
python3 corpus/instruments/mirror-containment-check.py \
  --resolver /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/c1-baseline-resolver.py \
  --json base24.json                                                                    # 12/24 exit 1

# F3/F4: same resolver, two unpack paths, plus the key census
export=/tmp/kasegi-r23-falsify-VacuityDisclosure
python3 $h/corpus/instruments/resolve.py $export/a            # internal=197 all=208/1589
python3 $h/corpus/instruments/resolve.py $export/cur/export   # internal=198 all=209/1589
python3 - <<'PY'  # over the last-written TSV
import csv, collections
rows=list(csv.reader(open("corpus/instruments/citation-survival.tsv", newline=""), delimiter="\t"))[1:]
c=collections.Counter(r[0] for r in rows if r)
print(len(rows), len(c), [(k,n) for k,n in c.items() if n>1])   # 1589 1588 [('evidence-manifest/v1', 2)]
PY
```

(The `922a4dd` export is `git -C …/kasegi-shokunin archive 922a4dd | tar -x -C $export/a`,
copied to `$export/cur/export` for the depth-3 case.)

## Scope limits

- Judged C1 disclosure, count integrity and the availability-wording inventory only.
  I did not evaluate F06–F08 entry content, registry row fields, snapshot quote
  fidelity, or C2 denominators (C2 seats own those).
- I did not judge, admit, score, edit production files, integrate, or run the wave
  registry; no claim of admission or score movement.
- The lane advanced through 8 commits while this seat ran. Findings are pinned to
  blob shas; `F1b, F2, F3, F4, F5` were re-checked at `f6966d4` and `5842ef7`. If
  HEAD advances again, re-derive rather than citing these line numbers.
- Reproductions used `/tmp` only (scratch trees under
  `/tmp/kasegi-r23-falsify-VacuityDisclosure`); no package installs, no host
  configuration, no network.
