VERDICT: BROKEN

# R46CritAxis — axis-naming critic (round 46, C1 depth:verifiability, C2 coverage)

Scope: frozen claims `.ufo/waves/round-46/claims.json` (sha256 e56ebf87…d740, freeze 9f23aab, base 914ca0b). Read-only. Trees exported with `git archive 9f23aab` and `git archive 914ca0b…` into a scratch root (removed on exit). No commit, index or git mutation; no shared file touched; no install.

## Decision per claim

| Claim | Axis as filed | Axis right? | Score honestly reportable | Wording the report may use |
|---|---|---|---|---|
| C1 | depth:verifiability | Name fits the surface it changes (recheck lines, the gate-count limb of depth:verifiability). The "verifiability" *gain* is BROKEN as framed: the anchors verify tokens in a subset re-implementation, not the lost-tree claims the two entries make. | depth:verifiability **4 → 4 HELD**. Gate-count limb 24→22 moves only if the re-grounds land; limb 2 (non-author 25/25 audit) untouched. | "re-pointed 2 gated rechecks onto committed instrument bytes; gated 24→22; score held at 4". Do NOT write "verifiability improved" or "verified". |
| C2 | coverage | Name is defensible (frontier rows are the lane's counted surfaces; lane precedent at SCORECARD.md:1748). But the score-bearing measure cannot move. | coverage **8 → 8 HELD**. Ratio 1.000 before and after; raw frontier count 27→28. | "frontier 27→28, SOURCES 72→73 (S073 mined); coverage held at 8; no ratio move; 0/18 domain denominator unchanged". |

## Findings

### F1 — do-nothing control for C1 (surface unmoved)

Commands run (freeze and base exports, same output at both):

    python3 corpus/instruments/score-gap.py | grep '^gap:'
    gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims

    python3 freeze/corpus/instruments/r46-c1-gate.py --root freeze --baseline base
    gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
    gate L2 pass=0 read=base-gated=24 regrounded=0
    ...
    c1-gate fixed=1/7 exit=1

The do-nothing reading is therefore `gap: 24 of 64` and `fixed=1/7`; both reproduce the frozen `freeze_tree_reading`.

The lane's own precedent says re-grounding is not neutral. SCORECARD.md:1545: "an entry could instead be re-grounded on a committed capture or have its anchors marked LOST-RECORDED, and neither has been done for these 23 because it changes what the recheck proves." C1 has to say what the re-ground changes.

### F2 — the anchor object is not the object the entries describe

- `corpus/knowledge/claim-gates.md:3` (base): "Source: `~/Projects/bounties/ops/claim-check.mjs` (233 lines, read in full 2026-09-28)". `claim-package-contract.md:66-67` carries `[lost-tree]` provenance. Both entries describe the lost tool.
- `corpus/instruments/claim-package-check.py:2-8` (freeze) says: "The lost claimant tool (~/Projects/bounties/ops/claim-check.mjs) was documentation-only for this lane; this file is the executable gate for the subset the contract states, and nothing more."
- Divergences the frozen `before` text glosses over (the claim says the gate "now implements the contract"):
  - `claim-gates.md:15`: "`/no submission (performed|made)/i`". The instrument, `claim-package-check.py:121`: `NO_SUBMISSION = 'No submission performed'`, a case-sensitive literal with no `made` branch.
  - `claim-gates.md:72`: "`claim_review.reviewer`: `role === 'kx-reviewer'` exactly". Command: `grep -n kx-reviewer corpus/instruments/claim-package-check.py` printed nothing. The instrument checks identity, fallback and distinctness only (`claim-package-check.py:593-608`).

So a row "claim-gates ↔ claim-package-check.py:N token T" establishes that a Python file contains T. It does not establish that claim-check.mjs does what the entry says. The entries' body claims stay `[lost-tree]` and unverified after the re-ground.

### F3 — prototype falsification of the counter (scratch, not committed)

I appended a `## Re-ground (round 46)` section to a scratch copy of `claim-gates.md`, with 8 rows: 7 anchors in `claim-package-check.py` (lines 460, 305, 584, 527, 127, 120, 365) and 1 in the fixture manifest (`corpus/instruments/fixtures/claim-package/defect-1-missing-file/evidence/manifest.json:2`). I replaced its recheck with `r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`.

- Prototype, per-entry: `row G1 ok=1 read=token-located` … `reground entry=claim-gates.md rows=8 ok=8 files=2 exit=0`, rc=0.
- Body falsified (line 32: "`scope_signal` exactly `NO_SCOPE_OBJECTION`" replaced with "`scope_signal` is not checked by the gate (any value passes)"), rows intact: per-entry still `rows=8 ok=8 files=2 exit=0`, rc=0. The per-entry recheck cannot see body text.
- Same falsified tree, aggregate: `gate L5 pass=0 read=bad=claim-gates.md`. Only the append-only limb L5 catches body edits; the per-entry recheck does not.
- Anchor drift (token `NO_SCOPE_OBJECTION` blanked in the instrument): `row G1 ok=0 read=token-not-in-lines`, `reground entry=claim-gates.md rows=8 ok=7 exit=1`, rc=1. This is the real value of the check: it detects anchor drift.
- Aggregate on the prototype (one entry): `gate L1 pass=0 read=gated=23`, `gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md`, `gate L6 pass=1 read=mutants=8 survivors=none`, `c1-gate fixed=5/7 exit=1`. The frozen L2 needs two entries.
- Marker-only control re-run on the freeze tree (two recheck lines replaced by `true`): `gate L1 pass=1 read=gated=22`, `L2 pass=1 regrounded=2`, `L3 pass=0`, `L4 pass=0`, `L5 pass=0`, `c1-gate fixed=3/7 exit=1`. This matches `controls/freeze-controls.txt`.

### F4 — limb 1 of score 5 is satisfiable by re-pointing alone

SCORECARD.md:1538-1541 defines score-5 limb 1 as gated=0. Re-pointing a recheck at any two committed files that contain a token meets it, with no lost-tree claim verified. Limb 2 (SCORECARD.md:331, 1541: "a non-author audit passing 25/25 source chains and 0 unsupported current claims") is the real verifiability gate. C1 must not be read as moving limb 2.

### F5 — C2 coverage: the surface moves, the score-bearing measure does not

Commands, base export unless marked:

    grep -cE '^\| F[0-9]+ \|' corpus/README.md                              -> 27
    awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md  -> 27
    awk -F'|' '/^\| S[0-9][0-9][0-9] /{gsub(/ /,"",$9); if($9=="queued") q++; if($9=="mined") m++} END{print "queued="q+0, "mined="m+0}' corpus/SOURCES.md  -> queued=0 mined=57

- r22/r39 ratio (SCORECARD.md:1549-1553): before (20+27)/(20+27+0) = 47/47 = 1.000. After C2, with 28 admitted rows, S073 mined and queued still 0: 48/48 = 1.000. The ratio cannot register C2. The do-nothing reading gives the same 1.000.
- The frontier-only reading, which the lane's round-40 coverage row used ("measure 43/43 = 1.000", SCORECARD.md:1596), is the reading SCORECARD.md:1553 calls non-discriminating ("cannot discriminate 7 from 8 and is not the criterion"). So the current score-8 evidence is itself saturated by construction.
- Count-only signal: `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 28` → `frontier expected=28 admitted=27 verdict=SHORT exit=1` at base and at freeze. It moves only when the row lands.
- Operator denominator unmoved: corpus/README.md:55-56 "the 18-surface coverage denominator is 0/18 present"; corpus/README.md:217-218 "the public-practice frontier above is a separate denominator … and is not counted into the 0/18 figure".
- Lane precedent: SCORECARD.md:1748 round 45, "coverage | 8 | 8 held — measured (+1 admitted frontier row; not a coverage-ratio move)".
- Coverage 8→9 criterion: `grep -nE 'coverage[^|]{0,40}(8 *→ *9|9 needs|→ 9|for 9)' SCORECARD.md` printed nothing. No 9 bar is stated in the sections read.
- Gap: `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` (base) printed nothing, exit 1. The surface is new in the corpus, so the axis is not double-counting.

### F6 — the frozen C2 counters, re-run

- `r46-c2-gate.py --root freeze` → `c2-gate fixed=2/7 exit=1` (G4 capture pass, G7 census pass), as frozen.
- Same counter run against the base tree → `c2-gate fixed=1/7 exit=1`, as frozen.
- `freeze-check.py --claims .ufo/waves/round-46/claims.json --tool-root freeze --base base` → `claim C1 base_read=c1-gate fixed=1/7 exit=1 verdict=ok`, `claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok`, `freeze-check claims=2 base_ok=2 exit=0`.

## Recommended report text (held vs moved)

- depth:verifiability — score 4, HELD. Gate-count limb: re-grounded rechecks 24→22 (only if both entries land). Verified object: the Python subset gate, not the lost claim-check.mjs. Body claims remain `[lost-tree]`. Recommend the claim be re-titled "recheck re-grounding (gate-count limb of depth:verifiability)" or the word "verifiability" be qualified in the report, and the non-author row-to-claim check in the kill rule be run before anything beyond a held score is said.
- coverage — score 8, HELD. Ratio 1.000 → 1.000 (47/47 → 48/48). Raw surface: frontier 27→28, SOURCES 72→73. 0/18 domain denominator unchanged.

## Limitations

- I did not run `recheck-audit.py` strict against the live lane. Against an export it prints `strict pass=1/64 cdroot_fail=63`, because the cd-root check needs the live path. Only the gated count (`executes=40 gated=24 broken=0`) is meaningful on an export.
- The 8-row prototype is my construction in scratch, not a lane draft. No F28 draft or C1 re-ground draft exists yet under `wave1/` (only `R46ExecPlain.draft` and `R46ScribeRegistry.draft`), so I did not grade them.
- No non-author semantic check of any row against its entry's claim was run; F2 and F3 establish only what the counter can and cannot see.
- The `cd /home/vgpnk/...` prefix in every recheck line is host-specific. The counter strips it; a non-operator host would not run these lines as written.
- Installs: none. Scratch removed (`ls -d` → "No such file or directory").
