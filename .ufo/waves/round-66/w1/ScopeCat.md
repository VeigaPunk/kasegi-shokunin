# ScopeCat — Round 66 Wave 1 Scoped Scope Screen and Synthesis Report

**Seat:** ScopeCat (connector, leaf)  
**Round:** kasegi r66 wave w1  
**Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`  
**Base:** `b6db9e818d322726e39cb441f2179d34d4170275`  
**Judged axis:** `depth:verifiability` (nominal R58, score 4 held)  
**Milestone:** predata cat SIGPIPE masking repair and falsification  
**Role:** UFO-FSD connector / cross-surface scope screen  

---

## Executive Summary

1. **Cross-Surface Scope Screen:**  
   The planned cat gate work in `corpus/instruments/figure-audit.py` is an **internal instrument repair** of kasegi's verification substrate. It audits figure derivations in kasegi's own documents. Sibling domains (`chousa` for research methodology, `kengaku` for model evaluation, `kumitate` for swarm orchestration and process execution) are adjacent and reported out; no sibling scope is absorbed, and no domain expansion is asserted.
2. **Considerthese Proposal 2 Disposition:**  
   Repairing `figure-audit.py` to fix multi-operand `cat` SIGPIPE masking confers **ZERO domain-task completion credit** towards Proposal 2 (`considerthese/2026-10-26.md:30`) or SHONEN Box 2. Proposal 2 requires an end-to-end six-file bounty claim package and pricing exercise; it remains **partially landed / domain task open**, and SHONEN Box 2 remains **`[ ]`**.
3. **Round 65 Routed Defects Mapping:**  
   All six routed defects identified in `corpus/lessons/round-65-verifier-spotcheck.md:132-152` are mapped to concrete round 66 record corrections (enforcing LOG bullet indices instead of "bolts", 100% commit reconciliation for unlisted commits `1929a47` and `6824522`, citing exact final driver SHA `7f27c4d2`, distinguishing measured commit `03a23921` from tip `a3357329`, capturing explicit exit codes in all receipts, and clarifying per-run invocation counts).
4. **Connector Synthesis Move:**  
   A non-obvious move synthesizes the round's proposals: a **Dual-Phase Decoded-Operand Normalizer with Signature-Preserving Upstream Guard**. It strictly normalizes input streams (handling `--` option separators, treating lone `-` as a stream, and conservatively refusing options), preserves backward compatibility with two-argument `upstream_stale` callers, incorporates dual-order operand failure controls (`cat missing big` and `cat big missing`), and enforces dynamic runtime status gating (`status == -signal.SIGPIPE`) to prevent false rejections of benign small-file runs (P7).

---

## 1. Cross-Surface Scope Screen Table (PROVINCE Inspection)

| Lane | Province Domain & Ownership | In-Scope Surfaces | Explicit Refusals & Boundary Rules | Cat Gate Work Fit & Adjacency Disposition |
|---|---|---|---|---|
| **kasegi-shokunin** *(Own)* | Bounty & security research: scopes `~/Projects/bounties` (absent), program rules, claim packages, triage/claim gates, submission packaging (`PROVINCE.md:1-26`). | `corpus/knowledge/`, `corpus/lessons/`, in-lane gate instruments (`corpus/instruments/figure-audit.py`, `figure-audit-mutbat.py`, `figure-audit-ledger.json`). | Refuses live-target testing; refuses anything outside domain. Cross-domain evidence reported out, not absorbed (`PROVINCE.md:25`). | **OWNED IN-LANE INSTRUMENT REPAIR.** `figure-audit.py` audits kasegi figure citations against shell derives. Fixing multi-operand `cat` SIGPIPE masking deepens `depth:verifiability` (nominal R58, score 4 held) without expanding domain scope or claiming bounty execution. |
| **chousa-shokunin** *(Sibling)* | Deep-research method (調査): craft of source research, question framing, source hierarchy, citation chaining, claim-vs-source verification (`chousa/PROVINCE.md:1-8`). | Research taxonomy, claim verification protocols, search strategy, external-target approval tables, chousa corpus/gates. | Explicitly refuses bounty-program scope & claim packages (`→ kasegi`); refuses model eval (`→ kengaku`); refuses orchestration (`→ kumitate`); refuses secrets (`→ kagi`). `PROVINCE.md:17`: "Out of province → report, never absorb." | **ADJACENT; NOT ABSORBED.** Chousa owns general source-verification methodology, but kasegi's `figure-audit.py` is an internal verification gate for local figure derivations. Kasegi maintains its own instruments and reports out findings without modifying chousa's research domain. |
| **kengaku-shokunin** *(Sibling)* | LLM / model research & evaluation: model eval craft, benchmark batteries, model serving interpretation (`kengaku/PROVINCE.md:1-6`). | Eval notes (`llm-wiki`), benchmark batteries (`bench-arena`), served model telemetry/endpoints, in-repo gate `grader.py`. | Explicitly refuses model serving plane; refuses kagi vault/secrets; refuses kumitate orchestration; refuses kasegi bounty ledger mission-state / dispatcher semantics (`kengaku/PROVINCE.md:26-36`). | **ADJACENT; NOT ABSORBED.** Kengaku benchmarks model outputs and autonomous capabilities. Kasegi's `figure-audit.py` evaluates deterministic Unix pipeline execution for document figures, not model capabilities. S091–S094 citations in kasegi are documented finding accounts; model eval stays adjacent in kengaku. |
| **kumitate-shokunin** *(Sibling)* | Orchestration & tooling: OMP task/hub, ufo-fsd runtime & scripts, process supervision, isolation substrates (`kumitate/PROVINCE.md:1-6`). | Origin scripts (`ufo-fsd-alpha/scripts/`), runtime crates (`ufo-core-runtime`, `ufo-cli`), Kimi substrate, isolation substrates, durable execution research (`kumitate/PROVINCE.md:8-28`). | Refuses MCP/OAuth security practice (`→ kasegi / kagi`); refuses local model serving (`→ kama`); refuses prompt craft (`→ kotoba`); refuses research method (`→ chousa`). Refuses upstream live patches (`PROVINCE.md:29-33`). | **ADJACENT; NOT ABSORBED.** While pipeline mechanics (SIGPIPE, exit codes, process group supervision) are tooling-adjacent, `figure-audit.py` is kasegi's internal audit instrument for its own repository claims. Kumitate owns the execution runtime of the swarm host; kasegi owns its figure-audit gate. Kasegi does not absorb kumitate's runtime scope, nor does it export `figure-audit.py` into kumitate. |

---

## 2. Considerthese Proposal 2 and Held Package Task

- **Proposal 2 Content (`considerthese/2026-10-26.md:30`):**  
  Asks to run one end-to-end domain task round to uncheck SHONEN Box 2 by taking a public disclosed vulnerability report (H1 Hacktivity or Immunefi), constructing the six-file claim package (`manifest.json`, finding description, vulnerability analysis, reproduction script/test, severity pricing, remediation advisory) under `corpus/knowledge/claim-package-contract.md`, and pricing it through F13/F17/F18.
- **Documented Ledger Disposition:**  
  In `corpus/knowledge/considerthese-proposals-ledger.md:168-172`, Proposal 2 is recorded as:
  `partially landed / domain task open → partially landed / domain task open`.
- **Determination for Round 66:**  
  The current milestone is an **instrument repair** (`figure-audit.py` SIGPIPE masking fix). It enhances verification rigor, but does not execute a domain task, construct a claim package, or price a vulnerability.
  **Conclusion:** **ZERO domain-task completion credit is conferred from instrument repair.** Proposal 2 remains **partially landed / domain task open**, and SHONEN Box 2 remains **`[ ]`**.

---

## 3. Mapping of Round 65 Verifier Routed Defects

Mapped from `corpus/lessons/round-65-verifier-spotcheck.md:132-152`:

1. **Defect 1: Report commit→LOG ties cite non-existent labels ("LOG bolts 1–12").**  
   *Root Cause:* Report used informal term "bolts" while `LOG.md` had 10 bullets.  
   *Round 66 Correction:* Use exact bullet citations (e.g. "§ Round 66 bullet N") or direct line ties in `LOG.md`; "bolts" is strictly forbidden.
2. **Defect 2: Two round commits missing from Landed-changes table (`1929a47`, `6824522`).**  
   *Root Cause:* Errata commits were added post-drafting without reconciliation against `git rev-list --count`.  
   *Round 66 Correction:* Strict 100% commit inventory reconciliation against `git rev-list --count base..tip`. ScribeRound append-only draft explicitly cites both `1929a47` and `6824522`.
3. **Defect 3: "Exact final driver" label cited before receipt from `base-finaldrv2` (`5aa842ab…`).**  
   *Root Cause:* Cited intermediate erratum-1 driver instead of final driver receipt `controls/driver-base-donothing-r65.txt` (`7f27c4d2…`).  
   *Round 66 Correction:* The baseline before receipt must strictly match the final driver SHA (`7f27c4d2…`). Round 66 drivers ensure baseline donothing receipt matches the final frozen driver hash.
4. **Defect 4: "Final tip" receipt named revision `03a23921`, while lane tip was `a3357329`.**  
   *Root Cause:* Measured at code-complete commit `03a23921`, followed by 2 receipt-only commits.  
   *Round 66 Correction:* Explicitly name measured revision (`03a23921`) and document receipt-only delta to tip (`a3357329`), or re-run driver at pushed tip.
5. **Defect 5: Base receipts record no exit code (`failures=3` without `exit=` line).**  
   *Root Cause:* Driver output printed failures but omitted process return code on failure.  
   *Round 66 Correction:* Every driver, probe, and selftest receipt MUST output an explicit `exit=<rc>` / `rc=<rc>` line. Never leave return code implicit.
6. **Defect 6: Sentinel helper-count phrasing ("executed a helper 121900 times").**  
   *Root Cause:* Quoted aggregate executions across 2 runs without stating run divisor.  
   *Round 66 Correction:* Disclose iteration count and per-run breakdown (e.g. "~60,950 invocations/run across 2 runs = 121,900 total invocations").

---

## 4. Connector Synthesis Proposal: Non-Obvious Move

### Bounded Move
**Dual-Phase Decoded-Operand Normalizer with Signature-Preserving Upstream Guard**

### Evidence
- At base `86becbde…`, `cat big.txt missing.txt | head -n 1` yields exit 0 (green) despite native status `[-13, 0]` and untruncated cat failing (`rc=1`).
- `ReviewCat` demonstrated dual-order masking: `cat missing.txt big.txt | head -n 1` emits stderr `cat: missing.txt: ...` but is killed by SIGPIPE on subsequent writes, overwriting its exit code to -13 and yielding a false green at base.
- `CriticCat` probed boundary conditions (`--` separator, `-- --` literal filename, lone `-` stdin operand) and demonstrated that small-file twin `cat big.txt other.txt | head -n 1` (P7) completes with exit 0 and native `[0, 0]`.
- Existing mutation test batteries (`figure-audit-mutbat.py`, `signal-mutbat-r65.py`) anchor on two-argument calls to `upstream_stale`.

### Affected Axes
- **`depth:verifiability` (Targeted, Improved):** Falsifies multi-operand SIGPIPE masking across both operand failure orders, prevents false-stale regressions on option separators (`--`), preserves runtime discrimination over static text-arity heuristics, and maintains backwards compatibility with two-argument callers.
- **`coverage` (Held at 8; Unharmed):** Bounded strictly to instrument repair; no new knowledge/frontier entries.
- **`depth:density` (Held at 9; Unharmed):** No alteration of density formulas or assertion density.

### Proposed Move
1. **Decoded Input Stream Counting (`cat_sigpipe_exempt`):**
   - Strip exactly one leading `"--"` token from `argv[1:]` if present.
   - Refuse any token starting with `"-"` (except lone `"-"`) fail-closed as an unparsed option (conservative refusal).
   - Count remaining tokens as input streams: file operand = 1 stream, lone `"-"` = 1 stream.
   - Exemption holds iff total input stream count $\le 1$.
2. **Signature-Preserving Default Parameter:**
   - Define `def upstream_stale(head, status, stage_argv=None):` to maintain backward compatibility with legacy harness callers, while `run_derive` passes decoded `stage_argv`.
3. **Dual-Order Falsification Battery:**
   - Ensure committed-input counter driver incorporates both `P1` (missing second: `cat big.txt missing.txt | head -n 1`) and `P1b` (missing first: `cat missing.txt big.txt | head -n 1`), verifying neither signal overwriting nor stderr suppression bypasses the gate.
4. **Dynamic Runtime Status Gating:**
   - Enforce `status == -signal.SIGPIPE` before operand inspection, ensuring small-file pipelines that do not trigger SIGPIPE (P7) remain green.

### Risks
1. *Conservative Option Refusal:* `cat -n big.txt | head -n 1` is judged stale even though single-file. (Acceptable fail-closed capability restriction; zero impact on the 35 production figures).
2. *Pipe Buffer Sensitivity:* Producer output must exceed OS pipe buffer ($64\text{ KiB}$). Addressed by pinning fixture sizes to $\ge 4\text{ MiB}$.
3. *Non-Cat Heads:* Multi-file `head` and wrapper scripts remain unexempted by design under the finite C1 claim.

### Verification
1. Counter battery `probes.py` (8 probes: P1–P8): candidate achieves 8/8 pass; base fails P1, P2, P8.
2. Candidate `figure-audit.py --selftest` achieves 67/67 pass.
3. Production ledger replay (`figure-audit.py --ledger corpus/instruments/figure-audit-ledger.json`) achieves identical 35/35 figures pass.
4. Legacy signature verification `upstream_stale('grep', 1)` executes without `TypeError`.

---

## 5. Tooling & Hygiene

- **Tooling Directive:** Followed `/home/vgpnk/.omp/agent/RULES.md`. No tools installed or upgraded. Used existing system `python3` (3.14.8), `git`, and GNU coreutils. All pacman transactions paused.
- **File Isolation:** Wrote only to `.ufo/waves/round-66/w1/ScopeCat/` and this report `.ufo/waves/round-66/w1/ScopeCat.md`. Production, fleet, and sibling files untouched.
- **Scratch Hygiene:** Used `/fast/scratch/hyaku/kasegi-r66/ScopeCat`. All temporary artifacts cleaned before yield.

---

## Retained Receipts and Durable Deliverables

(Paths relative to `kasegi-shokunin`)
- `.ufo/waves/round-66/w1/ScopeCat/province-cross-surface-screen.md`
- `.ufo/waves/round-66/w1/ScopeCat/considerthese-proposal2-disposition.md`
- `.ufo/waves/round-66/w1/ScopeCat/r65-routed-defects-map.md`
- `.ufo/waves/round-66/w1/ScopeCat/connector-synthesis-proposal.md`
- `.ufo/waves/round-66/w1/ScopeCat.md`
