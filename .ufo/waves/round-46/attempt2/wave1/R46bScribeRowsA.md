VERDICT: DRAFT-READY

# R46bScribeRowsA — C2 registry drafter A (kasegi, round 46 attempt 2)

Seat: C2 registry drafter A. Scope: **draft only** — nothing in `corpus/` was edited by this seat.
Item: the S074 `corpus/SOURCES.md` row, the `## Registry changes` bullets, and the `## Search log`
bullet for frontier F29 (GitHub repository security advisories, maintainer-side advisory lifecycle).

Files written by this seat (the only ones):
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/rows.md` — the draft (row + both bullet sets)
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/census-receipts.txt` — census runs and outputs
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/gate-receipts.txt` — committed-gate run + 3 negative controls
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/sweep-receipts.txt` — absence-sweep commands and printed output
- `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.md` — this report

Nothing else was touched: `corpus/SOURCES.md`, the committed counters `corpus/instruments/r46-c1-gate.py`
and `r46-c2-gate.py`, the committed `corpus/instruments/r46-f29-gate.py`, and the frozen claims file
`.ufo/waves/round-46/attempt2/claims.json` are byte-unchanged. No commit, push, or mutating git/jj
command was run anywhere; only `git archive`, `git show`, `git diff --name-status`, `git log`,
`git rev-parse`, `git status` (read-only). No tool was installed — the host's `bash`, `gawk`,
`python3`, `sha256sum`, `wc` and the lane's committed instruments were sufficient — so there is no
tool/version/channel record to report. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA`)
was removed after the receipts were copied into the draft dir.

## Finding 1 — the S074 row: 11 cells exactly, no `|` inside any cell

The row drafted in `rows.md` §(a), placed inside `## Registry` immediately after the `| S073 |` row
(today `corpus/SOURCES.md:79`; `## Paths` begins at `:81`):

```
| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side flow, advisory editing, the REST API or the Advisory Database edit flow | heading and body prose lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL), sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 | Draft the advisory, fix in a temporary private fork and credit contributors before publication; request the CVE from GitHub as CNA while the advisory is still private, because requesting a CVE does not make the advisory public. | mined | 2026-10-29 | 90d | corpus/knowledge/github-repository-security-advisories.md |
```

Command (scratch tree `/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/work`, a `git archive HEAD
corpus` export with the row inserted after the `| S073 |` line):

```
$ python3 -  # parse the row, print cell count and the graded cells
cells: 11
kind: 'docs' tier: 'A' status: 'mined' opened: '2026-10-29' recheck: '90d'
scope words: 45 teaches words: 37
pipe in any cell: False
```

Every cell value was checked against the live registry's shape (`corpus/SOURCES.md` rows S072/S073)
and against `CORPUS.md`'s `SOURCES.md` contract:

- **id** `S074` — the next unused id. The registry runs S001–S073 today:
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **73**.
- **source** — `GitHub Docs, Repository security advisories — <canonical URL>`. The canonical URL is
  the **first** url in the cell (both the census's `url_of()` and the F29 gate's H3 take the first
  match); `grep -c 'repository-security-advisories' corpus/SOURCES.md` printed **0** before the
  insert, so the URL is new to the registry.
- **kind** `docs` · **tier** `A` — tier A is scoped by the scope cell, never global.
- **scope** — the maintainer-side advisory lifecycle ONLY: draft advisory, temporary private fork,
  CVE request via GitHub as CNA, credit, publication and the fix-version duty; explicitly **not**
  the reporter-side flow, advisory editing, the REST API or the Advisory Database edit flow. Each of
  those four exclusions is a surface the capture names only as link text or a one-line pointer:
  `S074.txt:16` (REST API), `S074.txt:19` (Advisory Database edit flow), `S074.txt:34` (editing a
  repository security advisory), and the reporter-side flow held by S073.
- **anchor** — `lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt`, plus the capture
  digest, the snapshot size, the manifest raw byte count, the fetch timestamp, HTTP 200 and the
  final-URL equality. The manifest's own S074 record carries exactly those numbers:
  `sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, `bytes 582877`,
  `snapshot_bytes 7087`, `lines 42`, `fetched_utc 2026-10-29T20:19:30Z`, `http.status 200`,
  `http.final_url` equal to the row URL. Independently re-measured on the live capture:
  `sha256sum …/round-46-a2/S074.txt` → `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`
  and `wc -lc …` → `42 7087`.
- **teaches** — 37 words, one grounded learner benefit: draft → private fork → credit → publish, and
  request the CVE from GitHub as CNA while the advisory is still private. Grounded sentence by
  sentence in the capture: `S074.txt:10` (privately discuss and fix), `:12` (draft advisory), `:13`
  (temporary private fork), `:17` (credit), `:24` (GitHub is a CNA), `:25` (request a CVE; requesting
  one does not make the advisory public), `:38` (add a fix version prior to publishing).
- **status** `mined` · **opened** `2026-10-29` · **recheck** `90d` (a cadence, not a recency claim)
  · **used-by** `corpus/knowledge/github-repository-security-advisories.md`.

## Finding 2 — the census run on a scratch copy with the row inserted, quoted exactly

Command:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/work/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
EXIT=1
```

**The census prints exactly one new finding, `E11`, and exits 1 — because the used-by entry file
`corpus/knowledge/github-repository-security-advisories.md` does not exist yet.** The census resolves
used-by paths relative to the tree root, so the row is clean the moment that entry lands; the E11
is not a defect in the row. The three `W04` lines are pre-existing (they are the same three the
lane's own before-receipt `controls/sources-census-before.txt` records, and the census-before
receipt exits 0 with them).

Two controls on the same scratch tree discriminate that reading:

*Entry present (placeholder file), same command:*

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/ctrl2/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/ctrl2/corpus/SOURCES.md
EXIT=0
```

*Do-nothing control — the same tree with the S074 row removed:*

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/ctrl3/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/ctrl3/corpus/SOURCES.md
EXIT=0
```

So: the row contributes **no** E-code of its own; the only difference between "row absent" and
"row present" is the E11 raised by the not-yet-written entry file. No E01 (11-cell shape), no E05
(kind), no E07 (status), no E08 (opened), no E09 (recheck cadence), no E04/W04 for this URL, and
no E12 (row outside `## Registry`) is raised.

## Finding 3 — the committed F29 gate grades this row, and three negative controls prove it is graded

The committed, frozen instrument `corpus/instruments/r46-f29-gate.py` (unmodified) run against a
tree carrying this seat's SOURCES.md:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/g1 --work /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/g1work
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
EXIT=0
```

H3 — the limb that grades the SOURCES.md row — reads `row-S074=ok`. The tree was built by the
committed control `controls/f29-fixture.py --mode positive` and then had **this seat's**
`corpus/SOURCES.md` copied in, so the row under test is the row drafted here.

Three negative controls on the same tree, each mutating only the S074 row:

```
--- anchor sha256 hex replaced by zeros (cell count preserved) ---
gate H3 pass=0 read=bad=anchor-sha
f29-gate fixed=6/7 exit=1

--- kind cell changed to 'Docs' ---
gate H3 pass=0 read=bad=kind
f29-gate fixed=5/7 exit=1

--- anchor sha256 hex + label deleted (row loses one cell) ---
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=1
f29-gate fixed=5/7 exit=1
```

The row is therefore graded on its content, not merely accepted for being present.

## Finding 4 — the `## Registry changes` bullets to append

Drafted in `rows.md` §(b), in the S073 bullet's shape, to be appended at the end of the
`## Registry changes` section (today `:118`–`:162`):

1. **S074 row added** — new row (id `S074`, kind `docs`, tier A scoped to the maintainer-side
   advisory lifecycle only, status mined, opened 2026-10-29, recheck `90d`, used-by
   `corpus/knowledge/github-repository-security-advisories.md`), anchor pinned to the round-46-a2
   capture with its sha256 and the located line map (heading L2, purpose L3, private discuss-and-fix
   L10, draft advisory L12, temporary private fork L13, publish-on-patch L14, credit L17, CNA L24,
   CVE request and 72-hour review L25, other-CNA boundary L26, publication visibility L30–L31, URL
   stability L33, Dependabot alerts L35–L36, fix-version duty L37–L38). Rule-1 Gate quote grounding
   `teaches` (11 words): "Requesting a CVE identification number doesn't make your security advisory
   public." (S074.txt:25). Access 2026-10-29 (manifest `fetched_utc 2026-10-29T20:19:30Z`, HTTP 200,
   final URL equals the row URL). Registry rows 73 → 74 (R8); no pre-existing row status, recheck or
   used-by cell changed.
2. **Capture directory note** — `corpus/source-snapshots/round-46-a2/` exists beside
   `corpus/source-snapshots/round-46/` because the attempt-1 round-46 manifest is sha-pinned by the
   round-46 attempt-1 receipts and must stay byte-identical. Verified here, not asserted:
   `git show 04af9bc92229232ea5cce8b32bfe59dd969eb26d:corpus/source-snapshots/round-46/manifest.json | sha256sum`
   → `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`, equal to the digest at
   HEAD and in the worktree, and equal to the pin recorded at `.ufo/waves/round-46/freeze.txt:7` and
   `.ufo/waves/round-46/wave1/R46SentinelContent.md:13`; the new a2 manifest hashes to
   `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f` (pinned as `manifest-a2-sha256`
   in `.ufo/waves/round-46/attempt2/freeze.txt`). `git diff --name-status 04af9bc9… HEAD --
   corpus/source-snapshots/` prints only the two `A` additions under `round-46-a2/`, so no attempt-1
   capture byte moved.

## Finding 5 — the `## Search log` bullet (PRISMA-style, with a stop rationale)

Drafted in `rows.md` §(c), to be appended inside `## Search log` (today `:90`–`:111`, the F28 bullet
at `:110`; `## Leads (unopened)` at `:112`) after the F28 bullet. Its sweep commands and printed
output were re-run by this seat (receipts `sweep-receipts.txt`); the counts were first established
by the absence-scout seat `R46bScoutAbsence`.

On the committed base export (`git archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus`):

```
$ grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md
corpus/knowledge/github-private-vulnerability-reporting.md
corpus/SOURCES.md
EXIT=0

$ grep -ciE 'repository securit. advisor|GHSA' corpus/README.md
0
EXIT=1

$ grep -rn 'S074' corpus/SOURCES.md corpus/README.md
EXIT=1

$ grep -rniE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | cut -c1-95
corpus/knowledge/github-private-vulnerability-reporting.md:40:- The page does not state the mai
corpus/knowledge/github-private-vulnerability-reporting.md:43:- Four linked pages appear only a
corpus/SOURCES.md:74:| S068 | GitHub Advisory Database entry GHSA-v676-f8gm-92r9 for CVE-2025-9
corpus/SOURCES.md:157:- Public disclosed advisory pair for the claim-package gate exemplar (rou
EXIT=0
```

and on the live lane the same file-level sweep printed the same two files. Counts behind the bullet:
`find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → **65**;
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **73**;
`grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **28**;
`grep -c 'repository-security-advisories' corpus/SOURCES.md` → **0**.

The bullet's PRISMA line reads: *identified 4 units, screened 4, included 1, excluded 3* — the
primary page https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
included as S074 with the new entry `corpus/knowledge/github-repository-security-advisories.md`;
excluded, with reason: the F28 entry's two scope-out notes at
`corpus/knowledge/github-private-vulnerability-reporting.md:40` and `:43` (the linked page "Creating
a repository security advisory" appears there only as link text in the S073 capture, `S073.txt:563`,
so the maintainer-side body was never held — confirmed here: `grep -n 'Creating a repository
security advisory' corpus/source-snapshots/round-46/S073.txt` returns only the L563 pointer), the
rejected S068 row at `corpus/SOURCES.md:74` (an Advisory Database mirror of one NVD record, tier B,
not the maintainer-side lifecycle), and the round-43 search-log bullet at `corpus/SOURCES.md:157` (a
historical note naming GHSA candidates for a different question). **Stop rationale:** the four hits
are the whole in-corpus mention of this ground and every one points away from it, so the sweep
stopped at the opened primary page; the sibling pages it links (creating a repository security
advisory, editing a repository security advisory, editing GitHub Advisory Database advisories, the
REST API endpoints) stay leads, not rows, until a round opens them.

## Limitations

- **The used-by path does not exist yet.** The census on the scratch copy prints
  `file E11 S074 missing used-by corpus/knowledge/github-repository-security-advisories.md` and exits
  1. That entry is another seat's deliverable; this seat drafts only the row that points at it.
  When it lands, the same command prints `file ok …` and exits 0 (shown above).
- **The gate run above is on a synthetic tree, not the live lane.** The live lane has no F29
  frontier row, no F29 entry and no S074 row yet, so `r46-f29-gate.py --root <live lane>` cannot
  reach 7/7 today; the run above uses the committed `controls/f29-fixture.py --mode positive` tree
  with this seat's SOURCES.md substituted in, which isolates exactly what this seat produces. The
  fixture's own entry text is the fixture's, not this seat's — this seat drafted no entry file.
- **The capture was not re-fetched.** Live-target testing is refused for this corpus, and the
  capture was opened by the L1 on 2026-10-29T20:19:30Z. This seat verified the committed capture's
  bytes, digest, line map and manifest record against the manifest, and verified the source-recheck
  result the gate reports (`recheck-rc=0 quotes-ok=9`), but did not re-fetch the page itself.
- **The `## Registry changes` and `## Search log` bullets are drafts only.** Their final wording,
  their placement among sibling bullets, and the round lesson's `## Gate` section belong to the L1
  at integration; appending them is a write to a shared production file and was not done here.
- **Row text is not byte-pinned by any frozen instrument.** The F29 gate's H3 grades the row's
  structure (11 cells, kind, tier, scope/teaches word floors, opened date, recheck cadence, anchor
  digest and locator, used-by path, canonical first URL) but not its prose; the entry's bytes and
  the row's bytes were explicitly not pinned at freeze.
- **The census script lives at the fleet root**, outside this lane; the H7 limb depends on it, so a
  change there would change this seat's H7 result.

## Out of scope for this seat (not done)

- No edit to `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/**`, `corpus/lessons/**`.
- No F29 frontier row in `corpus/README.md` and no knowledge entry — other seats' deliverables.
- No commit, push, or mutating git/jj command anywhere; no edit to the committed counters, the
  frozen claims file, `MANIFEST.json`, `.ufo/state`, the fleet repo, sibling lanes, or
  `~/Projects/shokuknow`.

Report: .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.md
