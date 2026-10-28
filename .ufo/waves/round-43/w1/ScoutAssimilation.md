# ScoutAssimilation — round 43

Seat: ScoutAssimilation. Read-only on the fleet repo, the lane tree except this file, and `/home/vgpnk/Projects/shokuknow`. No git mutation. No tool install. No campaign tool run inside shokuknow. The §10 check ran in scratch, not in `.ufo/waves/round-43/assimilation` (the prompt's `$A` path): the seat spec says scratch only.

Axes: `depth:verifiability` (the id-collision guard must be able to fail) and `coverage` (whether this round adopts a `merge/kasegi/` theme). A move that adopted a package entry would widen a frozen claim; it was not kept.

## Verdict

**Assimilation: none.**

No theme from `/home/vgpnk/Projects/shokuknow/merge/kasegi/` fits the frozen claims. No renumber map. Nothing from `SOURCES.append.md` is appended. The C2 disclosure source is a §2b source row minted this round (frozen after-state: registry `S067` `mined`, cited by the new `claim-package-gate` entry), not an adoption of a staged package row.

Frozen claims read (never edited): `.ufo/waves/round-43/claims.json`, `frozen_at_utc` `2026-10-28T16:37:07Z`, `frozen_by` KasegiR43, base `ab98fac9dce87130bc4f66de89e30650d63943dc`. C1 is the narrative-evidence instrument `corpus/instruments/r43-closure.sh` (K1–K19). C2 is the executable six-file gate `corpus/instruments/claim-package-check.py` plus an exemplar built from one public disclosed report captured this round. Neither predicate names a `merge/kasegi/knowledge/` path.

§10 of `.ufo/prompts/kasegi-round-43.md` (frozen-round clause): material from shokuknow may serve an already-frozen claim only as ordinary §2b curation (a source opened this round), never as a new or widened target. Assimilation otherwise waits.

Nearest package theme, and why it does not fit: `knowledge/corpus/knowledge/claim-packaging-and-report-quality.md` cites staged `S034` (https://zc.cnvd.org.cn/news/helpList), `S035` (https://security.360.cn/Reward/rules), `S036` (https://security.bilibili.com/static/docs/BILISRC_V1.7.pdf) — Chinese SRC scoring and report-quality rules. The lane already holds the six-file contract in `corpus/knowledge/claim-package-contract.md`. Those three staged ids are already different lane documents (lane `S034` is the MIC citizen page, `S035` the NPA commentary, `S036` the Cybozu handling policy — source cells compared below). Adopting that entry would be a new target the frozen predicate does not name.

## Package state (read-only)

`/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md` sha256 `0e6759b47595f1bce5fbf49bf0422838ff89a394b2f424d17fb17d96a09106df`.

Observed lines:

- "Nothing was written into the lane repo."
- proposed rows accepted **94**, refused **0**, knowledge entries **67**
- "lane registry currently holds **30** rows; first staged id is **S031**" — stale. Live registry is 66 rows (`S001`–`S066`). `find …/knowledge -name '*.md' | wc -l` = 67, matching the report.
- `SOURCES.append.md` sha256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`. Header comment: `corpus-expansion-1 :: staged rows for lane kasegi`. First data row is staged `S031` (HackerOne standard program policy). Last data row is staged `S124`.

## Live id-collision check

Scratch: `/fast/scratch/hyaku/kasegi-r43/ScoutAssimilation` (removed after this receipt). Disk guard before the run: `/fast/scratch/hyaku` 25% used, 606.3G free. Run UTC `2026-10-28T16:39:56Z`.

Lane worktree HEAD is `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (base is an ancestor). `git status --porcelain -- corpus/SOURCES.md` printed nothing. Ids extracted from the worktree file and from `git show ab98fac9dce87130bc4f66de89e30650d63943dc:corpus/SOURCES.md` were identical (`diff -q` empty).

Pattern (0–3 leading spaces, then the id cell), as §10 specifies:

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort
comm -12 reg-ids staged-ids > collisions
```

| list | count | range | gaps | sha256 |
|---|---|---|---|---|
| reg-ids | 66 | S001–S066 | none | `0f6a5412d24d06ba8be1a99b12389065fee9596c204af3652bbfea8ff3968dfd` |
| staged-ids | 94 | S031–S124 | none | `550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f` |
| collisions | **36** | S031–S066 | none | `0cc403967f0dfe6533347c1630f4af3ad0ea2da07142c3ed4d0b075d6263b2c4` |

Unique counts equal line counts (66 and 94). `S002` is absent from staged-ids.

Both live files have **zero** rows with 1–3 leading spaces (`grep -cE '^ {1,3}\|'` = 0 and 0). A column-zero-only pattern (`^\|`) therefore produces the same three lists on the live files (66 / 94 / 36). That agreement is not a proof the guard works; the fixture below is.

Collision ids (the scratch `collisions` file, verbatim):

```
S031
S032
S033
S034
S035
S036
S037
S038
S039
S040
S041
S042
S043
S044
S045
S046
S047
S048
S049
S050
S051
S052
S053
S054
S055
S056
S057
S058
S059
S060
S061
S062
S063
S064
S065
S066
```

Of the 36 overlapping ids, **35 source cells differ** and **1 is the same document**. The identical cell is `S042`: `IPA 脆弱性関連情報の届出受付業務における取扱いプロセス — https://www.ipa.go.jp/security/todokede/vuln/process.html`. Samples of different documents wearing one id:

- `S031` lane: CVE CNA Operational Rules v4.2.6 (`cve.org/.../CNA_Rules_v4.2.6.pdf`). Staged: HackerOne standard program policy (`hackerone.com/security/policy_versions`).
- `S032` lane: NIST SP 800-115. Staged: Bugcrowd VRT README.
- `S033` lane: e-Gov 不正アクセス禁止法 `411AC0000000128`. Staged: Bugcrowd VRT CWE mapping JSON.

No renumber was built. §10 says a nonempty `collisions` file is fixed in scratch only when rows are adopted, and adopted ids continue the lane registry with citations re-pointed by document, never by arithmetic. This round adopts nothing, so the collision list stands as a refusal input, not a map.

Forward note, not part of the count 36: staged `S067` is free in the current registry and is a different document — Microsoft Security Testing Rules of Engagement, `https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement`. Frozen C2's after-state assigns lane `S067` to the new mined disclosure row. Keeping the package's staged id would collide with the row this round mints. Another reason not to append.

## Guard proof (indented `  | S002 |`)

§10: a column-zero pattern false-greens an indented collision. Proof UTC `2026-10-28T16:40:50Z`. Scratch registry `$S/guard/corpus/SOURCES.md`: column-zero `S001`, then a row indented by two spaces whose id cell is `S002`. Scratch staged file is the single line `S002` (live staged-ids do not contain `S002`; the proof's staged side is the id the indented row carries). Status `queued`, 11 columns, so the row is census-legal rather than a malformed line the parser skips.

Column-zero extractor: reg = `S001` only; `comm -12` collisions **empty** (0 bytes, 0 lines).

0–3-space extractor: reg = `S001` and `S002`; collisions file body:

```
S002
```

`test -s` → `GUARD_NONEMPTY=yes`. The guard is not broken.

Census on that fixture (`sources-census.sh`, fleet script, scratch file only):

```
validate --today 2026-10-28 --file …/guard/corpus/SOURCES.md
file	ok	…/guard/corpus/SOURCES.md
validate_exit=0
census: file rows=2 tier.B=2 status.queued=2
census_exit=0
```

`rows=2` is the check that the indented row was parsed, not ignored. Exit 0 with both rows counted is census-valid.

Second proof, same patterns, against the **live** staged-ids: a two-line scratch registry with column-zero `S001` and indented `  | S031 |`. Column-zero `comm -12` was empty. The 0–3 pattern reported `S031`. An indented collision with a real staged id is caught; the column-zero pattern misses it.

## Not done

No write under `/home/vgpnk/Projects/shokuknow`. No write under `.ufo/waves/round-43/assimilation`. No registry append, no knowledge copy, no quarantine-slice file (not this seat). `considerthese/` is ScoutConsiderthese's item. Scratch removed after this file was written.
