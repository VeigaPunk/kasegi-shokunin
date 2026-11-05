# mistakes-draft — `## Mistakes` candidate rows for the round-77 lesson (WAVE-DIR DRAFT)

Seat: ScribeSources (round 77, attempt 1, wave `w1`). Draft only; the L1 `KasegiR77` decides which candidates
are this round's OWN ledger rows and finalises their wording. Every row below is marked
**pending L1 confirmation** — this seat mined them, it did not accept them.

Source of the mining: the inherited round-76 verdict (`corpus/lessons/round-76.md` § Mistakes, lines 25-33)
and its non-author spot-check (`corpus/lessons/round-76-verifier-spotcheck.md` § 6 fix list V-A..V-E). The
round-76 mistake ids are M76-1..M76-7; the ids proposed here are M77-candidate-N, which the L1 renumbers to
M77-1.. on acceptance. The L1's own working-tree lesson already carries M77-1..M77-4 for THIS round's
integration mistakes (the gate's self-inclusion, the capture written to a file path, the census TMPDIR
fragility, the pre-freeze dry-run ordering); those are the L1's, not this seat's, and are not restated here.

Every evidence line below was re-measured by this seat against committed bytes; the receipts are in
`.ufo/waves/round-77/w1/ScribeSources.verification-r77.txt` (sections numbered below) and
`.ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt`.

---

## M77-candidate-1 — the r76 m2b survivor class is closed by a consumed assertion, and the fix is shown able to fail

- **Class:** `survivor` — an assertion whose removal from the instrument's own consumption site leaves the
  gate green (the r76 defect, M76-3 / QUALITY R127).
- **Evidence:** the r76 candidate design's consuming-conjunct mutant still survives: `python3 -B
  .ufo/waves/round-76/controls/m2b-conjunct-removed.py --selftest` → `selftest cases=8 failures=0`, **rc 0**
  (re-run in scratch by this seat: rc 0, same last line — `ScribeSources.verification-r77.txt` §2; frozen
  receipt `.ufo/waves/round-77/controls/c1-redbefore-r76-survivor-r77.txt`). The r77 gate closes it by making
  the case-6 RESULT limb a consumed assertion behind four checks: the required m2b-class kill is K-M2
  (the registration closure body replaced by `True`, arguments unconsumed), which exits 1 with
  `gate-consume ok clean_ok=True` and `gate-negpolarity FAIL neg_ok=True` — an **assertion failure, no
  traceback** — not the NameError-only kill R127 forbids (re-run by this seat: rc 1, `selftest cases=12
  failures=1`; committed receipt `.ufo/waves/round-77/controls/m2-consumption-neutered.py.out`). The
  exception-class mutant K-M3 is separately distinguished: `gate-consume FAIL exception=NameError(...)`
  (rc 1, `cases=12 failures=2`), recorded as the exception class and not counted as a semantic kill.
- **Captured-by:** QUALITY R127 (`corpus/QUALITY.md:579` — "Distinguish mutation assertion failures from
  runtime exceptions … a NameError alone does not prove semantic detection"); the round-76 fix list V-A
  (`corpus/lessons/round-76-verifier-spotcheck.md` §6 V-A).
- **Fix:** the frozen C1 predicate's A3 makes the case-6 result a consumed assertion with a four-check gate
  (`gate-regs`, `gate-consume`, `gate-negpolarity`, `gate-checkids`), and the red-before receipt keeps the
  survivor class visible on the r76 design. The fix is **shown able to fail**: the red-before mutant is
  rc 0 on the old bytes and the same class of mutation is rc 1 on the amended bytes, so the gate is the
  delta that kills it.
- **Status:** pending L1 confirmation.

## M77-candidate-2 — a mutation seat dispatched before its input existed (r76 M76-7 recurrence guard)

- **Class:** `dispatch-order` — a seat that consumes another seat's output runs before that output exists.
- **Evidence:** round-76 `w1/MutC1.md` — `blocked-no-candidate`, "ExecC1Amend.patch absent (ls rc=2, checked
  once after setup, no wait-loop)". In round 77 the analogous input is committed AT THE FREEZE
  (`.ufo/waves/round-77/c1-amended-reference.py`, sha256 `18bfc439…`, and the five committed mutant controls
  under `.ufo/waves/round-77/controls/`), so the class is structurally prevented this round; the wave's
  mutation seat writes its evidence into `.ufo/waves/round-77/w1/MutC1-evidence/` (24 files, present at
  2026-11-05T12:42Z), including a `r76-m2b-redbefore.out` receipt.
- **Captured-by:** none in QUALITY (the r76 lesson recorded "Captured-by: none"); the round-76 wave's
  dependency-ordering rule (r76 lesson R-E).
- **Fix:** freeze the mutation input with the claims (as round 77 does) or dependency-order the seats of a
  wave.
- **Status:** pending L1 confirmation. **Note for the L1:** this is a candidate for the round's ledger only if
  the round's own wave had a dead or blocked seat; the r76 class did not recur on the recorded evidence.

## M77-candidate-3 — a distinctness sweep that runs after the freeze does not close the freeze (r76 M76-1 / R125)

- **Class:** `scope` / `reference-drift` — a coverage claim lists as new ground what the lane already holds.
- **Evidence:** round-76 `CriticClaims` F12 (BLOCKER) and `ReviewC2` re-opened the frozen C2 statement and
  found the six endpoint path strings already held from `S108.txt:5-9` (F51's own Limits bullet,
  `corpus/knowledge/osv-post-v1-query-contract.md:75`) and S080 — a sweep run AFTER the freeze.
  Round 77 freezes the opposite shape: the C2 statement claims only the batch-contract clauses (Q01-Q13 at
  S112.txt lines 24, 30, 31, 34, 35, 36, 166, 168, 169, 170, 195) and states the path string and the host
  form as already-held listed-not-described ground (frozen B6). Re-measured by this seat:
  `grep -n 'POST /v1/querybatch' corpus/knowledge/osv-post-v1-query-contract.md` → line 75 (the F51 Limits
  bullet, "They are listed, not described."); `grep -n 'POST /v1/querybatch'
  corpus/source-snapshots/round-73/S108.txt` → line 5; `grep -n 'POST /v1/querybatch'
  corpus/source-snapshots/round-76/S111.txt` → lines 5 and 43.
- **Captured-by:** QUALITY R114 (subject sweep, `corpus/QUALITY.md:538`) and R125 (admitted-entry sweep,
  `corpus/QUALITY.md:577`).
- **Fix:** run the subject sweep AND the admitted-entry sweep before the freeze, and record the per-clause
  verdict — which is what the round-77 `ScoutSurface` seat is for.
- **Status:** pending L1 confirmation.

## M77-candidate-4 — a manifest quote below the instrument's own floor (r76 M76-2 / R126)

- **Class:** `number-drift`-adjacent — a pinned value the gate itself refuses.
- **Evidence:** the round-76 frozen Q01 quote "API (1.0)" normalizes to 9 characters against
  `MIN_QUOTE_CHARS = 12` at `corpus/instruments/source-recheck.py:33`, and exited 2 from `source-recheck.py`
  (`S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`). Round 77 froze a FRESH
  manifest whose 13 quotes all pass: the frozen receipt
  `.ufo/waves/round-77/controls/c2-prerecheck-r77.txt` prints `S112:sha256 OK` and 13
  `OK occurrences=1 anchor=<n>-ok` lines, rc 0; this seat re-ran the same command on the committed tree and
  got the same 14 lines, rc 0 (`ScribeSources.verification-r77.txt` §5). The longest ground quote in the
  round-77 registry row is 15 words ("Query for multiple packages (by either package and version or git
  commit hash) at once.", S112.txt:24), inside the ≤25-word cap of Q3.
- **Captured-by:** QUALITY R126 (`corpus/QUALITY.md:578`).
- **Fix:** run the source recheck on the final manifest BEFORE freezing its success predicate; the round-77
  receipt does that, so the class does not recur — the candidate row records that the fix is in place.
- **Status:** pending L1 confirmation.

## M77-candidate-5 — a freeze commit that carries a capture without its registry row (r76 M76-5)

- **Class:** `landing` — the binding between a capture, its manifest record and its registry row is split
  across commits.
- **Evidence:** round 76 `capture-binding-check.py` read `FAIL rule=no-row record=S111` on the freeze tree
  until the row landed (`w1/ExecC2Checks` r4). Round 77's freeze commit `539a4387` carries
  `corpus/SOURCES.md` (+1 line, the S112 row), `corpus/source-snapshots/round-77/S112.txt` (+216) and
  `corpus/source-snapshots/round-77/manifest.json` (+89) in ONE commit (`git show --stat 539a4387`); the
  instrument at the freeze tree reads `records=91 bound=91 unbound=0` and exits 0 (re-run by this seat —
  `ScribeSources.verification-r77.txt` §6).
- **Captured-by:** QUALITY R20 (a capture snapshot ships with its manifest in the same round and commit) and
  R21 (a manifest record carries a `url` the registry row independently names and a fetch instant).
- **Fix:** stage the capture with its row in one commit.
- **Status:** pending L1 confirmation.

## M77-candidate-6 — a registry row that lands without its `## Registry changes` prose (this round's own
## observation, carried from the round-76 record)

- **Class:** `landing` / `record-discipline` — the ledger of registry changes is not the same thing as the
  registry itself, and a row can land with no record of when it was written, at what status, or why it is
  unused.
- **Evidence:** `corpus/SOURCES.md` carries no `## Registry changes` bullet and no `## Search log` entry for
  round 76: `grep -n 'Round-76\|round-76' corpus/SOURCES.md` prints exactly ONE hit — the S111 row's own
  capture path at `corpus/SOURCES.md:123` — while the preceding rounds' bullets are present
  (round-73 at :271, round-74 at :272, round-75 at :273) and the round-76 S111 row itself is at :123. The
  round-76 lesson's own Gate records the row ("new row written this round: S111 — `queued`"), so the
  omission is in the registry prose, not in the lesson.
- **Captured-by:** QUALITY R8 (log every status/recheck/used-by old → new change) — the lane's own
  convention, since every earlier round that wrote a row wrote its bullet.
- **Fix:** the round-77 bullets in `.ufo/waves/round-77/w1/registry-changes-draft.md` §(A) record S112 with
  its two landing flips; the missing round-76 S111 bullet may be appended by the L1 as its own statement
  (R8 append-only form) or routed to the next round. This seat does not write it.
- **Status:** pending L1 confirmation. **This candidate is this seat's own finding for this round** and is
  the only row here that is not mined from the round-76 verdict — the L1 may keep it, reword it, or route it.

## M77-candidate-7 — a reject line that cites an HTTP status the measured receipt contradicts (this round's
## own observation)

- **Class:** `record-discipline` / `stale-premise` — a Gate reject line asserts a URL state that the round's
  own receipts show to be different.
- **Evidence:** the four sibling OSV.dev endpoint pages answer **HTTP 200** at the slugs the S111 navigation
  names (`get-v1-vulns/` 19961 B, `post-v1-determineversion/` 30242 B, `get-v1-importfindings/` 16418 B,
  `post-v1-ubuntu-binary-to-source/` 18769 B, probed 2026-11-05T12:40:45Z,
  `.ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt`); the round-77 morning 404s (11373 B each)
  came from WRONG-SLUG shapes (`get-v1-vulns-id`, `get-v1experimental-importfindings`,
  `post-v1experimental-determineversion`, `post-v1experimental-ubuntu-binary-to-source`). The four pages are
  therefore unopened-but-live leads, not 404 ends, and a reject line that says 404 is a stale premise under
  R19.
- **Captured-by:** QUALITY R19 (a figure quoted inside a record row is produced by a command the row cites)
  and R121 (a clause binding an absolute value must name the revision it was measured at).
- **Fix:** state the reject reason as "not adopted this round (one admission per round per lane practice;
  each needs its own capture and its own distinctness sweep)" and carry the HTTP receipts for the LIVE
  slugs; record the wrong-slug 404s as what they are.
- **Status:** pending L1 confirmation. The draft wording that satisfies this is in
  `.ufo/waves/round-77/w1/lesson-gate-skeleton.md` § Gate.

---

## M77-candidate-8 — a staged id collides with this lane's own row, and the round's premise about the
## staged range was false (r76 routed defect R-D, persisting)

- **Class:** `landing` / `id-drift` — a registry id is minted inside the range the staged package already
  uses, for a different document.
- **Evidence:** the round-76 lesson routed this as R-D (the staged `S111` id collided with this lane's own
  round-76 S111 row; `merge/kasegi/SOURCES.append.md:87` is a CN-CERT weekly-report row). The round-77
  connector's recount shows the same class one id further up and shows that the round's own premise was
  wrong: the staged package spans **S031-S124**, not S001-S094 — registry 112 ids, staged 94 ids,
  **82 collisions** (`.ufo/waves/round-77/w1/ConnectorOverlap.collisions.txt`; `reg ∩ staged == collisions`,
  82 == 82, verified by this seat), with both `S111` (`:87`, NCSC weekly report) and `S112` (`:88`, a TC260
  route record) colliding against this lane's own rows at `corpus/SOURCES.md:123-124`. The connector's own
  words: "the spec premise 'the new S112 is outside S001-S094 so it adds none' is false"
  (`ConnectorOverlap.md` §1).
- **Captured-by:** none in QUALITY — the round-76 lesson recorded "Captured-by: none" for R-D; the round-76
  fix list V-D ("two L0 questions remain open … keep routed around; never assume an answer").
- **Fix:** mint a registry id outside the staged package's whole range, or renumber at merge time; resolve
  the id before integration. Until then the package stays L0-routed and nothing is adopted. This seat's
  drafts record the collision as a routed item rather than adopting anything.
- **Status:** pending L1 confirmation.

---

## Summary for the L1

| candidate | class | mined from | evidence re-measured by this seat | status |
|---|---|---|---|---|
| M77-candidate-1 | `survivor` | r76 M76-3 / V-A | yes (rc 0 red-before; K-M2 rc 1 assertion kill) | pending L1 confirmation |
| M77-candidate-2 | `dispatch-order` | r76 M76-7 / R-E | yes (input committed at the freeze; no recurrence on the recorded evidence) | pending L1 confirmation |
| M77-candidate-3 | `scope` / `reference-drift` | r76 M76-1 / R114+R125 | yes (F51:75, S108.txt:5, S111.txt:5,43) | pending L1 confirmation |
| M77-candidate-4 | `number-drift`-adjacent | r76 M76-2 / R126 | yes (14 OK lines, rc 0, fresh manifest) | pending L1 confirmation |
| M77-candidate-5 | `landing` | r76 M76-5 / R20+R21 | yes (`records=91 bound=91 unbound=0`; one-commit freeze) | pending L1 confirmation |
| M77-candidate-6 | `landing` / `record-discipline` | this round's own | yes (SOURCES.md round-76 bullet absent) | pending L1 confirmation |
| M77-candidate-7 | `record-discipline` / `stale-premise` | this round's own | yes (four live slugs answer 200) | pending L1 confirmation |
| M77-candidate-8 | `landing` / `id-drift` | r76 R-D / V-D | yes (staged S031-S124; 82 collisions; S111 and S112 both collide) | pending L1 confirmation |

**L1 decision needed on two points this seat cannot decide:**
1. Which of these eight become the round-77 ledger's own `M77-1..` rows (the L1's own M77-1..M77-4 occupy
   those ids in its working-tree lesson — the L1 must renumber or fold them).
2. Whether the round-77 lesson's `## Gate` reject line for the four endpoint pages asserts the measured
   HTTP 200 (this seat's draft) or the morning 404 (the L1's current working-tree wording). The receipts
   support the 200 wording for the navigation slugs.
