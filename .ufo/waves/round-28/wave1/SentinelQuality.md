# SentinelQuality — quality-bar sentinel receipt (round 28, wave 1)

Seat: SentinelQuality — F12 entry admission-bar sample verification + SKILL.md append-only check.
Scope: read-only inspection of landed bytes; no production edits (only this receipt).
Timestamps UTC. Access dates: 2026-10-25.

## State at check time
- F12 entry `corpus/knowledge/japanese-domestic-disclosure-workflow.md` **landed** (working tree, untracked, 18 456 bytes, 103 lines). L1 re-check: `git status --short corpus/knowledge/japanese-domestic-disclosure-workflow.md` → `??`.
- `corpus/source-snapshots/round-28/S041.txt` (2 354 lines, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`) and `S042.txt` (974 lines, sha256 `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`) landed; `manifest.json` landed (12 quote assertions, all exactly-once).
- `SKILL.md` landed modifications verified (2 added lines, 0 deleted; see §4).

## 1. Random load-bearing claim sample (seed = my own reads)
Three load-bearing claims chosen at random from the landed entry; each quote opened at its cited anchor in the round-28 captures and confirmed verbatim.

| claim | anchor cited | verbatim quote (capture) | verdict |
|---|---|---|---|
| 起算日 definition | S041.txt:340 | 「本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。」 | verbatim, exactly-once |
| 45-day target | S041.txt:648 | 「みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、」 | verbatim, exactly-once |
| one-year withdrawal | S041.txt:305-306 | 「なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、」+「情報非開示依頼の取り下げを求めることができます。」 | verbatim (two lines, one sentence) |

Supporting random checks (all verbatim at cited anchors):
- S041.txt:344 「画面キャプチャ」、 (entry's disclaimer that L929 is the second occurrence — confirmed, exactly 2 occurrences).
- S041.txt:430-431 withdrawal process clause (line-wrap verified).
- S041.txt:650 「① 対策方法の作成に要する期間」 / :653 「④ 当該脆弱性の悪用に関するリスク」.
- S041.txt:1331 図４ caption; :1281 図３ caption; :1157 annex-2 scope sentence.
- S042.txt:130 METI notification sentence; :131 IPA receipt-agency sentence; :144-145 step-5 relay; :159 step 10; :170/171 web step 4; :182 web-step-7 suppression; :200 self-report step 8.
- Claims that depend on *counts*: "45 日" appears exactly 2 times in S041 (L648, L786 — matches entry); 図３ has four 起算日の連絡 boxes (L1170, 1171, 1186, 1211 — matches entry); 図２ overview numbers five steps (S041:859-886 — matches entry); web path has seven steps (S042:162-182 — matches entry; staged draft's "six-step" was corrected); self path eight steps (S042:184-200). All numeric claims match capture lines.

## 2. Universalized attribution (Q4)
No Q4 violations found. Every policy-level claim names its source: "IPA and JPCERT/CC", "IPA dates the arrangement to a Ministry of Economy, Trade and Industry notification", "JPCERT/CC sets…", "The guideline matches". The entry explicitly rejected the over-generalization "This is the Japanese standard for coordinated disclosure" and scopes the guideline to partnership parties. The state-coordinated pipeline claim is grounded in S042:130 (METI 告示) and S042:131, not asserted as a universal truth.

## 3. Memory-typed numbers
All numeric claims in the entry were checked against capture lines (see §1 counts). No number is retyped from memory; e.g. "45 日" quotes the capture's own string, "1 年以上" matches S041:305, figure-step counts match the capture's numbered lists.

## 4. SKILL.md append-only check
`git diff c9f8b115a098c65356e4b3b6048af45a37ab8395 -- SKILL.md`:
- +2 added lines, 0 deleted lines (no rewrite of existing content).
- Hunk 1: insertion of the `anchorcheck.py` instrument-table row after base line 982 (mid-file, inside the  instruments table).
- Hunk 2: end-of-file append (Round-28 note).

**Finding (LOW):** the SKILL.md change is not a strict end-append: the instrument-table row is inserted mid-file (base L983 → wt L984), shifting ~50 downstream lines by +1. R6 ("append at the end; keep every existing line at its number") is not literally met. Impact assessed: the only live committed anchor into the shifted region is `corpus/instruments/resolve-dispatch-fixtures.json` (`SKILL.md:1000`), which resolves to a different line under the shift; but at base that anchor already pointed at a non-brace line (the four-alternative set cited in its `why` is at base L1007, not L1000), so the anchor was already stale before this round and the shift does not break a currently-valid pin. No other live (non-`.ufo/`) file cites SKILL.md lines ≥983. Recommendation for L1 (not in my write scope): note the R6 deviation in the round-28 lesson; if the fixture anchor is meant to pin the four-set, it should have cited L1007 at base or be updated to L1008 now.

## 5. Recheck line (Q7/Q10/Q12) and manifest (Q9)
- Entry recheck line: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042` — one chain, `bash -n` clean, carries `cd`, covers declared header ids, exit 0 from foreign cwd, prints all 12 assertions OK.
- Manifest Q9: both `sha256` pins match real file digests; all 12 quotes exactly-once (occurrences=1); path stem == id.
- Q6 documentation-only: no probing/scanning/logging-in/submitting/touching instructions; no credentials/session/private URLs (URLs are public capture sources); reads-only on public documents.

## Verdict
F12 entry passes the sampled admission bar (Q1-Q6, Q9, Q10, Q12; Q2/Q3 quote fidelity verified verbatim). One LOW R6 deviation in SKILL.md (mid-file insertion; no currently-valid anchor breaks). No fabrication; all checks run on landed bytes.
