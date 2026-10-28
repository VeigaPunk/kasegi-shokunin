VERDICT: INFO

The three named knowledge entries do not already state the kernel's 7-calendar-day publication ceiling or its exceptional 14-calendar-day extension. They do state other embargo or publication-delay rules. None of those rules is set by the kernel security-bugs process, and none of them runs from the start of the release process.

## Kernel ceiling being compared

Attacked text: `corpus/source-snapshots/round-45/S071.txt` lines 305-315 and 340-346 (the ceiling the seat names is 310-311).

Command:

```
python3 << 'PY'
from pathlib import Path
s071 = Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt")
lines = s071.read_text().splitlines()
print(f"S071 lines={len(lines)}")
for i in list(range(304, 315)) + list(range(339, 346)):
    print(f"{i+1}: {lines[i]}")
PY
```

Output printed:

```
S071 lines=372
305: Once a robust fix has been developed, the release process starts.  Fixes
306: for publicly known bugs are released immediately.
307: 
308: Although our preference is to release fixes for publicly undisclosed bugs
309: as soon as they become available, this may be postponed at the request of
310: the reporter or an affected party for up to 7 calendar days from the start
311: of the release process, with an exceptional extension to 14 calendar days
312: if it is agreed that the criticality of the bug requires more time.  The
313: only valid reason for deferring the publication of a fix is to accommodate
314: the logistics of QA and large scale rollouts which require release
315: coordination.
340: Please note that the respective policies and rules are different since
341: the 3 lists pursue different goals.  Coordinating between the kernel
342: security team and other teams is difficult since for the kernel security
343: team occasional embargoes (as subject to a maximum allowed number of
344: days) start from the availability of a fix, while for "linux-distros"
345: they start from the initial post to the list regardless of the
346: availability of a fix.
```

Who sets it:

- The maximum is this document's own cap: "up to 7 calendar days" and "an exceptional extension to 14 calendar days" (`S071.txt:310-312`). The page opens as the kernel developers' process (`S071.txt:6-8`: "Linux kernel developers take security very seriously. As such, we'd like to know when a security bug is found so that it can be fixed and disclosed as quickly as possible.").
- The postponement is "at the request of the reporter or an affected party" (`S071.txt:309-310`). Those parties request the delay. The sentence does not let them choose the length.
- The step from 7 to 14 happens only "if it is agreed that the criticality of the bug requires more time" (`S071.txt:312`). The sentence does not name who must agree.
- The same paragraph states the only valid reason: "to accommodate the logistics of QA and large scale rollouts which require release coordination" (`S071.txt:313-315`).
- The coordination section names whose embargoes these are: "for the kernel security team occasional embargoes (as subject to a maximum allowed number of days)" (`S071.txt:342-344`).

From what event it runs:

- The ceiling sentence itself says "from the start of the release process" (`S071.txt:310-311`).
- "Once a robust fix has been developed, the release process starts" (`S071.txt:305`). Fixes for publicly known bugs "are released immediately" (`S071.txt:305-306`). The stated preference for publicly undisclosed bugs is to release "as soon as they become available" (`S071.txt:308-309`); the 7/14 postponement is the exception to that preference.
- Later, the same file says those kernel-security-team embargoes "start from the availability of a fix" (`S071.txt:343-344`). It contrasts linux-distros, whose embargoes "start from the initial post to the list regardless of the availability of a fix" (`S071.txt:344-346`). This file does not give linux-distros a day count.

Two formulations are in the file. The ceiling lines say "start of the release process". The coordination lines say "availability of a fix". Line 305 ties the release process to a robust fix having been developed. This scan does not collapse those phrases into a third event.

A different embargo object sits beside the ceiling and is not the 7/14 clock. Command excerpt (same interpreter, lines 316-327):

```
316: 
317: While embargoed information may be shared with trusted individuals in
318: order to develop a fix, such information will not be published alongside
319: the fix or on any other disclosure channel without the permission of the
320: reporter.  This includes but is not limited to the original bug report
321: and followup discussions (if any), exploits, CVE information or the
322: identity of the reporter.
323: 
324: In other words our only interest is in getting bugs fixed.  All other
325: information submitted to the security list and any followup discussions
326: of the report are treated confidentially even after the embargo has been
327: lifted, in perpetuity.
```

That is confidentiality of the report and related material, including after the embargo lifts. It is not the publication-delay ceiling.

## Do-nothing control

Hypothesis discriminated against: leave the three knowledge files untouched and treat them as already containing this ceiling.

Command:

```
python3 << 'PY'
from pathlib import Path
files = [
    Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md"),
    Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md"),
    Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/multiparty-vulnerability-coordination.md"),
]
needles = ["7 calendar", "14 calendar", "calendar day", "release process", "availability of a fix", "security-bugs", "kernel"]
for p in files:
    low = p.read_text().lower()
    print(f"FILE {p.name}")
    for n in needles:
        print(f"  count {n!r} = {low.count(n.lower())}")
PY
```

Output printed: for every file, `count '7 calendar' = 0`, `count '14 calendar' = 0`, `count 'calendar day' = 0`, `count 'release process' = 0`, `count 'availability of a fix' = 0`, `count 'security-bugs' = 0`, `count 'kernel' = 0`.

A do-nothing reading of these three files cannot recover "7 calendar days from the start of the release process" or the exceptional 14. The recorded freeze line `.ufo/waves/round-45/controls/freeze-controls.txt:2` says `control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED`. That line was read, not re-executed. This seat did not run `r45-c2-gate.py`.

A corpus-wide token check of `corpus/knowledge/*.md` for `7 calendar|14 calendar|start of the release process|availability of a fix` printed one hit, and it is not the kernel ceiling: `corpus/knowledge/japanese-domestic-disclosure-workflow.md:43` says the F02 sources' recorded triggers "are the report or the availability of a fix (F02, S004 and S005)". That gloss points at CERT/CC and Project Zero. It does not state 7 or 14 calendar days, and it does not name the kernel release process.

## Statements that already cover an embargo or a publication delay

Inventory command (the three files only):

```
python3 << 'PY'
from pathlib import Path
import re
files = [
    Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/coordinated-disclosure-timelines.md"),
    Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md"),
    Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/multiparty-vulnerability-coordination.md"),
]
pat = re.compile(r"embargo|deadline|grace|disclos|publicat|postpone|defer|timeline|time frame|extension|calendar|90-day|45 day|30 day|14-day|14 day", re.I)
for p in files:
    print(f"===== {p.name} =====")
    n = 0
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if pat.search(line):
            n += 1
            print(f"{i}: {line}")
    print(f"-- matches {n}")
PY
```

That command printed 22 matching lines in `coordinated-disclosure-timelines.md`, 15 in `vendor-third-party-finding-coordination.md`, and 11 in `multiparty-vulnerability-coordination.md`. The lines below are the ones that state a delay, an embargo, or the absence of one. Lines that only use "disclosure" as a package name, a CVD label, or the word "disclosed" in "capture gap (disclosed)" are not delay statements; they are in that command's output and are omitted from this list.

### Positive clocks — `corpus/knowledge/coordinated-disclosure-timelines.md`

1. `coordinated-disclosure-timelines.md:20` — S003: "A time frame may be a fixed period, a minimum or maximum, or a negotiated default starting point." Who: CISA supplier guidance, not a named coordinator's clock. Event: none. A "negotiated default starting point" is a shape, not an event. Interval: none. Difference: the kernel ceiling is one stated maximum (7, exceptional 14) running from a named event (start of the release process, `S071.txt:310-311`), requested by the reporter or an affected party (`S071.txt:309-310`), with one valid reason (`S071.txt:313-315`). S003's sentence is a menu of shapes.

2. `coordinated-disclosure-timelines.md:21` — the only positive use of the word "embargo" in the three files. S003: "Suppliers and researchers should work collaboratively to adjust embargo periods", and the entry adds "this is supplier-facing best-practice guidance, not a universal clock." Who: suppliers and researchers, collaboratively. Event: none named. Interval: none. Difference: the kernel text is a ceiling, not an open collaborative adjustment, and the entry itself says this sentence is not a universal clock. A separate count command printed `coordinated-disclosure-timelines.md embargo_lines=1`, this line only.

3. `coordinated-disclosure-timelines.md:22` — S004 / CERT/CC: "Vulnerabilities reported to the CERT/CC will be disclosed to the public 45 days after the initial report". Who: CERT/CC. Event: the initial report. Interval: 45 days until public disclosure. Difference: the kernel clock does not start at the initial report. It starts at the start of the release process (`S071.txt:310-311`), which line 305 places after a robust fix has been developed. The interval is 7 calendar days, not 45.

4. `coordinated-disclosure-timelines.md:23` — S004: "may result in earlier or later disclosure." Who: CERT/CC, for extenuating circumstances. Event: no new trigger. Interval: unbounded relative to the 45 days. Difference: the kernel extension is a bounded step from 7 to 14 calendar days, and only if criticality is agreed to need more time (`S071.txt:311-312`), for QA and large-scale rollout logistics (`S071.txt:313-315`). It is not an open earlier-or-later adjustment.

5. `coordinated-disclosure-timelines.md:24` — S005 / Project Zero: "this bug report will become public 30 days after the fix was made available." The entry says this is Project Zero's policy when a fix is available before its deadline. Who: Project Zero. Event: the fix was made available. Interval: 30 days, inside a 90-day deadline. Difference: this is the closest trigger (a fix already exists), and it is still a different rule. The setter is Project Zero, not the kernel security-bugs process. The interval is 30 days, not 7 calendar days. What becomes public is the bug report. The kernel sentence postpones publication of a fix that the process would otherwise release as soon as it is available (`S071.txt:308-311`).

6. `coordinated-disclosure-timelines.md:25` — S005: "we grant a 14-day grace extension only when there's a commitment by the developer to ship a fix within the 14-day grace period." Who: Project Zero grants it. Event: a patch is not broadly available after 90 days, plus a commitment to ship inside the grace. Interval: 14 days, written "14-day", not "14 calendar days". Difference: same numeral, opposite phase. Project Zero's 14 days is extra time before a fix ships. The kernel's 14 calendar days (`S071.txt:311-312`) is an exceptional extension after the release process has started, and line 305 says that process starts once a robust fix has been developed. The kernel condition is agreed criticality, and the only valid reason is QA and rollout logistics (`S071.txt:312-315`), not a commitment to ship a fix that does not exist yet. `coordinated-disclosure-timelines.md:17` says "Do not transplant CERT/CC or Project Zero intervals into another policy record." Copying this 14-day grace onto the kernel ceiling is the transplant that line forbids.

7. `coordinated-disclosure-timelines.md:33` — rejected statement: "All vulnerability reports use a 90-day disclosure deadline." This rejects a universal publication delay. It does not state the kernel ceiling. `coordinated-disclosure-timelines.md:37` adds that S003 "does not prescribe a single deadline for every researcher or coordinator." `coordinated-disclosure-timelines.md:38`: "S004 describes CERT/CC's own policy, and S005 describes Project Zero's own policy; neither establishes a general legal requirement."

### Measured absence — `corpus/knowledge/vendor-third-party-finding-coordination.md`

These lines cover embargo language by recording that the MSVR page has none. They are not a positive delay.

- `vendor-third-party-finding-coordination.md:116-120` — "It does not state the coordination agreements, a timeline, a reporting address or a per-vendor process", with ``grep -ciE '90[ -]day|deadline|embargo|timeline'`` → `0`.
- `vendor-third-party-finding-coordination.md:133` — "FC-3 — no clock and no channel on the page." The same grep on `corpus/source-snapshots/round-31/S048.txt` → `0`. "Any 'MSVR's N-day embargo' ... line cannot be supported from S048."
- `vendor-third-party-finding-coordination.md:150-153` — the page "states no obligation, no deadline and no address."
- `vendor-third-party-finding-coordination.md:166` — the capture "carries no per-vendor process, contact or timeline."

A count command printed `vendor-third-party-finding-coordination.md embargo_lines=2`, lines 118 and 133 only, both inside the absence claims. Difference: S071 states a numeric ceiling (`S071.txt:310-311`). This entry records that S048 states no embargo and no timeline. An absence on one vendor's programme page is not the kernel rule, and it does not say who may request a kernel postponement or which event starts it.

### Negotiated timeline, no numeric delay — `corpus/knowledge/multiparty-vulnerability-coordination.md`

A count command printed `multiparty-vulnerability-coordination.md embargo_lines=0`.

- `multiparty-vulnerability-coordination.md:11-13` — "Record contact ownership, negotiated expectations, and a timeline for each party; one vendor's patch date is not evidence that every downstream product has received a fix." Who: the package reviewer records a per-party timeline. Event: none. Interval: none. Difference: a worksheet field is not a 7-calendar-day cap, and one vendor's patch date is a different claim from the kernel's start-of-release-process clock.
- `multiparty-vulnerability-coordination.md:15-16` — FIRST's practices are "not a universal legal deadline." Difference: this denies a universal deadline. It does not state the kernel's particular maximum.
- `multiparty-vulnerability-coordination.md:27` — S018: "All parties should clearly and securely communicate and negotiate expectations and timelines." Who: all parties, by negotiation. Event: the row is "Prior to disclosure"; no start event such as release-process start. Interval: none. Difference: the kernel ceiling is not an open negotiation. It is a stated maximum from a named event, with one valid deferral reason (`S071.txt:310-315`).
- `multiparty-vulnerability-coordination.md:29` — "Vendors should be aware that publication of fixes can disclose the presence of the same vulnerability in other vendors' components." This is an effect of publication, not a delay. No setter, no start event, no interval. It does not state the kernel's QA/rollout deferral.
- `multiparty-vulnerability-coordination.md:43-46` — rejects "The upstream vendor shipped, so every downstream user is patched and public disclosure is automatically safe." The entry says FIRST "calls for negotiated communication rather than a universal automatic disclosure trigger." Difference: that rejection is about whether an upstream shipment makes disclosure safe. The kernel rule is a short, capped postponement of publishing a fix, measured from the start of the release process (`S071.txt:310-311`), not a ban on treating shipment as a disclosure trigger.

### Recording rules that mention a clock and state no duration

These are in `coordinated-disclosure-timelines.md` and do not already contain the kernel ceiling. They say how to record someone else's clock: name the policy, the event that starts it, the interval, the patch/publication relationship, and any extension (`:7`); do not treat one interval as the universal researcher deadline (`:8`); do not conflate patch and publication (`:13`); an extension must name its condition (`:14`); distinguish a fixed deadline from a negotiated starting point (`:15`); do not transplant CERT/CC or Project Zero intervals (`:17`); bind the timeline to that policy (`:29`); keep that policy's own exceptions and patch trigger (`:30`). `multiparty-vulnerability-coordination.md:37` requires a "timeline basis" on a worksheet and states no interval.

Applied to S071, those rules are why the kernel ceiling still needs its own record: the setter is the kernel security-bugs process, the request belongs to the reporter or an affected party, the event is the start of the release process, the interval is 7 calendar days, and the extension is 14 calendar days if criticality is agreed to need more time. None of that tuple is filled in by the three files.

## Limitations

- The existing-statement side is the three knowledge files as read. This seat did not re-open the S003, S004, S005, S018, or S048 snapshots to re-prove those entries' quotes.
- `r45-c2-gate.py` was not re-run. The freeze-controls do-nothing line was read from `controls/freeze-controls.txt:2`.
- Full reads were the three named files plus `S071.txt` (the disclosure and coordination sections, and lines 6-8). The knowledge-corpus check was a token search, plus a read of `japanese-domestic-disclosure-workflow.md:35-43` for the one "availability of a fix" hit. Other files may discuss publication in words that token search did not select. They do not contain the strings "7 calendar", "14 calendar", or "start of the release process".
- `S071.txt:312` ("if it is agreed") does not name the agreeing parties. This scan does not invent them.
- `S071.txt:344-346` says linux-distros embargoes start at the initial post. It does not state a linux-distros day count, and neither do the three knowledge files.
- No scratch directory was created. No git or jj command was run. No file other than this report was written.
