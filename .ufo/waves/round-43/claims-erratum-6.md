# Round-43 claims erratum 6 — appended in round 44

Correction (round 43): the C1 before-cell's `closed=13/19 exit=1` base figure is superseded. No committed run of the landed `r43-closure.sh` exists at base `ab98fac9dce87130bc4f66de89e30650d63943dc`; the cited 13/19 figure came from a draft/stub suite, while committed seat receipts reported different counts. Do not use 13/19 as a measured base result. The supported base evidence is that `r43-closure.sh` is absent at base and the r42 stand-in prints `closed=12/13 exit=1` there (`.ufo/waves/round-43/c1-controls/do-nothing.txt`).

Correction (round 43): the before-cell's missing-suite `exit 127` is a direct `bash corpus/instruments/r43-closure.sh` attempt on the exported base, not a value printed by `c1-controls/do-nothing.txt`; that control's `exit=2` belongs to its failed `ls` in §A. Round-44 receipt `.ufo/waves/round-44/controls/missing-suite-base.txt` records the direct command and its exit. The two values describe different commands; the before-cell must not attribute the 127 result to the control receipt.

Both corrections are append-only and use `superseded` as the frozen K17 vocabulary. The claims.json bytes and their original frozen predicate are unchanged.

Clarification (round 44): the cited control contains the string `127` at line 41 only as quoted round-42 before-cell prose; it is not a measured exit from the r43 command. Its measured §A operation is `ls corpus/instruments/r43-closure.sh`, which returns exit 2. The direct `bash corpus/instruments/r43-closure.sh` replay at exported base `ab98fac9dce87130bc4f66de89e30650d63943dc` returns exit 127, as captured in `.ufo/waves/round-44/controls/missing-suite-base.txt:1-6`.
Correction (round 44): the preceding paragraph mislabels the `closed=13/19` token as the C1 before-cell. It is in the C1 after-cell (`claims.json:41`); the before-cell says `closed=12/13`. The round-43 verifier spotcheck's §6.1 description also mislocates that token. R44Critic2 ran the committed current `r43-closure.sh` against `--export-ref ab98fac9dce87130bc4f66de89e30650d63943dc` and recorded `closed=12/19 exit=1`, with K8 and K14–K19 open (`.ufo/waves/round-44/wave1/R44Critic2.md:21-50`). This is a seat report, not a committed `final-gates` base receipt; it contradicts rather than supports the frozen 13/19 after-value. K17 skips after-cells and K18 already treats 13/19 as superseded from the spotcheck prescription itself (`R44Critic2.md:54-93`), so the appended prose does not verify or close C1. C1 remains unverified.
R44 score disposition (append-only): neither frozen claim is admitted as a score-bearing result. C1 is unverified: the drafted counter accepted a marker-only after-tree, was removed, and its selftest is not a verifier (`.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`; `R44Critic1.md`, `R44Critic2.md`). C2 is unverified: the frozen counter reads 0 in both worlds, and no independent nonauthor admit/reject spot-check was obtained (`controls/c2-frozen-counter-replay.txt`; `R44Critic11.md`). The corrected diagnostic counts show the corpus additions, not satisfaction of the frozen claims. Hold scores; do not infer a score delta from the word “target.”
## Round-44 capability disposition

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 44 | depth:verifiability | 4 (round-43 score) | 4 held; C1 unverified, no delta | `.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`; `wave1/R44Critic1.md`, `R44Critic2.md` |
| 44 | coverage | 8 (round-43 score) | 8 held; C2 unverified, no delta | `.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt`; `wave1/R44Critic11.md`; no independent nonauthor spot-check |
| 44 | depth:density | 9 (round-43 score) | 9 held; no target or measurement | `.ufo/waves/round-44/controls/do-nothing.txt` |

The frozen C2 counter `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` prints 0 at both the frozen base and the after tree; it cannot certify F26. The *different* table-aware diagnostic in `controls/c2-counter-audit.txt` returns 25→26, with registry rows 68→70 and knowledge files 62→63. These are structural observations, not a C2 verdict. C1's draft counter is rejected for accepting a marker-only false-green; it was removed from production paths. Round-44 score changes: none. Saturation: unchanged; the lowest non-retired axis remains depth:verifiability at 4.

### Planned evidence gates for round 45

- `depth:verifiability`: freeze a counter over committed artifacts and require red on both the do-nothing export and marker-only mutants before scoring; a correction paragraph alone cannot satisfy a defect.
- `coverage`: freeze a table-correct counter and committed-export basis, then obtain a nonauthor admit/reject spot-check before claiming coverage movement.
