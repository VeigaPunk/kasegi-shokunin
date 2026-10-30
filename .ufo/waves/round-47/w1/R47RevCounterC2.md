# R47RevCounterC2 — frozen C2 counter review

Axes: depth:verifiability; coverage. Scope: read-only frozen `corpus/instruments/r47-f30-gate.py`; synthetic trees only. Recommendation: retain both falsifiers as disclosed counter gaps; no admission/integration decision is made here.

## Findings, by severity

### Medium — H1 accepts an invisible duplicate frontier row (observed false green)

`corpus/instruments/r47-f30-gate.py:169-176` normalizes only U+200B/U+200C/U+200D/U+FEFF before its visible-row count. The strict parser at :159-166 recognizes only ASCII digits adjacent to F. Append the otherwise identical F30 row with id `F\u206030` (U+2060 WORD JOINER): both parsers ignore that additional visibly F30-shaped row. This violates the explicit zero-width ghost-row rejection contract at :21-26, yet H1 reports `pass=1 read=rows=30 admitted=30 F30=admitted` and the full gate reports `f30-gate fixed=7/7 exit=0`.

Evidence: `R47RevCounterC2.draft/word-joiner-duplicate.txt` contains the exact command, all seven limb outputs and exit 0. `R47RevCounterC2.draft/probe.py` reproduces the tree by appending exactly one row; `mutations.txt` records the escaped character. The do-nothing control also passes 7/7, so this is not a red baseline masking a limb outcome. Suggested correction: explicitly reject invisible format characters in frontier candidate rows, rather than silently omitting unrecognized row-shaped input.

### Medium — H2 validates a sanitized recheck rather than its actual bytes (observed false green)

At :224, H2 passes the entry through `live_lines`; :143 removes inline HTML comments before :228 applies `RECHECK_LINE`. Append ` <!-- ; echo HOSTILE_TOKEN -->` to the canonical recheck line. The raw line is outside the exact allowed form (:109-111 prohibits shell metacharacters in its optional cadence comment), but H2 sees the sanitized canonical command and reports `recheck=1`, with full gate 7/7 exit 0. The issue is the exact-form provenance check bypass, not a demonstrated shell exploit: no entry recheck command was executed.

Evidence: `R47RevCounterC2.draft/hostile-recheck-comment.txt`; single-line mutation reproduced in `probe.py`. Suggested correction: validate raw provenance lines before removing presentation comments, while retaining live-text handling for sections.

## Bounded experiment / do-nothing control

Executed `python3 .ufo/waves/round-47/w1/R47RevCounterC2.draft/probe.py` from the lane. Each invocation uses the unchanged canonical frozen gate, `python3 -I`, explicit `--root` and `--work`, and scratch-local TMPDIR.

| Tree | Mutation relative to synthetic control | Observed result |
|---|---|---|
| do-nothing-control | none | H1-H7 pass; 7/7; process exit 0 |
| word-joiner-duplicate | append F30 row with U+2060 inside id | H1-H7 pass; 7/7; process exit 0 |
| hostile-recheck-comment | append hostile-token HTML comment to recheck | H1-H7 pass; 7/7; process exit 0 |

Receipts and reproducible driver: `.ufo/waves/round-47/w1/R47RevCounterC2.draft/`. Control is **synthetic**, not an integrated candidate: copied current knowledge files, unmodified pinned round-47 capture/manifest, first Registry section only, one generated S075 row, one generated F30 row and a generated structurally passing entry (`control-entry.md`). No inference that the control is a substantive approved F30 entry. Two strongest trees were run, not the full battery.

## Requested mutation design coverage

| Design | Intended limb | Assessment |
|---|---|---|
| Append four-space-indented duplicate F30 row | H1 | Not run; parser strips indentation and counts 31 rows (:133-147, :159-166), predicting rejection. |
| Append zero-width-dressed duplicate F30 row | H1 | U+2060 variant run: false green above. U+200B variant not run; :174 predicts detection. |
| Fence-wrap required entry section | H2/H5 | Not run; :138-142 removes fenced content, predicting missing section and/or live core rejection. |
| Insert U+200B into F30 status cell | H1 | Not run; exact `admitted` comparison at :196 predicts rejection. |
| Hostile token in recheck comment | H2 | HTML-comment variant run: false green above; ordinary `# ; ...` variant not run and :111 predicts rejection. |
| Duplicate an extra manifest quote record | H4 | Not run; byte pin at :300-301 predicts rejection before quote processing. |
| Append snapshot newline | H3/H4 | Not run; snapshot byte pin at :272-276 predicts H3 rejection, source recheck predicts H4 rejection. H5 alone splits lines (:327), so unchanged line citations are not a byte-integrity test. |

H6/H7 were exercised unchanged in both attacks and the control; no independent attack on their census/name/content invariants is claimed.

## Residual risk and verification gaps

- LSP device unavailable: `read xd://lsp` returned `No such tool`; semantic references/definition/diagnostics unavailable. Findings use direct source inspection plus observed canonical-gate outputs, not grep as semantic proof.
- No production diff was supplied or edited; this review targets the frozen counter behavior only. No rerouting, admission, resume, or saturation-path changes are asserted.
- Known pre-freeze gaps remain: C2 21 mutants / 3 caught / 18 uncaught; C1 35 / 19 / 16. No claim these new attacks are distinct from those survivors; full battery not rerun. The 43-case selftest was not rerun.
- Disk guard printed scratch free 375.8G (54% use), /tmp 96.7G; the guard's later top-consumer phase timed out at 30s. No ENOSPC occurred. The tool automatically backgrounded that guard at its deadline; no background work was intentionally requested and no other background job was started.
- Scratch `/fast/scratch/hyaku/kasegi-r47/R47RevCounterC2` was removed by the driver's `finally` after receipts were written. No git/jj mutations, tool installs, shared-production writes, or execution of hostile recheck text occurred.

Self-evaluation: accuracy 4 (no browser-rendering verification of U+2060); completeness 4 (five designs statically assessed, two strongest executed as requested); clarity 4 (synthetic control explicitly distinguished); actionability 4 (driver and exact source ranges supplied, no fix authorized); conciseness 4 (bounded evidence retained). Mean 4.0. Improvement: integrated-tree rerun by the integrating reviewer; preserve raw-line and invisible-character fixtures. User agreement expected because observed passes and unrun predictions are separated.
