# ScoutSurface — round 74 w1 — per-surface reconnaissance for C2 (F52 / S109) distinctness and capture integrity

Seat: ScoutSurface (scout, leaf — no subagent dispatch).
Round: 74, attempt 1, lane kasegi. Freeze commit `847b53792d2d29d161cad7d21a33c89df9e52e8d`.
Host: linux, `curl`/`python3` only. No tools installed or upgraded this wave (nothing needed; all checks used in-tree instruments and stock `curl`).
Scratch root used: `/fast/scratch/hyaku/kasegi-r74/ScoutSurface` (created, `TMPDIR` exported explicitly for the in-tree instruments; deleted before this report was written — see §7).
Working directory for every command: the seat's own scratch dir or an explicit `cd` into the lane root; the fleet root was never written to.

**Bottom line for the L1: no HELD clause. All six content clauses are DISTINCT, the capture re-fetches byte-identical, and the OSV lead bullet's two statements are confirmed verbatim on the live page. Two non-blocking observations are recorded in §6 (the SOURCES.md Fuzzilli lead bullet is still parked as "unopened" and must move or be retired when F52 lands; the round-74 snapshot directory has no `manifest.json` yet, so `capture-binding-check.py` currently FAILs `missing-manifest dir=round-74` and the C2 `capture` after-predicate `records=88 bound=88 unbound=0 exit 0` requires the L1 to add the round-74 manifest with the ≥10 S109 quotes).**

---

## 1. Scope read

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-74/claims.json` read in full (64 lines), including the C2 block with `distinctness_screen` and `scope_limit` (the `target` string was read raw at `:37` because the first read truncated it at 768 chars). Binding clauses used verbatim below:

- C2 target: admit Frontier F52 — the Fuzzilli project's own primary documentation ground — on source S109 (`https://github.com/googleprojectzero/fuzzilli`, capture `corpus/source-snapshots/round-74/S109.txt`), with one knowledge entry citing S109.
- C2 `distinctness_screen`: `F41_S093` (Project Zero's comparison post) — DISTINCT; `F40_S092_F42_S094` — DISTINCT; `F31_S080` — DISTINCT; `siblings` — DISTINCT (connector seat re-verifies); `pre_freeze_quote_locus` — L151, L165, L212, L214-L221, L226-L227, L230, L233+L236, L154-L156, L243.
- C2 `scope_limit`: "the project's own README/documentation statements only; not Project Zero's comparison post (S093/F41), not Big Sleep (S092/F40, S094/F42), not the NDSS 2023 paper's content (existence and name only), not any listed CVE's specifics (only that the README lists bugs found with Fuzzilli), and no live fuzzing (live-target testing stays refused)".

---

## 2. Capture integrity — S109 re-fetch

Re-fetched the pinned URL with the lane's own instrument, then byte-compared against the frozen snapshot.

```
$ export TMPDIR=/fast/scratch/hyaku/kasegi-r74/ScoutSurface
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 corpus/instruments/capture-source.py --id S109 --url https://github.com/googleprojectzero/fuzzilli \
      --out $S/S109-refetch.txt --kind html
S109 status=200 fetched_bytes=347611 snapshot_bytes=19630 sha256=c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486 utc=2026-11-05T08:42:52Z out=/fast/scratch/hyaku/kasegi-r74/ScoutSurface/S109-refetch.txt
exit=0
```

```
$ cmp -s $S/S109-refetch.txt .../corpus/source-snapshots/round-74/S109.txt ; echo $?
0
$ sha256sum $S/S109-refetch.txt .../corpus/source-snapshots/round-74/S109.txt
c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486  .../S109-refetch.txt
c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486  .../corpus/source-snapshots/round-74/S109.txt
$ wc -l -c  (both)
375 19630   (both files)
```

- `cmp` exit **0** — the re-fetch is **byte-identical** to the frozen capture; there are **no differing lines at all**, so the "mutable counters" allowance in the seat spec did not need to be invoked.
- Re-fetch sha256 `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486` = the sha256 frozen in `claims.json` (C2 `capture` predicate) = the sha256 of the committed file. **No digest difference.**
- Both files are 375 lines / 19630 bytes, matching the claim's "375 lines".
- Copy of the re-fetch kept as evidence: `.ufo/waves/round-74/w1/ScoutSurface-S109-refetch.txt`.

Frozen-capture provenance confirmed against the freeze commit (read-only git):

```
$ git -C <lane> rev-parse 847b5379...:corpus/source-snapshots/round-74/S109.txt
423a73fbc6b348b37d5525349638eb3752810e01
$ git -C <lane> hash-object corpus/source-snapshots/round-74/S109.txt
423a73fbc6b348b37d5525349638eb3752810e01
$ git -C <lane> ls-tree 847b5379... corpus/source-snapshots/round-74/
100644 blob 423a73fbc6b348b37d5525349638eb3752810e01   corpus/source-snapshots/round-74/S109.txt
$ git -C <lane> diff --stat ccd6a54b... 847b5379... -- corpus/
 corpus/source-snapshots/round-74/S109.txt | 375 +++++
```

The worktree file, the freeze-commit blob and the base→freeze diff all agree: the capture was committed at the freeze commit and is unmodified in the worktree. The `round-74/` snapshot directory did **not** exist at the base revision (`git ls-tree ccd6a54b... corpus/source-snapshots/ | grep -c round-74` → `0`), so the capture is a pure addition at freeze.

### URL form probe

```
$ for u in https://github.com/google/fuzzilli https://github.com/googleprojectzero/fuzzilli; do
    curl -s -o /dev/null -w '%{http_code}' -L --max-time 30 -A 'kasegi-shokunin/1.0 (documentation capture)' "$u"; done
https://github.com/google/fuzzilli -> 404
https://github.com/googleprojectzero/fuzzilli -> 200
```

- `https://github.com/google/fuzzilli` → **HTTP 404** (confirmed, matches the observed 404 in the seat spec).
- `https://github.com/googleprojectzero/fuzzilli` → **HTTP 200**, `num_redirects=0`, `url_effective` identical to the requested URL (`curl -w 'http_code=%{http_code} num_redirects=%{num_redirects} effective=%{url_effective}'` → `http_code=200 num_redirects=0 effective=https://github.com/googleprojectzero/fuzzilli`, exit 0). **The lead URL's canonical form is the `googleprojectzero` path**; the `google/` path is a 404 and must not be used as a registry URL.

---

## 3. Distinctness screen — per clause

### 3.1 The clause ground, located in the capture

Each of the six frozen content clauses was located in `corpus/source-snapshots/round-74/S109.txt` by line, and a ≤25-word quote candidate was confirmed present at that anchor line (word counts computed with `len(q.split())`):

| Clause | Frozen locus | Verified in capture | Quote candidate (≤25 words) | Words | Located |
|---|---|---|---|---|---|
| L151 definition / FuzzIL | L151 | `A (coverage-)guided fuzzer for dynamic language interpreters based on a custom intermediate language ("FuzzIL") which can be mutated and translated to JavaScript.` | `A (coverage-)guided fuzzer for dynamic language interpreters based on a custom intermediate language ("FuzzIL")` | 14 | ✅ L151 |
| L165 semantic correctness | L165 | `When fuzzing for core interpreter bugs, e.g. in JIT compilers, semantic correctness of generated programs becomes a concern. …` | `semantic correctness of generated programs becomes a concern` | 8 | ✅ L165 |
| L165 (contrast half) | L165 | `… semantic correctness can easily be worked around by wrapping the generated code in try-catch constructs.` | `semantic correctness can easily be worked around by wrapping the generated code in try-catch constructs` | 15 | ✅ L165 |
| L212 Swift/C split | L212 | `The fuzzer is implemented in Swift, with some parts (e.g. coverage measurements, socket interactions, etc.) implemented in C.` | (whole line) | 18 | ✅ L212 |
| L214-L221 architecture components | L214-L221 | `A fuzzer instance (implemented in Fuzzer.swift) is made up of the following central components:` then `MutationFuzzer:` L215, `ScriptRunner:` L216, `Corpus:` L217, `Environment:` L218, `Minimizer:` L219, `Evaluator:` L220, `Lifter:` L221 | per-component one-liners at L215/L216/L217/L220/L221 | 10/7/11/14/10 | ✅ all located |
| L226-L227 Storage + event-driven | L226-L227 | `Storage: stores crashing programs to disk.` / `The fuzzer is event-driven, with most of the interactions between different classes happening through events.` | as quoted | 6 / 15 | ✅ |
| L230 REPRL | L230 | `Fuzzilli uses a custom execution mode called REPRL (read-eval-print-reset-loop). … execute it, then reset its internal state and wait for the next script.` | `Fuzzilli uses a custom execution mode called REPRL (read-eval-print-reset-loop).` | 9 | ✅ L230 |
| L233+L236 tree hierarchy | L233, L236 | `To scale, fuzzer instances can form a tree hierarchy, in which case they report newly found interesting samples and crashes to their parent node.` / `… one root instance, 16 intermediate nodes connected to the root, and 256 "leaves" connected to the intermediate nodes.` | as quoted | 22 / 18 | ✅ |
| L154-L156 Targets/ + patches + clang | L154-L156 | `See the Targets/ directory for the list of supported JavaScript engines.` / `Apply the corresponding patches from the target's directory.` / `Compile the engine with coverage instrumentation (requires clang >= 4.0)` | as quoted | 11 / 8 / 10 | ✅ |
| L243 NDSS 2023 | L243 | `A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers.` | as quoted | 16 | ✅ |

Every `pre_freeze_quote_locus` line in `claims.json` is confirmed present in the capture at the stated line. All candidate quotes are ≤25 words (max 22), so a manifest can satisfy the "each ≤25 words" clause using these strings.

### 3.2 Screen of the HELD corpus

Screened files (all present, `ls` confirmed):
`corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` (F41/S093) · `corpus/knowledge/google-big-sleep-findings-tracker.md` (F40/S092) · `corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md` (F42/S094) · `corpus/knowledge/osv-affected-range-events.md` (F31/S080) · `corpus/README.md`.

Pattern sweep over exactly those five files (`grep -nEi <pat> <five files>`, exit 1 = no match):

| Clause | Patterns swept | Result |
|---|---|---|
| L151 definition / FuzzIL | `FuzzIL`, `intermediate language`, `coverage-guided`, `dynamic language`, `guided` | **No match** in the five files except `coverage-guided` in F41's own title line (`knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:1`) and `corpus/README.md:1005` — see 3.3. |
| L165 semantic correctness | `semantic correct`, `try-catch`, `interpreter` | **No match** for `semantic correct` or `try-catch`; `interpreter` matches only `osv-affected-range-events.md:6` (the recheck command line), `:70` ("interpretation"), `:74` ("interpreted") — unrelated to fuzzing. |
| L212 Swift/C split | `Swift`, `implemented in Swift` | **No match.** |
| L214-L221 architecture components | `MutationFuzzer`, `ScriptRunner`, `Corpus:`, `Minimizer`, `Lifter`, `Evaluator`, `event-driven` | **No match** for any component name. The single `Evaluator` hit (`corpus/README.md:815`) is the NVD schema row's `evaluatorComment`/`evaluatorSolution` fields — a different sense, not Fuzzilli's `Evaluator` component. |
| L226-L227 Storage / event-driven | `Storage`, `event-driven` | **No match.** |
| L230 REPRL | `REPRL`, `read-eval-print` | **No match.** |
| L233/L236 tree hierarchy | `tree hierarchy`, `root instance`, `interpreter` | **No match** for `tree hierarchy` or `root instance`. |
| L154-L156 Targets/ + instrumentation | `Targets/`, `coverage instrumentation`, `clang` | **No match.** |
| L243 NDSS 2023 | `NDSS` | **No match.** |

Broader sweep over the **entire** kasegi held corpus (`corpus/knowledge/`, `corpus/README.md`, `corpus/SOURCES.md`) with the same clause-specific strings returned **no match** for `FuzzIL` (case-sensitive), `REPRL`, `read-eval-print`, `MutationFuzzer`, `ScriptRunner: executes programs`, `Lifter: translates`, `custom intermediate language`, `semantic correctness of generated programs`, `tree hierarchy, in which case`, `implemented in Swift`, `NDSS Symposium 2023`, `root instance, 16 intermediate nodes`. The Fuzzilli hits returned by the case-insensitive `FuzzIL` sweep are the word **Fuzzilli** inside the F41 entry — a substring artifact of `-i`, not the intermediate-language term.

The S093 capture itself (`corpus/source-snapshots/round-60/S093.txt`) was also swept for the clause terms: **no** `REPRL`, `read-eval-print`, `MutationFuzzer`, `ScriptRunner`, `Lifter`, `Minimizer`, `implemented in Swift`, `semantic correct`, `tree hierarchy`, `NDSS`. It names Fuzzilli only as "a JavaScript engine fuzzer" (S093.txt:22) / "a generative JavaScript engine fuzzer" (S093.txt:16) and compares it with BigSleep.

### 3.3 Per-clause verdict

| Clause | Verdict | Basis |
|---|---|---|
| L151 definition / FuzzIL | **DISTINCT** | FuzzIL, "custom intermediate language", "dynamic language interpreters" appear nowhere in the held corpus. F41's own title (`knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:1`) and the registry row (`corpus/README.md:1005`) call Fuzzilli "a coverage-guided … fuzzer" — that is the *adjective*, carried by the Project Zero comparison post's characterisation, not the tool's own README self-description and not the FuzzIL intermediate-language ground. `claims.json`'s own screen already states F41's scope limit keeps the Fuzzilli method out. The adjective overlap is noted for the L1's entry wording (§6.1) but it is **not** the L151 clause ground, so it is not a HELD verdict. |
| L165 semantic correctness | **DISTINCT** | No occurrence of `semantic correctness` / `try-catch` in any held file. |
| L212 Swift/C split | **DISTINCT** | No occurrence of `Swift` in the five screened files. |
| L214-L221 architecture components | **DISTINCT** | No occurrence of any of MutationFuzzer / ScriptRunner / Corpus / Environment / Minimizer / Evaluator / Lifter as Fuzzilli components. |
| L230 REPRL | **DISTINCT** | `REPRL` and `read-eval-print` occur nowhere in the held corpus (nor in the S093 capture). |
| L233/L236 tree hierarchy | **DISTINCT** | `tree hierarchy` / `root instance` occur nowhere in the held corpus. |
| F40/F42 (S092, S094) | **DISTINCT** | Big Sleep tracker and SQLite case are a different system; no fuzzer-mechanism ground. |
| F31 (S080) | **DISTINCT** | OSV format ranges — unrelated. |

**No clause is HELD. No claim-narrowing finding is raised against C2.**

---

## 4. Sibling scan

```
$ grep -ril fuzzilli /home/vgpnk/Projects/shokunin/*-shokunin/corpus /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md 2>/dev/null
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/knowledge-expected.txt
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-60-verifier-spotcheck.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-60.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-61.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-73.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-60/S093.txt
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-60/manifest.json
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-74/S109.txt
exit=0
```

**Every hit is inside kasegi.** No sibling repo names Fuzzilli in its corpus or SKILL.md.

Fuzzer-adjacent holdings in siblings, checked for competing ownership of fuzzer-tool documentation ground (`grep -rilE 'fuzzer|fuzzing|fuzzilli|coverage-guided'` per sibling, then the match inspected in context):

- **kengaku** — two hits, both inside a *fetched evidence file* (`corpus/evidence/round53/fetched/C1PriceL1-general-best-practices.html`, `C1PriceScoutD-…html`), where "the fuzzer" is a quoted third-party reviewer's remark about a different artifact. Not a kengaku-held fuzzer-tool ground.
- **revenger** — holds the strongest fuzzer-tool ground of any sibling: `S117` DecFuzzer (ISSTA'20 artifact README, tier A, `corpus/SOURCES.md:132`), `S243` icicle-emu README (`:258`), `S395` Trail-of-Bits differential-fuzzing post (`:410`), `S396` trailofbits/mishegos differential fuzzer for x86 decoders (`:411`). All four are **binary-decompilation / x86-decoder fuzzing**, not a coverage-guided interpreter fuzzing tool; none names Fuzzilli, FuzzIL, REPRL or a JS-engine fuzzer. A clause-fact sweep of revenger's corpus for `FuzzIL|REPRL|read-eval-print|MutationFuzzer|ScriptRunner|googleprojectzero` returns only the word **"lifter"** (its binary-lifting rows, e.g. `SOURCES.md:133`, `:138-140`, `:143`) — a different sense from Fuzzilli's `Lifter` component. **No overlap.**
- **tameshi** — holds `S024` The Fuzzing Book §Delta Debugging (tier B, reducer practice, `corpus/SOURCES.md:35`) and the knowledge entry `corpus/knowledge/delta-debugging-minimization-contract.md:2`; its Leads list `C-Vise`, `HypoFuzz`, "Fuzzing with Agents?" (unopened). This is **input-reduction / delta-debugging method ground**, a different technique from a coverage-guided interpreter fuzzer's own documentation. Its `ScriptRunner` hit (`corpus/knowledge/webmcp-completion-lifecycle-round-20.md:38`) is `V8ScriptRunner::ReportException` in a Chromium WebMCP lifecycle trace — a different symbol entirely.
- **mori** — kernel `Documentation/admin-guide/kernel-parameters.txt` occurrences of "fuzz" (Linux kernel fuzzing knobs). Unrelated.
- **tabi** — Chromium `html_form_element.cc` "fuzz" in a checked-out browser source blob; `SKILL.md` and one knowledge entry name `V8ScriptRunner`. Unrelated to Fuzzilli.

**Conclusion: no sibling owns fuzzer-tool documentation ground that overlaps F52's six clauses.** kasegi's only existing Fuzzilli holding is via **S093** (Project Zero's comparison post, F41) — exactly as the seat spec expected — which `claims.json`'s scope_limit already excludes from C2's ground.

Sibling clause-fact sweep, for the record:
```
$ for d in /home/vgpnk/Projects/shokunin/*-shokunin; do grep -rilE 'FuzzIL|REPRL|read-eval-print|MutationFuzzer|ScriptRunner|\bLifter\b|googleprojectzero' $d/corpus $d/SKILL.md $d/PROVINCE.md; done
```
→ hits only in `revenger-shokunin` (`lifter`, binary-lifting sense) and `tabi-shokunin` (`V8ScriptRunner`, Chromium symbol); every hit outside `corpus/` and `SKILL.md` (strace logs, `.jj/` op-stores, wave scratch) was inspected and is incidental (`reprlib.py` in strace output; `open()`/`read()` syscall names in `.jj` operation records). **No sibling holds any of the six clauses' ground.**

---

## 5. OSV overview page — lead-only, unopened-as-row

Fetched with the lane's own instrument and with plain `curl`; both conversions agree byte-for-byte.

```
$ curl -sSL --max-time 40 -A 'kasegi-shokunin/1.0 (documentation capture)' \
    -o $S/osv-api-overview.html -w 'http_code=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    https://google.github.io/osv.dev/api/
http_code=200 bytes=15262 url=https://google.github.io/osv.dev/api/
curl_exit=0
$ date -u '+fetch_date_utc=%Y-%m-%dT%H:%M:%SZ'
fetch_date_utc=2026-11-05T08:43:42Z
```

```
$ python3 corpus/instruments/capture-source.py --id OSVLEAD --url https://google.github.io/osv.dev/api/ \
      --out $S/osv-api-overview.snapshot.txt --kind html
OSVLEAD status=200 fetched_bytes=15262 snapshot_bytes=1810 sha256=6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab utc=2026-11-05T08:43:58Z out=.../osv-api-overview.snapshot.txt
exit=0
```

- **Fetch date:** 2026-11-05 (UTC), 08:43:42Z (curl) / 08:43:58Z (instrument).
- **Bytes:** 15262 raw HTML fetched; 1810 snapshot bytes after the instrument's html→text conversion (48 lines).
- **sha256 of the converted text:** `6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab` — identical for the instrument's snapshot and an independent local conversion of the same raw HTML (both files 48 lines / 1810 bytes), i.e. the conversion is reproducible.

The two statements the round-73 spotcheck named (`corpus/lessons/round-73-verifier-spotcheck.md:94` — "Live page states 'Currently there are no limits on the API' and a 32 MiB HTTP/1.1 limit"), **lead-only, unopened-as-row** — line numbers are in *my fetch* (the converted text; the raw HTML is a single 15262-byte line, so the raw file carries both sentences at line 1):

| # | Exact quote (my fetch) | Line in my fetch |
|---|---|---|
| 1 | `Currently there are no limits on the API.` | **L36** of `$S/osv-api-overview.snapshot.txt` (also L36 of the independent conversion) |
| 2 | `The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2.` | **L38** of `$S/osv-api-overview.snapshot.txt` (also L38 of the independent conversion) |

Surrounding context lines in the same fetch: L35 `Is the API rate limited?`, L36 (quote 1), L37 `Are there any response size limits?`, L38 (quote 2).

- Evidence kept: `.ufo/waves/round-74/w1/ScoutSurface-osv-api-overview-snapshot.txt` (converted, 1810 B) and `.ufo/waves/round-74/w1/ScoutSurface-osv-api-overview-raw.html` (raw, 15262 B).
- **This is a lead, not a row and not evidence.** The URL `https://google.github.io/osv.dev/api/` is **not** in `corpus/SOURCES.md` today (`grep -n 'osv\.dev/api' corpus/SOURCES.md` → exit 1, no match), so the R73-V2 lead bullet is still to be added by the L1; the two statements above are the material for it. Note the round-73 spotcheck's own recorded decision (item 3, "reject (not captured, no row; Residual 2)") still holds: no row, no capture record, no evidence use.
- Scope caution for the L1's bullet wording: the page also carries the HTTP/2 no-limit half of quote 2; the F51 entry's scope limit (`PROVINCE.md`, r73 amendment) excludes "the overview page's rate-limit or size statements" from F51's ground, so the bullet must stay a lead and must not be cross-referenced as F51 evidence.

---

## 6. Findings for the L1 (non-blocking, no claim-narrowing)

**6.1 — The SOURCES.md Fuzzilli lead bullet is still parked as "unopened" and must move with the admission.**
`corpus/SOURCES.md:172` currently reads:
`- Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.`
The lead has now been opened (capture committed at freeze; §2). When F52 lands, this lead bullet needs a disposition — retired into the S109 row, or re-worded — otherwise the registry carries a lead for a source the lane has already opened. (The `## Leads (unopened)` heading is at `corpus/SOURCES.md:170`.) This is a wording/consistency item for the integrator; the seat spec's scope for me is reconnaissance only.

**6.2 — The round-74 snapshot directory has no `manifest.json` yet, so the C2 `capture` after-predicate currently cannot hold.**
Run at the freeze tip:
```
$ python3 corpus/instruments/capture-binding-check.py --scratch $S/cbc-scratch | tail -3
FAIL rule=missing-manifest dir=round-74
records=87 bound=87 unbound=0
exit=1
```
The C2 `capture` predicate is "capture-binding-check.py: records=88 bound=88 unbound=0 exit 0 (base 87); manifest corpus/source-snapshots/round-74/manifest.json pins >=10 quotes for S109, each <=25 words, each located at its anchor line in the capture whose sha256 is c9a7…486". So the L1 must add `corpus/source-snapshots/round-74/manifest.json` with one `sources[]` record for S109 carrying `url`/`capture_url`/`http.status`/`http.final_url`/`kind`/`fetch_method`/`fetched_utc`/`path`/`sha256`/`bytes`/`lines` and **≥10 quotes**. The record shape is in `corpus/source-snapshots/round-73/manifest.json` (single-source, `sources[]` list, each quote `{id, quote, anchor}`); the binding rules the checker enforces are in `corpus/instruments/capture-binding-check.py` (A1/A2 manifest presence + per-file binding, B1-B5 URL binding to the registry row).
Ready-made quote candidates that satisfy "≤25 words and located at its anchor" are in §3.1 — the table gives 19 candidate strings, each verified present at its anchor line, all ≤22 words. A ≥10-quote set is therefore available without re-deriving anything.
Note also: the base counter receipt `.ufo/waves/round-74/controls/c2-base-counters-r74.txt` records `records=87 bound=87 unbound=0` at the *base* revision (before `round-74/` existed), consistent with the `87 → 88` delta in the claim.

**6.3 — Base-state counters re-verified read-only at the freeze tip (no drift since the freeze).**
```
$ python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|entries='
FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108
…
entries=54 pass=54 exit=0
frontier_exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   → 108
$ ls corpus/knowledge/*.md | wc -l                                        → 89
$ grep -c 'S109' corpus/SOURCES.md                                        → 0   (exit 1)
$ grep -qE '^\|[[:space:]]*S109[[:space:]]*\|' corpus/SOURCES.md           → exit 1 (no row)
$ grep -n 'F52' corpus/README.md corpus/SOURCES.md                        → no match
$ grep -n 'fuzzilli' corpus/instruments/knowledge-expected.txt
71:corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
$ wc -l corpus/instruments/knowledge-expected.txt   → 91   ; grep -vc '^#' → 89
```
These match the frozen do-nothing control exactly (`.ufo/waves/round-74/controls/c2-base-counters-r74.txt`: rows=51, entries=54, records=87, registry=108, knowledge=89, F52 absent, S109 absent). **S109 does not collide with an existing id** (no `S109` token anywhere in `corpus/SOURCES.md`). `corpus/README.md` carries F50 at `:1145` and F51 at `:1159`, and **no F52 row** — so the landing must add the F52 frontier row to `corpus/README.md` and the F52 entry to `corpus/instruments/knowledge-expected.txt` (base 91 lines / 89 non-comment rows → 92 / 90 after, per the claim).

**6.4 — `knowledge-expected.txt` base row count.** The claim's `knowledge` predicate says "92 lines / 90 non-comment rows". The base file is 91 lines with 89 non-comment rows (`grep -vc '^#'` → 89; the `c2-base-counters-r74.txt` receipt records `91` / `89`). 91+1 = 92 and 89+1 = 90, so the claim's after-values are consistent with the base — the delta is exactly the one new entry. No discrepancy to report.

---

## 7. Command + exit log (every number above)

All commands ran with cwd = the seat scratch dir or an explicit `cd` into the lane root; `TMPDIR` was exported explicitly to `/fast/scratch/hyaku/kasegi-r74/ScoutSurface` for every in-tree instrument invocation.

| # | Command | Exit | Result used above |
|---|---|---|---|
| 1 | `mkdir -p /fast/scratch/hyaku/kasegi-r74/ScoutSurface` | 0 | scratch created |
| 2 | `read .ufo/waves/round-74/claims.json` (full; `:37` raw) | 0 | C1/C2 blocks, distinctness_screen, scope_limit |
| 3 | `python3 corpus/instruments/capture-source.py --id S109 --url https://github.com/googleprojectzero/fuzzilli --out $S/S109-refetch.txt --kind html` | 0 | status=200, 347611 fetched, 19630 snapshot, sha256 c9a7…486, utc 2026-11-05T08:42:52Z |
| 4 | `cmp -s $S/S109-refetch.txt corpus/source-snapshots/round-74/S109.txt` | **0** | byte-identical, no differing lines |
| 5 | `sha256sum` (both files) | 0 | identical c9a7…486 |
| 6 | `wc -l -c` (both files) | 0 | 375 lines / 19630 bytes each |
| 7 | `curl -w '%{http_code}' -L https://github.com/google/fuzzilli` | 0 | **404** |
| 8 | `curl -w '%{http_code}' -L https://github.com/googleprojectzero/fuzzilli` | 0 | **200** |
| 9 | `curl -w 'http_code=… num_redirects=… effective=…' -L https://github.com/googleprojectzero/fuzzilli` | 0 | 200 / 0 redirects / effective == requested |
| 10 | `sed -n '<line>p' corpus/source-snapshots/round-74/S109.txt` × 11 loci | 0 | L151/154/155/156/165/212/214-221/226/227/230/233/236/243 text recorded in §3.1 |
| 11 | python3 candidate-quote presence + word-count script (19 candidates) | 0 | all present at anchor, ≤22 words |
| 12 | `grep -nEi <20 patterns> <five held files>` | 1 where no match | §3.2 table |
| 13 | `grep -rnEi <12 clause strings> corpus/knowledge/ corpus/README.md corpus/SOURCES.md` | 1 (no match) | whole-corpus sweep, §3.2 |
| 14 | `grep -nEi <10 patterns> corpus/source-snapshots/round-60/S093.txt` | 1 (no match) | S093 carries none of the clause terms |
| 15 | `grep -ril fuzzilli /home/vgpnk/Projects/shokunin/*-shokunin/corpus /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md 2>/dev/null` | 0 | 11 hits, all kasegi |
| 16 | per-sibling `grep -rilE 'fuzzer\|fuzzing\|fuzzilli\|coverage-guided' $d/corpus $d/SKILL.md $d/PROVINCE.md` | 0/1 | kengaku, mori, revenger, tabi, tameshi — each inspected in context (§4) |
| 17 | per-sibling clause-fact sweep `FuzzIL\|REPRL\|…` over corpus/SKILL.md/PROVINCE.md | 0 | revenger `lifter`, tabi `V8ScriptRunner` — both different senses |
| 18 | `curl -sSL -o $S/osv-api-overview.html -w 'http_code=… bytes=… url=…' https://google.github.io/osv.dev/api/` | 0 | 200 / 15262 bytes / effective == requested |
| 19 | `date -u '+fetch_date_utc=…'` | 0 | 2026-11-05T08:43:42Z |
| 20 | `python3 corpus/instruments/capture-source.py --id OSVLEAD --url https://google.github.io/osv.dev/api/ --out $S/osv-api-overview.snapshot.txt --kind html` | 0 | 200 / 15262 fetched / 1810 snapshot / sha256 6f92…1ab / utc 08:43:58Z |
| 21 | `grep -n 'no limits on the API' \| grep -n '32MiB'` on both conversions | 0 | **L36** and **L38** in both |
| 22 | `sha256sum` on both conversions + raw html | 0 | 6f92…1ab (both conversions), dc64…8f1 (raw) |
| 23 | `grep -n 'osv\.dev/api' corpus/SOURCES.md` | **1** (no match) | the OSV lead bullet is not yet in the registry |
| 24 | `grep -n 'Fuzzilli project' corpus/SOURCES.md` | 0 | lead bullet at `:172` |
| 25 | `python3 corpus/instruments/capture-binding-check.py --scratch $S/cbc-scratch` | **1** | `FAIL rule=missing-manifest dir=round-74`; records=87 bound=87 unbound=0 (§6.2) |
| 26 | `python3 corpus/instruments/frontier-recheck-count.py` | 0 | FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108; entries=54 pass=54 exit=0 |
| 27 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 | 108 |
| 28 | `ls corpus/knowledge/*.md \| wc -l` | 0 | 89 |
| 29 | `grep -c 'S109' corpus/SOURCES.md` | 1 | 0 — no S109 token, no id collision |
| 30 | `grep -qE '^\|[[:space:]]*S109[[:space:]]*\|' corpus/SOURCES.md` | 1 | no S109 row |
| 31 | `grep -n 'F52' corpus/README.md corpus/SOURCES.md` | 1 | no F52 row |
| 32 | `grep -n 'fuzzilli' corpus/instruments/knowledge-expected.txt` | 0 | `:71` (F41 entry only) |
| 33 | `wc -l corpus/instruments/knowledge-expected.txt` / `grep -vc '^#'` | 0 | 91 / 89 |
| 34 | `git -C <lane> rev-parse HEAD` | 0 | `847b53792d2d29d161cad7d21a33c89df9e52e8d` (freeze tip) |
| 35 | `git -C <lane> rev-parse 847b5379…:corpus/source-snapshots/round-74/S109.txt` | 0 | `423a73fbc6b348b37d5525349638eb3752810e01` |
| 36 | `git -C <lane> hash-object corpus/source-snapshots/round-74/S109.txt` | 0 | `423a73fb…` (identical) |
| 37 | `git -C <lane> ls-tree 847b5379… corpus/source-snapshots/round-74/` | 0 | one blob, `100644 423a73fb…` |
| 38 | `git -C <lane> ls-tree ccd6a54b… corpus/source-snapshots/ \| grep -c round-74` | 1 (no match) | 0 — round-74 absent at base |
| 39 | `git -C <lane> diff --stat ccd6a54b… 847b5379… -- corpus/` | 0 | S109.txt +375 only |

All git invocations were read-only (`rev-parse`, `ls-tree`, `hash-object`, `diff --stat`); no mutating git/jj command was run anywhere, and nothing was written into the lane working tree except this report file and the three evidence files named below.

**Evidence files written (all under the wave report dir):**
- `.ufo/waves/round-74/w1/ScoutSurface-S109-refetch.txt` (19630 B — the byte-identical re-fetch of S109)
- `.ufo/waves/round-74/w1/ScoutSurface-osv-api-overview-snapshot.txt` (1810 B — the lead-only OSV converted text, quotes at L36/L38)
- `.ufo/waves/round-74/w1/ScoutSurface-osv-api-overview-raw.html` (15262 B — the raw lead-only fetch)

**Scratch cleanup:** `/fast/scratch/hyaku/kasegi-r74/ScoutSurface` (and the `cbc-scratch` subdir under it) was removed with `rm -rf -- /fast/scratch/hyaku/kasegi-r74/ScoutSurface` after the evidence copies were made; the scratch root no longer exists. Verified with `ls /fast/scratch/hyaku/kasegi-r74/` → only the L1's directory remains.

---

## 8. Summary for the L1

| Question | Answer |
|---|---|
| S109 capture integrity | **PASS** — re-fetch byte-identical (`cmp` exit 0), sha256 `c9a7adfb…d486` = the frozen value = the committed blob, 375 lines / 19630 bytes, no differing lines. |
| Canonical URL | `https://github.com/googleprojectzero/fuzzilli` → 200, 0 redirects; `https://github.com/google/fuzzilli` → **404**. Use the `googleprojectzero` path. |
| Six content clauses | **All DISTINCT** — no clause ground is held by F41/S093, F40/S092, F42/S094, F31/S080, `corpus/README.md`, or any sibling corpus. **No claim-narrowing finding.** |
| Quote readiness | 19 candidate quotes, every one verified present at its anchor line and ≤22 words — enough for the manifest's ≥10-quote requirement. |
| Sibling scan | Only kasegi names Fuzzilli (via S093). revenger holds DecFuzzer/icicle-emu/mishegos (binary-decompiler and x86-decoder fuzzing), tameshi holds Fuzzing Book delta-debugging — different technique, no clause overlap. |
| OSV overview lead | Both named statements confirmed verbatim on the live page — L36 "Currently there are no limits on the API." and L38 "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." in my 2026-11-05T08:43:42Z fetch (15262 raw bytes; converted 1810 B / 48 lines; sha256 6f92…1ab). **Lead-only, unopened-as-row**; not in `corpus/SOURCES.md` yet. |
| Landability | C2's base counters re-verified at the freeze tip with no drift (rows=51, entries=54, registry=108, knowledge=89, records=87); S109 is a free id; F52 has no row yet. Two follow-ups for the integrator: add `corpus/source-snapshots/round-74/manifest.json` (§6.2 — `capture-binding-check.py` currently exits 1 on `missing-manifest dir=round-74`), and dispose of the now-stale Fuzzilli lead bullet at `corpus/SOURCES.md:172` (§6.1). |
