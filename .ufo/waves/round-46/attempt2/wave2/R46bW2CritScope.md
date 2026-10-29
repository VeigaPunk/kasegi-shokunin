VERDICT: BROKEN

## Finding 1 — F29's package rule weakens the F07/CNA boundary

**Artifact attacked:** `corpus/knowledge/github-repository-security-advisories.md:121-139` (especially item 3); related boundary at `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36`.

**Counterexample:** A public-repository project is covered by another, most-appropriate-scope CNA, but that CNA has not assigned an identifier yet. It therefore does not yet “use[] another numbering authority's identifier.” A package can record a private GitHub CVE request and GitHub's general CNA authority while item 3's stated conditional is false. But F07 requires the most-appropriate-scope CNA to receive the first opportunity, and S074 says GitHub cannot assign when another CNA covers the project. This is a false-pass recipe at the exact F29/F07 seam.

**Evidence (local reads):**
- `read corpus/knowledge/github-repository-security-advisories.md:121-139` → “if the project uses another numbering authority's identifier” and “GitHub cannot assign CVEs to your project if it is covered by another CNA.”
- `read corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36` → “The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign.”
- `read corpus/source-snapshots/round-46-a2/S074.txt:26` → “GitHub cannot assign CVEs to your project if it is covered by another CNA.”

**Impacted axes:** coverage and authority-boundary clarity. This is a fixable wording/decision-rule defect, not a reason to reject the F29 source or its admission.

**Smallest safe correction:** Trigger the GitHub limitation on the source's actual condition—project coverage by another CNA, not possession of that CNA's identifier—and direct assigner selection/first opportunity back to F07. Do not characterize GitHub as the assigner where that condition bars it.

## Checks that held

- **Province fit:** `PROVINCE.md:3,29-33` defines program rules, scopes and claim packages as core domain; `PROVINCE.md:174` admits the maintainer-side advisory lifecycle. F29 is in-domain.
- **F28 boundary:** `read corpus/knowledge/github-private-vulnerability-reporting.md:39-40` → “The page does not state the maintainer-side flow, CVE requests, timelines or rewards.” F29's overlap section (`github-repository-security-advisories.md:50-61`) assigns intake to F28 and the maintainer lifecycle to F29; no reporter-flow absorption found.
- **Do-nothing control:** Exported base `04af9bc92229232ea5cce8b32bfe59dd969eb26d` with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d PROVINCE.md corpus/README.md corpus/knowledge/github-private-vulnerability-reporting.md corpus/knowledge/cna-assignment-and-vulnerability-rules.md | tar -x -C /fast/scratch/hyaku/kasegi-r46/R46bW2CritScope`; observed `base_F29_in_province=0`, `base_F28=4`, `base_F29_entry=absent`. The specialized search over that base export returned `No matches found` for `F29|github-repository-security-advisories`. Thus this is not a do-nothing tree mistaken for the F29 landing.
- **Live-target boundary:** `read PROVINCE.md:52` → “Live-target testing is refused; this corpus is documentation only.” `read corpus/knowledge/github-repository-security-advisories.md:118-119` → “Documentation only” and no advisory creation, CVE request, maintainer contact or repository probing. No live-target testing or live-page request was made by this seat.

## Limitations

This is the assigned province/scope-boundary audit only. It does not re-run the F29 admission gate, source-recheck, quote battery, or live-page comparison; no claim is made that those checks passed.