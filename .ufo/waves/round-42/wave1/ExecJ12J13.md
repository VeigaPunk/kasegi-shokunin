# ExecJ12J13 — round-42 closure-suite limbs J12 and J13

Seat: `ExecJ12J13` (executor, leaf). Item: build the J12 and J13 limbs of the round-42
closure suite `corpus/instruments/r42-closure.sh` — J12 (depth:density no-harm guard) and J13
(quiescence). Axes: **depth:verifiability** (primary), **coverage**.

**Verdict: PASS.** 40/40 graded assertions across 17 scenarios: both greens over the HEAD export
(J12 `deleted=0,density=1,base-density=1,missing=0,diff-read=ok` exit 0; J13
`clone=ok,ref=ok,uncommitted=0,drift=0,untracked=0,strays=0,leftovers=0,read=ok,scope=own` exit 0),
and 17 planted-failure scenarios each red with the expected payload value and exit 1.

No lane file, fleet file, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`,
`corpus/`, `templates/`, `scripts/` or `.ufo/state/` was written. No mutating git/jj command was
run anywhere. No subagent was spawned (leaf seat). The lane's `.git` directory is byte-identical
before and after the whole run (digest `d64631cf285f689e887ae0862ddabcaf1f885ee51aa51e7bcd119bb232a64767`).

---

## 1. Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-42/wave1/ExecJ12J13.sh` | 500 | `80299366e91b4219c71d78e0a27b414966f48cce2f4570cf6ff9602405d50b09` |
| `.ufo/waves/round-42/wave1/ExecJ12J13.transcript.txt` | 114 | `28a95ee7a0a41e4a4bf1fe0df5fffd1ec700f0a6a3fcd3099de37acc4057ed74` |

`ExecJ12J13.sh` contains only landable limb bytes: the header contract, the two sourceable entry
points and their helpers. It is a **sourceable** file — sourcing it defines the functions and
executes nothing (verified: sourcing produces empty stdout and no side effects). It carries no
validation tables, no notes and no headings that are not part of the landed text. The transcript
carries the raw evidence.

### 1.1 API the suite calls

```bash
check_j12 TREE REF   # -> "deleted=<n>,renamed=<n>,density=<0|1>,base-density=<0|1>,
                      #     missing=<0|1>,diff-read=<ok|fail>"   ; exit 0 green / 1 red
check_j13 TREE REF   # -> "clone=<ok|fail>,ref=<ok|fail>,uncommitted=<n>,drift=<n>,
                      #     untracked=<n>,strays=<n>,leftovers=<n>,read=<ok|fail>,
                      #     scope=<own|host-global>"             ; exit 0 green / 1 red
```

Both are pure functions of `(TREE, REF)` plus the suite's globals `LANE`, `BASE_REF`, `WORK`,
`SCRATCH_ROOT`. Per-seat overrides are honoured: `J12_LANE`/`J12_BASE`/`J12_TREE`/`J12_REF` and
`J13_LANE`/`J13_WORK`/`J13_SCRATCH_ROOT`/`J13_TREE`/`J13_REF`. Helpers are prefixed `j12j13_`/`j13_`
except the two entry points, so the suite can source this file beside its own helpers.

Integration check — the limb sourced exactly as the suite will source it, with only the suite's
globals set, over the HEAD export:

```
$ bash verify/suite-sim.sh
J12 payload=deleted=0,renamed=0,density=1,base-density=1,missing=0,diff-read=ok closed=1
J13 payload=clone=ok,ref=ok,uncommitted=0,drift=0,untracked=0,strays=0,leftovers=0,read=ok,scope=own closed=1
closed=2/2 exit=0
$ bash -c ". .../ExecJ12J13.sh"      # sourcing alone
source output=[]
```

---

## 2. What J12 asserts (and why it is not vacuous)

The frozen C1 predicate names J12 as "no tracked deletions in corpus paths and
`corpus/instruments/density.py` byte-identical to base (depth:density no-harm guard)". Erratum 1
item **E5** confirms the scope: corpus-path deletions and density.py byte-identity only — the
F-TABLE repair legitimately deletes lines from `SKILL.md`, which is outside `corpus/` and out of
J12's scope, so the retired r41 `skdel==0` clause is **not** ported.

- **deleted** — `git --no-optional-locks -C <lane> diff --name-status --no-renames
  --diff-filter=D <base> <ref> -- corpus/`. The pathspec is `corpus/`, so a deletion outside
  `corpus/` never counts. `--no-renames` is deliberate: a corpus path renamed away is *gone*, and
  with rename detection on such a path would be reported as `R` and slip past a `D`-only filter.
  Scenario 8 plants exactly that rename and it reds (`deleted=1`).
- **density** — sha256 of `TREE/corpus/instruments/density.py` against the sha256 of the **base
  blob** `base:corpus/instruments/density.py`, both re-derived at run time (never a hard-coded
  expectation on the tree side). The base blob's own digest is then checked against the pinned
  round-42 digest `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`
  (`J12_PINNED_DENSITY`), so a wrong base is a red rather than a pass — scenario 13 plants a
  zero base and gets `base-density=0,diff-read=fail`.
- **missing** — `TREE/corpus/instruments/density.py` absent ⇒ `missing=1` (scenario 15).
- **diff-read** — a failed git call yields `diff-read=fail` and exit 1. There is no fail-open path.

Redundancy note for the L1: `deleted` and `renamed` are separate counters but only `deleted`
gates. `renamed` is diagnostic (the number of rename rows git reports for `corpus/` with rename
detection on). `deleted` already subsumes it.

---

## 3. What J13 asserts

Erratum 1 item **E4** is the governing scope note: "J13's quiescence scan is rooted at the run's
`--scratch-root` argument … any leftover seat dir under that prefix (or under the parent family
pattern `kasegi-r4[0-9]*`) is a red stray and must be cleaned before the receipt run — that
cleanup IS the check's job, not a bypass." Erratum 2 item **E8** confirms J12/J13 have no
committed defeat artifact to replay, so their graded selftest mutants are the required negative
evidence.

### 3.1 Quiescence of the exported tree (bound to the exported ref by name)

The measurement is made in a clone of the lane that is **bound to the exported ref by name**:

1. `git -c gc.auto=0 -c maintenance.auto=false clone --quiet --shared --no-checkout <lane> <work>/j13-ref-clone`
   — `--shared` keeps it at 112 KB (no object copy) and `--no-checkout` leaves the lane's objects
   untouched. The clone's toplevel is asserted to equal the clone path before it is used.
2. `git -C <clone> cat-file -e "$ref^{commit}"` — the exported ref must resolve in the clone.
   A mistyped ref is a distinct red (`ref=fail`), never a vacuous tally (scenario 10).
3. `git -C <clone> update-ref --no-deref HEAD "$ref"` then `git -C <clone> read-tree "$ref"` —
   the clone's HEAD and index become the exported ref's tree, and the exported tree is then used as
   the clone's work tree. Every reported change is therefore a change that is **not in the commit**.
4. Three independent measurements of the same property:
   - **uncommitted** — `git status --porcelain --untracked-files=all` line count. This is the
     literal "no uncommitted changes in a clone of the exported ref" reading.
   - **drift** — `git diff --name-status` line count (modified / deleted / type-changed paths).
   - **untracked** — `git ls-files --others` line count, counted **without** the standard excludes,
     so an ignored extra file counts too.

Three separate counters rather than one, so a partial failure cannot hide behind another. The
clone is removed before the function returns, so J13 leaves no residue in the scratch root.

Attack classes proven rejected (each is a graded assertion in the transcript):

| planted failure | payload | verdict |
|---|---|---|
| modified file in the exported tree | `uncommitted=1,drift=1` | red |
| **stat-cache attack**: one byte changed, size and mtime restored | `uncommitted=1,drift=1` | red |
| extra untracked file in the exported tree | `uncommitted=1,untracked=1` | red |
| tracked file missing from the exported tree | `uncommitted=1,drift=1` | red |
| the exported tree is a different commit's tree | `uncommitted=1,drift=1` | red |

The stat-cache case matters: `git diff` consults the index's stat cache, so a naive
size-and-mtime-preserving edit could be missed. The measurement re-derives content, so it is caught
(`drift=1`).

### 3.2 Quiescence of the scratch root (erratum E4)

The scan is rooted at the run's `--scratch-root` argument and is never host-global.

- **strays** — entries whose name matches the family `kasegi-r4[0-9]*`, matched
  case-insensitively and separator-insensitively after normalization (leading dots stripped, every
  separator run folded to a single `-`), so `kasegi-r42`, `kasegi-r42-leftover`, `kasegi_r42` and
  `.Kasegi-R42.` all match while `kasegi-r4` does not.
- **leftovers** — *every* other entry in the scratch root that is not this run's own `--work`,
  which is what makes a leftover **seat dir** (a non-family name like `ExecJ5Scan`) a red stray as
  E4 requires. Scenario 3 plants exactly such a dir and gets `leftovers=1`.
- The `--work` subtree is pruned from the traversal, so this run's own artifacts — including the
  J13 clone's `.git` files — can never be counted.
- Tolerance: the `--work` dir, everything inside it, and a **clean-chain** ancestor of it (each
  level holds exactly the next component and nothing else). A family-named **symlink** resolving to
  an ancestor of `--work` is never tolerated — the round-40 wave-2 F5 escape — and is a stray
  (scenario 9).
- The scan resolves each entry with `realpath -m`, not `cd`. `cd` fails on a plain regular file
  and would have counted the clone's own `.git` files as strays; this was a real defect found and
  fixed during development (see §5).

### 3.3 Scope guards (fail closed)

- **scope=host-global** — the caller's scratch root equals the fleet scratch root
  (`/fast/scratch/hyaku`). That is host-global state, which the claim forbids for J13, so it is
  red. Scenario 11 plants it (with `J13_FLEET_ROOT` redirected at the probe's own tree, so the
  case never walks the real fleet root).
- **--work outside the scanned scratch root** — the scan could then not distinguish this run's
  artifacts from a leftover, so the check fails closed (`read=fail`). Scenario 12 plants it.
- A missing/unreadable lane, an unresolvable ref, a failed clone or a failed scan all red.

---

## 4. Lane-safety evidence

- The only git operations against the lane are **reads**: `diff`, `cat-file blob`, `rev-parse`,
  `archive`, and `clone --shared --no-checkout` (which reads the lane's object store and writes
  only into the scratch). The lane's `.git` directory is byte-identical before and after
  (`d64631cf285f689e887ae0862ddabcaf1f885ee51aa51e7bcd119bb232a64767`).
- The clone is created under the run's own `--work` dir, never inside the lane, and is deleted
  again before the function returns.
- `git status --porcelain` in the lane shows **no tracked modifications** after the whole run;
  `git diff --name-status --diff-filter=D <base> HEAD -- corpus/` is empty (0 rows).
- Disk guard was green before the work (`disk-guard.sh status` exit 0) and no heavy pass was run
  while it was not.

---

## 5. Defects found and fixed during development (all in my own limb, none in the lane)

These are recorded because each was a real, silent false-green risk, and the fixes are the reason
the current verdicts hold.

1. **The scan resolved entries with `cd`.** `cd` fails on a plain regular file, so the J13 clone's
   own `.git` files were counted as strays (`strays=26` on a clean scratch). Fixed by resolving
   with `realpath -m`, which handles regular files, symlinks-to-files and dangling symlinks alike,
   plus pruning the `--work` subtree.
2. **`J13_LANE` was ignored.** `check_j13` read the lane through the J12 accessor, so a J13-specific
   lane override was silently dropped. Fixed: `j12j13_lane [OVERRIDE_VAR]` takes the override
   variable name, and `check_j13` passes `J13_LANE`.
3. **The default lane derivation assumed a fixed depth** (`<file>/../..`), which resolves to the
   wrong directory when the limb sits in a wave directory rather than `corpus/instruments/`. Fixed:
   the default now walks up to the nearest enclosing git work tree.
4. **The F5 symlink escape was not distinguished.** A family symlink resolving to an ancestor of
   `--work` was tolerated whenever the chain below it happened to be clean. Fixed: a symlink
   resolving to an ancestor is never tolerated (scenario 9).
5. **The probe's own host-global case walked the real `/fast/scratch/hyaku`** (over a million
   entries), which was slow and contrary to the "never host-global" rule. Fixed by redirecting
   `J13_FLEET_ROOT` at the probe's own tree so the case is hermetic.

One defect was in my **test**, not the limb: the planted missing-file case removed
`SKORECARD.md` (a typo) instead of `SCORECARD.md`, so the tree was never actually mutated and the
case correctly reported green. The typo was fixed and the case now reds as designed. This is worth
flagging to the L1 because it is the same shape of error the round-42 kill rule targets: a
"failure" fixture that does not actually plant the failure.

---

## 6. Integration notes for the L1 (suite author)

- Source `ExecJ12J13.sh` and call `check_j12 "$EXPORT" "$REF"` / `check_j13 "$EXPORT" "$REF"`.
  Both print one payload line and return 0 green / 1 red.
- The suite must set `BASE_REF=5053a7f46de35784cff4b56756906e9014a38276` (or `J12_BASE`) and
  `SCRATCH_ROOT` to the run's own scratch root. `WORK` must lie **inside** `SCRATCH_ROOT`, else
  J13 fails closed by design.
- At receipt time the scratch root must be free of leftover seat dirs and of `kasegi-r4[0-9]*`
  entries other than this run's own `--work` — E4 states that cleanup is the check's job, not a
  bypass. The suite's own `--work` subtree is pruned, so the suite's export/mut/neg-* directories
  are not counted.
- The J12/J13 selftest cases should plant the 17 failures enumerated in the transcript's
  Section 2 and assert both the payload value and the exit status (E8: these checks have no
  committed defeat artifact, so their graded mutants are the required negative evidence).
- Suggested payload needles for the graded selftest: J12 `deleted=1`, `density=0`, `missing=1`,
  `base-density=0`; J13 `uncommitted=1`, `drift=1`, `untracked=1`, `strays=1`, `leftovers=1`,
  `ref=fail`, `scope=host-global`, `read=fail`.
- Do not point `SCRATCH_ROOT` at `/fast/scratch/hyaku`: J13 reports `scope=host-global` and reds,
  because the claim requires the quiescence scan to be evaluated inside the suite's own scratch
  root, never host-global state.

---

## 7. Scope and boundaries

- Only two files were written in the lane: the deliverable `ExecJ12J13.sh` and the deliverable
  `ExecJ12J13.transcript.txt`, both under `.ufo/waves/round-42/wave1/`. This receipt is the third
  and last file written.
- No other lane file, fleet file, sibling-lane file or source tree was written.
- No mutating git/jj command was run anywhere (`add`/`commit`/`push`/`checkout`/`reset`/`stash`,
  or any `jj` mutating subcommand). The fixture repos used for the J12 deletion/rename scenarios
  were built with `git init` inside the seat's own scratch dir and their toplevel was asserted
  before every commit, per the host guard.
- Scratch dir `/fast/scratch/hyaku/kasegi-r42/ExecJ12J13/` is removed before this receipt is
  yielded; `TMPDIR` was bound to it for every command.
- Tooling: no package was installed. The limb uses only the host's existing `git` 2.56.0 and
  coreutils (`realpath`, `find`, `sha256sum`, `tar`).

### Files changed

| path | kind | lines | sha256 |
|---|---|---|---|
| `.ufo/waves/round-42/wave1/ExecJ12J13.sh` | deliverable (new) | 500 | `80299366e91b4219c71d78e0a27b414966f48cce2f4570cf6ff9602405d50b09` |
| `.ufo/waves/round-42/wave1/ExecJ12J13.transcript.txt` | deliverable (new) | 114 | `28a95ee7a0a41e4a4bf1fe0df5fffd1ec700f0a6a3fcd3099de37acc4057ed74` |
| `.ufo/waves/round-42/wave1/ExecJ12J13.md` | receipt (this file) | — | — |

---

## 8. Residual risks

- **The J13 scratch scan is a live measurement.** It is red whenever the suite's scratch root holds
  anything beyond this run's `--work`. That is the specified behaviour (E4), but it makes the
  check sensitive to the L1's cleanup discipline at receipt time. If the L1 runs the suite with a
  shared round container rather than a per-run scratch root, J13 will red until that container is
  cleaned. This is intended, not a defect, but the L1 should know it before the receipt run.
- **`renamed` in the J12 payload does not gate.** It is diagnostic; `deleted` (computed with
  `--no-renames`) is the gate. If the L1 prefers `renamed` to gate as well, that is a one-line
  change, but it would double-count the same defect.
- **The J13 clone depends on the lane's object store** through `--shared` (alternates). If the
  lane were garbage-collected between the clone and the measurement, the clone's object lookup
  could fail and the check would red closed (`ref=fail` / `read=fail`) rather than false-green.
  Within a single suite run this window is negligible.
- The lane HEAD advanced twice while this seat worked (`27e18d2` claims-erratum-1, `8be06a9`
  claims-erratum-2, then `514ff62`). The transcript records the ref it was measured against
  (`514ff62d61ee9bc717a20a02a22c65ec0c5124ed`); the limb itself is ref-agnostic and reads the ref
  it is given, so it does not need re-measuring against a later HEAD — but the graded selftest
  should be run against the final Y ref when the suite lands.
