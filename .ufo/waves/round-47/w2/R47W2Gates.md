# R47W2Gates — integrated-tree frozen checks

Axes: depth:verifiability, coverage. Review is against the integrated tree supplied for this wave. No installs, domain-target actions, network access, battery, selftests, builds, linting, formatting, or git/jj mutations were performed. The five requested commands below were explicitly executed. Full stdout (including exit markers) is preserved in sibling receipts.

## Executed results

- `python3 corpus/instruments/r47-routed-defects.py --root .` — **exit 1**. Receipt: `R47W2Gates-c1.stdout`. Exact verdict: `routed-defects total=11 fixed=10 unresolved=1 exit=1`; L3 (D5) alone remains `fixed=0`, read `corrections-section-present content=0`. This is mechanical C1 green on the ten repair limbs, not full claim verification. Do not claim C1 fully met: the integrated S074 status stays mined historical because rejecting it would break B3; `corpus/SOURCES.md:176` records the old→new used-by transition, unchanged `90d`, and why rejection is unsafe.
- `python3 corpus/instruments/r47-f30-gate.py --root .` — **exit 1**. Receipt: `R47W2Gates-c2.stdout`. Exact verdict: `f30-gate fixed=6/7 exit=1`; H1 reads `rows=29 admitted=29 dup=0` and fails. C2 is not met: there is no F30 row. ZDI remains S075 enrichment of F02, not an F30 admission (`corpus/SOURCES.md:175`; round-47 lesson `corpus/lessons/round-47.md`, §Gate/decision).
- `./scripts/sources-census.sh census --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` — **exit 0**. Receipt: `R47W2Gates-census.stdout`. Rows 76; A=69, B=4, C=3; mined=61, rejected=15; fleet invalid tier/status=0, queued=0, missing=0.
- `python3 corpus/instruments/capture-binding-check.py` — **exit 0**. Receipt: `R47W2Gates-capture-binding.stdout`. `records=63 bound=63 unbound=0`; reports one orphan, `S040-live.txt`. It also reports 63 URL-bound records, digest-unpinned=0, and round-47 records=2, each URL-bound/fetched.
- `python3 corpus/instruments/recheck-audit.py` — **exit 0**. Receipt: `R47W2Gates-recheck-audit.stdout`. Strict 67/67; `executes=45 gated=22 broken=0`; lines 67/67 pass, fail-closed=22, parse/cwd/path failures=0; expected present, missing=0, unexpected=0.

## Review conclusion

The integrated tree passes census, capture-binding and recheck-audit mechanically. Neither counter is fully green: C1 returns 1 because of L3 (while the repair subset is 10/11), and C2 returns 1 because F30's H1 is absent (6/7). These are findings, not instructions to reroll the frozen targets. The C1 frozen counter does not encode the B3 no-harm decision around S074; the C2 count does not turn ZDI into independent F30 evidence. S075 is recorded as F02 coordinator evidence and S076 as the current reproducible F29 capture in `corpus/SOURCES.md:175`; S074's historical row and B3 constraint are explicit at `:176-177`.

Executed evidence is only the commands and output in the receipts listed above. Source-registry/lesson statements cited here were statically reviewed. No runtime/network/source recapture was performed. No blockers. No tools installed or updated.