# RevEntryC2 — F12 entry bar-check (round 28, wave 1)

Seat: RevEntryC2 (reviewer). Scope: bar-check `corpus/knowledge/japanese-domestic-disclosure-workflow.md`
against `corpus/QUALITY.md` Q1-Q10 (+ Q4 attribution, Q5 falsifiable-rule-and-rejection), plus the three
end-to-end verifications assigned (captures at cited anchors, recheck from foreign cwd, R12 source-id equality).
Run time: 2026-10-25 UTC (session). Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin.

## 0. State at start (PRE-STATE) and at check time (POST-STATE)

At first read the lane entry did not exist yet, `round-28/manifest.json` was not landed, and the only
object was the staged skeleton at `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`
(read-only). The staged skeleton FAILED the bar in six concrete ways, all of which the landed entry later
fixed (verified byte-level at check time):

| staged skeleton defect | bar violated | fix observed in the landed entry |
|---|---|---|
| `source: S043` (package-local id) | R12/harness-A (declared ids must equal recheck ids; lane id is S041) | header now `source: S041` + `source: S042`, both lane ids |
| `recheck: 180d — curl … && pdftotext …` then confirm… (network fetch, prose+command hybrid, no cd prefix, no manifest) | Q7/Q10/R12/harness-C | `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042` |
| `verified-at: 2026-10-23` (staging date) | Q1 (author re-open date) | `verified-at: 2026-10-25` |
| `ground: F13` | lane frontier row is F12 | `ground: F12 — …` |
| "second six-step flow" for web apps | Q3 accuracy (capture shows seven) | entry says seven, with S042.txt:162-182 and 図４ S041.txt:1331 cited; registry changelog independently refused the staged six-step anchor |
| no quote record with exact locations; no falsifiable rules; no rejected over-generalizations | Q3/Q5 | `## The quoted record` table (30 quotes, each ≤70 chars with capture line), `## Falsifiable rules` (3), `## Rejected over-generalizations` (4) |

Also fixed: the staged skeleton's "Step 5" attribution of the schedule-negotiation sentences pointed at the IPA
page; the landed entry relocated those quotes to the guideline (S041); the IPA page's step 5 is only the 起算日
relay (S042.txt:144-145).
The schedule quotes are NOT in S042; they exist verbatim only in S041 付録2 item 5)/Ⅳ.3) (S041.txt:649-653).

## 1. Criterion table — entry line evidence

| id | verdict | evidence (entry line / object) |
|---|---|---|
| Q1 | PASS | Lines 3-6: two `source:` lines (S041 row id + URL + exact anchors: L340, L648-653, L658-660, L430, L1157, L1281, L1331; S042 page + 最終更新日 L123 + step ranges L133-159/L162-182/L184-200), `verified-at: 2026-10-25`, one executable `recheck:` command naming manifest and both --source ids. |
| Q2 | PASS | All load-bearing claims cite S041 (tier A) and S042 (tier A, opened 2026-10-25). No tier-C support anywhere. |
| Q3 | PASS | `## The quoted record` (lines 49-80): 30 quotes, each verbatim contiguous substring ≤70 chars with an exact capture line + line-number location; all 30 verified verbatim against the capture bytes at the stated lines this session (see §2 for the pinned ones). |
| Q4 | PASS | Claims attributed to the two bodies: "IPA receives the report as the designated intake body, and JPCERT/CC contacts …" (line 11), "states its own role as …" (line 11), "JPCERT/CC defines what that date is" (line 21); rejected-over-generalization 4 explicitly refuses "This is the Japanese standard for coordinated disclosure" — scoped to the 早期警戒パートナーシップ under a METI notification (S042.txt:130). No vendor policy generalized. |
| Q5 | PASS | Three falsifiable rules with checkable commands/quotes (trigger rule L84; scope rule L85 with `grep -c '45 日' corpus/source-snapshots/round-28/S041.txt` → prints `2` — verified, both inside chapter Ⅳ; withdrawal rule L86). Four rejected over-generalizations with reasons (lines 90-93). |
| Q6 | PASS | Documentation-only; both sources read as public documents on 2026-10-25 (line 103); no probing/submission/credential/private-URL content. |
| Q7 | PASS | recheck field is one command, not prose; successful output names what was checked (sha256 OK + per-quote occurrence lines); a pinned captured-source comparison, not a network verification (manifest purpose line 3). |
| Q8 | PASS | No capture markup (`<u>` etc.) is present in any quoted string; the instrument reported raw `OK` (no transformation needed), so nothing to declare. |
| Q9 | PASS | manifest.json: schema_version 1; path stems equal ids (S041.txt/S042.txt); sha256 pins equal actual bytes (S041 e18acbf9…, S042 b432ec16… — re-computed, match); 12 quote assertions, instrument prints `occurrences=1` for all (exactly-once); no non-unique quote is pinned without an anchor (the only duplicate string, 「画面キャプチャ」、, is unpinned and bound by the entry's line number, disclosed in Limits). |
| Q10 | PASS | The recheck line is one executable command (two `source-recheck.py` invocations chained with `&&`), carries its own `cd <lane-root> &&` prefix, and ran with exit 0 from a foreign cwd (verified, §3). |

## 2. Three load-bearing claims — end-to-end (capture line + entry quote)

Claim 1 — 起算日 is anchored on the first attempted contact (footnote 4), not the report/acknowledgement.
- Entry (line 21): "「本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。」 (S041.txt:340)".
- Capture S041.txt:340, verbatim: `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。`
- Footnote-4 identity corroborated by S041.txt:648 (`２．注釈 4 を参照`) and the footnote block position; manifest S041 Q1 pins the string, instrument: `S041:Q1 OK occurrences=1`.

Claim 2 — IPA's step 5 relays the clock both ways: JPCERT/CC's contact-start to IPA, 起算日 + detail-contact date to the finder.
- Entry (line 23): quote pair at S042.txt:145.
- Capture S042.txt:145, verbatim: `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。` — both entry substrings are contiguous substrings; manifest S042 Q1 pins the full sentence, instrument: `S042:Q1 OK occurrences=1`.
- Heading L144 `5.起算日の連絡` verbatim (entry quote at line 56 of the record table).

Claim 3 — the 45-day figure is a 目安 off the 起算日 anchor, with four stated considerations and a five-ground abort list.
- Entry (lines 25): `みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、` at S041.txt:648; considerations `① 対策方法の作成に要する期間` L650 → `④ 当該脆弱性の悪用に関するリスク` L653; `公表日を変更することがあります。` L660; five grounds L662-671.
- Capture S041.txt:648 verbatim identical; L649-653 verbatim (read); L660 verbatim (read); grounds list (ア)-(オ) L664-671 present. Manifest S041 Q4 pins the 45-day string, instrument: `S041:Q4 OK occurrences=1`.

All other record-table quotes (30/30) checked verbatim at their stated capture lines this session; none mismatched.

## 3. Recheck from foreign cwd + R12

- Ran from `mktemp -d` (foreign cwd) the exact `recheck:` line: exit 0, output `S041:sha256 OK`, `S041:Q1…Q6 OK occurrences=1`, `S042:sha256 OK`, `S042:Q1…Q6 OK occurrences=1`.
- R12: declared source ids (header lines 3-4) = {S041, S042}; recheck `--source` ids = {S041, S042}; both ids cited throughout the body; the named manifest lists both. Harness (frontier-recheck-count.py) evaluates the same contract: F12 reported `PASS ids=S041,S042 exit=0`.
- Harness full run: `entries=15 pass=15 exit=0` (matches C2 after-value; README F12 row admitted, row 213).

## 4. Additional verification

- `grep -c '45 日' corpus/source-snapshots/round-28/S041.txt` → `2` (L648, L786), both inside chapter Ⅳ — the falsifiable scope rule's command is truthful.
- S041 round-28 re-capture byte-identical to round-26 (both sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`) — the entry's claim that F11 line anchors still hold is corroborated.
- 図３ contains four 起算日の連絡 boxes (S041.txt:1170, 1171, 1186, 1211); 図４ (S041.txt:1331) has none; 図２ numbers five steps (S041.txt:859-886) vs 図４'s seven — all verified against the capture.
- Web path step count: S042.txt:162-182 numbers seven steps; the entry and the registry both follow the capture (the staged "six-step" was wrong).

## 5. Verdict

**ADMIT-BAR-MET.** Q1-Q10 all pass on line evidence; Q4 and Q5 pass explicitly; the three load-bearing claims are verified
end-to-end (verbatim at cited anchors, recheck exit 0 from a foreign cwd, R12 id equality); manifest pins hold; harness 15/15.

Residual risk / gaps (non-blocking):
- 18 of 30 record-table quotes are not manifest-pinned; their binding is the entry's stated line number, verified by hand this session against the capture bytes. A future capture re-run re-checks only the 12 pinned assertions; the unpinned quotes depend on line stability of the captures.
- The C2 census counter and assimilation-Gate receipts are other seats' items and were not run here; harness and manifest are green.

Nothing left for the L1 to re-run for this seat: the entry, manifest, captures, README row, and registry rows were all present and consistent at check time (the only PRE-STATE gap was timing — the entry/manifest landed before this seat's runs; the staged-skeleton findings in §0 are recorded for the lesson, not as defects of the landed bytes).
