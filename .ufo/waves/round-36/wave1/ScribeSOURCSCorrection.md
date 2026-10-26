# ScribeSOURCSCorrection — round 36: R9 appended correction for the S052 Search-log bullet (M35-6)

Seat: ScribeSOURCSCorrection (leaf, scribe). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims freeze / lane HEAD `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`; r35 base `3266c9937b03062d9bbc2f436e20820115ed179c`; r35 judged head `0aee0ef105395a2f1d6ace7eaeef13871bb26988`. Axis: depth:verifiability. All measurements 2026-10-26.
Writes made: this receipt only, plus scratch under `/fast/scratch/hyaku/kasegi-r36/ScribeSOURCSCorrection/` (removed before yield). No lane file was edited. No tooling installed (no `uv`/`npx`/binary install; pacman untouched).

## 1. Deliverable — exact appended text

Landing (as specified by the seat item, "a new Search-log paragraph"): append as the closing paragraph of the `## Search log` section, immediately after the round-35 CISA bullet now at `:79` (line numbers at base `b47f2cd`). Do **not** rewrite `:79`; the bullet stays byte-intact.

One physical line, 1,400 bytes including the trailing newline, sha256 `21bc6306599b0d747601aa41cf2c18d01c1384e6fd7c02c8931e83dceb6705b2`:

~~~text
- Round-35 S052 Search-log bullet correction: the CISA known-exploited-vulnerabilities bullet at `:79` (base `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`) abbreviates the S052 capture digest as `d69349e8…77e8826`, but `corpus/source-snapshots/round-35/S052.txt` hashes to `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` (1,479,694 bytes, 27,870 lines; the full digest is also printed by `corpus/source-snapshots/round-35/manifest.json` and the S052 registry row), whose last eight characters are `779e8826`; `77e8826` is not a substring of that digest, so the abbreviation should read `d69349e8…779e8826` or the full digest. The same bullet's PRE-STATE figure "7 SOURCES rows" is a whole-file line count, not a registry-row count: at the round-35 base `3266c9937b03062d9bbc2f436e20820115ed179c`, the row-restricted count `grep -E '^\| S[0-9]{3} \|' corpus/SOURCES.md | grep -ci cisa` is 5 (`S003 S008 S021 S023 S026`), while `grep -ci cisa corpus/SOURCES.md` is 7 because it also counts two `## Search log` bullets (the CVD, safe-harbor and reporting-duty sweep and the AI-assisted finding-validation sweep); at the round-36 base `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` the row-restricted count is 6 because S052's own row names CISA. The bullet at `:79` stays byte-intact; this paragraph is the correction (R9, M35-6), and its changed-file scope is `corpus/SOURCES.md` only.
~~~

The corrected suffix `779e8826` ends in `e8826`, matching the item's shorthand; the item's "the registry has 5 rows mentioning CISA: S003 S008 S021 S023 S026" is stated base-scoped, because at the round-36 base the row-restricted count is already 6 (S052's own row names CISA; still 6 after an S053 row lands). The line contains 3 `|` characters, all inside backticked code spans; safe in a bullet, not a table row.

### Landing notes (anchor drift disclosed)

- Inserting one line after `:79` (base `b47f2cd`) shifts `## Leads (unopened)` 81→82, `## Registry changes` 87→88, and the two existing round-35 correction lines `:111`/`:112` → `:112`/`:113`. Nothing in the lane cites `SOURCES.md:111`/`:112` (grep over `*.md`/`*.py`/`*.json`; only unrelated `:111` hits in other files), so no filed pointer breaks; the shift is still recorded here for the L1.
- Sibling landing: the round-36 S053 registry row (claims.json C2: registry rows 52→53) inserts one line before `## Search log`, so the CISA bullet moves `:79`→`:80` and this correction to `:81`. The pointer inside the text is base-qualified (`b47f2cd`), so it remains resolvable under R9; re-open it against the final head at landing if the L1 prefers head-line numbers.
- House precedent: the two existing corrections about this same bullet (superseded line, scope correction) sit under `## Registry changes` at `:111-:112`. The identical line is valid there as an EOF R9 bullet if the L1 prefers zero drift; content is unchanged either way.

## 2. Facts verified (command → output)

| # | Fact | Command | Output |
|---|---|---|---|
| F1 | The capture's real digest | `sha256sum corpus/source-snapshots/round-35/S052.txt`; `wc -c -l` | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`; `27870 1479694` |
| F2 | Printed suffix is invalid | `python3` on the digest string | `64 d69349e8 779e8826 False True` (len 64; prefix `d69349e8`; last 8 `779e8826`; `'77e8826' in d` → `False`; `'779e8826' in d` → `True`) |
| F3 | Old abbreviation occurs once; full digest twice | `grep -o` / `grep -c` on `corpus/SOURCES.md` | `sha256 d69349e8…77e8826` → 1 occurrence (`:79`); full digest → 2 lines (`:58` S052 row, `:108` S052 row-added line) |
| F4 | Row count at r35 base | `git show 3266c993…:corpus/SOURCES.md` → `grep -E '^\| S[0-9]{3} \|' \| grep -ci cisa` | `5`, on lines `:9 :14 :27 :29 :32` = `S003 S008 S021 S023 S026` |
| F5 | Where the 7 came from | same base file, `grep -ci cisa` and `grep -n '^## '` | whole-file `7`; `## Search log` at `:66`, `## Leads` at `:79`; extra two hits at `:69` (CVD, safe-harbor and reporting-duty sweep) and `:70` (AI-assisted finding-validation sweep) — both Search-log bullets |
| F6 | Row count at r35 judged head / round-36 base | `git show <rev>:corpus/SOURCES.md` | `6` rows (`5` above + S052 at `:58`); whole-file `10` |
| F7 | `:79` pointer re-opened | `git show <rev>:corpus/SOURCES.md \| sed -n '79p'` | at `0aee0ef` and at `b47f2cd` line 79 opens `- CISA known-exploited-vulnerabilities sweep (round 35); …` (bullet unchanged between the two) |
| F8 | Manifest provenance | `grep -rn d69349e86c5 corpus/source-snapshots/round-35/` | `manifest.json:8` carries the full digest |
| F9 | Text audit | `wc -l -c`, `sha256sum`, `grep -o '\|'` | 1 line, 1,400 bytes, sha256 `21bc6306…b6705b2`, 3 pipes (all inside code spans) |

The two defect facts are the ones minted as M35-6 in `corpus/lessons/round-35.md:269` and measured earlier in `.ufo/waves/round-35/wave1/ScribeSearchLog.md` §5a (digest) and `.ufo/waves/round-35/wave1/ScribeSOURCESRow.md` (row count). This receipt re-measured both at the cited revisions rather than copying those receipts.

## 3. R9 compliance

- Base named: `3266c993…` for the sweep's row/line counts; `b47f2cd` for the `:79`/`:58` pointers. Checked at `0aee0ef` too (F7).
- Changed-file scope named: `corpus/SOURCES.md` only.
- Appended, not rewritten: `:79` is untouched (verified by `git show` at both revisions and by this seat making no lane write); the correction is a new paragraph.
- Every number is published with its counting command (F1–F6).

## 4. Gate state

The frozen claims' C1 checks E1–E9 do not consume this correction, and the C2 kill rules do not either (`.ufo/waves/round-36/claims.json` contains no `SOURCES`/`M35-6`/`S052` predicate). This is the M35-6 fix required by the round-35 lesson and this round's item, not a claim limb; no suite output depends on it. The **only** outstanding action is the L1 applying the text at the chosen landing point — this seat cannot edit `corpus/SOURCES.md`.

## 5. Out of scope / not done

- Did not edit `corpus/SOURCES.md:79` (or any line of it), the S052 row, the capture, its manifest, the lesson, or any other lane/fleet file; no commit, no mutating git.
- Did not re-derive the bullet's other figures (fetched_bytes 1,807,090 vs snapshot 1,479,694; "2 knowledge files"), and the correction makes no statement about them.
- Did not re-fetch the upstream feed (this is a filed-bytes correction, not a freshness check).
- No sibling coordination needed; no `agent://all` message; no subagents.

## 6. Artifacts and cleanup

- Report (this file): `.ufo/waves/round-36/wave1/ScribeSOURCSCorrection.md`.
- Scratch: `/fast/scratch/hyaku/kasegi-r36/ScribeSOURCSCorrection/` held `S_<rev>.md` (read-only exports of `corpus/SOURCES.md` at `3266c993`, `0aee0ef`) and `correction.txt` (the text above); removed before yield via `rm -rf`.
- Provenance: `corpus/lessons/round-35.md:269` (M35-6), `corpus/source-snapshots/round-35/manifest.json:8`, `.ufo/waves/round-35/wave1/ScribeSearchLog.md` §5a, `.ufo/waves/round-35/wave1/ScribeSOURCESRow.md`.

Report: .ufo/waves/round-36/wave1/ScribeSOURCSCorrection.md
