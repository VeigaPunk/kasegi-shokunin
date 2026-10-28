# R44W2Scout03 — frontier recon (dangling knowledge entries and S-ids)

- seat: `R44W2Scout03` (scout, read-only); lane: kasegi; round 44 attempt 2, wave 2 (falsify)
- target commit: `8063547d0ce647d6f9eafc3c8d0a502616685218` (`git rev-parse HEAD` in `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
- item: for each of the 26 frontier rows in `corpus/README.md`, the named knowledge entry exists under `corpus/knowledge/` and every S-id the row cites exists in `corpus/SOURCES.md`
- scratch: `/fast/scratch/hyaku/kasegi-r44/R44W2Scout03/` (created with `mkdir -p`; no files written; removed before yield)
- edits: this report only. No production file, no other seat's file, no git/jj mutation.
- tooling: no install. Census used stock `git` and `python3`. `RULES.md` was not applied because nothing was installed.

## Result

**Not falsified.** On commit `8063547d0ce647d6f9eafc3c8d0a502616685218` there is no dangling knowledge entry and no dangling S-id among the 26 frontier rows.

- 26 rows, ids `F01`–`F26`, each once, each with status cell `admitted`. No other `| F<digits> |` row.
- 29 knowledge paths (three rows name two files). Each is a committed `100644` blob under `corpus/knowledge/`, size > 0.
- 47 distinct `S`-ids cited on those rows (citation column and note cell). Each is the first cell of exactly one `corpus/SOURCES.md` registry row.

This does not score C1, C2, the eight routed defects, or the counters. It only says the dangling-entry / dangling-S-id attack does not land.

## Row rule

A frontier row is a line matching `^\| F\d+ \|`, the same rule as `ROW_RX` in `corpus/instruments/r44-frontier-count.py:41`. Cells are pipe-split and stripped. On every selected line the cells are `id | title | status | knowledge | sources | note`, and `status` is `admitted`.

`git show 8063547d0ce647d6f9eafc3c8d0a502616685218:corpus/README.md` is 632 lines. The 26 row lines are 202–213, 264, 284, 309, 335, 361, 388, 389, 416, 477, 506, 534, 563, 591, 628.

Two other pipe-lines mention F-ids and were not counted as frontier rows:

- `corpus/README.md:433` — amendment count line naming historical `F01`–`F18` spans, not a `| Fxx |` row
- `corpus/README.md:447` — meta text ("pipe-split of the F20 line"), not a frontier row

Working tree and commit agree for the files that were read:

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
8063547d0ce647d6f9eafc3c8d0a502616685218

git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --exit-code \
  8063547d0ce647d6f9eafc3c8d0a502616685218 -- \
  corpus/README.md corpus/SOURCES.md corpus/knowledge
# exit 0, empty diff
```

Evidence below is from `git show <commit>:<path>` and `git ls-tree -r -l <commit> corpus/knowledge`, not from an uncommitted overlay.

## How existence was decided

- Knowledge entry: after stripping markdown backticks, every `knowledge/<name>.md` token in the knowledge cell is a path `corpus/<that token>` present in `git ls-tree -r -l 8063547d0ce647d6f9eafc3c8d0a502616685218 corpus/knowledge`. The knowledge cell of every row was fully consumed by those tokens (no leftover path text).
- S-id: every `S` + three or more digits on the whole row line, including the note cell. Exists when `corpus/SOURCES.md` has a line matching `^\|\s*<id>\s*\|` (registry header is `corpus/SOURCES.md:5`, separator `:6`). 70 such ids in the file, none duplicated. Cited ids are a subset.

`F26`'s knowledge cell is backtick-wrapped. The path inside the span is the one that was checked:

```
corpus/README.md:628
| F26 | Google Cloud VRP's own program scope, customer-resource testing prohibition and reward-ineligibility boundary | admitted | `knowledge/google-cloud-vrp-customer-resource-boundary.md` | S069 | ...
```

`S069`'s registry row is `corpus/SOURCES.md:75`, first cell `S069`, used-by `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`.

## The 26 rows

Citation-column ids are the sources cell. "Note-only" ids appear in the note and not in that cell. Both sets resolve.

| README line | id | knowledge paths under `corpus/` | citation-column S-ids | note-only S-ids |
|---|---|---|---|---|
| 202 | F01 | `knowledge/cvss-v4-severity-and-vector.md` | S001, S002 | — |
| 203 | F02 | `knowledge/coordinated-disclosure-timelines.md` | S003, S004, S005 | — |
| 204 | F03 | `knowledge/authorization-safe-harbor-and-scope.md` | S006, S007, S008 | — |
| 205 | F04 | `knowledge/ai-assisted-finding-validation.md` | S009, S010, S011, S012 | — |
| 206 | F05 | `knowledge/cwe-top25-2025-methodology.md` | S013, S014, S015 | — |
| 207 | F06 | `knowledge/multiparty-vulnerability-coordination.md` | S018 | — |
| 208 | F07 | `knowledge/cna-assignment-and-vulnerability-rules.md` | S031 | — |
| 209 | F08 | `knowledge/cra-manufacturer-reporting-duties.md` | S029 | — |
| 210 | F09 | `knowledge/authorised-testing-rules-of-engagement.md`, `knowledge/statutory-authorization-and-unauthorized-access.md` | S032, S033, S034, S035 | — |
| 211 | F10 | `knowledge/vendor-disclosure-policies-as-corpus-objects.md`, `knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | S036, S037, S038, S039, S040 | — |
| 212 | F11 | `knowledge/iso-29147-and-30111-division-of-labour.md`, `knowledge/iso-29147-divergence-and-clause-crosswalk.md` | S041 | — |
| 213 | F12 | `knowledge/japanese-domestic-disclosure-workflow.md` | S041, S042 | S004 (also repeats S041) |
| 264 | F13 | `knowledge/program-severity-ladders-and-reward-scales.md` | S043, S044, S045 | — |
| 284 | F14 | `knowledge/japanese-severity-vocabulary-and-impact-model.md` | S046, S047, S041 | — |
| 309 | F15 | `knowledge/vendor-third-party-finding-coordination.md` | S048 | S039, S040 (also repeats S048) |
| 335 | F16 | `knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` | S049, S050 | — (note repeats S049, S050) |
| 361 | F17 | `knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` | S051 | — (note repeats S051) |
| 388 | F18 | `knowledge/cisa-kev-catalog.md` | S052 | — |
| 389 | F19 | `knowledge/epss-exploit-prediction-scoring.md` | S053 | — |
| 416 | F20 | `knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` | S054 | S001, S002, S052, S053 (note also repeats S054) |
| 477 | F21 | `knowledge/csaf-vex-product-status-and-justifications.md` | S055 | — (note repeats S055) |
| 506 | F22 | `knowledge/cisa-when-to-issue-vex.md` | S057 | — |
| 534 | F23 | `knowledge/cyclonedx-analysis-subtree.md` | S060 | S055, S057 (note also repeats S060) |
| 563 | F24 | `knowledge/rfc-9116-security-txt.md` | S063 | — |
| 591 | F25 | `knowledge/cve-json-record-format.md` | S064 | — (note repeats S064) |
| 628 | F26 | `knowledge/google-cloud-vrp-customer-resource-boundary.md` | S069 | — |

Note-only contexts (committed `corpus/README.md`):

- `:213` F12 ends with `from the initial report (S004, F02)`.
- `:309` F15 says `as F10's S039/S040 rows route it`.
- `:416` F20 says `source those definitions from S001/S002, S052 and S053`.
- `:534` F23 contrasts `S055` and ends with `that layer is S057's`.

## Blobs (`git ls-tree -r -l 8063547d0ce647d6f9eafc3c8d0a502616685218 corpus/knowledge`)

29 cited paths. `missing=0`, `size=0` count `=0`, non-`100644`/`blob` count `=0`. The tree has 63 blobs under `corpus/knowledge/`; only these 29 are named by frontier rows.

| mode | type | blob | bytes | path |
|---|---|---|---:|---|
| 100644 | blob | `d63954daa374070457e6f13b155a9ee6425887d7` | 4556 | `corpus/knowledge/cvss-v4-severity-and-vector.md` |
| 100644 | blob | `ab4ce3411597abda5d8abd1f7f2fdcaf8afeaf0c` | 4423 | `corpus/knowledge/coordinated-disclosure-timelines.md` |
| 100644 | blob | `8d824f30f14845f928edac91548f23ad0d95ff75` | 4445 | `corpus/knowledge/authorization-safe-harbor-and-scope.md` |
| 100644 | blob | `b4d056619a1eed0ae2361f8559053bc5b64a0423` | 4866 | `corpus/knowledge/ai-assisted-finding-validation.md` |
| 100644 | blob | `ab194fa78d6fbcc69d566bf0cca849c5c330993a` | 4685 | `corpus/knowledge/cwe-top25-2025-methodology.md` |
| 100644 | blob | `505b667a16c539c102b087701388580c2488556b` | 4476 | `corpus/knowledge/multiparty-vulnerability-coordination.md` |
| 100644 | blob | `a94c54922de685ce090ed545610207df1811e86e` | 5650 | `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` |
| 100644 | blob | `5c10d464dc5baa3e1a674589c658da1b6e384291` | 6005 | `corpus/knowledge/cra-manufacturer-reporting-duties.md` |
| 100644 | blob | `0e54ad782232702fcb34d9f70ff5f8fee15e08b6` | 5296 | `corpus/knowledge/authorised-testing-rules-of-engagement.md` |
| 100644 | blob | `e391832ac460732b7c4af9f50537d0442203f267` | 15211 | `corpus/knowledge/statutory-authorization-and-unauthorized-access.md` |
| 100644 | blob | `d2f3c80623a99ddc90069841468db2215fed4303` | 14264 | `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` |
| 100644 | blob | `b2193ea686e4cd3909c37f808a4c1d24586628ca` | 16468 | `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` |
| 100644 | blob | `074f6d6e8a79fe9eda1727e5f6b5a5513c73c93b` | 7255 | `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` |
| 100644 | blob | `cb386210490e4455bef68fc53e62f8fae79c7731` | 10547 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` |
| 100644 | blob | `33b26d8b744595a6d7875e886288a8aa6f9237ae` | 18544 | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` |
| 100644 | blob | `33e7f36a9c089c20e8dc98d10e3f3d46ba6b9fd7` | 8095 | `corpus/knowledge/program-severity-ladders-and-reward-scales.md` |
| 100644 | blob | `245ada02cfe6686a8baf8ec029c554936a1c52e7` | 7096 | `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` |
| 100644 | blob | `692a48e902e7e1810ea2ea2cb8d739e18f481dff` | 12900 | `corpus/knowledge/vendor-third-party-finding-coordination.md` |
| 100644 | blob | `77e0681116b77852b900080641a9d5c8d58c4fb2` | 24539 | `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` |
| 100644 | blob | `060491cdd849f943f0debee46260b382410c5221` | 11143 | `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` |
| 100644 | blob | `bac9126b0284923f1efc65599a9581bc9c719d89` | 15831 | `corpus/knowledge/cisa-kev-catalog.md` |
| 100644 | blob | `d0cabacbab72800d820f2199d2f03b3985ab9e2f` | 17372 | `corpus/knowledge/epss-exploit-prediction-scoring.md` |
| 100644 | blob | `e124017567b8dcb1b38d738cabbf39adc3624e60` | 13081 | `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` |
| 100644 | blob | `2977a4381c1a35657c16fa0fd1737358f71adc77` | 22887 | `corpus/knowledge/csaf-vex-product-status-and-justifications.md` |
| 100644 | blob | `7bd4c784916733e8304d35b49e948af5fe393725` | 19196 | `corpus/knowledge/cisa-when-to-issue-vex.md` |
| 100644 | blob | `fe678a7a01c14d220c4c8c618d27c752a5cdff7f` | 22993 | `corpus/knowledge/cyclonedx-analysis-subtree.md` |
| 100644 | blob | `6102a57c47d924c792c0ad3689876a9fdb4ff782` | 10898 | `corpus/knowledge/rfc-9116-security-txt.md` |
| 100644 | blob | `4345e664418f237b488b533cd4cbd64f5872e1a5` | 23793 | `corpus/knowledge/cve-json-record-format.md` |
| 100644 | blob | `2800b9c5161702b7429c5fb6b003fb41d22f981c` | 5843 | `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` |

## S-id registry lines (`git show 8063547d…:corpus/SOURCES.md`)

Each cited id, one registry line, first cell equal to that id:

| S-id | SOURCES.md line | S-id | line | S-id | line | S-id | line |
|---|---:|---|---:|---|---:|---|---:|
| S001 | 7 | S002 | 8 | S003 | 9 | S004 | 10 |
| S005 | 11 | S006 | 12 | S007 | 13 | S008 | 14 |
| S009 | 15 | S010 | 16 | S011 | 17 | S012 | 18 |
| S013 | 19 | S014 | 20 | S015 | 21 | S018 | 24 |
| S029 | 35 | S031 | 37 | S032 | 38 | S033 | 39 |
| S034 | 40 | S035 | 41 | S036 | 42 | S037 | 43 |
| S038 | 44 | S039 | 45 | S040 | 46 | S041 | 47 |
| S042 | 48 | S043 | 49 | S044 | 50 | S045 | 51 |
| S046 | 52 | S047 | 53 | S048 | 54 | S049 | 55 |
| S050 | 56 | S051 | 57 | S052 | 58 | S053 | 59 |
| S054 | 60 | S055 | 61 | S057 | 62 | S060 | 66 |
| S063 | 69 | S064 | 70 | S069 | 75 | | |

Ids that exist in the registry but are not cited by any of these 26 rows (S016, S017, and the other gaps) are not dangling citations. They were not reported.

## Preamble that was read and not used as a hit

`corpus/lessons/round-43-verifier-spotcheck.md` §6 (lines 97–108) lists eight routed defects: unbacked `closed=13/19`, no check seeing defect 1, the 29-vs-26 character numeral, report omissions, wave-evidence hygiene, a missing `SHONEN.md` newline, a `corpus/instruments/README.md` pointer, and the C1 before-cell `127` vs `exit=2`. None of them is a frontier-row dangling path or S-id, so they do not change this census.

Frozen claims were read from `.ufo/waves/round-44/claims.json`. C2's before/after text says the frontier moves from 25 rows to 26. This seat checked those 26 rows for dangling names only.

## Limitations

- Existence of a knowledge entry means the committed blob at the named path. The file body was not checked for a matching title or for the S-ids the row cites.
- Existence of an S-id means a registry row whose first cell is that id. A prose mention alone would have been reported as no row; none of the 47 needed that fallback. Source URLs were not fetched.
- No language server is mounted in this seat. The objects are markdown table cells, so the census is `git show` / `git ls-tree`, not an LSP definition query.
- Rows were not re-derived by executing `corpus/instruments/r44-frontier-count.py`. The row regex was read from that file (`:41`) and applied to the committed README. The C2 counter's exit status was not run and is not claimed.
- `corpus/README.md:433` and `:447` were excluded as non-rows, as stated above.
