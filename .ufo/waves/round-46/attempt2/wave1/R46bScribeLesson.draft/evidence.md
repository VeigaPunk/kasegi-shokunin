# Evidence transcript — seat R46bScribeLesson (round 46 attempt 2, kasegi lane)

Every command below was run by this seat on 2026-10-29 against the lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only) and a scratch tree under
`/fast/scratch/hyaku/kasegi-r46/R46bScribeLesson/` (`TMPDIR` passed explicitly as
`/fast/scratch/hyaku/kasegi-r46/R46bScribeLesson/tmp`). No commit, no push, no mutating git/jj call;
no file outside the seat's draft directory and its Report file was written. The scratch tree was removed
after the receipts were copied here.

---

## E1 — S074 capture and manifest digests

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46-a2
$ sha256sum S074.txt
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  S074.txt
$ wc -l S074.txt ; wc -c S074.txt
42 S074.txt
7087 S074.txt
```

Matches `freeze.txt` (`S074-sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`)
and the claim's `after` text (42 lines). The manifest digest was not recomputed here beyond the gate's own
pin check (H4 prints `recheck-rc=0 quotes-ok=9 frozen-cores-missing=0`, and the gate compares the manifest
bytes against `PINS["manifest.json"] = 46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`).

## E2 — the nine quotes located on their anchor lines (sed)

```
$ sed -n '10p'  S074.txt
Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project. After collaborating on a fix, repository maintainers can publish the security advisory to publicly disclose the security vulnerability to the project's community. …
$ sed -n '13p'  S074.txt
Privately collaborate to fix the vulnerability in a temporary private fork.
$ sed -n '17p'  S074.txt
You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory.
$ sed -n '24p'  S074.txt
GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. …
$ sed -n '25p'  S074.txt
When you create a security advisory for a public repository on GitHub, … GitHub usually reviews the request within 72 hours. Requesting a CVE identification number doesn't make your security advisory public. …
$ sed -n '26p'  S074.txt
If you already have a CVE you want to use, … GitHub cannot assign CVEs to your project if it is covered by another CNA.
$ sed -n '31p'  S074.txt
Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.
$ sed -n '38p'  S074.txt
Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to.
```

Substring / word-count check of the manifest's own quote records against those anchor lines:

```
Q1 anchor=10 substring=True words=19 <=25=True
Q2 anchor=13 substring=True words=11 <=25=True
Q3 anchor=17 substring=True words=12 <=25=True
Q4 anchor=24 substring=True words=15 <=25=True
Q5 anchor=25 substring=True words=8 <=25=True
Q6 anchor=25 substring=True words=11 <=25=True
Q7 anchor=26 substring=True words=14 <=25=True
Q8 anchor=31 substring=True words=22 <=25=True
Q9 anchor=38 substring=True words=15 <=25=True
```

## E3 — the recheck command and the frozen cores

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
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
RC=0
```

Frozen-core coverage over the manifest's quote text (the gate's H4 rule):

```
quotes=9 distinct=9 distinct_anchors=8
CORE OK   privately discuss and fix a security vulnerability -> ['Q1@10']
CORE OK   temporary private fork -> ['Q2@13']
CORE OK   authorized to assign CVE identification numbers -> ['Q4@24']
CORE OK   reviews the request within 72 hours -> ['Q5@25']
CORE OK   add a fix version to a security advisory prior to publishing -> ['Q9@38']
```

## E4 — counter lineage (base vs freeze)

```
$ git diff --stat 04af9bc92229232ea5cce8b32bfe59dd969eb26d fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 -- \
    corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py \
    corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py \
    corpus/instruments/r46-mutbat.py corpus/instruments/r46-f29-gate.py
 corpus/instruments/r46-f29-gate.py | 367 +++++++++++++++++++++++++++++++++++++
 corpus/instruments/r46-mutbat.py   | 184 +++++++++++++++++++
 2 files changed, 551 insertions(+)

r46-c1-gate.py            base=95f2eb7933841d6c freeze=95f2eb7933841d6c same=yes
r46-c2-gate.py            base=647bd5b7b6268551 freeze=647bd5b7b6268551 same=yes
r46-counters-selftest-c1.py base=8b17164aadbd9c69 freeze=8b17164aadbd9c69 same=yes
r46-counters-selftest-c2.py base=ff7104cfc8910071 freeze=ff7104cfc8910071 same=yes
r46-mutbat.py             base=e3b0c44298fc1c14 freeze=f7a7cdfa187ef6f2 same=NO   (absent at base)
r46-f29-gate.py           base=e3b0c44298fc1c14 freeze=a1091e246a51c1c1 same=NO   (absent at base)
```

(`e3b0c44298fc1c14…` is the sha256 of an empty blob — the file does not exist at the base.)
The freeze digests match `freeze.txt` (`mutbat-sha256-v1 f7a7cdfa…`, `f29-gate-sha256-v1 a1091e24…`).
The two counters are v1.2 (their docstring line 2 reads "v1.2 (hardened after the wave-1 and wave-2
falsification; errata E1 and E2, see .ufo/waves/round-46/counter-errata.md)").

## E5 — frozen receipts re-read (sha256 and contents)

```
$ sha256sum .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd  .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
```

(matches `freeze.txt`: `controls/mutbat-before.txt (sha256 13c21fcd…)`; the receipt ends with
`mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0`,
`mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0`, `BATEXIT=1`.)

`controls/selftest-baselines.txt`:

```
# selftest baselines at base 04af9bc9 (live tree == base bytes for these instruments), run 2026-10-29
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
c1-exit=0
selftest cases=137 failures=0
c2-exit=0
```

`controls/sources-census-before.txt`:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

## E6 — the admission gate, three trees (do-nothing controls vs the draft rows)

Base export `04af9bc9`:

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1
```

Freeze export `fe0f56b7` (do-nothing control — the capture and manifest are committed, nothing else):

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=2/7 exit=1
```

Freeze export + the two draft rows (F29 in `corpus/README.md`, S074 in `corpus/SOURCES.md`) and a stub
entry file (the gate's H3 limb requires the `used-by` entry to exist):

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 full=0/4 table-rows=0 xrefs=0/0 anchored=0
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=0 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=4/7 exit=1
```

Intermediate state (freeze tree + the draft S074 row only — no F29 row, no entry file):

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=bad=used-by
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=0 read=census-rc=1 ok-line=0
f29-gate fixed=1/7 exit=1
```

and the census's own words on that tree:

```
file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
   (exit 1)
```

## E7 — registry and README diffs (additive only)

```
$ diff <(git show 04af9bc92229232ea5cce8b32bfe59dd969eb26d:corpus/SOURCES.md) "$S/SOURCES.new.md"
79a80
> | S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's ...
added lines (grep -c '^>') = 1
removed lines (grep -c '^<') = 0

$ diff <(git show 04af9bc92229232ea5cce8b32bfe59dd969eb26d:corpus/README.md) "$S/README.new.md"
668a669,674
>
> ## Round-46 (attempt 2) admission — Frontier F29 (appended 2026-10-29)
>
> | id | topic | status | entry | sources | next |
> |---|---|---|---|---|---|
> | F29 | GitHub repository security advisories, maintainer flow: private discussion and fix of a vulnerability, the tem...
```

## E8 — base counts (freeze export, which equals the base for these files)

```
frontier rows: 28
SOURCES rows: 73
knowledge entries: 65
absence sweep:
corpus/knowledge/github-private-vulnerability-reporting.md
corpus/SOURCES.md
count: 2
```

## E9 — capture binding

At the tip (S074 capture committed, row not yet landed):

```
$ python3 corpus/instruments/capture-binding-check.py --root .
MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
FAIL rule=no-row record=S074 dir=round-46-a2
records=61 bound=60 unbound=1
```

With the draft S074 row and its entry present in the tree:

```
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
records=61 bound=61 unbound=0
```

## E10 — the attempt-2 claims file has no candidates list

```
$ grep -n -i 'candidat' .ufo/waves/round-46/attempt2/claims.json
(no output)
```

`python3 -c "import json;print(list(json.load(open('.../claims.json'))))"` →
`['schema', 'lane', 'round', 'attempt', 'author', 'base', 'note', 'claims', 'sourced_claim', 'frontier_step']`.
The reject/flip candidates in `gate-block.md` are therefore reconstructed from the lane's own corpus
evidence (README rows F07/F28, SOURCES rows S068/S073) and from attempt 1's `## Gate` section — stated
in the draft as a deviation, not presented as a quotation from the claims file.
