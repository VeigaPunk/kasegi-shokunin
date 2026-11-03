SCOPE CLEAR — no sibling PROVINCE.md or sibling corpus claims the Big Sleep tracker or the Project Zero trial ground, and F40 Claim 2 does not re-count S017; one held-ground attribution sentence in F40 Claim 4 is overstated (recommendation R1).

# SiblingOverlap — kasegi round 59, wave w1, seat SiblingOverlap (leaf, no subagents)

Lane HEAD `472737847ff31d1255bf1a0745822a5e878e9622`; frozen claims commit `00b535758d2cfa4511cda7167b67cdc045b85fb4`. Read-only throughout; nothing under the lane was written. Scratch directory was created, used for three temp files, and removed (no leftovers).

Tools installed or upgraded by this seat: none. Only pre-existing `grep`, `sed`, `git` (read-only), `python3` (manifest JSON read).

Commands beyond the item's named list (disclosed): the lane's `frontier-recheck-count.py` and `source-recheck.py --source S092` (read-only, both are C2 counting commands; run once each to confirm the held rows), plus read-only `git show/diff/status/log`.

## 1. Sibling PROVINCE sweep (Change step 1)

Command: `grep -n -i -E "Big Sleep|issue tracker|disclosure trial|Project Zero" /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` — exit 0. Output (decisive line):
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md:207: [r59 Frontier amendment …] F40 — Google Big Sleep public findings tracker … scope limit: the tracker README's own statements only — the Project Zero trial text stays S017's ground (corpus/knowledge/pz-reporting-transparency-trial.md) …`

That is the only hit in all 21 PROVINCE.md files (kasegi plus 20 siblings).

Per-file count: `for f in /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md; do printf "%s %s\n" "$(grep -c -i -E 'Big Sleep|issue tracker|disclosure trial|Project Zero' "$f")" "$f"; done` — kasegi-shokunin = 1, the other 20 = 0. Per-pattern totals (`grep -c -i -F` per pattern across the 21 files): "Big Sleep" 1, "issue tracker" 1, "Issue Tracker" 1 (same line 207), "disclosure trial" 0, "Project Zero" 1 (line 207).

Broader sweep: `grep -n -i -E "tracker|issuetracker|bigsleep" /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md | grep -v kasegi` — exit 0 from the pipeline. Output: `kake-shokunin/PROVINCE.md:241` and `:284`, both the IETF word "datatracker" in a web-standards context, not this ground.

Adjacent disclosure/bounty wording in siblings (none claims F40 ground):
- `chousa-shokunin/PROVINCE.md:10`: "Refuses: bounty-program scope and claim packages (→ kasegi)".
- `kake-shokunin/PROVINCE.md:291`: "report intake, triage, remediation, disclosure timing, bounty and policy operation … are not kake's ground".
- `revenger-shokunin/PROVINCE.md:9-12`: bounty triage enters only through `corpus/training/bounty-triage/MODULE.md`; artifact triage, "disclosure outside the program channel" stay outside revenger. Adjacent to kasegi's bounty ground, but about artifact triage, not a tracker README.
- `kengaku-shokunin/PROVINCE.md:307`: "disclosure" refers to its own round-38 TB2 probe ordering; unrelated.

## 2. Sibling corpora sweep (outside PROVINCE.md)

- `grep -rn -i -l -E "Big Sleep|Project Zero" /home/vgpnk/Projects/shokunin/*-shokunin/ 2>/dev/null | grep -v kasegi | head -20` — one file: `tabi-shokunin/.ufo/waves/round-33/w1/ScribeSrcSandbox/fetch/sandbox.md:403`, a link to a 2015 Project Zero post ("in-console-able"). Not Big Sleep, not the trial.
- `grep -rn -i -l -E "issuetracker\.google\.com|goo\.gle/bigsleep|430375499|7155917" … --include=*.md --include=*.txt --include=*.json` (non-kasegi) — no files printed. (Pipeline exit 0 came from `head`.)
- `grep -rn -i "issuetracker" /home/vgpnk/Projects/shokunin/*-shokunin/corpus/` (non-kasegi) — six lines, all Chromium/Android component links, none the Big Sleep component: `mori-shokunin/corpus/evidence/sources-r67/S578.html:4887,4904` (componentid=1400680); `revenger-shokunin/corpus/snapshots/dex-format.html:8642,8755` (componentid 190923, 191476); `tabi-shokunin/corpus/evidence/round-24/sources/bfcache.html:3021,3038` (componentid=1400680).
- `grep -rn -i "Big Sleep" /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/ | grep -v kasegi` — no output.

Conclusion for sweep: no sibling lane holds Big Sleep, the Big Sleep tracker, or the PZ trial. No contested scope exists, so the PROTOCOL contested-scope rule (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:457-461`) is not triggered and no ruling is needed.

## 3. F40 Claim 2 re-count test (Change step 2)

Entry: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/google-big-sleep-findings-tracker.md`.

Command A: `grep -n -i -E "90-?day|90\+30|notice milestone|three facts|upstream patch gap|public notice|disclosure of existence" <entry>` — no output, exit 1. None of the S017 trial content terms (the 90-day deadline, the 90+30 model, the notice milestone, the three-fact notice list, the upstream gap) appears in F40.

Command B: `grep -n -i -o trial <entry>` — hits at lines 32, 35, 36, 37, 38, 79, 80 only. Line 32 is the Claim 2 heading; 35-38 are Claim 2 text; 79-80 are the Limits held-ground pointer. Line 37 says the trial "itself is held ground: corpus/knowledge/pz-reporting-transparency-trial.md (source S017) already records that Big Sleep joins the Project Zero trial (S017.txt L28)". Line 38 is the same sentence's tail. This is a cross-reference to S017, not a re-derivation.

S017 entry Big Sleep mentions: `grep -n "Big Sleep" corpus/knowledge/pz-reporting-transparency-trial.md` → lines 18, 20, 87, 98, 108, 125, 134 (the L28 quote, "no coverage beyond" limit, the falsifiable rule, the "not Google" rejection). The F40 entry re-states none of them.

Decision on Claim 2: F40 does not re-count the trial ground. The only S017 sentence it touches is the L28 participation fact, which it cites as held.

## 4. S017 L28 pointer versus F40 Claim 1 (observation, not a re-count)

- `grep -n "goo.gle/bigsleep" corpus/source-snapshots/round-40/S017.txt` → line 28: "…will also be trialling this policy for their vulnerability reports. The issue tracker for Google Big Sleep is at goo.gle/bigsleep". Exit 0.
- The S017 knowledge entry does NOT record the tracker pointer: its Big Sleep lines (step 3) do not mention the tracker or goo.gle.
- F40 Claim 1 (entry lines 19-30): `grep -c S017` over those lines → 0. Claim 1 verifies the destination (goo.gle/bigsleep → savedsearches/7155917 via the opens receipt) and cites the Leads bullet `corpus/SOURCES.md:141` instead of S017 L28.

Reading: the destination check is new ground; the pointer's first appearance is held (S017 L28), and F40 does not cite that line where it first relies on it. Citation gap, no double count.

## 5. F40 Claim 4 held-ground attribution (defect; the recommendation)

F40 entry lines 61-62 read: "…linking https://googleprojectzero.blogspot.com/2024/06/project-naptime.html beside https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html (S092.txt:2) — the documents S010 already mines (F04)."

Checks:
- `grep -c "from-naptime-to-big-sleep" corpus/source-snapshots/round-24/S010.txt` → 0 (exit 1). `grep -c -i "Big Sleep" …S010.txt` → 0.
- S010 capture lines 1 and 12 carry the title "Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models"; line 13 carries "2024-Jun-20".
- `grep -c "from-naptime-to-big-sleep" corpus/knowledge/ai-assisted-finding-validation.md` → 0; `grep -c "2024/10"` → 0. F04's S010 evidence is at lines 22-23 ("Perfect Verification", "Conclusions").
- `grep -c "from-naptime-to-big-sleep" corpus/SOURCES.md` → 0 (exit 1).
- `grep -rn -l "from-naptime-to-big-sleep" corpus/knowledge/` → only `google-big-sleep-findings-tracker.md`.

So only the 2024/06 Naptime document is S010/F04 ground. The 2024/10 "From Naptime to Big Sleep" document is linked by the S092 README (`S092.txt`, 5 occurrences of the URL in the single JSON line) and held by no registry row. "The documents S010 already mines" is therefore overstated for one of the two links. F40 does not state Naptime findings, so this is attribution, not a re-count.

Identity note (not verified): S010's registry URL is `projectzero.google/2024/06/project-naptime.html`; F40's link is `googleprojectzero.blogspot.com/2024/06/…`. I did not check that the two hosts redirect to the same article; the title and date match (step 5, lines 1, 12, 13).

## 6. Held rows F04 and F26 (Change context)

- F40 vs F04 (validation method): `grep -n -i -E "perfect verification|validation|independent agent|reproducib|NCSC" <entry>` → line 81 only (the Limits pointer "the AI-assisted-finding-validation method stays F04"). No re-count.
- F40 vs F26 (VRP customer-resource boundary): `grep -n -i -E "disqualifying|do not test|multi-tenant|customer resource|bounty" <entry>` → no output, exit 1. F26 appears only as a pointer at line 30 ("Google Cloud VRP rules (S069, F26)"). No re-count.

## 7. Counters and registry (read-only; outside the item's named list, disclosed above)

- `python3 corpus/instruments/frontier-recheck-count.py` → `FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92`; `FRONTIER-PASS F40 ids=S092`; `entries=43 pass=43 exit=0`.
- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092` → `S092:sha256 OK`; `S092:Q1` through `Q10` each `OK occurrences=1`; exit 0.
- `sha256sum corpus/source-snapshots/round-59/S092.txt` → `048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38` (matches the frozen digest).
- S092 capture contains "Findings from the project will be publicly disclosed following" once (Q2).
- S092 registry row `corpus/SOURCES.md:99`: "…not Google's researcher intake and not the held Project Zero trial text (S017)".

## 8. Lead bullet and implementation diff (observations; frozen)

- `git diff 472737847ff31d1255bf1a0745822a5e878e9622~1 472737847ff31d1255bf1a0745822a5e878e9622 -- corpus/SOURCES.md` → one insertion (`+| S092 …`), zero deletions. Exit 0.
- `grep 'Google Big Sleep reporting beyond the tracker' corpus/SOURCES.md | sha256sum` → `3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432`; identical at base `472737847~1`. Matches the frozen C2 lead-line sha.
- Observation: `corpus/SOURCES.md:141` still reads "the referenced tracker at https://goo.gle/bigsleep was not opened" under "Leads (unopened)". It is now stale after admission. The C2 kill rule freezes its sha, so it is recorded here, not recommended for edit.

## 9. Lane tree state (scope note)

`git status --porcelain` on the four F40 paths (entry, SOURCES.md, README.md, PROVINCE.md) → empty (committed). The lane tree has other uncommitted changes (`M LOG.md`, `M SCORECARD.md`, `M corpus/QUALITY.md`, untracked `.ufo/waves/round-57|58|59` files). Not examined; outside F40.

## Recommendation (one)

R1 (text only, for the lane owner): in `corpus/knowledge/google-big-sleep-findings-tracker.md` lines 61-62, replace "the documents S010 already mines (F04)" with wording that attributes only the 2024/06 Naptime document to S010/F04 and states that the 2024/10 "From Naptime to Big Sleep" document is linked by the S092 README and held by no registry row. Whether entry bytes may change under the C2 freeze is the lead's decision; this seat does not edit.

## Limits

- No live network check: the goo.gle redirect and the blogspot/projectzero host equivalence are from captured files, not re-fetched.
- Sibling PROVINCE and corpus sweeps are grep-based; a non-matching synonym (e.g., "bug tracker", "Big Sleep" written differently) would not appear. Searched terms were chosen from the F40 entry and its S092 capture.
- Verdict SCOPE CLEAR is about cross-lane overlap. It is not a judgment of the F40 entry's accuracy beyond the Claim 4 attribution finding.
