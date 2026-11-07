# ScribeEntry — round 93, wave 1, attempt 1

**Seat:** ScribeEntry (leaf, non-author). **Assignment:** draft, do not commit, the round-93 evidence prose
the L1 integrates — (1) the S139 `SOURCES.md` row and row-change bullet at the freeze, (2) the C2 capability-row
text at the landing, (3) a `## Gate` block for `corpus/lessons/round-93.md`, (4) a `LOG.md` Round 93 bullet set;
all four checked against committed bytes, at `.ufo/waves/round-93/w1/ScribeEntry-receipts/drafts.md`.

**Pins used:** base `e15996bfd2f6eca4af39507a7c5973afbeca8347`, freeze `5bad9e55d3d9319446e3d9b63bc2dece633cdb68`,
C1 landing `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`, C2 landing `9225954a6e3f177af46bdb9d811c062a4353a552`.
**Scope guard:** no `corpus/` edit, no `LOG.md`/`SCORECARD.md`/`SOURCES.md`/`QUALITY.md` edit, no instrument edit,
no `git add/commit/checkout/reset/stash`, no jj mutation, no subagent, no `ask`, no `agent://all`, no network
capture beyond one read-only GET of the rejected page.

## Verdict

`drafts=4 defects=3` — four drafts written (row/bullet verified PASS, capability row PASS, Gate block PASS,
LOG bullet set PASS); three routed defects in committed bytes, none a `SOURCES.md` cell mismatch and none
re-scoring C1 or C2: D1 the round-93 manifest's `"lines": 415` (file is 414), D2 the landed scanner's
known-limits parenthetical citing `S139 line 86` where `glpat-` is on line 87, D3 the row-change bullet's
"teaching samples" covering three of its four allowlist rows (the fourth is prose). Full bytes and re-run
commands: `drafts.md` § Defects.

## Behaviour

| item | draft | result |
|---|---|---|
| 1 | S139 row + row-change bullet at `5bad9e55` | **PASS** — 11/11 cells match the capture and manifest (URL and title, `docs` in the E05 enum, tier A on the S136 precedent, scope, anchor lines 85-87 with heading at 84, teaches cell including "the page states no alphabet", `queued`, `2026-11-07`, `180d`, `—`); bullet's five row facts match; four allowlist rows and the rc-3 pre-capture refusal confirmed |
| 2 | capability row at `9225954a` | **PASS** — landed row is byte-identical to the frozen candidate row (sha256 `6d18d579…`, `diff` rc 0) and names `gitlab-pat`, the escape boundary (JSON/percent/HTML-entity terminator, `github-token` left boundary, round 93), S139, and keeps first-working round 87 as the final cell |
| 3 | `## Gate` block | **PASS** — S139 URL HTTP 200, accessed 2026-11-07 (13:55:21Z), capture sha256 `154a7e15…` at 25,370 bytes / 414 lines, quote at `S139.txt:87` = 6 words, row change `queued` → `mined` with used-by `—` → `corpus/instruments/capture-secret-scan.py`, one rejection (PAT profile page, HTTP 200, 0 `glpat`, method limit stated) |
| 4 | `LOG.md` Round 93 bullets | **PASS** — form matches rounds 88–92; freeze, controls (11 C1 / 14 C2, all rc as expected), both landings, seeds 638505535/1/9191, K8 50 clauses, registry 138 → 139 all from receipts; `[L1]` placeholders only where the fact does not exist yet (wave verdicts, integration edits, mistakes) |

The wave is ONE v1 wave of 13 seats (`w1-spec.json` items = 13; receipt `07`); no other count is asserted.

## Gates (measured)

| check | command | observed |
|---|---|---|
| S139 capture identity | `sha256sum` / `stat` / `wc -l` / `awk END{NR}` | `154a7e1535b4a245e45e3f82705c271344f59aa6c344807645fa0bc4d1e1b188`; 25,370 bytes; 414 lines both ways; trailing newline present |
| quote location and length | `sed -n 83,88p`; `printf 'glpat- followed by a 20-character string' \| wc -w` | line 87 carries the quote; 6 words; line 84 `Rule-based detection`, 85-86 the rule sentence |
| "states no alphabet" | `grep -c -i -E 'alphabet\|alphanumeric\|A-Za-z'`; `grep -o -i character \| wc -l` | 0 (rc 1); 1 occurrence, line 87 |
| manifest digests and anchors | `cat corpus/source-snapshots/round-93/manifest.json`; `source-recheck-r93.txt` | url/sha/bytes match; `S139:sha256 OK`, `Q01-glpat-20 OK anchor=87-ok`, `Q02-pattern-rule OK anchor=85-ok`, rc 0 |
| manifest line count | `grep '"lines"' round-92 + round-93 manifests`; `wc -l` | round-92 `178/274/440` = `wc -l`; round-93 `415` vs `414` → D1 |
| C2 row identity | `git show 9225954a:SCORECARD.md \| awk '/^\| capture-secret-scan \|/' \| sha256sum`; `diff` vs `c2/candidate-row.txt` | both `6d18d57978f3ae8e45da85fcf9ef6cdf2a523f1ec50955c7d496e85741e3fb40`; diff rc 0; 2,731 bytes |
| C2 row elements | `grep -o -E 'gitlab-pat\|S139\|escape terminator\|…left boundary, round 93\|\| 87 \|'` | all five patterns print; `round 87`…`round 93` each twice |
| C2 landing limbs | `grep -c 'CAPABILITY-CHECK-RESULT pass rc=0'`; `grep '^LIMB K8'` | 3 (runtime seed 638505535, 1, 9191); `K8 pass clauses=50`; `row-equal yes` |
| registry parses with S139 | `scripts/sources-census.sh validate --root … kasegi`; then an `awk` pass over the freeze bytes | census `kasegi ok` rc 0, same six inherited W04 warnings (it read the working tree, already under the L1's edit); the binding pass over `git show 5bad9e55:corpus/SOURCES.md` prints no cell-count, E05, tier or status line, S139 row `docs/A/queued/180d`, S139 URL once, rejected-page URL absent |
| rejection | `curl … personal_access_tokens/`; `grep -o -i glpat \| wc -l` | `http=200 bytes=81326`; 0 matches both cases |
| C1 landing context (LOG only) | `git diff-tree`; `c1-landing-r93.txt` | one path; `M0–M10 pass`, `after=1009/2000`, `kinds=cell-repair=2,no-edit=3,range=3` |
| controls | `grep '^CONTROL' controls/c1-controls-r93.txt c2-controls-r93.txt` | `C1-CONTROLS-RESULT pass controls=11`, `C2-CONTROLS-RESULT pass controls=14`; every named control rc as frozen |

## Touched surfaces

Written (only these, all under the seat's two assigned paths):

- `.ufo/waves/round-93/w1/ScribeEntry-receipts/drafts.md` (164 lines, sha256 `0104db529ef78a29448acd6b5de0f0078d99e96fff7924a56c002e1a1ecc87f0`)
- `.ufo/waves/round-93/w1/ScribeEntry-receipts/01-commits.txt` … `07-census-enums-precedent.txt` (sha256 in § Receipts)

Read-only: `corpus/SOURCES.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-92*.md`,
`corpus/instruments/{capture-secret-scan.py,capture-secret-allow.tsv}`, `corpus/source-snapshots/round-9{2,3}/`,
`.ufo/waves/round-93/{claims.json,controls/,l1/,c1/,c2/,w1-spec.json}`, `git log`/`git show`. Nothing under
`.ufo/state`, `.scratch`, the fleet repo, a sibling lane, or `MANIFEST.json` was touched. No git/jj write of any
kind. Scratch `/fast/scratch/hyaku/kasegi-r93/ScribeEntry` held one fetched page and was removed at exit; no
`__pycache__` (`python3 -B`), no tool install (pacman guard respected — nothing was needed, so nothing to record).

## Findings — routed, none re-scores a claim

- **D1** `corpus/source-snapshots/round-93/manifest.json` `"lines": 415` vs `414` (`wc -l` and `awk NR` agree; file
  ends with a newline; the round-92 manifests match `wc -l`). No predicate reads it; the Gate block carries 414.
- **D2** `corpus/instruments/capture-secret-scan.py:107-108` — `GitLab token prefixes (S139 line 86 names only
  `glpat-`)`; line 87 is where `glpat-` occurs. The shape docstring at `:99` (`S139 lines 86-87`) is correct.
- **D3** `corpus/SOURCES.md` round-93 bullet — "generic-detection teaching samples matched …; four digest-bound
  allowlist rows": the cited receipt calls three of the four matches samples and the fourth (`S139.txt:139`) the
  finding-type list prose. Row cells unaffected.

Qualifiers, not defects: the capability row's "whose last byte is alphanumeric" gloss does not describe the
HTML-entity forms (last byte `;`) though detection covers them; tier A rests on the S136 precedent because no
written tier legend was located (`corpus/QUALITY.md:7` points into `SOURCES.md`, which has none); the S139 scope
cell narrows a broader page; the rejection was verified on raw HTML, not converted text, with no committed capture.

## Out of scope

C1/C2 verdicts (critic, executor and mutation seats own those) — this seat verified no predicate and re-ran no
frozen counter; the meter and capability figures quoted in the LOG draft are taken from the L1's own receipts
(`.ufo/waves/round-93/l1/`). The L1's integration edits (row status/used-by, re-anchors, QUALITY rule, knowledge
entries) were not made here. The working tree changed under this seat while writing (the L1 integrating); every
row/cell check above reads a commit via `git show <rev>:<path>`. The one working-tree read — the census — had
already picked up the L1's `SOURCES.md` edit, so the enum/status/cell-count check was repeated over the freeze
bytes (`07`, appended block) and is the binding one.

## Receipts

| file | lines | sha256 | content |
|---|---|---|---|
| `01-commits.txt` | 31 | `944a6ee1a3154a56fcc38044f442940c906e5204733b0ed4a90bb691bbd2de6a` | `git log --oneline -6` (tip `9225954`), freeze parent = base, freeze/C1/C2 path sets (`git diff-tree`: C1 one path, C2 two), and `git status --porcelain corpus/SOURCES.md` printing ` M corpus/SOURCES.md` — the L1's integration edit was already in the working tree, which is why every row/cell check here reads `git show <rev>:corpus/SOURCES.md` |
| `02-sources-row.txt` | 28 | `0ce18301d2225fd7632ff14b63b0ba892063ddf1dfce9436043197a0c022aa18` | registry header, the 11 S139 cells split by `awk`, row counts `139/139`, the round-93 bullet raw, the `+` lines of the freeze diff |
| `03-s139-anchor.txt` | 87 | `e5688b5bf4fdb859539b9cae722cdd3820ed4db42bc3c05864ae13515f9e8827` | sha256/bytes/line counts and trailing-byte hexdump, lines 83-88 numbered, `glpat` occurrence, alphabet/character counts (0 / 1), manifest JSON, `source-recheck` output, intake-refusal and scan excerpt, allowlist rows = 4 |
| `04-c2-row.txt` | 77 | `ff0866b981527816e441ec4945881c6a0bc248ba7c62db1a23282efa839dc365` | landed vs candidate row sha256 and `diff` rc 0, the five element greps, SCORECARD `+` line, `c2-landing-r93.txt` limbs, scanner `_ESC_LB`/`_GL_LB`/`glpat` lines, 14 C2 controls |
| `05-c1-landing.txt` | 44 | `bf1e9c029668a3877b0f0a214567266fdcc02e80be845361fc6567eda1dcdb03` | C1 path set (one file), `--numstat` 5/5, the five changed lines, `c1-landing-r93.txt` M0-M10, 11 C1 controls |
| `06-rejected-page.txt` | 13 | `19be218506884ca803cb58091d16557787d0588713a07e905f7d5eb6b9fa3b9d` | the GET (`http=200 bytes=81326`, rc 0) and both `glpat` counts 0, with the raw-HTML/no-capture method limit |
| `07-census-enums-precedent.txt` | 95 | `48a2dce4b6665a663fa15a2af16964820e434c2edd40b1666bc0271acf833456` | census-start receipt (138 rows), E05 kind enum, Q2/Q4, absent tier legend, round-92 vs round-93 `lines` convention, S136/S139 cell comparison, r92 closure verdict and 6 routed defects, `w1-spec.json` items = 13, live census `kasegi ok` rc 0, and the appended freeze-bytes enum/status/cell/count pass |
| `drafts.md` | 164 | `0104db529ef78a29448acd6b5de0f0078d99e96fff7924a56c002e1a1ecc87f0` | the four drafts with per-item PASS/DEFECT lines, defect bytes and re-run commands, qualifiers |
