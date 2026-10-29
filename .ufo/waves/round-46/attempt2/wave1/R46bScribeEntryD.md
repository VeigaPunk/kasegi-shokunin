VERDICT: DRAFT-READY

# Seat R46bScribeEntryD — C2 (coverage) F29 knowledge entry drafter D, round 46 attempt 2, lane kasegi

## What I built

Exactly one artifact: the F29 knowledge entry draft

    /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.draft/github-repository-security-advisories.md

11255 bytes. Sources read myself and nothing else: `corpus/source-snapshots/round-46-a2/S074.txt`
(42 lines, whole capture is body) and `corpus/knowledge/github-private-vulnerability-reporting.md`
(F28 house shape) plus `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` (F07, for the
contrast). I did not open any sibling entry draft (`R46bScribeEntry{A,B,C,F}.draft/`), per my spec.

The entry carries: the provenance trio on lines 1-4 in the required order and form
(`# <title>`, blank, `source: S074 — <canonical URL> — <section names>`, `verified-at: 2026-10-29`,
`recheck: cd … && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074 # 90d`);
the four exact sections `## Scope and decision rule`, `## Overlap and novelty`, `## Limits`,
`## Falsifiable package rule`; a three-cell table `| id | observed question | ground |` with nine
rows G1..G9; and 33 curly-quoted spans, every one immediately followed by a
` (`S074.txt:N`)` locator.

## Finding 1 — the entry draft satisfies the F29 admission gate at 7/7

Built the positive fixture tree from the wave control
(`.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive --dir $S/tree-pos`), replaced
its entry with my draft, and ran the gate named in the claim:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root $S/tree-pos --work $S/work
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=9 xrefs=4/4 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=33 located=33 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
exit=0
```

H5 is the limb that matters for a drafter: `spans=33 located=33 failed=0 uncited=0 cores=5/5` —
every quoted span re-locates in the pinned capture, no quote is uncited, and all five frozen cores
are carried by live text. H2 confirms the structure (`sections=4/4 full=4/4 table-rows=9 xrefs=4/4
anchored=1`).

## Finding 2 — the gate discriminates against do-nothing and fabricated controls

The same gate on the two wave-provided control trees, unmodified apart from their own entry:

```
$ python3 …/r46-f29-gate.py --root $S/tree-junk --work $S/work-junk
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1

$ python3 …/r46-f29-gate.py --root $S/tree-fab --work $S/work-fab
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```

A marker-only entry with no located quotes (junk) fails H5 with `cores=0/5`; an entry whose
citations are kept but whose quote text the source does not hold (fabricated) fails H5 with
`failed=2 cores=4/5`. My draft is therefore not passing on structure alone: it passes only because
its quotes are real and located.

## Finding 3 — every quote is byte-exact in the pinned capture, and all nine mandated claims are carried by located quotes

Re-located all 33 spans independently of the gate with my own check (same normalisation the gate
uses: curly→straight quotes, markup stripped, whitespace collapsed), and separately checked
**byte-exact** containment with no normalisation at all:

```
spans: 33 byte-exact substrings of capture: 33
```

All 33 are literal substrings of `S074.txt`, so no span was stitched or re-punctuated.

The nine claims the entry must state, each confirmed inside a located quote:

```
PASS private discuss-and-fix definition line=10  quoted_in_located_span=True
PASS temporary private fork           line=13  quoted_in_located_span=True
PASS credit                            line=17  quoted_in_located_span=True
PASS GitHub as CNA                     line=24  quoted_in_located_span=True
PASS 72-hour review clock              line=25  quoted_in_located_span=True
PASS requesting does not publish       line=25  quoted_in_located_span=True
PASS other-CNA boundary                line=26  quoted_in_located_span=True
PASS publication visibility            line=31  quoted_in_located_span=True
PASS fix-version duty                  line=38  quoted_in_located_span=True
```

The capture contains no curly apostrophes (`RSQ 0`, `LSQ 0`; only ASCII `'`), and my quotes use
only ASCII apostrophes, so no span depends on curly-apostrophe normalisation.

## Finding 4 — self-check: the `sed -n 'Np'` line behind each distinct quoted line

```
sed -n '10p' S074.txt -> Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerab
sed -n '12p' S074.txt -> Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project
sed -n '13p' S074.txt -> Privately collaborate to fix the vulnerability in a temporary private fork.
sed -n '14p' S074.txt -> Publish the security advisory to alert your community of the vulnerability once a patch is released.
sed -n '17p' S074.txt -> You can give credit to individuals who contributed to a security advisory. For more information, see Creating a reposito
sed -n '19p' S074.txt -> If you created a security advisory in your repository, the security advisory will stay in your repository. We publish se
sed -n '23p' S074.txt -> GitHub Security Advisories builds upon the foundation of the Common Vulnerabilities and Exposures (CVE) list. The securi
sed -n '24p' S074.txt -> GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, 
sed -n '25p' S074.txt -> When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE 
sed -n '26p' S074.txt -> If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, ad
sed -n '31p' S074.txt -> Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have ac
sed -n '32p' S074.txt -> Collaborators can view the conversation history of the advisory.
sed -n '34p' S074.txt -> If you need to update or correct information in a security advisory that you've published, you can edit the security adv
sed -n '38p' S074.txt -> Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, t
sed -n '42p' S074.txt -> Not planned, be clear about it in the advisory so that your users don't contact you to ask when a fix will be made. In t
```

Distinct cited lines: 10, 12, 13, 14, 17, 19, 23, 24, 25, 26, 31, 32, 34, 38, 42 — 17 distinct
quotes, 33 cited instances, every span ≤ 25 words and every range ≤ 12 lines.

## Finding 5 — the entry's shape metrics

```
## Scope and decision rule       words=773
## Overlap and novelty           words=323
## Limits                        words=311
## Falsifiable package rule       words=327
3-cell table rows (incl header/sep): 11
refs: [('github-private-vulnerability-reporting.md','9','13'), ('github-private-vulnerability-reporting.md','22','23'), ('cna-assignment-and-vulnerability-rules.md','9','13'), ('github-private-vulnerability-reporting.md','9','13')]
bytes: 11255
```

Gate thresholds are ≥ 25 words per section (≥ 12 for the falsifiable rule) and ≥ 6 table rows; every
cross-reference resolves to a real line of a real corpus file, which is what the gate's `xrefs=4/4`
reports. The F28 contrast is stated as a contrast of coverage — F28 holds the reporter actor at the
intake stage, this entry holds the maintainer actor at the draft→publish stage — and the F07
contrast states that F07 holds the CVE-programme assignment scope while this entry holds the
platform's per-advisory request path and its limits.

## Finding 6 — the live recheck line in the entry actually passes

Ran the exact command the entry's `recheck:` line states, against the real lane:

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
exit=0
```

Nine quotes OK, sha256 OK, exit 0.

## Finding 7 — on a real export of the lane, the only red limbs are surfaces that are not mine

Exported the lane's committed tree read-only
(`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive HEAD corpus | tar -x -C $S/real`),
dropped my draft in as `corpus/knowledge/github-repository-security-advisories.md`, and ran the gate:

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

The two red limbs are the two integration surfaces owned by other seats / by L1:
**H1** wants the F29 row in `corpus/README.md` (`rows=28` — the frontier table at HEAD still holds
28 rows, F01..F28) and **H3** wants the S074 row in `corpus/SOURCES.md` (`hits=0` — no S074 row
exists yet). Every limb that depends on the entry's own bytes — H2, H4, H5, H6, H7 — is green on
the real export. H6's `knowledge=66` also confirms the entry lands in the knowledge directory
without disturbing the 65 pinned siblings (`base-intact=1`).

## Findings summary

| # | Attacked / built | Command | Outcome |
|---|---|---|---|
| 1 | Draft entry vs the F29 admission gate | `r46-f29-gate.py --root $S/tree-pos` | `f29-gate fixed=7/7 exit=0` |
| 2 | Do-nothing control (junk entry) | `r46-f29-gate.py --root $S/tree-junk` | `fixed=6/7 exit=1`, H5 `cores=0/5` |
| 2 | Quote-not-in-source control (fabricated) | `r46-f29-gate.py --root $S/tree-fab` | `fixed=6/7 exit=1`, H5 `failed=2 cores=4/5` |
| 3 | Byte-exactness + nine mandated claims | my own locator over the draft and `S074.txt` | `33 byte-exact substrings of capture: 33`; 9/9 PASS |
| 4 | Line-by-line quote provenance | `sed -n 'Np' S074.txt` for each cited line | 15 lines printed above, all matching the quoted text |
| 5 | Entry shape metrics | word/row/ref count over the draft | 773/323/311/327 words, 9 data rows, 4 resolving refs |
| 6 | The entry's own recheck command | `source-recheck.py --manifest …/round-46-a2/manifest.json --source S074` | 9× `OK`, `exit=0` |
| 7 | Entry against a real lane export | `r46-f29-gate.py --root $S/real` | `fixed=5/7`, red only on H1 (README F29 row) and H3 (SOURCES.md S074 row) — both other seats'/L1's surfaces |

## Limitations

- **The draft is not integrated.** I wrote only my own draft directory and this Report, as my seat
  permits. `corpus/knowledge/github-repository-security-advisories.md` does not yet exist in the
  lane; L1 must copy the draft there and commit it. The README F29 row and the SOURCES.md S074 row
  (limbs H1 and H3) are still absent at HEAD and are not my surfaces.
- **The 7/7 run is against the wave's own fixture tree**, which synthesises the README and SOURCES
  rows that do not exist in the lane yet. Finding 7 is the honest lane-level measurement: 5/7, with
  the two reds attributable to the two missing rows and not to the entry's bytes.
- **Documentation only.** This corpus records what GitHub's documentation says. Nothing here was
  tested against GitHub, no advisory was created, no CVE was requested, no repository was touched.
  The `recheck:` line proves the pinned capture's bytes, not the live page.
- **Single page.** The capture is the overview page only. The advisory form's field list, the
  post-publication editing flow, the REST API endpoints and the GitHub Advisory Database edit flow
  are named by the capture but not held by it; the entry's `## Limits` section says so rather than
  filling those gaps.
- **One-sided reading.** I read the capture and the two sibling knowledge entries only. I did not
  read other seats' drafts, the freeze record, or the R50 receipt, so I cannot say whether another
  drafter produced a differently-shaped entry or whether the F29 coverage is claimed elsewhere.
- **No tooling installed or upgraded** for this seat, so the operator's tooling directive records
  nothing: `/home/vgpnk/.omp/agent/RULES.md` was read and no package was installed, downgraded or
  updated. All commands used `python3` from the base system and `git archive` (read-only).

## Artifact paths

- Draft entry: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.draft/github-repository-security-advisories.md`
- Gate receipts (all four runs, verbatim): `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.draft/receipts-gate.txt`
- This report: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.md`
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeEntryD/` removed on exit (receipts copied into
  the draft directory first, as required).
