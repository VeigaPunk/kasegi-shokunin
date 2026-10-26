# ExecSuiteBuild — round-39 receipt (C1 depth:verifiability)

seat: ExecSuiteBuild (leaf executor; no spawns, one scratch dir, no lane writes)
lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `480b1a50`, claims freeze `dcd31701`)
axis: depth:verifiability
item: build the complete `corpus/instruments/r39-closure.sh` for frozen claim C1

## Deliverable

| path | lands at | lines | bytes | sha256 |
|---|---|---:|---:|---|
| `.ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh` | `corpus/instruments/r39-closure.sh` | 1793 | 75170 | `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` |

The file is bash-clean (`bash -n`), shellcheck-clean at `-S warning`, contains no `2>/dev/null`,
and contains none of the round's placeholder tokens: a grep for the pending-marker prefix, the
angle-bracket fill markers, the L1-fill phrase, the lane-hash marker, the round-marker prefix and the
bare placeholder words returns 0 hits on both the script and this receipt. Land it unchanged: G2's
`export-suite` and `digest-match`
limbs bind the receipt to these exact bytes, so a post-landing edit reds G2.

Evidence pack: `.ufo/waves/round-39/wave1/ExecSuiteBuild.overlay/` (24 small files + `MANIFEST.txt`
with per-file sha256): the seven append blocks, `declared-blocks.txt`, the base-run transcript
(`reds.txt`), the dispatch/results pair, the v3 receipt, and every run transcript quoted below —
including the full r38-head red (`run-at-r38head.txt`) and the 37-character-ref refusal
(`run-at-r38head-37char.txt`).

## 1. What the suite does

Export mode only. `--export-ref <hash>` extracts `git -C <lane> archive <hash> | tar -xf -` into
`<work>/export`; a plain run exits 2. Flags: `--export-ref`, `--selftest`, `--lane`, `--work`,
`--scratch-root`, `-h`. `--work` is refused inside the lane (before creating anything), and its
`export/`, `mut/`, `r37/`, `r37-pinned/` subdirectories are cleared on every run. All git reads use
`--no-optional-locks`; the only live reads are G6's scratch scan and the ref-scoped git limbs
(G1 numstat, G2 ancestry/diff, G3 added lines, G8 `git show`).

| check | reads | passes only when | reopens (RED) when |
|---|---|---|---|
| G1 | `.ufo/waves/round-39/declared-blocks.txt`, `PROVINCE.md`, `corpus/README.md`, `git diff --numstat BASE REF` | every declaration binds `tail -n <lines>` sha, `lines` == the path's added-line count, deleted == 0, path plain-relative and present in the export, ≥1 line per front door, backtick+tilde fence walks CLOSED at EOF, 0 corrections inside fences, every `Correction (round 39)` inside its declared tail | partial tail, sha flip, tilde opener closed by backticks, correction inside a fence, `../` declaration, missing door, non-append edit |
| G2 | `.ufo/waves/round-39/final-gates/all-gates.txt`, `SCORECARD.md`, `SHONEN.md`, the export's own suite copy | header `all-gates v3`; one `export-ref=<40hex>` that exists, is ancestor-or-equal of REF, and whose post-receipt diff is only the receipt; one `suite-sha256` equal to both the executing bytes and the export copy; eight distinct `G<n> ... closed=1`, zero `closed=0`; `closed=8/8 exit=0`; eight GRADED case lines (both `positive=pass` and `verdict=pass` present), zero ungraded case lines; one `selftest cases=8 failures=0`; SCORECARD `## Round 39` and SHONEN round-39 lines carry the judged-head phrase and zero `Final lane commit:` | v2 header, self-naming/forged receipt, extra file after the receipt, digest mismatch, summary-only case line, `verdict=fail`, 7 cases, final-label line |
| G3 | added (`+`) lines of `git diff BASE REF` over SCORECARD/SHONEN/LOG/round-38.md, `.ufo/waves/round-39/final-gates/` | every added line quoting a run (`closed=` + `--export-ref <hex>`) is either labeled `report-only` on that line or names a ref that appears in a committed transcript under round-39/final-gates | a quote with no transcript and no label; a ref stored outside the transcript dir |
| G4 | `.ufo/waves/round-39/*-dispatch.json` + paired results | ≥1 dispatch; results parse; entries == `len(taskCall.tasks)`; identity field (`id`,`name`,`seat`,`agent`, first present in every entry) is distinct; wave fields agree; zero-task dispatch RED | missing results, duplicate identity, short count, zero tasks, unparseable JSON, wave mismatch |
| G5 | SCORECARD `## Round 39` section + whole file | section present, zero `Final lane commit:`, ≥1 line beginning `Correction (round 39)` naming `f06148c6` and labeled `report-only` | final label, missing correction, unlabeled correction, missing section |
| G6 | LIVE scratch root (not export), fail-closed | `kasegi-r37`/`kasegi-r38` absent-or-empty; `kasegi-r39` absent or holds only this run's `--work` (or a clean chain toward it); unreadable dir RED | leftover file/dir/symlink, residual sibling under the tolerated parent, unreadable root |
| G7 | `corpus/knowledge/considerthese-proposals-ledger.md` | `## Round-39 dispositions (appended 2026-10-26)` after the round-38 section, a `Correction (round 39)` line, ≥3 numeric-first-cell rows including 1 and 3 | section before round-38, missing row, missing correction |
| G8 | `git show 2387dcf6:corpus/instruments/r37-closure.sh`, the export's r37 copy, the pinned run | pinned bytes hash to `PIN_R37_SHA`, export copy hash matches BEFORE trust, run `--export-ref REF --lane LANE --work <work>/r37` ends `closed=14/14 exit=0` and exits 0 | mutated/absent export copy, pinned run red (e.g. lane HEAD ≠ REF) |

## 2. Runs (actual output)

### 2.1 syntax + static check

```
$ bash -n r39-closure.sh && shellcheck -S warning r39-closure.sh && echo CLEAN
CLEAN
```

### 2.2 plain run

```
$ bash r39-closure.sh
r39-closure: refusing to run against the live worktree: this suite is export-mode only.
r39-closure: pass --export-ref <hash> (see --help) or --selftest.
plain-exit=2
```

### 2.3 base export `480b1a50…` — required red

`bash r39-closure.sh --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a --work <scratch>/work/base
--scratch-root <clean dir>` → `exit=1`:

```
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

G3 is green at base because base adds no quoting line (the check's scope is this round's added
quotes); G6 is green only with a clean `--scratch-root`.

### 2.4 r38 judged head — required red (both spellings)

```
$ bash r39-closure.sh --export-ref 66703acaaff50529a35be49aa8759d04140720ad --work <scratch>/work/r38head ...
G1 … closed=0   G2 … closed=0   G3 … closed=1   G4 … closed=0
G5 … closed=0   G6 … closed=1   G7 … closed=0   G8 … closed=0
closed=2/8 exit=1
```

The 37-character spelling in the frozen claim text does not resolve in the lane, so it is a harness
error, not a red run — this is claims erratum E2 (`.ufo/waves/round-39/claims-erratum-1.md`, real head
`66703acaaff50529a35be49aa8759d04140720ad`):

```
$ bash r39-closure.sh --export-ref 66703aca50529a35be49aa8759d04140720ad ...
r39-closure: cannot resolve export ref in /home/vgpnk/Projects/shokunin/kasegi-shokunin: 66703aca50529a35be49aa8759d04140720ad
exit=2
```

### 2.5 the live scratch limb (G6) is live

Same base export, but WITHOUT `--scratch-root` (so the real `/fast/scratch/hyaku` is scanned while
wave-1 seats are still running) → `closed=1/8 exit=1`, and G6 names the residual:

```
G6 payload=r37=absent,r38=absent,r39=present,work=inside,tolerated=none,read=ok closed=0
```

`r39=present` is the live `/fast/scratch/hyaku/kasegi-r39` tree that seats (this one included) must
remove before closure. At the judged head the L1 must run G6 with the real root after the seats'
scratch is gone, or with a `--scratch-root` that holds only its own `--work`.

### 2.6 `--selftest` at base — 8 graded case lines, every mutant rejected, positives honestly red

`bash r39-closure.sh --selftest --export-ref 480b1a50… --work <scratch>/work/selftest-base
--scratch-root <clean>` → `exit=1`:

```
selftest case=G1 positive=fail mutants=4/4 verdict=fail
selftest case=G2 positive=fail mutants=8/8 verdict=fail
selftest case=G3 positive=pass mutants=2/2 verdict=pass
selftest case=G4 positive=fail mutants=6/6 verdict=fail
selftest case=G5 positive=fail mutants=4/4 verdict=fail
selftest case=G6 positive=pass mutants=4/4 verdict=pass
selftest case=G7 positive=fail mutants=3/3 verdict=fail
selftest case=G8 positive=fail mutants=3/3 verdict=fail
selftest cases=8 failures=6
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
selftest judge=forged-no-verdict rejected=1
```

Every one of the 34 mutants was rejected on its named limb at base (no `rejected=0` line). The six
red positives are the base tree's own defect state, reported honestly (G3/G6 pass because base adds
no quote and the scratch root was clean).

### 2.7 overlay: the same suite is GREEN on a head that carries the round's evidence

Scratch fixture repository (base = lane base; `git rev-parse --show-toplevel` asserted equal to the
fixture dir before every commit; fixture identity only), with J' = base + the round-39 landing shape
(the seven append blocks, `declared-blocks.txt`, the suite at its real path, dispatch+results, the
base-run transcript) and Y' = J' + the receipt only:

```
J=f918ec4f8edae900f528f6d2daaab84ac425cc31
Y=b3a3b06b5acb1c17d584636b70c9cbdc9e8b04fc
$ git -C <fixture> diff --name-only J Y
.ufo/waves/round-39/final-gates/all-gates.txt
```

`--export-ref Y` (lane HEAD = Y, clean tree) → `exit=0`:

```
G1 payload=declared=2,valid=2,front-doors=2,tail-match=2,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=1,corrections-inside=0,corrections-declared=1,diff-read=ok closed=1
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,diff-read=ok,digest-match=1,export-suite=1,run-lines=8,closed-lines=0,distinct-ids=8,closed-line=1,graded-cases=8,ungraded-cases=0,selftest-summary=1,scorecard-ref=1,shonen-ref=1,final-lane-commit=0 closed=1
G3 payload=added-quotes=1,covered=1,uncovered=0,report-only=0,diff-read=ok closed=1
G4 payload=dispatches=1,pairs=1,seats-ok=1,zero-task=0,read=ok closed=1
G5 payload=round39-section=1,final-lane-commit=0,correction=1,correction-labeled=1 closed=1
G6 payload=r37=absent,r38=absent,r39=absent,work=outside,tolerated=none,read=ok closed=1
G7 payload=section=1,after-round38=1,correction=1,rows=4,proposal-1=1,proposal-3=1 closed=1
G8 payload=pin-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=1,r37-exit=0 closed=1
closed=8/8 exit=0
```

The receipt committed at Y carries those exact G lines (byte-identical to the live run — verified by
`diff`), `export-ref=J`, `suite-sha256=2856a210…`, and the eight graded case lines:

```
all-gates v3
export-ref=f918ec4f8edae900f528f6d2daaab84ac425cc31
suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
run-utc=2026-10-26T21:10:00Z
…
== selftest ==
selftest case=G1 positive=pass mutants=4/4 verdict=pass
… (G2 8/8, G3 2/2, G4 6/6, G5 4/4, G6 4/4, G7 3/3, G8 3/3)
selftest cases=8 failures=0
```

`--selftest --export-ref Y` (same fixture) → `exit=0`:

```
selftest case=G1 positive=pass mutants=4/4 verdict=pass
selftest case=G2 positive=pass mutants=8/8 verdict=pass
selftest case=G3 positive=pass mutants=2/2 verdict=pass
selftest case=G4 positive=pass mutants=6/6 verdict=pass
selftest case=G5 positive=pass mutants=4/4 verdict=pass
selftest case=G6 positive=pass mutants=4/4 verdict=pass
selftest case=G7 positive=pass mutants=3/3 verdict=pass
selftest case=G8 positive=pass mutants=3/3 verdict=pass
selftest cases=8 failures=0
selftest judge=own-report accepted=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
selftest judge=forged-no-verdict rejected=1
```

Final identity check, executing the LANDED path (not the scratch copy) against the same fixture —
the digest binding is path-independent:

```
$ bash .ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh --export-ref <Y> --lane <fixture> …
closed=8/8 exit=0
$ bash .ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh --selftest --export-ref <Y> … | grep -E '^selftest |suite-sha256'
selftest export-ref=b3a3b06b5acb1c17d584636b70c9cbdc9e8b04fc … suite-sha256=2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b
selftest case=G1 positive=pass mutants=4/4 verdict=pass
… (G2 8/8 … G8 3/3)
selftest cases=8 failures=0
```

## 3. Selftest coverage — 34 single-defect mutants, 4 green controls

| check | controls (must be accepted) | mutants (must be rejected, by limb) |
|---|---|---|
| G1 | whole-tail-green (`declared=2,valid=2,tail-match=2`) | declared-short-of-added → `valid=0`; tilde opener closed by backticks → `readme-fence=open`; correction inside a fence → `corrections-inside=1`; `../` declaration → `paths=0` |
| G2 | (positive = shipped export) | sentinel v2 → `sentinel=0`; digest mismatch → `digest-match=0`; summary-only case line → `graded-cases=0`; `verdict=fail` case → `graded-cases=7`; 7 graded cases → `graded-cases=7`; `Final lane commit:` in section → `final-lane-commit=1`; export-ref on a side branch → `ancestor=0`; extra file after the receipt → `diff-clean=0` |
| G3 | quoted-run-transcribed (covered=1) | quote without transcript → `uncovered=1`; ref stored outside final-gates → `uncovered=1` |
| G4 | (positive = shipped export) | results absent → `pairs=0`; duplicate identity → `seats-ok=0`; short count → `seats-ok=0`; zero-task dispatch → `zero-task=1`; unparseable results → `pairs=0`; results wave mismatch → `pairs=0` |
| G5 | (positive = shipped export) | final label in section → `final-lane-commit=1`; correction absent → `correction=0`; correction without `report-only` → `correction-labeled=0`; section absent → `round39-section=0` |
| G6 | own-work-dir accepted; nested clean chain accepted | r37 leftover file → `r37=present`; r38 residual seat → `r38=present`; r39 sibling under the tolerated parent → `r39=present`; chmod-000 root → `r37=unreadable` |
| G7 | (positive = shipped export) | proposal 3 row absent → `proposal-3=0`; correction absent → `correction=0`; section before round-38 → `after-round38=0` |
| G8 | (positive = shipped export) | export copy with an appended mutation line → `export-copy=0`; copy absent → `r37-copy=0`; pinned run over a ref that is not the lane HEAD → `r37-closed=0` |

The G2 history mutants run in a fixture repo whose toplevel is asserted; the G1/G3 history mutants
share one fixture repo fetched `--no-tags` at `BASE_REF` and reset with `checkout -f` per mutant, so
each mutant commit's parent is the base and its diff is single-defect.

## 4. The green window, measured (this is the round's R1/M39-1 hazard)

| export-ref | lane HEAD | printed | why |
|---|---|---|---|
| J' = `f918ec4f…` | J' | `closed=7/8 exit=1` | G2 RED: the receipt cannot exist at the commit it names |
| J' = `f918ec4f…` | Y' | `closed=6/8 exit=1` | G2 RED, plus G8 RED (the r37 suite's E9 head-match needs HEAD == REF) |
| Y' = `b3a3b06b…` | Y' | `closed=8/8 exit=0` | the receipt exists, names J', and `diff J..Y` is the receipt only |

The suite states this in its header. The frozen C1 counting command says "over J"; a commit cannot
contain its own hash, so the honest 8/8 run is over the tip Y = J + receipt. The L1's records should
quote the run by reference (`export-ref of .ufo/waves/round-39/final-gates/all-gates.txt`) rather than
by a hash it cannot know at J, or the G3 transcript limb will demand a transcript for a hash that
does not exist yet.

## 5. Landing requirements (what the judged head must carry for 8/8)

Derived from the checks and the measured overlay; each is a byte-level constraint on the L1's commit:

1. `corpus/instruments/r39-closure.sh` lands byte-identical to the deliverable (`sha256 2856a210…`);
   `.ufo/waves/round-39/declared-blocks.txt` declares **each front door's whole appended tail**
   (`<path> <added-lines> <sha256-of-that-tail>`, added lines from `git diff --numstat 480b1a50 J`),
   paths plain-relative, both fence walks closed, and any `Correction (round 39)` line outside a fence
   and inside the declared tail.
2. `.ufo/waves/round-39/final-gates/all-gates.txt` starts `all-gates v3`, carries `export-ref=J`
   (40 hex, ancestor of Y, `diff J Y` = this file only), `suite-sha256=<executing digest>`, the eight
   `G1..G8 payload=… closed=1` lines, `closed=8/8 exit=0`, exactly eight **graded** `selftest case=G<n>
   … positive=pass … verdict=pass` lines and `selftest cases=8 failures=0`.
3. SCORECARD `## Round 39` section and SHONEN's round-39 lines carry
   `judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt` and no `Final lane
   commit:` line. SCORECARD carries `Correction (round 39): … f06148c6 … report-only …` (the words
   `f06148c6` and `report-only` are required).
4. Every run quoted in an **added** line of SCORECARD/SHONEN/LOG/round-38.md (a `closed=` line that
   also names `--export-ref <hex>`) needs its ref in a committed file under
   `.ufo/waves/round-39/final-gates/` or the literal `report-only` on that line. Quoting the positive
   run by reference, and committing `reds.txt` for the base/prior-head runs, satisfies this; the
   overlay does exactly that.
5. Every tracked `.ufo/waves/round-39/*-dispatch.json` needs a paired results file (`<base>-results.json`
   or `<wave>-results.json` with the same `wave`) listing exactly `len(taskCall.tasks)` seats whose
   `name` values are distinct — including any wave-2 dispatch written this round. Probe on the real
   files: `g4_pair(.ufo/waves/round-39/wave1-dispatch.json, .ufo/waves/round-38/kasegi-r38-build-results.json)`
   → `tasks=49`, `ident=name`; `g4_pair(round-38 dispatch, round-38 results)` → `tasks=73,results=73,ident=name,distinct=1`.
6. `corpus/knowledge/considerthese-proposals-ledger.md` gets `## Round-39 dispositions (appended
   2026-10-26)` after `## Round-37 dispositions — filled (round 38)`, a `Correction (round 39)` line,
   and ≥3 numeric-first-cell rows including proposals 1 and 3 (the draft block in
   `ExecConsidertheseLedger` is enough if it keeps those).
7. G6 is LIVE: at the run, `/fast/scratch/hyaku/kasegi-r37` and `kasegi-r38` absent-or-empty and
   `kasegi-r39` holding only the run's own `--work` (or nothing, when `--work` is elsewhere). Any
   surviving seat dir — this seat's included — reds it.
8. G8 needs the lane checked out at the run's ref with a clean tree (the pinned r37 suite's E9 limbs
   are live), and the pin commit `2387dcf6` reachable; pinned digest
   `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` (measured via
   `git show 2387dcf6:corpus/instruments/r37-closure.sh | sha256sum`).

## 6. Limits and named risks (documented in the suite header, not hidden)

- **G3 scope.** It reads the files this round ADDS to (base lines are exempt: a prior round's quote
  is not this round's debt) and requires a `--export-ref <hex>` token, so a quote that names its head
  only as "J" is out of scope. File-wide application would red on pre-round-39 quoted runs whose refs
  have no committed transcript anywhere (`SCORECARD.md:1434` `3266c993…`, `:1494` `274fa9ae…`/`0aee0ef…`,
  `:1505` `aa88877bf9…`; `SHONEN.md:176` `aa88877bf9…`; the r37 receipt names `9492c776…`, not
  `aa88877b…`). That is the historical R3 class, recorded, not silently greened: an honest head cannot
  re-transcribe a run it did not take, and the round-38 lesson already records it.
- **G1's fence model** is the contract's spelling (three-character openers with an optional info
  string, three-character closers plus blanks, backtick and tilde); a four-backtick closer does not
  close. A mid-paragraph `Correction (round 39)` is not counted (so it cannot red the inside-fence
  limb). Corrections of earlier rounds are out of scope.
- **G2 accepts ancestor-or-equal** (as the frozen predicate says), so `export-ref == REF` passes with
  a vacuous diff; the receipt's binding to a *run* is the `suite-sha256` + export-copy limbs and G3's
  transcripts, not a payload-value comparison against a live run. Absolute paths in a declaration are
  rejected; a doubled declaration is validated twice.
- **G4** resolves identities by exact string; a results file listing the right number of distinct
  WRONG seats is not caught (the dispatch is the authority for names).
- **G6** does not audit the contents of `--work` (the caller's own space); it audits the scratch root.
- **G8** executes the pinned r37 suite, whose live limbs (worktree, HEAD, scratch) must be satisfied
  by the caller's environment.

## 7. Tooling and scratch

No tool was installed or upgraded for this seat (bash, awk, sed, grep, sha256sum, git, python3 and
the already-present `/usr/bin/shellcheck` covered it). No pacman transaction was run. No lane file
outside the deliverable, the receipt and the evidence pack was written; no mutating git command was
run in the lane (fixtures only, with the toplevel assertion above). Scratch
`/fast/scratch/hyaku/kasegi-r39/ExecSuiteBuild` was removed after the copies, so G6 sees no
`ExecSuiteBuild` entry.

## Report

Files: `.ufo/waves/round-39/wave1/ExecSuiteBuild.r39-closure.sh` (deliverable),
`.ufo/waves/round-39/wave1/ExecSuiteBuild.overlay/` (evidence), this receipt.
