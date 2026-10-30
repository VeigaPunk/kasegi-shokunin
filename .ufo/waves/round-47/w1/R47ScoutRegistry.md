# R47ScoutRegistry — registry-shape verification

Axes: depth:verifiability; coverage. Confidence: high for measured fixture, not an integrated-tree verdict.

## Scope and fixture

Copied the lane `corpus/` into `/fast/scratch/hyaku/kasegi-r47/R47ScoutRegistry/mirror/corpus`. Do-nothing control = that copy unchanged (including frozen round-47 captures but no S075/S076 registry rows). Candidate = identical copy with (i) the three original fenced bullets landed using the inspected `land_bullets` helper, (ii) S076 row, (iii) S075 row, and (iv) S074 status `mined` → `rejected`, used-by → `corpus/lessons/round-46.md`. Rows are **frozen fixture candidates**, taken verbatim from `corpus/instruments/r47-counters-selftest.py:105-124`, not a claim about a later scribe draft. Helpers are at :69-101 and :127-135; original bullets at `corpus/SOURCES.md:122,183-184`.

No F30 entry was created: the requested four registry edits alone reference a file absent from the copied corpus. This produces E11; do not misreport the candidate census as exit 0. No production file, git/index, or shared script was modified. Scratch was removed in `finally`; printed `scratch_removed= True`. No tools installed. Disk guard printed `/fast/scratch/hyaku 54% 376.3G free`, then its top-consumer scan timed out at 30s; free-space output was available before copying.

## Findings

- Do-nothing census: exit **0**, three W04 warnings, no E04.
- Candidate census: exit **1**, four W04 warnings (adds S076), **no E04**, one E11 for absent `corpus/knowledge/zdi-disclosure-policy.md`.
- Do-nothing binding: **records=63 bound=61 unbound=2**, exit **1** (S075/S076 have no rows).
- Candidate binding: **records=63 bound=62 unbound=1**, exit **1**. New rows bind both round-47 records, but rejecting S074 unbinds its preserved round-46-a2 record: `FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2`.

### Every W04 / E04 finding and rule

All commands below emitted W04 for S028 (`docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq`), S029 (`eur-lex.europa.eu/eli/reg/2024/2847/oj/eng`), and S072 (`bughunters.google.com/about/rules/about-this-section`). Candidate additionally emitted W04 for S076 (`docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories`). There were **zero E04 findings** in either run.

Observed rule: `scripts/sources-census.sh:600-604` normalizes the URL; :643-645 warns W04 when an already-seen normalized URL has a different literal scope. :646-649 emits E04 only for same URL+scope, a non-rejected current row, a prior non-rejected row at that scope, and no `supersedes S[0-9]{3}` in current teaches. Thus different scopes still warn even when teaches explicitly supersedes. Existing S072/S070 precedent is recorded at `corpus/SOURCES.md:175`: W04 warning-only, exit 0. Candidate S076 behaves the same **on duplicate handling**; candidate overall exit differs because E11, not W04 or E04.

Binding rule B3 is independent: `corpus/instruments/capture-binding-check.py:337-339` rejects a record whose own row status is `rejected`; it does not follow supersedes. The S072 precedent does not establish that rejecting a row with a preserved manifest record remains bound. This is an observed compatibility gap in the requested S074 flip, not justification to alter pinned historical manifests or suppress the failure.

## Exact receipts

### do-nothing census

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r47/R47ScoutRegistry/mirror/corpus/SOURCES.md
```

Exit: 0

```text
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r47/R47ScoutRegistry/mirror/corpus/SOURCES.md
```

### do-nothing capture-binding

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py --root /fast/scratch/hyaku/kasegi-r47/R47ScoutRegistry/mirror
```

Exit: 1

```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-43 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-45 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-47 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=63 with_url=63 with_fetched_utc=25 with_archival=38 snapshot_dirs=24 manifest_dirs=24 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S075 dir=round-47
FAIL rule=no-row record=S076 dir=round-47
records=63 bound=61 unbound=2
```

### candidate census

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r47/R47ScoutRegistry/mirror/corpus/SOURCES.md
```

Exit: 1

```text
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
file	E11	S075 missing used-by corpus/knowledge/zdi-disclosure-policy.md
```

### candidate capture-binding

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py --root /fast/scratch/hyaku/kasegi-r47/R47ScoutRegistry/mirror
```

Exit: 1

```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-43 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-45 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
MANIFEST round-47 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=63 with_url=63 with_fetched_utc=25 with_archival=38 snapshot_dirs=24 manifest_dirs=24 missing_manifest=0 multi_row_url=5 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2
records=63 bound=62 unbound=1
```

## Limits

This is a bounded registry fixture probe, not a full counter battery, F30 content evaluation, or verification of drafts that landed later. The working corpus copy is the do-nothing control, not a separately exported historical base. No claim that unbound=0 or census exit=0 was established for the candidate. LSP device was unavailable (`read xd://lsp`: “No such tool”); source-rule citations are literal implementation evidence, not semantic reference-server results. No exported contract was changed. Full battery intentionally not rerun; the disclosed 34 pre-freeze mutant survivors remain unresolved by this seat.
