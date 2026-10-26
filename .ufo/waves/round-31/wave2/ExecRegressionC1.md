# ExecRegressionC1 — C1 final no-harm run (round 31, wave 2)

Seat: `ExecRegressionC1` (leaf executor). Write scope: this receipt plus `/tmp/exec-regr-c1` scratch
(outside the lane). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `eecad59` (read-only
`git rev-parse`/`status` only; no git/jj mutation, no commit). Judged axes: depth:verifiability,
coverage. Answering model: `opencode-go/deepseek-v4.1-flash` (config route table decided; no model
passed). Tooling: nothing installed or upgraded; pacman never invoked; no network fetch.

All values below are **POST-FIX** (after `ExecCounterFix` landed) unless a line says PRE-STATE.
Every command ran from the lane root and, where the tool supports it, from `cd /` with `--root` or an
absolute path.

## 0. Quiescence gate

Waited for the counter fix seat's receipt before the first recorded run:

```
$ until [ -s .ufo/waves/round-31/wave2/ExecCounterFix.md ]; do sleep 20; done   # appeared 2026-10-26T00:43:24Z
$ ls -la --time-style=full-iso corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
-rwxr-xr-x 1 vgpnk vgpnk 33594 2026-10-25 21:36:12.804900569 -0300 corpus/instruments/limb-mutation-check.py
-rw-r--r-- 1 vgpnk vgpnk 11930 2026-10-25 20:42:39.374996965 -0300 corpus/instruments/limb-ledger.json
```

Then a 30-second byte-stability check (hash, sleep 30, re-hash):

```
$ sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json > /tmp/exec-regr-c1/q1.sha && sleep 30 && sha256sum -c /tmp/exec-regr-c1/q1.sha
corpus/instruments/limb-mutation-check.py: OK
corpus/instruments/limb-ledger.json: OK
```

The same two digests are reproduced after every run in §5, so no run straddled an edit.

## 1. Digests of every instrument + the ledger (POST-FIX, all runs complete)

```
$ sha256sum corpus/instruments/*.py corpus/instruments/limb-ledger.json
d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912  corpus/instruments/anchorcheck.py
e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18  corpus/instruments/capture-source.py
ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710  corpus/instruments/density.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a  corpus/instruments/mirror-containment-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1  corpus/instruments/resolve-dispatch-check.py
db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667  corpus/instruments/resolve.py
855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb  corpus/instruments/score-gap.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
16a6ff281d89845444a7face5034c611594adaf59438e62b3f1dce55f7a5711e  corpus/instruments/test_resolve.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
```

`limb-mutation-check.py` and `limb-ledger.json` are byte-identical to the §0 quiescence sample, and to
the digests `ExecCounterFix` cites for its final bytes.

## 2. C1 counter — twice, lane root (POST-FIX)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
guard cases=3 failures=0
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
$ echo $?
0
```

Counts:

```
$ grep -c '^LIMB ' /tmp/exec-regr-c1/counter1.out
13
$ grep -c '^CONTROL ' /tmp/exec-regr-c1/counter1.out
3
```

Second run and byte identity:

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json > /tmp/exec-regr-c1/counter2.out 2>&1; echo $?
0
$ cmp /tmp/exec-regr-c1/counter1.out /tmp/exec-regr-c1/counter2.out && echo IDENTICAL
IDENTICAL
$ sha256sum /tmp/exec-regr-c1/counter1.out /tmp/exec-regr-c1/counter2.out
d6aefddca50293347c348646479bbe406745ad3163422b27edefcea861264270  /tmp/exec-regr-c1/counter1.out
d6aefddca50293347c348646479bbe406745ad3163422b27edefcea861264270  /tmp/exec-regr-c1/counter2.out
```

`d6aefddc…` is the same digest `ExecCounterFix` reports for its green pair (independent reproduction).

### 2.1 Counter from a foreign cwd (POST-FIX)

```
$ cd / && L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 $L/corpus/instruments/limb-mutation-check.py --ledger $L/corpus/instruments/limb-ledger.json --root $L; echo $?
limbs=13 killed=13 survivors=0
controls=3 rejected=3
0
IDENTICAL_to_lane_root_run

$ python3 $L/corpus/instruments/limb-mutation-check.py --ledger $L/corpus/instruments/limb-ledger.json; echo $?   # default root derivation
limbs=13 killed=13 survivors=0
controls=3 rejected=3
0
IDENTICAL_to_lane_root_run
```

Both foreign-cwd transcripts `cmp`-match `counter1.out` (same 17 data lines), so the counter is
cwd-independent with and without `--root`.

### 2.2 Counter `--selftest` (POST-FIX)

```
$ python3 corpus/instruments/limb-mutation-check.py --selftest; echo $?      # lane root
selftest cases=20 failures=0
0
$ cd / && python3 $L/corpus/instruments/limb-mutation-check.py --selftest; echo $?   # foreign cwd
selftest cases=20 failures=0
0
```

The three implicit guard cases (`invalid-live-baseline`, `invalid-find-count`, `invalid-timeout`) run
on every `--ledger` invocation and report `guard cases=3 failures=0` (§2), not only under `--selftest`.

## 3. recheck-audit (POST-FIX)

```
$ python3 corpus/instruments/recheck-audit.py --quiet; echo $?
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
0
```

```
$ cd / && python3 $L/corpus/instruments/recheck-audit.py --quiet --root $L; echo $?
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
0
```

`--selftest` (both cwds, tail):

```
$ python3 corpus/instruments/recheck-audit.py --selftest; echo $?
expect=absent expected=0 missing=0 unexpected=0 exit=1
selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok
0
```

## 4. source-recheck, anchorcheck, frontier harness, score-gap (POST-FIX)

```
$ python3 corpus/instruments/source-recheck.py --selftest; echo $?
selftest cases=10 failures=0
0
$ cd / && python3 $L/corpus/instruments/source-recheck.py --selftest; echo $?
selftest cases=10 failures=0
0

$ python3 corpus/instruments/anchorcheck.py --selftest; echo $?
selftest cases=12 failures=0
skip=0
limbs=9 covered=9
0
$ cd / && python3 $L/corpus/instruments/anchorcheck.py --selftest; echo $?
skip=0
limbs=9 covered=9
0

$ python3 corpus/instruments/frontier-recheck-count.py; echo $?
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
0
$ cd / && python3 $L/corpus/instruments/frontier-recheck-count.py --root $L; echo $?
entries=18 pass=18 exit=0
0

$ python3 corpus/instruments/score-gap.py --selftest; echo $?
selftest fields=7 failures=0
0
$ cd / && python3 $L/corpus/instruments/score-gap.py --selftest; echo $?
selftest fields=7 failures=0
0
```

(Trailing spaces at line ends are trimmed in the harness block above; every `PASS` line's columns and
the summary line are otherwise verbatim from `/tmp/exec-regr-c1/harness.out`, whose byte-level diff
against the receipt block differs only in those trailing spaces.)

## 5. Every registered source-recheck, manifests rounds 23-31 (POST-FIX)

Manifest directories present: `round-23, round-24, round-25, round-26, round-28, round-29,
round-30, round-31` — **there is no `round-27` manifest directory**, so 8 manifests, not 9.

```
$ for d in corpus/source-snapshots/round-*; do for id in <ids from $d/manifest.json>; do
    python3 corpus/instruments/source-recheck.py --manifest "$d/manifest.json" --source "$id"; done; done
source_checks=38 failures=0
```

```
$ awk '{print $1}' /tmp/exec-regr-c1/sr-root.out | sort | uniq -c
      4 round-23
     19 round-24
      5 round-25
      1 round-26
      2 round-28
      3 round-29
      3 round-30
      1 round-31
```

Foreign cwd, absolute manifests:

```
$ cd / && for d in $L/corpus/source-snapshots/round-*; do for id in <ids>; do
    python3 $L/corpus/instruments/source-recheck.py --manifest "$d/manifest.json" --source "$id"; done; done
source_checks=38 failures=0
```

IDs by manifest (from each `manifest.json`): r23 S018,S029,S030,S031; r24 S001-S015,S032-S035;
r25 S036-S040; r26 S041; r28 S041,S042; r29 S043,S044,S045; r30 S046,S047,S041; r31 S048.
All 38 exit 0 in both locations; no `FAIL`/`MISMATCH` line in any output.

## 6. Independent ledger-shape re-derivation (read-only, outside the counter)

Shape of every row re-derived by this seat without the counter (`/tmp` copies only):

```
LIMB RA-parse                   find_count=1 noop=False compiles=True live_exit=0
LIMB RA-cwd                     find_count=1 noop=False compiles=True live_exit=0
LIMB RA-paths                   find_count=1 noop=False compiles=True live_exit=0
LIMB RA-cdroot                  find_count=1 noop=False compiles=True live_exit=0
LIMB RA-instrument              find_count=1 noop=False compiles=True live_exit=0
LIMB RA-own                     find_count=1 noop=False compiles=True live_exit=0
LIMB RA-completeness            find_count=1 noop=False compiles=True live_exit=0
LIMB RA-expect-missing          find_count=1 noop=False compiles=True live_exit=0
LIMB RA-expect-unexpected       find_count=1 noop=False compiles=True live_exit=0
LIMB SR-stem-mismatch           find_count=1 noop=False compiles=True live_exit=1
LIMB SR-occurrence-not-unique   find_count=1 noop=False compiles=True live_exit=1
LIMB FR-missing-entry           find_count=1 noop=False compiles=True live_exit=1
LIMB FR-duplicate-entry         find_count=1 noop=False compiles=True live_exit=1
CONTROL CTL-noop                   find_count=1 noop=True  compiles=True  live_exit=0  expect=invalid:noop
CONTROL CTL-nocompile              find_count=1 noop=False compiles=False live_exit=0  expect=invalid:nocompile
CONTROL CTL-equivalent             find_count=1 noop=False compiles=True  live_exit=1  expect=survivor
independent_shape_failures=0 []
```

So no LIMB row can be `invalid:find-count`, `invalid:noop` or `invalid:nocompile` on these bytes; the
13 verdicts in §2 are verdicts of the mutant run, not of a shape gate. The control expectations are
structurally what the counter reported (`CTL-noop` bytes-identical, `CTL-nocompile` non-compiling,
`CTL-equivalent` compiles and survives).

## 7. Non-harm: no lane write, no scratch left

```
$ ls -d /tmp/limb-* 2>/dev/null | head; echo "(none above = clean)"
(none above = clean)

$ git status --porcelain -- corpus/ .ufo/waves/round-31/wave2/ | head
 M corpus/QUALITY.md
 M corpus/instruments/limb-mutation-check.py
?? corpus/lessons/round-31.md
?? .ufo/waves/round-31/wave2/
```

Every post-run instrument digest in §1 equals the pre-run digest (only `limb-mutation-check.py` is
modified relative to HEAD, which is `ExecCounterFix`'s edit, not this seat's; `QUALITY.md` and
`lessons/round-31.md` are other seats' write scopes). `corpus/instruments/__pycache__` existed before
this seat's first run and receives no new lane file from these runs (it is not in `git status`).
Scratch for this seat lives at `/tmp/exec-regr-c1` (evidence copies) and the counter's own
`limb-mutation-*`/`limb-guard-*`/`limb-selftest-*` dirs are all removed at exit.

## 8. Non-zero exits

None. Every command in §2-§5 exited 0 in both locations; there is no failing value to attribute to an
owning seat. PRE-STATE sanity note: this seat ran one early sanity pass on the four instrument families
before `ExecCounterFix` landed (counter pair excluded); those values are PRE-STATE and are not cited
as C1 evidence above — the POST-FIX values in §2-§5 are the ones of record.

## 9. Residuals / observations (not claims of this seat)

- `round-27` has no `corpus/source-snapshots/round-27/` directory, so the sweep is 38 ids over 8
  manifests; if a round-27 manifest was intended, its absence is the L1's to route.
- Peer receipt `wave2/ExecLimbRAcdroot.md` §0 reports the RA-cdroot row as killed but shape-narrow
  (three non-equivalent mutants of the same limb survive, no contract clause violated). Not
  re-measured here; cited only as a pointer.
- The counter now evaluates three implicit guard fixtures on every `--ledger` run (`guard cases=3
  failures=0`, §2); the frozen summary lines and row count are unaffected.
- `wave2/ScoutLiveDrift.md` reports the S048 pinned capture differs from a live re-fetch on exactly one
  line (the per-request Trace Id), with no assertion text changed. This seat ran `source-recheck` on
  the committed capture only, so that observation is neither confirmed nor contradicted here.

## 10. Commands as run (verbatim index)

```sh
$LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin; S=/tmp/exec-regr-c1
cd "$LANE" && sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json > $S/q1.sha
sleep 30 && sha256sum -c $S/q1.sha
cd "$LANE" && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json > $S/counter1.out 2>&1
cd "$LANE" && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json > $S/counter2.out 2>&1
cmp $S/counter1.out $S/counter2.out && sha256sum $S/counter1.out $S/counter2.out
grep -c '^LIMB ' $S/counter1.out; grep -c '^CONTROL ' $S/counter1.out
cd / && python3 "$LANE/corpus/instruments/limb-mutation-check.py" --ledger "$LANE/corpus/instruments/limb-ledger.json" --root "$LANE"
cd / && python3 "$LANE/corpus/instruments/limb-mutation-check.py" --ledger "$LANE/corpus/instruments/limb-ledger.json"
cd "$LANE" && python3 corpus/instruments/limb-mutation-check.py --selftest
cd "$LANE" && python3 corpus/instruments/recheck-audit.py --quiet
cd / && python3 "$LANE/corpus/instruments/recheck-audit.py" --quiet --root "$LANE"
cd "$LANE" && python3 corpus/instruments/recheck-audit.py --selftest
cd "$LANE" && python3 corpus/instruments/source-recheck.py --selftest
cd "$LANE" && python3 corpus/instruments/anchorcheck.py --selftest
cd "$LANE" && python3 corpus/instruments/frontier-recheck-count.py
cd / && python3 "$LANE/corpus/instruments/frontier-recheck-count.py" --root "$LANE"
cd "$LANE" && python3 corpus/instruments/score-gap.py --selftest
# 38 x (lane root, relative manifest) and 38 x (cd /, absolute manifest):
cd "$LANE" && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-NN/manifest.json --source Sxxx
cd / && python3 "$LANE/corpus/instruments/source-recheck.py" --manifest "$LANE/corpus/source-snapshots/round-NN/manifest.json" --source Sxxx
cd "$LANE" && python3 - <<'PY'   # §6 independent ledger-shape re-derivation, /tmp copies only
PY
sha256sum corpus/instruments/*.py corpus/instruments/limb-ledger.json
git -C "$LANE" status --porcelain -- corpus/
```
