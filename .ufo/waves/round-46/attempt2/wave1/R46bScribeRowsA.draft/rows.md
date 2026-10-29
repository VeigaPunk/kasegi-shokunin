# R46bScribeRowsA — draft registry material for C2 / F29 / S074 (kasegi, round 46 attempt 2)

Seat: C2 registry drafter A. Draft only — nothing in `corpus/` was edited by this seat.
Contract: `CORPUS.md` section `SOURCES.md — where a shokunin learns` (v1, frozen).
Live shape read from `corpus/SOURCES.md` rows S072/S073 (the two immediately preceding rows).

## (a) The S074 registry row

Placement: inside `## Registry`, immediately after the `| S073 |` row (today that row is
`corpus/SOURCES.md:79`; `## Paths` starts at `:81`). **11 cells, no `|` inside any cell.**

```markdown
| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side flow, advisory editing, the REST API or the Advisory Database edit flow | heading and body prose lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL), sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 | Draft the advisory, fix in a temporary private fork and credit contributors before publication; request the CVE from GitHub as CNA while the advisory is still private, because requesting a CVE does not make the advisory public. | mined | 2026-10-29 | 90d | corpus/knowledge/github-repository-security-advisories.md |
```

Cell-by-cell:

| # | cell | value | why |
|---|---|---|---|
| 1 | id | `S074` | next unused id; the registry runs S001–S073 today (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` prints 73) and the ids are never reused. |
| 2 | source | `GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories` | the canonical URL, and the FIRST url in the cell (the census's `url_of()` and the F29 gate's H3 both take the first match). |
| 3 | kind | `docs` | the census `kind` enum; the capture is GitHub's own documentation page. |
| 4 | tier | `A` | authoritative for the scoped ground: GitHub's own statement of its own maintainer-side advisory lifecycle. The scope cell bounds it, so tier A is not global. |
| 5 | scope | maintainer-side advisory lifecycle ONLY … not the reporter-side flow, advisory editing, the REST API or the Advisory Database edit flow | tier A is scoped to the scope cell; the four exclusions are the four neighbouring surfaces the capture only names as link text (`S074.txt:16` REST API, `S074.txt:19` Advisory Database edit flow, `S074.txt:34` editing a repository security advisory) and the reporter-side flow held by S073. |
| 6 | anchor | `lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt` + sha256 `1296528d…c278039` + `snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL` | exact section plus the revision (the capture digest). The manifest's own record for S074 carries `sha256 1296528d…c278039`, `bytes 582877`, `snapshot_bytes 7087`, `lines 42`, `fetched_utc 2026-10-29T20:19:30Z`, `http.status 200`, `http.final_url` equal to the row URL. The locator `lines 1-42` sits inside the capture's body (1–42). |
| 7 | teaches | draft → private fork → credit → publish; request the CVE from GitHub as CNA while still private | one grounded learner benefit, ≥8 words (37). Grounded by the capture's own sentences at `S074.txt:10` (privately discuss and fix), `:12` (draft advisory), `:13` (temporary private fork), `:17` (credit), `:24` (GitHub is a CNA), `:25` (request a CVE; requesting one does not make the advisory public), `:38` (add a fix version prior to publishing). |
| 8 | status | `mined` | the row is cited by `corpus/knowledge/github-repository-security-advisories.md` (the `used-by` cell). |
| 9 | opened | `2026-10-29` | ISO date the row's author opened the source (manifest `fetched_utc 2026-10-29T20:19:30Z`). |
| 10 | recheck | `90d` | a cadence, not a recency claim; the census accepts `^[0-9]+d$`. |
| 11 | used-by | `corpus/knowledge/github-repository-security-advisories.md` | the repo-relative path of the knowledge entry that cites this row. |

Anchor-cell line map (for the L1's `## Registry changes` bullet), read from the committed capture
`corpus/source-snapshots/round-46-a2/S074.txt` (42 lines):

| capture line | what it carries |
|---|---|
| L2 | heading `## Repository security advisories` |
| L3 | one-line purpose: privately discuss, fix and publish |
| L10 | maintainers of public repositories may privately discuss and fix |
| L12 | create a draft security advisory, use it to discuss impact privately |
| L13 | privately collaborate to fix in a temporary private fork |
| L14 | publish the advisory once a patch is released |
| L17 | give credit to individuals who contributed |
| L19 | advisory stays in the repository; published to the GitHub Advisory Database; anyone may submit a change there (the edit flow this row excludes) |
| L16 | REST API for repository security advisories (excluded by the scope cell) |
| L24 | GitHub is a CNA and is authorized to assign CVE identification numbers |
| L25 | you may request a CVE from GitHub; usually reviewed within 72 hours; requesting one does not make the advisory public |
| L26 | GitHub cannot assign CVEs to a project covered by another CNA |
| L27 | GitHub publishes the CVE to the MITRE database after publication |
| L30–L31 | publication visibility: the advisory data and accepted credits are public, the conversation history is not |
| L33 | the advisory URL does not change after publication |
| L34 | editing a published repository security advisory (excluded by the scope cell) |
| L35–L36 | Dependabot alerts; a fork's advisory alerts only if the fork owns a package on a public registry |
| L37–L38 | importance of fix versions: add a fix version before publishing |
| L39–L42 | the three fix-version states (imminent, in development, not planned) |

## (b) `## Registry changes` bullets to append

Append at the end of the `## Registry changes` section (today that section starts at
`corpus/SOURCES.md:118` and the file ends at `:162`). Follow the S073 bullet's shape.

```markdown
- S074 row added: new row (id `S074`, kind `docs`, tier A scoped to GitHub's own statement of the maintainer-side advisory lifecycle only, status mined, opened 2026-10-29, recheck `90d`, used-by `corpus/knowledge/github-repository-security-advisories.md`), anchor pinned to the round-46-a2 capture `corpus/source-snapshots/round-46-a2/S074.txt` (sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines: heading L2, one-line purpose L3, private discuss-and-fix L10, draft advisory L12, temporary private fork L13, publish-on-patch L14, credit L17, CNA L24, CVE request and 72-hour review L25, other-CNA boundary L26, publication visibility L30-L31, URL stability L33, Dependabot alerts L35-L36, fix-version duty L37-L38). Rule-1 Gate quote grounding `teaches` (11 words): "Requesting a CVE identification number doesn't make your security advisory public." (S074.txt:25). Access 2026-10-29 (manifest `fetched_utc` 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL). Registry rows 73 → 74 (R8); no pre-existing row status, recheck or used-by cell changed.
- Capture directory note: `corpus/source-snapshots/round-46-a2/` exists beside `corpus/source-snapshots/round-46/` because the attempt-1 round-46 manifest is sha-pinned by the round-46 attempt-1 receipts (`01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`, recorded at `.ufo/waves/round-46/freeze.txt:7` and `.ufo/waves/round-46/wave1/R46SentinelContent.md:13`) and therefore must stay byte-identical; the attempt-1 manifest hashes to that digest at base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, at HEAD and in the worktree, while the new attempt-2 manifest `corpus/source-snapshots/round-46-a2/manifest.json` hashes to `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f` (pinned as `manifest-a2-sha256` in `.ufo/waves/round-46/attempt2/freeze.txt:7`). `git diff --name-status 04af9bc92229232ea5cce8b32bfe59dd969eb26d HEAD -- corpus/source-snapshots/` prints only the two `A` additions under `round-46-a2/`, so no attempt-1 capture byte moved.
```

## (c) The `## Search log` bullet to append

Append inside `## Search log` (today that section spans `corpus/SOURCES.md:90`–`:111`, the F28
bullet at `:110`; `## Leads (unopened)` starts at `:112`), after the F28 bullet, separated by one
blank line. PRISMA-style, in the F28 bullet's shape. The sweep commands and their printed output
are the ones this seat re-ran itself (receipts in this draft dir); the counts were first
established by the absence-scout seat `R46bScoutAbsence`.

```markdown
- Repository security advisory lifecycle sweep (round 46 attempt 2, frontier F29); question: does the lane hold a first-party source for GitHub's maintainer-side repository security advisory lifecycle (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication, fix-version duty), and does any held row or entry already cover it; where: the committed base export (`git archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus`) swept with `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md`, which printed 2 files and exited 0 over 65 knowledge files, the README and SOURCES — `corpus/knowledge/github-private-vulnerability-reporting.md` and `corpus/SOURCES.md` — with the same command on the live lane printing the same 2 files; `grep -ciE 'repository securit. advisor|GHSA' corpus/README.md` printed 0 and exited 1 (no frontier admission), `grep -rn 'S074' corpus/SOURCES.md corpus/README.md` printed nothing and exited 1 (no row, no admission), and the line-level `grep -rniE 'repository securit. advisor|GHSA'` gave 4 hits: the F28 entry's scope-out notes at `corpus/knowledge/github-private-vulnerability-reporting.md:40` and `:43`, the rejected S068 Advisory-Database row at `corpus/SOURCES.md:74`, and the round-43 search-log bullet at `corpus/SOURCES.md:157`; date 2026-10-29; identified 4 units, screened 4, included 1, excluded 3: the primary page https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories (included as S074 with the new entry `corpus/knowledge/github-repository-security-advisories.md`); excluded, with reason: the F28 entry's two scope-out notes (the linked page "Creating a repository security advisory" appears there only as link text in the S073 capture, `S073.txt:563`, so the maintainer-side body was never held), the rejected S068 row (an Advisory Database mirror of one NVD record, tier B, not the maintainer-side lifecycle) and the round-43 search-log bullet (a historical note naming GHSA candidates for a different question). Stop rationale: the four hits are the whole in-corpus mention of this ground and every one of them points away from it, so the sweep stopped at the opened primary page; the sibling pages it links (creating a repository security advisory, editing a repository security advisory, editing GitHub Advisory Database advisories, the REST API endpoints) stay leads, not rows, until a round opens them.
```

## Validation performed by this seat (all re-runs by this seat; raw output in the receipts)

1. **Census on a scratch copy with the row inserted** — `bash
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file
   /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsA/work/corpus/SOURCES.md` printed
   `file E11 S074 missing used-by corpus/knowledge/github-repository-security-advisories.md`
   (plus the three pre-existing W04 warnings) and exited **1**. The E11 is expected and is the
   only new finding: the entry file `corpus/knowledge/github-repository-security-advisories.md`
   does not exist yet, so the census's used-by existence check fails on it. The census resolves
   used-by paths relative to the tree root, so the same file passes as soon as the entry lands.
   Control: with a placeholder entry file present in the scratch tree the same command printed
   `file ok …` and exited **0**, with the same three W04 warnings and no E-code — so the row
   itself introduces no E-code and the E11 is purely the not-yet-written entry.
2. **Committed F29 gate on a tree carrying this row** — `python3
   corpus/instruments/r46-f29-gate.py --root <fixture tree with this SOURCES.md>` printed
   `gate H3 pass=1 read=row-S074=ok` and `f29-gate fixed=7/7 exit=0`.
3. **Negative controls** — the same gate on the same tree with (a) the anchor sha256 replaced by
   zeros printed `gate H3 pass=0 read=bad=anchor-sha` and `f29-gate fixed=6/7 exit=1`; (b) the
   kind cell changed to `Docs` printed `gate H3 pass=0 read=bad=kind` and `f29-gate fixed=5/7
   exit=1`; (c) the anchor sha256 text deleted printed `gate H3 pass=0
   read=row-S074=absent-or-malformed-or-not-registry-only hits=1`. The row therefore is graded,
   not merely present.
4. **Do-nothing control** — the census on the same scratch tree with the S074 row removed
   printed the same three W04 warnings plus `file ok …` and exited 0, so the warnings are
   pre-existing and not caused by the new row.

## Notes for the L1 integrator

- The `used-by` path `corpus/knowledge/github-repository-security-advisories.md` must exist in the
  lane before the census can exit 0 (E11 otherwise). The entry is another seat's deliverable; this
  seat only drafts the row that points at it.
- Rows are append-only: only `status`, `recheck` and `used-by` change in place on existing rows,
  and no pre-existing row needs a change here — S074 is a new row.
- The S074 scope cell deliberately differs from S073's scope cell and from the S068/S065 rows'
  scopes, so no E04 duplicate-URL-within-scope and no W04 duplicate-URL-across-scopes is raised
  for this URL (`grep -c 'repository-security-advisories' corpus/SOURCES.md` printed 0 before
  the insert).
