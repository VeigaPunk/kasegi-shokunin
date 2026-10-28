VERDICT: HOLDS

Seat R45W2CritAxisHonesty (leaf critic, read-only, falsify wave 2). Attacked: the proposed round-45 score statement — depth:verifiability 4 held, coverage 8 held, depth:density 9 held, score delta 0 on all three, with C1 and C2 reported as trend work — against the integration tree at lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd). Attacked export: `/fast/scratch/hyaku/kasegi-r45/R45W2CritAxisHonesty/export` (git archive of 6662a42); base: `.../base` (git archive of dc5bb8c). The moving lane working tree was not used for any measurement. Nothing committed, nothing mutated in git/jj/index, no shared file touched.

Bottom line: holding all three scores is the honest statement. HOLDS is conditional on the round report carrying the wording in Finding 9. Without it, the counters' green invites exactly the misreading this critic is asked about. The score-8 coverage value rests on a measure the SCORECARD itself records as never adopted (Finding 4); the report must disclose that rather than silently inherit it.

## Finding 1 — the integration tree asserts no score; the round row does not yet exist

Attacked: `SCORECARD.md` at 6662a42 (and LOG.md).
Command: `grep -n -i "round 45\|round-45\|r45" SCORECARD.md LOG.md` (in the export).
Output: `SCORECARD.md:1703:### Planned evidence gates for round 45` and `LOG.md:1992:- Planned for round 45: freeze a committed-export counter for depth:verifiability ...`. No `Round 45 result` table and no round-45 score statement exists in the tree.
Consequence: the score statement is not yet landed anywhere; the round report/row must add it. The three rows below are the statements I checked.

## Finding 2 — depth:verifiability 4 held: correct; C1 moves the counter, not the bar

Promotion bar quoted from `SCORECARD.md:1536-1541` (`### depth:verifiability, 4 → 5`):
- limb 1: "**0 gated rechecks.** `python3 corpus/instruments/recheck-audit.py --root . --quiet` prints `executes=<n> gated=0 broken=0` together with `lines=<n> total=<n> ... exit=0`."
- limb 2: "The score-5 audit bar. `SCORECARD.md:331`: 'Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims.'"

Commands and printed output (re-run by me):
- base: `recheck-audit.py --root . --quiet` → `executes=39 gated=24 broken=0 ...` / `lines=63 total=63 pass=63 fail-closed=24 ... exit=1`
- export: `recheck-audit.py --root . --quiet` → `executes=40 gated=24 broken=0 ...` / `lines=64 total=64 pass=64 fail-closed=24 ... exit=1`
- `score-gap.py --root .`: base `gap: 24 of 63 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`; export `gap: 24 of 64 ...`.
- The one new line (F27 entry, `knowledge/linux-kernel-security-bugs-reporting-process.md`) is not gated; `recheck-audit.py --root .` (non-quiet) classes it `FROZEN-ONLY` (passes the frozen limbs, fails the strict ones), the same class as the rest of the set.
- Strict: export `strict pass=1/64 cdroot_fail=63`; base `strict pass=1/63 cdroot_fail=62`. Neither tree sits at the `~/Projects/shokunin` path the strict limb expects, so the bar's `exit=0` cannot be shown on either export. A report must not print "0 gated, exit 0" from these trees.

Counter (C1), do-nothing vs integration, `r45-routed-defects.py --root <tree> --baseline base`:
- base: `routed-defects total=5 fixed=0 unresolved=5 exit=1` (limbs R1–R5 each `fixed=0`)
- export: `limb R1 fixed=1 read=S072=supersedes ...` / `R2 fixed=1 read=criteria=3` / `R3 fixed=1 read=selftest-cases=43` / `R4 fixed=1 read=selftest-cases=20 replay=base_ok=2` / `R5 fixed=1 read=refiled=pinned-run-output original=unchanged` / `routed-defects total=5 fixed=5 unresolved=0 exit=0`

Reading: the counter moved 0/5 → 5/5; the 4→5 limb 1 (gated) stayed at 24; limb 2 (non-author audit) is not in C1 and no audit is claimed. C1 therefore moves no limb of the 4→5 bar. Hold 4.

## Finding 3 — the "held 4" rests on a census that the base does not reproduce

Attacked: the depth:verifiability measure. `SCORECARD.md:33-38` defines the axis as the resolve.py fraction ("fraction of distinct path-like citations that resolve on disk"); the 4→5 bar (Finding 2) uses the gated count instead. The two measures are not the same instrument.

Commands and output:
- `git show dc5bb8c:corpus/instruments/citation-survival.md | sed -n '5p;33p'` → `Scope: \`SKILL.md\` + \`corpus/**/*.md\` (50 files).` / `- lane total (SKILL.md + corpus): **134/1480 = 9.05%**`
- `find base/corpus -name '*.md' | wc -l` → `213`
- `resolve.py` re-run on base (one run, scratch): `all=866/4121` (21.01%); `skill=87/630` (13.81%); `corpus=836/3742`.
- `resolve.py` re-run on export: `all=894/4186` (21.36%); `skill=100/646` (15.48%); `corpus=861/3804`.

Reading: the committed census of record (9.05%, 50-file scope) does not reproduce from the base bytes (21.01%, 213-file scope). The round report must not present the committed 134/1480 as a current measurement. Its "held 4" is a held score on a measure the lane's own instrument no longer reproduces; that must be disclosed, not resolved in this round.

Measurement-surface change: the integration adds 16 SKILL citation instances (630 → 646), of which 13 resolve (87 → 100). That moves the SKILL resolve share by +1.67 points with no verification performed on the new citations. The row must say "measurement-surface change, not verification" (as the wave-1 C1 critic also recommended). It must not say verifiability rose.

## Finding 4 — coverage 8 held: correct on the arithmetic, but the 8 rests on an unadopted measure

Promotion bar quoted from `SCORECARD.md:1547-1549` (`### coverage, 7 → 8`): "`(20 + F_admitted) / (20 + F_total) = 1.000` ... the r22 measure, `SCORECARD.md:332`; planned for adoption at `SCORECARD.md:178` and never adopted — round 23 kept the r15 denominator".

Commands and output:
- Criterion, base: F rows `26`, admitted `26`, queued registry rows `0` (`56 mined / 14 rejected`) → `(20+26)/(20+26) = 1.000`.
- Criterion, export: F rows `27`, admitted `27`, queued `0` (`57 mined / 15 rejected`) → `(20+27)/(20+27) = 1.000`.
- `frontier-recheck-count.py --root .` export: `entries=30 pass=30 exit=0`.
- `r44-frontier-count.py --root . --expect 27`: base `frontier expected=27 admitted=26 verdict=SHORT exit=1`; export `frontier rows=27 admitted=27`, exit 0.
- `r45-c2-gate.py --root <tree>`: base `c2-gate fixed=1/7 exit=1`; export `c2-gate fixed=7/7 exit=0`.
- Adoption check: `grep -n adopt SCORECARD.md` returns lines 178, 332, 491, 1217, 1549 only; none adopts the r22 ratio. The adopted denominator stays `0/18` (`SCORECARD.md:1555`: "the adopted r15 denominator holds 0/18 domain surfaces present"; `corpus/README.md:215`: "The original domain-root map is exhausted: 0/18 surfaces are present.").

Reading: the criterion is identical at base and export (1.000 both), so F27 moves no coverage score. It is expansion-trend work (`AXES.md:21`: "Expansion ↔ `coverage` + `adjacency`"; LEARNING.md:1-4 "its corpus expands"). Holding 8 is honest.

Pre-existing debt the report must carry: the score-8 itself (the round-40 move, `SCORECARD.md:1591-1596`, "measure 43/43 = 1.000") was granted on the r22 ratio that `SCORECARD.md:1549` says was never adopted. The round report must write "coverage 8 held on the corpus-facing r22 ratio (unadopted; SCORECARD.md:1549); the adopted domain denominator is 0/18 and unchanged". It must not write "coverage 8 → 9" or "coverage moved".

## Finding 5 — depth:density 9 held: correct, but the measured mean moved and must be printed as form

Commands (re-run by me, `density.py SKILL.md --label …`):
- base: `| | **mean dens** | | | | | | | | **237.4** |` / `Total path-citation instances: 793 across 31 blocks.`
- export: `| 32 | Round-45 Gates & probes registry addition (appended 2026-10-28) | 10 | 9 | 23 | 6 | 12 | 12 | 53 | 588.9 |` / `| | **mean dens** | … | **248.4** |` / `Total path-citation instances: 816 across 32 blocks.`
- SKILL.md diff vs base: `11 insertions(+)` only.

Reading: the mean rose 237.4 → 248.4 (+11.0) because a new table block (588.9) sits above the mean. SCORECARD records the form effect (`SCORECARD.md:32`: "identical content: 93.3 prose vs 150.0 table"). No density bar above 9 is written in SCORECARD (the only density bar is `BAR_R15 = 142.5` for repaired blocks, `SCORECARD.md` bar rule). So "9 held" is the honest statement, and "density up" is not. The most recent recorded mean is `SCORECARD.md:1426`: `mean **220.9**, 26 blocks`; the base's 237.4 over 31 blocks is consistent with five later blocks, but no round 43–44 density mean was recorded, so the round report should print the base and export means explicitly.

## Finding 6 — the do-nothing control separates counter movement from score movement

Attacked: whether the green counters are, by themselves, evidence of a score move. Control = the base tree (do-nothing), measured with the same commands as above.

| quantity | do-nothing (base) | integration (export) | moved? |
|---|---|---|---|
| C1 counter `routed-defects` | fixed=0/5, exit=1 | fixed=5/5, exit=0 | yes — routed-defect closure |
| depth:verifiability limb 1 (`gated`) | 24 of 63 | 24 of 64 | no |
| C2 counter `c2-gate` | fixed=1/7, exit=1 | fixed=7/7, exit=0 | yes — F27 frontier shape |
| coverage criterion (r22) | 1.000 (46/46) | 1.000 (47/47) | no |
| density mean (SKILL.md) | 237.4 / 31 blocks | 248.4 / 32 blocks | +11.0 by form, no bar |

The counters discriminate (red at base, green at export); none of the score quantities moves. A reader who sees "fixed=5/5 exit=0" or "fixed=7/7 exit=0" next to "held" is reading two different things, which is why Finding 9 is needed.

## Finding 7 — C1 should be reported as quality-trend work, with its frozen axis label annotated

Attacked: whether C1 belongs under `depth:verifiability` at all.
- `claims.json` C1 carries `"axis": "depth:verifiability"`; its kill rule has no limb predicate (the counter is the only instrument), so the frozen label is not supported by any score limb.
- `corpus/instruments/r45-routed-defects.py:2` labels itself "round-45 C1 counter (depth:verifiability)".
- The lane's trend map: `AXES.md:21` "quality ↔ `depth` + `freshness` + `operability`"; LEARNING.md:3–4 "its corpus expands, the **quality** of what it holds rises".
- The five items are a quality/operability set: R1 source correction, R2 QUALITY.md criteria, R3 registry/gate hygiene, R4 freeze tool, R5 receipt hygiene.
- Precedent: `SCORECARD.md:1712` (round 44, depth:verifiability row): "4 held — measured … **Score delta: 0** — … the increment is graded under the quality trend, not as a score move".

Conclusion: report C1 as quality-trend work (routed-defect closure, 0/5 → 5/5 on the counter), with score delta 0 on depth:verifiability. The frozen axis label stays as frozen; the round report annotates it. A counter-docstring label change is logged as counter errata (the kill rule permits errata that keep the predicate), not silently edited.

## Finding 8 — the lane has withdrawn green counters before; the report must use "not verified"

Precedents in the committed SCORECARD (grep `Correction (round` in `SCORECARD.md`):
- `SCORECARD.md:1560` and `:1588` (round 39/40 corrections): "the 8/8 in that row is withdrawn, not merely qualified".
- `SCORECARD.md:1603` (round 41): the round-40 row's "4 (held; verified)" "is withdrawn to score 4 held, not verified … a green suite run is not claim admission when the frozen kill rule fires."
- `SCORECARD.md:1736` (round 44 falsify-wave correction): a fully fabricated evidence tree graded `fixed=8 unresolved=0`; the counter was hardened to v2.

So the honest status word for C1 and C2 at this head is "measured, not independently verified" (the round-44 wording at `SCORECARD.md:1712`), never "verified". Neither kill rule fires on the export (C1 controls red per `controls/freeze-controls.txt`; C2 non-author closure not run by me), so "not verified" is the conservative label, not a finding that the counters are wrong.

## Finding 9 — required report wording (what the round row must say, and what it must not)

Must say, for each axis, in the round move-log row:
- `depth:verifiability | 4 | 4 held — score delta 0. Measured: routed-defect counter 0/5 → 5/5 at export (quality trend; C1 is routed-defect closure, not a 4→5 limb). Limb 1 gated 24 → 24 (of 63 → 64 lines; F27 line not gated). Limb 2 (non-author audit) not run. The 4 rests on a census that does not reproduce: committed 134/1480 (50-file scope) vs live resolve all=866/4121 base, 894/4186 export. SKILL resolve share +1.67 pts from 16 new citations (13 resolve): measurement-surface change, not verification. Not verified.`
- `coverage | 8 | 8 held — score delta 0. Frontier 26 → 27 admitted (expansion trend). Criterion (r22 ratio) 1.000 at base and export; the criterion is unadopted (SCORECARD.md:1549); the adopted domain denominator stays 0/18. Not verified by a non-author.`
- `depth:density | 9 | 9 held — score delta 0. SKILL.md mean 237.4 → 248.4 (31 → 32 blocks); the rise comes from a new 10-row table block (588.9) and is form, not density gain; no 9→10 bar exists.`

Must not write: "verifiability improved", "verified", "0 gated" without the strict-exit caveat, "coverage 8 → 9", "coverage moved", "F27 raises coverage", "density up", "held 4 (re-measured)", "fixed=5/5 ⇒ depth:verifiability 4→5 path", or any reading of the counter line as a score.

Must also carry the claims-label erratum: "claims.json C1 axis `depth:verifiability` and C2 axis `coverage` are frozen labels; the scored effect of C1 is quality-trend work, and of C2 expansion-trend work; score delta 0 on both."

## Limitations

- Attacked the export of 6662a42 only; the lane working tree was not used. The export is not at `~/Projects/shokunin/kasegi-shokunin`, so `recheck-audit.py` strict mode and `cdroot` checks are structurally unreachable there; the gated count (24) is the value compared, not a strict pass.
- `resolve.py` was run once per tree (≈5 min each, two runs in parallel); no repeat. Its scope and census numbers are for the export/base copies; the committed census was not regenerated in the lane.
- I did not re-run the frozen do-nothing/marker-only control file; `controls/freeze-controls.txt` records `c1-marker-only fixed=0` and `c2-junk-row fixed=4/7`, which I cite as recorded output, not as a re-run. My do-nothing control is the base export.
- I did not run a non-author audit or the C2 non-author closure; no score claim here depends on them, but the 4→5 bar and any coverage "verified" wording do.
- The F27 entry's recheck line `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …` depends on the live lane path; on a host without that path it would be gated. Noted, not scored.
- The density base mean 237.4 was compared with the most recent recorded mean (220.9, `SCORECARD.md:1426`, 26 blocks); no round-43/44 density mean is recorded, so the 5-block gap is inferred, not reconciled.
- Wave-1 seats' figures (R45CritAxisC1, R45CritAxisC2, R45CritDensityHarm) were read as context; every number above was re-measured from the export/base by this seat except where marked as recorded.
- Tools installed or upgraded: none. Scratch `/fast/scratch/hyaku/kasegi-r45/R45W2CritAxisHonesty` removed on exit.
