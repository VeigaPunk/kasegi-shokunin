# CritC1Kill — round 28 wave 1: kill-rule attack on C1 (selftest fixture isolation)

- Seat: CritC1Kill (critic, leaf — no subagents, no background jobs, no production edits)
- Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin (read-only except this receipt)
- Lane base: c9f8b115a098c65356e4b3b6048af45a37ab8395 (claims freeze)
- Claim under attack: C1(c) "anchorcheck.py --selftest runs one isolating fixture per limb"
- Kill rule (claims.json C1): "a selftest fixture is shown non-isolating (a fixture that fails a
  limb other than its own, or a limb with no failing fixture)"
- Recorded UTC: 2026-10-25T17:32:51Z
- Instrument digest at evidence time: `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
  (landed bytes; the same selftest code was present at the first observed landed digest
  `c36292292ec0d85eef348b0c1ef723c6501fb136cab939e0e87c93137edb6a2a` earlier this session.
  The impl landed mid-session; no PRE-STATE label is needed.)

## Verdict

**KILL — the `pin-broken` selftest fixture is non-isolating.** Its verdict is decided not by the
case's own declared state but by ambient git environment inherited from the parent process. A
single env perturbation flips the case from `PIN-BROKEN` to `IN-RANGE(PIN)`; under that
perturbation the pin limb has no failing fixture (kill-rule clause 2). The selftest then fails
(`selftest cases=9 failures=1`, exit 1) despite the instrument being correct — the self-test's
pass/fail is not self-contained.

## 1. The fixture and the leak

`_selftest()` (landed bytes) runs each case as a subprocess with:

```python
env = dict(os.environ)
env.update(KASEGI_LANE_ROOT=root['lane'],
           KASEGI_MIRROR=root['mirror'],
           KASEGI_ORIGIN_ROOT=root['origin'],
           KASEGI_BOUNTIES=root['bounties'])
```

The four KASEGI roots are overridden per case, but **everything else is inherited**, including
`GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`. Case `pin-broken`
(landed bytes) is:

```python
add('pin-broken',
    "<!-- pin: pinned.md deadbeef -->\n"
    "Pinned cite whose blob does not exist: `pinned.md:1`\n",
    want(**{'PIN-BROKEN': 1}), 1, git_dir='lane')
```

`git_show()` runs `git -C <lane> show deadbeef:pinned.md`. If the parent environment has
`GIT_DIR` pointing at any repository that happens to contain a ref literally named `deadbeef`
(a legal short ref) and a `pinned.md` blob, that command succeeds, the verdict becomes
`IN-RANGE(PIN)`, and the fixture's premise (a broken pin) is destroyed.

## 2. Evidence (verbatim)

Baseline (ambient env, no perturbation):

```
$ python3 corpus/instruments/anchorcheck.py --selftest
selftest cases=9 failures=0
$ echo $?
0
```

Perturbation: parent env sets `GIT_DIR=/tmp/c1kill-gitrepo-*/ .git` where that repo has branch
`deadbeef` and `pinned.md` (a plain `git init` + commit + `git branch deadbeef`).

```
$ GIT_DIR=/tmp/c1kill-gitrepo-76wl02nz/.git python3 corpus/instruments/anchorcheck.py --selftest
selftest FAIL pin-broken: PIN-BROKEN: want 1, got 0; IN-RANGE: want 0, got 1; exit: want 1, got 0
  == /tmp/anchorcheck-selftest-p5anllpo/pin-broken/fixture.md: 1 in-range cite instances, 0 bad; 1 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
  OK md:2 pinned.md:1  [one]
selftest cases=9 failures=1
$ echo $?
1
```

Wanted: `PIN-BROKEN=1`, exit 1. Got: `IN-RANGE=1`, exit 0. The case flipped.

## 3. Perturbation matrix (complete, all on landed bytes)

| # | Perturbation | exit | `selftest cases=…` | Flip? |
|---|---|---|---|---|
| 1 | baseline (ambient) | 0 | 9 failures=0 | — |
| 2 | `KASEGI_MIRROR=/tmp/kasegi-c1kill-mirror` | 0 | 9 failures=0 | no |
| 3 | `KASEGI_MIRROR` unset | 0 | 9 failures=0 | no |
| 4 | `KASEGI_BOUNTIES=/tmp/kasegi-c1kill-bounties` | 0 | 9 failures=0 | no |
| 5 | all four `KASEGI_*` overridden | 0 | 9 failures=0 | no |
| 6 | `GIT_DIR` → repo **with** ref `deadbeef` | 1 | 9 failures=1 | **YES (pin-broken)** |
| 7 | `GIT_DIR` → repo **without** ref `deadbeef` | 0 | 9 failures=0 | no |
| 8 | `GIT_CEILING_DIRECTORIES=/tmp` | 0 | 9 failures=0 | no |
| 9 | `GIT_DISCOVERY_ACROSS_FILESYSTEM=1` | 0 | 9 failures=0 | no |
| 10 | `cwd` = a fresh temp dir | 0 | 9 failures=0 | no |
| 11 | `PATH` = empty dir (no `git`) | 1 | no cases line (traceback) | crash (below) |

The item's named perturbations (`KASEGI_MIRROR` set/unset, `KASEGI_BOUNTIES` set) are inert:
the selftest's per-case `env.update` overrides all four roots, so the host's absent bases never
leak in. No strict cross-FAIL-class flip was observed anywhere in the matrix. The isolation
breach is real and specific: the git environment (unowned ambient state) decides the pin limb's
verdict. Under perturbation 6 the `PIN-BROKEN` limb has no failing fixture — exactly the second
clause of the kill rule.

## 4. Secondary finding (robustness, not the kill)

Case 11: if `git` is not on `PATH`, `subprocess.run(['git', …])` raises an unhandled
`FileNotFoundError`; `--selftest` dies in a traceback and prints **no** `selftest cases=…`
line (exit 1). The frozen counter `grep -cE 'selftest cases='` would then read 0. On this host
`git` is present, so the frozen counters are unaffected here; this is a robustness defect in the
landed bytes, not a demonstrated counter miss.

Coverage note (not a kill): the `outside-base` case exercises only the BOUNTIES arm's escape
confinement. The MIRROR and ORIGIN arms' `OUTSIDE-BASE` sub-limbs have no failing fixture; the
same is true of the ORIGIN arm's `BASE-ABSENT`. The claim's "one isolating fixture per limb"
holds at the verdict-class level (all six FAIL_CLASSES have exactly one failing fixture on this
host), but is arm-blind.

## 5. Smallest safe correction

In `_selftest()`, spawn each case subprocess from a sanitized environment: drop `GIT_DIR`,
`GIT_OBJECT_DIRECTORY`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_CEILING_DIRECTORIES`,
`GIT_DISCOVERY_ACROSS_FILESYSTEM`, `GIT_ALTERNATE_OBJECT_DIRECTORIES` from the case env (or
build `env` from a whitelist: `PATH`, `HOME`, plus the four KASEGI overrides). That restores
the fixture's isolation — the pin limb's verdict then depends only on the case's own
`git init`-ed lane. Optionally harden `git_show()`/`git init` against `git` absence with a
bounded, readable failure instead of a traceback.

Re-run command for the L1 after the fix (from the lane root):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && D=$(mktemp -d) && git -C "$D" init -q && printf 'one\ntwo\nthree\n' > "$D/pinned.md" && git -C "$D" add pinned.md && git -C "$D" -c user.name=t -c user.email=t@t commit -qm x && git -C "$D" branch deadbeef && GIT_DIR="$D/.git" python3 corpus/instruments/anchorcheck.py --selftest; echo exit=$?; rm -rf "$D"
```

Post-fix expectation: exit 0 and `selftest cases=9 failures=0` under the same `GIT_DIR`.
Any `selftest FAIL pin-broken` line under this command means the isolation breach remains.

## 6. Evidence integrity

All outputs above were produced in this session on the bytes with digest
`95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
(verified by `sha256sum corpus/instruments/anchorcheck.py` immediately before and after the
runs). No production file was read-modified or written by this seat; no VCS write; no tool
install; no subagent; no background job.
