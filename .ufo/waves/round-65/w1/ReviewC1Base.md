# ReviewC1Base — C1 premise reproduction review (base `a283189b`)

Independent, reproduction-first review of the round-65 C1 premise at base revision
`a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`. This is predata: no claim is frozen, nothing here
admits or scores a claim, and no candidate implementation was judged (that is a different seat's
scope; the sibling candidate bytes that exist in `w1/ExecSignalGate/` were not read or run).
Read-only outside my own scratch and report dir. No commit, no mutating git, no production file
edited, no tool installed, no pacman transaction.

## VERDICT: **PREMISE HOLDS**

Precisely: in `corpus/instruments/figure-audit.py` at `a283189b`, `upstream_stale()` returns
`False` for every negative `Popen.returncode`, so a non-final pipeline stage terminated by
SIGTERM (`-15`) or SIGKILL (`-9`) is not stale; when the final stage's stdout still equals
`want`, the figure prints `ok` and the audit exits **0**. Reproduced with the real instrument for
stage 0 and for a middle stage, for both signals. A *final*-stage signal is caught by the
`status != 0` branch (exit 1) but the printed reason is the malformed `derive-exit--15`
(`-9` → `derive-exit--9`), which contradicts the instrument's own documented `derive-exit-N`
grammar. Both claimed positives stay green. The default 35-figure ledger is 35/35 green on the
base bytes; no current derive triggers the false green by itself (the defect is in the gate's
contract, not in a live wrong number today), but two real figures (`want == "0"`) cannot tell a
killed upstream from a legitimate no-match.

## Base identity

| item | value |
|---|---|
| revision | `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b` (lane `HEAD` at review start) |
| `corpus/instruments/figure-audit.py` sha256 | `8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9` |
| `corpus/instruments/figure-audit-ledger.json` sha256 | `28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b` |
| scratch export | `git archive` of the revision into `/fast/scratch/hyaku/kasegi-r65/ReviewC1Base` (no `.git`); export instrument sha equalled the lane's at review start, byte for byte |
| host | linux 7.2.11-arch1-1, python 3.14.8, git 2.56.0 |
| git derivation env | `refs/replace` 0 entries, no `info/grafts`, `core.bare=false`; ledger revs `32782bd…` and `8a5d7538…` resolve (`git cat-file -e` exit 0) |

The real-ledger scan (§R5) needs `.git` and the committed `.ufo` receipts, so it ran with the
scratch ledger and `--root` = the lane checkout; that root was used **read-only** (all derives are
`git show|cat-file|ls-tree`, `grep`, `wc`, `cut`, `tr`). At review start and throughout every run
below, lane `HEAD` was `a283189b` and `git diff --stat` was empty; `git status --porcelain` showed
only its pre-existing untracked set (round-57..60 `w1.ready.dispatched` markers and the untracked
`round-65/`).

**Lane movement after the runs (other seats integrating):** `HEAD` is now `57cb8dec` and the lane
working tree carries a candidate `corpus/instruments/figure-audit.py` (sha256
`86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`) plus frontier appends. None
of that is mine and none of it is judged here. Every number in this review was produced against
the pinned export, whose `figure-audit.py` still hashes `8d92eaa0…`, byte-identical to
`git show a283189b:corpus/instruments/figure-audit.py` (`sha256sum` of both compared post-run).
A rerun against the current lane tip would not reproduce these base bytes.

## Reproduction receipts

Fixture built by hand under `c1fix/` in the export (not the selftest harness): a two-line `g.txt`
(`alpha\nbravo\n`), and helpers `corpus/instruments/{kill,kill9,segv,intr}.py` that send
themselves SIGTERM, SIGKILL, SIGSEGV, SIGINT. Raw statuses observed outside the gate:
`python3 kill.py` → shell 143, `kill9.py` → 137, `segv.py` → 139, `intr.py` → 130;
`python3 kill.py | wc -l` → `PIPESTATUS=143 0`; `cat g.txt | python3 kill.py` →
`PIPESTATUS=0 143`.

Every receipt is `python3 -B <export>/corpus/instruments/figure-audit.py --ledger <L> --root <c1fix>`
run with cwd `c1fix`; `=== EXIT:` is the instrument's exit code.

### R1 — upstream SIGTERM: **false green** (`r1.txt`, sha256 `a6258cd3…`)
```
FIG c1-upstream-sigterm recorded=0 derived=0 ok
FIG c1-middle-sigterm recorded=0 derived=0 ok
FIGURE-AUDIT figures=2 ok=2 stale=0 exit=0
=== EXIT: 0
```
Derives: `python3 corpus/instruments/kill.py | wc -l` and
`cat g.txt | python3 corpus/instruments/kill.py | wc -l`. Stage code vectors measured by the
probe: `[-15,0]` and `[0,-15,0]`. The stage is dead, the figure says ok.

### R2 — upstream SIGKILL: **false green** (`r2.txt`, sha256 `57eba5e4…`)
```
FIG c1-upstream-sigkill recorded=0 derived=0 ok
FIG c1-middle-sigkill recorded=0 derived=0 ok
FIGURE-AUDIT figures=2 ok=2 stale=0 exit=0
=== EXIT: 0
```
Derives: `python3 corpus/instruments/kill9.py | wc -l` and
`cat g.txt | python3 corpus/instruments/kill9.py | wc -l`; vectors `[-9,0]` and `[0,-9,0]`.

### R3 — final-stage signal: fails closed, malformed label (`r3.txt`, sha256 `6746155247…`)
```
FIG c1-final-sigterm recorded=0 derived=UNAVAILABLE reason=derive-exit--15 stale
FIG c1-final-sigterm-single recorded=0 derived=UNAVAILABLE reason=derive-exit--15 stale
FIG c1-final-sigkill-single recorded=0 derived=UNAVAILABLE reason=derive-exit--9 stale
FIGURE-AUDIT figures=3 ok=0 stale=3 exit=1
=== EXIT: 1
```
Derives: `cat g.txt | python3 corpus/instruments/kill.py`, the same single-stage, and the SIGKILL
single-stage. Exit code 1 is correct; the label is not. The docstring promises `derive-exit-N`
(line 42); the emitted token is `derive-exit-` + the signed `returncode` (`-15`), i.e.
`derive-exit--15`. The intended `derive-signal-N` is absent.

### R4 — the two positives stay green (`r4.txt`, sha256 `98e9e74c…`)
```
FIG c1-grep-exit1-nomatch recorded=1 derived=1 ok
FIG c1-clean-pipeline recorded=2 derived=2 ok
FIG c1-grep-exit1-zero-lines recorded=0 derived=0 ok
FIG c1-middle-grep-exit1 recorded=0 derived=0 ok
FIGURE-AUDIT figures=4 ok=4 stale=0 exit=0
=== EXIT: 0
```
`grep -c absent g.txt | wc -l` → 1; `cat g.txt | wc -l` → 2; `grep absent g.txt | wc -l` → 0;
and a **middle-stage** no-match `cat g.txt | grep absent | wc -l` → 0. The same positive exists
in situ in the real ledger: `figure-audit-mentions-base-log` group 1 has vector `[0,1,0]` (middle
`grep` exit 1) and audits ok.

### Baseline and selftest
- Real ledger at base: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` (`lane-baseline.txt`,
  sha256 `ddbc25de…`).
- `--selftest` (scratch `HYAKU_SCRATCH`): exit 0, `selftest cases=59 failures=0`, and
  `selftest case=upstream-python-signal-ignored exit=0 want=0 verdict=pass` — the selftest does
  not merely permit the false green, it **pins** it (`selftest.txt`, sha256 `b51618a2…`).

## Line anchors (base `corpus/instruments/figure-audit.py`)

`upstream_stale`, lines 79–86 — the negative-status hole:
```
79  def upstream_stale(head, status):
80      """Stale upstream statuses: any >1, or exit1 from a program other than grep.
81
82      Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored.
83      """
84      if status > 1:
85          return True
86      return status == 1 and os.path.basename(head) != "grep"
```
`-15`, `-9`, `-13`, `-11`, `-2` all fail `> 1` and fail `== 1`, so all return `False`.

Contract text, lines 41–44:
```
41  After all pipeline stages finish, a nonzero final status takes precedence
42  (derive-exit-N); otherwise the first upstream status that is >1, or exit1 from a
43  program other than grep, is stale (derive-upstream-exit-N). Grep exit1 is an ordinary
44  no-match and is not an error; negative signal statuses remain ignored. This is not
```

Dispatch and labels, lines 115–122:
```
115              status = processes[-1].returncode
116              if status != 0:
117                  out = b"".join(output).decode("utf-8", "replace").strip()
118                  return None, out, "derive-exit-%d" % status
119              for p, head in zip(processes[:-1], heads[:-1]):
120                  if upstream_stale(head, p.returncode):
121                      out = b"".join(output).decode("utf-8", "replace").strip()
122                      return None, out, "derive-upstream-exit-%d" % p.returncode
```
Line 118 is what prints `derive-exit--15`. Line 122 is the latent twin: it is unreachable for
negatives today only because line 120 asks `upstream_stale` first; the moment that predicate
returns `True` for a signal, line 122 emits `derive-upstream-exit--15`. Verified by string
formatting, not a gate run: `"derive-exit-%d" % -15` → `derive-exit--15`,
`"derive-upstream-exit-%d" % -15` → `derive-upstream-exit--15`.

Stage mechanics, lines 111–113: the final stage is drained by `communicate()`, then every
non-final stage is `wait()`ed before the status checks, so a non-final stage's `returncode` is
final and negative when it was signalled. The cleanup that could inject a synthetic `-9`
(`p.kill()`) runs in `finally` after the checks (line 130), so it does not contaminate them.

Report site, line 302: `print("FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" % (…, err))`
— the reason token is user-facing, which is why `derive-exit--15` is a contract defect, not typography.

Selftest encoding of the defect: line 72 `EXPECTED_CASES = 59`, lines 365–366 write
`kill.py` with `os.kill(os.getpid(), signal.SIGTERM)`, and line 449 is
`run_case("upstream-python-signal-ignored", 0, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"))`.
There is exactly one signal case, it is stage 0, it wants exit 0, and there is **no**
final-stage-signal case and **no** signal-under-`&&` case anywhere in the selftest.

## R5 — SIGPIPE scan of the real 35-figure ledger

Method: `stage-status-probe.py` (own diagnostic, in `c1fix/`) imports the gate's *unmodified*
`parse_derive` for argv fidelity, executes every pipeline with `Popen` (no shell), records every
stage's `returncode`, and reports negatives; nothing is written. Ledger = the base-revision bytes
above; root = lane, read-only. Command:
`python3 -B stage-status-probe.py ../corpus/instruments/figure-audit-ledger.json <lane> 30`.

Result (`r5-stage-status.txt`, sha256 `be443a28…`):
```
SUMMARY figures=35 reps=30 stage_runs=2730 negative_total=0 sigpipe_total=0
STRUCTURAL early-exit-downstream figures=7
EARLY id=census-fresh-literal-r55 stage_indexes=0 chain=grep | head | cut
EARLY id=census-internal-r55-receipt stage_indexes=0 chain=grep | head | cut
EARLY id=census-gone-r55-receipt stage_indexes=0 chain=grep | head | cut
EARLY id=fail-entry-records stage_indexes=0 chain=grep | head | cut
EARLY id=census-fresh-literal-r56 stage_indexes=0 chain=grep | head | cut
EARLY id=census-internal-r56-receipt stage_indexes=0 chain=grep | head | cut
EARLY id=census-gone-r56-receipt stage_indexes=0 chain=grep | head | cut
```
Coverage: 35 figures, 37 pipeline groups (two figures chain a single-stage group and a piped
group with `&&`), 91 stages per pass, 30 repeats = 2730 stage executions.
All 35 figures' status vectors are `0` (the two `&&` figures read `0:[0] 1:[0,1,0]`).

Which stages *could* receive SIGPIPE: only the 7 `grep | head -1 | cut` figures — stage 0 (`grep`)
writes into an early-exit reader (`head`). The two `tail -1` derives (`census-fixedpoint-*`) are
not at risk: `tail` reads to EOF. Volumes measured on the committed receipts: every `head -1`
producer emits **exactly one line of 10–22 bytes** (round-55: 19/14/10 B; round-56: 16/14/10 B;
round-53 `FAIL_entry_records` 22 B), a single atomic pipe write, so `head` cannot close before the
write lands and no `EPIPE`/SIGPIPE occurs — confirmed by 0/2730. The same shape exists in the
control ledger `.ufo/waves/round-54/controls/red-d53-ledger.json` (`d53-1-trailer`, also 1 match,
22 B).

Forced control (`r5-forced-sigpipe.json`, `r5-forced-sigpipe.txt`, sha256 `3e04ee5d…`): with a
200 000-line `big.txt`, `cat big.txt | grep xx | head -1` yields vectors `[-13,-13,0]` and the
base gate prints `FIG c1-forced-sigpipe recorded=xx yy derived=xx yy ok` / `exit=0`.

**Answer on necessity:** the proposed SIGPIPE exception is **not exercised by the current 35
figures** (0 SIGPIPEs in 2730 stage runs; the producers are size-bounded to one short line), but
it is **required as a guard** the moment the predicate is generalized (see F1/F3): the shape is
legitimate and present in 7 figures plus one control ledger, and it kills **two** stages at once.
So the pinned positive control must be a ≥3-stage chain (`cat | grep | head -1`, not just
`grep | head -1`): a control that only permits the stage adjacent to `head` would leave `cat`
falsely stale.

## Findings — behaviours the intended predicate would get wrong

### F1 (HIGH, under-refusal) A SIGTERM/SIGKILL-only rule still accepts every other signal
Measured on the base gate: `python3 corpus/instruments/segv.py | wc -l` → vectors `[-11,0]`,
`cat g.txt | segv.py | wc -l` → `[0,-11,0]`, and `intr.py | wc -l` → `[-2,0]`; all audit
`ok`/`exit=0` (`r5b-segv.txt`, sha256 `2f3a8e87…`). SIGABRT (`-6`), SIGBUS (`-7`) and SIGFPE
(`-8`) follow from the same two comparisons at lines 84–86 but were not separately run. If the
implementation enumerates only `-15`/`-9`, this whole class stays a false green. Recommend the
general rule `status < 0 and status != -SIGPIPE` (non-final) / `status < 0` → `derive-signal-N`
(final), which subsumes the stated intent; the literal enumeration does not.

### F2 (HIGH, under-refusal + diagnostics) The upstream reason at line 122 is a second malformed label
Making `upstream_stale` return `True` for a signal without adding a dedicated branch produces
`derive-upstream-exit--15` (format-string verified). The acceptance phrase "with a reason naming
the signal" is only met by a new branch, e.g. `derive-upstream-signal-15`, evaluated before line
122. The same patch must update the contract text at lines 41–44 and the docstring at line 82,
which currently assert that negative statuses are ignored.

### F3 (MEDIUM, over-refusal) Scope the SIGPIPE exemption to *all* non-final stages, not the one before `head`
Measured: `cat big.txt | grep xx | head -1` gives `-13` on both `cat` and `grep`. An exemption
keyed to "stage immediately feeding an early-exit reader" or to `head`-adjacent stages would
flag `cat` stale on a legitimate pipeline. The exemption must be stage-index agnostic on
non-final stages.

### F4 (MEDIUM, under-refusal) Middle-stage coverage must be explicit and pinned
The false green is not a stage-0 quirk: `cat g.txt | python3 kill.py | wc -l` is green at base
(`[0,-15,0]`, R1) and so is the SIGKILL middle case (`[0,-9,0]`, R2). The predicate already
iterates `processes[:-1]`, so the fix inherits this — but the *selftest* does not pin it. The
only signal case (line 449) is stage 0, so a candidate that replaced only that case would leave
middle-stage, final-stage, and `&&`-group signals unpinned. Required new pins: middle-stage
signal stale, final-stage signal `derive-signal-N`, signal in the second `&&` group, and a
SIGPIPE positive control.

### F5 (MEDIUM, under-refusal in the real corpus) Two `want == "0"` figures cannot distinguish a killed upstream from a no-match
`figure-audit-mentions-base-log` and `figure-audit-mentions-base-knowledge-expected` derive
`… | grep 'figure-audit' | wc -l` with `want "0"`. A `git show` killed by an external SIGTERM
(OOM is SIGKILL; harness timeouts are SIGTERM) yields `grep` no-match (exit 1, legitimately
ignored) and `wc -l` = `0`, which equals `want` — the figure is green under both the status rule
and the value comparison. These two are the concrete place where the base defect has bite; a
general signal rule closes them.

### F6 (LOW, diagnostics) The documented label grammar is contradicted even before the fix
`derive-exit-N` (line 42) versus the emitted `derive-exit--15`/`derive-exit--9` (R3). Exit code is
already 1, so this is not a false green; it is a reason-string contract break, and it is currently
unpinned (no final-stage signal case in the selftest). Today no script parses `derive-exit-`
(the consumers in `.ufo/waves/round-5x` are prose receipts), so nothing mis-decodes it yet.

### F7 (LOW, test-suite integrity) The fix must change the pin, not just the code
`EXPECTED_CASES = 59` (line 72) and line 449's `want_exit 0` encode the defect. Flipping behaviour
without renaming/flipping that case makes the selftest red (correctly); adding the SIGPIPE control
requires bumping the pin. A candidate that leaves `upstream-python-signal-ignored exit=0
want=0 verdict=pass` in place has not met C1, even if the implementation is right.

### Over-refusal cases that are *not* real risks (checked, so they don't get "fixed" into bugs)
- **Final-stage SIGPIPE as stale:** unreachable in this gate's I/O model — the final stage's stdout
  is drained by `communicate()` to EOF, so it has no early-closing reader. Treating `-13` on the
  final stage as `derive-signal-13` is harmless; treating it as benign would be equally harmless.
  [INFERENCE from lines 111–118, not observed.]
- **`grep` exit 1 positives:** unchanged by any negative-status rule; the real ledger's
  `[0,1,0]` middle-grep figure and all four R4 cases are green and must stay so.
- **Gate-deadline kills:** the timeout path returns `derive-timeout` before the status checks
  (line 123), and the `finally` `p.kill()` cannot leak a synthetic `-9` into the labels as long
  as the status checks stay above the cleanup. A refactor that moves the check after the
  `finally` would create a false `derive-signal-9` on every timeout.

## Residual risk and verification gaps

- **The defect is latent for the shipped ledger.** 35/35 green at base, and no committed derive
  self-signals; C1 is a gate-contract repair with two `want == "0"` entry points (F5) and an
  external-kill exposure, not a currently-wrong number. Severity should be read that way.
- **SIGPIPE absence is empirically bounded, not proven for all inputs.** 30 repeats over the
  byte-pinned ledger with 1-line/≤22-byte producers; the argument that no `EPIPE` can occur is
  size-based (atomic ≤`PIPE_BUF` write after `head` read). A future receipt with many matches
  would make the 7 figures timing-dependent, which is exactly what the pinned control must hold.
- **30 reps is not a race proof.** It is a repetition bound on deterministic commands; no
  adversarial scheduling was injected.
- **Signals delivered to the gate process itself** (e.g. a CI runner SIGTERM to the process
  group) are outside the ledger contract: the audit dies with 143/137 and no `FIGURE-AUDIT`
  summary. Callers must treat an exit outside `{0,1,2}` as harness failure. Not addressed by C1.
- **I did not read or run the candidate bytes** in `w1/ExecSignalGate/`; this review judges the
  premise only, so candidate conformance to F1–F7 remains to be measured by its own seat.

## Commands actually run (all read-only or scratch-only)

```
git -C <lane> archive a283189b… | tar -x -C /fast/scratch/hyaku/kasegi-r65/ReviewC1Base
cmp via sha256sum: export figure-audit.py == lane figure-audit.py
cd <export>/c1fix && python3 -B ../corpus/instruments/figure-audit.py \
   --ledger r{1,2,3,4}-*.json --root $PWD            # receipts r1..r4, exit codes 0,0,1,0
cd <export> && HYAKU_SCRATCH=<scratch>/selftest-tmp python3 -B corpus/instruments/figure-audit.py --selftest
cd <lane> && python3 -B corpus/instruments/figure-audit.py        # run while HEAD == a283189b: 35/35 ok, exit 0
cd <export>/c1fix && python3 -B stage-status-probe.py ../corpus/instruments/figure-audit-ledger.json <lane> 30
cd <export>/c1fix && python3 -B stage-status-probe.py r5-forced-sigpipe.json $PWD 1
cd <export>/c1fix && python3 -B stage-status-probe.py r5b-segv.json $PWD 1
native status probes: kill.py 143, kill9.py 137, segv.py 139, intr.py 130; PIPESTATUS vectors
read-only: git rev-parse, git status, git diff --stat, git replace -l, git cat-file -e, sha256sum
```
No package installed; pacman untouched. Scratch (`/fast/scratch/hyaku/kasegi-r65/ReviewC1Base`,
byte-identical export + `c1fix/` fixtures and probe) removed on exit after the receipts were
copied to `.ufo/waves/round-65/w1/ReviewC1Base/`.

Report: .ufo/waves/round-65/w1/ReviewC1Base.md
