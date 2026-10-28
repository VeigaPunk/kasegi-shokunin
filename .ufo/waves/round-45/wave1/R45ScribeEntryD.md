VERDICT: DRAFT-READY

# R45ScribeEntryD — C2 entry drafter D (F27, Linux kernel security-bugs reporting process)

Draft only. Nothing committed, nothing written to the tree outside this report and the draft directory. The draft is `.ufo/waves/round-45/wave1/R45ScribeEntryD.draft/linux-kernel-security-bugs-reporting-process.md` (1589 words, 13-row table). The frontier row (`corpus/README.md`), the SOURCES row S071 and the entry file itself are for L1 to land; I did not write them into the tree.

## Finding 1 — the draft satisfies the entry-level constraints I can check

Command run (read-only, on the draft):
```
grep -n "^## \|^source: \|^verified-at: \|^recheck: " <draft>
```
printed:
```
3:source: S071 — https://docs.kernel.org/process/security-bugs.html — section anchors: Preparing your report (S071.txt:10-71); What qualifies as a security bug (S071.txt:73-107); Responsible use of AI to find bugs (S071.txt:174-252); Disclosure and embargoed information (S071.txt:299-327); RST capture at `corpus/source-snapshots/round-45/S071.txt`.
4:verified-at: 2026-10-28
5:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d
7:## Scope and decision rule
31:## Overlap and novelty
45:## Limits
52:## Falsifiable package rule
56:## Rejected over-generalizations
```
Layout note: the brief says "lines 1-4" but lists five items (title, blank, source, verified-at, recheck). I followed the house template (title line 1, blank line 2, provenance on lines 3-5, blank line 6). The gate's G2 reads the first 8 lines.

Table: 13 data rows, columns `observed question | kernel text | package consequence` (header line 15). Sections present: Scope and decision rule; table; Overlap and novelty (F02, F04, F15 held state, then the three new items); Limits; falsifiable package rule; rejected over-generalizations.

## Finding 2 — every curly-quoted span is located in the pinned S071 capture (self-check)

Verifier: `$SCR/verify.py` (a replica of the gate's G5 regex and `norm()` from `corpus/instruments/r45-c2-gate.py`, scratch-only). Command:
```
TMPDIR=$SCR python3 $SCR/verify.py <draft> corpus/source-snapshots/round-45/S071.txt
```
Printed (exact):
```
curly-quoted spans total=24 with-citation=24
curly quotes lacking citation: []
PASS L17-18 words=11 :: The following information are absolutely necessary in any security bug report
PASS L20-22 words=10 :: with no version indication, your report will not be processed
PASS L22-23 words=14 :: A stable identifier such as a commit ID or an exact version is required
PASS L23-24 words=15 :: Versions designating kernels not coming from kernel.org (such as distro kernels) are meaningless to maintainers
PASS L39-40 words=5 :: Binary-only executables are not accepted
PASS L41-43 words=19 :: By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug
PASS L95-96 words=16 :: If you resorted to AI assistance to identify a bug, you must treat it as public
PASS L99-99 words=12 :: do not publicly share a reproducer, as this could cause unintended harm
PASS L210-211 words=9 :: the reproducer should only be shared upon maintainers' request
PASS L305-305 words=11 :: Once a robust fix has been developed, the release process starts
PASS L342-344 words=23 :: for the kernel security team occasional embargoes (as subject to a maximum allowed number of days) start from the availability of a fix
PASS L310-311 words=21 :: for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days
PASS L312-312 words=13 :: if it is agreed that the criticality of the bug requires more time
PASS L312-314 words=18 :: The only valid reason for deferring the publication of a fix is to accommodate the logistics of QA
PASS L350-350 words=9 :: a fix is accepted by the affected code's maintainers
PASS L271-272 words=10 :: If there are two or fewer recipients in your message
PASS L272-273 words=10 :: you must also always Cc: the Linux kernel security team
PASS L362-363 words=16 :: The security team does not assign CVEs, nor do we require them for reports or fixes
PASS L208-209 words=9 :: the validity of the report should be seriously questioned
PASS L333-334 words=15 :: other groups focus on fixing issues in distros and coordinating disclosure between operating system vendors
PASS L241-242 words=23 :: Prepare a plain-text report explaining the problem. It must contain the four items listed at the top of this file as absolutely necessary
PASS L309-310 words=14 :: this may be postponed at the request of the reporter or an affected party
PASS L117-117 words=5 :: or use of AI-based tools
PASS L332-332 words=6 :: solely focuses on getting bugs fixed
```
`grep -c PASS` → 24; `grep -c FAIL` → 0.

The line numbers were also checked with `sed -n` per cited window, one call per span. Examples of what it printed (full set in the run log, summarised here):
- `sed -n 310,311p` → line 310 "the reporter or an affected party for up to 7 calendar days from the start", line 311 "of the release process, with an exceptional extension to 14 calendar days".
- `sed -n 95,96p` → line 95 "**If you resorted to AI assistance to identify a bug, you must treat it as", line 96 "public**. While you may have valid reasons…" (the `**` is removed by the gate's normaliser).
- `sed -n 39,40p` → line 39 "instructions, file-system image etc).  Binary-only executables are not", line 40 "accepted.  Working exploits…".
- `sed -n 41,43p` → line 41 "…unless they are already public.  By", line 42 "definition if an issue cannot be reproduced, it is not exploitable, thus it", line 43 "is not a security bug."
- `sed -n 208,209p` → line 208 "the reproducer does not work, or if the tool cannot produce one, the", line 209 "validity of the report should be seriously questioned…".
- `sed -n 117,117p` → "anyone, or use of AI-based tools)." The span is within the single line 117.
Two corrections were made during this self-check and are in the draft: the F04 quote was first cited as 209 and failed (it starts on 208), now `S071.txt:208-209`; and "or use of AI-based tools" was first in prose without a citation directly after it, now `(`S071.txt:117`)` immediately after.

All 24 spans are at most 25 words (max 23). Quote text contains no curly quotes inside, and no quote is stitched from two places except where the cited window is a 2–3-line span of one sentence.

## Finding 3 — the gate's G5 counter on the draft, in a scratch fixture (positive)

Fixture (scratch only): a copy of `corpus/instruments/source-recheck.py`, `r45-c2-gate.py`, the S071 capture, `manifest.json`, the draft copied to `corpus/knowledge/`, and a one-row `corpus/README.md` with F27 pointing at the draft. Command:
```
TMPDIR=$SCR python3 $SCR/tree/corpus/instruments/r45-c2-gate.py --root $SCR/tree
```
Relevant printed lines:
```
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=24 located=24 failed=0 cores=4/4
c2-gate fixed=3/7 exit=1
```
G1, G3, G6, G7 fail in this fixture only because it has no SOURCES.md, no 27-row frontier and no full knowledge directory. I claim G5 and G2/G4 only.

## Finding 4 — negative control: a fabricated quote is refused by G5

Control: the same fixture with the 7-day quote altered in the entry to "for up to 10 calendar days from the start of the release process" (the line-310 and 311 text in the source says 7 and 14). Command and printed line:
```
sed -i 's/for up to 7 calendar days from the start/for up to 10 calendar days from the start/; s/“for up to 7 calendar days/“for up to 10 calendar days/' <neg>/corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
TMPDIR=$SCR python3 <neg>/corpus/instruments/r45-c2-gate.py --root <neg>
gate G5 pass=0 read=spans=24 located=23 failed=1 cores=3/4
c2-gate fixed=2/7 exit=1
```
G5 discriminates: one fabricated span fails and the "up to 7 calendar days" core is lost (cores 3/4). The untouched draft passes (Finding 3).

## Finding 5 — do-nothing control on the live lane tree, and a drift against the freeze record (read-only)

Command (read-only; the gate writes nothing):
```
TMPDIR=$SCR python3 corpus/instruments/r45-c2-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
```
Printed:
```
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G2 pass=0 read=F27-rows=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=0 read=F27-rows=0
gate G6 pass=0 read=knowledge=63
gate G7 pass=1 read=census-rc=0
c2-gate fixed=2/7 exit=1
```
The freeze record `.ufo/waves/round-45/controls/freeze-controls.txt` says `control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED`. The live tree reads 2/7, so the do-nothing control has drifted, not held. Differences: G7 now exits 0 (census-rc=0; the freeze measurement reads 1/7 overall) and the README frontier has 26 rows where G1 requires 27. Git state, read-only: `git log -1` → `5242db6fbf2b3575da6600974f0b5b4292caa62f round-45: wave 1 spec (64 seats, policy v2) and dispatch`, while the freeze commit is `8cf62c879e6e6b031e67412f8fac1fba0bd378cf`. `git status --short` shows untracked `.ufo/waves/round-45/wave1/`, `wave1.ready`, `wave1.ready.dispatched` and one round-44 control file. I did not investigate the cause; this is for L1. Note for L1: G6 requires exactly 64 knowledge files and the tree has 63, so landing the F27 entry is what satisfies G6.

## Finding 6 — overlap claims checked against the held entries and S071

- F02 (`corpus/knowledge/coordinated-disclosure-timelines.md`): its rule on line 7 requires policy, clock-starting event, interval, patch/publication relationship and extension; line 17 forbids transplanting another coordinator's interval; lines 22 and 24-25 hold the CERT/CC 45-day and Project Zero 30-day / 14-day grace rows. The draft cites these lines and does not restate the figures as its own.
- F04 (`corpus/knowledge/ai-assisted-finding-validation.md`): lines 7-8 and 15 hold the candidate rule and the reviewer-distinct-from-producer check. `grep -c "reviewer" corpus/source-snapshots/round-45/S071.txt` → `0`, so S071 does not require a distinct reviewer; the draft says so.
- F15 (`corpus/knowledge/vendor-third-party-finding-coordination.md:91-96`, `corpus/README.md:309`): the README row 309 is `| F15 | A vendor's research programme as an intake route for other vendors' bugs | admitted | ...`, and lines 91-96 hold the coordinator-of-record point. The draft uses F15 for "record which party coordinates" and states S071's coordinator as other groups (S071.txt:333-334).
- The version label: the assignment says the page is "versioned 7.3.0 at capture". `grep -c "7\.3" corpus/source-snapshots/round-45/S071.txt` → `0`. The capture carries no version string. The draft says so in its Limits and does not rely on the label.

## Limitations

- Draft only. The frontier row, SOURCES row and entry file in the tree are L1's to land. I did not run G1, G3, G6 or G7 on a real tree with the F27 row in place; the fixture results above cover G2, G4 and G5 only.
- The quote checks are exact-text checks against the pinned capture (fetched 2026-10-28T20:52:44Z per manifest). They are not a current online check.
- My verifier (`verify.py`) replicates the gate's regex and normaliser by hand; the authoritative count is the gate run in Finding 3, which agrees (24/24, cores 4/4).
- Nothing in the entry is a rule of law or a general CVD standard; the entry says so in its Limits.
- No install or upgrade of any tool was needed or performed.
- Scratch root `/fast/scratch/hyaku/kasegi-r45/R45ScribeEntryD/` is removed on exit; this report contains the commands and printed output so the checks can be re-run.
