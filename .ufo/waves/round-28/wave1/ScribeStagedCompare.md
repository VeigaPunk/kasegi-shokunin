# Staged F12 entry vs the lane's F11 and F02 ground — overlap map

- Seat: `ScribeStagedCompare` (round 28, wave 1, kasegi-shokunin). Lane base `c9f8b115a098c65356e4b3b6048af45a37ab8395`.
- Date: 2026-10-25 (UTC). **Read-only seat: no production file was edited.** This file is the only artefact written.
- Consumers: `ScribeEntryC2` (writes `corpus/knowledge/japanese-domestic-disclosure-workflow.md`), `RevengerC2` (checks F12/F11 distinctness), L1.
- Everything below was measured against the committed bytes named in §1; commands are in §8 and each result is quoted as printed. Nothing here asserts what the landed entry *will* say — the entry does not exist yet.

## 0. Verdict

Nine claim units were separated out of the staged entry. Measured against the lane's two F11 entries and F02:

| class | count | units |
|---|---|---|
| duplicate of F11 or F02 ground | **0** | — |
| genuinely new ground | **6** | P2 nine-step flow, P3 起算日, P5 pre-publication notice, P6 one-year withdrawal, P7 付録3, P8 web-app parallel path |
| adjacent — must not be restated as F11/F02 ground | **3** | P1 (state-vs-platform contrast), P4 (negotiated schedule), P9 (Japanese column for timelines) |

Two annotations cut across those units and are counted separately:

| hazard | count | where |
|---|---|---|
| quote-level overlap with F11 (one shared assertion string) | **1** | P6 — F11-b already owns the 7-day receipt sentence |
| label collision that can manufacture a duplicate | **1** | P2 — `図1` names two different figures in one PDF |

The three headline new claims the ticket names are all real: the 起算日 workflow (P3), the one-year withdrawal (P6), the web-app parallel path (P8). None of them is anywhere in the lane's F11 entries (mechanical check, §8: `起算日`, `情報非開示依頼`, `取扱い開始連絡`, `修正完了`, `付録3`/`付録３` all return **0** in both F11 files) and none is in F02 (which mentions no Japanese source at all: `日本|Japan|JPCERT|IPA` → **0**).

F11's own ground — the 29147/30111 division and the policy-obligation divergence — is **not** re-made by the staged entry: `30111`, `社外とのやりとり`, `脆弱性公開ポリシー`, `最小限の要素` each occur **0** times in the staged bytes. The ticket's caution holds and is confirmed: the staged `source: S043` line names the guideline, and its anchor names `図1` + `付録3` — neither is 付録6, and the staged body makes no standards claim at all.

## 1. Objects compared

| object | path | sha256 |
|---|---|---|
| staged entry (read-only) | `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md` (55 lines) | `ee667c2f5d9d24da99eeed903c613a79c12912d83af3d4952f8e7a36458372ec` |
| F11-a | `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` | `b2600651e0c1725d93d8db738ae2301b476824b34693ab70c7c7c6aa88c85d85` |
| F11-b | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | `b55dcf9c33d1982d535712cd8ff4342dcaa99fd38aa10c369ccdc07abfbd7f80` |
| F02 | `corpus/knowledge/coordinated-disclosure-timelines.md` | `7ca630ca87572360b6c6210383694d3f897df91a3f6e3dd5902f3cad54600b8a` |
| round-28 S041 capture | `corpus/source-snapshots/round-28/S041.txt` | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` |
| round-28 S042 capture | `corpus/source-snapshots/round-28/S042.txt` | `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` |

Two provenance facts that bear on distinctness:

1. The round-28 `S041.txt` is **byte-identical** to the round-26 capture (`cmp` → `byte-identical`; both `e18acbf9…`), which is the capture both F11 entries cite. So F12's S041 provenance is not independent of F11's: the same bytes, re-fetched and re-pinned. Only S042 is new ground.
2. `corpus/source-snapshots/round-28/manifest.json` now exists and binds **12** assertions (S041 ×6, S042 ×6). All 12 are exactly-once in their capture (§8), and `source-recheck.py` exits 0 on both ids (§8) — but see D9 for the command form.

## 2. Overlap map, claim by claim

Line references `S041.txt` / `S042.txt` are round-28 capture lines. "F11" = the two entries above; "F02" = the timeline entry.

| unit | staged claim (short) | staged source | correct lane anchor (measured) | F11 | F02 | ruling |
|---|---|---|---|---|---|---|
| P1 | Japan runs a **state-coordinated** flow: "no marketplace, no bounty, no per-finding severity ratchet" | S042 + S043 | S042.txt:130 (economic-industry ministry 告示 since 2004-07-08) + :131 (IPA is 届出受付機関); S041.txt:251-267 | not F11 ground; F11-b is about obligation divergence (policy required vs not) | none | **adjacent, scope it.** Structural contrast, not a standards claim. Must be limited to the IPA/JPCERT/CC pipeline — see D7 |
| P2 | the nine-step flow (発見者→IPA→JPCERT/CC→開発者→調整→対策→公表前通知→公表→統計) | "図1 … and the IPA process page" | **S041.txt:249** (body caption `図１ ソフトウエア製品に係る脆弱性関連情報取扱の概要`, exactly-once) + **S041.txt:251-267** (items 1)-9)); S042.txt:132-159 is a **10-step** operational restatement | F11's `図1` is a *different object* (see §3) | none | **new**, but two anchors are conflated (D3, D4) |
| P3 | **起算日** = "the day the notification specified in Ⅳ.4.2) was first attempted" — attempt-anchored, not submission- or acknowledgment-anchored | footnote 4 | **S041.txt:340** verbatim; S042.txt:144-145 (step 5 起算日の連絡) | 0 hits in both F11 files | F02's triggers are submission-anchored (CERT/CC: "45 days after the initial report") and fix-anchored (Project Zero: "30 days after the fix") — 起算日 is neither | **new — headline.** This is the transferable artefact |
| P4 | the schedule is negotiated against "対策方法の作成や海外の調整機関との調整に要する期間" and "当該脆弱性情報流出に係るリスク" | "Step 5" | **S041.txt:256-258** = Ⅳ．１ item 5); the fuller 公表日 rule is Ⅳ．４．3) 公表日の決定 at S041.txt:643-654 with **four** considerations ①-④ | none | overlaps F02's *vocabulary* only: CISA "A time frame may be … a negotiated default starting point." No shared quote | **adjacent** — attribute per document, and do not restate CISA (D6) |
| P5 | the developer may notify users **before** the publication date | S043 | **S041.txt:261-263** (item 7)); restated at S041.txt:729 and S041.txt:828 ("公表前に通知する") | none | none | **new** |
| P6 | a finder may withdraw a **情報非開示依頼** once **one year** has passed since 起算日 | S043 | **S041.txt:305-306**; operator side at **S041.txt:429-433** (item 11) 情報非開示依頼の取下げ) | none | none | **new — headline**, but its quote string is also F11's (§3.1) |
| P7 | 付録3 法的な論点について gives finders / developers / site operators each their own legal section; finders attach 検証コード, 画面キャプチャ, ログ | S043, p.36 | TOC **S041.txt:37**; body **S041.txt:1333**; the three audiences at **S041.txt:1336** (発見者), **:1415** (製品開発者), **:1439** (ウェブサイト運営者); evidence artefacts at **S041.txt:341-346** (footnote 5) | F11 covers 付録**6**, not 付録3; no overlap | none | **new** |
| P8 | web applications have a parallel, lighter path via the ウェブサイト運営者, ending in 取扱い開始連絡 and 修正完了の連絡 | S042 | **S042.txt:161-181**: steps 1-7, with 4.取扱い開始連絡 (:170), 6.修正完了の連絡 (:179), **7.統計情報の公表 (:181)** | none | none | **new — headline**, but the "six-step / ends in 修正完了" description is falsified by step 7 (D4) |
| P9 | "Any future lane entry that compares coordinator timelines should use it as the Japanese column" | — | no source needed | — | this is F02's subject matter | **adjacent** — a forward pointer, not a claim; it must not read as though F02 now covers Japan (D6) |

## 3. The two overlap hazards, precisely

### 3.1 One shared assertion string (mechanically measured)

Of the 12 round-28 manifest assertions, exactly **one** is byte-identical to an assertion in the round-26 (F11) manifest:

```
shared (id,quote) pairs: 1
   S041 '受信した旨を 7 日以内に返信することが必要となります。'
```

`S041.txt:1916`, `付録6 §4` — this is F11-b's `q-seven-day-receipt` (manifest id Q4 there; Q5 in round-28). F11-b already states it, and already distinguishes the guideline's conformance-guidance voice ("必要となります") from the standard's own "recommended ... within seven calendar days" it reproduces at L1901-1903.

Ruling: pinning it in the round-28 manifest is harmless (a manifest assertion is not a claim), **but the F12 entry must not present it as new F12 ground**. If it appears at all it appears as a one-line 付録6 pointer, attributed the way F11-b attributes it. Preferred: leave it out; F12 does not need it.

### 3.2 `図1` names two different objects in one PDF

- **Body flow figure** — pointer sentence `S041.txt:212` ("…は、図１の通りです。"), caption `S041.txt:249` `図１ ソフトウエア製品に係る脆弱性関連情報取扱の概要`. Exactly-once. This is the object the staged entry means.
- **付録6 standards figure** — `S041.txt:1676` `図 1`, title `S041.txt:1677` `ISO/IEC 29147 と ISO/IEC 30111 の対応`, caption `S041.txt:1678`. This is F11-a's `jpcert-fig1-title` / `jpcert-fig1-caption`; F11-a's own Limits note already records that the caption string repeats five times inside 付録6 (L1678, L1777, L1867, L1908, L1974).

The numbering restarts per annex, so a bare "図1 of the 2026 guideline" is ambiguous and, read against the annex, lands on F11's figure. Ruling: the F12 entry cites the body figure **by line and caption** (`S041.txt:249`, quoted) and never as bare `図1`; it must not reuse `jpcert-fig1-title` or `jpcert-fig1-caption`. The round-28 manifest already does this correctly (S041/Q2 at L212, S041/Q3 at L249).

## 4. What is genuinely new, with the anchors to use

| new claim | quote | capture line |
|---|---|---|
| 起算日 definition | `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。` | S041.txt:340 |
| 起算日 relayed to the finder | `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。` | S042.txt:145 (heading `5.起算日の連絡` at :144) |
| one-year withdrawal | `なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、` … `情報非開示依頼の取り下げを求めることができます。` | S041.txt:305-306; S041.txt:429-433 |
| pre-publication user notice | `公表日以前に製品利用者に脆弱性検証の結果、対策方法および対応状況について通知することができる` | S041.txt:261-263 (cf. :729, :828) |
| 45-day publication target (staged entry omits it) | `みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。` | S041.txt:648, repeated at :786 |
| web-app path terminal steps | `発見者へ、ウェブサイト運営者に脆弱性関連情報を連絡した旨(取扱い開始連絡)を連絡します。` | S042.txt:171; the step list runs :161-181 |
| 付録3 audiences | `１ 発見者が心得ておくべき法的な論点` / `２ 製品開発者が…` / `３ ウェブサイト運営者が…` | S041.txt:1336 / :1415 / :1439 |

## 5. Adjacency boundaries — what F12 must not do

1. **Do not re-argue ISO conformance.** The 29147/30111 division (F11-a) and the policy-obligation divergence (F11-b) are settled ground with their own quote tables. F12 gets at most a one-clause pointer with no quote from 付録6 §2 and none of F11-b's six quote ids. Concretely, after landing, `grep -c '30111\|社外とのやりとり\|脆弱性公開ポリシー'` on the F12 entry should be **0**.
2. **Do not transplant a timeline.** F02's standing rule is that an interval belongs to the policy that states it and a trigger must be named. If F12 lands the 45-day `目安` (S041.txt:648) it must call it JPCERT/CC's *target* measured from 起算日, with the four considerations ①-④ (S041.txt:650-654), and must not present it as a deadline. The numeric coincidence with CERT/CC's 45 days (F02: "45 days after the initial report") is a trap in both directions: same number, different coordinator, different anchor, and F02's "Do not transplant CERT/CC or Project Zero intervals into another policy record" applies in reverse.
3. **Do not read the one-year withdrawal as a grace extension.** F02 asks for a documented extension condition; the withdrawal is a *state change of the secrecy obligation* (the finder who asked for non-disclosure may lift it), not an extension of a publication clock. Project Zero's 14-day grace is a different construct. If the analogy is drawn at all it must be rejected explicitly.
4. **Do not generalize the "no bounty" contrast.** The lane already holds a Japanese vendor whose published policy names `脆弱性報奨金制度を含む外部からの報告` as an intake channel (S036 L19, quoted in `vendor-disclosure-policy-commitments-crosswalk.md:59` as `cybozu-bounty-intake`). "No bounty" is true of the *state* pipeline only; unscoped it is contradicted by a lane row.

## 6. Defects in the staged bytes that would blur F12/F11 or break the landing

Each is a change `ScribeEntryC2` must make; none is a judgement about the staged author's intent [INFERENCE where marked].

- **D1 · `source: S043` must become `source: S041`.** No lane row S043 exists; the lane holds 41 rows (S001-S041). The staged S043 URL `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` is the URL of **lane S041** (`corpus/SOURCES.md:47`). Adopted verbatim the header would cite a nonexistent row. Frozen C2 says the same: "staged S043 = already lane S041 round 26, cited not re-registered". The staged S043 **row** in `SOURCES.append.md` is therefore not adoptable: its `teaches` and `anchor` cells describe a different anchor for an already-registered document — exactly the R8 trap — and the frozen predicate lands S041 used-by += the entry instead.
- **D2 · `ground: F13` must become `ground: F12`.** The staged entry says "F13 (new frontier item; extends F02…)"; `corpus/README.md`'s frontier ends at F11 and the frozen C2 declares F12. An F13 label would claim a row that does not exist and would leave the frozen `frontier_admitted 11→12` counter unmoved.
- **D3 · "Step 5" is used for two different documents' step 5.** In the same two paragraphs the staged entry writes "The IPA process page's step 5 is titled 起算日の連絡" (true: S042.txt:144) and "Step 5 has JPCERT/CC and the developer agree the publication schedule" (true only of S041's Ⅳ．１ item 5), S041.txt:256-258). The two documents also disagree on the flow's length: S041 lists **9** items (S041.txt:251-267), S042's page lists **10** (S042.txt:132-159, where 統計情報の公表 is step 10 and 起算日の連絡 is step 5). Fix: name the document with every step number.
- **D4 · the web-app flow is seven steps, and does not end where the staged entry says.** S042.txt:161-181 numbers 1.届出の受付 … 4.取扱い開始連絡 (:170) … 6.修正完了の連絡 (:179) … **7.統計情報の公表 (:181)**. "A second six-step flow … ending in 取扱い開始連絡 and 修正完了の連絡" is falsified by step 7, and 取扱い開始連絡 is step 4, not a terminal. The defensible formulation [INFERENCE — this is the distinction the source supports]: the web-app path has **no 起算日 step and no negotiated 公表日 step**; where the product flow has 5.起算日の連絡 it has 4.取扱い開始連絡, and where the product flow has 8.公表日の調整 it has 6.修正完了の連絡.
- **D5 · the quarterly-statistics claim drops `原則`.** S041.txt:267 reads `9) IPA は統計情報を、原則、四半期ごとに公表する`. The staged "IPAは四半期ごとに統計情報を公表" drops the qualifier; S042's step 10 (:159) states no period at all. Anchor the qualifier to S041.
- **D6 · the 45-day target and consideration ④ are missing.** S041.txt:648 gives `45 日後を目安`; the four considerations are ①対策方法の作成に要する期間 ②海外の調整機関との調整に要する期間 ③脆弱性情報流出に係るリスク ④当該脆弱性の悪用に関するリスク (S041.txt:650-654). The staged entry quotes ①②③ and omits ④ and the target. See §5.2 before adding the target.
- **D7 · "no bounty" unscoped** — see §5.4; scope the sentence to the state pipeline.
- **D8 · header fields are stale for the landing.** `verified-at: 2026-10-23` must be `2026-10-25` (Q1; Gate access dates are today). The staged `recheck:` is a network `curl … && pdftotext` prose-hybrid with no `cd` prefix and no `--source` — it fails Q10 (parse/cwd) and R12 (id coverage), covers only S043/S041, and never exercises S042.
- **D9 · the prescribed recheck form silently checks one id.** `source-recheck.py` declares `--source` as a single-value option (`corpus/instruments/source-recheck.py:275`), so `--source S041 --source S042` keeps only S042 and prints **7** lines (S042 sha256 + Q1-Q6), exit 0 — the S041 half is never checked. Measured:
  ```
  $ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 --source S042
  S042:sha256 OK
  S042:Q1 OK occurrences=1 … S042:Q6 OK occurrences=1
  exit=0
  ```
  Correct single line (verified, 14 lines, exit 0):
  ```
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
  ```
  This also corrects round-27 lesson carry-forward 3, which prescribes the collapsing form.
- **D10 · manifest documentation pointer (for `ExecManifest`/L1, not the entry).** Round-28 S041/Q4 labels L648 "Ⅳ．４．5) note". The sentence sits under **Ⅳ．４．3) 公表日の決定** (heading at S041.txt:643, inside `４．JPCERT/CC（調整機関）の対応` at :596); item 5) is 脆弱性関連情報の取扱い at :673. `location` is documentation the instrument does not read (Q9), so this is not a gate failure — but `ScribeEntryC2` must not copy the label.

## 7. Anchors: use / forbid

Use the §4 table. Forbid in the F12 entry (things F11 already owns or that would re-anchor F11's figure):

`jpcert-29147-subject`, `jpcert-outward-exchanges`, `jpcert-outward-enum`, `jpcert-30111-half1`, `jpcert-30111-half2`, `jpcert-fig1-title`, `jpcert-fig1-caption` (F11-a); `q-policy-not-required`, `q-policy-required`, `q-seven-day-receipt`, `q-min-policy-aspects`, `q-optional-policy-aspects`, `q-secure-comm-option`, the 参考1 clause table and the 6.2/6.3 republication (F11-b); F02's `s003`/`s004`/`s005` quotes and its 90-day / 45-day / 14-day statements.

Not forbidden, but must not be new F12 ground: the 7-day receipt sentence (§3.1).

## 8. Re-runnable distinctness checks (for `RevengerC2`; all run, results as printed)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
grep -c '起算日'   corpus/knowledge/iso-29147-and-30111-division-of-labour.md corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md   # 0 0
grep -cE '30111|社外とのやりとり|脆弱性公開ポリシー|最小限の要素' /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md   # 0  (one count: lines matching any pattern)
grep -cE '日本|Japan|JPCERT|IPA' corpus/knowledge/coordinated-disclosure-timelines.md   # 0
grep -n '図１\|図 1' corpus/source-snapshots/round-28/S041.txt   # 212, 249 (body flow) and 1676 (付録6 figure label)
```
Round-28 manifest integrity (12/12 exactly-once, both ids exit 0) — measured by counting each `quotes[].quote` in its `path`, and by:
```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
```
Manifest-vs-F11 assertion overlap (round-26 vs round-28 manifests, by `(id, quote)`): shared = **1**, the 7-day receipt string (§3.1).

After the F12 entry lands, the two checks that decide distinctness:
```
grep -c '付録6\|30111\|社外とのやりとり\|脆弱性公開ポリシー' corpus/knowledge/japanese-domestic-disclosure-workflow.md   # expect 0, or a pointer count with the quote ids of §7 absent
grep -c '起算日' corpus/knowledge/iso-29147-and-30111-division-of-labour.md corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md   # expect 0 0 (F11 must not grow F12's term)
```

## 9. Limits and what this seat did not run

- Read-only: no production file edited, no VCS write, no subagent, no background job, no tool installed. This file is the only artefact written in the lane.
- Disclosure: the first write used a lane-relative path and, because the tool's cwd is the fleet root, landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-28/wave1/ScribeStagedCompare.md` (a path outside this lane's write scope). It was immediately byte-copied here (identical sha256), the stray file deleted, and the two directories it had created removed; nothing else under the fleet root was read or altered, and `.ufo/waves` (pre-existing) is intact.
- This is a comparison of staged bytes against lane bytes; it does not review the landed F12 entry (it does not exist) and does not judge frozen C2's after-values.
- The staging package's `SOURCES.append.md` numbers the IPA page `S042` and the JPCERT guideline `S043`; the lane mapping (staged S042 → lane S042, staged S043 → lane S041) is per frozen C2 and round-27 lesson carry-forward 3, and is corroborated above by URL identity, not assumed.
- Capture-level facts (line numbers, occurrence counts) are true of the round-28 bytes only; the PDF and the IPA page may change after 2026-10-25.
- No `anchorcheck.py` work was touched; the C1 instrument was not read or run by this seat.
