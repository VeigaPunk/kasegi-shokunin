# wave3/MutCounterReplay — replay of the six wave-2 counter mutants against the repaired counter

Seat: MutCounterReplay, round 31 wave 3 (residual re-review), lane `/home/vgpnk/Projects/shokunin`
/kasegi-shokunin`. Wave-3 scope: seats are READ-ONLY on the lane; every run below used mktemp scr
atch copies of the counter (`/tmp/mutreplay-w3.4sZs1H`); the only lane write is this receipt.
Answering model: zai/glm-5.3-flash (config route; no model passed to any call — all steps are det
erministic shell/Python, bound 10 n/a for outcomes). Tooling: nothing installed or upgraded, no pa
acman transaction (host-paused), Python 3 stdlib only (bound 5: nothing needed).

## Verdict in one table

The repaired counter `corpus/instruments/limb-mutation-check.py` (sha256
`237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4`, matches the item's frozen val
ue) kills **all six published wave-2 counter mutants** on the landed ledger. No published mutant
survives. Two SUPPLEMENTARY guard-harness tamper probes of my own design (the residual class Exec
CounterFix §7 declared out of their scope) survive the frozen kill rule — coverage findings, repo
rted in §6; no contract change proposed.

| mutant (wave-2 receipt) | exit | frozen-kill-rule clauses tripped |
|---|---|---|
| alwayskilled (MutCtrAlwaysKilled) | 1 | exit-nonzero; lacks `controls=3 rejected=3` (prints `rejected=2`); all 13 LIMB lines live==mutant; guard invalid-timeout FAIL |
| no-live-baseline (MutCtrNoLiveBaseline) | 1 | exit-nonzero only (guard `invalid-live-baseline … FAIL`, `guard cases=3 failures=1`; both summary lines still print) |
| no-compile-check (MutCtrNoCompileCheck) | 1 | exit-nonzero; lacks `controls=3 rejected=3` (`CTL-nocompile verdict=invalid:import … ok=n`, `rejected=2`) |
| non-unique-find (MutCtrNonUniqueFind) | 1 | exit-nonzero only (guard `invalid-find-count … FAIL`, `failures=1`) |
| signal-ignored (MutCtrSignalIgnored) | 1 | exit-nonzero; lacks `limbs=13 killed=13 survivors=0` (prints `limbs=13 killed=12 survivors=1`; FR-missing-entry → survivor) |
| timeout-killed (MutCtrTimeoutKilled) | 1 | exit-nonzero only (guard `invalid-timeout … FAIL`, `failures=1`) |

## 1. Subject bytes and quiescence (bound 6)

```
$ sha256sum <lane>/corpus/instruments/limb-mutation-check.py <lane>/corpus/instruments/limb-ledger.json
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  limb-ledger.json
$ git -C <lane> status --porcelain -- corpus/instruments
(empty)
```

Identical hashes re-measured AFTER all eleven runs (§8): the subject bytes were quiescent for the
whole probe; no PRE-STATE labeling needed. Scratch: `SCR=$(mktemp -d /tmp/mutreplay-w3.XXXXXX)` →
`/tmp/mutreplay-w3.4sZs1H`; `cp` of the lane counter hashed identical to the lane bytes. All nine
planned find strings (six published mutants + two guard probes, one is two-hunk) were verified to
occur EXACTLY ONCE in the repaired counter before editing (`helper.py count`: every `count=1`);
ledger check: `limbs=13 controls=3`.

## 2. Baseline — real counter twice + selftest (frozen C1 counter command)

```
$ env PYTHONDONTWRITEBYTECODE=1 python3 $SCR/counter-real.py \
    --ledger <lane>/corpus/instruments/limb-ledger.json --root <lane >$SCR/real-1.out 2>$SCR/real-1.err
real1_exit=0 ; real2_exit=0 ; stdout cmp=identical ; stderr cmp=identical
1258 bytes stdout, 0 bytes stderr; sha256(real-1.out) = d6aefddca50293347c348646479bbe406745ad316
3422b27edefcea861264270
```

Baseline is LIVE (not PRE-STATE): exit 0, exactly the frozen predicate output — 3 guard fixture li
nes ok + `guard cases=3 failures=0`, 13 `LIMB … verdict=killed` lines each with live-result != mut
ant-result, 3 `CONTROL … ok=y`, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`. The out
put hash equals the one recorded in wave2/ExecCounterFix §5 (`d6aefddc…`), so the repaired counter
reproduces byte-for-byte on this seat's runs. `--selftest`: exit 0, `selftest cases=20 failures=0
` (all eleven verdict fixtures, six validation fixtures, both aggregates, control-verdict rule — f
ull 21-line listing in `$SCR/selftest.out`).

## 3. The six published mutations, applied to scratch copies

Each mutant = wave-2 receipt's published diff applied verbatim to a `cp` of the repaired counter (
`mut-<name>.py`); every mutant `py_compile`s ok. Mutant sha256:

```
bc50441e4b4eb02e3420c1f52a81d7adfb9a1ebcd9a77bdf7058dd9a887cc7ce  mut-alwayskilled.py
2662d32845fa8ac2e33596f3de9e2a8cf380ce074ff9fa1d63e99601dbc9c6e0  mut-nolive.py
3364f2d40ae4b7dd62b821043197a7832e3b7d9f28e88dca616c0a3c20fcb24a  mut-nocompile.py
3f74ac9b5b3f74fae95cdc68f7cfcf618af1d03368a284ebc4684fb167bfc908  mut-nonunique.py
a7b161dbdde57d3d046d55d50843a45e9a426779d14453f0f4e2edeb0574c459  mut-signalignored.py
f56cda84ee6f3c51de443288e2dc3fb1b1881f83ddf2b106e347481f37c7382e  mut-timeout.py
```

Substitutions (old → new, all unique strings in the repaired bytes):

- **alwayskilled** (2 hunks, as published): `mutant = measure_side(row, make_scratch, mutated, ti
meout)` → `mutant = {"token": "ok", "exit": row["live_exit"], "display": str(row["live_exit"]), "
signal": True}  # MutCtrAlwaysKilled: mutant run skipped`; and `"killed" if killed else "survivor"
` → `"killed"  # MutCtrAlwaysKilled: always report killed`.
- **nolive**: the eight-line live-baseline block (`live = measure_runs(...)` through the second `
invalid:live-baseline` return) → `live_exit = str(row["live_exit"])  # MUTANT never-run-live-base
line: trust the declaration`.
- **nocompile**: deleted `if not compiles(instrument_path, scratch):` + its `invalid:nocompile` r
eturn.
- **nonunique**: `if text.count(row["find"]) != 1:` → `if text.count(row["find"]) == 0:`.
- **signalignored**: `killed = mutant["exit"] != row["live_exit"] or not mutant["signal"]` → `kil
led = mutant["exit"] != row["live_exit"]`.
- **timeout**: mutant-side branch `return verdict_row(live_exit, "y", mutant["display"], "n", "in
valid:timeout")` → `… "n", "killed")`.

Each run used the item's exact command shape: `python3 $SCR/mut-<name>.py --ledger <lane>/corpus/i
nstruments/limb-ledger.json --root <lane>` (lane read-only; counter writes only its own mktemp scr
atch). stderr was 0 bytes on every run.

## 4. Mutant runs — complete output deltas vs the byte-identical baseline

Full stdout of every run is kept in `$SCR/mut-<name>.out`; per-mutant `diff real-1.out mut-<name>.
out`:

**alwayskilled** (exit 1):
```diff
guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
guard cases=3 failures=0
```
→ `guard invalid-timeout … verdict=killed … FAIL`, `guard cases=3 failures=1`; all 13 LIMB lines
become `live=<e>/y mutant=<e>/y` (fabricated mutant column equals live; e.g. `LIMB RA-parse live=
0/y mutant=0/y verdict=killed`); `CONTROL CTL-equivalent verdict=killed expected=survivor ok=n`;
`controls=3 rejected=2`. Caught by: exit-nonzero + missing-exact-control-summary + all-13-live==m
utant (LIMB clause) — three independent clauses, matching MutCtrAlwaysKilled §5's prediction plus
the new guard FAIL (that tester's run predated the guards).

**nolive** (exit 1): only the guard block changes —
```diff
-guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
+guard invalid-live-baseline  verdict=killed               want=invalid:live-baseline FAIL
-guard cases=3 failures=0
+guard cases=3 failures=1
```
Both frozen summary lines still print; the catch is the exit-nonzero clause, exactly the ExecCoun
terFix §5 design.

**nocompile** (exit 1):
```diff
-CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
+CONTROL CTL-nocompile verdict=invalid:import expected=invalid:nocompile ok=n
-controls=3 rejected=3
+controls=3 rejected=2
```
Guards all ok (the three guard-fixture mutants still compile, so the dropped gate never fires for
them). Same two changed lines as the wave-2 probe of the pre-fix counter.

**nonunique** (exit 1):
```diff
-guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
+guard invalid-find-count     verdict=killed               want=invalid:find-count   FAIL
-guard cases=3 failures=0
+guard cases=3 failures=1
```
All 13 LIMB lines byte-identical to baseline (every ledger `find` occurs exactly once, so `!= 1`
and `== 0` remain the same predicate on the ledger); catch is exit-nonzero only.

**signalignored** (exit 1):
```diff
-LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
+LIMB FR-missing-entry live=1/y mutant=1/n verdict=survivor
-limbs=13 killed=13 survivors=0
+limbs=13 killed=12 survivors=1
```
Guards all ok; catch is exit-nonzero + missing-exact-limb-summary, same tripwire limb (FR-missing-
entry) as wave 2.

**timeout** (exit 1):
```diff
-guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
-guard cases=3 failures=0
+guard invalid-timeout        verdict=killed               want=invalid:timeout      FAIL
+guard cases=3 failures=1
```
Catch is exit-nonzero only; LIMB and CONTROL lines and both summaries unchanged.

Wall times per run on the loaded box (siblings running concurrently): baseline pair 188.8 s total,
alwayskilled 69.5 s, nolive 30.8 s, nocompile 75.0 s, nonunique 50.6 s, signalignored 46.7 s, time
out 38.5 s, guardcmp 35.8 s, guarddrop 38.2 s, selftest 2.2 s. All guard fixtures classified corre
ctly in every run (no load-induced guard misclassification observed).

## 5. Guard-fixture vacuity check (item requirement)

Method: for each of the three guard fixtures, mutate the counter CHECK the fixture exists to guard
(the published mutants are exactly such single-gate mutations, since no ledger row trips these gat
es), and observe the fixture's own line.

| guard fixture | gate mutation applied | fixture notices? | vacuous? |
|---|---|---|---|
| `invalid-live-baseline` | nolive (live-baseline block deleted) | YES — prints `FAIL`, failures=1, exit 1 | not vacuous |
| `invalid-find-count` | nonunique (`!= 1` → `== 0`) | YES — prints `FAIL`, failures=1, exit 1 | not vacuous |
| `invalid-timeout` | timeout (mutant timeout → `killed`) | YES — prints `FAIL`, failures=1, exit 1 | not vacuous |

Corroborating: the alwayskilled mutant (which neuters the MUTANT side under every fixture) is noti
ced by exactly the `invalid-timeout` fixture — the only one of the three whose fixture row reache
s the mutant run at all (the other two are stopped by their own earlier gates: baseline signal los
s, find count 2). So each fixture is tight: it fails when its gate breaks and passes when its gate
holds.

## 6. SUPPLEMENTARY guard-harness tamper probes — two SURVIVORS (coverage findings)

ExecCounterFix §7 states the residual risk: "a mutant that edits `run_guard` could neuter them" (t
he guard class was not attacked in wave 2). I probed it with two single-substitution mutants of my
own design on the same repaired bytes:

- **guardcmp** — neuter the guard comparator in `run_guard`: `ok = result["verdict"] == want` (the
 line after the `GUARD_TIMEOUT` evaluate_row call, disambiguated from the identical selftest line)
 → `ok = True  # MUTANT guard comparator neutered`. Result: exit 0, stdout **byte-identical to th
e real counter** (`cmp` clean), both frozen summary lines, 13 LIMB lines → **SURVIVES the frozen k
ill rule** (mutant sha256 `56a2ba530a0bd2144a65b490d09f476fec4688f46cad693de3ff1a3b342704a0`).
- **guarddrop** — delete the `invalid-timeout` fixture tuple from `guard_rows()`. Result: exit 0,
both frozen summary lines, 13 LIMB lines; only the guard block shrinks (`guard cases=2 failures=0
`, the fixture line and total line gone) → **SURVIVES the frozen kill rule** (mutant sha256 `2219
760bfde189c132d2779712c34b5668020bd62bebac31de0f224d5b754da5`). The frozen rule as stated in the
item/claims pins the two summary lines, 13 LIMB lines and exit 0 — it does not pin the guard block
, so a counter that deletes a guard fixture is not caught.

Reading: each guard FIXTURE is sound (§5), but the guard HARNESS is not tamper-evident — a counte
r that (a) neuters the comparator, or (b) removes a fixture, prints the frozen target output. Comb
ining such a tamper with one of the three gate-mutants would re-open the wave-2 survivors (e.g. no
live + guardcmp prints the target lines with exit 0 again). Per my role this is a coverage finding
, not permission to change the contract: the frozen claims text is untouched and no re-freeze is p
roposed here. If the L1 wants closure, the natural route is the one ExecCounterFix already hinted
(`--selftest` already carries fixture-level checks; a guard-block presence/comparison self-asserti
on folded into the ledger-run exit would close both probes) — routed to the L1/ExecCounterFix, not
 implemented by this seat.

## 7. Kill-rule assessment against claims.json C1

`mutants_of_the_counter` (claims.json C1) requires each listed counter mutant to "fail the 3 contr
ols or the LIMB-line clause" — i.e. NOT print both `limbs=13 killed=13 survivors=0` and `controls=
3 rejected=3` with exit 0. Measured: alwayskilled fails both the controls clause and the LIMB clau
se; nocompile fails the controls clause; signalignored fails the LIMB clause; nolive, nonunique an
d timeout pass controls and LIMB lines but exit 1 via guard failures (the repaired counter folds `
guard cases=<n> failures=<f>` into the exit status), so they print at most one of the two target c
onditions with a non-zero exit. Six of six published mutants: KILLED. The C1 `counter_commands` an
d the item's real-counter runs reproduce the frozen predicate (§2).

## 8. Restoration / lane integrity

- Lane bytes AFTER all eleven runs — identical to §1: counter `237fd07cbcb4a12a470e912d1a4b68ff19
68fde62f2709b182822fed42d791f4`, ledger `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765
d6ed03be`.
- `git -C <lane> status --porcelain -- corpus/instruments` → empty after the runs.
- The lane tree was never written by this seat; every mutated byte lives in `/tmp/mutreplay-w3.4s
Zs1H`. Counter-internal scratch cleanliness: `ls -d /tmp/limb-mutation-* | wc -l` → 0 after all ru
ns (the counter deletes every scratch lane it builds).
- Nothing to restore (no lane byte was modified). Scratch kept as the command-to-output trail for
L1 re-derivation: `/tmp/mutreplay-w3.4sZs1H` (counter-real.py, 8 mutants, all .out/.err, helper.p
y); ~330 KB total.

## 9. Commands as run (verbatim; `$SCR` = `/tmp/mutreplay-w3.4sZs1H`, `$LANE` = lane root)

```sh
SCR=$(mktemp -d /tmp/mutreplay-w3.XXXXXX); echo "$SCR" > /tmp/mutreplay-w3.path
cp "$LANE/corpus/instruments/limb-mutation-check.py" "$SCR/counter-real.py"
sha256sum "$SCR/counter-real.py" "$LANE/corpus/instruments/limb-ledger.json"   # §1 values
git -C "$LANE" status --porcelain -- corpus/instruments                        # empty
python3 "$SCR/helper.py" count                                                 # 9 find strings count=1, limbs=13 controls=3
env PYTHONDONTWRITEBYTECODE=1 python3 "$SCR/counter-real.py" --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE" > "$SCR/real-1.out" 2> "$SCR/real-1.err"   # x2
cmp "$SCR/real-1.out" "$SCR/real-2.out"                                        # identical
env PYTHONDONTWRITEBYTECODE=1 python3 "$SCR/counter-real.py" --selftest        # cases=20 failures=0, exit 0
# per mutant m in alwayskilled nolive nocompile nonunique signalignored timeout guardcmp guarddrop:
#   cp counter-real.py mut-$m.py; edit-tool one published substitution (alwayskilled: two); py_compile; then:
env PYTHONDONTWRITEBYTECODE=1 python3 "$SCR/mut-$m.py" --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE" > "$SCR/mut-$m.out" 2> "$SCR/mut-$m.err"; echo "exit=$?"
diff "$SCR/real-1.out" "$SCR/mut-$m.out"
# classification: helper.py classify <m> <exit> <out>  (frozen-kill-rule clause checker)
sha256sum "$SCR"/mut-*.py "$LANE/corpus/instruments/limb-mutation-check.py" "$LANE/corpus/instruments/limb-ledger.json"
ls -d /tmp/limb-mutation-* 2>/dev/null | wc -l                                 # 0
```

## Bounds

Writes: this receipt only (plus `/tmp` scratch). No git/jj mutation anywhere (read-only `status`,
`rev-parse` scope only); no fleet-root, sibling-lane, shokuknow, scripts/, templates/, `.ufo/state
` write; no pacman or tool install; no network fetch; no live bounty target; no credential materia
l; no subagents, no background jobs of my own (the harness auto-backgrounded two long counter runs
past the 60 s foreground window; results were consumed from their deliveries). Quotes: program ou
tput lines quoted verbatim from captured files; claims/COUNT fragments ≤ 25 words with their file
or JSON-key location; no number retyped from memory — every figure above is copied from a captured
output listed in §2/§4/§8 or the diff/summary blocks in §4/§6.
