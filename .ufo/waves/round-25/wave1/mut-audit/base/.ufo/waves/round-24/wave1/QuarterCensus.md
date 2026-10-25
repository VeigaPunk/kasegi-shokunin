# QuarterCensus — round-24 SOURCES contract census ("before" Gate)

Seat: `L1Kasegi24.QuarterCensus` (read-only census; no lane file modified, all probes in `/tmp`).
Run date: 2026-10-25. Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Subject bytes: `corpus/SOURCES.md`, sha256 `e64f095b7a86e8c4443e1020ab21def2b424d41193c3975e2363c06b0ebf0ab5`.

State pinned before any measurement:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse master
c2480b143120364728b40397926ffcf30a7309c8
$ git log --oneline -2
c2480b1 round-23 verifier spot-check (integrator, hyaku): non-author admit/reject
d0a3f6a round-23: final amended ControlsRerun seat report
$ git diff --quiet d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a -- corpus/SOURCES.md && echo identical
SOURCES.md identical to frozen base d0a3f6a
```

So the census below is the frozen-claim base (`d0a3f6a`, contract base) plus one report-only commit; the registry bytes are byte-identical to the base blob (`sha256sum corpus/SOURCES.md` and `git show d0a3f6a:corpus/SOURCES.md | sha256sum` both `e64f095b7a86e8c4443e1020ab21def2b424d41193c3975e2363c06b0ebf0ab5`).

---

## 1. Findings

**Q-1 (clean before-state, all seven counters).** Row count 31, malformed 0, duplicate ids none, enum/tier-inflation none, mined-`used-by` missing paths none; tier `A=29 C=2`, status `mined=19 queued=9 rejected=3`. Every one of the seven frozen commands exits 0. Receipts §2.1.

**Q-2 (maintained validator: exit 0, two W04 warnings, both by design).** `validate` prints exactly two findings, both `W04 duplicate url ... across scopes`:
- `S028` shares the HackerOne safe-harbor URL with `S006`; S028 is the *rejected* duplicate-row proposal (`corpus/SOURCES.md`, S028 `teaches` begins `REJECTED: S006 already names the correct enablement heading …`) and its `scope` is deliberately different (*"Whether a new source row is needed to repair the r22 Gate's quote location"* vs S006's *"HackerOne's own safe-harbor statements and the relation to its program scope"*). W04, not E04, is the correct code because E04 requires the same scope.
- `S029` shares the EUR-Lex CRA URL with `S024`; S029 `teaches` begins `supersedes S024 —`, and E04 was correctly suppressed for a superseding row.
Neither is a defect and neither changes exit status. Receipt §2.2.

**Q-3 (falsifier: every counter and every W-code is live).** A planted-defect copy in `/tmp` (no lane write) makes each instrument fire exactly once with the expected text: NF=12 row → CMD2 `1`; reused `S001` → CMD5 `S001`; `kind=blog`/`tier=D` → CMD6 `tier S033 D` + `kind S033 blog`; `community` at tier A → `tier-inflation S034`; dangling `used-by` → `missing: corpus/knowledge/does-not-exist.md`; tier-C mined with `used-by` → `W01`; `rejected` with 5-char `teaches` → `W02`; mined with `used-by = —` → `W03`; duplicate URL across scopes → `W04`. So the empty/short outputs above are measured absence, not a dead command. Receipts §2.4, §2.5.

**Q-4 (exit codes are not a usable gate on the frozen block).** CMD5/CMD6/CMD7 are `awk … | sort | uniq -d`, `awk`, and `awk … | while read`; each exits 0 whether it finds nothing *or* finds violations (proved in §2.4: CMD5/6/7 exit 0 while printing `S001`, `tier S033 D`, `missing: …`). CMD2/CMD3/CMD4 are `awk` and likewise exit 0 on a non-zero malformed count (`1` in §2.4). Only CMD1 (`grep -c`) flips: exit 1 when the count is 0. A round-end Gate must therefore read **output text**, and use `scripts/sources-census.sh` exit 1 for E-class findings — the frozen block alone cannot fail.

**Q-5 (frozen-vs-maintained row-count divergence, measured, not theoretical).** On identical bytes a row indented by two spaces is invisible to all seven frozen commands (`^|` anchor) but parsed by the maintained CLI (`CORPUS.md` §"Maintained parser note", 0–3 leading spaces accepted). Probe: same file, frozen CMD1 → `36`, maintained `census` → `rows 37`; the delta is exactly the planted `S036` two-space row. **On the real lane there are zero indented row lines** (`grep -nE '^[[:space:]]+\|' corpus/SOURCES.md` exits 1, no output in §2.3), so today the two instruments agree numerically (31 = 31). Risk is prospective only: a future row that is indented will silently undercount in the frozen block while `validate` still sees it.

**Q-6 (the assigned path and the cited collision map do not exist).** The item cites `…/kasegi-shokunin/CORPUS.md`; that path is absent (`read` → "Path … not found"; `find /home/vgpnk/Projects/shokunin -maxdepth 3 -name CORPUS.md` returns only `/home/vgpnk/Projects/shokunin/CORPUS.md`, the fleet-root contract). Likewise `claims.json` `assimilation.collision_map` = `.ufo/waves/round-24/assimilation/renumber-map.tsv` is absent; that directory actually holds `census-before.txt`, `collisions`, `reg-ids`, `staged-ids`. A reader following either pointer gets ENOENT. Evidence §2.6.

**Q-7 (my before-receipt reproduces the wave's stored one byte-for-byte).** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/assimilation/census-before.txt` and my fresh `validate` capture have the same sha256 `920e6fd4b2e82aee969bf489a9a2a4cd97188cf84ec001b4df1c944ea5901499` (diff empty). The before state is therefore corroborated by two independent runs, not one seat's paste. Evidence §2.6.

**Q-8 (C2 counter B is blind to the ids the package actually carries — instrument risk, L1 decision).** `claims.json` C2 `counter.command_B` is `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l`, i.e. only `S100`–`S199` match. The two admitted candidates carry `source: S123 …` (`authorised-testing-rules-of-engagement.md`) and `source: S039 / S040 / S041 …` (`statutory-authorization-in-three-traditions.md`), package sha256 `bf40409e…` / `f37a7d9e…`. Simulated post-merge in `/tmp`:

| ids as committed in the entry | counter B |
|---|---|
| package ids kept (`S123`; `S039,S040,S041`) | **1** |
| contract "next unused" (`S032`–`S035`) | **0** |
| both entries carry an `S1xx` row (`S123`; `S100,S101,S102`) | **2** |

So `after_target_B = 2` is reachable **only** if both admitted entries' `source:` lines cite a row numbered `S100`–`S199`. Meanwhile the registry is contiguous `S001`–`S031` (no gaps, no duplicates, §2.3), so the contract's `id — S + 3 or more digits, the next unused` names `S032` as the next id; registering `S100+` satisfies the counter but skips `S032`–`S099`, and registering `S032+` satisfies the rule but can never move the counter. That is a claim-vs-instrument conflict for L1 to resolve explicitly (renumber into `S1xx` with the skip logged, or amend counter B), not something a census seat may decide. Evidence §2.7.

The wave's own append plan lands on exactly the failing branch: `wave1/SOURCESRows.md:100-103` registers the four adopted rows at **S040–S042** (statute) and **S124** (NIST 800-115), i.e. only the ROE entry carries an `S1xx` row, so the counter lands at **1**. `wave1/ScoutCensus.md:253-257` reaches the same arithmetic independently ("the counter lands at 1 and C2 must be declared short or re-based on a row in S100–S125"). My S039–S041 variant in §2.7 is byte-equivalent to the planned S040–S042 for this regex (non-`S1xx` either way), so the table's first row is the receipt for the planned state.

**Q-9 (expected round-end W04 growth is not a regression).** If the admitted package rows re-register the EUR-Lex CRA or NIST 800-115/NIST-family URLs under new `scope` text (package `SOURCES.append.md` registers each article under its own scope), `W04` will fire once per such row. `validate` stays exit 0 for W-codes (`CORPUS.md` maintained-parser note and script header: "W-codes … never change status"). L1 should read the round-end warning count against this baseline (2), not against 0.

**Q-10 (registry shape observed for C2/F09).** 31 rows, ids `S001 … S031` contiguous; `corpus/README.md` admits exactly `F01 … F08` (counter A = 8); 33 knowledge files exist but only 8 are cited by a `mined` row and each of those 8 carries both an `S###` token and an external URL on its `source:` line. C2 counter B is currently 0 (`grep -lE '^source: S1[0-9][0-9] ' … | wc -l`). Evidence §2.3, §2.8.

**Q-11 (what the round-end census should read, mechanically derived — do not assume).** The planned append is 4 rows (`wave1/SOURCESRows.md:100-103`: S040, S041, S042 e-Gov/MIC/NPA, S124 NIST SP 800-115; S041 is tier B per that table). Against this baseline (31 rows, A=29 B=0 C=2) the post-landing census should read `rows 35`, `tier.A 32`, `tier.B 1`, `tier.C 2`, `status` deltas `mined +3/+4` depending on which of the four are `mined`; `wave1/SOURCESRows.md:156` reports `rows 35`, `tier.A 32`, `tier.B 1`, `tier.C 2` from its private clone. All four URLs (e-Gov, MIC, NPA, nvlpubs NIST) are new to the registry, so no **new** W04 is expected from them and the round-end `validate` should still show exactly the two S028/S029 W04 lines of §2.2 — if it shows more, a URL was re-registered and that must be reconciled. This is a derived expectation, UNVERIFIED until L1 runs the block at round end; the point of recording it now is that a *different* number is a finding, not a rounding.
---

## 2. Verbatim receipts

All commands run with cwd = `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless stated. Commands are the seven frozen examples from `/home/vgpnk/Projects/shokunin/CORPUS.md` §"Census — run from the lane root", unmodified.

### 2.1 The seven frozen census commands

```
# CMD 1 — rows (spacing-tolerant)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
31
EXIT=0

# CMD 2 — malformed rows (NF != 13); must print 0
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
EXIT=0

# CMD 3 — tier histogram
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=29 C=2 
EXIT=0

# CMD 4 — status histogram
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=19 queued=9 rejected=3 
EXIT=0

# CMD 5 — duplicate ids; must print nothing
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
EXIT=0

# CMD 6 — enum violations and tier inflation; must print nothing
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(no output)
EXIT=0

# CMD 7 — mined rows whose used-by paths do not exist; must print nothing
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
EXIT=0
```

### 2.2 Maintained validator, pasted whole

```
$ cd /home/vgpnk/Projects/shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

(stderr empty; whole stdout above, 3 lines.)

### 2.3 Shape and identity checks

```
$ awk -F'|' '… print i …' corpus/SOURCES.md     # ids in file order
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031
EXIT=0

$ grep -nE '^[[:space:]]+\|' corpus/SOURCES.md
(no output)
EXIT=1            # zero indented rows: frozen and maintained parsers agree numerically today

$ grep -nE '^\|[[:space:]]*S[0-9]{4,}[[:space:]]*\|' corpus/SOURCES.md
(no output)
EXIT=1            # no 4-digit ids

$ awk … mined used-by … corpus/SOURCES.md | sort -u | nl
     1	corpus/knowledge/ai-assisted-finding-validation.md
     2	corpus/knowledge/authorization-safe-harbor-and-scope.md
     3	corpus/knowledge/cna-assignment-and-vulnerability-rules.md
     4	corpus/knowledge/coordinated-disclosure-timelines.md
     5	corpus/knowledge/cra-manufacturer-reporting-duties.md
     6	corpus/knowledge/cvss-v4-severity-and-vector.md
     7	corpus/knowledge/cwe-top25-2025-methodology.md
     8	corpus/knowledge/multiparty-vulnerability-coordination.md

$ ls corpus/knowledge/*.md | wc -l
33
```

Cross-check of the same bytes through `census` mode (counts agree with §2.1 exactly):

```
$ cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh census --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
file	rows	31
file	tier.A	29
file	tier.C	2
file	status.mined	19
file	status.queued	9
file	status.rejected	3
FLEET	rows	31
FLEET	tier.A	29
FLEET	tier.B	0
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	19
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
EXIT=0
```

Supplementary freshness channel (`overdue`), whole output — 31 cadence lines, **0 overdue rows**:

```
$ scripts/sources-census.sh overdue --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
file	cadence	S001 recheck=on-release opened=2026-10-19
file	cadence	S002 recheck=on-release opened=2026-10-19
file	cadence	S003 recheck=180d opened=2026-10-19
file	cadence	S004 recheck=180d opened=2026-10-19
file	cadence	S005 recheck=180d opened=2026-10-19
file	cadence	S006 recheck=90d opened=2026-10-19
file	cadence	S007 recheck=90d opened=2026-10-19
file	cadence	S008 recheck=180d opened=2026-10-19
file	cadence	S009 recheck=90d opened=2026-10-19
file	cadence	S010 recheck=on-release opened=2026-10-19
file	cadence	S011 recheck=90d opened=2026-10-19
file	cadence	S012 recheck=90d opened=2026-10-19
file	cadence	S013 recheck=on-release opened=2026-10-19
file	cadence	S014 recheck=on-release opened=2026-10-19
file	cadence	S015 recheck=on-release opened=2026-10-19
file	cadence	S016 recheck=90d opened=2026-10-19
file	cadence	S017 recheck=90d opened=2026-10-19
file	cadence	S018 recheck=180d opened=2026-10-19
file	cadence	S019 recheck=on-release opened=2026-10-19
file	cadence	S020 recheck=on-release opened=2026-10-19
file	cadence	S021 recheck=on-release opened=2026-10-19
file	cadence	S022 recheck=on-release opened=2026-10-19
file	cadence	S023 recheck=90d opened=2026-10-19
file	cadence	S024 recheck=on-release opened=2026-10-19
file	cadence	S025 recheck=on-release opened=2026-10-19
file	cadence	S026 recheck=90d opened=2026-10-19
file	cadence	S027 recheck=180d opened=2026-10-19
file	cadence	S028 recheck=90d opened=2026-10-20
file	cadence	S029 recheck=on-release opened=2026-10-20
file	cadence	S030 recheck=on-release opened=2026-10-20
file	cadence	S031 recheck=on-release opened=2026-10-25
EXIT=0
```

### 2.4 Falsifier probe A — `/tmp/casegi-r24-census-probe2` (lane copy + 6 planted rows inside `## Registry`)

Host: `/tmp/casegi-r24-census-probe2/corpus/SOURCES.md` = lane file + planted `S032` (10 cells), `S001` (dup), `S033` (`kind=blog`,`tier=D`), `S034` (`community`@A), `S035` (dangling used-by), `S036` (two-space indent); `corpus/knowledge/` copied so only planted defects can fire.

```
$ cd /tmp/casegi-r24-census-probe2
#### CMD1  36        EXIT=0
#### CMD2  1         EXIT=0
#### CMD3  A=33 C=2 D=1       EXIT=0
#### CMD4  mined=23 queued=10 rejected=3       EXIT=0
#### CMD5  S001      EXIT=0
#### CMD6  tier S033 D
          kind S033 blog
          tier-inflation S034      EXIT=0
#### CMD7  missing: corpus/knowledge/does-not-exist.md      EXIT=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/casegi-r24-census-probe2 --file /tmp/casegi-r24-census-probe2/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E01	S032 fields=10
file	E03	S001 duplicate id
file	E05	S033 kind=blog
file	E06	S033 tier=D
file	W03	S033 mined but unused
file	E10	S034 community-at-A
file	W03	S034 mined but unused
file	E11	S035 missing used-by corpus/knowledge/does-not-exist.md
EXIT=1

$ scripts/sources-census.sh census --file /tmp/casegi-r24-census-probe2/corpus/SOURCES.md
file	rows	37
file	tier.A	34
file	tier.C	2
file	tier.invalid	1
file	status.mined	23
file	status.queued	11
file	status.rejected	3
EXIT=0
```

Frozen CMD1 = 36 vs maintained rows = 37 on the same bytes: the two-space `S036` is the only difference (Q-5).

### 2.5 Falsifier probe B — `/tmp/casegi-r24-census-probe3` (adds `S037` tier-C mined, `S038` thin reject)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/casegi-r24-census-probe3 --file /tmp/casegi-r24-census-probe3/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W01	S037 tierC mined used-by=corpus/knowledge/cvss-v4-severity-and-vector.md
file	W02	S038 thin reject reason
file	E01	S032 fields=10
file	E03	S001 duplicate id
file	E05	S033 kind=blog
file	E06	S033 tier=D
file	W03	S033 mined but unused
file	E10	S034 community-at-A
file	W03	S034 mined but unused
file	E11	S035 missing used-by corpus/knowledge/does-not-exist.md
EXIT=1
```

W01–W04 are all proven emittable; the real lane's single W-code (W04×2) is therefore a measured result.

### 2.6 Path and corroboration checks (Q-6, Q-7)

```
$ read /home/vgpnk/Projects/shokunin/kasegi-shokunin/CORPUS.md
Path '/home/vgpnk/Projects/shokunin/kasegi-shokunin/CORPUS.md' not found

$ find /home/vgpnk/Projects/shokunin -maxdepth 3 -name 'CORPUS.md'
/home/vgpnk/Projects/shokunin/CORPUS.md

$ ls -la .ufo/waves/round-24/assimilation/
census-before.txt  collisions  reg-ids  staged-ids      # no renumber-map.tsv

$ cat .ufo/waves/round-24/assimilation/collisions
S031
$ head -3 .ufo/waves/round-24/assimilation/staged-ids
S031
S032
S033
$ wc -l < .ufo/waves/round-24/assimilation/staged-ids
94

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi > /tmp/qc-validate-now.txt 2>&1; echo "EXIT=$?"
EXIT=0
$ diff -u .ufo/waves/round-24/assimilation/census-before.txt /tmp/qc-validate-now.txt && echo IDENTICAL
IDENTICAL to census-before.txt
$ sha256sum .ufo/waves/round-24/assimilation/census-before.txt /tmp/qc-validate-now.txt
920e6fd4b2e82aee969bf489a9a2a4cd97188cf84ec001b4df1c944ea5901499  .ufo/waves/round-24/assimilation/census-before.txt
920e6fd4b2e82aee969bf489a9a2a4cd97188cf84ec001b4df1c944ea5901499  /tmp/qc-validate-now.txt
```

### 2.7 C2 counter-B sensitivity (Q-8) — `/tmp` only, package bytes read-only

```
$ sha256sum /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md \
            /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/statutory-authorization-in-three-traditions.md
bf40409ec27b10a7110e61c84a358ec48d439019af8c5841dc5d749664049ca3  …/authorised-testing-rules-of-engagement.md
f37a7d9edf51ec9b10e06d6deee520c0fe9d6d3b1b1b49cff6e8d6e4821142c5  …/statutory-authorization-in-three-traditions.md

$ grep -n '^source:' …/authorised-testing-rules-of-engagement.md
2:source: S123 — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf — `# Appendix B (Rules of Engagement Template); the glossary entry for Rules of Engagement (ROE)` — NIST Special Publication 800-115, …
$ grep -n '^source:' …/statutory-authorization-in-three-traditions.md
4:source: S039 — https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 — 第二条 (定義) 第四項, 第十一条 (罰則)
5:source: S040 — https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/ — （定義）第二条 第四項, 第十一条
6:source: S041 — https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf — §3 不正アクセス行為の禁止、処罰, (1)

# /tmp/casegi-r24-c2probe  (package ids kept)
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l
1
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md
corpus/knowledge/authorised-testing-rules-of-engagement.md

# same probe, statutory rows renumbered S100-S102
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l
2

# /tmp/casegi-r24-c2probe2  (contract "next unused" ids S032-S035)
$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l
0
```

### 2.8 Coverage counters (supplementary before-state; not this seat's verdict)

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
8
EXIT=0
$ awk … '{print $2}' corpus/README.md
F01 F02 F03 F04 F05 F06 F07 F08

$ grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l
0
$ grep -lE '^source: .*https?://' corpus/knowledge/*.md | wc -l
8
$ grep -lE '^source:.*S[0-9]{3}' corpus/knowledge/*.md | wc -l
8
```

## 3. Scope, non-actions, and UNVERIFIED

- No lane file, git/jj state, fleet file or `/home/vgpnk/Projects/shokuknow` file was written. Lane `git status --porcelain` at the start of this seat showed only `?? .ufo/waves/round-24/` (the integrator's own untracked wave dir); `corpus/SOURCES.md` had no modification.
- At the end of this seat the lane working tree had gained `M corpus/instruments/resolve.py` and untracked `corpus/instruments/{capture-source.py,resolve-dispatch-check.py,resolve-dispatch-fixtures.json}` plus `corpus/source-snapshots/round-24/` from sibling seats; none of those are mine. `corpus/SOURCES.md` was re-checked after those edits and still hashes `e64f095b7a86e8c4443e1020ab21def2b424d41193c3975e2363c06b0ebf0ab5` with `git status --porcelain corpus/SOURCES.md` empty, so every receipt above measures the bytes it names.
- I ran no build, lint, test or formatter; the only executable invoked besides the census CLI and shell text tools is `python3` for the `/tmp` fixture copy.
- No tool install or upgrade; pacman untouched (host pause respected). Nothing to record under the tooling directive.
- UNVERIFIED: whether `validate`'s recovery of `W04`-vs-`E04` for a *future* superseding row will behave as it did for `S029`, if the new row's scope string equals its predecessor's — that depends on the scope text L1 writes, not on current bytes. UNVERIFIED: `overdue` judgement for `on-release` rows is by design never "overdue" (script header), so the 31 cadence lines say nothing about staleness of `on-release` sources.
- The seven-command block cannot fail on E-class content by itself (Q-4); the round-end Gate should paste both this block and the `validate` block, and read `validate`'s exit code as the gating signal.
