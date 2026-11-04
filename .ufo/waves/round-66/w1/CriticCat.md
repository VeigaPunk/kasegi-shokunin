# CriticCat — round66 prefreeze adversarial review

Axis: **depth:verifiability**, nominal 4. This is corroborating predata, not the claim counter, a freeze, a judgment, or admission authority.

## Final requested finite controls — all six matched

At L1's explicit follow-up request I reran the **same** ID/text/always-green mutants, added fixed always-stale and path-label mutants, and retained the real candidate positives. Exact immutable identities:

- Final collector: `CriticCat/collector-opaque-final.py`, SHA256 `d788bbc16cd1ac9f345e5fc1a29f3e87542ceed1f2dfcdfa5e4b7593d3a57312`.
- Final candidate: `CriticCat/candidate-opaque-final.py`, SHA256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`.

| unchanged finite control | probes | failures | actual collector rc |
|---|---:|---:|---:|
| ID-keyed no-work oracle | 8 | 4 | 1 |
| root-path-keyed no-work oracle | 8 | 4 | 1 |
| text/arity-only oracle | 8 | 1 (P7) | 1 |
| always-green oracle | 8 | 4 | 1 |
| always-stale exit1 oracle | 8 | 7 (P5 correctly passes) | 1 |
| real candidate, including single-file/stdin positives | 8 | 0 | 0 |

All six runs have complete `PROBES` summaries: these are deliberate finite-mutant rejections, not syntax errors or crashes. Outer result: `FINITE-CONTROLS controls=6 failures=0`, rc0. Exact commands, actual stdout/stderr/rc, instrument/base/input hashes, fresh nonce ledgers and fixture hashes: `CriticCat/receipts/opaque-final-{id-oracle,path-oracle,text-oracle,always-green,always-stale,real-candidate}.{json,txt}`. The outer command is in `opaque-final-command.json`; the concise evidence index is `CriticCat/opaque-final-summary.json`.

The fresh-ID plus whole-FIG binding correction kills the original ID mutant; opaque fixture paths close the root-label route. My path mutant also measured **8/0 rc0 against the earlier 1d28ca24 collector**, in `CriticCat/receipts/collector-path-oracle-v2.json`. I identified the same stable `cases/P1-.../root` leakage in the intermediate nonce-only source. [INFERENCE] That source would still expose the classification label to this path oracle despite fresh FIG IDs; I did not complete a whole-run measurement of that nonce-only generation. Its opaque-path replacement is measured above.

A further copied mid-edit collector (`CriticCat/collector-nonce-stage.py`, SHA256 `cfcd9da9c5cb36916534c9a3109f8cd5298e014ba4ca03f060215c70318d8ca3`) crashed writing `gate.stdout` to the obsolete label-named directory. Its six `nonce-stage-*` receipts have **no summary** and are chronological harness errors, not kills. They are superseded by the complete six-run table above.

This closes these concrete finite counterexamples before freeze; it does not turn a finite collector into a universal authenticity or sandbox proof. Revision/source/hash controls remain required. Exact final artifacts and digests were delivered to ExecCatDriver and L1. No full committed-input driver acceptance was measured by this seat.


## Initial counterexample — no-work oracle passes the earlier public collector

**Measured:** `CriticCat/id-oracle.py` never executes a derive, parses its argv, reads operands, or observes a child status. It hardcodes `P1-`, `P2-`, and `P8-` IDs to `derive-upstream-signal-13`, `P5-` to `derive-upstream-exit-1`, and prints each ledger's `want` as its derived value otherwise.

Against the earlier stable eight-probe collector (`1d28ca24…`) it nevertheless prints:

```
PROBES probes=8 failures=0 mode=candidate instrument_sha256=2596baad6e5072f61ea285efef1f7900688b74a79407e371683ee7fd4775cf51
rc=0
```

Public collector invocation, full input hashes, native statuses, gate stdout/stderr, and actual exit status: `CriticCat/receipts/collector-id-oracle-v2.{json,txt}`. Collector snapshot: `CriticCat/collector-v2.py`, SHA256 `1d28ca247ec3bfb3618c3610fe4da5eec34c0c9ad22716f729e0bdb44ade4ab9`.

The smallest counterexample changes **only the figure ID**, not derive, want, fixture root, or operands:

| instrument | figure ID | derive | native | actual gate rc/reason |
|---|---|---|---|---|
| no-work ID oracle | `P1-cat-two-operand-missing-sigpipe` | `cat big.txt missing.txt \| head -n 1` | `[-13,0]` | 1 / `derive-upstream-signal-13` |
| same oracle | `held-out-same-command` | identical | `[-13,0]` | **0 / green** |
| real candidate | either ID | identical | `[-13,0]` | 1 / `derive-upstream-signal-13` |
| either instrument | ordinary or renamed single-input ID | `cat big.txt \| head -n 1` | `[-13,0]` | **0 / green** |

Eight complete public CLI invocations, their ledger documents and hashes, fixture hashes, stdout, stderr and rc are in `CriticCat/receipts/identity-counter.json`. This retains the positive single-input control rather than replacing the policy with blanket refusal.

**Impacted axis:** collector-only evidence cannot establish that the implementation executes and evaluates the finite runtime predicate. This does **not** demonstrate that the committed-input driver accepts this oracle; I did not run that driver. Its directory was absent during the initial review; later I read its declarations and sent its author the exact old and final control artifacts, without executing it.

**Smallest safe correction:** retain revision-pinned reviewed gate bytes, source-anchored semantic mutations and final gate identity checking; do not describe collector success as anti-forgery evidence. A paired ID-invariance control rejects this particular oracle. No finite public probe list excludes every possible hardcoded oracle, so adding cases alone is not an authenticity boundary. Preserve the no-option single-input and stdin positives.

## M65-5 control repaired before freeze

A separate no-work `CriticCat/text-oracle.py` applies the decoded cat-arity rule **regardless of runtime status**. The original specified P1–P6 all accept its answers. In both the earlier stable and final collectors P1–P6 and P8 report `pass=true`; **P7 alone kills it**:

```
NATIVE P7-same-derive-small-twin stage0=0 stage1=0 out=alpha err_bytes=0
PROBE P7-same-derive-small-twin rc=1 expected=0 reason=derive-upstream-signal-13 pass=false
PROBES probes=8 failures=1 mode=candidate ...
rc=1
```

Receipts: `CriticCat/receipts/collector-text-oracle-v2.{json,txt}`. Turning the same oracle into always-green via `ORACLE_ALWAYS_GREEN=1` is rejected on P1/P2/P5/P8: **8 probes, 4 failures, rc1**, in `collector-always-green-v2.{json,txt}`. The real candidate is **8 probes, 0 failures, rc0**, in `collector-candidate-v2.{json,txt}`.

I proposed the identical-command runtime twin and the `cat -- -- missing.txt` case to ExecCatProbes before these were frozen. The seat adopted both as P7/P8. It also adopted an empty `other.txt` in both P2/P7: only `big.txt` changes, from >4MiB to `alpha\n`. The small twin therefore has one small write, not two tiny nonempty writes racing `head`. The stable collector's fixture hashes are copied into every v2 JSON receipt.

My earlier own small-file observations used two nonempty files: they observed `[0,0]`, but are not offered as timing-proof fixtures. Use the corrected collector pair for the frozen counter.

## Candidate: decoded argv and operator coverage

Source identities:

- Committed base `b6db9e818d322726e39cb441f2179d34d4170275`, gate SHA256 `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`.
- Independently captured candidate from ExecCatGate, SHA256 `d48a5e45a2afa60abefb0cbc15ed4cca41bc6c6abdd40e3789a9db09b18479c7`.
- Exact snapshots: `CriticCat/base-gate.py`, `CriticCat/candidate-gate.py`; base extraction command and rc in `CriticCat/receipts/setup.json`; candidate identity in `candidate-identity.json`.
- The documentation-only successor SHA256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` was initially only read, then independently captured, hashed and executed in the final finite-control rerun above. The 36-case matrix below remains bound to `d48a5e45…`; the final eight-probe positive control is bound to `51f299af…`.

The independent public-CLI matrix has **31 observed cases**, plus **5 compound/middle-stage cases**. Every candidate result matched the declared finite policy or explicitly named unchanged boundary; these counts are not a general correctness proof. Every row records actual gate stdout/rc/reason and independent `Popen` statuses with parent pipe fds closed. The enclosing harness rc0 means receipt collection completed; individual observations are the evidence.

| shape | observed candidate result |
|---|---|
| large cat + missing/existing/renamed second operand | stale1 / `derive-upstream-signal-13` |
| quoted head `c'at'`; escaped/quoted operands; no spaces around pipe | same refusal after decoding |
| one large operand; stdin-only; lone `-` with input redirection | green0 |
| one filename containing a blank, literal `\|`, or literal `&&` | green0; still one decoded operand |
| leading `--` + one operand; `--` stdin; filename starting `-` after separator | green0 |
| leading `--` + two operands; real large filename `--` followed by missing operand; empty-string second operand | stale1 / signal13 |
| file + `-`, or `-` + file, with stdin redirection | stale1 / signal13 |
| earlier missing or directory operand, followed by large file | stale1 / signal13; native stderr includes the earlier diagnostic |
| directory as the only input, fully drained | stale1 / `derive-upstream-exit-1`, unchanged |
| final stage exit7, with upstream cat SIGPIPE | stale1 / `derive-exit-7`, precedence retained |
| multi-input cat before or after `&&`; multi-input middle stage | stale1 / signal13 |
| single-input cat followed by `&&`; stdin-only middle cat | green0 |

Receipts: `CriticCat/receipts/{base-public,candidate-public,base-operators,candidate-operators}.{json,txt}` and their `*-command.json` wrappers. In compound receipts `native_groups` are independently replayed pipelines, not a claim of shell/gate `&&` equivalence.

The candidate's leading-separator handling removes **only the first** `--`. The second token can be a real filename and is correctly counted; I found no decoded-argv bypass in these cases.

### Deliberate restriction that must be stated

`cat -u big.txt | head -n 1` has one input file and native `[-13,0]`: base green0, candidate stale1 / signal13. This is the explicitly permitted conservative option-token policy, not retention of *every* single-input cat invocation. The frozen predicate must say **stdin-only or one decoded operand without options, with an optional leading `--`**. Calling all single-input cat pipelines unchanged would be false.

The original captured candidate module docstring L46 said SIGPIPE was benign "ONLY when ... a cat", while L52–53 and the implementation preserved other heads. This wording defect was corrected before freeze by the successor above: its observed L47–50 scope the restriction to cat and explicitly retain the other-head exemption. The final eight-probe control exercised that successor; the broader 36-case matrix exercised the original snapshot.

## Boundaries retained, not repaired or claimed

- **Other heads:** `head -q -n 100000000 big.txt missing.txt | head -n 1` still has native `[-13,0]` and is green. Cat-only is intentional.
- **Wrappers:** an allowed Python counter that runs `cat missing.txt`, ignores its failure and prints `alpha` exits0 and remains green. Inner failures/grandchildren are not direct-child status evidence.
- **Single-input read errors:** an immediate directory-read failure remains stale1. An actual single-input SIGPIPE still exempts the unread suffix; this review does not reproduce or claim detection of a later EIO in that suffix. No completeness guarantee follows from arity alone.
- Other allow-listed heads, configured executables, PATH shadowing, mutable input/producer content, exit0 truncation, and swallowed statuses remain outside this finite repair. No broad sandbox, general error-detection, or end-to-end domain-task claim is supported.

## R88/R89 carry-in and receipt provenance

Read: round65 spotcheck; round65 lesson M65-5/M65-7/M65-8; QUALITY R88/R89; prior critic H1/D2 and mutation emulator evidence. R88 is exercised by both the masked missing operand and the unmasked cat-exit1 control, not merely by benign single-cat SIGPIPE.

The first collector snapshot (`CriticCat/collector-v1.py`, SHA256 `bf5a656e9f9f2d613d71e9267986dfb8efbcd482ebe97d9fb80a3a8989243819`) was captured during a sibling's edit. It reported P1–P6, then raised `KeyError` for unfinished P7; **it is not a successful full collector receipt**. It also showed bash141 versus expected-13 as non-load-bearing notes. Those findings were sent to ExecCatProbes. Stable v2 normalizes native statuses and makes harness/parser notes fail the probe. Keep v1 receipts as chronological evidence, not as the counter's identity.

For R89, only the L1's chosen final counter can establish committed controls revision, committed pins, base-vs-candidate pin mode, scratch guards and child timeouts. My captured mutable predata snapshots are labelled as such; neither v1 nor v2 is independently committed or frozen by this seat. Recommend retaining the actual committed control revision and source hashes, not an "adding commit" lookup or worktree fallback. Do not substitute this critic harness as a second counter (R86).

## Scope and tools

No production, fleet, sibling, routing, index or jj write; no commit/push; no subagent dispatch; zero clones and zero git mutations. All generated fixtures and TMPDIR were confined to the assigned scratch. Durable receipts were copied before scratch removal. After L1 requested the additional finite controls, scratch was recreated only for those controls and removed again; `CriticCat/cleanup-followup.json` records final `remaining_exists=false`, rc0 (`cleanup.json` records the earlier removal).

No install/update or pacman transaction. Preinstalled tools used: Python3 **3.14.8**, Git **2.56.0**, GNU coreutils cat/head/wc **9.12**, GNU grep **3.12-modified**, GNU Bash **5.3.20**. Channels and reasons: existing host executables, finite public gate/native-pipeline probes and committed-base extraction. Version commands, stdout and rc: `CriticCat/receipts/setup.json`, `additional-tool-versions.json`. No selftest, general build/lint/test suite, full driver, or domain repository test was run by this seat.

## Review self-check (not axis judgment)

Accuracy 4/5: immutable snapshots and actual rc recorded; driver-level acceptance unmeasured and explicitly excluded. Completeness 4/5: requested argv/operator/oracle/positive/boundary work covered; no actual late single-input EIO fixture, explicitly not claimed. Clarity 4/5: fixed defects and finite limitations separated; raw evidence remains larger than the summary. Actionability 4/5: exact ID counterexample and prefreeze controls supplied; L1 alone must bind final committed controls. Conciseness 4/5: receipt index is necessarily detailed. Mean 4.0/5. Highest-value improvement is committed-driver confirmation of oracle rejection, not a wider sandbox claim.

Report: `.ufo/waves/round-66/w1/CriticCat.md`
Receipts: `.ufo/waves/round-66/w1/CriticCat/receipts/`
Artifacts: `.ufo/waves/round-66/w1/CriticCat/`
