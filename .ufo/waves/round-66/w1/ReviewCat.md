# ReviewCat — round66 C1 independent review

## Findings by severity

- **High/medium: none found in the finite executable claim.** **VERIFIED** for tested candidate `d48a5e45a2afa60abefb0cbc15ed4cca41bc6c6abdd40e3789a9db09b18479c7` and doc-corrected candidate `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`, not an admission or an assessment of a later production tip. My own public-gate matrix exercised **43 cases at BASE and 43 at tested candidate**: 18 expected behavior changes, 25 unchanged controls, zero expectation failures in either matrix. The base matrix's zero failures means its *predicted false greens reproduced*, not that the base was correct. The doc-corrected candidate has an independently byte-compared identical executable tail; it was not re-run.
- **Low — documentation contradiction found and resolved before return.** Tested v1 `w1/ReviewCat/candidate-figure-audit.py:46-53` said SIGPIPE was benign **ONLY** for cat, then exempted other heads; its `:38-39` summary excluded SIGPIPE wholesale. Actual `upstream_stale` and my non-cat head/cut receipts disagreed with those sentences. I reported the finding; v2 `w1/ReviewCat/candidate-v2-figure-audit.py:37-55` now explicitly says **non-exempt upstream signal**, limits only the **cat** exemption and retains the other-head rule. My own exact-byte comparison from `import json` through EOF found all 26,031 subsequent bytes unchanged (`candidate-v2-identity.json`); `candidate-v2-doc-only.diff` contains only the module-docstring correction. No open executable or documentation finding remains in this reviewed delta.

All `w1/...` references below are relative to `.ufo/waves/round-66/` unless a full lane-relative path is shown. Checked bytes are preserved in `w1/ReviewCat/{base,candidate,candidate-v2}-figure-audit.py`; `candidate.diff` is the complete BASE→tested-candidate delta, and `candidate-v2-doc-only.diff` identifies the subsequent correction.

## Residual risk and verification gaps

1. **Conservative refusal is observable, but not an unintended regression under the assignment.** Two existing large operands, duplicate operands, two `-` operands, and option-bearing single-input cats (`-u`, `-n`, `--number`, `-u --`) change from green to stale when cat dies by SIGPIPE. These are not evidence that the input actually failed; the rule intentionally refuses a shape whose truncated execution cannot establish completion. The option policy was explicitly permitted by the seat contract and is documented in the candidate. It must not be described as general error detection or as proof that every newly stale case contains a missing input.
2. **Non-cat SIGPIPE remains exempt.** Own head and cut controls stay green with independently observed native `[-13,0]`. The repair does not close wrappers, other utilities' multi-input masking, input read failures beyond the truncation point of a single file, or status-zero programs that print a plausible value. The unchanged top-level docstring still disclaims a sandbox; this review adds no sandbox or broad-safety claim.
3. **Review method limitation:** `read xd://lsp` returned `No such tool`; no status/references/definition/diagnostics device was mounted. Caller/definition review therefore used literal text fallback plus the exact full diff, not LSP semantic proof. No empty cold-index result is treated as absence.
4. **Measured identities, not a later tip:** my BASE clone is exactly `b6db9e818d322726e39cb441f2179d34d4170275`; both candidate identities are snapshotted predata artifacts, not claimed committed production revisions. V2's evidence transfer is limited to its byte-identical executable tail, not a fabricated new test run. Any further change must be identified separately. I did not run or certify the committed-input canonical driver, mutation battery, real 35-row ledger, or full selftest; those belong to their assigned seats/L1. No executor output supplies my verdict.
5. Native vectors in these receipts are **independent subprocess mirror observations**, not advertised as an instrumented capture of the public gate's hidden wait vector. Public gate rc/reason/stdout were separately captured by invoking the unchanged script through its real CLI. The reviewed runtime derives the reason directly from its waited process status.
6. No resume path, routing identity, host runtime selection, or saturation mechanism is changed by this Python-gate diff. Those are outside this finite review; no runtime-rerouting or saturation certification is asserted. The nominal depth:verifiability claim holds score4 per R58; this seat asserts no coverage, density, domain-task, or SHONEN credit.

## Identity and receipts

| Item | Exact value / receipt |
|---|---|
| BASE | `b6db9e818d322726e39cb441f2179d34d4170275` |
| BASE gate SHA-256 | `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef` |
| Tested candidate gate SHA-256 | `d48a5e45a2afa60abefb0cbc15ed4cca41bc6c6abdd40e3789a9db09b18479c7` |
| Doc-corrected v2 gate SHA-256 | `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`; identical executable tail, no new gate invocation |
| Independent probe driver SHA-256 | `e573e04fc8ba9c8faf26dcdb41c05b18a2f87776d37bd46171676285e629c092` |
| Large fixture | `b"alpha\n" * 1398102`, 8,388,612 bytes, SHA-256 `8811b2514850fe5ad47ab777dafabdd92281109b6d4a2277872d81629b041bce` |
| Small fixture | `alpha\nbravo\n`, 12 bytes, SHA-256 `1ec8367d6c8b59e9dd0c7a4f47214db8d2e76ebd2cd5bf4155508cb27263dd2f` |
| BASE public CLI matrix | `w1/ReviewCat/base-invocation.{json,stdout,stderr}`: `SUMMARY probes=43 failures=0 mode=base`, driver rc0 |
| Candidate public CLI matrix | `w1/ReviewCat/candidate-invocation.{json,stdout,stderr}`: `SUMMARY probes=43 failures=0 mode=candidate`, driver rc0 |
| Every individual observation | `w1/ReviewCat/{base,candidate}/<probe>.json` plus unedited `.stdout`, `.stderr`, and `.ledger.json` |
| Complete side-by-side matrix | `w1/ReviewCat/matrix.md`, machine-readable `comparison.json` |
| Fully drained cat contrast | `w1/ReviewCat/untruncated-contrast.json` |
| Guarded clone commands and rc | `w1/ReviewCat/setup.json` plus per-command stdout/stderr |

Each per-probe JSON records exact command/cwd, BASE and gate/driver/input hashes, TMPDIR, observed rc/stdout/stderr/reason, and separate native stage argv/status/stderr. A missing reason is JSON null, not an inferred signal success. All gate subprocesses had a 45s timeout; native stages had 30s waits. No shell was used to interpret derives.

### Reproduction commands used

Executed with cwd `/fast/scratch/hyaku/kasegi-r66/ReviewCat`, `TMPDIR` and `HYAKU_SCRATCH` both explicitly set to that seat's `tmp/`, and `LC_ALL=C`:

```text
/usr/bin/python -B <lane>/.ufo/waves/round-66/w1/ReviewCat/probe.py --instrument <scratch>/repo/corpus/instruments/figure-audit.py --mode base
/usr/bin/python -B <lane>/.ufo/waves/round-66/w1/ReviewCat/probe.py --instrument <lane>/.ufo/waves/round-66/w1/ReviewCat/candidate-figure-audit.py --mode candidate
```

`<lane>` is the assigned kasegi lane; `<scratch>` is the seat root above. Every concrete expanded argv is retained in the corresponding invocation JSON. The driver invokes `/usr/bin/python -B <instrument> --root <scratch>/repo/review-fixture --ledger <fixture>/ledger.json` once per case; it imports no executor or candidate helper code.

## Independently reproduced BASE defect

Own `base/later-missing-large.json`:

```text
derive: cat big.txt missing.txt | head -n 1
native statuses: [-13,0]; native stderr: empty
FIG later-missing-large recorded=alpha derived=alpha ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
gate rc=0; reason absent
```

Own candidate receipt for the same derive and fixture:

```text
native statuses: [-13,0]
FIG later-missing-large recorded=alpha derived=UNAVAILABLE reason=derive-upstream-signal-13 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
gate rc=1
```

**An earlier failure is also masked at BASE**, not merely an unvisited later operand: `cat missing.txt big.txt | head -n 1` has native `[-13,0]` **with** `cat: missing.txt: No such file or directory` on native stderr, yet the BASE gate says green rc0. Candidate says stale rc1 with `derive-upstream-signal-13`. Both fully drained cat operand orders exit1 with the missing-file diagnostic (`untruncated-contrast.json`); stdout was explicitly discarded to `/dev/null`, not claimed captured. Thus the earlier-error contrast is observed, not assumed from operand existence.

With the 12-byte fixture, both missing-first and missing-last versions instead yield native `[1,0]`, gate rc1 and `derive-upstream-exit-1` in **both** revisions. These controls distinguish the SIGPIPE-specific repair from pre-existing exit1 detection; a tiny-file-only reproduction would miss the motivating defect.

## Boundary and regression review

The complete 43-row matrix is in `matrix.md`; key rows are grouped here. `signal13` means the exact reason `derive-upstream-signal-13`.

| Boundary | Own observed BASE → candidate | Interpretation |
|---|---|---|
| Single large file; stdin-only; one `-` with redirected stdin | rc0 → rc0; native `[-13,0]` | Required positives retained |
| Leading `--` with no operand, one file, or one `-` | rc0 → rc0; native `[-13,0]` | Separator not counted as an input |
| One quoted/escaped spaced filename; one quoted `|` filename | rc0 → rc0 | Count decoded argv, not shell-text words/operators |
| `cat -- -n`, `cat -- --` with real large literal filenames | rc0 → rc0 | Tokens after separator are operands, not options |
| Large missing-first and missing-last, with/without `--` | rc0 → rc1/signal13 | Both masking orders closed |
| Two existing large inputs; same file twice | rc0 → rc1/signal13 | Intentional conservative refusal, not demonstrated input failure |
| `- file`, `file -`, `- -`, stdin before/after missing operand | rc0 → rc1/signal13 | A lone `-` counts as one operand; repeated/combined stdin is not silently omitted |
| `-u`, `-n`, `--number`, `-u --` plus one large file | rc0 → rc1/signal13 | Explicitly allowed conservative option policy; even harmless `-u` is refused |
| Two existing small inputs; two existing large inputs drained by wc | rc0 → rc0 | Does not reject every multi-input cat; status must be SIGPIPE |
| Missing-only; small missing-first/last; large missing-last fully drained | rc1/upstream-exit1 → same | Other exit-status rules unchanged |
| Grep no-match piped to wc | rc0 → rc0; native `[1,0]` | Existing grep exit1 exemption retained |
| Non-cat head/cut killed by SIGPIPE | rc0 → rc0; native `[-13,0]` | Other heads unchanged |
| Python exit7; SIGTERM | rc1/upstream-exit7 and rc1/upstream-signal15 → same | Other positive/signal status rules unchanged |
| Upstream multi-cat SIGPIPE, final grep invalid regex | rc1/`derive-exit-2` → same; native `[-13,2]` | Final-stage error still takes precedence |
| Middle-stage `cat - big.txt` versus `cat -` | Multi rc0 → rc1/signal13; single rc0 → rc0; native `[-13,-13,0]` | Correct per-stage argv reaches the predicate, not the first pipeline stage's argv |

### Exact implementation and affected callers

Code line anchors in this subsection refer to the preserved tested v1 snapshot; v2 adds one module-docstring line, so each executable anchor is +1 there.

Canonical execution is still candidate `run_derive` at `:127-183`, called by `audit` at `:338-354`. Parser `:280-312` still constructs the decoded validated argv plan, and the same argv is passed to `subprocess.Popen` at `:142-143`. The new `stage_argvs.append(list(argv))` at `:146` records corresponding decoded values after each successful spawn; the sole text-found predicate caller at `:160-161` zips the matching non-final processes, heads and argv vectors. No second derive executor or text-based command-status oracle was introduced.

`cat_sigpipe_exempt` at `:89-103` removes one optional **leading** separator, conservatively refuses option-like tokens before that separator, and permits zero or one remaining decoded operand. `upstream_stale` at `:116-124` applies that check only to SIGPIPE on a cat basename; all non-SIGPIPE signal/positive-exit branches are unchanged. Existing final-error-first ordering and `derive-upstream-signal-%d` formatting remain at `:154-165`. The full diff has no parser, ledger-format, comparison, timeout, cleanup, or read-error-path change. No compatibility alias/shim or obsolete second call signature remains in the candidate text. LSP unavailability limits the caller claim as disclosed above.

The candidate adds four large-fixture public-path selftests and changes EXPECTED_CASES 63→67; I read the actual delta but did **not** claim to execute those selftests. My public matrix is independently generated corroboration, **not a second canonical counter** (R86).

## Round65 carry-in and host boundaries

Read `corpus/lessons/round-65-verifier-spotcheck.md`, especially C1 `:38-71` and routed defects `:132-151`, plus M65-7/R88. The spotcheck's C1 result was evidence-only, whereas this seat ran the exact production BASE blob. The six routed corrections remain L1's record responsibility: LOG **bullets**, omitted `1929a47`/`6824522`, final-driver `7f27c4d2...` rather than `5aa842ab...`, measured `03a23921` rather than tip `a3357329`, no invented historical BASE exit, and helper121900 **across two runs**. My receipts capture their own actual rc and do not repair historical missing rc by inference.

Read `/home/vgpnk/.omp/agent/RULES.md` before tooling. Existing tools only: Python3.14.8, Git2.56.0, GNU cat/head coreutils9.12 (`environment.json`); **no install/update**, so no installation channel; no pacman transaction and no PATH-directory write. One `git --shared --no-checkout` scratch clone only; every git invocation had explicit `-C` under my scratch. Clone toplevel was asserted equal to the clone directory before detached BASE checkout. No fixture commit, index change outside scratch, production/fleet/sibling edit, routing change, commit, push, or subagent dispatch. All durable writes are this seat's report and directory. Scratch cleanup is recorded in `w1/ReviewCat/cleanup.json` before terminal return.

Report: .ufo/waves/round-66/w1/ReviewCat.md
