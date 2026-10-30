# R47ExecS074Flip — S074 disposition draft

Axes: depth:verifiability (exact field-only edit and census rule); coverage (the S074 disposition/log lines needed for D7).

## Exact edited row

Source: `corpus/SOURCES.md:80` (read as the complete raw row). Proposed row, with only status and used-by changed:

```text
| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side flow, advisory editing, the REST API or the Advisory Database edit flow | heading and body prose lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL), sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 | Draft the advisory, fix in a temporary private fork and credit contributors before publication; request the CVE from GitHub as CNA while the advisory is still private, because requesting a CVE does not make the advisory public. | rejected | 2026-10-29 | 90d | corpus/lessons/round-46.md |
```

## Registry-changes log lines

Use these old → new records (per-field, preserving the established round-46 `## Status, recheck and used-by changes (old → new)` convention and its S072/S070 Registry-changes precedent at `corpus/lessons/round-46.md:46-49`):

- S074 status: `mined` → `rejected`.
- S074 used-by: `corpus/knowledge/github-repository-security-advisories.md` → `corpus/lessons/round-46.md`.

The rejection is due to the superseding S076 re-capture; the S074 row is retained as historical provenance, not deleted.

## Census consequence and control

Executed `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch corpus>/SOURCES.md` against a scratch copy of `corpus`, containing the proposed S074 cell changes and a minimal S076 successor row with the same canonical URL and a different scope (teaches begins `supersedes S074 —`). The do-nothing control kept S074 `mined`/old used-by with that same S076 row. Both printed the pre-existing W04 warnings S028, S029, S072, plus `file W04 S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes`; both ended `file ok <scratch SOURCES.md>` and `exit=0`. Thus the shared URL is a **W04, not E04** finding: it has distinct scopes and the successor declares `supersedes S074` (census rule descriptions: `sources-census.sh:24-33`). The S074 status/used-by flip does not remove that expected warning; it remains warning-only.

A preliminary `--file` run without a corpus mirror emitted E11 missing-used-by findings because the scratch path had no adjacent knowledge files; that is a bad control setup, superseded by the complete corpus-copy run above. All scratch was under `/fast/scratch/hyaku/kasegi-r47/R47ExecS074Flip/` and removed before report completion. No shared production files were changed. No build/test/lint, git/jj mutation, or install was performed.

Limit: the scratch S076 row was a minimal census fixture, not the final S076 registry row. The result establishes the URL-pair classification under the described distinct-scope + supersedes condition; the integrated final row still needs the parent’s census/integration check. The two census runs were printed identically; the tool returned clean `file ok`, exit 0.
## Newly reported integration blocker: capture binding

Reviewer R47RevD7 reports an isolated actual-record control: unchanged S074 gives `records=3 bound=3 unbound=0 EXIT=0`; with S074 rejected, `FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2`, `records=3 bound=2 unbound=1 EXIT=1` (receipt: `.ufo/waves/round-47/w1/R47RevD7.receipts.txt`). This conflicts with the requested rejected-status flip: capture-binding-check B3 requires the retained historical manifest record's row to remain anchorable. Preserve the pinned round-46-a2 manifest; recommend keeping S074 mined and documenting explicit supersession, unless L1 intentionally migrates the binding contract. My census fixture only tested `sources-census.sh`; it does not cover or override this binding failure. I did not independently run the reviewer’s binding check.
