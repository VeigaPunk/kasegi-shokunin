# MutC1Suite — one-limb mutation test of the drafted `r36-closure.sh`

Seat: MutC1Suite (leaf, no subagents) · Round 36, hyaku run 9 · judged axis depth:verifiability · 2026-10-26.
Instrument under test: `corpus/instruments/r36-closure.sh` DRAFT by ExecC1SuiteBuild, bytes taken verbatim from the committed receipt `.ufo/waves/round-36/wave1/ExecC1SuiteBuild.md` (```bash fence) after the builder declared FINAL and removed their scratch.

- **Suite digest tested:** `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (894 lines, 39 022 bytes). Fence-extracted twice (12:5x and 13:0x), identical both times; re-compared against the receipt again at 13:1x — still `4db1ae70…`.

## Detector (bounded, per the limb-mutation-check.py ledger pattern)

`corpus/instruments/limb-mutation-check.py` semantics adapted to a bash instrument, run by a scratch rig (`run_rig.py` + `ledger.json`, removed with my scratch; definitions reproduced below so the run is reproducible):

- one find/replace per row, required to occur **exactly once** in the pristine bytes (`invalid:find-count`);
- `find == replace` → `invalid:noop`; mutant must pass `bash -n` (`invalid:nocompile`) — bash has no import step, so the checker's import gate is covered by the parse gate plus the kill run itself;
- kill command run **twice per side** on separate fresh scratch lane copies; unstable → `invalid:{live,mutant}-baseline`;
- **killed** iff the mutant's (exit, signal) differs from the pristine live baseline; otherwise **survivor** (a survivor is a coverage defect, reported — not relabeled);
- the ledger carries an `expect` field per row so predicted survivors are reported as findings, not failures (`expect mismatches=0` required for rig exit 0).

**Kill command (every row):** `bash {inst} --selftest --export-ref <fixture-HEAD> --lane <fixture-lane> --work {root}/st-w --scratch-root {root}/st-s` with `live_exit=0`, `signal=(?m)^selftest cases=9 failures=0$`. The suite's own selftest is the per-limb fixture harness: each E1–E9 case carries one-or-more reopen fixtures whose rejection the weakened limb must lose, so a killed mutant makes the suite report that check open/red (`selftest case=E<i> … verdict=fail`, exit 0→1).

## Green fixture lane (pristine positive control)

Built inside my scratch as a verified git fixture (`git init` with `rev-parse --show-toplevel` checked equal to the fixture root before any mutating command; all mutating git ran with `-C <fixture>`): `git fetch <lane> b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` + `reset --hard FETCH_HEAD` (full r35 history present so E1's `cat-file -e` / `merge-base --is-ancestor` resolve), then five overlays and two commits → fixture HEAD `6b4658d0a26c0ba911f1d11f08f1f3a4f5bf5389`, worktree clean:

1. SCORECARD.md: appended `## Round 36` block with `**Final lane commit: `b47f2cdf…`**` (the freeze SCORECARD has **no** Round-36 heading — E1 open at the freeze);
2. SKILL.md: two registry rows inserted inside the `## Gates & probes registry` section (SKILL.md:977): `r35-defect-closure.sh` and `r36-closure.sh`. **Measured fact:** at b47f2cd no `r35-defect-closure.sh` row exists anywhere in SKILL.md (grep = 0 lines) — the round-35 addition section (SKILL.md:1094) registers `r-defect-closure.sh` (the round-33/34 name) and `kill-rule-check.py`, so the final head must add the exact-basename row for E3 to close;
3. `.ufo/waves/round-35/wave1-results.json.provenance.md` (non-empty — E4 requires `-s`);
4. `corpus/lessons/round-36.md` with `M36-1`/`M36-2` rows naming `source-recheck` (round-35 lesson exists and its stale line is already gone at the freeze: grep `source-recheck exit 0 on committed bytes` = 0).

## Pristine baselines (independent reproduction, suite sha `4db1ae70…`)

| Probe | Command (abridged) | Result |
|---|---|---|
| green fixture | `--export-ref 6b4658d0… --lane fixture` | `closed=9/9 exit=0` — E1..E9 all `closed=1` |
| green selftest | `--selftest` on fixture | `selftest cases=9 failures=0`, exit 0, `judge=own-report accepted=1`, all four forged reports rejected |
| r35 base | `--export-ref 3266c99… --lane <lane>` | `closed=0/9 exit=1` — **matches frozen claim C1's negative control exactly** (all E1–E9 `closed=0`) |
| r35 judged head | `--export-ref 0aee0ef… --lane <lane>` | `closed=3/9 exit=1` (closed: E5 E6 E7) — satisfies "closed<9/9" |
| claims freeze | `--export-ref b47f2cd… --lane <lane>` | `closed=4/9 exit=1` (open: E1 no-Round-36-block, E3 no exact-basename rows, E4 no provenance note, E8 no round-36 lesson, E9 dirty/stale) |

## Rig result (12 limbs, 3 controls)

```text
guard cases=3 failures=0
limbs=12 killed=9 survivors=3 invalid=0
controls=3 rejected=3
expect mismatches=0
RESTORE sha=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4 kill=0/y ok=y
```

Per-limb mutants — exact find → replace over the pristine bytes, verdict, and the mutant's actual divergent output (the reopened fixture it now accepts):

| id | find → replace | verdict | killed by (mutant's red line, exit 1 each) | mutant sha256 |
|---|---|---|---|---|
| E1-placeholder-limb | `[ "$ph" -eq 0 ]` → `[ "$ph" -ge 0 ]` | **killed** | `E1 mutant=placeholder rejected=0 rc=0 payload=placeholders=1,…,round36-section=1,…,bound=1` | `2fdafdea347b70936c7ec1ae2d6fe7037ef576e18e71f4ab740f0ec1b850ccf1` |
| E2-row-limb | `[ "$row" -ge 1 ]` → `[ "$row" -ge 0 ]` | **killed** | `E2 mutant=marker-without-row rejected=0 rc=0 payload=erratum-marker=1,erratum-row=0,erratum-mean=1` | `c0fd051cccfe2b53dfeb5d9049b6c6c453ca230a9b0e989cc86911dc8ecd6563` |
| E3-registry-scope | awk `inreg && $0 ~ pat { n++ }` → `$0 ~ pat { n++ }` | **killed** | `E3 mutant=rows-outside-registry rejected=0 rc=0 payload=registry-r35-defect-closure=1,registry-r36-closure=1` | `c7bdfce9b723f158c939e39e394317776646a8247221ef5e6d906707a71fa750` |
| E4-provenance-limb | `…&& [ "$note" -eq 1 ] && return 0` → `…&& return 0` (t_ref/t_idx arms kept) | **killed** | `E4 mutant=provenance-absent rejected=0 rc=0 payload=tracked-ref=1,tracked-index=1,provenance-note=0` | `38df9dcb12e4ca33158a9fe845ece35cdd7cab05787d06a06ecd9f3e2a65092e` |
| E5-erratum-test | `if [ -f "$p" ] && [ -s "$p" ]; then ok=1; fi` → `ok=1` | **killed** | `E5 mutant=erratum-absent rejected=0 rc=0 payload=claims-erratum-d5=1` | `5e354b0b1520a24e06fa3af636d9fe385366aab5f225920831e62da95d930a54` |
| E6-correction-gate | `[ "$cor" -ge 1 ] && return 0` → `return 0` | **killed** | `E6 mutant=correction-absent rejected=0 rc=0 payload=path=…L1Integration.md,correction-round35=0` | `5b2163a46cce7d6ebe81ead2e518863e7c9ea7f04122aa999e019f28c5c070fb` |
| E7-r23-limb | `[ "$r22" -ge 1 ] && [ "$r23" -ge 1 ] && exit 0` → `[ "$r22" -ge 1 ] && exit 0` | **killed** | `E7 mutant=r23-row-absent rejected=0 rc=0 payload=supersedes-r22=1,supersedes-r23=0` | `c6570236d462d6f0cd7cda2bd27959892483702520c0b21115d1811315ef4242` |
| E8-stale-limb | `[ "$stale" -eq 0 ]` → `[ "$stale" -ge 0 ]` | **killed** | `E8 mutant=stale-line-present rejected=0 rc=0 payload=m36-rows=1,names-corrected-line=1,stale-line=1,round35-lesson=1` | `c2bf06a56969cd8d2a6550b06eb58ecfb14d47ddf5d1cd6416444606c5fa2b01` |
| E9-dirty-limb | `[ "$porcelain" -eq 0 ]` → `[ "$porcelain" -ge 0 ]` | **killed** | `E9 mutant=dirty-worktree rejected=0 rc=0 payload=status-dirty=1,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present` | `170f9658441d42d1874aebfe42283b48d695af860b37967fdc988a7407e5110e` |
| E2-marker-limb | `[ "$marker" -ge 1 ]` → `[ "$marker" -ge 0 ]` | **survivor** (defect, see F1) | — selftest stays `cases=9 failures=0` | `8540370fb9f577934b17eba940700075f9c1e217435ca4656303faa6bb9464dd` |
| E2-mean-limb | `[ "$mean" -ge 1 ]` → `[ "$mean" -ge 0 ]` | **survivor** (defect, see F2) | — | `c280e8609564dd364cd95ba26270c6715bdda35b2e304f76635e103f0dcbc890` |
| E3-r36row-limb | `[ "$b" -ge 1 ]` → `[ "$b" -ge 0 ]` | **survivor** (defect, see F3) | — | `bfaf44ed8508a8cbd7f7021eb07142d43db6de7b85e8846ad34c40e83e651115` |

Controls: `CTL-noop` (find==replace) → `invalid:noop` ✓; `CTL-nocompile` (`die() {` → `die() (`, sha `95750762…`) → `invalid:nocompile` ✓; `CTL-equivalent` (`MUT=$WORK/mut` → `MUT="${WORK}/mut"`, sha `0113e1c8…`) → `survivor` ✓ — the verdict gates are live in both directions.

**Verdict on C1's instrument quality:** 9/9 per-check one-limb mutants killed — every check E1–E9 is load-bearing in the suite's own selftest on real defective fixtures, and the pristine suite reproduces the claim's controls (base `closed=0/9`, judged `3/9`, green `9/9 exit=0`) end-to-end through the CLI. Three limb-isolation defects survive (below).

## Findings (survivors — report only; strengthening is the suite owner's move)

- **F1 (E2-marker-limb survivor):** no E2 fixture presents `marker=0` with `row≥1 ∧ mean≥1`, so removing/weakening the `Erratum (round 35)` marker arm passes the entire selftest. The marker requirement is currently tested only conjunctively. Fix direction: a fixture with the corrected row + mean but no marker line.
- **F2 (E2-mean-limb survivor):** the stale-mean fixture (`| depth:density | 9 | mean **201.7**, 25 blocks |`) is red via marker=0 AND row=0 AND mean=0 simultaneously — its rejection is overdetermined, so a weakened mean arm is undetected. Fix direction: give that fixture the marker and the corrected row shape so only the mean limb is red.
- **F3 (E3-r36row-limb survivor; the r35-row arm is symmetric by construction):** every E3 fixture SKILL.md is a bare fragment with no `## …Gates & probes registry…` header, so `a=0 ∧ b=0` in all five and rejection is overdetermined — a weakened row-count arm (e.g. `-ge 1` → `-ge 0`) passes the selftest. The scoping arm IS tested (E3-registry-scope killed by rows-outside-registry). Fix direction: add the registry header line to the r35only/r36only fixture fragments so one arm is red at a time.
- Provenance note (superseded intermediate, recorded because I tested it): at intermediate `c0505c47…` (829 lines) `selftest_case_E1` called the then-removed helper `e1_bound_hashes` (only `e1_final_hashes` existed; the command-not-found was silently swallowed by the `h=$REF_RESOLVED` fallback) and the E1 fixtures were heading-less, which made every E1 limb unisolable. The FINAL `4db1ae70…` bytes fix both (selftest calls `e1_final_hashes`; all four E1 fixtures carry the Round-36 heading / section as appropriate). No action needed; kept here so the earlier weakness is not lost.

## Limits of this test (declared, not hidden)

- One mutant per check (the item's one-limb rule): E1's `lane-hash-marker`/`unbound`/`history-only` arms, E2's `row` variants beyond the tested arm, E7's `r22` arm, E8's `m36`/`names`/`lesson35` arms, and E9's `scratch-seat-dirs`/`head-match`/`lane-root` arms each have an isolating fixture that the pristine suite rejects (`rejected=1` observed in the pristine selftest run), but they were not individually mutated.
- The kill detector is the suite's own selftest on a synthesized green lane, not the future round-36 final head (none exists yet); the fixture satisfies every check through the real CLI, so the positive control is end-to-end.
- Weakened mutants do not flip the base-probe output (`closed=0/9` on 3266c99) because on a fully-defective tree other limbs of the same check stay red; the selftest fixtures are the discriminating probe by design.

## Restoration and hygiene evidence

- `RESTORE sha=4db1ae70… kill=0/y ok=y` — after all 15 patches, the pristine bytes still hash to `4db1ae70…` and still produce the live baseline verdict; the rig writes only under per-side scratch lanes (deleted in `finally`).
- Fixture lane untouched by the runs: HEAD still `6b4658d0…`, `status --porcelain` empty.
- Lane repo: this seat ran only read-only git (`rev-parse`, `fetch` into the scratch fixture, `archive` via the suite, `status`, `ls-tree`); every mutating command was inside the verified scratch fixture. The `M`/`??` entries now visible in the lane worktree belong to other seats/the L1, not to me.
- No tools installed (operator 2026-10-19 authorization unused): bash, python3, git, awk only.
- Scratch `/fast/scratch/hyaku/kasegi-r36/MutC1Suite/` is removed after this receipt. Note: a fleet-wide wipe of `/fast/scratch/hyaku/kasegi-r36/` at 12:59 destroyed my first fixture build; everything was rebuilt from the committed receipt and the lane repo, so no evidence depends on the lost bytes.
