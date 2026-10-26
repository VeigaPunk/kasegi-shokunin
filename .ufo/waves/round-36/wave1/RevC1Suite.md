# RevC1Suite — review of the drafted r36-closure.sh (round-36, claim C1, depth:verifiability)

Reviewed bytes: `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh`, copied read-only to
my scratch as `r36-frozen.sh`. sha256 `ff616adc045a8938c7ca69b3693565ef0f676a0d1d67df293b1b6c4a82da4720`,
737 lines, `bash -n` → exit 0. (An earlier 710-line iteration sha256 `1019d64d…` was superseded
mid-review; all findings below are against the frozen 737-line bytes. Line numbers cite
`corpus/instruments/r36-closure.sh` positions = frozen scratch copy.)

## Verdict

**REFUSE for the first frozen draft `ff616adc…` (737 lines) — ADMIT for the repaired freeze
`76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323` (817 lines)**; all five
actionable findings (2 HIGH, 1 MED, 2 LOW) were repaired and are verified below (§ Re-review of the
repaired freeze). The original REFUSE rationale: two HIGH defects sat exactly on the routed defect
this round's C1 exists to close (round-35 verifier spot-check §5.3: "make D1/D3/D7 checks
section-scoped or structural") — E3 and E7 were file-wide literal greps, not registry-row/structural
checks, exposing C1 to a false pass (check green while its defect is present — a frozen kill-rule
clause). Everything else was ADMIT-grade from the start; the architecture (export-only mode,
refusal paths, fail-closed driver, self-report cross-check, forgery-rejecting selftest judge) is
sound.

## Defect list

| # | sev | where | defect | evidence | repair |
|---|---|---|---|---|---|
| 1 | HIGH | `check_e3` (:283-296) | E3 is file-wide literal: `grep -cF 'r35-defect-closure.sh' SKILL.md` / `'r36-closure.sh'` over the whole file. Frozen claim says "SKILL.md Gates & probes registry **rows** for exact basenames"; spot-check routed defect 3 demands section-scoped/structural for D3. Any prose mention elsewhere in SKILL.md (a kill-rule quote "r36-closure.sh missing (ls_exit=2)", a suite-description note) satisfies E3 with **no registry row present**. The payload label `registry-r36-closure=` promises registry scoping the check does not do. The draft's own E3-inexact selftest mutant proves basename exactness only — it cannot catch this, so the selftest is blind to the gap. | frozen :289-291; SKILL.md registry home at `:977` + appended `## Round-N Gates & probes registry addition` sections (:1037, :1050) are the structural target; today SKILL.md has 0 mentions of either basename (measured), so the gap is latent until the rows land | awk-scope to the registry sections (`^## Gates & probes registry` and `^## Round-[0-9]+ Gates & probes registry addition`, until next `^## `), require a table row whose first cell is the exact basename: `^\|[[:space:]]*r36-closure\.sh[[:space:]]*\|` (same for `r35-defect-closure\.sh`). Add a selftest mutant: basename in prose outside any registry section → must be rejected |
| 2 | HIGH | `check_e7` (:339-350) | E7 is file-wide literal: `grep -cF 'supersedes R22'` / `'supersedes R23'` over corpus/QUALITY.md. Same routed defect names D7; frozen claim says "supersedes-R22/R23 **rows** present". A prose quote (a future QUALITY erratum quoting the R26/R27 rows, another row's criterion citing them) satisfies it without the rows. Measured today: QUALITY.md carries exactly 2 `supersedes R2[23]` mentions, both table rows (:249, :250) — no live false-pass, but the check is not structural and does not close routed defect 3 | frozen :343-345; QUALITY.md :249/:250 are the row shapes (`\| R26 \| … \| supersedes R22 — …`) | row-shaped match: `grep -cE '^\| R[0-9]+[[:space:]]*\|.*supersedes R22'` (tighter third-cell anchor: `^\| R[0-9]+[[:space:]]*\|[^|]*\|[[:space:]]*supersedes R22`). Add a selftest mutant: a non-row prose line containing `supersedes R22` → must be rejected |
| 3 | MED | `check_e4` (:300) | `t_idx=$(git -C "$LANE" ls-files -- "$p")` reads the **live lane index** — live worktree state in a suite whose header says "The suite never reads the live worktree" (:14-15) and whose spec says "runs every check against THAT export (never the live worktree)". Fail-closed direction (AND limb, no false pass) and outcome-neutral: verified `tracked-index=1` in all three export runs while `tracked-ref` decided every verdict; given E9(a)+(c) (clean tree + ref==HEAD) index==ref whenever 9/9 prints, so the limb can never flip a measured outcome. It is dead weight plus a contract contradiction (the header's own justification "cannot be answered from the export bytes" is wrong for this limb — `ls-tree` at the ref answers "tracked" from git metadata without the live index) | frozen :300 vs header :14-18; T3/T4/T8 payloads all `tracked-index=1` | drop the `t_idx` limb (ls-tree at ref is the frozen measure — the spot-check's own D4 command was `git ls-tree -r`), or reword the header to "never reads live worktree *content*; git-metadata reads are enumerated". Prefer dropping |
| 4 | LOW | `check_e8` (:356-364) | The `stale==0` limb vacuously passes when `corpus/lessons/round-35.md` is **absent** from the export (grep error suppressed → empty → 0 → closed). E1 guards SCORECARD.md existence (:247); E8 has no existence guard for either lesson file. A tampered export lacking round-35.md greens the limb | frozen :358-360; `stale=${stale:-0}` maps grep-failure to the closed value | `[ -f corpus/lessons/round-35.md ] \|\| { printf 'round35-lesson-missing'; exit 1; }` before the grep (round-36.md absence already fails via `m36=0`, but an explicit guard is cheap) |
| 5 | LOW | `check_e9` (:379-384) | Limb (b) vacuously passes when the scratch root does not exist (`[ -d "$sroot" ]` false → `left=0`): a typo'd `--scratch-root` silently greens "no leftover seat dirs". Default root is the kill-rule path (correct, must stay hardcoded); only the override is exposed | frozen :379-384 | when the root is absent, print `scratch-root=absent` in the payload (keep honest) and either fail the limb or die exit 2 on an explicitly-passed absent override |
| 6 | INFO | `e1_bound_hashes` (:219-236) | E1 binds only capital-F `Final lane commit` lines. This is the **correct** fail-closed choice (case-insensitive matching would let the historical lowercase lines at SCORECARD.md:1110/:1241/:1271 bind and mask a missing round-36 line), but it imposes a cross-seat contract: the round-36 SCORECARD line must be `**Final lane commit: `<40-hex>`**` (house form per :987-988 and :1129-1130, hash possibly on the next line — the +4-line window covers that). If the SCORECARD writer follows the older lowercase style, `total=0` → E1 open → suite red at closure | SCORECARD.md:987/1129 capital-F closed forms; :1110/:1241/:1271 lowercase historical forms; grep -c 'Final lane commit' SCORECARD.md = 2 at HEAD | no code change; surface the capital-F + full-40-hex contract to the SCORECARD writer / L1 (suite header :56-60 documents the line name) |
| 7 | INFO | `check_e2` (:298-306) | E2 is the spec-pinned bare `201.2` count — weaker than r35's D2 (which had erratum-row + mean + stale-row-bytes limbs); any unrelated `201.2` mention passes. Regression-guard only. Not a builder fault (the item spec pinned exactly this form); verifier should know the claim's "erratum present" is measured this loosely | spec (wave1-spec.json ExecC1SuiteBuild item): "E2 grep -c '201.2' SCORECARD.md >=1"; measured count 6 at HEAD | none required; optional strengthening to the r35 three-limb form if the L1 wants it |
| 8 | INFO | `check_e8` (:356-364) | The `m36` limb binds a loose `M36` literal (any mention in round-36.md). The discriminator is the stale limb — measured live: phrase count **1** at the r35 judged head 0aee0ef (lesson :15), **0** at the r36 base b47f2cd — so the limb is satisfiable and discriminating, not dead-on-arrival | `git show 0aee0ef…:corpus/lessons/round-35.md \| grep -c 'source-recheck exit 0 on committed bytes'` → 1; same at b47f2cd → 0 | none; CritC1Kill will probe the loose literal |
| 9 | INFO | `--lane`/`--scratch-root`/`--work` flags | Override flags widen the surface (a tampered `--lane` makes E1/E4/E9 answer from a fake repo). The `--work` guard is good (refuses inside-lane lexical AND physical paths before any write, refuses `/`); `--lane` has no equivalent "must be the canonical lane" guard. L1's counting commands use defaults | frozen :167-183 | optional: warn (not refuse) when `--lane` differs from the default; attack-surface detail is CritC1Export's item |
| 10 | INFO | `--selftest` | Environment-dependent by design: the E9 positive limb reads the real lane + real scratch root, and E1-E8 positives read the HEAD export — so `--selftest` reads red mid-wave (expected) and greens only at the quiescent final head, which is exactly when the claim's counting command runs it. Not a bug; record so mid-wave red is not misread | frozen :723-727 (`prepare_export "${EXPORT_REF:-HEAD}"`), header :41-49 | none; document in the landing receipt |

## Kill-rule clause coverage (no count-zero escape found outside defects 4/5)

| kill clause | suite limb | escape check |
|---|---|---|
| plain run closed != 9/9 or exit != 0 | `run_suite_report` summary + exit code | self-report cross-check: 9 `^E[1-9] payload=` lines required, `closed=1$` count must equal k, else `closed=0/9 exit=1` (:404-419) — summary cannot disagree with the per-check lines |
| --selftest < 9 cases or any failure | `judge_selftest_report` (:641-657) | requires exactly 9 `verdict=pass` case lines, per-id uniqueness, exactly one summary; three forgeries rejected by construction (summary-only, summary-without-cases, cases-with-verdict=fail) |
| an E-check's fixture passes while its defect is present | per-check selftest mutants (9 case fns, 13 mutants) | every mutant must be REJECTED with the payload naming the reopened limb (`st_neg` needle match) |
| `grep -c 'filled by the L1' SCORECARD.md` != 0 | E1 placeholder limb (file-wide — mirrors the kill rule's own form; correct) | SCORECARD.md existence guarded first (:247); missing file → open, not closed |
| Final lane commit hash not exists / not ancestor | E1 hash limb (`cat-file -e` + `merge-base --is-ancestor`, :253-257) | `total>=1 && bound==total`: missing line, unresolvable hash, or side-branch hash → open. Canary run proved `bound=0` surfaces when the lane repo lacks the hashes |
| worktree not clean at filing | E9(a) `status --porcelain` | unreadable status repo → early open with `status-repo=unreadable` (:371-374); count 0 from a failed git is unreachable |
| leftover kasegi-r36 scratch seat dirs | E9(b) `find -maxdepth 1 -type d` | missing root → vacuous pass (defect 5); own `--work` excluded by realpath only when under the root |
| suite missing (ls_exit=2) | L1-level clause, not the suite's job | n/a |

Other count-zero hunts came up clean: `count_lines` (`grep -c . \|\| true`) preserves the "0" output while swallowing only the exit status; every `X=${X:-0}` default maps a failed grep to the OPEN direction for presence-limbs (E2/E3/E5/E6/E7/E8-m36) and is guarded by an existence check where absence would otherwise read closed (E1); E4's git failures map to 0 → open; E6 requires exactly 1 path candidate (0 or ≥2 → open).

## Dynamic evidence (all runs read-only; lane untouched)

| test | command (abbreviated) | observed | verdict |
|---|---|---|---|
| bash -n | `bash -n r36-frozen.sh` | exit 0 | pass |
| T1 plain-run refusal | `bash r36-closure.sh` (no args) | `refusing to run against the live worktree: this suite is export-mode only.` + hint, **exit 2** | pass (spec: refuse exit 2, explicit message) |
| T2 bad ref | `--export-ref 0000…0000` | `cannot resolve export ref in <lane>: 0000…`, **exit 2** | pass |
| T6 --work inside lane | `--export-ref HEAD --work <lane>/.ufo/waves/round-36/revc1-probe` | `--work must be outside the lane (it would write there)`, **exit 2**, and the dir was **not created** (ls: No such file or directory) | pass (guard fires before any write) |
| T7 help | `-h` | usage text, exit 0, no code bleed | pass |
| T3 r35 base export | `--export-ref 3266c993…` | **closed=0/9 exit=1**; E1 placeholders=1, E2 mean=0, E3 0/0, E4 tracked-ref=0, E5 0, E6 0, E7 0/0, E8 m36=0, E9 dirty=9/left=32/head-match=0 | pass — matches the frozen counting command |
| T4 r35 judged head export | `--export-ref 0aee0ef1…` | **closed=4/9 exit=1** (E2/E5/E6/E7 closed; E1 placeholders=1, E3 0/0, E8 stale-line=1, E9 open) | pass — closed<9/9 with E1/E3/E8 open, as the claim expects |
| T8 freeze head export | `--export-ref b47f2cdf…` | **closed=5/9 exit=1** (E1/E2/E5/E6/E7 closed; E3/E4/E8/E9 open) | pass — the four open checks are exactly the wave's landing requirements (SKILL rows, r35 provenance note, round-36 lesson, quiescence) |
| canary (export-only proof) | scratch copy of the lane at b47f2cd as its own git repo (mktemp fixture, toplevel verified), worktree dirtied with an uncommitted `filled by the L1` line, then `--lane <copy> --export-ref HEAD` | E1 payload **placeholders=0** — the suite read the committed export, not the dirty worktree; `bound=0` also proves the hash limb reads the lane repo's object database (the copy has no history) | pass — export-mode discipline proven dynamically |
| lane untouched | `git status --porcelain \| sha256sum` before/after all runs | `93ef94a8…47621fb3` identical | pass — nothing written under the lane |
| no /tmp literal | `grep -c '/tmp' r36-frozen.sh` | 0 matches | pass |
| TMPDIR honoured | `TMPDIR=$S/tprobe mktemp -d -t r36-closure.XXXXXXXX` (the suite's exact form, frozen :186) | dir created under $TMPDIR | pass |
| E8 discriminator live | phrase count at 0aee0ef vs b47f2cd | 1 vs 0 | pass — limb satisfiable and discriminating |

## Residual risk / not covered here

- I did not execute `--selftest` (RevC1Selftest's item) or the fixture matrix (ExecC1Fixtures / RevC1Fixtures), did not mutation-test (MutC1Suite), and did not run the attack matrix (CritC1Kill / CritC1Export). Defects 1/2 predict a CritC1Kill survivor: prose-mention-only SKILL.md / QUALITY.md passing E3/E7.
- E1's +4-line window binds every 40-hex token near a capital-F Final-lane-commit line (e.g. the wave-1 integration hash sharing line 987) — broader than the claim's "the Final lane commit line's hash", i.e. stricter, fail-closed; noted, not a defect.
- The selftest's E4 mutant covers the provenance limb only (1 of 3 limbs); the tracked limbs are discriminated by the base/head export runs (frozen counting commands), not by selftest mutants.

## Tooling

No tool installs or upgrades were needed or performed (bash, coreutils, git only).

## Scratch

`/fast/scratch/hyaku/kasegi-r36/RevC1Suite/` removed before yield; this receipt is the only lane write.

**Contamination note (2026-10-26, during re-review):** after my scratch dir was recreated for the
re-review, a sibling seat wrote two read-only lane-tree exports into it —
`RevC1Suite/exports/base/…` and `RevC1Suite/exports/judged/…` (full `git archive` extractions of
lane trees, files/dirs mode-locked so plain `rm -rf` failed with EPERM). These are not this seat's
files: no command of mine creates an `exports/` path, and the suite's own layout is
`$WORK/export` + `$WORK/mut` (my runs used `w-base`/`w-head`/`w-freeze`/`w2-*`/`u`/`tprobe`
subdirs). The names `base`/`judged` suggested ExecC1BaseFail's R35BASE/R35HEAD exports and
ExecC1Fixtures' base-snapshot item; **all four seats whose items touch a base/judged export pair
denied ownership with detailed path accounting (BaseFail, Fixtures, ExportMode, SuiteBuild — the
builder's exports are ~1 MB extractions deleted on exit, byte-shape mismatch with the found
~120 MB mode-locked pair) — attribution unresolved**. The full roster (41 further live peers
omitted from this seat's view) and IRC record
are the L1's sources if attribution matters. Removed with `chmod -R u+w` + `rm -rf` before yield;
no lane file was touched (the exports are copies of committed trees).

## Re-review of the repaired freeze (76273416…, 817 lines) — all findings verified repaired

Reviewed bytes: sha256 `76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323`, 817 lines,
`bash -n` → exit 0. Copied to scratch as `r36-v2.sh` and probed both statically and by direct
invocation of the repaired check functions (sourced; the `BASH_SOURCE[0] = $0` guard keeps sourcing
inert).

| finding | repair in 76273416 | verification |
|---|---|---|
| HIGH-1 E3 file-wide | `check_e3` now counts via `e3_registry_rows` — awk heading-bounded to sections whose `## ` heading contains `Gates & probes registry` (covers the main registry home and the `Round-N … addition` sections), row pattern `^\|[[:space:]]*`?basename`?[[:space:]]*\|` — first cell must be the exact basename (optional backticks, dot escaped) | unit probes: prose mention outside any registry section → rc=1 counts 0/0 (REJECTED); proper registry-section rows → rc=0 1/1 (would close); rows in a non-registry section → rc=1 (section scoping holds). New selftest mutants cover the prose/mention cases |
| HIGH-2 E7 file-wide | `check_e7` now row-shaped: `^\|[[:space:]]*R[0-9]+[[:space:]]*\|[^|]*\|[[:space:]]*supersedes R22($|[^0-9])` (third cell must BEGIN with the supersession; the `($|[^0-9])` tail also stops `supersedes R220`-style overmatch) | unit probes: prose line mentioning both → rc=1 (REJECTED); **the real committed QUALITY.md rows :249-250** → rc=0, 1/1 (the regex matches the actual bytes — no false-open at closure). New prose-not-row selftest mutant |
| LOW-1 E8 vacuous pass on absent lesson | `check_e8` gained a `round35-lesson` presence limb (absent round-35.md → limb 0 → open) plus a `names-corrected-line` limb (the round-36 lesson must mention `source-recheck`, i.e. name the line it corrects) | unit probe: round-36 lesson present with M36 + names but round-35.md absent → rc=1, `round35-lesson=0` (REJECTED) |
| LOW-2 E9 absent scratch root | `check_e9` payload now reports `scratch-root=present\|absent` (non-gating, as recommended) | T3/T4/T8 payloads show `scratch-root=present` on the real root |
| MED E4 live index limb | kept (the seat spec pins `git ls-files … = 1`), ANDed with the ref-scoped `ls-tree` limb; header reworded to enumerate the sole live reads honestly ("E9's quiescence limbs … and E4's frozen `git ls-files` index limb") | header :13-16 read; fail-closed direction and outcome-neutrality re-confirmed (tracked-index=1 in all three runs, tracked-ref decided every verdict) |
| (bonus) E9 lane-root limb | new limb: `rev-parse --show-toplevel` must equal the physical lane path — an export path or a subdirectory of an enclosing repo cannot inherit another tree's cleanliness; plus `git --no-optional-locks status` so the status read takes no transient `.git/index.lock` under the lane | real lane IS its own toplevel (limb passes there, no permanent-red risk); new selftest mutant `enclosing-repo` → needle `lane-root=0` |

Dynamic suite re-run at this digest: refusal exit 2 (plain run), bad-ref exit 2, r35 base export
**closed=0/9 exit=1**, r35 judged head export **closed=4/9 exit=1**, freeze-head export
**closed=5/9 exit=1** (E9 payloads now carry `lane-root=1,scratch-root=present`); lane
`git status --porcelain` sha256 identical before/after; export-only canary re-proven at this digest
(dirty worktree copy → E1 read `placeholders=0` from the export). 15 `st_neg` mutant calls across
E3/E7/E8/E9 selftest cases.

Remaining open items are the INFO/coordination rows of the defect list above (E2's spec-pinned
loose count, now additionally anchored by an erratum-anchor limb the builder added after
ExecC1Fixtures' prose-survivor finding; the capital-F SCORECARD contract to be surfaced to the
SCORECARD writer; `--selftest` mid-wave red is expected; `--lane` override surface is
CritC1Export's item). No further repair required from this seat.
