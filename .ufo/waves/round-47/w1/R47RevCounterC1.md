# R47RevCounterC1 — frozen C1 false-green review

Axes: depth:verifiability; coverage. Recommendation only; no admission, integration, or production edits.

## Findings (high severity)

1. **L2/L8/L10 accept wholly commented-out registry evidence (D5/D7/D8).** Attack A wraps the entire synthetic-green `corpus/SOURCES.md` in one multiline HTML comment. No source table, landed Search-log/Registry-changes bullets, or REST-API lead is rendered. All markers and pinned capture bytes remain. Frozen counter still reports `routed-defects total=11 fixed=11 unresolved=0 exit=0`, process return code 0. Root cause: `r47-routed-defects.py:96-110` removes only same-line comments and opening comment lines, without comment state; `:122-138` does not handle comments at all. L2 consumes that section text at `:159-173`; L8 consumes the falsely live row at `:234-267`; L10 accepts the hidden list at `:300-309`. This is a substantive false green, not a hash bypass: L8's real manifest/source recheck still succeeds.

2. **L3/L4/L5/L6/L7/L9/L11 accept non-rendered corrections while false F29 claims remain visible (D5/D6/D7/D8).** Attack B fences both lesson files with four tildes, moves the entire corrected F29 entry into a multiline HTML comment, and appends visible assertions: `All 42 lines are body **prose**; the whole capture is that **body**.`, `Follow the lifecycle in the order the page **states** it.`, and `The three cases let a **maintainer** publish without a fix.` Frozen counter again reports `total=11 fixed=11 unresolved=0 exit=0`, process return code 0, including `L9 ... spans=47 located=47 failed=0 uncited=0` from hidden quotes. Raw-token scans at `:176-183`, `:190-223`, `:226-231`, `:270-297`, and `:312-318` neither bind to rendered corrections nor normalize the still-false visible assertions. Actual quoted-source matching remains intact but is applied to evidence the reader cannot see.

Receipts: `.ufo/waves/round-47/w1/R47RevCounterC1.draft/attack-A.txt` and `attack-B.txt` contain complete commands, every limb, and process status. Changed fixture files are retained under `attack-A/` and `attack-B/` in that directory. Counter source was not changed.

## Per-limb mutation design and bounded result

| Limb | Content-killing mutation retaining relevant markers | Evidence/status |
|---|---|---|
| L1 | Append original scaffold instructions but split each exact matched phrase with inline emphasis, e.g. `The **\`## Search log\`** bullet to append`; rendered instruction survives, raw exact phrase does not. | Hypothesis only; `:153-156` checks four exact byte strings. Keeping an unchanged scaffold phrase in an HTML comment instead would remain red, not false-green. |
| L2 | Keep all three required bullets inside a multiline HTML comment. | Attack A: fixed=1. Ordinary backtick fences are counted at `:161-164` and are not this bypass. |
| L3 | Put Corrections heading and its marker-bearing correction into a fenced example. | Attack B: fixed=1. |
| L4 | Hide corrected prose/chrome marker in a comment; restore false claims using inline emphasis. | Attack B: fixed=1. |
| L5 | Hide required corrected-order sentence; retain false visible order claim with emphasis. | Attack B: fixed=1. |
| L6 | Hide two-cases/forbidding-case correction; split `let a maintainer publish` with emphasis in visible three-cases claim. | Attack B: fixed=1. |
| L7 | Fence both dropped-seat-name errata. | Attack B: fixed=1. |
| L8 | Leave pinned manifest/capture unchanged but place S076 row inside multiline comment. | Attack A: fixed=1. Same-line comments are stripped; multiline placement is essential. |
| L9 | Place every valid re-anchored quotation in an HTML comment; publish no visible located quotations. | Attack B: fixed=1, all 47 hidden spans located. |
| L10 | Keep URL and `- ` bytes inside multiline comment, so it is not a rendered lead bullet. | Attack A: fixed=1. Plain visible URL without `- ` would fail the explicit predicate at `:305-306`. |
| L11 | Fence the ZDI-reservation and S068-precision notes. | Attack B: fixed=1. |

Combined-tree results establish the listed targeted limbs remain green; they do not independently isolate every mutation. L1 is a designed but unexecuted attack, not an observed false green.

## Controls, identity, reproduction

- **Do-nothing control:** minimal unmodified base export (three files required by the fixture builder) at `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`: `routed-defects total=11 fixed=0 unresolved=11 exit=1`, process status 1. Receipt `R47RevCounterC1.draft/do-nothing-base.txt`.
- **Positive control:** committed `r47-counters-selftest.py:212-228` green builder using that export, pinned round-47 snapshots, and committed fixed entry bytes: `routed-defects total=11 fixed=11 unresolved=0 exit=0`, status 0. Receipt `R47RevCounterC1.draft/green-control.txt`.
- Driver asserts counter and fixture-builder working bytes equal freeze commit `308a2cb2dc7bdce233461cc1ac49dd88e51c6193` before importing/running them. Exact identity in `R47RevCounterC1.draft/identity.json`. All four runs invoke the same frozen counter file, Python isolated mode, explicit `--root` and `--work`; no gate monkeypatching, alternate runtime admission, or git mutation.
- Reproducer: `python3 -I /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-47/w1/R47RevCounterC1.draft/probe.py`. Scratch is explicitly `/fast/scratch/hyaku/kasegi-r47/R47RevCounterC1/`; the driver's `finally` removes it after receipts and changed fixture bytes are copied to the wave directory. This bounded probe ran successfully and cleanup completed through that finally block.
- Disk guard before fixture work printed `/fast/scratch/hyaku 54% 376.3G` free, `/tmp 25% 96.7G`; its top-consumer scan timed out at 30s after printing status. No ENOSPC. No tools installed or updated.

## Residual risk and verification gaps

- `xd://lsp` lookup returned `No such tool`; no LSP status/references/definition/diagnostics device is available. Source-line reading and literal delimiter search are fallback evidence, not semantic proof from a server.
- This is the assigned synthetic-tree/frozen-counter attack, not an integrated-tree or full actual-diff review. No claims about unprovided production changes, runtime rerouting, or resume-continuity behavior. No shared files were edited.
- Only these two attack trees and two controls ran. No full battery or selftest rerun. Existing disclosed mutation gaps remain: C1 35 mutants/19 caught/16 uncaught; C2 21/3/18, baseline_failures=0. These are assignment-provided observations, not newly measured results; no zero-survivor or saturation claim.
- Recommended counter repair: use a consistent rendered-content representation that excludes multiline comments/fences before presence checks, normalize markup for false-claim checks, and add these two trees as negative controls. Frozen instrument was deliberately left unchanged.

Self-evaluation: accuracy 4/5 (exact counter receipts; rendered semantics inspected rather than separately rendered), completeness 4/5 (all 11 designs; only required strongest two trees executed), clarity 4/5 (combined trees need limb matrix), actionability 4/5 (reproducer and negative fixtures supplied; repair not applied by reviewer contract), conciseness 4/5 (matrix retained to satisfy every-limb requirement); overall 4.0. Highest-impact improvement: integration owner should preserve both trees as regression cases and isolate individual mutation variants before claiming closure.
