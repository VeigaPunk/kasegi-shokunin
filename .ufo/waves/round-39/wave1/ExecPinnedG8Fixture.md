# ExecPinnedG8Fixture — G8' pinned-bytes fixtures (round 39, wave 1)

Seat: `ExecPinnedG8Fixture`, executor, leaf. Axis: `depth:verifiability` (C1). Milestone: round-39.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat apart from the two
paths below). Base `480b1a505a2dfc14a4f718d16d63808247214d0a`, claims freeze
`dcd31701720a6a4929a32471a62011ed87103421`.

Deliverable: `.ufo/waves/round-39/wave1/ExecPinnedG8Fixture.fixtures/` (16 files, 169635 bytes).

## 1. What the limb requires

Frozen G8 (claims.json C1): the round-37 closure suite is carried forward only when **both** hold —

1. the export's `corpus/instruments/r37-closure.sh` hashes equal to the bytes
   `git show 2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh` returns;
2. the run of those **pinned** bytes ends `closed=14/14 exit=0` with exit 0.

The run is of the pinned bytes, never of the export copy: a copy that has been edited supplies no
verdict of its own. The fixtures pin the decision — inputs (pinned digest, export-copy digest,
recorded run) → the `G8 payload=… closed=…` line the suite must print — so the suite builder can
adopt the key set and the expected lines, and a later verifier can re-run the discrimination without
a lane.

## 2. (a) Extraction and pinned digest

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show \
    2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh > pinned/r37-closure.sh
$ sha256sum pinned/r37-closure.sh
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  pinned/r37-closure.sh
$ wc -lc < pinned/r37-closure.sh
   1558   73132
$ git -C <lane> rev-parse 2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh
68ac41e8fdab46ba508800a377f396e663f2a436
$ ( cd pinned && sha256sum -c sha256.txt )
r37-closure.sh: OK
```

The digest agrees with the committed round-37 gate receipt, which records the same
`suite-sha256=0da98e37…42434d` in `.ufo/waves/round-37/final-gates/all-gates.txt:3,7,25` — the
pinned bytes are the bytes that produced the round-37 `closed=14/14 exit=0`.

`pinned/` carries `r37-closure.sh` (the byte stream), `sha256.txt` (one `sha256sum` line),
`commit.txt` (`2387dcf6…`) and `path.txt` (`corpus/instruments/r37-closure.sh`).

## 3. Cases and expected lines

`expected/expected.txt` (the contract; one line per case):

```
positive -> G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,digest-match=1,r37-suite=1,r37-closed=1,r37-exit=0 closed=1
negative-mutated -> G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=4a5aea99d88d5750e43556a0501491a6c70443852abe09dbdecd7d0e71060483,digest-match=0,r37-suite=1,r37-closed=1,r37-exit=0 closed=0
negative-open -> G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,digest-match=1,r37-suite=1,r37-closed=0,r37-exit=1 closed=0
negative-absent -> G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=-,digest-match=0,r37-suite=0,r37-closed=0,r37-exit=1 closed=0
```

Decision rule (`fixtures.json`, `README.md`): `closed=1` iff `digest-match=1 AND r37-suite=1 AND
r37-closed=1 AND r37-exit=0`; `r37-closed=1` iff the transcript's last non-empty line is exactly
`closed=14/14 exit=0`.

| case | (b)/(c)/(d) | export copy | digest | run | expected |
|---|---|---|---|---|---|
| `positive/` | (b) | pinned bytes `0da98e37…` | match | committed 14/14, exit 0 | GREEN `closed=1` |
| `negative-mutated/` | (c) | one-byte mutant `4a5aea99…` | mismatch | same 14/14 transcript, exit 0 | RED `closed=0` |
| `negative-open/` | (d) | pinned bytes `0da98e37…` | match | measured 13/14, exit 1 | RED `closed=0` |
| `negative-absent/` | control | absent (`-`) | mismatch | none, exit 1 | RED `closed=0` |

### (c) the one-byte mutation

```
$ cmp -l pinned/r37-closure.sh negative-mutated/corpus/instruments/r37-closure.sh
78  61  62
$ diff -u pinned/r37-closure.sh negative-mutated/corpus/instruments/r37-closure.sh
-# r37-closure.sh — round-37 closure counter for claim C1 (depth:verifiability).
+# r37-closure.sh — round-37 closure counter for claim C2 (depth:verifiability).
$ sha256sum negative-mutated/corpus/instruments/r37-closure.sh
4a5aea99d88d5750e43556a0501491a6c70443852abe09dbdecd7d0e71060483
$ wc -lc < negative-mutated/corpus/instruments/r37-closure.sh
   1558   73132
$ bash -n pinned/r37-closure.sh && bash -n negative-mutated/corpus/instruments/r37-closure.sh
pinned parse ok / mutant parse ok
```

Byte 78 (1-based), `1`→`2` inside the line-2 comment: same length, same line count, one differing
byte, both parse. It is a comment byte, so no check reads it — except the digest.

## 4. Measured runs behind the transcripts

`positive/run.txt` and `negative-mutated/run.txt` are the committed round-37 receipt block
`.ufo/waves/round-37/final-gates/all-gates.txt:8-22` (14 `E<n> payload=… closed=1` lines plus
`closed=14/14 exit=0`, 15 lines). That block is the pinned bytes' own recorded run — G8 executes the
pinned bytes, so the run line is identical in both cases and only the export copy differs.

`negative-open/run.txt` is this round's real run of the pinned bytes:

```
$ bash pinned/r37-closure.sh --export-ref 2387dcf6ccfefcfb703783387b9aade8fc82abfa \
      --lane <lane> --work <work>/r37-pinned
export-ref=2387dcf6… mode=export lane=… suite-sha256=0da98e37…42434d
deviation=non-default --lane
E1 payload=placeholders=0,lane-hash-markers=0,round37-section=1,round37-final-lane-commits=1,bound=1 closed=1
…
E9 payload=status-read=ok,status-dirty=7,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent closed=0
E10 payload=all-gates=1,suite-file=1,header=1,ancestor=1,digest-match=1,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0 closed=1
…
closed=13/14 exit=1
```

Thirteen of fourteen: E9 is live and the lane's HEAD is not the exported ref (`head-match=0`,
`status-dirty=7` — the wave-1 tree is in flight). A fresh `closed=14/14` therefore cannot be produced
this round; the 14/14 transcript used by (b) and (c) is the committed receipt, which is why it is
cited by line rather than re-run.

The mutant's own run at the same ref, for the neutrality claim:

```
$ bash <mutant> --export-ref 2387dcf6… --lane <lane> --work <work>/r37-mutant
E10 payload=all-gates=1,suite-file=1,header=1,ancestor=1,digest-match=0,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0 closed=0
closed=12/14 exit=1
$ diff -u <pinned run normalised for suite-sha256> <mutant run normalised for suite-sha256>
-E10 payload=…,digest-match=1,… closed=1
+E10 payload=…,digest-match=0,… closed=0
-closed=13/14 exit=1
+closed=12/14 exit=1
```

After normalising the `suite-sha256` header the two runs differ only in E10 and the total: E1–E9 and
E11–E14 are byte-identical. The mutation changes no check's reading except the digest read.

## 5. Why the digest is pinned from the git object

A mutated export copy is not caught by the export's own receipt check if the receipt is edited in the
same pass. Measured on a scratch export of `2387dcf6` whose `corpus/instruments/r37-closure.sh` is the
mutant and whose `.ufo/waves/round-37/final-gates/all-gates.txt` has its three `suite-sha256=` lines
rewritten to the mutant digest (`4a5aea99…`), calling `check_e10` directly:

```
mutant bytes executing:   all-gates=1,suite-file=1,header=1,ancestor=1,digest-match=1,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0  rc=0
pinned bytes executing:   all-gates=1,suite-file=1,header=1,ancestor=1,digest-match=0,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0  rc=1
```

With the coordinated edit the export's own E10 accepts the mutant copy (`digest-match=1`, `rc=0`), so
its run would be 14/14 at a green-E9 head — which is exactly the "even though its run would still be
14/14" state (c) pins. G8' pins the digest from the git object at `2387dcf6`, which no edit inside the
export can move, so the same state is RED on `digest-match=0` while `r37-closed=1`.

## 6. Harness, and its self-controls

```
$ cd .ufo/waves/round-39/wave1/ExecPinnedG8Fixture.fixtures && TMPDIR=/var/tmp bash g8-pinned-check.sh
case=positive G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,digest-match=1,r37-suite=1,r37-closed=1,r37-exit=0 closed=1
case=positive verdict=PASS
case=negative-mutated G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=4a5aea99d88d5750e43556a0501491a6c70443852abe09dbdecd7d0e71060483,digest-match=0,r37-suite=1,r37-closed=1,r37-exit=0 closed=0
case=negative-mutated verdict=PASS
case=negative-open G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,digest-match=1,r37-suite=1,r37-closed=0,r37-exit=1 closed=0
case=negative-open verdict=PASS
case=negative-absent G8 payload=pinned-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d,export-sha256=-,digest-match=0,r37-suite=0,r37-closed=0,r37-exit=1 closed=0
case=negative-absent verdict=PASS
g8p cases=4 failures=0
rc=0
```

Self-controls (run against a scratch copy of the fixture set):

```
# 1. assert the mutant case is GREEN in expected.txt -> harness must reject the assertion
case=negative-mutated G8 payload=…,digest-match=0,…,r37-closed=1,r37-exit=0 closed=0
case=negative-mutated verdict=FAIL want=… closed=1
g8p cases=1 failures=1
rc=1

# 2. replace pinned/r37-closure.sh with the mutant -> digest file disagreement, fail-closed
g8p: pinned digest disagreement computed=4a5aea99…060483 recorded=0da98e37…42434d
rc=2
```

So the harness is not vacuous: a wrong expectation fails, and tampered pinned bytes are refused
before any case runs.

## 7. Deliverable inventory

| file | lines | sha256 |
|---|---|---|
| `README.md` | 113 | `314fd410e418539633a005a6208a3611779deb2d52bc06bf64b51809027fd4b3` |
| `fixtures.json` | 103 | `77cf2a9fbd1f44ca63e483f4d19da871549be1fe72dddf6ed5f4c2a1bc574da9` |
| `g8-pinned-check.sh` | 129 | `936ee31f38bf8b649ab23b3d6c01620c7efb9bec0b61f8361362c44f316df3d4` |
| `expected/expected.txt` | 4 | `33a2360d8cd4eaf58749009a593074691b6f9f3c27cd1f15d8837a53766c7b89` |
| `pinned/r37-closure.sh` | 1558 | `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` |
| `pinned/sha256.txt` | 1 | `c566e774a11010e65029f2603a653947a5dde494bffb592394ffce8ec19f5c08` |
| `pinned/commit.txt` | 1 | `bdb68715f3dde9c1c54580dcef2ecb1adc2d6f5bbeda6c5a97092354b625e518` |
| `pinned/path.txt` | 1 | `b6c901711b1774c8aa818b559194a2a35810fd3de91c862e3f5b2bc085f479f4` |
| `positive/case.env` | 6 | `d61243bc52bc07c05ca78a1dadf39413892668ee6ccf8240c87fa8207addb4c2` |
| `positive/run.txt` | 15 | `a5401662441c9f10dc9c7e35cf877ddcc1e59fcdd91a18163805af3453f2bc7c` |
| `negative-mutated/case.env` | 8 | `cef49e2db1cae9fa96b9f28f6383487d82e64c073b24357951599c9bc39ada26` |
| `negative-mutated/corpus/instruments/r37-closure.sh` | 1558 | `4a5aea99d88d5750e43556a0501491a6c70443852abe09dbdecd7d0e71060483` |
| `negative-mutated/run.txt` | 15 | `a5401662441c9f10dc9c7e35cf877ddcc1e59fcdd91a18163805af3453f2bc7c` |
| `negative-open/case.env` | 6 | `3a32c6aa05ef96bacd85a0298e8f27db7a0b0d3feb90a4ed95f3c8c7ef4dc1d9` |
| `negative-open/run.txt` | 15 | `28e8f8b40945c600dea9e58d167c920b14538ddaea2466cc887cd2e4fbcfdd33` |
| `negative-absent/case.env` | 6 | `ce94c7be47ff442ab930fceb067d30485991b297362f4d7812c91d6007110470` |

`positive/run.txt` and `negative-mutated/run.txt` are byte-identical by design (same pinned run, only
the export copy differs).

## 8. No-harm / scope

- Writes: the deliverable directory and this receipt only. No lane tracked file, no fleet file, no
  source tree, no sibling repo.
- Git: read-only only — `git show`, `git rev-parse`, `git archive`, `git status --porcelain`,
  `git cat-file`-free reads. No add/commit/checkout/reset/stash, no jj. No git fixture was created.
- Citation census: `resolve.py` scans `SKILL.md` + `corpus/**/*.md`; this deliverable sits under
  `.ufo/waves/`, so it adds no citations and moves no census counter.
- `git status --porcelain .ufo/waves/round-39/wave1/` → `?? .ufo/waves/round-39/wave1/` (the wave
  directory is untracked until the L1 lands it; the deliverable adds no modification to a tracked
  path).
- Tooling: nothing installed or upgraded; no package manager run.
- Scratch: `S=/fast/scratch/hyaku/kasegi-r39/ExecPinnedG8Fixture` was created with `mkdir -p`,
  `TMPDIR=$S` bound for every run, `--work` under `$S`, and removed before this receipt
  (`rm -rf -- "$S"`, rc 0; `[ -e "$S" ]` → `ABSENT`). `kasegi-r39` now holds only other seats'
  directories.

## 9. Limits and risks

- **These are payloads for the limb's decision, not a second suite.** The harness models the limb;
  `r39-closure.sh` is authoritative. The payload keys
  (`pinned-sha256`, `export-sha256`, `digest-match`, `r37-suite`, `r37-closed`, `r37-exit`) are this
  set's proposal, shaped to extend the round-38 G8 payload (`r37-suite`, `r37-closed`, `r37-exit`)
  with the pinned digest. If the suite emits a different key set, the inputs and verdicts still
  hold but `expected/expected.txt` must be regenerated to the suite's spelling.
- **The 14/14 transcript is the committed round-37 receipt, not a fresh run.** A fresh
  `closed=14/14` needs a clean lane whose HEAD is the exported ref; measured this round, the pinned
  bytes at `2387dcf6` print `closed=13/14 exit=1` because E9's live limbs see the wave-1 tree. The
  fixture says so in `case.env` (`run_source=`) and in the README.
- **The mutation is a comment byte on purpose.** It proves the digest limb discriminates on a state
  whose checks all read the same; it does not prove the suite rejects a semantic edit — that is the
  suite's own selftest mutants' job.
- **`negative-absent/` is a control, not one of the three named cases.** It reproduces the round-38
  `carry-over-suite-absent` mutant so the fail-closed branch has a fixture; it is listed as a control
  in `fixtures.json`.
- The two real runs above were invoked with an explicit `--lane` equal to the default, so their
  headers carry `deviation=non-default --lane`; the bytes read are the default lane's.
