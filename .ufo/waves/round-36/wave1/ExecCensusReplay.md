# ExecCensusReplay — round-36 C2 before-census replay (census validate ×2 + frozen census commands)

Seat: `ExecCensusReplay` (leaf executor, axis `coverage`). Sole writer of this receipt.
Round: kasegi-shokunin round 36, hyaku run 9. Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`.

Writes: this receipt only, plus scratch under `/fast/scratch/hyaku/kasegi-r36/ExecCensusReplay/` (deleted
after this receipt was written). Every command below is read-only: `sources-census.sh` without `--out` writes
nothing; `grep`/`awk`/`sort`/`uniq`/`sha256sum`/`stat` are reads; `git rev-parse`, `git show`, `git status`
are reads. No `git add/commit/push/fetch` and no `jj` mutation was run. No tool installs or upgrades were needed
(tooling authorization recorded as unused; nothing installed).

## Report

### 1. What bytes were measured (read before quoting any number)

`corpus/SOURCES.md` in the lane working tree is **byte-identical to the `b47f2cdf` blob**, so the numbers below
are bound to that commit, not to a transient edit:

```
$ git rev-parse HEAD                                  -> b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
$ git show HEAD:corpus/SOURCES.md | sha256sum          -> 0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba
$ sha256sum < corpus/SOURCES.md                        -> 0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba
$ git status --porcelain -- corpus/SOURCES.md | wc -l  -> 0
```

`stat -c %y corpus/SOURCES.md` = `2026-10-26 03:41:13.946987678 -0300`. Capture bracket:
`2026-10-26T15:35:23Z` (pre) → `2026-10-26T15:36:24Z` (post), re-checked sha at each end — unchanged.

Worktree quiescence at the same instants: `git status --porcelain` shows 8 entries, **all** under
`.ufo/waves/round-36/` (wave artifacts); `git status --porcelain | grep -v '^?? \.ufo/waves/round-36/' | wc -l`
= 0. No lane content file was dirty during the replay.

Pre-append state (the C2 delta this round will add is not yet present):
`grep -cE '^\|[[:space:]]*S053[[:space:]]*\|' corpus/SOURCES.md` = **0**;
`corpus/knowledge/epss-exploit-prediction-scoring.md` **absent**;
`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l` = **47**.

### 2. `sources-census.sh validate` — two runs, identical

Command (exactly as dispatched, run with cwd = `/home/vgpnk/Projects/shokunin` and repeated):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

Run 1 stdout (exit **0**), stderr empty:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

Run 2 stdout (exit **0**), stderr empty — byte-identical to run 1 (`cmp -s` → identical):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

- exit **0** in both runs (captured per run; the runner appended `EXIT=` to its own scratch capture, not to the
  script's output).
- Findings: exactly **two `W04`** lines, **S028 and S029 only** (`grep -c 'W04'` = 2; ids found = `S028 S029`).
  No `E##` code. One registry (`…/kasegi-shokunin/corpus/SOURCES.md`), lane verdict `kasegi ok`.
- Matches the dispatched expectation ("exit 0, W04 S028/S029 only").

### 3. Frozen census commands — seven run, six named categories covered

Frozen set is `/home/vgpnk/Projects/shokunin/CORPUS.md` §"Census — run from the lane root" (unchanged since
round 24; the maintained-parser note says the frozen manual examples assume column-zero input). The dispatch
names six categories; the frozen block also carries a malformed-row counter, so all **seven** commands were run
with cwd = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Each exit code was captured per command (no pipeline
exit misattribution). Outputs verbatim:

| # | frozen command | output | exit |
|---|---|---|---|
| 1 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `52` | 0 |
| 2 | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md` | `0` | 0 |
| 3 | tier histogram (`$5`) | `A=49 B=1 C=2 ` | 0 |
| 4 | status histogram (`$9`) | `mined=40 queued=9 rejected=3 ` | 0 |
| 5 | duplicate ids (`sort \| uniq -d`) | *(empty, 0 bytes)* | 0 |
| 6 | enum violations + tier inflation (`$4`/`$5`/`$9`, community@A) | *(empty, 0 bytes)* | 0 |
| 7 | mined rows whose `used-by` paths do not exist | *(empty, 0 bytes)* | 0 |

Commands 3–7 are the frozen one-liners verbatim as printed in `CORPUS.md:135-152`; stderr was empty for all
seven. All seven were run in one batch inside the 15:35:23Z–15:35:52Z window; the sha256 of `SOURCES.md` was
identical before and after the batch.

### 4. Cross-checks (so nothing in §3 is vacuous)

| check | output | exit |
|---|---|---|
| unique ids `sort -u \| wc -l` | `52` (= rows, so command 5's empty output is not a parse failure) | 0 |
| `sort \| tail -1` over ids | `S052` (ids `S001…S052`, no gaps at the top end) | 0 |
| mined rows with non-`—`, non-empty `used-by` cell | `40` (= `mined=40`, so command 7 walked every mined row) | 0 |
| sum checks | `49+1+2 = 52` rows; `40+9+3 = 52` statuses | — |

Maintained-CLI census (supplementary; same frozen bytes, confirms the greps and the CLI agree):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
kasegi	rows	52
kasegi	tier.A	49
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	40
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	52
FLEET	tier.A	49
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	40
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
census_mode_exit=0
```

`FLEET.missing 0` = the lane registry was found; `FLEET.rows 52` = the lane is the only contributor.

### 5. Corroboration against the L1's `census-before.txt`

`.ufo/waves/round-36/census-before.txt` (sha256
`920e6fd4b2e82aee969bf489a9a2a4cd97188cf84ec001b4df1c944ea5901499`, 269 B) holds the same two `W04` lines.
`diff` of its first two lines against this seat's run-1 stdout → no difference (`census_before_lines_match=yes`).
The committed before-file and this replay therefore agree on the finding set, not just the count.

### 6. Before-state the round's C2 claim will be measured against

| surface | before (this replay, at `b47f2cdf`) | frozen C2 cell |
|---|---|---|
| registry rows | **52** (`S001…S052`) | S053 appended → 53 |
| tier histogram | **A=49 B=1 C=2** | A 49 → 50 |
| status histogram | **mined=40 queued=9 rejected=3** | mined 40 → 41 |
| malformed rows | **0** | 0 |
| duplicate ids | **none** | E03 free |
| enum/tier-inflation violations | **none** | E05/E06/E10 free |
| mined `used-by` paths missing | **none** | — |
| `validate` verdict | **exit 0, W04 S028/S029 only** | exit 0 retained |
| knowledge entries | **47** | 47 → 48 |
| S053 row / EPSS entry | **absent / absent** | added |

### 7. Limits and risks

- Numbers are bound to `b47f2cdf` via the blob-identical check in §1; siblings appending S053/S054 or the EPSS
  entry after 15:36:24Z will legitimately change them — any later receipt must re-measure, not quote these.
- This replay covers the **before** side only. It does not verify the after-state, the S053 row fields, the
  capture/manifest binding, the harness counters, or the junk twin — those are other seats' items.
- `W04` for S028/S029 is a pre-existing finding carried from earlier rounds; per the script header `W` codes
  never change a clean lane's status, and both runs confirm that.
- The dispatch's phrase "three frozen census greps" resolves to the six named categories / seven frozen
  commands in `CORPUS.md`; all seven were run, so no named category is unmeasured. Nothing was skipped as
  "the third grep".
- Scratch `/fast/scratch/hyaku/kasegi-r36/ExecCensusReplay/` was removed after this receipt was written.

### 8. Retained evidence

Every command in §1–§5 was executed in this session; the verbatim stdout/stderr/exit captures existed under
the seat scratch (`census-run1.out`, `census-run2.out`, `f1-rows.out` … `f7-minedusedby.out`,
`census-mode.out`, `state*.txt`, `crosschecks.txt`, `blob-binding.txt`) and were re-read to build the tables
above before the scratch tree was deleted. No claim here rests on a file this seat did not read.

axis: coverage → before-census evidence recorded; census exit 0 twice with only W04 S028/S029; frozen
commands show 52 rows / A=49 B=1 C=2 / mined=40 queued=9 rejected=3 / no malformed, duplicate-id, enum or
dangling-used-by finding.
