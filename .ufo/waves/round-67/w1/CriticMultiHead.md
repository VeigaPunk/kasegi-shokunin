# CriticMultiHead — C1 falsification (kasegi round 67, one v1 wave)

Seat: critic (leaf). Judged on depth:verifiability and coverage. Task: falsify C1 (the
multi-head SIGPIPE input-completeness repair) by attacking the candidate gate and the
round-67 driver: (1) cheap no-work forgeries must be rejected, (2) find a masking shape the
new rule still admits, (3) find a genuinely complete shape the rule refuses (false stale) and
judge documentation, (4) test exit-0 partial-output producers and wrappers.

I did not edit any candidate, production file, ledger, or lane git/jj state. Every number
below is a measured command output; nothing is asserted from reading code alone.

## Artifacts under test (sha256, as frozen for the whole run at 18:00:48 -03)

| artifact | path (lane-relative) | sha256 |
|---|---|---|
| candidate gate | `.ufo/waves/round-67/w1/ExecMultiHeadGate/figure-audit.py` | `d5e8fcae6f1523d0ffbe8f21540fde839a24abbe98958378e54da284eec38c05` |
| driver | `.ufo/waves/round-67/w1/ExecMultiHeadDriver/verify.py` | `f2d11468ed39f2fa2fbafc77bc690e3ea8d049fca8c37f56f9f619096b6ae8bb` |
| probe battery | `.ufo/waves/round-67/w1/ExecMultiHeadProbes/probes.py` | `3f2d38a669cbee32b2b5cc97614451981f4f9b58714385a42a3e76a3ac871c28` |
| multi-head limb battery | `.ufo/waves/round-67/w1/MutationMultiHead/multihead-mutbat.py` | `937f8677fb6276635501ac8b6fa6cbe631e7d5ef9dc3b8a2e1cc0c7f9b66e233` |
| production base gate | `corpus/instruments/figure-audit.py` | `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` |

The gate, driver, probes and battery were still being written while this seat ran (the gate
went `51f299…` → `978c98…` → `d5e8fc…`; the driver went `80ea29…` → `4f6fb4…` → `f2d114…`
inside one minute). I froze copies under `w1/CriticMultiHead/frozen/` and every driver verdict
below is against those bytes; the driver's own `driver-self-pin` measurement confirms the
running file equals the pinned digest.

## Method (all receipts in `w1/CriticMultiHead/`)

* Fixtures (`mkfix.py`, native `fix/`): `big.txt` 4224006 B starting `alpha`, `other.txt`
  4224005 B starting `beta`, `xlines.txt` 400000 B (200000 lines of `x`), `missing.txt` and
  `-missing.txt` absent. `big.txt` sha256 `86025c9e…031c4c2`, `xlines.txt` sha256
  `83d10921…ccf4749`.
* Native statuses: `matrix.py` replays each pipeline with `subprocess.Popen` (no shell),
  parent closes its own pipe ends, five repeats, and records every stage's returncode
  (`native-matrix-5x.txt`).
* Gate verdicts: `shapes.py` runs the real gate once per shape on its own one-figure ledger
  (`base-shapes.txt`, `cand-shapes.txt`), so one refusal cannot hide another.
* Driver verdicts: `drive.py` commits the frozen driver, probes, battery and a pin manifest
  into a fixture clone of the lane (`fixture-repo`, `git init`-style clone at `8e2a8fe8…`,
  toplevel asserted) because the round-67 wave is untracked in the lane and the driver reads
  its controls with `git show`. It then runs the real driver in candidate mode with
  `--candidate` for the honest gate and for each forgery; raw output in `forgery-run-*.txt`.
* Forgeries: `forgeries/f1..f7*.py`, each a drop-in `figure-audit.py` that derives nothing.

## Ranked survivors (what still passes the gate that should not; what fails that should pass)

1. **S3/S4 — SIGPIPE masking survives for cut and grep when a later operand's name starts
   with `-` and `--` appears after the first operand.** The gate reads **ok**; native stage 0
   is **-13** five of five; the named file is never opened. Highest-value falsification: it
   refutes the claim as written ("exempt only when the decoded argv names at most one input
   operand") for two of the three repaired heads.
2. **D1 — the driver cannot certify the honest candidate: its own `parse_fig` cannot read a
   FIG line whose derived value contains a space.** `shape-identity` and `probes-base-paired`
   FAIL on the correct gate with `rc=0 verdict=stale`. This is a false-red in the verifier,
   not in the gate.
3. **S11/S12/S18/S21 — exit-0 partial-output producers and wrappers.** `grep -q PAT f1 f2`
   exits 0 without opening `f2` and the gate reads ok (`| wc -l` → `0`, `&& wc -l big.txt` →
   `66001 big.txt`); a python head that swallows EPIPE (S18) or restores `SIG_DFL` (S21)
   is exempt with two operands. The rule cannot see any of these.
4. **S7/S8/S9/S10/S19 — false stales (genuinely complete pipelines refused).** `head -n
   100000 f | head -n 1`, `cut -d : -f 1 f | head -n 1`, `sort -k 1,1 f | head -n 1`,
   `cat f | tr , \n | head -n 1`, `grep -o x f | head -n 1`: native stage 0 `-13` five of
   five, base green, candidate **stale**. Only the option-VALUE class is documented.
5. **D2/D3 — driver-side verifiability gaps.** The multi-head battery measurement's docstring
   promises "base kind is the expected red" but the code requires `rc == 0`; and a battery
   that prints `COLLECTOR ignored=… reason=AttributeError` still counts as PASS.
6. **P8 payload inconsistency (coverage premise).** The wave payload froze
   `grep -c alpha big.txt | head -n 1 → derive-upstream-signal-13`; native stage 0 is `0`
   five of five (grep -c writes once at EOF), so that expectation is unsatisfiable. The
   probes seat already flagged it (`PAYLOAD-DEV candidate P8 payload=rc1/… frozen=rc0`).

No forgery survived: F1–F7 are all rejected (table below).

---

## Finding 1 (depth:verifiability, highest) — masking survives through a mid-argv `--`

Candidate rule as implemented (`w1/ExecMultiHeadGate/figure-audit.py:114-131`, frozen):

```
    tokens = list(argv[1:])
    if tokens and tokens[0] == "--":
        tokens = tokens[1:]
    for _ in range(SIGPIPE_REQUIRED_NONFILE_ARGS.get(head, 0)):
        if tokens:
            tokens = tokens[1:]
    return sum(1 for t in tokens if not (t.startswith("-") and t != "-"))
```

A `--` is only honoured in position 1; a later `--` and every token after it that starts with
`-` are counted as options, so a real file operand disappears from the count.

Native (5 repeats, `python3 -B matrix.py fix`):

```
S3   stages=cut -f1 -d: big.txt -- -missing.txt ;; head -n 1 repeats=['[-13, 0]'] stable=yes stdout_bytes=[6] first=b'alpha\n'
S4   stages=grep x xlines.txt -- -missing.txt ;; head -n 1 repeats=['[-13, 0]'] stable=yes stdout_bytes=[13] first=b'xlines.txt:x\n'
S6   stages=cut -f1 -d: big.txt -missing.txt ;; head -n 1 repeats=['[1, 0]'] stable=yes stdout_bytes=[0] first=b''
```

`-missing.txt` does not exist (`mkfix.py` prints `-missing.txt present: False`). S3/S4 die of
SIGPIPE **before** reaching it; the differential S6 (same argv without `--`) exits 1 because
cut then treats `-missing.txt` as an unknown option — which proves S3/S4 did treat it as a
file operand.

Gate verdicts (`python3 -B shapes.py …`), base vs candidate:

```
base-shapes.txt:S3-cut-mid-dashdash    masking-dashdash rc=0 verdict=ok    FIG S3-cut-mid-dashdash recorded=alpha derived=alpha ok
base-shapes.txt:S4-grep-mid-dashdash   masking-dashdash rc=0 verdict=ok    FIG S4-grep-mid-dashdash recorded=xlines.txt:x derived=xlines.txt:x ok
cand-shapes.txt:S3-cut-mid-dashdash    masking-dashdash rc=0 verdict=ok    FIG S3-cut-mid-dashdash recorded=alpha derived=alpha ok
cand-shapes.txt:S4-grep-mid-dashdash   masking-dashdash rc=0 verdict=ok    FIG S4-grep-mid-dashdash recorded=xlines.txt:x derived=xlines.txt:x ok
```

So a green FIG line still reports success on a world where a named input was never read —
the exact class C1 was opened to close, for two of the three repaired heads. `cat` is safe
(S5 stale: the r66 function refuses any option token), which shows the r66 rule was stronger
than the new one.

Why the battery misses it: the four new selftest cases are cut/wc/grep with two plain
operands plus `grep x big.txt` (selftest cases `s-cutmulti`, `s-wcmulti`, `s-grepmulti`,
`s-grepone`); the driver's SHAPES P1–P18 contain no mid-argv `--`; the probes P1–P18 likewise.
The r66 P8 shape (`cat -- -- missing.txt`) is the leading-`--` form only.

Smallest safe correction: treat `--` as an end-of-options separator **wherever it appears**
(drop it and stop counting dash tokens as options after it), or refuse the exemption when a
`--` appears after the first token. Add one selftest case and one driver shape for
`cut -f1 -d: big.txt -- -missing.txt | head -n 1` (native -13) and for
`grep x xlines.txt -- -missing.txt | head -n 1`.

## Finding 2 (verifiability, high) — the driver's `parse_fig` cannot read its own shapes

`w1/ExecMultiHeadDriver/verify.py:407-418` (frozen):

```
        m = re.search(r" derived=(\S+) ok$", ln)
        if m:
            return "ok", "-", m.group(1)
        return "stale", "-", None
```

`\S+` cannot match a derived value containing a space, and the driver's own SHAPES P10
(`wc -l big.txt missing.txt | head -n 1` want `4096 big.txt`), P13 (`wc -l big.txt | head -n 1`
want `4096 big.txt`) and P14 (`sha256sum big.txt | head -n 1` want `<hash>  big.txt`) all
have space-bearing wants.

Receipt `dw-candidate/receipts/shape-P13-probe.txt` (gate rc 0, gate green):

```
FIG P13-probe-spelling recorded=4096 big.txt derived=4096 big.txt ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
[exit=0]
```

Driver verdict on the honest candidate (`forgery-run-candidate.txt`):

```
RESULT shape-identity FAIL shapes=18 P1 rc=1 verdict=stale … | P13 rc=0 verdict=stale reason=- native0=0 | P14 rc=0 verdict=stale reason=- …
RESULT probes-base-paired FAIL … face-recorded=P10=rc0/-,P11=rc0/-,P9=rc0/- FACES base-paired attempts=… P10 sig-face stage0=-13 base=stale:- want=ok; …
VERIFY measurements=12 failures=2 revision=8e2a8fe8eb92d7c824902a4b70aab027a9aacee0 mode=candidate
DRIVER-RC 1
```

So the delivered driver returns 1 on the correct candidate. Its only two failures are this
parse defect (P13/P14 in `shape-identity`, P10 in `probes-base-paired`). A driver that cannot
green the honest candidate cannot certify the claim; the L1 must not read `DRIVER-RC 1` here
as a gate defect.

Smallest safe correction: parse from the right — `derived=(.*) ok$` with `want` compared as a
whole string — or emit a machine-stable separator in the gate's FIG line and parse that.
Re-run and require `VERIFY measurements=12 failures=0` on the honest candidate before any
claim is read green.

## Finding 3 (verifiability, medium-high) — the multi-head battery measurement

`w1/ExecMultiHeadDriver/verify.py:668-695` (frozen) says in its docstring "a baseline failure
is the battery's own honest exit 1, which at base kind is the expected red", but line 695 is
`ok = rc == 0 and want is not None and len(lines) == 1 and lines[0] == want`. Measured on the
base gate, the battery exits 1 with `MUTBAT killed=0/7 survivors=0 equivalents=0
invalid_rejected=10 failures=5`; on the candidate it exits 0 with `MUTBAT killed=7/7
survivors=0 equivalents=3 invalid_rejected=0 failures=0`. The base-kind expected red is
therefore unreachable in code: a base-mode driver run always FAILs this measurement.

Second gap in the same measurement: the battery reports that it could not use the collector it
was handed, and the driver still passes it because the note is not part of the verdict:

```
RESULT multihead-mutbat PASS exit=0 want='MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0' sha256=937f86… COLLECTOR ignored=/…/controls/probes.py reason=AttributeError
```

That is a battery that silently ran without the probe collector and was still counted as a
pass. Either the driver fails on any `COLLECTOR ignored=` line, or the battery must not emit a
passing summary when its collector failed.

Smallest safe correction: make the base-kind path accept the pinned red (`rc in {0,1}` with
the pinned summary for that kind) and fail on any `COLLECTOR ignored=` line.

## Finding 4 (depth, medium) — false stales: complete pipelines refused

Native (5 repeats) vs gate verdict (base green, candidate stale):

```
S7   stages=head -n 100000 big.txt ;; head -n 1            repeats=['[-13, 0]'] stable=yes  cand rc=1 stale
S8   stages=cut -d : -f 1 big.txt ;; head -n 1             repeats=['[-13, 0]'] stable=yes  cand rc=1 stale
S9   stages=cat big.txt ;; tr , \n ;; head -n 1            repeats=['[-13, -13, 0]'] stable=yes  cand rc=1 stale
S10  stages=sort -k 1,1 big.txt ;; head -n 1               repeats=['[-13, 0]'] stable=yes  cand rc=1 stale
```

Candidate FIG lines (`cand-shapes.txt`):

```
S7-head-large-n        false-stale-optval rc=1 verdict=stale FIG … reason=derive-upstream-signal-13 stale
S8-cut-sep-opts        false-stale-optval rc=1 verdict=stale FIG … reason=derive-upstream-signal-13 stale
S9-tr-two-sets         false-stale-tr  rc=1 verdict=stale FIG … reason=derive-upstream-signal-13 stale
S10-sort-sep-key       false-stale-optval rc=1 verdict=stale FIG … reason=derive-upstream-signal-13 stale
```

Each pipeline names exactly one file, that file exists and is read, and the truncation hides
nothing — the refusal is conservative, not corrective.

Documentation judgement (candidate docstring, frozen lines 49-56):

* Option-value inflation **is** documented: "the count is conservative: a leading \"--\"
  separator is dropped, grep's pattern is skipped as a required non-file argument, a token
  starting with \"-\" that is not \"-\" itself is an option and not an operand, and everything
  else counts — so option VALUES inflate the count and cause a safe stale."
* `tr` is **not** documented: its two arguments are character sets, never files, so
  `SIGPIPE_REQUIRED_NONFILE_ARGS` should carry `tr: 2` (or tr should be exempt
  unconditionally); with the current table tr can never be exempt. The docstring says only
  "everything else counts".
* The grep skip is positional and **not** documented as such: it removes `tokens[0]` after the
  leading-`--` drop, so `grep -o x f` loses `-o` instead of the pattern and counts 2 operands.
  Measured: native `grep -o x xlines.txt | head -n 1` = `[-13, 0]` five of five; base green;
  candidate `FIG S19 … reason=derive-upstream-signal-13 stale`. This is the spelling the real
  ledger already uses (`grep -oE '…' file | head -1 | cut -d= -f2`), so it is one large
  operand away from a production false red.

Impact on the committed ledger: none today. `python3 -B <candidate> --ledger
corpus/instruments/figure-audit-ledger.json --root .` prints
`FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` (rc 0). The false-stale classes are latent,
not active.

Smallest safe correction: `SIGPIPE_REQUIRED_NONFILE_ARGS = {"grep": 1, "tr": 2}`; skip
required non-file arguments **after** option filtering rather than before; keep option values
counted (documented conservatism) or, better, note the residual in the docstring.

## Finding 5 (depth, medium) — exit-0 partial producers and wrappers defeat any SIGPIPE rule

Native, then gate verdict:

```
S11  stages=grep -q x big.txt missing.txt                     repeats=['[0]']      stable=yes  stdout_bytes=[0]
S12  stages=grep -q x big.txt missing.txt ;; wc -l            repeats=['[0, 0]']   stable=yes  stdout_bytes=[2] first=b'0\n'
S17  stages=python3 corpus/instruments/wrapper.py big.txt missing.txt ;; head -n 1   repeats=['[1, 0]'] stable=yes
S18  stages=python3 corpus/instruments/wrapper2.py big.txt missing.txt ;; head -n 1  repeats=['[0, 0]'] stable=yes
S21  stages=python3 corpus/instruments/pipe2.py big.txt missing.txt ;; head -n 1     repeats=['[-13, 0]'] stable=yes
```

```
candidate: S11 rc=0 ok (derived=66001 big.txt)      # `grep -q … && wc -l big.txt`
candidate: S12 rc=0 ok (derived=0)                  # `grep -q … | wc -l`
candidate: S17 rc=1 stale reason=derive-upstream-exit-1   # plain wrapper: caught
candidate: S18 rc=0 ok                              # wrapper that swallows EPIPE
candidate: S21 rc=0 ok                              # python head with SIG_DFL, native -13
```

`grep -q` exits 0 on the first match and never opens the second named file; no SIGPIPE is
involved, so no input-count rule can see it. S21 is the named residual made concrete: the
gate's own selftest fixture `pipe.py` is exactly this shape (SIG_DFL stream), and any
allow-listed python head keeps the benign rule. S18 is a wrapper that reports success after a
broken pipe. The docstring says "Unknown heads retain the benign rule" — it does not say that
a python head can therefore name two operands and mask one, nor that an exit-0 partial
producer is invisible.

Scope note: S11/S12 predate the repair (base is green too) and are outside the SIGPIPE claim;
S21 is a declared residual. They are ranked here because the wave's stated purpose is "a green
FIG line reports success on a world where a named input was never read", and these are exactly
that, unchanged.

## Finding 6 (coverage premise) — the frozen P8 expectation is unsatisfiable

```
$ python3 -B native.py fix 5 'grep -c alpha big.txt;;head -n 1'
run1 stages=[0, 0] … run5 stages=[0, 0]
```

The wave payload froze `P8 … candidate -> rc1 derive-upstream-signal-13`; grep -c writes once
at EOF, so no SIGPIPE can occur. The probes battery already reports the deviation
(`PAYLOAD-DEV candidate P8 payload=rc1/derive-upstream-signal-13 frozen=rc0 … native stage0
[0,0]`) and the driver pins P8 as `(0, "-")`. The L1 should record the payload correction as
a wave defect, not a host flake.

## (1) Forgery rejection — measured

Each forgery is a complete `figure-audit.py` replacement that performs no derivation. "own rc"
is the forgery's own exit code on the driver's red ledger (`g.txt` contains `35`, want `34`;
the real base gate prints `FIG RED recorded=34 derived=35 want=34 stale`, exit 1). Driver
column is `DRIVER-RC` plus the failing measurements from `forgery-run-*.txt`.

| forgery | own rc on red ledger | driver rc | failing measurements (of 12) |
|---|---|---|---|
| F1 always-green | 0 | 1 | probes-base-paired, probes-measured, shape-identity, selftest, mutbat-existing, multihead-mutbat, red-wrong-want |
| F2 always-stale | 1 | 1 | + real-ledger (8) |
| F3 probe-id keyed | 1 | 1 | 8 (incl. real-ledger, red-wrong-want) |
| F4 fixture-path keyed | 1 | 1 | 8 |
| F5 record-text keyed | 0 | 1 | 8 |
| F6 recorded==want counter | 0 | 1 | 8 |
| F7 derive-text lookup (table copied from the driver's own SHAPES, default green) | 0 | 1 | 7 (incl. red-wrong-want) |
| honest candidate (control) | 1 | 1 | 2 — both Finding 2, not forgeries |

Representative driver lines:

```
RESULT shape-identity FAIL shapes=18 P1 rc=0 verdict=ok … | P9 rc=0 verdict=ok … | P10 rc=0 verdict=stale reason=- …
RESULT red-wrong-want FAIL exit=0 red-stale-line=no
RESULT selftest FAIL cases=0 failures=0 want=71 exit=0 kind=candidate
RESULT probes-measured FAIL mode=candidate probes=18 rc=1 problems=P1 rc=0 want=[1]; P2 rc=0 want=[1]; P5 rc=0 want=[1]; …
VERIFY measurements=12 failures=7 revision=8e2a8fe8eb92d7c824902a4b70aab027a9aacee0 mode=candidate
DRIVER-RC 1
```

What actually kills them: the two-spelling shape ledger (`P*-probe-spelling` vs
`held-<sha10>`) kills id keying; `red-wrong-want` kills any oracle whose default is green or
whose comparison is ledger-internal; `real-ledger` kills any oracle whose default is stale;
`selftest` kills "cases=0"; the probe battery and the limb battery kill the rest. The
anti-forgery design holds.

## What this falsification does NOT claim

* Not a sandbox claim: the gate still executes allow-listed heads and python scripts under
  `corpus/instruments/`; S18/S21 show a python head can report success while an operand is
  unread.
* Not general shell correctness or pipefail: `&&`, option-value semantics, and exit-0 partial
  producers remain outside the rule.
* `wc -l big.txt missing.txt | head -n 1` is flaky at native level on this host and is
  reported as flaky, not as a rule defect: my pass gave stage 0 = `1` once and `-13` four
  times, a later pass gave `-13` five of five. Under the candidate both outcomes read stale
  (`derive-upstream-exit-1` once, `derive-upstream-signal-13` four times), which is the
  behaviour `controls/dispatch-addendum-r67.md` requires.

## Setup notes / failed setups (honesty)

* The round-67 wave is untracked in the lane, so the driver's `git show <controls>:pins`
  contract cannot be exercised against the lane at all in predata. I ran the real driver
  against a fixture clone (`fixture-repo`, HEAD `8e2a8fe8…`, toplevel asserted) with the
  frozen controls committed there. Pins were authored by me from measured values
  (`ctl/expected.json`): `selftest_cases` 67/71, `mutbat_summary` measured, and
  `multihead_mutbat_summary` measured per kind. No production byte was touched.
* I ran the mutation battery before its collector path worked; it printed
  `COLLECTOR ignored=… reason=AttributeError` on every invocation I made, including the ones
  the driver counts as PASS (Finding 3). I did not treat that battery as evidence for the
  candidate.
* No tool was installed or upgraded; no pacman transaction was attempted.
* Scratch `/fast/scratch/hyaku/kasegi-r67/CriticMultiHead/` held fixtures, frozen artifacts,
  the fixture clone and all receipts; durable receipts are copied into this directory and the
  scratch tree is deleted before yielding.

## Receipts in this directory

`base-shapes.txt`, `cand-shapes.txt` (frozen candidate), `native-matrix-5x.txt`,
`reference-rule.txt` (spec read literally), `forgery-verdicts.txt`,
`forgery-run-{candidate,F1…F7}.txt`, `forgeries/*.py`, `wrapper.py`, `wrapper2.py`,
`pipe2.py`, `frozen/` (byte copies with the shas above).
