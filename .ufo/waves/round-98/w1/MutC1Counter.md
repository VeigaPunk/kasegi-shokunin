# MutC1Counter — round-98 C1 control-set mutation test

Seat: `MutC1Counter` (leaf; no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `2133f5bd993aaf34efad795d5e0b588485401fb2`,
freeze `12bb2f98cf9d07bcbc8b62985516cc3ff65d9ae8`, C1 landing `e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`,
C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`.

Target: `corpus/instruments/census-at-rev.py` (sha256
`66383371211bf4b801df608d5e20c23e2b51457717fcb1b76de471b8feb62502`, matches the C1
`instrument_sha256` pin). Detector: the frozen control harness
`.ufo/waves/round-98/controls/c1-controls-r98.py`, run as committed at the C1 landing
(sha256 `d97132684455aa6cca5bd65dd0e07a94942b8469801d05f219ba3a52b47ecc1a`; the claim's
`harness_sha256` `d39a1fc8…` matches neither the freeze bytes `0488d796…` nor the landing bytes
— see §6). Every mutant was copied into the harness's own fixture clone; the lane was never
edited. Receipts: `MutC1Counter-receipts/`.

## 1. Method

Twelve single-point mutants were generated from the pristine instrument by exact-string
replacement (each anchor asserted to occur exactly once; `receipts/01-generate.txt`). Eleven
are one textual hunk; M12 is one behavioural point expressed as three hunks (signature,
assignment, call site). All twelve compile (`py_compile`). The frozen harness was invoked once
per mutant with the mutant as `--instrument` (an absolute path; the harness's
`os.path.join(lane, abs)` yields the absolute path), the fixture's copied instrument was
hash-checked equal to the mutant (`copy=ok` in `receipts/00-index.tsv`), and the harness's own
8 controls decided the verdict:

```
HOME=$S/fakehome python3 -B .ufo/waves/round-98/controls/c1-controls-r98.py \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work $S/runs/<mutant> \
  --instrument $S/mutants/<mutant>.py --base 2133f5bd993aaf34efad795d5e0b588485401fb2
```

`rc=1` with at least one `CONTROL … FAIL` = **killed**; `rc=0` with
`C1-CONTROLS-RESULT pass controls=8` = **survived**; `rc=2` setup error = inconclusive (none
occurred under the controlled HOME).

### 1.1 Environment: real HOME is unusable on this host, controlled HOME is validated

The first three baseline runs with the real `HOME` died with `CENSUS-WRITE error
reason=resolve-rc-15` (`receipts/00-baseline.txt`, `00-baseline-retry.txt`,
`00-baseline-retry2.txt`). `journalctl` shows `earlyoom` sending SIGTERM to my `resolve.py`
at VmRSS 2191, 2713 and 3528 MiB (`receipts/05-earlyoom-evidence.txt`). Cause: the base
corpus cites `` `~/Projects/**` ``; `resolve.py`'s `exists_any()` expands it with
`glob.glob(..., recursive=True)` over the real host tree (confirmed: `is_pathlike` and
`GLOBMETA` both true for that token). Under the 13-seat wave the host is at ~29/31 GB RAM and
~22/31 GB swap, so that expansion is killed.

A controlled `HOME` with a 4-file `Projects/` tree makes the same frozen harness complete in
25 s (`receipts/00-baseline-fakehome.txt`, 8/8 pass). It changes only the host-dependent part
of the measurement, which the instrument already reports separately (R142):

```
HOME=$S/fakehome python3 -B corpus/instruments/census-at-rev.py --lane . \
  --rev e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 --work $S/runs/rev-e2caf4a1
CENSUS rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78
```

The committed census's pinned line is
`SKILL 162/732 = 22.13% | corpus 2551/7559 = 33.75% | lane 2589/7961 = 32.52%`
(`corpus/instruments/citation-survival.md:6`): the pinned (INTERNAL-only) triple is identical
under the controlled HOME. Only the host-inclusive line shifts (168/732 and 2628/7559 under
the controlled HOME vs 166/732 and 2629/7559 in the committed census), which is exactly the
host-owned part the instrument documents as not revision-stable. All mutant runs therefore
use the controlled HOME; the pinned comparison the controls exercise is unchanged.

## 2. Baseline (detector validity)

`receipts/00-baseline-fakehome.txt`:

```
CONTROL candidate rc=0 want=0 PASS reason=none declared=none
CONTROL do-nothing rc=1 want=1 PASS reason=no-measured-at declared=no-measured-at
CONTROL tampered-pinned rc=1 want=1 PASS reason=pinned-mismatch declared=pinned-mismatch
CONTROL stale-rev rc=1 want=1 PASS reason=pinned-mismatch declared=pinned-mismatch
CONTROL no-pinned-line rc=1 want=1 PASS reason=no-pinned-line declared=no-pinned-line
CONTROL missing-file rc=2 want=2 PASS reason=missing-file declared=missing-file
CONTROL bad-revision rc=2 want=2 PASS reason=bad-revision declared=bad-revision
CONTROL no-resolve rc=2 want=2 PASS reason=no-resolve declared=no-resolve
ATTRIBUTION pass fixtures=8
C1-CONTROLS-RESULT pass controls=8 rc=0
```

The pristine instrument is not killed by its own control set, so a mutant kill is attributable
to the mutant, not to a baseline failure.

## 3. Matrix

| # | mutant | single-point defect | harness | FAIL controls | verdict |
|---|---|---|---|---|---|
| M01 | `no-measured-at-format` | `^measured-at: (.+)$` (40-hex pin dropped) | rc=0 | none | **survived** |
| M02 | `write-accepts-any-rev` | `--write` drops the 40-hex `fullmatch` | rc=0 | none | **survived** |
| M03 | `no-pinned-compare` | `if got != want:` → `if False:` | rc=1 | tampered-pinned, stale-rev | **killed** |
| M04 | `compare-only-skill` | compares only the SKILL segment | rc=1 | stale-rev | **killed** |
| M05 | `no-host-owned-line` | header omits `host-owned inputs` | rc=0 | none | **survived** |
| M06 | `accept-missing-pinned` | missing pinned line → rc 0 | rc=1 | no-pinned-line | **killed** |
| M07 | `cache-by-lane` | cache key `lane.json`, not `rev + ".json"` | rc=1 | stale-rev, bad-revision, no-resolve | **killed** |
| M08 | `body-from-lane-tree` | body read from lane worktree, not extract | rc=0 | none | **survived** |
| M09 | `ignore-resolve-rc` | resolve.py's non-zero exit ignored | rc=0 | none | **survived** |
| M10 | `accept-12-char-rev` | `^measured-at: ([0-9a-f]{12,40})$` | rc=0 | none | **survived** |
| M11 | `pinned-uses-host-inclusive` | pinned line filled from `*_host` counts | rc=0 | none | **survived** |
| M12 | `check-trusts-cli-rev` | check measures `--rev`, not `measured-at` | rc=1 | stale-rev | **killed** |

5 killed, 7 survived. Mutant hashes and hunk counts: `receipts/07-matrix-evidence.txt`;
per-mutant diffs and outputs: `receipts/mNN-*.diff` / `receipts/mNN-*.txt`.

## 4. Killed mutants — the control that caught each

**M03 `no-pinned-compare`** — the comparison is disabled, so both comparison controls pass a
census they must reject (`receipts/m03-no-pinned-compare.txt`):

```
CONTROL tampered-pinned rc=0 want=1 FAIL reason=none declared=pinned-mismatch
CONTROL stale-rev rc=0 want=1 FAIL reason=none declared=pinned-mismatch
```

**M04 `compare-only-skill`** — killed by `stale-rev`, and the reason is instructive: the SKILL
field is revision-stable across the base and the round-97 stale rev, while corpus/lane are not
(`receipts/m04-compare-only-skill.txt`):

```
CONTROL stale-rev rc=0 want=1 FAIL reason=none declared=pinned-mismatch
CENSUS-CHECK pass rev=b06af5e07efbd961a8449f7de6b57eeea62c6bd3 skill=162/732 corpus=2527/7497 lane=2565/7899 host_owned=77
```

The candidate's pinned line is `SKILL 162/732 | corpus 2550/7556 | lane 2588/7958`
(fixture headers in `receipts/07-matrix-evidence.txt`; the same numbers appear in
`receipts/m07-cache-by-lane.txt`). The stale mismatch is therefore entirely in corpus/lane; a
mutant that ignores those fields misses it, and `stale-rev` kills it.

**M06 `accept-missing-pinned`** — a census with the pinned line removed is accepted
(`receipts/m06-accept-missing-pinned.txt`):

```
CONTROL no-pinned-line rc=0 want=1 FAIL reason=none declared=no-pinned-line
CENSUS-CHECK pass rev=bc27ee1d8a0c3d5832a94e310de995271ef4460f (no pinned line)
```

**M07 `cache-by-lane`** — one cache entry serves every revision, so the stale, bad-revision and
no-resolve controls all return the write's measurement instead of their own outcome
(`receipts/m07-cache-by-lane.txt`):

```
CONTROL stale-rev rc=0 want=1 FAIL reason=none declared=pinned-mismatch
CONTROL bad-revision rc=0 want=2 FAIL reason=none declared=bad-revision
CENSUS rev=0000000000000000000000000000000000000000 skill=162/732 corpus=2550/7556 lane=2588/7958 host_owned=78
CONTROL no-resolve rc=0 want=2 FAIL reason=none declared=no-resolve
CENSUS rev=94c8a11ee9a9c078fbac7c47b4775b5342cd16e8 skill=162/732 corpus=2550/7556 lane=2588/7958 host_owned=78
```

**M12 `check-trusts-cli-rev`** — the check measures the harness's `--rev` (`rev_cand`) instead
of the file's `measured-at`, so the stale census's pinned line matches and the control cannot
see the stale revision (`receipts/m12-check-trusts-cli-rev.txt`):

```
CONTROL stale-rev rc=0 want=1 FAIL reason=none declared=pinned-mismatch
CENSUS-CHECK pass rev=a49ab8be0845bbd5ab5c7bfe0beff5893775f1c8 skill=162/732 corpus=2550/7556 lane=2588/7958 host_owned=78
```

## 5. Survivors — the limb each escapes, and the routed gap

Each survivor was confirmed to be a real behavioural defect by a direct probe or by the
mutant's own written artifact; the frozen 8 controls simply never present the triggering
input. Probe outputs: `receipts/06-survivor-probes.txt`; artifacts:
`receipts/07-matrix-evidence.txt`.

**M01 `no-measured-at-format` — escaped limb: the `measured-at` 40-hex format pin.**
Probe P2 uses a census whose `measured-at:` is the tag `cand` pointing at the candidate rev:

```
pristine: CENSUS-CHECK fail reason=no-measured-at rc=1
M01:      CENSUS-CHECK pass rev=cand skill=162/732 corpus=2550/7556 lane=2588/7958 host_owned=78  rc=0
```

No control feeds a non-hex `measured-at`; `do-nothing` has no line at all, so `(.+)` and the
40-hex regex are indistinguishable to the harness. Routed gap: a control that writes
`measured-at: <tag>` (or `HEAD`) into an otherwise valid census and requires rc=1
`no-measured-at`.

**M02 `write-accepts-any-rev` — escaped limb: `--write` revision validation.** Probe P3:

```
pristine: CENSUS-WRITE error reason=bad-revision rc=2
M02:      CENSUS-WRITE ok rev=cand skill=162/732 lane=2588/7958 host_owned=78  rc=0
          measured-at: cand
```

The harness only calls `--write` with a 40-hex rev; the `bad-revision` control exercises
`--rev` in *measure* mode, not the `--write` path. Routed gap: a control that calls
`--write --rev <non-hex>` and requires rc=2 `bad-revision`.

**M05 `no-host-owned-line` — escaped limb: emission of the `host-owned inputs` header line.**
The mutant's census header has only `measured-at`, `pinned`, `host-inclusive` before `---`
(`receipts/07-matrix-evidence.txt`); the harness still passes 8/8. `check` never reads that
line, and its printed `host_owned=` comes from the measurement, not the file. Routed gap: a
control that greps the written census for `^host-owned inputs: <n> ` and compares `n` to the
measurement.

**M08 `body-from-lane-tree` — escaped limb: body provenance.** The mutant writes the base
census body (the lane worktree's file) under a fresh header: header pinned
`corpus 2550/7556 | lane 2588/7958`, body `Scope: … (224 files)` and
`distinct path-like citations: **5152**` — while the pristine body is
`Scope: … (333 files)` / `**7958**` (`receipts/07-matrix-evidence.txt`). The harness passes
8/8 because `check` compares only the header's pinned line. Routed gap: a control that
compares the written body's `Scope:`/`distinct path-like citations` lines (or the whole body)
to resolve.py's fresh output for the same rev.

**M09 `ignore-resolve-rc` — escaped limb: resolve.py's non-zero exit.** Probe P4 uses a
fixture whose `resolve.py` writes a valid TSV and exits 1:

```
pristine: CENSUS error reason=resolve-rc1 rc=2
M09:      CENSUS rev=f62367a15a8bf4be7f91dce04d0851901472ac7e skill=1/1 corpus=0/1 lane=1/2 host_owned=1  rc=0
```

The frozen `no-resolve` control deletes `resolve.py`, which is caught earlier in `extract()`;
the “present but failing” path is never exercised. Routed gap: a control with a resolve.py
that exits non-zero after writing a TSV, expecting rc=2 `resolve-rc1`.

**M10 `accept-12-char-rev` — escaped limb: `measured-at` length validation.** Probe P1:

```
pristine: CENSUS-CHECK fail reason=no-measured-at rc=1
M10:      CENSUS-CHECK pass rev=fac43d87ee97 skill=162/732 corpus=2550/7556 lane=2588/7958 host_owned=78  rc=0
```

All controls use a full 40-hex rev; `git archive` happily resolves the 12-char prefix, so the
mutant is self-consistent. Routed gap: a control that feeds a 12-char (or otherwise
abbreviated) `measured-at` and requires rc=1 `no-measured-at`.

**M11 `pinned-uses-host-inclusive` — escaped limb: the pinned line's INTERNAL-only
semantics.** The mutant's census records the host-inclusive counts *as* the pinned line
(`receipts/07-matrix-evidence.txt`):

```
pinned rate (INTERNAL only; revision-stable): SKILL 168/732 = 22.95% | corpus 2627/7556 = 34.77% | lane 2666/7958 = 33.50%
host-inclusive rate (resolve.py's definition): SKILL 168/732 = 22.95% | corpus 2627/7556 = 34.77% | lane 2666/7958 = 33.50%
```

while the pristine pinned line is `162/732 | 2550/7556 | 2588/7958`. The harness passes 8/8
because `check` recomputes `want` with the same mutant and compares it to the file's line; no
control asserts the INTERNAL-only definition, and none compares the printed
`skill=/corpus=/lane=` triple to the file's pinned line (the claim's P1 does state that
equality). Routed gap: a control that asserts the file's pinned line equals the INTERNAL-only
triple (or that the `CENSUS-CHECK pass` printed triple equals the file's `pinned rate` line).

## 6. Ancillary findings (not mutant results; for routing)

**(a) The frozen harness pin is unreproducible.** The C1 claim's `harness_sha256` is
`d39a1fc8cc5ad189b5077dc03c1c3373bca59d77a120493163ccca63eb4f05e0`
(`.ufo/waves/round-98/claims.json`). The harness at the freeze is
`0488d79626e54731a8d5be3985fd1edad68b2b612a74d86454d5bca8a3950e7a`; at the C1 landing and in
the worktree it is `d97132684455aa6cca5bd65dd0e07a94942b8469801d05f219ba3a52b47ecc1a`;
`d39a1fc8` is not an object in the repository (`git cat-file --batch-all-objects` count 0).
The erratum discloses the harness change (the fixture now checks out `--base`) but the pin was
not updated, so the claim's harness identity cannot be reproduced from the claim metadata
(`receipts/04-frozen-metadata.txt`).

**(b) The seat brief's corpus/lane numbers are the base's, not the census's.** The brief says
the census records `corpus 2550/7556, lane 2588/7958` at `measured-at: e2caf4a1…`. The
committed census at that revision records `corpus 2551/7559, lane 2589/7961`
(`corpus/instruments/citation-survival.md:6`), and the instrument's own re-measurement of
`e2caf4a1` prints `corpus=2551/7559 lane=2589/7961` (`receipts/02-fakehome-pinned-validation.txt`).
The brief's numbers are exactly the base `2133f5bd` measurement (fixture headers in
`receipts/07-matrix-evidence.txt`: `corpus 2550/7556`, `lane 2588/7958`; also the cached
rates in `receipts/m07-cache-by-lane.txt`). The pinned SKILL `162/732` and `host-owned 78`
match both. This is a documentation inconsistency in the brief, not an instrument failure.

**(c) Host-memory hazard.** The base corpus's `` `~/Projects/**` `` citation makes
`resolve.py` recursively glob the whole host tree; on this host that is a 2.2–3.5 GB RSS /
multi-minute expansion that `earlyoom` kills (`receipts/05-earlyoom-evidence.txt`). The
pinned (INTERNAL) measurement is cheap and stable, but any run of the census instrument with
the real `HOME` is currently non-reproducible on this host. This is a reproducibility risk for
the C1 command itself, not a mutant result.

## 7. Restoration and bounds

- No lane file was edited. Instrument sha256 before/after:
  `66383371…` (`sha256sum corpus/instruments/census-at-rev.py`). Harness sha256 before/after:
  `d9713268…` (worktree file untouched). `git status --porcelain` in the lane before and after
  the seat is identical (the pre-existing `M`/`??` entries from other seats; my only writes are
  this report and `MutC1Counter-receipts/` under the untracked `w1/`).
- Every clone, fixture, extract and probe lived under
  `/fast/scratch/hyaku/kasegi-r98/MutC1Counter`; the scratch dir was removed after the
  receipts were copied here. No fixture repo was outside `$S`; every fixture git call named
  `-C <fixture>` and the harness's own `commit()` asserts the fixture is its own top level.
- No tools were installed or upgraded; no host sysctl was touched.

## VERDICT

VERDICT: M01 `no-measured-at-format` — SURVIVED; escaped limb = `measured-at` 40-hex format pin (probe P2: pristine rc=1 `no-measured-at`, mutant rc=0 `pass rev=cand`).
VERDICT: M02 `write-accepts-any-rev` — SURVIVED; escaped limb = `--write` revision validation (probe P3: pristine rc=2 `bad-revision`, mutant rc=0 `CENSUS-WRITE ok rev=cand`).
VERDICT: M03 `no-pinned-compare` — KILLED by tampered-pinned and stale-rev (both rc=0 where rc=1 `pinned-mismatch` is required).
VERDICT: M04 `compare-only-skill` — KILLED by stale-rev (SKILL 162/732 is revision-stable; the stale mismatch is corpus 2527/7497 and lane 2565/7899, which the mutant ignores).
VERDICT: M05 `no-host-owned-line` — SURVIVED; escaped limb = emission of the `host-owned inputs` header line (no control reads it; harness 8/8 pass).
VERDICT: M06 `accept-missing-pinned` — KILLED by no-pinned-line (mutant rc=0 where rc=1 `no-pinned-line` is required).
VERDICT: M07 `cache-by-lane` — KILLED by stale-rev, bad-revision and no-resolve (one lane-keyed cache entry serves every revision).
VERDICT: M08 `body-from-lane-tree` — SURVIVED; escaped limb = body provenance (mutant body is the 224-file/5152-citation base census under a fresh 333-file/7958-citation header; harness 8/8 pass).
VERDICT: M09 `ignore-resolve-rc` — SURVIVED; escaped limb = resolve.py's non-zero exit (probe P4: pristine rc=2 `resolve-rc1`, mutant rc=0 with rates).
VERDICT: M10 `accept-12-char-rev` — SURVIVED; escaped limb = `measured-at` length validation (probe P1: pristine rc=1 `no-measured-at`, mutant rc=0 `pass rev=fac43d87ee97`).
VERDICT: M11 `pinned-uses-host-inclusive` — SURVIVED; escaped limb = pinned-line INTERNAL-only semantics (mutant writes host-inclusive 168/732 as the pinned line; harness 8/8 pass).
VERDICT: M12 `check-trusts-cli-rev` — KILLED by stale-rev (the check measures the harness's `--rev` instead of the file's `measured-at`).
VERDICT: C1 control set — 5/12 mutants killed, 7/12 survived; the 8 controls cover pinned comparison, missing-pinned handling, per-revision cache keying and file-named-revision authority, but not measured-at format/length, `--write` revision validation, host-owned-line emission, body provenance, resolve-failure, or pinned-line semantics.
VERDICT: Detector baseline — VALID under the controlled HOME (pristine 8/8 pass, 25 s); the real-HOME baseline is INCONCLUSIVE (three earlyoom SIGTERM kills, not detector failures).
VERDICT: Frozen harness pin — NOT REPRODUCIBLE: `d39a1fc8…` matches no committed harness (freeze `0488d796…`, landing `d9713268…`) and is not an object in the repo.
VERDICT: Seat-brief numbers — the brief's `corpus 2550/7556, lane 2588/7958` are the base `2133f5bd` measurement; the committed census at `e2caf4a1` records `corpus 2551/7559, lane 2589/7961` (pinned SKILL 162/732 and host-owned 78 match).
