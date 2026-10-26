# MutG5G8 — mutation probe: `r38-closure.sh` limbs G5, G6, G7, G8

Round 38 wave1, lane kasegi-shokunin. Judged axis: depth:verifiability. Probe window 2026-10-26T18:37–18:53Z. Leaf seat — no subagents, no writes outside scratch + this receipt.

## Source under test

- The executor deliverable `wave1/ExecSuiteBuild.r38-closure.sh` was found at poll check #2 of 4 (check #1 18:37:56Z absent; found 18:42:56Z, 61159 bytes). The **real suite** was therefore mutated; the fallback "own minimal implementation" route was not needed.
- Copied byte-exact into scratch. `sha256sum` of the scratch copy equals the wave-dir original: `85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6` (1473 lines). The wave-dir original was never modified.

## Detector (bounded; identical for pristine, every mutant, and the restored copy)

- **(a) base export** — `TMPDIR=$S bash <suite> --export-ref a173b0c2b98c5ae39599fa9be76027fbbead0b9e --work $S/work-<id>-base`: the limb must **stay red where it is red at base**.
- **(b) selftest** — `TMPDIR=$S bash <suite> --selftest --export-ref a173b0c2… --work $S/work-<id>-st`: kill signal is the limb's `selftest case=G<n> mutants=<ok>/<n>` ratio dropping below `n/n` (a fixture-mutant accepted by the mutated check).
- Baseline note: the selftest's **positive** limbs require the judged head J, which had not landed during the probe (lane HEAD `7001535`, no `.ufo/waves/round-38/final-gates/`). On the base ref the pristine selftest is `cases=8 failures=8` with **every** fixture-mutant ratio full; the fixture machinery is export-independent, so the per-case ratio is a valid kill detector on this red baseline. Control mutant `M-G6b` is **killed** (5/5 → 4/5), proving the detector actually rejects a broken conjunct rather than rubber-stamping.

## Pristine baselines (actual outputs)

Base export run (18:45:47Z; lane HEAD `7001535`, porcelain 17 — L1 mid-landing):

```
G1 payload=province-correction=0,readme-correction=0,province-fence=closed,readme-fence=open,declared-blocks=0,declared-ok=0 closed=0
G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,digest-match=0,run-lines=0,closed-line=0,selftest-lines=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0,head-token-lines=0 closed=0
G3 payload=resolutions-section=0,line-tokens=0,added-pending=0,added-placeholders=0,diff-read=ok closed=0
G4 payload=dispatches=0,pairs=0,seats-ok=0,read=fail closed=0
G5 payload=round38-section=0,final-lane-commit-lines=0,correction=0,f3246559=1,anchor-ancestor=1 closed=0
G6 payload=r36=absent,r37=absent,r38=present,work=inside,tolerated=none,read=ok closed=0
G7 payload=filled-section=0,correction=0,proposal-rows=0,missing=0 closed=0
G8 payload=r37-suite=1,r37-closed=0,r37-exit=1 closed=0
closed=0/8 exit=1
```

Selftest on the base ref (2.46 s):

```
selftest case=G1 positive=fail mutants=3/3 verdict=fail
selftest case=G2 positive=fail mutants=6/6 verdict=fail
selftest case=G3 positive=fail mutants=2/2 verdict=fail
selftest case=G4 positive=fail mutants=2/2 verdict=fail
selftest case=G5 positive=fail mutants=4/4 verdict=fail
selftest case=G6 positive=fail mutants=5/5 verdict=fail
selftest case=G7 positive=fail mutants=2/2 verdict=fail
selftest case=G8 positive=fail mutants=2/2 verdict=fail
selftest cases=8 failures=8
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
```

Sanity: `bash -n` ok; plain run (no `--export-ref`, no `--selftest`) refused with exit 2 — the claim's refusal behavior holds.

## Mutant table

| id | limb | style | find → replace (line) | mutated sha256 | base export run | selftest case | demo probe (pristine → mutant) | verdict |
|---|---|---|---|---|---|---|---|---|
| M-G5-corwid | G5 | widen regex | L596: drop `&& index($0, "f3246559") > 0 \` from the `cor` awk — a `Correction (round 38)` line no longer has to name `f3246559` | `2b21d3d7f006897360ad2bc399ddcd0ba68798d11012c16fb28a4dc66771c4cf` | `closed=0/8 exit=1`, payloads byte-identical to pristine | `case=G5 … mutants=4/4` unchanged | G5-cor-nohash tree: pristine `correction=0` rc=1 → mutant `correction=1,f3246559=0,anchor-ancestor=1` rc=0 | **SURVIVED** |
| M-G6-elifdel | G6 | delete condition | L693-695: delete `elif [ -e "$sroot/kasegi-r38" ] \|\| [ -L "$sroot/kasegi-r38" ]; then r38=present` — a non-directory `kasegi-r38` counts as `absent` | `861629d647a8cefa30fade00d4d3843835a52494bf294180ee515ffcf5501b5b` | `closed=0/8 exit=1`, payloads byte-identical | `case=G6 … mutants=5/5` unchanged | g6-file-root (kasegi-r38 is a FILE): pristine `r38=present` rc=1 → mutant `r38=absent` rc=0 | **SURVIVED** |
| M-G7-secwid | G7 | widen regex | L717: extractor `{ if (NR > s && $0 ~ /^## /) exit; print }` → `{ print }` — the filled section no longer ends at the next `## ` heading | `0cba056c0e6866395eb820e44ee9185bf46842ffe209c6e3185aead4472a0b13` | `closed=0/8 exit=1`, payloads byte-identical | `case=G7 … mutants=2/2` unchanged | g7-launder ledger (empty filled section; Correction + 7 rows in a later `## ` section): pristine `correction=0,proposal-rows=0,missing=7` rc=1 → mutant `correction=1,proposal-rows=7,missing=0` rc=0 | **SURVIVED** |
| M-G8-rcdel | G8 | delete condition | L753: drop `&& [ "$rc" -eq 0 ]` from the pass condition — the carry-over suite may exit nonzero while printing `closed=14/14 exit=0` | `317e120036de509697f2b459c1a2940b9418f9751cf72c23d24b4e4c737f3fb7` | `closed=0/8 exit=1`, payloads byte-identical | `case=G8 … mutants=2/2` unchanged | g8-rc fake suite (prints `closed=14/14 exit=0`, exits 1): pristine `r37-closed=1,r37-exit=1` rc=1 → mutant same payload rc=0 | **SURVIVED** |
| M-G6b-r36del | G6 | delete condition (detector-sanity control) | L698: drop `[ "$r36" != present ] && [ "$r36" != unreadable ] \` from the pass condition | `6b04e37ae70dbf938eb9e774cedb6b8d4b9a2caa6da807cf1a2d2c735d9dac5f` | `closed=0/8 exit=1`, payloads byte-identical | `case=G6 … mutants=4/5` — `mutant=r36-leftover-file rejected=0 rc=0` | (not needed — killed by the suite's own fixture) | **KILLED** |

Diff evidence: every mutant's base-run output differs from pristine **only** in the `suite-sha256=` header line (the mutant's own digest — proving the mutant bytes executed); every payload line and `closed=0/8 exit=1` byte-identical. Every mutant's selftest output differs from pristine only in the G6 control-detail `tolerated=` paths (per-mutant `--work` dir names) — except M-G6b, which shows exactly the predicted kill (`rejected=1` → `rejected=0 rc=0`, ratio 5/5 → 4/5).

## Findings — four surviving mutants, each a selftest coverage gap

A surviving mutant is a coverage finding, not permission to change the contract; nothing in the lane was edited.

1. **F-G5 (limb G5, M-G5-corwid).** Missing fixture: a tree whose round-38 SCORECARD section carries a `Correction (round 38)` line with anchor-ancestor wording naming a hash **other than** `f3246559`. The `g5_fixture` knobs cover only section/final/correction **presence** (`correction=no` removes the line entirely; the `correction-inside` hazard fixture quotes `f3246559`), so no negative fixture exercises the anchor-hash conjunct of the `cor` awk. Suggested fixture: `g5_fixture correction=otherhash` + `st_neg … 'correction=0'`. Note the payload still discloses the anomaly (`f3246559=0`) — the gap is in the pass condition, not the payload.
2. **F-G6 (limb G6, M-G6-elifdel).** Missing fixture: a scratch root where `kasegi-r38` exists as a **non-directory** (file or symlink). All G6 fixtures build directory roots; the `elif` branch has zero coverage, and under the mutant a stray file at the root is laundered to `r38=absent` (payload and verdict both wrong). Suggested fixture: `printf x > "$root/kasegi-r38"` + `st_neg … 'r38=present'`.
3. **F-G7 (limb G7, M-G7-secwid).** Missing fixture: a ledger with content **after** the filled section — e.g. a later `## ` heading carrying its own `Correction (round 38)` line and proposal-numbered rows. `g7_fixture` ends at the last proposal row, so the extractor's next-`## `-heading bound is never exercised; under the mutant a later section's rows and correction are laundered into the round-37 filled section (payload laundered too). Suggested fixture: `g7_fixture trailing=section` + `st_neg … 'proposal-rows=0'`.
4. **F-G8 (limb G8, M-G8-rcdel).** Missing fixture: a fake r37 suite whose last line is exactly `closed=14/14 exit=0` but which **exits nonzero**. The existing `carry-over-red` fixture conflates both limbs (it prints `closed=13/14 exit=1`), so deleting the `[ "$rc" -eq 0 ]` conjunct is invisible to it. The payload stays honest under the mutant (`r37-exit=1` printed) while the verdict greens. Suggested fixture: fake suite printing the right line + `exit 1` + `st_neg … 'r37-exit=1'`.

The killed control (M-G6b) shows the selftest's negative machinery does fire when a fixture covers the mutated conjunct — the four survivors are genuine fixture gaps, not a broken harness.

## Restoration evidence

- Protocol per mutant: mutate the scratch working copy → run detector (a) → run detector (b) → run demo probe → restore pristine bytes → verify sha256. Restoration verified after **every** mutant (`OK` × 5); final working-copy sha256 `85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6` == pristine.
- Wave-dir original `ExecSuiteBuild.r38-closure.sh` sha256 unchanged (`85d33ea9…`) — never written.
- Lane state: HEAD `7001535` throughout; porcelain 17 (18:45:47Z) → 19 (18:47–18:53Z) — the L1's concurrent wave1 landing, not this seat (this seat wrote only under its scratch and this receipt).

## Notes

- G8 is red at base in **every** run (`r37-exit=1`): live-state artifact — the lane worktree is dirty mid-landing and the r37 suite's live limbs red on a dirty lane by construction (suite header: "a dirty lane or a stale HEAD reds G8"). Identical for pristine and all mutants, so comparisons are unaffected. The before-control's `closed=14/14` was measured at freeze when the tree was clean at base==HEAD.
- The claimed green selftest shape (`--selftest --export-ref J` → `cases=8 failures=0`) needs J, which lands post-wave; that counting command is the L1's to run. This probe's verdicts rest on the export-independent fixture-machinery ratios, validated by the killed control.
- No tools installed or upgraded (bash/python3/git/coreutils only); pacman untouched.
- All suite fixture writes (including G2's fixture repos, whose toplevel the suite itself asserts equals the fixture dir) lived under `--work` inside `/fast/scratch/hyaku/kasegi-r38/MutG5G8`; the suite's EXIT trap cleared `export/` and `mut/` each run. Scratch dir removed before yield.
