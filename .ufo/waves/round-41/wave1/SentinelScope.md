# SentinelScope — round 41, wave 1 (receipt-only: scope watch)

Seat `SentinelScope` (leaf; no subagents). Item: scope watch for the whole wave — re-list
`.ufo/waves/round-41/wave1/` every ~10 minutes and verify every new file is a
`<SEATNAME>.md` receipt or a `<SEATNAME>.<suffix>` deliverable for one of the 60 dispatched
seats (`.ufo/waves/round-41/wave1-dispatch.json` → `registry.members`), record every edit to
an existing file with mtime + sha256, and at wave end verify that no lane file outside
`.ufo/waves/round-41/` was touched, that the fleet root and shokuknow were not written, and
report any violation prominently.

Watch window: **2026-10-27T08:24:00Z → 09:29:30Z** (UTC; lane local time is UTC-3, so
05:24→06:29 local). Samples at 08:24:20Z, 08:35:37Z, 08:44:48Z, 08:51:34Z, 08:54:06Z,
09:00:55Z, 09:10:03Z, 09:19:19Z, 09:27:41Z, plus the close checks at 09:28:48Z/09:29Z.

Writes made by this seat: **this receipt only**, plus scratch
`S=/fast/scratch/hyaku/kasegi-r41/SentinelScope` (removed at yield). No deliverable (item is
receipt-only). No lane, fleet-root, shokuknow, PATH-directory, sibling-lane or source-tree
write. No git/jj mutation (read-only `git rev-parse`, `status`, `log`, `diff`, `show`,
`hash-object`, `ls-files`, `check-ignore`). No tool installed. No network fetch. Disk guard
green at open (`/fast/scratch/hyaku` 25 % use, 608.9 G free) and at close (26 % use, 596.2 G
free — the 10 G drop is other lanes' work plus 78 MB of surviving wave-1 scratch, §3).

## 0 Verdict

**One HIGH-severity cross-seat destructive event, one LOW self-remediated PATH-directory
write, one I6-class surviving scratch, one LOW freeze-timestamp inconsistency. Zero
out-of-scope lane writes, zero stray deliverable names, zero cross-seat overwrites, zero
misleading hash pins, zero fleet-root or shokuknow writes.**

| id | severity | subject | state |
|---|---|---|---|
| V1 | **HIGH** | `ExecI8Forge` removed the shared round-41 scratch parent | confirmed, self-reported + corroborated |
| V2 | LOW | `ExecI4Fence` transiently wrote `~/.local/bin/cmark` | confirmed, self-remediated, verified absent |
| V3 | MEDIUM | `MutC2Counters` scratch (78 MB) survives its receipt | observed at close, I6-class |
| V4 | LOW | `claims.json` `frozen_at_utc` is ~41 min later than its own write | confirmed by file mtime + commit time |

Everything else conformed; §5–§8 carry the positive evidence.

## 1 V1 — HIGH — seat `ExecI8Forge` deleted the shared scratch parent (cross-seat data loss)

**What happened.** After landing its deliverables, `ExecI8Forge` ran its cleanup as two
commands: `rm -rf -- "$S"` (its own seat dir) **and then** `rm -rf -- /fast/scratch/hyaku/kasegi-r41`
— the parent that all 60 seats share. Every live sibling's in-flight scratch was destroyed.

**Evidence (three independent sources).**

1. Peer message received from `ExecI8Forge` (verbatim): *"at ~05:46 my scratch cleanup
   over-removed — I ran `rm -rf /fast/scratch/hyaku/kasegi-r41` (the shared round-41 scratch
   PARENT) instead of only my own seat dir `/fast/scratch/hyaku/kasegi-r41/ExecI8Forge`. Any
   of your scratch staged under that parent at that moment was deleted."*
2. Its own in-wave receipt `wave1/ExecI8Forge.md` §Incident, lines 160-174:
   *"I removed my scratch with `rm -rf -- "$S"` **and then also**
   `rm -rf -- /fast/scratch/hyaku/kasegi-r41` — the shared round-41 scratch **parent**, not
   just my own seat directory. That deleted every sibling seat's scratch tree that existed at
   ~05:46"*; its transcript (`history://ExecI8Forge`) carries the same admission.
3. Direct observation by this seat: at 08:50Z
   `ls: cannot access '/fast/scratch/hyaku/kasegi-r41/SentinelScope': No such file or directory`
   while the parent held 7 seat dirs with ctimes 05:46-05:50 local; my reconstructed
   baselines/watch log are labelled as reconstructed for exactly this reason.

**Exploit path.** The cleanup literal is a hard-coded parent path, executed by any seat with
write access to the shared parent; nothing in the guard asserts that the deletion target is
the seat's own directory. One seat's typo destroys the whole wave's scratch state. The blast
radius is every concurrent seat, in every wave that shares a parent.

**Impact.** In-flight scratch of all live wave-1 seats destroyed at ~08:46Z (this seat's
watch log, baselines and snapshot history among the losses — see §9 for what was
reconstructed). Sibling seats rebuilt within 1-3 minutes (dir ctimes 05:47-05:50 local) and
**no deliverable bytes were lost**: every seat artifact lives in the lane tree, and my
filesystem sweep shows 0 lane writes outside `.ufo/waves/round-41/` all window (§4). The
residual risk is a seat whose only copy of non-deterministic evidence was in scratch — it
would have silently lost it and could have reported unreproducible results.

**Smallest remediation.** (a) Seat cleanup must be a single guarded delete of its own dir
only: `rm -rf -- "${S:?}"` with a structural assertion before it, e.g.
`[ "$(dirname "$S")" = /fast/scratch/hyaku/kasegi-r41 ] && [ "$(basename "$S")" = "$SEAT" ] || exit 9`.
(b) Never template the shared parent into a cleanup line; the parent is harness-owned. (c) The
harness should reap seat scratch after the wave (and can then verify a vanished dir rather
than trusting self-reports).

## 2 V2 — LOW — seat `ExecI4Fence` transiently wrote into `~/.local/bin` (PATH directory)

**Evidence.** Its receipt `wave1/ExecI4Fence.md` (lines 357-364): *"I first ran
`uv tool install commonmark`, which wrote a `cmark` symlink into `~/.local/bin` — a PATH
directory the seat host guard forbids writing to — so I removed it with
`uv tool uninstall commonmark` immediately afterwards."* Its own network fetch is logged at
`utc_fetch=2026-10-27T08:26:45Z`.

Corroborated and independently verified remediated by this seat:

```
$ stat -c '%y %n' /home/vgpnk/.local/bin
2026-10-27 05:26:51.392366006 -0300 /home/vgpnk/.local/bin      # ≡ 08:26:51Z: entry add+remove
$ find /home/vgpnk/.local/bin -maxdepth 1 -newerct '2026-10-27 05:05:00'
/home/vgpnk/.local/bin                                          # directory only, no entry survives
$ ls -la /home/vgpnk/.local/bin/cmark
ls: cannot access '/home/vgpnk/.local/bin/cmark': No such file or directory
$ ls -d /home/vgpnk/.local/share/uv/tools/commonmark
ls: cannot access ...: No such file or directory
```

**Impact.** None surviving: a ~6 s window, no `cmark` left behind, 100 entries before and
after, and the seat re-ran its deliverable with `uv run --with commonmark` (ephemeral), which
is the correct channel. The guard text (seat host guard: "use `uv tool install` … Never write
to any PATH directory") is internally contradictory; this seat resolved it the right way after
the fact. Remediation: state the rule as "`uv run --with` / `npx` / `uvx` only — a PATH
directory is never a valid install target" so seats do not have to discover the contradiction
mid-task.

## 3 V3 — MEDIUM — I6-class: `MutC2Counters` scratch survives its own receipt

The spec: *"A seat whose scratch dir survives is an I6-class round-41 defect."*

```
$ ls -l wave1/MutC2Counters.md
-rw-r--r-- 1 vgpnk vgpnk 9019 Oct 27 06:08 MutC2Counters.md          # receipt written 09:08Z
$ du -sh /fast/scratch/hyaku/kasegi-r41/MutC2Counters
78M
$ find .../MutC2Counters -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' | sort | tail -1
2026-10-27 06:07 .../m9-twin-notrio/corpus/knowledge/rfc-9116-security-txt.md
$ ls -1 /fast/scratch/hyaku/kasegi-r41        # at 09:29Z, 21 min after the receipt
MutC2Counters
SentinelScope
```

Observed at 09:27:41Z and again at 09:29:07Z: 78 MB of fixtures (green base, m1-m10 mutation
twins) still present 19-21 minutes after the seat published its receipt, with no file newer
than 09:07Z. If the seat is still live it is merely late; if it has yielded, it is an I6-class
defect (scratch survived). The seat also had its scratch deleted by V1 at ~08:46Z and rebuilt
the fixture tree at 05:47-05:54 local, so the surviving tree is post-wipe work. Remediation:
the harness reaps `$S` after each seat (V1 remediation (c)) and the seat reports the reap in
its receipt.

## 4 V4 — LOW — the frozen claim stamp post-dates its own file by ~41 minutes

```
$ date -u                     # observation instant
2026-10-27T08:31:57Z
$ stat -c '%y' .ufo/waves/round-41/claims.json
2026-10-27 05:23:14.591783514 -0300     # ≡ 08:23:14Z
$ git show -s --format='%cI' 96dbd5f    # the errata commit that last wrote claims.json
2026-10-27T05:26:15-03:00               # ≡ 08:26:15Z
$ grep -n frozen_at_utc claims.json
6:  "frozen_at_utc": "2026-10-27T09:05:00Z",
70: "frozen_at_utc": "2026-10-27T09:05:00Z",
76: "frozen_at_utc": "2026-10-27T09:05:00Z",
```

`frozen_at_utc` (09:05:00Z) is 41 min **after** the file's write instant and 39 min after the
commit that produced it, and was still 33 min in the future when sampled. The stamp is a
nominal value, not the freeze instant; any seat that validates "frozen before data" against
it validates nothing. Impact is provenance-only (no claim value is affected: the base-hash and
I11 errata themselves check out — `5b29ea14…f0f0bf98…` resolves as a commit, and
`.ufo/waves/round-40/wave2/CritKillRule.md` carries `### F` headings F1-F8). Smallest
remediation: emit `frozen_at_utc` from `date -u` at write time, or rename the field to a
nominal round-open stamp.

## 5 Wave-directory conformance (all 113 files, checked three ways)

Final listing 09:28:48Z (before this receipt): **113 entries**, all regular files (`find -type l` / `-type d` /
non-regular: empty), owner `vgpnk:vgpnk`, 111 seat-stem files + 2 L1 artifacts.

```
== full name conformance:
 files= 113 exempt= ['CORRECTIONS-L1.md', 'swarm-registry.json'] nonconforming= []
```

Breakdown: 59 peer receipts `<seat>.md` + 3 other `.md` (`CORRECTIONS-L1.md`,
`ScribeC2Entry.entry.md`, `ScribeLesson.lesson.md`) + 51 non-md (50 seat deliverables +
`swarm-registry.json`). Every seat stem is a dispatched seat name.

Exemptions, both L1-owned and named as such:

- `swarm-registry.json` — dispatcher registry (`registry.path` of `wave1-dispatch.json`),
  mtime 05:16, before any seat deliverable.
- `CORRECTIONS-L1.md` — added by the L1 commit `96dbd5f` ("round-41: freeze errata …"), the
  only wave1 file the L1 committed: `git show --name-status 96dbd5f` → `A
  .ufo/waves/round-41/wave1/CORRECTIONS-L1.md` (plus claims/spec/control edits). Its content
  is an L1 instruction note, not a seat receipt.

## 6 Edits to pre-existing files (self-rewrites only, no cross-seat overwrite)

Rewrites of files that already existed at baseline; every one keeps its owning seat's stem —
no seat wrote another seat's name. Baseline hash → final hash (size at close):

| file | baseline (sha256, or first-seen size) | final sha256 | final bytes |
|---|---|---|---|
| `ScoutLeads.txt` | `e70d977a04d6020bbaf2593feadfec7d0e3eb617b387301f09584cd685ef2cc5` | `2d910590197e24566fd6f20d0ffde44e941c2695c969919f63f341091394d31b` | 4174 |
| `ScribeScorecard.md` | `bb4e531c7f18d1d2e2665815182fdbe2877fc6fbf65c1c726b913126f0bfdd5c` | `17ddd03964e14deb390ccecd72bd431045b8ad017d0ccc48479d019bf8c48863` | 12820 |
| `ScribeScorecard.round41-table.txt` | `8693ff241c47d2041303907b6756838fcd3bf94d4cd67a3154882c29d4c2d4a8` | `ff1d63e33e39f082677c7fdb7261ddc02c294d10d5f6976af62032d383b130d8` | 4365 |
| `ScribeShonenLog.md` | `9a10771c2799cf595509626cfc5910fb91dc3f93eb02ae55cb0010be6fe6a406` | `1014e2747453ec608ea5100186f2f3d5693ffdd9fe292d6f4fe1d21a30ac9a26` | 15358 |
| `ScribeShonenLog.shonen-append.txt` | `88e0fd399948c37d55a49222d4b8779a7594c007029d12fe98cf02c6c8274052` | `82437c2473f08b90498a0d2033c39c45cc2551c366de025bc6ce4345e7606b29` | 4758 |
| `ScribeCorrections.md` | `31b63641d4e2ec767269026fbdfbcf13d1105e66a235121e3b37a4db040d6e6e` | `37228a77400f36ca055f607504e1f2381ce5912e94ebfa4c4ed07b5d052b8d4e` | 22145 (19533→22145) |
| `ScribeCorrections.full-blocks.txt` | `44a3bc8072870dee14a56ebab261459a0e154a515a32435a88d67754152b4838` | `ee3ffa7630f85235eea52087d5683032b4f04218a0d3ce5ce6fe0d25b2ec6e82` | 5009 (4949→5009) |
| `ExecI8Forge.md` | `first seen 11233 B (no baseline hash)` | `d0d00306ce5484741e4eda7e9f7904d4bb01dad69617b065020baac36783b680` | 13358 (incident section appended) |
| `ExecI6Scan.sh` | `first seen 17423 B (no baseline hash)` | `e9341dcac5781e0ee41e004a53ab0c02f84f62932714222f7235abfca5bb2e25` | 20242 |
| `LabH6Probe.md` | `first seen 14547 B (no baseline hash)` | `490fc13920e315f1bcee177314589cb79b2b59732783e3d174269ebd6c01c77e` | 14874 |
| `ExecControls.junk-s063.txt` | `first seen 58080 B (no baseline hash)` | `63a522608a1f0de9884d1a2dce32465fdceb79fb757a7d1ec7b6c67e68360656` | 61647 |

The four `first seen` rows are files created after the baseline sample and then revised
in-place before my next size sample, so no pre-edit hash exists for them; their final bytes are
pinned above. All are mid-flight revisions published before any landing (`lane HEAD` stayed `96dbd5f`
throughout; the L1 has not yet committed seat files), so none can be a post-landing tamper.

## 7 Provenance cross-check — every receipt hash pin against the actual bytes

For each receipt, every 64-hex token in a context naming that seat's own wave1 file was
compared with that file's sha256:

```
pins-verified-ok= 60
mismatches= 4
```

All four "mismatches" are sub-extract pipeline digests, redistributed byte-exactly — e.g.
`tail -1 ExecI7Registry.skill-fix.txt | sha256sum` → `20402c77…` (whole file is
`37d2b49d…`, 4 lines) and `grep '^Correction (round 41):' ScribeCorrections.full-blocks.txt |
sha256sum` → `782d5a5a…` (whole file `ee3ffa76…`). Re-verified:

```
$ tail -1 ExecI7Registry.skill-fix.txt | sha256sum → 20402c77e39edc8b337852ff69e83ca39b19b5b6da7f5484522afb978e503164
$ sed -n '2,3p' ExecI7Registry.skill-fix.txt | sha256sum → ac5cee380f96e9ab3ffdeb97d3388f6933b07bc97c747e5bcfe5571ae33f2c75
$ grep '^Correction (round 41):' ScribeCorrections.full-blocks.txt | sha256sum → 782d5a5aaaba40ae978d0071a6dbe8f872514533eda5f0efcb7ae2bac87b5434
```

**No stale or fabricated pin was found.** Two trivia worth the L1's eye: two seats delivered
byte-identical fix blocks under different names (`ExecI7Registry.skill-fix.txt` ≡
`RevD4D5D6.skill-table-fix.txt`, both `37d2b49d…`, disclosed by
`ExecI7Registry.md`), and `RevD4D5D6.shonen-tally-fix.txt` is a deliberate 0-byte file
(`e3b0c442…`, disclosed as such in its receipt).

## 8 Close-time scope verification (commands and actual output)

```
== close_utc=2026-10-27T09:28:48Z
== wave1 files=113
== symlinks/dirs/nonregular in wave1:                      (empty)
== lane status -uall, paths outside .ufo/waves/round-41/:  count=0
== lane FS writes outside round-41 (newer than 05:05):     count=0
== round-41 tree, top level:
d c1-controls   d c2-controls   d wave1
f census-before.txt  f claims.json  f wave1-dispatch.json  f wave1-spec.json
f wave1-run.err  f build-wave1-spec.py  f build-wave2-spec.py
f kasegi-r41-build.ready  f kasegi-r41-build.ready.dispatched
== fleet status: ?? .ufo/reports/round-61/kake.md
== shokuknow status hash: e9636d64793a417d739e32e3f543b88fd2f4467b46fb5e2a6770b9fc22234ff2
== shokuknow in-window writes: 0
== PATH dirs: /usr/bin newer=0  local-bin-entries-ctime-new=0  cmark=absent
== scratch dirs: MutC2Counters SentinelScope
== lane HEAD: 96dbd5f4276fcf8f93552fb97554485904cc0488
== lane commits since 96dbd5f:                              (none)
```

Interpretation:

- **Lane:** every changed/untracked path is under `.ufo/waves/round-41/` (git `-uall`, so the
  check is file-level, not directory-level); the independent filesystem sweep for lane writes
  newer than 05:05 outside `.git`/`.jj`/`round-41` returns **0**. The frozen control files are
  byte-identical to their committed blobs (`claims.json 901aa617…`, `c1-controls/do-nothing.txt
  60c7b2d8…`, `c2-controls/before.txt 456f9c3b…`, `census-before.txt 3bf68c98…`), so no seat
  edited the freeze.
- **Fleet root:** the only tracked-file state is an untracked file — `.ufo/reports/round-61/kake.md`
  (kake lane's own round-61 report, `grep -icE 'kasegi|round-41|r41'` = 0; kake-shokunin HEAD
  `eaa9177` "round-61: contract …"). The other in-window fleet-root churn is other lanes'
  reports/prompts and `.ufo/state/*` harness logs (the disk-guard log includes my own
  `status` invocation). Fleet `MANIFEST.json` was touched at 08:52:27Z but is **byte-identical
  to `HEAD`** (`git hash-object` = `git rev-parse HEAD:MANIFEST.json` = `c1e4055f…`, `git
  status` clean), i.e. a no-op working-copy refresh, not a content write. Zero kasegi-seat
  fleet-root writes.
- **shokuknow:** status hash identical to the 08:24Z baseline and **0 files** with mtime in
  the window; the 1918-entry dirty set is pre-existing drift (newest mtime 2026-10-25 13:34).
- **PATH directories:** no entry created anywhere (`/usr/bin` 0 newer; `~/.local/bin` has no
  entry with ctime in the window) and V2's `cmark` is gone.
- **Lane commits:** HEAD moved once in the window — `b3b08b27` (baseline, 05:17 local) →
  the L1's own errata commit `96dbd5f` at 08:26:15Z (author and committer both `kasegi-shokunin <kasegi@shokunin.local>`,
  `2026-10-27T05:26:15-03:00`, files: `build-wave1-spec.py`, `build-wave2-spec.py`,
  `c1-controls/do-nothing.txt`, `claims.json`, `CORRECTIONS-L1.md`). No seat-authored commit
  exists in the lane. The `c1-controls/do-nothing.txt` change is an **append only** (erratum
  paragraph after the recorded `exit=127` verdict, verdict text unchanged), i.e. the control's
  observation was not rewritten.

## 9 Limits

- Sampling is interval-based (~10 min) plus one 60 s sampler; two file generations between
  samples of the same file would be seen as one edit. Edit rows above are the ones visible at
  my samples.
- V1 destroyed my scratch at ~08:46Z. Baselines, the watch log and snapshots before that
  instant are **reconstructed from this session's tool transcripts** (baseline listing hashes,
  the 08:35:37Z and 08:44:48Z file counts 67/91, and the shokuknow/fleet baselines are exact;
  the per-file membership of those two intermediate listings was displayed truncated
  in-session and is therefore not fully enumerable). Reconstruction is labelled at the top of
  this receipt and in `WIPE-INCIDENT.md` (scratch, removed at yield).
- The seats' own claims (I1-I12, F24/S063) are out of this seat's scope; I checked only
  scope, provenance shape and hash consistency, not suite semantics.
- `MutC2Counters` may still be live at close; V3 is recorded as observed, not as a verdict on
  the seat.

## 10 Reproduction

```
S=/fast/scratch/hyaku/kasegi-r41/SentinelScope   # recreated by hand after V1
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain -uall \
  | grep -vE '^.. \.ufo/waves/round-41/'                       # → no output
find /home/vgpnk/Projects/shokunin/kasegi-shokunin -xdev \
  -newermt '2026-10-27 05:05:00' -type f -not -path '*/.git/*' \
  -not -path '*/.jj/*' -not -path '*/.ufo/waves/round-41/*'    # → no output
git -C /home/vgpnk/Projects/shokunin status --porcelain         # → ?? .ufo/reports/round-61/kake.md
git -C /home/vgpnk/Projects/shokuknow status --porcelain | sha256sum
  # → e9636d64793a417d739e32e3f543b88fd2f4467b46fb5e2a6770b9fc22234ff2
find /home/vgpnk/.local/bin -maxdepth 1 -newerct '2026-10-27 05:05:00' -mindepth 1  # → none
ls /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-41/wave1 | wc -l   # → 114 with this receipt
```
