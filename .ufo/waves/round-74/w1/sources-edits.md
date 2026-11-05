# sources-edits — corpus/SOURCES.md, round 74 (DRAFT by seat ScribeLesson)

The L1 applies these by hand in one commit with the entry and manifest. Line numbers are the base-tree numbers measured by this seat (`grep -n '^## '` on `corpus/SOURCES.md`: Registry 3, Paths 122, Search log 131, Leads 170, Registry changes 174; S108 row 120; Round-70 search entry 168; Fuzzilli lead 172; file ends at 266). Apply in the order listed; each insertion is below the one before it, so later numbers do not move.

## 1. Registry row S109 — insert after line 120 (the S108 row); no other row changes

Insert this single line, 11 cells, no `|` inside any cell:

```
| S109 | googleprojectzero/fuzzilli README, "Fuzzilli: A JavaScript Engine Fuzzer" — https://github.com/googleprojectzero/fuzzilli | docs | A | The Fuzzilli project's own README statements about its design and scope: what it is, its FuzzIL mutation model, the Swift/C split, components, REPRL execution, instance tree, targets and the NDSS 2023 paper's existence; not Project Zero's comparison post (S093), not the paper's content, not any listed CVE | README L151 self-description, L154-L156 Targets/ and coverage build, L165 semantic correctness, L212-L221 Swift/C split and components, L226-L227 Storage and event-driven design, L230 REPRL, L233-L236 instance tree, L243 NDSS 2023 paper; GitHub page captured 2026-11-05, corpus/source-snapshots/round-74/S109.txt, sha256 c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486, 375 lines | The project's own README is the primary statement of what Fuzzilli is and how its fuzzer is organised: read FuzzIL mutation, REPRL state reset and the instance tree as the tool's documented design, separate from third-party comparisons of it | mined | 2026-11-05 | 90d | corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md |
```

Cell check (run by this seat on this draft's row, see the report): 11 cells between the outer pipes, none containing `|`.

Old line 120 (S108 row) is byte-identical after the insert.

## 2. Search log paragraph — insert after line 168 (the Round-70 entry); line 169 stays blank

```
- Round-74 bounded documentation-ground screen, 2026-11-05: question — does the lane hold the Fuzzilli tool's own documentation ground (the project's README: what the fuzzer is, its design and its scope), which Frontier F41 (S093, Project Zero's comparison) and the round-60 and round-61 lessons only cite second-hand? Where — the named lead at line 172 (`https://github.com/googleprojectzero/fuzzilli`); a sibling sweep, `grep -rliI fuzzilli` over corpus/, PROVINCE.md and README.md (hits: the S093 knowledge entry, its round-60 snapshot and manifest, the round-60 and round-61 lessons, the round-73 lesson, the README F41 row, this file, knowledge-expected; no held README or tool-documentation capture), and `considerthese/` (no match, exit 1); date 2026-11-05; identified 1 (S109), screened 1, included 1 (S109, F52), excluded 0 documents, with no exclusion reasons because the one screened document was admitted. The OSV overview page and the NDSS 2023 paper were not screened in this search (the first is a round-73 lead, the second is outside the frozen scope). Stop rationale: frozen scope (claims.json C2 scope_limit: the project's own README and documentation statements only; no Project Zero comparison, no Big Sleep, no NDSS content, no CVE specifics, no live fuzzing).
```

## 3. Leads (unopened) — insert after line 172 (the Fuzzilli lead, kept byte-identical)

Line 173 is the existing blank line. Insert these two bullets, separated by a blank line, after line 172 and before the blank line that already precedes `## Registry changes`:

```

- OSV.dev overview page at https://google.github.io/osv.dev/api/ — lead, not evidence: opened lead-only for the round-73 bullet (R73-V2), not captured or admitted, so no row exists. Its two statements, quoted verbatim from the page's fetch (round-74 scout receipt `.ufo/waves/round-74/w1/ScoutSurface.md` §5; fetched 2026-11-05T08:43:42Z UTC, HTTP 200), are "Currently there are no limits on the API." (rate limit) and "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." (response size); they are named here as lead statements only. The 32 MiB HTTP/1.1 limit on POST /v1/query is admitted separately under S108; the overview's statements are not, and must not be cross-referenced as F51 evidence. Flip: a round that needs these statements as admitted ground opens the page with its own capture and manifest.

- NDSS Symposium 2023 paper about Fuzzilli and how it compares to other fuzzers, named at line 243 of the S109 capture — unopened; outside the frozen round-74 scope, which claims its existence and name only; the S109 capture gives no URL for it. Lead, not evidence. Flip: a round that needs its content as admitted ground opens it with its own capture and manifest.
```

## 4. Retired Fuzzilli lead — annotation only, appended after line 266 (the round-73 S108 bullet) in `## Registry changes`

Line 172 is NOT edited. The annotation:

```
- Lead retired old → new (round 74, F52 admission): `- Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.` (corpus/SOURCES.md:172) is kept byte-identical as history and is retired as opened: the project's README is now S109 (docs, tier A scoped, mined, opened 2026-11-05), held as Frontier F52 in corpus/README.md with the entry corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md. The NDSS 2023 paper that the same README names stays a lead in its own bullet above.
```

## 5. Registry changes — census and row counts, appended after the retired-lead annotation

```
- Round-74 S109 added (docs, scoped tier A, mined, opened 2026-11-05, recheck 90d, used-by corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md). Registry 108 -> 109; no pre-existing status, recheck, used-by, id or URL cell changed. Anchor pinned to the round-74 capture corpus/source-snapshots/round-74/S109.txt (sha256 c9a7adfb...d486, 375 lines).
- Census before -> after: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 before (`kasegi ok`, six inherited W04 warnings S028 S029 S072 S076 S080 S085) and exit [L1 measures after] after. Recorded in the round-74 lesson.
```

## Checks the L1 runs after applying (not run by this seat; listed so the L1 can verify)

- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 109 (base 108).
- `sed -n '120p;121p' corpus/SOURCES.md` shows the S108 row then the S109 row (line 121).
- `sed -n '172p' corpus/SOURCES.md` is byte-identical to the base line 172.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 once `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` exists (the mined used-by path must resolve).
