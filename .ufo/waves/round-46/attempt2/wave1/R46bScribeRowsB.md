VERDICT: DRAFT-READY

# R46bScribeRowsB — C2 registry drafter B (round 46 attempt 2, kasegi)

Seat: C2 registry drafter B (independent of R46bScribeRowsA/C). Scope: draft — nothing applied.
Written: draft `corpus/SOURCES.md` row S074 + `## Registry changes` bullets + `## Search log`
bullet, and the PRISMA-style absence sweep behind them.

Files written by this seat (the only ones):
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/rows.md` (the draft)
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/census-receipts.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/gate-receipts.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/sweep-receipts.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.md` (this report)

Nothing in `corpus/` was edited; the committed counters, the frozen claims file and the committed
`corpus/SOURCES.md` are untouched. No git/jj mutation was run anywhere (only `git archive`,
`git log`, `git status`, `git ls-files`, `git rev-parse`). No tool was installed (nothing needed
installing; the host's `bash`, `gawk`, `python3` and the lane's committed instruments were
sufficient), so there is no tool/version/channel record to report.

## Finding 1 — the S074 row exists in the draft, with 11 cells and no `|` inside any cell

Built: the row for GitHub Docs, Repository security advisories
(https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories),
kind `docs`, tier `A` scoped to the maintainer-side advisory lifecycle only, status `mined`,
opened `2026-10-29`, recheck `90d`, used-by `corpus/knowledge/github-repository-security-advisories.md`.
The full row text is in the draft (`rows.md` §(a)); the anchor cell is
`lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt, sha256
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 (snapshot 42 lines, 7087 bytes;
manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL)`.

Command (scratch copy of the base export with the row inserted after S073; `$S` =
`/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsB`):

```
$ python3 - "$S"  # insert the row line from rows.md after the "| S073 |" line
cells: 11
kind: 'docs' tier: 'A' status: 'mined' opened: '2026-10-29' recheck: '90d'
scope words: 57
teaches words: 39
anchor has S074.txt: True | has sha: True
locator: lines 1-42
first url: https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
pipe inside any cell: False
used-by: corpus/knowledge/github-repository-security-advisories.md
```

## Finding 2 — the drafted row passes the F29 admission gate's row limb (H3)

Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root $S/gate`
(the tree carries this draft's row, the committed `round-46-a2` capture and a placeholder entry):

```
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 full=0/4 table-rows=0 xrefs=0/0 anchored=0
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=0 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=3/7 exit=1
```

H3 is the limb that grades the S074 registry row (`11 cells`, kind `docs`, tier `A`, scope ≥ 8
words, teaches ≥ 8 words, recheck cell, anchor locator inside the 42-line capture, anchor sha256,
status `mined`, opened `2026-10-29`, row URL equal to the capture URL, used-by path). H1/H2/H5/H6
stay red because the F29 README row and the knowledge entry are other seats' work — this seat
drafts only the registry row and its bullets.

Mutation control (the limb is live on this row, so the row is not a no-op):

```
$ python3 .../r46-f29-gate.py --root $S/gateM      # row tier cell A -> B
gate H3 pass=0 read=bad=tier
f29-gate fixed=2/7 exit=1

$ python3 .../r46-f29-gate.py --root $S/gateM2     # row recheck cell 90d -> 90 days
gate H3 pass=0 read=bad=recheck-cell
gate H7 pass=0 read=census-rc=1 ok-line=0
f29-gate fixed=1/7 exit=1
```

## Finding 3 — the census: control (do-nothing) is clean, the draft's row adds exactly one honest E11, and a paired entry clears it

Control (base export `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, no S074 row):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/base/corpus/SOURCES.md --today 2026-10-29
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsB/base/corpus/SOURCES.md
exit=0
```

Treatment (this draft's row inserted; the paired knowledge entry does not exist yet — the census
resolves used-by paths against the registry's own directory, so the path must exist in the same
commit):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/treatment/corpus/SOURCES.md --today 2026-10-29
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
exit=1
```

This is exactly what the census prints for a registry row whose used-by path does not exist yet:
one `E11` line naming the missing path, and exit 1 (the three `W04` lines are pre-existing
warnings that do not change the exit status; there is no `ok` line while a finding exists).

Control B (same tree, with the paired entry present as a placeholder file) — the row itself is
census-clean:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/treatB/corpus/SOURCES.md --today 2026-10-29
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsB/treatB/corpus/SOURCES.md
exit=0
```

Mutation control on the census (proves the census is live on the treatment tree): with the row's
recheck cell changed from `90d` to `90 days`, the same command printed
`file	E09	S074 recheck=90 days` in addition to the `E11` and exited 1.

## Finding 4 — the capture is the pinned one and all nine manifest quotes locate

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

$ sha256sum corpus/source-snapshots/round-46-a2/S074.txt corpus/source-snapshots/round-46-a2/manifest.json corpus/source-snapshots/round-46/manifest.json corpus/instruments/source-recheck.py
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  corpus/source-snapshots/round-46-a2/S074.txt
46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f  corpus/source-snapshots/round-46-a2/manifest.json
01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34  corpus/source-snapshots/round-46/manifest.json
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
```

`S074.txt` is 42 lines / 7087 bytes; the `round-46-a2` manifest record carries `bytes` 582877 (the
raw fetch) and `snapshot_bytes` 7087, which is the "manifest raw 582877 bytes" the anchor cell
quotes (the same convention as S073's "manifest raw 577188 bytes" for the round-46 manifest's
`bytes: 577188`). The rule-1 grounding quote for `teaches` is 17 words and sits at S074.txt:38:
`"Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory."`

## Finding 5 — the absence sweep behind the Search-log bullet (PRISMA-style counts with a stop rationale)

Sweeps ran on the committed base export
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C $S/base`
(65 knowledge files; registry ends S073 with 73 rows; SOURCES.md 118066 bytes).

Four-term zero-hit test over `corpus/knowledge corpus/SOURCES.md corpus/README.md`:

```
term 'fix version' -> hits=0
term 'CVE identification number' -> hits=0
term 'publish the advisory' -> hits=0
term 'GitHub is a CVE' -> hits=0
```

Term sweep over the whole `corpus/` tree (ledger `corpus/knowledge/considerthese-proposals-ledger.md`
excluded, and its own hit count shown separately):

```
term 'repository security advisor   ' corpus-hits(excl. ledger)=5 ledger-hits=0
term 'private fork                  ' corpus-hits(excl. ledger)=11 ledger-hits=0
term 'advisory credit               ' corpus-hits(excl. ledger)=9 ledger-hits=0
term 'fix version                   ' corpus-hits(excl. ledger)=0 ledger-hits=0
term 'draft advisory                ' corpus-hits(excl. ledger)=1 ledger-hits=0
term 'draft security advisory       ' corpus-hits(excl. ledger)=3 ledger-hits=0
term 'request a CVE                 ' corpus-hits(excl. ledger)=1 ledger-hits=0
term 'CVE identification number     ' corpus-hits(excl. ledger)=0 ledger-hits=0
term 'publish the advisory          ' corpus-hits(excl. ledger)=0 ledger-hits=0
term 'GitHub is a CVE               ' corpus-hits(excl. ledger)=0 ledger-hits=0
```

Every non-zero hit is located and is *not* a maintainer-side lifecycle statement: the F28 entry
(`corpus/knowledge/github-private-vulnerability-reporting.md:23,40,43,49`), the S073 row and its
registry-change bullet (`corpus/SOURCES.md:79,161`), the F28 README lines (658, 666), the S073
capture's one pointer sentence (`corpus/source-snapshots/round-46/S073.txt:563` "create a draft
security advisory directly", quoted as Q2 in `corpus/lessons/round-46.md:34`), the round-46 lesson's
Q2/Q8 quotes, the claim-package fixture checklists ("advisory CREDITS"), the C2 gate/selftest
strings, and `corpus/source-snapshots/round-24/S003.txt:274`.

The six sibling pages the S074 capture names as link text only (each is a lead, not a row, and the
F29 scope excludes advisory editing, the REST API and the Advisory Database edit flow):

```
9:see Coordinated disclosure of security vulnerabilities.
16:see REST API endpoints for repository security advisories.
17:see Creating a repository security advisory.
18:see Adding a security policy to your repository.
19:see Editing security advisories in the GitHub Advisory Database.
34:See Editing a repository security advisory.
```

Corroborated by the independent scout seat `R46bScoutAbsence` (its Report:
`.ufo/waves/round-46/attempt2/wave1/R46bScoutAbsence.md`), whose base-export and live-lane sweep
`grep -rliE 'repository securit. advisor|GHSA' <scratch>/corpus/knowledge <scratch>/corpus/SOURCES.md <scratch>/corpus/README.md`
printed exactly `corpus/knowledge/github-private-vulnerability-reporting.md` and `corpus/SOURCES.md`,
while `grep -ciE 'repository securit. advisor|GHSA' <scratch>/corpus/README.md` printed `0`; the
live lane gave identical files and line numbers and `grep -rn 'S074' corpus/SOURCES.md
corpus/README.md` printed nothing (exit 1).

The Search-log bullet in the draft therefore records: date 2026-10-29; identified 13 units,
screened 13, included 1, excluded 12 (the primary page included as S074; the six sibling pages and
the six held rows S022/S030/S031/S065/S068/S073 excluded with reasons); stop rationale — the
primary page is GitHub's own first-party statement of the maintainer lifecycle, its sibling pages
are leads until a round opens and cites them, and the file-level and term-level sweeps leave no
unexamined in-lane candidate for this scope.

## Finding 6 — the `## Registry changes` bullets (pattern of the S073 bullets) and the capture-dir note

The draft supplies three append bullets (`rows.md` §(b)): the S074-row-added bullet (id, kind,
tier scope, status, opened, recheck, used-by, the anchor pin with the capture digest and line
locators, the 17-word rule-1 quote with its location, the access date from the manifest
`fetched_utc`, and "Registry rows 73 → 74 (R8); no pre-existing row status, recheck or used-by
cell changed"); the capture-directory note; and the "no status/recheck/used-by cell changed"
statement.

The capture-dir note is grounded in a sha pin that exists in the lane:

```
$ grep -rn "$(sha256sum corpus/source-snapshots/round-46/manifest.json | cut -d' ' -f1)" .ufo/waves/round-46 | cut -c1-200
.ufo/waves/round-46/freeze.txt:7:manifest-sha256 01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34
.ufo/waves/round-46/wave1/R46ScribeRegistry.md:90:corpus/source-snapshots/round-46/manifest.json MATCH     (01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34)
```

so `corpus/source-snapshots/round-46-a2/` exists beside `round-46/` because the round-46 manifest is
sha-pinned by the round-46 attempt-1 receipts and must stay byte-identical; the a2 directory holds
exactly the two new files `S074.txt` and `manifest.json`, both committed in the round-46 attempt-2
freeze commit `fe0f56b`. No file under `corpus/source-snapshots/round-46/` is modified by this
round.

## Limitations

1. Draft only. No file under `corpus/` was created or modified by this seat; the L1 integrates the
   row, the two bullets and the Search-log bullet. The row and the paired knowledge entry must land
   in the same commit, otherwise the census prints
   `file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md` and
   exits 1 (measured above).
2. The census was run with `--today 2026-10-29` (the host's UTC date, `date -u +%F` → `2026-10-29`),
   so the `opened` cell's date check was evaluated against today. A future run date could turn the
   `E08` check on `opened 2026-10-29` on.
3. The F29 gate was exercised on a scratch tree, not on the lane: H1, H2, H5 and H6 remain red
   there because the F29 README row, the knowledge entry and the 66-entry knowledge directory are
   other seats' work. Only H3 (the registry-row limb), H4 and H7 were in scope for this seat, and
   H3 was also checked with two mutants to show it is live on this row.
4. The gate's H7 limb runs the fleet-root census script (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`),
   which is outside the lane and outside this seat's scope; it was read and executed, never edited.
5. The page was not re-fetched from the network by this seat: the capture and its manifest are the
   L1's, frozen in commit `fe0f56b`, and this seat re-verified their digests and all nine quotes
   with the committed `source-recheck.py` (exit 0). The claim "HTTP 200, final URL equals the row
   URL" is therefore the frozen manifest's record, checked for internal consistency here, not a
   live fetch performed by this seat.
6. The six sibling pages named in the capture were not opened; they are recorded as leads with
   their capture line numbers, and the F29 scope excludes three of them by the task's own
   definition. "Coordinated disclosure of security vulnerabilities" and "Creating a repository
   security advisory" are named as leads only; a later round may find them in scope for a
   different frontier.
7. The Search-log unit count (13 = 1 primary page + 6 named sibling pages + 6 held rows) is a
   screening-unit count, not a page count; the underlying file-level and term-level sweep outputs
   are quoted verbatim in `sweep-receipts.txt` so the count can be re-derived.
8. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsB/`) was removed after the receipts were
   copied into the draft directory; the receipts are the citable evidence, not the scratch paths.
