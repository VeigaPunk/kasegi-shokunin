# CriticClaimsC1 — round 93, C1 frozen-predicate attack

Seat: CriticClaimsC1 (leaf; no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `e15996bfd2f6eca4af39507a7c5973afbeca8347`; freeze `5bad9e55d3d9319446e3d9b63bc2dece633cdb68`;
C1 landing `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`. C2 is not judged here.

Method: fresh `git clone --shared` of the lane (toplevel asserted equal to the clone); the counter,
map and labels were extracted **from the freeze blob**, re-hashed, and the frozen command was run
against the clone. All command outputs are in `CriticClaimsC1-receipts/` (index: `00-commands.txt`).

## Verdict

**C1 STANDS on the frozen predicate P1–P3 at `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`.** I
re-derived every part myself from committed bytes; no limb was taken from the claims file.

- **P1 PASS, rc=0.** `KNOWLEDGE-METER base=1007/2001 after=1009/2000 base_target=1007/2001
  target=1009/2000 sites=5 labels=8 mirror_absent=True pinned=archive`; `M0 pass`, `M1 pass`,
  `M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0`, `M4 pass bad=none`,
  `M5 pass out_of_range=none`, `M9 pass rows=5 unbound=none`, `M10 pass labelled=8 want=5
  mapped=5 kinds=cell-repair=2,no-edit=3,range=3 unknown=none unapplied=none unlabelled=none`,
  `M6 pass sha256=7ab66a7f…`; `KNOWLEDGE-METER-RESULT pass rc=0` (receipt `01-frozen-run.txt`).
- **P2 PASS.** Counter sha256 `d9f9432d44f09154da95a03531ff8e5643e708bee0f4b067781819a8e57c4b92`
  and map sha256 `7ab66a7fc8a90cf92d026d0ba1abaa23461b10a3bbd79d003ee4a33961eb3b76` equal the
  frozen values at the freeze blob, at the landing blob and in the worktree. The labels blob
  `51b4f3eb3ccc44c9138c29a1052dbb08f951001c9cc0f9dd2971c25f0b670dff` is likewise identical at
  freeze/landing/worktree (not required by P2; checked as context) (`02-p2-p3-freeze.txt`).
- **P3 PASS.** `git diff-tree --no-commit-id --name-only -r ae53b3c` prints exactly **1** path;
  `--name-status` prints `M corpus/knowledge/triage-thresholds.md`. The landing's parent is the
  freeze (`git rev-list --parents -n 1 ae53b3c` → `ae53b3c 5bad9e5`; freeze's parent is the base).
  Freeze therefore precedes the landing, and the landing changes no other tracked path.
- **Controls are freeze blobs.** `c1-controls-r93.txt` (sha256 `40278335…`) and
  `c1-controls-r93.py` (sha256 `a8af1960…`) are byte-identical at the freeze and in the worktree;
  `git diff 5bad9e5..HEAD -- .ufo/waves/round-93/c1/ .ufo/waves/round-93/controls/` is empty.
  Re-running the frozen controls script against a clone of the landing reproduces the receipt
  **byte-for-byte** (`diff` rc=0; `C1-CONTROLS-RESULT pass controls=11`) — but see the routed
  defect: control 10 is a false pass even though it reproduces.
- **Arithmetic re-derived, not read off the target.** Token-set delta base→landing: removed 6
  distinct tokens (`SKILL.md:111`, `SKILL.md:117`, `SKILL.md:494-506`, `intake-surface.md:75-76`,
  `mission-control.md:37-38`, `openai-oauth/gpt-6-astra:max`), added 5 (`SKILL.md:176-178`,
  `SKILL.md:191`, `SKILL.md:827-848`, `corpus/knowledge/intake-surface.md:89-93`,
  `corpus/knowledge/mission-control.md:55-57`). Non-GONE removed 3 / added 5 → numerator
  `1007 − 3 + 5 = 1009`; total `2001 − 6 + 5 = 2000`; class churn on common tokens is empty. The
  printed `1007/2001 → 1009/2000` is exactly the five label-named edits and nothing else
  (`03-token-delta.txt`).
- **Provenance of the cell repairs (statement check, not scored).** The landed last cells for 437
  and 438 are byte-identical to the payloads the round-92 `ReviewC1Labels` TSV carries and to the
  round-93 label payloads (sha256 of the cell text `5fb889c77fb0d23a…` at 437, `12a9be3804379f42…`
  at 438). Anchors checked: base `SKILL.md:117` is a `provenance.json` line, not an attempts
  statement; base `SKILL.md:494-506` is park-disposition/autopsy text with no EV term; landing
  `SKILL.md:191` is the `attempts()≥2` termination statement; landing `SKILL.md:827-848` contains
  the EV formula block and the UNKNOWN fail-closed sentence; `MAX_ATTEMPTS` occurs 0 times in
  `SKILL.md` at base and landing; `intake-surface.md:89-93` and `mission-control.md:55-57` carry
  the round-13 corrections (`07-provenance-cells.txt`, `08-anchors.txt`).

## Routed defect — the advertised M3 labelled-file extension crashes; its only control is a false pass

**Counterexample (strongest available from local evidence).** Add one label that names a citing
file outside `corpus/knowledge` and change nothing else — e.g. the frozen counter's own control-10
label `SKILL.md:191  SKILL.md:191  CORRECT  "No edit…"` on top of the landing. The frozen
`knowledge-meter.py` exits **rc=1 with no LIMB line at all**:

```
KNOWLEDGE-METER base=1007/2001 after=1009/2000 … sites=5 labels=9 …
Traceback (most recent call last):
  File ".../knowledge-meter.py", line 399, in main
    if a.map_sha256:
AttributeError: 'str' object has no attribute 'map_sha256'
```

Cause: line 282 of the frozen counter shadows the argparse namespace `a` —
`b, a = file_at(B["tree"], rel), file_at(A["tree"], rel)` — inside the loop that exists only to add
labelled citing files outside the corpus/knowledge scope. Line 399 then reads `a.map_sha256`. The
loop is entered exactly when a label names such a file; every run in that configuration dies before
any limb is printed. Receipts: `05-ctl10-crash.txt`, `04g-F5.out`, `09-shadowing-source.txt`.

**Consequence for the claim's evidence.** The pre-freeze control `m3-labelled-file-scope` was meant
to prove the new walk. Its receipt line is `CONTROL m3-labelled-file-scope rc=1 want=1 PASS`
followed only by the summary line and then `C1-CONTROLS-RESULT pass controls=11` — no `LIMB M3
FAIL` line. The control "passes" because the crash's rc=1 equals the expected rc=1. I reproduced
that receipt byte-for-byte and separately reproduced the traceback. So the only control for the
successor counter's advertised `M3 … walks every labelled citing file` capability is invalid.

**Does this re-score C1? No, on the frozen predicate.** At this landing all eight label *sites*
(citing files) are `corpus/knowledge/*`, so `labelled_files - set(bfiles)` is empty, the shadowing
loop never runs, and P1's M3 passes. The item is a routed defect/qualifier, not a verdict change
per the wave rule. It does mean the C1 statement's sentence "M3 compares every labelled file's base
and after lines" and the surface's "walks every labelled citing file in M3, not only
corpus/knowledge (r92 CriticClaims counter gap)" are **not true of the frozen counter in general**;
at this landing the extension is vacuous, and the round-92 CriticClaims counter gap is not actually
closed.

**Impacted axis:** depth:verifiability (the counter capability the claim cites for closing the r92
gap). The landing's measured 5 edits are unaffected.

**Smallest safe correction (demonstrated, not applied).** Rename the two loop locals only:

```
-            b, a = file_at(B["tree"], rel), file_at(A["tree"], rel)
-            if b is not None and a is not None:
-                bfiles[rel], afiles[rel] = b, a
+            b, atext = file_at(B["tree"], rel), file_at(A["tree"], rel)
+            if b is not None and atext is not None:
+                bfiles[rel], afiles[rel] = b, atext
```

With only that 3-line diff, the control-10 scenario prints `LIMB M3 FAIL same_files=True
bad_lines=1 old_not_once=0 dup_rows=0` and `M9 pass`/`M10 pass`, rc=1 (`10-fixed-counter-control10.txt`;
patched copy `tools-km-fixed.py`). The control should then assert the printed `LIMB M3 FAIL`
(and empty stderr), not rc alone.

## Forgery matrix (four required variants plus one extra)

All forged commits were made in a scratch clone whose toplevel was asserted before every commit;
base `e15996b`, frozen map/labels except where noted. Full outputs: `04*.out` / `04-forgeries.txt`.

| # | Variant | rc | Limb evidence | Killed by |
|---|---|---|---|---|
| F1 | Unlabelled in-scope edit: `corpus/knowledge/citation-bases.md:20` gains plain text; rate unchanged | 1 | `M3 FAIL bad_lines=1`; M0/M1/M4/M5/M9/M10/M6 pass | **M3** |
| F2 | Out-of-scope edit: `SCORECARD.md` (meter is blind to it) | 0 | **all limbs pass** | no meter limb; **P3** (see F2b) |
| F2b | Landing-like commit with parent = freeze: triage restored from `ae53b3c` + `SCORECARD.md` edit | 0 | meter passes; `diff-tree --name-only` prints **2** paths (`SCORECARD.md`, `corpus/knowledge/triage-thresholds.md`) | **P3** (one-path test fails) |
| F3 | Map row's `new` differs from the frozen label: label says `SKILL.md:191`, map/after tree say `SKILL.md:526` at line 58 | 1 | `M9 FAIL unbound=triage-thresholds.md:58`; M1 `1009/2000`, M3/M4/M5/M10 all pass | **M9** |
| F4 | Label anchor out of range: labels rev + map + after tree write `SKILL.md:5000-5001` at line 144 (`SKILL.md` has 1251 lines) | 1 | `M5 FAIL out_of_range=triage-thresholds.md:144`; `M1 FAIL after=1010/2001`; M3/M4 pass, M9 passes (map==label) | **M5** (anchor range); M1 also trips |
| F5 | Extra: one `CORRECT "No edit"` label naming `SKILL.md`, **no edit anywhere** | 1 | no LIMB lines; `AttributeError` at line 399 | **none — the counter cannot evaluate this label set** (defect above) |

Notes: F3 shows the label binding is load-bearing independently of the written text (M3 passes
because the after tree matches the map; M9 is what rejects the disagreement). F4 shows the only
anchor-range check is M5; classify is range-blind (`strip_anchor` then existence), so M4 passes
`SKILL.md:5000-5001` and M5 catches it; the new out-of-range token also moves the rate to
`1010/2001`, so M1 trips alongside. F2/F2b show the meter is blind outside
`corpus/knowledge ∪ labelled citing files`; at this landing P3, not the meter, is the load-bearing
guard against an out-of-scope path, and P3 does kill it.

## Qualifiers (no verdict change)

1. **Label pin.** The counter pins the map by sha256 (M6) but never pins the labels blob; the frozen
   command pins `--labels-rev 5bad9e5`, whose labels blob is `51b4f3eb…`, so P2 stands. A future
   counter should carry a `--labels-sha256` like the map pin, otherwise the same command with a
   different labels rev is unpinned.
2. **Cell-repair M4 shape.** M4 accepts a `cell-repair` whose written corpus/knowledge value(s) need
   not include the key's own basename (it requires *either* a matching `corpus/knowledge/<basename>`
   value *or* lane-root values in range). The landed 437 cell does include
   `corpus/knowledge/intake-surface.md:89-93`, so the errata pointer is intact here; the loophole is
   latent, not exercised.
3. **Scope extension unexercised.** The landing's own label set has no citing file outside
   `corpus/knowledge`, so the new walk adds nothing to this tranche's M3; its only evidence is the
   invalid control-10. See the routed defect.

## Receipts

All outputs under `.ufo/waves/round-93/w1/CriticClaimsC1-receipts/`; commands in `00-commands.txt`.

| file | command (abbreviated) | observed |
|---|---|---|
| `01-frozen-run.txt` | frozen `knowledge-meter.py` over clone `--base-rev e15996b --after-rev ae53b3c --labels-rev 5bad9e5 --map repair-map.frozen.tsv --map-sha256 7ab66a7f… --base-target 1007/2001 --target 1009/2000` | rc=0; `KNOWLEDGE-METER-RESULT pass`; M0,M1,M3,M4,M5,M9,M10,M6 pass; base 1007/2001 after 1009/2000 |
| `02-p2-p3-freeze.txt` | `git show <rev>:<path> \| sha256sum`; `git merge-base --is-ancestor`; `git rev-list --parents`; `git diff-tree --no-commit-id --name-only/-status -r ae53b3c`; `git diff 5bad9e5..HEAD -- c1/ controls/` | counter d9f9432d…, map 7ab66a7f…, labels 51b4f3eb… same at freeze/landing/worktree; ancestor rc=0; landing parents `ae53b3c 5bad9e5`; 1 path `M corpus/knowledge/triage-thresholds.md`; post-freeze c1/controls diff empty |
| `03-token-delta.txt` | `python3 -B token-diff.py` (frozen counter imported; `reading()` at base and landing) | base 1007/2001, after 1009/2000; removed 6, added 5; non-GONE −3/+5; no class churn |
| `04-forgeries.txt`, `04b…`–`04i…`, `tools-forge-suite.py`, `tools-token-diff.py` | forge suite: F1 in-scope unlabelled, F2/F2b out-of-scope, F3 map≠label, F4 out-of-range anchor, F5 labelled non-knowledge no-edit | F1 rc=1 M3 FAIL bad_lines=1; F2 rc=0 PASS; F2b rc=0 with 2-path diff-tree; F3 rc=1 M9 FAIL unbound=58; F4 rc=1 M5 FAIL out_of_range=144 + M1 1010/2001; F5 rc=1 AttributeError, no limbs |
| `05-ctl10-crash.txt`, `tools-ctl10-repro.py` | clone landing; edit `SKILL.md:191`; append control-10 label; frozen map; commit; run meter | rc=1; summary line only, no LIMB lines; `AttributeError: 'str' object has no attribute 'map_sha256'` (line 399) |
| `06-controls-rerun.txt`, `06-controls-rerun-diff.txt` | `c1-controls-r93.py` re-run against a clone of the landing; `diff` against the frozen receipt | identical (diff rc=0); `C1-CONTROLS-RESULT pass controls=11`; control 10 shows rc=1 PASS with no LIMB line |
| `07-provenance-cells.txt` | compare round-92 `round93-labels.tsv` payloads, round-93 labels payloads, landed last cells | 437 and 438 equal byte-for-byte; cell sha256 5fb889c7… / 12a9be38… |
| `08-anchors.txt` | `git show <rev>:SKILL.md \| sed -n`; `grep -c MAX_ATTEMPTS`; intake/mission-control anchors | base 117 = provenance line; base 494-506 = park-disposition; landing 191 = attempts statement; landing 827-848 = EV formula/fail-closed; `MAX_ATTEMPTS` 0/0; corrections present at 89-93 / 55-57 |
| `09-shadowing-source.txt` | `sed -n '279,283p;396,402p' knowledge-meter.py`; `grep -n` | line 282 `b, a = file_at(…)` shadows `a`; line 399 `if a.map_sha256:` |
| `10-fixed-counter-control10.txt`, `tools-km-fixed.py` | 282-284 renamed (`b, a`→`b, atext`), fixed counter on the control-10 scenario | `LIMB M3 FAIL bad_lines=1`, M9/M10 pass, rc=1 |
