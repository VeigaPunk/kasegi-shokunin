# Big Sleep's SQLite variant-analysis case — a first-party, pre-release finding report

source: S094 — https://projectzero.google/2024/10/from-naptime-to-big-sleep.html — capture corpus/source-snapshots/round-61/S094.txt, sha256 663ac16df13b7c93c2d9848265854625c46e8f59d0c39a5bbb4d68bf6573e804; opened 2026-11-04 using capture-source.py --kind html (HTTP 200; 56257 fetched bytes; 15904 snapshot bytes; 125 lines; fetched 2026-11-04T14:13:15Z).
verified-at: 2026-11-04
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-61/manifest.json --source S094
ground: F42

## Attribution and scope

The Project Zero page is dated 2024-Nov-01 and credited to the Big Sleep team (S094.txt:13-15). It says Naptime evolved into Big Sleep, a collaboration between Project Zero and DeepMind (S094.txt:17). This entry records the publisher's account, not an independently reproduced finding, a current SQLite vulnerability, a program policy, authorization or an intake route.

## Claim 1 — a pre-release finding, not proof that released users were exposed

The team describes an exploitable stack buffer underflow in SQLite, reported in early October and fixed by the developers that same day (S094.txt:18). Its crucial qualification is that the issue was found before an official release, so SQLite users were not impacted (S094.txt:18, Q1).

Falsifiable rule: attribution to this account must preserve its pre-release qualification. Rejected: calling the finding an exploited bug in a released SQLite version; the cited paragraph says neither.

## Claim 2 — a recent-commit starting point, not open-ended discovery from no hints

The methodology supplies recent SQLite commits after manually removing trivial and documentation-only changes, then gives the agent a commit message and diff and asks it to review the current repository at HEAD for related unfixed issues (S094.txt:25, Q2-Q3). The team calls variant analysis a better fit for current LLMs than the general open-ended problem (S094.txt:24). These are the team's reported setup choices, not a lane-authored research method or a measured recommendation for another target.

Falsifiable rule: a retelling that removes the seed commits and presents the exercise as unseeded open-ended discovery contradicts S094.txt:24-25. Rejected: inferring an agent-wide success rate from this successful case; the page provides no denominator here.

## Claim 3 — the negative fuzzing result is harness-bound

The post attributes the missed issue partly to harness configuration: OSS-Fuzz lacked generate_series, while fuzzingshell.c contained an older unaffected seriesBestIndex (S094.txt:112, Q4). The team's own CLI-target AFL experiment, with generate_series and rowid present in the corpus, left the issue undiscovered after 150 CPU-hours (S094.txt:113, Q5). This is the post's own experiment, not a lane re-run and not proof that fuzzing cannot find the bug.

Falsifiable rule: preserve the named harness differences and the CPU-hour unit. Rejected: treating 150 CPU-hours as wall-clock hours or a universal fuzzer-versus-agent result. The team explicitly calls its results highly experimental and says a target-specific fuzzer would likely be at least as effective at finding vulnerabilities (S094.txt:118, Q6-Q7).

## Kasegi use and limits

When evaluating an AI-generated finding narrative, retain the seed information, reproduction environment, release exposure and the author's comparative caveat before treating it as evidence. This case supplies those qualifications; it grants no permission to test a live target.

F04 retains Naptime's principles and validation guidance; F40 retains the public findings tracker and F41 the later V8 production comparison. F42 adds this dated SQLite finding account and its pre-release/harness qualifications, not another count of those held surfaces. Research methodology belongs to chousa and LLM benchmark evaluation to kengaku; no new method or benchmark conclusion is asserted here. The lane executes no SQLite exploit or live-target test.
