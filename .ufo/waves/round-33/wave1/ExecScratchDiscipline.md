# ExecScratchDiscipline — scratch-discipline audit (kasegi-shokunin round 33)

Seat: ExecScratchDiscipline (executor). Axes: depth:verifiability, coverage. Milestone: round-33.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `690b69d`, claims freeze `6e55c8d`).
Model this seat actually ran on (from the session route, not passed by me): `opencode-go/deepseek-v4.1-flash`.
Lane writes: this receipt only. No git/jj mutation, no tool install/upgrade (none needed), no fetch,
no credential material touched, no peer messaged.

Scope, verbatim from the seat item:
> after seats settle, list $HYAKU_SCRATCH/kasegi-r33/ (if it exists) and report any seat directory
> still present (a seat that ends with its tree on disk reports that as a defect of its own); confirm
> no new `/tmp` clutter from this wave (find /tmp -maxdepth 1 -newermt '<wave start>' -name 'kasegi*'
> -o -name 'tmp*' | head; report); and confirm `disk-guard.sh status` if present.

Wave-start reference used for every `-newermt`: **`2026-10-26 01:09:27`**, the claims-freeze commit
(`6e55c8d`, `git log --pretty='%h %ad %s'` gives `6e55c8d 2026-10-26 01:09:27 -0300 round-33: freeze
claims C1/C2 with do-nothing controls, census-before, assimilation guard, watch-dog digest, LOG r32
entry (D1)`). The later dispatch commit (`a6a5023 2026-10-26 01:15:12 -0300 round-33: wave-1 spec (64
seats, v2 policy), validated plan and dispatch`) is reported as the tighter bound where it changes an
answer; for the two lists below it does not.

## 0. Method and evidence rules

Measurement instrument written for this seat, run from `$HYAKU_SCRATCH/kasegi-r33/ExecScratchDiscipline/`
(stdlib only, read-only over `/proc`, `du -xsk`, `os.walk`; no `TMPDIR` assumption, both paths passed
as arguments). It reports per seat dir: apparent size, file count, newest mtime, live PIDs (any
`/proc/<pid>/{cwd,exe,root,fd/*}` resolving under the dir), and whether the seat's wave-1 receipt exists.

```
$ python3 audit.py /fast/scratch/hyaku/kasegi-r33 .ufo/waves/round-33/wave1
```

PRE-STATE is labelled: seats were still landing while I measured. Seven measurements were taken (T0-T6; T4-T6
are tabulated in §7), and only quiescent-bytes passes are used for verdicts — T3 for the dir inventory, T5/T6
for the one charged case. T0/T1/T2/T4 numbers are in-flight observations and are never compared to a
settled column (M30-3).

| pass | wall clock | receipts landed of 64 | seat dirs |
|---|---|---|---|
| T0  | 01:18:05 | 4  | 22 |
| T1  | 01:49:16 | 55 | 7  |
| T2  | 01:49:53 | 55 | 7  |
| T3  | 01:50:31 | 55 | 7  |
| T5  | 01:53:07 | 60 | 5  |
| T6  | 01:54:21 | 60 | 4  |

Settlement poll (bounded, `sleep 20`, never busy-looped), series kept because it shows the drain rate:

```
01:18:09 receipts=5 scratch=23      01:31:11 receipts=39 scratch=18
01:19:49 receipts=10 scratch=30     01:33:52 receipts=46 scratch=14
01:22:09 receipts=15 scratch=29     01:36:52 receipts=51 scratch=11
01:24:49 receipts=22 scratch=24     01:40:52 receipts=53 scratch=8
01:28:09 receipts=30 scratch=21     01:47:11 receipts=54 scratch=8
01:30:09 receipts=34 scratch=19     01:48:51 receipts=55 scratch=7
```

## 1. `$HYAKU_SCRATCH/kasegi-r33/` — seat dirs still on disk at T3 (01:50:31)

The root exists (`exists=True`). Seven entries, all directories, 118,852 KiB apparent total:

```
CritMistakes           kb=884     files=45    idle_min=27  receipt=NO live=-
ExecScratchDiscipline  kb=40      files=8     idle_min=0   receipt=NO live=[1666685]   # this seat
ExecWaveEvidencePack   kb=52      files=7     idle_min=0   receipt=NO live=-
RevC1BeforeAfter       kb=117772  files=6706  idle_min=29  receipt=NO live=-
RevGateSpot            kb=52      files=4     idle_min=28  receipt=NO live=-
ScribeLesson           kb=8       files=2     idle_min=7   receipt=NO live=-
SimplifierCleanup      kb=44      files=2     idle_min=16  receipt=NO live=-
```

Verdict, split by the rule the item cites (§7.2 of `scripts/hyaku/lane-addendum.md`: "A seat that ends
with its tree still on disk reports that as a defect of its own"):

- **Seats that yielded (receipt present) with a tree still on disk: 1 — `ExecWaveEvidencePack`.** Of the
  60 seats with receipts at filing, the other 59 left no tree (this seat's own removed in §6). Eight
  residual dirs were created and reclaimed inside the poll window
  (`ScoutDatawalk` 117,832 KiB at T0, `ExecNoHarmFinal` peak 364,632 KiB at 01:45:01,
  `ExecBeforeReceipts` 235,616 KiB at T0, `ExecDeterminism` 117,776 KiB, `RevC1BeforeAfter` 117,776 KiB,
  `ScribeSkillGate`, `ExecCensusDry`, `ScribeLesson`).

  The charged case, measured twice. `ExecWaveEvidencePack` receipt exists (`wave1/ExecWaveEvidencePack.md`,
  mtime 01:51:28) and its §6 says: "Removed with `rm -rf -- \"$S\"` before this seat finished; nothing of
  this seat's scratch remained on disk at hand-off" (lines 235-237). The disk at T5 (`01:53:07`) and at
  post-removal (`01:54:21`) still holds it:

  ```
  CritMistakes           kb=884  files=45  idle_min=31  receipt=NO  live=-
  ExecWaveEvidencePack   kb=72   files=9   idle_min=0   receipt=yes live=-      ← charged
  RevGateSpot            kb=52   files=4   idle_min=32  receipt=NO  live=-
  SimplifierCleanup      kb=44   files=2   idle_min=21  receipt=NO  live=-
  ```

  and its nine files are byte-identical to the hashes its own receipt tabulates "before removal"
  (`sha256sum *` in `$HYAKU_SCRATCH/kasegi-r33/ExecWaveEvidencePack/` reproduces
  `672cb662…6a6c assemble.py`, `ec223b72…102c census.txt`, `fd4e0477…acad hash-check.txt`,
  `ae6cce174…fb1 index.md`, `e49f06dc…fb1 index-wave.py`, `44f745e3…c702 receipt-draft.md`,
  `55021076…2e71 render-index.py`, `b3b229285…f0029 role-coverage.txt`, `405adb03…3bfa size-summary.txt`,
  `43143 total`) — so the tree was never removed; the `rm -rf` claim and the disk disagree. That is both
  the §7.2 defect (seat ended with its tree on disk) and a claim-versus-evidence defect in a round whose
  axis is `depth:verifiability`. Remedy belongs to the L1 at landing: `inline.sh advance` purges the round
  root; the receipt row should be corrected by an appended erratum, not edited in place.
- **Seats not yet settled at T3: 6 dirs** (`CritMistakes`, `ExecWaveEvidencePack`, `RevC1BeforeAfter`,
  `RevGateSpot`, `ScribeLesson`, `SimplifierCleanup`). These carried no receipt at T3, so at that instant
  they were in flight, not defects: an in-flight tree is exactly what the wave dir is for. By the
  post-removal pass, `RevC1BeforeAfter` (117,776 KiB) and `ScribeLesson` had landed clean, and
  `ExecWaveEvidencePack` had landed **with** its tree (the charged case above); the other three still had
  no receipt and still held trees.
- **Orphan risk flagged, not charged:** at the post-removal pass three seats held trees with no receipt and
  had been idle past a plausible single tool call — `CritMistakes` (884 KiB, idle 31 min), `RevGateSpot`
  (52 KiB, idle 32 min), `SimplifierCleanup` (44 KiB, idle 21 min). `RevC1BeforeAfter` was the same at T3
  (117,772 KiB, idle 29 min) and then settled clean. If any of the three dies without yielding, §7.2 makes
  the tree its own defect and the L1 must purge `$HYAKU_SCRATCH/kasegi-r33` at landing (`inline.sh advance`
  also purges). Last observation before yield (T7, `01:56`): `RevGateSpot` had landed and its tree was
  gone; the root then held exactly three entries — the charged `ExecWaveEvidencePack` tree and the two
  unyielded `CritMistakes`, `SimplifierCleanup`.
- Dir contents say what holds the bytes: `RevC1BeforeAfter/base` is a whole-lane copy at the freeze
  revision — `du -sk .ufo corpus` → `113960 .ufo`, `3404 corpus`, and `du -sk .ufo/*` → `113588 .ufo/waves`.
  No `.git` under it (`find . -maxdepth 3 -name .git` → empty), so it is an extract, not a clone; §7.3
  asks for `git archive`/`--shared` over full clones, which this satisfies, but 114 MB of `.ufo/waves`
  history is not evidence-shaped (the rule's own wording: "a 600 MB mirror is not evidence; cite the
  revision and the command instead").
- **This seat's own dir,** reported per the same rule: created at `mkdir -p` (T0 `kb=4`), held the audit
  script, the three captures and the `TMPDIR` probe dir; removed before this receipt was filed — command
  and post-removal listing in §6.

## 2. `/tmp` — new clutter from this wave: YES — nine round-33 files, 9,676 bytes

The item's command, run literally, and the same command parenthesised:

```
$ find /tmp -maxdepth 1 -newermt '2026-10-26 01:09:27' -name 'kasegi*' -o -name 'tmp*' | head
/tmp
/tmp/kasegi-r33-msg.txt
/tmp/kasegi-msg-ExecCaptureBinding.txt
/tmp/kasegi-msg-ExecManifestUpgrade.txt
/tmp/kasegi-msg-RevC1Instrument.txt
/tmp/kasegi-msg-CritC1Kill.txt
/tmp/kasegi-msg-RevClaimsFreeze.txt
```

Two defects in the command as specified, both worth fixing in the next dispatch of this seat:
`-o` without parentheses makes `-name 'tmp*'` ignore the `-newermt` bound, and `/tmp` itself matches
because its own directory mtime is newer than the wave start. The honest form is
`find /tmp -maxdepth 1 -type f -newermt '<wave start>'` — which is what I report below.

```
$ find /tmp -maxdepth 1 -type f -newermt '2026-10-26 01:09:27'
/tmp/kasegi-r33-msg.txt
/tmp/kasegi-msg-ExecCaptureBinding.txt
/tmp/kasegi-msg-ExecManifestUpgrade.txt
/tmp/kasegi-msg-RevC1Instrument.txt
/tmp/kasegi-msg-CritC1Kill.txt
/tmp/kasegi-msg-RevClaimsFreeze.txt
/tmp/r33-prompts-dump.txt
/tmp/t.diff
/tmp/code.154.0.8037.97
/tmp/code.156.0.8078.47
/tmp/g1
/tmp/z2.tsv
/tmp/u2.tsv
```

Inventory (`stat -c '%n|%s|%y'`), with content-based attribution (a `/tmp` file carries no owner):

| path | bytes | mtime | content / attribution |
|---|---|---|---|
| `/tmp/kasegi-r33-msg.txt` | 393 | 01:18:26 | relay of the L1 erratum ruling text (`L1 ruling filed at .ufo/waves/round-33/claims-erratum-1.md…`); master copy |
| `/tmp/kasegi-msg-{ExecCaptureBinding,ExecManifestUpgrade,RevC1Instrument,CritC1Kill,RevClaimsFreeze}.txt` | 329 each | 01:18:28 | same ruling, one file per recipient seat |
| `/tmp/r33-prompts-dump.txt` | 6,187 | 01:22:15 | dump of round-33 seat prompt text (first heading `#### ExecRegistryAppend`) |
| `/tmp/t.diff` | 0 | 01:37:24 | empty diff, unattributable |
| `/tmp/code.154.0.8037.97`, `/tmp/code.156.0.8078.47` | 3 each | 01:26:02 | session/editor temp snippets, unattributable |
| `/tmp/z2.tsv`, `/tmp/u2.tsv` | 365 each | 01:38:56 | kaidoku lane manifest hashes (`usr/lib/kaidoku/blocks.bin …`) — **not** kasegi-owned |
| `/tmp/g1` | 23 | 01:48:33 | `ground: F1-jj — edge` — **not** kasegi-owned |
| `/tmp/c3counter_frozen.mjs` | 24,917 | 01:49:18 | self-identifies as the **tabi** lane gate `check-release-pins.mjs` — **not** kasegi-owned |
| `/tmp/rec59.txt` | 1,451 | 01:53:36 | list of `wave1/*.md` receipt paths (60 entries), round-33-related, owner not recorded |

Reading:

- **Round-33-owned `/tmp` writes are 9 files, 9,676 bytes total** (2,038 for the six 01:18 message files,
  6,187 `r33-prompts-dump.txt`, 0 `t.diff`, 1,451 `rec59.txt`), i.e. 0.019 % of the 50 MB `/tmp`
  allowance in §7.1. The two `code.*` snippets are 3 bytes each and not attributable to a lane.
- They are still a placement deviation from §7.1 ("The L1 puts the exact path into every seat prompt";
  scratch root is `$HYAKU_SCRATCH/<lane>-r<round>/<seat>/`) and from §7.5 ("A `/tmp` path is therefore
  never citable evidence"). The 01:18 message files are how one seat relayed the C1 Rule-B erratum to five
  seats; the correct channel is a `write agent://<id>` message, not a file.
- `/tmp/r33-prompts-dump.txt` is the one with a hygiene cost beyond size: it moves round-33 seat prompt
  text (instructions) outside the lane into a world-readable-by-user temp file that the reaper deletes
  without notice. Treated as data here; nothing in it was followed.
- Cross-check, independent seat: `wave1/SentScopeFinal.md` line 160 already measured the same 6 message
  files — "24K total  # 6 message files, 329–393 B each → inside the \"<50 MB in /tmp\" allowance; no
  committed tool hardcodes /tmp". Two seats, same set, no contradiction (its `24K` is `du` block
  allocation, the byte sum is 2,038).
- Root cause, measured: **`TMPDIR` and `HYAKU_SCRATCH` are unset in the seat environment**
  (`echo "TMPDIR=${TMPDIR:-<unset>} HYAKU_SCRATCH=${HYAKU_SCRATCH:-<unset>}"` → `TMPDIR=<unset>
  HYAKU_SCRATCH=<unset>`), while `scripts/hyaku/hyaku.env` prescribes "Launch the orchestrator session
  with `TMPDIR=$HYAKU_SCRATCH/tmp` so seat subprocesses that honour TMPDIR land there too". Any tool that
  relies on an inherited `TMPDIR` therefore lands in `/tmp`; this is the mechanism behind both the
  kasegi files and the other lanes' entries in the table.
- No residue from the round's selftests: `ls -d /tmp/capture-binding-selftest-*` → `none`.
- `/var/tmp`: no kasegi entry at all (`ls -d /var/tmp/*kasegi*` → `none`; `find /var/tmp -maxdepth 1
  -newermt '2026-10-26 01:09:27'` returns only `/var/tmp` itself). Its 38 % occupancy is prior-round
  debris kept by the guard (e.g. `keep-excluded /var/tmp/souji-r23-census-before.txt ? idle=?
  plain-file-requires-emergency`), outside this wave's ownership.

## 3. `disk-guard.sh` — present, green, and it already sees this round's root

Present, not on `PATH`: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh` (plus
`disk-guard-selftest.sh`). It is a fleet-root file, read-only to this lane, executed only in its
non-mutating modes (`check`, `status`, `sweep --dry-run`), with `HYAKU_DISK_LOG` redirected into my
scratch so no fleet state file was touched.

```
$ bash scripts/hyaku/disk-guard.sh check
ok root=/tmp use=2% soft=70%
ok root=/var/tmp use=38% soft=70%
ok root=/fast/scratch/hyaku use=27% soft=70%
check_rc=0

$ bash scripts/hyaku/disk-guard.sh status      # full table in the run below; rc
root                             use%     free
/tmp                               2%   125.4G
/var/tmp                          38%   571.1G
/fast/scratch/hyaku               27%   594.2G
status_rc=0
```

`status` measured at T3 = `2026-10-26T01:50:5x`, i.e. the state the round's last seats are running in.
All three roots are below `SOFT_PCT=70` (`scripts/hyaku/hyaku.env`), so no seat of this round can claim
ENOSPC pressure.

Dry run, to show what the driver will reclaim and that this round's root is already targeted:

```
$ bash scripts/hyaku/disk-guard.sh sweep --dry-run --all
pressure /tmp use=2% soft=70% target=60%   → ok /tmp use=2% after sweep
pressure /var/tmp use=38% …                → ok /var/tmp use=38% after sweep
pressure /fast/scratch/hyaku use=27% …     → ok /fast/scratch/hyaku use=27% after sweep
# log lines for this root:
keep-young /fast/scratch/hyaku/kasegi-r33 ? idle=1 younger-than-min-age=10m
```

with the surrounding roots named by the same pass (`kaidoku-r36`, `kengaku-r37`, `souji-r30`, `tabi-r29`
— the fleet is running several lanes concurrently, which is why `/tmp` is shared and attribution needs
content evidence).

## 4. Committed-tool rule (§7.4): the round's new instrument honours TMPDIR and leaves nothing behind

The only new committed-and-executable artefact of this round is `corpus/instruments/capture-binding-check.py`
(untracked at measurement, `?? corpus/instruments/capture-binding-check.py`). Static: no `/tmp` literal
(`grep -n '/tmp' corpus/instruments/*.py` returns only pre-existing citation text in `density.py:6-7`,
`resolve.py:10,43`, and a test string in `recheck-audit.py:216`); scratch precedence in the file is
`--scratch` → `$HYAKU_SCRATCH` → `$TMPDIR` → platform default (`:367-377`).

Dynamic proof — `TMPDIR` pinned into my scratch, `HYAKU_SCRATCH` unset, so the fallback chain is exercised:

```
$ env -u HYAKU_SCRATCH TMPDIR=/fast/scratch/hyaku/kasegi-r33/ExecScratchDiscipline/tdir \
    python3 corpus/instruments/capture-binding-check.py --selftest
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=url-matching-two-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0
rc=0
$ ls -la /fast/scratch/hyaku/kasegi-r33/ExecScratchDiscipline/tdir
total 0
drwxr-xr-x 2 vgpnk vgpnk   6 Oct 26 01:49 .          # empty: fixture tree removed at exit
$ ls -d /tmp/capture-binding-selftest-* /fast/scratch/hyaku/capture-binding-selftest-*
none
```

So the round's gate obeys §7.4 in both directions (honours the caller's scratch root, removes its own
fixture tree). `ExecDeterminism` proves the same file's precedence positively for `TMPDIR=/tmp`
(`SPY mkdtemp dir='/tmp' path='/tmp/capture-binding-selftest-ca3wqtcy'` in its receipt), which is the
mirror-image evidence: the tool follows `TMPDIR`, it does not hardcode a root.

## 5. Defects and risks (ranked; none blocks C1/C2)

0. **S-0 (round-33, charged to one seat): `ExecWaveEvidencePack` ended with its tree on disk and its
   receipt says it did not.** 72 KiB / 9 files / 43,143 bytes, all nine hashes identical to the table it
   prints "before removal", receipt present since 01:51:28. §7.2 makes this its own defect; the claim
   line (receipt §6, lines 235-237) needs an appended erratum. Evidence in §1.
1. **S-1 (round-33, fixable next round): `/tmp` staging of seat messages.** 6 files, 2,038 bytes,
   01:18:26–01:18:28, relaying the C1 Rule-B erratum. Inside the 50 MB allowance, outside the scratch
   root, and non-citable by §7.5. Use `write agent://<id>` instead.
2. **S-2 (round-33): `/tmp/r33-prompts-dump.txt`** — 6,187 bytes of seat prompt text in `/tmp`
   (01:22:15), reaped without notice and outside the lane. Same fix: keep prompt dumps in the wave dir.
3. **S-3 (environment, systemic): `TMPDIR`/`HYAKU_SCRATCH` unset in seat env** while `hyaku.env`
   prescribes `TMPDIR=$HYAKU_SCRATCH/tmp`. Every tool that trusts an inherited `TMPDIR` leaks to `/tmp`;
   this is what produced the other lanes' entries too. Cheapest durable fix: export both in the
   dispatcher (`inline.sh` spawn env), not in each seat prompt.
4. **S-4 (orphan risk, not charged):** at the post-removal pass three seats still held trees with no
   receipt — `CritMistakes` (884 KiB, idle 31 min), `RevGateSpot` (52 KiB, idle 32 min), `SimplifierCleanup`
   (44 KiB, idle 21 min). If they die unyielding, §7.2 makes the trees their defect and the L1 purge at
   landing is the remedy. (`RevC1BeforeAfter`, 117,776 KiB at T5, and `ScribeLesson` settled clean.)
5. **S-5 (shape, not a breach):** `RevC1BeforeAfter/base` carries `.ufo/waves` (113,588 KiB) — a
   lane-history copy in scratch. §7.3 prefers citing the revision over carrying the tree.
6. **S-6 (item text):** the audit `find` this seat was given has the unparenthesised `-o` defect and
   reports `/tmp` itself; rewritten form in §2.

## 6. This seat's own scratch (self-report)

Created `mkdir -p /fast/scratch/hyaku/kasegi-r33/ExecScratchDiscipline`; held `audit.py`, four captures,
`dg/` (guard logs), `tdir/` (the probe's empty TMPDIR). Everything cited above is inline in this receipt,
then:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r33/ExecScratchDiscipline
$ date -Is; ls -d /fast/scratch/hyaku/kasegi-r33/*/
2026-10-26T01:54:21-03:00
/fast/scratch/hyaku/kasegi-r33/CritMistakes/
/fast/scratch/hyaku/kasegi-r33/ExecWaveEvidencePack/
/fast/scratch/hyaku/kasegi-r33/RevGateSpot/
/fast/scratch/hyaku/kasegi-r33/SimplifierCleanup/
$ ls -la /fast/scratch/hyaku/kasegi-r33/
drwxr-xr-x 15 vgpnk vgpnk 4096 Oct 26 01:23 CritMistakes
drwxr-xr-x  2 vgpnk vgpnk 4096 Oct 26 01:50 ExecWaveEvidencePack
drwxr-xr-x  2 vgpnk vgpnk   84 Oct 26 01:22 RevGateSpot
drwxr-xr-x  2 vgpnk vgpnk   39 Oct 26 01:33 SimplifierCleanup
$ ls -d /fast/scratch/hyaku/kasegi-r33/ExecScratchDiscipline
ls: cannot access '/fast/scratch/hyaku/kasegi-r33/ExecScratchDiscipline': No such file or directory
$ bash scripts/hyaku/disk-guard.sh check      # run from the fleet root after my removal
ok root=/tmp use=2% soft=70%
ok root=/var/tmp use=38% soft=70%
ok root=/fast/scratch/hyaku use=27% soft=70%
check_rc=0
```

`ExecScratchDiscipline/` is absent from those listings: no tree of mine is on disk at yield. The four
remaining entries belong to seats without receipts (§1, §5 S-4) plus the charged one (§5 S-0).

No `/tmp` file, no `/var/tmp` file, no tool install, no model flag passed, no git/jj mutation.

## 7. Limits, and how the ambiguous case resolved

Pass table (all four measurements, same instrument, same two arguments):

| pass | wall clock | receipts | seat dirs | note |
|---|---|---|---|---|
| T3 | 01:50:31 | 55/64 | 7 | verdict pass for §1 |
| T4 | 01:51:49 | 58/64 | 7 | `ExecWaveEvidencePack` receipt + tree + live PID 1839468 |
| T5 | 01:53:07 | 60/64 | 5 | `ExecWaveEvidencePack` receipt + tree, **no** live PID |
| T6 (post-removal) | 01:54:21 | 60/64 | 4 | mine gone; the charged tree still present |

- Unresolved at T3: the 6 dirs of §1 plus `ExecWaveEvidencePack`, `ScribeScorecard` and this seat. At filing
  the count is **60 of 64**; the 4 still open are `ScribeReportDraft`, `CritMistakes`, `RevGateSpot`,
  `SimplifierCleanup` (`python3 -` over `wave1-spec.json` items minus `wave1/*.md`).
- **Resolution of the one ambiguous case:** `ExecWaveEvidencePack` had a receipt and a tree with a live PID
  at T4 — a seat still finishing. By T5 the PID was gone and the tree remained, byte-identical to the
  pre-removal hashes in its own receipt, so it is a yielded-seat-with-tree: charged in §5 S-0, not excused
  as in-flight.
- Those four open seats can still create and remove trees or `/tmp` files after this audit. Post-landing
  re-check, one command (script in the appendix):
  `python3 audit.py /fast/scratch/hyaku/kasegi-r33 .ufo/waves/round-33/wave1` → expect `seat_dirs=0` once
  the L1 purges the round root.
- Liveness in the tables is `/proc`-based at that instant; absence of a live PID is not proof of death and
  I never infer seat failure from it. Presence of a live PID *is* treated as "in use", which is why T4 is
  reported separately instead of charged.
- Self-disclosure: this receipt was edited after it was first written (`01:52` → `01:55`), so the row
  `MISMATCH ExecScratchDiscipline.md table=8b968d565db2d920 now=ce087c1c7c0f074f` in
  `wave1/ExecWaveEvidencePack.md` §3 is expected — its census hashed the earlier draft. Cite the
  later state: this receipt was revised after the census (the §1 charged case and §6 output were
  added), so any in-file hash of it is superseded by construction — hash it at read time.

## Appendix — audit script (stdlib, read-only, scratch paths as arguments)

```python
#!/usr/bin/env python3
"""ExecScratchDiscipline audit: which seat scratch dirs still exist, sizes, liveness, receipts.

Read-only. Takes the scratch root and the wave1 report dir as arguments (no hardcoded /tmp).
"""
import json
import os
import subprocess
import sys
import time


def du_kb(path):
    try:
        out = subprocess.run(["du", "-xsk", "--", path], capture_output=True, text=True, timeout=120)
        return int(out.stdout.split()[0]) if out.stdout.strip() else -1
    except Exception:
        return -1


def newest_mtime(path):
    newest = 0.0
    for root, dirs, files in os.walk(path):
        for n in files + dirs:
            try:
                newest = max(newest, os.lstat(os.path.join(root, n)).st_mtime)
            except OSError:
                pass
    return newest


def count_files(path):
    n = 0
    for root, dirs, files in os.walk(path):
        n += len(files)
    return n


def live_pids(path):
    """PIDs whose cwd/exe/root/fd resolves under path."""
    hits = []
    real = os.path.realpath(path)
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        base = os.path.join("/proc", pid)
        cands = []
        for link in ("cwd", "exe", "root"):
            try:
                cands.append(os.readlink(os.path.join(base, link)))
            except OSError:
                pass
        try:
            fd_dir = os.path.join(base, "fd")
            for fd in os.listdir(fd_dir):
                try:
                    cands.append(os.readlink(os.path.join(fd_dir, fd)))
                except OSError:
                    pass
        except OSError:
            pass
        for c in cands:
            rc = os.path.realpath(c) if c.startswith("/") else c
            if rc == real or rc.startswith(real + os.sep):
                hits.append(int(pid))
                break
    return sorted(set(hits))


def main():
    scratch = sys.argv[1]
    reports = sys.argv[2]
    as_json = "--json" in sys.argv
    rows = []
    if os.path.isdir(scratch):
        for name in sorted(os.listdir(scratch)):
            p = os.path.join(scratch, name)
            if not os.path.isdir(p):
                continue
            rows.append(
                {
                    "seat": name,
                    "kb": du_kb(p),
                    "files": count_files(p),
                    "newest_mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(newest_mtime(p))),
                    "live_pids": live_pids(p),
                    "receipt": os.path.exists(os.path.join(reports, name + ".md")),
                }
            )
    receipts = sorted(f[:-3] for f in os.listdir(reports) if f.endswith(".md")) if os.path.isdir(reports) else []
    out = {"scratch_root": scratch, "exists": os.path.isdir(scratch), "seats": rows,
           "receipts": receipts, "receipt_count": len(receipts)}
    if as_json:
        print(json.dumps(out, indent=1))
        return
    print(f"scratch_root={scratch} exists={out['exists']} seat_dirs={len(rows)} receipts={len(receipts)}")
    for r in rows:
        print(
            f"{r['seat']:<24} kb={r['kb']:<8} files={r['files']:<6} newest={r['newest_mtime']} "
            f"live={','.join(map(str, r['live_pids'])) or '-'} receipt={'yes' if r['receipt'] else 'NO'}"
        )


if __name__ == "__main__":
    main()
```
