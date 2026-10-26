# ExecR37Carry — G8 carry-over limb: live reads, pinned constants, and the invariance the L1 must hold at J

Seat `ExecR37Carry`, round 38, lane `kasegi-shokunin`. Judged on `depth:verifiability`. Receipt only — **there is no landable deliverable** (see §7).

Lane state read at start (read-only): `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` → `700153593eb586c70a6499c8ca225ee4d673bc9b` (round-38 wave-1 spec + dispatch), with three untracked round-38 paths (`.ufo/waves/round-38/wave1.ready`, `wave1.ready.partial`, `.ufo/waves/round-38/wave1/`). Instrument under study: `corpus/instruments/r37-closure.sh`, 1558 lines, sha256 `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` — byte-identical at base `a173b0c2`, r37 judged head `2387dcf6`, the r37 receipt's `export-ref` `9492c77`, and current HEAD `7001535`; identical to the `suite-sha256` recorded in `.ufo/waves/round-37/final-gates/all-gates.txt`.

Scratch: `/fast/scratch/hyaku/kasegi-r38/ExecR37Carry/`, `TMPDIR` bound there, all fixture and `--work` directories under it, removed before yielding. Tooling: none installed or upgraded (no pacman, no network fetch). Every git command against the lane was read-only (`rev-parse`, `show`, `log`, `status --porcelain`, `ls-tree`, `archive`, `cat-file`); the only mutating git commands ran inside `git init` fixtures whose `rev-parse --show-toplevel` was verified equal to the fixture path.

## 1. Every LIVE (non-export) read r37-closure.sh makes

"Live" = read from the lane repository, the lane index, the executing process's own bytes, or the host filesystem — i.e. not answerable from the extracted `export/` tree. Line numbers are `corpus/instruments/r37-closure.sh`.

| # | Line | Read | Limb / why it is live |
|---|---|---|---|
| L1 | 303 | `git -C "$LANE" rev-parse --git-dir` | liveness probe before archive; fails → exit 2 |
| L2 | 305 | `git -C "$LANE" rev-parse --verify --quiet <want>^{commit}` | resolves `--export-ref` against the live object DB |
| L3 | 308 | `git -C "$LANE" archive --format=tar <ref> \| tar -x -C $EXPORT` | the export itself; anchors every "export" read to live bytes |
| L4 | 431 | `git -C "$LANE" cat-file -e <h>^{commit}` (E1) | the 40-hex on/after a `Final lane commit` line must resolve **in the live repo** |
| L5 | 432 | `git -C "$LANE" merge-base --is-ancestor <h> <ref>` (E1) | ancestry in the live object DB (ancestor-or-equal of the exported ref) |
| L6 | 479 | `git -C "$LANE" ls-tree -r --name-only <ref> -- .ufo/waves/round-35/wave1-results.json` (E4) | tracked-at-ref limb |
| L7 | 480 | `git -C "$LANE" ls-files -- .ufo/waves/round-35/wave1-results.json` (E4) | **INDEX read** — cannot be answered from an export at all |
| L8 | 503–505 | `git -C "$LANE" ls-tree -r --name-only <ref>` + two greps (E6) | derives the receipt path from the tree; the filter is `(^|/)\.ufo/waves/round-34/wave1/L1Integration\.md$` minus a leading `corpus/instruments/` |
| L9 | 566 | `git -C "$srepo" rev-parse --git-dir` (E9; `srepo` = `$LANE` by default) | quiescence |
| L10 | 572–573 | `cd "$srepo" && pwd -P`; `git -C "$srepo" rev-parse --show-toplevel` (E9) | lane-root limb: toplevel must equal the physical path |
| L11 | 581 | `git --no-optional-locks -C "$srepo" status --porcelain` (E9) | **exit status is read**; failure ⇒ `status-read=failed`, RED. Untracked files count. |
| L12 | 591 | `cd "$WORK" && pwd -P` (E9) | excludes the run's own work dir from the leftover scan |
| L13 | 599 | `find "$sroot" -mindepth 1 -maxdepth 1 -type d` (E9) | default `$sroot` = `/fast/scratch/hyaku/kasegi-r37` (line 185) |
| L14 | 601 | `git -C "$srepo" rev-parse --verify --quiet HEAD` (E9) | **head-match**: HEAD must equal the exported ref |
| L15 | 629 | `git -C "$LANE" ls-tree -r --name-only <ref> -- corpus/instruments/r37-closure.sh` (E10) | suite tracked at ref |
| L16 | 648 | `git -C "$LANE" cat-file -e <xref>^{commit}` (E10) | `export-ref` in the committed receipt must resolve |
| L17 | 649 | `git -C "$LANE" merge-base --is-ancestor <xref> <ref>` (E10) | ancestor-or-equal, not equality |
| L18 | 215–221 (`suite_digest`) | `sha256sum -- "$SELF"` | digest of the **bytes actually executing**, not the export copy |
| L19 | 272, 279 | `realpath -m -- "$WORK_ARG"`; `cd "$norm" && pwd -P` | work-dir guard: refuses `--work` inside `$LANE` (exit 2) |
| L20 | 287 | `mktemp -d -t r37-closure.XXXXXXXX` | honours inherited `TMPDIR` |
| L21 | 1531 | `LANE=$( cd "$LANE" && pwd -P )` | normalises the lane path once |
| L22 | 1141 | `st_pos E9 "$EXPORT" "$REF_RESOLVED"` (only under `--selftest`) | the E9 **positive** case runs against the live lane (`srepo=$LANE`, `sroot=$SCRATCH_ROOT`) — so `--selftest` inherits the same head/cleanliness requirement |

Live writes: none under the lane. `status` runs with `--no-optional-locks`; the only writes are `$WORK/export` and `$WORK/mut`, both removed on exit (`cleanup`, 262–266) — and a reused `--work` is cleared first (`rm -rf "$EXPORT" "$MUT"`, line 294).

Everything else (E2, E3, E5, E7, E8, E11, E12, E13, E14, and the content limbs of E1/E4/E6/E10) reads only files under `$EXPORT`.

## 2. Round-37-pinned constants

| Check | Constant (line) |
|---|---|
| default lane | `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (184) |
| default scratch root | `/fast/scratch/hyaku/kasegi-r37` (185) |
| check id set | `E1..E14` (186), and E10 re-derives the same set with `seq 1 14` (633) |
| E1 | heading regex `^#{1,4} .*Round[- ]?37([^0-9]|$)` (330, 346); phrase `[Ff]inal lane commit` (333); 40-hex extraction (335); placeholder literals assembled at 425–426 (`filled by the ` + `L1`, `<LANE` + `_HASH>`); the scan runs from the **last** round-37 heading to **EOF** (no stop at the next heading) |
| E2 | `Erratum (round 35)` (452); row regex `^\| depth:density \| 9 \| mean \*\*201\.2\*\*` (453); `201.2` (454) |
| E3 | first-column basenames `r35-defect-closure.sh`, `r36-closure.sh` inside `## …Gates & probes registry…` (468–469, helpers 354–362) |
| E4 | `.ufo/waves/round-35/wave1-results.json` (477) + `.provenance.md` beside it (483) |
| E5 | `.ufo/waves/round-35/claims-erratum-d5.md` (492) |
| E6 | `.ufo/waves/round-34/wave1/L1Integration.md` (504); `Correction (round 35)` (512) |
| E7 | `corpus/QUALITY.md` rows whose 3rd cell starts `supersedes R22` / `supersedes R23` (527–528) |
| E8 | `corpus/lessons/round-36.md` contains `M36` (540) and `source-recheck` (543); `corpus/lessons/round-35.md` must exist (546) and not contain `source-recheck exit 0 on committed bytes` (548) |
| E10 | `.ufo/waves/round-37/final-gates/all-gates.txt` (623); header grammar `all-gates v1`, `export-ref=[0-9a-f]{40}`, `suite-sha256=[0-9a-f]{64}`, `run-utc=` strict UTC (636–640); `E<n> … closed=1` for all 14 with no `closed=0` (656–660); exactly one `closed=14/14 exit=0` (661); 14 `selftest case=E<n>` with `positive=pass`, `verdict=pass`, `mutants=o/n`, `o==n`, and `n` matching `selftest detail=` lines (665–682); exactly one `selftest cases=14 failures=0` (681); cross-run **payload key-set** equality for E1..E9,E11..E14 (683–691); placeholder regex `<(hash\|sha\|digest\|ref\|payload\|N\|n\|id)>\|TODO\|TBD` (692) |
| E11 | last `## …Round[- ]?37…` LOG.md block (393, 401) must carry `Correction (round 37)` (720), `corpus/instruments/r36-fixtures/` (721) and one of `absent\|never committed\|does not exist\|not present` (723) |
| E12 | last round-37 SCORECARD block must carry `c20300df` (745) and `anchor[- ]ancestor` (746) and **not** `Final lane commit: e666d902` (747); `corpus/lessons/round-37.md` must carry `c20300df` (751) and `anchor[- ]ancestor` (752) |
| E13 | `r36-closure.sh` registry rows: type cell exactly `gate` or `probe`, verdict cell matching `2…could-not-evaluate` (762–783) |
| E14 | on the **export's own copy** of r37-closure.sh: the assembled `porcelain:-0` needle = 0, every `status --porcelain` line free of `2>/dev/null` and `|| true`, ≥1 such site, `status-read=failed` present (785–808). Measured payload: `status-read-sites=10, fail-closed-marker=8` |

## 3. Prediction and measurement: does 14/14 survive a round-38 head?

Two fixtures, both `git init` in scratch with verified toplevel:

- **F1 (the prescribed fixture)** — seeded by `git -C <lane> archive a173b0c2 \| tar -x -C D`, then synthetic append-only round-38 edits to `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/lessons/round-37.md`, `PROVINCE.md`, `corpus/README.md`, one commit `fd31fe2a` (fresh repo: **no ancestry**).
- **F2 (ancestry-preserving)** — same `git init` fixture, `git fetch <lane> '+refs/heads/*:refs/heads/*'`, `checkout -B fixture a173b0c2`, the identical append set, one commit `52b7299c` whose parent is base `a173b0c2` (so `2387dcf6`, `9492c77`, `f3246559`, `83975ac` all resolve).

The synthetic append set is a realistic round-38 head: a `## Round 38` SCORECARD section with a `Correction (round 38)` line naming `f3246559…` **without** the phrase `Final lane commit`; a SHONEN evidence bullet; a `## Round 38` LOG entry; a `## Round-38 dispositions` heading in `corpus/lessons/round-37.md`; `Correction (round 38)` paragraphs in `PROVINCE.md` and `corpus/README.md`. All six files are append-only (before/after byte sizes recorded below).

| Run | Command (abbreviated) | Result |
|---|---|---|
| F1 | `r37-closure.sh --lane D --export-ref fd31fe2a --work $S/work-fixture` | `E1 … round37-final-lane-commits=1,bound=0 closed=0`; `E10 … ancestor=0 … closed=0`; `closed=12/14 exit=1` |
| F2 | `r37-closure.sh --lane D2 --export-ref 52b7299c --work $S/work-ancestry` | `E1 … bound=1 closed=1`; `E10 … ancestor=1,digest-match=1,crossrun=1 … closed=1`; **`closed=14/14 exit=0`** |
| F2 selftest | `--selftest --lane D2 --export-ref 52b7299c` | every `selftest case=E<n> positive=pass … verdict=pass`, `selftest cases=14 failures=0`, exit 0 |
| F2 selftest at Y | receipt-only commit `80cc10ae` on top, `--selftest --export-ref 52b7299c` | `selftest case=E9 positive=fail … head-match=0`, `selftest cases=14 failures=1`, exit 1 |
| F2 at Y | plain run, `--export-ref 52b7299c`, HEAD = `80cc10ae` | `E9 … head-match=0 … closed=0` → `closed=13/14 exit=1` |
| live lane | `--lane <lane> --export-ref 7001535` (HEAD) | `E9 … status-dirty=3 … closed=0` → `closed=13/14 exit=1` |
| live lane | `--export-ref 9a10b02` and `--export-ref a173b0c2` (HEAD = 7001535) | `E9 … head-match=0` → `closed=13/14 exit=1` |
| plain run | `r37-closure.sh` | exit 2, `refusing to run against the live worktree: this suite is export-mode only.` |

**Answer:** yes, `14/14` survives an append-only round-38 head — measured on F2 — but only because F2 keeps the *live* history the suite names. The prescribed archive-seeded fixture (F1) goes to `12/14`: E1's bound limb and E10's ancestor limb both need the named historical commits to exist in the repo passed as `--lane`, and a fresh `git init` has no objects beyond its one commit. So the carry-over is not a property of the exported *bytes*; it is a property of **bytes × live history × live worktree state × live index**.

## 4. Which checks depend on live state (dependency classes)

| Class | Checks | Failure mode on a correct round-38 head |
|---|---|---|
| export-only | E2, E3, E5, E7, E8, E11, E12, E13, E14 + content limbs of E1/E4/E6/E10 | none, if the round-37 bytes are untouched |
| ref-scoped live object DB | E1 ancestry, E6 path derivation, E10 suite-at-ref + xref ancestry | red if the named commits are absent (F1) or on a branch not reachable from the lane |
| live **index** | E4 `ls-files` | red if the index lacks `.ufo/waves/round-35/wave1-results.json` (measured: `tracked-ref=1,tracked-index=0` → `closed=12/14`) |
| live **quiescence** | E9 all six limbs | red on any untracked/dirty path, on HEAD≠export-ref, on a first-level directory under `kasegi-r37`, on a broken status read |
| executing bytes | E10 `suite_digest` | red if the executing copy of the suite differs from the committed copy at REF or from the receipt digest |
| live lane in selftest | E9 positive case under `--selftest` | same as E9; measured `failures=1` when HEAD≠export-ref |

## 5. What the L1 must keep true at the judged head J for G8 = `closed=14/14`

Measured preconditions, in the order the suite evaluates them:

1. **Suite bytes unchanged.** `sha256sum corpus/instruments/r37-closure.sh` at J = `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`, and the executing copy has the same digest (E10 `digest-match`, E14 shape, E10 cross-run key sets). Any edit to the r37 suite — even a comment — reds E10 and probably E14.
2. **The round-37 receipt stays as committed.** `.ufo/waves/round-37/final-gates/all-gates.txt` keeps `export-ref=9492c776724e737caf5815fabc98e59ea04830df`, `suite-sha256=0da98e37…`, one `closed=14/14 exit=0`, 14 `E<n> … closed=1` lines and the 14 `selftest case=` lines (E10 `header`, `run-lines`, `recorded-closed`, `selftest-cases`, `selftest-summary`). `9492c77` must remain an ancestor of the r38 ref (it is: J descends from base `a173b0c`, which descends from `9492c77`).
3. **Round-37 SCORECARD section untouched** — `c20300df` + `anchor ancestor` inside it, and no `Final lane commit: e666d902` anywhere inside it (E12). Appending a `## Round 38` section *after* it is safe: `e12_section` stops at the next `## ` heading (measured: `scorecard37-section=1,c20300df=1,anchor-ancestor=1,stale-e666d902=0` on F1/F2).
4. **LOG.md round-37 block untouched** — `Correction (round 37)`, `corpus/instruments/r36-fixtures/`, and a falsity word (E11). Appending a `## Round 38` LOG entry is safe for the same reason (measured `falsity-stated=3`).
5. **`corpus/lessons/round-37.md` keeps** `c20300df` and `anchor ancestor` (E12 lesson limbs; appending a `## Round-38 …` section is safe — measured `lesson-c20300df=5,lesson-anchor-ancestor=2`).
6. **No new 40-hex on a `Final lane commit` line that is not an ancestor of J.** `e1_final_hashes` scans from the **last** round-37 heading to **EOF**, so a `Final lane commit:` line inside the round-38 SCORECARD block is collected too (B1: a bogus 40-hex → `round37-final-lane-commits=2,bound=1` → `closed=13/14`). Naming the real ancestor `f3246559…` on such a line is safe (B2: deduplicated by `sort -u` → `1,bound=1` → `14/14`). **Recommendation:** word the mandatory `Correction (round 38)` line for `f3246559` without the phrase `Final lane commit` (the F1/F2 wording does) — then E1 sees exactly the one round-37 line.
7. **Do not introduce a `Round 37` heading below the round-37 SCORECARD block** (e.g. `### Round-37 correction` inside the round-38 section). It becomes the "last Round-37 heading", the scan window starts there, and if no `Final lane commit` line follows, `round37-final-lane-commits=0` → E1 red (B3, measured `closed=13/14`).
8. **SCORECARD.md must contain neither** `filled by the L1` **nor** `<LANE_HASH>` anywhere, including the new round-38 text (E1 `placeholders`, `lane-hash-markers`, file-wide).
9. **Exactly one** `.ufo/waves/round-34/wave1/L1Integration.md` outside a leading `corpus/instruments/` prefix (E6). A second copy anywhere in the tree — including a fixture under `.ufo/waves/round-38/` — flips the payload key from `path` to `path-candidates`, which reds E6 *and* reds E10 `crossrun` (this is the only text-driven payload-shape branch in the suite).
10. **`.ufo/waves/round-35/wave1-results.json` stays tracked in the export and in the live index**, with `.provenance.md` beside it (E4). Do not stage its deletion, sparsely check it out, or commit with a filtered index (measured `tracked-index=0` → `closed=12/14`).
11. **Quiescence at the moment G8 runs** (E9): the lane worktree must be porcelain-clean — untracked files count, so `.ufo/waves/round-38/wave1.ready`, `wave1.ready.partial` and `wave1/` must be committed or removed (live lane today: `status-dirty=3`); `HEAD` must equal the exported ref (`head-match`); `find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 -maxdepth 1 -type d` must be empty (absent root reads `scratch-root=absent` and is fine; a leftover seat dir reads `scratch-seat-dirs=1` → red); and the repo's toplevel must be the lane root itself (`lane-root`).
12. **Evaluate G8 at REF = HEAD.** With the receipt-only commit Y on top, `--export-ref J` gives `head-match=0` → `closed=13/14` (measured both plain and `--selftest`). So the r38 `all-gates.txt` must record the run made while HEAD was still J, exactly like the round-37 bootstrap. Re-running r38-closure.sh at Y will legitimately print a red G8; only the receipt's recorded J-run is the gate.
13. **If G8 also carries the selftest**, the same head-equality rule applies (E9 positive, line 1141), and at HEAD==REF it prints `selftest cases=14 failures=0` (measured on F2).

## 6. Retained evidence (verbatim)

Instrument identity across refs:

```
$ for r in a173b0c2… 2387dcf6… 9492c77… 7001535…; do git show "$r:corpus/instruments/r37-closure.sh" | sha256sum; done
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  -   (all four refs, identical)
$ sha256sum corpus/instruments/r37-closure.sh
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  corpus/instruments/r37-closure.sh
```

F1 (fresh-history fixture, head `fd31fe2af84b439bbbe354e735e9c56c965c2291`, 1 commit; append-only deltas: SCORECARD 173625→174246, SHONEN 15964→16152, LOG 148994→149332, lesson-37 31704→31844, PROVINCE 10894→11122, README 43629→43846):

```
E1 payload=placeholders=0,lane-hash-markers=0,round37-section=1,round37-final-lane-commits=1,bound=0 closed=0
E9 payload=status-read=ok,status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=1
E10 payload=all-gates=1,suite-file=1,header=1,ancestor=0,digest-match=1,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0 closed=0
closed=12/14 exit=1
```

F2 (ancestry fixture, head `52b7299c2ef5e66bafb6703afc3fe1afa07ec2fd`, parent = base `a173b0c2…`):

```
E1 payload=placeholders=0,lane-hash-markers=0,round37-section=1,round37-final-lane-commits=1,bound=1 closed=1
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=7 closed=1
E3 payload=registry-r35-defect-closure=1,registry-r36-closure=2 closed=1
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=1 closed=1
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=4,names-corrected-line=3,stale-line=0,round35-lesson=1 closed=1
E9 payload=status-read=ok,status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=1
E10 payload=all-gates=1,suite-file=1,header=1,ancestor=1,digest-match=1,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0 closed=1
E11 payload=log37-block=1,correction-marker=1,false-path-named=1,falsity-stated=3 closed=1
E12 payload=scorecard37-section=1,c20300df=1,anchor-ancestor=1,stale-e666d902=0,lesson37=1,lesson-c20300df=5,lesson-anchor-ancestor=2 closed=1
E13 payload=registry-rows=2,single-choice-type=1,exit2-verdict=1 closed=1
E14 payload=suite-file=1,porcelain-default=0,status-read-swallow=0,status-read-sites=10,fail-closed-marker=8 closed=1
closed=14/14 exit=0
selftest: selftest case=E1..E14 positive=pass … mutants=<n>/<n> verdict=pass / selftest cases=14 failures=0 (rc 0)
```

Sensitivity probes, each one commit on top of F2 (`reset --hard` back to `52b7299c` between probes):

```
B1 bogus line, commit 134935a2: E1 … round37-final-lane-commits=2,bound=1 closed=0      -> closed=13/14 exit=1
B2 ancestor  f3246559, commit 66e6b911: E1 … round37-final-lane-commits=1,bound=1 closed=1 -> closed=14/14 exit=0
B3 `### Round-37 correction` last, commit 0603e84f: E1 … round37-final-lane-commits=0,bound=0 closed=0 -> closed=13/14 exit=1
A  receipt-only Y 185aafc2, export-ref 52b7299c: E9 … head-match=0 closed=0            -> closed=13/14 exit=1
E4 staged index deletion: E4 tracked-ref=1,tracked-index=0,provenance-note=1 closed=0  -> closed=12/14 exit=1
E9 untracked file:        E9 status-read=ok,status-dirty=1,… closed=0                 -> closed=13/14 exit=1
E9 corrupt .git/index:    E9 status-read=failed,status-dirty=?,… closed=0; E4 tracked-index=0 -> closed=12/14 exit=1
E9 leftover scratch dir:  E9 … scratch-seat-dirs=1,scratch-root=present closed=0      -> closed=13/14 exit=1
--work inside --scratch-root: E9 scratch-seat-dirs=0,scratch-root=present closed=1    -> closed=14/14 exit=0
reused --work parent:     E9 scratch-seat-dirs=2 (previous run's work dir counts)     -> closed=13/14 exit=1
```

Live lane (read-only; `--work` in scratch):

```
$ git --no-optional-locks -C <lane> status --porcelain
?? .ufo/waves/round-38/wave1.ready
?? .ufo/waves/round-38/wave1.ready.partial
?? .ufo/waves/round-38/wave1/
HEAD 7001535, --export-ref 7001535        -> E9 status-dirty=3,head-match=1  -> closed=13/14 exit=1
HEAD 7001535, --export-ref 9a10b02        -> E9 status-dirty=3,head-match=0  -> closed=13/14 exit=1
HEAD 7001535, --export-ref a173b0c2       -> E9 status-dirty=3,head-match=0  -> closed=13/14 exit=1
$ bash corpus/instruments/r37-closure.sh
r37-closure: refusing to run against the live worktree: this suite is export-mode only.   (exit 2)
```

## 7. Deliverable

None. This item is receipt-only analysis: it lands no bytes into the lane. The findings above are inputs to the r38 G8 limb design (and to the L1's final commit hygiene), not landable prose. No file was written outside this receipt and the scratch dir.

## 8. Risks and blockers

- **Live-state dependence is structural, not a defect to fix here.** G8 cannot be made export-only without editing the r37 suite (which would red E10 `digest-match`). The L1 should therefore treat G8 as a *quiescence-coupled* limb and sequence it exactly as round-37 did: commit everything, run while HEAD == REF == J, then commit only the receipt.
- **Untracked round-38 artifacts are the sharpest hazard.** At filing time the lane has three untracked paths and the r37 E9 limb counts them; any seat receipt left uncommitted at the G8 run reds the carry-over. Residue in `/fast/scratch/hyaku/kasegi-r37` (including a *previous* `--work` directory under that root) has the same effect.
- **Payload-shape coupling.** E6's `path-candidates` branch is the only text-driven payload key change; a stray duplicate `…/round-34/wave1/L1Integration.md` reds two checks at once (E6 and E10 `crossrun`). Worth a pre-flight `git ls-tree -r --name-only <ref> | grep -c '/\.ufo/waves/round-34/wave1/L1Integration\.md$'` (= 1, excluding `corpus/instruments/`).
- **My scratch dir** `/fast/scratch/hyaku/kasegi-r38/ExecR37Carry/` is removed before yield, so it is not a G6/G8 residue.
