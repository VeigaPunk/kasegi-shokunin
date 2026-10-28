# ExecSuiteCore — round-42 C1 `corpus/instruments/r42-closure.sh` (J1–J13)

Seat **ExecSuiteCore** (executor, leaf). Lane `kasegi-shokunin`. Base
`5053a7f46de35784cff4b56756906e9014a38276`. Lane tip at the final run
`29061f64065dcd5b60f713f1f48892866629974e`. Judge axes: `depth:verifiability`
(claim C1), `coverage` (C2, not this seat).

Nothing was installed; no network fetch was made; no pacman transaction was run.
Scratch `/fast/scratch/hyaku/kasegi-r42/ExecSuiteCore` is removed before yield.

## Deliverables (written beside this receipt)

| file | lines | sha256 |
|---|---|---|
| `ExecSuiteCore.r42-closure.sh` (landable suite, byte-exact) | 2142 | `d92c0de1e3b4d01ca330994c781fda6aeb0cfd874f00f6d17641c3f6bc73f464` |
| `ExecSuiteCore.transcripts.txt` (teed observed runs) | 95 | `67d4baf50a670d7b0cb5163bdf6b591f25a16d17458bdcef194dd1e385f6f8a7` |

The suite is self-contained: `bash` + `python3` + coreutils + `git` and `tar`
for the export only. No network. One file, no `source` of any sibling seat
artifact — a closure suite that has to fetch its own limbs cannot be replayed
from an export.

## 1. Shape (the C1 predicate, implemented literally)

* **Export mode only.** `--export-ref <hash>` is mandatory. A plain run prints
  `r42-closure: a plain run is refused (export mode only)` on stderr and exits
  2. The tree is extracted with
  `git -C <lane> archive <resolved> | tar -x -C <work>/export`; `<work>`
  defaults to `<scratch-root>/r42-<ref12>/work`, outside the lane.
* **Unresolvable ref is a red, not a pass.** `rev-parse --verify --quiet
  "<ref>^{commit}"` failing prints
  `ERROR ref-not-found ref=<arg> closed=0 exit=1` and exits 1.
* **Run transcript** (19 lines, stdout):
  five header lines (`all-gates v2`, `export-ref`, `suite-sha256`,
  `time-basis=ref-commit`, `run-utc`), thirteen `J<n> payload=... closed=0|1`
  lines in J1..J13 order, then `closed=<n>/13 exit=0|1`.
* **Receipt** (`--receipt-out PATH`): the same 19 lines followed by the
  thirteen `selftest case=J<n> ...` lines and `selftest cases=13 failures=<k>`
  — 33 lines, the teed transcript of run + selftest. `run-utc` is the
  committer instant of the named ref, never wall-clock.
* **`--selftest --export-ref <hash>`** prints only the thirteen graded lines
  plus `selftest cases=13 failures=<k>` (14 lines) and exits 0 only on zero
  failures.

## 2. The thirteen checks and the replay limb each carries

Every J1–J7 carries a REPLAY limb inline: it re-executes its family's
**committed** defeat artifact, bound by digest, against the current suite bytes,
and requires rejection. An artifact whose bytes are not the pinned commit is
reported `artifact-missing:<name>` and the limb fails — a missing defeat cannot
be graded as repaired.

| J | family | what it measures | committed defeat replayed (sha256-pinned) | green at HEAD |
|---|---|---|---|---|
| J1 | F-EVID | every `Correction (round <n>)` line in SCORECARD/LOG/SHONEN names a resolvable evidence id **per line**, plus `union=0`; never a cross-record tally | `.ufo/waves/round-41/wave2/RevC1Counters.md` | no |
| J2 | F-TOKEN | `closed=`/`failures=`/`cases=` read whole-token (10 boundary probes), no mangled tally in a round-42 correction, suite tally round-trips | `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` | yes |
| J3 | F-TABLE | SKILL.md registry: `r42-closure.sh` row present exactly once, `r40-closure.sh` once and inside a table, no bare-pipe/leading-space/off-width rows | `.ufo/waves/round-41/wave2/MutSkillTablePipes.md` | yes |
| J4 | F-DECL | `declared-blocks.txt` declares every export path the suite reads (11), every declaration resolves inside the export root, no symlink escape | `.ufo/waves/round-41/wave2/CritDeclarationCoverage.md` | no |
| J5 | F-SCAN | scratch hygiene on a materialized fixture: `kasegi-r4[0-9]*` (case/dot/underscore-normalised) inside and outside the configured root | `.ufo/waves/round-41/wave2/MutScratchTiming.md` | yes |
| J6 | F-BIND | `capture-binding-check.py --root <mutated corpus copy>` still green on the unmutated copy and **rejects** missing-path, URL-uppercased and mutated-`sha256` records | `.ufo/waves/round-41/wave2/MutBindingExistence.md` | yes |
| J7 | F-FLIP | `frontier-recheck-count.py --root <mutated copy>` still green unmutated and **rejects** a `status: admitted` flip and a `recheck: true` line | `.ufo/waves/round-41/wave2/MutFrontierParser.md` | yes |
| J8 | F-RCPT | the receipt: sentinel, 33 lines, named ref, `suite-sha256` equals the export's suite bytes, `time-basis=ref-commit`, `run-utc` equals the ref's committer instant, ref is an ancestor with only the receipt between it and the current ref, 13 run lines, 13 graded lines all `pass`, `cases=13 failures=0`, `closed=13/13 exit=0`, no stray lines, **12/12 deterministic payloads re-derived**, and six forgeries rejected | 6 in-memory forgeries | no |
| J9 | (negatives) | two nested depth-1 runs over base and the round-41 judged head must each report `closed<13/13` with a non-zero exit **and at least two tree-dependent reds** — a control red only because of the depth cap is refused (`neg_accept`) | the two refs themselves | yes |
| J10 | (isolation) | the thirteen selftest cases ran, each in its own removed fixture root, no canary token leaked into any payload, thirteen graded lines emitted | synthetic canary set | no |
| J11 | F-CORR | no `Correction (round <n>)` block duplicated verbatim unexcused; a `Correction-dedup` marker must name the record, the round, and every occurrence line, and must be appended after every pre-42 correction; no record ends inside a fence | in-place marker strip | yes |
| J12 | (no-harm) | `git diff --diff-filter=DR base..ref -- corpus/` is empty and `density.py` is byte-identical to its base blob (`ee803726…f54710`) | fixture git repo with a deleted corpus file | yes |
| J13 | (quiescence) | the export set equals `ls-tree -r` at the ref, the suite's own scratch root is named for the ref and holds no family-shaped leftover, and the lane index carries no skip-worktree/assume-unchanged marker | export-with-extra-file and clean replicas | yes |

## 3. Measured runs (transcripts file, quoted)

Lane tip `29061f64065dcd5b60f713f1f48892866629974e` — **9/13, exit 1**:

```
J1 payload=records=1,blocks=2,graded=1,evidence=1,missing=1,wrong-grade=0,per-record=SCORECARD.md=1/2;LOG.md=0;SHONEN.md=0,union=0,replay=RevC1Counters.md=rejected closed=0
J4 payload=declared=0,valid=0,missing=11,escape=0,coverage=0/11,file=absent,replay=CritDeclarationCoverage.md=no-substrate closed=0
J8 payload=receipt=(canonical),source=canonical,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=0,summary=0,closed-line=0,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6 closed=0
J10 payload=cases=13,isolated=13,canary=0,graded-lines=9,fixture=synthetic closed=0
closed=9/13 exit=1
```

`--selftest` at the same ref: `selftest cases=13 failures=4` — the four are
exactly J1, J4, J8, J10, and J8/J10 are downstream of the first two
(J8's canonical receipt cannot show thirteen passing graded lines while the
selftest has failures; J10 counts graded lines). Nine cases already read
`positive=pass payload-match=1`, and J8's forgery limb reads `mutants=6/6`.

Base `5053a7f4…` — **4/13, exit 1**. Red: J1 (no round-42 correction lines),
J2 (`stated=0`), J3 (`bare=5`, `r40-split=1`, no r42 row), J4, J6
(`digest-mutated=0`, replay accepted), J7 (`status-flip=0`, replay accepted),
J8, J10, J11 (`unexcused=4`, no marker). Green: J5, J9, J12, J13.

Round-41 judged head `1f74646…` — **3/13, exit 1**. Same set plus
`J12 closed=0` with `deleted=1`: the tree deletes
`corpus/lessons/round-41-verifier-spotcheck.md` relative to base, and the
no-harm guard catches it.

Both control refs satisfy `closed<13/13 exit=1` as the predicate requires.
Nested-run and ref-not-found behaviour is in transcript §5.

## 4. Why the receipt can be written at J and re-derived at Y

The Y ref is J + receipt only, so J8 is graded against a receipt that does not
exist at J. At J the reader grades a **canonical** transcript: the run lines of
this very run plus the selftest block it just produced. Since every check's
payload is a pure function of the exported tree (no wall-clock, no host path, no
`$TMPDIR`, no ref name — J13's payload deliberately drops the ref it was
measured at), the twelve deterministic payloads recorded at J re-derive
byte-identically at Y and `payload-match` is 12/12 on both sides. J8 alone is
excluded from that comparison; its own facts are receipt-internal.

## 5. Two landings still required for 13/13 (L1 action, measured)

Both are outside this seat's write scope. With them, J1, J4, J10 and J8 flip
green and the selftest reaches `cases=13 failures=0`.

1. **J1 — one evidence identifier on SCORECARD.md line 1632.** The
   `Correction (round 42)` at line 1632 names its subject in prose only
   (`D-r41-1 (self-defect, SCORECARD)`), so no resolvable identifier is present
   and `missing=1`. The repair is the record's own name with its extension:

   ```
   -Correction (round 42): D-r41-1 (self-defect, SCORECARD) is carried append-only …
   +Correction (round 42): D-r41-1 (self-defect, `SCORECARD.md`) is carried append-only …
   ```

   Line 1630 already names `0f64b8c5…` and `MutH6H10`, so it is green.

2. **J4 — land the declared-blocks file.** `.ufo/waves/round-42/declared-blocks.txt`
   does not exist. The seat deliverable
   `.ufo/waves/round-42/wave1/ExecJ4Decl.declared-blocks.txt` (324 lines) already
   declares all eleven paths J4 requires (`SCORECARD.md`, `LOG.md`, `SHONEN.md`,
   `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
   `corpus/instruments/{r42-closure.sh,capture-binding-check.py,
   frontier-recheck-count.py,density.py}` — verified by `awk '$1==p'`), so landing
   it at the path above is sufficient.

`corpus/lessons/round-42.md` is deliberately **not** in the required set: the
suite does not read it, and requiring an unread path would be a false
requirement.

## 6. Risks / what a falsifier should attack

* **J1's evidence rule is the strict one.** It accepts a resolvable path, a
  resolvable 40-hex commit, or a known defeat-artifact stem; it does not accept
  a bare word. A falsifier should try to pass a correction line by naming an
  unrelated-but-existing file — it passes, and so does the r41 design; the
  defect actually closed is the **union**: evidence stripped from one record's
  line reds it (`replay=RevC1Counters.md=rejected`, and the selftest mutant
  `mutants=1/1`).
* **J6's `digest-mutated` limb needs the patched**
  `corpus/instruments/capture-binding-check.py` (ExecJ6Bind) landed. It is
  green at the current tip, so the landing happened.
* **J7's `status-flip` limb needs the patched**
  `corpus/instruments/frontier-recheck-count.py` (ExecJ7Flip) landed — it is,
  and the census now reports `rows=25 admitted=25`.
* **J9 costs two nested exports per run** (~2×149 MB, ~100 s of the ~150 s
  total). That is the price of a negative control that is tree-red rather than
  cap-red; a cheaper variant would be the M-H8a defect again.
* **J13 reads the live lane index** for skip-worktree markers. It is 0 today; a
  lane that used that escape to hide a dirty file would red it.
* The suite never writes the lane, never commits, and removes nothing outside
  `<scratch-root>`; its own scratch root is `<scratch-root>/r42-<ref12>`.
