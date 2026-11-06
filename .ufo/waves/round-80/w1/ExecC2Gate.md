# ExecC2Gate — C2 (coverage) landing gate on a scratch mirror, round 80 attempt 1

Seat: ExecC2Gate (leaf executor, C2 gate). Scratch root `/fast/scratch/hyaku/kasegi-r80/ExecC2Gate` (TMPDIR passed explicitly; removed before yield).
Freeze commit `4ab545865f747fca8456370b5927fe51236fe579` (base `58905f2bbc52db6b1634566cc1be9c92cdddebfb`).
No frozen byte was edited: candidate counter/table/builder (`c1/`), `claims.json`, the round-80 manifest, `S114.txt` and the w1-input draft are read-only inputs. All landing edits were made in scratch trees only. No git/jj writes. `pacman` not used; no tool installed.

## 1. Landings applied

### 1a. Gate mirror `$S/tree` (the construction in this item)

Built with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 4ab545865f747fca8456370b5927fe51236fe579 | tar -x -C $S/tree`, then:

| # | file (in `$S/tree`) | change | sha256 after |
|---|---|---|---|
| 1 | `corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md` | created, byte copy of `.ufo/waves/round-80/w1-input/osv-ubuntu-binary-to-source-mapping.md` | `5b176aa578d8da541d76742281a2fa71afa219b2014d8770fdc211632e17c8d8` (identical to the input draft) |
| 2 | `corpus/SOURCES.md` line 126 (row S114), field 9 and field 12 only | field 9 ` queued ` → ` mined `; field 12 ` — ` → ` corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md ` | `529146059edad24146634ad8299fde1d8426b09387d380696dedda03b94ff383` |
| 3 | `corpus/instruments/knowledge-expected.txt` | inserted `corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md` between `...osv-post-v1-query-contract.md` and `...policy-access-playbook.md` (LC_ALL=C position; whole .md row list verified sorted) | `f189b269126488d8665518a919199c2bfc7bd027a863701c8af9527b34aad6f3` |
| 4 | `corpus/README.md` EOF | appended `## Round-80 admission — Frontier F56 (2026-11-06)`, the frontier table header + separator, the F56 row (line 1223), and an `[r80 amendment, appended 2026-11-06]` line | `d332f8cf66c7855893cfa91776762804f6bcf2e6d8ec6590b2613cd290c94e96` |

F56 row used (line 1223 of the gate mirror; also written alone to `ExecC2Gate-readme-row.txt`):

```
| F56 | OSV.dev POST /v1experimental/ubuntu/binary-to-source Ubuntu binary-to-source mapping contract — the purpose (Ubuntu binary package names to their corresponding source package names), the reason (Ubuntu vulnerability advisories in OSV are indexed by source package name rather than binary package name), the scanner use (callers such as scanners query OSV using the resulting source package names), the ecosystem parameter's three stated Ubuntu release forms, the non-empty binary_names array with its 1000-per-request maximum, and the empty object for a binary name with no known source package mappings | admitted | knowledge/osv-ubuntu-binary-to-source-mapping.md | S114 | Read the six clauses at their pinned lines (S114.txt:25 purpose; :35 source-name indexing and scanner use; :38 ecosystem forms; :39 binary_names bounds; :58 unmapped-name empty object) and claim neither the experimental-status paragraph nor the input-matched ordering clause F54 already holds |
```

Row-parse precondition (read before writing): `frontier-recheck-count.py` `FRONTIER_ROW = ^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|` (four cells: id, topic, status, entry) and `FRONTIER_SOURCES` (5th cell = source ids). The row has exactly six cells, `admitted` in cell 3, `knowledge/…md` in cell 4, `S114` in cell 5; no cell contains `|` or a backtick.

### 1b. Lane mirror `$S/lane-tree` (the bytes the L1 had already written)

While this gate ran, the lane working tree already carried an integration (`corpus/SOURCES.md` field 9 = `mined`, field 12 = the entry path; entry present). To keep the gate evidence pinned, the lane's four landing files were snapshotted into a second freeze archive and every B-limb re-run there:

| file | lane sha256 at snapshot |
|---|---|
| `corpus/SOURCES.md` | `e9df9bd071340349e769ffc31e5e93e5bc183936fb8fd51f48b2db54266a3ff4` |
| `corpus/README.md` | `58dc1843de97ad6dc003cec09f8cdbc2760915fd9e28b1673ed6dc1cabcdf048` |
| `corpus/instruments/knowledge-expected.txt` | `f189b269126488d8665518a919199c2bfc7bd027a863701c8af9527b34aad6f3` (identical to the gate mirror) |
| `corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md` | `5b176aa578d8da541d76742281a2fa71afa219b2014d8770fdc211632e17c8d8` (identical to the gate mirror and to the input draft) |

Lane-vs-freeze `corpus/SOURCES.md`: 275 → 276 lines; the single registry-row change is line 126, fields 9 and 12 exactly as above; registry count 114 → 114 (no row added, removed, or re-ordered). The one added line is a non-row changelog bullet (`- Round-80 S114 added …`) inside the existing amendment list — outside B1's row-scoped predicate. The lane's `corpus/README.md` F56 section is the L1's own text (coverage-map row + frontier row + amendment), textually different from the gate-mirror row; it parses and passes every limb (see §3b).

## 2. B0–B7 (named commands, gate mirror `$S/tree`)

| limb | command | output (verbatim) | rc | verdict |
|---|---|---|---|---|
| B0 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-80/manifest.json --source S114` | `S114:sha256 OK` + `S114:Q01-purpose OK occurrences=1 anchor=25-ok`, `S114:Q02-source-indexing OK occurrences=1 anchor=35-ok`, `S114:Q03-scanner-use OK occurrences=1 anchor=35-ok`, `S114:Q04-ecosystem-forms OK occurrences=1 anchor=38-ok`, `S114:Q05-binary-names-limit OK occurrences=1 anchor=39-ok`, `S114:Q07-unmapped-empty-object OK occurrences=1 anchor=58-ok` | 0 | **met** (six OK lines, anchors 25/35/35/38/39/58 = manifest) |
| B1 | `git show 4ab5458:corpus/SOURCES.md` vs landing; field-level compare; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on both | differing line indexes `[125]` ⇒ line 126 only; 13 fields each; changed fields `9 OLD=[ queued ] NEW=[ mined ]`, `12 OLD=[ — ] NEW=[ corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md ]`; registry rows `114` / `114`; line counts 275/275 | diff rc 1 (expected: a difference exists) | **met** (exactly one row, exactly its status and used-by cells) |
| B2 | `ls corpus/knowledge/*.md \| wc -l`; `wc -l < knowledge-expected.txt`; `grep -c '\.md$'`; sorted set diff vs listing | `94`; `96`; `94`; `MD_ROW_SET_EQUALS_LISTING`; `EXPECTED_SORT_LC_ALL_C_OK` (`LC_ALL=C sort -c` silent) | 0 | **met** (93→94 entries, 95/93 → 96/94 lines/rows, set equal, C-order preserved) |
| B3 | `python3 corpus/instruments/frontier-recheck-count.py \| grep -E 'FRONTIER-CENSUS\|F56'` | `FRONTIER-CENSUS rows=56 admitted=56 closed=56 problem-rows=0 registry=114`; `FRONTIER-PASS F56 ids=S114`; record `PASS F56 knowledge/osv-ubuntu-binary-to-source-mapping.md ids=S114 exit=0`; `grep -c FAIL` = 0 | 0 | **met** (exact string; the census executed **all 56** recheck lines, 0 failures) |
| B4 | `python3 corpus/instruments/capture-binding-check.py \| tail -3` | `MANIFEST round-80 records=1 url_bound=1 fetched=1 archival=0`; `AUDIT records=94 with_url=94 with_fetched_utc=56 with_archival=38 snapshot_dirs=53 manifest_dirs=53 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt`; `records=94 bound=94 unbound=0` | 0 | **met** (`unbound=0`; the `orphans=1 S040-live.txt` line is pre-existing at the freeze, unrelated to S114) |
| B5 | entry `recheck:` line extracted; string equality against the B0 command behind `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `; then `bash -c "$R"` from fresh cwd `$S/foreign` | `EXACT_MATCH_OK`; from the foreign cwd: six OK lines, `B5 rc=0`, `pwd` = `/fast/scratch/hyaku/kasegi-r80/ExecC2Gate/foreign` | 0 | **met** (line is exactly `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-80/manifest.json --source S114`; exits 0 from a foreign cwd) |
| B6 | literal containment of each of the six manifest quotes over the 93 pre-existing `corpus/knowledge/*.md` (new entry excluded) | `Q01..Q07 files_with_quote=0` for all six; `B6 total_files_with_quote= 0 verdict met` | 0 | **met** on the literal limb (0/6 files; the freeze control `controls/c2-prerecheck-r80.txt` records the same 0/6). The paraphrase limb is a scout record, not re-executed here — see §5 note 4 |
| B7 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/tree/corpus/SOURCES.md` | six inherited `W04` lines (S028 S029 S072 S076 S080 S085) then `file ok …/tree/corpus/SOURCES.md` | 0 | **met** (no new finding; identical output to the same command on a full freeze tree `$S/base-tree`, apart from the file path — a `diff` shows only line 7's path) |

B7 note (as required by the item): the `--file` form infers the lane directory as `realpath(dirname(FILE)/..)`, so a `SOURCES.md` copied outside a complete lane floods `E11 missing used-by` for every mined row (observed: 98 E11 lines when the file sat at `$S/freeze-SOURCES.md`). The freeze baseline is therefore taken at `$S/base-tree` (a full archive) and is byte-for-byte the same finding set as the landing. The `--root` form (`validate --root /home/vgpnk/Projects/shokunin kasegi`) resolves the lane from `shokunin.conf` and needs the **real** lane (or a root that carries the conf and the lane dir); it was not run here — it would read the live lane, which other seats are editing, so it is not gateable deterministically from scratch and belongs to the L1's post-integration run.

## 3. Step 3 — quoted spans citing `S114.txt:<n>`

Regex scan of the draft entry: pattern A `"([^"\n]+)"\s*\(S114\.txt:(\d+)` (claim prose) and pattern B `\|\s*S114\.txt:(\d+)\s*\|\s*(\d+)\s*\|\s*"([^"\n]+)"\s*\|` (the Gate table, which additionally carries a `wc -w` column).

**ok=12 bad=0** — every bad is listed (there are none).

| source | snapshot line | check |
|---|---|---|
| Claim 1 prose | 25 | quote on that line |
| Claim 2 prose | 35 | quote on that line |
| Claim 3 prose | 35 | quote on that line |
| Claim 4 prose | 38 | quote on that line |
| Claim 5 prose | 39 | quote on that line |
| Claim 6 prose | 58 | quote on that line |
| Gate table cl1 (Q01) | 25 | quote on line and `wc -w` = 11 |
| Gate table cl2 (Q02) | 35 | quote on line and `wc -w` = 16 |
| Gate table cl3 (Q03) | 35 | quote on line and `wc -w` = 14 |
| Gate table cl4 (Q04) | 38 | quote on line and `wc -w` = 9 |
| Gate table cl5 (Q05) | 39 | quote on line and `wc -w` = 12 |
| Gate table cl6 (Q07) | 58 | quote on line and `wc -w` = 20 |

All cited snapshot lines are in range (`cited lines [22, 25, 33, 35, 38, 39, 41, 48, 58, 60]`, snapshot has 73 lines). The Gate table's six `manifest pin` ids and quoted strings are byte-equal to the manifest entries, and its line numbers equal the manifest anchors (`quote_equal True` and `anchor == manifest anchor` for all six).

## 4. Extra evidence gathered (not part of B0–B7)

1. **Capture metadata reconciles.** `sha256sum corpus/source-snapshots/round-80/S114.txt` = `e1ccfb9bd13bb3f9a077feb60ae5d738ccb47bc85f630aef9a7a5776ca8788d2`; `73` lines; `2365` bytes — all three equal the manifest and the entry's Gate bullet. Manifest `fetched_utc` = `2026-11-06T19:42:42Z`, `http.status` 200, `final_url` = the requested URL; the manifest's `fetch_method` states `raw page 18769 bytes`, matching the entry.
2. **The 404 sentence in the entry is true today, not just inherited.** Read-only probe at `2026-11-06T19:51:06Z`: `post-v1experimental-ubuntu-binary-to-source http=404 bytes=11373`, `post-v1-ubuntu-binary-to-source http=200 bytes=18769`. The in-lane receipt for the same 404 is `.ufo/waves/round-77/w1/ScribeSources.endpoint-probe-r77.txt:22` (`probe time (UTC): 2026-11-05T12:40:45Z`), so the entry's `on 2026-11-06` date is now directly receipted by this probe; the 18769-byte live size also matches the manifest's raw-page count.
3. **The entry's negative-evidence greps still hold on the frozen capture** (each prints nothing, rc 1): `rate limit|ratelimit|quota|api key|api_key|authenticat|credential`; `paginat|page_token|next_page_token`; `error|status code|throttl|400`; `severity|CVE|cvss`; `Debian|deb|dpkg`. The pre-entry subject sweep `grep -rli ubuntu` over the 93 admitted entries prints nothing, rc 1. The capture carries no timestamp (`grep -nE '2026|T[0-9]{2}:[0-9]{2}'` rc 1), as the entry's Limits states.
4. **Cross-entry citations resolve.** `corpus/knowledge/osv-post-batch-query-contract.md:37` is the "1,000 vulnerabilities" / "3,000 vulnerabilities total" sentence (Claim 5's distinction is correct); `…:19` is `## Claim 2 — the response ordering is guaranteed to match the input` (Distinctness's "ordering rule-shape F54 holds" citing :19 is correct); `corpus/knowledge/osv-post-v1-query-contract.md:75` lists the experimental endpoints without describing them (Attribution correct). Snapshot `:22-23` is the page heading `POST /v1experimental/ubuntu/binary-to-source`; `:33` is the experimental-status paragraph the entry excludes; `:41`/`:60`/`:71` are the payload skeleton and the `results` array bounds the entry excludes.
5. **Entry shape matches its sibling.** The first seven lines (h1, `source:`, `verified-at:`, `recheck:`) are structurally identical to `osv-determineversion-cc-library-versioning.md`, including the `cd <lane> && …` recheck form used by all 55 prior entries.

## 5. Notes, risks, routed observations

1. **The census's execution limb is lane-bound, not root-bound.** `frontier-recheck-count.py` runs each `recheck:` line with `bash -c` and `cwd=<root>`, but every entry's own line starts `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`, so the executed command re-verifies the **real lane's** frozen captures (`corpus/source-snapshots/round-80/…`, unchanged since the freeze). `B3`'s structural limbs (row count, status, entry existence, entry↔source binding, manifest listing, duplicate realpath) do read the mirror, and they are what `rows=56 … FRONTIER-PASS F56 ids=S114` scores. This is the pre-existing convention (all 55 siblings share it), not a defect introduced by F56; it does mean `B3` at a scratch root is not an independent proof that the *mirror's* capture bytes are present.
2. **The lane had already landed when this gate sampled it**, so the gate validated two independent byte sets: the construction in this item (§1a) and the lane's own integration (§1b). Both are `met` on B0, B2, B3, B4, B5, B6, B7 with the same outputs quoted above; the only difference is the README prose (§1b note) and the extra changelog bullet in `corpus/SOURCES.md`. The entry file and `knowledge-expected.txt` are byte-identical across the two.
3. **No coverage-map row was added to the gate mirror.** This item asked only for a frontier row, so the mirror's README carries the heading, the table header/separator, the F56 row and an amendment line. The lane's own integration does carry the coverage-map row; if the L1 later replaces the mirror shape, the census does not read coverage-map rows (no instrument references them: `grep -rln 'coverage map\|coverage-map' corpus/instruments/` prints nothing).
4. **B6's paraphrase limb is a record, not a command I re-ran.** The frozen control `.ufo/waves/round-80/controls/c2-prerecheck-r80.txt` records the literal sweep (0/6) and the scout paraphrase sweep; this gate re-measured the literal half (0/6) and verified that each claimed clause's nearest admitted terms are absent (`ubuntu` subject sweep rc 1). No seat may re-score the scout's prose judgement here, and a paraphrase finding would be a round-81 routed defect, not a verdict change.
5. **Frozen bytes untouched.** No file under `c1/`, `controls/`, `w1-input/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or any instrument was modified by this seat; the only writes are the two files below (plus scratch, deleted).
6. **B1's predicate wording** says "adds none, removes none" about registry **rows**; the lane's added changelog bullet is not a row (`grep -cE '^\| S[0-9]{3,} \|'` = 114 before and after) and does not touch B1's measured cells. Flagged so the L1's own receipt states the same scope.

## 6. Files written by this seat

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/ExecC2Gate.md` (this file)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/ExecC2Gate-readme-row.txt` (the F56 row line alone, as used in the gate mirror)

Scratch `/fast/scratch/hyaku/kasegi-r80/ExecC2Gate` removed at exit. No build, lint, test or formatter run; the lane's gate suite was not executed by this seat.
