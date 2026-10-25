# QuarterCounters — declared-counter freshness (round 24, read-only)

Scope: every counting command written into `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md` for rounds 22, 23 and the move log, re-run read-only against the current committed tree (`master` = `c2480b143120364728b40397926ffcf30a7309c8`; frozen claim base `d0a3f6a…` is an ancestor, confirmed by `git merge-base --is-ancestor`). Nothing edited; all scratch output under `/tmp/qc24/`.

Headline: **no counter is a dead instrument** — every path named stays in tree, no `exit 127`, no moved file. The staleness that exists is *value* staleness and *bytes-dependence*, in four places (F2–F5) plus one live-tree hazard (F1).

---

## F1. The lane worktree is dirty mid-round; resolver-digesting counters are now checkout-dependent (HAZARD, observed live)

`git status --porcelain` was clean at my first probe and dirty minutes later at `/tmp` mtime `2026-10-25 04:14:32`:

```
 M corpus/instruments/resolve.py
 M corpus/instruments/source-recheck.py
?? corpus/instruments/capture-source.py
?? corpus/instruments/resolve-dispatch-check.py
?? corpus/instruments/resolve-dispatch-fixtures.json
?? corpus/source-snapshots/round-24/
```

`git diff HEAD --stat -- corpus/instruments/resolve.py` = `1 file changed, 14 insertions(+), 7 deletions(-)`, the round-24 brace/glob dispatch repair (empty-alternative expansion `{,x}`, glob dangling-symlink skip) — i.e. a round-24 C1 writer is editing the lane tree in place.

Consequence for the round-23 counter it feeds: `corpus/instruments/mirror-containment-check.py:43` sets `DEFAULT_RESOLVER = <instruments>/resolve.py`, and the receipt digests *working-tree* bytes:

| resolver bytes used | command | exit | printed digest cell |
|---|---:|---:|---|
| committed `HEAD` (`git show HEAD:corpus/instruments/resolve.py`, sha `690153ad…ea2d`) | `python3 corpus/instruments/mirror-containment-check.py --resolver /tmp/qc24/head-resolve.py` | 0 | `resolver_sha256=690153ad…ea2d`, `matrix_sha256=d05b1e0c…b809`, 24/24 |
| dirty worktree | `python3 corpus/instruments/mirror-containment-check.py` (row's command verbatim) | 0 | `resolver_sha256=035f8844e66357f6dbe6f1158776978f2ce1103108e222d0746afdef9521b661`, 24/24 |

So `SCORECARD.md:437` (`resolver_sha256=690153ad…ea2d`) is reproducible from **committed** bytes and remains true for HEAD, but a fresh reader running the row's command today gets a different digest cell while the pass count stays 24/24. The pass/fail claim survives; the digest claim no longer prints. All other counters below were re-run against committed instrument bytes where the instrument is dirty (recheck loop and `source-recheck.py` done both ways; identical results).

## F2. Round-23 C1 result-table cells `7/13` and `13/13` do not reproduce with committed checker bytes (STALE CELLS)

`SCORECARD.md:398` claims, for the *first* matrix: do-nothing `matrix 7/13, exit 1`, landed `matrix 13/13, exit 0`, `matrix_sha256=5e61a33e…b5e76a9`. The row names no fixture path; its command uses the default fixtures, which now hold 24 cases. Reconstructing the named matrix from history (`git show 953c278:corpus/instruments/mirror-containment-fixtures.json` → sha256 `5e61a33ed5fa5305`, 13 cases — confirms the digest cell) and running it with the *exact* resolver bytes of that commit plus the baseline:

```
13-case + baseline resolver   exit 0  cases=13 escape=6 controls=7 pass=6  fail=7
13-case + 953c278 resolver    exit 0  cases=13 escape=6 controls=7 pass=12 fail=1
```

Not `7/13` and not `13/13`. The single extra failure in both runs is the checker's newer `resolved_path` assertion, which did not exist at the 13-case landing:

```
lane-relative-parent-internal-control  control expect=INTERNAL actual=INTERNAL FAIL path_check=path-outside-internal
```

Escapes behave as the row says (`0/6 GONE`, all `actual=MIRROR-EQUIVALENT`, `path_check=gone-with-path`). Verdict: the two pass-count cells describe the pre-`bf9ce02` checker as well as the pre-24-case matrix; the errata's phrase "describe the first matrix" (`SCORECARD.md:436-438`) under-describes the dependency, and no committed pointer names the 13-case fixture, so the cells cannot be re-derived from the command as written.

## F3. Round-23 named receipts were overwritten; the `5e61a33e` cell is false for those files (STALE POINTER)

`SCORECARD.md:399-400` says both receipts print `matrix_sha256=5e61a33e…b5e76a9`. Current committed contents:

```
.ufo/waves/round-23/c1-baseline.json  totals={'cases':24,'pass':12,'fail':12}  matrix_sha256=d05b1e0cf62738ac  resolver=d6a3c3f1…
.ufo/waves/round-23/c1-fixed.json     totals={'cases':24,'pass':24,'fail':0}   matrix_sha256=d05b1e0cf62738ac  resolver=690153ad…  generated_at=2026-10-25T06:52:43Z
```

The errata's cells (`SCORECARD.md:434-438`) reproduce exactly — `12/24` exit 1 do-nothing, `24/24` exit 0 landed, `d05b1e0c…b809`. The result-table cells do not, and the file names are the same. Only the matrix version differs.

## F4. Coverage-map counter: claimed 33, now 36 (LIVE INSTRUMENT, UNTAGGED SNAPSHOT VALUE)

```
awk '/^## Coverage map/{f=1;next}/^## /{f=0} f&&/^\| /{n++} END{print n-2}' corpus/README.md
```

| tree | output |
|---|---:|
| `94aace2` (r22 before) | 25 |
| `c8b719d` (r22 after) | 33 |
| `922a4dd` (r23 base) | 33 |
| `HEAD` | **36** |

Diff `922a4dd`→`HEAD` for that section is exactly the three round-23 rows: `Multi-party coordination (round 23)`, `CNA assignment rules, current version (round 23)`, `CRA manufacturer reporting duties (round 23)`. Instrument live, before/after claims correct at their own commits; the move-log cell `map rows 33` (`SCORECARD.md:192`) and the r22 row's `25 → 33` no longer describe the committed tree because no round tag or date bounds them.

## F5. SOURCES census: claimed 27 rows, now 31; the seven commands are not written down (STALE VALUE + UNRECORDED COMMAND)

`SCORECARD.md:301` claims "all seven contract census commands run clean … 27 rows (A=25 C=2; mined=15 queued=10 rejected=2), malformed 0, dup/enum/missing-used-by empty", with outputs at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22.md:105-115`. **The seven command texts exist nowhere in committed bytes** — `grep -rn "tier histogram\|malformed (must be 0)\|enum/tier-inflation" --include='*.md'` returns only those output lines (`corpus/lessons/round-22.md:109,110,113`), no command. The claim is therefore unfalsifiable as written.

Reconstruction (table parser over `| S### |` rows, 11 cells, used-by `.md` existence check), which reproduces the r22 block exactly at its own commit:

| tree | rows | malformed | tier | status | dup | enum-bad | missing-used-by |
|---|---:|---:|---|---|---:|---:|---:|
| `c8b719d` | 27 | 0 | A=25 C=2 | mined=15 queued=10 rejected=2 | 0 | 0 | 0 |
| `HEAD` | **31** | 0 | **A=29 C=2** | **mined=19 queued=9 rejected=3** | 0 | 0 | 0 |

`HEAD` addition is S028–S031 (r23), so the drift is content, not instrument. `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = **31** vs the claimed 27.

## F6. Round-22 resolver census: no configuration reproduces all three cells (SELF-REFERENCE, ±1)

`SCORECARD.md:351-353` claims base `skill=32/506 corpus=140/1212 all=156/1539`, round-22 `skill=39/513 corpus=187/1259 all=203/1586`. Reproduced with `git archive <rev> | tar -x` + that export's own `resolve.py` (never the live tree):

| export | as-committed | with generated `citation-survival.{md,tsv}` removed |
|---|---|---|
| `94aace2` | skill=32/506 corpus=**141**/1212 all=**157**/1539 | skill=**31**/506 corpus=**141**/1212 all=156/1539 |
| `c8b719d` | skill=39/513 corpus=**188**/1259 all=**204**/1586 | skill=**38**/513 corpus=**188**/1259 all=203/1586 |

The corpus numerator is +1 in all four runs; skill/all flip with the presence of the instrument's own generated report (only `citation-survival.md` is excluded via `GENERATED_REPORT`, `resolve.py:137` — the `.tsv` is not). The r22 fixed-point disclosure ("each recording pass moves the rate < 0.1 pp") is real and now quantified as a ±1-cell dependence, but the recorded base and round-22 cells cannot both be produced today from committed bytes in one configuration, and no command text beside them names the configuration.

---

## F7. Counter ledger (everything else re-ran and still matches)

| # | SCORECARD anchor / row | command (as written) | exit | observed | claim | verdict |
|---|---|---|---:|---|---|---|
| 1 | `:339` r22 C1 | `for k in source verified-at recheck; … echo "$k $n/25"` | 0 | `source 25/25`, `verified-at 25/25`, `recheck 25/25` | 25/25 ×3 | MATCH |
| 2 | `:340` r22 C1 | recheck-exit loop | 0 | `2 0` / `23 1` | 23 fail closed, 2 pass | MATCH (also with committed `source-recheck.py`) |
| 3 | `:342` r22 C1 | git-prefix anchor loop | 0 | `25 0` (25 files, 0 bad) | all original lines prefix of current | MATCH |
| 4 | `:343` r22 C1 | `grep -c 'r22 correction' … \| awk '{s+=$2}'` | 0 | `31` | 31 dead-path markers | MATCH (`grep -o '\[r22 correction'`=31; the 25 headings read "round-22 correction", no double count) |
| 5 | `:344` r22 C1 | presence-wording sweep | 0 | `5` | 5 residual | MATCH |
| 6 | `:346` r22 C2 | `grep -cE '^\| F0[1-5] .*\| admitted \|' corpus/README.md` | 0 | `5` | 5/5 | MATCH |
| 7 | `:347` r22 C2 | coverage-map awk | 0 | `36` | 33 | **DRIFT (F4)** |
| 8 | `:348` r22 C2 | `grep -cE '^## (Core\|Frontier\|Adjacent)' PROVINCE.md` | 0 | `3` (0 at `94aace2`) | 0 → 3 | MATCH |
| 9 | `:349` r22 C2 | SOURCES row grep | 0 | `31` | 27 | **DRIFT (F5)** |
| 10 | `:349` r22 no-harm | `density.py SKILL.md --label r22` | 0 | mean **154.0**, 19 blocks, block 19 `155.6`, 652 cites; identical at `c8b719d` | mean 154.0 → 154.0, block 155.6 | MATCH |
| 11 | `:349` r22 no-harm | `anchorcheck.py SKILL.md` | 0 | `7 in-range, 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` | 0 bad, PIN-BROKEN=0 | MATCH |
| 12 | `:351` r22 prose | resolver census | 0 | see F6 | see F6 | **PARTIAL (F6)** |
| 13 | `:399` r23 C2 | `grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md` | 0 | `3` (0 at `922a4dd`) | 0 → 3 | MATCH |
| 14 | `:399` r23 C2 | `grep -cE '^\| F0[1-8] .*\| admitted \|' corpus/README.md` | 0 | `8` (5 at `922a4dd`) | 5 → 8 | MATCH |
| 15 | `:453` errata | `awk -F'\|' '$2 ~ /^ *F0[1-8] / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | 0 | `8`; F06–F08 variant `3` | 8 / 3 | MATCH |
| 16 | `:400`/`:455` r23 C2 | `source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S0xx` | 0 ×4 | S018, S029, S030, S031 all exit 0 (full manifest: 36 checks `OK` = 4 `sha256` + 32 quotes); `S999` exit 2 `not-listed` | four exit 0 | MATCH (identical with committed `HEAD` instrument bytes, sha `5f72b4c0…`) |
| 17 | `:456` errata | three failing controls (digest / missing / fabricated quote), manifests copied to `/tmp` | 1 / 2 / 1 | `sha256 MISMATCH` / `source UNAVAILABLE reason=not-listed` / `quote-not-found` | 1/2/1 | MATCH |
| 18 | `:398` r23 C1 | `mirror-containment-check.py --resolver .ufo/waves/round-23/c1-baseline-resolver.py` | 1 | `cases=24 escape=12 controls=12 pass=12 fail=12`, `matrix_sha256=d05b1e0c…b809`, `resolver_sha256=d6a3c3f1…`; escapes `0/12 GONE`, controls 12/12 | errata `0/12 GONE`, 12/24, exit 1 | MATCH (errata); result-row `7/13` **STALE (F2)** |
| 19 | `:437` errata | containment on committed resolver bytes | 0 | `pass=24 fail=0`, `resolver_sha256=690153ad…ea2d`, `matrix_sha256=d05b1e0c…b809` | 24/24, exit 0, same digests | MATCH from HEAD bytes; digest diverges on the dirty worktree (F1) |
| 20 | claims C1-A before-control (`.ufo/waves/round-24/claims.json`) | per-entry `recheck:` loop over the 8 frontier entries | 0 | F06/F07/F08 `0`; F01–F05 `2` (`S001:source UNAVAILABLE reason=not-listed`) = **3/8** | 3/8, F01–F05 exit 2 | MATCH |
| 21 | `:190` move log r20 | lesson pointer | 0 | `corpus/lessons/round-20-recensus.md` present | exists, no scalar | MATCH |
| 22 | `:191` move log r22 | rows 1/2/4 counters | 0 | 25/25, 23 fail closed, 31 markers | same | MATCH |
| 23 | `:192` move log r22 | frontier grep + coverage awk | 0 | `5`, `36` | 5/5, 33 | frontier MATCH, map **DRIFT (F4)** |

## Stale instruments — exact form

No counter is missing-file stale. The four that no longer yield their declared number:

1. `SCORECARD.md:347`/`:192` coverage-map awk — 33 declared, **36** printed (three r23 rows; instrument live).
2. `SCORECARD.md:301`/`:349` SOURCES row grep — 27 declared, **31** printed (S028–S031).
3. `SCORECARD.md:398` containment pass cells — `7/13` and `13/13` declared, **6/13** and **12/13** printed against the matrix the row's digest names; extra failure `lane-relative-parent-internal-control FAIL path_check=path-outside-internal`.
4. `SCORECARD.md:399-400` receipt digest cell — `5e61a33e…b5e76a9` declared for named files that now hold `d05b1e0c…b809`.

## Live instruments with checkout-dependent values (not stale, but not stable either)

- `mirror-containment-check.py` default resolver digest — `690153ad…` (HEAD) vs `035f8844…` (dirty worktree), pass count unchanged 24/24.
- `resolve.py` census — ±1 cell on whether its own generated `citation-survival.md`/`.tsv` are present in the scanned tree.

## Remaining unknowns

- Whether the round-24 in-flight edits (F1) are a contract breach by a writer seat or an L1-sanctioned in-tree edit: not determinable from this seat, and not judged here.
- `corpus/lessons/round-22.md:105-115` records the seven SOURCES outputs but no commands; whether the original command set differed from my reconstruction cannot be proven from committed bytes. My reconstruction reproduces all seven r22 values exactly at `c8b719d`, which is consistent with, not proof of, identity.
- `.ufo/waves/round-24/c1-counterA-before.txt` exists (untracked); I did not use it as evidence — every number above is from my own runs.

Tooling: no installs or upgrades this session.
