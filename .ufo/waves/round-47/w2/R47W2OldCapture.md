# R47W2OldCapture — final integrated static review

Axes: depth:verifiability; coverage. Scope: historical S074 preservation, retained mined disposition and current-entry supersession only. Reviewed integrated `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Recommendation, not admission.

## Findings by severity

No new actionable defect in this bounded repair. The frozen C1 status target remains unmet, intentionally: this is not an overall C1 pass recommendation.

### Confirmed preservation and supersession

1. **Old snapshot and entire manifest are byte-identical to base.** Read-only committed-object inspection found identical Git blobs at both revisions: S074.txt `2eb0c3a71ca8f4ffa524f33205b332c2d8d87f54`; manifest.json `82fe7fb699e5b59b949a6442fd340b95442418d7`. Independent SHA-256 streams from both commits agree: snapshot `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`; manifest `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`. Historical manifest metadata remains at `corpus/source-snapshots/round-46-a2/manifest.json:5-18`. The scoped directory diff is empty. Exact observations and commands: `R47W2OldCapture.receipts.txt` beside this report.
2. **S074 remains mined historical evidence, not rejected or silently rewritten.** `corpus/SOURCES.md:80` retains status `mined`, recheck `90d`, source/scope/anchor/teaches, and changes only used-by from the current knowledge entry to `corpus/lessons/round-46.md`. The historical lesson actually cites S074 and its manifest at `corpus/lessons/round-46.md:103-124`. The permitted cell transition and historical chrome correction are explicit at `corpus/SOURCES.md:176-177` and `corpus/lessons/round-47.md:67`.
3. **Current guidance is re-pointed to S076.** The current entry's source and recheck select S076 and the round-47 manifest (`corpus/knowledge/github-repository-security-advisories.md:3-5`); literal full-file search found S076 citations and no S074/round-46-a2 references. The successor registry row is mined, points used-by back to that current entry, and literally starts teaches with `supersedes S074 —` (`corpus/SOURCES.md:82`). This is the landed row, not a wave-1 fixture. The entry correctly describes its recheck as pinned-capture/quote verification, not a live-page comparison (`:115-117`).
4. **Rejecting the predecessor is not a safe substitute.** The actual binding definition returns failure for any rejected owning row before binding the capture (`corpus/instruments/capture-binding-check.py:327-339`). Since the historical manifest still contains S074, rejection would enter this error path. This is static control-flow evidence, not a fresh execution. Wave-1's corresponding executed witness remains historical evidence at `.ufo/waves/round-47/w1/R47RevD7.md:9-13`. The integrated lesson explicitly refuses to reroll the frozen target (`corpus/lessons/round-47.md:59,69`).

## Residual risk and verification gaps

- **Old producing recipe remains unsolved.** Byte preservation and successful local pin checks do not recreate the original 42-line rendering. The successor explicitly records the absent committed producing script/receipt (`corpus/SOURCES.md:82`), and the historical lesson's erratum disclaims retroactive reproduction and future upstream byte stability (`corpus/lessons/round-46.md:157`). No inference that S076 solves S074's old recipe is warranted.
- C1 is not fully met because its frozen rejected after-state was not performed; the safe mined disposition is not a replacement acceptance criterion. C2 remains unmet/no F30 per the integrated decisions (`corpus/lessons/round-47.md:59-65`); novelty was not independently reviewed in this bounded seat.
- LSP discovery returned `No such tool` for `xd://lsp`; status, references, definition and diagnostics were unavailable. Literal file/committed-diff checks are not semantic-reference proof.
- Executed: read-only Git object/diff inspections and SHA-256 hashing. Unrun: project runtime, counters, tests, selftests, mutation battery, capture/recheck commands and network actions. No claims of fresh runtime binding success, live capture reproduction, canonical-runtime/rerouting/resume validation, saturation or full gate completion.
- No production edits, git/jj mutations, delegation, installations, service restarts or scratch creation. No scratch cleanup needed. Only this report and its small receipt were written. Reviewed worktree paths were confirmed unchanged relative to the assigned integrated commit.

## Self-evaluation (not a gate)

Accuracy 4/5: committed hashes and landed cells established; recipe reproduction intentionally unrun. Completeness 4/5: all three assigned checks covered, runtime binding unrun under reviewer restriction. Clarity 4/5: separates historical evidence from executed inspection, at the cost of a dense evidence list. Actionability 4/5: no repair requested; preserve the unmet-C1 distinction during closure. Conciseness 4/5: exact identifiers increase length but make the preservation check auditable. Mean 4.0/5. Highest-impact closure safeguard: do not promote this bounded safe-repair result to a full frozen-target pass. The user should agree this assessment is scoped, not admission.

Report: .ufo/waves/round-47/w2/R47W2OldCapture.md
