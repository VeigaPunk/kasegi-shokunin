# ScribeSources — round 77, attempt 1, wave `w1`

Seat: ScribeSources (scribe; leaf, no delegation). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze `539a43877809bd90b6f506e8fd24a6d871598cd5`; base `2e53fc74776824898b5c5eb914aeddc19a091157`.
Milestone: round-77 attempt 1 — C1 recheck-cwd RESULT-limb gate (12 checks, 5 mutant kills) and C2 F54 OSV
querybatch admission on S112.

**Writes made by this seat (all under the wave report dir; no lane tree file was edited, no git/jj mutation
of any kind):**

| artifact | path |
|---|---|
| this report | `.ufo/waves/round-77/w1/ScribeSources.md` |
| draft 1 — lesson Gate skeleton | `.ufo/waves/round-77/w1/lesson-gate-skeleton.md` |
| draft 2 — SOURCES.md registry / leads / search-log prose | `.ufo/waves/round-77/w1/registry-changes-draft.md` |
| draft 3 — `## Mistakes` candidate rows | `.ufo/waves/round-77/w1/mistakes-draft.md` |
| evidence — independent re-measurements | `.ufo/waves/round-77/w1/ScribeSources.verification-r77.txt` |
| evidence — endpoint-page HTTP receipts | `.ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt` |

Scratch root `/fast/scratch/hyaku/kasegi-r77/scribesources` was created with `mkdir -p`, passed explicitly as
`TMPDIR=` to every instrument run, and removed before this report was filed. No tool was installed or
upgraded (nothing in the seat's task needed one; the host's `pacman` pause was therefore not engaged).

---

## 1. What the three drafts contain

**`lesson-gate-skeleton.md`** — the `corpus/lessons/round-77.md` skeleton in the shape of
`corpus/lessons/round-76.md` (Gate :5-15, Counters :17-23, Mistakes :25-33, Routed defects :35-41):

- header with the frozen claims, freeze `539a4387…`, base `2e53fc74…`, and the wave shape
  **"one v1 wave of 13 seats, attack 5/13"** (13 = the item count of `.ufo/waves/round-77/w1-spec.json`;
  the five attack seats are ReviewC1, ReviewC2, CriticClaims, MutC1, SentinelC1). The final dead-seat
  count is left explicitly **for the L1 to fill** — at write time no seat had reported dead or alive
  (`ls -la .ufo/waves/round-77/w1/`, 2026-11-05T12:42Z, shows only this seat's files, the connector's three
  id files and a `MutC1-evidence/` directory).
- `## Gate` with: candidates considered (F54 = the `POST /v1/querybatch` contract on S112, with the
  located ≤25-word quote "Query for multiple packages (by either package and version or git commit hash) at
  once." at **S112.txt:24**, 15 words); the four other endpoint pages screened as leads; new rows written
  (S112 — URL, access date 2026-11-05, capture digest, anchor lines, quote); admitted (F54, pending L1
  landing, with the entry's claimed ground enumerated); rejected rows (none); **three reject lines** —
  the R119 distinctness line, the four-leads line, and the S111-still-queued line; considerthese and
  assimilation placeholder lines; spot-check pending note; and the sourced-claim (frontier step) line.
- a `## Counters` table of the values this seat re-measured, each with its command, rc and observed output;
  a pointer to the mistakes draft; and two routed-defect candidates (§ R-77-D, § R-77-E below).

**`registry-changes-draft.md`** — the three SOURCES.md prose blocks the L1 lands:

- `## Registry changes`: the round-77 S112 bullet (registry 111 → 112, tier A docs, anchor pinned to the
  round-77 capture, F54 admitted, knowledge 91 → 92), the **two landing cell flips recorded as old → new**
  (`queued` → `mined`; used-by `—` → `corpus/knowledge/osv-post-v1-querybatch-contract.md`), and the
  capture/row-binding note (one commit carries capture + manifest + row → `records=91 bound=91 unbound=0`).
- `## Leads (unopened)`: the round-77 bullet naming the four sibling endpoint pages **with their HTTP
  receipts** (19961 / 30242 / 16418 / 18769 bytes, all 200) and the S111 queued-carried note.
- `## Search log`: the round-77 bounded-screen entry (question; where searched; identified 5, screened 5,
  included 1 (querybatch), excluded 4; the stop rationale), with a bookkeeping note on the screened count.

**`mistakes-draft.md`** — eight `## Mistakes` candidate rows mined from the inherited round-76 verdict,
each with class / evidence / captured-by / fix and each marked **pending L1 confirmation**:
M77-candidate-1 (the r76 m2b survivor class — closed by the consumed assertion, with the red-before receipt
proving the fix is able to fail), -2 (dispatch order), -3 (distinctness sweep after the freeze), -4 (a
manifest quote below the instrument floor), -5 (a capture without its registry row), -8 (the r76 R-D id
collision persisting, now for two ids), plus two candidates this seat found in this round's own bytes: -6 (a
registry row that lands without its `## Registry changes` prose) and -7 (a reject line whose HTTP status the
receipts contradict).

---

## 2. Measurements this seat took (all re-runnable; receipts in `ScribeSources.verification-r77.txt`)

| # | command | rc | observed |
|---|---|---|---|
| 1 | `python3 -B .ufo/waves/round-76/controls/m2b-conjunct-removed.py --selftest` (scratch copy) | 0 | `selftest cases=8 failures=0` — the r76 survivor class still stands on the r76 design (red-before) |
| 2 | `python3 -B .ufo/waves/round-77/c1-amended-reference.py --selftest` (scratch copy) | 0 | `selftest cases=12 failures=0` |
| 3 | `python3 -B .ufo/waves/round-77/controls/m1-registration-removed.py --selftest` | 1 | `cases=12 failures=3`; `gate-regs FAIL registered=[]`, `gate-consume FAIL no-registration`, `gate-negpolarity FAIL no-registration` — assertion class |
| 4 | `python3 -B .ufo/waves/round-77/controls/m2-consumption-neutered.py --selftest` | 1 | `cases=12 failures=1`; `gate-consume ok clean_ok=True`, **`gate-negpolarity FAIL neg_ok=True`** — the required m2b-class **assertion** kill (R127 satisfied: no traceback) |
| 5 | `python3 -B .ufo/waves/round-77/controls/m3-computation-deleted.py --selftest` | 1 | `cases=12 failures=2`; `gate-consume FAIL exception=NameError("name 'out6' is not defined")`, `gate-negpolarity FAIL not-evaluated-after-exception` — the **exception** class, logged distinctly (R127) |
| 6 | `python3 -B .ufo/waves/round-77/controls/m4-negpolarity-inverted.py --selftest` | 1 | `cases=12 failures=1`; `gate-negpolarity FAIL neg_ok=False` — assertion class |
| 7 | `python3 -B .ufo/waves/round-77/controls/m5-check-deleted.py --selftest` | 1 | `cases=11 failures=1`; `gate-checkids FAIL missing=['both-headers'] extra=[]` — assertion class |
| 8 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` | 0 | `S112:sha256 OK` + 13 × `OK occurrences=1 anchor=<n>-ok` (anchors 24,24,24,30,31,34,35,36,166,168,169,170,195) — matches the frozen R126 receipt `controls/c2-prerecheck-r77.txt` |
| 9 | `python3 corpus/instruments/capture-binding-check.py` | 0 | `records=91 bound=91 unbound=0`; `MANIFEST round-77 records=1 url_bound=1 fetched=1 archival=0` |
| 10 | `python3 corpus/instruments/frontier-recheck-count.py` | 0 | `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112` / `entries=56 pass=56 exit=0` (at the freeze tree; frozen B3 expects rows=54 / entries=57 at the landing tree) |
| 11 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | 0 | `kasegi ok …/corpus/SOURCES.md` with the six inherited W04 warnings (S028, S029, S072, S076, S080, S085) unchanged |
| 12 | endpoint-page probes (4 live slugs + 6 wrong slugs), 2026-11-05T12:40:45Z | — | live: 200 / 19961, 30242, 16418, 18769 bytes; wrong-slug: 404 / 11373 bytes each — receipt `ScribeSources.endpoint-probe-r77.txt` |
| 13 | `git status --porcelain` | — | untracked only (`w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/`, `corpus/lessons/round-77.md`); no tracked file modified by this seat |

Digests verified: `c1-amended-reference.py` = `18bfc439…a33` (matches the frozen claim), base counter
`corpus/instruments/recheck-cwd-census.py` = `e666ae11…21a` (matches the frozen claim), `S112.txt` =
`f3ca0465…0907` (matches the manifest record), the five mutant controls = `c2746492…`, `b7772949…`,
`1fd8d29a…`, `7f5bb936…`, `b7af7722…` (matches `c1-mutant-transforms.md`).

---

## 3. Findings for the L1 (routed, not edits)

**F-SS-1 — the reject line's "and S111 captures" does not support the `api.osv.dev` host form.**
The frozen B6 and the L1's working-tree lesson reject "the endpoint path string `POST /v1/querybatch` and
the `api.osv.dev` host form" as already held "from `S108.txt:5-9` … and from `S111.txt:5,43`". Measured:
`grep -c 'api\.osv\.dev' corpus/source-snapshots/round-76/S111.txt` → **0** — the S111 capture carries no
host form at all; and `grep -rn 'api\.osv\.dev' corpus/knowledge/*.md` → 0 hits in every knowledge entry.
The host form is held, but from different bytes: `S108.txt:72,76,80,147` (`https://api.osv.dev/v1/query`)
and the **S065** registry row (`corpus/SOURCES.md:71`, `api.osv.dev/v1/vulns/CVE-2025-55305`). The PATH
string claim is sound (`S108.txt:5`, `S111.txt:5` and `:43`, named at `corpus/knowledge/osv-post-v1-query-contract.md:75`).
The draft reject line in `lesson-gate-skeleton.md` keeps the frozen wording and adds the S065 citation
rather than the S111 one; the L1 decides.

**F-SS-2 — the four lead pages answer 200, not 404.** The L1's working-tree lesson's leads reject line
says the four sibling endpoint pages "were probed at the morning slugs `get-v1-vulns-id` and siblings and
returned HTTP 404 (11373 B)". Measured at 2026-11-05T12:40:45Z: the four **navigation** slugs answer
**HTTP 200** (19961 / 30242 / 16418 / 18769 bytes); the 404s come from the wrong-slug shapes. The pages are
live and unopened, so the reject reason must be "not adopted this round (one admission per round per lane
practice; each needs its own capture and its own distinctness sweep)", with the live-slug receipts. The
draft in `lesson-gate-skeleton.md` and `registry-changes-draft.md` §(B)/(C) is written that way.

**F-SS-3 — round 76 landed a registry row with no `## Registry changes` prose and no `## Search log` entry.**
`grep -n 'Round-76\|round-76' corpus/SOURCES.md` prints exactly one hit — the S111 row's own capture path at
`corpus/SOURCES.md:123` — while round-73/74/75 bullets sit at :271/:272/:273. The round-76 lesson's Gate
does record the row, so the omission is in the registry prose. The round-77 bullets in
`registry-changes-draft.md` §(A) close the round-77 side; the round-76 S111 bullet may be appended by the
L1 as its own statement (R8 append-only) or routed onward. This seat did not write it.

**F-SS-4 — the staged campaign package collides with S112 as well as S111.**
`merge/kasegi/SOURCES.append.md` (read-only) stages **94 ids spanning S031-S124**, and its `S112`
(`:88`, a TC260 route record) is a different document from this lane's S112. The round-77 connector's own
recount agrees — and states the same finding independently: reg-ids 112, staged-ids 94, collisions **82**,
and `reg ∩ staged == collisions` (82 == 82, with S111 and S112 both in the list). The connector's own
words (`ConnectorOverlap.md` §1): "the spec premise 'the new S112 is outside S001-S094 so it adds none' is
false. The staged package spans S031–S124." This is the round-76 R-D defect recurring one id further up
the band — a routed defect for the L0 question file, not a blocker for this round's admission, since the
lane's own ids are authoritative inside `corpus/SOURCES.md` and the package is not adopted this round.
Draft bullet in `registry-changes-draft.md` §(A.1); draft mistake row `M77-candidate-8` in
`mistakes-draft.md`.

**F-SS-5 — a minor bookkeeping fork in the search-log count.** The five candidates of this round's screen
are `querybatch` plus the four sibling endpoint pages (the sixth endpoint, `POST /v1/query`, is already
held from S108/F51 and is listed as held rather than re-screened). The draft records "identified 5, screened
5, included 1, excluded 4"; a "screened 1" reading is also defensible as long as it is one of them and the
four excluded pages carry their receipts. Flagged in `registry-changes-draft.md` §(C.1).

---

## 4. Out of scope for this seat (stated, not done)

- No lane file was edited: `corpus/lessons/round-77.md`, `corpus/SOURCES.md`, `corpus/README.md`,
  `PROVINCE.md`, `corpus/knowledge/` and every instrument are untouched by this seat.
- No git or jj mutation of any kind was run; only `show / log / rev-parse / ls-tree / diff / status` and
  `git archive`-free reads were used.
- The L1's own working-tree lesson (`corpus/lessons/round-77.md`, untracked at the time of writing) was
  read for consistency and NOT modified; this seat's drafts are wave-dir drafts only.
- No knowledge entry, README block, PROVINCE line or `knowledge-expected.txt` row was drafted — those are
  the `ScribeEntry` seat's named artifacts.
- No sibling-lane scan (the `ScoutSurface`/`ConnectorOverlap` seats' subjects) and no shokuknow edit; the
  staged package was read only.

---

## 5. The two decisions the L1 must take from this seat

1. **Which of the eight mistake candidates become the round-77 ledger's own rows** (ids, and whether the
   two this-seat-own findings — F-SS-3's row and F-SS-2's row — are kept, reworded or routed), given that
   the L1's working-tree lesson already occupies M77-1..M77-4.
2. **Which wording the `## Gate` reject line carries for the four endpoint pages** — the measured HTTP 200
   (this seat's drafts) or the morning 404 (the L1's current wording). The receipts support the 200 wording,
   and F-SS-1 shows the host-form half of the distinctness line needs the S065 citation rather than S111.

---

## 6. Dead-seat count — NOT filled by this seat (the L1's to fill)

At the time of this report the wave dir holds reports from some seats and not others
(`ls -la .ufo/waves/round-77/w1/`, 2026-11-05T12:46Z). `RevengerInherited.md` is a 12-byte file containing
only `PLACEHOLDER` — that seat has not filed a real report — and several seats have not filed at all. This
seat does not state a dead-seat count: the count is the L1's, and it must be taken from the wave's own
dispatch results after WAKE-DONE. The skeleton in `lesson-gate-skeleton.md` leaves the field explicitly
open with this note attached.
