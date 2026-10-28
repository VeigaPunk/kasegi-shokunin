# ExecJ5Scan — round-42 wave-1 receipt (J5 scratch-hygiene limb, family F-SCAN)

Seat: `ExecJ5Scan` (executor, leaf). Item: build the J5 scratch-scan limb — a sourceable
bash function that audits the lane scratch area for leftover entries of the round family,
enumerates sibling round prefixes (not one literal round), and detects a leftover that
lies OUTSIDE the configured scratch root — and replay the committed round-41 defeat
artifacts against the new bytes. Axis: **depth:verifiability** (primary, C1), **coverage**
(secondary).

**Verdict: PASS.** 16/16 graded selftest cases pass; both committed round-40/round-41
defeat artifacts are replayed and rejected; the three required planted-stray scenarios
behave exactly as specified (green when clean; red over `kasegi-r41/SeatX`; red over
`kasegi-r42/OtherSeat`; red over one outside-configured-root stray); four weakened copies
of the limb bytes are each killed by the suite's own replay probe.

No lane file, fleet file, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`,
`corpus/`, `templates/`, `scripts/`, `.ufo/state/` or `.scratch/` was written. No mutating
git/jj command was run anywhere. No subagent was spawned (leaf seat; the one permitted
labrat probe was not needed).

---

## 1. Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-42/wave1/ExecJ5Scan.sh` | 759 | `157cd803bcacf97a2c43a0c5535e7df24f5abd7e7d6f5142f46183b76642eee0` |
| `.ufo/waves/round-42/wave1/ExecJ5Scan.transcript.txt` | 169 | `037c356b7a2423cc167d8634bd1b4f12e42c419d6242c273b551d83c34382289` |

`ExecJ5Scan.sh` contains only landable limb bytes: the sourceable functions, the hermetic
probe, the replay probe, and the header contract. No validation tables, no notes, no
headings that are not part of the landed text. `ExecJ5Scan.transcript.txt` carries the raw
evidence (sections 0–5 of the generator).

### 1.1 API the suite calls

Sourcing `ExecJ5Scan.sh` defines the following and executes nothing (`BASH_SOURCE[0] != $0`
guard; verified in transcript §0: `sourced-ok j5_function_count=23`,
`check_j5_type=function`).

```bash
check_j5 [--root DIR] [--work DIR] [--outside-root DIR]   # -> "J5 payload=strays=..,outside=..,read=..,scanned=..,scope=.. closed=0|1"
j5_scan_root  ROOT WORK                                  # -> "strays=N,read=ok|fail,scanned=N"
j5_scan_scope SCOPE WORK EXCL                            # -> "outside=N,read=ok|fail,scanned=N"
j5_scan_pair  ROOT WORK [OUTSIDE_ROOT]                   # -> the combined payload
check_j5_detail ROOT WORK [OUTSIDE_ROOT]                 # -> payload + one "stray: <path>" per stray
j5_fixture_init DIR                                       # -> "scope=<DIR> root=<DIR>/scratch"
```

Environment fallbacks when no flag is given: root = `$J5_SCRATCH_ROOT` else `$SCRATCH_ROOT`;
work = `$J5_WORK` else `$WORK`; outside-root = `$J5_OUTSIDE_ROOT` else `$WORK/j5-fixture/scratch`.

**Positional arguments are ignored.** The suite's r41-style `check_<id> TREE REF` dispatch
shape cannot silently repoint this check at the export tree; transcript §0 shows the
positional call failing closed (`read=fail`) rather than scanning the export tree.

## 2. The two round-41 defects this closes, and how

### Defect (a) — the sibling-round-prefix escape

The round-39 limb looked only under the literal `kasegi-r39/`; the round-40 limb only
under `kasegi-r39*`/`kasegi-r40*`; the round-41 limb only under the literal token
`kasegi-r41`. A leftover container of any *other* round was invisible to all three.

The limb's family is a **shape**, not one literal round directory: the default
`J5_FAMILY_GLOB` is `kasegi-r4[0-9]*`, so `kasegi-r40`, `kasegi-r41`, `kasegi-r42`, … are
all in scope. Matching is case-insensitive and separator-insensitive (every run of
non-alphanumeric characters folds to a single `-`, so `Kasegi_R41`, `.kasegi-r41` and
`kasegi-r41` all match) and leading dots are ignored — the round-40 and round-41
precedent, carried forward. `J5_FAMILY_GLOB` overrides the shape (colon-separated globs).

### Defect (b) — the outside-configured-root escape

`.ufo/waves/round-41/wave2/MutScratchTiming.md` recorded that the r41 I6 limb "scanned
only the configured root, so an outside-root object is not observed" — the probe left
`/tmp/kasegi_r41_outside_probe` and I6 stayed `strays=0,read=ok,scanned=0 closed=1`.

The limb audits a **second root**: the *parent* of the configured scratch root is scanned
for family-shaped entries, and each entry that is neither the configured root nor at or
under it is one outside stray. That is the MutScratchTiming shape.

Per the seat spec, this outside limb **must not read host-global state**, so it never
scans the parent of the live host root. The suite materializes a fixture under `--work`
(`j5_fixture_init`, default `$WORK/j5-fixture/scratch`) and the limb audits *that*
fixture's parent. The outside limb therefore operates on a materialized, deterministic
tree by construction.

### The unit rule

A family-shaped **directory** is a *container*; its **direct children** are the seat-level
entries, and each child that is not on this run's own path is one stray — this is the
"seat-named stray (anything not matching this run's own `--work` dir)" rule. A
family-shaped container with **no** children is itself one stray (a seat that merely
emptied its scratch still left the entry). A family-shaped **symlink** is one stray unless
it resolves to `WORK` or inside `WORK`: a symlink resolving to a `WORK` *ancestor* stays
red, which is the round-40 wave-2 **F5** escape. A family-shaped **regular file** is one
stray (round-40 wave-2 **m10**). A family-shaped child of a container is graded by the
recursive traversal, so nothing is counted twice. When the configured root itself carries
the family shape it is a container too, so its seat-level children are still enumerated.

Own-path tolerance: `WORK` itself, everything inside `WORK`, and `WORK`'s real-dir
ancestors are never strays. The tolerance is *path containment*, not a "clean chain"
heuristic — the round-41 chain rule was the source of its own false reds.

## 3. Evidence (transcript `ExecJ5Scan.transcript.txt`)

### 3.1 Graded selftest — 16/16, `selftest cases=16 failures=0`, `selftest verdict=pass`

| case | expect | payload |
|---|---|---|
| clean-green | green | `strays=0,outside=0,read=ok,scanned=0,scope=on` |
| sibling-round-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| foreign-seat-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| two-planted-red | red | `strays=2,outside=0,read=ok,scanned=2,scope=on` |
| outside-root-red | red | `strays=0,outside=1,read=ok,scanned=1,scope=on` |
| own-work-green | green | `strays=0,outside=0,read=ok,scanned=1,scope=on` |
| own-work-contents-green | green | `strays=0,outside=0,read=ok,scanned=2,scope=on` |
| family-symlink-red | red | `strays=1,outside=0,read=ok,scanned=2,scope=on` |
| dot-prefixed-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| case-separator-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| nested-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| empty-container-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| family-file-red | red | `strays=1,outside=0,read=ok,scanned=1,scope=on` |
| family-shaped-root-red | red | `strays=1,outside=0,read=ok,scanned=0,scope=on` |
| missing-root-red | red | `strays=0,outside=0,read=fail,scanned=0,scope=on` |
| missing-work-red | red | `strays=0,outside=0,read=fail,scanned=0,scope=on` |

### 3.2 Replay of the committed defeat artifacts — `replay defeats=2 failures=0`, `replay verdict=pass`

The limb carries its own replay probe (`--replay-defeats`) that re-executes the two
committed round-40/round-41 defeat artifacts against the **current** limb bytes and
requires rejection:

* **D-A — sibling-round-prefix defeat** (a leftover `kasegi-r40` container; the r39/r40
  limbs matched only one literal round, so the input was green for them).
  → `replay defeat=D-A sibling-round-prefix rejected=1 verdict=pass payload=strays=1,outside=0,read=ok,scanned=1,scope=on`
* **D-B — outside-configured-root defeat** (a leftover `kasegi-r41` container that is a
  SIBLING of the configured root — the MutScratchTiming shape,
  `.ufo/waves/round-41/wave2/MutScratchTiming.md`; the r41 I6 limb looked only inside the
  configured root, so the input was accepted).
  → `replay defeat=D-B outside-configured-root rejected=1 verdict=pass payload=strays=0,outside=1,read=ok,scanned=1,scope=on`
* Control (same tree, clean) → `replay control=clean accepted=1 verdict=pass payload=strays=0,outside=0,read=ok,scanned=0,scope=on`

### 3.3 The three required planted-stray scenarios (transcript §3)

| scenario | output | exit |
|---|---|---|
| green when clean | `strays=0,outside=0,read=ok,scanned=0,scope=on` | 0 |
| planted `kasegi-r41/SeatX` | `strays=1,outside=0,read=ok,scanned=1,scope=on` + `stray: kasegi-r41/SeatX` | 1 |
| planted `kasegi-r42/OtherSeat` | `strays=1,outside=0,read=ok,scanned=1,scope=on` + `stray: kasegi-r42/OtherSeat` | 1 |
| planted `kasegi-r40/SeatX` (sibling round prefix) | `strays=1,outside=0,read=ok,scanned=1,scope=on` + `stray: kasegi-r40/SeatX` | 1 |
| one outside-configured-root stray | `strays=0,outside=1,read=ok,scanned=1,scope=on` + `outside-stray: kasegi-r42` | 1 |

### 3.4 Fail-closed probes (transcript §4) — all `read=fail`, exit 1

unreadable entry inside the root (`strays=1,outside=0,read=fail,scanned=1`); unreadable
root (`read=fail`); missing root (`read=fail`); missing work dir (`read=fail`). A `find`
error (any non-empty stderr) sets `read=fail` — never a vacuous green.

### 3.5 Mutation probe — four weakened copies of the limb bytes, each killed (transcript §5)

Each mutant is a **copy** of the limb in scratch; the lane file was never mutated.

| mutant | weakening | result |
|---|---|---|
| M1 | family narrowed back to the r41 literal `kasegi-r41` | `replay defeats=2 failures=1`, `replay verdict=fail` — D-A survives |
| M2 | outside limb disabled | `replay defeats=2 failures=1`, `replay verdict=fail` — D-B survives |
| M3 | seat-level children ignored (container counted instead) | `replay defeats=2 failures=1`, `replay verdict=fail` — D-A survives |
| M4 | fail-open on a missing work dir | `selftest cases=16 failures=1`, `selftest verdict=fail` — the `missing-work-red` case goes green |

The two mutants that target one defect each still kill the *other* defect's case only
where the weakening touches it; every mutant is detected by at least one graded case.

## 4. How the L1 wires this into `corpus/instruments/r42-closure.sh`

The limb is sourceable and executes nothing on source. Suggested integration, mirroring the
r41 suite's `--scratch-root`/`--work` contract:

```bash
# in r42-closure.sh, after the export is materialized:
bash "$EXPORT/corpus/instruments/j5-scan.sh" --root "$SCRATCH_ROOT" --work "$WORK" \
     --outside-root "$WORK/j5-fixture/scratch"
```

or, if the suite prefers to source the limb:

```bash
source "$EXPORT/corpus/instruments/j5-scan.sh"
check_j5 --root "$SCRATCH_ROOT" --work "$WORK" --outside-root "$WORK/j5-fixture/scratch"
```

which prints exactly one line:

```
J5 payload=strays=<n>,outside=<n>,read=<ok|fail>,scanned=<n>,scope=<on|off> closed=<0|1>
```

and exits 0 only when `read=ok and strays=0 and outside=0`. That is the J5 payload the
r42 receipt line `J5 payload=... closed=0|1` needs. The suite should call
`j5_fixture_init "$WORK/j5-fixture"` (or `mkdir -p "$WORK/j5-fixture/scratch"`) before the
call so the outside limb has a real, suite-owned tree to audit.

**One wiring note for the L1 (a real risk, flagged not hidden):** the outside limb audits
the *parent* of the outside root. If the suite passes `--outside-root "$WORK/j5-fixture/
scratch"`, the audited parent is `$WORK/j5-fixture`, which the suite owns — good. If the
suite instead passes the *live* scratch root as the outside root, the audited parent is
the host-level scratch directory, which is host-global state and outside this seat's
write scope; the suite should not do that. The limb itself never hardcodes a host path:
with no `--outside-root` it defaults to `$WORK/j5-fixture/scratch`, which is suite-owned.

**Live-root state is never read by this seat.** The transcript reads no host scratch root;
every fixture lives under `/fast/scratch/hyaku/kasegi-r42/ExecJ5Scan/`. The limb, as
delivered, has no default for `--root` either — a suite that passes no root gets
`read=fail`, never a vacuous green.

## 5. Relationship to J13 (overlap flagged by `SimplifierSuite`)

J5 (this seat) and J13 (`ExecJ12J13`) both concern the scratch area. The split is clean
and non-overlapping in *rule*:

* **J5** = scratch **hygiene**: leftover seat directories and foreign round containers
  under the configured root, plus the outside-configured-root case. Its unit is the
  seat-level child of a family container.
* **J13** = scratch **quiescence**: no `kasegi-r4[0-9]*` entry other than this run's own
  `--work`, inside the suite's own scratch, bound to the exported ref by name.

They share the family shape and the scratch root, but they answer different questions and
their payloads differ (`strays=`/`outside=` versus J13's own counters). Merging them
would weaken J5's outside-root coverage and J13's quiescence binding; the overlap is
deliberate and complementary. No simplification is proposed.

## 6. Host hygiene

* Disk guard was checked before and after the work:
  `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
  `/tmp 5% 121.9G`, `/var/tmp 36% 576.0G`, `/fast/scratch/hyaku 29% 571.2G` (green; no
  heavy pass was run while the guard was not green).
* Scratch dir `/fast/scratch/hyaku/kasegi-r42/ExecJ5Scan/` was created with `mkdir -p` and
  bound as `TMPDIR` for every run; all fixtures, mutants and probe scripts live there.
  The scratch dir is removed before this seat yields.
* No network fetch was performed by this seat, so no HTTP status/bytes/UTC fetch time to
  record.
* No tool was installed or upgraded by this seat (the task needed none beyond the
  pre-installed bash 5.3.20, find 0.8.0, realpath 0.8.0), so there is no
  tool/version/channel entry to record.
* The delivered limb contains **no hardcoded host path**: `grep -nE "/fast/scratch|
  /home/vgpnk" ExecJ5Scan.sh` outside comment lines returns nothing. Every root is an
  argument or an environment-supplied value.
* No mutating git/jj command was run anywhere; no `pacman` transaction was attempted.

## 7. Risks and blockers

* **Blocker: none.** The item's deliverable is complete and every named acceptance
  criterion is exercised by a real run.
* **Risk (integration, owned by the L1):** the outside limb's audited scope is the parent
  of the outside root. The suite must pass a suite-owned outside root (§4) or the limb
  will audit a host-level directory. The limb's default is already suite-owned.
* **Risk (integration, owned by the L1):** the family shape `kasegi-r4[0-9]*` covers the
  r4x decade. If the lane's scratch convention later moves to a different decade, the
  suite must set `J5_FAMILY_GLOB`; the limb does not guess a broader shape on its own,
  because a broader shape would also match other lanes' `*-rNN` containers and turn the
  check red on unrelated host state.
* **Risk (semantics, recorded):** the outside limb counts family-shaped **entries** in
  the scope (the shape the round-41 defect describes), while the in-root limb counts
  family-shaped **containers' seat-level children**. The asymmetry is intentional: the
  in-root rule is the lane's seat-hygiene rule (a leftover seat directory), the outside
  rule is the defect's own shape (a foreign container beside the configured root). Both
  rules are stated in the limb's header so the suite's grader can read the same contract.

## 8. Traceability

| item requirement | where satisfied |
|---|---|
| scan enumerates `kasegi-r4[0-9]*`-shaped dirs under the suite's own scratch-root argument | `J5_FAMILY_GLOB` default (§2 defect (a)); `--root` is mandatory, no host default |
| never a hardcoded host path | no host path appears in the limb; `--root`/`--outside-root` have no host defaults; transcript reads no host root |
| a seat-named stray (anything not matching this run's own `--work` dir) is detected | container/child unit rule (§2); transcript §3 `kasegi-r41/SeatX` → `strays=1` |
| an outside-configured-root stray is detected by scanning the parent of the given scratch root | `j5_scan_scope` audits `dirname(outside-root)` (§2 defect (b)); transcript §3 `outside=1` |
| the check must not read host-global state — it operates on a materialized tree | outside limb audits a suite-owned fixture under `--work`; default `$WORK/j5-fixture/scratch` |
| the limb scans two roots: the declared live root arg for leftovers (`strays`) and a fixture root the selftest populates | `j5_scan_root` → `strays`; `j5_scan_scope` → `outside`; `j5_fixture_init` |
| transcript: green when clean | §3.3 row 1, exit 0 |
| transcript: rejected over planted `kasegi-r41/SeatX` | §3.3 row 2, exit 1 |
| transcript: rejected over planted `kasegi-r42/OtherSeat` | §3.3 row 3, exit 1 |
| transcript: rejected over one outside-configured-root stray | §3.3 row 5, exit 1 |
| every repaired check carries a REPLAY limb that re-executes its committed defeat artifact against the current suite bytes and requires rejection | `--replay-defeats` (§3.2), M1–M4 mutation probe (§3.5) |
