# ScribeGate — round 99 gate-record and correction audit

Read-only audit. No lane file was edited, no commit made, no subagent
dispatched. Lane HEAD at audit start `29cd305`; the integrator landed
`bedb6c4` (round-99 integration) and `2c2124f` (claims-controls erratum)
during the audit, so every citation below is against `2c2124f` unless a
revision is named. The working tree carried an unrelated sibling mutation
(observation O1); the census evidence is read from HEAD, not the working tree.

## 1. Gate-record draft (round-98 spot-check routed defect 4)

The committed block exists at `corpus/lessons/round-98.md:145-196`
(`## Appended corrections (round 99 — closes the round-98 spot-check's routed
defects 4 and 5)`), introduced by `bedb6c4`. It records S148 and S149 with a
URL, an access date, a byte/line/digest anchor and a located quote. Verified
against the rows and the wave receipt:

- `corpus/SOURCES.md:160` (S148): kind `docs`, tier `A`, status `mined`,
  opened `2026-11-07`, recheck `180d`, anchor `line 6 (1,028 bytes / 23 lines
  / sha256 b50856e4413c392ffe47fd0f212d5dd22067d52db710a7a8f93a11e9182ac319,
  fetched 2026-11-07 via the repository-files API)`.
- `corpus/SOURCES.md:161` (S149): kind `docs`, tier `B`, status `mined`,
  opened `2026-11-07`, recheck `180d`, anchors `line 5` of
  `gitlab_iam_refresh_token.md` (1,190 bytes / 26 lines / sha256
  `9b37df1e…`) and `gitlab_iam_authorization_code.md` (1,322 bytes / 27 lines
  / sha256 `52348dd6…`).
- `.ufo/waves/round-98/w1/ScoutSources-receipts/new-row-candidate-upstream-md.txt:5`
  records `fetch: GitLab API raw URL, ref=<commit>, HTTP 200 for all 30 .md
  files`; lines 14-17 carry the quotes and word counts.

Defects in the committed block (all corrected in the draft):

- **F1 word count, S148.** Committed `Quote, line 6 (17 words)`. Measured
  `len("The value is a 64-character hexadecimal session ID, with an optional
  \`cell-<ID>-\` prefix.".split())` = **13**; the receipt at line 17 also says
  `(13 words)`. The committed count is wrong.
- **F2 word count, S149.** Committed `(13 and 14 words)`. Measured **13 and
  13** for the two quoted sentences. The receipt's 17 and 16 count longer
  fragments that continue `The GitLab IAM service` / `The GitLab IAM`
  (receipt lines 14-15), not the block's quotes.
- **F3 quote fidelity.** The committed quotes escape the source's backticks as
  `\`` inside single-backtick code spans; CommonMark does not process
  backslash escapes inside a code span, so the rendered quote carries literal
  backslashes and is not verbatim. The draft uses double-backtick spans.
- **F4 provenance, round-99 lesson.** `corpus/lessons/round-99.md:39` says S148
  was "re-opened from its committed capture"; `corpus/SOURCES.md:365` says the
  same. There is **no** S148/S149 capture on disk (`find corpus -iname
  '*S148*' -o -iname '*S149*'` prints 0), and the rows record a live
  repository-files API fetch, not a capture path. The round-98 appended block
  is accurate ("from the rows in `corpus/SOURCES.md` and the round-98 wave's
  receipts"); the round-99 lesson and SOURCES bullet overstate the provenance.

Draft: `.ufo/waves/round-99/w1/ScribeGate-receipts/appended-corrections-draft.md`.

## 2. Correction sweep (round-98 spot-check routed defect 5)

**Registry counts** (`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|
S[0-9]{3} \|'`):

```
2133f5bd 147   (round-98 base)
12bb2f98 147   (freeze)
e2caf4a1 147   (C2 landing)
e2d3de7b 147   (C1 landing)
2790774  149   (round-98 integration)
6195db3  149   (round-99 base / freeze)
2c2124f  150   (round-99 HEAD)
```

`git log --oneline -S '| S148 |' -- corpus/SOURCES.md` and the same for
`| S149 |` print only `2790774`. So the round's **landing** commits were
`147 → 147`; the **integration** added S148/S149 and closed the round at
`149`. The committed block's sentence "the round landed **147 → 149**"
conflates the two; the SCORECARD bullet's `(no new row)` is false at the
round's close, and the lesson's `147 → 147` is true only for the landing.
The draft states the split.

**Superset wording.** Targets verified at HEAD:
`SCORECARD.md:3396` (`the five shapes widened to S140's punct/space/EOL
class`) and `corpus/lessons/round-98.md:75` (`restores S140's own right
boundary on five shapes`). The C2 erratum in
`.ufo/waves/round-98/claims.json` says `(?![A-Za-z0-9])` is a **strict
superset** of S140's `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` and records
156 of 256 right-boundary bytes. An independent Python witness matches `é`,
`Ω`, `\x00` and `中` with `(?![A-Za-z0-9])` and not with S140's class, so the
superset claim holds; the regex is unchanged. The committed block's superset
correction is correct.

**S140 `used-by`.** Base `2133f5bd` and C2 landing `e2caf4a1` carry only
`corpus/instruments/capture-secret-scan.py`; `2790774` and HEAD carry five
paths. Four were added:
`github-refresh-tokens-and-gitlab-jwt-tokens.md` (round-95 entry),
`gitlab-remaining-token-families.md` (round-97 entry),
`gitlab-routable-and-versioned-token-forms.md` (round-96 entry) and
`gitlab-iam-ci-build-and-session-token-shapes.md` (round-98 entry). The
committed block says "four" but enumerates `remaining-token-families`,
`iam-ci-build` and "the round-97 entry itself" — the round-97 entry **is**
`gitlab-remaining-token-families.md`, so the enumeration names two distinct
paths and omits the round-95 and round-96 entries (F5).

**Redaction count.** The committed block's final paragraph says `53 synthetic
session values, one ... marker each`. Measured at HEAD: 8 + 12 + 18 + 19 =
**57** markers; `git show a3db47e --numstat` shows 8/8, 12/12, 18/18, 19/19
(the line counts are unchanged); `git show a3db47e` adds 57 marker lines and
removes 64 64-hex values (some lines held two values; only the matched value
was replaced). `.ufo/waves/round-99/controls/redaction-r99.txt` records **4**
lines (the first matched line per file), not 57 (F6).

Draft: `.ufo/waves/round-99/w1/ScribeGate-receipts/correction-sweep-draft.md`.

## 3. Round-99 SOURCES schema check (S150 row and change-log bullet)

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kasegi` prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL
warnings (S028, S029, S072, S076, S080, S085, S143) and no E-codes
(`ScribeGate-receipts/census-validate.txt`).

S150 row (`corpus/SOURCES.md:162`, inside `## Registry`):

- split on `|` → 13 fields → **11 cells**;
- `literal pipe inside a cell: False`;
- `id='S150' kind='code' tier='B' status='mined' opened='2026-11-07'
  recheck='180d'`; `recheck valid NNd: True`; `opened valid ISO: True`;
- both `used-by` paths exist on disk (`corpus/instruments/capture-secret-scan.py`,
  `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`);
- the anchor's `HTTP 200, 128,120 bytes, sha256 aa60d7af…` matches the
  round-99 bullet and the lesson's Gate.

Round-99 bullet (`corpus/SOURCES.md:365`): prose, not a table row; no literal
`|`; states `Registry 149 -> 150 rows`, which matches the measured counts
(`6195db3` 149, HEAD 150). No E12 (row outside Registry) and no E01/E09.

Observation (not a schema failure): the census validator's E11 checks only
that a `used-by` path exists, not that the file cites the row. `grep -n 'S150'
corpus/instruments/capture-secret-scan.py` prints 0 (and the same for S148,
S144); the instrument implements the ground but names no S-row. The S150
`used-by` cell is therefore substantively right but not citation-verified.

## 4. Round-99 knowledge entry citations at the C2 landing

At `a3db47e7`, `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`
(88 lines):

- `capture-secret-scan.py:N` citations: **0**. The entry mentions the
  instrument twice, both without a line number: the `recheck:` line (line 5,
  `python3 -B corpus/instruments/capture-secret-scan.py --selftest`) and line
  69 (`corpus/instruments/capture-secret-scan.py --selftest` covers twelve
  separator positives). The requested in-range check is therefore **vacuous**
  for this entry.
- The entry's source citations are in range:
  `S140:293/480/497/549/550` ≤ 563; `S144:356/362` ≤ 418;
  `S148:6` ≤ 23; `S149:5` and `S149:5-6` ≤ 26.
- The committed census (`git show HEAD:corpus/instruments/citation-survival.md`)
  has 83 `capture-secret-scan.py:` rows, all `| in range |` at total 737, and
  the entry's `corpus/source-snapshots/round-96/S144.txt:356` row is
  `INTERNAL … 356 | 418 | in range`.
- Coverage gap: the entry's bare `S140:293`, `S148:6`, `S149:5` citations are
  not path-like and the census extracts none of them (`S140.txt:293`,
  `S148`, `S149` rows: 0 in the committed census); S148/S149 have no lane
  capture, so the census cannot verify those citations at all.

## Findings

| # | severity | finding | evidence |
|---|---|---|---|
| F1 | medium | committed block's S148 quote is 13 words, not 17 | `ScribeGate-receipts/evidence.txt`; receipt line 17 |
| F2 | medium | committed block's S149 authorization quote is 13 words, not 14 | `evidence.txt`; receipt lines 14-15 |
| F3 | low | quotes are not verbatim (escaped backticks inside a code span) | committed block lines 158, 168 and 170 |
| F4 | medium | round-99 lesson and SOURCES bullet say S148 has a "committed capture"; none exists | `find corpus -iname '*S148*'` = 0; `corpus/lessons/round-99.md:39`; `corpus/SOURCES.md:365` |
| F5 | medium | S140 used-by enumeration names three items for two distinct paths and omits two of the four added | `evidence.txt` (S140 cells at `2133f5bd`/`2790774`) |
| F6 | medium | redaction count is 57, not 53; the receipt covers 4 of 57 lines | `evidence.txt`; `redaction-r99.txt` |
| F7 | medium | "the round landed 147 → 149" is true only at the integration; the landing commits are 147 | `evidence.txt` |
| F8 | low | the lesson's `## Learning` quote "S140's … class" does not match the actual sentence "restores S140's own right boundary" | `corpus/lessons/round-98.md:75` |
| F9 | medium | census header and body disagree by one citation (pinned 2607 vs body INTERNAL 2608; host-inclusive 2683 vs RESOLVES+INTERNAL 2684) with no `confined:` line in the artifact | committed census lines 7-8 and 31-34; instrument `census-at-rev.py:146-156` |
| F10 | low | used-by cells for S144/S148/S150 name the instrument, but the instrument cites no S-row (0 hits) | `grep -n 'S150\|S148\|S144' corpus/instruments/capture-secret-scan.py` |

## Out-of-scope observations

- **O1 — working-tree census mutation by a sibling.** At 19:27:37 the working
  tree's `corpus/instruments/citation-survival.md` and `.tsv` were modified;
  the working-tree census carries 1250 `/fast/scratch` occurrences and the
  path `/fast/scratch/hyaku/kasegi-r99/CriticClaimsC1/D2/w/extract-a3db47e71fe2/tree`,
  while `git show HEAD:corpus/instruments/citation-survival.md | grep -c
  'fast/scratch'` prints 0. I did not write it; the census evidence in this
  report is from HEAD. The working tree is not a stable citation base while
  the wave runs.
- **O2 — the census's 1-citation gap.** The committed census's pinned numerator
  (lane 2607/8026) is one less than the body's INTERNAL count (2608) because
  one `..` walk-out is confined out of the numerator; the header has no
  `confined:` line, so the artifact alone cannot reconcile 2607 with 2608 or
  the host-inclusive 2683 with the class-table sum 2684. The `--check` output
  prints `confined=1`; the artifact does not.

## Tool installs

None.

## Artifacts

- `.ufo/waves/round-99/w1/ScribeGate.md` (this report)
- `.ufo/waves/round-99/w1/ScribeGate-receipts/appended-corrections-draft.md`
- `.ufo/waves/round-99/w1/ScribeGate-receipts/correction-sweep-draft.md`
- `.ufo/waves/round-99/w1/ScribeGate-receipts/evidence.txt`
- `.ufo/waves/round-99/w1/ScribeGate-receipts/schema-check.txt`
- `.ufo/waves/round-99/w1/ScribeGate-receipts/citation-check.txt`
- `.ufo/waves/round-99/w1/ScribeGate-receipts/census-validate.txt`

VERDICT: item 1 (S148/S149 Gate records) — DRAFTED; the committed block records both rows with URL, access date and a located quote, but two of three word counts are wrong (17→13, 14→13) and the quotes are not verbatim; the corrected block is at `ScribeGate-receipts/appended-corrections-draft.md`.
VERDICT: item 2 (correction sweep) — DRAFTED; the superset correction is verified (strict superset, 156/256 boundary bytes), the 147→149 correction is true at the round's close (`2790774`) but not at the landing commits (`e2caf4a1`/`e2d3de7b` are 147), and the S140 used-by enumeration is wrong (four added, three named with one duplicate).
VERDICT: item 3 (SOURCES schema) — PASS; S150 has 11 cells, no literal pipe, valid `180d` recheck, valid opened/kind/tier/status, existing used-by paths; the round-99 bullet states 149→150 and matches; the validator prints `kasegi ok` rc 0 with seven inherited W04 warnings and no E-codes.
VERDICT: item 4 (knowledge-entry `capture-secret-scan.py:N` citations) — VACUOUS; the round-99 entry has zero such citations at `a3db47e7`, its source citations are in range (S140 ≤ 563, S144 ≤ 418, S148:6 ≤ 23, S149:5/5-6 ≤ 26), and the census's 83 instrument citations are all in range at 737 lines.
