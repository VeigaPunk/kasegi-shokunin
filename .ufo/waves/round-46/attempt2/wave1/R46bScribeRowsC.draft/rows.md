# R46bScribeRowsC — C2 registry draft (F29 / S074). DRAFT ONLY; the L1 integrates.

Seat: C2 registry drafter C (independent of `R46bScribeRowsB`). Nothing outside this
draft directory and the seat Report file was written; no git/jj command was run that
mutates any repository, index or working tree.

## 0. Where the row goes

Insert the row below **directly after the S073 row** in the `## Registry` table of
`corpus/SOURCES.md` (at the frozen base `04af9bc9` the S073 row is line 79 and the
table ends at line 79; the new row becomes line 80). It must stay inside the
`## Registry` section — the census reports `E12 row outside Registry section` for a
row-shaped line placed elsewhere.

## 1. Registry row (11 cells exactly, no `|` inside any cell)

```
| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side repository security advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side reporting flow, not advisory editing, not the REST API and not the Advisory Database edit flow | body lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt (the whole capture is the page body), sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL); the nine located manifest quotes Q1-Q9 sit at L10, L13, L17, L24, L25 (Q5 and Q6), L26, L31 and L38 | A maintainer drafts the advisory, fixes in a temporary private fork, requests a CVE from GitHub as CNA while the advisory stays private, credits contributors, then publishes with a fix version attached. | mined | 2026-10-29 | 90d | corpus/knowledge/github-repository-security-advisories.md |
```

Cell-by-cell (the contract's 11-cell shape, `CORPUS.md` "SOURCES.md — where a shokunin learns"):

| # | cell | value | note |
|---|---|---|---|
| 1 | id | `S074` | next unused id after S073; no row carries S074 at the base |
| 2 | source | `GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories` | first URL in the cell is the canonical URL (gate H3 `row[1]` URL test) |
| 3 | kind | `docs` | GitHub's own documentation page |
| 4 | tier | `A` | scoped to the maintainer-side advisory lifecycle only |
| 5 | scope | GitHub's own statement of the maintainer-side repository security advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side reporting flow, not advisory editing, not the REST API and not the Advisory Database edit flow | 43 words; the negative half mirrors the S073 scope cell's style |
| 6 | anchor | body lines 1-42 of `corpus/source-snapshots/round-46-a2/S074.txt` … sha256 `1296528d…c278039` (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL); the nine located manifest quotes Q1-Q9 sit at L10, L13, L17, L24, L25 (Q5 and Q6), L26, L31 and L38 | locator `lines 1-42` is inside the snapshot body |
| 7 | teaches | A maintainer drafts the advisory, fixes in a temporary private fork, requests a CVE from GitHub as CNA while the advisory stays private, credits contributors, then publishes with a fix version attached. | 28 words; every clause is a located manifest quote (see §4) |
| 8 | status | `mined` | the entry `corpus/knowledge/github-repository-security-advisories.md` cites it |
| 9 | opened | `2026-10-29` | the manifest's `fetched_utc` date |
| 10 | recheck | `90d` | cadence only — no recency claim |
| 11 | used-by | `corpus/knowledge/github-repository-security-advisories.md` | the F29 entry path the gate names |

## 2. `## Registry changes` bullets to append (pattern of the S073 bullets)

```markdown
- S074 row added: new row (id `S074`, kind `docs`, tier A scoped to GitHub's own statement of the maintainer-side repository security advisory lifecycle only, status mined, opened 2026-10-29, recheck `90d`, used-by `corpus/knowledge/github-repository-security-advisories.md`), anchor pinned to the round-46-a2 capture `corpus/source-snapshots/round-46-a2/S074.txt` (sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines: whole capture is the page body; draft advisory L12, temporary private fork L13, publication after a patch L14, credit L17, GitHub-as-CNA L24, CVE-request/72-hour/keeps-private L25, other-CNA boundary L26, publication visibility L31, fix-version duty L38). Rule-1 Gate quote grounding `teaches` (11 words): "Requesting a CVE identification number doesn't make your security advisory public." (S074.txt:25). Access 2026-10-29 (manifest `fetched_utc` 2026-10-29T20:19:30Z). Registry rows 73 → 74 (R8); no pre-existing row status, recheck or used-by cell changed.
- Capture-directory note (round 46 attempt 2): the S074 capture and its manifest live in the sibling directory `corpus/source-snapshots/round-46-a2/`, not in `corpus/source-snapshots/round-46/`. The attempt-1 capture directory is sha-pinned by the round-46 attempt-1 receipts — `.ufo/waves/round-46/freeze.txt:7` records `manifest-sha256 01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34` and `corpus/instruments/r46-c2-gate.py:61` pins the same digest under `PINS["manifest.json"]`, so `corpus/source-snapshots/round-46/manifest.json` stays byte-identical and keeps serving S073; the new capture is therefore a second directory beside it rather than an edit to the pinned one. The attempt-2 freeze record `.ufo/waves/round-46/attempt2/freeze.txt` pins the new pair separately (`S074-sha256 1296528d…c278039`, `manifest-a2-sha256 46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`).
```

The second bullet is a factual note about where the bytes live; it changes no row cell and
is not an old→new transition on any row. No `status`, `recheck` or `used-by` cell of any
pre-existing row (S001–S073) changes.

## 3. `## Search log` bullet to append (from the ScoutAbsence sweep)

```markdown
- Maintainer-side repository security advisory sweep (round 46, frontier F29); question: does the corpus already hold the maintainer-side advisory lifecycle (draft advisory, private fork, CVE request through GitHub as CNA, credit, publication, fix-version duty) in any knowledge entry, SOURCES row or README admission; where: `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md`, run twice on 2026-10-29 — (a) the frozen base `04af9bc92229232ea5cce8b32bfe59dd969eb26d` exported with `git archive … corpus | tar -x`, (b) the live lane — plus a line-level `-n` re-run of the same pattern and a direct `grep -rn 'S074'` probe; date: 2026-10-29; identified 2 files (identical in both trees), screened 4 line hits, included 1, excluded 3. Included: no held row or entry covers the maintainer-side lifecycle, so the page is admitted as S074 and the new entry `corpus/knowledge/github-repository-security-advisories.md` is the target of that row. Excluded, with reason: the F28 entry's own scope-out notes `corpus/knowledge/github-private-vulnerability-reporting.md:40,43` (the lifecycle pages appear there only as link text, explicitly outside F28's reporter-side scope), the S068 row `corpus/SOURCES.md:74` (a rejected GitHub Advisory Database mirror of an NVD record, not a maintainer-published advisory) and the round-43 search-log bullet `corpus/SOURCES.md:157` (a historical hunt for the claim-package exemplar, a different question). README: 0 matches. Adjacent-held check: S073 reporter-side only, S031 CVE-program CNA rules, S069 Google Cloud VRP — none covers the lifecycle. Stop rationale: the hits are exhausted with saturation — every hit is either the gap's own note or an unrelated scope, so a wider corpus sweep would only re-find the F28 pointer.
```

## 4. Rule-1 grounding for `teaches` (the located quotes)

`teaches` claims four things; each is a manifest quote located in the snapshot body.
Verified present in `corpus/source-snapshots/round-46-a2/S074.txt` (line numbers below
are the file's own line numbers; `source-recheck.py` resolves them):

| teaches clause | quote | line | manifest id |
|---|---|---|---|
| drafts the advisory | "Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project." | 12 | — |
| fixes in a temporary private fork | "Privately collaborate to fix the vulnerability in a temporary private fork." | 13 | Q2 |
| requests a CVE from GitHub as CNA while the advisory stays private | "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers." / "Requesting a CVE identification number doesn't make your security advisory public." | 24 / 25 | Q4 / Q6 |
| credits contributors | "You can give credit to individuals who contributed to a security advisory." | 17 | Q3 |
| publishes with a fix version attached | "Publish the security advisory to alert your community of the vulnerability once a patch is released." / "you should add a fix version to a security advisory prior to publishing the advisory" | 14 / 38 | — / Q9 |

The Rule-1 Gate quote offered for the lesson's `## Gate` section (11 words, inside the
snapshot body): **"Requesting a CVE identification number doesn't make your security
advisory public."** (`S074.txt:25`).

## 5. Out of scope for this seat

The entry file `corpus/knowledge/github-repository-security-advisories.md`, the README
frontier row F29 and the lesson's `## Gate` section belong to other seats. This draft
only supplies the SOURCES.md material. The census therefore reports `E11` for S074 until
the entry lands — that is the expected pre-entry state, not a defect in the row.
