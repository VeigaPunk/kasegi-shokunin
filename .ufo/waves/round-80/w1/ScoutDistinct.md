# ScoutDistinct — C2 B6 paraphrase half + live re-open (round 80, attempt 1)

Seat: ScoutDistinct (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Frozen bytes read-only: `corpus/source-snapshots/round-80/manifest.json`, `corpus/source-snapshots/round-80/S114.txt`.
Nothing in the lane tree was edited by this seat. Scratch `/fast/scratch/hyaku/kasegi-r80/ScoutDistinct` was removed on exit.

---

## 1. Live re-open record

### 1.1 Fetch of the claimed page

| item | value |
|---|---|
| requested URL | `https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/` |
| HTTP status | **200** |
| bytes downloaded | **18769** |
| final URL (`url_effective`) | `https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/` — **identical to the request, no redirect** |
| body sha256 (live) | `71944736668ff6a16d858fab6b5a6a96a956168d071db2d194726e8a0f620fe1` |
| body sha256 with the capture instrument's own UA (`kasegi-shokunin/1.0 …`) | identical — `71944736668ff6a16d858fab6b5a6a96a956168d071db2d194726e8a0f620fe1` (server serves the same bytes to both UAs) |
| manifest's recorded raw size | 18769 bytes (`corpus/source-snapshots/round-80/manifest.json`, `fetched_utc` 2026-11-06T19:42:42Z) — **matches the live fetch byte count** |
| live re-open time | 2026-11-06 ~19:48–19:51Z (same day as the capture) |

### 1.2 Determinism of the capture (strongest verifiability result)

Re-running the lane's own capture pipeline (`corpus/instruments/capture-source.py` → `html_to_text` → `collapse`) over the **live** bytes yields:

```
raw_bytes 18769  snap_bytes 2365  sha256 e1ccfb9bd13bb3f9a077feb60ae5d738ccb47bc85f630aef9a7a5776ca8788d2
```

which is **byte-identical to the committed frozen snapshot** `corpus/source-snapshots/round-80/S114.txt`
(sha256 `e1ccfb9bd13bb3f9a077feb60ae5d738ccb47bc85f630aef9a7a5776ca8788d2`, 2365 bytes, 73 lines).
Verified twice: over the default-UA body and over the instrument-UA body — same sha256 both times, and `live == frozen` byte comparison is **True**.
So the page is unchanged since the freeze and the capture is deterministic: the six pinned quotes are re-derivable from the live page by the lane's own instrument, with no hand-editing.

### 1.3 The six quotes against the live text

Text was produced by a `html.parser` tag stripper (block-level tags → newline, `<script>/<style>` dropped, entities decoded) plus per-line whitespace collapse — the same normalisation the capture instrument performs. Each quote was then searched in (a) the whitespace-normalised flat text and (b) the instrument-normalised live snapshot, line by line.

| pin | quote (abbrev.) | in live flat text | occurrences | live snapshot line | manifest anchor | anchor match |
|---|---|---|---|---|---|---|
| Q01-purpose | "Map Ubuntu binary package names to their corresponding source package names." | **yes** | **1** | 25 | 25 | **OK** |
| Q02-source-indexing | "Ubuntu vulnerability advisories in OSV are indexed by source package name rather than binary package name." | **yes** | **1** | 35 | 35 | **OK** |
| Q03-scanner-use | "allowing callers such as scanners to query OSV using the resulting source package names." | **yes** | **1** | 35 | 35 | **OK** |
| Q04-ecosystem-forms | "The Ubuntu release ecosystem (e.g. Ubuntu:24.04, Ubuntu:24.04:LTS, or Ubuntu:Pro:24.04:LTS)." | **yes** | **1** | 38 | 38 | **OK** |
| Q05-binary-names-limit | "A non-empty array of Ubuntu binary package names (maximum 1000 per request)." | **yes** | **1** | 39 | 39 | **OK** |
| Q07-unmapped-empty-object | "with an empty object {} for binary package names that have no known source package mappings in that Ubuntu release" | **yes** | **1** | 58 | 58 | **OK** |

All six occur **exactly once** in the live text, and each lands on the **same snapshot line** as its manifest anchor. The frozen `controls/c2-prerecheck-r80.txt` receipt (six `OK occurrences=1 anchor=<n>-ok` lines, rc=0) is reproduced independently: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-80/manifest.json --source S114` run from a foreign cwd (`/tmp`) printed `S114:sha256 OK` + the six anchor-OK lines, **rc=0**.

**Verifiability trap worth recording (falsifiable, one command):** in the **raw HTML** the Q04 and Q07 strings occur **0** times — they are broken by inline `<code class="…">` markup (`Ubuntu:24.04</code>, <code…>Ubuntu:24.04:LTS</code>`, `an empty object <code…>{}</code>`). The other four occur once even in raw HTML. Any future recheck that greps the served bytes instead of the instrument-normalised text will report a false miss on Q04 and Q07.

### 1.4 The second URL (the r79 lead's path name)

```
curl -o /dev/null -w '%{http_code} %{url_effective}' https://google.github.io/osv.dev/post-v1experimental-ubuntu-binary-to-source/
→ 404  https://google.github.io/osv.dev/post-v1experimental-ubuntu-binary-to-source/
```
HTTP/2 404 from the GitHub Pages edge (`x-github-request-id: 3C60:1454F7:1459B:15E03:6AEE2CC6`), no redirect to the working slug. **Confirms** the round-79 lead's path name is not the page's address and that the working URL in the manifest, the S114 registry row and the L1 draft is the correct one.

### 1.5 Side observation (source-side naming asymmetry)

The live page's own H1/breadcrumb reads `POST /v1experimental/ubuntu/binary-to-source` while the URL slug is `post-v1-ubuntu-binary-to-source` (the slug drops "experimental"). The registry URL and the manifest `capture_url` both use the slug form, which is the one that returns 200 — no action needed, but the entry should not be read as claiming the slug mirrors the endpoint path.

### 1.6 Corroborating live fetch (not required, but decisive for §2 Q01)

`https://google.github.io/osv.dev/api/` → **HTTP 200, 15262 bytes**, and the live page still carries the binary-to-source listing (1 hit). The committed capture of that page (`corpus/source-snapshots/round-76/S111.txt:34`) reads:

> `Map Ubuntu binary package names to their corresponding source package names. (Experimental)`

and the round-76 manifest pins it as `Q09-binary-to-source` (anchor 34). Stripping the trailing ` (Experimental)` makes it **verbatim identical to Q01**. See §3 finding R-81-A.

---

## 2. Per-clause paraphrase classification against the 93 admitted entries

Method: literal containment of each pinned quote over `corpus/knowledge/*.md` **excluding the new entry** (93 files), then 2–4 paraphrase keyword sets per clause with `file:line` hits, then a reading of each hit to decide whether it is *the same rule about the same endpoint*.

**Literal containment (independent recomputation): 0 files for all six pins.** Each pin occurs in **0 of the 93** admitted entries — matching the frozen control `controls/c2-prerecheck-r80.txt` ("zero 6 of 6 knowledge files 93").

**Subject sweeps (R114, run before classification):**
- `grep -rli -i 'ubuntu' corpus/knowledge/` → **0 hits** among the 93 (only the new entry matches once it exists); in `corpus/SOURCES.md` only the S114 row itself (`:126`) and the round-80 provenance note (`:276`).
- `grep -rli -i 'osv' corpus/knowledge/` (excluding the new entry) → 7 admitted entries: `osv-affected-range-events.md` (F31), `osv-post-v1-query-contract.md` (F51), `osv-post-batch-query-contract.md` (F54), `osv-determineversion-cc-library-versioning.md` (F55), `openssf-scorecard-checks.md` (F35), `github-advisory-database-curation-semantics.md`, `fuzzilli-js-engine-fuzzing-framework.md`. Each read below.

### Per-clause table

| clause | pin | paraphrase keyword sets used | admitted-entry hits (file:line) | why the hit is **not** the same rule about the same endpoint | verdict |
|---|---|---|---|---|---|
| **Q01 purpose** — map Ubuntu binary package names → source package names | S114.txt:25 | `ubuntu`; `binary package`; `source package`; `binary.to.source` | `ubuntu` → **0 hits**; `source package` → `osv-affected-range-events.md:30` ("describing vulnerabilities in open source packages", S080.txt:9-10); `binary package` → 0; `binary.to.source` → 0 | `:30` is the OSV **format's own scope sentence** ("open source packages" = the open-source ecosystem, S080), not a binary→source **name-mapping** rule and not about any endpoint | **novel** (but see **R-81-A**: an identical sentence is already a *pinned manifest quote* on the queued source S111) |
| **Q02 source-name indexing** — Ubuntu advisories in OSV are indexed by source package name, not binary package name | S114.txt:35 | `index(ed\|ing) by`; `source package`; `advisor(y\|ies) .*index`; `binary package` | `index(ed\|ing) by` → **0 hits**; `advisor(y\|ies) .*index` → **0 hits**; `source package` → `osv-affected-range-events.md:30` (format scope, see above) | The nearest *name* rule is F51 `osv-post-v1-query-contract.md:29,31` — how a **query request's** package name is matched (exact, three registry exceptions). That is a matching rule about `POST /v1/query`, not an **indexing key** for Ubuntu advisories, and not about this endpoint | **novel** |
| **Q03 scanner use** — the endpoint's output is what a scanner then queries OSV with | S114.txt:35 | `scanner`; `osv-scanner`; `query OSV` | `scanner` → `openssf-scorecard-checks.md:36,38` (`osv-scanner.toml` suppression); `csaf-vex-product-status-and-justifications.md:16` ("not a scanner"); `intake-surface.md:104` (lane's own intake scanner); `submitted-registry.md:148` | F35 `openssf-scorecard-checks.md:36-38` is the **Scorecard programme's** own `osv-scanner.toml` suppression mechanism — a different subject, a different service and a different endpoint. It does not state that binary→source **results** are what a scanner queries OSV with | **novel** |
| **Q04 ecosystem forms** — `Ubuntu:24.04`, `Ubuntu:24.04:LTS`, `Ubuntu:Pro:24.04:LTS` | S114.txt:38 | `Ubuntu:`; `release ecosystem`; `ecosystem.*(LTS\|Pro)`; `ecosystem` | `Ubuntu:` → **0 hits**; `release ecosystem` → **0 hits**; `ecosystem` → `github-global-security-advisories-rest-api.md:50,65,66` (a closed list of 13 ecosystems for a **different** REST API), `osv-affected-range-events.md:84,96,109` (the OSV format's `ECOSYSTEM` type semantics), `osv-post-v1-query-contract.md:29` (three registry-name exceptions) | The GitHub row enumerates **language registries** for the GitHub Global Security Advisories API; the F31 rows are the **format spec's** ecosystem comparison semantics; F51's is name matching on `POST /v1/query`. **No admitted entry names an Ubuntu *release* ecosystem string, LTS or Pro.** No admitted entry states the *forms* of this endpoint's `ecosystem` parameter | **novel** |
| **Q05 binary_names bounds** — non-empty array, maximum 1000 per request | S114.txt:39 | `maximum of 1000`; `max(imum)? 1000`; `1000 (packages\|names\|per)`; `non-empty` | `maximum of 1000` → `github-global-security-advisories-rest-api.md:54` ("A maximum of 1000 packages can be specified.", S103.txt:308-311); `1,000` → `osv-post-batch-query-contract.md:37,39,41,75` (F54) and `osv-post-v1-query-contract.md:47,51` (F51); `non-empty` → only lane-internal entries (`claim-gates.md`, `claim-package-*.md`, `triage-thresholds.md`) | The GitHub row's "maximum of 1000 packages" is the **same numeral and the same request-size rule-shape**, but on a **different service and different endpoint** (GitHub Global Security Advisories REST API, `affects` parameter). F54's 1,000/3,000 and F51's 1,000 are **counts of vulnerabilities returned**, a different quantity from "binary package names per request". No admitted entry bounds this endpoint's `binary_names` | **novel** (but see **R-81-B**: the *closer* numeral analogue is F36/F47's GitHub row, which the draft's rejected-over-generalization for Q05 does not name) |
| **Q07 unmapped name → empty object** | S114.txt:58 | `empty object`; `\{\}`; `empty (result\|array\|object)`; `unmapped` | `empty object` → **0 hits**; `unmapped` → **0 hits**; `\{\}` → only lane-internal JSON defaults (`triage-thresholds.md:71,366`) | `triage-thresholds.md` occurrences are the lane's own receipts/lease defaults, unrelated. F54 `osv-post-batch-query-contract.md:19` holds the **input-matched ordering** rule-shape for `POST /v1/querybatch` — a *different endpoint*; the draft deliberately claims only the empty-object clause of S114.txt:58 and does not re-claim the ordering clause | **novel** |

**Summary:** 6 of 6 clauses classify **novel** against the 93 admitted entries; **0** are held, **0** are partly-held. No clause restates admitted ground, so the B6 kill-rule clause ("a B6 paraphrase finding that a claimed clause restates admitted ground") is **not** triggered by anything I found in the admitted corpus.

---

## 3. Routed findings (findings outside the frozen table — defects for round 81; no verdict change here)

### R-81-A (coverage, medium) — Q01 is verbatim identical to an already-pinned quote on the **queued** source S111

- `corpus/source-snapshots/round-76/manifest.json` → source `S111`, quote `Q09-binary-to-source`, anchor 34:
  `"Map Ubuntu binary package names to their corresponding source package names. (Experimental)"`
- `corpus/source-snapshots/round-80/S114.txt:25` (Q01): `"Map Ubuntu binary package names to their corresponding source package names."`
- Stripping the trailing `" (Experimental)"` from the S111 quote yields a string **exactly equal** to Q01 (checked programmatically: `q111.replace(' (Experimental)','') == q01` → `True`).
- S111's registry row (`corpus/SOURCES.md:123`) is status **queued**, used-by **—**: it has a committed capture and pinned manifest quotes but **no admitted entry** (`grep -rn 'S111' corpus/knowledge/` → 0 hits). Therefore it is **not** admitted ground, and the letter of predicate B6 ("none restates admitted ground") is **not** violated by it.
- But R114 (distinctness by subject) and R125 (inspect admitted entries *as well as source navigation captures*) point the other way: the round-80 entry's Distinctness section (`w1-input/osv-ubuntu-binary-to-source-mapping.md:59-65`) records the `ubuntu` literal sweep and the F51/F54/F55/F31 neighbours, and does **not** record that S111 already pins the identical purpose sentence. When S111 is later admitted, two entries will both claim the purpose clause of the same sentence.
- The S113/F55 precedent does **not** cover this: S111's determineversion line is `"Return a list of probable versions of a specified C/C++ project. (Experimental)"`, a *different* sentence from S113's Q01 (`"Given the source code hashes of C/C++ libraries, this endpoint attempts to find the closest upstream library and version."`), so F55 had no duplicate-sentence problem — F56 does.
- **Route:** round 81 / L1. Either add an explicit cross-reference in the F56 Distinctness section (S111 holds the same purpose sentence as a pinned, unmined quote; S111's own entry must not re-claim it), or route S111's admission to state that the clause stays with F56. No change to the C2 verdict on the frozen bytes.

### R-81-B (coverage, low) — the Q05 rejected-over-generalization names only F54, not the closer numeral analogue F36/F47

- `w1-input/osv-ubuntu-binary-to-source-mapping.md:49` rejects "the 1000 limit is the same per-queryset limit as the batch query endpoint" and cites only `corpus/knowledge/osv-post-batch-query-contract.md:37`.
- The closer analogue — same numeral, same request-size rule-shape, different service — is `corpus/knowledge/github-global-security-advisories-rest-api.md:54`: *"A maximum of 1000 packages can be specified."* (S103.txt:308-311). F54's 1,000/3,000 are vulnerability **counts returned**, so they are a weaker foil than a "1000 packages per request" bound on another API.
- The clause itself remains **novel** (different endpoint), so this is a completeness gap in the Distinctness narrative, not a distinctness failure.
- **Route:** round 81 / L1 — extend the Q05 rejected-over-generalization to name the GitHub 1000-packages row alongside F54.

### R-81-C (depth:verifiability, low) — Claim 6's falsifiable rule leans on the ordering clause the entry explicitly does not claim

- `w1-input/osv-ubuntu-binary-to-source-mapping.md:55`: *"a caller that reads a missing `source_names` key as an error, **or that drops empty objects and then pairs the remaining results with its input names**, misreads S114.txt:58"*.
- The second half of that rule ("pairs the remaining results with its input names") presupposes the **input-matched ordering** clause — the leading clause of S114.txt:58, which the same entry lists under "Not claimed" (`:69`) and which F54 holds as a rule-shape for `POST /v1/querybatch` (`osv-post-batch-query-contract.md:19`). The pinned quote Q07 covers only the empty-object clause.
- The empty-object fact alone still falsifies "dropping empty objects" (the mapping is lost), so the rule is not wrong; but its *stated* consequence is grounded in an unpinned, unclaimed sentence on the same line.
- **Route:** round 81 / L1 — either ground the ordering premise explicitly as borrowed-from-F54 rule-shape (as the "Not claimed" paragraph already does for the clause itself), or narrow the rule to the empty-object clause.

### R-81-D (coverage, low, informational) — "held" for the experimental-status paragraph is a listed-not-described argument

- `w1-input/osv-ubuntu-binary-to-source-mapping.md:69` declines the S114.txt:33 experimental-status paragraph on the grounds that *"F51's Limits bullet already lists the experimental endpoints"* (`corpus/knowledge/osv-post-v1-query-contract.md:75`).
- That bullet says the navigation endpoints are *"listed, not described"*; it does not state an experimental-status rule for this endpoint. S108.txt:9 does list the path `POST /v1experimental/ubuntu/binary-to-source`, so the path string is already-held ground — but "the endpoint is still considered experimental" as a *statement* is not held by any admitted entry (`grep -rniE 'considered experimental|still experimental' corpus/knowledge/` → only F55's own "Not claimed" line at `osv-determineversion-cc-library-versioning.md:87`).
- This is **conservative** (declining a clause is safe) and matches the F55 precedent exactly, so it is not a distinctness failure; it is a wording precision note.
- **Route:** round 81 / L1 — reword as "the path string is already-held listed-not-described ground (F51:75 / S108.txt:9); the status sentence itself is unclaimed by any admitted entry".

---

## 4. Commands run (all read-only over committed bytes or scratch)

| command | result |
|---|---|
| `curl -sSL -w '%{http_code} %{size_download} %{url_effective}' https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/` | 200 / 18769 / final URL == requested |
| same, with the capture instrument's UA | 200 / 18769 / same body sha256 |
| `curl -o /dev/null -w '%{http_code}' https://google.github.io/osv.dev/post-v1experimental-ubuntu-binary-to-source/` | **404** |
| `curl -sSL https://google.github.io/osv.dev/api/` | 200 / 15262 (corroborating fetch for §1.6) |
| `html.parser` tag strip + whitespace collapse over the live body | 89 lines; all six quotes found |
| `corpus/instruments/capture-source.py` → `html_to_text` over the live body | 2365 bytes, sha256 `e1ccfb9b…88d2` == frozen S114.txt, byte-identical |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-80/manifest.json --source S114` (run from `/tmp`) | `S114:sha256 OK` + 6 anchor-OK lines, rc=0 |
| literal containment of the six pins over `corpus/knowledge/*.md` excluding the new entry | 0 files for each of 6 pins (93 files scanned) |
| paraphrase sweeps (`ubuntu`, `binary.to.source`, `binary_names`, `source package`, `binary package`, `1,000`, `1000`, `maximum of 1000`, `empty object`, `unmapped`, `Ubuntu:24.04`, `release ecosystem`, `ecosystem`, `scanner`, `index(ed\|ing) by`, `ordering`, `experimental`, `v1experimental`) over `corpus/knowledge/*.md` | hits recorded with `file:line` in §2 |
| `grep -rli -i 'ubuntu'` / `grep -rli -i 'osv'` over `corpus/knowledge/` and `corpus/SOURCES.md` | R114 subject sweeps, §2 |
| manifest-wide quote-overlap sweep over all `corpus/source-snapshots/*/manifest.json` | only overlap outside round 80: S111 `Q09-binary-to-source` ⊃ Q01 (§3 R-81-A) |
| `git -C <lane> show 4ab5458…:corpus/SOURCES.md`, `git log`, `git diff --stat` (read-only) | freeze commit 4ab5458 is HEAD; S114 row already flipped `queued→mined` in the working tree, used-by = the new entry; registry rows 114 at freeze and now |
| `ls corpus/knowledge/*.md \| wc -l` = 94; `corpus/instruments/knowledge-expected.txt` 96 lines / 94 `.md` rows; set equality vs the listing | exact set equality (no diff) |

No git/jj write of any kind was performed (no commit, add, stash, checkout, reset, push, fetch, pull, bookmark, rebase, abandon). No file in the lane tree outside `.ufo/waves/round-80/w1/` was created or modified. No subagent was dispatched. No tool was installed.
