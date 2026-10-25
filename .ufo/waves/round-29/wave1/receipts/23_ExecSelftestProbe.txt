# ExecSelftestProbe — reproducibility probe on the FIXED anchorcheck.py

Seat: `ExecSelftestProbe` (executor, leaf). Round 29, wave 1 (`kasegi-r29-build`).
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. UTC stamp of measurement: 2026-10-25T18:19:08Z.
Answering model (session route table): `inception/mercury-3` (per workstation profile; no env hint present).

Scope: the frozen C1 predicate's reproducibility half. The probe runs the fixed instrument's
`--selftest` twice as-is and twice with `PATH` stripped of git, asserts byte-identical output
across repeats and exit 0 on all four runs, and records digests. No source edit was made by this
seat (read-only over `corpus/instruments/anchorcheck.py`).

## Subject file

| item | value |
|---|---|
| live digest | `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` |
| line count | 561 |
| git state | `M corpus/instruments/anchorcheck.py` (uncommitted; diff vs HEAD 120 changed, +78/−42) |
| declared by owning seat | `ExecImplC1-2`: same digest; "cases=12 failures=0, limbs=9 covered=9, exit 0; git-free emits required SKIP line" — matches all four live runs below |

Stability check before probing: `sha256sum` twice 2 s apart → identical (no mid-edit race).

## Probe method (exact commands)

Normal variant, per run: `cd <lane> && python3 corpus/instruments/anchorcheck.py --selftest >out 2>err; echo $? >exit`
Git-free variant, per run:
```
T=$(mktemp -d) && ln -s "$(command -v python3)" "$T/python3" &&
cd <lane> && env -i "PATH=$T" "$T/python3" corpus/instruments/anchorcheck.py --selftest >out 2>err; echo $? >exit ; rm -rf "$T"
```
Host: `python3` = `/usr/bin/python3.14` (3.14.8); `git` = `/usr/bin/git` 2.56.0 (present in normal PATH;
absent in the git-free `PATH`). Byte-identity checked with `cmp -s`; exit codes recorded per run.

## Results on the FIXED bytes

### Normal runs (×2) — identical stdout, empty stderr, exit 0 ×2

```
selftest cases=12 failures=0
limbs=9 covered=9
```
stdout sha256 (both runs): `40fa12b8461614d88269f548efd08bf49b8118edd781024bcb5ef8c946dcbe3f`
stderr sha256 (both runs): `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)
exits: `0 0`

### Git-free runs (×2) — identical stdout, empty stderr, exit 0 ×2, no traceback

```
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
```
stdout sha256 (both runs): `516a47f7fe8c45bc49958eb7fd77acb66f7f6fc29f8ee451519163f603ea9a7f`
stderr sha256 (both runs): `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty — no traceback)
exits: `0 0`

### Assertions

| assertion | result |
|---|---|
| normal run 1 exit 0 | PASS |
| normal run 2 exit 0 | PASS |
| git-free run 1 exit 0 | PASS |
| git-free run 2 exit 0 | PASS |
| normal stdout byte-identical across repeats (`cmp -s` = 0) | PASS |
| normal stderr byte-identical across repeats (both empty) | PASS |
| git-free stdout byte-identical across repeats | PASS |
| git-free stderr byte-identical across repeats (both empty) | PASS |
| `selftest cases=12 failures=0` on all four runs | PASS |
| `limbs=9 covered=9` on all four runs | PASS |
| git-free prints `SKIP pin-broken (git not found)` (clean skip, no crash) | PASS |

No temp paths appear in any successful output, so byte-identity held without normalization ("modulo
temp paths" was not needed). The fixed instrument is deterministic: four runs, two environments,
two output fingerprints.

## PRE-STATE contrast (labeled, not an after column — rule 6)

Before the fix landed, the same harness ran against the base bytes (digest `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`,
525 lines — identical at base 7a6591c1, freeze f28ff5d, and HEAD before the edit):

- normal runs ×2: `selftest cases=9 failures=0`, exit 0 both, byte-identical (the pre-fix set of 9
  cases reproduces too);
- git-free runs ×2: `FileNotFoundError: [Errno 2] No such file or directory: 'git'` traceback on
  stderr, exit 1 both, byte-identical tracebacks.

The probe therefore discriminates exactly the two frozen gaps (limb-coverage assertion; git-free
crash) and shows the fix turned both into stable, repeatable success. No PRE-STATE number is
compared against an after column.

## Digests of record

- fixed instrument (live): `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`
- pre-fix instrument (base/freeze/HEAD-before): `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`
- fixed normal selftest stdout: `40fa12b8461614d88269f548efd08bf49b8118edd781024bcb5ef8c946dcbe3f`
- fixed git-free selftest stdout: `516a47f7fe8c45bc49958eb7fd77acb66f7f6fc29f8ee451519163f603ea9a7f`
- both stderrs: empty (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)

## Observations (context, not changes)

1. The round-28 instruments README records the round-28 "landed digest" as `95333e29…` (523
   lines); the measured repo blobs at base/freeze and at round-28 commit 1265fe1 are all
   `23818c12…` (525 lines). That is the M28-12 receipt-digest-drift class, re-observed from
   committed bytes; this seat records live digests only.
2. The git-free clean skip is conditional: the host has `git` 2.56.0 at `/usr/bin/git`, and the
   normal runs exercise PIN-BROKEN with a real temp `git init` (no SKIP line there); the SKIP line
   appears only when `git` is absent from `PATH`.
3. All probe scratch lives under `/tmp/probe-scratch` (outside the lane); the only lane write by
   this seat is this receipt.
