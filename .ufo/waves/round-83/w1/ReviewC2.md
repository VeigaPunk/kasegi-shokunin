# ReviewC2 — F59 draft entry review (S117 OSV.dev FAQ post-import lifecycle)

Reviewed: `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` against `corpus/source-snapshots/round-83/S117.txt` + `manifest.json`, `corpus/QUALITY.md`, four distinctness entries, and `corpus/README.md` frontier rows. Receipts: `ReviewC2-receipts/quote-verify.txt` (byte-exact quote checks), `ReviewC2-receipts/recheck-rerun.txt` (live recheck, rc=0).

## Verified clean (evidence)

- **Quotes:** all six pinned quotes are byte-exact substrings of their pins, `occurrences_in_snapshot=1` each, word counts 11/6/19/12/17/12 (all ≤25, Q3); Q06's U+2019 apostrophe matches. Snapshot sha256 `0a5fa51c…bd53e`, 137 lines, 10229 bytes — equals manifest and the entry's Gate block. Entry `recheck:` line re-run live: exit 0, six `OK occurrences=1 anchor=<n>-ok` lines (Q9, R12).
- **Pairings:** F59|S117 (`README.md:1271`), F58|S116 (`:1257`), F57|S115 (`:1243`), F51|S108 (`:1159`), F47|S103 (`:1087`) — all match. Each comparison entry's header carries the claimed S-number. `S103.txt:306-307` = `is_withdrawn boolean` / "Whether to only return advisories that have been withdrawn." F51 "navigation only" verified at `osv-post-v1-query-contract.md:75` ("GET /v1/vulns/{id} … They are listed, not described."). F58 out-of-scope verified at `osv-high-quality-record-import-bar.md:19` and `S116.txt:27` (companion "Managing the Perishability of OSV Records", revalidation out of scope). S117 registry row tier A (`corpus/SOURCES.md:129`).
- **Sweep claim:** `c2-prefreeze-r83.txt` shows the six-quote literal sweep 0 files each over the 96 knowledge files at prefreeze; with the uncommitted draft on disk the count is 97, so "the other 96" is consistent.
- **Attribution/paraphrase spot-checks:** nav span `:2-12`, title `:1`, exclusion list `:113-114`, retention list `:115-118`, GCS sentence `:121`, REST/Git + issue links `:122`, modified_id.csv root/format/per-ecosystem/sort `:94-100`, four import operations `:105-108` — every cited-line paraphrase outside the findings below says only what its lines say. Claims 1, 2, 4, 6 rules are falsifiable and tied to their quotes; their rejected over-generalizations are each refuted at the cited line.

## Findings

### Medium 1 — Claim 3 falsifiable rule over-reaches the page in three ways
Sentence: "Falsifiable rule: a mass upstream deletion from a GCS-imported source that would mark over 10% of its records withdrawn is aborted, so those records stay unmarked until the next import (S117.txt:121)."
Snapshot (`S117.txt:121`): "GCS sources: OSV.dev marks deleted records as withdrawn. There is additionally a safety threshold in the case of feed availability issues: if more than 10% of records are about to be marked as withdrawn, OSV.dev aborts and does not proceed."
Over-reach: (a) "its records" — the page says "more than 10% of records" and never states the denominator (per-source or global); (b) "stay unmarked until the next import" — the page states only that OSV.dev "aborts and does not proceed"; nothing about a later import succeeding (a still-over-threshold next import would abort again); (c) what aborts is the marking, not the deletion.
Proposed replacement: "Falsifiable rule: a GCS import that is about to mark more than 10% of records as withdrawn aborts and does not proceed, so a mass upstream deletion can leave those records unmarked after that import (S117.txt:121); the page does not state whether the 10% is measured over the source's records or over all records."

### Medium 2 — Claim 5's rejected over-generalization is not refuted at any cited line
Sentence: "Rejected over-generalization, not a page sentence: modified_id.csv also lists records deleted upstream. The page describes it for added or changed records (S117.txt:94); deletion handling is a separate answer (S117.txt:119-122)."
Snapshot (`S117.txt:94`): "Yes, we provide a modified_id.csv file that can be used to identify recently added or changed vulnerability records. …" The page says the file "can be used to" identify added/changed records — a capability statement, not an exclusivity claim. Nothing at `:94` or `:119-122` says the CSV omits deleted records, so the stated over-generalization is unsupported rather than refuted; unlike Claims 1-4 and 6, no line contradicts it.
Proposed replacement: "Rejected over-generalization, not a page sentence: a mirror must download the full database to learn which records changed. The page names modified_id.csv for identifying added or changed records and has the reader track entries 'since your last download' by streaming the reverse-chronological CSV (S117.txt:94, :100)."

### Low 1 — Claim 5 body: "one line per record" is an inference
Sentence: "The file sits at the root of the GCS bucket, one line per record as `<iso modified date>,<ecosystem_dir>/<id>`, with a per-ecosystem copy and reverse chronological order (S117.txt:94-100, Q05 pins line 94 only)."
Snapshot: the page gives the row format (`:96`) and one example (`:98`) but never states that each record appears exactly (or at most) once per line.
Proposed replacement: "The file sits at the root of the GCS bucket, its rows formatted `<iso modified date>,<ecosystem_dir>/<id>` (S117.txt:94-98), with a per-ecosystem copy and reverse chronological order (S117.txt:99-100, Q05 pins line 94 only)."

### Low 2 — Claim 1 falsifiable rule cites :112 only; its POST limb rests on :113
Sentence: "…has not ruled out a record excluded because its withdrawn field is set (S117.txt:112)." The exclusion-from-POST half ("the responses to POST API queries") is `S117.txt:113`, which the entry's own body marks outside the pinned span.
Proposed replacement: cite "…excluded because its withdrawn field is set (S117.txt:112-113)."

### Low 3 — Not claimed: data-correction range starts late; two unclaimed answers unlisted
Sentence: "the data-correction route (S117.txt:86-88)". The named lines are route content, but the answer spans `:83-88`; the unclaimed position statements at `:84-85` ("aggregator … most appropriate place to correct the data is at the source", "avoid … broker") sit in no listed range, and the "Why isn't a record available?" answer (`:79-82`, the 404/quality-bar statement) is unclaimed and unlisted.
Proposed replacement: "the data-correction answer (S117.txt:83-88), including the aggregator-not-broker position (:84-85), and the not-imported/404 answer (:79-82)".

## Residual risk and verification gaps

- The two GitHub issue links (`S117.txt:122`) were not opened — the entry labels them unopened leads and claims nothing from them; consistent.
- The 10% denominator is genuinely unstated by the page; Medium 1's replacement keeps the page's own words and names the gap instead of resolving it.
- All verification is captured-source comparison (manifest `fetch_method` declares the normalization); no fresh network fetch was made or is needed for these claims.
- The C2 entry gate (G6 tie limb) and its controls are another seat's scope; not reviewed here.
- No host tooling was installed or upgraded; no tool/version/channel to record.
