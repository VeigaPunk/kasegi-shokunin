VERDICT: HOLDS

# R46bScoutAbsence — F29 admission absence sweep (round-46 attempt-2)

Scope: search-log evidence only. No edits outside this Report file and scratch `/fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence/` (removed after receipts; nothing under /tmp is cited).

## Finding 1 — Base-export absence sweep (attacked: does the frozen base already hold F29?)

Built the base export exactly per spec, then ran the prescribed sweep verbatim:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C /fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence
ARCHIVE_OK

$ grep -rliE 'repository securit. advisor|GHSA' /fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence/corpus/knowledge /fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence/corpus/SOURCES.md /fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence/corpus/README.md
/fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence/corpus/knowledge/github-private-vulnerability-reporting.md
/fast/scratch/hyaku/kasegi-r46/R46bScoutAbsence/corpus/SOURCES.md
EXIT=0
```

README.md is not in the hit list; explicitly: `grep -ciE 'repository securit. advisor|GHSA' <base>/corpus/README.md` printed `0` (exit 1). Line-level (`grep -rniE`, same pattern and paths), 4 hits in 2 files:

1. `corpus/knowledge/github-private-vulnerability-reporting.md:40` — the F28 entry's scope-out note: "The page does not state the maintainer-side flow, CVE requests, timelines or rewards. … The page's pointers forward are link text only: 'Configuring private vulnerability reporting for a repository' (`S073.txt:561`), **'Creating a repository security advisory' (`S073.txt:563`)**, 'Coordinated disclosure of security vulnerabilities' (`S073.txt:566`) and 'Managing privately reported security vulnerabilities' (`S073.txt:579`) … none of those pages is in the capture."
2. `corpus/knowledge/github-private-vulnerability-reporting.md:43` — same entry, "Four linked pages appear only as link text in the capture, and their bodies are not recorded here: … 'Creating a repository security advisory' (`S073.txt:563`) …"
3. `corpus/SOURCES.md:74` — the **S068** row: "GitHub Advisory Database entry GHSA-v676-f8gm-92r9 for CVE-2025-9086 …" status cell `REJECTED: screened out on primary-of-record and record completeness — the page republishes NVD's record of the CVE …`. Round-43 question; a rejected *database mirror* row, not the maintainer-side advisory lifecycle.
4. `corpus/SOURCES.md:157` — the round-43 search-log bullet for the claim-package exemplar ("… GHSA-v6mg-96c6-gmpq … GHSA-v676-f8gm-92r9 lands as the S068 reject …"), a historical hunt note for a different question.

Decomposition vs expectation: the knowledge hit is exactly the F28 entry's scope-out notes (expectation met). The SOURCES.md GHSA-string hits sit on an unrelated rejected row (S068) and a historical log bullet — there is **no SOURCES row and no README line carrying the GitHub maintainer-side repository security advisory lifecycle**. Direct probe: `grep -rn 'S074' corpus/SOURCES.md corpus/README.md` (live lane) printed nothing, exit 1. Filename check `ls corpus/knowledge | grep -iE 'advis|report'` lists only `cra-manufacturer-reporting-duties.md`, `github-private-vulnerability-reporting.md`, `linux-kernel-security-bugs-reporting-process.md`, `pz-reporting-transparency-trial.md` — no advisory-lifecycle entry.

## Finding 2 — Live-lane sweep (attacked: did anything change since freeze?)

```
$ grep -rliE 'repository securit. advisor|GHSA' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-private-vulnerability-reporting.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

Identical file set to the base export; line numbers identical (40, 43, 74, 157). `grep -rn 'S074' corpus/SOURCES.md corpus/README.md` → empty stdout, exit 1. Do-nothing control discrimination: a control that ran nothing has no observable; these runs distinguish absence (S074 probe: no output, exit 1) from presence (base/live sweeps: 2 paths, exit 0), so the prints themselves are the evidence.

## Finding 3 — Adjacent rows held, with scope cells (for the entry's Overlap section)

From base-export `corpus/SOURCES.md` (header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`, line 4):

- **S073** (line 79) — GitHub Docs, Privately reporting a security vulnerability. scope cell: "GitHub's own statement of the reporter-side private-reporting flow only (who may report, the form's default fields, submission and the temporary private fork); **not maintainer handling of a report, the GitHub Advisory Database or CVE assignment**". Contrast: F29 is exactly the maintainer side S073 excludes — and S073.txt:563 links the F29 page as out-of-capture link text.
- **S031** (line 37) — CVE Numbering Authority Operational Rules v4.2.6. scope cell: "CVE Program CNA scope, vulnerability determination and assignment requirements in the current version 4.2.6". Contrast: program-wide CNA rules, not GitHub's product-level advisory lifecycle (draft → collaborate → publish, CVE request, credit).
- **S069** (line 75) — Google Cloud Vulnerability Reward Program Rules. scope cell: "Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule". Contrast: a vendor bug-bounty program's testing boundaries, not repository advisory publication.

## Finding 4 — Draft Search-log bullet (PRISMA-style)

> - F29 admission search (maintainer-side GitHub repository security advisory lifecycle; feeds row S074 and entry `corpus/knowledge/github-repository-security-advisories.md`). Question: does the corpus already hold the maintainer-side advisory lifecycle (create/draft advisory, collaborate, publish, CVE request, credit), in any knowledge entry, SOURCES row, or README admission? Where: `corpus/knowledge/`, `corpus/SOURCES.md`, `corpus/README.md`, searched twice on 2026-10-29 — (a) frozen base `04af9bc92229232ea5cce8b32bfe59dd969eb26d` exported with `git archive … corpus | tar -x`, (b) the live lane. Method: `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md`, plus line-level `-n` re-run and a direct `grep -rn 'S074'` probe. Identified: 2 files (identical in both trees). Screened: 4 line hits. Included: 1 — no existing row/entry covers the maintainer-side lifecycle, so S074 is admitted and the entry is new. Excluded 3: F28 entry scope-out notes (`github-private-vulnerability-reporting.md:40,43` — the lifecycle pages appear only as link text, explicitly outside F28's reporter-side scope); S068 (`SOURCES.md:74` — rejected Advisory-Database mirror of an NVD record, not a maintainer-published advisory); round-43 search-log bullet (`SOURCES.md:157` — historical hunt for the claim-package exemplar, different question). README: 0 matches. Adjacent-held check: S073 reporter-side only, S031 CVE-program CNA rules, S069 Google Cloud VRP — none covers the lifecycle. Stop rationale: hits exhausted with saturation (every hit is either the gap's own note or an unrelated scope); a wider corpus sweep would only re-find the F28 pointer.

## Limitations

- The sweep is the prescribed textual pattern over the three target paths only; `lessons/`, `instruments/`, `source-snapshots/` and non-target corpus files were not swept, so "absent" means absent from knowledge entries, SOURCES and README (the admission-bearing surfaces), not corpus-wide.
- Live-lane state is as of the run time (2026-10-29); a sibling landing a row after my sweep is not reflected.
- I did not open the round-46-a2 snapshot (`corpus/source-snapshots/round-46-a2/S074.txt`) or manifest; capture-quality is F29-gate territory, not the absence question.
- `git archive` reproduces tree content, not commit metadata; provenance rests on the frozen rev id in the command line above.
- No tooling installed or upgraded; no git/jj mutation anywhere; scratch removed after this Report was written.
