# PlannerWalk — round-24 instrument data-walk (wave 1)

Seat: `L1Kasegi24.PlannerWalk` — read-only bounded planner data-walk.
Measured at committed tip `c2480b143120364728b40397926ffcf30a7309c8` (`master`, = frozen base `d0a3f6a` + one commit: `corpus/lessons/round-23-verifier-spotcheck.md` only; `git diff --stat d0a3f6a..master`). SKILL.md, `corpus/instruments/density.py`, `anchorcheck.py` unchanged; `corpus/instruments/resolve.py` changed +54/-17 vs r23 baseline `922a4dde90b60b465e2b8b241d1fe363f1f27e98`.

## Instrument runs (command / output / exit)

### 1. density — `python3 corpus/instruments/density.py SKILL.md --label r24-before`
- Exit 0. Output: `# Density census — r24-before (1023 lines, 19 blocks)`; 19 blocks scored; `mean dens 154.0`; `Total path-citation instances: 652 across 19 blocks.` Block table unchanged (Pipeline 13.3 … Frontier decision table 155.6).
- **Moved since r23:** nothing — byte-identical to the r23 record (`.ufo/waves/round-23/before-instruments.json` `density.stdout`: same 1023/19/154.0/652). SKILL.md has zero commits between 922a4dd and tip.

### 2. anchorcheck — `python3 corpus/instruments/anchorcheck.py SKILL.md`
- Exit 0. Summary line: `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`. 6 `OK` in-range cites, the rest LOST-RECORDED (not checked by design).
- **Moved since r23:** nothing — identical summary vs `before-instruments.json` `anchors.stdout` (7/7/306/0/0/0/0).

### 3. resolve — `python3 corpus/instruments/resolve.py <dir>` on `/tmp` `git archive` exports
Committed-tip bytes (`sha256 690153ad…` resolve.py) on `git archive master` → `/tmp/kasegi-tip`:

```
distinct=1669 resolves=14 mirror=0 internal=216 other=0 gone=1439 skill=39/513 corpus=215/1344 all=230/1669
wrote /tmp/kasegi-tip/corpus/instruments/citation-survival.tsv
wrote /tmp/kasegi-tip/corpus/instruments/citation-survival.md
```
- Exit 0. Fractions: SKILL 39/513 = 7.60 %; CORPUS 215/1344 = 16.00 %; ALL 230/1669 = 13.78 %.
- **Moved since r23** (r23 record: `distinct=1589 resolves=11 internal=197 gone=1381 skill=39/513 corpus=192/1262 all=208/1589`, revision 922a4dd): numerator all 208→230 (+22; RESOLVES +3, INTERNAL +18), corpus 192→215 (+23 of 82 new distinct), SKILL fraction unchanged. **Attribution: 100 % content, 0 % instrument** — committed-tip resolve.py on the r23-baseline tree reproduces `1589 / 11 / 198 / 1380 = 209`, identical to the r23 script's classification of the same tree (see Reproducibility).

## Supplementary counters (C1 counter A, run verbatim from claims.json)

```
for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines authorization-safe-harbor-and-scope ai-assisted-finding-validation cwe-top25-2025-methodology multiparty-vulnerability-coordination cna-assignment-and-vulnerability-rules cra-manufacturer-reporting-duties; do r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //'); bash -c "$r" >/dev/null 2>&1; echo "$f $?"; done
```
Result: F01–F05 exit 2, F06–F08 exit 0 → **3/8**, exactly the frozen `before_expected`. Exit-2 cause verified: `source-recheck.py --source S001` prints `S001:source UNAVAILABLE reason=not-listed` (exit 2); `corpus/source-snapshots/round-23/manifest.json` `sources[]` = `[S018, S029, S030, S031]` — S001–S015 have no committed captures. Recheck commands are pure local manifest reads (safe, no writes observed).

C2 counters at tip: `awk` admitted-F-rows → **8**; `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l` → **0**; `corpus/knowledge/*.md` = 33 files (was 30 at 922a4dd), `corpus/**/*.md` = 66 (was 61).

## Reproducibility / drift findings (verifiability-relevant)

1. **resolve.py output is host-FS-sensitive, not byte-stable.** Re-running the committed r23 script on a byte-identical `git archive 922a4dd` today gives `internal=198 gone=1380` vs the r23 record's `197/1381` — a one-citation flip caused by non-lane host filesystem state changing since the record. Implication: cross-round comparisons have a ±1 noise floor on INTERNAL/GONE; the do-nothing control and the dispatch-matrix counter should be re-measured in the same session, never compared against a stored stdout.
2. **resolve.py writes the census into the script's own directory, not the target dir.** Invoking `python3 <lane>/corpus/instruments/resolve.py /tmp/export` writes `corpus/instruments/citation-survival.{tsv,md}` in the live lane tree. I polluted the lane copy this way and restored it to committed bytes (`git status` clean except pre-existing `.ufo/waves/round-24/` and sibling-seat untracked files). The r23 pattern — copy the instrument inside the export and run it there — is the correct containment.
3. **Uncommitted C1(B) fix is already measurable: −1 GONE / +1 INTERNAL.** The working-tree resolve.py diff (uncommitted, `git diff` shows brace empty-alternative kept + dangling-symlink glob skip) run on the tip tree gives `internal=217 all=231` vs committed `216/230`. The only classification delta in the TSV is citation `{}`: GONE → INTERNAL `/tmp/.../` via method `brace` — a real behavior change but a degenerate citation (`{}` → root dir). Planner note: the brace fix moves the all-fraction by one citation on this corpus; the glob skip has no observable delta on the tip tree (no dangling-symlink-first matches exist in lane `.ufo` trees).
4. **Instrument delta since r23 = zero on both trees.** Committed-tip resolve.py on old tree = old script on old tree (1589/11/198/1380). All r23→r24 resolver movement is corpus content (+80 distinct citations: round-23 lessons, knowledge F06–F08 files, source-snapshots, instrument docs), not instrument change.

## Axis one-liners (what moved since the r23 record)

- **density (score 9):** flat — SKILL.md byte-identical; mean 154.0, 19 blocks, 652 path-cites.
- **depth:verifiability (score 4):** resolvable-lane fraction 208→230 all (+22, driven by +18 INTERNAL lane-relative citations from round-23 artifacts), but the decisive surfaces are unchanged: recheck counter A still 3/8 (F01–F05 exit-2 not-listed, manifest lacks S001–S015) and committed resolve.py still drops empty brace alternatives (`{,x}`/`{x,}` → GONE `{}` case) and still first-match-credits glob.
- **coverage (score 7):** corpus grew 61→66 md files (knowledge 30→33: F06–F08 admitted in round 23) and corpus resolvability 192→215; admitted frontier topics still 8, S100+ sourced entries still 0 — the F09/adendum-10 surface is untouched at tip.

## Tooling directive record
No installs, no package operations. PACMAN untouched per pause directive. All work in `/tmp` exports + read-only repo commands; the single instrument side-effect write was reverted (finding #2).

## Remaining unknowns / UNVERIFIED
- The `resolve-dispatch-check.py` + `resolve-dispatch-fixtures.json` counter-B instrument exists only as untracked working-copy files at measure time (`git status`); I did not run it — it is another seat's surface. Counter-B baseline number for the planner must come from that seat.
- The ±1 INTERNAL drift (finding #1) is asserted as host-FS origin; the specific flipped citation was not isolated between the r23 record's run and today's re-run.
