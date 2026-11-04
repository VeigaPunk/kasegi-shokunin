# CounterBase — round 62 C2 do-nothing baseline

Axes: depth:verifiability (nominal 4 held), coverage (8 held). No implementation, freeze, admission or score judgment made.

## Retained evidence

- `.ufo/waves/round-62/w1/CounterBase/baseline-receipt.txt`: complete commands, cwd, stdout, stderr, exit codes, host/tool versions, input digests, all 94 registry ids/URL tokens and 70 absolute-home recheck strings. Measured 2026-11-04T15:13:49Z.
- `.ufo/waves/round-62/w1/CounterBase/baseline-results.json`: same execution results and registry enumeration, structured.
- `.ufo/waves/round-62/w1/CounterBase/inventory-normalized.json`: complete sorted path list, normalization, inventory comparison and sort exits.
- `.ufo/waves/round-62/w1/CounterBase/baseline-receipt.py`: reproducible measurement driver; scratch export must first be recreated.

Read round-61 lesson and verifier spotcheck, QUALITY admission rules and recent R58/R65/R67/R71/R76–R83 constraints, and SCORECARD planned-for-62. Commands below are predata observations, not frozen predicates.

## Export and commands

Unchanged committed export of `f7dcab84b104ccc03083fa1ad8c38e12830d25c9`, created by:

```sh
mkdir -p /fast/scratch/hyaku/kasegi-r62/CounterBase/base
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive f7dcab84b104ccc03083fa1ad8c38e12830d25c9 | tar -x -C /fast/scratch/hyaku/kasegi-r62/CounterBase/base
```

Measurement cwd: `/fast/scratch/hyaku/kasegi-r62/CounterBase/base`. No git index/ref mutation or clone checkout was necessary. Full argv arrays are retained in the JSON receipt.

| Command | Observed output | Exit |
|---|---|---:|
| `python3 corpus/instruments/frontier-recheck-count.py` | `FRONTIER-CENSUS rows=42 admitted=42 closed=42 problem-rows=0 registry=94`; `entries=45 pass=45 exit=0` | 0 |
| `python3 corpus/instruments/capture-binding-check.py` | `records=77 bound=77 unbound=0`; snapshot/manifest dirs 37/37, missing_manifest=0, digest_unpinned=0, orphan `S040-live.txt` | 0 |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /fast/scratch/hyaku/kasegi-r62/CounterBase --file /fast/scratch/hyaku/kasegi-r62/CounterBase/base/corpus/SOURCES.md` | rows94; tiers A84/B5/C5; mined76/rejected18/queued0; invalid0/missing0 | 0 |
| Same census path, mode `validate`, same `--root`/`--file` | six existing W04 warnings, then `file ok <export>/corpus/SOURCES.md` | 0 |
| `sort corpus/instruments/knowledge-expected.txt` | Full 82-line sorted output retained, including two comment lines | 0 |
| `sort -c corpus/instruments/knowledge-expected.txt` | `sort: corpus/instruments/knowledge-expected.txt:3: disorder: corpus/knowledge/ai-assisted-finding-validation.md` | 1 |

The raw whole-file sortedness check is **not** an entry-list failure: the two introductory comments participate in host collation. Supplemental explicitly normalized measurement removes blank/comment lines, passes all 80 path lines to `sort` and `sort -c` on stdin with `LC_ALL=C`: both exit0. Expected paths=80, unique=80, actual knowledge files=80, missing=0, unexpected=0. Do not freeze 82 as the entry count.

Current lane read-only validation ran once:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit0, same six W04 warnings, no errors.

## All-row id/URL screen before admission

All BASE rows were enumerated in the receipts: S001–S094, 94 unique ids, no duplicate ids, 11 columns per row. First free id is **S095**; S095 rows=0. Proposed URL `https://certcc.github.io/CERT-Guide-to-CVD/topics/phases/` appears in no existing registry source-cell URL token. All existing id/URL-token pairs matched the current lane at measurement time.

S077 is the legitimate own-work exception: its source is `.ufo/waves/round-48/controls/protocol-source.txt`, not an HTTPS URL. The JSON field `malformed_rows` flags it only because the extra URL-shape heuristic expects one URL; it is **not** a census failure. The normalized receipt explicitly corrects that interpretation.

Seven exact URL duplicate groups exist: S006/S028, S024/S029, S059/S060, S065/S080, S066/S085, S070/S072, S074/S076. Census reports six W04 warnings (S028/S029/S072/S076/S080/S085); raw exact-URL grouping is a different definition, not seven census warnings. No rows were changed or deduplicated.

## Host differences and limits

Linux 7.2.11-arch1-1 x86_64; Python3.14.8, bash5.3.20, coreutils9.12, gawk5.4.1, git2.56.0. Original locale `LANG=en_US.UTF-8`, LC_ALL/LC_COLLATE unset. Census is the host fleet script, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, not a script exported from the lane.

The export's frontier/binding/source-recheck instruments, expected list, SOURCES and README were digest-equal to the live lane at measurement time. Their exact SHA256 values are in the receipt. **Frontier is host-bound:** it executes recheck strings verbatim, including absolute `cd` prefixes. The receipt enumerates 70 absolute-home recheck lines across the knowledge corpus; no path replacement was applied. Thus this is an unchanged-export enumeration with real host-dependent recheck execution, not proof that every subprocess read only BASE bytes. Binding and registry counts read the exported files. Only one host was measured; no cross-host equivalence is asserted.

Counters establish structure/binding and pinned recheck results, not new-entry substance or novelty (R67). This seat did not source-open S095, admit F43, run candidate gates, run unrelated suites, or make a sandbox claim. No LSP symbol work was needed. No tools installed/updated; paused pacman/PATH/service restrictions respected.

## Cleanup and handoff

Owned scratch `/fast/scratch/hyaku/kasegi-r62/CounterBase` removed; removal command and absence check exited0. Only this report and four files in the exclusive CounterBase draft directory were written in production. No commits, pushes, index/bookmark changes or sibling edits.

L1 can freeze measured C2 before-values: frontier42/42, registry94, frontier-entry45/45, captures77/77, knowledge80. It should retain the explicit host-binding limitation and use normalized path counting rather than raw line count. Candidate after-values and admission review remain L1's post-integration responsibility.

Self-evaluation (not a verdict): accuracy4 — exact receipts retained but host binding prevents fully isolated replay; completeness4 — assigned counters and all-row screen covered, only one host available; clarity4 — raw versus normalized sort and S077 exception separated; actionability4 — literal argv and recreate-export command retained; conciseness4 — long raw enumerations moved to receipts. Average4.0. Highest-impact improvement for later methodology: make recheck roots explicit without mislabelling substituted commands as literal execution. This report does not implement that scope expansion.

Report: .ufo/waves/round-62/w1/CounterBase.md
