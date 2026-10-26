# CritC1Export — round 38: export-mode integrity of the planned r38 suite

Receipt-only item. Deliverable: none (no landable bytes; every guard below is for
`corpus/instruments/r38-closure.sh`, whose owner is ExecSuiteBuild).

Lane refs read: base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, r37 judged head
`2387dcf6ccfefcfb703783387b9aade8fc82abfa`, lane tip at read `7001535`. Tool versions
present: `git 2.56.0`, `GNU tar 1.35`, `bash 5.3.x`, `coreutils 9.x`; nothing installed,
no `pacman`, no network fetch. Scratch `/fast/scratch/hyaku/kasegi-r38/CritC1Export/`,
removed after this receipt was written.

Method: the shared design is `corpus/instruments/r37-closure.sh` (export mode only; plain
run refused). I attacked the four surfaces the item names by running the r37 instrument
against live and historical refs (`--export-ref`, read-only `git archive`/`ls-tree`/
`check-attr`/`status`), and by executing fixture repositories
(`D=$(mktemp -d -p "$S") && git -C "$D" init -q`, toplevel asserted `== $D`) that reproduce
each export divergence in isolation. Six exploit rows, each with what I ran and what it
printed. Where a sibling receipt already named the shape, I say so and only add the
measured mechanism.

---

## 1. E1 — symlinks inside the export read live lane bytes (export-only is false)

**Exploit sketch.** `git archive` stores mode `120000` entries as symlinks and
`tar -xf` restores them verbatim. A tracked symlink may carry an absolute path into the
lane. Every `[ -f … ]` test and every `cat`/`grep` under the export root then follows it,
so an "export-only" check can read bytes that are not in the exported ref — including a
file that only exists at a *later* commit. Fixture, executed:

```text
$ git init -q . (fixture) ; ln -s "$D/live/instruments" tree/instruments ; git commit
$ git -C "$D" archive --format=tar HEAD | tar -xf - -C "$D/dest"
$ ls "$D/dest/tree/instruments"                      -> gate.sh
$ echo v2-NOT-IN-THE-REF > live/instruments/gate.sh
$ echo NEWFILE-AT-HEAD-ONLY > live/instruments/r38-closure.sh
$ ls "$D/dest/tree/instruments"                      -> gate.sh  r38-closure.sh
$ cat "$D/dest/tree/instruments/gate.sh"             -> v2-NOT-IN-THE-REF
$ test -f "$D/dest/tree/instruments/r38-closure.sh"  -> YES-VISIBLE-IN-EXPORT
```

The lane tree already carries this shape: `58` tracked symlinks at `2387dcf6`, of which
`6` escape the export root (measured with `realpath -m` over `find . -type l`):

```text
./.ufo/waves/round-25/assimilation/rows/validate/corpus/knowledge -> /home/vgpnk/…/kasegi-shokunin/corpus/knowledge
./.ufo/waves/round-28/assimilation/schema2/corpus/knowledge       -> /home/vgpnk/…/kasegi-shokunin/corpus/knowledge
./.ufo/waves/round-28/assimilation/schema3/corpus/knowledge       -> /home/vgpnk/…/kasegi-shokunin/corpus/knowledge
./.ufo/waves/round-28/assimilation/schema4/corpus/knowledge       -> /home/vgpnk/…/kasegi-shokunin/corpus/knowledge
./.ufo/waves/round-29/wave1/CritC2Kill-scratch/corpus/instruments -> /home/vgpnk/…/kasegi-shokunin/corpus/instruments
./.ufo/waves/round-29/wave1/CritC2Kill-scratch/corpus/knowledge   -> /home/vgpnk/…/kasegi-shokunin/corpus/knowledge
```

Same six at the base ref (`find -type l` = 58, escaping = 6). Export/ref agreement is
otherwise exact: base export `find -type f` = `7290`, `-type l` = `58` against ref
`files=7290 symlinks=58`.

**Likelihood.** Low for the eight named r38 check targets (they all live under real
directories; git cannot place a file beneath a symlink in one tree, so a parent-dir
hijack needs a *new* symlink committed at J). Medium for the general claim: the
`round-29/wave1/CritC2Kill-scratch/corpus/instruments` link means an export of any ref
already exposes the lane's live `corpus/instruments/`; once `r38-closure.sh` lands, an
export of `a173b0c2` will *contain* it through that link.

**Guard.** Do not adopt a blanket "no escaping symlink" limb — it is red on today's tree
(6 links) and the house rule is append-only, so it would be unsatisfiable. Two cheap limbs
that are green today and bite the exploit:

1. Completeness by count: `git ls-tree -r REF` non-`120000` count == `find "$EXPORT" -type f | wc -l`
   and `120000` count == `find "$EXPORT" -type l | wc -l` (measured 0.13 s for the whole
   tree, see E2).
2. Per-target mode assertion: for every path a check reads, require
   `git -C "$LANE" ls-tree REF -- "$p"` to be exactly one line with mode `100644`/`100755`
   (never `120000`), *before* reading it; and any `find`-style enumeration must use
   `-type f` (not follow). A selftest mutant whose target is a symlink to a live path must
   be rejected — that is the fixture above.

---

## 2. E2 — `export-ignore` attributes hide files; absence reads as "zero violations"

**Exploit sketch.** `git archive` honours `export-ignore` from `.gitattributes`. A file the
check counts violations in can simply be absent from the export; a limb written as
`n=$(grep -c TOKEN "$EXPORT/$p" 2>/dev/null || true); [ "$n" -eq 0 ]` then goes green.
Fixture, executed:

```text
$ printf 'corpus/lessons/round-38.md export-ignore\n' > .gitattributes ; git commit
$ git ls-tree -r --name-only HEAD   -> .gitattributes  corpus/lessons/keep.md  corpus/lessons/round-38.md
$ (cd dest && find . -type f)       -> ./corpus/lessons/keep.md  ./.gitattributes
$ grep -c 'pending' dest/corpus/lessons/round-38.md ; echo rc=$?
grep: …/dest/corpus/lessons/round-38.md: No such file or directory (os error 2)
rc=2
$ completeness loop            -> MISSING-IN-EXPORT corpus/lessons/round-38.md
```

The same shape covers `export-subst` (`$Format:…$` rewritten on extraction), so bytes
differ from the blob without any file being absent.

**Likelihood.** Low as an attack (needs `.gitattributes` at J; none is tracked today:
`git ls-tree -r --name-only 2387dcf6 | grep -c gitattributes` → `0`). High as a silent
false-green *class*: the frozen checks that count zero occurrences (G3's widened tokens,
G1's placeholder counts, G2's placeholder limb) all treat "absent" as "clean" unless they
assert presence first. This is the same mechanism as CritC1Kill K12 for the kill rule's
`grep -c` on an absent lesson.

**Guard.** Two lines, both cheap and green today:

1. Attribute detector over the ref (one process, NUL-safe both ways):
   `git -C "$LANE" ls-tree -r --name-only REF | git -C "$LANE" check-attr --stdin export-ignore export-subst`
   must contain `0` records whose value is not `unspecified` (measured `14692` records,
   `0` non-`unspecified`, at `2387dcf6`; on the fixture it prints
   `corpus/lessons/round-38.md: export-ignore: set`).
2. Fail-closed per-path presence: `[ -f "$EXPORT/$p" ] && git -C "$LANE" ls-tree -r --name-only REF -- "$p" | wc -l == 1`
   before any "count is zero" test — no `2>/dev/null`, no `|| true` on that read.

---

## 3. E3 — `--work` is guarded against the lane but not against the wave roots

**Exploit sketch.** `--work` is the only path the suite writes. r37 refuses the lane three
ways, and all three still hold (measured, exit status read without a pipe):

```text
--work <lane>/.ufo/w/w1        rc=2  r37-closure: --work must be outside the lane (it would write there): …/.ufo/w/w1
--work $S/lnk-lane (symlink to <lane>/.ufo/w)
                               rc=2  r37-closure: --work must be outside the lane (it would write there): …/.ufo/w
cd <lane> && --work relwork    rc=2  r37-closure: --work must be outside the lane (it would write there): …/kasegi-shokunin/relwork
                               and <lane>/relwork was NOT created
plain run                      rc=2  r37-closure: refusing to run against the live worktree: this suite is export-mode only.
```

What is *not* guarded: `--work` under the round's own scratch root is accepted and the
directory survives the run, because `cleanup()` removes `export/` and `mut/` but keeps a
user-specified work root:

```text
$ bash r37-closure.sh --export-ref HEAD --work /fast/scratch/hyaku/kasegi-r38/CritC1Export/workprobe
E9 payload=…,scratch-seat-dirs=0,…,scratch-root=absent closed=0     (the r37 root, not the r38 root)
closed=13/14 exit=1
$ ls -d /fast/scratch/hyaku/kasegi-r38/CritC1Export/workprobe       -> SURVIVES
```

The auto path has the same exposure from the other side: the work dir is
`mktemp -d -t r37-closure.XXXXXXXX`, which honours `TMPDIR` — and every seat's `TMPDIR`
is its own scratch under `/fast/scratch/hyaku/kasegi-r38/`. Measured with
`TMPDIR=$S` inside the r38 root: the suite ran (`closed=13/14`) and cleaned up
(`r37-closure.*` before=`0`, after=`0`), i.e. a *transient* directory appears inside the
root G6 scans for the duration of the run. For r38's own suite this is a live race against
G6 rather than a forgery.

**Likelihood.** High, not hypothetical: G6's frozen wording excludes "the suite's own
`--work` dir", so the exclusion path is caller-supplied. Passing `--work` equal to a real
leftover seat dir (`/fast/scratch/hyaku/kasegi-r38/ExecX`) makes that dir "the suite's own
work dir" and G6 green while the leftover exists. Nothing else in the construction pins
which path is excluded.

**Guard.** Extend the `make_work` case list (before `mkdir`, physical path, same shape as
the lane test):

```sh
for root in /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38; do
  case $norm in "$root"|"$root"/*) die "--work must be outside the wave scratch roots: $norm" ;; esac
done
```

and make G6 exclude *nothing*: require each root to be absent or hold zero entries. With
the guard above the suite always writes outside the roots, so the exclusion becomes
unnecessary — which is exactly what removes the hole.

---

## 4. E4 — stale work dirs: closed in r37, keep the shape, add one clause

**Exploit sketch.** A reused `--work` that still holds an old `export/` (with an old
`all-gates.txt` or old lesson bytes) satisfies a check without extracting anything.

Measured: r37 clears both owned subdirectories before use (`rm -rf -- "$EXPORT" "$MUT"`).
I planted a fake receipt and re-ran:

```text
$ mkdir -p …/workprobe/export/.ufo/waves/round-37/final-gates ; printf 'all-gates v1\n' > …/all-gates.txt
$ bash r37-closure.sh --export-ref HEAD --work …/workprobe   -> closed=13/14 exit=1
$ test -e …/workprobe/export/.ufo/waves/round-37/final-gates/all-gates.txt
CLEARED
```

**Likelihood.** Closed today. The residual is inherited from E3: `$WORK` itself survives,
so anything the suite writes *beside* `export/` and `mut/` (r37 writes `live-lines.txt`,
`selftest-report.txt`, `forge-*.txt` there) persists into the next run. Those are all
written with `>` before being read in the same run, so no stale read was found — but the
r38 suite must keep that property, and it must clear `export/` *and* its receipt/live-line
scratch file, not only the export.

**Guard.** (a) keep `rm -rf "$EXPORT" "$MUT"` before extraction; (b) truncate the live-lines
file with `: > "$LIVE"` at the start of the run, never `>>`; (c) re-verify with the planted
receipt fixture in selftest (a stale `all-gates` must not be readable after `prepare_export`).

---

## 5. E5 — G6 quiescence: `-type d`, caller-chosen root, and a TOCTOU against live seats

**Exploit sketch.** Three separate failure modes, all measured on the r37 limb that G6 is
modelled on (`E9` limb c, `find "$sroot" -mindepth 1 -maxdepth 1 -type d`, then
`cd "$d" && pwd -P` to compare against `$WORK`):

1. **Entries that are not directories are invisible.** Root holding one file and one
   symlink, no dir:

   ```text
   $ find $R -mindepth 1 -maxdepth 1   -> leftover-file.txt  leftover-link-into-root
   E9 payload=…,scratch-seat-dirs=0,… closed=0   (the quiescence limb is GREEN)
   ```

   The frozen G6 wording is "zero entries", so a copy of the `-type d` filter reads green
   with two leftovers present. (With a directory added: `scratch-seat-dirs=1`.)
2. **The scanned root is an argument.** `--scratch-root` is accepted (`SCRATCH_OVERRIDE=1`)
   and any *empty* directory satisfies limb (c); r37 only reports
   `scratch-root=present|absent` so a redirected root is visible but not rejected. A caller
   can therefore green the limb while `/fast/scratch/hyaku/kasegi-r38` is full.
3. **TOCTOU against live peers.** `find` lists an entry, then `cd "$d"` resolves it; a
   sibling that removes its dir in between yields `dp=''` (counted as leftover → false
   RED), and a sibling that creates one after `find` is invisible (false GREEN). Measured
   live at read time: `/fast/scratch/hyaku/kasegi-r36 absent`, `kasegi-r37 absent`,
   `kasegi-r38 present entries=28 dirs=28` — the count moves with every peer start/stop.

**Likelihood.** (1) Low as an attack, but it is a false-green in the limb's own shape.
(2) Low. (3) Certain: the r38 suite can only be run while peers are live, so the limb's
value is a snapshot of host state, not of the ref — the same objection CritC1Kill K7 raises
for `closed=8/8`; my row adds the mechanism and the entry-wise fix.

**Guard.** Pin constants, scan entries, do not resolve:

```sh
for root in /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38; do
  n=$(find "$root" -mindepth 1 -maxdepth 1 -printf 'x\n' 2>/dev/null | wc -l)   # absent root -> 0
  printf '%s entries=%s' "${root##*/}" "${n:-0}"
done
```

plus: reject any `--scratch-root` override that is not one of the three constants (selftest
fixtures may use a fourth, injected internally), and echo the three counts in the payload so
the receipt records what was measured rather than a single boolean.

---

## 6. E6 — G8 runs the export's r37 bytes, and `closed=14/14` is not satisfiable at REF

Two defects in one limb; the second is the one the frozen counting command cannot meet.

**6a. The instrument is ref-controlled.** G8 executes `"$EXPORT/corpus/instruments/r37-closure.sh"`,
i.e. whatever the judged head J committed. A stub satisfies any grep-shaped assertion:

```text
$ printf '#!/bin/sh\nprintf "closed=14/14 exit=0\\n"\nexit 0\n' > $D/export/corpus/instruments/r37-closure.sh
$ bash $D/export/corpus/instruments/r37-closure.sh | grep -E 'closed=14/14 exit=0'
closed=14/14 exit=0
G8-PASSES-ON-STUB
$ sha256sum stub                       -> 6679829ba4ebe04bc1f7f4b523356a23b2663011f5e5c77100f3d52b93387521
$ sha256sum real (2387dcf6 and tip)    -> 0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d
```

The pin is exact and free: the file is byte-identical at the r37 judged head and at the
lane tip, and inside the r37-head export
(`sha256sum arch2/corpus/instruments/r37-closure.sh` → `0da98e37…`). CritC1Kill K8 proposes
pinning blob `68ac41e8…`; that is the *git blob* hash, while `0da98e37…` is the sha256 of
the bytes — both bind, but G8 must compare the same function it prints. Use sha256 of the
exported bytes, and require the count once (`grep -cE '^closed=14/14 exit=0$'` == 1), not
`grep -q`.

**6b. E9's live limbs make 14/14 impossible for REF ≠ HEAD.** Measured, all three via the
r37 instrument in export mode:

```text
--export-ref a173b0c2 (base)          -> E9 status-dirty=3,head-match=0  closed=13/14 exit=1
--export-ref 2387dcf6 (r37 head)      -> E9 status-dirty=3,head-match=0  closed=13/14 exit=1
--export-ref 2387dcf6 (re-run later)  -> E9 status-dirty=15,head-match=0 closed=13/14 exit=1
--export-ref 7001535  (lane tip)      -> E9 status-dirty=3,head-match=1  closed=13/14 exit=1
```

The dirty count rose from `3` to `15` between two runs of the same ref while peers committed
their wave-1 files: limb (b) is a live reading, so the same command over the same bytes
prints a different payload minutes apart.

E9 limb (d) compares the exported ref with the *live lane's* `HEAD`; limb (b) reads the live
porcelain; limb (c) the live scratch root. At filing, J is committed and Y = J + receipt
follows, so a judge re-running G8 on J sees `head-match=0` no matter how honest the work
was. (ExecBaseRed records the same divergence at the base, and CritC1Kill K1 carries the
predicate-level consequence; this row is the mechanism plus a construction that satisfies
the frozen words anyway.)

**Construction that satisfies the frozen words, measured twice.** Give the r37 instrument a
*lane view fixed at REF* instead of the live lane. In `--work`:

```sh
git clone --shared "$LANE" "$WORK/r37lane"      # writes only under $WORK; lane untouched
git -C "$WORK/r37lane" checkout --detach "$REF"
[ "$(git -C "$WORK/r37lane" rev-parse --show-toplevel)" = "$WORK/r37lane" ]
[ "$(git -C "$WORK/r37lane" rev-parse HEAD)" = "$REF" ]
[ -z "$(git -C "$WORK/r37lane" status --porcelain)" ]
mkdir -p "$WORK/r37scratch"                     # an export-local, empty scratch root
bash "$EXPORT/corpus/instruments/r37-closure.sh" --export-ref "$REF" \
     --lane "$WORK/r37lane" --scratch-root "$WORK/r37scratch" --work "$WORK/r37run"
```

```text
$ git clone -q --shared <lane> $D ; git -C $D checkout -q --detach 2387dcf6…
TOPLEVEL_OK $D    HEAD=2387dcf6ccfefcfb703783387b9aade8fc82abfa dirty=0
E9 payload=status-read=ok,status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
closed=14/14 exit=0
(run again on the same fixture) -> closed=14/14 exit=0
```

while the real lane was dirty (`3` untracked wave entries) and `28` seat directories lived
under `kasegi-r38`. `git clone --shared` reads the lane only (verified after the fact:
`status --porcelain` unchanged, no `.git/index.lock`), and `--work` is outside the lane, so
this adds no write under the lane. Cost measured: one clone of 7346 entries ≈ 1 s, once per
run.

**Why this is also the guard, not just a trick.** The same invocation proves that
`--lane`/`--scratch-root` are a forge surface today: a caller can hand the r37 instrument a
clean clone and an empty root and get `closed=14/14 exit=0` while the real lane is red (it
is exactly what the block above does). So G8 must *construct* those two paths itself, from
constants, and the r38 suite must refuse `--lane`/`--scratch-root` overrides outside
selftest. If the L1 prefers not to clone, the honest alternative is a claim amendment
(G8 accepts `closed=13/14` whose only open id is E9, with `status-read=ok,lane-root=1`
recorded); I cannot make that call.

---

## 7. Counterexample table

| # | exploit (measured) | exploit result | likelihood | guard |
|---|---|---|---|---|
| E1 | export carries 6 absolute symlinks; a file outside the ref is readable through the export | fixture prints `YES-VISIBLE-IN-EXPORT`; live bytes replace ref bytes | low for the 8 named targets, medium in general | count-completeness + per-target `ls-tree` mode != `120000`; `find -type f`; selftest symlink mutant |
| E2 | `export-ignore` removes the lesson/declared-blocks file | export has 2 of 3 files; `grep -c` → rc=2, no count → "zero violations" | low as attack, high as silent class | `check-attr` (measured 14692 records, 0 set) + fail-closed `-f`/tracked presence before any zero-count limb |
| E3 | `--work` under `kasegi-r38` accepted and persists | `SURVIVES` after exit; G6 excludes "the suite's own work dir" = caller choice | high | extend the lane case-list to the three wave roots; G6 excludes nothing |
| E4 | stale `export/` reused | planted receipt `CLEARED`, run unchanged 13/14 | closed | keep `rm -rf export mut`; truncate live-lines; stale-receipt selftest |
| E5 | quiescence limb counts only directories; root is an argument; `cd` resolution races live seats | file+symlink root → `scratch-seat-dirs=0` (green); 28 live seat dirs at read | (1) low, (3) certain | entry-wise `find -printf` on pinned constants, no `cd`; counts in payload |
| E6a | export's r37 bytes are J-controlled | stub prints `closed=14/14` → `G8-PASSES-ON-STUB` | high | sha256 pin `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`, `grep -c` == 1 |
| E6b | E9's live limbs at REF ≠ HEAD | base/r37-head/tip exports all `closed=13/14` | certain | fixture `clone --shared` at REF + export-local scratch root → measured `closed=14/14` twice |

## 8. Impacted axes

| axis | impact |
|---|---|
| depth:verifiability (C1, held 4) | E2 and E6a are false-green surfaces in *this* round's suite (a hidden file or a stub r37 satisfies a limb); E3/E5 make G6 both forgeable and load-bearing on host state; E6b is the same claim-truth hazard CritC1Kill K1 and ExecBaseRed record, with a measured construction that meets the frozen words. Export-only is the claim's whole defence, and today it is not proven: the export is not asserted equal to the ref. |
| depth:density | none (receipt only, no lane bytes) |
| coverage | none |

Verdict: **fixable defects, not a rejected tradeoff** — every guard above is one or two
shell conditions and none weakens a check. The one thing the canonical judge should not
accept is a G8 limbed on `grep -q closed=14/14` over export-controlled bytes, or a G6 that
excludes a caller-supplied path.

## 9. Smallest safe corrections, ranked

| id | sev | one-line fix | cost |
|---|---|---|---|
| E6a | S1 | pin the r37 bytes (`sha256 == 0da98e37…`) before running them; require the `closed=14/14` line count == 1 | 3 lines |
| E6b | S1 | build the r37 lane view in `--work` (`clone --shared` at REF, `checkout --detach`, assert toplevel/HEAD/clean) + export-local `--scratch-root`; refuse caller overrides | ~10 lines, 1 clone |
| E2 | S2 | `check-attr … export-ignore export-subst` all `unspecified`; every zero-count limb asserts `-f` + tracked first | 2 conditions |
| E3 | S2 | add `kasegi-r36|r37|r38` to `make_work`'s refusal list; G6 excludes nothing | 3 lines |
| E5 | S2 | entry-wise `find -printf '%f'` over three pinned roots, no `cd`, counts in payload | 4 lines |
| E1 | S3 | count-completeness + `ls-tree` mode check on each read target; selftest symlink mutant | 5 lines + 1 fixture |
| E4 | S3 | truncate the live-lines file; stale-receipt selftest | 2 lines |

## 10. Cross-references (no duplication intended)

* CritC1Kill K7 (G6 is the only non-export limb) and K8 (r37 bytes unbound) name the two
  shapes in E5/E6a at predicate level; this receipt supplies the measured mechanism
  (entry-type filter, root override, TOCTOU, stub forgery, digest value and the clone
  construction).
* CritC1Kill K1 and ExecBaseRed § "The G8 divergence" record that 14/14 is unreachable on a
  historical ref; E6b adds the run that reaches it reproducibly and the code to do so.
* ExecBaseRed's finding 3 (`declared-blocks.txt` must declare round-38 bytes) stands; E2's
  presence rule is what stops that file being absent from the export.
