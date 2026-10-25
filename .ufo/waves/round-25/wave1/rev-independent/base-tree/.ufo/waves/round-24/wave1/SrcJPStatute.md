# SrcJPStatute — re-grounding `statutory-authorization-in-three-traditions.md`

Seat: read-only scout. Access date **2026-10-25** (UTC). Lane base d0a3f6a4.
Entry under test: `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/statutory-authorization-in-three-traditions.md`
Bodies held in `/tmp/src-jp-statute/`. No installs performed this seat.

---

## 1. Captures

Every hash below is **stable across two independent fetches** (`egov.xml`/`egov2.xml`, `soumu.html`/`soumu2.html`, `npa.pdf`/`npa2.pdf` — identical sha256 pairs), so the captures are deterministic and safe to pin.

| ID | URL | HTTP | Bytes | SHA-256 |
|---|---|---|---|---|
| S039 | `https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` | 200 | 36058 | `baac5ef21a89ed131bd1d5289487292451da10d8dd6e62735e6311987b5a3992` |
| S040 | `https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` | 200 | 85874 | `dd5e49512f46ae9a858aefdae16d22f4767b696fbd860a96a717250716261ce4` |
| S041 | `https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` | 200 | 477938 | `1f8ac1fb4e7f01e99c90c4f80ad9373c4dad1e7bb24fa0415bb259b3e00508a6` |

Observed metadata:
- S040 `Last-Modified: Fri, 16 Oct 2026 01:20:47 GMT`, footer `© 2009 Ministry of Internal Affairs and Communications`.
- S041 `Last-Modified: Wed, 12 Jul 2023 18:58:26 GMT`, PDF v1.4, 17 pages.
- S039 XML: `LawTitle=不正アクセス行為の禁止等に関する法律`, `LawNum=平成十一年法律第百二十八号`.

Commands: `curl -sSL -A 'Mozilla/5.0 (X11; Linux x86_64)' -o <file> -w '%{http_code}' <url>` then `stat -c%s`, `sha256sum`.

---

## 2. The three required answers

### (i) Does the e-Gov XML carry 三年以下の拘禁刑 or 三年以下の懲役 in 第十一条?

**三年以下の拘禁刑.** Verbatim, `<Article Num="11">`, `<ArticleTitle>第十一条</ArticleTitle>`, single `<Sentence Num="1">`:

```
第三条の規定に違反した者は、三年以下の拘禁刑又は百万円以下の罰金に処する。
```

File-wide census in S039: `拘禁刑` = **2** (`第十一条` 三年以下, `第十二条` 一年以下), `懲役` = **0**. `Article Num="11"` occurs exactly once.

The entry's quoted penalty string is **exactly correct** against S039.

Independent direction check — the Penal Code itself (`https://laws.e-gov.go.jp/api/1/lawdata/140AC0000000045`, HTTP 200, 416317 bytes, sha256 `f8108dbd7d4516fce2583db8ab5392916dfcee9d782110106cd750b167ea6081`, `LawTitle=刑法`, `LawNum=明治四十年法律第四十五号`): `拘禁刑` = 256, `懲役` = 6. So 拘禁刑 is the current statutory form and 懲役 is the superseded one. The e-Gov consolidated text is the current form.

### (ii) Does the MIC page differ, and in which direction?

**Yes — backward (pre-拘禁刑).** S040 `第十一条` reads:

```
第三条の規定に違反した者は、三年以下の懲役又は百万円以下の罰金に処する。
```

`懲役` = 2, `拘禁刑` = 0 on S040. Its `第十二条` likewise reads `一年以下の懲役` where S039 reads `一年以下の拘禁刑` — so the staleness is page-wide, not a single dropped word.

**The entry understates this: it names only S040.** S041 differs in the *same* direction. NPA §3 preamble reads `３年以下の懲役又は100万円以下の罰金に処せられることとなっています(第11条)。` (`懲役` = 2, `拘禁刑` = 0 on S041). Two of the three primaries are stale, not one, and the entry's tier-B reasoning never accounts for S041's penalty even though it cites S041 §3.

On the entry's *explanation* ("the MIC page predates the 刑法 amendment"): supported in substance by the `© 2009` footer, but note `Last-Modified: 2026-10-16` — the page is served freshly today while carrying 2009-era text. "Predates" describes the **text block**, not the file. S041's `Last-Modified: 2023-07-12` genuinely predates the amendment.

### (iii) Can each of the three be quoted exactly-once under whitespace-collapsing normalization?

Normalization used = the lane instrument's declared rule, `corpus/instruments/source-recheck.py::normalize` = `" ".join(MARKUP_RE.sub("", text).split())` (collapses all Unicode whitespace incl. U+3000; drops only `<u>`/`</u>`). For S039 I additionally ran the tag-stripped variant the ticket names (tag boundary → whitespace, then collapse). Counts are multiplicity in the normalized capture.

**S039 — YES, all loci exactly-once.**

| string | raw XML | tag-stripped+normalized |
|---|---|---|
| `第三条の規定に違反した者は、三年以下の拘禁刑又は百万円以下の罰金に処する。` (37 ch) | 1 | 1 |
| `この法律において「不正アクセス行為」とは、次の各号のいずれかに該当する行為をいう。` (41 ch) | 1 | 1 |
| carve-out 号一 (67 ch) | 1 | 1 |
| carve-out 号二 incl. `次号において同じ。` (61 ch) | 1 | 1 |
| 第二条第一項 アクセス管理者 定義 (117 ch) | 1 | 1 |

Notably the statutory strings are **contiguous in the raw XML too** — no tag-stripping needed for the lane instrument's raw-substring branch.

**S040 — PARTIAL.**

| string | raw HTML | normalized |
|---|---|---|
| `第三条の規定に違反した者は、三年以下の懲役又は百万円以下の罰金に処する。` | 1 | 1 |
| carve-out 号一 (identical bytes to S039's) | 1 | 1 |
| `この法律において「不正アクセス行為」とは、…` canonical form | **0** | **0** (tag-stripped: only `「 不正アクセス 行為」` with injected spaces) |
| 第二条第一項 アクセス管理者 定義 | **absent** | absent |

S040 renders 不正アクセス as a hyperlink, so canonical quoting of the 第二条第四項 lead **fails in every branch**; the page also prints `第二条 1～3略`, i.e. **第一項–第三項 are literally omitted**. S040 therefore cannot ground アクセス管理者 at all.

**S041 — NO for any long sentence; YES only for short fragments.**

The PDF hard-wraps text, and each wrap becomes a space under normalization, inserting a space mid-word inside the quote. Verified identical across `pdftotext` default, `-raw`, `-layout` (3/3 modes, so this is intrinsic to the PDF, not an extraction artifact):

| string | default | -raw | -layout |
|---|---|---|---|
| penalty sentence | 0 | 0 | 0 |
| carve-out restatement | 0 | 0 | 0 |
| security-check rationale sentence (103 ch) | 0 | 0 | 0 |
| `コンピュータのセキュリティ・チェックを実施する場合` (25 ch) | **1** | 1 | 1 |
| `禁止の対象から除外しています。` (15 ch) | 1 | 1 | 1 |

Actual wrapping, e.g. `…３年以下の懲役又は100万円以下の⏎罰金に…`, `…識別符号を付与⏎されている利用権者…`, `…や、⏎会社の同僚…`. The canonical strings only match if the injected space is preserved verbatim (as-wrapped variants each = 1).

**Instrument-level blocker for S041:** `npa.pdf` is **not UTF-8-decodable** (`UnicodeDecodeError: byte 0xe2 in position 10`), and `source-recheck.py` calls `source_bytes.decode("utf-8")` → it would emit `S041:source UNAVAILABLE reason=not-utf8`, exit 2. S041 cannot become a committed capture as a PDF; it needs a declared text extraction, and the extraction method decides quotability (see table above).

---

## 3. Verbatim Japanese strings with markers

### 第二条第四項 (definition, three 号)

Lead, `<Sentence Num="1">` under `<Paragraph Num="4">`:
```
この法律において「不正アクセス行為」とは、次の各号のいずれかに該当する行為をいう。
```

**第一号** — 他人の識別符号を悪用する limb:
```
アクセス制御機能を有する特定電子計算機に電気通信回線を通じて当該アクセス制御機能に係る他人の識別符号を入力して当該特定電子計算機を作動させ、当該アクセス制御機能により制限されている特定利用をし得る状態にさせる行為（当該アクセス制御機能を付加したアクセス管理者がするもの及び当該アクセス管理者又は当該識別符号に係る利用権者の承諾を得てするものを除く。）
```

**第二号** — vulnerability/information limb:
```
アクセス制御機能を有する特定電子計算機に電気通信回線を通じて当該アクセス制御機能による特定利用の制限を免れることができる情報（識別符号であるものを除く。）又は指令を入力して当該特定電子計算機を作動させ、その制限されている特定利用をし得る状態にさせる行為（当該アクセス制御機能を付加したアクセス管理者がするもの及び当該アクセス管理者の承諾を得てするものを除く。次号において同じ。）
```
(item bodies measure 176 / 190 / 137 characters; the 号 label `一`/`二`/`三` lives in a separate `ItemTitle` element and is not part of the quoted run)

**第三号** — no parenthetical of its own; inherits 第二号's carve-out via `次号において同じ。`:
```
電気通信回線を介して接続された他の特定電子計算機が有するアクセス制御機能によりその特定利用を制限されている特定電子計算機に電気通信回線を通じてその制限を免れることができる情報又は指令を入力して当該特定電子計算機を作動させ、その制限されている特定利用をし得る状態にさせる行為
```

### 第二条第一項 (アクセス管理者 — the definition the entry depends on, **not** in its `source:` pointer)
```
この法律において「アクセス管理者」とは、電気通信回線に接続している電子計算機（以下「特定電子計算機」という。）の利用（当該電気通信回線を通じて行うものに限る。以下「特定利用」という。）につき当該特定電子計算機の動作を管理する者をいう。
```

### 第十一条 (罰則)
```
第三条の規定に違反した者は、三年以下の拘禁刑又は百万円以下の罰金に処する。
```

### S041 NPA commentary — the legitimate-security-check sentence (entry's central NPA claim)
At `§3 不正アクセス行為の禁止、処罰(第２条第４項、第３条、第11条関係)`, subsection `(1) 他人の識別符号を悪用する行為(第２条第４項第１号)`:
```
なお、アクセス管理者が行う場合及びアクセス管理者又は入力する識別符号を付与されている利用権者の承諾を得て行う場合は禁止の対象から除外しています。これは、正当な利用形態(例えば、コンピュータのセキュリティ・チェックを実施する場合や、会社の同僚に対して自分の代わりに電子メールが着信していないかどうかのチェックを依頼する場合など。)が考えられるためです。
```

**The entry's NPA claim is substantively TRUE and located at the cited §3(1).** Caveat: the NPA gives *two* legitimate uses (security check, and asking a colleague to check one's mail); the entry names only the first. The NPA's rationale is phrased as `正当な利用形態…が考えられるためです` ("legitimate uses are contemplated"), not an explicit "not criminalised".

**Do not pin the block above verbatim.** It is the canonical rendering for reading; its normalized count in S041 is **0** (hard wraps inject `付与⏎され`, `場合や、⏎会社`). Pin A3 in §5 instead. Same applies to the 第一号 carve-out restatement earlier in this subsection: canonical 0, as-wrapped 1.

---

## 4. Falsifiers against the entry (ordered by severity)

**F1 — carve-out over-attribution (factual error).** Entry: *"Both limbs exclude conduct done by the access manager, or with the consent of the access manager or of the user to whom the identification symbol was granted."* Only **第一号** mentions 利用権者 consent. **第二号**'s parenthetical is `当該アクセス管理者の承諾を得てするものを除く。` — access manager only. Verified at item level: `ITEM 1 parenthetical=True`, `ITEM 2 parenthetical=True`, `ITEM 3 parenthetical=False`.

**F2 — omitted extension to 第三号 (material omission).** 第二号's carve-out ends `次号において同じ。`, so **第三号 inherits it** — the very limb covering a circumventing input against a computer restricted by *another* computer's access-control function. The entry's mental model (carve-out on "第一号 and 第二号" only) leaves limb three reading as a no-consent offence, which is wrong.

**F3 — limb (iii) mis-described.** Entry: *"(iii) the same, where the information or instruction is input over a telecommunications line."* The actual 第三号 is about the **restricting access-control function residing on a different connected computer**, not "the same over a line". The entry's own `recheck:` note also calls 第二条第四項 a "three-limb" test whose limbs are (i)/(ii)/(iii) — fine — but (iii) is not a restatement of (ii).

**F4 — the vulnerability limb is two 号, not one.** Entry: *"Limb (ii) is the vulnerability-exploitation limb — the one a bounty researcher occupies."* S041: `コンピュータプログラムの不備を衝く(第２条第４項第２号、第３号)`. The NPA groups 第二号 **and** 第三号 as the flaw-exploiting limb. An entry that assigns the researcher's act to (ii) alone under-describes the exposure.

**F5 — アクセス管理者 definition is 第二条第一項, uncited.** The entry's `source:` line says `第二条 (定義) 第四項` only, yet its "access manager is the scope owner" section rests on 第一項 (117 ch, exactly-once quotable). S040 cannot supply it (`1～3略`). Coverage gap in the pointer, not in the fact.

**F6 — two stale primaries, one named.** The entry frames 懲役 vs 拘禁刑 as an S039-vs-S040 issue. S041 is stale in the same direction (F-table in §2(ii)). The tier-B judgement is right but incompletely argued.

**Rebutted (entry claim that SURVIVES).** The NPA legitimate-security-check rationale exists, verbatim and at the cited subsection (§3 above). The entry's central bridging claim between statute and bounty practice is **upheld**; F1–F4 attack its carve-out mechanics, not its thesis.

---

## 5. Three assertion candidates (5–25 words / Japanese counted in characters)

Each is exactly-once in its own capture under the lane's `normalize`; counts measured, not estimated.

| # | Assertion (verbatim quotable unit) | Source | Chars | Normalized count | Raw-file match |
|---|---|---|---|---|---|
| A1 | `三年以下の拘禁刑又は百万円以下の罰金` | S039 | **18** | 1 | yes (`in` raw XML) |
| A2 | `三年以下の懲役又は百万円以下の罰金` | S040 | **17** | 1 | yes (`in` raw HTML) |
| A3 | `コンピュータのセキュリティ・チェックを実施する場合` | S041 | **25** | 1 | n/a — PDF, text-extraction only |

A1/A2 are the clean falsifier pair: the two strings are mutually exclusive per capture (A1 count in S040 = 0; A2 count in S039 = 0), so pinning both makes the 拘禁刑-with-justification claim self-checking across two sources. A3 is the longest S041 fragment that survives all three pdftotext modes; it carries the entry's central NPA claim and sits at the 25-character ceiling.

---

## 6. Instrument findings that bind the above (verifiability axis)

1. **`source-recheck.py` has no multiplicity check.** `check_source` uses `assertion["quote"] in source_text` (and the `normalize(...) in normalize(...)` fallback) — pure containment. Probe: `不正アクセス` occurs **25** times in `egov.xml`; `'不正アクセス' in text` returns `True`. The instrument cannot distinguish exactly-once from 25-times, so "exactly-once quotability" is currently **unenforced by tooling** and rests on manual counts like §2(iii). Path: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py`.
2. **PDF captures are structurally inadmissible.** Same file, `source_bytes.decode("utf-8")` → S041 exits 2 `UNAVAILABLE reason=not-utf8`. Any S041 capture must be a declared text extraction, and the extraction mode changes whether a long sentence is quotable (§2(iii)).
3. **Cross-source string collision — wider than the carve-out.** All three 第二号/第三号 item bodies *and* the 第一号 carve-out are **byte-identical** between S039 and S040 (measured: each of the three 号 bodies = 1 in egov and 1 in soumu). Only the 第二条第四項 **lead sentence** differentiates the two captures (S040's is link-spaced). So a manifest asserting any 号 body proves the *norm text*, not *which source* was read; only the lead sentence (S039-only in canonical form) and the penalty string (mutually exclusive: 拘禁刑 vs 懲役) actually discriminate source identity.
4. **The entry's `recheck:` field is prose, not a command** (`recheck: 730d — \`curl …\` then confirm … (ran 2026-10-23)`). The frozen C1 counter A greps `^recheck: ` and runs the remainder via `bash -c`; this line would execute `730d — \`curl …\``, not a check. Routed to C1's owner, recorded here because it is the same entry.

---

## 7. UNVERIFIED / open

- **UNVERIFIED:** the entry's claim that MIC "predates the 刑法 amendment" as a *cause*. Evidence is `© 2009` footer (supports) vs `Last-Modified: 2026-10-16` (page re-served this month). No amendment-hash citation appears on the capture, so causation is inference. `[INFERENCE]`
- **UNVERIFIED:** the 刑法 懲役→拘禁刑 amendment's own law number and commencement date. I did not open that law; I only established direction from two consolidated e-Gov records (S039 and 140AC0000000045). Do not cite a law number from this report.
- **UNVERIFIED (unchanged from entry):** the Chinese half (刑法 第285条). Out of scope for this seat; the entry's own honest-limit paragraph stands.
- **Not attempted:** any live target contact — documentation-only discipline held; only the three cited public documents plus the Penal Code API were opened.

---

## 8. Recommendation to L1 (integration owner)

Admit the entry with **F1, F2, F3, F5** corrected before pinning: the carve-out must be stated as 第一号 (manager **or** 利用権者 consent) vs 第二号 (manager consent only, `次号において同じ` → 第三号), アクセス管理者 must be re-pointed to 第二条第一項, and the penalty divergence must name both S040 and S041. F4 is a wording fix. Pin A1–A3 as the manifest's quotable units; use A1/A2 as a mutual-exclusion pair. If S041 is to be a recheckable source, capture its text extraction and record the extraction command, because the PDF fails the instrument's UTF-8 decode.
