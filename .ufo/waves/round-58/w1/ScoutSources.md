VERDICT: AGREE — 9/9 quotes occur exactly once in independent re-open; 23/23 citations in knowledge file resolve to their stated referent; independent fetch and lane conversion byte-for-byte reproduce committed snapshot (sha256 d2ba7199...); source-recheck.py exits 0; no claim-killing disagreement found.

DETAIL: S091 (https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing) was independently re-opened using curl with an independent User-Agent (HTTP 200, 33476 raw HTML bytes, sha256 ce714d89...). Running the lane instrument's html_to_text conversion on this independent fetch reproduces the committed snapshot byte-for-byte (11660 bytes, 67 lines, sha256 d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618; identical=True). Independent conversion using Python stdlib html.parser produces 11664 bytes, 71 lines, sha256 fd8d40a23c414cbc9c80a7be2744827453cafe8f60e926cf08d30b0d6558e046. The +4 lines difference is entirely accounted for by block element separation (<figcaption> before paragraphs and <h3>, plus navigation link splitting). Every one of quotes Q1–Q9 occurs exactly once in the independent text with zero mismatches. All 23 line-anchor citations (S091.txt:NN) in corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md resolve to their named referents in the committed capture. The lane instrument source-recheck.py exits 0 with all 9 quotes verified.

Seat: ScoutSources (round 58 wave 1, kasegi lane). Role: independent verifier, not author.
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin (read-only).
Scratch root: /fast/scratch/hyaku/kasegi-r58/ScoutSources (cleaned before final yield).
Wave evidence dir: /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-58/w1/
Lane HEAD commit: 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b (claims freeze 543cac13886b91ac660d788ed20e64ae70ee0fa5).

Tooling installed/upgraded: NONE (used host curl 8.23.0 and python3 3.14.8 already present; no pacman, no uv, no ~/.local/bin writes).

=====================================================================
1. FETCH — S091 URL, independent UA, single GET
=====================================================================

Command:
  S=/fast/scratch/hyaku/kasegi-r58/ScoutSources
  mkdir -p "$S"
  url="https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing"
  http_code=$(curl -sS -L --max-time 60 \
    -A 'kasegi-research-verifier/1.0 (independent re-open; contact: operator)' \
    -o "$S/S091.raw.html" -w '%{http_code}' "$url")
  echo "HTTP_CODE=$http_code"
  wc -c "$S/S091.raw.html"
  sha256sum "$S/S091.raw.html"

Printed output:
  HTTP_CODE=200
  33476 /fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.raw.html
  ce714d89f7305102934b73182d1f78060ea9a12b45e8aad647e96d55db6607cd  /fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.raw.html
  exit code: 0

Note on bytes: The fetched byte count of 33476 bytes exactly matches the fetched size recorded in the knowledge file header (corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:3: "11660 snapshot bytes over 33476 fetched").

=====================================================================
2. INDEPENDENT CONVERSION — Python stdlib html.parser
=====================================================================

Method: Python stdlib html.parser.HTMLParser streaming text extractor, deliberately differing from the regex-substitution method in corpus/instruments/capture-source.py:48-53.
- Skips non-visible tags: <script>, <style> (using depth tracking).
- Separates structural block elements: emits newlines on open and close for {'p', 'div', 'li', 'tr', 'h1'..'h6', 'section', 'article', 'br', 'header', 'footer', 'nav', 'main', 'aside', 'figure', 'figcaption', 'title', 'blockquote', etc.}.
- Automatically converts character entity references (convert_charrefs=True).
- Per-line whitespace collapse: ' '.join(line.split()) for each non-empty line.

Converter script: $S/indep_convert.py

Command:
  python3 "$S/indep_convert.py" "$S/S091.raw.html" "$S/S091.independent.txt"
  wc -l -c "$S/S091.independent.txt"
  sha256sum "$S/S091.independent.txt"

Printed output:
  71 11664 /fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.independent.txt
  fd8d40a23c414cbc9c80a7be2744827453cafe8f60e926cf08d30b0d6558e046  /fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.independent.txt
  exit code: 0

---------------------------------------------------------------------
2a. TRANSITIVE CHECK — Lane conversion on independent fetch raw HTML
---------------------------------------------------------------------
Command:
  python3 -c "
  import sys, hashlib
  sys.path.insert(0, '/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments')
  cs = __import__('capture-source')
  with open('/fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.raw.html', 'r', encoding='utf-8') as f:
      raw = f.read()
  conv = cs.html_to_text(raw)
  with open('/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt', 'r', encoding='utf-8') as f:
      comm = f.read()
  print('conv_bytes:', len(conv.encode('utf-8')), 'comm_bytes:', len(comm.encode('utf-8')))
  print('conv_sha256:', hashlib.sha256(conv.encode('utf-8')).hexdigest())
  print('comm_sha256:', hashlib.sha256(comm.encode('utf-8')).hexdigest())
  print('identical:', conv == comm)
  "

Printed output:
  conv_bytes: 11660 comm_bytes: 11660
  conv_sha256: d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618
  comm_sha256: d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618
  identical: True
  exit code: 0

Finding: The committed snapshot corpus/source-snapshots/round-58/S091.txt is byte-for-byte identical to the raw web page served by the UK AISI server run through the lane conversion instrument. No editorial changes or redactions exist.

---------------------------------------------------------------------
2b. DIFFERENCE ACCOUNTING — Committed vs Independent Text
---------------------------------------------------------------------
Comparison of committed (67 lines, 11660 B) vs independent (71 lines, 11664 B):
Command:
  python3 -c "
  import difflib
  with open('/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt') as f:
      c = f.read().splitlines()
  with open('/fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.independent.txt') as f:
      i = f.read().splitlines()
  diff = list(difflib.unified_diff(c, i, fromfile='committed', tofile='independent', lineterm=''))
  print('\n'.join(diff))
  "

Printed output:
  --- committed
  +++ independent
  @@ -3,8 +3,10 @@
   Please enable javascript for this website.
   A
   A
  -AboutResearchGrantsBlogContactCareers
  -HomeAboutResearchGrantsBlogCareers
  +AboutResearchGrantsBlogContact
  +Careers
  +HomeAboutResearchGrantsBlog
  +Careers
   Blog
   Cyber & Autonomous Systems
   How fast is autonomous AI cyber capability advancing?
  @@ -23,7 +25,8 @@
   To analyse the pace of capability progress, we fit an exponential curve to historical results for the most capable models at any given time. This is an imperfect model, and is not a future prediction, nor a fixed law.
   Cyber Time Horizons Results
   In February 2026, we estimated that frontier models’ 80%-reliability cyber time horizon had doubled every 4.7 months since reasoning models emerged in late 2024, given a 2.5M token limit. This was around half our November 2025 doubling time estimate, which was 8 months for both 50% and 80% reliability. Claude Mythos Preview and GPT-5.5 have since significantly outperformed this trend. At the time of writing, it's unclear whether Mythos Preview and GPT-5.5 represent an isolated break from existing rates of progress or are part of a new, faster trend.
  -Figure 1: 80% reliability cyber time horizon on AISI's narrow cyber task suite (2.5M token budget). Shaded bands show each model’s bootstrap distribution (1000 hierarchical resamples of tasks/runs). Inner band is the central 50%, outer band is the central 95%. The longest task in our cyber suite is 12 hours.Mythos Preview and GPT-5.5 have large upper-bound error bars due to near-100% success rates on our narrow cyber suite’s longest tasks, even with the 2.5M token limit.2 Our tasks are also not long enough to determine how sharply the models’ reliability would deteriorate at higher task lengths. This places some of the latest models at the limit of what our narrow test suite can measure.
  +Figure 1: 80% reliability cyber time horizon on AISI's narrow cyber task suite (2.5M token budget). Shaded bands show each model’s bootstrap distribution (1000 hierarchical resamples of tasks/runs). Inner band is the central 50%, outer band is the central 95%. The longest task in our cyber suite is 12 hours.
  +Mythos Preview and GPT-5.5 have large upper-bound error bars due to near-100% success rates on our narrow cyber suite’s longest tasks, even with the 2.5M token limit.2 Our tasks are also not long enough to determine how sharply the models’ reliability would deteriorate at higher task lengths. This places some of the latest models at the limit of what our narrow test suite can measure.
   Without the 2.5M token cap, success rates are so high that time horizons become impossible to calculate. The cap, alongside our use of a simple agent scaffold, artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds. In return, it ensures time horizons are measurable and can be compared across models. For reference, a 2.5M token limit is relatively low – in our cyber range experiment we use up to 100M tokens and find performance would likely still improve beyond that budget, especially for recent models, which disproportionately benefit from higher token limits.
   Several other factors make doubling times uncertain. Longer time horizon estimates rely on only six tasks with durations of eight hours or more; a bigger sample could include long tasks that AI models find harder or easier than those we currently evaluate, reducing or increasing time horizon estimates.
   Human baselines are also imperfect – different experts could be faster or slower than the ones we timed – and we have only a few human baselines for the six longest tasks. Nevertheless, we believe human baselines are valuable as they provide a more objective measure of task difficulty than alternative metrics.
  @@ -33,7 +36,8 @@
   We have also observed further evidence of cyber autonomy beyond our narrow task suite. AISI’s cyber ranges (shown below) measure AI models’ ability to complete cyberattacks against small, undefended enterprise networks, where initial access has already been gained. Each cyber range requires sustained planning and execution capability; more detail on them can be found in our recent paper.
   In AISI’s latest testing, the newer Mythos Preview checkpoint completed both our cyber ranges, solving the range “The Last Ones” in 6 of 10 attempts and the previously unsolved “Cooling Tower” in 3 of 10 attempts. This was the first time that a model completed the second of our two cyber ranges. GPT-5.5 solved “The Last Ones” on 3 of 10 attempts.
   These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting. Notable capability jumps do not always require new model releases: later iterations of the same model can also meaningfully change our estimates of frontier capabilities.
  -Figure 2: Average number of steps completed on “The Last Ones” (a 32-step simulated corporate network attack) as a function of total token spend. Each line represents a different model, with the shaded region showing the min–max range across all runs at each token budget.Implications
  +Figure 2: Average number of steps completed on “The Last Ones” (a 32-step simulated corporate network attack) as a function of total token spend. Each line represents a different model, with the shaded region showing the min–max range across all runs at each token budget.
  +Implications
   No single benchmark result should be read as a precise measure of AI capability. Time horizon estimates carry genuine uncertainty; the longest tasks in our narrow suite have the fewest human baselines, and it is too early to tell whether the step-change from recent models is representative of a new ongoing (or accelerating) pace. Regardless, the direction of change and rapid growth have been consistent across the models, methodological choices and independent data we examined.
   exit code: 0

Accounting:
- Exactly 4 structural differences account for the 4 additional lines (67 -> 71):
  1. Committed line 6: Navigation link "Careers" split onto next line (+1 line).
  2. Committed line 7: Navigation link "Careers" split onto next line (+1 line).
  3. Committed line 26: The lane instrument's regex (capture-source.py:50) did not include <figcaption> in its block tag set, so </figcaption> immediately preceding <p> glued "12 hours." and "Mythos Preview". HTMLParser correctly treats <figcaption> and <p> as separate blocks (+1 line).
  4. Committed line 36: Similarly, </figcaption> immediately preceding <h3> glued "... token budget." and "Implications". HTMLParser correctly separates them (+1 line).
- Character and word difference: ZERO content words differ. All substantive text, numbers, and dates match identically in sequence.

=====================================================================
3. QUOTE RECHECK TABLE — Pinned Quotes Q1–Q9 vs Independent Text
=====================================================================

Command:
  python3 -c "
  import json
  with open('/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/manifest.json', 'r', encoding='utf-8') as f:
      m = json.load(f)
  quotes = next(s for s in m['sources'] if s['id'] == 'S091')['quotes']
  with open('/fast/scratch/hyaku/kasegi-r58/ScoutSources/S091.independent.txt', 'r', encoding='utf-8') as f:
      lines = [l.strip() for l in f if l.strip()]
  for q in quotes:
      qid, qtext, anchor = q['id'], q['quote'], q['anchor']
      norm = ' '.join(qtext.split())
      matching = [i for i, l in enumerate(lines, 1) if norm in ' '.join(l.split())]
      print(f'{qid} occurrences={len(matching)} indep_line={matching} committed_anchor={anchor} delta={matching[0]-anchor if matching else None}')
  "

Printed output:
  Q1 occurrences=1 indep_line=[1] committed_anchor=1 delta=0
  Q2 occurrences=1 indep_line=[16] committed_anchor=14 delta=2
  Q3 occurrences=1 indep_line=[23] committed_anchor=21 delta=2
  Q4 occurrences=1 indep_line=[25] committed_anchor=23 delta=2
  Q5 occurrences=1 indep_line=[27] committed_anchor=25 delta=2
  Q6 occurrences=1 indep_line=[33] committed_anchor=30 delta=3
  Q7 occurrences=1 indep_line=[37] committed_anchor=34 delta=3
  Q8 occurrences=1 indep_line=[49] committed_anchor=45 delta=4
  Q9 occurrences=1 indep_line=[16] committed_anchor=14 delta=2
  exit code: 0

Per-Quote Verification Table:
| Quote ID | Pinned Quote Text | Committed Anchor | Indep. Line | Occurrences | Delta | Mismatch |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| **Q1** | "How fast is autonomous AI cyber capability advancing? \| AISI Work" | 1 | 1 | 1 | 0 | None (exact match) |
| **Q2** | "already an acceleration from our November 2025 estimate of 8 months" | 14 | 16 | 1 | +2 | None (exact match) |
| **Q3** | "We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time." | 21 | 23 | 1 | +2 | None (exact match) |
| **Q4** | "This is an imperfect model, and is not a future prediction, nor a fixed law." | 23 | 25 | 1 | +2 | None (exact match) |
| **Q5** | "had doubled every 4.7 months since reasoning models emerged in late 2024" | 25 | 27 | 1 | +2 | None (exact match) |
| **Q6** | "Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months." | 30 | 33 | 1 | +3 | None (exact match) |
| **Q7** | "solving the range “The Last Ones” in 6 of 10 attempts and the previously unsolved “Cooling Tower” in 3 of 10 attempts" | 34 | 37 | 1 | +3 | None (exact match) |
| **Q8** | "The AI Security Institute is a research organisation within the Department of Science, Innovation and Technology." | 45 | 49 | 1 | +4 | None (exact match) |
| **Q9** | "It is unclear whether this represents a new, faster trend." | 14 | 16 | 1 | +2 | None (exact match) |

Result: 9 of 9 quotes occur exactly once (occurrences=1) in the independent text. Zero mismatches found. The line deltas (+0, +2, +3, +4) match the exact four structural line additions identified in difference accounting.

=====================================================================
4. CITATION REFERENT RESOLUTION TABLE (S091.txt:NN)
=====================================================================

Evaluation of every line-anchor citation of the form S091.txt:NN in corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md against the committed snapshot corpus/source-snapshots/round-58/S091.txt.

Command:
  python3 -c "
  import re
  md_path = '/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md'
  txt_path = '/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/S091.txt'
  with open(md_path) as f: md_lines = [l.rstrip() for l in f]
  with open(txt_path) as f: s_lines = [l.rstrip() for l in f]
  cites = []
  for idx, line in enumerate(md_lines, 1):
      for full, s, e in re.findall(r'(S091\.txt:(\d+)(?:-(\d+))?)', line):
          cites.append((idx, line, full, int(s), int(e) if e else int(s)))
  for md_l, line, c, s, e in cites:
      text = ' // '.join(s_lines[s-1:e])
      print(f'MD:{md_l} {c} text={text[:60]}...')
  print(f'Total citations checked: {len(cites)}')
  "

Printed output (summary):
  Total citations checked: 23
  exit code: 0

Detailed Citation Verification Table (23 citations across 14 lines):
| # | MD Line | Citation | Referent Named in Markdown Sentence | Committed S091.txt Line Text (Trimmed) | Verdict |
|:---:|:---:|:---|:---|:---|:---:|
| 1 | 13 | S091.txt:45 | Q8 names the publisher | "The AI Security Institute is a research organisation within the Department of Science, Innovation and Technology." | RESOLVES-TO-REFERENT |
| 2 | 21 | S091.txt:14 | "already an acceleration from our November 2025 estimate of 8 months" (Q2) | "In February 2026, we internally estimated that the length of cyber tasks AI models could complete had doubled every 4.7 months since late 2024 – already an acceleration from our November 2025 estimate of 8 months. ..." | RESOLVES-TO-REFERENT |
| 3 | 23 | S091.txt:25 | "had doubled every 4.7 months since reasoning models emerged in late 2024" (Q5) | "In February 2026, we estimated that frontier models’ 80%-reliability cyber time horizon had doubled every 4.7 months since reasoning models emerged in late 2024, given a 2.5M token limit. ..." | RESOLVES-TO-REFERENT |
| 4 | 24 | S091.txt:14 | "It is unclear whether this represents a new, faster trend." (Q9) | "... It is unclear whether this represents a new, faster trend." | RESOLVES-TO-REFERENT |
| 5 | 29 | S091.txt:23 | "an imperfect model, and is not a future prediction, nor a fixed law." (Q4) | "To analyse the pace of capability progress, we fit an exponential curve to historical results for the most capable models at any given time. This is an imperfect model, and is not a future prediction, nor a fixed law." | RESOLVES-TO-REFERENT |
| 6 | 35 | S091.txt:19 | "These tasks cover only some of the capabilities relevant to real-world cyberattacks." | "At AISI, we assign each task in our narrow cyber suite an estimate for how long it would take a cyber expert to complete.1 Tasks in our narrow suite require models to identify and exploit cybersecurity weaknesses in target systems, testing skills such as reverse engineering and web exploitation in self-contained setups. These tasks cover only some of the capabilities relevant to real-world cyberattacks." | RESOLVES-TO-REFERENT |
| 7 | 36 | S091.txt:20 | "For over a third of our tasks" (empirical completion times) | "For over a third of our tasks, we timed how long human experts took to complete them as a baseline. The remainder use expert estimates for completion times, rather than empirical baselines; these could be over- or underestimates. ..." | RESOLVES-TO-REFERENT |
| 8 | 37 | S091.txt:20 | "we focus on a success threshold of 80%" | "... By calculating frontier models’ success rates across all tasks in our narrow cyber suite, we can estimate the length of task they complete with a given likelihood of success – in this post we focus on a success threshold of 80%." | RESOLVES-TO-REFERENT |
| 9 | 39 | S091.txt:21 | "We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time." (Q3) | "We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time. This understates what frontier models can do. We discuss this decision further below." | RESOLVES-TO-REFERENT |
| 10 | 40 | S091.txt:21 | "understates what frontier models can do" | "We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time. This understates what frontier models can do. We discuss this decision further below." | RESOLVES-TO-REFERENT |
| 11 | 41 | S091.txt:27 | "artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds." | "Without the 2.5M token cap, success rates are so high that time horizons become impossible to calculate. The cap, alongside our use of a simple agent scaffold, artificially lowers success rates and understates what models can do with more tokens and stronger scaffolds. ..." | RESOLVES-TO-REFERENT |
| 12 | 44 | S091.txt:33 | "against small, undefended enterprise networks, where initial access has already been gained." | "... AISI’s cyber ranges (shown below) measure AI models’ ability to complete cyberattacks against small, undefended enterprise networks, where initial access has already been gained. Each cyber range requires sustained planning and execution capability; more detail on them can be found in our recent paper." | RESOLVES-TO-REFERENT |
| 13 | 52 | S091.txt:30 | "Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months." (Q6) | "... Though this is a concern, our evidence suggests the trend does not hinge on individual models. Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months." | RESOLVES-TO-REFERENT |
| 14 | 54 | S091.txt:28 | "Longer time horizon estimates rely on only six tasks with durations of eight hours or more;" | "Several other factors make doubling times uncertain. Longer time horizon estimates rely on only six tasks with durations of eight hours or more; a bigger sample could include long tasks that AI models find harder or easier than those we currently evaluate, reducing or increasing time horizon estimates." | RESOLVES-TO-REFERENT |
| 15 | 57 | S091.txt:30 | single-omission sensitivity of the pre-Mythos fit | "... Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months." | RESOLVES-TO-REFERENT |
| 16 | 63 | S091.txt:34 | "solving the range “The Last Ones” in 6 of 10 attempts and the previously unsolved “Cooling Tower” in 3 of 10 attempts" (Q7) | "In AISI’s latest testing, the newer Mythos Preview checkpoint completed both our cyber ranges, solving the range “The Last Ones” in 6 of 10 attempts and the previously unsolved “Cooling Tower” in 3 of 10 attempts. ..." | RESOLVES-TO-REFERENT |
| 17 | 64 | S091.txt:34 | "This was the first time that a model completed the second of our two cyber ranges." | "... This was the first time that a model completed the second of our two cyber ranges. GPT-5.5 solved “The Last Ones” on 3 of 10 attempts." | RESOLVES-TO-REFERENT |
| 18 | 67 | S091.txt:35 | "These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting." | "These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting. Notable capability jumps do not always require new model releases: later iterations of the same model can also meaningfully change our estimates of frontier capabilities." | RESOLVES-TO-REFERENT |
| 19 | 73 | S091.txt:13 | dated blog post (May 13, 2026) | "May 13, 2026" | RESOLVES-TO-REFERENT |
| 20 | 76 | S091.txt:32 | METR's software-engineering doubling time of 4.2 months | "Our latest doubling time estimates are close to those produced by METR, a research non-profit that estimates time horizons for software engineering – a skillset related to cyber, but broader. Their results imply a consistent doubling time of 4.2 months on software tasks since late 2024.3" | RESOLVES-TO-REFERENT |
| 21 | 76 | S091.txt:44 | footnote 3 (METR doubling time) | "3. We estimate METR's 80% – reliability doubling time for frontier models from o1–preview onward. Excluding Mythos Preview, the estimated doubling time is 4.2 months; when included, this accelerates slightly to 4 months. METR’s evaluations use a slightly different selection of models than AISI’s cyber evaluations." | RESOLVES-TO-REFERENT |
| 22 | 78 | S091.txt:2 | Frontier AI Trends Report | "Read the Frontier AI Trends Report" | RESOLVES-TO-REFERENT |
| 23 | 79 | S091.txt:42-44 | report's three footnotes | L42: "1. AISI’s narrow cyber suite is used to estimate time horizons, ..." // L43: "2. With a 2.5M token cap, GPT 5.5 achieves a 100% success rate on five of six tasks ..." // L44: "3. We estimate METR's 80% – reliability doubling time for frontier models from o1–preview onward. ..." | RESOLVES-TO-REFERENT |

Corroborating Header Note (Line 3):
Line 3 of the knowledge file also indexes:
- date L13 -> "May 13, 2026" (matches)
- title L1 -> "How fast is autonomous AI cyber capability advancing? | AISI Work" (matches)
- estimate and acceleration L14 -> 4.7 months and 8 months (matches)
- method L19-L21 -> cyber expert baselines, 80% threshold, 2.5M token cap (matches)
- threshold L20 -> "we focus on a success threshold of 80%" (matches)
- 80% time-horizon doubling L25 -> "doubled every 4.7 months" (matches)
- token-cap statement L21 and L27 -> "understates what frontier models can do" (matches)
- uncertainty L28-L30 -> six tasks, human baselines, single-omission band 4.1 to 5.0 (matches)
- cyber ranges L33-L35 -> The Last Ones (6 of 10), Cooling Tower (3 of 10) (matches)
- publisher statement L45 -> DSIT / AISI statement (matches)

Result: All 23 citations resolve directly to their named referent. Zero mismatches (0/23).

=====================================================================
5. LANE INSTRUMENT EXECUTION — source-recheck.py
=====================================================================

Command:
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-58/manifest.json \
    --source S091

Printed output:
  S091:sha256 OK
  S091:Q1 OK occurrences=1 anchor=1-ok
  S091:Q2 OK occurrences=1 anchor=14-ok
  S091:Q3 OK occurrences=1 anchor=21-ok
  S091:Q4 OK occurrences=1 anchor=23-ok
  S091:Q5 OK occurrences=1 anchor=25-ok
  S091:Q6 OK occurrences=1 anchor=30-ok
  S091:Q7 OK occurrences=1 anchor=34-ok
  S091:Q8 OK occurrences=1 anchor=45-ok
  S091:Q9 OK occurrences=1 anchor=14-ok
  exit code: 0

Verification result:
- SHA256 integrity: OK (binds to d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618).
- All 9 assertions: OK, occurrences=1, anchor=N-ok.
- Exit code: 0.

=====================================================================
6. ANCHOR PORTABILITY PROBE — Lane Instrument on Independent Text
=====================================================================

To test anchor resilience against alternative extraction methods, a scratch manifest was constructed pointing to S091.independent.txt (sha256 fd8d40a2..., 11664 bytes, 71 lines) and evaluated with source-recheck.py.

Command:
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py \
    --manifest /fast/scratch/hyaku/kasegi-r58/ScoutSources/portability/manifest.json \
    --source S091

Printed output:
  S091:sha256 OK
  S091:Q1 OK occurrences=1 anchor=1-ok
  S091:Q2 OK occurrences=1 anchor=14-ok
  S091:Q3 OK occurrences=1 anchor=21-ok
  S091:Q4 OK occurrences=1 anchor=23-ok
  S091:Q5 OK occurrences=1 anchor=25-ok
  S091:Q6 OK occurrences=1 anchor=30-ok
  S091:Q7 OK occurrences=1 anchor=34-ok
  S091:Q8 OK occurrences=1 anchor=45-BROKEN
  S091:Q9 OK occurrences=1 anchor=14-ok
  exit code: 0

Analysis:
- The anchor verification window in source-recheck.py:110 is raw_lines[max(0, anchor - 1):anchor + 3] (a 4-line window).
- For quotes Q1–Q7 and Q9, the delta caused by block separation (+0 to +3 lines) falls within the window, resulting in anchor=N-ok.
- For Q8, the delta is +4 lines (line 49 vs anchor 45), landing one line outside the 4-line window, triggering anchor=45-BROKEN.
- Because all quotes are unique (occurrences=1), the anchor is advisory (source-recheck.py:192-200); the run succeeds with exit code 0. This demonstrates that quote uniqueness is preserved across parser implementations.

=====================================================================
7. SUMMARY & CLEANUP
=====================================================================

Summary of key verification metrics:
- Independent fetch HTTP code: 200
- Independent fetch raw bytes: 33476 (sha256 ce714d89f7305102934b73182d1f78060ea9a12b45e8aad647e96d55db6607cd)
- Committed snapshot: 11660 bytes, 67 lines (sha256 d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618)
- Independent html.parser text: 11664 bytes, 71 lines (sha256 fd8d40a23c414cbc9c80a7be2744827453cafe8f60e926cf08d30b0d6558e046)
- Transitive check (lane converter on independent raw bytes): IDENTICAL (sha256 matches committed snapshot exactly)
- Quote recheck Q1–Q9: 9 of 9 quotes occur exactly once (occurrences=1), 0 mismatches
- Citations check: 23 of 23 line-anchor citations (S091.txt:NN) resolve to referent, 0 mismatches
- Lane instrument source-recheck.py: exit 0, all 9 assertions OK
- Scratch root cleanup: /fast/scratch/hyaku/kasegi-r58/ScoutSources deleted before yield; leftovers: NONE
