# EntryClaimTable — F39 non-author claim table for `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md` against the committed capture `corpus/source-snapshots/round-58/S091.txt`

PASS WITH CORRECTIONS — every load-bearing sentence of the entry (Attribution, Claims 1-4, Limits) is supported by the capture at the cited line; no sentence universalises AISI's suite-bound estimate into a universal rate, forecast or capability verdict; all 19 quoted spans in the entry are verbatim in the capture (whitespace-normalised) and all are <= 25 words (max 22). 33 rows checked: 24 YES, 9 PARTIAL, 0 NO. Eight corrections are proposed as text in section 7 (none applied).

- Seat: `EntryClaimTable` (scribe), kasegi round 58 wave 1.
- Lane repo (read-only): `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (L).
- Lane tree HEAD at measurement time: `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b` (the implementation under test), working tree clean for the two files under test (`git -C L status --porcelain -- <entry> <capture-dir>` printed nothing).
- Freeze commit: `543cac13886b91ac660d788ed20e64ae70ee0fa5`, claims read from `L/.ufo/waves/round-58/claims.json` (never edited).
- Scratch root for this seat: `/fast/scratch/hyaku/kasegi-r58/EntryClaimTable` (removed at the end of the seat; see section 9).
- Tools installed: **none**. No `pacman`, no `uv tool install`, no binary download, no `npm -g`, no `cargo install` was run by this seat; the channel order in `/home/vgpnk/.omp/agent/RULES.md` was not needed (every command used is stock `coreutils`/`grep`/`python3` already present on the host). Nothing was written outside `L/.ufo/waves/round-58/w1/EntryClaimTable.md` and this seat's scratch.
- No credential material appears in this file: only path:line pointers and pattern names are reported.

---

## 1. Method

Every load-bearing sentence of the entry's Attribution, Claims 1-4 and Limits was split into one row. For each row the quoted span was extracted programmatically from the entry text, its word count was taken with `wc -w`, and its occurrence count and capture line were recomputed from the committed capture with a whitespace-normalised comparison (the same normalisation `corpus/instruments/source-recheck.py` uses — `normalize()` at `L/corpus/instruments/source-recheck.py:189`, `:211`). Verdicts:

- **YES** — the capture states the sentence's referent at the cited line.
- **PARTIAL** — the capture states it, but with a qualifier the entry drops, or the entry's rendering differs from the manifest's pinned assertion for the same referent.
- **NO** — not in the capture.

Gate-level facts asserted by the entry (capture date line, capture size, sha256) were re-computed from the capture bytes, not read from the manifest.

Scratch driver (reproducible): `/fast/scratch/hyaku/kasegi-r58/EntryClaimTable/verify.py` (written by this seat; removed with the scratch root). Its output is `verify.out` in the same directory.

---

## 2. Commands and their output

All commands below were run with `TMPDIR=/fast/scratch/hyaku/kasegi-r58/EntryClaimTable` and absolute paths. `L=/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `CAP=$L/corpus/source-snapshots/round-58/S091.txt`, `E=$L/corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md`.

### 2.1 Re-computed capture facts (item 4)

```
$ wc -c -l /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt
   67 11660 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt
exit=0

$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt
d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt
exit=0

$ sed -n '13p' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt
May 13, 2026
exit=0
```

Result — the entry's three Gate facts at `E:3` and `E:73` are **reproduced from the bytes**:

| Entry fact (`E:3`, `E:73`) | Entry value | Re-computed | Verdict |
|---|---|---|---|
| capture size (bytes) | 11660 (`E:3`) | 11660 | YES |
| capture lines | 67 (manifest `lines`) | 67 | YES |
| sha256 | `d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618` (`E:3`) | identical | YES |
| date line | `May 13, 2026` at `S091.txt:13` (`E:73`) | `sed -n '13p'` prints `May 13, 2026` | YES |

Manifest cross-check (`python3 -c` over `L/corpus/source-snapshots/round-58/manifest.json`): `bytes=11660 snapshot_bytes=11660 lines=67`, matching the byte count recomputed above; `fetched_bytes` field present in the manifest: **False** (see the note in section 6.3 on the entry's "33476 fetched" figure).

### 2.2 Manifest pinned quotes: word count, occurrences, anchor (all re-computed with `wc -w` and a capture scan)

```
Q1 anchor=1  words=11 occ=1 cap_line=[1]  anchor_ok=True
Q2 anchor=14 words=11 occ=1 cap_line=[14] anchor_ok=True
Q3 anchor=21 words=17 occ=1 cap_line=[21] anchor_ok=True
Q4 anchor=23 words=15 occ=1 cap_line=[23] anchor_ok=True
Q5 anchor=25 words=12 occ=1 cap_line=[25] anchor_ok=True
Q6 anchor=30 words=22 occ=1 cap_line=[30] anchor_ok=True
Q7 anchor=34 words=22 occ=1 cap_line=[34] anchor_ok=True
Q8 anchor=45 words=16 occ=1 cap_line=[45] anchor_ok=True
Q9 anchor=14 words=10 occ=1 cap_line=[14] anchor_ok=True
```

All nine manifest pins: occurrence 1, anchor resolves to the line holding the quote, max word count 22 <= 25. This independently reproduces the word counts recorded at `L/corpus/lessons/round-58.md:27-35` (Q1 11, Q2 11, Q3 17, Q4 15, Q5 12, Q6 22, Q7 22, Q8 16, Q9 10).

### 2.3 Entry quoted spans (word count per quote; occurrence and capture line)

Whitespace-normalised comparison against the capture; `wc -w` on the extracted span:

```
entry:20  words=11 occ_in_capture=1 cap_lines=[14] OK<=25 :: already an acceleration from our November 2025 estimate of 8 months
entry:22  words=12 occ_in_capture=1 cap_lines=[25] OK<=25 :: had doubled every 4.7 months since reasoning models emerged in late 2024
entry:23  words=6  occ_in_capture=1 cap_lines=[14] OK<=25 :: substantially exceeded both doubling rate trends
entry:24  words=10 occ_in_capture=1 cap_lines=[14] OK<=25 :: It is unclear whether this represents a new, faster trend.
entry:28  words=13 occ_in_capture=1 cap_lines=[23] OK<=25 :: an imperfect model, and is not a future prediction, nor a fixed law.
entry:34  words=12 occ_in_capture=1 cap_lines=[19] OK<=25 :: These tasks cover only some of the capabilities relevant to real-world cyberattacks.
entry:35  words=7  occ_in_capture=1 cap_lines=[20] OK<=25 :: For over a third of our tasks
entry:36  words=8  occ_in_capture=1 cap_lines=[20] OK<=25 :: we focus on a success threshold of 80%
entry:38  words=17 occ_in_capture=1 cap_lines=[21] OK<=25 :: We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time.
entry:39  words=6  occ_in_capture=1 cap_lines=[21] OK<=25 :: understates what frontier models can do
entry:40  words=16 occ_in_capture=1 cap_lines=[27] OK<=25 :: artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds.
entry:43  words=12 occ_in_capture=1 cap_lines=[33] OK<=25 :: against small, undefended enterprise networks, where initial access has already been gained.
entry:51  words=22 occ_in_capture=1 cap_lines=[30] OK<=25 :: Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months.
entry:53  words=16 occ_in_capture=1 cap_lines=[28] OK<=25 :: Longer time horizon estimates rely on only six tasks with durations of eight hours or more;
entry:60  words=3  occ_in_capture=3 cap_lines=[34, 36] OK<=25 :: The Last Ones
entry:60  words=2  occ_in_capture=1 cap_lines=[34] OK<=25 :: Cooling Tower
entry:62  words=22 occ_in_capture=1 cap_lines=[34] OK<=25 :: solving the range "The Last Ones" in 6 of 10 attempts and the previously unsolved "Cooling Tower" in 3 of 10 attempts
entry:63  words=16 occ_in_capture=1 cap_lines=[34] OK<=25 :: This was the first time that a model completed the second of our two cyber ranges.
entry:66  words=15 occ_in_capture=1 cap_lines=[35] OK<=25 :: These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting.
max_words=22 over25=0
```

Every quoted span in the entry is present verbatim in the capture; **max 22 words, none over 25**. The two range names at `E:60` ("The Last Ones" 3 words, "Cooling Tower" 2 words) are titles, not claims; "The Last Ones" occurs 3 times in the capture (L34, L36) — that is the capture's own repetition, not an entry defect.

### 2.4 Entry quote strings vs the manifest's pinned strings (whitespace-normalised)

```
Q1 entry_contains_manifest_string=False
Q2 entry_contains_manifest_string=True
Q3 entry_contains_manifest_string=True
Q4 entry_contains_manifest_string=False
Q5 entry_contains_manifest_string=True
Q6 entry_contains_manifest_string=True
Q7 entry_contains_manifest_string=True
Q8 entry_contains_manifest_string=False
Q9 entry_contains_manifest_string=True
entry Q4-rendering == manifest Q4 string: False
entry Q4-rendering words=13  manifest Q4 words=15
```

Q1 and Q8 are cited by the entry as anchors, not quoted inline (title at `E:3` as "title L1"; publisher at `E:13` as "Q8 names the publisher, S091.txt:45"), so their absence as inline strings is expected. **Q4 is different**: `E:28-29` quotes 13 words but labels the citation `(S091.txt:23 Q4)`, and the manifest's Q4 is a 15-word string. See row B6 and correction 2.

### 2.5 Overclaim scan (item 3) — forecast/verdict vocabulary in the entry

```
$ grep -nEi "will |shall |expect|forecast|predict|project|by 20[0-9][0-9]|soon|imminent|inevitable" <entry>
6:recheck: cd ... && python3 corpus/instruments/source-recheck.py ...   # lane recheck procedure line
29:and is not a future prediction, nor a fixed law." (S091.txt:23 Q4); so it is not a universal rate of
30:AI progress and not a forecast of any capability threshold.
exit=0
```

The only hits are the lane's own recheck command line and the entry's **negative** statements (quoting the capture's own disclaimer at `S091.txt:23` and asserting the figure is not a universal rate and not a forecast). **No forward-looking, universal-rate, forecast or capability-verdict sentence exists in the entry.** This is the decisive negative result for item 3 and it is what the verdict rests on.

### 2.6 The capture's own disclaimers, located for the overclaim assessment

```
$ grep -n 'these could be over- or underestimates' $CAP                       -> 20   (exit=0)
$ grep -n 'alongside our use of a simple agent scaffold' $CAP                 -> 27   (exit=0)
$ grep -n 'a bigger sample could include long tasks' $CAP                     -> 28   (exit=0)
$ grep -n 'we have only a few human baselines for the six longest tasks' $CAP -> 29   (exit=0)
$ grep -n 'Excluding Mythos Preview' $CAP                                    -> 44   (exit=0)
$ grep -n 'GPT-5.5 solved' $CAP                                              -> 34   (exit=0)
$ grep -n 'given a 2.5M token limit' $CAP                                    -> 25   (exit=0)
$ grep -n 'internally estimated|self-contained setups|our testing setup' $CAP -> 14, 19, 22 (exit=0)
$ grep -c 'closed' $CAP                                                      -> 0    (exit=1)
```

The `grep -c 'closed'` exit code 1 with count 0 is the decisive check for row A2: **the capture never uses the word "closed"**.

---

## 3. The claim table (33 rows)

Verdict key: YES / PARTIAL / NO. "Capture referent" gives the capture line holding the quoted text.

### Attribution

| # | Entry line | Load-bearing sentence (abridged) | Capture referent | Verdict |
|---|---|---|---|---|
| A1 | `E:10-12` | "The AI Security Institute's own blog report on its own measurement programme: what AISI estimates, how it bounds the estimate, what it says the estimate does not show, and the results of its cyber ranges." | L45 (publisher statement), L14+L25 (estimates), L19-L21 (bounds), L37-L38 ("What this evidence does not tell us..."), L33-L35 (ranges) | **YES** |
| A2 | `E:12-13` | "Every model result, doubling figure and range completion below is AISI's first-party statement about its own **closed testing** (Q8 names the publisher, S091.txt:45)." | L45 = Q8 ("The AI Security Institute is a research organisation within the Department of Science, Innovation and Technology."); "first-party" supported by L14 "we internally estimated"; but `grep -c 'closed'` = 0 — the capture says "self-contained setups" (L19), "our testing setup" (L22), "In AISI's latest testing" (L34) | **PARTIAL** (wording, not substance — see correction 3) |
| A3 | `E:13-15` | "This entry records those statements; it does not verify any model behaviour and does not verify the underlying runs, which the report does not publish." | No underlying run data in the capture; L37 "No single benchmark result should be read as a precise measure of AI capability"; L15 "evaluations are an imperfect measure" | **YES** |
| A4 | `E:15-16` | "It is documentation-only: it instructs no probing, scanning, login or submission against any target, and carries no credential material." | Entry-internal; the only command in the entry is the lane's own recheck command at `E:6` (a re-fetch procedure against the committed capture, not a target probe); credential-pattern scan of the entry matched only the benign tokens "token cap"/"success threshold" | **YES** |

### Claim 1

| # | Entry line | Load-bearing sentence (abridged) | Capture referent | Verdict |
|---|---|---|---|---|
| B1 | `E:18` (heading) | "AISI estimated the 80%-reliability cyber time horizon doubled every 4.7 months from late 2024, an acceleration from its own November 2025 estimate of 8 months, and says it is unclear whether the latest models start a new, faster trend" | L25 "frontier models' 80%-reliability cyber time horizon had doubled every 4.7 months since reasoning models emerged in late 2024"; L14 "already an acceleration from our November 2025 estimate of 8 months"; L14 Q9 / L25 "it's unclear whether Mythos Preview and GPT-5.5 represent an isolated break from existing rates of progress or are part of a new, faster trend" | **PARTIAL** (L25's condition "given a 2.5M token limit" is not attached to the figure here — correction 4) |
| B2 | `E:20-21` | "The February 2026 estimate is 'already an acceleration from our November 2025 estimate of 8 months' (S091.txt:14 Q2)" | L14, occurrence 1, 11 words, == manifest Q2 exactly | **YES** |
| B3 | `E:21-23` | "the report states the doubling directly: frontier models' 80%-reliability cyber time horizon 'had doubled every 4.7 months since reasoning models emerged in late 2024' (S091.txt:25 Q5)" | L25, occurrence 1, 12 words, == manifest Q5 exactly | **YES** |
| B4 | `E:23-24` | "**The same paragraph** says the latest models 'substantially exceeded both doubling rate trends' and that 'It is unclear whether this represents a new, faster trend.' (S091.txt:14 Q9)" | Both quoted fragments are at L14 (occ 1, 6 and 10 words); the preceding sentence cited L25, and L25 says "significantly outperformed this trend", not "substantially exceeded both doubling rate trends" | **PARTIAL** (the referent phrase points at the wrong paragraph — correction 1) |
| B5 | `E:25-27` | Falsifiable rule: "a reading that gives AISI's February 2026 doubling estimate as longer than its November 2025 estimate, or that presents the post-Mythos rate as an established new trend, contradicts the report as served on the recorded fetch date." | L14 + L25 (4.7 vs 8 months; "unclear whether ... a new, faster trend"), L37 ("it is too early to tell whether the step-change from recent models is representative of a new ongoing (or accelerating) pace") | **YES** |
| B6 | `E:27-30` | "the 4.7-month figure is AISI's suite-bound estimate under its own curve fit, which the report calls 'an imperfect model, and is not a future prediction, nor a fixed law.' (S091.txt:23 Q4); so it is not a universal rate of AI progress and not a forecast of any capability threshold." | L23 "we fit an exponential curve to historical results ... This is an imperfect model, and is not a future prediction, nor a fixed law."; L38 "What this evidence does not tell us is ... when AI will reach any particular capability threshold" | **PARTIAL** (the quoted string is 13 words; manifest Q4 is the 15-word string starting "This is" — correction 2) |

### Claim 2

| # | Entry line | Load-bearing sentence (abridged) | Capture referent | Verdict |
|---|---|---|---|---|
| C1 | `E:32` (heading) | "the measurement is bounded by its method: a narrow cyber suite, expert-time baselines, an 80% success threshold and a 2.5M token cap that AISI says understates what the models can do" | L19 ("our narrow cyber suite"), L19-L20 (expert baselines), L20 ("success threshold of 80%"), L21 ("This understates what frontier models can do.") | **YES** |
| C2 | `E:34-35` | "The suite is narrow by AISI's own statement: 'These tasks cover only some of the capabilities relevant to real-world cyberattacks.' (S091.txt:19)" | L19, occurrence 1, 12 words | **YES** |
| C3 | `E:35-37` | "Completion times are empirical 'For over a third of our tasks' and expert estimates for the rest (S091.txt:20); the headline threshold is 'we focus on a success threshold of 80%' (S091.txt:20)" | L20 for both spans (occ 1, 7 and 8 words) | **PARTIAL** (L20's caveat "these could be over- or underestimates" is dropped — correction 5a) |
| C4 | `E:37-39` | "The token cap is a comparability choice: 'We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time.' (S091.txt:21 Q3)" | L21, occurrence 1, 17 words, == manifest Q3 exactly | **YES** |
| C5 | `E:39-40` | "and the report states that it 'understates what frontier models can do' (S091.txt:21)" | L21 "This understates what frontier models can do.", occ 1, 6 words | **YES** |
| C6 | `E:40-41` | "and that the cap 'artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds.' (S091.txt:27)" | L27, occ 1, 16 words; but L27 attributes the effect to "The cap, **alongside our use of a simple agent scaffold**" | **PARTIAL** (the scaffold conjunct is dropped — correction 5b) |
| C7 | `E:41-44` | Falsifiable rule: "a reading that treats the suite's time horizons as an upper bound on model capability, or as a measure of defended real-world systems, contradicts these statements." | L21 + L27 (cap understates capability), L38 ("how these capabilities will translate against defended, real-world systems"), L33 ("small, undefended enterprise networks") | **YES** |
| C8 | `E:43-44` | "The cyber ranges are described as measuring attacks 'against small, undefended enterprise networks, where initial access has already been gained.' (S091.txt:33)" | L33, occ 1, 12 words | **YES** |
| C9 | `E:45-47` | "Rejected over-generalizations: the time horizons are not a capability leaderboard across cyber work as a whole, and the human baselines are a timed sample for over a third of tasks, not a certified difficulty standard." | L37 ("No single benchmark result should be read as a precise measure of AI capability"), L38, L32 (METR is "a skillset related to cyber, but broader"), L20 (over a third timed / remainder estimated) | **YES** (conservative direction: the entry's rejected readings are all readings the capture itself refuses) |

### Claim 3

| # | Entry line | Load-bearing sentence (abridged) | Capture referent | Verdict |
|---|---|---|---|---|
| D1 | `E:49` (heading) | "AISI states its uncertainty: a single-model omission moves the pre-Mythos doubling estimate only within 4.1 to 5.0 months, and the longest tasks rest on six tasks" | L30 "Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months." (the "single omission" is of a model — L30 "fit on only a small number of models ... the trend does not hinge on individual models"); L28 "Longer time horizon estimates rely on only six tasks with durations of eight hours or more"; L29 "the six longest tasks" | **YES** |
| D2 | `E:51-52` | "The report bounds one sensitivity: 'Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months.' (S091.txt:30 Q6)" | L30, occ 1, 22 words, == manifest Q6 exactly | **YES** |
| D3 | `E:52-54` | "It names the longest-task limit: 'Longer time horizon estimates rely on only six tasks with durations of eight hours or more;' (S091.txt:28)" | L28, occ 1, 16 words; the capture sentence continues past the semicolon: "a bigger sample could include long tasks that AI models find harder or easier than those we currently evaluate, reducing or increasing time horizon estimates" | **PARTIAL** (the quote stops at the semicolon and drops the direction-of-error caveat — correction 5c) |
| D4 | `E:54-58` | Falsifiable rule + "Rejected over-generalization: the 4.1-to-5.0 band is the single-omission sensitivity of the pre-Mythos fit (S091.txt:30), not a statistical interval on any later estimate." | L30 (explicitly "pre-Mythos doubling time estimate"), L25 (the 4.7-month figure is "given a 2.5M token limit", i.e. pre-Mythos), L37-L38 | **YES** |

### Claim 4

| # | Entry line | Load-bearing sentence (abridged) | Capture referent | Verdict |
|---|---|---|---|---|
| E1 | `E:60` (heading) | "AISI reports a newer Mythos Preview checkpoint solved both of its cyber ranges, 'The Last Ones' in 6 of 10 attempts and the previously unsolved 'Cooling Tower' in 3 of 10" | L34 "the newer Mythos Preview checkpoint completed both our cyber ranges, solving the range 'The Last Ones' in 6 of 10 attempts and the previously unsolved 'Cooling Tower' in 3 of 10 attempts."; L16 "including the first completion of both our cyber ranges" | **PARTIAL** (the capture's same-line result for GPT-5.5 is not recorded — correction 7) |
| E2 | `E:62-63` | "The report states: 'solving the range "The Last Ones" in 6 of 10 attempts and the previously unsolved "Cooling Tower" in 3 of 10 attempts' (S091.txt:34 Q7)" | L34, occ 1, 22 words, == manifest Q7 exactly | **YES** |
| E3 | `E:63-64` | "and 'This was the first time that a model completed the second of our two cyber ranges.' (S091.txt:34)" | L34, occ 1, 16 words | **YES** |
| E4 | `E:64-68` | Falsifiable rule + "The caveat is stated: 'These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting.' (S091.txt:35)" | L35, occ 1, 15 words; L16 ("we received access to a newer checkpoint") supports the earlier-checkpoint rule | **YES** |
| E5 | `E:68-69` | "Rejected over-generalization: these are one checkpoint's attempt counts on two bespoke ranges, not a reproducible public benchmark, and they are not comparable to earlier published checkpoint results without that caveat." | L35 (checkpoint caveat), L33 ("more detail on them can be found in our recent paper" — not opened by this entry), L37 | **YES** (the entry's own restriction is consistent with the capture) |

### Limits

| # | Entry line | Load-bearing sentence (abridged) | Capture referent | Verdict |
|---|---|---|---|---|
| F1 | `E:73-75` | "The page is a dated blog post (May 13, 2026, S091.txt:13). Byte stability is asserted within this round's opens only; the 90d row recheck re-fetches, and a changed estimate, a newer post or an edited page supersedes by a new row (R8)." | L13 = "May 13, 2026" (re-computed); "we internally estimated" (L14) and "At the time of writing" (L25) are the capture's own dated-voice markers; registry row S091 recheck = `90d` (SOURCES.md:98, field 11) and opened 2026-11-03; R8 defined at `L/corpus/QUALITY.md:50` and applied at `L/corpus/SOURCES.md:215` | **YES** |
| F2 | `E:76-78` | "METR's software-engineering doubling time of 4.2 months (S091.txt:32, footnote 3 at S091.txt:44) is a different programme's figure, named by the report and not absorbed here" | L32 "Their results imply a consistent doubling time of 4.2 months on software tasks since late 2024"; L44 footnote 3 "Excluding Mythos Preview, the estimated doubling time is 4.2 months; when included, this accelerates slightly to 4 months"; L32 "a research non-profit ... a skillset related to cyber, but broader" | **PARTIAL** (footnote 3's "Excluding Mythos Preview" condition is dropped — correction 5d) |
| F3 | `E:78` | "the linked Frontier AI Trends Report (S091.txt:2) is named and not opened: a lead, not a row." | L2 "Read the Frontier AI Trends Report" | **YES** |
| F4 | `E:79-80` | "The report's three footnotes (S091.txt:42-44) carry the suite's scope caveats and are read as part of the statements above, not as separate sources." | L42, L43, L44 are the three numbered footnotes (L41 is a zero-width joiner line); L42 "AISI's narrow cyber suite is used to estimate time horizons"; L43 cap/long-task detail; L44 METR estimate | **YES** |
| F5 | `E:81-83` | "Adjacency: LLM evaluation and benchmark method is kengaku's province (PROVINCE.md, Adjacent)." | `L/PROVINCE.md:43` "## Adjacent", listing "kengaku — LLM evaluation and benchmarks" | **YES** |

### Tally

**YES 24 · PARTIAL 9 · NO 0 · total 33 rows.**

Counted from the table itself: `grep -cE "^\| (A[1-4]|B[1-6]|C[1-9]|D[1-4]|E[1-5]|F[1-5]) \|" EntryClaimTable.md` = 33; of those rows, 24 end in `**YES**` and 9 in `**PARTIAL**`.

PARTIAL rows: A2, B1, B4, B6, C3, C6, D3, E1, F2. No sentence in the entry is unsupported by the capture; every PARTIAL is a dropped qualifier, a label/wording mismatch, or a coverage gap — not a false statement.

---

## 4. Quote word counts — every quote in the entry

`wc -w` on each extracted span (the same measurement the lesson records at `L/corpus/lessons/round-58.md:27-35`):

| Entry line | Quote | Words | <= 25 |
|---|---|---|---|
| 20 | "already an acceleration from our November 2025 estimate of 8 months" (= manifest Q2) | 11 | yes |
| 22 | "had doubled every 4.7 months since reasoning models emerged in late 2024" (= manifest Q5) | 12 | yes |
| 23 | "substantially exceeded both doubling rate trends" | 6 | yes |
| 24 | "It is unclear whether this represents a new, faster trend." (= manifest Q9) | 10 | yes |
| 28 | "an imperfect model, and is not a future prediction, nor a fixed law." | 13 | yes |
| 34 | "These tasks cover only some of the capabilities relevant to real-world cyberattacks." | 12 | yes |
| 35 | "For over a third of our tasks" | 7 | yes |
| 36 | "we focus on a success threshold of 80%" | 8 | yes |
| 38 | "We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time." (= manifest Q3) | 17 | yes |
| 39 | "understates what frontier models can do" | 6 | yes |
| 40 | "artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds." | 16 | yes |
| 43 | "against small, undefended enterprise networks, where initial access has already been gained." | 12 | yes |
| 51 | "Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months." (= manifest Q6) | 22 | yes |
| 53 | "Longer time horizon estimates rely on only six tasks with durations of eight hours or more;" | 16 | yes |
| 60 | "The Last Ones" (range title) | 3 | yes |
| 60 | "Cooling Tower" (range title) | 2 | yes |
| 62 | "solving the range "The Last Ones" in 6 of 10 attempts and the previously unsolved "Cooling Tower" in 3 of 10 attempts" (= manifest Q7) | 22 | yes |
| 63 | "This was the first time that a model completed the second of our two cyber ranges." | 16 | yes |
| 66 | "These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting." | 15 | yes |

**Max 22 words, 19 spans, none over 25.** The longest (22) is Q6 at `E:51` and Q7 at `E:62`; both equal the manifest's own counts.

---

## 5. Overclaims (item 3) — flagged with the capture line

**No overclaim of the specified kind was found.** The entry never generalises AISI's suite-bound estimate into a universal rate, a forecast, or a capability verdict; the scan in section 2.5 returns only the lane's recheck command and the entry's two *negative* statements. The capture's own disclaimers are carried by the entry at the right places:

| Capture disclaimer | Entry site |
|---|---|
| L23 "This is an imperfect model, and is not a future prediction, nor a fixed law." | `E:28-30` (quoted, with the caveat attached) |
| L37 "No single benchmark result should be read as a precise measure of AI capability." / L38 "What this evidence does not tell us is how the pace of progress will evolve, when AI will reach any particular capability threshold..." | `E:27-30` (as the rejected over-generalisation) |
| L21 "This understates what frontier models can do." + L27 "artificially lowers success rates..." | `E:39-41` |
| L30 "pre-Mythos doubling time estimate" | `E:51-58` (the pre-Mythos restriction is stated twice, in the heading and the rejected over-generalisation) |
| L35 "These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting." | `E:66-67` (quoted as the report's own caveat) |
| L33 "small, undefended enterprise networks, where initial access has already been gained." | `E:43-44` |

The following are **dropped caveats** — the capture states them, the entry omits them. None turns a sentence into a false statement, so each is reported as PARTIAL and as a text correction, not as an overclaim. The last column maps each to the proposed wording in section 7:

| # | Capture line | Dropped qualifier | Where the entry drops it | Correction |
|---|---|---|---|---|
| 1 | L20 | "The remainder use expert estimates for completion times, rather than empirical baselines; **these could be over- or underestimates**." | `E:35-36` states "expert estimates for the rest" bare (row C3) | 5a |
| 2 | L27 | "The cap, **alongside our use of a simple agent scaffold**, artificially lowers success rates and understates what models can do..." | `E:40-41` attributes the effect to the cap alone (row C6) | 5b |
| 3 | L28 | the clause after the semicolon: "a bigger sample could include long tasks that AI models find harder or easier than those we currently evaluate, **reducing or increasing time horizon estimates**." | `E:53-54` stops its quote at the semicolon, dropping the direction-of-error caveat (row D3) | 5c |
| 4 | L25 | "had doubled every 4.7 months since reasoning models emerged in late 2024, **given a 2.5M token limit**." | `E:18` (Claim 1 heading) does not attach the token-limit condition to the doubling figure (the cap is covered under Claim 2) (row B1) | 4 |
| 5 | L29 | "different experts could be faster or slower than the ones we timed" and "we have only a few human baselines for the six longest tasks." | not carried anywhere in the entry | none proposed — the entry already refuses the leaderboard reading (row C9), so this is recorded for the round report only |
| 6 | L44 | footnote 3: "**Excluding Mythos Preview**, the estimated doubling time is 4.2 months; when included, this accelerates slightly to 4 months." | `E:76` states the 4.2-month figure flatly (row F2) | 5d |
| 7 | L34 | "**GPT-5.5 solved "The Last Ones" on 3 of 10 attempts.**" | `E:60` (Claim 4 heading) records only the Mythos Preview checkpoint's range results; the entry never claims exclusivity, so this is a coverage gap in a paragraph that is explicitly about range comparability (row E1) | 7 |
| 8 | L19 | "testing skills such as reverse engineering and web exploitation in **self-contained setups**" | supports A2's "closed testing" but is not the capture's wording (`grep -c 'closed'` = 0) (row A2) | 3 |

---

## 6. Gate-level facts asserted by the entry — re-computed

### 6.1 Reproduced

See section 2.1. The entry's `E:3` "11660 snapshot bytes", sha256 `d2ba7199…820618`, and `E:73` "May 13, 2026, S091.txt:13" are all reproduced from the capture bytes by `wc -c -l`, `sha256sum` and `sed -n '13p'`.

### 6.2 The entry's line-anchor map (`E:3`) — every anchor checked against the capture

| Entry anchor | What the entry claims it carries | Capture content at that line | Verdict |
|---|---|---|---|
| "title L1" | page title | L1 "How fast is autonomous AI cyber capability advancing? \| AISI Work" (= manifest Q1) | YES |
| "date L13" | post date | L13 "May 13, 2026" | YES |
| "estimate and acceleration L14" | 4.7-month estimate + acceleration from 8 months | L14 carries both | YES |
| "method L19-L21" | suite, baselines, threshold, token cap | L19 suite/expert baselines, L20 baselines+threshold, L21 cap | YES |
| "threshold L20" | 80% success threshold | L20 "we focus on a success threshold of 80%" | YES |
| "80% time-horizon doubling L25" | the doubling statement | L25 "frontier models' 80%-reliability cyber time horizon had doubled every 4.7 months" | YES |
| "token-cap statement L21 and L27" | the cap statement | L21 "This understates what frontier models can do."; L27 "artificially lowers success rates..." | YES |
| "uncertainty L28-L30" | uncertainty block | L28 six tasks, L29 human baselines, L30 omission band | YES |
| "cyber ranges L33-L35" | range description, results, caveat | L33 range framing, L34 results, L35 checkpoint caveat | YES |
| "publisher statement L45" | publisher | L45 "The AI Security Institute is a research organisation within the Department of Science, Innovation and Technology." (= manifest Q8) | YES |

The header's "9 pinned assertions Q1-Q9, each occurrences=1 at its anchor" is **reproduced**: section 2.2 shows 9/9 with occurrence 1 and a resolving anchor.

### 6.3 Two provenance points in the header (`E:3`) that are not reproducible from the committed capture or manifest

1. **"over 33476 fetched"** — the manifest carries no fetched-byte field (`fetched_bytes` present in the manifest JSON: **False**); it records only `bytes=11660` / `snapshot_bytes=11660`, i.e. the snapshot size, which is the number the entry's own "11660 snapshot bytes" refers to. The 33476 figure is the raw HTML body size that `corpus/instruments/capture-source.py` prints as `fetched_bytes` (instrument source: `L/corpus/instruments/capture-source.py:95-96`). It is corroborated inside the lane by `L/corpus/lessons/round-58.md:26` ("33476 fetched bytes") and, independently, by the sibling seat's re-fetch recorded at `L/.ufo/waves/round-58/w1/ScoutSources.md:30` and `:325` ("33476 … S091.raw.html"; sha256 `ce714d89…` of the raw body, which is necessarily different from the snapshot digest `d2ba7199…` because one is raw HTML and the other whitespace-collapsed text). The figure is therefore consistent but is not verifiable from the committed capture/manifest alone. **Reported, not claimed as a defect.**
2. **"a second same-sha open at 20:35:32Z and a third recorded open at 20:35:59Z"** — the manifest's `fetch_method` says "**two** same-sha opens recorded (probe 20:35:32Z, recorded + verification re-open 20:35:59Z)", and `L/corpus/lessons/round-58.md:26` likewise says "**two** same-sha opens this round: 20:35:32Z probe and 20:35:59Z recorded/verification". The entry's wording enumerates a second and a third open, i.e. it implies three opens where the manifest and the lesson record two. This is a count/wording discrepancy in the header, not in the claim bodies. See correction 6.

### 6.4 The entry's `recheck:` line (`E:6`) — exit-code claims exercised on scratch copies

The entry claims the recheck "exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote moved, so a missing or corrupted capture fails closed". Exercised on scratch copies of the manifest and capture (the lane tree was not modified; the scratch root was removed afterwards):

```
$ python3 <L>/corpus/instruments/source-recheck.py --manifest <scratch>/t3/nope.json --source S091
manifest UNAVAILABLE reason=missing
EXIT=2                                  # manifest absent -> exit 2  (matches the entry)

$ python3 ... --manifest <scratch>/t4/manifest.json --source S091      # capture file removed
S091:source UNAVAILABLE reason=missing
EXIT=2                                  # capture absent -> exit 2  (matches the entry)

$ python3 ... --manifest <scratch>/t1/manifest.json --source S091      # sha256 zeroed in the manifest
S091:sha256 MISMATCH expected=000...0 actual=d2ba7199...0618
EXIT=1                                  # digest differs -> exit 1  (matches the entry)

$ python3 ... --manifest <scratch>/t5/manifest.json --source S091      # Q4's sentence removed, sha re-pinned to the edited capture
S091:sha256 OK
S091:Q4 MISMATCH reason=quote-not-found
EXIT=1                                  # a pinned quote is absent -> exit 1  (matches the entry)

$ python3 ... --manifest <scratch>/t6/manifest.json --source S091      # Q4's sentence RELOCATED to another line, sha re-pinned
S091:sha256 OK
S091:Q4 OK occurrences=1 anchor=23-BROKEN
EXIT=0                                  # a quote that MOVED but still occurs once -> exit 0
```

The last case is the one the entry overstates: the instrument's anchor check only gates on `occurrences > 1` (`L/corpus/instruments/source-recheck.py:192`, `if occurrences > 1 and anchor_verdict_result != "ok"`), so a quote whose *anchor* no longer holds is reported as `anchor=NN-BROKEN` in the note while the line still prints `OK` and the run exits 0. A moved quote that is still present in the capture therefore does **not** produce exit 1, although the entry's `recheck:` line says it does. (The `anchor=BROKEN` note is still visible in the output, so the drift is not silent.) This is the entry's recheck-description row, outside the Attribution/Claims/Limits scope proper; reported here because it is a statement the entry makes about its own verification procedure.

---

## 7. Proposed corrections — TEXT ONLY (the entry was not edited)

No file under `L` was modified by this seat. The corrections below are for the round's report / the next editor; they are not applied.

**Correction 1 — `E:23-24` (row B4), referent phrase.**
Current: `The same paragraph says the latest models "substantially exceeded both doubling rate trends" and that "It is unclear whether this represents a new, faster trend." (S091.txt:14 Q9).`
Proposed: `The February 2026 summary paragraph says the latest models "substantially exceeded both doubling rate trends" and that "It is unclear whether this represents a new, faster trend." (S091.txt:14 Q9).`
Reason: the preceding sentence cited `S091.txt:25`; both quoted fragments are at `S091.txt:14` (occ 1 each), and `S091.txt:25` says "significantly outperformed this trend", so "the same paragraph" points at the wrong paragraph.

**Correction 2 — `E:28-29` (row B6), Q4 string mismatch.**
Current: `which the report calls "an imperfect model, and is not a future prediction, nor a fixed law." (S091.txt:23 Q4)`
Proposed: `which the report calls "This is an imperfect model, and is not a future prediction, nor a fixed law." (S091.txt:23 Q4)`
Reason: the manifest's pinned Q4 is the 15-word string beginning "This is"; the entry's 13-word rendering is a truncation of it, so the "(… Q4)" label does not name the string actually quoted. Quoting the pinned form restores label/string equality (15 words, still <= 25).

**Correction 3 — `E:12-13` (row A2), "closed testing" is not the capture's wording.**
Current: `Every model result, doubling figure and range completion below is AISI's first-party statement about its own closed testing (Q8 names the publisher, S091.txt:45).`
Proposed: `Every model result, doubling figure and range completion below is AISI's first-party statement about its own internal, self-contained testing (Q8 names the publisher, S091.txt:45).`
Reason: `grep -c 'closed'` on the capture returns 0 (exit 1); the capture's own terms are "we internally estimated" (L14), "self-contained setups" (L19) and "our testing setup" (L22). The substance (first-party, AISI's own) is unaffected.

**Correction 4 — `E:18` (row B1), the token-limit condition on the doubling figure.**
Current: `## Claim 1 — AISI estimated the 80%-reliability cyber time horizon doubled every 4.7 months from late 2024, an acceleration from its own November 2025 estimate of 8 months, and says it is unclear whether the latest models start a new, faster trend`
Proposed: `## Claim 1 — AISI estimated the 80%-reliability cyber time horizon, given a 2.5M token limit, doubled every 4.7 months from late 2024, an acceleration from its own November 2025 estimate of 8 months, and says it is unclear whether the latest models start a new, faster trend`
Reason: `S091.txt:25` conditions the doubling estimate on "given a 2.5M token limit"; the entry attaches the cap to the method (Claim 2) but not to this figure.

**Correction 5 — dropped caveats, four sites (rows C3, C6, D3, F2).**
5a. `E:35-36`. Current: `Completion times are empirical "For over a third of our tasks" and expert estimates for the rest (S091.txt:20);`
Proposed: `Completion times are empirical "For over a third of our tasks" and expert estimates for the rest, which the report says "could be over- or underestimates" (S091.txt:20);`
Reason: `S091.txt:20` states the caveat; the entry states the fact without it. The added span is 5 words, so the quoted spans stay within 25 words.
5b. `E:40-41`. Current: `and that the cap "artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds." (S091.txt:27)`
Proposed: `and that the cap, alongside the simple agent scaffold the report uses, "artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds." (S091.txt:27)`
Reason: `S091.txt:27` attributes the effect to the cap *and* the simple agent scaffold.
5c. `E:53-54`. Current: `It names the longest-task limit: "Longer time horizon estimates rely on only six tasks with durations of eight hours or more;" (S091.txt:28).`
Proposed: `It names the longest-task limit: "Longer time horizon estimates rely on only six tasks with durations of eight hours or more" (S091.txt:28), and adds that a bigger sample could include long tasks AI finds harder or easier, reducing or increasing the estimates.`
Reason: the capture's direction-of-error clause after the semicolon is dropped by the entry's truncation. The full capture clause quoted verbatim would be 41 words (measured: `wc -w` = 41), over the entry's own <= 25-word rule, so the caveat must be paraphrased outside the quotation marks; the quoted span stays at 16 words.
5d. `E:76`. Current: `METR's software-engineering doubling time of 4.2 months (S091.txt:32, footnote 3 at S091.txt:44) is a`
Proposed: `METR's software-engineering doubling time of 4.2 months, which the report's footnote 3 gives excluding Mythos Preview (4 months with it) (S091.txt:32, footnote 3 at S091.txt:44), is a`
Reason: `S091.txt:44` conditions the 4.2-month figure.

**Correction 6 — `E:3` (header), open count.**
Current: `a second same-sha open at 20:35:32Z and a third recorded open at 20:35:59Z are byte-identical`
Proposed: `a same-sha probe open at 20:35:32Z and the recorded-plus-verification re-open at 20:35:59Z are byte-identical`
Reason: the manifest's `fetch_method` and `L/corpus/lessons/round-58.md:26` both record **two** same-sha opens, not three.

**Correction 7 — `E:60` / `E:62` (row E1), the second range result on the same capture line.**
Current (heading): `## Claim 4 — AISI reports a newer Mythos Preview checkpoint solved both of its cyber ranges, "The Last Ones" in 6 of 10 attempts and the previously unsolved "Cooling Tower" in 3 of 10`
Proposed: `## Claim 4 — AISI reports a newer Mythos Preview checkpoint solved both of its cyber ranges, "The Last Ones" in 6 of 10 attempts and the previously unsolved "Cooling Tower" in 3 of 10, while GPT-5.5 solved "The Last Ones" on 3 of 10`
Reason: `S091.txt:34` records the GPT-5.5 result on the same line the entry cites; recording it prevents the entry from implying a single model cleared a range.

**Correction 8 — `E:6` (recheck line), exit-code description.**
Current: `exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote moved, so a missing or corrupted capture fails closed`
Proposed: `exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote is absent from the capture, so a missing or corrupted capture fails closed; a pinned quote whose anchor no longer holds is printed as "anchor=NN-BROKEN" and still exits 0`
Reason: section 6.4 — the instrument gates the anchor check on `occurrences > 1` (`L/corpus/instruments/source-recheck.py:192`).

---

## 8. Out of scope / not claimed by this seat

- The ledger, the frozen claims (`claims.json`), `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, the knowledge file and every instrument were **read only**. No edit, no `git add`/`commit`/`stash`/`checkout`/`switch`/`reset`/`pull`/`push`, no `jj` command against `L`.
- The lane's counters (`frontier-recheck-count.py`, `source-recheck.py --source S091` against the *lane* manifest, `capture-binding-check.py`, `sources-census.sh`) belong to the C2 review seat and the C2 count claims; this seat did not run them and claims nothing about the census numbers. The only `source-recheck.py` runs here were on **scratch copies** of the manifest/capture, to exercise the exit-code limbs the entry's `recheck:` line describes (section 6.4).
- The registry row S091 (`corpus/SOURCES.md:98`) and the frontier row F39 (`corpus/README.md:964`) were read only as cross-checks for the entry's `ground: F39` line and the "90d" recheck claim (row F1); this seat does not claim the registry or census state.
- The sibling-lane overlap question (kengaku adjacency) is the SiblingOverlap seat's scope; row F5 records only that `PROVINCE.md:43-49` lists kengaku as adjacent.
- No credential material, token, cookie, session value or `op://` reference appears in this evidence file; only path:line pointers and pattern names are used.

---

## 9. Scratch and hygiene

- Scratch root: `/fast/scratch/hyaku/kasegi-r58/EntryClaimTable` — created with `mkdir -p`, used for the driver `verify.py` / `verify.out`, the `wq/`, `wq2/` word-count files and the `mv/`, `t1`-`t6/` fixture copies of the manifest and capture. Removed with `rm -rf -- /fast/scratch/hyaku/kasegi-r58/EntryClaimTable` before this seat yielded; no leftover.
- `TMPDIR=/fast/scratch/hyaku/kasegi-r58/EntryClaimTable` was exported for every command that wrote.
- The lane tree was never written to; the only file created under `L` is this evidence file, `L/.ufo/waves/round-58/w1/EntryClaimTable.md`.
- Pre-existing lane modifications, **not** this seat's: `git -C L status --porcelain` also shows ` M LOG.md`, ` M SCORECARD.md`, ` M corpus/QUALITY.md` (mtimes 17:51:50-17:52:23, i.e. before this seat's first write at 18:07:50; `git -C L diff --stat` on them: 44 insertions). These are another actor's in-flight round edits and were left untouched. HEAD remained `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b` for the whole seat; no index, worktree or history mutation was performed by this seat.
