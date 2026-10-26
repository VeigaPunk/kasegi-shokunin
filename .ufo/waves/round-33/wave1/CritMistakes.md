# CritMistakes — attack on the round-33 mistake-mining (M33-1 able-to-fail, wave sweep coverage)

Seat: `CritMistakes` (leaf critic; no subagent dispatch, no background jobs, no own swarm).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`;
freeze `6e55c8d`; integration HEAD measured `9f98488`. Answering model actually run on:
`opencode-go/deepseek-v4.1-flash` (config route; this seat passed no model).
Landing: this receipt is the only file I wrote in the lane. No git/jj mutation, no gate run, no
network fetch (the two live-drift captures I relied on are `wave1/ScoutLiveDrift.md`'s, not mine).
Tooling installed: none. Scratch: `$HYAKU_SCRATCH/kasegi-r33/CritMistakes` (`HYAKU_SCRATCH`
unset → `/fast/scratch/hyaku`), removed at §6. Every mutation below ran on scratch copies of
committed bytes; the lane tree was only read.

## 0. Subjects and digests (quiescent at measurement)

| Subject | Digest |
|---|---|
| `wave1/ExecErratumCheck.md` (the subject of item 1) | `2f67a145f26b62a98b009e7adcfa278e55ab2b15d06cb9ed0b5d4df81cb50eef` |
| closure check extracted from it (`§1` fenced block) | `438709fdfa82ef5d58ee432f4c1f8152166f64f0454c31f30eb62b17b8712895`, 119 lines, `bash -n` exit 0 |
| `corpus/source-snapshots/round-32/manifest.json` (committed at `9f98488`, worktree identical) | `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774` |
| `corpus/instruments/capture-binding-check.py` (final generation) | `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` |
| `corpus/lessons/round-33.md` (subject of item 2), mtime `01:53:33 -0300` | `120937c6b6d19e4b49e44bf3ea7314976b8f9c191305519d08680196123c9fb2` |

Script extraction is byte-exact against the hash the receipt claims for its own run copy:

```
$ python3 - <<'PY'   # extract the ```sh block from ExecErratumCheck.md §1, hash it
... (re.search(r'```sh\n(#!/usr/bin/env bash\n.*?)\n```', text, re.S))
PY
sha256=438709fdfa82ef5d58ee432f4c1f8152166f64f0454c31f30eb62b17b8712895 lines=119
$ bash -n "$S/closure-final.sh" ; echo bash_n_exit=$?
bash_n_exit=0
```

## 1. Item (1) — re-running `ExecErratumCheck`'s closure-check proof

### 1.1 The three cases the item names

Fixtures are lane-shaped roots (`<root>/corpus/source-snapshots/round-32/…`) copied from the
**committed** round-32 dir (`git archive 9f98488`), so the green case uses the landed manifest,
not a worktree draft. `A` = manifest removed; `B` = as committed; `C` = committed copy, manifest
deleted after a green run (`rm -f …/manifest.json`).

```
$ bash "$S/closure-final.sh" --root "$S/a_nomanifest" --checks manifest ; echo exit=$?
CHECK round-32-manifest FAIL reason=manifest-absent dir=…/a_nomanifest/corpus/source-snapshots/round-32 captures=S049.txt,S050.txt
CLOSURE checks=1 failed=1 exit=1
exit=1
$ bash "$S/closure-final.sh" --root "$S/b_withmanifest" --checks manifest ; echo exit=$?
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S049.txt,S050.txt
CLOSURE checks=1 failed=0 exit=0
exit=0
$ bash "$S/closure-final.sh" --root "$S/c_deleted" --checks manifest ; echo exit=$?     # after rm
CHECK round-32-manifest FAIL reason=manifest-absent dir=…/c_deleted/corpus/source-snapshots/round-32 captures=S049.txt,S050.txt
CLOSURE checks=1 failed=1 exit=1
exit=1
```

| case | exit | check line |
|---|---|---|
| A no manifest | **1** | `FAIL reason=manifest-absent … captures=S049.txt,S050.txt` |
| B committed manifest | **0** | `PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S049.txt,S050.txt` |
| C manifest deleted after green | **1** | `FAIL reason=manifest-absent …` |
| live lane, both checks | **0** | `PASS …` + `round-32-log PASS count=1 line=1593`, `CLOSURE checks=2 failed=0 exit=0` |
| committed integration bytes (`git archive 9f98488`) | **0** | same two PASS lines; manifest sha `6e4e719a…` |

**The three named cases reproduce exactly.** I also re-derived two of the receipt's other claims on
scratch bytes: the base-tree root (`git archive 690b69d corpus/source-snapshots/round-32 LOG.md`)
→ `FAIL reason=manifest-absent` + `FAIL reason=count-0`, `CLOSURE checks=2 failed=2 exit=1`; and the
content mutant that drops `S049.fetched_utc` → `FAIL … fetched_utc=1 url_exact=2
reason=no-fetched_utc:S049`, exit 1. §1's "121 lines" I saw in the pre-final revision is corrected
to "119 lines" in both places of the landed receipt, and 119 matches the bytes.

### 1.2 Counterexample — the able-to-fail set has a zero-escape on the capture-existence limb

`m1` is the *mirror* of M33-1: a `round-32` snapshot dir that carries the manifest and **none** of
the captures. `m5` keeps `S050.txt` but drops the file record `S049` names. `m4` replaces
`S049.txt` with 18 bytes (`sha256 e6f92877…7a06`, not the manifest's `962a451a…`). All three are
built from committed `9f98488` bytes; `m1`/`m5` carry the committed 50-row `corpus/SOURCES.md` so
the C1 instrument can be run against the real registry.

```
$ ls "$S/head_nocaptures/corpus/source-snapshots/round-32"
manifest.json
$ bash "$S/closure-final.sh" --root "$S/head_nocaptures" --checks manifest ; echo exit=$?
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=none
exit=0
$ python3 corpus/instruments/capture-binding-check.py --root "$S/head_nocaptures" ; echo exit=$?
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=2 with_url=2 with_fetched_utc=2 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
records=2 bound=2 unbound=0
exit=0
$ ls "$S/head_pathmissing/corpus/source-snapshots/round-32"        # record S049's path file gone
S050.txt  manifest.json
$ bash "$S/closure-final.sh" --root "$S/head_pathmissing" --checks manifest ; echo exit=$?
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S050.txt
exit=0
$ python3 corpus/instruments/capture-binding-check.py --root "$S/head_pathmissing" ; echo exit=$?
records=2 bound=2 unbound=0
exit=0
$ bash "$S/closure-final.sh" --root "$S/head_corrupt" --checks manifest ; echo exit=$?   # m4
CHECK round-32-manifest PASS records=2 ids=S049,S050 fetched_utc=2 url_exact=2 captures=S049.txt,S050.txt
exit=0
$ python3 corpus/instruments/capture-binding-check.py --root "$S/head_corrupt" ; echo exit=$?
records=2 bound=2 unbound=0
exit=0
```

Why this is a defect of the *fix* rather than of the frozen claim:

- The closure check's own PASS line prints the fact that convicts it — `captures=none`,
  `captures=S050.txt` — and never acts on it. `find … ! -name manifest.json` is computed for
  reporting only; no branch tests it (`closure-final.sh`, `check_manifest`).
- QUALITY **R20** (landed this round) states the criterion as "ships its `manifest.json` in the same
  round and the same commit that adds its captured files" (`corpus/QUALITY.md:169`). The
  capture-existence half of that sentence has no runnable check: `m1` is R20-violating and green.
  R15 requires an open defect's closure to be runnable; R18 requires "no count-zero escape".
- `wave1/ExecErratumCheck.md:316` heads its control section "ABLE-TO-FAIL — the check can go red on
  **every failure mode**". Five modes are measured there (absent manifest, base tree, no
  `fetched_utc`, non-contract url, unparseable JSON); the inverse-commit mode (`m1`) and the
  path-missing mode (`m5`) are not, and both are green.
- The instrument shares the blindness (`m1`/`m5`/`m4` all `bound=2 unbound=0`), which the lesson
  already records as a Gate caveat ("C1 binds manifest metadata to registry text, not bytes to
  captures", `corpus/lessons/round-33.md` § Gate caveats, citing `CritC1Kill` H1–H3 and
  `ExecCaptureBinding.md` §8 item 1). The *closure check* is a second authority over the same
  surface and is **not** covered by that caveat, which speaks only of the instrument.

Verdict on item 1: the able-to-fail demonstration is **sound and reproducible for the three cases
the item names** and for the base-tree and content-mutant cases; it is **incomplete for the
capture-existence limb**, and the §6 heading overstates what was shown. Fixable defect, not a
tradeoff: the data does not need to move — all 40 records already carry `path` + `sha256`
(`ExecCaptureBinding.md` §8 item 1 measured `path_missing=0 sha_or_empty_fail=0`).

## 2. Item (2) — wave sweep and `ScribeLesson`'s Mistakes coverage

### 2.1 My sweep (pinned set, command first)

Composition of the measured set is pinned so the numbers are reproducible from the tree:

```
$ cd .ufo/waves/round-33/wave1 && ls *.md | sort > /tmp/set.txt
receipts=62 listingsha=fcab8c86abe29c689449e9400dcb73a7880a8da1ab37be3a70767d90474925bd
$ for w in BLOCKED DEFECT survivor FAIL traceback PRE-STATE; do
    printf '%s files=%s hits=%s\n' "$w" \
      "$(grep -lF "$w" $(cat /tmp/set.txt) | wc -l)" \
      "$(grep -oF "$w" $(cat /tmp/set.txt) | wc -l)"; done
BLOCKED files=4 hits=16
DEFECT files=1 hits=2
survivor files=11 hits=29
FAIL files=25 hits=172
traceback files=1 hits=2
PRE-STATE files=37 hits=97
$ # the lesson's word set adds uppercase SURVIVOR:
SURVIVOR files=6 hits=13
```

Per-file distribution of the hits that are not pasted gate output (full table in the run; every
`FAIL`-bearing file was read):

`BLOCKED` — `ExecExpectedList.md:204` "BLOCKED: none." (negative assertion), `ScribeProvince.md:41`
(negative assertion), `ExecWaveEvidencePack.md` 7 (its own token-total table), `ScribeLesson.md` 4
(its sweep block). `DEFECT`/`traceback` — both hits are inside `ScribeLesson.md`'s own sweep line;
no receipt reports either. `survivor` — `MutCtrUnbound.md:136,212` (real, plain-run),
`MutEntryF16.md:176` (real, harness rule A), `MutLegacyManifestDrop.md:5,109` /
`MutCtrFetchMissing.md` / `MutCtrUrlMismatch.md` / `RevCalibration.md` / `CritC2Kill.md` /
`ExecWaveEvidencePack.md` (control or review text), `RevGateSpot.md:128` and
`ScribeReportDraft.md:338` (both report the two real ones). `FAIL` — 25 files, all pasted
instrument/mutant output, discrimination controls, or the three in-flight/anchor findings.

### 2.2 Coverage against the lesson

| sweep class | hits | where `corpus/lessons/round-33.md` covers it |
|---|---|---|
| `BLOCKED` | 4 files / 16 | § Mistakes opening: "No `BLOCKED:` hit is a seat reporting a blocker", naming the two negative assertions and the token table |
| `DEFECT` | 1 file / 2 | same paragraph, `files=0 hits=0` (its own line only) — correct |
| `traceback` | 1 file / 2 | same paragraph — correct |
| `survivor`/`SURVIVOR` | 11 / 29 (+6 / 13) | **M33-6(a)** `MutCtrUnbound` plain-run url limb; **M33-6(b)** `MutEntryF16` one-directional harness rule A; citations dismissed by name |
| `FAIL` | 25 / 172 | M33-3 (anchor drift), M33-4 (Q3 quote drift), M33-5 (digest churn) carry the material ones; the rest are control output |
| `PRE-STATE` | 37 / 97 | used as the label discipline throughout; no mistake class owed |

So **every sweep-word hit is covered or explicitly dismissed**. That answer is not the whole item
though; §2.3 and §2.4 are the two defects the sweep cannot see.

### 2.3 The lesson's own sweep block does not reproduce

The lesson prints (`corpus/lessons/round-33.md:89`): "over 56 receipts → `BLOCKED files=3 hits=10`,
`DEFECT… files=0 hits=0`, `SURVIVOR files=3 hits=4`, `survivor files=8 hits=20`, `FAIL files=22
hits=161`, `traceback files=0 hits=0`, `PRE-STATE files=34 hits=91`", with the command
`grep -l "$w" wave1/*.md` / `grep -o "$w" wave1/*.md`.

No receipt set I can construct from the tree yields those numbers:

| set | n | BLOCKED | DEFECT | SURVIVOR | survivor | FAIL | traceback | PRE-STATE |
|---|---|---|---|---|---|---|---|---|
| lesson (as printed) | 56 | 3/10 | 0/0 | 3/4 | 8/20 | 22/161 | 0/0 | 34/91 |
| all receipts now (§2.1) | 62 | 4/16 | 1/2 | 6/13 | 11/29 | 25/172 | 1/2 | 37/97 |
| receipts whose mtime precedes the lesson (n=57; none is `ScribeLesson.md`, whose receipt postdates the lesson) | 57 | 2/2 | 0/0 | 3/5 | 7/10 | 23/122 | 0/0 | 34/90 |
| `**/*.md` under `round-33/` | — | 4/16 | 1/2 | 5/9 | 9/25 | 25/171 | 1/2 | 37/97 |

The printed scope also contradicts its own counts: `BLOCKED hits=10` needs
`ExecWaveEvidencePack.md`'s token table (7 of the 16 `BLOCKED` hits today), i.e. at least a 59th
file, while the text says 56. In-flight rewrites explain part of the drift (`ExecWaveEvidencePack.md`
was rewritten at `01:53:54`, `ExecScratchDiscipline.md` at `01:56:09`, both after the lesson's
`01:53:33`), but a sweep figure with neither timestamp nor a pinned receipt-set digest cannot be
re-derived at all — the round-31 lesson's own fix (`O6`: "a sweep is evidence only when command and
output are both in the receipt") is stated in the command but not satisfied by the number.

The lesson's receipt-coverage line has two checkable errors of the same kind
(`corpus/lessons/round-33.md:7`): it lists `ScribeScorecard` and `RevC1BeforeAfter` among the absent
seats, but both receipts existed before composition — `ScribeScorecard.md` mtime `01:51:22 -0300`
(11822 B) and `RevC1BeforeAfter.md` mtime `01:52:01 -0300`, against the lesson's `01:53:33`. The
same lesson then quotes `ScribeScorecard.md`'s content in its sweep paragraph ("`ScribeScorecard.md`
only cites them"), so the absence list and its own citation disagree. Measured seat coverage at
composition: 57 of 64 receipts present (7 absent), not "56 of 64".

### 2.4 Two attack-seat findings of the class M33-6 admits are missing from Mistakes

Both receipts landed **before** the lesson (`MutCtrUrlMismatch.md` `01:24:44`,
`MutCtrSelftestSkip.md` `01:25:16`), are named in the lesson's own provenance list (line 138,
`MutCtr*`), and are quoted in the lesson's receipt matrix as `## Mistakes` evidence — but neither
finding appears in M33-1…M33-6:

- `MutCtrSelftestSkip.md:84` — the instrument's `--selftest` dispatch replaced by
  `print("selftest cases=0 failures=0"); return 0` is **KILLED** only by a clause the frozen C1
  predicate does not contain: "failures=0 lines printed from real cases". C1's predicate reads
  "`--selftest` prints failures=0 and exits 0", which the forged line satisfies. That is a
  verifiability hole in the claim's own wording — the same class as M33-6, and the only place the
  round measured it.
- `MutCtrUrlMismatch.md:180` — the instrument's selftest never exercises the substring-loosening
  world; the seat's fixture probe kills the mutant and proposes "a seventh case ("url is a proper
  prefix of its own row's URL token → must fail") would close it".

Neither receipt contains any of the six sweep words except one incidental `PRE-STATE` line
(`MutCtrSelftestSkip.md`: 0/0/0/0/0/1; `MutCtrUrlMismatch.md`: 1 `survivor`, 4 pasted `FAIL`), so
the sweep cannot find them. A third, later one is owed as an appended row: `ExecScratchDiscipline.md:75`
charges `ExecWaveEvidencePack` with a claim-versus-disk defect — "the `rm -rf` claim and the disk
disagree" (`ExecScratchDiscipline.md:99`) — while `ExecWaveEvidencePack.md:240` still states
"Removed with `rm -rf -- \"$S\"` … nothing of this seat's scratch remained", and
`/fast/scratch/hyaku/kasegi-r33/ExecWaveEvidencePack/` still holds 9 files (mtime `01:56`). That
receipt landed at `01:56:09`, after the lesson (`01:53:33`), so it is a late arrival and not a
composition defect — but M33-1…M33-6 is the ledger that would carry it.

Verdict on item 2: the Mistakes section **covers every sweep-word hit** (BLOCKED/DEFECT/survivor/
FAIL/traceback/PRE-STATE) and dismisses the non-mistake classes explicitly; it **does not cover**
two pre-lesson attack findings of a class it already admits, and its own sweep block and
receipt-coverage line are not reproducible/are stale.

## 3. Impacted axes

- `depth:verifiability` (C1, held 4) — **primary.** C1's predicate is met on landed bytes
  (`records=40 bound=40 unbound=0` exit 0, `selftest cases=11 failures=0`), so the claim is not
  falsified; but its two new authorities accept a round-32 tree whose captures are absent
  (`captures=none` PASS) or altered (`bound=2 unbound=0` on 18 bytes), so "held 4" certifies
  manifest↔registry binding and not capture↔manifest binding. R20's second clause is unwitnessed.
- `depth:density` (9, unclaimed this round) — **no harm from this seat**: no lane file other than
  this receipt, no instrument or manifest edit.
- `coverage` (C2, held 7) — unaffected: nothing here touches F16/S049/S050 binding; the walk found
  `entries=19 pass=19 exit=0` including `PASS F16 … ids=S049,S050` on my own run.
- Mistake ledger — the lessons' record of what the round learned: 2 admitted classes missing, 1
  late-arrival owed, 1 sweep figure unreproducible.

## 4. Smallest safe corrections

1. **`closure-check.sh` capture-existence conjunct** (owner: `ExecErratumCheck`'s file, no lane
   data change, ~10 lines): after the record loop, require each record's `path` (default
   `<id>.txt`) to exist under `$d` and, when the record carries `sha256`, to hash to it; add two
   exit-1 cases (`captures=none`; one `path` deleted). All 40 landed records already satisfy it
   (`ExecCaptureBinding.md` §8 item 1: `path_missing=0 sha_or_empty_fail=0`), so the lane stays
   green and R20's second clause becomes runnable. Narrow the §6 heading to the modes actually
   measured if the conjunct is not taken.
2. **Rule D for the instrument** (owner: L1 erratum, already proposed as
   `ExecCaptureBinding.md` §8 item 1 and named in the lesson's Gate caveats): land it or state in
   the C1 record that `bound=40` is metadata binding only. Until then R15 has an open defect whose
   closure check exits 0 — `m1` is the receipt.
3. **Append M33-7 and M33-8 to `corpus/lessons/round-33.md`** (append-only, R16 form — leave M33-1…6
   byte-identical): M33-7 = the selftest-forgery wording hole (`MutCtrSelftestSkip.md:84`), M33-8 =
   the substring-loosening world the selftest never builds (`MutCtrUrlMismatch.md:180`);
   both are pre-lesson receipts already cited as `## Mistakes` evidence in the lesson's receipt.
4. **Append a sweep re-run** to the lesson with its timestamp and the sorted receipt-name digest
   (my §2.1 form: `receipts=62 listingsha=fcab8c86…`), and correct line 7's absence list in the
   same appended erratum (measured: `ScribeScorecard.md` `01:51:22`, `RevC1BeforeAfter.md`
   `01:52:01`, 57 of 64 receipts present at `01:53:33`). M33-9 for the false `rm -rf` attestation
   is the L1's call once `ExecWaveEvidencePack` settles.

## 5. Bounds on what this proves

- The three required cases were run on **committed** `9f98488` bytes and on a base-tree
  (`690b69d`) extraction; the receipt's own runs were on an **untracked** worktree manifest. I did
  not reproduce the seat's PRE-STATE timing, only its outputs.
- `m1`/`m5`/`m4` are scratch mutants, not states the lane ever held: no landed tree is claimed to
  have missing captures. The claim is about what the two checkers can distinguish.
- My sweep is a point-in-time measurement of a mutable directory; the listing digest in §2.1 is the
  only thing that makes it re-derivable. Receipts still being written when I measured
  (`ExecWaveEvidencePack.md` `01:53:54`, `ExecScratchDiscipline.md` `01:56:09`,
  `ScribeReportDraft.md` `01:56:49`) are labelled as late arrivals, never compared as before/after.
- I judge no claim and edit nothing: item (1) verdicts are the checker's exit codes, item (2)
  verdicts are `grep` counts over named files.

## 6. Cleanup

All fixture trees, the extracted script and every log live under
`$HYAKU_SCRATCH/kasegi-r33/CritMistakes/` and are removed here, after this receipt was written:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r33/CritMistakes
$ ls -d /fast/scratch/hyaku/kasegi-r33/CritMistakes ; echo ls_exit=$?
ls_exit=2
```

`ExecScratchDiscipline.md` (§ T3 table) listed `CritMistakes` at `884 KiB / 45 files` with no
receipt; that was this seat mid-run. No other scratch path of mine existed; no `/tmp` path is cited
as evidence above (`/tmp/set.txt` is the piped listing of a lane directory and is re-derivable from
the command shown).
