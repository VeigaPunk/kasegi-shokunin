# UK AISI autonomous cyber-capability progress rate — the AI Security Institute's own measurement record of how fast autonomous AI cyber task capability is advancing: the 80%-reliability time-horizon doubling estimate and its acceleration, the bounded method that produces it, the stated uncertainty, and the cyber-range results

source: S091 — https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing — capture corpus/source-snapshots/round-58/S091.txt (11660 snapshot bytes over 33476 fetched; sha256 d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618; recorded fetch 2026-11-03T20:35:59Z, HTTP 200; a same-sha probe open at 20:35:32Z and the recorded-plus-verification re-open at 20:35:59Z are byte-identical; date L13, title L1, estimate and acceleration L14, method L19-L21, threshold L20, 80% time-horizon doubling L25, token-cap statement L21 and L27, uncertainty L28-L30, cyber ranges L33-L35, publisher statement L45); manifest corpus/source-snapshots/round-58/manifest.json (9 assertions Q1-Q9, each occurrences=1 at its anchor)
verified-at: 2026-11-03 (opened this round; the page is a dated blog post — byte stability is asserted within this round's opens only, and the 90d row recheck re-fetches)
ground: F39
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote is absent from the capture, so a missing or corrupted capture fails closed; a pinned quote whose anchor no longer holds is printed as "anchor=NN-BROKEN" and still exits 0; a pinned-capture comparison, not a fresh network check

## Attribution

The AI Security Institute's own blog report on its own measurement programme: what AISI estimates,
how it bounds the estimate, what it says the estimate does not show, and the results of its cyber
ranges. Every model result, doubling figure and range completion below is AISI's first-party
statement about its own internal, self-contained testing (Q8 names the publisher, S091.txt:45). This entry records
those statements; it does not verify any model behaviour and does not verify the underlying runs,
which the report does not publish. It is documentation-only: it instructs no probing, scanning,
login or submission against any target, and carries no credential material.

## Claim 1 — AISI estimated the 80%-reliability cyber time horizon, given a 2.5M token limit, doubled every 4.7 months from late 2024, an acceleration from its own November 2025 estimate of 8 months, and says it is unclear whether the latest models start a new, faster trend

The February 2026 estimate is "already an acceleration from our November 2025 estimate of 8 months"
(S091.txt:14 Q2), and the report states the doubling directly: frontier models' 80%-reliability
cyber time horizon "had doubled every 4.7 months since reasoning models emerged in late 2024"
(S091.txt:25 Q5). The February 2026 summary paragraph says the latest models "substantially exceeded both doubling
rate trends" and that "It is unclear whether this represents a new, faster trend." (S091.txt:14 Q9).
Falsifiable rule: a reading that gives AISI's February 2026 doubling estimate as longer than its
November 2025 estimate, or that presents the post-Mythos rate as an established new trend, contradicts
the report as served on the recorded fetch date. Rejected over-generalizations: the 4.7-month figure
is AISI's suite-bound estimate under its own curve fit, which the report calls "This is an imperfect model, and is not a future prediction, nor a fixed law." (S091.txt:23 Q4); so it is not a universal rate of
AI progress and not a forecast of any capability threshold.

## Claim 2 — the measurement is bounded by its method: a narrow cyber suite, expert-time baselines, an 80% success threshold and a 2.5M token cap that AISI says understates what the models can do

The suite is narrow by AISI's own statement: "These tasks cover only some of the capabilities
relevant to real-world cyberattacks." (S091.txt:19). Completion times are empirical "For over a third
of our tasks" and expert estimates for the rest, which the report says "could be over- or underestimates" (S091.txt:20); the headline threshold is "we focus on a
success threshold of 80%" (S091.txt:20). The token cap is a comparability choice:
"We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over
time." (S091.txt:21 Q3), and the report states that it "understates what frontier models can do"
(S091.txt:21) and that the cap, alongside the simple agent scaffold the report uses, "artificially lowers success rates and understates what models can
do with more tokens and stronger scaffolds." (S091.txt:27). Falsifiable rule: a reading that treats
the suite's time horizons as an upper bound on model capability, or as a measure of defended real-world
systems, contradicts these statements. The cyber ranges are described as measuring attacks "against
small, undefended enterprise networks, where initial access has already been gained." (S091.txt:33).
Rejected over-generalizations: the time horizons are not a capability leaderboard across cyber work
as a whole, and the human baselines are a timed sample for over a third of tasks, not a certified
difficulty standard.

## Claim 3 — AISI states its uncertainty: a single-model omission moves the pre-Mythos doubling estimate only within 4.1 to 5.0 months, and the longest tasks rest on six tasks

The report bounds one sensitivity: "Any single omission only shifts the pre-Mythos doubling time
estimate to a minimum of 4.1 months, and a maximum of 5.0 months." (S091.txt:30 Q6). It names the
longest-task limit: "Longer time horizon estimates rely on only six tasks with durations of eight hours or more" (S091.txt:28), and adds that a bigger sample could include long tasks AI finds harder or easier, reducing or increasing the estimates. Falsifiable rule: a reading that presents the 4.7-month estimate
without the stated uncertainty, or that reads the 4.1-to-5.0 band as a confidence interval on the
post-Mythos rate, contradicts the report. Rejected over-generalization: the 4.1-to-5.0 band is the
single-omission sensitivity of the pre-Mythos fit (S091.txt:30), not a statistical interval on any
later estimate.

## Claim 4 — AISI reports a newer Mythos Preview checkpoint solved both of its cyber ranges, "The Last Ones" in 6 of 10 attempts and the previously unsolved "Cooling Tower" in 3 of 10, while GPT-5.5 solved "The Last Ones" on 3 of 10

The report states: "solving the range “The Last Ones” in 6 of 10 attempts and the previously unsolved
“Cooling Tower” in 3 of 10 attempts" (S091.txt:34 Q7), and "This was the first time that a model
completed the second of our two cyber ranges." (S091.txt:34). Falsifiable rule: a reading that gives
the same two-range completion to an earlier checkpoint in AISI's reporting, or that omits the report's
caveat, contradicts the report. The caveat is stated: "These results utilise a newer Mythos Preview
checkpoint than that included in previous AISI reporting." (S091.txt:35). Rejected over-generalization:
these are one checkpoint's attempt counts on two bespoke ranges, not a reproducible public benchmark, and
they are not comparable to earlier published checkpoint results without that caveat.

## Limits

- The page is a dated blog post (May 13, 2026, S091.txt:13). Byte stability is asserted within this
  round's opens only; the 90d recheck re-fetches, and a changed estimate, a newer post or an edited page
  supersedes by a new row (R8).
- METR's software-engineering doubling time of 4.2 months, which the report's footnote 3 gives excluding Mythos Preview (4 months with it) (S091.txt:32, footnote 3 at S091.txt:44), is a
  different programme's figure, named by the report and not absorbed here; the linked Frontier AI Trends
  Report (S091.txt:2) is named and not opened: a lead, not a row.
- The report's three footnotes (S091.txt:42-44) carry the suite's scope caveats and are read as part of
  the statements above, not as separate sources.
- Adjacency: LLM evaluation and benchmark method is kengaku's province (PROVINCE.md, Adjacent). This
  entry records one government institute's cyber-task measurement statements because they bear on
  vulnerability-finding throughput planning; the method itself is not re-scored here.
