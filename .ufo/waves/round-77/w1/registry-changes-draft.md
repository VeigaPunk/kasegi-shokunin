# registry-changes-draft — the `corpus/SOURCES.md` prose for round 77 (WAVE-DIR DRAFT)

Seat: ScribeSources (round 77, attempt 1, wave `w1`). Draft only: the L1 `KasegiR77` applies and lands
these in `corpus/SOURCES.md`. No lane file was edited by this seat.

Target file: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` (273 lines at the freeze tree;
`## Registry` at :3, `## Paths` at :126, `## Search log` at :135, `## Leads (unopened)` at :174,
`## Registry changes` at :179). Round-77 anchors: the S112 registry row is at `corpus/SOURCES.md:124`;
the S111 row is at `corpus/SOURCES.md:123`; the last existing `## Registry changes` bullet is the round-75
one at `corpus/SOURCES.md:273`.

R8 form is followed throughout: an old → new cell transition is recorded as prose in this section; no
existing row cell is edited in place, and every other row is untouched.

---

## (A) `## Registry changes` — appended bullet(s), to land at the END of the section (after
## `corpus/SOURCES.md:273`, per R6 append-at-the-end)

```markdown
- Round-77 S112 added (docs, scoped tier A, mined, opened 2026-11-05, recheck 180d, used-by
  corpus/knowledge/osv-post-v1-querybatch-contract.md). Registry 111 -> 112; no pre-existing status,
  recheck, used-by, id or URL cell changed. S112 is the OSV.dev project's own reference for one batch query
  endpoint, POST /v1/querybatch, anchored to the round-77 capture
  corpus/source-snapshots/round-77/S112.txt (sha256
  f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907, 216 lines, 4575 snapshot bytes over
  30406 raw bytes, fetched 2026-11-05T12:22:10Z; 13 pinned quotes Q01-Q13 at anchors L24/L24/L24/L30/L31/
  L34/L35/L36/L166/L168/L169/L170/L195 in corpus/source-snapshots/round-77/manifest.json, all located
  rc=0 before the freeze, receipt .ufo/waves/round-77/controls/c2-prerecheck-r77.txt). Frontier F54 is
  admitted in corpus/README.md; knowledge 91 -> 92. The row's own scope cell names what it does NOT hold:
  not the single-query POST /v1/query contract (S108, F51), not the OSV record format (S080, F31), not the
  API overview page (S111), not any other endpoint's page, and not any live query or rate-limit statement
  (the page states none). The one-row insert moves every line below S112 down by one.
- Round-77 S112 cell flips at the landing (old -> new): status `queued` -> `mined`; used-by `—` ->
  corpus/knowledge/osv-post-v1-querybatch-contract.md. The row was written `queued` at the freeze commit
  539a43877809bd90b6f506e8fd24a6d871598cd5 (corpus/SOURCES.md:124) and flips only when the entry lands; no
  other cell of the row changes, and no pre-existing row cell changes (R8).
- Round-77 capture/row binding: the freeze commit carries corpus/source-snapshots/round-77/S112.txt,
  corpus/source-snapshots/round-77/manifest.json and the S112 registry row in ONE commit, so
  corpus/instruments/capture-binding-check.py reads `records=91 bound=91 unbound=0` with no
  `FAIL rule=no-row` — the round-76 M76-5 fix (stage the capture with its row).
```

### (A.1) The id-collision fact the L1 must record for S112 (read from the staged package, read-only)

The staged campaign package `merge/kasegi/SOURCES.append.md` stages **94 ids spanning S031-S124**
(`grep -oE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]{3}' |
sort -u | wc -l` = 94; first S031, last S124). **`S112` is one of them** — a DIFFERENT document: TC260's own
suggestion route and the standards platform's project record (`merge/kasegi/SOURCES.append.md:88`). The
round-77 connector seat's own recount agrees: 112 registry ids, 94 staged ids, 82 collisions
(`.ufo/waves/round-77/w1/ConnectorOverlap.reg-ids.txt`, `.staged-ids.txt`, `.collisions.txt`;
`reg ∩ staged == collisions` verified: 82 == 82, with S111 and S112 both in the collision list;
`ConnectorOverlap.md` §1 table: "collisions | 82 | range S031 … S112", "staged S112 present? | yes |
`merge/kasegi/SOURCES.append.md:88`").

The connector's own §1 finding is the same one this seat reached independently: "the spec premise 'the new
S112 is outside S001-S094 so it adds none' is false. The staged package spans S031-S124." The round-76 R-D
item therefore persists for TWO ids now.

This is the SAME defect class the round-76 lesson routed as R-D (the staged `S111` id collided with this
lane's own round-76 S111 row; `merge/kasegi/SOURCES.append.md:87` is a CN-CERT weekly-report row). The
recurrence is a routed defect for the L1 and the L0 question file, not a blocker for this round's admission:
the lane's own ids are authoritative inside `corpus/SOURCES.md`, and the staged package is not adopted by
this round. Suggested bullet for the L1 to append (or to route to `.ufo/l0-questions.md` beside the
round-76 S111 collision):

```markdown
- Round-77 id collision (routed, not adopted): the staged merge/kasegi/SOURCES.append.md stages 94 ids
  spanning S031-S124, and its S112 is a DIFFERENT document from this lane's S112 (a TC260 route record,
  merge/kasegi/SOURCES.append.md:88). The round-77 connector recount gives reg-ids 112, staged-ids 94,
  collisions 82 (.ufo/waves/round-77/w1/ConnectorOverlap.collisions.txt; reg ∩ staged == collisions, 82
  == 82; .ufo/waves/round-77/w1/ConnectorOverlap.md §1). The round-76 S111 collision (staged S111 = a
  CN-CERT weekly report, merge/kasegi/SOURCES.append.md:87) is therefore the second of at least two ids in
  the S111-S112 band that collide with this lane's own rows. Adopt nothing from the package this round;
  the collision is routed to the L0 question file, which already carries the round-76 S111 collision.
```

### (A.2) The registry-prose gap this round inherits (a finding for the L1, not an edit by this seat)

`corpus/SOURCES.md` carries **no `## Registry changes` bullet and no `## Search log` entry for round 76**:
`grep -n 'Round-76\|round-76' corpus/SOURCES.md` prints exactly one hit — the S111 row's own capture path
at `corpus/SOURCES.md:123` — and the last `## Registry changes` bullet is the round-75 one at
`corpus/SOURCES.md:273`. Every earlier round that wrote a row wrote its bullet (round-73 at :271, round-74
at :272, round-75 at :273). The round-76 row therefore landed with no record of when it was written, at
what status or why it is unused; QUALITY R8 asks for the old -> new status/recheck/used-by change to be
logged, and the lane's own convention logs a row addition. Suggested handling: the round-77 bullet above
records S112; the round-76 S111 bullet may be appended by the L1 as its own statement (R8 form — appended
prose, never an edit of the round-76 record) or routed to the next round. This seat does not write it.

---

## (B) `## Leads (unopened)` — appended bullet, to land at the END of the section (after
## `corpus/SOURCES.md:177`, per R6 append-at-the-end)

```markdown
- The four remaining OSV.dev endpoint reference pages, named by the S111 navigation (S111.txt:4-9) but not
  captured and not rows: GET /v1/vulns/{id} at https://google.github.io/osv.dev/get-v1-vulns/ (HTTP 200,
  19961 bytes), POST /v1experimental/determineversion at .../post-v1-determineversion/ (HTTP 200, 30242
  bytes), GET /v1experimental/importfindings at .../get-v1-importfindings/ (HTTP 200, 16418 bytes) and
  POST /v1experimental/ubuntu/binary-to-source at .../post-v1-ubuntu-binary-to-source/ (HTTP 200, 18769
  bytes) — probed read-only on 2026-11-05T12:40:45Z, no capture into the corpus, receipts
  .ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt. The round-77 morning 404s (11373 bytes each)
  were wrong-slug shapes, not dead pages: get-v1-vulns-id, get-v1experimental-importfindings,
  post-v1experimental-determineversion and post-v1experimental-ubuntu-binary-to-source all answer 404,
  while the four navigation slugs above answer 200. Unopened leads, no rows, no evidence; a successor
  round captures one of them under the instrument UA, with its own located quotes and its own R114 subject
  sweep plus R125 admitted-entry sweep, and admits it as the next Frontier row. The OSV.dev API overview
  page stays queued-not-admitted with its round-76 B5/B6 reasons carried (see the round-77 lesson's Gate
  reject line for S111).
```

---

## (C) `## Search log` — appended bullet, to land at the END of the section (after
## `corpus/SOURCES.md:172`, per R6 append-at-the-end)

```markdown
- Round-77 bounded OSV endpoint-contract screen, 2026-11-05: question — which of the five non-query OSV.dev
  endpoint contracts is the strongest distinct F54 ground, and is it distinct from the ground already
  held from S080 (record format, F31), S108 (POST /v1/query contract, F51) and the queued S111 overview
  page? Where — the google.github.io/osv.dev slugs probed read-only on 2026-11-05 (the four sibling
  endpoint pages at the S111 navigation slugs and the batch page at post-v1-querybatch/), the lane's own
  registry and knowledge sweep for the OSV subject (S080, S108/F51, S111 rows at corpus/SOURCES.md:71,
  :122, :123; F51's own Limits bullet at corpus/knowledge/osv-post-v1-query-contract.md:75 naming the
  other endpoints as "listed, not described"), and the lane's own capture bytes for the subject sweep
  (corpus/source-snapshots/round-73/S108.txt:5-9 and corpus/source-snapshots/round-76/S111.txt:4-9,43).
  Identified 5, screened 5, included 1 (POST /v1/querybatch, admitted as F54 on the new row S112),
  excluded 4 (GET /v1/vulns/{id}, POST /v1experimental/determineversion,
  GET /v1experimental/importfindings, POST /v1experimental/ubuntu/binary-to-source) — all four answer HTTP
  200 at their navigation slugs (19961 / 30242 / 16418 / 18769 bytes, 2026-11-05T12:40:45Z, receipts
  .ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt), so they are excluded as NOT ADOPTED this
  round rather than as unavailable; the round-77 morning 404s (11373 bytes) were wrong-slug shapes, and
  the four pages remain unopened leads with their flip conditions. Stop rationale: one admission per round
  per lane practice, and each remaining endpoint needs its own capture, its own located quotes and its own
  distinctness sweep before it can be admitted.
```

### (C.1) Why the search-log entry says "screened 5", not "screened 1"

The five candidates are the five non-record OSV.dev endpoint contracts: `POST /v1/query` (held from S108 /
F51), `POST /v1/querybatch` (this round's admission), `GET /v1/vulns/{id}`, `GET
/v1experimental/importfindings`, `POST /v1experimental/determineversion` and
`POST /v1experimental/ubuntu/binary-to-source`. `POST /v1/query` is listed in the search-log bullet as
already held (S108, F51) rather than re-screened, so the bullet's "identified 5, screened 5" counts the
five candidates of THIS round's screen (querybatch plus the four siblings). The L1 may prefer to state
"identified 5, screened 1, included 1, excluded 4" — the difference is bookkeeping about whether the
already-held `POST /v1/query` is inside the five. **The seat's own brief states the count as "identified 5,
included 1 (querybatch), excluded 4"; the draft above follows that, with `screened 5` matching the number
of pages actually probed.** Either wording is defensible as long as it is one of them and the four excluded
pages carry their receipts.

---

## (D) Cell-shape notes for the L1 (the S112 row's own cells, from the frozen row)

The frozen S112 row (`corpus/SOURCES.md:124`, pipe-split into 12 fields) reads:
`S112` | `OSV.dev API reference, POST /v1/querybatch (OSV project) — https://google.github.io/osv.dev/post-v1-querybatch/`
| `docs` | `A` | the scope cell (batch-contract clauses; the four "not …" exclusions) | the anchor cell
(lines 24-36 and 166-195; capture sha256; 216 lines; 4575 bytes; fetched 2026-11-05T12:22:10Z; 13 pinned
quotes; per-clause line numbers) | the headline cell | `queued` | `2026-11-05` | `180d` | `—`.

At the landing, two cells flip (status, used-by) and the other ten stay byte-identical (R8). The `teaches`
cell's exclusions are already the distinctness statement: the entry may not claim the single-query contract
(S108/F51), the record format (S080/F31), the overview page (S111), another endpoint's page, or any live
query or rate-limit statement.

### (D.1) A wording point the L1 should check before the flip

The S112 row's scope cell says the page holds "not any live query or rate-limit statement (the page states
none)". Verified against the capture: `corpus/source-snapshots/round-77/S112.txt` carries no rate-limit or
quota sentence (the rate-limit answer is held from S111/S111.txt:35-36), and the S112 page's own response
clause is the batch pagination rule, not a size or rate limit. No cell change is required — this is a note,
not a defect.
