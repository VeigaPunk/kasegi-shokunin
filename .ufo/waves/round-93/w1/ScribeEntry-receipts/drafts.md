# Round-93 w1 — ScribeEntry drafts (not committed)

Seat: ScribeEntry (leaf, non-author). Base `e15996bfd2f6eca4af39507a7c5973afbeca8347`, freeze
`5bad9e55d3d9319446e3d9b63bc2dece633cdb68`, C1 landing `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`,
C2 landing `9225954a6e3f177af46bdb9d811c062a4353a552`. Every fact below was read from committed bytes
via `git show <rev>:<path>`; the one census run in item 1 read the working tree, which the L1 had already
begun editing, so the enum/status check was repeated over the freeze bytes (`07`, appended block).
The commands and their observed output are in this directory (`01`–`07`).

Result line: **drafts=4 defects=3** (three routed defects, none a SOURCES cell mismatch and none
re-scoring C1 or C2; qualified items listed in § Qualifiers).

---

## Item 1 — `corpus/SOURCES.md` S139 row and the round-93 row-change bullet at the freeze `5bad9e55`

Verified against the capture `corpus/source-snapshots/round-93/S139.txt` and
`corpus/source-snapshots/round-93/manifest.json` (receipt `02-sources-row.txt`, `03-s139-anchor.txt`).
Column order is the registry header `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`
(11 cells; `02` prints the split).

| # | cell (trimmed) | evidence | match |
|---|---|---|---|
| 1 | `S139` | registry rows at the freeze `139`; S138 is the preceding row; the census-start receipt reads 138 before the edit | yes |
| 2 | `GitLab Docs, Secret detection: Detected secrets — https://docs.gitlab.com/user/application_security/secret_detection/detected_secrets/` | capture line 1 reads `Detected secrets \| GitLab Docs`; `Secret detection` occurs at lines 44 and 77; the URL equals `manifest.json` `url`/`capture_url` | yes |
| 3 | `docs` | lane kind enum `spec · docs · paper · code · tool · dataset · talk · book · community · own-work`; an `awk` pass over every registry row of the freeze bytes prints no cell-count, E05, tier or status line (`07` appended block); the live census prints `kasegi ok` rc 0 with no E05 line | yes |
| 4 | `A` | first-party GitLab documentation, the same tier as the round-92 S136 row (GitHub Docs, `docs`, `A`, `180d`); Q4 attribution holds. No written tier legend exists in the corpus contract — see Qualifier Q2 | yes (precedential) |
| 5 | `GitLab's own rule statement for the personal access token format` | the page is GitLab's own docs and lines 84–87 are its rule statement for the token format; the page is broader (generic detection, catalogue), so the cell is the admitted scope, not the page's whole extent (Q3) | yes |
| 6 | `Rule-based detection section, snapshot lines 85-87 (the pattern statement and the 20-character sentence); capture corpus/source-snapshots/round-93/S139.txt` | line 84 is the `Rule-based detection` heading; 85–86 the pattern statement; 87 the 20-character sentence (`03` prints 83–88 with numbers) | yes |
| 7 | `A GitLab personal access token is \`glpat-\` plus a 20-character string, … the page states no alphabet …` | line 87: `glpat- followed by a 20-character string.`; the only `character` occurrence in 414 lines is line 87; `alphabet`/`alphanumeric`/`A-Za-z` occur 0 times (`grep -c` rc 1) | yes |
| 8 | `queued` | freeze-time status; the C2 landing does not touch `SOURCES.md` (`git diff-tree` names `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py`) | yes |
| 9 | `2026-11-07` | `manifest.json` `fetched_utc` `2026-11-07T13:55:21Z` | yes |
| 10 | `180d` | same recheck as S136/S137 (`docs`, `A`) | yes |
| 11 | `—` | no used-by at the freeze; the row change below is the integration step | yes |

Row-change bullet (last line of the freeze file), checked cell by cell against the same evidence:
`id S139`, `kind docs`, `tier A`, `opened 2026-11-07`, `recheck 180d`, `status queued`, `used-by —` in
the round-93 freeze — all five match the row. `four digest-bound allowlist rows for
corpus/source-snapshots/round-93/S139.txt` — `grep -c round-93/S139.txt corpus/instruments/capture-secret-allow.tsv` = 4.
`pre-capture refusal: .ufo/waves/round-93/controls/capture-intake-r93.txt` — the receipt holds
`INTAKE-REFUSED S139 shape=bearer line=124 … written=no`, `shape=credential line=116`, `rc=3`.
One wording defect in the same bullet (three samples, four rows): Defect D3.

**Item 1: PASS** — 11/11 cells match; no cell to correct.

---

## Item 2 — the `capture-secret-scan` capability row at the C2 landing `9225954a`

The landed row is byte-identical to the frozen candidate row (receipt `04-c2-row.txt`):
`sha256 6d18d57978f3ae8e45da85fcf9ef6cdf2a523f1ec50955c7d496e85741e3fb40`, `diff` rc 0, 2,731 bytes,
equal to `candidate_row_sha256` in `claims.json`.

| element the row must name | landed text | match |
|---|---|---|
| `gitlab-pat` | ``and `gitlab-pat` (a `glpat-` prefix plus a 20-character string, S139)`` | yes |
| the escape boundary | ``plus tokens preceded by a JSON, percent or HTML-entity escape terminator whose last byte is alphanumeric (the `github-token` left boundary, round 93)`` | yes (wording qualifier Q1) |
| S139 | `S139` inside the `gitlab-pat` clause, and `S139` also in no other place | yes |
| first-working round 87 kept | row still opens `the claim-package gate patterns, AWS STS session tokens and AWS key ids (round 87)`; the row's final cell (first-working round) is `87` | yes |

The prose matches the landed regexes: `_GL_LB`/`_GH_LB` admit `\\[ntr]`, `\\u[0-9A-Fa-f]{4}`,
`%[0-9A-Fa-f]{2}`, `&#[0-9]{2};`, `&#[xX][0-9A-Fa-f]{2};` (`capture-secret-scan.py:169-177`), and
`gitlab-pat` is `glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` (`:179`). Landing evidence:
`CAPABILITY-CHECK-RESULT pass rc=0` three times (seeds 638505535, 1, 9191), `K8 pass clauses=50`,
`landed sha256` = `frozen candidate sha256` = `7d9d7309…`, `row-equal yes` (`.ufo/waves/round-93/l1/c2-landing-r93.txt`).

**Item 2: PASS** — all four elements present; wording qualifier Q1 on the parenthetical gloss.

---

## Item 3 — `## Gate` block for `corpus/lessons/round-93.md` (lane form)

Form copied from `corpus/lessons/round-92.md` § Gate (heading, URL, Accessed, Capture, Located quote,
Row change, Rejected this round). Numbers: sha256 `154a7e15…` (`sha256sum`), 25,370 bytes (`stat`),
414 lines (`wc -l`, `awk NR`), quote at line 87 with **6 words** (`printf … | wc -w`), access date
2026-11-07 (`manifest.json` `fetched_utc` 13:55:21Z).

```markdown
### S139 — GitLab Docs, Secret detection: Detected secrets (admitted, used by the instrument)

- **URL:** https://docs.gitlab.com/user/application_security/secret_detection/detected_secrets/, HTTP 200.
- **Accessed:** 2026-11-07 (capture 13:55:21Z).
- **Capture:** `corpus/source-snapshots/round-93/S139.txt`, sha256 `154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188` (25,370 bytes, 414 lines); manifest `corpus/source-snapshots/round-93/manifest.json`, `source-recheck.py` rc 0 (anchors 85 and 87; `.ufo/waves/round-93/controls/source-recheck-r93.txt`); captured through the intake gate after a pre-capture refusal (`INTAKE-REFUSED S139 shape=bearer line=124`, `shape=credential line=116`, rc 3) and four digest-bound allowlist rows (`.ufo/waves/round-93/controls/capture-intake-r93.txt`); the frozen candidate scanned capture and manifest with hits 0 (same receipt, §4).
- **Located quote, S139.txt:87 (6 words):** "glpat- followed by a 20-character string". Line 86 is the sentence that introduces it ("For example, a GitLab personal access token is identified by the pattern"), line 85 opens the rule sentence and line 84 is the `Rule-based detection` heading. The page names no alphabet and no other GitLab token prefix (the only `character` occurrence in the capture is line 87).
- **Row change (old → new):** new row, kind `docs`, tier A, status `queued` (freeze `5bad9e55`) → `mined` (integration); used-by `—` → `corpus/instruments/capture-secret-scan.py`.

### Rejected this round

- **The GitLab personal-access-token profile page,** https://docs.gitlab.com/user/profile/personal_access_tokens/, HTTP 200 on 2026-11-07 (81,326 bytes): its text carries no `glpat` occurrence (0 case-sensitive, 0 case-insensitive; `.ufo/waves/round-93/w1/ScribeEntry-receipts/06-rejected-page.txt`), so it states neither the prefix nor the length. Rejected as the C2 source and not registered — no SOURCES row, `.ufo/waves/round-93/claims.json` § frontier.rejected. Limit: the check read the raw HTML as served, not text converted by `capture-source.py`, and no capture of the page is committed.
```

**Item 3: PASS** — every element the item names is present and measured; the rejection's method limit
is stated in the block rather than glossed (Qualifier Q4).

---

## Item 4 — `LOG.md` Round 93 bullet set (lane style, rounds 88–92)

Placeholders marked `[L1]` are facts that do not exist yet (seat verdicts, integration edits, mistakes);
they are not fillable from committed bytes and are not invented here.

```markdown
## Round 93 — C1 (tranche 8: five label-named edits — the 437/438 whole-cell errata repairs, the 454 second token, the 58/144 lane-root repoints; pinned meter 1007/2001 → 1009/2000), C2 (capture-secret-scan: `gitlab-pat` on S139 and the escape-terminator left boundary)

- Read first: the r92 closure (`admitted`, `corpus/lessons/round-92-verifier-spotcheck.md:95`) and that spot-check's routed defects 1–6; the round-92 C2 counter defects D1–D5 are recorded in `.ufo/waves/round-93/claims.json` § declined. Freeze `5bad9e55` holds claims, counters, map, labels, candidate scanner and row, executed controls (`.ufo/waves/round-93/controls/`), the S139 snapshot and manifest, four allowlist rows and the SOURCES row:
  - C1 controls: no-work, partial-437-unmapped, map-454-noop, no-edit-pair-mapped, cell-437-noop, duplicate-map-row, wrong-key-454, missing-labels (rc 2), wrong-map-sha and m3-labelled-file-scope each rc 1 (missing-labels rc 2); candidate rc 0 (`C1-CONTROLS-RESULT pass controls=11`).
  - C2 controls: no-work (the round-92 instrument) and forgeries G1 no-gitlab, G2 loose gitlab length, G3 no right boundary, G4 any prefix, G5 tab-only escape, G6 any letter as escape, G7 literal-keyed, G8 path-keyed, G9 tampered instrument (the pin), G10 always-clean, row-round92 and s139-allow-rows-removed each rc 1; candidate rc 0 pinned and unpinned at seed 4242 (`C2-CONTROLS-RESULT pass controls=14`).
- C1 landing `ae53b3c6` (`corpus/knowledge/triage-thresholds.md` only): M0–M10 pass, 1009/2000, M10 kinds cell-repair=2, no-edit=3, range=3.
- C2 landing `9225954a` (`corpus/instruments/capture-secret-scan.py`, SCORECARD capability row): K1–K8 pass at seeds 638505535, 1 and 9191 (K8 50 clauses); landed sha256 `7d9d7309…` = frozen candidate, and the landed row equals the frozen candidate row.
- Sources: S139 (GitLab Docs, Secret detection: Detected secrets) opened 2026-11-07, captured through the intake gate, `queued` at the freeze → `mined` at integration; the GitLab personal-access-token profile page opened and rejected (no `glpat` occurrence, not registered). Registry 138 → 139.
- Wave w1 (13 seats): [L1 — seat verdicts, findings, routings]
- Integration: S139 `queued` → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py`; [L1 — re-anchor pass, knowledge-entry changes, any QUALITY rule minted].
- Mistakes: [L1 — M93-n, or "none minted this round"].
```

**Item 4: PASS** — form matches rounds 88–92 (heading with C1/C2 parentheticals, then
Read-first/controls, landings, Sources, Wave, Integration, Mistakes); every non-placeholder number
is from the receipts above.

---

## Defects (routed; none re-scores C1 or C2)

**D1 — `corpus/source-snapshots/round-93/manifest.json`: `"lines": 415`, the file has 414.**
Bytes: `wc -l corpus/source-snapshots/round-93/S139.txt` = `414`; `awk 'END{print NR}'` = `414`; the file
ends with a newline (`tail -c 12 | xxd` shows `…licenses\n`). The round-92 manifests use `wc -l`
(`178`/`178`, `274`/`274`, `440`/`440`), so 415 is off by one, not a different convention. Re-run:
`grep '"lines"' corpus/source-snapshots/round-93/manifest.json; wc -l corpus/source-snapshots/round-93/S139.txt`
(`03`/`07`). No frozen predicate reads the manifest's line count, so the claim is untouched; the number the
Gate block carries is 414.

**D2 — `corpus/instruments/capture-secret-scan.py:107-108`: the known-limits parenthetical cites the wrong line.**
Text: `GitLab token prefixes (S139 line 86 names only `glpat-`)`. Line 86 is `credential type, called a rule. For
example, a GitLab personal access token is identified by the pattern`; the token prefix appears on line 87.
The shape docstring at `:99` is correct (`S139 lines 86-87`). Re-run:
`git show 9225954a:corpus/instruments/capture-secret-scan.py | sed -n '106,109p'; sed -n '86,87p' corpus/source-snapshots/round-93/S139.txt`
(`04`). Cosmetic; the statement's names-only-`glpat-` reading of the page holds.

**D3 — `corpus/SOURCES.md` round-93 row-change bullet: "teaching samples" carries four rows but describes three samples.**
Text: `The page's generic-detection teaching samples matched the intake gate's `credential` and `bearer` shapes;
four digest-bound allowlist rows …`. The receipt the bullet cites says three of the four matches are the
generic-detection teaching samples (lines 116, 124, 126) and the fourth (line 139) is the finding-type list
prose. The freeze's own manifest `note` makes the same distinction ("the samples are fabricated examples: an
api_key query sample, an --api-token sample, a Bearer JWT sample and the finding-type prose"), so the bullet's
compression contradicts the bytes it cites. Re-run: `sed -n '16,26p' .ufo/waves/round-93/controls/capture-intake-r93.txt;
grep -c round-93/S139.txt corpus/instruments/capture-secret-allow.tsv` (`03`). Correct phrasing for the integration pass:
"three teaching samples and one prose line matched …; four digest-bound allowlist rows". No cell of the row changes.

## Qualifiers (not defects)

- **Q1 (capability-row gloss).** "whose last byte is alphanumeric" describes the SentinelGitHub finding
  (`\t`, `\u0020`, `%20`, `%3A`); the HTML-entity forms the same clause names end in `;`. Detection is
  unaffected (selftest `gh-escape-html-entity`, `gl-pat-*` cases at `:386-395`), so the row's list of
  forms is the operative text and the parenthetical is a summary.
- **Q2 (tier basis).** No written A/B/C legend was located in the corpus contract: `corpus/SOURCES.md` has
  no tier section, `corpus/QUALITY.md:7` says tiers are defined there, and `:15` (Q2) only requires an A or
  B row. Tier A for S139 is therefore checked as first-party documentation on the S136 precedent, not
  against a definition. Receipt `07`.
- **Q3 (scope narrowing).** The S139 page covers rule-based and generic detection and a catalogue of
  detected secret types; the row admits only the rule statement. Consistent with the registry's practice
  of a narrow scope cell, and named here so the narrowing is visible.
- **Q4 (rejection method).** The PAT-profile rejection was verified on the raw HTML as served
  (81,326 bytes, 0 `glpat`), not on `capture-source.py`-converted text, and no capture of that page is
  committed. The gate block states this limit.
