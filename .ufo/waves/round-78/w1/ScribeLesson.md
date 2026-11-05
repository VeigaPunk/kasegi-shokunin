# ScribeLesson — round 78, attempt 1, wave w1 (kasegi)

Seat: ScribeLesson (scribe). Drafting seat: no lane tree file was edited, no git/jj write was run, no
delegation, no background job, no tool installed, no host sysctl touched. The scratch root
`/fast/scratch/hyaku/kasegi-r78/ScribeLesson` was used for every measurement that wrote bytes and was
deleted before this yield.

## What I wrote (wave output dir only)

1. `.ufo/waves/round-78/w1/lesson-round-78.md` — the round-78 lesson draft for the L1 to land, in the
   sections the seat spec names: `## Gate` (C1 and C2 with their frozen predicates referenced to
   `.ufo/waves/round-78/claims.json` at freeze `2d81fe84`; the S112 access record — URL, access date
   2026-11-05, HTTP 200, and the live re-fetch note that all seven quotes are present after tag-boundary
   whitespace normalization; the S112 status change `queued` -> `mined` logged old -> new; the staged-package
   collision note — S112/TC260 collides with the staged shokuknow package, routed to L0, nothing adopted),
   `## Mistakes` (exactly one mined entry, M77-3, class `environment-assumption`, captured-by none, fix =
   the C1 successor's TMPDIR refusal, with the red-before pair named), `## Sources` (the S112 row before and
   after, the seven clauses admitted, the not-claimed clauses with their reasons),
   `## Learning` (expansion, quality, discernment — one line each), `## Routed` (R-77-D, R-77-E, R-77-F).
   Plus a `## L1 open items` section for the one finding this seat measured, and a `## Seats` line.
2. `.ufo/waves/round-78/w1/scorecard-round-78.md` — the `SCORECARD.md` round-78 section draft: the axis
   table with before/after per claim, the counting command per claim (C1's four commands and the eight-mutant
   kill loop; C2's nine commands), the registry change old -> new, the claim-verdict cells left for the L1 to
   fill, the move log, and the planned-after list. The measured commit is the literal token `LANDING_HASH`,
   for the L1 to replace with the landing commit.
3. `.ufo/waves/round-78/w1/ScribeLesson-evidence-r78.txt` — the measurement receipt behind every number in
   (1) and (2): freeze bytes read, the seven-quote source check, the B6 quote-absence sweep, the F51
   paraphrase sweep, the live re-fetch and the normalization detail, the base red-before, the candidate
   measurements, the K-X2 analysis, and the P6 pin rows.

## The finding that matters for the L1: K-X2 survives on the current build candidate

On the build candidate bytes (`.ufo/waves/round-78/w1/successor/recheck-cwd-census.py`, sha256
`f68499715f38b6e74f368c441766954a240d7f5036d68157110e5017c8457db1`) the named-kill set measures **7 of 8**,
not 8 of 8:

| mutant | rc | summary | kill class |
|---|---:|---|---|
| K-M1 | 1 | `cases=13 failures=3` (`gate-regs FAIL`, `gate-consume FAIL no-registration`, `gate-negpolarity FAIL no-registration`) | assertion |
| K-M2 | 1 | `cases=13 failures=1` (`gate-negpolarity FAIL neg_ok=True`) | assertion (required) |
| K-M3 | 1 | `cases=13 failures=2` (`gate-consume FAIL exception=NameError`, `not-evaluated-after-exception`) | exception class |
| K-M4 | 1 | `cases=13 failures=1` (`gate-negpolarity FAIL neg_ok=False`) | assertion |
| K-M5 | 1 | `cases=12 failures=1` (`gate-checkids FAIL missing=['both-headers']`) | assertion |
| K-X1 | 1 | `cases=13 failures=1` | assertion (required) |
| **K-X2** | **0** | **`cases=13 failures=0`** | **survivor** |
| K-M8 | 1 | `cases=13 failures=1` | assertion (required) |

Two independent grounds, both measured by this seat:

- The frozen table's K-X2 anchor is `check("gate-consume", clean_ok is True, "clean_ok=%r" % (clean_ok,))`
  (the r77 reference's line). That exact string does **not** occur in the candidate bytes — the candidate
  reads `check("gate-consume", clean_ok is True and limb_log == [True], ...)`. Per the frozen kill rule, a
  mutant that cannot be derived by its anchored transform from the landing bytes is NOT DERIVED and counts
  as NOT VERIFIED.
- Under the natural adaptation of the transform (replace `clean_ok is True` with `True` — what the build seat
  did) the mutant still survives. I derived both readings by hand from the candidate bytes, one anchored
  text transform each, and re-ran them: the table reading exits 0 with `cases=13 failures=0`, and so does a
  whole-body neutering of the `gate-consume` check.

The cause is structural, and it is the same position as the round-77 X2 survivor that made the round-77
closure reject C1: the candidate's only assertion on the case-6 RESULT limb is the `gate-consume` check
itself. The sibling `gate-negpolarity` check reads `limb(out2c, ret2c)` — the case-2c limb, not case 6 — so
neutering `gate-consume` leaves nothing that fails on the case-6 value. K-X1 dies only because the same
check also asserts `limb_log == [True]`, and that conjunct sits inside the very check K-X2 neuters.

Consequence for the L1: on these bytes C1's P3 and its kill rule are not met. Either land a successor in
which the `gate-consume` body is itself asserted by a second, independent check (so neutering it still fails
on the case-6 limb), or record C1 as NOT VERIFIED. The red-before for that successor is the K-X2 receipt
above. The other C1 predicates measure true on the candidate: selftest `cases=13 failures=0` rc 0 (P1);
real-tree census `entries=91 … restoration_only=0` conformant rc 0 (P2); the TMPDIR refusal rc 2 with
`recheck-cwd: TMPDIR <path> is not a directory`, stdout empty, no traceback, for both a nonexistent path and
an existing non-directory path (P4); one `subprocess.run` call site and one `bash -c` pair (P7). P6's two
pin rows are `SKILL.md:982` and `corpus/instruments/README.md:354` (`selftest cases=6` -> `cases=13`).

## C2 — what measured true

The seven frozen quotes are all located and all distinct. `python3 corpus/instruments/source-recheck.py
--manifest corpus/source-snapshots/round-78/manifest.json --source S112` prints `S112:sha256 OK` and seven
`OK occurrences=1 anchor=<n>-ok` lines, rc 0 — the same bytes as the committed pre-freeze control. The
snapshot hash is `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907`, byte-identical to the
round-77 capture. Each of the seven quotes sits on its declared snapshot line exactly (24, 24, 24, 166, 168,
169, 195), so the r78 manifest does not depend on the anchor window (R-77-D stays a question about the
instrument, not about this manifest). The B6 quote-absence sweep returns zero files for all seven quotes
over the 91 admitted entries, and the paraphrase sweep against F51 finds `querybatch` only in F51's
not-claimed navigation bullet (`:75`) with the version rule (`:21`) and the pagination substance (`:47`)
held there — so 7 of 7 clauses are distinct. The live re-fetch returns HTTP 200 and 30406 raw bytes, and
all seven quotes occur exactly once after the instrument's own `html_to_text` normalization; one detail
worth keeping: replacing tags with a space instead of removing them breaks Q13, because the live page wraps
`page_token` in `<code>` tags.

Census before the landing: `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112`,
knowledge 91, `knowledge-expected.txt` 93 lines / 91 `.md` rows, registry 112, `capture-binding-check.py`
`records=92 bound=92 unbound=0` rc 0, `sources-census.sh validate` rc 0 with the six inherited W04
duplicate-url warnings and no new finding.

## Collision and routed items

The staged shokuknow package `merge/kasegi/SOURCES.append.md:88` names its own `S112` as the TC260
suggestion route — a different document from this lane's OSV.dev row. The staged package spans S031–S124
(94 rows); 82 of its ids collide with this lane's 112-row registry. Nothing is appended; the collision
stays with the L0 question at `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:353`. R-77-D, R-77-E and
R-77-F are carried into the lesson's `## Routed` with their status (the first two L0-pending, the third
still open with three live endpoint pages remaining).

## One discrepancy between the seat brief and the frozen bytes (reported, not silently resolved)

The seat brief's `## Sources` line asks for "the four not claimed with reason". The frozen C2 statement
and the r78 manifest name **six** not-claimed clauses — Q04, Q05, Q06, Q07, Q08 and Q12 — in two reason
classes (three cross-references into the single-query contract, three restatements of admitted F51); 13
minus 7 is 6. Repo files beat the brief, so the lesson states six and gives each class its reason. If the
L1 wants the brief's "four", the two extra clauses to reconcile are Q04 and Q05 (the parameters and
pagination-instructions pointers), which the round-78 manifest drops along with Q06.

## Tooling

Nothing installed or upgraded; no pacman transaction; no sysctl change. Commands used: read-only `git`
(`log`, `show`, `ls-files`, `cat-file -t`), one read-only `curl` GET of the S112 URL, `python3 -B`,
`sha256sum`, `wc`, `ls`, `grep`, `find`, `sed -n` for line display.
