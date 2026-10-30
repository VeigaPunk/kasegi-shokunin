# R47W2NoHarm — integrated revision comparison

## Axes
- **Verifiability:** compare frozen base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8` to integrated revision `65e19bdb142c90a08103eb4b2af60c71218a920e` using read-only git inspection.
- **Coverage:** original captures/counters, entry length, deletion scope, base prefixes, registry-cell constraints, and frozen-target honesty.

## Exact retained evidence
Commands below were executed from the repository root; no build, test, mutation battery, runtime, or selftest was run.

```text
git diff --stat BASE INTEGRATED
277 files +49636 -77

git diff --name-status BASE INTEGRATED -- ':!.ufo/waves/round-47'
M LOG.md
M SKILL.md
M corpus/QUALITY.md
M corpus/README.md
M corpus/SOURCES.md
M corpus/instruments/README.md
A corpus/instruments/entry29-fixed-bytes.md
M corpus/instruments/knowledge-expected.txt
A corpus/instruments/r47-counters-selftest.py
A corpus/instruments/r47-f30-gate.py
A corpus/instruments/r47-mutbat.py
A corpus/instruments/r47-routed-defects.py
A corpus/instruments/r47-counters-selftest.py
M corpus/knowledge/github-repository-security-advisories.md
A corpus/knowledge/zdi-disclosure-policy.md
M corpus/lessons/round-46.md
A corpus/lessons/round-47.md
A corpus/source-snapshots/round-47/S075.txt
A corpus/source-snapshots/round-47/S076.txt
A corpus/source-snapshots/round-47/manifest.json

entry-lines=145
S074-blob-base=2eb0c3a71ca8f4ffa524f33205b332c2d8d87f54
S074-blob-integrated=2eb0c3a71ca8f4ffa524f33205b332c2d8d87f54
tracked-deletions-outside-wave: [empty]
```

Note: the raw name-status output includes further added round-47 instrument files beyond the excerpt above; no deletions were reported. The exact command output for that query was recorded in the tool transcript. The diff stat is dominated by round-47 wave evidence and the 610-line successor capture.

## Findings

- **Original capture preserved:** S074's committed blob is identical between base and integrated revision (blob id above); the capture remains historical evidence. `corpus/lessons/round-47.md:20-21,59,65-69` explicitly describes retaining S074 mined and using S076 as the successor.
- **Frozen counters unchanged:** `corpus/lessons/round-47.md:61` says counters remain byte-frozen; `corpus/lessons/round-47.md:51` differentiates frozen base replay from the live-tree changes. Static inspection of the base-to-integrated changed paths shows the newly added round-47 counters and no changed pre-existing counter files. The freeze record `.ufo/waves/round-47/freeze.txt` records the frozen instrument digests. No counter execution was performed for this review.
- **Entry length:** integrated `corpus/knowledge/github-repository-security-advisories.md` is exactly 145 lines. Its changes re-anchor the entry from S074 to S076 and repair provenance/chrome and order statements; this matches the lesson's D5/D6/D8 decisions (`corpus/lessons/round-47.md:9-12,67`).
- **Tracked deletions outside wave evidence:** none. The only observed corpus source modifications are append/repair operations; the explicit deletion-filter query returned no paths.
- **Base prefixes:** `LOG.md`, `SKILL.md`, `corpus/QUALITY.md`, and `corpus/README.md` all have appended-only additions in the base-to-integrated diff. For LOG and SKILL, diff hunks begin at the old EOF. The displayed QUALITY/README diffs were not captured line-for-line in the exact evidence output; prefix retention is assessed statically from the integrated tree and is consistent with the diff summary. No leading-prefix replacement observed.
- **Original registry cells:** `corpus/lessons/round-47.md:67` records only S074 `used-by` change, with S074 status and recheck unchanged and no other pre-existing cell changes. `corpus/SOURCES.md` diff shows the S074 row plus new S075/S076 rows; the old S074 row's changed text is consistent with the stated used-by disposition. This cell claim is static review, not a registry gate execution.
- **Frozen claim misses are retained honestly:** lesson lines 59-60 and 65 report C1 unmet (S074 remains mined because rejection breaks B3) and C2 unmet (ZDI is F02 enrichment; no F30). This agrees with the request not to reroll targets.

## Risks / blockers
- No execution evidence is claimed. Main/integration owner should run its planned post-integration gates; this reviewer did not.
- The exact wide diff has 277 changed paths overall and the output was truncated by the tool. The filtered non-wave changed-path listing was also truncated; claims above about relevant source files are based on shown output and targeted diffs, not an exhaustive preserved listing. No blocking discrepancy found in the evidence inspected.
- No tools installed or updated; no pacman transaction or service restart attempted.