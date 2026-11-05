
## Round-74 admission — coverage map row and Frontier F52 (2026-11-05)

Appended amendment (R6): the round-74 entry `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` (Frontier F52, source S109) rests on the Fuzzilli project's own README at https://github.com/googleprojectzero/fuzzilli, captured `corpus/source-snapshots/round-74/S109.txt` (sha256 c9a7adfb...d486, 375 lines, 16 pinned quotes), manifest `corpus/source-snapshots/round-74/manifest.json`. The coverage map above is not edited in place (R6); the coverage-map row is appended here, and the F52 frontier row uses the same six-cell table shape as F51.

| Area | Entry | Source basis |
|---|---|---|
| Fuzzilli fuzzer design and operation: the FuzzIL-based coverage-guided JavaScript-engine fuzzer, its semantic-correctness concern, the architecture components, REPRL execution and tree scaling (round 74) | knowledge/fuzzilli-js-engine-fuzzing-framework.md | S109, the Fuzzilli project's own README, opened 2026-11-05 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F52 | Fuzzilli's own README: a coverage-guided fuzzer for dynamic language interpreters built on the FuzzIL intermediate language (S109.txt:151); the semantic-correctness concern for core interpreter bugs such as JIT compilers, against try-catch-wrapped runtime-API fuzzing (S109.txt:165); the Swift and C implementation split (S109.txt:212); the components MutationFuzzer, ScriptRunner, Corpus, Minimizer, Evaluator and Lifter, with the optional Storage module and the event-driven design (S109.txt:215-221, S109.txt:226-227); the REPRL execution mode with state reset (S109.txt:230); the instance tree hierarchy for scale, with its root, 16-node and 256-leaf example (S109.txt:233, S109.txt:236); the Targets/ engine procedure with patches and coverage instrumentation, clang >= 4.0 (S109.txt:154-156); and the NDSS 2023 paper's existence and name (S109.txt:243) | admitted | knowledge/fuzzilli-js-engine-fuzzing-framework.md | S109 | Read the semantic-correctness concern as the README's statement for core interpreter bugs such as JIT compilers (S109.txt:165) and not as a claim about every fuzzing target; read the tree as the README's scaling design with its root, 16-intermediate and 256-leaf layout given as an example (S109.txt:236); and read the REPRL overhead remark as qualitative, since the README gives no figure for it (S109.txt:230). |

[r74 amendment, appended 2026-11-05] The frontier as of round 74 is F01-F52 admitted: F52 at round 74. The C2 admission rests on S109 alone; the F52 scope limit stays as written in the entry, and the README's bug showcase, the NDSS 2023 paper's content and any listed CVE's specifics are not claimed by this entry.
