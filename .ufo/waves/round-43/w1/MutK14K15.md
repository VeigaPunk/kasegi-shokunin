# MutK14K15 — mutation battery for the two new narrative limbs (K14, K15)

- seat: `MutK14K15`, role mutation-tester, leaf (no subagent dispatch)
- round: kasegi-shokunin round 43 (hyaku run 11, one v2 wave), base `ab98fac9dce87130bc4f66de89e30650d63943dc`
- frozen claims read first and never edited: `.ufo/waves/round-43/claims.json` (C1, axis depth:verifiability; K14 = RD42-1 corrections-literal, K15 = RD42-2/3 wave-dispatch narrative)
- scratch: `/fast/scratch/hyaku/kasegi-r43/MutK14K15` (2.0 G, removed before yield; see §8)
- tooling installed/upgraded: **none** (no pacman — host-wide pause; nothing was needed). No writes outside the scratch dir and this receipt.
- disk guard before the heavy pass: `/dev/nvme1n1p2 804G 204G 600G 26% /fast`; `disk-guard.sh status` → `/fast/scratch/hyaku 29% 577.9G` free.
- deliverables: **receipt-only item** — this file is the only wave-dir write; the item names no byte-exact deliverable file. All patch texts and outputs are inline below.

## 0. Verdict summary

| mutant | limb semantic removed | battery (fixture trees) | committed graded selftest | verdict |
|---|---|---|---|---|
| K14-M1 | stale-literal comparison dropped | base 0→1 (flip) | `verdict=fail`, `mutant:accepted;shape:accepted` | **killed** |
| K14-M2 | supersede marker accepted from **any** record file | `cross` 0→1 (flip) | `verdict=pass` — same line as pristine | **SURVIVOR (defect)** |
| K14-M3 | supersede marker naming not checked | `gen` 0→1 (flip) | `verdict=pass` — same line as pristine | **SURVIVOR (defect)** |
| K15-M4 | a missing results file treated as present | base 0→1 (flip) | `verdict=fail`, `mutant:accepted;shape:accepted` | **killed** |
| K15-M5 | seat-count comparison ignored | `mismatch` 0→1 (flip) | `verdict=pass` — same line as pristine | **SURVIVOR (defect)** |

Pristine baselines used for every comparison: K14 → base `closed=0`, `pos` `closed=1`; K15 → base `closed=0`, `pos` `closed=1`; graded selftest → `K14 … verdict=pass` and `K15 … verdict=pass` at the Y-like tree (§5). No baseline failure is counted as a kill.

**Independent blocking finding (not a mutant):** the round-43 narrative deliverables as landed make **K15 red at Y**. `ScribeLogEntry.log-entry.md:128` and `ScribeLessonDraft.round-43-lesson.md:12` assert `kasegi-r43-hyaku` **73 seats dispatched**, and no `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` exists (nor `hyaku/` receipt dir). On a byte-exact Y-like tree K15 prints `payload=sentences=7,unbacked=2,superseded=3,mismatch=0 closed=0`. Committing the 73-seat results artifact closes it: `unbacked=0 … closed=1`. Evidence and both runs in §6 F5.

## 1. Artifacts under test (bytes actually graded)

| path | sha256 | mtime (UTC) |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecK14Corrections.sh` | `4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c` | 2026-10-28T13:50 |
| `.ufo/waves/round-43/w1/ExecK15WaveNarrative.sh` | `14a195b1eb7ec61550bf4938f62ae7856dbae0c1a49dc7aba078f7b97304e93a` | 2026-10-28T13:50 |
| graded runner `.ufo/waves/round-43/w1/ExecSelftest19.sh` | `d2c947b4a5004d49f9677479f6142a10b1d796f638da3fd3481863ffb5a11848`; 999 lines, mtime 13:49 (stable through every run below) | — |
| base export | `git -C <lane> archive ab98fac9dce87130bc4f66de89e30650d63943dc` (8384 files) | — |

Cross-check after the runs: the integrator's staged copies `corpus/instruments/r43-limbs/k14-corrections.sh` and `k15-wave-narrative.sh` (working tree, 14:03) hash-match the two tested files above (`4a4945b0…`, `14a195b1…`), so the bytes that will land are the bytes mutated here.

Revision note (honesty): the K14 limb was re-delivered by its owner at 13:50 (`9fb97b4c…` → `4a4945b0…`, 174 → 202 lines, the R41 evidence rule rewritten from a defect-token list to fence/`mutant=`/`live=` modes). My first pass ran against `9fb97b4c…`; **every observation reported here was re-derived from a fresh archive against `4a4945b0…` and `14a195b1…`**, and the earlier pass is not cited. My own scratch `export-base` was also contaminated mid-run by in-place writes through `cp -al` hardlinks (scratch only, no lane byte touched); I rebuilt all fixtures from a second archive with `cp -a --reflink=auto` (CoW) and re-ran the full battery. §3–§5 are the clean, CoW-isolated pass.

## 2. Method

One limb at a time, never the tree: each mutant is a copy of the **landed** limb with exactly one semantic removed, carried in scratch. Pristine bytes are never written (restoration evidence §7). Each mutant gets `bash -n` on the file and `python3 -m py_compile` on the extracted heredoc, then the same two detectors as pristine:

**Detector A — limb-level fixture battery** (a reduced export tree per case, built from the base archive; the check is sourced and called exactly as the suite calls it):

```
$ . <limb>; check_k14 <tree>      # prints one payload line, returns 0|1
$ . <limb>; check_k15 <tree>
```

**Detector B — the committed graded selftest**, i.e. the shipped runner's own K14/K15 case (positive tree, committed-defect tree, duplicated-shape tree, payload-match, isolation):

```
$ bash .ufo/waves/round-43/w1/ExecSelftest19.sh \
    --export <Y-like> --work <scratch>/… --scratch-root <scratch> \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --base-ref ab98fac9dce87130bc4f66de89e30650d63943dc \
    --cases K14 --check-cmd '. <limb>; check_k14 "$2"'
```

**Y-like tree** = base archive + the three landed scribe correction blocks (`ScribeCorrections.scorecard.txt`, `.log.txt`, `.lesson42.txt`, appended byte-exact) + the committed selftest's own positive lines (`k14_positive`, `k15_positive`, appended with a blank separator). This is the smallest tree that carries the narrative state Y will carry; K14 reads only `SCORECARD.md`/`LOG.md`/`SHONEN.md`, K15 only `LOG.md` + `corpus/lessons/*.md` + `.ufo/waves/round-<NN>/…-results.json`, so the simulation is faithful for these two checks. Pristine at that tree: `K14 … closed=1`, `K15 … closed=1` (§5).

## 3. Fixtures and pristine behaviour

| fixture | construction (from the base archive) | expected | pristine measured |
|---|---|---|---|
| `base` | unmodified `ab98fac9` export | K14 0, K15 0 | K14 `stale=1 closed=0`; K15 `unbacked=3 closed=0` |
| `pos` | + the three landed scribe correction blocks | 1, 1 | K14 `superseded=2 closed=1`; K15 `superseded=3 closed=1` |
| `gen` | + a `Correction (round 43)` on `SCORECARD.md` that names no literal | K14 0 | `stale=1 closed=0` |
| `cross` | + the SCORECARD correction appended to `LOG.md` (wrong file) | K14 0 | `stale=SCORECARD.md:1634`, `superseded=LOG.md:1808`, `closed=0` |
| `anyfile` | + a correct-value `corrections=34` line in `LOG.md` | K14 0 | `stale=1 closed=0` |
| `mismatch` | + `.ufo/waves/round-42/{wave2,kasegi-r42-falsify}-results.json` at `seats=35` (sentence says 36) | K15 0 | `mismatch=3 closed=0` |
| `matched` | same two artifacts at `seats=36` (positive evidence control) | K15 1 | `unbacked=0,mismatch=0 closed=1` |
| `selftest-pos-base` | base + the committed `k15_positive` lines only | — (documents F4) | `unbacked=2,superseded=1 closed=0` |
| `y-like` | `pos` + committed `k14_positive`/`k15_positive` lines | 1, 1 | K14 `closed=1`; K15 `closed=1` |
| `y-like-full` / `y-direct` | `pos` + landed `ScribeLogEntry` appended to `LOG.md` + landed `ScribeLessonDraft.round-43-lesson.md` at `corpus/lessons/round-43.md` | — (F5) | K15 `unbacked=2 closed=0` |
| `y-like-full-art` / `y-direct-art` | + `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` (`seats=73`, 73 results) | — (F5 remedy) | K15 `unbacked=0 closed=1` |

Pristine verbatim (clean pass):

```
== limb=ExecK14Corrections.sh tree=base
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
STATUS=1
== limb=ExecK14Corrections.sh tree=pos
K14 superseded=SCORECARD.md:1634 corrections=33 live=36
K14 superseded=SCORECARD.md:1661 corrections=33 live=36
K14 payload=literals=3,stale=0,superseded=2,live=corrections=36,groups=4 closed=1
STATUS=0
== limb=ExecK15WaveNarrative.sh tree=base
K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
STATUS=1
== limb=ExecK15WaveNarrative.sh tree=pos
K15 payload=sentences=5,unbacked=0,superseded=3,mismatch=0 closed=1
STATUS=0
```

## 4. Mutants — patch text, proof, kill case

Each row is one limb semantic. Hashes are of the mutated copies in scratch (not deliverables).

### K14-M1 — drop the stale-literal comparison (`0e3ed4f2627e5e782345df65f267b666767ee0f02acd609351675cce6b32857a`)

```diff
--- a/ExecK14Corrections.sh
+++ b/k14-m1.sh
@@ -173,7 +173,7 @@
                 key, val = m.group(1), int(m.group(2))
                 lit = "%s=%d" % (key, val)
                 literals += 1
-                if val == live[key]:
+                if True:  # MUTANT K14-M1: stale-literal comparison dropped
                     continue
```

Kill case (base — the committed r42 defect bytes):

```
$ . k14-m1.sh; check_k14 base
K14 payload=literals=2,stale=0,superseded=0,live=corrections=34,groups=4 closed=1
STATUS=0
```

Pristine base: `stale=1 … closed=0`. The mutant closes the tree that carries the evaluator's own counter-defect → **killed**.

### K14-M2 — accept a literal's supersede marker found in any file (`10c414462da675c1ecd70ac17cc7f539fb6d2b58fa33b6a192f7719b9d48033c`)

```diff
@@ -157,8 +157,10 @@
     for rec in records:
         text = ns["read_text"](os.path.join(TREE, rec))
         rows = ns["fence_scan"](text)
-        markers = [(int(rnd), ln, line)
-                   for (rnd, ln, line) in ns["correction_lines"](text, MARKER_ROUND)]
+        markers = [(int(rnd), ln, line)            # MUTANT K14-M2: any file
+                   for _r in records
+                   for (rnd, ln, line) in ns["correction_lines"](
+                       ns["read_text"](os.path.join(TREE, _r)), MARKER_ROUND)]
```

Kill case (`cross` — the correction lives in `LOG.md`, the stale literal in `SCORECARD.md`; the limb's contract says the marker must be "later in the SAME file"):

```
$ . k14-m2.sh; check_k14 cross
K14 superseded=SCORECARD.md:1634 corrections=33 live=35
K14 superseded=LOG.md:1808 corrections=33 live=35
K14 payload=literals=3,stale=0,superseded=2,live=corrections=35,groups=4 closed=1
STATUS=0
```

Pristine `cross`: `stale=1 … closed=0` (it supersedes only the LOG-side marker and keeps SCORECARD's literal stale). Mutant accepts → **killed by the battery**, but see F1: the committed graded selftest does **not** kill it.

### K14-M3 — skip the supersede marker's naming check (`c1cf82414096a3517249eaa651be8c0b16bb8b7ee26296e811e503d4fdecac7b`)

```diff
@@ -177,7 +177,7 @@
                 excused = False
                 for _rnd, mline, mtext in markers:
-                    if mline > lineno and whole(mtext, lit):
+                    if mline > lineno:  # MUTANT K14-M3: marker naming skipped
                         excused = True
```

Kill case (`gen` — a round-43 correction that names no literal):

```
$ . k14-m3.sh; check_k14 gen
K14 superseded=SCORECARD.md:1634 corrections=33 live=35
K14 payload=literals=2,stale=0,superseded=1,live=corrections=35,groups=4 closed=1
STATUS=0
```

Pristine `gen`: `stale=1 … closed=0`. Mutant accepts a blanket marker → **killed by the battery**, survivor of the graded selftest (F2).

### K15-M4 — treat a missing results file as present (`b730c6a400865e78fcd8c4d994f84fcdf1cd601f48df679af87116071660ca12`)

```diff
@@ -315,6 +315,8 @@
     if claim['name']:
         artifacts.append(os.path.join(round_dir, '%s-results.json' % claim['name']))
+    if artifacts and not any(os.path.isfile(p) for p in artifacts):  # MUTANT K15-M4
+        return 'backed', artifacts[0], {'state': 'ok', 'seats': claim['stated']}
     present = [(p, read_artifact(p, claim['round']))
                for p in artifacts if os.path.isfile(p)]
```

Kill case (base — no artifact exists for the asserted wave):

```
$ . k15-m4.sh; check_k15 base
K15 payload=sentences=5,unbacked=0,superseded=0,mismatch=0 closed=1
STATUS=0
```

Pristine base `unbacked=3 closed=0` → **killed**. (It still rejects a *present-but-wrong* artifact: on `mismatch` it prints `mismatch=3 closed=0`, which is why the F5 remedy is not closed by this mutant.)

### K15-M5 — ignore the seat-count comparison (`de05ce1d808c804554b6b9a6947d1a470c912375324e481750e7d7066e3e56b8`)

```diff
@@ -318,8 +318,7 @@
     for path, info in present:
-        if info['state'] == 'ok' and (claim['stated'] is None
-                                      or info['seats'] == claim['stated']):
+        if info['state'] == 'ok':  # MUTANT K15-M5: seat-count comparison ignored
             return 'backed', path, info
@@ -335,7 +334,7 @@
         count = receipt_count(directory)
         if count is None or count == 0:
             continue
-        if claim['stated'] is None or count == claim['stated']:
+        if True:  # MUTANT K15-M5: receipt seat-count comparison ignored
             return 'backed', directory, {'state': 'receipts', 'seats': count}
```

Kill case (`mismatch` — artifacts present with `seats=35` while every sentence states 36):

```
$ . k15-m5.sh; check_k15 mismatch
K15 payload=sentences=5,unbacked=0,superseded=0,mismatch=0 closed=1
STATUS=0
```

Pristine `mismatch`: `mismatch=3 closed=0`. Mutant accepts → **killed by the battery**, survivor of the graded selftest (F3).

Syntax proof for all five (run in scratch):

```
$ for f in k14-m1.sh k14-m2.sh k14-m3.sh k15-m4.sh k15-m5.sh; do bash -n "$f" && echo "$f: bash -n ok"; done
k14-m1.sh: bash -n ok
k14-m2.sh: bash -n ok
k14-m3.sh: bash -n ok
k15-m4.sh: bash -n ok
k15-m5.sh: bash -n ok
$ for f in /tmp/heredoc-*.py; do python3 -m py_compile "$f" && echo "python3 -m py_compile $f: ok"; done
python3 -m py_compile /tmp/heredoc-mut2-k14-m1.sh.py: ok
python3 -m py_compile /tmp/heredoc-mut2-k14-m2.sh.py: ok
python3 -m py_compile /tmp/heredoc-mut2-k14-m3.sh.py: ok
python3 -m py_compile /tmp/heredoc-mut2-k15-m4.sh.py: ok
python3 -m py_compile /tmp/heredoc-mut2-k15-m5.sh.py: ok
```

(`py_compile` is applied to the `K14_PY`/`K15_PY` heredoc body extracted verbatim from each mutant, so a mutated limb cannot be syntax-dead and still be reported as a survivor.)

## 5. Graded selftest at the Y-like tree (verbatim)

```
== case=K14 limb=pristine
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=1 failures=0
rc=0
== case=K14 limb=m1
selftest case=K14 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest cases=1 failures=1
ExecSelftest19: K14 red: mutant:accepted;shape:accepted
rc=1
== case=K14 limb=m2
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=1 failures=0
rc=0
== case=K14 limb=m3
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=1 failures=0
rc=0
== case=K15 limb=pristine
selftest case=K15 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=1 failures=0
rc=0
== case=K15 limb=m4
selftest case=K15 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest cases=1 failures=1
ExecSelftest19: K15 red: mutant:accepted;shape:accepted
rc=1
== case=K15 limb=m5
selftest case=K15 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=1 failures=0
rc=0
```

Off-claim record (same runner, export = base archive), kept because it bounds how the case can be exercised:

```
== case=K14 limb=pristine tree=base
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
rc=0
== case=K15 limb=pristine tree=base
selftest case=K15 mutants=2/2 positive=fail payload-match=1 verdict=fail
rc=1
ExecSelftest19: K15 red: positive:closed=0
```

**Integrated-suite spot check (read-only, after the wave's C1 commit).** The integrator's commit `ffe197d` carries `corpus/instruments/r43-closure.sh` plus `r43-limbs/k14-corrections.sh` and `k15-wave-narrative.sh` that hash-match the two files I mutated (§1). Running the committed suite over that same ref reproduces my limb-level results inside the real instrument, and confirms the ref does **not** yet carry the round-43 narrative that triggers F5:

```
$ bash corpus/instruments/r43-closure.sh --export-ref ffe197d --work <scratch>/w --scratch-root <scratch>
K14 payload=literals=3,stale=0,superseded=2,live=corrections=36,groups=4 closed=1
K15 payload=sentences=5,unbacked=0,superseded=3,mismatch=0 closed=1
closed=15/19 exit=1
```

Out-of-scope observation for the L1 (not my item, reported because a leaf saw it): in that same run `K16 payload=limb=error,file=k16-placeholder.sh closed=0` and `K18 payload=limb=error,file=k18-transcript.sh closed=0`, and `K8` is red because no receipt is committed at that ref. The summary does not follow from those lines: the run prints **16** `closed=1` payload lines (all except K8, K16, K18) but the last line is `closed=15/19 exit=1`; the committed script computes `CLOSED=$((TOTAL - OPEN))` (`git show HEAD:corpus/instruments/r43-closure.sh:351`), so `OPEN` counted 4 while only three checks printed `closed=0` — one failure path appears to be counted twice. That is the suite's own counter, the K16/K17 and K18/K19 seats' surface, and the working tree already carries a further edit to `r43-closure.sh` at the time of writing; I did not touch it.

## 6. Findings

**F1 (defect, coverage) — K14-M2 survives the graded K14 case.** Accepting a supersede marker from any record file is invisible to the committed case: its mutant tree is the committed r42 bytes (no round-43 marker exists at all) and its shape tree duplicates that same defect, so `positive` and both mutants are unchanged. The frozen kill rule is not violated (the mutants still reject the committed defect), but `selftest cases=19 failures=0` does **not** mean the K14 check would reject a marker taken from the wrong file. Kill case needed: a tree where the literal is stale in `SCORECARD.md` and the naming correction lives in `LOG.md` (§4).

**F2 (defect, coverage) — K14-M3 survives the graded K14 case.** Same mechanism: the committed mutant has no round-43 marker, so "a marker exists" and "a marker names the literal" are indistinguishable in that case. Kill case needed: a general `Correction (round 43)` that names no literal (§4).

**F3 (defect, coverage) — K15-M5 survives the graded K15 case.** The K15 batteries are built from the committed bytes, where the evidence is *absent*; the seat-count rule only bites on a present-but-wrong artifact, and the shape mutant (`36 seats dispatched` → `64 seats dispatched`) stays unbacked rather than mismatched. So the comparison the check exists for is never exercised by its own case. Kill case needed: `.ufo/waves/round-42/{wave2,kasegi-r42-falsify}-results.json` at 35 seats against a 36-seat sentence (§4).

**F4 (note, not a contract violation) — the K15 positive fixture is not self-sufficient on a base-derived tree.** `k15_positive`'s lesson correction says "the wave-2 seat counts … RD42-3 never-true; wave 2 was handed off…" — it carries neither the wave token `kasegi-r42-falsify` nor a round token (`RD42-3` does not match the limb's round regex), so the two `wave 2 dispatched 36 seats` claims stay unbacked:

```
$ . ExecK15WaveNarrative.sh; check_k15 selftest-pos-base
K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 payload=sentences=5,unbacked=2,superseded=1,mismatch=0 closed=0
```

One blank-line-separated correction naming the wave + `r42` closes it, proving the defect is the fixture text, not the limb:

```
$ . ExecK15WaveNarrative.sh; check_k15 selftest-pos-repaired
K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 superseded-by=1808
K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 superseded-by=153
K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 superseded-by=153
K15 payload=sentences=5,unbacked=0,superseded=3,mismatch=0 closed=1
```

The claim runs `--selftest --export-ref Y`, and at the Y-like tree the case passes (§5), so this is a note: the K15 case cannot be graded at base the way K14 can, and a reviewer who sanity-runs the selftest at base will see `positive:closed=0` (not a K15 limb defect). At Y the scribe corrections supply the missing naming.

**F5 (blocking at Y, independent of the mutants) — the landed round-43 narrative asserts the round-43 wave without its results artifact.** `ScribeLogEntry.log-entry.md:128` (`- Wave shape: one v2 wave \`kasegi-r43-hyaku\`, 73 seats dispatched …`) will be appended to `LOG.md`, and `ScribeLessonDraft.round-43-lesson.md:12` (`wave 1 \`kasegi-r43-hyaku\` dispatched 73 seats`) lands at `corpus/lessons/round-43.md`. `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` does not exist, and the receipts live in `w1/`, which K15 does not consult for a named wave. Byte-exact landing order (`cat` append, no synthetic separators):

```
$ . ExecK15WaveNarrative.sh; check_k15 y-direct     # base + scribe corrections + landed LOG entry + landed lesson
K15 detail=LOG.md:1936 wave=kasegi-r43-hyaku round=43 stated-seats=73 unbacked=no-evidence
K15 detail=corpus/lessons/round-43.md:12 wave=kasegi-r43-hyaku round=43 stated-seats=73 unbacked=no-evidence
K15 payload=sentences=7,unbacked=2,superseded=3,mismatch=0 closed=0
STATUS=1
```

Remedy, measured on a copy of the same tree: commit the wave's results artifact.

```
$ mkdir -p y-direct-art/.ufo/waves/round-43
$ python3 - <<'PY'
import json
n = 73; seats = [{"name": "Seat%03d" % i, "status": "ok"} for i in range(1, n + 1)]
open("y-direct-art/.ufo/waves/round-43/kasegi-r43-hyaku-results.json", "w").write(
    json.dumps({"lane": "kasegi", "round": 43, "wave": "kasegi-r43-hyaku",
                "seats": n, "results": seats}) + "\n")
PY
$ . ExecK15WaveNarrative.sh; check_k15 y-direct-art
K15 payload=sentences=7,unbacked=0,superseded=3,mismatch=0 closed=1
STATUS=0
```

Consequences for C1 as frozen: at Y, with these two files landed and no artifact, K15 prints `closed=0` → `closed=19/19` and `selftest … failures=0` both fail the claim. The honest fixes are (a) commit `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` with `seats` 73 and 73 results in the same commit as the narrative (the L1 has the wave's real results when the run completes), or (b) do not assert the dispatch in `LOG.md`/the lesson until that artifact is part of the tree. A `never-true` correction is **not** honest here: the wave did run. `K14` is unaffected at the same tree (`closed=1`, §3).

## 7. Restoration evidence

Pristine bytes were never written: every mutant is a `cp` into scratch, and the graded inputs are read-only. Hash check after the full battery, against the values read at the start of the clean pass:

```
$ sha256sum .ufo/waves/round-43/w1/ExecK14Corrections.sh .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh
4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c  …/ExecK14Corrections.sh
14a195b1eb7ec61550bf4938f62ae7856dbae0c1a49dc7aba078f7b97304e93a  …/ExecK15WaveNarrative.sh
```

Identical to §1 (the K14 revision landed before my clean pass; it did not move again: mtime 13:50, current 17:01Z). "Restored" behaviour is the pristine run reproduced after the mutant runs and equals the pre-mutation run byte for byte:

```
== K14 base (pristine, after the battery)
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
== K15 base (pristine, after the battery)
K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
```

## 8. Scratch cleanup

All work lived under `/fast/scratch/hyaku/kasegi-r43/MutK14K15` (exports, fixtures, mutant copies, `res/`, `res2/` transcripts). Removed before yield:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r43/MutK14K15
$ ls -d /fast/scratch/hyaku/kasegi-r43/MutK14K15 2>&1
ls: cannot access '/fast/scratch/hyaku/kasegi-r43/MutK14K15': No such file or directory
```

No lane byte other than this receipt was written; no fleet-root, sibling-lane or `shokuknow` write; no mutating git/jj command (only `git archive`, `git cat-file` via the selftest, `rev-parse`); no PATH directory touched; no host service restarted.

## 9. Limits

- The Y-like tree is the narrative state Y must carry, not Y itself (Y contains the round's instruments and corpus additions too). For K14/K15 the graded inputs are exactly the three records, `LOG.md` + `corpus/lessons/*.md` and the results artifacts, so the tree is faithful for these checks; the L1 must still run the real `--selftest --export-ref Y`.
- The graded runner was the delivered `ExecSelftest19.sh` at 13:49 (`d2c947b4…`, 999 lines); if it is re-delivered with different K14/K15 builders, F1–F3 should be re-measured against the new bytes with the same five mutants.
- F5's premise is the current content of the two scribe deliverables; if the L1 edits either block before landing (e.g. drops "dispatched" or adds the results path as evidence), re-run the `y-direct` case.
