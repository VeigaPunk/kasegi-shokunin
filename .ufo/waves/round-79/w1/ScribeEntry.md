# ScribeEntry — round 79 w1, C2 draft (F55 / S113)

Scope: draft only. No lane file was edited; the four artifacts are under `.ufo/waves/round-79/w1/c2/`. No git/jj write, no scratch dir created (all measurement read-only on committed bytes), no tool installed.

## Behavior

Drafted the round-79 C2 admission for Frontier F55 on source S113 (OSV.dev `POST /v1experimental/determineversion`): the knowledge entry, its SOURCES registry row, the README coverage-map frontier block, the PROVINCE end-of-file amendment line, and the `knowledge-expected.txt` successor.

## Artifacts (all absolute)

| path | what |
|---|---|
| `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/c2/osv-determineversion-cc-library-versioning.md` | the entry: 8 claims, one per pinned quote; header `source:`/`verified-at: 2026-11-06`/`recheck:`; Attribution; Distinctness; Not claimed; Gate (8-row table); Limits (6 greps that print nothing); Scope limit |
| `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/c2/SOURCES-S113-row.md` | the S113 registry row, 11 cells, `queued`->`mined` and `—`->`corpus/knowledge/osv-determineversion-cc-library-versioning.md`, nothing else changed |
| `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/c2/README-F55.md` | round-79 admission block, 3-column coverage-map row, 6-column F55 frontier row, `[r79 amendment]` line, and the PROVINCE end-of-file F55 line in the r78 shape |
| `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/c2/knowledge-expected.txt` | 95 lines / 93 `.md` rows, new row inserted in `LC_ALL=C` order |
| `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/ScribeEntry.md` | this report |

## Gates exercised (observed, this seat)

1. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-79/manifest.json --source S113` -> `S113:sha256 OK` plus 8 lines `S113:<pin> OK occurrences=1 anchor=<n>-ok`, anchors 25/41/41/55/61/62/66/85, rc0. (B0 sub-check; the lane's own B5/B7 runs remain the L1's.)
2. Byte-substring test in python over `S113.txt` split on `\n`: each of the 8 manifest quotes is present exactly once on its declared line; every quoted span in the entry is one of those 8 at its pinned line (the only other quoted span is F51's own Limits bullet, verified byte-equal against `corpus/knowledge/osv-post-v1-query-contract.md:75`).
3. Word counts by `wc -w` equivalent (`len(quote.split())`) for all 8: 19, 18, 12, 22, 14, 7, 11, 14 — all <= 25, and each equals the words column written in the Gate table.
4. Each of the 6 Limits greps run literally from the lane root: rc=1, zero bytes of output, for `rate limit|ratelimit|quota|api key|api_key|authenticat|credential`, `paginat|page_token|next_page_token`, `timeout|limit|maximum`, `severity|CVE|cvss`, `error|status code|throttl`, `worker|thread|proxy`.
5. `grep -rli 'determineversion\|indexer' corpus/knowledge/` -> no output, rc=1 (reported in the entry's Distinctness bullet). Note this is why the Distinctness argument cites F51 `:75` by its "experimental endpoints" wording rather than by the endpoint name: no admitted entry carries the string.
6. `knowledge-expected.txt` successor: 95 lines, 93 `^corpus/knowledge/.*\.md$` rows, `grep ... | LC_ALL=C sort -c` clean, and `diff` against the lane file shows exactly one added line (`corpus/knowledge/osv-determineversion-cc-library-versioning.md`, between `osv-affected-range-events.md` and `osv-post-batch-query-contract.md`).
7. `SOURCES-S113-row.md`: split on `|` gives 13 fields = 11 cells; field diff against `corpus/SOURCES.md:125` is `[8, 11]` only.
8. Table shapes in `README-F55.md`: coverage map 4 pipes, frontier row 7 pipes — identical to the F54 block at `corpus/README.md:1196,1198,1201`.

## Touched surfaces

Read-only: `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `corpus/instruments/knowledge-expected.txt`, `corpus/knowledge/{osv-post-v1-query-contract,osv-post-batch-query-contract,osv-affected-range-events}.md`, `.ufo/waves/round-79/claims.json`, `corpus/source-snapshots/round-79/{S113.txt,manifest.json}`. Written: only the five paths above.

## Out of scope / left to the L1

- Integration of the four artifacts into the lane tree (`corpus/knowledge/`, `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `corpus/instruments/knowledge-expected.txt`).
- B1/B2/B3/B4/B6/B7 counter runs at the landing commit (`frontier-recheck-count.py`, `capture-binding-check.py`, `sources-census.sh validate`) — not run here, not claimed.
- The paraphrase sweep record in the round lesson (claims.json B6) — the literal grep above is measured; the per-clause paraphrase sweep is not.

## Findings / routed notes

- No defect in the frozen capture or manifest found: all eight quotes verbatim on their anchors, sha256 OK.
- Note for the lesson, not a rule change: the Q09 pin is a sentence fragment (the extension list itself, `S113.txt:67-72`, is unpinned). The entry therefore grounds claim 7 on the fragment and names the list as located-but-unpinned under Limits, rather than quoting it.
- Distinctness citation `corpus/knowledge/osv-post-v1-query-contract.md:31` verified to carry the case-sensitivity sentence (S108.txt:53), so `S113.txt:64` is correctly left unclaimed.

## Known limits

- Prose only; nothing was built, published or committed, and no lane gate suite was run.
- `verified-at: 2026-11-06` is the round date; the capture's own instant is `fetched_utc 2026-11-06T18:43:10Z`.
