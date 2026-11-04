# Cross-Surface Scope Screen: Own and Sibling Provinces

**Seat:** ScopeCat (connector, leaf)  
**Round:** kasegi r66 wave w1  
**Base:** `b6db9e818d322726e39cb441f2179d34d4170275`  
**Judged axis:** `depth:verifiability` (nominal R58, score 4 held)  

---

## 1. Province Inspection & Adjacency Mapping

| Lane | Domain & Province Ownership | In-Scope Surfaces | Explicit Refusals & Boundary Rules | Fit for Cat Gate Repair (`figure-audit.py`) & Adjacency Disposition |
|---|---|---|---|---|
| **kasegi-shokunin** *(Own)* | Bounty & security research: program rules, scopes, claim packages, triage and claim gates, submission/disclosure packaging (`PROVINCE.md:1-26`). | `corpus/knowledge/`, `corpus/lessons/`, in-lane gate instruments (`corpus/instruments/figure-audit.py`, `figure-audit-mutbat.py`, `figure-audit-ledger.json`). | Refuses live-target testing; refuses anything outside bounty/security research domain. Cross-domain evidence reported out, not absorbed (`PROVINCE.md:25`). | **OWNED AS IN-LANE INSTRUMENT REPAIR.** `figure-audit.py` audits figures cited in kasegi's knowledge entries against shell derives. Fixing multi-operand `cat` SIGPIPE masking is an internal instrument repair of the lane's verification substrate (depth:verifiability). It does not expand domain coverage or claim bounty execution. |
| **chousa-shokunin** *(Sibling)* | Deep-research method (調査): craft of source research, question framing, source hierarchy (primary/secondary/aggregator), citation chaining, claim-vs-source verification (`chousa/PROVINCE.md:1-8`). | Research taxonomy, claim verification protocols, search strategy, external-target approval tables, chousa's own corpus and gates. | Explicitly refuses bounty-program scope and claim packages (`→ kasegi`); refuses model eval (`→ kengaku`); refuses orchestration (`→ kumitate`); refuses secrets (`→ kagi`). `PROVINCE.md:10-17`: "Out of province → report, never absorb." | **ADJACENT; NOT ABSORBED.** Chousa governs the general epistemological source hierarchy, but kasegi's `figure-audit.py` is a lane-local script auditing kasegi-specific document derivations. Kasegi maintains its own verification gates and reports local instrument findings without altering or absorbing chousa's research-methodology domain. |
| **kengaku-shokunin** *(Sibling)* | LLM / model research & evaluation: model eval craft, benchmark batteries, model serving interpretation (`kengaku/PROVINCE.md:1-6`). | Eval notes (`llm-wiki`), benchmark batteries (`bench-arena`), served model telemetry/endpoints, in-repo gate `grader.py`. | Explicitly refuses model serving plane (llama-server flags); refuses kagi vault/secrets; refuses kumitate orchestration; refuses kasegi bounty ledger mission-state / dispatcher semantics (`kengaku/PROVINCE.md:26-36`). | **ADJACENT; NOT ABSORBED.** Kengaku benchmarks model outputs and autonomous capabilities. Kasegi's `figure-audit.py` evaluates deterministic Unix pipeline execution for document figures, not LLM behavior. S091/S092/S093/S094 citations in kasegi are documented finding accounts, while model eval remains strictly adjacent in kengaku. |
| **kumitate-shokunin** *(Sibling)* | Orchestration & tooling: OMP task/hub, ufo-fsd runtime & scripts, process supervision, isolation substrates (`kumitate/PROVINCE.md:1-6`). | Origin scripts (`ufo-fsd-alpha/scripts/`), runtime crates (`ufo-core-runtime`, `ufo-cli`), Kimi substrate, isolation substrates, durable execution research (`kumitate/PROVINCE.md:8-28`). | Refuses MCP/OAuth security practice (`→ kasegi / kagi`); refuses local model serving (`→ kama`); refuses prompt craft (`→ kotoba`); refuses research method (`→ chousa`). Refuses upstream live patches (`PROVINCE.md:29-33`). | **ADJACENT; NOT ABSORBED.** While pipeline mechanics (SIGPIPE, exit codes, process group supervision) are tooling-adjacent, `figure-audit.py` is kasegi's internal audit instrument for its own repository claims. Kumitate owns the execution runtime of the swarm host; kasegi owns its figure-audit gate. Kasegi does not absorb kumitate's runtime scope, nor does it export `figure-audit.py` into kumitate. |

---

## 2. Key Scope Boundary Conclusions

1. **No Domain Expansion:** The repair of `figure-audit.py` is an instrument maintenance action that fixes false-green masking under `upstream_stale`. It deepens `depth:verifiability` (nominal R58, score 4 held) without expanding kasegi's domain scope.
2. **No Cross-Lane Absorption:** The pipeline execution fix does not encroach on `kumitate`'s orchestration domain, `kengaku`'s model evaluation domain, or `chousa`'s deep-research methodology domain. All cross-lane interfaces remain strictly adjacent and reported out.
3. **No Knowledge/Frontier Admission:** No new F-row, S-source, or knowledge entry is admitted in C1. Coverage remains held at 8.
