# MutC2Scanner — C2 mutation probe (round-87, attempt 1)

Seat: MutC2Scanner (mutation tester). Base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`,
freeze `afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69`, C2 landing
`132e16c588a2424c06b5ca15ea01fce1ee9a396d`.

Instrument under test: `corpus/instruments/capture-secret-scan.py`
(sha256 `b2bf9d65e0a2bea99003ea7fdb3aec237449abb4ccd301f45b3ce496d161c6d1`) with
`capture-secret-allow.tsv` (`f9fbd7e7…`) beside `claim-package-check.py` (`8b6f84…`).
Detector: frozen `.ufo/waves/round-87/c2/capability-check.py`
(`4fba0cbe…`), run **without** `--instrument-sha256` so the sha pin cannot be the killer.

**Baseline (pristine landing, same invocation): K1-K5 all pass, rc=0** →
C2 P1 holds at the landing commit independent of this seat. Everything below is a
routed defect for round 88, never a re-score.

## 1. Method

- `git clone --shared` of the lane into scratch; clone checked out at `132e16c`
  (`git -C <clone> rev-parse --show-toplevel` asserted `== <clone>` before every commit).
- 20 single-point mutants of the scanner. Each was written to the clone's
  `corpus/instruments/capture-secret-scan.py`, committed **inside the clone** under
  fixture identity, and judged at `HEAD` by

  ```
  python3 -B .ufo/waves/round-87/c2/capability-check.py --lane <clone> --rev HEAD \
    --work <scratch>/w --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6
  ```

- After each run the clone was hard-restored to `132e16c`; final state verified
  (`mutc2-restore.txt`): HEAD `132e16c…`, worktree clean, instrument sha
  `b2bf9d65…`, allowlist sha `f9fbd7e7…` — i.e. back to the frozen bytes.
- One deviation: `run_instr` ignores its timeout (M16 hung the counter; see §4), so
  that one run was executed under a 180 s harness timeout.

## 2. Result matrix (20 mutants)

| id | mutation (single point) | predicted detector | actual limbs | outcome |
|---|---|---|---|---|
| M01 | `aws-sts-session-token` shape deleted from `AWS_PATTERNS` | K1, K2, K4 | K1 K2 K4 FAIL | killed |
| M02 | STS regex loses `(?i)` case folding | survivor | all pass | **survived** |
| M03 | `aws-access-key-id` loses both `\b` boundaries | K1 | K1 FAIL | killed |
| M04 | `ALLOWED_VALUES` widened with a second key-id value | K4 | K4 FAIL | killed |
| M05 | `NEVER_ALLOWED` emptied | K4 | K4 FAIL | killed |
| M06 | `HEX64` relaxed to `{1,64}` | survivor | all pass | **survived** |
| M07 | allowlist key dropped the digest: `(path, shape)` | K3, K4 | K1 K2 K3 K4 FAIL | killed |
| M08 | scope clause `corpus/source-snapshots/` broken | K3, K4 | K1 K2 K3 K4 FAIL | killed |
| M09 | scope clause `-receipts` dropped | K4 | K3 K4 FAIL | killed |
| M10 | scope clause `live-` dropped | K4 | K1 K2 K3 K4 FAIL | killed |
| M11 | scope `-receipts` widened to substring match | survivor | all pass | **survived** |
| M12 | first-match `break` → `continue` | survivor | all pass | **survived** |
| M13 | `rc = 1 if hits else 0` → `rc = 0` | K2, K4 | K2 K4 FAIL | killed |
| M14 | `allowed` no longer incremented | K3 | K1 K3 FAIL | killed |
| M15 | `unused_allow` = `len(allow)` | K3 | K3 FAIL | killed |
| M16 | `read_blobs` off-by-one (`header[2] + 1`) | data desync | none (no verdict) | **inconclusive — hangs the counter** |
| M17 | symlink skip (`mode != 120000`) removed | survivor | all pass | **survived** |
| M18 | selftest expectation changed | K1 | K1 FAIL | killed |
| M19 | `ALLOWED_VALUES` bypass removed | K1, K4 | K1 K2 K3 K4 FAIL | killed |
| M20 | gate `SECRET_PATTERNS` dropped | K1, K4 | K1 K3 K4 FAIL | killed |

15 killed · 5 survived · 1 inconclusive (of 20). Kill/survive matched the
prediction for 19/20 (M16 was predicted to fail a limb; it hangs instead).

Limb load: sole killers were K1 (M03, M18), K3 (M15), K4 (M04, M05). K2 never killed
alone (M13 shared with K4). **K5 killed nothing** — it is a SCORECARD limb, not an
instrument limb; its only exercise is the pre-freeze "no SCORECARD row" control.

## 3. Survivors — measured behaviour and the control that would kill each

All probes ran the pristine instrument and the mutant instrument side by side on
scratch fixtures; receipts carry only `HIT`/summary lines and digests, never a matched
value (`mutc2-probes.txt`).

### 3.1 M02 — STS shape is case-sensitive if `(?i)` is lost (routed, highest value)

Strictly weaker: `x-amz-security-token=<value>` (lower case) is not matched by the AWS
shape. The gate's generic `credential` shape still fires, and that is the hazard:

```
M02b (pristine) rc=1  HIT shape=credential … / HIT shape=aws-sts-session-token …
M02b (M02)      rc=1  HIT shape=credential … (no aws-sts-session-token line)

M02c (pristine, relative path + allowlisted credential row) rc=1 hits=1 allowed=1
      HIT shape=aws-sts-session-token path=lower-sts-query.txt line=1
M02c (M02,      same allowlist)                             rc=0 hits=0 allowed=1
```

With the AWS shape case-blind, a lower-case session token can be **fully allowlisted
through a `credential` row**, which defeats the stated guarantee "a session token is
never a false positive" (`NEVER_ALLOWED` only refuses the STS shape name).

Why it survives: K1's selftest cases, K2's oracle regex
(`X-Amz-Security-Token=…`, case-sensitive) and K4's plants are all upper case.

Killing control (cheap, in K1): add a selftest case
`("lower-sts", b"x-amz-security-token=" + token + b"\\u0026X-Amz-Signature=1", {"aws-sts-session-token", "credential"})`
— M02 then fails K1. Equivalent K4 form: add a lower-case plant and require its
`(path, aws-sts-session-token)` pair in `PLANT_EXPECT`.

### 3.2 M06 — malformed allowlist digest accepted

`HEX64 = ^[0-9a-f]{1,64}$` accepts a short/partial digest; row validation is silently
weakened although the docstring promises "a refused or malformed row is a read error
(exit 2)":

```
M06 (pristine) row digest "abc" → CAPTURE-SECRET-SCAN error reason=OSError rc=2
M06 (M06)      row digest "abc" → CAPTURE-SECRET-SCAN … unused_allow=1 rc=0
```

Why it survives: K4 only exercises the *refused shape* path (`NEVER_ALLOWED`), never a
malformed digest.

Killing control: in K4, alongside `plant-allow-sts.tsv`, write
`plant-allow-short.tsv` with a 3-hex digest and require `rc2 == 2` for it as well.

### 3.3 M11 — scope widened from `p.endswith("-receipts")` to `"-receipts" in p`

Adds files to the scan set (false-positive side only):

```
fixture repo: 120000 corpus/source-snapshots/r/S900.txt, 100644 w/x-receipts-notes/a.json
M11 (pristine) scanned=0 hits=0 rc=0
M11 (M11)      scanned=1 hits=1 rc=1  HIT shape=credential path=w/x-receipts-notes/a.json
```

Why it survives: the landing tree contains no capture-class path that the widening
newly admits, so no limb's counts move.

Killing control: add `w/x-receipts-notes/a.json` (credential-shaped, benign value) to
K4's `PLANTS` and require its **absence** from `PLANT_EXPECT`; the widened rule then
reports an `extra` pair and K4 fails.

### 3.4 M12 — `break` → `continue`: per-shape match count no longer collapsed

```
fixture: one file with two credential-shaped matches
M12 (pristine) hit_lines=1  … scanned=1 hits=1
M12 (M12)      hit_lines=2  … scanned=1 hits=2
```

Why it survives: K2/K4 compare **sets** of `(path, shape)`; K3 requires `hits=0`. No
limb reads the `hits=` count or the number of `HIT` lines, so duplicate reporting is
invisible (unbounded output growth on a crafted capture is the risk).

Killing control: in K4 assert the summary count as well as the set —
`summ[1] == len(PLANT_EXPECT)` (K3's `summ[1] == 0` already does this for the clean
tree; K4 currently discards `summ`).

### 3.5 M17 — symlink skip removed (`mode != b"120000"`)

```
fixture repo: 120000 corpus/source-snapshots/r/S900.txt whose target text trips the STS shape
M17 (pristine) scanned=0 hits=0 rc=0
M17 (M17)      scanned=1 hits=2 rc=1  (credential + aws-sts-session-token at the link path)
```

Reading a symlink blob scans the *link target text*, so the guard is a false-positive
boundary, not a miss. The landing tree has 58 symlinks, none under a capture-class path
(checked with `git ls-tree -r 132e16c | awk '$1=="120000"'`), so the guard is unexercised.

Killing control: plant a `120000` blob whose target text trips a shape and require its
absence from `PLANT_EXPECT`.

## 4. Detector defect — a non-terminating instrument wedges the gate (M16)

M16 (`int(header[2]) + 1`) desynchronises the `cat-file --batch` header stream and the
mutant scanner blocks in `read()`. Measured on a 5-file capture fixture repo:

```
M16 (pristine) rc=1  scanned=5 hits=2
M16 (M16)      TIMEOUT after 25 s (instrument did not terminate)
```

Run through the frozen counter it did not finish in 1200 s, and again not in 180 s;
`LIMB` lines are never printed because `run_instr` calls `subprocess.run(...)` with **no
timeout** (capability-check.py line 86) and capture_output is buffered until exit. So a
wedged instrument produces no limb verdict at all — the gate hangs instead of failing
closed.

Routed defect (r88): give `run_instr` a bounded `timeout=` and treat
`subprocess.TimeoutExpired` as a `FAIL` on that limb with detail `timeout`. Re-runnable
demonstration: the fixture repo above plus any `--lane/--rev` invocation; the pristine
instrument returns in 0.0 s, M16 never returns.

## 5. Coverage observations for the planner

- 15/20 single-point weakenings are caught; the K1 selftest is load-bearing (2 sole
  kills) and K4's exact-set comparison is the strongest limb (2 sole kills, plus 8
  shared).
- The five survivors cluster into two classes: (a) **real detection gaps** — case-fold
  of the STS shape (M02) and digest validation (M06); (b) **unexercised guards** —
  scope widening (M11), per-shape match count (M12), symlink skip (M17). Class (a)
  should be closed in r88; class (b) is cheap to pin in the same pass.
- The counter has no timeout anywhere (`run_instr`), so "instrument fails to terminate"
  is indistinguishable from "counter still running".

## 6. Claims status (not re-scored)

- P1: baseline run of the frozen counter at `132e16c` prints
  `CAPABILITY-CHECK-RESULT pass rc=0` (K1-K5) — **pass**.
- P2: instrument and allowlist at `132e16c` hash to the frozen candidates
  (`b2bf9d65…`, `f9fbd7e7…`) — **pass** (read-only `git show`, §restore).
- Findings above are routed defects / qualifiers for round 88; no lane byte was changed.

## Receipts

`.ufo/waves/round-87/w1/MutC2Scanner-receipts/`

- `mutc2-baseline.txt` — pristine counter run at `132e16c` (K1-K5 pass).
- `mutc2-matrix.txt` — 20 mutants: mutation, predicted detector, limb matrix, outcome,
  mutant instrument sha256, mutant commit (inside the scratch clone).
- `mutc2-raw.txt` — per-mutant counter stdout, verbatim.
- `mutc2-probes.txt` — survivor probes (M02/M02b/M02c, M06, M11, M12/M12b, M17, M16)
  and the fixture repo trees.
- `mutc2-restore.txt` — restore evidence: clone HEAD back at `132e16c`, clean worktree,
  instrument/allowlist sha equal to the frozen candidates, lane bytes at `132e16c`
  re-hashed read-only.

Scratch (`/fast/scratch/hyaku/kasegi-r87/MutC2Scanner`) is deleted before yield; it
held the clone, the mutant sources and all fixtures. No mutant source, fixture byte or
planted value was written under `w1/`. No tool was installed for this seat.
