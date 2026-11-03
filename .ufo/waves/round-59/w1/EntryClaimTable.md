PASS WITH CORRECTIONS (27 rows: 23 GROUNDED, 3 OVERREACH, 1 UNGROUNDED; corrections C-1 to C-5 below, text only, entry not edited)

# EntryClaimTable — F40 entry claims 1-4 at 472737847ff31d1255bf1a0745822a5e878e9622

Scope: corpus/knowledge/google-big-sleep-findings-tracker.md, Claims 1 to 4 (every sentence asserting a fact about the tracker, the README, the policies, the fields or the dates). Frozen-sentence rules ("Falsifiable rule", "Rejected over-generalization" clauses) are methodology, not facts about the world, and are excluded; a negative assertion ("the README grants no intake") is included and graded by absence. Pinned quotes are from corpus/source-snapshots/round-59/manifest.json (sources[0].quotes, Q1-Q10). Capture is corpus/source-snapshots/round-59/S092.txt, single body line L2.

## Table

| claim id | short sentence | quote id | capture line | status | note |
|---|---|---|---|---|---|
| 1.0 | Tracker is the collection point of Big Sleep's disclosed findings; the short link in Project Zero's lead resolves to it | NONE | L2 (Q3) + S017 L28 + receipt | GROUNDED | composite: Q3 "found here" link; S017.txt L28 "The issue tracker for Google Big Sleep is at goo.gle/bigsleep" (round-40 capture); receipt control line 64 |
| 1.1 | README names its subject: issue "[Big Sleep] README" | Q1 | L2 | GROUNDED | occurrences=1 |
| 1.2 | README states "All issues reported by the project so far can be found [here](https://goo.gle/bigsleep)" | Q3 | L2 | GROUNDED | occurrences=1 |
| 1.3 | Recorded Leads bullet on the tracker, bytes unchanged this round | NONE | SOURCES.md:141 | GROUNDED | sha256 of the bullet line equals base 69de8d3 and HEAD 4727378 (3ed4f54d...a432) |
| 1.4 | Opens receipt records goo.gle/bigsleep returning HTTP 200 at final URL savedsearches/7155917 | NONE | receipt, not S092 | GROUNDED | controls/s092-opens-r59.txt:64 "code=200 final=https://issuetracker.google.com/savedsearches/7155917" |
| 1.5 | ... "the tracker's saved search for the project" | NONE | receipt, not S092 | OVERREACH | the receipt proves the redirect target only; the saved-search shell the instrument fetched contains 0 "Big Sleep" and 0 "savedsearches/7155917" strings (controls/s092-opens-r59.txt:42-44; controls/s092-savedsearch-shell.html); the content "for the project" is not verified. See C-1 |
| 1.6 | README grants no intake; nothing in it invites researchers to file findings into this tracker | NONE | L2 (absent) | GROUNDED | by absence: L2 contains 0 "intake", 0 "submit"; full README body read (readme_tail, body.md, E8) |
| 1.7 | Researcher-intake surfaces remain S072 (bug-hunters) and S069/F26 (Cloud VRP), not this README | NONE | n/a (registry) | GROUNDED | SOURCES.md:78 (S072), SOURCES.md:75 (S069), corpus/README.md:628 (F26) |
| 2.1 | README commitment: "Findings from the project will be publicly disclosed following [Google's industry standard disclosure policy]" | Q2 | L2 | GROUNDED | occurrences=1 |
| 2.2 | README names Project Zero's 2025 policy and disclosure trial at googleprojectzero.blogspot.com/2025/07/reporting-transparency.html | NONE | L2 (unpinned) | GROUNDED | true in L2 but not pinned: Q2 ends at "policy]"; "Project Zero's 2025 policy and disclosure trial" count=1 and the URL count=5 in L2 (E17). See C-2 |
| 2.3 | Trial is held ground: pz-reporting-transparency-trial.md (S017) records that Big Sleep joins the trial (S017.txt L28) | NONE | n/a (S017) | GROUNDED | corpus/knowledge/pz-reporting-transparency-trial.md:18 quotes S017.txt L28; round-40 S017.txt L28 text confirmed (E9) |
| 2.4 | The tracker's own statement binds Big Sleep's published findings to both named policies | Q2 | L2 | GROUNDED | the L2 body reads "following [Google's ...] and [Project Zero's 2025 policy ...]" (E2); "binds" is the entry's gloss on that commitment |
| 2.5 | Not a disclosure deadline (no interval in the README); does not modify the policies it names | NONE | L2 (absent) | GROUNDED | by absence: L2 contains 0 of days/hours/week/month/year/deadline (E8) |
| 3.1 | Capture serves the tracker's field definitions beside the README | NONE | L2 | GROUNDED | field definitions at L2 [0][1][22][14][1..5] (Fixed, Impact, Product, Reported, Vendor) (E13) |
| 3.2 | Field "Impact of the vulnerability" | Q4 | L2 | GROUNDED | occurrences=1 |
| 3.3 | Impact value list ["High","Medium","Low","None"] | Q7 | L2 | GROUNDED | occurrences=1; def [0][1][22][14][2] |
| 3.4 | Field "Software product the vulnerability was found in" | Q5 | L2 | GROUNDED | occurrences=1 |
| 3.5 | Field "Date when the bug was reported" | Q6 | L2 | GROUNDED | occurrences=1 |
| 3.6 | Field "Date when the bug was fixed" | Q8 | L2 | GROUNDED | occurrences=1 (served text is "...fixed by the vendor"; Q8 is its substring) |
| 3.7 | "This is the per-finding metadata contract the tracker itself serves for Big Sleep reports." | NONE | L2 | OVERREACH | the definitions sit on the README issue 430375499 record itself (E13); the capture holds no finding issue, so "per-finding" and "for Big Sleep reports" are not shown. See C-3 |
| 3.8 | Impact is "the tracker's coarse triage field, not a severity system" | NONE | L2 | UNGROUNDED | "coarse triage" appears nowhere in S092; the capture says only "Impact of the vulnerability" with four values. See C-4 |
| 3.9 | Not CVSS (F01), not a severity ladder (F13), not Immunefi VSCS (F17); defines no reward | NONE | L2 (absent) + registry | GROUNDED | corpus/README.md:202 (F01), :264 (F13), :361 (F17); L2 contains 0 "CVSS", 0 "severity", 0 "reward" (E8) |
| 4.1 | Issue record's Reported value is "2025-07-08" | Q9 | L2 | GROUNDED | occurrences=1; value at L2 [0][1][22][2][14][0][9], field id 1456622 = "Reported" (E12) |
| 4.2 | Further-reading list opens with "Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models" | Q10 | L2 | GROUNDED | occurrences=1; first bullet of the README list |
| 4.3 | Reading list links googleprojectzero.blogspot.com/2024/06/project-naptime.html beside .../2024/10/from-naptime-to-big-sleep.html | NONE | L2 | GROUNDED | both URLs present in L2 README bullets (E2) |
| 4.4 | "— the documents S010 already mines (F04)" | NONE | n/a (registry) | OVERREACH | S010 is projectzero.google/2024/06/project-naptime.html (SOURCES.md:16), a different host from the blogspot 2024/06 URL; the 2024/10 "From Naptime to Big Sleep" post appears in no source row (E10); F04 cites S010 only (ai-assisted-finding-validation.md:22,23,39). See C-5 |
| 4.5 | Date and links date the example issue and reading list, not the project's start; capture does not say when Big Sleep began | NONE | L2 (absent) | GROUNDED | by inspection: the only dates in L2 are the Reported value 2025-07-08 and epoch timestamps (1752013968 = 2025-07-08T22:32:48Z; 1752176286 = 2025-07-10T19:38:06Z; 1776341538 = 2026-04-16T12:12:18Z); none is a project-start claim (E14) |

Status count (from the table): GROUNDED 23, OVERREACH 3 (1.5, 3.7, 4.4), UNGROUNDED 1 (3.8). Total 27 rows.

## Corrections (text only; the entry is not edited)

- C-1 (row 1.5): replace "the tracker's saved search for the project" with "the saved search URL the goo.gle redirect lands on (savedsearches/7155917); the saved search's content was not verified, because the fetched shell carries no Big Sleep text."
- C-2 (row 2.2): the Project Zero 2025 policy link is grounded in L2 but not pinned. Pin it as an 11th manifest quote (proposed text: "[Project Zero's 2025 policy and disclosure trial]") so the recheck covers it. Manifest change is a proposal only.
- C-3 (row 3.7): replace "This is the per-finding metadata contract the tracker itself serves for Big Sleep reports." with "These are the field definitions carried on the README issue 430375499 record; the capture holds no finding issue, so the per-finding template is not shown."
- C-4 (row 3.8): delete "coarse triage field". Replace with "The four-value enum is the value list the README record serves for Impact; the capture does not say how the field is used."
- C-5 (row 4.4): replace "— the documents S010 already mines (F04)" with "; S010 (SOURCES.md row S010, projectzero.google host) covers the 2024-06 Naptime post only. The 2024-10 post is in no admitted source row, and the blogspot URL is not verified as the same document as S010's URL."
- Outside claims 1-4 (Attribution section, noted for the reviewer): "kept in the tracker's Big Sleep component" is UNGROUNDED. L2 has no component name; component id 1836411 appears (E12), and "Big Sleep" appears only as the value of the Product field (id 1457392). Proposed text: "filed under component id 1836411 and carrying Product value 'Big Sleep'."

## Word counts (R56: wc -w on each pinned quote's text, manifest sources[0].quotes)

| quote | words | limit 25 |
|---|---|---|
| Q1 | 3 | ok |
| Q2 | 11 | ok |
| Q3 | 12 | ok |
| Q4 | 4 | ok |
| Q5 | 7 | ok |
| Q6 | 6 | ok |
| Q7 | 1 | ok |
| Q8 | 6 | ok |
| Q9 | 1 | ok |
| Q10 | 10 | ok |
| total | 61 | max 12 |

## Evidence (commands and printed output; exit codes in brackets)

E1. sha256 and size of the capture (matches manifest sha256 048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38 and bytes 6371):
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -c corpus/source-snapshots/round-59/S092.txt && sha256sum corpus/source-snapshots/round-59/S092.txt`
  -> `6371 corpus/source-snapshots/round-59/S092.txt` / `048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38  corpus/source-snapshots/round-59/S092.txt` [0]

E2. L2 extracted to scratch (L2.txt, 6365 chars). Command: `python3 -c "lines=open('corpus/source-snapshots/round-59/S092.txt',encoding='utf-8').read().split('\n'); open(S+'/L2.txt','w',encoding='utf-8').write(lines[1])"` [0]. README body quoted in the tail of L2 reads: "Big Sleep is a collaboration between Google Project Zero and Google DeepMind ... Findings from the project will be publicly disclosed following [Google's industry standard disclosure policy](https://about.google/company-info/appsecurity/) and [Project Zero's 2025 policy and disclosure trial](https://googleprojectzero.blogspot.com/2025/07/reporting-transparency.html). All issues reported by the project so far can be found [here](https://goo.gle/bigsleep). ... * [Project Naptime: ...](https://googleprojectzero.blogspot.com/2024/06/project-naptime.html) * [From Naptime to Big Sleep: ...](https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html)" (decoded from the `\u003c` HTML-escaped body string in L2).

E3. Word counts: `python3 -c` over manifest quotes, and `printf '%s' "$rest" | wc -w` per quote from a quotes.txt regenerated from the manifest; output Q1 3, Q2 11, Q3 12, Q4 4, Q5 7, Q6 6, Q7 1, Q8 6, Q9 1, Q10 10; whole-file `wc -w` 71 including the 10 id tokens, so 71 - 10 = 61 [0].

E4. Each pinned quote occurrence in L2 (raw and whitespace-normalized, markup stripped): occ=1 for Q1-Q10 [0]. Command: python3 count over L2.txt with manifest quotes.

E5. Leads bullet identity. `git show 69de8d363b2193fdb37d03fd3e235bceeb1c2daa:corpus/SOURCES.md | grep 'Google Big Sleep reporting beyond the tracker' | sha256sum` and the same on the working tree SOURCES.md both print `3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432  -` [0]. Line is SOURCES.md:141. `git diff 69de8d3 HEAD -- corpus/SOURCES.md` adds only the S092 row (line 99).

E6. Opens receipt: `sed -n '40,70p' .ufo/waves/round-59/controls/s092-opens-r59.txt` -> line 64 `code=200 final=https://issuetracker.google.com/savedsearches/7155917` (command recorded in the receipt as `curl -sS -o /dev/null -L ... https://goo.gle/bigsleep`).

E7. Saved-search shell content: receipt lines 42-44 record `grep -c "savedsearches/7155917" controls/s092-savedsearch-shell.html` -> 0 and `grep -o "Big Sleep" ... | wc -l` -> 0 [receipt, not re-run].

E8. Negative greps over L2 (`grep -o -i -- KW L2.txt | wc -l`): intake 0, submit 0, days 0, hours 0, week 0, month 0, year 0, deadline 0, CVSS 0, severity 0, reward 0, Immunefi 0, bounty 0, component 0 [0 each].

E9. Held ground: `sed -n '28p' corpus/source-snapshots/round-40/S017.txt` -> "Google Big Sleep, a collaboration between Google DeepMind and Google Project Zero, will also be trialling this policy for their vulnerability reports. The issue tracker for Google Big Sleep is at goo.gle/bigsleep" [0]. `grep -n 'Big Sleep' corpus/knowledge/pz-reporting-transparency-trial.md` line 18 quotes S017.txt L28 [0].

E10. Naptime sources: `grep -rn 'from-naptime-to-big-sleep' corpus/ --include=*.md --include=*.txt` -> only corpus/knowledge/google-big-sleep-findings-tracker.md:61 and corpus/source-snapshots/round-59/S092.txt:2 [0]. SOURCES.md:16 row S010 = "Google Project Zero, Project Naptime — https://projectzero.google/2024/06/project-naptime.html" [0].

E11. `grep -n -i -E 'naptime|S010|project zero' corpus/knowledge/ai-assisted-finding-validation.md` -> lines 22, 23 and 39 cite S010 (the Naptime post, "Perfect Verification" and conclusions). No line cites the 2024/10 post [0] (`grep -c 'from-naptime' ...` -> 0).

E12. Field mapping (python json.loads on L2): issue = L2[0][1][22]; issue[1] = 430375499; issue[2][0] = 1836411 (component id); issue[2][5] = "[Big Sleep] README"; field definitions at issue[14]: 1456855 CVE ID, 1457313 "Fixed" ("Date when the bug was fixed by the vendor"), 1472278 "Impact" ("Impact of the vulnerability", enum ["High","Medium","Low","None"]), 1457392 "Product" ("Software product the vulnerability was found in"), 1456622 "Reported" ("Date when the bug was reported"), 1456856 "Vendor". Field values at issue[2][14]: 1456622 -> 2025-07-08 (string "2025-07-08" at index 7/9), 1456856 -> "Google", 1457392 -> "Big Sleep" [0].

E13. Field definitions sit on the README issue record: `issue[14]` is the field-definition list of issue 430375499 itself; `issue[2][14]` holds the README issue's own field values. No finding issue is in the capture [0].

E14. Epoch conversion: `python3 -c "import datetime; [print(datetime.datetime.fromtimestamp(t, datetime.UTC).isoformat()) for t in (1752013968,1752176286,1776341538)]"` -> 2025-07-08T22:32:48, 2025-07-10T19:38:06, 2026-04-16T12:12:18 [0] (timestamps are in L2 issue[4], [34], [35]).

E15. Registry and admitted-row checks: `grep -nE '^\| (S072|S069) |^\| F(01|13|17|26) ' corpus/SOURCES.md corpus/README.md` -> SOURCES.md:78 S072, :75 S069; README.md:202 F01, :264 F13, :361 F17, :628 F26 [0].

E16. Quote-vs-entry fidelity: entry quotes "Findings from the project will be publicly disclosed following [Google's industry standard disclosure policy]", "All issues reported by the project so far can be found [here](https://goo.gle/bigsleep)", "Impact of the vulnerability", "Software product the vulnerability was found in", "Date when the bug was reported", "Date when the bug was fixed", "2025-07-08", "[Project Naptime: ...]" each occur once in L2 (python count, E4) [0].

E17. `grep -o "Project Zero's 2025 policy and disclosure trial" L2.txt | wc -l` -> 1; `grep -o 'googleprojectzero.blogspot.com/2025/07/reporting-transparency' L2.txt | wc -l` -> 5 [0].

Tools: none installed or upgraded. Used python3 standard library, grep, sha256sum, sed, wc, git show (read-only).

Scratch: /fast/scratch/hyaku/kasegi-r59/EntryClaimTable (L2.txt, f1.txt, fields.txt, readme_tail.txt, body.md, quotes.txt). Removed before yield; nothing left behind.

No credential material in this file. No lane file was edited; no git mutation was run.
