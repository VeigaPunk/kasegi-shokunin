# CriticClaimsC1 — C1 (`depth:verifiability`) attack report

Seat: `CriticClaimsC1` (leaf critic; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Target: C1 landing `e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`; frozen claims
`12bb2f98cf9d07bcbc8b62985516cc3ff65d9ae8`; base `2133f5bd993aaf34efad795d5e0b588485401fb2`;
C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`.
Scratch: `/fast/scratch/hyaku/kasegi-r98/CriticClaimsC1` (removed before yield; receipts copied first).
Clone: `git clone --shared` of the lane at the C1 landing, `git rev-parse HEAD` =
`e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`.
Receipts: `CriticClaimsC1-receipts/` (each file names the command/output it records).

## 0. Host condition (affects every heavy run below)

The wave's 13 seats each run `resolve.py` over the same 334-file tree; each process peaks at
1.8-3.5 GiB RSS. The host (30 GiB RAM, 30 GiB swap) was saturated (swap 28.9/30 GiB used), and
`earlyoom` (`/usr/bin/earlyoom -r 3600 --prefer (^|/)(java|node|chromium|python3?)$`) sent
SIGTERM to the largest `python3` processes. In a 30-minute window it logged **147** SIGTERM
sends. All five of my `resolve.py` children were killed (exact journal lines in
`09-earlyoom.txt`), including the three P1 attempts and the P2 fixture run.

Consequence: my own independent re-measurement of `e2caf4a1` **never completed**. The
instrument's failure string is `"resolve-rc%d" % returncode`; `"%d" % -15` is `-15`, so
`resolve-rc-15` is **SIGTERM**, not a resolve.py error (verified: `repr('resolve-rc%d' % -15)`
= `'resolve-rc-15'`, receipt `06-p1-runs.txt`).

## 1. P1 — DOES-NOT-STAND

### 1.1 The exact frozen command, three attempts

```
$ cd <clone-at-e2d3de7>
$ python3 -B corpus/instruments/census-at-rev.py --lane . \
    --check corpus/instruments/citation-survival.md --work <scratch>/w
CENSUS-CHECK fail reason=resolve-rc-15 rc=2
rc=2
real 3m19.410s
```
(service run, fresh `--work w3`):
```
CENSUS-CHECK fail reason=resolve-rc-15 rc=2
P1-RC=2
```
(retry, `nice -n 19`, `--work w`):
```
CENSUS-CHECK fail reason=resolve-rc-15 rc=2
P1-RETRY-RC=2
```
None printed the required `CENSUS-CHECK pass rev=e2caf4a1...` line. Exact journal attribution
(`09-earlyoom.txt`):
```
18:13:22 sending SIGTERM to process 1724225 ... VmRSS 1982 MiB ... /CriticClaimsC1/w/tree-e2caf4a1561b/.../resolve.py
18:14:54 sending SIGTERM to process 3244642 ... VmRSS 1795 MiB ... /CriticClaimsC1/wbase/tree-2133f5bd993a/.../resolve.py
18:17:40 sending SIGTERM to process 321032  ... VmRSS 2230 MiB ... /CriticClaimsC1/p2work/instwork/tree-540fcd729a27/.../resolve.py
18:19:30 sending SIGTERM to process 535697  ... VmRSS 2763 MiB ... /CriticClaimsC1/w3/tree-e2caf4a1561b/.../resolve.py
18:26:27 sending SIGTERM to process 3315741 ... VmRSS 3473 MiB ... /CriticClaimsC1/w/tree-e2caf4a1561b/.../resolve.py
```
This is environmental (host memory pressure), not a resolve.py logic error: the instrument
never printed a `pinned-mismatch` or a pass. But P1 as frozen requires the pass line with rc 0;
at the landing, in this wave, it does not reproduce.

### 1.2 The substantive defect: the pinned rate is not revision-stable

The claim calls the pinned line `(INTERNAL only; revision-stable)` and the docstring says "the
measurement is deterministic for a revision". It is not. `resolve.py` classifies a relative
citation with a `../` walk-out against the **extract's parent directory**, i.e. the verifier's
scratch, not the revision. Two citations in the measured scope do exactly this:

- `corpus/knowledge/source-tree-loss-2026-09-28.md:315` cites `` `../MISSION.md:49-56` ``
- `corpus/lessons/round-20-recensus.md:4` cites
  `` `../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kasegi*.md` ``

In the live lane, `../MISSION.md` resolves to `/home/vgpnk/Projects/shokunin/MISSION.md`
(INTERNAL). In the extract at `<work>/tree-e2caf4a1561b`, it resolves to `<work>/MISSION.md`,
which exists only if the verifier's work dir happens to contain it.

**Self-contained proof (my own fixture, no peer data), receipt `04-layout-instability.txt`:**
same rev `6486f8f5e45fdb476c86a0304a3cf7c4baa948f4`, two work dirs:

```
layout A (parent has only the tree):
pinned rate (INTERNAL only; revision-stable): SKILL 0/3 = 0.00% | corpus 0/0 = n/a | lane 0/3 = 0.00%
layout B (parent also has MISSION.md):
pinned rate (INTERNAL only; revision-stable): SKILL 1/3 = 33.33% | corpus 0/0 = n/a | lane 1/3 = 33.33%
isoA census checked with isoB cache:
CENSUS-CHECK fail reason=pinned-mismatch rc=1
  file: ... SKILL 0/3 ... lane 0/3 ...
  rev : ... SKILL 1/3 ... lane 1/3 ...
isoB census checked with isoA cache:
CENSUS-CHECK fail reason=pinned-mismatch rc=1
```

**Real landed census, same file, same revision, two caches (receipt `05-real-file-layout.txt`):**

```
vs author cache (l1/census-land, clean layout):
CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78
rc=0

vs a layout cache whose parent contains MISSION.md and .ufo/.../KasegiGateRepair.md
(peer ReviewC1Census/workD, 2553):
CENSUS-CHECK fail reason=pinned-mismatch rc=1
  file: pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2551/7559 = 33.75% | lane 2589/7961 = 32.52%
  rev : pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2553/7559 = 33.77% | lane 2591/7961 = 32.55%
rc=1
```

The same rev `e2caf4a1` was independently cached as **2551/7559** (author `l1/census-land`,
peer `workS`, `workF`) and **2553/7559** (peer `workD`, `workE`) — receipt `11-cache-rates.txt`.
The peer TSV diff (captured before that seat cleaned its scratch, receipt `12-tsv-flip.txt`)
shows exactly the two citations flipping:

```
workS: ../.ufo/.../members/Kasegi*.md  GONE ; ../MISSION.md:49-56  GONE ; INTERNAL 2589
workD: ../.ufo/.../members/Kasegi*.md  INTERNAL -> workD/.../KasegiGateRepair.md ; ../MISSION.md:49-56 INTERNAL -> workD/MISSION.md ; INTERNAL 2591
```

`workD/MISSION.md` and `workD/.ufo/.../KasegiGateRepair.md` are 0-byte files the verifier's
work dir contained. The peer reviewer `ReviewC1Census` reached the same F1 finding independently
(`ReviewC1Census.md:83-115`, verdict at line 268: "'Revision-stable' pinned rate — NOT VERIFIED /
OVERSTATED (scratch-parent dependence via `../`; 2589 -> 2591 and `--check` fails under a
contaminated work dir)").

Therefore P1's pass is a function of the verifier's scratch layout, not of the revision. A
correct census can fail `pinned-mismatch`; a contaminated scratch can make the landed census
fail. The claim's central label is false.

### 1.3 Goal numbers vs landed artifact

The assignment states "corpus 2550/7556, lane 2588/7958". The landed file says
`corpus 2551/7559 | lane 2589/7961`. The `12bb2f9` (freeze) cache says `2550/7556, 2588/7958`
(receipt `11-cache-rates.txt`). The C2 landing adds the new knowledge entry, which adds exactly
1 INTERNAL and 3 distinct citations. So the assignment's numbers are the **freeze/base**
measurement, not the C2 landing; the landed file's numbers match the C2 landing in a clean
scratch (author `l1` + peer `workS`). The goal text is stale; the file is consistent with
`e2caf4a1` only in a clean layout. This does not rescue P1, because the layout dependence is
real and the goal's own numbers do not match the artifact.

## 2. P2 — DOES-NOT-STAND

Exact command and output (receipt `07-p2-run.txt`):

```
$ python3 -B .ufo/waves/round-98/controls/c1-controls-r98.py --lane . \
    --work <scratch>/p2work --instrument corpus/instruments/census-at-rev.py \
    --base 2133f5bd993aaf34efad795d5e0b588485401fb2
C1-CONTROLS-RESULT error reason=write rc=2
CENSUS-WRITE error reason=resolve-rc-15 rc=2
rc=2
```

The harness's first `--write` runs `resolve.py` in the fixture; earlyoom killed it (pid 321032,
18:17:40, receipt `09-earlyoom.txt`). The eight controls never ran, so the required
`C1-CONTROLS-RESULT pass controls=8 rc=0` and `ATTRIBUTION pass fixtures=8` were not observed
in my post-landing re-run. The author's postfix receipt shows a pass, but P2 is a post-landing
re-run predicate and it did not reproduce here.

Secondary provenance defect: the frozen `harness_sha256` does not identify the harness that
produced the postfix receipt (receipt `10-pins.txt`):

```
claims harness_sha256:       d39a1fc8cc5ad189b5077dc03c1c3373bca59d77a120493163ccca63eb4f05e0
landing harness sha256:      d97132684455aa6cca5bd65dd0e07a94942b8469801d05f219ba3a52b47ecc1a
freeze harness blob sha256:  0488d79626e54731a8d5be3985fd1edad68b2b612a74d86454d5bca8a3950e7a
instrument present at freeze 12bb2f9? NO
```

The erratum discloses the harness fix (base checkout) but the pin was not updated; the freeze
commit's claims also pin an instrument (`435128a2...`) that is not in the freeze tree (the
instrument was added at the landing). The pre-freeze pin is unverifiable from history.

## 3. P3 — STANDS

Receipt `08-p3.txt`:

```
git merge-base --is-ancestor e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 HEAD   -> rc=0
grep -c '/fast/scratch' corpus/instruments/citation-survival.md              -> 0 (rc=1)
grep -c 'tree-e2caf4a1561b' corpus/instruments/citation-survival.md          -> 0 (rc=1)
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (measured from the git-archive extract of `e2caf4a1561b...`)
```

The frozen P3 command passes as written. The erratum's premise ("the frozen command was
mis-specified because the corpus cites /fast/scratch paths") does not hold for the census file:
the frozen grep reads only the census file, and it prints 0. The first generated census's
extract paths (1,243 occurrences) are exactly what the frozen grep would have caught, so the
erratum narrows the check without need. It does not change the landing outcome.

## 4. Attacks (a)-(d): what the check prints, and whether P1/P3 still holds

All attacks use a small fixture repo (3 files + the lane's own `resolve.py`) under my scratch,
so the measurement is instant and independent of the host load. The instrument is the landing
instrument, run from the landing clone.

### (a) Pinned line matches, body hand-edited — attack succeeds

Receipt `01-abc-body-repoint.txt`:
```
body "distinct path-like citations: **4**" -> "**9999**", header untouched
CENSUS-CHECK pass rev=e8aa4811ae891304dfa0be8befcec045618dee8a skill=2/3 corpus=2/2 lane=3/4 host_owned=0
rc=0
```
`check()` only regexes `measured-at` and the `pinned rate` line and re-measures; it never reads
the body. P1 (as frozen) still holds — the printed triple equals the file's pinned line — while
the census body is wrong. The statement's clause "The body below the header is resolve.py's own
generated output for that revision" is not verified by P1.

### (a2) Host-inclusive and host-owned lines tampered — attack succeeds

Receipt `01-abc-body-repoint.txt`:
```
host-inclusive: SKILL 99/99 ... | corpus 99/99 ... | lane 99/99 ...
host-owned inputs: 4242 ...
CENSUS-CHECK pass rev=e8aa4811... skill=2/3 corpus=2/2 lane=3/4 host_owned=0
rc=0
```
The check never verifies the host-inclusive line or the host-owned count, although the claim's
statement rests on both.

### (b) `measured-at` names a revision the file was not generated from — attack succeeds

Receipt `01-abc-body-repoint.txt`:
```
real landed census body (still names e2caf4a1 and carries 7961-scale numbers),
header re-pointed to e8aa4811 with that rev's pinned line:
CENSUS-CHECK pass rev=e8aa4811ae891304dfa0be8befcec045618dee8a skill=2/3 corpus=2/2 lane=3/4 host_owned=0
rc=0
```
P1 holds for the *named* rev; the body is from a different tree. The check cannot tell.

### (c) `measured-at` is not an ancestor of the branch tip — attack succeeds against P1-only verification

Receipt `02-cd-nonancestor-removed.txt`:
```
side=37188550809e49e302bd6a9c961689f1ad5a64d9
git merge-base --is-ancestor 3718855... main -> rc=1
CENSUS-CHECK pass rev=37188550809e49e302bd6a9c961689f1ad5a64d9 skill=3/4 corpus=2/2 lane=4/5 host_owned=0
check rc=0
```
`check()` contains no ancestry test (`grep 'ancestor|merge-base|rev-list'` over lines 203-232:
no match). P3 (run separately) would fail if the census named such a rev, but the claim's own
`command` is P1 only; a verifier who runs only it accepts a non-ancestor revision.

### (d) Census generated from a tree with one knowledge file removed — passes where the rev exists

Receipt `02-cd-nonancestor-removed.txt`:
```
fixture tree at b79304d... has corpus/README.md removed
CENSUS-CHECK pass rev=b79304d14b9872a74aa5978d40d771aadb94ef9e skill=1/3 corpus=0/0 lane=1/3 host_owned=0
check-in-fixture rc=0
same census checked in the lane clone (rev absent):
CENSUS-CHECK fail reason=bad-revision rc=2
check-in-lane rc=2
```
The check's guarantee is repo-local: it verifies "some revision in this repo", not "the revision
the lane's tip implies". A census generated from an ancestor whose file set is missing a
knowledge file (e.g. the base) is accepted if the rev exists in the repo.

### Cache trust — attack succeeds

Receipt `03-cache-trust.txt`:
```
fabricated work/cache/e8aa4811....json with rates 1/3, 1/2, 1/4
CENSUS-CHECK pass rev=e8aa4811... skill=1/3 corpus=1/2 lane=1/4 host_owned=0
check rc=0
real measurement in a fresh work dir:
CENSUS rev=e8aa4811... skill=2/3 corpus=2/2 lane=3/4 host_owned=0
```
`measure()` returns `work/cache/<rev>.json` if it exists, without verifying it was produced by
this instrument or this extract. A stale or fabricated cache makes `--check` pass with rates
that contradict the real measurement. (A peer's `workP` cache with `skill=[999,732]`,
`corpus=[9999,9999]` shows the same attack was already exercised in this wave.) The cache is
also keyed only by rev, not by the instrument sha256 or the extract's parent layout.

### Extract reuse (code reading, not exercised)

`extract()` returns early if `<work>/tree-<rev12>/corpus/instruments/resolve.py` exists, so a
partial or tampered extract in the verifier's scratch is reused without an integrity check.
Same threat model as the cache: the verifier's scratch is trusted.

## 5. Impacted axes

- **depth:verifiability (C1's axis)** — the revision pin is real (`measured-at`, ancestry, no
  scratch path), but the pinned rate is **not revision-stable** and the body/host lines are
  unverified. The census of record can be wrong in its body while P1 passes, and a correct
  census can fail P1 depending on the verifier's scratch layout. The claim's word
  "revision-stable" is false; this is the axis the claim was supposed to move.
- **coverage** — no interaction found; C1 does not touch the scanner. The C2 axis is unaffected.

## 6. Smallest safe correction

1. **Isolate the extract's parent.** Create `<work>/iso/<rev>/tree` with the parent created
   fresh and asserted to contain only `tree` (or run `resolve.py` with a root whose `..` is a
   fresh empty dir), so `../` citations deterministically resolve to nothing. Re-generate and
   re-pin; the clean layout yields the landed 2551/7559, so the numbers should not move, but
   verify.
2. **Bind the body.** After `measure`, compare the file's body to the generated body (or store
   and verify a body sha256), and verify the host-inclusive and host-owned lines. Otherwise the
   statement's body clause is unverified.
3. **Add an ancestry check** to `--check` (`git merge-base --is-ancestor <rev> HEAD`), failing
   `not-ancestor`.
4. **Key the cache** by `(rev, instrument sha256, resolve.py blob)` or refuse a cache the
   instrument did not write in this run.
5. **Fix the pins:** `harness_sha256` must match the executed harness (landing
   `d9713268...`); the freeze claims pin an instrument (`435128a2...`) absent from the freeze
   tree.
6. **Correct the erratum's P3 premise:** the frozen command passes as written; the first
   census's extract paths were the real failure, which the frozen command correctly caught.

## 7. Verdicts

VERDICT: P1 — DOES-NOT-STAND. The exact frozen command printed `CENSUS-CHECK fail reason=resolve-rc-15 rc=2` on three attempts (earlyoom SIGTERM, journal-attributed); and the pinned triple is not revision-stable: the same rev `e2caf4a1` measures 2551/7559 in a clean scratch and 2553/7559 in a scratch whose parent contains `MISSION.md`/`.ufo`, and the landed census passes against one cache and fails `pinned-mismatch` against the other.
VERDICT: P2 — DOES-NOT-STAND. My post-landing re-run printed `C1-CONTROLS-RESULT error reason=write rc=2` / `CENSUS-WRITE error reason=resolve-rc-15 rc=2`; the eight controls did not run. The frozen `harness_sha256` also matches neither the freeze nor the landing harness.
VERDICT: P3 — STANDS. Ancestry rc=0; `grep -c '/fast/scratch'` = 0; `grep -c 'tree-e2caf4a1561b'` = 0; the `Lane root:` line names the lane. The erratum's "mis-specified" premise is not supported.
VERDICT: attack (a) body hand-edit — SUCCEEDS; `CENSUS-CHECK pass ... rc=0` while the body is wrong. P1's header condition holds; the statement's body clause is unverified.
VERDICT: attack (a2) host-line tamper — SUCCEEDS; `CENSUS-CHECK pass ... rc=0` with fabricated host-inclusive/host-owned lines.
VERDICT: attack (b) `measured-at` re-point — SUCCEEDS; `CENSUS-CHECK pass rev=e8aa4811... rc=0` with the real landed body from a different rev. P1 holds for the named rev only.
VERDICT: attack (c) non-ancestor — SUCCEEDS against P1-only verification; `CENSUS-CHECK pass ... rc=0`, ancestry rc=1, no ancestry test in the instrument. P3 would fail if the census named it.
VERDICT: attack (d) removed knowledge file — SUCCEEDS only where the rev exists; `CENSUS-CHECK pass ... rc=0` in the fixture, `CENSUS-CHECK fail reason=bad-revision rc=2` in the lane.
VERDICT: cache-trust attack — SUCCEEDS; a fabricated `work/cache/<rev>.json` yields `CENSUS-CHECK pass ... skill=1/3 corpus=1/2 lane=1/4` against a real measurement of `2/3, 2/2, 3/4`.
