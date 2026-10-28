VERDICT: HOLDS

# R45CritWaveShape — round-shape critique (kasegi round 45, wave 1)

Sub-verdicts: (a) wave-1 shape, one v2 wave of 64 seats, conforms to the band and role rules it is held to: HOLDS. (b) Second v1 wave of >=32 seats: NOT MET on today's landed artifacts (13 genuinely new attack items found; 32 is reached only if wave-1 deliverables that are not on disk yet all land). Do not pre-size wave 2; decide after WAVE-DONE and results.json.

Read-only seat. No commits, no git mutation, no writes outside this report. Scratch under $HYAKU_SCRATCH/kasegi-r45/R45CritWaveShape/ removed on exit.

## 1. Wave-1 shape (what the spec actually carries)

Inputs: `.ufo/waves/round-45/wave1-spec.json` (64 items), `.ufo/waves/round-45/wave1-dispatch.json` (`taskCall.tasks`, 64 entries), `.ufo/waves/round-45/wave1.ready.dispatched` (dispatched 2026-10-28T18:02:21).

Counted by a stdlib script (`shape_check.py`, scratch) over the registry members, which equal the spec roles. Role counts:

```
{'connector': 2, 'critic': 8, 'executor': 6, 'mutation-tester': 8, 'revenger': 1, 'reviewer': 16, 'scout': 10, 'scribe': 10, 'sentinel': 2, 'simplifier': 1}
```

Checks against the rules the prompt states (prompt = `.ufo/prompts/kasegi-round-45.md`):

| Rule | Source | Result |
|---|---|---|
| Band 64–128 | policy v2 `scripts/hyaku/ufo-wave-policy-v2.json:89-90` (`"waveMinLanes": 64`, `"waveMaxLanes": 128`); prompt line 346 "one v2 wave (64–128)" | 64 seats: PASS (floor) |
| >=25% attack seats (reviewer, critic, mutation-tester, labrat) | prompt lines 348-349 "with ≥25% of its seats attack roles (reviewer, critic, mutation-tester, labrat)" | 16+8+8 = 32/64 = 50.0%: PASS |
| Few connectors | prompt §2 / run-9 block line 217 | 2 connectors: PASS (assumed threshold <=4; the prompt gives no number) |
| L2 floor (§3, met inside the single v2 wave) | prompt lines 80-88 (1 planner, 1 connector, 3 executor, 1 scribe, 1 scout, 1 reviewer, 1 critic) | connector 2, executor 6, scribe 10, scout 10, reviewer 16, critic 8: all met; planner not a swarm seat (see §2) |
| Only validator-admitted roles | `~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:265-275` `SWARM_ROLES` = scout, reviewer, critic, connector, sentinel, executor, mutation-tester, revenger, simplifier, scribe | all 64 in set: PASS; no planner |
| Routing never passed | prompt line 154 "(never pass `model`)"; dispatch | taskCall keys per seat = {agent, name, task}; no `model` key anywhere; `agent` holds the role name (e.g. "reviewer"), not a model alias: PASS |
| Registry = spec = taskCall | `wave1-dispatch.json` registry.members vs taskCall names | 64 unique names; registry names == taskCall names: True; role counts identical: PASS |
| Lane self-seat present | spec item `R45CritWaveShape` | present (critic): PASS |

Do-nothing and discrimination control (the same checker, deliberately broken inputs):

```
REAL: seats 64, band_ok True, attack_seats 32, attack_share_pct 50.0, attack_ok True, connectors_ok True, l2_floor_missing [], roles_all_swarm True, no_model_key True, PASS True
CTL-A do-nothing (all 64 scout):   attack_share_pct 0.0, attack_ok False, l2_floor_missing ['connector','executor','scribe','reviewer','critic'], PASS False
CTL-B strip reviewer/critic/mutation-tester: seats 32, attack_share_pct 0.0, attack_ok False, PASS False
CTL-C inject planner:              seats 65, roles_all_swarm False, PASS False
CTL-D only 2 executors:            seats 60, l2_floor_missing ['executor'], PASS False
CTL-E first 40 seats:              seats 40, band_ok False, PASS False
```

So the checker is not a rubber stamp: each deliberately broken shape fails on the rule it breaks.

Observation: the validator does NOT enforce role mix. `ufo-swarm-wave.mjs` checks the band (`waveMinLanes`/`waveMaxLanes`, lines ~822-1092) and role membership (line 988), not the attack share, connector count or L2 floor. Those rules live only in the prompt, so they are enforced by counting, not by the validator.

Concentration note: wave-1 attack seats mostly target the frozen artifacts. Reviewers R45RevLimbR1-R5 and R45RevGateG1-G7 (12 seats) plus mutation-testers R45MutLimbR1-R5 and R45MutG123/G45/G67 (8 seats) all point at `r45-routed-defects.py`, `r45-c2-gate.py` or the freeze/claims/controls. The attack share is met on paper, but its targets are narrow (see §3).

## 2. Planner, routing, dispatch state

- Planner: no planner seat in the wave, as the prompt permits (line 376 "Planner seat (orchestrator ruling 2026-10-19): the validator rejects `planner`"). The L1 holds the §3 planner seat. The round-44 spot-check item D4 shows the failure mode of an unrecorded mapping: "the round-44 LOG section does not record the affirmative planner=L1 mapping" (`corpus/lessons/round-44-verifier-spotcheck.md` routed defects; selftest case D4-denial in final-attempt3-refiled.txt). The round-45 LOG/report must state `planner=L1` affirmatively.
- Routing label drift (for the L1 and operator, not changed by me): the prompt's run-11 label (lines 154-165) says every role is `@m_flash` except scout `@m_grok` and task `@m_zfl`, with reviewer/critic/mutation-tester/connector on `@m_auto`. The operator-owned authority, `~/.omp/agent/config.yml` lines 408-426 (`task.agentModelOverrides`), currently reads:

  ```
  task: "@m_sonnet"  executor: "@m_sonnet"  planner: "@m_sonnet"  labrat: "@m_mim"
  mutation-tester: "@m_mim"  sentinel: "@m_mim"  simplifier: "@m_haiku"  revenger: "@m_haiku"
  scout: "@m_grok"  scribe: "@m_flash"  critic: "@m_haiku"  reviewer: "@m_mim"  connector: "@m_mim"
  security-reviewer: "@m_sonnet"
  ```

  The prompt itself says config is the authority and the label is only a label (prompt line 158). So the label and the config disagree (e.g. reviewer `@m_mim` vs label `@m_auto`; critic `@m_haiku` vs label `@m_auto`; task `@m_sonnet` vs label `@m_zfl`). Claims that depend on a seat's answering model must record it. I did not edit config.
- Dispatch: `wave1.ready.dispatched` exists, so the orchestrator took the ready file and spawned the 64 seats. `wave1-results.json` is not on disk yet, so dead-seat and final role counts are not verified here. Pending results.json.
- Resume sends: none (`counts.resume` = 0, `resumeSends` = []).

## 3. Second v1 wave: are there >=32 distinct genuine attack items?

Policy v1 band: `scripts/hyaku/ufo-wave-policy.json:89-90` (`"waveMinLanes": 32`, `"waveMaxLanes": 64`). A 32-seat second wave is in band, so the band is not the constraint; the item count is.

Attack items must each name an artifact and a falsifiable hypothesis. Items already covered by a wave-1 seat by name (listed in §1) are not counted as new. Status tags: [RUN] = I ran it and quote the output; [CODE] = read the code, not run; [HYP] = hypothesis only.

### 3a. New items attackable on landed artifacts today (13)

Landed now: freeze commit 8cf62c8 (counters, controls, claims, S071/S072 snapshots, manifest), lane HEAD 5242db6, and the five wave-1 draft files under `.ufo/waves/round-45/wave1/` (R45ExecFreezeA/B `freeze-check.py`, R45ExecFrontA/B `r44-frontier-count.py`, R45ScribeRowsA `rows.md`).

1. N1 `R45ExecFreezeA.draft/freeze-check.py`: `--selftest` must produce >=6 real cases, not a printed stub [HYP].
2. N2 same file: whole-line match must reject `fixed=0x` for expect `fixed=0` (R41 pattern) [HYP].
3. N3 same file: a claim missing any of the three fields (counter_cmd, expect_before, expect_after) must not pass [HYP].
4. N4 same file: a nonzero counter exit is not by itself a failure, per its spec [HYP].
5. N5 `R45ExecFreezeB.draft/freeze-check.py`: its own selftest case count and verdicts [HYP].
6. N6 A vs B parity: same replay verdicts on `claims.json` at base and at lane tree [HYP].
7. N7 `R45ExecFrontA.draft/r44-frontier-count.py`: `--expect` parsing and selftest case count [HYP].
8. N8 `R45ExecFrontB.draft/r44-frontier-count.py`: same two checks [HYP].
9. N9 A vs B parity on the base (must print `frontier expected=27 admitted=26 verdict=SHORT exit=1`, which I ran on base, see §4) [HYP].
10. N10 `R45ScribeRowsA.draft/rows.md`: every row has 11 cells in SOURCES.md column order [HYP].
11. N11 same file: the S071 anchor cell contains sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40` (the manifest value; I verified the file's sha256 matches) [HYP].
12. N12 same file: the S072 `teaches` cell opens with `supersedes S070 —` and status is `rejected` (the limb_r1 predicate, [CODE] lines 99-143) [HYP].
13. N13 same file: `opened` and `used-by` agree with manifest `fetched_utc` 2026-10-28T20:52:44Z [HYP].

### 3b. Conditional items: attack the wave-1 deliverables not on disk yet (19)

These exist only once wave 1 lands the F27 entry, QUALITY criteria, lesson correction, SOURCES rows, receipt and selftest outputs (the wave-1 spec's own deliverables). Each is a distinct target.

14. K1 F27 knowledge entry: each curly span is located at its cited `S071.txt:N[-M]` window (G5).
15. K2 same: a 26-word span must fail the <=25-word cap (boundary test).
16. K3 same: core regexes (`up to 7 calendar days`, `treat it as public`, …) match as substrings of any located span, so the gate is meaning-blind [CODE, `r45-c2-gate.py` g5 lines 169-190].
17. K4 same: provenance trio requires the exact `https://docs.kernel.org/process/security-bugs.html` (G2).
18. K5 same: a citation window that covers the whole file lets any located span pass (window tolerance).
19. K6 same: exactly 3 located spans plus 1 unlocated must fail (`len(passed) >= 4` boundary).
20. K7 same: the 64-count (G6) is satisfied by a non-entry .md file [HYP].
21. Q1 QUALITY R47-R49 rows: each `Grounded in round-44.md` cites an M44 id that exists there [HYP].
22. Q2 QUALITY: an in-place edit of an earlier row (R22-R43) must fail the append-only check [HYP].
23. Q3 QUALITY: the R47/R48/R49 regex tokens (`do-nothing`+`before data`, `presence-only`, `capture method`+`reject`) satisfied by non-criterion prose [HYP; limb_r2 regex list line 144-146].
24. L1 round-44 lesson correction: a `Correction (round 45` line containing S072 and `10 029` anywhere in the tail passes, even outside a section [CODE, limb_r1 lines 128-143].
25. L2 routed item 1 wording vs R1 predicate: §6 item 1 asks for an append to SOURCES.md S070 and to round-44.md `## Gate`; limb_r1 checks only that the S070 raw row is unchanged and a `Correction (round 45` line exists in the lesson tail, not in `## Gate` [CODE].
26. S1 SOURCES S071 row: anchor cell sha equals snapshot sha (G3) [HYP].
27. S2 SOURCES S071 row: `used-by` names an entry path that exists [HYP].
28. R5a refiled receipt: the failed bare call text is absent even when quoted in a comment or header [HYP].
29. R5b refiled receipt: the printed exit line is consistent with the selftest run it records [HYP].
30. R3a SKILL.md Gates & probes: a README-only registry row must not satisfy the R3 registry limb [HYP].
31. X1 mutation of the new `freeze-check.py` gate, one limb forced to pass, against the do-nothing expect string [HYP; see §4 for the same class on C1].
32. X2 mutation of the new `r44-frontier-count.py` gate, same class [HYP].

Sum: 13 (3a) + 19 (3b) = 32. The 32 is the floor, and it holds only if every wave-1 deliverable in 3b lands and each item survives scoping. Drop one deliverable and the count falls below 32.

Second-wave verdict: today NOT MET (13 < 32). Wave 2 should be sized to the items that exist when wave 1 returns, one seat per item, never padded. A residual call of <=8 seats covers leftovers.

## 4. Falsification evidence on frozen artifacts (what I ran)

Scratch base = `/fast/scratch/hyaku/kasegi-r45/L1/pure` copied; lane tree = `git -C <lane> archive 5242db6` (no edits to any tree).

Frozen before-strings at base (claims.json lines 15 and 26):

```
$ python3 corpus/instruments/r45-routed-defects.py --root <base> --baseline <base>
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1      (exit=1)
$ python3 corpus/instruments/r45-c2-gate.py --root <base>
gate G7 pass=1 read=census-rc=0
c2-gate fixed=1/7 exit=1                                 (exit=1)
$ python3 corpus/instruments/r44-frontier-count.py --root <base> --expect 27
frontier expected=27 admitted=26 verdict=SHORT exit=1    (exit=1)
```

The C1 before string matches `expect_before` exactly. C2 matches `c2-gate fixed=1/7 exit=1` exactly. Lane HEAD C1 stays at 0/5 (expected, not yet repaired). Lane HEAD C2 prints `c2-gate fixed=2/7 exit=1` (G4 passes at HEAD, which the claim allows). Controls reproduce: `freeze-controls.py` run on the unmutated lane gives control lines byte-identical to `controls/freeze-controls.txt` (diff empty; `controls total=5 red=5 green=0`).

Claim hashes: `sha256sum claims.json` = `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`, which matches `freeze.txt` `claims-sha256`.

Attack V1 (verified [RUN]): `freeze-controls.py` grades each control RED by exit code only (`got = "RED" if rc != 0 else "GREEN"`). I forced limb R3 to always pass in a scratch copy:

```
limb R3 fixed=1 read=MUTANT-always-pass
routed-defects total=5 fixed=1 unresolved=4 exit=1
control do-nothing-base counter=C1 routed-defects total=5 fixed=1 unresolved=4 exit=1 expect=RED got=RED
control c1-marker-only counter=C1 routed-defects total=5 fixed=1 unresolved=4 exit=1 expect=RED got=RED
controls total=5 red=5 green=0
exit=0
```

So the controls pass a counter that false-positives one limb on the do-nothing base. The exact `expect_before` string (`fixed=0 unresolved=5`) is what catches it, and freeze-controls.py never checks that string. (Wave-1 reviewer R45RevControls covers control adequacy and may find this; I list it here as a verified fact, not a new item.)

Attack V2 (verified [RUN]): `source-recheck.py` exits 0 with a broken anchor. Mutant manifest copy with S071 Q1 anchor set to 1:

```
S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=1-BROKEN
...
exit=0
```

G4 (C2) and limb_r1 (C1) both key on `source-recheck.py` exit code, so neither sees anchor errors. Wave-1 seat R45RevGateG4 covers G4 and may find it.

Anchor observation (verified [RUN]): unmodified S072 `Q2 anchor=1-ok` for `an overview of the different vulnerability reward programs Google maintains`. Line 1 of S072.txt is blank; the quote starts on line 2. The recheck's window tolerance accepts it.

Threshold literals (verified [CODE]): limb_r3 uses `tk[0] < 8` (line 191) and limb_r4 `tk[0] < 6` (line 216), matching claims C1 "after" text (>=8 and >=6). claims.json is not bound by any limb: `grep -n "freeze.txt\|claims-sha\|sha256" r45-routed-defects.py` returns only the S072 sha lines 126 and 129, so a post-freeze edit to claims.json is not detected by C1 counter code. Wave-1 mutation seat R45MutLimbR4 may cover this.

## 5. Limitations

- Role-mix thresholds (connector "few", L2 floor counts) are my readings of the prompt; the prompt gives no exact connector number. I used <=4 for connectors.
- I did not check whether the wave-1 seats' items will land their deliverables; 3b depends on that.
- The item list in §3 is a count of named hypotheses. Only V1, V2, the anchor observation and the threshold/claims-binding checks were run or code-read. Items marked [HYP] are untested and may turn out to be non-issues. They are counted as distinct targets, not as confirmed defects.
- Live-target testing is out of scope (documentation corpus). No network fetches were made.
- results.json is not on disk, so the executed wave-1 seat outcomes (dead seats, final roles) are not verified here.
- I did not verify that the operator's routing config matches what each seat actually answered on; routing is reported from config text only.

## 6. Routed to L1 (not changed by this seat)

1. Record `planner=L1` affirmatively in the round-45 LOG (round-44 D4 failure mode).
2. Route-label drift between prompt run-11 and `~/.omp/agent/config.yml`. Operator decision; L0 question if needed.
3. Validator enforces the band only; role-mix is a manual count. Keep the count in the report (this file has the counts).
4. Wave 2: decide size only after results.json. Need 32 distinct items after wave-1 deliverables land; today the count is 13.

Tooling: none installed. No ~/.local/bin or PATH writes. Scratch dir removed on exit.
