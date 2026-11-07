# ConnectorOverlap — round 85 / w1 (connector, leaf, read-only)

Axes named: **depth:verifiability** (C1, the `resolve.py` SKILL.md meter) and **coverage** (C2, the
end-to-end priced claim package). All receipts beside this file under
`ConnectorOverlap-receipts/assimilation/`. Lane read-only; no lane file edited by this seat.

---

## 1. Cross-lane scan: does any sibling already hold C2's ground?

Read-only corpus sweep of every `/-shokunin` sibling except kasegi (`.ufo/`, `node_modules/`,
`evidence/`, `lessons/` and `fixtures/` excluded so only product surface counts):

```
grep -rn --binary-files=text -E 'hackerone\.com/reports/[0-9]+|curl\.se/dev/vuln-disclosure|curl\.se/docs/CVE-|CVE-2023-28319|1913733' \
  --include='*.md' --include='*.txt' --include='*.json' --include='*.py' --exclude-dir=.ufo --exclude-dir=node_modules \
  --exclude-dir=evidence --exclude-dir=lessons --exclude-dir=fixtures <siblings>  → 0 matches
```

A wider pass with the same id-bearing terms and no `evidence/`/`lessons/`/`fixtures/` exclusion — i.e. over
every markdown/text file of the 20 siblings except `.ufo/`, `node_modules/`, `.git/` — also prints **0**
lines for `hackerone.com/reports/<n>|curl.se/dev/vuln-disclosure|CVE-2023-28319|1913733`.

**Result: no sibling lane holds H1-record pricing ground, and none holds curl advisory or curl
disclosure-policy ground.** Nearest holdings (found by a broader vocabulary pass over `curl.se`,
`bounty`, `security.txt`, `severity ladder`), all of a different kind:

| lane | file:line | what it actually holds | C2 ground? |
|---|---|---|---|
| kake | `kake-shokunin/corpus/knowledge/security-txt-publishing.md:99` | GitHub's `security.txt` `Contact: https://hackerone.com/github` — an org **policy pointer**, round-35 S084 | No (no report, no amount) |
| kake | `kake-shokunin/PROVINCE.md:208-218`, `LOG.md:1460` | RFC 9116 publishing frontier step | No |
| kagi | `kagi-shokunin/corpus/SOURCES.md:35` (S029), `:43` (S037) | curl(1) man page and `curl.se/info` release identity — the lane's own release clock | No (tool semantics, not advisory/VDP) |
| mori | `mori-shokunin/corpus/SOURCES.md:181` (S175) | curl(1) man page for `-f/--fail` recheck fetch | No |
| kama | `kama-shokunin/corpus/lessons/round-90.md:18` | curl `lib/http.c`/`curl.h` named as **not-appended** SC01 proposals | No (source code, declined) |
| kotodama | `kotodama-shokunin/corpus/knowledge/synthesis/finding-disposition-workflow.md:28` | "severity ladder" of gate findings | No (gate severity, not bounty) |
| chousa | `chousa-shokunin/corpus/knowledge/scope-refusal-r12.md:21` | `claim package(s)` → kasegi refusal vocabulary | No (scope boundary only) |

Second-order read: C2's four priced sources (`S119` H1 JSON, `S120` curl advisory, `S121` curl VDP,
`S052` KEV capture) are **singular to kasegi**. There is no sibling corpus from which this package can
be quoted, so E2/E4 (evidence bytes, located quotes) can only be satisfied from
`corpus/source-snapshots/round-85/` and `corpus/source-snapshots/round-35/` — and conversely, no
sibling's assimilation can supply or legitimate them. That makes §3 the only live id-space risk.

---

## 2. considerthese: what is still unimplemented after this round

Numbering = the seven proposals of `considerthese/2026-10-26.md` (the ledger's own convention,
`corpus/knowledge/considerthese-proposals-ledger.md:150-152`). The six proposals of
`2026-10-25.md` carry dispositions in the base table (`:11-16`) and round-31 flip block (`:22-33`);
nothing there is open.

| # (2026-10-26) | status after round 85 | evidence |
|---|---|---|
| 1 distance-to-next-score | **landed** (r31 measurement, r39 criteria) | `SCORECARD.md:1534`; `corpus/instruments/score-gap.py` |
| 2 end-to-end domain task | **end-to-end build + pricing half lands this round; remainder open** | the frozen C2 claim builds the six-file package (`curl-h1-1913733`: `report.md`, `claim_checklist.md`, `provenance.json`, `custodian-receipts.json`, `status.json`, `evidence/`; candidate at `.ufo/waves/round-85/w1/ExecC2Package-candidate/`, `corpus/practice/` not yet on disk) priced from S119/S120/S121 with KEV absence from S052; but the package is retrospective (`claimable:false`, no submission, no authorization, no reviewer-distinctness), so SHONEN box 2's "domain task" stays `[~]` and the authorized/submitted path is untouched |
| 3 quiescence gate | **landed** | `r35-defect-closure.sh` D1 + `r36-closure.sh` E9(b) + `r46-landing-gate.py` (`--selftest` 30 cases) |
| 4 cap/externalise wave evidence | **open (operator-owned)** — not moved by this round | measured now, `git ls-tree -r -l HEAD`: 16093 tracked files, 15400 under `.ufo/` (**95.7 %**); 204 577 363 bytes total, 191 182 610 under `.ufo/` (**93.5 %**); `grep -c gitattributes` = 0 |
| 5 F18 PROVINCE amendment | **landed r36** | `PROVINCE.md:77`; `grep -c F18 PROVINCE.md` = 6 |
| 6 re-tune cadence | **open (operator-owned)** — not moved | `considerthese/` = 8 files, one per day 2026-10-19…2026-10-26, none since |
| 7 proposal-status ledger | **landed (r30), but its per-round upkeep is 23 rounds behind** | last section is `## Round-62 dispositions` (`:168`, 2026-11-04); `grep -c '^## Round-(6[3-9]\|7[0-9]\|8[0-5]) dispositions'` = 0 |

Older carry-overs resolved by evidence, not open:
- 10-19 #1 anchorcheck regression test — declined as superseded by `anchorcheck.py` fail-closed in r28
  (`considerthese/2026-10-26.md:35`); `git ls-files | grep -c test_anchorcheck` = 0 and no lesson claims it.
- 10-19 #5 / 10-23 #5 / 10-24 #5 "decide draft PR #1 and the 8 README branches" — the 8 `cursor/*`
  refs are gone: `git branch -a --format='%(refname:short)'` = 8 refs, `grep -c 'cursor/'` = **0**.
  PR #1 state is not locally observable (no network beyond the named GETs) and is not claimed here.
- 10-19 #6 craft-vs-meta ratio, 10-21 #5 blocked-round ledger — no tracked artefact
  (`ls corpus/knowledge | grep -iE 'craft|blocked|meta-ratio'` = empty); they survive only as prose in
  the 10-19/10-21 files and are outside the ledger's numbering. Not claimed open or landed by this seat.

**Actionable residue after this round: proposal 2's authorized/submitted remainder, proposals 4 and 6
(operator), and proposal 7's `## Round-63…85 dispositions` backlog.** Proposal 7's upkeep is the only
one that is both unimplemented and lane-owned, and this round is the natural place to file
`## Round-85 dispositions` plus the round-85 `## considerthese` record.

---

## 3. Assimilation id-collision check (shokuknow staging vs lane registry)

Commands, exactly as scoped (`S=/home/vgpnk/Projects/shokuknow`,
`A=…/w1/ConnectorOverlap-receipts/assimilation`):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | tr -d ' |' > $A/lane-ids.txt
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/merge/kasegi/SOURCES.append.md | tr -d ' |' > $A/append-ids.txt
comm -12 <(sort -u $A/lane-ids.txt) <(sort -u $A/append-ids.txt)
```

**Id-list sizes: lane 121, append 94. Collision count: 91.** (`$A/lane-ids.txt`, `$A/append-ids.txt`,
`$A/collisions.txt`, per-row comparison in `$A/id-conflicts.tsv`.)

### 3.1 The collisions are content conflicts, not duplicates

Parsing the second (source) column of both registries (`$A/id-conflicts.tsv`):

- intersection **91** = **1 identical** (`S042`, IPA 脆弱性関連情報の届出受付業務における取扱いプロセス) + **90 conflicting**;
- append-only **3** = `S122`, `S123`, `S124` — the only rows that would land without collision;
- lane-only **30** = the lane's own pre-staging `S001–S030` block.

The staging package's own record says why it thinks 91 is safe:
`$S/merge/kasegi/MERGE-REPORT.json` → `existing_rows: 30`, `first_id: "S031"`,
`renumbered: []`, `refused: []`, `accepted: 94`. That measurement is **stale at the lane tip**: the
staged block claims `S031…S124` wholesale, but the lane independently consumed `S031…S121` for a
different body of work. Its header still says "staged rows for lane kasegi / Review before appending"
(`SOURCES.append.md:2-3`).

### 3.2 The four ids this round actually depends on

| id | lane `corpus/SOURCES.md` | `SOURCES.append.md` | `manifest.json` id → URL |
|---|---|---|---|
| S052 | CISA KEV catalog JSON feed — `mined`, used-by `cisa-kev-catalog.md` | 信息安全漏洞周报 2026 年第 40 期 (CNNVD) | `corpus/source-snapshots/round-35/S052.txt`, 1 479 694 B |
| S119 | HackerOne report 1913733 JSON — `queued` | GB/T 网络安全漏洞分类分级指南 编制说明 | `hackerone.com/reports/1913733.json`, `S119.txt` sha256 `9e4fb52e7e757248…`, 5001 B, 4 quotes |
| S120 | curl advisory CVE-2023-28319 — `queued` | 全国标准信息公共服务平台 标准详情 GB/T 30279-2020 | `curl.se/docs/CVE-2023-28319.html`, `S120.txt` sha256 `65d6b230ad58e865…`, 3053 B, 5 quotes |
| S121 | curl Vulnerability Disclosure Policy — `queued` | 全国标准信息公共服务平台 attachment probe | `curl.se/dev/vuln-disclosure.html`, `S121.txt` sha256 `9e346a4e579769aa…`, 19 670 B, 3 quotes |

A freeze-time apply of the append as-is would therefore leave **two `S119`, two `S120`, two `S121`
and two `S052` rows**, 90 of 91 pairs with conflicting sources. The round's C2 counter is pinned to
these ids (`grep -oE 'S1[0-9]{2}|S0[0-9]{2}' .ufo/waves/round-85/c2/e2e-check.py` → `S119`×11,
`S120`×9, `S121`×6, `S052`×3) and to `corpus/source-snapshots/round-85/manifest.json`, whose `sources[]`
maps `S119 → https://hackerone.com/reports/1913733.json` + sha256 + quotes[].

### 3.3 Why no frozen limb catches this (the non-obvious gap)

`e2e-check.py` E2 reads `corpus/source-snapshots/round-85/S119.txt`, `S120.txt`, `S121.txt` by path and
binds them to the manifest's sha256 (`e2e-check.py:33`, `:67-68`); `E3` re-derives severity / reward /
bounty-flag / KEV / CVE from those bytes. It never opens `corpus/SOURCES.md`. Greps for
`queued|mined|used-by|SOURCES.md` over `e2e-check.py` → **0 hits**; `claim-package-contract.md` likewise
names no SOURCES status rule. So a registry re-point of `S119` is invisible to every frozen limb: the
counter stays green while `SOURCES.md` tells a reader, and any future claim package built from that
registry, that `S119` is a Chinese standards document. The id space is shared by three substrates —
snapshot filenames, `manifest.json`, `SOURCES.md` — and only two of them are pinned.

### 3.4 Guard proof on a scratch registry (indented colliding row)

```
# receipt copy of the scratch registry (scratch itself is deleted before this seat yields)
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $A/guard-registry.md | tr -d ' |'   # → S001, S052
comm -12 <(sort -u $A/lane-ids.txt) <(sort -u $A/guard-ids.txt)                # → S001, S052
```

Guard collision count = **2** (`$A/guard-ids.txt`, `$A/guard-collisions.txt`, `$A/guard-registry.md`).
The 2-space-indented colliding row `S052` **is** extracted and **is** flagged; the 4-space row and the
tab row are not — which is correct, because 4 spaces or a tab opens a Markdown indented code block, not
a table row. Coverage on the real inputs is complete: `grep -cE '^ {4,}\|[[:space:]]*S[0-9]{3,}'` and
the tab form both print **0** for `SOURCES.md` and for `SOURCES.append.md`. The anchored extraction is
therefore sound, and the 91/90 result is not an artefact of indentation.

---

## Routed defect (re-runnable, one)

**D85-CONN-1 — shokuknow's staged `SOURCES.append.md` id plan is stale and would collide with the
round's own evidence ids; `MERGE-REPORT.json` asserts the opposite.**

Re-run:

```
python3 - <<'EOF'
import re
pat=re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|(.*)$')
rows=lambda p:{m.group(1):m.group(2).split(' | ')[0].strip()
               for m in map(pat.match, map(str.rstrip, open(p,encoding='utf-8'))) if m}
lane=rows('corpus/SOURCES.md'); app=rows('/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md')
i=set(lane)&set(app)
print(len(lane),len(app),len(i),sum(lane[k]==app[k] for k in i))
EOF
```

Expected now: `121 94 91 1`. Owner: the L1 / assimilation step (not this seat — a finding is a routed
defect, not an edit). Required fix at apply time: renumber the staged block from **lane max + 1
(`S122…`, already the case for the three append-only rows)** and re-run the check above; do **not** trust
`MERGE-REPORT.json.first_id`, which was measured against `existing_rows: 30`.

## Proposed move (one, bounded)

Treat the registry id space as a *pinned substrate* for C2 rather than prose: keep the round's apply step
away from `SOURCES.append.md` entirely, and — since S119/S120/S121 are `queued` with `used-by: —` — let
this round's integration flip only those three rows to `mined` with `used-by:
corpus/practice/curl-h1-1913733/…`, leaving every other row byte-identical. This improves
**depth:verifiability** (the meter's citations and C2's citations stop sharing an id space with an
unapplied, conflicting staging file) and **coverage** (the package's priced fields stay bound to the
snapshots the manifest names), and harms neither: no frozen limb reads `SOURCES.md`, so the registered
status flip cannot turn a frozen counter red, and no sibling lane is touched.

## Risks

- The flip is an L1 lane edit and is out of this seat's scope; if the L1 chooses instead to admit
  `S122–S124`, the `S119/S120/S121` rows must still be the ones flipped, or E5's "LOG/SHONEN name the
  package path" will point at a registry row whose source is a standards document.
- `MERGE-REPORT.json` will keep asserting `renumbered: []`; any future automation that trusts it
  re-opens D85-CONN-1. A guard belongs on the apply side, not in the package.
- Proposal 4's byte share (93.5 % under `.ufo/`) is unchanged by this round and stays operator-owned; the
  connector records it and takes no decision.

## Verification (for the L1, after integration)

```
A=.ufo/waves/round-85/w1/ConnectorOverlap-receipts/assimilation
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | tr -d ' |' | sort -u | wc -l      # expect 121
grep -nE '^\| S1(19|20|21) ' corpus/SOURCES.md | cut -c1-40                                       # rows unchanged except status/used-by
python3 -B .ufo/waves/round-85/c2/e2e-check.py   # frozen C2 limbs must be unaffected by a SOURCES-only flip
python3 -B .ufo/waves/round-85/c1/skill-meter.py # C1 167/732 unaffected (SOURCES.md is not in the SKILL scope)
```

Receipts: `ConnectorOverlap-receipts/assimilation/{lane-ids.txt,append-ids.txt,collisions.txt,id-conflicts.tsv,guard-registry.md,guard-ids.txt,guard-collisions.txt}`.
