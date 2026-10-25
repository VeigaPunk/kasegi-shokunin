# ScoutCensus — SOURCES append conformance pre-check (round 24)

Read-only scout. No production file, git/jj state, lane tree or shokuknow byte was modified.
All probes wrote only under `/tmp`. No tool installs were performed; pacman untouched.

Paths used throughout:

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
APP=/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
CORPUS=/home/vgpnk/Projects/shokunin/CORPUS.md
```

---

## 1. Findings (severity order)

**F1 — The two target paths in the ticket do not exist as stated.** `CORPUS.md` and
`scripts/sources-census.sh` live at the **fleet root**, not under the lane.
`ls /home/vgpnk/Projects/shokunin/kasegi-shokunin` → `AGENTS.md considerthese corpus LOG.md plans PROVINCE.md README.md SCORECARD.md SHONEN.md` (no `CORPUS.md`, no `scripts/`).
Real locations: `CORPUS=/home/vgpnk/Projects/shokunin/CORPUS.md` (section
`## SOURCES.md — where a shokunin learns`, L64–L171) and
`S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (806 lines). No lane-local
`corpus/sources-census.sh` exists either; the lane's own lessons already cite the fleet-root
path (`corpus/lessons/round-23.md:206`). Confidence: high (two `ls`/`glob` receipts).

**F2 — 43 of the append's 94 rows fail E09 on `recheck`.** Every row from S081 on carries
`90d — re-open … (ran 2026-10-24)` / `30d — …` in the `recheck` cell. `symbolic()`
(`S:582`) requires `^[A-Za-z][A-Za-z0-9 _-]*$`; a cell starting with `9` is neither ISO,
nor `^[0-9]+d$`, nor symbolic → E09. Measured: `grep -c $'\tE09\t' /tmp/probe-validate.txt`
= **43**. The executor prompt already orders prose stripped into a scratch note; this is the
proof that the strip is mandatory and its size.
Evidence: `/tmp/probe-validate.txt` (probe `/tmp/kasegi-census-r24` = lane registry + append rows).

**F3 — 108 E11 occurrences over 67 distinct `used-by` paths; every one is a merge-package
filename the lane does not hold.** `usedby_findings()` (`S:538–568`) tests
`[ -e "$dir/$path" ]`. The lane has 33 files in `corpus/knowledge/`; the package holds 67
(`ls /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge | wc -l` = 67)
and the append cites 67 distinct names, **none** of which exist in the lane
(`grep -c $'\tE11\t' /tmp/probe-validate.txt` = 108). Names differ by suffix, e.g. the append
cites `corpus/knowledge/authorization-safe-harbor-and-scope-2026-10-23-amendment.md` while
the lane holds `corpus/knowledge/authorization-safe-harbor-and-scope.md`.
Consequence: the append cannot land as written unless exactly those entries are admitted, or
the rows are `queued` with `used-by` `—`.

**F4 — S031 collides with a live lane row (E03).** `LANE/corpus/SOURCES.md` already owns S031
= CVE Numbering Authority Operational Rules v4.2.6 (`cve.org/.../CNA_Rules_v4.2.6.pdf`,
opened 2026-10-25), while the append's S031 = HackerOne standard program policy set. Lane max
id is S031, so the append's staged S031–S124 must become **S032–S125** (whole-block +1).
Measured: `E03 … S031 duplicate id`; the frozen command prints `S031`.
The referenced collision ledger `.ufo/waves/round-24/assimilation/renumber-map.tsv`
**does not exist** — the directory holds only `collisions` (`S031`), `reg-ids` (S001–S031),
`staged-ids` (S031–S124), `census-before.txt`. The +1 rule survives only from the executor
prompt body, not from a committed map.

**F5 — S120 is the one malformed row (E01, NF=14).** Its `source` cell contains a literal `|`,
shifting every later column; `opened` reads `mined` and `status` reads prose. Reported as
`E01 S120 fields=12` (`NF-2` = cell count). Contract `CORPUS.md:88` forbids `|` inside any
cell. Because E01 short-circuits (`S:635–638` prints E01 then `next`), the shifted
`kind`/`tier`/`status` junk is not separately reported — fixing NF re-arms E05–E09 on that row.
Side effect: `overdue` on the probe reports exactly one line, `S120 1d recheck=2026-10-24
opened=mined` (the shifted cells), which disappears with the fix.

**F6 — 3 tier-C `mined` rows (W01).** S098, S100, S102 are `tier=C`, `status=mined`, with a
concrete `used-by`. `CORPUS.md:96` says tier C is never sole support for an admitted entry.
Warning only, but each of the three also lands an E11.

**F7 — 5 new cross-scope URL duplicates (W04), plus the 2 already disclosed.** Probe reports
`W04` for S064 (dup of lane S043's `jpcert.or.jp/vh/partnership_guideline2026.pdf`), S076
(dup of append S064), S089 (dup of lane S047's `sse.com.cn` PDF), S090 (dup of append S086's
`kass.sacinfo.org.cn/kfs/token/download/udghvosaqozjdqze`), S105 (dup of append S104's
`iolaw.cssn.cn/...`). Baseline lane W04 = S028, S029. Total 7; exit still 0.

**F8 — Indentation is a false-clean trap.** 3-space indent is fully tolerated (probe
`/tmp/kasegi-indent3`: `rows 125`, `tier.A 109`); **4-space indent makes all 94 rows vanish**
(`/tmp/kasegi-indent4`: `rows 31`, `validate` exit **0**, only the 2 lane W04s). An append
indented 4+ spaces "passes" while contributing nothing — the census is blind, not clean.

**F9 — No same-scope URL duplicates (E04) in the append.** 0 pairs after URL normalisation:
the append's `scope` cells are long prose, so a repeated URL always lands on a *different*
scope and surfaces as W04, never E04. The `supersedes S0NN —` exemption is untested today.

**F10 — `validate` treats the em dash as data.** `used-by` must be exactly `—` to mean "none":
`-`, an empty cell, or a path on a `queued` row are read as paths (E11) or invert W01/W03.
`W03` fires only on `mined` + exactly `—`; `W01` fires on any non-`—` value (`S:665–672`).

**F11 — For L1's round counters.** Frozen claim C2 counter_B is
`grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l`. Under the required +1
renumber, append S039 (statutory authorisation, cited by
`statutory-authorization-in-three-traditions.md`) becomes **S040**, which does not match
`S1[0-9][0-9]`. If that is one of the two F09 entries, counter_B caps at 1 and C2 lands short.
Rows that do end at S100+: append S099→S100 … S124→S125 (e.g. S104→S105
`cn-authorised-vulnerability-mining-regime.md`, S105→S106
`yuanwei-case-privileged-testing-unsettled.md`).

---

## 2. Census check inventory — exact conditions

Source of truth: `S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.
The header comment (`S:2–35`) states the contracts; implementation lines are cited per row.
Row scanning accepts **0–3 leading ASCII spaces**; 4+ is indented code and invisible
(`S:541`, `S:609–616`).

| id | exact condition enforced | code |
|---|---|---|
| E01 | In `## Registry`, a non-header, non-separator table row has `NF != 13` with `-F'\|'` — i.e. not 11 columns between the outer pipes. Prints `fields=NF-2`, then `next`: no other E-code is evaluated for that row. | `S:635–638` |
| E02 | `id` does not match `^S[0-9]{3,}$` (S + 3 or more digits, nothing else after trim). | `S:637,640` |
| E03 | `id` already seen earlier in the same file (reached only when NF==13 and E02 did not fire). | `S:641–642` |
| E04 | Same normalised URL **and** byte-identical `scope`, row not `rejected`, an earlier non-rejected row with that URL+scope exists, and this row's `teaches` does not match `supersedes S[0-9]{3}`. URL = first `https?://[^ \t\|]+`, trailing `#…` and trailing `/` stripped, host lower-cased only. | `S:600–607,636–652` |
| E05 | `kind` ∉ {`spec`,`docs`,`paper`,`code`,`tool`,`dataset`,`talk`,`book`,`community`,`own-work`}. | `S:655–656` |
| E06 | `tier` !~ `^[ABC]$` (exactly one uppercase letter). | `S:657` |
| E07 | `status` ∉ {`queued`,`mined`,`rejected`} — `watch` is **not** a status. | `S:658–659` |
| E08 | `opened` is not a real ISO `YYYY-MM-DD` (validated by round-trip through `mktime`) **or** is later than `--today` (UTC, default `date -u +%F`). | `S:575–580,661–663` |
| E09 | `recheck` is not an ISO date, **not** `^[0-9]+d$`, **and** not symbolic `^[A-Za-z][A-Za-z0-9 _-]*$`. Any trailing prose fails. | `S:582,664–668` |
| E10 | `tier` = `A` **and** `kind` = `community`. | `S:669` |
| E11 | Row `status` = `mined` and any comma-split `used-by` element (trimmed, non-empty, not exactly `—`) fails `[ -e "<lane-dir>/<path>" ]`. One finding per bad element, so a row may emit several. | `S:538–568` |
| E12 | A line matching `^\| *S[0-9]{3,} *\|` appears while **not** inside a heading whose text is exactly `Registry` at `##` level (0–3 spaces). Rows under `## Paths`, `## Search log`, `## Leads`, a `# ` heading, or a differently worded `##` heading all trip it. | `S:609–622` |
| W01 | `tier` = `C` **and** `status` = `mined` **and** `used-by` ≠ exact `—`. | `S:665–666` |
| W02 | `status` = `rejected` **and** `length(teaches) < 8`. | `S:667–668` |
| W03 | `status` = `mined` **and** `used-by` == exact `—`. | `S:669–670` |
| W04 | URL seen earlier in the same registry under a **different** scope (cross-scope duplicate; suppressed when the scope string repeats). | `S:643–645` |

Exit status (`S:29–33`,`S:747–756`): **0** clean or W-only · **1** any E, any due row under
`overdue`, or a missing registry under `census` · **2** usage/environment error or missing
registry under `validate`/`overdue`/`shared` · **3** selftest failure. W codes never change exit.

Two behaviours the checklist must respect:

- A *header/separator* row is skipped when `trim($2)=="id"` or every cell from 2..NF-1 is
  `^:?-+:?$` (`S:591–598`) — so the append's own `| id | … |` line and `|---…|` line are inert
  wherever they sit inside `Registry`.
- `usedby_findings()` splits `used-by` on **commas only**, while the frozen manual census
  (`CORPUS.md:147`) splits on `[,;]`. A semicolon-separated `used-by` passes `validate` but
  fails the frozen command. Never use `;` in `used-by`.

---

## 3. Column schema (11 columns ⇒ `NF=13` with `-F'|'`)

| # | column | awk field | constraint enforced by the census | contract |
|---|---|---|---|---|
| 1 | (empty) | `$1` | row starts with `|` at 0–3 leading spaces | `CORPUS.md:88` |
| 2 | `id` | `$2` | `^S[0-9]{3,}$`, unique in file, next unused, never reused (E02/E03) | L88 |
| 3 | `source` | `$3` | no `|` in cell; first `https?://…` is the dedup key (E04/W04); `own-work` may be a repo path | L89 |
| 4 | `kind` | `$4` | 10-value enum (E05); `community` never A (E10) | L90–91 |
| 5 | `tier` | `$5` | `A|B|C` (E06); C is never sole support of an admitted entry (W01) | L92–96 |
| 6 | `scope` | `$6` | free prose; participates verbatim in the E04/W04 key | L97 |
| 7 | `anchor` | `$7` | no machine check; contract forbids a bare homepage | L98–99 |
| 8 | `teaches` | `$8` | `rejected` rows need ≥8 chars and the `REJECTED: …; flip: …` form (W02); `supersedes S0NN —` is the only E04 exemption | L100–103 |
| 9 | `status` | `$9` | `queued|mined|rejected` (E07); `mined` ⇒ ≥1 real path (W03 inverse) | L104–106 |
| 10 | `opened` | `$10` | ISO date, not future (E08) | L107 |
| 11 | `recheck` | `$11` | ISO date **or** `NNd` **or** symbolic cadence, nothing else (E09) | L107–108 |
| 12 | `used-by` | `$12` | comma-separated repo-relative paths that exist on disk, or exactly `—` (E11/W01/W03) | L109–110 |
| 13 | (empty) | `$13` | closing pipe; its absence is what produces NF≠13 | — |

---

## 4. Measured diff — `APP` against that schema

Block shape: 2 HTML comments, 1 header row, 1 separator row, **94 data rows**, ids
**S031–S124**, all at column zero. `wc -lc` = 100 lines / 89 718 B.

| check | predicted | measured on `/tmp/kasegi-census-r24` (lane registry + append rows) |
|---|---|---|
| rows | 31 + 94 = 125 | `rows 125` ✔ |
| E01 | 1 (S120, NF=14) | `E01 S120 fields=12` |
| E02 | 0 | 0 |
| E03 | 1 (S031 vs lane S031) | `E03 S031 duplicate id` |
| E04 | 0 | 0 |
| E05 | 0 (docs 58, spec 21, own-work 13, dataset 1, paper 1) | 0 |
| E06 | 0 (A 80, B 11, C 3) | 0 |
| E07 | 0 for well-formed rows | 0 (S120 masked by E01) |
| E08 | 0 (opened 2026-10-23 ×50, 2026-10-24 ×43; today 2026-10-25) | 0 |
| E09 | 43 | **43** |
| E10 | 0 (no `community` kind) | 0 |
| E11 | 108 occurrences / 67 distinct files | **108** |
| E12 | 0 if inserted in `## Registry` | 0 |
| W01 | 3 (S098, S100, S102) | **3** |
| W02 | 0 (no `rejected` rows) | 0 |
| W03 | 0 | 0 |
| W04 | 7 total (2 lane + 5 new) | **7** |
| validate exit | 1 | **1** |
| overdue exit | 1 (S120 artifact only) | 1 (`S120 1d`) |

Frozen v1 commands (`CORPUS.md:134–147`) on the same probe: `rows 125` · `malformed 1` ·
`tier A=109 B=11 C=5` · `duplicate ids → S031` · `enum violations → (none)` ·
`missing used-by (distinct) → 66` (the malformed S120 row is excluded by the `NF==13` guard,
hence 66 not 67).

Reproduction (writes confined to `/tmp`):

```bash
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
APP=/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
p=/tmp/kasegi-census-r24; rm -rf "$p"; mkdir -p "$p/corpus"
ln -s "$LANE/corpus/knowledge" "$p/corpus/knowledge"; ln -s "$LANE/corpus/lessons" "$p/corpus/lessons"
awk -v app="$APP" '/^## Paths/ && !d {while ((getline l < app) > 0) if (l ~ /^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/) print l; close(app); d=1} {print}' \
  "$LANE/corpus/SOURCES.md" > "$p/corpus/SOURCES.md"
"$S" validate --today 2026-10-25 "$p"; echo "EXIT=$?"
```

Baseline for contrast: `"$S" validate --today 2026-10-25 "$LANE"` → two W04 (S028, S029) +
`kasegi-shokunin ok` → **exit 0**.

---

## 5. Checklist the append block MUST satisfy

`C` = the executor's clone root (`/tmp/kasegi-r24-SOURCESRows`). Run everything against the
clone, never the lane. Every check below is machine-checkable; the pass column says what
"green" looks like.

**1. Rows sit under a heading whose text is exactly `Registry` at `##` level (0–3 spaces).**
Header/separator rows are inert; everything else outside that section is E12.

```bash
"$S" validate --today 2026-10-25 --file "$C/corpus/SOURCES.md" | grep -c $'\tE12\t'   # 0
```

**2. No 4-space indentation anywhere in the block** (4+ is invisible — F8).

```bash
grep -cE '^ {4,}\|[[:space:]]*S[0-9]{3,}' "$C/corpus/SOURCES.md"                       # 0
```

**3. Every row is exactly 11 columns (NF=13), i.e. no literal `|` inside a cell** (F5).

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF!=13 {print NR": "$0}' "$C/corpus/SOURCES.md"    # empty
```

**4. `id` matches `^S[0-9]{3,}$`.**

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/{i=$2; gsub(/ /,"",i); if (i !~ /^S[0-9]{3,}$/) print NR": "i}' \
  "$C/corpus/SOURCES.md"                                                               # empty
```

**5. No duplicate id in the merged file.** The staged S031 collides with the lane's own S031
(F4), so the adopted block must be shifted +1 — staged S031–S124 → S032–S125.

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/{i=$2; gsub(/ /,"",i); print i}' "$C/corpus/SOURCES.md" \
  | sort | uniq -d                                                                     # empty (today: S031)
```

**6. The id space is gapless and its size equals 31 + the adopted row count**, i.e. the block
really starts at S032 and nothing was dropped or double-numbered. Run after #5 — a duplicate
masks a gap otherwise (`uniq` on the probe reports 124 ids for 125 rows).

```bash
ids=$(grep -oE '^[[:space:]]{0,3}\|[[:space:]]*S[0-9]{3,}' "$C/corpus/SOURCES.md" \
      | grep -oE 'S[0-9]{3,}' | sed 's/^S0*//' | sort -n | uniq)
diff <(printf '%s\n' "$ids") <(seq 1 "$(printf '%s\n' "$ids" | tail -1)")               # empty
printf '%s\n' "$ids" | tail -1                                                          # 31 + adopted
```

**7. `kind` ∈ the 10-value enum.**

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF==13{k=$4; gsub(/ /,"",k);
  if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print $2,k}' \
  "$C/corpus/SOURCES.md"                                                               # empty
```

**8. `tier` ∈ {A,B,C}; `community` never A (E06/E10).**

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF==13{t=$5; k=$4; gsub(/ /,"",t); gsub(/ /,"",k);
  if (t !~ /^[ABC]$/) print "tier",$2,t; if (t=="A" && k=="community") print "inflation",$2}' \
  "$C/corpus/SOURCES.md"                                                               # empty
```

**9. `status` ∈ {queued,mined,rejected} — never `watch` (E07).**

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF==13{s=$9; gsub(/ /,"",s);
  if (s !~ /^(queued|mined|rejected)$/) print $2,s}' "$C/corpus/SOURCES.md"            # empty
```

**10. `opened` is ISO and not in the future (E08).**

```bash
"$S" validate --today 2026-10-25 --file "$C/corpus/SOURCES.md" | grep -c $'\tE08\t'    # 0
```

**11. `recheck` is only an ISO date, `NNd`, or a symbolic cadence — no prose, no `(ran …)`,
no compound cell (F2).**

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF==13{r=$11; gsub(/^ +| +$/,"",r);
  if (r !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/ && r !~ /^[0-9]+d$/ && r !~ /^[A-Za-z][A-Za-z0-9 _-]*$/)
    print $2"\t"r}' "$C/corpus/SOURCES.md"                                             # empty
```

**12. No same-URL+same-scope pair without a `supersedes S0NN —` in `teaches` (E04).**

```bash
"$S" validate --today 2026-10-25 --file "$C/corpus/SOURCES.md" | grep -c $'\tE04\t'    # 0
```

**13. Every `used-by` element is a clone-relative path that exists, or the cell is exactly
`—` (F3).**

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF==13{s=$9; gsub(/ /,"",s); if (s=="mined"){
    n=split($12,a,/,/); for(j=1;j<=n;j++){q=a[j]; gsub(/^ +| +$/,"",q); if(q!="" && q!="—") print q}}}' \
  "$C/corpus/SOURCES.md" | while read -r q; do [ -e "$C/$q" ] || echo "missing: $q"; done  # empty
```

**14. No semicolon in `used-by`** (frozen census splits on `[,;]`, the script does not).

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/{if ($12 ~ /;/) print $2}' "$C/corpus/SOURCES.md"      # empty
```

**15. Status/path coherence: `mined` ⇒ concrete path; `—` only on `queued`/`rejected`
(no W01/W03 inversion — F6/F10).**

```bash
"$S" validate --today 2026-10-25 --file "$C/corpus/SOURCES.md" | grep -cE $'\t(W01|W03)\t'  # 0 (today 3 W01)
```

**16. `anchor` is never a bare homepage** (manual contract rule; no machine check in the tool).

```bash
awk -F'|' '/^\| *S[0-9]{3,} *\|/ && NF==13{a=$7; gsub(/^ +| +$/,"",a);
  if (a ~ /^https?:\/\/[^ ]+$/) print $2}' "$C/corpus/SOURCES.md"                      # empty
```

**17. Round lesson records, per new row, the URL, access date and a ≤25-word grounded quote**
(`CORPUS.md:111–114`; the file does not exist yet, so this is blocked on ScribeLesson).

```bash
grep -cE '^S0(3[2-9]|[4-9][0-9])|^S1[0-2][0-9]' "$C/corpus/lessons/round-24.md" 2>&1    # one line per adopted id
```

**18. Append-only discipline: no existing lane row is rewritten** to absorb a package row;
only `status`, `recheck`, `used-by` may change in place, each logged old→new
(`CORPUS.md:115–118`).

```bash
diff <(grep -E '^\|[[:space:]]*S0[0-3][0-9][[:space:]]*\|' "$LANE/corpus/SOURCES.md") \
     <(grep -E '^\|[[:space:]]*S0[0-3][0-9][[:space:]]*\|' "$C/corpus/SOURCES.md")     # empty
```

**19. No credential/session/`op://` material** (`CORPUS.md:130`).

```bash
grep -c 'op://' "$C/corpus/SOURCES.md"                                                 # 0
```

**20. Whole-registry gate: exit 0, W04 lines exactly the disclosed set.**

```bash
"$S" validate --today 2026-10-25 --file "$C/corpus/SOURCES.md"; echo "EXIT=$?"
```

Pass: `EXIT=0`; W04 lines = 2 lane (S028, S029) + the 5 new (S064, S076, S089, S090, S105),
each named in the round lesson. Any E line is a hard fail.

**21. Row delta is exactly the adopted count; nothing vanished silently.**

```bash
"$S" census --today 2026-10-25 --file "$C/corpus/SOURCES.md" | head -1                  # rows = 31 + adopted
```

**22. No new overdue row from the append.**

```bash
"$S" overdue --today 2026-10-25 --file "$C/corpus/SOURCES.md" | grep -c overdue        # 0
```

Order of repair: **#3/#4 (S120) → #5/#6 (renumber) → #11 (recheck strip) → #13 (used-by)**,
because E01 suppresses every other check on its own row and E03 masks the id-space question
for everything downstream.

---

## 6. Interaction with the frozen claims (L1 decision input)

- **C2 counter_B** (`^source: S1[0-9][0-9]`) is satisfied only by rows that end at ≥ S100
  after the +1 shift: append S099→S100 … S124→S125. The statutory entry's cited row
  (append S039→**S040**) does not match, so if that is one of the two F09 entries the
  counter lands at 1 and C2 must be declared short or re-based on a row in S100–S125 (F11).
  Show it with:
  `for f in corpus/knowledge/*.md; do grep -H -m1 '^source: ' "$f"; done | grep -E 'S1[0-9][0-9]'`.
- **C2 counter_A** is `corpus/README.md` only; row count is explicitly not an expansion
  metric (`CORPUS.md:119–126`, rule 4). A 94-row append with no admitted entries moves C2 by
  zero while adding 108 E11s — which is why #13 and #15 gate adoption.
- **The executor's stated verification** (`validate --file <clone>/corpus/SOURCES.md`)
  resolves `used-by` against `dirname(file)/..` = the clone root, which is the correct base
  and matches the lane convention. It does **not** read `corpus/README.md`, so C2 counter_A
  is outside the executor's gate and must be shown separately by L1.

---

## 7. Unknowns / blocked

- **UNVERIFIED:** whether the adopted subset is all 94 rows or only the rows backing the F09
  entries. The executor prompt says "rows for the adopted entries' cited staged ids", so the
  E09/E11 totals above are the whole-block worst case; every per-row condition in §5 holds
  either way.
- **UNVERIFIED:** whether `corpus/lessons/round-24.md` will carry the `## Gate` block required
  by checklist #17 — the file does not exist (`ls corpus/lessons/round-24.md` → no such file;
  newest lesson by version sort is `round-23-verifier-spotcheck.md`). Blocked on ScribeLesson.
- **UNVERIFIED:** the intended `used-by` values for adopted rows: the `renumber-map.tsv`
  referenced by both the claims and the executor prompt is absent from disk. The three files
  present (`collisions`, `reg-ids`, `staged-ids`) fix the +1 shift but say nothing about paths.
- No `lsp` server serves Markdown or bash in this workspace, so every structural claim above
  rests on the shell/gawk/grep receipts quoted inline (recorded here per the fallback rule);
  nothing was asserted from prose alone.
