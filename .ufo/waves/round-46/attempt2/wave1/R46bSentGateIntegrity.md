# R46bSentGateIntegrity — integrity audit of the round-46 (attempt 2) instruments

Seat: sentinel / integrity audit. Lane: `kasegi-shokunin`.
Scope: `corpus/instruments/r46-f29-gate.py`, `corpus/instruments/r46-mutbat.py`, the planned
selftests (`r46-counters-selftest-c1.py`, `r46-counters-selftest-c2.py`, and the planned
`r46-selftest-f29.py`). Read-only audit; no production file was modified.

Audited bytes at the freeze commit `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` (matches
`freeze.txt`): `r46-f29-gate.py` = `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`,
`r46-mutbat.py` = `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`,
`source-recheck.py` = `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`
(verified with `sha256sum`; all three match the freeze record).

VERDICT: BROKEN

---

## Finding 1 — tree-supplied code execution: the mutation battery executes the graded tree's own selftest, unpinned and un-allow-listed

**Exact thing attacked.** `r46-mutbat.py` grades mutants of the tree's counters by running the
**tree's** selftest as a subprocess:

```
corpus/instruments/r46-mutbat.py:98    st = os.path.join(tree, "corpus/instruments", COUNTER[which][2])
corpus/instruments/r46-mutbat.py:99    cmd = [sys.executable, "-I", st]
corpus/instruments/r46-mutbat.py:106   p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=tree)
```

`tree` is the `--root` argument — the tree under test. The verdict of every mutant is then read
out of that subprocess's own stdout (`r46-mutbat.py:107  m = re.findall(r"failures=(\d+)", p.stdout)`).
There is **no pin, no hash, and no allow-list** on the file that is executed: `grep -n "sha\|hashlib\|pin"
corpus/instruments/r46-mutbat.py` returns only mutant-table text and the `--equivalent` help string.

**The precedent this violates** is in the same lane's other instrument, `r46-c1-gate.py`, which
treats tree-supplied commands as hostile by construction:

```
corpus/instruments/r46-c1-gate.py:82-88   def allowed(cmd): ...  # only the line shapes the lane's 64 rechecks actually use are ever executed
corpus/instruments/r46-c1-gate.py:91-95   def grader_env(): ...  # Minimal environment: no tokens, agent sockets or other host secrets reach a tree-supplied line
corpus/instruments/r46-c1-gate.py:241     cmd = cmd.replace("python3 corpus/instruments/", "python3 " + TOOL_LANE + "/corpus/instruments/")
```

Line 241 is explicit: *"instruments run from the grader's own lane (cwd stays the tree): a tree
cannot swap in its own instrument."* `r46-mutbat.py` has no equivalent rewrite — it runs the
tree's copy.

**Command and output (exploit).** A tree whose `corpus/instruments/r46-counters-selftest-c1.py`
reports `failures=1` for any invocation carrying `--counter` and `failures=0` otherwise:

```
$ cat $S/e5/tree/corpus/instruments/r46-counters-selftest-c1.py
import sys
print("selftest cases=1 failures=%d" % (1 if "--counter" in sys.argv else 0))

$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-mutbat.py \
      --root $S/e5/tree --pure $S/e5/work --work $S/e5/work --counter c1
...
mutant=M14-L6-exit-ignored baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M15-L7-always-true baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M16-min-rows-5 baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M17-min-token-1 baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M18-anchor-dirs-wide baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M19-L2-eq-relaxed baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=1 verdict=caught
mutbat counter=c1 mutants=20 caught=20 equivalent=0 uncaught=0 baseline_failures=0
BATEXIT=0
```

Twenty mutants, `uncaught=0`, `BATEXIT=0` — the exact green the C1 kill rule demands
(`expect_after`: `caught+equivalent=20 uncaught=0 baseline_failures=0`) — with a selftest that
examines nothing about the counter.

**Discriminating control.** The same tree with the selftest inverted (`failures=0` always) is the
opposite verdict, proving the reading is a pure function of the tree's self-report and not of the
mutant:

```
$ python3 .../r46-mutbat.py --root $S/c1/tree --pure $S/c1/work --work $S/c1/work --counter c1 | tail -2
mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=0 verdict=uncaught
mutbat counter=c1 mutants=20 caught=0 equivalent=0 uncaught=20 baseline_failures=0
```

**Impact.** C1's kill rule is `uncaught>0 ⇒ claim fails`. `uncaught` is computed from a number the
graded artifact prints. A tree that self-reports `failures=1` satisfies the kill rule with zero
real coverage, and the battery cannot tell the two apart. The frozen before-value
(`controls/mutbat-before.txt`: `c1 … uncaught=7`, `c2 … uncaught=13`) is *not* structurally
protected against this, because the same tree-supplied file supplies those numbers too.

**Note on the f29 extension.** The wave-1 plan (`build-wave1-spec.py:136`) extends the battery
with `--counter f29`. If that mode routes through the existing `run_selftest` (which resolves
`os.path.join(tree, "corpus/instruments", ...)`), the f29 gate inherits this exact hole; the planned
`r46-selftest-f29.py` is committed into the lane's `corpus/instruments/`, so it *will* be
tree-resident at grading time.

**Smallest remediation.** In `run_selftest`, resolve the selftest from the grader's own lane
(mirroring `r46-c1-gate.py:241`'s `TOOL_LANE` rewrite) rather than from `--root`, and/or pin the
selftest's sha256 against a committed value before executing it, failing closed on mismatch. One
of the two closes the hole; the first is the pattern already used in this lane.

---

## Finding 2 — environment capture: the tree-supplied selftest inherits the grader's whole environment, and the f29 gate's census subprocess is not env-scrubbed

**Exact thing attacked.**

* `r46-mutbat.py:106` — `subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=tree)`
  passes **no `env=`**, so the executed tree-supplied selftest inherits every variable of the
  grader process, with `cwd` inside the tree. Compare `r46-c1-gate.py:243`, which passes
  `env=grader_env()` (`r46-c1-gate.py:91-95`: only `HOME`, `PATH`, `TMPDIR`, plus `LANG=C`).
* `r46-f29-gate.py:337` — `p = subprocess.run(["bash", CENSUS, "validate", "--file", ...], capture_output=True, text=True, timeout=120)`
  likewise passes no `env=`. The census script reads `SHOKUNIN_ROOT` (`scripts/sources-census.sh:88`)
  and `TODAY` (`:90`) from the environment.

**Command and output.** A tree-supplied selftest dumping its own environment:

```
$ cat $S/c2/tree/corpus/instruments/r46-counters-selftest-c1.py
import os, sys
keys = sorted(os.environ)
open("/fast/scratch/hyaku/kasegi-r46/R46bSentGateIntegrity/ENV_DUMP.txt","w").write(
    "\n".join("%s=%s" % (k, os.environ[k]) for k in keys))
print("selftest cases=1 failures=1")

$ SECRET_MARKER_VALUE=x python3 .../r46-mutbat.py --root $S/c2/tree --pure $S/c2/work --work $S/c2/work --counter c1
$ wc -l < $S/ENV_DUMP.txt
268
$ grep -c SECRET_MARKER_VALUE $S/ENV_DUMP.txt
1
$ grep '^HOME=' $S/ENV_DUMP.txt
HOME=/home/vgpnk
```

268 variables, including a marker that existed only in the grader's environment and the user's
`HOME`, reached code chosen by the tree. The same selftest also wrote its dump to an absolute path
**outside `--work`**, which is the write-scope half of this finding (Finding 4).

For the f29 gate's own census leg, a poisoned `SHOKUNIN_ROOT` reaches the census script and moves
H7:

```
$ SHOKUNIN_ROOT=/nonexistent python3 .../r46-f29-gate.py --root $S/pos
gate H7 pass=0 read=census-rc=2 ok-line=0
f29-gate fixed=6/7 exit=1
```

versus the default:

```
$ python3 .../r46-f29-gate.py --root $S/pos
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

**Discriminating control (this direction is closed).** `TODAY` in the environment does **not**
poison the reading — `scripts/sources-census.sh:44` initialises `TODAY=""`, so the env value is
discarded before `:90 TODAY=${TODAY:-$(date -u +%F)}`:

```
$ TODAY=2020-01-01 python3 .../r46-f29-gate.py --root $S/pos | grep -E "^gate H7|fixed"
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

while the explicit flag does move it (proving the leg is date-sensitive at all):

```
$ bash scripts/sources-census.sh validate --today 2020-01-01 --file $S/pos/corpus/SOURCES.md
file	E08	S074 opened=2026-10-29
rc=1
```

**Impact.** The `SHOKUNIN_ROOT` channel only ever moves H7 *red* (fail-closed), so it is not a
green-forging channel; I record it as low severity. The high-severity half is the mutbat's
unscrubbed environment reaching tree-supplied code: host secrets, tokens and `HOME` are exposed
to the artifact being graded, and the c1-gate precedent in the same lane shows the intended
discipline.

**Smallest remediation.** Pass `env=grader_env()` (the existing `r46-c1-gate.py:91-95` helper) to
the mutbat's selftest subprocess and to the f29 gate's census subprocess.

---

## Finding 3 — path escape: the frontier-table limb reads `corpus/README.md` through a symlink out of the tree, while sibling limbs refuse symlinks

**Exact thing attacked.** `r46-f29-gate.py` reads the frontier table with a plain `open()`, which
follows symlinks:

```
corpus/instruments/r46-f29-gate.py:129-133  def txt(root, rel): ... open(p, encoding="utf-8", errors="replace").read()
corpus/instruments/r46-f29-gate.py:139       for ln in live_lines(txt(root, "corpus/README.md") or ""):
corpus/instruments/r46-f29-gate.py:177       raw = [ln for ln in live_lines(txt(root, "corpus/README.md") or "") if re.match(r"^\| F29 \|", ln)]
```

H1 (`r46-f29-gate.py:159-178`) is the limb that decides *"F29 admitted"*, and it takes its bytes
from that path with **no `islink` check**. The gate demonstrably knows the symlink rule — it
enforces it two limbs later:

```
corpus/instruments/r46-f29-gate.py:328  links = [x for x in (os.path.join(root, "corpus"), d) if os.path.islink(x)] + [n for n in everything if os.path.islink(os.path.join(d, n))]      # H6
corpus/instruments/r46-f29-gate.py:335  if os.path.islink(os.path.join(root, "corpus")) or os.path.islink(os.path.join(root, "corpus/SOURCES.md")):                # H7
```

`corpus/README.md` is in neither list.

**Command and output (exploit).** The tree's README moved outside the tree and replaced by a
symlink to it:

```
$ mv $S/esc/corpus/README.md $S/outside_README.md
$ ln -s $S/outside_README.md $S/esc/corpus/README.md
$ python3 .../r46-f29-gate.py --root $S/esc
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

7/7 with the frontier table living outside the tree.

**Discriminating control.** Pointing the same symlink at a table with one row fewer flips H1 red,
which shows the limb genuinely reads through the link (and is not passing on a stale copy):

```
$ grep -v '^| F29 |' $S/pos/corpus/README.md > $S/outside_README_28.md
$ rm $S/e11/corpus/README.md; ln -s $S/outside_README_28.md $S/e11/corpus/README.md
$ python3 .../r46-f29-gate.py --root $S/e11 | grep -E "^gate H1|fixed"
gate H1 pass=0 read=rows=28 admitted=28 dup=0
f29-gate fixed=6/7 exit=1
```

**Second escape in the same class.** The whole capture directory symlinked out of the tree also
reads green, because H3/H4/H5 read `S074.txt` and `manifest.json` through `txt()`/`open()` with no
`islink` check, and the *content* is pinned by sha256 but the *location* is not:

```
$ ln -s $S/e15_outside $S/e15/corpus/source-snapshots/round-46-a2
$ python3 .../r46-f29-gate.py --root $S/e15
...
f29-gate fixed=7/7 exit=0
```

Here the sha256 pins (`r46-f29-gate.py:92-97`, checked at `:261` and `:281`) hold the *bytes* fixed,
so content forgery is impossible — the escape is containment, not content. The stricter layer
catches it only by luck of ordering: symlinking the single file `S074.txt` out makes H4 red,
because `source-recheck.py` refuses a source outside the manifest's directory:

```
$ python3 .../r46-f29-gate.py --root $S/esc2
gate H3 pass=1 read=row-S074=ok
gate H4 pass=0 read=recheck-rc=2 quotes-ok=0 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
f29-gate fixed=6/7 exit=1
```

Note H3 and H5 still read the out-of-tree bytes and pass; only H4's recheck fails.

**Sibling limbs are sound.** `corpus/SOURCES.md` symlinked out is caught by H7
(`gate H7 pass=0 read=census-input-is-a-symlink`, `f29-gate fixed=6/7 exit=1`), and the entry file
symlinked out of `corpus/knowledge/` is caught by H6 (`gate H6 pass=0 read=… symlinks=1`,
`f29-gate fixed=6/7 exit=1`). The census script's `used-by` cell is a second, tree-controlled
existence oracle reaching one level above the tree root
(`scripts/sources-census.sh:501  dir_abs = realpath -- "$(dirname -- "$file_abs")/.."`):

```
$ bash scripts/sources-census.sh validate --file $S/e14d/corpus/SOURCES.md      # used-by = ../deep/DEEP_PROBE (exists)
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bSentGateIntegrity/e14d/corpus/SOURCES.md
rc=0
$ bash scripts/sources-census.sh validate --file $S/e13c/corpus/SOURCES.md      # used-by = ../PROBE_ABSENT.txt (absent)
file	E11	S074 missing used-by ../PROBE_ABSENT.txt
rc=1
```

**Impact.** The limb that certifies *"F29 admitted"* can be satisfied by bytes the tree does not
contain. Because the README content is deliberately unpinned (the row bytes do not exist at
freeze), a tree cannot forge *content* through this channel — but it can relocate it, so the
green "29 rows, 29 admitted, F29 admitted" reading is not a statement about the tree's own bytes.

**Smallest remediation.** Extend the existing symlink policy to the paths the gate reads:
refuse when `corpus/README.md` (and the `round-46-a2` snapshot directory) is a symlink, i.e. add
them to the `islink` test already written at `r46-f29-gate.py:335`.

---

## Finding 4 — write scope: the battery's mutant write follows a tree-supplied symlink and lands outside both the tree and `--work`

**Exact thing attacked.** `r46-mutbat.py` copies the tree's instruments directory into scratch
**preserving symlinks**, then writes the mutant through that copy:

```
corpus/instruments/r46-mutbat.py:119  shutil.copytree(os.path.join(tree, "corpus", "instruments"), dst_inst, symlinks=True)
corpus/instruments/r46-mutbat.py:120  dst_counter = os.path.join(dst_inst, os.path.basename(src_counter))
corpus/instruments/r46-mutbat.py:121  open(dst_counter, "w", encoding="utf-8").write(text.replace(old, new, 1))
```

`symlinks=True` recreates symlinks as symlinks; `open(..., "w")` then **follows** them. The
docstring's contract is `the lane tree is only read` and `Mutant copies live under --work`
(`r46-mutbat.py:14-16`).

**Command and output (exploit).** The tree's `corpus/instruments/r46-c1-gate.py` is a symlink to a
file outside the tree and outside `--work`:

```
$ cp .../corpus/instruments/r46-c1-gate.py $S/e12/VICTIM_OUTSIDE.py
$ ln -s $S/e12/VICTIM_OUTSIDE.py $S/e12/tree/corpus/instruments/r46-c1-gate.py
$ BEFORE=$(sha256sum $S/e12/VICTIM_OUTSIDE.py | cut -d' ' -f1)
$ python3 .../r46-mutbat.py --root $S/e12/tree --pure $S/e12/work --work $S/e12/work --counter c1
$ AFTER=$(sha256sum $S/e12/VICTIM_OUTSIDE.py | cut -d' ' -f1)
victim sha before: 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7
victim sha after : f2d6f5e57c4860b628e36fa29c122be65e8dbe1cedcf1d8a16797e2786dc7920
VICTIM-OVERWRITTEN-OUTSIDE-TREE
$ grep -c "TARGET_GATED = 24" $S/e12/VICTIM_OUTSIDE.py
1
```

The file outside the tree was overwritten with mutant content (`TARGET_GATED = 24` — the M01
mutation). Direct confirmation of the mechanism:

```
$ python3 -  # calling apply_mutant directly
dst_counter      : /fast/scratch/.../work/corpus/instruments/r46-c1-gate.py
islink(dst)      : True
readlink(dst)    : /fast/scratch/.../e4/victim_c1-gate.py
victim changed   : True
mutant in victim : True
```

**Impact.** The write lands wherever the tree's symlink points — outside `--work` and outside the
tree. Any file the grading user can write is reachable, and the content written is
attacker-chosen within the mutant template. Combined with Finding 2 (the tree's selftest also ran
with `cwd=tree` and wrote to an absolute path of its choosing), the battery gives tree-supplied
code an unrestricted write primitive, contradicting its own documented contract.

**Control that passes — the f29 gate is clean here.** The f29 gate's write scope on `--root` is
sound. Full-tree content hash and mtime hash, before and after a run on the same tree:

```
$ BEFORE=$(cd $S/esc3 && find . -type f -printf '%p %s ' -exec sha256sum {} \; | sort | sha256sum)
$ MT=$(cd $S/esc3 && find . -printf '%p %T@\n' | sort | sha256sum)
$ python3 .../r46-f29-gate.py --root $S/esc3 >/dev/null
$ AFTER=$(cd $S/esc3 && find . -type f -printf '%p %s ' -exec sha256sum {} \; | sort | sha256sum)
$ MT2=$(cd $S/esc3 && find . -printf '%p %T@\n' | sort | sha256sum)
content-before: e2a759efb9d56c8b3d8771cadae04a057d6e1eae4a0c770881268efbf3d353a2  -
content-after : e2a759efb9d56c8b3d8771cadae04a057d6e1eae4a0c770881268efbf3d353a2  -
mtime-before  : c148d2e720d16e80a7b4c97fbceb9bd1147eb637244798b0ba7a79b41768a23f  -
mtime-after   : c148d2e720d16e80a7b4c97fbceb9bd1147eb637244798b0ba7a79b41768a23f  -
CONTENT-UNCHANGED
MTIME-UNCHANGED
```

**Smallest remediation.** After `copytree(..., symlinks=True)`, refuse to write through a symlink:
resolve `dst_counter` and assert `os.path.realpath(dst_counter)` is inside `dst_dir` (or copy the
counter's bytes rather than the link). One `realpath` containment assert closes it.

---

## Finding 5 (coverage class, same instruments) — the battery's `equivalent` predicate accepts an empty proof file, weaker than the claim's own kill rule

**Exact thing attacked.** `r46-mutbat.py:169-171`:

```
corpus/instruments/r46-mutbat.py:169   elif mid in eq and os.path.isfile(eq[mid]):
corpus/instruments/r46-mutbat.py:170       equivalent += 1
corpus/instruments/r46-mutbat.py:171       verdict = "equivalent"
```

Only `isfile` is checked — not non-empty, not content.

**Command and output.** With a selftest that reports `failures=0` (so mutants fall through to the
`equivalent` branch) and a **zero-byte** proof file:

```
$ : > $S/e16b/proof_EMPTY.txt
$ python3 .../r46-mutbat.py --root $S/e16b/tree --pure $S/e16b/work --work $S/e16b/work --counter c1 --equivalent $S/e16b/eq.json | grep -E "M01-L1|mutbat counter"
mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=0 verdict=equivalent
mutbat counter=c1 mutants=20 caught=0 equivalent=1 uncaught=19 baseline_failures=0
```

An empty file is accepted as a committed proof.

**Impact.** The C1 kill rule states: *"an equivalent verdict's proof file is missing, empty, or
falsified by a constructed input … kills that equivalence and with it the claim."* The battery's
own predicate is strictly weaker than the rule it feeds: it accepts the empty file that the rule
names as a kill condition, and reports `equivalent=1`. The rule's protection therefore depends on
a reviewer reading each proof by hand rather than on the instrument that produces the number.

**Smallest remediation.** At `r46-mutbat.py:169`, require the proof file to be non-empty
(`os.path.isfile(...) and os.path.getsize(...) > 0`), matching the rule's wording.

---

## What holds (verified, with the controls above)

* The f29 gate executes **no** tree-supplied command. Its only subprocesses are its own
  `source-recheck.py`, resolved from `INSTRUMENTS = os.path.dirname(SELF)` (`:71`, `:263`, `:266`)
  and sha256-pinned at `:264` before execution, and the fleet-root census script at a fixed
  absolute path (`:102`, `:337`). Neither comes from `--root`.
* That pin is a real control, not decoration: with a malicious `source-recheck.py` planted in the
  tree's own `corpus/instruments/` and the gate invoked from that tree, H4 refuses and the planted
  code never runs —
  `gate H4 pass=0 read=source-recheck-not-the-pinned-bytes`, `f29-gate fixed=6/7 exit=1`, and the
  planted `SELFTEST-COMMAND-EXECUTED-MARKER` line never appeared in the output.
* The f29 gate is read-only on `--root` (Finding 4 control): content and mtimes unchanged.
* `TODAY` in the environment does not poison the census leg (Finding 2 control).
* H7's symlink refusal on `corpus/` and `corpus/SOURCES.md` and H6's symlink refusal inside
  `corpus/knowledge/` both work (Finding 3).
* `source-recheck.py` refuses a capture outside its manifest directory (`outside-manifest-directory`),
  which is why a symlinked single `S074.txt` turns H4 red.

## Limitations

* This is a static-plus-dynamic audit of **instrument integrity only**. I did not evaluate whether
  the C2 entry/row content is correct, nor whether the F29 claim itself is true.
* Findings 1, 2 and 4 are graded against the *general* threat model of a hostile `--root` tree.
  In the intended workflow the tree under test is the lane's own final revision, whose selftest
  is also a wave deliverable and is separately reviewed. I make no claim that a hostile tree is
  the actual failure mode of this round; I claim the instruments do not enforce the property their
  own documentation and kill rules assert, and that a reviewer cannot detect the difference from
  the receipts alone.
* Finding 1's exploit used a selftest I authored. Whether the *committed* selftests would
  self-report is a separate question I did not adjudicate; the point is that the battery has no
  mechanism to tell the two apart, and its documented before-value is equally exposed.
* I did not run the full battery against the live lane (the freeze receipts already record it:
  `c1 … uncaught=7`, `c2 … uncaught=13`). All battery runs above used minimal synthetic trees
  under my own scratch.
* The `--equivalent` path in Finding 5 was exercised with a synthetic tree; I did not exercise it
  against the lane's own `--equivalent` map (none is committed at the freeze commit).
* The f29 gate's `--work` argument is parsed but never used, and `tempfile` is imported but never
  called (`:68`, `:349`); the docstring's "scratch under `--work` / TMPDIR" (`:51`) is therefore
  inaccurate. This is dead surface rather than a vulnerability — the gate writes nothing at all —
  and I flag it only so it is not mistaken for a guarantee.
* No production file was modified. No git/jj mutation was performed. Scratch removed on exit.
