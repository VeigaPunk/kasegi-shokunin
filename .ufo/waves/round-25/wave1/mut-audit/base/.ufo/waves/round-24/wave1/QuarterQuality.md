# QuarterQuality — QUALITY.md gap analysis, round 24

author: L1Kasegi24.QuarterQuality (scout, read-only)
date: 2026-10-25
lane base: `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`; lane tip at review `c2480b143120364728b40397926ffcf30a7309c8`
inputs: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md` (Q1–Q8, R1–R10), `.ufo/waves/round-24/claims.json`, `corpus/lessons/round-23.md` § Mistakes, `corpus/lessons/round-23-verifier-spotcheck.md` § Defects
wrote: this report only. `corpus/QUALITY.md` untouched, no production file edited, no git/jj state changed.

## Verdict

Two criteria are missing for this round's work, and both close a route by which a counter can go
green without the thing it claims. No existing row covers them: Q8 governs *how* a captured quote is
normalized, not *what* it binds (Q9 gap); R10 governs which spellings a matrix *exercises*, not
whether the matrix can *discriminate* an implementation (R11 gap).

- **Q9 (proposed)** — a captured-source assertion must bind the sentence the entry relies on, at the
  location the entry names, to the row id the entry cites. Demonstrated controls below: the rechecker
  exits 0 for a one-word assertion, for an assertion whose `location` field is pure fiction, and for a
  row id pointing at a different source's capture.
- **R11 (proposed)** — a counter whose measuring instrument is minted in the same round freezes that
  instrument and its fixtures *before* the fix, and publishes a uniform-verdict control score through
  the same checker. Frozen claim C1 counter B names a checker absent from the base tree.

Three defect-grade findings need no new row (they are existing-row tightening or bookkeeping), listed
in §4. One positive finding for C1 counter A in §2.5: the round-24 captures **do** bind all 29 claim
quotes of F01–F05 today, so the honest route to 8/8 exists and the gap is only the cheaper route.

## 1. What reproduces today (baseline, from committed bytes)

### 1.1 Counter A is red exactly as frozen

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines \
         authorization-safe-harbor-and-scope ai-assisted-finding-validation \
         cwe-top25-2025-methodology multiparty-vulnerability-coordination \
         cna-assignment-and-vulnerability-rules cra-manufacturer-reporting-duties; do
  r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //')
  bash -c "$r" >/tmp/out 2>&1; echo "$f exit=$?"; tail -1 /tmp/out
done
```

| entry | exit | last line |
|---|---|---|
| cvss-v4-severity-and-vector | 2 | `S001:source UNAVAILABLE reason=not-listed` |
| coordinated-disclosure-timelines | 2 | `S003:source UNAVAILABLE reason=not-listed` |
| authorization-safe-harbor-and-scope | 2 | `S006:source UNAVAILABLE reason=not-listed` |
| ai-assisted-finding-validation | 2 | `S009:source UNAVAILABLE reason=not-listed` |
| cwe-top25-2025-methodology | 2 | `S013:source UNAVAILABLE reason=not-listed` |
| multiparty-vulnerability-coordination | 0 | 7 OK lines |
| cna-assignment-and-vulnerability-rules | 0 | 11 OK lines |
| cra-manufacturer-reporting-duties | 0 | 10 OK lines |

`3/8` — matches `claims.json` counter_A `before_expected` and routed defect 1.

### 1.2 Counter B is red exactly as frozen

```sh
python3 corpus/instruments/resolve-dispatch-check.py \
  --resolver .ufo/waves/round-24/c1-baseline-resolver.py \
  --fixtures corpus/instruments/resolve-dispatch-fixtures.json   # 4/8, exit 1
python3 corpus/instruments/resolve-dispatch-check.py \
  --fixtures corpus/instruments/resolve-dispatch-fixtures.json   # 8/8, exit 0 (working-tree resolver)
```

`resolver_sha256=690153ad…ea2d` (baseline; equals `git show d0a3f6a:corpus/instruments/resolve.py | sha256sum`),
`035f8844…b661` (working tree), `matrix_sha256=5133e98e656f07d2454f1f4799d4b0b5e5ab260ea69b1fd9d1cade3e0f9628b6`,
`checker_sha256=88090efc…b69`. Baseline failures: three `expect=INTERNAL actual=GONE` and one
`actual=INTERNAL path=<CASE>/lane/refs/a-lure.md path_check=path-missing-on-disk`.

### 1.3 Counter B still discriminates a uniform verdict — measured, not asserted

Same checker and fixtures, resolvers whose `classify()` body was replaced line-wise in `/tmp` with a
single return (production bytes untouched):

| implementation | score | exit |
|---|---|---|
| baseline (round-23 bytes) | 4/8 | 1 |
| landed (working tree) | 8/8 | 0 |
| `return "GONE", "", "", ""` (uniform GONE) | **1/8** (only `control-absent-face`) | 1 |
| `return "INTERNAL", lane_root, "literal", "internal"` (uniform INTERNAL) | **6/8** | 1 |

So the matrix *can* tell the target defect from a uniform answer. What no row requires is that this
number ever be **published** as part of the claim's evidence: the fixture file only says so in prose
(`control-absent-face.why`: “A resolver that answers GONE for everything passes only this control and
the one below.”), and the receipt carries no control score. That is the R11 gap.

### 1.4 The measuring instrument of counter B postdates the base tree

```sh
git cat-file -e d0a3f6a:corpus/instruments/resolve-dispatch-check.py
# fatal: path 'corpus/instruments/resolve-dispatch-check.py' exists on disk, but not in 'd0a3f6a'
git log --oneline -1 -- corpus/instruments/resolve-dispatch-check.py       # 0 commits
git log --oneline -1 -- corpus/instruments/resolve-dispatch-fixtures.json  # 0 commits
git status --porcelain   # ?? corpus/instruments/resolve-dispatch-check.py, ?? …fixtures.json, ?? …capture-source.py
```

C1 froze (2026-10-25T00:00Z) a `before_expected: 4/8, exit 1 on frozen baseline resolver bytes` whose
only possible producer is a checker, and a fixture set, authored in the same wave as the resolver
patch. The baseline *resolver* bytes are pinned (`sha256` 690153ad…), the *fixture expectations* are
not: `ResolverPatch` and `LivenessMatrix` are separate, concurrent seats, so "the matrix was frozen
before the fix" is unprovable from committed bytes. R7 as written ("freeze an axis claim against its
registered detector before implementation") did not stop a claim that names a detector file absent from
the tree it froze against.

### 1.5 The round-24 captures do bind the entries' existing claim quotes

29 of 29 claim quotes in F01–F05 are present in `corpus/source-snapshots/round-24/S0xx.txt` under the
Q8 normalization (`<u>` stripped, whitespace collapsed), matched per row line `- S###, <location>: “claim”`
(last quoted span; the location heading is itself quoted and is not a claim):

| entry | claim quotes found | capture ids |
|---|---|---|
| cvss-v4-severity-and-vector | 10/10 | S001, S002 |
| coordinated-disclosure-timelines | 4/4 | S003, S004, S005 |
| authorization-safe-harbor-and-scope | 6/6 | S006, S007, S008 |
| ai-assisted-finding-validation | 5/5 | S009–S012 |
| cwe-top25-2025-methodology | 4/4 | S013–S015 |

`corpus/source-snapshots/round-24/S003.txt` is the guide body, not the landing-page shell: line 200
carries “Establish Reasonable Time Frames for Remediation and Disclosure of Reported”, line 202–203
“A time frame may be a fixed period, a minimum or maximum, or a negotiated default starting point.”,
line 213 “Page 6 of 12”. So C1 counter A is reachable **honestly**; Q9 exists to stop it being reached
by asserting something easier than the entries' sentences.

## 2. Demonstrated controls behind Q9

All three use scratch manifests in `/tmp` over committed snapshots; the checker is
`corpus/instruments/source-recheck.py` unmodified.

### 2.1 A one-word assertion is a passing recheck

```sh
# manifest: {"id":"S031","path":"S031.txt","sha256":"<digest of S031.txt>",
#            "quotes":[{"id":"trivial","quote":"Version"}]}
python3 corpus/instruments/source-recheck.py --manifest /tmp/q24-…/trivial.json --source S031
```
```
S031:sha256 OK
S031:trivial OK
exit=0
```
`quote: " the "` also exits 0. The instrument refuses *zero* assertions (`missing-quotes`, line 90)
and *empty* strings (`empty-quote`, lines 101–103), so the hole is not an assertion-less manifest —
it is an assertion that binds nothing the entry claims. Fifteen such rows would take counter A from
3/8 to 8/8 with no claim sentence captured.

### 2.2 `location` is decorative — the checker never reads it

```sh
grep -n 'location' corpus/instruments/source-recheck.py
# 191:                    "location": "fixture line 1",     <- selftest fixture only
```
Validation (lines 88–103) checks `id` uniqueness and `quote` non-emptiness; matching (lines 134–140)
is `assertion["quote"] in source_text` plus the `normalize()` fallback. A scratch assertion carrying
`"location": "page 99, rule 99.9.9 — never checked"` exits **0**. The production round-23 manifest's
quote records carry only `{'id','quote'}` — the field is not even present:

```sh
python3 -c "import json;m=json.load(open('corpus/source-snapshots/round-23/manifest.json'));
print([sorted(q) for s in m['sources'] for q in s['quotes']][:1])"   # [['id','quote']]
```
The manifest's own `purpose` already discloses the ceiling: “the instrument asserts substring
containment only; quote-to-location binding is human-verified and is not machine-checked”. M15 is what
that ceiling costs: the 24-hour phrase existed in both Article 14 tracks and passed as a substring;
the repair was extra hand-added assertions, not an instrument property.

### 2.3 A row id pointed at another source's capture is a passing recheck

```sh
# manifest row: {"id":"S031","path":"S029.txt","sha256":"<digest of S029.txt>",
#                "quotes":[{"id":"cra-14-2c",
#                  "quote":"no later than 14 days after a corrective or mitigating measure is available"}]}
```
```
S031:sha256 OK
S031:cra-14-2c OK
exit=0
```
S031 is the CVE CNA Rules 4.2.6 PDF (`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:2`);
the asserted sentence is EU CRA Art. 14(2)(c). Nothing compares the manifest row's identity with the
`source:` URL, and nothing compares the entry's `--source` arguments with its `source:` ids. The
receipt proves “these bytes contain these characters”, never “this row is this source”. This is the
literal form of *a capture whose sha256 binds bytes the assertion never touches*: the digest binds
S029's 8 KB correctly and the assertion attributes them to S029's neighbour.

## 3. Proposed rows (exact table shape; append as `## Round-24 additions` at file end — Q1–Q8/R1–R10 untouched, no line shifts)

### 3.1 Q9

| id | criterion | grounded in |
|---|---|---|
| Q9 | A captured-source assertion binds what the entry claims, not merely bytes the capture contains: each assertion names a location the checker resolves (line/offset or anchor) and the receipt prints the occurrence count and the resolved location of the match; a quote occurring more than once passes only with a disambiguating context string; the manifest row's URL is the URL in the entry's `source:` line, and the entry's `recheck:` `--source` ids are exactly its `source:` row ids. An assertion the entry does not rely on is not evidence, even when it exits 0. | `corpus/lessons/round-23.md` M15 — the 24-hour phrase sat in both Article 14 tracks and passed as a substring, repaired by hand-added assertions; round-24 demonstrated controls: `source-recheck.py` exits 0 for `quote:"Version"`, for a fabricated `location`, and for row `S031` bound to `S029.txt` (report §2.1–2.3); `location` is read nowhere but the selftest (line 191) and the round-23 manifest omits it; the sheet's own ceiling sentence in `corpus/source-snapshots/round-23/manifest.json` `purpose`. |

Landing shape, one command: `source-recheck.py` gains occurrence counting (`source_text.count(quote)`
and a `line:` for the match), a `--source`-vs-entry check is a separate tiny gate (`source:` ids parsed
from the entry vs argv), and the manifest row gains `url`, compared to the SOURCES row. Cost: ~15 lines
of checker + `matches=` in each receipt line. Direction of failure: a non-unique quote with no context
string exits 1, as M15 would have.

### 3.2 R11

| id | criterion | grounded in |
|---|---|---|
| R11 | A counter measured by a lane-authored checker that is itself new this round freezes the checker and its fixture matrix (sha256 both) in the claims file or a committed receipt **before** the fix lands, and the final receipt publishes a uniform-verdict control score — an implementation answering one class for everything — through the same checker, shown below the pass threshold. A `before` produced by a checker first written beside the fix measures the fixtures, not the difference. | R7 was not enough: r24 C1 froze a `before_expected` naming `corpus/instruments/resolve-dispatch-check.py`, absent at base (`git cat-file -e d0a3f6a:…` → fatal); `corpus/lessons/round-23.md` M17 + R10 — `AddHocAbsForm`/`MatrixFreezeOrder` mutants passed the unchanged 13-case matrix; measured controls this round: baseline 4/8, uniform-GONE 1/8, uniform-INTERNAL 6/8, landed 8/8 (report §1.3–1.4). |

Landing shape, one command: add `uniform-GONE` and `uniform-INTERNAL` implementations to the receipt
(`--control` mode of `resolve-dispatch-check.py`, ~10 lines: copy the resolver, replace the `classify`
body, score), and record `checker_sha256`+`matrix_sha256` in `claims.json` at freeze. Both numbers must
be in the receipt or the counter does not count.

## 4. Defect-grade findings that need no new row

| # | finding | evidence | existing row it tightens |
|---|---|---|---|
| D1 | F01–F05 `recheck:` lines are cwd-dependent; F06–F08 self-locate after the r23 `F-RA-1` repair, F01–F05 were left behind. Run from `/tmp`: `can't open file '/tmp/corpus/instruments/source-recheck.py'`, exit 2 (a *different* failure than `not-listed`); from the lane root: `S001:source UNAVAILABLE reason=not-listed`, exit 2. Counter A's command is therefore reproducible only from one undeclared directory. | `grep -m1 '^recheck: ' corpus/knowledge/cvss-v4-severity-and-vector.md` (starts `python3 corpus/…`) vs `…/multiparty-vulnerability-coordination.md` (starts `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`); run from `/tmp` and from the lane root, both exit 2 with different text. | Q7 — one clause: “a published recheck runs from any directory; it begins with its own `cd`”. Fix while the entries are being re-pointed anyway. |
| D2 | The round's three new instruments are outside the corpus index — the r23 erratum recurring. | `grep -c 'capture-source\|resolve-dispatch' corpus/README.md corpus/instruments/README.md` → `0` and `0`; `corpus/README.md:35` lists only the r23 additions; `corpus/lessons/round-23.md` errata §Indexing records the same omission last round. | R2/R3 (self-description, instrument of record) — an index row per instrument + receipt path. |
| D3 | C2 counter B (`grep -lE '^source: S1[0-9][0-9] ' …`) counts *ids*, not new authority. A row registered under a fresh `S1xx` id whose URL already has a row moves the counter while adding no grounding; the census calls that a warning, not an error. | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 with `W04 S028 duplicate url …` and `W04 S029 duplicate url …`; counter B today `0`. | R8 covers corrected anchors and supersession, not duplicate new ids. Recommendation (not a new row): newly admitted rows must carry a URL with no existing row, or `supersedes S###`; then W04 for a new id is an error. |

## 5. Non-gaps — do not mint these

- **Normalization** is Q8's, already implemented (`normalize()` strips `<u>`/`</u>`, collapses
  whitespace, receipt prints `normalized=markup-whitespace`). Q9 does not restate it.
- **Fixture spelling coverage** is R10's; the C1B matrix already carries the absolute-arm and
  brace-expansion cases that r23's mutants proved missing. R11 adds *discrimination*, not coverage.
- **Failing controls** are Q7's; the r23 `c2-controls.txt` three-way control (digest 1, missing 2,
  fabricated quote 1) still satisfies it.
- **Do-nothing control** is present in the claim (`before_expected`), reproduces, and cannot meet
  either after-target. Nothing to add.
- **`quotes: []`** already fails closed (`missing-quotes`, exit 2) — an “assertion-less manifest” in the
  literal sense is not the hole; the hole is §2.1.

## 6. UNVERIFIED

- The round-24 manifest does not exist yet (`corpus/source-snapshots/round-24/` holds S001–S015 `.txt`
  only, no `manifest.json`), so whether it will assert the entries' 29 claim quotes — as opposed to 15
  convenient ones — cannot be checked. `CaptureTool`'s prompt asks for exactly-once 5–25 word
  assertions; the checker does not enforce exactly-once, so that requirement is currently a seat
  instruction, not an instrument property.
- Faults in the two degenerate resolvers are mine (`classify` body replaced in `/tmp`); I did not run
  any sibling seat's report, and no admission judgment is made here.
- Whether `ResolverPatch` landed before or after `LivenessMatrix` wrote the fixtures is unprovable from
  committed bytes (both untracked); I record the absence, not an accusation of ordering.

Tooling: none installed or upgraded this round.
