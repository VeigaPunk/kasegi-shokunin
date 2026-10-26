# CritCrossAxis — round-40 falsify wave 2: cross-axis harm (receipt)

Seat: CritCrossAxis (§critic, leaf — no subagent dispatch). Item attacked: cross-axis harm —
depth:density (SKILL.md append-only, density instrument unchanged, density mean not reduced),
calibration (SHONEN boxes' new pointers resolve; no fabricated `[x]`), adjacency (no absorbed
sibling ground). Lane state: judged head J = `3074c76` (J5); lane tip Y = J + untracked receipt
`.ufo/waves/round-40/final-gates/all-gates.txt` (final-gates dir is untracked at HEAD; SKILL.md /
SHONEN.md working-tree bytes == HEAD blobs). Base B = `a7af2ce63bce153757d39bf66b366a96caf30c13`.
All commands run read-only from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` or scratch
`/fast/scratch/hyaku/kasegi-r40/CritCrossAxis` (removed before yield). No tool installs (none
needed; python3 stdlib suffices). No lane/sibling/fleet file edited.

## 1. depth:density

| Check | Command | Result |
|---|---|---|
| Density instrument unchanged | `git rev-parse B:corpus/instruments/density.py HEAD:corpus/instruments/density.py` | both `1f99e66f883ac2ddfd4829e83b9c037f5f0742a5` (208 lines each) — identical |
| Anchor instrument unchanged | `git rev-parse B:corpus/instruments/anchorcheck.py HEAD:corpus/instruments/anchorcheck.py` | both `54200ebc85b3f0537f7094db4d8947c18129d31d` (563 lines each) — identical |
| SKILL.md append-only | `git diff --numstat B HEAD -- SKILL.md`; `git diff B HEAD -- SKILL.md \| grep -cE '^-[^-]'` | `7 0` insertions/deletions; deleted-line count 0. Base 1115 lines → HEAD 1122 lines. Only round-40 Gates & probes registry block appended |
| Density mean not reduced | `python3 density.py SKILL.base.md` vs `python3 density.py SKILL.head.md` (same instrument bytes) | BASE: mean **232.9** over 27 blocks, 771 path-citation instances (exit 0). HEAD: mean **233.5** over 28 blocks, 774 cites (exit 0). New block #28 "Round-40 Gates & probes registry addition" dens 250.0. Mean increased (232.9 → 233.5), not reduced |
| Anchor gate on final SKILL.md | `cd <lane> && python3 corpus/instruments/anchorcheck.py SKILL.md` | exit **0**; `16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` |

Verdict depth:density: **no harm.** Instrument byte-identical, SKILL.md strictly append-only,
density mean increased, anchor gate green. (Note: anchorcheck must run from the lane root or with
`KASEGI_LANE_ROOT` set — invoking it on a scratch copy mis-routes lane-relative cites and prints
spurious `BASE-ABSENT`; that is an invocation artifact, not a repo defect.)

## 2. Calibration (SHONEN boxes)

SHONEN.md base→HEAD delta is exactly the 5-line `## BLOCK SHONEN.md` correction block
(`git diff --numstat B HEAD -- SHONEN.md` = `5 0`); the four boxes and their prior evidence
lines are untouched. Every new pointer in the BLOCK block was re-opened against committed bytes:

1. "committed receipt at Y `8371e7ac9f32cae5ed72f8c28205634603f836fa` … all-gates v5, sha256
   8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471" —
   `git show 8371e7ac…:.ufo/waves/round-39/final-gates/all-gates.txt | sha256sum` =
   `8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471` **exact match**; header
   line `all-gates v5`; `closed=7/8 exit=1` (line 17); `selftest cases=8 failures=1` (line 79);
   `selftest-exit=1` (line 87); `selftest case=G2 positive=fail mutants=8/8 verdict=fail` (line 39);
   G2 payload `diff-clean=0 … closed=0` (line 10). **Reproduced.**
2. "8/8 exists only in the discarded attempt-1 receipt at `5006097a` (all-gates v3,
   `run-utc=2026-10-26T21:35:00Z`, after its containing commit)" —
   `git show 5006097a:.ufo/waves/round-39/final-gates/all-gates.txt` header `all-gates v3`,
   `run-utc=2026-10-26T21:35:00Z`; containing commit date `2026-10-26 17:12:12 -0300` =
   20:12:12Z → run-utc **after** the commit (future-dated). **Reproduced.**
3. "G2 accepts forged payload values (mut-f/g/h/j/k, `wave2/CritG2Exploit.md`)" —
   `.ufo/waves/round-39/wave2/CritG2Exploit.md` exists and records mut-f/g/h/j/k all `rc=0`
   with `g2_run_shapes` accepting empty payloads (`payload=… closed=1` shape). **Reproduced.**
4. "G6 depends on a scratch root the seats populate (`wave2/CritC1Kill.md`)" —
   `.ufo/waves/round-39/wave2/CritC1Kill.md` exists, records G6 default-root reds while seats are
   live (`closed=5/8`, `closed=6/8`, clean-clone @Y `closed=7/8` with G6 red). **Reproduced.**
5. "box 3 stays `[~]`, not independently verified" — `grep -c '\[x\]' SHONEN.md` = **0**
   (no fabricated `[x]`); all four boxes remain `[~]`; box 3 stays `[~]`.
6. Cross-record consistency: LOG.md and SCORECARD.md round-40 `Correction (round 40)` blocks name
   the same receipt values (v5 sha256 8d46d7b2…, 7/8, failures=1, attempt-1 5006097a future-dated).
   Consistent.

Observed calibration debit (pre-existing, NOT round-40-introduced): `anchorcheck.py SHONEN.md`
exits 1 on one `PAST-EOF md:70 PROVINCE.md:284-286 (file has 161 lines)` — the round-34-era box 4
evidence cites kake's `PROVINCE.md:284-286` unqualified and it resolves against the lane root
(161 lines) as past-EOF. The identical line exists at base a7af2ce line 70; round-40 did not touch
it. Reported for completeness; not a round-40 harm.

Verdict calibration: **no round-40 defect** — every new (round-40) pointer resolves byte-exactly,
no fabricated `[x]`; one pre-existing stale cross-lane cite remains in SHONEN (round-34 debt).

## 3. Adjacency

Re-grep of the eight new knowledge entries (anthropic-cvd-provenance-and-pacing, cisa-bod-20-01-
vdp-minimums, cisa-cvd-program-stages, cve-bench-agent-exploitation-benchmark, cyclonedx-analysis-
subtree, doj-vdp-framework-scope-and-authorization, nist-sp800-216-vdp-framework, pz-reporting-
transparency-trial) for sibling-domain topics and sibling lane names (kengaku, kaidoku, kake,
kotoba, kotodama, kumitate, chousa, kama, mori, mado, souji, tabi, tameshi, tsukuroi, revenger,
shokuknow, kagi, lore, audio, game-dev): **zero hits** for sibling lane names in all eight
entries; no SBOM-extraction/provenance-fidelity content (kaidoku ground), no security.txt
publishing (kake ground), no model-provider/packaging material (kotoba/kumitate/kama), no
benchmark-selection/offline-replay/capability-measurement claims (kengaku ground).

Contested boundary S025 (CVE-Bench) checked against the ConnSibling constraint: the entry reads the
paper for the disclosure-process implication only — it documents how to quote rates with
denominator/setting/attempt-budget/model, explicitly rejects using them as finding- or
triage-accuracy evidence, rejects real-world generalization, and makes no agent-capability or
benchmark-selection claim of its own (its "ground" line names the paper's own capability-measurement
arm only to fence it off; the claims themselves are descriptive and the output guidance denies
capability/generalization). Boundary honored; no eval craft absorbed. F23 CycloneDX entry is
scoped to the v1.7 `analysis`/`affects` slice (L2-L111), disclaims producer practice, and defers
issuance rules to S057 / CSAF comparisons to kasegi's own S055 capture — matches the ConnSibling
ruling (F23 uncontested, adjacent to kaidoku SBOM extraction which it does not enter). S060 row
(SOURCES.md line 66) and the F23 PROVINCE.md amendment (line 161) are present as claimed.

Verdict adjacency: **no absorbed sibling ground.**

## Overall verdict

No cross-axis harm found in the round-40 build: depth:density intact (append-only, instrument
unchanged, mean 232.9 → 233.5), calibration intact for all new SHONEN pointers (byte-exact
receipt values, no fabricated `[x]`), adjacency clean (no sibling ground absorbed; S025 boundary
honored). Green re-runs above are evidence. One pre-existing calibration debit (SHONEN line 70
`PROVINCE.md:284-286` past-EOF, round-34 era) recorded for the record, not a round-40 defect.
