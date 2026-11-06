# MutC1Hunt — round 81 / attempt 1 (C1 mutation hunt on the recheck-cwd successor)

Seat: `MutC1Hunt` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Attack seat: no lane, corpus or instrument edits. Frozen bytes untouched.

## Pins and baseline

| artifact | path | sha256 |
|---|---|---|
| frozen candidate | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/c1/recheck-cwd-census.py` | `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0` |
| frozen counter | `.../round-81/c1/mutbat.py` | `fa96223b38f93b5fd9a08d11923dc7f7fe7f35a61b734c0cb3503381062843b4` |
| frozen table | `.../round-81/c1/mutant-table.json` | `abcc834eb21102f11a11cc91b7482f68957f988ea91e68e803a82251a216d095` |

Baseline (pristine copy, fresh dir): `rc=0`, `selftest cases=22 failures=0`, no `FAIL`, no
`Traceback` — `clean_pass=true`. After the battery the frozen candidate re-hashed to the same
`a3b58aa5…` bytes (`frozen_unchanged=true` in `results.json`).

## Method

* 50 single-transform mutants derived from the frozen candidate and kept **outside** the
  frozen 59-row table: every `(anchor, replacement)` pair is asserted distinct from all table
  pairs in the driver, and every anchor must occur exactly once in the frozen bytes.
* Each mutant is written to its own fresh directory and run as
  `TMPDIR=<fresh dir> python3 -B <mutant> --selftest`, exactly the frozen counter's shape.
* Classification reuses the frozen counter's own functions (`mutbat.fail_lines`,
  `mutbat.clean_pass`, `mutbat.verdict`), imported read-only, with a declared `kill_cases`
  set per row. Verdicts therefore mean what they mean under `mutbat.py`: case-matched
  `KILLED`, `SURVIVED` on exit 0, `DIRTY` on a non-zero exit without a
  `selftest case=<id> FAIL` line, `MISKILLED` on FAILs only outside the declared cases.
* Survivors and DIRTY rows get a probe: in-process calls comparing pristine vs mutant, or a
  composed second transform (often a frozen table row) whose detection the survivor is
  supposed to keep alive. Probe evidence is in `MutC1Hunt-receipts/survivor-probes.json`.

## Tally

| bucket | count |
|---|---|
| rows outside the frozen table | 50 |
| KILLED | 17 |
| SURVIVED | 29 |
| DIRTY | 4 |
| MISKILLED / NOT-DERIVED | 0 / 0 |
| survivors classified **real gap** (probe differs) | 25 |
| survivors classified **equivalent** (probe identical) | 4 |
| masking probes (table row or contract guard lost) | 13 |

Killed rows: `RC01 RC02 RC03 RC04 RC06 RC07 RC12 RC13 RC14 RC22 RC27 RC29 RC30 RC39 RC41
RC49 RC50`. Notably the two constant-`True` stubs (`RC49`, `RC50`) are killed by the round-79
F1 wiring guard (`gate-wiring`, then `gate-checkids`), not by the check they stub; that is the
intended guard behavior and it is why the clean conjunct *deletions* (`RC05`, `RC25`) are the
surviving shapes.

DIRTY rows: `RC23 RC44 RC45 RC46` — all detected loudly (non-zero exit) but not countable
under the frozen case-matched classifier; see "Counter-semantics findings".

## Survivors — real gaps (25)

Probe notation: `+Sxx` = the surviving mutant has the frozen table row `Sxx` applied on top;
`pristine+Sxx` is the control. `clean 22/0` = `selftest cases=22 failures=0`, rc 0.

| id | surviving transform | probe evidence | verdict |
|---|---|---|---|
| RC05 | conform-limbs: delete `and "norecheck=1 restoration_only=0" in out15n` | pristine+S37 fails `conform-limbs`; mutant+S37 is clean 22/0 | **real gap** — conform-limbs no longer pins the bucket line, so table row S37 is lost |
| RC10 | case16 stderr assertion reduced to `"is not a directory"` | pristine+wrong-path message fails `{tmpdir-file,tmpdir-refusal}`; mutant+wrong-path fails only `{tmpdir-refusal}` | **real gap** local to case 16; case 13 provides redundant coverage for the same secondary defect |
| RC11 | case16 `ret16 == 2` widened to `ret16 in (0, 2)` | pristine+guard-`return 0` fails `{tmpdir-file,tmpdir-refusal}`; mutant+same fails only `{tmpdir-refusal}` | **real gap** local; same case-13 redundancy |
| RC15 | delete `globals()["TIMEOUT"] = saved_timeout17` | after selftest: pristine `TIMEOUT=120`, mutant `TIMEOUT=1`; both clean 22/0 | **real gap** — leaked global; any later slow case/consumer times out at 1 s |
| RC18 | unconditional `os.environ["TMPDIR"] = saved_tmp18` | with `TMPDIR` unset: pristine clean 22/0, mutant `TypeError: str expected, not NoneType` (DIRTY) | **real gap** — selftest is only valid with `TMPDIR` set; the counter always sets it |
| RC19 | usage-guards: drop `"usage:" in err19.getvalue()` | pristine+usage-print-removed fails `usage-guards`; mutant+same is clean 22/0 | **real gap** — masks a missing usage line |
| RC20 | usage-guards: `ret19u == 2` → `ret19u in (0, 2)` | pristine+S30 fails `usage-guards`; mutant+S30 is clean 22/0 | **real gap** — masks frozen table row S30 |
| RC21 | usage-guards: delete the `exit19 == "recheck-cwd: no corpus/knowledge …"` line | pristine+S31 fails `usage-guards`; mutant+S31 is clean 22/0 | **real gap** — masks frozen table row S31 |
| RC24 | `--verbose` branch sets `verbose = False` | `main --verbose`: pristine prints `ENTRY p.md`, mutant does not (both rc 0) | **real gap** — the flag surface is untested |
| RC25 | output-lines: delete `and "ENTRY a-prefixed.md" not in _t1` | pristine+`if True:` ENTRY print fails `output-lines`; mutant+same is clean 22/0 | **real gap** — masks over-printing for passing entries |
| RC26 | output-lines: `"RESTORATION-ONLY r.md"`/`"NORECHECK n-neither.md"` → bare markers | pristine+wrong marker name fails `output-lines`; mutant+same is clean 22/0 | **real gap** — marker entry names unpinned |
| RC28 | output-lines: `"ENTRY b-relative.md noprefix=1 foreign_exit=2"` → `"ENTRY b-relative.md"` | pristine+truncated ENTRY line fails `output-lines`; mutant+same is clean 22/0 | **real gap** — ENTRY columns unpinned for prefix-less entries |
| RC31 | census ENTRY condition `code == 2` → `code in (1, 2)` | mutant prints `ENTRY d-exit1.md noprefix=0 foreign_exit=1`; pristine prints none | **real gap** — extra diagnostic lines are unconstrained |
| RC32 | census ENTRY condition drops `verbose` | `census(..., verbose=True)`: pristine prints `ENTRY p.md`, mutant does not | **real gap** — `--verbose` untested end-to-end |
| RC33 | new gate row `(gate_consume_ok(1, [True]), False)` → `(True, True)` | pristine+S08 fails `gate-predicates`; mutant+S08 clean 22/0 | **real gap** — identity-edge row is the only detector of S08 and can be tautologized |
| RC34 | new gate row `(gate_negpolarity_ok(False, 0), False)` → `(True, True)` | pristine+S40 fails `gate-predicates`; mutant+S40 clean 22/0 | **real gap** — masks S40 |
| RC35 | new gate row `(both_headers_ok(True, 1, False), False)` → `(True, True)` | pristine+S41 fails `gate-predicates`; mutant+S41 clean 22/0 | **real gap** — masks S41 |
| RC36 | new gate row `(gate_checkids_ok(["a"],["a"],[[False,True]]), False)` → `(True, True)` | pristine+S13 fails `gate-predicates`; mutant+S13 clean 22/0 | **real gap** — masks S13 |
| RC37 | new gate row `(wiring_findings(zero_src), …)` → `(True, True)` | pristine+S15 fails `gate-predicates`; mutant+S15 clean 22/0 | **real gap** — masks S15 |
| RC38 | new gate row `(wiring_findings(upper_src), …)` → `(True, True)` | pristine+S43 fails `gate-predicates`; mutant+S43 clean 22/0 | **real gap** — masks S43 |
| RC40 | F1 test `ok.value is True` → `ok.value == True` | `wiring_findings('check("x", 1, "")')`: pristine no F1; mutant emits `F1:x:1` | **real gap** — integer 1 satisfies the F1 constant guard |
| RC42 | `first_recheck`: `startswith("recheck:")` → `startswith("recheck")` | entry `recheck-ish: true`: pristine `norecheck=1`; mutant `noprefix=1, exit_other=1` | **real gap** — header word match unpinned |
| RC43 | `run_foreign` child env replaced by `{"TMPDIR": scratch}` | entry testing an inherited variable: pristine `exit0_foreign=1`; mutant `exit1_foreign=1` | **real gap** — env inheritance unasserted |
| RC47 | selftest scratch `dir=os.environ.get("TMPDIR") or None` → `dir=None` | selftest mkdtemp recorder: pristine 0 `dir=None` calls, mutant 1 of 29 | **real gap** — the docstring's "every temp path honours TMPDIR" is unenforced |
| RC48 | census `env_tmp = os.environ.get("TMPDIR") or None` → `None` | census mkdtemp dirs: pristine `[TMPDIR]`, mutant `[None]` | **real gap** — `tmpdir-parent` explicitly allows `dir is None`, so /tmp use is legal |

### Survivors — equivalent (4)

| id | transform | probe evidence | verdict |
|---|---|---|---|
| RC08 | conform-limbs: drop the `"RECHECK-CWD-RESULT nonconformant" in out15e` conjunct | 16/16 crafted count combinations: pristine and mutant both satisfy `(ret==1) == nonconformant line` | equivalent — `main` prints the RESULT line on every `ret==1` path; conjunct is redundant |
| RC09 | case16: drop `out16 == ""` | bogus TMPDIR: both `ret=2`, stdout empty | equivalent — the guard writes only stderr |
| RC16 | tmpdir-unset uses `os.environ.get` instead of `pop` | refused value `False` in both `unset` and `valid_dir` states for both modules | equivalent on reachable states; only TMPDIR visibility differs, and the file-TMPDIR state is refused before case 18 (see note) |
| RC17 | `refused18 in (False, None)` instead of `refused18 is False` | truth table: only divergent combination is `(refused=None, no exception)`, unreachable | equivalent |

Note on RC16/RC17: the *check* named `tmpdir-unset` never actually observes an unset TMPDIR
when the harness sets `TMPDIR` (both modules see `False` either way). That is a test-intent
observation for round 82, not a behavior difference this mutant introduces.

## Masking probes (13)

`RC05 RC19 RC20 RC21 RC25 RC26 RC28 RC33 RC34 RC35 RC36 RC37 RC38` each become the sole
reason a frozen table row (or an equivalent contract guard) stops being killed:
`S37, usage-line, S30, S31, over-print guard, marker-name guard, ENTRY-column guard, S08,
S40, S41, S13, S15, S43` respectively. Every probe compared
`pristine+second` (FAILs on the expected case) against `mutant+second` (clean 22/0).
This is the central coverage result: the 59-row table's kills are load-bearing on exact
assertion text, and a single surgical deletion in the candidate neutralizes a row while the
table still reports `rows=59 … neutral_ok=3/3`.

## Counter-semantics findings (DIRTY, not counted as kills)

| id | transform | observed |
|---|---|---|
| RC23 | `while i < len(argv):` → `while i < len(argv) - 1:` | `--bogus` is ignored; `main` falls through to `census(".")`, which raises `SystemExit` and escapes the case-19 capture. Non-zero exit, no FAIL line → DIRTY. The crash **depends on the counter's cwd**: run from the lane root, `census(".")` would execute every `corpus/knowledge` recheck instead of failing fast — an isolation hazard for the runner, not just a scoring one. |
| RC44 | `if not ok: failures.append(case)` → `failures.append(case)` | rc 1, `selftest cases=22 failures=22`, no `FAIL` line, no Traceback → DIRTY. A self-broken tally is outside the case-matched rule. |
| RC45 | delete case-13 TMPDIR restore | rc 1, `FileNotFoundError` in the next `tempfile.mkdtemp` (Traceback) → DIRTY. The restore is load-bearing, but crashes cannot be counted. |
| RC46 | delete case-16 TMPDIR restore | rc 1, `NotADirectoryError` in case 17 (Traceback) → DIRTY. Same. |

These four are detected by any human/runner (non-zero exit) yet score as not-killed under
`mutbat.verdict`. Round 82 should decide whether a non-zero exit with no FAIL line should count
as a kill for rows that declare `class: "assertion"`, or whether a dedicated `crash` class is
needed; today a mutant that only crashes is outside the tally.

One attribution correction is recorded rather than hidden: `RC41`
(`_pred_call(node.args[1])` → `args[0]`) was initially declared against `gate-predicates` and
scored MISKILLED. It is in fact killed by the self-parse F2/F3 findings on its own
`check("gate-wiring", consumed(wiring_log, wiring_ok(wfind)), …)` call. The probe still shows
the uncovered shape: for
`check("gate-consume", consumed(gate_consume_ok(True, y), gate_negpolarity_ok(x, y)), "")`
pristine emits `F2:gate-consume` while the mutant wires `args[0]` and emits `F4:gate-consume`.
No gate row exercises an asymmetric `consumed()` shape; only the self-parse catches this exact
transform.

## Round-80 survivors re-run against the r81 candidate (10/10 still survive)

All ten were applied as their original single transforms to the r81 bytes and run through the
same detector; every one still exits 0 with `selftest cases=22 failures=0`.

| id | transform | probe (pristine vs r81 mutant) |
|---|---|---|
| R80S03 | glob enumeration no longer sorted | patched glob order: pristine a,b,c / mutant c,b,a |
| R80S06 | `DEFAULT_LANE` = fleet root | fixture prefixed with the lane: pristine conformant rc0 / mutant nonconformant rc1 |
| R80S18 | `consumed()` arity guard removed | `check("gate-consume", consumed(x), …)`: pristine returns findings / mutant `IndexError` |
| R80S24 | selftest scratch cleanup removed | TMPDIR after run: pristine `[]` / mutant `[recheck-cwd-selftest-…]`, both rc0 |
| R80S29 | summary line format `entries = %d` | pristine `RECHECK-CWD entries=1 …` / mutant `entries = 1 …` |
| R80S32 | `leftover = 0` | +run_foreign-cleanup-removed: pristine fails `scratch-cleanup` / mutant clean 22/0 |
| R80S33 | `capture()` no longer restores stdout | subprocess stdout: pristine 3758 chars incl. cases line / mutant 0 chars, rc0 |
| R80S36 | gate-wiring read-failure fallback → `[]` | unreadable own file: pristine `F0:unreadable` + FAIL gate-wiring rc1 / mutant clean rc0 |
| R80S38 | tmpdir-parent drops `dir is None` limb | selftest with TMPDIR unset: pristine clean 22/0 / mutant FAIL `tmpdir-parent` |
| R80H27 | fresh-cwd fixture → `recheck: true` | +`cwd=None`: pristine fails `prefix-census` / mutant clean 22/0 |

The r81 seven new checks did not close any of them. Their failure modes are the same class as
the real gaps above: assertions on exact text/buckets that can be weakened, guards that are
only load-bearing under a composed regression, and environmental assumptions (`TMPDIR` set,
readable own file) the counter never varies.

## Highest-value additions for round 82 (routed defects; no verdict changes here)

1. **Pin the r81 gate rows structurally, not only by count.** A row replaced by `(True, True)`
   keeps `len(rows) == GATE_ROWS` and passes. Either pin each row's expected value via an
   independent literal table compared with `==` against `(predicate_call, False/True)` pairs, or
   assert that every gate predicate appears in at least one row with both polarities
   (a `frozenset` of `(name, expected)` per predicate). Six of the twelve new rows are the sole
   detector of a frozen table row (`S08/S13/S15/S40/S41/S43`), so this is the cheapest depth
   win.
2. **Make the weakening shapes fail the F1 guard symmetrically**: F1 currently accepts a
   non-bool constant via `==` (RC40) and it is the only thing that kills `and True` stubs. Extend
   F1 to reject any `Constant` operand that is not `False` and bind its rows; add an F1 row for a
   deleted conjunct that leaves no constant.
3. **Give the new checks discriminating limbs**: conform-limbs' bucket line (RC05), usage-guards'
   usage text/exit message/lane fixture (RC19–RC21), output-lines' entry names/columns/absence
   (RC25/RC26/RC28) and ENTRY policy (RC31/RC32) all need exact-text rows; each now masks a
   frozen table row or a contract guard when deleted.
4. **Cover the environment the counter actually owns**: assert `TMPDIR` is honoured by the
   selftest scratch and by `run_foreign` (RC47/RC48), vary `TMPDIR` unset (RC18/R80S38), and run
   the selftest with an isolated cwd (RC23) — the current runner inherits its cwd, so one mutant
   can turn `--bogus` into a full-corpus execution.
5. **Restore/leak limbs**: keep a post-selftest `TIMEOUT == 120` assertion (RC15) and treat the
   four DIRTY shapes explicitly (crash class or a "non-zero exit, no FAIL" kill rule).
6. **r80 survivors to carry into r81's successor table** (all ten rows above are table-ready
   anchors with declared cases; their probes show real behavioral differences).

## Reproduce

```
S=/fast/scratch/hyaku/kasegi-r81/MutC1Hunt
TMPDIR=$S/t python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt/driver.py
```
Scratch (`$S`) was deleted after the run; the report and receipts remain. No tools were
installed or upgraded (pacman paused; nothing needed). No `git`/`jj` writes.

## Files written

* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt.md` (this report)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt/driver.py`
  (`sha256 6350be037188782e45fa7f5e1718e5e8472fe664399b44355f4f2c822f183993`)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt/results.json`
  (`sha256 5e6e66ae60bef68637b04a870e7501923c5120c99bf2210428ed808e2df588e3`; full rows, probes, pins)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt-receipts/survivor-probes.json`
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt-receipts/rows.tsv`
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/MutC1Hunt-receipts/r80-rerun.tsv`
