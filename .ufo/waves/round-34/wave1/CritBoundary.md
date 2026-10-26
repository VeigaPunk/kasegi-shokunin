# CritBoundary — round-34 scope-guard critique (critic, leaf)

Seat: CritBoundary · Round: kasegi-shokunin round 34, wave 1 (hyaku run 8, dispatched by KasegiR34) · Date: 2026-10-26
Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`; lane HEAD at audit `206e5108f1190e61b3e2622d21cab8a5d921650c`.
Assignment: scope-guard critique only — (A) seat writes outside the lane write scope, (B) lane git/jj state mutation, (C) sibling repos and shokuknow, (D) scratch-root discipline and leftover trees. C1/C2 claim correctness is out of scope for this seat.

## Report

### 0. Method, self-disclosure, scratch

Every command below was read-only except this receipt. Two things I did that touched state outside my seat's own writes, disclosed up front:

1. **I mutated no tree, but my reads bumped two `.git` directory mtimes.** `git -C /home/vgpnk/Projects/shokunin status` and `git -C /home/vgpnk/Projects/shokuknow status` at `02:41:22 -0300` set both `.git` **directory** mtimes to `02:41:22.05`/`.09`; no file inside either `.git` changed (`shokuknow/.git/index` is still `2026-10-24 23:33:24`). Any later audit that sees `shokuknow/.git` newer than dispatch is seeing *this seat's* read, not a seat write.
2. **Scratch**: `/fast/scratch/hyaku/kasegi-r34/CritBoundary` (4 files: two `touch` reference stamps, notes) was removed before this receipt was written —
   `rm -rf -- /fast/scratch/hyaku/kasegi-r34/CritBoundary` → `ls: cannot access '…/CritBoundary': No such file or directory` (exit 2 from `ls`, tree absent). Directory count under the round root went `16 → 15`.

For (B) I deliberately did **not** use bare `jj` reads: every `jj` call below carries `--ignore-working-copy`, which is the only form that does not snapshot (verified with a positive control in §2.4 — my op-id reads all return the same top op).

Tool versions used: `git 2.x` (host), `jj` at `/home/vgpnk/.local/bin/jj`, `find`/`stat` coreutils. Nothing installed or upgraded.

---

### 1. Axis A — writes outside the lane write scope: **FAIL (one file, author proven)**

#### A1. `/home/vgpnk/Projects/shokunin/baseline-plain.txt` — fleet-root write by lane seat `RevKillRule`

Measured `2026-10-26T05:49:18Z`, still on disk at audit end:

```
$ cd /home/vgpnk/Projects/shokunin && sha256sum baseline-plain.txt; wc -l baseline-plain.txt
56f08a92037cc2520dc89f23f4acd0fdffc4a9331796e7cfbff7c534263a6038  baseline-plain.txt
13 baseline-plain.txt
$ stat -c '%y %s' baseline-plain.txt
2026-10-26 02:37:04.340777462 -0300 850
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | grep baseline
?? baseline-plain.txt
```

Content is a `capture-binding-check.py` *plain-run* audit of the **mid-wave** state (round-34 snapshot dir present, S051 registry row not yet appended):

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
… (round-24,25,26,28,29,30,31,32,34)
MANIFEST round-34 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S051 dir=round-34
records=41 bound=40 unbound=1
```

**Author and mechanism, proven from the seat's own tool-call transcript** (I re-derived this independently of `SentScopeFinal` §A1 and it reproduces byte-for-byte):

```
$ grep -o 'capture-binding-check.py > [^;]*' \
  ~/.omp/agent/sessions/-Projects-shokunin/2026-10-26T03-41-55-460Z_01a1764c-ed84-730d-b290-e516d052c218/RevKillRule.jsonl
capture-binding-check.py > \"$PWD/../baseline-plain.txt\" 2>&1
capture-binding-check.py > \"$PWD/../baseline-plain.txt\" 2>&1
capture-binding-check.py > /fast/scratch/hyaku/kasegi-r34/RevKillRule/cb-round33.py && sha256sum …
```

With `$PWD = /home/vgpnk/Projects/shokunin/kasegi-shokunin` (the session cwd is the lane root — the same default cwd this seat inherits), `"$PWD/../baseline-plain.txt"` resolves to the **fleet root**. The seat's *other* writes in the same line use absolute `/fast/scratch/...` paths, so the misroot is a single `../` in one redirect, not a scratch-root misconfiguration.

The same command's second redirect produced the sibling in-lane stray, still on disk:

```
$ sha256sum kasegi-shokunin/selftest-baseline.txt; stat -c '%y %s' kasegi-shokunin/selftest-baseline.txt
ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51  kasegi-shokunin/selftest-baseline.txt
2026-10-26 02:37:05.022777160 -0300 1552
```

`RevKillRule.md` does **not** exist at audit end (`ls .ufo/waves/round-34/wave1/RevKillRule.md` → `No such file or directory`), so non-disclosure is pending rather than consummated; the seat is still live (scratty tree `files=20`, no process at the last scan). **Impact: no content harm** (a stdout capture; no lane file altered, no fleet tracked file altered) but the fleet worktree is dirtied for every other lane's L1 and a declared read-only tree was written.

#### A2. No in-lane byte copy exists, so "just delete it" loses the only file-form evidence

| candidate in-lane copy | sha256 | verdict |
|---|---|---|
| `.ufo/waves/round-34/wave1/ScribeSkillGate/capture-binding-runs.txt` (31 lines) | `4ccd75baab09dcb629baa5d89fa2d415dbd1132e6449f9e5fe4013cc9fdab8bc` | **not** byte-equal; contains the three signature lines (`:27` `MANIFEST round-34 …`, `:28` `AUDIT records=41 …`, `:30` `records=41 bound=40 unbound=1`) but not the full 13-line block |
| `.ufo/waves/round-34/c1-controls/before.txt` | `d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0` | pre-dispatch control baseline, not this capture |
| `.ufo/waves/round-34/c2-controls/before.txt` | `d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0` | same bytes as c1 |
| receipts `ExecCaptureBindingHarden.md:90`, `ExecSnapshotR34.md` §5 | digest only | text of the 13 lines is quoted, digest `56f08a92…` recorded |

So the bytes are reproducible (base `014ee2d` + round-34 capture + registry row absent — all three recoverable from history) but the *file* is unique. **Smallest safe correction:** copy the bytes into `.ufo/waves/round-34/c1-controls/baseline-plain.txt` (or the wave dir) with its digest recorded in the same commit, then remove the fleet-root original. Deleting without the copy drops a file whose digest three receipts already cite but that no lane artifact can be `cmp`'d against.

#### A3. Fleet-root changes that are **not** seat writes (named so they are not scored against seats)

| path | measurement | attribution |
|---|---|---|
| `MANIFEST.json` | mtime `02:35:20.918`, **content identical to HEAD** (`git diff --stat -- MANIFEST.json` empty, `git ls-files -m` empty) | fleet bookkeeping rewrite of unchanged bytes; the only tool that writes it is `scripts/hyaku/append-closure.py` (fleet harness), not a kasegi seat; no kasegi receipt claims it |
| `.ufo/state/disk-guard.log` | untracked, growing (`02:40:00` → `02:44:14`), `1,088,517 B` | host disk-guard service (`… pressure /tmp … use=89%`) |
| `.ufo/state/{kasegi.report-baseline,watchdog.log,inline-dispatcher.log}`, `scripts/hyaku/*` | ` M` before and during the wave; `kasegi.report-baseline` mtime `02:24:05` (**pre**-dispatch) | L1/harness bookkeeping |
| fleet `.ufo` paths naming kasegi newer than dispatch | `find /home/vgpnk/Projects/shokunin/.ufo -newer <dispatch-ref> -iname '*kasegi*'` → **empty** | no lane seat wrote into fleet `.ufo`/`state`/`watchdog.log` |
| fleet-root files newer than dispatch, depth 1 | `MANIFEST.json` (02:35), `baseline-plain.txt` (02:37) — nothing else (files at 02:27 predate the 02:29:48 dispatch commit) | one finding (A1) |

**Axis A verdict: FAIL** — exactly one seat-authored out-of-lane write (`baseline-plain.txt`, `RevKillRule`, proven from transcript), plus its in-lane twin `selftest-baseline.txt`. Everything else at the fleet root is harness bookkeeping or unchanged-content touches.

---

### 2. Axis B — lane git/jj state: **FAIL at the jj level (no git commit/branch mutation)**

#### B1. No seat commit, no branch change, nothing staged

```
$ git rev-parse --short master                                   → 206e510
$ git reflog -2                                                  → 206e510 … export from jj / 29f606d … export from jj
$ git log -1 --format='%h %ci %s' master                          → 206e510 2026-10-26 02:29:48 -0300 round-34: wave-1 spec …
$ git diff --cached --name-only | wc -l                          → 0
$ ls .git/*.lock                                                 → No such file or directory
$ stat -c '%y %n' .git/logs/HEAD .git/refs/heads/master          → 02:29:48.204 / 02:29:48.247 (dispatch commit only)
```

`.git/index` mtime is `02:39:17.390713214` — see §2.5 for the corrected mechanism.

#### B2. Four jj working-copy snapshots were created by seats — and each one exported a **commit object + `refs/jj/keep/*`** into the lane's `.git`

`jj --ignore-working-copy --no-pager op log --limit 6` (read-only; op ids as printed):

```
@  3038db8e52bc  snapshot working copy   args: jj status
○  1c80be616d4b  snapshot working copy   args: jj status
○  497fe0c449c0  snapshot working copy   args: jj log -r 'ancestors(@, 6)' --no-pager
○  2d099a7898ec  snapshot working copy   args: jj log -r 'ancestors(@, 8)' --no-graph -T '…'
○  2a94577af3ba  push bookmark master to git remote origin  args: jj --config 'snapshot.auto-track="none()"' git push …
○  3751c35b0b54  point bookmark master to commit 206e5108…   args: jj --ignore-working-copy bookmark set master -r 206e5108…
```

The L1's own ops all carry `--config 'snapshot.auto-track="none()"'`/`--ignore-working-copy`; the four snapshots carry neither, so they are not the L1's. Mapping each op to its git-side footprint (my addition — the peer scope receipt stops at the op log):

| op | time | `refs/jj/keep/` ref created | working-copy commit | tree |
|---|---|---|---|---|
| `2d099a7898ec` (`jj log -r 'ancestors(@, 8)'`) | 02:34:52 | `bf974b0f…` | `bf974b0f911d26d4abf89975df36054109863a24` | `9fa9fc08…` |
| `497fe0c449c0` (`jj log -r 'ancestors(@, 6)'`) | 02:35:40 | `2ac99083…` | `2ac99083c55090eae1aa6106d9782302cbdb07e5` | `dd14bc25…` |
| `1c80be616d4b` (`jj status`) | 02:37:58 | `ce155c58…` | `ce155c58934d4bac27ce43a4b84df9937ea08b60` | `e8678f5e…` |
| `3038db8e52bc` (`jj status`) | 02:39:17 | `be5b615a…` | `be5b615a3677ee84d341fa0fcac06095e72a2a53` | `e89ba1e2…` |

All four commits share `parent 206e5108…` and `change-id tuwssuvrlzqwltvksokxqvsnqtptoqqs`; committer timestamps `1792992892/1792992940/1792993078/1792993157` = the four op times exactly. Object-store cost:

```
$ find .git/objects -type f -newer <02:30:10 ref> | wc -l        → 43   (loose objects, all post-dispatch)
$ git for-each-ref refs/jj/keep | wc -l                          → 290  (4 of them created by these snapshots)
$ git for-each-ref --sort=-committerdate … refs/jj/keep | head -4
refs/jj/keep/be5b615a… 2026-10-26 02:39:17 -0300
refs/jj/keep/ce155c58… 2026-10-26 02:37:58 -0300
refs/jj/keep/2ac99083… 2026-10-26 02:35:40 -0300
refs/jj/keep/bf974b0f… 2026-10-26 02:34:52 -0300
```

**False-provenance hazard (new, not in the claims and not in the peer scope receipt):** because jj keeps exported commits alive under `refs/jj/keep`, `git log --all` now puts a phantom, empty-subject commit at the top of the lane's all-refs history:

```
$ git log --all --oneline -1        → be5b615        (empty subject, mid-wave partial tree)
$ git log --oneline -1              → 206e510 round-34: wave-1 spec …   (master correct)
```

Any later audit, instrument or L1 sweep that reads "the tip" with `git log --all` / `git describe --all` / `git rev-list --all` will see four wave-time commits whose trees are *intermediate* wave states. The landing itself is safe (`master` unchanged, `git diff --cached` empty), but "the tip" must be read as `master`, not `--all`.

#### B3. Torn-file probe on the four snapshots — **negative** (no corrupted capture)

A snapshot can in principle record a file another seat is mid-write. Tested: for every path each snapshot commit changes, compare the recorded blob against today's bytes.

```
02:34:52 bf974b0f: 8 paths — equal=4 superseded=2 prefix=2 (QUALITY.md 29726→30340, round-33.md 47069→49907)
02:35:40 2ac99083: 8 paths — equal=5 superseded=2 prefix=1 (QUALITY.md 29726→30340)
02:37:58 ce155c58: 11 paths — equal=7 superseded=1 prefix=3 (QUALITY.md, SOURCES.md 57170→58561, instruments/README.md 57986→69960)
02:39:17 be5b615a: 11 paths — equal=8 superseded=3 prefix=0
```

Every "prefix" blob ends on a newline with a coherent sentence tail (`…proposal 6 (2026-10-25) |\n`, `…pre-append → 50 post-append (R8).\n`, `…case lines is not the landed selftest.\n`); the prefix class is explained by the corpus's append-only authoring (QUALITY.md grew 29726 → 30183 across the snapshots), not by truncation. No mid-line cut, no zero-length read. **The jj side effect is content-safe; it is a rule and ref-namespace defect, not a data-integrity defect.**

#### B4. Positive control for this seat

Two `jj --ignore-working-copy op log` reads (start and end of this audit) both report top op `3038db8e52bc` unless a seat adds one; this seat added zero operations. The instrumented form is the fix, and it costs nothing.

#### B5. Three receipts declare jj cleanliness that is false under jj semantics

| receipt | line | claim | its own op |
|---|---|---|---|
| `RevErrata.md` | `:12` `No git/jj mutation performed; no writes outside this receipt.` and `:153` `… no git/jj mutation; …` | no jj mutation | `497fe0c449c0` (`jj log -r 'ancestors(@, 6)'`), which snapshotted |
| `RevClaimsFreeze.md` | `:16` `… no jj mutations, no writes outside this receipt and the scratch dir` | no jj mutation | `2d099a7898ec` (`jj log -r 'ancestors(@, 8)'`) |
| `ScoutDatawalk.md` | `:73` `No repo mutation (no git add/commit, no jj mutation); …` | no jj mutation | `1c80be616d4b` (`jj status`) |
| `ScoutQuarantine.md` | `:189` quotes `jj st` as a *method* | makes no cleanliness claim | `3038db8e52bc` (`jj status`) |

This is the M34-1 class (overstated cleanliness) reappearing at the scope layer: "I only read" is true of intent, false of jj's contract. `ScoutQuarantine` is clean here precisely because it disclosed the command.

#### B6. `.git/index` mtime `02:39:17.390` — mechanism correction, same verdict

`SentScopeFinal` attributes the index refresh to read-only `git status` calls. The tighter reading: `.390713214` is 7 ms after op `3038db8e52bc` (`.383`); in a colocated repo the `jj status` that snapshots also brings the git index in line with the working copy. Either way the index carries **0 staged entries** and master is untouched, so the verdict (no git mutation) holds; only the attribution wording needs to not claim a git-command cause that nobody observed.

**Axis B verdict: FAIL at the jj level** — no seat commit/branch/push, nothing staged, but four jj working-copy snapshots (2× `jj status`, 2× `jj log`) wrote one commit + `refs/jj/keep` ref + loose objects each (43 objects total), and three receipts assert the opposite. Content-integrity probe negative.

---

### 3. Axis C — sibling repos, shokuknow, bounties: **PASS**

```
$ git -C /home/vgpnk/Projects/shokuknow status --porcelain | wc -l   → 1918   (all pre-existing campaign edits)
$ find /home/vgpnk/Projects/shokuknow -newer <dispatch-ref> -not -path '*/.git/*' | wc -l → 0
$ stat -c '%y' /home/vgpnk/Projects/shokuknow/.git/index            → 2026-10-24 23:33:24 (no git add/commit this round)
$ find /home/vgpnk/Projects/bounties -newer <dispatch-ref> -not -path '*/.git/*' | wc -l  → 0
```

The only newer entry under shokuknow is the `.git` **directory** (`02:41:22`), created by my own read in §0.1.

Sibling lanes are demonstrably running their *own* rounds concurrently, so their dirt is theirs, not ours:

```
kaidoku-shokunin  85218c59 2026-10-26 02:33:07  protocol-shokunin round-36 verifier spot-check
kengaku-shokunin  e95cf55  2026-10-26 02:38:41  kengaku-shokunin round-38: first recorded build-pmars probe …
tabi-shokunin     9cc92b0  2026-10-26 02:39:25  tabi-shokunin round-29: 23 independent re-fetch records (wave 2) …
souji-shokunin    9dcd367  2026-10-26 02:16:06  souji-shokunin round-30: C3 after-measurements …
```

Checks for kasegi fingerprints in siblings and in other rounds' scratch roots:

```
$ for r in /fast/scratch/hyaku/*/; do find "$r" -maxdepth 3 -iname '*kasegi*'; done   → only /fast/scratch/hyaku/kasegi-r33 itself
$ ls -la /fast/scratch/hyaku/kasegi-r33/                                              → empty (0 files)
$ find /home/vgpnk/Projects/shokunin -maxdepth 2 -newer <dispatch-ref> -not -path '*/kasegi-shokunin/*' … → sibling files, all inside sibling trees
```

No kasegi-named file exists in any sibling lane, sibling scratch root, shokuknow or bounties. **Axis C verdict: PASS.**

---

### 4. Axis D — scratch discipline: **PASS at snapshot (14 trees live at close-of-audit; two watch items)**

All seat trees that existed during the round are under the assigned root — no seat used `/tmp`, `TMPDIR`, or its lane directory as a work tree, and no seat created a root outside `/fast/scratch/hyaku/kasegi-r34/<seat>/`. Counts over the wave: `30` dirs / `1.3G` at `02:41` (peer measurement) → `16` / `511M` at `05:48:30Z` → **`14` / `475M`** at `05:50:43Z`, after my own tree was removed at `05:49Z`.

Inventory at `05:50:43Z` (`files` = regular files; `live` = a process whose argv names the tree; `receipt` = mtime of `wave1/<seat>.md`; both `wait-*.sh` watchers observed running at `05:40`/`05:45` had exited by `05:50:37Z`, which is why neither appears live):

| tree | files | receipt | live | note |
|---|---|---|---|---|
| `ExecRegressionC1` | 6837 | – | yes | `wait-quiescent.sh` polling |
| `ExecDoNothingReject` | 6842 | 02:49:09 | yes | live after receipt (post-receipt cleanup) |
| `SimplifierCleanup` | 155 | – | yes | live |
| `ExecRDefectClosureSuite` | 6820 | 02:50:35 | no | receipt 8 s old at measure — **re-check at close** |
| `ExecKillRuleCheck` | 13 | 02:45:46 | no | receipt 5 min old, 13-file tree remains — **watch item** |
| `MutFrontierRuleA` | 35 | 02:50:13 | no | receipt 30 s old at measure |
| `ExecCensusAfter` | 10 | – | no | `wait-landed.sh` exited between `05:45` and `05:50` (no `QUIESCENT` path reached in the observed window); seat has not yet reported |
| `MutRSuiteChecks` / `ScribeLesson` / `ScribeReportDraft` / `ExecNoHarmFinal` / `RevKillRule` | 4–6824 | – | no | seats live / not yet reported; not violations until yield |
| `ScribeScorecard` / `ScribeShonen` | 0 | – | no | created, never populated (harmless) |

Cleanup happened properly for the seats that finished and yielded: `ExecCaptureBindingHarden`, `RevC1BeforeAfter`, `RevC2BeforeAfter`, `RevRowS051`, `ScoutDatawalk`, `ScoutImmunefiLive`, `ScribeAssimilationGate`, `ScribeQualityDraft`, `ScribeSOURCESRow`, `ScribeSkillGate`, `ExecSnapshotR34`, `ExecFrontierBidirectional`, `ExecHarnessAfter`, `RevCensus`, `RevNoHarm`, `RevErrata`, `MutSelftestSummary`, `MutCaptureBindingLimbs` — no tree remains for any of them (verified by `ls -1d`). The rule bites at yield, and every yielded seat has so far complied.

`/tmp` (allowed for files < 50 MB, but litter outlives the round):

| path | size | mtime | round |
|---|---|---|---|
| `/tmp/_idx_r34.txt` | 4,122 B | `02:35:46` | **34** (Immunefi page text; a Scout's intermediate) |
| `/tmp/kasegi-msg-*.txt` ×5, `/tmp/kasegi-r33-msg.txt` | 329–393 B | `01:18:26–28` | 33 (prior round, never cleaned) |

None exceeds the size allowance; the finding is hygiene — round-33's message files are still there, so round-34's will be too.

**Axis D verdict: PASS at snapshot.** No live-or-yielded seat is using the wrong root; two trees need a close-time re-check — `ExecRDefectClosureSuite` (receipt `02:50:35`, 6820-file tree, no process) and `ExecKillRuleCheck` (receipt `02:45:46`, 13-file tree, no process). Both seats may still be running (their receipts may be incremental), so this is a re-check order, not a violation.

---

### 5. Verdict and smallest safe corrections

**Overall: the round's scope discipline fails on two axes and passes on two.**

| axis | verdict | evidence |
|---|---|---|
| A — out-of-lane writes | **FAIL** | `baseline-plain.txt` at fleet root, 850 B, `56f08a92…`, `RevKillRule` proven; in-lane twin `selftest-baseline.txt` `ca3759d1…` |
| B — lane git/jj | **FAIL (jj only)** | 4 snapshot ops → 4 working-copy commits + 4 `refs/jj/keep` + 43 objects; master/staged/reflog clean; 3 receipts claim otherwise |
| C — siblings/shokuknow/bounties | **PASS** | 0 kasegi fingerprints; sibling dirt is their own concurrent rounds |
| D — scratch | **PASS at snapshot** | 15 trees, all under the assigned root; every yielded seat cleaned; `/tmp` litter |

Ranked, smallest-safe-first for the L1:

1. **Preserve then remove the fleet-root stray.** `cp /home/vgpnk/Projects/shokunin/baseline-plain.txt .ufo/waves/round-34/c1-controls/baseline-plain.txt` (digest `56f08a92037cc2520dc89f23f4acd0fdffc4a9331796e7cfbff7c534263a6038`), record it in the integration receipt, then delete the fleet-root original. Do the same for `selftest-baseline.txt` (`ca3759d1…`) or drop it — it is in-lane but unintended and no receipt owns it.
2. **Land from `master`, never `--all`.** Four phantom, empty-subject wave commits (`bf974b0f`, `2ac99083`, `ce155c58`, `be5b615a`) now top `git log --all`; they are mid-wave partial trees kept alive by `refs/jj/keep`. Do not delete the keep refs (jj owns them); state in the landing receipt that `--all` shows them and that `master` is the only content history.
3. **Rule wording for round 35 (root cause, not blame).** "Never run jj mutations" is read by seats as "`jj log`/`jj status` are safe". They are not: any jj command without `--ignore-working-copy` snapshots. Say: *lane inspection uses `jj --ignore-working-copy …`; a bare `jj` is a mutation.* The four snapshots cost nothing in content (§B3) but four seats would have declared clean while writing state.
4. **Re-run axis D at wave close** for `ExecRDefectClosureSuite` (receipt `02:43:37`, 6818-file tree, no process) and `ExecDoNothingReject` (receipt `02:47:35`, 6840-file tree); and have `RevKillRule` disclose the `$PWD/../` redirect in its receipt when it yields — its command is otherwise clean (all other paths absolute under its scratch root).

No claim C1/C2 content is touched by any of this: the stray capture is a *before*-state, the phantom commits are not reachable from `master`, and the scratch trees are outside the lane.
