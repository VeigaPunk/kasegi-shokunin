# ExecQuiescenceProbe — round-37 pre-wave quiescence probe

Seat: ExecQuiescenceProbe (executor, depth:verifiability). Item: verify the round's
quiescence preconditions (E9-relevant) — lane `git status --porcelain` count, scratch
seat-dir count before seats run, `disk-guard.sh status` (green? free space),
`df -h /fast/scratch/hyaku /tmp`, and that `git rev-parse master` equals base
`b56a41680cefd391868c1c370dc063c69d827e7d`. Report findings; state what the round
must do if any precondition fails.

Verdict: **preconditions hold in substance; two of the four literal commands no
longer read as written because the round has advanced past its base and is mid-wave.
One live cleanup obligation (`l1prep/`) will turn E9 red at the final gate if it
survives, and one measured fail-open shape in the r36 suite's scratch limb is not
covered by the frozen D6 wording.**

Live lane write: this receipt only. No install, no lane edit, no scratch left behind.

## 0. Verdict table (measured 2026-10-26T17:00–17:05Z)

| Precondition | Literal command at probe time | Verdict |
|---|---|---|
| base binding | `git rev-parse master` → `b362068195d5489aa94b31e6ec8f880c367e0ba0` (≠ base) | **PASS in substance** — base is the round's exact root (§1) |
| lane clean | `git status --porcelain \| wc -l` → `6` (≠ 0) | **PASS in substance** — 0 outside round-37, 0 tracked drift; the 6 are this wave's own untracked artifacts (§2) |
| scratch seats = 0 before seats | live `find … -type d \| wc -l` → `13` | **PASS** — the pre-seat `0` **is recorded**, in a committed before-control; the live count is post-wave by construction (§3) |
| disk-guard | `disk-guard.sh check` → `rc=0`, `ok` on all three roots (max 29% vs `SOFT_PCT=70`) | **PASS** (§4) |
| `df -h` headroom | `/fast` 578G avail (29%), `/tmp` 126G avail (3%) | **PASS** (§4) |

Pre-seat zero state, quoted verbatim from the committed before-control
(`.ufo/waves/round-37/c1-controls/before.txt`, bound at claims-freeze `224df74`,
measured `2026-10-26T16:31Z` = `13:31 -03`, i.e. 26 min before the freeze commit and
30 min before the first seat directory):

```
$ git status --porcelain | wc -l
0
$ find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l
0
```

## 1. Base binding — `rev-parse master` is now 3 commits past base, by design

```
$ git -C kasegi-shokunin rev-parse master HEAD
b362068195d5489aa94b31e6ec8f880c367e0ba0
b362068195d5489aa94b31e6ec8f880c367e0ba0          # detached HEAD, branch `master` at same hash
$ git merge-base --is-ancestor b56a416… master && echo YES
YES
$ git rev-list --count b56a416…master
3
$ git log --format='%H %p %ci %s' -4 master
b362068… f324655… 2026-10-26 14:00:19 -0300 round-37: claims-erratum-1 (S054 capture URL …)
f324655… 224df74… 2026-10-26 13:59:17 -0300 round-37: wave evidence — spec/plan/dispatch
224df74… b56a416… 2026-10-26 13:57:07 -0300 round-37: claims freeze + before controls
b56a416… c20300d… 2026-10-26 13:47:37 -0300 round-36 verifier spot-check (integrator, hyaku)
```

So the honest assertion is **not** `rev-parse master == b56a416` but
`merge-base --is-ancestor b56a416 master`, `rev-list --count b56a416..master == 3`,
and those 3 commits are the round's own (claims freeze `224df74`, wave evidence
`f324655`, claims-erratum-1 `b362068`). The literal equality held only in the
window before the freeze commit: `git rev-parse 224df74^` → `b56a416…`, so
immediately before the round's first commit `master` was exactly the declared base.
The declared claims-freeze commit `224df74` is an ancestor of `master` (YES).

Integrity of the base→head span (this is the check that matters for a no-smuggling
claim, and it is stronger than the literal one):

```
$ git diff --name-only b56a416…..master | grep -v '^\.ufo/waves/round-37/' | wc -l
0
$ git diff --name-only b56a416…..master
.ufo/waves/round-37/c1-controls/before.txt
.ufo/waves/round-37/c2-controls/before.txt
.ufo/waves/round-37/census-before.txt
.ufo/waves/round-37/claims-erratum-1.md
.ufo/waves/round-37/claims.json
.ufo/waves/round-37/wave1-dispatch.json
.ufo/waves/round-37/wave1-plan.out
.ufo/waves/round-37/wave1-spec.json
```

8 files, all inside the round directory, zero bytes changed anywhere else in the
lane since base.

Note for the integrator: `HEAD` is **detached** at `b362068` (`git rev-parse
--abbrev-ref HEAD` → `HEAD`, branches show `* (no branch)`). Any integration commit
must name its target branch/tip explicitly; a bare `git commit` would advance a
detached HEAD and leave `master` behind.

## 2. Lane cleanliness — 6 porcelain lines, all this wave's own untracked artifacts

```
$ git status --porcelain | wc -l
6
$ git status --porcelain
?? .ufo/waves/round-37/assimilation/
?? .ufo/waves/round-37/wave1-plan.err
?? .ufo/waves/round-37/wave1-run.err
?? .ufo/waves/round-37/wave1.ready
?? .ufo/waves/round-37/wave1.ready.partial
?? .ufo/waves/round-37/wave1/
$ git status --porcelain --untracked-files=all | wc -l
9        # assimilation/{collisions,quarantine-slice,reg-ids,staged-ids} + wave1/swarm-registry.json
$ git status --porcelain --untracked-files=all | grep -v '^?? \.ufo/waves/round-37/' | wc -l
0        # nothing dirty outside the round directory
$ git diff --name-only | wc -l          # unstaged tracked changes
0
$ git diff --cached --name-only | wc -l # staged changes
0
$ git status --porcelain --ignored | grep -c round-37
0        # no ignored residue inside the round dir (32 ignored entries exist, all pre-existing .jj/ + __pycache__)
```

Read correctly: **zero tracked drift, zero dirty paths outside `.ufo/waves/round-37`**.
The 6 lines are the wave's own in-flight artifacts, which are untracked by
construction — `wave1/` is where every seat's receipt lands, so porcelain must be
non-zero for the whole wave. Two consequences the round has to respect:

- **E9 limb (b) has a measurement window, not a value.** It can read 0 only
  (i) at the pre-dispatch instant (recorded, §0) or (ii) after an integration commit
  that lands every artifact. It cannot read 0 during the wave.
- Porcelain at default `--untracked-files=normal` collapses a whole directory to one
  line, so `wave1/` (all 60+ receipts) counts as **1**, not 60. The dirty count is
  therefore insensitive to seat count; that is fine, but nobody may read `dirty=1`
  as "one leftover file".

## 3. Scratch seat-dir census — pre-seat 0 is recorded; live count is post-wave

Committed pre-seat record: `0` (§0, `16:31Z`). Live samples during the wave, all
`find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 -maxdepth 1 -type d`:

| Time (UTC) | dirs | composition |
|---|---|---|
| 17:01 | 5 | 5 seats, no `l1prep` yet (first seats spawned 17:01) |
| 17:02 | 14 | 13 seats + `l1prep` |
| 17:04 | 15 | 14 seats + `l1prep` |
| 17:04:59 | 13 | 12 seats + `l1prep` — three seats had already finished and removed theirs |

The count oscillates with live seats, which is the healthy signature: seats are
removing their scratch dirs on yield (`ExecC1BaseFail`, `ExecC2QuoteOnce`,
`ExecExpectedListSync` disappeared between samples).

**The pre-seat zero is a one-shot measurement and is not re-derivable.** `l1prep/`
was created at `14:00 -03` (17:00Z), i.e. *before* the first seat at `14:01 -03`, so
from 17:00Z onward the round scratch root has never been empty again. The durable
evidence is the committed `before.txt`, not any later re-run. Anyone asked to
re-produce "0 seat dirs" after spawn will get ≥1 and must not call that a defect.

### 3a. Live obligation: `l1prep/` must be removed before the final-gate run

Current non-seat entries at the scratch root:

```
l1prep/                 # directory — COUNTED by E9's -type d limb
build-spec.py           # file — not counted
```

E9's limb (c) is `find <scratch-root> -mindepth 1 -maxdepth 1 -type d` and the r36
implementation excludes only the suite's own `--work` dir by absolute path. At the
final gate, every seat dir will be gone but **`l1prep/` will still be there unless
the L1 deletes it**, and limb (c) will report `scratch-seat-dirs=1` → E9 red →
`closed<14/14 exit=1`. Round-36 solved exactly this: its scratch round dir
`/fast/scratch/hyaku/kasegi-r36` is now empty (0 entries, `13:13`).

Preferred: L1 removes `l1prep/` (and may leave `build-spec.py`, which `-type d`
ignores). Acceptable alternative: the r37 suite excludes it by an absolute,
reported path like `--work`, with the exclusion printed in E9's payload — but that
is a name-based carve-out and a critic will (correctly) call it a loophole, so it
must be visible in the payload, never silent.

## 4. Disk — green, far from soft pressure

```
$ scripts/hyaku/disk-guard.sh check
ok root=/tmp use=3% soft=70%
ok root=/var/tmp use=35% soft=70%
ok root=/fast/scratch/hyaku use=29% soft=70%
check rc=0
$ scripts/hyaku/disk-guard.sh status   # rc=0 ; table head
root                             use%     free
/tmp                               3%   125.3G
/var/tmp                          35%   582.5G
/fast/scratch/hyaku               27%   589.6G
$ df -h /fast/scratch/hyaku /tmp
/dev/nvme1n1p2  804G  226G  578G  29% /fast
/dev/nvme1n1p1  128G  2.6G  126G   3% /tmp
```

Thresholds read from the script: `SOFT_PCT=70`, `TARGET_PCT=60`,
`ROOTS_RAW=/tmp /var/tmp /fast/scratch/hyaku`; `status`/`check` exit 1 if any root
is at or above soft. All roots are 41+ points under soft. (Measured `use%` moved
27%→29% on `/fast` while probing; the round's own scratch grew
383M → 897M → 2.2G → 2.7G in ~7 min ≈ 0.3 GB/min, which at 578G free is a
non-issue even for a long wave.)

## 5. E9-relevant instrument findings — three measured shapes the suite must handle

These are properties of the quiescence check itself, measured now, that bear on the
frozen E9/E14 wording. They are reported, not fixed — the suite is another seat's
file.

### 5a. E9 cannot run against the export (re-confirmed for r37)

```
$ git archive master .ufo/waves/round-37/c1-controls | tar -x -C $S/exporttest
$ git -C $S/exporttest status --porcelain
fatal: not a git repository …                      rc=128
$ ( set -o pipefail; git -C $S/exporttest status --porcelain | wc -l )
0                                                  pipefail rc=128
$ git -C $S/exporttest status --porcelain 2>/dev/null | wc -l
0                                                  rc=0    ← reads CLEAN on a non-repo
```

An export has no `.git`. The fail-closed form must therefore read **the live lane
worktree** (r36's `root_ok` limb already does this: `rev-parse --show-toplevel`
must equal the physical path), and must never let the export path reach the status
read. r37 keeps E9 in the 14-check export run, so this pairing must survive.

### 5b. `pipefail` alone does not close D6 — the rc is discarded

The r36 limb is (verbatim, lines 293-295 and 465-466):

```bash
count_lines() { grep -c . 2>/dev/null || true; }
porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)
porcelain=${porcelain:-0}
```

and the script already runs `set -uo pipefail`. Measured on a nonexistent repo,
reproducing those exact lines:

```
assignment rc=128
porcelain=0 (reads CLEAN)
```

`pipefail` does produce `128`, but it lands in the rc of an **assignment**, which
nothing reads; `count_lines`'s own `|| true` forces the pipeline's captured stdout
to `0`. So "E14 forbids `2>/dev/null`" is necessary but not sufficient — a rewrite
that keeps `p=$(git … | count_lines)` with pipefail and merely drops `2>/dev/null`
is still fail-open (rc 128, value `0`). Required shape, measured both ways:

```
$ ( set -uo pipefail; out=$(git -C /nonexistent/notarepo status --porcelain 2>&1); rc=$?;
    if [ "$rc" -ne 0 ]; then echo "RED status-read rc=$rc"; exit 1; fi; … )
RED status-read rc=128     → rc=1
$ ( same, against the real lane )
porcelain=6                → rc=0
```

i.e. capture git's **own** exit status before any pipe, and treat non-zero as red.

### 5c. Limb (c) reads clean on an absent scratch root — same fail-open family

`find "$sroot" … 2>/dev/null` runs inside a process substitution, `left` only
increments inside the loop, and `sroot_state=absent` is printed but **never
asserted**; the predicate is `[ "$left" -eq 0 ]`. Measured with the r36 suite on
the round-37 base export, changing only `--scratch-root`:

```
$ bash corpus/instruments/r36-closure.sh --export-ref b56a416… --scratch-root $S/NOSUCH-seat-root --work $S/workA
E9 payload=status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent closed=0
closed=8/9 exit=1

$ bash corpus/instruments/r36-closure.sh --export-ref b56a416… --scratch-root /fast/scratch/hyaku/kasegi-r37 --work $S/workB
E9 payload=status-dirty=6,scratch-seat-dirs=15,head-match=0,lane-root=1,scratch-root=present closed=0
closed=8/9 exit=1
```

A **nonexistent** scratch root yields `scratch-seat-dirs=0`, i.e. limb (c) passes.
E9 was red in both runs only through the other limbs (`status-dirty=6`,
`head-match=0`); with a clean worktree and matching head, a typo'd `--scratch-root`
would have gone **green with zero seats counted** — the doc comment's claim that
`scratch-root=present|absent` makes a typo "visible" is true but "visible" is not
"failing". `E14` as frozen only pins the `porcelain:-0` string, so this limb is
outside its letter and should be pinned too: assert `sroot_state=present` (explicit
`[ -d "$sroot" ] || return 1`, i.e. a missing root is red) and treat an unreadable
root (`find` rc≠0) as red rather than as zero leftovers.

Also measured (the underlying primitive, independent of the suite):

```
$ find /fast/scratch/hyaku/kasegi-r37/DOES-NOT-EXIST -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l
0        rc=0        ← masked
$ find /fast/scratch/hyaku/kasegi-r37/DOES-NOT-EXIST -mindepth 1 -maxdepth 1 -type d >/dev/null 2>&1
rc=1                 ← rc preserved, red
```

### 5d. Sequencing constraint for the final gate (from the artifacts, not theory)

E10 requires `.ufo/waves/round-37/final-gates/all-gates.txt` **in the export**, and
E9 requires the live worktree clean with `HEAD == export-ref`. Those two cannot
both hold for a single run unless the round does:

1. commit every seat receipt + `wave1*` + `assimilation/*` (porcelain → 0),
2. run the suite `--export-ref <that head>` with `--work` outside the lane
   (E9 green: `status-dirty=0`, `head-match=1`, `scratch-root=present`,
   `scratch-seat-dirs=0` after all seats **and `l1prep/`** are removed),
3. commit the resulting `all-gates.txt`.

Consequence to design around: the committed artifact's `export-ref` header is
necessarily the **parent** of the commit that carries it (step 3 creates a new head
after step 2 measured the old one). So E10's digest/binding check must not also
demand `artifact export-ref == carrier head` — that is unsatisfiable, and a suite
that tests it would be red on its own correct output. Round-36's actual artifact
confirms the shape: `a23dc4788aa7c98831eed6db953434034ce5ae8d:.ufo/waves/round-36/final-gates/all-gates.txt`
opens directly with `== selftest ==` and carries **no** `suite-sha256=` header (D1),
with `closed=0/9 exit=1` and `closed=3/9 exit=1` for the neg base/judged runs —
i.e. the required-red direction for thesis checks A/B is present, but the
quiescence/digest binding D1 targets is absent.

## 6. What the round must do (short list)

1. **Delete `/fast/scratch/hyaku/kasegi-r37/l1prep/` before the final-gate run**, or
   make its exclusion explicit in E9's payload. Otherwise limb (c) counts it and E9
   is red. (`build-spec.py` may stay: it is a file, and `-type d` ignores it.)
2. Measure E9 **after** the integration commit that lands all receipts/artifacts, and
   never during the wave. The pre-dispatch `0` is already recorded in `before.txt`;
   do not re-measure it and call the post-wave number a regression.
3. In the r37 suite's E9, check the **status read's own rc** (capturing rc before any
   pipe), not just the absence of `2>/dev/null` — `pipefail` is already on and does
   not help (§5b).
4. Assert `scratch-root=present` (and `find` rc=0) rather than printing it (§5c).
5. Keep E9 reading the live lane root identified by `rev-parse --show-toplevel`, never
   the export (§5a).
6. Any integration commit must name `master` explicitly — `HEAD` is detached (§1).
7. Free-space and cleanliness preconditions are green; no action needed.

## 7. Scope, tooling, scratch

- Lane writes: this receipt only. No lane file edited, no mutating git/jj command run
  (only `log/show/diff/status/rev-parse/ls-tree/cat-file/merge-base/archive` and read-only
  suite runs whose writes went to `--work` under my scratch).
- Fleet repo, sibling lane repos and `/home/vgpnk/Projects/shokuknow` untouched
  (read-only reads of `scripts/hyaku/disk-guard.sh` and `scripts/sources-census.sh`
  evidence text only).
- Tooling: **none installed, none upgraded** (nothing was needed; `git`, `find`,
  `du`, `df` suffice).
- Scratch `/fast/scratch/hyaku/kasegi-r37/ExecQuiescenceProbe/` (export fixture +
  two `--work` dirs) removed before yield.
- Retained evidence: every command/output block above was produced by this seat in
  this window; the two suite payload lines (§5c) carry `suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`
  = `sha256sum corpus/instruments/r36-closure.sh` at probe time.

## Risks

- **R1 (blocking for E9 green):** `l1prep/` survives seat cleanup by design (owned by
  the L1, created pre-spawn). Left in place, E9's scratch limb counts 1 forever.
- **R2 (verifiability):** §5c is a live fail-open in the limb E14 does not pin;
  a typo'd `--scratch-root` can read green with zero seats inspected.
- **R3 (sequencing):** a final-gate run during the wave is red by construction
  (porcelain ≥ 6, `head-match=0`); only the post-commit run is meaningful. If the
  round runs the gate first and commits after, the artifact will not match E9/E10
  bindings.
- **R4 (mechanical):** detached `HEAD`; an unnamed-target integration commit strands
  `master`.
- **R5 (evidence, non-defect):** the pre-seat `0/0` cannot be reconstructed from the
  live machine; it exists only because it was captured into `before.txt` at
  `16:31Z` and committed at `224df74`. Future rounds should keep that capture
  ordering, because a missing before-control is unrecoverable.
