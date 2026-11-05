# ReviewC2 — independent pre-integration verification of frozen claim C2 (round-76, attempt 1, wave w1)

Seat: ReviewC2 (leaf reviewer; no subagent dispatch). Frozen claims read IN FULL:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-76/claims.json`
(sha256 719e0d7884565bbeedb4add52fe510a1a8c166a710fec53969f7b8b48b2fde3d, identical to the
committed blob at the freeze commit `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`; the B1–B7
predicates and the kill rule are quoted below verbatim from it, not reworded). All
commands ran from the lane root unless stated; every recorded exit code is the real
return of the command as run.

Scope note: this is a PRE-INTEGRATION review. At the freeze commit, the landing surfaces
(corpus/SOURCES.md row S111, the knowledge entry, corpus/README.md F54 block,
corpus/instruments/knowledge-expected.txt line) do NOT exist; the freeze carries only the
capture + manifest + receipts. B1, B2, B3, B4, B7 are integration-state letters and are
recorded PENDING-INTEGRATION with the named commands. What can be measured now (B5, B6
ground, base-counter reproduction) is measured now — and B5 fails.

## Environment

- Freeze commit resolves: `git rev-parse 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e^{commit}` →
  `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`, rc=0. `git log --oneline -1` at the lane root
  prints the same commit as HEAD (lane parked at the freeze; the only worktree delta is the
  untracked w1 wave files).
- Scratch: `/fast/scratch/hyaku/kasegi-r76/ReviewC2/` created rc=0; all counter runs passed
  `--scratch /fast/scratch/hyaku/kasegi-r76/ReviewC2/...`; removed before reporting.

## 1. B5 — source-recheck on S111 (measured now): FAIL

Command (as specified verbatim):
`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-76/manifest.json --source S111`
(ran from the lane root, cwd = /home/vgpnk/Projects/shokunin/kasegi-shokunin, rc checked by `echo rc=$?`)

Expected by predicate B5: "reports sha256 OK and all 13 quotes anchor-located, exit 0."
Observed, three runs (all identical):

```
S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence
rc=2
```

Nothing else prints: because the validator fails closed at its first hard error
(`return 2`), not even `sha256 OK` is emitted. The capture bytes themselves are sound —
the sha256 in the manifest pins and I re-derived it:
`sha256sum corpus/source-snapshots/round-76/S111.txt` →
`6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab`, rc=0 (48 lines,
`wc -l` rc=0; 1810 bytes per the manifest `bytes` field). Fan-out cross-check:

1. **Root cause, instrument bytes (not flake, not environment):**
   `corpus/instruments/source-recheck.py:33` sets `MIN_QUOTE_CHARS = 12` ("normalized
   minimum: a shorter 'quote' matches any capture"), and lines 149–154 fail closed:
   a quote shorter than 12 normalized chars exits rc=2 before any anchor matching.
   `--source` invocation is `return recheck(args.manifest, args.source)`
   (line 411), so exit 2 is the hard stop.
2. **Root cause, normalization:** the instrument strips HTML tags and collapses
   whitespace before counting. `Q01-api-version` quotes "API (1.0)"; I reproduced the
   validator's own `normalize()` (tag-strip + `\s+`→space + strip) in Python →
   normalized length **9**, below the 12 floor. A quote stranded entirely on a short
   line can never anchor against that line.
3. **Line-21 exhaustion:** every alternative quote for line 21 of S111.txt has the
   same problem — normalized `API (1.0)` = 9, and no other anchor on that line. Renaming
   the quote id does not help because the missing credit comes from the false prefix
   `S111:Q01-api-version` + punctuation. No fixture built over capture line 21 as its
   sole anchor can pass.
4. **12 other quotes are individually sound (by the instrument's own matcher):** the
   sibling scratch experiment
   `.ufo/waves/round-76/w1/ScribeEntry-recheck-S111-without-Q01.txt` (same manifest and
   capture with Q01 removed in a scratch copy — L1-owned experiment, I read the file but
   did not rerun it) shows exactly what predication wants minus Q01: `S111:sha256 OK`
   plus 12 × `OK occurrences=1 anchor=N-ok` for anchors 22, 28, 29, 30, 31, 32, 33, 34,
   35, 36, 38, 39. My independent Python anchor check agrees: each of the 13 declared
   anchors (21, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39) locates its quote at
   exactly that line, exactly once, in the capture — the manifest's *content* is good.
5. **Pre-existing, not introduced after the freeze:** this is not a mutation of an
   already-green run; the frozen receipt itself shows it — ScribeEntry's committed
   `ScribeEntry-recheck-S111.txt` (mtime 2026-11-05 07:54:30 -0300, pre-integration)
   prints the same `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`.
   unchanged at the freeze: `git log --oneline -1 --
   corpus/instruments/source-recheck.py` →
   `eecad59 round-31: wave-1 integration (C1 limb ledger+counter, C2 F15/S048, score-gap, erratum, LOG r30), wave-2 spec`
   (the instrument last changed in round 31; it was NOT touched in rounds 74–76), and
   `git diff 5da54cd -- corpus/instruments/source-recheck.py | head` → empty,
   rc=0 (the working tree's copy is byte-identical to the freeze-commit blob).
6. **So B5's as-written shape cannot be satisfied:** the designed claim's planned
   "13 quotes anchor-ok" needs 13 PASS-ing quotes; the capture physically supports
   them (independent Python recheck), but the instrument floor makes Q01 as-authored
   unpassable. Until the landing fixes the fixture (options already drafted in
   ScribeEntry: (a) drop/rewrite Q01 or re-anchor it to a >12-char line, e.g. the
   "Not the record format..." clause 1; the L1 drafts name the same repair), the
   landing instrument will exit 2 no matter what the rest of the round looks like.

The count question stays on the L1 side to answer, not on the instrument — the
12-char floor is pre-existing behavior protecting against r24 RevC1Control-style forgery
and is NOT rewritten by this round for C1 parity (quals note: MIN_QUOTE_CHARS applies
to every manifest, so relaxing it just for S111 is exactly the single-flight sugar the
round is trying to kill).

Because B5 fails at pre-integration and B5 "source-recheck... exit 0" is also the gate
without which the landing B4/B3/B1 chain cannot be measured (the landing tree still
prints UNAVAILABLE on the same frozen manifest path), I record:

**B5: FAIL — `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`, rc=2, expected exit 0 with 13 quotes anchor-located.**

## 2. B6 — knowledge entry draft (measured now, entry not yet landed): PASS-with-notes

Entry draft: `.ufo/waves/round-76/w1/f54-entry-draft.md` (72 lines). The file I read at
`2026-11-05T11:04:28Z` (after it stopped being revised at 07:5x, all check-window
rereads agree):

1. **Header contract present:** the draft opens with `source: S111 — https://google.github.io/osv.dev/api/`
   and names the capture with the frozen sha256
   (`6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab`, verified against
   the file). The `recheck:` line names the instrument path (same invocation as B5's
   canonical command, matching the frozen spec).

2. **Sentence-by-anchor check:** every anchored clause sits where the draft says:

   - `"API (1.0)"` (S111.txt:21): the capture line is exactly `API (1.0)` — byte-for-byte.
   - `"Download the OpenAPI specification"` (S111.txt:22): capture line 22 — exact.
   - `"Download Here"` (S111.txt:23): capture line 23 — exact.
   - "There are six different types of requests that can be made of the API."
     (S111.txt:28): capture line 28 — exact.
   - The six semantics (S111.txt:29–34): all six exact, in capture order.
   - Navigation paths (S111.txt:4–9): `POST /v1/query`, `POST /v1/querybatch`,
     `GET /v1/vulns/{id}`, `GET /v1experimental/importfindings`,
     `POST /v1experimental/ determineversion`, `POST /v1experimental/ubuntu/binary-to-source`
     — exact; the entry faithfully records the page's space-after-slash in the
     determineversion path and writes the semantics in **capture line order** (29½34),
     preserving the page's own order and openly flagging (`[entry's reading]`) that the
     "pairing" of semantic line ↔ path verb is the entry's own act, not page-supplied.
   - Rate-limit Q&A (S111.txt:35–36): both exact.
   - Response-size clause (S111.txt:38): "The API has a response size limit of 32MiB
     when using HTTP/1.1. There is no limit when using HTTP/2." — byte-identical, and
     I verified the same sentence is already held at S108 (round-73): S108.txt:148 reads
     `The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2. We recommend using HTTP/2 for queries that may result in large responses.`
     and the round-73 manifest pins it as Q27 (`Q27-size-http1`, anchor 148),
     Q28 (`Q28-size-http2`, anchor 148), Q29 (`Q29-http2-recommend`, anchor 148);
     `corpus/knowledge/osv-post-v1-query-contract.md:55` (F51, Claim 6 at :53) already
     holds both.
   - HTTP/2 recommendation (S111.txt:39): "We recommend using HTTP/2 for queries that
     may result in large responses (e.g. big OSV Linux queries)." — exact.
3. **No-sentence-without-anchor:** I found no clause attributed to a capture line that
   does not exist there, and no quote whose source is not the page (all six list items
   match capture bytes exactly; a few pages surface the same sentence on multiple lines,
   which the entry does not depend on). The only non-page material in the entry body is
   the entry's own analysis (the `[entry's reading]` pairing paragraph at line 32 and
   the "Limits — what this entry does not hold" section), which the entry itself marks.
   The "Rejected over-generalization" clauses are analysis, not attributions of page text.
4. **32MiB/HTTP-2 clause marked as already-held, not claimed new:** the entry has
   block `## Response-size limits — held ground from S108, cross-referenced, not
   claimed here` and states: "These two sentences are word-identical to S108.txt:148
   and are already held: F51 (`corpus/knowledge/osv-post-v1-query-contract.md`,
   Claim 6), round-73 manifest Q27-Q28. This entry adds no claim on them." That is the
   correct B6 discipline. Also correct: line 39 (`Q13-http2-recommend`) is noted as
   "in the capture and manifest (Q13) but is not claimed here" (parenthetical example
   beyond the already-held sentence). The frozen B6 wording crosses the Q13 line as
   "not claimed", and the draft headline "the response-size clauses at capture line 38
   are ALREADY-HELD ground" matches exactly what the entry does (32MiB at :38 not
   claimed new; the :39 recommendation explicitly not claimed either).
5. **Distinctness (the kill-rule clause):** the draft's subject sweep names exactly the
   set of pages holding any OSV subject today — S065 (SOURCES.md:71), S080 (row :86,
   entry `osv-affected-range-events.md:18`), S108 (row :120, entry
   `osv-post-v1-query-contract.md`), the lead-only note at SOURCES.md:175, and the
   Scorecard service mentions in `openssf-scorecard-checks.md:35, :83`. I re-ran the
   sweep: `grep -n -i -E 'osv\.dev|google\.github\.io/osv' corpus/SOURCES.md corpus/knowledge/*.md`
   → rc=0, **12 matches in exactly those 4 files** (SOURCES.md :71, :86, :120, :175;
   openssf-scorecard-checks.md :35, :83; osv-affected-range-events.md :18;
   osv-post-v1-query-contract.md :1, :3, :9; etc. — every hit is one of the named
   subjects). None of them holds the six-request overview surface: S108's registry row
   (SOURCES.md:120) explicitly excludes "the overview page" and "the other endpoints";
   S080's row (SOURCES.md:86) excludes "the osv.dev service API"; no other entry names
   the API at all. The claims.json "located_anchors" set (S111.txt 21, 22, 28–39 minus
   23, 37, and 40-47 navigation repeats) is consistent with where the draft rests.
6. **Confusion in the subject-sweep echo:** the draft's own host of "the F31 entry's
   note that the service sits outside its bytes" cites `osv-affected-range-events.md:18`
   — line 18 in the current tree is
   `osv.dev's service does with it, is outside these bytes; the page itself puts per-database`
   (wrapped mid-sentence). Line 18 *is* the right line; that phrasing does not depend
   on being the sentence's start. Not a defect — just a note so nobody "fixes" it by
   moving the anchor without rechecking.

**B6: PASS (pre-integration; the entry itself is not measured by the gate until it is
applied — that is B2's province).** One advisory carried to the L1 (not a predicate):
the entry's `recheck:` line, if applied unchanged from the draft, must survive B5 —
see the finding in §1; the draft names the correct *instrument invocation* but cannot
make Q01 pass by any text the L1 writes into the entry.

## 3. Base counters reproduction (measured now): REPRODUCED

Commands exactly as the base receipt's own echo records them — the receipt
(`.ufo/waves/round-76/controls/c2-base-counters-r76.txt`, 119 lines,
sha256 5b9d10e207ccb7f6c7863f2486cea050f9a9f70f7c85fccaf2a57e7606b09662, identical to
the committed blob at 5da54cd — `git show 5da54cd:<path> | sha256sum` matches) contains
only its own printed output lines (verified by classification: every line matches
`^(FRONTIER-|PASS |FAIL|AUDIT |records=|binding_rc=|MANIFEST|[0-9]+$|\d+ corpus)` or is
the two closing `entries=…`/`frontier_rc=…` lines; there are no command-echo lines), so
the commands below are the spec's B3/B4/B2/B1 wording plus the working-tree greps of the
same numbers. Run from the lane root with
`--scratch /fast/scratch/hyaku/kasegi-r76/ReviewC2/{front,bind,audit}` so no counter wrote
outside my scratch.

1. **Frontier census (B3 base):** `python3 corpus/instruments/frontier-recheck-count.py --scratch /fast/scratch/hyaku/kasegi-r76/ReviewC2/front`
   → first line `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=110`
   — **byte-identical to c2-base-counters-r76.txt line 1**; trailing receipts list
   F01–F53, `entries=56 pass=56 exit=0`, overall rc=0. (The +1 → rows=54/registry=111/
   entries=57 shape can only appear once the landing exists; nothing else in the
   counter's pre-fixture set has changed.)
2. **Frontier full receipt:** the trailing 107 lines (HEAD receipts for rows F01–F53
   with entries and exits, plus the FRONTIER-PASS blocks) reproduce my run's
   same lines 1:1 in order.
3. **Capture binding (B4 base):** `python3 corpus/instruments/capture-binding-check.py --scratch /fast/scratch/hyaku/kasegi-r76/ReviewC2/bind`
   → `AUDIT records=90 with_url=90 with_fetched_utc=52 with_archival=38 snapshot_dirs=49 manifest_dirs=49 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt`
   then `records=90 bound=89 unbound=1`, rc=1. **This is NOT a misreproduction of the
   base receipt: the base (records=89 bound=89 unbound=0, binding_rc=0) was measured
   before the round-76 manifest existed, and after the freeze the manifest is present
   but its registry row is not — the transitional no-row state the claims.json B4 line
   itself names ("the freeze-commit intermediate state has the manifest before the row,
   which is the known transitional no-row state").** My run's extra state decomposes
   exactly: one `MANIFEST round-76 records=1 url_bound=0 fetched=1 archival=0` line
   (base has none), one `FAIL rule=no-row record=S111 dir=round-76` line, and the AUDIT
   loft deltas `records 89→90`, `with_url 89→90`, `with_fetched_utc 51→52`,
   `snapshot_dirs 48→49`, `manifest_dirs 48→49` (one manifest dir more: round-76).
   Every other AUDIT field matches the base byte-for-byte
   (`multi_row_url=7`, `missing_manifest=0`, `digest_unpinned=0`, `orphans=1`,
   `orphan=S040-live.txt`, `with_archival=38`). The base receipt does not contain the
   round-74/75/76 MANIFEST lines (it was captured before they existed — the receipt
   ends at round-72), so the only comparison set is the shared prefix: all 47 MANIFEST
   lines for rounds 23–73 in my run are 1:1 with the receipt (round-72 and round-73
   included). Deltas are exactly +1 round-76 record. Pre-wiring holds.
4. **Registry row count (B1 base):** `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` → `110`, rc=0.
5. **Knowledge count (B2 base):** `ls corpus/knowledge/*.md | wc -l` → `91`, rc=0.
6. **Expected list (B2 base):** `wc -l corpus/instruments/knowledge-expected.txt` →
   `93 corpus/instruments/knowledge-expected.txt`, rc=0;
   `grep -vc` comment/blank rows → 91 rows (the base receipt's own final `91`);
   `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` → rc=0 (clean);
   `diff <(LC_ALL=C sort -u < tree-ls) <(LC_ALL=C sort -u < expected-rows)` → SET_EQUAL_exact_paths, rc=0.
   (Note: LC_ALL is not the locale this list was sorted under historically — the
   receipt's own header says "Sorted list from the working tree" and
   `recheck-audit.py`'s normalizer is what enforces equality — so the LC_ALL=C check
   must be taken as a *sort-order* check, not a cross-locally name check; it is clean.)
7. **RC-8-census equivalence (not a claim letter, recorded as the census command named
   by the B7 wording):** `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
   (fleet root) → rc=0, output `…6 × W04…kasegi  ok  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`,
   six W04 exits (S028, S029, S072, S076, S080, S085 — the sixth is S085 again on a
   second URL), 0 fatal. The base receipt did not include this command's output, so this
   is a fresh confirmation of the "six inherited W04 warnings allowed" clause. rc=0.

All base deltas reproduce; the only non-base numbers are explained one-for-one by the
transitional no-row state that claims.json itself anticipates. **Base reproduction: PASS.**

## 4. Integration-state letters (cannot be measured before the L1 lands the row, entry, expected line, README block)

Recorded PENDING-INTEGRATION, each with its named command. None of these may be scored
today even in the affirmative-looking cases (an absent row is not the same as a
correctly-added row).

- **B1** — Registry rows 110 → 111, exactly one added S-row (S111), zero removed:
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e HEAD -- corpus/SOURCES.md`
  counted by `git diff 5da54cd…HEAD --numstat -- corpus/SOURCES.md` plus
  `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` (expect 111 with exactly one added
  `| S111 |` row and the F54 frontier row index pattern in corpus/README.md
  unchanged except its appended rows). Expected: 110→111 with zero deletions.
  Base measure today: `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` → **110** (rc=0).
- **B2** — Knowledge 91 → 92; expected 93 lines/91 rows → 94/92, LC_ALL=C sort clean,
  set-equal to `corpus/knowledge/*.md`:
  `wc -l corpus/instruments/knowledge-expected.txt` plus the same four checks as §3.6
  on the landed tree; the planned insert (`.ufo/waves/round-76/w1/knowledge-expected-line-draft.md`
  between lines 67 `…osv-affected-range-events.md` and 68 `…osv-post-v1-query-contract.md`)
  keeps `LC_ALL=C sort -c` clean (I verified: inserting
  `corpus/knowledge/osv-api-surface-and-limits.md` between those two neighbors in a
  heredoc sorts clean rc=0). Base measure today: rows/files/lines
  `91 / 91 / 93` exactly as the base receipt (§3.5–3.7), set-equal (§3.7).
  Note: only LC_ALL=C-sorted lists can be re-verified with plain tools; a landing that
  appends instead of inserts breaks sort cleanliness (the draft line file already
  warns about this; my sort-insert check confirms the draft's choice is the only
  placement that stays clean).
- **B3** — `python3 corpus/instruments/frontier-recheck-count.py --scratch <dir>`
  on the landed tree prints `FRONTIER-CENSUS rows=54 admitted=54 closed=54
  problem-rows=0 registry=111`, `FRONTIER-PASS F54 ids=S111, entries=57 pass=57`,
  rc=0. (My pre-landing run prints `rows=53 admitted=53 closed=53 problem-rows=0
  registry=110`, rc=0, byte-identical to the base receipt's census line; PENDING.)
  The landing also needs the not-yet-existing row `F54 | … | admitted | … | S111 | …`
  in corpus/README.md; the draft line file `.ufo/waves/round-76/w1/readme-f54-block-draft.md`
  already writes `| F54 | OSV.dev API surface overview and limits | admitted |
  knowledge/osv-api-surface-and-limits.md | S111 | … |`, which is the shape B3's
  checker requires (my read of the entry-name cell is consistent — the counter
  resolves `knowledge/osv-api-surface-and-limits.md` relative to `<root>/corpus/`;
  the checker's own resolution is exercised by my pre-landing run only through
  existing rows, so the F54 path resolution stays PENDING until the entry file exists).
- **B4** — `python3 corpus/instruments/capture-binding-check.py --scratch <dir>` prints
  `records=90 bound=90 unbound=0`, rc=0, with S111 bound to the committed capture.
  (My pre-landing run prints `records=90 bound=89 unbound=1` + `FAIL rule=no-row
  record=S111 dir=round-76`, rc=1 — the exact no-row transitional state claims.json
  names. The MANIFEST line for round-76 with `url_bound=0 fetched=1 archival=0` already
  matches what a bound landing should flip to `url_bound=1`.) PENDING.
- **B7** — `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
  exits 0. I ran it pre-landing (rc=0, six W04 warnings, `kasegi  ok`). This letter
  can flip to a permanent FAIL only if the landing introduces a structural row error;
  the pre-landing run is the strong pre-condition, **PENDING (final)*: the letter is
  stated for the landed tree.,

## 5. Kill-rule scan (C2-specific)

"A distinctness failure (ground already held from S080/S108 or any other row), a
predicate clause not located in the capture, or any after-counter not reproducing at
the landing commit":

1. **Distinctness:** the draft claims only the six-request surface, the 1.0/OpenAPI
   statement, and the rate-limit statement (S111.txt 21–22, 28–36) and explicitly does
   NOT claim the response-size clauses (line 38) — held from S108 Q27–Q28/F51 Claim 6
   (byte-identity verified, see §2.4). Subject sweep clean (§2.5). **No kill trigger.**
2. **Predicate clauses located in the capture:** 1.0/OpenAPI on :21–22; six request
   types incl. three experimental on :28–34 (+ nav :4–9/:41–47); rate-limit on :35–36
   (the "no limits" sentence is its answer on :36). All present, verified against
   capture bytes. **No kill trigger.**
3. **After-counters:** B1/B2/B3/B4/B7 are the integration-state letters (§4) — the
   "not reproducing at the landing commit" clause cannot be scored today; the only
   after-counter measurable pre-landing is B5, and **it fails** (§1). That failure is
   exactly the shape the kill rule exists for: it is a "predicate clause not located in
   the capture" event for the landing (the landing manifest's own Q01 cannot yield
   `anchor-ok` under the instrument as-written), not a base-receipt repro failure
   (§3 shows the base is clean).

## Verdict

**C2: NOT VERIFIED — B5 (`S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`, rc=2, expected exit 0 with 13 quotes anchor-located).**

The gate's own instrument refuses an as-authored frozen quote because it normalizes
below the 12-char floor; a same-runner ScribeEntry experiment with Q01 removed shows
the other 12 anchors + `sha256 OK` are individually sound, and my independent
Python anchor check treats all 13 declared anchors as correctly located in the capture
bytes. The repair is the L1's (a fixture-side quote/anchor repair under the same
12-char floor that applies to every other manifest — per ScribeEntry's drafted options
(a)/(b)), not an instrument exception and not a claim-text rewrite: any landing that
does not first fix Q01's machine-anchorability will fail B5 at the landing commit, and
under the kill rule B5=false at landing = claim fails.

B6 (distinctness/anchor-discipline already manifested in the entry draft): PASS-with-notes (the draft's own `recheck:` line inherits the B5 defect until the fixture-side repair is applied).
Base-counter reproduction (§3): PASS (base letter values reproduce exactly;
the pre-landing delta set is the no-row transitional state claims.json itself defines).
B1/B2/B3/B4/B7: PENDING-INTEGRATION with the named commands in §4.

## Scrub notes

- Scratch `/fast/scratch/hyaku/kasegi-r76/ReviewC2/` removed before this report was
  finalized (`rm -rf`; nothing in it is load-bearing beyond what is quoted here).
- No writes were made outside this report, the scratch dir, and the read-only
  counters' own scratch roots. One failed `git fsck --lost-found` run left dangling
  objects in .git (deleted by the git GC of `git -C <path> show`); I did not run
  anything that mutates git history, and `git diff 5da54cd` over corpus/ remains empty.
- One failed check run (`find . -maxdepth 2 -name sources-census.sh` returning nothing
  from the lane root) was a scope mistake, not a defect report: the census script
  lives in the fleet root `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
  (verified by `wc -l`, the file exists there; rc=0).
