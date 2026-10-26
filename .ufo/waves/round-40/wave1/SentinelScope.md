# SentinelScope — round-40 wave-1 receipt

Role: sentinel (leaf, no dispatch). Milestone: write-scope verification feeding the L1 misroot sweep.
Axes touched: depth:verifiability (scope contract made checkable), coverage (adjacent spill inventory).
Snapshot: 2026-10-26T21:19Z; lane @ `5e985b74075dd3813a63d7750966bf8abf693465`, fleet @ `4bb33202687f02a84947811666a493164c82917d`.
Deliverable: `.ufo/waves/round-40/wave1/SentinelScope.txt`, 73 lines, sha256 `f828f0177bc7fb0500929de4f26ea80bc0a9125b3f07c9f978219f29d3bb6f14` (5768 bytes).

## 1. Contract read

`python3 -c "json.load(open('.ufo/waves/round-40/wave1-spec.json'))"` → keys `wave, reportDir, maxLanes, axes, milestone, context, items`;
`reportDir=.ufo/waves/round-40/wave1`, 54 wave-1 items. The `context` block carries the discipline verbatim:

- "Lane repo …/kasegi-shokunin is the ONLY lane repo. The fleet root …/shokunin is read-only … /home/vgpnk/Projects/shokuknow is read-only."
- "Your ONLY allowed writes are (1) your receipt … `<SEATNAME>.md`, (2) byte-exact deliverable files your item names … `<SEATNAME>.<suffix>` … (3) scratch under your scratch dir."
- "Create S=/fast/scratch/hyaku/kasegi-r40/<SEATNAME>/ … bind ALL scratch/work copies there (TMPDIR=$S) … Remove your scratch dir before you yield … A seat whose scratch dir survives is a round-40 defect (H6 checks it live)."
- "Never run a mutating git/jj command anywhere"; "Never edit MANIFEST.json, templates/, scripts/ (fleet), .ufo/state/, .ufo/watchdog.log, .scratch/".
- "Do not run a heavy pass while the disk guard is not green."

Item text confirmed identical to the handoff (the byte match was checked by eye against `items[?name==SentinelScope].prompt`).

## 2. Own scratch discipline

```
$ S=/fast/scratch/hyaku/kasegi-r40/SentinelScope; export TMPDIR=$S; cd "$S"; t=$(mktemp -d)
mktemp resolves under scratch: /fast/scratch/hyaku/kasegi-r40/SentinelScope/tmp.AnRD666F2A
TMPDIR_BIND=ok
$ ls -A "$S" | wc -l
0
```
Inherited `TMPDIR` was empty (`echo "TMPDIR=$TMPDIR"` → `TMPDIR=`), so the binding was proved, not assumed. No work copies were needed:
every check below is a read of the lane/fleet/scratch trees.

Cleanup (executed before this receipt, since the receipt must be written last):
```
$ rm -rf -- "$S"; ls -d "$S"
ls: cannot access '/fast/scratch/hyaku/kasegi-r40/SentinelScope': No such file or directory
own_dir_present=no
```

## 3. Lane repo check

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
5e985b74075dd3813a63d7750966bf8abf693465
$ git -C …/kasegi-shokunin status --porcelain | wc -l
15
$ git -C …/kasegi-shokunin status --porcelain          # all entries
?? .ufo/waves/round-40/build-wave1-spec.py
?? .ufo/waves/round-40/build-wave2-spec.py
?? .ufo/waves/round-40/kasegi-r40-build.ready
?? .ufo/waves/round-40/kasegi-r40-build.ready.partial
?? .ufo/waves/round-40/wave1-dispatch.json
?? .ufo/waves/round-40/wave1-plan.err
?? .ufo/waves/round-40/wave1-plan.out
?? .ufo/waves/round-40/wave1-run.err
?? .ufo/waves/round-40/wave1-spec.json
?? .ufo/waves/round-40/wave1/
?? .ufo/waves/round-40/wave2-dispatch.json
?? .ufo/waves/round-40/wave2-plan.err
?? .ufo/waves/round-40/wave2-plan.out
?? .ufo/waves/round-40/wave2-run.err
?? .ufo/waves/round-40/wave2-spec.json
$ LANE_NONROUND40_UNTRACKED=0   # sed 's/^?? //' | grep -vc '^\.ufo/waves/round-40/'
$ git -C …/kasegi-shokunin diff --stat HEAD | wc -l
0
$ git cat-file -t a7af2ce… && git cat-file -t 5e985b7… && git merge-base --is-ancestor a7af2ce… 5e985b7… && echo ok
commit
commit
base-is-ancestor-of-freeze=yes
$ git log --oneline -3 --no-decorate
5e985b7 round-40: freeze claims C1/C2 + control receipts
a7af2ce round-39 verifier spot-check (integrator, hyaku): non-author admit/reject
8371e7a round-39: record final-head closure results
```
Zero `M`/`D`/`R` entries at any point: no wave seat edited a tracked lane file. `kasegi-r40-build.ready.dispatched` appeared and the
`.partial` marker churned during the window — orchestrator dispatch markers, not seat writes.

Wave-1 directory conformance (`python3` walk of `wave1/` against both specs):
```
wave1_entries=59 prefix_seats=26 nonconforming=1   # at 18:19Z
nonconforming: ['ExecMistakesDraft.h5-replica.sh']
wave1 dirs: []                                      # no subdirectories
$ find wave1 -mindepth 1 \( -not -user vgpnk -o -perm -4000 -o -perm -0002 \) -printf '%M %u %p\n'
(none)
$ find wave1 -mindepth 1 -type f -printf '%M\n' | sort | uniq -c
     45 -rw-r--r--      (plus 2 -rwxr-xr-x for the .sh)
```
At the final read the dir held 68 entries over 30 declared seat prefixes and 25 receipts. `ExecMistakesDraft.h5-replica.sh` is the
proof transcript its item asks for ("the proof transcript"), so it is in scope; the only extras beyond a literal filename are
`ExecH9DeclaredBlocks.{examples-declared,province,readme}.txt` and `ExecMistakesDraft.fixture-future-dated.txt`, each backed by
"also deliver one working example block …" / "the proof transcript" in their prompts. Reported, not a defect.

Writes outside the wave dir after 18:05 (find, excluding `.git`): only `.jj/repo/*`, `.jj/working_copy/*` (working-copy snapshot
18:10:32–18:10:34) and `.git` index bookkeeping from read-only `git status`. No lane `.ufo/state`, no lane `.scratch`
(`ls .ufo/state .scratch` → both "No such file or directory").

## 4. Fleet root check

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
?? .ufo/reports/round-42/kengaku.md
$ stat -c '%y %s' .ufo/reports/round-42/kengaku.md
2026-10-26 18:06:25 -0300  13949
$ grep -c -i 'kasegi' .ufo/reports/round-42/kengaku.md ; grep -c 'round-40' …
0
4
$ git -C /home/vgpnk/Projects/shokunin diff --stat HEAD | wc -l
0
$ git hash-object MANIFEST.json ; git rev-parse HEAD:MANIFEST.json
0e598dd91bf60aa089f0fcb2d745e43bc1cbe73f
0e598dd91bf60aa089f0fcb2d745e43bc1cbe73f
```
The single untracked file predates the wave (18:06:25 < 18:10:05), is the kengaku lane's round-42 report, and never says "kasegi";
its four `round-40` hits are kengaku's own battery40 (`grep -n round-40` → lines 15, 36, 122, 138). Not round-40 authored.
`MANIFEST.json` mtime 18:05:03 is pre-wave and its blob is byte-identical to HEAD.

Writes inside the wave window at fleet level (`find` maxdepth 4, lane repos and `.git`/`.jj` pruned):
```
2026-10-26 18:17:11 ./.ufo/state/disk-guard.log
2026-10-26 18:17:18 ./.ufo/state/inline-dispatcher.log
```
Harness-owned; dispatcher tail reads `… cap-defer /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-40/kasegi-r40-build.ready occupied 87`.
`find scripts templates -newermt '2026-10-26 18:05'` → empty.

## 5. Scratch-root check

```
$ find /fast/scratch/hyaku/kasegi-r40 -mindepth 1 -maxdepth 1 -type f | wc -l
0
$ ls -1 /fast/scratch/hyaku/kasegi-r40
ConnSibling CritClaimsContradiction ExecAssimilation ExecAuditRun ExecBindingCheck ExecConsiderthese
ExecH10NoHarmBase ExecH2Corrections ExecH3Criterion ExecH4GateRows ExecH6ScratchFixtures ExecH7Determinism
ExecH9DeclaredBlocks ExecHarnessUpdate ExecJunkRecheck ExecMistakesDraft ExecRecheckAll ExecSuiteBuild
ExecSuiteSelftestRun ScoutF23Lead ScoutS016Chk … ScoutS060Leads ScribeEntriesG1 ScribeEntriesG2 ScribeF23
ScribeGateBlocks ScribeNewRows ScribeRows SentinelScope      (36 at 21:19Z)
```
Cross-check against both specs: `undeclared scratch dirs: []`, i.e. every directory is a declared wave-1 or wave-2 seat. (The complement,
"declared seats with no scratch dir", is the normal finished/not-yet-started set and is not a finding.) Empty dirs at snapshot:
`MutKillList ReviewerC1Design ReviewerC2Baseline ScribeGateBlocks ScribeNewRows`; `MutBaseline/r39-export` looks old-mtimed only
because `git archive` stamps extraction times. After my cleanup the root held 27 dirs and `own_dir_present=no`.

Stray scan:
```
$ find /fast/scratch -maxdepth 3 -name 'kasegi-r39*' -o -maxdepth 3 -name 'kasegi-r40*'
/fast/scratch/hyaku/kasegi-r40
/fast/scratch/hyaku/kasegi-r40-l1
```
No `kasegi-r39*` anywhere — the round-39 leftover the C1 before-control promises removed is in fact gone. `kasegi-r40-l1`
is the only `kasegi-r40*` sibling: 1 file `integration-plan.md` (18:16, 1656 B, vgpnk:vgpnk 755, owner-writable only).
It matches the pattern H6 grades and the C1 kill rule's "leftover kasegi-r39*/r40 scratch entry at filing" — flagged for removal
before filing (I did not delete it; not my write scope). Pre-existing strays at the hyaku root, all older than round 40:
`base-census.sh` (04:14), `line137.txt` (15:20), `_d.txt` (16:25).

## 6. Cross-lane and shokuknow

```
$ for r in */; do git -C "$r" status --porcelain | grep -icE 'kasegi|round-40'; done   (21 lane repos)
kasegi-shokunin kasegi_round40_hits=15   # its own wave artifacts
… every other lane: 0
$ find /home/vgpnk/Projects/shokuknow -path '*/.git' -prune -o -newermt '2026-10-26 18:00' -print
(empty)
```
Sibling-lane writes seen during the window (tameshi SKILL/SOURCES/README 18:11–18:12, kaidoku PROVINCE/SOURCES 18:12) carry no
kasegi reference (`grep -c -i kasegi` = 0 on the two largest) and belong to those lanes' own live waves (`tameshi-r48/-r49`,
`kaidoku-r41` scratch roots present).

## 7. Disk guard

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
/tmp 3% 125.2G · /var/tmp 35% 585.2G · /fast/scratch/hyaku 26% 601.7G     (21:18:23Z, "ok" lines in disk-guard.log)
```

## 8. Verdict and residual items

No round-40 seat violated the write-scope contract at snapshot: no tracked-file edits in lane or fleet, no lane writes outside
`.ufo/waves/round-40/`, no round-40 content in fleet root / sibling lanes / shokuknow, no stray scratch dirs beyond declared seats.
Open filing-time conditions handed to the L1: (a) remove `/fast/scratch/hyaku/kasegi-r40-l1` (sibling scratch entry), (b) every
`/fast/scratch/hyaku/kasegi-r40/<SEAT>/` must be gone at filing except the passed `--work` dir, (c) `.ufo/reports/round-42/kengaku.md`
is another lane's, do not re-attribute it. Nothing was deleted by this seat.

## 9. Tooling

No installs, no upgrades, no pacman, no network fetches — all evidence is local reads. Tools used: coreutils `find/stat/sha256sum/wc`,
`git` (read-only), `python3` (json + directory walk), `bash disk-guard.sh status`.
