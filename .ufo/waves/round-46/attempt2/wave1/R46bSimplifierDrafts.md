VERDICT: DRAFT-READY

# R46bSimplifierDrafts — dead-weight findings for round 46 (attempt 2), lane kasegi

Seat: R46bSimplifierDrafts (leaf, read-only research lane). **No edits were made to the lane
repo, to the shared counters, to the frozen claims, to any sibling lane, or to any `.ufo`
state.** Every cut below is a findings item with exact lines and the reason the behaviour is
identical; the L1 applies them at integration (or logs them as errata).

## 0. What I read

The attempt-2 drafts appeared while I worked, so I read **both** the frozen instruments and the
drafts:

| instrument | state I read |
|---|---|
| `corpus/instruments/r46-f29-gate.py` (v1, frozen `fe0f56b`, sha256 `a1091e24…`) | committed, 367 lines |
| `corpus/instruments/r46-mutbat.py` (v1, frozen `fe0f56b`, sha256 `f7a7cdfa…`) | committed, 184 lines |
| `corpus/instruments/r46-counters-selftest-c1.py` | committed (byte-identical to base `04af9bc9`), 675 lines |
| `corpus/instruments/r46-counters-selftest-c2.py` | committed (byte-identical to base `04af9bc9`), 619 lines |
| `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py` | draft, sha256 `23b528a40e1d982820d360aea3cd12166a8b6ac07226e7567fd5abaa16f4435d`, 906 lines (it was `86b74f99…`, 876 lines when I first read it — the draft is still moving) |
| `.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py` | draft, sha256 `37a723c0952af8523f17e79e949e2e3670783dc126dc1f35047d653b9c73814a` |
| `.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-c2-gate.py` | draft (counter amendment C2-E7) |
| `.ufo/waves/round-46/attempt2/controls/f29-fixture.py`, `f29-defects.py` | the L1's tree builders (used read-only as a test bed) |

The attempt-1 counters `r46-c1-gate.py` / `r46-c2-gate.py` are READ-ONLY for every seat and out
of my scope; I read them only to compare helper behaviour (O-1).

The F29 draft was still being edited while I read it (861 → 876 → 906 lines mid-session); the line
numbers below are those of the sha256 quoted above (`23b528a4…`). The L1 should re-anchor them
against the revision it integrates.

## 1. Test bed, controls, and how each claim was checked

Scratch (removed on exit): `$HYAKU_SCRATCH/kasegi-r46/R46bSimplifierDrafts`
(= `/fast/scratch/hyaku/…`), `TMPDIR` passed explicitly; the frozen `pure2` export was **copied**,
never edited.

Trees built from frozen commits with
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive <rev> corpus | tar -x -C <scratch>`:

* `base`   = `04af9bc92229232ea5cce8b32bfe59dd969eb26d` (frozen base)
* `freeze` = `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` (freeze commit: counters + mutbat + f29-gate)
* `tree-positive`, `tree-junk`, `tree-fabricated` = the three modes of the L1's
  `controls/f29-fixture.py` (positive = the tree the gate must read 7/7 on)
* `def-*` = the 17 per-limb defect trees of `controls/f29-defects.py` (duprow, fencedf29, vjunk,
  thinsection, badnames, row9cells, thinscope, kindcase, manws, fewquotes, dupquote, widespan,
  longquote, fewspans, nestedmd, entrymutant, symlink)

**Do-nothing control.** The unmodified frozen gate on `base` reproduces the L1's frozen receipt
byte for byte:

```
$ python3 $S/freeze/corpus/instruments/r46-f29-gate.py --root $S/base > f29-orig-base.txt
$ diff -u f29-orig-base.txt …/controls/f29-gate-at-base.txt
IDENTICAL to frozen control receipt
```

**Power control.** The same comparison has teeth: one semantic change in a copy of the gate
(`b - a <= 11` → `b - a <= 110`, `r46-f29-gate.py:300`) changes the reading on `def-widespan`:

```
orig : gate H5 pass=0 read=spans=8 located=7 failed=1 uncited=0 cores=5/5
power: gate H5 pass=1 read=spans=8 located=8 failed=0 uncited=0 cores=5/5
```

**Static probes** (AST, no runtime, read-only): `deadnames.py` reports names that are bound and
never read; `unusedimports.py` reports imports that are never read. Both were run over all four
committed instruments and all three drafts.

## 2. Cut candidates (behaviour-identical)

### C-1  `r46-f29-gate.py:68` — dead import `tempfile`

`tempfile` is never used (the gate writes no scratch at all).

```
== …/r46-f29-gate.py
   unused-import: tempfile       line 68
```

(the probe also reports `annotations` for every file — that is `from __future__ import annotations`,
a false positive, not a finding.)

Cut: delete line 68. Behaviour identical: `grep -n "tempfile" r46-f29-gate.py` → only the import.

### C-2  `r46-f29-gate.py:79` + `:247` — duplicate authority for the number 42

`BODY = (1, 42)` (line 78) and `SNAP_LINES = 42` (line 79) are the same number under two names;
`SNAP_LINES` is used exactly once (line 247).

Cut: delete line 79, use `BODY[1]` at line 247. Behaviour identical: both are the literal 42, so
`int(loc.group(2)) <= SNAP_LINES` and `… <= BODY[1]` are the same predicate.

### C-3  `r46-f29-gate.py:154-156` vs `:211-213` — the same section extractor written twice

`sect_words` (154-156) and the nested `sect` inside `h2` (211-213) contain the **identical**
regex `"^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)"` with the same flags (`re.M | re.S`);
`sect` returns `m.group(1) if m else ""`, `sect_words` counts `\w+` runs in `m.group(1)` and
falls back to 0 — the same value the empty string yields (`len(re.findall(r"\w+", "")) == 0`).

Cut: keep one module-level extractor and derive the word count from it:

```python
def sect_text(body: str, heading: str) -> str:
    m = re.search("^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


def sect_words(body: str, heading: str) -> int:
    return len(re.findall(r"\w+", sect_text(body, heading)))
```

and replace the four `sect(SECTIONS[i])` calls (215-218) with `sect_text(body, SECTIONS[i])`.
Behaviour identical — the two regexes were character for character the same.

### C-4  `r46-f29-gate.py:177-179` — an **unreachable branch** (the strongest item)

```python
177:    raw = [ln for ln in live_lines(txt(root, "corpus/README.md") or "") if re.match(r"^\| F29 \|", ln)]
178:    if len(raw) != 1:
179:        return False, "F29-row-not-one-live-line"
```

Why it can never fire (the `frontier()` helper, lines 137-144, is the only other reader of
`corpus/README.md`):

* `frontier()` collects **every** live line matching `^\| F\d+ \|`; every line matching
  `^\| F29 \|` also matches `^\| F\d+ \|` and its first cell is exactly `"F29"` after `strip()`.
  So `len(raw) == len(f29)` for every possible tree.
* The guard above (lines 165-168) requires `len(rows) == 29`, `adm == 29`, `dup == 0`, where
  `dup = len(ids) - len(set(ids))` and `ids` are those first cells. `dup == 0` ⇒ the ids are
  pairwise distinct ⇒ **at most one** row can carry the id `F29`.
* `if not f29 …: return False` (line 170) excludes the empty case.

⇒ at line 177 `len(f29) == 1`, hence `len(raw) == 1`, hence line 178 is never true. The branch is
dead code, and so is the second parse of `corpus/README.md` it performs.

Cut: delete lines 177-179 (or, conservatively, replace them with `if len(f29) != 1:`, equally
unreachable but keeps the guard's shape).

Empirical confirmation over the whole test bed — the token `F29-row-not-one-live-line` occurs
**zero** times in 21 trees:

```
$ for r in base tree-positive tree-junk tree-fabricated def-*; do
    python3 …/r46-f29-gate.py --root $r | grep -c "F29-row-not-one-live-line"; done
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

and the two trees that could plausibly reach it are caught by *earlier* branches:

```
duprow       gate H1 pass=0 read=rows=30 admitted=30 dup=1
fencedf29    gate H1 pass=0 read=rows=28 admitted=28 dup=0
```

**Interaction with the F29 draft (the L1 must decide both together).** The draft's
`clause-a-raw-once` case reaches this clause only by *monkey-patching the counter's own
reader*: `R46bExecSelftestF29.draft/r46-selftest-f29.py:603-647` (`patch_frontier`,
`controlled_rows`) replaces `mod.frontier` with a controlled 29-unique-row list while the README
carries two live F29 rows, and the case at lines 706-711 installs that patch. With the real
reader the two readers of the same file cannot disagree, so the clause is vacuous and the case
manufactures the disagreement artificially. If the L1 applies C-4, the case must go with it —
and `patch_frontier` / `controlled_rows` (≈25 lines) become dead weight with it. If the L1 keeps
the clause as a cheap guard against a future divergence between the two readers, then C-4 is
withdrawn and the draft case stays.

### C-5  `r46-mutbat.py:39-40` — two module-level names that are never read

```python
39: SELF = os.path.realpath(__file__)
40: INSTRUMENTS = os.path.dirname(SELF)
```

`INSTRUMENTS` is never read anywhere (the battery resolves the tree's instruments through
`--root`, not through its own location), and `SELF` is read only by the dead line 40.

```
== …/r46-mutbat.py
   bound-never-read: INSTRUMENTS            stored at line(s) 40
```

Cut: delete lines 39-40. Behaviour identical —
`grep -n "INSTRUMENTS\|SELF" r46-mutbat.py` → only lines 39-40; and the full-flow differential in
§5 runs the entire battery (all 41 mutants, both counters) through the cut copy and gets a
byte-identical transcript.

### C-6  `r46-counters-selftest-c2.py:475-476` — a loop whose result is never used

```python
475:        for i, (sct, floor) in enumerate(zip(SECTIONS, SECT_FLOORS)):
476:            nm = ["scope", "overlap", "limits", "falsifiable"][i]
```

`nm` and `floor` are bound and never read; the loop body has no other statement.

```
== …/r46-counters-selftest-c2.py
   bound-never-read: floor                  stored at line(s) 475
   bound-never-read: nm                     stored at line(s) 476
```

Cut: delete lines 475-476. Behaviour identical: the loop only rebinds two locals that nothing
reads (it is the residue of a loop that used to name the four sections; the names it built are
already in `SECTIONS` / `SECT_FLOORS`).

**Still open in the attempt-2 draft:** the same dead loop is present in
`R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py` at lines **478-479** (the draft adds
three lines above it). The cut must be applied to the draft, not only to the committed file.

### C-7  `r46-counters-selftest-c1.py:278-279` — a duplicated fixture read that re-implements an existing helper

```python
278: def m_still_gated_edited(t):
279:     set_recheck(t, "evidence-dir.md", rd(t, "corpus/knowledge/evidence-dir.md").split("\n")[next(i for i, ln in enumerate(rd(t, "corpus/knowledge/evidence-dir.md").split("\n")) if ln.startswith("recheck:"))] + " # edited")
```

The same file is read twice and the "index of the first `recheck:` line" is recomputed, although
`_recheck_idx(t, name)` (lines 351-353) already returns exactly that `(lines, index)` pair.

Cut:

```python
def m_still_gated_edited(t):
    ls, i = _recheck_idx(t, "evidence-dir.md")
    set_recheck(t, "evidence-dir.md", ls[i] + " # edited")
```

Behaviour identical: `_recheck_idx` returns the same `split("\n")` list and the same
`next(i for i, ln in enumerate(ls) if ln.startswith("recheck:"))` index that line 279 recomputes;
both reads of the original happen before any write, so they see the same bytes.

### C-8  `r46-counters-selftest-c1.py:620` — a bound name that is never read

```python
620:    limbs, reads, fixed, rc, stdout = run_counter(counter, tip, base, os.path.join(scratch, "w-tip"))
```

`stdout` is never read afterwards (the two sibling lines already bind `_`).

```
== …/r46-counters-selftest-c1.py
   bound-never-read: stdout                 stored at line(s) 620
```

Cut: bind `_` instead of `stdout` (line 621 already does). Behaviour identical.

### C-9  `R46bExecSelftestF29.draft/r46-selftest-f29.py:65` — dead constant in the F29 draft

```python
65: ENTRY_NAME = "github-repository-security-advisories.md"
```

The draft addresses the entry by path (`ENTRY_REL`, line 58); `ENTRY_NAME` is never read.

```
== …/R46bExecSelftestF29.draft/r46-selftest-f29.py
   bound-never-read: ENTRY_NAME             stored at line(s) 65
```

Cut: delete line 65. Behaviour identical (no reference anywhere in the file).

### C-10  `R46bExecSelftestF29.draft/r46-selftest-f29.py:249` — dead binding in a fixture builder

```python
249:        prose, tail = rest.split("\n\n| id |", 1)
```

`prose` is bound and never read (the rewrite only uses `tail`).

```
== …/R46bExecSelftestF29.draft/r46-selftest-f29.py
   bound-never-read: prose                  stored at line(s) 249
```

Cut: `_, tail = rest.split("\n\n| id |", 1)`. Behaviour identical (a tuple unpack).

### C-11  `r46-f29-gate.py:349` + docstring lines 51/54 — an accepted-but-inert `--work` flag

```python
349:    ap.add_argument("--work", default=None)
```

`a.work` is never read (and there is no `tempfile` use either — see C-1), while the docstring
advertises it twice:

```
51:    READ-ONLY on --root; scratch under --work / TMPDIR; never runs git; stdlib only.
54:    python3 corpus/instruments/r46-f29-gate.py --root TREE [--work DIR]
```

This is docstring drift from code: the gate creates no scratch and honours neither `--work` nor
`TMPDIR`.

Two cuts at different risk levels — the L1 should pick:

* **C-11a (zero risk, docstring only):** rewrite lines 51 and 54 to state that the gate is
  read-only and takes no scratch directory. Behaviour identical (the docstring is read by
  `argparse` only through `__doc__.splitlines()[0]`, i.e. its first line, which is unchanged).
* **C-11b (CLI contract change — L1 decision, NOT certified identical by me):** delete the
  `--work` argument. A caller passing `--work DIR` would get an argparse error instead of a
  silent no-op. No committed caller passes it (the frozen claim's counter command is
  `python3 {tool}/corpus/instruments/r46-f29-gate.py --root {tree}`), **but the F29 draft does**:
  `R46bExecSelftestF29.draft/r46-selftest-f29.py:571-573`

  ```python
  def run_cli(counter: str, root: str, work: str) -> tuple[int, str]:
      p = subprocess.run([sys.executable, counter, "--root", root, "--work", work], …)
  ```

  So C-11b would break the draft's `ctl-positive-cli` case unless the draft's `run_cli` is
  changed in the same step (drop `--work work`). C-11a has no such coupling.

### C-12  `R46bExecSelftestF29.draft/r46-selftest-f29.py:798` — `--jobs` accepted and never read

```python
798:    ap.add_argument("--jobs", type=int, default=1)
```

`a.jobs` appears nowhere in the draft (the draft grades in-process, serially — `grep -n "jobs"`
returns only the USAGE line 39 and this line), and the USAGE line 39 advertises it:

```
39:                               [--jobs N] [--do-nothing-control] [--keep] [-v]
```

Cut: delete line 779 and drop `[--jobs N]` from the USAGE line. Behaviour: the draft is not yet
landed, so no committed caller can depend on the flag; the only observable change is that a caller
passing `--jobs 8` would now get an argparse error instead of a silent no-op.

### C-13  `R46bExecSelftestF29.draft/r46-selftest-f29.py:40` — the docstring claims `--pure` is an input

```
40: READ-ONLY on --lane and --pure; scratch only under --work (default
```

`--pure` is parsed (line 797) and never read — the flag's own help text says so ("accepted for
interface parity; the F29 trees are built from the lane's committed corpus"), and the trees are
built by `build_positive(dest, lane)` from the **lane**, not from a pure export.

Unlike `--jobs`, `--pure` is *deliberate* interface parity with the other two selftests (a shared
driver can call all three the same way), so it should stay; the **docstring** is what drifts.
Cut: reword line 40 to "READ-ONLY on --lane; `--pure` is accepted for interface parity and read
by nothing". Behaviour: identical (docstring only; `argparse` reads only the first docstring
line).

## 3. Docstring drift (no code change needed)

| file:line | documented | actual |
|---|---|---|
| `r46-mutbat.py:26` | `mutbat counter=<c> mutants=<n> caught=<k> equivalent=<e> uncaught=<u> baseline_failures=<b> exit=0|1` | the printed summary (line 176) has **no** `exit=` field: `mutbat counter=%s mutants=%d caught=%d equivalent=%d uncaught=%d baseline_failures=0`. The exit status is the process exit code, not a printed field. |
| `r46-f29-gate.py:51,54` | "scratch under --work / TMPDIR"; `[--work DIR]` | the gate writes no scratch; `--work` is inert (C-11). |
| `R46bExecSelftestF29.draft/r46-selftest-f29.py:17-18` | two bullets, `clause-a-counts-30` … "-> only the" / `clause-a-counts-28` … "count clause fires (receipt disclosure (a), first half)." | the first sentence is split across two bullets: the `clause-a-counts-30` bullet ends mid-sentence ("-> only the") and its completion is glued to the `clause-a-counts-28` bullet, which therefore has no description of its own. Fix: give each bullet its own sentence. |
| `R46bExecSelftestF29.draft/r46-selftest-f29.py:519-520` | `"""The counter's live-line rule (fenced and HTML-commented lines are not live)."""` | the implementation skips only lines that *start* with `<!--`; a line **inside** a multi-line HTML comment block is treated as live (see O-1). The docstring overstates the rule. |
| `R46bExecSelftestF29.draft/r46-selftest-f29.py:8-13` | case names `ctl-positive`, `ctl-positive-cli`, `ctl-junk`, `ctl-fabricated` | the code prints `ctl positive`, `ctl positive-cli`, `ctl junk`, `ctl fabricated` (kind + name); the first three bullets carry a `ctl-` prefix the printed lines do not have. Harmless, but the docstring should use the printed names. |
| `R46bExecSelftestF29.draft/r46-selftest-f29.py:40` | "READ-ONLY on --lane and --pure" | the draft reads nothing from `--pure` (the trees are built from the lane's committed corpus) — see C-13. |

## 4. Deliberate duplication that must **not** be cut

`R46bExecSelftestF29.draft/r46-selftest-f29.py` vendors the tree recipes of
`controls/f29-fixture.py` and `controls/f29-defects.py` (lines 70-73 pin their sha256, lines 78+
carry the copies). This looks like a duplicated fixture builder, but it is **intentional and
documented** ("the recipes are vendored so the selftest stays self-contained") and it carries its
own drift check. I verified the pins against the live control files — they match exactly:

```
$ sha256sum …/controls/f29-fixture.py …/controls/f29-defects.py
52ea96939c62a71943838ca883d7914dd598f3e7eeb061266975ece7ccb26275  f29-fixture.py
2e95d4d4b6cf372a8464803bf82c7ae79d1612dc8060b5a9c18798cfbcbc07c2  f29-defects.py
```

(the draft's `BUILDER_PROVENANCE` at lines 70-73 holds exactly these two digests.) No cut.

## 5. Observations that are **not** dead-weight cuts (for the L1; not applied)

**O-1  `r46-f29-gate.py:115-126` — the copied `live_lines` is weaker than the counter it was
copied from, and the weaker copy is exploitable.**

`r46-c2-gate.py:120-132` (attempt-1 counter) removes whole HTML comment blocks and tracks the
fence *marker*:

```python
120: def live_lines(t: str) -> list[str]:
121:     """Lines outside HTML comments and fenced code blocks."""
122:     t = re.sub(r"(?s)<!--.*?-->", "", t)
123:     out, fence = [], None
…
127:         if st.startswith("```") or st.startswith("~~~"):
128:             mark = st[:3]
129:             fence = None if fence == mark else (fence or mark)
```

`r46-f29-gate.py:115-126` (the round-46 C2 counter) skips only lines that *start* with `<!--`
and toggles one boolean fence:

```python
115: def live_lines(text: str) -> list[str]:
…
120:         if st.startswith("```") or st.startswith("~~~"):
121:             fence = not fence
…
123:         if fence or not st or st.startswith("<!--"):
```

Consequence, reproduced by me: a tree whose F29 frontier row **and** S074 registry row are hidden
inside HTML comment blocks (a rendered table with 28 frontier rows) is graded **7/7**:

```
$ python3 …/r46-f29-gate.py --root $S/tree-comment
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H3 pass=1 read=row-S074=ok
…
f29-gate fixed=7/7 exit=0
```

The same input shape against the attempt-1 counter on its own tree is correctly red — the
discriminating run:

```
$ python3 …/r46-c2-gate.py --root $S/tree-comment-c2
gate G1 pass=0 read=rows=27 admitted=27 dup=0
gate G2 pass=0 read=F28-rows=0
gate G3 pass=0 read=row-S073=absent-or-malformed
c2-gate fixed=2/7 exit=1
```

The c2 selftest already carries this shape as a committed case (`mut-f28-row-in-html-comment-block`,
`mut-s073-row-in-html-comment`); the f29 gate has no equivalent case. The reviewer seat
`R46bRevF29H1` reached the same hole independently (its receipt
`R46bRevF29H1.draft/a6-comment-oneline-f29.gate.txt` prints `f29-gate fixed=7/7 exit=0` for a
comment-hidden F29 row), so this is corroborated, not a one-off.
This is a behaviour **change**, so it is not on my cut list — it is a candidate erratum. Note that
the same inherited pattern (and a literal dead `or (False)` disjunct) exists in the read-only
attempt-1 counter at `r46-c2-gate.py:186-188`; fixing one and not the other leaves two
conventions.

**O-2  `r46-mutbat.py:169` — the "equivalent" verdict accepts an empty proof file.**

```python
169:            elif mid in eq and os.path.isfile(eq[mid]):
```

The claim C1 kill rule says an equivalent verdict dies when its proof file is "missing, empty, or
falsified"; the battery tests only existence, not emptiness. Truth table on the exact source
expression:

```
battery condition  `mid in eq and os.path.isfile(eq[mid])`  -> True
size of that proof file: 0 bytes
missing-path variant -> False
```

Consequence: an empty file in the `--equivalent` map is graded `equivalent`, and the battery would
still print `uncaught=0`. A one-token strengthening (`os.path.getsize(eq[mid]) > 0`) is a
behaviour change and is therefore not certified identical here — flagged for the L1.

**O-3  stale scratch-seat names in the two committed selftests** (attempt-1 seat names hard-coded
into the attempt-2 instruments):

* `r46-counters-selftest-c1.py:575` → `"kasegi-r46", "R46W2ExecSelftestC1"`
* `r46-counters-selftest-c2.py:282` → `"kasegi-r46", "R46W2ExecSelftestC2"` (also documented at
  c2 line 31)

Both default to a closed round's seat directory under `$HYAKU_SCRATCH`, so two seats can collide
on the same default scratch path. Renaming moves where files are written (not the verdicts) — an
L1 decision.

Live corroboration while I worked: `/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2` (the
stale default of the committed C2 selftest) was being written by another seat at 19:29:13 while
my own runs used an explicit `HYAKU_SCRATCH` under my own scratch. The collision is not
hypothetical — it is the default path two seats would share.

**O-4  the drafted C2 counter amendment (`R46bExecGatePinAmend.draft/r46-c2-gate.py`) is clean.**
AST probe over it: no dead bindings, no unused imports; the diff against the committed v1.2 is a
focused 20-line change (ledger joins `CONTENT_EXEMPT`, one pin updated, docstring counts updated
from "62 … the two entries" to "61 … three entries", consistent with 64 − 3 = 61). No cut.

## 6. Differential summary (what was actually run)

**F29 gate — cut set C-1…C-4 applied to a scratch copy of the frozen instrument** (the copy keeps
`import tempfile` dropped, `SNAP_LINES` collapsed into `BODY[1]`, one shared `sect_text`
extractor, and the unreachable `raw` branch replaced by `len(f29) != 1`); a second copy
(`cut2`) additionally **deletes** the branch. Both copies were run against 21 trees:

```
base             SAME power-same | orig: f29-gate fixed=1/7 exit=1  | cut:= cut2:=
tree-positive    SAME power-same | orig: f29-gate fixed=7/7 exit=0  | cut:= cut2:=
tree-junk        SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
tree-fabricated  SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-badnames     SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-dupquote     SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-duprow       SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-entrymutant  SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-fencedf29    SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-fewquotes    SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-fewspans     SAME power-same | orig: f29-gate fixed=5/7 exit=1  | cut:= cut2:=
def-kindcase     SAME power-same | orig: f29-gate fixed=5/7 exit=1  | cut:= cut2:=
def-longquote    SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-manws        SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-nestedmd     SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-row9cells    SAME power-same | orig: f29-gate fixed=5/7 exit=1  | cut:= cut2:=
def-symlink      SAME power-same | orig: f29-gate fixed=5/7 exit=1  | cut:= cut2:=
def-thinscope    SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-thinsection  SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-vjunk        SAME power-same | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
def-widespan     SAME power-DIFF | orig: f29-gate fixed=6/7 exit=1  | cut:= cut2:=
```

`SAME` = the cut copy's transcript is byte-identical to the frozen gate's on that tree
(`diff -q`); `power-same/power-DIFF` = whether the power-control copy (one semantic change)
differs — it differs on exactly one tree, `def-widespan`, which is the tree that exercises the
changed clause. 21 trees × 3 gate copies = 63 runs.

**C1 selftest — cut set C-7 + C-8 applied to a scratch copy of `r46-counters-selftest-c1.py`**
(the copy's delta is exactly the two items: `m_still_gated_edited` rewritten onto `_recheck_idx`,
and `stdout` → `_`; verified by `diff -u`). Both copies were run over the **whole** selftest
(76 counted cases + the residual case), against the frozen tree and the frozen pure export:

```
$ python3 $S/freeze/corpus/instruments/r46-counters-selftest-c1.py --lane $S/freeze --pure $S/pure --work … --jobs 8
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
$ python3 $S/cut-mut/r46-counters-selftest-c1.py  --lane $S/freeze --pure $S/pure --work … --jobs 8
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
$ diff -q c1selftest-orig.txt c1selftest-cut.txt
C1 SELFTEST TRANSCRIPTS BYTE-IDENTICAL      (78 lines each, exit 0 both)
```

`cases=76 failures=0` matches the frozen baseline receipt `controls/selftest-baselines.txt`
("c1 76/0"), so the differential ran the real selftest (its 76 cases include the TIP-7of7 control,
the do-nothing control and the two HOME-bounties controls), not a degraded one.

**C2 selftest — cut set C-6 applied to a scratch copy of `r46-counters-selftest-c2.py`** (the copy
has exactly the two dead-loop lines removed — verified by `diff -u`, the delta is only

```
-        for i, (sct, floor) in enumerate(zip(SECTIONS, SECT_FLOORS)):
-            nm = ["scope", "overlap", "limits", "falsifiable"][i]
```

). Both copies were run over the **whole** selftest (137 counted cases + the probes), against the
frozen tree and the frozen pure export:

```
$ HYAKU_SCRATCH=… python3 $S/freeze/corpus/instruments/r46-counters-selftest-c2.py --lane $S/freeze --pure $S/pure
selftest cases=137 failures=0
$ HYAKU_SCRATCH=… python3 $S/cut-mut/r46-counters-selftest-c2.py  --lane $S/freeze --pure $S/pure
selftest cases=137 failures=0
$ diff -q c2selftest-orig.txt c2selftest-cut.txt
C2 SELFTEST TRANSCRIPTS BYTE-IDENTICAL      (145 lines each, exit 0 both)
```

`cases=137 failures=0` matches the frozen baseline receipt
`controls/selftest-baselines.txt` ("c2 137/0"), so the differential ran the real selftest, not a
degraded one.

**Mutation battery — cut set C-5 applied to a scratch copy of `r46-mutbat.py`** (the copy has
lines 39-40 deleted). Both copies were run over the **whole** battery flow (all 20 C1 mutants and
all 21 C2 mutants, baseline run included) against a tree whose two selftests are replaced by a
one-line stub printing `selftest cases=1 failures=0`, so that every mutant and the baseline are
exercised without the multi-minute real selftest:

```
$ python3 …/r46-mutbat.py --root $S/stubtree --pure $S/pure --work $S/work-stub-orig --counter both --jobs 8 > mutbat-stub-orig.txt
$ python3 …/cut-mut/r46-mutbat.py --root $S/stubtree --pure $S/pure --work $S/work-stub-cut --counter both --jobs 8 > mutbat-stub-cut.txt
MUTBAT OUTPUT IDENTICAL
```

(the transcripts are 43 lines each: 41 mutant lines + 2 summary lines; `--list` output, 41 lines,
is identical too.) This is a **shape** differential over the full instrument flow, not a verdict
differential: the stub selftest makes every mutant read `uncaught`, so the transcripts agree by
construction on the verdict columns. What it certifies is that the cut changes neither the
instrument's control flow, its output format, its exit status, nor its mutant table.

**Attempted and not completed — the verdict-level battery differential.** I also launched the
*real* battery (frozen tree, frozen pure export, `--counter c1 --jobs 8`) to compare the frozen
instrument with the C-5 cut copy on the real selftests. It ran 30 minutes under the wave's load
and was killed by the 1800 s cap after **one** mutant: each mutant re-runs the full C1 selftest
(≈90 counter invocations), so the 41-mutant battery does not fit in this seat's window. The one
mutant it did finish reproduces the frozen receipt's first line exactly, which confirms my test
bed is the L1's:

```
mine:    mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught
frozen:  mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught
                                  (…/controls/mutbat-before.txt, line 1)
```

I therefore do **not** claim a verdict-level battery differential; the stub-tree differential
above plus the AST/grep proof (C-5) is what I have.

## 7. Limitations

* The C1 and C2 counters themselves (`r46-c1-gate.py`, `r46-c2-gate.py`) were read only for
  comparison; they are out of scope and untouched.
* The battery differential in §6 is the stub-selftest *shape* differential described above; the
  verdict-level differential against the real selftests was **attempted and killed at the 1800 s
  cap** (one mutant of 41 finished), so I do not claim that the cut preserves the real battery's
  verdicts on the real tree (it must — the two removed names are never read — but that is an
  argument plus the AST/grep proof, not a completed re-run).
* The F29 draft was a moving target while I read it (861 → 876 lines). Line numbers for the draft
  are those of sha256 `23b528a4…` (906 lines); the draft changed twice under me (861 → 876 → 906 lines),
  so the L1 must re-anchor them against the revision it integrates.
* The drafts of `ExecSelftestC1`, `ExecSelftestC2` and `ExecMutbatF29` were not present in
  `.ufo/waves/round-46/attempt2/wave1/` while I worked, so my findings for the C1/C2 selftests and
  the battery are stated against their committed base; each must be re-checked against the draft.
* No live target was contacted: the corpus is documentation only, the F29 capture is the frozen
  local snapshot, and the census script is the local fleet copy.
* A /tmp path is not cited as evidence anywhere in this report; every quoted output comes from a
  re-run I performed in `$HYAKU_SCRATCH/kasegi-r46/R46bSimplifierDrafts`.
