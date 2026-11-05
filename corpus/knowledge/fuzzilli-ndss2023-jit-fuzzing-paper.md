source: S110 - FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities (NDSS 2023), https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf
verified-at: 2026-11-05
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110
ground: F53 — the paper's own pinned statements on its identity, its design, its comparison design, and its evaluation window and counts; the comparison outcome is not pinned in the round-75 manifest and is not stated here

# FUZZILLI (NDSS 2023): a JIT-focused fuzzer, as the paper states its design, comparison design and evaluation scope

## Attribution

This is the paper's own text (S110.txt:1), captured as S110 at corpus/source-snapshots/round-75/S110.txt. Every quoted statement about the paper below is one of the 24 quotes pinned in the round-75 manifest, and each carries the capture line that manifest pins it to. The capture prints the title as "F UZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities" (S110.txt:1). The space inside the word is a text-extraction artifact, so the source line above uses the registry's spelling (S110.txt:1).

Three of the five authors are pinned: "Lukas Bernhard" (S110.txt:4), "Thorsten Holz" (S110.txt:11) and "Martin Johns" (S110.txt:12). The conference line is "Network and Distributed Systems Security (NDSS) Symposium 2023" (S110.txt:57), and the DOI line is "https://dx.doi.org/10.14722/ndss.2023.24290" (S110.txt:60).

## Claim 1 — the design statements

The paper's own priority claim is pinned as "In this paper, we close this gap and present the first fuzzer" (S110.txt:33). This entry records that claim as the paper's and does not verify it.

The design is stated as "the design and implementation of an intermediate representation" (S110.txt:35), "(IR) that focuses on discovering JIT compiler vulnerabilities. We" (S110.txt:36). The translation step is introduced with "Lifting the IR to JavaScript: We lift a program from our IR" (S110.txt:704).

The selection criterion the paper pins is coverage: "If execution of Pm increases the coverage of the target" (S110.txt:887).

## Claim 2 — the comparison design, not its outcome

The introduction summarises the comparison as "We find that our fuzzer compares well with" (S110.txt:128), with the comparator named as "the state-of-the-art method called Superion." (S110.txt:142). The contributions list says "We perform a comprehensive comparison against modern" (S110.txt:140) fuzzers.

The evaluation section describes the approach as "designed our approach called Fuzzilli specifically for finding" (S110.txt:1080) JIT vulnerabilities.

## Claim 3 — the evaluation scope and counts

The evaluation runs against "code of three state-of-the-art JavaScript engines: Google V8," (S110.txt:868) and "Apple JavaScriptCore, and Mozilla SpiderMonkey." (S110.txt:869).

The campaign window is "a consecutive series of fuzzing sessions spanning six months." (S110.txt:872). The abstract gives it as "evaluated our fuzzer over a period of six months. In total, we" (S110.txt:38).

The paper gives 17 as its count in three pinned places: the abstract, "discovered 17 confirmed security vulnerabilities. Our results show" (S110.txt:39); the type-classification text, "summary of all 17 vulnerabilities found which resulted in" (S110.txt:1041); and the conclusion, "frame we discovered 17 previously unknown vulnerabilities." (S110.txt:1377).

The descriptive evaluation words the count as "found 17 vulnerabilities that eluded competing fuzzers, with" (S110.txt:1126). The conclusion gives the age as "Those vulnerabilities were on average at least 16 months" (S110.txt:1378).

## Distinctness

- The Fuzzilli README (F52 / S109, corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md) lists this paper by name as "A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers." (S109.txt:243), a line the round-74 manifest pins as Q16-ndss-paper. The README's own statements are S109's and are not used here.
- Project Zero's comparison post (F41 / S093, corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md) is not used, and this entry does not cite S093.
- Revenger's tool-documentation rows, DecFuzzer (S117) and mishegos (S396) in ../revenger-shokunin/corpus/SOURCES.md, are not used. The distinctness screen asserts only that this paper's design, comparison and evaluation ground is distinct from those rows. It does not claim that no sibling registry holds fuzzer documentation.

## Limits

- Scope: the pinned statements only, covering identity, design, comparison design, evaluation window and counts, and age. Not the tool README (S109), not Project Zero's comparison post (S093), and not live fuzzing.
- No comparison outcome is stated. The round-75 manifest pins the introduction's comparison wording (S110.txt:128, 140, 142) and does not pin the evaluation section's outcome text, so this entry records no result from either.
- The priority claim pinned at S110.txt:33 is the paper's own and is not verified here.
- No live-fuzzing guidance and no exploit content. The entry names no CVE and no vulnerability identifier.
- The category and root-cause counts are not pinned in this manifest, so this entry states no breakdown of the 17.

## Verification

Each quoted string in this entry is one of the 24 quotes pinned in corpus/source-snapshots/round-75/manifest.json, at the same anchor line. The sole exception is the S109 line at S109.txt:243, which is pinned in corpus/source-snapshots/round-74/manifest.json as Q16-ndss-paper.

The check is `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110`, run from a foreign cwd (the recheck line above). The drafted run, with the lane capture byte-identical to the scratch capture (sha256 0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef, 88072 bytes), is recorded in the scribe report.
