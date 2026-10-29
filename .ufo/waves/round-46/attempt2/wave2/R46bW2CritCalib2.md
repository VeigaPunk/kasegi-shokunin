VERDICT: BROKEN

Scope: `git show -s` identifies `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` as the attempt-2 freeze and `96379ae26ef9443097b860ddb33ef924b2cd5b5a` as the wave-1 integration. Calibration below uses an archive of the latter; base readings use `04af9bc92229232ea5cce8b32bfe59dd969eb26d` (pure C1/C2 corpus: `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`).

## Findings

1. **C2 selftest calibration is false at integration.** `SCORECARD.md:1823,1831`, `SHONEN.md:341-343`, and `LOG.md:2025,2030` report the extended C2 selftest as `147/0` and describe the C2 mutation coverage as closed. In the integration tree, `corpus/instruments/r46-counters-selftest-c2.py:68-69` reads `C1_ENTRIES` before defining it. Re-run:

   ```text
   python3 -B <96379 export>/corpus/instruments/r46-counters-selftest-c2.py --lane <96379 export> --pure <914ca0 corpus export>
   Traceback (most recent call last):
     .../r46-counters-selftest-c2.py", line 68, in <module>
       EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}
   NameError: name 'C1_ENTRIES' is not defined
   exit=1
   ```

   The C2 battery control also fails before grading mutants: `r46-mutbat.py --root <96379 export> --pure <914ca0 corpus export> --work <scratch> --counter c2 --jobs 8` prints `mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1` and exits 1. In contrast, the integration C1 selftest did run cleanly: `selftest cases=83 failures=0` (exit 0). **Impacted:** `depth:verifiability` C1, plus SHONEN's agent-executability evidence. **Smallest safe correction:** define `C1_ENTRIES` before `EXEMPT_ENTRIES`, then rerun the C2 selftest and battery; do not retain `147/0` or C2 coverage-closed until those runs pass.

2. **After-value evidence cited by the new rows is absent from the integration commit.** `SCORECARD.md:1823` and `SHONEN.md:340-343` cite `controls/final-battery.txt`; `LOG.md:2028` cites `controls/final-measure.txt`. Against the 96379 export, the presence check printed:

   ```text
   final-measure.sh=present
   final-measure.txt=missing
   final-battery.txt=missing
   freeze-controls.txt=missing
   ```

   Thus the reported after-values have no committed receipt at this tree (independent of the C2 failure above). **Impacted:** `depth:verifiability` evidence/provenance and SHONEN's agent-executability evidence; C2 after-state is also not evidenced here. **Smallest safe correction:** commit the actual rerun receipts, or mark these cells pending until the receipts exist.

## Re-scan corroboration

- Do-nothing/frontier control: `r44-frontier-count.py --root <04af9 export> --expect 29` → `frontier rows=28 admitted=28`, `verdict=SHORT exit=1`; on 96379 → `frontier rows=29 admitted=29` (exit 0). Knowledge files: 65 → 66. The absence sweep names two matching files at base (S068 context, F28 scope note) and four at integration (adds README/F29 and the F29 entry). These plain C2 deltas match `SCORECARD.md:1824,1832`.
- On 96379, `source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` printed `S074:sha256 OK` and Q1–Q9 `OK`; `capture-binding-check.py --root <96379 export>` printed `records=61 bound=61 unbound=0`; `frontier-recheck-count.py --root <96379 export>` printed `entries=32 pass=32 exit=0`.
- `recheck-audit.py --root <96379 export> --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet` printed `strict pass=66/66 ... exit=0` and `expect=present expected=66 missing=0 unexpected=0 exit=0`. `anchorcheck.py SKILL.md` printed `16 in-range cite instances, 0 bad` (exit 0).
- `density.py` measured base 258.7 / 33 blocks and integration 275.1 / 34 blocks; its bytes were equal at both exports. This supports the scorecard's non-target density guard. `comm -12` over the committed assimilation receipts reproduced registry 74, staged 94, collisions 44; the ledger sizes were 30696 → 40843 bytes. These LOG values matched.

## Limitations

I did not run the full C1/C2 mutant battery or `r46-f29-gate.py` H7: the latter invokes the fleet-root census script, outside this seat's allowed lane boundary. The base C2 selftest `137/0` is present in `controls/selftest-baselines.txt` but was not rerun by this seat. No live page/target was tested. An unrun gate or full battery is not counted as passing.