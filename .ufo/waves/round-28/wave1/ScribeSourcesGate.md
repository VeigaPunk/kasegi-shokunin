# ScribeSourcesGate — SOURCES-anchored evidence block (round 28, wave 1)

Seat: `ScribeSourcesGate` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Claims freeze: `.ufo/waves/round-28/claims.json` (base `c9f8b115a098c65356e4b3b6048af45a37ab8395`).
Written: 2026-10-25 (UTC). Role: **read-only evidence assembly — no production edits**.
Every `S###`, URL, access date, line number, occurrence count and exit code below was produced by
a command run in this seat; nothing is quoted from memory or from another seat's receipt.

Purpose: the report's *Sources & frontier* raw material, and the §2b "at least one sourced claim"
evidence for C2, which rests on **S042 opened this round (2026-10-25)**.

---

## 0. Method and instruments

| step | command (absolute paths) | instrument |
|---|---|---|
| capture IPA page | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py --id S042 --url https://www.ipa.go.jp/security/todokede/vuln/process.html --kind html --out .ufo/waves/round-28/wave1/ScribeSourcesGate/S042.try.txt` | `corpus/instruments/capture-source.py` (repo, unmodified) |
| capture JPCERT guideline | same instrument, `--id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out …/S041.try.txt` | same |
| assert quotes | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json` | `corpus/instruments/source-recheck.py` (repo, unmodified) |
| census / row count | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md` and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi` / `… validate …` | fleet census script, lane `SOURCES.md` |

No tool was installed or upgraded for this seat (existing `python3` 3.14, `pdftotext` already present
via `capture-source.py --kind pdf`); no `pacman` transaction was attempted. The captured bytes used for the
cross-check below were kept only under `.ufo/waves/round-28/wave1/ScribeSourcesGate/` and are **not committed**
(QUALITY R14, wave-evidence economy: no full corpus copy in git — the digests and fetch metadata below are the
evidence, and the exact capture commands regenerate the bytes); the live snapshots under
`corpus/source-snapshots/round-28/` were written by `ExecCaptureS041`/`ExecCaptureS042`, not by this seat.

---

## 1. Sources opened this round

### 1.1 S042 — IPA intake-process page (new row, round 28)

| field | value |
|---|---|
| S-row | **S042** (`corpus/SOURCES.md` row, tier A, docs, mined, opened 2026-10-25) |
| URL | `https://www.ipa.go.jp/security/todokede/vuln/process.html` |
| Access date | **2026-10-25** |
| HTTP | `status=200 fetched_bytes=229982` → `snapshot_bytes=60508`, `utc=2026-10-25T17:22:35Z` (this seat's own fetch) |
| Snapshot | `corpus/source-snapshots/round-28/S042.txt`, `sha256=b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` |
| Page provenance | `最終更新日：2017年5月30日` (L123); update history ends `2017年5月30日 — ソフトウェア製品、ウェブアプリケーションの取扱いプロセスを改訂` (L207–L208). **The page is a 2017 revision, not a 2026 statement.** |
| Knowledge path citing it | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` |

Located quotes (each ≤25 whitespace tokens, each measured in the committed capture):

1. **L145** — `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。`
   — 2 tokens, **occurrences=1**. Located under heading `5.起算日の連絡` (L144) of
   `ソフトウエア製品の取扱いプロセス` (L132). This is the claim S042's `teaches` cell rests on:
   the finder is told both the 起算日 and the detail-information date.
2. **L171** — `発見者へ、ウェブサイト運営者に脆弱性関連情報を連絡した旨(取扱い開始連絡)を連絡します。`
   — 1 token, **occurrences=1**. Web-application flow step 4 `取扱い開始連絡` (L170).
3. **L123** — `最終更新日：2017年5月30日` — 1 token, **occurrences=1** (the bare string
   `2017年5月30日` occurs twice, L123 and L207; only the prefixed form is exactly-once).
4. Structural anchors verified (not assertions): the software flow heading is **L132** (`ソフトウエア製品の取扱いプロセス`),
   its ten step headings run **L133 (1.届出の受付) → L159 (10. 統計情報の公表)** with the last body line **L160**;
   the web-application flow heading is **L161** and its **seven** steps run **L162–L182** (届出の受付, 受理／不受理,
   ウェブサイト運営者への連絡, 取扱い開始連絡, 対応, 修正完了の連絡, 統計情報の公表); a third flow
   `自社製品の取扱いプロセス` begins at **L183**, with step headings **L184 → L200** and the last body **L201**.

### 1.2 S041 — JPCERT/CC 2026 partnership guideline (re-capture of an existing row)

| field | value |
|---|---|
| S-row | **S041** (`corpus/SOURCES.md` row, tier A, spec, mined, opened 2026-10-25; round-26 row, re-captured round 28) |
| URL | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` |
| Access date | **2026-10-25** |
| HTTP | `status=200 fetched_bytes=1338665` → `snapshot_bytes=147267`, `utc=2026-10-25T17:22:39Z` (this seat's own fetch) |
| Snapshot | `corpus/source-snapshots/round-28/S041.txt`, `sha256=e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` |
| Edition evidence | PDF digital signature block L1–L7: `日付 : 2026.09.29 18:01:10 +09'00'`; title block L8–L10: `情報セキュリティ早期警戒 / パートナーシップガイドライン / 2026 年 10 月` |
| Knowledge path citing it | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (plus the pre-existing `corpus/knowledge/iso-29147-and-30111-division-of-labour.md`, `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`) |

Located quotes (each ≤25 whitespace tokens, each measured in the committed capture):

1. **L340** (footnote 4) — `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。`
   — 1 token, **occurrences=1**. The normative 起算日 definition: *first attempted* contact, not
   acknowledgement and not submission.
2. **L306** — `情報非開示依頼の取り下げを求めることができます。` — 1 token, **occurrences=1**.
   Read with L305 (`なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、`) the
   one-year withdrawal rule holds; the two lines are separate capture lines and must not be asserted
   as one unanchored multi-line string.
3. **L1677** (図 1 caption, `付録６ 国際標準に準拠するための留意点` p.45) —
   `ISO/IEC 29147 と ISO/IEC 30111 の対応` — 6 tokens, **occurrences=1**.
4. **L7** — `日付 : 2026.09.29 18:01:10 +09'00'` — 5 tokens, **occurrences=1**; and **L10** —
   `2026 年 10 月` — 4 tokens, **occurrences=1**. Edition pin only; neither is a substantive claim.

---

## 2. Staged assimilation package (read-only, `/home/vgpnk/Projects/shokuknow/merge/kasegi/`)

Opened today, 2026-10-25, read-only. No write, no script from the package was executed.

| staged file | S-row it becomes / cites | URL it carries | access date | ≤25-word located quote | knowledge path citing it |
|---|---|---|---|---|---|
| `MERGE-REPORT.md` | own-work packaging record (cites the whole package, not one row) | — (local path) | 2026-10-25 | L3: `Staged by \`corpus-expansion-1\`. **Nothing was written into the lane repo.**` (10 tokens, occ=1) | n/a — packaging record, cited by this report only |
| `MERGE-REPORT.md` L9 | id-space claim (stale) | — | 2026-10-25 | `lane registry currently holds **30** rows; first staged id is **S031**` (11 tokens, occ=1) | n/a — see finding F-2 |
| `SOURCES.append.md` L18 | becomes **S042** (staged id ≡ lane id, URL-verified) | `https://www.ipa.go.jp/security/todokede/vuln/process.html` | 2026-10-25 | `Japan runs a coordinator-mediated flow in which the finder is told the 起算日 and the detail-information date, and may query progress` (21 tokens, occ=1) | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` |
| `SOURCES.append.md` L19 | cites **S041** (staged id `S043`; URL identical to lane S041 — see finding F-3) | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | 2026-10-25 | row title `情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月` | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` |
| `knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md` L52 | cites **S042** and staged `S043` (= lane **S041**) | both URLs above | 2026-10-25 | `起算日 is the single most transferable artefact this round produced.` (10 tokens, occ=1) | lands at `corpus/knowledge/japanese-domestic-disclosure-workflow.md` |

Staged header block as read (L4–L8): `source: S042 — …process.html — 脆弱性関連情報の取扱いプロセス, step 5 起算日の連絡`;
`source: S043 — …partnership_guideline2026.pdf — 2026年10月, 図1, 付録3 法的な論点について`;
`verified-at: 2026-10-23`; `recheck: 180d — \`curl -sSL …\` then confirm the edition stamp is still 2026年10月 (ran 2026-10-23)`;
`ground: F13 (new frontier item; extends F02, which compares coordinator timelines)`.

Note on the staged entry's own citation of 起算日 and the publication schedule: the staged text attributes the
schedule wording to "step 5", and neither quoted phrase is present in the S042 capture — measured
`occurrences=0` in `S042.txt` for both `対策方法の作成や海外の調整機関との調整に要する期間` and
`当該脆弱性情報流出に係るリスク`. In S041 the same substance appears, but the first phrase is **split by the
PDF's hard wrap** (`…海外の調整機関との調整に要す` at L256, continuing `る期間` at L257), so the composed string is a
readable reconstruction with raw `occurrences=0`, not a citable substring; the guideline also states the factors
separately as `① 対策方法の作成に要する期間` (L650) and `② 海外の調整機関との調整に要する期間` (L651), each
exactly-once and directly assertable. `当該脆弱性情報流出に係るリスク` occurs twice in `S041.txt` (L257, L781),
so it would need an anchor. Any landed sentence keeping that wording must cite **S041**, never S042.

---

## 3. Q9 assertion audit of the landed manifest (measured, not assumed)

Manifest: `corpus/source-snapshots/round-28/manifest.json` (written by `ExecManifest`; present at 2026-10-25 14:24 local).
Run: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json`

```
S041:sha256 OK
S041:Q1 OK occurrences=1
S041:Q2 OK occurrences=1
S041:Q3 OK occurrences=1
S041:Q4 OK occurrences=1
S041:Q5 OK occurrences=1
S041:Q6 OK occurrences=1
S042:sha256 OK
S042:Q1 OK occurrences=1
S042:Q2 OK occurrences=1
S042:Q3 OK occurrences=1
S042:Q4 OK occurrences=1
S042:Q5 OK occurrences=1
S042:Q6 OK occurrences=1
recheck_exit=0
```

Independent recount of all 12 assertions against the committed snapshots (`str.count` on the raw UTF-8 text):
**every assertion occurs exactly once** (`occ=1`), so no `anchor` field is required by Q9 and
`anchor_verdict` reports no `MISSING`/`BROKEN` note. Path stems equal ids (`S041.txt`, `S042.txt`) and both
sha256 pins match the files on disk.

Discriminating candidates this seat rejected (they would have tripped Q9 if used unanchored):

| candidate quote | capture | occurrences | lines |
|---|---|---|---|
| `JPCERT/CCは製品開発者と脆弱性関連情報に係る公表日を調整します。` | S042 | **2** | 155, 197 |
| `ソフトウェア製品、ウェブアプリケーションの取扱いプロセスを改訂` | S042 | **2** | 206, 208 |
| `脆弱性関連情報の届出受付業務における取扱いプロセス` (page title) | S042 | **4** | 1, 121, 122, 571 |
| `起算日の連絡` | S041 | **4** | 1170, 1171, 1186, 1211 |
| `45 日後を目安とします。` (short form) | S041 | **2** | 648, 786 |
| `１ 発見者が心得ておくべき法的な論点` | S041 | **2** | 38 (TOC), 1336 (body) |

The landed manifest's S041 Q4 quote is the *longer* discriminator
`みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、` — occ=1 at L648, which is why it passes
without an anchor. Future edits must keep the long form (or add `"anchor": 648`).

---

## 4. Independent capture cross-check (two fetches, same bytes)

This seat fetched both URLs itself, at 17:22:35Z (S042) and 17:22:39Z (S041), into its own scratch directory
(`.ufo/waves/round-28/wave1/ScribeSourcesGate/S042.try.txt` and `S041.try.txt`, now deleted after digesting under
R14 — regenerate with the §0 capture commands, which reproduce these bytes deterministically whenever the host
serves the same content). The files `ExecCaptureS041`/`ExecCaptureS042` committed to
`corpus/source-snapshots/round-28/` carry the **same digests**:

```
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-28/S041.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  .ufo/waves/round-28/wave1/ScribeSourcesGate/S041.try.txt
b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966  corpus/source-snapshots/round-28/S042.txt
b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966  .ufo/waves/round-28/wave1/ScribeSourcesGate/S042.try.txt
```

That is a second, independent DNS/TLS fetch of each URL inside the round, not a replay of the committed file:
the captures are reproducible within the round, and the manifest sha256 pins are not a transcription artifact.

---

## 5. Census row count — S042 lands at exactly 42 rows (re-run by this seat)

Frozen counter basis: rows with an `S###` id cell in `corpus/SOURCES.md`.

PRE-STATE (before `ScribeRegistryC2`'s append reached the working tree):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md
41
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
kasegi  rows    41
kasegi  tier.A  38
kasegi  tier.B  1
kasegi  tier.C  2
kasegi  status.mined     29
kasegi  status.queued    9
kasegi  status.rejected  3
FLEET   rows    41
census_mode_exit=0
```

POST-STATE (after the S042 append and the S041 `used-by` edit were present):

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md
42
$ grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
1
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi > /tmp/sg-census.out 2>&1; echo "census_mode_exit=$?"
census_mode_exit=0
$ cat /tmp/sg-census.out | head -9
kasegi  rows    42
kasegi  tier.A  39
kasegi  tier.B  1
kasegi  tier.C  2
kasegi  status.mined     30
kasegi  status.queued    9
kasegi  status.rejected  3
FLEET   rows    42
```

Measurement note: the exit code above is the census script's own — the run redirects to a file and the pipe to
`head` happens afterwards. (An earlier piped invocation in this seat reported `head`'s status, not the script's;
that figure was discarded, not reported.) Census output is TSV; the two columns are shown space-separated here.

**Confirmed: total row count is exactly 42** (41 + the one S042 row), with exactly one S042 row.
The delta is arithmetic-clean: `rows 41→42`, `tier.A 38→39`, `status.mined 29→30`, everything else unchanged.

Census `validate` (the frozen C2 counter), observed twice:

**Interim — entry not yet on disk (measured before `ScribeEntryC2` landed):**

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi  W04  S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi  W04  S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi  E11  S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
kasegi  E11  S042 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
census_exit=1
```

Both E11 rows pointed at the one absent entry file; nothing in the registry was wrong.

**Final — after the entry landed (this is the state the round closes on):**

```
$ ls corpus/knowledge/japanese-domestic-disclosure-workflow.md
corpus/knowledge/japanese-domestic-disclosure-workflow.md
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi  W04  S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi  W04  S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi  ok    /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

`census_exit=0` with the two unchanged W04 warnings and no E-codes. E11 cleared exactly as predicted — the
fix was the entry file, not a registry edit. The re-run command for the L1 (same command, unchanged):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l
```

Observed: `census_exit=0`, `42`, `1`.

Other frozen C2 counters, measured after the entry landed:

```
frontier_admitted=12        # awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
entries_citing_S042=1       # grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l
```

Landed entry spot-check (headers only; the entry is `ScribeEntryC2`'s file, not this seat's):
`L3` = `source: S041 — …partnership_guideline2026.pdf — … 注釈4 起算日の定義 (L340) …`; `L4` = `source: S042 — …process.html — …` with the 2017-05-30 date;
`L6` = one `recheck:` line, `bash -n` exit 0, carrying `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` and **both**
`--source S041` and `--source S042` against `corpus/source-snapshots/round-28/manifest.json`; `L7` = `ground: F12`.
Its S041 header anchors spot-check true against the capture: Ⅳ.11) `情報非開示依頼の取下げ` heading **L429** (body L430),
付録２ `付録２ 脆弱性情報取扱いのフロー` heading **L1156**, 図３ **L1281**, 図４ **L1331**.

`corpus/README.md` now carries the F12 row: `| F12 | Japanese state-coordinated disclosure workflow | admitted | knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | Use 起算日 — the first *attempted* developer contact, not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02. |` — frontier 11→12, and the appended `S042` row now has its admitted entry citing it, so the C2 kill rule's "row without an admitted entry" arm is clear at this writing.

---

## 6. §2b evidence — at least one claim sourced this round

> **Sourced claim (C2 / F12).** The Japanese state-coordinated flow gives the finder a clock start date.
> Source **S042**, `https://www.ipa.go.jp/security/todokede/vuln/process.html`, opened **2026-10-25**,
> snapshot `corpus/source-snapshots/round-28/S042.txt` `sha256=b432ec16…96966`, at **L144–L145**:
> `5.起算日の連絡` / `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。`
> (occ=1). The clock's *definition* is not on that page but in **S041** (opened 2026-10-25,
> `sha256=e18acbf9…ab47`) at **L340**: `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。` (occ=1).
> Knowledge path: `corpus/knowledge/japanese-domestic-disclosure-workflow.md`.

Two tiers of evidence are kept apart on purpose: S042 states *that* IPA relays the 起算日 and the
detail-contact date to the finder (first-party coordinator process); S041 states *what* the 起算日 is
(first attempted contact under Ⅳ.4.2). Neither generalizes the rule beyond Japan; S042's own page is a
2017 revision (L123), so the claim is "the process the page describes", not "Japan's 2026 rule" — the
2026 date belongs to S041's edition stamp (L10, digital signature L7).

---

## 7. Findings and risks (for the L1 and for the other seats)

- **F-1 (S042 provenance).** The IPA page is dated `最終更新日：2017年5月30日` (L123) with the last update-history
  entry at 2017-05-30 (L207–L208). Any sentence presenting S042 as a 2026-current statement would be a Q4
  attribution error. The landed registry row records the date, and the landed entry's S042 header carries
  `最終更新日 2017年5月30日 (L123)`; both were checked, not assumed.
- **F-2 (staged package id space is stale).** `MERGE-REPORT.md:9` says `lane registry currently holds **30** rows;
  first staged id is **S031**`. At the frozen base the lane already held **41** rows, so staged ids
  **S031–S041 all collide** with lane rows S031–S041 and **none of the 11 URLs match** (measured: staged S031 =
  `hackerone.com/security/policy_versions` vs lane S031 = `cve.org/…/CNA_Rules_v4.2.6.pdf`; intersection of
  matching URLs = empty). Appending `SOURCES.append.md` as the package's checklist step 3 instructs would have
  written 11 wrong-scope rows. Only the two F12 files are in round-28 scope.
- **F-3 (staged S043 ≡ lane S041).** URL equality verified: staged `S043` and lane `S041` are both
  `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf`. Re-registering it would be a Q8/R8 immutable-field
  violation; the frozen plan's "cite, not re-register" is the correct arm, and the landed `used-by` append
  (`old → new` logged in `SOURCES.md` § Registry changes) is the only S041 change.
- **F-4 (staged entry's recheck fails Q10/R12 as written — fixed in the landed entry).** Staged `recheck:` (L7) is a
  prose+command hybrid (`… pdftotext … -` then `then confirm the edition stamp is still 2026年10月`), has no
  `cd <lane-root> &&` prefix, and only re-verifies the **JPCERT PDF** — it never asserts an S042 quote, while the entry
  declares `source: S042` and `source: S043`. The landed entry's `L6` is one `bash -n`-clean command with the lane-root
  prefix and **both** `--source S041` and `--source S042` against `corpus/source-snapshots/round-28/manifest.json`;
  checked, not assumed.
- **F-5 (staged entry's `ground:` is F13 — corrected in the landed entry).** The lane's README numbers this item
  **F12**; the staged text says `ground: F13 (new frontier item; extends F02 …)`. The landed entry's `L7` reads
  `ground: F12 — …` and the README F12 row is admitted, so the pointer resolves.
- **F-6 (staged row fields not carried, correctly).** The staged S042 row has `opened 2026-10-23` (package date)
  while the frozen predicate requires `opened 2026-10-25`; the landed row uses 2026-10-25. The staged row also
  claimed the web-application flow has `steps 1 to 6`; the capture shows **seven** (L162–L182), and a third
  `自社製品の取扱いプロセス` flow exists at L183–L201. The landed row dropped both claims — verified, not assumed.
- **F-7 (was transient; resolved at this writing).** `sources-census.sh validate` exited 1 on E11 ×2 while
  `corpus/knowledge/japanese-domestic-disclosure-workflow.md` was absent; after the entry landed the same command
  exits **0** with only the two pre-existing W04 warnings (§5, final run). The row count was correct at 42
  throughout. Nothing in the registry needed changing: the error cleared because the `used-by` target file appeared.
- **F-7a (entry-side check passed).** The landed entry's S041/S042 headers, `ground: F12`, and the single
  `bash -n`-clean `recheck:` line with both `--source S041` and `--source S042` were spot-checked in §5;
  every quoted anchor inspected (Ⅳ.11 L429, 付録２ L1156, 図３ L1281, 図４ L1331, S042 L133/L144/L159/L184/L200)
  resolves to the line the header names. This does not re-admit the entry — that is the reviewer seats' item.
- **F-8 (manifest is clean).** All 12 landed quote assertions are exactly-once (measured), path stems equal ids,
  both sha256 pins match, `source-recheck` exit 0 — Q9 holds with no anchor required. The non-unique candidates
  in §3 are recorded so a later edit does not silently swap a unique quote for a duplicate.

---

## 8. Limits (what this block does not assert)

- No network freshness claim: `source-recheck` verifies *captured bytes*, not current upstream availability;
  the IPA page's currency is explicitly 2017-05-30, and the JPCERT PDF's is its 2026.09.29 signature.
- `capture-source.py`'s `collapse()` drops blank lines, so every "L###" above is a **capture line**, not a
  printed-page line. Page-level locations (p.45, p.36) are taken from the PDF's own TOC/printed footers
  (TOC L37–L40 lists 付録３ at p.36; L1674 prints `45` on the 図1 page of 付録６).
- **Citation status is two-phase, both measured.** §2's "knowledge path citing it" was, at the time the staged
  section was assembled, the registry's declared target (`used-by`); after `ScribeEntryC2` landed, the citation is
  **observed**: `entries_citing_S042=1` and the census E11 codes cleared (§5). No statement in this block rests on
  the entry's prose — the entry's claims were only spot-checked for anchor resolution (F-7a), not adopted as evidence.
- This seat wrote no production file, ran no VCS write, installed nothing, and spawned nothing. Its only surviving
  write is this file; the two scratch captures it used for the cross-check were deleted after their digests were
  recorded (§4), leaving no duplicate corpus bytes in the lane tree (R14).
