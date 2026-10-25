# C1 anchorcheck selftest hermeticity mutation probe

## Detector and subject

Subject copied from `corpus/instruments/anchorcheck.py` at SHA-256 `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` (28,102 bytes; 561 lines) into `/tmp/mutc1hermetic-uhow_8er/pristine.py`. Probe was confined to copies in that `/tmp` directory; the lane source was not edited.

Same bounded detector for pristine, each mutant, and each restored copy: invoke the copied script with `--selftest`, using `env -i`-equivalent environment containing only `PATH=<temporary dir with python3 symlink>`; timeout 30 seconds. Thus `git` is absent from PATH. Detector is red on nonzero exit or traceback; green is exit 0 without traceback. This follows the frozen C1 git-free counter's isolated PATH/environment shape.

## Results

Pristine baseline: exit 0, no traceback. Stdout:

```text
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
```

| Mutant | Smallest mutation | Mutant SHA-256 | Actual output / exit | Verdict |
|---|---|---|---|---|
| M1 | Replaced `env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}` with `env = dict(os.environ)` (re-includes ambient GIT_* variables in case env). | `7d0bae3981f80843ee0b580e1b542b26f298aecce8846eca48022f0a91d1053c` | Exit 0, no traceback; stdout identical to pristine: `SKIP pin-broken (git not found)\nselftest cases=12 failures=0\nlimbs=9 covered=9\n`; stderr empty. | **SURVIVED** — coverage finding. The canonical detector uses `env -i`, so `GIT_DIR` is absent from its outer environment; additionally, git-dependent fixture setup is skipped when git is unavailable. This detector cannot expose this hermeticity regression. |
| M2 | Replaced `git = shutil.which('git', path=env.get('PATH'))` with `git = 'git'`, bypassing the absent-git skip so the subprocess invocation is attempted. | `6b61787dc88e91bcf1d99b5f306f7807c0d028bdca72c35982d0be3c245fabcd` | Exit 1; stdout empty. Stderr traceback ends `FileNotFoundError: [Errno 2] No such file or directory: 'git'`. | **KILLED** |
| M3 | Replaced the absent-git skip's `print('SKIP pin-broken (git not found)')` with `raise RuntimeError('git not found')`. | `f26441a16dc8b799bda804845ab0ad1405451899b676e1b54e575ead544ec553` | Exit 1; stdout empty. Stderr traceback ends `RuntimeError: git not found`. | **KILLED** |

## Restoration evidence

After each mutant run, its scratch file was overwritten with the exact pristine bytes, re-hashed, and the same detector rerun. For M1, M2, and M3, restored SHA-256 was exactly `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`; each restored run exited 0, emitted the pristine three stdout lines above, and had empty stderr/no traceback. Mutant scratch copies were then removed. No tools were installed.
