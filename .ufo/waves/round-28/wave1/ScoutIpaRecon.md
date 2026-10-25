# ScoutIpaRecon — round-28 wave-1 reconnaissance for the S042 capture (C2)

- seat: ScoutIpaRecon (read-only recon; leaf — no subagents, no background jobs, no VCS writes)
- lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `c9f8b115a098c65356e4b3b6048af45a37ab8395`
- owned path written: `.ufo/waves/round-28/wave1/ScoutIpaRecon.md` (this file) — **no production file was touched**
- axis judged: coverage (C2)
- status: recon complete; **two staged-anchor claims are contradicted by the live page** (§4)

---

## 1. Exact curl command, exit code and response facts

Command as dispatched (run from `/tmp`, output to a scratch file, nothing written into the lane):

```
curl -sSL -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" \
  https://www.ipa.go.jp/security/todokede/vuln/process.html \
  -o /tmp/scout-exact.html \
  -w 'http_code=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\nnum_redirects=%{num_redirects}\nsize=%{size_download}\n'
echo "curl_exit=$?"
```

Verbatim output:

```
http_code=200
final_url=https://www.ipa.go.jp/security/todokede/vuln/process.html
content_type=text/html
num_redirects=0
size=229982
curl_exit=0
```

| field | value |
|---|---|
| HTTP status | **200** |
| final URL | **identical to the requested URL — 0 redirects** (no redirect chain to record) |
| content-type | `text/html` (server sends **no `charset` parameter**; the encoding comes from the document's `<meta charset="UTF-8">`) |
| fetched bytes | 229982 |
| raw-body sha256 | `4f2f0f13f9fd6ecff7f58842c6f92b17d76787ebfe31d229b941412b24394213` (two independent fetches, byte-identical) |
| `Last-Modified` | Fri, 23 Oct 2026 02:02:26 GMT |
| `Server` / cache | Apache; `x-cache: Miss from cloudfront` via CloudFront (ATL58-P12) |
| response headers seen | `cache-control: no-store`, `x-frame-options: SAMEORIGIN`, `x-content-type-options: nosniff` |

**Cross-check against the landed snapshot (already on disk, `ExecCaptureS042`'s file):**

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-28 && sha256sum S042.txt
b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966  S042.txt
$ diff -q S042.txt /tmp/scout-S042.txt   # my independent capture-source.py run
IDENTICAL
```

I re-ran the instrument twice into `/tmp` (`capture-source.py --id S042 --url https://www.ipa.go.jp/security/todokede/vuln/process.html --out /tmp/scout-S042.txt --kind html`):
`sha256=b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`, 229982 fetched bytes → 60508 snapshot bytes, **byte-identical to the landed `corpus/source-snapshots/round-28/S042.txt`**. The raw HTML fetched by `curl` and by the instrument's `urllib` client normalise to the *same* text (`text_equal_curl_vs_instrument=True`).

---

## 2. Does the page carry the two claimed step sequences?

Measured on the capture text (60508 bytes / 974 lines; `S042.txt` line numbers below).

### 2a. The 10-step software-product flow — **PRESENT**, but under a different heading than the staged claim

Heading `ソフトウエア製品の取扱いプロセス` at **L132**, steps at L133, L136, L138, L140, L144, L146, L152, L154, L157, L159:

```
L133 1.届出の受付            L136 2.届出の受理／不受理の決定
L138 3.JPCERT/CC への脆弱性関連情報の連絡   L140 4.製品開発者へ連絡
L144 5.起算日の連絡          L146 6.製品開発者による対応
L152 7. 対応状況の受付       L154 8.公表日の調整
L157 9. 対応状況（対策方法）の公表         L159 10. 統計情報の公表
```

**But there is no section on the page named `脆弱性関連情報の取扱いプロセス`.** The string `脆弱性関連情報の取扱いプロセス` occurs **exactly once in the whole capture — L204**, and there it is the *title of the 2004-07-08 original posting* inside the 更新履歴 (revision-history) block:

```
L202 更新履歴
L203 2004年7月8日
L204 「脆弱性関連情報の取扱いプロセス」を掲載
```

The live page's own heading for the same material is `脆弱性関連情報の届出受付業務における取扱いプロセス` (L121, L122, and again in the site nav at L1 and L571). The 10 numbered steps hang off the **software-product** sub-heading, not off a `脆弱性関連情報の取扱いプロセス` heading.

### 2b. The web-application flow — **SEVEN steps, not six**

Heading `ウェブアプリケーションの取扱いプロセス` at **L161**, steps at L162, L165, L167, L170, L172, L179, L181:

```
L162 1. 届出の受付           L165 2.届出の受理／不受理の決定
L167 3.ウェブサイト運営者への連絡   L170 4.取扱い開始連絡
L172 5.ウェブサイト運営者による対応   L179 6.修正完了の連絡
L181 7.統計情報の公表          <- body L182
```

The flow does not end at `修正完了の連絡`; it ends with `7.統計情報の公表` (body L182: `IPAは、脆弱性に係る実態の周知徹底、被害の予防のため、脆弱性関連情報に係る届出受付業務に係る統計情報を公表します。その際、届出のウェブサイトが判別可能な情報は公表しません。`). Steps 1–6 are the operational path; step 7 is the statistics publication (the analogue of the product flow's step 10). **Any "steps 1 to 6" / "six-step" phrasing is unsupported by these bytes.** (Independently measured by `ExecCaptureS042`; this seat did not read that report before measuring.)

### 2c. A third flow the staged material does not mention

`自社製品の取扱いプロセス` at **L183**, 8 steps (L184, L186, L188, L190, L192, L196, L198, L200). Present in the bytes; optional for the entry.

---

## 3. Step 5 `起算日の連絡` — located quote with line context

Located at **L144** (heading) with its body at **L145**, inside the `ソフトウエア製品の取扱いプロセス` flow (heading L132), i.e. the 10-step list.

Exact capture lines:

```
L144  5.起算日の連絡
L145  JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。
```

Raw markup that produced them (`<dt class="def-list__ttl">` / `<dd class="def-list__desc">` pairs, one per step):

```html
<div class="def-list">
  <dt class="def-list__ttl">5.起算日の連絡</dt>
  <dd class="def-list__desc">
    <p class="article-txt">
JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。
    </p>
  </dd>
</div>
```

**Recommended ≤25-word Gate quote (63 chars, exactly-once, no `anchor` needed):**

> `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。`
> — ソフトウエア製品の取扱いプロセス step 5 (`5.起算日の連絡`, L144), body L145

Occurrence counts measured with the instrument's own normalization (`source-recheck.py`'s `normalize`: collapse whitespace, strip `<u>` tags) against the landed `S042.txt`:

| candidate | chars | occurrences |
|---|---|---|
| `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。` | 63 | **1** |
| `IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。` | 30 | 1 |
| `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）` | 31 | 1 |
| `5.起算日の連絡` (heading) | 8 | 1 — **but 8 chars is below `MIN_QUOTE_CHARS=12`**, so `source-recheck.py` rejects it as `quote-too-short-to-be-evidence`; use it as a *locator*, not as a manifest quote |
| `脆弱性関連情報の届出受付業務における取扱いプロセス` | 25 | **4** (L1, L121, L122, L571) → needs `anchor` |
| `IPA、JPCERT/CCは、脆弱性関連情報に係る対応状況（対策方法）をポータルサイト(JVN)にて公表します。` | — | **2** (L158, L199) → needs `anchor` |

Other exactly-once body quotes usable by `ExecManifest` / `ScribeEntryC2` (all measured, all ≥ 12 chars, all occ=1):

| line | chars | quote |
|---|---|---|
| L130 | 23 | `2004年7月8日から経済産業省の告示に基づき` |
| L131 | 40 | `IPA は、届出受付機関として届出された脆弱性関連情報を下記のとおり取扱います。` |
| L142 | 49 | `製品開発者に連絡が取れない場合は、連絡不能開発者一覧に公表し、製品開発者からの連絡を呼びかけます。` |
| L153 | 54 | `JPCERT/CCは、製品開発者の対応状況をIPAと共有します。また、発見者は、IPAへ進捗状況の問い合わせを行なう事ができます。` |
| L160 | 59 | `IPA、JPCERT/CCは、脆弱性に係る実態の周知徹底、被害の予防のため、脆弱性関連情報に係る統計情報を公表します。` |
| L171 | 44 | `発見者へ、ウェブサイト運営者に脆弱性関連情報を連絡した旨(取扱い開始連絡)を連絡します。` |
| L180 | 50 | `ウェブサイト運営者から脆弱性関連情報に係る修正完了の報告を受領した場合、その旨を発見者に連絡します。` |
| L182 | 29 | `その際、届出のウェブサイトが判別可能な情報は公表しません。` |

---

## 4. Confirmation of the staged S042 anchor claim — **partly contradicted**

Staged row (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` L18, read-only), anchor cell:

> `脆弱性関連情報の取扱いプロセス steps 1 to 10, step 5 起算日の連絡; ウェブアプリケーションの取扱いプロセス steps 1 to 6`

| staged claim | live-page verdict | evidence |
|---|---|---|
| `step 5 起算日の連絡` | **CONFIRMED** | heading `5.起算日の連絡` at L144, body L145, exactly-once for `起算日の連絡` (3 raw hits of `起算日` on 2 lines: L144 ×1, L145 ×2) |
| `脆弱性関連情報の取扱いプロセス steps 1 to 10` | **NOT as worded** | the 10 steps exist (L133–L159) but under `ソフトウエア製品の取扱いプロセス` (L132). The literal string `脆弱性関連情報の取扱いプロセス` exists only at L204, in the 更新履歴, as the 2004 posting's title — it names no live step list |
| `ウェブアプリケーションの取扱いプロセス steps 1 to 6` | **OFF BY ONE** | that flow has 7 steps (L162–L181), ending `7.統計情報の公表` (L182) |

The lane's already-landed registry row for S042 (`corpus/SOURCES.md` L48) does **not** repeat the staged wording: its anchor cell reads `脆弱性関連情報の届出受付業務における取扱いプロセス and ソフトウエア製品の取扱いプロセス steps 1 to 10 (L132-L160), step 5 起算日の連絡 (L144-L145) … 最終更新日 2017-05-30`, and its scope cell says the web-application flow has **7 steps**. My measurements are consistent with the landed row. The staged package wording is the thing that is wrong; the lane row must not inherit it.

### Attribution check against the staged *entry* text (not the row) — for `ScribeEntryC2`

The staged entry `japanese-domestic-disclosure-workflow.md` attributes several claims to the IPA page's step 5. Measured against `S042.txt`:

| staged entry claim | in S042 (IPA page) | in S041 (guideline) |
|---|---|---|
| "Step 5 has JPCERT/CC and the developer agree the publication schedule `対策方法の作成や海外の調整機関との調整に要する期間`" | **0 occurrences** | L256, L650, L651 |
| "`当該脆弱性情報流出に係るリスク`" | **0 occurrences** | L257, L652 |
| "The clock can be withdrawn … once one year has passed since 起算日" | **0** occurrences of `情報非開示依頼` / `撤回` / `1年` in this sense | L305–L307, L429–L430 |
| "`9 IPAは四半期ごとに統計情報を公表する`" (図1 flow, attributed jointly to "図1 of the 2026 guideline, and the IPA process page") | the IPA page's step 10 says `統計情報を公表` with **no** `四半期`; `四半期` on the IPA page occurs 38× but only in the unrelated site news feed | L216 (図1), L267, L482, L886 |
| `検証コード` / `画面キャプチャ` | **0 occurrences** | 3× / present (L338 area) |

So the IPA page's step 5 is the **起算日 relay** and nothing more; the schedule/leak-risk/withdrawal/quarterly material belongs to the **guideline (S041)**. An entry that keeps the staged attribution would put S042-unbacked quotes under an S042 `source:` header — an attribution failure under QUALITY Q2/Q4.

---

## 5. Markup quirks `capture-source.py --kind html` must handle on this page

Measured on the raw HTML (229982 bytes) and the normalised capture:

1. **Encoding.** `<meta charset="UTF-8">`; the HTTP `content-type` carries **no** charset parameter, so a client defaulting to Shift_JIS/latin-1 would mojibake it. The instrument decodes UTF-8 explicitly. Capture is valid UTF-8, **no BOM**, LF-only, 0 replacement characters (`�`), 0 NUL bytes.
2. **No entities, no `<u>` markup on this page.** `&nbsp;` = 0, `&amp;` = 0, `<u>` = 0. Therefore the `source-recheck.py` "normalized=markup-whitespace" branch is **not** needed for S042 — every recommended quote matches the raw bytes and the instrument prints plain `OK occurrences=1` (no `normalized=` prefix). (Do not assume that for the S041 PDF capture, where the split-quote pinning in `round-26/manifest.json` was required.)
3. **`<script>` / `<style>` are stripped** by `SCRIPT_RE`; `</p>`, `</div>`, `</li>`, `</tr>`, `</h1-6>`, `</section>`, `</article>`, `</br>` become newlines. The result is that each `<dt class="def-list__ttl">` heading lands on its **own** line and each `<dd>` body on the next — this is why `5.起算日の連絡` is exactly L144 and its body exactly L145. Line numbers are therefore stable for recheck purposes *within these pinned bytes*.
4. **Heading strings are NOT unique** because of nav/footer/news boilerplate — the capture keeps the whole site chrome and a site-wide news feed:
   - `脆弱性関連情報の届出受付業務における取扱いプロセス` → L1 (title bar), L121, L122, L571 (footer nav)
   - `ソフトウエア製品の取扱いプロセス` → L126, L132
   - `ウェブアプリケーションの取扱いプロセス` → L127, L161, L206, L208 (update-history lines)
   - `自社製品の取扱いプロセス` → L128, L183, L206
   → **Quote bodies, not headings.** Every heading quote needs an `anchor`; the recommended bodies are all exactly-once and need none.
5. **Inconsistent step-number spacing in the source itself** — a quote must match byte-for-byte:
   - product flow: `1.届出の受付` (no space) … `7. 対応状況の受付` (space after the dot), `9. 対応状況（対策方法）の公表`, `10. 統計情報の公表`
   - web flow: `1. 届出の受付` (space) but `2.届出の受理／不受理の決定` (no space)
   - so `5.起算日の連絡` (no space) occurs once, while `5. 起算日の連絡` (with space) occurs **0** times; the guideline S041 spells it `5起算日の連絡` (no dot). Quote the exact form of the source you cite.
6. **Bracket width differs between flows.** Step 5's body uses **fullwidth** `（起算日）`; the web-app step-4 body uses **halfwidth** `(取扱い開始連絡)`. Keep the original bracket form in the quote.
7. **Boilerplate volume.** L1–L120 = global nav, L121–L208 = the actual process content, **L209–L974 = footer nav + a live, dated news feed** (e.g. L520 `情報セキュリティ安心相談窓口の相談状況［2026年第3四半期（7月～9月）］`, L213 a JVN item). Consequence: a re-fetch may not be byte-identical (the feed changes); `source-recheck.py` is unaffected because it pins bytes by sha256, but **no receipt may claim that re-fetching reproduces `b432ec16…`**. Also, `四半期` appearing 38× in the capture is *news-feed noise*, never the disclosure statistic — do not let it be quoted as such.
8. **Content freshness vs retrieval date.** The page's own `最終更新日：2017年5月30日` (L123) is the revision stamp of the page; `opened 2026-10-25` is the retrieval date. Keep the two distinct in the registry row and the entry (Q4).

---

## 6. Machine-checked state at the moment of writing (observed, not assumed)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
S042:sha256 OK
S042:Q1 OK occurrences=1
S042:Q2 OK occurrences=1
S042:Q3 OK occurrences=1
S042:Q4 OK occurrences=1
S042:Q5 OK occurrences=1
S042:Q6 OK occurrences=1
exit=0
```

The landed `corpus/source-snapshots/round-28/manifest.json` (written by `ExecManifest`, not by this seat) pins `S042.txt` at `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` — the same digest this seat's independent capture produced — and all six of its S042 assertions print `occurrences=1`, exit 0. `S041` likewise rechecks exit 0. (`round-28/S041.txt` is byte-identical to `round-26/S041.txt`, sha `e18acbf99…`.)

## 7. Known gaps at write time (not this seat's to close)

- `corpus/knowledge/japanese-domestic-disclosure-workflow.md` is **not on disk** at write time (owner: `ScribeEntryC2`), so `python3 corpus/instruments/frontier-recheck-count.py` currently aborts with `FileNotFoundError` on that path and the F12 row at `corpus/README.md` L213 points at a file that does not yet exist. This is PRE-STATE, expected mid-wave; **no waiting/polling was done**.
- `corpus/SOURCES.md` L47/L48 already list the entry in S041/S042 `used-by`, so the sources census will report `E11 missing used-by` until the entry lands (already recorded by `ScribeRegistryC2`).

**L1 re-run commands after the entry lands (not run by this seat — an unrun check has not passed):**

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 --source S042; echo recheck_exit=$?
```

## 8. Handoffs

- **`ScribeEntryC2`** — write the web-application flow as **7 numbered steps (1–6 operational, 7 = 統計情報の公表)**, never "six-step"; anchor the 起算日 relay at `S042.txt:145`; keep the schedule-risk / withdrawal / quarterly / 検証コード material attributed to **S041**, not to the IPA page's step 5; do not repeat the staged "脆弱性関連情報の取扱いプロセス steps 1 to 10" wording (use `ソフトウエア製品の取扱いプロセス steps 1 to 10`, or the page heading `脆弱性関連情報の届出受付業務における取扱いプロセス`).
- **`ScribeRegistryC2`** — the landed S042 anchor cell already matches these bytes; no change needed.
- **`ExecManifest`** — the landed manifest's six S042 assertions all pass exactly-once at the pinned digest; no change needed.
- **`ScribeLesson`** — usable inline Gate quote (≤25 words / 63 chars, occ=1): `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。` — cite it as `S042.txt:145`, and record the two contradicted staged claims (§4) with their evidence lines (L204; L181–L182).

## 9. Honesty / tooling

- No tool was installed or upgraded; no pacman transaction was attempted (host-wide pause respected). No background job, no subagent, no VCS write was performed by this seat.
- Every count, quote, exit code and digest above is a single execution's output from this session. Scratch bytes live in `/tmp` only (`/tmp/scout-S042.txt`, `/tmp/scout-S042-b.txt`, `/tmp/ipa_process.html`, `/tmp/scout-exact.html`, `/tmp/scout-manifest/`).
- This seat wrote **no** production file: not `corpus/source-snapshots/round-28/S042.txt` (owner `ExecCaptureS042`), not `manifest.json` (owner `ExecManifest`), not `corpus/SOURCES.md` (owner `ScribeRegistryC2`).
