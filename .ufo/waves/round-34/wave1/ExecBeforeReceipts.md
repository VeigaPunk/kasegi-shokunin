# ExecBeforeReceipts — round-34 frozen before-controls replay

Seat: ExecBeforeReceipts (executor, leaf). Lane: `kasegi-shokunin`. Round: 34. Axes: `depth:verifiability`, `coverage`.
Base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13` (tree `a002be50dcd5ad106ffe85524bf4553d4b008c0b`, committed 2026-10-26T02:23:13-03:00).
Answering model (runtime-reported): `opencode-go/deepseek-v4.1-flash`.
No subagents, no delegation, no background jobs, no labrat. No git/jj mutation (read-only `archive`/`show`/`rev-parse`/`diff`/`status` only). No tools installed. Nothing written outside the lane receipt and the scratch tree (deleted before yielding).

## Verdict

**PASS — all 45 lines of `c1-controls/before.txt` reproduce; byte-identical after one documented path normalization.**

- Freeze archive: `git archive 29f606db` → 6824 files; base archive `014ee2d` → 6815 files; a second freeze extraction is `diff -r` identical.
- Reconstructed receipt: sha256 `d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0`, equal to the committed blob's sha256 and to `cmp` (exit 0). Second run byte-identical (`cmp`).
- Un-normalized run differs on exactly **one** line — the census `ok` line carries the scratch root by construction (round-33 precedent); root substitution is shown verbatim below.
- Replay at base `014ee2d` equals replay at freeze `29f606db`: `git diff --name-only 014ee2d 29f606d` lists only the nine `.ufo/waves/round-34/*` control files, and the two replay outputs are `diff`-identical.
- `claims.json` at the freeze commit hashes to its committed bytes: `git show 29f606db:... | sha256sum` = archive copy = live lane copy = `dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850`; blob `786d68a5f32fb28c3a455a8e1dac61ecf7dc0d52` is identical at `29f606db` and at `HEAD` (no post-freeze edit).

Two receipt-hygiene findings are recorded at the end (both non-blocking reproductions): the lesson-erratum line's value is reproducible only as a coincidental string count, and the three committed before-receipts are one file in three places.

## Method note (bounds the claim)

`before.txt` is **output-only**: it records no command line, and no command transcript is committed. The commands below were **reconstructed** from the receipt's own section labels and re-derived from freeze bytes. Byte-identity of the rebuilt file is evidence that the frozen values are reproducible, not proof that the L1's original invocation was character-identical.

The C2 census line embeds an absolute registry path, so the archive run is normalized on that line only (`$S/root/kasegi-shokunin/` → `/home/vgpnk/Projects/shokunin/kasegi-shokunin/`). The live lane was **not** used for any measurement — it is being edited in flight this wave (`git status --porcelain` shows `M SCORECARD.md`, `M corpus/QUALITY.md`, `M corpus/instruments/capture-binding-check.py`, `M corpus/instruments/frontier-recheck-count.py`, `M corpus/lessons/round-29.md`, `M corpus/lessons/round-33.md`, `M corpus/source-snapshots/round-26/manifest.json`, `M corpus/source-snapshots/round-32/manifest.json`, plus untracked round-34 files); all runs are against the freeze export.

## Report

### Inputs

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
FREEZE=29f606dbdd28aff6fd4573ab4b90788bbb90af13
BASE=014ee2d7aa8c3c095ff57ae51097606a9906228c
S=/fast/scratch/hyaku/kasegi-r34/ExecBeforeReceipts      # deleted before yield
```

```
$ git -C "$LANE" archive "$FREEZE" | tar -x -C "$S/freeze"     # exit 0
$ git -C "$LANE" archive "$BASE"   | tar -x -C "$S/base"       # exit 0
$ git -C "$LANE" archive "$FREEZE" | tar -x -C "$S/freeze2"    # exit 0
freeze_files=6824 base_files=6815
$ diff -r "$S/freeze" "$S/freeze2"                             # exit 0 → second_extract_identical
$ diff -r "$S/base/corpus" "$S/freeze/corpus"                  # exit 0 → corpus_identical
$ diff -r "$S/base" "$S/freeze" --exclude=.ufo                 # exit 0 → no non-control difference
$ git -C "$LANE" diff --name-only 014ee2d 29f606d              # exit 0, nine paths, all .ufo/waves/round-34/*
```

### Census target

```
$ mkdir -p "$S/root"; cp /home/vgpnk/Projects/shokunin/shokunin.conf "$S/root/shokunin.conf"
$ cp -a "$S/freeze" "$S/root/kasegi-shokunin"
$ grep -n '^kasegi' "$S/root/shokunin.conf"
46:kasegi|kasegi-shokunin|depth + coverage (bounty and security research)
```

### Per-line match report

`OBS` = value measured from the freeze export by the reconstructed command. All lines 1–45 accounted for; static `==`/`##`/`--` labels are literal strings, value lines are measured.

| line | receipt text | reconstructed command (cwd = freeze export) | OBS | match |
|---|---|---|---|---|
| 1 | `== kasegi round-34 frozen before-controls (base 014ee2d...) ==` | literal echo | — | static |
| 2 | (blank) | — | — | yes |
| 3 | `### C1 (depth:verifiability) before ###` | literal echo | — | static |
| 4 | `-- r-defect-closure.sh presence --` | literal echo | — | static |
| 5 | `ls: cannot access 'corpus/instruments/r-defect-closure.sh': No such file or directory` | `ls corpus/instruments/r-defect-closure.sh 2>&1` | same message | **yes** |
| 6 | `ls_exit=2` | `$?` after the `ls` | `2` | **yes** |
| 7 | `-- capture-binding-check --selftest cases at base --` | literal echo | — | static |
| 8 | `selftest cases=11 failures=0` | `python3 corpus/instruments/capture-binding-check.py --selftest \| tail -1` (exit 0; 11 `selftest case=` lines) | `selftest cases=11 failures=0` | **yes** |
| 9 | `-- survivor mutants under the frozen round-33 kill rule --` | literal echo | — | static |
| 10 | `skip-selftest summary mutant: prints 'selftest cases=0 failures=0' exit 0 (F-5: NOT caught by frozen clause)` | mutant built from freeze bytes, `--selftest` (see below) | line contains `selftest cases=0 failures=0`, exit 0 | **yes** |
| 11 | `accept-record-without-url mutant: prints 'records=2 bound=2 unbound=0' exit 0 (SURVIVOR of plain-run rule)` | mutant built from freeze bytes, `--root fixture2` (see below) | `records=2 bound=2 unbound=0`, exit 0 | **yes** |
| 12 | `-- <LANE_HASH> marker count --` | literal echo | — | static |
| 13 | `2` | `grep -c '<LANE_HASH>' SCORECARD.md` | `2` (lines 988, 1087; 2 occurrences) | **yes** |
| 14 | `-- round-32 manifest fetched_utc values --` | literal echo | — | static |
| 15 | `S049 '2026-10-25T23:14:00-03:00' archival= None` | JSON read of `corpus/source-snapshots/round-32/manifest.json` | identical | **yes** |
| 16 | `S050 '2026-10-25T23:14:00-03:00' archival= None` | same | identical | **yes** |
| 17 | `-- round-26 S040-live.txt manifest record? --` | literal echo | — | static |
| 18 | `records= 1 paths= ['S041.txt']` | JSON read of `corpus/source-snapshots/round-26/manifest.json` (`print('records=', len(srcs), 'paths=', [...])`) | identical; `S040-live.txt` present in dir and absent from `paths` → orphan | **yes** |
| 19 | `-- QUALITY R20 'exactly one' occurrences --` | literal echo | — | static |
| 20 | `1` | `grep -c 'exactly one' corpus/QUALITY.md` | `1` (R20 row, `QUALITY.md:169`) | **yes** |
| 21 | `-- round-33 lesson erratum present? --` | literal echo | — | static |
| 22 | `4` | `grep -c 'Erratum' corpus/lessons/round-33.md` | `4` — **but** the 4 matches are the seat name `ExecErratumCheck`, not errata text (see finding F2) | value yes / control weak |
| 23 | (blank) | — | — | yes |
| 24 | `### C2 (coverage) before ###` | literal echo | — | static |
| 25 | `-- frontier admitted --` | literal echo | — | static |
| 26 | `16` | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `16` | **yes** |
| 27 | `-- registry rows --` | literal echo | — | static |
| 28 | `50` | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `50` | **yes** |
| 29 | `-- S051 rows --` | literal echo | — | static |
| 30 | `0` | `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `0` | **yes** |
| 31 | `-- entries citing S051 --` | literal echo | — | static |
| 32 | `0` | `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `0` | **yes** |
| 33 | `-- harness --` | literal echo | — | static |
| 34 | `entries=19 pass=19 exit=0` | `python3 corpus/instruments/frontier-recheck-count.py \| tail -1` (19 PASS lines, 0 FAIL lines; exit 0) | identical | **yes** |
| 35 | `-- source-recheck S051 (manifest absent) --` | literal echo | — | static |
| 36 | `manifest UNAVAILABLE reason=missing` | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | identical (round-34 dir absent at freeze) | **yes** |
| 37 | `recheck_exit=2` | `$?` after source-recheck | `2` | **yes** |
| 38 | `-- knowledge entries --` | literal echo | — | static |
| 39 | `45` | `ls corpus/knowledge/*.md \| wc -l` | `45` | **yes** |
| 40 | (blank) | — | — | yes |
| 41 | `### census before ###` | literal echo | — | static |
| 42 | `kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes` | `sources-census.sh validate --root "$S/root" kasegi` | identical (TAB-separated) | **yes** |
| 43 | `kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes` | same | identical | **yes** |
| 44 | `kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` | same, normalized root | identical after substitution (raw: `.../ExecBeforeReceipts/root/kasegi-shokunin/corpus/SOURCES.md`) | **yes** |
| 45 | `census_exit=0` | `$?` after census | `0` | **yes** |

### Reproduction script (verbatim, written to `$S/repro-c1.sh`)

```bash
#!/usr/bin/env bash
# Reconstructs .ufo/waves/round-34/c1-controls/before.txt from the freeze export.
set +e
FR=$1; S=$2; CENSUS_ROOT=$3; OUT=$4
cd "$FR" || exit 2
{
  echo "== kasegi round-34 frozen before-controls (base 014ee2d7aa8c3c095ff57ae51097606a9906228c) =="
  echo ""
  echo "### C1 (depth:verifiability) before ###"
  echo "-- r-defect-closure.sh presence --"
  ls corpus/instruments/r-defect-closure.sh 2>&1
  echo "ls_exit=$?"
  echo "-- capture-binding-check --selftest cases at base --"
  python3 corpus/instruments/capture-binding-check.py --selftest | tail -1
  echo "-- survivor mutants under the frozen round-33 kill rule --"
  skip_line=$(grep -E '^selftest cases=' "$S/mut-skip.out")
  printf "skip-selftest summary mutant: prints '%s' exit 0 (F-5: NOT caught by frozen clause)\n" "$skip_line"
  accept_line=$(grep -E '^records=2 bound=2 unbound=0$' "$S/mut-unbound.out")
  printf "accept-record-without-url mutant: prints '%s' exit 0 (SURVIVOR of plain-run rule)\n" "$accept_line"
  echo "-- <LANE_HASH> marker count --"
  grep -c '<LANE_HASH>' SCORECARD.md
  echo "-- round-32 manifest fetched_utc values --"
  python3 - <<'PY'
import json
d = json.load(open('corpus/source-snapshots/round-32/manifest.json'))
for s in d.get('sources', []):
    print(s.get('id'), repr(s.get('fetched_utc')), 'archival=', repr(s.get('archival')))
PY
  echo "-- round-26 S040-live.txt manifest record? --"
  python3 - <<'PY'
import json
d = json.load(open('corpus/source-snapshots/round-26/manifest.json'))
srcs = d.get('sources', [])
print('records=', len(srcs), 'paths=', [s.get('path') for s in srcs])
PY
  echo "-- QUALITY R20 'exactly one' occurrences --"
  grep -c 'exactly one' corpus/QUALITY.md
  echo "-- round-33 lesson erratum present? --"
  grep -c 'Erratum' corpus/lessons/round-33.md
  echo ""
  echo "### C2 (coverage) before ###"
  echo "-- frontier admitted --"
  grep -cE '^\| F[0-9]+ \|' corpus/README.md
  echo "-- registry rows --"
  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
  echo "-- S051 rows --"
  grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md
  echo "-- entries citing S051 --"
  grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l
  echo "-- harness --"
  python3 corpus/instruments/frontier-recheck-count.py | tail -1
  echo "-- source-recheck S051 (manifest absent) --"
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
  echo "recheck_exit=$?"
  echo "-- knowledge entries --"
  ls corpus/knowledge/*.md | wc -l
  echo ""
  echo "### census before ###"
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$CENSUS_ROOT" kasegi
  echo "census_exit=$?"
} > "$OUT" 2>&1
exit 0
```

### Reproduction and byte comparison

```
$ "$S/repro-c1.sh" "$S/freeze" "$S" "$S/root" "$S/c1-repro-freeze-raw.txt"   # exit 0
$ "$S/repro-c1.sh" "$S/base"   "$S" "$S/root" "$S/c1-repro-base-raw.txt"     # exit 0
$ sed "s|$S/root/kasegi-shokunin/|/home/vgpnk/Projects/shokunin/kasegi-shokunin/|g" \
      "$S/c1-repro-freeze-raw.txt" > "$S/c1-repro-freeze.txt"
$ diff -u "$S/freeze/.ufo/waves/round-34/c1-controls/before.txt" "$S/c1-repro-freeze.txt"
(no output)                                                                  # diff_exit=0
$ cmp "$S/freeze/.ufo/waves/round-34/c1-controls/before.txt" "$S/c1-repro-freeze.txt"
                                                                             # cmp_exit=0
$ sha256sum "$S/c1-repro-freeze.txt"
d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0
$ diff -u "$S/c1-repro-base.txt" "$S/c1-repro-freeze.txt"                    # diff_exit=0

Raw (un-normalized) difference is exactly one line:
-kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
+kasegi	ok	/fast/scratch/hyaku/kasegi-r34/ExecBeforeReceipts/root/kasegi-shokunin/corpus/SOURCES.md

Second run:
$ "$S/repro-c1.sh" "$S/freeze" "$S" "$S/root" "$S/c1-repro-freeze-raw-2.txt"
$ cmp "$S/c1-repro-freeze.txt" "$S/c1-repro-freeze-2.txt"                    # second_run_identical
```

Census date-window control (the frozen command pins no `--today`; E08 compares `opened` to today):

```
$ sources-census.sh validate --root "$S/root" --today 2026-10-26 kasegi      # exit 0
$ sources-census.sh validate --root "$S/root" kasegi                          # exit 0
$ diff -u "$S/census-pinned.txt" "$S/census-default.txt"                      # diff_exit=0
```

### Mutant controls (lines 10–11)

Built from the freeze instrument `corpus/instruments/capture-binding-check.py` (sha256 `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`, 492 lines) by one asserted single-occurrence replacement each, in scratch only:

- skip-selftest: `if args.selftest:\n        return selftest(args.scratch)` → `if args.selftest:\n        print("selftest cases=0 failures=0")\n        return 0` (count 1). Mutant sha256 `7c0680550251468a03d87223430553fd928e074f4775411d4fdebb939f927db7`.
- accept-record-without-url: in `bind_record()`, `return False, ["rule=url-mismatch record=%s detail=absent" % record_id]` → `return True, []` (count 1). Mutant sha256 `9001ec5dbcf25df7ba74e6580969edaaa1859269ecce34d59512d52e46323dcb`.

```
$ python3 "$S/mut/skip-selftest.py" --selftest
selftest cases=0 failures=0
skip_exit=0

$ python3 "$S/mut/accept-record-without-url.py" --root "$S/fixture2"
MANIFEST round-23 records=2 url_bound=2 fetched=0 archival=2
AUDIT records=2 with_url=1 with_fetched_utc=0 with_archival=2 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
records=2 bound=2 unbound=0
unbound_exit=0

# detector sound on the same fixture (fixture2 rebuilt from round-33 MutCtrUnbound §fixture v2: S001 carries url, S002 has none)
$ python3 corpus/instruments/capture-binding-check.py --root "$S/fixture2"
MANIFEST round-23 records=2 url_bound=1 fetched=0 archival=2
AUDIT records=2 with_url=1 with_fetched_utc=0 with_archival=2 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=url-mismatch record=S002 detail=absent dir=round-23
records=2 bound=1 unbound=1
pristine_exit=1

# the accept mutant is also invisible to the plain run on the landed freeze tree:
$ python3 "$S/mut/accept-record-without-url.py" --root "$S/freeze"
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
mutant_landed_exit=0
```

Frozen round-33 C1 kill rule (verbatim from `29f606db:.ufo/waves/round-33/claims.json`), the rule under which these are survivors: "…`--selftest` prints any failure or exits non-zero; OR a fake checker … that prints the summary without validating exits 0 …". The skip mutant prints no failure and exits 0 → **not caught** (F-5); the accept mutant prints the exact passing plain-run summary and exits 0 → **survivor of the plain-run rule** (killed only by the instrument's own `--selftest`, which is why C1's after-state routes them to `kill-rule-check.py`). Both receipt lines are therefore derived, not echoed.

### claims.json at the freeze commit

```
$ git -C "$LANE" show 29f606db:.ufo/waves/round-34/claims.json | sha256sum
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  -
$ sha256sum "$S/freeze/.ufo/waves/round-34/claims.json"
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850
$ sha256sum "$LANE/.ufo/waves/round-34/claims.json"
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850
blob@freeze=786d68a5f32fb28c3a455a8e1dac61ecf7dc0d52
blob@HEAD=786d68a5f32fb28c3a455a8e1dac61ecf7dc0d52
```

`blob@base` is absent (`fatal: path '.ufo/waves/round-34/claims.json' exists on disk, but not in '014ee2d'`) — expected: the claims file is introduced by the freeze commit.

### Stored control-file digests (git-show vs archive vs live lane)

```
c1-controls/before.txt     git-show=d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0 archive=same live=same
c2-controls/before.txt     git-show=d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0 archive=same live=same
census-before.txt          git-show=d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0 archive=same live=same
c2_cmp_exit=0  census_cmp_exit=0   # c2-controls/before.txt and census-before.txt are byte-identical to c1-controls/before.txt
```

### Freeze-export digests used by the controls

```
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247  corpus/source-snapshots/round-26/manifest.json
e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3  SCORECARD.md
00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087  corpus/QUALITY.md
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
ca17591d4a36e1a6623adb9acb7ac2bc0a3dbd87c24f3913229fe0b4b781feb2  corpus/lessons/round-33.md
435e97b5929beb75fe53b2fe849855fdb8bd851c2a1e621c5dc3d1e7c5063420  corpus/lessons/round-33-verifier-spotcheck.md
```

## Findings for the L1 (advisory; no action taken)

**F1 — the three "before" receipts are one file copied three times.** `c1-controls/before.txt`, `c2-controls/before.txt`, and `census-before.txt` all hash to `d90ce017…48db5f0` (`cmp` exit 0). There is therefore exactly **one** independently produced before-receipt this round; the C2 and census "receipts" add no independent capture. The values they carry are correct and reproducible, but the file placement implies three captures where there is one. If the round's evidence model wants per-claim receipts, this is a receipt-hygiene defect (landing/reference-drift class), not a measurement error.

**F2 — line 22's control is not a valid "R7 erratum absent" witness.** The only reconstruction that yields `4` is `grep -c 'Erratum' corpus/lessons/round-33.md`, and all four matches are the seat name `ExecErratumCheck` (`grep -o '.\{0,30\}Erratum.\{0,30\}'` shows `wave1/ExecErratumCheck.md` ×3 and the seat list ×1). The meaningful counts are: `grep -c 'erratum'` = 5 (the word), `grep -c 'R7'` = 0, `grep -c 'S050.txt:70'` = 0, `grep -c '31/22'` = 0 — the last three do confirm the R7 erratum is **absent** at the freeze, which is what `claims.json` asserts. Recommendation: treat F2 as a receipt-label defect (the control name promises an R7 check the command does not perform) and rely on the token-absence counts for R7's before-state.

**F3 (method bound) — the before-receipt is output-only.** No command line is committed for any of the 45 lines; the commands above are reconstructions that yield byte-identical output. Two lines are reconstructed by choice rather than uniquely determined: line 8 (the receipt keeps only the selftest summary, so `tail -1` discards the 11 per-case lines) and line 22 (F2). This is the same limitation round-33's `ExecBeforeReceipts` recorded; it does not affect the measured values.

**F4 (positive) — base and freeze are the same corpus bytes.** `git diff --name-only 014ee2d 29f606d` touches only the nine `.ufo/waves/round-34/*` control files; replaying from the base export produces the identical receipt (`diff` exit 0). The freeze commit adds no data or instrument drift over the base, so the before-values bind both commits.

## Risks / limits

- Census is validated against an archive-carrying scratch root, so its `ok` path line is root-dependent; the substitution is the only normalization applied and is displayed in full.
- The live lane is mid-wave with eight modified tracked files and new untracked round-34 files; none were read for this receipt except read-only `git status`/`git show`.
- No closure check (R1–R9), instrument selftest beyond `cases=11`, or post-freeze after-state was judged here — that is other seats' scope and the L1's integration call.
- Scratch tree `/fast/scratch/hyaku/kasegi-r34/ExecBeforeReceipts` (470 MB) was deleted before yield; no scratch remains, so the receipt URLs above are command recipes, not live paths.
- No tools installed or upgraded; nothing to record under the 2026-10-19 tooling authorization.
