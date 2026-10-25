# Q1Executable — critic report: r22 "five prose rechecks exit 2", exact parsing, executable replacement contract

Scope: read-only audit of `claims.json`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-22*.md`, the five F01–F05 headers, the new F06–F08 headers, `corpus/instruments/source-recheck.py`, and `corpus/source-snapshots/round-23/`. Working tree is at `922a4dde` plus uncommitted wave artifacts. No production edits; no self-credit.

## Evidence

1. The r22 verifier's signal is ungrounded: `round-22-verifier-spotcheck.md` says the five prose rechecks "exit 2" but never names the executor. `sh -c 'On each FIRST …'` exits 127, `python3` exits 1 — no obvious runner yields 2. R3 requires a verdict to name its matcher; the recorded "exit 2" is unreproducible, so "no longer exit 2" is unfalsifiable.
2. Q7 (`QUALITY.md` diff) literal trigger "prose beginning 'On each'" under-captures: of the five flagged fields only `cvss-v4-severity-and-vector.md`, `authorization-safe-harbor-and-scope.md` (begins "On platform-policy"), and `cwe-top25-2025-methodology.md` (begins "On release") start with "On …"; `coordinated-disclosure-timelines.md` and `ai-assisted-finding-validation.md` begin "Annually". A verifier applying Q7's literal wording re-admits 2/5 of the mined defect.
3. The five prose fields are still prose in the working tree (`grep '^recheck: ' corpus/knowledge/{cvss,coordinated,authorization,ai-assisted,cwe}*`) — the M2 correction currently lands only on new F06–F08 entries; the actually-flagged 5/8 admitted frontier entries keep non-executable `recheck:` lines.
4. The replacement commands themselves still exit 2 today: the three new entries' `recheck:` fields run `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S0NN`, and `corpus/source-snapshots/round-23/` contains `S018.txt`, `S029.txt`, `S030.txt` but **no manifest.json**. Observed: `python3 corpus/instruments/source-recheck.py --manifest … --source S018` → `manifest UNAVAILABLE reason=missing`, `exit=2`.
5. Exit-code collision built into the contract: the verifier used 2 = "not executable"; the new tool uses 2 = UNAVAILABLE (`source-recheck.py:74-112,149`). Once the manifest exists, a deleted/corrupt snapshot correctly exits 2 — an acceptance predicate keyed on the integer either forces honest UNAVAILABLE into disguise or rejects correct fail-closed behavior.
6. Dual sha256 authority: `opened-source-snapshots.json` and `manifest.json` each pin a sha256 for the same snapshot files; nothing checks they agree. They can silently diverge (R2/R9 class).
7. Freshness laundering opening: F07/C2 claim "current CNA operational rules". The recheck only proves pinned snapshot bytes; CVE publishing v4.3.0 tomorrow leaves every check green while "current" rots. S030's `teaches` cell already says "use current 4.2.0 requirements" — currentness was established once at open time (2026-10-20) and is not recheckable locally. Q7's second sentence covers the tool's own output language but not the entry/claim text.

## Falsifier (strongest counterexample, observed not inferred)

Run the F06 declared recheck verbatim from the lane root:
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018` → prints `manifest UNAVAILABLE reason=missing`, exits **2**. The "executable replacement" for M2 currently reproduces the same exit integer the r22 verifier counted as the defect, because the manifest is absent. If acceptance is "exits 0", it fails today; if acceptance is "exits ≠ 2", it fails permanently by design (UNAVAILABLE is a legitimate 2).

## Smallest warranted corrections (in priority order)

1. **Define the executable predicate by output grammar, not exit code.** Acceptance: the `recheck:` line executed verbatim under the declared runner (state the runner: `sh -c` from lane root) emits the tool's stable verdict lines (`<id> OK|MISMATCH|UNAVAILABLE`), with ≥1 `OK` id for a healthy pass. Prose under the same runner emits no verdict id — that is the red-before control. Integer exit codes alone distinguish nothing.
2. **Widen Q7's literal wording** from "prose beginning 'On each'" to "a field that is not a single verbatim-executable command line"; 2/5 mined offenders begin "Annually".
3. **Close M2 on the flagged files, not only the new ones**: replace the five F01–F05 `recheck:` fields with runnable commands (they cite remote URLs, so snapshot-pin them the same way as F06–F08) or record them as named residual debt — silent persistence contradicts `supporting_corrections` M2.
4. **Commit `manifest.json` before any entry may cite it in `recheck:`**; make it the single sha256 authority (have `opened-source-snapshots.json` reference rather than re-pin, or add a cross-check line to the tool).
5. **Scope "current" claims to the pinned version+date** (e.g., "CNA Operational Rules v4.2.0, effective 2026-08-25, opened 2026-10-20"); the local recheck asserts snapshot integrity only, never upstream currency.

## Impacted axes / scope limits

- depth:verifiability — the executable-recheck detector contract (items 1,4,5) is the axis move; without fix 1 the correction is unfalsifiable. coverage — F06–F08 admission gates on these rechecks (items 4,7); F01–F05 prose fields (item 3) touch the same admission bar. No verdict on C1 mirror work; no install performed; findings bounded to observed tree state — if the manifest lands in a later wave artifact, item 4's observed exit 2 remains the recorded pre-integration evidence, not a prediction.
