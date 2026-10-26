# ExecMistakesDraft — round-40 wave 1 receipt

Seat: executor (leaf; no subagent, no task/agent/workpool call, no background job, no orchestration
runtime). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` only; fleet root and
`/home/vgpnk/Projects/shokuknow` read-only and unread in this seat except for the disk-guard script.
Base `a7af2ce63bce153757d39bf66b366a96caf30c13`; claims-freeze `5e985b74075dd3813a63d7750966bf8abf693465`;
frozen claims read at `.ufo/waves/round-40/claims.json` (C1 predicate H1–H10 and kill rule; not edited).
Route chain captured at spawn: fleet-root cwd → own scratch
`/fast/scratch/hyaku/kasegi-r40/ExecMistakesDraft`; every read/write by absolute path; all git use was
read-only (`git log`, `git show`, `git rev-parse`) and no git/jj mutation ran anywhere.

Disk guard before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
`/fast/scratch/hyaku 26% free 599.9G`, `/tmp 3% free 125.2G`, `/var/tmp 35% free 585.3G` — green.

## Deliverables

| path (relative to lane) | bytes | lines | sha256 | shape |
|---|---|---|---|---|
| `.ufo/waves/round-40/wave1/ExecMistakesDraft.txt` | 6618 | 73 | `4662293d9bf315434d1ff1359b84f681fdeddc3b87ee7f4970cb5bd7cfec39cf` | line 1 = the landable `## Mistakes` table row (7 cells, one line, no newline inside); every later line is evidence the row's last cell cites, after one marker line `# evidence only — …` |
| `.ufo/waves/round-40/wave1/ExecMistakesDraft.h5-replica.sh` | 4341 | 97 | `db56b5dad26172b6f2f82834ec7596749068e23766c59f92693769f8b9839856` | independent replica of the H5 limb (re-derives `version`/`xref`/`digest`/`declared` from the export tree, and enforces `export-commit ≤ run-utc ≤ receipt-commit`); bash, `bash -n` clean |
| `.ufo/waves/round-40/wave1/ExecMistakesDraft.fixture-future-dated.txt` | 7428 | 87 | `0bf299a65c17b054d609076276d9316c246baa15822d36cde69b75bbf535e525` | the committed `all-gates v5` receipt bytes (`8371e7ac…`) with one byte-range changed: `run-utc=2026-10-26T20:54:44Z` → `run-utc=2026-10-27T21:35:00Z` |

The row lands by appending it to `## Mistakes` in `corpus/lessons/round-40.md` (that file is created at
integration; the row is line 1 of `ExecMistakesDraft.txt` and nothing else from this file lands). The two
sibling artifacts are the evidence the row's `able to fail` cell names, so a reader can re-run it.

## What the row states (and what it does not)

- id `M40-1`, class `evidence-provenance` — the R1 routed defect: the round-39 attempt-1 receipt
  `5006097a:.ufo/waves/round-39/final-gates/all-gates.txt` (`all-gates v3`, export-ref `46c66c26`) records
  `run-utc=2026-10-26T21:35:00Z`, `closed=8/8 exit=0`, `selftest cases=8 failures=0`, while its containing
  commit is `2026-10-26T20:12:12Z` (+82m48s) and the L1's own run over `5006097a` printed `closed=6/8 exit=1`
  and `selftest cases=8 failures=2`.
- `captured-by`: `none at the time` — the wave-2 instrument attack found it (`CritC1Kill.md` §K5), and no
  instrument parsed `run-utc`: the only `run-utc` writer in `corpus/instruments/r39-closure.sh` is the fixture
  helper `g2_content` (`:1150`), so the committed header was authored, not teed.
- `fix`: H5/H7 of `r40-closure.sh` (H5 re-derives payload from the export and bounds `run-utc`;
  H7 makes the receipt the teed transcript of one run with `run-utc` printed by the run and a byte-identical
  re-run) + `corpus/QUALITY.md` R37, minted this round by `ExecH3Criterion` (`wave1/ExecH3Criterion.txt:15`,
  whose rule text already states "its `run-utc` is printed by the run itself at execution and never
  post-dates the commit that contains it").
- It does **not** re-decide C1 (that is the L1's gate), does not edit `claims.json`, and does not claim the
  committed H5 case passes: `corpus/instruments/r40-closure.sh` did not exist at this seat's run time
  (`ls corpus/instruments/r40-closure.sh` → no such file), so the falsification below is an independent
  replica of the frozen H5 shape, not the committed instrument.

## Retained evidence — commands and actual output

### E1. The defect, from the commit that contains it

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin log -1 --format='%H %cI' 5006097a
5006097a84305267c9a3e8c1e1d560e60fe41d37 2026-10-26T17:12:12-03:00

$ TZ=UTC git -C … log -1 --format='%H committer-utc=%cd' --date=format-local:'%Y-%m-%dT%H:%M:%SZ' 5006097a
5006097a84305267c9a3e8c1e1d560e60fe41d37 committer-utc=2026-10-26T20:12:12Z

$ git -C … show 5006097a:.ufo/waves/round-39/final-gates/all-gates.txt | sed -n '1,4p'
all-gates v3
export-ref=46c66c268502abd1b2c342fc71bf88ccf721845b
suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
run-utc=2026-10-26T21:35:00Z

$ git -C … show 5006097a:…/all-gates.txt | grep -E '^(G2 payload|closed=8/8|selftest cases=)'
G2 payload=receipt=1,…,diff-clean=1,diff-read=ok,digest-match=1,…,final-lane-commit=0 closed=1
closed=8/8 exit=0
selftest cases=8 failures=0
```

The graded export-ref `46c66c26` is committed `2026-10-26T17:11:10-03:00` (`git log -1 --format='%H %cI %s' 46c66c26`),
so both the containing commit and the graded head precede the recorded run time. Delta recomputed here:
`python3 -c "…2026-10-26T21:35:00+00:00 − 2026-10-26T20:12:12+00:00"` → `1:22:48`, matching
`wave2/CritC1Kill.md` §K5 (`+82m48s after the commit`).

### E2. Corroboration read (not re-run, and labelled as such)

- Verifier `corpus/lessons/round-39-verifier-spotcheck.md:158-167` (R1): the scratch transcript
  `/fast/scratch/hyaku/kasegi-r39-l1/verify-Y.txt` (sha256 `98290ee6…`, mtime `17:12:25-03:00`, uncommitted)
  shows the L1's own run over `5006097a` printing `closed=6/8 exit=1` and `selftest cases=8 failures=2`, and
  `make-receipt.sh` there prints no `run-utc` line. I did not re-run it; the transcript is not durable.
- `corpus/lessons/round-39.md:86` discloses the false timestamp in the round's own words.
- `wave2/CritC1Kill.md` §K5 (lines 396-409) records the same arithmetic and notes "G2 does not parse `run-utc`
  at all"; §K1 (`:312`) records that the suite never prints `run-utc=` itself.
- Absence check now: `test -e /fast/scratch/hyaku/kasegi-r39-l1/verify-Y.txt && echo present || echo absent`
  → `absent`; `ls -d /fast/scratch/hyaku/kasegi-r39*` → `No such file or directory` (so the row cites the
  verifier's reading of a file that no longer exists, not a file I inspected).
- `grep -n "printf 'run-utc" corpus/instruments/r39-closure.sh` → `1150:    printf 'run-utc=2026-10-26T20:00:00Z\n'`,
  inside `g2_content` (fixture writer) — the row's claim that the only writer is the fixture helper.

### E3. H5 able-to-fail proof (the item's required transcript)

Detector `wave1/ExecMistakesDraft.h5-replica.sh`; run from the lane root, four cases. Full transcript is
`ExecMistakesDraft.txt` after the marker line; the decisive lines:

```
$ git -C . show 8371e7ac…:…/all-gates.txt | sed 's/^run-utc=2026-10-26T20:54:44Z$/run-utc=2026-10-27T21:35:00Z/' > …/ExecMistakesDraft.fixture-future-dated.txt
$ diff <(git -C . show 8371e7ac…:…/all-gates.txt) …/ExecMistakesDraft.fixture-future-dated.txt
4c4
< run-utc=2026-10-26T20:54:44Z
---
> run-utc=2026-10-27T21:35:00Z
exit=1                                        # one line differs, nothing else

$ bash …/ExecMistakesDraft.h5-replica.sh --lane . --export-ref ee5ae5e1… --receipt .ufo/waves/round-39/final-gates/all-gates.txt --contained-in 8371e7ac…
H5 payload=version=1,xref=1,digest=1,declared=1(recorded=2,export=2),run-utc=2026-10-26T20:54:44Z,dated=ok closed=1
exit=0                                        # control: the unedited receipt passes every limb

$ bash … --export-ref ee5ae5e1… --receipt …/ExecMistakesDraft.fixture-future-dated.txt --contained-in 8371e7ac…
H5 payload=version=1,xref=1,digest=1,declared=1(recorded=2,export=2),run-utc=2026-10-27T21:35:00Z,dated=future closed=0
exit=1                                        # future-dated run-utc alone flips the verdict

$ bash … --export-ref 46c66c26… --receipt-ref 5006097a…:…/all-gates.txt --contained-in 5006097a…
H5 payload=version=1,xref=1,digest=1,declared=1(recorded=2,export=2),run-utc=2026-10-26T21:35:00Z,dated=future closed=0
exit=1                                        # the real defective receipt, rejected

$ git -C . show 8371e7ac…:…/all-gates.txt | sed 's/^G1 payload=declared=2,/G1 payload=declared=3,/' > /tmp/h5-forged-payload.txt
$ bash … --export-ref ee5ae5e1… --receipt /tmp/h5-forged-payload.txt --contained-in 8371e7ac…
H5 payload=version=1,xref=1,digest=1,declared=0(recorded=3,export=2),run-utc=2026-10-26T20:54:44Z,dated=ok closed=0
exit=1                                        # forged payload limb, same date window
```

The replica is time-invariant: the window is computed from `git log --format=%ct` of the export-ref and of
the containing commit, never from wall clock, so a re-run prints the same bytes (H7's determinism
requirement) and the fixture cannot pass by matching a hardcoded string — the positive control shows the
same code path returning `closed=1`.

Digests of the three inputs, printed in the same transcript:
`8d46d7b2…` `all-gates.txt` (= the v5 receipt digest the verifier records), `0bf299a6…` fixture,
`db56b5da…` detector.

## Checks I ran beyond the proving pair

- `bash -n` on the detector (clean) and on the landed copy; `sha256sum` on the landed copy equals the digest
  printed in the transcript (`db56b5da…`), and the landed fixture equals `0bf299a6…`.
- Row shape: exactly 7 non-empty cells (id/class/event/evidence/captured-by/fix/able-to-fail) and 8 `|`
  separators, i.e. the same shape as `M39-1…M39-4` in `corpus/lessons/round-39.md:74-79`; no cell contains a
  raw `|`, so the table cannot break.
- The row's R37 reference resolves to the block drafted this round (`wave1/ExecH3Criterion.txt`, row `R37`),
  and its quoted rule text contains the provenance limb the row claims.
- Lane writes confined: `git status --porcelain` shows only the pre-existing untracked `.ufo/waves/round-40/`
  entries plus `wave1/`; no tracked file touched, no `corpus/` or top-level file written.

## Risks / limits (for the L1)

1. **Row id may renumber.** `M40-1` is my allocation; this seat is the only wave-1 seat drafting a
   `## Mistakes` row, but a wave-2 critic may mint an earlier row. Renumbering changes only cell 1.
2. **The replica is not the committed instrument.** ExecSuiteBuild owns `r40-closure.sh`; if its H5 uses a
   different window (e.g. receipt-commit only, or the graded ref only) or a different payload field, the row's
   `able to fail` wording still holds but the command in it should be swapped for the committed
   `--selftest` H5 case at integration. The committed case must print
   `selftest case=H5 positive=pass verdict=pass`, which the row already requires.
3. **The 6/8 figure is second-hand and non-durable.** It comes from verifier R1's reading of the L1's own
   scratch transcript, which is gone (`absent`, E2). The row says so; do not upgrade it to a re-run claim.
4. **Fixture derivation.** My future-dated fixture is the committed v5 receipt with one line changed, so its
   other limbs are real v5 values. ExecForgeFixtures' H5 fixture is a separate artifact; if the L1 prefers one,
   keep both (they falsify different limbs) or land ExecForgeFixtures' and keep mine as the recorded proof.
5. `5006097a`'s receipt file mtime (`17:12:08-0300`) is quoted only where wave-2 recorded it; git does not
   store mtimes, so the row does not lean on it.

## Tooling

None installed or upgraded this seat (no `uv tool install`, no `npx`, no binary fetch, no pacman — pacman is
paused host-wide). Only preinstalled bash, coreutils, git, diff, python3 were used.

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ExecMistakesDraft/` held the work tree (fixture generation, transcript
capture, replica development). It is removed before this seat yields, so no `kasegi-r40` scratch entry other
than the L1's own `--work` dir survives (H6).
