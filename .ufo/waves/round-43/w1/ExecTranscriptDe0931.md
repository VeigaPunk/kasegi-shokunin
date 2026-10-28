# ExecTranscriptDe0931 — round-43 evidence: `r42-closure.sh` teed transcript at `de09313`

Seat **ExecTranscriptDe0931** (executor, leaf). Lane `kasegi-shokunin`, base
`ab98fac9dce87130bc4f66de89e30650d63943dc`. Frozen claims
`.ufo/waves/round-43/claims.json` read first, never edited. Nothing was
installed, no network fetch, no pacman, no mutating git command anywhere.
Scratch `/fast/scratch/hyaku/kasegi-r43/ExecTranscriptDe0931` is removed before
yield.

Pinned ref (from the seat spec, not substituted):
`de09313e8edb98280b19767d0094bb2dd8031d73` — "round-42: remove poisoned
w2.ready (pointed at spec without taskCall; orchestrator hygiene)",
committer instant `2026-10-28 11:08:59 -0300`.

## 0. Deliverable (byte-exact tee, nothing else in the file)

| file | bytes | lines | sha256 |
|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecTranscriptDe0931.txt` | 2974 | 33 | `8c3f9dd553fe24e88689c07c036f11510fa08d5f6016a71e7533013c2ba10302` |

The L1 lands it at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`. No
header line, no edit, no appended note: first line `all-gates v2`, last line
`selftest cases=13 failures=1`, final byte LF, zero CR bytes. `tee` wrote the
wave path directly; no copy, no `sed`, no post-processing.

## 1. Ref resolution, exact commands, exit codes

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --verify 'de09313e8edb98280b19767d0094bb2dd8031d73^{commit}'
de09313e8edb98280b19767d0094bb2dd8031d73
rc=0
```

The captured pipeline (one tee, two invocations, in the suite's print order —
`--selftest` is a separate mode in `main()` and prints only its 14-line block,
so "run both" cannot be one engine mode):

```
S=/fast/scratch/hyaku/kasegi-r43/ExecTranscriptDe0931
I=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r42-closure.sh
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
R=de09313e8edb98280b19767d0094bb2dd8031d73
D=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecTranscriptDe0931.txt
cd "$S"; export TMPDIR="$S"
{
  bash "$I" --export-ref "$R" --lane "$L" --work "$S/w" --scratch-root "$S"
  printf '%s\n' "$?" > "$S/rc-run.txt"
  bash "$I" --selftest --export-ref "$R" --lane "$L" --work "$S/ws" --scratch-root "$S"
  printf '%s\n' "$?" > "$S/rc-selftest.txt"
} 2>&1 | tee "$D"
```

Observed:
- run exit **1** (`run_exit=1`);
- `--selftest` exit **1** (`selftest_exit=1`);
- pipeline wall **464 s**, deliverable `bytes=2974 lines=33`;
- stdout and stderr merged into one fd before `tee`. In a pre-flight probe of the
  same run with streams captured separately, stderr was 0 bytes, and the 33
  captured lines all parse as the suite's stdout shape, so the merged fd adds
  nothing.

Exit-code capture writes to `$S/rc-run.txt` / `$S/rc-selftest.txt` (outside the
tee), never into the transcript.

## 2. What the transcript contains (verbatim)

Lines 1-5 header, 6-18 `J1`..`J13`, line 19 tally, lines 20-32 selftest cases,
line 33 summary:

```
all-gates v2
export-ref=de09313e8edb98280b19767d0094bb2dd8031d73
suite-sha256=d92c0de1e3b4d01ca330994c781fda6aeb0cfd874f00f6d17641c3f6bc73f464
time-basis=ref-commit
run-utc=2026-10-28T14:08:59Z
...
J8 payload=receipt=.ufo/waves/round-42/final-gates/all-gates.txt,source=committed,sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=0,run-lines=1,selftest-lines=1,verdicts=0,summary=0,closed-line=0,no-stray=1,payload-match=0,forged=1,payload-match=9/12,forged=6/6 closed=0
...
closed=12/13 exit=1
selftest case=J1 mutants=1/1 positive=pass payload-match=1 verdict=pass
...
selftest case=J8 mutants=6/6 positive=fail payload-match=1 verdict=fail
...
selftest case=J13 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=13 failures=1
```

Twelve checks close. **J8 (receipt integrity) is open at this ref**, and the
selftest's J8 positive arm fails for the same reason. Every K1-K13 replay limb in
the transcript is `rejected` (J1 `RevC1Counters.md=rejected`, J2
`RevC1Counters.defeats.txt=rejected`, J3 `MutSkillTablePipes.md=3/3`, J4
`CritDeclarationCoverage.md=2/2`, J5 `MutScratchTiming.md=outside=detected,inside=detected`,
J6 `MutBindingExistence.md=rejected`, J7 `MutFrontierParser.md=rejected`).

## 3. Why J8 is open at `de09313` (measured, not inferred)

The committed receipt at that ref is stale and self-declares a red run:

```
$ git show de09313:.ufo/waves/round-42/final-gates/all-gates.txt | sed -n '1,5p;/^closed=/p;/^selftest cases=/p'
all-gates v2
export-ref=d238e36c28d73d1e76002a6943baaa9616917c31
suite-sha256=d92c0de1e3b4d01ca330994c781fda6aeb0cfd874f00f6d17641c3f6bc73f464
time-basis=ref-commit
run-utc=2026-10-28T12:55:59Z
closed=9/13 exit=1
selftest cases=13 failures=4
```

J8's facts follow mechanically:
- `ref` names `d238e36`, two commits behind the graded ref; the `diff` fact allows
  at most one changed file (the receipt itself):
  `git diff --name-only d238e36..de09313 | wc -l` = **5**
  (`.ufo/waves/round-42/final-gates/all-gates.txt`, `wave1/ExecSuiteCore.md`,
  `wave1/ExecSuiteCore.r42-closure.sh`, `wave1/ExecSuiteCore.transcripts.txt`,
  `wave2-dispatch.json`) → `diff=0`.
- the receipt's own lines record 9/13: `verdicts=0` (four `verdict=fail`),
  `summary=0` (expects `(13,0)`, reads `(13,4)`), `closed-line=0` (expects
  `(13,13,0)`, reads `(9,13,1)`), `payload-match=9/12` (J1, J4, J10 payloads in
  the receipt no longer match the live ones).
- It is **the ref's own state, not the r43 hardening**: the instrument committed
  *at* `de09313` (sha256 `d92c0de1…`, the exact `suite-sha256` printed in the
  transcript) run at `de09313` prints
  `closed=10/13 exit=1` with the same J8 facts
  (`...diff=0,...,verdicts=0,summary=0,closed-line=0,payload-match=10/12,forged=6/6 closed=0`),
  rc=1, wall 169 s. The historical control ran from a scratch copy of
  `git show de09313:corpus/instruments/r42-closure.sh`.
- The selftest's `J8 ... positive=fail` is the same defect seen from the positive
  arm: the unmutated receipt at this ref is already defective, so a check that
  grades it cannot pass there. Twelve of thirteen graded cases pass; only J8 fails.

Context, no substitution made: the lane's later r42 commits carry a green
receipt — `b2c49ea` (committer instant `12:15:28 -0300`) commits
`closed=13/13 exit=0` / `selftest cases=13 failures=0` minted at
`J=4c40ef2`, and `de09313` is an ancestor of `4c40ef2`. The seat spec pinned
`de09313`; I captured that ref exactly and did not re-point the run.

## 4. Verification of the delivered bytes

```
$ wc -l -c D
  33 2974 D
$ sha256sum D
8c3f9dd553fe24e88689c07c036f11510fa08d5f6016a71e7533013c2ba10302  D
$ grep -c '^closed=' D
1
$ grep -n '^closed=' D
19:closed=12/13 exit=1
$ grep -c '^selftest case=' D
13
$ grep -c '^selftest cases=' D
1
$ head -c 20 D | od -An -c
   a   l   l   -   g   a   t   e   s       v   2  \n
$ tail -c 40 D | od -An -c
   r   d   i   c   t   =   p   a   s   s  \n   s   e   l   f   t
   e   s   t       c   a   s   e   s   =   1   3       f   a   i
   l   u   r   e   s   =   1  \n
$ tr -d '\n' < D | grep -c $'\r'
0
```

(The required content is present: one `closed=` tally — `closed=12/13 exit=1` —
thirteen `selftest case=` graded lines and one `selftest cases=13 failures=1`
summary.)

Determinism note, measured only where measured: `run-utc` is the pinned ref's
committer instant (`2026-10-28T14:08:59Z` = `11:08:59 -0300`), not wall clock,
and J5's counts come from a fixture the check materialises itself under
`--work` (`WORK/j5-fixture`), so neither field depends on when or where the run
happened. A second full tee was not produced and no byte-for-byte re-run
comparison was made; the two independent executions that were made (pre-flight
probe and the final pipeline) produced identical `J1`-`J13` payload text and
identical `closed=12/13 exit=1`.

## 5. Environment, hygiene, bounds

- Scratch `S=/fast/scratch/hyaku/kasegi-r43/ExecTranscriptDe0931`, `TMPDIR=$S`;
  exports under `$S/w/export` and `$S/ws/export`, historical control under
  `$S/hw/export`, probe under `$S/probe-w/export`. Removed before yield;
  verified `test ! -e $S` afterwards.
- Disk guard at start: `/fast/scratch/hyaku` 25% used, 607.3 G free; `/tmp` 17%
  used, 106.8 G free. All work trees live on `/fast/scratch`.
- The instrument was executed from the lane working tree
  (`corpus/instruments/r42-closure.sh`, sha256
  `fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b`, identical
  to lane `HEAD` `4cb6d4a`), while the transcript's `suite-sha256` line reports
  the **export's** instrument (`d92c0de1…`, `de09313`'s copy) because
  `suite_sha()` hashes `in_tree(SUITE_REL)` inside the export.
- No tooling installed or upgraded; no network fetch; no pacman; no mutating git
  (only `rev-parse`, `show`, `log`, `diff`, `merge-base --is-ancestor`, and the
  instrument's own read-only `git archive`).
- Writes: the deliverable and this receipt under
  `.ufo/waves/round-43/w1/`, plus scratch. `git status --porcelain` after the run
  is exactly `?? .ufo/waves/round-43/INTEGRATION-PLAN.md`,
  `?? .ufo/waves/round-43/w1-REGISTRY.txt`, `?? .ufo/waves/round-43/w1.ready`,
  `?? .ufo/waves/round-43/w1.ready.dispatched`, `?? .ufo/waves/round-43/w1/` —
  all untracked round-43 wave paths (dispatcher/sibling files; mine are the two
  `ExecTranscriptDe0931.*` entries inside `w1/`). `git diff --stat` over the
  tracked tree is empty: no tracked lane file was modified by this seat. Fleet
  root and `shokuknow` untouched.

## 6. Risks / what the L1 must decide before landing

- **The pinned ref is red under its own suite** (`closed=12/13 exit=1`,
  `selftest cases=13 failures=1`, J8 open). If `final-gates/r42-at-de09313.txt`
  is meant to be green "r42 closed" evidence, this pin does not support that
  reading; the green r42 receipt lives at `b2c49ea` (J=`4c40ef2`). I did not
  substitute a ref — the assignment forbade it — so the landed file will show the
  red. If the L1 wanted the green r42 state, a new dispatch must pin the ref that
  actually mints it.
- The two instrument hashes differ by design (`suite-sha256` = export copy,
  executing copy = lane HEAD). A later reader comparing either to the current tip
  must use the matching one; both are recorded above.
- Nothing in the deliverable may be re-typed or re-headed: it is the raw tee, and
  its sha256 above is the contract for landing.
