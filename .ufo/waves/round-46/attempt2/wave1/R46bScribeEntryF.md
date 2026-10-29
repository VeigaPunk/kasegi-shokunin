VERDICT: DRAFT-READY

# R46bScribeEntryF — C2 (F29) knowledge-entry drafter, round 46 attempt 2

Seat scope: draft the F29 entry only. Nothing else in the lane was written: no `corpus/` file,
no `corpus/README.md`, no `corpus/SOURCES.md`, no counter, no git/jj mutation. The only writes in
the lane are my draft directory and this Report.

## 1. What was built

Draft entry (my own draft dir, ready for L1 integration at
`corpus/knowledge/github-repository-security-advisories.md`):

- `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/github-repository-security-advisories.md`
  — 11668 bytes, 0 ASCII double quotes, 33 curly-quote pairs (all 33 immediately followed by a
  `(`S074.txt:N`)` citation), 1 `recheck:` line, exactly the four required sections
  (`## Scope and decision rule`, `## Overlap and novelty`, `## Limits`,
  `## Falsifiable package rule`), one `| id | observed question | ground |` table with 9 data rows
  (G1..G9).

Header, lines 1-5 (verified by script, output in §3.5):

```
# GitHub repository security advisories: the maintainer-side advisory lifecycle

source: S074 — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories — section anchors: About repository security advisories (S074.txt:9-21); CVE identification numbers (S074.txt:22-27); Publication of security advisories (S074.txt:28-34); Dependabot alerts for published security advisories (S074.txt:35-36); Importance of fix versions (S074.txt:37-42)
verified-at: 2026-10-29
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074 # 90d
```

Source read for the draft (no other draft was read; the two sibling entry drafts were not opened):
`corpus/source-snapshots/round-46-a2/S074.txt` (42 lines, whole capture is body) and, as house
shape only, `corpus/knowledge/github-private-vulnerability-reporting.md` (F28).

## 2. Coverage of the mandated C2 claims

All nine mandated statements are inside located quotes, at the mandated source lines
(script output, §3.5 `required:` lines):

| mandated item | quote anchor | entry location |
|---|---|---|
| private discuss-and-fix definition | `S074.txt:10` | Scope prose + row G1 |
| temporary private fork | `S074.txt:13` | Scope prose + row G2 + falsifiable rule (2) |
| credit | `S074.txt:17` | Scope prose + row G3 |
| GitHub as CNA | `S074.txt:24` | Scope prose + row G4 + falsifiable rule (3) |
| 72-hour review clock | `S074.txt:25` | Scope prose + row G5 |
| requesting does not publish | `S074.txt:25` | Scope prose + row G6 + falsifiable rule (3) |
| other-CNA boundary | `S074.txt:26` | Scope prose + row G7 + falsifiable rule (4) |
| publication visibility | `S074.txt:31` | Scope prose + row G8 |
| fix-version duty | `S074.txt:38` | Scope prose + row G9 + falsifiable rule (4) |

Decision rule stated in the entry (L1 can act on it): draft before publish, fix version before
publish, CVE request while private — with the consequence that a package claiming a published
advisory with no fix version, or treating a CVE request as publication, fails the rule.
`## Limits` names the overview page's own gaps: the advisory form's fields
(`S074.txt:23`, sibling page `S074.txt:17`), the editing flow (`S074.txt:34`), the REST API
(`S074.txt:16`) and the Advisory Database edit flow (`S074.txt:19`) are sibling pages the capture
names but does not hold.
`## Overlap and novelty` contrasts F28 (`corpus/knowledge/github-private-vulnerability-reporting.md:9-13`,
`:15-24` — actor: reporter, stage: intake) with this entry (actor: maintainer, stage: handling
after intake) as a contrast of coverage, and F07
(`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:9-13`, `:30-38` — programme-level CNA
assignment scope) with the platform's per-advisory request. Both file line ranges were checked
against the files on disk (F28 has 49 lines, F07 has 80 lines).

## 3. Evidence (commands I ran, and their printed output)

### 3.1 Scratch tree, built read-only from the freeze commit

```
S=/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryF
mkdir -p "$S/tree" "$S/work"; export TMPDIR="$S/work"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 corpus | tar -x -C "$S/tree"
```

### 3.2 Control A — the same tree WITHOUT my entry (do-nothing control)

```
$ python3 corpus/instruments/r46-f29-gate.py --root "$S/tree" --work "$S/work"
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=2/7 exit=1
```

### 3.3 My entry installed in the scratch tree, lane corpus rows untouched

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=9 xrefs=4/4 anchored=1
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=33 located=33 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=5/7 exit=1
```

H1 and H3 are red here because the lane's `corpus/README.md` has 28 frontier rows and no F29 row,
and `corpus/SOURCES.md` has no S074 row. Those two rows are L1 integration work, not this seat's
scope (both files are read-only for me), so I did not add them to the lane.

### 3.4 Integration rehearsal (scratch only): my entry + L1-style rows → 7/7

To show the entry composes to a green gate, I added an F29 frontier row to the scratch copy of
`corpus/README.md` and an S074 registry row to the scratch copy of `corpus/SOURCES.md` (scratch
copies only; the lane's files were not touched):

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=9 xrefs=4/4 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=33 located=33 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=1
```

Do-nothing control on that same composed tree, with the entry removed:

```
gate H1 pass=0 read=F29-row-or-entry-missing entry-absent advisor-named=
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=bad=used-by
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=0 read=census-rc=1 ok-line=0
f29-gate fixed=1/7 exit=1
```

The two rows I used (for L1 to reproduce verbatim if useful) are in the receipts'
`gate-composed.txt` context and in the scratch tree; their shape satisfies H1 (`F29 | … |
admitted | `corpus/knowledge/github-repository-security-advisories.md` | S074 | …`) and H3 (11
cells, kind `docs`, tier `A`, status `mined`, opened `2026-10-29`, recheck `90d`, anchor cell
carrying `corpus/source-snapshots/round-46-a2/S074.txt`, `sha256
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039` and the locator `lines 1-42`,
used-by `corpus/knowledge/github-repository-security-advisories.md`). They are my rehearsal rows,
not lane rows.

### 3.5 Per-quote self-check (every quote re-located against the pinned capture)

Script (`$S/quotecheck.py`, scratch) re-implements the gate's locator (whitespace/markup
normalisation) and prints, for each quoted span, the `sed -n 'Np'` line it was verified against;
receipt `receipts/quotecheck.txt` has all 33 spans. Summary line:

```
SPANS=33 LOCATED=33
```

Excerpt (verbatim from the receipt):

```
QUOTE[10..10] words=19 located=True :: Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.
   sed -n '10p' S074.txt
     Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to 
   (receipt line truncated at 230 characters by the checker; the full line is `sed -n '10p' corpus/source-snapshots/round-46-a2/S074.txt`)
QUOTE[24..24] words=15 located=True :: GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.
   sed -n '24p' S074.txt
     GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website.
QUOTE[38..38] words=15 located=True :: you should add a fix version to a security advisory prior to publishing the advisory
   sed -n '38p' S074.txt
     Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, w
   (receipt line truncated at 230 characters by the checker; the full line is `sed -n '38p' corpus/source-snapshots/round-46-a2/S074.txt`)
```

Structure check on the draft file itself:

```
line1: '# GitHub repository security advisories: the maintainer-side advisory lifecycle'
line2 empty: True
line3 ok: True
line4: 'verified-at: 2026-10-29'
line5: 'recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074 # 90d'
recheck-lines: 1
bytes: 11668
## Scope and decision rule count: 1
## Overlap and novelty count: 1
## Limits count: 1
## Falsifiable package rule count: 1
ascii-double-quote count: 0
curly-single: 0 0
curly-double: 33 33
xrefs: ['corpus/knowledge/github-private-vulnerability-reporting.md:9-13', 'corpus/knowledge/github-private-vulnerability-reporting.md:15-24', 'corpus/knowledge/cna-assignment-and-vulnerability-rules.md:9-13', 'corpus/knowledge/cna-assignment-and-vulnerability-rules.md:30-38']
table rows: 9
required: 10 privately discuss and fix a security vulnerab -> [(10, 10), (10, 10)]
required: 13 temporary private fork -> [(13, 13), (13, 13), (13, 13)]
required: 17 give credit to individuals -> [(17, 17), (17, 17)]
required: 24 authorized to assign CVE identification numbe -> [(24, 24), (24, 24), (24, 24)]
required: 25 reviews the request within 72 hours -> [(25, 25), (25, 25)]
required: 25.5 doesn't make your security advisory public -> [(25, 25), (25, 25), (25, 25)]
required: 26 covered by another CNA -> [(26, 26), (26, 26)]
required: 31 Anyone can see the current version of the adv -> [(31, 31), (31, 31)]
required: 38 add a fix version to a security advisory prio -> [(38, 38), (38, 38), (38, 38)]
```

### 3.6 Mutants of my own entry (each must go red)

Receipt `receipts/mutants.txt`:

- mut1 — the 72-hour clock reworded to "one business day", citation kept:
  `gate H5 pass=0 read=spans=33 located=31 failed=2 uncited=0 cores=4/5` → `f29-gate fixed=6/7 exit=1`
- mut2 — one citation dropped after the credit quote:
  `gate H5 pass=0 read=spans=31 located=31 failed=0 uncited=2 cores=5/5` → `f29-gate fixed=6/7 exit=1`
- mut3 — the whole `## Limits` section deleted:
  `gate H2 pass=0 read=source=1 verified-at=1 recheck=1 sections=3/4 full=3/4 table-rows=9 xrefs=4/4 anchored=0` → `f29-gate fixed=6/7 exit=1`
- restored good entry: `f29-gate fixed=7/7 exit=0`
- the wave's own fixture controls, built by `.ufo/waves/round-46/attempt2/controls/f29-fixture.py`:
  `--mode junk` → `f29-gate fixed=6/7 exit=1`; `--mode fabricated` → `f29-gate fixed=6/7 exit=1`

### 3.7 Source recheck of the pinned capture

H4's own run is the recheck: `recheck-rc=0 quotes-ok=9 frozen-cores-missing=0`, i.e.
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074`
exits 0 against the pinned manifest and all nine pinned S074 quotes verify.

## 4. Tooling

No tool was installed or upgraded. The draft, the checks and the scratch tree used only python3
(stdlib) and coreutils already on the host; the pacman guard was not touched. Reason recorded for
the record: the task needed no new binary.

## 5. Limitations

- This seat delivers a draft only. The lane corpus is unchanged: the F29 frontier row
  (`corpus/README.md`) and the S074 registry row (`corpus/SOURCES.md`) do not exist yet, so the
  lane as it stands reads `f29-gate fixed=5/7` with my entry present (§3.3) — H1 and H3 stay red
  until L1 adds those two rows. My 7/7 reading in §3.4 is a scratch rehearsal with my own
  rehearsal rows, not a lane state.
- Quote verification is against the pinned capture `corpus/source-snapshots/round-46-a2/S074.txt`
  (sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`), never against the
  live GitHub page; no network fetch was made, and live-target testing is out of scope.
- The capture is one overview page (42 lines, whole capture is body). It does not hold the
  advisory form's field list, the editing flow, the REST API shapes or the Advisory Database edit
  flow; the entry says so in `## Limits` and does not quote them.
- The entry is documentation only: it prescribes no advisory creation, no CVE request, no
  contact with any maintainer and no probing of any repository.
- The `recheck:` cadence `90d` is the claim's cadence, copied from the seat spec; the capture
  itself carries no cadence.
- Two separate 72-hour clocks exist on the page (CVE-request review at `S074.txt:25`,
  Dependabot-alert processing at `S074.txt:36`). The entry keeps them apart, quoting each where it
  is used; a package must not merge them.
- I did not read the sibling entry drafts (E/A/C/D or any other seat's draft), per the seat card;
  the entry's wording is my own, derived from S074 and the F28 house shape only.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryF` was removed after the receipts were
  copied into my draft directory.

## 6. Artefacts

- Draft entry: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/github-repository-security-advisories.md`
- Receipts: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/receipts/gate-composed.txt`,
  `gate-no-entry.txt`, `gate-no-entry-rows.txt`, `mutants.txt`, `quotecheck.txt`
- This report: `.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.md`

Report: .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.md
