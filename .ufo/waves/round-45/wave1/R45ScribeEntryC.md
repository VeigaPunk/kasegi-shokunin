VERDICT: DRAFT-READY

Seat R45ScribeEntryC, C2 entry drafter C (F27, Linux kernel security-bugs reporting process). Draft only: no commit, no index or git mutation, no shared production file touched. Wrote only the draft directory and this Report. Scratch `/fast/scratch/hyaku/kasegi-r45/R45ScribeEntryC/` used for the gate self-check and removed on exit. No tool installed or upgraded.

## 1. Artifact

Draft: `.ufo/waves/round-45/wave1/R45ScribeEntryC.draft/linux-kernel-security-bugs-reporting-process.md` (61 lines).

- Lines 1-5: `# Linux kernel security-bugs reporting process`, blank, `source: S071 — https://docs.kernel.org/process/security-bugs.html — sections …; RST capture at corpus/source-snapshots/round-45/S071.txt`, `verified-at: 2026-10-28`, `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d`. The recheck sits on line 5, as in the house template; G2 accepts it within the first 8 lines.
- Sections: Scope and decision rule (includes the four mandatory items, S071.txt:17-18); a table of 11 rows, `Observed question | Kernel text | Package consequence`; Overlap and novelty (F02, F04, F15 opened and compared; three new items); Limits; Falsifiable package rule; Rejected over-generalization.
- Every curly-quoted span uses the form `“…” (`S071.txt:N-M`)`. Longest span is 22 words.

## 2. Frozen-gate self-check (G2, G4, G5), run on a scratch tree

Scratch tree: the round-45 snapshot directory and `source-recheck.py` copied in; the draft placed at `corpus/knowledge/`; `r45-c2-gate.py` imported with `entry_path` pinned to the draft path, because the README F27 row does not yet exist (see section 6).

Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071`
Output:
```
S071:sha256 OK
S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=310-ok
S071:Q2 OK normalized=markup-whitespace occurrences=1 anchor=95-ok
S071:Q3 OK normalized=markup-whitespace occurrences=1 anchor=39-ok
S071:Q4 OK normalized=markup-whitespace occurrences=1 anchor=41-ok
S071:Q5 OK normalized=markup-whitespace occurrences=1 anchor=20-ok
recheck_rc=0
```
Command: `selfcheck.py <tree>` (calls gate G2, G4, G5 directly)
Output:
```
G2 pass=1 read=source=1 verified-at=1 recheck=1
G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
G5 pass=1 read=spans=15 located=15 failed=0 cores=4/4
selfcheck_rc=0
```
G1, G3, G6, G7 were not exercised on the tree (see section 6).

## 3. Per-quote line verification (`sed -n`, run by me on the pinned capture)

Each span is matched by the G5 regex (`“([^”]+)”\s*\(`?S071\.txt:N-M`) on the final draft. Line ranges were checked with `sed -n 'N,Mp' corpus/source-snapshots/round-45/S071.txt`:

| # | Draft citation | Words | sed -n output confirming the words (first line shown; quoted words on it or the next) |
|---|---|---|---|
| 1 | S071.txt:17-18 | 11 | `information is helpful.  The following information are absolutely necessary in` / `**any** security bug report:` |
| 2 | S071.txt:20-21 | 10 | `  * **affected kernel version range**: with no version indication, your report` / `    will not be processed.` |
| 3 | S071.txt:21-22 | 12 | `will not be processed.  Note that a time-dependent version such as "latest` / `mainline" is not acceptable.` |
| 4 | S071.txt:23-25 | 20 | `exact version is required.  Versions designating kernels not coming from` / `kernel.org (such as distro kernels) are meaningless to maintainers and` / `will not be processed.` |
| 5 | S071.txt:39-40 | 5 | `instructions, file-system image etc).  Binary-only executables are not` / `accepted.` |
| 6 | S071.txt:41-43 | 19 | `without consent from the reporter, unless they are already public.  By` / `definition if an issue cannot be reproduced, it is not exploitable, thus it` / `is not a security bug.` |
| 7 | S071.txt:45 | 8 | `  * **conditions**: if the bug depends on certain configuration options,` |
| 8 | S071.txt:95-96 | 16 | `**If you resorted to AI assistance to identify a bug, you must treat it as` / `public**. While you may have valid reasons…` |
| 9 | S071.txt:99 | 12 | `case, do not publicly share a reproducer, as this could cause unintended harm;` |
| 10 | S071.txt:310-311 | 21 | `the reporter or an affected party for up to 7 calendar days from the start` / `of the release process, with an exceptional extension to 14 calendar days` |
| 11 | S071.txt:312-314 | 22 | `if it is agreed that the criticality of the bug requires more time.  The` / `only valid reason for deferring the publication of a fix is to accommodate` / `the logistics of QA and large scale rollouts which require release` |
| 12 | S071.txt:21 | 4 | `will not be processed.  Note that a time-dependent version such as "latest` (used in Overlap item 1) |
| 13 | S071.txt:305 | 11 | `Once a robust fix has been developed, the release process starts.  Fixes` (Overlap item 3) |
| 14 | S071.txt:340 | 8 | `Please note that the respective policies and rules are different since` (Limits) |

Plain (non-quoted) line citations also checked: S071.txt:37-39 (example reproducer forms), 22-23 (stable identifier), 239-242 (AI MUST list and the four items at 242), 343-344 and 350 (linux-distros coordination; the start-rule sentence at 343-344, the "UNTIL" sentence at 350). Both 343-344 and 345-346 were read with `sed` before use; an earlier unverified read of this block was off by one line and is not relied on.

Quote words: max 22 (limit 25). G5 found zero failed spans.

## 4. Discrimination controls (G5 on the scratch tree)

- Control A, mutated quote (word "Binary-only" → "Binary"): `G5 pass=0 read=spans=15 located=14 failed=1 cores=3/4`. G5 detects a one-word change inside a located quote.
- Control B, do-nothing (empty entry file): `G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4`.
- Restored draft: `G5 pass=1 read=spans=15 located=15 failed=0 cores=4/4`.

## 5. Overlap and novelty evidence

Opened and read (corpus/knowledge):
- F02 `coordinated-disclosure-timelines.md`: Rule lines 7-17 (line 17: "Do not transplant CERT/CC or Project Zero intervals into another policy record"); evidence line 25 (Project Zero 14-day grace, conditional on a developer commitment).
- F04 `ai-assisted-finding-validation.md`: Rule lines 7-8 (candidate until reproducible observation and a reviewer distinct from the producer).
- F15 `vendor-third-party-finding-coordination.md`; README row line 309: "Record which party coordinates a multi-vendor finding".

Novelty greps over `corpus/knowledge/*.md` (run by me, read-only):
```
linux-distros        -> (no file)
get_maintainer       -> (no file)
security@kernel      -> (no file)
Binary-only          -> (no file)
7 calendar           -> (no file)
release process      -> (no file)
Reported-by          -> (no file)
kernel.org           -> (no file)
Fixes:               -> corpus/knowledge/claim-package-gate.md, corpus/knowledge/retirement-autopsies.md (unrelated to kernel rules)
reporter             -> 8 files (generic usage; not the kernel rule)
```

New in F27, as the draft states it: (1) the kernel's mandatory-field intake contract with a rejection clause; (2) the AI-assisted report duties (public treatment, reproducer withheld, MUST list); (3) the 7/14-day ceiling as an upstream-maintainer rule, triggered at release-process start (S071.txt:305, 310-311). The 14-day figure also appears in F02, but there it is Project Zero's grace extension with a different condition; the draft says so and does not transplant it.

## 6. Discrepancies and open items for L1 (not fixed by me; shared files untouched)

1. `corpus/README.md` has no F27 row: `grep -c "^| F27 |" corpus/README.md` → `0`. G1 cannot pass until the row admits F27 with the entry path `knowledge/linux-kernel-security-bugs-reporting-process.md`.
2. `corpus/SOURCES.md` has no S071 row: `grep -n S071 corpus/SOURCES.md` → no output. G3 needs an 11-cell tier-A `mined` row (opened 2026-10-28, sha256 `0918dcfa…f40`, used-by path).
3. Knowledge count: `ls corpus/knowledge/*.md | wc -l` → `63`. G6 expects 64; the entry supplies the 64th. G7 (`sources-census.sh validate`) not run.
4. Version label: the round brief describes the page as "versioned 7.3.0 at capture". `grep -n "7\.3" corpus/source-snapshots/round-45/S071.txt` → no output (exit 1); the same grep over the round-45 directory, `claims.json` and `freeze.txt` also finds nothing. The draft's Limits section records no page version and does not rely on the label. L1 should confirm or drop the label.
5. Capture form: the manifest's `capture_url` is `docs.kernel.org/_sources/process/security-bugs.rst.txt` (RST), while the required source line names the rendered HTML URL. The draft says so in Limits.
6. Citation shape: G5's regex needs an opening parenthesis between the closing curly quote and the backticked citation. The draft uses `“…” (`S071.txt:N`)`, as the house template does. A bare `“…” `S071.txt:N`` would not be counted.

## 7. Limitations

- Checked against the pinned RST capture only, not the live page (no network fetch; the capture is the frozen evidence).
- Gate G1, G3, G6, G7 not exercised on any tree; only G2, G4, G5 were, with the entry path pinned.
- No live target contact, no submission, no reporting or testing against any target; documentation only.
- Novelty claim is limited to the knowledge files in this lane's `corpus/knowledge` at the time of the grep, against the terms listed.
