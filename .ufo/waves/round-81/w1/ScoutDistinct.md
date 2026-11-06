SCOUT novel=6/6 live_sha_match=yes

# ScoutDistinct — C2 live re-open and paraphrase distinctness (round 81, attempt 1)

Seat: ScoutDistinct (leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze commit `7ad3118c86ee14fde433d73671cc407668533cec` (base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`).
Scratch: `/fast/scratch/hyaku/kasegi-r81/ScoutDistinct` (deleted before yield). No lane tree, corpus, instrument or fleet-repo file was edited; no git/jj writes.

## 0. Summary

| check | result |
|---|---|
| live re-open of the S115 URL | HTTP 200, 16418 bytes downloaded, final URL = requested URL (no redirect) |
| live capture sha256 vs committed `corpus/source-snapshots/round-81/S115.txt` | **identical** — `e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f` (2224 bytes, 44 lines); `diff` empty |
| six pinned quotes, paraphrase test against the 94 admitted entries | **6 novel / 0 restated** |
| declared reject A (:39 case-sensitivity) | **held** — `corpus/knowledge/osv-post-v1-query-contract.md:31` (quotes S108.txt:53). Rule held; the S115-only *example* (`'ghsa'` vs `'GHSA'`) is held nowhere (routed observation O2). |
| declared reject B (:32 experimental-status sentence) | **reject is faithful to the frozen text but its stated ground is "listing", not "holding"** — `osv-post-v1-query-contract.md:75` says the experimental endpoints "are listed, not described"; the status sentence itself is held nowhere in the corpus (routed observation O1, consistent with the same reason used at F55:87 and F56:70). |
| linked "Properties of a High Quality OSV Record" page | `https://google.github.io/osv.dev/data_quality.html` — HTTP 200, 24473 bytes, sha256 `4ea85ac1869c17ded703ca145281a1a5504dad8ed97b144bb4e59dd2c1592776`. **Would be a lead** (round-82 frontier material); no rows added, per instruction. |
| B0 / B8 re-run of the frozen instruments on the frozen bytes | `source-recheck.py` → `S115:sha256 OK` + 6 × `OK occurrences=1 anchor=<n>-ok`, rc 0; `entry-gate.py` → `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok` / `ENTRY-GATE-RESULT pass`, rc 0; `entry-gate.py --selftest` ok |

## 1. Live re-open

```
$ curl -sSL -w '%{http_code} %{size_download} %{url_effective}' \
    https://google.github.io/osv.dev/get-v1-importfindings/ -o $S/live.html
200 16418 https://google.github.io/osv.dev/get-v1-importfindings/
```

The final URL equals the requested URL; no redirect, no 404.

```
$ python3 corpus/instruments/capture-source.py --id S115 \
    --url https://google.github.io/osv.dev/get-v1-importfindings/ \
    --out $S/S115-live.txt --kind html
S115 status=200 fetched_bytes=16418 snapshot_bytes=2224 \
  sha256=e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f \
  utc=2026-11-06T20:25:05Z
```

```
$ sha256sum $S/S115-live.txt corpus/source-snapshots/round-81/S115.txt
e304eb88…6f7f  $S/S115-live.txt
e304eb88…6f7f  corpus/source-snapshots/round-81/S115.txt
$ diff $S/S115-live.txt corpus/source-snapshots/round-81/S115.txt   # no output
```

**live_sha_match=yes.** The page served at 20:25:05Z is byte-identical to the committed capture taken at 20:11:18Z (`corpus/source-snapshots/round-81/manifest.json`, `fetched_utc`), including the raw served size (16418 bytes) the draft entry cites. Live HTML kept at `w1/ScoutDistinct-receipts/live.html`, live snapshot at `w1/ScoutDistinct-receipts/S115-live.txt`.

Independent confirmation of the frozen pins against the committed snapshot (all six, `occurrences=1`, quote verbatim on the anchored line):

| pin | anchor | words | on anchor line | occurrences in snapshot |
|---|---|---|---|---|
| Q01-purpose | 25 | 14 | yes | 1 |
| Q02-audience | 32 | 12 | yes | 1 |
| Q03-not-imported | 34 | 23 | yes | 1 |
| Q04-only-parameter | 36 | 18 | yes | 1 |
| Q05-url-template | 37 | 1 | yes | 1 |
| Q06-source-yaml-name | 38 | 12 | yes | 1 |

Manifest sha256 re-checked: `corpus/source-snapshots/round-81/manifest.json` = `7429df80bf425c8132b1325d0cd3b9e8527323f7e6eb61c31ce8b0774c5c05cf`, matching the value recorded in `.ufo/waves/round-81/claims.json` (`claims[1]/manifest`).

## 2. Paraphrase distinctness, clause by clause

Corpus state used for the test: the **94 admitted entries** = `git ls-files corpus/knowledge/` (94 files; the 95th file on disk is the untracked round-81 draft `osv-importfindings-record-quality-feedback.md`, whose bytes are identical to `.ufo/waves/round-81/w1-input/osv-importfindings-record-quality-feedback.md`, sha256 `2895011e23b38deb04f634398072d70e88ce9dfe878bffe3d64d00af0c371940`).

Subject sweeps over the 94 admitted entries (all **0 hits**): `importfindings`, `source\.yaml`, `home database`, `quality bar`, `import-time`, `quality checks`, `not been imported`, `still considered experimental`, `api\.osv\.dev`, `record provider`, `OSV-Linter`, `New Data Source`, `imports from`, `imported from`, `not imported`, `never imported`, `not published`, `not accepted`, `quality check`, `fails validation`, `upstream publisher`, `own database`, `OSV import`, `import pipeline`, `records that fail`, `path segment`, `only parameter`, `one parameter`, `name value`.

### cl1 purpose (Q01, S115.txt:25) — **novel**
Rule: the endpoint reports a source's records that fail the checks OSV.dev runs at import time.
Nearest admitted relative: `corpus/knowledge/github-advisory-database-curation-semantics.md:54-58` (the GHSA admission table, incl. `:57` "an NVD import only; not checked for validity or completion"). That is a different service (the GitHub Advisory Database), a different actor (GitHub's curators) and a different rule-shape (an import path and its labelling), not OSV.dev's import-time quality gate on a publisher's records. No admitted entry holds the rule in any wording. **novel.**

### cl2 audience (Q02, S115.txt:32) — **novel**
Rule: the endpoint is addressed to the operators of the upstream home databases OSV.dev imports from.
`home database` and `record provider` occur 0× in the 94; every `operator` hit is procedural corpus vocabulary (`corpus/knowledge/claim-gates.md:16`, `corpus/knowledge/operator-queue.md`), unrelated. Closest admitted relative: `corpus/knowledge/github-advisory-database-curation-semantics.md:66` ("eight imported feeds plus a community-contribution channel") — GitHub's own upstream feeds, not OSV.dev home databases. **novel.**

### cl3 not-imported (Q03, S115.txt:34) — **novel**
Rule: a published record below OSV.dev's quality bar is a record OSV.dev has not imported.
`not been imported` / `not imported` occur 0× in the 94. Closest admitted relative: `corpus/knowledge/github-advisory-database-curation-semantics.md:57` — the inverse relation (the record *is* imported from NVD but unchecked). Different service, opposite direction of consequence; no paraphrase. **novel.**

### cl4 only parameter (Q04, S115.txt:36) — **novel**
Rule: the source is the sole parameter and it is carried in the URL, not a body.
Held elsewhere only for other APIs/endpoints: `corpus/knowledge/osv-post-v1-query-contract.md:11` (four top-level query keys), `corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md:37` (the `ecosystem` parameter form), `:45` (the `binary_names` bounds), `corpus/knowledge/openssf-scorecard-api-contract.md:39` (Scorecard's single `publish` body parameter). None states "the only parameter is the source" for this endpoint. **novel.**

### cl5 URL template (Q05, S115.txt:37) — **novel**
Rule: `https://api.osv.dev/v1experimental/importfindings/{source}`.
`api.osv.dev` occurs **0× across all 94 admitted entries**. The four sibling OSV entries hold rules from the *documentation* pages (`google.github.io/osv.dev/…`): `corpus/knowledge/osv-post-v1-query-contract.md:3` (S108), `osv-post-batch-query-contract.md` (S112), `osv-determineversion-cc-library-versioning.md:3` (S113), `osv-ubuntu-binary-to-source-mapping.md:3` (S114). This is therefore the first admitted entry to hold an **osv.dev service URL** template. **novel.**

### cl6 source.yaml name (Q06, S115.txt:38) — **novel**
Rule: the `source` value equals the `name` value in the source's `source.yaml`.
`source.yaml` occurs 0× in the 94 admitted entries; corpus-wide the only occurrences are `corpus/source-snapshots/round-81/S115.txt:38`, the round-81 manifest and the draft itself. Closest admitted relative by vocabulary only: `corpus/knowledge/openssf-scorecard-checks.md:11` and `:90` (`checks.yaml` — a different project file in a different ecosystem) and `corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md:21` (Ubuntu *source package* names, a different sense of "source"). Neither restates the rule. **novel.**

**Tally: 6 novel / 0 restated.** The draft's own Distinctness block (`corpus/knowledge/osv-importfindings-record-quality-feedback.md`, "## Distinctness") is consistent with this verdict, and its subject-sweep claim is accurate for the pre-draft corpus.

## 3. The two declared rejects

### Reject A — the :39 case-sensitivity note → **held**
`corpus/knowledge/osv-post-v1-query-contract.md:31` (grep -n, pasted):
> The name rule: "Package names are matched exactly, except in ecosystems whose registry treats other spellings as the same package:" (S108.txt:54) … Parameter names and values are case-sensitive: "Case Sensitivity: API requests are case-sensitive." (S108.txt:53).

(`S108.txt:53` = `Case Sensitivity: API requests are case-sensitive. Please ensure that you use the correct case for parameter names and values. For example, use ‘PyPI’ instead of ‘pypi’.`) The **rule** the S115:39 note states is genuinely held at `:31`, by the same page text quoted from a sibling capture. Reject A is correct. Observation O2 below covers the one thing F51 does *not* hold.

### Reject B — the :32 experimental-status sentence → **faithful to the frozen text; ground is a listing, not a holding**
`corpus/knowledge/osv-post-v1-query-contract.md:75` (grep -n, pasted):
> - the other endpoints in the page's navigation (POST /v1/querybatch, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are listed, not described.

`S108.txt:7` is `GET /v1experimental/importfindings`, so the bullet does list this endpoint — but it explicitly says the listed endpoints are **not described**. It therefore does **not** hold the sentence "This API endpoint is still considered experimental." (S115.txt:32) nor the feedback request beside it. The manifest note (`corpus/source-snapshots/round-81/manifest.json`, `note`) says the experimental-status sentences are "Not pinned … (F51 :75 already lists the experimental endpoints)", and the draft's "Not claimed" section says the same, in the same words, so **no false statement is made** and no verdict changes. The precedent is exact: the same ground is used by the two sibling experimental-endpoint entries at `corpus/knowledge/osv-determineversion-cc-library-versioning.md:87` (S113.txt:37) and `corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md:70` (S114.txt:33), whose snapshot lines carry the identical sentence (`This API endpoint is still considered experimental.` — verified byte-identical in all three snapshots).

## 4. The linked "Properties of a High Quality OSV Record" page — lead assessment

The nav link was located in the live HTML: `href="/osv.dev/data_quality.html"` → `https://google.github.io/osv.dev/data_quality.html`.

```
$ curl -sSL -w '%{http_code} %{size_download} %{url_effective}' \
    https://google.github.io/osv.dev/data_quality.html -o $S/data_quality.html
200 24473 https://google.github.io/osv.dev/data_quality.html
sha256 4ea85ac1869c17ded703ca145281a1a5504dad8ed97b144bb4e59dd2c1592776
```

**Would it be a lead? Yes** — and it is the strongest uncovered adjacent ground I found. Structure of the page (238 collapsed text lines): title `Properties of a High Quality OSV Record`; `Version 1.0.0 (SEMVER)`; `Purpose` — "Describe the 'good enough' OSV record that will be imported by OSV.dev"; `Out of scope` (bit rot, deferred `ecosystem_specific` validation); `Audience` — "OSV record producers" / "Downstream OSV.dev record consumers"; `Rationale` (the quality bar must be "both defined and sustainably enforced"); then the rule-bearing sections `Valid` (JSON Schema validation prerequisite for the declared `schema_version`), `Precise` (the package-level minimum standard; the `introduced`/`fixed`/`last_affected` event constraints, `package.ecosystem` + identifier prefix, canonical `package.name`, purl conformance, 2xx/3xx reference URLs), `Identifiable` (alias / related / upstream identifiers), `Examples` (GO-2024-2687, OSV-2024-98, DSA-5678-1), and `Appendix A: OSV Schema validation` (schema v1.6.3 field requirements plus the conditional `affected[].ranges[]` validations).

Why it is a lead rather than a duplicate: the 94 admitted entries hold **nothing** from it — `High Quality OSV Record` / `data_quality` occur 0× in `corpus/knowledge/`, `quality bar` 0×, `OSV-Linter` 0×, `precise`/`identifiable` as record properties 0×. Only the nav label `Properties of a High Quality OSV Record` appears in the corpus, as a nav line in the S108/S111/S112/S113/S114/S115 captures (e.g. `corpus/source-snapshots/round-81/S115.txt:14`). Partial overlap to watch: `Appendix A` restates OSV-schema field requirements, which F31 (`corpus/knowledge/osv-affected-range-events.md`, source S080) partly covers; the `Valid`/`Precise`/`Identifiable` properties, the audience/purpose and the reference-URL rule do not. The draft correctly records this as unclaimed (`## Not claimed`, "the quality bar itself … navigation only, which this entry does not open").

**No rows added**, per instruction. Two further adjacent pages observed while reading the nav, reported for routing only (not added, not proposed as rows): `https://google.github.io/osv.dev/data/` (HTTP 200, 27419 bytes — the data-source index) and `https://google.github.io/osv.dev/data/new/rest-api.html` (HTTP 200, 17441 bytes — "Contributing Data via REST API": a REST endpoint serving at least vulnerability ids and date modified, HEAD+GET with Last-Modified, a base URL, the `.json` extension preference, a license URL). Note the bare nav target `/osv.dev/data/new/rest-api` 404s while `…/rest-api.html` returns 200 — a nav-hygiene observation only.

## 5. Routed observations (no verdict change; outside the frozen sets)

- **O1 — the experimental-status rule is held nowhere in the corpus.** `grep -c "still considered experimental"` over the 94 admitted entries = 0. F51:75 lists the experimental endpoints without describing them, and all three experimental-endpoint entries (F55:87, F56:70, and this draft's "Not claimed") decline the sentence for the same reason. The rule is therefore unclaimed corpus-wide. The frozen manifest's choice not to pin it is respected here; the gap is recorded for round 82 (either a home for the sentence or an explicit standing decision that the status line is never a corpus rule).
- **O2 — the case-sensitivity *example* is held nowhere.** F51:31 holds the rule and quotes S108.txt:53, whose example is `'PyPI'` instead of `'pypi'`; S115.txt:39's example is `'ghsa'` instead of `'GHSA'`. The rule is covered, the concrete instance is not. Same routing note as O1.
- **O3 — the draft's subject sweep is no longer literally reproducible.** `grep -rli 'importfindings' corpus/knowledge/` now exits 0 and returns the draft itself (`corpus/knowledge/osv-importfindings-record-quality-feedback.md`), because the draft has been placed in `corpus/knowledge/` (untracked). The claim as written is scoped "before this entry" and is accurate for the pre-draft corpus (re-verified: 0 hits over the 94 tracked files). A reader re-running it today needs `git ls-files corpus/knowledge/` scoping, as used in §2. Verifiability note for the L1's integration, not a claim defect.
- **O4 — the API-surface gap is real and now covered for the first time.** `api.osv.dev` occurs 0× in the 94 admitted entries before this entry; after F57 lands, the corpus holds one `api.osv.dev` URL template. Recorded so that a future round does not read the absence as "the service URLs are covered elsewhere".

## 6. What I ran (and did not run)

Run, read-only, on the committed frozen bytes or on scratch copies of them:
`curl` (3 URLs: the S115 page, `data_quality.html`, `data/`, `data/new/rest-api.html`); `corpus/instruments/capture-source.py --id S115 --url … --out $S/S115-live.txt --kind html`; `sha256sum`; `diff`; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115` (rc 0); `python3 -B .ufo/waves/round-81/c2/entry-gate.py --entry corpus/knowledge/osv-importfindings-record-quality-feedback.md --manifest … --source S115 --lane …` (rc 0, pass) and `--selftest` (rc 0); `git ls-files`, `git status --porcelain`, `git rev-parse HEAD` (read-only).

Not run, by contract: the lane's full gate suite, any C1 counter or forgery driver, any mutation or landing action, any write outside `w1/`. No package installs were needed (curl, git, python3 and coreutils were already present), so no tool/version/channel entry is required.

## 7. Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScoutDistinct.md` (this report)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScoutDistinct-receipts/evidence.txt` (commands, hashes, sweeps, reject anchors)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScoutDistinct-receipts/live.html` (live S115 page, 16418 bytes)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScoutDistinct-receipts/S115-live.txt` (live capture, sha256 e304eb88…6f7f)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScoutDistinct-receipts/data_quality.html` (linked quality doc, 24473 bytes, sha256 4ea85ac1…2776)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScoutDistinct-receipts/curl-stats.txt`, `capture.log`, `dq-stats.txt` (raw instrument output)

Scratch `/fast/scratch/hyaku/kasegi-r81/ScoutDistinct` removed before yield.
