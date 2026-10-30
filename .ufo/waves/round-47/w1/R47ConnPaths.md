# R47ConnPaths — bounded D2 pointer audit

Axes: **depth:verifiability**, **coverage**. Report-only: no judgment, admission, integration, production edit, counter run, or other runtime invoked.

## Evidence and scope

At `2026-10-30T11:43:56.347588+00:00`, a read-only Python Eval enumeration captured **40 existing wave files**, excluding `swarm-registry.json` and this seat. It included reports, draft entry, scripts, receipts, and copied attack fixtures. The complete input list, candidate-token inventory, per-reference file/line/context, existence results, contextual resolutions, and committed instrument listing are preserved in `.ufo/waves/round-47/w1/R47ConnPaths.draft/pointer-inventory.json`. Input hashes were sampled when saving the receipt, after initial enumeration; this is not an atomic wave freeze.

Printed observations:

```text
references 1210
CONCRETE 852 distinct_tokens 316
literal-or-basename-resolves: 658
context-only-resolution: 49
ephemeral-or-template: 51
unresolved-review: 94
```

These are candidate occurrences, **not 94 defects**: broad extraction intentionally includes historical fixture prose, descriptive filenames, and code operands. URLs and slash-separated prose are not local file obligations. Every candidate is retained for review rather than silently discarded. Relative literal paths were checked against the lane; basename citations additionally against their containing directory and corpus instruments; contextual alternatives are separately labeled, never silently called literal successes.

## Findings

| Evidence | Observed result / disposition |
|---|---|
| `R47ScoutConsiderthese.md:11` says paths are lane-relative; `:34` cites `controls/c2-base.txt` and `controls/freeze-controls.txt` | **Literal resolution contradiction.** Both lane-root paths are absent. Existing destinations are `.ufo/waves/round-47/controls/c2-base.txt` and `.ufo/waves/round-47/controls/freeze-controls.txt`. The preceding fully qualified c1 citation makes the intended meaning recoverable, but does not make the shorter paths exist. |
| `R47RevEntryQ.md:34` cites `controls/freeze-controls.txt` | Same missing lane-relative literal; existing round-root destination above. No explicit root declaration here; treat as ambiguous shorthand rather than a second proven false assertion. |
| `R47ScoutS076Live.md:34` cites bare `live-2.txt` and `committed-vs-live.diff` | Neither exists beside the report or at lane root; both exist under `.ufo/waves/round-47/w1/R47ScoutS076Live.draft/`. The immediately preceding fully qualified live-1 citation supplies context, so this is a recoverable shorthand, not lost evidence. |
| `R47ScoutMerge.md:11,13-19` | The four `knowledge/corpus/knowledge/*.md` entries resolve under the explicitly declared `/home/vgpnk/Projects/shokuknow/merge/kasegi/` root. `MERGE-REPORT.md` also exists there, although line 11 explicitly qualifies only paths beginning `knowledge/`. Do not misreport these as missing lane documents. No package contents were modified. |
| `R47ExecMergeGuard.md:8` | Its relative absent-defect-register citation does not resolve in the lane, but the same line supplies the existing absolute shokuknow path. Recoverable external-root shorthand. |
| `R47ExecMergeGuard.md:5` | All three assimilation receipts exist: `.ufo/waves/round-47/assimilation/reg-ids`, `staged-ids`, `collisions`; the last two resolve with the first's parent. This audit says nothing about who created them or write authorization. |
| `R47RevEntryQ.md:7` | Missing `R47SrF30Entry.md` is explicitly described as absent at that review time, not presented as available evidence. A real entry draft now exists at `.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md`; do not convert the older review into review of that later artifact. |
| `R47ScoutRegistry.md:14,95`; `R47RevCounterC2.draft/probe.py:6` | `corpus/knowledge/zdi-disclosure-policy.md` does not exist in production. Registry report explicitly records E11 for that absence; script names a fixture target. The draft exists at the path above. This is an explicit pre-integration target, **not an available production entry**. |
| `R47ScoutZdiLive.md:35,41-42,75`; `R47ScoutS076Live.md:10,34,48`; counter receipt argv | Scratch paths do not survive cleanup. The two live reports explicitly disclose removal, so historical command operands are not broken claims of durable files. S076 separately retains both captures and a JSON receipt in its draft directory. ZDI report retains printed receipts but not independently reopenable raw live captures; do not cite its removed scratch files as durable evidence. |

Additional unresolved candidate classification: **85/94** occurrences are in copied `R47RevCounterC1.draft/attack-A/corpus/SOURCES.md` or `attack-B/corpus/lessons/round-{46,47}.md`. They include inherited historical `wave1/`, `wave2/`, controls, staged-entry names, external `security.txt`, and extracted suffixes such as `-c2.py`/`3.md`. These are not newly supplied round-47 instrument names. The inventory preserves every occurrence; no historical-path repair or existence certification is claimed. The remaining nine are explicit missing entry operands (three), orphan-description `S040-live.txt` mentions (three), bare `manifest.json` shorthand (two), and descriptive `corpus/SKILL` token (one). Per-file occurrence counts: registry 4, state 1, C2 probe 1, EntryQ 1, S076Live 1, scaffold 1. The orphan name describes an audit result, not a newly linked artifact; the manifest shorthand points contextually to `corpus/source-snapshots/round-47/manifest.json`.

## Exact instrument names

Read-only command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree --name-only HEAD corpus/instruments/` printed **61 committed entries**; full listing is in the receipt. All newly cited lane-instrument basenames in this snapshot match committed spelling, including:

`r47-routed-defects.py`, `r47-f30-gate.py`, `r47-counters-selftest.py`, `capture-source.py`, `source-recheck.py`, `capture-binding-check.py`, `recheck-audit.py`, `density.py`, `claim-package-check.py`, `claim-package-selftest.py`, `score-gap.py`, and the cited round-46 instruments.

`sources-census.sh` and `disk-guard.sh` are fleet scripts, **not** committed lane instruments; their cited absolute fleet paths exist. `build-wave1-spec.py` is a round-cache spec file, not a corpus instrument. Historical copied controls (`final-measure.sh`, `plain-rows.sh`, `run-controls.sh`) and extraction suffix `-c2.py` are excluded from the new-instrument spelling conclusion, not certified as current instruments.

## One bounded proposed move

**Canonicalize current-round evidence pointers in the integration report to lane-relative full paths, preserving explicit external-root declarations and historical argv unchanged.** In particular expand the two `controls/` citations in Considerthese, the EntryQ control citation, and S076's two draft basenames. Link the entry draft as a draft until L1 actually installs the production target. This needs no frozen-counter change, new abstraction, or new source material.

Second-order effects: runtime commands/argv remain untouched; the report contract no longer relies on a reader's cwd or inferred parent; durable wave receipts rather than deleted scratch become the evidence substrate; independent verification can resolve the same paths without changing C1/C2 predicates. **Depth improves; coverage content/count is unchanged.** Risk: blindly prefixing all paths would corrupt explicitly external or historical references and confuse proposed targets with installed files. Preserve those classifications.

Do-nothing control: retain the exact current report strings and resolve from the lane root. Printed Eval output was `controls/c2-base.txt False`, `controls/freeze-controls.txt False`, while each `.ufo/waves/round-47/controls/...` equivalent printed `True`; production `corpus/knowledge/zdi-disclosure-policy.md False`. Thus a text-only pointer move has a concrete discriminant without pretending the substantive gates passed. Frozen do-nothing controls remain named in `.ufo/waves/round-47/controls/freeze-controls.txt:1-3`; the disclosed 16 C1 and 18 C2 mutant survivors are not closed by this audit.

## Verification and limitations

Exercised: bounded existence/path resolution and read-only committed-filename listing. No gate, test suite, full battery, network access, or production verification run. An existence result is not a content, line-anchor, digest, authorization, or semantic pass. Files arriving or changing after the captured input set are not certified; L1 should repeat this pointer inventory on its final assembled report and resolve every current-round evidence target after scratch cleanup. This is a proposed integration check, not an unrun pass.

No installs, PATH changes, delegation, background jobs, git/jj mutation, or scratch directory/fixture. Only this report and its draft inventory were written; no scratch remains.

Self-evaluation: accuracy 4 (contextual and historical candidates explicitly separated); completeness 4 (bounded 40-file snapshot, not future arrivals); clarity 4 (inventory retains noisy candidates); actionability 4 (one exact pointer-normalization move, not integration); conciseness 3 (full evidence inventory is intentionally separate). Overall 3.8/5. Improvement: final assembled-report recheck eliminates the remaining moving-wave limitation. Would the user agree? Expected yes, subject to this explicit snapshot boundary.

Report: .ufo/waves/round-47/w1/R47ConnPaths.md
