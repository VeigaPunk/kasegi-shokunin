# ExecCaptureS042 — round-28 wave 1, C2 capture limb

- seat: ExecCaptureS042 (executor, leaf; no subagents, no background jobs, no VCS writes)
- lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `c9f8b115a098c65356e4b3b6048af45a37ab8395`
- owned production path written: `corpus/source-snapshots/round-28/S042.txt` (only)
- receipt: `.ufo/waves/round-28/receipts/ExecCaptureS042.txt`
- axes: coverage · status: capture landed; one dispatch expectation **fails** verification (§4)

## 1. Capture

Instrument invocation (exactly as dispatched):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py --id S042 --url https://www.ipa.go.jp/security/todokede/vuln/process.html --kind html --out corpus/source-snapshots/round-28/S042.txt
```

Verbatim stdout, exit 0:

```
S042 status=200 fetched_bytes=229982 snapshot_bytes=60508 sha256=b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966 utc=2026-10-25T17:22:03Z out=corpus/source-snapshots/round-28/S042.txt
```

| field | value |
|---|---|
| HTTP status | 200 |
| fetched bytes | 229982 |
| snapshot bytes / lines | 60508 / 974 |
| sha256 (independent `sha256sum`, matches instrument) | `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` |
| fetch timestamp (UTC) | `2026-10-25T17:22:03Z` |

Supporting pipeline-determinism check: `capture-source.py --selftest` → `selftest normalize=ok deterministic=ok`, exit 0. Hygiene: UTF-8 valid, 0 NUL bytes, 0 residual `<` tags, 0 residual HTML entities, trailing newline present.

## 2. Keyword sweep

`起算日` — 3 occurrences on 2 lines:

| line | chars | first 100 chars |
|---|---|---|
| L144 | 8 | `5.起算日の連絡` |
| L145 | 93 | `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。` |

`取扱いプロセス` — 16 occurrences on 15 lines: L1, L121, L122, L126, L127, L128, L129, L132, L161, L183, L204, L206, L208, L571, L573. First-100-char text for each is tabulated in the receipt §4.

## 3. Flow headings found (verbatim, with capture lines)

**ソフトウエア製品の取扱いプロセス — 10 steps, CONFIRMED:** L133 `1.届出の受付` · L136 `2.届出の受理／不受理の決定` · L138 `3.JPCERT/CC への脆弱性関連情報の連絡` · L140 `4.製品開発者へ連絡` · L144 `5.起算日の連絡` · L146 `6.製品開発者による対応` · L152 `7. 対応状況の受付` · L154 `8.公表日の調整` · L157 `9. 対応状況（対策方法）の公表` · L159 `10. 統計情報の公表`.

**ウェブアプリケーションの取扱いプロセス — SEVEN steps, not six:** L162 `1. 届出の受付` · L165 `2.届出の受理／不受理の決定` · L167 `3.ウェブサイト運営者への連絡` · L170 `4.取扱い開始連絡` · L172 `5.ウェブサイト運営者による対応` · L179 `6.修正完了の連絡` · L181 `7.統計情報の公表`.

**自社製品の取扱いプロセス — 8 steps, present but not named in the dispatch:** L184/L186/L188/L190/L192/L196/L198/L200 (`1. 届出の受付`, `2.届出の受理／不受理の決定`, `3.JPCERT/CC への脆弱性関連情報の連絡`, `4.製品開発者へ連絡`, `5. 製品開発者による対応`, `6.公表日の調整`, `7.対応状況（対策方法）の公表`, `8.統計情報の公表`).

Page provenance in the capture: L123 `最終更新日：2017年5月30日`; 更新履歴 L202-L208 (2004-07-08 掲載 / 2015-07-23 改訂+自社製品追加 / 2017-05-30 改訂).

## 4. Finding — the "6-step web-application flow" expectation is not in the bytes

The dispatch asked me to verify a six-step web-application flow. The instrument's bytes number **seven** steps, contiguous 1-7, ending in `7.統計情報の公表` (body L182: `その際、届出のウェブサイトが判別可能な情報は公表しません。`). Steps 1-6 are the operational path; step 7 is the statistics publication, the analogue of product-flow step 10. So "six-step" holds only if the closing statistics step is excluded — the page does **not** end at 修正完了の連絡.

This also contradicts the staged assimilation entry (read-only): `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md` L46 asserts a "second six-step flow ... ending in 取扱い開始連絡 and 修正完了の連絡". The `6-step` wording also appears in the ScribeEntryC2 dispatch text ("10-step product path + 6-step web-app path") and in this seat's own dispatch, so it will propagate unless corrected. Capture-grounded phrasing for the entry: *7 numbered steps (1-6 operational, 7 = 統計情報の公表); no 公表日の調整 step*.

I did not hand-scrape, edit or normalize the snapshot to fit the expectation.

## 5. Manifest support (measured for ExecManifest)

All candidates below are contiguous byte substrings, exactly-once under `source-recheck.py`'s normalization, and ≥ `MIN_QUOTE_CHARS=12`, so none needs an `anchor`:

| id | line | occ | chars | quote |
|---|---|---|---|---|
| Q1-step5-startdate | L145 | 1 | 63 | `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。` |
| Q2-intake-role | L131 | 1 | 40 | `IPA は、届出受付機関として届出された脆弱性関連情報を下記のとおり取扱います。` |
| Q3-legal-basis | L130 | 1 | 23 | `2004年7月8日から経済産業省の告示に基づき` |
| Q4-webapp-fix-report | L180 | 1 | 50 | `ウェブサイト運営者から脆弱性関連情報に係る修正完了の報告を受領した場合、その旨を発見者に連絡します。` |
| Q5-webapp-stats-redaction | L182 | 1 | 29 | `その際、届出のウェブサイトが判別可能な情報は公表しません。` |
| Q6-unreachable-developer | L142 | 1 | 49 | `製品開発者に連絡が取れない場合は、連絡不能開発者一覧に公表し、製品開発者からの連絡を呼びかけます。` |
| Q7-product-stats-step | L160 | 1 | 59 | `IPA、JPCERT/CCは、脆弱性に係る実態の周知徹底、被害の予防のため、脆弱性関連情報に係る統計情報を公表します。` |

Measured traps (do not quote): `5.起算日の連絡` (8 chars) and `10. 統計情報の公表` (9 chars) fall below `MIN_QUOTE_CHARS` → `UNAVAILABLE quote-too-short-to-be-evidence`; `脆弱性関連情報の届出受付業務における取扱いプロセス` occurs 4× (L1, L121, L122, L571) and `IPA、JPCERT/CCは、脆弱性関連情報に係る対応状況（対策方法）をポータルサイト(JVN)にて公表します。` occurs 2× (L158, L199) → both need `anchor=`.

## 6. Post-landing recheck of my own capture (manifest appeared after my capture)

ExecManifest landed `corpus/source-snapshots/round-28/manifest.json` (sha256 `e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d`) after my capture; I then ran the S042 limb read-only at `2026-10-25T17:25:25Z`:

```
S042:sha256 OK
S042:Q1 OK occurrences=1
S042:Q2 OK occurrences=1
S042:Q3 OK occurrences=1
S042:Q4 OK occurrences=1
S042:Q5 OK occurrences=1
S042:Q6 OK occurrences=1
exit=0
```

So my landed bytes are the bytes the manifest pins, and every S042 assertion is exactly-once with no anchor needed. The full-manifest run (S041 included) remains ExecManifest's authoritative one; the manifest's own location text never counts web-app steps, so the §4 finding requires no manifest change.

## 7. Risks

1. `6-step` claims in the registry anchor, entry body or lesson Gate are unsupported by this capture (§4). ExecManifest's `location` text never counts web-app steps, so its manifest needs no change.
2. The snapshot necessarily includes IPA chrome and a live news feed (L209-L974) with dated items (L213 JVN#66473735 Movable Type item; L520 2026年第3四半期 consultation report). A future re-fetch will not be byte-identical; `source-recheck` is unaffected (it pins these bytes), but no receipt may claim a re-fetch reproduces `b432ec16…`.
3. The document is a 2017-dated page (最終更新日 2017年5月30日); `opened 2026-10-25` is the retrieval date, not content freshness.
4. No credential/session/private-URL material is present in the snapshot or receipts.

## 8. Handoffs

- **ExecManifest** (done): pin `S042.txt` at `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` — confirmed identical in the landed manifest, and its Q1 is my L145 quote (§6).
- **ScribeEntryC2**: replace the staged "six-step" claim with the capture-grounded 7-step reading; anchor `起算日` at `S042.txt:145`.
- **ScribeRegistryC2**: the S042 anchor cell should read "10-step product flow + step 5 起算日の連絡 + 7-step web-application flow", not 6-step.
- **L1**: the whole-manifest recheck is ExecManifest's (`--manifest corpus/source-snapshots/round-28/manifest.json`, exit 0 reported); my own `--source S042` limb at `2026-10-25T17:25:25Z` exited 0 on the landed bytes (§6). Re-run that limb only if `S042.txt` is ever rewritten.

## 9. Not run (unrun ≠ passed)

Frontier harness, sources census, anchorcheck C1 counters — none are this item's and none were executed here. No tool install or pacman transaction was performed.
