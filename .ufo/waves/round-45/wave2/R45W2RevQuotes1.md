VERDICT: HOLDS

Scope: F27 entry quotes 1-8 in `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`, read from the export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (`git archive ... | tar -x`, scratch since removed). Numbering = curly-quoted spans in file order; span 8 is the first of the two spans on entry line 23. Snapshot = `corpus/source-snapshots/round-45/S071.txt` (RST source). Live = `https://docs.kernel.org/process/security-bugs.html` (curl HTTP 200, 33621 B; tags stripped, text saved to scratch).

Method: each quote normalised (curly to straight quotes, `**` removed, whitespace collapsed); searched for (a) the live text, (b) the smallest contiguous window of S071 lines containing it. Control: the same quote with one word altered (the middle word given an added or removed trailing `s`) returned not-found in both live and snapshot, so the containment test discriminates. Character-level difflib of each quote against its live location: 0 non-equal ops for all eight.

## Per-quote results

| # | Entry line | Quote (first words) | Cited | Minimal S071 window | Live | Result |
|---|---|---|---|---|---|---|
| 1 | L11 | "The following information are absolutely necessary in any security bug report" | S071.txt:17-18 | 17-18 | found | OK |
| 2 | L17 | "with no version indication, your report will not be processed" | S071.txt:20-22 | 20-21 | found | LOOSE-RANGE (line 22 not needed) |
| 3 | L18 | "A stable identifier such as a commit ID or an exact version is required" | S071.txt:22-23 | 22-23 | found | OK (quote); paraphrase overreach, see P1 |
| 4 | L19 | "Versions designating kernels not coming from kernel.org (such as distro kernels) are meaningless to maintainers" | S071.txt:23-24 | 23-24 | found | OK (quote); paraphrase overreach, see P2 |
| 5 | L20 | "Binary-only executables are not accepted" | S071.txt:39-40 | 39-40 | found | OK (quote); paraphrase overreach, see P3 |
| 6 | L21 | "By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug" | S071.txt:41-43 | 41-43 | found | OK |
| 7 | L22 | "If you resorted to AI assistance to identify a bug, you must treat it as public" | S071.txt:95-96 | 95-96 | found | OK |
| 8 | L23 | "do not publicly share a reproducer, as this could cause unintended harm" | S071.txt:99 | 99 | found | OK |

Commands and printed output (abridged, from the run):

```
[1] entry L11: 'The following information are absolutely necessary in any security bug report'
    in-live: True   snapshot minimal window: (17, 18)
[2] entry L17: 'with no version indication, your report will not be processed'
    in-live: True   snapshot minimal window: (20, 21)
...
[8] entry L23: 'do not publicly share a reproducer, as this could cause unintended harm'
    in-live: True   snapshot minimal window: (99, 99)
control(perturbed) ... snapshot: None   (all eight)
8 live offset ... char-diff ops vs live: 0
```

No MISMATCH at word level. No quote is stitched, truncated mid-sentence, or cited at a wrong line. Snapshot and live wording are identical for all eight (the only snapshot difference is the `**any**` markdown emphasis, which is not in the quoted text).

## Findings

- F-1 (LOOSE-RANGE, quote 2, entry L17): cites `S071.txt:20-22`; the quote ends on line 21 (`will not be processed.`). Line 22 (`mainline" is not acceptable...`) is outside the quote. Fix the cite to `20-21`.

- P1 (paraphrase overreach, quote 3, entry L18): the cell says "Accept only a commit ID or an exact version." S071 says "A stable identifier **such as** a commit ID or an exact version is required" (`S071.txt:22-23`). "such as" gives examples; "only" narrows the rule to a closed list the page does not state. Suggested: "Accept a stable identifier such as a commit ID or an exact version."

- P2 (paraphrase unsupported, quote 4, entry L19): "Keep the distro string as context only." S071 (`S071.txt:23-24`) says such versions "are meaningless to maintainers and will not be processed". "as context only" is not in the page. The "kernel.org identifier is still required" half is a fair reading. Suggested: state only that the page rejects non-kernel.org designations.

- P3 (paraphrase overreach, quote 5, entry L20): "The reproducer field must hold source code, a shell script, an instruction sequence or a file-system image (listed at S071.txt:38-39)." S071 (`S071.txt:37-39`) says a reproducer "with low complexity dependencies will be needed (source code, shell script, sequence of instructions, file-system image etc)". The list is examples ("etc") and the page's condition is low-complexity dependencies. The entry drops both and states the list as exhaustive. Suggested: keep "etc" semantics and add the low-complexity condition.

- P4 (extra prohibition, quote 2, entry L17): "do not fill the field from a date, a branch name or a distro string." The date and branch-name prohibitions are not in S071 lines 20-24 or elsewhere in the cited page text I read. Only the distro-kernel rule is sourced. Either cite a source for the date/branch rule or drop it.

Paraphrase checked as supported (no finding): rows for quotes 6, 7 and 8 (reproduction gate; AI-assisted finding treated as public; reproducer kept private and available on request, `S071.txt:99`, `S071.txt:210-211`).

Out-of-scope note: the second span on entry line 23 ("the reproducer should only be shared upon maintainers' request", cited `S071.txt:210-211`) was checked in passing: minimal snapshot window 210-211 (matches cite) and found in live. Not in this seat's 1-8.

## Limitations

- Snapshot S071 is the RST source; live is the rendered HTML. I did not establish that they are the same revision of the kernel docs. Wording agrees for all eight quotes, but the live page's build date/commit was not checked.
- Matching normalised curly quotes, `**` markup and whitespace; it does not judge typographic differences (curly vs straight apostrophes) beyond that.
- Paraphrase judgments (P1-P4) are my reading of the sentences, not a formal entailment check.
- No edits made; no git mutation; scratch removed.
