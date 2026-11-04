# EntryS098 — F44 entry draft, sentence table, gate block and weakening record

Seat: EntryS098 (leaf scribe, C2/F44). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round 65, wave 1. **Predata build-and-falsify wave: claims are NOT frozen, and nothing
this seat produced is admitted by itself.** L1 (KasegiR65) is the sole production
integrator.

Base master at the time of writing: `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b` (an ancestor
of the lane HEAD `a333d8ef7183a9d8bb969c6ec5c29b8db01f7481`).

## Deliverables

| artifact | path |
|---|---|
| entry draft | `.ufo/waves/round-65/w1/EntryS098/first-psirt-services-framework.md` |
| sentence table (QUALITY R76) | `.ufo/waves/round-65/w1/EntryS098/claim-table.md` |
| Gate block | `.ufo/waves/round-65/w1/EntryS098/gate.md` |
| weakening + correction record | `.ufo/waves/round-65/w1/EntryS098/NOTES.md` |
| manifest-assertions proposal | `.ufo/waves/round-65/w1/EntryS098/manifest-assertions-proposal.json` |
| recheck receipts | `.ufo/waves/round-65/w1/EntryS098/receipts/recheck-committed-18quotes.txt`, `…/recheck-proposal-45quotes.txt` |
| this report | `.ufo/waves/round-65/w1/EntryS098.md` |

No production corpus file was edited. No commit, push, mutating git/jj command, task
dispatch, install or service start was performed.

## Behavior: what the entry holds

The entry is FIRST's **product-side service catalogue** as the S098 capture actually states
it, with three pieces of ground the landed production entry does not carry:

1. **The taxonomy spine**, four levels deep — service area → service → function →
   sub-function (L227) — over six service areas (the first two titled only in prose),
   28 services, 84 functions and 159 sub-function headings.
2. **The maturity definition and the maturity absence.** The capture carries exactly one
   maturity definition (Glossary, L1510) and one measurement statement (L675). It contains
   **no** maturity level vocabulary: `grep -c -iE 'Maturity Level|Level [0-9]'` over the
   document body returns 0. The levels (Basic / Intermediate / Advanced) live in a
   *different* FIRST document that this page only links from its Downloads sidebar — a
   distinction that a package review can get wrong and that a F44 entry must therefore
   state.
3. **The organizational models and the Operational Foundations tiers**, with an explicit
   statement that Strategic/Tactical/Operational are foundation layers and not maturity
   levels.

The entry is bounded against the held rows it could be confused with: F43 (CERT/CC's
phase-to-role matrix — S098 has no phase model and no responsibility matrix, 0 `<table>`
elements), F06/S018 (multi-party coordination guidelines — S098's only FIRST coordination
cross-reference is a footnote URL to the **v1.0** multiparty PDF at L1531), F01 (CVSS),
F19/F20 (EPSS/SSVC), F11/F38 (the ISO records).

## Gates and verification actually run

Every check below was executed by this seat; nothing is reported from another seat's
receipt without being named as such.

**Independent capture.** The seat spec said to use ScoutS098's candidate and `quotes.md`
"when they exist (poll once; if absent, operate from your own independent open of the URL
and say so)". At the first poll, `ScoutS098/S098.candidate.txt` and `quotes.md` did not
exist. This seat therefore made its own open with the lane's instrument:

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py \
  --id S098 --url https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 \
  --out /fast/scratch/hyaku/kasegi-r65/EntryS098/S098.candidate.txt --kind html
```

Output: `status=200 fetched_bytes=229255 snapshot_bytes=170137
sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2 utc=2026-11-04T19:25:39Z`.

**Later, ScoutS098's outputs did appear** (`S098.candidate.txt` and `quotes.md`, written
19:26 and 19:28). This seat then compared: `sha256sum` over Scout's candidate, the L1's
`w1/S098.txt` and the committed `corpus/source-snapshots/round-65/S098.txt` gives the same
digest `cfa42e23…` for all three. Scout's 28 quoted lines were re-verified independently by
this seat (all 28 verbatim at their anchors, declared word counts matching measured counts,
maximum 25 words). Scout's `quotes.md` uses the capture's own line numbers, which is why
this seat's proposal uses the same anchor space.

**Real instrument, committed manifest (unmodified).**

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098
```

→ `S098:sha256 OK` plus 18 `Q…OK` lines, every one `occurrences=1 anchor=N-ok`, `RC=0`.

**Real instrument, this seat's 45-quote proposal.** The shipped
`manifest-assertions-proposal.json` was copied unmodified into a scratch directory beside a
copy of the committed capture and run through the same instrument:

→ `S098:sha256 OK` plus 45 quote lines, `RC=0`. 44 print `occurrences=1 anchor=N-ok`; E35
prints `occurrences=2 anchor=680-ok` (the non-unique quote the instrument's B2 limb resolves
by anchor).

**Sentence-level audit.** 73 rows graded: 61 content, 8 method, 4 cross-reference.
**73 GROUNDED, 0 OVERREACH, 0 UNGROUNDED.** Every quote is a verbatim substring of its
anchored line, ≤25 whitespace-delimited words (maximum 25, at E09 and E10), and ≥12
normalized characters — the `source-recheck.py` floor. Every inline quotation in the entry
draft was mechanically re-checked against the proposal and the capture: 0 mismatches, and
all 45 proposal ids are cited by the entry.

**Counts and absences**, each re-measured over the document body L216-L1536 and, where the
sentence says "the capture", over the whole file: service areas 6 / services 28 /
functions 84 / sub-function headings 159; `shall` 0; `conform` 0; `safe harbor` 0;
`Maturity Level|Level [0-9]` 0; `SSVC` 0; `EPSS` 0; numeric intervals 0; `certification` 3;
`compliance` 6; `should` 138 occurrences on 109 lines; `must` 30 on 25; `phase` 3; `role` 14;
`CVSS` 4; `<table>` 0; `<img>` 30; 40 `Figure N:` caption lines over 20 distinct figures.

**Not run by this seat:** any frontier counter, census, claim-package gate, freeze check,
capture-binding check or score movement. No score is claimed, and no admission is claimed.

## Findings — for the L1

**F-1 (material). The committed manifest's `body_lines: [216, 1450]` excludes the Glossary,
where the capture's only maturity definition lives.** The range stops inside Annex 2
(Acknowledgements, L1448-L1466), so it omits the Glossary (L1498-L1512) — and with it
L1510 — plus Annexes 3/4/5 and the Annex 1 supporting-resources list (L1440-L1447) whose
ISO edition years the entry's date analysis depends on. The recheck instrument does not
enforce `body_lines`, so the existing 18 assertions are unaffected and the committed
manifest still passes (`RC=0`). But a reader who treats `body_lines` as "the document body"
will conclude the Glossary is not part of S098, which is false. Two remedies, both
harmless to the existing assertions: widen to `[216, 1536]` and merge this seat's
proposal; or leave the range and note in the entry that the maturity definition sits
outside it. **This seat did not edit the manifest** — it is L1's production surface.

**F-2 (material). The production F44 entry and the F44 row already landed during this
seat's run.** Commit `1c36d72` ("round-65: land signal-fail-closed derive gate and F44 PSIRT
services catalogue") added `corpus/knowledge/first-psirt-services-framework.md`, the capture,
the manifest and the `| F44 |` frontier row; `a333d8e` followed. This seat did not produce
that entry and does not claim it was derived from this draft. **This seat audited it
instead** (read-only): its 18 quoted fragments were extracted mechanically and each checked
verbatim at its declared anchor with its declared word count — **18/18 pass**, no
OVERREACH, no UNGROUNDED, no anchor failure, maximum 18 words.

Two substantive differences between the landed entry and this draft, for the L1's decision:

- The landed entry's scope is the **intake → qualification → reproduction → disclosure
  chain**; it does not mention maturity at all — neither the Glossary definition nor the
  absence of levels. A reader of the landed entry can therefore carry "FIRST defines
  maturity levels for a PSIRT" out of it without any sentence contradicting it. This draft
  closes that gap (its own §Maturity and the maturity rule).
- The landed entry's header says "content lines 216-1450" and its Scope bullet says "the
  capture includes the site's navigation above line 216, so only content lines are cited" —
  but the manifest's declared range ends at L1450, which excludes the Glossary. The landed
  entry's own citations happen to sit at L1 and L219-L1231, so nothing it cites is
  affected; the header's line range is nonetheless wider than the manifest's declared
  body. This draft states the body as L216-L1536 and marks L1537-L1573 as chrome.

**F-3 (minor). The maturity document is a live, distinct FIRST document, and it is the
natural home for the level ladder.** This seat opened it read-only:
`https://www.first.org/standards/frameworks/psirts/psirt_maturity_document`, HTTP 200,
82978 bytes, sha256 `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e`. Its
text carries "Maturity Level 1 (Basic)", "Maturity Level 2 (Intermediate)", "Maturity
Level 3 (Advanced)" and "Beyond 'Level 3'". If the L1 wants level ground, that is a new
source id, a new manifest and a new entry — not an extension of S098.

**F-4 (minor, hygiene). The landed entry's `| F44 |` row and the `| S098 |` registry row
are both present, and the S098 row's recheck cadence is `90d` while comparable tier-A
documentation rows in the registry use `180d`.** Not this seat's call; flagged because the
page is mutable and unversioned in its prose (the URL embeds `v1.1`, but the prose can
change under it).

## Errors this seat caught in its own draft

Recorded in full in `NOTES.md` Part 2. Six sentences were written, then refuted by
re-measurement and corrected — all before delivery:

1. "0 occurrences of 'days'/'week'/'deadline'" — false; the body has 7, all in the idiom
   "day to day" / "every day" / "day of advisory publication" / "zero-day". The surviving
   claim is stronger: **no numeric interval** appears anywhere.
2. "the only date in the capture is the copyright range" — false; 12 body lines carry
   ISO edition years (2002, 2009, 2013, 2014, 2018). The entry now distinguishes them.
3. "no certification or compliance vocabulary" — false; 3 and 6 occurrences. The entry now
   names them and their sense.
4. "'should' occurs 109 times … 'must' 25" — line counts presented as occurrence counts;
   the real figures are 138 and 30. Both are now stated and labelled.
5. "`grep -c 'Role'` → 2" — case-sensitive, omitting that lowercase "role" occurs on 14
   body lines. The claim is about the absence of a *matrix*, and now says so.
6. The body range and the Downloads sidebar — the first draft called L216-L1548 "the body"
   and treated the sidebar as document content; the served HTML's `<div id="sidebar">`
   opens after the last content line, so L1537 onward is chrome.

Separately, the entry's inline quotations had their curly apostrophes normalised to
straight ones on write (`stakeholder's`, `'case'`), which broke verbatim match against the
capture on three quotations (E06, E17, E23). Caught by the mechanical re-check and
restored.

## Touched surfaces

Written, all inside this seat's own directory:

- `.ufo/waves/round-65/w1/EntryS098/first-psirt-services-framework.md`
- `.ufo/waves/round-65/w1/EntryS098/claim-table.md`
- `.ufo/waves/round-65/w1/EntryS098/gate.md`
- `.ufo/waves/round-65/w1/EntryS098/NOTES.md`
- `.ufo/waves/round-65/w1/EntryS098/manifest-assertions-proposal.json`
- `.ufo/waves/round-65/w1/EntryS098/receipts/recheck-committed-18quotes.txt`
- `.ufo/waves/round-65/w1/EntryS098/receipts/recheck-proposal-45quotes.txt`
- `.ufo/waves/round-65/w1/EntryS098.md` (this report)

Scratch: `/fast/scratch/hyaku/kasegi-r65/EntryS098/` (created explicitly; the one shared
clone was not needed — no git fixture was used). It held the independent capture, the raw
HTML, the maturity-document cross-check and the manifest-recheck test directory.
**Removed on exit** (`rm -rf`, verified absent) after the receipts were copied into
`.ufo/waves/round-65/w1/EntryS098/receipts/` — the two `source-recheck.py` transcripts
(18-quote committed manifest and 45-quote proposal), both ending `RC=0`. The receipts, the
digests and the command outputs printed in this report, the gate block and the claim table
are self-contained.

Not touched: `corpus/instruments/`, `corpus/knowledge/`, `corpus/SOURCES.md`,
`corpus/source-snapshots/`, `corpus/README.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
`PROVINCE.md`, `QUALITY.md`, the fleet repo, sibling lanes, any domain source tree, and
every PATH directory. The production `corpus/knowledge/first-psirt-services-framework.md`
was **read** for audit purposes and not edited.

## L1 decisions on this seat's findings (received 2026-11-04, verified against the bytes)

The L1 (KasegiR65) answered this seat's report with decisions on all four findings and
recorded them in the working tree. **Verified by this seat against the files, not taken on
trust:**

| finding | L1 decision | verified state |
|---|---|---|
| F-1 | accepted; landed | manifest `body_lines` widened `[216, 1450]` → `[216, 1536]`; entry header reads "content lines 216-1536"; new QUALITY rule **R90** ("a capture's declared body range is read from the document's own structure … and a range that ends inside an annex is a defect"); lesson **M65-9** records it, citing this seat's `gate.md` and `manifest-assertions-proposal.json`. Commit `1929a474` + the working-tree edit. Recheck over the widened manifest: `S098:sha256 OK` + 18 `Q…OK`, `RC=0`. |
| F-2(a) | accepted; a Limits bullet added | Present in the working-tree entry: "**Maturity is a glossary definition, not a level ladder.**" — but see the conflict below. |
| F-2(b) | accepted; fixed with F-1 | The Scope sentence now reads "the capture includes the site's navigation above line 216, so **only the title line (L1, the document's own title) and content lines are cited**" — the L1-title exception is now named explicitly. |
| F-3 | recorded as an unopened lead, no row | Present in `corpus/SOURCES.md`: "Lead added (round 65, not admitted): FIRST PSIRT Maturity document at https://www.first.org/standards/frameworks/psirts/psirt_maturity_document … sha256 `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e`" — this seat's measured digest, carried forward. |
| F-4 | accepted; cadence 90d → 180d | Present: the S098 registry row's recheck cell now reads `180d`, with "S098 recheck cell old → new: `90d` → `180d`" logged in Registry changes. |
| — | the 45-quote proposal deliberately **not** merged | The L1's reason: C2's frozen predicate pins "18 anchored quotes" in the committed manifest, and merging would make the counter print 63 against a frozen record of 18. The proposal is retained as corroborating evidence at `w1/EntryS098/manifest-assertions-proposal.json`. The committed manifest still carries exactly 18 assertions and still passes the recheck. |

### Conflict found in the L1's newly added maturity bullet — reported, not edited

The L1's bullet states: "S098's **only maturity statement** is the glossary entry at L1510
… the capture states no maturity levels, no level names **and no assessment method**
(measured: `grep -cE 'Maturity Level|Level [123]'` over the capture = 0)."

Two of its three negatives are false, and the measurement it cites cannot carry them:

- **"no assessment method" is false.** L675 states one: "Maturity of a PSIRT may be measured
  via the availability and efficiency of the difference services prescribed in this service
  area" (the source's own "difference services" typo). Verified: the body has exactly five
  lines mentioning maturity — L274 (prose), L403 ("the maturity lifecycle of the PSIRT"),
  **L675 (the measurement statement)**, L1499 (the glossary entry for "Actions"), L1510
  (the definition).
- **"only maturity statement" is false for the same reason** — L675 is a second maturity
  statement. The defensible claim is "only maturity *definition*".
- The cited `grep -cE 'Maturity Level|Level [123]'` = 0 (confirmed 0 both over the whole
  capture and over the body L216-L1536) supports "no maturity levels" and "no level names"
  only; it says nothing about assessment methods.

A minimal correction keeping the bullet's purpose was sent to the L1: "only maturity
*definition*" for the first clause, and the L675 measurement stated rather than denied.
This seat did **not** edit the landed entry — it is L1's production surface. The conflict
was reported to `agent://KasegiR65` on 2026-11-04 with the source lines quoted verbatim.

This is the same failure mode as F-1, on the claim axis rather than the capture axis: a
negative a reader could quote back ("FIRST gives a PSIRT no way to assess maturity") where
the page in fact says maturity may be measured via service availability and efficiency.

**Status update: the overreach is now COMMITTED.** Commit `2cf5039` ("round-65: record
maturity limits, cadence cell and the final tip receipt", 2026-11-04 16:53:04) landed the
bullet with the overreach intact — `git show HEAD:corpus/knowledge/first-psirt-services-framework.md`
still contains "no assessment method". This seat's correction was delivered to
`agent://KasegiR65` in the same minute and raced the commit; the working tree is clean for
`corpus/`, so no fix is pending. The finding stands as an open item for the L1 or the
closure: the bullet's second and third negatives are contradicted by L675 of the very
capture it cites, and its cited measurement supports only the first.

### One correction to the L1's reply

The L1's message states this seat's draft is "74/74 grounded". The claim table has **73**
graded rows (61 content + 8 method + 4 cross-reference), all GROUNDED. The 74 comes from a
`grep -c GROUNDED` that also matches this seat's own summary row; the row count is 73, as
the table's summary and this report both state.

## Limits and handoff

- **Nothing here is admitted by itself.** This is a predata wave. The L1 decides whether
  the entry draft, the 45-quote manifest proposal, the `body_lines` widening (F-1) or any
  part of this seat's audit of the landed entry lands.
- **The audit of the landed entry (F-2) is this seat's own work, not a gate.** It is a
  sentence-level quote audit (18/18 quotes verbatim, counts matching); it is not a claim
  about whether the landed entry's *interpretation* is right, and it is not an
  independent admit/reject judgment — that remains the closure's responsibility.
- **Byte-identity is reproducibility, not meaning.** Three independent fetches produced
  sha256 `cfa42e23…`; that shows the served bytes reproduce, not that the document says
  what this seat reads it to say.
- **The maturity levels were not admitted.** They are in a separate document this seat
  fetched read-only but did not capture, register or write an entry for.
- **The `E01`-`E45` quote ids are this seat's own.** They are not in the committed
  manifest and would need merging under whatever ids the L1 chooses; the anchor space is
  the capture's line numbers either way.
- **No conflicts with the canonical assignment were observed.** The assignment's C2 —
  "frontier F44 to be admitted on S098, FIRST's PSIRT Services Framework v1.1,
  distinguished from F43 (CERT/CC CVD phases/roles) and F06/S018 (multi-party
  coordination)" — is what this draft holds: F44 on S098, with both distinctions stated
  and grounded.

## Deliverable self-evaluation (not a gate)

| axis | score | evidence / limit |
|---|---:|---|
| accuracy | 4 | 45/45 quotes verbatim at their anchors under the real instrument, 73/73 rows graded with 0 overreach; six own-draft errors caught and corrected before delivery. |
| completeness | 4 | Entry, sentence table, gate block, weakening/correction record and a manifest proposal delivered; the landed production entry was audited but not edited. |
| clarity | 4 | Entry separates source teaching, package rules, rejected readings and limits; the maturity distinction is stated where a reader would otherwise be misled. |
| actionability | 4 | The 45-quote proposal is instrument-verified and ready to merge; F-1 gives the L1 two named options with their consequences. |
| conciseness | 4 | No production edit; every claim carries one anchor; the report names the checks run and the ones not run. |

Overall 4.0/5. Highest-impact remaining work is the L1's integration decision on F-1 and
F-2, not more execution by this seat. Self-check: the deliverables meet the requested draft
scope without claiming admission or integration success.

Report: .ufo/waves/round-65/w1/EntryS098.md
