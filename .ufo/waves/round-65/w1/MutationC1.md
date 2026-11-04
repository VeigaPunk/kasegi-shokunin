# MutationC1 — independent mutation test of the C1 signal-fail-closed limb

Seat: `MutationC1` (leaf; no subagents, no commits, no production edits).
Round 65, wave `w1`. Date 2026-11-04.

* Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
* Base: `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
* Gate under test: `corpus/instruments/figure-audit.py`
  blob sha256 `8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9`
  (extracted with `git archive`; byte-identical to `git show a283189:… | sha256sum`)
* Scratch: `/fast/scratch/hyaku/kasegi-r65/MutationC1` (removed after receipts copied)
* Receipts: `.ufo/waves/round-65/w1/MutationC1/`
* Report: `.ufo/waves/round-65/w1/MutationC1.md`

The C1 limb was decomposed into five runtime behaviours, each with its own probe:
upstream SIGTERM, upstream SIGKILL, non-final SIGPIPE (benign), final-stage signal
label, and grep exit 1 (benign). Two controls ride along: a clean pipeline and a
held-out pair sharing identical derive *text* with different runtime *status*.

---

## 1. Probe set (built independently; ExecSignalProbes was not read or reused)

All probes are one-figure ledgers `{id, record, recorded, derive, want}` run through
the gate's real CLI `python3 <gate> --ledger L --root R`. Fixtures per probe root:

```
g.txt                                  "35\n"
big.txt                                200000 lines (forces a blocked writer)
corpus/instruments/kill.py             os.kill(getpid(), SIGTERM)
corpus/instruments/kill9.py            os.kill(getpid(), SIGKILL)
corpus/instruments/kill_after.py       writes "35\n", flushes, then SIGTERM
corpus/instruments/maybe_kill.py       SIGTERM only if arm.txt exists, else prints 35
```

Native wait statuses are the Python `returncode` values the gate itself observes
(`Popen.returncode`), measured on the same argv chain; the shell view
(`PIPESTATUS`, i.e. 128+N) is shown for cross-checking.

| Probe | derive | native rc (py) | native rc (bash) | C1 expectation |
|---|---|---|---|---|
| P1 sigterm-upstream | `python3 corpus/instruments/kill.py \| wc -l` | `[-15, 0]` | `[143, 0]` | exit 1, reason names SIGTERM |
| P2 sigkill-upstream | `python3 corpus/instruments/kill9.py \| wc -l` | `[-9, 0]` | `[137, 0]` | exit 1, reason names SIGKILL |
| P3 sigpipe-nonfinal | `cat big.txt \| head -n 1 \| wc -l` | `[-13, 0, 0]` | `[141, 0, 0]` | exit 0, derived `1` (benign) |
| P4 final-signal | `python3 corpus/instruments/kill_after.py` | `[-15]` | `[143]` | exit 1, reason `derive-signal-15`, **never** `derive-exit--15` |
| P5 grep-nomatch | `grep absent g.txt \| wc -l` | `[1, 0]` | `[1, 0]` | exit 0, derived `0` |
| P6 clean-control | `cat g.txt \| wc -l` | `[0, 0]` | `[0, 0]` | exit 0, derived `1` |
| H1 text-only-success | `python3 corpus/instruments/maybe_kill.py \| wc -l` (unarmed) | `[0, 0]` | `[0, 0]` | exit 0, derived `1` |
| H2 text-only-signal | same text as H1 (armed) | `[-15, 0]` | `[143, 0]` | exit 1, reason names SIGTERM |

Scoring of a reason: `derive-signal-N` exactly for P4 (plus a forbid on
`derive-exit--15`); for upstream signals the reason must name the signal either by
name (`sigterm`/`sigkill`) or by the word `signal` plus the bare number. A reason of
the form `derive-upstream-exit--15` is rejected: it is the negative-exit spelling
C1 rules out.

Design note that shaped P4: `run_derive` keeps **only the final stage's stdout**
(`raw, _ = processes[-1].communicate()`); upstream stdout is merely piped into the
next stage. A first P4 built as `cat g.txt | python3 kill.py` therefore collapsed to
`derive-empty` and could only be caught by its label. P4 was rewritten so the final
stage itself emits the recorded value `35` and *then* dies of SIGTERM, which makes
the fail-open path observable as exit 0. That rewrite is what turns m4 below from a
label mismatch into a true accept-on-signal.

## 2. The base gate's observed behaviour (the gap C1 names)

| Probe | base exit | base FIG line | vs C1 |
|---|---|---|---|
| P1 | 0 | `FIG … recorded=0 derived=0 ok` | **fail-open**: upstream -15 counted as success |
| P2 | 0 | `FIG … recorded=0 derived=0 ok` | **fail-open**: upstream -9 counted as success |
| P3 | 0 | `FIG … recorded=1 derived=1 ok` | matches C1 (but undocumented, unpinned) |
| P4 | 1 | `… derived=UNAVAILABLE reason=derive-exit--15 stale` | **wrong label** (`derive-exit--15`) |
| P5 | 0 | `FIG … recorded=0 derived=0 ok` | matches C1 |
| P6 | 0 | `FIG … recorded=1 derived=1 ok` | matches C1 |
| H1 | 0 | `FIG … recorded=1 derived=1 ok` | matches C1 |
| H2 | 0 | `FIG … recorded=0 derived=0 ok` | **fail-open** (same defect as P1) |

Base therefore fails 4/8 probes: P1, P2, P4, H2. `upstream_stale` (`status > 1`, or
`status == 1` for a non-grep head) never sees a negative status, and the final branch
prints `%d` of a negative returncode.

## 3. Family A — one-limb mutants of the base gate (6, as tasked)

Each mutant is a one-hunk patch against `variants/base.py`; `diff -u` shows exactly
one `@@` hunk, `py_compile` clean. "Killed by" lists the probes that reject the
mutant against the C1 contract; "Δ vs base" is the literal reading of *which probe
expectations change* relative to the base gate's own observed outcomes.

| Mutant | single limb change | killed | killed by | Δ vs base | note |
|---|---|---|---|---|---|
| m1 blanket-ignore | `upstream_stale` → `return False` | yes | P1, P2, P4, H2 | **∅** | behaviourally **equivalent to base** under these probes |
| m2 ignore-only-SIGTERM | negatives fatal except `-15` | yes | P1, P2, P3, P4, H2 | P2, P3 | P2 dies on *label* (`derive-upstream-exit--9`); P3 dies because "other signals fatal" swallows SIGPIPE |
| m3 ignore-only-SIGKILL | negatives fatal except `-9` | yes | P1, P2, P3, P4, H2 | P1, P3, H2 | symmetric to m2; P1 dies on label (`derive-upstream-exit--15`) |
| m4 ignore-any-negative-final | final `status < 0` → `status = 0` | yes | P1, P2, P4, H2 | P4 | **true fail-open**: P4 becomes `derived=35 ok`, exit 0 |
| m5 SIGPIPE-fatal | `status == -13` → stale | yes | P1, P2, **P3**, P4, H2 | P3 | P3 is the only unique detector here |
| m6 grep-exit1-fatal | drop the grep exemption | yes | P1, P2, P4, **P5**, H2 | P5 | P5 is the only unique detector here |

Counts (Family A, spec-relative kill — observed ≠ C1 on ≥1 probe):

```
killed=6/6  survivors=0  equivalents=1
```

`equivalents=1` is m1: it is rejected only because it inherits the base gate's own
violations. No probe in this set carries a **non-signal** upstream failure, so m1's
extra regression (every upstream exit ≥1 and >1 now ignored) is invisible here — the
shipped selftest kills it on 17 cases (section 6). This is the main coverage gap of
the five-probe design and it is deliberate: non-signal upstream classes belong to the
existing suite, not to the C1 limb.

Because the base gate is itself non-conforming, Family A cannot measure
load-bearingness cleanly. Family B closes that.

## 4. Family B — single-limb knockouts of a calibration reference (9)

`ref_c1_calibration.py` is a **calibration artefact, not a candidate proposal**: it
adds exactly the C1 limbs (negative upstream statuses stale except SIGPIPE, final
negative status → `derive-signal-N`, upstream negative → `derive-upstream-signal-N`)
and nothing else. It exists so the probe set can be shown satisfiable. It passes
8/8 probes; each knockout below is a one-hunk patch against it.

| Knockout | limb removed | killed by | 
|---|---|---|
| r1 blanket-ignore | all upstream status handling | P1, P2, H2 |
| r2 ignore-only-SIGTERM | SIGTERM exemption only (others fatal) | P1, P3, H2 |
| r3 ignore-only-SIGKILL | SIGKILL exemption only (others fatal) | P2, P3 |
| r4 ignore-negative-final | final-stage signal check | **P4** |
| r5 SIGPIPE-fatal | the benign SIGPIPE exemption | **P3** |
| r6 grep-exit1-fatal | the grep exemption | **P5** |
| r7 SIGTERM-benign | SIGTERM stale, SIGPIPE correctly benign | P1, H2 |
| r8 SIGKILL-benign | SIGKILL stale, SIGPIPE correctly benign | **P2** |
| r9 always-stale | over-strict substitute (all upstream stale) | P3, P5, P6, H1 |

Counts (Family B):

```
killed=9/9  survivors=0  equivalents=0
```

Probe irreplaceability (a probe is irreplaceable if some mutant is killed by it and
by no other):

| Probe | exclusive kill | role |
|---|---|---|
| P1 | — (H2 duplicates it) | SIGTERM upstream stale |
| P2 | r8 | SIGKILL upstream stale |
| P3 | r5 | SIGPIPE benign — the only thing that stops "all negatives fatal" when the SIGTERM/SIGKILL legs are already right |
| P4 | r4 | final-stage signal fail-closed and `derive-signal-15` |
| P5 | r6 | grep exit 1 stays ordinary no-match |
| P6 | — (with P3/P5) | positive control; kills the over-strict r9 |
| H1 | emulator | anti-emulation |
| H2 | — (pairs with P1) | H1's partner; alone adds no discrimination |

r7 is the case that matters for SIGTERM: a gate that treats SIGTERM as benign while
handling SIGKILL and SIGPIPE correctly passes every other probe. P1 (and its pair
H2) is what forces the SIGTERM leg. Likewise r8 forces P2, r5 forces P3, r4 forces
P4, r6 forces P5.

## 5. Semantic emulator — rejected, but only by the held-out pair

`variants/emulator.py` is a drop-in gate that delegates the derive to the base gate
and then **rewrites the FIG line from the derive text alone**: any stage naming
`kill.py` yields `derive-upstream-signal-15` / `derive-signal-15`, `kill9.py` yields
`derive-upstream-signal-9`, `maybe_kill.py` yields a SIGTERM reason. It never looks at
a returncode for the signal limb.

Observed with the five tasked pipelines plus the clean control:

| | P1 | P2 | P3 | P4 | P5 | P6 | H1 | H2 |
|---|---|---|---|---|---|---|---|---|
| emulator | ok | ok | ok | ok | ok | ok | **K** | ok |

The emulator passes 6/6 of the documented probe set and would be **accepted** by a
scoring that stopped there. It is rejected by H1, the unarmed twin of H2: identical
derive text, runtime status `[0, 0]`, so the expected answer is `ok`, while the
text-keyed emulator prints `reason=derive-upstream-signal-15 stale` and exits 1.
H1 and H2 are only decisive as a pair — a gate that hardcodes "ok" for that text
fails H2, a gate that hardcodes "signal" fails H1.

Consequence for C1's own selftest: a case that only feeds the five named pipelines
proves nothing about the implementation being status-driven. The pinned control must
pair a does-die and a does-not-die case on the *same* command text.

## 6. The shipped selftest as the competing detector (59 cases, `--selftest`)

Run for every variant with `HYAKU_SCRATCH` inside this scratch. `S` =
`upstream-python-signal-ignored`, the case that pins the current bug.

| Variant | rc | failures | distinguishable from ref? | reading |
|---|---|---|---|---|
| base | 0 | 0 | — | suite is green while the bug is live |
| ref_c1_calibration | 1 | 1 (`S`) | — | **the suite must change for C1 to be admissible** |
| m1 / r1 | 1 | 17 | yes | non-signal upstream classes |
| m2 ignore-only-SIGTERM | 0 | 0 | **no** | suite cannot see SIGTERM still benign |
| m3 ignore-only-SIGKILL | 1 | 1 (`S`) | **no** | suite has no SIGKILL case |
| m4 ignore-negative-final | 0 | 0 | **no** | no final-signal case at all; fail-open passes |
| m5 SIGPIPE-fatal | 0 | 0 | **no** | no SIGPIPE case at all |
| r2 SIGTERM benign + SIGPIPE fatal | 0 | 0 | **no** | suite accepts it outright |
| r3 SIGKILL benign | 1 | 1 (`S`) | **no** | identical to ref |
| r4 final signal ignored | 1 | 1 (`S`) | **no** | identical to ref |
| r5 SIGPIPE fatal | 1 | 1 (`S`) | **no** | identical to ref; only `S` reacts, via SIGTERM |
| r6 grep exit1 fatal | 1 | 3 | yes | the two grep cases react |
| r7 SIGTERM benign | 0 | 0 | **no** | suite accepts it outright |
| r8 SIGKILL benign | 1 | 1 (`S`) | **no** | identical to ref |
| r9 always-stale | 1 | 7 | yes | over-strict, trips clean/grep/count positives |

Three consequences, stated plainly:

1. **The shipped suite is blind to three of the four C1 legs.** SIGKILL (r8 ≡ ref),
   final-stage signal (r4 ≡ ref, m4 passes outright) and SIGPIPE (r5 ≡ ref, m5
   passes outright) have zero shipped coverage. Only the SIGTERM leg is touched, and
   it is **inverted**: the suite requires the buggy behaviour (`S` expects exit 0), so
   a correct C1 candidate fails the suite until `S` is flipped or replaced.
2. A plausible substitute that merely stops the SIGTERM leak (m2, r2, r7) is
   **green on the entire shipped suite**. So is the final-stage fail-open (m4) and
   the over-strict SIGPIPE handling (m5). A C1 candidate whose selftest edits stop at
   "S now expects 1" would admit those substitutes.
3. The "pinned positive control" for SIGPIPE demanded by C1 does not exist today;
   m5's 0 failures is direct evidence. Any C1 selftest must add a SIGPIPE case, a
   SIGKILL case and a final-signal case, or the limb remains unpinned.

## 7. What these probes cannot distinguish

* **Non-signal upstream failures.** No probe carries an upstream exit ≥2 or a
  non-grep exit 1, so m1 (blanket ignore) is behaviourally equal to the base gate
  here. Detection of that regression comes only from the shipped suite (17 cases).
* **Documentation / pinning.** "SIGPIPE stays an explicit, documented benign case
  with a pinned positive control" is a property of the source text and the selftest,
  not of a runtime observation. P3 only proves the *behaviour* is benign; it cannot
  tell deliberate exemption from carelessness. m5 and the shipped suite both show
  the pin is the load-bearing artefact.
* **SIGPIPE on the final stage.** P3 is non-final only. A gate that is benign for
  non-final SIGPIPE and fatal for final SIGPIPE (or vice versa) is not probed.
* **Signals other than 15, 9, 13.** SIGINT, SIGQUIT, SIGSEGV, SIGABRT, SIGALRM are
  unprobed; a gate that ignores them survives everything here.
* **Which stage is reported when several stages die.** Each probe has at most one
  negative stage, so first-stage precedence and the `&&` group ordering are untested.
* **Reason spelling beyond the required tokens.** P1/P2/H2 accept `sigterm`/`sigkill`
  or `signal`+number and reject `derive-upstream-exit--15`. A reason that names the
  signal another way (e.g. "terminated", "killed") would be marked a failure even if
  semantically correct; P4 requires the exact label `derive-signal-15`.
* **Multi-figure ledgers.** Every probe is one figure; figure ordering, aggregation
  of `ok`/`stale` counts, and exit-code precedence across figures are not covered.
* **Text-keyed emulation of other limbs.** H1/H2 only defeat emulation of the SIGTERM
  upstream leg. An emulator that fakes the SIGKILL or final-signal reason by text is
  killed only by P2/P4 as probes, not by a paired text twin — those have no twin here.
* **Timeout and exec-error paths** (`derive-timeout`, `derive-exec-error-*`) are not
  touched by the C1 limb and are not probed.

## 8. Reading for the integrator

* The limb is load-bearing: with a conforming reference, every one-limb knockout is
  detected (9/9), and each of P2, P3, P4, P5 has at least one exclusive kill. The
  SIGPIPE exemption is not cosmetic — two of the natural partial fixes (m2/m3, and
  their refined forms r2/r3) break it, so a candidate that adds "any other negative
  status is stale" without an explicit `-13` exemption will be caught by P3 alone.
* The final-signal check must precede the value comparison. m4 shows the concrete
  fail-open: `derived=35`, `want=35`, exit 0 on a stage that died of SIGTERM.
* A correct candidate **cannot pass the shipped selftest unchanged**: `S`
  (`upstream-python-signal-ignored`) pins the bug. The suite has 59 cases; the
  reference fails exactly that one, so 58 stay green. Flipping/replacing `S` and
  adding one control each for SIGKILL, non-final SIGPIPE and final-stage signal
  gives ≥62 cases, and all three new controls are required: without them, m4,
  m5 and r8 are green (section 6). The two grep positives and the clean pipeline
  are unaffected by the reference in every run.
* If the selftest is extended with only the five named pipelines as fixture cases,
  the semantic emulator in section 5 passes them. The pinned controls must include a
  same-text/different-status pair (H1/H2) or a status-blind implementation ships.

## 9. Reproduction

All commands were run with the shell in the stated directory; no relative writes
outside scratch.

```sh
# base extraction + provenance
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive \
    a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b corpus/instruments/figure-audit.py | tar -x
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show \
    a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b:corpus/instruments/figure-audit.py | sha256sum

# mutants (one hunk each)
cp variants/base.py variants/m1_blanket_ignore.py
patch -s variants/m1_blanket_ignore.py patches/m1_blanket_ignore.patch
# … same for m2..m6; r1..r9 are one-hunk patches on variants/ref_c1_calibration.py
diff -u variants/base.py variants/m1_blanket_ignore.py | grep -c '^@@'   # 1
python3 -m py_compile variants/m1_blanket_ignore.py

# probe matrices
python3 probe.py --work work  --gates '<JSON [[name,path],…]>' --out results/matrix.json
python3 probe.py --work work2 --gates '<JSON [[name,path],…]>' --out results/matrix-ref.json

# shipped selftest as competing detector
HYAKU_SCRATCH=/fast/scratch/hyaku/kasegi-r65/MutationC1/tmp \
    python3 variants/<variant>.py --selftest
```

Final matrix (Family A):

```
gate                     P1  P2  P3  P4  P5  P6  H1  H2
base                     K   K   ok  K   ok  ok  ok  K
m1_blanket_ignore        K   K   ok  K   ok  ok  ok  K
m2_ignore_only_SIGTERM   K   K   K   K   ok  ok  ok  K
m3_ignore_only_SIGKILL   K   K   K   K   ok  ok  ok  K
m4_ignore_neg_final      K   K   ok  K   ok  ok  ok  K
m5_SIGPIPE_fatal         K   K   K   K   ok  ok  ok  K
m6_grep_exit1_fatal      K   K   ok  K   K   ok  ok  K
ref_c1_calibration       ok  ok  ok  ok  ok  ok  ok  ok
emulator                 ok  ok  ok  ok  ok  ok  K   ok
```

Final matrix (Family B):

```
gate                     P1  P2  P3  P4  P5  P6  H1  H2
ref_c1_calibration       ok  ok  ok  ok  ok  ok  ok  ok
r1_blanket_ignore        K   K   ok  ok  ok  ok  ok  K
r2_ignore_only_SIGTERM   K   ok  K   ok  ok  ok  ok  K
r3_ignore_only_SIGKILL   ok  K   K   ok  ok  ok  ok  ok
r4_ignore_neg_final      ok  ok  ok  K   ok  ok  ok  ok
r5_SIGPIPE_fatal         ok  ok  K   ok  ok  ok  ok  ok
r6_grep_exit1_fatal      ok  ok  ok  ok  K   ok  ok  ok
r7_SIGTERM_benign        K   ok  ok  ok  ok  ok  ok  K
r8_SIGKILL_benign        ok  K   ok  ok  ok  ok  ok  ok
r9_always_stale          ok  ok  K   ok  K   K   K   ok
emulator                 ok  ok  ok  ok  ok  ok  K   ok
```

## 10. Artefacts and hashes

Base and variants (sha256):

```
8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9  base.py
530aa5033a46d2f0259c23f0b94acb735b439a3cee931468de9febafa0558347  ref_c1_calibration.py
8ac50435e23758f010bdf18137e72d9e6b9881ca1f46d79282d1a90adab9d9fc  m1_blanket_ignore.py
468926b285362359a740d317e547570db0598f4764ba4d1d5c9be9964e88cc25  m2_ignore_only_sigterm.py
cc97ebed1d1f96f69fb268563725c44b0c1776336b03add4db7b92ea647a06f1  m3_ignore_only_sigkill.py
2f02b2db1e1dfd92708e61241654a3ccd9bc4df932131d66391319cec8e95fe2  m4_ignore_any_negative_final.py
fb1512b36aa3d9a26f06e8fa8c79cd6031afd91b83c3281c43e19b28f305e7cb  m5_sigpipe_fatal.py
7fa3372788c8308ca705e5613278927e2407330f2bfa7b735e6f775d4e1c3bf9  m6_grep_exit1_fatal.py
be9327e3be1d2497321511702c86402b9875bf3f00029275a5248956f9a78ddc  r1_blanket_ignore.py
6a25a8656527b56bce937334045230fd99ec0079f9e68950225040b77760b5ee  r2_ignore_only_sigterm.py
b2bc5bbcc1d200e4aa49cadd99b93a617674d9babfa88cc9574597680a735aaa  r3_ignore_only_sigkill.py
cfd6cb2864123ecb644090a16aeac6bc84ffbfdf94f1ebc19d5ab6ab9161196a  r4_ignore_negative_final.py
58b264ba0febd535d9273a7abb71a1179b251fdb3bb690163df3acb439e36e00  r5_sigpipe_fatal.py
cfe7d94bfacf344426842a082806c4996fbf9af4dd732ffcd5a99f59305e540b  r6_grep_exit1_fatal.py
e55bdb28c0dda75f159a84fb7c77b188b1abdd9275ab0c00e3df826bf71cc751  r7_sigterm_benign.py
360e1aac9dba8b62c351fbe84b8b09b25c687f4f239e4b78ae793df7a23b3606  r8_sigkill_benign.py
960ab71695de3d36670dd76bec68e8e73c23a20206cc8489b22ef5625798e1bb  r9_always_stale.py
895e37f02393b6496854d5c352c5ad603be870061fbe87e4921b8dc836ca0f6a  emulator.py
```

Receipt bundle (copied before scratch removal):

```
MutationC1/probe.py                    harness (fixtures, runner, scorer)
MutationC1/variants/*.py               exact bytes (base, ref, m*, r*, emulator)
MutationC1/patches/*.patch             one-hunk mutant patches (15) + ref_a/b/c (3)
MutationC1/results/matrix.json         Family A raw observations + natives
MutationC1/results/matrix-ref.json     Family B raw observations + natives
MutationC1/results/selftest-*.txt      shipped selftest output per variant (17)
```

Tooling: no installs and no package-manager transactions were performed; Python 3
from PATH and the base gate's own stdlib only.

## 11. No production edit

Nothing outside `/fast/scratch/hyaku/kasegi-r65/MutationC1` and
`.ufo/waves/round-65/w1/MutationC1{,.md}` was written. No git/jj mutation, no
commit, no push, no subagent. `ref_c1_calibration.py` is a scratch calibration
artefact, explicitly not a candidate implementation for integration.

Lane movement during this seat, recorded so the provenance is not misread: the
lane's `HEAD` advanced from the tested base `a283189` to `a333d8e` while this seat
ran (`1c36d72` lands a C1 gate; `SKILL.md` carries an uncommitted `r65 correction`
edit and `.ufo/waves/round-65/controls/final-verification-r65.txt` appeared). None
of that is this seat's work and none of it was used here — every observation above
is from the base blob whose sha256 is pinned in the header. The landed candidate was
not read, run or judged by this seat; that is the reviewers' and L1's call.
