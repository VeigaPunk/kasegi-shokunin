# R46bScribeRowsB — C2 registry drafter B (round 46 attempt 2; DRAFT only, not applied)

Status: DRAFT for the L1 to integrate. This seat wrote no registry file in the lane; the only
files written are this draft and the seat Report. The row (a) must land in the same commit as
`corpus/knowledge/github-repository-security-advisories.md`: without that entry the used-by path
is missing and the census exits 1 (measured below).

Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`). Round 46 attempt 2, C2
(coverage), frontier F29. Frozen base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; freeze commit
`fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`. Opened 2026-10-29.

## (a) Registry row (11 cells; no `|` inside any cell)

| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side advisory lifecycle only: draft the advisory, fix it in a temporary private fork, request a CVE from GitHub as CNA, credit contributors, publish, and carry the fix-version duty; not the reporter-side flow (S073), not advisory editing, not the REST API and not the Advisory Database edit flow | lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt, sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL): L10 the maintainer statement, L12-L15 the three capabilities, L17 the credit bullet, L24-L26 the CVE-request paragraphs, L31-L33 the publication visibility rules, L38 the fix-version duty | A maintainer's advisory lifecycle runs draft → private-fork fix → CVE request to GitHub as CNA (a request does not publish) → credit → publication; publish with a fix version, or Dependabot alerts users with no safe version to move to. | mined | 2026-10-29 | 90d | corpus/knowledge/github-repository-security-advisories.md |

Cell notes for the L1 (not part of the row):

- `kind` = `docs`, `tier` = `A` scoped to GitHub's own statement of the maintainer-side lifecycle
  (contract tier A: primary/official docs for that scope), `status` = `mined` (the row is cited by
  `corpus/knowledge/github-repository-security-advisories.md`), `opened` = `2026-10-29`,
  `recheck` = `90d` (cadence only, per census rule E09: no fetch note in the recheck cell).
- `scope` names the five lifecycle duties the page states and explicitly fences off the four
  neighbours that are out of scope for F29: the reporter-side flow (held as S073), advisory editing,
  the REST API and the Advisory Database edit flow. Each of those four is a separate page named
  only as link text in the capture, so it is a lead, not a row.
- `anchor` pins the exact capture: file path, sha256, snapshot size (42 lines, 7087 bytes), the
  manifest's raw fetch size (582877 bytes), the fetch timestamp and the HTTP/final-URL fact, then
  the line locators used by the entry.
- `teaches` is one grounded learner benefit (37 words) whose last clause is the fix-version duty
  grounded by the rule-1 quote "Whenever possible, you should add a fix version to a security
  advisory prior to publishing the advisory." (S074.txt:38, 17 words, ≤ 25 words as rule 1 requires).
- No `|` appears in any cell; the row is 11 cells (census NF = 13).

## (b) `## Registry changes` bullets to append

- S074 row added: new row (id `S074`, kind `docs`, tier A scoped to GitHub's own statement of the maintainer-side advisory lifecycle only, status mined, opened 2026-10-29, recheck `90d`, used-by `corpus/knowledge/github-repository-security-advisories.md`), anchor pinned to the round-46-a2 capture `corpus/source-snapshots/round-46-a2/S074.txt` (sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines, 7087 bytes: L10 the maintainer statement, L12-L15 the three capabilities, L17 the credit bullet, L24-L26 the CVE-request paragraphs, L31-L33 the publication visibility rules, L38 the fix-version duty). Rule-1 Gate quote grounding `teaches` (17 words): "Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory." (S074.txt:38). Access 2026-10-29 (manifest `fetched_utc` 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL; manifest raw 582877 bytes, snapshot 7087 bytes). Registry rows 73 → 74 (R8); no pre-existing row status, recheck or used-by cell changed.
- Capture-directory note (round 46 attempt 2): the S074 capture and its manifest live in the new sibling directory `corpus/source-snapshots/round-46-a2/`, not in `corpus/source-snapshots/round-46/`, because the round-46 manifest is sha-pinned by the round-46 attempt-1 receipts and must stay byte-identical: `corpus/source-snapshots/round-46/manifest.json` is `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`, recorded in `.ufo/waves/round-46/freeze.txt:7` and re-verified in `.ufo/waves/round-46/wave1/R46ScribeRegistry.md:90` ("MATCH"). Adding an S074 record to that manifest would have changed those pinned bytes. `corpus/source-snapshots/round-46-a2/` therefore holds exactly two new files, `S074.txt` (sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines, 7087 bytes) and `manifest.json` (sha256 `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`), both committed in the round-46 attempt-2 freeze commit `fe0f56b`; no file under `corpus/source-snapshots/round-46/` is modified by this round.
- No status/recheck/used-by cell changed on any pre-existing row; S001–S073 untouched (logged). Registry 73 rows pre-append → 74 post-append (R8).

## (c) Search-log bullet

- Maintainer-side advisory lifecycle sweep (round 46 attempt 2, frontier F29); question: does the lane hold a first-party source for GitHub's maintainer-side repository security advisory lifecycle (draft advisory, private-fork fix, CVE request with GitHub as CNA, credit, publication visibility and the fix-version duty), and do any held rows already state it; where: the committed base export (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C <scratch>`), swept over `corpus/knowledge` (65 files), `corpus/SOURCES.md` and `corpus/README.md` with `grep -rliE 'repository securit. advisor|GHSA' <scratch>/corpus/knowledge <scratch>/corpus/SOURCES.md <scratch>/corpus/README.md`, which printed exactly two files (`corpus/knowledge/github-private-vulnerability-reporting.md` and `corpus/SOURCES.md`), while `grep -ciE 'repository securit. advisor|GHSA' <scratch>/corpus/README.md` printed `0`; date 2026-10-29; identified 13 units, screened 13, included 1, excluded 12: the primary page https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories (included as S074); the six sibling pages the capture names as link text only — Coordinated disclosure of security vulnerabilities (S074.txt:9), REST API endpoints for repository security advisories (L16), Creating a repository security advisory (L17), Adding a security policy to your repository (L18), Editing security advisories in the GitHub Advisory Database (L19) and Editing a repository security advisory (L34) — all excluded because their bodies are not in the capture and the F29 scope excludes advisory editing, the REST API and the Advisory Database edit flow (leads, not rows); and the six held rows S022, S030, S031, S065, S068 and S073, all excluded because S073 states the reporter-side flow only ("not maintainer handling of a report, the GitHub Advisory Database or CVE assignment") and its one maintainer-side sentence is a pointer ("create a draft security advisory directly", S073.txt:563, quoted as Q2 in corpus/lessons/round-46.md:34), S031/S030/S022 state the CNA program's own rules rather than GitHub's maintainer advisory flow, S065 states a different interchange vocabulary and S068 is one rejected Advisory-Database record. A four-term zero-hit sweep over the same export (`grep -rniE 'fix version'`, `'CVE identification number'`, `'publish the advisory'`, `'GitHub is a CVE'`) printed 0 hits for every term, so no held row states the fix-version duty, the CVE-request mechanics or the publication step; stop rationale: the primary page is GitHub's own first-party statement of the maintainer lifecycle, its sibling pages are leads until a round opens and cites them, and the file-level and term-level sweeps leave no unexamined in-lane candidate for this scope.

## Validation performed on a scratch copy (not the lane)

Base export used for all sweeps: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C $S/base`
($S = `/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsB`, `TMPDIR` passed explicitly; scratch removed on exit).
Verbatim outputs are copied into this draft directory: `census-receipts.txt`, `gate-receipts.txt`,
`sweep-receipts.txt`.

- Control (do-nothing, no S074 row):
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/base/corpus/SOURCES.md --today 2026-10-29` →
  ```
  file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
  file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
  file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
  file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsB/base/corpus/SOURCES.md
  exit=0
  ```
- Treatment (this draft's row inserted after S073; the paired knowledge entry does not exist yet):
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/treatment/corpus/SOURCES.md --today 2026-10-29` →
  ```
  file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
  file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
  file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
  file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
  exit=1
  ```
  The `E11` is the expected, honest state of a draft whose paired knowledge entry has not landed yet
  (the census resolves used-by paths against the registry's own directory, so the path must exist in
  the same commit). It is not a defect in the row.
- Control B (same tree + the paired knowledge entry present as a placeholder file): the same command
  printed the three `W04` warnings and `file	ok	.../treatB/corpus/SOURCES.md`, exit 0 — so the row
  itself is census-clean and the `E11` is caused solely by the missing entry.
- Mutation control (proves the census is live on the treatment tree): with the row's recheck cell
  changed from `90d` to `90 days`, the same command printed
  `file	E09	S074 recheck=90 days` in addition to the `E11`, exit 1.
- F29 admission gate, run against the scratch tree that carries this draft's row plus the committed
  `round-46-a2` capture and a placeholder entry:
  `python3 corpus/instruments/r46-f29-gate.py --root $S/gate` →
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
  H3 is the limb that grades the S074 registry row, and it passes on this draft
  (`row-S074=ok`: 11 cells, kind `docs`, tier `A`, scope 57 words, teaches 39 words, recheck `90d`,
  anchor locator `lines 1-42` inside the 42-line capture, anchor sha256 present, status `mined`,
  opened `2026-10-29`, row URL equal to the capture URL, used-by path present). H1/H2/H5/H6 stay red
  because the F29 README row and the knowledge entry are other seats' work, not this draft's.
- Gate mutation controls (the H3 limb is live on this row, i.e. the row is not a no-op):
  tier cell `A` → `B` gives `gate H3 pass=0 read=bad=tier`; recheck cell `90d` → `90 days` gives
  `gate H3 pass=0 read=bad=recheck-cell` and `gate H7 pass=0 read=census-rc=1 ok-line=0`.
- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` →
  ```
  S074:sha256 OK
  S074:Q1 OK occurrences=1 anchor=10-ok
  …
  S074:Q9 OK occurrences=1 anchor=38-ok
  exit=0
  ```
- Digests re-measured: `S074.txt` `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`
  (42 lines, 7087 bytes), `round-46-a2/manifest.json`
  `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`, `round-46/manifest.json`
  `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34` (unchanged), `source-recheck.py`
  `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` — all four equal the pins the
  gate asserts.
