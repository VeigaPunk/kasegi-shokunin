VERDICT: BROKEN — the declared axis `depth:verifiability` is not supported for C1. C1 moves neither scored limb; the honest statement is `depth:verifiability 4 → 4 (held)`, with the round's increment recorded under the quality trend, not as an axis move. (Axis-naming critic, seat R45CritAxisC1, read-only; no edits, no commits.)

## Scope attacked

Round-45 C1 as frozen in `.ufo/waves/round-45/claims.json` (`"axis": "depth:verifiability"`, base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`, claims-sha256 `bbe40503…c6206` per `freeze.txt`). The five routed defects R1-R5 (`corpus/lessons/round-44-verifier-spotcheck.md` §6, items 1-5) and the counter `corpus/instruments/r45-routed-defects.py` (read from lane HEAD `5242db6`, because the counter is not in base `dc5bb8c`). Question: is `depth:verifiability` the right axis, and does C1 move either limb?

## Finding 1 — what the axis is, per the lane's own definitions

- `AXES.md` (fleet root, `/home/vgpnk/Projects/shokunin/AXES.md:11`): `| **depth** | Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources |`. There is no `depth:verifiability` row there; the sub-axis exists only because the lane split `depth` (AXES.md:37-38 allows a split "recorded in `SCORECARD.md` with reason"). The lane has no `AXES.md` of its own (`find . -iname '*AXES*'` in the lane returns nothing).
- The split is recorded at `SCORECARD.md:71-76`: depth:verifiability is "whether a reader can open what the skill cites" — the `resolve.py` citation-resolution fraction (`SCORECARD.md:33-38`).
- The scored axes of this lane are only depth and coverage: `MISSION.md:23`: `kasegi:     { cwd: kasegi-shokunin/, axes: "depth + coverage (bounty/security research)" }`. `SCORECARD.md:3-6`: "Lane axes per `../MISSION.md`: **depth + coverage** … The other four axes (operability, freshness, calibration, adjacency) are worked by their owning lanes … adjacency evidence from this lane is reported, not scored here."
- The trend mapping that C1's content actually belongs to: `AXES.md:21`: `quality ↔ depth + freshness + operability`; `LEARNING.md:3-4`: "its corpus expands, the **quality** of what it holds rises"; C1 R2 adds QUALITY.md criteria, the textbook quality-trend move.

## Finding 2 — the promotion bars for 4 → 5 (the limbs C1 would have to move)

`SCORECARD.md:1536` `### depth:verifiability, 4 → 5`. Limb 1 at `SCORECARD.md:1540`: "**0 gated rechecks.** `python3 corpus/instruments/recheck-audit.py --root . --quiet` prints `executes=<n> gated=0 broken=0`…". Limb 2 at `SCORECARD.md:1541`: "**The score-5 audit bar.** `SCORECARD.md:331`: "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."" Coverage bar header at `SCORECARD.md:1547`.

Structural scope check (what the limb instruments can read at all):

- `grep -n 'glob' corpus/instruments/recheck-audit.py` → `171: for path in sorted(glob.glob(os.path.join(root, "corpus/knowledge/*.md"))):` — limb 1 reads `corpus/knowledge/*.md` only. No C1 repair (R1 SOURCES/lesson, R2 QUALITY.md, R3 registry/README/SKILL, R4 `freeze-check.py`, R5 receipt) adds or edits a knowledge entry.
- `SCORECARD.md:331` / limb 2 reads "source chains" of the knowledge entries; C1's `S072` is a SOURCES registry row, not a knowledge-entry chain.

## Finding 3 — measured: C1 surface moves the counter, not the limbs (do-nothing vs. marker-only vs. C1-approximation)

Fixtures in my scratch (removed on exit): `base` = `git archive dc5bb8c | tar -x`; `marker` = base + appended correction/registry text only (SKILL.md table, lesson "Correction (round 45)" line, three QUALITY.md rows, one SOURCES S072 row), no tools; `c1fix` = marker + `R45ExecFreezeA.draft/freeze-check.py` + `R45ExecFrontB.draft/r44-frontier-count.py`. The fixture is an approximation of a C1 landing (see limitations).

Counter, run as `python3 corpus/instruments/r45-routed-defects.py --root <tree> --baseline <base>` from the lane HEAD tool tree:

- base (do-nothing): `limb R1 fixed=0 read=row-S072=absent` / `limb R2 fixed=0 read=quality-not-append-only-or-unchanged` / `limb R3 fixed=0 read=selftest-rc=2-tokens=None` / `limb R4 fixed=0 read=freeze-check-absent` / `limb R5 fixed=0 read=refiled-absent` / `routed-defects total=5 fixed=0 unresolved=5 exit=1` — matches the frozen `expect_before`.
- marker-only: `limb R1 fixed=0 read=manifest-absent` / `R2 fixed=0 read=R47-cells=2` / `R3 fixed=0 read=selftest-rc=2-tokens=None` / `R4 fixed=0 read=freeze-check-absent` / `R5 fixed=0 read=refiled-absent` / `routed-defects total=5 fixed=0 unresolved=5 exit=1`.
- c1fix: `R1 fixed=0 read=manifest-absent` / `R2 fixed=0 read=R47-cells=2` / `R3 fixed=0 read=readme-row-absent` / `R4 fixed=0 read=replay-rc=1` / `R5 fixed=0 read=refiled-absent` / `routed-defects total=5 fixed=0 unresolved=5 exit=1`.

Limb instrument, `python3 corpus/instruments/recheck-audit.py --root . --quiet`:

- base: `executes=39 gated=24 broken=0 …` / `lines=63 total=63 pass=63 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1`
- marker: `lines=63 total=63 pass=63 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1`
- c1fix: `lines=63 total=63 pass=63 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1`

Gated count identical across do-nothing, marker-only and C1-approximation: C1 does not discriminate on limb 1 (the gated count stays 24). `score-gap.py --root <base>` prints `gap: 24 of 63 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` and the census figures `census-lane: 134/1480 = 9.05%`, `census-skill: 32/506 = 6.32%` (read from the committed file, not recomputed).

Also: the counter's selftest-free R3 and R4 limbs read the approximations as absent/failing — the counter does discriminate on its own predicate (fixed stays 0 for every non-landed surface), so the frozen counter is not vacuous; it simply measures routed-defect closure, not a limb.

## Finding 4 — the lane's own record already grades this kind of increment as quality, not as a score move

`SCORECARD.md:1712` (round 44, depth:verifiability row): "4 held — **measured** … **Score delta: 0** — the axis number stays where the saturation window holds it; the increment is graded under the quality trend, not as a score move". `SCORECARD.md:1727` (round 44 final measurement) repeats it as "**Score delta: 0** — the saturation window keeps the axis number; the increment is graded under the quality trend". Round 44's C1 was also a routed-defect counter (`fixed=8 unresolved=0`) that the lane held at 4. Round 45 C1 is the same kind of claim with the same kill-rule shape (counter-only; no limb predicate). The frozen kill rule in `claims.json` ("C1 fails if the counter prints fixed<5 … or if any control … grades fixed=5") has no clause that could fail on a limb; a fully landed C1 could therefore verify on the counter and still not move depth:verifiability — the state the lane has recorded as "held" across its rounds 17–44 scorecard rows.

## Finding 5 — the depth:verifiability measurement is not re-derivable at base (affects the "held 4" statement itself)

- `git show dc5bb8c:corpus/instruments/citation-survival.md | sed -n 5p` → `Scope: `SKILL.md` + `corpus/**/*.md` (50 files).`; line 33 → `- lane total (SKILL.md + corpus): **134/1480 = 9.05%**`.
- Live count at the same base bytes: `find corpus -name '*.md' | wc -l` → `213`; `resolve.py <base>` (14 min wall, output file `citation-survival.md` in my scratch) printed `distinct=4121 resolves=40 mirror=0 internal=826 other=0 gone=3255 skill=87/630 corpus=836/3742 all=866/4121`, and its header read `Scope: SKILL.md + corpus/**/*.md (183 files)`.

So the committed 134/1480 census of record describes a 50-file scope; the base scope is 183 files (213 corpus .md on disk). The "held 4" is therefore carried by a stale committed figure that the current instrument does not reproduce from the base bytes. This does not change the C1 verdict, but any "held" statement should say the limb-2 number is the committed census, not a live measurement.

## Finding 6 — the one C1 surface that can move the census is SKILL.md

`resolve.py` scope is `SKILL.md` plus `corpus/**/*.md` (`resolve.py:7`; `resolve.py:305`: `files = [os.path.join(repo, "SKILL.md")]`). C1 R3 requires a `## Round-45 Gates & probes registry addition` table in SKILL.md with path-bearing rows (`r44-frontier-count.py`, `r44-routed-defects.py`, `wave-registry.py`). Adding path citations to SKILL.md can change the census numerator and denominator without any citation being verified — a citation-padding route. I did not finish measuring this: the c1fix census rerun was still running when L1 asked for the Report, and I cancelled it (`proc://bg_20523/kill`), so the live effect of the SKILL table on the census is UNMEASURED.

## Recommendation (the honest score statement)

1. Do not declare C1 as `depth:verifiability`. Name the surface: **routed-defect closure — QUALITY criteria (R2), freeze tooling (R4, operability), registry/gate hygiene (R3), source correction (R1), receipt hygiene (R5)**, verdict under the **quality trend** (`LEARNING.md`), with the counter's `fixed=k/5` as the measurement.
2. Score statement: **depth:verifiability 4 → 4, HELD.** C1 moves neither limb (gated 24 unchanged; no knowledge chain touched; census-of-record stale). Do not write `improved`.
3. If the lane wants a depth:verifiability move, a limb must move: `gated` (24 → 0, which needs base restoration or re-anchoring of the 23 `~/Projects/bounties` guards and the `citation-bases.md` anchors — explicitly out of C1 scope), or a re-derived census at the judged base. Neither is C1.
4. If R3's SKILL.md table lands, re-run `resolve.py` on the landed tree and report the delta as "measurement-surface change, not verification" so it cannot be read as a verifiability gain.

## Limitations

- My C1 "approximation" (`c1fix`) is not a faithful landing: R1 is a hand-written S072 row without a manifest entry, R2 rows are approximate, and R4's `freeze-check.py` (the executor draft A) replays with `replay-rc=1` in the fixture, so the counter reads `fixed=0` on it. The approximation is used only to test whether limb values move, not to grade R1-R5.
- The live census rerun on `c1fix` did not complete (cancelled per L1 instruction after ~15 min); the SKILL-table effect on the census is unmeasured (Finding 6).
- Recheck-audit on the base export exits 1 with `strict pass=1/63 cdroot_fail=62` because the export is not at the `~/Projects/shokunin` path; the gated count (24) is the value I compared, which matches the r39 baseline `executes=26 gated=24` at `SCORECARD.md:1543`.
- The axis definitions come from the fleet-root `AXES.md` and `MISSION.md` and from the lane's own `SCORECARD.md:33-38`; I did not read `PROTOCOL.md` or the protocol aggregator that might re-define depth:verifiability.
- No pre-existing measured round-45 post-landing numbers exist (the C1 repairs are not committed); all C1-after statements above are fixture-based or from the frozen counter.
- Installed/updated tools: none. Scratch `/fast/scratch/hyaku/kasegi-r45/R45CritAxisC1` removed on exit. Nothing committed, nothing mutated in git/jj/index, no shared production file touched; the only lane-repo write is this Report.
