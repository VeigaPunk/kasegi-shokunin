# ExecControlC1 — Round 29 wave 1

Axes: depth:verifiability, coverage. The control bundle is under `c1-controls/`; it contains the frozen baseline receipt, compact counter outputs, and four mutant outputs. Mutant source copies were kept in `/tmp`, not copied into the repository.

## Baseline receipt

Copied `.ufo/waves/round-29/c1-controls/before.txt` byte-for-byte to `c1-controls/before.txt`.

- Source and copy SHA-256: `9d7ff4a1db4bac976704e8bf69398d6fd4d16e7bef3490def5ddbf38e8db4cab`.
- The receipt's baseline instrument digest is `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`.

## Do-nothing control

Extracted the frozen base bytes with `git show 7a6591c1eb8a14f427297980a96fa8bb339f29ee:corpus/instruments/anchorcheck.py > /tmp/base-anchorcheck.py`. SHA-256 matches the frozen value: `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`.

- `base-control-selftest.txt`: `selftest cases=9 failures=0`, `selftest_exit=0`.
- `base-control-grep.txt`: the counter prints cases=9; `grep -cE 'limbs=[0-9]+ covered='` returns `0`.
- `base-control-nogit.txt`: with `env -i PATH=<python3-only-dir>`, it crashes with `FileNotFoundError: [Errno 2] No such file or directory: 'git'`; `nogit_exit=1`.

Thus the unchanged base bytes do not meet the frozen C1 target.

## Fixed instrument identity and normal run

The production instrument, owned and changed by ExecImplC1, was snapshotted read-only to `/tmp/fixed-anchorcheck.py` after its normal selftest passed. Both snapshot and production file SHA-256: `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`.

Observed normal output: `selftest cases=12 failures=0`, `limbs=9 covered=9`, exit 0. The git-free run also passed with the required `SKIP pin-broken (git not found)` and reported `cases=12 failures=0`, `limbs=9 covered=9`, exit 0. This final fixed digest incorporates ExecImplC1's repair: a skipped PIN-BROKEN case is counted in executed limb coverage.

## Mutant results

Each mutated file was derived from the fixed snapshot above, run in `/tmp`, and its output saved in the named receipt:

| Mutant | Mutation | Observed result | Receipt |
|---|---|---|---|
| M1 | Removed `outside-base-mirror` fixture | Selftest red: 11 cases, 1 failure; `missing executed cases outside-base-mirror`; `limbs=9 covered=8`; exit 1. | `c1-controls/mutant-m1.txt` |
| M2 | Removed the `limbs=` output line | Instrument itself reports `cases=12 failures=0`, exit 0; the frozen output assertion fails because no `limbs=9 covered=9` line exists. `frozen_assertion_exit=1` is recorded. | `c1-controls/mutant-m2.txt` |
| M3 | Force `covered=8` while claiming `limbs=9` | Instrument prints `cases=12 failures=0`, `limbs=9 covered=8`, exit 0; frozen output assertion fails (`frozen_assertion_exit=1`). | `c1-controls/mutant-m3.txt` |
| M4 | Replaced GIT_* environment filtering with `dict(os.environ)` only; retained the git-presence guard and all other fixed case logic | With `GIT_OBJECT_DIRECTORY=/dev/null`, mutation fails PIN-BROKEN's `git init` (exit 1), then reports missing executed case and `limbs=9 covered=8`; total selftest exit 1. The fixed snapshot under the same poisoned environment passes `cases=12 failures=0`, `limbs=9 covered=9`, exit 0. | `c1-controls/mutant-m4.txt` |

**Interpretation:** M2 and M3 do not make the Python selftest process exit nonzero by themselves; the frozen counter's required output assertion is what rejects them. Their receipts retain both the actual instrument exit and the assertion exit, rather than claiming otherwise. M4 isolates unsanitized environment forwarding (not git absence): only the environment-filter expression differs, and the same Git poison is green on fixed bytes and red on the mutant.

## Files and retained evidence

- `c1-controls/before.txt`
- `c1-controls/base-control-selftest.txt`
- `c1-controls/base-control-grep.txt`
- `c1-controls/base-control-nogit.txt`
- `c1-controls/mutant-m1.txt` through `mutant-m4.txt`
- This report: `.ufo/waves/round-29/wave1/ExecControlC1.md`

No production instrument or other lane file was edited by this executor. No checks beyond the specified base-control and mutant selftest/counter runs were performed.