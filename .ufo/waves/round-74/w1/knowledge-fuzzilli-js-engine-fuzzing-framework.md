source: S109 — Google Project Zero Fuzzilli, https://github.com/googleprojectzero/fuzzilli (capture corpus/source-snapshots/round-74/S109.txt, sha256 c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486)
verified-at: 2026-11-05
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-74/manifest.json --source S109
ground: F52 — the Fuzzilli project's own README: its self-description as a coverage-guided fuzzer for dynamic language interpreters built on the FuzzIL intermediate language; the semantic-correctness concern for core interpreter bugs against try-catch-wrapped runtime-API fuzzing; the Swift/C split; the named architecture components and the event-driven design; the REPRL execution mode; the instance tree hierarchy for scale; the Targets/ engine procedure (patches, coverage instrumentation, clang >= 4.0, Docker and Google Compute Engine support); and the NDSS 2023 paper's existence

# Fuzzilli, as the project describes itself: a FuzzIL-based coverage-guided fuzzer for JavaScript engines, its semantic-correctness concern, architecture, REPRL execution and tree scaling

## Attribution

This is the Fuzzilli project's own README, captured with its repository page as S109 (corpus/source-snapshots/round-74/S109.txt, 375 lines). Every statement below is that README's statement, and each one carries its capture line. The capture names the repository owner as the handle `googleprojectzero` (S109.txt:1 and S109.txt:62). The label Google Project Zero in the source line is the registry's name for that owner; the capture does not contain that phrase. The capture also carries the page's disclaimer "This is not an officially supported Google product." (S109.txt:341). This entry makes no call against github.com or any other host, and every check replays the pinned capture.

## Claim 1 — the definition: a coverage-guided fuzzer built on FuzzIL

The README defines the project in one sentence. It is "A (coverage-)guided fuzzer for dynamic language interpreters" (S109.txt:151), "based on a custom intermediate language" (S109.txt:151), and that language is named FuzzIL on the same line, "which can be mutated and translated to JavaScript" (S109.txt:151).

The README states three properties of a FuzzIL program. "A FuzzIL program is simply a list of instructions." (S109.txt:199) "Inputs to instructions are always variables, there are no immediate values." (S109.txt:201) "Every variable is defined before it is used." (S109.txt:203)

The README gives one example program in the intermediate language (S109.txt:167-178) and its translation to JavaScript (S109.txt:180-191). The example is an illustration; the README introduces the translation with "Which can e.g. be trivially translated to the following JavaScript code:" (S109.txt:179).

## Claim 2 — the semantic-correctness concern for core interpreter bugs

The README's concern is stated for one target class: "When fuzzing for core interpreter bugs, e.g. in JIT compilers, semantic correctness of generated programs becomes a concern." (S109.txt:165) It sets this against another: "semantic correctness can easily be worked around by wrapping the generated code in try-catch constructs" (S109.txt:165), which the README gives as the case of "fuzzing of runtime APIs" (S109.txt:165).

For the JIT case the README names one approach: "a mutational approach in which all samples in the corpus are also semantically valid" (S109.txt:165). Its stated mechanism is that "each mutation only has a small chance of turning a valid sample into an invalid one" (S109.txt:165).

## Claim 3 — the Swift/C split

The README states the implementation split in one sentence: "The fuzzer is implemented in Swift" and, for some parts, "some parts (e.g. coverage measurements, socket interactions, etc.) implemented in C." (S109.txt:212)

## Claim 4 — the architecture components and the event-driven design

The README introduces the components with "A fuzzer instance (implemented in Fuzzer.swift) is made up of the following central components:" (S109.txt:214). Each is given one line of description:

- MutationFuzzer: "produces new programs from existing ones by applying mutations" (S109.txt:215).
- ScriptRunner: "executes programs of the target language" (S109.txt:216).
- Corpus: "stores interesting samples and supplies them to the core fuzzer" (S109.txt:217).
- Environment: "has knowledge of the runtime environment" (S109.txt:218).
- Minimizer: "minimizes crashing and interesting programs" (S109.txt:219).
- Evaluator: "evaluates whether a sample is interesting according to some metric, e.g. code coverage" (S109.txt:220).
- Lifter: "translates a FuzzIL program to the target language (JavaScript)" (S109.txt:221).

The README lists further optional modules at S109.txt:222-225: Statistics, NetworkSync, ThreadSync. Its Storage module is "stores crashing programs to disk" (S109.txt:226).

The event-driven design is stated at S109.txt:227: "The fuzzer is event-driven, with most of the interactions between different classes happening through events." The README gives the purpose as "The event mechanism effectively decouples the various components of the fuzzer" (S109.txt:227), and says events are dispatched "as a result of a crash or an interesting program being found" (S109.txt:227). It points to "See Events.swift for the full list of events" (S109.txt:227); that file is not in the capture.

## Claim 5 — REPRL execution

The README names the execution mode: "Fuzzilli uses a custom execution mode called REPRL (read-eval-print-reset-loop)." (S109.txt:230) It describes the mechanism in one sentence: "the target engine is modified to accept a script input over pipes and/or shared memory" (S109.txt:230), then "execute it, then reset its internal state and wait for the next script" (S109.txt:230). The stated effect is "This removes the overhead from process creation" (S109.txt:230). The README gives no measurement of that effect.

## Claim 6 — the instance tree hierarchy for scale

The README states the instance model: "There is one Fuzzer instance per target process." (S109.txt:232) For scale, "fuzzer instances can form a tree hierarchy" (S109.txt:233), and "they report newly found interesting samples and crashes to their parent node" (S109.txt:233). A parent "synchronizes its corpus with its child nodes" (S109.txt:233).

The README names two synchronisation modules: "synchronize instances in the same process" (S109.txt:234, inter-thread) and "synchronize instances over a simple TCP-based protocol" (S109.txt:235, inter-machine).

The README's example layout is "one root instance, 16 intermediate nodes connected to the root, and 256" leaves, with the leaves "connected to the intermediate nodes" (S109.txt:236). Its reason is stated as "As one parent node can quickly become overloaded if too many instances send programs to it" (S109.txt:236). The README says the design "allows the fuzzer to scale to many cores on a single machine as well as to many different machines" (S109.txt:236). It points to the Cloud/ directory for distributed fuzzing (S109.txt:236); that directory's contents are not in the capture.

## Targets and operation

The README gives the operating procedure in six steps (S109.txt:154-158):

1. "Download the source code for one of the supported JavaScript engines." (S109.txt:154)
2. "See the Targets/ directory for the list of supported JavaScript engines." (S109.txt:154) The list itself is not in the capture.
3. "Apply the corresponding patches from the target's directory." (S109.txt:155)
4. "Compile the engine with coverage instrumentation (requires clang >= 4.0) as described in the README." (S109.txt:156)
5. "Compile the fuzzer: swift build [-c release]." (S109.txt:157)
6. "Run the fuzzer: swift run [-c release] FuzzilliCli --profile=<profile> [other cli options] /path/to/jsshell." (S109.txt:158)

So the README's target procedure is the engine source with the target's patches applied and then compiled with coverage instrumentation; the one toolchain requirement it states for that compile is clang >= 4.0 (S109.txt:156). The README adds that "Building and running Fuzzilli and the supported JavaScript engines inside Docker and on Google Compute Engine is also supported." (S109.txt:159)

## Resources — the NDSS 2023 paper

The README lists "A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers." (S109.txt:243) This entry establishes the paper's existence and its name as the README gives them, and nothing more. The README's one-line description is the README's; this entry does not characterise the paper.

## Distinctness

- F41 / S093 (Project Zero's comparison post, corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md): a publisher's comparison of two systems. Per the round-74 distinctness screen (claims.json), its scope limit keeps the Fuzzilli method out, and the tool's own documentation ground is unheld. This entry takes the tool's own README and does not cite S093.
- F40 / S092 and F42 / S094 (Big Sleep): a different system. Not used here.
- F31 / S080 (OSV format ranges): unrelated. Not used here.
- Sibling registries: per the same screen, none holds fuzzer tool documentation. The connector seat re-verifies this.

## Limits

Scope limit: the project's own README/documentation statements only; not Project Zero's comparison post (S093/F41), not Big Sleep (S092/F40, S094/F42), not the NDSS 2023 paper's content (existence and name only), not any listed CVE's specifics (only that the README lists bugs found with Fuzzilli), and no live fuzzing (live-target testing stays refused).

The README does not state the following. Each absence was checked against the capture:

- No reward schedule and no success-rate claim. `grep -n -i -E '\b(reward|rewards|schedul[a-z]*|bandit|success|percent|percentage|probabilit[a-z]*|throughput|per second|/s)\b|%' corpus/source-snapshots/round-74/S109.txt` prints nothing and exits 1. The only standalone word "rate" in the capture is the concept sentence at S109.txt:165.
- No rate figure. The README says "an acceptable rate of semantically correct samples" (S109.txt:165) and gives no number for it.
- No version minimum other than clang. `grep -n -i -E 'version|limit|install|minimum|swift [0-9]' corpus/source-snapshots/round-74/S109.txt` prints nothing and exits 1. The one stated minimum is "requires clang >= 4.0" (S109.txt:156).
- No coverage metric beyond the example "e.g. code coverage" (S109.txt:220).
- No mutator list beyond the README's own, which ends "and more..." (S109.txt:209).
- No event list: "See Events.swift for the full list of events" (S109.txt:227); the file is not in the capture.
- No Targets/, Cloud/ or Docs/ contents. The capture lists these directories by name (S109.txt:110-119 and S109.txt:236) and holds the contents of none of them.
- No content of the NDSS 2023 paper, the Offensive Con 2019 presentation, the master's thesis, or the two blog posts (S109.txt:239-242).
- No bug analysis. The Bug Showcase (S109.txt:244-340) is a list of bug names and identifiers. The README gives no exploitation, root cause or fix for any entry, and this entry does not reproduce or characterise any of them. The README's statement is that the list contains "some of the bugs found with the help of Fuzzilli" (S109.txt:245).
- No performance or throughput figure. Only the overhead remark at S109.txt:230 appears, without a number.
- Page state is not a claim. Stars, forks, issue and pull-request counts, and commit counts at S109.txt:66-67, 77-78, 89, 93 and 101 are the page as fetched.
- The capture's bytes carry no timestamp. The fetch instant is pinned in the round-74 manifest, not in this entry.
- Nothing about the current state of the repository or any host. No query against github.com was made.
