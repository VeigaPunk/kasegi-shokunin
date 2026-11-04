# Connector Synthesis Proposal: Dual-Phase Decoded-Operand Normalizer with Signature-Preserving Upstream Guard

**Seat:** ScopeCat (connector, leaf)  
**Round:** kasegi r66 wave w1  
**Base:** `b6db9e818d322726e39cb441f2179d34d4170275`  
**Judged axis:** `depth:verifiability` (nominal R58, score 4 held)  

---

## 1. Evidence

1. **Baseline False-Green Masking (`ReviewCat/base-review.json:18-21`, `ExecCatProbes/probes.py:46-52`, `ScribeRound/receipts/base-false-green-r66.txt`):**
   - At base `86becbde…`, `cat big.txt missing.txt | head -n 1` produces `gate_rc = 0` (green), despite `native_statuses = [-13, 0]` and `untruncated_cat_rc = 1`. The SIGPIPE signal (-13) triggered by `head` closing the pipe early terminates `cat` before it reaches `missing.txt`. Because base `upstream_stale` treats all non-final SIGPIPE as benign, the missing file is masked.
   - Crucially, `ReviewCat` demonstrated that the reverse order (`cat missing.txt big.txt | head -n 1`) also yields `gate_rc = 0` at base: `cat` encounters `missing.txt` first and emits `cat: missing.txt: No such file or directory` to stderr, but then opens `big.txt`, streams data, and is killed by SIGPIPE (-13), overwriting its return code to -13. Base gate ignores -13, resulting in another false green.
2. **Candidate Implementation (`ExecCatGate/figure-audit.py:89-125`):**
   - Candidate `d48a5e45…` introduces `cat_sigpipe_exempt(argv)` and updates `upstream_stale(head, stage_argv, status)`. It strips a leading `"--"`, conservatively refuses non-dash options (`t.startswith("-") and t != "-"`), and allows at most 1 operand (`len(tokens) <= 1`).
   - Selftest cases expand from 63 to 67 (+4 production-path cases with 4 MiB fixtures), and 35/35 production ledger figures pass identically.
3. **Adversarial Boundary Probes (`CriticCat/probe.py:100-145`, `receipts/candidate-public.txt`, `collector-v2.py:53-110`):**
   - `separator-double-dash-name` (`cat -- -- | head -n 1`): first `--` is stripped; second `--` is an operand.
   - `separator-single` (`cat -- big.txt | head -n 1`): first `--` stripped leaves 1 operand (green).
   - `file-and-stdin-multi` (`cat big.txt - < other.txt | head -n 1`): `-` is an operand, totaling 2 operands (stale).
   - `P7-same-derive-small-twin` (`CriticCat/collector-v2.py:79-82`): when `big.txt` fits the pipe buffer (e.g. 64 KiB), `cat` completes without SIGPIPE (`native = [0, 0]`). A static text-arity filter falsely marks it stale, whereas runtime status gating correctly keeps it green.
4. **Harness / Caller Compatibility Substrate:**
   - In base `corpus/instruments/figure-audit.py:83`, the signature is `upstream_stale(head, status)`. Mutation batteries (`figure-audit-mutbat.py`, `figure-audit-mutbat-r64.py`, `signal-mutbat-r65.py`) anchor on calls to `upstream_stale`. Changing `upstream_stale` to require 3 positional arguments risks breaking two-argument callers.

---

## 2. Affected Axes

- **`depth:verifiability` (Targeted, Improved):**
  - Falsifies the baseline false green on multi-operand `cat` pipelines under SIGPIPE.
  - Prevents false-stale regressions on single-file pipelines using `--` option separators.
  - Discriminates runtime SIGPIPE from benign small-file completion (P7).
  - Shields caller compatibility by avoiding broken signatures in harness mutations.
- **`coverage` (Held at 8; Unharmed):**
  - No new knowledge or frontier entries admitted. Bounded strictly to instrument repair.
- **`depth:density` (Held at 9; Unharmed):**
  - No alteration of density metrics or word count definitions.

---

## 3. Proposed Move: Synthesized Bounded Contract

Integrate a **Dual-Phase Decoded-Operand Normalizer with Signature-Preserving Upstream Guard**:

1. **Stream-Normalized Operand Counting (`cat_sigpipe_exempt`):**
   - Strip exactly one leading `"--"` token from `argv[1:]` if present.
   - Any token starting with `"-"` (except lone `"-"`) triggers conservative refusal (fail-closed, returns `False`).
   - Count remaining tokens as input streams: each file token counts as 1 stream; lone `"-"` counts as 1 stream.
   - Exemption holds iff total input stream count $\le 1$.
2. **Signature-Preserving Default Parameter:**
   - Define `def upstream_stale(head, status, stage_argv=None):` or support flexible parameter ordering.
   - If `stage_argv is None`, preserve the legacy fallback behavior, while `run_derive` supplies the full decoded `argv` slice.
3. **Dual-Order Falsification Battery:**
   - The committed-input driver must retain both `P1` (missing second: `cat big.txt missing.txt | head -n 1`) and `P1b` (missing first: `cat missing.txt big.txt | head -n 1`) to ensure neither signal overwriting nor stderr suppression can bypass the gate.
4. **Dynamic Runtime Status Gating:**
   - The check `status == -signal.SIGPIPE` must remain strictly evaluated at runtime before operand inspection, ensuring that small-file pipelines that do not trigger SIGPIPE (P7) remain green.

---

## 4. Risks & Explicit Contradictions

1. **Conservative Refusal of Valid Single-File Options:**
   - Commands like `cat -n big.txt | head -n 1` will be refused as stale even though only one file is read.
   - *Classification:* Acceptable fail-closed capability boundary (named in module docstring). Does not affect any of the 35 production ledger figures.
2. **Static vs. Dynamic Oracle Contradiction:**
   - An AST-only oracle that refuses any `cat` with multiple arguments without checking `status == -13` will falsely reject `P7` (where both small files complete with exit 0).
   - *Resolution:* The gate must check `status == -signal.SIGPIPE` first, applying operand inspection only to SIGPIPE'd stages.
3. **Pipe Buffer Size Sensitivity:**
   - Deterministic SIGPIPE delivery requires the producer's output to exceed the operating system's pipe buffer ($64\text{ KiB}$).
   - *Mitigation:* Selftest and counter battery fix fixture sizes to $\ge 4\text{ MiB}$ (well above any standard OS buffer).
4. **Finite Claim Boundaries:**
   - Other multi-file heads (`head -q -n ... big.txt missing.txt | head -n 1`) and wrapper scripts (`python3 wrapper.py | head -n 1`) remain unaddressed by this repair. This is an intentional finite claim, not broad sandbox error detection.

---

## 5. Verification Plan

1. **Counter Battery:** Execute `probes.py` with 8 probes (P1–P8). Base must fail exactly P1, P2, P8 (probes=8, failures=3); candidate must pass 8/8 (failures=0).
2. **Selftest Pin:** Run `figure-audit.py --selftest` on candidate (assert `cases=67 failures=0 exit=0`).
3. **Production Non-Regression:** Run `figure-audit.py --ledger corpus/instruments/figure-audit-ledger.json` across base and candidate (assert identical `figures=35 ok=35 stale=0 exit=0`).
4. **Signature Compatibility:** Verify that legacy two-argument invocations `upstream_stale(head, status)` execute without `TypeError`.
5. **Hygiene Verification:** Assert zero uncommitted tracked changes in lane working tree, and delete scratch `/fast/scratch/hyaku/kasegi-r66/ScopeCat` prior to wave yield.
