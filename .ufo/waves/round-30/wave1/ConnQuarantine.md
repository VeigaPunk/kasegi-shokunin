# ConnQuarantine — Cross-Source Pattern Join & Quarantine Synthesis (Round 30 Wave 1)

**Seat:** `ConnQuarantine` (leaf connector, UFO-FSD role)  
**Lane:** `kasegi-shokunin`  
**Milestone:** `round-30` | **Wave:** `kasegi-r30-build` (wave 1)  
**Assigned Judged Axis:** `coverage` (supporting `depth:verifiability`)  
**Report Destination:** `.ufo/waves/round-30/wave1/ConnQuarantine.md`

---

## 1. Evidence (Current Round Cache & Local Repo Evidence)

Measured bytes and authoritative digests:
- **Quarantine Slice:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-30/assimilation/quarantine-slice`  
  `sha256: d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862` (7 rows, extracted by `ScoutQuarantineSlice`)
- **Staged Package SOURCES:** `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`  
  `sha256: 4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` (94 staged rows, S031–S124)
- **Absent Defect Register:** `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`  
  `sha256: 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
- **Lane Registry:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`  
  `sha256: f55025c2275d3d08eb254b4a3c83e578e79e55ad30e806591b85a6f1d52735ff` (45 rows: S001–S045)
- **Claims Specification:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-30/claims.json`  
  `sha256: 68d77757c71f1779be89ac97efe3f1299a5858187c7f95e06d9da4e52cae523b`
- **Existing Lane Snapshot for Cisco Policy (S040):**  
  `corpus/source-snapshots/round-25/S040.txt` (`sha256: b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`)

---

## 2. F14 Benchmark Sources (Context & Lineage)

Frontier F14 (*Japanese severity vocabulary and the handling-priority model*) admits entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` backed by three source documents:
1. **Staged S049 → Lane S046:** IPA JVN iPedia 活動報告レポート  
   `https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf`  
   *Publisher/Lineage:* Information-technology Promotion Agency, Japan (IPA / 独立行政法人情報処理推進機構). JVN severity band mapping.
2. **Staged S050 → Lane S047:** IPA JVN iPedia の登録状況 2026年第3四半期  
   `https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html`  
   *Publisher/Lineage:* IPA. Quarterly statistical severity distribution and CWE rankings.
3. **Staged S043 → Lane S041:** JPCERT/CC 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月  
   `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf`  
   *Publisher/Lineage:* JPCERT Coordination Center (JPCERT/CC) in early warning partnership with METI and IPA. Handling-priority matrix (付録4). Already registered in lane as `S041`.

The core institutional lineage of F14 is the **Japanese statutory/coordinator vulnerability handling framework** (IPA, JPCERT/CC, METI Notification No. 19).

---

## 3. Quarantine Slice Cross-Source Join Table

For each of the 7 rows in `.ufo/waves/round-30/assimilation/quarantine-slice`, the table records:
- Register Class (`payload-absent` vs `unreachable`)
- Document Title and Cited Locator
- Publisher and Institutional Lineage
- F14 Relationship (`related-to-F14` vs `unrelated`)
- Document Identity in Lane Registry
- Required Lane ID if Adopted (*strictly document-identity driven; never arithmetic*)

| Staged ID | Register Class | Document Title & Locator | Publisher & Lineage | F14 Overlap | Lane Registry Match | Required Lane ID If Adopted |
|---|---|---|---|---|---|---|
| **S037** | `payload-absent` | 国家标准全文公开系统 标准信息 GB/T 30279-2020<br>`https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | 国家市场监督管理总局 (SAMR) / 中国国家标准化管理委员会 (SAC). Chinese national vulnerability grading standard catalogue. | `unrelated` | None (absent) | **New sequential ID (S048+)**<br>*Never arithmetic S037 (collides with lane S037 Cybozu FAQ)* |
| **S054** | `payload-absent` | 重要電子計算機に対する不正な行為による被害の防止に関する法律等の施行を踏まえた脆弱性関連情報の取扱いについて（要請）<br>`https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | 内閣府サイバー官民連携室長 (Cabinet Office); recipient & publishing host: 独立行政法人情報処理推進機構 (IPA). Japanese statutory notification feeding METI Notification No. 19. | **`related-to-F14`** | None (absent) | **New sequential ID (S048+)**<br>*Never arithmetic S054. Isolated from F14 gate (cited by statutory amendment, not F14)* |
| **S048** | `unreachable` | 全国标准信息公共服务平台 标准计划 20260806-T-469<br>`https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | SAMR / SAC / 全国网络安全标准化技术委员会 (TC260). Chinese national standard live revision plan. | `unrelated` | None (absent) | **New sequential ID (S048+)**<br>*Never arithmetic S048* |
| **S065** | `unreachable` | 全国人民代表大会常务委员会《现行有效法律目录》（303件）<br>`http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | 全国人大常委会 (NPCSC). Chinese national legislature statutory catalogue for Criminal Law (刑法). | `unrelated` | None (absent) | **New sequential ID (S048+)**<br>*Never arithmetic S065* |
| **S068** | `unreachable` | Cisco Security Vulnerability Policy<br>`https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | Cisco Systems, Inc. (US vendor PSIRT). Mentions JP-CERT in multi-vendor coordination clause, but institutional governance is US enterprise corporate PSIRT. | `unrelated` | **Matches lane `S040` exactly** (`SOURCES.md:46`) | **`S040`**<br>*Document identity match. Zero new ID allocation needed* |
| **S069** | `unreachable` *(suspected truncated locator)* | 国家标准《网络安全技术 网络安全漏洞分类分级指南》（征求意见稿）GB/T 30279—202X<br>`https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_WD_2025005470_…` | 全国网络安全标准化技术委员会 (TC260) / 中国信息安全测评中心 (CNITSEC). Chinese national standard draft. | `unrelated` | None (absent) | **New sequential ID (S048+)**<br>*Never arithmetic S069* |
| **S070** | `unreachable` *(suspected truncated locator)* | 国家标准《网络安全技术 网络安全漏洞分类分级指南》（征求意见稿）编制说明<br>`https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_DI_2025005470_…` | 全国网络安全标准化技术委员会 (TC260) / 中国信息安全测评中心 (CNITSEC). Drafting explanation note. | `unrelated` | None (absent) | **New sequential ID (S048+)**<br>*Never arithmetic S070* |

---

## 4. Lesson Gate Feeding & Verdict Consistency

This cross-source join feeds directly into `ScribeQuarantine` and `ScribeLessonGate` to establish consistent, evidence-based verdicts across the wave:

1. **Isolation of the F14 Admission Gate from Quarantine Defects:**
   - Although **S054** is marked `related-to-F14` due to its IPA publisher and Japanese statutory lineage, the F14 entry (`japanese-severity-vocabulary-and-impact-model.md`) **does not cite S054**. F14 cites only S046 (staged S049), S047 (staged S050), and S041 (staged S043).
   - S054 is used exclusively by an out-of-round statutory amendment (`corpus/knowledge/authorization-safe-harbor-and-scope-2026-10-23-amendment.md`).
   - Therefore, S054's quarantine status (`payload-absent`) does **not** contaminate or block the admission of F14.
2. **Rejection Consistency for Unrelated Quarantine Rows:**
   - The five Chinese standards and legislative rows (**S037, S048, S065, S069, S070**) are all `unrelated` to F14. They belong to out-of-province themes (Chinese national grading and criminal thresholds) that were previously refused in round 25/29. Their presence in the quarantine slice reinforces refusal at the F14 Gate without impacting the Japanese CVD theme.
3. **Resolution of Staged S068 via Document Identity:**
   - In `absent-defect-register.md`, **S068** is classified as `unreachable` ("the cited source could not be fetched").
   - `considerthese/2026-10-25.md` logged routed defect **R25-5**: Cisco's URL 403s automated/browser fetchers without bot-bypass headers.
   - However, by document identity, staged S068 **is byte-equal in URL to lane S040** (`https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`), which was already registered in round 25 and captured locally (`corpus/source-snapshots/round-25/S040.txt`).
   - The lesson Gate can close S068 as `already-mined-by-document` (mapped to `S040`), resolving the unreachable defect locally without network calls.

---

## 5. Non-Obvious Move: Compatible Synthesis Proposal

### Proposed Move:
**Pre-Adoption Document-Identity Gate for Quarantine Resolution with Lineage Decoupling**

Synthesize the `by_document_rule` of C2 (`claims.json:62`), the open-defects ledger pattern (proposal 5 in `considerthese/2026-10-25.md`), and QUALITY R8:
1. **Deduplicate Before Fetch:** Before dispatching external network re-fetches for unreachable quarantine rows, run a strict URL match against the lane registry (`corpus/SOURCES.md`). Where a match exists (staged S068 = lane S040), close the quarantine ticket immediately with status `already-mined-by-document` mapped to the existing ID, citing the lane's local verified capture (`corpus/source-snapshots/round-25/S040.txt`).
2. **Decouple Institutional Lineage from Theme Scope:** Mandate that publisher overlap (`related-to-F14`) cannot substitute for entry citation. A quarantined row from the same publisher (IPA's S054) must remain quarantined under its own falsification check without impeding the clean admission of sibling publications (S046/S047) cited by the F14 entry.
3. **Enforce Zero-Arithmetic ID Allocation:** Formally record in the lesson Gate that all 6 absent quarantine rows (S037, S048, S054, S065, S069, S070) have no reserved S-space arithmetic slots; they may only take the next free monotonic lane ID (S048+) at the point an admitted entry cites them.

### Affected Axes:
- **`coverage` (Primary):** Protects clean admission of F14 (frontier admitted 13 → 14, registry 45 → 47) by preventing false-positive thematic blocking from S054 and preventing duplicate registry entries from S068.
- **`depth:verifiability` (Secondary/No-Harm):** Eliminates un-reproducible external network fetch failures against anti-bot targets (Cisco S068 / R25-5), grounding verification in committed snapshot bytes.

### Risks:
- *Risk 1 (Over-eager reuse):* Mapping S068 to S040 assumes Cisco's policy text in round 25 satisfies any quotes asserted by the staged entry. *Mitigation:* The lane snapshot `S040.txt` is verified and immutable; any staged entry adopting S040 must pin quotes against that existing capture.
- *Risk 2 (Premature clearance of S054):* Reviewers seeing IPA's name might conflate S054 with F14's green IPA documents. *Mitigation:* Explicitly marking S054 as `related-to-F14` in lineage but `quarantined: payload-absent` in validity keeps the boundary strict.

### Verification:
1. `grep -cE 'https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html' corpus/SOURCES.md` returns exactly 1 (lane S040).
2. `sources-census.sh validate --root . kasegi` exits 0 (no duplicate URLs or colliding S-ids).
3. `frontier-recheck-count.py` passes 17/17 with F14 admitted and no references to unadmitted quarantine rows.
4. `ScribeQuarantine.md` and `ScribeLessonGate.md` record matching verdicts for all 7 slice rows.

---

## 6. Self-Audit & Operational Directives
- Leaf seat: No subagents dispatched, no external git/jj mutations performed.
- Read-only execution against `/home/vgpnk/Projects/shokuknow/` and fleet root.
- Tool installations: None (standard Unix utilities used).
