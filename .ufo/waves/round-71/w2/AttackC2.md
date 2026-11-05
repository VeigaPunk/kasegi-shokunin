# AttackC2 — source-outrun audit of F49/S106 (R108), round 71 attempt 2

Seat: AttackC2 (critic, leaf, no dispatch). Lane `kasegi-shokunin`, tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`.
Every audited byte was read with `git -C … show <rev>:<path>` at that revision. Attempt-1's `CriticC2` died, so this
audit is unrun from attempt 1 and the attempt-1 wave carries no outrun verdict for F49.

Audited artifacts (committed bytes only):
- entry `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`
- registry row `corpus/SOURCES.md:118`
- frontier row `corpus/README.md:1114` (+ its section prose `README.md:1099-1120`)
- capture-binding manifest note `corpus/source-snapshots/round-71/manifest.json:3` (the 15-quote manifest C2's
  `sourced_claim` rests on)

## 0. Preconditions measured

```
$ git -C <lane> show 3cc8cd4…:corpus/source-snapshots/round-71/S106.txt | sha256sum
291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db  -
$ … | wc -l
148
$ python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-71/manifest.json --source S106
S106:sha256 OK
S106:Q01-scope OK occurrences=2 anchor=28-ok
S106:Q02-acquisition OK occurrences=1 anchor=31-ok      … (Q03..Q14 each occurrences=1, anchor-ok)
S106:Q15-nolimit OK occurrences=1 anchor=60-ok
EXIT=0
$ python3 -B corpus/instruments/frontier-recheck-count.py
FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106
PASS     F49  knowledge/zdi-disclosure-process-and-vendor-coordination.md ids=S106 exit=0
entries=52 pass=52 exit=0
$ python3 -B corpus/instruments/capture-binding-check.py
AUDIT … orphans=1 orphan=S040-live.txt
records=85 bound=85 unbound=0            (exit 0; the orphan line is pre-existing)
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	… (six inherited W04 lines: S028, S029, S072, S076, S080, S085)
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

Quote-level sweep (script over the entry): 67 double-quoted spans. Every span presented as a capture quote resolves to the
anchor line cited beside it; the 8 spans absent from the capture are the six rejected propositions (L164-185, declared by
the entry as its own phrasing) and two labels used as terms, not quotes ("ZDI disclosure timeline", "what does this page
establish?"). **0 misquotes, 0 false provenance.** All 15 manifest quotes are substrings of their declared anchor line ([28,31,47,49,70,70,70,52,51,60,62,61,69,72,60]). `wc -w` of Q01..Q15 = 7,13,19,5,15,15,25,19,12,19,19,16,19,18,13 (max 25) and the eight
"further span" counts = 15,17,22,19,16,21,25,10 — all match entry L199-228. Numeric claims: `"120 days"` occurs once
(L70), `"15 business days"` once (L70), `"30, 60, or 90"` once (L70); Q01 occurs twice (L28, L102), pinned at the first.
Entry claims 148 lines / 15004 bytes for the capture: `wc -l`=148, `stat` bytes=15004 — both match.

## 1. Two lists

### 1a. What S106 states (disclosure-relevant, line-anchored)

1. Self-description, first party: "the world's largest vendor-agnostic vulnerability disclosure program" (28).
2. Brand as printed: title "About Us - TrendAI™ Zero Day Initiative™ (ZDI)" (1); footer "©2026 TrendAI™ Zero Day
   Initiative™ (ZDI)." (127); contact addresses remain `zdi@trendmicro.com` (130), `media_relations@trendmicro.com` (132).
3. Acquisition model: "A vendor-agnostic bug bounty program where researchers are financially incentivized to submit
   vulnerabilities." (31).
4. Programme history/counts: established 2005 (29); "more than 19,000 independent researchers", 14 threat centers (34);
   "15,000+" disclosed since 2007 (95); "73%" of 2024 global disclosures (97); "35+" Pwn2Own events since 2007 (99).
5. Process guarantee: handled responsibly, not resold/redistributed/censored (47); every acquired vulnerability managed
   under ZDI's disclosure policy (47).
6. Validation first; impact and severity confirmed; technical details documented (49).
7. "Once validated, the researcher receives their reward, and the issue is privately shared with the affected vendor" (49).
8. During the coordination window ZDI deploys protection filters for its customers "without revealing sensitive exploit
   information", and helps with root cause, fix feasibility and patch (50).
9. On patch release: full advisory with technical details, credit (unless anonymous), links to the vendor patch (51).
10. "If a vendor does not produce a fix or declines to address the issue within the coordination timeline, ZDI **may**
    publish a limited advisory … while withholding information that could enable exploitation"; may also share sanitized
    information with other vendors/researchers "beyond Trend customers" (52).
11. Researcher flow: report → validate → confirm severity → formal monetary offer → accept → payment → "the case enters
    the vendor coordination phase" (60); points, "bonus multipliers, higher payout tiers", Pwn2Own invitations (60);
    "imposes no limit on the number of reports" (60); loyalty bonuses, priority processing (60).
12. ZDI handles all vendor communication incl. patch timelines and disclosure scheduling (61); credit / anonymous /
    pseudonym (61).
13. "Every case is tracked, managed under a defined timeline, and disclosed according to our disclosure policy even if a
    vendor declines to issue a patch" (62); "guarantees that your work will not disappear into a backlog" (62).
14. Vendor dossier: proof of concept, reproducible steps, severity assessment, exploitability insight (69).
15. "Vendors are given a standard coordination window of 120 days under TrendAI™ ZDI's disclosure policy" (70).
16. Shortened window "to 30, 60, or 90 days, depending on multiple factors" for "flaws that result from incomplete or
    problematic security patches" (70); a parenthetical points to "our failed patch disclosure policy" (70).
17. "If a vendor fails to respond within 15 business days of first contact, TrendAI™ ZDI **may** escalate to a limited
    public advisory to protect users" (70).
18. On a vendor patch: joint advisory with full credit and links (71); refusal/unresponsive: "may publish a full or
    limited advisory" (72); sanitized sharing in certain cases (72).
19. Pwn2Own mentioned at 43, 60 (invitation), 80 ("breakthroughs demonstrated at … Pwn2Own contests"), 99 (35+ events).

### 1b. What a reader is tempted to attribute that the page does not state

1. That 120 days is an industry/coordinator norm, or that other programmes use it — the page attaches it to "TrendAI™
   ZDI's disclosure policy" only (70). **No artifact appears to make this claim** (see test (a)).
2. That 30/60/90 is selected by severity — this page says only "depending on multiple factors" (70). No factor is named
   here. (ZDI's *policy* page does tier it; see §4 C1.)
3. That escalation/publication is automatic after 15 business days — the page says "may escalate" (70).
4. That the no-backlog guarantee binds coordinated disclosure generally or another programme (62: ZDI's own cases).
5. That the page states a severity taxonomy, CVSS band or payout amount — it states none (49, 60, 69 mention severity
   confirmation/assessment only).
6. Anything about Microsoft (0 occurrences in the capture) or any Pwn2Own finding/vendor outcome (the page states none).
7. That ZDI/Trend Micro was renamed to "TrendAI" — the page prints "TrendAI™" as its current brand and never states a
   renaming (`rebrand|renam` = 0 hits).
8. That the page carries a publication or revision date — it carries only historical years (29, 95, 97, 99) and ©2026 (127).
9. That the 120-day clock starts at submission/validation/first contact — the page names no start for that window; "first
   contact" is the reference for the 15-business-day branch only (70).
10. That ZDI publishes a *full* advisory when a vendor declines within the timeline (:52 says limited; :72 says full or
   limited for refusal/unresponsive) — the two branches overlap and must not be collapsed.
11. That the reward at :49 is the payment at :60 — the page describes them in two sections and never equates them.
12. That the 15 business days sit on an acknowledgement ladder (5+5) — that is S075:23, not this page.
13. That protection filters are deployed only after disclosure — the page says during the coordination period, before
    vendor patches (50).
14. That "TrendAI ZDI" is a different organisation from Trend Micro — the same page routes e-mail to `trendmicro.com`.

## 2. OUTRUNS=8

Every O carries: artifact+line, the anchor, the source line, the correction. O1-O4 are in the entry (R108's subject);
O5-O8 are in the binding rows/note, which are claims too.

**O1 — entry L133-135 (high).** Sentence: "Where a number below is ZDI's own statement about its own programme, a package
that restates it as a general rule, as another coordinator's deadline, or as a severity-tiered window has left the source."
Anchor: `S106.txt:70`. Source line: the shortened window is stated for "flaws that result from incomplete or problematic
security patches … depending on multiple factors" (70) — but the same ZDI that owns this page states the tier selection on
its policy page: "For critical-rated bugs where active exploitation is detected or imminent, the vendor will have 30 days …
critical- and high-severity vulnerabilities where the original patch does offer some protection and exploitation is not
imminent … 60 days. All other reports in this category will be given a time of 90 days." (`S075.txt:25`, held by F02,
`corpus/knowledge/zdi-disclosure-policy.md`). As written, the entry tells a reader that a severity-tiered restatement is
off-source, while the lane's own F02 entry records it as ZDI's stated policy.
Correction: replace "has left the source." with "has left this page; the severity-selected shortened-window tiers ZDI
states on its policy page stay with F02/S075 (`S075.txt:25`)."

**O2 — entry L168-171 (high).** Sentence: "Rejected: ZDI states the shortened window for \"flaws that result from
incomplete or problematic security patches\" (`S106.txt:70`) and names no severity band, only \"depending on multiple
factors\" (`S106.txt:70`)." Anchor `S106.txt:70`. The subject is "ZDI", not "this page"; ZDI does name severity bands
(`S075.txt:25`: "critical-rated", "critical- and high-severity"). The sentence is true of S106 and false of ZDI, and it
contradicts F02 in the same lane. (Entry L92 gets this right: "the page names no factor …" — the body is internally split.)
Correction: "Rejected: this page states the shortened window for … and names no severity band, only \"depending on multiple
factors\" (`S106.txt:70`); severities select the shortened length on ZDI's policy page, which stays with F02/S075
(`S075.txt:25`)."

**O3 — entry L239-241 (medium).** Sentence: "**The factors behind 30/60/90 are not enumerated.** ZDI states \"depending on
multiple factors\" (`S106.txt:70`) and does not list them, so a package cannot select a shortened length for a given finding
from this page." Anchor `S106.txt:70`. "ZDI … does not list them" is falsified by `S075.txt:25`, which lists exactly those
factors; only the page-local reading survives, and the "from this page" qualifier sits on the consequence clause, not on
the claim. Correction: "**The factors behind 30/60/90 are not enumerated on this page.** The page states \"depending on
multiple factors\" (`S106.txt:70`) and does not list them, so a package cannot select a shortened length for a given finding
from this page; the policy page's severity and exploitation tiers stay with F02/S075 (`S075.txt:25`)."

**O4 — entry L146-149 (medium).** Sentence: "If the package states 30, 60 or 90 days it must carry ZDI's own condition
\"For flaws that result from incomplete or problematic security patches\" (`S106.txt:70`); a package that applies the
shortened windows to ordinary reports fails this check." Anchor `S106.txt:70`. The rule is stated as unconditional, so a
package grounded in F02/S075 ("30 days for a critical-rated bug where active exploitation is detected or imminent",
`S075.txt:25`) states 30 days, carries S075's condition and would still be failed by F49 check #2, while F02's own package
rule requires a *different* mandatory condition set ("preserve both partial protection and no imminent exploitation, not
merely severity"). Two acceptance predicates now bind the same numbers. Correction: append "The check binds packages that
state the figure on this page's authority; where a package cites F02/S075's policy-page tiers, S075's severity and
exploitation conditions apply instead."

**O5 — registry row `corpus/SOURCES.md:118` (medium).** Cell text: "escalation to a limited public advisory after 15
business days of vendor silence". Source: "If a vendor fails to respond within 15 business days of first contact, TrendAI™
ZDI **may** escalate to a limited public advisory to protect users" (70). The row drops the permission, converts
"fails to respond within … of first contact" into "after … of vendor silence", and thereby states the one formulation the
entry's own check #3 (L150-152) declares failing: "a package that says ZDI publishes after 15 business days of silence fails
this check." Correction: "ZDI's permissive escalation to a limited public advisory if a vendor fails to respond within 15
business days of first contact".

**O6 — frontier row `corpus/README.md:1114` (medium).** Same phrase, same defect: "escalation to a limited public advisory
after 15 business days of vendor silence". A frontier row is a claim (R108's test applies to it). Same correction as O5.

**O7 — manifest note `corpus/source-snapshots/round-71/manifest.json:3` (low).** "… escalation after 15 business days of
silence …". The capture-binding manifest is citable and C2's `sourced_claim` rests on it; the note states the escalation as
a scheduled step. Correction: "a permissive escalation to a limited public advisory if a vendor fails to respond within 15
business days of first contact".

**O8 — registry row `corpus/SOURCES.md:118` (low).** Anchor cell: "the served page shows no visible publication or revision
date, the only date signal being a 2026 copyright line at L127". False as written: the capture carries 2005 (L29,
"established in 2005"), 2007 (L95, L99), 2024 (L34, L97) and ©2026 (L127). True only for publication/revision dates, which
the clause already says. Correction: "the served page shows no visible publication or revision date; its other year signals
are 2005 (L29), \"since 2007\" (L95, L99), 2024 (L34, L97) and the 2026 copyright line (L127)".

Counted but borderline (listed so the integrator can rule): (i) entry L64 "ZDI prints the flow as: submission → validation
→ reward → private sharing with the vendor → vendor coordination → advisory" — a synthesis of :49-:51 plus :60; the page
never prints an arrow chain and pays "reward" at :49 but "formal monetary offer … payment" at :60; each arrow is supported
by contiguous anchored text, so not counted, but "as a synthesis of S106.txt:49-51 and :60" would close it. (ii) entry L6
ground line "the 15-business-day escalation to a limited public advisory" — same modality family as O5-O7, but a topic
label; the reproducible edit is "the 15-business-day escalation to a limited public advisory" → "ZDI's permissive
15-business-day escalation to a limited public advisory". (iii) entry L122 "Both sentences are ZDI's own guarantee" — the second (:62) is
written as practice, the word "guarantee" is at :62 for the first only. (iv) entry L179-180 "this page states only a formal
monetary offer" — the same page also states "bonus multipliers, higher payout tiers" (:60), which L242-244 does record.
(v) entry L55 row key "submission volume" heads a quote about a report-count limit, not volume.

## 3. The seven required temptation tests

| test | verdict | evidence |
|---|---|---|
| (a) 120 days as an industry/coordinator norm | PASS | entry L10-16 and L133-135 scope it to ZDI's own policy; registry: "not a coordinator's statutory timeline", "not as a universal deadline"; F49 row: "Read … not as a universal deadline" |
| (b) 30/60/90 as a severity ladder | PASS on over-attribution, FAIL on over-correction | entry L87, L91, L148, registry: "for flaws that result from incomplete or problematic security patches"; F49 row: same condition — no artifact applies 30/60/90 to ordinary reports. Inverse defect: O1-O3 deny ZDI's policy-page tiers |
| (c) "may escalate" read as a deadline guarantee | FAIL in the binding artifacts, PASS in the entry body | entry L88, L93-94, L150-152, L172-175 are correct; O5, O6, O7 are the failures |
| (d) "no backlog" read as applying to other programmes | PASS | stated only at entry L116-123, explicitly "not a property of coordinated disclosure in general"; absent from registry/F49 row |
| (e) page read as a severity taxonomy | PASS | entry L127-129, L242-246; registry "not a platform severity ladder" |
| (f) Microsoft / Pwn2Own attributed to the page | PASS | `grep -c -i microsoft S106.txt` = 0; artifacts assert no Microsoft or Pwn2Own finding; page mentions Pwn2Own at 43, 60, 80, 99 only |
| (g) a rebrand claim the page does not support | PASS | `rebrand|renam` = 0 hits in capture and artifacts; "TrendAI™ Zero Day Initiative™ (ZDI)" is the page's own title (1) and footer (127), with `@trendmicro.com` addresses (130, 132), so the naming is page-supported and no renaming is claimed |

## 4. Coverage and duplicate authority (not outruns)

**C1 — duplicate authority by subject (R114).** F02/S075 already holds ZDI's 120-day window (`S075.txt:24`), the
30/60/90 truncation (`S075.txt:25`) and the fifteen-business-day escalation (`S075.txt:23`). Committed `README.md:1116-1117`
says F49 "adds … statements, which the lane did not hold": true of the About page's own sentences, false of four of the
five items the frozen C2 sentence lists as F49's ground. Correction: name the four already-held numbers and confine F49's
novelty to the acquisition-side flow (:60), the dossier (:69), "no limit on reports" (:60) and the no-backlog guarantee
(:62). The lane **working tree** already carries an uncommitted `[r71 erratum 1]` (README.md:1121-1133) that does this; it
is not in `3cc8cd4` and was not audited (see §6).

**C2 — coverage gap, misclassified.** `S106.txt:50`: "During this period, TrendAI™ ZDI deploys protection filters for its
customers without revealing sensitive exploit information." The entry files "protection-filter deployment" under "general
programme claims" beside founding year and counts (L247-250) and does not state it, although it is a statement inside the
disclosure-process section and the frontier is "disclosure process and vendor coordination". Correction: cover it in the
windows section, or list it as an explicit process-scope exclusion rather than a "general programme claim".

**C3 — coverage gap.** `S106.txt:71` ("When the vendor issues a patch, TrendAI™ ZDI publishes a joint advisory with full
credit to the researcher (if they choose) and links to the vendor's fix") is not covered; the advisory table cites :51 only.
Correction: add the :71 wording as a row, or state that :71 restates :51.

**C4 — cell placement.** The registry row's *anchor* cell carries scope prose ("not a platform severity ladder", the date
sentence) and the *scope* cell carries the locator digest. The row still parses (11 cells, `sources-census.sh validate`
exit 0), so this is placement, not a defect.

## 5. Entry hash before / after

```
before (committed, 3cc8cd4):  6f304a052190d988b189ed82d547b0ba53562fc6837fa3dd52a8dbfb87986684
after  (this seat's proposed wording, applied to a SCRATCH COPY only):
                              65ba64546b60acc948f99a6614e6c2835031a8136900cba2a5976345412e7700
```
The entry was **not** edited in the lane (this seat writes only its report). The after-hash is of
`/fast/scratch/hyaku/kasegi-r71/AttackC2/entry-proposed.md`, produced by five hunks in
`/fast/scratch/hyaku/kasegi-r71/AttackC2/`: the four numbered corrections O1-O4 plus the ground-line wording of
borderline item (ii). Applying only O1-O4 yields a different digest; the integrator's own wording will too — R108's
erratum must name the hash it actually lands. The patch is reproducible from this report: O1-O4 as written above, plus the
ground-line replacement of "the 15-business-day escalation to a limited public advisory" with "ZDI's permissive 15-business-
day escalation to a limited public advisory". In the patched copy no quoted span was altered and all 67 spans still resolve.

## 6. Notes, limits, and state at audit time

- **Working tree, not tip.** At audit time `git -C <lane> status --porcelain` shows uncommitted tracked modifications to
  `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md` (+13 lines: an `[r71 erratum 1]` draft) and
  `corpus/lessons/round-71.md`. All findings above are against the committed bytes at `3cc8cd4`; the working-tree draft was
  read only to avoid duplicating a sibling's correction (C1), and it is not ground for any verdict here.
- **Capture hygiene.** The tag-stripped capture retains HTML-comment text: L2-4 ("(from the old blog.html shell).", "Swap
  this in if the full responsive set above causes background styling issues.", "-->") and a stray "-->" at L125. No
  anchor or quoted span sits inside that residue, so no entry sentence quotes non-rendered text; but "the served page"
  in the registry row (O8) means the *rendered* text only, since raw HTML (and any `<meta>` date) is not retained.
- **Not audited**: attempts' other seats' verdicts (absent), the C1 side of this round, and the entry's factual accuracy
  against the live page (the recheck verifies pinned bytes only).
- **Tooling.** None installed or upgraded; all checks ran on the host's `python3`, GNU coreutils and the lane's committed
  instruments.
- **No production file was written.** Only this report.
