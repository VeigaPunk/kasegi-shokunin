VERDICT: DRAFT-READY

# Seat R46bScribeEntryA — C2 entry drafter A (F29, GitHub repository security advisories)

**Deliverable (draft only; the L1 integrates and commits):**
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryA.draft/github-repository-security-advisories.md`
(12798 bytes, 55 lines)

**Draft-dir receipts (committed-with-draft candidates for the L1):**
- `…/R46bScribeEntryA.draft/quote-selfcheck.txt` — every one of the 28 curly-quoted spans with the `sed -n 'Np'` line it was verified against.
- `…/R46bScribeEntryA.draft/gate-receipt.txt` — the `r46-f29-gate.py` output on a scratch tree carrying this entry.

**Target path at L1 integration (not written by me):**
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/github-repository-security-advisories.md`

---

## 1. What was built

The F29 knowledge entry for the maintainer-side GitHub repository-security-advisory lifecycle, written from the pinned capture `corpus/source-snapshots/round-46-a2/S074.txt` (42 lines, sha256 `1296528d…c278039`), read directly by this seat. No sibling entry draft was read (the sibling `.draft/` dirs `R46bScribeEntryB.draft`, `R46bScribeEntryC.draft`, `R46bScribeEntryF.draft` were listed once by `ls` and never opened).

Required shape, all present:
- Line 1 `# <title>`, blank, then `source: S074 — <canonical URL> — <section names>`, `verified-at: 2026-10-29`, `recheck: cd … --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074 # 90d`.
- Sections exactly `## Scope and decision rule`, `## Overlap and novelty`, `## Limits`, `## Falsifiable package rule`.
- A `| id | observed question | ground |` table with 10 rows, ids G1…G10, three cells per row, the ground cell carrying the quote + cite.
- Every quotation is curly double quotes, at most 25 words, immediately followed by ` (`S074.txt:N`)` or ` (`S074.txt:N-M`)`. Longest quote is 20 words.

The nine facts the task named, each inside a located quote:

| required fact | quote | cite |
|---|---|---|
| private discuss-and-fix definition | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” | `S074.txt:10` |
| temporary private fork | “Privately collaborate to fix the vulnerability in a temporary private fork.” | `S074.txt:13` |
| credit | “You can give credit to individuals who contributed to a security advisory.” | `S074.txt:17` |
| GitHub as CNA | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” | `S074.txt:24` |
| 72-hour review clock | “GitHub usually reviews the request within 72 hours.” | `S074.txt:25` |
| requesting does not publish | “Requesting a CVE identification number doesn't make your security advisory public.” | `S074.txt:25` |
| other-CNA boundary | “GitHub cannot assign CVEs to your project if it is covered by another CNA.” | `S074.txt:26` |
| publication visibility | “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” | `S074.txt:31` |
| fix-version duty | “you should add a fix version to a security advisory prior to publishing the advisory” | `S074.txt:38` |

## 2. Gates and commands run (all re-runs I performed)

### 2.1 The entry's own `recheck:` line, run verbatim

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
S074:Q2 OK occurrences=1 anchor=13-ok
S074:Q3 OK occurrences=1 anchor=17-ok
S074:Q4 OK occurrences=1 anchor=24-ok
S074:Q5 OK occurrences=1 anchor=25-ok
S074:Q6 OK occurrences=1 anchor=25-ok
S074:Q7 OK occurrences=1 anchor=26-ok
S074:Q8 OK occurrences=1 anchor=31-ok
S074:Q9 OK occurrences=1 anchor=38-ok
rc=0
```

### 2.2 The mechanical target: `r46-f29-gate.py` on a scratch tree carrying this entry

Scratch tree built with the round's own fixture (`.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive`), then the fixture's synthetic entry replaced by this draft. The lane tree itself was never modified.

```
$ python3 corpus/instruments/r46-f29-gate.py --root $S/tree --work $S/wfinal
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=10 xrefs=6/6 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=28 located=28 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

Baseline for comparison — the same tree with the fixture's own entry, before I substituted mine, so the 7/7 is attributable to the tree and not to my file:

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=9 xrefs=6/6 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=26 located=26 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

### 2.3 Discriminating negative controls (do-nothing / fabricated / broken variants of *my* entry)

Each control is a one-line mutation of this draft substituted into the same tree. Every control kills the gate; none is graded 7/7.

| # | mutation | gate result |
|---|---|---|
| n1 | 72-hour clock paraphrased: `reviews the request within 72 hours` → `reviews the request within one business day` | `gate H5 pass=0 read=spans=28 located=26 failed=2 uncited=0 cores=4/5` → `f29-gate fixed=6/7 exit=1` |
| n2 | an extra curly quote with no cite: `the three actions` → `the three actions “and nothing else at all”` | `gate H5 pass=0 read=spans=28 located=28 failed=0 uncited=1 cores=5/5` → `f29-gate fixed=6/7 exit=1` |
| n3 | `## Overlap and novelty` section deleted (kills the F28/F07 contrasts) | `gate H2 pass=0 read=source=1 verified-at=1 recheck=1 sections=3/4 full=3/4 table-rows=10 xrefs=0/0 anchored=0` → `f29-gate fixed=6/7 exit=1` |
| n4 | table rows G6–G10 deleted (5 rows, below the ≥6 floor) | `gate H2 pass=0 read=… table-rows=5 …` → `f29-gate fixed=6/7 exit=1` |
| n5 | `recheck:` manifest path switched to the attempt-1 manifest `round-46/manifest.json` | `gate H2 pass=0 read=… recheck=0 …` → `f29-gate fixed=6/7 exit=1` |
| n6 | F07 xref `cna-assignment-and-vulnerability-rules.md` swapped for `linux-kernel-security-bugs-reporting-process.md` | `gate H2 pass=0 read=… xrefs=6/6 anchored=1` → `f29-gate fixed=6/7 exit=1` |
| n7 | F07 xref line number pushed out of range (`:36` → `:360`) | `gate H2 pass=0 read=… xrefs=5/6 anchored=1` → `f29-gate fixed=6/7 exit=1` |

n1 is the load-bearing one for C2's kill_rule ("a control that grades 7/7" must not): a fabricated clock is caught by H5 as `failed=2 cores=4/5`.

### 2.4 Per-quote `sed -n 'Np'` self-check

Full transcript in `…/R46bScribeEntryA.draft/quote-selfcheck.txt` (202 lines). Summary line:

```
total quoted spans: 28 ; max words per quote: 20 ; contained: 28/28
```

Each of the 28 spans was located by running `sed -n 'Np' corpus/source-snapshots/round-46-a2/S074.txt` and confirming containment; the capture contains 9 ASCII apostrophes and zero curly apostrophes, so the one apostrophe-bearing quote (`doesn't`, `S074.txt:25`) uses the ASCII form the capture itself holds, and no span needed a curly-apostrophe workaround.

Character audit of the entry: 26 → 28 curly double-quoted spans, **0** of them uncited; 0 curly single quotes; 2 ASCII double quotes, both inside a `grep -n -i -E "…"` shell example in Limits (not a quotation). H5 reports `uncited=0`.

### 2.5 Cross-reference line numbers verified against the real files

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sed -n '9p' corpus/knowledge/github-private-vulnerability-reporting.md
This entry records one reporter-side flow: GitHub's documented route for a person who wants to report a security vulnerability privately to a repository's maintainers. …
$ sed -n '13p' corpus/knowledge/github-private-vulnerability-reporting.md
Decision rule: a package may describe a report as submitted through GitHub private vulnerability reporting only when the target repository's enablement is recorded and the submission follows the steps quoted below. …
$ sed -n '9p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md
A local CVE-request package review separates technical vulnerability determination,
$ sed -n '36p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md
| 4.2.1.1 | “The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign.” | An assignment-routing proposal names the appropriate CNA scope and unresolved exceptions. …
$ wc -l corpus/knowledge/github-private-vulnerability-reporting.md corpus/knowledge/cna-assignment-and-vulnerability-rules.md
49 corpus/knowledge/github-private-vulnerability-reporting.md
80 corpus/knowledge/cna-assignment-and-vulnerability-rules.md
```

Both cited ranges are in range (F28 9–13 of 49; F07 9–13 and 36 of 80).

## 3. Covered surfaces

- **Scope and decision rule** — a maintainer-actionable rule, not a restatement: draft while private, request the CVE while private, fix version before publish; with the failure modes named (describing a CVE request as the publication event; publishing with no fix version while implying a safe upgrade; claiming a GitHub assignment for a project covered by another CNA).
- **Table G1–G10** — ten observed questions, each with a located ground.
- **Overlap and novelty** — F28 contrasted on actor and lifecycle stage and explicitly framed as a *contrast of coverage*, not of policy (F28 = reporter/intake; this = maintainer/draft-to-publication); F07 contrasted on program assignment scope vs the platform's per-advisory request.
- **Limits** — overview page only; form fields (`S074.txt:23` standardisation stated, fields not held), editing flow (`S074.txt:34`), REST API (`S074.txt:16`), Advisory Database edit flow (`S074.txt:19`) named as sibling pages the capture names but does not hold; the two distinct 72-hour clocks kept apart (`S074.txt:25` CVE review vs `S074.txt:36` Dependabot); documentation-only scope.
- **Falsifiable package rule** — seven numbered conditions, each with a cite.

## 4. Out-of-scope items (not touched by this seat)

- The committed entry path `corpus/knowledge/github-repository-security-advisories.md` — L1 integration owns it.
- `corpus/README.md` F29 row, `corpus/SOURCES.md` S074 row, `considerthese-proposals-ledger.md` disposition — L1 integration owns them (the scratch tree used the fixture's synthetic rows for H1/H3/H7).
- The committed counters `r46-c1-gate.py`, `r46-c2-gate.py`, `r46-f29-gate.py`, the manifest and the capture — read-only throughout; bytes unchanged (`git status --porcelain` in the lane shows only the pre-existing untracked wave files plus my draft dir).
- C1 (the counter-mutation claim) — out of this seat's scope.
- No git/jj mutation, no commit, no push, no network fetch, no live-target testing. The GitHub Docs page was never opened live; everything is read from the pinned capture.

## 5. Findings and caveats

1. **The `S074.txt:25` admin-permission sentence is a tenth located fact the task list did not name.** A sweep over the body (`grep -n -i -E "required|must|permission|role|owner|deadline|escalat" corpus/source-snapshots/round-46-a2/S074.txt`) printed exactly one matching capture line, 25, whose only match is “Anyone with admin permissions to a security advisory can request a CVE identification number.” I added it as G10 and in the Scope prose. This is strictly additive coverage, not a substitution: the nine required facts are each still carried by their own located quote.
2. **The two 72-hour clocks must not be conflated.** `S074.txt:25` is the CVE-request review; `S074.txt:36` is the Dependabot publication process. The entry keeps them in separate sections and says so explicitly in Limits.
3. **A first draft of mine failed the H5 "uncited" limb.** An early version quoted F28's own opening sentence inside a curly pair. The gate counts any curly-quoted span without a trailing `S074.txt:N` as uncited (`uncited=1`), so the F28 comparison is now stated in my own words with a `corpus/knowledge/…md:N` locator instead. Control n2 reproduces this failure on demand.
4. **The Limits sweep claim was corrected, not asserted.** My first draft said the sweep "printed only the lines quoted elsewhere in this entry"; it actually printed line 25, whose permission sentence was then *not* quoted anywhere. The Limits bullet now states the exact output (one capture line, 25) and the sweep is re-runnable verbatim.
5. **`S074.txt` has no curly apostrophes** (9 ASCII `'`, 0 curly). The one apostrophe-bearing quote (`doesn't`) therefore reproduces the capture's own ASCII form rather than a typographic one — the manifest's own Q6 holds it the same way.
6. **The entry quotes only what the capture holds.** Every one of the 28 spans is a contiguous substring of the cited capture line(s); no quote was stitched across lines or paraphrased inside quotation marks. Control n1 confirms a paraphrase inside quotation marks is caught.

## 6. Limitations

- **Documentation only — no live verification.** The GitHub Docs page was never re-opened; the non-author closure re-opening the page remains the L1's check under C2's kill_rule. My 7/7 is a mechanical, capture-local result.
- **The 7/7 was measured on a fixture-built scratch tree, not on the lane tree.** The lane tree at the freeze tip reads `f29-gate fixed=2/7 exit=1` because the entry, the F29 README row and the S074 SOURCES row do not exist there yet — those are the L1's integration artifacts. My scratch tree supplied them via `.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive`, so H1/H3/H7 in my receipt reflect the fixture's synthetic rows, not rows I authored.
- **H6's `base-intact=1` therefore attests to the fixture's copy of the 65 pre-existing knowledge entries**, not to a tree that already contains my entry at the committed path.
- **My scratch tree was not a git checkout** — it was assembled by the fixture from the live lane's `corpus/` files. It is therefore not evidence about any commit.
- **The entry has no live-observed fields or timings beyond the page.** The page gives no required-field list, no role model, no deadline and no escalation path for the CVE request; the entry says so rather than filling the gap.
- **Not verified by me:** the census result on the L1's eventual `corpus/SOURCES.md`, the H1 frontier-row text the L1 will write, the ledger disposition, and the C1 counter-mutation claim. None is in this seat's scope.
- Scratch (`/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryA/`) was removed before this report was written; the receipts cited above live in the draft directory, which is durable.

## 7. Tooling

No tool was installed or upgraded for this seat; `/home/vgpnk/.omp/agent/RULES.md` was read and the pacman guard observed (no pacman transaction attempted). Only the Python 3 standard library and `bash`/`grep`/`sed`/`git status`/`git log` (read-only) were used.
