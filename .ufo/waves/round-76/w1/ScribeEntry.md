# ScribeEntry — round-76 w1, C2 F54 drafts (S111, OSV.dev API overview)

Seat: ScribeEntry (leaf, no subagents). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin, freeze 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e. No lane edits; no git mutation; no network.

## Deliverables (wave dir, drafts for the L1 to apply)

- `.ufo/waves/round-76/w1/f54-entry-draft.md` — target `corpus/knowledge/osv-api-surface-and-limits.md`. 72 lines, 8878 bytes. Header trio per QUALITY Q1 with the mandatory `cd … &&` recheck prefix. Sections: Attribution, Claims 1-2, Rate limits, Response-size limits (held ground, not claimed), Limits, Distinctness, Province fit. 17 anchored quotes; all match their S111.txt line (see V4).
- `.ufo/waves/round-76/w1/s111-row-draft.md` — one SOURCES.md registry row, 11 cells, tier A, kind docs, status mined, opened 2026-11-05, recheck 90d, used-by the target entry above.
- Receipts (evidence files I name): `ScribeEntry-recheck-S111.txt` (committed manifest, exit 2) and `ScribeEntry-recheck-S111-without-Q01.txt` (scratch experiment, exit 0).

## BLOCKER for the C2 after-state: the committed S111 manifest fails its own recheck

The round-76 manifest quote Q01 is `"API (1.0)"` (anchor line 21). That string normalizes to 9 characters. `corpus/instruments/source-recheck.py` sets `MIN_QUOTE_CHARS = 12` (line 33) and rejects shorter quotes at manifest-validation time (line 151-153), before the SHA or any other quote is checked. Result: the S111 recheck exits 2 and checks none of the other 12 quotes. The frozen after-state "source-recheck 13 quotes anchor-ok" cannot hold at the committed manifest.

- Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111` → rc 2; output `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence` (`ScribeEntry-recheck-S111.txt`).
- Scratch experiment (copy of S111.txt and the manifest in a scratch dir, Q01 removed from the copy only) → rc 0; `S111:sha256 OK` and all 12 remaining quotes OK with anchors 22, 28-36, 38, 39 (`ScribeEntry-recheck-S111-without-Q01.txt`).
- No single S111 line reaches 12 normalized characters on line 21 (the line is only `API (1.0)`), so the version statement cannot be machine-anchored by any quote on that line. Repair options for the L1/operator: (a) drop Q01 from the manifest and state the version as an explicit paraphrase of line 21 (the entry's Claim 1 then rests on the line the reader checks by hand); (b) keep Q01 and widen the quote to a longer line-anchored string, which this page does not offer. I did not edit the manifest (L1-owned path). The entry keeps the verbatim `"API (1.0)"` quote, so its recheck line will fail closed until the L1 chooses (a) or (b).

## Verification (every number with its command and exit code)

- V1 capture identity: `sha256sum corpus/source-snapshots/round-76/S111.txt` → `6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab`; `wc -l` 48 lines, `wc -c` 1810 bytes (matches manifest and the frozen claim; the hash line printed, I did not capture its rc separately).
- V2 recheck, committed manifest: rc 2 (see blocker above).
- V3 recheck, scratch manifest minus Q01: rc 0 (12 quotes OK + sha256 OK).
- V4 entry quote anchors: python regex over the entry for `"…" (S111.txt:N)` → 17 anchored quotes, 0 mismatches against the cited capture line (rc 0). Non-capture quotes present in the entry, each checked to its named file: "the overview page", "the other endpoints" (SOURCES.md:120), "the osv.dev service API" (SOURCES.md:86), "triage and claim gates" (PROVINCE.md:30).
- V5 negative terms: `grep -n -i -E 'api key|api_key|authenticat|credential|quota' S111.txt` → no match, rc 1 (entry's "no key/quota/auth" statement).
- V6 experimental labels: `sed -n '29,34p' S111.txt | grep -c Experimental` → 3 (rc 0); `sed -n '4,9p' S111.txt | grep -c experimental` → 3 (rc 0).
- V7 endpoint contract coverage: `grep -n -E 'querybatch|vulns/|importfindings|determineversion|binary-to-source' corpus/knowledge/*.md PROVINCE.md corpus/README.md` → hits only in `osv-post-v1-query-contract.md:75` (F51 Limits bullet, rc 0). The entry's "the other five endpoints have no contract in the corpus" rests on this.
- V8 registry row: `tr -cd '|'` → 12 pipes; 11 cells between them. The row's trailing pipe was missing on the first draft and was corrected (the S108 row ends `… .md |`, same shape). The table header is at SOURCES.md:5 with 11 column names.
- V9 cross-reference of held size ground: `sed -n '148p' round-73/S108.txt` → its first two sentences are word-identical to S111.txt:38; round-73 manifest Q27-Q29 present (python read of manifest, rc 0).
- V10 province and distinctness: `grep -n -o -i -E '.{0,60}osv\.dev.{0,40}' corpus/SOURCES.md` and the knowledge sweep (`grep -n -i -E 'osv\.dev|google\.github\.io/osv' corpus/SOURCES.md corpus/knowledge/*.md`, rc 0). Verdicts are in the entry's Distinctness section.
- V11 registry absence: `grep -c -E '^\| S111 ' corpus/SOURCES.md` → 0 (row not yet admitted, correct pre-integration).
- V12 lane clean: `git -C … status --short -- corpus/` → no output, rc 0 (I did not stage, commit or edit anything in the lane). Disclosure: `git status` is not in the enumerated read-only list; it may refresh the index stat cache. No other git command was run.

## Deviations and reader decisions (disclosed)

1. Row anchor cell carries the full sha256 rather than the spec's `6f92e5b7…` abbreviation, for verifiability.
2. Endpoint pairing: the navigation list (S111.txt:4-9) and the semantic lines (29-34) are in different orders (importfindings before determineversion in nav; the reverse in semantics). The entry pairs them by content and marks that as `[entry's reading]`. The capture gives no explicit link.
3. The capture writes the determineversion path with a space (`POST /v1experimental/ determineversion`, S111.txt:8, :46). The entry quotes it verbatim and reads it as the unspaced path, noting the capture's text.
4. S111.txt:39 (HTTP/2 recommendation with the parenthetical example) is in the manifest as Q13 but is not claimed; the held S108 sentence carries no such example.
5. "Currently" (S111.txt:36) dates the rate-limit answer to the capture; the rejected over-generalization ("no limits of any kind") is answered by the page's own next question (S111.txt:37-38).
6. The S108 registry row (SOURCES.md:120) excludes "the overview page" and "the other endpoints"; the S111 row takes exactly that gap. The lead-only note at SOURCES.md:175 is superseded by the row at integration.
7. Province fit cites PROVINCE.md:30 (core covers triage) and PROVINCE.md:178 (F31 excludes the osv.dev service API). It claims no lane use of the endpoints.

## Tooling

No tool installed, upgraded or removed. No pacman, no sysctl, no ~/.local/bin change.

## Scratch and writes

- Scratch root /fast/scratch/hyaku/kasegi-r76/ScribeEntry created, used for the scratch manifest experiment, and removed (`rm -rf` rc 0; `ls` confirms absence).
- Writes: the three drafts and the two receipts above, all under `.ufo/waves/round-76/w1/`. Nothing else written in the lane.

## Hand-off for KasegiR76 (integration)

- Decide the Q01 repair (options a/b above) before applying the S111 manifest; without it the entry's `recheck:` line exits 2, and the C2 after-state "13 quotes anchor-ok" does not hold.
- Apply `f54-entry-draft.md` as `corpus/knowledge/osv-api-surface-and-limits.md`; apply `s111-row-draft.md` as a new row after S110 in `corpus/SOURCES.md`.
- Expected post-integration checks for the L1: `source-recheck.py --source S111` (after the repair), `grep -c -E '^\| S111 ' corpus/SOURCES.md` → 1, and the knowledge-expected line for F54 (not drafted here; L1-owned).
