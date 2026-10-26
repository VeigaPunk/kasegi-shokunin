# ExecRunbookChecks — round-39 receipt (integration runbook for the L1)

Seat: executor, axes depth:verifiability. Leaf seat; no subagent dispatch used. Read-only throughout the lane;
all writes are this receipt, the deliverable beside it, and scratch under
`/fast/scratch/hyaku/kasegi-r39/ExecRunbookChecks` (removed before yielding).

## Deliverable

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-39/wave1/ExecRunbookChecks.runbook.md` | 402 | 26,620 | `6bc87163887e65c2d119618a768f51f7ee6fcc57dc3730e6606d523de03e60be` |

Contents: landing sequence B1 capture → B2 rows/entry → B3 instrument → B4 required reds → B5 corrections →
B6 ledger → B7 declarations → B8 = J; the receipt cycle J → R1 (bootstrap receipt) → Y (genuine receipt,
`git diff --name-only J Y` = the receipt only); the exact `jj-lane.sh commit` boundary table with pathspecs and
message text; a validation matrix with every expected value and its source; G1–G8 rule notes; measured
constraints; stop conditions. The deliverable was scanned for the six placeholder/leftover token families and
the inference-bracket dodge named in the ExecNoPlaceholderScan item: 0 hits.

## Evidence (commands run, actual output)

All commands ran from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` with `TMPDIR` bound to the scratch dir.

### E1 — base counters match the frozen before-controls

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
entries=24 pass=24 exit=0
$ python3 corpus/instruments/capture-binding-check.py | tail -1
records=45 bound=45 unbound=0
$ python3 corpus/instruments/recheck-audit.py --quiet | tail -1
expect=present expected=50 missing=0 unexpected=0 exit=0
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                    -> 21
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 55
$ ls corpus/knowledge/*.md | wc -l                              -> 50
```

### E2 — frozen r38-head hash is malformed; the erratum is already filed

```
$ git rev-parse 66703ac
66703acaaff50529a35be49aa8759d04140720ad
$ git rev-parse 66703aca50529a35be49aa8759d04140720ad
fatal: ambiguous argument '66703aca50529a35be49aa8759d04140720ad': unknown revision
$ grep -o '66703aca[0-9a-f]*' .ufo/waves/round-39/claims.json | sort -u
66703aca50529a35be49aa8759d04140720ad          # 38 chars, not 40
$ git log -1 --format='%h %s' 7beae60
7beae60 round-39: claims erratum 1 (registry 59; r38-head full hash)
```

The runbook uses the 40-char `66703acaaff50529a35be49aa8759d04140720ad` for every control run and cites
erratum E2 instead of re-filing it.

### E3 — registry after-count is 59, not the frozen 58

Base registry rows 55; the round appends four rows (S057 mined, S056/S058/S059 rejected); the seat row files are
each NF=13; `grep -cE` on a scratch mirror with the four rows inserted after `S055` prints `59`. Census on the
mirror (`validate --file`, knowledge dir symlinked) printed the two W04 lines plus a single
`E11 S057 missing used-by corpus/knowledge/cisa-when-to-issue-vex.md` while the F22 entry deliverable was
still in flight — i.e. the only blocker to the claims' `exit 0` is the entry landing, not the rows. Erratum E1
(commit `7beae60`) already records 59.

### E4 — S057 recheck and the junk twin, measured from the wave-1 bytes

```
$ cp ExecFrontierCapture.{S057.txt,manifest.json} into <mirror>/corpus/source-snapshots/round-39/
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
recheck_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest .../junk-manifest.json --source S057
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
junk_exit=1
```

### E5 — plain run is refused; suites are mode 644

```
$ bash corpus/instruments/r38-closure.sh; echo $?
r38-closure: refusing to run against the live worktree: this suite is export-mode only.
r38-closure: pass --export-ref <hash> (see --help) or --selftest.
2
$ ls -l corpus/instruments/r37-closure.sh corpus/instruments/r38-closure.sh   -> -rw-r--r-- both
```

### E6 — the J-versus-receipt-head reading, measured on the r38 suite

```
$ bash corpus/instruments/r38-closure.sh --export-ref 66703acaaff50529a35be49aa8759d04140720ad \
      --lane "$LANE" --work <scratch>/work/r38-j | tail -3
G8 payload=r37-suite=1,r37-closed=0,r37-exit=1 closed=0
closed=6/8 exit=1
$ bash corpus/instruments/r38-closure.sh --export-ref 7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e \
      --lane "$LANE" --work <scratch>/work/r38-y | tail -2
G8 payload=r37-suite=1,r37-closed=0,r37-exit=1 closed=0
closed=7/8 exit=1
```

The receipt-bearing head cannot reach 8/8 today because G8 executes the pinned r37 suite, whose E9 limb reads
LIVE lane state:

```
$ bash <pinned r37-closure.sh> --export-ref 7dd2fcd6… --lane "$LANE" --work <scratch>/work/r37-y | grep '^E9'
E9 payload=status-read=ok,status-dirty=5,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
```

`head-match=0` because the live lane HEAD (`7beae60`) is not the exported ref, and `status-dirty=5` because
wave-1 files are still untracked. At the judged head with a clean tree and `HEAD` equal to the exported commit,
E9 is green and G8 closes. The runbook therefore makes “clean tree, HEAD = exported commit, empty kasegi-r37”
a hard precondition for the R1/Y runs, and records that a later replay at a moved tip must not be read as an
r39 regression.

Reading recorded in the runbook: the receipt's `export-ref` names the no-receipt commit J, and the exported
commit must be the receipt-bearing head; expected pair is J → `closed=7/8 exit=1` (G2 red, receipt absent)
and Y → `closed=8/8 exit=0`. The r38 receipt's own `export-ref-run: closed=7/8 exit=1` is the same structural
fact. The J-only number is never to be quoted as the judged run.

### E7 — front-door fence state and append boundaries

```
$ python3 <CommonMark walk over ``` and ~~~> for corpus/README.md, PROVINCE.md
corpus/README.md EOF-fence-state= closed
PROVINCE.md EOF-fence-state= closed
```

Both files end outside any fence, so the round-39 appends land outside fences and a `Correction (round 39)`
line there would count. Every append deliverable ends with a newline; `PROVINCE.md` is 156 lines and
`corpus/README.md` 486 lines at the current tip, matching the runbook's 157 / 514 expectations.

### E8 — the audit's expected list is a landing dependency

```
$ wc -l corpus/instruments/knowledge-expected.txt        -> 52 (2 comment lines + 50 entries)
$ diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | sort) <(ls corpus/knowledge/*.md | sort)
   (empty, exit 0)
```

Without inserting `corpus/knowledge/cisa-when-to-issue-vex.md`, the audit prints
`unexpected=corpus/knowledge/cisa-when-to-issue-vex.md` and exits 1, so `expected=51` is unreachable. The runbook
adds this line to boundary B2.

### E9 — stale premise in the QUALITY item

```
$ wc -l corpus/QUALITY.md; wc -c corpus/QUALITY.md
292 corpus/QUALITY.md
46569 corpus/QUALITY.md
```

QUALITY lives at `corpus/QUALITY.md`, not the lane root, and is 292 lines / 46,569 bytes (the item text said
288 lines / 45.5 KB). Recorded in the runbook so the L1 measures before appending.

### E10 — lane and tool state

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kasegi-shokunin
state branch=master local=7beae6098f58cba99b0a9d1ac387edc664c0abe4 remote=7beae6098f58cba99b0a9d1ac387edc664c0abe4 ahead=0 behind=0 head=detached tracked=0 untracked=7
$ bash scripts/hyaku/disk-guard.sh status     -> /fast/scratch/hyaku 24% used, 610.6G free (green)
```

The lane is jj-colocated; `jj-lane.sh commit <lane> --as kasegi -m <msg> -- <paths>` is pathspec-limited and
prints `landed <hash>`; `.ufo/waves/...` paths are committable while bare `.ufo` is not.

### E11 — results identity for G4

```
$ python3 -c 'round-38 results: entries=73 distinct names=73; keys={name,agent,output,note}; seats=73'
$ python3 -c 'round-38 dispatch wave1-dispatch.json tasks=73'
```

Identity is the per-entry `name` (unique); `agent` is the role and repeats. The runbook requires 49 entries with
49 distinct names, under either `kasegi-r39-build-results.json` or `wave1-results.json`.

### E12 — pinned r37 digest

```
$ git show 2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh | sha256sum
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  -
```

Recorded in the runbook's G8 note.

## Expected-value cross-check against claims.json

| claims.json expectation | Frozen value | Source of the runbook expectation |
|---|---|---|
| frontier rows | 22 | C2 counting command; base 21 measured (E1) |
| registry rows | 58 | 59 per erratum E1 (base 55 + four rows; measured in E3) |
| entries citing S057 | 1 | C2 counting command |
| harness | entries=25 pass=25, PASS F22 ids=S057 | C2; base 24/24 measured (E1) |
| source-recheck S057 | exit 0 | C2; measured 5 OK lines, exit 0 (E4) |
| binding | records=46 bound=46 unbound=0 | C2; base 45/45 measured (E1) |
| audit | expected=51 missing=0 unexpected=0 | C2; base 50 measured (E1) + E8 dependency |
| census | exit 0, W04 S028/S029 only | C2; base and mirror both measured (E1, E3) |
| knowledge count | 51 | C2 |
| suite at judged head | `closed=8/8 exit=0` | C1; satisfiable only over the receipt-bearing head (E6) |
| suite selftest | `selftest cases=8 failures=0`, 8 graded cases | C1 |
| base red | `closed<8/8 exit=1` | C1 (hash per E2) |
| r38-head red | `closed<8/8 exit=1` | C1 + erratum E2 |
| plain run | exit 2 | C1; measured on the r38 model (E5) |
| junk twin | 4 MISMATCH, exit 1 | C2; measured independently (E4) |

## Discrepancies found (both already covered by erratum `7beae60`)

1. **Registry after-count** — frozen 58, actual 59 (four appended rows). Erratum E1.
2. **r38 judged-head hash** — frozen string is 38 hex chars and does not resolve; the real head is
   `66703acaaff50529a35be49aa8759d04140720ad`. Erratum E2.

Two reading notes the report must carry (not numeric errata):

3. C1's “8/8 on J” is satisfiable only over the head that adds the receipt (J+receipt), because G2 reads the
   receipt from the export while the receipt cannot name its own commit. Expected pair J → 7/8, Y → 8/8.
4. G8 is live-state bound through the pinned r37 suite's E9; the judged run must be taken at Y with a clean
   tree, `HEAD` = Y, and an empty `kasegi-r37`.

## Risks and open items

- `corpus/instruments/r39-closure.sh` (ExecSuiteBuild) and several wave-1 deliverables were still in flight when
  the runbook was written (`ScribeEntryF22.entry.md`, `ScribeShonen.shonen.append.md`, the fixture packs,
  `ExecHarnessProbe.harness.txt`, `ExecCensusAfterMirror`, `ExecArchiveNoHarmMirror`, `ExecNoPlaceholderScan`,
  `ExecProofSuiteSelftest`). The runbook's section 1 presence loop is the gate; G payload keys must be copied
  from the landed suite's actual output, never hand-written.
- The receipt cycle needs at most two receipt-only commits; a third is admissible only if the receipt's diff
  against J stays receipt-only, and each receipt commit needs a fresh run at the new head.
- No commit is permitted after Y in this round; the lane tip must stay at Y with a clean tree.
- The census mirror measurement (E3) was taken with the F22 entry absent, so it shows the entry as the sole
  remaining E11; the runbook's expected exit 0 depends on B2 landing that entry.

## Tooling

No installs or upgrades; no pacman transaction. Instruments used were already committed. `jj-lane.sh state` and
all git calls were read-only.

## Scratch

`/fast/scratch/hyaku/kasegi-r39/ExecRunbookChecks` removed before yielding; the mirror under it held only
copies of wave-1 bytes and symlinks to lane files.
