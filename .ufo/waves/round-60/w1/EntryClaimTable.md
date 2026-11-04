PASS (29 rows, all GROUNDED)

# EntryClaimTable — kasegi r60 w1

Seat: EntryClaimTable. Targets (read-only): `L/corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md`, `L/corpus/source-snapshots/round-60/manifest.json`, `L/corpus/source-snapshots/round-60/S093.txt`, pinned at commit `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`.

Headline: **29 load-bearing sentences** in Attribution and Claims 1–4, **29 GROUNDED**, 0 OVERREACH, 0 UNGROUNDED. **15/15** pinned quotes at most 25 words (max 25, Q13). **50** literal inline `S093.txt:` anchor instances plus 3 shorthand continuations (`:28`, `:31`, `:34`) — **31** distinct literal expressions (28 single lines + 3 ranges) — all on supporting lines, **0 one line off**. 29 in-scope quoted spans with a citation: 27 byte-exact + 2 differing only in nested quotation marks (N3); 0 on the wrong line.

Entry line map (for the table): A rows `entry:10`; C1-1…C1-3 `entry:14`, C1-4…C1-5 `entry:16`; C2-1…C2-3 `entry:20`, C2-4…C2-5 `entry:22`; C3-1…C3-6 `entry:26`, C3-7…C3-8 `entry:28`; C4-1…C4-3 `entry:32`, C4-4…C4-5 `entry:34`.

## Pin (E8)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git rev-parse HEAD
228118a8cfba679c1d97841aa3af38e5ec83d84a
$ git diff --stat 7f7dd267283d2a16ca38d4cb05bed92165cb35cd HEAD -- corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/source-snapshots/round-60/manifest.json corpus/source-snapshots/round-60/S093.txt
(no output)                                       exit 0
$ git log --oneline 7f7dd267283d2a16ca38d4cb05bed92165cb35cd..HEAD
228118a round-60: SCORECARD round-60 result (axes table, move log, capabilities rows for derive-gate-chain-ref
fb6a928 round-60: lesson (M60-1..M60-7, Gate S093 with 15 quotes, sources/frontier, R78-R80 in QUALITY), exten
b8c77fb round-60: wave-1 spec, validated plan and dispatch (13 seats, policy v1 band 8-16, attack share 4/13=3
(3 commits; `git rev-list --count 7f7dd26..HEAD` = 3) exit 0
$ for f in corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/source-snapshots/round-60/manifest.json corpus/source-snapshots/round-60/S093.txt; do a=$(git show 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:$f | sha256sum | cut -d' ' -f1); b=$(sha256sum "$f" | cut -d' ' -f1); echo "$f"; echo "  at-7f7dd26=$a"; echo "  worktree  =$b"; [ "$a" = "$b" ] && echo "  IDENTICAL" || echo "  DIFFERS"; done
corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
  at-7f7dd26=77e200f8663d623f3b93410193c09d42bee0c5c42d151cff47ab40772b2253e1
  worktree  =77e200f8663d623f3b93410193c09d42bee0c5c42d151cff47ab40772b2253e1
  IDENTICAL
corpus/source-snapshots/round-60/manifest.json
  at-7f7dd26=b9a6ebfabf8054f4c3689198a4ca47ca1ba4b207b73a8741712b81bcbe27c8e8
  worktree  =b9a6ebfabf8054f4c3689198a4ca47ca1ba4b207b73a8741712b81bcbe27c8e8
  IDENTICAL
corpus/source-snapshots/round-60/S093.txt
  at-7f7dd26=46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96
  worktree  =46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96
  IDENTICAL
```

The lane HEAD is three commits past the seat's stated target (`228118a` vs `7f7dd26`); the three target blobs are byte-identical at both, so this table is over the target commit's bytes (N5). No lane file was edited; only this evidence file was written. No git mutation was run. No tool was installed (none needed).

## Evidence

**E1 — capture digest.**
```
$ sha256sum corpus/source-snapshots/round-60/S093.txt
46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96  corpus/source-snapshots/round-60/S093.txt   exit 0
```
Matches the entry header (`entry:3`) and manifest `sha256`.

**E2 — capture size.**
```
$ wc -l -c corpus/source-snapshots/round-60/S093.txt
  283 40649 corpus/source-snapshots/round-60/S093.txt   exit 0
```
Matches the entry header ("40649 snapshot bytes over 283 lines") and manifest `snapshot_bytes`/`lines`.

**E3 — manifest pinned quotes (anchor, occurrence, on-line, `wc -w`).** The checker writes each quote's exact text to a temp file and runs the `wc -w` binary on it (temp files were inside `$S`, now removed). Command: `TMPDIR=$S python3 $S/check_final.py` → exit 0; section E3:
```
Q1: anchor=12 occurrences=2 on_anchor_line=True wc_w=10
Q2: anchor=16 occurrences=1 on_anchor_line=True wc_w=23
Q3: anchor=40 occurrences=1 on_anchor_line=True wc_w=18
Q4: anchor=51 occurrences=1 on_anchor_line=True wc_w=14
Q5: anchor=61 occurrences=1 on_anchor_line=True wc_w=10
Q6: anchor=65 occurrences=1 on_anchor_line=True wc_w=11
Q7: anchor=68 occurrences=1 on_anchor_line=True wc_w=24
Q8: anchor=71 occurrences=1 on_anchor_line=True wc_w=17
Q9: anchor=74 occurrences=1 on_anchor_line=True wc_w=19
Q10: anchor=82 occurrences=1 on_anchor_line=True wc_w=20
Q11: anchor=88 occurrences=1 on_anchor_line=True wc_w=19
Q12: anchor=16 occurrences=1 on_anchor_line=True wc_w=7
Q13: anchor=16 occurrences=1 on_anchor_line=True wc_w=25
Q14: anchor=281 occurrences=1 on_anchor_line=True wc_w=16
Q15: anchor=281 occurrences=1 on_anchor_line=True wc_w=14
```

**E4 — every quoted span in the entry vs the citation that follows it.** Same invocation, section E4. Each line is `verdict anchors=[…] quoted-span` (the span is truncated to 90 chars by the script):
```
OK-exact anchors=[12] 'Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines'
OK-exact anchors=[16] 'two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, '
OK-exact anchors=[22] 'For this blog post, we will limit ourselves to two concrete systems: Fuzzilli, a JavaScrip'
OK-exact anchors=[23] 'We also limit ourselves to V8 as a target'
OK-exact anchors=[16] 'LLM-based bug finding system'
OK-exact anchors=[26] 'the six months from April to September 2026'
OK-exact anchors=[40] 'roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37'
OK-exact anchors=[16] 'BigSleep found more vulnerabilities than Fuzzilli (45 versus 37) with a 25% overlap in the'
OK-exact anchors=[51] 'roughly 25% (20 out of a total of 81)'
OK-exact anchors=[41] 'it’s challenging to make a comparison at this stage in the research'
OK-exact anchors=[56] 'roughly 600 vulnerabilities'
OK-exact anchors=[60] '132 historic bugs'
OK-exact anchors=[61] 'a final number of 112 bugs'
OK-exact anchors=[65] '25 attempts on each commit'
OK-exact anchors=[65] 'the same underlying model: Gemini 3.6 flash'
OK-exact anchors=[68] 'BigSleep was able to re-discover ~62% of the original bugs, while finding a different (but'
OK-exact anchors=[71] 'no statistically significant amount of memorization pre-2026'
OK-exact anchors=[82] '10 additional bugs in total: 8 from the different starting points and 7 with the rephrased'
OK-exact anchors=[84] 'correct'
OK-exact anchors=[88] 'around 60% of historic Fuzzilli bugs (70% with additional runs that used different prompts'
OK-exact anchors=[84] 'should be treated with some caution'
OK-quote-marks-only anchors=[53] "is more difficult to set up, since fuzzers cannot easily be given a similar 'starting poin"
OK-exact anchors=[16] 'fuzzing and LLMs are still complementary approaches'
OK-exact anchors=[16] 'We recommend vendors perform both fuzzing and agentic analysis of their code to maximize t'
OK-exact anchors=[281] 'the two approaches remain complementary, and specialized fuzzing continues to provide valu'
OK-quote-marks-only anchors=[90] 'Bugs that are difficult for a fuzzer to find are more likely to also be difficult to find '
OK-exact anchors=[91] 'The overlap seems to be smaller in the JIT Compilers and higher in the rest of the engine'
OK-exact anchors=[74] 'Bugs that are hard to find for a fuzzer are likely also hard to find for an AI agent'
OK-exact anchors=[281] 'we expect further model improvements, potentially coupled with better prompting and more f'
FAIL anchors=[30, 30, 31, 32, 33, 34] 'cheaper per bug'
span checks: exact=27 quote_marks_only=2 fail=1 total=30
```
The single `FAIL` is the Limits bullet's own coinage `"cheaper per bug"` (entry:39), followed by the citation `S093.txt:30-34`; it is the entry's scare-quote phrase, not a post quote, and lies outside the table's scope (Claims 1–4 + Attribution). The two `quote_marks_only` spans are S093.txt:53 and :90 (N3).

**E5 — numeric/date/byline citations.** Same invocation, section E5: `numeric/date/byline checks: 33/33` (316, 441, 178, 95, 45 vs 37, 20 of 81, 1150, 600, 132, 112, 25 attempts, Gemini 3.6 flash, March 2026, 62/12/26%, 10 = 8 + 7 with 5 in both, 70%, 84%, some caution, 60% of historic Fuzzilli bugs, “easy” overlap, JIT Compilers, hard-for-agent, more-difficult-to-set-up, 2026-Oct-27, Samuel Groß, and both hotlist query strings).

**E6 — anchor expressions.** Same invocation, section E6:
```
instances: 50 distinct: 31
{'12': 1, '13': 1, '14': 1, '16': 6, '22': 4, '23': 2, '26': 1, '27': 1, '30': 1,
 '30-34': 1, '33': 1, '33-34': 1, '40': 2, '41': 2, '51': 1, '53-68': 1, '53': 2,
 '55': 1, '56': 1, '60': 1, '61': 1, '65': 2, '68': 1, '71': 4, '74': 1, '82': 1,
 '84': 2, '88': 1, '90': 1, '91': 1, '281': 3}
```

**E7 — negative-claim checks.**
```
$ grep -c -i -E 'bounty|severity|intake|submission' corpus/source-snapshots/round-60/S093.txt
0                                                  exit 1 (no match)
$ grep -c -i -E 'policy' corpus/source-snapshots/round-60/S093.txt
1                                                  exit 0
   -> only line 9, the site nav link "vulnerability disclosure policy"; not post content
$ grep -oE 'crbug\.com/[0-9]+' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md | wc -l
0                                                  exit 0
```
`reward` occurs only in the technical coverage-feedback sense at capture lines 151 and 200; no bounty/reward guidance.

**E8 — pin.** See "Pin" above.

**E9 — table self-count (this file).**
```
$ grep -cE '^\| [AC][0-9]' .ufo/waves/round-60/w1/EntryClaimTable.md
29                                                 exit 0
$ grep -cE '\| GROUNDED \|$' .ufo/waves/round-60/w1/EntryClaimTable.md
29                                                 exit 0
$ grep -cE '\| (OVERREACH|UNGROUNDED) \|$' .ufo/waves/round-60/w1/EntryClaimTable.md
0                                                  exit 1 (no match)
```

## Claim table

| ID | Short sentence | Quote | Capture line | Status |
| A1 | Title "Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines" | Q1 | 12 | GROUNDED |
| A2 | Dated 2026-Oct-27 | NONE | 13 | GROUNDED |
| A3 | Byline Samuel Groß | NONE | 14 | GROUNDED |
| A4 | Self-description: "two automated tools used by Google to find vulnerabilities in Chrome's JavaScript engine, V8, on a regular basis" | NONE | 16 | GROUNDED |
| A5 | Research report on Google's own two systems, not a policy, program rule, intake channel or severity ladder | NONE | 16, 22 | GROUNDED |
| A6 | Entry asserts only the post's statements and counts, verifies no finding and no crbug.com reference, instructs no probing | NONE | n/a (entry self-check) | GROUNDED |
| C1-1 | Scoped to two systems (Fuzzilli, BigSleep) and to V8 as target | NONE | 22, 23 | GROUNDED |
| C1-2 | Fuzzilli generative JS-engine fuzzer, BigSleep LLM-based; both production pipelines on newly added code; many instances vs once per day | NONE | 16, 22 | GROUNDED |
| C1-3 | Comparison of these two on one engine, not a general fuzzing-versus-agent benchmark | NONE | 22, 23 | GROUNDED |
| C1-4 | Rule: capture fixes date/byline/target; scope and target sentences bound the claim | NONE | 12-14, 22-23 | GROUNDED |
| C1-5 | Rejected reading: the scope and target sentences exclude a general benchmark reading | NONE | 22, 23 | GROUNDED |
| C2-1 | Two Chromium hotlist queries over April-September 2026 with the two printed query strings | NONE | 26, 27, 28 | GROUNDED |
| C2-2 | Three views: raw 316/441, type:vulnerability 178/95, actionable Type-Vuln 45 vs 37 | Q3 | 30, 31, 33, 34, 40 | GROUNDED |
| C2-3 | Summary states 45 vs 37 with 25% overlap; overlap section gives ~25% (20 of 81) | Q2, Q4 | 16, 51 | GROUNDED |
| C2-4 | Rule: citing 441/316 as vulnerability counts contradicts the post's narrowing | NONE | 33-34, 40 | GROUNDED |
| C2-5 | Rejected: cost-per-bug comparison is challenging at this stage; raw counts are not vulnerability counts | NONE | 32, 33-34, 41 | GROUNDED |
| C3-1 | Sample: ~1150 raw, ~600 vulnerabilities, 132 historic, final 112 | Q5 | 55, 56, 60, 61 | GROUNDED |
| C3-2 | 25 attempts per commit; same underlying model Gemini 3.6 flash; March 2026 cutoff | Q6, Q8 | 65, 71 | GROUNDED |
| C3-3 | Result: ~62% re-discovered, ~12% different bug, ~26% none | Q7 | 68 | GROUNDED |
| C3-4 | Memorization: no statistically significant amount pre-2026 for that model | NONE | 71 | GROUNDED |
| C3-5 | Follow-ups at 5 attempts: 10 = 8 + 7 (5 in both); combined ~70% correct, ~84% any bug; caution | Q10 | 82, 84 | GROUNDED |
| C3-6 | Experiment summary: ~60% overlap, 70% with different prompts | Q11 | 88 | GROUNDED |
| C3-7 | Rule: printed counts must appear; a bidirectional reading contradicts the experiment lines | NONE | 53-68, 82 | GROUNDED |
| C3-8 | Rejected: reverse direction was not run, being "more difficult to set up" | NONE | 53 | GROUNDED |
| C4-1 | Conclusion: complementary; recommend both; conclusion repeats complementary and specialized-fuzzing value | Q12, Q13, Q14 | 16, 281 | GROUNDED |
| C4-2 | Overlap uneven: more on "easy" bugs, smaller in JIT compilers; hard-for-fuzzer implies hard-for-agent | Q9 | 74, 90, 91 | GROUNDED |
| C4-3 | Post expects further model improvements, prompting and harnesses | Q15 | 281 | GROUNDED |
| C4-4 | Rule: replacing fuzzing, or agent superiority, contradicts Q13/Q14 | Q13, Q14 | 16, 281 | GROUNDED |
| C4-5 | Rejected: not vendor policy, bounty-program rule, intake channel or severity ladder; no intake or reward guidance | NONE | 9 (nav link only); no such content | GROUNDED |

## Word counts (`wc -w` per pinned quote; limit 25)

| Quote | Anchor | Words | ≤25 |
| Q1 | 12 | 10 | yes |
| Q2 | 16 | 23 | yes |
| Q3 | 40 | 18 | yes |
| Q4 | 51 | 14 | yes |
| Q5 | 61 | 10 | yes |
| Q6 | 65 | 11 | yes |
| Q7 | 68 | 24 | yes |
| Q8 | 71 | 17 | yes |
| Q9 | 74 | 19 | yes |
| Q10 | 82 | 20 | yes |
| Q11 | 88 | 19 | yes |
| Q12 | 16 | 7 | yes |
| Q13 | 16 | 25 | yes |
| Q14 | 281 | 16 | yes |
| Q15 | 281 | 14 | yes |

Max = 25 (Q13), at the limit; every other quote is below it. Counts are from `wc -w` on a temp file holding each quote's exact text (E3).

## Anchor check

Every inline `S093.txt:<n>` anchor in the entry (50 literal instances, 31 distinct expressions, plus the three `:N` shorthand continuations) names a line whose text supports the sentence. Distinct single-line anchors and their decisive text (line: first 110 chars):

| Line | Text |
| 12 | Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines |
| 13 | 2026-Oct-27 |
| 14 | Samuel Groß |
| 16 | Project Zero compared two automated tools used by Google … (summary: 45 vs 37, 25% overlap, complementary, recommend both) |
| 22 | For this blog post, we will limit ourselves to two concrete systems … both run in production … once per day |
| 23 | We also limit ourselves to V8 as a target … |
| 26 | … We limit our analysis to the six months from April to September 2026 … |
| 27 | Fuzzilli: hotlistid:5433121 created:2026-04-01..2026-09-30 |
| 28 | BigSleep: hotlistid:8067258 created:2026-04-01..2026-09-30 |
| 30 | Fuzzilli: 316 |
| 31 | BigSleep: 441 |
| 33 | Fuzzilli: 178 |
| 34 | BigSleep: 95 |
| 40 | So in terms of vulnerabilities, it's roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37. |
| 41 | … it's challenging to make a comparison at this stage in the research … |
| 51 | … we see an overlap of roughly 25% (20 out of a total of 81) … |
| 53 | … the other direction … is more difficult to set up, since fuzzers cannot easily be given a similar “starting point”. |
| 55 | … around 1150 raw bugs. |
| 56 | … roughly 600 vulnerabilities. |
| 60 | We end up with 132 historic bugs. |
| 61 | … This leaves us with a final number of 112 bugs. |
| 65 | We now run the agent for 25 attempts on each commit … the same underlying model: Gemini 3.6 flash. |
| 68 | … re-discover ~62% … a different … bug for another ~12% of commits. On around 26% … failed to find any bugs. |
| 71 | … knowledge cutoff date is March 2026 … there seems to be no statistically significant amount of memorization pre-2026. |
| 74 | … Bugs that are hard to find for a fuzzer are likely also hard to find for an AI agent. |
| 82 | … the agent re-discovered 10 additional bugs in total: 8 … and 7 … (with 5 found in both runs). |
| 84 | … the share of “correct” bugs found climbs to ~70%, and we find some kind of bug for ~84% of starting points … should be treated with some caution. |
| 88 | In our experiment, overlap was around 60% of historic Fuzzilli bugs (70% with additional runs …). |
| 90 | Bugs that are difficult for a fuzzer to find are more likely to also be difficult to find for an agent, so there’s more overlap on “easy” bugs. |
| 91 | The overlap seems to be smaller in the JIT Compilers and higher in the rest of the engine. |
| 281 | … the two approaches remain complementary, and specialized fuzzing continues to provide value … we expect further model improvements … |

Range anchors: 30-34 (raw + type:vulnerability counts), 33-34 (the narrowing), 53-68 (experiment setup through results). None is off by one. The three shorthand continuations `(S093.txt:27, :28)`, `(S093.txt:30, :31)` and `(S093.txt:33, :34)` were checked as well: line 28 = BigSleep query, line 31 = BigSleep 441, line 34 = BigSleep 95 (E5).

Quoted spans: 29 in-scope spans with a following citation, 27 byte-exact, 2 differing only in nested quotation marks (53, 90), 0 on the wrong line (E4). Numeric/date/byline check: 33/33 (E5).

## Notes (no row status changes)

- **N1 — C3-4, memorization modality.** Capture line 71 says "there seems to be no statistically significant amount of memorization pre-2026"; the entry says the check "finds" that text. The quoted fragment is verbatim and the quantitative claim is the post's; the entry's verb is firmer than the post's "seems". Row stays GROUNDED. A stricter wording would be: reports that "there seems to be no statistically significant amount of memorization pre-2026".
- **N2 — C3-7, rule range.** The rule sentence cites `S093.txt:53-68`, which covers the experiment setup and main results, while the follow-up counts it also requires (10 = 8 + 7, 5 in both) sit at line 82. The range is attached to the contradiction clause (attempt budget, sample sizes, shares, direction — all within 53-68), so the row stays GROUNDED; a precise citation would be `53-68, 82`.
- **N3 — nested quotation marks (C3-8, C4-2).** At 53 and 90 the capture has inner curly double quotes (“starting point”, “easy”); the entry renders them as single quotes inside its outer quotation. Content is identical (character-normalized match, `stripq` in Appendix A); the anchors are correct. A byte-exact substring test fails on these two spans only.
- **N4 — Q1 occurrence count.** Q1 occurs twice in the capture (page title line 1 and h1 line 12); the manifest anchors 12 and the on-line match holds there.
- **N5 — commit drift.** Lane HEAD measured `228118a` (three later round-60 commits: wave spec `b8c77fb`, lesson `fb6a928`, SCORECARD `228118a`; Pin block). The seat's target `7f7dd26` is an ancestor and the three target blobs are identical (E8), so the table is over the target bytes; no later commit touched the three files.

## Out of scope

- No lane instrument or suite was run (the seat names `wc -w` and the anchor check only); `source-recheck` and the frontier counters belong to other seats.
- The entry header's "independent curl open … 64812 bytes and carries the same text" (entry:3) is manifest-asserted provenance; it is not reproducible from the pinned artifacts and no network fetch was made in this seat.
- No tool installs were needed or performed; no scratch files remain (scratch dir `/fast/scratch/hyaku/kasegi-r60/EntryClaimTable` was deleted after this file was written).

## Appendix A — checker source (verbatim, for E3–E6)

```python
#!/usr/bin/env python3
# EntryClaimTable checker (kasegi r60 w1). Read-only on the lane.
# E3-E6 of .ufo/waves/round-60/w1/EntryClaimTable.md.
import json, re, subprocess, tempfile, os
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
ENTRY = L + "/corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md"
CAP = L + "/corpus/source-snapshots/round-60/S093.txt"
MAN = L + "/corpus/source-snapshots/round-60/manifest.json"
S = "/fast/scratch/hyaku/kasegi-r60/EntryClaimTable"

entry = open(ENTRY, encoding="utf-8").read()
lines = open(CAP, encoding="utf-8").read().splitlines()
quotes = json.load(open(MAN, encoding="utf-8"))["sources"][0]["quotes"]

def stripq(s):
    return re.sub(r"[\u2018\u2019\u201c\u201d\"']", "", s)

def parse_anchors(spec):
    nums = []
    for seg in spec.split("S093.txt:")[1:]:
        h = re.match(r"\s*(\d+)(?:-(\d+))?", seg)
        if h:
            nums.append(int(h.group(1)))
            if h.group(2):
                nums.extend(range(int(h.group(1)), int(h.group(2)) + 1))
        for sh in re.findall(r":\s*(\d+)", seg):
            nums.append(int(sh))
    return nums

print("== E3. manifest pinned quotes: anchor, occurrences, on anchor line, wc -w ==")
for it in quotes:
    qid, anchor, text = it["id"], it["anchor"], it["quote"]
    occ = len(re.findall(re.escape(text), open(CAP, encoding="utf-8").read()))
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=S) as f:
        f.write(text); fn = f.name
    w = int(subprocess.run(["wc", "-w", fn], capture_output=True, text=True).stdout.split()[0])
    os.unlink(fn)
    print(f"{qid}: anchor={anchor} occurrences={occ} on_anchor_line={text in lines[anchor-1]} wc_w={w}")

print("\n== E4. every quoted span in the entry vs the citation that follows it ==")
ok = qmark = fail = 0
for m in re.finditer(r'"([^"]{5,500})"', entry):
    tail = entry[m.end():m.end() + 260]
    a = re.search(r"\(S093\.txt:([^)]*)\)", tail)
    if not a:
        continue
    nums = parse_anchors("S093.txt:" + a.group(1))
    if any(m.group(1) in lines[n - 1] for n in nums):
        tag, ok = "OK-exact", ok + 1
    elif any(stripq(m.group(1)) in stripq(lines[n - 1]) for n in nums):
        tag, qmark = "OK-quote-marks-only", qmark + 1
    else:
        tag, fail = "FAIL", fail + 1
    print(f"{tag} anchors={nums} {m.group(1)[:90]!r}")
print(f"span checks: exact={ok} quote_marks_only={qmark} fail={fail} total={ok+qmark+fail}")

print("\n== E5. numeric/date/byline citations on their anchor line ==")
checks = [("2026-Oct-27", 13), ("Samuel Gro\u00df", 14), ("316", 30), ("441", 31),
          ("178", 33), ("95", 34), ("5433121", 27), ("8067258", 28),
          ("six months from April to September 2026", 26), ("45 vs. 37", 40),
          ("20 out of a total of 81", 51), ("1150", 55), ("600", 56), ("132", 60),
          ("112", 61), ("25 attempts", 65), ("Gemini 3.6 flash", 65), ("March 2026", 71),
          ("62%", 68), ("12%", 68), ("26%", 68), ("10 additional bugs", 82),
          ("8 from the different starting points", 82), ("7 with the rephrased prompt", 82),
          ("5 found in both", 82), ("70%", 84), ("84%", 84), ("some caution", 84),
          ("60% of historic Fuzzilli bugs", 88), ("overlap on \u201ceasy\u201d bugs", 90),
          ("JIT Compilers", 91), ("hard to find for an AI agent", 74),
          ("more difficult to set up", 53)]
bad = 0
for needle, n in checks:
    hit = needle in lines[n - 1]
    bad += 0 if hit else 1
    print(("OK  " if hit else "MISS") + f" line {n}: {needle!r}")
print(f"numeric/date/byline checks: {len(checks)-bad}/{len(checks)}")

print("\n== E6. inline anchor expressions ==")
c = Counter(re.findall(r"S093\.txt:([0-9]+(?:-[0-9]+)?)", entry))
print("instances:", sum(c.values()), "distinct:", len(c))
print(dict(sorted(c.items(), key=lambda kv: int(kv[0].split("-")[0]))))
```

Invocation: `TMPDIR=$S python3 $S/check_final.py` from the lane root, exit 0 (recreate the script from this appendix as `$S/check_final.py`; `$S=/fast/scratch/hyaku/kasegi-r60/EntryClaimTable`). The script reads only; it writes no lane file (temp files inside `$S` are removed by the script, and `$S` was removed after this file was written).
