# ScribeEntry — round-78 wave-1 seat report (F54 knowledge entry draft)

Scope: C2 (coverage) only. This seat drafts the F54 knowledge entry for the L1 to land verbatim if it passes. It does not land it, does not edit the lane tree outside this wave dir, and does not touch the C1 counter.

## Files written

| path | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-78/w1/c2/osv-post-batch-query-contract.md` | 12,893 | `78cd76babc3589000f2c7fa9f71460b43eb271bc41f178d36daaa5c9b5a8d438` |

Word count (`wc -w`): **1816** (91 lines). The draft is the entry body only; the L1 lands it at `corpus/knowledge/osv-post-batch-query-contract.md`.

## Entry shape (mirrors the admitted sibling `corpus/knowledge/osv-post-v1-query-contract.md`)

H1 title; three header lines (`source: S112 — <url> (anchor: …)`, `verified-at: 2026-11-05`, `recheck: cd … && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112`); `## Attribution`; five `## Claim N` sections in the sibling's prose form (each = a quoted sentence + `Falsifiable rule:` + `Rejected over-generalization, not a page sentence:`); `## Distinctness`; `## Not claimed`; `## Gate — S112 (OSV.dev POST /v1/querybatch)` with the URL, the access date, the capture digest, and the seven located quotes in a pipe-free table; `## Limits`; and a closing scope-limit sentence.

The `source:` line names S112 and only S112. The `recheck:` line is character-exact as specified (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112`), verified with `cat -A` — no trailing comment, no escaped pipe, one shell command.

## Seven quote-to-line map (all verbatim at the stated line; word counts by `wc -w`)

| clause | manifest pin | snapshot line | words | quote |
|---|---|---|---|---|
| C1 batch definition | Q01-batch-definition | S112.txt:24 | 15 | Query for multiple packages (by either package and version or git commit hash) at once. |
| C2 return shape | Q02-return-shape | S112.txt:24 | 7 | Returns vulnerability ids and modified field only. |
| C3 ordering | Q03-ordering | S112.txt:24 | 10 | The response ordering will be guaranteed to match the input. |
| C4 partial next_page_token | Q09-partial-tokens | S112.txt:166 | 18 | However, a querybatch request may return results with a next_page_token for only a few of the total queries. |
| C5 per-query count | Q10-individual-1000 | S112.txt:168 | 11 | An individual query within the queryset returns more than 1,000 vulnerabilities |
| C6 queryset count | Q11-total-3000 | S112.txt:169 | 9 | The entire queryset returns more than 3,000 vulnerabilities total |
| C7 follow-up request | Q13-next-request | S112.txt:195 | 20 | To get the next page of results, your next request should specify page_token only for the queries that returned next_page_token. |

All seven are ≤25 words (longest 20). Word counts are measured with `wc -w` on the quoted text, per QUALITY R56 — not hand-typed.

## Recheck result (the seat's required check)

The recheck line was run **verbatim** from a scratch copy of the lane (`$S/copy`, an exact tar copy of `/home/vgpnk/Projects/shokunin/kasegi-shokunin` excluding `.git`/`.jj`), never against the lane tree, with `TMPDIR=$S/tmp`:

```
$ cd $S/copy && bash -c 'cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112'
S112:sha256 OK
S112:Q01-batch-definition OK occurrences=1 anchor=24-ok
S112:Q02-return-shape OK occurrences=1 anchor=24-ok
S112:Q03-ordering OK occurrences=1 anchor=24-ok
S112:Q09-partial-tokens OK occurrences=1 anchor=166-ok
S112:Q10-individual-1000 OK occurrences=1 anchor=168-ok
S112:Q11-total-3000 OK occurrences=1 anchor=169-ok
S112:Q13-next-request OK occurrences=1 anchor=195-ok
rc=0
```

The identical run inside the copy (manifest read from the copy) prints the same eight lines, rc 0. **The recheck passes: 7/7 pinned quotes, all `occurrences=1`, all anchors exact, sha256 OK, exit 0.** This matches the committed pre-freeze receipt `.ufo/waves/round-78/controls/c2-prerecheck-r78.txt` byte for byte.

## Other instrument runs (scratch copy only, entry landed in `$S/copy/corpus/knowledge/`)

The landing was simulated in the copy only (entry file + one `| F54 | … | admitted | knowledge/osv-post-batch-query-contract.md | S112 |` row appended to `corpus/README.md` after the F53 row + the entry added to `corpus/instruments/knowledge-expected.txt`). The lane tree was not modified.

| instrument | command | result |
|---|---|---|
| `frontier-recheck-count.py` | `python3 corpus/instruments/frontier-recheck-count.py` | `FRONTIER-CENSUS rows=54 admitted=54 closed=54 problem-rows=0 registry=112`, `FRONTIER-PASS F54 ids=S112`, exit 0 |
| `anchorcheck.py` | `python3 corpus/instruments/anchorcheck.py corpus/knowledge/osv-post-batch-query-contract.md` | 10 in-range cite instances, 0 bad, 9 distinct anchors, exit 0 |
| `recheck-cwd-census.py` | `python3 corpus/instruments/recheck-cwd-census.py --root $S/copy --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin` | `RECHECK-CWD entries=92 noprefix=0 exit2_foreign=0 exit0_foreign=70 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`, `RECHECK-CWD-RESULT conformant`, exit 0 |
| `capture-binding-check.py` | `python3 corpus/instruments/capture-binding-check.py --root $S/copy` | `records=92 bound=92 unbound=0`, exit 0 |
| `recheck-audit.py` | `python3 corpus/instruments/recheck-audit.py --root $S/copy` | `lines=92 total=92 pass=92 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0`, `expect=present expected=92 missing=0 unexpected=0`; exit 1 because `strict pass=0/92 cdroot_fail=92` — see finding F1 below (the same `strict pass=0/91 cdroot_fail=91` reads at the unmodified base, so the entry adds no new failure) |

The `recheck-audit.py` and `recheck-cwd-census.py` runs against the **unmodified lane** (`--root /home/vgpnk/Projects/shokunin/kasegi-shokunin`) read `strict pass=91/91 cdroot_fail=0` and `lines=91 total=91 pass=91 … exit=0` — i.e. the lane is green on the base and the entry's own line passes the same limbs.

## Distinctness (the round-77 rejection reason)

The round-77 closure rejected C2 because three of the thirteen clauses restated admitted F51. This draft claims **only** the seven batch-specific clauses and names the other six in one `## Not claimed` line with their F51 cross-reference (`corpus/knowledge/osv-post-v1-query-contract.md:21`, `:47`; `S108.txt:40,41,136`):

- Q04 parameters pointer (S112.txt:31), Q05 instructions pointer (S112.txt:32), Q06 item-rules pointer (S112.txt:34) — cross-references to the single-query contract, not restatements of it.
- Q07 version rule (S112.txt:35), Q08 400 consequence (S112.txt:36), Q12 threading-variance note (S112.txt:170) — restatements of F51 ground, cited as held, not claimed.

Measured checks:

- **B6 quote-absence:** for each of the seven claimed quotes, `grep -F -l -- "<quote>" corpus/knowledge/*.md | grep -v osv-post-batch-query-contract | wc -l` → **0** for all seven.
- **The six not-claimed clauses are not quoted anywhere in the draft**: `grep -c -F` for each of the six sentences → **0** hits each.
- **Subject sweep:** `grep -rli -i 'osv' corpus/knowledge/*.md` returns five admitted entries (fuzzilli-js-engine-fuzzing-framework, github-advisory-database-curation-semantics, openssf-scorecard-checks, osv-affected-range-events, osv-post-v1-query-contract). The OSV ground among them is the single-query contract (F51), the record format (F31) and Scorecard's use of the OSV service (`corpus/knowledge/openssf-scorecard-checks.md`, S086); the other two mentions are a format statement deferring to F31 and a distinctness line. None states a clause of this page.
- **The one real overlap is the number 1,000.** F51 holds the single-query pagination trigger ("more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds", `corpus/knowledge/osv-post-v1-query-contract.md:47`, quoting S108.txt:136); the count claimed here is scoped to one query *inside a queryset* (S112.txt:168), and the 3,000 figure has no counterpart in F51 at all (`grep -c '3,000' corpus/knowledge/osv-post-v1-query-contract.md` → 0). The draft states this scope difference explicitly in `## Distinctness` so a reader can check that the overlap is a different scope, not the same ground twice. The per-query scope is the batch-specific clause the frozen C2 statement names ("the 1,000-per-query and 3,000-total thresholds (Q10, Q11)").

## Scope discipline

Every factual sentence carries an `S112.txt:<line>` citation; the only non-S112 citations are the sibling/registry paths and the two sweep commands, each named where used. No claim beyond the seven clauses: the two located-but-unpinned sentences (S112.txt:167, the pagination-condition lead-in, and S112.txt:194, the distinct-token sentence) are named in `## Limits` as located but not clause-grounded; the request/response JSON examples and the payload shape are named as not claimed.

No literal or escaped pipe character appears in any table cell (verified programmatically over all 9 table lines: 0 cells contain `|` or `\|`).

## Findings

**F1 (informational, not a defect in the draft) — `recheck-audit.py`'s `cdroot` limb is a copy-path artifact.** In `$S/copy` the audit reads `strict pass=0/92 cdroot_fail=92`; the **unmodified** base copy reads the same `strict pass=0/91 cdroot_fail=91`, and the **unmodified lane** reads `strict pass=91/91 cdroot_fail=0`. The limb compares the `cd` target in the recheck line against the audited root, so it fires for every entry whenever the audited root is not the lane root. The entry's line uses the canonical lane root (the same target every one of the 91 admitted entries uses), so it will pass the limb once landed in the lane. No other limb fails for the draft: `parse_fail=0 cwd_fail=0 paths_fail=0 own_fail=0`.

**F2 (routed, informational) — `POST /v1/querybatch` is a GONE path-like token under `resolve.py`.** The draft backticks the endpoint path string (as the sibling does for `POST /v1/query`). `resolve.py` classifies `POST /v1/querybatch` as GONE/rel — the identical, pre-existing verdict for `POST /v1/query` (base census row: `POST /v1/query GONE 2 files`, `POST /v1/querybatch GONE 1 file`). This is the same noise class the sibling already carries; it is not a new class member and is not a claim.

**F3 (routed, informational) — `citation-ground-check.py` reads `verdict=failed` on the base as well as on the copy.** The failures are pre-existing `blocked-protected-fleet-relative` rows over `corpus/lessons/*` and `scripts/`, not over this entry; the base copy produces the same verdict, so the entry adds no new member.

**F4 (design note for the L1) — the `## Not claimed` line names S112.txt lines for six clauses that are not claimed.** That is deliberate: the reader must be able to see *which* six sentences were dropped and where they sit, and each is named with its line so the exclusion is checkable rather than asserted. The line carries the F51 cross-reference the frozen C2 statement specifies (`corpus/knowledge/osv-post-v1-query-contract.md:21,47; S108.txt:40,41,136`). Note the anchor `corpus/knowledge/osv-post-v1-query-contract.md:21,47` is written as two separate one-anchor cites (`:21` and `:47`) rather than one comma list, because QUALITY's citation-bases rule 5 (`corpus/knowledge/citation-bases.md:104`) states that one cite per anchor is the convention and comma-anchor lists defeat the resolver — `resolve.py` classifies `…md:21,47` as GONE, while the two single anchors classify INTERNAL.

## Out of scope for this seat (left to the L1)

- Landing the entry at `corpus/knowledge/osv-post-batch-query-contract.md`.
- The `| F54 |` row in `corpus/README.md` (six-cell shape, `admitted`, `knowledge/osv-post-batch-query-contract.md`, `S112`, evidence cell).
- The `corpus/SOURCES.md` S112 row flip `queued -> mined` with `used-by` naming the entry (the registry row currently sits at `corpus/SOURCES.md:124`).
- Adding the entry to `corpus/instruments/knowledge-expected.txt` (91 → 92 entries; 93 → 94 lines).
- The round-78 lesson's Gate section recording the C2 admission.

## Reproduction

Scratch root: `/fast/scratch/hyaku/kasegi-r78/ScribeEntry/` (`copy/` = exact lane tar copy excluding `.git`/`.jj`, `tmp/` = TMPDIR for every run). No counter output was written outside it. No git or jj command was run against the lane, the fleet repo, or any sibling lane. No tool was installed or upgraded by this seat.
