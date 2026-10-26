# ReviewerH5H6Fixtures — round-40 wave 1 receipt

Seat: reviewer (leaf; no subagent dispatch). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
only; fleet root read-only; no git/jj mutation anywhere (read-only git only). Route: fleet-root cwd →
own scratch `S=/fast/scratch/hyaku/kasegi-r40/ReviewerH5H6Fixtures`; all reads/writes absolute.
Disk guard before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
`/fast/scratch/hyaku 26% free 601.7G` — green.

Item: review the H5/H6 fixture deliverables (ExecForgeFixtures, ExecH6ScratchFixtures) once present:
confirm the forged-payload and future-dated receipts are genuine violations (a naive fix would miss
them), confirm the expected verdicts are the frozen predicate's, and confirm the sibling-dir probe is
hermetic. Deliver verdicts per fixture; no lane edits.

## Deliverables (byte stats, measured)

| File | Lines | Bytes | sha256 |
|---|---|---|---|
| `ReviewerH5H6Fixtures.txt` | 4 | 1040 | `d9e9c72e9d314da4c5323d701964f5e6c32b02234eff6f51e7802290a058316c` |
| `ReviewerH5H6Fixtures.md` | this receipt, written last |

## Reviewed artifacts (final bytes)

| Artifact | sha256 | lines |
|---|---|---|
| `ExecForgeFixtures.forged-payload.txt` | `09388af91592e51f867de95cb755f2e822d6a15d43a5e9f69a64cb18cf281cef` | 33 |
| `ExecForgeFixtures.future-dated.txt` | `2a1f2c77466edab3a728868e7fe378f07df9738115435a43bd4a395e584be9ee` | 33 |
| `ExecForgeFixtures.expected.txt` | `4bc9f96a7a70fced5db81e00b29c7a05b14f9bf9b0bf0f1066c8c0f5a5e8ff55` | 2 |
| `ExecH6ScratchFixtures.sibling-dir.sh` | `202f46bddd524284f54f6cde4332d842ef16243a1f14e14873461b4f1b3d8339` | 434 |

## H5 verdicts

### V1 — ExecForgeFixtures.forged-payload.txt: PASS

Genuine violation, confirmed independently:
- Both fixtures are round-40-shaped transcripts (`all-gates v6`, `export-ref=8371e7ac…`, ten `H<n> payload=… closed=1`
  lines, `closed=10/10 exit=0`, ten graded `selftest case=H<n> positive=pass mutants=n/n verdict=pass` lines,
  `selftest cases=10 failures=0`).
- Exported the named ref and re-derived the true H2 count:
  ```
  $ git -C <lane> archive 8371e7ac9f32cae5ed72f8c28205634603f836fa | tar -xf - -C S/export8371
  $ for f in SCORECARD.md LOG.md SHONEN.md corpus/lessons/round-39.md; do grep -c '^Correction (round 40)' S/export8371/$f; done
  → 0 0 0 0
  ```
  The receipt records `H2 payload=corrections=4,files=4 closed=1` — mismatches (4 vs 0, 4 vs 0). This is the
  frozen example verbatim ("a check line claims a correction count that is absent from the export").
- Naive fix would miss it: I ran the seat's shape-only validator (r39 G2 semantics, H-ids — sentinel,
  ten `closed=1` run lines, tally, ten graded case lines, summary; never compares payload values, never reads
  `run-utc`) against both fixtures:
  ```
  naive-shape ExecForgeFixtures.forged-payload.txt … accepted=1 → exit 0
  naive-shape ExecForgeFixtures.future-dated.txt … accepted=1 → exit 0
  ```
  A shape-only fix accepts both, so the fixtures discriminate the real H5 (payload cross-check + date bound)
  from the naive fix.
- Strict H5 (named recomputable fields: H2 `corrections=`/`files=` vs export; `run-utc` vs export commit time)
  rejects it on the payload limb, other limbs green:
  ```
  H5 payload=xref=1,run-utc=2026-10-26T20:55:17Z,corrections=0(recorded=4),files=0(recorded=4),dated=ok closed=0 → exit 1
  ```
- expected.txt verdict `rejected closed=0 limb=H2.payload.corrections` matches the frozen predicate (H5: the
  forged/tampered receipt "is rejected"); the stated reason is factually correct (measured here).

### V2 — ExecForgeFixtures.future-dated.txt: PASS

Genuine violation, confirmed independently:
- `run-utc=2027-01-01T00:00:00Z` vs export-commit time of its own `export-ref`:
  ```
  $ git -C <lane> log -1 --format='%ct %cI' 8371e7ac9f32cae5ed72f8c28205634603f836fa
  1793048117 2026-10-26T17:55:17-03:00      # = 2026-10-26T20:55:17Z
  $ date -u -d '2027-01-01T00:00:00Z' +%s  → 1798761600 > 1793048117
  ```
  Post-dates the tree it describes by ~66 days; the transcript cannot be that tree's run.
- Minimal: `diff` against the honest control shows exactly one changed line (run-utc). Its H2 payload
  (`corrections=0,files=0`) is truthful at 8371e7a, so the payload limb stays green and the date limb alone
  carries the rejection:
  ```
  H5 payload=xref=1,run-utc=2027-01-01T00:00:00Z,corrections=0(recorded=0),files=0(recorded=0),dated=future closed=0 → exit 1
  ```
- Naive shape accepts it (above). Honest control (line 4 restored) passes all limbs (`closed=1`, exit 0).
- expected.txt verdict `rejected closed=0 limb=run-utc.future-dated` matches the frozen predicate; stated
  reason is factually correct (measured here).

### V3 — ExecForgeFixtures.expected.txt: PASS

Both verdict lines are exactly what the frozen H5 predicate demands (rejected / not-closed), with accurate
per-limb reasons; line counts and hashes match the seat's receipt. Independent arithmetic agrees (V1/V2).

### H5 observations (non-blocking, for L1/suite-builder)

1. The forged-payload fixture is over-forged at 8371e7a: besides H2, its `H1 suite=1,registry-row=1` (no
   `r40-closure.sh`, no SKILL.md registry row at that ref), `H3 criterion=1,cites=M39-2` (no M39-2 citation in
   QUALITY.md at that ref) and `H4 url=1,date=1,quote=1` (round-39 lesson S056/S058/S059 rows are bare
   bullets there) also contradict the export. Rejection is therefore robust to any checked subset of limbs,
   but the fixture is not a strict single-field forgery; the single-field case is covered by
   `ExecMistakesDraft.h5-replica.sh`'s `declared=3` probe and by the wave-2 `CritReceiptForge` one-field
   mutations (per ExecForgeFixtures.md §4).
2. `suite-sha256=2856a210…` is the r39 instrument digest (resolvable at 8371e7a) — deliberate fabrication,
   well-formed under the only receipt checker existing today; the suite builder owns the r40 sentinel token
   (v6 assumed, per ExecForgeFixtures.md §5).
3. Pairing: both fixtures bind to the frozen 8371e7a export. The H5 graded case must validate them against
   that ref (by their `export-ref`), or rebind per ExecForgeFixtures.md §4; validating against Y without
   rebinding would reject on xref instead of the target limb.

## H6 verdict

### V4 — ExecH6ScratchFixtures.sibling-dir.sh: PASS

Discrimination (ran the final 15375-byte bytes myself; `bash -n` clean):
- Full matrix: `probe scenarios=21 failures=0`, `probe exit=0` (TMPDIR pinned to my scratch; sandbox removed
  by the EXIT trap afterwards).
- Required RED/GREEN pair reproduced: strays `kasegi-r39-stray/` + `kasegi-r40-stray/` with a clean `--work`
  → `closed=9/10 exit=1`, payload names both strays; after removal → `closed=10/10 exit=0`.
- The passed `--work` dir itself never reds: clean single-child chain under a matching entry → green
  (`work=inside,tolerated=kasegi-r40-seat`); junk inside the work dir (export/, mut/, files) → green;
  a sibling leftover next to the work chain → red.
- T5 sibling-mutant family covered: `kasegi-r40-build-extra`, `kasegi-r40x`, `.kasegi-r40-seat` (one leading
  dot stripped by `lane_name`), file named `kasegi-r40-l1`, symlink to a foreign dir — all red; `kasegi-r41*`
  and other non-round names ignored. The r39 G6 exact-name defect is genuinely closed: the family glob catches
  `kasegi-r39-l1`-style names (I reproduced red for `kasegi-r39-l1`).
- Adversarial probes beyond the matrix, all as expected: exact `kasegi-r39`/`kasegi-r40` names red; regular
  file matching the family red (fail-closed on presence); dangling symlink red; symlink loop red; uppercase
  `KASEGI-…` ignored (frozen pattern is lowercase); nested (non-top-level) matching dir ignored (documented
  top-level-only policy); missing `--work` or missing scratch root → `read=fail closed=0` red, never "zero
  entries"; `--work` == scratch root with a stray inside → red.

Hermeticity:
- `refuse_real_root` refuses the live root, `/`, and every ancestor of `/fast/scratch/hyaku`
  (measured exit 2: `/fast/scratch/hyaku`, `/fast/scratch`, `/`). Non-existent roots with a would-be
  ancestor path are refused too (`realpath -m`).
- Matrix mode creates its own mktemp sandbox under `${TMPDIR:-/tmp}` only; every write site is under `$SB`
  (checked by code review). `--check` mode never creates or modifies dirs. The only touch of the real root is
  a `cd`+`pwd` resolution inside the refusal guard — no entry scan, no write; header claim `real-root-read=no`
  is honest.
- Sandbox cleanup verified: my matrix run left no `h6-sibling-dir.*` leftover in my scratch; the seat's own
  `transcript.out` teardown shows `sandbox-removed=1`. No real `/fast/scratch/hyaku/kasegi-r40/*` siblings
  were created or disturbed by my runs (only files inside my own seat scratch).

H6 observations (non-blocking):
1. The H6 payload labels a present-but-tolerated family as `r39=empty`/`r40=empty` (e.g.
   `r40=empty,work=inside,tolerated=kasegi-r40-seat`). Semantically it means "family clean (no stray)";
   the label choice is odd but the verdict is correct and the needle assertions used by the scenarios pass.
2. `--root`/`--scratch-root` *inside* the real root (e.g. a seat's own scratch path) is deliberately allowed —
   seats' scratch lives under `/fast/scratch/hyaku`; the probe's guarantee is that it refuses the root itself
   and ancestors, never that it refuses sub-paths. Matrix mode with `--root` inside the real root writes only
   within that dir.
3. The seat's own transcripts (`transcript.sh`/`transcript.out`) show the required RED→GREEN sequence with
   the real stray named `kasegi-r39-l1` (the exact kill-rule name) and `sandbox-removed=1`.

## Tooling

None installed or upgraded (no pacman — paused host-wide; no uv/npx/network). Used preinstalled bash,
coreutils, git, tar, diff, python3, date.

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ReviewerH5H6Fixtures/` (seat-specs.txt, export8371/, probe-current.sh,
naive-shape.sh, strict-h5.sh, control-honest.txt, h6-final-matrix.out, h6adv/ h6adv2/) — removed after the
deliverables and this receipt were copied to the wave dir. No scratch path survives.

Report: .ufo/waves/round-40/wave1/ReviewerH5H6Fixtures.md
