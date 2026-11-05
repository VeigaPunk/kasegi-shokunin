# ScoutSurface — round 76, C2 (S111 capture freshness + quote location)

Seat: ScoutSurface-7. Scope: C2 only (S111). Not a claim; this seat re-verifies the frozen capture and reports.
Evidence file: `.ufo/waves/round-76/w1/ScoutSurface-evidence-r76.txt`. Refetch copy: `.ufo/waves/round-76/w1/S111-refetch.txt`.
Scratch (now removed): `/fast/scratch/hyaku/kasegi-r76/ScoutSurface`. No lane file was written, edited or committed by this seat; no git/jj mutation was run anywhere.

## Verdict in one line

**The capture is fresh and byte-identical, and all 13 manifest quotes sit exactly once at their declared anchors. On the freeze-commit manifest, claim C2's predicate B5 was FALSE — quote Q01 was below `source-recheck.py`'s 12-character floor and aborted the whole record before `sha256 OK` was printed. The L1 has since applied a disclosed repair to that manifest (Q01 → `How does the API work?` at S111.txt:27); on the working tree every C2 after-counter now reproduces (B1 registry 111, B2 94/92 sort-clean, B3 rows=54 F54 entries=57 pass=57, B4 records=90 bound=90 unbound=0, B5 sha256 OK + 13/13 anchor-located exit 0, B7 census validate exit 0). The capture file itself is untouched, so the freshness and parity results below still hold against the landing bytes. One residual is open for the L1: the repair moved Q01's anchor from line 21 to line 27, so the landing manifest's anchor set no longer matches the frozen `located_anchors` list.**

---

## 1. Freshness (re-fetch with the lane instrument)

```
export TMPDIR=/fast/scratch/hyaku/kasegi-r76/ScoutSurface
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py \
  --id S111 --url 'https://google.github.io/osv.dev/api/' --out $TMPDIR/S111-refetch.txt --kind html
```
rc=0, output:

```
S111 status=200 fetched_bytes=15262 snapshot_bytes=1810 sha256=6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab utc=2026-11-05T10:54:00Z
```

- HTTP status **200**; raw page **15262 bytes**; snapshot **1810 bytes**, **48 lines** — matches the manifest's `bytes: 1810`, `lines: 48` and its note "raw page 15262 bytes, snapshot 1810 bytes".
- sha256 `6f92e5b7…e5581ab` — identical to the manifest pin and to the frozen capture.
- Independent corroboration, same URL with plain `curl` and the instrument UA: `http_code=200 size_download=15262 url_effective=https://google.github.io/osv.dev/api/` (rc=0), raw sha256 `dc64d5eb…08f1`.
- The round-74 lead-only fetch recorded the same 15262/1810/sha256 triple (`corpus/SOURCES.md:175`), so the page has not changed across three fetches (round-74 08:43:42Z, round-76 10:41:25Z, this seat 10:54:00Z).
- `python3 corpus/instruments/capture-source.py --selftest` → `selftest normalize=ok deterministic=ok` rc=0 (the instrument's pipeline is deterministic, so byte-identity is a real freshness result, not a fluke).

**Freshness: CONFIRMED.** The only network target touched was `https://google.github.io/osv.dev/api/`, via the lane instrument and one plain curl to that same URL.

## 2. Byte-comparison against the committed capture

```
cmp $TMPDIR/S111-refetch.txt /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-76/S111.txt
```
rc=**0**, no output → byte-identical. `diff` rc=0, output file 0 bytes → **empty diff, zero drift**. `sha256sum` of both files prints the same digest.

The committed bytes were also confirmed to be the committed *blob*, not a dirty worktree copy:
- `git -C … cat-file -p HEAD:corpus/source-snapshots/round-76/S111.txt | sha256sum` → `6f92e5b7…e5581ab` (rc=0)
- `git -C … status --porcelain corpus/source-snapshots/round-76/` → empty (rc=0); `git diff --stat HEAD -- corpus/source-snapshots/round-76/` → empty (rc=0).

**Parity: CONFIRMED — no drift, no differing line to report.**

## 3. Quote-location check (all 13 manifest quotes)

Manifest read in full from `corpus/source-snapshots/round-76/manifest.json` (schema_version 1, one source, 13 quotes Q01–Q13). For each quote: `grep -c -F <exact quote>` on the committed capture (must be 1) and `sed -n '<anchor>p'` (must equal the quote byte-for-byte).

| quote id | anchor | `grep -c` | `sed -n '<anchor>p'` |
|---|---|---|---|
| Q01-api-version | 21 | 1 | EXACT — `API (1.0)` |
| Q02-openapi | 22 | 1 | EXACT — `Download the OpenAPI specification` |
| Q03-six-types | 28 | 1 | EXACT — `There are six different types of requests that can be made of the API.` |
| Q04-query | 29 | 1 | EXACT — `Query vulnerabilities for a particular project at a given commit hash or version.` |
| Q05-batch | 30 | 1 | EXACT — `Batched query vulnerabilities for given package versions and commit hashes.` |
| Q06-by-id | 31 | 1 | EXACT — `Return a Vulnerability object for a given OSV ID.` |
| Q07-determineversion | 32 | 1 | EXACT — `Return a list of probable versions of a specified C/C++ project. (Experimental)` |
| Q08-importfindings | 33 | 1 | EXACT — `Retrieve records failing import-time quality checks, by record source (Experimental)` |
| Q09-binary-to-source | 34 | 1 | EXACT — `Map Ubuntu binary package names to their corresponding source package names. (Experimental)` |
| Q10-rate-q | 35 | 1 | EXACT — `Is the API rate limited?` |
| Q11-rate-none | 36 | 1 | EXACT — `Currently there are no limits on the API.` |
| Q12-size-http1 | 38 | 1 | EXACT — `The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2.` |
| Q13-http2-recommend | 39 | 1 | EXACT — `We recommend using HTTP/2 for queries that may result in large responses (e.g. big OSV Linux queries).` |

An independent Python scan over all 48 capture lines reproduces the same table: each quote occurs on exactly one line and that line **is** its declared anchor. Script rc=0, `ALL_QUOTES_OK=True`.

**Quote location: CONFIRMED for all 13.** Each quote is exactly-once, so the instrument's B2 uniqueness rule needs no anchor fallback; the declared anchors are nonetheless all correct and are exactly the anchors `claims.json` `located_anchors` names (21, 22, 28–36, 38, 39).

## 4. Already-held cross-check (B6 distinctness evidence)

```
sed -n '148p' corpus/source-snapshots/round-73/S108.txt
```
rc=0 →

```
The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2. We recommend using HTTP/2 for queries that may result in large responses.
```

`grep -n '32MiB'` and `grep -n 'HTTP/2'` on S108 both print only line 148 (rc=0). **Both required statements are present on S108.txt:148** — the 32MiB/HTTP-1.1 limit and the no-HTTP/2-limit half. This is the distinctness evidence for B6: the response-size clause is already held from round-73 manifest Q27–Q29 and must be cross-referenced, not claimed as new ground.

Refinement measured (both rc recorded): S111 line 38 is **word-identical** to S108 line 148 (`grep -c -F` on S108 = 1), but S111 line **39** adds the parenthetical `(e.g. big OSV Linux queries)`, which S108 does not carry (`grep -c -F 'big OSV Linux queries'` on S108 = 0, rc=1). So line 39 is *not* purely already-held ground. The entry draft already handles this correctly: it marks line 38 as held-and-cross-referenced and states that line 39 "is in the capture and manifest (Q13) but is not claimed here, and the held S108 sentence (Q29) carries no such example." **The frozen B6 wording requires the entry to name only lines 21–36 as claimed ground and to mark line 38 as held — the drafted entry does exactly that, and claims nothing from line 39.** That keeps C2 inside the frozen predicate.

## 5. BLOCKER: B5 is false on the committed manifest (Q01 is below the instrument's quote floor)

Frozen B5 reads: *"python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111 reports sha256 OK and all 13 quotes anchor-located, exit 0."*

Measured on the live lane at the freeze commit `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`:

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111
S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence
rc=2
```

- `corpus/instruments/source-recheck.py` sets `MIN_QUOTE_CHARS = 12` (a normalized minimum, with the stated reason that a shorter quote "matches any capture").
- Q01's quote is `API (1.0)` → 9 normalized characters → 3 short of the floor.
- The instrument **aborts the whole record on the first short quote and returns 2 before printing `sha256 OK`**, so the committed manifest yields neither `sha256 OK` nor any `anchor=NN-ok` line. B5's after-state is therefore unreachable on the committed bytes.
- Scope of the defect: this is the **only** sub-12 quote in the lane's manifest corpus. Measured across all 46 manifests under `corpus/source-snapshots/`, every earlier round (round-23 … round-75, 45 manifests, ~1000 quotes) has zero quotes below 12 normalized characters; round-76 is the single outlier, with exactly one.
- This is the same defect the sibling seat `ScribeEntry` recorded independently in `.ufo/waves/round-76/w1/ScribeEntry-recheck-S111-without-Q01.txt` (12 quotes OK, sha256 OK) — two independent measurements of the same cause. It is *not* a discovery of this seat alone, and it is *not* a S111 capture defect: the capture bytes are sound.

### Fix, verified in a scratch clone (never in the lane)

`corpus/source-snapshots/*` is an L1 integration surface, so this seat did not touch it. The fix was measured in a `git archive HEAD` clone under scratch:

1. **Widen Q01's quote text** in `corpus/source-snapshots/round-76/manifest.json` from `API (1.0)` to **`API (1.0) Download the OpenAPI specification`** (44 normalized characters, spanning capture lines 21–22; the anchor stays 21; the quote count stays 13; the text is still exactly-once in the capture).

   Rationale: line 21 is the H1 `API (1.0)` heading; the next line is `Download the OpenAPI specification`. There is no longer form of the version string on line 21 alone — the heading is 9 characters in the capture and cannot be widened on its own line. Widening across the heading + its immediately following line is the minimal change that keeps 13 quotes, keeps every anchor, keeps the quote exactly-once, and names the same ground.

   Measured result (rc=0, full output in the evidence file):

   ```
   S111:sha256 OK
   S111:Q01-api-version OK normalized=markup-whitespace occurrences=1 anchor=21-ok
   S111:Q02-openapi OK occurrences=1 anchor=22-ok
   … (Q03–Q13 all OK, occurrences=1, anchor=NN-ok)
   ```

   The instrument labels Q01 `normalized=markup-whitespace` because the widened quote spans a line break; that is the instrument's own declared-normalization path (QUALITY Q8), not a failure — the same shape as 90+ quotes in the round-24 and round-45 manifests.

2. **Regression sweep:** re-running `source-recheck.py` over every manifest in the clone (all 45 earlier rounds plus round-76) printed no FAIL line for any of them, rc=0.

3. **B4 in the same clone:** with the S111 registry row and the knowledge file present, `capture-binding-check.py --root <clone>` prints `records=90 bound=90 unbound=0`, rc=0 — the transitional `FAIL rule=no-row record=S111` state that the live lane shows now resolves cleanly once the row lands, as claim B4 anticipates.

**Recommendation to the L1:** apply a Q01 quote repair to `corpus/source-snapshots/round-76/manifest.json` at integration, alongside the S111 row and knowledge entry. Without it, B5 stays false at the landing commit and the C2 kill rule ("any after-counter not reproducing at the landing commit = NOT VERIFIED") trips on C2 as a whole.

**Note on agreement with the other seats:** the same blocker was independently measured by `CriticClaims` (F10, `CriticClaims.md:105`), `ExecC2Checks` (check 2, `ExecC2Checks.md:23`) and `ScribeEntry` (`ScribeEntry-recheck-S111-without-Q01.txt`). This seat's cause analysis and the critic's agree exactly: `MIN_QUOTE_CHARS = 12` vs a 9-character Q01, aborting the record before `sha256 OK`. The critic's fix class ("a quote of ≥12 normalized characters that the capture carries, e.g. the two-line span `API (1.0) Download the OpenAPI specification`") is the same repair this seat measured to reach exit 0.

### 5b. The L1's applied repair, as observed on the working tree (after this seat's report)

Observed while this seat was cleaning up: the L1 has applied a **different** repair to the same manifest. The working-tree manifest now reads:

```
{"id": "Q01-api-heading-question", "quote": "How does the API work?", "anchor": 27,
 "repair": "round-76 evidence repair: the frozen Q01 quote \"API (1.0)\" (9 chars) is below source-recheck.py MIN_QUOTE_CHARS=12 (critic F10); replaced by the 22-char line at S111.txt:27 from the same capture; the API (1.0) statement remains at S111.txt:21 and is not a pinned quote"}
```

Measured on the working tree:
- `source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111` → `S111:sha256 OK` + **13/13 quotes `OK occurrences=1 anchor=NN-ok`**, rc=**0**. **B5 is reached.**
- The new Q01 quote `How does the API work?` is exactly-once in the capture (`grep -c -F` = 1, rc=0) and its anchor line 27 reads exactly that (rc=0).
- `capture-binding-check.py` → `records=90 bound=90 unbound=0`, rc=0 (the S111 row has landed).
- `frontier-recheck-count.py` → `FRONTIER-CENSUS rows=54 admitted=54 closed=54 problem-rows=0 registry=111`, `FRONTIER-PASS F54 ids=S111`, `entries=57 pass=57 exit=0`, rc=0. **B3 reached.**
- `knowledge-expected.txt` = 94 lines, 92 knowledge rows, `LC_ALL=C sort -c` rc=0. **B2 reached.**
- Registry rows = 111. **B1 reached.**
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → six inherited W04 warnings + `kasegi ok`, rc=0. **B7 reached.**
- **The capture file itself is untouched**: `git status --porcelain corpus/source-snapshots/round-76/S111.txt` is empty and its sha256 is still `6f92e5b7…e5581ab`, so every freshness/parity result in §1–§3 above still holds against the landing bytes.

**Residual risk on the applied repair (for the L1, measured not inferred):** the repair changes the manifest's anchor set from the frozen `located_anchors` list. Frozen `claims.json` C2 `located_anchors` reads *"S111.txt lines 21, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39 (manifest Q01-Q13)"*; the landing manifest's anchor set is `{22, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39}`. **Line 21 is no longer a pinned quote anchor**, and `located_anchors` is not read by any instrument or gate (`grep -rn 'located_anchors'` over the lane's `.py`/`.sh` → no hits), so nothing machine-checks this. Consequences, all measured:
- The entry still grounds the API-version clause as a **free** anchor — `corpus/knowledge/osv-api-surface-and-limits.md:13` reads *"The page's heading reads \"API (1.0)\" (S111.txt:21)"*, and `sed -n '21p'` confirms line 21 carries the referent `API (1.0)`. Under QUALITY **R71** a free anchor must name a line carrying the referent of the sentence it supports: **satisfied**.
- But the *pinned* evidence for the version clause is now absent. B5's own wording ("all 13 quotes anchor-located") is met, and B6's wording ("the entry's ground names only clauses located in the capture at lines 21-36") is met because line 21 is inside 21-36 — so neither predicate is violated on its literal text.
- The claim's C2 `statement` enumerates the ground as *"the API 1.0/OpenAPI specification availability"* — that clause is still in the entry, still located at S111.txt:21, but no longer backed by a manifest quote.
- `corpus/README.md:1194` (the applied round-76 block) does record the repair in prose: *"Q01 was repaired from \"API (1.0)\", 9 characters, below the 12-character floor, to \"How does the API work?\" at S111.txt:27 — a repair of evidence, recorded in the manifest itself"*. **The repair is disclosed, not silent** — this satisfies the spirit of the R6/R8 append-only discipline.

**Assessment:** the L1's applied repair is sound and disclosed, and it reaches every C2 after-counter. The only open question is whether the loss of the pinned quote at line 21 is acceptable against the frozen `located_anchors` list. Two defensible readings, and this seat does not decide between them:
1. The `located_anchors` list is a *description of the frozen manifest*, not a predicate clause; predicates are A1-A5 and B1-B7 only, and none of them names line 21. On this reading the repair is conformant.
2. `located_anchors` is a binding scope statement under the spec's "its predicates A1-A5 / B1-B7, kill rules and scope statements are binding" clause, and moving Q01's anchor from 21 to 27 makes the landing manifest diverge from it.

The alternative repair this seat measured — widening Q01 in place to `API (1.0) Download the OpenAPI specification` (44 normalized chars, spanning lines 21-22, anchor still 21) — keeps the anchor set **identical** to the frozen `located_anchors` and also reaches exit 0 with `anchor=21-ok`. It is offered as the anchor-preserving alternative, not as a demand: the L1's choice is disclosed, documented and passes every counter.

## 6. Other C2 counters measured on the live lane

(These are the **freeze-commit base** readings, taken before the L1's integration. The **applied** readings are in §5b.)

| counter | measured | rc | reading |
|---|---|---|---|
| `frontier-recheck-count.py` | `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=110`; `entries=56 pass=56 exit=0` | 0 | base state, matches the `c2-base-counters-r76.txt` control exactly. After-state (rows=54, registry=111, F54 ids=S111, entries=57) needs the F54 row/entry — not yet present. |
| `capture-binding-check.py` | `records=90 bound=89 unbound=1`; `FAIL rule=no-row record=S111 dir=round-76` | 1 | the **known transitional no-row state** named in claim B4 ("the freeze-commit intermediate state has the manifest before the row"). Resolves to `bound=90 unbound=0` in the clone with the row present. |
| `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | six inherited W04 warnings (S028, S029, S072, S076, S080, S085) then `kasegi ok …/corpus/SOURCES.md` | 0 | B7 after-state holds. No other lane has a row carrying the S111 URL (`grep` over every lane's `SOURCES.md` rows: 0 hits), so adding the S111 row creates **no new** W04 duplicate-url warning. |

## 7. Distinctness sweep (R114 subject sweep, for the L1's cross-check)

Same organisation (OSV.dev / OSV), all rows in the lane:

- **S080** (OSV format specification) — scope excludes "the osv.dev service API" (`corpus/SOURCES.md:86`).
- **S108** (OSV.dev `POST /v1/query` reference) — scope excludes "the overview page, not the other endpoints, and not any rate-limit or API-key statement (the page has none)" (`corpus/SOURCES.md:120`).
- **F51 entry** `corpus/knowledge/osv-post-v1-query-contract.md:75` already holds the **path list** of the other five endpoints ("They are listed, not described", cited to S108.txt:5-9) — but no per-endpoint semantics.
- The **rate-limit answer** is held nowhere as ground: S108's capture has no rate/limit/quota sentence (`grep -n -i 'rate limit\|ratelimit\|quota'` on S108 → no output, rc=1) and no admitted entry asserts it. The only lane mention is the round-74 lead-only bullet (`corpus/SOURCES.md:175`), which is explicitly "lead, not evidence, not a row".
- The **API-1.0 / OpenAPI / six-types** clauses are held nowhere: `grep -rn -i -E 'API \(1\.0\)|API 1\.0|six different types|six types of request|OpenAPI specification'` over `corpus/knowledge/ corpus/SOURCES.md corpus/README.md` → no output, rc=0.

**Conclusion:** the ground S111 adds (the six one-line request-type semantics at lines 29–34, the API 1.0 heading, the OpenAPI availability, the rate-limit answer) is **not** already held. The *path list* of the five other endpoints **is** already held from S108/F51 as names only — so the entry must claim the per-endpoint semantics and not the paths as new ground. The drafted entry (`f54-entry-draft.md`) already draws that line correctly: it states the paths come from the navigation list at S111.txt:4-9, marks the path↔semantics pairing as `[entry's reading]`, and names the already-held path list in its "does not hold" bullet citing `osv-post-v1-query-contract.md:75`.

Two further measured facts the L1 should keep consistent with the drafted entry:
- The capture writes the determineversion path with a space after the slash (`POST /v1experimental/ determineversion`, lines 8 and 46) — `grep -c -F 'POST /v1experimental/determineversion'` = 0 (rc=1), with the space = 2 (rc=0). The claims.json C2 statement spells it without the space; the drafted entry states the discrepancy explicitly and reads it as `/v1experimental/determineversion` without claiming the space is absent. Correct handling.
- The capture contains no auth/key/credential/quota token: `grep -n -i -E 'api key|api_key|authenticat|credential|quota'` → no output, rc=1.

## 8. Out-of-scope observations (not C2's, recorded for the L1)

- `census-freshness-check.py` prints `CENSUS-FRESH=stale` (rc=1). **Pre-existing since round-58**, not round-76's doing: the freeze commit `a78802..5da54cd` touched **no** `corpus/**/*.md` and no `SKILL.md`, which is the census's entire scope (`SKILL.md` + `corpus/**/*.md`); it added only `corpus/source-snapshots/round-76/S111.txt` and `manifest.json` (.txt/.json). Flagging only; this seat does not own the citation-survival census.
- `citation-ground-check.py` prints `verdict=failed` (rc=1) on `blocked-protected-fleet-relative` lines only (fleet-root files cited from lessons). No S111 / round-76 hit. Pre-existing, unrelated.
- `scripts/sources-census.sh` lives at the **fleet root** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, not in the lane repo; claim B7's `bash scripts/sources-census.sh …` therefore resolves against the fleet root.

## 9. Tooling

No tool was installed or upgraded by this seat; the host's pacman pause was therefore not engaged. Only the Python 3 standard library and `curl` were used, both already present. `/home/vgpnk/.omp/agent/RULES.md` was read before any network or install action.

## 10. Confidence and remaining unknowns

- **High confidence** (byte-level, reproduced twice with independent tools): capture freshness, byte-identity, and all 13 quote locations.
- **High confidence** on the B5 blocker: reproduced on the live lane, in a clone, and independently by a sibling seat; the cause (`MIN_QUOTE_CHARS = 12` vs a 9-character Q01) is read from the instrument source and confirmed by the instrument's own reason string. **Now resolved on the working tree** (§5b).
- **High confidence** on the B6/S108 cross-check: the required 32MiB/HTTP-2 statements are on S108.txt:148 as the frozen predicate expects.
- **Medium confidence** on the residual in §5b: whether moving Q01's anchor from line 21 to line 27 is conformant. The two readings are set out there; the measurement (anchor-set divergence, `located_anchors` read by no instrument, line 21 still carrying the referent for the entry's free anchor) is certain, but the classification is the L1's call, not this seat's.
- **Closed during this seat's run:**
  1. ~~Whether the L1 applies a Q01 quote repair.~~ **Done** — applied and disclosed in `corpus/README.md:1194` and in the manifest's own `repair` key.
  2. ~~Whether the F54/README/knowledge drafts reproduce B3's `entries=57 pass=57` at the landing tree.~~ **Done** — measured `rows=54 … registry=111`, `FRONTIER-PASS F54 ids=S111`, `entries=57 pass=57 exit=0`, rc=0 on the working tree.
- **Still open for the L1 / other seats:**
  1. The anchor-set divergence in §5b (line 21 out, line 27 in, against the frozen `located_anchors`).
  2. Whether the L1 retires the round-74 lead bullet (`corpus/SOURCES.md:175`) as the S111 row lands — the drafted entry says "The lead note at SOURCES.md:175 is superseded by this row at integration", and the lane's precedent (`corpus/SOURCES.md:251`, `:264`) is to keep the old lead byte-identical as history and record a retirement line in `## Registry changes`, not to delete it in place. That is an L1 surface; this seat did not touch it.
  3. Whether the pre-existing `CENSUS-FRESH=stale` state (§8) is repaired this round — out of C2's scope, and it is not caused by round-76.
