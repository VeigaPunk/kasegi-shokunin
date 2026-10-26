# ConnSibling Receipt — Sibling-Overlap Scan, Province Boundary & Synthesis for F15 (Round 31, Wave 1)

- **Seat**: `ConnSibling` (UFO-FSD connector)
- **Round**: 31, Wave 1
- **Lane**: `kasegi-shokunin` (working root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
- **Base commit**: `b374febbb33ccadade78a787279707fd5d2e6e1d`
- **Answering model**: `google-antigravity/gemini-3.8-flash`
- **Scope & Role**: Leaf connector. Read-only sibling corpus scan; PROVINCE.md boundary review; cross-look of frontier entries F06/F10/F11; bounded synthesis proposal. Single write target: `.ufo/waves/round-31/wave1/ConnSibling.md`.

---

## 1. Sibling-Overlap Scan for F15 Ground

### 1.1 Question
Does any sibling lane in the fleet (`chousa-shokunin`, `kengaku-shokunin`, `kake-shokunin`, `kagi-shokunin`, `kumitate-shokunin`, `kotoba-shokunin`) already hold ground on:
- Microsoft MSRC or MSVR (Microsoft Security Vulnerability Research),
- Third-party vulnerability coordination, or
- Vendor security research programmes?

### 1.2 Target Corpora (Read-Only)
The scanned target paths encompass `corpus/README.md` and `corpus/knowledge/` across all 6 sibling lanes:
1. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md` and `corpus/knowledge`
2. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md` and `corpus/knowledge`
3. `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md` and `corpus/knowledge`
4. `/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/README.md` and `corpus/knowledge`
5. `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/README.md` and `corpus/knowledge`
6. `/home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/README.md` and `corpus/knowledge`

### 1.3 Grep Executions and Outputs

Executed command suite:
```bash
TARGET_PATHS=(
  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md
  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge
  /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md
  /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge
  /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/README.md
  /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/knowledge
  /home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/README.md
  /home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge
  /home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/README.md
  /home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/knowledge
)
```

#### Term 1: `MSVR`
```bash
grep -ril "MSVR" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)

grep -rin "MSVR" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)
```
**Result**: 0 files match, 0 line hits. Completely absent across all siblings.

#### Term 2: `Microsoft Security Vulnerability Research`
```bash
grep -ril "Microsoft Security Vulnerability Research" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)

grep -rin "Microsoft Security Vulnerability Research" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)
```
**Result**: 0 files match, 0 line hits. Completely absent across all siblings.

#### Term 3: `coordinator of vulnerabilities`
```bash
grep -ril "coordinator of vulnerabilities" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)

grep -rin "coordinator of vulnerabilities" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)
```
**Result**: 0 files match, 0 line hits. Completely absent across all siblings.

#### Term 4: `coordinated vulnerability disclosure`
```bash
grep -ril "coordinated vulnerability disclosure" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)

grep -rin "coordinated vulnerability disclosure" "${TARGET_PATHS[@]}"
# Output: (none; exit 1)
```
**Result**: 0 files match, 0 line hits. Completely absent across all siblings.

#### Term 5: `third-party`
```bash
grep -ril "third-party" "${TARGET_PATHS[@]}"
```
Output files (13 matching files across 6 siblings):
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/aggregator-vs-source-r36.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-count-semantics-r37.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/istic-citation-verification-r39.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/benchmark-task-validity-checklist.md`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json`
- `/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/knowledge/drift-gate.md`
- `/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/knowledge/handler-on-disk-state.md`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/README.md`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/executable-scorecard.md`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/kimi-config-plane.md`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/remaining-scripts-census.md`
- `/home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/knowledge/client-trust-gates-round68.md`

Detailed `path:line` output for `third-party`:
```
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md:1072:| `knowledge/citation-count-semantics-r37.md` | Round-49 note (adopted by document): what a CNKI count is a count of, as copies and third-party guides state it — a co-authorship self-citation rule and zero-count rows not listed (S100), the data specification's 文献标志码 and GB/T 7714 / ISO 690 split (S101), separate citation and download columns (S102), the AI trace panel's source and counter fields (S103) | `S100`–`S103`; `corpus/evidence/round49/spans.tsv`; `corpus/lessons/round-49.md` `## Gate` |
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/aggregator-vs-source-r36.md:87:  hosted copies and a third-party guide.
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-count-semantics-r37.md:10:ground: source hierarchy — what an index's counter is a count of; every source here is a copy or a third-party guide (no CNKI first-party page was opened), so the rows are scoped to "as these copies state"
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-count-semantics-r37.md:32:- **A third-party guide to the CNKI interface (Japanese).** The KNS8.0 guide
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/istic-citation-verification-r39.md:14:  representative works, and their 收录 and 引用, delivered as a third-party
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/istic-citation-verification-r39.md:40:- **The report is the officer's record, and its printed form is stated elsewhere.** Review and archive are the retrieval officer's steps, `03 完成并审核 报告 06 出具正式报 告并存档` (`char 380`), and the default deliverable is `检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件` (`char 1784`); a third-party report artefact that outlives the session is the shape the lane's support side wants, and what the page does not attach to it is the state of the indexes it was taken from (`S104`).
/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/benchmark-task-validity-checklist.md:25:them. S091 (ABC) is the one independent third-party instrument here, and it judges other people's
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:152:    "publisherCheck": "Preparation only: kake inventories the scope and requests a separately operator-authorized evaluator; tabi owns authorized browser/assistive-technology execution and any account operation remains operator-gated. The following is a requested criterion-specific procedure, not permission to run it: On each page in scope, list every source of audio that plays automatically, without the user requesting audio playback, including embedded video, background music, and third-party widgets. Time how long each one plays. For any audio that plays automatically for more than 3 seconds, confirm one of two things: a mechanism available to the user paus…
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:155:    "limitation": "This card supports manual review only; it records no pass or fail result. Source inspection or automated scanning cannot establish how long audio plays at runtime, whether a script or third-party embed starts audio, or whether a mechanism actually works and is independent of system volume, so a human must observe the rendered page. Audio that plays automatically for 3 seconds or less is outside this criterion's requirement, and the card makes no claim about other criteria or about overall WCAG conformance.",
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:260:    "publisherCheck": "Preparation only: kake inventories the scope and requests a separately operator-authorized evaluator; tabi owns authorized browser/assistive-technology execution and any account operation remains operator-gated. The following is a requested criterion-specific procedure, not permission to run it: List every component on each page that keyboard focus can reach, including embedded players, iframes, widgets, rich-text editors, dialogs and third-party content. For each one, a human reviewer moves focus into the component with the keyboard only, then tries to move focus out with unmodified Tab, Shift+Tab, arrow keys or other standard exit meth…
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:261:    "evidenceNeeded": "A per-page inventory of focusable components, including embedded and third-party content. For each component: the keys used to enter and leave it, the result (focus left or stayed trapped), and the browser, assistive-technology and platform used. Where a non-standard exit is needed: the exact wording and location of the advice telling users how to move focus away, captured as a screenshot or transcript. Record the reviewer's name and the review date. Shared record for every card: reviewer, evaluation date, delivered build/revision, full page/process scope and variants, relied-upon technologies and accessibility-support evidence, method a…
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:262:    "failureExample": "A page embeds a third-party video player. Once focus enters the player, Tab and Shift+Tab only cycle through its play, volume and fullscreen buttons. Escape does nothing, and no instructions explain how to return to the rest of the page. A keyboard-only user cannot reach the content after the player.",
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:296:    "publisherCheck": "Preparation only: kake inventories the scope and requests a separately operator-authorized evaluator; tabi owns authorized browser/assistive-technology execution and any account operation remains operator-gated. The following is a requested criterion-specific procedure, not permission to run it: Inventory every moving, blinking, scrolling, or auto-updating item on each page in scope (carousels, marquees, animated banners, tickers, live feeds, auto-refreshing widgets), including third-party embeds and decorative animation. For each moving, blinking, or scrolling item, record whether it starts automatically, lasts more than five seconds, a…
/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/accessibility-review-cards.json:308:    "publisherCheck": "Preparation only: kake inventories the scope and requests a separately operator-authorized evaluator; tabi owns authorized browser/assistive-technology execution and any account operation remains operator-gated. The following is a requested criterion-specific procedure, not permission to run it: Inventory every item on each page that can flash: video, animation, animated images, canvas or CSS effects, transitions, ads and third-party embeds, including content not relied on to meet any other criterion. For each item, confirm no one-second period contains more than three flashes; otherwise confirm the flashes are below the general flash an…
/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/knowledge/drift-gate.md:162:  package manager's, and they are third-party bytes the lane must not own.
/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/knowledge/handler-on-disk-state.md:176:  declares it). Not a secret — but it is 4.7 MB of third-party catalog sitting
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/README.md:61:| `lessons/round-6-aggregator-audit.md` | Round-6 aggregator audit (third-party artifact, aggregator-owned): independent re-verification of this lane's counts; ERROR rows quoted inside it are re-detected as findings (no quotation exemption) | LOG.md round-6; artifact owner: aggregator lane |
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/README.md:62:| `lessons/round-8-aggregator-box3-coldrun.md` | Aggregator-lane round-8 box-3 non-author cold run against this lane's `SKILL.md` (third-party artifact, aggregator-owned, committed into this repo by that lane as `e79fefa`): re-ran the checklist items and measured this lane's embedded live claims at that time; its own pins were correct then and read as stale now — recorded, not rewritten | LOG.md round-8; artifact owner: aggregator lane |
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/README.md:63:| `lessons/round-9-aggregator-corpus-verdict.md` | Aggregator-lane round-9 corpus verdict on THIS repo at revision `e0e5de1` (third-party artifact, aggregator-owned, committed into this checkout as `93b0567`): box 3 firm at `59e6c0c`, both hermetic tallies green, rule 8 FAIL-literal / PASS-intent, rules 1/2/4/6/7/9 still failed, and the Gate-standard mapping gap in `SKILL.md` | LOG.md round-9; artifact owner: aggregator lane |
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/executable-scorecard.md:459:  round's own landing plus the third-party `lessons/round-8-aggregator-box3-coldrun.md`
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/kimi-config-plane.md:85:  (`"managed:kimi-code"`) with a nested `.oauth` sub-table, plus **6 third-party
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/kimi-config-plane.md:89:  `alibaba-token-plan{,-2,-3}` groups** — i.e. **4 distinct hosts for the 6 third-party groups**.
/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/remaining-scripts-census.md:366:must report zero errors in this note (its remaining errors are third-party
/home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/knowledge/client-trust-gates-round68.md:4:source: S201 — Microsoft Agent Framework — Agent Skills — https://learn.microsoft.com/en-us/agent-framework/agents/skills — the "Security best practices" subsection — located quote "Agent Skills should be treated like any third-party code you bring into your project."
/home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/knowledge/client-trust-gates-round68.md:26:| Microsoft Agent Framework | the skill tools require approval by default, and a skill is reviewed as third-party code before it is deployed | "Agent Skills should be treated like any third-party code you bring into your project." | S201 |
/home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/knowledge/client-trust-gates-round68.md:39:   skill as third-party code with the review discipline of an open-source dependency.
```

### 1.4 Analysis of Adjacent Terms Across Siblings
- **`MSRC` search**:
  ```bash
  grep -rin "MSRC" "${TARGET_PATHS[@]}"
  ```
  Only appears in `kotoba-shokunin/corpus/knowledge/claude-md-surface.md:27, 29`:
  - L27: `~/scratch/msrc-hunt2/fluentui/CLAUDE.md` (118L, nx-workspace generated)
  - L29: `~/scratch/msrc-hunt2/azure-sdk-for-net/**`
  These are filesystem inventory paths from a disk census of `CLAUDE.md` files; `kotoba` holds prompt/markdown convention ground, not vulnerability research or coordination.
- **`vulnerability` search**:
  ```bash
  grep -rin "vulnerability" "${TARGET_PATHS[@]}"
  ```
  Hits:
  1. `chousa-shokunin/corpus/knowledge/pin-capture-env-r37.md:44`: used metaphorically for bash environment drift (`BASH_ENV` pollution).
  2. `kake-shokunin/corpus/README.md:457-460`: **explicit jurisdictional refusal**:
     > "Vulnerability handling itself (report intake, triage, remediation, disclosure timing, bounty and policy operation) stays outside this province, and writing, building or deploying the file on an owned site is an operator-owned publishing action."
     (`kake-shokunin/corpus/README.md:457-460`, 25 words).
- **`vendor research` / `vulnerability coordination`**:
  ```bash
  grep -rin "vulnerability coordination" "${TARGET_PATHS[@]}"
  grep -rin "vendor research" "${TARGET_PATHS[@]}"
  ```
  Both return `NO MATCH` (exit 1).

### 1.5 Scan Conclusion
**Zero overlap.** No sibling lane holds ground on Microsoft MSRC/MSVR, third-party vulnerability coordination, or vendor research programmes. Sibling `kake-shokunin` affirmatively disclaims vulnerability intake and handling in its own index.

---

## 2. Province Analysis (`PROVINCE.md`) & Boundary Assessment

### 2.1 Kasegi Province Definition
Reading `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md`:
- **Domain**:
  > "Domain: bounty & security research — scopes ~/Projects/bounties, program rules, claim packages"
  (`PROVINCE.md:3`, 10 words).
- **Core**:
  > "The line-3 domain comprises program rules, scopes, and claim packages; the core also covers triage and claim gates, and submission/disclosure packaging."
  (`PROVINCE.md:29-30`, 23 words).
- **Adjacent**:
  > "Sibling lanes are reported, not absorbed: - chousa — research method and source hierarchy - kagi — secrets and vault handling - kake — web properties - kengaku — LLM evaluation and benchmarks"
  (`PROVINCE.md:45-50`, 25 words).
- **Refusal**:
  > "Live-target testing is refused; this corpus is documentation only."
  (`PROVINCE.md:52`, 10 words).

### 2.2 Boundary Assessment: Is F15 Inside Province or Contested?
- **F15 sits squarely INSIDE kasegi's province.**
  - F15 examines how a vendor operates a formal research programme (MSVR) as an intake channel for vulnerabilities found in third-party software, formalizing the vendor's operational role as a finder, affected party, and multi-vendor coordinator.
  - This directly expands kasegi's core domain of "program rules, scopes, and claim packages" and "submission/disclosure packaging".
  - It extends existing frontier entries F06 (multi-party coordination guidelines), F10 (vendor disclosure policies), and F11 (ISO 29147/30111 division of labour).
- **Uncontested**:
  - No sibling claims this territory.
  - Sibling `kake-shokunin` explicitly disclaims vulnerability handling, report intake, triage, and disclosure timing.
  - Sibling `chousa` owns research methodology and source hierarchy; `kagi` owns secrets/vaults; `kengaku` owns benchmark validation; `kotoba` owns prompt surfaces; `kumitate` owns packaging.
- **Strict Guardrails**:
  - In accordance with `PROVINCE.md:52` and QUALITY Q6, F15 must remain strictly documentation-only. The entry analyzes the publicly published MSVR charter (`https://www.microsoft.com/en-us/msrc/msvr`), without probing endpoints, submitting reports, or referencing private credentials.

---

## 3. Cross-Look at Kasegi Frontier Entries F06, F10, F11

Examining existing frontier entries provides the concrete standard for admission under QUALITY Q1–Q10 and R1–R15:

### 3.1 Entry F06 (`knowledge/multiparty-vulnerability-coordination.md`, S018 — FIRST Guidelines v1.1)
- **Entry Shape**:
  - Three-line header (`source:`, `verified-at:`, `recheck:` citing `source-recheck.py`).
  - `## Rule`: Formal definition of relationships and responsibilities.
  - `## Evidence`: Structured table mapping Located source, Exact quote (<=25 words), and Package-review consequence.
  - `## Falsifiable local check`: Synthetic worksheet evaluation rejecting an undifferentiated single "vendor" row.
  - `## Rejected`: Explicit rejection of over-generalization:
    > "The upstream vendor shipped, so every downstream user is patched and public disclosure is automatically safe." (`multiparty-vulnerability-coordination.md:43-44`, 15 words).
  - `## Limits`: Discloses capture bounds, documentation boundaries, and unobserved context.
- **Patterns F15 should follow**:
  - Distinct role taxonomy: clearly differentiate finder, upstream vendor, downstream vendor, and coordinator.
  - Mandatory capture gap disclosure (e.g. noting unobserved chrome or dynamic headers).
- **Patterns F15 should avoid**:
  - Conflating an upstream fix with downstream resolution; assuming a coordinator always exists when optional.

### 3.2 Entry F10 (`knowledge/vendor-disclosure-policies-as-corpus-objects.md` & crosswalk, S036–S040)
- **Entry Shape**:
  - `## Attribution`:
    > "Every statement below is the named vendor's own position about its own handling: a first-party self-description of published policy text, not an audit finding, and not a rule about vendors in general." (`vendor-disclosure-policies-as-corpus-objects.md:13-16`, 25 words).
  - Explicit numbered claims:
    - Claim 1: Intake is a policy-level list; bounty is only one channel.
    - Claim 2: Handling scope and disclosure scope are two different lists.
    - Claim 3: Severity is one indicator inside internal triage, not reporter dictate.
    - Claim 4: Publication date is an agreement, not a mechanical clock.
- **Patterns F15 should follow**:
  - First-party attribution disclaimer (naming Microsoft explicitly as the stating party per Q4).
  - Treating published vendor policies as standing self-descriptions rather than universal rules.
  - Differentiating intake channels from bounty programmes (MSVR is an intake/coordination mechanism, not a cash bounty).
- **Patterns F15 should avoid**:
  - Generalizing one vendor's policy or timeline commitments to other vendors.

### 3.3 Entry F11 (`knowledge/iso-29147-and-30111-division-of-labour.md`, S041 — JPCERT/CC)
- **Entry Shape**:
  - Structural division of labour: outward-facing communication (ISO/IEC 29147) vs. internal vulnerability handling (ISO/IEC 30111).
  - Quoted record table with exact line citations (`S041.txt:1667-1678`).
  - Falsifiable classification rules accompanied by executable command checks (`grep -c '29147:2018'` vs `'29147:2014'`).
  - Explicit `## Rejected over-generalizations`:
    > "Rejected: 'ISO/IEC 29147 is only about receiving vulnerability reports.'" (`iso-29147-and-30111-division-of-labour.md:46`, 9 words).
- **Patterns F15 should follow**:
  - Runnable machine checks (e.g. grep counts or pattern checks) verifying the entry's claims against capture files.
  - Directional classification rules (intake vs internal triage vs outbound disclosure).
- **Patterns F15 should avoid**:
  - Omission of standard/policy editions; assuming "29147 = intake only" without verifying advisory publication.

### 3.4 Summary: Concrete Requirements for F15 (`corpus/knowledge/vendor-third-party-finding-coordination.md`)
1. **Header**: Q1/Q10-compliant:
   ```markdown
   # A vendor's research programme as an intake route for other vendors' bugs
   source: S048 — https://www.microsoft.com/en-us/msrc/msvr — the three intake routes L32-34 and three roles L35
   verified-at: 2026-10-25
   recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
   ground: F15 — vendor research programme as an intake route for other vendors' bugs
   ```
2. **Attribution Block**: Stated explicitly as Microsoft's first-party description of MSVR, not a general law of vulnerability disclosure (Q4).
3. **Evidence Table**: Verbatim quotes <= 25 words matching exact lines from `corpus/source-snapshots/round-31/S048.txt`:
   - Route 1 (L32): Internal Microsoft engineers finding vulnerabilities in third-party software.
   - Route 2 (L33): External reports to MSRC where reporter believes finding affects Microsoft and third party.
   - Route 3 (L34): Internal research projects.
   - Three Roles (L35): Affected vendor, finder in third-party products, and coordinator of multi-vendor vulnerabilities.
4. **Falsifiable Local Check**: Synthetic review worksheet testing classification across the 3 routes and 3 roles, rejecting any review that collapses MSVR into an affected-vendor bug bounty.
5. **Rejected Over-generalizations**:
   - Rejected: "MSVR is a bug bounty payout programme." (MSVR is an intake, research, and coordination mechanism; financial bounties are governed by separate MSRC bounty rules).
   - Rejected: "Reporting a third-party finding to MSVR absolves the finder of multi-vendor coordination duties." (CVD requires active coordination; FIRST v1.1 and MSVR both treat coordination as negotiated).
6. **Limits & Capture Quirks**:
   - Dynamic Trace ID on line 2 (sha256 of capture is pinned to committed bytes, not refetchable live).
   - Curly apostrophe on line 30 vs ASCII apostrophe on line 35.
   - Line 33 source typo preserved verbatim: `"third-party product of affects both"` (sic).

---

## 4. UFO-FSD Connector Move: Synthesis Across Round Proposals

### 4.1 Declared Axes of the Round
- **`depth:verifiability`** (score 4, held; C1 establishes one-limb mutation ledger `limb-ledger.json` + counter `limb-mutation-check.py` for 13 recheck-family limbs).
- **`coverage`** (score 7, held; C2 establishes Frontier F15 admission 14 -> 15, S048 registry row 47 -> 48, knowledge entry, snapshot manifest).
- **Non-claim items**: `score-gap.py` (`considerthese/2026-10-25.md` proposal 2), assimilation collision guard, mistake M31-1 erratum.

### 4.2 Evidence
1. **Unpinned Network Recheck in Staged Entry**:
   The staged campaign file `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` specified:
   `recheck: 180d — curl -sSL https://www.microsoft.com/en-us/msrc/msvr ...`
   This is non-hermetic, fails Q7/Q10, and prevents automated verifiability gating.
2. **Local Quirk Discrimination in S048**:
   `ScoutMSVR.md` proved that line 2 carries a non-deterministic `This is the Trace Id: <32 hex>` header, while lines 31-35 contain exactly-once text for 3 distinct intake routes and 3 distinct operational roles.
3. **Fleet-Level Jurisdiction Alignment**:
   `kake-shokunin` (`corpus/README.md:457-460`) explicitly refused vulnerability handling. No other sibling touches vulnerability coordination.

### 4.3 Proposed Move (Bounded Synthesis)
**Move**: Bind F15's admission directly into the round's hermetic verifiability surface by:
1. Anchoring S048's manifest assertions in `corpus/source-snapshots/round-31/manifest.json` to the exactly-once 3-route and 3-role strings, ensuring `source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048` executes 100% offline and hermetically.
2. Formulating F15's falsifiable local check around the tri-role matrix (Affected Vendor vs. Finder vs. Multi-Vendor Coordinator), directly expanding F06's worksheet check so that synthetic review worksheets must distinguish vendor-as-finder from vendor-as-recipient.
3. Formally referencing `kake-shokunin`'s explicit refusal (`kake-shokunin/corpus/README.md:457-460`) within kasegi's PROVINCE.md / receipts as mutual corroboration of exclusive domain ownership across the fleet.

### 4.4 Second-Order Effects Across Surfaces
- **Runtime surface**: Zero network calls during CI or verification. `recheck-audit.py`, `source-recheck.py`, and `frontier-recheck-count.py` execute cleanly offline.
- **Contract surface**: Satisfies QUALITY Q1, Q3, Q4, Q5, Q7, Q9, Q10 and RECORD R6, R8, R12, R13.
- **Substrate surface**: Single-writer ownership preserved; fleet root untouched; zero git mutations.
- **Verification surface**: `score-gap.py` (proposal 2) directly measures the increased coverage and verified source chain without scoring regressions.

### 4.5 Risks & Mitigations
- **Risk**: A reviewer quotes line 2 of S048 or attempts a live refetch, hitting trace ID drift.
  - **Mitigation**: Disclose the Trace ID quirk in `corpus/knowledge/vendor-third-party-finding-coordination.md` § Limits; manifest binds the committed snapshot bytes via sha256.
- **Risk**: ASCII vs. curly apostrophe mismatch in quote verification.
  - **Mitigation**: Quote selection strictly targets ASCII apostrophe lines (L35) or apostrophe-free strings (L31, L32, L33, L34) as verified in `ScoutMSVR.md`.

### 4.6 Verification
1. `grep -rn -i "msvr" /home/vgpnk/Projects/shokunin/{chousa,kengaku,kake,kagi,kumitate,kotoba}-shokunin/corpus/` returns 0 hits.
2. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048` prints `verified=1 failures=0` and exits 0.
3. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py` prints `entries=18 pass=18` and exits 0.
4. `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` prints `15`.
