# Scout — kasegi-province triage of the merge corpus (67 entries)

**Seat** L1Kasegi24.ScoutMergeOther · read-only · round 24, wave 1  
**Source read** `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/` (67 `*.md`, 3 243 lines total), plus `MERGE-REPORT.json`/`.md` and `SOURCES.append.md` in the package root.  
**Lane base compared against** `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at `d0a3f6a4` — `corpus/SOURCES.md` (31 rows), `corpus/README.md` (F01–F08), `corpus/knowledge/` (33 files, 8 of them frontier entries).  
**Province definition used** the lane's own description, `SKILL.md:2` — *"scopes ~/Projects/bounties, program rules, claim packages"* — plus the ticket's axis split (grading standards / court procedure / statute versions are adjacent).  
**Adopted nothing. Wrote nothing outside this file.** No build, lint, test or formatter run.

---

## 1. Findings

**F1 — Province split is 18 in / 9 borderline / 40 adjacent.** 18 entries carry programme rules, scopes, triage or claim-packaging ground; 9 are authorisation doctrine whose primary is a court or standards document; 40 are national grading standards (20), statute text/version (4) and source-access probes (16). `MERGE-REPORT.md:6` states the package has 67 entries; every one is classified below and no file is left unplaced. Two entries are already this round's candidates (`claims.json` `assimilation.candidates_admit`): `authorised-testing-rules-of-engagement.md` (S123) and `statutory-authorization-in-three-traditions.md` (S039); one is the round's refusal (`chinese-criminal-thresholds-and-authorisation.md`, S044).

**F2 — Only 6 of 67 entries have a `recheck:` that names the exact public URL of every row in their own `source:` block.** The other 61 cannot satisfy C1's exit-0 predicate as filed. Buckets, computed from the front matter of all 67 files: exact-URL-for-every-source **6**; recheck names a same-host but different URL and leaves a row un-re-opened **3**; a cited source row's host never appears in the recheck at all **20**; `recheck:` is prose with neither URL nor shell command **20**; `recheck:` has a shell command but no URL (lane-local artifact or re-minted token only) **5**; every source row is a lane-local capture with no public URL **13**. Worked examples: `chinese-criminal-case-law-2026-10-23.md:4-9` cites S051 and S063 on `gongbao.court.gov.cn` but its recheck (`:9`) curls only `www.court.gov.cn/fabu/xiangqing/283891.html` (S061); `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` cites S068 `www.cisco.com` and never re-opens it; `claim-packaging-and-report-quality.md` cites S034/S035/S036 and its recheck only re-fetches the S036 PDF.

**F3 — The package's first staged id collides with a row the lane registered today.** `MERGE-REPORT.md:7-9` fixes `first id S031` against "lane registry currently holds 30 rows" and `MERGE-REPORT.json` reports `accepted: 94`, `collides_with_existing: []`, `duplicate_target: false` for all 67. The lane now holds 31 rows: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md:37` = **S031, CVE Numbering Authority Operational Rules v4.2.6, mined 2026-10-25**. The package's S031 is `hackerone.com/security/policy_versions`. The package's own census already records it — `.ufo/waves/round-24/assimilation/collisions` contains the single line `S031` — but the manifest field that an integrator would read is stale-false. Only one id collides; S032–S124 (93 rows) are free.

**F4 — 13 of 40 adjacent entries cite nothing but the lane's own probe logs.** `source:` is a path under `lanes/kasegi/roundNN/evidence/*.txt` or `round16/evidence/*.txt` (S109, S110, S112, S113, S114, S115, S116, S117, S118, S120, S121, S122, S072). Importing them imports route knowledge the lane already earned, not a new reopenable primary; they should be weighed as narrative, never as verifiability gain.

**F5 — 11 source rows are cited by more than one package entry, and S034 by four.** S034 (zc.cnvd.org.cn help page) grounds `chinese-program-severity-instrument`, `claim-packaging-and-report-quality`, `program-scope-rules-and-asset-boundaries` and `program-severity-ladders-and-reward-scales`; S057/S043 by three each. The renumber map must therefore be many-to-many (one row ↔ N entries), not one row per entry, or four entries will each mint a separate id for one URL.

**F6 — Five strongest in-province candidates for a future round** (§3), the strongest unused ground being **claim packaging** (the lane's `corpus/knowledge/claim-package-contract.md` is a lost-tree document with no openable equivalent) and **Chinese crowdsourcing conduct** (the lane holds Western safe-harbour text and no Chinese programme-side prohibited-method list).

**F7 — Do not re-propose S123, S039 or S044 in a later round.** They are this round's two admissions and one refusal (`claims.json`); re-proposing them would double-count the coverage counter that C2 is measuring.

---

## 2. Triage table (all 67)

Bucket key: **IN** = programme rules / scope / triage / claim package / disclosure handling. **BORD** = in-province subject, adjacent primary (court, standards body, academic). **ADJ** = adjacent only, with sub-kind in the note.

| entry | bucket | source ids | primary host(s) | note |
|---|---|---|---|---|
| `authorised-testing-rules-of-engagement.md` | IN | S123 | nvlpubs.nist.gov | ROE as the instrument that confers authority, with NIST's own template |
| `authorization-safe-harbor-and-scope-2026-10-23-amendment.md` | IN | S053, S058, S054, S057 | pepabo.com, www.ipa.go.jp, www.meti.go.jp | Japanese statutory track behind a vendor-level safe harbour |
| `authorization-safe-harbor-and-scope-2026-10-23-r4-amendment.md` | IN | S066, S067 | www.microsoft.com | a safe harbour that names the statutes it stands on (CFAA, DMCA, WA code) |
| `chinese-program-severity-instrument.md` | IN | S034, S047 | www.sse.com.cn, zc.cnvd.org.cn | CVSS 3.0 base plus the temporal metrics a programme actually publishes, with coefficients |
| `claim-packaging-and-report-quality.md` | IN | S034, S035, S036 | security.360.cn, security.bilibili.com, zc.cnvd.org.cn | claim-proof, scored report fields and the enumerated downgrade list — the openable form of the lane's lost `claim-package-contract` |
| `cn-crowdsourced-testing-roles-and-conduct.md` | IN | S081, S082 | std.samr.gov.cn, zc.cnvd.org.cn | China's crowdsourced-testing conduct code: four-role authorisation, prohibited methods, no direct vendor contact |
| `iso-29147-and-30111-division-of-labour-2026-10-23.md` | IN | S076 | www.jpcert.or.jp | which of 29147/30111 does what, without buying either standard |
| `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` | IN | S064, S068 | www.cisco.com, www.jpcert.or.jp | the one-sentence obligation difference between ISO/IEC 29147:2014 and the Japanese P-guideline |
| `japanese-disclosure-legal-framework.md` | IN | S043, S039 | laws.e-gov.go.jp, www.jpcert.or.jp | the statutory base the Japanese flow runs on |
| `japanese-domestic-disclosure-workflow.md` | IN | S042, S043 | www.ipa.go.jp, www.jpcert.or.jp | the national nine-step flow and 起算日 as the clock anchor |
| `japanese-severity-vocabulary-and-impact-model.md` | IN | S049, S050, S043 | www.ipa.go.jp, www.jpcert.or.jp | 緊急/重要/警告/注意 and the handling-priority model behind them |
| `japanese-vendor-disclosure-policies-2026-10-23.md` | IN | S055, S056, S057, S060 | cybozu.co.jp, pepabo.com, www.hitachi.co.jp | intake-broader-than-programme, disclosure scope narrower than handling scope |
| `program-quirks-2026-10-23-amendment.md` | IN | S055, S056, S057 | cybozu.co.jp, pepabo.com | three Japanese vendor programmes: invitation-only intake, product-list scope, deferred payment |
| `program-scope-rules-and-asset-boundaries.md` | IN | S031, S034, S035 | hackerone.com, security.360.cn, zc.cnvd.org.cn | scope list and safe harbour are different instruments; third-party assets are not the platform's to authorise |
| `program-severity-ladders-and-reward-scales.md` | IN | S032, S033, S034, S036 | raw.githubusercontent.com, security.bilibili.com, zc.cnvd.org.cn | four incompatible severity ladders and a worked example where max CVSS pays 4 or 12 points |
| `statutory-authorization-in-three-traditions.md` | IN | S039, S040, S041 | laws.e-gov.go.jp, www.npa.go.jp, www.soumu.go.jp | what "authorised" means in three statutes, against a platform promise |
| `vendor-cvd-policy-crosswalk-2026-10-23.md` | IN | S068 | www.cisco.com | vendor policy as a process commitment with an LDoS boundary and named coordinators |
| `vendor-third-party-finding-coordination-2026-10-23.md` | IN | S080 | www.microsoft.com | vendor research programme as an intake route for other vendors' findings |
| `authorised-account-scope-and-intrusion.md` | BORD | S098 | www.055110.com | account/Token used beyond its authorised scope is the intrusion — doctrine in province, primary is a commercial republication |
| `authorised-tester-case-law.md` | BORD | S094, S095 | web.archive.org, www.bjjc.gov.cn | guiding-case analysis of the "intrusion program" element |
| `chinese-criminal-case-law-2026-10-23.md` | BORD | S051, S061, S062, S063 | gongbao.court.gov.cn, www.court.gov.cn | what courts decide about partly-consented access |
| `chinese-criminal-thresholds-and-authorisation.md` | BORD | S044, S045, S046 | czt.ln.gov.cn, nj.jsjc.gov.cn, www.court.gov.cn | judicial thresholds plus the authorisation element; refused as a candidate this round |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | BORD | S077, S078, S079 | openstd.samr.gov.cn, std.sacinfo.org.cn, www.sac.gov.cn | crowd testing as a standardised service — programme-adjacent, standard primary |
| `cn-authorised-vulnerability-mining-regime.md` | BORD | S104 | iolaw.cssn.cn | 许可挖掘 as a named Chinese authorisation regime, from a CASS law-institute article |
| `cn-jp-severity-bands-and-attribution.md` | BORD | S083, S087 | web.archive.org, www.cert.org.cn | two state databases, two severity vocabularies |
| `triage-thresholds-2026-10-23-r5-amendment.md` | BORD | S073, S074 | gongbao.court.gov.cn, www.court.gov.cn | how courts measure 后果严重 and what counts as a system — triage input, court primary |
| `yuanwei-case-privileged-testing-unsettled.md` | BORD | S105 | iolaw.cssn.cn | the case the Chinese authorisation debate is organised around |
| `chinese-criminal-law-charge-names-2026-10-23.md` | ADJ | S075 | jtgl.beijing.gov.cn | charge names printed in the code |
| `chinese-grading-annexes-transcribed-2026-10-23.md` | ADJ | S072 | none — lane artifact | national grading standard, annex tables (lane artifact S072) |
| `chinese-grading-standard-draft-2026-10-23.md` | ADJ | S069, S070 | std.samr.gov.cn | national grading standard (202X draft) |
| `chinese-national-grading-applied-2026-10-23.md` | ADJ | S052, S059 | www.cnnvd.org.cn, www.phic.org.cn | grading applied by two state databases |
| `chinese-national-grading-model.md` | ADJ | S047, S048 | std.samr.gov.cn, www.sse.com.cn | national grading model A.1–A.7 |
| `chinese-statute-version-drift-2026-10-23-r4-amendment.md` | ADJ | S065 | www.npc.gov.cn | statute in force per the NPC record |
| `chinese-statute-version-drift-2026-10-23.md` | ADJ | S051 | gongbao.court.gov.cn | statute version drift (Gazette trap) |
| `chinese-vulnerability-taxonomy-and-grading.md` | ADJ | S037, S038 | openstd.samr.gov.cn, std.samr.gov.cn | national taxonomy/grading standard record |
| `cn-authorised-tester-acquittal-source-routes-2026-10.md` | ADJ | S113 | none — lane artifact | court-DB access probe |
| `cn-case-library-refusal-is-family-wide.md` | ADJ | S120 | none — lane artifact | case-library access probe |
| `cn-case-library-search-needs-a-session.md` | ADJ | S116 | none — lane artifact | case-library session requirement |
| `cn-criminal-offence-art285-baseline.md` | ADJ | S084, S088 | web.archive.org, www.npc.gov.cn | art. 285 baseline text |
| `cn-dyjf-case-library-api-base-and-registration-closed.md` | ADJ | S122 | none — lane artifact | case-library API base probe |
| `cn-revision-comment-disposition-not-published.md` | ADJ | S112 | none — lane artifact | TC260 disposition absence probe |
| `cncert-weekly-host-role-and-cnvd-series.md` | ADJ | S097 | www.cert.org.cn | CNCERT weekly host role |
| `cnnvd-document-serving-route-and-live-spec-table.md` | ADJ | S101 | www.cnnvd.org.cn | CNNVD document-serving route |
| `cnnvd-grading-specification-primary.md` | ADJ | S099 | raw.githubusercontent.com | CNNVD grading specification |
| `cnnvd-scoring-and-band-thresholds.md` | ADJ | S092 | html.rhhz.net | CNNVD numeric band thresholds |
| `cnnvd-specification-api-needs-a-session.md` | ADJ | S115 | none — lane artifact | CNNVD spec API probe |
| `cnnvd-specification-host-retired.md` | ADJ | S110 | none — lane artifact | CNNVD host retirement probe |
| `cnvd-2026-bulletin-absence-on-canonical-host.md` | ADJ | S111 | www.cert.org.cn | CNVD 2026 bulletin absence |
| `cnvd-bulletin-absence-by-directory-and-title.md` | ADJ | S117 | none — lane artifact | CNVD bulletin absence sweep |
| `cnvd-canonical-advisory-cross-references-2026-10-23.md` | ADJ | S071 | www.cert.org.cn | CNVD advisory CVE cross-reference |
| `cnvd-weekly-bulletin-publication-paths.md` | ADJ | S093 | www.cert.org.cn | CNVD weekly bulletin paths |
| `cnvd-weekly-series-locator-and-naming.md` | ADJ | S103 | www.phic.org.cn | CNVD weekly series index |
| `court-data-source-availability-2026-10.md` | ADJ | S108 | wenshu.court.gov.cn | court DB availability notice |
| `gb28458-companion-revision-plan.md` | ADJ | S124 | std.samr.gov.cn | GB/T 28458 companion revision plan |
| `gb30279-2020-annex-structure-and-industry-application.md` | ADJ | S089 | www.sse.com.cn | GB/T 30279-2020 annex structure |
| `gb30279-2020-appendix-table-rows.md` | ADJ | S114 | none — lane artifact | GB/T 30279-2020 appendix table rows |
| `gb30279-2020-chinese-scope-applicable-parties.md` | ADJ | S102 | down.waizi.org.cn | GB/T 30279-2020 scope/applicable parties |
| `gb30279-2020-draft-and-plan-machine-record.md` | ADJ | S106 | std.samr.gov.cn | GB/T 30279-2020 plan record fields |
| `gb30279-2020-edition-provenance.md` | ADJ | S096 | std.samr.gov.cn | GB/T 30279-2020 edition provenance |
| `gb30279-2020-english-edition-front-matter.md` | ADJ | S100 | chinastandards.org | GB/T 30279-2020 English edition front matter |
| `gb30279-2020-own-appendix-tables-text.md` | ADJ | S109 | none — lane artifact | GB/T 30279-2020 appendix text (lane artifact S109) |
| `gb30279-2026-revision-attachment-existence-test.md` | ADJ | S121 | none — lane artifact | GB/T 30279 revision attachment existence |
| `gb30279-2026-revision-comment-handling.md` | ADJ | S090, S091 | kass.sacinfo.org.cn, std.samr.gov.cn | GB/T 30279 revision comment disposition |
| `gb30279-2026-revision-drafting-process-and-disposition-reference.md` | ADJ | S119 | kass.sacinfo.org.cn | GB/T 30279 revision drafting note |
| `gb30279-2026-revision-drafting-units-and-english-title.md` | ADJ | S107 | std.samr.gov.cn | GB/T 30279 revision drafting units |
| `gb30279-revision-annexes-and-change-list.md` | ADJ | S085, S086 | kass.sacinfo.org.cn | GB/T 30279 revision annexes/change list |
| `tc260-portal-serves-one-catch-all-shell.md` | ADJ | S118 | none — lane artifact | TC260 portal shell probe |

Totals: IN 18 · BORD 9 · ADJ 40 (grading/standards 20, statute 4, source-access probe 16). Source ids in the table are the *package's* numbering, which is not the lane's after S031.

---

## 3. Top 5 candidates for a future assimilation round

Ranked by province centrality × ground the lane does not hold × public primary × recheck health. Each line: entry — ground it would add — public primary (host).

1. **`claim-packaging-and-report-quality.md`** (S034 zc.cnvd, S035 security.360.cn, S036 security.bilibili.com) — grounds the *claim package* itself: proof-over-theory admission rule, report quality scored on five named fields (1.1/1.0/0.9), and an enumerated 降级 scenario list — the openable replacement for the lane's lost `claim-package-contract.md`. Public primaries: **zc.cnvd.org.cn, security.360.cn, security.bilibili.com** (all three reached directly). Caveat: its recheck re-opens only S036.

2. **`cn-crowdsourced-testing-roles-and-conduct.md`** (S081 zc.cnvd.org.cn, S082 std.samr.gov.cn) — grounds China's programme-side conduct code inside a grant: four roles (众测需求方/组织方/授权测试方/审计方), prohibited methods (no direct vendor contact, no validating unstable systems, no retaining user data), and why "the platform accepted it" is not vendor consent. Public primaries: **zc.cnvd.org.cn** (2018 公告) and **std.samr.gov.cn** (project record 20220608-T-469; the published GB/T 43741-2024 text itself is behind 在线预览). Caveat: recheck is prose with no URL (class: prose).

3. **`program-scope-rules-and-asset-boundaries.md`** (S031 hackerone.com, S034 zc.cnvd.org.cn, S035 security.360.cn) — grounds the distinction the lane's F03 currently blurs: a scope list is not a safe harbour, and third-party assets are never the platform's to authorise; three platforms, two mechanisms. Public primaries: **hackerone.com, zc.cnvd.org.cn, security.360.cn**. Blocker: its S031 is the colliding id — renumber to S125+ before admission, and repair the recheck, which re-opens only hackerone.

4. **`japanese-domestic-disclosure-workflow.md`** (S042 ipa.go.jp, S043 jpcert.or.jp) — grounds a second, non-market timeline for F02: the nine-step national flow and **起算日** as a clock anchored on *first attempted contact*, withdrawable after one year. Public primaries: **ipa.go.jp** (`/security/todokede/vuln/process.html`) and **jpcert.or.jp** (partnership_guideline2026.pdf). Caveat: recheck covers S043 only.

5. **`iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`** (S064 jpcert.or.jp, S068 cisco.com) — grounds the round-1 paywalled ISO/IEC 29147 lead without buying the standard: the obligation difference (P-guideline does not require a disclosure policy; 29147:2014 does) plus a 留意すべき事項 crosswalk table, and a vendor's own conformance claim. Public primaries: **jpcert.or.jp**, **cisco.com**. Caveat: recheck re-opens S064 only.

Runners-up, all in province and all weaker on one axis: `vendor-cvd-policy-crosswalk-2026-10-23.md` (cisco.com; the only entry with a clean exact-URL recheck), `vendor-third-party-finding-coordination-2026-10-23.md` (microsoft.com/msrc/msvr; clean recheck, narrow ground), `program-severity-ladders-and-reward-scales.md` (bugcrowd VRT + the 4-vs-12-point worked example; recheck covers 2 of 4 rows), `japanese-vendor-disclosure-policies-2026-10-23.md` (cybozu/pepabo/hitachi; recheck covers 2 of 4 rows).

---

## 4. Recheck audit — detail

Class assignment is mechanical: `source:` rows parsed from each file's front matter; `recheck:` searched for the exact source URL, then for the source host.

### 4.1 exact URL for every cited source (6)

`chinese-criminal-law-charge-names-2026-10-23`, `chinese-statute-version-drift-2026-10-23`, `chinese-statute-version-drift-2026-10-23-r4-amendment`, `iso-29147-and-30111-division-of-labour-2026-10-23`, `vendor-cvd-policy-crosswalk-2026-10-23`, `vendor-third-party-finding-coordination-2026-10-23`

### 4.2 recheck names a URL on the same host, but not the source row's own URL (3)

`authorization-safe-harbor-and-scope-2026-10-23-r4-amendment` — S067 never re-opened · `cnvd-canonical-advisory-cross-references-2026-10-23` — S071 never re-opened (recheck reads the `/publish/main/9/index.html` listing instead of the cited article) · `cnvd-weekly-bulletin-publication-paths` — S093 never re-opened by exact URL (recheck re-sweeps the `upload/File/CNVD2026*.pdf` glob, which is a weaker but arguably covering check)

Three further entries name a URL that is a *different document* on a host they also cite: `chinese-criminal-case-law-2026-10-23` (recheck reads S061's URL, leaves S051/S063 on `gongbao.court.gov.cn` un-opened), `japanese-severity-vocabulary-and-impact-model` (recheck reads S050, leaves S049's PDF un-opened), `program-quirks-2026-10-23-amendment` (recheck reads S056's FAQ, leaves S055 un-opened). They are counted in 4.3.

### 4.3 a cited source row's host never appears in the recheck (20)

- `authorization-safe-harbor-and-scope-2026-10-23-amendment.md` — never re-opened: S058, S054, S057
- `chinese-criminal-case-law-2026-10-23.md` — never re-opened: S051, S063
- `chinese-criminal-thresholds-and-authorisation.md` — never re-opened: S045, S046
- `chinese-crowd-testing-national-standard-2026-10-23.md` — never re-opened: S077, S078
- `chinese-national-grading-applied-2026-10-23.md` — never re-opened: S059
- `chinese-national-grading-model.md` — never re-opened: S047
- `chinese-program-severity-instrument.md` — never re-opened: S047
- `chinese-vulnerability-taxonomy-and-grading.md` — never re-opened: S037
- `claim-packaging-and-report-quality.md` — never re-opened: S034, S035
- `gb30279-revision-annexes-and-change-list.md` — never re-opened: S085, S086
- `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` — never re-opened: S068
- `japanese-disclosure-legal-framework.md` — never re-opened: S039
- `japanese-domestic-disclosure-workflow.md` — never re-opened: S042
- `japanese-severity-vocabulary-and-impact-model.md` — never re-opened: S043
- `japanese-vendor-disclosure-policies-2026-10-23.md` — never re-opened: S057, S060
- `program-quirks-2026-10-23-amendment.md` — never re-opened: S057
- `program-scope-rules-and-asset-boundaries.md` — never re-opened: S034, S035
- `program-severity-ladders-and-reward-scales.md` — never re-opened: S034, S036
- `statutory-authorization-in-three-traditions.md` — never re-opened: S040, S041
- `triage-thresholds-2026-10-23-r5-amendment.md` — never re-opened: S073

### 4.4 recheck is prose — no URL, no shell command (20)

`authorised-account-scope-and-intrusion`, `authorised-tester-case-law`, `cn-authorised-vulnerability-mining-regime`, `cn-criminal-offence-art285-baseline`, `cn-crowdsourced-testing-roles-and-conduct`, `cn-jp-severity-bands-and-attribution`, `cncert-weekly-host-role-and-cnvd-series`, `cnnvd-document-serving-route-and-live-spec-table`, `cnnvd-grading-specification-primary`, `cnnvd-scoring-and-band-thresholds`, `cnvd-weekly-series-locator-and-naming`, `court-data-source-availability-2026-10`, `gb30279-2020-annex-structure-and-industry-application`, `gb30279-2020-chinese-scope-applicable-parties`, `gb30279-2020-draft-and-plan-machine-record`, `gb30279-2020-edition-provenance`, `gb30279-2020-english-edition-front-matter`, `gb30279-2026-revision-comment-handling`, `gb30279-2026-revision-drafting-units-and-english-title`, `yuanwei-case-privileged-testing-unsettled`

### 4.5 recheck has a shell command but no URL — runnable only against a lane-local artifact or a re-minted token (5)

`authorised-testing-rules-of-engagement`, `chinese-grading-standard-draft-2026-10-23`, `cnvd-2026-bulletin-absence-on-canonical-host`, `gb28458-companion-revision-plan`, `gb30279-2026-revision-drafting-process-and-disposition-reference`

### 4.6 every source row is a lane-local capture (13)

`chinese-grading-annexes-transcribed-2026-10-23`, `cn-authorised-tester-acquittal-source-routes-2026-10`, `cn-case-library-refusal-is-family-wide`, `cn-case-library-search-needs-a-session`, `cn-dyjf-case-library-api-base-and-registration-closed`, `cn-revision-comment-disposition-not-published`, `cnnvd-specification-api-needs-a-session`, `cnnvd-specification-host-retired`, `cnvd-bulletin-absence-by-directory-and-title`, `gb30279-2020-appendix-table-rows`, `gb30279-2020-own-appendix-tables-text`, `gb30279-2026-revision-attachment-existence-test`, `tc260-portal-serves-one-catch-all-shell`

---

## 5. Remaining unknowns

- **UNVERIFIED** whether the lane's `.ufo/waves/round-24/assimilation/renumber-map.tsv` exists: `claims.json` names it as the collision map, the directory holds only `census-before.txt`, `collisions`, `reg-ids`, `staged-ids`. Id mapping is therefore read from `MERGE-REPORT.json` + `corpus/SOURCES.md` only.

- **UNVERIFIED** whether `SOURCES.append.md` carries the 94 rows in the lane's 11-column schema with the id shift applied after the S031 collision; I read the package's front matter only.

- The published full texts of GB/T 43741-2024 and GB/T 30279—2020 sit behind 在线预览; only project records and draft attachments were reachable from this seat. Unchanged by this triage, but it caps what the 20 grading entries can ever verify.

- Adjacent-vs-in-province is a judgement, not a measurement: I placed entries by what a reader can *use* for a bounty claim (programme rules, claim package, disclosure handling) and put anything whose primary is a court, statute or national standard on the adjacent side even when its subject is authorisation. The 9 BORD rows are the honest grey zone and should be arbitrated by L1, not by this table.
