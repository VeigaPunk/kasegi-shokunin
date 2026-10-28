VERDICT: BROKEN

# R45MutLimbR5 — C1 mutation test of counter limb R5 (refiled receipt)

Seat: R45MutLimbR5 (leaf, read-only on the counter; builder output limited to this Report).
Subject: `corpus/instruments/r45-routed-defects.py` limb R5, lines 225-242 (sha256 `82004c70…f24f04ee`, unmodified; the counter was run as a CLI only, never edited).
Base: `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` (pure export at `/fast/scratch/hyaku/kasegi-r45/L1/pure`, copied to scratch, never edited).

Counter lines the mutants target (verbatim from the file):
- L230 `if re.search(r"^(usage:|.*error:)", t, re.M | re.I):` → `usage-or-error-line-present`
- L232 `if not re.search(r"^selftest cases=20 failures=0\s*$", t, re.M):`
- L234 `if not re.search(r"(^|\s)exit=0\s*$", t, re.M):`
- L236 `if not re.search(r"--root \S+ --selftest --work \S+", t):`
- L238-241 original `final-attempt3.txt` compared byte-for-byte with the base copy.

## Survivors (defect present, counter accepts) — 3 of 8

Each mutant re-creates the failed bare `--selftest` call that lesson §6 item 5 (`corpus/lessons/round-44-verifier-spotcheck.md` L83) and the counter docstring (`r45-routed-defects.py` L31-34) say must be absent. All three are accepted with the satisfied verdict.

1. **M3-usage-indented** — edit: insert before line 3 of the refiled receipt the line `  usage: r44-routed-defects.py [-h] --root ROOT [--baseline BASELINE]` (two leading spaces).
   - command: `recipe.py` (appendix), output:
     `SURVIVOR mutant=M3-usage-indented rejected=0 read=refiled=ok original=unchanged`
   - why: L230 anchors `usage:` at column 0 (`^usage:`); `.*error:` needs `error:` contiguous.

2. **M4-bare-call-exit2-no-error-token** — edit: insert before the `selftest cases=20 failures=0` line the three lines `$ python3 corpus/instruments/r44-routed-defects.py --selftest`, `r44-routed-defects: refused, --root is required`, `exit=2`.
   - output: `SURVIVOR mutant=M4-bare-call-exit2-no-error-token rejected=0 read=refiled=ok original=unchanged`
   - why: no line in L230-237 rejects a nonzero `exit=` value or a bare `--selftest` invocation without `--work`; L234 only requires that some line ends `exit=0`, which the satisfied `exit=0` already supplies.

3. **M5-argparse-error-parenthetical** — edit: insert before line 3 `r44-routed-defects.py: error (exit 2): the following arguments are required: --root`.
   - output: `SURVIVOR mutant=M5-argparse-error-parenthetical rejected=0 read=refiled=ok original=unchanged`
   - why: L230 matches the literal `error:`; `error (exit 2):` does not contain it.

Exact printed diffs for the survivors (from the run):
```
SURVIVOR mutant=M3-usage-indented rejected=0 read=refiled=ok original=unchanged
  | @@ -2,0 +3 @@
  | +  usage: r44-routed-defects.py [-h] --root ROOT [--baseline BASELINE]
SURVIVOR mutant=M4-bare-call-exit2-no-error-token rejected=0 read=refiled=ok original=unchanged
  | @@ -4,0 +5,3 @@
  | +$ python3 corpus/instruments/r44-routed-defects.py --selftest
  | +r44-routed-defects: refused, --root is required
  | +exit=2
SURVIVOR mutant=M5-argparse-error-parenthetical rejected=0 read=refiled=ok original=unchanged
  | @@ -2,0 +3 @@
  | +r44-routed-defects.py: error (exit 2): the following arguments are required: --root
```

## Caught (rejected=1) — 5 of 8

```
mutant=M1-usage-col0 rejected=1          read=usage-or-error-line-present
mutant=M2-argparse-error-col0 rejected=1 read=usage-or-error-line-present
mutant=M6-exit0-line-deleted rejected=1  read=exit0-absent
mutant=M7-invocation-work-stripped rejected=1 read=invocation-absent
mutant=M8-original-receipt-edited rejected=1  read=original-receipt-changed
```

## Controls (discriminate against do-nothing)

```
control=control-satisfied-unmutated rejected=0 read=refiled=ok original=unchanged expect_rejected=0 ok
control=control-do-nothing-base rejected=1 read=refiled-absent expect_rejected=1 ok
```
- Verbatim defect bytes (`final-attempt3.txt` copied in as the refiled receipt; `cmp` identical = yes):
  `limb R5 fixed=0 read=usage-or-error-line-present` — the real defect shape is rejected, so the survivors are proxy gaps, not a counter that accepts everything.
- Live lane tree, read-only run (`PYTHONDONTWRITEBYTECODE=1`, scratch TMPDIR):
  `limb R5 fixed=1 read=refiled=ok original=unchanged`, with
  `routed-defects total=5 fixed=1 unresolved=4 exit=1` (R1-R4 are unresolved in the live tree; not this seat's limb). The untracked draft `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` contains no bare-call block, so the live verdict is not affected by the survivors.

## Interpretation

The R5 limb rejects the canonical argparse shapes (column-0 `usage:` and `error:`), the missing `--work`, the deleted `exit=0`, and an edited original. It accepts a failed bare `--selftest` call whose refusal text or exit status avoids those two literal tokens: an indented usage line (M3), a refusal line with `exit=2` (M4), or an `error (exit 2):` token (M5). The defect the limb exists to catch is therefore only partly enforced. Repair belongs to the counter's owner, not this seat; a stronger predicate would reject any line matching `(?i)usage|error|refused|required` and any `exit=[1-9]` line, or any `r44-routed-defects.py` invocation not followed by `--root … --selftest --work …`. The counter is frozen; no edit was made.

## Limitations

- Eight single-edit mutants plus two controls and one verbatim-defect run. Not exhaustive; the survivors above are existence proofs.
- Code-reading only, not exercised: L232 accepts `selftest cases=20 failures=0` even when the same receipt also contains a failing selftest line; L236 accepts the literal placeholder `--root <tip>` and does not bind the receipt to a real run (no digest or export reference); L234 accepts `exit=0` from any line. No mutant tests these.
- The satisfied tree's refiled receipt is hand-built by this seat to pass the limb, not the lane's draft. The live draft was checked separately (above).
- Each counter run is deterministic and single-shot; no timing or flakiness measured.
- R1-R4 subprocesses ran inside scratch trees only; they do not affect the R5 verdict.

## Reproduction

- Recipe (exact text, sha256 `0a2bfc55…c41fd6`), run as
  `SCRATCH=<dir> PYTHONDONTWRITEBYTECODE=1 TMPDIR=<dir>/tmp python3 recipe.py`
  with `$SCRATCH/base` copied from `/fast/scratch/hyaku/kasegi-r45/L1/pure` and the counter at `corpus/instruments/r45-routed-defects.py` (sha256 `82004c70…f24f04ee`):

```python
#!/usr/bin/env python3
"""R45MutLimbR5 mutation recipe: limb R5 of r45-routed-defects.py (scratch only).

Builds a hand-built tree in which limb R5 is satisfied (base export copy +
hand-built refiled receipt + original receipt from the base), applies one
single edit per mutant to a fresh copy, runs the UNMODIFIED counter CLI on
each tree and prints `mutant=<name> rejected=0|1`.  rejected=1 <=> the counter
printed `limb R5 fixed=0`.  Expected: every mutant is rejected=1; any
rejected=0 is a survivor (the edit reintroduces the defect and the counter
still accepts).
"""
import difflib
import os
import re
import shutil
import subprocess
import sys

SCRATCH = os.environ["SCRATCH"]
PURE = "/fast/scratch/hyaku/kasegi-r45/L1/pure"
SNAP = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45"
COUNTER = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r45-routed-defects.py"
REFILED = ".ufo/waves/round-44/controls/final-attempt3-refiled.txt"
ORIGINAL = ".ufo/waves/round-44/controls/final-attempt3.txt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=os.path.join(SCRATCH, "tmp"))

# Hand-built refiled receipt in which limb R5 is satisfied (checked by the counter).
SAT = [
    "# refile of the selftest invocation of final-attempt3.txt (hand-built probe tree)\n",
    "$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>\n",
    "selftest case=POSITIVE verdict=pass fixed=8 unresolved=0\n",
    "selftest case=FABRICATED-ARTIFACTS verdict=pass detail=unresolved limbs: D1,D2,D3,D5,D8\n",
    "selftest cases=20 failures=0\n",
    "exit=0\n",
]


def ins(at, *new):
    def f(lines):
        return lines[:at] + list(new) + lines[at:]
    return f


def dele(at):
    def f(lines):
        return lines[:at] + lines[at + 1:]
    return f


def repl(at, new):
    def f(lines):
        return lines[:at] + [new] + lines[at + 1:]
    return f


def append_orig(lines):
    return lines + ["# edited\n"]


# (name, target, edit, description). target: "refiled" edits the SAT lines; "original" edits the original receipt.
MUTANTS = [
    ("M1-usage-col0", "refiled", ins(2, "usage: r44-routed-defects.py [-h] --root ROOT [--baseline BASELINE]\n"),
     "insert argparse usage line at column 0 after the invocation line"),
    ("M2-argparse-error-col0", "refiled",
     ins(2, "r44-routed-defects.py: error: the following arguments are required: --root\n"),
     "insert argparse error line at column 0 after the invocation line"),
    ("M3-usage-indented", "refiled",
     ins(2, "  usage: r44-routed-defects.py [-h] --root ROOT [--baseline BASELINE]\n"),
     "insert the usage line indented by two spaces (no ^usage: at column 0)"),
    ("M4-bare-call-exit2-no-error-token", "refiled",
     ins(4, "$ python3 corpus/instruments/r44-routed-defects.py --selftest\n",
         "r44-routed-defects: refused, --root is required\n",
         "exit=2\n"),
     "insert the failed bare --selftest call with a refusal line (no error:/usage: token) and exit=2 before the selftest cases line"),
    ("M5-argparse-error-parenthetical", "refiled",
     ins(2, "r44-routed-defects.py: error (exit 2): the following arguments are required: --root\n"),
     "insert an error line in which the token is error (exit 2): rather than error:"),
    ("M6-exit0-line-deleted", "refiled", dele(5),
     "delete the exit=0 line"),
    ("M7-invocation-work-stripped", "refiled",
     repl(1, "$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest\n"),
     "strip '--work <scratch>' from the invocation line"),
    ("M8-original-receipt-edited", "original", append_orig,
     "append '# edited' to the ORIGINAL final-attempt3.txt inside the root tree"),
]


def make_tree(name, refiled_lines):
    tree = os.path.join(SCRATCH, "trees", name)
    shutil.copytree(BASE, tree, symlinks=True)
    os.makedirs(os.path.join(tree, "corpus/source-snapshots"), exist_ok=True)
    shutil.copytree(SNAP, os.path.join(tree, "corpus/source-snapshots/round-45"), dirs_exist_ok=True)
    if refiled_lines is not None:
        with open(os.path.join(tree, REFILED), "w", encoding="utf-8") as fh:
            fh.write("".join(refiled_lines))
    else:
        assert not os.path.exists(os.path.join(tree, REFILED)), "base export already carries a refiled receipt"
    return tree


def run_counter(tree):
    p = subprocess.run([sys.executable, COUNTER, "--root", tree, "--baseline", BASE],
                       capture_output=True, text=True, env=ENV, timeout=900)
    out = p.stdout + p.stderr
    m = re.search(r"^limb R5 fixed=([01]) read=(.*)$", out, re.M)
    if m is None:
        raise SystemExit(f"no limb R5 line in counter output:\n{out}")
    return int(m.group(1)), m.group(2), out


def diff_lines(a, b, label):
    return [ln.rstrip("\n") for ln in difflib.unified_diff(a, b, fromfile=f"base/{label}",
                                                           tofile=f"mutant/{label}", n=0, lineterm="")][2:]


BASE = os.path.join(SCRATCH, "base")
if not os.path.isdir(BASE):
    shutil.copytree(PURE, BASE, symlinks=True)

results = []

# controls
sat_tree = make_tree("control-satisfied", SAT)
fixed, read, _ = run_counter(sat_tree)
results.append(("control-satisfied-unmutated", 0 if fixed == 1 else 1, read, 0, "no edit"))

nothing_tree = make_tree("control-do-nothing-base", None)
fixed, read, _ = run_counter(nothing_tree)
results.append(("control-do-nothing-base", 0 if fixed == 1 else 1, read, 1, "refiled receipt absent"))

# mutants
rows = []
for name, target, fn, desc in MUTANTS:
    if target == "refiled":
        tree = make_tree(name, SAT)
        path = os.path.join(tree, REFILED)
        before = list(SAT)
        after = fn(list(SAT))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("".join(after))
        label = REFILED
    else:
        tree = make_tree(name, SAT)
        path = os.path.join(tree, ORIGINAL)
        with open(path, encoding="utf-8") as fh:
            before = fh.readlines()
        after = fn(list(before))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("".join(after))
        label = ORIGINAL
    assert before != after, f"{name}: edit was a no-op"
    fixed, read, _ = run_counter(tree)
    rej = 1 if fixed == 0 else 0
    d = diff_lines(before, after, label)
    rows.append((name, rej, read, desc, d))

# Survivors first: mutants that should be rejected but were not.
survivors = [r for r in rows if r[1] == 0]
print(f"survivors={len(survivors)} of mutants={len(rows)}")
for name, rej, read, desc, d in survivors:
    print(f"SURVIVOR mutant={name} rejected={rej} read={read}")
    print(f"  edit: {desc}")
    for ln in d:
        print(f"  | {ln}")
print("--- controls ---")
for name, rej, read, expect, desc in results:
    print(f"control={name} rejected={rej} read={read} expect_rejected={expect} "
          f"{'ok' if rej == expect else 'UNEXPECTED'}")
print("--- mutants ---")
for name, rej, read, desc, d in rows:
    print(f"mutant={name} rejected={rej}")
    print(f"  read={read}")
    print(f"  edit: {desc}")
    for ln in d:
        print(f"  | {ln}")
```

Scratch (`/fast/scratch/hyaku/kasegi-r45/R45MutLimbR5/`) removed on exit; no installs; no git/jj mutation. Post-run lane status (`git -C … status --porcelain -- corpus/instruments .ufo/waves/round-45/wave1`) showed only other seats' untracked `wave1/` directory; `corpus/instruments` clean.

## Scope note for the L1

Nothing committed. The only file written is this Report. No shared production file, MANIFEST.json, .ufo/state, or sibling lane was touched.
