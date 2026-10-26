# ScoutPackageThemes receipt — round 31 assimilation set (lesson Gate input)

Answering model: anthropic/claude-sonnet-5-5. Read-only throughout: package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and the lane were only read; nothing copied, no package tool run, no network fetch (nothing in my item names a URL). Written file: this receipt only.

## Verdict (one line each)

| staged entry | recommendation |
|---|---|
| `vendor-third-party-finding-coordination-2026-10-23.md` | **ADMIT** — as the F15 rewrite (lane row S048, ground F15), not as staged bytes |
| `program-scope-rules-and-asset-boundaries.md` | REJECT (re-refused; HackerOne half already lane-held) |
| `claim-packaging-and-report-quality.md` | REJECT (re-refused) |
| `cn-crowdsourced-testing-roles-and-conduct.md` | REJECT (nearest to a flip) |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | REJECT (furthest from a flip) |

Gate requirement (>=1 admit, >=1 reject): met, 1 admit + 4 reject. Exactly one ADMIT.

## Evidence base (commands run)

Package digests (`sha256sum`, run 2026-10-25):
```
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  SOURCES.append.md   (same digest ScoutAssimPackage measured in round 30)
8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b  MERGE-REPORT.json
48e9de4ec971f39e30d0ec4ba9f266ddeb5ac183ec172667b42787dc76c995dc  knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md
120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8  knowledge/corpus/knowledge/program-scope-rules-and-asset-boundaries.md
6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc  knowledge/corpus/knowledge/claim-packaging-and-report-quality.md
a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813  knowledge/corpus/knowledge/cn-crowdsourced-testing-roles-and-conduct.md
6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f  knowledge/corpus/knowledge/chinese-crowd-testing-national-standard-2026-10-23.md
```

MERGE-REPORT.json flags, all five entries: `collides_with_existing: False`, `duplicate_target: False`; `existing_rows 30`, `first_id S031`, `renumbered []`. The package assumed a 30-row lane registry; the lane holds 47 (S001-S047). **Every staged S031-S047 id therefore collides in the id-space with a different lane row** (e.g. staged S031 = HackerOne policy_versions; lane S031 = CVE CNA Rules v4.2.6; staged S034 = CNVD helpList; lane S034 = 総務省 page). Adoption must map by document/URL, never by id. Staged S077-S082 do not collide in id (lane tops at S047, next free S048), but they are not the lane's rows either.

### URL join: staged `SOURCES.append.md` rows -> lane `corpus/SOURCES.md` (python regex join on the URL after ` — `, run in lane root)
```
S031 https://hackerone.com/security/policy_versions -> ['S043']
S034 https://zc.cnvd.org.cn/news/helpList -> None
S035 https://security.360.cn/Reward/rules -> None
S036 https://security.bilibili.com/static/docs/BILISRC_V1.7.pdf -> None
S077 https://std.sacinfo.org.cn/gnoc/queryInfo?id=E8261DDA41842E54E073557BFF2F9E7B -> None
S078 https://www.sac.gov.cn/xw/bzhdt/art/2024/art_f1892c53ae3e4317b5e9aea08b6a72fc.html -> None
S079 https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=57CAF3B46207A7D43649E9BE15AEA0C0 -> None
S080 https://www.microsoft.com/en-us/msrc/msvr -> None
S081 https://zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100 -> None
S082 https://std.samr.gov.cn/gb/search/gbDetailed?id=D0FE299A5DFDD818E05397BE0A0AFD6C -> None
```
(Regex parsed 68 of the 94 staged rows with the ` — URL |` shape; 18 of those 68 URLs are already lane rows. Only the ten rows above matter to this set. Lane S043's `used-by` is `corpus/knowledge/program-severity-ladders-and-reward-scales.md` = F13.)

Recheck-line parse (each staged `recheck:` payload piped to `bash -n`): **all five fail** — `syntax error near unexpected token '('` (vendor, claim-packaging, cn-crowd, national-standard) and `unexpected EOF while looking for matching "'"` (program-scope). They are prose (`180d — \`curl …\``), no `cd <lane> &&` prefix, no captured-source comparison. H1 count (`grep -c '^# '`): vendor 1, program-scope 1, claim-packaging 1, **cn-crowd 0**, national-standard 1.

Lane ground (corpus/README.md Frontier table, read 2026-10-25): F01-F14 admitted (14/14); F06 `multiparty-vulnerability-coordination.md` S018; F09 authorisation outside the platform (ROE + statute) S032-S035; F10 vendor policies as corpus objects S036-S040; F11 ISO 29147/30111 S041; F12 JP state workflow; F13 severity ladders S043-S045; F14 JP severity vocabulary S046/S047/S041. Staged `ground:` labels (F09, F11, F20, F24) are the package's own F-space and **collide in label with lane F09/F11 (different topics)**.

## Per-entry findings

### 1. vendor-third-party-finding-coordination-2026-10-23.md — ADMIT (rewritten, F15 / S048)

(a) PROVINCE: in scope. PROVINCE.md line 3 domain "bounty & security research — scopes … program rules, claim packages"; Frontier paragraph indexes general practice incl. F10 vendor-side disclosure policies and F11 coordination standards. Needs a PROVINCE Frontier append for F15 (owner ScribeProvince) — PROVINCE currently names F01-F11 only.

(b) Coverage: **partly distinct, not a restatement.** Lane holds F06 (S018 FIRST multi-party: roles of finder/vendor/coordinator, generic) and F10 crosswalk (Cisco S040 "Incidents that may impact other vendors", names CERT/CC, CERT-FI, JP-CERT, NPSA at L187-L190 — `vendor-disclosure-policy-commitments-crosswalk.md:26`). Sweep `grep -rniE 'MSRC|MSVR|Microsoft|third-party product|finder-side'` over multiparty / vendor-disclosure-* / coordinated-disclosure-timelines hits only: multiparty L8/L25/L28 ("finder" as FIRST's generic role), vendor-disclosure-policies-as-corpus-objects L33 (Cybozu's *own use* of third-party products). **No lane entry holds a vendor that runs an intake programme for other vendors' products; no MSRC/MSVR/Microsoft hit anywhere.** The reviewer's required "not a restatement of F06/F10" sweep passes on that command.

(c) Q-criteria failed as staged (flip = the rewrite the C2 seats are already doing):
- Q1: `source:` names S080 (a staged id; lane id must be S048), `ground: F20` is not a lane frontier item (must be F15), `recheck:` is prose-plus-curl and not a `cd`-prefixed command (also Q7, Q10: no pinned capture, no corrupted-source control, `bash -n` fails).
- Q3: no verbatim quote with a located line at all (only the paragraph-opener phrase is mentioned, as a paraphrase anchor). Flip: quote from the lane capture S048.txt. Peer `ScoutMSVR.md` already located exactly-once quotes, ≤25 words (counts 1 each): L31 "MSVR learns about vulnerabilities in third-party products in three ways"; L32 route 1; L33 "These issues are coordinated by MSVR."; L34 route 3 "Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices."; L35 the three roles ("as a finder of new vulnerabilities in third-party products and services", "as a coordinator of vulnerabilities that affect multiple vendors") and "This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach." Quirks the capture must handle (from that receipt): L2 nondeterministic trace id (never quote), L30 curly apostrophe vs L35 ASCII, L33 source typo "of" for "or" (quote verbatim).
- Q4 (attribution/over-generalization, two staged sentences exceed the page): (i) "For third-party findings the reported issue is coordinated by MSVR" generalizes route 2 only (L33 "These issues are coordinated by MSVR" sits on the external-reports route); route 1 (L32) is "reported to the MSVR team, which then works with the affected vendor" and route 3 (L34) is "reported to the affected vendor". (ii) "the *finder* also has a coordinated-disclosure obligation" — an obligation is not stated on the page; the page states Microsoft's own roles and its CVD *approach*. Flip: drop "obligation", say "MSVR states".  (iii) "does not report the coordination agreements themselves, which are not published" — an absence claim the page cannot support; replace with the capture's own limit: page-level evidence only, no timelines or contacts (L35 is the only coordination statement).
- Q5: no falsifiable rule and no "Rejected" over-generalization section. Flip: add e.g. rule "every claim about MSVR intake carries the stating route line (L32/L33/L34) and names Microsoft"; rejected: "all third-party findings are coordinated by MSVR" (only route 2 says so).
- Q2/Q9: S080 tier A is right, but it must be re-opened in the admitting round (staged `opened` 2026-10-23) and captured under the Q8 normalization (markup-whitespace) with the Q9 stem==id check and occurrence counts (all quotes occur once; no anchors needed).

(d) Source rows: exactly one — staged S080 (Microsoft MSVR, https://www.microsoft.com/en-us/msrc/msvr, docs, tier A, `recheck 180d`). **Not a lane row by URL (join: None).** Assimilation is by DOCUMENT: staged S080 -> new lane **S048** (registry 47 -> 48); no existing lane row reused. Rewrite its anchor against the round-31 capture lines 31-35, set `opened` to the capture date, and keep `used-by corpus/knowledge/vendor-third-party-finding-coordination.md` (staged path carries a `-2026-10-23` suffix; lane naming for F14/F13 entries drops the date suffix, matching the C2 predicate path).

R8 note for the lesson: a staged anchor that is rewritten is logged as old->new, as round 30 did for S046/S047.

### 2. program-scope-rules-and-asset-boundaries.md — REJECT (standing from round 30)

(a) PROVINCE: in scope (program rules, scopes).
(b) Coverage: **half held.** The HackerOne half (third-party assets out of scope) is already lane-held in F13: `program-severity-ladders-and-reward-scales.md` source line 3 (S043 capture, "In Scope L31, Out of Scope L40") and L16 quoting "Issues affecting assets under HackerOne's c…". Safe-harbor-vs-scope separation is F03 (S006). Not held: the CNVD 众测 and 360SRC scope statements. The staged "ground: F09 (new frontier item; extends F03)" collides with lane F09 (authorisation outside the platform) and binds no lane frontier.
(c) Fails as staged: **Q1** (three `source:` lines carrying staged ids S031/S034/S035; ground label not a lane F-id; recheck prose, `bash -n` "unexpected EOF while looking for matching `''"), **Q2** (S034/S035 not lane rows; cited tier-A rows not opened in the lane's admitting round), **Q3** (no located quote ≤25 words; only paraphrase and three quote-marked fragments with no line/page), **Q7/Q10** (non-executable recheck, no cwd prefix, no control), **Q5** (no rejected over-generalization section; "one invariant … every platform's scope list" generalizes three platforms' rules into a universal — Q4). Flip: register+capture CNVD helpList (S034 URL) and 360SRC rules (S035 URL) as new lane rows, reuse lane S043 for HackerOne, quote with locations, one `cd … && source-recheck.py` line, attribute each claim to its platform, name a lane frontier item (likely a new F16+ "Chinese program scope/packaging rules" or fold into F13's CN half), drop the universal.
(d) Rows: staged S031 -> **already lane S043 by URL** (same document; id differs); staged S034, S035 -> no lane row. (S036 is cited only in entry 3.) Note S034 is cited here for scope, in entry 3 for report quality, and in the already-refused round-30 CN scoring material (lane F13 L64: "CNVD 众测 and BILISRC ladders … not adopted this round").

### 3. claim-packaging-and-report-quality.md — REJECT (standing from round 30)

(a) PROVINCE: **core** (claim packages are line-3 domain); the topic belongs, the entry as staged does not.
(b) Coverage: lane holds Western packaging as lost-tree documents (`claim-package-contract.md`, `claim-gates.md`, `vdp-disclosure-packages.md`, `claim-anatomy-sample.md`) — corpus-attested, source roots absent (PROVINCE Core). Lane holds **no** CNVD/360SRC/BILISRC/Japanese-flow packaging rules by any registered row (grep `众测|CNVD|360SRC|BILISRC` over `corpus/knowledge`: only the F13 "not adopted" note). Staged `ground: F11 (new frontier item)` collides with lane F11 (ISO 29147/30111).
(c) Fails: **Q1** (ground; recheck is `curl … -o bili.pdf && pdftotext …` prose-prefixed, `bash -n` fails), **Q2** (S034/S035/S036 unregistered), **Q3** (three Chinese phrases are quote-marked but carry no page/line; "降级场景" etc. are paraphrased without a located quote), **Q4** ("stricter than most Western platforms' published rules suggest", "standard practice in the Eastern programs" — a regional universal built from three first-party documents), **Q5** (no rejected over-generalization — the closing paragraph asserts the generalization), **Q7/Q10**. Its own claim "The lane's claim-package-contract … describe a lost local tree" is plausible but unsourced here. Flip: register+capture S034/S035/S036 URLs; quote each downgrade/proof rule with PDF page/line; state per-platform positions; delete the "Eastern programs" universal; add recheck and a lane frontier ground.
(d) Rows: staged S034, S035, S036 (BILISRC_V1.7.pdf) -> **none is a lane row by URL**.

### 4. cn-crowdsourced-testing-roles-and-conduct.md — REJECT (nearest to a flip)

(a) PROVINCE: in scope (a platform's tester conduct code is a program rule; authorised-testing boundary is F09-adjacent). Chinese material is already in-province (F12/F14 are Japanese; none Chinese yet).
(b) Coverage: lane holds no Chinese crowd-testing material and no Chinese authorised-tester conduct material (grep above: none). Lane holds `authorization-safe-harbor-and-scope.md` (F03) which the staged entry extends, and F09 ROE/statute. So the ground is genuinely new.
(c) Fails: **Q1** (file has **no H1 title** — `grep -c '^# '` = 0; header lines begin the file; `ground: round-6 ledger item 2` is not a lane frontier; recheck `90d — re-open both URLs…` prose, `bash -n` syntax error), **Q2** (S081/S082 not lane rows, staged `opened 2026-10-24` is not a lane admitting-round open; S082 is the *project record* — drafting stage — and the entry's own Limits say so, so "GB/T 43741-2024 binds all four" rests on a drafting-stage scope sentence, a Q4 attribution problem), **Q3** partially met (4 located Chinese quotes with section/item but no revision/page, and not checked ≤25 words/exactly-once against a lane capture), **Q7/Q10** (no captured-source comparison, no control, non-executable recheck). Q5 present (a "Rejected" paragraph) and Q6 fine. Flip: add H1, register+capture S081 and S082 (new lane rows S049+), pin exact quotes under Q8/Q9 normalization, one `cd … &&` recheck line plus a corrupted-source control, re-ground to a named lane frontier item, label S082 as drafting-stage in the claim sentence.
(d) Rows: staged S081, S082 -> neither is a lane row by URL. Overlap note: S082 is the project record of the same standard whose catalogue records are staged S077-S079 (entry 5) — one lane entry covering the standard should cite S082 + whatever of S077-S079 is captured, not two entries.

### 5. chinese-crowd-testing-national-standard-2026-10-23.md — REJECT (furthest from a flip)

(a) PROVINCE: marginal — catalogue metadata (identity, status, CCS/ICS codes, promulgation dates) of a recommended national standard, not a program rule, scope or claim package; arguably adjacent. Not out of scope, but low yield per the domain.
(b) Coverage: no lane row/entry holds GB/T 43741 or Chinese standards infrastructure for 众测 (lane holds no Chinese material beyond the F13 "not adopted" note). Content is new but thin.
(c) Fails: **Q1** (`ground: F24 (new frontier item …)` not a lane F-id; recheck prose, `bash -n` syntax error), **Q2** (S077/S078/S079 unregistered; their `opened` is the package round, not the lane's), **Q3** (**zero** quote-marked strings: `grep -c '"'` = 0; the 描述了…角色以及职责、服务流程、安全风险、服务要求 sentence from S078 is paraphrased, not quoted with a location), **Q5** (no falsifiable rule, no rejected over-generalization — the entry's own "honest limit" says requirements were never read; "A curator should now read the platform's rules as an implementation of, or a peer to, a national standard" is an inference not a claim a reader can check), **Q7/Q10**. The entry therefore asserts a reframing it cannot ground (the standard's text was unreadable; scope read only in a commercial restatement). Flip: register/capture S077-S079, quote the S078 sentence with location, state identity/status/date facts as catalogue facts only, add a falsifiable rule (e.g. "the standard's status/effective date is read from S079's 标准信息表 row, not from a platform page") and a rejected generalization ("the standard transfers consent to the vendor" is already in entry 4), and merge with entry 4 into one lane entry rather than two.
(d) Rows: staged S077, S078, S079 -> none is a lane row by URL.

## Ranking for the Gate (not an instruction to the L1)

1. ADMIT now: entry 1 (single new row S048; rewrite as C2 already specifies).
2. Reject with flip, ordered by distance: 4 (two rows, H1, recheck, ground) < 2 (two new rows + HackerOne reuse S043 + ground) < 3 (three rows incl. a PDF, plus the universal to delete) < 5 (three rows + no quote + unsupportable reframing).
3. Standing note: staged ids collide with lane ids from S031 up; the lesson Gate should state the mapping S080->S048 and that rows S077-S079/S081/S082 and staged S034-S036 stay un-mapped (no lane id assigned) this round. No Q/R bar relaxed; no package file copied.

## Limits of this scout

- No fetch, so entry 1's staged paraphrases were checked against the peer's capture notes (`ScoutMSVR.md`, S048.txt 97 lines, sha256 78dbb989f257db1f21dd6c8c5b67d20341d60bc8f8e71f52a9472b42259828f4 per that receipt — whose own caveat is that line 2 makes the sha non-reproducible), not against bytes I fetched. The lane's committed S048 capture (ExecCapManifest) was absent at read time (`corpus/source-snapshots/round-31` did not exist); re-check the quote lines once it lands.
- The `bash -n` check ran on each `recheck:` payload text alone; it shows non-conformance to Q10, not an actual exit-code run.
- Entries 2-5 were not audited claim-by-claim against their sources (no fetch); their rejection rests on the lane-side Q failures above, which are checkable from the staged bytes and the lane registry alone.
