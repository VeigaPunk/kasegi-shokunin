# ExecC1Indep — independent C1 re-measurement (round 89, wave 1)

**Verdict: AGREE on every number.** An independent re-implementation of the knowledge-scope meter reproduces C1's frozen predicates exactly at the C1 landing `eb5f0df8eaceca617465e493c710e8626e9aa618`. No routed defects.

## Method (independent of the frozen counter)
- Own script `ExecC1Indep-receipts/indep_meter.py` imports only the lane instrument `corpus/instruments/resolve.py` (`collect`/`classify`; mirror root taken from `resolve.MIRROR_ROOT`, absent on this host — matching the counter's `mirror_absent=True`, so mirror-classified citations count truthfully GONE). It **never imports** `.ufo/waves/round-89/c1/knowledge-meter.py`.
- Scope = every `corpus/knowledge/*.md`, materialized at base `090a46f89932324787e00ca20b1007f893934c9a` and at the C1 landing via `git show <rev>:<path>` into scratch (working tree never read for any measurement).
- Classification lane: `git clone --shared` of the lane into scratch, toplevel asserted equal to the clone dir, then `git -C <clone> checkout eb5f0df8…` inside the clone.
- M9 re-checked by an independent parse of `labels.tsv` against `git show d0d9f49241420456f2373f62e417f8fa56a0f7d5:.ufo/waves/round-88/w1/ReviewC1Semantics.md` (216 lines; all 9 cited rows exist at the cited line numbers).

## Numbers — agree/disagree per number

| # | Measure | Claim / expectation | Independent result | Verdict |
|---|---------|--------------------|--------------------|---------|
| 1 | base rate | 777/1798 | 777/1798 | **AGREE** |
| 2 | after rate | 785/1797 | 785/1797 | **AGREE** |
| 3 | removed token set | exactly the 9 map keys | 9 == map keys, no strays | **AGREE** |
| 4 | added token set | subset of map values | 8 of 9 values (see qualifier) | **AGREE** |
| 5 | unrepaired keys in after | 0 | 0 | **AGREE** |
| 6 | line diff | every changed line = base line under only the 9 backticked substitutions; 9/9 keys present at base | 100 scope files, same file set, same per-file line counts, 0 bad lines under BOTH chained-replace and single-pass regex; 9/9 keys hit | **AGREE** |
| 7 | binding + range (M4/M5 recomputed) | keys GONE at base; values INTERNAL at landing, only tracked basename outside `.ufo/`, anchors in range | 0 problems | **AGREE** |
| 8 | M9 label binding | 9/9 rows bound to review lines | 9/9 OK (own parse, table below) | **AGREE** |
| 9 | frozen counter on fresh shared clone | pass rc=0 | pass rc=0 (output pasted below) | **AGREE** |
| 10 | P2 instrument pins at C1 landing | all equal | 15/15 pass | **AGREE** |

## M9 rows (own parse; review file at `d0d9f492…`, whole-token `L<N>`/`L<N>-<M>` anchors)
```
map==labels: yes (9 pairs)
L45   claim-gates.md:34                  WRONG OK   (regex is L35)
L46   claim-gates.md:35-36               WRONG OK   (needs L36-37)
L48   claim-gates.md:63-66               WRONG OK   (heuristics are L78-80)
L49   claim-gates.md:66-67               WRONG OK   (guard is L81-85)
L54   claim-package-contract.md:28-29    WRONG OK   (hard gates are L52-53)
L103  claim-gates.md:10-11               FN    OK   (L10-11 six-file list; anchors equal)
L106  claim-package-contract.md:15       FN    OK   (L15 provenance row; anchors equal)
L107  claim-package-contract.md:9-16     FN    OK   (L9-16 six-file table; anchors equal)
L116  ops-invariants.md:17-25            FN    OK   (L17-25 shared constants; anchors equal)
```

## Qualifier (observation, not a defect)
The added-token set has **8** entries, not 9: `corpus/knowledge/claim-package-contract.md:15` already existed at base (one occurrence in `corpus/knowledge/claim-package-gate.md`), so the `:15` prefix repoint at `triage-thresholds.md:241` changes an occurrence, not the distinct-token set. M2 is defined as a subset check (`stray_added=0`), and the frozen counter agrees; nothing to fix.

## Frozen counter output (verbatim, run once on a fresh `git clone --shared` of the lane checked out at `eb5f0df8…`, pins from claims.json)
```
KNOWLEDGE-METER base=777/1798 after=785/1797 target=785/1797 keys=9 mirror_absent=True
LIMB M1 pass after=785/1797
LIMB M2 pass removed=9 keys=9 stray_removed=0 stray_added=0 unrepaired=0
LIMB M3 pass same_files=True bad_lines=0 keys_hit=9
LIMB M4 pass bad=none
LIMB M9 pass labels=9 unbound=none
LIMB M5 pass out_of_range=none
LIMB M7 pass sha256=8aed5bded717a92df78943ea41332bd3a46b90858ec1396bc797eec85644050d
LIMB M6 pass sha256=c29f4c2186ed13495a9b03866f2412c6da5b95f7425b93f7dd1675a986d0e2ec
KNOWLEDGE-METER-RESULT pass rc=0
```
(Also pasted in `ExecC1Indep-receipts/counter-out.txt`; independent run in `indep-out.txt`, ends `INDEP-METER-RESULT pass` rc=0; pins in `pins-out.txt`.)

## Re-run
```
bash .ufo/waves/round-89/w1/ExecC1Indep-receipts/driver.sh   # scratch paths inside; creates its own shared clone
```

## Hygiene
- No credential-shaped values in any wave file: receipts carry digests, counts, LIMB lines and label-binding lines only; no fixture bytes; the scanner, the frozen counter and no `S<digits>.txt` snapshot were copied into the wave dir.
- Scratch `/fast/scratch/hyaku/kasegi-r89/ExecC1Indep` (incl. the shared clone and both scope trees) **deleted before yield** — gone.
- Tools installed: none.
