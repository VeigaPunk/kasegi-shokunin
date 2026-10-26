# wave2/ExecCounterFix — counter-mutant survivors closed inside the counter (no 4th control, counts frozen)

Seat: ExecCounterFix, round 31 wave 2 (falsify wave), lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Write scope: `corpus/instruments/limb-mutation-check.py` and `corpus/instruments/limb-ledger.json` (fixes only), plus this receipt. All attack/replay work ran on copies under `/tmp`; the lane counter's final edit is timestamped 21:36:12 -0300, i.e. after the last `MutCtr*` receipt landed (`MutCtrTimeoutKilled.md`, 21:35:00 -0300), and that tester's own after-hash check still saw the pre-fix bytes `c660a95f…`.
Judged axes: depth:verifiability, coverage. Model: deterministic shell/Python work; no model-routed step, none recorded (bound 10 n/a). Tooling: none installed or upgraded (bound 5: nothing needed; pacman never invoked).

## 1. Verdict

**CHANGE**, smallest possible: the counter now evaluates **three implicit guard fixtures on every `--ledger` run** (not `--selftest` only) on a throwaway probe lane, and folds their result into the exit status. That kills the three counter-mutant SURVIVORS the wave-2 mutation-testers reported, **without** adding a limb or a control row: the frozen C1 lines stay `limbs=13 killed=13 survivors=0` and `controls=3 rejected=3`, exit 0.

No ledger byte changed. No limb id changed. No 13th→14th limb and no 3rd→4th control exists in the ledger; `corpus/instruments/limb-ledger.json` is byte-identical to its pre-fix state.

| subject | before (pre-fix) | after (this seat) |
|---|---|---|
| `corpus/instruments/limb-mutation-check.py` | `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` (747 lines) | `237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4` (820 lines) |
| `corpus/instruments/limb-ledger.json` | `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` | `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` (unchanged) |

`git diff --numstat` on the counter: `81  8  corpus/instruments/limb-mutation-check.py`.

## 2. Inputs — the six wave-2 counter-mutant receipts

All six seats reported (receipts 21:28–21:35 -0300); `MutCtrTimeoutKilled` landed last and its own receipt records pre- and after-hash `c660a95f…` on the lane counter, so every probe was made against the pre-fix bytes.

| receipt | mutant | verdict reported | frozen clause it was reported under |
|---|---|---|---|
| `MutCtrAlwaysKilled.md` | skip the mutant run, stamp `killed` | KILLED | controls (`CTL-equivalent` → killed, `rejected=2`) + LIMB lines (`live == mutant`) |
| `MutCtrNoLiveBaseline.md` | delete the whole live-baseline block | **SURVIVOR** | none — byte-identical to real, exit 0 |
| `MutCtrNoCompileCheck.md` | drop the `py_compile` gate | KILLED | controls (`CTL-nocompile` → `invalid:import`, `rejected=2`) |
| `MutCtrNonUniqueFind.md` | `!= 1` → `== 0` | **SURVIVOR** | none — every ledger `find` occurs once |
| `MutCtrSignalIgnored.md` | kill by exit difference only | KILLED | LIMB line (`FR-missing-entry` → survivor, `killed=12`) |
| `MutCtrTimeoutKilled.md` | mutant-side timeout → `killed` | **SURVIVOR** | none — no ledger row times out |

The three survivors share one root cause: **each verdict gate the committed ledger happens not to trip could be deleted with no observable change in the `--ledger` run.** Two testers proposed adding a 4th control bound to `invalid:live-baseline` / `invalid:timeout`. That is out of scope for this seat by the frozen predicate (`controls=3 rejected=3`) and would need a claims re-freeze; the guard route closes the same mutants with the counts untouched. All three testers were told this in reply (`agent://MutCtrNonUniqueFind`, `agent://MutCtrNoLiveBaseline`, `agent://MutCtrTimeoutKilled`); no claims amendment is needed for what landed here.

## 3. Red-before — the three survivors on the pre-fix bytes

Pre-fix counter materialised read-only from git (`git show HEAD:corpus/instruments/limb-mutation-check.py`, sha256 `c660a95f…`), each tester's published mutation applied as a single substitution, run against the lane ledger with `--root <lane>` (the counter writes only to its own mkdtemp scratch):

```sh
$ D=/tmp/ecf-red; git -C <lane> show HEAD:corpus/instruments/limb-mutation-check.py > "$D/pre-fix.py"
$ sha256sum "$D/pre-fix.py"
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  /tmp/ecf-red/pre-fix.py
$ python3 "$D/pre-fix-nolive.py"     --ledger <lane>/corpus/instruments/limb-ledger.json --root <lane>; echo $?
limbs=13 killed=13 survivors=0
controls=3 rejected=3
0
$ python3 "$D/pre-fix-nonunique.py"  --ledger … --root <lane>; echo $?
limbs=13 killed=13 survivors=0
controls=3 rejected=3
0
$ python3 "$D/pre-fix-timeout.py"    --ledger … --root <lane>; echo $?
limbs=13 killed=13 survivors=0
controls=3 rejected=3
0
```

Mutant forms (exactly the published diffs):

- `nolive` (MutCtrNoLiveBaseline §diff): the six-line live block (`live = measure_runs…` through the `invalid:live-baseline` return) replaced by `live_exit = str(row["live_exit"])  # MUTANT never-run-live-baseline: trust the declaration`.
- `nonunique` (MutCtrNonUniqueFind §diff): `if text.count(row["find"]) != 1:` → `if text.count(row["find"]) == 0:`.
- `timeout` (MutCtrTimeoutKilled §diff): `return verdict_row(live_exit, "y", mutant["display"], "n", "invalid:timeout")` → `… "killed")`.

The timeout replay is byte-identical to that tester's published mutant: both are sha256 `8d648a096d6a22d02c4fad11fb71933b40719167f226479023c4475b7e6729cb`. Mutant-file hashes from this seat's build: `nolive d37f8e0b1d2e…`, `nonunique d5eff7f5313e…` (prefixes; full files were scratch and are gone).

Red-before summary: **three counter mutants print both target summary lines and exit 0 on the landed ledger** — the hole is real, and the guard is aimed at it.

## 4. The fix — three implicit guard fixtures in the `--ledger` path

`run_ledger()` now calls `run_guard()` after `load_ledger()` and before reading any instrument; the ledger result and the guard result are ANDed into the exit status. `run_guard()` builds a throwaway lane holding only the existing `PROBE_SOURCE` (`probe_lane()`, extracted from `selftest()` and now shared by both) and evaluates one fixture per unexercised gate with `GUARD_TIMEOUT = 1`:

| guard fixture | row (probe instrument) | ledger trips it today? | must be |
|---|---|---|---|
| `invalid-live-baseline` | `find='MODE = "pass"'`, `replace='MODE = "fail"'`, `signal="^probe never$"` (baseline exits 0 but loses its declared signal) | no | `invalid:live-baseline` |
| `invalid-find-count` | `find='print("probe'` (occurs twice), `replace='print("probe2'` | no | `invalid:find-count` |
| `invalid-timeout` | `find='MODE = "pass"'`, `replace='MODE = "fail"'`, `kill='if grep -q \'MODE = "fail"\' {inst}; then sleep 5; fi; python3 {inst}'` | no | `invalid:timeout` |

Printed before the LIMB rows, one line per fixture plus a total:

```
guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
guard cases=3 failures=0
```

Why this shape and not a 4th control row:

- The frozen C1 predicate names `controls=3 rejected=3`; a ledger control bound to `invalid:live-baseline`/`invalid:timeout` would print `controls=4 rejected=4` and need a claims re-freeze (both testers flagged this themselves). Guard fixtures are neither limbs nor controls and never enter either count.
- They sit in the `--ledger` path, not in `--selftest`, because the frozen kill rule only ever sees the `--ledger` invocation (the NoLiveBaseline tester raised exactly this risk; its own selftest already failed on that mutant while the ledger run did not).
- `py_compile`/`pyflakes` untouched; nothing in the ledger schema, row validation, or output grammar for LIMB/CONTROL lines changed. Docstring grew by ~25 lines documenting the guards and the new exit rule; the output-grammar sample now lists the `guard` lines.

## 5. Green-after — real counter, double run, and every mutant replayed on the final bytes

```sh
$ cd <lane> && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json   # x2
guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
guard cases=3 failures=0
LIMB RA-parse live=0/y mutant=1/n verdict=killed
… (13 LIMB lines, all `verdict=killed`, every line live ≠ mutant) …
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
```

- run1 exit 0, run2 exit 0, `cmp` identical, sha256 of the output `d6aefddca50293347c348646479bbe406745ad3163422b27edefcea861264270`.
- `grep -c '^LIMB '` = 13; `grep -c '^guard '` = 4; both exact summary lines present.
- `python3 corpus/instruments/limb-mutation-check.py --selftest` → `selftest cases=20 failures=0`, exit 0 (the eleven verdict fixtures and six validation fixtures are unchanged; the eleven-fixture setup now calls `probe_lane()`).
- Usage paths unchanged: missing ledger → exit 2 (`ledger not found`), no `--ledger` → exit 2 (`--ledger is required`).
- Wall time on the lane: ~20 s before, ~22 s after (guard adds ~2 s, capped by `GUARD_TIMEOUT = 1`).

Every mutant replayed against the **final lane bytes** (counter copied to `/tmp/ecf-green/mut-*.py`, lane used read-only via `--root <lane>`):

| mutant | exit | summary | caught by |
|---|---|---|---|
| alwayskilled | 1 | `limbs=13 killed=13 survivors=0` / `controls=3 rejected=2` | controls |
| nolive (published diff) | 1 | 13/13/0 · 3/3 | **guard** `invalid-live-baseline … verdict=killed … FAIL`, `guard cases=3 failures=1` |
| nocompile | 1 | 13/13/0 · `rejected=2` | controls |
| nonunique (published diff) | 1 | 13/13/0 · 3/3 | **guard** `invalid-find-count … verdict=killed … FAIL`, `failures=1` |
| signalignored | 1 | `limbs=13 killed=12 survivors=1` / 3/3 | LIMB clause |
| timeout (published diff) | 1 | 13/13/0 · 3/3 | **guard** `invalid-timeout … verdict=killed … FAIL`, `failures=1` |

So on the final bytes **no counter mutant prints both target lines with exit 0**, and the real counter does (twice, byte-identically).

## 6. What deliberately did **not** change

- `limb-ledger.json`: zero bytes touched (sha256 unchanged). All 16 rows keep `find_count = 1` on their instruments; limb ids order `RA-parse … FR-duplicate-entry`, exactly 13 limbs / 3 controls.
- The two summary lines, exit-code contract (0/1/2), verdict vocabulary, LIMB/CONTROL grammar and `aggregate()` are unchanged; the guard only ANDs one more boolean into `main`'s exit for the ledger path.
- No instrument other than the counter; no entries, registry, README, SKILL.md, PROVINCE.md; no `.ufo/state`, no scripts/templates, no fleet-root write, no git/jj mutation (only `git show` / `git status --porcelain` / `git diff --numstat`, read-only).

## 7. Residual risk (stated, not hidden)

- `invalid:import` and `invalid:mutant-baseline` are **not** guard fixtures: the ledger never trips them either, but no wave-2 mutant attacked them and the seat brief says smallest fix for reported survivors. A counter that dropped the import gate or the double-run agreement would still print the target lines; its `--selftest` (fixtures `invalid-import`, `invalid-import-exit`, `invalid-nondeterministic`, `invalid-mutant-baseline`) would fail, but nothing in `--ledger` would. If wave 3 wants closure, the same guard table takes two more rows at ~0.2 s each.
- The guard fixtures are themselves counter code: a mutant that edits `run_guard` could neuter them. That class (mutating the guard) was not attacked this round.
- Guard cost is ~2 s per run and needs /tmp space for six small scratch copies; on a full `/tmp` the counter fails loudly (`shutil.Error`, non-zero) rather than printing a summary — see §8.

## 8. Environment notes (honest, with impact)

- **/tmp reached 100 % (280 KiB free) mid-seat**, from other seats' scratch trees (`du -sh /tmp/* | sort -rh | head`: `kumitate-r64` 9.3 G, `t47` 5.1 G, `c1v2-…` 4.4 G, several `tameshi-r47-*` 0.6–4 G each). One of my pre-fix replays was truncated by `[Errno 28] No space left on device` inside `build_scratch`; that output was discarded, my own scratch (~44 MB: `ecf-mut-*`, `ecf-patch.*`, `ecf-probe*`) was deleted, and every number cited above was re-measured afterwards. `/tmp` was back to 28 G free when the final runs completed. I deleted **only** my own `/tmp` entries — no peer scratch was touched.
- No pacman transaction, no tool install/upgrade, no host service restart, no model passed or selected, no network fetch, no live bounty target contacted, no credential/session material read.
- Only this seat's receipt and the two owned files were written in the lane; `/tmp/ecf-red` and `/tmp/ecf-green` remain as the command-to-output trail for the L1's closure re-derivation.

## 9. Commands as run (verbatim, `$LANE` = lane root, `$D` as noted)

```sh
# red-before: pre-fix bytes from git, three published mutant diffs, run against the lane ledger
$ git -C "$LANE" show HEAD:corpus/instruments/limb-mutation-check.py > /tmp/ecf-red/pre-fix.py
$ sha256sum /tmp/ecf-red/pre-fix.py            # c660a95f… == pre-fix counter
$ python3 /tmp/ecf-red/pre-fix-nolive.py     --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE"; echo $?   # 0
$ python3 /tmp/ecf-red/pre-fix-nonunique.py  --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE"; echo $?   # 0
$ python3 /tmp/ecf-red/pre-fix-timeout.py    --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE"; echo $?   # 0

# green-after: real counter twice + selftest on the final bytes
$ cd "$LANE" && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json > /tmp/ecf-red/green-1.out 2>&1
$ cd "$LANE" && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json > /tmp/ecf-red/green-2.out 2>&1
$ cmp /tmp/ecf-red/green-1.out /tmp/ecf-red/green-2.out && sha256sum /tmp/ecf-red/green-1.out   # identical, d6aefddc…
$ cd "$LANE" && python3 corpus/instruments/limb-mutation-check.py --selftest                    # exit 0, cases=20 failures=0

# green-after: all six wave-2 mutants on the final bytes (copies under /tmp/ecf-green, lane read-only)
$ for m in alwayskilled nolive nocompile nonunique signalignored timeout; do
    python3 "/tmp/ecf-green/mut-$m.py" --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE" > "/tmp/ecf-green/mut-$m.out" 2>&1; echo "$m exit=$?"
  done      # every exit=1 (§5 table)

# usage paths and lane state
$ python3 corpus/instruments/limb-mutation-check.py --ledger /nonexistent.json; echo $?     # 2
$ python3 corpus/instruments/limb-mutation-check.py; echo $?                                # 2
$ git -C "$LANE" status --porcelain -- corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
 M corpus/instruments/limb-mutation-check.py                       # ledger untouched
$ sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
```
