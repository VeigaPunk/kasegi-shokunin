# MutC2Gate — C2 `capture-intake-gate` mutation test (Kasegi round 90, attempt 1)

Seat: mutation tester for the C2 capability. Judged only on the frozen predicate at the
landing commit; every item below is a routed defect / coverage finding, not a re-score.

## Pin and method

- Instrument under test: `corpus/instruments/capture-source.py` at
  `643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2`, sha256
  `0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf`
  (extracted with `git show`; the `git archive` tree copy the counter builds hashes the same).
- Counter: `.ufo/waves/round-90/c2/capability-check.py` (sha256 `339c9801…`).
- 26 single-point mutants of the round-90 lines: `lane_rel` L109-112, `intake_gate` L115-123,
  the capture refusal branch L135-142, `main` exit path L188-194, `selftest` L149-174, plus the
  round-90 constants they read (`LANE` L48, `REFUSED_RC` L49). Each mutant is the pristine bytes
  with one byte-range replacement; every mutant compiles (`py_compile`), and the replacements are
  behaviour-bearing (no comment/docstring-only edits).
- Replay command (run from the lane, one `--work` per mutant, `python3 -B`, `TMPDIR=$S`):

```
python3 -B .ufo/waves/round-90/c2/capability-check.py \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --rev 643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 \
  --base-rev 6088c3eb0c29040415c69e7b5fb91e110480ab26 \
  --work <S>/w-<mutant> --instrument <mutant>.py \
  --instrument-sha256 0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf \
  --seed 9090
```

- Seeds: every mutant at `--seed 9090`; each survivor re-run once with a runtime seed
  (`random.SystemRandom`, printed in the receipt). Two pristine runs (9090 and runtime seed
  `1285815401`) both pass G0-G6 and P with rc 0, so a mutant failure is attributable to the mutant.
- The `P` limb fails on every mutant by construction (it pins the landed digest); verdicts are
  therefore read from the behavioural limbs G0-G6 only. Counter rc is 1 for every mutant for the
  same reason. Baseline rc is 0.

## Baseline (landed bytes, no `--instrument`)

| seed | G0 | G1 | G2 | G3 | G4 | G5 | G6 | P | rc |
|---|---|---|---|---|---|---|---|---|---|
| 9090 | pass | pass | pass | pass | pass | pass | pass | pass | 0 |
| 1285815401 | pass | pass | pass | pass | pass | pass | pass | pass | 0 |

## Mutants

19 killed, 7 survived. `Killed by` lists the behavioural limbs that failed; `P` is omitted
(identity pin, fails on all).

| # | mutant | line | single-point change | verdict | killed by |
|---|---|---|---|---|---|
| M01 | gate-after-write | L135-142 | gate moved below `makedirs`/`open`/`write` | KILLED | G1,G2,G4,G5,G6 |
| M02 | refusal-falls-through | L138-139 | refusal prints but `return None` deleted, falls through to write | KILLED | G1,G2,G4,G5,G6 |
| M03 | refuse-only-multi-shape | L136 | `if found:` -> `if len(found) > 1:` | KILLED | G1,G4,G5 |
| M04 | refusal-echoes-value | L138 | refusal line appends the converted body (`%r`) | KILLED | G1 (leak) |
| M05 | refusal-omits-shape | L138 | refusal prints `shape=unknown` instead of the shape name | KILLED | G1 (named) |
| M06 | gate-first-256-bytes | L135 | gate scans `data[:256]` | SURVIVED | — |
| M07 | gate-fails-open | L122-123 | exception handler returns `[]` | KILLED | G4,G5 |
| M08 | gate-except-import-only | L122 | `except Exception` -> `except ImportError` | KILLED | G4,G5 |
| M09 | gate-returns-empty | L121 | `return found` -> `return []` | KILLED | G1,G2,G4,G6 |
| M10 | gate-ignores-allowlist | L119 | allowlist load -> `{}` | KILLED | G3,G4 |
| M11 | gate-scans-abs-path | L120 | path arg `lane_rel(out)` -> `abspath(out)` | KILLED | G3,G4 |
| M12 | lane-rel-always-abs | L112 | always return the absolute path | KILLED | G3,G4 |
| M13 | lane-rel-from-cwd | L111 | relpath base `LANE` -> `os.getcwd()` | SURVIVED | — |
| M14 | lane-root-one-level-short | L48 | `LANE` one directory short | KILLED | G3,G4 |
| M15 | lane-rel-no-outside-guard | L112 | return `rel` even when it starts with `..` | SURVIVED | — |
| M16 | main-refusal-rc-zero | L192-193 | refused branch returns 0 | KILLED | G1,G2,G4,G5 |
| M17 | refused-rc-one | L49 | `REFUSED_RC` 3 -> 1 | KILLED | G1,G2,G4,G5 |
| M18 | main-check-inverted | L192 | `is None` -> `is not None` | KILLED | G1,G2,G3,G4,G5 |
| M19 | selftest-always-zero | L174 | selftest returns 0 unconditionally | SURVIVED | — |
| M20 | selftest-assumes-refusal | L171 | refusal exercise replaced by `refused=True` (capture call removed) | SURVIVED | — |
| M21 | selftest-refusal-inverted | L171 | refusal test inverted (`is not None`) | KILLED | G6 |
| M22 | default-allow-path-dropped | L119 | default allowlist join dropped (`load_allow(None)`) | KILLED | G1,G3 |
| M23 | gate-error-treated-as-clean | L136 | `gate-error` entries filtered before refusal | KILLED | G4,G5 |
| M24 | gate-skips-text-kind | L135 | gate skipped when `--kind text` | SURVIVED | — |
| M25 | gate-first-shape-only | L121 | `return found[:1]` | KILLED | G1 (`aws-sts-session-token` not named) |
| M26 | selftest-plant-shortened | L164 | selftest STS fixture 65 -> 17 chars | SURVIVED | — |

Killed notes worth keeping: M01 shows G1/G2/G5 do test "refuse before write"; M03 shows the
counter's plant bodies each trip one shape except the STS plant (generic + STS), which is why the
single-shape AWS plant still refused under M03; M10's G3 failure is the allowlisted S128 snapshot
being refused once the allowlist is ignored, and its G4 failure is the never-allowed STS row never
being loaded; M11/M12/M14 fail G3 as well as G4 because they change the path key the allowlisted
S128 row binds to; M25 is caught only by the STS plant because `credential` is matched first.

## Survivors and the limb/plant that would kill each

Probes are scratch-only, run against the same extracted tree with a loopback HTTP server; they
print rc / written / shape only (see `MutC2Gate-receipts/probes.log`).

| survivor | probe | pristine | mutant | kill limb |
|---|---|---|---|---|
| M06 (gate scans 256 B) | P1: text with >256 B of clean prose before the matching value | rc 3, not written | rc 0, written | G1 with one plant padded past 256 bytes of converted text (same for G2/G4). Current G1 bodies put every hit in the first ~40 bytes, so the gate input length is unpinned. |
| M13 (relpath from cwd) | P2: allowlisted lane-relative path; instrument run cwd=lane vs cwd=other | rc 0 written in both cwds | rc 0 written at cwd=lane; rc 3 refused at cwd=other | A G4 run whose cwd is not the extracted lane root (the counter always runs cwd=T). This is a spurious-refusal direction: the digest-bound allow row stops matching when the instrument is invoked elsewhere. |
| M15 (no `..` guard) | P3: `--out` outside the lane root, allow row keyed by the `lane_rel` `../…` string | rc 3, not written | rc 0, written outside the lane | A G4 variant with `--out` outside the lane root and a row whose path is the relative `..` form. This is the dangerous direction: the guard is what stops a row from authorising a write outside the lane the allowlist is lane-relative to. |
| M19 (selftest always 0) | P5a: selftest with one assertion forced false (`kept=False`) | rc 1 | M19+kept-false rc 0 | A G6b limb that runs `--selftest` on an instrument whose selftest assertion actually fails and requires rc 1. G6 only checks rc 0 on the mutant's own selftest, which passes by construction. |
| M20 (refusal exercise deleted) | P5b: `--selftest` stdout | rc 0, `INTAKE-REFUSED` lines for `credential` and `aws-sts-session-token` | rc 0, no `INTAKE-REFUSED` line at all | A G6 assertion on stdout: require at least one `INTAKE-REFUSED` line and the STS shape. G6 reads only rc. (`kept` still catches write-through, so the deletion is invisible only because the gate happens to be intact.) |
| M24 (gate skipped for text) | P4: `--kind text` input carrying a matching value | rc 3, not written | rc 0, written | G1 with a text-kind plant (or G3 capturing a hit-bearing snapshot as text and requiring refusal). All 11 G1 plants are HTML (default kind); G3's three text inputs are clean, so the dominant capture kind is never refused in the counter. |
| M26 (selftest fixture shortened) | P5c: `--selftest` stdout shapes | rc 0, `credential` + `aws-sts-session-token` | rc 0, `credential` only | A G6 assertion that the STS shape line appears (or a tightened generic-shape value floor). The 17-char value still matches the generic `credential` shape, so the selftest still refuses and rc stays 0 while the STS pattern is no longer exercised. |

All seven survivors were re-run at a runtime seed and survived again (seeds in `mutants.tsv`).

## Routed coverage findings (counter, not the claim)

1. **Text/PDF capture kinds are never planted** (M24): G1/G2/G4 use HTML only; G3's text inputs
   are clean. A gate that skips `--kind text` passes the whole counter, although text snapshots
   are the dominant captured kind.
2. **Allowlist path binding is only tested from one cwd** (M13) and **never outside the lane
   root** (M15). The latter is a write-outside-lane bypass when an allow row uses the relative
   `..` path that `lane_rel` is supposed to prevent from binding.
3. **G6 is rc-only** (M19, M20, M26): it cannot tell an asserted refusal from an assumed one, a
   failing assertion from a passing one, or which shape fired. It also never inspects the
   `INTAKE-REFUSED` lines it prints. A G6b that runs `--selftest` on a deliberately broken
   instrument and requires rc 1, plus assertions on the printed shape(s), would cover M19/M20/M26.
4. **No minimum scan length / no padded plant** (M06): a hit past byte 256 of the converted body
   is written. G1 plants are short.
5. **Multi-shape reporting is only indirectly covered** (M25 killed, but M03 shows the single-shape
   plants hide the `>1` case except for the STS plant). A plant that trips exactly two generic
   shapes would pin the "one line per shape" docstring claim directly.

## Hygiene, bounds, tooling

- No lane file was edited: `git show`/`git archive` only; the lane worktree bytes of
  `corpus/instruments/capture-source.py` are still `0630d32b…` after the seat. No git/jj writes
  anywhere; no fixture repositories; no sysctls; no sudo; network was loopback only (plus no
  external fetch at all).
- No credential-shaped value was written into the wave directory. Fixtures live in scratch only;
  the probe fixture is a 16-char placeholder that matches the generic `credential` shape, and
  receipts carry rc/booleans/shape names/hashes only. The scanner was run over all six new wave
  files as a self-check: `CAPTURE-SECRET-SCAN mode=files scanned=6 hits=0 files=0 allowed=0
  unused_allow=19 rc=0`.
- Scratch `S=/fast/scratch/hyaku/kasegi-r90/MutC2Gate` is deleted before yield; no counter output
  was written under `/tmp`.
- No tools installed or upgraded; nothing installed this seat.

## Files written

- `.ufo/waves/round-90/w1/MutC2Gate.md` (this report)
- `.ufo/waves/round-90/w1/MutC2Gate-receipts/mutants.tsv`
- `.ufo/waves/round-90/w1/MutC2Gate-receipts/baseline.log`
- `.ufo/waves/round-90/w1/MutC2Gate-receipts/mutant-limbs.txt`
- `.ufo/waves/round-90/w1/MutC2Gate-receipts/probes.log`
- `.ufo/waves/round-90/w1/MutC2Gate-receipts/pins.txt`
