# ScribeFrontier — round 30 frontier verification

## Scope and evidence

Verified the `corpus/README.md` frontier rows and F14 appendix against the frozen C2 claim (`.ufo/waves/round-30/claims.json`) and committed before-state receipts (`c2-controls/before.txt`, `census-before.txt`). The declared frontier counter is:

```sh
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
```

Measured current working-tree bytes: **14 admitted rows**; committed before receipt: **13**. The appended F14 row bytes are:

```text
| F14 | Japanese severity vocabulary and the handling-priority model | admitted | knowledge/japanese-severity-vocabulary-and-impact-model.md | S046, S047, S041 | Keep each 深刻度 band label attached to the CVSS version that produced it (v2 bands survive beside v3); JVN translates CVSS base scores into Japanese vocabulary rather than scoring independently, so derive handling priority from the P-guideline steps, not from the label alone. |
```

The row binds F14 to `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` and sources S046, S047, S041. README records the same entry and source binding in the round-30 coverage-map appendix and states **14/14 admitted**, F01–F14. `corpus/README.md` SHA-256 at measurement: `df04b0490591446c6605d421569a497845c22546dc27ea5a020fff770f2fc64f`.

Round-30 capture manifest binds S046/S047/S041 to their local capture files and SHA-256s; manifest digest `53c69065924dfc42b29bdecf3e2992eef453d79f3e6032a86b3e40d6e4a98e34`. Capture digests: S046 `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3`; S047 `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4`; S041 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`. Registry has 47 source rows (pre-state 45); `corpus/SOURCES.md` SHA-256 `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927`.

## Before → current measurements

| Check | Before receipt | Current working-tree run |
|---|---:|---:|
| Admitted frontier rows | 13 | 14 |
| Knowledge entries citing S046/S047 | 0 | 0 |
| SOURCES registry rows | 45 | 47 |
| Sources census | exit 0 | exit 1 (E11: S046 and S047 `used-by` paths missing) |
| Frontier harness | entries=16 pass=16 exit=0 | entries=17 pass=16 exit=1; F14 fails `missing-entry` |

Commands run for the current counters were the frozen C2 commands: frontier `awk` above; `grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md | wc -l`; `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`; and `python3 corpus/instruments/frontier-recheck-count.py`. No per-source `source-recheck.py` runs were performed by this seat. The mapped entry was absent from the knowledge tree at measurement, so these current failures are not converted into passing evidence. Frozen C2 kill-rule completion is therefore **not established by this report**.

## Frontier snippet for lesson/report

> **Coverage frontier:** the admitted public-practice frontier advanced from **13 to 14** rows. F14, “Japanese severity vocabulary and the handling-priority model,” is listed as admitted and binds the proposed entry `knowledge/japanese-severity-vocabulary-and-impact-model.md` to S046, S047 and S041. The README’s recorded denominator is **14/14 admitted**. At this measurement, the entry itself was not yet present: the frozen entry counter was 0 (expected 1), census exited 1 for missing S046/S047 `used-by` paths, and the frontier harness reported F14 `missing-entry` (16/17 pass). Thus F14’s README admission and source-row binding are present, but end-to-end admission checks remain unresolved in the measured bytes.

## Limits and surfaces

Read-only inputs included the lane’s frozen claims and before receipts, README, SOURCES, QUALITY, SCORECARD, round-29 lesson and verifier spot-check, plus the read-only shokuknow merge report, staged sources append and absent-defect register. The report file is the only file written by this seat. No product files, git/jj state, `.ufo/state`, or `MANIFEST.json` were changed; no tool was installed; no live bounty target was contacted. Checks are current working-tree measurements, not a commit-level or post-integration verification.