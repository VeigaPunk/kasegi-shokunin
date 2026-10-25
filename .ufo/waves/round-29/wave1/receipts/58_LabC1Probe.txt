# LabC1Probe — bounded C1 probe (round-29 wave 1)

Seat: `LabC1Probe` (executor, leaf). UTC: 2026-10-25T18:18–18:20Z.
Probe object: **the FIXED bytes** of `corpus/instruments/anchorcheck.py`
(round-29 C1 implementation as present in the working tree when probed).

**Measured instrument digest:** `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`
(sha256 of the probed copy; the live lane file had the identical digest at
18:19Z — `sha256sum corpus/instruments/anchorcheck.py` → same value).
Probe ran read-only against copies in `/tmp/labc1probe/scratch/`; nothing in
the lane repo was edited by this seat except this report.

No tool was installed or upgraded (stdlib python3 + pre-existing git only;
operator 2026-10-19 rule — nothing needed). This item is deterministic command
execution; it does not depend on an answering model, so no model route is
recorded (bound 8).

---

## Method

Driver `driver.sh` (scratch copy; kept under `/tmp/labc1probe/`) performed,
for each probed bytes snapshot:

1. **Clean run ×2** — `python3 <copy> --selftest`, stdout/stderr captured,
   exits recorded, byte-compared.
2. **Git-free run ×2** — canonical frozen-counter form:
   `T=$(mktemp -d) && ln -s "$(command -v python3)" "$T/python3" && cd <lane-root>
   && env -i PATH=$T $T/python3 <copy> --selftest`, exits recorded,
   byte-compared.
3. **Hostile ambient-env run** — same selftest with
   `GIT_WORK_TREE=<hostile-worktree>`, `GIT_OBJECT_DIRECTORY=<hostile-object-store>`,
   `PYTHONPATH=<hostile-dir>` exported. The hostile dir contains a
   `sitecustomize.py` witness (standard interpreter-startup hook) that appends
   one line per interpreter start — `pid`, `argv0`, and the values of the three
   ambient variables as that interpreter saw them — to a log. The hostile
   object store is a real `git init` repo's copied `.git/objects` (so IF
   `GIT_OBJECT_DIRECTORY` leaked into a child `git show`, objects would be
   findable there). The hostile worktree holds a real `pinned.md`.

---

## Findings

### (1) Pin-broken case, git absent on the FIXED bytes → skip line + exit 0: CONFIRMED

Git-free run stdout (both repeats, byte-identical):

```
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
```

- `nogit_run1.exit=0`, `nogit_run2.exit=0` (frozen counter `nogit_exit=0`).
- The skip prints exactly once; the case is still recorded as executed, so the
  limb-coverage assertion stays `limbs=9 covered=9` and the run exits 0. No
  traceback. Implementation: `_selftest()` uses
  `shutil.which('git', path=env.get('PATH'))`; when absent it prints
  `SKIP pin-broken (git not found)`, increments the skip counter, records the
  case as executed, and continues (`anchorcheck.py:328-334`).
- Baseline contrast (do-nothing control, committed): at base `7a6591c1` the
  git-free run exits 1 with a `FileNotFoundError: 'git'` traceback
  (`.ufo/waves/round-29/c1-controls/before.txt`). The fix removes that crash.

### (2) Env sanitization completeness → GIT_* scrubbed; PYTHONPATH inherited (measured)

Hostile-run witness log (`hostile_log_lines=13` = 1 parent + 12 child
interpreters):

```
sitecustomize pid=… argv0=fixed-anchorcheck.py GIT_WORK_TREE='…/hostile/worktree' GIT_OBJECT_DIRECTORY='…/hostile/objects' PYTHONPATH='…/hostile'   ← parent (ambient)
sitecustomize pid=… argv0=fixed-anchorcheck.py GIT_WORK_TREE=None GIT_OBJECT_DIRECTORY=None PYTHONPATH='…/hostile'   ← ×12 children
```

- **`GIT_WORK_TREE` / `GIT_OBJECT_DIRECTORY`: fully scrubbed from all 12
  child interpreters** (`None` in every child witness) — the
  `not k.startswith('GIT_')` filter (`anchorcheck.py:323`) plus the same
  scrubbed env for the `git init` subprocess holds (M28-13 lineage).
- **`PYTHONPATH` is NOT scrubbed**: all 12 child interpreters inherited it and
  executed arbitrary code from the hostile directory (the `sitecustomize.py`
  witness ran in every child). The current env construction is
  `os.environ.items()` minus `GIT_*`, so any ambient `PYTHONPATH` is passed to
  every per-case child interpreter.
- **Behavioral impact observed: none.** The hostile run's stdout is
  byte-identical to the clean run (`hostile_vs_clean_stdout=identical`), exit
  0, `selftest cases=12 failures=0`, `limbs=9 covered=9`. The witness payload
  is passive; no case's verdict counts or exit differed.
- Consequence to record: a hostile `PYTHONPATH` cannot change any selftest
  verdict in this construction, but it does inject import-time code into every
  child interpreter — a hostile payload shadowing a stdlib module used by
  `anchorcheck.py` would execute in each child. This is an env-sanitization
  gap (not a frozen-C1-predicate violation: the predicate and kill rule only
  require the git-free clean skip, exit 0, cases=12, failures=0,
  limbs=9 covered=9). Flagged for the gate: **scrub `PYTHONPATH` (and any
  non-allowlisted var) in the case env alongside `GIT_*`** for full
  hermeticity.

### (3) Repeat runs byte-identical: CONFIRMED

| pair | stdout | stderr |
|---|---|---|
| clean_run1 vs clean_run2 | identical | identical |
| nogit_run1 vs nogit_run2 | identical | — |
| hostile_run vs clean_run1 | identical | — |

All exits 0. Output is deterministic (no temp paths leak into success output;
failure path prints are order-deterministic).

---

## A note on what was measured when

The probed bytes are the working-tree implementation at 18:18–18:19Z (lane
HEAD `46e07f6` + uncommitted `anchorcheck.py` edit by `ExecImplC1`; the wave is
in flight). The digest `68e1bdc6…` is pinned above; if the file changes before
the integration commit, the canonical C1 re-runs (`ExecCanonC1`,
`ExecAssembleReceipts`) re-hash at the committed digest — this receipt then
documents the identical bytes under the earlier digest. No PRE-STATE number is
compared against any after column; all numbers above are AFTER values on the
fixed bytes.

## Verification commands (all reproducible)

```sh
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/anchorcheck.py --selftest          # cases=12 failures=0; limbs=9 covered=9; exit 0
T=$(mktemp -d) && ln -s "$(command -v python3)" "$T/python3" && cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && env -i PATH=$T $T/python3 corpus/instruments/anchorcheck.py --selftest; echo nogit_exit=$?   # SKIP line; exit 0
```
