# lesson-gate-skeleton — the `corpus/lessons/round-77.md` skeleton (WAVE-DIR DRAFT)

Seat: ScribeSources (round 77, attempt 1, wave `w1`). This is a DRAFT for the L1 `KasegiR77`, which is the sole
integrator. Nothing in the lane tree was edited to produce it; the L1 applies the landing surfaces. Every
factual line below carries its `path:line` or its command output; the receipts live in
`.ufo/waves/round-77/w1/ScribeSources.verification-r77.txt` and
`.ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt`.

Shape reference: `corpus/lessons/round-76.md` (Gate at `:5-15`, Counters at `:17-23`, Mistakes at `:25-33`,
Routed defects at `:35-41`) and `corpus/lessons/round-76-verifier-spotcheck.md` (fix list V-A..V-E at §6).

---

## Proposed header (L1 to finalise; the dead-seat count is the L1's to fill)

```markdown
# Round 77 — lesson (kasegi, attempt 1)

Frozen claims: `.ufo/waves/round-77/claims.json` (freeze `539a43877809bd90b6f506e8fd24a6d871598cd5`,
base `2e53fc74776824898b5c5eb914aeddc19a091157`). Wave `w1` — one v1 wave of 13 seats, attack 5/13
(reviewer×2, critic, mutation-tester, sentinel) — and its receipts under `.ufo/waves/round-77/w1/` and
`.ufo/waves/round-77/controls/`. Verdicts: **C1 <VERIFIED|NOT VERIFIED as declared>**,
**C2 <VERIFIED|NOT VERIFIED as declared>**. <Admission sentence, L1's wording.>

## Gate
```

Notes for the L1 on the header:
- `13 seats` is the item count of `.ufo/waves/round-77/w1-spec.json` (`len(items)` = 13; seats 1..13 =
  ExecC1Verify, ExecC2Counters, ExecReplay, ScoutSurface, ScribeEntry, ScribeSources, ConnectorOverlap,
  ReviewC1, ReviewC2, CriticClaims, MutC1, SentinelC1, RevengerInherited).
- `attack 5/13` = ReviewC1, ReviewC2, CriticClaims, MutC1, SentinelC1 (the seat spec's own count; the
  `RevengerInherited` seat is an inherited-state attacker, not one of the five attack seats of the spec).
- **Dead-seat count: TO BE FILLED BY THE L1.** This seat cannot state it: at the time of writing the wave
  dir holds some seat reports and not others (`ls -la .ufo/waves/round-77/w1/`, 2026-11-05T12:46Z —
  `RevengerInherited.md` is a 12-byte file containing only `PLACEHOLDER`, and several seats have filed
  nothing). The L1 fills the count from the wave's own dispatch results after WAKE-DONE.

---

## Proposed `## Gate` block

```markdown
## Gate

- candidates considered: **F54 — the OSV.dev project's `POST /v1/querybatch` contract**, its own reference
  page `https://google.github.io/osv.dev/post-v1-querybatch/`, opened 2026-11-05 (capture fetched
  2026-11-05T12:22:10Z by `corpus/instruments/capture-source.py`, sha256
  `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907`, 216 lines, 4575 snapshot bytes; the
  raw page is 30406 bytes, the same byte count the round-77 morning probe printed —
  `corpus/source-snapshots/round-77/S112.txt`). Located quote (15 words, ≤25):
  "Query for multiple packages (by either package and version or git commit hash) at once." at
  **S112.txt:24**; the same line also carries "Returns vulnerability ids and modified field only." (7 words)
  and "The response ordering will be guaranteed to match the input." (10 words). Thirteen pinned quotes
  Q01-Q13 are anchored at S112.txt lines 24, 24, 24, 30, 31, 34, 35, 36, 166, 168, 169, 170, 195
  (`corpus/source-snapshots/round-77/manifest.json`); the R126 pre-freeze dry run and the independent re-run
  both print `S112:sha256 OK` and 13 `OK occurrences=1 anchor=<n>-ok` lines, rc 0
  (`.ufo/waves/round-77/controls/c2-prerecheck-r77.txt`; re-run receipt
  `.ufo/waves/round-77/w1/ScribeSources.verification-r77.txt` §5). Candidate C1: the recheck-cwd census
  counter amendment (`corpus/instruments/recheck-cwd-census.py`, base bytes sha256
  `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`).

- the four sibling OSV.dev endpoint pages — `GET /v1/vulns/{id}`, `POST /v1experimental/determineversion`,
  `GET /v1experimental/importfindings`, `POST /v1experimental/ubuntu/binary-to-source` — were screened as
  leads and are listed as candidates considered, not as admissions (receipts below).

- new rows written this round: **S112** — `queued` at the freeze (`corpus/SOURCES.md:124`, `used-by —`),
  flipped to `mined` only at the landing. URL `https://google.github.io/osv.dev/post-v1-querybatch/`;
  accessed 2026-11-05 (capture `fetched_utc` 2026-11-05T12:22:10Z); anchor
  `corpus/source-snapshots/round-77/S112.txt` lines 24-36 and 166-195. Located quote (15 words, ≤25):
  "Query for multiple packages (by either package and version or git commit hash) at once." (S112.txt:24).
  Registry rows 111 → 112. The row's `teaches` names only the batch-contract clauses; the single-query
  contract stays with S108 (F51), the record format with S080 (F31) and the overview page with S111.

- admitted: **F54**, the `POST /v1/querybatch` batch contract, pending L1 landing — the knowledge entry
  `corpus/knowledge/osv-post-v1-querybatch-contract.md` is drafted in the wave dir
  (`.ufo/waves/round-77/w1/entry-osv-post-v1-querybatch-contract.md`), not in `corpus/`, until its B-predicates
  are measured at the landing tree. Ground claimed: the queries-array payload, the ids-and-modified-only
  return shape, the input-matched ordering guarantee, the parameters-same-as-`POST /v1/query` sentence,
  the per-item version rules with the 400 Bad Request consequence, and the per-query pagination semantics
  (per-result `next_page_token`, the 1,000/3,000 thresholds, the threading-variance note, the
  follow-up-request rule).

- rejected rows: none this round.

- reject line (R119 distinctness, C2 B6): `rejected as new ground: the endpoint path string
  POST /v1/querybatch and the api.osv.dev host form` — already held as listed-not-described from
  `corpus/source-snapshots/round-73/S108.txt:5-9` (F51 `corpus/knowledge/osv-post-v1-query-contract.md:75`)
  and from `corpus/source-snapshots/round-76/S111.txt:5,43`. Flip: a successor that DESCRIBES an endpoint's own
  payload, version rules or pagination semantics — rather than listing its path — with its own capture and its
  own distinctness sweep (this round's C2 is exactly such a successor for one endpoint: the batch one).

- reject line (leads, not adopted): `GET /v1/vulns/{id}`, `POST /v1experimental/determineversion`,
  `GET /v1experimental/importfindings`, `POST /v1experimental/ubuntu/binary-to-source` — the four sibling
  endpoint pages named by the S111 navigation (S111.txt:4-9). They were probed read-only on 2026-11-05 at
  the live navigation slugs and all four answer **HTTP 200** —
  `get-v1-vulns/` 19961 B, `post-v1-determineversion/` 30242 B, `get-v1-importfindings/` 16418 B,
  `post-v1-ubuntu-binary-to-source/` 18769 B — so they are NOT dead ends and NOT rejected for
  unavailability; the round-77 morning 404s (`11373 B`) came from wrong-slug shapes
  (`get-v1-vulns-id`, `get-v1experimental-importfindings`, `post-v1experimental-determineversion`,
  `post-v1experimental-ubuntu-binary-to-source`, all 404) (receipt
  `.ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt`). They are not adopted this round: one
  admission per round per lane practice, and each needs its own capture, its own located quotes and its own
  distinctness sweep. Flip: a successor round captures one of the four (its own capture, its own manifest
  record, its own R114+R125 sweep) and admits it as the next F-number. **L1: the wording of this reject line
  should not assert a 404 for the four pages — the measured receipts are 200 for the live slugs.**

- reject line (S111 carried, still not admitted): the OSV.dev API overview page stays **queued, not
  admitted** — its round-76 reasons carry unchanged. B5 failed on the frozen round-76 manifest
  (`S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`, rc 2; the frozen quote
  "API (1.0)" normalizes to 9 characters against the instrument's own floor `MIN_QUOTE_CHARS = 12` at
  `corpus/instruments/source-recheck.py:33`) and B6 failed on distinctness (the endpoint path strings were
  already held). The r76 verdict stands; this round neither repaired that manifest in place nor admitted
  S111, and the fresh round-77 manifest (`corpus/source-snapshots/round-77/manifest.json`) does not touch
  S111. Flip: a successor freezes a NEW manifest whose quotes all pass `source-recheck.py` before the freeze
  (QUALITY R126) and runs the R114 subject sweep plus the R125 admitted-entry sweep over the overview's own
  ground before writing its predicate.

- considerthese: none fits — the connector's own disposition: no file after `considerthese/2026-10-26.md`
  (last commit `e86afb8`) and none of the seven 2026-10-26 proposals fits either frozen claim
  (`.ufo/waves/round-77/w1/ConnectorOverlap.md` §2, §2c). The lane's own ledger
  (`corpus/knowledge/considerthese-proposals-ledger.md`) has no matching section for round 74, 75 or 76
  (`ConnectorOverlap.md` §2 F-CT4) — a ledger gap this round does not close.

- assimilation: **none this round** — the connector's recount: 112 registry ids, 94 staged ids, **82
  collisions** (`reg ∩ staged == collisions`, 82 == 82), range S031-S112
  (`.ufo/waves/round-77/w1/ConnectorOverlap.collisions.txt`, `.reg-ids.txt`, `.staged-ids.txt`;
  `ConnectorOverlap.md` §1). The staged package `merge/kasegi/SOURCES.append.md` spans **S031-S124**, not
  S001-S094: its `S111` (`:87`, an NCSC weekly report) and its `S112` (`:88`, a TC260 route record) are
  DIFFERENT documents from this lane's own S111 (`:123`, landed round 76) and S112 (`:124`, landed at the
  round-77 freeze). Nothing is appended; the package stays L0-routed (the round-76 R-D item persists, now
  for two ids).

- spot-check: pending the non-author closure. Attack verdicts are recorded in `.ufo/waves/round-77/w1/`
  (CriticClaims, ReviewC1, ReviewC2, MutC1, SentinelC1, RevengerInherited).

- sourced claim (frontier step): C2 rests on S112 — its statement, its predicates B0-B7 and its receipts
  cite the row, and its draft entry's every load-bearing clause is anchored to a Q01-Q13 line in
  `corpus/source-snapshots/round-77/S112.txt`. C1 is instrument work with no source row.
```

---

## Draft `## Counters` rows (L1 to re-measure at the landing tree; these are the values observed at the
## freeze tree and at the base bytes, NOT at a landing tree)

| counter | command | rc | value |
|---|---|---|---|
| base census selftest (do-nothing control) | `python3 -B corpus/instruments/recheck-cwd-census.py --selftest` at base bytes `e666ae11…` | 0 | `selftest cases=6 failures=0` (receipt `controls/c1-donothing-selftest-r77.txt`) |
| base real-tree census (do-nothing control) | `TMPDIR=<scratch>/tmp python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` | 0 | `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` / `RECHECK-CWD-RESULT conformant` (receipt `controls/c1-base-realtree-census-r77.txt`) |
| r76 survivor, red-before | `python3 -B .ufo/waves/round-76/controls/m2b-conjunct-removed.py --selftest` | 0 | `selftest cases=8 failures=0` — the survivor still stands on the r76 design; re-run in scratch rc=0, same last line (`ScribeSources.verification-r77.txt` §2) |
| r77 reference candidate selftest | `python3 -B .ufo/waves/round-77/c1-amended-reference.py --selftest` | 0 | `selftest cases=12 failures=0` — re-run in scratch rc=0 (`ScribeSources.verification-r77.txt` §3) |
| five named mutants (K-M1..K-M5) | `python3 -B .ufo/waves/round-77/controls/m{1..5}-*.py --selftest` | 1 / 1 / 1 / 1 / 1 | `cases=12 failures=3` / `cases=12 failures=1` (gate-negpolarity FAIL neg_ok=True — the required m2b-class assertion kill) / `cases=12 failures=2` (gate-consume FAIL exception=NameError — the exception class, R127) / `cases=12 failures=1` (gate-negpolarity FAIL neg_ok=False) / `cases=11 failures=1` (gate-checkids FAIL missing=['both-headers']); re-run in scratch, all five rc=1 (`ScribeSources.verification-r77.txt` §4) |
| B0 / R126 pre-freeze dry run | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` | 0 | `S112:sha256 OK` + 13 `OK occurrences=1 anchor=<n>-ok` (receipt `controls/c2-prerecheck-r77.txt`; independent re-run §5) |
| capture binding (freeze tree) | `python3 corpus/instruments/capture-binding-check.py` | 0 | `records=91 bound=91 unbound=0` (the freeze commit carries capture, manifest and the S112 row together — the r76 M76-5 fix) |
| frontier counters (freeze tree) | `python3 corpus/instruments/frontier-recheck-count.py` | 0 | `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112` / `entries=56 pass=56 exit=0` — the F54 README/PROVINCE rows land with the entry; frozen B3 expects `rows=54 … registry=112` / `entries=57 pass=57` at the landing tree |
| sources census, round start | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | 0 | `kasegi ok …/corpus/SOURCES.md` with the six inherited W04 duplicate-url warnings (S028, S029, S072, S076, S080, S085) unchanged (receipt `controls/sources-census-start-r77.txt`) |
| registry rows, base → freeze | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 | base `2e53fc74` = 111; freeze tree = 112 (receipt `controls/c2-base-counters-r77.txt`) |

## Draft `## Mistakes` rows

See `.ufo/waves/round-77/w1/mistakes-draft.md` for the candidate rows this seat mined from the inherited
round-76 verdict; each is marked **pending L1 confirmation** and the L1 decides which are this round's own.

## Draft `## Routed defects` rows

The L1's own routed-defect list (M77-1..M77-4 as already drafted in the L1's working-tree lesson) stands; this
seat contributes one prose-level candidate and one registry-prose candidate:

- **R-77-D (registry prose for a frozen-queued row):** the `## Registry changes` and `## Search log`
  sections of `corpus/SOURCES.md` carry no round-76 bullet for the S111 row and no round-76 search-log entry
  (`grep -n "Round-76\|round-76" corpus/SOURCES.md` → one hit only, the S111 row's own capture path at
  `corpus/SOURCES.md:123`; the round-75 bullet is the last `## Registry changes` bullet at
  `corpus/SOURCES.md:273`). A row that lands queued still needs its registry-changes prose, otherwise the
  next reader cannot see when S111 was written, at what status and why it was not used.
  Fix: the round-77 bullets below record the S112 row; a successor may append the missing round-76 S111
  bullet as its own statement (R8 form — an appended statement, never an edit of the r76 record).

- **R-77-E (reject-line wording must match the measured receipt):** a reject line that cites a 404 for a URL
  shape that answers 200 is a stale premise under R19. The four lead pages are live; the round-77 morning
  404s were wrong-slug shapes. The wording in the Gate block above is written to the measured receipts.
