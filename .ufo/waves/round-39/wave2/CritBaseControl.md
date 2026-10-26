# CritBaseControl — round-39 do-nothing controls (wave 2, attack seat)

Seat `CritBaseControl` (leaf, critic). Item: with the r39 suite landed, prove the do-nothing
controls red — `--export-ref 480b1a50…` (base) and `--export-ref 66703acaaff50529a35be49aa8759d04140720ad`
(r38 judged head) must each print `closed<8/8 exit=1`, record every G line; then verify a round
that ships NONE of the C1/C2 changes cannot produce the C2 after-counts.

Seat declaration: I did not write the deliverable under attack (`corpus/instruments/r39-closure.sh`,
the C2 rows/capture/entry, the receipts). Nothing in this receipt is authored by the seat that
produced them.

Environment. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `HEAD=5006097a84305267c9a3e8c1e1d560e60fe41d37`
(Y), J = `46c66c268502abd1b2c342fc71bf88ccf721845b`, `git diff --name-only J Y` =
`.ufo/waves/round-39/final-gates/all-gates.txt` (verified). Suite bytes executing are the committed
bytes: `sha256sum corpus/instruments/r39-closure.sh` =
`2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`, identical to the
`suite-sha256=` line the suite prints and to the receipt's `suite-sha256`. Read-only git only; no
tool installed, no network fetch, all work under `/fast/scratch/hyaku/kasegi-r39/CritBaseControl/`
(removed before yield). Runs were serial; the first attempt launched the two control runs in
parallel and the tool merged their byte streams (both outputs carried both processes' stderr), so
both were re-run serially and only the serial transcripts below are the record.

Axes: `depth:verifiability` (primary — the control decides whether C1 discriminates), `coverage`
(secondary — whether the C2 counters discriminate).

---

## 1. Control A — base 480b1a50 exports red

```
$ export-ref=480b1a505a2dfc14a4f718d16d63808247214d0a mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
$ bash corpus/instruments/r39-closure.sh --export-ref 480b1a50… --work $S/w-base --scratch-root $S/clean-scratch
G1 payload=declared=0,valid=0,front-doors=0,tail-match=0,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=0,corrections-inside=0,corrections-declared=1,diff-read=missing closed=0
G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,diff-read=ok,digest-match=0,export-suite=0,run-lines=0,closed-lines=0,distinct-ids=0,closed-line=0,graded-cases=0,ungraded-cases=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0,final-lane-commit=0 closed=0
G3 payload=added-quotes=0,covered=0,uncovered=0,report-only=0,diff-read=ok closed=1
G4 payload=dispatches=0,pairs=0,seats-ok=0,zero-task=0,read=fail closed=0
G5 payload=round39-section=0,final-lane-commit=0,correction=0,correction-labeled=0 closed=0
G6 payload=r37=absent,r38=absent,r39=absent,work=outside,tolerated=none,read=ok closed=1
G7 payload=section=0,after-round38=0,correction=0,rows=0,proposal-1=0,proposal-3=0 closed=0
G8 payload=pin-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
closed=2/8 exit=1
```

exit=1 (`EXIT=1` measured). Base is red on G1, G2, G4, G5, G7, G8.

Second base run with the **default scratch root** (no `--scratch-root`), which is the live G6
limb and which every in-progress wave-2 seat must also produce:

```
G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=none,read=ok closed=0
closed=1/8 exit=1
```

G6 reds fail-closed on real residue (my own work dir/logs plus sibling seat dirs under
`kasegi-r39`; `read=ok`, never `read=fail`) — the check is live, not a stub.

## 2. Control B — r38 judged head 66703aca exports red

```
$ bash corpus/instruments/r39-closure.sh --export-ref 66703acaaff50529a35be49aa8759d04140720ad --work $S/w-r38 --scratch-root $S/clean-scratch
G1 payload=declared=0,valid=0,front-doors=0,tail-match=0,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=0,corrections-inside=0,corrections-declared=1,diff-read=missing closed=0
G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,diff-read=ok,digest-match=0,export-suite=0,run-lines=0,closed-lines=0,distinct-ids=0,closed-line=0,graded-cases=0,ungraded-cases=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0,final-lane-commit=0 closed=0
G3 payload=added-quotes=0,covered=0,uncovered=0,report-only=0,diff-read=ok closed=1
G4 payload=dispatches=0,pairs=0,seats-ok=0,zero-task=0,read=fail closed=0
G5 payload=round39-section=0,final-lane-commit=0,correction=0,correction-labeled=0 closed=0
G6 payload=r37=absent,r38=absent,r39=absent,work=outside,tolerated=none,read=ok closed=1
G7 payload=section=0,after-round38=0,correction=0,rows=0,proposal-1=0,proposal-3=0 closed=0
G8 payload=pin-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
closed=2/8 exit=1
```

exit=1. Both required controls hold: `closed<8/8 exit=1`. The payloads are byte-identical between
base and r38 head because neither tree carries any round-39 artifact (verified in the base export:
no `corpus/instruments/r39-closure.sh`, no `.ufo/waves/round-39/declared-blocks.txt`, no
`final-gates/all-gates.txt`, no `corpus/source-snapshots/round-39/`, `S057` rows 0, `F22` in
README 0).

### Per-check attribution of the control reds (what actually discriminates)

| check | base/r38 payload | why red | discriminating for a do-nothing round? |
|---|---|---|---|
| G1 | `declared=0,front-doors=0` | round-39 declarations absent | yes |
| G2 | `receipt=0,graded-cases=0` | round-39 receipt absent | yes |
| G4 | `dispatches=0,read=fail` | no round-39 dispatch | yes |
| G5 | `round39-section=0,correction=0` | no round-39 labels | yes |
| G7 | `section=0,rows=0` | no round-39 ledger section | yes |
| G3 | `added-quotes=0` → **closed=1** | vacuous pass: nothing added, nothing to quote | no (free pass) |
| G6 | `work=outside` → **closed=1** (isolated root) | liveness, no residue | no (free pass; reds on live residue, §1) |
| G8 | `r37-closed=0,r37-exit=1` | **environment**, see §3 — also red at Y | no |

So the do-nothing floor is five content-driven reds (G1, G2, G4, G5, G7); G3/G6 are vacuous-green
at a quiet scratch root, and G8's control red is not evidence about base/r38 at all.

## 3. G8 probe — the control's G8 red is environment-driven, not ref-driven

`check_g8()` runs the pinned r37 suite (`PIN_R37_SHA=0da98e37…434d`, verified) with the live lane. I
ran those pinned bytes directly at all three refs:

```
$ bash r37-pinned.sh --export-ref <ref> --lane /…/kasegi-shokunin --work $S/r37-<ref> --scratch-root $S/clean-scratch
base 480b1a50 : E9 payload=status-read=ok,status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
               closed=13/14 exit=1
r38  66703aca : E9 payload=status-read=ok,status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
               closed=13/14 exit=1
Y    5006097a : E9 payload=status-read=ok,status-dirty=6,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=0
               closed=13/14 exit=1
```

E9 reds on `status-dirty=6` (the in-progress lane's untracked `.ufo/waves/round-39/…` entries) at
every ref, so G8 is red regardless of the exported ref; only `head-match` moves (0/0/1). Consequence
for the positive side, measured in the same environment:

```
$ r39-closure.sh --export-ref 5006097a… (Y)  → closed=7/8 exit=1   (G8 red, r37-closed=0)
$ r39-closure.sh --export-ref 46c66c2…  (J)  → closed=6/8 exit=1   (G2 receipt=0, G8 red)
$ r39-closure.sh                              → exit 2   ("refusing to run against the live worktree: this suite is export-mode only.")
```

The receipt's committed `closed=8/8` was measured with a clean tree; E4's documented J-run
(`7/8, receipt=0`) likewise. With wave-2 files untracked, the suite cannot print 7/8 at J or 8/8 at
Y. That precondition is documented in the suite header ("at the real judged head the lane must be
checked out at Y with a clean tree, else G8 reds by construction") — so it is a known limit, not a
hidden one — but it means **no in-process run this wave can reproduce C1's green**, and my control
must not cite G8's red as content discrimination.

## 4. A round that ships NONE of the C1/C2 changes cannot produce the after-counts

Trees extracted with `git archive` into scratch (`mirror-base`, `mirror-r38`, `mirror-head`); every
counter run with cwd at the extracted root (audit counters are cwd-bound, §5.3).

| counter (frozen form) | base 480b1a50 | r38 head 66703aca | HEAD/Y 5006097 |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | **21** | **21** | 22 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **55** | **55** | 59 (E1) |
| `grep -rlE '^source: S057' corpus/knowledge \| wc -l` | 0 | 0 | 1 |
| `ls corpus/knowledge/*.md \| wc -l` | **50** | **50** | 51 |
| `frontier-recheck-count.py` | **entries=24 pass=24 exit=0** | **entries=24 pass=24 exit=0** | entries=25 pass=25 exit=0 |
| `capture-binding-check.py` | 45/45, `unbound=0` | 45/45, `unbound=0` | 46/46, `unbound=0` |
| `recheck-audit.py --quiet` | `expected=50 missing=0 unexpected=0` | `expected=50 missing=0 unexpected=0` | `expected=51 missing=0 unexpected=0` |
| `source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` | `manifest UNAVAILABLE reason=missing` **exit=2** | same **exit=2** | four `S057:Q<n> OK … anchor=<n>-ok` **exit=0** |
| `sources-census.sh census` (FLEET) | rows 55, mined 43, rejected 3, queued 9, missing 0, exit 0 | — | rows 59, mined 44, rejected 6, queued 9, missing 0, exit 0 (also exact frozen lane form `census --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi rows 59`, exit 0) |
| `sources-census.sh validate` | exit 0 (W04×2 only) | — | exit 0 (W04×2 only, same two) |

Expected-list binding (cross-tree attack: HEAD's committed expected list over the base tree):
`recheck-audit.py --root <base> --expect <HEAD>/corpus/instruments/knowledge-expected.txt` →
`expected=51 missing=1 unexpected=0 exit=1` (missing = `corpus/knowledge/cisa-when-to-issue-vex.md`).
The 51 requires the new entry's bytes, not just a list edit.

Verdict on this control: **holds**. None of 22 / 59 / 51 / 25-25 / 46-46 / expected=51 is reachable
from either no-change tree; the harness row count, registry count, knowledge count, binding count,
audit expected set and S057 recheck all move only with the round-39 content.

## 5. Findings

### F1 — C2 `junk-f22 rejected` is not rerunnable where it is frozen (minor; fail-closed, not a kill)

`.ufo/waves/round-39/c2-controls/junk-manifest.json` declares `"path": "S057.txt"`, and
`source-recheck.py` resolves `path` against `manifest_path.parent` (`base = manifest_path.parent`,
`resolved = (base / path)`), so the frozen artifact alone gives:

```
$ python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-39/c2-controls/junk-manifest.json --source S057
S057:source UNAVAILABLE reason=missing
exit=2
```

The same holds for the delivered `wave1/ExecJunkRecheck.manifest.json` run from its own directory
(no `S057.txt` there; the capture is `ExecFrontierCapture.S057.txt`, and `check_source` requires
`Path(path).stem == id`). With the documented capture-relative step (copy the committed
`corpus/source-snapshots/round-39/S057.txt`, sha256 `11c8d6d6…d64f2f`, beside the manifest) the
recorded signature reproduces exactly:

```
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
exit=1
```

`ExecJunkRecheck.md` §3.4/§7 documents this path semantics, and exit 2 is fail-closed (the
instrument did not accept a junk claim), so the kill rule ("junk-f22 accepted") is not triggered.
Smallest safe correction: commit a byte-identical `S057.txt` beside `c2-controls/junk-manifest.json`
(or write the copy step into the frozen counting command), so the counter's recorded `exit=1` is
reproducible from frozen bytes. Impacted axis: coverage (control reproducibility).

### F2 — G8 gives the control no discrimination; C1's green is tree-state-gated (minor; documented)

Measured in §3: G8 red at base, r38 head **and** Y, all from pinned-r37 E9 `status-dirty=6`; Y now
prints `closed=7/8 exit=1`, J `closed=6/8 exit=1`. The suite header already states the clean-tree
precondition, and E4 documents the J-run. Smallest safe correction: no lane change needed for the
control (it is red either way); the round report must (a) not quote my in-process Y/J numbers as a
claim, and (b) attribute C1's discrimination to G1/G2/G4/G5/G7 rather than to G8. Impacted axis:
depth:verifiability.

### F3 — the audit's `exit=0` limb is cwd-bound, not ref-bound (paper-level; not a kill)

`recheck-audit.py`'s strict `cdroot` limb compares each `cd <path> && …` target against `--root`:
on any export mirror both base and HEAD report `cdroot_fail=50/51` and `exit=1`, while the
discriminating field is `expected=50` vs `expected=51`. `exit=0` is therefore produced by running
inside the live lane path, not by a tree. The C2 kill rule reads `expected`/`unexpected`, so nothing
is killed; the counting-command line should be read as `expected=51 missing=0 unexpected=0` +
`exit=0 from the lane root`. Impacted axis: coverage.

### F4 — claims.json freezes `registry != 58`; measured 59 (paper contradiction, resolved by E1)

`claims.json` C2 counting command and kill rule say 58; E1 fixes both to 59; HEAD measures 59
(`grep -cE` and census `rows 59` agree, no duplicate id — `uniq -c` over `^\| S[0-9]{3,}` printed
nothing above one). A literal reader applying the as-frozen kill rule to HEAD would red the round.
Smallest safe correction: the report cites E1 by id wherever 58 appears (already the erratum's
instruction); no lane byte changes. Impacted axis: coverage.

## 6. Verdict

- Control A (base) and Control B (r38 judged head): **both red, `closed=2/8 exit=1`** (1/8 with the
  live scratch root), each G line recorded above. C1 is not satisfiable by a no-change tree.
- Do-nothing after-counts: **unreachable** — 21/55/50/24-24/45-45/expected=50/S057 exit 2 on both
  no-change trees versus 22/59/51/25-25/46-46/expected=51/S057 exit 0 at HEAD.
- No kill triggered by this seat. Two repair-worthy defects on landed bytes (F1 reproducibility of
  the C2 junk control, F4's 58-vs-59 paper text resolved only by erratum), one environment gate on
  C1's green (F2), one counter-semantics note (F3).

Scratch `/fast/scratch/hyaku/kasegi-r39/CritBaseControl/` removed after this receipt was copied to
the wave dir. Writes made: this file only.
