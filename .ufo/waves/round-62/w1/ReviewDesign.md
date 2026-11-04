# ReviewDesign — round 62 predata C1 review

Axes: depth:verifiability; coverage (C2 substance not assigned here). Recommendation only, not admission or a frozen verdict. Initial scope was current gate and intended contract; candidate instrument arrived immediately after report drafting and was read once in two contiguous windows. The addendum below supersedes candidate-unavailable statements; candidate runner remains unreviewed.

## Findings by severity

### High — validation and execution interpret different arguments

`corpus/instruments/figure-audit.py:180-187` checks `head.split()` script text, while `:72-87` runs the original string through `bash -c`; `audit():225-228` calls these independently. Thus checking a quoted/escaped path is not checking the script argv Bash executes. The known example `python3 corpus/instruments/"../../outside.py"` is consistent with this mismatch: realpath of text containing quote characters differs from the dequoted executed path. Round-61 lesson Wave-1 integration records this as an observed residual, not something reproduced by this seat.

Smallest structural requirement: tokenize a derive once into argv pipelines plus explicit operators/input bindings; validate every command argv in that representation, then execute that same representation directly (`shell=False`, no shell reassembly/reparse). Preserve lexical restrictions separately: Python argv[1] must retain `corpus/instruments/` prefix, and realpath relative to derive root must remain a strict descendant of the instruments directory. Do not silently broaden to arbitrary absolute-inside scripts when adopting argv.

### High — old runner completion is not a predicate verdict

`.ufo/waves/round-61/controls/c1-probe-run-r61.sh:17-21` checks the instrument before deleting scratch, so an instrument beneath scratch can be deleted. `:34-39` prints child exits without asserting them; `:37` masks failed find behind wc. The old runner therefore cannot itself establish the new C1 claim. The round-61 HarnessAttack report findings 1–3 gives observed instrument deletion, exit-99 instrument, and find-71 counterexamples, each ending runner exit 0. Do not rerun those reported failures merely to confirm them.

New runner predicate must require exact named tuple agreement, not merely nonzero/zero audit status: case id, expected audit exit, marker count, and refusal reason or derived value as applicable. Preflight canonical instrument/scratch containment before any deletion; reject instrument equal to or beneath scratch with an existing sentinel and instrument bytes unchanged. Missing instrument, dependency/setup/read/count failure, timeout, and broken instrument must never become success. A Python-native marker enumerator legitimately removes find as a dependency; then test its enumeration-error path rather than demanding an obsolete find fault still affect it.

### Medium — naive pipeline repair breaks valid ledger evidence

The allowed grammar is not arbitrary shell but it is more than a list of independent commands:

- Ledger `:59`: `wc -l < corpus/source-snapshots/round-54/S086.txt` requires explicit input-file binding (or a disclosed ledger rewrite preserving figure/want). Passing `<` as a literal wc argument breaks this row.
- Ledger `:123,131`: `git cat-file -e REV:PATH && git show REV:PATH | grep 'figure-audit' | wc -l` requires pipeline precedence above `&&`, conditional execution of the right pipeline, and retention of its final stdout. A failed cat-file must prevent the right side from producing a matching zero (QUALITY R68, `QUALITY.md:439`).
- These two zero-count rows intentionally tolerate grep no-match exit 1 inside a successful pipeline. A global all-stage-success/pipefail rule changes the current contract; it is not a free harness fix. Preserve existing pipeline final-stage status unless the claim explicitly freezes a narrower changed policy with adjusted derives. This leaves upstream-error masking outside the guarded rows as a residual, not a universal fail-closed guarantee.
- Ledger `:11,19` uses quoted ERE pipes; `:67` uses `cut -d' ' -f1`; `:91` uses `cut -d'|'` and `tr ',' '\\n'`. Token splitting cannot lose quote grouping, treat quoted pipes as operators, or pre-decode tr's argument escape into another language.

Execution risks [INFERENCE]: sequential subprocess capture is acceptable for the existing bounded data if explicit; a real Popen pipeline must close/reap children, avoid stderr deadlock, and bound the entire derive rather than leave earlier stages running after final-stage timeout. Do not claim complete resource isolation.

### Medium — two surviving limbs need behavioral detectors, not an inflated tally

Round-61 `w1/MutationPython.md:73-80,183-190` specifies exact prefix-off and boundary-separator-off edits; its direct witnesses distinguish pristine from mutants but the 24-case selftest and eight-case runner both survive. Existing absolute-out probe does not distinguish prefix removal because final containment still refuses it.

Required new witnesses: (1) a real absolute path to a script INSIDE instruments, refused by pristine solely because of the literal-prefix policy; (2) `corpus/instruments/../instruments-evil/out.py`, a real executable marker fixture refused by separator-aware containment. Removing each respective limb must compile and change that witness to an observable execution/admission result. A missing file that merely exits 1 is weaker evidence than a fixture whose marker is demonstrably created by the mutant. Kill must be attributable to the named failing case, not a syntax exception, unrelated dependency failure, or an exact-once site failure.

### Medium — advertised read-only invariant is already false

The module docstring `:25` says “the audit never runs a mutating command”; its `:21` also promises Bash execution. Both must be corrected before the new digest freeze. The allow-list contains executable counters whose behavior is not inspected, and flags/configuration of allowed tools remain capable of effects. Literal argv removes a shell reinterpretation boundary, not those effects. Update any changed registry execution/safety sentence to the same bounded model (QUALITY R74/R75/R81); do not manufacture a sandbox claim.

## Smallest honest predicate to freeze

Suggested bounded claim language (not frozen by this report):

> On the named round-62 fixtures and declared tool baseline, the pinned figure-audit implementation validates and directly executes one parsed literal-argv representation of the supported pipeline/&&/input grammar. The named quoted-traversal probes are refused before their marker scripts execute, both round-61 prefix/boundary mutants are behaviorally killed, the named admitted controls and unchanged 35-figure ledger retain their values, and the pinned runner exits success only when its complete named tuple set matches the selected baseline/candidate expectations. Named preflight and collector failures return nonzero, with instrument-under-scratch refusal preceding deletion. This is a nominal depth:verifiability instrument repair, score 4 held; no sandbox or universal absence-of-side-effects claim.

Freeze actual measured ids, tuples, test tally, instrument/battery/runner/fixture digests and baseline commit, rather than guessed counts. Fix the docstring first. Source/runtime structure inspection is needed for the “same representation” clause; finite behavioral probes alone cannot prove that architectural invariant.

R58 classification: `QUALITY.md:415` requires the axis counter itself to read the moved metric. `SCORECARD.md:2510,2526` identifies this figure gate as outside the citation-resolution metric. Therefore hold 4→4, delta 0, name citation resolution as the non-moving metric. Passing this claim cannot justify score increase, removal of nominal, a new saturation waiver, or a capability acquisition. The existing 9/10 saturation statement (`SCORECARD.md:2516`) is not independently re-measured here.

## Necessary discrimination controls

| Control | Required discrimination |
|---|---|
| Base/do-nothing, pinned base f7dcab84b104ccc03083fa1ad8c38e12830d25c9 | Run the frozen probe set in baseline expectation mode and retain measured tuples. Candidate expectation mode must reject the base on the actual quoted-path red probes; baseline mode success alone is not improvement. Existing prefix/boundary refusals are not red-before feature gains: the improvement there is detector sensitivity. |
| Genuine before fixture | Outside script and directory intermediates must exist; record base marker creation, not only audit nonzero. Use the same fixture design before/after (R79). |
| Pristine and equivalent patch | Both selftests pass; preserve previous three mutant kills and add two valid, exact-once, compile-success behavioral kills. Invalid/unapplied mutant is failure of the battery, not a kill. |
| Always-refuse instrument | Must fail positive admitted controls; prevents a reject-all implementation satisfying C1. |
| Always-admit / exit99 / missing instrument | Must fail named expectation comparisons or preflight; no marker-zero-only pass. |
| Existing good grammar | Inside + normalized-inside Python; quoted semicolon/pipe argument; plain count; quoted/escaped path with spaces if included in grammar. All must preserve exact values. |
| Pipeline and && controls | Successful chain; failed-left && blocks marker-producing RHS; valid zero-count chain returns zero; invalid early segment refuses whole parsed derive before starting an earlier valid segment. |
| Literal semantics | Escaped whitespace and mixed quote concatenation decode once; quoted operator remains data. Define whether `$VAR`, `*`, tilde, `#`, ANSI-C quoting are refused or literal, not accidentally expanded. A named safe literal-value control distinguishes direct argv from shell expansion. |
| Runner negative controls | Instrument beneath scratch + sentinel preserved; unusable scratch; fixture error; enumeration/read error; missing required executable; broken instrument; missing/duplicate named result. All nonzero with no fabricated success tuple. |
| Existing guards | Same 35/35 ledger; whole-value stale fixture (34 vs 340); failed-derive stale; prior refusal probes remain refused. Do not assume a changed selftest count without measuring it. |

These are scoped contract requirements, not a top-level round plan. Unrelated counters/source work remain outside this seat.

## Residual risk and verification gaps

- No candidate was available at the recorded availability check; this is a current-code/design review, not a pass of the eventual diff. No implementation, runner, selftest, battery or live source was executed here.
- LSP unavailable: `read xd://lsp` returned “No such tool”; no status/references/definition/diagnostics server was available. Text/file inspection is fallback evidence, not semantic-reference proof. Known direct callers inspected: audit→check_read_only/run_derive, selftest subprocess invocation, mutant battery invocation, old runner invocation, ledger derives. External unknown callers are not asserted absent.
- No resume path, same-identity reroute or canonical runtime change occurs in the inspected C1 code. Round-61 lesson routing history is not independently revalidated. This review invokes no other runtime and makes no saturation/promotion judgment.
- Direct argv still inherits PATH, environment, tool configuration, symlink races, and effects of allowed counters/flags. Do not claim all writes prevented, all escapes eliminated, every failed intermediate pipeline rejected, exhaustive mutant coverage, universal no regression, or OS confinement.

## Commands, outputs and tooling

Read `/home/vgpnk/.omp/agent/RULES.md` first; read godspeed and self-evaluation skills. Used read/glob/grep for the cited source, round-61 lesson/spotcheck/MutationPython/HarnessAttack, QUALITY and SCORECARD. Initial shell locator `grep -n "planned62\\|planned-62\\|round-62\\|r62" /home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md | head -40` produced no output; that is not evidence of section absence (the subsequent ranged read located “Planned for round 62”). No report claim relies on that locator.

`sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py` exited 0, printing respectively:

- `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`
- `f94393d981eeb93a05f6c57782b787faabfc56bfa5b4775f1c319f405fdd353c`

Candidate glob of absolute W/ExecArgv/** and W/ExecHarness/** returned both paths not found. These observations do not claim they remain absent later. No installs/updates, services, subagents, git/jj mutations, commits, production code changes, or scratch directories created; nothing to remove. Only this unique report is written. Shared the ledger compatibility facts with ExecArgv by direct peer message.

Self-evaluation: accuracy 4 (static inference and historical observations labelled; eventual candidate not examined); completeness 4 (contract/controls/ledger/runner/R58 covered, candidate unavailable); clarity 4 (severity separates current defects from design risks, but control table is dense); actionability 4 (specific witnesses and tuples, actual frozen counts intentionally left to measured predata); conciseness 4 (retains evidence and limits at cost of length). Overall 4.0. Highest-impact next evidence is the actual candidate diff and named before/after tuple receipts; do not convert this recommendation into their verification. Would the user agree: likely, because unavailable evidence is explicit and no success is invented.

## Candidate addendum — static review after late availability

Read `W/ExecArgv/figure-audit.py:1-340,344-431` once after ExecArgv's direct availability message (read tool also exposed overlapping context). No execution or extra runtime used.

- The draft closes the structural same-argv mismatch: `audit:275-279` calls `parse_derive` once and passes its returned plan to `run_derive`; `parse_derive:237-248` validates every stage before return; `run_derive:82-90` passes each stored argv directly to Popen, without shell/reassembly. This is source evidence for a shared representation, not a universal security proof.
- Quoted operators are tagged before shlex decoding (`:123-179`), allowing ledger quoted ERE delimiters to remain data. `< file` is first-stage input binding (`:228-235`, `:84-86`); `&&` separates pipeline groups (`:241-243`); final-stage status and stdout concatenation are implemented at `:95-102,117-120`. These match the ledger compatibility requirements identified above by inspection; actual 35/35 replay is still owed.
- The draft preserves literal decoded prefix and separator-bounded containment (`:196-204`), adds dot-prefix and sibling witnesses (`:393-394`), and fixes the false docstring (`:21-43`). A dot-prefix-inside witness is also a valid prefix-off discriminator; the absolute-inside control proposed above is not the only possible honest witness. Existing inside fixture makes the dot-prefix case executable if the prefix limb is removed.
- Selftest now uses `sys.executable` (`:359-361`), not bare python/Bash. This addresses the old host-conditional interpreter concern structurally; no 35-case success is claimed from reading EXPECTED_CASES.
- Remaining verification gap: `and-shortcircuit-fails` (`:401`) grades only overall exit, so it cannot alone prove RHS did not run; the external marker control remains necessary. Same for absence-of-mutation claims: selftest mostly grades exit (`:363`) rather than markers.
- Low-severity documentation precision: “Expansion syntax is refused outside single quotes” (`:32`) is broader than implementation; backslash-escaped `$` is consumed by `:150-154`, and double-quoted wildcard/tilde tokens remain literal. Better wording: unsupported unescaped expansion syntax is refused; escaped or quoted literal argument characters stay literal. This is not a bypass of direct argv execution.
- Pipeline cleanup kills/reaps directly started children (`:107-116`), not their descendants. This is consistent with the explicit non-sandbox limit; do not promote it to complete timeout containment.

No new actionable high-severity defect found in the inspected candidate's same-representation path. Runner/fault-injection/mutant receipts and frozen candidate digests remain required before a frozen success recommendation. The baseline defects above are reasons for this change, not assertions that this candidate retains them. Self-evaluation update: accuracy/completeness remain 4 because candidate source is now inspected but behavioral receipts and candidate runner are not; strongest next evidence is named tuple replay, not another speculative design pass.

Report: .ufo/waves/round-62/w1/ReviewDesign.md
