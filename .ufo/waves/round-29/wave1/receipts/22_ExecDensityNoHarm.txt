# ExecDensityNoHarm — no-harm measurement receipt (round 29, wave 1)

Seat: `ExecDensityNoHarm` (leaf executor). Assignment: no-harm measurement of SKILL.md
density + anchor verdict classes across the wave's SKILL.md append.
Answering model: `inception/mercury-3` (config route; I never passed a model).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (ONLY write scope).
Base revision: `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims-freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`;
dispatch HEAD `46e07f6ae8f23debb10034164252e7027b4d9091` (round-29 wave-1 spec + dispatch; SKILL.md byte-identical to base there — `git diff 7a6591c..HEAD -- SKILL.md` empty, 1035 lines both sides).

## 1. Base measurement (BASE revision bytes, `git show 7a6591c…:SKILL.md > /tmp/skill-base.md`)

### 1a. density (label r29-base)
Command: `python3 corpus/instruments/density.py /tmp/skill-base.md --label r29-base` — exit 0.
- **mean dens = 160.2**; 20 blocks; total path-citation instances = 656.
- Thin blocks at base (dens < 100): Pipeline 13.3, Retirement 93.0, Operator queue 97.2.
- Instrument digest at base of `density.py` = `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710` (UNCHANGED this round; no owner declared it).
- Comparand (history, disclosed): r28 base 150.3/20 blocks/652 cites (round-28 lesson), r28 close 160.2 (round-28 verifier spotcheck). The r29 base 160.2 equals the r28 post-append close — a continuation, not a policy.

### 1b. anchorcheck (BASE bytes)
Two runs, both recorded:

1. Literal spec invocation `python3 corpus/instruments/anchorcheck.py /tmp/skill-base.md` (file outside the lane root → lane root not derived; `corpus/…` cites fall to the absent mirror base):
   `== /tmp/skill-base.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=7` — exit 1.
   NOTE: file-location artifact, not a content property; NOT the after comparand (recorded because the spec named it).
2. Semantically comparable run, lane root pinned: `KASEGI_LANE_ROOT=$PWD python3 corpus/instruments/anchorcheck.py /tmp/skill-base.md`:
   `== /tmp/skill-base.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` — exit 0.
   This is the BASE comparand for the after run (`anchorcheck.py SKILL.md` from the lane root); it matches the round-28 canonical no-harm line.

### 1c. instrument baseline snapshot (start-of-wave sha256) and declared owners
| instrument | base sha256 | declared owner this round |
|---|---|---|
| anchorcheck.py | `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396` (== frozen C1 do-nothing digest) | ExecImplC1 ONLY |
| density.py | `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710` | none |
| resolve.py | `db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667` | none |
| source-recheck.py | `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` | none |
| capture-source.py | `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18` | none |
| frontier-recheck-count.py | `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` | none |
| mirror-containment-check.py | `dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a` | none |
| resolve-dispatch-check.py | `acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1` | none |
| recheck-audit.py | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` | none |
| test_resolve.py | `16a6ff281d89845444a7face5034c611594adaf59438e62b3f1dce55f7a5711e` | none |
| knowledge-expected.txt (data of recheck-audit.py) | 42 lines / 40 entries at wave start | ExecRecheckAudit ONLY (40→41 entries / 42→43 lines after F13 entry) |

### 1d. pre-state label
Sections 1a–1c measured before any wave edit (BASE/PRE-STATE). Comparands used below are 1b#2 ↔ 3b only.

## 2. Waiting for the append
The r29 `ScribeSkillGate` seat's append landed on disk: SKILL.md sha `125be37d…` → `82bdced5d5c46b6847a169f5ce6bec172dbf0c57d51bc5ec5361e2bd4731ee70`, 1035 → 1047 lines (+12, append-only). Receipt `.ufo/waves/round-29/wave1/ScribeSkillGate.md` exists (2026-10-25T15:22Z). (A stale parked r28 seat with the same name answered the first coordination ping with r28 boilerplate; ground truth was the working tree, and the actual append was confirmed by file bytes.)

## 3. After measurement (live SKILL.md)

### 3a. density (label r29-after) — same instrument, same form
- **mean dens = 167.5** (160.2 → 167.5); 22 blocks (20 → 22); total path-citation instances 659 (656 → 659).
- All 20 pre-existing blocks' rows are byte-identical (19/20 literal row equality; block 20 "Frontier decision table" line-count 12→13 only because a trailing blank moved into its span — nb/cites/tbl/num/sig/ev/dens unchanged, 200.0 both sides).
- Two NEW appended blocks: block 21 "Round-29 Gates & probes registry addition" (8 lines, nb=5, ev=14, dens=280.0) and block 22 "Round-29 frontier note" (3 lines, nb=2, ev=4, dens=200.0).
- Disclosed: the +7.3 mean is a measurement change from the wave's SKILL.md append (12 lines), not a claim; no density credit is taken.

### 3b. anchorcheck (live SKILL.md, comparable invocation)
`python3 corpus/instruments/anchorcheck.py SKILL.md` (from lane root):
`== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` — exit 0.

### 3c. verdict-class comparison (BASE 1b#2 vs AFTER 3b)
| class | BASE | AFTER | moved? |
|---|---|---|---|
| in-range cite instances | 7 | 7 | no |
| bad (MISSING-FILE+PAST-EOF+OUTSIDE-BASE) | 0 | 0 | no |
| distinct anchors | 7 | 7 | no |
| LOST-RECORDED | 306 | 306 | no |
| PIN-BROKEN | 0 | 0 | no |
| ORIGIN | 0 | 0 | no |
| OUTSIDE-BASE | 0 | 0 | no |
| BASE-ABSENT | 0 | 0 | no |
| exit | 0 | 0 | no |
**Verdict classes did not move.** R6 proof: `head -n 1035 SKILL.md` is byte-identical to base SKILL.md (`cmp` exit 0); the +12 lines are file-tail appends.

## 4. No other instrument changed
After-wave sweep vs section 1c snapshot: among `corpus/instruments/*.py` ONLY `anchorcheck.py` changed — `23818c12…` → `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` (531 lines), declared owner ExecImplC1; its diff (base vs live) is confined to the selftest/limb-region and module docstring (LIMBS registry, 3 new isolating fixtures outside-base-mirror/outside-base-origin/base-absent-origin, PIN-BROKEN git-free skip, prints `limbs=9 covered=9`; selftest now `cases=12 failures=0` exit 0). `knowledge-expected.txt` changed 42→43 lines / 40→41 entries (declared owner ExecRecheckAudit). All other instruments unchanged, including `density.py` (`ee803726…`) — the density measurement instrument itself was untouched. Non-instrument modified files (SKILL.md, corpus/README.md, corpus/SOURCES.md, corpus/QUALITY.md, LOG.md) correspond to their declared single-writer owners (ScribeSkillGate/ScribeReadmeC2/ScribeSourcesGate/ScribeQuality/ScribeLog).

## 5. Risks / notes
- The literal spec baseline command (1b#1) cannot be compared to the after column; the comparable pair is 1b#2 ↔ 3b. If an integrator re-runs either check, use the lane-root invocation.
- The r29 ScribeSkillGate slot is distinct from the parked r28 seat of the same name; message routing to `agent://ScribeSkillGate` reached the r28 seat. Landed-file evidence is authoritative.
- I observed ` M .ufo/waves/round-28/receipts/ScoutAssimilation.txt` and ` M .ufo/waves/round-28/wave1/ScoutAssimilation.md` in the working tree (round-28 files touched during round 29). That is outside instrument scope; flagged for SentScope/L1.
- Outputs of every command named above are reproducible; full selftest state at close: `cases=12 failures=0`, `limbs=9 covered=9`, exit 0 (run by ExecCanonC1/ExecSelftestProbe for the canonical receipt).
