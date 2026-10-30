# R47MutC2a — counter-source mutants, C2 set A

Axes: depth:verifiability; coverage. Result: **six fresh single-edit mutants survived; zero killed; zero inconclusive**. These are disclosed detector-coverage findings, not equivalence claims or production fixes.

## Frozen inputs and detector

Gate, selftest and source-recheck bytes were read with `git show 308a2cb2dc7bdce233461cc1ac49dd88e51c6193:corpus/instruments/<name>` into isolated scratch. Base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 corpus | tar -x -C /fast/scratch/hyaku/kasegi-r47/R47MutC2a/base`.

Identical bounded detector for pristine, each mutant, and each byte-restored mutant:

```text
python3 -I /fast/scratch/hyaku/kasegi-r47/R47MutC2a/instruments/r47-counters-selftest.py --base /fast/scratch/hyaku/kasegi-r47/R47MutC2a/base --work /fast/scratch/hyaku/kasegi-r47/R47MutC2a/work-<tag> --counter c2 --gate /fast/scratch/hyaku/kasegi-r47/R47MutC2a/instruments/<gate>.py
```

Do-nothing control: frozen gate through the same `--gate` interface, named `pristine`, printed `selftest cases=23 failures=0 exit=0`, process rc=0. All six mutant runs and all six restoration runs printed the identical summary and rc=0. Total: thirteen detector invocations, not the full battery. Actual commands, full stdout/stderr and return codes are in `R47MutC2a.draft/pristine.json` and each mutant JSON.

The selftest defines this interface at `corpus/instruments/r47-counters-selftest.py:24-26`; C2 case mapping and evaluation are at lines 512-526. Each fresh edit was asserted to match exactly once. The committed C2 battery definitions were compared at `corpus/instruments/r47-mutbat.py:90-111`; none of the six exact old/new pairs below duplicates a committed pair. Related hypothesis classes intentionally overlap existing disclosed gaps.

## Mutants and observed results

Locations below refer to the frozen `corpus/instruments/r47-f30-gate.py`.

| ID | Location and single edit | Expected detector sensitivity | Output / verdict |
|---|---|---|---|
| A1-H1-upper-bound | :198; `len(rows) != 30 or adm != 30` → `len(rows) > 30 or adm > 30` | Reject loss of a non-F30 admitted row; exact count becomes only an upper bound. Different from committed H1a's lower-bound relaxation. | 23 cases, 0 failures, rc=0; **survived** |
| A2-H2-unbounded-head | :225; `head = body.splitlines()[:8]` → `head = body.splitlines()` | Reject provenance displaced below the opening eight live lines. | 23 cases, 0 failures, rc=0; **survived** |
| A3-H2-source-prefix | :226; canonical URL/em-dash source prefix → `h.startswith("source: S075")` | Reject wrong canonical source URL or malformed source identifier prefix. | 23 cases, 0 failures, rc=0; **survived** |
| A4-H3-teaches-floor | :281; teaches-word rejection threshold `< 8` → `< 1` | Reject a nonempty but thin teaches cell, independently of the scope cell. | 23 cases, 0 failures, rc=0; **survived** |
| A5-H4-partial-manifest-pin | :300; compare full manifest SHA256 → compare only first twelve hex digits on both sides | Full-byte pin enforcement should distinguish a weakened prefix-only comparison. Existing simple whitespace corruption still differs in its prefix. | 23 cases, 0 failures, rc=0; **survived** |
| A6-H4-seven-quote-floor | :317; `oks >= 8` → `oks >= 7` | Detect the weakened eight-quote floor rather than the previously committed one-quote floor. | 23 cases, 0 failures, rc=0; **survived** |

Exact unified diffs: `R47MutC2a.draft/A1-H1-upper-bound.patch` through the corresponding six named `.patch` files. Detailed per-case output and before/mutated/restored hashes: the corresponding `.json` files and consolidated `R47MutC2a.draft/results.json`.

## Hash and restoration evidence

Pristine SHA256: `563d52b827acf3afe269a0079f76ba7b208cefed69c14ff24ea47b86030e6b3b`. Every restored mutant had exactly that hash before its restoration detector run.

| Mutant | Mutated SHA256 |
|---|---|
| A1 | `d4f78bc6a698a6059a235c103799d7451da80731c6a77690f9e9cfec202847ba` |
| A2 | `5984656ec506cdac366eb88086e5630d208bf5223823619b76985268186e8cee` |
| A3 | `feaea80c10b73defe11a25ff25948476fe6c63116b35ec15ecca01c9a89422a2` |
| A4 | `8d677c9a237a0a1d2b81e278e232010a36a5e86105478869b93db2b1ce2a81f0` |
| A5 | `c6ae3096d7c669fa6e024e3a32114146220beadc03506c71547706d51373f736` |
| A6 | `602879f9d5f83ee1501410a67a592aec2af2f0539b9ddc3b7ec3d47538f457c4` |

Restoration was in a `finally` block per mutant; the scratch root was removed in the enclosing `finally`. Printed evidence: `scratch_removed= True`. No production file edits, git mutations, commits, installs, or sibling writes occurred.

## Limits and interpretation

- These results assess the frozen selftest against counter-source defects, not truth or novelty of a proposed F30 entry. No integrated wave-2 tree was graded.
- H4's quote-floor change is masked by the independent exact manifest pin on these fixtures: `fewquotes` changes manifest bytes and is rejected before the floor is reached (`r47-counters-selftest.py:433-439`; gate :300-301). Survival is not proof that a seven-quote tree passes the unmodified full gate.
- A5 weakens the integrity predicate, but ordinary altered manifest fixtures still fail a 48-bit prefix check. No collision search was run or claimed; no practical exploit or equivalence is established.
- Other listed expected sensitivities describe missing discriminating cases; no additional fixture probes beyond the assigned `--gate` runs were executed.
- The initial local receipt classifier mistakenly assumed 24 C2 cases and temporarily labelled the successful 23-case runs inconclusive. Metadata was corrected from observed summaries, without rerunning or altering detector output. All raw output is retained.
- Existing pre-freeze receipt remains C2 21 mutants / 3 caught / 18 uncaught, C1 35 / 19 / 16 (`.ufo/waves/round-47/controls/mutbat-receipt.txt`). This seat adds six disclosed survivors, not a revised full-battery total.
- Disk guard printed 375.8G free on `/fast/scratch/hyaku` before fixture work; its later top-consumer listing timed out. No ENOSPC occurred.

Self-evaluation: accuracy 4 (all verdicts backed by raw receipts; A5 has no practical collision witness); completeness 5 (six edits and pristine/restored controls retained); clarity 4 (full details require the per-mutant JSON); actionability 4 (gaps localized; no out-of-scope detector edits); conciseness 4 (hash/restoration detail retained for audit). Overall 4.2/5. Highest-value next review is discriminating missing-row, displaced-head and thin-teaches fixtures; this seat does not change their contracts.
