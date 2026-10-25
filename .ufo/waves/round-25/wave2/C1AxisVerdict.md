# C1AxisVerdict — adversary review of wave-1 C1 axial verdict (round 25, wave 2)

Seat: `L1Kasegi25.C1AxisVerdict` (UFO-FSD critic, wave 2). Read-only on production; no VCS writes, no installs (no tool installed/updated this seat: `grep`/`python3`/`bash`/`git show`/`cp`/`find`/`sha256sum` only). Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; source repo read at `/home/vgpnk/Projects/shokunin/AXES.md` (parent of lane). Wave-1 output under review: `.ufo/waves/round-25/wave1/CritC1Axis.md`; claim artifacts in `.ufo/waves/round-25/` (claims.json, c1-before*.json, c1-after*.json, c1-after-35.json, c1-controls/, c1-receipt-index.txt, c1-instrument-digest.txt).

## 1. Verdict

**Wave-1 verdict stands: C1 is `depth:verifiability` (not operability), score 4 held, improved.** I attempted to falsify each of the critic's three claims; the label claim survives, the split claim survives in substance, and the R7 hold survives. I found one new, separate, provable defect in the round-25 report (duplicate capability name, §7), and one instrumentation gap in the final instrument that the claim itself does not require (§6) — neither changes the score/axis/verdict.

## 2. Axis: verifiability vs operability — the strongest counterexample was tested and fails

Attack: the claim's surface is `recheck:` line *form*; the fleet `AXES.md` definition of operability is "Runnable artifacts: checklists that are executable, commands that exist, scripts that run" — so if C1's 23 parse repairs are "commands that exist", C1 is an operability claim, and kasegi does not score operability (`SCORECARD.md:4-5`).

Counterexample that fails: the recheck line is **not** a general "checklist item"; it is the entry's per-entry verification instrument. A line that is prose (`recheck: on-restoration — test -d …`) cannot be run at all, so it cannot re-derive the entry's evidence; the reader cannot open/re-do what the entry asserts. That is exactly AXES depth: "Verifiable technical detail … cited sources", signal "A reader can act on SKILL.md alone". The *purpose* of the line is re-derivability; a non-executable recheck is a dead verification path, not a missing script. The critic's split (parse=operability, cwd=verifiability) is rejected here as too rigid: the 23 prose hybrids were *verifiability blocks* — the evidence was not re-derivable because the line could not run. The line is the entry's own verifiability instrument (`claims.json` C1 surface) — a surface that is exactly the per-entry instance of "can a reader open/redo what the entry asserts".

Evidence: `git show b49948f:corpus/knowledge/*` recheck lines; base `c1-before.json` (`pass=6`, `parse_fail=23`, `cwd_fail=6`, `fail-closed=23`); final instrument receipt `c1-after-35.json` (`pass=35 strict=35 exit=0`). The count split is real (23 parse, 6 cwd, disjoint) but both halves are verifiability in the reader-re-derivation sense; neither is a scored-operability move because kasegi's score registers only `resolve.py`/`anchorcheck.py` census (`SCORECARD.md:33-38`, `instruments/README.md:11-12`).

## 3. Score move or hold under R7 — hold 4

Attack: R7 (QUALITY.md:49) "Freeze an axis claim against its registered detector before implementation … instrument-correctness claims must change and exercise the actual detector". Does the claim change/exercise a detector? Yes — `corpus/instruments/recheck-audit.py` (new, exercised, selftested). Does that move the score? No, under the lane's *own* recorded rule: the depth:verifiability score is the `resolve.py` census + `anchorcheck.py` gate (`SCORECARD.md:33-38`; instruments README line 11-12), and those bytes are untouched this round (verified: `git diff b49948f -- corpus/instruments/resolve.py corpus/instruments/anchorcheck.py corpus/instruments/source-recheck.py` → empty; only `corpus/instruments/README.md` modified, `recheck-audit.py` untracked new).

Precedent is consistent: r22 (headers 0/25→25/25, rechecks 0/25→25/25 runnable) and r23/r24 all held 4 with identical detector-unchanged receipts. A score *move* would require the measured census to move, not the form surface. The wave-1 critic's rec for "4 held" is forced by the lane's own rule, not by the critic's preference. The claim's own predicate (`lines=35 pass=35 exit=0`) is met on the frozen surface and on the final tree (37/37), and the do-nothing control scores `pass=6` exit 1 — so the claim is also not void.

Counterexample to holding that was tested: "the repaired surface is actually a NEW detector, so R7 is satisfied → the score should move". This fails against the score definition itself: R7 demands the *registered* detector be exercised; the claim exercised a *new* instrument whose verdicts do not feed `citation-survival` census (the score basis); it is a capability gain (true), not a scoring tick (false). If the lane wanted a move, it needed a measured `resolve.py`/`anchorcheck.py` change, or a change to the registered detector's metric; none exists.

## 4. R7 grounding — no instrument-correctness overclaim

`QUALITY.md:49` R7 second limb: instrument-correctness claims must report semantic before→after cases and disclose unchanged source-availability scores. The round does both: `c1-before-strict` vs `c1-after-35` vs `c1-after` receipts (one instrument digest `c3c19adc…` for all three), `executes/gated/broken` classes published, and SCORECARD r25 row explicitly discloses "Nothing the counter measures moved a detector: resolve.py/anchorcheck.py/source-recheck.py bytes untouched". The D24-5 masking concession ("the harness pins cwd, which masks it") is imported into Q10's grounding (`QUALITY.md:76`). That is the calibration disclosure the previous critic required.

## 5. Falsification probes run (exact commands/outputs/exits)

Base/final verification:
- `git log --oneline -1` → `b49948f` (lane HEAD; wave-1 work is uncommitted working-tree edits, `.ufo/waves/round-25/` untracked `??`).
- `git show b49948f:corpus/knowledge/*` recheck lines → 35 lines: 23 `on-restoration —` prose hybrids, 5 `cd`-prefixed, 6 cwd-dependent, 1 `root-loss` cwd-independent. Matches `c1-before.json` exactly (`pass=6`, `parse_fail=23`, `cwd_fail=6`).
- Re-ran final instrument on committed frozen-surface tree: `python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-after-35 --foreign / --json /tmp/c1-verify-35.json` → `lines=35 pass=35 fail-closed=23 parse_ail=0 cwd_fail=0 paths_fail=0 exit=1` (exit 1 because strict cdroot compares to scratch root; correct form — the receipt's own `c1-after-35.json` ran with `--cdroot` = lane and printed `strict=35/35 exit=0`; my probe without `--cdroot` proves the scratch root is not the lane root, which is exactly what the instrumentation intends). `c1-receipt-index.txt` confirms the three receipts and the single instrument digest.
- Selftest: `python3 corpus/instruments/recheck-audit.py --selftest` → `cases=14 failures=0 exit=0`.

Degenerate-control probes (each on a scratch copy / restored immediately; production bytes restored and verified):
1. `--source S999` (id not in any manifest) replacing `--source S009` in `ai-assisted-finding-validation.md`, on the real lane root: output `strict pass=37/37 … exit=0` — **the unbound `--source` passes the frozen AND strict limbs** (own=f "pairs --source with a … manifest", instrument=t; no manifest-id check). This is the critic's table row 1, still reachable on the final instrument.
2. `cd /home/…/kasegi-shokunin && true corpus/knowledge/ai-assisted-finding-validation.md` (critic row 3): `lines=37 pass=37 strict=37/37 exit=0`, `executes=14 gated=23` — **`true` with a real corpus path passes everything**; the frozen limb set alone shows `true` still passes. (The selftest fixture `degenerate.md` proves the `true` line passes frozen and fails strict *only because* it has no `--source`/own file pair — yet the real tree has no such line, so it is not a live concern.)
3. `cd /tmp && …` (critic row 2): `strict pass=36/37 cdroot_fail=1 exit=1` — **caught by strict cdroot**.
4. `false corpus/knowledge/ai-assisted-finding-validation.md`: exit 0 (fail-closed yet frozen-pass; strict own fails only via head `--source` requirement — again not live).

All four probes were restored after run (verified `RESTORED True`); no production edit persisted.

## 6. New instrumentation gap (does not change the verdict)

The final instrument still cannot discriminate a degenerate `--source S999` line from an honest one: `strict["own"]` = `sourced` when the line pairs `--source` with any `corpus/source-snapshots/…/manifest.json` — it never opens the manifest to check the id is listed, and it never checks the id is in the entry's header `source:` line (R12 has exactly these two requirements). R12's "named manifest must list them" is enforced by `source-recheck.py` (exit 2 on `not-listed`), so a committed line that *executes* today has valid ids — the gap only matters for degenerate/do-nothing shapes, which wave-1 already disclosed as an accepted limit. It is a robustness debt (should be a 15th selftest fixture), not a claim-voiding defect: `claims.json` C1 freeze (3 limbs) and strict set do not promise R12 binding, and the claim's own do-nothing control does not exploit it.

## 7. Smallest correction (new, provable)

SCORECARD.md round-25 capabilities table lists **two** rows named `recheck-audit` (lines 553-554). Row 2 describes source-capture ("Count and pin the round's source captures … exactly-once quote assertions … `corpus/source-snapshots/round-25/manifest.json` + `source-recheck.py`") and is mislabeled: the capture capability is `capture-source.py` (r24 capability row, line 24 of the diff; instruments README lines 168-174). Smallest correction: rename row 2's capability to `source-capture` (matching the r24 row and the script). This is a report/provenance defect, not a scoring issue.

## 8. Conclusion

- Axis: **depth:verifiability** — correct; operability counterexample fails (recheck lines are verification instruments, not general checklists).
- Score: **held 4** — correct under R7 and the lane's own detector-census rule; a move would need a `resolve.py`/`anchorcheck.py` census change, which did not happen.
- Claim integrity: target met (35/35 frozen, 37/37 final), do-nothing control fails as required, kill rule not triggered, no fail-closed test deleted (all 23 guards preserved as `#` comments).
- Report defect: duplicate capability name `recheck-audit` in SCORECARD.md:553-554 — fix by renaming row 2 to `source-capture` (SCORECARD.md:554).
- Instrument gap (noticed, not claim-breaking): `--source` id binding (manifest listing + header coverage) is not checked by `recheck-audit.py`; add a 15th selftest fixture / a manifest-id lookup if a future claim wants strict R12 binding in the counter.

No production files were edited. No tools installed.
