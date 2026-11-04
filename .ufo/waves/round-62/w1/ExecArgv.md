# ExecArgv — round-62 predata literal-argv candidate

Axes: depth:verifiability (nominal, score 4 held) and coverage preservation (existing 35-figure ledger). No score, freeze, sandbox, or C2 admission verdict is claimed.

## Deliverable and boundaries

Complete proposed instrument: `.ufo/waves/round-62/w1/ExecArgv/figure-audit.py`.

Base `f7dcab84b104ccc03083fa1ad8c38e12830d25c9`; scratch clone `/fast/scratch/hyaku/kasegi-r62/ExecArgv`. Production implementation and ledger were not modified. Only this report and the exclusive ExecArgv draft directory were written in the production tree. No commits, pushes, index/bookmark changes in production, installs, service changes, or external-substrate changes.

Read round61 lesson and verifier spotcheck, QUALITY entry/record criteria and later relevant rows, and SCORECARD planned62. No LSP tool is exposed in this seat's tool inventory; definitions/call sites were inspected through ranged reads instead. Python observed: `/usr/bin/python`, 3.14.8. Tool installs: none.

## Semantics

- Quote-aware operator scanning followed by POSIX `shlex` word decoding. Quoted/escaped separators remain arguments, not executable separators. Parse once, validate the decoded argv, execute the same stored argv using `Popen`, with no shell invocation or second tokenization.
- Supported grammar: words, quoting/escapes, pipelines, `&&`, and one `< file` on the first stage of a pipeline. Unsupported expansion/control syntax is refused, not emulated. Single-quoted grep expressions retain `$`, braces and escaped pipes; existing `cut -d' '` and `tr ',' '\n'` derives remain valid.
- Pipelines stream between subprocesses. Status deliberately remains the last command's status, NOT pipefail, so the two ledger grep-no-match/`wc -l` zero-count derives preserve their meaning. `&&` short-circuits and aggregates stdout across successful groups. A final nonzero status or empty complete output remains stale. Spawn/input errors become stale execution errors.
- Exact decoded executable/subcommand matching replaces raw string-prefix admission. Python's decoded script must retain the literal `corpus/instruments/` prefix AND resolve beneath `realpath(base) + os.sep`. The exact prefix and separator-boundary mutation anchors remain unchanged. `./corpus/instruments/ok.py` remains refused; normalized `../instruments2/ok.py` remains refused.
- Existing dangerous-flag checks operate on decoded tokens, including quoted and escaped spellings. This does not extend the list to every tool flag or claim complete option screening.
- Corrected the historical “never runs a mutating command” docstring before the final digest. It explicitly names allowed counters, unscreened flags, PATH binaries, Git configuration and filesystem races as residual write/execute avenues, and states NOT a sandbox.
- Selftest invokes its audit subprocess with `sys.executable`, not bare Python through bash. Fixtures use HYAKU_SCRATCH when set, otherwise tempfile's TMPDIR behavior. Counter derives still intentionally name the admitted `python3` executable, which must exist on PATH.

Selftest grows 24 → 35 cases: quoted traversal, dot-prefix, normalized sibling boundary, dollar expansion, double-quoted expansion, quoted/escaped sort output flags, quoted Git output flag, input redirection, failed `&&`, and concatenated `&&` output. The existing admitted quoted-separator control is retained. Sibling fixture contains a real executable script, so dropping the realpath separator is not tested against a nonexistent target.

## Executed evidence

All measurements ran from the pinned scratch clone, with TMPDIR and HYAKU_SCRATCH both `/fast/scratch/hyaku/kasegi-r62/ExecArgv/tmp`. Full literal commands, stdout, stderr and exit status are retained in the named receipts, not inferred from collector exit alone.

| Receipt under `.ufo/waves/round-62/w1/ExecArgv/` | Command summary | Observed result |
|---|---|---|
| `baseline-selftest.txt` | `/usr/bin/python <retained baseline> --selftest` | `selftest cases=24 failures=0`, exit0 |
| `candidate-selftest.txt` | `/usr/bin/python <final candidate> --selftest` | `selftest cases=35 failures=0`, exit0 |
| `baseline-ledger.txt` | `/usr/bin/python <retained baseline>` | `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` |
| `candidate-ledger.txt` | `/usr/bin/python <final candidate>` | `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` |
| `argv-comparison.txt` | `/usr/bin/python <argv-probes.py> <baseline> <candidate> <owned scratch tmp>` | 10 paired cases, driver exit0; per-case tuples below |

Targeted comparison tuples `(audit exit, marker exists)`:

| Case | Baseline | Candidate |
|---|---|---|
| quoted Python traversal | (0,true) | (2,false) |
| dot prefix | (2,false) | (2,false) |
| normalized sibling boundary | (2,false) | (2,false) |
| dollar-expanded Python traversal | (0,true) | (2,false) |
| quoted sort output flag | (0,true) | (2,false) |
| escaped sort output flag | (0,true) | (2,false) |
| quoted separator | (0,false) | (0,false) |
| single-quoted regex dollar anchor | (0,false) | (0,false) |
| fully quoted inside script path | (2,false) | (0,false) |
| failed `&&` with marker-writing RHS | (1,false) | (1,false) |

The fully quoted legitimate inside-script path is intentionally newly admitted after decoding. Therefore there is no broad “zero new admissions” claim. Probe scripts and markers are synthetic files owned by this seat, never external targets.

## Digests and retained files

Final candidate sha256: `a0ddbd40a577d3d9e87dc89dbda0c5eb3237918246c89e0b20a29a47d395f080`.

Base instrument sha256: `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`.

`sha256.json` pins all retained candidate/baseline/probe files and five receipts. Besides the candidate, `baseline-figure-audit.py` retains the exact `git show <base>:corpus/instruments/figure-audit.py` bytes; `argv-probes.py` is the complete bounded comparison driver. An earlier candidate was measured, then only its docstring was clarified following ReviewDesign's static note; final candidate controls and comparison were rerun and the retained candidate receipts correspond to the final digest above.

## Limits and integration obligations

No full suite, formatter, linter, mutant battery or integrated runner was run by this seat. ExecMutants received preserved prefix/boundary anchors and the new head-admission anchor; its integrated candidate battery execution remains L1-owned. The new selftest fixtures are intended to kill the two r61 survivors, not a claimed measured mutant verdict here. Runner fail-open repair and F43/S095 source admission belong to other assigned seats.

Last-stage pipeline status can still hide an upstream command failure; the historical ledger uses explicit `git cat-file -e ... &&` guards where required. No process sandbox, arbitrary flag safety, descendant-process containment, trusted PATH/configuration guarantee, resource quota, or race-free path confinement is provided. Allowed Python counters can still write. Existing symlink selftest setup inherits its historical host-dependent exception path. No source-availability metric is changed by this proposal.

ReviewDesign supplied a bounded static review of the earlier candidate and identified the doc wording nit plus the need for a marker shortcircuit control; both were addressed. Its review was not independent execution. CriticArgv's attempted response returned a provider `cyber_policy` error and no answer; no critic success is inferred and no retry was requested.

Parent checks to run after integration: final candidate selftest, 35-figure ledger, ExecMutants' five-mutant battery, and ExecHarness' named repaired-runner positive/negative tuples against frozen bytes. Freeze predicates only after reconciling these predata results.

Cleanup: removed the owned scratch clone with `rm -rf /fast/scratch/hyaku/kasegi-r62/ExecArgv && test ! -e /fast/scratch/hyaku/kasegi-r62/ExecArgv`; subsequent direct path read returned “not found”. All durable evidence is retained in the exclusive draft directory.

Report: `.ufo/waves/round-62/w1/ExecArgv.md`
