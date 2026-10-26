# ExecSiblingSweep — sibling-lane EPSS / exploitation-likelihood ground + doctrine host check (read-only), round 36

Lane head read at start: `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze), on top of `cc692008b0cfd58d18275aa6c4aed79620120799`.
Wrote nothing outside this receipt and `/fast/scratch/hyaku/kasegi-r36/ExecSiblingSweep/` (removed before yield). No lane/fleet/shokuknow file edited; no tool installed or upgraded.

## Ruling: RATIFIED (uncontested)

No sibling lane holds any EPSS / exploit-prediction / exploitation-likelihood ground. The absence is **measured**, not merely unchecked: a hidden-inclusive full-tree sweep of all 20 sibling lanes returns **0** files for the word-bounded token `\bEPSS\b`, and every case-insensitive near-match (127 files) resolves to a non-EPSS substring. No sibling `SKILL.md` mentions `vulnerabilit*` at all, so kasegi is the fleet's only vulnerability-domain lane.

Two things this ruling does **not** say:
- It does not supply sibling corroboration for F19/S053; the admission rests on kasegi's own S053 capture and harness PASS.
- It does not license the phrasing "EPSS never appeared in the lane": kasegi's own round-24 CVSS snapshots already carry the FIRST navigation entry for EPSS (caveat A).

Consistency with prior seat: `ScoutF19Sibling.md` (wave1) ruled UNCONTESTED on the sibling axis; this seat agrees and adds the doctrine-host axis, the whole-lane hidden-inclusive sweep, a correction to that seat's shokuknow result, and the lane-internal pre-token. No contradiction found between the two receipts.

## Hit table — EPSS family (lane, file, line, token, verdict)

Pattern (case-insensitive, whole lane trees, `.git` excluded, hidden files included): `EPSS|Exploit Prediction|exploitation likelihood|exploitation-likelihood|probability of exploit`. **127 files**, all non-ground.

### game-dev-2d-shokunin — 97 files, one token class: `epssweep` (a Godot boundary-test sweep identifier)

| file | line | token |
|---|---|---|
| `corpus/fixtures/r98b_attack.gd` | 27, 54, 565, 567 | `epssweep` / `_arm_epssweep` / `r98b_epssweep` |
| `corpus/fixtures/run_battery.py` | 1304, 1390, 1391 | `r98b_epssweep` |
| `corpus/live/r98-boundary/analysis.txt` | 169–174 | `r98b_epssweep` |
| `corpus/live/r98-boundary/{RECEIPTS.md,run_matrix.sh,manifest.sha256,probes/r98b_attack.gd,proj/r98b_attack.gd}` | — | `epssweep` (one file each) |
| `corpus/live/r99-simplifier/patchcheck/corpus/fixtures/{r98b_attack.gd,run_battery.py}` | — | `epssweep` |
| `corpus/live/runs/<20 run dirs>/{scratch,missing-preset-scratch,export-launch/{positive,negative}}/r98b_attack.gd`, `verdicts.json` | — | `epssweep` (69 files) |
| `reports/round-98/{r98-author.md,r98-boundary.md,r98-reviewer.md}` | 92 (r98-author) | `r98b_epssweep` |
| `reports/round-101/{mutations/{analysis2,results,ver9_baseline_r100}.json,r101-simp1.md}` | 99 (r101-simp1) | `r98b_epssweep` |
| `reports/round-103/mutations/*` (8 files) | — | `r98b_epssweep` |
| `reports/round-104/mutations/w8_census_raw.jsonl` | — | `r98b_epssweep` |

Verdict: **no** — `epssweep` is an epsilon/scale readback test arm (`docs.godotengine.org`-domain lane). No vulnerability content.

### Other lanes — 30 files, all substring noise

| lane | file | line | token | verdict |
|---|---|---|---|---|
| tameshi | `corpus/knowledge/r8-flaky-cost-baseline.md` | 12 | `EPSS` inside `conf/icst/LeinenEPSSJ24` | no — DBLP key of an author surname; paper is flaky-test cost |
| tameshi | `.ufo/evidence/round-47/{assimilation/package/r8-flaky-cost-baseline.md,coverage/sources/s2-icst24-cost-of-flaky.json}`, `.ufo/waves/round-47/w1/T47*.md` (7 files) | — | `LeinenEPSSJ24` | no — same key, mirrored into wave artifacts |
| kotodama | `reports/supplement-opencode-1/scratch/source-recheck-orality/gragas_v2.txt` | 19261, 19307 | `epss` | no — OCR/lemma fragment in a phonetics source |
| kotodama | `reports/supplement-opencode-1/scratch/22-label-representation/hj1903_djvu.txt` | 129616 | `EpSs` | no — djvu OCR noise |
| kotodama | `.ufo/waves/round-60/support/transcripts/KotodamaR60A3.Support{B60,U60}.jsonl` + 3 `.scratch/{base,eval-base,smoke}` copies (8 files) | 67 (B60) | `epSS` / `ePSS` | no — randomized identifier inside transcript JSON |
| kotoba | `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt` | 561137, 958554 | `epSs` | no — `strings` dump of a binary |
| kaidoku | `.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch` | 42445, 55099 | `ePSs` / `ePsS` | no — case-mutated patch symbols |
| kake | `.ufo/waves/round-41/verification/r40standing/CtlKeyFinder__ctl_keyfinder_laneonly.json` | 180 | `epss` | no — control-fixture random key |
| kake | `.ufo/waves/round-42/controls/w1/CtlCache/ctl_{accept,reject}_table_seed4242.py` | 3602, 4185 | `epSS` / `epsS` | no — base64 control payload |
| kake | `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-4{1,2}/…` (3 files) | — | same three | no — copies of the above |
| mado | `.ufo/waves/round-25/controls/CtlCacheDelta.py` | 10 | `ePss` | no — fixture key |
| research (fleet root, non-lane) | `round-18-kimi-model-routing/battery/raw/responses/openai-codex-gpt-6.1-sol/k2-r1.json` | 73 | `epsS` | no — model response text |

## Hit table — loose alternatives (`percentile`, `probability … exploit`), 20 files

All are generic statistical vocabulary in unrelated domains. Kept because the item's regex named them.

| lane | file | line | token |
|---|---|---|---|
| audio | `corpus/live/r93-scout/sources/libebur128-1.2.6.c.txt` | 1279, 1298, 1339–1340 | `percentile` (EBU R128 loudness code) |
| kake | `corpus/knowledge/field-performance-cwv.md` | 8, 29, 32, 38 | `percentile` (Web Vitals p75) |
| kake | `corpus/lessons/round-28.md` / `round-28-verifier-spotcheck.md` | 33 / 158 | `percentile` |
| kake | `corpus/README.md` / `corpus/SOURCES.md` / `SKILL.md` | 45 / 44 / 684 | `percentile` |
| kengaku | `corpus/knowledge/eval-prior-art-calibration.md` / `corpus/evidence/round9-fleet/prior-art.md` | 60 / 82 | `percentile` |
| kumitate | `corpus/knowledge/runtime-remainder-census.md` | 429, 443 | `percentile` (routing-health latency rank helper) |
| mori | `corpus/evidence/recheck-r32/S002.src`, `corpus/evidence/sources-r50/cgroup-v2.7.2.html` | 1849, 1855, 1879, 1894 / 1814, 1820, 1844, 1859 | `percentile` (kernel io.latency docs) |
| mori | `corpus/evidence/sources-r42/S262.oa.json` | 1 | `citation_normalized_percentile` (OpenAlex field) |
| kotodama | `reports/supplement-opencode-1/scratch/**` (6 OpenAlex/HTML artifacts) | 1 / 1155 | `percentile` (OpenAlex field) |

`probability of exploit` / `probability … exploit`: **0 files** in any sibling lane.

## Doctrine check — host/channel assignment touching first.org: **none exists**

`/home/vgpnk/Projects/shokuknow/doctrine/` (12 markdown files) was searched read-only:

| pattern | files | detail |
|---|---|---|
| `first.org` | **0** | no host row, no channel row, no anchor example |
| `EPSS` | **0** | — |
| `Exploit Prediction` / `exploitation likelihood` | **0** | — |
| `cve.org`, `nvd.nist.gov` | **0** | — |
| `CVSS` | 1 | `channel-index-chinese.md:669` — inside the `zc.cnvd.org.cn` help-page row ("the CVSS 3.0 temporal metrics"); no host assignment |
| `vulnerability scor*` | **0** | — |
| `\bFIRST\b` | 2 | both the English adverb (`coverage-lever.md:1423` "named sources FIRST", `anchor-craft.md:1799` "the FIRST quote"); **not** the FIRST organisation |
| `cisa.gov` | 1 | `channel-recurrence.md:62` — one-off channel, assigned to `kasegi` |
| `jvndb.jvn.jp` | 3 files / 17 rows in `channel-index-japanese.md` | Japanese advisory channels |

`channel-recurrence.md` was computed from the lanes' own `CHANNELS.md` (round 1–2): 187 distinct hosts, 5 recurring, 14 niche, 168 one-off. Kasegi's assigned one-off hosts number **26** — `cisa.gov`, `cnnvd.org.cn`, `cnvd.org.cn`, `codeofchina.com`, `court.gov.cn`, `czt.ln.gov.cn`, `edatacompliance.com`, `flk.npc.gov.cn`, `gongbao.court.gov.cn`, `hackerone.com`, `ipa.go.jp`, `iso.org`, `jpcert.or.jp`, `jvndb.jvn.jp`, `kanxue.com`, `laws.e-gov.go.jp`, `nj.jsjc.gov.cn`, `npa.go.jp`, `scjg.ln.gov.cn`, `security.360.cn`, `security.bilibili.com`, `seebug.org`, `sohu.com`, `soumu.go.jp`, `sse.com.cn`, `zc.cnvd.org.cn`. **`first.org` is in none of them.**

Consequence for adjacency: doctrine supports F18 (CISA KEV) by a host row and by the cisa.gov one-off assignment; it supports no EPSS/FIRST host. F19's host is therefore **unassigned by doctrine** while being **already exercised in-lane** — kasegi's SOURCES cites `www.first.org` in 3 rows:

- S001 — FIRST CVSS v4.0 User Guide (`https://www.first.org/cvss/v4.0/user-guide`)
- S002 — FIRST CVSS v4.0 Specification Document (`…/cvss/v4.0/specification-document`)
- S018 — FIRST multi-party vulnerability coordination guidelines v1.1 (`…/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1`)

So the doctrine host table is **incomplete for kasegi** (first.org mined since round 22–24, invisible to the 187-host census because that census predates it). This is a doctrine-state observation only — shokuknow is read-only to this seat and no doctrine row was written.

## Caveat A — lane-internal pre-token (matters for the entry scribe)

`corpus/source-snapshots/round-24/S001.txt` and `S002.txt` already contain the FIRST site navigation block:

```
153 Exploit Prediction Scoring System (EPSS)Why EPSS?
155 Using EPSS
156 How EPSS Works
159 Who is using EPSS?
208 Exploit Prediction Scoring System (EPSS)
```

Identical line numbers in both files (site chrome of the CVSS user guide and specification pages). This is navigation text, not EPSS content — but it means:

1. kasegi's novelty claim must be phrased **"first EPSS ground"**, never "EPSS was absent from the lane".
2. The lane has fetched `first.org` since round 24 (S001/S002/S018 are all first.org), so S053's host is not new to the lane; only its EPSS path (`/epss/`) is.

## Caveat B — the only genuine EPSS text in scope lives in the shokuknow campaign, not in any lane corpus

`/home/vgpnk/Projects/shokuknow/lanes/revenger/round12/measurements/iwsec-program-20241113.txt:2196` contains:

> 「最後に、影響がある脆弱性のリスクをどう判断するか、**SSVCやKEV・EPSSなどを利用して**考えます。」

sha256 `7be78c6d81e3740311649f5f297cbf446ecdf9a496d0fc4a29837008ffe95535`, byte-identical to `.ufo/waves/corpus-expansion-1/.qcache/0f25edf4e0bde5d87291edea.txt`. Surrounding text identifies the talk as 企画講演3「脆弱性管理と課題」(神戸/篠原/中岡, フューチャー株式会社 — the Vuls maintainers), session 3F5 OWS企画②, and the same program carries 企画講演2「FIRST等を活用したCSIRT間の国際連携活動」(内田有香子, JPCERT/CC).

Two notes, both data-only:

- The cached document's own title is **コンピュータセキュリティシンポジウム2024（CSS2024）プログラム**, while its filename says `iwsec-program-20241113` — a filename/content mismatch inside the campaign's revenger lane. Recorded, not fixed (shokuknow is read-only).
- This is a **conference programme abstract**, not EPSS ground: it names EPSS as one of three prioritisation inputs (SSVC, KEV, EPSS) and carries no method, no threshold and no data. It corroborates the *adjacency* of the F19 framing (exploitation-likelihood scoring used to triage scanner noise) in the Japanese security literature; it must not be cited as a source and it does not create the host assignment doctrine lacks.

The same cache holds 5 first.org artifacts (CVSS specification, v2 guide, v3.1 spec, `/cvss/`, global SIGs vulnerability-coordination page); the other uppercase match in `.qcache/537a6e98ad454c7ae7727817.pdf` is compressed-stream bytes.

## Caveat C — correction to a prior seat's method (same ground, different conclusion)

`ScoutF19Sibling.md` records "whole `/home/vgpnk/Projects/shokuknow` (excl .git) for `\bEPSS\b|Exploit Prediction Scoring`: **0 hits**". The tree is not empty; the pattern's word boundary is. `\b` is Unicode-aware, and in 「EPSSなど」 the token is followed by a word character (な), so `\bEPSS\b` cannot match. Reproduced:

| probe | result |
|---|---|
| `rg -l 'EPSS'` over shokuknow, default (hidden skipped) | 3 files — all the unrelated DBLP/surname/HTML noise |
| `rg -l --hidden -g '!.git/**' 'EPSS'` | + `.qcache/{0f25…,f49f…}.{raw,txt}` |
| `rg -o '\bEPSS\b' .qcache/0f25…txt` | no output (boundary fails before な) |
| `rg -o 'EPSS' .qcache/0f25…txt` | `EPSS` |

The `-I` binary-skip in that seat's receipt is not the cause either: the matching artifact is UTF-8 text. Practical consequence for the entry scribe: any strict anchor used against Japanese-language sources must drop `\b` (or use `(?<![A-Za-z])EPSS(?![A-Za-z])`), otherwise a real mention followed by CJK script reads as absent.

For the sibling-lane ruling this changes nothing: my sibling-lane `\bEPSS\b` sweep is **0 files** and my boundary-free case-insensitive sweep of the same 20 lanes finds no CJK-adjacent EPSS either — every sibling hit is ASCII substring noise listed above.

## Adjacency map (what actually neighbours F19 in the fleet)

| lane | adjacent ground | contest? |
|---|---|---|
| kasegi (self) | F01 CVSS v4 severity, F18 CISA KEV catalog (S052), FIRST CVSS/multiparty sources S001/S002/S018; r24 nav pre-token | no — F19 extends the ladder (severity → exploitation status → exploitation likelihood) |
| kagi | `.ufo/waves/round-28/retained-probes/SrcCve202010735/nvd-api*.json`: NVD API probe retaining CISA-ADP **SSVC** fields (`"exploitation":"none"`, `"automatable":"no"`), 4 files | no — SSVC decision points, no EPSS, no SOURCES row |
| mori | S012 GHSA systemd-oomd advisory (CVSS score line only); S049/S222 OWASP cheat sheets | no — advisory prose |
| tameshi | none (its `EPSS` is a DBLP surname) | no |
| revenger / tabi / kake / souji / others | none; `git-cvsserver` man page (souji), `cvss-overall-score-id` HTML chrome (mori S012), `CVSs` in bundled Playwright report (tabi) | no |
| shokuknow doctrine | security channels limited to JVN/JVN iPedia and CNVD rows; cisa.gov one-off→kasegi; no first.org | n/a — doctrine gap, see above |

Registry scoping (adjacency guard): `S053` exists as a **different** source row in `kake-shokunin`, `tabi-shokunin` and `tameshi-shokunin` `corpus/SOURCES.md`, so SOURCES ids are lane-local and kasegi's S053 raises no fleet id collision. Frontier ids are lane-local too — `F19` in game-dev-2d (`custom_step` tween pause/process row, `reports/round-84/r84-scout.md:311`) and game-dev-3d (`actors-scene.md:160`) are unrelated per-lane findings.

## Method (exact, re-runnable)

```
# 1. sibling lane set (kasegi excluded)
ls -d /home/vgpnk/Projects/shokunin/*-shokunin     # 21 lanes, 20 swept

# 2. EPSS family, whole lane trees, hidden included, .git excluded
rg -il --hidden --no-ignore --no-messages -g '!.git/**' \
   -e 'EPSS' -e 'Exploit Prediction' -e 'exploitation likelihood' \
   -e 'exploitation-likelihood' -e 'probability of exploit' \
   /home/vgpnk/Projects/shokunin --glob '!kasegi-shokunin/**'
# → 127 files (all classified above); visible-only variant → 101

# 3. word-bounded decisive test
rg -l '\bEPSS\b' /home/vgpnk/Projects/shokunin --hidden --no-ignore --glob '!kasegi-shokunin/**'
# → 0 files   (control: kasegi-shokunin/corpus/source-snapshots/round-24/S001.txt → 5)

# 4. loose alternatives
rg -il -e 'percentile' -e 'probability of exploit|probability.{0,20}exploit' … --glob '!kasegi-shokunin/**'
# → 20 files

# 5. sibling SKILL.md domain probe
rg -il 'vulnerabilit' --glob '*-shokunin/SKILL.md' --glob '!kasegi-shokunin/**'
# → 0 files

# 6. doctrine host/channel check
grep -ril 'first\.org' /home/vgpnk/Projects/shokuknow/doctrine/     # → 0, rc=1
grep -ril -e 'EPSS' -e 'cve\.org' -e 'nvd\.nist\.gov' …            # → 0
grep -rlw 'FIRST' …                                                # → 2 files, adverb only
```

Everything above is read-only git/grep/ripgrep; no mutating git command was run, no fixture repo created.

## Risks / handoff notes

1. **Doctrine host gap (not a lane defect).** `first.org` is absent from the 187-host channel census while kasegi has cited it since S001/S002/S018. If the lane keeps mining `first.org/epss/`, a doctrine channel row is owed — owned by the shokuknow campaign, not by this seat; shokuknow is read-only here.
2. **Phrasing in the F19 entry.** Say "first EPSS ground"; do not say EPSS was absent from the lane (caveat A) and do not cite the CSS2024 programme text (caveat B).
3. **Strict-anchor guidance.** `ScoutF19Sibling.md`'s recommendation to use the strict regex for the junk-twin/negative sweep is right for sibling corpora, but its `\bEPSS\b` form under-reports CJK-adjacent mentions; use `(?<![A-Za-z])EPSS(?![A-Za-z])` when any Japanese source is in scope (caveat C).
4. **Campaign-side filename mismatch** (`iwsec-program-20241113.txt` holds the CSS2024 programme) is recorded only; nothing in the round-36 claims depends on it.
5. Unresolved: none. No tool installed, so no tool record is owed.

Scratch `/fast/scratch/hyaku/kasegi-r36/ExecSiblingSweep/` removed before yield.
