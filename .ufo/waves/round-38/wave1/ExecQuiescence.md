# ExecQuiescence — round-38 quiescence preconditions and the G6 rule

Seat: ExecQuiescence (executor, leaf). Round: kasegi-shokunin 38. Item: record the
quiescence preconditions and scratch state, read the round-37 report's quiescence claim and
`corpus/lessons/round-37-verifier-spotcheck.md` §5 D-E, and state the precise G6 rule that is
implementable from those facts — including how the suite must exclude its own `--work` dir and
what happens to the dir of a seat still running. Receipt only; no deliverable file.

Measurement window: 2026-10-26T18:26Z–18:30Z on lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `700153593eb586c70a6499c8ca225ee4d673bc9b`.
All commands below are read-only; nothing was installed or upgraded; scratch
`/fast/scratch/hyaku/kasegi-r38/ExecQuiescence` existed only for this seat and was removed.

## 1. Preconditions as measured

### 1.1 Lane status and position

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain | wc -l
3
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain
?? .ufo/waves/round-38/wave1.ready
?? .ufo/waves/round-38/wave1.ready.partial
?? .ufo/waves/round-38/wave1/
$ git rev-parse HEAD
700153593eb586c70a6499c8ca225ee4d673bc9b
$ git log --oneline -6
7001535 round-38: wave1 spec + validated dispatch (73 seats, v2)
9a10b02 round-38: freeze claims C1 (r38-closure G1-G8) and C2 (F21 CSAF VEX) with before-controls
a173b0c round-37 verifier spot-check (integrator, hyaku): non-author admit/reject
83975ac round-37: WAVE-DONE results — kasegi-r37-build-results.json (64/64 settled)
2387dcf round-37: F3 final head — bind final lane hash in SHONEN/SCORECARD
aa88877 round-37: F2 final head — genuine all-gates transcript of the F1 run
```

Three porcelain lines, all untracked and all inside `.ufo/waves/round-38/`; zero tracked drift
(no ` M`/`A `/`D ` lines) and zero dirty path outside the round dir. The pre-wave 0 is not
re-derivable mid-wave: `wave1/` is where every seat receipt lands, so porcelain is non-zero for
the whole wave (same shape as round-37 ExecQuiescenceProbe, which also measured 6 until filing).

### 1.2 jj-lane state (read-only)

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kasegi-shokunin
state branch=master local=700153593eb586c70a6499c8ca225ee4d673bc9b remote=700153593eb586c70a6499c8ca225ee4d673bc9b ahead=0 behind=0 head=detached tracked=0 untracked=3
```

`local == remote`, `ahead=0 behind=0`; detached HEAD at the wave1-spec commit, `untracked=3`
agreeing with §1.1. The claims-freeze commit `9a10b02` and the declared base `a173b0c` are
ancestors of HEAD (the log above).

### 1.3 Scratch roots

```
$ ls -la /fast/scratch/hyaku | grep kasegi
drwxr-xr-x  18 vgpnk vgpnk  4096 Oct 26 15:27 kasegi-r38
$ ls -ld /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37
ls: cannot access '/fast/scratch/hyaku/kasegi-r36': No such file or directory
ls: cannot access '/fast/scratch/hyaku/kasegi-r37': No such file or directory
$ for r in /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37; do
    if [ -e "$r" ]; then echo "EXISTS $r entries=$(find "$r" -mindepth 1 -maxdepth 1 | wc -l)";
    else echo "ABSENT $r"; fi; done
ABSENT /fast/scratch/hyaku/kasegi-r36
ABSENT /fast/scratch/hyaku/kasegi-r37
```

Samples of the live r38 root (point-in-time; the set moved while sampling):

```
$ find /fast/scratch/hyaku/kasegi-r38 -maxdepth 1            # 18:26Z, 17 paths incl. root (16 entries)
/fast/scratch/hyaku/kasegi-r38
/fast/scratch/hyaku/kasegi-r38/L1
/fast/scratch/hyaku/kasegi-r38/ExecFenceWalk
/fast/scratch/hyaku/kasegi-r38/ExecBaseRed
/fast/scratch/hyaku/kasegi-r38/ExecR37HeadRed
/fast/scratch/hyaku/kasegi-r38/ExecR37Carry
/fast/scratch/hyaku/kasegi-r38/ExecDeclaredBlocks
/fast/scratch/hyaku/kasegi-r38/ExecC2Capture
/fast/scratch/hyaku/kasegi-r38/ExecC2QuoteOnce
/fast/scratch/hyaku/kasegi-r38/ExecC2Census
/fast/scratch/hyaku/kasegi-r38/ExecIdCollision
/fast/scratch/hyaku/kasegi-r38/ExecCsafStatus
/fast/scratch/hyaku/kasegi-r38/ExecSchemaCross
/fast/scratch/hyaku/kasegi-r38/ExecNoHarm
/fast/scratch/hyaku/kasegi-r38/ExecDensity
/fast/scratch/hyaku/kasegi-r38/ExecQuarantine
/fast/scratch/hyaku/kasegi-r38/ExecQuiescence
$ ls -1a /fast/scratch/hyaku/kasegi-r38                  # 18:27Z, 22 direct entries (no . or ..)
ExecBaseRed ExecC2Audit ExecC2Binding ExecC2Capture ExecC2Census ExecC2Harness
ExecC2Junk ExecC2QuoteOnce ExecCsafStatus ExecDeclaredBlocks ExecDensity ExecIdCollision
ExecNoHarm ExecQuarantine ExecQuiescence ExecR37Carry ExecR37HeadRed ExecSchemaCross
ExecSuiteBuild L1 ScribeEntryF21 ScribeRowS055
$ find /fast/scratch/hyaku/kasegi-r38 -mindepth 1 -maxdepth 1 | wc -l
26                                                        # 18:29:21Z, peers live
```

The r38 count moves between samples (22 → 26) because sibling seats create and remove their
dirs; that is the healthy mid-wave signature, and it is also why a "quiescent" reading is only
meaningful at filing.

Pre-state mutation worth recording: `.ufo/waves/round-38/c1-controls/before.txt`
(measured 18:16:23Z, at the freeze) records `G6/D-E: find /fast/scratch/hyaku/kasegi-r36
/fast/scratch/hyaku/kasegi-r37 -mindepth 1 | wc -l -> 1 (/fast/scratch/hyaku/kasegi-r37/build-spec.py)`.
At 18:29Z that file is gone (`find /fast/scratch/hyaku -maxdepth 2 -name build-spec.py` → no
output) and both roots are absent. So the D-E pre-state has been cleaned between freeze and now;
the G6 limb still needs the file-shape fix below, because this green is a cleanup, not
enforcement, and the same class can recur at filing.

### 1.4 Disk

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                               3%   125.2G
/var/tmp                          35%   582.2G
/fast/scratch/hyaku               24%   610.9G
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status >/dev/null 2>&1; echo "status_rc=$?"
status_rc=0
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh check; echo "check_rc=$?"
ok root=/tmp use=3% soft=70%
ok root=/var/tmp use=35% soft=70%
ok root=/fast/scratch/hyaku use=24% soft=70%
check_rc=0
$ df -h /fast/scratch/hyaku /tmp
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  193G  612G  24% /fast
/dev/nvme1n1p1  128G  2.7G  126G   3% /tmp
```

All roots ≥46 points under `SOFT_PCT=70`; `check rc=0`, `status rc=0`. `disk-guard.sh status`
also lists the usual idle `/tmp` and `/var/tmp` leftovers from other lanes; none is under
`kasegi-r3x`, so G6's roots are unaffected by them.

## 2. The round-37 claim and the defect it hid

Round-37 report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:41`, the report
the round-37 verifier graded) claims:

> `after: all six routed defects closed (E10–E14 green), quiescent at filing (worktree clean, scratch empty).`

The committed receipt agrees with itself
(`.ufo/waves/round-37/final-gates/all-gates.txt:16`):

```
E9 payload=status-read=ok,status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
```

Round-37 verifier §5 D-E (`corpus/lessons/round-37-verifier-spotcheck.md:181-182`):

> **D-E — scratch not empty.** `/fast/scratch/hyaku/kasegi-r37/build-spec.py` remains (no seat dirs, so E9 is unaffected); the report says "scratch empty" (§7 delete-on-exit).

Both statements are true at once because of one word in the r37 limb
(`corpus/instruments/r37-closure.sh`, `check_e9`):

```bash
while IFS= read -r d; do
  ...
done < <(find "$sroot" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
```

`-type d` enumerates directories only. `build-spec.py` is a regular file, so
`scratch-seat-dirs=0` was an accurate count of dirs and a false statement about entries. The
miss is structural, not a bad reading: the frozen r37 E9 wording spoke of "scratch seat dirs",
so the file was outside its letter, and the r37 report inherited the false "scratch empty".
Two secondary fail-open shapes in the same limb, already measured by round-37
ExecQuiescenceProbe §5b–5c and still present in the r37 bytes, are relevant to the r38 fix:

1. `find … 2>/dev/null` swallows a read error, so an unreadable root is indistinguishable from
   an empty one, and an absent root is only "visible" via `scratch-root=absent`, never asserted
   (`[ "$left" -eq 0 ]` is the sole predicate).
2. The work-dir exclusion is correct in shape — `dp=$( cd "$d" && pwd -P )` compared to
   `skip=$( cd "$WORK" && pwd -P )` — but it only ever sees `-type d` children, so a *file*
   named like the work dir (or a symlink) can never be excluded *or* counted; a symlink is
   silently skipped by `-type d`, i.e. it reads as absent rather than as an entry.

## 3. The precise G6 rule, implementable from these facts

Frozen G6 (`claims.json` C1): "live scratch quiescence: `/fast/scratch/hyaku/kasegi-r36` and
`/fast/scratch/hyaku/kasegi-r37` hold zero entries (or are absent) and
`/fast/scratch/hyaku/kasegi-r38` holds nothing except the suite's own `--work` dir". The rule
below is the minimal implementation of exactly that sentence; nothing in it is beyond the frozen
text.

### R1 — Roots are fixed absolute constants

`R36=/fast/scratch/hyaku/kasegi-r36`, `R37=/fast/scratch/hyaku/kasegi-r37`,
`R38=/fast/scratch/hyaku/kasegi-r38`, hard-coded in the production path. No flag, env var or
`--scratch-root` may retarget them (a retargetable root is a forgery: point it at an empty temp
dir and G6 goes green). Selftest passes fixture roots to the internal check function only.

### R2 — Count entries, not directories (the D-E fix)

For each root: `find "$root" -mindepth 1 -maxdepth 1 -print0` (NUL-delimited; regular files,
dotfiles, symlinks, fifos, empty dirs all count as one entry each). The r37 `-type d` filter must
not survive: D-E exists precisely because a file at `kasegi-r37/` was invisible to it.

### R3 — Absence is green, unreadability is red

- `[ ! -e "$root" ] && [ ! -L "$root" ]` → that root contributes 0 entries (`r36=absent`).
- Root present but `find` exits non-zero (permissions, I/O) → G6 red with
  `r3x=unreadable`; the rc is captured before any pipe and never `2>/dev/null`-ed into 0 (r36
  D6 family; the same fail-closed discipline r37 applied to its status read).
- Enumerate `R36` and `R37` independently so the payload names which root is dirty.

### R4 — Exclude exactly one entry: the suite's own `--work` dir, by canonical identity

The exclusion applies only to `R38`, and only to a **direct child**:

```
work_real=$( cd "$WORK" && pwd -P )          # WORK exists before G6 runs
r38_real=$( cd "$R38"  && pwd -P )
tolerate_name=$(basename -- "$work_real")     # only if dirname(work_real) == r38_real
```

For every direct entry `c` of `R38`: tolerate it iff `$R38/$c` is a directory, `[ ! -L "$R38/$c" ]`,
and `realpath` of `$R38/$c` equals `$work_real`. Count everything else (`r38=<residual>`); G6
closes only when `r38 == 0`.

Constraints that make this safe and non-launderable:

1. **`WORK` must be empty before extraction.** The suite checks
   `find "$WORK" -mindepth 1 -print -quit` and dies exit 2 if non-empty. Without this, a runner
   could pass its own populated scratch dir as `--work` and have a leftover seat dir tolerated as
   "the suite's work dir".
2. **`WORK`'s canonical parent must be `R38`** (so the tolerated entry is one direct child), or
   `WORK` must lie outside all three roots — in which case the tolerated set is empty and `R38`
   must be empty. If `WORK` is nested deeper (`R38/L1/work`), its ancestors are **not** excluded:
   `L1` is an entry → red. Ancestor laundering is the one loophole that would let a still-running
   seat pass, so it is closed explicitly.
3. **No name/glob/prefix matching, no symlink following.** A child named like the work dir but
   resolving elsewhere is an entry; a symlink child is an entry even if its target is `WORK`.
4. All suite temporaries (`export/`, `mut/` — the r37 shape `EXPORT=$WORK/export`,
   `MUT=$WORK/mut`) live inside `WORK`, so the suite never adds a second direct child.
5. Ordering: create/validate `WORK` first, then read `R38`; on EXIT the suite removes `WORK`
   (auto-created case), so a post-run re-read finds `R38` empty.

Practical default that satisfies all five: the suite auto-creates its work dir with
`mktemp -d -p "$R38" r38-closure-work.XXXXXXXX`; a supplied `--work` is accepted only under the
preconditions above.

### R5 — The dir of a seat still running is a leftover: G6 red

No exclusion, no wait, no retry, no PID/file-recency heuristic. Any `R38/<SEAT>` entry — even an
empty dir — is counted in `r38` and fails G6, and any entry under `R36`/`R37` fails those limbs.
The check is a single live reading at suite-run time (concurrent creation after the read is out
of scope and must be stated as such in the suite's comments). Consequences the round must plan
for:

- A still-running seat cannot be distinguished by this check from a leaked one, so the
  conservative verdict is red. That matches the frozen kill rule ("any leftover
  kasegi-r36/r37/r38 scratch entry at filing").
- The judged run must therefore be executed by a process whose own scratch is **outside** the
  three roots. A live `/fast/scratch/hyaku/kasegi-r38/L1` would keep `r38` non-zero and G6 red
  even after every other seat has exited; running from `kasegi-r38/L1` and passing
  `--work` elsewhere does not help. The clean sequencing is: all seats yield and remove their
  dirs → the L1's final-gate scratch is a work root not named `kasegi-r36/r37/r38` (e.g. a
  fresh `--work` outside them, leaving `r38` empty) → run the suite over J → write the receipt.
  This is the round-37 `l1prep/` lesson (ExecQuiescenceProbe §3a) carried forward one level:
  round-37's fix was "L1 removes `l1prep/`"; round 38 must instead make the check count files and
  run the gate from scratch the check does not scan.
- If `R38` does not exist at all, it contributes 0 entries (green) by R3.

### R6 — Payload and selftest

Suggested closed line: `G6 payload=r36=<absent|0|N>,r37=<absent|0|N>,r38=<residual>,work=<inside|outside|absent>,work-entries=0 closed=1`.
Selftest cases (each must be **rejected**), one `selftest case=G6` line each:

1. a stray **regular file** directly under `R36` (the D-E shape) → red;
2. a stray dotfile directly under `R37` → red;
3. `R38` with `WORK` plus one empty dir → red (`r38=1`);
4. `WORK` non-empty at suite start → die exit 2 (violates R4.1);
5. `WORK` nested one level below `R38` (`R38/X/work`) → red on `X` (violates R4.2);
   positive: `R38` containing only an empty `WORK` → green, and all three roots absent → green.

Mutants are run against fixture roots through the internal function; the production roots stay
hard-coded (§R1), so the selftest cannot become a forgery surface.

### R7 — Scope note: G6 as frozen is scratch-only

The frozen G6 sentence covers scratch roots only. r37's E9 also carried `status-dirty` /
`head-match` / `lane-root` limbs; those are not part of G6's predicate here and must not be added
to its `closed` computation silently. If the suite prints them, keep them as separate payload
fields and do not let them flip G6: at the judged run the all-gates receipt does not exist yet
(so the worktree is momentarily dirty by that file, or clean, depending on when it is written),
and a status limb would make the required `closed=8/8` run fragile without being in the claim.
The lane-clean-at-filing obligation lives in the C1 kill rule, not in G6. Conversely, if G6
includes only scratch, base and r37-head exports will read G6 green (the host is quiescent at
those runs); their required `closed<8/8 exit=1` comes from G1–G5/G7/G8 and is unaffected.

## 4. Projection at this measurement

| Limb | Measured 18:26–18:30Z | G6 verdict now |
|---|---|---|
| `R36` zero entries / absent | absent | green (absent) |
| `R37` zero entries / absent | absent (was 1 file, `build-spec.py`, at the 18:16:23Z freeze) | green (absent) |
| `R38` nothing but the suite's `--work` dir | 16 direct entries at 18:26Z, 22 at 18:27Z, 26 at 18:29:21Z, incl. `L1` and live seats | **red** (no suite `--work` exists yet; every entry is a leftover under R5) |

So G6 is expected to be red for the whole wave and to be green only at the judged run, under the
sequencing in §R5. Any `closed=8/8` observed while any seat dir stands is a forged or broken
reading.

## 5. Risks and limits

- The reading is live host state, not export content: the same suite bytes can print different
  G6 verdicts at different moments. This is inherent to D-E's frozen wording ("live scratch
  quiescence") and must be documented in the suite, not "fixed" by snapshotting.
- The r38 root is shared with live peers; the samples in §1.3 are point-in-time and the dir set
  moved by ten entries in ~3 minutes. No count here should be compared to a count in another
  receipt without a timestamp.
- The D-E pre-state in `c1-controls/before.txt` (1 file at 18:16:23Z) is already gone at 18:29Z.
  A future observer must not read the current absence as "G6 was always clean": the before-state
  is the committed control, and the rule in §R2 is what prevents recurrence.
- I did not run the r38 suite (it does not exist at HEAD; `git ls-tree -r --name-only HEAD |
  grep -c r38-closure` → 0), so no G6 green/red transcript from the instrument itself is claimed
  here; §3 is the implementable rule, §4 the host-state projection.

## 6. Tooling and scratch

- Installed/upgraded: none (no pacman; host-wide pause respected — no uv/npx/official binary was
  needed; stdlib `find`/`git`/`ls`/`df` only).
- Lane writes: this receipt only. No mutating git command; no lane/fleet/sibling/source-tree
  edit; `agent://ExecSuiteBuild` received two advisory coordination notes with the §R2–R5 traps
  and the §7 reply.
- Scratch `/fast/scratch/hyaku/kasegi-r38/ExecQuiescence/` removed before yield; verified absent
  (`ls -d` → exit 2).

## 7. Peer coordination — suite builder's G6 divergence (recorded for the L1)

ExecSuiteBuild replied on `agent://` that it adopts the entry-count limb (R2), the fail-closed
`find` rc (R3) and the live-seat rule (R5) verbatim, but its item fixes the r38 residual as
"absent or contains no entry other than the realpath of the suite's own `--work` dir (or its
top-level parent under `kasegi-r38`)": the direct child equal to WORK's top-level parent under
`kasegi-r38` would be tolerated, because `TMPDIR=$S` with `S=/fast/scratch/hyaku/kasegi-r38/<SEAT>`
makes WORK sit one level below a direct child. That is a deviation from the frozen C1 G6 wording
("holds nothing except the suite's own `--work` dir") and, unqualified, a laundering path:

- `--work /fast/scratch/hyaku/kasegi-r38/<X>/w` would tolerate `<X>` even when `<X>` is a leaked or
  still-running seat dir with leftovers;
- when the tolerated child is WORK itself (`--work=$S`), its contents are below `-maxdepth 1`, so a
  populated seat scratch passes unless WORK is required empty before extraction.

Constraints I sent back, which would make the parent carve-out defensible rather than a claim
change: (a) chain-empty — the tolerated direct child may contain at `-maxdepth 1` only the next
realpath component toward WORK, nothing else (a sibling leftover is red); (b) WORK empty before
extraction (`find "$WORK" -mindepth 1 -print -quit` empty, else die exit 2), without which (a) is
vacuous when the tolerated child is WORK; (c) the payload prints the tolerated path and selftest
rejects a tolerated parent with a sibling leftover, a populated WORK, and WORK outside `R38` with
a stray entry under `R38`.

Claim-literal shapes for the judged run, either of which needs no ancestor carve-out: pass the
run dir itself as `--work` (the sole direct child of `kasegi-r38`, emptied first), or run with
WORK outside `kasegi-r36/r37/r38` while `kasegi-r38` is empty. Under either shape the §R4 rule as
written holds byte-for-byte with the frozen G6 sentence, and the L1 can rule on the divergence
without a stricter reading being imposed by this seat: this receipt states the rule and records
the builder's stated deviation; it does not adopt the deviation as green.
