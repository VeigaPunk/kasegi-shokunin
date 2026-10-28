VERDICT: DRAFT-READY

Scope: C2 entry drafter A, frontier F27 (Linux kernel security-bugs reporting process, source S071). Draft only. Nothing committed, nothing integrated into corpus/README.md, corpus/SOURCES.md or corpus/knowledge/. No git mutation. Scratch removed.

Artifact: `.ufo/waves/round-45/wave1/R45ScribeEntryA.draft/linux-kernel-security-bugs-reporting-process.md` (1765 words; sha256 `291500a12f9d4dde86f1e5605233b22d5fe78500cb7090902bc4215f72b393e7`). Header: line 1 `# Linux kernel security-bugs reporting process`, line 2 blank, line 3 `source: S071 — https://docs.kernel.org/process/security-bugs.html — ...`, line 4 `verified-at: 2026-10-28`, line 5 `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d`. I used the house template's five-line header (title, blank, source, verified-at, recheck) rather than the brief's "lines 1-4" wording, because the template and G2 both expect the recheck line in the header.

## Finding 1 — the source capture was read directly, and the required quotes are in it

Command: `sha256sum corpus/source-snapshots/round-45/S071.txt`
Output: `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  corpus/source-snapshots/round-45/S071.txt` (matches the brief).

Each required anchor, checked by printing its range with `sed -n`:
- Embargo ceiling and 14-day exception, `sed -n '310,311p'`: `the reporter or an affected party for up to 7 calendar days from the start` / `of the release process, with an exceptional extension to 14 calendar days`.
- AI treated as public, `sed -n '95,96p'`: `**If you resorted to AI assistance to identify a bug, you must treat it as` / `public**. While you may have valid reasons to believe it is not, the security`.
- Binary-only refusal, `sed -n '39,40p'`: `instructions, file-system image etc).  Binary-only executables are not` / `accepted.  Working exploits are extremely helpful and will not be released`.
- Unreproducible is not a security bug, `sed -n '41,43p'`: `without consent from the reporter, unless they are already public.  By` / `definition if an issue cannot be reproduced, it is not exploitable, thus it` / `is not a security bug.`
- Version range, `sed -n '20,21p'`: `  * **affected kernel version range**: with no version indication, your report` / `    will not be processed.  Note that a time-dependent version such as "latest`.

## Finding 2 — the draft's own quote self-check (every curly-quoted span with its citation)

Method: every span in the draft matching the gate's own pattern (curly quote, optional whitespace, `(`, backticked `S071.txt:N[-M]`) was located in the cited lines after the gate's normalisation, and each span's `sed -n` range was printed. Result: 34 spans, 34 located, 0 unlocated, 34 opening and 34 closing curly quotes (so no uncited curly quotes remain). Longest quote 22 words (limit 25).

Per span, the cited range, the `sed -n` command, and the printed first line:

| # | cited | sed -n command | printed (first line) | located |
|---|---|---|---|---|
| 1 | 17-18 | `sed -n '17,18p'` | `information is helpful.  The following information are absolutely necessary in` | yes |
| 2 | 89-90 | `sed -n '89,90p'` | `The security list exists for urgent bugs that grant an attacker a capability` | yes |
| 3 | 103-104 | `sed -n '103,104p'` | `If you are unsure whether an issue qualifies, err on the side of reporting` | yes |
| 4 | 105-106 | `sed -n '105,106p'` | `a real vulnerability.  Reporting ordinary bugs to the security list, however,` | yes |
| 5 | 20-21 | `sed -n '20,21p'` | `  * **affected kernel version range**: with no version indication, your report` | yes |
| 6 | 22-23 | `sed -n '22,23p'` | `    mainline" is not acceptable.  A stable identifier such as a commit ID or an` | yes |
| 7 | 23-25 | `sed -n '23,25p'` | `    exact version is required.  Versions designating kernels not coming from` | yes |
| 8 | 26-27 | `sed -n '26,27p'` | `    have already been fixed, so it is extremely important that vulnerabilities` | yes |
| 9 | 28-29 | `sed -n '28,29p'` | `    version), at least by verifying that the code has not changed since the` | yes |
| 10 | 39-40 | `sed -n '39,40p'` | `    instructions, file-system image etc).  Binary-only executables are not` | yes |
| 11 | 38-39 | `sed -n '38,39p'` | `    dependencies will be needed (source code, shell script, sequence of` | yes |
| 12 | 41-43 | `sed -n '41,43p'` | `    without consent from the reporter, unless they are already public.  By` | yes |
| 13 | 95-96 | `sed -n '95,96p'` | `**If you resorted to AI assistance to identify a bug, you must treat it as` | yes |
| 14 | 97-98 | `sed -n '97,98p'` | `team's experience shows that bugs discovered this way systematically surface` | yes |
| 15 | 99 | `sed -n '99p'` | `case, do not publicly share a reproducer, as this could cause unintended harm;` | yes |
| 16 | 210-211 | `sed -n '210,211p'` | `    report will be posted to a public list, the reproducer should only be` | yes |
| 17 | 100-101 | `sed -n '100,101p'` | `just mention that one is available and maintainers might ask for it privately` | yes |
| 18 | 113-114 | `sed -n '113,114p'` | `affected subsystem's maintainers and Cc: the Linux kernel security team.  Do` | yes |
| 19 | 116-117 | `sed -n '116,117p'` | `widely available automated vulnerability scanning tool that can be repeated by` | yes |
| 20 | 271-273 | `sed -n '271,273p'` | `The report must be sent to maintainers.  If there are two or fewer` | yes |
| 21 | 169-170 | `sed -n '169,170p'` | `maintainers, **and only in this case**, it's possible to send your report to` | yes |
| 22 | 169 | `sed -n '169p'` | `maintainers, **and only in this case**, it's possible to send your report to` | yes |
| 23 | 310-311 | `sed -n '310,311p'` | `the reporter or an affected party for up to 7 calendar days from the start` | yes |
| 24 | 305 | `sed -n '305p'` | `Once a robust fix has been developed, the release process starts.  Fixes` | yes |
| 25 | 312-314 | `sed -n '312,314p'` | `if it is agreed that the criticality of the bug requires more time.  The` | yes |
| 26 | 362-363 | `sed -n '362,363p'` | `The security team does not assign CVEs, nor do we require them for` | yes |
| 27 | 171-172 | `sed -n '171,172p'` | `will receive instructions about whom to contact, if needed.  Your message may` | yes |
| 28 | 17-18 | `sed -n '17,18p'` | (as #1; the span "absolutely necessary" sits inside it) | yes |
| 29 | 241 | `sed -n '241p'` | `1. Prepare a plain-text report explaining the problem. It must contain the` | yes |
| 30 | 246 | `sed -n '246p'` | `2. Start the report with a temporary section listing the recipients' addresses` | yes |
| 31 | 195-196 | `sed -n '195,196p'` | `Please **always convert your report to plain text** without any formatting` | yes |
| 32 | 371-372 | `sed -n '371,372p'` | `The Linux kernel security team is not a formal body and therefore unable` | yes |
| 33 | 82-83 | `sed -n '82,83p'` | `It turns out that the majority of the bugs reported via the security team are` | yes |
| 34 | 345-346 | `sed -n '345,346p'` | `they start from the initial post to the list regardless of the` | yes |

Spans 22/28 are nested inside 21/1 and are listed for completeness; each is still individually located.

Mutation check (is the gate discriminating?): I copied the draft to scratch and made two changes: the binary-only quote was reworded ("are never accepted"), and the 14-day quote was cited at `S071.txt:300-301` instead of `310-311`. The same locator then reported `located=NO` for exactly those two spans (`10 lines 39-40 words=5 located=NO :: Binary-only executables are never accepted` and `23 lines 300-301 words=21 located=NO :: for up to 7 calendar days from the start of the release process, with ...`). So the locator is not vacuous.

## Finding 3 — the frozen C2 gate on the do-nothing control and on the treatment

I did not touch the pure export. I built two scratch trees from `/fast/scratch/hyaku/kasegi-r45/L1/pure`, overlaying only the frozen round-45 captures, manifest and gate/recheck instruments from the lane working tree (read-only inputs). The pure base has no round-45 captures or gate scripts, so the overlay is required to run the gate at all.

(a) Do-nothing control (pure base + captures, no entry, no README row). Command: `python3 .../r45-c2-gate.py --root <base>`. Output:
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

(b) Control with a scratch-only F27 README row but no entry: G1 pass=0 read=F27-entry-missing; G2 pass=0 read=F27-entry-missing; G5 pass=0 read=F27-entry-missing; `c2-gate fixed=2/7 exit=1`.

(c) Treatment: scratch-only F27 README row plus the final draft (copied to `corpus/knowledge/`). Output:
```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=34 located=34 failed=0 cores=4/4
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=6/7 exit=1
```

So the draft moves G2, G5 (all four frozen cores present), G6 (64 knowledge files) and, with the F27 row, G1. G3 is the only gate still failing, and it is not something this draft can satisfy: it needs a `corpus/SOURCES.md` row S071 (11 cells, tier A, status mined, `used-by` naming this entry, anchor cell with the sha256). That row is L1's integration, not drafted here.

Discrepancy not reconciled: the freeze control file records `control do-nothing-base counter=C2 c2-gate fixed=1/7`. My do-nothing rerun gives `fixed=2/7` (G4 and G7 pass) because I overlaid the round-45 captures onto the pure base. I did not investigate which gate the frozen control tree fails; L1 should check that before relying on either number.

## Finding 4 — overlap with F02, F04, F15 (paths read, nothing copied as a new claim)

- F02 `corpus/knowledge/coordinated-disclosure-timelines.md` holds the "name the policy, trigger, interval, extension" rule and the S004 (CERT/CC 45 days) and S005 (Project Zero 90-day, 14-day grace) figures. The kernel 14-day figure is a different rule with a different trigger: the page says the kernel clock starts at release-process start while linux-distros starts at the initial post (`sed -n '345,346p'`). The draft says the two 14-day figures must not be merged.
- F04 `corpus/knowledge/ai-assisted-finding-validation.md` holds candidate-until-reproduced-and-reviewed and the preserve-program-restriction rule. The draft does not repeat it; it adds the kernel's treat-as-public duty and the AI report-content duties.
- F15 `corpus/knowledge/vendor-third-party-finding-coordination.md` holds "name the coordinating party". The kernel security team's forward-as-is role is consistent with it and is cited, not claimed as new.
- Novelty check: `grep -ril 'kernel' corpus/knowledge` printed nothing before the draft existed, so the kernel's required-fields intake contract, AI-assisted report duties and 7/14-day ceiling as a maintainer rule are new in this knowledge base.

## Finding 5 — version label "7.3.0" is not in the capture

The brief says the page is "versioned 7.3.0 at capture". `grep -c '7\.3' corpus/source-snapshots/round-45/S071.txt` printed `0`, and the manifest carries no version. The draft therefore states no version and says so under Limits, rather than citing a label the snapshot does not hold.

## Limitations

- G3 (SOURCES.md row) and the README F27 row are L1 integration; the draft is not integrated. The README row used above was scratch-only.
- Verification ran on scratch copies of the pure base with the frozen round-45 captures overlaid; the lane working tree was not changed.
- The quote check uses the frozen gate's own normalisation, which strips `**` and double backticks and folds curly punctuation; it is a locator, not a reading of the rendered docs page. The capture is the RST source from `docs.kernel.org/_sources/...`.
- The `source-recheck.py` S071 pass (quotes-ok=5) is the frozen manifest's five quotes, not the 34 spans above.
- The house-template header has five lines; the brief's "lines 1-4" wording was read as the template layout.
- Tool installs/updates: none. No commands were run outside the lane's read-only scope apart from the gate and the scratch copies above.

## Limits of this draft (for the knowledge reader)

One upstream project's process; not law; not general guidance; not evidence of response times. The page's own embargo ceiling is a deferral limit on publication of a fix, not a deadline for every report.
