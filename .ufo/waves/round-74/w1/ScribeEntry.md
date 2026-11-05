# ScribeEntry — round 74, attempt 1, wave w1 (C2 F52 knowledge entry draft)

Seat: ScribeEntry (leaf; no subagents). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Item: draft the F52 Fuzzilli entry on S109 for the L1 integrator.

## Result

- Draft written: `.ufo/waves/round-74/w1/knowledge-fuzzilli-js-engine-fuzzing-framework.md` (100 lines, 11907 bytes). The L1 integrator lands it at `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`. Seats do not write the lane tree, so the draft stays in the wave dir.
- Provenance trio is the first three lines, byte-equal to the frozen form (verifier: `trio exact: True`).
- The entry's own recheck does NOT exit 0 yet. The round-74 manifest does not exist (`corpus/source-snapshots/round-74/` holds only `S109.txt`), so `source-recheck.py` exits 2. The L1 must create the manifest with an S109 block before the C2 foreign-cwd recheck can pass. I did not create it; it is an integrator write.
- Every capture quote (57 quotes) is a verbatim substring of S109.txt at its cited anchor line, and no quote exceeds 25 words (max 19). The L1 can pin these as the manifest quotes.
- The scope-limit paragraph in the Limits section equals `claims.json` C2 `scope_limit` byte-for-byte (verifier: `scope_limit verbatim: True`).

## Deviations from the spec (for the L1)

1. Opening order. The C2 predicate requires the entry to open with `source:`/`verified-at:`/`recheck:`. The house model (`osv-post-v1-query-contract.md`) puts an H1 title first. I followed the predicate: the trio is lines 1-3, then the `ground:` line (line 4), then the H1 title. This is the only structural departure from the model.
2. Owner name. The frozen source line says "Google Project Zero". The capture never states that phrase. `grep -n -i -E 'project zero|projectzero|googleprojectzero'` on S109.txt printed only L1 and L62 (both `googleprojectzero`), exit 0. The Attribution section says so explicitly, and it cites the page's disclaimer at L341 ("This is not an officially supported Google product.").
3. Seven components, not six. The frozen clause lists "MutationFuzzer, ScriptRunner, Corpus, Minimizer, Evaluator, Lifter". The capture's list (L214-L221) also names `Environment` (L218). The entry states all seven, as the capture does, plus the optional modules (L222-L226).
4. Targets clause. The frozen wording says "patched, coverage-instrumented target-engine builds under Targets/". The capture does not say builds live under `Targets/`; it says `Targets/` lists the supported engines (L154), patches come from the target's directory (L155), and the engine is compiled with coverage instrumentation (L156). The entry states those three steps and nothing more.
5. NDSS. Existence and name only (L243). The README's one-line description of the paper is recorded as the README's, not the paper's.

## Content clauses and anchors used (all in S109.txt)

| Clause | Anchor lines |
|---|---|
| Definition, FuzzIL properties, example IL and JS translation | 151, 199, 201, 203; example 167-178, translation 180-191; 179 |
| Semantic-correctness concern (JIT vs try-catch runtime APIs; mutational approach; per-mutation chance) | 165 |
| Swift/C split | 212 |
| Architecture components (seven), optional modules, Storage, event-driven design | 214-221; 222-226; 227 |
| REPRL execution mode | 230 |
| Tree hierarchy for scale, per-process instance, sync modules, example layout | 232-236 |
| Targets and operation (six steps), Docker/GCE | 154-159 (clang >= 4.0 at 156) |
| NDSS 2023 paper existence | 243 |
| Owner handle, disclaimer | 1, 62; 341 |
| Bug Showcase presence only | 245 (list 244-340) |
| Resources list (not characterised) | 239-242 |
| Directory names (no contents) | 108-119 |
| Mutator "and more..." | 209 |
| Coverage metric example | 220 |
| Events list pointer | 227 |
| Page chrome counts (not claims) | 66-67, 77-78, 89, 93, 101 |

## Distinctness

Taken from the claims.json distinctness screen. Checked on disk: `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` exists and cites S093 and F41 (`grep -n -E 'S109|S093|F41' ...` exit 0; the matched lines are S093/F41 lines, no S109 line in its first matches). The F40/F42/F31 and sibling statements are carried from claims.json, not independently re-verified here.

## Commands run and exit codes

Scratch: `/fast/scratch/hyaku/kasegi-r74/ScribeEntry` (created, used for `verify.py`, removed before yield; see the last step).

| # | Command (abbreviated) | Exit | Output summary |
|---|---|---|---|
| 1 | `mkdir -p` scratch; `sha256sum corpus/source-snapshots/round-74/S109.txt; wc -l` | 0 | sha256 `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486`; 375 lines |
| 2 | read `claims.json` (full), `S109.txt` 1-375, `corpus/knowledge/osv-post-v1-query-contract.md` | n/a (reads) | as above |
| 3 | `grep -n -i -E '\b(reward\|rewards\|schedul[a-z]*\|bandit\|success\|percent\|percentage\|probabilit[a-z]*\|throughput\|per second\|/s)\b\|%' S109.txt` | 1 | no output (no reward, schedule, success-rate, percentage or throughput sentence) |
| 4 | `grep -n -i -w -E 'rate\|rates' S109.txt` | 0 | one line: 165 (`an acceptable rate of semantically correct samples`) |
| 5 | `grep -n -i -E 'version\|limit\|install\|minimum\|swift [0-9]' S109.txt` | 1 | no output |
| 6 | `grep -n -i -E 'project zero\|projectzero\|googleprojectzero' S109.txt` | 0 | L1, L62 |
| 7 | `grep -n -i -E 'exploit\|root cause' S109.txt` | 1 | no output |
| 8 | `grep -n -i -w 'fix\|fixes\|fixed' S109.txt` | 0 | L8, L22 only (page chrome, not README body) |
| 9 | `grep -n -E '^\|[[:space:]]*S109[[:space:]]*\|' corpus/SOURCES.md` | 1 | no S109 row yet (expected; L1 adds it) |
| 10 | `grep -rl -i fuzzilli corpus/` | 0 | includes `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` |
| 11 | `grep -n -E 'S109\|S093\|F41' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` | 0 | S093/F41 lines |
| 12 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-74/manifest.json --source S109` | 2 | `manifest UNAVAILABLE reason=missing` (expected before L1 lands the manifest) |
| 13 | `python3 .ufo/waves/round-74/w1/ScribeEntry-verify.py` (saved as `ScribeEntry-verify.txt`) | 0 | trio exact True; scope_limit verbatim True; quotes=57 BAD=0; max quote words 19; capture sha256 as in row 1 |
| 14 | `wc -l -c` and `grep -c -P '[^\x00-\x7F]'` on the draft | 0 | 100 lines, 11907 bytes; 9 lines carry em dashes (non-ASCII) |
| 15 | `edit` on the draft (3 edits: owner sentence, rate sentence, two over-long quotes split/reanchored; one toolchain sentence narrowed) | applied | final text re-verified by rows 13-14 |

Verifier method (row 13): every straight-double-quoted fragment in the draft is checked for substring presence in S109.txt, the nearest following `S109.txt:N[-M]` anchor in the same paragraph must contain a line where the fragment occurs, and the fragment must be at most 25 words. Quotes that are not capture text are not used in the draft.

## Evidence files (in this wave dir)

- `ScribeEntry-verify.py` — the verifier (row 13).
- `ScribeEntry-verify.txt` — its output.

## Not done here (integrator / other seats)

- Landing the entry under `corpus/knowledge/`, the S109 registry row, the round-74 manifest, frontier/capture/knowledge counts, and the expected-list update: L1 integrator work.
- The foreign-cwd recheck pass and sources-census run: blocked on the manifest (row 12).
- Non-claim work (SHONEN box 2 trial, R73-V1/V2/V4/V6): not in this seat's scope.

## Tooling

None installed or updated. No provider errors.

## Cleanup

Scratch dir `/fast/scratch/hyaku/kasegi-r74/ScribeEntry` removed before yield (see final step of this seat). Receipts copied into this wave dir first.
