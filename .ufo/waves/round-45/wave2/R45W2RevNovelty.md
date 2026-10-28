# R45W2RevNovelty — coverage-credit review of F27 (Linux kernel security-bugs process, row S071)

VERDICT: HOLDS

Seat: R45W2RevNovelty (leaf reviewer, read-only). Tree attacked: export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (`git archive … | tar -x`, scratch only, removed on exit). Pre-round control: export of dc5bb8c6e31efc4a6650819df85e79b72fd64bcd.

## Answer in one paragraph

F27 is a NEW holding, not a restatement: the pre-round corpus holds no Linux-kernel, `security@kernel.org`, `linux-distros`, postponement, or binary-only-reproducer rule. Eight of the twelve kernel-specific questions below have no pre-round answer at all; three are answerable only by generic rule shape (F02, F04, F07). Coverage may be credited honestly as **+1 admitted frontier row (26 → 27) and +1 new source class (an upstream open-source project's own intake and embargo rules)**. It must NOT be reported as a coverage ratio moving: the frontier "27/27" is a count of admitted rows, so it reads 100% before and after. The report should say "+1 row", not "frontier coverage 27/27".

## Findings

### F-1 (holds) — the "held nowhere" before-state is true on the pre-round control
Attacked: frozen claim C2 `before` ("the Linux kernel's own security-bugs reporting process … is held nowhere in corpus/").
Command: `cnt` over `dc5bb8c6` export, `grep -rliF --include=*.md -e <term> corpus | grep -v /lessons/`.
Output: `security@ base=0`, `kernel base=0`, `linux-distros base=0`, `postpon base=0`, `reproducer base=0`, `binary-only base=0`, `treat it as public base=0`, `7 calendar base=0`, `release process base=0`, `kernel.org base=0`.
Counts also match the frozen before-state: knowledge `*.md`=63, SOURCES rows=70, frontier rows=26 (base) and 64 / 72 / 27 on the lane commit.

### F-2 (holds) — twelve kernel-specific questions a pre-round reader could not answer, each with its S071 line
Source: `corpus/source-snapshots/round-45/S071.txt` on 6662a427 (372 lines, RST, line-wrapped).

| # | Question | Answer and S071 line | Pre-round answer? |
|---|---|---|---|
| Q1 | Must a kernel report carry a kernel.org version? | "with no version indication, your report will not be processed" — S071.txt:20-21; distro kernels "meaningless to maintainers" — :23-24 | No (kernel=0). F04 line 10 "identify the code or package version" is a generic Kasegi rule only. |
| Q2 | Is a binary-only reproducer accepted? | "Binary-only executables are not accepted" — S071.txt:39-40 | No (binary-only=0, reproducer=0). |
| Q3 | Does an AI-found bug stay private? | "you must treat it as public" — S071.txt:95-96 | No (treat it as public=0). F04 has no privacy rule. |
| Q4 | May the reproducer be posted publicly? | "do not publicly share a reproducer" — S071.txt:98-99 | No. |
| Q5 | What starts the kernel embargo clock? | "Once a robust fix has been developed, the release process starts" — S071.txt:303-305; occasional embargoes start "from the availability of a fix" — :342-344 | Shape only: F02 lines 7-8 require naming the clock-start event. Kernel trigger is new. |
| Q6 | Maximum fix-publication postponement? | "for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days" — S071.txt:309-311 | Number new (7 calendar=0 base). Shape duplicated by the base S016 maintainer-requested "further 7-day extension" (see F-4). |
| Q7 | Which deferral reason is valid? | "The only valid reason for deferring the publication of a fix is to accommodate the logistics of QA…" — S071.txt:312-314 | No (postpon=0). |
| Q8 | When may linux-distros be contacted? | "DO NOT contact the 'linux-distros' mailing list UNTIL a fix is accepted by the affected code's maintainers" — S071.txt:348-351 | No (linux-distros=0). |
| Q9 | Who must be Cc'd? | "If there are two or fewer recipients in your message, you must also always Cc: the Linux kernel security team" — S071.txt:270-273 | No (security@=0, kernel=0). |
| Q10 | Is a CVE required? | "The security team does not assign CVEs, nor do we require them" — S071.txt:362-363 | Shape only: F07 covers CNA rules generically; kernel stance is new. |
| Q11 | Is an unreproducible issue a security bug? | "if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug" — S071.txt:41-43 | Shape only: F04 line 7 keeps AI findings "candidate" until reproduction. |
| Q12 | Where is the kernel security list? | `<security@kernel.org>` — S071.txt:281 | No pre-round answer, and still NO answer post-round (see F-5). |

Net: 8 new answers (Q1-Q4, Q6-Q9), 3 shape-only (Q5, Q10, Q11), 1 unanswered even after the round (Q12).

### F-3 (holds, with a caveat) — the duplicated part is the rule shape, and F27 says so for F02, F04, F15
Read: `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:35-37` (the "Overlap and novelty" section) names F02 (`coordinated-disclosure-timelines.md:7-17`), F04 (`ai-assisted-finding-validation.md:7-8,15`) and F15 (`vendor-third-party-finding-coordination.md:91-96`). Read against the frontier entries I opened:
- F02 (lines 7-17) requires naming the policy, clock trigger, interval, and documented extension, and forbids transplanting another coordinator's interval. F27's 7/14-day ceiling is applied under that rule; the rule itself is not new.
- F04 (lines 7-8, 15) requires a reproducible observation and a reviewer distinct from the producer. F27 Q11 reuses the reproduction gate; the reviewer requirement is not in S071 (F27 says so at :36).
- F15 (lines 84-96, 115-117) records which party coordinates. S071.txt:333-334 ("other groups focus on fixing issues in distros and coordinating disclosure") is a new fact about who coordinates a kernel report; the recording rule is F15's.
Caveat: F27 names none of these as a duplicate beyond the rule; the ratio of new to restated is therefore a judgement, not a count.

### F-4 (attack, finding against the entry) — the nearest pre-round overlap is not acknowledged
Attacked: F27 "Overlap and novelty" section (`linux-kernel-security-bugs-reporting-process.md:33-37`) and "Rejected over-generalizations" (:56-60).
Pre-round file: `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` (S016, round-40 entry, "ground: F02", no frontier row). Quotes:
- `"If the maintainer is actively working on a fix and requests more time, we may grant a further 7-day extension." — S016.txt:L12`
- `"making progress toward a fix as the 90-day deadline approaches, we may grant a 14-day extension on request" — S016.txt:L11`
This is Anthropic's discoverer-side policy, not the kernel's, so it does not answer Q6. But it already holds a 7/14-day maintainer-facing extension shape, and F27's "what is new" item 3 ("The 7/14-day ceiling as an upstream-maintainer rule") does not mention it. A reader will conflate the two 7-day figures unless F27 says they differ. Requested fix: add one overlap sentence naming S016 and its 7-day extension as a different policy.

### F-5 (gap) — F27 does not record the channel address
Command: `grep -c "@" corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` → `0`. Capture: `grep -n "security@kernel.org" S071.txt` → `281:<security@kernel.org>.  This is a private list of security officers`.
The frontier row (`corpus/README.md:651`) and the round-45 block (`:637-640`) both say "the private security list" / "private report channel" without naming it. The entry's own "Limits" say it instructs no contact, so omitting the address may be deliberate. Either way the claimed "private report channel" is an unnamed object, and a reader asking "where does the report go" gets no answer from F27. The report should not present F27 as answering channel-discovery; that question stays open.

### F-6 (holds) — the coverage ratio is tautological; +1 row is the only honest credit
Counter: `corpus/instruments/r44-frontier-count.py` counts rows whose status cell `== "admitted"` (`r44-frontier-count.py`, `_is_admitted`: `return cells[2] == "admitted"`).
Command (on the lane export): `cd tree && python3 corpus/instruments/r44-frontier-count.py --root "$PWD" --expect 27` → `frontier rows=27 admitted=27`, exit 0.
Command (on the base export): `python3 corpus/instruments/r44-frontier-count.py --root "$PWD"` → `frontier rows=26 admitted=26`.
Status column on the lane export: all 27 rows read `admitted` (`grep -E '^\| F[0-9]+ \|' corpus/README.md | awk -F'|' '{…$4…}' | sort | uniq -c` → `27 admitted`).
So rows = admitted by construction; "27/27" is 100% before (26/26) and after. The counter verifies row count, not coverage of the public-practice space. A ratio "moved" claim is therefore unsupported; "+1 admitted row, +1 new source class" is supported.

### F-7 (attack, finding against the counts) — S072 inflates the SOURCES figure
`corpus/SOURCES.md` S072 row: used-by column `—`. S072 is the C1 R1 secondary routing summary, cited by no entry. The SOURCES count goes 70 → 72 with one row used by F27 (S071) and one used by nothing. Coverage credit must count S071 only; the frozen C2 `after` line "SOURCES rows 70 → 72" should not be read as coverage.

### F-8 (limitation of the quote check, not a failure) — verbatim grep of RST quotes fails on line wraps
`grep -c -F "with no version indication, your report will not be processed" S071.txt` → `0`; the phrase is wrapped across lines 20-21. After collapsing whitespace (`tr -s ' \n' ' '`) the same quote → `1`, and the others I checked (`Binary-only executables are not accepted`, `By definition if an issue cannot be reproduced, it is not exploitable`, `for up to 7 calendar days from the start of the release process`, `The security team does not assign CVEs`) each → `1`. `until a fix is accepted by the affected code's maintainers` → `0` only because the capture writes `UNTIL` in capitals; case-insensitive whitespace-collapsed → `1`. The entry's located line numbers are right; the C1/C2 counters must normalise whitespace or they will mis-grade. Not a coverage defect.

### F-9 (note) — base commit disagreement
The assignment names base dc5bb8c6; `git -C … rev-parse 6662a427^` prints `5242db6fbf2b3575da6600974f0b5b4292caa62f`. The lane commit's first parent is not the stated round base. I used dc5bb8c6 as the do-nothing control as instructed; the grep results are identical for both trees' pre-round content, but the parent mismatch should be explained by the L1.

## Recommended coverage wording for the report

- "Frontier rows 26 → 27 (+1). Source class moved: first corpus holding of an upstream open-source project's own intake and embargo rules (Linux kernel, S071)."
- "Eight kernel-specific answers are new (version requirement, binary-only refusal, AI-found-is-public, reproducer withholding, postponement ceiling 7/14 days, QA-only deferral reason, linux-distros timing, Cc rule). Three are rule-shape restatements of F02, F04, F07. The channel address is not recorded."
- Do NOT write "frontier coverage 27/27" or "coverage 100%" as progress; the count is admitted rows by construction.
- Do NOT count S072 toward coverage.

## Limitations

- Attacked the export of 6662a427 and the pre-round export of dc5bb8c6 only; the lane working tree was not touched.
- Relied on the pinned capture `source-snapshots/round-45/S071.txt`; the live docs.kernel.org page was not re-fetched (out of scope and forbidden for live-target work).
- I did not run `r45-c2-gate.py` (the C2 counter is another seat's); my coverage analysis uses the frontier counter and grep controls only.
- "New vs restated" is a judgement over a 12-question table I wrote; the question set is mine, not frozen.
- Control discrimination is grep-based on terms; a synonym-only pre-round answer (e.g. "deferral" phrased without "postpon") could be missed. I checked `defer`: `grep -rliF --include=*.md -e defer base/corpus | grep -v /lessons/ | wc -l` → `9` non-lesson base files; `… | xargs grep -liF -e kernel | wc -l` → `0`.
- Scratch export and fixtures removed on exit.
