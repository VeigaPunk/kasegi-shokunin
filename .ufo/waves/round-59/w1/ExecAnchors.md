REFERENTS-HOLD

# ExecAnchors — R71 anchor-referent table for F40 / S092 (kasegi round-59 w1)

Scope: every free line anchor of the form `S092.txt:<n>` or `S092.txt:<n>-<m>` in
`L/corpus/knowledge/google-big-sleep-findings-tracker.md` (14), the S092 row of
`L/corpus/SOURCES.md` (0 anchors of that form), and the F40 row of
`L/corpus/README.md` (1) — 15 anchors total, no range anchors. Each was printed
beside its named capture line (first 120 chars) and judged: the cited sentence's
stated referent (a pinned Q quote, a URL, or the issue id) is on capture L2 in
every case. Script exit code 0.

Files changed: this file only (`L/.ufo/waves/round-59/w1/ExecAnchors.md`).
Lane read-only; no git/jj mutation; no tool installs; scratch deleted at yield.

---

## 1. Anchor census (independent of the table script)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ for f in corpus/knowledge/google-big-sleep-findings-tracker.md corpus/SOURCES.md corpus/README.md; do
    printf '%s ' "$f"; grep -oE 'S092\.txt:[0-9]+(-[0-9]+)?' "$f" | wc -l; done
corpus/knowledge/google-big-sleep-findings-tracker.md 14
corpus/SOURCES.md 0
corpus/README.md 1
exit 0

$ grep -cE 'S092\.txt:[0-9]+-[0-9]+' corpus/knowledge/google-big-sleep-findings-tracker.md corpus/SOURCES.md corpus/README.md
corpus/knowledge/google-big-sleep-findings-tracker.md:0
corpus/SOURCES.md:0
corpus/README.md:0
exit 1        # grep 1 because no range anchor matched; the three zeros are the census
```

Anchor-bearing lines in the entry, from the run in §3: 10, 13, 21, 22, 35, 36,
47, 48, 49 (x3), 58, 59, 61. README row at 984. SOURCES row at 99 has no
`S092.txt:<n>` anchor; its line reference is the deictic "L2" (checked in §5).

Pointer commands:

```
$ grep -nE '^\| (S092|F40) ' corpus/SOURCES.md corpus/README.md | cut -d: -f1,2
corpus/SOURCES.md:99
corpus/README.md:984
exit 0

$ grep -n "each on capture line L2" corpus/lessons/round-59.md | cut -d: -f1
25
exit 0

$ grep -n 'capture `corpus/source-snapshots/round-59/S092.txt`' corpus/README.md | cut -d: -f1
975
exit 0
```

---

## 2. Script and run

`S=/fast/scratch/hyaku/kasegi-r59/ExecAnchors`

```
$ sha256sum "$S/anchor-referents.py"
aae130e850a4c3958a5cd65d9e6d28c5d414abfa728cb368af09c2355782e198  /fast/scratch/hyaku/kasegi-r59/ExecAnchors/anchor-referents.py
$ wc -l "$S/anchor-referents.py"
229 /fast/scratch/hyaku/kasegi-r59/ExecAnchors/anchor-referents.py

$ cd "$S" && TMPDIR="$S" python3 "$S/anchor-referents.py" > "$S/run.out" 2>&1; echo "EXIT=$?"
EXIT=0

$ sha256sum "$S/run.out"; wc -l "$S/run.out"
42bf1a90eee7b2cf9cc9f8f50489a0283702112dd5e0d78020d7fad57074ebc4  /fast/scratch/hyaku/kasegi-r59/ExecAnchors/run.out
153 /fast/scratch/hyaku/kasegi-r59/ExecAnchors/run.out
```

Judgment rule the script applies (its docstring): the named line is
`capture[n-1:m]`; needles are every Q-id within 32 chars after / 24 chars before
the anchor, resolved through the manifest's pinned quote for that id, or, when
no Q-id is in that window, every http(s) URL in the anchor's paragraph. HOLD iff
every needle occurs on the named line and every referenced Q pin is anchored
there; MISMATCH otherwise; out-of-range line -> MISMATCH.

Script header (the capture facts every number below rests on):

```
ANCHOR-REFERENT TABLE (QUALITY R71) — S092 / F40 — round-59 w1 ExecAnchors
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
capture=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-59/S092.txt lines=2 bytes=6371 sha256=048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38
manifest=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-59/manifest.json quotes=10 manifest_anchor_values=[2]
capture line lengths: L1=4, L2=6365
```

---

## 3. Anchors, named line, referent judged (verbatim script output)

Line content column is the exact first 120 characters the script printed for
capture L2 (all 15 anchors name L2; the same 120-char prefix therefore repeats):

`[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null`

| # | citing file:line | anchor | named line | line content (120 ch) | referent on the named line | judgment |
|---|---|---|---|---|---|---|
| 01 | knowledge:10 | `S092.txt:2` | L2 | `[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null` | Q1 `[Big Sleep] README` occ=1 col=171 | HOLD |
| 02 | knowledge:13 | `S092.txt:2` | L2 | same 120 | Q2 `research. Findings ... following [Google` occ=1 col=2180 | HOLD |
| 03 | knowledge:21 | `S092.txt:2` | L2 | same 120 | Q1 `[Big Sleep] README` occ=1 col=171 | HOLD |
| 04 | knowledge:22 | `S092.txt:2` | L2 | same 120 | Q3 `All issues reported ... [here](https://goo.gle/bigsleep)` occ=1 col=2479 | HOLD |
| 05 | knowledge:35 | `S092.txt:2` | L2 | same 120 | Q2 occ=1 col=2180 (entry span through `policy]` occ=1, S14) | HOLD |
| 06 | knowledge:36 | `S092.txt:2` | L2 | same 120 | URL `.../2025/07/reporting-transparency.html` occ=5 col=1725 | HOLD |
| 07 | knowledge:47 | `S092.txt:2` | L2 | same 120 | Q4 `Impact of the vulnerability` occ=1 col=1097 | HOLD |
| 08 | knowledge:48 | `S092.txt:2` | L2 | same 120 | Q7 `["High","Medium","Low","None"]` occ=1 col=1131 | HOLD |
| 09 | knowledge:49 | `S092.txt:2` | L2 | same 120 | Q5 `Software product the vulnerability was found in` occ=1 col=1200 | HOLD |
| 10 | knowledge:49 | `S092.txt:2` | L2 | same 120 | Q6 `Date when the bug was reported` occ=1 col=1298 | HOLD |
| 11 | knowledge:49 | `S092.txt:2` | L2 | same 120 | Q8 `Date when the bug was fixed` occ=1 col=1007 | HOLD |
| 12 | knowledge:58 | `S092.txt:2` | L2 | same 120 | Q9 `null,"2025-07-08",[[null,"7/8/2025"]]` occ=1 col=360 | HOLD |
| 13 | knowledge:59 | `S092.txt:2` | L2 | same 120 | Q10 `[Project Naptime: Evaluating ... Models]` occ=1 col=2632 | HOLD |
| 14 | knowledge:61 | `S092.txt:2` | L2 | same 120 | URL 2024/06/project-naptime occ=5 col=1851; URL 2024/10/from-naptime-to-big-sleep occ=5 col=1932 | HOLD |
| 15 | README:984 | `S092.txt:2` | L2 | same 120 | Q2 occ=1 col=2180; Q3 occ=1 col=2479 | HOLD |

Per-anchor output, verbatim from `$S/run.out`:

```
[01] knowledge /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/google-big-sleep-findings-tracker.md:10  anchor=S092.txt:2 -> capture L2
     citing: Google's Issue Tracker speaks for Google's own project: issue 430375499 ("[Big Sleep] README", S092.txt:2 Q1)
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q1 occurrences=1 col=171 needle='[Big Sleep] README'
       on-line context: ',430375499,[1836411,10,1,3,3,"[Big Sleep] README",[null,"g'
     judgement=HOLD

[02] knowledge .../google-big-sleep-findings-tracker.md:13  anchor=S092.txt:2 -> capture L2
     citing: (Q2 names the disclosure commitments, S092.txt:2 Q2). This entry records those statements and the finding-record
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q2 occurrences=1 col=2180 needle='research. Findings from the project will be publicly disclosed following [Google'
       on-line context: "tomate software vulnerability research. Findings from the project will be publicly disclosed following [Google's industr"
     judgement=HOLD

[03] knowledge .../google-big-sleep-findings-tracker.md:21  anchor=S092.txt:2 -> capture L2
     citing: The tracker's own README names its subject: issue "[Big Sleep] README" (S092.txt:2 Q1) states "All issues
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q1 occurrences=1 col=171 needle='[Big Sleep] README'
       on-line context: ',430375499,[1836411,10,1,3,3,"[Big Sleep] README",[null,"g'
     judgement=HOLD

[04] knowledge .../google-big-sleep-findings-tracker.md:22  anchor=S092.txt:2 -> capture L2
     citing: reported by the project so far can be found [here](https://goo.gle/bigsleep)" (S092.txt:2 Q3). The recorded
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q3 occurrences=1 col=2479 needle='All issues reported by the project so far can be found [here](https://goo.gle/bi'
       on-line context: 'reporting-transparency.html). All issues reported by the project so far can be found [here](https://goo.gle/bigsleep).\\n\\nYou c'
     judgement=HOLD

[05] knowledge .../google-big-sleep-findings-tracker.md:35  anchor=S092.txt:2 -> capture L2
     citing: industry standard disclosure policy]" (S092.txt:2 Q2), and it names Project Zero's 2025 policy and disclosure trial
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q2 occurrences=1 col=2180 needle='research. Findings from the project will be publicly disclosed following [Google'
       on-line context: "tomate software vulnerability research. Findings from the project will be publicly disclosed following [Google's industr"
     judgement=HOLD

[06] knowledge .../google-big-sleep-findings-tracker.md:36  anchor=S092.txt:2 -> capture L2
     citing: at https://googleprojectzero.blogspot.com/2025/07/reporting-transparency.html (S092.txt:2). The trial itself is
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent URL occurrences=5 col=1725 https://googleprojectzero.blogspot.com/2025/07/reporting-transparency.html
     judgement=HOLD

[07] knowledge .../google-big-sleep-findings-tracker.md:47  anchor=S092.txt:2 -> capture L2
     citing: The capture serves the tracker's field definitions beside the README: "Impact of the vulnerability" (S092.txt:2 Q4)
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q4 occurrences=1 col=1097 needle='Impact of the vulnerability'
       on-line context: '2278,1836411,3,true,"Impact","Impact of the vulnerability",null,["H'
     judgement=HOLD

[08] knowledge .../google-big-sleep-findings-tracker.md:48  anchor=S092.txt:2 -> capture L2
     citing: with the value list ["High","Medium","Low","None"] (S092.txt:2 Q7), "Software product the vulnerability was found in"
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q7 occurrences=1 col=1131 needle='["High","Medium","Low","None"]'
       on-line context: 'ct of the vulnerability",null,["High","Medium","Low","None"],2],[14573'
     judgement=HOLD

[09] knowledge .../google-big-sleep-findings-tracker.md:49  anchor=S092.txt:2 -> capture L2
     citing: (S092.txt:2 Q5), "Date when the bug was reported" (S092.txt:2 Q6) and "Date when the bug was fixed" (S092.txt:2 Q8).
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q5 occurrences=1 col=1200 needle='Software product the vulnerability was found in'
       on-line context: '392,1836411,1,true,"Product","Software product the vulnerability was found in",null,nul'
     judgement=HOLD

[10] knowledge .../google-big-sleep-findings-tracker.md:49  anchor=S092.txt:2 -> capture L2
     citing: (S092.txt:2 Q5), "Date when the bug was reported" (S092.txt:2 Q6) and "Date when the bug was fixed" (S092.txt:2 Q8).
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q6 occurrences=1 col=1298 needle='Date when the bug was reported'
       on-line context: '22,1836411,2,true,"Reported","Date when the bug was reported",null,nul'
     judgement=HOLD

[11] knowledge .../google-big-sleep-findings-tracker.md:49  anchor=S092.txt:2 -> capture L2
     citing: (S092.txt:2 Q5), "Date when the bug was reported" (S092.txt:2 Q6) and "Date when the bug was fixed" (S092.txt:2 Q8).
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q8 occurrences=1 col=1007 needle='Date when the bug was fixed'
       on-line context: '57313,1836411,2,null,"Fixed","Date when the bug was fixed by the ve'
     judgement=HOLD

[12] knowledge .../google-big-sleep-findings-tracker.md:58  anchor=S092.txt:2 -> capture L2
     citing: The issue record's Reported value is "2025-07-08" (S092.txt:2 Q9), and the README's further-reading list opens with
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q9 occurrences=1 col=360 needle='null,"2025-07-08",[[null,"7/8/2025"]]'
       on-line context: '7,8],null,null,null,null,null,null,"2025-07-08",[[null,"7/8/2025"]]],[1456856'
     judgement=HOLD

[13] knowledge .../google-big-sleep-findings-tracker.md:59  anchor=S092.txt:2 -> capture L2
     citing: "[Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models]" (S092.txt:2 Q10), linking
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q10 occurrences=1 col=2632 needle='[Project Naptime: Evaluating Offensive Security Capabilities of Large Language M'
       on-line context: 'oject in these blog posts:\\n* [Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models](https://g'
     judgement=HOLD

[14] knowledge .../google-big-sleep-findings-tracker.md:61  anchor=S092.txt:2 -> capture L2
     citing: https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html (S092.txt:2) — the documents S010
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent URL occurrences=5 col=1851 https://googleprojectzero.blogspot.com/2024/06/project-naptime.html
     referent URL occurrences=5 col=1932 https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html
     judgement=HOLD

[15] README /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:984  anchor=S092.txt:2 -> capture L2
     citing: | F40 | Google Big Sleep public findings tracker — the Google Issue Tracker's own README for the tracker where Big Sleep's disclosed findings are collected: the disclosure policies they follow and the
     named line first 120: '[["b.IssueFetchResponse",[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null'
     referent Q2 occurrences=1 col=2180 needle='research. Findings from the project will be publicly disclosed following [Google'
       on-line context: "tomate software vulnerability research. Findings from the project will be publicly disclosed following [Google's industr"
     referent Q3 occurrences=1 col=2479 needle='All issues reported by the project so far can be found [here](https://goo.gle/bi'
       on-line context: 'reporting-transparency.html). All issues reported by the project so far can be found [here](https://goo.gle/bigsleep).\\n\\nYou c'
     judgement=HOLD
```

Note: blocks [02]-[14] print the absolute path in `run.out`; the `...` abbreviation here stands only for the repeated prefix `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge` and no other text. Every number in the table above is printed in these blocks or in §4.

`run.out` tail:

```
SUMMARY anchors=15 hold=15 mismatch=0 unjudged=0 q_pin_defects=0
FILES knowledge=14 SOURCES=0 README=1
RESULT: REFERENTS-HOLD
```

---

## 4. Structural referent checks (verbatim, same run)

These test that each Q quote actually sits where the citing sentence says, not
merely that the substring exists somewhere on L2.

```
S1 issue title rec[2][5]='[Big Sleep] README'; Q1 in title=True
S2 Q2 inside README body rec[43][0]=True (body length 933)
S2 Q3 inside README body rec[43][0]=True (body length 933)
S2 Q10 inside README body rec[43][0]=True (body length 933)
S2b Q2 continuation "industry standard disclosure policy" in body=True; Project Zero 2025 link text in body=True
S3 Q4 field id=1472278 name='Impact' desc='Impact of the vulnerability' relation=exact
S3 Q5 field id=1457392 name='Product' desc='Software product the vulnerability was found in' relation=exact
S3 Q6 field id=1456622 name='Reported' desc='Date when the bug was reported' relation=exact
S3 Q8 field id=1457313 name='Fixed' desc='Date when the bug was fixed by the vendor' relation=prefix
S4 Q7 enum=["High","Medium","Low","None"] equals Impact field enum list=True (Impact name='Impact')
S5 Reported value entry field id=1456622 display='2025-07-08' def name='Reported'; Q9 occurrences in entry=1
S6 Q1 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q2 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q3 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q4 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q5 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q6 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q7 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q8 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q9 pinned anchor=2 occurrences_on_raw_L2=1
S6 Q10 pinned anchor=2 occurrences_on_raw_L2=1
S7 capture bytes=6371 manifest_bytes=6371 sha_match=True
S12 issue id 430375499 occurrences on L2=2 (knowledge:10 states the issue number)
S13 README-body intake-marker counts on L2: intake=0, submit=0, file your=0, report your=0, send us=0, report a vulnerability=0, researcher=0, third-party=0; body_length=933
S14 entry-stated span on L2 occurrences=1 needle='Findings from the project will be publicly disclosed following [Google'
S14 entry-stated span on L2 occurrences=1 needle="Project Zero's 2025 policy and disclosure trial"
S14 entry-stated span on L2 occurrences=0 needle="kept in the tracker's Big Sleep component"
S8 component-name occurrences on L2=0; component id 1836411 occurrences=8; component clause carrying the *name* on L2=False
S9 S092 row count=1; names capture by path=True; says 'L2 is the tracker's action JSON'=True; S092.txt:* anchor form in row=False
S10 README F40 row count=1; anchor form in row=True
```

---

## 5. Deictic line references (adjunct; not `S092.txt:<n>` form)

```
DEICTIC LINE REFERENCES (L<n> near the S092 capture path; adjunct, not S092.txt:NN form)
D1 knowledge:3 says 'capture line L2'=True; L2 parses as JSON=True top_tag='b.IssueFetchResponse'
D2 knowledge:77 says 'All ten pinned quotes sit on capture line L2'=True; quotes_on_L2=10/10
D3 SOURCES:99 says 'L2 is the tracker's action JSON'=True; named row capture line exists=True
S11 lessons Gate located-quote lines=10 at [26, 27, 28, 29, 30, 31, 32, 33, 34, 35]; states 'each on capture line L2'=True; mentions the F40 entry=True; prints any S092.txt:NN citing anchor=False
```

```
$ grep -c 'S092\.txt:' corpus/lessons/round-59.md
0
exit 1        # grep 1 because the count is 0
```

The entry sentence carrying the component clause (pointer for N2):

```
$ sed -n '10,12p' corpus/knowledge/google-big-sleep-findings-tracker.md
Google's Issue Tracker speaks for Google's own project: issue 430375499 ("[Big Sleep] README", S092.txt:2 Q1)
is the tracker's own README, kept in the tracker's Big Sleep component by the project it describes. Every
statement below is that README's first-party statement about its own tracker and its own handling commitments
exit 0
```

---

## 6. Notes (do not flip the verdict; report only)

- **N1 — coarse anchors, no discrimination.** All 15 anchors are `S092.txt:2`, the
  capture's only content line (L1 is the 4-byte `)]}'` XSSI prefix; L2 is 6365
  bytes). The line test is therefore satisfied by construction for anything on L2;
  the Q label is what discriminates. A capture-format change that splits L2 would
  make all 15 anchors point at the wrong line silently; this table must be re-run
  on any capture re-format. Evidence: script header, S6, `run.out` SUMMARY.
- **N2 — sentence clause not carried by name (entry:11).** The anchored sentence at
  knowledge:10-12 says the issue is "kept in the tracker's Big Sleep component".
  L2 contains `component` 0 times and component id `1836411` 8 times; the name
  "Big Sleep" on L2 is the Product field value and the README body, not a
  component name. The anchor tags Q1 (the issue title), which is present, so the
  anchor holds; the component-name clause is unanchored and unconfirmed by the
  named line. Evidence: S8, S14 line 3, `sed -n '10,12p'`.
- **N3 — Q8 quote is a truncated field description.** Entry:49 and the manifest pin
  quote "Date when the bug was fixed"; L2's Fixed-field description (id 1457313)
  is "Date when the bug was fixed by the vendor". The line carries the stated
  phrase as a prefix, so R71 holds, but the quoted text drops "by the vendor"
  without an ellipsis. Evidence: S3.
- **N4 — README row's Q2 tag under-covers its clause.** README:984 tags "Project
  Zero's 2025 trial" with Q2, but the manifest Q2 pin stops at "[Google"; the
  Project Zero half is on L2 in the same sentence (`...and [Project Zero's 2025
  policy and disclosure trial](https://...reporting-transparency.html)`). The line
  anchor holds; the pin does not cover the clause. Evidence: block [15], S14
  line 2.
- **N5 — SOURCES row has no anchor of the R71 form.** SOURCES:99 cites the capture
  by path plus the deictic "L2"; zero `S092.txt:<n>` matches in the file. D3 shows
  the deictic reference holds. Entry:3 and entry:77 are two further deictic "L2"
  references that hold (D1, D2). R71's `file:NN` wording does not scan this form,
  so these three line references are outside the anchor check by construction.
- **N6 — Gate table characterization.** Entry:77 says the lessons Gate's
  "anchor-referent table ... maps each cited line to the sentence it supports
  (R71)". The Gate (lessons:25-35) is a located-quote list — Q1-Q10, "each on
  capture line L2", with word counts and glosses — and prints no `S092.txt:NN`
  citing anchor (S11, `grep -c "S092\.txt:" corpus/lessons/round-59.md` = 0). It
  supports each quote's line, not each citing sentence; the per-anchor table is
  this file.

---

## 7. Scratch, tooling, writes

- Scratch `S=/fast/scratch/hyaku/kasegi-r59/ExecAnchors` held the script, its
  output and no clones; deleted before yield. No leftovers.
- No tool install or upgrade was needed or performed: no pacman transaction, no
  uv/npx, no network fetch (the capture and manifest were read locally).
- Reads only in L: the three target files, `S092.txt`, `manifest.json`,
  `corpus/lessons/round-59.md`, `corpus/QUALITY.md:452`, `corpus/lessons/round-58.md`.
  No lane write except this file. No git/jj command was run; no sibling lane, no
  fleet-root tracked file, no `~/.local/bin` write.
- No lane suite, build, lint or formatter was run (parent owns post-integration
  gates).

---

## Appendix A — script source (sha256 aae130e850a4c3958a5cd65d9e6d28c5d414abfa728cb368af09c2355782e198)

```python
#!/usr/bin/env python3
"""R71 anchor-referent table for S092 / F40 (round-59 w1, seat ExecAnchors).

Rules applied, per anchor occurrence:
  * ANCHOR: regex S092\\.txt:(N)(?:-(M))? in the knowledge entry, the S092
    row of SOURCES.md and the F40 row of README.md.
  * NAMED LINE: the line N (or N..M) of corpus/source-snapshots/round-59/S092.txt.
    Out of range -> MISMATCH.
  * REFERENT NEEDLES: (a) every Q-id within 32 chars after / 24 chars before the
    anchor, resolved through the manifest's pinned quote for that id, when the
    manifest anchor for that id equals the named line; (b) when no Q-id is in
    that window, every http(s) URL in the anchor's paragraph (contiguous
    non-empty lines, at most 3 either side).
  * HOLD when every needle occurs on the named line and every referenced Q pin
    is anchored at that line; MISMATCH otherwise; UNJUDGED when no needle can
    be derived.
Output: one block per anchor, then structural referent checks, then RESULT.
Exit: 0 REFERENTS-HOLD, 1 MISMATCH, 2 UNJUDGED present.
"""
import hashlib
import json
import re
import sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
K = L + "/corpus/knowledge/google-big-sleep-findings-tracker.md"
SO = L + "/corpus/SOURCES.md"
R = L + "/corpus/README.md"
C = L + "/corpus/source-snapshots/round-59/S092.txt"
M = L + "/corpus/source-snapshots/round-59/manifest.json"

ANCHOR = re.compile(r"S092\.txt:(\d+)(?:-(\d+))?")
QID = re.compile(r"\b(Q\d+)\b")
URL = re.compile(r"https?://[^\s)\]>\"`]+")


def read_lines(p):
    with open(p, encoding="utf-8") as f:
        return f.read().splitlines()


def para(text_lines, idx):
    """Contiguous non-empty line window around idx (0-based), at most 3 either side."""
    lo = idx
    while lo > 0 and text_lines[lo - 1].strip() and idx - lo < 3:
        lo -= 1
    hi = idx
    while hi + 1 < len(text_lines) and text_lines[hi + 1].strip() and hi - idx < 3:
        hi += 1
    return "\n".join(text_lines[lo:hi + 1])


cap = read_lines(C)
manifest = json.load(open(M, encoding="utf-8"))
src = [s for s in manifest["sources"] if s["id"] == "S092"][0]
quotes = {q["id"]: q for q in src["quotes"]}
cap_sha = hashlib.sha256(open(C, "rb").read()).hexdigest()

print("ANCHOR-REFERENT TABLE (QUALITY R71) — S092 / F40 — round-59 w1 ExecAnchors")
print(f"L={L}")
print(f"capture={C} lines={len(cap)} bytes={len(open(C,'rb').read())} sha256={cap_sha}")
print(f"manifest={M} quotes={len(quotes)} manifest_anchor_values={sorted({q['anchor'] for q in quotes.values()})}")
print(f"capture line lengths: " + ", ".join(f"L{i+1}={len(t)}" for i, t in enumerate(cap)))
print()

rows = []
q_pin_defects = []
for path, label in ((K, "knowledge"), (SO, "SOURCES"), (R, "README")):
    tl = read_lines(path)
    for i, line in enumerate(tl):
        for m in ANCHOR.finditer(line):
            n = int(m.group(1))
            mm = int(m.group(2)) if m.group(2) else n
            after = line[m.end():m.end() + 32]
            before = line[max(0, m.start() - 24):m.start()]
            qids = QID.findall(before + " " + after)
            urls = [] if qids else sorted(set(URL.findall(para(tl, i))))
            needles = []  # (kind, id, text)
            for q in qids:
                if q in quotes:
                    needles.append(("Q", q, quotes[q]["quote"]))
                else:
                    needles.append(("Q", q, None))
            for u in urls:
                needles.append(("URL", "-", u))
            named = []
            verdict = "UNJUDGED"
            reasons = []
            if not (1 <= n <= len(cap)) or not (1 <= mm <= len(cap)) or mm < n:
                verdict = "MISMATCH"
                reasons.append(f"named line {n}-{mm} out of capture range 1-{len(cap)}")
            else:
                named = cap[n - 1:mm]
                seg = "\n".join(named)
                occ = []
                pin_bad = False
                for kind, qid, text in needles:
                    if text is None:
                        pin_bad = True
                        occ.append((kind, qid, "MISSING-FROM-MANIFEST", -1))
                        continue
                    if kind == "Q":
                        pin = quotes[qid]
                        if pin["anchor"] != n:
                            q_pin_defects.append((qid, pin["anchor"], n))
                            pin_bad = True
                            reasons.append(f"{qid} pinned at anchor {pin['anchor']} != named line {n}")
                    c = seg.count(text)
                    occ.append((kind, qid, text, c))
                    if c < 1:
                        pin_bad = True
                if needles and not pin_bad and all(c >= 1 for _, _, _, c in occ):
                    verdict = "HOLD"
                elif needles:
                    verdict = "MISMATCH"
                else:
                    reasons.append("no Q-id in window and no URL in paragraph")
            rows.append(dict(file=label, path=path, line=i + 1, n=n, mm=mm,
                             anchor=m.group(0), needles=needles, occ=occ,
                             named=named, verdict=verdict, reasons=reasons))

for k, r in enumerate(rows, 1):
    print(f"[{k:02d}] {r['file']} {r['path']}:{r['line']}  anchor={r['anchor']} -> capture L{r['n']}"
          + ("" if r['mm'] == r['n'] else f"-L{r['mm']}"))
    tl_line = read_lines(r['path'])[r['line'] - 1]
    print(f"     citing: {tl_line.strip()[:200]}")
    if r['named']:
        head = r['named'][0][:120].replace("\n", "\\n")
        print(f"     named line first 120: {head!r}")
        for kind, qid, text, c in r['occ']:
            if kind == "Q" and text is not None:
                col = r['named'][0].find(text)
                ctx = r['named'][0][max(0, col - 30):col + len(text) + 10] if col >= 0 else ""
                print(f"     referent {qid} occurrences={c} col={col} needle={text[:80]!r}")
                if col >= 0:
                    print(f"       on-line context: {ctx!r}")
            else:
                col = "\n".join(r['named']).find(text)
                print(f"     referent URL occurrences={c} col={col} {text}")
    for reason in r['reasons']:
        print(f"     reason: {reason}")
    print(f"     judgement={r['verdict']}")
    print()

# ---- structural referent checks (beyond substring presence) ----
print("STRUCTURAL REFERENT CHECKS")
body = json.loads(cap[1])
rec = body[0][1][22]
title = rec[2][5]
field_defs = rec[14]
defs = {fd[0]: dict(name=fd[4], desc=fd[5], enum=fd[7]) for fd in field_defs}
readme_body = rec[43][0]
print(f"S1 issue title rec[2][5]={title!r}; Q1 in title={quotes['Q1']['quote'] in title}")
for qid in ("Q2", "Q3", "Q10"):
    print(f"S2 {qid} inside README body rec[43][0]={quotes[qid]['quote'] in readme_body} "
          f"(body length {len(readme_body)})")
print(f"S2b Q2 continuation \"industry standard disclosure policy\" in body="
      f"{'industry standard disclosure policy' in readme_body}; Project Zero 2025 link text in body="
      f"{'Project Zero' in readme_body and 'disclosure trial' in readme_body}")
for qid, fid in (("Q4", 1472278), ("Q5", 1457392), ("Q6", 1456622), ("Q8", 1457313)):
    d = defs[fid]
    q = quotes[qid]["quote"]
    rel = "exact" if q == d["desc"] else ("prefix" if d["desc"].startswith(q) else "not-a-prefix")
    print(f"S3 {qid} field id={fid} name={d['name']!r} desc={d['desc']!r} relation={rel}")
print(f"S4 Q7 enum={quotes['Q7']['quote']} equals Impact field enum list="
      f"{json.dumps(defs[1472278]['enum'], separators=(',', ':')) == quotes['Q7']['quote']} "
      f"(Impact name={defs[1472278]['name']!r})")
value_entry = rec[2][14][0]
print(f"S5 Reported value entry field id={value_entry[0]} display={value_entry[9]!r} "
      f"def name={defs[value_entry[0]]['name']!r}; Q9 occurrences in entry="
      f"{json.dumps(value_entry, separators=(',', ':')).count('2025-07-08')}")
for qid, q in quotes.items():
    print(f"S6 {qid} pinned anchor={q['anchor']} occurrences_on_raw_L2={cap[1].count(q['quote'])}")
print(f"S7 capture bytes={len(open(C,'rb').read())} manifest_bytes={src['bytes']} "
      f"sha_match={cap_sha == src['sha256']}")
comp_name = cap[1].count("component")
comp_id = cap[1].count("1836411")
print(f"S12 issue id 430375499 occurrences on L2={cap[1].count('430375499')} (knowledge:10 states the issue number)")
toks=["intake","submit","file your","report your","send us","report a vulnerability","researcher","third-party"]
print(f"S13 README-body intake-marker counts on L2: " + ", ".join(f"{t}={readme_body.lower().count(t)}" for t in toks) + f"; body_length={len(readme_body)}")
for t in ["Findings from the project will be publicly disclosed following [Google's industry standard disclosure policy]",
          "Project Zero's 2025 policy and disclosure trial",
          "kept in the tracker's Big Sleep component"]:
    print(f"S14 entry-stated span on L2 occurrences={cap[1].count(t)} needle={t[:70]!r}")
print(f"S8 component-name occurrences on L2={comp_name}; component id 1836411 occurrences={comp_id}; "
      f"component clause carrying the *name* on L2={comp_name > 0}")
so_row = [t for t in read_lines(SO) if t.startswith("| S092 |")]
l2_clause = "L2 is the tracker's action JSON" in so_row[0]
print(f"S9 S092 row count={len(so_row)}; names capture by path={'corpus/source-snapshots/round-59/S092.txt' in so_row[0]}; "
      f"says 'L2 is the tracker's action JSON'={l2_clause}; "
      f"S092.txt:* anchor form in row={bool(ANCHOR.search(so_row[0]))}")
r_row = [t for t in read_lines(R) if re.match(r"^\| F40 ", t)]
print(f"S10 README F40 row count={len(r_row)}; anchor form in row={bool(ANCHOR.search(r_row[0]))}")

print()
print("DEICTIC LINE REFERENCES (L<n> near the S092 capture path; adjunct, not S092.txt:NN form)")
ok_json = True
try:
    top = json.loads(cap[1])
    tag = top[0][0]
except Exception as e:  # noqa: BLE001
    ok_json = False
    tag = f"parse-error {e}"
k3 = read_lines(K)[2]
k77 = read_lines(K)[76]
so99 = so_row[0]
print(f"D1 knowledge:3 says 'capture line L2'={'capture line L2' in k3}; L2 parses as JSON={ok_json} top_tag={tag!r}")
print(f"D2 knowledge:77 says 'All ten pinned quotes sit on capture line L2'="
      f"{'All ten pinned quotes sit on capture line L2' in k77}; quotes_on_L2={sum(1 for q in quotes.values() if cap[1].count(q['quote']) >= 1)}/10")
print(f"D3 SOURCES:99 says 'L2 is the tracker's action JSON'={l2_clause}; named row capture line exists={len(cap) >= 2}")
G = L + "/corpus/lessons/round-59.md"
gl = read_lines(G)
gate_q = [i + 1 for i, t in enumerate(gl) if re.match(r"\s+- Q\d+ — ", t)]
print(f"S11 lessons Gate located-quote lines={len(gate_q)} at {gate_q}; "
      f"states 'each on capture line L2'={'each on capture line L2' in chr(10).join(gl)}; "
      f"mentions the F40 entry={any('google-big-sleep-findings-tracker' in t for t in gl)}; "
      f"prints any S092.txt:NN citing anchor={any(ANCHOR.search(t) for t in gl)}")

hold = sum(1 for r in rows if r['verdict'] == "HOLD")
mis = sum(1 for r in rows if r['verdict'] == "MISMATCH")
unj = sum(1 for r in rows if r['verdict'] == "UNJUDGED")
print()
print(f"SUMMARY anchors={len(rows)} hold={hold} mismatch={mis} unjudged={unj} "
      f"q_pin_defects={len(q_pin_defects)}")
print(f"FILES knowledge={sum(1 for r in rows if r['file']=='knowledge')} "
      f"SOURCES={sum(1 for r in rows if r['file']=='SOURCES')} "
      f"README={sum(1 for r in rows if r['file']=='README')}")
print("RESULT: " + ("REFERENTS-HOLD" if mis == 0 and unj == 0 else "MISMATCH"))
sys.exit(0 if mis == 0 and unj == 0 else (1 if mis else 2))
```
