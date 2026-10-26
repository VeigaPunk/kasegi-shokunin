# ExecIdCollisions — round-35 assimilation: id-collision check + quarantine slice

Seat `ExecIdCollisions` (executor, wave 1, round 35). Judged on `depth:verifiability`, `coverage`.
Scope of this seat: the frozen non-claim frontier item `assimilation` only —
`.ufo/waves/round-35/claims.json` `non_claim_frontier_items.assimilation` (`sha256
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`). I claim no axis score, edit no frozen
claim and judge no claim; the L1 integrates and decides.

Write scope: `.ufo/waves/round-35/assimilation/` (the assignment's own `mkdir -p "$A"` target) and this
receipt. Nothing else in the lane was written; `corpus/SOURCES.md` is untouched (append-only registry; **no
append was performed**), `/home/vgpnk/Projects/shokuknow` was read-only throughout, none of its campaign
tools (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py`) was invoked, no
git/jj mutation was run, and no package/network tool was installed or upgraded (zero tooling actions).

Measurement window `2026-10-26T06:28Z`–`06:41Z`. Lane work tree at first read: head `da2d3c6`
("round-35: wave-1 spec + dispatch (64 seats, v2)"), base `3266c993…`, claims-freeze `617496b9…`.
`git status --porcelain .ufo/waves/round-35/assimilation` → `?? .ufo/waves/round-35/assimilation/` (untracked;
the L1 commits).

## Inputs, read this seat

| path | sha256 | shape |
|---|---|---|
| `corpus/SOURCES.md` | `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6` | 105 lines, **51** registry rows `S001`–`S051`, no gaps, no duplicate ids |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` | `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` | 100 lines / 89718 B, **94** staged rows `S031`–`S124`, ascending, no duplicates, 11 columns (same column count as the lane table) |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.json` | `8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b` | 67 knowledge files in the package |
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` | 375 lines, unchanged since round 34 |
| `corpus/README.md` | `876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29` | 17 frontier rows `F01`–`F17` (`F18` not yet on disk) |
| `corpus/QUALITY.md` | `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` | entry bar Q1–Q10, record R1–R26 |
| `SCORECARD.md` | `31ebb1ea8afacb3c70161b67c2c6cbe1649c28e85f9849952f36a49ffce337e1` @06:29Z → `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` @06:38Z | moved by a sibling seat mid-window; no figure below depends on it |

Staged entry digests (read-only, unchanged from round 34's record): `program-scope-rules-and-asset-boundaries.md`
`120d8cd5d50b` 39 L · `claim-packaging-and-report-quality.md` `6ad64d785f8f` 45 L ·
`cn-crowdsourced-testing-roles-and-conduct.md` `a5302aaf0b9a` 45 L ·
`chinese-crowd-testing-national-standard-2026-10-23.md` `6c15d9411424` 45 L ·
`chinese-criminal-thresholds-and-authorisation.md` `1660c00c1636` 57 L ·
`chinese-program-severity-instrument.md` `442e0f2bfb08` 41 L ·
`program-severity-ladders-and-reward-scales.md` `35de5f8b19ed` 50 L. Lane same-name entry
`corpus/knowledge/program-severity-ladders-and-reward-scales.md`
`6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6`, 67 L.

---

## 1. Id-collision check — the assignment's block, run verbatim

```
S=/home/vgpnk/Projects/shokuknow; A=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-35/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Exit codes `0 0 0`. Counts: `reg-ids=51`, `staged-ids=94`, **`collisions=21`**, range `S031..S051`.
`uniq -d` on both lists → empty (no duplicate ids on either side). A second, independent derivation of the
staged ids from the package's `source:` header lines (`grep -ohE '^ {0,3}source:[[:space:]]*S[0-9]{3,}'` over
the 67 knowledge files, `sort -u`) also yields **94** ids, and `comm -3` against the row-derived list prints
**0 lines** — the row table and the `source:` headers name the same id set.

Artifact digests (lane copies):

```
a262e5f46ca2407263cc9eb15b56686f61c5c011bb65d7d130fbd08af8ed0974  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
e7718d617b04972a00d91124bf8c8b38219e08a7980db17104654cb83f299740  collisions
```

`staged-ids` is byte-identical to round-34's committed `550a0129…`, so the package id set did not move between
rounds; `reg-ids`/`collisions` differ from round-34's `ecc9c3b9…`/`dcfd73c7…` only because the registry grew
from 50 to 51 rows (`S051`, round 34) — `collisions` gained exactly `S051`.

### Registry id list (51, `reg-ids`)

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010
S011 S012 S013 S014 S015 S016 S017 S018 S019 S020
S021 S022 S023 S024 S025 S026 S027 S028 S029 S030
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050
S051
```

### Staged id list (94, `staged-ids`)

```
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050
S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070
S071 S072 S073 S074 S075 S076 S077 S078 S079 S080
S081 S082 S083 S084 S085 S086 S087 S088 S089 S090
S091 S092 S093 S094 S095 S096 S097 S098 S099 S100
S101 S102 S103 S104 S105 S106 S107 S108 S109 S110
S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124
```

### Collisions (21, `collisions`) — the full file

```
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050
S051
```

The frozen claims expect a non-empty collision file (standing `S031…` collisions; round-34 rerun 21), and that
is what the live tree produces. **Nothing was fixed in the lane**: the registry is append-only and renumbering
stays scratch-side (§4). A non-empty collision file is not a defect in the lane; it is the guard working.

## 2. Guard proof — the indented-row fixture, proven before any append decision

The guard is the *pattern*, so it is proved on a fixture, not on the live file (where both patterns happen to
agree at 51). One scratch registry, `sha256 ee8088e5208f4c215881858ac05088008847446ccd2c4d393b604edfe4fb842f`
(the same fixture bytes round 34 used), carries `S001` at column 0 and a **2-space-indented** `S031` row:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | x — https://example.com/a | docs | A | s | a | t | mined | 2026-10-01 | 90d | — |
  | S031 | y — https://example.com/b | docs | A | s | a | t | mined | 2026-10-01 | 90d | — |
```

`bash .ufo/waves/round-35/assimilation/collide-check.sh <registry> <staged> <wide|col0>` (embedded at
`collide-check.sh`, `sha256 6d17e641e9439c38536f69797e186704248e763346ac31a68ae9bd26f9dbf917`):

| run | registry | pattern | output | exit |
|---|---|---|---|---|
| guard, wide | fixture above | `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | `reg_ids=2 staged_ids=94 collisions=1 ids=S031` | 0 |
| guard, column-0 | fixture above | `^\|[[:space:]]*S[0-9]{3,}` | `reg_ids=1 staged_ids=94 collisions=0 ids=` | 0 |
| negative control | `S901`-only fixture (`scratch-registry-noncollide.md`, `sha256 45a598c903ba…`) | wide | `reg_ids=1 staged_ids=94 collisions=0 ids=` | 0 |
| live tree | `corpus/SOURCES.md` | wide | `reg_ids=51 staged_ids=94 collisions=21 ids=S031 … S051` | 0 |
| live tree | `corpus/SOURCES.md` | column-0 | identical (`reg_ids=51 … collisions=21`) | 0 |
| fail-closed | absent path | wide | `grep: … No such file or directory` / `reg_ids=0 … collisions=0` | **2** |

**Verdict: the guard is not broken.** An indented row that the staged set collides with produces a non-empty
`collisions` under the declared 0–3-space pattern (1, `S031`) and is *missed* by a column-0-only pattern (0) —
the wider pattern is load-bearing, not decorative. The negative control shows the check is not simply
always-non-empty, and a missing registry fails closed at exit 2 rather than reporting "no collisions".

Indent boundary, measured (disclosed as a limit, R8): 3-space indent → caught (1); **4-space indent → not
caught (0)**; tab indent → not caught (0). All 51 registry rows and all 94 staged rows are at column 0 today
(the wide and column-0 patterns both read 51 on the live registry), so this boundary costs nothing on today's
tree, but a 4-space-indented future row would be invisible to the guard.

Because the guard held, the append *decision* is not blocked by instrument failure — it is blocked by the
collision itself (§3) and by unmet flips (§6).

## 3. What a collision means here — adoption is by document, never by number

The colliding ids are not cosmetic: each pair names a different document.

| id | lane row (registered) | staged row (package) |
|---|---|---|
| `S044` | Bugcrowd Vulnerability Rating Taxonomy repository README | 最高人民法院、最高人民检察院…法释〔2011〕19号 |
| `S045` | Bugcrowd VRT CWE mapping dataset | 中华人民共和国刑法（2023 修正）第二百八十五条、第二百八十六条 |
| `S046` | IPA JVN activity report | 南京市人民检察院 检务指南… |
| `S047` | IPA JVN quarterly registration report | JR/T 0276—2023 证券期货业信息系统渗透测试规范 |
| `S050` | 360SRC 外部漏洞处理和评分标准 V2.0 | 脆弱性対策情報データベース JVN iPedia の登録状況 2026年第3四半期 |
| `S051` | Immunefi Vulnerability Severity Classification System v2.2 | 中华人民共和国刑法（最高人民法院公报刊载文本） |
| `S052` | *(free at measurement; C2's CISA KEV row is the incoming occupant)* | 信息安全漏洞周报（2026 年第 40 期，总第 853 期） |

Blast radius of a naive append, measured on the lane's own citations: `^source:[ \t]*(S[0-9]{3,})\b` over
`corpus/knowledge/*.md` (46 entries; 20 entries carry an `S`-id `source:` line; 28 distinct ids cited) →
**27 `source:` citations across 20 lane knowledge entries cite an id in the 21-id collision set** (`S031`–`S051`;
1–4 entries per id; e.g. `S041` is cited by 4: `iso-29147-and-30111-division-of-labour.md`,
`iso-29147-divergence-and-clause-crosswalk.md`, `japanese-domestic-disclosure-workflow.md`,
`japanese-severity-vocabulary-and-impact-model.md`). Appending staged rows at their own ids would silently
repoint all 27 to different documents with no instrument firing, because each id still resolves to *a* row.
That is why the package's own `existing_rows 30 / first_id S031 / renumbered 0` assumption cannot be adopted.

Projection after C2 lands (`S052` = CISA KEV, a third document again distinct from staged `S052` = CNNVD
weekly): collisions `21 → 22` (`S031…S052`) and the repoint surface `27 → 28` citations. Measured at 06:35Z,
`S052` was **not** yet on disk (`grep -cE '^ {0,3}\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` → 0;
`corpus/knowledge/cisa-kev-catalog.md` absent), so the post-landing figure is labelled a projection, not a run.

## 4. Renumber map (scratch-side only, nothing applied)

Rule: keep the append file's row order, map the *first* staged id onto the first free lane id, offset the rest
by the same constant (verified constant across all 94 rows). Two instantiations, because the registry is
moving: pre-C2 (`first free = S052`) and post-C2 (`first free = S053`). Quarantined ids are marked `HOLD` —
they must not be admitted at any id.

- `renumber-map-pre-c2.txt` (`sha256 34e82d34daf936505ab576ace04110d0baf4caa9e57c73b45114f48e676c893d`):
  `S031 -> S052 … S124 -> S145`, 7 HOLD.
- `renumber-map-post-c2.txt` (`sha256 5fb517bcdd74179261f9869d8e2ffc2b28a62fa81fd5a345ec7e320179259275`),
  operative at round close if C2's row lands: `S031 -> S053 … S124 -> S146`, 7 HOLD.

```
S031 -> S053
S032 -> S054
S033 -> S055
S034 -> S056
S035 -> S057
S036 -> S058
S037 -> S059  HOLD(quarantine)
S038 -> S060
S039 -> S061
S040 -> S062
S041 -> S063
S042 -> S064
S043 -> S065
S044 -> S066
S045 -> S067
S046 -> S068
S047 -> S069
S048 -> S070  HOLD(quarantine)
S049 -> S071
S050 -> S072
S051 -> S073
S052 -> S074
S053 -> S075
S054 -> S076  HOLD(quarantine)
S055 -> S077
S056 -> S078
S057 -> S079
S058 -> S080
S059 -> S081
S060 -> S082
S061 -> S083
S062 -> S084
S063 -> S085
S064 -> S086
S065 -> S087  HOLD(quarantine)
S066 -> S088
S067 -> S089
S068 -> S090  HOLD(quarantine)
S069 -> S091  HOLD(quarantine)
S070 -> S092  HOLD(quarantine)
S071 -> S093
S072 -> S094
S073 -> S095
S074 -> S096
S075 -> S097
S076 -> S098
S077 -> S099
S078 -> S100
S079 -> S101
S080 -> S102
S081 -> S103
S082 -> S104
S083 -> S105
S084 -> S106
S085 -> S107
S086 -> S108
S087 -> S109
S088 -> S110
S089 -> S111
S090 -> S112
S091 -> S113
S092 -> S114
S093 -> S115
S094 -> S116
S095 -> S117
S096 -> S118
S097 -> S119
S098 -> S120
S099 -> S121
S100 -> S122
S101 -> S123
S102 -> S124
S103 -> S125
S104 -> S126
S105 -> S127
S106 -> S128
S107 -> S129
S108 -> S130
S109 -> S131
S110 -> S132
S111 -> S133
S112 -> S134
S113 -> S135
S114 -> S136
S115 -> S137
S116 -> S138
S117 -> S139
S118 -> S140
S119 -> S141
S120 -> S142
S121 -> S143
S122 -> S144
S123 -> S145
S124 -> S146
```

Held rows (quarantine, §5), post-C2 numbering: `S037 -> S059`, `S048 -> S070`, `S054 -> S076`, `S065 -> S087`,
`S068 -> S090`, `S069 -> S091`, `S070 -> S092`. The map is advisory: no file in the package or the lane was
rewritten, and `renumber-staged.py` was not run (it writes into shokuknow).

## 5. Quarantine slice — re-derived from the register (read-only)

Register `sha256 5afe1810…f64bad833`, 375 lines, unchanged since round 34; section state machine
(`## Rows` = `payload-absent`, `## Rows whose quotes were NEVER CHECKED` = `unreachable`), lane cell `kasegi`,
id normalised of the register's stray trailing backtick:

```
S037 | round1 | payload-absent
S054 | round3 | payload-absent
S048 | round2 | unreachable
S065 | round4 | unreachable
S068 | round4 | unreachable
S069 | round4 | unreachable
S070 | round4 | unreachable
```

`slice_rows=7 slice_malformed_lines=0`, `sha256 7696d76c4f17d1d9f41598e7c36def077e1f7429d947639726afdebf6e528f31`
— **identical bytes to round-34's re-derivation**, and the same seven ids in the same order as the committed
`.ufo/waves/round-35/assimilation/quarantine-slice`
(`sha256 d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`, which I did not touch; that
committed copy carries the register's raw class text and no round column). Cross-check on the register:
`## By lane` reads `| kasegi | 2 |`, agreeing with the two `payload-absent` rows.

Blast radius inside the lane, re-measured this round: the staged entries citing a quarantined id are
`chinese-vulnerability-taxonomy-and-grading.md` (S037), `chinese-national-grading-model.md` (S048),
`authorization-safe-harbor-and-scope-2026-10-23-amendment.md` (S054),
`chinese-statute-version-drift-2026-10-23-r4-amendment.md` (S065),
`iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` + `vendor-cvd-policy-crosswalk-2026-10-23.md` (S068),
`chinese-grading-standard-draft-2026-10-23.md` (S069, S070) — **seven files, all absent from
`corpus/knowledge/`**, so no admitted lane entry rests on a quarantined register row. Blast radius = 0.

Per-row dispositions are **not re-fetched this round** (limit R8): the register's two classes are re-read as
recorded, and round-34's live verdicts at `2026-10-26T05:31–05:32Z` stand — `S037` refuse (spliced field
collage), `S054` refuse (registered span elides the statutory parenthetical), `S048` unreachable (404), `S065`
reachable-today but no recorded span, `S068` unreachable (403), `S069`/`S070` unreachable in substance (200 with
an empty body, one URL twice). Net: **0 adopted, 2 refused, 5 unreachable** — unchanged.

## 6. Standing refusals — flip predicates re-measured on today's lane bytes

Every predicate below is a lane-side measurement run this seat (no network, no write); "met?" is the measured
value, not an opinion. All flip sets remain partially unmet, so no refused entry becomes assimilable.

| staged entry | decision | measured predicate today | met? |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` (`120d8cd5d50b`) | REFUSED (standing, r30) | `grep -cE 'txt:[0-9]+'` → **0** located quotes; its `ground: F09 (new frontier item …)` calls F09 new while the lane already admits a different F09 at `corpus/README.md:210` | **no** |
| `claim-packaging-and-report-quality.md` (`6ad64d785f8f`) | REFUSED (standing) | `grep -c bilibili corpus/SOURCES.md` → **0**; id `S036` exists in the lane but names 脆弱性情報ハンドリングポリシー (サイボウズ), so BILISRC is neither registered nor free at that id | **no** |
| `cn-crowdsourced-testing-roles-and-conduct.md` (`a5302aaf0b9a`) | REFUSED (standing) | `grep -c '^# '` → **0** (no H1); ids `S081`/`S082` → **0** lane rows | **no** |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (`6c15d9411424`) | REFUSED (standing) | `sacinfo` → 0, `sac.gov.cn` → 0, `57CAF3B4` → 0 rows; ids `S077`/`S078`/`S079` → **0** lane rows; its `ground: F24` → `grep -cE '^\| F24 \|' corpus/README.md` → **0** (frontier is F01–F17) | **no** |
| `chinese-criminal-thresholds-and-authorisation.md` (`1660c00c1636`) | REFUSED (standing, r30) | `court.gov.cn` → 0, `czt.ln` → 0, `nj.jsjc` → 0 rows; staged ids `S044`–`S046` are occupied by Bugcrowd VRT README / Bugcrowd VRT CWE / IPA JVN rows, so registration needs the renumber map first | **no** |
| `chinese-program-severity-instrument.md` (`442e0f2bfb08`) | REFUSED as an entry (r33) | `grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt` → **0** (`newsType_21` → 1); `sse.com.cn` → **0** lane rows | **no** |
| `program-severity-ladders-and-reward-scales.md` (`35de5f8b19ed`) | REFUSED / do-not-copy | same-name lane entry with different bytes: staged `35de5f8b19ed`/50 L vs lane `6c05c98f3c68`/67 L — an overwrite hazard, not a flip | unchanged |

This round's new ground cannot lift any of them: `grep -rliE 'cisa|known exploited|kev'` over the package's 67
knowledge files → **0 files**, so F18/S052 (CISA KEV) has no contact surface in the package. F17/S051
(Immunefi) likewise reaches nothing new (`immunefi` appears in 3 lane `SOURCES.md` lines — the row plus its two
provenance notes — and in no package file). No new refusal is opened and no prior refusal is lifted.

## 7. Verdict

- **Guard:** proven load-bearing on an indented-row fixture before any append decision; `collisions` non-empty
  as expected (21). **Guard not broken.**
- **Append:** none. `corpus/SOURCES.md` unchanged (`4c85ff8608dd` at 06:29Z and 06:35Z, 51 rows); no staged row
  entered the lane at any id.
- **Quarantine:** re-derived to identical bytes (7 rows, `7696d76c…`); 0 adopted, 2 refused, 5 unreachable; lane
  blast radius 0.
- **Flips:** no staged entry's flip set is fully met (§6); the seven standing refusals stand.
- **Assimilation: none adopted this round.** The renumber map is advisory only; the operative variant at close
  is `S031 -> S053 … S124 -> S146` with 7 HOLD rows.


## 8. Addendum — second moment: C2's `S052` row landed mid-seat (`06:40Z`)

The registry moved under this seat after §1–§7 were written (limit R8.3 anticipated it). Recorded, not
rewritten: every figure in §1–§7 stays the **51-row moment** (`06:29–06:35Z`, `corpus/SOURCES.md`
`4c85ff8608dd`) and is labelled as such; this section is the post-landing moment.

- `corpus/SOURCES.md` now `sha256 510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`, **52 rows**
  (`S052` at `:58` = CISA Catalog of Known Exploited Vulnerabilities); `corpus/knowledge/cisa-kev-catalog.md`
  exists and cites `source: S052` (47 knowledge entries). `corpus/README.md` still carries **17** frontier rows
  (`F18` not on disk at this read) — not this seat's claim, only context.
- The assignment's block re-run at `06:40Z`, exits `0 0 0`: **`reg_ids=52 staged_ids=94 collisions=22`**,
  range `S031..S052`, and a second independent run into a fresh scratch dir is byte-identical
  (`diff -q` → `same-reg`, `same-coll`). Artifacts: `assimilation/reg-ids-post-c2`
  `sha256 2d95a2702fa2af54d4ab551b0e63129f606850cc139991a73db5b7b1ec6f3d00`, `assimilation/collisions-post-c2`
  `sha256 11623fc54a36902bde1872ad904fdefa01db99ba5ff37f7a4d8d2769598e7c36`. The staged set is unmoved
  (`staged-ids` `550a0129…` before and after).
- Guard re-run on the post-landing live tree: `kind=wide reg_ids=52 staged_ids=94 collisions=22 ids=S031 … S052`,
  exit 0 — still not broken, still non-empty as expected.
- Repoint surface rose as projected: **28 `source:` citations across 22 colliding ids** (47 entries, 29 distinct
  ids). `S052` is now cited by `cisa-kev-catalog.md` — i.e. the C2 landing is itself the 28th citation the
  collision set would repoint if the package were appended at its own ids (staged `S052` = CNNVD weekly, a
  third document).
- The operative renumber instantiation is therefore **`renumber-map-post-c2.txt`**
  (`S031 -> S053 … S124 -> S146`, 7 HOLD rows, `sha256 5fb517bc…`); `renumber-map-pre-c2.txt` is now historical.
- Correction to the assignment's framing, measured: the standing collision range is **`S031..S051`** at the
  51-row moment and **`S031..S052`** after the landing (not `S031-S047`); the frozen "round-34 rerun: 21"
  reproduces exactly on the pre-landing tree.
- **Peer artifact, same directory, arrived after §5 was written:** `assimilation/quarantine-verdicts.md`
  (seat `ExecQuarantineSlice`, `sha256 b086936919174837f48e04b4209794cc7738716a25abaae3396d43a2dfe5b5a0`, live fetches `06:32–06:44Z`) re-fetched the
  same seven rows with finer labels: `present-and-located` S065/S068/S069/S070, `prose-class-unverifiable`
  S037/S054, `unreachable` S048, `absent` 0, and it adopts nothing. That supersedes my §5 re-statement of
  round-34's coarser classes (`unreachable` for S065/S068/S069/S070) — the slice, its 7 ids, the blast radius
  (0) and the no-adoption conclusion are unchanged, and both files agree that the package is not adopted. I do
  not restate their fetch numbers here; read their file for those.

---

## Report

### R1 — Id-collision run (commands, outputs, exits)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ A=.ufo/waves/round-35/assimilation; S=/home/vgpnk/Projects/shokuknow; mkdir -p "$A"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"                          # exit 0, 51 lines
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"  # exit 0, 94 lines
$ comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"                                                                         # exit 0, 21 lines
reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051
$ uniq -d "$A/reg-ids" | wc -l        # 0
$ uniq -d "$A/staged-ids" | wc -l     # 0
```

Independent staged-set derivation (package `source:` headers) and agreement check:

```
$ grep -ohE '^ {0,3}source:[[:space:]]*S[0-9]{3,}' "$S"/merge/kasegi/knowledge/corpus/knowledge/*.md | grep -ohE 'S[0-9]+' | sort -u > /fast/scratch/…/staged-ids-src
$ wc -l < /fast/scratch/…/staged-ids-src                            # 94
$ comm -3 "$A/staged-ids" /fast/scratch/…/staged-ids-src | wc -l    # 0
```

Shape checks: registry `rows 51 min 1 max 51 gaps [] dupes 0`; append-table row column count 11 = lane-table
column count 11; append ids ascending (`LC_ALL=C sort -c` exit 0), `dupes-in-append=0`.

Reproducibility: the whole block was run a second time into a fresh scratch dir; `diff -q` against the lane
artifacts → `identical reg-ids`, `identical staged-ids`, `identical collisions` (three diffs, exit 0 each).

### R2 — Guard proof (fixtures + controls) and boundary

```
GUARD fixture wide  : kind=wide reg_ids=2 staged_ids=94 collisions=1 ids=S031     exit 0
GUARD fixture col0  : kind=col0 reg_ids=1 staged_ids=94 collisions=0 ids=          exit 0
NEGCTRL wide        : kind=wide reg_ids=1 staged_ids=94 collisions=0 ids=          exit 0
LIVE wide           : kind=wide reg_ids=51 staged_ids=94 collisions=21 ids=S031 … S051  exit 0
LIVE col0           : kind=col0 reg_ids=51 staged_ids=94 collisions=21 ids=S031 … S051  exit 0
missing registry    : reg_ids=0 staged_ids=94 collisions=0                        exit 2
indent=3 wide=1 col0=0 | indent=4 wide=0 col0=0 | indent=tab wide=0
```

The fixture is `scratch-registry.md` `ee8088e5208f…` (same bytes as round 34's fixture); the negative control is
`scratch-registry-noncollide.md` `45a598c903ba…`; the checker is `collide-check.sh` `6d17e641e943…`.

### R3 — Collision semantics and lane blast radius

```
lane vs staged identity: S044/S045/S046/S047/S050/S051/S052 each name different documents (§3 table)
$ python3 (source:-line census over corpus/knowledge/*.md)
lane_knowledge_entries_total= 46
lane_entries_with_S_source= 20
distinct_lane_cited_ids= 28
colliding_ids_cited_by_lane_entries= 21 ['S031' … 'S051']
lane_entries_that_would_be_repointed= 27
```

Projection (not a run): registry + one `S052` row → `proj_reg=52 proj_collisions=22`; post-C2 first free id
`S053`.

### R4 — Renumber map

```
$ python3 (map from staged-ids-ordered; offset = first_free - 31; HOLD for the 7 quarantined ids)
map-pre-c2.txt  : S031->S052 S124->S145 held=7   sha256 34e82d34daf9…
map-post-c2.txt : S031->S053 S124->S146 held=7   sha256 5fb517bcdd74…
offset_const= True
```

### R5 — Quarantine slice

```
$ awk -F'|' '<section state machine: ## Rows -> payload-absent, ## Rows whose quotes were NEVER CHECKED -> unreachable>' "$REGISTER" > slice.txt
S037 | round1 | payload-absent
S054 | round3 | payload-absent
S048 | round2 | unreachable
S065 | round4 | unreachable
S068 | round4 | unreachable
S069 | round4 | unreachable
S070 | round4 | unreachable
rows=7 malformed=0   sha256 7696d76c4f17…   (== round-34 re-derivation)
committed .ufo/waves/round-35/assimilation/quarantine-slice sha256 d02acb68cb40… (untouched)
register sha256 5afe1810a6c3… 375 lines (unchanged)
```

Quarantine blast radius: seven staged entries cite the quarantined ids; all seven are absent from
`corpus/knowledge/`.

### R6 — Flip predicates (exact counts)

```
bilibili 0 | sse.com.cn 0 | sacinfo 0 | sac.gov.cn 0 | 57CAF3B4 0 | court.gov.cn 0 | czt.ln 0 | nj.jsjc 0 | openstd 0
S036 lane_rows=1 (different document) | S044/S045/S046 lane_rows=1 each (different documents)
S077 S078 S079 S081 S082 lane_rows=0 each
frontier rows 17 (F01–F17); F24 rows 0; F09 admitted at corpus/README.md:210
newsType_6 in round-32/S049.txt = 0 ; newsType_21 = 1
package files matching 'cisa|known exploited|kev' = 0
H1 in cn-crowdsourced-testing-roles-and-conduct.md = 0
located quotes ('txt:NN') in each of the seven staged entries = 0
```

### R7 — Artifacts written, and nothing else

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-35/assimilation/reg-ids` | `a262e5f46ca2407263cc9eb15b56686f61c5c011bb65d7d130fbd08af8ed0974` |
| `…/assimilation/staged-ids` | `550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f` |
| `…/assimilation/collisions` | `e7718d617b04972a00d91124bf8c8b38219e08a7980db17104654cb83f299740` |
| `…/assimilation/guard-proof.txt` | `714ccb8795182c31063edef0e579a0ef0fbbc8c700b21eba9f409069bcf88fbe` |
| `…/assimilation/scratch-registry.md` | `ee8088e5208f4c215881858ac05088008847446ccd2c4d393b604edfe4fb842f` |
| `…/assimilation/scratch-registry-noncollide.md` | `45a598c903ba6d9c1ae6981ebd3230a04a8c7f70e314c1a40410dfd725329033` |
| `…/assimilation/collide-check.sh` | `6d17e641e9439c38536f69797e186704248e763346ac31a68ae9bd26f9dbf917` |
| `…/assimilation/quarantine-slice-rederived` | `7696d76c4f17d1d9f41598e7c36def077e1f7429d947639726afdebf6e528f31` |
| `…/assimilation/renumber-map-pre-c2.txt` | `34e82d34daf936505ab576ace04110d0baf4caa9e57c73b45114f48e676c893d` |
| `…/assimilation/renumber-map-post-c2.txt` | `5fb517bcdd74179261f9869d8e2ffc2b28a62fa81fd5a345ec7e320179259275` |

No other path was written: no edit to `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`,
`SCORECARD.md`, `SKILL.md` or any instrument; `.ufo/waves/round-35/assimilation/quarantine-slice` left
byte-identical (`d02acb68…`). Scratch tree `/fast/scratch/hyaku/kasegi-r35/ExecIdCollisions/` was deleted after
the artifacts were copied (`rm -rf`; `ls` of the path → absent). No git/jj mutation; no tooling installed or
upgraded (0 tools, so no version to record); no campaign tool of `shokuknow` invoked.

### R8 — Limits, stated as measured

1. **No live re-fetch of the seven quarantine sources this round.** The register's classes are re-read as
   recorded; the per-row live verdicts quoted in §5 are round-34's, at `2026-10-26T05:31–05:32Z`, and are not
   restated as a fresh observation.
2. **Indent boundary:** the guard covers 0–3 leading spaces by declaration; a 4-space or tab-indented row is
   invisible (measured 0). No live row is indented today (51/51 registry rows and 94/94 staged rows at column
   0), so the boundary costs nothing now.
3. **Moving registry:** C2's `S052` (CISA KEV) was not on disk at 06:35Z (51 rows). If it lands before close,
   `collisions` becomes 22 (`S031…S052`), the repoint surface 28, and the operative renumber map starts at
   `S053` — both maps are stored so the L1 can print the landed figure without re-deriving the map.
4. `SCORECARD.md` moved mid-window (`31ebb1ea` → `51337bf1`) under a sibling seat; no figure in this receipt
   depends on it.

### Gate drop-in (for `corpus/lessons/round-35.md`)

```markdown
### Assimilation: none adopted — id-collision guard proven, quarantine slice unchanged

- Id-collision re-run at `2026-10-26T06:28–06:41Z`: `reg_ids=51 staged_ids=94 collisions=21 S031..S051` at the
  51-row moment, and **`reg_ids=52 staged_ids=94 collisions=22 S031..S052`** after C2's `S052` landed
  (`wave1/ExecIdCollisions.md` §1 + §8; artifacts
  `.ufo/waves/round-35/assimilation/{reg-ids,staged-ids,collisions,reg-ids-post-c2,collisions-post-c2}`,
  `a262e5f4…`/`550a0129…`/`e7718d61…` and `2d95a270…`/`11623fc5…`). The staged id set is byte-identical to
  round 34's (`550a0129…`); registry growth, not package movement, moves the collision set.
- Guard proven load-bearing before any append: an indented `S031` row yields `collisions=1` under the declared
  0–3-space pattern and `0` under a column-0 pattern; negative control `0`; missing registry `exit=2`
  (§2; `assimilation/collide-check.sh` `6d17e641…`). Not broken.
- A naive append would repoint **28 `source:` citations across 22 colliding ids** (27 across 21 at the 51-row
  moment; the C2 entry is itself the 28th);
  adoption is by document, never by number (§3). Renumber map scratch-side only: `S031 -> S053 … S124 -> S146`
  with 7 HOLD rows (`assimilation/renumber-map-post-c2.txt` `5fb517bc…`); nothing applied.
- Quarantine slice re-derived to identical bytes: 7 rows, `slice_rows=7 slice_malformed_lines=0`,
  `sha256 7696d76c…` = round 34's (§5); 0 adopted, 2 refused (S037, S054), 5 unreachable (S048, S065, S068,
  S069, S070); lane blast radius 0 (all seven citing staged entries absent from `corpus/knowledge/`).
- Seven standing refusals re-measured: every flip predicate still unmet (`bilibili` 0, `S077`–`S082` 0 lane
  rows, F24 absent, `newsType_6` 0, `sse.com.cn` 0, do-not-copy digest mismatch `35de5f8b`/50 L vs
  `6c05c98f`/67 L); F18/S052 reaches 0 package files, so the round's new ground lifts nothing.
- **Assimilation: none adopted this round.** No refused entry's flip set is fully met; no new refusal opened,
  no prior refusal lifted.
```
Report: `.ufo/waves/round-35/wave1/ExecIdCollisions.md`
