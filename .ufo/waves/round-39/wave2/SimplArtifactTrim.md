# SimplArtifactTrim — round-39 wave 2 (falsify) receipt

Seat: `SimplArtifactTrim` (simplifier, leaf; no spawns, no swarm, no `agent://all`).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo; fleet root and
`shokuknow` read-only and unread for this item).
HEAD at review: `5006097a84305267c9a3e8c1e1d560e60fe41d37` (Y). J =
`46c66c268502abd1b2c342fc71bf88ccf721845b` (`final-gates/all-gates.txt` `export-ref=`).
Base `480b1a505a2dfc14a4f718d16d63808247214d0a`. Snapshot `2026-10-26T20:21:13Z`.
Axes named: depth:verifiability, coverage.

Item: review the full round-39 artifact set (wave dirs + new lane commits), identify
redundant / duplicated / superseded artifacts, propose a minimal evidence set for the
report. Read-only on every repo. Deliverable: `SimplArtifactTrim.trim.md` (19,256 B).

**Author declaration**: I wrote none of the artifacts reviewed (no wave-1 or wave-2
deliverable, no lane file). I read the frozen claims first. My writes are exactly this
receipt, the deliverable, and `$S` scratch, which is removed before yielding.

## 1. Reads and inventory

```
$ git log --oneline 480b1a50..HEAD
5006097 round-39: receipt Y (all-gates v3)
46c66c2 round-39: content head J2 (lesson, LOG, SCORECARD, SHONEN, wave1 results + evidence)
1a139e0 round-39: wave1 integration (C1 suite + C2 F22/S057; corrections, criteria, ledger, distance block)
57ea9ea round-39: erratum E5 non-vacuous semantics
06632fa round-39: erratum E4 (verification ref Y = J + receipt)
7beae60 round-39: claims erratum 1 (registry 59; r38-head full hash)
d65d823 round-39: wave1 spec/dispatch
dcd3170 round-39: claims freeze C1/C2 + controls

$ git ls-files .ufo/waves/round-39 | wc -l          -> 262
$ git ls-files -z .ufo/waves/round-39 | xargs -0 stat -c%s | awk '{s+=$1} END{print s}'
                                                    -> 3670980
$ git ls-files --others --exclude-standard .ufo/waves/round-39 | wc -l   -> 19 (wave 2 in flight)
```

Per-directory bytes (live dir, `os.walk` + `getsize`): root files 24 / 2,282,680;
`wave1` 236 / 1,597,122; `c1-controls` 1 / 1,017; `c2-controls` 4 / 8,298;
`final-gates` 2 / 2,366 (`all-gates.txt` tracked + wave-2 `reds.txt` untracked);
`wave2` 31 entries at 20:21Z; `__pycache__` 2 / 74,567.

## 2. Duplication measurements (commands + actual output)

### 2.1 Byte-identical to landed files

```
$ sha256sum corpus/instruments/r39-closure.sh .ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh
2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b  corpus/instruments/r39-closure.sh
2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b  .ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh
$ sha256sum corpus/instruments/r37-closure.sh .ufo/waves/round-39/wave1/ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  (both)
$ sha256sum corpus/source-snapshots/round-39/S057.txt .ufo/.../wave1/ExecFrontierCapture.S057.txt
11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f  (both)
$ sha256sum corpus/source-snapshots/round-39/manifest.json .ufo/.../wave1/ExecFrontierCapture.manifest.json
432f2205b368acb39d620bb85fe81c0fd6ccb345dd0878661478085ac1ce6659  (both)
$ sha256sum c2-controls/junk-f22-recheck.txt wave1/ExecJunkRecheck.junk-recheck.txt
7d6e7df20fc546625a60c5e72a7e24cb9e6803344238f73188651c36fbffbcbc  (both)
$ sha256sum c2-controls/junk-manifest.json wave1/ExecJunkRecheck.manifest.json
9dafce3647086cd082ab5ebb53d9b9601fd43ff76f701e595c5503afc388470a  (both)
$ sha256sum wave1/ExecSuiteBuild.overlay/blocks/province.append.md wave1/ScribeProvinceF22.province.append.md
bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d  (both)
```

Also: `overlay/blocks/reds.txt` vs `overlay/run-at-base.txt` —
`diff <(cat blocks/reds.txt) <(cat run-at-base.txt)` → `2d1 < deviation=non-default --lane`
(1,330 vs 1,301 B), i.e. the base transcript twice.

### 2.2 Append blocks contained byte-exact in landed files

`python3` containment (`wave bytes in landed bytes`): 16 of 26 candidate blocks pass —
`ExecCorrectionsR2.{log,scorecard,shonen,round38-lesson}.append.md`,
`ExecQualityCriteria.quality.append.md`, `ExecConsidertheseLedger.ledger.append.md`,
`ExecConsiderthese.scorecard.append.md`, `ScribeSearchLog.searchlog.append.md`,
`ScribeRowS057.row.md`, `ScribeRowsRejected.S056/S058/S059.row.md`,
`ScribeFrontierF22.readme.append.md` (after trailing-newline trim),
`ScribeProvinceF22.province.append.md`, `overlay/blocks/province.append.md`,
`ScribeEntryF22.entry.md` → 51,562 B. Superseded total (2.1 + 2.2) = **229,458 B**.

Draft superseded by landed row: `wave1/ExecConsiderthese.ledger-row.md` is not contained
but is replaced by the landed `## Round-39 dispositions` row 1
(`corpus/knowledge/considerthese-proposals-ledger.md:81`), which carries the same status
plus the numbering correction and the score-gap measurement.

### 2.3 Stale declaration block

```
$ sha256sum .ufo/waves/round-39/declared-blocks.txt .ufo/.../overlay/blocks/declared-blocks.txt
07e63e96c523871854bc675f2e105292afd2fb52fe551f4b79314c6e31f5cc5f  declared-blocks.txt
f982712d8e70aee8bd35c340e4a78b4d28bdba877739f862b3f0bbb7569bf17d  overlay/blocks/declared-blocks.txt
$ tail -n 2 PROVINCE.md | sha256sum   -> fa2dd99f...  (root declares 2 lines fa2dd99f: exact)
$ tail -n 1 PROVINCE.md | sha256sum   -> bd8dbc09...  (overlay declares 1 line bd8dbc09: pre-final)
$ tail -n 15 corpus/README.md | sha256sum -> bead673d...
$ tail -n 28 corpus/README.md | sha256sum -> a59d42cc... (root declares 28 a59d42cc: exact)
```
The overlay declares README 15 lines `f8f01dae…`, which matches no suffix of
`corpus/README.md` at HEAD — the overlay pack predates the final front-door appends.

### 2.4 Two `all-gates v3` receipts, one with unresolvable refs

```
$ cat .ufo/waves/round-39/final-gates/all-gates.txt | head -4
all-gates v3
export-ref=46c66c268502abd1b2c342fc71bf88ccf721845b
suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
run-utc=2026-10-26T21:35:00Z
$ head -4 .ufo/.../wave1/ExecSuiteBuild.overlay/all-gates.txt
all-gates v3
export-ref=f918ec4f8edae900f528f6d2daaab84ac425cc31
suite-sha256=2856a210...
run-utc=2026-10-26T21:10:00Z
$ git cat-file -t f918ec4f8edae900f528f6d2daaab84ac425cc31
fatal: git cat-file: could not get object info
$ git cat-file -t b3a3b06b5acb1c17d584636b70c9cbdc9e8b04fc
fatal: git cat-file: could not get object info
```
Payload drift between the two: G1 `corrections-outside=1` vs 0, G3 `added-quotes=1` vs 0,
G6 `r39=absent` vs `present`, G7 `rows=4` vs 7. The stale pair is quoted by
`overlay/{heads,MANIFEST,run-at-J,run-at-J-with-head,run-at-Y,selftest-at-Y}.*` and
`wave1/ExecSuiteBuild.md` §Runs; those transcripts are not replayable (refs absent) and
carry no `report-only` label, so the report must not cite them (R35,
`corpus/QUALITY.md:307`).

### 2.5 Wave-1 index vs HEAD bytes

Row-by-row re-verification of `wave1/ScribeWaveEvidence.index.md` (`da6a7e8b…`):
235 rows parsed; **233 match** bytes/lines/sha256; 2 do not —

```
ExecNoPlaceholderScan.md  index 12420 B / 263 lines / 08566ad1…  HEAD 14299 B / 293 lines / 02a022f0…
ScribeWaveEvidence.md     index  6644 B / 114 lines / 5383c906…  HEAD  6959 B / 120 lines / 56d41265…
```
Row-byte total 1,541,795 vs stated 1,539,601 (Δ 2,194). Both files were finalised in
`46c66c2`, the same commit that carries the index.

### 2.6 Overlay manifest integrity (control)

```
$ cd .ufo/waves/round-39/wave1/ExecSuiteBuild.overlay && sha256sum -c MANIFEST.txt
(24 entries, no failures)
```
The manifest is internally consistent; its defect is the two unresolvable head refs, not
its digests.

## 3. C1 counting commands: measured (report-only; not committed to `final-gates/`)

All runs use `TMPDIR=$S`, `--work $S/...` outside the lane, a clean `--scratch-root`.
Suite digest in every run: `2856a210…b4222b`.

```
# live lane (default --lane), base
closed=2/8 exit=1        G3 closed=1, G6 closed=1
# live lane, r38 judged head 66703acaaff50529a35be49aa8759d04140720ad
closed=2/8 exit=1
# live lane, J 46c66c2
G2 payload=receipt=0,...,scorecard-ref=1,shonen-ref=1 closed=0
G8 payload=...,r37-closed=0,r37-exit=1 closed=0
closed=6/8 exit=1
# live lane, Y 5006097
G8 payload=...,r37-closed=0,r37-exit=1 closed=0
closed=7/8 exit=1
# live lane, selftest at Y
selftest case=G8 positive=fail mutants=3/3 verdict=fail
selftest cases=8 failures=1  exit=1
# clean clone at Y (git clone --shared; rev-parse --show-toplevel = $S/clone; status 0 lines)
G8 payload=...,r37-closed=1,r37-exit=0 closed=1
closed=8/8 exit=0
selftest cases=8 failures=0  exit=0
# clean clone at J2
G2 payload=receipt=0,... closed=0
G8 payload=...,r37-closed=1,r37-exit=0 closed=1
closed=7/8 exit=1
# pinned r37 suite at Y against the live lane, showing the cause
E9 payload=status-read=ok,status-dirty=6,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=0
closed=13/14 exit=1
```

Reading: the live lane reds G8 only because the nested r37 suite's E9 reads the live
worktree (six untracked wave-2 paths) — a limit the instrument documents
(`corpus/instruments/r39-closure.sh:185-190`) but the frozen counting command and three
lane lines (`corpus/lessons/round-39.md:15`, `:76`, `SCORECARD.md:1567`) do not carry.
With a clean checkout at Y the claim reproduces exactly (`8/8`, `cases=8 failures=0`);
after the round's next commit it cannot (E9 `head-match` + G2 receipt-diff). These runs
are my own measurements, **report-only**, and are not offered as closure evidence for C1.

## 4. C2 counters re-measured from the tree (reproducible; no wave copy needed)

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                  -> 22
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        -> 59   (erratum E1)
$ grep -rlE '^source: S057' corpus/knowledge | wc -l                          -> 1
$ ls corpus/knowledge/*.md | wc -l                                            -> 51
$ python3 corpus/instruments/frontier-recheck-count.py
PASS     F22  knowledge/cisa-when-to-issue-vex.md   ids=S057   exit=0
entries=25 pass=25 exit=0
$ python3 corpus/instruments/capture-binding-check.py
AUDIT records=46 with_url=46 ... orphans=1 orphan=S040-live.txt
records=46 bound=46 unbound=0
$ python3 corpus/instruments/recheck-audit.py --quiet
lines=51 total=51 pass=51 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=51 missing=0 unexpected=0 exit=0
```

## 5. Findings (for the L1 / report)

- **F1 (depth:verifiability, record defect).** The C1 counting commands as frozen carry
  no `--lane`; run in the live lane they now print `closed=7/8 exit=1` at Y and
  `selftest cases=8 failures=1` (G8/E9 live-worktree limb, `status-dirty=6`). The claim
  holds only against a clean checkout at Y (measured `8/8`, `cases=8 failures=0`), and
  cannot be re-earned after the next commit. The report must state the precondition and
  label any live-lane quote `report-only`; `final-gates/all-gates.txt` records no lane
  state.
- **F2.** E4's "run at J prints 7/8" is 7/8 only in a clean clone at J2; the live lane
  prints 6/8 (G2 + G8). E4's number is correct under the same precondition it omits.
- **F3.** Two artifacts self-labelled `all-gates v3`; the `wave1/ExecSuiteBuild.overlay/`
  copy names `f918ec4f`/`b3a3b06b`, neither of which is an object in the lane, and its
  payloads differ from the canonical receipt. Its transcripts must not be quoted.
- **F4.** `wave1/ExecSuiteBuild.overlay/blocks/declared-blocks.txt` is a pre-integration
  declaration: README digest `f8f01dae…` matches no suffix at HEAD, PROVINCE declared at
  1 line where HEAD has 2. Only `.ufo/waves/round-39/declared-blocks.txt` is exact.
- **F5.** The wave-1 evidence index is stale in 2 of 235 rows (Δ 2,194 B); both files
  changed in the commit that carries the index.
- **F6.** 229,458 B of wave-1 artifacts are byte-identical to landed files or contained
  in them; only three `wave1/` paths are cited by landed files
  (`ExecSuiteBuild.md`, `ExecConsiderthese.scorecard.append.md`, `ExecScoreGap.gap.txt`),
  so the trimmed citable set can drop the rest without losing a fact.
- **F7.** The wave-2 live set already contains `final-gates/reds.txt` (untracked) whose
  summary `closed=1/8` at base and at the r38 head disagrees with the instrument's own
  output for those refs (`closed=2/8`, measured twice, and with the wave-1 committed
  transcripts). Its excerpt lists only G7/G8 payloads and no environment, so it cannot be
  reconciled as written; a red control that reds for an unrecorded environment reason is
  not a discriminating control.

## 6. Deliverable

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39/wave2/SimplArtifactTrim.trim.md`
(19,256 B): inventory, authority rule, T1–T6 duplication/supersession evidence, the
clean-checkout measurement, and the 14-row minimal evidence set (R1–R14) with hashes and
per-row justification, plus the do-not-drop list and the tradeoffs.

## 7. Hygiene

- No write outside `wave2/SimplArtifactTrim.md` and `wave2/SimplArtifactTrim.trim.md`;
  no lane/fleet/`shokuknow` file touched; no `git`/`jj` mutation in any existing repo
  (only `clone` + `checkout` inside `$S/clone`, whose toplevel was asserted).
- No tool installed, no `pacman` run; no host service touched.
- Scratch `/fast/scratch/hyaku/kasegi-r39/SimplArtifactTrim/` removed after the
  deliverable was written (work dirs, clone, run logs).
- Peer coordination: none needed (read-only item); no message to `agent://all`.
