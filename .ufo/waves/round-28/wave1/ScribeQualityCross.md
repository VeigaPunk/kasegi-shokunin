# ScribeQualityCross — F12 entry bar check against QUALITY.md

Seat: independent admission check of `corpus/knowledge/japanese-domestic-disclosure-workflow.md`
(Q1–Q10, R1–R6 where applicable, R12) **before it is committed**. No production edit by this
seat; it owns only this file and `.ufo/waves/round-28/receipts/ScribeQualityCross.txt`.

## 0. Object checked

| item | value |
|---|---|
| entry | `corpus/knowledge/japanese-domestic-disclosure-workflow.md`, 103 lines, **sha256 `a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6`** |
| entry bytes | landed 17:26Z as `0261f315…`, revised in place to `a22d2321…` by 17:29Z; the full audit below was **re-run on the later bytes** and every line pointer is identical in both |
| captures | `round-28/S042.txt` 60 508 B / 974 lines; `round-28/S041.txt` 147 267 B / 2 354 lines |
| manifest | `round-28/manifest.json` sha256 `e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d` |
| registry | 42 rows; S041 `:47`, S042 `:48` (both tier A, `mined`, opened 2026-10-25) |
| frontier | 12 admitted rows; F12 at `corpus/README.md:213` |

## 1. Verdict table

| id | verdict | evidence from the landed entry |
|---|---|---|
| **Q1** header trio | **PASS** | `:3` `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — … 注釈4 起算日の定義 (L340), … (L648-653) … (L430) … (L1157, L1281, L1331)`; `:4` `source: S042 — https://www.ipa.go.jp/security/todokede/vuln/process.html — … (L123); ソフトウエア製品 1.–10. (L133-159) … ウェブアプリケーション 1.–7. (L162-182) …`; `:5` `verified-at: 2026-10-25`; `:6` one `recheck:` command; `:7` `ground: F12`. Both ids exist in the registry; every header line number re-checked and correct (`L123` revision stamp, `L144-145` step 5, `L162-182` web path, `L184-200` self path, `L340` definition, `L648-653` 45-day + four factors, `L658-660` date change, `L430` withdrawal, `L1157`/`L1281`/`L1331` annex-2 figures). |
| **Q2** tier-A/B opened this round | **PASS** | Every load-bearing claim rests on S041 or S042 — both tier A, `mined`, `opened 2026-10-25` (`SOURCES.md:47-48`). The single outside citation, `(F02, S004)` at `:43`, is a comparative aside about CERT/CC's interval and is already supported inside its own admitted entry (`coordinated-disclosure-timelines.md:22`, verbatim 45-day quote). No tier-C row is load-bearing. |
| **Q3** verbatim + exact location ≤25 words | **PASS** | 30 quote rows audited mechanically: **30/30 occur on the stated capture line**, **29/30 exactly-once**, longest 49 characters / 5 words (the lane's admitted convention, see F11). Numbers checked against the captures, not memory: `45 日` in 2 lines (`S041.txt:648, 786`), one-year rule at `:305/:430`, step counts 10 / 7 / 8 at `S042.txt:133-159`, `:162-182`, `:184-200`. |
| **Q4** attribution, no universalizing | **PASS, one residual** | Attribution is explicit and correct: "It is IPA's and JPCERT/CC's operation of the 早期警戒パートナーシップ under a METI notification" (rejected over-generalization 4, `:93`), and the legal annex is scoped to the partnership's finders/developers/operators. **Residual (F3):** the opening sentence still reads "Japan's vulnerability intake is a state-coordinated pipeline … There is no bounty and no per-finding severity ratchet" (`:11`) — the "no bounty" clause is unquoted and, read literally about Japan, is falsified by this lane's own S037 (サイボウズ 脆弱性報奨金制度 FAQ, tier A, `SOURCES.md:43`). |
| **Q5** falsifiable rule + rejected over-generalization | **PASS** | Three rules (`:84-86`) each carry a check, and rule 2 carries a runnable command whose output this seat reproduced: `grep -c '45 日' corpus/source-snapshots/round-28/S041.txt` → `2`. Four rejected over-generalizations (`:90-93`), each with the falsifying capture line. |
| **Q6** documentation-only | **PASS** | No probing/submission instruction; no credential, session or private URL; no op-scheme vault URI. The only URLs are the two public documents in the header (`:3-4`). |
| **Q7** executable recheck, names what it checked, a control must fail | **PASS** | Measured run prints 14 lines naming exactly what it checked — `S041:sha256 OK`, six `S041:Qn OK occurrences=1`, then the same for S042 — exit 0. The missing/corrupted-source control is the instrument's own `--selftest` (ExecInstrSelftest receipt), correctly left out of the entry rather than asserted in prose. |
| **Q8** declared normalization | **PASS** | Nothing in the entry needs a normalization excuse: all 12 manifest assertions match the captures **raw** (measured), all 30 entry quotes matched on their raw lines, and the two quotes that touch a PDF line wrap stop before it (`jpcert-withdraw-process` at `S041.txt:430` ends at `…情報非開示依`; the `jpcert-annex2-scope` quote at `:1157` likewise). |
| **Q9** stem==id, exactly-once or anchor, count printed | **PASS, two label corrections** | Manifest side: `S041→S041.txt`, `S042→S042.txt`, both sha256 pins match, 12/12 assertions `occurrences=1`, no anchor required, instrument prints the count. Entry side: 29/30 quotes exactly-once; `jpcert-finder-evidence` ("「画面キャプチャ」、") occurs 2× (`S041.txt:344`, `:929`) and the entry **carries the anchor and discloses the fork** in Limits (`:100`), which is precisely Q9's requirement. **But two `manifest pin` cells are false** — see **F1**. |
| **Q10** one command, `bash -n`, own `cd` | **PASS** | One line; `bash -n` exit 0; runs from the lane root **and** from `/` with byte-identical output (stdout sha256 `dbb21ba593e35996718b23b761646deaab4280ce9c622b95f5dd09d70135b6ac`, both exit 0). |
| **R1** live-tree claims carry as-of | n/a | The entry asserts no live tree or service; capture paths are committed files. |
| **R2** self-description is a claim | **PASS, one nit** | Commands and counts in the prose all reproduce (§3). **F4:** the Limits pointer `corpus/instruments/source-recheck.py:275` lands on `def main(argv=None):`; the `--source` declaration the sentence is about is `:277`. The claim itself is true — `add_argument("--source", …)` is single-valued, so a repeated flag would silently keep only the last id. |
| **R3** verdict names matcher/definition | **PASS** | The recheck names the instrument and its semantics (pinned sha256 + exactly-once), and the entry states the one-`--source` limitation with a code pointer. |
| **R4 / R5 / R6** | n/a | Round-record and lesson criteria (L1 / ScribeLesson); R6 is satisfied trivially — the file is new, so no existing `path:line` anchor points into it. The append obligations fall on `README.md` (ScribeReadmeC2) and `SOURCES.md` (ScribeRegistryC2), both of which appended rather than inserted (F12 at `:213`, S042 at `:48`, F11's `:212` and S041's `:47` unchanged). |
| **R12** recheck belongs to this entry | **PASS** | Declared ids `{S041,S042}` = recheck ids, both cited in the body, manifest lists both; the harness's A–D contract passes (`ids=S041,S042 exit=0`). |

**Admission recommendation: PASS on Q1–Q10, R2, R3, R12.** Nothing blocks admission. Four
corrections below are cheap and should land in the same commit.

## 2. Quote audit — all 30 rows, measured

Method: parse the `## The quoted record` table, then for each row test the quoted string
against the named capture line (whitespace-collapsed comparison) and count its occurrences
across the whole capture.

```
rows=30  on_stated_line=30  exactly_once=29  forked_with_disclosed_anchor=1
max_chars=49  max_words=5   rows_over_70_chars=0
forked: jpcert-finder-evidence "「画面キャプチャ」、" 2× (S041.txt:344, :929) — anchor disclosed at entry:100
```

Every header anchor and every in-body line citation resolved (§1 Q1, plus `:130`, `:131`,
`:142`, `:143`, `:144`, `:145`, `:153`, `:159`, `:168`, `:170`, `:171`, `:178`, `:179`,
`:182`, `:200` for S042; `:305`, `:306`, `:340`, `:344`, `:430`, `:648`-`:653`, `:660`,
`:856`, `:859`-`:886`, `:929`, `:1157`, `:1170`, `:1171`, `:1186`, `:1211`, `:1281`,
`:1331`, `:1338` for S041).

## 3. Gates run on the landed bytes

| gate | command | result |
|---|---|---|
| recheck (lane) | `eval "$(sed -n 's/^recheck: //p' <entry>)"` | **exit 0**, 14 `OK` lines |
| recheck (foreign cwd) | same line with `cd /` first | **exit 0**, same stdout hash |
| Q7/R12 harness | `python3 corpus/instruments/frontier-recheck-count.py` | **`entries=15 pass=15 exit=0`**; row `PASS F12 knowledge/japanese-domestic-disclosure-workflow.md ids=S041,S042 exit=0` |
| census (C2 after) | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **exit 0**; 42 rows; only the pre-existing `W04 S028`, `W04 S029` |
| expected-list completeness | `python3 corpus/instruments/recheck-audit.py --foreign /` | **exit 1** — but the entry is not the cause: `lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0`, and `expect=present expected=39 missing=0 unexpected=1` |
| C2 counter 1 | admitted frontier rows | `12` (after value) |
| C2 counter 2 | `grep -lE '^source: S042 ' corpus/knowledge/*.md \| wc -l` | `1` (after value) |
| C2 counter 3 | S042 registry rows | `1` (after value) |
| C2 counter 4 | frontier harness | `entries=15 pass=15 exit=0` (after value) |

All four frozen C2 counters now sit at their `after` values on the landed entry.

## 4. Findings needing a correction

**F1 (Q9 — the only substantive defect). Two `manifest pin` cells name assertions that do not
pin those quotes.**

| row | entry line | says | landed manifest actually holds | fix |
|---|---|---|---|---|
| `ipa-product-step5-head` | `:56` | `Q1 (heading)` | `S042:Q1` = the **L145 body sentence**, not the heading `5.起算日の連絡`; and that heading is 8 characters, below the instrument's `MIN_QUOTE_CHARS = 12`, so it can never be a valid assertion | change the cell to `—` |
| `jpcert-withdraw-verb` | `:75` | `Q6 (continuation)` | `S041:Q6` ends at `S041.txt:305` (`…発見者は IPA に対し、`); the cited string is on `:306`, which no assertion pins | change the cell to `—` |

Three neighbouring cells (`Q1 (first half)`, `Q1 (second sentence)`, `Q5 (second sentence)`)
are prefix/suffix of the pinned assertion — true, but the pin binds the whole string, not the
fragment; they are accurate only if read as "fragment of the pinned assertion". Optional
rewording: `Q1 (fragment)`.

Why this is not an admission blocker: the instrument never reads `manifest.json`'s `location`
or the entry's pin column, so no verdict moves. It is a false claim under R2's rule that
self-description is a claim, and it is exactly the direction the round is trying to close.

**F2 (dependency — not the entry's file). `corpus/source-snapshots/round-28/manifest.json`
`S042:Q2.location` says "step 4, line 142 (L142)"; the quote is at `S042.txt:131` (the page
introduction), and L142 belongs to `S042:Q4`.** The entry independently cites the correct line
(`:52`), so the entry is right and the manifest metadata is wrong. Owner: ExecManifest.

**F3 (Q4 residual). Scope the "no bounty" clause.** `:11` reads "Japan's vulnerability
intake is a state-coordinated pipeline, not a marketplace … There is no bounty and no
per-finding severity ratchet." The pipeline claim is sourced (`S042.txt:130-131`); the "no
bounty" clause is not, and about Japan it is false (S037). Fix: "The partnership's intake path
carries no bounty and no per-finding severity ratchet", optionally citing S037 — which also
turns the clause into a second Q5-style rejected over-generalization at no cost.

**F4 (R2 nit).** `:101`'s code pointer `source-recheck.py:275` should be `:277`
(`parser.add_argument("--source", …)`); `:275` is `def main`.

**F5 (dependency — blocks the round's expected-list gate, not the entry).**
`corpus/instruments/knowledge-expected.txt` still lists 39 entries; the tree now has 40, so
`recheck-audit` exits 1 with `unexpected=1` even though all 40 recheck lines pass. ExecExpectedList
measured PRE-STATE at 17:23Z and explicitly did not regenerate. Fix: append
`corpus/knowledge/japanese-domestic-disclosure-workflow.md` in sorted position, then

```bash
python3 corpus/instruments/recheck-audit.py --foreign /   # expect expected=40 … exit 0
```

## 5. What moved during this seat's run

The entry was **absent** for most of the run (PRE-STATE) and I first graded the staged
skeleton (`/home/vgpnk/Projects/shokuknow/merge/kasegi/…`, read-only). That draft would have
been rejected: it carried staged id `S043` (no such lane row), `verified-at: 2026-10-23`, a
prose `recheck:` that fails `bash -n`, `ground: F13`, a 9-step product flow and a "six-step"
web path (the captures say 10 and 7), no capture line anchors, no falsifiable rule, and the
unqualified "no bounty" claim. **The landed entry fixes all of them** — it cites S041/S042,
numbers both flows from the captures, anchors all 30 quotes, adds three rules and four
rejections, and records the staged-vs-lane discrepancies itself in Limits (`:102`).

One target moved mid-run and is recorded for the canonical judge: at 17:23Z the manifest's
`S042:Q1` was `"5.起算日の連絡"` (normalized length 8) and `source-recheck.py` exited 2 with
`S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`; the bytes were rewritten at
17:24:14Z to the 93-character L145 sentence and the run is exit 0. Every verdict above uses
manifest digest `e62ddad1…` and entry digest `a22d2321…`; the quote audit, the C2 counters and
the three gates were re-run on those bytes after the entry's 17:29Z revision and are unchanged.

## 6. Out of scope, conflicts, evidence volume

- **Not checked by this seat:** C1 (`anchorcheck.py`) — separate author/axis; the S042/S041
  registry rows' field-by-field correctness beyond the facts this item depends on (tier, status,
  opened date, used-by); the F12 README wording; the assimilation Gate quotes.
- **Conflict for the canonical judge:** the round-28 dispatch names `source: S041` +
  `source: S042`; the staged skeleton wrote `S042` + `S043`. The landed entry resolved this the
  way the dispatch requires (staged S043 → lane S041 by document). No second reading survives.
- **A contradiction inside the lane, reported verbatim:** `recheck-audit.py` returns exit 1
  while printing `lines=40 total=40 pass=40 … paths_fail=0`; the red is the expected-list
  equality (`unexpected=1`), not any entry's line. Do not read that exit 1 as an entry failure.
- **Evidence volume (R14 practice):** this seat wrote one markdown file and one receipt — no
  control trees, no corpus copies, no tarballs.

## Revisions

- 2026-10-25T17:31Z: rewritten from PRE-STATE to the landed-entry check; re-audited at 17:30Z
  on entry sha256 `a22d2321…` and manifest sha256 `e62ddad1…`. All quotes, counters and gate
  values in this file were measured on those bytes, and every cited entry line number resolves
  on them.
