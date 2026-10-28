# R44Critic9 — mutation-minded attack: how could the C1 closure counter accept a fake fixed state without checking relevant bytes?

- seat: `R44Critic9` (critic, leaf); round **44**, lane `kasegi`; read-only.
- lane `HEAD` at review: `66314015122b9aa32dc40f2f1815df56624c26d1` (`round-44: freeze claims and validated wave`); frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (`git merge-base --is-ancestor` → true).
- item under attack (verbatim, `.ufo/waves/round-44/claims.json:12,14`):
  - after: `"0 of those same 8 frozen routed defects remain unresolved, proven by one committed read-only counter over committed lane evidence; all eight have append-only fixes and at least one red-before control per changed gate."`
  - counter: `"python3 corpus/instruments/r44-routed-defects.py --root <lane-export> --baseline <frozen-base>"`
- kill rule: *"If a do-nothing replay against the frozen base can report all 8 fixed, or if any frozen defect remains unresolved at the final lane revision, C1 fails."*
- method: read-only. `git archive 5ab3a60 | tar -x` into scratch, then two probe counters (naive presence-shaped vs. byte-re-deriving) plus three mutant trees, all under `$HYAKU_SCRATCH/kasegi-r44/R44Critic9/`. No lane file, index, ref or fleet file was written. No tool installed.

**One-line answer.** The counter as specified can accept a fake fixed state through six independent channels — the two that matter most are (1) `--root` names a *directory*, so "committed lane evidence" is never bound, and (2) seven of the eight defect predicates can be written in a presence shape that is **already true at the frozen base**, so the do-nothing replay reads **4/8 fixed** (cheapest shape) to **7/8 fixed** (natural variants) instead of 8/8 open, and the kill rule's conjunction never trips.

---

## 1. The strongest counterexample (measured)

A six-line stand-in that reads **no defect byte at all** passes both the do-nothing control and the after-state.

```
$ python3 standin.py --root base  --baseline base      # do-nothing replay
routed-defects unresolved=8/8 closed=0
exit=1

$ python3 standin.py --root forge --baseline base      # "final revision", nothing fixed
routed-defects unresolved=0/8 closed=1
exit=0

$ grep -cE '13/19|29-character|planner|names=|SHONEN|README|127' standin.py
0
```

Its whole rule is `8 if tree_identity(root) == tree_identity(baseline) else 0`. Because `--baseline` is an argument the counter is *given*, branching on "is this the baseline?" is free, and the kill rule — which only forbids *all 8 fixed at base* — cannot see it. The round-43 lesson already recorded the remedy for exactly this class (`corpus/instruments/claim-package-check.py`: nine single-defect fixtures plus an always-pass stand-in rejected `observed=rejected-9/9`, spotcheck §4). C1 carries **no mutant-control requirement** for its counter; the only control named is `controls/c1-do-nothing.txt`, which is a conjunction-level tripwire.

---

## 2. Presence-shaped predicates are already true at the frozen base

`probe.py` implements, per frozen defect, the cheapest predicate a first implementer writes ("token present / file exists / path exists / ends with newline") and the predicate that re-derives the defect's bad byte.

```
$ python3 probe.py --root base --base base --report base-report.md      # do-nothing
id  naive strict note
D1  open  open   base-run=False; SCORECARD carries the literal=True
D2  open  open   erratum paragraph token+superseded=False
D3  FIXED open   26-occurrences=4; 29-character lines=2
D4  open  open   report=base-report.md planner-hits=0
D5  open  open   names=0 seats=73 members=73
D6  FIXED open   tail='`.\n' base-is-prefix=True
D7  FIXED open   README rows for the two instruments=0
D8  FIXED open   claim-has-127=True control-prints-127=False
naive_fixed=4/8 strict_fixed=0/8
```

Four defects read "fixed" at the base with **zero corrections in the tree**. The mechanism is uniform: each of these four is a *wrong value inside an artifact that already exists*, never a missing artifact —

| defect | bad byte at base | why the presence check is already true |
|---|---|---|
| D3 | `corpus/lessons/round-43.md:90,101` say `29-character prefix` | the correct numeral `26` and the 26-char prefix `c6ae07c6a541e0e96d0040afb6` already occur (4 and 2 times) |
| D6 | `SHONEN.md` tail is `` `[~]`.\n `` (one newline) | "ends with a newline" is true; the defect is the *second* newline |
| D7 | report bullet names `corpus/instruments/README.md`, which has 0 rows for the two instruments | "the named path exists" is true |
| D8 | r43 `claims.json:38` states `(exit 127)`; the cited control prints `exit=2` | "the claim states 127" is true |

With the three most natural variant predicates (D1 "SCORECARD carries the literal **and** any prior `Correction (round` heading" — SCORECARD is full of them; D2 "a `claims-erratum*.md` exists in the round dir" — one does; D5 "`de09313` appears under `final-gates/`" — the run file names it):

```
$ python3 variants.py
D1  FIXED ... D2  FIXED ... D3  FIXED ... D4  open ... D5  FIXED ... D6  FIXED ... D7  FIXED ... D8  FIXED
variant_naive_fixed=7/8 at the frozen base
```

**7 of 8 read fixed at the base.** Only **D4** is structurally open there, because its artifact (the round-44 report) does not exist yet. So in the 7/8 shape, the entire do-nothing control rests on a single defect, and the kill rule's "all 8 fixed" is unreachable by construction while seven predicates are vacuous. This is the precise gap: **the kill rule is a conjunction over defects; the counter is a conjunction of predicates; a conjunction of predicates can be vacuous on any proper subset and the conjunction-level control still reads "not all fixed".**

## 3. Forged tip: 8/8 with nothing fixed

Eight appended lines — no defect touched — flip every naive predicate:

```
$ python3 probe.py --root forge --base base --report forge-report.md
id  naive strict note
D1  FIXED open   base-run=False; SCORECARD carries the literal=True
D2  FIXED open   erratum paragraph token+superseded=True
D3  FIXED open   26-occurrences=5; 29-character lines=2
D4  FIXED open   report=forge-report.md planner-hits=1
D5  FIXED open   names=1 seats=73 members=73
D6  FIXED open   tail='`.\n' base-is-prefix=True
D7  FIXED open   README rows for the two instruments=0
D8  FIXED open   claim-has-127=True control-prints-127=False
naive_fixed=8/8 strict_fixed=0/8
```

The eight forgeries (`diff -rq base forge`): one `Correction (round 44)` line in `SCORECARD.md`; one erratum paragraph carrying `closed=13/19` + `superseded` and one carrying `exit 127` + `superseded`; one line in `corpus/lessons/round-43.md` saying "26 characters" with no counting command; `planner=L1` + `residual calls: 0` appended to a *copy* of the report with no seat mapping; `names=ExecSuiteSkeleton` (1 name against `seats=73`); `export-ref=de09313` appended to the transcript; an HTML comment in `corpus/instruments/README.md`. Every one is a naming without the superseding content the spotcheck's §6 demands.

## 4. `--root` is a directory: the export is never bound to a commit

`claims.json:14` grades the *tip* through `<lane-export>` (a directory) and the *before* side through `<frozen-base>` (a ref). The asymmetry is backwards: the side under test is the unverified one. The family's own committed defence is the opposite and is explicit (`corpus/instruments/r43-closure.sh:4-11`):

```
# A plain invocation (no --export-ref) refuses with exit 2: the suite only ever
# grades an exported tree, never a working tree.  The export is produced with
#     git -C <lane> archive <hash> | tar -x -C <work>/export
# A ref that does not resolve prints `ref-not-found` and exits 1: an
# unresolvable ref is a red, never a vacuous pass.

$ bash corpus/instruments/r43-closure.sh
r43-closure: a plain run is refused (export mode only); pass --export-ref <hash>
exit=2
```

r44 replaces `--export-ref <hash>` with `--root <dir>`. Nothing in the named command prevents `cp -r export forged && append eight lines`, and §3 above is exactly that: the forged tree is a directory, never a commit, and the counter has no argument with which to notice. A counter must print and re-derive `root-ref=<40 hex>` (or a tree digest) and must refuse a root that is not an extracted `git archive` of a commit in the lane.

## 5. `--baseline` is unpinned: the denominator can be zeroed

The population is defined only by *"numbered routed defects in `corpus/lessons/round-43-verifier-spotcheck.md` §6"* (`controls/do-nothing.txt:5`). That file landed **in** the spotcheck commit, so any earlier ref yields an absent file and a zero denominator:

```
$ git cat-file -e ab98fac9:corpus/lessons/round-43-verifier-spotcheck.md ; echo $?
ABSENT
$ git show ab98fac9:corpus/lessons/round-43-verifier-spotcheck.md | grep -Ec '^6\. Routed defects|^[0-9]+\. \*\*'
0
grep-exit=1
```

A counter that derives N from `--baseline` and then checks `unresolved == 0` reports **0 of 0** and closes. Even a shell-shaped `n=$(... | grep -Ec ...)` yields the string `0` on absent input (grep exits 1 but prints `0`), so the vacuity survives a `set -e`-free script. Required: `--baseline` must be pinned to `5ab3a60…` (or its §6 block digest), the file must exist, and N must be asserted `== 8` with a non-zero exit otherwise.

The population is also read from the *mutable* side if the counter takes it from the tree under test:

```
$ cp -a forge forge2 && <delete §6 item 3 from forge2>      # defect 3 untouched
$ grep -Ec '^6\. Routed defects|^[0-9]+\. \*\*' forge2/corpus/lessons/round-43-verifier-spotcheck.md
7
$ <append '9. **unrelated list item**' to another section>
$ grep -Ec '^6\. Routed defects|^[0-9]+\. \*\*' forge2/corpus/lessons/round-43-verifier-spotcheck.md
8
$ grep -Ec '^6\. Routed defects|^[0-9]+\. \*\*' base/corpus/lessons/round-43-verifier-spotcheck.md
8
```

Deleting one defect line drops the denominator to 7 → "0 of 7 unresolved"; the same regex is **file-global, not §6-scoped** (an unrelated numbered bold line anywhere restores 8). The `^6\. Routed defects` alternative is dead code (`grep -cE '^6\. Routed defects'` → `0`; the heading is `## 6. …`). The counter must bind the population by digest of the §6 block **taken from `--baseline` blobs**, and must require the tip's copy to still contain those 8 items.

## 6. Deletion is a fake fix that no presence predicate can see

```
$ cp -a base del3 && <delete the two '29-character' lines>   # in-place rewrite, forbidden
$ python3 probe.py --root del3 --base base --report base-report.md
D3  FIXED FIXED  26-occurrences=4; 29-character lines=0
$ <baseline lines absent from tip>
baseline lines absent from tip: 2
  - ...the fix pointer, a 29-ch…
  - ...The fix pointer is a 29-character prefix; the full 40-character hash…
```

Both the naive **and** the strict predicate read fixed, because the bad claim is gone. C1's after-state demands *"append-only fixes"*, and nothing in a presence check enforces it: the counter must assert `baseline_lines ⊆ tip_lines` for every graded file, and must anchor corrections by **content**, not by line number (line anchors drift the moment a line is inserted or removed).

## 7. Two of the eight defects are graded against a file the export cannot contain

Defects 4 and 7 are about the round report:

- D7's literal: `.ufo/reports/round-43/kasegi.md:91` — *"the two new instruments are registered in `corpus/instruments/README.md`"*.
- D4's fix is *"Record them next round (and in the next round's report shape)"* — i.e. the **round-44** report.

That file is **not in the lane repo**:

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h %an %s' -1 -- .ufo/reports/round-43/kasegi.md
fdf719a9 kasegi-shokunin round-43: kasegi report
$ git -C kasegi-shokunin cat-file -e fdf719a9
fatal: Not a valid object name fdf719a9
$ git -C kasegi-shokunin ls-tree -r --name-only HEAD -- .ufo/reports/
.ufo/reports/round-21/kasegi.md
$ ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kasegi.md
ls: cannot access '…': No such file or directory
```

So `--root <lane-export>` cannot see D4 or D7 at all. The counter then has exactly two bad options: silently drop them (report "0 of 8" while grading 6) or read the **fleet working tree**, which is neither committed lane evidence nor frozen (a single uncommitted edit to `.ufo/reports/round-44/kasegi.md` forges D4 and D7 simultaneously). A correct counter needs a third, explicit input — a fleet-side ref for the report — and must fail closed when it is absent. Note the report is also self-authored: D4's mapping must be cross-checked against the wave dispatch (seats actually spawned), not merely present.

## 8. Unobservable clauses and export hermeticity

- **D5's third clause is unfalsifiable.** `.ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp` was **untracked**; `git ls-tree -r 5ab3a60 -- .ufo/waves/round-43/final-gates/` lists four files and no `.tmp`, and `ls …/*.tmp` → *No such file or directory*. A `git archive` export can never contain it, so no committed byte records either its presence or its deletion. Any predicate "no `*.tmp` in the tree" is true at base and true on every fresh clone — **zero discriminating power**. Grade D5 on the *emitter* (the tracked file that produced `names=`) and say the leftover clause is out of scope, rather than counting a tautology as a fix.
- **The export is not hermetic.** It carries **58 committed symlinks** (`git ls-tree -r 5ab3a60 | awk '$1=="120000"' | wc -l` → 58), of which six are **absolute** and point back into the live lane tree, e.g. `.ufo/waves/round-29/wave1/CritC2Kill-scratch/corpus/instruments -> /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments`. A counter that walks with `grep -R`, `find -L` or `os.walk(followlinks=True)` reads the **working tree** through them, and a counter that resolves a path through a symlinked parent reads whatever the lane has staged. Resolution must refuse symlinks (or `lstat` and record them) before claiming "committed lane evidence".
- **Token extraction.** r43's `C1.before` is a **JSON list of strings**, not a string: `json.load(...)['claims'][0]['before']` returns `['see .ufo/waves/round-43/c1-controls/… (exit 127); …']`, and `'127' in <that list>` is `False` (membership, not substring). A first-implementer reader therefore sees *no token* where the defect is. The counter must walk the cell recursively as K17 does (`corpus/instruments/r43-limbs/k17-claims-before.sh`), and match whole tokens only — `exit=127` and `exit 127` are different tokens, and the spotcheck's D8 literal is `(exit 127)`.

---

## 9. Fixable defect vs. tradeoff

All of the above are **specification defects**, fixable inside the frozen claim without touching its wording — they do not require re-freezing, and none of them argues that C1's target is wrong. The minimal counter contract that survives every attack above:

1. `--root` must be a **ref**, not a directory: resolve `--export-ref <40 hex>`, export with `git archive`, print `export-ref=`, `counter-sha256=`, `root-digest=`, `baseline=`; refuse a plain run with exit 2 (copy `r43-closure.sh:4-11`).
2. Pin `--baseline` to `5ab3a60…`; require the spotcheck file present; take the 8-item population from the **baseline blob** by §6-block digest; assert N == 8; require the tip's copy still contains all 8 items.
3. **Append-only guard** on every graded file: `baseline_lines ⊆ tip_lines`; corrections anchored by content.
4. **Re-derive each defect's bad byte** and require a correction that carries the superseding *content* (a value, a per-limb result, a counting command, a seat mapping, a table row) — never a bare token.
5. Emit **8 per-defect payload lines** with ids and evidence pointers (the r43 `K<n> payload=` grammar), so a reviewer can audit the aggregate.
6. **Grade D4/D7 against an explicit fleet-side ref** for the report; fail closed if absent; cross-check the planner mapping against the wave dispatch.
7. **Mutant controls**: eight single-defect exports (fix all but one → the counter must name that one open) plus the always-pass stand-in must be rejected. Do-nothing alone is insufficient — §1 and §2 prove it.

## 10. What the do-nothing control can and cannot discriminate

- **Can**: detect an always-pass counter (it would read 8/8 fixed at base) and detect a counter that never runs.
- **Cannot**: detect a baseline-discriminating stand-in (§1); detect vacuity on any proper subset of the eight (§2: measured 4/8 and 7/8 fixed at base); detect a denominator of 0 or 7 (§5); detect deletion-as-fix (§6); detect that D4/D7 were never graded (§7).

So `controls/c1-do-nothing.txt` discriminates *do-nothing versus something*, not *real derivation versus fake*. C1's kill rule inherits that limit. I am not calling C1 failed — the target may well be reachable — but **at the freeze there is no committed artifact that could distinguish the real counter from the stand-in**, and C1's after-state as written does not require one.

## 11. Limitations

- `r44-routed-defects.py` does not exist at `HEAD` (`ls corpus/instruments | grep -i r44` → none), so this is an attack on the **specified interface** and on the predicate shapes an implementer will reach for; §2–§6 measure those shapes, not the lane's actual (unwritten) counter.
- The stand-in in §1 compares two directories; resolving `--baseline` as a ref is one `git archive` away and does not change the finding.
- The `forge`/`del3`/`forge2` trees are scratch artifacts; they are evidence of a reachable state, not of any lane commit. `git -C kasegi-shokunin status --porcelain` was not modified by this seat beyond the untracked `.ufo/waves/round-44/wave1/R44Critic9.md` this seat was told to write.
- The census, the frontier and C2 were out of this item's scope; not measured here.
- Tool installs: **none**. Scratch `/fast/scratch/hyaku/kasegi-r44/R44Critic9/` deleted on exit (see §12).

## 12. Scratch

`/fast/scratch/hyaku/kasegi-r44/R44Critic9/` — `base/`, `forge/`, `forge2/`, `del3/`, `probe.py`, `variants.py`, `standin.py`, `evidence.txt`, `base-report.md`, `forge-report.md`. Removed on exit:

```
$ rm -rf /fast/scratch/hyaku/kasegi-r44/R44Critic9 && ls -d /fast/scratch/hyaku/kasegi-r44/R44Critic9
ls: cannot access '/fast/scratch/hyaku/kasegi-r44/R44Critic9': No such file or directory
$ git -C kasegi-shokunin rev-parse HEAD
66314015122b9aa32dc40f2f1815df56624c26d1
```

Lane worktree after this seat: `?? .ufo/waves/round-44/wave1/R44Critic9.md` is the only path this seat added; the seven ` M` files (`PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`) are sibling seats' round-44 production edits, not this seat's.
