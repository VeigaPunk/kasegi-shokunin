# ExecC1ExportMode — export-mode discipline proof (round 36, C1 depth:verifiability)

Seat: `ExecC1ExportMode` (executor, leaf, hyaku run 9). Assignment: prove the export-mode
discipline of the round-36 C1 closure suite: (1) `--export-ref` extracts with `git archive` and
no check reads the live worktree; (2) a run without `--export-ref` exits 2; (3) the suite creates
or modifies nothing under the lane. Record commands + outputs.

**Verdict: PASS at the final frozen suite digest**
`sha256 4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`
(894 lines, 39022 bytes), the digest ExecC1SuiteBuild declared final (IRC: "FINAL DIGEST MOVED ONCE
MORE: 4db1ae70…") for the text it lands as `corpus/instruments/r36-closure.sh` and verbatim in
`.ufo/waves/round-36/wave1/ExecC1SuiteBuild.md`. All three properties hold on that digest, measured
against a synthetic all-green lane repo and against the real lane.

One real defect was found and fixed during the wave: plain `git status` in E9 created and unlinked
`.git/index.lock` **inside the lane** — the only write under the lane the suite ever performed. The
frozen digest carries `git --no-optional-locks -C "$srepo" status --porcelain`; a traced run at
`4db1ae70` shows **0 write syscalls under the lane and 0 `index.lock` lines**.

Digest trail for this seat (each full matrix was re-run at the digest it names):
`ff616adc` → `a6c1c922` → `53d9e324` → `dc5208fa` → `76273416` → **`4db1ae70` (final, proved)**.
The E1/E2/E4/E5/header deltas between `76273416` and `4db1ae70` are all covered below by re-running
the matrix, not by inference.

## 0. What was run, and on which bytes

* Suite under test (final): `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh`,
  sha256 `4db1ae70…`, 894 lines, 39022 bytes. I pinned a byte copy at
  `/fast/scratch/hyaku/kasegi-r36/ExecC1ExportMode/pinned/r36-closure-4db1ae70.sh` (sha256
  re-verified) and ran only that copy, so the digest cannot drift under a run.
* Synthetic all-green lane repo `G2` (my scratch): `cp -a` of the lane checkout at
  `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (full git history, so E1's commit bindings resolve),
  plus the round-36 closure bytes, committed as one synthetic head
  **`747820183c1a91f33539094f2de23dfebd17fd4c`**:

  ```
  b47f2cd  round-36: claims freeze + before controls (lane head, unmodified)
  7478201  synthetic H : E3 registry rows under "## Round-36 Gates & probes registry addition",
                         corpus/lessons/round-36.md with M36 rows + 'source-recheck',
                         non-empty .ufo/waves/round-35/wave1-results.json.provenance.md,
                         SCORECARD "## Round 36 — …" section with one
                         "**Final lane commit: `b47f2cdf…`**" line (an ancestor)
  ```

  `git -C G2 status --porcelain` → empty. E9 was pointed at an empty scratch root (`G2-empty`)
  because the live `/fast/scratch/hyaku/kasegi-r36` root held running seats' dirs.
* Commands (all read-only on the lane; nothing committed or written in the lane repo):

  ```
  bash r36-closure.sh --lane <G2> --export-ref 7478201… --scratch-root <empty> --work <outside lane>
  bash r36-closure.sh --selftest --lane <G2> --scratch-root <empty> --work <outside lane>
  bash r36-closure.sh --lane <G2> --export-ref 3266c993… --scratch-root <empty> --work …
  bash r36-closure.sh --lane <G2> --export-ref 0aee0ef1… --scratch-root <empty> --work …
  bash r36-closure.sh                                  # no arguments
  bash r36-closure.sh --root <G2>                      # round-35 interface vestige
  strace -f -s 256 -e trace=%file,execve -o <trace> bash r36-closure.sh …
  ```

  Tools: strace 7.2, git 2.56.0, GNU bash 5.3.20, GNU tar 1.35. No tool installed or upgraded;
  no pacman transaction attempted.

## 1. `--export-ref` runs `git archive`, and content checks read the export only

### 1a. Run header (new at this digest)

```
export-ref=747820183c1a91f33539094f2de23dfebd17fd4c mode=export lane=/fast/scratch/…/G2 suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
deviation=non-default --lane
deviation=non-default --scratch-root
```

The `suite-sha256=` field is the sha256 of the executing file (equal to the pinned digest above),
so a run self-identifies the bytes that produced it; `deviation=` is explicitly non-gating and only
names overridden roots.

### 1b. Extraction identity

Traced execve of the archive pipeline:

```
"git", "-C", ".../G2", "archive", "--format=tar", "747820183c1a91f33539094f2de23dfebd17fd4c"
"tar", "-xf", "-", "-C", ".../tr-G2-w/export"
```

Reproducing that exact pipeline into a private dir and comparing with the ref:

```
git -C G2 ls-tree -r --name-only 7478201 | wc -l   -> 7215 entries
find <repro> -type f|-type l | wc -l               -> 7215 entries, set equal = True
find <repro> -name .git                            -> 0 (the export holds no .git)
sha256(SCORECARD.md)               == sha256(git show 7478201:SCORECARD.md)   -> True
sha256(SKILL.md)                   == sha256(git show 7478201:SKILL.md)       -> True
sha256(corpus/lessons/round-36.md) == sha256(git show 7478201:…)              -> True
```

### 1c. No check reads live worktree *content*

strace of the plain green run (`--lane G2`, export at `7478201`) — 12 `git` execve calls:

```
subcommands: rev-parse (--git-dir ×2, --verify --quiet ×2, --show-toplevel)
             archive ×1, cat-file -e ×1, merge-base --is-ancestor ×1,
             ls-tree ×2, ls-files ×1, status --porcelain ×1
             (invoked as: git --no-optional-locks -C <lane> status --porcelain)
mutating subcommands (init/add/commit/reset/fetch/push/checkout/switch/stash/update-index): none
```

(12, not 18, because E1 is now scoped to the last Round-36 block and binds one hash, not four.)

Every non-write path touched under the worktree was only the repo root and the scratch root:

```
non-write worktree paths touched: ['.../G2', '.../G2-empty']
```

i.e. `-C` resolution and E9's scratch `find`; no content file under the worktree was opened by any
check. The absolute-lane strings in this trace are all `symlinkat` *targets* created by tar while
materializing committed symlinks inside the export — no read follows them (Risk 1).

### 1d. Mutation matrix — the exported bytes decide, the worktree does not

Four runs at `4db1ae70`. `green` = `--lane G2 --export-ref 7478201` → `closed=9/9 exit=0`.
`Gm` is a copy of `G2` with one line `**Round-36 closing note: filled by the L1 …**` appended to
SCORECARD.md and **committed** (`a28f9ee5510fe1420ea115ebc2ccd4585e36bab0`); `G2d` is a copy with
SKILL.md's `r36-closure.sh` renamed to `r36-closure-BROKEN.sh` and left **uncommitted**.

| run | --lane | --export-ref | result | check-line diff against green |
|---|---|---|---|---|
| green | G2 (HEAD 7478201) | 7478201 | `closed=9/9 exit=0` | — |
| B | Gm (HEAD a28f9ee) | 7478201 | `closed=8/9 exit=1` | only `E9 … head-match=0` |
| C | Gm (HEAD a28f9ee) | a28f9ee | `closed=8/9 exit=1` | only `E1 … placeholders=1` |
| D | G2d (HEAD 7478201, dirty) | 7478201 | `closed=8/9 exit=1` | only `E9 … status-dirty=1` |

Exact check-line deltas (everything else byte-identical; headers differ only in `lane=`, and in C in
`export-ref=`, which is the point of the run):

```
B: -E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
   +E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
C: -E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=1 closed=1
   +E1 payload=placeholders=1,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=1,bound=1 closed=0
D: -E9 payload=status-dirty=0,…,head-match=1,… closed=1
   +E9 payload=status-dirty=1,…,head-match=1,… closed=0
```

Readings: B breaks the *worktree and HEAD* at the archive source while exporting the old ref → the
eight content checks do not move (only E9's deliberate HEAD binding does). C puts the same defect
*inside the exported commit* → E1 opens. D breaks the worktree only → only E9's quiescence limb
opens; E3 stays closed even though the worktree SKILL.md lost the registry row, because E3 reads
the export. That is the discipline proved end-to-end, not just asserted.

### 1e. Historical refs behave as named heads (corroboration for ExecC1BaseFail)

Same suite, same `--lane G2`, export of the round-35 heads (matches ExecC1SuiteBuild's measurements):

```
--export-ref 3266c9937b03062d9bbc2f436e20820115ed179c -> closed=0/9 exit=1
--export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988 -> closed=3/9 exit=1
```

(0/9 matches the frozen C1 kill rule; 3/9 is `<9/9`. At 0aee0ef E2 is open — the corrected
`| depth:density | 9 | mean **201.2**` row and the `Erratum (round 35)` marker postdate that head —
and E8 reads `stale-line=1`, the false evidence line the round-35 spot-check routed.)

## 2. A run without `--export-ref` exits 2

```
$ bash r36-closure.sh
r36-closure: refusing to run against the live worktree: this suite is export-mode only.
r36-closure: pass --export-ref <hash> (see --help) or --selftest.
exit=2                                  (stdout empty)

$ bash r36-closure.sh --root <G2>       # the round-35 suite's interface must not be inherited
r36-closure: unknown argument: --root
exit=2

$ bash r36-closure.sh --export-ref      # missing value
r36-closure: --export-ref needs a commit-ish
exit=2

$ bash r36-closure.sh --export-ref deadbeef…   # unresolvable
r36-closure: export ref does not resolve to a commit: …
exit=2
```

There is no worktree code path to reach: extraction is mandatory, and `--selftest` (the only other
mode) exports `HEAD` through the same `git archive` path.

## 3. Nothing is created or modified under the lane

Measured twice: on the synthetic clean repo and on the real lane.

### 3a. Synthetic clean lane (`G2`, HEAD `7478201`)

Every tracked and untracked byte, mode, size and mtime of the worktree (excluding `.git`) and every
read of `.git` were unchanged; `git status --porcelain` stayed empty; the full strace shows

```
write-ish syscalls touching G2 (worktree or .git): 0
index.lock occurrences in trace: 0
```

### 3b. Real lane (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `b47f2cd`)

Traced run with `--scratch-root` an empty dir so E9's scratch scan measures 0:

```
before/after git status --porcelain (9 lines, uncleaned round-36 artifacts): equal  True
sha256 of the six files the checks read (SCORECARD.md, SKILL.md, corpus/QUALITY.md,
  .ufo/waves/round-34/wave1/L1Integration.md, .ufo/waves/round-35/wave1-results.json,
  .ufo/waves/round-35/claims-erratum-d5.md):                                equal  True
.git/index (size, mtime_ns):                                                equal  True
write-ish syscalls under the lane path:                                          0
index.lock lines in the trace:                                                   0
exit=1 at this pre-closure head: E1 (no Round 36 SCORECARD section yet), E3, E4 (provenance
  absent), E8, E9 open -> closed=4/9 (matches ExecC1SuiteBuild's HEAD reading of 4/9)
```

### 3c. Defect found and fixed in transit (the reason this proof exists)

At the digests before the fix (`ff616adc`, `a6c1c922`, `53d9e324`, `dc5208fa`), E9's
`git -C "$srepo" status --porcelain` took and unlinked `.git/index.lock` **inside the lane** — a
transient write, invisible to `git status` but a strict violation of "nothing under the lane". Trace
on the real lane:

```
openat(AT_FDCWD, ".../kasegi-shokunin/.git/index.lock", O_RDWR|O_CREAT|O_EXCL|O_CLOEXEC) = 3
unlink(".../kasegi-shokunin/.git/index.lock") = 0
```

Fix (in the final digest, verified by me and independently by SuiteBuild):

```
porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)
```

With it, the same traced runs on the real lane and on `G2` show 0 write syscalls and 0
`index.lock`. (My own first draft had the same defect; I patched it the same way.)

## 4. Selftest and negative controls at the final digest

```
$ bash r36-closure.sh --selftest --lane G2 --scratch-root <empty> --work <outside lane>
selftest case=E1 positive=pass mutants=… verdict=pass
…
selftest cases=9 failures=0
selftest judge=own-report accepted=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
exit=0
```

(The run's own selftest is green on the synthetic all-green tree; the same command on the live lane
head is expected to report failures there, because the lane has not landed the round-36 bytes yet —
that is the point of the gate, not a suite defect.)

## 5. Independent fallback draft (not to be landed)

Before SuiteBuild's draft existed I built a self-contained draft at
`/fast/scratch/hyaku/kasegi-r36/ExecC1ExportMode/draft-r36-closure.sh`
(422 lines, sha256 `44773ccd…` as recorded at first build) and proved the same three properties on
it independently: green `closed=9/9 exit=0`, committed-mutation/export-old-ref → only E9
`ref-is-head=0`, export-at-mutation → only E1 open, dirty worktree → only E9 `worktree-dirty=1`,
no-arg `exit=2`, and 0 write syscalls under the repo under test after the same
`--no-optional-locks` patch. It is corroboration only; the final SuiteBuild draft is the one to
land. Its per-check semantics are narrower than the final draft's (no E3 section scoping, no
row-shaped E7, no round35-lesson limb, no Round-36 E1 scoping).

## 6. Risks / residual limits (measured, not hidden)

1. **The export carries 58 committed symlinks whose targets are absolute live-lane paths**
   (e.g. `.ufo/waves/round-25/assimilation/rows/validate/corpus/knowledge` →
   `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge`). `git archive` preserves them,
   so the export is not hermetic if a check ever recurses (`grep -r`, `find -L`, `cp -rL`). The
   suite reads explicit paths only and the trace shows zero opens under the live lane with read
   flags. If a future check recurses, strip symlinks at extraction or keep path lists explicit.
2. **E9 is the one live limb by design** (worktree cleanliness, `rev-parse HEAD`, scratch scan), and
   E4's `tracked-index` limb is a live `git ls-files` (frozen claim: "tracked with provenance
   note"). The mutation matrix shows they move only when the worktree/HEAD moves, never the
   E1–E3/E5–E8 payloads.
3. **E9's `head-match` binds the export ref to the lane's standing HEAD.** A stale export ref fails
   by design (measured as runs B and the historical-ref runs). At filing the export ref must be the
   final lane HEAD.
4. **E1's scoping and hash window.** E1 requires a `Round[- ]36` SCORECARD heading and reads 40-hex
   tokens on `[Ff]inal lane commit` lines inside that block plus the four following lines each. A
   40-hex token (not a sha256, which is 64) inside that window — e.g. a receipt digest quoted in
   prose — becomes a required commit. At `G2` it read 1/1 bound; keep digest-bearing prose out of
   that five-line window.
5. **E8's `stale-line=0` limb is file-wide over `corpus/lessons/round-35.md`.** An append-only
   correction that *quotes* `source-recheck exit 0 on committed bytes` re-opens E8; the correction
   must paraphrase. The current head measures `stale-line=0`, so the L1 must not reintroduce the
   literal while appending (this collides with routed defect 4's "append corrections" remedy — put
   the paraphrase, not the quote, in the round-35 lesson; the round-36 lesson may name the
   defect).
6. **Digest volatility during the wave.** The suite moved six times while the wave ran
   (`ff616adc` → `a6c1c922` → `53d9e324` → `dc5208fa` → `76273416` → `4db1ae70`); each evidence
   layer was re-run at the digest it names, and the final matrix (green, B/C/D, strace, real-lane,
   negatives, selftest) was re-run at `4db1ae70`. If the landed
   `corpus/instruments/r36-closure.sh` has a different sha256 than `4db1ae70…`, the three proofs
   must be re-run with the recipe in §7 before the C1 counting commands are taken.
7. **E9 scratch scan at filing.** At this seat's runs the real `/fast/scratch/hyaku/kasegi-r36`
   root held other seats' dirs, so `--scratch-root` was an empty directory for the green proofs.
   My own seat dir is removed before this receipt is written; the final filing run must see the
   real root empty (E9 limb `scratch-seat-dirs=0`).

## 7. Reproduction recipe (verifier, after the instrument lands)

```bash
S=/fast/scratch/hyaku/kasegi-r36/verify-export-mode; mkdir -p "$S"
cp -a /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/G2"     # full history for E1
# write the round-36 closure bytes into $S/G2: E3 rows under a
#  "## … Gates & probes registry …" heading, corpus/lessons/round-36.md with M36 +
#  'source-recheck', a non-empty round-35 provenance note, and a last SCORECARD
#  "## Round 36 …" section whose single "**Final lane commit: `b47f2cdf…`**" line
#  names an ancestor; then commit.
git -C "$S/G2" add -A && git -C "$S/G2" -c user.name=v -c user.email=v@l commit -qm synthetic
H=$(git -C "$S/G2" rev-parse HEAD); mkdir -p "$S/empty" "$S/work"
bash corpus/instruments/r36-closure.sh --lane "$S/G2" --export-ref "$H" \
     --scratch-root "$S/empty" --work "$S/work"          # closed=9/9 exit=0
strace -f -s 256 -e trace=%file,execve -o "$S/tr" \
     bash corpus/instruments/r36-closure.sh --lane "$S/G2" --export-ref "$H" \
     --scratch-root "$S/empty" --work "$S/work"
grep -c 'index.lock' "$S/tr"                              # 0
bash corpus/instruments/r36-closure.sh                    # exit 2
```

## 8. Compliance

* Writes: this receipt only in the lane; all work under
  `/fast/scratch/hyaku/kasegi-r36/ExecC1ExportMode/` (removed before yield). No lane-repo edit, no
  commit/add/reset/checkout/push/fetch; the only mutating git commands were `init`/`add`/`commit`
  inside the `$S/G2` scratch fixture whose `rev-parse --show-toplevel` was verified equal to `$S/G2`
  before use. Fleet root and `/home/vgpnk/Projects/shokuknow` untouched.
* No subagents, no swarm, no `agent://all`. One IRC coordination thread with ExecC1SuiteBuild
  (draft path, contract, the index.lock defect + verified fix, freeze request, then the final
  digest handoff).
* Tooling: nothing installed or upgraded (strace 7.2, git 2.56.0, tar 1.35, bash 5.3.20 already
  present); no pacman.
* Axes: this seat moves `depth:verifiability` only (export-mode discipline of the C1 instrument);
  no other axis touched, no lane bytes changed.
