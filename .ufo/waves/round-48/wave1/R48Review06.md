# R48Review06 — Report-local selftest draft over persisted fixtures (exits + findings, dual-mode)

- **Seat:** R48Review06 (reviewer, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`; frozen at commit `3546f70`, claims-sha256 `b8022cdf…`)
- **Probe class:** report-local selftest script draft invoking the frozen CLI on persisted `.ufo/waves/round-48/controls/fixtures.json`, checking expected exits AND expected finding IDs — plus coverage-gap probes on scratch trees
- **Date:** 2026-10-30 (measured 2026-10-30T14:52–15:06Z)

## Verdict

The draft selftest passes **34/34 runs (17 persisted cases × 2 CLI modes), 0 failures, exit 0**, stable across two independent invocations. Both claim endpoints reproduce under the claim's literal `counter_cmd` form (`--root` only): before-tree `canonical=0 finding=SF-PREAMBLE exit=1` (= `expect_before`), production tree `canonical=1 finding=SF-CLEAN exit=0` (= `expect_after`). The frozen checker's four finding paths **not** exercised by the persisted fixture set (`SF-POINTER`, `SF-VERIFIER`, `SF-MISSING-BOX`, `SF-UNREADABLE`) were each demonstrated on isolated scratch trees and behave per the frozen source. One persisted-fixture naming caveat is recorded in §Coverage (the `missing-file` case is the empty-file case and never reaches pointer logic). No defeat of the frozen counter observed; no production, fleet, sibling, or git/jj state touched.

## Assignment scope executed

Create a **report-local selftest script draft** invoking the CLI on persisted `fixtures.json` and checking expected exits and findings; no production edit. The draft (`draft-selftest-shonen-form.py`) was written to this seat's scratch, exercised twice against the real persisted bytes, and is reproduced verbatim in §Annex A — it exists durably only inside this report ("report-local"), not as a repo file. It improves on the existing production selftest in two verifiable ways, without editing it:

1. **Dual mode.** Every case runs in *both* CLI modes: `--file` (isolated candidate, the production selftest's form) and `--root` with the fixture bytes written as the tree's own `SHONEN.md` — the claim C1 `counter_cmd` form exactly (`python3 {tool}/corpus/instruments/shonen-form.py --root {tree}`). Mode-independence of the verdict is thus measured, not assumed.
2. **Checker-byte pin.** In addition to the fixtures.json digest pin, the draft pins the frozen checker sha256 and refuses to run (`exit=2`, could-not-evaluate class) if either digest drifts — so a stale or amended counter cannot silently grade itself.

## Pins observed at measurement time

| Surface | Value | Status |
|---|---|---|
| `controls/fixtures.json` sha256 | `10d2aa79e231d1ac7bb02e9c53df4c7f50d78d07931c42bfa0384a82c0cbb288` | matches draft pin and production selftest pin |
| `corpus/instruments/shonen-form.py` sha256 | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | matches draft pin |
| production `SHONEN.md` sha256 | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` | current tree = canonical candidate bytes |
| before-tree `SHONEN.md` sha256 | `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` | equals the kill-rule archive hash (`controls/shonen-before.txt`, byte-identical to the `actual-r47-drift` fixture) |

No installs this seat (no tool/version/channel/reason entries).

## Observed commands and output (verbatim)

**RUN 1 — draft selftest, full receipt (work dir `…/R48Review06/work`):**

```text
$ python3 /fast/scratch/hyaku/kasegi-r48/R48Review06/draft-selftest-shonen-form.py \
    --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --work /fast/scratch/hyaku/kasegi-r48/R48Review06/work
case=canonical mode=file ok=1 rc=0 want='shonen-form canonical=1 finding=SF-CLEAN exit=0' observed='shonen-form canonical=1 finding=SF-CLEAN exit=0'
case=canonical mode=root ok=1 rc=0 want='shonen-form canonical=1 finding=SF-CLEAN exit=0' observed='shonen-form canonical=1 finding=SF-CLEAN exit=0'
case=actual-r47-drift mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-PREAMBLE exit=1' observed='shonen-form canonical=0 finding=SF-PREAMBLE exit=1'
case=actual-r47-drift mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-PREAMBLE exit=1' observed='shonen-form canonical=0 finding=SF-PREAMBLE exit=1'
case=missing-file mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-NEWLINE exit=1' observed='shonen-form canonical=0 finding=SF-NEWLINE exit=1'
case=missing-file mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-NEWLINE exit=1' observed='shonen-form canonical=0 finding=SF-NEWLINE exit=1'
case=fenced mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-PREAMBLE exit=1' observed='shonen-form canonical=0 finding=SF-PREAMBLE exit=1'
case=fenced mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-PREAMBLE exit=1' observed='shonen-form canonical=0 finding=SF-PREAMBLE exit=1'
case=commented mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-PREAMBLE exit=1' observed='shonen-form canonical=0 finding=SF-PREAMBLE exit=1'
case=commented mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-PREAMBLE exit=1' observed='shonen-form canonical=0 finding=SF-PREAMBLE exit=1'
case=duplicate mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-TRAILING exit=1' observed='shonen-form canonical=0 finding=SF-TRAILING exit=1'
case=duplicate mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-TRAILING exit=1' observed='shonen-form canonical=0 finding=SF-TRAILING exit=1'
case=extra-prose mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-TRAILING exit=1' observed='shonen-form canonical=0 finding=SF-TRAILING exit=1'
case=extra-prose mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-TRAILING exit=1' observed='shonen-form canonical=0 finding=SF-TRAILING exit=1'
case=crlf mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-NEWLINE exit=1' observed='shonen-form canonical=0 finding=SF-NEWLINE exit=1'
case=crlf mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-NEWLINE exit=1' observed='shonen-form canonical=0 finding=SF-NEWLINE exit=1'
case=no-newline mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-NEWLINE exit=1' observed='shonen-form canonical=0 finding=SF-NEWLINE exit=1'
case=no-newline mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-NEWLINE exit=1' observed='shonen-form canonical=0 finding=SF-NEWLINE exit=1'
case=wrong-label-0 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=wrong-label-0 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=missing-evidence-0 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=missing-evidence-0 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=wrong-label-1 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=wrong-label-1 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=missing-evidence-1 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=missing-evidence-1 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=wrong-label-2 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=wrong-label-2 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=missing-evidence-2 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=missing-evidence-2 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=wrong-label-3 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=wrong-label-3 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-BOX exit=1' observed='shonen-form canonical=0 finding=SF-BOX exit=1'
case=missing-evidence-3 mode=file ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
case=missing-evidence-3 mode=root ok=1 rc=1 want='shonen-form canonical=0 finding=SF-EVIDENCE exit=1' observed='shonen-form canonical=0 finding=SF-EVIDENCE exit=1'
selftest cases=17 modes=2 runs=34 failures=0
EXIT=0
```

**RUN 2 — stability re-run (fresh work dir `…/R48Review06/work2`):** identical summary line `selftest cases=17 modes=2 runs=34 failures=0`, `EXIT=0`. Byte-stable verdicts across runs.

**RUN 3 — claim C1 `counter_cmd` literal form, before-tree reconstruction** (base `903d47e13058982460f0d90c1c2b9c7c02680646` exports of `SHONEN.md LOG.md SKILL.md PROVINCE.md corpus/lessons/round-47-verifier-spotcheck.md` under scratch, read-only `git show`):

```text
$ sha256sum before-tree/SHONEN.md
596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05
$ python3 …/corpus/instruments/shonen-form.py --root …/R48Review06/before-tree
shonen-form canonical=0 finding=SF-PREAMBLE exit=1
BEFORE_EXIT=1
```

**RUN 4 — claim C1 `counter_cmd` literal form, production tree (HEAD `3d7e042`):**

```text
$ python3 …/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
shonen-form canonical=1 finding=SF-CLEAN exit=0
AFTER_EXIT=0
```

**RUN 5 — coverage-gap probes** (isolated scratch trees, claim counter_cmd form `--root <tree>`; each tree holds its own `SHONEN.md` + an isolated `LOG.md`):

```text
pointer-missing-target: rc=1  shonen-form canonical=0 finding=SF-POINTER exit=1
pointer-dotdot-escape:  rc=1  shonen-form canonical=0 finding=SF-POINTER exit=1
verifier-x-mark:        rc=1  shonen-form canonical=0 finding=SF-VERIFIER exit=1
missing-box-truncated:  rc=1  shonen-form canonical=0 finding=SF-MISSING-BOX exit=1
unchecked-no-evidence:  rc=0  shonen-form canonical=1 finding=SF-CLEAN exit=0
unreadable-utf8:        rc=2  shonen-form canonical=0 finding=SF-UNREADABLE error=UnicodeDecodeError exit=2
```

## Expected vs observed

| Case / run | Expected | Observed | Match |
|---|---|---|---|
| 17 persisted cases × 2 modes (draft selftest) | per-fixture exit + finding map in §Annex A | all `ok=1`, `runs=34 failures=0`, exit 0 | yes |
| Stability re-run | identical summary | identical summary, exit 0 | yes |
| Before tree (base `903d47e`) | `canonical=0 finding=SF-PREAMBLE exit=1` (claim `expect_before`) | `canonical=0 finding=SF-PREAMBLE exit=1` | yes |
| Production tree (HEAD `3d7e042`) | `canonical=1 finding=SF-CLEAN exit=0` (claim `expect_after`) | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| pointer-missing-target | reject, nonclean | `SF-POINTER exit=1` | yes |
| pointer-dotdot-escape | reject, nonclean | `SF-POINTER exit=1` | yes |
| verifier-x-mark | reject (`x` marks not mechanically attestable per claim `mechanical_limits`) | `SF-VERIFIER exit=1` | yes |
| missing-box-truncated | reject | `SF-MISSING-BOX exit=1` | yes |
| unchecked-no-evidence | accept (`[ ]` needs no evidence line) | `SF-CLEAN exit=0` | yes |
| unreadable-utf8 | `exit=2` could-not-evaluate class | `SF-UNREADABLE … exit=2` | yes |

## Coverage analysis of the persisted case set (depth)

The persisted `fixtures.json` carries 17 named cases but exercises **6 of the checker's 10 finding paths**:

| Finding | Persisted cases hitting it |
|---|---|
| `SF-CLEAN` | canonical |
| `SF-PREAMBLE` | actual-r47-drift, fenced, commented (3 — the kill-rule's hidden/commented shapes are here) |
| `SF-NEWLINE` | missing-file, crlf, no-newline (3) |
| `SF-BOX` | wrong-label-0..3 (4) |
| `SF-EVIDENCE` | missing-evidence-0..3 (4) |
| `SF-TRAILING` | duplicate, extra-prose (2 — the kill-rule's duplicate shape is here) |
| `SF-POINTER` | **none** |
| `SF-VERIFIER` | **none** |
| `SF-MISSING-BOX` | **none** |
| `SF-UNREADABLE` | **none** |

Caveats a reviewer must not elide:

1. **`missing-file` is misnamed.** Its persisted text is the *empty string* (0 bytes, no trailing newline), so the newline gate fires first and the case never reaches pointer-existence logic (`SF-POINTER` remains unexercised by the persisted set). This is not a defeat — the fixture still rejects with `exit=1` as recorded — but a reader inferring "missing evidence target covered" from the name would be wrong. RUN 5 supplies the missing observation.
2. **First-failure short-circuit.** `grade()` returns at the first violated gate in fixed order (newline → preamble → per-box label → per-box evidence/pointer → trailing). The 3× `SF-PREAMBLE` and 3× `SF-NEWLINE` cases are distinct inputs converging on one code path each; distinct finding IDs are not distinct coverage. The four uncovered paths were each demonstrated green-for-the-counter in RUN 5, so the coverage gap is closed observationally for this review without amending the frozen fixtures.
3. **`SF-VERIFIER` enforces the claim's `mechanical_limits`.** An `[x]` file with a valid pointer and perfect form still rejects — the author-side checker cannot attest reviewer independence. Observed, not assumed.

## Mechanism notes (read-only, from frozen source `0ab32a2c…`)

- Mode independence: `--file` only redirects the read; `--root` drives both the default read and the evidence-pointer resolution base. Dual-mode agreement (RUN 1) is therefore the meaningful equivalence, and the `--root`-only form (RUN 3/4) is the claim's graded surface.
- Pointer confinement: `resolved.is_relative_to(root.resolve())` plus a `..`-parts and absolute-path ban rejects the dot-dot escape before existence is consulted — RUN 5's `pointer-dotdot-escape` confirms `SF-POINTER` for both failure reasons through one finding ID.
- Kill-rule shapes: hidden (`commented`), fenced (`fenced`), and duplicate (`duplicate`) checklists all reject, matching the claim's kill clause "a tested hidden/commented/duplicate checklist passes the frozen checker" — none passes; archive retention hash `596122c0…` verified byte-identical to the before bytes (RUN 3).

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review06/` created explicitly; the draft script, gap trees, and before-tree lived only there; **removed after this report was written** (all receipts preserved verbatim above).
- No production file, fleet file, sibling file, domain tree, or git/jj index/state touched — the only production-tree operations were read-only checker invocations and `git show`/`git status` reads. `git status --porcelain` after measurement showed only pre-existing orchestrator/sibling state.
- No commit/push, no delegation, no background jobs, no tool installs.
- Counter bytes/predicate treated as frozen: observed behavior reported; nothing amended, no fixture or checker edit proposed.

## Residual limits

- The draft selftest is **report-local** by assignment; if the L1 wants it as a committed instrument, that is an integrator decision outside this seat's write scope.
- RUN 5 gap probes are single-shape demonstrations (one input per uncovered finding), not exhaustive boundary batteries for `SF-POINTER`/`SF-VERIFIER`/`SF-MISSING-BOX`/`SF-UNREADABLE`; sibling mutation seats own deeper per-path batteries.
- The production-tree measurement grades the moving worktree at HEAD `3d7e042` (2026-10-30T11:32:58-0300); a later commit changes the graded surface per the gate standard.
- Form validation only, per the claim: evidence-pointer existence was probed, semantic truth of any evidence and promotion remain independently judged — this review asserts nothing about them.

## Annex A — draft selftest (verbatim, as exercised)

```python
#!/usr/bin/env python3
"""DRAFT selftest (report-local, seat R48Review06, round 48).

Exercises the frozen shonen-form CLI against the persisted case set at
.ufo/waves/round-48/controls/fixtures.json, checking EXPECTED EXITS and EXPECTED
FINDING IDs per case, in BOTH CLI modes:

  mode=file : --root <isolated-tree> --file <candidate>   (isolated candidate file)
  mode=root : fixture bytes written as <tree>/SHONEN.md, CLI run with only --root
              (the claim C1 counter_cmd form: python3 {tool}/corpus/instruments/shonen-form.py --root {tree})

No production edit. Scratch trees only; the live lane tree is never a --root target
of a write, and the checker itself is read-only. Exit 0 iff every case passes in both
modes; exit 2 on snapshot/checker digest mismatch (could-not-evaluate); exit 1 on any
case mismatch.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# --- Pins (observed at draft time, 2026-10-30) --------------------------------
FIXTURES_REL = '.ufo/waves/round-48/controls/fixtures.json'
FIXTURES_SHA256 = '10d2aa79e231d1ac7bb02e9c53df4c7f50d78d07931c42bfa0384a82c0cbb288'
CHECKER_REL = 'corpus/instruments/shonen-form.py'
CHECKER_SHA256 = '0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd'

# --- Expected verdicts: name -> (exit, finding) --------------------------------
EXPECTED = {
    'canonical': (0, 'SF-CLEAN'),
    'actual-r47-drift': (1, 'SF-PREAMBLE'),
    'missing-file': (1, 'SF-NEWLINE'),   # empty text: newline gate fires first
    'fenced': (1, 'SF-PREAMBLE'),
    'commented': (1, 'SF-PREAMBLE'),
    'duplicate': (1, 'SF-TRAILING'),
    'extra-prose': (1, 'SF-TRAILING'),
    'crlf': (1, 'SF-NEWLINE'),
    'no-newline': (1, 'SF-NEWLINE'),
    'wrong-label-0': (1, 'SF-BOX'),
    'missing-evidence-0': (1, 'SF-EVIDENCE'),
    'wrong-label-1': (1, 'SF-BOX'),
    'missing-evidence-1': (1, 'SF-EVIDENCE'),
    'wrong-label-2': (1, 'SF-BOX'),
    'missing-evidence-2': (1, 'SF-EVIDENCE'),
    'wrong-label-3': (1, 'SF-BOX'),
    'missing-evidence-3': (1, 'SF-EVIDENCE'),
}


def run_case(tool, tree, case, mode):
    if mode == 'file':
        candidate = tree / 'candidate.md'
        candidate.write_bytes(case['text'].encode('utf-8'))
        cmd = [sys.executable, str(tool), '--root', str(tree), '--file', str(candidate)]
    else:  # root: fixture IS the tree's SHONEN.md (claim counter_cmd form)
        (tree / 'SHONEN.md').write_bytes(case['text'].encode('utf-8'))
        cmd = [sys.executable, str(tool), '--root', str(tree)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    want_exit, want_finding = EXPECTED[case['name']]
    want = f"shonen-form canonical={int(want_exit == 0)} finding={want_finding} exit={want_exit}"
    ok = (p.returncode == want_exit and p.stdout.strip() == want
          and p.stderr == '' and case['exit'] == want_exit)
    return ok, p, want


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True, help='lane root (read-only)')
    ap.add_argument('--work', type=Path, required=True, help='scratch work dir')
    args = ap.parse_args()

    fixture = args.root / FIXTURES_REL
    tool = args.root / CHECKER_REL
    if hashlib.sha256(fixture.read_bytes()).hexdigest() != FIXTURES_SHA256:
        print('selftest finding=SF-SNAPSHOT-TAMPERED exit=2')
        return 2
    if hashlib.sha256(tool.read_bytes()).hexdigest() != CHECKER_SHA256:
        print('selftest finding=SF-CHECKER-TAMPERED exit=2')
        return 2
    cases = json.loads(fixture.read_text())
    if {c['name'] for c in cases} != set(EXPECTED) or len(cases) != len(EXPECTED):
        print('selftest finding=SF-CASESET failures=1 exit=1')
        return 1

    args.work.mkdir(parents=True, exist_ok=True)
    failures = 0
    ran = 0
    for case in cases:
        for mode in ('file', 'root'):
            tree = Path(tempfile.mkdtemp(prefix=f"sf-{case['name']}-{mode}-", dir=args.work))
            try:
                # Isolated evidence target so pointer resolution is meaningful.
                (tree / 'LOG.md').write_text('isolated evidence fixture\n')
                ok, p, want = run_case(tool, tree, case, mode)
                ran += 1
                failures += not ok
                print(f"case={case['name']} mode={mode} ok={int(ok)} "
                      f"rc={p.returncode} want='{want}' observed='{p.stdout.strip()}'")
            finally:
                shutil.rmtree(tree)
    print(f'selftest cases={len(cases)} modes=2 runs={ran} failures={failures}')
    return int(failures != 0)


if __name__ == '__main__':
    raise SystemExit(main())
```
